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
.mc-locktag{display:inline-flex!important;align-items:center;gap:.24rem;margin-left:.32rem;
vertical-align:middle;border:none;cursor:pointer;font-family:'Rajdhani',sans-serif;
font-size:.68rem!important;font-weight:800;letter-spacing:.03em;padding:.2rem .55rem;
border-radius:100px;background:linear-gradient(135deg,#1E293B,#475569);color:#fff;
box-shadow:0 2px 8px rgba(15,23,42,.3),inset 0 1px 0 rgba(255,255,255,.18);
-webkit-tap-highlight-color:transparent;transition:filter .15s ease,transform .15s ease;}
.mc-locktag:hover{filter:brightness(1.2);transform:translateY(-1px);}
.mc-locktag i{font-style:normal;font-size:.76rem;line-height:1;}
/* owned: the lock disappears and the gold Premium pill goes green */
.mock-card.tssc-owned .mc-locktag{display:none!important;}
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
#mockBuyPop .mbp-no{text-align:center;margin-top:.6rem;font-size:.78rem;color:#94A3B8;cursor:pointer;}
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

PAYWALL_HTML = """
<!-- ===== premium unlock popup (""" + MARKER + """) ===== -->
<div id="mockBuyPop">
  <div class="mbp-card">
    <div class="mbp-head">
      <div class="mbp-h1">&#128274; Premium mock test</div>
      <div class="mbp-h2" id="mbpSub">Unlock the full SSC CGL mock series</div>
    </div>
    <div class="mbp-body">
      <div class="mbp-price"><s>&#8377;199</s> &#8377;49 <span style="font-size:.8rem;">/ year</span></div>
      <ul>
        <li>All 50 Tier I + all 50 Tier II mocks</li>
        <li>Every mock released during the year</li>
        <li>Real sectional timing, English &amp; Hindi</li>
        <li>Full solutions and section analysis</li>
      </ul>
      <button class="mbp-go" id="mbpGo">Unlock for &#8377;49 &rarr;</button>
      <div class="mbp-no" id="mbpNo">Maybe later</div>
    </div>
  </div>
</div>

<script type="module">
/* ===== """ + MARKER + """ — premium entitlement gate for mock cards =====

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
  module:      'ssc-cgl-mocks',
  freeUpTo:    """ + str(FREE_UP_TO) + """,
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

const enforcing = () => !CFG.enforceFrom || Date.now() >= new Date(CFG.enforceFrom).getTime();

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
const pop = document.getElementById('mockBuyPop');
function openBuy(title) {
  const sub = document.getElementById('mbpSub');
  if (sub) sub.textContent = title || 'Unlock the full SSC CGL mock series';
  if (pop) { pop.style.display = 'flex'; document.body.style.overflow = 'hidden'; }
}
function closeBuy() {
  if (pop) pop.style.display = 'none';
  document.body.style.overflow = '';
}
window.tsscOpenBuy  = openBuy;
window.tsscCloseBuy = closeBuy;

document.getElementById('mbpNo')?.addEventListener('click', closeBuy);
pop?.addEventListener('click', e => { if (e.target === pop) closeBuy(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeBuy(); });

/* Razorpay hook: define window.tsscStartCheckout(module) elsewhere and this
   button will call it. Until then it falls back to the pricing page. */
document.getElementById('mbpGo')?.addEventListener('click', () => {
  if (typeof window.tsscStartCheckout === 'function') {
    window.tsscStartCheckout(CFG.module);
  } else {
    window.location = CFG.buyUrl;
  }
});

/* ---- lock pill click ---- */
document.addEventListener('click', e => {
  const lock = e.target.closest?.('.mc-locktag');
  if (!lock) return;
  e.preventDefault();
  e.stopPropagation();
  const card = lock.closest('.mock-card');
  openBuy(card?.querySelector('.mc-title')?.textContent || '');
});

/* ---- gate the attempt button by wrapping the existing chooser ---- */
const _origChooser = window.openLangChooser;
if (typeof _origChooser === 'function') {
  window.openLangChooser = function (btn) {
    const card = btn?.closest?.('.mock-card');
    if (isGated(card)) {
      openBuy(btn.getAttribute('data-title') || '');
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
