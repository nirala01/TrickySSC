"""PROMPT-5-MTS §9 checks on the 4 CSVs. usage: checks.py <paperdir> [csvdir]"""
import sys, os, re, csv, collections, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from base import *
from chapters import CHAPTER_IDS

BS = chr(92)
BRACE_CMDS = ['frac', 'dfrac', 'tfrac', 'sqrt', 'text', 'operatorname']
SYM_CMDS = ['times', 'div', 'pi', 'theta', 'cdot', 'circ']
KNOWN = set('''frac dfrac tfrac sqrt text operatorname times div pi theta cdot circ left right le ge leq geq neq ne approx
 therefore because angle triangle degree circ pm mp infty sum alpha beta gamma Rightarrow rightarrow Leftrightarrow to quad qquad
 overline underline hat bar cos sin tan cot sec cosec csc log ln mathrm mathbf boxed cancel implies equiv propto sim
 cup cap in notin subset subseteq emptyset dots ldots cdots percent Delta delta lambda mu sigma omega phi rho prime
 begin end array lfloor rfloor lceil rceil vert lvert rvert mid ast star bullet square triangle space ,'''.split())


def read(path):
    raw = open(path, 'rb').read()
    bom = raw.startswith(b'\xef\xbb\xbf')
    with open(path, encoding='utf-8-sig', newline='') as fh:
        r = csv.reader(fh); rows = list(r)
    return bom, rows[0], rows[1:]


def run(pdir, cdir=None):
    errs = []; info = {}
    spec = importlib.util.spec_from_file_location('d', os.path.join(pdir, 'data.py')); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
    cdir = cdir or os.path.join(pdir, 'out'); p = D.META['prefix']
    hdr, T = parse_txt(os.path.join(pdir, 'out', f'{p}-questions-EN.txt'))
    F = {}
    for k in ('questions-EN', 'questions-HI', 'solutions-EN', 'solutions-HI'):
        path = os.path.join(cdir, f'{p}-{k}.csv')
        try:
            bom, h, rows = read(path)
        except Exception as e:
            errs.append(f'{k} unreadable {e}'); return errs, info
        want = QHDR if k.startswith('q') else SHDR
        if h != want: errs.append(f'{k} header {h}')
        if not bom: errs.append(f'{k} no BOM')
        if len(rows) != 90: errs.append(f'{k} rows {len(rows)}')
        if [r[0] for r in rows] != [str(i) for i in range(1, len(rows) + 1)]: errs.append(f'{k} qNum order')
        F[k] = {int(r[0]): dict(zip(h, r)) for r in rows if r and r[0].isdigit()}
        try:
            with open(path, encoding='utf-8-sig', newline='') as fh: list(csv.DictReader(fh))
        except Exception as e: errs.append(f'{k} DictReader {e}')
    if errs: return errs, info
    QE, QH, SE, SH = F['questions-EN'], F['questions-HI'], F['solutions-EN'], F['solutions-HI']
    others = 0
    for n in range(1, 91):
        if n not in QE or n not in QH or n not in SE or n not in SH: errs.append(f'Q{n} missing row'); continue
        qe, qh, se, sh = QE[n], QH[n], SE[n], SH[n]; t = T[n]
        # 2 subject/exam/year
        for lab, r in (('EN', qe), ('HI', qh)):
            if r['subject'] != SUBJECT[n]: errs.append(f'Q{n} {lab} subject')
            if r['exam'] != EXAM: errs.append(f'Q{n} {lab} exam')
            if r['year'] != hdr['YEAR']: errs.append(f'Q{n} {lab} year')
        # 3 keys
        if qe['correct'] != t['ANSWER']: errs.append(f'Q{n} EN key != txt')
        if qh['correct'] != qe['correct']: errs.append(f'Q{n} HI key != EN')
        # 4 verbatim
        for c, L in (('text', 'TEXT'), ('option_A', 'A'), ('option_B', 'B'), ('option_C', 'C'), ('option_D', 'D')):
            if qe[c] != t[L]: errs.append(f'Q{n} EN {c} drift')
        # 5 chapter
        if qe['chapterId'] not in CHAPTER_IDS: errs.append(f'Q{n} chapterId {qe["chapterId"]!r} not in list')
        if qh['chapterId'] != qe['chapterId']: errs.append(f'Q{n} chapterId EN != HI')
        if qe['chapterId'].split('.')[0] in ('hindi', 'computer', 'statistics', 'fineco'): errs.append(f'Q{n} forbidden family')
        if qe['chapterId'].endswith('.other'): others += 1
        # concept
        for lab, s in (('EN', se), ('HI', sh)):
            if s['concept'] != t['CONCEPT']: errs.append(f'Q{n} {lab} concept drift')
        # 6 verdict
        for lab, s, key in (('EN', se, qe['correct']), ('HI', sh, qh['correct'])):
            m = re.search(r'<div class="sol-verdict"><span class="vmk">✓</span><span>(?:Correct answer: Option|सही उत्तर: विकल्प) \(([A-D])\)', s['explanation'])
            if not m or m.group(1) != key: errs.append(f'Q{n} {lab} verdict')
        body_e = VERDICT_RE.sub('', se['explanation']); body_h = VERDICT_RE.sub('', sh['explanation'])
        # 7 stray letters
        if n in TRANSLATED:
            for lab, b, tr in (('EN', body_e, se['trick']), ('HI', body_h, sh['trick'])):
                if re.search(r'(?:[Oo]ption|विकल्प)\s*\(([A-Da-d])\)', b + ' ' + tr): errs.append(f'Q{n} {lab} hard-coded option letter')
        # 8 depth
        def steps(b): return len(re.findall(r'<div class="sol-step">(?:Step|चरण) \d+:', b))
        def buls(b): return len(re.findall(r'<div class="sol-bullet">', b.split('<div class="sol-section">')[0]))
        def facts(b):
            parts = b.split('<div class="sol-section">')
            return len(re.findall(r'<div class="sol-bullet">', parts[1])) if len(parts) > 1 else 0
        if n in MATHS_BAND or n in REASON_BAND:
            if steps(body_e) < 4: errs.append(f'Q{n} EN steps<4')
            if steps(body_h) < 4: errs.append(f'Q{n} HI steps<4')
        elif n in GA_BAND:
            if buls(body_e) < 5: errs.append(f'Q{n} EN GA bullets<5')
            if buls(body_h) < 5: errs.append(f'Q{n} HI GA bullets<5')
            if 'Exam Facts' not in body_e or facts(body_e) < 3: errs.append(f'Q{n} EN facts<3')
            if 'अतिरिक्त तथ्य' not in body_h or facts(body_h) < 3: errs.append(f'Q{n} HI facts<3')
        else:
            if buls(body_e) < 6: errs.append(f'Q{n} English bullets<6')
            pos = [body_e.find(f'Option ({L})') for L in 'ABCD']
            if min(pos) < 0 or pos != sorted(pos): errs.append(f'Q{n} English option bullets order')
        # 9 maths katex
        if n in MATHS_BAND:
            if '\\(' not in se['explanation'] or '\\(' not in sh['explanation']: errs.append(f'Q{n} maths without KaTeX')
        # 10 language rules
        allen = [qe[c] for c in QHDR] + [se[c] for c in SHDR]
        if any(DEVA.search(c) for c in allen): errs.append(f'Q{n} Devanagari in EN file')
        if n in TRANSLATED:
            if not DEVA.search(qh['text']): errs.append(f'Q{n} HI stem no Devanagari')
            if not DEVA.search(sh['explanation']): errs.append(f'Q{n} HI solution no Devanagari')
            if sh['explanation'] == se['explanation']: errs.append(f'Q{n} HI solution copies EN')
            if ('||' in qe['text']) != ('||' in qh['text']): errs.append(f'Q{n} HI || mismatch')
            if qe['text'].startswith('[FIGURE-BASED]') != qh['text'].startswith('[FIGURE-BASED]'): errs.append(f'Q{n} HI figure tag')
        else:
            for c in QHDR:
                if qh[c] != qe[c]: errs.append(f'Q{n} HI {c} != EN (English band)')
            for c in SHDR:
                if sh[c] != se[c]: errs.append(f'Q{n} HI sol {c} != EN (English band)')
        # 11 HI option alignment
        if n in TRANSLATED:
            eo = [qe['option_' + L] for L in 'ABCD']; ho = [qh['option_' + L] for L in 'ABCD']
            for i in range(4):
                if collections.Counter(re.findall(r'\d', eo[i])) != collections.Counter(re.findall(r'\d', ho[i])):
                    errs.append(f'Q{n} HI option {"ABCD"[i]} digit set')
                if ho[i] in eo and ho[i] != eo[i]: errs.append(f'Q{n} HI option {"ABCD"[i]} equals another EN option')
            for i, o in enumerate(eo):
                if o.startswith('(figure') and ho[i] != o: errs.append(f'Q{n} figure label translated')
        # 12-16 cell scans
        cells = {f'qe.{c}': qe[c] for c in ('text', 'option_A', 'option_B', 'option_C', 'option_D')}
        cells.update({f'qh.{c}': qh[c] for c in ('text', 'option_A', 'option_B', 'option_C', 'option_D')})
        cells.update({f'se.{c}': se[c] for c in ('explanation', 'trick')}); cells.update({f'sh.{c}': sh[c] for c in ('explanation', 'trick')})
        for nm, c in cells.items():
            spans = re.findall(r'\\\((.*?)\\\)', c, re.S)
            if any(DEVA.search(s) for s in spans): errs.append(f'Q{n} {nm} Devanagari inside KaTeX')
            if c.count('\\(') != c.count('\\)'): errs.append(f'Q{n} {nm} unbalanced \\( \\)')
            if re.search(r'\\u[0-9a-fA-F]{4}', c): errs.append(f'Q{n} {nm} literal \\u')
            if '\t' in c: errs.append(f'Q{n} {nm} TAB')
            if BS + BS in c: errs.append(f'Q{n} {nm} doubled backslash')
            if re.search(r'(?<![' + BS + BS + r'A-Za-z])(' + '|'.join(BRACE_CMDS) + r')\{', c): errs.append(f'Q{n} {nm} bare brace command')
            for s in spans:
                if re.search(r'(?<![' + BS + BS + r'A-Za-z{])(' + '|'.join(SYM_CMDS) + r')(?![A-Za-z])', s): errs.append(f'Q{n} {nm} bare symbol command')
                for cmd in re.findall(BS + BS + r'([A-Za-z]+)', s):
                    if cmd not in KNOWN: errs.append(f'Q{n} {nm} unknown command \\{cmd}')
            kt = re.sub(r'\\\(.*?\\\)', 'KTX', c, flags=re.S)
            if nm.startswith('q'):
                if re.search(r'\s:', kt) and not re.search(r'(Statements|Conclusions|Directions|Credit|PASSAGE \(Q\d+–Q\d+\))\s?:', kt): errs.append(f'Q{n} {nm} B1 padded colon')
            else:
                plain = re.sub(r'<[^>]+>', ' ', kt)
                if re.search(r'\d\s+:\s*\d|\w\s:\s\w', plain): errs.append(f'Q{n} {nm} B1 padded colon in solution')
                if re.search(r'\bRs\.?\s*\d', plain) or re.search(r'\d\s*x\s*\d', plain): errs.append(f'Q{n} {nm} plain-text math')
        # 17 non-empty
        for lab, s in (('EN', se), ('HI', sh)):
            for c in ('explanation', 'trick', 'concept'):
                if not s[c].strip(): errs.append(f'Q{n} {lab} empty {c}')
        for lab, r in (('EN', qe), ('HI', qh)):
            for c in QHDR:
                if not str(r[c]).strip(): errs.append(f'Q{n} {lab} empty {c}')
        if any(qe['option_' + L].startswith('(figure') for L in 'ABCD') and not qe['text'].startswith('[FIGURE-BASED]'):
            errs.append(f'Q{n} figure label without figure question')
    # 18 HI rows recomputed from the hi.py module through hi_opts (Q1-65) must equal the file
    try:
        import assemble
        _, _, _, HQ_, _ = assemble.build(pdir)
        for row in HQ_:
            n = int(row[0]); r = QH.get(n)
            if r is None: continue
            if [str(x) for x in row] != [r[c] for c in QHDR]: errs.append(f'Q{n} HI row != module')
    except Exception as e:
        errs.append(f'module recompute failed {e}')
    if others >= 3: errs.append(f'{others} .other chapter ids')
    info['others'] = others
    info['dist'] = dict(sorted(collections.Counter(QE[n]['correct'] for n in QE).items()))
    info['figset'] = sorted(n for n in QE if QE[n]['text'].startswith('[FIGURE-BASED]'))
    if set(info['figset']) != set(D.FIG): errs.append('figure set != docx set')
    return errs, info


if __name__ == '__main__':
    e, i = run(*sys.argv[1:3])
    print('FAIL' if e else 'PASS', *e[:60], sep='\n  ')
    print(i)
    sys.exit(1 if e else 0)
