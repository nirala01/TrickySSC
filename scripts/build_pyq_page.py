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
    return f"{SITE}/test.html?{qs}"


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
    years_list = list(ordered.keys())
    updated = datetime.datetime.utcnow().strftime("%d %b %Y")

    # Split groups into Tier I and Tier II
    def is_tier2(t):
        t = str(t).lower()
        return "2" in t or "ii" in t

    tier1 = {}
    tier2 = {}
    for y, groups in ordered.items():
        g1 = [g for g in groups if not is_tier2(g["tier"])]
        g2 = [g for g in groups if is_tier2(g["tier"])]
        if g1:
            tier1[y] = g1
        if g2:
            tier2[y] = g2

    t1_total = sum(len(v) for v in tier1.values())
    t2_total = sum(len(v) for v in tier2.values())

    def shift_badge(shift):
        digits = "".join(ch for ch in str(shift) if ch.isdigit())
        return f"S{digits}" if digits else "S"

    def render_paper_rows(tier_map):
        """Render the year-grouped accordion of paper rows for one tier."""
        if not tier_map:
            return (
                '<div class="empty-note">Papers will appear here soon. '
                'Check back shortly.</div>'
            )
        blocks = []
        for y, groups in tier_map.items():
            rows = []
            for g in groups:
                date_txt = pretty_date(g["heldOn"])
                qc = g.get("questionCount") or 100
                badge = shift_badge(g["shift"])
                shift_name = g["shift"].replace("-", " ")

                btns = []
                if "en" in g["langs"]:
                    btns.append(
                        f'<a class="ppr-btn ppr-btn-en" '
                        f'href="{html.escape(test_url(g, "en"))}">'
                        f'English</a>'
                    )
                if "hi" in g["langs"]:
                    btns.append(
                        f'<a class="ppr-btn ppr-btn-hi" '
                        f'href="{html.escape(test_url(g, "hi"))}">'
                        f'हिंदी</a>'
                    )
                btns_html = "".join(btns)

                rows.append(f"""
          <div class="ppr-row">
            <div class="ppr-info">
              <div class="ppr-title">
                <span class="ppr-shift">{html.escape(shift_name)}</span>
                <span class="ppr-chip">{badge}</span>
                <span class="ppr-date">{html.escape(date_txt)}</span>
              </div>
              <div class="ppr-meta">
                <span>📄 {qc} Qs</span>
                <span>⏱ 60 min</span>
                <span>🎯 200 marks</span>
              </div>
            </div>
            <div class="ppr-actions">{btns_html}</div>
          </div>""")

            blocks.append(f"""
        <div class="yr-group">
          <div class="yr-group-head">
            <span class="yr-badge">{y}</span>
            <span class="yr-label">SSC CGL Tier I {y}</span>
            <span class="yr-count">{len(groups)} papers</span>
          </div>
          <div class="yr-rows">{''.join(rows)}</div>
        </div>""")
        return "".join(blocks)

    tier1_html = render_paper_rows(tier1)
    tier2_html = render_paper_rows(tier2) if tier2 else (
        '<div class="empty-note">Tier II papers coming soon.</div>'
    )

    # ---- schema (kept from before, good for SEO) ----
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
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "SSC CGL Previous Year Papers (PYQ) — Free Online Tests",
        "numberOfItems": total_papers,
        "itemListElement": item_list,
    }

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question",
             "name": "Are SSC CGL previous year papers free on TrickySSC?",
             "acceptedAnswer": {"@type": "Answer",
                "text": "Yes. All SSC CGL Tier 1 previous year question papers (PYQ) on TrickySSC are completely free to attempt online. No payment or subscription is required."}},
            {"@type": "Question",
             "name": "Can I attempt SSC CGL PYQ papers in Hindi and English?",
             "acceptedAnswer": {"@type": "Answer",
                "text": "Yes. Every SSC CGL previous year paper is available in both English and Hindi. You can choose your preferred language before starting the test."}},
            {"@type": "Question",
             "name": "Do the SSC CGL PYQ tests include answer keys and solutions?",
             "acceptedAnswer": {"@type": "Answer",
                "text": "Yes. Each paper comes with the correct answer key and step-by-step solutions so you can review every question after submitting the test."}},
            {"@type": "Question",
             "name": "Which SSC CGL years are available for practice?",
             "acceptedAnswer": {"@type": "Answer",
                "text": "TrickySSC provides shift-wise SSC CGL previous year papers across multiple years, including the most recent 2025 Tier 1 exam shifts, added regularly as new papers are processed."}},
            {"@type": "Question",
             "name": "Is the test interface similar to the real SSC CGL exam?",
             "acceptedAnswer": {"@type": "Answer",
                "text": "Yes. The online test engine mirrors the real SSC CGL exam pattern with sectional layout, a question palette, a timer, and negative marking, so you practice in exam-like conditions."}},
        ],
    }

    faq_visible = """
      <section class="faq-sec" id="faq">
        <h2 class="sec-h2">Frequently Asked Questions</h2>
        <details><summary>Are SSC CGL previous year papers free on TrickySSC?</summary>
          <p>Yes. All SSC CGL Tier 1 previous year question papers (PYQ) on TrickySSC are completely free to attempt online. No payment or subscription is required.</p></details>
        <details><summary>Can I attempt SSC CGL PYQ papers in Hindi and English?</summary>
          <p>Yes. Every SSC CGL previous year paper is available in both English and Hindi. Choose your preferred language before starting the test.</p></details>
        <details><summary>Do the tests include answer keys and solutions?</summary>
          <p>Yes. Each paper comes with the correct answer key and step-by-step solutions, so you can review every question after submitting the test.</p></details>
        <details><summary>Which SSC CGL years are available?</summary>
          <p>Shift-wise SSC CGL previous year papers across multiple years, including the most recent 2025 Tier 1 exam shifts, added regularly as new papers are processed.</p></details>
        <details><summary>Is the interface similar to the real SSC CGL exam?</summary>
          <p>Yes. The test engine mirrors the real exam pattern with a sectional layout, question palette, timer, and negative marking for exam-like practice.</p></details>
      </section>"""

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
<title>SSC CGL Previous Year Papers (PYQ) — Free Online Test in Hindi &amp; English | TrickySSC</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="keywords" content="SSC CGL PYQ, SSC CGL previous year paper, SSC CGL previous year paper online free, SSC CGL PYQ test, SSC CGL question paper with solution, SSC CGL 2025 paper, SSC CGL Tier 1 PYQ, SSC CGL free online test">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{SITE}/{OUTPUT_FILE}">
<meta property="og:type" content="website">
<meta property="og:title" content="SSC CGL Previous Year Papers (PYQ) — Free Online Test">
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
  :root {{
    --saffron:#FF6B00; --saffron-light:#FF8C38; --saffron-dark:#CC5500;
    --bg:#F5F7FA; --card:#FFFFFF; --border:#E2E8F0;
    --green:#00A86B; --green-dim:#00875A; --gold:#F59E0B;
    --text-main:#1A202C; --text-dim:#4A5568; --text-muted:#718096;
  }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{
    font-family:'Hind',sans-serif; background:var(--bg);
    color:var(--text-main); overflow-x:hidden;
  }}
  a {{ text-decoration:none; color:inherit; }}

  /* ---- NAV ---- */
  nav {{
    position:sticky; top:0; z-index:1000; background:#FFFFFF;
    box-shadow:0 2px 12px rgba(0,0,0,.08); border-bottom:1px solid var(--border);
    padding:0 1.5rem;
  }}
  .nav-inner {{
    max-width:1280px; margin:0 auto; display:flex; align-items:center;
    justify-content:space-between; height:64px;
  }}
  .logo {{
    font-family:'Baloo 2',cursive; font-size:1.7rem; font-weight:800;
    letter-spacing:-.5px; color:#1A202C;
  }}
  .logo span {{ color:var(--saffron); }}
  .nav-links {{ display:flex; gap:.3rem; list-style:none; align-items:center; }}
  .nav-links a {{
    padding:.5rem .8rem; font-size:.9rem; font-weight:500;
    color:var(--text-dim); border-radius:8px; transition:.15s;
  }}
  .nav-links a:hover {{ background:#FFF7F0; color:var(--saffron); }}
  .nav-cta {{ background:var(--saffron); color:#fff !important; }}
  .nav-cta:hover {{ background:var(--saffron-dark) !important; color:#fff !important; }}
  .nav-toggle {{ display:none; font-size:1.5rem; background:none; border:none; cursor:pointer; color:var(--text-main); }}
  @media (max-width:900px) {{
    .nav-links {{ display:none; }}
    .nav-toggle {{ display:block; }}
  }}

  /* ---- WRAP ---- */
  .wrap {{ max-width:1080px; margin:0 auto; padding:1.5rem 1rem 4rem; }}
  .crumbs {{ font-size:.8rem; color:var(--text-muted); margin-bottom:1rem; }}
  .crumbs a:hover {{ color:var(--saffron); }}

  /* ---- HERO ---- */
  .hero {{
    background:linear-gradient(135deg,#FFF3E9 0%,#FFFFFF 100%);
    border:1px solid var(--border); border-left:4px solid var(--saffron);
    border-radius:16px; padding:1.6rem 1.5rem; margin-bottom:1.5rem;
  }}
  .hero h1 {{
    font-family:'Rajdhani',sans-serif; font-weight:700;
    font-size:clamp(1.4rem,4vw,2.1rem); line-height:1.2;
    color:var(--text-main); margin-bottom:.5rem;
  }}
  .hero p {{ color:var(--text-dim); font-size:.95rem; max-width:760px; }}
  .hero-stats {{ display:flex; flex-wrap:wrap; gap:.6rem; margin-top:1rem; }}
  .hstat {{
    background:#fff; border:1px solid var(--border); color:var(--text-dim);
    padding:.4rem .9rem; border-radius:999px; font-size:.82rem; font-weight:500;
  }}
  .hstat strong {{ color:var(--saffron); }}
  .updated {{ font-size:.75rem; color:var(--text-muted); margin-top:.8rem; }}

  /* ---- TIER TABS ---- */
  .tier-tabs {{ display:flex; gap:.8rem; margin-bottom:1.4rem; }}
  .tier-tab {{
    flex:1; text-align:center; padding:.9rem 1rem; border-radius:12px;
    font-family:'Rajdhani',sans-serif; font-weight:600; font-size:1.05rem;
    cursor:pointer; border:1px solid var(--border); background:#fff;
    color:var(--text-dim); transition:.15s; user-select:none;
  }}
  .tier-tab.active {{
    background:linear-gradient(135deg,var(--saffron) 0%,var(--saffron-light) 100%);
    color:#fff; border-color:var(--saffron);
    box-shadow:0 4px 14px rgba(255,107,0,.3);
  }}

  /* ---- SECTION HEAD ---- */
  .sec-head {{
    display:flex; align-items:center; justify-content:space-between;
    border-left:3px solid var(--saffron); padding-left:.7rem; margin-bottom:1rem;
  }}
  .sec-head h2 {{
    font-family:'Rajdhani',sans-serif; font-weight:600; font-size:1.15rem;
    color:var(--text-main);
  }}
  .sec-head .total {{ font-size:.8rem; color:var(--text-muted); }}

  /* ---- YEAR GROUP ---- */
  .yr-group {{ margin-bottom:1.4rem; }}
  .yr-group-head {{
    display:flex; align-items:center; gap:.6rem; margin-bottom:.7rem;
  }}
  .yr-badge {{
    background:var(--saffron); color:#fff; font-family:'Rajdhani',sans-serif;
    font-weight:700; font-size:.85rem; padding:.25rem .7rem; border-radius:7px;
  }}
  .yr-label {{ font-weight:600; color:var(--text-main); font-size:.98rem; }}
  .yr-count {{ margin-left:auto; font-size:.78rem; color:var(--text-muted); }}

  /* ---- PAPER ROWS ---- */
  .yr-rows {{ display:flex; flex-direction:column; gap:.6rem; }}
  .ppr-row {{
    background:var(--card); border:1px solid var(--border);
    border-left:3px solid var(--saffron); border-radius:11px;
    padding:.85rem 1.1rem; display:flex; align-items:center;
    justify-content:space-between; gap:1rem; transition:.15s; flex-wrap:wrap;
  }}
  .ppr-row:hover {{ box-shadow:0 4px 16px rgba(0,0,0,.07); transform:translateY(-1px); }}
  .ppr-title {{ display:flex; align-items:center; gap:.55rem; flex-wrap:wrap; }}
  .ppr-shift {{ font-weight:600; font-size:1rem; color:var(--text-main); }}
  .ppr-chip {{
    background:#FFF0E5; color:var(--saffron-dark); font-size:.7rem;
    font-weight:600; padding:.12rem .5rem; border-radius:5px;
  }}
  .ppr-date {{ font-size:.92rem; color:var(--text-dim); }}
  .ppr-meta {{ display:flex; gap:.9rem; margin-top:.35rem; font-size:.78rem; color:var(--text-muted); flex-wrap:wrap; }}
  .ppr-actions {{ display:flex; gap:.5rem; }}
  .ppr-btn {{
    padding:.5rem 1.1rem; border-radius:8px; font-size:.85rem; font-weight:600;
    transition:.15s; white-space:nowrap;
  }}
  .ppr-btn-en {{ background:var(--saffron); color:#fff; }}
  .ppr-btn-en:hover {{ background:var(--saffron-dark); }}
  .ppr-btn-hi {{ background:#fff; color:var(--green-dim); border:1px solid var(--green); }}
  .ppr-btn-hi:hover {{ background:#E8FBF3; }}

  .empty-note {{
    background:#fff; border:1px dashed var(--border); border-radius:11px;
    padding:1.5rem; text-align:center; color:var(--text-muted); font-size:.9rem;
  }}

  /* ---- INTRO / FAQ ---- */
  .intro {{ margin:2rem 0 1.5rem; }}
  .sec-h2 {{
    font-family:'Rajdhani',sans-serif; font-weight:600; font-size:1.25rem;
    color:var(--text-main); margin-bottom:.7rem;
    border-left:3px solid var(--saffron); padding-left:.7rem;
  }}
  .intro p {{ color:var(--text-dim); margin-bottom:.7rem; font-size:.92rem; }}
  .faq-sec {{ margin-top:2rem; }}
  .faq-sec details {{
    background:#fff; border:1px solid var(--border); border-radius:11px;
    padding:.85rem 1.1rem; margin-bottom:.6rem;
  }}
  .faq-sec summary {{ cursor:pointer; font-weight:600; font-size:.92rem; color:var(--text-main); }}
  .faq-sec p {{ color:var(--text-dim); margin-top:.6rem; font-size:.88rem; }}

  .more-link {{ margin-top:1.8rem; font-size:.9rem; }}
  .more-link a {{ color:var(--saffron); font-weight:600; }}

  footer {{
    margin-top:2.5rem; padding:1.5rem 1rem; border-top:1px solid var(--border);
    color:var(--text-muted); font-size:.82rem; text-align:center;
  }}

  @media (max-width:560px) {{
    .ppr-row {{ flex-direction:column; align-items:stretch; }}
    .ppr-actions {{ justify-content:stretch; }}
    .ppr-btn {{ flex:1; text-align:center; }}
    .tier-tabs {{ gap:.5rem; }}
  }}
</style>
</head>
<body>

<nav>
  <div class="nav-inner">
    <a href="{SITE}/index.html" class="logo">Tricky<span>SSC</span></a>
    <ul class="nav-links">
      <li><a href="{SITE}/index.html">Home</a></li>
      <li><a href="{SITE}/ssc-cgl.html">SSC CGL</a></li>
      <li><a href="{SITE}/ssc-cgl-pyq.html">PYQ Bank</a></li>
      <li><a href="{SITE}/ssc-cgl.html#mock">Mock Tests</a></li>
      <li><a href="{SITE}/current-affairs.html">Current Affairs</a></li>
      <li><a href="{SITE}/login.html" class="nav-cta">Login</a></li>
    </ul>
    <button class="nav-toggle" onclick="document.querySelector('.nav-links').style.display=(document.querySelector('.nav-links').style.display==='flex'?'none':'flex')">☰</button>
  </div>
</nav>

<div class="wrap">

  <nav class="crumbs">
    <a href="{SITE}/">Home</a> ›
    <a href="{SITE}/ssc-cgl.html">SSC CGL</a> ›
    PYQ Papers
  </nav>

  <header class="hero">
    <h1>SSC CGL Previous Year Papers (PYQ) — Free Online Test</h1>
    <p>Shift-wise SSC CGL Tier 1 question papers in English &amp; Hindi, with answer keys and step-by-step solutions. 100% free, real exam-pattern interface.</p>
    <div class="hero-stats">
      <span class="hstat"><strong>{total_papers}+</strong> Papers</span>
      <span class="hstat">🌐 Hindi &amp; English</span>
      <span class="hstat">✅ Solutions Included</span>
      <span class="hstat">🆓 No Payment</span>
    </div>
    <div class="updated">Last updated: {updated}</div>
  </header>

  <div class="tier-tabs">
    <div class="tier-tab active" id="tab-t1" onclick="showTier('t1')">🎯 Tier I</div>
    <div class="tier-tab" id="tab-t2" onclick="showTier('t2')">📊 Tier II</div>
  </div>

  <div id="pane-t1">
    <div class="sec-head">
      <h2>SSC CGL Tier I — Previous Year Papers</h2>
      <span class="total">{t1_total} papers</span>
    </div>
    {tier1_html}
  </div>

  <div id="pane-t2" style="display:none;">
    <div class="sec-head">
      <h2>SSC CGL Tier II — Previous Year Papers</h2>
      <span class="total">{t2_total} papers</span>
    </div>
    {tier2_html}
  </div>

  <section class="intro">
    <h2 class="sec-h2">Practice Real SSC CGL Question Papers, Free</h2>
    <p>SSC CGL previous year papers (PYQ) are the most reliable way to understand the actual exam pattern, difficulty level, and the topics SSC repeats every year. Instead of downloading PDFs and checking answers manually, you can attempt complete shift-wise papers online in a real exam-like interface — track your score, review mistakes, and build speed.</p>
    <p>Every paper above is free, available in both English and Hindi, and includes the correct answer key with detailed solutions. Pick any shift to begin.</p>
  </section>

  {faq_visible}

  <div class="more-link">
    Looking for more? Explore <a href="{SITE}/ssc-cgl.html">SSC CGL mock tests &amp; full course</a> →
  </div>

  <footer>
    © TrickySSC — Free SSC CGL previous year papers, mock tests &amp; solutions in Hindi &amp; English.
  </footer>

</div>

<script>
  function showTier(t) {{
    var t1 = document.getElementById('pane-t1');
    var t2 = document.getElementById('pane-t2');
    var b1 = document.getElementById('tab-t1');
    var b2 = document.getElementById('tab-t2');
    if (t === 't1') {{
      t1.style.display=''; t2.style.display='none';
      b1.classList.add('active'); b2.classList.remove('active');
    }} else {{
      t1.style.display='none'; t2.style.display='';
      b2.classList.add('active'); b1.classList.remove('active');
    }}
  }}
</script>
</body>
</html>
"""
    return page, total_papers


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
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


# urllib.parse needed at module level for helpers
import urllib.parse  # noqa: E402

if __name__ == "__main__":
    main()
