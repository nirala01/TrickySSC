#!/usr/bin/env python3
# build_app_pages.py — TSSC-APPPAGES-V1 (2026-11-14)
#
# Makes the app-only copies of the list pages:  <page>.html  ->  app-<page>.html
#
# The website page stays the single source of truth. This script copies it and
#   * takes out everything written for search visitors: meta description / Open Graph /
#     canonical / JSON-LD, the hero, breadcrumb, introductions and the long article
#   * marks the copy  noindex  so Google never lists it or treats it as duplicate content
#   * builds in the app bar (back · title · home) and the five bottom tabs
# and leaves every script exactly as it is, so the mock cards, free/paid locks, language
# chooser, prices and Firestore reads behave the same in the app as on the website.
#
# Nobody edits an app-*.html by hand: change the website page and the workflow
# (.github/workflows/build-app-pages.yml) rebuilds the copy. Standard library only.
#
#   python build_app_pages.py            # rebuild every page in PAGES
#   python build_app_pages.py --check    # exit 1 if any copy is out of date

import html as htmllib
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# website page -> which bottom tab is lit in the app copy
PAGES = {
    'ssc-cgl-mock-test.html': 'mocks',
    'ssc-cgl-tier-2-mock-test.html': 'mocks',
    'ssc-chsl-mock-test.html': 'mocks',
    'ssc-chsl-tier-2-mock-test.html': 'mocks',
    'ssc-mts-mock-test.html': 'mocks',
    'ssc-gd-mock-test.html': 'mocks',
    'rrb-ntpc-mock-test.html': 'mocks',
    'rrb-ntpc-gk-mock-test.html': 'mocks',
    'rrb-ntpc-maths-mock-test.html': 'mocks',
    'rrb-ntpc-reasoning-mock-test.html': 'mocks',
    'ssc-cgl-computer-mock-test.html': 'mocks',
    'ssc-cgl-english-mock-test.html': 'mocks',
    'ssc-cgl-gk-mock-test.html': 'mocks',
    'ssc-cgl-quant-mock-test.html': 'mocks',
    'ssc-cgl-reasoning-mock-test.html': 'mocks',
    'ssc-cgl-tier-2-english-mock-test.html': 'mocks',
    'ssc-cgl-tier-2-gk-mock-test.html': 'mocks',
    'ssc-cgl-tier-2-quant-mock-test.html': 'mocks',
    'ssc-cgl-tier-2-reasoning-mock-test.html': 'mocks',
    'ssc-chsl-english-mock-test.html': 'mocks',
    'ssc-chsl-gk-mock-test.html': 'mocks',
    'ssc-chsl-quant-mock-test.html': 'mocks',
    'ssc-chsl-reasoning-mock-test.html': 'mocks',
    'ssc-chsl-tier-2-computer-mock-test.html': 'mocks',
    'ssc-chsl-tier-2-english-mock-test.html': 'mocks',
    'ssc-chsl-tier-2-gk-mock-test.html': 'mocks',
    'ssc-chsl-tier-2-quant-mock-test.html': 'mocks',
    'ssc-chsl-tier-2-reasoning-mock-test.html': 'mocks',
    'ssc-gd-english-mock-test.html': 'mocks',
    'ssc-gd-gk-mock-test.html': 'mocks',
    'ssc-gd-maths-mock-test.html': 'mocks',
    'ssc-gd-reasoning-mock-test.html': 'mocks',
    'ssc-mts-english-mock-test.html': 'mocks',
    'ssc-mts-gk-mock-test.html': 'mocks',
    'ssc-mts-maths-mock-test.html': 'mocks',
    'ssc-mts-reasoning-mock-test.html': 'mocks',
    'mock-list.html': 'mocks',
    'ssc-cgl-tier-2-pyq.html': 'pyq',
    'rrb-ntpc-gk-previous-year-questions.html': 'pyq',
    'rrb-ntpc-maths-previous-year-questions.html': 'pyq',
    'rrb-ntpc-reasoning-previous-year-questions.html': 'pyq',
    'ssc-cgl-english-previous-year-questions.html': 'pyq',
    'ssc-cgl-gk-previous-year-questions.html': 'pyq',
    'ssc-cgl-quant-previous-year-questions.html': 'pyq',
    'ssc-cgl-reasoning-previous-year-questions.html': 'pyq',
    'ssc-cgl-tier-2-english-previous-year-questions.html': 'pyq',
    'ssc-cgl-tier-2-gk-previous-year-questions.html': 'pyq',
    'ssc-cgl-tier-2-quant-previous-year-questions.html': 'pyq',
    'ssc-cgl-tier-2-reasoning-previous-year-questions.html': 'pyq',
    'ssc-chsl-english-previous-year-questions.html': 'pyq',
    'ssc-chsl-gk-previous-year-questions.html': 'pyq',
    'ssc-chsl-quant-previous-year-questions.html': 'pyq',
    'ssc-chsl-reasoning-previous-year-questions.html': 'pyq',
    'ssc-chsl-tier-2-computer-previous-year-questions.html': 'pyq',
    'ssc-chsl-tier-2-english-previous-year-questions.html': 'pyq',
    'ssc-chsl-tier-2-gk-previous-year-questions.html': 'pyq',
    'ssc-chsl-tier-2-quant-previous-year-questions.html': 'pyq',
    'ssc-chsl-tier-2-reasoning-previous-year-questions.html': 'pyq',
    'ssc-gd-english-previous-year-questions.html': 'pyq',
    'ssc-gd-gk-previous-year-questions.html': 'pyq',
    'ssc-gd-maths-previous-year-questions.html': 'pyq',
    'ssc-gd-reasoning-previous-year-questions.html': 'pyq',
    'ssc-cgl-pyq.html': 'pyq',
    'ssc-chsl-pyq.html': 'pyq',
    'ssc-gd-pyq.html': 'pyq',
    'rrb-ntpc-pyq.html': 'pyq',
    'ssc-pyq-chapterwise.html': 'chapters',   # chapter-wise PYQs: subject list only
    'login.html': 'login',          # sign-in screen: no tabs, no back bar
}

# blocks removed from the copy: (tag, class). Written for search visitors, not app users.
CUT_BY_CLASS = [
    ('div', 'crumb'), ('div', 'breadcrumb'), ('div', 'hero'), ('p', 'tier-intro'), ('div', 'tier-bars'),
    ('section', 'seo-content'), ('div', 'mock-explain'), ('p', 'mlb-sub'), ('div', 'pyq-seo-index'),
    ('div', 'left-panel'), ('a', 'back-link'),          # login page: the website's sales panel and "Back to Home"
]

VOID = {'br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'area', 'base', 'col', 'embed', 'track', 'wbr'}
TOKEN = re.compile(r'<!--.*?-->|<(script|style)\b[^>]*>.*?</\1\s*>|<(/?)([a-zA-Z][a-zA-Z0-9]*)\b([^>]*)>', re.S)


def raw_ranges(doc):
    """(start, end) of every comment, <script> and <style>: never look for markup inside these."""
    return [(m.start(), m.end()) for m in TOKEN.finditer(doc) if m.group(3) is None]


def in_ranges(pos, ranges):
    for a, b in ranges:
        if a <= pos < b:
            return True
        if a > pos:
            break
    return False


def element_end(doc, start):
    """Index just past the element whose opening tag starts at `start` (counts same-name tags only,
    so an unclosed <p> or <li> inside it cannot throw the count off)."""
    first = TOKEN.match(doc, start)
    if not first or first.group(3) is None or first.group(2):
        return None
    name = first.group(3).lower()
    if name in VOID:
        return first.end()
    depth = 0
    for m in TOKEN.finditer(doc, start):
        if m.group(3) is None or m.group(3).lower() != name:
            continue
        if m.group(2):
            depth -= 1
        elif not m.group(4).rstrip().endswith('/'):
            depth += 1
        if depth == 0:
            return m.end()
    return None


def scripts_text(doc):
    return '\n'.join(m.group(0) for m in TOKEN.finditer(doc) if m.group(1) == 'script')


def safe_to_cut(chunk, js):
    """A block is only removed when no script mentions an id inside it; otherwise it is hidden,
    so page code that fills or reads it keeps working."""
    for i in re.findall(r'\bid="([^"]+)"', chunk):
        if re.search(r'''['"#]''' + re.escape(i) + r'''\b''', js):
            return False
    return True


def drop(doc, start, end, js, log, label):
    chunk = doc[start:end]
    if safe_to_cut(chunk, js):
        log.append('cut  %-28s %6d bytes' % (label, len(chunk)))
        return doc[:start] + doc[end:], start
    m = TOKEN.match(doc, start)
    log.append('hide %-28s (a script uses an id inside it)' % label)
    opened = doc[start:m.end() - 1] + ' data-tsa-hide>'
    return doc[:start] + opened + doc[m.end():end] + doc[end:], start + len(opened)


def cut_by_class(doc, tag, cls, js, log):
    pat = re.compile(r'<%s\b[^>]*\bclass="(?:[^"]*\s)?%s(?:\s[^"]*)?"[^>]*>' % (tag, re.escape(cls)))
    pos = 0
    while True:
        m = pat.search(doc, pos)
        if not m:
            return doc
        if in_ranges(m.start(), raw_ranges(doc)):
            pos = m.end()
            continue
        end = element_end(doc, m.start())
        if end is None:
            pos = m.end()
            continue
        doc, pos = drop(doc, m.start(), end, js, log, '%s.%s' % (tag, cls))


def cut_mock_heading(doc, js, log):
    """The <h2> that opens the mock list repeats the page title, which is already in the app bar."""
    m = re.search(r'<section\b[^>]*\bclass="[^"]*\bmock-list-block\b[^"]*"[^>]*>\s*(<h2\b)', doc)
    if m and not in_ranges(m.start(), raw_ranges(doc)):
        end = element_end(doc, m.start(1))
        if end:
            doc, _ = drop(doc, m.start(1), end, js, log, 'mock-list-block > h2')
    return doc


def parent_div_start(doc, pos):
    """Start of the nearest <div> that contains position `pos`."""
    ranges = raw_ranges(doc)
    best = None
    for m in re.finditer(r'<div\b[^>]*>', doc[:pos]):
        if in_ranges(m.start(), ranges):
            continue
        end = element_end(doc, m.start())
        if end and end > pos:
            best = m.start()
    return best


def trim_pyq(doc, js, log):
    """PYQ pages are written with inline styles, so they are trimmed by position:
    the heading block and the hero above the papers, and the article sections below them."""
    body = doc.find('<body')
    ranges = raw_ranges(doc)

    # 1. the <h1> block (the title is in the app bar)
    h1 = re.search(r'<h1\b', doc[body:])
    if h1:
        at = body + h1.start()
        par = parent_div_start(doc, at)
        if par is not None:
            end = element_end(doc, par)
            if end and end - par < 2500:
                doc, _ = drop(doc, par, end, js, log, 'pyq heading block')

    # 1b. the breadcrumb strip ("Home › SSC CGL › PYQ Papers"): the app bar has its own back button
    crumb = re.search(r'<div\b[^>]*style="background:#fff;border-bottom:1px solid[^"]*"[^>]*>', doc[body:])
    if crumb:
        at = body + crumb.start()
        end = element_end(doc, at)
        if end and end - at < 2500 and 'Home' in doc[at:end] and ('\u203a' in doc[at:end] or '&rsaquo;' in doc[at:end]) and not in_ranges(at, raw_ranges(doc)):
            doc, _ = drop(doc, at, end, js, log, 'pyq breadcrumb')

    # 2. the dark hero card, and the introduction paragraph right after it
    hero = re.search(r'<div\b[^>]*style="background:linear-gradient\(135deg,#1E1B4B[^"]*"[^>]*>', doc)
    if hero and not in_ranges(hero.start(), raw_ranges(doc)):
        end = element_end(doc, hero.start())
        if end:
            doc, at = drop(doc, hero.start(), end, js, log, 'pyq hero')
            if 'data-tsa-hide' in doc[hero.start():at]:      # hidden, not cut: step past the whole card
                at = element_end(doc, hero.start()) or at
            nxt = re.compile(r'\s*(<p\b)').match(doc, at)
            if nxt:
                pend = element_end(doc, nxt.start(1))
                if pend:
                    doc, _ = drop(doc, nxt.start(1), pend, js, log, 'pyq introduction')

    # 2b. papers first: the "chapter-wise" and "section-wise" practice cards that sit above the
    #     paper list on the website move below it in the app (same cards, same ids, new position)
    moved = []
    for pat in (r'<div\b[^>]*\bclass="(?:[^"]*\s)?pqc-wrap(?:\s[^"]*)?"[^>]*>', r'<div\b[^>]*\bid="tsscPC"[^>]*>'):
        m = re.search(pat, doc)
        pane = re.search(r'<div\b[^>]*\bid="pane-t1"[^>]*>', doc)
        if m and pane and m.start() < pane.start() and not in_ranges(m.start(), raw_ranges(doc)):
            end = element_end(doc, m.start())
            if end and end <= pane.start():
                moved.append(doc[m.start():end])
                doc = doc[:m.start()] + doc[end:]
                log.append('move practice card below the papers')

    # 3. article sections after the paper lists
    last = None
    for pane in ('pane-t2', 'pane-t1'):
        m = re.search(r'<div\b[^>]*\bid="%s"[^>]*>' % pane, doc)
        if m and not in_ranges(m.start(), raw_ranges(doc)):
            e = element_end(doc, m.start())
            if e and (last is None or e > last):
                last = e
    if last:
        pos = last
        sib = re.compile(r'\s*(?:<!--.*?-->\s*)*(<(/?)([a-zA-Z][a-zA-Z0-9]*)\b([^>]*)>)', re.S)
        while True:
            m = sib.match(doc, pos)
            if not m or m.group(2):          # reached the parent's closing tag
                break
            start = m.start(1)
            end = element_end(doc, start)
            if end is None:
                break
            style = re.search(r'\bstyle="([^"]*)"', m.group(4) or '')
            article = bool(m.group(3).lower() == 'div' and style and re.match(r'margin-top:(?:2(?:\.5)?|1\.8)rem', style.group(1)))
            if article:
                doc, pos = drop(doc, start, end, js, log, 'pyq article section')
            else:
                pos = end
        if moved:
            doc = doc[:last] + '\n' + '\n'.join(moved) + '\n' + doc[last:]
    return doc


CHAPTERS_CSS = """
<style>
/* chapter-wise PYQ home in the app: one tidy row per subject, nothing else */
.tsa-cw{display:flex;align-items:center;gap:.5rem;flex-wrap:wrap;margin:.2rem 0 .8rem;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.86rem;color:#4A5568}
.tsa-cw b{background:linear-gradient(135deg,#059669,#10B981);color:#fff;border-radius:100px;padding:.16rem .6rem;font-size:.72rem;letter-spacing:.8px}
#subjects>h2{font-size:1.12rem!important;margin:0 0 .15rem!important}
.sub-grid{grid-template-columns:1fr!important;gap:.55rem!important}
.sub{flex-direction:row!important;align-items:center;gap:.75rem;padding:.7rem .8rem!important;border-top:1px solid #E2E8F0!important;border-left:5px solid var(--accent)!important;border-radius:14px!important;box-shadow:0 1px 6px rgba(0,0,0,.04)!important;transform:none!important}
.sub::after{display:none!important}
.sub-top{display:contents!important}
.sub-ic{width:42px!important;height:42px!important;border-radius:12px!important;font-size:1.3rem!important;order:1}
.sub-name{order:2;flex:1 1 auto;min-width:0;font-size:1rem!important;line-height:1.2!important}
.sub-name small{display:none!important}
.sub-stats{order:3;position:absolute!important;left:calc(.8rem + 42px + .75rem);bottom:.62rem;display:block!important;padding:0!important;margin:0!important;background:none!important;white-space:nowrap}
.sub-stat{display:inline!important}
.sub-stat b,.sub-stat span{display:inline!important;font-family:'Hind',sans-serif!important;font-weight:500!important;font-size:.76rem!important;letter-spacing:0!important;text-transform:none!important;color:#718096!important}
.sub-stat span{margin-left:.22em}
.sub-stat b{font-weight:700!important;color:var(--accent-dark)!important}
.sub-stat+.sub-stat::before{content:'\\00b7';color:#A0AEC0;margin:0 .35em}
.sub-name{padding-bottom:1.15rem}
@media(max-width:350px){.sub-stat b,.sub-stat span{font-size:.64rem!important}.sub-stat+.sub-stat::before{margin:0 .15em}.sub-stat span{margin-left:.15em}.sub-ic{width:38px!important;height:38px!important}.sub-stats{left:calc(.8rem + 38px + .75rem)}}
.sub-btn{order:4;flex:0 0 auto;width:30px;height:30px;padding:0!important;border-radius:50%!important;background:var(--accent-soft)!important;color:var(--accent-dark)!important;font-size:0!important;box-shadow:none!important;position:static!important}
.sub-btn em{font-size:1rem;font-weight:700;transform:none!important}
.sub-btn::after{content:'';position:absolute;inset:0;z-index:2}
</style>
"""


def cut_el(doc, pat, js, log, label, within=None):
    """Cut every element whose opening tag matches pat (a regex)."""
    rx = re.compile(pat)
    pos = 0
    while True:
        m = rx.search(doc, pos)
        if not m:
            return doc
        end = None if in_ranges(m.start(), raw_ranges(doc)) else element_end(doc, m.start())
        if end is None:
            pos = m.end()
            continue
        doc, pos = drop(doc, m.start(), end, js, log, label)


def trim_chapters(doc, js, log):
    """Chapter-wise PYQ home: keep the subject cards, cut the reading matter around them."""
    nums = dict((k.lower(), n) for n, k in re.findall(r'<span class="chip"><b>(\d+)</b>\s*([A-Za-z]+)</span>', doc))
    doc = cut_el(doc, r'<header\b[^>]*\bclass="hero"[^>]*>', js, log, 'header.hero')
    for sid in ('why', 'faq', 'more'):
        doc = cut_el(doc, r'<section\b[^>]*\bid="%s"[^>]*>' % sid, js, log, 'section#' + sid)
    doc = cut_el(doc, r'<div\b[^>]*\bclass="sub-ex"[^>]*>', js, log, 'div.sub-ex')
    doc = cut_el(doc, r'<p\b[^>]*\bclass="sub-desc"[^>]*>', js, log, 'p.sub-desc')
    m = re.search(r'(<section\b[^>]*\bid="subjects"[^>]*>\s*<h2>.*?</h2>)(.*?)(<div class="sub-grid")', doc, re.S)
    if m:
        bits = ['<b>100% FREE</b>']
        if nums.get('pyqs'):
            bits.append('{:,} PYQs'.format(int(nums['pyqs'])))
        if nums.get('chapters'):
            bits.append('%s chapters' % nums['chapters'])
        bits.append('English &amp; हिंदी')
        strip = '<div class="tsa-cw">%s</div>' % ' <span>·</span> '.join(bits).replace('</b> <span>·</span> ', '</b> ')
        doc = doc[:m.end(1)] + strip + '\n' + doc[m.start(3):]
        log.append('cut  subject intro and exam chips; add one summary line')
    return doc


def child_elements(doc, start):
    """(start, end, tag, attrs) of each child element of the element that opens at start."""
    m = TOKEN.match(doc, start)
    pos, out = m.end(), []
    while True:
        m = TOKEN.search(doc, pos)
        if not m:
            return out
        if m.group(3) is None:          # comment, script or style
            pos = m.end()
            continue
        if m.group(2):                  # the parent's closing tag
            return out
        tag = m.group(3).lower()
        if tag in VOID or m.group(4).rstrip().endswith('/'):
            pos = m.end()
            continue
        end = element_end(doc, m.start())
        if end is None:
            return out
        out.append((m.start(), end, tag, m.group(4)))
        pos = end


def keep_only_list(doc, js, log):
    """Subject-wise PYQ page: keep the list of tests (and the one-line rows), cut the article around it."""
    m = re.search(r'<div\b[^>]*\bid="pane-subj"[^>]*>', doc)
    if not m:
        return doc
    parent = parent_div_start(doc, m.start())
    if parent is None:
        return doc
    n = 0
    for start, end, tag, attrs in reversed(child_elements(doc, parent)):
        if 'id="pane-subj"' in attrs or 'tsa-row' in attrs:
            continue
        if safe_to_cut(doc[start:end], js):
            doc = doc[:start] + doc[end:]
        else:
            t = TOKEN.match(doc, start)
            doc = doc[:t.end() - 1] + ' data-tsa-hide>' + doc[t.end():]
        n += 1
    log.append('cut  %d blocks around the test list' % n)
    return doc


def cut_after_year_list(doc, js, log):
    """Tier 2 papers page: everything after the last year block is article text."""
    last = None
    for m in re.finditer(r'<details\b[^>]*\bclass="(?:[^"]*\s)?yr-acc(?:\s[^"]*)?"[^>]*>', doc):
        if not in_ranges(m.start(), raw_ranges(doc)):
            last = m
    if not last:
        return doc
    end = element_end(doc, last.start())
    parent = None
    depth_pos = last.start()
    # the parent is the nearest enclosing div
    parent = parent_div_start(doc, depth_pos)
    if end is None or parent is None:
        return doc
    n = 0
    for start, e, tag, attrs in reversed(child_elements(doc, parent)):
        if start < end:
            break
        if safe_to_cut(doc[start:e], js):
            doc = doc[:start] + doc[e:]
        else:
            t = TOKEN.match(doc, start)
            doc = doc[:t.end() - 1] + ' data-tsa-hide>' + doc[t.end():]
        n += 1
    log.append('cut  %d article blocks after the papers' % n)
    return doc


def pass_summary(note):
    """Reads the numbers out of the website's own pass note, so the app line can never disagree with it."""
    text = htmllib.unescape(re.sub(r'<[^>]+>', ' ', note))
    parts = []
    tiers = [int(n) for n in re.findall(r'(\d+)\s+Tier\s+I+\b', text)]
    total = re.search(r'\((\d+)\s*\u092e\u0949\u0915\)', text)            # "(80 मॉक)"
    whole = re.search(r'all\s+(\d+)\s+full-length', text)
    count = int(total.group(1)) if total else (sum(tiers) if tiers else (int(whole.group(1)) if whole else 0))
    if count:
        parts.append('%d mocks' % count)
    if re.search(r'Tier\s+II\b', text):
        parts.append('Tier I + Tier II')
    free = re.search(r'Mock\s+1\s*[\u2013-]\s*(\d+)', text)
    if free:
        parts.append('Mock 1\u2013%s free' % free.group(1))
    else:
        named = re.findall(r'Mock\s+(\d+)', text.split('free')[0]) if 'free' in text else []
        if named:
            parts.append('Mock 1\u2013%s free' % max(named, key=int))
    return ' \u00b7 '.join(parts)


def add_pass_summaries(doc, log):
    pat = re.compile(r'<div\b[^>]*\bclass="(?:[^"]*\s)?price-note(?:\s[^"]*)?"[^>]*>')
    pos = 0
    while True:
        m = pat.search(doc, pos)
        if not m:
            return doc
        pos = m.end()
        if in_ranges(m.start(), raw_ranges(doc)) or 'data-gdf="before"' in m.group(0):
            continue
        end = element_end(doc, m.start())
        if end is None:
            continue
        note = doc[m.start():end]
        line = pass_summary(note)
        if not line:
            continue
        # goes right after the headline <b>…</b> (inside .pn-sell where the page has one)
        anchor = re.search(r'<span class="pn-sell">\s*<b>.*?</b>|<span class="pn-txt">\s*<b>.*?</b>', note, re.S)
        if not anchor:
            continue
        at = m.start() + anchor.end()
        add = '<span class="pn-app">%s</span>' % htmllib.escape(line, quote=False)
        doc = doc[:at] + add + doc[at:]
        pos = at + len(add)
        log.append('pass line: ' + line)


# Option blocks that open as a bottom sheet in the app: (class, row label, sheet title).
# On the website they are a grid of links in the page; in the app they are one row,
# and tapping it lists the same links in a popup.
SHEETS = [
    ('smr-box', '\U0001F9E9 Subject-wise mock tests', 'Subject-wise mock tests'),
    ('subj-links', '\U0001F9E9 Subject-wise mock tests', 'Subject-wise mock tests'),
    ('subj-pyq-links', '\U0001F9EE Subject-wise previous year questions', 'Subject-wise previous year questions'),
    ('pqc-wrap', '\U0001F5C2\uFE0F Chapter-wise and section-wise PYQs', 'Practise previous year questions', 'By chapter, or one section of a paper'),
]
CHEVRON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" '
           'stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>')


def collapse_to_sheets(doc, log, by_subject=False):
    sheets = []
    for entry in SHEETS:
        cls, label, title = entry[:3]
        if by_subject and cls == 'subj-links':
            label, title = '\U0001F9E9 Other subjects', 'Other subjects'
        if cls.startswith('#'):
            pat = re.compile(r'<div\b[^>]*\bid="%s"[^>]*>' % re.escape(cls[1:]))
        else:
            pat = re.compile(r'<div\b[^>]*\bclass="(?:[^"]*\s)?%s(?:\s[^"]*)?"[^>]*>' % re.escape(cls))
        m = pat.search(doc)
        while m and in_ranges(m.start(), raw_ranges(doc)):
            m = pat.search(doc, m.end())
        if not m:
            continue
        start, end = m.start(), element_end(doc, m.start())
        if end is None:
            continue
        block = doc[start:end]
        # the small heading the website prints just above the grid becomes the row itself
        head = re.search(r'<div\b[^>]*style="font-family:\'Rajdhani\',sans-serif;font-w[^"]*"[^>]*>(?:(?!<div\b).)*?</div>\s*$', doc[:start], re.S)
        if head and len(head.group(0)) < 600:
            start = head.start()
        n = len(sheets) + 1
        names = [htmllib.unescape(re.sub(r'<[^>]+>', ' ', a)).replace('\u2192', '') for a in re.findall(r'<a\b[^>]*>(.*?)</a>', block, re.S)]
        names = [re.sub(r'\s+', ' ', re.sub(r'\(.*?\)|NEW|\d+ Qs.*$|Mock Tests?|Previous Year Questions|[^\w\s&]', ' ', x)).strip() for x in names]
        short = [re.sub(r'^(?:CHSL|CGL|GD|MTS|NTPC|SSC|Tier 2|Tier II)\s+', '', x).strip() for x in names]
        short = [re.sub(r'^(?:Tier 2|Tier II)\s+', '', x).strip() for x in short if x]
        sub = entry[3] if len(entry) > 3 else ' \u00b7 '.join(short[:5])
        row = ('<button type="button" class="tsa-row" data-tsa-sheet="tsaSheet%d"><span class="tsa-row-t">%s'
               '<small>%s</small></span>%s</button>' % (n, label, htmllib.escape(sub, quote=False), CHEVRON))
        doc = doc[:start] + row + doc[end:]
        sheets.append('<div class="tsa-sheet" id="tsaSheet%d" data-tsa-close><div class="tsa-sheet-card">'
                      '<div class="tsa-sheet-h"><b>%s</b><button type="button" data-tsa-close aria-label="Close">\u2715</button></div>%s</div></div>'
                      % (n, title, block))
        log.append('sheet: %s (%d options)' % (cls, len(names)))
    if sheets:
        body_end = doc.lower().rfind('</body>')
        doc = doc[:body_end] + '\n' + '\n'.join(sheets) + SHEET_JS + doc[body_end:]
    return doc


SHEET_JS = """
<script>
/* TSSC-APPPAGES-V1: one-line rows that open their options as a bottom sheet */
(function(){
  function closeAll(){ var o=document.querySelectorAll('.tsa-sheet.open'); for(var i=0;i<o.length;i++) o[i].classList.remove('open'); }
  document.addEventListener('click',function(e){
    var t=e.target, r=t.closest?t.closest('[data-tsa-sheet]'):null;
    if(r){ var s=document.getElementById(r.getAttribute('data-tsa-sheet')); if(s){ closeAll(); s.classList.add('open'); } return; }
    if(t.classList&&t.classList.contains('tsa-sheet')){ closeAll(); return; }          /* tap outside the card */
    var c=t.closest?t.closest('button[data-tsa-close]'):null; if(c) closeAll();
  });
  window.addEventListener('pageshow',closeAll);                                         /* coming back from a subject page */
})();
</script>
"""


def short_title(doc):
    m = re.search(r'<title>(.*?)</title>', doc, re.S)
    t = htmllib.unescape(m.group(1)).strip() if m else 'TrickySSC'
    t = re.sub(r'\s*[|–—-]\s*TrickySSC.*$', '', t, flags=re.I)
    t = re.split(r'\s[–—|]\s|:\s|\s-\s', t)[0]
    t = re.sub(r'\s+(Free\b.*|in Hindi\b.*|with Solutions?\b.*)$', '', t, flags=re.I).strip()
    return t or 'TrickySSC'


def clean_head(doc, title, log):
    head_end = doc.lower().find('</head>')
    head, rest = doc[:head_end], doc[head_end:]
    before = len(head)
    head = re.sub(r'<script\b[^>]*type="application/ld\+json"[^>]*>.*?</script>\s*', '', head, flags=re.S)
    head = re.sub(r'<meta\b[^>]*\b(?:name|property)="(?:description|keywords|robots|googlebot|author|og:[^"]*|twitter:[^"]*)"[^>]*>\s*', '', head)
    head = re.sub(r'<link\b[^>]*\brel="(?:canonical|alternate)"[^>]*>\s*', '', head)
    head = re.sub(r'<title>.*?</title>', '<title>%s</title>' % htmllib.escape(title, quote=False), head, count=1, flags=re.S)
    head = re.sub(r'<meta\b[^>]*\bname="viewport"[^>]*>',
                  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">', head, count=1)
    log.append('head trimmed by %d bytes' % (before - len(head)))
    # JSON-LD that sits in the body is search markup too
    rest = re.sub(r'<script\b[^>]*type="application/ld\+json"[^>]*>.*?</script>\s*', '', rest, flags=re.S)
    return head + rest


CHROME_CSS = """
<!-- TSSC-APPPAGES-V1: app-only copy, built by build_app_pages.py from %(src)s. Do not edit by hand. -->
<meta name="robots" content="noindex">
<meta name="theme-color" content="#FFFFFF">
<link rel="manifest" href="/manifest.webmanifest">
<script>window.__tsscApp=1;try{sessionStorage.setItem('tssc_app','1');}catch(e){}</script>
<style id="tssc-app-css">
html{-webkit-tap-highlight-color:transparent;}
nav.tssc-nav,nav.topbar,nav.nav,nav.site-nav,header.nav,.mobile-menu,.tssc-mobile-menu,footer,[data-tsa-hide]{display:none!important;}
body{padding-bottom:calc(58px + env(safe-area-inset-bottom,0px))!important;}
.wrap{padding-top:12px!important;}
/* no empty band under the app bar, and no bare website links */
[data-tg-join]{display:none!important;}
nav.topbar+div{padding-top:0!important;}
nav.topbar+div>div{padding-top:10px!important;}
.tgf{bottom:calc(72px + env(safe-area-inset-bottom,0px))!important;}
/* info boxes: the headline only. The long explanation stays on the website page. */
.price-note{padding:10px 12px!important;margin:10px 0!important;align-items:center!important;}
.price-note .pn-txt{font-size:0!important;line-height:1.3!important;}
.price-note .pn-txt br{display:none!important;}
.price-note .pn-txt>b:first-child,.price-note .pn-sell>b:first-child,.price-note .pn-own>b:first-child{font-size:13.5px!important;display:block;}
.price-note .pn-app{display:block;font-size:12.5px!important;font-weight:600;margin-top:2px;opacity:.9;}
.rb-txt{font-size:0!important;line-height:1.3!important;}
.rb-txt>b:first-child{font-size:13.5px!important;}
.smr-box .smr-sub{display:none!important;}
/* one-line rows, and the bottom sheet their options open in */
.tsa-row{display:flex;align-items:center;gap:10px;width:100%%;min-height:56px;margin:10px 0;padding:10px 12px 10px 14px;border-radius:14px;border:1.5px solid #E2E8F0;background:#fff;text-align:left;cursor:pointer;font-family:'Rajdhani',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;font-weight:700;font-size:16.5px;line-height:1.2;color:#1A202C;box-shadow:0 2px 6px rgba(15,23,42,.04);}
.tsa-row:active{background:#FFF7F0;border-color:#FF6B00;}
.tsa-row-t{flex:1;min-width:0;}
.tsa-row small{display:block;margin-top:2px;font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;font-size:12px;font-weight:600;color:#64748B;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.tsa-row svg{flex:0 0 20px;width:20px;height:20px;color:#FF6B00;}
.tsa-sheet{display:none;position:fixed;inset:0;z-index:9990;background:rgba(15,23,42,.55);align-items:flex-end;justify-content:center;}
.tsa-sheet.open{display:flex;}
.tsa-sheet-card{width:100%%;max-width:560px;max-height:82vh;overflow-y:auto;background:#fff;border-radius:20px 20px 0 0;padding:6px 14px calc(18px + env(safe-area-inset-bottom,0px));box-shadow:0 -10px 30px rgba(0,0,0,.2);animation:tsaUp .18s ease-out;}
@keyframes tsaUp{from{transform:translateY(24px);opacity:.6;}to{transform:none;opacity:1;}}
.tsa-sheet-h{display:flex;align-items:center;gap:10px;padding:12px 2px 10px;position:sticky;top:0;background:#fff;z-index:1;}
.tsa-sheet-h b{flex:1;font-family:'Rajdhani',system-ui,sans-serif;font-weight:700;font-size:19px;color:#1A202C;}
.tsa-sheet-h button{width:36px;height:36px;border-radius:50%%;border:0;background:#F1F5F9;color:#475569;font-size:15px;cursor:pointer;}
.tsa-sheet .smr-box{border:0!important;box-shadow:none!important;padding:0!important;margin:0!important;background:none!important;}
.tsa-sheet .smr-head{display:none!important;}
.tsa-sheet .subj-links,.tsa-sheet .subj-pyq-links,.tsa-sheet .pqc-wrap,.tsa-sheet #tsscPC{margin:0!important;}
.tsa-sheet .pqc-wrap>*:first-child,.tsa-sheet #tsscPC>*:first-child{margin-top:0!important;}
.yr-intro{display:none!important;}
.yr-adding span{font-size:0!important;}
.yr-adding b{font-size:12.5px!important;}
.tsa-top{position:sticky;top:0;left:0;right:0;z-index:1000;display:flex;align-items:center;gap:4px;box-sizing:border-box;height:calc(52px + env(safe-area-inset-top,0px));padding:env(safe-area-inset-top,0px) 6px 0;background:#fff;border-bottom:1px solid #EDF0F5;box-shadow:0 1px 6px rgba(15,23,42,.05);font-family:'Rajdhani',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;color:#1A202C;}
.tsa-top a,.tsa-top button{flex:0 0 40px;width:40px;height:40px;border-radius:50%%;border:0;background:none;display:flex;align-items:center;justify-content:center;color:#1A202C;cursor:pointer;padding:0;margin:0;text-decoration:none;}
.tsa-top a svg,.tsa-top button svg{width:22px;height:22px;flex:0 0 22px;}
.tsa-top a:active,.tsa-top button:active{background:#F1F5F9;}
.tsa-top b{flex:1;min-width:0;font-weight:700;font-size:19px;line-height:1.1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.tsa-tabs{position:fixed;left:0;right:0;bottom:0;z-index:980;display:grid;grid-template-columns:repeat(5,1fr);box-sizing:border-box;height:calc(58px + env(safe-area-inset-bottom,0px));padding:0 0 env(safe-area-inset-bottom,0px);margin:0;background:#fff;border-top:1px solid #EDF0F5;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;}
.tsa-tabs a{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;font-size:10.5px;font-weight:700;line-height:1.2;color:#94A3B8;text-decoration:none;}
.tsa-tabs a svg{width:23px;height:23px;}
.tsa-tabs a.on{color:#FF6B00;}
.tsa-tabs a.on::before{content:"";position:absolute;top:0;left:50%%;width:26px;height:3px;margin-left:-13px;border-radius:0 0 4px 4px;background:#FF6B00;}
.tsa-tabs a.on svg{fill:rgba(255,107,0,.14);}
.tsa-tabs a:active{transform:scale(.94);}
</style>
"""

# Mock pages only. The website's own unlock popup does all the selling (plans, combos, "already
# owned" checks, Razorpay, the payment server). In the app it is shown as a bottom sheet, gets a
# payment summary, and opens by itself when the student arrives from the app's Buy Now button:
#     app-<page>.html?buy=1            the page's normal plan
#     app-<page>.html?buy=<productId>  that plan preselected
#     app-<page>.html?pass=all         the All Mocks Pass (already handled by the page itself)
CHECKOUT = """
<style id="tssc-app-pay-css">
#mockBuyPop{padding:0!important;align-items:flex-end!important;backdrop-filter:none!important;}
#mockBuyPop .mbp-card{width:100%!important;max-width:none!important;margin:0!important;border-radius:20px 20px 0 0!important;max-height:94vh;overflow-y:auto!important;}
#mockBuyPop .mbp-head{background:linear-gradient(135deg,#FF6B00,#FF9A3D)!important;padding:1rem 1.2rem!important;}
#mockBuyPop .mbp-body{padding:1rem 1.2rem calc(1.2rem + env(safe-area-inset-bottom,0px))!important;}
#mockBuyPop .mbp-go{min-height:50px;font-size:1rem!important;}
.tsa-sum{border:1px solid #EDF0F5;border-radius:14px;padding:4px 14px;margin:4px 0 14px;background:#FAFBFC;font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;}
.tsa-sum h4{font-family:'Rajdhani',system-ui,sans-serif;font-size:15px;font-weight:700;color:#1A202C;margin:10px 0 2px;}
.tsa-sum div{display:flex;justify-content:space-between;gap:12px;padding:8px 0;font-size:14px;color:#475569;border-bottom:1px dashed #E2E8F0;}
.tsa-sum div:last-child{border-bottom:0;font-weight:800;font-size:16px;color:#1A202C;}
.tsa-sum .g{color:#047857;font-weight:700;}
</style>
<script>
/* TSSC-APPPAGES-V1: display only. The amount charged is always decided by the payment server. */
(function(){
  function $(i){return document.getElementById(i);}
  function paint(){
    var sel=$('mbpCourse'), P=window.TSSC_PRICING;
    if(!sel||!sel.value||!P||!P.load) return;
    P.load().then(function(cat){
      var p=P.product(cat,sel.value); if(!p) return;
      var box=$('tsaSum');
      if(!box){ box=document.createElement('div'); box.id='tsaSum'; box.className='tsa-sum';
        var err=$('mbpErr'); if(!err||!err.parentNode) return; err.parentNode.insertBefore(box,err); }
      var r='\\u20b9', off=(p.mrp&&p.mrp>p.price)?(p.mrp-p.price):0;
      box.innerHTML='<h4>Payment summary</h4>'
        +'<div><span>'+String(p.label||'Premium pass').replace(/[<>&]/g,'')+'</span><span>'+r+(off?p.mrp:p.price)+'</span></div>'
        +(off?'<div><span>Discount</span><span class="g">\\u2212 '+r+off+'</span></div>':'')
        +'<div><span>Valid for</span><span>'+(p.durationDays>=365?Math.round(p.durationDays/365)+' year':p.durationDays+' days')+'</span></div>'
        +'<div><span>Amount to pay</span><span>'+r+p.price+'</span></div>';
    }).catch(function(){});
  }
  function watch(){
    var sel=$('mbpCourse'); if(!sel) return;
    sel.addEventListener('change',paint);
    try{ new MutationObserver(paint).observe(sel,{childList:true}); }catch(e){}
    paint();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',watch); else watch();

  var m=/[?&]buy=([^&#]*)/.exec(location.search);
  if(m){
    var want=decodeURIComponent(m[1]||''), tries=0;
    var t=setInterval(function(){
      if(++tries>80){ clearInterval(t); return; }                 /* give up after 20 s */
      if(typeof window.tsscOpenBuy!=='function') return;
      clearInterval(t);
      Promise.resolve(window.tsscOpenBuy(null)).then(function(){
        var sel=$('mbpCourse');
        if(sel && want && want!=='1'){
          for(var i=0;i<sel.options.length;i++) if(sel.options[i].value===want){ sel.value=want; sel.dispatchEvent(new Event('change',{bubbles:true})); break; }
        }
      }).catch(function(){});
    },250);
  }
})();
</script>
"""

LOGIN_CSS = """
<style id="tssc-app-login-css">
body{padding-bottom:0!important;display:block!important;background:#FFF8F2!important;min-height:100vh;}
.right-panel{display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;width:100%!important;max-width:460px;min-height:0!important;margin:0 auto!important;padding:calc(env(safe-area-inset-top,0px) + 18px) 16px 24px!important;}
.login-card{width:100%!important;max-width:none!important;margin:0!important;}
.tsa-brand{display:flex;align-items:center;justify-content:center;gap:10px;margin:18px 0 20px;font-family:'Baloo 2',system-ui,sans-serif;font-weight:800;font-size:30px;letter-spacing:-.5px;color:#1A202C;}
.tsa-brand i{width:46px;height:46px;border-radius:50%;background:linear-gradient(135deg,#FF6B00,#FF9A3D);display:flex;align-items:center;justify-content:center;font-style:normal;font-size:22px;box-shadow:0 6px 16px rgba(255,107,0,.35);}
.tsa-brand b{color:#FF6B00;}
.tsa-tag{text-align:center;color:#64748B;font-size:14px;margin:-12px 0 18px;font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;}
</style>
"""
LOGIN_BRAND = ('\n<div class="tsa-brand"><i>\u26a1</i><span>Tricky<b>SSC</b></span></div>'
               '<div class="tsa-tag">Mock tests &middot; Previous year papers &middot; Hindi &amp; English</div>\n')

SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">%s</svg>'
ICON = {
    'back': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>',
    'home': SVG % '<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/>',
    'mocks': SVG % '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    'pyq': SVG % '<path d="M14 3H6v18h12V7z"/><path d="M14 3v4h4"/><path d="M9 13h6M9 17h6"/>',
    'chapters': SVG % '<path d="M4 5h7v14H4zM13 5h7v14h-7z"/>',
    'me': SVG % '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
}
TABS = [('home', 'Home', '/app.html'), ('mocks', 'Mocks', '/app.html#mocks'), ('pyq', 'PYQs', '/app.html#pyq'),
        ('chapters', 'Chapters', '/app.html#chapters'), ('me', 'Me', '/app.html#me')]


def top_bar(title):
    return ('\n<div class="tsa-top"><button type="button" aria-label="Back" '
            "onclick=\"if(history.length>1)history.back();else location.href='/app.html';\">%s</button>"
            '<b>%s</b><a href="/app.html" aria-label="Home">%s</a></div>\n'
            % (ICON['back'], htmllib.escape(title, quote=False), ICON['home']))


def tab_bar(active):
    links = ''.join('<a href="%s"%s>%s%s</a>' % (href, ' class="on"' if key == active else '', ICON[key], label)
                    for key, label, href in TABS)
    return '\n<div class="tsa-tabs">%s</div>\n' % links


def build(src_name, tab):
    with open(os.path.join(ROOT, src_name), encoding='utf-8') as fh:
        doc = fh.read()
    log = []
    title = short_title(doc)
    js = scripts_text(doc)

    doc = clean_head(doc, title, log)
    for tag, cls in CUT_BY_CLASS:
        doc = cut_by_class(doc, tag, cls, js, log)
    doc = cut_mock_heading(doc, js, log)
    doc = add_pass_summaries(doc, log)
    by_subject = src_name.endswith('-previous-year-questions.html')
    if tab in ('mocks', 'pyq'):
        doc = collapse_to_sheets(doc, log, by_subject)
    if tab == 'pyq':
        doc = trim_pyq(doc, js, log)
        if by_subject:
            doc = keep_only_list(doc, js, log)
        if src_name == 'ssc-cgl-tier-2-pyq.html':
            doc = cut_after_year_list(doc, js, log)
    if tab == 'chapters':
        doc = trim_chapters(doc, js, log)

    head_end = doc.lower().find('</head>')
    extra = {'mocks': CHECKOUT, 'login': LOGIN_CSS, 'chapters': CHAPTERS_CSS}.get(tab, '')
    doc = doc[:head_end] + (CHROME_CSS % {'src': src_name}) + extra + doc[head_end:]
    if tab == 'login':
        # no bars on the sign-in screen: just the brand above the website's own sign-in card
        panel = re.search(r'<div\b[^>]*\bclass="(?:[^"]*\s)?right-panel(?:\s[^"]*)?"[^>]*>', doc)
        at = panel.end() if panel else re.search(r'<body\b[^>]*>', doc).end()
        return doc[:at] + LOGIN_BRAND + doc[at:], log
    body = re.search(r'<body\b[^>]*>', doc)
    doc = doc[:body.end()] + top_bar(title) + doc[body.end():]
    body_end = doc.lower().rfind('</body>')
    doc = doc[:body_end] + tab_bar(tab) + doc[body_end:]
    return doc, log


def main():
    check = '--check' in sys.argv
    stale = 0
    for src, tab in PAGES.items():
        if not os.path.exists(os.path.join(ROOT, src)):
            print('skip  %s (not in the repo)' % src)
            continue
        out_name = 'app-' + src
        doc, log = build(src, tab)
        out_path = os.path.join(ROOT, out_name)
        old = None
        if os.path.exists(out_path):
            with open(out_path, encoding='utf-8') as fh:
                old = fh.read()
        src_size = os.path.getsize(os.path.join(ROOT, src))
        state = 'same ' if old == doc else 'built'
        print('%s %-40s %7d -> %7d bytes' % (state, out_name, src_size, len(doc.encode('utf-8'))))
        if '-v' in sys.argv:
            for line in log:
                print('        ' + line)
        if old != doc:
            stale += 1
            if not check:
                with open(out_path, 'w', encoding='utf-8', newline='') as fh:
                    fh.write(doc)
    if check and stale:
        sys.exit(1)


if __name__ == '__main__':
    main()
