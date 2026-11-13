/* TSSC-ALLUP-V1 (2026-11-13) — "Upgrade to the All Mocks Pass" strip for pass holders.

   Shown on the mock list pages to a signed-in student who already holds 1-4 mock
   series but not everything. It names the price THEY pay — the difference, read
   from config/pricing: p-upgrade-all-1 (holds 1 series) and p-upgrade-all-2 (holds 2).
   Holders of 3 or more see nothing unless a p-upgrade-all-3 product is added. Tapping it opens the exam's main mock page
   with ?pass=all, where the buy popup leads with that upgrade and the checkout
   re-checks the holdings before any money moves.

   No Firestore read here: holdings come from the map the mock page already cached
   this session (tssc_ent_v2_<uid>). Free users and All-Mocks holders see nothing.
   Untick Live on the two products in admin-pricing and the strip disappears.
   Dismissing it hides it for the rest of the browser session. */
(function () {
  'use strict';
  var SERIES  = ['ssc-cgl-mocks', 'ssc-chsl-mocks', 'ssc-gd-mocks', 'ssc-mts-mocks', 'rrb-ntpc-mocks'];
  var DISMISS = 'tssc_allup_dismissed';
  var RUPEE   = '₹';

  try { if (sessionStorage.getItem(DISMISS)) return; } catch (e) {}
  if (/[?&]pass=all(&|$)/.test(location.search)) return;          // already here for it

  function uid() {
    try { var u = JSON.parse(localStorage.getItem('tssc_user') || 'null'); return (u && u.uid) || ''; }
    catch (e) { return ''; }
  }
  /* number of series held: 0-5, or null while the page has not read it yet */
  function held() {
    var id = uid();
    if (!id) return 0;
    try {
      var o = JSON.parse(sessionStorage.getItem('tssc_ent_v2_' + id) || 'null');
      if (!o || !o.m) return null;
      var n = 0;
      for (var i = 0; i < SERIES.length; i++) if (o.m[SERIES[i]] === true) n++;
      return n;
    } catch (e) { return null; }
  }
  function mainPage() {
    var p = location.pathname;
    if (/rrb-ntpc/.test(p)) return 'rrb-ntpc-mock-test.html';
    if (/ssc-mts/.test(p))  return 'ssc-mts-mock-test.html';
    if (/ssc-gd/.test(p))   return 'ssc-gd-mock-test.html';
    if (/ssc-chsl/.test(p)) return 'ssc-chsl-mock-test.html';
    return 'ssc-cgl-mock-test.html';
  }

  function show(n, price) {
    if (document.getElementById('tsscAllUp')) return;
    var anchor = document.querySelector('.search-row');
    if (!anchor || !anchor.parentNode) return;

    var css = document.createElement('style');
    css.textContent =
      '#tsscAllUp{position:relative;display:flex;align-items:center;gap:.7rem;flex-wrap:wrap;margin:0 0 1rem;' +
      'padding:.75rem 2.4rem .75rem .9rem;border-radius:14px;color:#fff;font-family:\'Rajdhani\',sans-serif;' +
      'background:linear-gradient(135deg,#1E1B4B,#4C1D95 55%,#9D174D);box-shadow:0 6px 18px rgba(76,29,149,.25);}' +
      '#tsscAllUp .au-t{flex:1 1 220px;min-width:0;font-weight:600;font-size:.95rem;line-height:1.35;color:#E9D5FF;}' +
      '#tsscAllUp .au-t b{display:block;font-family:\'Baloo 2\',\'Rajdhani\',sans-serif;font-weight:800;font-size:1.08rem;color:#fff;}' +
      '#tsscAllUp .au-t i{font-style:normal;color:#FDE68A;font-weight:700;}' +
      '#tsscAllUp .au-go{flex:none;text-decoration:none;background:#FDE68A;color:#4C1D95;border-radius:10px;' +
      'padding:.5rem .95rem;font-weight:800;font-size:.95rem;white-space:nowrap;}' +
      '#tsscAllUp .au-go:hover{background:#FCD34D;}' +
      '#tsscAllUp .au-x{position:absolute;top:6px;right:8px;width:26px;height:26px;border:0;border-radius:100px;' +
      'background:rgba(255,255,255,.18);color:#fff;font-size:1rem;line-height:1;cursor:pointer;}' +
      '#tsscAllUp .au-x:hover{background:rgba(255,255,255,.34);}';
    document.head.appendChild(css);

    var bar = document.createElement('div');
    bar.id = 'tsscAllUp';
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', 'Upgrade to the All Mocks Pass');

    var t = document.createElement('div'); t.className = 'au-t';
    var h = document.createElement('b');
    h.textContent = '⭐ Upgrade to the All Mocks Pass for just ' + RUPEE + price + ' more';
    t.appendChild(h);
    t.appendChild(document.createTextNode(
      'You already hold ' + (n === 1 ? 'a mock pass' : n + ' mock passes') + ', so you pay only the difference. '));
    var em = document.createElement('i');
    em.textContent = 'Every SSC CGL, CHSL, GD, MTS and RRB NTPC mock + every new series added, for 1 year.';
    t.appendChild(em);

    var go = document.createElement('a'); go.className = 'au-go';
    go.href = 'https://trickyssc.com/' + mainPage() + '?pass=all';
    go.textContent = 'Upgrade for ' + RUPEE + price + ' →';

    var x = document.createElement('button'); x.className = 'au-x'; x.type = 'button';
    x.setAttribute('aria-label', 'Hide this'); x.textContent = '×';
    x.addEventListener('click', function () {
      try { sessionStorage.setItem(DISMISS, '1'); } catch (e) {}
      if (bar.parentNode) bar.parentNode.removeChild(bar);
    });

    bar.appendChild(t); bar.appendChild(go); bar.appendChild(x);
    anchor.parentNode.insertBefore(bar, anchor);
  }

  function decide(n) {
    if (!(n >= 1 && n < SERIES.length)) return;                    // holds nothing, or everything
    var P = window.TSSC_PRICING;
    if (!P || typeof P.load !== 'function') return;
    P.load().then(function (cat) {
      if (!cat || cat.fallback) return;
      var id = 'p-upgrade-all-' + Math.min(n, 3), p = null;
      for (var i = 0; i < (cat.products || []).length; i++)
        if (cat.products[i].id === id && cat.products[i].live !== false) p = cat.products[i];
      if (p && p.price > 0) show(n, p.price);
    }, function () {});
  }

  var tries = 0;
  (function wait() {
    var n = held();
    if (n === null) { if (++tries < 12) setTimeout(wait, 1500); return; }   // page still reading the pass
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { decide(n); });
    else decide(n);
  })();
})();
