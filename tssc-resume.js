/* ============================================================================
   TSSC-RESUME-V1 (2026-11-14) — resume a test that was dropped mid-way.

   If a student loses a test half-way (network fault, page error, browser or
   phone closed, wrong tap, battery), opening the SAME test again offers:
       "Resume test"  -> same question, same answers, same time left
       "Start again"  -> a clean attempt from Question 1

   How it works
   - Every test engine hands its live state to this file through a small
     window.__tsscResumeAdapter block (answers, marked questions, current
     question, section clocks).
   - While a test is running the state is saved on this device (localStorage)
     every 2 seconds and again the moment the page is hidden or closed.
   - The save is removed as soon as the test is submitted.
   - Saved progress is kept for 72 hours, per login and per test.

   Nothing here touches the paywall, login, daily limit count or Firestore:
   zero reads, zero writes. If this file fails to load, tests run as before.
   ========================================================================== */
(function () {
  'use strict';
  var PFX = 'tssc_resume_v1:';
  var KEEP_MS = 72 * 60 * 60 * 1000;   // how long a dropped test stays resumable
  var SAVE_EVERY_MS = 2000;

  var offered = false;     // the resume question was shown (or is no longer needed) on this page load
  var dialogOpen = false;
  var sawRun = false;      // the test was actually running on this page load
  var lastSnap = '';

  function ad() { return window.__tsscResumeAdapter || null; }
  function call(fn, dflt) { try { return fn(); } catch (e) { return dflt; } }
  function shown(id) { var e = document.getElementById(id); return !!(e && e.getClientRects().length); }

  function testId(a) {
    var own = call(a.id, '');
    if (own) return own;
    // Same test = same page + same query, ignoring params that do not identify the paper.
    var drop = /^(review|v|ref|fbclid|gclid|utm_[a-z]+)$/i, keep = [];
    try {
      new URLSearchParams(location.search).forEach(function (val, k) { if (!drop.test(k)) keep.push(k + '=' + val); });
    } catch (e) {}
    keep.sort();
    return location.pathname + '?' + keep.join('&');
  }
  function keyFor(a) {
    var uid = call(a.uid, '');
    return uid ? (PFX + uid + ':' + testId(a)) : '';
  }

  function phase(a) {
    if (!a || call(a.review, false)) return 'off';
    if (!(call(a.count, 0) > 0)) return 'off';
    if (call(a.busy, false) || shown('resultScreen')) return 'done';
    if (shown('instrScreen')) return 'instr';
    if (shown('testScreen')) return 'run';
    return 'off';
  }

  function readSaved(key, a) {
    try {
      var o = JSON.parse(localStorage.getItem(key) || 'null');
      if (!o || o.v !== 1 || !o.s) return null;
      if (Date.now() - (o.t || 0) > KEEP_MS) return null;
      if (o.n !== call(a.count, 0)) return null;           // the paper changed since it was saved
      return o;
    } catch (e) { return null; }
  }
  function drop(key) { try { if (key) localStorage.removeItem(key); } catch (e) {} lastSnap = ''; }

  function save() {
    var a = ad(); if (!a || dialogOpen) return;
    var ph = phase(a), key = keyFor(a);
    if (!key) return;
    // Submitted: the save has done its job. (A result screen restored by the Back button, with
    // no test run on this page load, is left alone.)
    if (ph === 'done') { if (sawRun || call(a.busy, false)) drop(key); return; }
    if (ph !== 'run') return;
    sawRun = true; offered = true;
    try {
      var snap = JSON.stringify(a.snap());
      if (snap === lastSnap) return;
      localStorage.setItem(key, JSON.stringify({ v: 1, t: Date.now(), n: call(a.count, 0), s: JSON.parse(snap) }));
      lastSnap = snap;
    } catch (e) { /* storage full or blocked — the test simply continues without a save */ }
  }

  function sweep() {   // remove saves older than KEEP_MS so storage never fills up
    try {
      for (var i = localStorage.length - 1; i >= 0; i--) {
        var k = localStorage.key(i);
        if (!k || k.indexOf(PFX) !== 0) continue;
        var o = null; try { o = JSON.parse(localStorage.getItem(k)); } catch (e) {}
        if (!o || Date.now() - (o.t || 0) > KEEP_MS) localStorage.removeItem(k);
      }
    } catch (e) {}
  }

  function mmss(t) { t = Math.max(0, parseInt(t, 10) || 0); var m = Math.floor(t / 60), s = t % 60; return (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s; }
  function ago(ms) {
    var m = Math.round(ms / 60000);
    if (m < 1) return 'just now';
    if (m < 60) return m + ' min ago';
    var h = Math.round(m / 60);
    return h < 24 ? (h + ' hour' + (h > 1 ? 's' : '') + ' ago') : (Math.round(h / 24) + ' day' + (Math.round(h / 24) > 1 ? 's' : '') + ' ago');
  }

  function offer(a, key, saved) {
    dialogOpen = true; offered = true;
    var s = saved.s, total = saved.n;
    var answered = 0; for (var k in (s.a || {})) { if (s.a[k]) answered++; }
    var qNo = Math.min(total, (parseInt(s.q, 10) || 0) + 1);
    var timeLine = '';
    if (Array.isArray(s.tr)) timeLine = mmss(s.tr[s.ts || 0]) + ' left' + (s.tr.length > 1 ? ' in this section' : '');
    else if (s.tm) timeLine = mmss(s.tl) + ' left';

    var bg = document.createElement('div');
    bg.id = 'tsscResumeBg';
    bg.setAttribute('style', 'position:fixed;inset:0;z-index:2147483000;background:rgba(15,23,42,.72);display:flex;align-items:center;justify-content:center;padding:16px;font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;');
    bg.innerHTML =
      '<div role="dialog" aria-modal="true" aria-labelledby="tsscResumeTitle" style="background:#fff;border-radius:18px;max-width:400px;width:100%;padding:24px 22px 20px;box-shadow:0 24px 60px rgba(0,0,0,.35);text-align:center;">'
      + '<div style="font-size:2.2rem;line-height:1;margin-bottom:8px;">⏯️</div>'
      + '<div id="tsscResumeTitle" style="font-family:Rajdhani,Inter,sans-serif;font-weight:700;font-size:1.45rem;color:#0F172A;margin-bottom:6px;">Continue your test?</div>'
      + '<div style="font-size:.92rem;color:#475569;line-height:1.5;margin-bottom:14px;">You left this test unfinished ' + ago(Date.now() - saved.t) + '. Your answers and time are saved.</div>'
      + '<div style="background:#FFF7ED;border:1px solid #FED7AA;border-radius:12px;padding:10px 12px;font-size:.9rem;color:#9A3412;font-weight:600;line-height:1.6;margin-bottom:16px;">'
      + 'Question ' + qNo + ' of ' + total + ' &nbsp;·&nbsp; ' + answered + ' answered' + (timeLine ? '<br>⏱ ' + timeLine : '')
      + '</div>'
      + '<button type="button" id="tsscResumeYes" style="display:block;width:100%;border:0;border-radius:12px;background:#FF6B00;color:#fff;font-family:Rajdhani,Inter,sans-serif;font-weight:700;font-size:1.1rem;padding:12px;cursor:pointer;margin-bottom:9px;">▶ Resume test</button>'
      + '<button type="button" id="tsscResumeNo" style="display:block;width:100%;border:1.5px solid #CBD5E1;border-radius:12px;background:#fff;color:#334155;font-family:Rajdhani,Inter,sans-serif;font-weight:700;font-size:1rem;padding:10px;cursor:pointer;">Start again from Question 1</button>'
      + '</div>';
    document.body.appendChild(bg);
    function close() { dialogOpen = false; if (bg.parentNode) bg.parentNode.removeChild(bg); }

    document.getElementById('tsscResumeYes').onclick = function () {
      var ok = false;
      try { ok = a.restore(s) !== false; } catch (e) { console.warn('[tssc-resume] restore failed:', e); ok = false; }
      if (ok) sawRun = true;
      close();
      if (!ok) { drop(key); alert('Sorry, the saved progress could not be restored. Please start the test again.'); }
    };
    document.getElementById('tsscResumeNo').onclick = function () { drop(key); close(); };
  }

  function watch() {
    var a = ad(); if (!a) return;
    if (!offered && !dialogOpen && phase(a) === 'instr') {
      var key = keyFor(a);
      if (key) {
        var saved = readSaved(key, a);
        if (saved) offer(a, key, saved);
      }
    }
    if (phase(a) === 'run') { offered = true; sawRun = true; }   // the test is under way — nothing left to offer
  }

  sweep();
  setInterval(watch, 400);
  setInterval(save, SAVE_EVERY_MS);
  window.addEventListener('pagehide', save);
  window.addEventListener('beforeunload', save);
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') save(); });
})();
