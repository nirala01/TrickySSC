#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_mock_live.py — keep the mock pages' live state in sync with Firestore.

Designed to run unattended in GitHub Actions, the same way build_pyq_page.py
keeps the PYQ hub current. Reads the `mock_tests` collection over the Firestore
REST API (no credentials needed — the same public web API key the pages already
use), works out which Tier-I mocks are published, and rewrites the two mock
pages if anything changed.

    python update_mock_live.py                 # sync from Firestore
    python update_mock_live.py --live 36       # force a number, skip Firestore
    python update_mock_live.py --dry-run       # report only, write nothing

Exit codes: 0 = fine (whether or not anything changed), 1 = real failure.
It deliberately exits 0 and leaves the files untouched when Firestore is
unreachable — a flaky API call must never blank the live count on the site.
"""
import argparse, json, os, re, sys, urllib.request, urllib.error

PROJECT = "trickyssc-17bb3"
API_KEY = "AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA"   # public web key, same as the pages use
COLLECTION = "mock_tests"
DOC_RE = re.compile(r"ssc-cgl_tier1_mock(\d+)", re.I)

PAGES = ["ssc-cgl-mock-test.html", "mock-list.html"]
CARD = (r'<div class="mock-card locked"([^>]*?)data-tier="tier1"[^>]*?'
        r'data-n="(?P<n>\d+)"[^>]*?>(?P<body>.*?)\n</div>')

# the dated "📅 25 Aug 2026" / "Coming Soon" overlay pill
LOCK = re.compile(r'\s*<div class="mc-lock"><span>[^<]*</span></div>')

# Anything the card may ALREADY carry in its footer. Since TSSC-PAYWALL-V1 the
# not-yet-live cards ship with their Free/Premium badge and lock pill baked in,
# so a flip must strip these and re-emit rather than append — otherwise the card
# ends up with two Premium badges and the lock in the wrong place.
BADGE = re.compile(r'\s*<div class="mc-lock mc-(?:free|paid)-tag">.*?</div>', re.S)
LOCKBTN = re.compile(r'\s*<button class="mc-locktag".*?</button>', re.S)

FREE_TAG = ('\n  <div class="mc-lock mc-free-tag">'
            '<span><i class="mc-ico">&#10004;</i>Free</span></div>')
PAID_TAG = ('\n  <div class="mc-lock mc-paid-tag">'
            '<span><i class="mc-coin">&#129689;</i>Premium</span></div>')
LOCK_BTN = ('\n  <button class="mc-locktag" type="button" '
            'aria-label="Premium mock — unlock to attempt">'
            '<i>&#128274;</i>Unlock</button>')


# ----------------------------------------------------------------- Firestore
def fetch_published_max():
    """Highest published Tier-I mock number, or None if Firestore can't be read."""
    base = ("https://firestore.googleapis.com/v1/projects/%s/databases/(default)"
            "/documents/%s?pageSize=300&key=%s" % (PROJECT, COLLECTION, API_KEY))
    found, token, pages = [], None, 0
    while pages < 10:
        url = base + ("&pageToken=" + token if token else "")
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                data = json.load(r)
        except Exception as e:
            print("!! Firestore read failed (%s) — leaving pages unchanged" % e)
            return None
        for doc in data.get("documents", []):
            name = doc.get("name", "").rsplit("/", 1)[-1]
            m = DOC_RE.search(name)
            if not m:
                continue
            f = doc.get("fields", {})
            pub = f.get("isPublished", {})
            # treat a missing isPublished as published — the card only exists once uploaded
            if "booleanValue" in pub and pub["booleanValue"] is False:
                continue
            found.append(int(m.group(1)))
        token = data.get("nextPageToken")
        pages += 1
        if not token:
            break
    if not found:
        print("!! No ssc-cgl_tier1_mock* docs found in %s — leaving pages unchanged"
              % COLLECTION)
        return None
    print("   Firestore: %d published Tier-I mock docs, highest = %d"
          % (len(set(found)), max(found)))
    return max(found)


# --------------------------------------------------------------------- pages
def current_live(path):
    with open(path, encoding="utf-8") as fh:
        m = re.search(r'<span class="tc" id="tc1">(\d+) live', fh.read())
    return int(m.group(1)) if m else None


def update(path, live, free_upto, dry):
    with open(path, encoding="utf-8") as fh:
        s = fh.read()
    flipped = []

    def repl(m):
        n = int(m.group("n"))
        if n > live:
            return m.group(0)
        # Strip everything the footer may already hold — the dated pill, any
        # Free/Premium badge and any lock button — then re-emit in a fixed
        # order. Keeps the flip idempotent and duplicate-free.
        body = LOCK.sub("", m.group("body"))
        body = BADGE.sub("", body)
        body = LOCKBTN.sub("", body)
        tail = FREE_TAG if n <= free_upto else PAID_TAG + LOCK_BTN
        flipped.append(n)
        return ('<div class="mock-card live resolved"%sdata-tier="tier1" data-n="%d">%s%s\n</div>'
                % (m.group(1), n, body, tail))

    new = re.sub(CARD, repl, s, flags=re.S)
    new = re.sub(r'(<span class="tc" id="tc1">)\d+ live', r'\g<1>%d live' % live, new)
    new = re.sub(r'(<span class="tb-live-dot"></span>)\d+ Live', r'\g<1>%d Live' % live, new)
    # hero pill — "📝 35 Tier I Mocks Live". Was never synced before, so it had
    # drifted well behind the real count on both pages.
    new = re.sub(r'(<span class="hero-badge">[^<]*?)\d+( Tier I Mocks Live</span>)',
                 r'\g<1>%d\g<2>' % live, new)

    if new == s:
        print("   %-26s already at %d live" % (path, live))
        return False
    print("   %-26s -> %d live (flipped %s)" % (path, live, sorted(flipped) or "counts only"))
    if not dry:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new)
    return True


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", type=int, help="force this number instead of reading Firestore")
    ap.add_argument("--free", type=int, default=4, help="mocks 1..N carry the Free badge")
    ap.add_argument("--files", nargs="*", default=PAGES)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    live = a.live if a.live else fetch_published_max()
    if live is None:
        sys.exit(0)                      # unreachable API: no change, no failure
    if not 1 <= live <= 50:
        print("!! refusing an out-of-range live count: %s" % live)
        sys.exit(0)

    missing = [f for f in a.files if not os.path.exists(f)]
    if missing:
        print("!! missing files: %s" % missing)
        sys.exit(1)

    # never move backwards — a partial Firestore read must not re-lock live mocks
    have = [c for c in (current_live(f) for f in a.files) if c is not None]
    if have and live < max(have):
        print("!! Firestore says %d but pages already show %d — refusing to go backwards"
              % (live, max(have)))
        sys.exit(0)

    print("Target: %d Tier-I mocks live (1-%d free)" % (live, a.free))
    changed = [update(f, live, a.free, a.dry_run) for f in a.files]
    print("\nCHANGED=%s" % ("true" if any(changed) else "false"))
