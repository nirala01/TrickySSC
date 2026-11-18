/* TSSC-PAID98-V1 (2026-11-17) — has this student already paid Rs 98 or more in all?

   Such a student (for example two passes bought separately at Rs 49 each) is not shown any
   upgrade popup or strip on the website, and the mock pages do not sell them the upgrade.
   Same sum as the Android app's upgrade rule: payments with status "paid", test payments left out.

     window.tsscPaid98()  ->  Promise<boolean>   (false when signed out or when it cannot be read)

   One read of the student's own payments (the read "My orders" does). A yes is remembered on
   this device; a no is remembered for 10 minutes of the browser session. */
(function () {
  'use strict';
  if (window.tsscPaid98) return;
  var LIMIT = 98, FB = 'https://www.gstatic.com/firebasejs/10.7.1/';
  var CFG = { apiKey: 'AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA', authDomain: 'trickyssc-17bb3.firebaseapp.com', projectId: 'trickyssc-17bb3',
    storageBucket: 'trickyssc-17bb3.firebasestorage.app', messagingSenderId: '450627057220', appId: '1:450627057220:web:366267bf437d94f20c6e11' };
  function uid() { try { var u = JSON.parse(localStorage.getItem('tssc_user') || 'null'); return (u && u.uid) || ''; } catch (e) { return ''; } }
  function cached(id) {
    try {
      if (localStorage.getItem('tssc_p98_' + id) === '1') return true;
      var o = JSON.parse(sessionStorage.getItem('tssc_p98_' + id) || 'null');
      if (o && Date.now() - o.ts < 600000) return false;
    } catch (e) {}
    return null;
  }
  function remember(id, yes) {
    try {
      if (yes) localStorage.setItem('tssc_p98_' + id, '1');
      else sessionStorage.setItem('tssc_p98_' + id, JSON.stringify({ ts: Date.now() }));
    } catch (e) {}
  }
  var _p = null, _for = '';
  window.tsscPaid98 = function () {
    if (!window.TSSC_PAID98_ON) return Promise.resolve(false);   // 2026-11-18: off — Rs 98+ students see the normal offers
    var id = uid();
    if (!id) return Promise.resolve(false);
    var c = cached(id);
    if (c !== null) return Promise.resolve(c);
    if (_p && _for === id) return _p;
    _for = id;
    _p = new Promise(function (resolve) {
      var done = false;
      function fin(v) { if (!done) { done = true; resolve(v); } }
      setTimeout(function () { fin(false); }, 7000);
      var imp = new Function('u', 'return import(u)');
      Promise.all([imp(FB + 'firebase-app.js'), imp(FB + 'firebase-auth.js'), imp(FB + 'firebase-firestore.js')]).then(function (x) {
        var app = x[0].getApps().length ? x[0].getApps()[0] : x[0].initializeApp(CFG), auth = x[1].getAuth(app), db = x[2].getFirestore(app);
        var off = x[1].onAuthStateChanged(auth, function (fu) {
          try { off(); } catch (e) {}
          if (!fu || fu.uid !== id) { fin(false); return; }
          x[2].getDocs(x[2].query(x[2].collection(db, 'payments'), x[2].where('uid', '==', id))).then(function (snap) {
            var total = 0;
            snap.forEach(function (d) {
              var p = d.data() || {}, n = Number(p.amount);
              if (p.status === 'paid' && p.mode !== 'test' && isFinite(n) && n > 0 && n < 100000) total += n;
            });
            remember(id, total >= LIMIT);
            fin(total >= LIMIT);
          }, function () { fin(false); });
        });
      }, function () { fin(false); });
    });
    return _p;
  };
})();

/* Switch for the "Claim now" box on the mock pages. OFF (2026-11-18) until the trickyssc-play Worker
   and Google Play payments are set up; set to true then. */
window.TSSC_FREECLAIM_ON = false;
/* Switch for all Rs 98+ special handling (popups hidden, no upgrade sold). OFF 2026-11-18: those few
   students are handled by hand, everyone sees the normal offers. */
window.TSSC_PAID98_ON = false;

/* TSSC-FREECLAIM-V1 (2026-11-17) — "You are eligible for free Full Access — Claim now".
   Asks the trickyssc-play Worker (/upgrade-free, the same call the Android app makes). The Worker
   checks the paid total itself and opens every course; nothing is granted from the browser.

     window.tsscClaimFree(getIdToken)  ->  Promise<boolean>   true = full access is now on the account */
(function () {
  'use strict';
  if (window.tsscClaimFree) return;
  var API = 'https://trickyssc-play.nirala01.workers.dev';
  window.tsscClaimFree = function (getIdToken) {
    return Promise.resolve().then(getIdToken).then(function (idToken) {
      return fetch(API + '/upgrade-free', { method: 'POST', headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ idToken: idToken, platform: 'web' }) });
    }).then(function (r) { return r.json(); }).then(function (j) {
      if (!j || j.ok !== true) return false;
      try {
        localStorage.removeItem('tssc_ent_hint_v1');
        for (var i = sessionStorage.length - 1; i >= 0; i--) {
          var k = sessionStorage.key(i); if (k && k.indexOf('tssc_ent_v2_') === 0) sessionStorage.removeItem(k);
        }
      } catch (e) {}
      return true;
    }).catch(function () { return false; });
  };
})();
