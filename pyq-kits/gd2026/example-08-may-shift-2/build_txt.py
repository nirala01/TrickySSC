import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-08-may-shift-2'
PAPER = 'SSC GD Constable 2026 May 08 Shift 2'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {11, 12, 18, 19}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
# Q2: the source printed single colons "ABQ : CDS : ? : RJK : RMN : TOP" — set to the analogy form the stem describes
REP = {
 2:[('ABQ : CDS : ? : RJK : RMN : TOP', ana('ABQ : CDS :: ? : RJK :: RMN : TOP'))],
 4:[('? : RY :: LI : HD :: GA : CV', ana('? : RY :: LI : HD :: GA : CV'))],
 13:[('TU130 : TS90 :: AW95 : VZ55 :: ? : TR80', ana('TU130 : TS90 :: AW95 : VZ55 :: ? : TR80'))],
 14:[('BZA80 : AXX440 :: TJP90 : ? :: LMK110 : KKH470', ana('BZA80 : AXX440 :: TJP90 : ? :: LMK110 : KKH470'))],
 15:[('167 : 497 :: 437 : 1307 :: ? : 62', K('167 : 497 :: 437 : 1307 :: ? : 62'))],
 20:[('5 : 7', K('5 : 7'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 43: K(r'\dfrac{(0.5 \times 0.5) + (0.5 \times 0.05)}{0.1375} = ?'),
 44: K(r'\sqrt{20.25} + \sqrt{0.36} + \sqrt{6.25} - \sqrt{2.25} = ?'),
 # Q47: the source exponent 1/2 gives the fourth root of 320 (≈ 4.23), not an option; the key 320 needs the square
 47: K(r'\left(\sqrt{(21 + 11) \times (21 - 11)}\right)^{2} = ?'),
 49: K(r'\sqrt{48} + \sqrt{27} - \sqrt{12} = ?'),
}
FIXED_STEM_L = {
 45: {'EN': r'If \( x = \sqrt{100} \div \sqrt{25} + \sqrt{49} \), then what is the value of \( x^{2} \)?',
      'HI': r'यदि \( x = \sqrt{100} \div \sqrt{25} + \sqrt{49} \) है, तो \( x^{2} \) का मान क्या है?'},
}
FIXED_OPTS = {
 49: [K(r'4\sqrt{3}'), K(r'5\sqrt{3}'), K(r'7\sqrt{3}'), K(r'6\sqrt{3}')],
}
KEY_FIX = {}
# Q28: AOGUSY was approved/launched by the Ministry of Ayush in 2021 (not 2025)
EN_EDIT = {
 28: [('Samvardhan Yojana launched in 2025?', 'Samvardhan Yojana launched by the Ministry of Ayush in 2021?')],
}
HI_EDIT = {
 28: [('2025 में शुरू की गई', 'आयुष मंत्रालय द्वारा 2021 में शुरू की गई')],
}
# Q3 option C was a 14×10 image of "FA" — typed. Q61 D "mmigrated" -> "immigrated"; Q62 A shows the misspelt
# "resillience" the stem underlines (source option showed the correct spelling); Q70 A "The quest" -> "The guest" (as in the sentence)
OPT_FIX = {3: {'#C': 'FA'}}
OPT_FIX_EN = {61: {'mmigrated here': 'immigrated here'}, 62: {'resilience': 'resillience'}, 70: {'The quest': 'The guest'}}
OPT_FIX_HI = {}
HPD_STEM = {
 # "मैंने नहीं जाना" is also a correct past tense of जानना ("I did not know") — the classic सर्वनाम error sentence used instead
 61: [('अशुद्धि है-[BR]मैंने नहीं जाना।', 'अशुद्धि है?[BR]मैंने घर जाना है।')],
 # "आप … करो" also had a क्रिया error (करो with आप) — verb set to करें so only the सर्वनाम error (आपका → अपना) remains
 62: [('अशुद्धि है:[BR]आप आपका काम करो।', 'अशुद्धि है?[BR]आप आपका काम करें।')],
 75: [("'कानूनी रूप से पकड़ना' शब्द का उपयुक्त हिंदी अर्थ क्या है?", "'कानूनी रूप से पकड़ना' के लिए उपयुक्त शब्द क्या है?")],
}
# Q69 C देशज (ढूँढना is listed as देशज in many books) -> संकर so only the key B तद्भव fits;
# Q72 A "साक्ष्य मिटाना" (also means destroying evidence) -> "साक्ष्य संकलन"
HPD_OPT = {69: {2: 'संकर'}, 72: {0: 'साक्ष्य संकलन'}}

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
assert PASSAGE_EN.startswith('The Jaipur Literature Festival')
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
    for need in [r'\( \text{ABQ} : \text{CDS} :: ? : \text{RJK} :: \text{RMN} : \text{TOP} \)', r'\( ? : \text{RY} ::', r'\( \text{TU130} : \text{TS90}', r'\( \text{BZA80} : \text{AXX440}',
                 r'\( 167 : 497 :: 437 : 1307 :: ? : 62 \)', r'is \( 5 : 7 \).', 'C: FA\n', r'A: \( 3 : 5 \)', r'\( \dfrac{(0.5 \times 0.5)', r'\right)^{2} = ? \)', r'value of \( x^{2} \)?',
                 r'A: \( 4\sqrt{3} \)', 'launched by the Ministry of Ayush in 2021?', 'D: immigrated here\n', 'A: resillience\n', 'A: The guest\n',
                 'TEXT: [FIGURE-BASED] Two figures', 'TEXT: [FIGURE-BASED] In the following figure series', 'PASSAGE (Q76–Q80): The Jaipur Literature Festival']:
        assert need in en, need
    for bad in ['\\frac{', '​', 'A: \n', 'C: \n', 'D: \n', '\\rm', 'D: mmigrated', 'The quest', 'A: resilience\n', 'frac{1}{2}', 'CDS : ?', 'x^{2}?']:
        assert bad not in en, bad
    assert en.count('[FIGURE-BASED]') == 4 and en.count('(figure 1)') == 4 and en.count('PASSAGE (Q76–Q80)') == 5
    assert hp.count('PASSAGE (Q76–Q80): आंतरिक सुरक्षा में संवाद प्रणाली') == 5 and '​' not in hp
    for need in ['अशुद्धि है?||मैंने घर जाना है।', 'अशुद्धि है?||आप आपका काम करें।', 'C: संकर\n', 'A: साक्ष्य संकलन\n', "के लिए उपयुक्त शब्द क्या है?"]:
        assert need in hp, need
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['3']['opts'][2] == 'FA' and h['11']['opts'] == ['(figure 1)', '(figure 2)', '(figure 3)', '(figure 4)'] and 'आयुष मंत्रालय द्वारा 2021' in h['28']['TEXT']
    assert h['43']['TEXT'].startswith('निम्नलिखित') and h['45']['TEXT'].startswith('यदि \\(') and h['49']['opts'][0] == r'\( 4\sqrt{3} \)' and h['20']['opts'][0] == r'\( 3 : 5 \)'
    assert r'\( \text{ABQ}' in h['2']['TEXT'] and r'\( 5 : 7 \)' in h['20']['TEXT'] and r'^{2} = ? \)' in h['47']['TEXT']
    assert '\\frac' not in json.dumps(h) and '\\rm' not in json.dumps(h)
    print('ok')
