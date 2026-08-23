#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_mock_paywall.py  —  TrickySSC mock-list paywall patch  (TSSC-PAYWALL-V1)

Applies four changes to the SSC CGL mock listing pages:

  1. Re-attempt label fix.  `_applyPills()` is exposed as window.tsscApplyPills
     and re-run at the end of the Firestore availability pass, so a card that
     was statically `.locked` at auth time (and only unlocked a moment later)
     still picks up the "Re-attempt" label instead of being skipped.

  2. Premium lock button.  Every premium card gets a tappable lock pill beside
     the gold "Premium" badge.  It disappears — and the Premium badge turns
     green — once the signed-in user holds the entitlement.

  3. Missing tags backfilled.  Tier I 43-50 and ALL of Tier II had no
     Free/Premium badge at all.  Mock 1-4 of each tier get the Free badge,
     5-50 get Premium + lock.  Same rule both tiers.

  4. Buy popup + click gating.  Clicking a locked premium card (button or
     lock pill) opens an unlock popup instead of the language chooser.

Idempotent: re-running is a no-op.  Writes a .bak beside each page.

  python patch_mock_paywall.py --page mock-list.html --page ssc-cgl-mock-test.html
  python patch_mock_paywall.py --page mock-list.html --dry-run
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

MARKER = "TSSC-PAYWALL-V1"
FREE_UP_TO = 4  # mocks 1..4 free in BOTH tiers

# ─────────────────────────────────────────────────────────────────────────────
# 1. CSS
# ─────────────────────────────────────────────────────────────────────────────

CSS_ANCHOR = ("@media(prefers-reduced-motion:reduce)"
              "{.mc-paid-tag i,.mc-paid-tag span::after{animation:none;}}")

CSS_BLOCK = """
/* ===== premium lock (""" + MARKER + """) ===== */
.mc-locktag{display:none!important;align-items:center;gap:.24rem;margin-left:.32rem;
vertical-align:middle;border:none;cursor:pointer;font-family:'Rajdhani',sans-serif;
font-size:.68rem!important;font-weight:800;letter-spacing:.03em;padding:.2rem .55rem;
border-radius:100px;background:linear-gradient(135deg,#1E293B,#475569);color:#fff;
box-shadow:0 2px 8px rgba(15,23,42,.3),inset 0 1px 0 rgba(255,255,255,.18);
-webkit-tap-highlight-color:transparent;transition:filter .15s ease,transform .15s ease;}
.mc-locktag:hover{filter:brightness(1.2);transform:translateY(-1px);}
.mc-locktag i{font-style:normal;font-size:.76rem;line-height:1;}
/* owned: the lock disappears and the gold Premium pill goes green */
/* the lock appears ONLY once the paywall is enforcing, and only on a card
   this user hasn't bought. Before 25 Aug nobody sees it at all. */
body.tssc-enforce .mock-card.tssc-premium:not(.tssc-owned) .mc-locktag{display:inline-flex!important;}
.mock-card.tssc-owned .mc-paid-tag span{
background:linear-gradient(135deg,#059669,#34D399)!important;color:#fff!important;
text-shadow:none!important;
box-shadow:0 2px 8px rgba(5,150,105,.32),inset 0 1px 0 rgba(255,255,255,.35)!important;}
.mock-card.tssc-owned .mc-paid-tag span::after{display:none!important;}
.mock-card.tssc-owned .mc-paid-tag i{animation:none!important;}
/* while entitlement is still being read, don't flash a wrong state */
body:not(.tssc-ent-resolved) .mc-locktag{opacity:.55;pointer-events:none;}
/* unlock popup */
#mockBuyPop{display:none;position:fixed;inset:0;z-index:9998;background:rgba(15,23,42,.6);
align-items:center;justify-content:center;padding:1rem;backdrop-filter:blur(3px);}
#mockBuyPop .mbp-card{background:#fff;border-radius:18px;max-width:420px;width:100%;
overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.3);font-family:'Plus Jakarta Sans',sans-serif;}
#mockBuyPop .mbp-head{background:linear-gradient(135deg,#B45309,#F59E0B);padding:1.25rem 1.4rem;color:#fff;}
#mockBuyPop .mbp-h1{font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1.4rem;line-height:1.2;}
#mockBuyPop .mbp-h2{font-size:.84rem;opacity:.95;margin-top:.28rem;}
#mockBuyPop .mbp-body{padding:1.15rem 1.4rem 1.4rem;}
#mockBuyPop ul{margin:0 0 1rem;padding-left:1.1rem;font-size:.86rem;color:#334155;line-height:1.75;}
#mockBuyPop .mbp-price{text-align:center;background:#FFF7ED;border:1px solid #FDBA74;
border-radius:12px;padding:.7rem;margin-bottom:.95rem;font-family:'Rajdhani',sans-serif;
font-weight:800;font-size:1.5rem;color:#C2410C;}
#mockBuyPop .mbp-price s{color:#94A3B8;font-size:1.05rem;font-weight:700;}
#mockBuyPop .mbp-go{width:100%;background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;
border:none;border-radius:11px;padding:.8rem;font-family:'Rajdhani',sans-serif;font-weight:800;
font-size:1.02rem;cursor:pointer;}
#mockBuyPop .mbp-go[disabled]{opacity:.6;cursor:progress;}
#mockBuyPop .mbp-no{text-align:center;margin-top:.6rem;font-size:.78rem;color:#94A3B8;cursor:pointer;}
/* step dots */
#mockBuyPop .mbp-steps{display:flex;gap:.35rem;margin-top:.7rem;}
#mockBuyPop .mbp-dot{width:26px;height:4px;border-radius:100px;background:rgba(255,255,255,.35);}
#mockBuyPop .mbp-dot.on{background:#fff;}
/* which mock you clicked */
#mockBuyPop .mbp-mock{background:#F8FAFC;border:1px solid #E2E8F0;border-radius:11px;
padding:.7rem .85rem;margin-bottom:.9rem;}
#mockBuyPop .mbp-mock b{display:block;font-family:'Rajdhani',sans-serif;font-size:1rem;
color:#1E293B;line-height:1.3;}
#mockBuyPop .mbp-mock span{font-size:.74rem;color:#64748B;}
/* form */
#mockBuyPop .mbp-field{margin-bottom:.7rem;}
#mockBuyPop .mbp-field label{display:block;font-size:.76rem;font-weight:700;color:#475569;
margin-bottom:.25rem;}
#mockBuyPop .mbp-field label b{color:#DC2626;}
#mockBuyPop .mbp-field input,#mockBuyPop .mbp-field select{width:100%;border:1px solid #E2E8F0;
border-radius:9px;padding:.6rem .75rem;font-size:.9rem;font-family:'Plus Jakarta Sans',sans-serif;
outline:none;background:#fff;color:#1E293B;}
#mockBuyPop .mbp-field input:focus,#mockBuyPop .mbp-field select:focus{border-color:#FF6B00;}
#mockBuyPop .mbp-field input.bad,#mockBuyPop .mbp-field select.bad{border-color:#DC2626;background:#FEF2F2;}
#mockBuyPop .mbp-hint{background:#F0F9FF;border:1px solid #BAE6FD;color:#075985;
border-radius:9px;padding:.5rem .7rem;font-size:.78rem;margin-bottom:.75rem;line-height:1.5;}
#mockBuyPop .mbp-field.known label::after{content:'from your account';float:right;
font-weight:600;color:#0EA5E9;font-size:.68rem;text-transform:none;letter-spacing:0;}
#mockBuyPop .mbp-field.need label::after{content:'needs filling';float:right;
font-weight:600;color:#C2410C;font-size:.68rem;}
#mockBuyPop .mbp-note{font-size:.72rem;color:#64748B;line-height:1.5;margin-top:.3rem;}
#mockBuyPop .mbp-err{background:#FEF2F2;border:1px solid #FECACA;color:#B91C1C;border-radius:9px;
padding:.55rem .7rem;font-size:.8rem;margin-bottom:.7rem;line-height:1.5;}
/* success */
#mockBuyPop .mbp-done{font-size:2.6rem;text-align:center;line-height:1;margin-bottom:.5rem;}
#mockBuyPop .mbp-donetitle{font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1.35rem;
color:#059669;text-align:center;margin-bottom:.45rem;}
#mockBuyPop .mbp-donetxt{font-size:.86rem;color:#334155;line-height:1.6;text-align:center;
margin:0 0 1rem;}
"""

# ─────────────────────────────────────────────────────────────────────────────
# 2. Card markup
# ─────────────────────────────────────────────────────────────────────────────

CARD_RE = re.compile(
    r'^<div class="mock-card[^\n]*?data-tier="(?P<tier>\w+)" data-n="(?P<n>\d+)">\n'
    r'(?P<body>.*?)'
    r'^</div>\n',
    re.S | re.M,
)

FREE_TAG = '  <div class="mc-lock mc-free-tag"><span><i class="mc-ico">&#10004;</i>Free</span></div>\n'
PAID_TAG = '  <div class="mc-lock mc-paid-tag"><span><i class="mc-coin">&#129689;</i>Premium</span></div>\n'
LOCK_BTN = ('  <button class="mc-locktag" type="button" '
            'aria-label="Premium mock — unlock to attempt">'
            '<i>&#128274;</i>Unlock</button>\n')

# a plain (dateless-tag) overlay line, e.g. the "Live 15 Oct 2026" pill
PLAIN_LOCK_RE = re.compile(r'^  <div class="mc-lock"><span>.*?</span></div>\n', re.M)


def patch_cards(html: str) -> tuple[str, dict]:
    """Ensure every card carries the right badge, and every premium card a lock."""
    stats = {"free_added": 0, "paid_added": 0, "lock_added": 0}

    def fix(m: re.Match) -> str:
        body = m.group("body")
        n = int(m.group("n"))
        premium = n > FREE_UP_TO

        has_free = "mc-free-tag" in body
        has_paid = "mc-paid-tag" in body
        has_lock = "mc-locktag" in body

        insert = ""
        if premium and not has_paid:
            insert += PAID_TAG
            stats["paid_added"] += 1
        elif not premium and not has_free:
            insert += FREE_TAG
            stats["free_added"] += 1

        if insert:
            # place the badge just before the "Coming Soon / date" overlay if
            # there is one, otherwise at the end of the card
            hit = PLAIN_LOCK_RE.search(body)
            if hit:
                body = body[: hit.start()] + insert + body[hit.start():]
            else:
                body = body + insert

        if premium and not has_lock:
            # the lock pill sits immediately after the Premium badge
            idx = body.find('class="mc-lock mc-paid-tag"')
            end = body.find("\n", idx) + 1
            body = body[:end] + LOCK_BTN + body[end:]
            stats["lock_added"] += 1

        return m.group(0)[: m.group(0).index("\n") + 1] + body + "</div>\n"

    return CARD_RE.sub(fix, html), stats


# ─────────────────────────────────────────────────────────────────────────────
# 3. Re-attempt label fix  (two one-match edits)
# ─────────────────────────────────────────────────────────────────────────────

PILL_ANCHOR = "function _resetPills() {"
PILL_REPLACE = ("window.tsscApplyPills = _applyPills;  /* " + MARKER + " */\n"
                "function _resetPills() {")

# Both pages end the availability pass by writing the Tier I live count into
# #tc1, but with different surrounding code — so anchor on that id and splice
# the re-apply call in just above it, matching the local indentation.
AVAIL_ID = "getElementById('tc1')"


def wire_reapply(html: str) -> str:
    lines = html.split("\n")
    for i, ln in enumerate(lines):
        if AVAIL_ID in ln:
            pad = ln[: len(ln) - len(ln.lstrip())]
            lines[i:i] = [
                f"{pad}/* {MARKER} — availability is now known: re-label cards that were",
                f"{pad}   still .locked when auth first resolved (so they read Re-attempt),",
                f"{pad}   and repaint the premium locks over the freshly unlocked cards. */",
                f"{pad}if (window.tsscApplyPills) window.tsscApplyPills();",
                f"{pad}if (window.tsscApplyEntitlement) window.tsscApplyEntitlement();",
            ]
            return "\n".join(lines)
    raise SystemExit("  ✗ anchor not found: #tc1 live-count line")


# Full attempt-tracking module, for a page that has none (the SEO landing page
# never had it, which is why its cards never switched to "Re-attempt").
ATTEMPT_MODULE = """
<!-- ===== attempt tracking (""" + MARKER + """) — ported from mock-list.html ===== -->
<script type="module">
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { getFirestore, collection, query, where, getDocs } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

const _aApp = initializeApp({
  apiKey:"AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA",
  authDomain:"trickyssc-17bb3.firebaseapp.com",
  projectId:"trickyssc-17bb3",
  storageBucket:"trickyssc-17bb3.firebasestorage.app",
  messagingSenderId:"450627057220",
  appId:"1:450627057220:web:366267bf437d94f20c6e11"
});
const _aAuth = getAuth(_aApp);
const _aDb   = getFirestore(_aApp);

const __attempted = new Set();

function _loadLocalAttempts() {
  try {
    const seen = JSON.parse(localStorage.getItem('tssc_attempted') || '{}');
    Object.keys(seen).forEach(k => {
      if (k.startsWith('p:') || k.startsWith('m:')) __attempted.add(k.slice(2));
    });
  } catch (e) {}
}

function _applyPills() {
  document.querySelectorAll('.mc-attempt').forEach(btn => {
    const card = btn.closest('.mock-card');
    if (card && card.classList.contains('locked')) return;
    const pe = btn.getAttribute('data-pid-en');
    const ph = btn.getAttribute('data-pid-hi');
    if ((pe && __attempted.has(pe)) || (ph && __attempted.has(ph))) {
      btn.innerHTML = '\\u21bb Re-attempt';
    }
  });
}
window.tsscApplyPills = _applyPills;  /* """ + MARKER + """ */

function _resetPills() {
  __attempted.clear();
  document.querySelectorAll('.mc-attempt').forEach(btn => {
    const card = btn.closest('.mock-card');
    if (!card || !card.classList.contains('locked')) btn.innerHTML = '\\u25b6 Attempt Test';
  });
}

async function _syncAttempts(uid) {
  if (!uid) return;
  const _ck = 'tssc_attempts_' + uid, _ttl = 10 * 60 * 1000;
  try {
    const _c = sessionStorage.getItem(_ck);
    if (_c) {
      const _o = JSON.parse(_c);
      if (Date.now() - (_o.ts || 0) < _ttl && Array.isArray(_o.p)) {
        _o.p.forEach(id => __attempted.add(id)); _applyPills(); return;
      }
    }
  } catch (e) {}
  try {
    const snap = await getDocs(query(collection(_aDb, 'attempts'), where('uid', '==', uid)));
    snap.forEach(d => {
      const a = d.data() || {};
      if (a.paperId) __attempted.add(a.paperId);
      if (a.mockId)  __attempted.add(a.mockId);
    });
    try { sessionStorage.setItem(_ck, JSON.stringify({ ts: Date.now(), p: [...__attempted] })); } catch (e) {}
    _applyPills();
  } catch (e) { console.warn('attempts sync failed:', e.message); }
}

onAuthStateChanged(_aAuth, user => {
  if (!user) { _resetPills(); return; }
  _loadLocalAttempts(); _applyPills();
  _syncAttempts(user.uid);
});
</script>
"""


# ─────────────────────────────────────────────────────────────────────────────
# 4. Paywall module + popup
# ─────────────────────────────────────────────────────────────────────────────

PAYWALL_HTML = r"""
<!-- pricing catalog loader: prices live in Firestore config/pricing,
     edited in admin-pricing.html. No code change to alter a price. -->
<script src="https://trickyssc.com/tssc-pricing.js"></script>

<!-- ===== premium unlock: 3-step checkout (""" + MARKER + r""") =====
     step 1  what this mock is        (details card)
     step 2  buyer details + course   (mandatory form)
     step 3  handed to Razorpay, then "unlocked" confirmation
-->
<div id="mockBuyPop">
  <div class="mbp-card">
    <div class="mbp-head">
      <div class="mbp-h1" id="mbpTitle">&#128274; Premium mock test</div>
      <div class="mbp-h2" id="mbpSub">Unlock the full SSC CGL mock series</div>
      <div class="mbp-steps" id="mbpSteps">
        <span class="mbp-dot on" data-step="1"></span>
        <span class="mbp-dot" data-step="2"></span>
        <span class="mbp-dot" data-step="3"></span>
      </div>
    </div>

    <!-- ---------- step 1: what you are buying ---------- -->
    <div class="mbp-body mbp-step" data-step="1">
      <div class="mbp-mock" id="mbpMock"></div>
      <div class="mbp-price" id="mbpPrice"></div>
      <ul id="mbpPerks"></ul>
      <button class="mbp-go" id="mbpNext">Proceed to checkout &rarr;</button>
      <div class="mbp-no" data-close>Maybe later</div>
    </div>

    <!-- ---------- step 2: buyer details ---------- -->
    <div class="mbp-body mbp-step" data-step="2" hidden>
      <div class="mbp-hint" id="mbpHint" hidden></div>
      <div class="mbp-field">
        <label for="mbpName">Full name <b>*</b></label>
        <input id="mbpName" type="text" autocomplete="name" placeholder="As you want it on the receipt">
      </div>
      <div class="mbp-field">
        <label for="mbpMobile">Registered mobile number <b>*</b></label>
        <input id="mbpMobile" type="tel" inputmode="numeric" maxlength="10" autocomplete="tel-national" placeholder="10-digit mobile">
        <div class="mbp-note">This will be your registered mobile number.
          All communication about your purchase will go to this number only,
          so please check it before continuing.</div>
      </div>
      <div class="mbp-field">
        <label for="mbpPlace">Place <b>*</b></label>
        <input id="mbpPlace" type="text" autocomplete="address-level2" placeholder="City / district">
      </div>
      <div class="mbp-field">
        <label for="mbpCourse">Course <b>*</b></label>
        <select id="mbpCourse"></select>
      </div>
      <div class="mbp-err" id="mbpErr" hidden></div>
      <button class="mbp-go" id="mbpPay">Continue to payment &rarr;</button>
      <div class="mbp-no" data-back>&larr; Back</div>
    </div>

    <!-- ---------- step 3: unlocked ---------- -->
    <div class="mbp-body mbp-step" data-step="3" hidden>
      <div class="mbp-done">&#127881;</div>
      <div class="mbp-donetitle" id="mbpDoneTitle">Course unlocked</div>
      <p class="mbp-donetxt" id="mbpDoneTxt">
        Your payment went through. Every premium mock is open on this account now.</p>
      <button class="mbp-go" data-close>Start practising &rarr;</button>
    </div>
  </div>
</div>

<script type="module">
/* ===== """ + MARKER + r""" — premium entitlement gate for mock cards =====

   Entitlement contract (written by the trickyssc-pay Worker, never by a browser):

     entitlements/{uid} = {
       uid,
       allAccess: { active: true, expiresAt: <Timestamp> },        // the full plan
       modules: {
         "ssc-cgl-mocks": { active: true, expiresAt: <Timestamp>,
                            orderId, grantedAt, source: "razorpay"|"grandfather"|"manual" }
       }
     }

   A user is entitled if allAccess OR modules[MODULE] is active and not expired.
   Missing expiresAt is treated as "no expiry" (grandfathered accounts).
*/
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { getFirestore, doc, getDoc } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

const CFG = {
  exam:        'ssc-cgl',           // which catalog block the dropdown reads
  module:      'ssc-cgl-mocks',     // what THIS page sells (preselected)
  freeUpTo:    """ + str(FREE_UP_TO) + r""",
  // Locks are VISIBLE from now, but only BLOCK from this moment onward.
  // Keeps the "everything free until 24 Aug" promise on this page honest.
  // Set to null to enforce immediately.
  enforceFrom: '2026-08-25T00:00:00+05:30',
  buyUrl:      'https://trickyssc.com/pricing.html?module=ssc-cgl-mocks',
  cacheTtlMs:  10 * 60 * 1000
};

const _app = initializeApp({
  apiKey:"AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA",
  authDomain:"trickyssc-17bb3.firebaseapp.com",
  projectId:"trickyssc-17bb3",
  storageBucket:"trickyssc-17bb3.firebasestorage.app",
  messagingSenderId:"450627057220",
  appId:"1:450627057220:web:366267bf437d94f20c6e11"
});
const _auth = getAuth(_app);
const _db   = getFirestore(_app);

let OWNED = false;

const enforcing = () => {
  let o = null;
  try { o = sessionStorage.getItem('tssc_paywall_override'); } catch (e) {}
  if (o === 'on')  return true;   // testing: paywall live for THIS browser only
  if (o === 'off') return false;
  return !CFG.enforceFrom || Date.now() >= new Date(CFG.enforceFrom).getTime();
};

/* ---- test switches -------------------------------------------------------
   Affect only the browser tab you type them in. Students are never touched.

     ?paywall=on      force the paywall ON  (test the locked flow before 25 Aug)
     ?paywall=off     force it OFF
     ?paywall=clear   drop the override AND the cached entitlement

   The entitlement is cached for 10 minutes, so after a test purchase — or
   after deleting your entitlement doc to re-test the locked state — use
   ?paywall=clear, otherwise the stale cache keeps answering.
--------------------------------------------------------------------------- */
(function () {
  try {
    const q = new URLSearchParams(location.search).get('paywall');
    if (!q) return;
    if (q === 'on' || q === 'off') sessionStorage.setItem('tssc_paywall_override', q);
    if (q === 'clear') sessionStorage.removeItem('tssc_paywall_override');
    // any explicit switch also busts the entitlement cache.
    // Uses the indexed Storage API (length/key) rather than Object.keys, which
    // only works on Storage by accident of the named-property getter.
    const stale = [];
    for (let i = 0; i < sessionStorage.length; i++) {
      const k = sessionStorage.key(i);
      if (k && k.indexOf('tssc_ent_') === 0) stale.push(k);
    }
    stale.forEach(k => sessionStorage.removeItem(k));
    console.info('[paywall] override =', sessionStorage.getItem('tssc_paywall_override') || 'none');
  } catch (e) {}
})();

/* ---- mark every card free / premium from its data-n ---- */
function classify() {
  document.querySelectorAll('.mock-card').forEach(c => {
    const n = parseInt(c.getAttribute('data-n') || '0', 10);
    c.classList.add(n > CFG.freeUpTo ? 'tssc-premium' : 'tssc-free');
  });
}

/* ---- paint ownership onto the cards ---- */
function applyEntitlement() {
  document.body.classList.add('tssc-ent-resolved');
  document.body.classList.toggle('tssc-enforce', enforcing());
  document.body.classList.toggle('tssc-owned-user', OWNED);
  document.querySelectorAll('.mock-card.tssc-premium')
    .forEach(c => c.classList.toggle('tssc-owned', OWNED));
}
window.tsscApplyEntitlement = applyEntitlement;

/* ---- is this card gated right now? ---- */
function isGated(card) {
  return !!card
      && card.classList.contains('tssc-premium')
      && !card.classList.contains('tssc-owned')
      && enforcing();
}
window.tsscIsGated = isGated;

/* ---- unlock popup ---- */
/* ------------------------------------------------------------------
   3-step unlock modal.  Step 1 explains the mock, step 2 collects the
   mandatory details, step 3 confirms.  The course dropdown is built from
   the Firestore pricing catalog, so changing a price or adding a combo
   needs no edit here and no deploy.
------------------------------------------------------------------ */
const pop = document.getElementById('mockBuyPop');
let ORDER = {};   // what the buyer is purchasing, assembled across the steps

let CATALOG = null;   // resolved pricing catalog, loaded once
let PREFILL = null;   // in-flight profile read, awaited before step 2

async function catalog() {
  if (CATALOG) return CATALOG;
  const P = window.TSSC_PRICING;
  if (!P) throw new Error('Pricing catalog is unavailable. Please refresh.');
  CATALOG = await P.load();
  return CATALOG;
}

function showStep(n) {
  pop.querySelectorAll('.mbp-step').forEach(s => {
    s.hidden = s.getAttribute('data-step') !== String(n);
  });
  pop.querySelectorAll('.mbp-dot').forEach(d => {
    d.classList.toggle('on', parseInt(d.getAttribute('data-step'), 10) <= n);
  });
}

function money(c) {
  return (c.mrp ? '<s>\u20b9' + c.mrp + '</s> ' : '') +
         '\u20b9' + c.price + ' <span style="font-size:.8rem;">/ year</span>';
}

async function openBuy(card) {
  if (!pop) return;

  // paint the mock straight away — the catalog fetch shouldn't delay this.
  // Deliberately generic: the buyer is purchasing the whole series, not the
  // one mock they happened to tap, so naming "Mock Test 5" would mislead.
  const tierLabel = (card?.getAttribute('data-tier') === 'tier2') ? 'Tier II' : 'Tier I';
  const examLabel = (CFG.exam || 'ssc-cgl').replace(/^ssc-/, 'SSC ').toUpperCase();
  const title = examLabel + ' ' + tierLabel + ' Mock Test 2026';
  const stats = [...(card?.querySelectorAll('.mc-stat') || [])]
                  .map(s => s.textContent.replace(/\s+/g, ' ').trim()).join('  \u00b7  ');
  document.getElementById('mbpMock').innerHTML =
    (title ? '<b>' + title + '</b>' : '') + (stats ? '<span>' + stats + '</span>' : '');
  document.getElementById('mbpPrice').innerHTML = '<span style="font-size:.9rem;">Loading price\u2026</span>';
  document.getElementById('mbpPerks').innerHTML = '';
  document.getElementById('mbpSub').textContent = '';
  showStep(1);
  pop.style.display = 'flex';
  document.body.style.overflow = 'hidden';

  let cat, P;
  try {
    P = window.TSSC_PRICING;
    cat = await catalog();
  } catch (e) {
    document.getElementById('mbpPrice').innerHTML =
      '<span style="font-size:.85rem;color:#B91C1C;">Prices unavailable \u2014 please refresh.</span>';
    return;
  }

  // Lead with the cheapest product that unlocks what this page gates. That is
  // usually the single course, but if you ever price a combo below it, the
  // combo leads automatically.
  const lead = P.bestFor(cat, CFG.module);
  if (!lead) {
    document.getElementById('mbpPrice').innerHTML =
      '<span style="font-size:.85rem;color:#B91C1C;">Nothing is on sale for this yet.</span>';
    return;
  }
  ORDER = { courseId: lead.id };

  document.getElementById('mbpSub').textContent = lead.label;
  document.getElementById('mbpPrice').innerHTML = money(lead);

  // combos that also include this module, shown as an upsell line
  const combos = P.combosFor(cat, CFG.module).filter(c => c.id !== lead.id);
  document.getElementById('mbpPerks').innerHTML =
    (lead.blurb ? '<li>' + lead.blurb + '</li>' : '') +
    '<li>One payment \u2014 not per test</li>' +
    '<li>Access for ' + (lead.durationDays || 365) + ' days</li>' +
    combos.map(c =>
      '<li><b>' + c.label + '</b> \u2014 \u20b9' + c.price +
      ' for ' + c.grants.length + ' modules. Pick it in the next step.</li>').join('');

  // step 2 dropdown: every live product for this exam, combos included
  const all = P.productsFor(cat, CFG.exam);
  const sel = document.getElementById('mbpCourse');
  sel.innerHTML = all.map(c =>
    '<option value="' + c.id + '">' + c.label + ' \u2014 \u20b9' + c.price +
    (c.grants.length > 1 ? ' (' + c.grants.length + ' modules)' : '') + '</option>').join('');
  sel.value = lead.id;

  PREFILL = prefill();
}

function closeBuy() {
  if (pop) pop.style.display = 'none';
  document.body.style.overflow = '';
}

function showUnlocked(msg) {
  if (!pop) return;
  if (msg) document.getElementById('mbpDoneTxt').textContent = msg;
  showStep(3);
  pop.style.display = 'flex';
  document.body.style.overflow = 'hidden';
}

window.tsscOpenBuy     = openBuy;
window.tsscCloseBuy    = closeBuy;
window.tsscShowUnlocked = showUnlocked;

/* prefill name + mobile from the signed-in profile so the form is one tap */
/* Prefill from the signed-in profile so the form is a couple of taps.

   users/{uid} really holds:  name, displayName, email, phone, loginMethod,
   createdAt, lastActive, uid.  The number field is `phone` (NOT `mobile`),
   and it may be stored with a +91 prefix depending on how the OTP flow saved
   it — normalise() strips that.

   Google sign-ups often have no phone at all, which is normal, not an error:
   the field just stays empty for them to fill in.

   localStorage first (instant, no read), then one Firestore read to confirm. */
function tenDigits(v) {
  let d = String(v == null ? '' : v).replace(/\D/g, '');
  if (d.length === 12 && d.startsWith('91')) d = d.slice(2);
  if (d.length === 11 && d.startsWith('0'))  d = d.slice(1);
  return d.length === 10 ? d : '';
}

function fillFrom(u) {
  if (!u) return;
  const n = document.getElementById('mbpName');
  const m = document.getElementById('mbpMobile');
  const pl = document.getElementById('mbpPlace');
  const nm = u.name || u.displayName || '';
  if (n && !n.value && nm && nm !== 'Student') n.value = nm;
  const ph = tenDigits(u.phone);
  if (m && !m.value && ph) m.value = ph;
  // `place` isn't on the profile — it comes back from the last checkout
  const pc = u.place || u.city || '';
  if (pl && !pl.value && pc) pl.value = pc;
}

/* Tag each field so the buyer can see at a glance what came from their
   account and what they still have to type. */
function markFields() {
  const map = { mbpName: 'name', mbpMobile: 'mobile number', mbpPlace: 'place' };
  const missing = [];
  Object.keys(map).forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    const box = el.closest('.mbp-field');
    if (!box) return;
    const has = !!el.value.trim();
    box.classList.toggle('known', has);
    box.classList.toggle('need', !has);
    if (!has) missing.push(map[id]);
  });
  const hint = document.getElementById('mbpHint');
  if (hint) {
    if (!_auth.currentUser) { hint.hidden = true; return; }
    hint.hidden = false;
    hint.innerHTML = missing.length
      ? 'We\'ve filled in what your account already has. Please add your <b>' +
        missing.join('</b>, <b>') + '</b> \u2014 then pick your course.'
      : 'Filled in from your account. Change anything that\u2019s out of date, then pick your course.';
  }
  return missing;
}

/** Focus the first field still empty, so the buyer lands where the work is. */
function focusFirstGap() {
  const first = ['mbpName', 'mbpMobile', 'mbpPlace']
    .map(id => document.getElementById(id))
    .filter(el => el && !el.value.trim())[0];
  (first || document.getElementById('mbpCourse'))?.focus();
}

async function prefill() {
  try { fillFrom(JSON.parse(localStorage.getItem('tssc_user') || '{}')); } catch (e) {}
  try { fillFrom(JSON.parse(localStorage.getItem('tssc_checkout') || '{}')); } catch (e) {}
  const user = _auth.currentUser;
  if (!user) return;
  try {
    const snap = await getDoc(doc(_db, 'users', user.uid));
    if (snap.exists()) {
      const u = snap.data() || {};
      fillFrom(u);
      // keep the local copy current so the next checkout needs no read
      try {
        const cur = JSON.parse(localStorage.getItem('tssc_user') || '{}');
        localStorage.setItem('tssc_user', JSON.stringify({
          ...cur, uid: user.uid,
          name: u.name || u.displayName || cur.name,
          phone: u.phone || cur.phone || '',
          place: cur.place || ''
        }));
      } catch (e) {}
    }
  } catch (e) { /* profile unreadable: the buyer just types it in */ }
  markFields();
}

pop?.querySelectorAll('[data-close]').forEach(el => el.addEventListener('click', closeBuy));
pop?.querySelectorAll('[data-back]').forEach(el => el.addEventListener('click', () => showStep(1)));
pop?.addEventListener('click', e => { if (e.target === pop) closeBuy(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeBuy(); });

document.getElementById('mbpNext')?.addEventListener('click', async () => {
  if (!_auth.currentUser) {
    const back = encodeURIComponent(location.href);
    location = 'https://trickyssc.com/login.html?next=' + back;
    return;
  }
  const btn = document.getElementById('mbpNext');
  btn.disabled = true;
  // A registered buyer should never see empty boxes they could have avoided:
  // wait for the profile read before showing the form.
  try { await PREFILL; } catch (e) {}
  btn.disabled = false;
  markFields();
  showStep(2);
  focusFirstGap();
});

/* ---- validate, then hand off to checkout ---- */
function fail(msg, id) {
  const box = document.getElementById('mbpErr');
  box.textContent = msg; box.hidden = false;
  const f = id && document.getElementById(id);
  if (f) { f.classList.add('bad'); f.focus(); }
  return false;
}

function collect() {
  const box = document.getElementById('mbpErr');
  box.hidden = true;
  ['mbpName', 'mbpMobile', 'mbpPlace', 'mbpCourse']
    .forEach(id => document.getElementById(id)?.classList.remove('bad'));

  const name   = document.getElementById('mbpName').value.trim();
  // browser autofill often supplies +91XXXXXXXXXX or 0XXXXXXXXXX — normalise
  // to the bare 10 digits rather than rejecting a number that is actually fine
  let mobile = document.getElementById('mbpMobile').value.replace(/\D/g, '');
  if (mobile.length === 12 && mobile.startsWith('91')) mobile = mobile.slice(2);
  if (mobile.length === 11 && mobile.startsWith('0'))  mobile = mobile.slice(1);
  const place  = document.getElementById('mbpPlace').value.trim();
  const course = document.getElementById('mbpCourse').value;

  if (name.length < 2)             return fail('Please enter your full name.', 'mbpName');
  if (!/^[6-9]\d{9}$/.test(mobile)) return fail('Enter a valid 10-digit Indian mobile number.', 'mbpMobile');
  if (place.length < 2)            return fail('Please enter your city or district.', 'mbpPlace');
  if (!course)                     return fail('Please choose a course.', 'mbpCourse');

  return { name, mobile, place, courseId: course };
}

document.getElementById('mbpPay')?.addEventListener('click', async () => {
  const d = collect();
  if (!d) return;
  const user = _auth.currentUser;
  if (!user) { location = 'https://trickyssc.com/login.html'; return; }

  const btn = document.getElementById('mbpPay');
  btn.disabled = true;
  btn.textContent = 'Opening payment\u2026';
  ORDER = { ...d, uid: user.uid, email: user.email || '' };
  // so a second purchase is prefilled end to end, place included
  try {
    localStorage.setItem('tssc_checkout', JSON.stringify(
      { name: d.name, phone: d.mobile, place: d.place }));
  } catch (e) {}

  try {
    if (typeof window.tsscStartCheckout !== 'function') {
      throw new Error('Checkout is not wired up yet on this page.');
    }
    await window.tsscStartCheckout(ORDER);
  } catch (e) {
    fail(e.message || 'Could not start the payment. Please try again.');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Continue to payment \u2192';
  }
});

/* Called by the checkout layer once the Worker has confirmed the payment.
   Re-reads the entitlement (cache-busted) and repaints every card. */
window.tsscOnPaymentSuccess = async function (msg) {
  const user = _auth.currentUser;
  if (user) {
    try { sessionStorage.removeItem('tssc_ent_' + user.uid); } catch (e) {}
    OWNED = await loadEntitlement(user.uid);
  }
  applyEntitlement();
  showUnlocked(msg);
};

/* ---- lock pill click ---- */
document.addEventListener('click', e => {
  const lock = e.target.closest?.('.mc-locktag');
  if (!lock) return;
  e.preventDefault();
  e.stopPropagation();
  const card = lock.closest('.mock-card');
  openBuy(card);
});

/* ---- gate the attempt button by wrapping the existing chooser ---- */
const _origChooser = window.openLangChooser;
if (typeof _origChooser === 'function') {
  window.openLangChooser = function (btn) {
    const card = btn?.closest?.('.mock-card');
    if (isGated(card)) {
      openBuy(card);
      return;
    }
    return _origChooser.apply(this, arguments);
  };
}

/* ---- read the entitlement ---- */
function readCache(uid) {
  try {
    const o = JSON.parse(sessionStorage.getItem('tssc_ent_' + uid) || 'null');
    if (o && Date.now() - (o.ts || 0) < CFG.cacheTtlMs) return !!o.owned;
  } catch (e) {}
  return null;
}
function writeCache(uid, owned) {
  try { sessionStorage.setItem('tssc_ent_' + uid, JSON.stringify({ ts: Date.now(), owned })); }
  catch (e) {}
}

function grantActive(g) {
  if (!g || g.active !== true) return false;
  const exp = g.expiresAt;
  if (!exp) return true;                                   // no expiry = permanent
  const ms = exp.toDate ? exp.toDate().getTime()
           : (exp.seconds ? exp.seconds * 1000 : Date.parse(exp));
  return !isFinite(ms) || ms > Date.now();
}

async function loadEntitlement(uid) {
  const cached = readCache(uid);
  if (cached !== null) return cached;
  try {
    const snap = await getDoc(doc(_db, 'entitlements', uid));
    const d = snap.exists() ? (snap.data() || {}) : {};
    const owned = grantActive(d.allAccess) || grantActive((d.modules || {})[CFG.module]);
    writeCache(uid, owned);
    return owned;
  } catch (e) {
    console.warn('entitlement read failed:', e.message);
    return false;   // fail closed
  }
}

classify();
applyEntitlement();          // signed-out default: locked

onAuthStateChanged(_auth, async user => {
  if (!user) { OWNED = false; applyEntitlement(); return; }
  OWNED = await loadEntitlement(user.uid);
  applyEntitlement();
});
</script>
"""


# ─────────────────────────────────────────────────────────────────────────────
# driver
# ─────────────────────────────────────────────────────────────────────────────

def assert_once(html: str, needle: str, label: str, at_least: int = 1) -> int:
    n = html.count(needle)
    if n < at_least:
        raise SystemExit(f"  ✗ anchor not found: {label}")
    return n


def patch_file(path: Path, dry: bool) -> None:
    html = path.read_text(encoding="utf-8")
    print(f"\n=== {path.name} ({len(html):,} bytes) ===")

    if MARKER in html:
        print("  • already patched — nothing to do")
        return

    # 1. CSS (the SEO page carries two copies of the style block)
    n = assert_once(html, CSS_ANCHOR, "paid-tag reduced-motion rule")
    html = html.replace(CSS_ANCHOR, CSS_ANCHOR + CSS_BLOCK)
    print(f"  ✓ CSS block inserted ×{n}")

    # 2. cards
    html, stats = patch_cards(html)
    print(f"  ✓ Free badges added   : {stats['free_added']}")
    print(f"  ✓ Premium badges added: {stats['paid_added']}")
    print(f"  ✓ Lock buttons added  : {stats['lock_added']}")

    # 3. re-attempt fix
    tail = ""
    if "_applyPills" in html:
        assert_once(html, PILL_ANCHOR, "_resetPills declaration")
        html = html.replace(PILL_ANCHOR, PILL_REPLACE, 1)
        print("  ✓ existing attempt tracking exposed as window.tsscApplyPills")
    else:
        tail += ATTEMPT_MODULE
        print("  ! page had NO attempt tracking — full module injected "
              "(this is why Re-attempt never showed here)")
    html = wire_reapply(html)
    print("  ✓ re-attempt re-label wired into the availability pass")

    # 4. paywall module
    assert_once(html, "</body>", "</body>")
    html = html.replace("</body>", tail + PAYWALL_HTML + "</body>", 1)
    print("  ✓ entitlement module + unlock popup injected")

    if dry:
        print("  (dry run — nothing written)")
        return

    bak = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, bak)
    path.write_text(html, encoding="utf-8")
    print(f"  → written ({len(html):,} bytes), backup at {bak.name}")


def main() -> None:
    ap = argparse.ArgumentParser(description="TrickySSC mock paywall patch")
    ap.add_argument("--page", action="append", required=True,
                    help="page to patch (repeatable)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    for p in a.page:
        f = Path(p)
        if not f.exists():
            print(f"✗ missing: {p}", file=sys.stderr)
            continue
        patch_file(f, a.dry_run)
    print("\ndone.")


if __name__ == "__main__":
    main()
