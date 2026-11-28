import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-20-may-shift-3'
PAPER = 'SSC GD Constable 2026 May 20 Shift 3'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {6, 7, 17, 18, 19}      # [FIGURE-BASED] stems
FIGOPT = {6, 7, 17, 18, 19}   # options are figures too
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
def F(a, b, tail): return K(r'\dfrac{' + a + '}{' + b + '}' + tail)
REP = {
 8:[('QF100 : RH220 :: LX150 : ? :: MK270 : NM390', ana('QF100 : RH220 :: LX150 : ? :: MK270 : NM390'))],
 9:[('DKM140 : HNE240 :: TPF160 : ? :: LTJ320 : EWM420', ana('DKM140 : HNE240 :: TPF160 : ? :: LTJ320 : EWM420'))],
 10:[('2349 : ? :: 8345 : 8385 :: 9297 : 9337', K('2349 : ? :: 8345 : 8385 :: 9297 : 9337'))],
 11:[('159 : 483 :: 726 : ? :: 914 : 2748', K('159 : 483 :: 726 : ? :: 914 : 2748'))],
 20:[('9 : 10', K('9 : 10'))],
 54:[('3 : 5', K('3 : 5'))],
 57:[('(100/7)', K(r'\dfrac{100}{7}'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 44: K(r'(\sqrt{5} + \sqrt{2})^2 - (\sqrt{5} - \sqrt{2})^2 = ?'),
 48: K(r'15^2 + 10^2 + 25^2 + 2(15 \times 10 + 10 \times 25 + 25 \times 15) = ?'),
 49: K(r'22^2 + 18^2 + 30^2 + 2(22 \times 18 + 18 \times 30 + 30 \times 22) = ?'),
}
FIXED_STEM_L = {
 43: {'EN': r'Which of the following lies between \( 2\dfrac{3}{10} \) & \( 2\dfrac{4}{5} \)?',
      'HI': r'निम्नलिखित में से कौन \( 2\dfrac{3}{10} \) और \( 2\dfrac{4}{5} \) के बीच स्थित है?'},
 45: {'EN': r'What is the value of \( \sqrt{5 + 2\sqrt{6}} \)?',
      'HI': r'\( \sqrt{5 + 2\sqrt{6}} \) का मान क्या है?'},
}
FIXED_OPTS = {
 43: [F('41', '18', ''), F('59', '20', ''), F('47', '18', ''), F('62', '21', '')],
 44: [K(r'4\sqrt{10}'), K(r'4\sqrt{7}'), K(r'4\sqrt{15}'), K(r'4\sqrt{12}')],
 45: [K(r'\sqrt{3} + 2\sqrt{2}'), K(r'3\sqrt{3} + \sqrt{2}'), K(r'\sqrt{3} + 2'), K(r'\sqrt{3} + \sqrt{2}')],
}
KEY_FIX = {}
EN_EDIT = {
 # error-spotting sentence split into its four parts
 73: [('Before going to bed, the mother ensured that the child was protected by the chilling weather.',
       'Before going to bed, / the mother ensured / that the child was / protected by the chilling weather.')],
}
HI_EDIT = {}
OPT_FIX = {}
# Q65 "Choose the misspelt word": the EN copy spelt all four words correctly (option D "Pronunciation", key D); the Hindi and
# Gujarati copies still carry the intended misspelling "Pronounciation" -> restored
OPT_FIX_EN = {65: {'Pronunciation#D': 'Pronounciation'}}
OPT_FIX_HI = {}
HI_STEM_FIX = {}
HPD_STEM = {
 64: [('कौन-सा एक पूर्ण विराम का चिन्ह है?', 'कौन-सा पूर्ण विराम का चिह्न है?')],
 68: [("का सही शब्द है?", "के लिए सही अंग्रेज़ी शब्द है?")],
}
HPD_OPT = {}
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

# one RC passage for Q76-80 (all five copies identical); comp starts with the generic instruction line, which is dropped
assert all(EN[i]['comp'] == EN[75]['comp'] for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
PASSAGE_EN, _n = re.subn(r'^Read the following passage carefully and answer the questions based on the passage:\s*\[BR\]', '', clean(EN[75]['comp']))
assert _n == 1 and PASSAGE_EN.startswith("Socio-cultural theory") and PASSAGE_EN.count('[BR]') == 1
RC_INSTR = ''
# Hindi Part D passage is Q74-Q78 (hi[93..97]); Q61-Q73, Q79, Q80 standalone
assert all(HI[i]['comp'] == HI[93]['comp'] for i in range(93, 98)) and all(not HI[i]['comp'] for i in list(range(80, 93)) + [98, 99])
HPD_PASSAGE = clean(HI[93]['comp'])
assert HPD_PASSAGE.startswith("सामुदायिक भागीदारी") and '[BR]' not in HPD_PASSAGE

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
        if 74 <= n <= 78:
            t = 'PASSAGE (Q74–Q78): ' + HPD_PASSAGE + ' || ' + t
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
