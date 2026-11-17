/* ============================================================================
   trickyssc-mail — sends emails from contact@trickyssc.com for admin-premium.html
   (TSSC-MAILSEND-V2, 2026-11-17)

   The Email button on the admin page opens a compose window; Send posts here
   and this Worker hands the mail to Resend (resend.com), which delivers it as
   contact@trickyssc.com. Only admins can use it — the caller's Firebase
   sign-in is checked on every request.

   WHY NOT THE HOSTINGER MAILBOX DIRECTLY: smtp.hostinger.com sits on
   Cloudflare addresses, and a Worker is not allowed to open a socket to those,
   so the mailbox login can never work from here. Replies still arrive in the
   Hostinger inbox, and a copy of every mail sent is delivered there too.

     POST /send     { idToken, to, subject, text }  -> { ok: true }
     GET  /health   is it alive, is the key set

   SECRET (Settings -> Variables and Secrets, type Secret):
     RESEND_API_KEY   the API key from resend.com (trickyssc.com must be a
                      verified domain there)
   Optional plain-text variables (defaults shown):
     FROM_EMAIL  contact@trickyssc.com
     FROM_NAME   Team TrickySSC
     SAVE_COPY   yes
============================================================================ */

const WEB_API_KEY = 'AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA';   // public web key
const ADMINS = ['nirala01@gmail.com', 'ashish@trickyssc.com'];
const isAdmin = e => !!e && (ADMINS.includes(e) || /@trickyssc\.com$/i.test(e));

const ALLOWED_ORIGINS = [
  'https://trickyssc.com',
  'https://www.trickyssc.com',
  'http://localhost:5500',
  'http://127.0.0.1:5500'
];

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

const oneLine = s => String(s || '').replace(/[\r\n]+/g, ' ').trim();
const EMAIL_RE = /^[^\s@<>()",;:]+@[^\s@<>()",;:]+\.[a-z]{2,}$/i;

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

async function handleSend(req, env, origin) {
  let body;
  try { body = await req.json(); } catch (e) { return json({ error: 'Bad request' }, 400, origin); }

  const who = await verifyIdToken(body.idToken);
  if (!who || !isAdmin(who.email)) return json({ error: 'Not allowed' }, 403, origin);
  if (!env.RESEND_API_KEY) return json({ error: 'RESEND_API_KEY secret is not set on the trickyssc-mail Worker' }, 500, origin);

  const to = oneLine(body.to).toLowerCase();
  const subject = oneLine(body.subject).slice(0, 200);
  const text = String(body.text || '').slice(0, 20000);
  if (!EMAIL_RE.test(to)) return json({ error: 'That email address does not look right' }, 400, origin);
  if (!subject) return json({ error: 'Subject is empty' }, 400, origin);
  if (!text.trim()) return json({ error: 'Message is empty' }, 400, origin);

  const from = env.FROM_EMAIL || 'contact@trickyssc.com';
  const name = oneLine(env.FROM_NAME || 'Team TrickySSC').replace(/[<>"]/g, '');
  const saveCopy = String(env.SAVE_COPY || 'yes').toLowerCase() !== 'no';
  const mail = { from: `${name} <${from}>`, to: [to], reply_to: from, subject, text };
  if (saveCopy && to !== from.toLowerCase()) mail.bcc = [from];

  let res, data;
  try {
    res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + env.RESEND_API_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify(mail)
    });
    data = await res.json().catch(() => ({}));
  } catch (err) {
    return json({ error: 'Could not reach the email service: ' + String(err && err.message || err) }, 502, origin);
  }
  if (!res.ok) {
    const why = (data && (data.message || data.error || data.name)) || ('HTTP ' + res.status);
    const hint = res.status === 401 ? ' — check the RESEND_API_KEY secret'
               : res.status === 403 ? ' — trickyssc.com is probably not verified in Resend yet'
               : res.status === 429 ? ' — daily or monthly sending limit reached' : '';
    return json({ error: 'Email service said: ' + String(typeof why === 'string' ? why : JSON.stringify(why)).slice(0, 300) + hint }, 502, origin);
  }
  return json({ ok: true, id: data && data.id }, 200, origin);
}

export default {
  async fetch(req, env) {
    const origin = req.headers.get('Origin') || '';
    const url = new URL(req.url);
    if (req.method === 'OPTIONS') return new Response(null, { headers: cors(origin) });
    if (url.pathname === '/health') return json({ ok: true, via: 'resend', from: env.FROM_EMAIL || 'contact@trickyssc.com', ready: !!env.RESEND_API_KEY }, 200, origin);
    if (url.pathname === '/send' && req.method === 'POST') return handleSend(req, env, origin);
    return json({ error: 'Not found' }, 404, origin);
  }
};
