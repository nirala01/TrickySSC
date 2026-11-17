#!/usr/bin/env python3
"""
build_mts_pyq_page.py — bake the SSC MTS previous-year paper list into ssc-mts.html.
Runs from .github/workflows/build-mts-pyq.yml; nothing to run by hand.

What it does (TSSC-MTS-PYQ-STATIC-V1, 2026-11-17)
-------------------------------------------------
Until now ssc-mts.html asked Firestore for every SSC MTS question (thousands of reads per
visitor) just to list the papers, and the Android app asked Firestore too. This bakes the
list into the page, the way the CGL / CHSL / GD / NTPC PYQ pages work:

* Reads the small `papers` cards of exam ssc-mts, plus question 1 of every paper in
  `questions` (covers a paper uploaded before the cards existed). About 2 reads per paper.
* Writes the rows as ordinary HTML between <!-- LIST:MTS:START/END --> in ssc-mts.html
  (same markup the page's own script draws), so the app reads them with the same parser
  it uses for the other exams, and search engines see real links.
* Stamps window.__MTS_PYQ_DOCS so the page's script draws from it and never queries Firestore.

Safety rails
------------
* If the page already lists papers and Firestore returns none, nothing is written — a flaky
  read must never remove live papers from the site.
* Mock cards / mock questions (type 'mock' or a mockId) are ignored.

Usage
-----
    python build_mts_pyq_page.py
    python build_mts_pyq_page.py --dry-run
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html import escape

PROJECT = "trickyssc-17bb3"
API_KEY = "AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA"      # public web key, same as the pages
EXAM = "ssc-mts"
PAGE = "ssc-mts.html"
DEFAULT_Q = 90                                            # SSC MTS paper size, when a card carries no count
YEAR_COLORS = ["#FF6B00", "#6366F1", "#00A86B", "#0EA5E9", "#E11D48", "#F59E0B", "#8B5CF6", "#10B981"]
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
RUNQUERY = (f"https://firestore.googleapis.com/v1/projects/{PROJECT}"
            f"/databases/(default)/documents:runQuery?key={API_KEY}")
START, END = "<!-- LIST:MTS:START -->", "<!-- LIST:MTS:END -->"


def _val(v):
    if not v:
        return ""
    for t in ("stringValue", "integerValue", "doubleValue"):
        if t in v:
            return str(v[t])
    return ""


def _query(body):
    req = urllib.request.Request(RUNQUERY, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "Mozilla/5.0 (compatible; TrickySSC-build/1.0)"},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=120) as res:
        rows = json.loads(res.read().decode("utf-8"))
    return [r["document"] for r in rows if r.get("document") and "fields" in r["document"]]


def _exam_filter():
    return {"fieldFilter": {"field": {"fieldPath": "exam"}, "op": "EQUAL", "value": {"stringValue": EXAM}}}


def fetch_rows():
    """One row per paper per language: {year, shift, tier, heldOn, language, paperId, n}."""
    rows = []
    for d in _query({"structuredQuery": {"from": [{"collectionId": "papers"}], "where": _exam_filter()}}):
        f = d["fields"]
        c = {k: _val(f.get(k)).strip() for k in ("year", "shift", "tier", "heldOn", "language", "lang", "paperId", "mockId", "type")}
        c["paperId"] = c["paperId"] or d["name"].rsplit("/", 1)[-1]
        c["language"] = c["language"] or c["lang"]
        c["n"] = int(float(_val(f.get("questionCount")) or 0))
        c["card"] = True
        rows.append(c)
    print(f"[build] {len(rows)} `papers` cards")
    q1 = 0
    for one in ({"integerValue": "1"}, {"stringValue": "1"}):
        body = {"structuredQuery": {
            "from": [{"collectionId": "questions"}],
            "where": {"compositeFilter": {"op": "AND", "filters": [
                _exam_filter(),
                {"fieldFilter": {"field": {"fieldPath": "qNum"}, "op": "EQUAL", "value": one}}]}},
            "select": {"fields": [{"fieldPath": k} for k in ("year", "shift", "tier", "heldOn", "language", "type", "mockId", "paperId")]},
        }}
        try:
            docs = _query(body)
        except Exception as ex:                                   # the cards alone are enough
            print(f"  ! question-1 lookup failed ({ex}) — using the cards only", file=sys.stderr)
            continue
        for d in docs:
            f = d["fields"]
            c = {k: _val(f.get(k)).strip() for k in ("year", "shift", "tier", "heldOn", "language", "paperId", "mockId", "type")}
            c["n"] = 0
            c["card"] = False
            rows.append(c)
            q1 += 1
    print(f"[build] {q1} question-1 rows")
    return rows


def is_mock(c):
    return (c.get("type") or "").lower() == "mock" or bool(c.get("mockId"))


def is_hi(l):
    return (l or "").strip().lower() in ("hi", "hindi", "हिंदी", "हिन्दी")


def build_docs(rows):
    """Merge to one doc per (paper, language) — the shape the page's script expects."""
    out = {}
    for c in rows:
        if is_mock(c):
            continue
        if not (c["year"] or c["shift"] or c["heldOn"]):
            continue
        lang = "hi" if is_hi(c["language"]) else "en"
        key = (c["year"], c["shift"], c["heldOn"], c["tier"], lang)
        d = out.get(key)
        if d is None:
            d = out[key] = {"year": c["year"], "shift": c["shift"], "tier": c["tier"], "heldOn": c["heldOn"],
                            "language": lang, "paperId": "", "n": 0}
        if c["paperId"] and (not d["paperId"] or c["card"]):
            d["paperId"] = c["paperId"]
        d["n"] = max(d["n"], c["n"])
    docs = list(out.values())
    for d in docs:
        d["n"] = d["n"] or DEFAULT_Q
    docs.sort(key=lambda d: (d["year"], d["heldOn"], d["shift"], d["tier"], d["language"]))
    return docs


# ── HTML: mirrors show() in ssc-mts.html (TSSC-MTS-PYQ-V2 / V3) ──────────────────
def esc(t):
    return escape(str(t or ""), quote=True).replace("&#x27;", "'")


def fmt(d):
    p = str(d or "").split("-")
    if len(p) == 3 and p[1].isdigit() and 1 <= int(p[1]) <= 12 and p[2].isdigit():
        return f"{int(p[2])} {MON[int(p[1]) - 1]} {p[0]}"
    return d or ""


def enc(s):
    return urllib.parse.quote(str(s or ""), safe="-_.!~*'()")      # same as encodeURIComponent


def url(p, lang, pid):
    q = f"exam={EXAM}&year={enc(p['year'])}&tier={enc(p['tier'])}&shift={enc(p['shift'])}&heldOn={enc(p['heldOn'])}&lang={lang}"
    return f"test.html?{q}&paperId={enc(pid)}" if pid else f"loader.html?{q}"


def papers_of(docs):
    m = {}
    for d in docs:
        k = (d["year"], d["shift"], d["heldOn"], d["tier"])
        p = m.setdefault(k, {"year": d["year"], "shift": d["shift"], "heldOn": d["heldOn"], "tier": d["tier"],
                             "en": 0, "hi": 0, "pidEn": "", "pidHi": ""})
        if d["language"] == "hi":
            p["hi"] += d["n"]
            p["pidHi"] = p["pidHi"] or d["paperId"]
        else:
            p["en"] += d["n"]
            p["pidEn"] = p["pidEn"] or d["paperId"]
    papers = list(m.values())
    papers.sort(key=lambda p: p["shift"])
    papers.sort(key=lambda p: p["heldOn"], reverse=True)
    papers.sort(key=lambda p: int(p["year"]) if p["year"].isdigit() else 0, reverse=True)
    return papers


def list_html(papers):
    by_year, years = {}, []
    for p in papers:
        y = p["year"] or "Other"
        if y not in by_year:
            by_year[y] = []
            years.append(y)
        by_year[y].append(p)
    h = []
    for yi, y in enumerate(years):
        ac = YEAR_COLORS[yi % len(YEAR_COLORS)]
        n = len(by_year[y])
        h.append(f'<details class="yr-acc"{" open" if yi == 0 else ""}><summary class="yr-head">'
                 f'<span class="yr-badge" style="background:{ac};">{esc(y)}</span>'
                 f'<span class="yr-title">SSC MTS {esc(y)}</span>'
                 f'<span class="yr-count">{n} paper{"s" if n != 1 else ""}</span>'
                 f'<span class="yr-chev" aria-hidden="true">&#9662;</span></summary>'
                 f'<div class="yr-body" style="border-left:3px solid {ac};">')
        for p in by_year[y]:
            qs = max(p["en"], p["hi"])
            shift = p["shift"] or "Full Paper"
            date = fmt(p["heldOn"]) if p["heldOn"] else ""
            en_url = url(p, "en", p["pidEn"]) if p["en"] else ""
            hi_url = url(p, "hi", p["pidHi"]) if p["hi"] else ""
            pick = re.sub(r"[^A-Za-z0-9_-]+", "-", "-".join([EXAM, p["year"], p["shift"] or "full", p["heldOn"] or "", p["tier"] or ""]))
            title = f"SSC MTS {p['year']} · {shift}" + (f" · {date}" if date else "")
            a = f'<a class="pyq-attempt-btn" href="{esc(en_url or hi_url)}" data-pick="{esc(pick)}"'
            # data-pid-en is always written (empty when only Hindi exists): the app's list parser looks for it
            a += f' data-pid-en="{esc(p["pidEn"])}"'
            if en_url:
                a += f' data-en="{esc(en_url)}"'
            if hi_url:
                a += f' data-hi="{esc(hi_url)}"' + (f' data-pid-hi="{esc(p["pidHi"])}"' if p["pidHi"] else "")
            a += f' data-title="{esc(title)}" onclick="return openLangChooser(this)">&#9654; Attempt Test</a>'
            h.append('<div class="pyq-row"><div style="min-width:0;">'
                     f'<div><span class="pyq-shift">{esc(shift)}</span>'
                     + (f' <span class="pyq-date">&middot; {esc(date)}</span>' if date else "") + "</div>"
                     f'<div class="pyq-meta"><span>{qs} Qs</span>'
                     f'<span class="attempt-pill todo" data-pill="{esc(pick)}">&#9675; Not Attempted</span></div></div>'
                     + a + "</div>")
        h.append("</div></details>")
    return "\n" + "\n".join(h) + "\n"


def build(page_path, dry_run=False):
    html = open(page_path, encoding="utf-8").read()
    if START not in html or END not in html:
        raise SystemExit(f"markers {START} … {END} not found in {page_path}")
    docs = build_docs(fetch_rows())
    papers = papers_of(docs)
    print(f"[build] {len(papers)} papers ({len(docs)} paper-language rows)")
    already = html.split(START, 1)[1].split(END, 1)[0].count('data-pick="')
    if not papers and already:
        print(f"[build] Firestore returned no MTS papers but the page lists {already} — refusing to blank it", file=sys.stderr)
        return 0
    new = html.split(START, 1)[0] + START + (list_html(papers) if papers else "") + END + html.split(END, 1)[1]
    data = json.dumps(docs, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pat = re.compile(r"window\.__MTS_PYQ_DOCS = .*?;/\*MTSDOCS\*/", re.S)
    if not pat.search(new):
        raise SystemExit("window.__MTS_PYQ_DOCS stamp not found in page")
    new = pat.sub(lambda _: f"window.__MTS_PYQ_DOCS = {data if papers else 'null'};/*MTSDOCS*/", new, count=1)
    new = re.sub(r"<!-- mts-pyq built:[^>]*-->\n?", "", new)
    if new == html:
        print("[build] no change")
        return 0
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    new = new.replace("</body>", f"<!-- mts-pyq built: {stamp} · {len(papers)} papers -->\n</body>")
    if dry_run:
        print("[build] --dry-run: page not written")
    else:
        open(page_path, "w", encoding="utf-8", newline="\n").write(new)
        print(f"[build] wrote {page_path}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Bake the SSC MTS PYQ list into ssc-mts.html")
    ap.add_argument("--page", default=PAGE)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    sys.exit(build(a.page, a.dry_run))
