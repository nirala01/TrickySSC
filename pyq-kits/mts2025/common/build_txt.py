"""Build <PREFIX>-questions-EN.txt from the paper's data.py (all 90 stems/options typed there) and the source key.
usage: python build_txt.py <paperdir>"""
import sys, os, re, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from base import SUBJECT, N_Q
from srckey import keys

pdir = sys.argv[1]
spec = importlib.util.spec_from_file_location('data', os.path.join(pdir, 'data.py'))
D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
K = keys(D.META['src'])
K.update(getattr(D, 'KEY_FIX', {}))
out = ['# TRICKYSSC QUESTIONS', 'EXAM: ssc-mts', f'YEAR: {D.META["year"]}', f'PAPER: {D.META["paper"]}', 'LANG: EN', '']
for n in range(1, N_Q + 1):
    text, opts = D.T[n]
    if getattr(D, 'PASSAGE', None) and D.PASSAGE[0] <= n <= D.PASSAGE[1]:
        text = f'PASSAGE (Q{D.PASSAGE[0]}–Q{D.PASSAGE[1]}): {D.PASSAGE_TEXT} || {text}'
    assert len(opts) == 4 and all(o.strip() for o in opts), f'Q{n} blank option {opts}'
    out += [f'[Q{n}]', f'SUBJECT: {SUBJECT[n]}', f'CONCEPT: {D.CONCEPT[n]}', f'TEXT: {text}',
            f'A: {opts[0]}', f'B: {opts[1]}', f'C: {opts[2]}', f'D: {opts[3]}', f'ANSWER: {K[n]}', '']
path = os.path.join(pdir, 'out', f'{D.META["prefix"]}-questions-EN.txt')
os.makedirs(os.path.dirname(path), exist_ok=True)
open(path, 'w', encoding='utf-8').write('\n'.join(out).rstrip('\n') + '\n')
print('wrote', path)
