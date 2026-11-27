#!/usr/bin/env python3
"""TSSC-PYQCOUNTS-V1 (2026-11-27) — writes /pyq-counts.json: papers, questions and years of every
PYQ series, counted from the paper lists that the PYQ page builds have already baked into the
PYQ pages. It reads only files of this repo: NO Firestore reads, no network.

Every "Build ... PYQ page" workflow runs it right after baking its page, so the numbers on the
home page cards, the app home and the exam hubs always equal the papers listed on the PYQ page.

    python scripts/build_pyq_counts.py            # rewrite pyq-counts.json
    python scripts/build_pyq_counts.py --check    # print only
"""
import collections, datetime, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'pyq-counts.json')

# exam key -> (name, pages that list its papers, questions per paper when a row does not say)
SERIES = [
    ('ssc-cgl',     'SSC CGL',            ['ssc-cgl-pyq.html', 'ssc-cgl-tier-2-pyq.html'], 100),
    ('ssc-chsl',    'SSC CHSL',           ['ssc-chsl-pyq.html'], 100),
    ('ssc-gd',      'SSC GD',             ['ssc-gd-pyq.html'], 80),
    ('ssc-mts',     'SSC MTS',            ['ssc-mts.html'], 90),
    ('rrb-ntpc',    'RRB NTPC',           ['rrb-ntpc-pyq.html'], 100),
    ('rrb-ntpc-ug', 'RRB NTPC UG',        ['rrb-ntpc-ug-pyq.html'], 100),
    ('rrb-sm',      'RRB Station Master', ['rrb-station-master-pyq.html'], 100),
]
PID = re.compile(r'paperId=([A-Za-z0-9._-]+?)_en(?=["&\'])')
QS = re.compile(r'(\d{2,3})\s*Qs\b')
TAGS = re.compile(r'<script\b.*?</script>|<style\b.*?</style>', re.S | re.I)


def papers_of(exam, pages, default_q):
    """{paperId: questions} for one exam, from the baked rows (a row = "NN Qs" ... Attempt link)."""
    found = {}
    for page in pages:
        path = os.path.join(ROOT, page)
        if not os.path.exists(path):
            continue
        html = TAGS.sub('', open(path, encoding='utf-8').read())
        prev = 0
        for m in PID.finditer(html):
            pid = m.group(1).lower()
            if not pid.startswith(exam + '_') or pid in found:
                prev = m.end() if pid in found else prev
                continue
            qs = QS.findall(html[max(prev, m.start() - 2500):m.start()])
            found[pid] = int(qs[-1]) if qs else default_q
            prev = m.end()
    return found


def build():
    exams = collections.OrderedDict()
    for exam, name, pages, dq in SERIES:
        p = papers_of(exam, pages, dq)
        if not p:
            continue
        years = sorted({m.group(1) for m in (re.match(r'[a-z-]+_(\d{4})_', k) for k in p) if m})
        by_year = collections.OrderedDict((y, sum(1 for k in p if ('_' + y + '_') in k)) for y in years)
        exams[exam] = collections.OrderedDict(name=name, papers=len(p), questions=sum(p.values()), years=years, byYear=by_year)
    return exams


def dump(exams, built):
    # one exam per line with empty lines between them: two PYQ builds that finish together
    # change different lines, so their commits rebase without a conflict
    rows = [json.dumps(k) + ': ' + json.dumps(v, ensure_ascii=False, separators=(',', ':')) for k, v in exams.items()]
    return '{\n"exams": {\n\n\n' + ',\n\n\n'.join(rows) + '\n\n\n},\n\n\n"built": ' + json.dumps(built) + '\n}\n'


def main():
    exams = build()
    old = {}
    try:
        old = json.load(open(OUT, encoding='utf-8'))
    except Exception:
        pass
    for k, v in exams.items():   # "since" = the day this exam's numbers last changed
        o = (old.get('exams') or {}).get(k) or {}
        same = all(o.get(f) == v[f] for f in ('papers', 'questions', 'years'))
        v['since'] = o.get('since') if (same and o.get('since')) else datetime.date.today().isoformat()
    built = max([v['since'] for v in exams.values()] or [datetime.date.today().isoformat()])
    for k, v in exams.items():
        print('%-12s %4d papers %6d questions  %s' % (k, v['papers'], v['questions'], dict(v['byYear'])))
    if '--check' in sys.argv:
        return
    text = dump(exams, built)
    json.loads(text)
    if not exams:
        sys.exit('no papers found on any PYQ page; pyq-counts.json left as it is')
    open(OUT, 'w', encoding='utf-8').write(text)


if __name__ == '__main__':
    main()
