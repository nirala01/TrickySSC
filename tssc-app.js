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
  /* test engines and admin tools: untouched */
  if (/^(test|mock-test|ai-test)[a-z0-9-]*\.html$/.test(file)) return;
  if (/^(admin|batch-uploader|uploader|upload_|question-|solution-|image-question|trickyssc-figure|figure-checker|content-admin|ca-admin|chapter-tag-admin|reports-admin|mock-inspector|quality-check|json-to|pdf-to|hindi-translator|en-diag|clipboard|loader|candidates)/.test(file)) return;

  /* pages where the bottom tabs would get in the way (a test is running, or login) */
  var NO_TABS = /^(chapterwise-test|pyq-chapter-test|login|rank)\.html$/.test(file);

  var TAB = 58, BAR = 52;
  var root = document.documentElement;
  root.classList.add('tssc-app');
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

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build); else build();
})();
