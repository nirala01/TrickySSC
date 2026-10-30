#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_mock_live.py — keep the mock pages' live state in sync with Firestore.

Designed to run unattended in GitHub Actions, the same way build_pyq_page.py
keeps the PYQ hub current. Reads the `mock_tests` collection over the Firestore
REST API (no credentials needed — the same public web API key the pages already
use), works out which mocks are published, and rewrites the static mock pages so
the HTML itself (what Google indexes) shows released mocks as live instead of
"Releasing soon".

TSSC-MOCKLIVE-V2 (2026-10-15): covers every series, not just CGL Tier I —
    SSC CGL  Tier I   -> ssc-cgl-mock-test.html, mock-list.html
    SSC CGL  Tier II  -> ssc-cgl-mock-test.html, mock-list.html, ssc-cgl-tier-2-mock-test.html
    SSC CHSL Tier I   -> ssc-chsl-mock-test.html
    SSC CHSL Tier II  -> ssc-chsl-tier-2-mock-test.html
    SSC GD   CBE      -> ssc-gd-mock-test.html + the four ssc-gd-*-mock-test.html subject pages (TSSC-GD-MOCK-V1)
CHSL Refresher cards (Mock 31-40, data-refresher) are never flipped here: they
open by date through tssc-chsl-refresher.js, so the page script handles them.

    python update_mock_live.py                 # sync from Firestore
    python update_mock_live.py --live 36       # force CGL Tier I to 1..36, skip Firestore
    python update_mock_live.py --dry-run       # report only, write nothing

Exit codes: 0 = fine (whether or not anything changed), 1 = real failure.
It deliberately exits 0 and leaves the files untouched when Firestore is
unreachable — a flaky API call must never blank the live count on the site.
Cards only ever go locked -> live here, never back, so a partial read can't
re-lock anything.
"""
import argparse, json, os, re, sys, urllib.request

PROJECT = "trickyssc-17bb3"
API_KEY = "AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA"   # public web key, same as the pages use
COLLECTION = "mock_tests"
NAME_RE = re.compile(r"(ssc-[a-z]+)_(tier[12])_mock(\d+)", re.I)

# (exam, tier) -> pages that carry that series' cards
SERIES = {
    ("ssc-cgl", "tier1"):  ["ssc-cgl-mock-test.html", "mock-list.html"],
    ("ssc-cgl", "tier2"):  ["ssc-cgl-mock-test.html", "mock-list.html",
                            "ssc-cgl-tier-2-mock-test.html"],
    ("ssc-chsl", "tier1"): ["ssc-chsl-mock-test.html"],
    ("ssc-chsl", "tier2"): ["ssc-chsl-tier-2-mock-test.html"],
    # TSSC-GD-MOCK-V1: the GD series is a single CBE stored as tier1; its subject pages carry the same cards
    ("ssc-gd", "tier1"):   ["ssc-gd-mock-test.html", "ssc-gd-reasoning-mock-test.html", "ssc-gd-gk-mock-test.html",
                            "ssc-gd-maths-mock-test.html", "ssc-gd-english-mock-test.html"],
}
# pages that show the "N Live" status bar for an exam's tiers
BAR_PAGES = {
    "ssc-cgl":  ["ssc-cgl-mock-test.html", "ssc-cgl-tier-2-mock-test.html"],
    "ssc-chsl": ["ssc-chsl-mock-test.html", "ssc-chsl-tier-2-mock-test.html"],
    "ssc-gd":   ["ssc-gd-mock-test.html", "ssc-gd-reasoning-mock-test.html", "ssc-gd-gk-mock-test.html",
                 "ssc-gd-maths-mock-test.html", "ssc-gd-english-mock-test.html"],
}
ALL_PAGES = sorted({p for v in SERIES.values() for p in v})

# A not-yet-live card: exactly class="mock-card locked" (refresher cards carry
# an extra mc-is-ref class and are skipped on purpose).
CARD = re.compile(r'<div class="mock-card locked"(?P<attrs> [^>]*)>(?P<body>.*?)\n</div>', re.S)
# the "📅 Releasing soon" / "📅 Live 15 Oct 2026" overlay pill
LOCK = re.compile(r'\s*<div class="mc-lock"><span>[^<]*</span></div>')
# Free/Premium badge — every card already ships with the right one baked in;
# only cards that somehow lack one get it added.
BADGE = re.compile(r'<div class="mc-lock mc-(?:free|paid)-tag">')
FREE_TAG = ('\n  <div class="mc-lock mc-free-tag">'
            '<span><i class="mc-ico">&#10004;</i>Free</span></div>')
PAID_TAG = ('\n  <div class="mc-lock mc-paid-tag">'
            '<span><i class="mc-coin">&#129689;</i>Premium</span></div>'
            '\n  <button class="mc-locktag" type="button" '
            'aria-label="Premium mock — unlock to attempt">'
            '<i>&#128274;</i>Unlock</button>')
FREE_UPTO = {"ssc-cgl": 4, "ssc-chsl": 2, "ssc-gd": 3}   # TSSC-GD-FREEALL-V1: Free pill on Mock 1-3 while all GD mocks are free (restore 2)


# ----------------------------------------------------------------- Firestore
def _val(f, key):
    v = f.get(key, {})
    for t in ("stringValue", "integerValue", "doubleValue", "booleanValue"):
        if t in v:
            return v[t]
    return None


def fetch_published():
    """{(exam, tier): set(seriesNum)} of published mocks, or None if unreadable."""
    base = ("https://firestore.googleapis.com/v1/projects/%s/databases/(default)"
            "/documents/%s?pageSize=300&key=%s" % (PROJECT, COLLECTION, API_KEY))
    out, token, pages = {}, None, 0
    while pages < 20:
        url = base + ("&pageToken=" + token if token else "")
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                data = json.load(r)
        except Exception as e:
            print("!! Firestore read failed (%s) — leaving pages unchanged" % e)
            return None
        for doc in data.get("documents", []):
            f = doc.get("fields", {})
            # same rule as the pages: a doc counts only when isPublished is true
            if _val(f, "isPublished") is not True:
                continue
            exam, tier, n = _val(f, "exam"), _val(f, "tier"), _val(f, "seriesNum")
            if not (exam and tier and n is not None):          # fall back to the doc id
                m = NAME_RE.search(doc.get("name", "").rsplit("/", 1)[-1])
                if not m:
                    continue
                exam, tier, n = m.group(1), m.group(2), m.group(3)
            try:
                n = int(float(n))
            except (TypeError, ValueError):
                continue
            tier = "tier2" if tier == "tier2" else "tier1"
            out.setdefault((exam.lower(), tier), set()).add(n)
        token = data.get("nextPageToken")
        pages += 1
        if not token:
            break
    if not out:
        print("!! No published mock docs found in %s — leaving pages unchanged" % COLLECTION)
        return None
    for k in sorted(out):
        print("   Firestore: %-8s %s  %d published (max %d)" % (k[0], k[1], len(out[k]), max(out[k])))
    return out


# --------------------------------------------------------------------- pages
def flip_cards(s, exam, tier, nums):
    """Turn locked cards of this series into live ones where published."""
    flipped = []
    prefix = "%s_%s_mock" % (exam, tier)

    def repl(m):
        attrs = m.group("attrs")
        dm = re.search(r'data-mock="([^"]+)"', attrs)
        if not dm or not dm.group(1).startswith(prefix) or "data-refresher" in attrs:
            return m.group(0)
        n = int(dm.group(1)[len(prefix):])
        if n not in nums:
            return m.group(0)
        body = LOCK.sub("", m.group("body"))
        if not BADGE.search(body):
            body += FREE_TAG if n <= FREE_UPTO.get(exam, 0) else PAID_TAG
        flipped.append(n)
        return '<div class="mock-card live resolved"%s>%s\n</div>' % (attrs, body)

    return CARD.sub(repl, s), flipped


def set_bar(s, tier, count):
    """Static status bar -> '● N Live' (only ever upwards from 'soon')."""
    bar_id = "barTier1" if tier == "tier1" else "barTier2"
    pat = re.compile(r'<span class="tb-status [a-z]+" id="%s">(?:<span class="tb-live-dot"></span>)?'
                     r'(?P<txt>[^<]*)</span>' % bar_id)
    m = pat.search(s)
    if not m:
        return s
    old = re.match(r"(\d+) Live", m.group("txt"))
    if old and int(old.group(1)) >= count:
        return s
    return s[:m.start()] + ('<span class="tb-status live" id="%s"><span class="tb-live-dot"></span>%d Live</span>'
                            % (bar_id, count)) + s[m.end():]


def cgl_tier1_counters(s, live):
    """The CGL Tier I counters the original script kept (tc1 / hero pill)."""
    s = re.sub(r'(<span class="tc" id="tc1">)\d+ live', r'\g<1>%d live' % live, s)
    s = re.sub(r'(<span class="hero-badge">[^<]*?)\d+( Tier I Mocks Live</span>)',
               r'\g<1>%d\g<2>' % live, s)
    return s


def current_cgl_t1_live(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        m = re.search(r'<span class="tc" id="tc1">(\d+) live', fh.read())
    return int(m.group(1)) if m else None


def run(published, dry):
    texts = {}
    for p in ALL_PAGES:
        with open(p, encoding="utf-8") as fh:
            texts[p] = fh.read()
    orig = dict(texts)

    for (exam, tier), pages in SERIES.items():
        nums = published.get((exam, tier), set())
        if not nums:
            continue
        for p in pages:
            texts[p], flipped = flip_cards(texts[p], exam, tier, nums)
            if flipped:
                print("   %-32s %s %s: flipped %s" % (p, exam, tier, sorted(flipped)))
        # refresher numbers (31-40) are date-gated on CHSL, so leave them out of the count
        count = len([n for n in nums if not (exam == "ssc-chsl" and n >= 31)])
        for p in BAR_PAGES.get(exam, []):
            texts[p] = set_bar(texts[p], tier, count)
        if (exam, tier) == ("ssc-cgl", "tier1"):
            for p in pages:
                texts[p] = cgl_tier1_counters(texts[p], max(nums))

    changed = [p for p in ALL_PAGES if texts[p] != orig[p]]
    for p in ALL_PAGES:
        print("   %-32s %s" % (p, "CHANGED" if p in changed else "no change"))
    if not dry:
        for p in changed:
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(texts[p])
    return changed


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", type=int, help="force CGL Tier I to 1..N live, skip Firestore")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    missing = [f for f in ALL_PAGES if not os.path.exists(f)]
    if missing:
        # TSSC-GD-MOCK-V1: a series whose pages are not uploaded yet is skipped, not fatal
        print("!! missing files (skipped): %s" % missing)
        for k in list(SERIES):
            SERIES[k] = [p for p in SERIES[k] if os.path.exists(p)]
        for k in list(BAR_PAGES):
            BAR_PAGES[k] = [p for p in BAR_PAGES[k] if os.path.exists(p)]
        ALL_PAGES = [p for p in ALL_PAGES if os.path.exists(p)]
        if not ALL_PAGES:
            sys.exit(1)

    if a.live:
        if not 1 <= a.live <= 50:
            print("!! refusing an out-of-range live count: %s" % a.live)
            sys.exit(0)
        published = {("ssc-cgl", "tier1"): set(range(1, a.live + 1))}
    else:
        published = fetch_published()
        if published is None:
            sys.exit(0)                  # unreachable API: no change, no failure

    # never move the CGL Tier I counter backwards
    t1 = published.get(("ssc-cgl", "tier1"))
    have = [c for c in (current_cgl_t1_live(f) for f in SERIES[("ssc-cgl", "tier1")]) if c]
    if t1 and have and max(t1) < max(have):
        print("!! CGL Tier I: Firestore says %d but pages show %d — keeping the pages' count"
              % (max(t1), max(have)))
        published[("ssc-cgl", "tier1")] = set(range(1, max(have) + 1))

    changed = run(published, a.dry_run)
    print("\nCHANGED=%s" % ("true" if changed else "false"))
