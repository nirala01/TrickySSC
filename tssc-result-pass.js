/* TSSC-RESULTPASS-V1 (2026-11-14) — "Pick your pass" popup shown right after a FREE test is submitted.

   Replaces the mock-plans block that used to sit under the result on previous-year papers and
   chapter tests. The result screen now looks the same as on a paid mock; the plans come up once,
   as a popup over it, with a bold "Go to results" button that closes it.

   Who sees it
     - previous-year papers, chapter tests, PYQ chapter tests: anyone who does not hold every mock series
     - mocks: only when the student does NOT hold that mock's series, i.e. it was one of the free mocks
       (a paid mock can only be opened by a pass holder, who never sees this)
     - at most once per SHOW_EVERY_DAYS per browser (localStorage), whichever test it follows

   What it shows
     Same plans and links as the home page "Pick your pass" popup. A series the student already holds is
     never offered; a pass holder sees the All Mocks Pass as an upgrade at the difference price.
     Prices here are display only — the mock pages charge from config/pricing.

   Called by the test engines:  window.tsscResultPass({isMock, exam, readEnt})
     readEnt — the engine's own entitlement reader, resolving to {signedIn, m}. Fail-open: any error
     here simply means no popup, never a blocked result. */
(function () {
  'use strict';
  var SHOW_EVERY_DAYS = 1;                 // 1 = once a day. Raise it to show less often.
  var SEEN = 'tssc_rp_seen';
  var H = 'https://trickyssc.com/';
  var S5 = ['ssc-cgl-mocks', 'ssc-chsl-mocks', 'ssc-gd-mocks', 'ssc-mts-mocks', 'rrb-ntpc-mocks'];
  var R = '\u20B9';

  function seriesOf(exam) {
    var e = String(exam || '').toLowerCase();
    if (/ntpc/.test(e)) return 'rrb-ntpc-mocks';
    if (/mts/.test(e))  return 'ssc-mts-mocks';
    if (/gd/.test(e))   return 'ssc-gd-mocks';
    if (/chsl/.test(e)) return 'ssc-chsl-mocks';
    if (/cgl/.test(e))  return 'ssc-cgl-mocks';
    return '';
  }
  function seenRecently() {
    try {
      var t = parseInt(localStorage.getItem(SEEN) || '0', 10);
      return !!t && (Date.now() - t) < SHOW_EVERY_DAYS * 86400000;
    } catch (e) { return false; }
  }
  function markSeen() { try { localStorage.setItem(SEEN, String(Date.now())); } catch (e) {} }

  function readEntitlement(readEnt) {
    return new Promise(function (resolve) {
      var done = false;
      function fin(m) { if (!done) { done = true; resolve(m || null); } }
      setTimeout(function () { fin(null); }, 3000);
      try {
        Promise.resolve(typeof readEnt === 'function' ? readEnt() : null)
          .then(function (r) { fin(r && r.m); }, function () { fin(null); });
      } catch (e) { fin(null); }
    });
  }

  var CSS =
    '#tsscRP{position:fixed;inset:0;z-index:99998;display:flex;align-items:center;justify-content:center;padding:12px;' +
      'background:rgba(15,23,42,.72);font-family:\'Rajdhani\',system-ui,sans-serif;animation:tsscRPin .2s ease-out;}' +
    '@keyframes tsscRPin{from{opacity:0}to{opacity:1}}' +
    '#tsscRP *{box-sizing:border-box;font-style:normal;}' +
    '#tsscRP .rp-box{width:100%;max-width:410px;max-height:94vh;display:flex;flex-direction:column;background:#fff;' +
      'border-radius:20px;overflow:hidden;color:#0F172A;box-shadow:0 20px 50px rgba(0,0,0,.35);}' +
    '#tsscRP .rp-scroll{overflow-y:auto;padding:14px 14px 10px;display:flex;flex-direction:column;gap:9px;}' +
    '#tsscRP .rp-head{display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;}' +
    '#tsscRP .rp-done{display:inline-flex;align-items:center;gap:6px;background:#DCFCE7;color:#166534;border-radius:100px;' +
      'padding:4px 12px;font-weight:700;font-size:13px;letter-spacing:.06em;}' +
    '#tsscRP h2{margin:4px 0 0;font-family:\'Rajdhani\',sans-serif;font-weight:700;font-size:28px;line-height:1.1;color:#0F172A;}' +
    '#tsscRP h2 span{color:#C2410C;}' +
    '#tsscRP .rp-sub{margin:0;font-size:15px;font-weight:500;line-height:1.3;color:#475569;}' +
    '#tsscRP a{text-decoration:none;color:#0F172A;}' +
    '#tsscRP [hidden]{display:none!important;}' +
    '#tsscRP .rp-all{display:flex;align-items:center;gap:12px;background:#FFF7ED;border:2px solid #C2410C;border-radius:14px;padding:12px;}' +
    '#tsscRP .rp-who{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px;}' +
    '#tsscRP .rp-tag{align-self:flex-start;background:#C2410C;color:#fff;border-radius:100px;padding:2px 10px;font-weight:700;' +
      'font-size:12px;letter-spacing:.06em;}' +
    '#tsscRP .rp-nm{font-weight:700;font-size:19px;line-height:1.15;}' +
    '#tsscRP .rp-ct{font-size:13px;font-weight:500;line-height:1.3;color:#475569;}' +
    '#tsscRP .rp-up{font-size:14px;font-weight:600;line-height:1.3;color:#9A3412;}' +
    '#tsscRP .rp-pr{flex:none;display:flex;flex-direction:column;align-items:flex-end;gap:2px;}' +
    '#tsscRP .rp-was{font-size:14px;font-weight:500;color:#64748B;text-decoration:line-through;}' +
    '#tsscRP .rp-now{font-weight:700;font-size:30px;line-height:1;color:#15803D;}' +
    '#tsscRP .rp-sv{background:#15803D;color:#fff;border-radius:6px;padding:1px 6px;font-weight:700;font-size:12px;}' +
    '#tsscRP .rp-lbl{font-weight:700;font-size:14px;letter-spacing:.06em;color:#475569;}' +
    '#tsscRP .rp-cbs{display:flex;flex-direction:column;gap:8px;}' +
    '#tsscRP .rp-cb{display:flex;align-items:center;gap:10px;min-height:48px;border:1px solid #CBD5E1;border-radius:12px;padding:6px 12px;}' +
    '#tsscRP .rp-cb .rp-nm{font-size:17px;line-height:1.2;}' +
    '#tsscRP .rp-cb .rp-now{font-size:22px;}' +
    '#tsscRP .rp-sgs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;}' +
    '#tsscRP .rp-sg{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:60px;border-radius:12px;' +
      'padding:6px 4px;text-align:center;}' +
    '#tsscRP .rp-sg b{font-weight:700;font-size:15px;}' +
    '#tsscRP .rp-sg small{font-size:13px;font-weight:500;}' +
    '#tsscRP .rp-sg i{font-weight:700;font-size:18px;line-height:1.1;}' +
    '#tsscRP .rp-sg.is-addon i{font-size:13px;}' +
    '#tsscRP .rp-sg.cgl{background:#FFEDD5;color:#7C2D12;} #tsscRP .rp-sg.cgl b{color:#9A3412;}' +
    '#tsscRP .rp-sg.chsl{background:#E0E7FF;color:#312E81;} #tsscRP .rp-sg.chsl b{color:#3730A3;}' +
    '#tsscRP .rp-sg.gd{background:#DCFCE7;color:#14532D;} #tsscRP .rp-sg.gd b{color:#166534;}' +
    '#tsscRP .rp-sg.mts{background:#CCFBF1;color:#134E4A;} #tsscRP .rp-sg.mts b{color:#115E59;}' +
    '#tsscRP .rp-sg.ntpc{background:#DBEAFE;color:#1E3A8A;} #tsscRP .rp-sg.ntpc b{color:#1E40AF;}' +
    '#tsscRP .rp-band{margin:0;text-align:center;font-size:14px;font-weight:600;color:#166534;}' +
    '#tsscRP .rp-foot{flex:none;padding:10px 16px 14px;background:#fff;border-top:1px solid #E2E8F0;}' +
    '#tsscRP .rp-go{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;min-height:54px;border:0;border-radius:14px;' +
      'background:#0B3B8C;color:#fff;font-family:\'Rajdhani\',sans-serif;font-weight:700;font-size:21px;letter-spacing:.02em;cursor:pointer;}' +
    '#tsscRP .rp-go:hover{background:#0A2F70;}' +
    '#tsscRP .rp-go:focus-visible{outline:3px solid #F59E0B;outline-offset:2px;}' +
    '@media(max-width:360px){#tsscRP h2{font-size:25px}#tsscRP .rp-now{font-size:26px}#tsscRP .rp-cb .rp-nm{font-size:16px}}' +
    '@media(prefers-reduced-motion:reduce){#tsscRP{animation:none}}';

  function combo(grants, href, name, count) {
    return '<a class="rp-cb" data-rp-grants="' + grants + '" href="' + H + href + '">' +
      '<span class="rp-who"><span class="rp-nm">' + name + '</span><span class="rp-ct">' + count + '</span></span>' +
      '<span class="rp-was">' + R + '98</span><span class="rp-now">' + R + '79</span></a>';
  }
  function single(cls, grants, addonIf, href, name, count) {
    return '<a class="rp-sg ' + cls + '" data-rp-grants="' + grants + '"' + (addonIf ? ' data-rp-addon-if="' + addonIf + '"' : '') +
      ' href="' + H + href + '"><b>' + name + '</b><small>' + count + '</small><i>' + R + '49</i></a>';
  }
  var HTML =
    '<div class="rp-box"><div class="rp-scroll">' +
      '<div class="rp-head">' +
        '<span class="rp-done"><svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
          'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"></path></svg>TEST SUBMITTED</span>' +
        '<h2 id="tsscRPh">Pick your <span>pass</span></h2>' +
        '<p class="rp-sub">Full mock tests for a year. Every new mock released in the year is included.</p>' +
      '</div>' +
      '<a class="rp-all" href="' + H + 'ssc-chsl-mock-test.html?pass=all">' +
        '<span class="rp-who"><span class="rp-tag">ALL ACCESS PASS</span>' +
          '<span class="rp-nm">All Mocks Pass \u00B7 1 year</span>' +
          '<span class="rp-ct">SSC CGL + CHSL + GD + MTS + RRB NTPC \u00B7 360 mocks</span>' +
          '<span class="rp-up">New mock series join automatically</span></span>' +
        '<span class="rp-pr"><span class="rp-was">' + R + '245</span><span class="rp-now">' + R + '99</span>' +
          '<span class="rp-sv">SAVE ' + R + '146</span></span>' +
      '</a>' +
      '<div class="rp-lbl" data-rp-lbl="combo">COMBO OFFERS \u00B7 2 EXAMS</div>' +
      '<div class="rp-cbs" data-rp-group="combo">' +
        combo('ssc-cgl-mocks ssc-chsl-mocks', 'ssc-chsl-mock-test.html?combo=1', 'SSC CGL + SSC CHSL', '180 mocks \u00B7 100 CGL + 80 CHSL') +
        combo('ssc-chsl-mocks ssc-gd-mocks', 'ssc-gd-mock-test.html?combo=1', 'SSC CHSL + SSC GD', '140 mocks \u00B7 80 CHSL + 60 GD') +
        combo('ssc-mts-mocks ssc-gd-mocks', 'ssc-mts-mock-test.html?combo=1', 'SSC MTS + SSC GD', '120 mocks \u00B7 60 MTS + 60 GD') +
      '</div>' +
      '<div class="rp-lbl" data-rp-lbl="single">SINGLE EXAM PASS \u00B7 1 YEAR</div>' +
      '<div class="rp-sgs" data-rp-group="single">' +
        single('cgl', 'ssc-cgl-mocks', 'ssc-chsl-mocks', 'ssc-cgl-mock-test.html', 'SSC CGL', '100 mocks') +
        single('chsl', 'ssc-chsl-mocks', 'ssc-cgl-mocks', 'ssc-chsl-mock-test.html', 'SSC CHSL', '80 mocks') +
        single('gd', 'ssc-gd-mocks', 'ssc-chsl-mocks', 'ssc-gd-mock-test.html', 'SSC GD', '60 mocks') +
        single('mts', 'ssc-mts-mocks', '', 'ssc-mts-mock-test.html', 'SSC MTS', '60 mocks') +
        single('ntpc', 'rrb-ntpc-mocks', '', 'rrb-ntpc-mock-test.html', 'RRB NTPC', '60 mocks') +
      '</div>' +
      '<p class="rp-band">Hindi and English \u00B7 Sectional timing</p>' +
    '</div>' +
    '<div class="rp-foot"><button type="button" class="rp-go">Go to results' +
      '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" ' +
      'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"></path></svg></button></div></div>';

  function build(m) {
    function owns(k) { return !!(m && m[k] === true); }
    var box = document.createElement('div');
    box.id = 'tsscRP';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-labelledby', 'tsscRPh');
    box.innerHTML = HTML;

    var shown = 0, held = 0, i;
    for (i = 0; i < S5.length; i++) if (owns(S5[i])) held++;

    /* All Mocks Pass: Rs 99 with no pass; the difference for a holder of 1 or 2 series
       (Rs 49 / Rs 19, same as the home page popup); hidden for 3 or more. */
    var all = box.querySelector('.rp-all');
    if (held >= 3) { all.hidden = true; }
    else {
      if (held > 0) {
        var set = function (c, t) { var x = all.querySelector(c); if (x) x.textContent = t; };
        set('.rp-tag', 'UPGRADE FOR YOU');
        set('.rp-nm', 'Upgrade to All Mocks Pass');
        set('.rp-ct', 'You already hold ' + (held === 1 ? 'a mock pass' : held + ' mock passes') + ' \u2014 pay only the difference');
        set('.rp-up', 'Every SSC and RRB NTPC mock + every new series, for 1 year');
        set('.rp-was', R + '99'); set('.rp-now', '+' + R + [49, 19][held - 1]); set('.rp-sv', 'UPGRADE');
      }
      shown++;
    }
    var rows = box.querySelectorAll('[data-rp-grants]');
    for (i = 0; i < rows.length; i++) {
      var el = rows[i], keys = el.getAttribute('data-rp-grants').split(' '), hit = false, q;
      for (q = 0; q < keys.length; q++) if (owns(keys[q])) hit = true;
      if (hit) { el.hidden = true; continue; }
      shown++;
      var addIf = el.getAttribute('data-rp-addon-if');
      if (addIf && owns(addIf)) {
        el.classList.add('is-addon');
        var p = el.querySelector('i'); if (p) p.textContent = 'Add-on price';
        el.href = el.href + (el.href.indexOf('?') === -1 ? '?' : '&') + 'upgrade=1';
      }
    }
    if (!shown) return null;                                  // holds everything: nothing to offer
    ['combo', 'single'].forEach(function (g) {
      var grp = box.querySelector('[data-rp-group="' + g + '"]'), lbl = box.querySelector('[data-rp-lbl="' + g + '"]');
      var any = false, els = grp.children, k;
      for (k = 0; k < els.length; k++) if (!els[k].hidden) any = true;
      if (!any) { grp.hidden = true; if (lbl) lbl.hidden = true; }
    });
    return box;
  }

  function open(box) {
    if (!document.getElementById('tsscRPcss')) {
      var st = document.createElement('style'); st.id = 'tsscRPcss'; st.textContent = CSS; document.head.appendChild(st);
    }
    var prevOverflow = document.body.style.overflow;
    function close() {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = prevOverflow;
      if (box.parentNode) box.parentNode.removeChild(box);
      try { window.scrollTo(0, 0); } catch (e) {}
    }
    function onKey(e) { if (e.key === 'Escape') close(); }
    box.querySelector('.rp-go').addEventListener('click', close);
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.addEventListener('keydown', onKey);
    document.body.appendChild(box);
    document.body.style.overflow = 'hidden';
    markSeen();
    try { box.querySelector('.rp-go').focus({ preventScroll: true }); } catch (e) {}
  }

  window.tsscResultPass = function (opts) {
    try {
      opts = opts || {};
      if (document.getElementById('tsscRP') || seenRecently()) return;
      readEntitlement(opts.readEnt).then(function (m) {
        try {
          if (document.getElementById('tsscRP') || seenRecently()) return;
          if (opts.isMock) {
            var s = seriesOf(opts.exam);
            if (s && m && m[s] === true) return;              // holds this mock's series: not a free test for them
          }
          var box = build(m);
          if (box) open(box);
        } catch (e) { try { console.warn('[result-pass]', e); } catch (_) {} }
      });
    } catch (e) {}
  };
})();
