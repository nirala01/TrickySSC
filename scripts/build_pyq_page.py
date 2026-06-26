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
                btns = []
                if "en" in g["langs"]:
                    btns.append(
                        f'<a href="{html.escape(test_url(g, "en"))}" '
                        f'style="display:inline-flex;align-items:center;gap:0.3rem;'
                        f'background:linear-gradient(135deg,#FF6B00,#FF8C38);'
                        f'color:white;text-decoration:none;padding:0.5rem 0.9rem;'
                        f'border-radius:9px;font-family:\'Rajdhani\',sans-serif;'
                        f'font-weight:700;font-size:0.82rem;white-space:nowrap;">'
                        f'English</a>')
                if "hi" in g["langs"]:
                    btns.append(
                        f'<a href="{html.escape(test_url(g, "hi"))}" '
                        f'style="display:inline-flex;align-items:center;gap:0.3rem;'
                        f'background:#fff;color:#00875A;text-decoration:none;'
                        f'padding:0.5rem 0.9rem;border-radius:9px;'
                        f'border:1px solid #00A86B;'
                        f"font-family:'Rajdhani',sans-serif;font-weight:700;"
                        f'font-size:0.82rem;white-space:nowrap;">हिंदी</a>')
                btns_html = "".join(btns)

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
                  </div>
                </div>
              </div>
              <div style="display:flex;align-items:center;gap:0.4rem;flex-shrink:0;flex-wrap:wrap;justify-content:flex-end;">{btns_html}</div>
            </div>""")

            blocks.append(f"""
        <div style="margin-bottom:1.5rem;">
          <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.6rem;padding:0 0.25rem;">
            <div style="width:32px;height:32px;background:{accent};border-radius:8px;display:flex;align-items:center;justify-content:center;font-family:'Rajdhani',sans-serif;font-weight:800;font-size:0.72rem;color:white;letter-spacing:-0.3px;flex-shrink:0;">{year}</div>
            <div style="font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1rem;color:#1A202C;">SSC CGL {tier_label} {year}</div>
            <div style="margin-left:auto;background:#F1F5F9;border-radius:20px;padding:0.2rem 0.65rem;font-size:0.72rem;font-weight:700;color:#64748B;font-family:'Rajdhani',sans-serif;">{ycount} paper{'s' if ycount != 1 else ''}</div>
          </div>
          <div style="background:#fff;border:1px solid #E2E8F0;border-radius:14px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.05);border-left:3px solid {accent};">{''.join(rows)}</div>
        </div>""")
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
        "name": "SSC CGL Previous Year Papers (PYQ) — Free Online Tests",
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
    <h1 style="font-family:'Rajdhani',sans-serif;font-weight:800;font-size:clamp(1.1rem,4.2vw,1.55rem);line-height:1.25;color:#1A202C;margin:0;">SSC CGL Previous Year Papers (PYQ) – Free Online Tests</h1>
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

    <div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:11px;padding:0.65rem 1rem;display:flex;align-items:center;gap:0.55rem;margin-bottom:1.25rem;">
      <span style="font-size:0.95rem;">🎁</span>
      <span style="font-size:0.82rem;color:#15803D;font-weight:600;">All papers are free to attempt online in English &amp; Hindi. New papers added regularly!</span>
    </div>

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
