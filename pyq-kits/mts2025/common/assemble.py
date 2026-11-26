"""Assemble the 4 CSVs. usage: assemble.py <paperdir> [outdir]
paperdir holds data.py, sol_en.py (M, G, E dicts), hi.py (HQ, HM, HG dicts) and out/<prefix>-questions-EN.txt
"""
import sys, os, re, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from base import *


def load(pdir, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(pdir, name + '.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def build(pdir):
    D = load(pdir, 'data')
    txt = os.path.join(pdir, 'out', f'{D.META["prefix"]}-questions-EN.txt')
    hdr, Q_EN = parse_txt(txt)
    opt_bullets, hi_opts = make_helpers(Q_EN)
    import builtins
    builtins.opt_bullets = opt_bullets      # sol_en may call opt_bullets(n, {...})
    S = load(pdir, 'sol_en'); H = load(pdir, 'hi')
    YEAR = hdr['YEAR']
    EN_Q, EN_S, HI_Q, HI_S = [], [], [], []
    for n in range(1, N_Q + 1):
        q = Q_EN[n]; key = q['ANSWER']; ktext = q[key]
        qrow = (n, SUBJECT[n], D.CHAPTER[n], EXAM, YEAR, q['TEXT'], q['A'], q['B'], q['C'], q['D'], key)
        if n in S.M:
            raw, trick = S.M[n]; exp = explanation(raw, None, key, ktext, 'en')
        elif n in S.G:
            raw, facts, trick = S.G[n]; exp = explanation(raw, facts, key, ktext, 'en')
        else:
            ctx, notes, trick = S.E[n]
            raw = ctx.rstrip() + '\n' + opt_bullets(n, notes)
            exp = explanation(raw, None, key, ktext, 'en')
        srow = (n, exp, trick, q['CONCEPT'])
        EN_Q.append(qrow); EN_S.append(srow)
        if n in TRANSLATED:
            stem_hi, mp = H.HQ[n]
            HI_Q.append((n, SUBJECT[n], D.CHAPTER[n], EXAM, YEAR, stem_hi, *hi_opts(n, mp), key))
            if n in H.HM:
                raw, tr = H.HM[n]; e2 = explanation(raw, None, key, hi_opts(n, mp)['ABCD'.index(key)], 'hi')
            else:
                raw, facts, tr = H.HG[n]; e2 = explanation(raw, facts, key, hi_opts(n, mp)['ABCD'.index(key)], 'hi')
            HI_S.append((n, e2, tr, q['CONCEPT']))
        else:
            HI_Q.append(qrow); HI_S.append(srow)      # same objects: cannot drift
    return D, EN_Q, EN_S, HI_Q, HI_S


if __name__ == '__main__':
    pdir = sys.argv[1]
    D, EN_Q, EN_S, HI_Q, HI_S = build(pdir)
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(pdir, 'out')
    p = D.META['prefix']
    write_csv(os.path.join(out, f'{p}-questions-EN.csv'), QHDR, EN_Q)
    write_csv(os.path.join(out, f'{p}-questions-HI.csv'), QHDR, HI_Q)
    write_csv(os.path.join(out, f'{p}-solutions-EN.csv'), SHDR, EN_S)
    write_csv(os.path.join(out, f'{p}-solutions-HI.csv'), SHDR, HI_S)
    print('wrote 4 CSVs to', out)
