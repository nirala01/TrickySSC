import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/x/s3004_2.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-30-apr-shift-2'
PAPER = 'SSC GD Constable 2026 Apr 30 Shift 2'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {12, 13}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    out = []
    for tok in s.split(' '):
        out.append(T(tok) if re.search('[A-Z]', tok) else tok)
    return K(' '.join(out))
REP = {
 1: [('FS : IW :: WJ : ZN :: ? : LC', ana('FS : IW :: WJ : ZN :: ? : LC'))],
 14:[('?: MS710 :: AR318 : DV718 :: BK515 : EO915', ana('? : MS710 :: AR318 : DV718 :: BK515 : EO915'))],
 15:[('DFG43 : EDB86 :: TFK46 : IDR92 :: LPJ29 : ?', ana('DFG43 : EDB86 :: TFK46 : IDR92 :: LPJ29 : ?'))],
 17:[('965 : ? :: 826 : 1287 :: 891 : 1352', K('965 : ? :: 826 : 1287 :: 891 : 1352'))],
 18:[('2586 : 859 :: 2304 : 765 :: ? : 660', K('2586 : 859 :: 2304 : 765 :: ? : 660'))],
 43:[('(5/6)', K(r'\dfrac{5}{6}'))],
 47:[('(25/30)', K(r'\dfrac{25}{30}'))],
 48:[('5 : 3', K('5 : 3'))],
 49:[('A^{2}', K('A^{2}'))],
 57:[('5 : 4', K('5 : 4')), ('6 : 5', K('6 : 5'))],
 59:[('(3/11)', K(r'\dfrac{3}{11}'))],
}
FIXED_STEM = {
 44: K(r'\sqrt[3]{0.512} \times \sqrt{2.25} = ?'),
}
FIXED_OPTS = {
 43: [K(r'\dfrac{3}{4}'), K(r'\dfrac{2}{3}'), K(r'\dfrac{10}{11}'), K(r'\dfrac{4}{5}')],
 47: [K(r'\dfrac{15}{12}'), K(r'\dfrac{15}{2}'), K(r'\dfrac{30}{1}'), K(r'\dfrac{15}{1}')],
}
KEY_FIX = {}
EN_EDIT = {
 29: [('If the star is similar to the Sun,', 'An exoplanet orbits its star at the same distance at which the Earth orbits the Sun. If the star is similar to the Sun,')],
 68: [('sentence ._________ writing', 'sentence.||_________ writing')],
 72: [('his ambitious remarks only added fuel in the fire.', 'his <u>ambitious remarks only added fuel in the fire</u>.')],
 75: [('He ate all but none of the biscuits,', '<u>He ate all but none of the biscuits</u>,')],
}
HI_EDIT = {
 29: [('यदि तारा सूर्य के समान है,', 'एक बाह्यग्रह (exoplanet) अपने तारे की परिक्रमा उतनी ही दूरी पर करता है जितनी दूरी पर पृथ्वी सूर्य की परिक्रमा करती है। यदि तारा सूर्य के समान है,')],
}
# Q1 options A and D were truncated to single letters ("A", "Y") in the source (EN + HI) -> two realistic clusters of our own
OPT_FIX = {1: {'A': 'IA', 'Y': 'JY'}, 10: {'2400': '240O', '1920': '192O'}, 11: {'2160': '216O'}, 14: {'J0310': 'JO310'}}
OPT_FIX_EN = {64: {'Unscrupulous': 'Unscrupilous'}, 77: {'shal': 'shall'}}
OPT_FIX_HI = {}
HPD_STEM = {
 68: [('सुरक्षा कर्मी के लिए तय की गई कार्य प्रणाली क्या कहलाती है?',
       'सुरक्षा कर्मियों की ड्यूटी का समय, स्थान और कार्य तय करने वाली योजना क्या कहलाती है?')],
 74: [('<u>सही</u>', 'सही'), ('शब्दावली क्या होगी:', 'शब्दावली क्या होगी?')],
}
HPD_OPT = {70: {3: 'यात्रा के लिए'}, 79: {2: 'राष्ट्रीय'}}

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

# one passage for Q76-80 (Q76's copy); blanks D and E carry the tested words, shown as (D) <u>word</u>
PASSAGE_EN = clean(EN[75]['comp'])
for a, b in [('________ A ________', '___A___'), ('________ B ________', '___B___'), ('________ C ________', '___C___'),
             ('________ D ________ (restriction)', '(D) <u>restriction</u>'), ('________ E ________ (illustrates)', '(E) <u>illustrates</u>')]:
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
            t = 'PASSAGE (Q75–Q79): ' + p + ' || ' + t
        op = [HPD_OPT.get(n, {}).get(k, clean(x)) for k, x in enumerate(q['opts'])]
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
    for need in ['A: IA\n', 'D: JY\n', 'A: 240O\n', 'B: 192O\n', 'B: 216O\n', 'A: JO310\n', 'D: Unscrupilous\n', 'C: shall\n',
                 '(D) <u>restriction</u>', '(E) <u>illustrates</u>', '<u>ambitious remarks only added fuel in the fire</u>',
                 '<u>He ate all but none of the biscuits</u>', 'sentence.||_________ writing', 'same distance at which the Earth']:
        assert need in en, need
    for bad in ['J0310', 'B: 2160\n', 'A: 2400\n', 'B: 1920\n', 'shal\n', '________ A', 'A: A\n', 'D: Y\n']:
        assert bad not in en, bad
    assert 'D: यात्रा के लिए\n' in hp and 'C: राष्ट्रीय\n' in hp and '<u>' not in hp and 'होगी?' in hp and 'ड्यूटी का समय' in hp
    assert hp.count('PASSAGE (Q75–Q79)') == 5
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['1']['opts'] == ['IA', 'IY', 'FB', 'JY'] and h['10']['opts'][:2] == ['240O', '192O'] and h['11']['opts'][1] == '216O'
    assert 'पृथ्वी सूर्य की परिक्रमा' in h['29']['TEXT'] and h['44']['TEXT'].startswith('निम्नलिखित')
    print('ok')
