#!/usr/bin/env python3
"""
build_chsl_pyq_page.py — bake the SSC CHSL paper list into ssc-chsl-pyq.html.

Why this exists
---------------
The page can render its paper list from Firestore in the browser, but a
JavaScript-only list gives Google nothing to crawl. This script queries the same
data at build time and writes the list into the HTML as ordinary <a href> links,
so the crawl path is:

    CHSL PYQ hub  ->  every shift's test URL  ->  questions

The in-page script still runs: it compares a signature of the live data against
the one baked in here and only redraws when a paper was uploaded after the last
build. So SEO gets static HTML, users still get instant freshness.

Usage
-----
    py build_chsl_pyq_page.py                      # rewrite ssc-chsl-pyq.html in place
    py build_chsl_pyq_page.py --page path/to.html
    py build_chsl_pyq_page.py --sitemap sitemap-chsl-pyq.xml
    py build_chsl_pyq_page.py --dry-run            # print what would change

On Windows use the full interpreter path if the `py` Store alias is broken:
    C:\\Users\\DELL\\AppData\\Local\\Python\\bin\\python.exe build_chsl_pyq_page.py
"""

import argparse
import json
import re
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from html import escape

# ── Config ────────────────────────────────────────────────────────────────────
PROJECT = "trickyssc-17bb3"
API_KEY = "AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA"
EXAM = "ssc-chsl"
EXAM_NAME = "SSC CHSL"
SITE = "https://trickyssc.com"
PAGE = "ssc-chsl-pyq.html"

ENGINE = {"t1": f"{SITE}/test-chsl.html", "t2": f"{SITE}/test-chsl-tier2.html"}
TIER_META = {
    "t1": {"label": "Tier I", "mins": 60, "perQ": 2},
    "t2": {"label": "Tier II", "mins": 135, "perQ": 3},
}
YEAR_COLORS = ["#FF6B00", "#6366F1", "#00A86B", "#0EA5E9",
               "#E11D48", "#F59E0B", "#8B5CF6", "#10B981"]
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

RUNQUERY = (f"https://firestore.googleapis.com/v1/projects/{PROJECT}"
            f"/databases/(default)/documents:runQuery?key={API_KEY}")


# ── Fetch ─────────────────────────────────────────────────────────────────────
def fetch_meta():
    """Pull just the metadata fields of every question doc for this exam."""
    body = {
        "structuredQuery": {
            "from": [{"collectionId": "questions"}],
            "where": {"fieldFilter": {
                "field": {"fieldPath": "exam"},
                "op": "EQUAL",
                "value": {"stringValue": EXAM},
            }},
            "select": {"fields": [{"fieldPath": f} for f in
                                  ("year", "shift", "tier", "heldOn", "language", "paperId")]},
        }
    }
    req = urllib.request.Request(
        RUNQUERY,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 # a browser-ish UA avoids bot filtering on the way out
                 "User-Agent": "Mozilla/5.0 (compatible; TrickySSC-build/1.0)"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as res:
        rows = json.loads(res.read().decode("utf-8"))

    def val(f, key):
        v = f.get(key)
        if not v:
            return ""
        return str(v.get("stringValue", v.get("integerValue", "")) or "")

    docs = []
    for r in rows:
        d = r.get("document")
        if not d or "fields" not in d:
            continue
        f = d["fields"]
        docs.append({k: val(f, k) for k in
                     ("year", "shift", "tier", "heldOn", "language", "paperId")})
    return docs


# ── Shape the data (mirrors the in-page script) ───────────────────────────────
def tier_key(t):
    v = (t or "").lower()
    if not v:
        return "t1"
    return "t2" if ("2" in v or "ii" in v) else "t1"


def norm_lang(l):
    v = (l or "").strip().lower()
    if v in ("hindi", "हिंदी", "हिन्दी"):
        v = "hi"
    if v in ("english", "eng"):
        v = "en"
    return "hi" if v == "hi" else "en"


def build_papers(docs):
    papers = {}
    for d in docs:
        tk = tier_key(d["tier"])
        key = (d["year"], tk, d["shift"], d["heldOn"])
        p = papers.get(key)
        if p is None:
            p = papers[key] = {"year": d["year"], "tier": tk, "tierRaw": d["tier"],
                               "shift": d["shift"], "heldOn": d["heldOn"],
                               "en": 0, "hi": 0, "pidEn": "", "pidHi": ""}
        if not p["tierRaw"] and d["tier"]:
            p["tierRaw"] = d["tier"]
        if norm_lang(d["language"]) == "hi":
            p["hi"] += 1
            if d["paperId"] and not p["pidHi"]:
                p["pidHi"] = d["paperId"]
        else:
            p["en"] += 1
            if d["paperId"] and not p["pidEn"]:
                p["pidEn"] = d["paperId"]
    return [p for p in papers.values() if p["en"] or p["hi"]]


def signature(papers):
    """djb2 over the sorted paper set — the JS in the page computes this identically."""
    s = ";".join(sorted("|".join([p["year"], p["tier"], p["shift"], p["heldOn"],
                                  str(p["en"]), str(p["hi"])]) for p in papers))
    h = 5381
    for ch in s:
        h = ((h * 33) ^ ord(ch)) & 0xFFFFFFFF
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    b36, n = "", h
    while n:
        b36 = digits[n % 36] + b36
        n //= 36
    return (b36 or "0") + "-" + str(len(papers))


# ── Markup (must match rowHtml() in the page) ─────────────────────────────────
def tier_param(p):
    return p["tierRaw"] or ("tier2" if p["tier"] == "t2" else "tier1")


def paper_id(p, lang):
    stored = p["pidHi"] if lang == "hi" else p["pidEn"]
    if stored:
        return stored
    parts = [EXAM, p["year"], tier_param(p),
             re.sub(r"\s+", "-", (p["shift"] or "").lower()), p["heldOn"], lang]
    return "_".join(x for x in parts if x)


def test_url(p, lang):
    from urllib.parse import urlencode
    q = urlencode({"exam": EXAM, "year": p["year"], "tier": tier_param(p),
                   "shift": p["shift"], "heldOn": p["heldOn"], "lang": lang,
                   "paperId": paper_id(p, lang)})
    return f"{ENGINE[p['tier']]}?{q}"


def fmt_date(d):
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", d or "")
    if not m:
        return d or ""
    return f"{int(m.group(3))} {MONTHS[int(m.group(2)) - 1]} {m.group(1)}"


def e(s):
    return escape(str(s if s is not None else ""), quote=True)


def row_html(p):
    meta = TIER_META[p["tier"]]
    q_count = max(p["en"], p["hi"])
    marks = q_count * meta["perQ"]
    date = fmt_date(p["heldOn"])
    shift = p["shift"] or "Full Paper"
    s_num = re.search(r"Shift[- ]?(\d+)", p["shift"] or "", re.I)
    pick = re.sub(r"\s+", "-", "-".join([EXAM, p["tier"], p["year"],
                                         p["shift"] or "full", p["heldOn"] or ""]))
    title = f"{EXAM_NAME} {meta['label']} {p['year']} · {shift}" + (f" · {date}" if date else "")
    label = f"{EXAM_NAME} {meta['label']} {p['year']} {shift}" + (f" ({date})" if date else "")

    en_url = test_url(p, "en") if p["en"] else ""
    hi_url = test_url(p, "hi") if p["hi"] else ""
    primary = en_url or hi_url

    attrs = ['class="pyq-attempt-btn"', f'href="{e(primary)}"', f'data-pick="{e(pick)}"']
    if en_url:
        attrs.append(f'data-en="{e(en_url)}" data-pid-en="{e(paper_id(p, "en"))}"')
    if hi_url:
        attrs.append(f'data-hi="{e(hi_url)}" data-pid-hi="{e(paper_id(p, "hi"))}"')
    attrs += [f'data-title="{e(title)}"', 'onclick="return openLangChooser(this)"']

    lang_links = ""
    if en_url:
        lang_links += f'<a class="pyq-lang-link" href="{e(en_url)}" title="{e(label)} — English">EN</a>'
    if hi_url:
        lang_links += f'<a class="pyq-lang-link" href="{e(hi_url)}" title="{e(label)} — हिंदी">हिं</a>'

    return (
        '<div class="pyq-row">'
        '<div class="pyq-row-l"><div style="min-width:0;">'
        f'<div class="pyq-top"><span class="pyq-shift">{e(shift)}</span>'
        + (f'<span class="pyq-sbadge">S{s_num.group(1)}</span>' if s_num else "")
        + (f'<span class="pyq-date">{e(date)}</span>' if date else "")
        + '</div>'
        f'<div class="pyq-meta"><span class="m">📝 {q_count} Qs</span><span class="m">·</span>'
        f'<span class="m">⏱ {meta["mins"]} min</span><span class="m">·</span><span class="m">{marks} marks</span>'
        f'<span class="attempt-pill todo" data-pill="{e(pick)}">○ Not Attempted</span></div>'
        '</div></div>'
        f'<div class="pyq-actions"><a {" ".join(attrs)}>▶ Attempt Test</a>{lang_links}</div>'
        '</div>'
    )


def sort_rows(rows):
    """Newest date first, then shift number ascending."""
    def shift_num(p):
        m = re.search(r"(\d+)", p["shift"] or "")
        return int(m.group(1)) if m else 0
    return sorted(rows, key=lambda p: (p["heldOn"] or "", -shift_num(p)), reverse=True)


def tier_html(tk, papers):
    meta = TIER_META[tk]
    if not papers:
        return (f'\n<div class="pyq-empty">'
                f'<div style="font-size:2rem;margin-bottom:0.5rem;">📭</div>'
                f'<div style="font-family:\'Rajdhani\',sans-serif;font-weight:800;font-size:1.05rem;'
                f'color:#1E293B;margin-bottom:0.25rem;">No {meta["label"]} papers yet</div>'
                f'<div style="font-size:0.85rem;">{EXAM_NAME} {meta["label"]} papers will appear here '
                f'automatically as soon as they are uploaded.</div></div>\n')

    grouped = defaultdict(list)
    for p in papers:
        grouped[p["year"] or "Other"].append(p)
    years = sorted(grouped, key=lambda y: int(y) if y.isdigit() else -1, reverse=True)

    out = ["\n"]
    for yi, year in enumerate(years):
        accent = YEAR_COLORS[yi % len(YEAR_COLORS)]
        rows = sort_rows(grouped[year])
        out.append(
            f'<details class="yr-acc"{" open" if yi == 0 else ""}>\n'
            f'  <summary class="yr-head">\n'
            f'    <span class="yr-badge" style="background:{accent};">{e(year)}</span>\n'
            f'    <span class="yr-title">{EXAM_NAME} {meta["label"]} {e(year)}</span>\n'
            f'    <span class="yr-count">{len(rows)} test{"s" if len(rows) != 1 else ""}</span>\n'
            f'    <span class="yr-chev" aria-hidden="true">▾</span>\n'
            f'  </summary>\n'
            f'  <div class="yr-body" style="border-left:3px solid {accent};">\n'
        )
        for p in rows:
            out.append("    " + row_html(p) + "\n")
        out.append("  </div>\n</details>\n")
    return "".join(out)


def item_list_json(papers):
    items = []
    for i, p in enumerate(papers[:300], start=1):
        meta = TIER_META[p["tier"]]
        date = fmt_date(p["heldOn"]) or p["year"]
        name = f"{EXAM_NAME} {meta['label']} {date} {p['shift']} — Free Online Test"
        items.append({"@type": "ListItem", "position": i,
                      "name": re.sub(r"\s+", " ", name).strip(),
                      "url": test_url(p, "en" if p["en"] else "hi")})
    payload = {"@context": "https://schema.org", "@type": "ItemList",
               "name": f"Free {EXAM_NAME} PYQ Tests (Previous Year Papers) — Online in Hindi & English",
               "numberOfItems": len(items), "itemListElement": items}
    return ('<script type="application/ld+json" id="pyqItemList">\n'
            + json.dumps(payload, ensure_ascii=False) + "\n</script>")


# ── Injection ─────────────────────────────────────────────────────────────────
def between(html, start, end, new):
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pat.search(html):
        raise SystemExit(f"marker pair not found in page: {start} … {end}")
    return pat.sub(lambda _: start + new + end, html, count=1)


def set_text(html, el_id, text):
    """Replace the inner text of the element carrying this id (span, p, div …)."""
    pat = re.compile(r'(<(span|p|div) id="' + el_id + r'"[^>]*>).*?(</\2>)', re.S)
    if not pat.search(html):
        print(f"  ! #{el_id} not found — skipped", file=sys.stderr)
        return html
    return pat.sub(lambda m: m.group(1) + text + m.group(3), html, count=1)


def build(page_path, sitemap_path=None, dry_run=False):
    print(f"[build] querying Firestore for {EXAM} …")
    docs = fetch_meta()
    print(f"[build] {len(docs)} question docs")
    papers = build_papers(docs)
    t1 = [p for p in papers if p["tier"] == "t1"]
    t2 = [p for p in papers if p["tier"] == "t2"]
    sig = signature(papers)
    print(f"[build] {len(papers)} papers  (Tier I: {len(t1)}, Tier II: {len(t2)})  sig={sig}")

    if not papers:
        print("[build] no papers returned — refusing to blank the page", file=sys.stderr)
        return 1

    html = open(page_path, encoding="utf-8").read()
    html = between(html, "<!-- LIST:T1:START -->", "<!-- LIST:T1:END -->", tier_html("t1", t1))
    html = between(html, "<!-- LIST:T2:START -->", "<!-- LIST:T2:END -->", tier_html("t2", t2))
    html = between(html, "<!-- ITEMLIST:START -->", "<!-- ITEMLIST:END -->",
                   "\n" + item_list_json(papers) + "\n")
    html = re.sub(r"window\.__PYQ_SIG = '[^']*';/\*SIG\*/",
                  f"window.__PYQ_SIG = '{sig}';/*SIG*/", html, count=1)

    years = sorted({int(p["year"]) for p in papers if p["year"].isdigit()})
    span = f"{years[0]}–{years[-1]}" if len(years) > 1 else (str(years[0]) if years else "")
    html = set_text(html, "t1-count", f"{len(t1)} Paper{'s' if len(t1) != 1 else ''}")
    html = set_text(html, "t2-count", f"{len(t2)} Paper{'s' if len(t2) != 1 else ''}")
    html = set_text(html, "heroCount", f"{len(papers)} Paper{'s' if len(papers) != 1 else ''}")
    html = set_text(html, "heroSub",
                    f"Tier I &amp; Tier II{' · ' + span if span else ''} · Shift-wise with solutions")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    html = re.sub(r"<!-- built:[^>]*-->\n?", "", html)
    html = html.replace("</body>", f"<!-- built: {stamp} · {len(papers)} papers · sig {sig} -->\n</body>")

    if dry_run:
        print("[build] --dry-run: page not written")
    else:
        open(page_path, "w", encoding="utf-8", newline="\n").write(html)
        print(f"[build] wrote {page_path}")

    if sitemap_path:
        urls = [f"{SITE}/{PAGE}"]
        for p in papers:
            if p["en"]:
                urls.append(test_url(p, "en"))
            if p["hi"]:
                urls.append(test_url(p, "hi"))
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        body = "\n".join(
            f"  <url><loc>{escape(u, quote=True)}</loc><lastmod>{today}</lastmod>"
            f"<changefreq>weekly</changefreq><priority>{'0.9' if i == 0 else '0.7'}</priority></url>"
            for i, u in enumerate(urls))
        xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + body + "\n</urlset>\n")
        if dry_run:
            print(f"[build] --dry-run: would write {len(urls)} urls to {sitemap_path}")
        else:
            open(sitemap_path, "w", encoding="utf-8", newline="\n").write(xml)
            print(f"[build] wrote {sitemap_path} ({len(urls)} urls)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Bake the SSC CHSL PYQ list into static HTML")
    ap.add_argument("--page", default=PAGE, help="path to ssc-chsl-pyq.html")
    ap.add_argument("--sitemap", default=None, help="also write a sitemap XML here")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    sys.exit(build(a.page, a.sitemap, a.dry_run))
