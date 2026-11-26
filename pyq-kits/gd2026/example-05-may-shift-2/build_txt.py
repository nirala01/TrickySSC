import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-05-may-shift-2'
PAPER = 'SSC GD Constable 2026 May 05 Shift 2'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {12, 13, 20}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    out = []
    for tok in s.split(' '):
        out.append(T(tok) if re.search('[A-Z]', tok) else tok)
    return K(' '.join(out))
# Q2: "GT : JY" breaks the +2, +5 rule of the other pair (J is +3) -> "GT : IY" so the official key KS is the only answer
REP = {
 2: [('GT : JY :: FR : HW :: IN : ?', ana('GT : IY :: FR : HW :: IN : ?'))],
 14:[('JT290 : KU436 :: BF300 : CG446 :: KO480 : ?', ana('JT290 : KU436 :: BF300 : CG446 :: KO480 : ?'))],
 15:[('LPR80 : MSM180 :: AKP110 : KNB210 :: YVT150 : ?', ana('LPR80 : MSM180 :: AKP110 : KNB210 :: YVT150 : ?'))],
 16:[('2. Disgarge', '2. Disgorge'), ('4. Disguse', '4. Disguise')],
 17:[('9285 : 9334 :: ? : 7980 :: 4473 : 4522', K('9285 : 9334 :: ? : 7980 :: 4473 : 4522'))],
 43:[('(5/6)', K(r'\dfrac{5}{6}'))],
 55:[('4/7', K(r'\dfrac{4}{7}')), ('2/5', K(r'\dfrac{2}{5}'))],
 58:[('1/3', K(r'\dfrac{1}{3}'))],
 59:[('(8/3)', K(r'\dfrac{8}{3}')), ('(5/8)', K(r'\dfrac{5}{8}'))],
}
REP_EN = {49: [('A = 2^{5} x 3^{2}', K(r'A = 2^{5} \times 3^{2}')), ('B = 2^{8} x 3^{4}', K(r'B = 2^{8} \times 3^{4}'))]}
REP_HI = {49: [(r'A = 2^{5} \times 3^{2}', K(r'A = 2^{5} \times 3^{2}')), (r'B = 2^{8} \times 3^{4}', K(r'B = 2^{8} \times 3^{4}'))],
          42: [('22 x 2', '22 × 2')]}
FIXED_STEM = {
 44: K(r'(15.3 + 5.3)^{2} - 4 \times 15.3 \times 5.3 = ?'),
}
FIXED_OPTS = {
 43: [K(r'\dfrac{10}{11}'), K(r'\dfrac{4}{5}'), K(r'\dfrac{9}{10}'), K(r'\dfrac{7}{8}')],
 46: [K('4 : 7'), K('7 : 6'), K('7 : 3'), K('3 : 4')],
 49: [K(r'2^{13} \times 3^{6}'), K(r'2^{13} \times 3^{8}'), K(r'2^{10} \times 3^{6}'), K(r'2^{8} \times 3^{6}')],
 58: [K(r'\dfrac{600}{13}'), K(r'\dfrac{540}{11}'), K(r'\dfrac{136}{3}'), K(r'\dfrac{540}{13}')],
}
KEY_FIX = {}
EN_EDIT = {
 40: [("In 2025, IMF in its World Economic Outlook,", "In July 2025, IMF in its World Economic Outlook Update,")],
 61: [('difficulty level, Rahul on the Army', 'difficulty level, Rahul _____ on the Army')],
 64: [('He was in agony after', 'He was in <u>agony</u> after')],
 71: [('sector is fraught with numerous challenges ranging', 'sector is <u>fraught with numerous challenges</u> ranging')],
 73: [('issuing from a warren. D. One little boy', 'issuing from a warren.[BR]D. One little boy')],
 75: [('[BR]She made less mistakes this time, showing', '[BR]<u>She made less mistakes this time</u>, showing')],
}
HI_EDIT = {
 40: [('2025 में, IMF ने अपने वर्ल्ड इकोनॉमिक आउटलुक में', 'जुलाई 2025 में, IMF ने अपने वर्ल्ड इकोनॉमिक आउटलुक अपडेट में')],
}
OPT_FIX = {}
# Q61 "threw in the towe" -> towel; Q63 "Raucous" is also correctly spelt -> misspelt so only the key Rescind is right;
# Q66 "Concea" -> Conceal; Q80 "Grows" (evolve = develop/grow gradually) -> "Slows" so only the key Changes fits;
# Q59 option rebuilt as KaTeX
OPT_FIX_EN = {61: {'threw in the towe': 'threw in the towel'}, 63: {'Raucous': 'Raucus'}, 66: {'Concea': 'Conceal'},
              80: {'Grows': 'Slows'}, 59: {'(200/3) percent': K(r'\dfrac{200}{3}') + ' percent'}}
OPT_FIX_HI = {33: {'18 to 60 years': '18 से 60 वर्ष', '21 to 40 years': '21 से 40 वर्ष', '21 to 60 years': '21 से 60 वर्ष'},
              59: {r'\( (200/3) \) प्रतिशत': K(r'\dfrac{200}{3}') + ' प्रतिशत'}}
HPD_STEM = {
 75: [('नीचे दिए गए शब्द की <u>सही</u> पारिभाषिक शब्दावली क्या होगी:', 'नीचे दिए गए शब्द की सही पारिभाषिक शब्दावली क्या होगी?')],
}
# HI Part D option fixes (index 0-3): Q62 B "व्यक्ति" is a correctly spelt word -> misspelt; Q63 C "मसजिद" (older accepted variant)
# and D "मस्जिदों" (correct plural) -> misspelt; Q64 A "कमज़ोर" (nukta form, also correct) -> misspelt (key B कमजोर);
# Q70 D "अग्रेषण" (forwarding — also fitted "भेजी जाती है") -> "आदेश"; Q71 D "सील ज़ोन" (also a sealed-off area) -> "पार्किंग ज़ोन"
HPD_OPT = {62: {1: 'वयक्तिक'}, 63: {2: 'मसजीद', 3: 'मस्जीद'}, 64: {0: 'कमजौर'}, 70: {3: 'आदेश'}, 71: {3: 'पार्किंग ज़ोन'}}

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
    for k, x in enumerate(q['opts']):
        v = clean(x).replace('\u200b', '').strip()
        v = OPT_FIX.get(n, {}).get(v, v)
        fx = (OPT_FIX_EN if lang == 'EN' else OPT_FIX_HI).get(n, {})
        v = fx.get(v + '#' + 'ABCD'[k], fx.get(v, v))
        out.append(v)
    return out

def block(n, subj, concept, text, op, ans):
    return f"[Q{n}]\nSUBJECT: {subj}\nCONCEPT: {concept}\nTEXT: {text}\nA: {op[0]}\nB: {op[1]}\nC: {op[2]}\nD: {op[3]}\nANSWER: {ans}\n"

def header(lang): return f"# TRICKYSSC QUESTIONS\nEXAM: ssc-gd\nYEAR: 2026\nPAPER: {PAPER}\nLANG: {lang}\n"

# one cloze passage for Q76-80 (all five copies identical); blanks rebuilt as ___A___ ... ___C___, D/E are words tested in Q79/Q80
PASSAGE_EN = clean(EN[75]['comp'])
assert all(clean(EN[i]['comp']) == PASSAGE_EN for i in range(75, 80))
for L in 'ABC':
    a = f'______ {L} ______'
    assert PASSAGE_EN.count(a) == 1, a
    PASSAGE_EN = PASSAGE_EN.replace(a, f'___{L}___')
for L, w in (('D', 'reminisce'), ('E', 'evolves')):
    a = f'______ {L} ______ ({w})'
    assert PASSAGE_EN.count(a) == 1, a
    PASSAGE_EN = PASSAGE_EN.replace(a, f'({L}) <u>{w}</u>')
assert '____ ' not in PASSAGE_EN and ' , ' not in PASSAGE_EN

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
            p = clean(q['comp'])
            p = p.replace('[BR]उपरोक्त गद्यांश के आधार पर प्रश्न का उत्तर दें:', '')
            p = p.replace('आपसी विश्वास विश्वास और', 'आपसी विश्वास और')
            assert 'उपरोक्त' not in p and 'विश्वास विश्वास' not in p
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
    for need in [r'\( \text{GT} : \text{IY} :: \text{FR}', r'\( \text{JT290} : \text{KU436}', r'\( \text{LPR80}', r'\( 9285 : 9334', '2. Disgorge', '4. Disguise',
                 'In July 2025, IMF in its World Economic Outlook Update,', 'Rahul _____ on the Army', 'in <u>agony</u> after', '<u>fraught with numerous challenges</u>',
                 'warren.[BR]D. One little boy', '||<u>She made less mistakes this time</u>,', 'D: threw in the towel\n', 'C: Raucus\n', 'A: Conceal\n',
                 'B: Slows\n', r'\( \dfrac{5}{6} \)', r'\( \dfrac{4}{7} \)', r'\( \dfrac{1}{3} \)', r'\( \dfrac{8}{3} \)', r'A: \( \dfrac{200}{3} \) percent',
                 r'A: \( 4 : 7 \)', r'\( A = 2^{5} \times 3^{2} \)', r'A: \( 2^{13} \times 3^{6} \)', r'\( (15.3 + 5.3)^{2}', '___A___', '___C___',
                 '(D) <u>reminisce</u>', '(E) <u>evolves</u>', 'PASSAGE (Q76–Q80): Complete the passage']:
        assert need in en, need
    for bad in ['Concea\n', 'towe\n', '\\frac{', '​', ' , ', 'Disgarge', '2^{5} x', '______ A']:
        assert bad not in en, bad
    assert en.count('[FIGURE-BASED]') == 3 and en.count('(figure 1)') == 3
    assert hp.count('PASSAGE (Q76–Q80)') == 5 and '​' not in hp and 'क्या होगी?||Medical examination' in hp and '<u>' not in hp
    for need in ['B: वयक्तिक\n', 'C: मसजीद\n', 'D: मस्जीद\n', 'A: कमजौर\n', 'D: आदेश\n', 'D: पार्किंग ज़ोन\n']:
        assert need in hp, need
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['33']['opts'] == ['18 से 40 वर्ष', '18 से 60 वर्ष', '21 से 40 वर्ष', '21 से 60 वर्ष'] and 'जुलाई 2025' in h['40']['TEXT'] and 'अपडेट' in h['40']['TEXT']
    assert r'\text{GT} : \text{IY}' in h['2']['TEXT'] and 'Disgorge' in h['16']['TEXT'] and '22 × 2' in h['42']['TEXT'] and h['42']['TEXT'].startswith('निम्नलिखित')
    assert r'\( A = 2^{5} \times 3^{2} \)' in h['49']['TEXT'] and r'\( \dfrac{5}{6} \)' in h['43']['TEXT'] and h['59']['opts'][0] == r'\( \dfrac{200}{3} \) प्रतिशत'
    assert h['44']['TEXT'].startswith('निम्नलिखित') and r'\( \dfrac{2}{5} \)' in h['55']['TEXT'] and h['12']['opts'] == ['(figure 1)', '(figure 2)', '(figure 3)', '(figure 4)']
    assert '\\frac{' not in json.dumps(h) and h['46']['opts'][0] == r'\( 4 : 7 \)'
    print('ok')
