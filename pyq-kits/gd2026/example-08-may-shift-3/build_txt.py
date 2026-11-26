import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-08-may-shift-3'
PAPER = 'SSC GD Constable 2026 May 08 Shift 3'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {9, 10}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 11:[('QR75 : NO28 :: ? : BS46 :: MN99 : JK52', ana('QR75 : NO28 :: ? : BS46 :: MN99 : JK52'))],
 12:[('KLP8 : FGV100 :: MSB5 : HNH49 :: ZXO9 : ?', ana('KLP8 : FGV100 :: MSB5 : HNH49 :: ZXO9 : ?'))],
 13:[('2809 : 2761 :: ? : 5520 :: 2487 : 2439', K('2809 : 2761 :: ? : 5520 :: 2487 : 2439'))],
 14:[('27 : 841 :: 21 : 529 :: 17 : ?', K('27 : 841 :: 21 : 529 :: 17 : ?'))],
 52:[('3 : 7', K('3 : 7'))],
 57:[('1/3', K(r'\dfrac{1}{3}'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 44: K(r'\left(\dfrac{\sqrt{0.0169}}{1.3}\right) \times \left(\dfrac{0.18}{\sqrt{3.24}}\right) \times \left(\dfrac{0.24}{\sqrt{0.0576}}\right) = ?'),
 48: K(r'\dfrac{(3.452)^{2} - (2.948)^{2}}{0.504} = ?'),
}
FIXED_STEM_L = {
 45: {'EN': r'If \( x = \sqrt{169} \times \sqrt{81} \times \sqrt{121} \), then what is the value of x?',
      'HI': r'यदि \( x = \sqrt{169} \times \sqrt{81} \times \sqrt{121} \) है, तो x का मान क्या है?'},
}
FIXED_OPTS = {
 49: [K(r'7\sqrt{8}'), K(r'5\sqrt{13}'), K(r'6\sqrt{17}'), K(r'9\sqrt{12}')],
 58: [K(r'\dfrac{49}{17}'), K(r'\dfrac{45}{17}'), K(r'\dfrac{41}{17}'), '3'],
}
KEY_FIX = {}
# Q35: Rajasthan had 5.66% of India's population in Census 2011, so the 5.5% option is an approximation — "about" added
# Q76: the passage is above the question, not "below"
EN_EDIT = {
 35: [('has only _____ of', 'has only about _____ of')],
 76: [('according to the descriptions given below?', 'according to the passage?')],
}
HI_EDIT = {
 35: [('का केवल _____ है।', 'का केवल लगभग _____ है।')],
}
# Q39 B "Dada Bhai Naurauji" -> "Dadabhai Naoroji" (HI already दादा भाई नौरोजी); Q65 A "Criticism" -> "Critisism"
# (all four EN words were correctly spelt; the GU copy keeps the misspelling the key intends)
OPT_FIX = {}
OPT_FIX_EN = {39: {'Dada Bhai Naurauji': 'Dadabhai Naoroji'}, 65: {'Criticism': 'Critisism'}}
OPT_FIX_HI = {}
HPD_STEM = {
 61: [('किस चिन्ह का प्रयोग हुआ है-[BR]', 'किस चिह्न का प्रयोग हुआ है?[BR]')],
 # "लड़की ने जोर से हँस दी" — the real error was the ने with intransitive हँसना (a कारक error, not among the options);
 # sentence set to a gender-agreement error so the key लिंग is right
 62: [('लड़की ने जोर से हँस दी,', 'लड़की जोर से हँस दिया,')],
 64: [('का सही तकनीकी शब्द है:', 'का सही तकनीकी (अंग्रेज़ी) शब्द क्या है?')],
 # "पूर्व योजना" also fitted आकस्मिक योजना (a contingency plan is also made in advance)
 69: [('सुरक्षा व्यवस्था की पूर्व योजना क्या कहलाती है?', 'सुरक्षा व्यवस्था के लक्ष्य और उपाय पहले से तय करने वाली समग्र योजना क्या कहलाती है?')],
 72: [('<u>सही</u> पारिभाषिक शब्दावली क्या होगा:', 'सही पारिभाषिक शब्दावली क्या होगी?')],
 78: [('सड़क या क्षेत्र को रोकने के लिए लगाया गया अवरोधक', 'सड़क या क्षेत्र में आवागमन रोकने के लिए लगाया गया अस्थायी अवरोधक')],
 # the old stem "भविष्य की कार्य योजना" gave the key योजना away
 79: [('पुलिस द्वारा भविष्य की कार्य योजना को क्या कहा जाता है?', 'पुलिस द्वारा भविष्य में किए जाने वाले कार्यों की पहले से बनाई गई रूपरेखा क्या कहलाती है?')],
}
# Q62 D क्रिया (हँस दिया is also a verb-form error) -> वचन; Q63 B सर्वनाम (सब is a pronoun, so arguable) -> क्रिया;
# Q78 D रुकावट (a plain synonym of अवरोधक) -> पहरा
HPD_OPT = {62: {3: 'वचन'}, 63: {1: 'क्रिया'}, 78: {3: 'पहरा'}}

def edit(t, pair, n, tag):
    a, b = pair
    if a not in t: raise SystemExit(f'Q{n} {tag}: anchor missing {a!r}')
    return t.replace(a, b, 1)

def stem(q, n, lang):
    if n in FIXED_STEM: return FIXED_STEM[n]
    if n in FIXED_STEM_L: return FIXED_STEM_L[n][lang]
    t = clean(q['text']).replace('​', '')
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
    for k, x in enumerate(q['opts']):
        v = clean(x).replace('​', '').strip()
        v = OPT_FIX.get(n, {}).get(v, v)
        fx = {**OPT_FIX.get(n, {}), **(OPT_FIX_EN if lang == 'EN' else OPT_FIX_HI).get(n, {})}
        v = fx.get(v + '#' + 'ABCD'[k], fx.get(v, v))
        if re.fullmatch(r'\d+ : \d+', v): v = K(v)
        out.append(v)
    return out

def block(n, subj, concept, text, op, ans):
    return f"[Q{n}]\nSUBJECT: {subj}\nCONCEPT: {concept}\nTEXT: {text}\nA: {op[0]}\nB: {op[1]}\nC: {op[2]}\nD: {op[3]}\nANSWER: {ans}\n"

def header(lang): return f"# TRICKYSSC QUESTIONS\nEXAM: ssc-gd\nYEAR: 2026\nPAPER: {PAPER}\nLANG: {lang}\n"

# one reading-comprehension passage for Q76-80 (all five copies identical; instruction line dropped)
INSTR = 'Read the following passage carefully and answer the questions based on the passage:[BR]'
PASSAGE_EN = clean(EN[75]['comp'])
assert all(clean(EN[i]['comp']) == PASSAGE_EN for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
assert PASSAGE_EN.startswith(INSTR)
PASSAGE_EN = PASSAGE_EN[len(INSTR):]
assert PASSAGE_EN.startswith("India's Act East Policy")
HPD_PASSAGE = clean(HI[92]['comp'])
assert all(clean(HI[i]['comp']) == HPD_PASSAGE for i in range(92, 97)) and all(not HI[i]['comp'] for i in list(range(80, 92)) + [97, 98, 99])

def build_en():
    out = [header('EN')]
    for i in range(80):
        q = EN[i]; n = i + 1
        t = stem(q, n, 'EN')
        if q['comp']:
            t = 'PASSAGE (Q76–Q80): ' + PASSAGE_EN + ' || ' + t
        out.append(block(n, SUBJ[q['si']], CON_EN[n], t, opts(q, n, 'EN'), KEY_FIX.get(n, 'ABCD'[q['cidx']])))
    return '\n'.join(out)

def build_hi_partd():
    out = [header('HI')]
    for i in range(80, 100):
        q = HI[i]; n = i - 19
        t = clean(q['text'])
        for pair in HPD_STEM.get(n, []): t = edit(t, pair, n, 'HPD')
        if '[BR]' in t: t = t.replace('[BR]', '||', 1)
        if 73 <= n <= 77:
            t = 'PASSAGE (Q73–Q77): ' + HPD_PASSAGE + ' || ' + t
        op = [HPD_OPT.get(n, {}).get(k, clean(x).replace('​', '')) for k, x in enumerate(q['opts'])]
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
    assert all(EN[i]['cidx'] == HI[i]['cidx'] == o['gu'][i]['cidx'] for i in range(100)), 'en/hi/gu keys differ'
    assert all(EN[i]['si'] == HI[i]['si'] for i in range(100))
    assert all(len(q['opts']) == 4 for q in EN[:80] + HI[80:])
    open(f'{HERE}/out/{PREFIX}-questions-EN.txt', 'w', encoding='utf-8').write(build_en())
    open(f'{HERE}/out/{PREFIX}-questions-HI-partD.txt', 'w', encoding='utf-8').write(build_hi_partd())
    json.dump(hi_q1_60(), open(f'{HERE}/hi_q1_60.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    en = open(f'{HERE}/out/{PREFIX}-questions-EN.txt', encoding='utf-8').read()
    hp = open(f'{HERE}/out/{PREFIX}-questions-HI-partD.txt', encoding='utf-8').read()
    for need in [r'\( \text{QR75} : \text{NO28} :: ? : \text{BS46}', r'\( \text{KLP8} : \text{FGV100}', r'\( 2809 : 2761 :: ? : 5520 :: 2487 : 2439 \)', r'\( 27 : 841 :: 21 : 529 :: 17 : ? \)',
                 r'is \( 3 : 7 \) and', r'empty \( \dfrac{1}{3} \) part', r'\left(\dfrac{\sqrt{0.0169}}{1.3}\right)', r'\( \dfrac{(3.452)^{2}', r'A: \( 7\sqrt{8} \)', r'B: \( \dfrac{45}{17} \)', 'D: 3\n',
                 r'A: \( 5 : 3 \)', 'B: Dadabhai Naoroji\n', 'A: Critisism\n', 'has only about _____ of', 'according to the passage?',
                 'TEXT: [FIGURE-BASED] Two figures', "PASSAGE (Q76–Q80): India's Act East Policy"]:
        assert need in en, need
    for bad in ['\\frac{', '​', 'A: \n', 'C: \n', 'D: \n', '\\rm', 'Naurauji', 'A: Criticism', 'given below?', '7√8', 'Read the following passage']:
        assert bad not in en, bad
    assert en.count('[FIGURE-BASED]') == 2 and en.count('(figure 1)') == 2 and en.count('PASSAGE (Q76–Q80)') == 5
    assert hp.count('PASSAGE (Q73–Q77): जाँच एजेंसियों में जवाबदेही') == 5 and '​' not in hp and 'चिन्ह' not in hp
    for need in ['किस चिह्न का प्रयोग हुआ है?||तुम कहाँ', 'लड़की जोर से हँस दिया,', 'D: वचन\n', 'B: क्रिया\n', 'तकनीकी (अंग्रेज़ी) शब्द क्या है?', 'समग्र योजना क्या कहलाती है?',
                 'सही पारिभाषिक शब्दावली क्या होगी?||ध्यान देने योग्य', 'अस्थायी अवरोधक', 'D: पहरा\n', 'पहले से बनाई गई रूपरेखा']:
        assert need in hp, need
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['9']['opts'] == ['(figure 1)', '(figure 2)', '(figure 3)', '(figure 4)'] and 'केवल लगभग _____' in h['35']['TEXT']
    assert h['44']['TEXT'].startswith('निम्नलिखित') and h['45']['TEXT'].startswith('यदि \\(') and h['49']['opts'][0] == r'\( 7\sqrt{8} \)' and h['46']['opts'][1] == r'\( 3 : 2 \)'
    assert r'\( \text{QR75}' in h['11']['TEXT'] and r'\( 3 : 7 \)' in h['52']['TEXT'] and r'\dfrac{1}{3}' in h['57']['TEXT'] and h['58']['opts'][1] == r'\( \dfrac{45}{17} \)'
    assert '\\frac' not in json.dumps(h) and '\\rm' not in json.dumps(h)
    print('ok')
