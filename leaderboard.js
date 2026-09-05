// leaderboard.js — shared leaderboard score recorder for TrickySSC
// Usage from a test page (ES module):
//   import { recordScore } from './leaderboard.js';
//   recordScore({ uid, displayName, paperId, paperName, marks, maxMarks, accuracy });
// It writes the candidate's BEST score for a paper to:
//   leaderboards/{paperId}/scores/{uid}
// The display name is taken from the user's profile (users/{uid}.name) — the
// same name they set while logging in — falling back to displayName, then 'Student'.

import { getApps, getApp, initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getFirestore, initializeFirestore, doc, getDoc, runTransaction, serverTimestamp }
  from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

const FB_CONFIG = {
  apiKey: "AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA",
  authDomain: "trickyssc-17bb3.firebaseapp.com",
  projectId: "trickyssc-17bb3",
  storageBucket: "trickyssc-17bb3.firebasestorage.app",
  messagingSenderId: "450627057220",
  appId: "1:450627057220:web:366267bf437d94f20c6e11"
};

// Reuse the app the test page already initialised; otherwise create one.
const app = getApps().length ? getApp() : initializeApp(FB_CONFIG);
// leaderboard.js loads (via import) BEFORE the test page's own init, so it is
// usually the FIRST to touch Firestore. Initialise with long-polling auto-detect
// here so flaky networks don't stall on the WebChannel stream. The test pages
// request the SAME options, so their later call just reuses this instance.
let db;
try { db = initializeFirestore(app, { experimentalAutoDetectLongPolling: true }); }
catch(_) { db = getFirestore(app); }   // already initialised — reuse it

// Resolve the candidate's login name from their profile document.
async function resolveName(uid, fallback) {
  let name = (fallback || '').trim();
  try {
    const snap = await getDoc(doc(db, 'users', uid));
    if (snap.exists()) {
      const ud = snap.data();
      name = (ud.name || ud.displayName || name || '').trim();
    }
  } catch (_) { /* ignore — fall back below */ }
  return name || 'Student';
}

/**
 * Record (upsert) the candidate's BEST score for a paper onto the leaderboard.
 * Never throws — leaderboard writes must not block the test result flow.
 */
export async function recordScore(o) {
  try {
    if (!o || !o.uid || !o.paperId) return;
    const paperId  = String(o.paperId).trim();
    const uid      = String(o.uid);
    const marks    = Number(o.marks) || 0;
    const maxMarks = Number(o.maxMarks) || 0;
    const accuracy = (o.accuracy != null && !isNaN(o.accuracy)) ? Number(o.accuracy) : null;
    if (!paperId) return;
    // TSSC-ANSWERS-V1: per-subject marks (for section rank on the dashboard)
    // and time used. Only numbers are kept; anything odd is dropped silently.
    const subjectMarks = {};
    if (o.subjectMarks && typeof o.subjectMarks === 'object') {
      for (const k of Object.keys(o.subjectMarks)) {
        const v = Number(o.subjectMarks[k]);
        if (k && !isNaN(v)) subjectMarks[String(k).slice(0, 40)] = v;
      }
    }
    const timeUsed = (o.timeUsed != null && !isNaN(o.timeUsed)) ? Math.max(0, Math.round(Number(o.timeUsed))) : null;

    const name = await resolveName(uid, o.displayName);
    const ref  = doc(db, 'leaderboards', paperId, 'scores', uid);

    await runTransaction(db, async (tx) => {
      const cur = await tx.get(ref);
      const prevMarks = cur.exists() ? (Number(cur.data().marks) || 0) : -Infinity;
      if (!cur.exists() || marks > prevMarks) {
        // New personal best (or first attempt) → store the full row.
        tx.set(ref, {
          uid, name, paperId,
          paperName: (o.paperName || (cur.exists() ? cur.data().paperName : '') || '').trim(),
          marks, maxMarks, accuracy,
          subjectMarks, timeUsed,                       // TSSC-ANSWERS-V1
          submittedAt: serverTimestamp()
        });
      } else if (cur.exists() && cur.data().name !== name && name !== 'Student') {
        // Score not beaten, but keep the displayed name fresh.
        tx.set(ref, { name }, { merge: true });
      }
    });
  } catch (e) {
    console.warn('[leaderboard] recordScore failed (ignored):', e);
  }
}
