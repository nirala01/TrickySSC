// trickyssc-play — Cloudflare Worker for Google Play purchases made in the TrickySSC Android app.
//
// The app sends:  POST /verify  { idToken, productId, purchaseToken, amount }
//   1. the Firebase ID token is checked            -> who is buying (uid)
//   2. the purchase is checked with Google Play    -> it is real and paid
//   3. entitlements/{uid}.modules[<pass>] is set   -> the pass opens in the app and on the website
//   4. a row is added to payments (My orders) and the purchase is consumed (so it can be renewed later)
//
// One secret, set in Cloudflare (Worker -> Settings -> Variables and Secrets), never in this file:
//   GOOGLE_SA_JSON = the whole service-account JSON of the Firebase project.
// The same service account must be added in Play Console -> Users and permissions
// (permission: "View financial data, orders" + "Manage orders and subscriptions"),
// and the "Google Play Android Developer API" must be enabled in the Google Cloud project.

const PACKAGE = 'com.trickyssc.app';
const VALID_DAYS = 365;
const PRODUCTS = {
  pass_ssc_cgl: { key: 'ssc-cgl-mocks', label: 'SSC CGL Mock Test Series' },
  pass_ssc_chsl: { key: 'ssc-chsl-mocks', label: 'SSC CHSL Mock Test Series' },
  pass_ssc_mts: { key: 'ssc-mts-mocks', label: 'SSC MTS Mock Test Series' },
  pass_ssc_gd: { key: 'ssc-gd-mocks', label: 'SSC GD Constable Mock Test Series' },
  pass_rrb_ntpc: { key: 'rrb-ntpc-mocks', label: 'RRB NTPC Mock Test Series' },
  pass_all_mocks: { key: 'all-mocks', label: 'All Mock Test Series' },
};

const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'content-type': 'application/json' } });
const b64u = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const b64uText = (s) => b64u(new TextEncoder().encode(s));
const fromB64u = (s) => Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/')), (c) => c.charCodeAt(0));

// ---- Google access token from the service account (cached while the Worker stays warm)
let tokenCache = { token: '', exp: 0 };
async function accessToken(sa) {
  const now = Math.floor(Date.now() / 1000);
  if (tokenCache.token && tokenCache.exp - 60 > now) return tokenCache.token;
  const head = b64uText(JSON.stringify({ alg: 'RS256', typ: 'JWT' }));
  const claim = b64uText(JSON.stringify({
    iss: sa.client_email,
    scope: 'https://www.googleapis.com/auth/androidpublisher https://www.googleapis.com/auth/datastore',
    aud: 'https://oauth2.googleapis.com/token', iat: now, exp: now + 3600,
  }));
  const pem = sa.private_key.replace(/-----[A-Z ]+-----/g, '').replace(/\s+/g, '');
  const key = await crypto.subtle.importKey('pkcs8', Uint8Array.from(atob(pem), (c) => c.charCodeAt(0)), { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['sign']);
  const sig = b64u(await crypto.subtle.sign('RSASSA-PKCS1-v1_5', key, new TextEncoder().encode(head + '.' + claim)));
  const r = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: 'grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=' + head + '.' + claim + '.' + sig,
  });
  const j = await r.json();
  if (!j.access_token) throw new Error('google-auth');
  tokenCache = { token: j.access_token, exp: now + (j.expires_in || 3600) };
  return j.access_token;
}

// ---- Firebase ID token -> uid
let jwks = { keys: [], at: 0 };
async function verifyIdToken(idToken, projectId) {
  const [h, p, s] = String(idToken || '').split('.');
  if (!h || !p || !s) return null;
  const head = JSON.parse(new TextDecoder().decode(fromB64u(h)));
  const body = JSON.parse(new TextDecoder().decode(fromB64u(p)));
  const now = Math.floor(Date.now() / 1000);
  if (head.alg !== 'RS256' || body.aud !== projectId || body.iss !== 'https://securetoken.google.com/' + projectId) return null;
  if (!body.sub || body.exp < now || body.iat > now + 300) return null;
  if (Date.now() - jwks.at > 3600000 || !jwks.keys.find((k) => k.kid === head.kid)) {
    const r = await fetch('https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com');
    jwks = { keys: (await r.json()).keys || [], at: Date.now() };
  }
  const jwk = jwks.keys.find((k) => k.kid === head.kid);
  if (!jwk) return null;
  const key = await crypto.subtle.importKey('jwk', jwk, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify']);
  const ok = await crypto.subtle.verify('RSASSA-PKCS1-v1_5', key, fromB64u(s), new TextEncoder().encode(h + '.' + p));
  return ok ? body.sub : null;
}

// ---- Firestore (REST, as the service account)
const fsBase = (pid) => `https://firestore.googleapis.com/v1/projects/${pid}/databases/(default)/documents`;
const ts = (ms) => ({ timestampValue: new Date(ms).toISOString() });
const str = (v) => ({ stringValue: String(v) });
async function fsGet(pid, tok, path) {
  const r = await fetch(`${fsBase(pid)}/${path}`, { headers: { authorization: 'Bearer ' + tok } });
  return r.status === 200 ? r.json() : null;
}
async function fsPatch(pid, tok, path, fields, mask, extra = '') {
  const q = mask.map((m) => 'updateMask.fieldPaths=' + encodeURIComponent(m)).join('&');
  const r = await fetch(`${fsBase(pid)}/${path}?${q}${extra}`, {
    method: 'PATCH', headers: { authorization: 'Bearer ' + tok, 'content-type': 'application/json' }, body: JSON.stringify({ fields }),
  });
  return r.status;
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (req.method === 'GET') return json({ ok: true, service: 'trickyssc-play' });
    if (req.method !== 'POST' || url.pathname !== '/verify') return json({ ok: false, error: 'not-found' }, 404);
    try {
      if (!env.GOOGLE_SA_JSON) return json({ ok: false, error: 'not-configured' }, 500);
      const sa = JSON.parse(env.GOOGLE_SA_JSON);
      const pid = sa.project_id;
      const b = await req.json();
      const product = PRODUCTS[b.productId];
      const purchaseToken = String(b.purchaseToken || '');
      if (!product || purchaseToken.length < 20) return json({ ok: false, error: 'bad-request' }, 400);
      const uid = await verifyIdToken(b.idToken, pid);
      if (!uid) return json({ ok: false, error: 'sign-in' }, 401);

      // 1. is the purchase real and paid?
      const tok = await accessToken(sa);
      const api = `https://androidpublisher.googleapis.com/androidpublisher/v3/applications/${PACKAGE}/purchases/products/${b.productId}/tokens/${encodeURIComponent(purchaseToken)}`;
      const gr = await fetch(api, { headers: { authorization: 'Bearer ' + tok } });
      if (gr.status !== 200) return json({ ok: false, error: 'not-found-at-google', status: gr.status }, 402);
      const g = await gr.json();
      if (g.purchaseState === 2) return json({ ok: false, error: 'pending' }, 202);   // e.g. cash / slow UPI: Play tells the app again when it is paid
      if (g.purchaseState !== 0) return json({ ok: false, error: 'not-paid' }, 402);
      if (g.obfuscatedExternalAccountId && g.obfuscatedExternalAccountId !== uid) return json({ ok: false, error: 'other-account' }, 409);

      // 2. one purchase unlocks one account, once
      const hash = b64u(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(purchaseToken)));
      const recPath = `play_purchases/${hash}`;
      let rec = await fsGet(pid, tok, recPath);
      let expMs;
      if (rec) {
        const f = rec.fields || {};
        if ((f.uid || {}).stringValue !== uid) return json({ ok: false, error: 'used' }, 409);
        expMs = Date.parse((f.expiresAt || {}).timestampValue);
        if ((f.status || {}).stringValue === 'granted') return json({ ok: true, key: product.key, expiresAt: expMs, repeat: true });
      } else {
        const ent = await fsGet(pid, tok, `entitlements/${uid}`);
        const cur = ((((((ent || {}).fields || {}).modules || {}).mapValue || {}).fields || {})[product.key] || {}).mapValue;
        const curExp = cur && (cur.fields.active || {}).booleanValue === true ? Date.parse((cur.fields.expiresAt || {}).timestampValue) : 0;
        expMs = Math.max(Date.now(), curExp > Date.now() ? curExp : 0) + VALID_DAYS * 86400000;   // renewing early adds a year on top
        const st = await fsPatch(pid, tok, recPath, {
          uid: str(uid), productId: str(b.productId), key: str(product.key), orderId: str(g.orderId || ''), status: str('pending'),
          expiresAt: ts(expMs), createdAt: ts(Date.now()),
        }, ['uid', 'productId', 'key', 'orderId', 'status', 'expiresAt', 'createdAt'], '&currentDocument.exists=false');
        if (st !== 200) return json({ ok: false, error: 'busy' }, 409);
      }

      // 3. open the pass
      const grant = { mapValue: { fields: { active: { booleanValue: true }, expiresAt: ts(expMs), source: str('google-play'), orderId: str(g.orderId || '') } } };
      const st = await fsPatch(pid, tok, `entitlements/${uid}`, { modules: { mapValue: { fields: { [product.key]: grant } } }, updatedAt: ts(Date.now()) },
        ['modules.`' + product.key + '`', 'updatedAt']);
      if (st !== 200) return json({ ok: false, error: 'grant-failed' }, 500);

      // 4. order row for "My orders", mark done, consume (lets the student renew next year)
      const amount = Number(b.amount);
      await fsPatch(pid, tok, `payments/play_${hash}`, {
        uid: str(uid), status: str('paid'), gateway: str('google-play'), productId: str(b.productId), courseId: str(product.key), productLabel: str(product.label),
        amount: isFinite(amount) && amount > 0 && amount < 100000 ? { doubleValue: amount } : str(''),
        paymentId: str(g.orderId || ''), orderId: str(g.orderId || ''), paidAt: ts(Number(g.purchaseTimeMillis) || Date.now()), createdAt: ts(Date.now()),
      }, ['uid', 'status', 'gateway', 'productId', 'courseId', 'productLabel', 'amount', 'paymentId', 'orderId', 'paidAt', 'createdAt']);
      await fsPatch(pid, tok, recPath, { status: str('granted') }, ['status']);
      await fetch(api + ':consume', { method: 'POST', headers: { authorization: 'Bearer ' + tok } }).catch(() => {});
      return json({ ok: true, key: product.key, expiresAt: expMs });
    } catch (e) {
      return json({ ok: false, error: 'server' }, 500);
    }
  },
};
