import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-06-may-shift-2'
PAPER = 'SSC GD Constable 2026 May 06 Shift 2'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {11, 12, 18, 19}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 3: [('AZ : FA :: JS : OH :: KM : ?', ana('AZ : FA :: JS : OH :: KM : ?'))],
 5: [('HJ : FD :: AC : YW :: EX : ?', ana('HJ : FD :: AC : YW :: EX : ?'))],
 13:[('BG12 : EJ59 :: PQ48 : ST95 :: LM33 : ?', ana('BG12 : EJ59 :: PQ48 : ST95 :: LM33 : ?'))],
 14:[('AK40 : EE100 :: BM60 : ? :: DL80 : HF200', ana('AK40 : EE100 :: BM60 : ? :: DL80 : HF200'))],
 15:[('2436 : ? :: 777 : 257 :: 1812 : 602', K('2436 : ? :: 777 : 257 :: 1812 : 602'))],
 # 0.5 deg gives 3316 km (no option); the keyed 3475 km needs the Moon's real angular size, about 0.524 deg
 25:[('0.5°', '0.524°'), ('3.8×10^{8} m', K(r'3.8 \times 10^{8}') + ' m')],
 45:[(r'\sqrt{x+1} = 5', K(r'\sqrt{x + 1} = 5'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 43: K(r'6\dfrac{1}{3} + 4\dfrac{1}{2} - 2\dfrac{1}{4} - 1\dfrac{1}{6} = ?'),
 44: K(r'\left( \dfrac{\sqrt{0.04}}{0.4} \right) \times \left( \dfrac{0.8}{\sqrt{0.16}} \right) \times \left( \dfrac{1.2}{\sqrt{0.36}} \right) = ?'),
 47: K(r'\dfrac{(\sqrt{11} + \sqrt{4})^{2} + (\sqrt{11} - \sqrt{4})^{2}}{10\sqrt{15}} = ?'),
 50: K(r'(540 - 460)^{2} + 4 \times 540 \times 460 = ?'),
}
FIXED_OPTS = {
 43: [K(r'7\dfrac{1}{4}'), K(r'7\dfrac{5}{12}'), K(r'9\dfrac{1}{4}'), K(r'8\dfrac{11}{12}')],
 47: [K(r'\dfrac{\sqrt{15}}{5}'), K(r'\dfrac{15\sqrt{15}}{50}'), K(r'\dfrac{15\sqrt{15}}{25}'), K(r'\dfrac{3\sqrt{15}}{10}')],
 20: [K('21 : 5'), K('23 : 9'), K('27 : 5'), K('31 : 11')],
}
KEY_FIX = {}
EN_EDIT = {
 28: [('Which was the first Asian country to host the FIFA World Cup?', 'Which were the first Asian countries to host the FIFA World Cup?')],
 72: [('C. He said in the car', 'C. He sat in the car')],
}
HI_EDIT = {
 28: [('की मेजबानी करने वाला पहला एशियाई देश कौन सा था?', 'की मेजबानी करने वाले पहले एशियाई देश कौन-से थे?')],
 57: [('P से 2 गुना अधिक कार्यकुशल', 'P से 2 गुना कार्यकुशल'), ('Q से 1.5 गुना अधिक कार्यकुशल', 'Q से 1.5 गुना कार्यकुशल')],
}
OPT_FIX = {2: {'': 'I'}}
# Q2 A and Q3 D were images of the letters "I" and "NN" (typed); Q32 key D "Punjab and Haryana" was wrong (38th Surajkund Mela
# 2025 theme states were Odisha and Madhya Pradesh) - D rewritten to the true pair, B (the true pair) -> 2026 theme states UP & Meghalaya;
# Q63 B "inconsistent" -> "inconsistant" (the misspelt word as it stands in the sentence)
OPT_FIX_EN = {3: {'#D': 'NN'}, 32: {'Madhya Pradesh and Odisha': 'Uttar Pradesh and Meghalaya', 'Punjab and Haryana': 'Madhya Pradesh and Odisha'},
              63: {'inconsistent': 'inconsistant'}}
OPT_FIX_HI = {3: {'#D': 'NN'}, 32: {'मध्य प्रदेश और ओडिशा': 'उत्तर प्रदेश और मेघालय', 'पंजाब और हरियाणा': 'मध्य प्रदेश और ओडिशा'},
              37: {'राष्ट्रीय स्वास्थ्य नीति 2010': 'राष्ट्रीय फिटनेस नीति 2010'}}
HPD_STEM = {
 61: [('नीचे दिए गये वाक्य में किस प्रकार की <u>अशुद्धि</u> है:', 'नीचे दिए गए वाक्य में किस प्रकार की अशुद्धि है?')],
 72: [('जब एक आरोपी अपराध करने की मानसिक तैयारी में था, पर अपराध पूरा नहीं हुआ, तो यह क्या कहलाता है?',
       'जब कोई आरोपी अपराध करने के इरादे से उसकी ओर कदम उठा लेता है, पर अपराध पूरा नहीं होता, तो कानूनी भाषा में यह क्या कहलाता है?')],
}
# HI Part D option fixes (index 0-3): Q63 B "पुनरुक्ति-संबंधी" (also describes "गुप्त रहस्य") -> "लिंग-संबंधी";
# Q70 D duplicate "मीडिया को" -> "आम जनता को"; Q80 A "चेतावनी सूचना" (repeats the stem) -> "सम्मन"
HPD_OPT = {63: {1: 'लिंग-संबंधी'}, 70: {3: 'आम जनता को'}, 80: {0: 'सम्मन'}}

def edit(t, pair, n, tag):
    a, b = pair
    if a not in t: raise SystemExit(f'Q{n} {tag}: anchor missing {a!r}')
    return t.replace(a, b, 1)

def stem(q, n, lang):
    if n in FIXED_STEM: return FIXED_STEM[n]
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
        fx = (OPT_FIX_EN if lang == 'EN' else OPT_FIX_HI).get(n, {})
        v = fx.get(v + '#' + 'ABCD'[k], fx.get(v, v))
        out.append(v)
    return out

def block(n, subj, concept, text, op, ans):
    return f"[Q{n}]\nSUBJECT: {subj}\nCONCEPT: {concept}\nTEXT: {text}\nA: {op[0]}\nB: {op[1]}\nC: {op[2]}\nD: {op[3]}\nANSWER: {ans}\n"

def header(lang): return f"# TRICKYSSC QUESTIONS\nEXAM: ssc-gd\nYEAR: 2026\nPAPER: {PAPER}\nLANG: {lang}\n"

# one reading-comprehension passage for Q76-80 (all five copies identical; no instruction line in this file)
PASSAGE_EN = clean(EN[75]['comp'])
assert all(clean(EN[i]['comp']) == PASSAGE_EN for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
assert PASSAGE_EN.startswith('Literature and language studies')

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
    P = clean(HI[93]['comp'])
    assert all(clean(HI[i]['comp']) == P for i in range(93, 98)) and all(not HI[i]['comp'] for i in list(range(80, 93)) + [98, 99])
    for i in range(80, 100):
        q = HI[i]; n = i - 19
        t = clean(q['text'])
        for pair in HPD_STEM.get(n, []): t = edit(t, pair, n, 'HPD')
        if '[BR]' in t: t = t.replace('[BR]', '||', 1)
        if q['comp']:
            t = 'PASSAGE (Q74–Q78): ' + P + ' || ' + t
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
    for need in [r'\( \text{AZ} : \text{FA} :: \text{JS}', r'\( \text{HJ} : \text{FD}', r'\( \text{BG12} : \text{EJ59}', r'\( \text{AK40} : \text{EE100} :: \text{BM60} : ?',
                 r'\( 2436 : ? :: 777', 'A: I\n', 'D: NN\n', r'A: \( 21 : 5 \)', '0.524°', r'\( 3.8 \times 10^{8} \) m', r'\( \sqrt{x + 1} = 5 \)',
                 r'6\dfrac{1}{3}', r'B: \( 7\dfrac{5}{12} \)', r'\left( \dfrac{\sqrt{0.04}}{0.4} \right)', r'D: \( \dfrac{3\sqrt{15}}{10} \)', r'(540 - 460)^{2} + 4 \times 540',
                 'first Asian countries', 'B: Uttar Pradesh and Meghalaya\n', 'D: Madhya Pradesh and Odisha\n', 'B: inconsistant\n', 'C. He sat in the car',
                 'TEXT: [FIGURE-BASED] Two figures', 'PASSAGE (Q76–Q80): Literature and language']:
        assert need in en, need
    for bad in ['\\frac{', '​', 'Punjab and Haryana', 'He said in', 'A: \n', 'D: \n', '^{8} m.', 'first Asian country ']:
        assert bad not in en, bad
    assert en.count('[FIGURE-BASED]') == 4 and en.count('(figure 1)') == 4 and en.count('PASSAGE (Q76–Q80)') == 5
    assert hp.count('PASSAGE (Q74–Q78)') == 5 and '​' not in hp and '<u>अशुद्धि</u> है:' not in hp
    for need in ['B: लिंग-संबंधी\n', 'D: आम जनता को\n', 'A: सम्मन\n', 'अशुद्धि है?||जीवन और साहित्य', 'कानूनी भाषा में यह क्या कहलाता है?']:
        assert need in hp, need
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['2']['opts'][0] == 'I' and h['3']['opts'][3] == 'NN' and h['32']['opts'][3] == 'मध्य प्रदेश और ओडिशा' and h['32']['opts'][1] == 'उत्तर प्रदेश और मेघालय'
    assert '0.524°' in h['25']['TEXT'] and 'पहले एशियाई देश कौन-से थे' in h['28']['TEXT'] and 'अधिक कार्यकुशल' not in h['57']['TEXT'] and h['37']['opts'][2] == 'राष्ट्रीय फिटनेस नीति 2010'
    assert h['50']['TEXT'].startswith('निम्नलिखित') and h['11']['opts'] == ['(figure 1)', '(figure 2)', '(figure 3)', '(figure 4)'] and h['47']['opts'][1] == r'\( \dfrac{15\sqrt{15}}{50} \)'
    assert '\\frac{' not in json.dumps(h) and r'\( \sqrt{x + 1} = 5 \)' in h['45']['TEXT'] and h['20']['opts'][2] == r'\( 27 : 5 \)'
    print('ok')
