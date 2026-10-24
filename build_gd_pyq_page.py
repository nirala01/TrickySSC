#!/usr/bin/env python3
"""
build_gd_pyq_page.py — bake the SSC GD Constable paper list into ssc-gd-pyq.html
and the four subject-wise GD PYQ pages. Runs from .github/workflows/build-gd-pyq.yml;
nothing to run by hand.

What it does (TSSC-GD-PYQ-V1, 2026-10-24)
-----------------------------------------
* Reads the `papers` collection (one small card per paper per language) over the
  public Firestore REST API — NOT the `questions` collection. The CHSL builder
  scans ~7,600 question docs on every run; this one reads ~2 docs per paper.
* Writes every SSC GD CBE shift into ssc-gd-pyq.html as ordinary <a href> links
  between <!-- LIST:T1:START/END -->, so the crawl path is
      GD PYQ hub -> every shift's test-gd.html URL -> questions
* Rebakes the same shifts as 20-question Part A/B/C/D tests into the four
  ssc-gd-*-previous-year-questions.html pages between <!-- LIST:SUBJ:START/END -->.
* Writes sitemap-gd-pyq.xml (hub + every test URL).
* Stamps window.__PYQ_SIG so the in-page fallback never re-renders a current list.

Safety rails
------------
* Zero cards for the exam is a NORMAL state before the first GD paper is uploaded:
  the pages keep their "papers are being added" empty state and the script exits 0.
* If the page already lists papers and Firestore returns none, the script refuses
  to blank the page (exit 0, nothing written) — a flaky read must never remove
  live papers from the site.
* Mock cards (if any ever land in `papers` with a mockId) are ignored.

Usage
-----
    python build_gd_pyq_page.py --page ssc-gd-pyq.html --sitemap sitemap-gd-pyq.xml
    python build_gd_pyq_page.py --dry-run
"""

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from html import escape

# ── Config ────────────────────────────────────────────────────────────────────
PROJECT = "trickyssc-17bb3"
API_KEY = "AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA"      # public web key, same as the pages
EXAM = "ssc-gd"
EXAM_NAME = "SSC GD Constable"
SITE = "https://trickyssc.com"
PAGE = "ssc-gd-pyq.html"

ENGINE = f"{SITE}/test-gd.html"
SUBJ_ENGINE = f"{SITE}/test-gd-subject.html"
MINS, PER_Q = 60, 2
YEAR_COLORS = ["#FF6B00", "#6366F1", "#00A86B", "#0EA5E9",
               "#E11D48", "#F59E0B", "#8B5CF6", "#10B981"]
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

# the four subject pages: key -> (file, label, questions, minutes, part letter)
SUBJECT_PAGES = {
    "reasoning": ("ssc-gd-reasoning-previous-year-questions.html", "Reasoning", 20, 15, "A"),
    "gk":        ("ssc-gd-gk-previous-year-questions.html",        "GK",        20, 15, "B"),
    "quant":     ("ssc-gd-maths-previous-year-questions.html",     "Maths",     20, 15, "C"),
    "english":   ("ssc-gd-english-previous-year-questions.html",   "English",   20, 15, "D"),
}
SUBJ_BTN = {"reasoning": ("#6366F1", "#818CF8"), "gk": ("#00A86B", "#10B981"),
            "quant": ("#FF6B00", "#FF8C38"), "english": ("#0EA5E9", "#38BDF8")}

RUNQUERY = (f"https://firestore.googleapis.com/v1/projects/{PROJECT}"
            f"/databases/(default)/documents:runQuery?key={API_KEY}")


# ── Fetch ─────────────────────────────────────────────────────────────────────
def _val(v):
    if not v:
        return ""
    for t in ("stringValue", "integerValue", "doubleValue"):
        if t in v:
            return str(v[t])
    return ""


def fetch_cards():
    """Every `papers` card of this exam: {year, shift, tier, heldOn, language, paperId, questionCount, mockId}."""
    body = {"structuredQuery": {
        "from": [{"collectionId": "papers"}],
        "where": {"fieldFilter": {"field": {"fieldPath": "exam"}, "op": "EQUAL",
                                  "value": {"stringValue": EXAM}}},
    }}
    req = urllib.request.Request(RUNQUERY, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "Mozilla/5.0 (compatible; TrickySSC-build/1.0)"},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=120) as res:
        rows = json.loads(res.read().decode("utf-8"))
    cards = []
    for r in rows:
        d = r.get("document")
        if not d or "fields" not in d:
            continue
        f = d["fields"]
        c = {k: _val(f.get(k)) for k in ("year", "shift", "tier", "heldOn", "language", "lang", "paperId", "mockId", "type")}
        c["questionCount"] = int(float(_val(f.get("questionCount")) or 0))
        if not c["paperId"]:
            c["paperId"] = d["name"].rsplit("/", 1)[-1]
        if not c["language"]:
            c["language"] = c["lang"]
        cards.append(c)
    return cards


def is_mock(c):
    return (c.get("type") or "").strip().lower() == "mock" or bool((c.get("mockId") or "").strip())


# ── Shape ─────────────────────────────────────────────────────────────────────
def norm_lang(l):
    v = (l or "").strip().lower()
    if v in ("hindi", "हिंदी", "हिन्दी"):
        v = "hi"
    if v in ("english", "eng"):
        v = "en"
    return "hi" if v == "hi" else "en"


def build_papers(cards):
    papers = {}
    for c in cards:
        if is_mock(c):
            continue
        if "2" in (c["tier"] or "").lower():       # GD has a single CBE; ignore anything mis-tagged
            continue
        key = (c["year"], c["shift"], c["heldOn"])
        p = papers.get(key)
        if p is None:
            p = papers[key] = {"year": c["year"], "tier": "t1", "tierRaw": c["tier"] or "tier1",
                               "shift": c["shift"], "heldOn": c["heldOn"],
                               "en": 0, "hi": 0, "pidEn": "", "pidHi": ""}
        n = c["questionCount"] or 1
        if norm_lang(c["language"]) == "hi":
            p["hi"] = max(p["hi"], n)
            if c["paperId"] and not p["pidHi"]:
                p["pidHi"] = c["paperId"]
        else:
            p["en"] = max(p["en"], n)
            if c["paperId"] and not p["pidEn"]:
                p["pidEn"] = c["paperId"]
    return [p for p in papers.values() if p["en"] or p["hi"]]


def signature(papers):
    """djb2 over the sorted paper set, base36, plus the count."""
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
def paper_id(p, lang):
    stored = p["pidHi"] if lang == "hi" else p["pidEn"]
    if stored:
        return stored
    parts = [EXAM, p["year"], "tier1", re.sub(r"\s+", "-", (p["shift"] or "").lower()), p["heldOn"], lang]
    return "_".join(x for x in parts if x)


def test_url(p, lang):
    q = urllib.parse.urlencode({"exam": EXAM, "year": p["year"], "tier": "tier1",
                                "shift": p["shift"], "heldOn": p["heldOn"], "lang": lang,
                                "paperId": paper_id(p, lang)})
    return f"{ENGINE}?{q}"


def fmt_date(d):
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", d or "")
    if not m:
        return d or ""
    return f"{int(m.group(3))} {MONTHS[int(m.group(2)) - 1]} {m.group(1)}"


def e(s):
    return escape(str(s if s is not None else ""), quote=True)


def row_html(p):
    q_count = max(p["en"], p["hi"])
    marks = q_count * PER_Q
    date = fmt_date(p["heldOn"])
    shift = p["shift"] or "Full Paper"
    s_num = re.search(r"Shift[- ]?(\d+)", p["shift"] or "", re.I)
    pick = re.sub(r"\s+", "-", "-".join([EXAM, "t1", p["year"], p["shift"] or "full", p["heldOn"] or ""]))
    title = f"{EXAM_NAME} CBE {p['year']} · {shift}" + (f" · {date}" if date else "")
    label = f"{EXAM_NAME} CBE {p['year']} {shift}" + (f" ({date})" if date else "")
    en_url = test_url(p, "en") if p["en"] else ""
    hi_url = test_url(p, "hi") if p["hi"] else ""
    attrs = ['class="pyq-attempt-btn"', f'href="{e(en_url or hi_url)}"', f'data-pick="{e(pick)}"']
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
    return ('<div class="pyq-row"><div class="pyq-row-l"><div style="min-width:0;">'
            f'<div class="pyq-top"><span class="pyq-shift">{e(shift)}</span>'
            + (f'<span class="pyq-sbadge">S{s_num.group(1)}</span>' if s_num else "")
            + (f'<span class="pyq-date">{e(date)}</span>' if date else "")
            + '</div>'
            f'<div class="pyq-meta"><span class="m">📝 {q_count} Qs</span><span class="m">·</span>'
            f'<span class="m">⏱ {MINS} min</span><span class="m">·</span><span class="m">{marks} marks</span>'
            f'<span class="attempt-pill todo" data-pill="{e(pick)}">○ Not Attempted</span></div>'
            '</div></div>'
            f'<div class="pyq-actions"><a {" ".join(attrs)}>▶ Attempt Test</a>{lang_links}</div>'
            '</div>')


def sort_rows(rows):
    def shift_num(p):
        m = re.search(r"(\d+)", p["shift"] or "")
        return int(m.group(1)) if m else 0
    return sorted(rows, key=lambda p: (p["heldOn"] or "", -shift_num(p)), reverse=True)


def empty_html(what):
    return ('\n<div class="pyq-empty"><div style="font-size:2rem;margin-bottom:0.5rem;">📭</div>'
            '<div style="font-family:\'Rajdhani\',sans-serif;font-weight:800;font-size:1.05rem;color:#1E293B;'
            'margin-bottom:0.25rem;">SSC GD papers are being added</div>'
            f'<div style="font-size:0.85rem;">The first {EXAM_NAME} {what} will appear here automatically as soon as '
            'they are uploaded — this page rebuilds itself every few hours.</div></div>\n')


def list_html(papers):
    if not papers:
        return empty_html("CBE shifts")
    grouped = defaultdict(list)
    for p in papers:
        grouped[p["year"] or "Other"].append(p)
    years = sorted(grouped, key=lambda y: int(y) if y.isdigit() else -1, reverse=True)
    out = ["\n"]
    for yi, year in enumerate(years):
        accent = YEAR_COLORS[yi % len(YEAR_COLORS)]
        rows = sort_rows(grouped[year])
        out.append(f'<details class="yr-acc"{" open" if yi == 0 else ""}>\n'
                   f'  <summary class="yr-head">\n'
                   f'    <span class="yr-badge" style="background:{accent};">{e(year)}</span>\n'
                   f'    <span class="yr-title">{EXAM_NAME} CBE {e(year)}</span>\n'
                   f'    <span class="yr-count">{len(rows)} test{"s" if len(rows) != 1 else ""}</span>\n'
                   f'    <span class="yr-chev" aria-hidden="true">▾</span>\n'
                   f'  </summary>\n'
                   f'  <div class="yr-body" style="border-left:3px solid {accent};">\n')
        for p in rows:
            out.append("    " + row_html(p) + "\n")
        out.append("  </div>\n</details>\n")
    return "".join(out)


def item_list_json(papers):
    items = []
    for i, p in enumerate(papers[:300], start=1):
        date = fmt_date(p["heldOn"]) or p["year"]
        name = f"{EXAM_NAME} CBE {date} {p['shift']} — Free Online Test"
        items.append({"@type": "ListItem", "position": i, "name": re.sub(r"\s+", " ", name).strip(),
                      "url": test_url(p, "en" if p["en"] else "hi")})
    payload = {"@context": "https://schema.org", "@type": "ItemList",
               "name": f"Free {EXAM_NAME} PYQ Tests (Previous Year Papers) — Online in Hindi & English",
               "numberOfItems": len(items), "itemListElement": items}
    return ('<script type="application/ld+json" id="pyqItemList">\n'
            + json.dumps(payload, ensure_ascii=False) + "\n</script>")


# ── Subject pages ─────────────────────────────────────────────────────────────
def subj_url(p, lang, key):
    return test_url(p, lang).replace(ENGINE, SUBJ_ENGINE, 1) + "&subject=" + key


def subj_row_html(p, key, label, q, mins):
    date = fmt_date(p["heldOn"])
    shift = p["shift"] or "Full Paper"
    s_num = re.search(r"Shift[- ]?(\d+)", p["shift"] or "", re.I)
    pick = re.sub(r"\s+", "-", "-".join([EXAM, "t1", p["year"], p["shift"] or "full", p["heldOn"] or "", key]))
    title = f"{EXAM_NAME} CBE {p['year']} · {shift}" + (f" · {date}" if date else "") + f" · {label}"
    en_url = subj_url(p, "en", key) if p["en"] else ""
    hi_url = subj_url(p, "hi", key) if p["hi"] else ""
    c1, c2 = SUBJ_BTN.get(key, ("#FF6B00", "#FF8C38"))
    attrs = ['class="pyq-attempt-btn"', f'href="{e(en_url or hi_url)}"', f'data-pick="{e(pick)}"']
    if en_url:
        attrs.append(f'data-en="{e(en_url)}" data-pid-en="{e(paper_id(p, "en") + "__" + key)}"')
    if hi_url:
        attrs.append(f'data-hi="{e(hi_url)}" data-pid-hi="{e(paper_id(p, "hi") + "__" + key)}"')
    attrs += [f'data-title="{e(title)}"', 'onclick="openLangChooser(this);return false;"',
              f'style="display:inline-flex;align-items:center;gap:0.35rem;background:linear-gradient(135deg,{c1},{c2});'
              'color:#fff;border:none;border-radius:10px;padding:0.5rem 0.95rem;font-family:\'Rajdhani\',sans-serif;'
              'font-weight:700;font-size:0.88rem;text-decoration:none;white-space:nowrap;"']
    grey = 'style="font-size:0.72rem;color:#94A3B8;"'
    return ('<div class="pyq-row" style="display:flex;align-items:center;justify-content:space-between;gap:0.6rem;'
            'padding:0.85rem 1.1rem;border-bottom:1px solid #F1F5F9;background:white;">'
            '<div style="min-width:0;"><div style="display:flex;align-items:center;gap:0.45rem;flex-wrap:wrap;">'
            f'<span style="font-family:\'Rajdhani\',sans-serif;font-weight:700;font-size:0.95rem;color:#1A202C;">{e(shift)}</span>'
            + (f'<span style="display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;'
               f'border-radius:5px;background:#F1F5F9;font-family:\'Rajdhani\',sans-serif;font-weight:700;font-size:0.7rem;'
               f'color:#475569;">S{s_num.group(1)}</span>' if s_num else "")
            + (f'<span style="font-size:0.82rem;color:#475569;">{e(date)}</span>' if date else "")
            + '</div><div style="display:flex;align-items:center;gap:0.5rem;margin-top:0.2rem;flex-wrap:wrap;">'
            f'<span {grey}>📝 {q} {e(label)} Qs</span><span {grey}>·</span><span {grey}>⏱ {mins} min</span>'
            f'<span {grey}>·</span><span {grey}>{q * PER_Q} marks</span>'
            f'<span class="attempt-pill todo" data-pill="{e(pick)}">○ Not Attempted</span></div></div>'
            f'<a {" ".join(attrs)}>▶ Attempt Test</a></div>')


def subj_list_html(key, papers):
    fname, label, q, mins, part = SUBJECT_PAGES[key]
    if not papers:
        return empty_html(f"{label} tests (Part {part})")
    grouped = defaultdict(list)
    for p in papers:
        grouped[p["year"] or "Other"].append(p)
    years = sorted(grouped, key=lambda y: int(y) if y.isdigit() else -1, reverse=True)
    out = ["\n"]
    for yi, year in enumerate(years):
        accent = YEAR_COLORS[yi % len(YEAR_COLORS)]
        rows = sort_rows(grouped[year])
        out.append(f'<details class="yr-acc"{" open" if yi == 0 else ""}><summary class="yr-head">'
                   f'<span class="yr-badge" style="background:{accent};">{e(year)}</span>'
                   f'<span class="yr-title">{EXAM_NAME} CBE {e(year)} — {e(label)}</span>'
                   f'<span class="yr-count">{len(rows)} test{"s" if len(rows) != 1 else ""}</span>'
                   f'<span class="yr-chev" aria-hidden="true">▾</span></summary>'
                   f'<div class="yr-body" style="border-left:3px solid {accent};">\n')
        for p in rows:
            out.append(subj_row_html(p, key, label, q, mins) + "\n")
        out.append("</div></details>\n")
    return "".join(out)


def bake_subject_pages(papers, root, dry_run):
    written = []
    for key, (fname, label, q, mins, part) in SUBJECT_PAGES.items():
        path = os.path.join(root, fname)
        if not os.path.exists(path):
            print(f"  ! {fname} not found — skipped", file=sys.stderr)
            continue
        html = open(path, encoding="utf-8").read()
        html = between(html, "<!-- LIST:SUBJ:START -->", "<!-- LIST:SUBJ:END -->", subj_list_html(key, papers))
        html = set_text(html, "subjCount", f"{len(papers)} Test{'s' if len(papers) != 1 else ''}")
        html = set_text(html, "heroCount", str(len(papers)))
        if not dry_run:
            open(path, "w", encoding="utf-8", newline="\n").write(html)
        written.append(fname)
    print(f"[build] subject pages: {len(written)} baked")
    return written


# ── Injection ─────────────────────────────────────────────────────────────────
def between(html, start, end, new):
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pat.search(html):
        raise SystemExit(f"marker pair not found in page: {start} … {end}")
    return pat.sub(lambda _: start + new + end, html, count=1)


def set_text(html, el_id, text):
    pat = re.compile(r'(<(span|p|div) id="' + el_id + r'"[^>]*>).*?(</\2>)', re.S)
    if not pat.search(html):
        print(f"  ! #{el_id} not found — skipped", file=sys.stderr)
        return html
    return pat.sub(lambda m: m.group(1) + text + m.group(3), html, count=1)


def build(page_path, sitemap_path=None, dry_run=False, subject_pages=True):
    print(f"[build] reading `papers` cards for {EXAM} …")
    cards = fetch_cards()
    print(f"[build] {len(cards)} cards fetched")
    papers = build_papers(cards)
    sig = signature(papers)
    print(f"[build] {len(papers)} papers  sig={sig}")

    html = open(page_path, encoding="utf-8").read()
    already = len(re.findall(r'data-pick="', html.split("<!-- LIST:T1:START -->", 1)[-1].split("<!-- LIST:T1:END -->", 1)[0]))
    if not papers and already:
        print(f"[build] Firestore returned no GD papers but the page lists {already} — refusing to blank it", file=sys.stderr)
        return 0

    html = between(html, "<!-- LIST:T1:START -->", "<!-- LIST:T1:END -->", list_html(papers))
    html = between(html, "<!-- ITEMLIST:START -->", "<!-- ITEMLIST:END -->", "\n" + item_list_json(papers) + "\n")
    html = re.sub(r"window\.__PYQ_SIG = '[^']*';/\*SIG\*/", f"window.__PYQ_SIG = '{sig}';/*SIG*/", html, count=1)

    years = sorted({int(p["year"]) for p in papers if p["year"].isdigit()})
    span = f"{years[0]}–{years[-1]}" if len(years) > 1 else (str(years[0]) if years else "")
    html = set_text(html, "t1-count", f"{len(papers)} Paper{'s' if len(papers) != 1 else ''}")
    html = set_text(html, "heroCount", f"{len(papers)} Paper{'s' if len(papers) != 1 else ''}")
    html = set_text(html, "heroSub", f"CBE{' · ' + span if span else ''} · Shift-wise with solutions")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    html = re.sub(r"<!-- built:[^>]*-->\n?", "", html)
    html = html.replace("</body>", f"<!-- built: {stamp} · {len(papers)} papers · sig {sig} -->\n</body>")

    if dry_run:
        print("[build] --dry-run: page not written")
    else:
        open(page_path, "w", encoding="utf-8", newline="\n").write(html)
        print(f"[build] wrote {page_path}")

    if subject_pages:
        bake_subject_pages(papers, os.path.dirname(os.path.abspath(page_path)), dry_run)

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
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n")
        if dry_run:
            print(f"[build] --dry-run: would write {len(urls)} urls to {sitemap_path}")
        else:
            open(sitemap_path, "w", encoding="utf-8", newline="\n").write(xml)
            print(f"[build] wrote {sitemap_path} ({len(urls)} urls)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Bake the SSC GD PYQ list into static HTML")
    ap.add_argument("--page", default=PAGE)
    ap.add_argument("--sitemap", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-subject-pages", action="store_true")
    a = ap.parse_args()
    sys.exit(build(a.page, a.sitemap, a.dry_run, not a.no_subject_pages))
