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

/* TSSC-RESULT2-V1 — inside the app the result comes in two screens.
     1. Result: marks, the four counts, dashboard and rank buttons, rating. Fits one screen.
     2. Answers and solutions: opened by the bold button; scrolls as before.
   The engine still draws everything; this only shows one half at a time. Fail-open. */
(function () {
  'use strict';
  if (window.__tsscRes2) return; window.__tsscRes2 = 1;
  var css =
    '@media(max-width:820px){' +
    '#resultScreen.tsr-sum{position:fixed!important;inset:0!important;z-index:5;display:flex!important;flex-direction:column;justify-content:center;gap:10px;box-sizing:border-box;max-width:none!important;margin:0!important;' +
      'padding:calc(10px + env(safe-area-inset-top,0px)) 12px calc(10px + env(safe-area-inset-bottom,0px))!important;background:#F0F4F8;overflow:hidden;}' +
    '#resultScreen.tsr-sum.tsr-4{overflow-y:auto;justify-content:flex-start;}' +
    /* level 3: no room for the rating here, so it waits at the end of the solutions screen */
    '#resultScreen.tsr-sum.tsr-3>.rate-card{display:none!important;}' +
    '#resultScreen.tsr-sol.tsr-rate{display:flex!important;flex-direction:column;}' +
    '#resultScreen.tsr-sol.tsr-rate>.rate-card{display:block!important;order:9;margin:14px 0 20px!important;}' +
    '#resultScreen.tsr-sum>*{flex:0 0 auto;margin:0!important;}' +
    '#resultScreen.tsr-sum>#review{display:none!important;}' +
    '#resultScreen.tsr-sum>.result-card{padding:16px 14px!important;}' +
    '#resultScreen.tsr-sum #resultExamName{font-size:19px!important;margin-bottom:8px!important;line-height:1.15;}' +
    '#resultScreen.tsr-sum .result-verdict{margin-top:10px!important;}' +
    '#resultScreen.tsr-sum .stats{margin-top:14px!important;gap:7px!important;flex-wrap:nowrap!important;}' +
    '#resultScreen.tsr-sum .stat{padding:9px 4px!important;min-width:0!important;flex:1 1 0!important;}' +
    '#resultScreen.tsr-sum .gz-row{margin-top:14px!important;gap:8px!important;}' +
    '#resultScreen.tsr-sum .gz-row>#goDashboardBtn,#resultScreen.tsr-sum .gz-row>#viewRankBtn{white-space:normal!important;line-height:1.2!important;font-size:13px!important;padding:10px 8px!important;overflow:visible!important;}' +
    '#resultScreen.tsr-sum #saveStatus{margin-top:7px!important;}' +
    '#resultScreen.tsr-sum .rate-card{padding:12px 14px!important;text-align:center;}' +
    '#resultScreen.tsr-sum .rate-card h3{font-size:16px!important;}' +
    '#resultScreen.tsr-sum .rate-card .rc-sub{margin-bottom:6px!important;}' +
    '#resultScreen.tsr-sum .rc-stars{margin-bottom:8px!important;}' +
    '#resultScreen.tsr-sum .rc-star{font-size:30px!important;}' +
    '#resultScreen.tsr-sum .rc-diff{gap:6px!important;margin-bottom:10px!important;}' +
    '#resultScreen.tsr-sum .rc-chip{padding:6px 12px!important;font-size:12.5px!important;}' +
    '#resultScreen.tsr-sum .rc-submit{padding:9px 24px!important;}' +
    /* level 1 and 2: tighter, then the rating loses its small print */
    '#resultScreen.tsr-sum.tsr-1 .score-big{font-size:44px!important;}' +
    '#resultScreen.tsr-sum.tsr-1 .stat-val{font-size:22px!important;}' +
    '#resultScreen.tsr-sum.tsr-1>.result-card{padding:12px 12px!important;}' +
    '#resultScreen.tsr-sum.tsr-1 .stats,#resultScreen.tsr-sum.tsr-1 .gz-row{margin-top:10px!important;}' +
    '#resultScreen.tsr-sum.tsr-1{gap:8px;}' +
    '#resultScreen.tsr-sum.tsr-2 .rate-card .rc-sub{display:none!important;}' +
    '#resultScreen.tsr-sum.tsr-2 .rc-star{font-size:26px!important;}' +
    '#resultScreen.tsr-sum.tsr-2 .rate-card h3{display:inline-block;margin:0 0 4px!important;}' +
    '#resultScreen.tsr-sum.tsr-2 .rc-stars{margin-bottom:6px!important;}' +
    '#resultScreen.tsr-sum.tsr-2 .rc-diff{flex-wrap:nowrap!important;gap:4px!important;margin-bottom:8px!important;}' +
    '#resultScreen.tsr-sum.tsr-2 .rc-chip{padding:5px 8px!important;font-size:11.5px!important;white-space:nowrap;}' +
    '#resultScreen.tsr-sum.tsr-2 #resultExamName{font-size:17px!important;margin-bottom:5px!important;}' +
    '#resultScreen.tsr-sum.tsr-2 .stat-lbl span{display:none!important;}' +
    '#resultScreen.tsr-sum.tsr-2 .stat-lbl br{display:none!important;}' +
    /* the bold way in to the second screen */
    '.tsr-cta{display:none;align-items:center;justify-content:center;gap:10px;width:100%;min-height:56px;box-sizing:border-box;border:0;border-radius:16px;padding:10px 14px;cursor:pointer;' +
      'background:linear-gradient(135deg,#0B3B8C,#1D4ED8);color:#fff;font:700 19px/1.15 Rajdhani,system-ui,sans-serif;letter-spacing:.01em;box-shadow:0 8px 20px rgba(29,78,216,.32);}' +
    '.tsr-cta small{display:block;font:500 11.5px/1.2 system-ui,sans-serif;opacity:.9;margin-top:2px;letter-spacing:0;}' +
    '.tsr-cta i{font-style:normal;font-size:22px;}.tsr-cta u{text-decoration:none;font-size:22px;margin-left:auto;}' +
    '.tsr-cta span{text-align:left;}' +
    '#resultScreen.tsr-sum>.tsr-cta{display:flex;}' +
    '#resultScreen.tsr-sum.tsr-1>.tsr-cta{min-height:50px;font-size:18px;padding:8px 12px;}' +
    '#resultScreen.tsr-sum.tsr-2>.tsr-cta small{display:none;}' +
    /* second screen: every section tab fits the width, nothing slides sideways */
    '#resultScreen.tsr-sol{overflow-x:clip;}' +
    '#resultScreen.tsr-sol .rv-tabs{top:50px!important;}' +
    '#resultScreen.tsr-sol .rv-tabs{overflow:visible!important;gap:5px!important;flex-wrap:nowrap!important;}' +
    '#resultScreen.tsr-sol .rv-tab{flex:1 1 0!important;min-width:0!important;padding:6px 3px!important;gap:3px!important;}' +
    '#resultScreen.tsr-sol .rv-tab-name{white-space:normal!important;font-size:11.5px!important;line-height:1.15!important;text-align:center;overflow-wrap:anywhere;}' +
    '#resultScreen.tsr-sol .rv-tab-mini{gap:4px!important;font-size:9.5px!important;flex-wrap:wrap;justify-content:center;}' +
    '#resultScreen.tsr-sol .rv-tab-mini span{gap:2px!important;}' +
    '#resultScreen.tsr-sol .rv-tab-mini span::before{width:6px!important;height:6px!important;}' +
    /* one by one: the questions kept off-screen take no height, so the page ends where the open question ends */
    '#resultScreen .rv-wrap[data-rvpm="page"] .rv-items>.review-item.rvp-off{height:0!important;min-height:0!important;padding:0!important;border:0!important;overflow:hidden!important;}' +
    /* second screen */
    '#resultScreen.tsr-sol>*{display:none!important;}' +
    '#resultScreen.tsr-sol>#review{display:block!important;}' +
    '#resultScreen.tsr-sol>.tsr-bar{display:flex!important;}' +
    '#resultScreen.tsr-sol{padding-top:0!important;}' +
    '.tsr-bar{display:none;position:sticky;top:0;z-index:30;align-items:center;gap:6px;height:50px;margin:0 -12px 10px;padding:0 8px;background:#fff;border-bottom:1px solid #E2E8F0;box-shadow:0 1px 6px rgba(15,23,42,.05);' +
      'font:700 18px/1 Rajdhani,system-ui,sans-serif;color:#1A202C;}' +
    '.tsr-bar button{flex:0 0 auto;display:flex;align-items:center;gap:4px;height:36px;padding:0 12px 0 8px;border:0;border-radius:10px;background:#F1F5F9;color:#0B3B8C;font:700 14px/1 Rajdhani,system-ui,sans-serif;cursor:pointer;}' +
    '.tsr-bar b{flex:1;min-width:0;text-align:center;padding-right:70px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}' +
    '}';
  var st = document.createElement('style'); st.id = 'tssc-res2-css'; st.textContent = css;
  (document.head || document.documentElement).appendChild(st);

  var rs, cta, bar, mode = '', wasShown = false;
  function shown() { return rs.style.display && rs.style.display !== 'none'; }
  function small() { return window.innerWidth <= 820; }
  function fitSum() {
    if (mode !== 'sum') return;
    rs.classList.remove('tsr-1', 'tsr-2', 'tsr-3', 'tsr-4');
    var lv = ['tsr-1', 'tsr-2', 'tsr-3', 'tsr-4'];
    for (var i = 0; i < lv.length && rs.scrollHeight > rs.clientHeight + 1; i++) rs.classList.add(lv[i]);
    rs.classList.toggle('tsr-rate', rs.classList.contains('tsr-3'));
    rs.scrollTop = 0;
  }
  function set(m) {
    mode = m;
    rs.classList.toggle('tsr-sum', m === 'sum'); rs.classList.toggle('tsr-sol', m === 'sol');
    if (m !== 'sum') rs.classList.remove('tsr-1', 'tsr-2', 'tsr-3', 'tsr-4');
    try { window.scrollTo(0, 0); } catch (e) {}
    if (m === 'sum') { fitSum(); setTimeout(fitSum, 400); setTimeout(fitSum, 1500); }
  }
  function openSol() {
    if (mode === 'sol') return;
    try { history.pushState({ tsrSol: 1 }, ''); } catch (e) {}
    set('sol');
  }
  function sync() {
    if (!small()) { if (mode) set(''); return; }
    var on = shown();
    if (on && !wasShown) set('sum');
    if (!on && wasShown) set('');
    wasShown = on;
  }
  function start() {
    rs = document.getElementById('resultScreen'); var review = document.getElementById('review');
    if (!rs || !review || review.parentNode !== rs || !window.MutationObserver) return;
    cta = document.createElement('button'); cta.type = 'button'; cta.className = 'tsr-cta';
    cta.innerHTML = '<i>📝</i><span>Check answers &amp; solutions<small>Every question with the correct answer and explanation</small></span><u>→</u>';
    cta.addEventListener('click', openSol);
    var card = rs.querySelector('.result-card');
    rs.insertBefore(cta, card ? card.nextSibling : rs.firstChild);
    bar = document.createElement('div'); bar.className = 'tsr-bar';
    bar.innerHTML = '<button type="button">‹ Result</button><b>Answers &amp; solutions</b>';
    bar.querySelector('button').addEventListener('click', function () { try { history.back(); } catch (e) { set('sum'); } });
    rs.insertBefore(bar, rs.firstChild);
    window.addEventListener('popstate', function () { if (mode === 'sol') set('sum'); });
    new MutationObserver(sync).observe(rs, { attributes: true, attributeFilter: ['style'] });
    /* buttons and the rank card fill in after saving: fit again when they do */
    new MutationObserver(function () { if (mode === 'sum') fitSum(); }).observe(rs, { childList: true, subtree: true, attributes: true, attributeFilter: ['style', 'disabled'] });
    window.addEventListener('resize', function () { sync(); fitSum(); });
    sync();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
