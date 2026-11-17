/* TSSC-APPOFFERS-V1 — who sees which pass offer inside the app. Loaded by tssc-app.js (inner
   pages) and app.html. One rule set, used in two places:

     no pass bought        -> the student's exam pass, the All Mocks Pass, then the other exams
     1 or 2 series bought  -> only the All Mocks Pass at the difference price (TSSC-UPGRADEONLY-V1)
     3 or 4 series bought  -> nothing
     All Mocks Pass        -> nothing, anywhere

   Where it shows
     fill(room)   cards in the empty space under a short page
     openOnce()   the "Pick your pass" popup, once each time the app is opened

   The popup after a free test is the website's own (tssc-result-pass.js) and is not touched here.
   Ownership is read from Firestore (entitlements/<uid>), the same record the mock pages unlock from.
   Fail-closed: if ownership cannot be read, nothing is offered. */
(function () {
  'use strict';
  if (window.TSSC_APP_OFFERS) return;
  var CFG = { apiKey: 'AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA', authDomain: 'trickyssc-17bb3.firebaseapp.com', projectId: 'trickyssc-17bb3',
    storageBucket: 'trickyssc-17bb3.firebasestorage.app', messagingSenderId: '450627057220', appId: '1:450627057220:web:366267bf437d94f20c6e11' };
  var FB = 'https://www.gstatic.com/firebasejs/10.7.1/';
  var S5 = ['ssc-cgl-mocks', 'ssc-chsl-mocks', 'ssc-mts-mocks', 'ssc-gd-mocks', 'rrb-ntpc-mocks'];
  var EXAMS = [
    { k: 'cgl', name: 'SSC CGL', ic: '🎯', key: 'ssc-cgl-mocks', page: '/app-ssc-cgl-mock-test.html', c: '#EA580C', c2: '#FDA047', s: 'rgba(255,107,0,.25)', addonIf: 'ssc-chsl-mocks' },
    { k: 'chsl', name: 'SSC CHSL', ic: '📋', key: 'ssc-chsl-mocks', page: '/app-ssc-chsl-mock-test.html', c: '#0369A1', c2: '#38BDF8', s: 'rgba(14,165,233,.25)', addonIf: 'ssc-cgl-mocks' },
    { k: 'mts', name: 'SSC MTS', ic: '📝', key: 'ssc-mts-mocks', page: '/app-ssc-mts-mock-test.html', c: '#047857', c2: '#34D399', s: 'rgba(16,185,129,.25)', addonIf: '' },
    { k: 'gd', name: 'SSC GD', ic: '🛡️', key: 'ssc-gd-mocks', page: '/app-ssc-gd-mock-test.html', c: '#B91C1C', c2: '#F87171', s: 'rgba(239,68,68,.25)', addonIf: 'ssc-chsl-mocks' },
    { k: 'ntpc', name: 'RRB NTPC', ic: '🚆', key: 'rrb-ntpc-mocks', page: '/app-rrb-ntpc-mock-test.html', c: '#1E3FAE', c2: '#60A5FA', s: 'rgba(29,78,216,.25)', addonIf: '' }
  ];
  var UPGRADE_DIFF = [49, 20];             // All Mocks Pass for a holder of 1 / 2 series (same as the website popups)
  var R = '₹';

  function user() { try { var u = JSON.parse(localStorage.getItem('tssc_user') || 'null'); return u && u.uid ? u : null; } catch (e) { return null; } }
  function myExam() { try { return localStorage.getItem('tssc_app_exam') || ''; } catch (e) { return ''; } }
  function cached(uid, maxAge) {
    try { var o = JSON.parse(sessionStorage.getItem('tssc_ent_v2_' + uid) || 'null');
      return (o && o.m && (!maxAge || Date.now() - (o.ts || 0) < maxAge)) ? o.m : null; } catch (e) { return null; }
  }
  function active(g) {
    if (!g || g.active !== true) return false; var e = g.expiresAt; if (!e) return true;
    var ms = e.toDate ? e.toDate().getTime() : (e.seconds ? e.seconds * 1000 : Date.parse(e)); return !isFinite(ms) || ms > Date.now();
  }
  var _ent = null;
  /* resolves to {key:true|false} for the five series, or null when it cannot be known */
  function readEnt() {
    if (_ent) return _ent;
    var u = user(); if (!u) return Promise.resolve(null);
    var fresh = cached(u.uid, 5 * 60 * 1000); if (fresh) return Promise.resolve(fresh);
    _ent = new Promise(function (resolve) {
      var done = false; function fin(m) { if (!done) { done = true; resolve(m); } }
      setTimeout(function () { fin(cached(u.uid, 0)); }, 6000);
      var imp = new Function('u', 'return import(u)');
      Promise.all([imp(FB + 'firebase-app.js'), imp(FB + 'firebase-auth.js'), imp(FB + 'firebase-firestore.js')]).then(function (x) {
        var app = x[0].getApps().length ? x[0].getApps()[0] : x[0].initializeApp(CFG), auth = x[1].getAuth(app), db = x[2].getFirestore(app);
        var off = x[1].onAuthStateChanged(auth, function (fu) {
          try { off(); } catch (e) {}
          if (!fu) { fin(cached(u.uid, 0)); return; }
          x[2].getDoc(x[2].doc(db, 'entitlements', fu.uid)).then(function (snap) {
            var d = snap.exists() ? (snap.data() || {}) : {}, mods = d.modules || {}, all = active(d.allAccess) || active(mods['all-mocks']), m = {};
            S5.forEach(function (k) { m[k] = all || active(mods[k]); });
            try { sessionStorage.setItem('tssc_ent_v2_' + fu.uid, JSON.stringify({ ts: Date.now(), m: m })); } catch (e) {}
            fin(m);
          }, function () { fin(cached(u.uid, 0)); });
        });
      }, function () { fin(cached(u.uid, 0)); });
    });
    return _ent;
  }
  function loadScript(src, test) {
    return new Promise(function (res, rej) {
      if (test()) { res(); return; }
      var s = document.createElement('script'); s.src = src; s.onload = function () { res(); }; s.onerror = rej; document.head.appendChild(s);
    });
  }
  function pricing() {
    return loadScript('/tssc-pricing.js', function () { return !!window.TSSC_PRICING; }).then(function () { return window.TSSC_PRICING.load(); });
  }

  /* the offers for this student, best first: [{title, sub, price, was, href, c, c2, s, ic}] */
  function plan(m, cat) {
    var P = window.TSSC_PRICING, held = 0, out = [], mine = myExam();
    S5.forEach(function (k) { if (m[k] === true) held++; });
    if (held >= S5.length || held >= 3) return out;                                    // All Mocks Pass (or every series): nothing
    function cheapest(key, single) {
      var ps = P.productsGranting(cat, key).filter(function (p) {
        var all = (p.grants || []).indexOf('all-mocks') >= 0; return Number(p.price) > 0 && (single ? (!all && p.grants.length === 1) : all); });
      ps.sort(function (a, b) { return a.price - b.price; }); return ps[0] || null;
    }
    function years(p) { var d = Number(p.durationDays) || 365; return d >= 365 ? Math.round(d / 365) + ' year' : d + ' days'; }
    var mineX = null; EXAMS.forEach(function (x) { if (x.k === mine) mineX = x; });
    var allP = cheapest('all-mocks', false), allHref = ((mineX || EXAMS[0]).page) + '?pass=all', allCard = null;
    if (allP && held < 3) {
      allCard = held === 0
        ? { ic: '⭐', title: 'All Mocks Pass', sub: 'Every exam · valid ' + years(allP), price: R + allP.price, was: allP.mrp > allP.price ? R + allP.mrp : '', href: allHref }
        : { ic: '⭐', title: 'All Mocks upgrade', sub: 'Every exam · pay only the difference', price: '+' + R + UPGRADE_DIFF[held - 1], was: R + allP.price, href: allHref };
      allCard.c = '#4338CA'; allCard.c2 = '#818CF8'; allCard.s = 'rgba(79,70,229,.25)';
    }
    if (held > 0) return allCard ? [allCard] : out;                      // TSSC-UPGRADEONLY-V1
    var singles = [];
    EXAMS.slice().sort(function (a, b) { return (b.k === mine) - (a.k === mine); }).forEach(function (x) {
      if (m[x.key] === true) return;
      var p = cheapest(x.key, true); if (!p) return;
      var up = (held > 0 && x.addonIf && m[x.addonIf] === true && P.upgradeFor) ? P.upgradeFor(cat, x.key) : null;
      singles.push(up
        ? { ic: x.ic, title: 'Add ' + x.name + ' mocks', sub: 'Add-on price for pass holders', price: R + up.price, was: R + p.price, href: x.page + '?upgrade=1', c: x.c, c2: x.c2, s: x.s }
        : { ic: x.ic, title: x.name + ' Mock Pass', sub: 'Full mock series · valid ' + years(p), price: R + p.price, was: p.mrp > p.price ? R + p.mrp : '', href: '/app.html#p/' + x.k, c: x.c, c2: x.c2, s: x.s });
    });
    if (held === 0) { if (singles.length) out.push(singles.shift()); if (allCard) out.push(allCard); }
    else if (allCard) out.push(allCard);
    return out.concat(singles);
  }
  function card(o) {
    return '<a class="tsa-offer" href="' + o.href + '" style="--c:' + o.c + ';--c2:' + o.c2 + ';--s:' + o.s + '"><i>' + o.ic + '</i>' +
      '<div><b>' + o.title + '</b><small>' + o.sub + '</small></div><span>' + (o.was ? '<s>' + o.was + '</s>' : '') + o.price + '</span></a>';
  }
  /* cards for `room` px of empty space; resolves to an element or null */
  function fill(room) {
    return Promise.all([readEnt(), pricing()]).then(function (r) {
      var m = r[0], cat = r[1]; if (!m) return null;
      var list = plan(m, cat); if (!list.length) return null;
      var held = 0; S5.forEach(function (k) { if (m[k] === true) held++; });
      var n = Math.max(1, Math.floor((room - 40) / 73));
      var box = document.createElement('div'); box.className = 'tsa-offers';
      box.innerHTML = '<h4>' + (held ? 'Upgrades for you' : 'Unlock full mock tests') + '</h4>' + list.slice(0, n).map(card).join('');
      if (!held) return box;
      /* TSSC-PAID98-V1 — no upgrade cards for a student who has already paid Rs 98 or more */
      return loadScript('/tssc-paid98.js', function () { return !!window.tsscPaid98; }).then(function () { return window.tsscPaid98(); })
        .then(function (y) { return y ? null : box; }, function () { return box; });
    }).catch(function () { return null; });
  }
  /* the "Pick your pass" popup, once per opening of the app */
  function openOnce() {
    var KEY = 'tssc_app_offer_shown';
    try { if (sessionStorage.getItem(KEY)) return; } catch (e) { return; }
    if (!user()) return;
    Promise.all([readEnt(), loadScript('/tssc-result-pass.js', function () { return !!window.tsscPassPopup; })]).then(function (r) {
      var m = r[0]; if (!m || !window.tsscPassPopup) return;
      try { if (sessionStorage.getItem(KEY)) return; sessionStorage.setItem(KEY, '1'); } catch (e) { return; }
      var held = 0; S5.forEach(function (k) { if (m[k] === true) held++; });
      window.tsscPassPopup(m, { badge: held ? 'UPGRADES FOR YOU' : 'OFFER FOR YOU', button: 'Continue to app' });
    }).catch(function () {});
  }
  window.TSSC_APP_OFFERS = { readEnt: readEnt, fill: fill, openOnce: openOnce, plan: plan };
})();
