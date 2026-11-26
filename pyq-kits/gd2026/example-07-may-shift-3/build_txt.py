import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-07-may-shift-3'
PAPER = 'SSC GD Constable 2026 May 07 Shift 3'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {11, 12, 18, 19}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 3:[('? : DK :: PS : SX :: XT : AY', ana('? : DK :: PS : SX :: XT : AY'))],
 4:[('VA : BZ :: GY : ? :: LI : RR', ana('VA : BZ :: GY : ? :: LI : RR'))],
 13:[('KO825 : HK425 :: HF916 : EB516 :: ? : CT428', ana('KO825 : HK425 :: HF916 : EB516 :: ? : CT428'))],
 14:[('GKN11 : CGJ121 :: LMF13 : HIB169 :: OSR15 : ?', ana('GKN11 : CGJ121 :: LMF13 : HIB169 :: OSR15 : ?'))],
 15:[('608 : ? :: 13 : 242 :: 138 : 367', K('608 : ? :: 13 : 242 :: 138 : 367'))],
 20:[('7 : 12', K('7 : 12'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 44: K(r'(5.1)^{2} \times 5.1 - 3 \times 0.1 \times (5.1)^{2} + 3 \times 5.1 \times (0.1)^{2} - (0.1)^{3} = ?'),
 45: K(r'(\sqrt{6} + \sqrt{2})^{2} + (\sqrt{6} - \sqrt{2})^{2} = ?'),
 47: K(r'(9)^{3} + (7)^{3} + 3 \times 9 \times 7 \times 16 = ?'),
 50: K(r'40 \times (25^{2} + 15^{2} - 450) = ?'),
}
FIXED_STEM_L = {
 48: {'EN': r'If \( x = \dfrac{2 + \sqrt{6}}{2 - \sqrt{6}} \), \( y = \dfrac{2 - \sqrt{6}}{2 + \sqrt{6}} \), then what is the value of \( x^{2} + y^{2} \)?',
      'HI': r'यदि \( x = \dfrac{2 + \sqrt{6}}{2 - \sqrt{6}} \), \( y = \dfrac{2 - \sqrt{6}}{2 + \sqrt{6}} \) है, तो \( x^{2} + y^{2} \) का मान क्या है?'},
}
_E = lambda a: K(a + r' \times 10^{6}') + ' s'
FIXED_OPTS = {
 23: [_E('7.6'), _E('6.8'), _E('7.1'), _E('7.9')],
}
KEY_FIX = {}
# Q20: source "The sum of their ages is 57.6 years ago from now" fuses two sentences (HI: "योग 57 है। अब से 6 वर्ष पहले")
EN_EDIT = {
 20: [('The sum of their ages is 57.6 years ago from now, what was the ratio of the ages of the two persons?',
       'The sum of their ages is 57 years. What was the ratio of the ages of the two persons 6 years ago?')],
}
HI_EDIT = {
 20: [('उनकी आयु का योग 57 है।', 'उनकी आयु का योग 57 वर्ष है।')],
 35: [('जनवरी 2025 में घोषित घोषणा के अनुसार', 'जनवरी 2025 में की गई घोषणा के अनुसार')],
 40: [('सबसे सर्वोत्तम गुणवत्ता वाला', 'सर्वोत्तम गुणवत्ता वाला')],
}
# source option images typed: Q2 A/C/D "L"/"M"/"H", Q4 C "MZ", Q5 A "UW", Q66 D "laud"
# Q32: the policy was unveiled on 24 Jul 2025, the official key A was "January" -> option texts A/B swapped, key A kept
# Q72: Baldwin's original order is C-A-D-B, the official key D was "CBAD" -> option texts C/D swapped, key D kept
# Q63: option C was spelt correctly ("discrimination") though the underlined word is "discrmination" -> misspelling restored
OPT_FIX = {2: {'#A': 'L', '#C': 'M', '#D': 'H'}, 4: {'#C': 'MZ'}, 5: {'#A': 'UW'}}
OPT_FIX_EN = {32: {'January#A': 'July', 'July#B': 'January'}, 63: {'discrimination': 'discrmination'}, 66: {'#D': 'laud'},
              72: {'CADB#C': 'CBAD', 'CBAD#D': 'CADB'}}
OPT_FIX_HI = {32: {'जनवरी#A': 'जुलाई', 'जुलाई#B': 'जनवरी'}, 39: {'शार्ंगदेव': 'शारंगदेव'}}
HPD_STEM = {
 61: [('नीचे दिए गये वाक्य में किस प्रकार की अशुद्धि है-[BR]', 'नीचे दिए गए वाक्य में किस प्रकार की अशुद्धि है?[BR]')],
 62: [('नीचे दिए गये वाक्य में किस प्रकार की अशुद्धि है:[BR]', 'नीचे दिए गए वाक्य में किस प्रकार की अशुद्धि है?[BR]')],
 63: [('निम्नलिखित में वाक्य के शुद्ध रूप का चयन कीजिए:', 'निम्नलिखित में से वाक्य के शुद्ध रूप का चयन कीजिए।')],
 # "समस्याएं सुलझाने वाली बैठक" also fitted सभा; the police/forces grievance meeting held by the officer is a darbar
 67: [('सुरक्षा कर्मियों की समस्याएं सुलझाने वाली बैठक को क्या कहते हैं?',
       'पुलिस और सशस्त्र बलों में वरिष्ठ अधिकारी द्वारा जवानों की शिकायतें और समस्याएँ सीधे सुनकर उनका समाधान करने के लिए नियमित रूप से लगाई जाने वाली बैठक को क्या कहते हैं?')],
 # the stem "कार्य के मूल्यांकन" gave the key away
 68: [('कार्य के मूल्यांकन को क्या कहते हैं?',
       'किसी कर्मचारी के कार्य की गुणवत्ता और प्रदर्शन को परखकर उसका स्तर आँकने की प्रक्रिया को क्या कहते हैं?')],
 73: [("क्या है ?", "क्या है?")],
}
# Q61 C क्रिया (the verb ले लो also changes) -> कारक; Q63 A "युवा अवस्था" -> "युवावस्था" (sandhi form; यौवन + अवस्था is redundant);
# Q69 B पहचान (a badge also identifies) -> उपस्थिति; Q72 A "अपराध पूर्व अभ्यास" (a literal gloss of the stem) -> "अपराध पश्चात विश्लेषण"
HPD_OPT = {61: {2: 'कारक'}, 63: {0: 'युवावस्था की बुराइयों से बचो'}, 69: {1: 'उपस्थिति'}, 72: {0: 'अपराध पश्चात विश्लेषण'}}

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

# one reading-comprehension passage for Q76-80 (all five copies identical, no instruction line)
PASSAGE_EN = clean(EN[75]['comp'])
assert PASSAGE_EN.startswith('Driving is a responsibility')
assert all(clean(EN[i]['comp']) == PASSAGE_EN for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
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
    for need in [r'\( ? : \text{DK} :: \text{PS}', r'\( \text{VA} : \text{BZ} :: \text{GY} : ? ::', r'\( \text{KO825} : \text{HK425}', r'\( \text{GKN11} : \text{CGJ121}',
                 r'\( 608 : ? :: 13 : 242 :: 138 : 367 \)', r'is \( 7 : 12 \). The sum of their ages is 57 years. What was the ratio of the ages of the two persons 6 years ago?',
                 'A: L\nB: K\nC: M\nD: H\n', 'C: MZ\n', 'A: UW\n', 'D: laud\n', 'A: July\nB: January\n', 'C: CBAD\nD: CADB\n', 'C: discrmination\n',
                 r'A: \( 7.6 \times 10^{6} \) s', r'\( (5.1)^{2} \times 5.1', r'(\sqrt{6} + \sqrt{2})^{2} +', r'\( (9)^{3} + (7)^{3}', r'\( 40 \times (25^{2}',
                 r'value of \( x^{2} + y^{2} \)?', r'A: \( 5 : 12 \)', r'A: \( 24 : 25 \)', r'A: \( 3 : 2 \)', 'sports?||I. 4×100 metres[BR]II. 4×600 metres',
                 'TEXT: [FIGURE-BASED] Two figures', 'TEXT: [FIGURE-BASED] In the following figure series', 'PASSAGE (Q76–Q80): Driving is a responsibility']:
        assert need in en, need
    for bad in ['\\frac{', '​', 'A: \n', 'C: \n', 'D: \n', '57.6', '^{2} ×', 'C: discrimination']:
        assert bad not in en, bad
    assert en.count('[FIGURE-BASED]') == 4 and en.count('(figure 1)') == 4 and en.count('PASSAGE (Q76–Q80)') == 5
    assert hp.count('PASSAGE (Q76–Q80): आंतरिक सुरक्षा में प्रशिक्षण') == 5 and '​' not in hp and '<u>' not in hp and 'गये' not in hp
    for need in ['अशुद्धि है?||आप जाकर ले लो।', 'अशुद्धि है?||वह सब भले लोग हैं।', 'C: कारक\n', 'A: युवावस्था की बुराइयों से बचो\n', 'चयन कीजिए।\n',
                 'शिकायतें और समस्याएँ सीधे सुनकर', 'उसका स्तर आँकने की प्रक्रिया', 'B: उपस्थिति\n', 'A: अपराध पश्चात विश्लेषण\n', "अर्थ क्या है?\n"]:
        assert need in hp, need
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['2']['opts'] == ['L', 'K', 'M', 'H'] and h['4']['opts'][2] == 'MZ' and h['5']['opts'][0] == 'UW' and h['32']['opts'][:2] == ['जुलाई', 'जनवरी']
    assert h['39']['opts'][1] == 'शारंगदेव' and 'सबसे सर्वोत्तम' not in h['40']['TEXT'] and 'की गई घोषणा' in h['35']['TEXT'] and '57 वर्ष है' in h['20']['TEXT']
    assert h['44']['TEXT'].startswith('निम्नलिखित') and h['11']['opts'] == ['(figure 1)', '(figure 2)', '(figure 3)', '(figure 4)'] and h['48']['TEXT'].startswith('यदि \\(')
    assert r'\( \text{VA}' in h['4']['TEXT'] and h['23']['opts'][0] == r'\( 7.6 \times 10^{6} \) s' and h['60']['opts'][0] == r'\( 24 : 25 \)'
    assert '\\frac' not in json.dumps(h)
    print('ok')
