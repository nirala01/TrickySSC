import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-09-may-shift-2'
PAPER = 'SSC GD Constable 2026 May 09 Shift 2'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {9, 10}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 11:[('AJ150 : YH243 :: KG300 : IE393 :: SL310 : ?', ana('AJ150 : YH243 :: KG300 : IE393 :: SL310 : ?'))],
 12:[('ZYX160 : VUS320 :: ? : ATK240 :: JLR180 : FHM360', ana('ZYX160 : VUS320 :: ? : ATK240 :: JLR180 : FHM360'))],
 13:[('6276 : 6235 :: 3592 : 3551 :: ? : 7054', K('6276 : 6235 :: 3592 : 3551 :: ? : 7054'))],
 14:[('324 : 159 :: 1710 : 852 :: 680 : ?', K('324 : 159 :: 1710 : 852 :: 680 : ?'))],
 47:[('4/5', K(r'\dfrac{4}{5}'))],
 57:[('1/6', K(r'\dfrac{1}{6}'))],
 58:[('1/2', K(r'\dfrac{1}{2}'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 44: K(r'\dfrac{(2.5)^{3} - (1.5)^{3} - 0.25}{(2.5)^{2} + (1.5)^{2} - 7.5} = ?'),
 46: K(r'\dfrac{\sqrt{98} - \sqrt{147}}{\sqrt{18} - \sqrt{27}} = ?'),
 48: K(r'(325 - 275)^{2} + 4 \times 325 \times 275 = ?'),
}
FIXED_STEM_L = {
 43: {'EN': r'Find the HCF and LCM of the fractions \( \dfrac{3}{8} \), \( \dfrac{5}{12} \) and \( \dfrac{7}{18} \).',
      'HI': r'भिन्नों \( \dfrac{3}{8} \), \( \dfrac{5}{12} \) और \( \dfrac{7}{18} \) का HCF और LCM ज्ञात कीजिए।'},
 45: {'EN': r'If \( x = \sqrt{289} \times \sqrt{225} + \sqrt{144} \), then what is the value of 2x?',
      'HI': r'यदि \( x = \sqrt{289} \times \sqrt{225} + \sqrt{144} \) है, तो 2x का मान क्या है?'},
}
def HL(h, l): return r'HCF = \( \dfrac{1}{' + h + r'} \), LCM = \( \dfrac{' + l[0] + '}{' + l[1] + r'} \)'
FIXED_OPTS = {
 43: [HL('72', ('105', '2')), HL('36', ('105', '4')), HL('24', ('35', '2')), HL('72', ('35', '2'))],
 46: [K(r'\dfrac{7}{3}'), K(r'\dfrac{3}{7}'), K(r'\dfrac{7}{4}'), K(r'\dfrac{4}{3}')],
 58: ['2.5', K(r'\dfrac{8}{3}'), '3', K(r'\dfrac{10}{3}')],
}
KEY_FIX = {}
# Q26/Q33/Q40 statement II on its own line (EN + HI)
EN_EDIT = {
 26: [('a school. II. Devadana', 'a school.[BR]II. Devadana')],
 33: [('I. Liver II. Gall bladder', 'I. Liver[BR]II. Gall bladder')],
 40: [('I. Sikkim II. Mizoram', 'I. Sikkim[BR]II. Mizoram')],
 # Q78: B and C were close paraphrases of the passage too; stem now says "according to the passage"
 78: [('Why are Pacific Salmon', 'According to the passage, why are Pacific Salmon')],
}
HI_EDIT = {
 26: [('के लिए भूमि। II. देवदान', 'के लिए भूमि।[BR]II. देवदान')],
 33: [('I. यकृत II. पित्ताशय', 'I. यकृत[BR]II. पित्ताशय')],
 40: [('I. सिक्किम II. मिजोरम', 'I. सिक्किम[BR]II. मिजोरम')],
}
# Q65 had NO misspelt word — C "Ludicrous" -> "Ludicurous" (the GU copy keeps the misspelling the key intends)
# Q71 official key C was "of" ("evidence ___ him" needs "against") — options C/D swapped, key letter C kept
# Q78 B "within freshwater and marine ecosystems" (a near-paraphrase of the passage) -> "only within marine ecosystems"
OPT_FIX = {}
OPT_FIX_EN = {65: {'Ludicrous': 'Ludicurous'}, 71: {'of': 'against', 'against': 'of'},
              78: {'Pacific Salmon influence food-web structures and processes within freshwater and marine ecosystems.':
                   'Pacific Salmon influence food-web structures and processes only within marine ecosystems.'}}
OPT_FIX_HI = {}
HPD_STEM = {
 61: [('निम्न में से <u>शुद्ध</u> शब्द कौन-सा है?', 'निम्न में से शुद्ध शब्द कौन-सा है?')],
 62: [('मुझे मजा आती है, वाक्य में किस प्रकार की <u>अशुद्धि</u> है?', '"मुझे मजा आती है" — इस वाक्य में किस प्रकार की अशुद्धि है?')],
 63: [('रामायण का टीका, वाक्य में कौन-सी <u>अशुद्धि</u> है?', '"रामायण का टीका" — इस वाक्यांश में कौन-सी अशुद्धि है?')],
 64: [("'अभियोजन की रणनीति' का <u>सही</u> शब्द है?", "'अभियोजन की रणनीति' का सही अंग्रेज़ी शब्द है?")],
 # "कार्य प्रणाली" also fitted नीति
 67: [('सुरक्षा कर्मियों के लिए तय की गई कार्य प्रणाली क्या कहलाती है?', 'सुरक्षा कर्मियों के लिए किसी कार्य को करने का पहले से तय, चरण-दर-चरण तरीका क्या कहलाता है?')],
 # the old stem "विधिवत पूछताछ" gave the key पूछताछ away
 69: [('पुलिस द्वारा संदिग्ध व्यक्ति से की गई विधिवत पूछताछ को क्या कहते हैं?', 'पुलिस द्वारा किसी संदिग्ध व्यक्ति से अपराध के बारे में विधिवत सवाल-जवाब करने को क्या कहते हैं?')],
 72: [('नीचे दिए गए शब्द की <u>सही</u> पारिभाषिक शब्दावली क्या होगा:', 'नीचे दिए गए शब्द की सही पारिभाषिक शब्दावली क्या होगी?')],
 74: [('पहला चरण क्या होता है?', 'जोखिम मूल्यांकन में पहला चरण क्या होता है?')],
 75: [('विश्लेषण किसका किया जाता है?', 'खतरों की पहचान के बाद किसका विश्लेषण किया जाता है?')],
 # "जाँच और मूल्यांकन" also fitted निरीक्षण / जांच
 79: [('पुलिस कार्य की जाँच और मूल्यांकन को क्या कहा जाता है?', 'किसी अवधि में किए गए पुलिस कार्य को दोबारा देखकर उसकी कमियों और उपलब्धियों का आकलन करना क्या कहलाता है?')],
 # "कार्य रिकॉर्ड" is literally अभिलेख, not the key रजिस्टर
 80: [('पुलिस द्वारा बनाए गए कार्य रिकॉर्ड क्या कहलाते हैं?', 'पुलिस थाने में रोज़ के कार्य और घटनाएँ क्रम से लिखने के लिए रखी जाने वाली बंधी हुई पुस्तक क्या कहलाती है?')],
}
# Q61 D "आवाारा" (doubled matra) -> "आवरा"; Q78 C अभिलेखन (also means officially recording) -> अन्वेषण (key पंजीकरण)
HPD_OPT = {61: {3: 'आवरा'}, 78: {2: 'अन्वेषण'}}

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

# one reading-comprehension passage for Q76-80 (all five copies identical); instruction line dropped
INSTR = 'Read the following passage carefully and answer the questions based on the passage:[BR]'
assert all(clean(EN[i]['comp']) == clean(EN[75]['comp']) for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
PASSAGE_EN = clean(EN[75]['comp'])
assert PASSAGE_EN.startswith(INSTR); PASSAGE_EN = PASSAGE_EN[len(INSTR):]
assert PASSAGE_EN.startswith("The Pacific Salmon represent")
HPD_PASSAGE = clean(HI[92]['comp'])
assert all(clean(HI[i]['comp']) == HPD_PASSAGE for i in range(92, 97)) and all(not HI[i]['comp'] for i in list(range(80, 92)) + list(range(97, 100)))

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
    for need in [r'\( \text{AJ150} : \text{YH243}', r'\( \text{ZYX160} : \text{VUS320} :: ? :', r'\( 6276 : 6235 :: 3592', r'\( 324 : 159 :: 1710',
                 r'A: \( 3 : 5 \)', r'D: \( 1 : 3 \)', r'C: \( 3 : 7 \)', r'\dfrac{(2.5)^{3}', r'\dfrac{\sqrt{98}', r'4 \times 325 \times 275', r'If \( x = \sqrt{289} \times',
                 r'A: HCF = \( \dfrac{1}{72} \), LCM = \( \dfrac{105}{2} \)', r'B: \( \dfrac{8}{3} \)', r'is \( \dfrac{4}{5} \) of', r'empty \( \dfrac{1}{6} \) part',
                 'a school.[BR]II. Devadana', 'I. Liver[BR]II. Gall', 'I. Sikkim[BR]II. Mizoram', 'C: Ludicurous\n', 'C: against\nD: of\n', 'only within marine ecosystems.',
                 'According to the passage, why are', 'TEXT: [FIGURE-BASED] Two figures', "PASSAGE (Q76–Q80): The Pacific Salmon"]:
        assert need in en, need
    for bad in ['\\frac{', '​', 'A: \n', 'C: \n', 'D: \n', '\\rm', 'Read the following passage', 'C: Ludicrous', '3/8', '7/3']:
        assert bad not in en, bad
    assert en.count('[FIGURE-BASED]') == 2 and en.count('(figure 1)') == 2 and en.count('PASSAGE (Q76–Q80)') == 5
    assert hp.count('PASSAGE (Q73–Q77): आंतरिक सुरक्षा में जोखिम') == 5 and '​' not in hp and '<u>' not in hp
    for need in ['D: आवरा\n', 'C: अन्वेषण\n', 'सही अंग्रेज़ी शब्द', 'चरण-दर-चरण तरीका', 'सवाल-जवाब', 'शब्दावली क्या होगी?||अधिसूचना', 'बंधी हुई पुस्तक', 'दोबारा देखकर',
                 'जोखिम मूल्यांकन में पहला चरण', 'खतरों की पहचान के बाद']:
        assert need in hp, need
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['9']['opts'] == ['(figure 1)', '(figure 2)', '(figure 3)', '(figure 4)'] and 'I. सिक्किम[BR]II. मिजोरम' in h['40']['TEXT']
    assert h['44']['TEXT'].startswith('निम्नलिखित') and h['45']['TEXT'].startswith('यदि \\(') and h['43']['opts'] == [HL('72', ('105', '2')), HL('36', ('105', '4')), HL('24', ('35', '2')), HL('72', ('35', '2'))]
    assert r'\( \text{AJ150}' in h['11']['TEXT'] and h['60']['opts'][3] == r'\( 1 : 3 \)' and h['71' if False else '58']['opts'][1] == r'\( \dfrac{8}{3} \)'
    assert '\\frac' not in json.dumps(h) and '\\rm' not in json.dumps(h)
    print('ok')
