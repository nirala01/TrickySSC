#!/usr/bin/env python3
"""Builds assets/pyq_chapters.json: the chapter of every previous-year question, from the website's
chapter-wise PYQ lists (pyq-chapters/all/*.json). The app uses it for chapter analysis.

Run by .github/workflows/build-flutter.yml (never by hand):
    pyq_chapter_map.py <repo root> <output json>
Output: {"ch": [chapter ids], "n": [their names], "p": {"<paper id without _en/_hi>": [chapter index per question number, -1 = none]}}
"""
import glob
import json
import os
import re
import sys

root, out = sys.argv[1], sys.argv[2]
chs, names, papers = [], {}, {}
for f in sorted(glob.glob(os.path.join(root, 'pyq-chapters', 'all', '*.json'))):
    try:
        d = json.load(open(f, encoding='utf-8'))
    except Exception as e:
        print('::warning::skipped', f, e)
        continue
    cid = d.get('chapter') or os.path.basename(f)[:-5]
    if cid not in chs:
        chs.append(cid)
    ci = chs.index(cid)
    names[cid] = (d.get('name') or '').strip()
    for st in d.get('sets') or []:
        for q in st.get('qs') or []:
            m = re.match(r'^(.*)_(?:en|hi)_q(\d+)$', q.get('en') or q.get('hi') or '')
            if not m:
                continue
            n = int(m.group(2))
            if n < 1 or n > 400:
                continue
            row = papers.setdefault(m.group(1), [])
            if len(row) < n:
                row.extend([-1] * (n - len(row)))
            row[n - 1] = ci
if not papers and os.path.exists(out):
    print('::warning::No chapter-wise PYQ lists found; keeping the bundled file.')
    sys.exit(0)
json.dump({'ch': chs, 'n': [names.get(c, '') for c in chs], 'p': papers}, open(out, 'w', encoding='utf-8'), separators=(',', ':'))
print('pyq_chapters.json: %d chapters, %d papers, %d questions' % (len(chs), len(papers), sum(1 for r in papers.values() for v in r if v >= 0)))
