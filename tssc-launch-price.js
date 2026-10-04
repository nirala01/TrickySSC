/* ============================================================================
   tssc-launch-price.js  —  TSSC-LAUNCHPRICE-V1

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
  var NOTE  = days <= 1
    ? 'Last day at ' + RUPEE + INTRO + '. ' + RUPEE + REGULAR + ' from tomorrow.'
    : days + ' days left at ' + RUPEE + INTRO + '. ' + RUPEE + REGULAR + ' from ' + FIRST_DAY + '.';

  var CSS =
    '.lp-n{display:inline-block;box-sizing:border-box;max-width:100%;background:#FEF2F2;' +
      'border:1px solid #FECACA;color:#B91C1C;border-radius:12px;padding:.12rem .7rem;' +
      'font-weight:700;font-size:.92em;line-height:1.5;text-decoration:none;}' +
    '.lp-n-inline{margin:.2rem 0;}' +
    '.lp-n-tag{margin:.45rem 0 0;}' +
    '.lp-n-popup{margin:-.3rem 0 .85rem;font-size:.9rem;}';

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
    el.textContent = '\u23F3 ' + NOTE;
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
