/* ============================================================================
   tssc-gd-free.js  -  TSSC-GDFREE-V1  (SSC GD free period, 4-7 Nov 2026)

   Every SSC GD mock and subject-wise test is FREE until the end of 7 Nov 2026
   (IST). From 8 Nov 00:00 IST, Mock 1-2 stay free and the SSC GD pass
   (Rs 49 for one year) unlocks the rest. The locks themselves switch on by
   their own date settings (CFG.enforceFrom on the five GD list pages,
   TG_ENFORCE_FROM in mock-test.html / mock-test-subject.html). This file is
   DISPLAY ONLY: it never decides who can open a test.

   Until FREE_END it:
     - shows every [data-gdf="before"] element and hides every [data-gdf="after"];
     - writes the days left into every [data-gdf-left];
     - shows ONE "free till 7 Nov" popup per browser session to visitors who
       do not already hold the SSC GD pass (or All Access).
   From FREE_END on it does nothing: the pages show their normal Rs 49 wording.

   Hooks a page can carry:
     <span data-gdf="before" style="display:none">...</span>
                                                 shown only in the free period
     <span data-gdf="after">...</span>           hidden only in the free period
     <b data-gdf-left></b>                       "4 days left", "last day today"
     <button data-gdf-buy>                       opens the page's own checkout

   No Firestore read, no network call. Storage: one sessionStorage flag.
   Load it in <head> so the "after" wording never flashes during the offer.
============================================================================ */
(function () {
  'use strict';

  /* ---- SETTINGS ---------------------------------------------------------- */
  var FREE_END = Date.parse('2026-11-07T00:00:00+05:30');   // TSSC-GDPAY-NOW-V1: free period ended early on 7 Nov 2026 (paywall live now)
  var PRICE    = 49;
  var POP_KEY  = 'tsscGdFreePopSeen';
  /* ------------------------------------------------------------------------ */

  if (!(Date.now() < FREE_END)) return;                       // offer over: do nothing

  var RUPEE = '₹';
  var root = document.documentElement;
  root.classList.add('gdf-on');

  /* hide the "after" wording before the body paints */
  try {
    var st = document.createElement('style');
    st.textContent =
      'html.gdf-on [data-gdf="after"]{display:none!important;}' +
      '.gdf-left{white-space:nowrap;}' +
      '.gdf-buy{display:inline-block;margin-top:.55rem;background:linear-gradient(135deg,#FF6B00,#FF8C38);' +
        'color:#fff;border:none;border-radius:10px;padding:.55rem 1.15rem;font-family:\'Rajdhani\',sans-serif;' +
        'font-weight:800;font-size:.95rem;cursor:pointer;box-shadow:0 3px 10px rgba(255,107,0,.28);}' +
      '.gdf-buy:hover{filter:brightness(1.08);}' +
      'body.tssc-owned-user .gdf-buy{display:none!important;}' +
      '#gdfPop{position:fixed;inset:0;z-index:2147482000;display:flex;align-items:center;justify-content:center;' +
        'padding:16px;background:rgba(15,23,42,.72);-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px);}' +
      '#gdfPop .gdf-card{position:relative;background:#fff;color:#0F172A;width:100%;max-width:410px;border-radius:18px;' +
        'padding:26px 22px 20px;text-align:center;box-shadow:0 22px 55px rgba(0,0,0,.38);' +
        'font-family:\'Plus Jakarta Sans\',system-ui,sans-serif;max-height:calc(100vh - 32px);overflow:auto;}' +
      '#gdfPop .gdf-x{position:absolute;top:8px;right:10px;border:none;background:none;font-size:24px;line-height:1;' +
        'color:#94A3B8;cursor:pointer;padding:6px;}' +
      '#gdfPop .gdf-flag{display:inline-block;background:linear-gradient(135deg,#059669,#34D399);color:#fff;' +
        'font-family:\'Rajdhani\',sans-serif;font-weight:800;font-size:.8rem;letter-spacing:.06em;' +
        'padding:.25rem .8rem;border-radius:100px;}' +
      '#gdfPop .gdf-h{font-family:\'Rajdhani\',sans-serif;font-weight:800;font-size:1.45rem;line-height:1.2;' +
        'margin:.7rem 0 .2rem;}' +
      '#gdfPop .gdf-h span{color:#059669;}' +
      '#gdfPop .gdf-left-pill{display:inline-block;margin:.35rem 0 .2rem;background:#FEF3C7;color:#92400E;' +
        'font-weight:800;font-size:.85rem;padding:.2rem .7rem;border-radius:8px;}' +
      '#gdfPop .gdf-p{font-size:.92rem;color:#475569;line-height:1.6;margin:.55rem 0 0;}' +
      '#gdfPop .gdf-box{margin:.9rem 0 0;background:#FFF7ED;border:1px solid #FED7AA;border-radius:12px;' +
        'padding:.7rem .8rem;font-size:.88rem;color:#7C2D12;line-height:1.55;text-align:left;}' +
      '#gdfPop .gdf-box b{color:#C2410C;}' +
      '#gdfPop .gdf-hi{font-size:.85rem;color:#64748B;line-height:1.55;margin:.7rem 0 0;}' +
      '#gdfPop .gdf-go{display:block;width:100%;margin-top:1rem;padding:.8rem 1rem;border:none;border-radius:11px;' +
        'background:linear-gradient(135deg,#059669,#10B981);color:#fff;font-family:\'Rajdhani\',sans-serif;' +
        'font-weight:800;font-size:1.05rem;cursor:pointer;}' +
      '#gdfPop .gdf-pay{display:block;width:100%;margin-top:.55rem;padding:.7rem 1rem;border-radius:11px;' +
        'border:1.5px solid #FF6B00;background:#fff;color:#EA580C;font-family:\'Rajdhani\',sans-serif;' +
        'font-weight:800;font-size:.98rem;cursor:pointer;}';
    (document.head || root).appendChild(st);
  } catch (e) {}

  function leftText() {
    var ms = FREE_END - Date.now();
    if (ms <= 0) return '';
    var days = Math.ceil(ms / 86400000);
    if (days <= 1) return 'last day today';
    return days + ' days left';
  }

  function paint() {
    var i, el;
    var before = document.querySelectorAll('[data-gdf="before"]');
    for (i = 0; i < before.length; i++) { before[i].style.display = ''; before[i].hidden = false; }
    var lt = leftText();
    var left = document.querySelectorAll('[data-gdf-left]');
    for (i = 0; i < left.length; i++) { el = left[i]; el.textContent = lt; el.classList.add('gdf-left'); }
    var buys = document.querySelectorAll('[data-gdf-buy]');
    for (i = 0; i < buys.length; i++) { buys[i].addEventListener('click', buy); }
  }

  function buy(ev) {
    if (ev && ev.preventDefault) ev.preventDefault();
    closePop();
    if (typeof window.tsscOpenBuy === 'function') {
      try { window.tsscOpenBuy(null); return; } catch (e) {}
    }
    location.href = 'https://trickyssc.com/ssc-gd-mock-test.html';
  }

  function closePop() {
    var p = document.getElementById('gdfPop');
    if (p && p.parentNode) p.parentNode.removeChild(p);
    document.removeEventListener('keydown', onKey);
  }
  function onKey(e) { if (e.key === 'Escape') closePop(); }

  function owned() { return document.body.classList.contains('tssc-owned-user'); }
  function checkoutOpen() {
    var m = document.getElementById('mockBuyPop');
    if (!m) return false;
    var cs = window.getComputedStyle ? getComputedStyle(m) : null;
    return !!cs && cs.display !== 'none' && cs.visibility !== 'hidden' && !m.hidden;
  }

  function showPop() {
    if (document.getElementById('gdfPop') || owned() || checkoutOpen()) return;
    try { if (sessionStorage.getItem(POP_KEY)) return; sessionStorage.setItem(POP_KEY, '1'); } catch (e) {}
    var o = document.createElement('div');
    o.id = 'gdfPop';
    o.setAttribute('role', 'dialog');
    o.setAttribute('aria-modal', 'true');
    o.setAttribute('aria-label', 'SSC GD mocks free till 7 November');
    o.innerHTML =
      '<div class="gdf-card">' +
        '<button type="button" class="gdf-x" aria-label="Close">&times;</button>' +
        '<span class="gdf-flag">&#127881; FREE TILL 7 NOV</span>' +
        '<div class="gdf-h">All 60 SSC GD mocks are <span>FREE</span> till 7 Nov</div>' +
        '<span class="gdf-left-pill">&#9200; ' + leftText() + '</span>' +
        '<p class="gdf-p">Attempt every full-length mock and every Reasoning, GK, Maths and English ' +
          'subject-wise test at no cost until <b>7 November</b>.</p>' +
        '<div class="gdf-box">From <b>8 November</b>: Mock 1 and Mock 2 stay free. ' +
          'The full SSC GD series &mdash; all 60 mocks + every subject-wise test &mdash; ' +
          'is <b>' + RUPEE + PRICE + ' for one full year</b>.</div>' +
        '<p class="gdf-hi" lang="hi">7 नवंबर तक सभी SSC GD मॉक बिल्कुल फ्री। 8 नवंबर से मॉक 1&ndash;2 फ्री रहेंगे, ' +
          'पूरी सीरीज़ सिर्फ़ ' + RUPEE + PRICE + ' में (1 साल के लिए)।</p>' +
        '<button type="button" class="gdf-go">&#9654; Practise free now</button>' +
        '<button type="button" class="gdf-pay">&#128275; Get the full year for ' + RUPEE + PRICE + '</button>' +
      '</div>';
    document.body.appendChild(o);
    o.addEventListener('click', function (e) { if (e.target === o) closePop(); });
    o.querySelector('.gdf-x').addEventListener('click', closePop);
    o.querySelector('.gdf-go').addEventListener('click', function () {
      closePop();
      var list = document.getElementById('mock-list');
      if (list && list.scrollIntoView) { try { list.scrollIntoView({ behavior: 'smooth', block: 'start' }); } catch (e) {} }
    });
    o.querySelector('.gdf-pay').addEventListener('click', buy);
    document.addEventListener('keydown', onKey);
  }

  /* wait until the page has read the entitlement, so a pass holder never
     sees the popup; give up waiting after 6 s and show it anyway */
  function schedulePop() {
    if (!document.getElementById('mockBuyPop')) return;      // popup only on the GD mock list pages
    try { if (sessionStorage.getItem(POP_KEY)) return; } catch (e) {}
    var t0 = Date.now();
    (function wait() {
      if (document.body.classList.contains('tssc-ent-resolved') || Date.now() - t0 > 6000) {
        setTimeout(showPop, 900);
      } else {
        setTimeout(wait, 250);
      }
    })();
  }

  function start() { paint(); schedulePop(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
