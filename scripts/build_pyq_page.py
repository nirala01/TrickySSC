#!/usr/bin/env python3
"""
build_pyq_page.py
-----------------
Reads the `papers` collection from Firestore (public REST API, web key)
and writes a fully static, Google-crawlable SSC CGL PYQ page:

    ssc-cgl-pyq.html

- Every paper becomes a plain <a href="test.html?..."> link (no JS needed to see it).
- English + Hindi versions of the same paper are merged into one card
  with two language buttons.
- Papers are grouped by year (newest first) and sorted by date+shift.
- Includes FAQ + FAQPage/ItemList JSON-LD schema for SEO.

No service-account secret required. Uses only the Python standard library.
Run:  python3 scripts/build_pyq_page.py
"""

import json
import re
import urllib.request
import urllib.error
import html
import sys
import datetime
from collections import defaultdict

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
PROJECT_ID = "trickyssc-17bb3"
API_KEY = "AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA"  # public web key (safe)
COLLECTION = "papers"
SITE = "https://trickyssc.com"
OUTPUT_FILE = "ssc-cgl-pyq.html"

# Only include papers for this exam on this page.
EXAM_FILTER = "ssc-cgl"

REST_BASE = (
    f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}"
    f"/databases/(default)/documents/{COLLECTION}"
)

MONTHS = {
    "01": "January", "02": "February", "03": "March", "04": "April",
    "05": "May", "06": "June", "07": "July", "08": "August",
    "09": "September", "10": "October", "11": "November", "12": "December",
}


# ---------------------------------------------------------------------------
# MOCK-SERIES PROMO POPUP
# ---------------------------------------------------------------------------
# Injected verbatim just before </body> in the page template below.
# This page is rendered from scratch on every build, so the popup MUST live
# here — editing ssc-cgl-pyq.html by hand is undone by the next cron run.
#
# Two knobs inside the inline <script> at the bottom of this string:
#   PAID   — localStorage key the paywall sets on a successful unlock;
#            when present and truthy the popup is suppressed. No Firestore
#            read is made here, deliberately: this page must stay at zero
#            read cost per pageview.
#   EVERY  — false = once per 24h per device, true = every page load.
#
# NOTE: it is a plain string, not an f-string, so its CSS/JS braces need no
# doubling. It is interpolated into the f-string template as {MOCK_PROMO}.
MOCK_PROMO = r"""
<!-- TSSC:MOCK-PROMO:START -->
<style id="tsscMockPromoCSS">
#tsscMP{position:fixed;inset:0;z-index:99999;display:none;align-items:center;justify-content:center;
  background:rgba(26,32,44,.45);backdrop-filter:blur(2px);padding:18px;}
#tsscMP.on{display:flex;animation:tsscMPin .22s ease-out;}
@keyframes tsscMPin{from{opacity:0}to{opacity:1}}
.tsscMP-box{position:relative;width:100%;max-width:330px;max-height:66vh;overflow-y:auto;overflow-x:hidden;
  border-radius:16px;background:#FFFFFF;border:1px solid #E2E8F0;text-align:center;
  box-shadow:0 8px 30px rgba(0,0,0,0.12);
  font-family:'Rajdhani',sans-serif;font-style:normal;color:#1A202C;
  animation:tsscMPup .26s cubic-bezier(.16,1,.3,1);}
.tsscMP-box *{font-style:normal;}
@keyframes tsscMPup{from{transform:translateY(12px);opacity:0}to{transform:none;opacity:1}}
.tsscMP-top{background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;
  padding:.5rem .8rem;font-weight:700;font-size:.76rem;letter-spacing:.5px;}
.tsscMP-x{position:absolute;top:6px;right:8px;width:26px;height:26px;border:0;border-radius:100px;
  background:rgba(255,255,255,.24);color:#fff;font-size:1rem;line-height:1;cursor:pointer;}
.tsscMP-x:hover{background:rgba(255,255,255,.42);}
.tsscMP-body{padding:.9rem 1rem 1rem;}
.tsscMP-big{font-family:'Baloo 2',sans-serif;font-weight:800;font-size:2.1rem;line-height:1;
  margin:0;color:#1A202C;}
.tsscMP-big span{color:#FF6B00;}
.tsscMP-kicker{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.9rem;
  color:#4A5568;margin:.15rem 0 .6rem;}
.tsscMP-pills{display:flex;gap:.35rem;justify-content:center;flex-wrap:wrap;margin-bottom:.6rem;}
.tsscMP-pill{border-radius:100px;padding:.2rem .6rem;font-size:.72rem;font-weight:600;
  letter-spacing:.5px;background:#FFF7F0;border:1px solid #FFEDD5;color:#CC5500;}
.tsscMP-pill.g{background:#ECFDF5;border-color:#A7F3D0;color:#00875A;}
.tsscMP-band{background:linear-gradient(135deg,#FFF7F0,#FFEDD5);color:#CC5500;
  font-weight:700;font-size:.85rem;padding:.42rem .5rem;margin:0 -1rem .7rem;
  border-top:1px solid #FFEDD5;border-bottom:1px solid #FFEDD5;}
.tsscMP-price{font-weight:600;font-size:.88rem;color:#718096;margin-bottom:.65rem;}
.tsscMP-was{text-decoration:line-through;}
.tsscMP-now{font-family:'Baloo 2',sans-serif;font-weight:800;font-size:1.6rem;
  color:#00A86B;margin:0 .3rem;vertical-align:-3px;}
.tsscMP-go{display:flex;align-items:center;justify-content:center;gap:.5rem;text-decoration:none;
  border-radius:10px;padding:.85rem 1rem;color:#fff;letter-spacing:.4px;
  font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1rem;
  background:linear-gradient(120deg,#6D28D9,#DB2777,#F59E0B);background-size:200% 200%;
  box-shadow:0 4px 22px rgba(219,39,119,0.4);animation:tsscMPgrad 5s ease infinite;}
@keyframes tsscMPgrad{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.tsscMP-free{font-size:.78rem;font-weight:600;color:#00875A;margin:.55rem 0 0;}
@media(prefers-reduced-motion:reduce){#tsscMP.on,.tsscMP-box,.tsscMP-go{animation:none}}
</style>

<div id="tsscMP" role="dialog" aria-modal="true" aria-labelledby="tsscMPh">
  <div class="tsscMP-box">
    <div class="tsscMP-top">&#128227; SSC CGL MOCK TESTS 2026</div>
    <button class="tsscMP-x" type="button" aria-label="Close">&times;</button>
    <div class="tsscMP-body">
      <h2 class="tsscMP-big" id="tsscMPh">100 <span>MOCKS</span></h2>
      <div class="tsscMP-kicker">PYQs show the pattern. Mocks show your rank.</div>
      <div class="tsscMP-pills">
        <span class="tsscMP-pill">50 Tier I &middot; live now</span>
        <span class="tsscMP-pill g">50 Tier II &middot; 15 Oct 2026</span>
      </div>
      <div class="tsscMP-band">Real Sectional Timing &mdash; Just Like The Exam</div>
      <div class="tsscMP-price">
        <span class="tsscMP-was">&#8377;199</span><span class="tsscMP-now">&#8377;49</span>for a full year
      </div>
      <a class="tsscMP-go" href="https://trickyssc.com/ssc-cgl-mock-test">&#128640; START NOW</a>
      <p class="tsscMP-free">Mocks 1&ndash;4 free &mdash; no payment needed</p>
    </div>
  </div>
</div>

<script>
(function(){
  var KEY='tsscMockPromoSeen', PAID='tssc_entitlement', DELAY=1200;
  var box=document.getElementById('tsscMP');
  if(!box) return;
  // Never nag someone who already paid. localStorage only — no Firestore read,
  // so these pages stay at zero read cost per pageview.
  try{
    var p=localStorage.getItem(PAID);
    if(p && p!=='false' && p!=='null' && p!=='0') return;
  }catch(e){}
  // sessionStorage, not localStorage: the flag dies when the browser session
  // ends, so a visitor sees the popup once per visit to the site and again
  // the next time they come back. Shared across index / cgl-pyq / chsl-pyq.
  try{ if(sessionStorage.getItem(KEY)) return; }catch(e){}
  function close(){
    box.classList.remove('on');
    try{ sessionStorage.setItem(KEY,'1'); }catch(e){}
  }
  setTimeout(function(){ box.classList.add('on'); }, DELAY);
  box.querySelector('.tsscMP-x').addEventListener('click',close);
  box.addEventListener('click',function(e){ if(e.target===box) close(); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') close(); });
  box.querySelector('.tsscMP-go').addEventListener('click',function(){
    try{ sessionStorage.setItem(KEY,'1'); }catch(e){}
  });
})();
</script>
<!-- TSSC:MOCK-PROMO:END -->
"""


# ---------------------------------------------------------------------------
# 1. FETCH ALL PAPERS (with pagination)
# ---------------------------------------------------------------------------
def fetch_all_papers():
    papers = []
    page_token = None
    pages = 0
    while True:
        url = f"{REST_BASE}?pageSize=300&key={API_KEY}"
        if page_token:
            url += f"&pageToken={urllib.parse.quote(page_token)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.load(resp)
        except urllib.error.HTTPError as e:
            sys.stderr.write(
                f"ERROR reading Firestore ({e.code}): {e.read().decode()[:300]}\n"
            )
            sys.exit(1)

        for doc in data.get("documents", []):
            fields = doc.get("fields", {})
            rec = {k: _unwrap(v) for k, v in fields.items()}
            papers.append(rec)

        page_token = data.get("nextPageToken")
        pages += 1
        if not page_token or pages > 20:  # safety cap
            break

    return papers


def _unwrap(value):
    """Convert a Firestore typed value into a plain Python value."""
    if "stringValue" in value:
        return value["stringValue"]
    if "integerValue" in value:
        return int(value["integerValue"])
    if "doubleValue" in value:
        return float(value["doubleValue"])
    if "booleanValue" in value:
        return value["booleanValue"]
    if "timestampValue" in value:
        return value["timestampValue"]
    if "nullValue" in value:
        return None
    return ""


# ---------------------------------------------------------------------------
# 2. ORGANIZE: merge EN/HI, group by year
# ---------------------------------------------------------------------------
def organize(papers):
    """
    Returns: { year: [ paper_group, ... ] } sorted newest year first,
    each paper_group sorted by (date desc, shift asc).
    A paper_group merges the EN and HI docs of the same paper.
    """
    # key that identifies "the same paper" regardless of language
    groups = {}
    for p in papers:
        if p.get("exam") != EXAM_FILTER:
            continue
        if not p.get("paperId"):
            continue

        key = (
            p.get("exam", ""),
            str(p.get("year", "")),
            p.get("tier", ""),
            p.get("shift", ""),
            p.get("heldOn", ""),
        )
        g = groups.setdefault(key, {
            "exam": p.get("exam", ""),
            "year": str(p.get("year", "")),
            "tier": p.get("tier", ""),
            "shift": p.get("shift", ""),
            "heldOn": p.get("heldOn", ""),
            "questionCount": p.get("questionCount", ""),
            "langs": {},  # 'en' -> paperId, 'hi' -> paperId
        })
        lang = (p.get("language") or "en").lower()
        g["langs"][lang] = p.get("paperId")
        if p.get("questionCount"):
            g["questionCount"] = p.get("questionCount")

    by_year = defaultdict(list)
    for g in groups.values():
        by_year[g["year"]].append(g)

    # sort within each year: newest date first, then shift ascending
    def shift_num(s):
        digits = "".join(ch for ch in str(s) if ch.isdigit())
        return int(digits) if digits else 0

    for yr in by_year:
        # newest date first; within the same date, shift ascending (1,2,3)
        by_year[yr].sort(
            key=lambda g: (g["heldOn"], -shift_num(g["shift"])),
            reverse=True,
        )
        # the reverse=True above flips shift too; re-fix same-date ordering
        from itertools import groupby
        items = by_year[yr]
        fixed = []
        for _date, grp in groupby(items, key=lambda g: g["heldOn"]):
            same = list(grp)
            same.sort(key=lambda g: shift_num(g["shift"]))  # 1,2,3 ascending
            fixed.extend(same)
        by_year[yr] = fixed

    # years newest first
    ordered = dict(
        sorted(by_year.items(), key=lambda kv: kv[0], reverse=True)
    )
    return ordered


# ---------------------------------------------------------------------------
# 3. URL + LABEL HELPERS
# ---------------------------------------------------------------------------
def test_url(group, lang):
    pid = group["langs"][lang]
    parts = {
        "exam": group["exam"],
        "year": group["year"],
        "tier": group["tier"],
        "shift": group["shift"],
        "heldOn": group["heldOn"],
        "lang": lang,
        "paperId": pid,
    }
    qs = "&".join(
        f"{k}={urllib.parse.quote(str(v))}" for k, v in parts.items()
    )
    # Tier II papers run on a different engine, matching the live site.
    tv = str(group.get("tier", "")).lower()
    is_t2 = not (
        "tier1" in tv or "tier-1" in tv or tv == "tier i"
        or "paper1" in tv or "paper-1" in tv or tv == "paper i"
    )
    engine = "test-tier2.html" if is_t2 else "test.html"
    return f"{SITE}/{engine}?{qs}"


def pretty_date(held_on):
    # held_on like "2025-09-24"
    try:
        y, m, d = held_on.split("-")
        return f"{int(d)} {MONTHS.get(m, m)} {y}"
    except Exception:
        return held_on


def tier_label(tier):
    t = str(tier).lower()
    if "2" in t or "ii" in t:
        return "Tier II"
    return "Tier I"


# ---------------------------------------------------------------------------
# 4. RENDER HTML
# ---------------------------------------------------------------------------
def render(ordered):
    total_papers = sum(len(v) for v in ordered.values())
    updated = datetime.datetime.utcnow().strftime("%d %b %Y")

    YEAR_COLORS = ['#FF6B00', '#6366F1', '#00A86B', '#0EA5E9',
                   '#E11D48', '#F59E0B', '#8B5CF6', '#10B981']

    def is_tier2(t):
        v = str(t).lower()
        return not (
            'tier1' in v or 'tier-1' in v or v == 'tier i'
            or 'paper1' in v or 'paper-1' in v or v == 'paper i'
        )

    tier1, tier2 = {}, {}
    for y, groups in ordered.items():
        g1 = [g for g in groups if not is_tier2(g["tier"])]
        g2 = [g for g in groups if is_tier2(g["tier"])]
        if g1:
            tier1[y] = g1
        if g2:
            tier2[y] = g2

    def shift_badge(shift):
        m = re.search(r'Shift[- ]?(\d+)', str(shift), re.I)
        if m:
            return (f'<span style="display:inline-flex;align-items:center;'
                    f'justify-content:center;width:20px;height:20px;'
                    f'border-radius:5px;background:#F1F5F9;'
                    f"font-family:'Rajdhani',sans-serif;font-weight:700;"
                    f'font-size:0.7rem;color:#475569;">S{m.group(1)}</span>')
        if shift:
            return (f'<span style="background:#F1F5F9;border-radius:5px;'
                    f"padding:0.1rem 0.35rem;font-family:'Rajdhani',sans-serif;"
                    f'font-weight:700;font-size:0.7rem;color:#475569;">'
                    f'{html.escape(str(shift))}</span>')
        return ''

    def render_tier(tier_map, tier_label, tier_id):
        """Build the year-grouped cards for one tier, matching the live design."""
        if not tier_map:
            return ('<div style="text-align:center;padding:3rem;background:white;'
                    'border-radius:16px;border:1px solid #E2E8F0;color:#718096;">'
                    '<div style="font-size:2rem;margin-bottom:0.5rem;">📭</div>'
                    '<div style="font-weight:700;margin-bottom:0.25rem;">'
                    'Coming Soon</div>'
                    '<div style="font-size:0.85rem;">Papers will appear here as '
                    'they are added.</div></div>')

        is_t2 = (tier_id == 't2')
        time_label = '135 min' if is_t2 else '60 min'
        marks_label = '450 marks' if is_t2 else '200 marks'

        year_keys = list(tier_map.keys())  # already sorted newest-first
        blocks = []
        for yi, year in enumerate(year_keys):
            accent = YEAR_COLORS[yi % len(YEAR_COLORS)]
            groups = tier_map[year]
            ycount = len(groups)

            rows = []
            for pi, g in enumerate(groups):
                shift = g["shift"] or ''
                shift_disp = shift if shift else 'Full Paper'
                qc = g.get("questionCount") or (150 if is_t2 else 100)
                date_label = pretty_date(g["heldOn"]) if g["heldOn"] else ''
                is_last = (pi == len(groups) - 1)
                border_bottom = '' if is_last else 'border-bottom:1px solid #F1F5F9;'

                # language buttons — direct links (static, crawlable)
                # Unique id for this paper's language-chooser entry
                pick_id = re.sub(r'[^a-zA-Z0-9_-]', '_',
                                 f"{g['exam']}-{tier_id}-{year}-{g['shift']}-{g['heldOn']}")
                url_en = test_url(g, "en") if "en" in g["langs"] else ""
                url_hi = test_url(g, "hi") if "hi" in g["langs"] else ""
                pid_en = g["langs"].get("en", "")
                pid_hi = g["langs"].get("hi", "")
                pick_title = f"SSC CGL {tier_label} {year}"
                if shift:
                    pick_title += f" · {shift}"
                if date_label:
                    pick_title += f" · {date_label}"

                # Register this paper for the overlay (data-* attributes read by JS)
                reg = (
                    f'data-pick="{html.escape(pick_id)}" '
                    f'data-en="{html.escape(url_en)}" '
                    f'data-hi="{html.escape(url_hi)}" '
                    f'data-pid-en="{html.escape(pid_en)}" '
                    f'data-pid-hi="{html.escape(pid_hi)}" '
                    f'data-title="{html.escape(pick_title)}"'
                )

                # Visible "Attempt Test" button → opens language overlay.
                # Hidden crawlable <a> links keep the test URLs in the static
                # HTML so Google can still discover every paper.
                attempt_btn = (
                    f'<button class="pyq-attempt-btn" {reg} '
                    f'onclick="openLangChooser(this)" '
                    f'style="display:inline-flex;align-items:center;gap:0.35rem;'
                    f'background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;'
                    f'border:none;padding:0.55rem 1.05rem;border-radius:9px;'
                    f"font-family:'Rajdhani',sans-serif;font-weight:700;"
                    f'font-size:0.85rem;cursor:pointer;white-space:nowrap;'
                    f'box-shadow:0 3px 10px rgba(255,107,0,0.25);">'
                    f'▶ Attempt Test</button>'
                )
                hidden_links = ''
                if url_en:
                    hidden_links += f'<a href="{html.escape(url_en)}" style="display:none" aria-hidden="true" tabindex="-1">English</a>'
                if url_hi:
                    hidden_links += f'<a href="{html.escape(url_hi)}" style="display:none" aria-hidden="true" tabindex="-1">हिंदी</a>'

                # Attempted pill — JS flips it to "Attempted" after auth+sync.
                pill = (
                    f'<span class="attempt-pill todo" data-pill="{html.escape(pick_id)}">'
                    f'○ Not Attempted</span>'
                )
                btns_html = attempt_btn + hidden_links

                rows.append(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;gap:0.6rem;padding:0.85rem 1.1rem;{border_bottom}background:white;">
              <div style="display:flex;align-items:center;gap:0.7rem;min-width:0;">
                <div style="min-width:0;">
                  <div style="display:flex;align-items:center;gap:0.45rem;flex-wrap:wrap;">
                    <span style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:0.95rem;color:#1A202C;">{html.escape(shift_disp)}</span>
                    {shift_badge(shift)}
                    {f'<span style="font-size:0.82rem;color:#475569;">{html.escape(date_label)}</span>' if date_label else ''}
                  </div>
                  <div style="display:flex;align-items:center;gap:0.5rem;margin-top:0.2rem;flex-wrap:wrap;">
                    <span style="font-size:0.72rem;color:#94A3B8;">📝 {qc} Qs</span>
                    <span style="font-size:0.72rem;color:#94A3B8;">·</span>
                    <span style="font-size:0.72rem;color:#94A3B8;">⏱ {time_label}</span>
                    <span style="font-size:0.72rem;color:#94A3B8;">·</span>
                    <span style="font-size:0.72rem;color:#94A3B8;">{marks_label}</span>
                    {pill}
                  </div>
                </div>
              </div>
              <div style="display:flex;align-items:center;gap:0.4rem;flex-shrink:0;flex-wrap:wrap;justify-content:flex-end;">{btns_html}</div>
            </div>""")

            # Newest year opens by default; older years start collapsed.
            open_attr = ' open' if yi == 0 else ''
            blocks.append(f"""
        <details class="yr-acc"{open_attr}>
          <summary class="yr-head">
            <span class="yr-badge" style="background:{accent};">{year}</span>
            <span class="yr-title">SSC CGL {tier_label} {year}</span>
            <span class="yr-count">{ycount} test{'s' if ycount != 1 else ''}</span>
            <span class="yr-chev" aria-hidden="true">▾</span>
          </summary>
          <div class="yr-body" style="border-left:3px solid {accent};">{''.join(rows)}</div>
        </details>""")
        return "".join(blocks)

    t1_html = render_tier(tier1, "Tier I", "t1")
    t2_html = render_tier(tier2, "Tier II", "t2")

    t1_count = sum(len(v) for v in tier1.values())
    t2_count = sum(len(v) for v in tier2.values())

    # ---- schema for SEO ----
    item_list = []
    pos = 1
    for y, groups in ordered.items():
        for g in groups:
            lang = "en" if "en" in g["langs"] else next(iter(g["langs"]))
            item_list.append({
                "@type": "ListItem",
                "position": pos,
                "name": f"SSC CGL {pretty_date(g['heldOn'])} {g['shift']} — Free Online Test",
                "url": test_url(g, lang),
            })
            pos += 1

    itemlist_schema = {
        "@context": "https://schema.org", "@type": "ItemList",
        "name": "Free SSC CGL PYQ Tests (Previous Year Papers) — Online in Hindi & English",
        "numberOfItems": total_papers, "itemListElement": item_list,
    }

    faq_schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": "Are SSC CGL previous year papers free on TrickySSC?",
             "acceptedAnswer": {"@type": "Answer", "text": "Yes. All SSC CGL Tier 1 previous year question papers (PYQ) on TrickySSC are completely free to attempt online. No payment or subscription is required."}},
            {"@type": "Question", "name": "Can I attempt SSC CGL PYQ papers in Hindi and English?",
             "acceptedAnswer": {"@type": "Answer", "text": "Yes. Every SSC CGL previous year paper is available in both English and Hindi. You can choose your preferred language before starting the test."}},
            {"@type": "Question", "name": "Do the SSC CGL PYQ tests include answer keys and solutions?",
             "acceptedAnswer": {"@type": "Answer", "text": "Yes. Each paper comes with the correct answer key and step-by-step solutions so you can review every question after submitting the test."}},
            {"@type": "Question", "name": "Which SSC CGL years are available for practice?",
             "acceptedAnswer": {"@type": "Answer", "text": "TrickySSC provides shift-wise SSC CGL previous year papers across multiple years, including the most recent 2025 Tier 1 exam shifts, added regularly as new papers are processed."}},
            {"@type": "Question", "name": "Is the test interface similar to the real SSC CGL exam?",
             "acceptedAnswer": {"@type": "Answer", "text": "Yes. The online test engine mirrors the real SSC CGL exam pattern with sectional layout, a question palette, a timer, and negative marking, so you practice in exam-like conditions."}},
            {"@type": "Question", "name": "Are SSC CGL PYQ tests free?",
             "acceptedAnswer": {"@type": "Answer", "text": "Yes. Every SSC CGL PYQ test on TrickySSC is completely free to attempt online — no payment, subscription, or hidden charges."}},
            {"@type": "Question", "name": "Where can I attempt SSC CGL PYQ tests online?",
             "acceptedAnswer": {"@type": "Answer", "text": "You can attempt SSC CGL PYQ tests online at TrickySSC (trickyssc.com). Shift-wise Tier I and Tier II previous year papers are available in a real exam-like interface with timer and solutions."}},
            {"@type": "Question", "name": "Which website provides free SSC CGL previous year paper tests?",
             "acceptedAnswer": {"@type": "Answer", "text": "TrickySSC provides free SSC CGL previous year paper tests online, shift-wise, in both English and Hindi, with answer keys and step-by-step solutions for every question."}},
        ],
    }

    faq_visible = """
      <div style="margin-top:2rem;">
        <h2 style="font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1.25rem;color:#1A202C;margin:0 0 0.8rem;display:flex;align-items:center;gap:0.5rem;"><span style="display:inline-block;width:3px;height:18px;background:linear-gradient(180deg,#FF6B00,#FF8C38);border-radius:2px;"></span>Frequently Asked Questions</h2>
        <details style="background:#fff;border:1px solid #E2E8F0;border-radius:11px;padding:0.85rem 1.1rem;margin-bottom:0.6rem;"><summary style="cursor:pointer;font-weight:700;font-size:0.92rem;color:#1A202C;">Are SSC CGL previous year papers free on TrickySSC?</summary><p style="color:#4A5568;margin:0.6rem 0 0;font-size:0.88rem;">Yes. All SSC CGL Tier 1 previous year question papers (PYQ) on TrickySSC are completely free to attempt online. No payment or subscription is required.</p></details>
        <details style="background:#fff;border:1px solid #E2E8F0;border-radius:11px;padding:0.85rem 1.1rem;margin-bottom:0.6rem;"><summary style="cursor:pointer;font-weight:700;font-size:0.92rem;color:#1A202C;">Can I attempt SSC CGL PYQ papers in Hindi and English?</summary><p style="color:#4A5568;margin:0.6rem 0 0;font-size:0.88rem;">Yes. Every SSC CGL previous year paper is available in both English and Hindi. Choose your preferred language before starting the test.</p></details>
        <details style="background:#fff;border:1px solid #E2E8F0;border-radius:11px;padding:0.85rem 1.1rem;margin-bottom:0.6rem;"><summary style="cursor:pointer;font-weight:700;font-size:0.92rem;color:#1A202C;">Do the tests include answer keys and solutions?</summary><p style="color:#4A5568;margin:0.6rem 0 0;font-size:0.88rem;">Yes. Each paper comes with the correct answer key and step-by-step solutions, so you can review every question after submitting the test.</p></details>
        <details style="background:#fff;border:1px solid #E2E8F0;border-radius:11px;padding:0.85rem 1.1rem;margin-bottom:0.6rem;"><summary style="cursor:pointer;font-weight:700;font-size:0.92rem;color:#1A202C;">Which SSC CGL years are available?</summary><p style="color:#4A5568;margin:0.6rem 0 0;font-size:0.88rem;">Shift-wise SSC CGL previous year papers across multiple years, including the most recent 2025 Tier 1 exam shifts, added regularly as new papers are processed.</p></details>
        <details style="background:#fff;border:1px solid #E2E8F0;border-radius:11px;padding:0.85rem 1.1rem;margin-bottom:0.6rem;"><summary style="cursor:pointer;font-weight:700;font-size:0.92rem;color:#1A202C;">Is the interface similar to the real SSC CGL exam?</summary><p style="color:#4A5568;margin:0.6rem 0 0;font-size:0.88rem;">Yes. The test engine mirrors the real exam pattern with a sectional layout, question palette, timer, and negative marking for exam-like practice.</p></details>
        <details style="background:#fff;border:1px solid #E2E8F0;border-radius:11px;padding:0.85rem 1.1rem;margin-bottom:0.6rem;"><summary style="cursor:pointer;font-weight:700;font-size:0.92rem;color:#1A202C;">Are SSC CGL PYQ tests free?</summary><p style="color:#4A5568;margin:0.6rem 0 0;font-size:0.88rem;">Yes. Every SSC CGL PYQ test on TrickySSC is completely free to attempt online — no payment, subscription, or hidden charges.</p></details>
        <details style="background:#fff;border:1px solid #E2E8F0;border-radius:11px;padding:0.85rem 1.1rem;margin-bottom:0.6rem;"><summary style="cursor:pointer;font-weight:700;font-size:0.92rem;color:#1A202C;">Where can I attempt SSC CGL PYQ tests online?</summary><p style="color:#4A5568;margin:0.6rem 0 0;font-size:0.88rem;">You can attempt SSC CGL PYQ tests online at TrickySSC (trickyssc.com). Shift-wise Tier I and Tier II previous year papers are available in a real exam-like interface with timer and solutions.</p></details>
        <details style="background:#fff;border:1px solid #E2E8F0;border-radius:11px;padding:0.85rem 1.1rem;margin-bottom:0.6rem;"><summary style="cursor:pointer;font-weight:700;font-size:0.92rem;color:#1A202C;">Which website provides free SSC CGL previous year paper tests?</summary><p style="color:#4A5568;margin:0.6rem 0 0;font-size:0.88rem;">TrickySSC provides free SSC CGL previous year paper tests online, shift-wise, in both English and Hindi, with answer keys and step-by-step solutions for every question.</p></details>
      </div>"""

    seo_content = f"""
    <div style="margin-top:2rem;">
      <h2 style="font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1.25rem;color:#1A202C;margin:0 0 0.8rem;display:flex;align-items:center;gap:0.5rem;"><span style="display:inline-block;width:3px;height:18px;background:linear-gradient(180deg,#FF6B00,#FF8C38);border-radius:2px;"></span>Free SSC CGL PYQ Tests</h2>
      <p style="color:#4A5568;margin:0;font-size:0.9rem;line-height:1.6;">All SSC CGL PYQ tests on TrickySSC are completely free. You can attempt every previous year paper online without downloading PDFs. Each test follows the actual SSC CGL exam pattern and includes detailed solutions.</p>
    </div>

    <div style="margin-top:2rem;">
      <h2 style="font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1.25rem;color:#1A202C;margin:0 0 0.8rem;display:flex;align-items:center;gap:0.5rem;"><span style="display:inline-block;width:3px;height:18px;background:linear-gradient(180deg,#FF6B00,#FF8C38);border-radius:2px;"></span>What is SSC CGL?</h2>
      <p style="color:#4A5568;margin:0 0 0.7rem;font-size:0.9rem;line-height:1.6;">SSC CGL (Staff Selection Commission Combined Graduate Level Examination) is one of India's most prestigious government recruitment examinations. Conducted annually by the Staff Selection Commission (SSC), the exam recruits candidates for various Group B and Group C posts in central government ministries, departments, constitutional bodies, and organizations.</p>
      <p style="color:#4A5568;margin:0 0 0.7rem;font-size:0.9rem;line-height:1.6;">Through SSC CGL, candidates can secure highly sought-after posts such as Income Tax Inspector, Assistant Section Officer (ASO), Examiner, Preventive Officer, Central Excise Inspector, Auditor, Accountant, Tax Assistant, Divisional Accountant, and several other government positions. Due to excellent career growth, job security, government benefits, and attractive salary packages, SSC CGL attracts lakhs of aspirants every year.</p>
      <p style="color:#4A5568;margin:0;font-size:0.9rem;line-height:1.6;">Success in SSC CGL requires strong conceptual understanding, speed, accuracy, and continuous practice through previous year papers and mock tests. TrickySSC helps aspirants prepare effectively through SSC CGL Previous Year Papers, <a href="{SITE}/mock-list.html?exam=ssc-cgl" style="color:#FF6B00;font-weight:600;">online mock tests</a>, chapter-wise practice tests, detailed solutions, and exam-oriented resources.</p>
    </div>

    <div style="margin-top:2rem;">
      <h2 style="font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1.25rem;color:#1A202C;margin:0 0 0.8rem;display:flex;align-items:center;gap:0.5rem;"><span style="display:inline-block;width:3px;height:18px;background:linear-gradient(180deg,#FF6B00,#FF8C38);border-radius:2px;"></span>SSC CGL Previous Year Papers Online Test</h2>
      <p style="color:#4A5568;margin:0 0 0.7rem;font-size:0.9rem;line-height:1.6;">SSC CGL Previous Year Papers are among the most reliable resources for exam preparation. They provide direct insight into the actual exam pattern, difficulty level, question trends, and frequently asked concepts. Unlike random practice questions, PYQs help candidates understand exactly how SSC frames questions and what topics are repeatedly tested.</p>
      <p style="color:#4A5568;margin:0 0 0.7rem;font-size:0.9rem;line-height:1.6;">At TrickySSC, candidates can attempt SSC CGL Previous Year Papers online in a real exam-like environment. Instead of downloading PDFs and manually evaluating answers, aspirants can practice complete shift-wise papers, track performance, analyze mistakes, and improve speed through online testing.</p>
      <p style="color:#4A5568;margin:0 0 0.7rem;font-size:0.9rem;line-height:1.6;">Our SSC CGL PYQ Test Series includes papers from multiple years and examination shifts. Each paper follows the actual SSC pattern and helps candidates gain familiarity with Quantitative Aptitude, General Intelligence &amp; Reasoning, English Language, and General Awareness questions asked in recent examinations.</p>
      <p style="color:#4A5568;margin:0 0 0.5rem;font-size:0.9rem;line-height:1.6;">Regular practice of SSC CGL Previous Year Papers helps candidates:</p>
      <ul style="color:#4A5568;font-size:0.9rem;line-height:1.7;margin:0 0 0.7rem 1.2rem;padding:0;">
        <li>Understand actual SSC exam difficulty.</li>
        <li>Identify important and recurring concepts.</li>
        <li>Improve question selection strategy.</li>
        <li>Develop effective time management skills.</li>
        <li>Increase accuracy and confidence.</li>
        <li>Strengthen weak areas through repeated practice.</li>
        <li>Improve overall exam readiness.</li>
      </ul>
      <p style="color:#4A5568;margin:0;font-size:0.9rem;line-height:1.6;">Candidates preparing for SSC CGL Tier I and Tier II should make previous year paper practice a regular part of their preparation strategy.</p>
    </div>

    <div style="margin-top:2rem;">
      <h2 style="font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1.25rem;color:#1A202C;margin:0 0 0.8rem;display:flex;align-items:center;gap:0.5rem;"><span style="display:inline-block;width:3px;height:18px;background:linear-gradient(180deg,#FF6B00,#FF8C38);border-radius:2px;"></span>Why Solve SSC CGL Previous Year Papers?</h2>
      <p style="color:#4A5568;margin:0 0 0.7rem;font-size:0.9rem;line-height:1.6;">SSC CGL Previous Year Papers offer a clear understanding of what candidates can expect in the actual examination. Since these papers contain real questions asked by SSC, they provide the most authentic preparation experience available.</p>
      <p style="color:#4A5568;margin:0 0 0.5rem;font-size:0.9rem;line-height:1.6;">Benefits of solving SSC CGL PYQs include:</p>
      <ul style="color:#4A5568;font-size:0.9rem;line-height:1.7;margin:0 0 0.7rem 1.2rem;padding:0;">
        <li>Understanding the latest exam pattern.</li>
        <li>Recognizing important and recurring topics.</li>
        <li>Learning exam-oriented solving techniques.</li>
        <li>Improving speed and accuracy.</li>
        <li>Building confidence before the examination.</li>
        <li>Identifying strengths and weaknesses.</li>
        <li>Practicing under actual exam conditions.</li>
        <li>Reducing examination anxiety through familiarity.</li>
      </ul>
      <p style="color:#4A5568;margin:0;font-size:0.9rem;line-height:1.6;">Many successful SSC candidates consider previous year paper practice one of the most important factors behind their success.</p>
    </div>

    <div style="margin-top:2rem;">
      <h2 style="font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1.25rem;color:#1A202C;margin:0 0 0.8rem;display:flex;align-items:center;gap:0.5rem;"><span style="display:inline-block;width:3px;height:18px;background:linear-gradient(180deg,#FF6B00,#FF8C38);border-radius:2px;"></span>SSC CGL Exam Pattern</h2>
      <h3 style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.02rem;color:#0F4C81;margin:0 0 0.5rem;">Tier I Examination</h3>
      <div style="overflow-x:auto;margin:0 0 0.8rem;-webkit-overflow-scrolling:touch;">
        <table style="width:100%;border-collapse:collapse;min-width:420px;font-size:0.86rem;color:#334155;">
          <thead>
            <tr>
              <th style="background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;font-family:'Rajdhani',sans-serif;font-weight:700;border:1px solid #FF8C38;padding:0.55rem 0.7rem;text-align:left;">Subject</th>
              <th style="background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;font-family:'Rajdhani',sans-serif;font-weight:700;border:1px solid #FF8C38;padding:0.55rem 0.7rem;text-align:left;">Questions</th>
              <th style="background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;font-family:'Rajdhani',sans-serif;font-weight:700;border:1px solid #FF8C38;padding:0.55rem 0.7rem;text-align:left;">Marks</th>
            </tr>
          </thead>
          <tbody>
            <tr><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">General Intelligence &amp; Reasoning</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">25</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">50</td></tr>
            <tr style="background:#F8FAFC;"><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">General Awareness</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">25</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">50</td></tr>
            <tr><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Quantitative Aptitude</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">25</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">50</td></tr>
            <tr style="background:#F8FAFC;"><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">English Comprehension</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">25</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">50</td></tr>
            <tr style="background:#FFF7ED;font-weight:700;"><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Total</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">100</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">200</td></tr>
          </tbody>
        </table>
      </div>
      <p style="color:#4A5568;margin:0 0 0.5rem;font-size:0.9rem;line-height:1.6;">⏱ <strong>Duration:</strong> 60 Minutes</p>
      <p style="color:#4A5568;margin:0 0 0.4rem;font-size:0.9rem;line-height:1.6;"><strong>Key Highlights:</strong></p>
      <ul style="color:#4A5568;font-size:0.9rem;line-height:1.7;margin:0 0 0 1.2rem;padding:0;">
        <li>Objective-type online examination.</li>
        <li>100 questions carrying 200 marks.</li>
        <li>Negative marking of 0.50 marks for each incorrect answer.</li>
        <li>Qualifying candidates proceed to Tier II.</li>
      </ul>

      <h3 style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.02rem;color:#0F4C81;margin:1.4rem 0 0.5rem;">Tier II Examination</h3>
      <p style="color:#4A5568;margin:0 0 0.7rem;font-size:0.9rem;line-height:1.6;">Tier II is the main scoring stage of SSC CGL and plays a major role in final selection. It evaluates candidates across Mathematical Abilities, Reasoning, English, General Awareness, Computer Knowledge, and Data Entry Skills.</p>
      <div style="overflow-x:auto;margin:0 0 0.8rem;-webkit-overflow-scrolling:touch;">
        <table style="width:100%;border-collapse:collapse;min-width:620px;font-size:0.84rem;color:#334155;">
          <thead>
            <tr>
              <th style="background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;font-family:'Rajdhani',sans-serif;font-weight:700;border:1px solid #FF8C38;padding:0.55rem 0.7rem;text-align:left;">Section &amp; Module</th>
              <th style="background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;font-family:'Rajdhani',sans-serif;font-weight:700;border:1px solid #FF8C38;padding:0.55rem 0.7rem;text-align:left;">Subject</th>
              <th style="background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;font-family:'Rajdhani',sans-serif;font-weight:700;border:1px solid #FF8C38;padding:0.55rem 0.7rem;text-align:left;">Questions / Tasks</th>
              <th style="background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;font-family:'Rajdhani',sans-serif;font-weight:700;border:1px solid #FF8C38;padding:0.55rem 0.7rem;text-align:left;">Marks</th>
              <th style="background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;font-family:'Rajdhani',sans-serif;font-weight:700;border:1px solid #FF8C38;padding:0.55rem 0.7rem;text-align:left;">Duration</th>
              <th style="background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;font-family:'Rajdhani',sans-serif;font-weight:700;border:1px solid #FF8C38;padding:0.55rem 0.7rem;text-align:left;">Nature</th>
            </tr>
          </thead>
          <tbody>
            <tr><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Section I – Module I</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Mathematical Abilities</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">30</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">180</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">1 Hour</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Merit Ranking</td></tr>
            <tr style="background:#F8FAFC;"><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Section I – Module II</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Reasoning &amp; General Intelligence</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">30</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Included Above</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Included Above</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Merit Ranking</td></tr>
            <tr><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Section II – Module I</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">English Language &amp; Comprehension</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">45</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">210</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">1 Hour</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Merit Ranking</td></tr>
            <tr style="background:#F8FAFC;"><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Section II – Module II</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">General Awareness</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">25</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Included Above</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Included Above</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Merit Ranking</td></tr>
            <tr><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Section III – Module I</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Computer Knowledge Test</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">20</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">60</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">15 Minutes</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Qualifying</td></tr>
            <tr style="background:#F8FAFC;"><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Section III – Module II</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Data Entry Speed Test</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">One Task</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">—</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">15 Minutes</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Qualifying</td></tr>
            <tr style="background:#FFF7ED;"><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Paper II</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">Statistics</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">100</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">200</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">2 Hours</td><td style="border:1px solid #E2E8F0;padding:0.5rem 0.7rem;">For Statistical Investigator Posts</td></tr>
          </tbody>
        </table>
      </div>
      <h3 style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.02rem;color:#0F4C81;margin:1rem 0 0.4rem;">Tier II Weightage</h3>
      <ul style="color:#4A5568;font-size:0.9rem;line-height:1.7;margin:0 0 0.7rem 1.2rem;padding:0;">
        <li>Maths + Reasoning ~46%</li>
        <li>English ~35%</li>
        <li>General Awareness ~19%</li>
        <li>Computer Test · Qualifying</li>
        <li>Data Entry · Qualifying</li>
      </ul>
      <p style="color:#4A5568;margin:0;font-size:0.9rem;line-height:1.6;">Candidates should focus heavily on Mathematics, Reasoning, and English, as these sections contribute the majority of marks in the final merit calculation.</p>
    </div>

    <div style="margin-top:2rem;">
      <h2 style="font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1.25rem;color:#1A202C;margin:0 0 0.8rem;display:flex;align-items:center;gap:0.5rem;"><span style="display:inline-block;width:3px;height:18px;background:linear-gradient(180deg,#FF6B00,#FF8C38);border-radius:2px;"></span>SSC CGL Syllabus</h2>
      <p style="color:#4A5568;margin:0 0 0.7rem;font-size:0.9rem;line-height:1.6;">SSC CGL primarily tests candidates across four major areas.</p>
      <h3 style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.02rem;color:#0F4C81;margin:0 0 0.3rem;">Quantitative Aptitude</h3>
      <p style="color:#4A5568;margin:0 0 0.8rem;font-size:0.9rem;line-height:1.6;">Percentage, Ratio &amp; Proportion, Profit &amp; Loss, Time &amp; Work, Time-Speed-Distance, Algebra, Geometry, Mensuration, Number System, Data Interpretation, and Arithmetic.</p>
      <h3 style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.02rem;color:#0F4C81;margin:0 0 0.3rem;">General Intelligence &amp; Reasoning</h3>
      <p style="color:#4A5568;margin:0 0 0.8rem;font-size:0.9rem;line-height:1.6;">Analogy, Classification, Coding-Decoding, Series, Blood Relations, Directions, Ranking, Syllogism, Statement-Based Questions, and Non-Verbal Reasoning.</p>
      <h3 style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.02rem;color:#0F4C81;margin:0 0 0.3rem;">English Language</h3>
      <p style="color:#4A5568;margin:0 0 0.8rem;font-size:0.9rem;line-height:1.6;">Reading Comprehension, Cloze Test, Error Spotting, Sentence Improvement, One Word Substitution, Vocabulary, Synonyms, Antonyms, and Grammar.</p>
      <h3 style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.02rem;color:#0F4C81;margin:0 0 0.3rem;">General Awareness</h3>
      <p style="color:#4A5568;margin:0;font-size:0.9rem;line-height:1.6;">History, Geography, Indian Polity, Economics, Science, Current Affairs, Static GK, Government Schemes, and National &amp; International Events.</p>
    </div>

    <div style="margin-top:2rem;">
      <h2 style="font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1.25rem;color:#1A202C;margin:0 0 0.8rem;display:flex;align-items:center;gap:0.5rem;"><span style="display:inline-block;width:3px;height:18px;background:linear-gradient(180deg,#FF6B00,#FF8C38);border-radius:2px;"></span>SSC CGL Preparation Strategy</h2>
      <p style="color:#4A5568;margin:0 0 0.7rem;font-size:0.9rem;line-height:1.6;">A successful SSC CGL preparation strategy combines concept building, revision, previous year paper practice, and mock testing.</p>
      <p style="color:#4A5568;margin:0 0 0.7rem;font-size:0.9rem;line-height:1.6;">Candidates should first complete important concepts and then focus on solving SSC CGL Previous Year Papers to understand actual question trends. Mock tests should be used regularly to improve speed, accuracy, and exam temperament.</p>
      <p style="color:#4A5568;margin:0 0 0.4rem;font-size:0.9rem;line-height:1.6;">A recommended preparation approach is:</p>
      <ol style="color:#4A5568;font-size:0.9rem;line-height:1.7;margin:0 0 0.7rem 1.3rem;padding:0;">
        <li>Complete the syllabus topic-wise.</li>
        <li>Practice chapter-wise questions regularly.</li>
        <li>Solve SSC CGL Previous Year Papers consistently.</li>
        <li>Attempt full-length mock tests every week.</li>
        <li>Analyze mistakes after every test.</li>
        <li>Revise weak topics continuously.</li>
        <li>Focus on accuracy before speed.</li>
        <li>Track performance and monitor progress.</li>
      </ol>
      <p style="color:#4A5568;margin:0;font-size:0.9rem;line-height:1.6;">Consistent practice and performance analysis often contribute more to success than repeatedly studying new topics.</p>
    </div>"""

    desc = (
        f"Attempt {total_papers}+ SSC CGL Tier 1 previous year question papers "
        f"(PYQ) free online, shift-wise, in English & Hindi with answer keys and "
        f"step-by-step solutions. Real exam-pattern interface, no payment needed."
    )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SSC CGL PYQ Tests Free | Previous Year Papers Online (Hindi &amp; English) | TrickySSC</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="keywords" content="SSC CGL PYQ, SSC CGL previous year paper, SSC CGL previous year paper online free, SSC CGL PYQ test, SSC CGL question paper with solution, SSC CGL 2025 paper, SSC CGL Tier 1 PYQ, SSC CGL free online test">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{SITE}/{OUTPUT_FILE}">
<meta property="og:type" content="website">
<meta property="og:title" content="SSC CGL PYQ Tests Free | Previous Year Papers Online (Hindi &amp; English)">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}/{OUTPUT_FILE}">
<meta property="og:site_name" content="TrickySSC">
<meta property="og:image" content="{SITE}/og-pyq.png">
<meta name="twitter:card" content="summary_large_image">
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Baloo+2:wght@400;500;600;700;800&family=Hind:wght@300;400;500;600&display=swap" rel="stylesheet">
<script type="application/ld+json">
{json.dumps(faq_schema, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(itemlist_schema, ensure_ascii=False)}
</script>
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:'Hind',sans-serif; background:#F0F2F7; color:#1A202C; }}
  a {{ text-decoration:none; }}
  nav.topbar {{ position:sticky; top:0; z-index:1000; background:#fff; box-shadow:0 2px 12px rgba(0,0,0,.08); border-bottom:1px solid #E2E8F0; padding:0 1.5rem; }}
  .nav-inner {{ max-width:1280px; margin:0 auto; display:flex; align-items:center; justify-content:space-between; height:64px; }}
  .logo {{ font-family:'Baloo 2',cursive; font-size:1.7rem; font-weight:800; letter-spacing:-.5px; color:#1A202C; }}
  .logo span {{ color:#FF6B00; }}
  .nav-links {{ display:flex; gap:.2rem; list-style:none; align-items:center; }}
  .nav-links a {{ padding:.5rem .75rem; font-size:.88rem; font-weight:500; color:#4A5568; border-radius:8px; }}
  .nav-links a:hover {{ background:#FFF7F0; color:#FF6B00; }}
  .nav-cta {{ background:#FF6B00; color:#fff !important; }}
  .nav-toggle {{ display:none; font-size:1.5rem; background:none; border:none; cursor:pointer; }}
  @media (max-width:900px) {{ .nav-links {{ display:none; }} .nav-toggle {{ display:block; }} }}
  details summary::-webkit-details-marker {{ display:none; }}
  .pyq-attempt-btn:hover {{ filter:brightness(1.05); }}
  /* ---- Language chooser overlay (matches ssc-cgl.html) ---- */
  #langChooser {{ display:none; position:fixed; inset:0; z-index:6000; background:rgba(15,23,42,0.55); backdrop-filter:blur(4px); animation:lcFade .18s ease; }}
  .lc-card {{ position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:min(400px,92vw); background:#fff; border-radius:22px; box-shadow:0 30px 80px rgba(15,23,42,0.4); overflow:hidden; animation:lcPop .24s cubic-bezier(.2,.8,.3,1.2); }}
  .lc-head {{ padding:1.6rem 1.5rem 0.4rem; text-align:center; background:linear-gradient(180deg,#FBFCFE 0%,#fff 100%); border-bottom:1px solid #F1F5F9; }}
  .lc-icon {{ width:54px; height:54px; border-radius:16px; background:linear-gradient(135deg,#0EA5E9,#6366F1); display:flex; align-items:center; justify-content:center; font-size:1.6rem; margin:0 auto 0.8rem; box-shadow:0 8px 20px rgba(99,102,241,0.3); }}
  .lc-title {{ font-family:'Rajdhani',sans-serif; font-weight:800; font-size:1.3rem; color:#1A202C; line-height:1.2; }}
  .lc-sub {{ font-size:0.8rem; color:#94A3B8; margin-top:0.35rem; line-height:1.35; font-weight:600; }}
  .lc-body {{ padding:1.2rem 1.4rem 1.5rem; display:flex; flex-direction:column; gap:0.75rem; }}
  .lc-opt {{ display:flex; align-items:center; gap:0.95rem; width:100%; border:1.5px solid #EBEFF4; background:#fff; border-radius:15px; padding:0.85rem 1rem; cursor:pointer; text-align:left; transition:all .16s ease; font-family:'Rajdhani',sans-serif; }}
  .lc-opt.en:hover {{ border-color:#6366F1; background:#F6F7FF; transform:translateY(-2px); box-shadow:0 8px 22px rgba(99,102,241,0.14); }}
  .lc-opt.hi:hover {{ border-color:#FF6B00; background:#FFF8F2; transform:translateY(-2px); box-shadow:0 8px 22px rgba(255,107,0,0.14); }}
  .lc-badge {{ width:48px; height:48px; border-radius:14px; flex-shrink:0; display:flex; align-items:center; justify-content:center; font-family:'Rajdhani',sans-serif; font-weight:800; font-size:1.55rem; color:#fff; line-height:1; }}
  .lc-opt.en .lc-badge {{ background:linear-gradient(135deg,#0EA5E9,#6366F1); box-shadow:0 5px 14px rgba(14,165,233,0.32); }}
  .lc-opt.hi .lc-badge {{ background:linear-gradient(135deg,#FF6B00,#FF8C38); box-shadow:0 5px 14px rgba(255,107,0,0.32); }}
  .lc-opt-main {{ flex:1; min-width:0; display:flex; flex-direction:column; gap:0.12rem; }}
  .lc-opt-name {{ font-weight:800; font-size:1.08rem; color:#1A202C; line-height:1.2; }}
  .lc-opt-desc {{ font-size:0.74rem; color:#94A3B8; font-weight:600; margin-top:0.1rem; }}
  .lc-arrow {{ flex-shrink:0; width:26px; height:26px; border-radius:50%; display:flex; align-items:center; justify-content:center; background:#F1F5F9; color:#94A3B8; font-size:0.95rem; font-weight:800; }}
  .lc-cancel {{ margin-top:0.15rem; background:none; border:none; color:#94A3B8; font-family:'Rajdhani',sans-serif; font-weight:700; font-size:0.85rem; cursor:pointer; padding:0.55rem; border-radius:8px; }}
  .attempt-pill {{ display:inline-flex; align-items:center; gap:0.25rem; white-space:nowrap; font-family:'Rajdhani',sans-serif; font-weight:700; font-size:0.68rem; padding:0.18rem 0.55rem; border-radius:100px; border:1px solid transparent; letter-spacing:0.2px; line-height:1.3; }}
  .attempt-pill.done {{ background:#E8F5E9; color:#15803D; border-color:#BBF7D0; }}
  .attempt-pill.todo {{ background:#F1F5F9; color:#64748B; border-color:#E2E8F0; }}
  /* ---- Year accordion (SSC CGL Tier I 2025 / 2024 …) ---- */
  .yr-acc {{ margin-bottom:1rem; }}
  .yr-head {{ list-style:none; cursor:pointer; display:flex; align-items:center; gap:0.9rem; padding:1rem 1.15rem; background:#fff; border:1px solid #E2E8F0; border-radius:15px; box-shadow:0 2px 8px rgba(0,0,0,0.05); -webkit-user-select:none; user-select:none; transition:border-color .15s, box-shadow .15s, transform .12s; }}
  .yr-head::-webkit-details-marker {{ display:none; }}
  .yr-head::marker {{ content:''; }}
  .yr-head:hover {{ border-color:#CBD5E1; box-shadow:0 5px 16px rgba(0,0,0,0.09); }}
  .yr-head:active {{ transform:scale(0.995); }}
  .yr-head:focus:not(:focus-visible) {{ outline:none; }}
  .yr-head:focus-visible {{ outline:2px solid #FF6B00; outline-offset:2px; }}
  .yr-badge {{ width:46px; height:46px; border-radius:11px; display:inline-flex; align-items:center; justify-content:center; font-family:'Rajdhani',sans-serif; font-weight:800; font-size:0.92rem; color:#fff; letter-spacing:-0.3px; flex-shrink:0; }}
  .yr-title {{ font-family:'Rajdhani',sans-serif; font-weight:800; font-size:1.32rem; color:#1A202C; line-height:1.15; }}
  .yr-count {{ background:#F1F5F9; border-radius:20px; padding:0.3rem 0.8rem; font-family:'Rajdhani',sans-serif; font-weight:700; font-size:0.88rem; color:#64748B; white-space:nowrap; flex-shrink:0; }}
  .yr-chev {{ margin-left:auto; flex-shrink:0; width:32px; height:32px; border-radius:50%; background:#F8FAFC; color:#94A3B8; display:inline-flex; align-items:center; justify-content:center; font-size:1.05rem; line-height:1; transition:transform .2s ease; }}
  details[open] > .yr-head .yr-chev {{ transform:rotate(180deg); background:#FFF1E6; color:#FF6B00; }}
  details[open] > .yr-head {{ border-bottom-left-radius:0; border-bottom-right-radius:0; }}
  .yr-body {{ background:#fff; border:1px solid #E2E8F0; border-top:none; border-radius:0 0 15px 15px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.05); }}
  @media (max-width:480px) {{
    .yr-head {{ gap:0.7rem; padding:0.8rem 0.85rem; }}
    .yr-badge {{ width:40px; height:40px; font-size:0.82rem; border-radius:10px; }}
    .yr-title {{ font-size:1.12rem; }}
    .yr-count {{ font-size:0.8rem; padding:0.24rem 0.65rem; }}
    .yr-chev {{ width:28px; height:28px; }}
  }}
  @keyframes lcFade {{ from{{opacity:0;}} to{{opacity:1;}} }}
  @keyframes lcPop {{ from{{opacity:0;transform:translate(-50%,-46%) scale(.96);}} to{{opacity:1;transform:translate(-50%,-50%) scale(1);}} }}
</style>
</head>
<body>

<nav class="topbar">
  <div class="nav-inner">
    <a href="{SITE}/index.html" class="logo">Tricky<span>SSC</span></a>
    <ul class="nav-links">
      <li><a href="{SITE}/index.html">Home</a></li>
      <li><a href="{SITE}/ssc-cgl.html">SSC CGL</a></li>
      <li><a href="{SITE}/ssc-cgl-pyq.html">PYQ Bank</a></li>
      <li><a href="{SITE}/ssc-cgl.html">Mock Tests</a></li>
      <li><a href="{SITE}/current-affairs.html">Current Affairs</a></li>
      <li><a href="{SITE}/login.html" class="nav-cta">Login</a></li>
    </ul>
    <button class="nav-toggle" onclick="var n=document.querySelector('.nav-links');n.style.display=(n.style.display==='flex'?'none':'flex')">☰</button>
  </div>
</nav>

<div style="background:#F0F2F7;min-height:100vh;padding-top:1.5rem;">

  <div style="max-width:960px;margin:0 auto;padding:0.2rem 1.25rem 0.2rem;">
    <h1 style="font-family:'Rajdhani',sans-serif;font-weight:800;font-size:clamp(1.1rem,4.2vw,1.55rem);line-height:1.25;color:#1A202C;margin:0;">Free SSC CGL PYQ Tests (Previous Year Papers) – Online in Hindi &amp; English</h1>
  </div>

  <div style="background:#fff;border-bottom:1px solid #E8ECF2;padding:0.55rem 1.5rem;margin-top:0.6rem;">
    <div style="max-width:960px;margin:0 auto;display:flex;align-items:center;gap:0.4rem;font-size:0.79rem;color:#94A3B8;">
      <a href="{SITE}/index.html" style="color:#FF6B00;font-weight:600;">Home</a>
      <span style="color:#CBD5E1;">›</span>
      <a href="{SITE}/ssc-cgl.html" style="color:#FF6B00;font-weight:600;">SSC CGL</a>
      <span style="color:#CBD5E1;">›</span>
      <span style="color:#475569;font-weight:600;">PYQ Papers</span>
    </div>
  </div>

  <div style="max-width:960px;margin:0 auto;padding:1.5rem 1rem 3rem;">

    <div style="background:linear-gradient(135deg,#1E1B4B 0%,#1E3A5F 55%,#0F4C81 100%);border-radius:18px;padding:1.6rem 1.75rem;margin-bottom:1.25rem;position:relative;overflow:hidden;box-shadow:0 8px 32px rgba(15,30,60,0.2);">
      <div style="position:absolute;top:-30px;right:-30px;width:160px;height:160px;background:rgba(255,107,0,0.1);border-radius:50%;pointer-events:none;"></div>
      <div style="position:absolute;bottom:-40px;right:80px;width:100px;height:100px;background:rgba(99,102,241,0.12);border-radius:50%;pointer-events:none;"></div>
      <div style="display:flex;align-items:center;gap:1rem;position:relative;">
        <div style="width:50px;height:50px;background:linear-gradient(135deg,#FF6B00,#FFB347);border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0;box-shadow:0 4px 16px rgba(255,107,0,0.45);">📋</div>
        <div>
          <div style="font-family:'Rajdhani',sans-serif;font-size:1.6rem;font-weight:800;color:#fff;margin:0;line-height:1.15;letter-spacing:0.2px;">SSC CGL Previous Year Papers</div>
          <p style="color:rgba(255,255,255,0.5);font-size:0.8rem;margin:0.25rem 0 0;letter-spacing:0.1px;">Tier I &amp; Tier II · 2010–2025 · {total_papers}+ Papers</p>
        </div>
      </div>
      <div style="display:flex;gap:0.75rem;margin-top:1.1rem;position:relative;flex-wrap:wrap;">
        <div style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.12);border-radius:8px;padding:0.3rem 0.7rem;display:flex;align-items:center;gap:0.35rem;"><span style="font-size:0.8rem;">📚</span><span style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:0.78rem;color:rgba(255,255,255,0.88);">{total_papers}+ Papers</span></div>
        <div style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.12);border-radius:8px;padding:0.3rem 0.7rem;display:flex;align-items:center;gap:0.35rem;"><span style="font-size:0.8rem;">🌐</span><span style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:0.78rem;color:rgba(255,255,255,0.88);">Hindi &amp; English</span></div>
        <div style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.12);border-radius:8px;padding:0.3rem 0.7rem;display:flex;align-items:center;gap:0.35rem;"><span style="font-size:0.8rem;">✅</span><span style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:0.78rem;color:rgba(255,255,255,0.88);">Step-by-step Solutions</span></div>
      </div>
    </div>

    <p style="color:#475569;font-size:0.9rem;line-height:1.55;margin:0 0 1.1rem;">Attempt <strong>free SSC CGL PYQ tests</strong> online — shift-wise Tier I &amp; Tier II previous year papers in Hindi &amp; English, with answer keys, detailed solutions and a real exam timer.</p>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;margin-bottom:1.5rem;">
      <button id="t1-btn" onclick="switchTier('t1')" style="padding:0.9rem 1rem;border-radius:13px;border:2px solid #FF6B00;background:linear-gradient(135deg,#FF6B00,#FF8C38);color:white;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1rem;cursor:pointer;box-shadow:0 4px 16px rgba(255,107,0,0.28);display:flex;align-items:center;justify-content:center;gap:0.45rem;">🎯 Tier I</button>
      <button id="t2-btn" onclick="switchTier('t2')" style="padding:0.9rem 1rem;border-radius:13px;border:2px solid #E2E8F0;background:#fff;color:#64748B;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1rem;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.04);display:flex;align-items:center;justify-content:center;gap:0.45rem;">📊 Tier II</button>
    </div>

    <div id="pane-t1" style="display:block;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;padding:0 0.1rem;">
        <h2 style="font-family:'Rajdhani',sans-serif;font-size:1rem;font-weight:800;color:#1E293B;margin:0;display:flex;align-items:center;gap:0.5rem;"><span style="display:inline-block;width:3px;height:16px;background:linear-gradient(180deg,#FF6B00,#FF8C38);border-radius:2px;flex-shrink:0;"></span>SSC CGL Tier I — Previous Year Papers</h2>
        <span style="font-size:0.75rem;color:#94A3B8;font-weight:600;background:#F1F5F9;padding:0.2rem 0.6rem;border-radius:20px;">{t1_count} Papers</span>
      </div>
      {t1_html}
    </div>

    <div id="pane-t2" style="display:none;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;padding:0 0.1rem;">
        <h2 style="font-family:'Rajdhani',sans-serif;font-size:1rem;font-weight:800;color:#1E293B;margin:0;display:flex;align-items:center;gap:0.5rem;"><span style="display:inline-block;width:3px;height:16px;background:linear-gradient(180deg,#6366F1,#8B5CF6);border-radius:2px;flex-shrink:0;"></span>SSC CGL Tier II — Previous Year Papers</h2>
        <span style="font-size:0.75rem;color:#94A3B8;font-weight:600;background:#F1F5F9;padding:0.2rem 0.6rem;border-radius:20px;">{t2_count} Papers</span>
      </div>
      {t2_html}
    </div>

    <div style="margin-top:2.5rem;">
      <h2 style="font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1.25rem;color:#1A202C;margin:0 0 0.8rem;display:flex;align-items:center;gap:0.5rem;"><span style="display:inline-block;width:3px;height:18px;background:linear-gradient(180deg,#FF6B00,#FF8C38);border-radius:2px;"></span>Practice Real SSC CGL Question Papers, Free</h2>
      <p style="color:#4A5568;margin:0 0 0.7rem;font-size:0.9rem;line-height:1.6;">SSC CGL previous year papers (PYQ) are the most reliable way to understand the actual exam pattern, difficulty level, and the topics SSC repeats every year. Instead of downloading PDFs and checking answers manually, you can attempt complete shift-wise papers online in a real exam-like interface — track your score, review mistakes, and build speed.</p>
      <p style="color:#4A5568;margin:0;font-size:0.9rem;line-height:1.6;">Every paper above is free, available in both English and Hindi, and includes the correct answer key with detailed solutions. Pick any shift to begin.</p>
    </div>

{seo_content}

    {faq_visible}

    <div style="margin-top:1.8rem;font-size:0.9rem;">
      Looking for more? Explore <a href="{SITE}/ssc-cgl.html" style="color:#FF6B00;font-weight:700;">SSC CGL mock tests &amp; full course</a> →
    </div>

    <div style="margin-top:2.5rem;padding-top:1.5rem;border-top:1px solid #E2E8F0;color:#94A3B8;font-size:0.82rem;text-align:center;">
      © TrickySSC — Free SSC CGL previous year papers, mock tests &amp; solutions in Hindi &amp; English.
    </div>

  </div>
</div>

<script>
  function switchTier(t) {{
    var p1=document.getElementById('pane-t1'), p2=document.getElementById('pane-t2');
    var b1=document.getElementById('t1-btn'), b2=document.getElementById('t2-btn');
    var on='padding:0.9rem 1rem;border-radius:13px;border:2px solid #FF6B00;background:linear-gradient(135deg,#FF6B00,#FF8C38);color:white;font-family:Rajdhani,sans-serif;font-weight:700;font-size:1rem;cursor:pointer;box-shadow:0 4px 16px rgba(255,107,0,0.28);display:flex;align-items:center;justify-content:center;gap:0.45rem;';
    var off='padding:0.9rem 1rem;border-radius:13px;border:2px solid #E2E8F0;background:#fff;color:#64748B;font-family:Rajdhani,sans-serif;font-weight:700;font-size:1rem;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.04);display:flex;align-items:center;justify-content:center;gap:0.45rem;';
    if(t==='t1'){{ p1.style.display='block'; p2.style.display='none'; b1.style.cssText=on; b2.style.cssText=off; }}
    else {{ p2.style.display='block'; p1.style.display='none'; b2.style.cssText=on; b1.style.cssText=off; }}
  }}
</script>

<!-- Language chooser overlay -->
<div id="langChooser" onclick="if(event.target===this)closeLangChooser()">
  <div class="lc-card">
    <div class="lc-head">
      <div class="lc-icon">🌐</div>
      <div class="lc-title" id="lcTitle">Choose Your Language</div>
      <div class="lc-sub" id="lcSub"></div>
    </div>
    <div class="lc-body">
      <button class="lc-opt en" id="lcEn">
        <span class="lc-badge">A</span>
        <span class="lc-opt-main">
          <span class="lc-opt-name">English</span>
          <span class="lc-opt-desc">Attempt the paper in English</span>
        </span>
        <span class="lc-arrow">→</span>
      </button>
      <button class="lc-opt hi" id="lcHi">
        <span class="lc-badge">अ</span>
        <span class="lc-opt-main">
          <span class="lc-opt-name">हिंदी / Hindi</span>
          <span class="lc-opt-desc">पेपर हिंदी में हल करें</span>
        </span>
        <span class="lc-arrow">→</span>
      </button>
      <button class="lc-cancel" onclick="closeLangChooser()">Cancel</button>
    </div>
  </div>
</div>

<script>
  /* ---- Language chooser ---- */
  function openLangChooser(btn) {{
    var en = btn.getAttribute('data-en');
    var hi = btn.getAttribute('data-hi');
    var title = btn.getAttribute('data-title') || '';
    // single language → go straight in
    if(en && !hi){{ window.location = en; return; }}
    if(hi && !en){{ window.location = hi; return; }}
    if(!en && !hi) return;
    var m = document.getElementById('langChooser');
    document.getElementById('lcSub').textContent = title;
    var enB = document.getElementById('lcEn');
    var hiB = document.getElementById('lcHi');
    enB.style.display = en ? 'flex' : 'none';
    hiB.style.display = hi ? 'flex' : 'none';
    enB.onclick = function(){{ window.location = en; }};
    hiB.onclick = function(){{ window.location = hi; }};
    m.style.display = 'block';
    document.body.style.overflow = 'hidden';
  }}
  function closeLangChooser() {{
    var m = document.getElementById('langChooser');
    if(m) m.style.display = 'none';
    document.body.style.overflow = '';
  }}
  document.addEventListener('keydown', function(e){{
    if(e.key === 'Escape') closeLangChooser();
  }});
</script>

<!-- Firebase auth (name display) + attempts tracking (Attempted pills) -->
<script type="module">
import {{ initializeApp }} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import {{ getAuth, onAuthStateChanged }} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import {{ getFirestore, doc, getDoc, collection, query, where, getDocs }} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

const _app = initializeApp({{
  apiKey: "{API_KEY}",
  authDomain: "{PROJECT_ID}.firebaseapp.com",
  projectId: "{PROJECT_ID}",
  storageBucket: "{PROJECT_ID}.firebasestorage.app",
  messagingSenderId: "450627057220",
  appId: "1:450627057220:web:366267bf437d94f20c6e11"
}});
const _auth = getAuth(_app);
const _db = getFirestore(_app);

/* ---- Nav user display: read real name from `users` (same as index.html) ---- */
function _setNavUser(name) {{
  document.querySelectorAll('a[href="{SITE}/login.html"], a[href="login.html"]').forEach(el => {{
    el.href = '{SITE}/dashboard.html';
    el.style.background = 'linear-gradient(135deg,#00A86B,#0EA5E9)';
    el.innerHTML = '👤 ' + name.split(' ')[0];
  }});
}}

/* ---- Attempted tracking ---- */
const __attempted = new Set();

// Instant, device-local source (same as ssc-cgl.html): test.html writes
// each attempted paper to localStorage 'tssc_attempted' keyed by paper id.
// This shows "Attempted" immediately, without waiting on auth or network, and
// works regardless of which account is currently signed in on this device.
function _loadLocalAttempts() {{
  try {{
    const seen = JSON.parse(localStorage.getItem('tssc_attempted') || '{{}}');
    Object.keys(seen).forEach(k => {{
      if(k.startsWith('p:')) __attempted.add(k.slice(2));
    }});
  }} catch(e) {{}}
}}

function _applyPills() {{
  document.querySelectorAll('.pyq-attempt-btn').forEach(btn => {{
    const pe = btn.getAttribute('data-pid-en');
    const ph = btn.getAttribute('data-pid-hi');
    const done = (pe && __attempted.has(pe)) || (ph && __attempted.has(ph));
    if(done) {{
      const pick = btn.getAttribute('data-pick');
      const pill = document.querySelector('.attempt-pill[data-pill="'+pick+'"]');
      if(pill) {{ pill.className = 'attempt-pill done'; pill.textContent = '✓ Attempted'; }}
      btn.innerHTML = '↻ Re-attempt';
    }}
  }});
}}

// Attempted status is applied only AFTER we know the user is logged in
// (see onAuthStateChanged below). Logged-out visitors see plain
// "Attempt Test" on every paper.

// Reset every paper to the not-attempted state (used on logout).
function _resetPills() {{
  __attempted.clear();
  document.querySelectorAll('.pyq-attempt-btn').forEach(btn => {{
    const pick = btn.getAttribute('data-pick');
    const pill = document.querySelector('.attempt-pill[data-pill="'+pick+'"]');
    if(pill) {{ pill.className = 'attempt-pill todo'; pill.textContent = '○ Not Attempted'; }}
    btn.innerHTML = '▶ Attempt Test';
  }});
}}

async function _syncAttempts(uid) {{
  if(!uid) return;
  const _ck = 'tssc_attempts_' + uid, _ttl = 10*60*1000;
  try {{
    const _c = sessionStorage.getItem(_ck);
    if(_c) {{
      const _o = JSON.parse(_c);
      if(Date.now() - (_o.ts||0) < _ttl && Array.isArray(_o.p)) {{
        _o.p.forEach(id => __attempted.add(id));
        _applyPills();
        if(Date.now() - (_o.ts||0) < _ttl) return;
      }}
    }}
  }} catch(e) {{}}
  try {{
    const snap = await getDocs(query(collection(_db,'attempts'), where('uid','==',uid)));
    snap.forEach(d => {{ const a = d.data()||{{}}; if(a.paperId) __attempted.add(a.paperId); }});
    try {{ sessionStorage.setItem(_ck, JSON.stringify({{ ts:Date.now(), p:[...__attempted] }})); }} catch(e) {{}}
    _applyPills();
  }} catch(e) {{ console.warn('[TrickySSC] attempts sync failed:', e.message); }}
}}

onAuthStateChanged(_auth, async user => {{
  if(!user) {{
    // Logged out → show plain "Attempt Test" everywhere, no attempted status.
    _resetPills();
    return;
  }}
  // Logged in → show attempted status. Device-local first (instant)...
  _loadLocalAttempts();
  _applyPills();
  // name from local cache first (instant)
  try {{ const s = localStorage.getItem('tssc_user'); if(s){{ const u = JSON.parse(s); if(u.name && u.name!=='Student') _setNavUser(u.name); }} }} catch(e) {{}}
  // then authoritative name from `users` collection
  try {{
    const snap = await getDoc(doc(_db,'users',user.uid));
    if(snap.exists()) {{
      const name = snap.data().name;
      if(name && name!=='Student') {{
        _setNavUser(name);
        try {{ const s=localStorage.getItem('tssc_user'); const u=s?JSON.parse(s):{{}}; localStorage.setItem('tssc_user',JSON.stringify({{...u,name,uid:user.uid}})); }} catch(e) {{}}
      }} else _setNavUser(user.displayName||user.email||'Student');
    }} else _setNavUser(user.displayName||user.email||'Student');
  }} catch(e) {{ _setNavUser(user.displayName||user.email||'Student'); }}
  // ...then authoritative attempts from Firestore for this account.
  _syncAttempts(user.uid);
}});
</script>
{MOCK_PROMO}
</body>
</html>
"""
    return page, total_papers


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
SITEMAP_FILE = "sitemap.xml"


def update_sitemap_lastmod():
    """Update only the <lastmod> of the ssc-cgl-pyq.html entry in sitemap.xml
    to today's date. Leaves every other entry and the file's formatting
    (including CRLF/LF line endings) untouched. Safe no-op if the sitemap or
    the entry isn't found."""
    import os
    if not os.path.exists(SITEMAP_FILE):
        print(f"  (sitemap: {SITEMAP_FILE} not found, skipping)", file=sys.stderr)
        return

    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    page_url = f"{SITE}/{OUTPUT_FILE}"

    # Read in binary to preserve the file's exact line endings (CRLF vs LF).
    with open(SITEMAP_FILE, "rb") as f:
        raw = f.read()
    uses_crlf = b"\r\n" in raw
    content = raw.decode("utf-8")
    if uses_crlf:
        content = content.replace("\r\n", "\n")  # normalize for editing

    # Locate the <url>…</url> block that contains our page's <loc>.
    loc_pos = content.find(page_url)
    if loc_pos == -1:
        print(f"  (sitemap: {OUTPUT_FILE} entry not found, skipping)",
              file=sys.stderr)
        return

    block_start = content.rfind("<url>", 0, loc_pos)
    block_end = content.find("</url>", loc_pos)
    if block_start == -1 or block_end == -1:
        print("  (sitemap: malformed entry, skipping)", file=sys.stderr)
        return
    block = content[block_start:block_end]

    # Replace the <lastmod>…</lastmod> inside just this block.
    new_block, n = re.subn(
        r"<lastmod>.*?</lastmod>",
        f"<lastmod>{today}</lastmod>",
        block,
        count=1,
    )

    if n == 0:
        # No <lastmod> present in the block — insert one right after </loc>.
        new_block = block.replace(
            "</loc>", f"</loc>\n    <lastmod>{today}</lastmod>", 1
        )

    if new_block == block:
        print(f"  (sitemap: lastmod already {today}, no change)",
              file=sys.stderr)
        return

    content = content[:block_start] + new_block + content[block_end:]
    # Restore the file's original line-ending style.
    if uses_crlf:
        content = content.replace("\n", "\r\n")
    with open(SITEMAP_FILE, "wb") as f:
        f.write(content.encode("utf-8"))
    print(f"  updated {SITEMAP_FILE}: {OUTPUT_FILE} lastmod → {today}",
          file=sys.stderr)


def main():
    import urllib.parse  # noqa (used in helpers)
    print("Fetching papers from Firestore…", file=sys.stderr)
    papers = fetch_all_papers()
    print(f"  fetched {len(papers)} raw documents", file=sys.stderr)

    ordered = organize(papers)
    page, total = render(ordered)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(page)

    years = ", ".join(ordered.keys()) or "(none)"
    print(f"  wrote {OUTPUT_FILE} — {total} papers across years: {years}",
          file=sys.stderr)

    # Keep the sitemap's "last updated" date for this page in sync, so Google
    # re-crawls it promptly after new papers are added.
    update_sitemap_lastmod()


# urllib.parse needed at module level for helpers
import urllib.parse  # noqa: E402

if __name__ == "__main__":
    main()
