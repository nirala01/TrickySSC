import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/x/s3004_3.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-30-apr-shift-3'
PAPER = 'SSC GD Constable 2026 Apr 30 Shift 3'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {11, 12}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    out = []
    for tok in s.split(' '):
        out.append(T(tok) if re.search('[A-Z]', tok) else tok)
    return K(' '.join(out))
REP = {
 1: [('? : WW :: ON : MG :: UC : SV', ana('? : WW :: ON : MG :: UC : SV'))],
 13:[('AF150 : ZE270 :: ? : JP190 :: TL200 : SK320', ana('AF150 : ZE270 :: ? : JP190 :: TL200 : SK320'))],
 14:[('LM230 : ER330 :: JK420 : ? :: TU310 : MZ410', ana('LM230 : ER330 :: JK420 : ? :: TU310 : MZ410'))],
 15:[('4543 : ? :: 6368 : 6318 :: 6850 : 6800', K('4543 : ? :: 6368 : 6318 :: 6850 : 6800'))],
 16:[('347 : 685 :: ? : 1903 :: 610 : 1211', K('347 : 685 :: ? : 1903 :: 610 : 1211'))],
 48:[('3/4', K(r'\dfrac{3}{4}')), ('6/8', K(r'\dfrac{6}{8}')), ('9/10', K(r'\dfrac{9}{10}'))],
 52:[('5 : 4', K('5 : 4'))],
 53:[('3/5', K(r'\dfrac{3}{5}'))],
}
FIXED_STEM = {
 44: K(r'(2.5)^{2} \times 2.5 - 3 \times 0.5 \times (2.5)^{2} + 3 \times 2.5 \times (0.5)^{2} - (0.5)^{3} = ?'),
}
FIXED_OPTS = {
 48: [K(r'\dfrac{9}{2}'), K(r'\dfrac{18}{2}'), K(r'\dfrac{18}{5}'), K(r'\dfrac{27}{4}')],
}
KEY_FIX = {}
EN_EDIT = {
 33: [('in February 2025', 'in November 2024')],
 34: [('The Manmohan Singh Committee (1991) is known for:', 'The economic reforms of 1991, launched under Finance Minister Manmohan Singh, are mainly known for:')],
 38: [('About ______ of children in India aged 6-23 months lack diversity in diet as suggested by the World Health Organization in 2024.',
       'According to a study published in 2024, about ______ of children in India aged 6-23 months lack the diversity in diet suggested by the World Health Organization.')],
 63: [('invested a considerable amount', 'invested a <u>considerable</u> amount')],
 73: [('states have presented their reports on', 'states <u>have presented their reports</u> on')],
 74: [('some milk. D. They looked', 'some milk.[BR]D. They looked')],
 75: [("She didn't study for the test,", "<u>She didn't study for the test</u>,")],
 80: [('the word in (E): (heritage).', 'the word in (E) as it is used in the passage: (heritage).')],
}
HI_EDIT = {
 33: [('फरवरी 2025 में', 'नवंबर 2024 में')],
 34: [('मनमोहन सिंह समिति (1991) को किसके लिए जाना जाता है:', 'वित्त मंत्री मनमोहन सिंह के नेतृत्व में शुरू किए गए 1991 के आर्थिक सुधार मुख्य रूप से किसके लिए जाने जाते हैं:')],
 38: [('विश्व स्वास्थ्य संगठन द्वारा 2024 में दिए गए सुझाव के अनुसार, भारत में 6-23 महीने की उम्र के लगभग ______ बच्चों के आहार में विविधता की कमी है।',
       '2024 में प्रकाशित एक अध्ययन के अनुसार, भारत में 6-23 महीने की उम्र के लगभग ______ बच्चों के आहार में विश्व स्वास्थ्य संगठन द्वारा सुझाई गई विविधता की कमी है।')],
}
# Q7 option C is an image of the word UNIFORM in the source (EN + HI) -> typed as text
OPT_FIX = {7: {'': 'UNIFORM'}}
# Q65: the EN copy lost the misspelling (HI and GU copies have "Wrechedness"); Q72 misprints
OPT_FIX_EN = {65: {'Wretchedness': 'Wrechedness'}, 72: {'0n': 'on', 'ãI': 'at'}}
OPT_FIX_HI = {}
HPD_STEM = {
 72: [('<u>सही</u>', 'सही'), ('शब्दावली क्या होगी:', 'शब्दावली क्या होगी?')],
 74: [('पुलिस द्वारा बनाए गए कार्य नियम क्या कहलाते हैं?', 'पुलिस विभाग के कार्य-नियमों की संकलित पुस्तक क्या कहलाती है?')],
 75: [('पुलिस द्वारा अपराध रोकने के लिए उठाया गया कदम क्या कहलाता है?', 'अपराध होने पर पुलिस द्वारा अपराधियों के विरुद्ध उठाया गया कदम क्या कहलाता है?')],
}
HPD_OPT = {63: {3: 'ढ़कना'}, 77: {2: 'शिक्षा का विकास'}, 80: {0: 'व्यापार बढ़ाना'}}

def edit(t, pair, n, tag):
    a, b = pair
    if a not in t: raise SystemExit(f'Q{n} {tag}: anchor missing {a!r}')
    return t.replace(a, b, 1)

def stem(q, n, lang):
    if n in FIXED_STEM: return FIXED_STEM[n]
    t = clean(q['text']).replace('\u200b', '')
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
        v = clean(x).replace('\u200b', '')
        v = OPT_FIX.get(n, {}).get(v, v)
        v = (OPT_FIX_EN if lang == 'EN' else OPT_FIX_HI).get(n, {}).get(v, v)
        out.append(v)
    return out

def block(n, subj, concept, text, op, ans):
    return f"[Q{n}]\nSUBJECT: {subj}\nCONCEPT: {concept}\nTEXT: {text}\nA: {op[0]}\nB: {op[1]}\nC: {op[2]}\nD: {op[3]}\nANSWER: {ans}\n"

def header(lang): return f"# TRICKYSSC QUESTIONS\nEXAM: ssc-gd\nYEAR: 2026\nPAPER: {PAPER}\nLANG: {lang}\n"

# one passage for Q76-80 (Q76's copy); blanks D and E carry the tested words, shown as (D) <u>word</u>
PASSAGE_EN = clean(EN[75]['comp'])
for a, b in [('______ A ______', '___A___'), ('______ B ______', '___B___'), ('______ C ______', '___C___'),
             ('______ D ______ (vibrant)', '(D) <u>vibrant</u>'), ('______ E ______ (heritage)', '(E) <u>heritage</u>')]:
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
            p = re.sub(r'\[BR\]उपरोक्त गद्यांश के आधार पर प्रश्न का उत्तर दें:\s*$', '', clean(q['comp'])).replace('रहता है है कि', 'रहता है कि')
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
    for need in ['C: UNIFORM\n', 'C: Wrechedness\n', 'A: on\n', 'C: at\n', '(D) <u>vibrant</u>', '(E) <u>heritage</u>', '<u>considerable</u>',
                 '<u>have presented their reports</u>', "<u>She didn't study for the test</u>", 'milk.[BR]D. They looked', 'in November 2024',
                 'economic reforms of 1991', 'According to a study published in 2024', 'as it is used in the passage']:
        assert need in en, need
    for bad in ['February 2025', 'Wretchedness', '0n\n', 'ãI', '______ A', 'Committee (1991)', '​']:
        assert bad not in en, bad
    assert 'D: ढ़कना\n' in hp and 'C: शिक्षा का विकास\n' in hp and 'A: व्यापार बढ़ाना\n' in hp and '<u>' not in hp and 'होगी?' in hp
    assert 'संकलित पुस्तक' in hp and 'अपराधियों के विरुद्ध' in hp and 'है है' not in hp and '​' not in hp
    assert hp.count('PASSAGE (Q76–Q80)') == 5
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['7']['opts'][2] == 'UNIFORM' and 'नवंबर 2024' in h['33']['TEXT'] and '1991 के आर्थिक सुधार' in h['34']['TEXT']
    assert h['44']['TEXT'].startswith('निम्नलिखित') and h['41']['TEXT'].startswith('निम्नलिखित') and h['48']['opts'][0].startswith('\\(')
    print('ok')
