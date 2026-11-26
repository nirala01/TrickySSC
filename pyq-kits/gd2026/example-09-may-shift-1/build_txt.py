import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-09-may-shift-1'
PAPER = 'SSC GD Constable 2026 May 09 Shift 1'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {11, 12, 18, 19}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 3:[('AI : GO :: FP : ? :: RG : XM', ana('AI : GO :: FP : ? :: RG : XM'))],
 5:[('HO : CH :: GS : ? :: MZ : HS', ana('HO : CH :: GS : ? :: MZ : HS'))],
 13:[('AZ205 : CB112 :: CB200 : ED107 :: XM999 : ?', ana('AZ205 : CB112 :: CB200 : ED107 :: XM999 : ?'))],
 14:[('DI30 : HC75 :: KR40 : OL100 :: ? : HL150', ana('DI30 : HC75 :: KR40 : OL100 :: ? : HL150'))],
 15:[('11 : 729 :: 15 : 2197 :: 23 : ?', K('11 : 729 :: 15 : 2197 :: 23 : ?'))],
 20:[('2 : 5', K('2 : 5'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 43: K(r'\sqrt{\dfrac{0.1225}{0.25}} = ?'),
 44: K(r'\dfrac{(4.2 + 3.8)^{2} + (4.2 - 3.8)^{2}}{4.2 \times 4.2 + 3.8 \times 3.8} = ?'),
 47: K(r'(1 + \sqrt{5})^{2} - (1 - \sqrt{5})^{2} - 14\sqrt{5} = ?'),
 48: K(r'1 + 2 + 3 + \ldots + 35 = ?'),
}
FIXED_STEM_L = {
 45: {'EN': r'If \( x = \sqrt{81} \div \sqrt{9} + \sqrt{36} \), then what is the value of 2x?',
      'HI': r'यदि \( x = \sqrt{81} \div \sqrt{9} + \sqrt{36} \) है, तो 2x का मान क्या है?'},
}
FIXED_OPTS = {
 47: ['0', K(r'8\sqrt{5}'), K(r'-8\sqrt{5}'), K(r'-10\sqrt{5}')],
}
KEY_FIX = {}
# Q40 statement II on its own line; Q63 the source underlined "indigenous fauna" as one span and all four words were
# correctly spelt — four separate underlines restored and the word the key (A) intends set to the misspelling "indigenious"
EN_EDIT = {
 40: [('I. Cerium II. Europium', 'I. Cerium[BR]II. Europium')],
 63: [('<u>indigenous fauna</u>', '<u>indigenious</u> <u>fauna</u>')],
}
HI_EDIT = {
 40: [('I. सीरियम (Cerium) II. यूरोपियम', 'I. सीरियम (Cerium)[BR]II. यूरोपियम')],
}
# Q63 A indigenous -> indigenious (see above); Q66 C "àl" (garbage in EN/HI/GU) -> "alder"; Q68 B "0ff" -> "off";
# Q76 C "graple" -> "grapple" (the keyed form; the passage itself has "grapple")
OPT_FIX = {}
OPT_FIX_EN = {63: {'indigenous': 'indigenious'}, 66: {'àl': 'alder'}, 68: {'0ff': 'off'}, 76: {'graple': 'grapple'}}
OPT_FIX_HI = {}
HPD_STEM = {
 61: [('नीचे दिए गये वाक्य में किस प्रकार की <u>अशुद्धि</u> है:[BR]', 'नीचे दिए गए वाक्य में किस प्रकार की अशुद्धि है?[BR]')],
 62: [('नीचे दिए गये वाक्य में किस प्रकार की <u>अशुद्धि</u> है:[BR]', 'नीचे दिए गए वाक्य में किस प्रकार की अशुद्धि है?[BR]')],
 63: [('निम्नलिखित में वाक्य के <u>शुद्ध</u> रूप का चयन कीजिए:', 'निम्नलिखित में से वाक्य के शुद्ध रूप का चयन कीजिए।')],
 # the old stem "जब कोई आदेश लिखित रूप में आता है" gave the key लिखित आदेश away
 65: [('जब कोई आदेश लिखित रूप में आता है, तो वह क्या होता है?', 'जब किसी वरिष्ठ अधिकारी का ऐसा निर्देश, जिसका पालन करना ज़रूरी हो, कागज़ पर लिखकर और हस्ताक्षर करके जारी किया जाता है, तो उसे क्या कहते हैं?')],
 # the old stem "आगंतुक का नाम दर्ज करता है" gave the key आगंतुक पंजीकरण away
 67: [('सुरक्षा कर्मी जब किसी आगंतुक का नाम दर्ज करता है, तो वह क्या कर रहा होता है?', 'सुरक्षा कर्मी जब प्रवेश द्वार पर बाहर से आने वाले व्यक्ति का नाम, पता और आने का कारण रजिस्टर में लिखता है, तो वह क्या कर रहा होता है?')],
 # "अपराध को दबाने के लिए झूठी कहानी" also fitted अपराध आवरण and झूठा बहाना
 72: [('जब कोई अभियुक्त अपने अपराध को दबाने के लिए झूठी कहानी बनाता है, तो वह क्या कहलाता है?', 'जब कोई अभियुक्त पूछताछ में ऐसी कहानी सुनाता है जो पूरी तरह उसके मन से गढ़ी गई हो और जिसका कोई आधार न हो, तो उस कहानी को क्या कहते हैं?')],
}
# Q71 B completed; Q72 C झूठा बहाना (also fitted) -> स्वीकारोक्ति
HPD_OPT = {71: {1: 'वह प्रणाली जहाँ से पूरे नेटवर्क की निगरानी की जाती है'}, 72: {2: 'स्वीकारोक्ति'}}

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

# one reading-comprehension passage for Q76-80 (all five copies identical; no instruction line)
PASSAGE_EN = clean(EN[75]['comp'])
assert all(clean(EN[i]['comp']) == PASSAGE_EN for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
assert PASSAGE_EN.startswith("In the annals of human achievement")
HPD_PASSAGE = clean(HI[95]['comp'])
assert all(clean(HI[i]['comp']) == HPD_PASSAGE for i in range(95, 100)) and all(not HI[i]['comp'] for i in range(80, 95))

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
        if 76 <= n <= 80:
            t = 'PASSAGE (Q76–Q80): ' + HPD_PASSAGE + ' || ' + t
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
    for need in [r'\( \text{AI} : \text{GO} :: \text{FP}', r'\( \text{HO} : \text{CH}', r'\( \text{AZ205} : \text{CB112}', r'\( \text{DI30} : \text{HC75}',
                 r'\( 11 : 729 :: 15 : 2197 :: 23 : ? \)', r'is \( 2 : 5 \).', r'A: \( 13 : 22 \)', r'B: \( 19 : 7 \)', r'B: \( 39 : 50 \)',
                 r'\sqrt{\dfrac{0.1225}{0.25}}', r'\dfrac{(4.2 + 3.8)^{2}', r'If \( x = \sqrt{81} \div', r'D: \( -10\sqrt{5} \)', r'\ldots + 35',
                 'I. Cerium[BR]II. Europium', '<u>indigenious</u> <u>fauna</u> and <u>flora</u>', 'A: indigenious\n', 'C: alder\n', 'B: off\n', 'C: grapple\n',
                 'TEXT: [FIGURE-BASED] Two figures', 'TEXT: [FIGURE-BASED] In the following figure series', "PASSAGE (Q76–Q80): In the annals"]:
        assert need in en, need
    for bad in ['\\frac{', '​', 'A: \n', 'C: \n', 'D: \n', '\\rm', 'àl', '0ff', 'graple', '<u>indigenous', '......', '14√5']:
        assert bad not in en, bad
    assert en.count('[FIGURE-BASED]') == 4 and en.count('(figure 1)') == 4 and en.count('PASSAGE (Q76–Q80)') == 5
    assert hp.count('PASSAGE (Q76–Q80): आंतरिक सुरक्षा केवल') == 5 and '​' not in hp and 'गये' not in hp and '<u>' not in hp
    for need in ['किस प्रकार की अशुद्धि है?||मेरे को', 'किस प्रकार की अशुद्धि है?||तेरे को', 'निम्नलिखित में से वाक्य के शुद्ध रूप का चयन कीजिए।', 'हस्ताक्षर करके जारी',
                 'आने का कारण रजिस्टर में', 'उसके मन से गढ़ी गई', 'C: स्वीकारोक्ति\n', 'निगरानी की जाती है\n']:
        assert need in hp, need
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['11']['opts'] == ['(figure 1)', '(figure 2)', '(figure 3)', '(figure 4)'] and 'I. सीरियम (Cerium)[BR]II.' in h['40']['TEXT']
    assert h['43']['TEXT'].startswith('निम्नलिखित') and h['45']['TEXT'].startswith('यदि \\(') and h['47']['opts'][3] == r'\( -10\sqrt{5} \)' and h['58']['opts'][1] == r'\( 19 : 7 \)'
    assert r'\( \text{AI}' in h['3']['TEXT'] and r'\( 2 : 5 \)' in h['20']['TEXT']
    assert '\\frac' not in json.dumps(h) and '\\rm' not in json.dumps(h)
    print('ok')
