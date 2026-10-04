/* ============================================================================
   tssc-launch-price.js  —  TSSC-LAUNCHPRICE-V2 (bigger, bolder deadline note)

   SSC CGL mock plan: the Rs 49 launch price ends 10 Oct 2026. Rs 99 from 11 Oct.

   Every page's own HTML already says Rs 99. Until SWITCH_AT, this script shows
   the launch price in its place and fills in the "ends 10 Oct" notes. From
   SWITCH_AT onward it does nothing at all, so no page needs a second edit.

   DISPLAY ONLY. What a buyer is CHARGED comes from config/pricing, which you
   edit in admin-pricing.html. On 11 Oct, set the product price to 99 there.

   To move the deadline, change SWITCH_AT and FIRST_DAY under SETTINGS — nothing
   else. To end the launch price early, set SWITCH_AT to a date in the past.

   Hooks a page can carry:
     <span data-lp>Rs 99</span>               shows Rs 49 until the switch
     <span data-lp-note="inline" hidden>      deadline note, filled in and shown
     data-lp-note also takes "tag" and "popup": same words, different spacing

   No Firestore read, no network call, no storage.
============================================================================ */
(function () {
  'use strict';

  /* ---- SETTINGS ---------------------------------------------------------- */
  var INTRO     = 49;                                           // launch price
  var REGULAR   = 99;                                           // price from the switch
  var SWITCH_AT = Date.parse('2026-10-11T00:00:00+05:30');      // first moment of Rs 99 (IST)
  var FIRST_DAY = '11 Oct';                                     // how that date is written in the note
  /* ------------------------------------------------------------------------ */

  var left = SWITCH_AT - Date.now();
  if (!(left > 0)) return;                    // switch has passed: pages already say Rs 99

  var RUPEE = '\u20B9';
  var days  = Math.ceil(left / 86400000);     // counts today, so 10 Oct itself reads "last day"
  var BIG   = days <= 1 ? 'Last day at ' + RUPEE + INTRO : days + ' days left';
  var SMALL = days <= 1 ? RUPEE + REGULAR + ' from tomorrow'
                        : 'at ' + RUPEE + INTRO + ' \u00B7 ' + RUPEE + REGULAR + ' from ' + FIRST_DAY;

  var CSS =
    /* shared: solid red, white text */
    '.lp-n{box-sizing:border-box;max-width:100%;background:linear-gradient(135deg,#DC2626,#B91C1C);' +
      'color:#fff;border-radius:10px;font-weight:700;line-height:1.3;text-decoration:none;' +
      'box-shadow:0 3px 10px rgba(185,28,28,.28);}' +
    '.lp-n .lp-b{font-weight:800;white-space:nowrap;}' +
    '.lp-n .lp-s{font-weight:600;opacity:.96;}' +
    /* inside a sentence (price banner on the mock pages) and under the homepage card price */
    '.lp-n-inline,.lp-n-tag{display:inline-block;padding:.28rem .8rem;font-size:1.02em;}' +
    '.lp-n-inline{margin:.3rem 0;}' +
    '.lp-n-tag{margin:.5rem 0 0;}' +
    '.lp-n-inline .lp-b,.lp-n-tag .lp-b{font-size:1.14em;margin-right:.35em;}' +
    /* promo popup: a full-width block with a large first line, gently pulsing */
    '.lp-n-popup{display:block;margin:-.15rem 0 .95rem;padding:.6rem .8rem .65rem;border-radius:12px;' +
      'text-align:center;box-shadow:0 6px 18px rgba(220,38,38,.38);animation:lpPulse 1.7s ease-in-out infinite;}' +
    ".lp-n-popup .lp-b{display:block;font-family:'Baloo 2','Rajdhani',sans-serif;font-size:1.75rem;line-height:1.1;}" +
    '.lp-n-popup .lp-s{display:block;font-size:1.02rem;margin-top:.12rem;letter-spacing:.2px;}' +
    '@keyframes lpPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.035)}}' +
    '@media(prefers-reduced-motion:reduce){.lp-n-popup{animation:none}}';

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
    small.textContent = SMALL;
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
})();
