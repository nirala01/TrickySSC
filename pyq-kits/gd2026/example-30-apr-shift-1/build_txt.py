import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/x/s3004_1.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-30-apr-shift-1'
PAPER = 'SSC GD Constable 2026 Apr 30 Shift 1'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {11, 12}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    # letter/number cluster analogy with padded colons -> one KaTeX span, letter clusters in \text{}
    out = []
    for tok in s.split(' '):
        out.append(T(tok) if re.search('[A-Z]', tok) else tok)
    return K(' '.join(out))
REP = {
 1: [('KS : PH :: DN : WM :: ? : TQ', ana('KS : PH :: DN : WM :: ? : TQ'))],
 13:[('BL95 : OE141 :: DK81 : NG127 :: KF63 : ?', ana('BL95 : OE141 :: DK81 : NG127 :: KF63 : ?'))],
 14:[('RTU420 : ? :: YXD500 : VUA260 :: KMO480 : HJL240', ana('RTU420 : ? :: YXD500 : VUA260 :: KMO480 : HJL240'))],
 15:[('6307 : 6251 :: 4661 : ? :: 8253 : 8197', K('6307 : 6251 :: 4661 : ? :: 8253 : 8197'))],
 16:[('? : 581 :: 714 : 393 :: 759 : 438', K('? : 581 :: 714 : 393 :: 759 : 438'))],
 54:[('2/3', K(r'\dfrac{2}{3}'))],
 58:[('(7/10)', K(r'\dfrac{7}{10}'))],
}
FIXED_STEM = {
 44: K(r'\dfrac{(12.4 + 3.6)^{2} - (12.4 - 3.6)^{2}}{12.4 \times 3.6} = ?'),
 45: K(r'(10)^{3} + (6)^{3} + 3 \times 10 \times 6 \times 16 = ?'),
}
FIXED_OPTS = {
 54: [K(r'\dfrac{72}{13}'), K(r'\dfrac{72}{11}'), K(r'\dfrac{65}{9}'), K(r'\dfrac{61}{13}')],
}
# key: source EN/HI cidx for Q28 is A (Tushar Panwar) but the source's own Gujarati paper keys C and the source
# solution (all three languages) says Nitin Gupta, who set the 19:24.48 record (Patna, 10 Mar 2025) -> official key C
KEY_FIX = {28: 'C'}
EN_EDIT = {
 73: [('the higher one ascends, the lesser oxygen is available.', 'the higher one ascends, <u>the lesser oxygen is available</u>.')],
 75: [('If one is honest, people will respect you.', '<u>If one is honest</u>, people will respect you.')],
}
HI_EDIT = {11: [('(: :) के बाईं', '(::) के बाईं'), ('से (: :) के दाईं', 'से (::) के दाईं')],
           17: [('के रूप रूप में', 'के रूप में')]}
OPT_FIX = {17: {'SBlU': 'SBIU'}}
OPT_FIX_EN = {66: {'Concea': 'Conceal'}, 72: {'al': 'at', 'ïn': 'in', '01': 'on'}}
OPT_FIX_HI = {}
# Hindi Part D corrections
HPD_STEM = {
 72: [('<u>सही</u>', 'सही'), ('शब्दावली क्या होगा:', 'शब्दावली क्या होगी?')],
 75: [('पुलिस द्वारा जारी आधिकारिक लिखित सूचना क्या कहलाती है?',
       'पुलिस विभाग द्वारा अपने सभी थानों और कार्यालयों को एक साथ भेजी जाने वाली आधिकारिक लिखित सूचना क्या कहलाती है?')],
 76: [('पुलिस द्वारा जारी आधिकारिक लिखित सूचना क्या कहलाती है?',
       'गद्यांश में भारत की आंतरिक सुरक्षा के लिए तैनात किन अर्धसैनिक बलों के उदाहरण दिए गए हैं?')],
}
HPD_OPT = {61: {'बारात': 'बारत'}}

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

# one passage for Q76-80; blanks C and D carry the tested words, shown as (C) <u>word</u>
PASSAGE_EN = clean(EN[75]['comp'])
for a, b in [('____ A ____', '___A___'), ('____ B ____', '___B___'), ('____ E ____', '___E___'),
             ('____ C ____ (gallantry)', '(C) <u>gallantry</u>'), ('____ D ____ (conspicuous)', '(D) <u>conspicuous</u>')]:
    assert PASSAGE_EN.count(a) == 1, a
    PASSAGE_EN = PASSAGE_EN.replace(a, b)

def build_en():
    out = [header('EN')]
    for i in range(80):
        q = EN[i]; n = i + 1
        t = stem(q, n, 'EN')
        if q['comp']:
            t = 'PASSAGE (Q76–Q80): ' + PASSAGE_EN + ' || ' + t
        op = opts(q, n, 'EN')
        out.append(block(n, SUBJ[q['si']], CON_EN[n], t, op, KEY_FIX.get(n, 'ABCD'[q['cidx']])))
    return '\n'.join(out)

def build_hi_partd():
    out = [header('HI')]
    for i in range(80, 100):
        q = HI[i]; n = i - 19
        t = clean(q['text'])
        for pair in HPD_STEM.get(n, []): t = edit(t, pair, n, 'HPD')
        if '[BR]' in t: t = t.replace('[BR]', '||', 1)
        if q['comp']:
            p = re.sub(r'\[BR\]उपरोक्त गद्यांश के आधार पर प्रश्न का उत्तर दें:\s*$', '', clean(q['comp']))
            assert 'उपरोक्त' not in p
            t = 'PASSAGE (Q76–Q80): ' + p + ' || ' + t
        op = [HPD_OPT.get(n, {}).get(clean(x), clean(x)) for x in q['opts']]
        out.append(block(n, 'Hindi Language', CON_HI[n], t, op, 'ABCD'[q['cidx']]))
    return '\n'.join(out)

def hi_q1_60():
    D = {}
    for i in range(60):
        q = HI[i]; n = i + 1
        t = stem(q, n, 'HI')
        if not re.search('[ऀ-ॿ]', t): t = 'निम्नलिखित व्यंजक का मान ज्ञात कीजिए।||' + t
        D[n] = dict(TEXT=t, opts=opts(q, n, 'HI'), ANSWER=KEY_FIX.get(n, 'ABCD'[q['cidx']]))
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
    for need in ['C: SBIU', 'C: Conceal', 'A: at\n', 'C: in\n', 'D: on\n', '(C) <u>gallantry</u>', '(D) <u>conspicuous</u>',
                 '<u>the lesser oxygen is available</u>', '<u>If one is honest</u>']:
        assert need in en, need
    for bad in ['SBlU', 'Concea\n', 'ïn', '____ A', '____ C', 'different different']:
        assert bad not in en, bad
    assert 'A: बारत\n' in hp and '<u>' not in hp and 'होगी?' in hp and hp.count('पुलिस द्वारा जारी आधिकारिक') == 0
    assert hp.count('PASSAGE (Q76–Q80)') == 5
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['17']['opts'][2] == 'SBIU' and '(: :)' not in h['11']['TEXT'] and 'रूप रूप' not in h['17']['TEXT'] and h['28']['ANSWER'] == 'C'
    print('ok')
