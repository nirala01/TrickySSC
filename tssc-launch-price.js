/* ============================================================================
   tssc-launch-price.js  -  TSSC-LAUNCHPRICE-V7  (Dussehra offer, 17-22 Oct 2026)

   PRICES ARE NOT GOING UP. SSC CGL mocks stay Rs 49, SSC CHSL mocks stay Rs 49,
   and a CGL + CHSL combo is offered at Rs 79 as the Dussehra offer.

   Until FEST_END (the end of 22 Oct 2026, IST) this script:
     - fills every <span data-lp-note> with a short "Dussehra offer - price not
       increased, combo Rs 79" note (hidden from people who already own the plan);
     - shows ONE Dussehra-offer popup per browser session on the SSC CGL and
       SSC CHSL mock pages, to visitors who have not bought that page's plan.
   From FEST_END on it shows no note and no popup; the pages simply show their
   normal prices and the normal buy popup.

   It always keeps every <span data-lp> at Rs 49, so a page whose own text is out
   of date (an older copy still saying Rs 99) shows the right price.

   DISPLAY ONLY. What a buyer is CHARGED comes from config/pricing (admin-pricing).
   No Firestore read, no network call. Storage: one sessionStorage flag
   (tsscFestPopSeen) so the popup shows once per session.

   Hooks a page can carry:
     <span data-lp>Rs 49</span>               always shows Rs 49
     <span data-lp-note="inline" hidden>      offer note, shown until FEST_END
     data-lp-note also takes "tag" and "popup": same words, different spacing
============================================================================ */
(function () {
  'use strict';

  /* ---- SETTINGS ---------------------------------------------------------- */
  var PRICE     = 49;                                           // CGL plan, and CHSL plan
  var COMBO     = 79;                                           // CGL + CHSL combo
  var FEST_END  = Date.parse('2026-10-23T00:00:00+05:30');      // offer wording ends (IST)
  var LAST_DAY  = '22 Oct';                                     // how the last day is written
  var OFFER     = 'Dussehra offer';
  /* ------------------------------------------------------------------------ */

  var RUPEE = '\u20B9';
  var FEST  = Date.now() < FEST_END;

  var CSS =
    '.lp-n{box-sizing:border-box;max-width:100%;background:linear-gradient(135deg,#EA580C,#B91C1C);' +
      'color:#fff;border-radius:10px;font-weight:700;line-height:1.3;text-decoration:none;' +
      'box-shadow:0 3px 10px rgba(185,28,28,.28);}' +
    '.lp-n .lp-b{font-weight:800;white-space:nowrap;}' +
    '.lp-n .lp-s{font-weight:700;}' +
    ".lp-n-inline,.lp-n-tag{display:inline-block;padding:.3rem .85rem;font-family:'Rajdhani',sans-serif;" +
      'font-size:1.08rem;letter-spacing:.2px;}' +
    '.lp-n-inline{margin:.3rem 0;}' +
    '.lp-n-tag{margin:.5rem 0 0;}' +
    '.lp-n-inline .lp-b,.lp-n-tag .lp-b{font-size:1.1em;margin-right:.45em;}' +
    '.lp-n-inline .lp-s,.lp-n-tag .lp-s{display:block;font-size:.95em;margin-top:.1rem;}' +
    '.lp-n-inline .lp-t,.lp-n-tag .lp-t{margin:.35rem 0 .1rem;max-width:300px;}' +
    '.lp-n-inline .lp-r,.lp-n-tag .lp-r{font-size:.95rem;padding:.25rem 0;}' +
    '.lp-n-inline .lp-r b,.lp-n-tag .lp-r b{font-size:1.05rem;}' +
    '.lp-n-popup{display:block;margin:-.15rem 0 .95rem;padding:.6rem .8rem .65rem;border-radius:12px;' +
      'text-align:center;box-shadow:0 6px 18px rgba(220,38,38,.3);}' +
    ".lp-n-popup .lp-b{display:flex;align-items:center;justify-content:center;gap:.5rem;font-family:'Baloo 2','Rajdhani',sans-serif;font-size:1.5rem;line-height:1.15;}" +
    '.lp-n-popup .lp-s{display:block;font-size:1.05rem;line-height:1.3;margin-top:.2rem;}' +
    /* TSSC-LPNOTE-V2: the diya sits on a white disc so it stands out on the orange
       card, and the popup lists each price on its own line. */
    '.lp-n .lp-i{display:inline-flex;align-items:center;justify-content:center;width:1.55em;height:1.55em;' +
      'border-radius:50%;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.25);font-size:.95em;line-height:1;' +
      'vertical-align:middle;margin-right:.35em;}' +
    '.lp-n-popup .lp-b .lp-i{margin-right:0;font-size:1.05em;}' +
    '.lp-n .lp-t{display:block;margin:.55rem auto 0;max-width:290px;background:#fff;color:#1F2937;' +
      'border-radius:10px;padding:.2rem .7rem;text-align:left;}' +
    '.lp-n .lp-r{display:flex;justify-content:space-between;align-items:baseline;gap:.75rem;' +
      'padding:.38rem 0;font-size:1rem;font-weight:700;border-top:1px dashed #FED7AA;}' +
    '.lp-n .lp-r:first-child{border-top:0;}' +
    '.lp-n .lp-r b{font-size:1.2rem;font-weight:800;color:#15803D;white-space:nowrap;}' +
    '.lp-n .lp-r.lp-c{color:#B91C1C;}' +
    '.lp-n .lp-r.lp-c b{color:#B91C1C;}' +
    'body.tssc-owned-user .lp-n{display:none!important;}' +
    /* popup */
    '.lpP{position:fixed;inset:0;z-index:2147483000;display:flex;align-items:center;justify-content:center;' +
      'padding:16px;background:rgba(13,27,42,.62);opacity:0;transition:opacity .22s ease;}' +
    '.lpP.on{opacity:1;}' +
    '.lpP-box{position:relative;width:100%;max-width:400px;max-height:calc(100vh - 32px);' +
      "overflow-y:auto;background:#fff;border-radius:18px;box-shadow:0 24px 60px rgba(0,0,0,.38);text-align:center;" +
      "font-family:'Rajdhani',system-ui,sans-serif;color:#0D1B2A;transform:translateY(12px) scale(.97);" +
      'transition:transform .22s ease;outline:0;}' +
    '.lpP.on .lpP-box{transform:none;}' +
    '.lpP-top{background:linear-gradient(135deg,#B91C1C,#EA580C 60%,#F59E0B);color:#fff;font-weight:700;font-size:1.05rem;' +
      'letter-spacing:1px;text-transform:uppercase;padding:.7rem 2.9rem;line-height:1.25;border-radius:18px 18px 0 0;}' +
    '.lpP-x{position:absolute;top:.45rem;right:.5rem;width:34px;height:34px;border:0;border-radius:50%;padding:0;' +
      'background:rgba(255,255,255,.28);color:#fff;font-size:1.35rem;line-height:1;cursor:pointer;}' +
    '.lpP-body{padding:1.2rem 1.15rem 1.1rem;}' +
    ".lpP-h{font-family:'Baloo 2','Rajdhani',sans-serif;font-weight:800;font-size:1.85rem;line-height:1.1;" +
      'margin:0 0 .5rem;color:#0D1B2A;}' +
    '.lpP-rows{margin:0 0 .9rem;padding:0;list-style:none;font-size:1.12rem;font-weight:600;color:#334155;line-height:1.5;}' +
    '.lpP-rows b{color:#0D1B2A;}' +
    '.lpP-rows s{color:#94A3B8;font-weight:600;margin-left:.2rem;}' +
    '.lpP-combo{margin:0 0 1rem;padding:.65rem .8rem;border-radius:12px;background:#FFF7ED;border:2px dashed #F59E0B;' +
      'font-size:1.12rem;font-weight:700;color:#9A3412;line-height:1.35;}' +
    ".lpP-combo b{display:block;font-family:'Baloo 2','Rajdhani',sans-serif;font-size:1.45rem;color:#B91C1C;}" +
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
    if (el.hasAttribute('data-lp')) {                     // the price: always Rs 49
      if (el.textContent !== RUPEE + PRICE) el.textContent = RUPEE + PRICE;
      return;
    }
    if (el.__lp) return;
    el.__lp = 1;
    if (!FEST) return;                                    // after the offer: note stays hidden
    var kind = el.getAttribute('data-lp-note') || 'inline';
    if (kind !== 'tag' && kind !== 'popup') kind = 'inline';
    el.textContent = '';
    var mk = function (cls, txt) {
      var x = document.createElement('span');
      if (cls) x.className = cls;
      if (txt != null) x.textContent = txt;
      return x;
    };
    var big = mk('lp-b');
    big.appendChild(mk('lp-i', '\uD83E\uDE94'));
    big.appendChild(document.createTextNode(OFFER));
    el.appendChild(big);
    {                                                     // one price per line
      el.appendChild(mk('lp-s', 'Prices not increased!'));
      var t = mk('lp-t');
      [['SSC CGL mocks', RUPEE + PRICE, ''],
       ['SSC CHSL mocks', RUPEE + PRICE, ''],
       ['CGL + CHSL combo', RUPEE + COMBO, ' lp-c']].forEach(function (r) {
        var row = mk('lp-r' + r[2]);
        row.appendChild(mk('', r[0]));
        var b = document.createElement('b'); b.textContent = r[1];
        row.appendChild(b);
        t.appendChild(row);
      });
      el.appendChild(t);
    }
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
  }
  document.addEventListener('DOMContentLoaded', function () { sweep(document.documentElement); });

  /* After the Dussehra offer only the Rs 29 upgrade popup remains (for buyers of
     one series, while an upgrade product is Live in admin-pricing). */

  /* ==========================================================================
     Dussehra popups - SSC CGL and SSC CHSL mock pages. Once per browser session.
       signed out, or owns neither series   -> "Prices not increased" + combo Rs 79
       owns ONLY the other series            -> upgrade: add this series for Rs 29
       owns ONLY this page's series          -> upgrade: add the other series for Rs 29
       owns BOTH series                      -> nothing at all
     The Rs 29 upgrade popup shows only while an upgrade product (id p-upgrade-...)
     is Live in admin-pricing, and keeps running after 22 Oct until it is unticked.
     The "prices not increased" popup ends with the Dussehra offer (FEST_END).
     Anything unclear -> no popup.
  ========================================================================== */
  var ON_MOCK_PAGE = /\/(mock-list|ssc-(?:cgl|chsl)-(?:[a-z0-9]+-)*mock-test)(?:\.html)?\/?$/i.test(location.pathname);
  if (!ON_MOCK_PAGE) return;
  var IS_CHSL   = /ssc-chsl-/i.test(location.pathname);
  var THIS_KEY  = IS_CHSL ? 'ssc-chsl-mocks' : 'ssc-cgl-mocks';
  var OTHER_KEY = IS_CHSL ? 'ssc-cgl-mocks'  : 'ssc-chsl-mocks';
  var NAME  = { 'ssc-cgl-mocks': 'SSC CGL', 'ssc-chsl-mocks': 'SSC CHSL' };
  var COUNT = { 'ssc-cgl-mocks': 100,       'ssc-chsl-mocks': 80 };
  var HUB   = { 'ssc-cgl-mocks': '/ssc-cgl-mock-test.html', 'ssc-chsl-mocks': '/ssc-chsl-mock-test.html' };

  var POP_KEY      = 'tsscFestPopSeen';
  var ENT_FRESH_MS = 10 * 60 * 1000;      // same life as the page's own entitlement cache
  var POP_DELAY_MS = 1500;

  function popSeen()  { try { return sessionStorage.getItem(POP_KEY) === '1'; } catch (e) { return false; } }
  function markSeen() { try { sessionStorage.setItem(POP_KEY, '1'); } catch (e) {} }
  function ownsPlan() { return !!(document.body && document.body.classList.contains('tssc-owned-user')); }

  /* What the page's paywall found for this uid, for BOTH series (TSSC-ENTCACHE-V2
     record written by the mock pages), or null while not known yet. */
  function ownedMap(uid) {
    try {
      var o = JSON.parse(sessionStorage.getItem('tssc_ent_v2_' + uid) || 'null');
      if (o && o.m && Date.now() - (o.ts || 0) < ENT_FRESH_MS &&
          typeof o.m['ssc-cgl-mocks'] === 'boolean' && typeof o.m['ssc-chsl-mocks'] === 'boolean') return o.m;
    } catch (e) {}
    return null;
  }

  /* Calls back once we KNOW who this is: {signedIn:false} or {signedIn:true, m:{...}}.
     If the answer never arrives (30 s), it never calls back. */
  function whenKnown(cb) {
    var tries = 0;
    (function waitLogin() {
      var L = window.tsscLogin;
      if (!L || !L.auth || typeof L.auth.onAuthStateChanged !== 'function') {
        if (++tries < 100) setTimeout(waitLogin, 300);
        return;
      }
      var settled = false, unsub = null;
      unsub = L.auth.onAuthStateChanged(function (user) {
        if (settled) return;
        settled = true;
        setTimeout(function () { try { if (unsub) unsub(); } catch (e) {} }, 0);
        if (!user) { cb({ signedIn: false }); return; }
        var n = 0;
        (function waitPaywall() {
          var m = ownedMap(user.uid);
          if (m) { cb({ signedIn: true, m: m }); return; }
          if (++n < 75) setTimeout(waitPaywall, 400);
        })();
      });
    })();
  }

  /* Price of the Live upgrade product (id p-upgrade-...) that grants `key`, plus the
     normal price of that series; done(null) if no upgrade product is Live. */
  function upgradePrice(key, done) {
    var P = window.TSSC_PRICING;
    if (!P || typeof P.load !== 'function' || typeof P.upgradeFor !== 'function') { done(null); return; }
    P.load().then(function (cat) {
      var u = P.upgradeFor(cat, key), b = (typeof P.bestFor === 'function') ? P.bestFor(cat, key) : null;
      done(u ? u.price : null, b ? b.price : null);
    }, function () { done(null); });
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

  /* kind 'offer':   opt.combo = show the Rs 79 combo line
     kind 'upgrade': opt.key = the series to add, opt.price, opt.here = it is this page's series */
  function openPopup(kind, opt) {
    if (popEl || popSeen() || !document.body) return;
    if (kind === 'offer' && (ownsPlan() || !(Date.now() < FEST_END))) return;
    /* a checkout or login popup is already open: wait for it, then give up quietly */
    if (document.body.style.overflow === 'hidden' || document.documentElement.style.overflow === 'hidden') {
      if (++busyTries < 20) setTimeout(function () { openPopup(kind, opt); }, 1500);
      return;
    }
    markSeen();

    var wrap = make('div', 'lpP');
    wrap.setAttribute('role', 'dialog');
    wrap.setAttribute('aria-modal', 'true');
    wrap.setAttribute('aria-labelledby', 'lpPTitle');

    var box  = make('div', 'lpP-box');
    box.tabIndex = -1;
    var x    = make('button', 'lpP-x', '\u00D7');
    x.type = 'button';
    x.setAttribute('aria-label', 'Close');
    var body = make('div', 'lpP-body');
    var top, h, go, foot, onGo;
    var no = make('button', 'lpP-no', 'Not now');
    no.type = 'button';

    if (kind === 'upgrade') {
      var have = opt.key === 'ssc-cgl-mocks' ? 'ssc-chsl-mocks' : 'ssc-cgl-mocks';
      top = make('div', 'lpP-top', (Date.now() < FEST_END ? '\uD83E\uDE94 ' + OFFER : '\uD83C\uDF81 Special offer') + ' \u00B7 just for you');
      h   = make('h2', 'lpP-h', 'Add ' + NAME[opt.key] + ' mocks for ' + RUPEE + opt.price);
      var rows = make('ul', 'lpP-rows');
      rows.appendChild(make('li', '', 'You already have the ' + NAME[have] + ' mocks.'));
      body.appendChild(h); body.appendChild(rows);
      var deal = make('div', 'lpP-combo');
      deal.appendChild(make('b', '', 'All ' + COUNT[opt.key] + ' ' + NAME[opt.key] + ' mocks: ' + RUPEE + opt.price));
      deal.appendChild(document.createTextNode('For a full year' + (opt.regular > opt.price ? ', instead of ' + RUPEE + opt.regular : '')));
      body.appendChild(deal);
      go   = make('button', 'lpP-go', '\uD83D\uDD13 Add ' + NAME[opt.key] + ' for ' + RUPEE + opt.price);
      foot = make('p', 'lpP-f', 'Only for buyers of the ' + NAME[have] + ' mocks');
      onGo = function () {
        if (opt.here && typeof window.tsscOpenBuy === 'function') { window.tsscOpenBuy(null); return; }
        location.href = HUB[opt.key] + '?upgrade=1';
      };
    } else {
      top = make('div', 'lpP-top', '\uD83E\uDE94 ' + OFFER + ' \uD83E\uDE94');
      h   = make('h2', 'lpP-h', 'Prices not increased!');
      var list = make('ul', 'lpP-rows');
      var r1 = make('li');
      r1.appendChild(document.createTextNode('SSC CGL mocks: still '));
      r1.appendChild(make('b', '', RUPEE + PRICE));
      var r2 = make('li');
      r2.appendChild(document.createTextNode('SSC CHSL mocks: still '));
      r2.appendChild(make('b', '', RUPEE + PRICE));
      if (IS_CHSL) { list.appendChild(r2); list.appendChild(r1); } else { list.appendChild(r1); list.appendChild(r2); }
      body.appendChild(h); body.appendChild(list);
      if (opt && opt.combo) {
        var combo = make('div', 'lpP-combo');
        combo.appendChild(make('b', '', 'CGL + CHSL combo ' + RUPEE + COMBO));
        combo.appendChild(document.createTextNode('Both mock series for a full year, instead of ' + RUPEE + (PRICE * 2)));
        body.appendChild(combo);
      }
      go   = make('button', 'lpP-go', '\uD83D\uDD13 See the plans');
      foot = make('p', 'lpP-f', (opt && opt.combo) ? 'Combo offer till ' + LAST_DAY + ' \u00B7 first mocks stay free'
                                                   : 'First mocks stay free');
      onGo = function () {
        /* same thing the page's own "Go Premium" button does */
        if (typeof window.tsscOpenBuy === 'function') { window.tsscOpenBuy(null); return; }
        var pn = document.querySelector('.price-note');
        if (pn && pn.scrollIntoView) pn.scrollIntoView({ behavior: 'smooth', block: 'center' });
      };
    }
    h.id = 'lpPTitle';
    go.type = 'button';
    body.appendChild(go); body.appendChild(no); body.appendChild(foot);
    box.appendChild(top); box.appendChild(x); box.appendChild(body);
    wrap.appendChild(box);

    x.addEventListener('click', closePopup);
    no.addEventListener('click', closePopup);
    wrap.addEventListener('click', function (e) { if (e.target === wrap) closePopup(); });
    go.addEventListener('click', function () { closePopup(); onGo(); });

    popPrevOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    document.body.appendChild(wrap);
    popEl = wrap;
    document.addEventListener('keydown', onPopKey);
    /* if this page's plan becomes owned while an offer for it is open, step aside */
    if (kind === 'offer' || opt.here) popWatch = setInterval(function () { if (ownsPlan()) closePopup(); }, 1000);
    setTimeout(function () { if (popEl === wrap) { wrap.className = 'lpP on'; try { box.focus(); } catch (e) {} } }, 30);
  }

  function decide(st) {
    var fest  = Date.now() < FEST_END;
    var later = function (kind, opt) { setTimeout(function () { openPopup(kind, opt); }, POP_DELAY_MS); };
    if (!st.signedIn) { if (fest) later('offer', { combo: true }); return; }
    var mine = !!st.m[THIS_KEY], other = !!st.m[OTHER_KEY];
    if (mine && other) return;                                   // owns both: no offer at all
    if (!mine && !other) { if (fest) later('offer', { combo: true }); return; }
    if (mine) {                                                  // owns only this page's series
      upgradePrice(OTHER_KEY, function (price, regular) {
        if (price) later('upgrade', { key: OTHER_KEY, price: price, regular: regular, here: false });
      });
      return;
    }
    upgradePrice(THIS_KEY, function (price, regular) {           // owns only the other series
      if (price) later('upgrade', { key: THIS_KEY, price: price, regular: regular, here: true });
      else if (fest) later('offer', { combo: false });
    });
  }

  if (!popSeen()) whenKnown(decide);
})();
