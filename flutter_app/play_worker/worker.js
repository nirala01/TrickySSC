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
// Built-in courses; catalog.json (below) adds the ones released later.
const PRODUCTS = {
  pass_ssc_cgl: { key: 'ssc-cgl-mocks', label: 'SSC CGL Mock Test Series' },
  pass_ssc_chsl: { key: 'ssc-chsl-mocks', label: 'SSC CHSL Mock Test Series' },
  pass_ssc_mts: { key: 'ssc-mts-mocks', label: 'SSC MTS Mock Test Series' },
  pass_ssc_gd: { key: 'ssc-gd-mocks', label: 'SSC GD Constable Mock Test Series' },
  pass_rrb_ntpc: { key: 'rrb-ntpc-mocks', label: 'RRB NTPC Mock Test Series' },
  pass_rrb_sm: { key: 'rrb-sm-mocks', label: 'RRB Station Master Mock Test Series' },
  pass_all_mocks: { key: 'all-mocks', label: 'All Mock Test Series' },
};
// Combos: Play product id combo_<exam>_<exam>[...] in this order, e.g. combo_ssc_cgl is not used; combo_cgl_chsl = CGL + CHSL.
const SHORT = { cgl: ['ssc-cgl-mocks', 'SSC CGL'], chsl: ['ssc-chsl-mocks', 'SSC CHSL'], mts: ['ssc-mts-mocks', 'SSC MTS'], gd: ['ssc-gd-mocks', 'SSC GD'], ntpc: ['rrb-ntpc-mocks', 'RRB NTPC'], sm: ['rrb-sm-mocks', 'RRB Station Master'] };
// Upgrade to Full Access for students who already paid (plan doc): two fixed Play products.
const UPGRADES = { upgrade_full_49: 49, upgrade_full_20: 20 };
// Keys the app never grants (Dashboard Pro is retired; every gate also accepts ssc-cgl-mocks).
const DROP = ['ssc-cgl-dashboard'];
function productOf(id) {
  if (UPGRADES[id]) return { keys: [], key: 'upgrade-full', label: 'Upgrade to Full Access (All Mocks Pass)', upgrade: true, price: UPGRADES[id] };
  const one = PRODUCTS[id];
  if (one) return { keys: [one.key], key: one.key, label: one.label };
  const m = /^combo_([a-z_]+)$/.exec(String(id || ''));
  if (!m) return null;
  const parts = m[1].split('_');
  if (parts.length < 2 || parts.length >= Object.keys(SHORT).length || new Set(parts).size !== parts.length || parts.some((x) => !SHORT[x])) return null;
  const keys = parts.map((x) => SHORT[x][0]);
  return { keys, key: keys.join('+'), label: parts.map((x) => SHORT[x][1]).join(' + ') + ' Mock Tests (Combo)', combo: true };
}
// The matching product in admin-pricing (config/pricing): p-<key> for a single pass or the All Mocks Pass,
// for a combo the live product whose mock keys are exactly these. Its grants, label and id are used,
// so the app unlocks exactly what the website does (e.g. the CGL pass also opens ssc-cgl-dashboard).
let MOCK_KEYS = ['all-mocks', ...Object.values(SHORT).map((v) => v[0])];
// The course list the app also reads (flutter_app/catalog.json in the repo). A course added there can be
// bought in the app without changing this Worker. Read at most once every 5 minutes; if it cannot be read,
// the built-in courses above are used.
const CATALOG_URLS = ['https://trickyssc.com/flutter_app/catalog.json', 'https://raw.githubusercontent.com/nirala01/TrickySSC/main/flutter_app/catalog.json'];
let catalogAt = 0;
async function loadCatalog() {
  if (Date.now() - catalogAt < 300000) return;
  for (const u of CATALOG_URLS) {
    try {
      const r = await fetch(u + '?t=' + Math.floor(Date.now() / 300000));
      if (!r.ok) continue;
      const j = await r.json();
      if (!j || !Array.isArray(j.exams)) continue;
      for (const e of j.exams) {
        if (!e || e.live === false || !/^[a-z0-9]+$/.test(e.k || '') || !/^[a-z0-9-]+$/.test(e.pass || '') || e.pass === 'all-mocks') continue;
        const play = e.play || 'pass_' + e.pass.replace('-mocks', '').replace(/-/g, '_');
        if (UPGRADES[play] || play === 'pass_all_mocks' || !/^[a-z0-9_]+$/.test(play)) continue;
        PRODUCTS[play] = { key: e.pass, label: e.passName || (e.name || e.pass) + ' Mock Test Series' };
        SHORT[e.k] = [e.pass, e.name || e.pass];
      }
      MOCK_KEYS = ['all-mocks', ...Object.values(SHORT).map((v) => v[0])];
      catalogAt = Date.now();
      return;
    } catch (e) {}
  }
}
async function websiteProduct(pid, tok, product) {
  try {
    const d = await fsGet(pid, tok, 'config/pricing');
    const list = ((((d || {}).fields || {}).products || {}).arrayValue || {}).values || [];
    for (const v of list) {
      const f = (v.mapValue || {}).fields || {};
      const id = (f.id || {}).stringValue || '';
      if (id.startsWith('p-upgrade-')) continue;
      const g = (((f.grants || {}).arrayValue || {}).values || []).map((x) => x.stringValue).filter(Boolean);
      const mock = g.filter((k) => MOCK_KEYS.includes(k));
      const hit = product.combo
        ? mock.length === product.keys.length && product.keys.every((k) => mock.includes(k))
        : id === 'p-' + product.key;
      if (hit) return { id, label: (f.label || {}).stringValue || '', grants: g };
    }
  } catch (e) {}
  return null;
}

// CORS: trickyssc.com calls /upgrade-free (the "Claim now" free Full Access button on the mock pages).
const CORS = { 'access-control-allow-origin': '*', 'access-control-allow-methods': 'POST, GET, OPTIONS', 'access-control-allow-headers': 'content-type', 'access-control-max-age': '86400' };
const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'content-type': 'application/json', ...CORS } });
const b64u = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const b64uText = (s) => b64u(new TextEncoder().encode(s));
const fromB64u = (s) => Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/')), (c) => c.charCodeAt(0));

// New expiry for one course: a year from now, or a year on top of a pass still running.
// [granted]: the purchase was already recorded, so the year is not added twice when the grant is retried.
function expiryFor(ent, key, granted = false) {
  const cur = ((((((ent || {}).fields || {}).modules || {}).mapValue || {}).fields || {})[key] || {}).mapValue;
  const curExp = cur && (cur.fields.active || {}).booleanValue === true ? (expMsOf(cur.fields.expiresAt) || 0) : 0;
  if (granted && cur && (cur.fields.source || {}).stringValue === 'google-play' && curExp > Date.now() + (VALID_DAYS - 2) * 86400000) return curExp;
  return Math.max(Date.now(), curExp > Date.now() ? curExp : 0) + VALID_DAYS * 86400000;
}

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

// ---- Upgrade to Full Access: price from the student's paid orders (plan doc)
//   paid ₹49 -> pays ₹49 · paid ₹70-97 (combo, or pass + ₹29 add-on) -> ₹20 · paid ₹98+ -> ₹20 (no free upgrade since 2026-11-18) · full access -> nothing
// expiresAt as milliseconds. The website Worker (index.js) saves it as an ISO text, this Worker as a timestamp;
// both are read. NaN when the pass has no expiry date. (2026-11-18)
const expMsOf = (f) => {
  const x = f || {};
  const v = x.timestampValue ?? x.stringValue ?? (x.integerValue != null ? Number(x.integerValue) : x.doubleValue);
  if (v == null || v === '') return NaN;
  return typeof v === 'number' ? v : Date.parse(v);
};
// A pass with active:true and no expiry date (opened by hand from admin premium) counts as owned, the same as
// in the app (data.dart _active): activeExp gives NO_EXPIRY for it. (2026-11-18)
const NO_EXPIRY = 8640000000000000;
const activeExp = (ent, key) => {
  const m = ((((((ent || {}).fields || {}).modules || {}).mapValue || {}).fields || {})[key] || {}).mapValue;
  if (!m || !m.fields || (m.fields.active || {}).booleanValue !== true) return 0;
  const e = expMsOf(m.fields.expiresAt);
  if (!isFinite(e)) return NO_EXPIRY;
  return e > Date.now() ? e : 0;
};
async function paidTotal(pid, tok, uid) {
  const r = await fetch(`${fsBase(pid)}:runQuery`, {
    method: 'POST', headers: { authorization: 'Bearer ' + tok, 'content-type': 'application/json' },
    body: JSON.stringify({ structuredQuery: { from: [{ collectionId: 'payments' }], where: { fieldFilter: { field: { fieldPath: 'uid' }, op: 'EQUAL', value: { stringValue: uid } } } } }),
  });
  if (r.status !== 200) return 0;
  let total = 0;
  for (const row of await r.json()) {
    const f = ((row || {}).document || {}).fields;
    if (!f || (f.status || {}).stringValue !== 'paid' || (f.mode || {}).stringValue === 'test') continue;
    const a = f.amount || {};
    const n = Number(a.integerValue ?? a.doubleValue ?? a.stringValue ?? 0);
    if (isFinite(n) && n > 0 && n < 100000) total += n;
  }
  return total;
}
async function upgradeKeys(pid, tok) {
  const w = await websiteProduct(pid, tok, { key: 'all-mocks', keys: ['all-mocks'] });
  const k = ((w && w.grants) || []).filter((x) => x !== 'all-mocks' && !DROP.includes(x));
  return k.length ? k : Object.values(SHORT).map((v) => v[0]);
}
async function quote(pid, tok, uid) {
  const ent = await fsGet(pid, tok, `entitlements/${uid}`);
  const f = (ent || {}).fields || {};
  const allAcc = (((f.allAccess || {}).mapValue || {}).fields || {});
  const fullFlag = (allAcc.active || {}).booleanValue === true && (!isFinite(expMsOf(allAcc.expiresAt)) || expMsOf(allAcc.expiresAt) > Date.now());
  const exams = Object.values(SHORT).map((v) => v[0]);
  const owned = {}; // pass -> expiry (ms), for the "stays valid till" line; passes without an expiry date are left out
  let have = 0;
  for (const k of exams) { const e = activeExp(ent, k); if (e) { have++; if (e !== NO_EXPIRY) owned[k] = e; } }
  const full = fullFlag || activeExp(ent, 'all-mocks') > 0 || have >= exams.length;
  const paid = have > 0;
  const total = paid ? await paidTotal(pid, tok, uid) : 0;
  const price = full || !paid ? null : total >= 70 ? 20 : 49; // 2026-11-18: no free upgrade any more
  return { ok: true, paid, full, total, price, product: price === 49 ? 'upgrade_full_49' : price === 20 ? 'upgrade_full_20' : null, owned };
}
// Validity rule: a course already running keeps its expiry; every newly opened course gets a year from today.
async function grantUpgrade(pid, tok, uid, orderId) {
  const ent = await fsGet(pid, tok, `entitlements/${uid}`);
  const keys = await upgradeKeys(pid, tok);
  const year = Date.now() + VALID_DAYS * 86400000;
  const fields = {}, mask = ['updatedAt'], added = [];
  for (const k of keys) {
    if (activeExp(ent, k)) continue;
    fields[k] = { mapValue: { fields: { active: { booleanValue: true }, expiresAt: ts(year), source: str('upgrade-full'), orderId: str(orderId) } } };
    mask.push('modules.`' + k + '`');
    added.push(k);
  }
  if (!added.length) return { st: 200, added, year };
  const st = await fsPatch(pid, tok, `entitlements/${uid}`, { modules: { mapValue: { fields } }, updatedAt: ts(Date.now()) }, mask);
  return { st, added, year };
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
    if (req.method === 'GET') return json({ ok: true, service: 'trickyssc-play' });
    if (req.method !== 'POST' || !['/verify', '/quote', '/upgrade-free'].includes(url.pathname)) return json({ ok: false, error: 'not-found' }, 404);
    try {
      if (!env.GOOGLE_SA_JSON) return json({ ok: false, error: 'not-configured' }, 500);
      const sa = JSON.parse(env.GOOGLE_SA_JSON);
      const pid = sa.project_id;
      const b = await req.json();
      await loadCatalog();
      if (url.pathname !== '/verify') {
        const who = await verifyIdToken(b.idToken, pid);
        if (!who) return json({ ok: false, error: 'sign-in' }, 401);
        const t = await accessToken(sa);
        const q = await quote(pid, t, who);
        if (url.pathname === '/quote') return json(q);
        // /upgrade-free: switched off 2026-11-18 (the free upgrade was dropped)
        if (q.full) return json({ ok: true, already: true });
        if (url.pathname === '/upgrade-free') return json({ ok: false, error: 'not-eligible' }, 409);
        const g = await grantUpgrade(pid, t, who, 'free_' + who);
        if (g.st !== 200) return json({ ok: false, error: 'grant-failed' }, 500);
        const uf = ((await fsGet(pid, t, `users/${who}`)) || {}).fields || {};
        const us = (k) => (uf[k] || {}).stringValue || '';
        await fsPatch(pid, t, `payments/free_upgrade_${who}`, {
          uid: str(who), status: str('paid'), gateway: str('free-upgrade'), productId: str('upgrade_full_free'), courseId: str('p-upgrade-all-free'),
          productLabel: str('Free upgrade to Full Access'), amount: { doubleValue: 0 }, mode: str('live'), platform: str(b.platform === 'web' ? 'web' : 'app'),
          name: str(us('name')), email: str(us('email')), mobile: str(us('phone') || us('mobile')),
          grantedKeys: { arrayValue: { values: g.added.map(str) } }, expiresAt: ts(g.year), paidAt: ts(Date.now()), createdAt: ts(Date.now()),
        }, ['uid', 'status', 'gateway', 'productId', 'courseId', 'productLabel', 'amount', 'mode', 'platform', 'name', 'email', 'mobile', 'grantedKeys', 'expiresAt', 'paidAt', 'createdAt']);
        return json({ ok: true, added: g.added });
      }
      const product = productOf(b.productId);
      const purchaseToken = String(b.purchaseToken || '');
      if (!product || purchaseToken.length < 20) return json({ ok: false, error: 'bad-request' }, 400);
      const uid = await verifyIdToken(b.idToken, pid);
      if (!uid) return json({ ok: false, error: 'sign-in' }, 401);

      // 1. is the purchase real and paid?
      const tok = await accessToken(sa);
      let web = null, keys;
      if (product.upgrade) {
        const q = await quote(pid, tok, uid);
        // not acknowledged -> Google refunds it automatically within 3 days
        if (q.full) return json({ ok: false, error: 'already-full' }, 409);
        if (!q.paid || q.price === null || product.price < q.price) return json({ ok: false, error: 'not-eligible', price: q.price }, 409);
        keys = await upgradeKeys(pid, tok);
      } else {
        web = await websiteProduct(pid, tok, product);
        keys = [...new Set([...product.keys, ...((web && web.grants) || [])])].filter((k) => !DROP.includes(k));
      }
      const api = `https://androidpublisher.googleapis.com/androidpublisher/v3/applications/${PACKAGE}/purchases/products/${b.productId}/tokens/${encodeURIComponent(purchaseToken)}`;
      const gr = await fetch(api, { headers: { authorization: 'Bearer ' + tok } });
      if (gr.status !== 200) {
        // shown in Cloudflare -> Worker -> Observability: why Google did not confirm the purchase (no secrets in it)
        console.log('play-check', b.productId, gr.status, (await gr.text().catch(() => '')).replace(/\s+/g, ' ').slice(0, 300));
        return json({ ok: false, error: 'not-found-at-google', status: gr.status }, 402);
      }
      const g = await gr.json();
      if (g.purchaseState === 2) return json({ ok: false, error: 'pending' }, 202);   // e.g. cash / slow UPI: Play tells the app again when it is paid
      if (g.purchaseState !== 0) { console.log('play-check', b.productId, 'state', g.purchaseState); return json({ ok: false, error: 'not-paid' }, 402); }
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
        expMs = 0;
        if (product.upgrade) expMs = Date.now() + VALID_DAYS * 86400000;
        else for (const k of keys) expMs = Math.max(expMs, expiryFor(ent, k));
        const st = await fsPatch(pid, tok, recPath, {
          uid: str(uid), productId: str(b.productId), key: str(product.key), orderId: str(g.orderId || ''), status: str('pending'),
          expiresAt: ts(expMs), createdAt: ts(Date.now()),
        }, ['uid', 'productId', 'key', 'orderId', 'status', 'expiresAt', 'createdAt'], '&currentDocument.exists=false');
        if (st !== 200) return json({ ok: false, error: 'busy' }, 409);
      }

      // 3. open the pass (each course of a combo: renewing early adds a year on top of its own expiry)
      const entNow = await fsGet(pid, tok, `entitlements/${uid}`);
      const fields = {}, mask = ['updatedAt'];
      for (const k of keys) {
        if (product.upgrade && activeExp(entNow, k) && !(((((((entNow || {}).fields || {}).modules || {}).mapValue || {}).fields || {})[k] || {}).mapValue || { fields: {} }).fields.orderId?.stringValue === (g.orderId || '')) continue;   // validity rule: a running course keeps its expiry
        const e = product.upgrade ? expMs : keys.length === 1 ? expMs : expiryFor(entNow, k, true);
        fields[k] = { mapValue: { fields: { active: { booleanValue: true }, expiresAt: ts(e), source: str('google-play'), orderId: str(g.orderId || '') } } };
        mask.push('modules.`' + k + '`');
      }
      const st = await fsPatch(pid, tok, `entitlements/${uid}`, { modules: { mapValue: { fields } }, updatedAt: ts(Date.now()) }, mask);
      if (st !== 200) return json({ ok: false, error: 'grant-failed' }, 500);

      // 4. order row for "My orders", mark done, consume (lets the student renew next year)
      const amount = Number(b.amount);
      // buyer details for admin-premium.html (the website's checkout writes them from the form)
      const uf = ((await fsGet(pid, tok, `users/${uid}`)) || {}).fields || {};
      const us = k => (uf[k] || {}).stringValue || '';
      await fsPatch(pid, tok, `payments/play_${hash}`, {
        name: str(us('name')), email: str(us('email')), mobile: str(us('phone') || us('mobile')), place: str(us('place') || us('city')),
        grantedKeys: { arrayValue: { values: keys.map(str) } }, expiresAt: ts(expMs),
        mode: str(g.purchaseType === 0 ? 'test' : 'live'), platform: str('app'),
        uid: str(uid), status: str('paid'), gateway: str('google-play'), productId: str(b.productId), courseId: str(web && web.id ? web.id : product.key), productLabel: str(web && web.label ? web.label : product.label),
        amount: isFinite(amount) && amount > 0 && amount < 100000 ? { doubleValue: amount } : str(''),
        paymentId: str(g.orderId || ''), orderId: str(g.orderId || ''), paidAt: ts(Number(g.purchaseTimeMillis) || Date.now()), createdAt: ts(Date.now()),
      }, ['uid', 'status', 'gateway', 'productId', 'courseId', 'productLabel', 'amount', 'paymentId', 'orderId', 'paidAt', 'createdAt',
          'name', 'email', 'mobile', 'place', 'grantedKeys', 'expiresAt', 'mode', 'platform']);
      await fsPatch(pid, tok, recPath, { status: str('granted') }, ['status']);
      await fetch(api + ':consume', { method: 'POST', headers: { authorization: 'Bearer ' + tok } }).catch(() => {});
      return json({ ok: true, key: product.key, expiresAt: expMs });
    } catch (e) {
      console.log('play-error', url.pathname, String((e && e.message) || e).slice(0, 200));
      return json({ ok: false, error: 'server' }, 500);
    }
  },
};
