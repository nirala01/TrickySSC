/* ============================================================================
   tssc-aic.js — SSC CGL Tier-2 ALL INDIA CHALLENGE MOCK            TSSC-AIC-V1
   ----------------------------------------------------------------------------
   One free challenge paper every Sunday. Everything on the site that belongs to
   the challenge reads its dates and rules from THIS file, and every state
   (register / registered / mock is live / submitted / results out / next round)
   is worked out from the clock. Nothing has to be switched on or published by
   hand.

   THE WEEKLY TIMELINE (all times IST), round N = Sunday number N from 29 Nov 2026
     Saturday 11:59 pm   registration for that Sunday closes
     Sunday   9:00 am    mock opens (registered students only, one attempt)
     Sunday   9:45 pm    last entry (the paper is 2 h 15 min)
     Sunday  12 midnight window closes
     Tuesday  9:00 am    result + All India rank + solutions open on their own,
                         and the paper becomes a free mock for everyone

   REGISTRATION is one time. A student who registers once is in every later
   round; a registration made after a Saturday midnight counts from the next
   Sunday.

   THE PAPER of round N is the mock uploaded as  ssc-cgl_aic_mockN_en / _hi
   (batch-uploader-mock.html, tier "aic"). Its mock_tests cards are saved as
   drafts on purpose, so no mock list or count on the site picks them up.

   WHERE THINGS ARE STORED (no new collections, no rules change)
     users/{uid}.aic = { reg:true, at:<server time>, src:'web' }   registration
     leaderboards/aic-registered/scores/{uid}                      same, for the public count
     leaderboards/ssc-cgl_aic_mockN/scores/{uid}                   LIVE attempts only = the All India rank
     attempts/{id}.aic = { round:N, live:true|false, resultAt:<ms> } set by mock-test-tier2.html

   TO CHANGE SOMETHING
     - result time, window, last entry:  the numbers in round() below
     - stop the series after a round:    CFG.lastRound = that round number
   ========================================================================== */

import { getApps, getApp, initializeApp }
  from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getFirestore, doc, getDoc, setDoc, serverTimestamp, collection, query, orderBy, limit,
         getDocs, getCountFromServer }
  from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";
import { getAuth, onAuthStateChanged }
  from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

const FB_CONFIG = {
  apiKey: "AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA",
  authDomain: "trickyssc-17bb3.firebaseapp.com",
  projectId: "trickyssc-17bb3",
  storageBucket: "trickyssc-17bb3.firebasestorage.app",
  messagingSenderId: "450627057220",
  appId: "1:450627057220:web:366267bf437d94f20c6e11"
};
const app  = getApps().length ? getApp() : initializeApp(FB_CONFIG);
const db   = getFirestore(app);
const auth = getAuth(app);

/* ───────────────────────── schedule ───────────────────────── */
const H = 3600000;
export const CFG = {
  first: Date.UTC(2026, 10, 29, 3, 30, 0),   // Sunday 29 Nov 2026, 9:00 am IST — Challenge Mock 1
  week: 7 * 24 * H,
  lastRound: 0,                              // 0 = every Sunday with no end; set to N to make round N the last
  page: '/ssc-cgl-tier-2-all-india-challenge-mock.html',
  mocks: '/ssc-cgl-tier-2-mock-test.html',
  regBoard: 'aic-registered',
  graceMs: 30 * 60000                        // a test started in the window may still be submitted this long after midnight
};
export function round(n) {
  n = Math.max(1, parseInt(n, 10) || 1);
  const start = CFG.first + (n - 1) * CFG.week;
  return {
    n,
    start,                                   // Sunday 9:00 am
    lastEntry: start + (12 * 60 + 45) * 60000, // Sunday 9:45 pm
    end: start + 15 * H,                     // Sunday midnight
    regClose: start - 9 * H,                 // Saturday midnight
    resultAt: start + 48 * H,                // Tuesday 9:00 am
    board: 'ssc-cgl_aic_mock' + n,
    mockId: lang => 'ssc-cgl_aic_mock' + n + '_' + (lang === 'hi' ? 'hi' : 'en')
  };
}
export const isAicId = id => /^ssc-cgl_aic_mock\d+/i.test(String(id || ''));
export function roundOfMock(id) { const m = String(id || '').match(/_aic_mock(\d+)/i); return m ? parseInt(m[1], 10) : 0; }
export const hasRound = n => n >= 1 && (!CFG.lastRound || n <= CFG.lastRound);
/* the round a visitor should be looking at: the first one whose Sunday is not over yet */
export function nextRound(t) {
  let n = Math.max(1, Math.floor((t - (CFG.first + 15 * H)) / CFG.week) + 2);
  while (n > 1 && t < round(n - 1).end) n--;
  return n;
}
export function testUrl(n, lang) {
  const l = lang === 'hi' ? 'hi' : 'en';
  return '/mock-test-tier2.html?exam=ssc-cgl&tier=tier2&series=' + n + '&lang=' + l + '&mockId=' + round(n).mockId(l);
}

/* ───────────────────────── clock ─────────────────────────
   The device clock is checked once per tab against the Date header of this
   site's own server; a phone whose date is wrong by more than a minute is
   corrected, so nobody opens the paper early or sees a result early by
   changing the date. If the check fails the device clock is used as it is. */
let _skew = 0, _skewP = null;
try { const s = parseInt(sessionStorage.getItem('tssc_aic_skew') || '', 10); if (isFinite(s)) _skew = s; } catch (e) {}
export const now = () => Date.now() + _skew;
export function syncClock() {
  if (_skewP) return _skewP;
  try { if (sessionStorage.getItem('tssc_aic_skew') !== null) return (_skewP = Promise.resolve(_skew)); } catch (e) {}
  _skewP = (async () => {
    try {
      const t0 = Date.now();
      const r = await Promise.race([
        fetch('/robots.txt?aic=' + t0, { method: 'HEAD', cache: 'no-store' }),
        new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 4000))
      ]);
      const t1 = Date.now();
      const d = Date.parse(r.headers.get('date') || '');
      const age = (parseInt(r.headers.get('age') || '0', 10) || 0) * 1000;
      if (isFinite(d)) { const sk = (d + age) - (t0 + t1) / 2; _skew = Math.abs(sk) > 60000 ? Math.round(sk) : 0; }
      try { sessionStorage.setItem('tssc_aic_skew', String(_skew)); } catch (e) {}
    } catch (e) { /* keep the device clock */ }
    return _skew;
  })();
  return _skewP;
}

/* ───────────────────────── small helpers ───────────────────────── */
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const IST = { timeZone: 'Asia/Kolkata' };
export function fmtDay(ms)  { return new Date(ms).toLocaleDateString('en-IN', Object.assign({ weekday: 'long', day: 'numeric', month: 'short' }, IST)); }
export function fmtDate(ms) { return new Date(ms).toLocaleDateString('en-IN', Object.assign({ day: 'numeric', month: 'short' }, IST)); }
export function fmtShort(ms){ return new Date(ms).toLocaleDateString('en-IN', Object.assign({ weekday: 'short', day: 'numeric', month: 'short' }, IST)); }
const lsGet = k => { try { return localStorage.getItem(k); } catch (e) { return null; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} };
/* short-lived cache per tab, so one page view does not repeat the same Firestore reads */
const ssGet = (k, ttl) => { try { const o = JSON.parse(sessionStorage.getItem(k) || 'null'); return (o && Date.now() - o.ts < ttl) ? o : null; } catch (e) { return null; } };
const ssSet = (k, v) => { try { sessionStorage.setItem(k, JSON.stringify({ ts: Date.now(), v })); } catch (e) {} };
const ssDel = k => { try { sessionStorage.removeItem(k); } catch (e) {} };
const MIN5 = 5 * 60000, MIN10 = 10 * 60000;
const tsMs = v => !v ? 0 : (v.toMillis ? v.toMillis() : (v.seconds ? v.seconds * 1000 : (Date.parse(v) || 0)));
function localUser() { try { const u = JSON.parse(lsGet('tssc_user') || 'null'); return (u && u.uid) ? u : null; } catch (e) { return null; } }
export function currentUid() { return (auth.currentUser && auth.currentUser.uid) || (localUser() || {}).uid || ''; }
const authReady = new Promise(res => { let done = false; const fin = () => { if (!done) { done = true; res(); } };
  try { onAuthStateChanged(auth, fin, fin); } catch (e) { fin(); } setTimeout(fin, 3500); });

/* ───────────────────────── registration ───────────────────────── */
const regKey = uid => 'tssc_aic_reg_' + uid;
/* → the time (ms) this student registered, or 0. fresh=true always asks the server. */
export async function regAt(uid, fresh) {
  if (!uid) return 0;
  const c = parseInt(lsGet(regKey(uid)) || '', 10);
  if (isFinite(c) && c > 0 && !fresh) return c;
  if (!fresh && ssGet('tssc_aic_noreg_' + uid, MIN5)) return 0;
  let at = 0, read = false;
  try {
    const s = await getDoc(doc(db, 'users', uid)); read = true;
    const a = s.exists() ? (s.data() || {}).aic : null;
    if (a && a.reg) at = tsMs(a.at) || now();
  } catch (e) {}
  if (!at) {
    try { const s = await getDoc(doc(db, 'leaderboards', CFG.regBoard, 'scores', uid)); read = true;
      if (s.exists()) at = tsMs((s.data() || {}).submittedAt) || now(); } catch (e) {}
  }
  if (at) { lsSet(regKey(uid), String(at)); ssDel('tssc_aic_noreg_' + uid); return at; }
  if (read) ssSet('tssc_aic_noreg_' + uid, 1);
  /* the server could not be reached: trust what this phone remembers */
  return (!read && isFinite(c) && c > 0) ? c : 0;
}
async function ensureLogin() {
  if (auth.currentUser) return auth.currentUser;
  await authReady;
  if (auth.currentUser) return auth.currentUser;
  if (!window.tsscLogin) { try { await import('/login-modal.js'); } catch (e) {} }
  for (let i = 0; i < 40 && !window.tsscLogin; i++) await new Promise(r => setTimeout(r, 100));
  if (!window.tsscLogin) { lsSet('loginReturnTo', location.origin + CFG.page + '?register=1'); location.href = '/login.html'; return null; }
  return await window.tsscLogin.require();
}
/* One click. Asks for login first when needed. → { ok, at, already } or { ok:false, reason } */
export async function register() {
  const u = await ensureLogin();
  if (!u || !u.uid) return { ok: false, reason: 'login' };
  const had = await regAt(u.uid, true);
  if (had) return { ok: true, at: had, already: true };
  let ok = false;
  try { await setDoc(doc(db, 'users', u.uid), { aic: { reg: true, at: serverTimestamp(), src: 'web' } }, { merge: true }); ok = true; }
  catch (e) { console.warn('[aic] register (profile):', e && e.message); }
  /* the same row on a board, so the page can show how many students are in (same write the leaderboards use) */
  try {
    const lb = await import('/leaderboard.js');
    await lb.recordScore({ uid: u.uid, displayName: u.displayName, paperId: CFG.regBoard, paperName: 'All India Challenge registration', marks: 0, maxMarks: 0 });
    if (!ok) { const s = await getDoc(doc(db, 'leaderboards', CFG.regBoard, 'scores', u.uid)); ok = s.exists(); }
  } catch (e) { console.warn('[aic] register (board):', e && e.message); }
  if (!ok) return { ok: false, reason: 'write' };
  const at = now();
  lsSet(regKey(u.uid), String(at)); ssDel('tssc_aic_noreg_' + u.uid); ssDel('tssc_aic_count');
  try { if (window.gtag) window.gtag('event', 'aic_register', { round: nextRound(at) }); } catch (e) {}
  return { ok: true, at };
}

/* ───────────────────────── a student's round ───────────────────────── */
const doneKey  = (n, uid) => 'tssc_aic_done_' + n + '_' + uid;
const startKey = (n, uid) => 'tssc_aic_start_' + n + '_' + uid;
export function markStarted(n, uid) { if (uid && !lsGet(startKey(n, uid))) lsSet(startKey(n, uid), String(now())); }
export function startedAt(n, uid) { const v = parseInt(lsGet(startKey(n, uid)) || '', 10); return isFinite(v) ? v : 0; }
export function markDone(n, uid, attemptId) { if (uid) lsSet(doneKey(n, uid), JSON.stringify({ id: attemptId || '', at: now() })); }
/* → { id } when this student has a LIVE attempt in round n, else null */
export async function participated(n, uid, fresh) {
  if (!uid) return null;
  try { const o = JSON.parse(lsGet(doneKey(n, uid)) || 'null'); if (o && !fresh) return o; } catch (e) {}
  if (!fresh && ssGet('tssc_aic_np_' + n + '_' + uid, MIN5)) return null;
  try {
    const s = await getDoc(doc(db, 'leaderboards', round(n).board, 'scores', uid));
    if (s.exists()) { let id = ''; try { id = (JSON.parse(lsGet(doneKey(n, uid)) || 'null') || {}).id || ''; } catch (e) {}
      const o = { id, at: tsMs((s.data() || {}).submittedAt) || 0 }; lsSet(doneKey(n, uid), JSON.stringify(o)); return o; }
    ssSet('tssc_aic_np_' + n + '_' + uid, 1);
  } catch (e) { try { return JSON.parse(lsGet(doneKey(n, uid)) || 'null'); } catch (_) {} }
  return null;
}
export function resultUrl(n, done) {
  return '/test-analysis.html?' + (done && done.id ? 'id=' + encodeURIComponent(done.id) : 'aic=' + n);
}

/* Is this language of round n uploaded? (the Hindi button is hidden when it is not) */
export async function hasLang(n, lang) {
  const k = 'tssc_aic_lang_' + n + '_' + lang; const c = ssGet(k, MIN10); if (c) return !!c.v;
  try { const s = await getDoc(doc(db, 'mock_tests', round(n).mockId(lang))); ssSet(k, s.exists() ? 1 : 0); return s.exists(); }
  catch (e) { return true; }
}

/* ───────────────────────── the gate (used by mock-test-tier2.html) ─────────────────────────
   → { ok:true, mode:'live'|'practice', round, r }  or  { ok:false, screen:{ icon, title, body, cta, href } } */
export async function gate(uid, mockId) {
  await syncClock();
  const n = roundOfMock(mockId), t = now();
  const back = { cta: 'Open the All India Challenge page', href: CFG.page };
  if (!hasRound(n)) return { ok: false, screen: Object.assign({ icon: '📭', title: 'This challenge mock is not available', body: 'Please open the All India Challenge page for the current schedule.' }, back) };
  const r = round(n), nx = round(n + 1);
  const resLine = 'Result, All India rank and solutions: <b>' + fmtDay(r.resultAt) + ', 9 am</b>.';
  if (t < r.start) {
    const reg = await regAt(uid);
    const inTime = reg && reg < r.regClose;
    return { ok: false, screen: Object.assign({ icon: '⏳', title: 'Challenge Mock ' + n + ' opens on ' + fmtDay(r.start) + ' at 9 am',
      body: inTime ? 'You are registered. Come back on Sunday between 9 am and 9:45 pm to take the paper.'
        : (t < r.regClose ? 'Register (free, one click) before Saturday midnight to take this paper in the live window.'
          : 'Registration for this Sunday is closed. ' + (reg ? 'You are in from Challenge Mock ' + (n + 1) + ' (' + fmtDay(nx.start) + ').' : 'Register now for Challenge Mock ' + (n + 1) + ' (' + fmtDay(nx.start) + ').')) }, back) };
  }
  const started = startedAt(n, uid);
  if (t < r.end || (started && t < r.end + CFG.graceMs)) {
    const done = await participated(n, uid, true);
    if (done) return { ok: false, screen: Object.assign({ icon: '✅', title: 'Your Challenge Mock ' + n + ' is submitted', body: 'One attempt is allowed in the live challenge. ' + resLine }, back) };
    const reg = await regAt(uid, true);
    if (!reg || reg >= r.regClose) return { ok: false, screen: Object.assign({ icon: '🔒', title: 'Registration for Challenge Mock ' + n + ' closed on Saturday midnight',
      body: (reg ? 'You are registered from Challenge Mock ' + (n + 1) + ' (' + fmtDay(nx.start) + ').' : 'Register now and you are in for Challenge Mock ' + (n + 1) + ' on ' + fmtDay(nx.start) + '.')
        + ' This paper opens for everyone as a free mock on ' + fmtDay(r.resultAt) + ' at 9 am.' }, back) };
    if (!started && t > r.lastEntry) return { ok: false, screen: Object.assign({ icon: '⏰', title: 'Entry closed at 9:45 pm',
      body: 'The paper is 2 hours 15 minutes long, so the last entry was 9:45 pm. It opens as a free mock on ' + fmtDay(r.resultAt) + ' at 9 am, and you are already in for Challenge Mock ' + (n + 1) + ' on ' + fmtDay(nx.start) + '.' }, back) };
    return { ok: true, mode: 'live', round: n, r };
  }
  if (t < r.resultAt) return { ok: false, screen: Object.assign({ icon: '🕘', title: 'Challenge Mock ' + n + ' is over',
    body: resLine + ' From then this paper is open to everyone as a free mock.' }, back) };
  return { ok: true, mode: 'practice', round: n, r };
}

/* ───────────────────────── page widgets ─────────────────────────
   Any page can carry these empty holders; this file fills them:
     <div data-aic="banner"></div>   wide strip (home page)
     <div data-aic="strip"></div>    slim strip (top of the offers pop-up)
     <div data-aic="hub"></div>      the big status card (challenge page)
     <div data-aic="past"></div>     finished rounds with leaderboard and free-mock links (challenge page)
   and   <body data-aic-popup>  switches on the "results are out" pop-up.     */
const CSS = `
.aicB{font-family:'Hind',system-ui,sans-serif;box-sizing:border-box;border-radius:16px;color:#fff;position:relative;overflow:hidden;
  background:linear-gradient(120deg,#1E1B4B 0%,#4C1D95 48%,#BE185D 100%);box-shadow:0 8px 26px rgba(76,29,149,.28);padding:16px 18px;text-align:left}
.aicB *{box-sizing:border-box}
.aicB::after{content:"";position:absolute;right:-60px;top:-60px;width:210px;height:210px;border-radius:50%;background:radial-gradient(circle,rgba(253,230,138,.28),transparent 68%);pointer-events:none}
.aicB-row{display:flex;align-items:center;gap:14px;flex-wrap:wrap;position:relative;z-index:1}
.aicB-main{flex:1 1 280px;min-width:0}
.aicB-tag{display:inline-flex;align-items:center;gap:6px;background:#FDE68A;color:#4C1D95;border-radius:100px;padding:2px 10px;font-family:'Rajdhani',sans-serif;font-weight:800;font-size:.74rem;letter-spacing:.8px;text-transform:uppercase}
.aicB-tag i{width:7px;height:7px;border-radius:50%;background:#DC2626;font-style:normal;animation:aicPulse 1.2s infinite}
@keyframes aicPulse{0%,100%{opacity:1}50%{opacity:.25}}
.aicB-h{font-family:'Baloo 2','Rajdhani',sans-serif;font-weight:800;font-size:clamp(1.12rem,3.4vw,1.5rem);line-height:1.18;margin:6px 0 3px;color:#fff}
.aicB-h em{font-style:normal;color:#FDE68A}
.aicB-p{font-size:.9rem;line-height:1.5;color:#E9D5FF;margin:0}
.aicB-p b{color:#fff}
.aicB-act{display:flex;flex-direction:column;align-items:stretch;gap:7px;flex:0 0 auto;min-width:190px}
.aicB-btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:44px;padding:9px 18px;border-radius:12px;border:0;cursor:pointer;text-decoration:none;
  font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1.02rem;letter-spacing:.3px;background:linear-gradient(135deg,#F59E0B,#FDE68A);color:#3B0764!important;box-shadow:0 4px 14px rgba(245,158,11,.4)}
.aicB-btn:hover{filter:brightness(1.05)}
.aicB-btn[disabled]{opacity:.7;cursor:wait}
.aicB-btn.ghost{background:rgba(255,255,255,.14);color:#fff!important;box-shadow:none;border:1px solid rgba(255,255,255,.3);min-height:38px;font-size:.9rem;font-weight:700}
.aicB-ok{display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:40px;padding:7px 14px;border-radius:12px;background:rgba(16,185,129,.2);border:1px solid rgba(110,231,183,.6);color:#D1FAE5;font-family:'Rajdhani',sans-serif;font-weight:800;font-size:.98rem}
.aicB-cd{display:flex;gap:6px;margin-top:9px}
.aicB-cd span{background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.2);border-radius:9px;padding:4px 8px;min-width:50px;text-align:center;font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1.12rem;line-height:1.05;color:#fff}
.aicB-cd small{display:block;font-size:.6rem;font-weight:700;letter-spacing:.8px;color:#DDD6FE;text-transform:uppercase}
.aicB-note{font-size:.8rem;color:#DDD6FE;margin:7px 0 0;line-height:1.45;position:relative;z-index:1}
.aicB-note a{color:#FDE68A;font-weight:700}
.aicB-err{color:#FECACA;font-size:.82rem;font-weight:600;margin-top:2px}
.aicB.slim{border-radius:12px;padding:10px 12px;margin:0 0 .7rem;box-shadow:none}
.aicB.slim .aicB-h{font-size:1.02rem;margin:4px 0 2px}
.aicB.slim .aicB-p{font-size:.8rem}
.aicB.slim .aicB-act{min-width:0;flex:1 1 100%;flex-direction:row;flex-wrap:wrap}
.aicB.slim .aicB-act>*{flex:1 1 auto}
.aicB.slim .aicB-btn{min-height:38px;font-size:.95rem;padding:7px 12px}
.aicB.slim .aicB-ok{min-height:34px;font-size:.9rem}
.aicB.slim .aicB-btn.ghost:not([data-aic-hi]){display:none}
.aicB.slim .aicB-cd,.aicB.slim .aicB-note{display:none}
body.aic-pop-open #tsscMP{display:none!important}
.aicB.big{padding:22px 22px 20px}
.aicB.big .aicB-h{font-size:clamp(1.3rem,4.4vw,1.9rem)}
.aicB.big .aicB-p{font-size:.96rem}
@media(max-width:560px){.aicB-act{flex:1 1 100%;min-width:0}.aicB{padding:14px}}
.aicPast{display:grid;gap:12px}
.aicPast-card{background:#fff;border:1px solid #E2E8F0;border-radius:14px;padding:14px 16px}
.aicPast-top{display:flex;align-items:baseline;justify-content:space-between;gap:10px;flex-wrap:wrap}
.aicPast-top h3{font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1.12rem;color:#1A202C;margin:0}
.aicPast-top span{font-size:.82rem;color:#64748B;font-weight:600}
.aicPast-lb{width:100%;border-collapse:collapse;margin:10px 0 8px;font-size:.88rem}
.aicPast-lb td{padding:5px 6px;border-bottom:1px solid #F1F5F9;color:#334155}
.aicPast-lb td:first-child{width:38px;font-family:'Rajdhani',sans-serif;font-weight:800;color:#7C3AED}
.aicPast-lb td:last-child{text-align:right;font-weight:700;color:#1A202C;white-space:nowrap}
.aicPast-btns{display:flex;flex-wrap:wrap;gap:8px}
.aicPast-btns a{display:inline-flex;align-items:center;min-height:38px;padding:7px 13px;border-radius:10px;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.9rem;text-decoration:none;border:1.5px solid #DDD6FE;color:#5B21B6!important;background:#F5F3FF}
.aicPast-btns a.go{background:linear-gradient(135deg,#FF6B00,#FF8C38);border-color:#FF6B00;color:#fff!important}
.aicPast-empty{background:#fff;border:1px dashed #CBD5E1;border-radius:14px;padding:14px 16px;color:#64748B;font-size:.9rem}
#aicPop{position:fixed;inset:0;z-index:100000;display:flex;align-items:center;justify-content:center;background:rgba(15,23,42,.6);padding:16px}
#aicPop .aicPop-box{position:relative;width:100%;max-width:430px}
#aicPop .aicPop-x{position:absolute;top:8px;right:8px;z-index:3;width:32px;height:32px;border:0;border-radius:50%;background:rgba(255,255,255,.22);color:#fff;font-size:1.1rem;cursor:pointer;line-height:1}
#aicPop .aicB-row{flex-direction:column;align-items:stretch}
#aicPop .aicB-main{flex:0 0 auto}
#aicPop .aicB{padding:24px 20px 20px;text-align:center}
#aicPop .aicB-cd{justify-content:center}
#aicPop .aicB-note{text-align:center}
#aicPop .aicPop-box{animation:aicPopUp .26s cubic-bezier(.16,1,.3,1)}
@keyframes aicPopUp{from{transform:translateY(12px);opacity:0}to{transform:none;opacity:1}}
@media(prefers-reduced-motion:reduce){#aicPop .aicPop-box{animation:none}}
`;
function injectCss() { if (document.getElementById('aicCss')) return; const s = document.createElement('style'); s.id = 'aicCss'; s.textContent = CSS; document.head.appendChild(s); }

/* What to show a visitor right now. One description, three sizes. */
async function buildState() {
  const t = now(); let n = nextRound(t);
  const uid = currentUid();
  if (!hasRound(n)) {                       // the series is over: only the last result is left to show
    const p = CFG.lastRound; const pr = round(p);
    if (t > pr.resultAt + 6 * 24 * H) return null;
    const done = uid ? await participated(p, uid) : null;
    return { kind: t >= pr.resultAt ? 'result-final' : 'wait-final', n: p, r: pr, done, uid };
  }
  const r = round(n), reg = uid ? await regAt(uid) : 0;
  const prev = n > 1 ? round(n - 1) : null;
  const prevDone = (prev && uid) ? await participated(n - 1, uid) : null;
  const st = { n, r, uid, reg, prev, prevDone, t };
  st.prevPhase = !prev ? '' : (t < prev.resultAt ? 'wait' : 'out');
  if (t >= r.start) {                       // Sunday, the window is open
    st.done = uid ? await participated(n, uid) : null;
    if (st.done) st.kind = 'submitted';
    else if (reg && reg < r.regClose) st.kind = (t <= r.lastEntry || startedAt(n, uid)) ? 'live' : 'missed';
    else st.kind = reg ? 'live-next' : 'live-closed';
  } else if (reg && reg < r.regClose) st.kind = 'registered';
  else if (reg) st.kind = 'registered-next';
  else st.kind = t < r.regClose ? 'open' : 'closed';
  return st;
}

function cdHtml(target, label) {
  return '<div class="aicB-cd" data-aic-cd="' + target + '"><span><b data-d>0</b><small>days</small></span><span><b data-h>00</b><small>hrs</small></span><span><b data-m>00</b><small>min</small></span><span><b data-s>00</b><small>sec</small></span></div>'
    + (label ? '<p class="aicB-note" style="margin-top:4px">' + label + '</p>' : '');
}
function tickCd() {
  document.querySelectorAll('[data-aic-cd]').forEach(el => {
    let d = Math.max(0, parseInt(el.getAttribute('data-aic-cd'), 10) - now());
    if (d <= 0 && !el.dataset.fired) { el.dataset.fired = '1'; setTimeout(render, 1200); }
    const s = Math.floor(d / 1000), p = v => String(v).padStart(2, '0');
    const q = k => el.querySelector('[data-' + k + ']');
    if (q('d')) q('d').textContent = Math.floor(s / 86400);
    if (q('h')) q('h').textContent = p(Math.floor(s % 86400 / 3600));
    if (q('m')) q('m').textContent = p(Math.floor(s % 3600 / 60));
    if (q('s')) q('s').textContent = p(s % 60);
  });
}
const waShare = n => 'https://wa.me/?text=' + encodeURIComponent('SSC CGL Tier 2 All India Challenge Mock ' + n + ' on TrickySSC — free, new sectional timing, All India rank. Register here: https://trickyssc.com' + CFG.page);

function stateHtml(st, size) {
  if (!st) return '';
  const n = st.n, r = st.r, nx = round(n + 1);
  const title = 'SSC CGL Tier 2 <em>All India Challenge Mock ' + n + '</em>';
  const when = '<b>' + fmtDay(r.start) + '</b>, 9 am to 12 midnight';
  const more = size === 'big' ? '' : '<a class="aicB-btn ghost" href="' + CFG.page + '">How it works</a>';
  const regBtn = label => '<button type="button" class="aicB-btn" data-aic-register>' + label + '</button><div class="aicB-err" data-aic-err hidden></div>';
  /* line about the round that just finished */
  let prevLine = '';
  if (st.prev) {
    if (st.prevPhase === 'wait') prevLine = st.prevDone ? 'Your Challenge Mock ' + (n - 1) + ' is submitted. Result on <b>' + fmtDay(st.prev.resultAt) + ', 9 am</b>.' : '';
    else prevLine = 'Challenge Mock ' + (n - 1) + ' results are out. <a href="' + (st.prevDone ? resultUrl(n - 1, st.prevDone) : CFG.page + '#results') + '">' + (st.prevDone ? 'Check your result and rank' : 'See the leaderboard') + '</a>';
  }
  let tag = 'Free · Every Sunday', head = title, body = '', act = '', extra = '';
  switch (st.kind) {
    case 'open':
      tag = 'Free · Registration open';
      body = when + '. New 30-30-40-20-15 sectional timing, All India rank, full analysis. Registration closes <b>Saturday midnight</b>.';
      act = regBtn('Register free →') + more; extra = cdHtml(r.regClose, 'Time left to register for this Sunday'); break;
    case 'closed':
      tag = 'Registration closed for this Sunday';
      body = 'Challenge Mock ' + n + ' is on ' + when + ' for registered students. Register now and you are in from <b>Challenge Mock ' + (n + 1) + ' on ' + fmtDay(nx.start) + '</b>.';
      act = regBtn('Register for Mock ' + (n + 1) + ' →') + more; break;
    case 'registered':
      tag = 'You are registered';
      body = 'Your paper opens on ' + when + ' (last entry 9:45 pm). One attempt. Result on <b>' + fmtDay(r.resultAt) + ', 9 am</b>.';
      act = '<span class="aicB-ok">✓ Registered for all challenge mocks</span><a class="aicB-btn ghost" target="_blank" rel="noopener" href="' + waShare(n) + '">Invite friends on WhatsApp</a>';
      extra = cdHtml(r.start, 'Mock opens in'); break;
    case 'registered-next':
      tag = 'You are registered';
      head = 'SSC CGL Tier 2 <em>All India Challenge Mock ' + (n + 1) + '</em>';
      body = 'Registration for this Sunday had closed, so your first paper is <b>Challenge Mock ' + (n + 1) + ' on ' + fmtDay(nx.start) + '</b>, 9 am to 12 midnight.';
      act = '<span class="aicB-ok">✓ Registered from Mock ' + (n + 1) + '</span>' + more; extra = cdHtml(nx.start, 'Your mock opens in'); break;
    case 'live':
      tag = '<i></i>Live now';
      body = 'The paper is open until <b>12 midnight</b> (last entry 9:45 pm). 150 questions, 2 hours 15 minutes, one attempt.';
      act = '<a class="aicB-btn" href="' + testUrl(n, 'en') + '">Start in English →</a><a class="aicB-btn ghost" data-aic-hi href="' + testUrl(n, 'hi') + '">हिंदी में शुरू करें</a>';
      extra = cdHtml(r.lastEntry, 'Last entry closes in'); break;
    case 'missed':
      tag = 'Entry closed at 9:45 pm';
      body = 'This paper opens as a free mock on <b>' + fmtDay(r.resultAt) + ', 9 am</b>. You are already in for <b>Challenge Mock ' + (n + 1) + ' on ' + fmtDay(nx.start) + '</b>.';
      act = '<span class="aicB-ok">✓ Registered for Mock ' + (n + 1) + '</span>' + more; break;
    case 'live-next':
      tag = 'You are registered';
      head = 'SSC CGL Tier 2 <em>All India Challenge Mock ' + (n + 1) + '</em>';
      body = 'Today\'s paper is for students who registered before Saturday midnight. Your first paper is on <b>' + fmtDay(nx.start) + '</b>; today\'s opens as a free mock on ' + fmtDay(r.resultAt) + '.';
      act = '<span class="aicB-ok">✓ Registered from Mock ' + (n + 1) + '</span>' + more; break;
    case 'live-closed':
      tag = '<i></i>Challenge Mock ' + n + ' is live';
      body = 'Today\'s paper is open only to students who registered before Saturday midnight. Register now and you are in from <b>Challenge Mock ' + (n + 1) + ' on ' + fmtDay(nx.start) + '</b>.';
      act = regBtn('Register for Mock ' + (n + 1) + ' →') + more; break;
    case 'submitted':
      tag = 'Submitted';
      body = 'Your test has been submitted successfully. Result, All India rank and solutions on <b>' + fmtDay(r.resultAt) + ', 9 am</b>. You are already in for Challenge Mock ' + (n + 1) + ' on ' + fmtDay(nx.start) + '.';
      act = '<span class="aicB-ok">✓ Test submitted</span><a class="aicB-btn ghost" href="' + CFG.mocks + '">Practise Tier 2 mocks</a>';
      extra = cdHtml(r.resultAt, 'Result in'); break;
    case 'wait-final':
      body = st.done ? 'Your test has been submitted successfully. Result on <b>' + fmtDay(r.resultAt) + ', 9 am</b>.' : 'The last challenge is over. Results on <b>' + fmtDay(r.resultAt) + ', 9 am</b>.';
      act = more; break;
    case 'result-final':
      tag = 'Results out';
      body = 'Challenge Mock ' + n + ' results are out.';
      act = '<a class="aicB-btn" href="' + (st.done ? resultUrl(n, st.done) : CFG.page + '#results') + '">' + (st.done ? 'Check your result →' : 'See the leaderboard →') + '</a>'; break;
  }
  const note = (prevLine && st.kind !== 'wait-final' && st.kind !== 'result-final') ? '<p class="aicB-note">' + prevLine + '</p>' : '';
  return '<div class="aicB' + (size === 'slim' ? ' slim' : size === 'big' ? ' big' : '') + '"><div class="aicB-row"><div class="aicB-main">'
    + '<span class="aicB-tag">' + tag + '</span><div class="aicB-h">' + head + '</div><p class="aicB-p">' + body + '</p>' + extra + '</div>'
    + '<div class="aicB-act">' + act + '</div></div>' + note + '</div>';
}

let _busy = false;
async function onRegisterClick(btn) {
  if (_busy) return; _busy = true;
  const old = btn.innerHTML; btn.disabled = true; btn.innerHTML = 'Registering…';
  const err = btn.parentNode.querySelector('[data-aic-err]');
  if (err) err.hidden = true;
  let res; try { res = await register(); } catch (e) { res = { ok: false, reason: 'write' }; }
  _busy = false;
  if (res.ok) { await render(); return; }
  btn.disabled = false; btn.innerHTML = old;
  if (err) { err.hidden = false; err.textContent = res.reason === 'login' ? 'Please log in to register.' : 'Could not register. Check your internet and tap again.'; }
}

async function paintPast(el) {
  const t = now(); const last = nextRound(t) - 1; const rows = [];
  for (let n = Math.min(last, CFG.lastRound || last); n >= 1 && rows.length < 4; n--) if (t >= round(n).resultAt) rows.push(n);
  if (!rows.length) {
    el.innerHTML = '<div class="aicPast-empty">The first result comes out on <b>' + fmtDay(round(1).resultAt) + ' at 9 am</b>. The leaderboard, and the paper as a free mock, will appear here on their own.</div>';
    return;
  }
  const uid = currentUid();
  const cards = await Promise.all(rows.map(async (n, i) => {
    const r = round(n); let total = 0, top = [];
    const ck = 'tssc_aic_past_' + n, cc = ssGet(ck, MIN10);
    if (cc) { total = cc.v.total; top = cc.v.top; }
    else {
      try { total = (await getCountFromServer(collection(db, 'leaderboards', r.board, 'scores'))).data().count || 0; } catch (e) {}
      if (i === 0) { try { const s = await getDocs(query(collection(db, 'leaderboards', r.board, 'scores'), orderBy('marks', 'desc'), limit(10))); s.forEach(d => { const x = d.data() || {}; top.push({ name: x.name, marks: x.marks, maxMarks: x.maxMarks }); }); } catch (e) {} }
      ssSet(ck, { total, top });
    }
    const hi = await hasLang(n, 'hi');
    const done = uid ? await participated(n, uid) : null;
    const lb = top.length ? '<table class="aicPast-lb">' + top.map((x, k) => '<tr><td>#' + (k + 1) + '</td><td>' + esc(String(x.name || 'Student').slice(0, 28)) + '</td><td>' + esc(x.marks) + (x.maxMarks ? ' / ' + esc(x.maxMarks) : '') + '</td></tr>').join('') + '</table>' : '';
    return '<div class="aicPast-card"><div class="aicPast-top"><h3>All India Challenge Mock ' + n + '</h3><span>' + fmtDate(r.start) + (total ? ' · ' + total.toLocaleString('en-IN') + ' students' : '') + '</span></div>' + lb
      + '<div class="aicPast-btns">' + (done ? '<a class="go" href="' + resultUrl(n, done) + '">My result and rank</a>' : '')
      + '<a href="/rank.html?paper=' + encodeURIComponent(r.board) + '&name=' + encodeURIComponent('All India Challenge Mock ' + n) + '">Full leaderboard</a>'
      + '<a' + (done ? '' : ' class="go"') + ' href="' + testUrl(n, 'en') + '">Attempt as free mock</a>' + (hi ? '<a href="' + testUrl(n, 'hi') + '">हिंदी में</a>' : '') + '</div></div>';
  }));
  el.innerHTML = '<div class="aicPast">' + cards.join('') + '</div>';
}

/* <tbody data-aic="schedule"> — the next four Sundays (the rows typed in the page are only the no-JavaScript fallback) */
function paintSchedule() {
  const el = document.querySelector('[data-aic="schedule"]'); if (!el) return;
  const t = now(); let n = nextRound(t); const rows = [];
  for (let i = 0; i < 4 && hasRound(n + i); i++) {
    const r = round(n + i), live = t >= r.start && t < r.end;
    rows.push('<tr><td><b>Challenge Mock ' + r.n + '</b>' + (live ? ' <span style="color:#DC2626;font-weight:700;">· live now</span>' : '') + '</td><td>' + fmtShort(r.regClose - 60000) + ', 11:59 pm</td><td>' + fmtShort(r.start) + ', 9 am – 12 midnight</td><td>' + fmtShort(r.resultAt) + ', 9 am</td></tr>');
  }
  if (rows.length) el.innerHTML = rows.join('');
}

async function paintCount() {
  const els = document.querySelectorAll('[data-aic-count]'); if (!els.length) return;
  try {
    const cc = ssGet('tssc_aic_count', MIN10);
    const c = cc ? cc.v : ((await getCountFromServer(collection(db, 'leaderboards', CFG.regBoard, 'scores'))).data().count || 0);
    if (!cc) ssSet('tssc_aic_count', c);
    els.forEach(el => { if (c >= 50) { el.textContent = c.toLocaleString('en-IN') + ' students registered so far'; el.hidden = false; } else el.hidden = true; });
  } catch (e) {}
}

let _rendering = null;
export function render() {
  if (_rendering) return _rendering;
  _rendering = (async () => {
    try {
      const holders = document.querySelectorAll('[data-aic="banner"],[data-aic="strip"],[data-aic="hub"]');
      const past = document.querySelector('[data-aic="past"]');
      injectCss();
      const st = await buildState();
      holders.forEach(el => {
        const size = el.getAttribute('data-aic') === 'strip' ? 'slim' : el.getAttribute('data-aic') === 'hub' ? 'big' : '';
        el.innerHTML = stateHtml(st, size); el.hidden = !st;
        el.querySelectorAll('[data-aic-register]').forEach(b => b.addEventListener('click', () => onRegisterClick(b)));
      });
      tickCd();
      if (st && st.kind === 'live') hasLang(st.n, 'hi').then(ok => { if (!ok) document.querySelectorAll('[data-aic-hi]').forEach(a => a.remove()); });
      if (past) paintPast(past).catch(() => {});
      paintSchedule();
      paintCount();
      maybePopup(st);
    } catch (e) { console.warn('[aic] render:', e); if (_authKnown && !_popDecided && document.body.hasAttribute('data-aic-popup')) { _popDecided = true; popSignal('none'); } }
    finally { _rendering = null; }
  })();
  return _rendering;
}

/* TSSC-AICPOP-V2 (2026-11-21) — the home page has no banner any more: the challenge is a pop-up, and the plans
   pop-up opens only after this one is closed.
   What it shows:
     - "results are out" (Tuesday 9 am until the next paper opens), once a day per browser;
     - otherwise today's state of the challenge (register / registered / live / submitted):
         someone not yet registered, or a registered student on the live Sunday  → once per browser session
         a registered student on other days                                      → once a day
   window.__tsscAicPop = 'open' | 'closed' | 'none' and the event "tssc:aic-pop-done" tell the plans pop-up when to open. */
let _authKnown = false, _popDecided = false, _popVariant = '';
const ONCE_A_DAY = { registered: 1, 'registered-next': 1, missed: 1, 'live-next': 1, submitted: 1, 'wait-final': 1, 'result-final': 1 };
const istDay = () => new Date(now() + 19800000).toISOString().slice(0, 10);
function popSignal(v) { window.__tsscAicPop = v; if (v !== 'open') { try { window.dispatchEvent(new Event('tssc:aic-pop-done')); } catch (e) {} } }
function popClose() {
  const box = document.getElementById('aicPop'); if (box) box.remove();
  document.body.classList.remove('aic-pop-open'); _popVariant = ''; popSignal('closed');
}
function popShell(inner) {
  let box = document.getElementById('aicPop');
  if (!box) {
    box = document.createElement('div'); box.id = 'aicPop'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'SSC CGL Tier 2 All India Challenge Mock');
    box.addEventListener('click', e => { if (e.target === box) popClose(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && document.getElementById('aicPop')) popClose(); });
    document.body.appendChild(box);
  }
  box.innerHTML = '<div class="aicPop-box"><button type="button" class="aicPop-x" aria-label="Close">&times;</button>' + inner + '</div>';
  box.querySelector('.aicPop-x').addEventListener('click', popClose);
  box.querySelectorAll('[data-aic-register]').forEach(b => b.addEventListener('click', () => onRegisterClick(b)));
  document.body.classList.add('aic-pop-open');   /* the plans pop-up waits behind this one */
  tickCd();
  return box;
}
function resultsHtml(st) {
  const p = st.n - 1;
  const nextLine = st.reg ? 'You are already registered for <b>Challenge Mock ' + st.n + ' on ' + fmtDay(st.r.start) + '</b>.'
    : 'Next: <b>Challenge Mock ' + st.n + ' on ' + fmtDay(st.r.start) + '</b>. Register free before Saturday midnight.';
  return '<div class="aicB"><div class="aicB-row"><div class="aicB-main">'
    + '<span class="aicB-tag">Results out</span><div class="aicB-h">All India Challenge Mock ' + p + ' <em>results are out</em></div>'
    + '<p class="aicB-p">' + (st.prevDone ? 'Your All India rank, percentile, topper comparison and full solutions are ready.' : 'See who topped, and attempt the paper as a free mock with full solutions.') + '</p>'
    + '<p class="aicB-p" style="margin-top:8px">' + nextLine + '</p></div><div class="aicB-act">'
    + '<a class="aicB-btn" href="' + (st.prevDone ? resultUrl(p, st.prevDone) : CFG.page + '#results') + '">' + (st.prevDone ? 'Check your result →' : 'See the leaderboard →') + '</a>'
    + (st.reg ? '' : '<button type="button" class="aicB-btn ghost" data-aic-register>Register for Challenge Mock ' + st.n + '</button><div class="aicB-err" data-aic-err hidden></div>')
    + '</div></div></div>';
}
function maybePopup(st) {
  if (!document.body.hasAttribute('data-aic-popup')) return;
  /* an open pop-up follows the student's state (for example right after registering) */
  if (document.getElementById('aicPop')) {
    if (st) popShell(_popVariant === 'results' ? resultsHtml(st) : stateHtml(st, ''));
    return;
  }
  if (_popDecided || !_authKnown) return;          // decide once per page load, and only when the login state is known
  _popDecided = true;
  if (!st) { popSignal('none'); return; }
  const day = istDay();
  let variant = '';
  if (st.prev && st.prevPhase === 'out' && st.t < st.r.start && lsGet('tssc_aic_pop_' + (st.n - 1)) !== day) variant = 'results';
  else if (ONCE_A_DAY[st.kind]) { if (lsGet('tssc_aic_pop_d') !== day + ':' + st.kind) variant = 'state'; }
  else if (!ssGet('tssc_aic_pop_s', 864e5)) variant = 'state';
  if (!variant) { popSignal('none'); return; }
  if (variant === 'results') lsSet('tssc_aic_pop_' + (st.n - 1), day);
  if (ONCE_A_DAY[st.kind]) lsSet('tssc_aic_pop_d', day + ':' + st.kind);
  ssSet('tssc_aic_pop_s', 1);
  _popVariant = variant; popSignal('open');
  popShell(variant === 'results' ? resultsHtml(st) : stateHtml(st, ''));
}

/* ───────────────────────── start ───────────────────────── */
window.tsscAic = { CFG, round, nextRound, isAicId, roundOfMock, testUrl, now, syncClock, regAt, register, participated,
  markStarted, markDone, startedAt, resultUrl, gate, render, fmtDay };
function boot() {
  if (!document.querySelector('[data-aic]') && !document.body.hasAttribute('data-aic-popup')) return;
  syncClock().then(render);
  authReady.then(async () => { _authKnown = true; await render(); if (!_popDecided) await render(); });   /* TSSC-AICPOP-V2 */
  try { onAuthStateChanged(auth, () => render()); } catch (e) {}
  window.addEventListener('tssc:login', () => render());
  setInterval(tickCd, 1000);
  /* ?register=1 — a student sent to log in from the Register button comes back here and is registered */
  try { if (new URLSearchParams(location.search).get('register') === '1') authReady.then(async () => { if (auth.currentUser) { await register(); render(); } }); } catch (e) {}
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
