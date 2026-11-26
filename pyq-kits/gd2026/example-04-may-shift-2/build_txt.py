import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/x/s0405_2.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-04-may-shift-2'
PAPER = 'SSC GD Constable 2026 May 04 Shift 2'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {10, 11}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    out = []
    for tok in s.split(' '):
        out.append(T(tok) if re.search('[A-Z]', tok) else tok)
    return K(' '.join(out))
REP = {
 1: [('? : PA :: FA : DW :: PK : NG', ana('? : PA :: FA : DW :: PK : NG'))],
 12:[('JT310 : WM218 :: AT520 : WD428 :: LD620 : ?', ana('JT310 : WM218 :: AT520 : WD428 :: LD620 : ?'))],
 13:[('SP120 : PY180 :: EB200 : BK300 :: ? : KP135', ana('SP120 : PY180 :: EB200 : BK300 :: ? : KP135'))],
 14:[('2458 : 2501 :: 7327 : 7370 :: 7635 : ?', K('2458 : 2501 :: 7327 : 7370 :: 7635 : ?'))],
 15:[('13 : 34 :: 587 : 1756 :: 575 : ?', K('13 : 34 :: 587 : 1756 :: 575 : ?'))],
 45:[('2\\frac{1}{3}', K(r'2\dfrac{1}{3}')), ('2\\frac{5}{6}', K(r'2\dfrac{5}{6}'))],
 49:[('2 : 3', K('2 : 3'))],
}
REP_EN = {44: [('0.63̅ ?', K(r'0.6\overline{3}') + '?')], 52: [('1/5', K(r'\dfrac{1}{5}'))]}
REP_HI = {44: [('0.6\\overline{3}', K(r'0.6\overline{3}'))], 52: [('\\frac{1}{5}', K(r'\dfrac{1}{5}'))]}
FIXED_STEM = {
 43: K(r'\dfrac{1}{2} + \dfrac{1}{6} + \dfrac{1}{12} + \dfrac{1}{20} + \dots + \dfrac{1}{90} = ?'),
}
FIXED_OPTS = {
 43: [K(r'\dfrac{9}{10}'), K(r'\dfrac{4}{5}'), K(r'\dfrac{7}{11}'), K(r'\dfrac{8}{13}')],
 44: [K(r'0.6\overline{4}'), K(r'0.6\overline{7}'), K(r'0.6\overline{1}'), K(r'0.6\overline{9}')],
 45: [K(r'\dfrac{18}{7}'), K(r'\dfrac{17}{9}'), K(r'\dfrac{20}{11}'), K(r'\dfrac{38}{13}')],
 47: [K('2 : 3'), K('3 : 5'), K('4 : 3'), K('3 : 8')],
}
KEY_FIX = {}
EN_EDIT = {
 35: [('What is the name of the artificial intelligence action plan launched by the Indian government in 2025?',
       'What is the name of the national artificial intelligence mission approved by the Union Cabinet in March 2024?')],
 37: [('Which scheme provides financial incentives to promote exports from SEZs?',
       'Which scheme provided financial incentives to promote exports from SEZs until 2020?')],
 39: [('Along with whom did Rani Lakshmi Bai fight with the British in Jhansi?',
       'Along with whom did Rani Lakshmi Bai of Jhansi fight against the British in 1857–58?')],
 50: [('If A is 5 times more than B,', 'If A is 6 times B,')],
 61: [('he decided to leave his friend to', 'he decided to leave his friend to _____.')],
 70: [('She stiches fine dresses', 'She stitches fine dresses')],
 73: [('waiting eagerly for the chief guest to arrive since two hours.', 'waiting eagerly <u>for the chief guest to arrive since two hours</u>.')],
 75: [('he was unable to secure position at', '<u>he was unable to secure position</u> at')],
}
HI_EDIT = {
 35: [('2025 में भारत सरकार द्वारा शुरू की गई कृत्रिम बुद्धिमत्ता (आर्टिफिशियल इंटेलिजेंस) कार्य योजना का क्या नाम है?',
       'मार्च 2024 में केंद्रीय मंत्रिमंडल द्वारा स्वीकृत राष्ट्रीय कृत्रिम बुद्धिमत्ता (आर्टिफिशियल इंटेलिजेंस) मिशन का क्या नाम है?')],
 37: [('कौन सी योजना SEZ (विशेष आर्थिक क्षेत्रों) से निर्यात को बढ़ावा देने के लिए वित्तीय प्रोत्साहन प्रदान करती है?',
       'कौन सी योजना 2020 तक SEZ (विशेष आर्थिक क्षेत्रों) से निर्यात को बढ़ावा देने के लिए वित्तीय प्रोत्साहन प्रदान करती थी?')],
 39: [('रानी लक्ष्मी बाई ने झांसी में अंग्रेजों के साथ किसके साथ मिलकर लड़ाई लड़ी थी?',
       'झांसी की रानी लक्ष्मी बाई ने 1857–58 में किसके साथ मिलकर अंग्रेजों के विरुद्ध लड़ाई लड़ी थी?')],
 50: [('यदि A, B से 5 गुना अधिक है,', 'यदि A, B का 6 गुना है,')],
}
# Q1 option D and Q69 option B are small images of text in the source -> typed
OPT_FIX = {1: {'': 'PC'}, 69: {'': 'in'}}
# Q65: the EN copy lost the misspelling (HI and GU copies have "Validictory")
OPT_FIX_EN = {65: {'Valedictory': 'Validictory'}}
OPT_FIX_HI = {}
HPD_STEM = {
 66: [("'अस्वस्थ '", "'अस्वस्थ'")],
 67: [("'आजाद '", "'आजाद'")],
 72: [('शब्दावली क्या होगाः', 'शब्दावली क्या होगी?')],
 74: [('पुलिस द्वारा किसी क्षेत्र की स्थिति का निरीक्षण करना क्या कहलाता है?',
       'पुलिस अधिकारी द्वारा किसी थाने, चौकी या क्षेत्र की व्यवस्था को मौके पर जाकर जाँचना-परखना क्या कहलाता है?')],
}
# HI Q64: "बीबी" is an accepted variant of बीवी -> made a clear misspelling so only the key B is correct
HPD_OPT = {64: {0: 'बीवि'}}

def edit(t, pair, n, tag):
    a, b = pair
    if a not in t: raise SystemExit(f'Q{n} {tag}: anchor missing {a!r}')
    return t.replace(a, b, 1)

def stem(q, n, lang):
    if n in FIXED_STEM: return FIXED_STEM[n]
    t = clean(q['text']).replace('\u200b', '')
    t = re.sub(r'\\\(\s*(.*?)\s*\\\)', lambda m: m.group(1), t)
    for pair in REP.get(n, []): t = edit(t, pair, n, lang)
    for pair in (REP_EN if lang == 'EN' else REP_HI).get(n, []): t = edit(t, pair, n, lang + '_REP')
    for pair in (EN_EDIT if lang == 'EN' else HI_EDIT).get(n, []): t = edit(t, pair, n, lang + '_EDIT')
    if '[BR]' in t and '||' not in t: t = t.replace('[BR]', '||', 1)
    if n in FIG: t = '[FIGURE-BASED] ' + t
    return t

def opts(q, n, lang):
    if n in FIG: return [f'(figure {i})' for i in range(1, 5)]
    if n in FIXED_OPTS: return FIXED_OPTS[n]
    out = []
    for x in q['opts']:
        v = clean(x).replace('\u200b', '')
        v = OPT_FIX.get(n, {}).get(v, v)
        v = (OPT_FIX_EN if lang == 'EN' else OPT_FIX_HI).get(n, {}).get(v, v)
        out.append(v)
    return out

def block(n, subj, concept, text, op, ans):
    return f"[Q{n}]\nSUBJECT: {subj}\nCONCEPT: {concept}\nTEXT: {text}\nA: {op[0]}\nB: {op[1]}\nC: {op[2]}\nD: {op[3]}\nANSWER: {ans}\n"

def header(lang): return f"# TRICKYSSC QUESTIONS\nEXAM: ssc-gd\nYEAR: 2026\nPAPER: {PAPER}\nLANG: {lang}\n"

# one passage for Q76-80 (all five copies identical); blanks rebuilt as ___A___ ... ___E___
PASSAGE_EN = clean(EN[75]['comp'])
for L in 'ABCDE':
    a = f'_____ {L} _____'
    assert PASSAGE_EN.count(a) == 1, a
    PASSAGE_EN = PASSAGE_EN.replace(a, f'___{L}___')

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
        op = [HPD_OPT.get(n, {}).get(k, clean(x).replace('\u200b', '')) for k, x in enumerate(q['opts'])]
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
    for need in ['D: PC\n', 'B: in\n', 'B: Validictory\n', '___A___', '___E___', 'friend to _____.', 'She stitches', 'March 2024', 'until 2020',
                 'against the British in 1857–58', 'A is 6 times B', '<u>for the chief guest to arrive since two hours</u>', '<u>he was unable to secure position</u>',
                 r'\( 0.6\overline{3} \)?', r'\( \dfrac{1}{5} \)']:
        assert need in en, need
    for bad in ['Valedictory', '_____ A', 'stiches', 'in 2025?', '5 times more', '0.63̅', '​', '\\frac{']:
        assert bad not in en, bad
    assert 'A: बीवि\n' in hp and "'अस्वस्थ'" in hp and "'आजाद'" in hp and 'होगी?' in hp and 'होगाः' not in hp and 'मौके पर जाकर' in hp
    assert hp.count('PASSAGE (Q76–Q80)') == 5 and 'उपरोक्त' not in hp and '​' not in hp
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['1']['opts'][3] == 'PC' and 'मार्च 2024' in h['35']['TEXT'] and '2020 तक' in h['37']['TEXT'] and 'B का 6 गुना' in h['50']['TEXT']
    assert h['43']['TEXT'].startswith('निम्नलिखित') and h['41']['TEXT'].startswith('निम्नलिखित') and r'\( 0.6\overline{3} \)' in h['44']['TEXT']
    assert r'\( \dfrac{1}{5} \)' in h['52']['TEXT'] and r'\( 2\dfrac{1}{3} \)' in h['45']['TEXT'] and '\\frac{' not in json.dumps(h)
    print('ok')
