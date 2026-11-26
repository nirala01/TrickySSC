"""Row-level negative controls for the CSV checker. usage: controls.py <paperdir>"""
import sys, os, re, csv, shutil, tempfile, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
import checks
from base import QHDR, SHDR, VERDICT_RE

pdir = sys.argv[1]
spec = importlib.util.spec_from_file_location('d', os.path.join(pdir, 'data.py')); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
P = D.META['prefix']; SRC = os.path.join(pdir, 'out')
FILES = ['questions-EN', 'questions-HI', 'solutions-EN', 'solutions-HI']


def load(d, k):
    with open(os.path.join(d, f'{P}-{k}.csv'), encoding='utf-8-sig', newline='') as fh:
        r = list(csv.reader(fh))
    return r[0], r[1:]


def save(d, k, h, rows, bom=True):
    with open(os.path.join(d, f'{P}-{k}.csv'), 'w', encoding='utf-8-sig' if bom else 'utf-8', newline='') as fh:
        w = csv.writer(fh); w.writerow(h); w.writerows(rows)


def find(rows, h, col, pred):
    ci = h.index(col)
    for i, r in enumerate(rows):
        if pred(int(r[0]), r[ci]): return i
    raise AssertionError(f'no anchor for {col}')


results = []


def control(name, edits):
    tmp = tempfile.mkdtemp()
    for k in FILES: shutil.copy(os.path.join(SRC, f'{P}-{k}.csv'), tmp)
    changed = False
    try:
        for k, fn in edits:
            h, rows = load(tmp, k)
            before = [list(r) for r in rows], list(h)
            out = fn(h, rows)
            if out == 'NOBOM':
                save(tmp, k, h, rows, bom=False); changed = True; continue
            if out is not None: h, rows = out
            if ([list(r) for r in rows], list(h)) != before: changed = True
            save(tmp, k, h, rows)
        e, _ = checks.run(pdir, tmp)
        results.append((name, changed, bool(e)))
    except Exception as ex:
        results.append((name, changed, True if changed else False, f'exc {ex}'))
    shutil.rmtree(tmp)


def cell(n, col, fn):
    def _f(h, rows):
        i = find(rows, h, col, lambda q, v: q == n); ci = h.index(col); rows[i][ci] = fn(rows[i][ci])
    return _f


def cellp(col, pred, fn):
    def _f(h, rows):
        i = find(rows, h, col, pred); ci = h.index(col); rows[i][ci] = fn(rows[i][ci])
    return _f


flipk = lambda v: {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'A'}[v]
control('question text drift', [('questions-EN', cell(5, 'text', lambda v: v + ' extra'))])
control('option text altered', [('questions-EN', cell(7, 'option_B', lambda v: v + '1'))])
control('EN key flip', [('questions-EN', cell(3, 'correct', flipk))])
control('HI key flip only (Q1-65)', [('questions-HI', cell(10, 'correct', flipk))])
control('HI key flip in Q66-90', [('questions-HI', cell(70, 'correct', flipk))])
control('wrong subject', [('questions-EN', cell(25, 'subject', lambda v: 'General Awareness'))])
control('Q65 tagged English (boundary)', [('questions-EN', cell(65, 'subject', lambda v: 'English Language and Comprehension')), ('questions-HI', cell(65, 'subject', lambda v: 'English Language and Comprehension'))])
control('Q66 tagged GA (boundary)', [('questions-EN', cell(66, 'subject', lambda v: 'General Awareness')), ('questions-HI', cell(66, 'subject', lambda v: 'General Awareness'))])
control('HI subject differs', [('questions-HI', cell(30, 'subject', lambda v: 'Numerical and Mathematical Ability'))])
control('wrong exam', [('questions-EN', cell(12, 'exam', lambda v: 'ssc-gd'))])
control('wrong year in HI', [('questions-HI', cell(44, 'year', lambda v: '2024'))])
control('dropped row', [('solutions-EN', lambda h, r: (h, r[:-1]))])
control('91st row', [('questions-EN', lambda h, r: (h, r + [list(r[-1])]))])
control('renamed header', [('questions-EN', lambda h, r: (['QNum'] + h[1:], r))])
control('stripped BOM', [('solutions-HI', lambda h, r: 'NOBOM')])
control('empty cell', [('solutions-EN', cell(50, 'trick', lambda v: ''))])
control('concept drift', [('solutions-EN', cell(8, 'concept', lambda v: v + ' X'))])
control('concept translated', [('solutions-HI', cell(8, 'concept', lambda v: 'औसत'))])
control('chapterId not in list', [('questions-EN', cell(2, 'chapterId', lambda v: 'quant.made-up')), ('questions-HI', cell(2, 'chapterId', lambda v: 'quant.made-up'))])
control('chapterId EN vs HI', [('questions-HI', cell(45, 'chapterId', lambda v: 'ga.polity'))])
control('chapterId column dropped', [(k, (lambda h, r: ([c for c in h if c != 'chapterId'], [[x for j, x in enumerate(row) if h[j] != 'chapterId'] for row in r]))) for k in ('questions-EN', 'questions-HI')])
control('three .other ids', [(k, (lambda h, r: (h, [row[:2] + ([{'1': 'quant.other', '21': 'reason.other', '41': 'ga.other'}[row[0]]] if row[0] in ('1', '21', '41') else [row[2]]) + row[3:] for row in r]))) for k in ('questions-EN', 'questions-HI')])
control('verdict removed', [('solutions-EN', cell(15, 'explanation', lambda v: VERDICT_RE.sub('', v)))])
control('wrong verdict letter', [('solutions-HI', cell(15, 'explanation', lambda v: re.sub(r'विकल्प \(([A-D])\)', lambda m: f'विकल्प ({flipk(m.group(1))})', v)))])
def drop_step(v):
    parts = re.split(r'(?=<div class="sol-step">)', v); return ''.join(p for i, p in enumerate(parts) if i != 1)
control('steps<4 EN', [('solutions-EN', cell(9, 'explanation', drop_step))])
control('steps<4 HI', [('solutions-HI', cell(29, 'explanation', drop_step))])
def drop_bullet(v):
    i = v.find('<div class="sol-bullet">'); j = v.find('</span></div>', i) + len('</span></div>'); return v[:i] + v[j:]
control('GA bullets<5', [('solutions-EN', cell(50, 'explanation', drop_bullet))])
def drop_fact(v):
    s = v.index('<div class="sol-section">'); i = v.find('<div class="sol-bullet">', s); j = v.find('</span></div>', i) + len('</span></div>'); return v[:i] + v[j:]
control('GA facts<3 EN', [('solutions-EN', cell(52, 'explanation', drop_fact))])
control('GA facts<3 HI', [('solutions-HI', cell(52, 'explanation', drop_fact))])
def drop_opt(v):
    i = v.find('Option (C)'); i = v.rfind('<div class="sol-bullet">', 0, i); j = v.find('</span></div>', i) + len('</span></div>'); return v[:i] + v[j:]
control('English option bullet dropped', [(k, cell(80, 'explanation', drop_opt)) for k in ('solutions-EN', 'solutions-HI')])
control('hard-coded Option (X)', [('solutions-EN', cell(12, 'explanation', lambda v: v.replace('</div>', ' Option (B) is right.</div>', 1)))])
control('hard-coded विकल्प (X)', [('solutions-HI', cell(12, 'trick', lambda v: v + ' विकल्प (B)'))])
control('Devanagari in EN file', [('solutions-EN', cell(20, 'trick', lambda v: v + ' काम'))])
control('Devanagari in HI Q66-90', [('solutions-HI', cell(75, 'trick', lambda v: v + ' त्रुटि'))])
control('HI Q66-90 stem differs', [('questions-HI', cellp('text', lambda q, v: q >= 66 and ' the ' in v, lambda v: v.replace(' the ', ' teh ', 1)))])
control('HI Q66-90 explanation differs', [('solutions-HI', cellp('explanation', lambda q, v: q >= 66 and ' the ' in v, lambda v: v.replace(' the ', ' teh ', 1)))])
control('HI stem loses Devanagari', [('questions-HI', cell(13, 'text', lambda v: 'What is the unit digit of the product?'))])
def copy_en(h, rows):
    he, re_ = load(TMP_SRC, 'solutions-EN'); en = {r[0]: r for r in re_}
    i = find(rows, h, 'explanation', lambda q, v: q == 47); rows[i][1] = en['47'][1]
TMP_SRC = SRC
control('HI solution copies EN', [('solutions-HI', copy_en)])
control('HI stem loses ||', [('questions-HI', cell(23, 'text', lambda v: v.replace('||', ' ')))])
control('HI option digit set broken', [('questions-HI', cellp('option_A', lambda q, v: q <= 65 and re.search(r'[0-68-9]', v), lambda v: re.sub(r'[0-68-9]', '7', v, count=1)))])
def swap_opt(h, rows):
    i = find(rows, h, 'option_A', lambda q, v: q == 46); a, b = h.index('option_A'), h.index('option_B')
    he, re_ = load(SRC, 'questions-EN'); en = {r[0]: r for r in re_}
    rows[i][a] = en['46'][b]
control('HI option = another EN option', [('questions-HI', swap_opt)])
control('HI option != module', [('questions-HI', cell(48, 'option_C', lambda v: v + 'ा'))])
control('dropped backslash dfrac', [('solutions-EN', cellp('explanation', lambda q, v: '\\dfrac' in v, lambda v: v.replace('\\dfrac', 'dfrac', 1)))])
control('dropped backslash times', [('solutions-EN', cellp('explanation', lambda q, v: '\\times' in v, lambda v: v.replace('\\times', 'times', 1)))])
control('constructed \\costheta', [('solutions-EN', cell(18, 'explanation', lambda v: v.replace('\\( ', '\\( \\costheta ', 1)))])
control('unbalanced paren', [('solutions-EN', cell(14, 'explanation', lambda v: v.replace('\\)', '', 1)))])
control('injected \\uXXXX', [('solutions-EN', cell(11, 'trick', lambda v: v + ' \\u00d7'))])
control('injected TAB', [('solutions-HI', cell(11, 'trick', lambda v: v + '\t'))])
control('doubled backslash', [('solutions-EN', cell(6, 'explanation', lambda v: v.replace('\\(', '\\\\(', 1)))])
control('B1 padded colon question cell', [('questions-EN', cell(14, 'option_A', lambda v: '3 : 7'))])
control('B1 padded colon solution cell', [('solutions-EN', cell(16, 'trick', lambda v: v + ' ratio 7 : 13'))])
control('plain-text Rs', [('solutions-EN', cell(10, 'trick', lambda v: v + ' Rs 1650'))])
control('plain-text x math', [('solutions-EN', cell(17, 'trick', lambda v: v + ' 7 x 8'))])
control('Devanagari inside span', [('solutions-HI', cell(5, 'explanation', lambda v: v.replace('\\( ', '\\( दर ', 1)))])
control('(figure 2) -> (चित्र 2)', [('questions-HI', cell(28, 'option_B', lambda v: '(चित्र 2)'))])

# the HI-option-vs-module check lives in checks via digit/other-option tests; recompute through hi_opts here:
def module_check():
    import assemble
    _, EN_Q, EN_S, HI_Q, HI_S = assemble.build(pdir)
    h, rows = load(SRC, 'questions-HI')
    return all([str(x) for x in r] == rows[i] for i, r in enumerate(HI_Q))
ok_mod = module_check()
fails = [r for r in results if not (r[1] and r[2])]
for r in results: print('  ', 'ok ' if r[1] and r[2] else 'BAD', r)
print(f'controls {len(results) - len(fails)}/{len(results)}; HI rows recomputed through hi_opts match file: {ok_mod}')
sys.exit(0 if not fails and ok_mod else 1)
