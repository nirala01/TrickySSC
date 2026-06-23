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

    # ----- build year jump chips -----
    chips = "".join(
        f'<a class="yr-chip" href="#y{y}">{y}</a>' for y in years_list
    )

    # ----- build year sections -----
    sections = []
    for y, groups in ordered.items():
        cards = []
        for g in groups:
            date_txt = pretty_date(g["heldOn"])
            tlabel = tier_label(g["tier"])
            qc = g.get("questionCount") or ""
            qc_txt = f"{qc} Questions" if qc else ""
            title = f"SSC CGL {date_txt} {g['shift'].replace('-', ' ')}"

            # language buttons (only show languages that exist)
            btns = []
            if "en" in g["langs"]:
                btns.append(
                    f'<a class="btn btn-en" href="{html.escape(test_url(g, "en"))}" '
                    f'rel="nofollow">Attempt in English</a>'
                )
            if "hi" in g["langs"]:
                btns.append(
                    f'<a class="btn btn-hi" href="{html.escape(test_url(g, "hi"))}" '
                    f'rel="nofollow">हिंदी में हल करें</a>'
                )
            btns_html = "".join(btns)

            meta_bits = " · ".join(
                b for b in [tlabel, qc_txt, "Free"] if b
            )

            cards.append(f"""
        <div class="paper-card">
          <div class="paper-head">
            <span class="paper-icon">📝</span>
            <h3 class="paper-title">{html.escape(title)}</h3>
          </div>
          <p class="paper-meta">{html.escape(meta_bits)}</p>
          <div class="paper-actions">{btns_html}</div>
        </div>""")

        sections.append(f"""
      <section class="year-block" id="y{y}">
        <h2 class="year-heading">SSC CGL {y} Previous Year Papers <span class="count">({len(groups)})</span></h2>
        <div class="paper-grid">{''.join(cards)}</div>
      </section>""")

    sections_html = "".join(sections)

    # ----- ItemList schema (helps Google understand the list) -----
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
            {
                "@type": "Question",
                "name": "Are SSC CGL previous year papers free on TrickySSC?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes. All SSC CGL Tier 1 previous year question papers (PYQ) on TrickySSC are completely free to attempt online. No payment or subscription is required.",
                },
            },
            {
                "@type": "Question",
                "name": "Can I attempt SSC CGL PYQ papers in Hindi and English?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes. Every SSC CGL previous year paper is available in both English and Hindi. You can choose your preferred language before starting the test.",
                },
            },
            {
                "@type": "Question",
                "name": "Do the SSC CGL PYQ tests include answer keys and solutions?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes. Each paper comes with the correct answer key and step-by-step solutions so you can review every question after submitting the test.",
                },
            },
            {
                "@type": "Question",
                "name": "Which SSC CGL years are available for practice?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "TrickySSC provides shift-wise SSC CGL previous year papers across multiple years, including the most recent 2025 Tier 1 exam shifts, added regularly as new papers are processed.",
                },
            },
            {
                "@type": "Question",
                "name": "Is the test interface similar to the real SSC CGL exam?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes. The online test engine mirrors the real SSC CGL exam pattern with sectional layout, a question palette, a timer, and negative marking, so you practice in exam-like conditions.",
                },
            },
        ],
    }

    # visible FAQ
    faq_visible = """
      <section class="faq" id="faq">
        <h2>Frequently Asked Questions</h2>
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
<script type="application/ld+json">
{json.dumps(faq_schema, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(itemlist_schema, ensure_ascii=False)}
</script>
<style>
  :root {{
    --bg:#0f1222; --card:#171a2e; --card2:#1d2138; --line:#2a2f4a;
    --text:#e9ecf5; --muted:#9aa3c0; --accent:#5b8cff; --accent2:#22c55e;
    --hi:#f59e0b;
  }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; background:var(--bg); color:var(--text);
    font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;
    line-height:1.6;
  }}
  a {{ color:inherit; text-decoration:none; }}
  .wrap {{ max-width:1040px; margin:0 auto; padding:20px 16px 64px; }}
  .crumbs {{ font-size:13px; color:var(--muted); margin-bottom:14px; }}
  .crumbs a {{ color:var(--muted); }}
  .crumbs a:hover {{ color:var(--text); }}
  header.hero {{
    background:linear-gradient(135deg,#202650 0%,#161930 100%);
    border:1px solid var(--line); border-radius:18px;
    padding:26px 22px; margin-bottom:22px;
  }}
  header.hero h1 {{ font-size:clamp(22px,4.4vw,34px); margin:0 0 8px; line-height:1.25; }}
  header.hero p {{ margin:0; color:var(--muted); font-size:15px; }}
  .stats {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:16px; }}
  .stat {{
    background:var(--card2); border:1px solid var(--line);
    padding:8px 13px; border-radius:999px; font-size:13px; color:var(--text);
  }}
  .updated {{ font-size:12px; color:var(--muted); margin-top:12px; }}
  .yr-nav {{ display:flex; flex-wrap:wrap; gap:8px; margin:4px 0 26px; }}
  .yr-chip {{
    background:var(--card); border:1px solid var(--line);
    padding:7px 14px; border-radius:10px; font-size:14px; font-weight:600;
    transition:.15s;
  }}
  .yr-chip:hover {{ border-color:var(--accent); color:#fff; }}
  .year-block {{ margin-bottom:34px; scroll-margin-top:16px; }}
  .year-heading {{ font-size:20px; margin:0 0 14px; }}
  .year-heading .count {{ color:var(--muted); font-weight:500; font-size:15px; }}
  .paper-grid {{
    display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
    gap:14px;
  }}
  .paper-card {{
    background:var(--card); border:1px solid var(--line);
    border-radius:14px; padding:16px 16px 14px; transition:.15s;
  }}
  .paper-card:hover {{ border-color:var(--accent); transform:translateY(-2px); }}
  .paper-head {{ display:flex; align-items:flex-start; gap:9px; margin-bottom:6px; }}
  .paper-icon {{ font-size:18px; }}
  .paper-title {{ font-size:15.5px; margin:0; line-height:1.35; }}
  .paper-meta {{ font-size:12.5px; color:var(--muted); margin:0 0 12px; }}
  .paper-actions {{ display:flex; flex-wrap:wrap; gap:8px; }}
  .btn {{
    flex:1 1 auto; text-align:center; padding:9px 10px; border-radius:9px;
    font-size:13.5px; font-weight:600; border:1px solid transparent; transition:.15s;
    min-width:130px;
  }}
  .btn-en {{ background:var(--accent); color:#fff; }}
  .btn-en:hover {{ filter:brightness(1.1); }}
  .btn-hi {{ background:transparent; color:var(--hi); border-color:var(--hi); }}
  .btn-hi:hover {{ background:rgba(245,158,11,.12); }}
  .intro {{ margin:6px 0 26px; }}
  .intro h2 {{ font-size:18px; margin:0 0 8px; }}
  .intro p {{ color:var(--muted); margin:0 0 10px; font-size:14.5px; }}
  .faq {{ margin-top:34px; }}
  .faq h2 {{ font-size:20px; margin:0 0 12px; }}
  .faq details {{
    background:var(--card); border:1px solid var(--line);
    border-radius:11px; padding:13px 15px; margin-bottom:10px;
  }}
  .faq summary {{ cursor:pointer; font-weight:600; font-size:14.5px; }}
  .faq p {{ color:var(--muted); margin:9px 0 0; font-size:14px; }}
  .backlinks {{ margin-top:30px; font-size:14px; }}
  .backlinks a {{ color:var(--accent); }}
  footer {{ margin-top:40px; padding-top:18px; border-top:1px solid var(--line);
    color:var(--muted); font-size:13px; }}
  @media (max-width:560px) {{
    .paper-grid {{ grid-template-columns:1fr; }}
    .btn {{ min-width:0; }}
  }}
</style>
</head>
<body>
<div class="wrap">

  <nav class="crumbs">
    <a href="{SITE}/">Home</a> ›
    <a href="{SITE}/ssc-cgl.html">SSC CGL</a> ›
    PYQ Papers
  </nav>

  <header class="hero">
    <h1>SSC CGL Previous Year Papers (PYQ) — Free Online Test</h1>
    <p>Shift-wise SSC CGL Tier 1 question papers in English &amp; Hindi, with answer keys and step-by-step solutions. 100% free, real exam-pattern interface.</p>
    <div class="stats">
      <span class="stat">📚 {total_papers}+ Papers</span>
      <span class="stat">🌐 Hindi &amp; English</span>
      <span class="stat">✅ Solutions Included</span>
      <span class="stat">🆓 No Payment</span>
    </div>
    <div class="updated">Last updated: {updated}</div>
  </header>

  <nav class="yr-nav">{chips}</nav>

  <section class="intro">
    <h2>Practice Real SSC CGL Question Papers, Free</h2>
    <p>SSC CGL previous year papers (PYQ) are the most reliable way to understand the actual exam pattern, difficulty level, and the topics SSC repeats every year. Instead of downloading PDFs and checking answers manually, you can attempt complete shift-wise papers online in a real exam-like interface — track your score, review mistakes, and build speed.</p>
    <p>Every paper below is free, available in both English and Hindi, and includes the correct answer key with detailed solutions. Pick any shift to begin.</p>
  </section>

  {sections_html}

  {faq_visible}

  <div class="backlinks">
    Looking for more? Explore <a href="{SITE}/ssc-cgl.html">SSC CGL mock tests &amp; full course</a>,
    or jump to <a href="#faq">FAQs</a>.
  </div>

  <footer>
    © TrickySSC — Free SSC CGL previous year papers, mock tests &amp; solutions in Hindi &amp; English.
  </footer>

</div>
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
