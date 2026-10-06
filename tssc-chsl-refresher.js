/* tssc-chsl-refresher.js — TSSC-CHSLREF-V1 (2026-10-06)
   ------------------------------------------------------------------------
   ONE place for the SSC CHSL "Refresher" mocks — Mock 31–40 of each tier.
   Loaded as a plain <script> in the <head> of ssc-chsl-mock-test.html and
   ssc-chsl-tier-2-mock-test.html (and optionally index.html /
   ssc-chsl-2026.html) so every date on the site comes from this file.

   TO CHANGE A DATE: edit `opensAt` (and `examLabel`) below, upload this
   ONE file. Nothing else needs touching.

   opensAt  — ISO datetime (IST) from which the refresher cards become
              attemptable. Before it, a card stays locked even if the mock
              is already uploaded/published, with the pill "Opens <date>".
              null = exam date not announced yet: cards stay locked and the
              copy says "opens 20 days before the exam" until you fill it in.
   examLabel — shown in the notes ("20 days before the Tier I exam (…)").

   Rule of thumb: opensAt = first exam date minus 20 days. The CHSL Tier I
   2026 window is 30 Nov – 31 Dec, so Tier I opens 10 Nov 2026.
   ------------------------------------------------------------------------ */
(function () {
  window.TSSC_CHSL_REFRESHER = {
    tier1: {
      from: 31, to: 40,
      opensAt:   '2026-11-10T00:00:00+05:30',
      examLabel: '30 Nov \u2013 31 Dec 2026',
      caLabel:   'current affairs updated to November 2026'
    },
    tier2: {
      from: 31, to: 40,
      opensAt:   null,                       /* fill in once SSC announces the Tier II date */
      examLabel: 'date awaited from SSC',
      caLabel:   'current affairs updated to the exam month'
    }
  };

  var MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  function fmt(d, withYear) {
    /* d is a Date; print in IST so the day never shifts on a foreign clock */
    var ist = new Date(d.getTime() + (330 + d.getTimezoneOffset()) * 60000);
    return ist.getDate() + ' ' + MONTHS[ist.getMonth()] + (withYear ? ' ' + ist.getFullYear() : '');
  }

  /* State for one tier: { cfg, open, opensAt(Date|null), daysLeft } */
  function state(tier) {
    var cfg = window.TSSC_CHSL_REFRESHER[tier];
    if (!cfg) return null;
    var at = cfg.opensAt ? new Date(cfg.opensAt) : null;
    var now = Date.now();
    var open = !!(at && now >= at.getTime());
    var daysLeft = at && !open ? Math.ceil((at.getTime() - now) / 86400000) : 0;
    return { cfg: cfg, open: open, opensAt: at, daysLeft: daysLeft };
  }
  window.tsscRefState = state;

  var TIER_NAME = { tier1: 'Tier I', tier2: 'Tier II' };

  /* Text for the three display modes used in the pages:
       short — the pill on a locked card          "📅 Opens 10 Nov"
       date  — inline date inside a sentence       "10 Nov 2026"
       long  — the status line under the banner    "Opens 10 Nov 2026 · 35 days to go" */
  function text(tier, mode) {
    var st = state(tier); if (!st) return '';
    var tn = TIER_NAME[tier] || '';
    if (mode === 'short') {
      if (st.open) return '\u2705 Open now';
      return st.opensAt ? '\uD83D\uDCC5 Opens ' + fmt(st.opensAt, false)
                        : '\uD83D\uDCC5 20 days before exam';
    }
    if (mode === 'date') {
      return st.opensAt ? fmt(st.opensAt, true) : '20 days before the ' + tn + ' exam';
    }
    /* long */
    if (st.open) return 'Open now \u2014 attempt them before your exam date.';
    if (st.opensAt) {
      return 'Opens ' + fmt(st.opensAt, true) + ' \u2014 20 days before the ' + tn + ' exam (' +
             st.cfg.examLabel + ') \u00B7 ' + st.daysLeft + ' day' + (st.daysLeft === 1 ? '' : 's') + ' to go';
    }
    return 'Opens 20 days before the ' + tn + ' exam \u2014 ' + st.cfg.examLabel + '. The date is set here the day SSC announces it.';
  }
  window.tsscRefText = text;

  /* Paint every [data-chsl-ref="tier1|tier2"] element; mode from data-chsl-ref-mode. */
  function paint() {
    var els = document.querySelectorAll('[data-chsl-ref]');
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      var t = el.getAttribute('data-chsl-ref') || 'tier1';
      var m = el.getAttribute('data-chsl-ref-mode') || 'long';
      var s = text(t, m);
      if (s) el.textContent = s;
    }
  }
  window.tsscRefPaint = paint;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', paint);
  else paint();
})();
