/* TSSC-QFIT-V1 — inside the app, a question and its options fit one phone screen.

   Loaded by tssc-app.js on the test screens (mock-test*, test*, chapterwise-test, pyq-chapter-test).
   The engines are not edited: this only adds a class to #testScreen and lets CSS do the rest.

   How it works
     - always: the four action buttons sit on one row, and spacing is trimmed
     - after every question is drawn, it checks whether the question panel still scrolls. If it
       does, it steps the text and spacing down (levels 1 to 3, never below 12px) and stops at the
       first level that fits. A figure is capped to the height that is left.
     - a question that is still too long at the smallest level (a long passage) scrolls as before.
   Fail-open: any error leaves the test screen exactly as the engine drew it. */
(function () {
  'use strict';
  if (window.__tsscQfit) return; window.__tsscQfit = 1;
  var LEVELS = 3;
  var css =
    '@media(max-width:820px){' +
    /* level 0: on for every question */
    '#testScreen.tsq .qNum-row{padding:5px 12px 0!important;margin-bottom:4px!important;}' +
    '#testScreen.tsq .q-card{margin:0 10px 7px!important;padding:11px 13px!important;}' +
    '#testScreen.tsq .qText{line-height:1.55!important;}' +
    '#testScreen.tsq .options-wrap{padding:0 10px!important;gap:6px!important;}' +
    '#testScreen.tsq .option{padding:9px 12px!important;}' +
    '#testScreen.tsq .opt-body{line-height:1.45!important;}' +
    '#testScreen.tsq .report-link{font-size:11px!important;padding:1px 2px!important;}' +
    '#testScreen.tsq .options-wrap+div{margin:2px 10px 0!important;line-height:1!important;}' +
    '#testScreen.tsq #qImg{max-width:100%;height:auto;object-fit:contain;}' +
    /* one row of actions: Prev, Clear, Mark, Next */
    '#testScreen.tsq .nav-btns{flex-wrap:wrap!important;gap:6px!important;padding:7px 10px calc(7px + env(safe-area-inset-bottom,0px))!important;margin-top:6px!important;}' +
    '#testScreen.tsq .nav-btns>.btn-prev{order:1;flex:1 1 0!important;}' +
    '#testScreen.tsq .nav-btns>.skip-btn-row{order:2;flex:2 1 0!important;display:flex!important;gap:6px!important;}' +
    '#testScreen.tsq .nav-btns>.btn-next,#testScreen.tsq .nav-btns>.btn-submit{order:3;flex:1 1 0!important;}' +
    '#testScreen.tsq .nav-btns>.btn-section{order:4;flex:1 1 100%!important;padding:7px 0!important;font-size:12.5px!important;}' +
    '#testScreen.tsq .nav-btns .btn{padding:10px 0!important;font-size:13px!important;min-width:0;white-space:nowrap;}' +
    '#testScreen.tsq .skip-btn-row>.btn{flex:1 1 0!important;}' +
    /* level 1 */
    '#testScreen.tsq-1 .qText,#testScreen.tsq-1 .q-sentence{font-size:14px!important;line-height:1.45!important;}' +
    '#testScreen.tsq-1 .q-instruction{font-size:13px!important;margin-bottom:6px!important;}' +
    '#testScreen.tsq-1 .opt-body,#testScreen.tsq-1 .option{font-size:13.5px!important;}' +
    '#testScreen.tsq-1 .q-card{padding:9px 12px!important;margin-bottom:6px!important;}' +
    '#testScreen.tsq-1 .option{padding:7px 11px!important;}' +
    '#testScreen.tsq-1 .opt-label{width:27px!important;height:27px!important;min-width:27px!important;font-size:12px!important;}' +
    /* level 2 */
    '#testScreen.tsq-2 .qText,#testScreen.tsq-2 .q-sentence{font-size:13px!important;line-height:1.4!important;}' +
    '#testScreen.tsq-2 .q-instruction{font-size:12.5px!important;margin-bottom:4px!important;}' +
    '#testScreen.tsq-2 .q-sentence{padding:6px 10px!important;}' +
    '#testScreen.tsq-2 .opt-body,#testScreen.tsq-2 .option{font-size:12.5px!important;line-height:1.35!important;}' +
    '#testScreen.tsq-2 .q-card{padding:8px 11px!important;margin:0 8px 5px!important;}' +
    '#testScreen.tsq-2 .options-wrap{gap:5px!important;padding:0 8px!important;}' +
    '#testScreen.tsq-2 .option{padding:6px 10px!important;gap:8px!important;}' +
    '#testScreen.tsq-2 .opt-label{width:24px!important;height:24px!important;min-width:24px!important;font-size:11.5px!important;}' +
    '#testScreen.tsq-2 .qNum-row{padding-top:3px!important;margin-bottom:3px!important;}' +
    /* level 3: smallest text, and short options two to a row */
    '#testScreen.tsq-3 .qText,#testScreen.tsq-3 .q-sentence{font-size:12px!important;line-height:1.35!important;}' +
    '#testScreen.tsq-3 .q-instruction{font-size:12px!important;}' +
    '#testScreen.tsq-3 .opt-body,#testScreen.tsq-3 .option{font-size:12px!important;line-height:1.3!important;}' +
    '#testScreen.tsq-3 .option{padding:5px 9px!important;}' +
    '#testScreen.tsq-3 .nav-btns .btn{padding:8px 0!important;}' +
    '#testScreen.tsq-grid .options-wrap{display:grid!important;grid-template-columns:minmax(0,1fr) minmax(0,1fr);}' +
    '#testScreen.tsq-grid .opt-img-box img{max-height:84px!important;}' +
    '}';
  var st = document.createElement('style'); st.id = 'tssc-qfit-css'; st.textContent = css;
  (document.head || document.documentElement).appendChild(st);

  var ts, panel, busy = false, queued = false;
  function fits() { return panel.scrollHeight <= panel.clientHeight + 1; }
  function setLevel(n) {
    for (var i = 1; i <= LEVELS; i++) ts.classList.toggle('tsq-' + i, i <= n);
  }
  function shortOptions() {
    var o = ts.querySelectorAll('#options .option'); if (o.length < 2 || o.length > 5) return false;
    for (var i = 0; i < o.length; i++) {
      var t = (o[i].querySelector('.opt-body') || o[i]).textContent.replace(/\s+/g, ' ').trim();
      if (t.length > 22) return false;
    }
    return true;
  }
  function fit() {
    queued = false;
    if (!ts || ts.style.display === 'none' || window.innerWidth > 820) return;
    busy = true;
    try {
      var img = document.getElementById('qImg');
      if (img) img.style.maxHeight = '';
      ts.classList.remove('tsq-grid'); setLevel(0);
      if (!fits()) {
        var n = 0;
        while (n < LEVELS && !fits()) { n++; setLevel(n); }
        if (!fits() && shortOptions()) { ts.classList.add('tsq-grid'); }
        /* a figure takes what is left, down to a size that can still be read */
        if (!fits() && img && img.offsetHeight > 0) {
          var over = panel.scrollHeight - panel.clientHeight, h = img.offsetHeight - over;
          if (h >= 110) img.style.maxHeight = h + 'px';
        }
      }
      panel.scrollTop = 0;
    } catch (e) {}
    setTimeout(function () { busy = false; }, 0);
  }
  function ask() { if (queued) return; queued = true; (window.requestAnimationFrame || setTimeout)(fit); }
  function start() {
    ts = document.getElementById('testScreen'); panel = ts && ts.querySelector('.questionPanel');
    var q = document.getElementById('qText'), o = document.getElementById('options');
    if (!ts || !panel || !q || !o || !window.MutationObserver) return;
    ts.classList.add('tsq');
    var mo = new MutationObserver(function () { if (!busy) ask(); });
    mo.observe(q, { childList: true, subtree: true, characterData: true });
    mo.observe(o, { childList: true, subtree: true, characterData: true });
    var wrap = document.getElementById('qImgWrap'); if (wrap) mo.observe(wrap, { attributes: true, attributeFilter: ['style'] });
    new MutationObserver(ask).observe(ts, { attributes: true, attributeFilter: ['style'] });
    ts.addEventListener('load', function (e) { if (e.target && e.target.tagName === 'IMG') ask(); }, true);
    window.addEventListener('resize', ask);
    ask();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
