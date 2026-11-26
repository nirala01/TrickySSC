"""Self-check for a questions-EN.txt. usage: check_txt.py <txt> <data.py> [--quiet]
Returns non-zero on any failure."""
import sys, re, json, os, importlib.util, collections
sys.path.insert(0, os.path.dirname(__file__))
from base import parse_txt, SUBJECT, DEVA


def check(txt, datapy):
    errs = []
    try:
        hdr, Q = parse_txt(txt)
    except Exception as e:
        return [f'parse: {e}']
    spec = importlib.util.spec_from_file_location('d', datapy); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
    from srckey import keys
    SK = keys(D.META['src']); SK.update(getattr(D, 'KEY_FIX', {}))
    if sorted(Q) != list(range(1, 91)): errs.append(f'blocks {sorted(Q)[:3]}..{len(Q)}')
    if hdr.get('EXAM') != 'ssc-mts' or hdr.get('YEAR') != str(D.META['year']) or hdr.get('LANG') != 'EN': errs.append(f'header {hdr}')
    raw = open(txt, encoding='utf-8').read()
    order = [int(x) for x in re.findall(r'^\[Q(\d+)\]$', raw, re.M)]
    if order != list(range(1, 91)): errs.append('block order')
    for n, d in Q.items():
        for f in ('SUBJECT', 'CONCEPT', 'TEXT', 'A', 'B', 'C', 'D', 'ANSWER'):
            if f not in d: errs.append(f'Q{n} missing {f}')
        if d.get('SUBJECT') != SUBJECT.get(n): errs.append(f'Q{n} subject {d.get("SUBJECT")}')
        if d.get('ANSWER') not in ('A', 'B', 'C', 'D'): errs.append(f'Q{n} answer')
        if d.get('ANSWER') != SK[n]: errs.append(f'Q{n} key differs from source key')
        cells = [d.get('TEXT', '')] + [d.get(L, '') for L in 'ABCD']
        for L in 'ABCD':
            if not d.get(L, '').strip(): errs.append(f'Q{n} blank option {L}')
        stem_body = re.sub(r'^\[FIGURE-BASED\]\s*', '', d.get('TEXT', ''))
        if len(re.sub(r'\\\(.*?\\\)', 'x', stem_body).split()) < 3: errs.append(f'Q{n} stem too short')
        for c in cells:
            s = re.sub(r'\\\(.*?\\\)', 'KTX', c)
            if re.search(r'\s:', s) and not re.search(r'(Statements|Conclusions|Directions|Credit|PASSAGE \(Q\d+–Q\d+\)):', s.replace(' :', ':')):
                errs.append(f'Q{n} B1 padded colon: {c[:60]}')
            if c.count('\\(') != c.count('\\)'): errs.append(f'Q{n} unbalanced KaTeX')
            if re.search(r'(?<![\\A-Za-z])(frac|dfrac|sqrt|times|text)\{', c): errs.append(f'Q{n} bare command')
            if re.search(r'\\u[0-9a-fA-F]{4}', c) or '\t' in c: errs.append(f'Q{n} literal escape/tab')
            if DEVA.search(c): errs.append(f'Q{n} Devanagari')
            s2 = re.sub(r'</?u>', '', c)
            if re.search(r'<(?!/?u>)|(?<!u)>', re.sub(r'</?u>', '', c)) and '&lt;' not in c:
                if re.search(r'[<>]', s2): errs.append(f'Q{n} raw < or >')
        if d.get('TEXT', '').count('||') > 1: errs.append(f'Q{n} more than one ||')
        if re.search(r'contains? a[n]?\b[^|]*error', d.get('TEXT', '').split('||')[0]) and '<u>' in d.get('TEXT', ''):
            errs.append(f'Q{n} <u> in error-spotting')
        opts = [d.get(L) for L in 'ABCD']
        if len(set(opts)) < 4 and n not in getattr(D, 'DUP_OK', ()): errs.append(f'Q{n} duplicate options')
        isfig = d.get('TEXT', '').startswith('[FIGURE-BASED]')
        if isfig != (n in D.FIG): errs.append(f'Q{n} figure flag mismatch')
        if n in D.FIG:
            figopts = opts == [f'(figure {i})' for i in range(1, 5)]
            if figopts != (D.FIG[n] in ('both', 'opts')): errs.append(f'Q{n} figure options mismatch')
    # boundaries
    for a, b in ((20, 21), (40, 41), (65, 66)):
        if Q.get(a, {}).get('SUBJECT') == Q.get(b, {}).get('SUBJECT'): errs.append(f'boundary {a}/{b}')
    # passages
    ps = collections.defaultdict(set)
    for n, d in Q.items():
        m = re.match(r'^PASSAGE \(Q(\d+)–Q(\d+)\): (.*?) \|\| ', d.get('TEXT', ''))
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if not (a <= n <= b) or a < 66: errs.append(f'Q{n} passage range')
            ps[(a, b)].add(m.group(3))
    for k, v in ps.items():
        if len(v) != 1: errs.append(f'passage {k} copies differ')
        cnt = sum(1 for d in Q.values() if d.get('TEXT', '').startswith(f'PASSAGE (Q{k[0]}–Q{k[1]})'))
        if cnt != k[1] - k[0] + 1: errs.append(f'passage {k} count {cnt}')
    return errs


if __name__ == '__main__':
    errs = check(*sys.argv[1:3])
    if '--quiet' not in sys.argv:
        hdr, Q = parse_txt(sys.argv[1])
        print('answer distribution', dict(sorted(collections.Counter(d['ANSWER'] for d in Q.values()).items())))
    print('FAIL' if errs else 'PASS', *errs[:40], sep='\n  ')
    sys.exit(1 if errs else 0)
