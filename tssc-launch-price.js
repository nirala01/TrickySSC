/* ============================================================================
   tssc-launch-price.js  —  TSSC-LAUNCHPRICE-V5 (price-rise popup on the CGL mock pages, free users only)

   SSC CGL mock plan: the Rs 49 launch price ends 17 Oct 2026. Rs 99 from 18 Oct.

   Every page's own HTML already says Rs 99. Until SWITCH_AT, this script shows
   the launch price in its place and fills in the "ends 17 Oct" notes. From
   SWITCH_AT onward it does nothing at all, so no page needs a second edit.

   DISPLAY ONLY. What a buyer is CHARGED comes from config/pricing, which you
   edit in admin-pricing.html. On 18 Oct, set the product price to 99 there.

   To move the deadline, change SWITCH_AT and FIRST_DAY under SETTINGS — nothing
   else. To end the launch price early, set SWITCH_AT to a date in the past.

   Hooks a page can carry:
     <span data-lp>Rs 99</span>               shows Rs 49 until the switch
     <span data-lp-after hidden>              stays hidden until the switch, shown from
                                              it (V5: "Rs 99 plan also unlocks CHSL")
     <span data-lp-note="inline" hidden>      deadline note, filled in and shown
     data-lp-note also takes "tag" and "popup": same words, different spacing

   POPUP (V4). On the SSC CGL mock pages only, a visitor who has NOT bought the
   plan sees one price-rise popup per browser session. Someone who owns the
   plan never sees it, and the red deadline notes are hidden for them too.
   Who has paid is read from what the page's own paywall has already worked
   out (the tssc_ent_<uid> cache and the tssc-owned-user class on <body>), so
   this file makes no Firestore read of its own. If that answer never arrives,
   the popup stays closed. Like everything else here, it stops on SWITCH_AT.

   No Firestore read, no network call. Storage: one sessionStorage flag
   (tsscLpPopSeen) so the popup shows once per session.
============================================================================ */
(function () {
  'use strict';

  /* ---- SETTINGS ---------------------------------------------------------- */
  var INTRO     = 49;                                           // launch price
  var REGULAR   = 99;                                           // price from the switch
  var SWITCH_AT = Date.parse('2026-10-18T00:00:00+05:30');      // first moment of Rs 99 (IST)
  var FIRST_DAY = '18 Oct';                                     // how that date is written in the note
  /* ------------------------------------------------------------------------ */

  var left = SWITCH_AT - Date.now();
  if (!(left > 0)) { revealAfter(); return; } // switch has passed: pages already say Rs 99

  /* V5 — from the switch, show every <... data-lp-after hidden> line. */
  function revealAfter() {
    function run() {
      var els = document.querySelectorAll('[data-lp-after]');
      for (var i = 0; i < els.length; i++) els[i].hidden = false;
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
    else run();
  }

  var RUPEE = '\u20B9';
  var days  = Math.ceil(left / 86400000);     // counts today, so 17 Oct itself reads "last day"
  var BIG   = days <= 1 ? 'Last day at ' + RUPEE + INTRO : days + ' days left';
  /* second line, as [before-arrow, after-arrow]; no arrow on the last day */
  var SMALL = days <= 1 ? [RUPEE + REGULAR + ' from tomorrow']
                        : [RUPEE + INTRO + ' now', RUPEE + REGULAR + ' from ' + FIRST_DAY];

  var CSS =
    /* shared: solid red, white text */
    '.lp-n{box-sizing:border-box;max-width:100%;background:linear-gradient(135deg,#DC2626,#B91C1C);' +
      'color:#fff;border-radius:10px;font-weight:700;line-height:1.3;text-decoration:none;' +
      'box-shadow:0 3px 10px rgba(185,28,28,.28);}' +
    '.lp-n .lp-b{font-weight:800;white-space:nowrap;}' +
    '.lp-n .lp-s{font-weight:700;}' +
    ".lp-n .lp-a{display:inline-block;margin:0 .32em;font-family:Arial,'Segoe UI Symbol',sans-serif;" +
      'font-weight:900;font-size:1.3em;line-height:1;vertical-align:-.06em;}' +
    /* inside a sentence (price banner on the mock pages) and under the homepage card price */
    ".lp-n-inline,.lp-n-tag{display:inline-block;padding:.3rem .85rem;font-family:'Rajdhani',sans-serif;" +
      'font-size:1.08rem;letter-spacing:.2px;}' +
    '.lp-n-inline{margin:.3rem 0;}' +
    '.lp-n-tag{margin:.5rem 0 0;}' +
    '.lp-n-inline .lp-b,.lp-n-tag .lp-b{font-size:1.16em;margin-right:.45em;}' +
    /* the two parts never break in the middle: on a narrow screen the second part drops to its own line */
    '.lp-n-inline .lp-s,.lp-n-tag .lp-s{display:inline-block;white-space:nowrap;}' +
    /* promo popup: a full-width block with a large first line, gently pulsing */
    '.lp-n-popup{display:block;margin:-.15rem 0 .95rem;padding:.6rem .8rem .65rem;border-radius:12px;' +
      'text-align:center;box-shadow:0 6px 18px rgba(220,38,38,.38);animation:lpPulse 1.7s ease-in-out infinite;}' +
    ".lp-n-popup .lp-b{display:block;font-family:'Baloo 2','Rajdhani',sans-serif;font-size:1.75rem;line-height:1.1;}" +
    '.lp-n-popup .lp-s{display:block;font-size:1.3rem;line-height:1.25;margin-top:.15rem;letter-spacing:.2px;}' +
    '@keyframes lpPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.035)}}' +
    '@media(prefers-reduced-motion:reduce){.lp-n-popup{animation:none}}' +
    /* someone who already owns the plan sees no deadline note */
    'body.tssc-owned-user .lp-n{display:none!important;}' +
    /* price-rise popup (CGL mock pages, free users) */
    '.lpP{position:fixed;top:0;right:0;bottom:0;left:0;z-index:99990;display:flex;align-items:center;' +
      'justify-content:center;padding:14px;background:rgba(13,27,42,.64);opacity:0;transition:opacity .2s ease;}' +
    '.lpP.on{opacity:1;}' +
    ".lpP-box{position:relative;box-sizing:border-box;width:100%;max-width:400px;max-height:calc(100vh - 28px);" +
      "overflow-y:auto;background:#fff;border-radius:18px;box-shadow:0 24px 60px rgba(0,0,0,.38);text-align:center;" +
      "font-family:'Rajdhani',system-ui,sans-serif;color:#0D1B2A;transform:translateY(12px) scale(.97);" +
      'transition:transform .22s ease;outline:0;}' +
    '.lpP.on .lpP-box{transform:none;}' +
    '.lpP-top{background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;font-weight:700;font-size:1rem;' +
      'letter-spacing:1px;text-transform:uppercase;padding:.7rem 2.9rem;line-height:1.25;border-radius:18px 18px 0 0;}' +
    '.lpP-x{position:absolute;top:.45rem;right:.5rem;width:34px;height:34px;border:0;border-radius:50%;padding:0;' +
      'background:rgba(255,255,255,.28);color:#fff;font-size:1.35rem;line-height:1;cursor:pointer;}' +
    '.lpP-body{padding:1.25rem 1.15rem 1.1rem;}' +
    ".lpP-h{font-family:'Baloo 2','Rajdhani',sans-serif;font-weight:800;font-size:1.95rem;line-height:1.1;" +
      'margin:0 0 .4rem;color:#0D1B2A;}' +
    '.lpP-p{font-size:1.12rem;font-weight:600;line-height:1.35;color:#4A5568;margin:0 0 1.1rem;}' +
    '.lpP-p b{color:#0D1B2A;font-weight:700;}' +
    ".lpP-go{display:block;box-sizing:border-box;width:100%;border:0;border-radius:12px;padding:.85rem 1rem;" +
      "background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;font-family:'Rajdhani',system-ui,sans-serif;" +
      'font-weight:700;font-size:1.3rem;letter-spacing:.4px;line-height:1.2;cursor:pointer;' +
      'box-shadow:0 6px 16px rgba(255,107,0,.38);}' +
    ".lpP-no{display:inline-block;margin-top:.75rem;padding:.2rem .5rem;background:none;border:0;color:#718096;" +
      "font-family:'Rajdhani',system-ui,sans-serif;font-weight:600;font-size:1.02rem;cursor:pointer;" +
      'text-decoration:underline;}' +
    '.lpP-f{margin:.45rem 0 0;font-size:.98rem;font-weight:700;color:#00A86B;}' +
    '.lpP-x:focus-visible,.lpP-go:focus-visible,.lpP-no:focus-visible{outline:3px solid #0D1B2A;outline-offset:2px;}' +
    '@media(prefers-reduced-motion:reduce){.lpP,.lpP-box{transition:none;}}';

  function addCss() {
    if (document.getElementById('tsscLaunchPriceCSS')) return;
    var st = document.createElement('style');
    st.id = 'tsscLaunchPriceCSS';
    st.textContent = CSS;
    (document.head || document.documentElement).appendChild(st);
  }

  function paint(el) {
    if (el.__lp) return;
    el.__lp = 1;
    if (el.hasAttribute('data-lp')) {
      el.textContent = RUPEE + INTRO;
      return;
    }
    var kind = el.getAttribute('data-lp-note') || 'inline';
    if (kind !== 'tag' && kind !== 'popup') kind = 'inline';
    el.textContent = '';
    var big = document.createElement('span');
    big.className = 'lp-b';
    big.textContent = '\u23F3 ' + BIG;
    var small = document.createElement('span');
    small.className = 'lp-s';
    small.appendChild(document.createTextNode(SMALL[0]));
    if (SMALL.length > 1) {
      var arrow = document.createElement('span');
      arrow.className = 'lp-a';
      arrow.textContent = '\u2192';
      small.appendChild(arrow);
      small.appendChild(document.createTextNode(SMALL[1]));
    }
    el.appendChild(big);
    el.appendChild(document.createTextNode(' '));
    el.appendChild(small);
    el.className = (el.className ? el.className + ' ' : '') + 'lp-n lp-n-' + kind;
    el.removeAttribute('hidden');
  }

  var SEL = '[data-lp],[data-lp-note]';

  function sweep(root) {
    if (!root || root.nodeType !== 1) return;
    if (root.matches && root.matches(SEL)) paint(root);
    if (!root.firstElementChild) return;
    var found = root.querySelectorAll(SEL);
    for (var i = 0; i < found.length; i++) paint(found[i]);
  }

  addCss();
  sweep(document.documentElement);

  /* The script loads async, so part of the page may still be arriving, and some
     pages add their price line later from JS. Paint those as they appear. */
  if (window.MutationObserver) {
    new MutationObserver(function (recs) {
      for (var i = 0; i < recs.length; i++) {
        var added = recs[i].addedNodes;
        for (var j = 0; j < added.length; j++) sweep(added[j]);
      }
    }).observe(document.documentElement, { childList: true, subtree: true });
  } else {
    document.addEventListener('DOMContentLoaded', function () { sweep(document.documentElement); });
  }

  /* ==========================================================================
     Price-rise popup — SSC CGL mock pages only, and only for someone who has
     not bought the plan. Once per browser session. Gone on SWITCH_AT.
  ========================================================================== */
  var ON_MOCK_PAGE = /\/(mock-list|ssc-cgl-(?:[a-z0-9]+-)*mock-test)(?:\.html)?\/?$/i.test(location.pathname);
  if (!ON_MOCK_PAGE) return;

  var POP_KEY      = 'tsscLpPopSeen';
  var ENT_FRESH_MS = 10 * 60 * 1000;      // same life as the page's own entitlement cache
  var POP_DELAY_MS = 1500;

  function popSeen()  { try { return sessionStorage.getItem(POP_KEY) === '1'; } catch (e) { return false; } }
  function markSeen() { try { sessionStorage.setItem(POP_KEY, '1'); } catch (e) {} }
  function ownsPlan() { return !!(document.body && document.body.classList.contains('tssc-owned-user')); }

  /* What the page's paywall has concluded for this uid: true, false, or null = not known yet. */
  function entitlement(uid) {
    try {
      var o = JSON.parse(sessionStorage.getItem('tssc_ent_' + uid) || 'null');
      if (o && Date.now() - (o.ts || 0) < ENT_FRESH_MS) return !!o.owned;
    } catch (e) {}
    return null;
  }

  /* Calls back only once we KNOW this visitor has not bought the plan:
       signed out                                  -> free
       signed in, paywall says "not owned"         -> free
       signed in, paywall says "owned"             -> never
       anything unclear (login script or the paywall's answer never arrives) -> never */
  function whenFree(cb) {
    var tries = 0;
    (function waitLogin() {
      var L = window.tsscLogin;
      if (!L || !L.auth || typeof L.auth.onAuthStateChanged !== 'function') {
        if (++tries < 100) setTimeout(waitLogin, 300);          // up to 30 s
        return;
      }
      var settled = false, unsub = null;
      unsub = L.auth.onAuthStateChanged(function (user) {
        if (settled) return;
        settled = true;
        setTimeout(function () { try { if (unsub) unsub(); } catch (e) {} }, 0);
        if (!user) { cb(); return; }
        var n = 0;
        (function waitPaywall() {
          if (ownsPlan()) return;
          var e = entitlement(user.uid);
          if (e === true) return;
          if (e === false) { cb(); return; }
          if (++n < 75) setTimeout(waitPaywall, 400);           // up to 30 s
        })();
      });
    })();
  }

  var popEl = null, popPrevOverflow = '', popWatch = null, busyTries = 0;

  function closePopup() {
    if (!popEl) return;
    var el = popEl;
    popEl = null;
    if (popWatch) { clearInterval(popWatch); popWatch = null; }
    document.removeEventListener('keydown', onPopKey);
    document.body.style.overflow = popPrevOverflow;
    el.className = 'lpP';
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 220);
  }
  function onPopKey(e) { if (e.key === 'Escape' || e.keyCode === 27) closePopup(); }

  function make(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function openPopup() {
    if (popEl || popSeen() || ownsPlan() || !(SWITCH_AT - Date.now() > 0) || !document.body) return;
    /* a checkout or login popup is already open: wait for it, then give up quietly */
    if (document.body.style.overflow === 'hidden' || document.documentElement.style.overflow === 'hidden') {
      if (++busyTries < 20) setTimeout(openPopup, 1500);
      return;
    }
    markSeen();

    var wrap = make('div', 'lpP');
    wrap.setAttribute('role', 'dialog');
    wrap.setAttribute('aria-modal', 'true');
    wrap.setAttribute('aria-labelledby', 'lpPTitle');

    var box  = make('div', 'lpP-box');
    box.tabIndex = -1;                       // takes keyboard focus on open, without a ring
    var top  = make('div', 'lpP-top', '\uD83D\uDCE3 SSC CGL Mock Tests');
    var x    = make('button', 'lpP-x', '\u00D7');
    x.type = 'button';
    x.setAttribute('aria-label', 'Close');

    var body = make('div', 'lpP-body');
    var h    = make('h2', 'lpP-h', days <= 1 ? 'Price goes up tomorrow' : 'Price goes up on ' + FIRST_DAY);
    h.id = 'lpPTitle';

    var p = make('p', 'lpP-p');
    p.appendChild(make('b', '', 'All 100 mocks'));
    p.appendChild(document.createTextNode(' (50 Tier I + 50 Tier II) for a full year.'));

    var note = make('div');
    note.setAttribute('data-lp-note', 'popup');
    paint(note);

    var go = make('button', 'lpP-go', '\uD83D\uDD13 Unlock 100 mocks at ' + RUPEE + INTRO);
    go.type = 'button';
    var no = make('button', 'lpP-no', 'Not now');
    no.type = 'button';
    var foot = make('p', 'lpP-f', 'Mocks 1\u20134 stay free');

    body.appendChild(h); body.appendChild(p); body.appendChild(note);
    body.appendChild(go); body.appendChild(no); body.appendChild(foot);
    box.appendChild(top); box.appendChild(x); box.appendChild(body);
    wrap.appendChild(box);

    x.addEventListener('click', closePopup);
    no.addEventListener('click', closePopup);
    wrap.addEventListener('click', function (e) { if (e.target === wrap) closePopup(); });
    go.addEventListener('click', function () {
      closePopup();
      /* same thing the page's own "Go Premium" button does */
      if (typeof window.tsscOpenBuy === 'function') { window.tsscOpenBuy(null); return; }
      var pn = document.querySelector('.price-note');
      if (pn && pn.scrollIntoView) pn.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });

    popPrevOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    document.body.appendChild(wrap);
    popEl = wrap;
    document.addEventListener('keydown', onPopKey);
    /* if the plan becomes owned while this is open (login + purchase elsewhere), step aside */
    popWatch = setInterval(function () { if (ownsPlan()) closePopup(); }, 1000);
    setTimeout(function () { if (popEl === wrap) { wrap.className = 'lpP on'; try { box.focus(); } catch (e) {} } }, 30);
  }

  if (!popSeen()) whenFree(function () { setTimeout(openPopup, POP_DELAY_MS); });
})();
