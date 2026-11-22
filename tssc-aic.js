/* ============================================================================
   tssc-aic.js — ALL INDIA CHALLENGE MOCKS                          TSSC-AIC-V2
   ----------------------------------------------------------------------------
   Two free weekly challenge series run from this one file:
     cgl   SSC CGL Tier 2    every Sunday    from 29 Nov 2026 (no end date yet)
     chsl  SSC CHSL Tier 1   every Saturday  from 28 Nov 2026 to 26 Dec 2026
   Everything on the site that belongs to a challenge reads its dates and rules
   from THIS file, and every state (register / registered / mock is live /
   submitted / results out / next round) is worked out from the clock. Nothing
   has to be switched on or published by hand.

   THE WEEKLY TIMELINE of a series (all times IST), round N = week N from DEFS.first
     the day before, 11:59 pm   registration for that round closes
     challenge day  9:00 am     mock opens (registered students only, one attempt)
     challenge day  last entry  midnight minus the length of the paper
     challenge day  12 midnight window closes
     two days later 9:00 am     result + All India rank + solutions open on their
                                own, and the paper becomes a free mock for everyone

   REGISTRATION is one time PER SERIES. A student who registers once is in every
   later round of that series; a registration made after the closing midnight
   counts from the next round.

   THE PAPER of round N is the mock uploaded as  <exam>_aic_mockN_en / _hi
   (batch-uploader-mock.html, tier "aic"):  ssc-cgl_aic_mock1_en,  ssc-chsl_aic_mock1_en ...
   Its mock_tests cards are saved as drafts on purpose, so no mock list or count
   on the site picks them up. Both series are played in /mock-test-tier2.html.

   WHERE THINGS ARE STORED (no new collections, no rules change)
     users/{uid}.aic      = { reg:true, at:<server time>, src:'web' }   CGL registration
     users/{uid}.aicChsl  = { reg:true, at:<server time>, src:'web' }   CHSL registration
     leaderboards/aic-registered/scores/{uid}        CGL registration, for the public count
     leaderboards/aic-chsl-registered/scores/{uid}   CHSL registration, for the public count
     leaderboards/<exam>_aic_mockN/scores/{uid}      LIVE attempts only = the All India rank
     attempts/{id}.aic = { round:N, live:true|false, resultAt:<ms> }    set by mock-test-tier2.html

   TO CHANGE SOMETHING
     - dates, last round, length of the paper:  DEFS below
     - result time, window:                     the numbers in round() below
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

/* ───────────────────────── the two series ───────────────────────── */
const H = 3600000;
const DEFS = {
  cgl: {
    key: 'cgl', exam: 'ssc-cgl', name: 'SSC CGL Tier 2', short: 'CGL Tier 2',
    first: Date.UTC(2026, 10, 29, 3, 30, 0),   // Sunday 29 Nov 2026, 9:00 am IST — Challenge Mock 1
    week: 7 * 24 * H,
    lastRound: 0,                              // 0 = every week with no end; set to N to make round N the last
    page: '/ssc-cgl-tier-2-all-india-challenge-mock.html',
    mocks: '/ssc-cgl-tier-2-mock-test.html', mocksLabel: 'Practise Tier 2 mocks',
    regBoard: 'aic-registered', regField: 'aic',
    tag: '',                                   // part of this browser's storage keys ('' = the keys of the first release)
    urlTier: 'tier2',
    paperMin: 135, paperLen: '2 hours 15 minutes', hardStopMin: 145,
    pitch: 'New 30-30-40-20-15 sectional timing, All India rank, full analysis.',
    paperLine: '150 questions, 2 hours 15 minutes, one attempt.',
    graceMs: 30 * 60000                        // a test started in the window may still be submitted this long after midnight
  },
  chsl: {
    key: 'chsl', exam: 'ssc-chsl', name: 'SSC CHSL Tier 1', short: 'CHSL Tier 1',
    first: Date.UTC(2026, 10, 28, 3, 30, 0),   // Saturday 28 Nov 2026, 9:00 am IST — Challenge Mock 1
    week: 7 * 24 * H,
    lastRound: 5,                              // Saturdays 28 Nov, 5, 12, 19 and 26 Dec 2026 (Tier 1 exam: 30 Nov to 31 Dec)
    page: '/ssc-chsl-tier-1-all-india-challenge-mock.html',
    mocks: '/ssc-chsl-mock-test.html', mocksLabel: 'Practise CHSL mocks',
    regBoard: 'aic-chsl-registered', regField: 'aicChsl',
    tag: 'chsl_',
    urlTier: 'tier1',
    paperMin: 60, paperLen: '60 minutes', hardStopMin: 70,
    pitch: 'Real exam pattern (100 questions, 60 minutes), All India rank, full analysis.',
    paperLine: '100 questions, 60 minutes, one attempt.',
    graceMs: 30 * 60000
  }
};

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

const dayName = ms => new Date(ms).toLocaleDateString('en-IN', Object.assign({ weekday: 'long' }, IST));
const fmtTime = ms => new Date(ms).toLocaleTimeString('en-IN', Object.assign({ hour: 'numeric', minute: '2-digit', hour12: true }, IST)).replace(':00', '').toLowerCase();

/* One login for every Register button. → the user, or null when the student was sent to the login page. */
async function ensureLogin(backTo) {
  if (auth.currentUser) return auth.currentUser;
  await authReady;
  if (auth.currentUser) return auth.currentUser;
  if (!window.tsscLogin) { try { await import('/login-modal.js'); } catch (e) {} }
  for (let i = 0; i < 40 && !window.tsscLogin; i++) await new Promise(r => setTimeout(r, 100));
  if (!window.tsscLogin) { lsSet('loginReturnTo', location.origin + backTo); location.href = '/login.html'; return null; }
  return await window.tsscLogin.require();
}

/* ───────────────────────── one series ───────────────────────── */
function makeSeries(D) {
  const K = 'tssc_aic_' + D.tag;               // storage key prefix of this series
  function round(n) {
    n = Math.max(1, parseInt(n, 10) || 1);
    const start = D.first + (n - 1) * D.week;
    const end = start + 15 * H;
    return {
      n,
      start,                                   // challenge day 9:00 am
      lastEntry: end - D.paperMin * 60000,     // midnight minus the length of the paper
      end,                                     // challenge day midnight
      regClose: start - 9 * H,                 // the midnight before
      resultAt: start + 48 * H,                // two days later, 9:00 am
      board: D.exam + '_aic_mock' + n,
      mockId: lang => D.exam + '_aic_mock' + n + '_' + (lang === 'hi' ? 'hi' : 'en')
    };
  }
  const hasRound = n => n >= 1 && (!D.lastRound || n <= D.lastRound);
  /* the round a visitor should be looking at: the first one whose challenge day is not over yet */
  function nextRound(t) {
    let n = Math.max(1, Math.floor((t - (D.first + 15 * H)) / D.week) + 2);
    while (n > 1 && t < round(n - 1).end) n--;
    return n;
  }
  function testUrl(n, lang) {
    const l = lang === 'hi' ? 'hi' : 'en';
    return '/mock-test-tier2.html?exam=' + D.exam + '&tier=' + D.urlTier + '&series=' + n + '&lang=' + l + '&mockId=' + round(n).mockId(l);
  }

  /* ── registration ── */
  const regKey = uid => K + 'reg_' + uid;
  /* → the time (ms) this student registered, or 0. fresh=true always asks the server. */
  async function regAt(uid, fresh) {
    if (!uid) return 0;
    const c = parseInt(lsGet(regKey(uid)) || '', 10);
    if (isFinite(c) && c > 0 && !fresh) return c;
    if (!fresh && ssGet(K + 'noreg_' + uid, MIN5)) return 0;
    let at = 0, read = false;
    try {
      const s = await getDoc(doc(db, 'users', uid)); read = true;
      const a = s.exists() ? (s.data() || {})[D.regField] : null;
      if (a && a.reg) at = tsMs(a.at) || now();
    } catch (e) {}
    if (!at) {
      try { const s = await getDoc(doc(db, 'leaderboards', D.regBoard, 'scores', uid)); read = true;
        if (s.exists()) at = tsMs((s.data() || {}).submittedAt) || now(); } catch (e) {}
    }
    if (at) { lsSet(regKey(uid), String(at)); ssDel(K + 'noreg_' + uid); return at; }
    if (read) ssSet(K + 'noreg_' + uid, 1);
    /* the server could not be reached: trust what this phone remembers */
    return (!read && isFinite(c) && c > 0) ? c : 0;
  }
  /* One click. Asks for login first when needed. → { ok, at, already } or { ok:false, reason } */
  async function register() {
    const u = await ensureLogin(D.page + '?register=' + D.key);
    if (!u || !u.uid) return { ok: false, reason: 'login' };
    const had = await regAt(u.uid, true);
    if (had) return { ok: true, at: had, already: true };
    let ok = false;
    try { await setDoc(doc(db, 'users', u.uid), { [D.regField]: { reg: true, at: serverTimestamp(), src: 'web' } }, { merge: true }); ok = true; }
    catch (e) { console.warn('[aic] register (profile):', e && e.message); }
    /* the same row on a board, so the page can show how many students are in (same write the leaderboards use) */
    try {
      const lb = await import('/leaderboard.js');
      await lb.recordScore({ uid: u.uid, displayName: u.displayName, paperId: D.regBoard, paperName: D.name + ' All India Challenge registration', marks: 0, maxMarks: 0 });
      if (!ok) { const s = await getDoc(doc(db, 'leaderboards', D.regBoard, 'scores', u.uid)); ok = s.exists(); }
    } catch (e) { console.warn('[aic] register (board):', e && e.message); }
    if (!ok) return { ok: false, reason: 'write' };
    const at = now();
    lsSet(regKey(u.uid), String(at)); ssDel(K + 'noreg_' + u.uid); ssDel(K + 'count');
    try { if (window.gtag) window.gtag('event', 'aic_register', { series: D.key, round: nextRound(at) }); } catch (e) {}
    return { ok: true, at };
  }

  /* ── a student's round ── */
  const doneKey  = (n, uid) => K + 'done_' + n + '_' + uid;
  const startKey = (n, uid) => K + 'start_' + n + '_' + uid;
  function markStarted(n, uid) { if (uid && !lsGet(startKey(n, uid))) lsSet(startKey(n, uid), String(now())); }
  function startedAt(n, uid) { const v = parseInt(lsGet(startKey(n, uid)) || '', 10); return isFinite(v) ? v : 0; }
  function markDone(n, uid, attemptId) { if (uid) lsSet(doneKey(n, uid), JSON.stringify({ id: attemptId || '', at: now() })); }
  /* → { id } when this student has a LIVE attempt in round n, else null */
  async function participated(n, uid, fresh) {
    if (!uid) return null;
    try { const o = JSON.parse(lsGet(doneKey(n, uid)) || 'null'); if (o && !fresh) return o; } catch (e) {}
    if (!fresh && ssGet(K + 'np_' + n + '_' + uid, MIN5)) return null;
    try {
      const s = await getDoc(doc(db, 'leaderboards', round(n).board, 'scores', uid));
      if (s.exists()) { let id = ''; try { id = (JSON.parse(lsGet(doneKey(n, uid)) || 'null') || {}).id || ''; } catch (e) {}
        const o = { id, at: tsMs((s.data() || {}).submittedAt) || 0 }; lsSet(doneKey(n, uid), JSON.stringify(o)); return o; }
      ssSet(K + 'np_' + n + '_' + uid, 1);
    } catch (e) { try { return JSON.parse(lsGet(doneKey(n, uid)) || 'null'); } catch (_) {} }
    return null;
  }
  function resultUrl(n, done) {
    return '/test-analysis.html?' + (done && done.id ? 'id=' + encodeURIComponent(done.id) : 'aic=' + n + (D.key === 'cgl' ? '' : '&aics=' + D.key));
  }
  /* Is this language of round n uploaded? (the Hindi button is hidden when it is not) */
  async function hasLang(n, lang) {
    const k = K + 'lang_' + n + '_' + lang; const c = ssGet(k, MIN10); if (c) return !!c.v;
    try { const s = await getDoc(doc(db, 'mock_tests', round(n).mockId(lang))); ssSet(k, s.exists() ? 1 : 0); return s.exists(); }
    catch (e) { return true; }
  }
  /* words for the texts: "Sunday", "Saturday midnight", "9:45 pm" */
  const words = r => ({ day: dayName(r.start), regDay: dayName(r.regClose - 60000), last: fmtTime(r.lastEntry) });
  const nextIn = n => hasRound(n + 1) ? round(n + 1) : null;

  /* ── the gate (used by mock-test-tier2.html) ──
     → { ok:true, mode:'live'|'practice', round, r, api }  or  { ok:false, screen:{ icon, title, body, cta, href } } */
  async function gate(uid, mockId) {
    await syncClock();
    const n = roundOfMock(mockId), t = now();
    const back = { cta: 'Open the All India Challenge page', href: D.page };
    if (!hasRound(n)) return { ok: false, screen: Object.assign({ icon: '📭', title: 'This challenge mock is not available', body: 'Please open the All India Challenge page for the current schedule.' }, back) };
    const r = round(n), nx = nextIn(n), w = words(r);
    const resLine = 'Result, All India rank and solutions: <b>' + fmtDay(r.resultAt) + ', 9 am</b>.';
    const freeLine = 'This paper opens for everyone as a free mock on ' + fmtDay(r.resultAt) + ' at 9 am.';
    const nxName = nx ? 'Challenge Mock ' + (n + 1) + ' (' + fmtDay(nx.start) + ')' : '';
    if (t < r.start) {
      const reg = await regAt(uid);
      const inTime = reg && reg < r.regClose;
      return { ok: false, screen: Object.assign({ icon: '⏳', title: 'Challenge Mock ' + n + ' opens on ' + fmtDay(r.start) + ' at 9 am',
        body: inTime ? 'You are registered. Come back on ' + w.day + ' between 9 am and ' + w.last + ' to take the paper.'
          : (t < r.regClose ? 'Register (free, one click) before ' + w.regDay + ' midnight to take this paper in the live window.'
            : 'Registration for this ' + w.day + ' is closed. ' + (nx ? (reg ? 'You are in from ' + nxName + '.' : 'Register now for ' + nxName + '.') : freeLine)) }, back) };
    }
    const started = startedAt(n, uid);
    if (t < r.end || (started && t < r.end + D.graceMs)) {
      const done = await participated(n, uid, true);
      if (done) return { ok: false, screen: Object.assign({ icon: '✅', title: 'Your Challenge Mock ' + n + ' is submitted', body: 'One attempt is allowed in the live challenge. ' + resLine }, back) };
      const reg = await regAt(uid, true);
      if (!reg || reg >= r.regClose) return { ok: false, screen: Object.assign({ icon: '🔒', title: 'Registration for Challenge Mock ' + n + ' closed on ' + w.regDay + ' midnight',
        body: (nx ? (reg ? 'You are registered from ' + nxName + '. ' : 'Register now and you are in for ' + nxName + '. ') : '') + freeLine }, back) };
      if (!started && t > r.lastEntry) return { ok: false, screen: Object.assign({ icon: '⏰', title: 'Entry closed at ' + w.last,
        body: 'The paper is ' + D.paperLen + ' long, so the last entry was ' + w.last + '. It opens as a free mock on ' + fmtDay(r.resultAt) + ' at 9 am'
          + (nx ? ', and you are already in for ' + nxName + '.' : '.') }, back) };
      return { ok: true, mode: 'live', round: n, r, api };
    }
    if (t < r.resultAt) return { ok: false, screen: Object.assign({ icon: '🕘', title: 'Challenge Mock ' + n + ' is over',
      body: resLine + ' From then this paper is open to everyone as a free mock.' }, back) };
    return { ok: true, mode: 'practice', round: n, r, api };
  }

  /* ── what a visitor should see right now ── */
  async function buildState() {
    const t = now(); const n = nextRound(t);
    const uid = currentUid();
    if (!hasRound(n)) {                       // the series is over: only the last result is left to show
      const p = D.lastRound; const pr = round(p);
      if (t > pr.resultAt + 6 * 24 * H) return null;
      const done = uid ? await participated(p, uid) : null;
      return { S, kind: t >= pr.resultAt ? 'result-final' : 'wait-final', n: p, r: pr, done, uid, t };
    }
    const r = round(n), reg = uid ? await regAt(uid) : 0;
    const prev = n > 1 ? round(n - 1) : null;
    const prevDone = (prev && uid) ? await participated(n - 1, uid) : null;
    const st = { S, n, r, uid, reg, prev, prevDone, t, nx: nextIn(n) };
    st.prevPhase = !prev ? '' : (t < prev.resultAt ? 'wait' : 'out');
    if (t >= r.start) {                       // challenge day, the window is open
      st.done = uid ? await participated(n, uid) : null;
      if (st.done) st.kind = 'submitted';
      else if (reg && reg < r.regClose) st.kind = (t <= r.lastEntry || startedAt(n, uid)) ? 'live' : 'missed';
      else st.kind = reg ? 'live-next' : 'live-closed';
    } else if (reg && reg < r.regClose) st.kind = 'registered';
    else if (reg) st.kind = 'registered-next';
    else st.kind = t < r.regClose ? 'open' : 'closed';
    /* the last round: there is no "next challenge" to offer */
    if (!st.nx && (st.kind === 'closed' || st.kind === 'registered-next' || st.kind === 'live-next' || st.kind === 'live-closed')) st.kind = 'last-closed';
    return st;
  }
  const waShare = n => 'https://wa.me/?text=' + encodeURIComponent(D.name + ' All India Challenge Mock ' + n + ' on TrickySSC — free, real exam pattern, All India rank. Register here: https://trickyssc.com' + D.page);

  const api = { def: D, key: D.key, round, hasRound, nextRound, testUrl, regAt, register, markStarted, startedAt, markDone,
    participated, resultUrl, hasLang, gate, buildState, waShare, words, fmtDay, now };
  const S = api;
  return api;
}

export const SERIES = { cgl: makeSeries(DEFS.cgl), chsl: makeSeries(DEFS.chsl) };
const ORDER = ['chsl', 'cgl'];
export const seriesByKey = k => SERIES[k] || SERIES.cgl;
export const isAicId = id => /^ssc-(cgl|chsl)_aic_mock\d+/i.test(String(id || ''));
export function seriesOfMock(id) { return /^ssc-chsl_/i.test(String(id || '')) ? SERIES.chsl : SERIES.cgl; }
export function roundOfMock(id) { const m = String(id || '').match(/_aic_mock(\d+)/i); return m ? parseInt(m[1], 10) : 0; }
/* the gate of whichever series the paper belongs to */
export function gate(uid, mockId) { return seriesOfMock(mockId).gate(uid, mockId); }
/* the names of the first release keep working and mean the CGL Tier 2 series */
export const CFG = DEFS.cgl;
export const round = SERIES.cgl.round, hasRound = SERIES.cgl.hasRound, nextRound = SERIES.cgl.nextRound, testUrl = SERIES.cgl.testUrl,
  regAt = SERIES.cgl.regAt, register = SERIES.cgl.register, markStarted = SERIES.cgl.markStarted, startedAt = SERIES.cgl.startedAt,
  markDone = SERIES.cgl.markDone, participated = SERIES.cgl.participated, resultUrl = SERIES.cgl.resultUrl, hasLang = SERIES.cgl.hasLang;

/* ───────────────────────── page widgets ─────────────────────────
   Any page can carry these empty holders; this file fills them. Add data-aic-series="chsl" for the CHSL series
   (without it a holder shows the CGL Tier 2 series):
     <div data-aic="hub"></div>      the big status card (challenge page)
     <div data-aic="papers"></div>   one card per paper: live date and time, unlocks by itself (challenge page)
     <div data-aic="past"></div>     finished rounds with leaderboard and free-mock links (challenge page)
     <tbody data-aic="schedule">     the coming rounds
     <span data-aic-count>           how many students have registered
     <div data-aic="banner"></div>   wide strip          <div data-aic="strip"></div>   slim strip
   and   <body data-aic-popup>  switches on the challenge pop-up (both series in one pop-up).     */
const CSS = `.aicB{font-family:'Hind',system-ui,sans-serif;box-sizing:border-box;border-radius:16px;color:#fff;position:relative;overflow:hidden;
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
.aicPap-list{display:grid;gap:14px}
.aicPap-row{display:flex;gap:18px;align-items:stretch;position:relative;z-index:1}
.aicPap-main{flex:1 1 auto;min-width:0}
.aicPap-side{flex:0 0 270px;display:flex;flex-direction:column;justify-content:center;gap:9px}
.aicPap-side .aicB-btn,.aicPap-side .aicB-ok{width:100%;justify-content:center;text-align:center}
.aicPap-side .aicB-btn{min-height:50px;font-size:1.08rem}
.aicPap-side .aicB-ok{min-height:46px;font-size:1rem}
.aicPap-side .aicB-btn.ghost{min-height:42px;font-size:.92rem}
.aicPap-side .aicPap-note{font-size:.8rem;color:#F5F3FF;text-align:center;line-height:1.4;margin:0}
@media(max-width:720px){.aicPap-row{flex-direction:column;gap:12px}.aicPap-side{flex:0 0 auto}}
.aicT-btn{box-sizing:border-box;display:inline-flex;align-items:center;justify-content:center;margin-top:6px;width:210px;max-width:100%;height:36px;padding:0 10px;border-radius:9px;font-family:'Rajdhani',sans-serif;font-weight:800;font-size:.9rem;text-decoration:none;white-space:nowrap;border:0;background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff!important;box-shadow:0 4px 12px rgba(255,107,0,.25)}
.aicT-btn.alt{background:linear-gradient(135deg,#6D28D9,#8B5CF6);box-shadow:0 4px 12px rgba(109,40,217,.25)}
.aicT-btn.off{filter:blur(1.4px) grayscale(.6);opacity:.55;pointer-events:none;box-shadow:none;user-select:none}
.aicT-btn.done{background:#DCFCE7;color:#15803D!important;box-shadow:none;pointer-events:none}
.aicT-cell small{display:block;font-size:.72rem;color:#64748B;margin-top:3px}
.aicPap{position:relative;overflow:hidden;border-radius:18px;padding:20px 20px 18px;color:#fff;background:linear-gradient(125deg,#1E1B4B 0%,#4C1D95 52%,#BE185D 100%);box-shadow:0 12px 30px rgba(76,29,149,.28);border:2px solid transparent}
.aicPap::after{content:'🏆';position:absolute;right:-6px;top:-14px;font-size:92px;opacity:.1;pointer-events:none}
.aicPap.live{background:linear-gradient(125deg,#7F1D1D 0%,#B91C1C 45%,#EA580C 100%);border-color:#FDE68A;box-shadow:0 14px 34px rgba(220,38,38,.35)}
.aicPap.wait{background:linear-gradient(125deg,#1E293B 0%,#334155 60%,#475569 100%);box-shadow:0 10px 24px rgba(15,23,42,.22)}
.aicPap.later{padding:15px 18px 14px;box-shadow:0 6px 16px rgba(76,29,149,.18)}
.aicPap-top{display:flex;align-items:center;gap:8px;flex-wrap:wrap;position:relative;z-index:1}
.aicPap-chip{display:inline-flex;align-items:center;gap:6px;border-radius:100px;padding:2px 11px;font-family:'Rajdhani',sans-serif;font-weight:800;font-size:.78rem;letter-spacing:.8px;text-transform:uppercase;background:#FDE68A;color:#4C1D95}
.aicPap.live .aicPap-chip{background:#fff;color:#B91C1C}
.aicPap.live .aicPap-chip i{width:8px;height:8px;border-radius:50%;background:#DC2626;animation:aicPulse 1.1s infinite}
@keyframes aicPulse{0%,100%{opacity:1}50%{opacity:.25}}
.aicPap-name{font-size:.86rem;font-weight:700;color:#E9D5FF;letter-spacing:.2px}
.aicPap-h{font-family:'Baloo 2','Rajdhani',sans-serif;font-weight:800;font-size:clamp(1.45rem,5.6vw,2rem);line-height:1.15;margin:8px 0 2px;position:relative;z-index:1}
.aicPap.later .aicPap-h{font-size:clamp(1.15rem,4.4vw,1.4rem)}
.aicPap-h em{font-style:normal;color:#FDE68A}
.aicPap-when{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:clamp(1.05rem,4.2vw,1.3rem);color:#fff;position:relative;z-index:1}
.aicPap .aicPap-line{font-size:.95rem;color:#F5F3FF!important;line-height:1.55;margin:10px 0 12px!important;position:relative;z-index:1}
.aicPap .aicPap-line b{color:#FDE68A!important}
.aicPap-btns{display:flex;flex-wrap:wrap;gap:9px;align-items:center;position:relative;z-index:1}
.aicPap-btns .aicB-btn{min-height:48px;font-size:1.08rem;padding:10px 22px}
.aicPap-btns .lock{display:inline-flex;align-items:center;min-height:44px;padding:8px 16px;border-radius:12px;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1rem;border:1.5px dashed rgba(255,255,255,.5);color:#fff;background:rgba(255,255,255,.1)}
.aicPap .aicB-cd{margin:10px 0 2px;position:relative;z-index:1}
.aicPap .aicB-cd span{min-width:58px;font-size:1.3rem;padding:6px 8px}
.aicPap .aicPap-cdl{font-size:.8rem;color:#F5F3FF!important;font-weight:600;margin:3px 0 0!important;position:relative;z-index:1}
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
#aicPop .aicDuo{padding:20px 16px 16px;text-align:center}
.aicDuo-h{font-family:'Baloo 2','Rajdhani',sans-serif;font-weight:800;font-size:clamp(1.15rem,4.6vw,1.45rem);line-height:1.2;margin:8px 0 2px;color:#fff;position:relative;z-index:1}
.aicDuo-h em{font-style:normal;color:#FDE68A}
.aicDuo-sub{font-size:.84rem;color:#DDD6FE;margin:0 0 12px;line-height:1.4;position:relative;z-index:1}
.aicDuo-list{display:grid;gap:10px;position:relative;z-index:1;text-align:left}
.aicC{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.22);border-radius:13px;padding:11px 12px}
.aicC-top{display:flex;align-items:center;justify-content:space-between;gap:8px}
.aicC-top b{font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1.12rem;color:#fff;letter-spacing:.2px}
.aicC-chip{flex:none;background:#FDE68A;color:#4C1D95;border-radius:100px;padding:1px 9px;font-family:'Rajdhani',sans-serif;font-weight:800;font-size:.72rem;letter-spacing:.5px;text-transform:uppercase}
.aicC-chip.live{background:#DC2626;color:#fff}
.aicC-when{font-size:.86rem;color:#fff;font-weight:600;margin-top:2px}
.aicC-line{font-size:.8rem;color:#E9D5FF;line-height:1.45;margin-top:3px}
.aicC-line b{color:#fff}
.aicC-line a{color:#FDE68A;font-weight:700}
.aicC-act{display:flex;flex-wrap:wrap;align-items:center;gap:7px;margin-top:9px}
.aicC-act .aicB-btn{min-height:38px;font-size:.95rem;padding:7px 14px;flex:1 1 auto}
.aicC-act .aicB-ok{min-height:36px;font-size:.9rem;flex:1 1 auto}
.aicC-act .aicC-more{flex:none;color:#DDD6FE;font-size:.8rem;font-weight:700;text-decoration:underline;padding:4px 2px}
.aicDuo-both{margin-top:12px;width:100%;position:relative;z-index:1}
.aicDuo-foot{font-size:.76rem;color:#DDD6FE;margin:10px 0 0;line-height:1.45;position:relative;z-index:1}
`;
function injectCss() { if (document.getElementById('aicCss')) return; const s = document.createElement('style'); s.id = 'aicCss'; s.textContent = CSS; document.head.appendChild(s); }

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
const regBtnHtml = (keys, label, cls) => '<button type="button" class="aicB-btn' + (cls ? ' ' + cls : '') + '" data-aic-register="' + keys + '">' + label + '</button>';

/* The full status card of ONE series (challenge page, single pop-up, banner, strip). */
function stateHtml(st, size) {
  if (!st) return '';
  const S = st.S, D = S.def, n = st.n, r = st.r, nx = st.nx, w = S.words(r);
  const title = D.name + ' <em>All India Challenge Mock ' + n + '</em>';
  const nextTitle = D.name + ' <em>All India Challenge Mock ' + (n + 1) + '</em>';
  const when = '<b>' + fmtDay(r.start) + '</b>, 9 am to 12 midnight';
  const more = size === 'big' ? '' : '<a class="aicB-btn ghost" href="' + D.page + '">How it works</a>';
  const regBtn = label => regBtnHtml(D.key, label) + '<div class="aicB-err" data-aic-err hidden></div>';
  const nxLine = nx ? 'Challenge Mock ' + (n + 1) + ' on ' + fmtDay(nx.start) : '';
  const freeOn = 'opens as a free mock on <b>' + fmtDay(r.resultAt) + ', 9 am</b>';
  /* line about the round that just finished */
  let prevLine = '';
  if (st.prev) {
    if (st.prevPhase === 'wait') prevLine = st.prevDone ? 'Your Challenge Mock ' + (n - 1) + ' is submitted. Result on <b>' + fmtDay(st.prev.resultAt) + ', 9 am</b>.' : '';
    else prevLine = 'Challenge Mock ' + (n - 1) + ' results are out. <a href="' + (st.prevDone ? S.resultUrl(n - 1, st.prevDone) : D.page + '#results') + '">' + (st.prevDone ? 'Check your result and rank' : 'See the leaderboard') + '</a>';
  }
  let tag = 'Free · Every ' + w.day, head = title, body = '', act = '', extra = '';
  switch (st.kind) {
    case 'open':
      tag = 'Free · Registration open';
      body = when + '. ' + D.pitch + ' Registration closes <b>' + w.regDay + ' midnight</b>.';
      act = regBtn('Register free →') + more; extra = cdHtml(r.regClose, 'Time left to register for this ' + w.day); break;
    case 'closed':
      tag = 'Registration closed for this ' + w.day;
      body = 'Challenge Mock ' + n + ' is on ' + when + ' for registered students. Register now and you are in from <b>' + nxLine + '</b>.';
      act = regBtn('Register for Mock ' + (n + 1) + ' →') + more; break;
    case 'registered':
      tag = 'You are registered';
      body = 'Your paper opens on ' + when + ' (last entry ' + w.last + '). One attempt. Result on <b>' + fmtDay(r.resultAt) + ', 9 am</b>.';
      act = '<span class="aicB-ok">✓ Registered for all ' + D.short + ' challenge mocks</span><a class="aicB-btn ghost" target="_blank" rel="noopener" href="' + S.waShare(n) + '">Invite friends on WhatsApp</a>';
      extra = cdHtml(r.start, 'Mock opens in'); break;
    case 'registered-next':
      tag = 'You are registered'; head = nextTitle;
      body = 'Registration for this ' + w.day + ' had closed, so your first paper is <b>' + nxLine + '</b>, 9 am to 12 midnight.';
      act = '<span class="aicB-ok">✓ Registered from Mock ' + (n + 1) + '</span>' + more; extra = cdHtml(nx.start, 'Your mock opens in'); break;
    case 'live':
      tag = '<i></i>Live now';
      body = 'The paper is open until <b>12 midnight</b> (last entry ' + w.last + '). ' + D.paperLine;
      act = '<a class="aicB-btn" href="' + S.testUrl(n, 'en') + '">Start in English →</a><a class="aicB-btn ghost" data-aic-hi="' + D.key + '" href="' + S.testUrl(n, 'hi') + '">हिंदी में शुरू करें</a>';
      extra = cdHtml(r.lastEntry, 'Last entry closes in'); break;
    case 'missed':
      tag = 'Entry closed at ' + w.last;
      body = 'This paper ' + freeOn + '.' + (nx ? ' You are already in for <b>' + nxLine + '</b>.' : '');
      act = (nx ? '<span class="aicB-ok">✓ Registered for Mock ' + (n + 1) + '</span>' : '') + more; break;
    case 'live-next':
      tag = 'You are registered'; head = nextTitle;
      body = 'Today\'s paper is for students who registered before ' + w.regDay + ' midnight. Your first paper is on <b>' + fmtDay(nx.start) + '</b>; today\'s ' + freeOn.replace(/<\/?b>/g, '') + '.';
      act = '<span class="aicB-ok">✓ Registered from Mock ' + (n + 1) + '</span>' + more; break;
    case 'live-closed':
      tag = '<i></i>Challenge Mock ' + n + ' is live';
      body = 'Today\'s paper is open only to students who registered before ' + w.regDay + ' midnight. Register now and you are in from <b>' + nxLine + '</b>.';
      act = regBtn('Register for Mock ' + (n + 1) + ' →') + more; break;
    case 'last-closed':
      tag = 'Final challenge of this series';
      body = 'Challenge Mock ' + n + ' on ' + when + ' is for students who registered before ' + w.regDay + ' midnight. It ' + freeOn + ' for everyone.';
      act = more; break;
    case 'submitted':
      tag = 'Submitted';
      body = 'Your test has been submitted successfully. Result, All India rank and solutions on <b>' + fmtDay(r.resultAt) + ', 9 am</b>.' + (nx ? ' You are already in for ' + nxLine + '.' : '');
      act = '<span class="aicB-ok">✓ Test submitted</span><a class="aicB-btn ghost" href="' + D.mocks + '">' + D.mocksLabel + '</a>';
      extra = cdHtml(r.resultAt, 'Result in'); break;
    case 'wait-final':
      body = st.done ? 'Your test has been submitted successfully. Result on <b>' + fmtDay(r.resultAt) + ', 9 am</b>.' : 'The last challenge is over. Results on <b>' + fmtDay(r.resultAt) + ', 9 am</b>.';
      act = more; break;
    case 'result-final':
      tag = 'Results out';
      body = 'Challenge Mock ' + n + ' results are out.';
      act = '<a class="aicB-btn" href="' + (st.done ? S.resultUrl(n, st.done) : D.page + '#results') + '">' + (st.done ? 'Check your result →' : 'See the leaderboard →') + '</a>'; break;
  }
  const note = (prevLine && st.kind !== 'wait-final' && st.kind !== 'result-final') ? '<p class="aicB-note">' + prevLine + '</p>' : '';
  return '<div class="aicB' + (size === 'slim' ? ' slim' : size === 'big' ? ' big' : '') + '"><div class="aicB-row"><div class="aicB-main">'
    + '<span class="aicB-tag">' + tag + '</span><div class="aicB-h">' + head + '</div><p class="aicB-p">' + body + '</p>' + extra + '</div>'
    + '<div class="aicB-act">' + act + '</div></div>' + note + '</div>';
}

/* The small card of one series inside the two-challenge pop-up. */
const CAN_REGISTER = { open: 1, closed: 1, 'live-closed': 1 };
function cardHtml(st) {
  const S = st.S, D = S.def, n = st.n, r = st.r, nx = st.nx, w = S.words(r);
  const shortDay = ms => fmtShort(ms);
  let chip = 'Mock ' + n, chipCls = '', when = shortDay(r.start) + ' · 9 am to 12 midnight', line = '', act = '';
  const more = '<a class="aicC-more" href="' + D.page + '">Details</a>';
  const reg = label => regBtnHtml(D.key, label);
  switch (st.kind) {
    case 'open':
      line = 'Free. Register by <b>' + w.regDay + ' midnight</b>.'; act = reg('Register for ' + D.short) + more; break;
    case 'closed':
      line = 'Registration for this ' + w.day + ' is closed. Register now for <b>Mock ' + (n + 1) + ' on ' + shortDay(nx.start) + '</b>.';
      act = reg('Register for ' + D.short) + more; break;
    case 'registered':
      line = 'You are in. Last entry ' + w.last + ', result ' + shortDay(r.resultAt) + ', 9 am.'; act = '<span class="aicB-ok">✓ Registered</span>' + more; break;
    case 'registered-next':
      chip = 'Mock ' + (n + 1); when = shortDay(nx.start) + ' · 9 am to 12 midnight';
      line = 'This ' + w.day + '\'s registration had closed, so this is your first paper.'; act = '<span class="aicB-ok">✓ Registered</span>' + more; break;
    case 'live':
      chip = 'Live now'; chipCls = ' live'; when = 'Open till 12 midnight · last entry ' + w.last; line = D.paperLine;
      act = '<a class="aicB-btn" href="' + S.testUrl(n, 'en') + '">Start in English →</a><a class="aicB-btn ghost" data-aic-hi="' + D.key + '" href="' + S.testUrl(n, 'hi') + '">हिंदी</a>'; break;
    case 'missed':
      line = 'Entry closed at ' + w.last + '. Free mock from ' + shortDay(r.resultAt) + ', 9 am.' + (nx ? ' You are in for Mock ' + (n + 1) + '.' : ''); act = more; break;
    case 'live-next':
      chip = 'Mock ' + (n + 1); when = shortDay(nx.start) + ' · 9 am to 12 midnight';
      line = 'Today\'s paper is for students who registered earlier. This is your first paper.'; act = '<span class="aicB-ok">✓ Registered</span>' + more; break;
    case 'live-closed':
      chip = 'Live now'; chipCls = ' live';
      line = 'Today\'s paper is for registered students. Register now for <b>Mock ' + (n + 1) + ' on ' + shortDay(nx.start) + '</b>.'; act = reg('Register for ' + D.short) + more; break;
    case 'last-closed':
      line = 'Final round, for registered students. Free mock for everyone from ' + shortDay(r.resultAt) + ', 9 am.'; act = more; break;
    case 'submitted':
      chip = 'Submitted'; line = 'Your test is submitted. Result and All India rank on <b>' + shortDay(r.resultAt) + ', 9 am</b>.'; act = '<span class="aicB-ok">✓ Test submitted</span>' + more; break;
    case 'wait-final':
      line = st.done ? 'Your test is submitted. Result on <b>' + shortDay(r.resultAt) + ', 9 am</b>.' : 'The last challenge is over. Results on <b>' + shortDay(r.resultAt) + ', 9 am</b>.'; act = more; break;
    case 'result-final':
      chip = 'Results out'; when = 'Challenge Mock ' + n; line = 'Results and the leaderboard are out.';
      act = '<a class="aicB-btn" href="' + (st.done ? S.resultUrl(n, st.done) : D.page + '#results') + '">' + (st.done ? 'Check your result →' : 'See the leaderboard →') + '</a>'; break;
  }
  if (st.prev && st.prevPhase === 'out' && st.kind !== 'result-final')
    line += ' <span style="display:block;margin-top:3px">Mock ' + (n - 1) + ' results are out: <a href="' + (st.prevDone ? S.resultUrl(n - 1, st.prevDone) : D.page + '#results') + '">' + (st.prevDone ? 'check your result and rank' : 'see the leaderboard') + '</a></span>';
  return '<div class="aicC" data-aic-card="' + D.key + '"><div class="aicC-top"><b>' + D.name + '</b><span class="aicC-chip' + chipCls + '">' + chip + '</span></div>'
    + '<div class="aicC-when">' + when + '</div><div class="aicC-line">' + line + '</div><div class="aicC-act">' + act + '</div></div>';
}
/* Both challenges in one pop-up: a card each, and "Register for both" while both can still be joined. */
function duoHtml(list) {
  const open = list.filter(st => CAN_REGISTER[st.kind]);
  const live = list.some(st => st.kind === 'live');
  return '<div class="aicB aicDuo"><span class="aicB-tag">' + (live ? '<i></i>Live today' : 'Free · every week') + '</span>'
    + '<div class="aicDuo-h">All India <em>Challenge Mocks</em></div>'
    + '<p class="aicDuo-sub">Real exam pattern, one live attempt, All India rank. Register for one or both.</p>'
    + '<div class="aicDuo-list">' + list.map(cardHtml).join('') + '</div>'
    + (open.length > 1 ? regBtnHtml(open.map(st => st.S.key).join(','), 'Register for both →', 'aicDuo-both') : '')
    + '<div class="aicB-err" data-aic-err hidden style="position:relative;z-index:1;margin-top:6px"></div>'
    + '<p class="aicDuo-foot">Registration is free and one time for each exam.</p></div>';
}

let _busy = false;
async function onRegisterClick(btn) {
  if (_busy) return; _busy = true;
  const keys = String(btn.getAttribute('data-aic-register') || '').split(',').filter(k => SERIES[k]);
  if (!keys.length) keys.push('cgl');
  const old = btn.innerHTML; btn.disabled = true; btn.innerHTML = 'Registering…';
  const scope = btn.closest('.aicB') || btn.parentNode;
  const err = scope.querySelector('[data-aic-err]');
  if (err) err.hidden = true;
  let res = { ok: true };
  try { for (const k of keys) { const x = await SERIES[k].register(); if (!x.ok) { res = x; break; } } }
  catch (e) { res = { ok: false, reason: 'write' }; }
  _busy = false;
  if (res.ok) { await render(); return; }
  btn.disabled = false; btn.innerHTML = old;
  if (err) { err.hidden = false; err.textContent = res.reason === 'login' ? 'Please log in to register.' : 'Could not register. Check your internet and tap again.'; }
  if (res.reason !== 'login') render();        // one of two may have gone through
}
function bindRegister(root) { root.querySelectorAll('[data-aic-register]').forEach(b => { if (!b.__aic) { b.__aic = 1; b.addEventListener('click', () => onRegisterClick(b)); } }); }
const holderSeries = el => seriesByKey(el.getAttribute('data-aic-series') || 'cgl');

async function paintPast(el) {
  const S = holderSeries(el), D = S.def;
  const t = now(); const last = S.nextRound(t) - 1; const rows = [];
  for (let n = Math.min(last, D.lastRound || last); n >= 1 && rows.length < 4; n--) if (t >= S.round(n).resultAt) rows.push(n);
  if (!rows.length) {
    el.innerHTML = '<div class="aicPast-empty">The first result comes out on <b>' + fmtDay(S.round(1).resultAt) + ' at 9 am</b>. The leaderboard, and the paper as a free mock, will appear here on their own.</div>';
    return;
  }
  const uid = currentUid();
  const cards = await Promise.all(rows.map(async (n, i) => {
    const r = S.round(n); let total = 0, top = [];
    const ck = 'tssc_aic_' + D.tag + 'past_' + n, cc = ssGet(ck, MIN10);
    if (cc) { total = cc.v.total; top = cc.v.top; }
    else {
      try { total = (await getCountFromServer(collection(db, 'leaderboards', r.board, 'scores'))).data().count || 0; } catch (e) {}
      if (i === 0) { try { const s = await getDocs(query(collection(db, 'leaderboards', r.board, 'scores'), orderBy('marks', 'desc'), limit(10))); s.forEach(d => { const x = d.data() || {}; top.push({ name: x.name, marks: x.marks, maxMarks: x.maxMarks }); }); } catch (e) {} }
      ssSet(ck, { total, top });
    }
    const hi = await S.hasLang(n, 'hi');
    const done = uid ? await S.participated(n, uid) : null;
    const lb = top.length ? '<table class="aicPast-lb">' + top.map((x, k) => '<tr><td>#' + (k + 1) + '</td><td>' + esc(String(x.name || 'Student').slice(0, 28)) + '</td><td>' + esc(x.marks) + (x.maxMarks ? ' / ' + esc(x.maxMarks) : '') + '</td></tr>').join('') + '</table>' : '';
    return '<div class="aicPast-card"><div class="aicPast-top"><h3>All India Challenge Mock ' + n + '</h3><span>' + fmtDate(r.start) + (total ? ' · ' + total.toLocaleString('en-IN') + ' students' : '') + '</span></div>' + lb
      + '<div class="aicPast-btns">' + (done ? '<a class="go" href="' + S.resultUrl(n, done) + '">My result and rank</a>' : '')
      + '<a href="/rank.html?paper=' + encodeURIComponent(r.board) + '&name=' + encodeURIComponent(D.name + ' All India Challenge Mock ' + n) + '">Full leaderboard</a>'
      + '<a' + (done ? '' : ' class="go"') + ' href="' + S.testUrl(n, 'en') + '">Attempt as free mock</a>' + (hi ? '<a href="' + S.testUrl(n, 'hi') + '">हिंदी में</a>' : '') + '</div></div>';
  }));
  el.innerHTML = '<div class="aicPast">' + cards.join('') + '</div>';
}

/* <div data-aic="papers"> — TSSC-AICPAPERS-V1 (2026-11-22): one card per challenge paper.
   The coming paper always has a card; a later paper gets its card as soon as it is uploaded. A card shows the
   date and time it goes live and unlocks by itself at that time (Start for registered students), then shows
   the result time. After the result the paper moves to the results block below. */
async function isUploaded(S, n) {
  const k = 'tssc_aic_' + S.def.tag + 'up_' + n; const c = ssGet(k, MIN5); if (c) return !!c.v;
  try { const x = await getDoc(doc(db, 'mock_tests', S.round(n).mockId('en'))); ssSet(k, x.exists() ? 1 : 0); return x.exists(); } catch (e) { return false; }
}
let _papTimer = 0;
async function paintPapers(el) {
  const S = holderSeries(el), D = S.def, t = now(), cur = S.nextRound(t), uid = currentUid();
  const list = [];
  if (cur > 1 && S.hasRound(cur - 1) && t < S.round(cur - 1).resultAt) list.push(cur - 1);
  for (let i = 0; i < 6 && S.hasRound(cur + i); i++) if (i === 0 || await isUploaded(S, cur + i)) list.push(cur + i);
  if (!list.length) { el.innerHTML = ''; el.hidden = true; return; }
  const reg = uid ? await S.regAt(uid) : 0;
  let nextFlip = 0;
  let firstUpcoming = true;
  const nx = n => S.hasRound(n + 1) ? S.round(n + 1) : null;
  /* the right-hand column: is this student in for this paper, and if not, the Register button */
  function side(n, r) {
    const w = S.words(r), inTime = reg && reg < r.regClose, n2 = nx(n);
    const invite = '<a class="aicB-btn ghost" target="_blank" rel="noopener" href="' + S.waShare(n) + '">Invite friends on WhatsApp</a>';
    if (inTime) return '<span class="aicB-ok">✓ You are registered</span><p class="aicPap-note">For all ' + D.short + ' challenge mocks</p>' + invite;
    if (reg) return '<span class="aicB-ok">✓ You are registered</span><p class="aicPap-note">' + (n2 ? 'Your first paper is Mock ' + (n + 1) + ' on ' + fmtShort(n2.start) : 'Registration for this paper had closed') + '</p>' + invite;
    if (t < r.regClose) return regBtnHtml(D.key, 'Register free →') + '<p class="aicPap-note">One time. Closes ' + w.regDay + ' midnight.</p><div class="aicB-err" data-aic-err hidden></div>';
    if (n2) return regBtnHtml(D.key, 'Register for Mock ' + (n + 1) + ' →') + '<p class="aicPap-note">Registration for this paper is closed.</p><div class="aicB-err" data-aic-err hidden></div>';
    return '<p class="aicPap-note">Registration for this paper is closed.</p>';
  }
  const cards = await Promise.all(list.map(async n => {
    const r = S.round(n), w = S.words(r);
    let chip, cls = '', head, when, line, lock = '', cd = '', sideHtml;
    if (t < r.start) {
      nextFlip = nextFlip ? Math.min(nextFlip, r.start) : r.start;
      const big = firstUpcoming; firstUpcoming = false; if (!big) cls = ' later';
      chip = 'Upcoming'; head = 'Live on <em>' + fmtDay(r.start) + '</em>'; when = '9 am to 12 midnight · last entry ' + w.last;
      line = (reg && reg < r.regClose) ? 'The Start button appears here at 9 am on ' + w.day + '.' : D.paperLine;
      lock = '<span class="lock">🔒 Opens ' + fmtShort(r.start) + ', 9 am</span>';
      if (big) cd = cdHtml(r.start) + '<p class="aicPap-cdl">Goes live in</p>';
      sideHtml = side(n, r);
    } else if (t < r.end) {
      nextFlip = nextFlip ? Math.min(nextFlip, r.end) : r.end;
      chip = '<i></i>Live now'; cls = ' live'; head = 'The paper is <em>live now</em>'; when = 'Open till 12 midnight · last entry ' + w.last;
      const done = uid ? await S.participated(n, uid) : null;
      if (done) { line = 'Your test has been submitted successfully. Result and All India rank on <b>' + fmtDay(r.resultAt) + ', 9 am</b>.'; sideHtml = '<span class="aicB-ok">✓ Test submitted</span>'; }
      else if (reg && reg < r.regClose) {
        line = D.paperLine + ' The test cannot be paused.';
        const hi = await S.hasLang(n, 'hi');
        sideHtml = '<a class="aicB-btn" href="' + S.testUrl(n, 'en') + '">Start in English →</a>' + (hi ? '<a class="aicB-btn ghost" href="' + S.testUrl(n, 'hi') + '">हिंदी में शुरू करें</a>' : '');
        if (t < r.lastEntry) cd = cdHtml(r.lastEntry) + '<p class="aicPap-cdl">Last entry closes in</p>';
      } else {
        line = 'Today\'s paper is for students who registered before ' + w.regDay + ' midnight. It opens for everyone as a free mock on <b>' + fmtDay(r.resultAt) + ', 9 am</b>.';
        lock = '<span class="lock">🔒 Registered students only</span>'; sideHtml = side(n, r);
      }
    } else {
      nextFlip = nextFlip ? Math.min(nextFlip, r.resultAt) : r.resultAt;
      chip = 'Paper over'; cls = ' wait'; head = 'Result on <em>' + fmtDay(r.resultAt) + '</em>'; when = '9 am · marks, All India rank and solutions';
      const done = uid ? await S.participated(n, uid) : null;
      line = (done ? 'Your test is submitted. ' : '') + 'The result opens by itself at 9 am. From then this paper is a free mock for everyone.';
      lock = '<span class="lock">🕘 Result ' + fmtShort(r.resultAt) + ', 9 am</span>';
      cd = cdHtml(r.resultAt) + '<p class="aicPap-cdl">Result in</p>';
      sideHtml = done ? '<span class="aicB-ok">✓ Test submitted</span>' : side(n, r);
    }
    return '<div class="aicB aicPap' + cls + '" style="margin:0"><div class="aicPap-row"><div class="aicPap-main">'
      + '<div class="aicPap-top"><span class="aicPap-chip">' + chip + '</span><span class="aicPap-name">' + D.name + ' · All India Challenge Mock ' + n + '</span></div>'
      + '<div class="aicPap-h">' + head + '</div><div class="aicPap-when">' + when + '</div>' + cd
      + '<p class="aicPap-line">' + line + '</p>' + (lock ? '<div class="aicPap-btns">' + lock + '</div>' : '') + '</div>'
      + '<div class="aicPap-side">' + sideHtml + '</div></div></div>';
  }));
  el.innerHTML = '<div class="aicPap-list">' + cards.join('') + '</div>'; el.hidden = false;
  bindRegister(el); tickCd();
  /* unlock by itself: paint again when the next card changes state */
  if (nextFlip && nextFlip - t < 20 * 24 * H) { clearTimeout(_papTimer); _papTimer = setTimeout(render, Math.max(1500, nextFlip - now() + 1500)); }
}

/* <tbody data-aic="schedule"> — the coming rounds (the rows typed in the page are only the no-JavaScript fallback) */
/* TSSC-AICTABLE-V1 (2026-11-22): every row carries its own buttons.
   Mock window: "Attempt test" — live for students registered in time; blurred for everyone else; after the paper
   it turns into "Attempt free test" from the result time. Result: "Check rank & leaderboard", blurred until 9 am. */
async function paintSchedule() {
  for (const el of document.querySelectorAll('[data-aic="schedule"]')) {
    const S = holderSeries(el), t = now(), cur = S.nextRound(t), uid = currentUid();
    const reg = uid ? await S.regAt(uid) : 0;
    const from = Math.max(1, cur - 3), rows = [];
    for (let n = from; rows.length < 8 && S.hasRound(n) && n < cur + 5; n++) {
      const r = S.round(n), live = t >= r.start && t < r.end;
      const done = (uid && t >= r.start) ? await S.participated(n, uid) : null;
      let win, res;
      if (t < r.start) win = '<span class="aicT-btn off" title="Opens ' + fmtShort(r.start) + ', 9 am">Attempt test</span><small>Opens ' + fmtShort(r.start) + ', 9 am</small>';
      else if (live) {
        if (done) win = '<span class="aicT-btn done">✓ Submitted</span>';
        else if (reg && reg < r.regClose) win = '<a class="aicT-btn" href="' + S.testUrl(n, 'en') + '">Attempt test →</a><small>Live now · last entry ' + S.words(r).last + '</small>';
        else win = '<span class="aicT-btn off">Attempt test</span><small>Registered students only · free mock from ' + fmtShort(r.resultAt) + '</small>';
      } else if (t < r.resultAt) win = done ? '<span class="aicT-btn done">✓ Submitted</span>' : '<span class="aicT-btn off">Attempt free test</span><small>Free test from ' + fmtShort(r.resultAt) + ', 9 am</small>';
      else win = '<a class="aicT-btn alt" href="' + S.testUrl(n, 'en') + '">Attempt free test →</a>';
      if (t < r.resultAt) res = '<span class="aicT-btn off">Check rank &amp; leaderboard</span>';
      else res = '<a class="aicT-btn" href="' + (done ? S.resultUrl(n, done) : '/rank.html?paper=' + encodeURIComponent(r.board) + '&name=' + encodeURIComponent(S.def.name + ' All India Challenge Mock ' + n)) + '">Check rank &amp; leaderboard →</a>';
      rows.push('<tr><td><b>Challenge Mock ' + n + '</b>' + (live ? ' <span style="color:#DC2626;font-weight:700;">· live now</span>' : '') + '</td>'
        + '<td>' + fmtShort(r.regClose - 60000) + ', 11:59 pm</td>'
        + '<td class="aicT-cell">' + fmtShort(r.start) + ', 9 am – 12 midnight<br>' + win + '</td>'
        + '<td class="aicT-cell">' + fmtShort(r.resultAt) + ', 9 am<br>' + res + '</td></tr>');
    }
    if (rows.length) el.innerHTML = rows.join('');
  }
}

async function paintCount() {
  const els = [...document.querySelectorAll('[data-aic-count]')]; if (!els.length) return;
  for (const key of Object.keys(SERIES)) {
    const mine = els.filter(el => holderSeries(el).key === key); if (!mine.length) continue;
    const D = SERIES[key].def, ck = 'tssc_aic_' + D.tag + 'count';
    try {
      const cc = ssGet(ck, MIN10);
      const c = cc ? cc.v : ((await getCountFromServer(collection(db, 'leaderboards', D.regBoard, 'scores'))).data().count || 0);
      if (!cc) ssSet(ck, c);
      mine.forEach(el => { if (c >= 50) { el.textContent = c.toLocaleString('en-IN') + ' students registered so far'; el.hidden = false; } else el.hidden = true; });
    } catch (e) {}
  }
}

let _rendering = null;
export function render() {
  if (_rendering) return _rendering;
  _rendering = (async () => {
    try {
      const holders = document.querySelectorAll('[data-aic="banner"],[data-aic="strip"],[data-aic="hub"]');
      injectCss();
      const wantPop = document.body.hasAttribute('data-aic-popup');
      const need = new Set(wantPop ? ORDER : []); holders.forEach(el => need.add(holderSeries(el).key));
      const states = {};
      await Promise.all([...need].map(async k => { states[k] = await SERIES[k].buildState(); }));
      holders.forEach(el => {
        const st = states[holderSeries(el).key];
        const size = el.getAttribute('data-aic') === 'strip' ? 'slim' : el.getAttribute('data-aic') === 'hub' ? 'big' : '';
        el.innerHTML = stateHtml(st, size); el.hidden = !st;
        bindRegister(el);
      });
      tickCd();
      Object.keys(states).forEach(k => { const st = states[k];
        if (st && st.kind === 'live') SERIES[k].hasLang(st.n, 'hi').then(ok => { if (!ok) document.querySelectorAll('[data-aic-hi="' + k + '"]').forEach(a => a.remove()); }); });
      document.querySelectorAll('[data-aic="past"]').forEach(el => paintPast(el).catch(() => {}));
      paintSchedule().catch(() => {});
      document.querySelectorAll('[data-aic="papers"]').forEach(el => paintPapers(el).catch(() => {}));
      paintCount();
      if (wantPop) maybePopup(ORDER.map(k => states[k]).filter(Boolean));
    } catch (e) { console.warn('[aic] render:', e); if (_authKnown && !_popDecided && document.body.hasAttribute('data-aic-popup')) { _popDecided = true; popSignal('none'); } }
    finally { _rendering = null; }
  })();
  return _rendering;
}

/* TSSC-AICPOP-V3 (2026-11-21) — the home page shows the challenges in a pop-up, and the plans pop-up opens only after
   this one is closed. One card per running series; "Register for both" while both can be joined.
   How often:
     - anyone who can still register for a series, or has a paper live right now   → once per browser session
     - everyone else (registered, submitted, waiting for a result)                 → once a day, and again when
       something changes (a result comes out, a paper goes live)
   window.__tsscAicPop = 'open' | 'closed' | 'none' and the event "tssc:aic-pop-done" tell the plans pop-up when to open. */
let _authKnown = false, _popDecided = false;
const istDay = () => new Date(now() + 19800000).toISOString().slice(0, 10);
function popSignal(v) { window.__tsscAicPop = v; if (v !== 'open') { try { window.dispatchEvent(new Event('tssc:aic-pop-done')); } catch (e) {} } }
function popClose() {
  const box = document.getElementById('aicPop'); if (box) box.remove();
  document.body.classList.remove('aic-pop-open'); popSignal('closed');
}
function popShell(inner) {
  let box = document.getElementById('aicPop');
  if (!box) {
    box = document.createElement('div'); box.id = 'aicPop'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'All India Challenge Mocks');
    box.addEventListener('click', e => { if (e.target === box) popClose(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && document.getElementById('aicPop')) popClose(); });
    document.body.appendChild(box);
  }
  box.innerHTML = '<div class="aicPop-box"><button type="button" class="aicPop-x" aria-label="Close">&times;</button>' + inner + '</div>';
  box.querySelector('.aicPop-x').addEventListener('click', popClose);
  bindRegister(box);
  document.body.classList.add('aic-pop-open');   /* the plans pop-up waits behind this one */
  tickCd();
  return box;
}
function resultsHtml(st) {
  const S = st.S, D = S.def, p = st.n - 1;
  const nextLine = st.reg ? 'You are already registered for <b>Challenge Mock ' + st.n + ' on ' + fmtDay(st.r.start) + '</b>.'
    : 'Next: <b>Challenge Mock ' + st.n + ' on ' + fmtDay(st.r.start) + '</b>. Register free before ' + S.words(st.r).regDay + ' midnight.';
  return '<div class="aicB"><div class="aicB-row"><div class="aicB-main">'
    + '<span class="aicB-tag">Results out</span><div class="aicB-h">' + D.name + ' Challenge Mock ' + p + ' <em>results are out</em></div>'
    + '<p class="aicB-p">' + (st.prevDone ? 'Your All India rank, percentile, topper comparison and full solutions are ready.' : 'See who topped, and attempt the paper as a free mock with full solutions.') + '</p>'
    + '<p class="aicB-p" style="margin-top:8px">' + nextLine + '</p></div><div class="aicB-act">'
    + '<a class="aicB-btn" href="' + (st.prevDone ? S.resultUrl(p, st.prevDone) : D.page + '#results') + '">' + (st.prevDone ? 'Check your result →' : 'See the leaderboard →') + '</a>'
    + (st.reg ? '' : regBtnHtml(D.key, 'Register for Challenge Mock ' + st.n, 'ghost') + '<div class="aicB-err" data-aic-err hidden></div>')
    + '</div></div></div>';
}
const resultsOut = st => !!(st.prev && st.prevPhase === 'out' && st.t < st.r.start);
function popHtml(list) {
  if (list.length > 1) return duoHtml(list);
  const st = list[0];
  return resultsOut(st) ? resultsHtml(st) : stateHtml(st, '');
}
function maybePopup(list) {
  /* an open pop-up follows the student's state (for example right after registering) */
  if (document.getElementById('aicPop')) { if (list.length) popShell(popHtml(list)); return; }
  if (_popDecided || !_authKnown) return;          // decide once per page load, and only when the login state is known
  _popDecided = true;
  if (!list.length) { popSignal('none'); return; }
  const day = istDay();
  /* a student who has joined at least one series is not shown the pop-up on every visit just because the other one is open */
  const anyReg = list.some(st => st.reg);
  const everyVisit = list.some(st => st.kind === 'live') || (!anyReg && list.some(st => CAN_REGISTER[st.kind]));
  const sig = day + ':' + list.map(st => st.S.key + '.' + st.kind + (resultsOut(st) ? '.out' : '')).join('|');
  const seenVisit = !!ssGet('tssc_aic_pop_s', 864e5), seenSig = lsGet('tssc_aic_pop_d') === sig;
  if (everyVisit ? seenVisit : seenSig) { popSignal('none'); return; }
  lsSet('tssc_aic_pop_d', sig); ssSet('tssc_aic_pop_s', 1);
  popSignal('open');
  popShell(popHtml(list));
}

/* Any element with data-aic-open opens the challenge pop-up (the "Challenge Mock" tab on the home page). */
export async function openPop() {
  injectCss();
  const list = [];
  for (const k of ORDER) { try { const st = await SERIES[k].buildState(); if (st) list.push(st); } catch (e) {} }
  if (!list.length) { location.href = CFG.page; return; }
  _popDecided = true; popSignal('open'); popShell(popHtml(list));
}
document.addEventListener('click', e => {
  const b = e.target.closest && e.target.closest('[data-aic-open]'); if (!b) return;
  e.preventDefault(); openPop();
});

/* ───────────────────────── start ───────────────────────── */
window.tsscAic = { SERIES, seriesByKey, seriesOfMock, CFG, round, nextRound, isAicId, roundOfMock, testUrl, now, syncClock, regAt, register, participated,
  markStarted, markDone, startedAt, resultUrl, gate, render, fmtDay, openPop };
function boot() {
  if (!document.querySelector('[data-aic]') && !document.body.hasAttribute('data-aic-popup')) return;
  syncClock().then(render);
  authReady.then(async () => { _authKnown = true; await render(); if (!_popDecided) await render(); });
  try { onAuthStateChanged(auth, () => render()); } catch (e) {}
  window.addEventListener('tssc:login', () => render());
  setInterval(tickCd, 1000);
  /* ?register=cgl | chsl | cgl,chsl  (or the old ?register=1) — a student sent to log in from a Register button comes back here and is registered */
  try {
    const q = new URLSearchParams(location.search).get('register');
    if (q) authReady.then(async () => {
      if (!auth.currentUser) return;
      const hub = document.querySelector('[data-aic="hub"],[data-aic="papers"]');
      const keys = q === '1' ? [hub ? holderSeries(hub).key : 'cgl'] : q.split(',').filter(k => SERIES[k]);
      for (const k of keys) await SERIES[k].register();
      render();
    });
  } catch (e) {}
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
