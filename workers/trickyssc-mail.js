/* ============================================================================
   trickyssc-mail — sends follow-up emails from contact@trickyssc.com
   (TSSC-MAILSEND-V1, 2026-11-17)

   Used by admin-premium.html: the Email button opens a compose window with
   the address, subject and message filled in; Send posts here and this Worker
   delivers it through Hostinger's mail server. Only admins can use it — the
   caller's Firebase sign-in is checked on every request.

     POST /send     { idToken, to, subject, text }  -> { ok: true }
     GET  /health   is it alive

   SETUP (Cloudflare dashboard -> Workers & Pages -> Create -> Worker):
     name: trickyssc-mail   (address becomes trickyssc-mail.nirala01.workers.dev)
     paste this whole file as the Worker code, Deploy.
     Settings -> Variables and Secrets -> add a SECRET:
       SMTP_PASS   the password of the contact@trickyssc.com mailbox
     Optional plain-text variables (defaults shown):
       SMTP_USER   contact@trickyssc.com
       SMTP_HOST   smtp.hostinger.com
       FROM_NAME   Ashish - TrickySSC
       SAVE_COPY   yes   (a copy of every sent mail lands in your own inbox,
                          because mail sent this way is not put in "Sent")
============================================================================ */

import { connect } from 'cloudflare:sockets';

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

const enc = new TextEncoder();
const dec = new TextDecoder();

/* base64 of UTF-8 text (btoa alone breaks on Hindi / ₹) */
function b64(str) {
  const bytes = enc.encode(String(str));
  let bin = '';
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(bin);
}
const wrap76 = s => s.replace(/.{1,76}/g, '$&\r\n');
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

/* ------------------------------------------------------------- SMTP (465) */
async function smtpSend(env, { from, fromName, to, bcc, subject, text }) {
  const host = env.SMTP_HOST || 'smtp.hostinger.com';
  const user = env.SMTP_USER || 'contact@trickyssc.com';
  const sock = connect({ hostname: host, port: 465 }, { secureTransport: 'on' });
  const w = sock.writable.getWriter();
  const r = sock.readable.getReader();
  let buf = '';

  async function reply() {
    for (;;) {
      const lines = buf.split('\r\n');
      for (let i = 0; i < lines.length - 1; i++) {
        if (/^\d{3} /.test(lines[i])) {
          buf = lines.slice(i + 1).join('\r\n');
          return { code: +lines[i].slice(0, 3), text: lines.slice(0, i + 1).join(' | ') };
        }
      }
      const { value, done } = await r.read();
      if (done) throw new Error('Mail server closed the connection');
      buf += dec.decode(value, { stream: true });
    }
  }
  async function cmd(line, expect, hide) {
    if (line != null) await w.write(enc.encode(line + '\r\n'));
    const res = await reply();
    if (!expect.includes(res.code)) {
      throw new Error(hide
        ? 'Mailbox login refused (' + res.code + ') — check the SMTP_PASS secret is the contact@trickyssc.com password'
        : 'Mail server said: ' + res.text.slice(0, 200));
    }
    return res;
  }

  try {
    await cmd(null, [220]);
    await cmd('EHLO trickyssc.com', [250]);
    await cmd('AUTH LOGIN', [334]);
    await cmd(b64(user), [334]);
    await cmd(b64(env.SMTP_PASS || ''), [235], true);
    await cmd(`MAIL FROM:<${from}>`, [250]);
    await cmd(`RCPT TO:<${to}>`, [250, 251]);
    if (bcc) await cmd(`RCPT TO:<${bcc}>`, [250, 251]);
    await cmd('DATA', [354]);

    const msg = [
      `From: =?UTF-8?B?${b64(fromName)}?= <${from}>`,
      `To: <${to}>`,
      `Reply-To: <${from}>`,
      `Subject: =?UTF-8?B?${b64(subject)}?=`,
      `Date: ${new Date().toUTCString().replace('GMT', '+0000')}`,
      `Message-ID: <${crypto.randomUUID()}@trickyssc.com>`,
      'MIME-Version: 1.0',
      'Content-Type: text/plain; charset=UTF-8',
      'Content-Transfer-Encoding: base64',
      '',
      wrap76(b64(text.replace(/\r?\n/g, '\r\n')))
    ].join('\r\n');
    await w.write(enc.encode(msg + '\r\n.\r\n'));
    await cmd(null, [250]);
    try { await cmd('QUIT', [221]); } catch (e) { /* already delivered */ }
  } finally {
    try { await sock.close(); } catch (e) {}
  }
}

async function handleSend(req, env, origin) {
  let body;
  try { body = await req.json(); } catch (e) { return json({ error: 'Bad request' }, 400, origin); }

  const who = await verifyIdToken(body.idToken);
  if (!who || !isAdmin(who.email)) return json({ error: 'Not allowed' }, 403, origin);
  if (!env.SMTP_PASS) return json({ error: 'SMTP_PASS secret is not set on the trickyssc-mail Worker' }, 500, origin);

  const to = oneLine(body.to).toLowerCase();
  const subject = oneLine(body.subject).slice(0, 200);
  const text = String(body.text || '').slice(0, 20000);
  if (!EMAIL_RE.test(to)) return json({ error: 'That email address does not look right' }, 400, origin);
  if (!subject) return json({ error: 'Subject is empty' }, 400, origin);
  if (!text.trim()) return json({ error: 'Message is empty' }, 400, origin);

  const from = env.SMTP_USER || 'contact@trickyssc.com';
  const saveCopy = String(env.SAVE_COPY || 'yes').toLowerCase() !== 'no';
  try {
    await smtpSend(env, {
      from, fromName: env.FROM_NAME || 'Ashish - TrickySSC',
      to, bcc: saveCopy && to !== from.toLowerCase() ? from : '',
      subject, text
    });
    return json({ ok: true }, 200, origin);
  } catch (err) {
    return json({ error: String(err && err.message || err) }, 502, origin);
  }
}

export default {
  async fetch(req, env) {
    const origin = req.headers.get('Origin') || '';
    const url = new URL(req.url);
    if (req.method === 'OPTIONS') return new Response(null, { headers: cors(origin) });
    if (url.pathname === '/health') return json({ ok: true, mailbox: env.SMTP_USER || 'contact@trickyssc.com', ready: !!env.SMTP_PASS }, 200, origin);
    if (url.pathname === '/send' && req.method === 'POST') return handleSend(req, env, origin);
    return json({ error: 'Not found' }, 404, origin);
  }
};
