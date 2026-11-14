/* ============================================================================
   tssc-app.js — TrickySSC "app mode" for the inner pages           TSSC-APP-V1
   ----------------------------------------------------------------------------
   Does NOTHING in a normal browser. It switches on only when the page is opened
   inside the Android app (or an installed home-screen app), and then:

     • hides the website header, mobile menu, breadcrumb and footer
     • puts a slim app bar at the top:  ‹ back · page title · home
     • keeps the same five bottom tabs as the app home (/app.html)

   The test screens (test*.html, mock-test*.html) are left exactly as they are.

   No page needs editing: the service worker (/sw.js) adds this script to every
   page it serves. You can also include it by hand anywhere:
       <script src="/tssc-app.js"></script>

   Try it in Chrome without the app:  add  ?app=1  to any page (that tab stays in
   app mode);  ?app=0  switches it off again.
   ========================================================================== */
(function () {
  'use strict';
  if (window.__tsscApp) return;
  window.__tsscApp = 1;

  var ss = null;
  try { ss = window.sessionStorage; } catch (e) {}
  var qs = location.search || '';
  if (/[?&]app=0\b/.test(qs)) { try { ss.removeItem('tssc_app'); } catch (e) {} return; }

  var on = false;
  try {
    on = (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) ||
         /^android-app:/.test(document.referrer || '') ||
         /[?&]app=1\b/.test(qs) ||
         !!(ss && ss.getItem('tssc_app') === '1');
  } catch (e) {}
  if (!on) return;
  try { ss.setItem('tssc_app', '1'); } catch (e) {}

  var path = location.pathname;
  var file = path.split('/').pop() || 'index.html';
  if (file === 'app.html' || file === 'offline.html') return;
  /* the website homepage is replaced by the app home */
  if ((path === '/' || path === '/index.html') && !location.hash) { location.replace('/app.html'); return; }
  /* TSSC-APPPAGES-V1: these list pages have an app-only copy (app-<page>.html, built by
     build_app_pages.py). Inside the app, any link to the website page lands on the copy. */
  var APP_COPY = ' login mock-list rrb-ntpc-gk-mock-test rrb-ntpc-gk-previous-year-questions rrb-ntpc-maths-mock-test rrb-ntpc-maths-previous-year-questions rrb-ntpc-mock-test rrb-ntpc-pyq rrb-ntpc-reasoning-mock-test rrb-ntpc-reasoning-previous-year-questions ssc-cgl-computer-mock-test ssc-cgl-english-mock-test ssc-cgl-english-previous-year-questions ssc-cgl-gk-mock-test ssc-cgl-gk-previous-year-questions ssc-cgl-mock-test ssc-cgl-pyq ssc-cgl-quant-mock-test ssc-cgl-quant-previous-year-questions ssc-cgl-reasoning-mock-test ssc-cgl-reasoning-previous-year-questions ssc-cgl-tier-2-english-mock-test ssc-cgl-tier-2-english-previous-year-questions ssc-cgl-tier-2-gk-mock-test ssc-cgl-tier-2-gk-previous-year-questions ssc-cgl-tier-2-mock-test ssc-cgl-tier-2-pyq ssc-cgl-tier-2-quant-mock-test ssc-cgl-tier-2-quant-previous-year-questions ssc-cgl-tier-2-reasoning-mock-test ssc-cgl-tier-2-reasoning-previous-year-questions ssc-chsl-english-mock-test ssc-chsl-english-previous-year-questions ssc-chsl-gk-mock-test ssc-chsl-gk-previous-year-questions ssc-chsl-mock-test ssc-chsl-pyq ssc-chsl-quant-mock-test ssc-chsl-quant-previous-year-questions ssc-chsl-reasoning-mock-test ssc-chsl-reasoning-previous-year-questions ssc-chsl-tier-2-computer-mock-test ssc-chsl-tier-2-computer-previous-year-questions ssc-chsl-tier-2-english-mock-test ssc-chsl-tier-2-english-previous-year-questions ssc-chsl-tier-2-gk-mock-test ssc-chsl-tier-2-gk-previous-year-questions ssc-chsl-tier-2-mock-test ssc-chsl-tier-2-quant-mock-test ssc-chsl-tier-2-quant-previous-year-questions ssc-chsl-tier-2-reasoning-mock-test ssc-chsl-tier-2-reasoning-previous-year-questions ssc-gd-english-mock-test ssc-gd-english-previous-year-questions ssc-gd-gk-mock-test ssc-gd-gk-previous-year-questions ssc-gd-maths-mock-test ssc-gd-maths-previous-year-questions ssc-gd-mock-test ssc-gd-pyq ssc-gd-reasoning-mock-test ssc-gd-reasoning-previous-year-questions ssc-mts-english-mock-test ssc-mts-gk-mock-test ssc-mts-maths-mock-test ssc-mts-mock-test ssc-mts-reasoning-mock-test ssc-pyq-chapterwise ';
  if (/\.html$/.test(file) && APP_COPY.indexOf(' ' + file.slice(0, -5) + ' ') >= 0) {
    location.replace('/app-' + file + location.search + location.hash);
    return;
  }
  /* the website's exam hub pages are replaced by the app's own course page */
  var HUB = { 'ssc-cgl.html': 'cgl', 'ssc-chsl.html': 'chsl', 'ssc-mts.html': 'mts', 'ssc-gd.html': 'gd', 'rrb-ntpc.html': 'ntpc' };
  if (HUB[file] && !location.hash) { location.replace('/app.html#c/' + HUB[file]); return; }
  /* test engines and admin tools: untouched */
  if (/^(test|mock-test|ai-test)[a-z0-9-]*\.html$/.test(file)) return;
  if (/^(admin|batch-uploader|uploader|upload_|question-|solution-|image-question|trickyssc-figure|figure-checker|content-admin|ca-admin|chapter-tag-admin|reports-admin|mock-inspector|quality-check|json-to|pdf-to|hindi-translator|en-diag|clipboard|loader|candidates)/.test(file)) return;

  /* pages where the bottom tabs would get in the way (a test is running, or login) */
  var NO_TABS = /^(chapterwise-test|pyq-chapter-test|login|rank)\.html$/.test(file);

  var TAB = 58, BAR = 52;
  var root = document.documentElement;
  root.classList.add('tssc-app');
  root.setAttribute('data-tsa-file', file.replace(/\.html$/, ''));
  if (!NO_TABS) root.classList.add('tssc-app-tabs');

  /* ---------- styles (added at once, so the website header never flashes) ---------- */
  var css =
    /* known site chrome: kept in layout until measured, then removed (see build) */
    'html.tssc-app nav.tssc-nav,html.tssc-app nav.topbar,html.tssc-app nav.nav,html.tssc-app nav.site-nav,html.tssc-app header.nav,html.tssc-app body>nav:first-of-type{visibility:hidden!important;}' +
    'html.tssc-app .tsa-gone,html.tssc-app .mobile-menu,html.tssc-app .tssc-mobile-menu,html.tssc-app footer,html.tssc-app .crumb,html.tssc-app .breadcrumb,html.tssc-app nav.crumbs,' +
    'html.tssc-app [id$="seo-content"],html.tssc-app .pyq-seo-index{display:none!important;}' +
    /* list pages: go straight to the tests. The page title is already in the app bar, and the long
       introductions are written for search visitors, not for someone already inside the app. */
    'html.tssc-app .wrap>.hero,html.tssc-app .wrap>.tier-intro,html.tssc-app .wrap>.tier-bars,html.tssc-app .mock-list-block>h2,html.tssc-app .mock-list-block>.mlb-sub,' +
    'html.tssc-app .mock-list-block>.mock-explain,html.tssc-app section.seo-content,' +
    'html.tssc-app nav.topbar+div>div:first-child,html.tssc-app nav.topbar+div>div:nth-child(3)>p,' +
    'html.tssc-app #pane-t1~div[style^="margin-top:2"],html.tssc-app #pane-t1~div[style^="margin-top:1.8rem"]{display:none!important;}' +
    /* TSSC-APPTRIM-V1: every page inside the app shows what you can tap, not what was written for
       search visitors. Reading sections are removed; study sections become one-line rows (see sheets). */
    'html.tssc-app body>header.hero,html.tssc-app .wrap>header.hero,' +
    ['intro','marks','how','why','plan','compare','hindi','faq','more','weightage','syllabus','strategy','about','related','all-chapters','format','notes-cta','about-mocks']
      .map(function (id) { return 'html.tssc-app section#' + id; }).join(',') + '{display:none!important;}' +
    /* kept sections: no headings or introductions, the app bar already names the page */
    'html.tssc-app section#subjects>h2,html.tssc-app section#subjects>p,html.tssc-app section#chapters>h2,html.tssc-app section#chapters>p,' +
    'html.tssc-app section#tests>h2,html.tssc-app section#tests>p,html.tssc-app #chNote,html.tssc-app .types-card,html.tssc-app .subj-nav,html.tssc-app .ch-ex,' +
    'html.tssc-app details.faq,html.tssc-app section.seo,html.tssc-app body>section.hero,html.tssc-app .feat-wrap+main .inside,html.tssc-app .feat-wrap+main .ctas,' +
    'html.tssc-app .masthead,html.tssc-app .intro-block,html.tssc-app .exam-grid .soon,html.tssc-app .exam-grid~.info,' +
    'html.tssc-app .sc.soon,html.tssc-app .sc-facts,html.tssc-app .sc-desc,html.tssc-app .sc-sub,html.tssc-app #subjects .tier-label{display:none!important;}' +
    /* chapter-test home: one row per subject */
    'html.tssc-app .sc-stat:nth-child(n+3),html.tssc-app [data-tg-join],html.tssc-app body>header.site-head,html.tssc-app header.mast,html.tssc-app body>.foot,html.tssc-app body>header.bar{display:none!important;}html.tssc-app .feat-wrap{margin-top:14px!important;}' +
    'html.tssc-app .subj-grid{display:grid!important;grid-template-columns:1fr!important;gap:9px!important;margin:0!important;}' +
    'html.tssc-app .sc{position:relative!important;display:flex!important;flex-direction:row!important;flex-wrap:wrap;align-items:center;gap:0 12px;padding:11px 12px!important;border:1px solid #E2E8F0!important;border-left:5px solid var(--c)!important;border-radius:14px!important;box-shadow:0 1px 6px rgba(0,0,0,.04)!important;transform:none!important;overflow:hidden;}' +
    'html.tssc-app .sc::before,html.tssc-app .sc::after{display:none!important;}' +
    'html.tssc-app .sc-top{display:contents!important;}' +
    'html.tssc-app .sc-ic{width:42px!important;height:42px!important;border-radius:12px!important;font-size:21px!important;flex:0 0 42px;grid-row:span 2;align-self:center;margin:0!important;}' +
    'html.tssc-app .sc-top>div:not(.sc-ic){flex:1 1 0;min-width:0;}' +
    'html.tssc-app .sc-name{font-size:16px!important;line-height:1.2!important;margin:0 0 17px!important;}' +
    'html.tssc-app .sc-live{position:absolute!important;left:71px;bottom:9px;display:block!important;padding:0!important;margin:0!important;background:none!important;border:0!important;white-space:nowrap;min-height:0!important;}' +
    'html.tssc-app .sc-live::before,html.tssc-app .sc-live::after,html.tssc-app .sc-stat::before,html.tssc-app .sc-stat b::before{display:none!important;}' +
    'html.tssc-app .sc-stat{display:inline!important;padding:0!important;margin:0!important;}' +
    'html.tssc-app .sc-stat b,html.tssc-app .sc-stat span{display:inline!important;font-family:Hind,system-ui,sans-serif!important;font-size:12px!important;font-weight:500!important;letter-spacing:0!important;text-transform:none!important;color:#718096!important;line-height:1.2!important;}' +
    'html.tssc-app .sc-stat b{font-weight:700!important;color:var(--c2)!important;}html.tssc-app .sc-stat span{margin-left:.22em;}' +
    'html.tssc-app .sc-stat+.sc-stat::before{content:"\\00b7"!important;display:inline!important;color:#A0AEC0;margin:0 .3em;position:static!important;width:auto!important;height:auto!important;background:none!important;}' +
    'html.tssc-app .sc-btn{flex:0 0 30px;width:30px;height:30px;padding:0!important;margin:0!important;border-radius:50%!important;background:var(--csoft)!important;color:var(--c2)!important;font-size:0!important;box-shadow:none!important;display:flex!important;align-items:center;justify-content:center;position:static!important;}' +
    'html.tssc-app .sc-btn em{font-size:16px;font-style:normal;font-weight:700;transform:none!important;}' +
    'html.tssc-app .sc-btn::after{content:"";position:absolute;inset:0;z-index:2;}' +
    /* study sections on a chapter page: one-line rows that open in a bottom sheet */
    '.tsa-rows{display:flex;flex-direction:column;gap:8px;margin:14px 0 4px;}' +
    '.tsa-row{display:flex;align-items:center;gap:10px;width:100%;box-sizing:border-box;padding:13px 14px;border:1px solid #E2E8F0;border-radius:14px;background:#fff;font:700 15px/1.25 Rajdhani,system-ui,sans-serif;color:#1A202C;text-align:left;cursor:pointer;box-shadow:0 1px 6px rgba(0,0,0,.04);}' +
    '.tsa-row span{flex:1;min-width:0;}.tsa-row svg{flex:0 0 18px;width:18px;height:18px;color:#94A3B8;}' +
    '.tsa-sheet{position:fixed;inset:0;z-index:1200;display:none;align-items:flex-end;background:rgba(15,23,42,.5);}.tsa-sheet.on{display:flex;}' +
    '.tsa-sheet-card{width:100%;max-height:88vh;box-sizing:border-box;display:flex;flex-direction:column;background:#fff;border-radius:18px 18px 0 0;padding-bottom:env(safe-area-inset-bottom,0px);}' +
    '.tsa-sheet-h{flex:0 0 auto;display:flex;align-items:center;gap:8px;padding:14px 12px 10px 16px;border-bottom:1px solid #EDF0F5;font:700 17px/1.2 Rajdhani,system-ui,sans-serif;color:#1A202C;}' +
    '.tsa-sheet-h b{flex:1;min-width:0;}.tsa-sheet-h button{flex:0 0 34px;width:34px;height:34px;border:0;border-radius:50%;background:#F1F5F9;font-size:15px;color:#475569;cursor:pointer;}' +
    '.tsa-sheet-b{flex:1 1 auto;overflow-y:auto;-webkit-overflow-scrolling:touch;padding:6px 16px 18px;}' +
    '.tsa-sheet-b>section{display:block!important;margin:0!important;padding:0!important;border:0!important;box-shadow:none!important;background:none!important;}.tsa-sheet-b>section>h2:first-child{display:none!important;}' +
    'html.tsa-lock,html.tsa-lock body{overflow:hidden!important;}' +
    'html.tssc-app .wrap{padding-top:12px!important;}' +
    'html.tssc-app{-webkit-tap-highlight-color:transparent;}' +
    'html.tssc-app-tabs body{padding-bottom:calc(' + TAB + 'px + env(safe-area-inset-bottom,0px))!important;}' +
    'html.tssc-app-tabs .tgf{bottom:calc(' + (TAB + 14) + 'px + env(safe-area-inset-bottom,0px))!important;}' +
    /* top bar */
    '.tsa-top{top:0;left:0;right:0;z-index:1000;display:flex;align-items:center;gap:4px;box-sizing:border-box;height:calc(' + BAR + 'px + env(safe-area-inset-top,0px));' +
      'padding:env(safe-area-inset-top,0px) 6px 0;background:#fff;border-bottom:1px solid #EDF0F5;box-shadow:0 1px 6px rgba(15,23,42,.05);' +
      "font-family:'Rajdhani',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;color:#1A202C;}" +
    '.tsa-top.tsa-sticky{position:sticky;}.tsa-top.tsa-fixed{position:fixed;}' +
    '.tsa-top a,.tsa-top button{flex:0 0 40px;width:40px;height:40px;border-radius:50%;border:0;background:none;display:flex;align-items:center;justify-content:center;color:#1A202C;cursor:pointer;padding:0;margin:0;text-decoration:none;}' +
    '.tsa-top a svg,.tsa-top button svg{width:22px;height:22px;flex:0 0 22px;}' +
    '.tsa-top a:active,.tsa-top button:active{background:#F1F5F9;}' +
    '.tsa-top b{flex:1;min-width:0;font-weight:700;font-size:19px;line-height:1.1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;letter-spacing:0;text-transform:none;}' +
    /* bottom tabs */
    '.tsa-tabs{position:fixed;left:0;right:0;bottom:0;z-index:980;display:grid;grid-template-columns:repeat(5,1fr);box-sizing:border-box;height:calc(' + TAB + 'px + env(safe-area-inset-bottom,0px));' +
      'padding:0 0 env(safe-area-inset-bottom,0px);margin:0;background:#fff;border-top:1px solid #EDF0F5;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;}' +
    '.tsa-tabs a{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;font-size:10.5px;font-weight:700;line-height:1.2;color:#94A3B8;text-decoration:none;text-transform:none;letter-spacing:0;padding:0;margin:0;background:none;border:0;border-radius:0;}' +
    '.tsa-tabs a svg{width:23px;height:23px;}' +
    '.tsa-tabs a.on{color:#FF6B00;}' +
    '.tsa-tabs a.on::before{content:"";position:absolute;top:0;left:50%;width:26px;height:3px;margin-left:-13px;border-radius:0 0 4px 4px;background:#FF6B00;}' +
    '.tsa-tabs a.on svg{fill:rgba(255,107,0,.14);}' +
    '.tsa-tabs a:active{transform:scale(.94);}';
  var st = document.createElement('style');
  st.id = 'tssc-app-css';
  st.textContent = css;
  (document.head || root).appendChild(st);

  function svg(d) { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + d + '</svg>'; }
  var ICON = {
    back: '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>',
    home: svg('<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/>'),
    mocks: svg('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>'),
    pyq: svg('<path d="M14 3H6v18h12V7z"/><path d="M14 3v4h4"/><path d="M9 13h6M9 17h6"/>'),
    chapters: svg('<path d="M4 5h7v14H4zM13 5h7v14h-7z"/>'),
    me: svg('<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>')
  };

  function activeTab() {
    var p = path.toLowerCase();
    if (/dashboard|my-orders|login/.test(p)) return 'me';
    if (/chapter|-questions\.html|^\/pyq-chapters\//.test(p)) return 'chapters';
    if (/pyq|previous-year/.test(p)) return 'pyq';
    if (/mock/.test(p)) return 'mocks';
    return '';
  }
  function pageTitle() {
    var t = String(document.title || '').replace(/\s*[|–—-]\s*TrickySSC.*$/i, '');
    t = t.split(/\s[–—|]\s|:\s|\s-\s/)[0];
    t = t.replace(/\s+(Free\b.*|in Hindi\b.*|with Solutions?\b.*)$/i, '').trim();
    return t || 'TrickySSC';
  }
  function siteNav() {
    var c = document.querySelectorAll('nav.tssc-nav,nav.topbar,nav.nav,nav.site-nav,header.nav,body>nav');
    return c.length ? c[0] : null;
  }

  function build() {
    if (document.querySelector('.tsa-top')) return;
    var body = document.body; if (!body) return;

    /* measure the website header, then take it out */
    var nav = siteNav(), fixed = false, h = 0;
    if (nav) {
      try { fixed = getComputedStyle(nav).position === 'fixed'; h = nav.offsetHeight || 0; } catch (e) {}
      nav.classList.add('tsa-gone');
    }

    /* breadcrumbs written without a class: "Home › Courses › …" */
    try {
      var sp = document.querySelectorAll('span');
      for (var i = 0; i < sp.length; i++) {
        if (sp[i].textContent.trim() !== '\u203A') continue;
        var p = sp[i].parentElement;
        if (!p || p === body || p.classList.contains('tsa-gone')) continue;
        var txt = p.textContent.trim();
        if (txt.length > 160 || !/^(\uD83C\uDFE0\s*)?Home/.test(txt)) continue;
        var up = p.parentElement;
        ((up && up !== body && up.children.length === 1 && up.textContent.trim() === txt) ? up : p).classList.add('tsa-gone');
      }
    } catch (e) {}

    var top = document.createElement('div');
    top.className = 'tsa-top ' + (fixed ? 'tsa-fixed' : 'tsa-sticky');
    /* a fixed website header already has its space reserved by the page: fill exactly that space */
    if (fixed && h > BAR) top.style.height = 'calc(' + h + 'px + env(safe-area-inset-top,0px))';
    top.innerHTML = '<button type="button" aria-label="Back">' + ICON.back + '</button><b></b><a href="/app.html" aria-label="Home">' + ICON.home + '</a>';
    top.querySelector('b').textContent = pageTitle();
    top.querySelector('button').addEventListener('click', function () {
      if (history.length > 1) history.back(); else location.href = '/app.html';
    });
    body.insertBefore(top, body.firstChild);

    if (!NO_TABS) {
      var cur = activeTab();
      var tabs = document.createElement('div');
      tabs.className = 'tsa-tabs';
      tabs.innerHTML = [['home', 'Home', '/app.html'], ['mocks', 'Mocks', '/app.html#mocks'], ['pyq', 'PYQs', '/app.html#pyq'], ['chapters', 'Chapters', '/app.html#chapters'], ['me', 'Me', '/app.html#me']]
        .map(function (t) { return '<a href="' + t[2] + '"' + (t[0] === cur ? ' class="on"' : '') + '>' + ICON[t[0]] + t[1] + '</a>'; }).join('');
      body.appendChild(tabs);
    }

    /* links that would drop the student on the website homepage go to the app home instead */
    document.addEventListener('click', function (e) {
      var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
      if (!a) return;
      var href = a.getAttribute('href') || '';
      if (/^(https?:\/\/(www\.)?trickyssc\.com)?\/?(index\.html)?$/.test(href) && href !== '') { e.preventDefault(); location.href = '/app.html'; }
    }, true);
  }


  /* TSSC-APPTRIM-V1: study sections of a chapter page become one-line rows; the section opens in a sheet */
  var STUDY = [['topics', '📘', 'Concepts and formulas'], ['examples', '✏️', 'Solved examples'], ['tips', '💡', 'Tips and common mistakes']];
  function trim() {
    var body = document.body, tests = document.querySelector('main>section#tests');
    if (tests && !document.querySelector('.tsa-rows')) {
      var rows = document.createElement('div'); rows.className = 'tsa-rows';
      STUDY.forEach(function (x) {
        var sec = document.querySelector('main>section#' + x[0]); if (!sec) return;
        var sheet = document.createElement('div'); sheet.className = 'tsa-sheet';
        sheet.innerHTML = '<div class="tsa-sheet-card"><div class="tsa-sheet-h"><b></b><button type="button" aria-label="Close">✕</button></div><div class="tsa-sheet-b"></div></div>';
        sheet.querySelector('b').textContent = x[2];
        sheet.querySelector('.tsa-sheet-b').appendChild(sec);
        var close = function () { sheet.classList.remove('on'); root.classList.remove('tsa-lock'); };
        sheet.addEventListener('click', function (e) { if (e.target === sheet) close(); });
        sheet.querySelector('button').addEventListener('click', close);
        body.appendChild(sheet);
        var b = document.createElement('button'); b.type = 'button'; b.className = 'tsa-row';
        b.innerHTML = '<i style="font-style:normal"></i><span></span>' + svg('<path d="M9 6l6 6-6 6"/>');
        b.firstChild.textContent = x[1]; b.querySelector('span').textContent = x[2];
        b.addEventListener('click', function () { sheet.classList.add('on'); root.classList.add('tsa-lock'); sheet.querySelector('.tsa-sheet-b').scrollTop = 0; });
        rows.appendChild(b);
      });
      if (rows.firstChild) tests.parentNode.insertBefore(rows, tests.nextSibling);
    }
    /* chapter rows: keep the count, drop the rest of the small print */
    var metas = document.querySelectorAll('.ch-list .ch-meta');
    for (var i = 0; i < metas.length; i++) {
      var h = metas[i].innerHTML, k = h.indexOf(' · ');
      if (k > 0 && /<b>\d/.test(h.slice(0, k))) metas[i].innerHTML = h.slice(0, k);
    }
  }
  function start() { build(); try { trim(); } catch (e) {} }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
