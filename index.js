/* ============================================================================
   trickyssc-pay — the payment server.

   Three jobs, and one rule behind all of them: THE BROWSER IS NEVER TRUSTED.
   The price comes from Firestore here, not from the page. The signature is
   checked here with a secret the browser never sees. Entitlements are written
   here with a service account, and the security rules forbid any browser from
   writing them.

     POST /order    start a purchase  -> returns a Razorpay order id
     POST /verify   buyer finished    -> checks signature, unlocks the course
     POST /webhook  Razorpay tells us -> same unlock, authoritative
     GET  /health   is it alive

   WHY BOTH /verify AND /webhook: /verify runs in the buyer's browser after
   payment, so it never runs if they close the tab or lose signal at the wrong
   moment — which happens more often than you would think on mobile. The
   webhook comes from Razorpay's servers and always arrives. Both grant the
   same entitlement and both are idempotent, so whichever lands first wins and
   the second is a no-op.

   SECRETS (set with `wrangler secret put NAME`, never in this file):
     RAZORPAY_KEY_ID       rzp_test_… while testing, rzp_live_… later
     RAZORPAY_KEY_SECRET   from the same Razorpay dashboard page
     RAZORPAY_WEBHOOK_SECRET   whatever you type when creating the webhook
     FIREBASE_SA_JSON      the whole service-account JSON, pasted as one line
============================================================================ */

const PROJECT = 'trickyssc-17bb3';
const WEB_API_KEY = 'AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA';   // public web key
const FS = `https://firestore.googleapis.com/v1/projects/${PROJECT}/databases/(default)/documents`;

const ALLOWED_ORIGINS = [
  'https://trickyssc.com',
  'https://www.trickyssc.com',
  'http://localhost:5500',       // handy while testing locally
  'http://127.0.0.1:5500'
];

// ---------------------------------------------------------------- utilities

function cors(origin) {
  const ok = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    'Access-Control-Allow-Origin': ok,
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400'
  };
}

function json(data, status, origin) {
  return new Response(JSON.stringify(data), {
    status: status || 200,
    headers: { 'Content-Type': 'application/json', ...cors(origin) }
  });
}

const enc = new TextEncoder();

async function hmacHex(secret, message) {
  const key = await crypto.subtle.importKey(
    'raw', enc.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, enc.encode(message));
  return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, '0')).join('');
}

/** Constant-time compare, so a wrong signature can't be guessed byte by byte. */
function safeEqual(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

// ------------------------------------------------------- Firebase ID tokens

/** Confirm the caller really is who they claim. Returns { uid, email } or null.
    Uses Google's own lookup endpoint rather than verifying the JWT by hand —
    fewer moving parts, and it also catches tokens from deleted accounts. */
async function verifyIdToken(idToken) {
  if (!idToken || typeof idToken !== 'string') return null;
  const r = await fetch(
    `https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=${WEB_API_KEY}`,
    { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ idToken }) });
  if (!r.ok) return null;
  const d = await r.json();
  const u = d.users && d.users[0];
  if (!u || !u.localId) return null;
  return { uid: u.localId, email: u.email || '' };
}

// ----------------------------------------------- Firestore (service account)

let _tokenCache = { token: null, exp: 0 };

function b64url(buf) {
  return btoa(String.fromCharCode(...new Uint8Array(buf)))
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function pemToBinary(pem) {
  const body = pem.replace(/-----[A-Z ]+-----/g, '').replace(/\s+/g, '');
  const raw = atob(body);
  const out = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; i++) out[i] = raw.charCodeAt(i);
  return out.buffer;
}

/** Google OAuth access token for the service account. Cached until it expires. */
async function accessToken(env) {
  const now = Math.floor(Date.now() / 1000);
  if (_tokenCache.token && _tokenCache.exp - 60 > now) return _tokenCache.token;

  const sa = JSON.parse(env.FIREBASE_SA_JSON);
  const header = b64url(enc.encode(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
  const claim = b64url(enc.encode(JSON.stringify({
    iss: sa.client_email,
    scope: 'https://www.googleapis.com/auth/datastore',
    aud: 'https://oauth2.googleapis.com/token',
    iat: now, exp: now + 3600
  })));
  const key = await crypto.subtle.importKey(
    'pkcs8', pemToBinary(sa.private_key),
    { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['sign']);
  const sig = b64url(await crypto.subtle.sign(
    'RSASSA-PKCS1-v1_5', key, enc.encode(`${header}.${claim}`)));

  const r = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
      assertion: `${header}.${claim}.${sig}`
    })
  });
  if (!r.ok) throw new Error('service account auth failed: ' + await r.text());
  const d = await r.json();
  _tokenCache = { token: d.access_token, exp: now + (d.expires_in || 3600) };
  return d.access_token;
}

/* ---- Firestore typed values <-> plain JS ---- */
function toFs(v) {
  if (v === null || v === undefined) return { nullValue: null };
  if (typeof v === 'string') return { stringValue: v };
  if (typeof v === 'boolean') return { booleanValue: v };
  if (typeof v === 'number')
    return Number.isInteger(v) ? { integerValue: String(v) } : { doubleValue: v };
  if (v instanceof Date) return { timestampValue: v.toISOString() };
  if (Array.isArray(v)) return { arrayValue: { values: v.map(toFs) } };
  return { mapValue: { fields: toFsFields(v) } };
}
function toFsFields(o) {
  const f = {};
  for (const k of Object.keys(o)) f[k] = toFs(o[k]);
  return f;
}
function fromFs(v) {
  if (!v) return null;
  if ('stringValue' in v) return v.stringValue;
  if ('integerValue' in v) return parseInt(v.integerValue, 10);
  if ('doubleValue' in v) return Number(v.doubleValue);
  if ('booleanValue' in v) return v.booleanValue;
  if ('timestampValue' in v) return v.timestampValue;
  if ('nullValue' in v) return null;
  if ('arrayValue' in v) return (v.arrayValue.values || []).map(fromFs);
  if ('mapValue' in v) return fromFsFields(v.mapValue.fields || {});
  return null;
}
function fromFsFields(f) {
  const o = {};
  for (const k of Object.keys(f)) o[k] = fromFs(f[k]);
  return o;
}

/** Read a document. Public docs need no token; pass one for protected paths. */
async function fsGet(path, token) {
  const url = token ? `${FS}/${path}` : `${FS}/${path}?key=${WEB_API_KEY}`;
  const r = await fetch(url, token ? { headers: { Authorization: 'Bearer ' + token } } : {});
  if (r.status === 404) return null;
  if (!r.ok) throw new Error(`firestore read ${path}: ${r.status}`);
  const d = await r.json();
  return d.fields ? fromFsFields(d.fields) : {};
}

/** Write a whole document (create or replace). */
async function fsSet(path, obj, token) {
  const r = await fetch(`${FS}/${path}`, {
    method: 'PATCH',
    headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' },
    body: JSON.stringify({ fields: toFsFields(obj) })
  });
  if (!r.ok) throw new Error(`firestore write ${path}: ${r.status} ${await r.text()}`);
  return true;
}

// ------------------------------------------------------------------ pricing

/** The catalog, straight from Firestore. This is what decides the amount —
    whatever the browser claims the price is gets ignored. */
async function loadProduct(courseId) {
  const cat = await fsGet('config/pricing');
  if (!cat || !Array.isArray(cat.products) || !cat.products.length) {
    throw new Error('config/pricing is missing or empty — publish it in admin-pricing.html');
  }
  const p = cat.products.find(x => x.id === courseId);
  if (!p) throw new Error('unknown course: ' + courseId);
  if (p.live === false) throw new Error('this course is not on sale');
  const price = Number(p.price);
  if (!(price > 0)) throw new Error('course has no valid price');
  return { product: p, price, version: cat.version || 0 };
}

// ------------------------------------------------------------- entitlements

/** Grant every key a product includes. Read-modify-write so a second course
    purchase doesn't wipe the first, and re-running is harmless. */
async function grant(uid, product, orderId, source, token) {
  const path = `entitlements/${uid}`;
  const cur = (await fsGet(path, token)) || {};
  const modules = cur.modules || {};
  const days = Number(product.durationDays) || 365;

  for (const key of (product.grants || [])) {
    const existing = modules[key];
    // Extend from an unexpired grant rather than overwriting it, so buying a
    // combo that overlaps something already owned never shortens access.
    let from = Date.now();
    if (existing && existing.active && existing.expiresAt) {
      const t = Date.parse(existing.expiresAt);
      if (isFinite(t) && t > from) from = t;
    }
    modules[key] = {
      active: true,
      expiresAt: new Date(from + days * 86400000).toISOString(),
      grantedAt: new Date().toISOString(),
      orderId: orderId || '',
      productId: product.id,
      source: source
    };
  }

  await fsSet(path, {
    ...cur, uid, modules,
    updatedAt: new Date().toISOString()
  }, token);
  return Object.keys(modules);
}

// -------------------------------------------------------------- POST /order

async function handleOrder(req, env, origin) {
  const body = await req.json().catch(() => ({}));
  const { idToken, courseId, name, mobile, place } = body;

  const user = await verifyIdToken(idToken);
  if (!user) return json({ error: 'Please sign in again.' }, 401, origin);

  if (!/^[6-9]\d{9}$/.test(String(mobile || '')))
    return json({ error: 'A valid 10-digit mobile number is required.' }, 400, origin);
  if (!String(name || '').trim() || !String(place || '').trim())
    return json({ error: 'Name and place are required.' }, 400, origin);

  let priced;
  try { priced = await loadProduct(courseId); }
  catch (e) { return json({ error: e.message }, 400, origin); }

  const amountPaise = Math.round(priced.price * 100);
  const auth = 'Basic ' + btoa(`${env.RAZORPAY_KEY_ID}:${env.RAZORPAY_KEY_SECRET}`);

  const r = await fetch('https://api.razorpay.com/v1/orders', {
    method: 'POST',
    headers: { Authorization: auth, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      amount: amountPaise,
      currency: 'INR',
      receipt: `${courseId}-${Date.now()}`.slice(0, 40),
      notes: { uid: user.uid, courseId, name, mobile, place }
    })
  });
  if (!r.ok) {
    const t = await r.text();
    console.log('razorpay order failed', t);
    return json({ error: 'Could not start the payment. Please try again.' }, 502, origin);
  }
  const order = await r.json();

  const token = await accessToken(env);
  await fsSet(`payments/${order.id}`, {
    orderId: order.id,
    uid: user.uid,
    email: user.email,
    name: String(name).trim(),
    mobile: String(mobile),
    place: String(place).trim(),
    courseId,
    productLabel: priced.product.label || courseId,
    amount: priced.price,
    currency: 'INR',
    status: 'created',
    catalogVersion: priced.version,
    mode: String(env.RAZORPAY_KEY_ID).startsWith('rzp_test') ? 'test' : 'live',
    createdAt: new Date().toISOString()
  }, token);

  return json({
    orderId: order.id,
    amount: amountPaise,
    currency: 'INR',
    keyId: env.RAZORPAY_KEY_ID,
    productLabel: priced.product.label || courseId,
    price: priced.price
  }, 200, origin);
}

// ------------------------------------------------------------- POST /verify

async function handleVerify(req, env, origin) {
  const body = await req.json().catch(() => ({}));
  const { idToken, razorpay_order_id, razorpay_payment_id, razorpay_signature } = body;

  const user = await verifyIdToken(idToken);
  if (!user) return json({ error: 'Please sign in again.' }, 401, origin);

  const expected = await hmacHex(env.RAZORPAY_KEY_SECRET,
    `${razorpay_order_id}|${razorpay_payment_id}`);
  if (!safeEqual(expected, String(razorpay_signature || ''))) {
    console.log('signature mismatch', razorpay_order_id);
    return json({ error: 'Payment could not be verified.' }, 400, origin);
  }

  const token = await accessToken(env);
  const pay = await fsGet(`payments/${razorpay_order_id}`, token);
  if (!pay) return json({ error: 'Unknown order.' }, 404, origin);
  // the order was created for this account; nobody else can redeem it
  if (pay.uid !== user.uid) return json({ error: 'Order does not belong to you.' }, 403, origin);

  const priced = await loadProduct(pay.courseId);
  const keys = await grant(user.uid, priced.product, razorpay_order_id, 'razorpay', token);

  await fsSet(`payments/${razorpay_order_id}`, {
    ...pay, status: 'paid', paymentId: razorpay_payment_id,
    paidAt: pay.paidAt || new Date().toISOString(), grantedKeys: keys
  }, token);

  return json({ ok: true, unlocked: keys, product: priced.product.label }, 200, origin);
}

// ------------------------------------------------------------ POST /webhook

async function handleWebhook(req, env) {
  const raw = await req.text();
  const sig = req.headers.get('x-razorpay-signature') || '';
  const expected = await hmacHex(env.RAZORPAY_WEBHOOK_SECRET, raw);
  if (!safeEqual(expected, sig)) return new Response('bad signature', { status: 400 });

  let evt;
  try { evt = JSON.parse(raw); } catch (e) { return new Response('bad json', { status: 400 }); }

  const kind = evt.event || '';
  if (kind !== 'payment.captured' && kind !== 'order.paid') {
    return new Response('ignored', { status: 200 });
  }

  const payment = evt.payload?.payment?.entity || {};
  const orderId = payment.order_id;
  if (!orderId) return new Response('no order id', { status: 200 });

  const token = await accessToken(env);
  const pay = await fsGet(`payments/${orderId}`, token);
  if (!pay) return new Response('unknown order', { status: 200 });
  if (pay.status === 'paid') return new Response('already granted', { status: 200 });

  const priced = await loadProduct(pay.courseId);
  const keys = await grant(pay.uid, priced.product, orderId, 'razorpay-webhook', token);
  await fsSet(`payments/${orderId}`, {
    ...pay, status: 'paid', paymentId: payment.id || '',
    paidAt: new Date().toISOString(), grantedKeys: keys
  }, token);

  return new Response('ok', { status: 200 });
}

// -------------------------------------------------------------------- entry

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const origin = req.headers.get('Origin') || '';

    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors(origin) });

    try {
      if (url.pathname === '/health') {
        return json({
          ok: true,
          mode: String(env.RAZORPAY_KEY_ID || '').startsWith('rzp_test') ? 'test' : 'live',
          time: new Date().toISOString()
        }, 200, origin);
      }
      if (url.pathname === '/order'   && req.method === 'POST') return handleOrder(req, env, origin);
      if (url.pathname === '/verify'  && req.method === 'POST') return handleVerify(req, env, origin);
      if (url.pathname === '/webhook' && req.method === 'POST') return handleWebhook(req, env);
      return json({ error: 'not found' }, 404, origin);
    } catch (e) {
      console.log('unhandled', e.stack || e.message);
      return json({ error: 'Something went wrong. Please try again.' }, 500, origin);
    }
  }
};
