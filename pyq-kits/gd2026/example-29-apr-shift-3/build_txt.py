import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/x/s2904_3.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-29-apr-shift-3'
PAPER = 'SSC GD Constable 2026 Apr 29 Shift 3'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {12, 13}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
# exact replacements in the stem, BOTH languages (anchor must exist) — B1 wraps and fractions
REP = {
 1: [('? : XVF :: ANT : WJP :: EUM : AQI', K(r'? : ' + T('XVF') + ' :: ' + T('ANT') + ' : ' + T('WJP') + ' :: ' + T('EUM') + ' : ' + T('AQI')))],
 14:[('CK42 : EM84 :: ? : ZW96 :: KI14 : MK28', K(T('CK42') + ' : ' + T('EM84') + ' :: ? : ' + T('ZW96') + ' :: ' + T('KI14') + ' : ' + T('MK28')))],
 15:[('DEW14 : GHT28 :: LKO28 : ONL56 :: ACJ40 : ?', K(T('DEW14') + ' : ' + T('GHT28') + ' :: ' + T('LKO28') + ' : ' + T('ONL56') + ' :: ' + T('ACJ40') + ' : ?'))],
 17:[('136 : 671 :: 332 : ? :: 950 : 1485', K('136 : 671 :: 332 : ? :: 950 : 1485'))],
 18:[('1083 : 363 :: 2487 : 831 :: 804 : ?', K('1083 : 363 :: 2487 : 831 :: 804 : ?'))],
 47:[('3/5', K(r'\dfrac{3}{5}')), ('4/15', K(r'\dfrac{4}{15}')), ('8/25', K(r'\dfrac{8}{25}'))],
 48:[('3 : 5', K('3 : 5'))],
 49:[('2/5', K(r'\dfrac{2}{5}'))],
 57:[('2 : 4 : 5 : 7', K('2 : 4 : 5 : 7'))],
}
FIXED_STEM = {
 43: K(r'\sqrt{1.44 \times 0.0225} = ?'),
 44: K(r'\sqrt{0.09} + \sqrt[3]{0.125} + \sqrt[4]{0.0081} - \sqrt{0.64} = ?'),
}
FIXED_OPTS = {
 47: [K(r'\dfrac{24}{25}'), K(r'\dfrac{24}{5}'), K(r'\dfrac{16}{5}'), K(r'\dfrac{16}{25}')],
 53: [K(r'\dfrac{3}{2}'), '1', K(r'\dfrac{5}{2}'), '3'],
}
# stem corrections (listed in the delivery report)
EN_EDIT = {
 37: [('In June 2024,', 'In August 2024,')],
 72: [('The new policy was believing to have reduced corruption', 'The new policy <u>was believing to have reduced</u> corruption')],
 73: [('Antoine felt: ill at ease', 'Antoine felt ill at ease'), ('at a review when; he did not', 'at a review when he did not'),
      ('as he; leaned his head out', 'as he leaned his head out'), ('in the distance: his father', 'in the distance his father')],
 75: [('the parties did nothing but accused each other.', 'the parties <u>did nothing but accused each other</u>.')],
}
HI_EDIT = {37: [('जून 2024 में,', 'अगस्त 2024 में,')]}
OPT_FIX = {1: {'BZ1': 'BZJ'}}
OPT_FIX_EN = {71: {'into': 'onto'}, 79: {'shal': 'shall', 'Wil': 'will'}}
OPT_FIX_HI = {29: {'पुडुचेरी (पॉन्डिक्षेरी)': 'पुडुचेरी (पॉन्डिचेरी)'}}
# Hindi Part D corrections
HPD_STEM = {67: [("'कुख्यात '", "'कुख्यात'")], 74: [('<u>सही</u>', 'सही'), ('शब्दावली क्या होगी:', 'शब्दावली क्या होगी?')]}

def edit(t, pair, n, tag):
    a, b = pair
    if a not in t: raise SystemExit(f'Q{n} {tag}: anchor missing {a!r}')
    return t.replace(a, b, 1)

def stem(q, n, lang):
    if n in FIXED_STEM: return FIXED_STEM[n]
    t = clean(q['text'])
    t = re.sub(r'\\\(\s*(.*?)\s*\\\)', lambda m: m.group(1), t)
    for pair in REP.get(n, []): t = edit(t, pair, n, lang)
    for pair in (EN_EDIT if lang == 'EN' else HI_EDIT).get(n, []): t = edit(t, pair, n, lang + '_EDIT')
    if '[BR]' in t and '||' not in t: t = t.replace('[BR]', '||', 1)
    if n in FIG: t = '[FIGURE-BASED] ' + t
    return t

def opts(q, n, lang):
    if n in FIG: return [f'(figure {i})' for i in range(1, 5)]
    if n in FIXED_OPTS: return FIXED_OPTS[n]
    out = []
    for x in q['opts']:
        v = clean(x)
        v = OPT_FIX.get(n, {}).get(v, v)
        v = (OPT_FIX_EN if lang == 'EN' else OPT_FIX_HI).get(n, {}).get(v, v)
        out.append(v)
    return out

def block(n, subj, concept, text, op, ans):
    return f"[Q{n}]\nSUBJECT: {subj}\nCONCEPT: {concept}\nTEXT: {text}\nA: {op[0]}\nB: {op[1]}\nC: {op[2]}\nD: {op[3]}\nANSWER: {ans}\n"

def header(lang): return f"# TRICKYSSC QUESTIONS\nEXAM: ssc-gd\nYEAR: 2026\nPAPER: {PAPER}\nLANG: {lang}\n"

# one passage for Q76-80 (source repeats it with uneven blank lengths and quote styles)
PASSAGE_EN = clean(EN[75]['comp'])

def build_en():
    out = [header('EN')]
    for i in range(80):
        q = EN[i]; n = i + 1
        t = stem(q, n, 'EN')
        if q['comp']:
            t = 'PASSAGE (Q76–Q80): ' + PASSAGE_EN + ' || ' + t
        op = opts(q, n, 'EN')
        out.append(block(n, SUBJ[q['si']], CON_EN[n], t, op, 'ABCD'[q['cidx']]))
    return '\n'.join(out)

def build_hi_partd():
    out = [header('HI')]
    for i in range(80, 100):
        q = HI[i]; n = i - 19
        t = clean(q['text'])
        for pair in HPD_STEM.get(n, []): t = edit(t, pair, n, 'HPD')
        if '[BR]' in t: t = t.replace('[BR]', '||', 1)
        if q['comp']: t = 'PASSAGE (Q75–Q79): ' + clean(q['comp']) + ' || ' + t
        op = [clean(x) for x in q['opts']]
        out.append(block(n, 'Hindi Language', CON_HI[n], t, op, 'ABCD'[q['cidx']]))
    return '\n'.join(out)

def hi_q1_60():
    D = {}
    for i in range(60):
        q = HI[i]; n = i + 1
        t = stem(q, n, 'HI')
        if not re.search('[ऀ-ॿ]', t): t = 'निम्नलिखित व्यंजक का मान ज्ञात कीजिए।||' + t
        D[n] = dict(TEXT=t, opts=opts(q, n, 'HI'), ANSWER='ABCD'[q['cidx']])
    return D

if __name__ == '__main__':
    os.makedirs(f'{HERE}/out', exist_ok=True)
    assert all(EN[i]['cidx'] == HI[i]['cidx'] for i in range(60)), 'EN/HI keys differ in Q1-60'
    assert all(EN[i]['si'] == HI[i]['si'] for i in range(100))
    assert all(len(q['opts']) == 4 for q in EN[:80] + HI[80:])
    open(f'{HERE}/out/{PREFIX}-questions-EN.txt', 'w', encoding='utf-8').write(build_en())
    open(f'{HERE}/out/{PREFIX}-questions-HI-partD.txt', 'w', encoding='utf-8').write(build_hi_partd())
    json.dump(hi_q1_60(), open(f'{HERE}/hi_q1_60.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    en = open(f'{HERE}/out/{PREFIX}-questions-EN.txt', encoding='utf-8').read()
    hp = open(f'{HERE}/out/{PREFIX}-questions-HI-partD.txt', encoding='utf-8').read()
    for need in ['B: BZJ', 'D: onto', 'A: shall', 'B: will', 'In August 2024,']:
        assert need in en, need
    for bad in ['BZ1', 'felt:', 'when;', 'he;', 'shal\n', 'Wil\n']:
        assert bad not in en, bad
    assert "'कुख्यात'" in hp and '<u>' not in hp and 'होगी?' in hp
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['1']['opts'][1] == 'BZJ' and h['29']['opts'][2] == 'पुडुचेरी (पॉन्डिचेरी)' and 'अगस्त 2024' in h['37']['TEXT']
    print('ok')
