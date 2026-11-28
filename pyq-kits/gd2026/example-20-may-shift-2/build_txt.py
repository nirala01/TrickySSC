import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-20-may-shift-2'
PAPER = 'SSC GD Constable 2026 May 20 Shift 2'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {18, 19, 20}      # [FIGURE-BASED] stems
FIGOPT = {18, 19, 20}   # options are figures too
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
def F(a, b, tail): return K(r'\dfrac{' + a + '}{' + b + '}' + tail)
REP = {
 10:[('KT222 : QH336 :: SU302 : RP416 :: ZW432 : ?', ana('KT222 : QH336 :: SU302 : RP416 :: ZW432 : ?'))],
 11:[('ZKX102 : UHW204 :: XYR126 : ? :: LST305 : QPI610', ana('ZKX102 : UHW204 :: XYR126 : ? :: LST305 : QPI610'))],
 12:[('2793 : 2838 :: 6270 : ? :: 8180 : 8225', K('2793 : 2838 :: 6270 : ? :: 8180 : 8225'))],
 13:[('479 : 960 :: 25 : 52 :: ? : 728', K('479 : 960 :: 25 : 52 :: ? : 728'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 45: K(r'640\dfrac{1}{3} + 640\dfrac{1}{15} + 640\dfrac{1}{35} + \ldots + 640\dfrac{1}{99} = ?'),
}
FIXED_STEM_L = {}
FIXED_OPTS = {
 45: [K(r'3200\dfrac{5}{11}'), K(r'3750\dfrac{5}{13}'), K(r'3200\dfrac{4}{9}'), K(r'3500\dfrac{7}{8}')],
 46: [F('23', '24', ''), F('19', '20', ''), F('29', '30', ''), F('14', '15', '')],
}
KEY_FIX = {}
EN_EDIT = {
 # NCERT lists maize alone as "used both as food and fodder"; jowar/barley are arguable, so the stem is anchored to NCERT; key C kept
 27: [('Which crop is used as both food and fodder in India?', 'According to NCERT, which crop is used as both food and fodder in India?')],
 # the CATS Warrior was shown at Aero India (Feb 2025) and engine-tested in Jan 2025, not in May 2025; date dropped, key A (HAL) kept
 35: [(' in May 2025?', '?')],
 66: [],
 72: [('replete with loopholes which can have far-reaching', '<u>replete with loopholes which can have</u> far-reaching')],
 73: [('virtue. S2. There was', 'virtue.[BR]S2. There was')],
 75: [('His argument was not entirely wrong, but', '<u>His argument was not entirely wrong</u>, but')],
}
HI_EDIT = {
 27: [('भारत में किस फसल का उपयोग', 'एनसीईआरटी (NCERT) के अनुसार, भारत में किस फसल का उपयोग')],
 35: [('मई 2025 में किस संगठन द्वारा', 'किस संगठन द्वारा')],
}
# Q60 options "3:2"/"4:1" spaced like the other two (then KaTeX-wrapped)
OPT_FIX = {60: {'3:2': '3 : 2', '4:1': '4 : 1'}}
# Q63 C "Serendipity" (the Hindi/Gujarati copies still carry the misspelt "Serendepity"; the key C is the misspelt word);
# Q66: "tour ____ bus" - the official key "on" is not idiomatic without an article, "by bus" is the standard phrase -> the two option
# texts are swapped so the key letter B now sits on "by"
OPT_FIX_EN = {63: {'Serendipity#C': 'Serendepity'}, 66: {'by#A': 'on', 'on#B': 'by'}}
OPT_FIX_HI = {66: {'by#A': 'on', 'on#B': 'by'}}
HI_STEM_FIX = {}
HPD_STEM = {
 65: [("'औपचारिक ' का", "'औपचारिक' का")],
 66: [("'अमर ' का", "'अमर' का")],
}
# Q62 B "सदृिश्य" is an impossible letter sequence -> "सदृस्य"; Q72 A "राष्ट्रीय चिन्ह्" -> "राष्ट्रीय चिह्न"
HPD_OPT = {62: {1: 'सदृस्य'}, 72: {0: 'राष्ट्रीय चिह्न'}}
HPD_PASSAGE = None

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
    if lang == 'HI':
        for pair in HI_STEM_FIX.get(n, []): t = edit(t, pair, n, 'HI_FIX')
    if '[BR]' in t and '||' not in t: t = t.replace('[BR]', '||', 1)
    if n in FIG: t = '[FIGURE-BASED] ' + t
    return t

def opts(q, n, lang):
    if n in FIGOPT: return [f'(figure {i})' for i in range(1, 5)]
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

# one RC passage for Q76-80 (all five copies identical, no instruction line in comp); the instruction sits at the start of each stem
assert all(EN[i]['comp'] == EN[75]['comp'] for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
PASSAGE_EN = clean(EN[75]['comp'])
assert PASSAGE_EN.startswith("Environments characterized by poverty") and '[BR]' not in PASSAGE_EN
RC_INSTR = 'Read the following passage carefully and answer the questions based on the passage:||'
# Hindi Part D passage is Q73-Q77 (hi[92..96]); Q61-Q72, Q78-Q80 standalone
assert all(HI[i]['comp'] == HI[92]['comp'] for i in range(92, 97)) and all(not HI[i]['comp'] for i in list(range(80, 92)) + [97, 98, 99])
HPD_PASSAGE = clean(HI[92]['comp'])
assert HPD_PASSAGE.startswith("आंतरिक सुरक्षा व्यवस्था")

def build_en():
    out = [header('EN')]
    for i in range(80):
        q = EN[i]; n = i + 1
        t = stem(q, n, 'EN')
        if q['comp']:
            assert t.startswith(RC_INSTR), n
            t = 'PASSAGE (Q76–Q80): ' + PASSAGE_EN + ' || ' + t[len(RC_INSTR):]
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
    print('ok')
