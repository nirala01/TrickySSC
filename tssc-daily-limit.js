/* ===================== TSSC-DAILYLIMIT-V1 =====================
   Daily test limit for every test engine (PYQ, subject-wise PYQ, chapter
   tests, mocks): FREE users 20 tests per day, PAID users 80 per day.
   The day is the IST calendar day and resets at midnight IST.

   - A test is COUNTED when it is submitted (not when it is opened), so a
     test left half-way or a refresh never uses up the limit.
   - The limit is CHECKED when the student presses "I am ready to begin".
   - PAID = any active grant in entitlements/{uid} (allAccess or any module:
     CGL mocks, CHSL mocks, combo, dashboard ...).
   - Admins (nirala01@gmail.com, ashish@trickyssc.com, *@trickyssc.com) are
     never limited and never counted.
   - The count lives on the student's own users/{uid} doc as
     dailyTests = { d: 'YYYY-MM-DD', n: <tests submitted that day> }
     and is mirrored in localStorage. No Firestore rules change.
   - FAIL-OPEN everywhere: if anything here errors, is slow (>4 s) or this
     file is missing, the engine starts the test exactly as before.

   To change the limits, edit the two numbers below — nothing else.
================================================================ */
import { getApps } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getFirestore, doc, getDoc, setDoc } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

export const FREE_LIMIT = 20;
export const PAID_LIMIT = 80;

const ADMINS = ['nirala01@gmail.com', 'ashish@trickyssc.com'];
const CHECK_TIMEOUT_MS = 4000;

function today() {                                   // IST calendar day
  return new Date(Date.now() + 19800000).toISOString().slice(0, 10);
}
function app() { const a = getApps(); return a && a.length ? a[0] : null; }
function db() { const a = app(); return a ? getFirestore(a) : null; }

function userEmail() {
  try { const a = app(); const u = a && getAuth(a).currentUser; if (u && u.email) return u.email; } catch (e) {}
  try { const c = JSON.parse(localStorage.getItem('tssc_user') || 'null'); return (c && c.email) || ''; } catch (e) { return ''; }
}
function isAdmin() {
  const e = String(userEmail() || '').toLowerCase();
  return !!e && (ADMINS.includes(e) || /@trickyssc\.com$/.test(e));
}

function localUsed(uid) {
  try { const o = JSON.parse(localStorage.getItem('tssc_dl_' + uid) || 'null'); return (o && o.d === today()) ? (parseInt(o.n, 10) || 0) : 0; }
  catch (e) { return 0; }
}
function localSet(uid, n) {
  try { localStorage.setItem('tssc_dl_' + uid, JSON.stringify({ d: today(), n })); } catch (e) {}
}

async function serverUsed(uid) {
  const d = db(); if (!d) return 0;
  const s = await getDoc(doc(d, 'users', uid));
  const t = s.exists() ? (s.data() || {}).dailyTests : null;
  return (t && t.d === today()) ? (parseInt(t.n, 10) || 0) : 0;
}

function grantActive(g) {
  if (!g || g.active !== true) return false;
  const e = g.expiresAt; if (!e) return true;
  const ms = e.toDate ? e.toDate().getTime() : (e.seconds ? e.seconds * 1000 : Date.parse(e));
  return !isFinite(ms) || ms > Date.now();
}
async function isPaid(uid) {
  const key = 'tssc_dl_paid_' + uid;
  try { const c = JSON.parse(sessionStorage.getItem(key) || 'null'); if (c && Date.now() - (c.ts || 0) < 600000) return !!c.paid; } catch (e) {}
  const d = db(); if (!d) return true;
  try {
    const s = await getDoc(doc(d, 'entitlements', uid));
    const x = s.exists() ? (s.data() || {}) : {};
    const paid = grantActive(x.allAccess) || Object.values(x.modules || {}).some(grantActive);
    try { sessionStorage.setItem(key, JSON.stringify({ paid, ts: Date.now() })); } catch (e) {}
    return paid;
  } catch (e) { return true; }                       // could not check → give the higher limit
}

/* Returns { used, limit, paid } — never throws. */
export async function tdlStatus(uid) {
  let used = localUsed(uid);
  try { used = Math.max(used, await serverUsed(uid)); } catch (e) {}
  const paid = await isPaid(uid);
  return { used, limit: paid ? PAID_LIMIT : FREE_LIMIT, paid };
}

/* Resolves true = start the test, false = blocked (the notice is shown). */
export async function tdlGate(uid) {
  try {
    if (!uid || isAdmin()) return true;
    const st = await Promise.race([
      tdlStatus(uid),
      new Promise(r => setTimeout(() => r(null), CHECK_TIMEOUT_MS))
    ]);
    if (!st || st.used < st.limit) return true;
    showBlocked(st);
    return false;
  } catch (e) { return true; }
}

/* Called once per real submit (never in review replay). Best-effort. */
export async function tdlCount(uid) {
  try {
    if (!uid || isAdmin()) return;
    let used = localUsed(uid);
    try { used = Math.max(used, await serverUsed(uid)); } catch (e) {}
    const n = used + 1;
    localSet(uid, n);
    const d = db(); if (!d) return;
    await setDoc(doc(d, 'users', uid), { dailyTests: { d: today(), n } }, { merge: true });
  } catch (e) { /* swallowed — the local mirror still counts */ }
}

function showBlocked(st) {
  if (document.getElementById('tdlOverlay')) { document.getElementById('tdlOverlay').style.display = 'flex'; return; }
  const o = document.createElement('div');
  o.id = 'tdlOverlay';
  o.setAttribute('role', 'dialog');
  o.style.cssText = 'position:fixed;inset:0;z-index:2147483000;background:rgba(15,23,42,.72);display:flex;align-items:center;justify-content:center;padding:16px;font-family:inherit;';
  const upsell = st.paid ? '' :
    '<a href="mock-list.html" style="display:block;margin-top:14px;padding:12px 16px;border-radius:10px;background:linear-gradient(135deg,#F97316,#EA580C);color:#fff;font-weight:700;text-decoration:none;">⭐ Go Premium — ' + PAID_LIMIT + ' tests a day</a>';
  o.innerHTML =
    '<div style="background:#fff;color:#0F172A;max-width:400px;width:100%;border-radius:16px;padding:24px 22px;text-align:center;box-shadow:0 20px 50px rgba(0,0,0,.35);">' +
      '<div style="font-size:40px;line-height:1;">⏳</div>' +
      '<div style="font-size:19px;font-weight:800;margin-top:10px;">Daily test limit reached</div>' +
      '<div style="font-size:14.5px;color:#475569;margin-top:10px;line-height:1.55;">You have submitted <b>' + st.used + '</b> tests today. ' +
        (st.paid ? 'Premium' : 'Free') + ' accounts can take up to <b>' + st.limit + '</b> tests a day.<br>Your limit resets at <b>midnight</b>.</div>' +
      upsell +
      '<button type="button" id="tdlBack" style="margin-top:12px;width:100%;padding:11px 16px;border-radius:10px;border:1px solid #CBD5E1;background:#F8FAFC;color:#0F172A;font-weight:600;font-size:14px;cursor:pointer;">← Go back</button>' +
    '</div>';
  document.body.appendChild(o);
  document.getElementById('tdlBack').onclick = () => {
    if (history.length > 1) history.back(); else location.href = 'dashboard.html';
  };
}
