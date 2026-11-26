import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-06-may-shift-1'
PAPER = 'SSC GD Constable 2026 May 06 Shift 1'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {9, 10}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 4: [(' DD, HZ, LV', '||DD, HZ, LV')],
 5: [(' OT, LQ, IM', '||OT, LQ, IM')],
 11:[('AZ300 : CD440 :: BY400 : DC540 :: CX200 : ?', ana('AZ300 : CD440 :: BY400 : DC540 :: CX200 : ?'))],
 12:[('?: MM225 :: AJ80 : GF200 :: DL70 : JH175', ana('? : MM225 :: AJ80 : GF200 :: DL70 : JH175'))],
 13:[('4740 : 4770 :: 2049 : ? :: 670 : 700', K('4740 : 4770 :: 2049 : ? :: 670 : 700'))],
 14:[('867 : 1341 :: 776 : 1250 :: ? : 541', K('867 : 1341 :: 776 : 1250 :: ? : 541'))],
 18:[('UQL162 WUR243', 'UQL162, WUR243')],
 39:[(' II. ', '[BR]II. ')],
 51:[('? I. p = 35. II. ', '?[BR]I. p = 35.[BR]II. ')],
 52:[('7 : 9', K('7 : 9'))],
 54:[('5 : 2', K('5 : 2'))],
 55:[('10 : 13', K('10 : 13'))],
 57:[('1/5', K(r'\dfrac{1}{5}'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 44: K(r'\dfrac{(0.7)^{4} - (0.3)^{4}}{(0.7)^{2} + (0.3)^{2}} = ?'),
 45: K(r'\dfrac{1}{4 + \sqrt{2}} + \dfrac{1}{4 - \sqrt{2}} = ?'),
 # source printed sqrt(108900 + sqrt(12321)) = 330.17; every option (21, 23, 26, 27) needs sqrt(sqrt(108900) + sqrt(12321)) = sqrt(441) = 21
 46: K(r'\sqrt{\sqrt{108900} + \sqrt{12321}} = ?'),
 48: K(r'1^{2} + 2^{2} + 3^{2} + \ldots + 30^{2} = ?'),
}
FIXED_OPTS = {
 45: [K(r'\dfrac{7}{4}'), K(r'\dfrac{4}{7}'), K(r'\dfrac{5}{7}'), K(r'\dfrac{3}{7}')],
 55: [K('3 : 10'), K('3 : 13'), K('13 : 7'), K('7 : 13')],
 58: ['17', K(r'\dfrac{58}{3}'), '18', K(r'\dfrac{55}{3}')],
}
KEY_FIX = {}
EN_EDIT = {
 26: [('Which of the following is the largest contributor to urban PM2.5 in India?',
       "According to source-apportionment studies of Delhi's air, which of the following is the largest overall contributor to PM2.5?")],
 33: [('II. Other Backward Caste', 'II. Other Backward Classes')],
 72: [('the problem would aggravate into an', '<u>the problem would aggravate into</u> an')],
 75: [('keeps reverting back to her bad habits', '<u>keeps reverting back to her bad habits</u>')],
}
HI_EDIT = {
 26: [('निम्नलिखित में से कौन भारत में शहरी PM2.5 का सबसे बड़ा योगदानकर्ता है?',
       'दिल्ली की वायु के स्रोत-विभाजन (source apportionment) अध्ययनों के अनुसार, निम्नलिखित में से कौन PM2.5 का सबसे बड़ा समग्र योगदानकर्ता है?')],
}
OPT_FIX = {}
# Q8 D "s" -> "S" (the girl's name, as in the HI paper); Q63 D "spurious" (also correctly spelt) -> "spurrious" so only the key
# Sanguine is right; Q66 D "Āō" (garbage in all three languages) -> "Aid" (a synonym, so impede stays the only antonym);
# Q70 A "Each wal" -> "Each wall"
OPT_FIX_EN = {8: {'s': 'S'}, 63: {'spurious': 'spurrious'}, 66: {'Āō': 'Aid'}, 70: {'Each wal': 'Each wall'}}
OPT_FIX_HI = {}
HPD_STEM = {
 72: [('क्या होगा:', 'क्या होगी?')],
}
# HI Part D option fixes (index 0-3): Q74 D "नज़र के अंतर्गत बंद करना" (also describes custody) -> "ज़मानत पर रिहा करना"
HPD_OPT = {74: {3: 'ज़मानत पर रिहा करना'}}

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

# one reading-comprehension passage for Q76-80 (all five copies identical); generic instruction line dropped
PASSAGE_EN = clean(EN[75]['comp'])
assert all(clean(EN[i]['comp']) == PASSAGE_EN for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
assert PASSAGE_EN.startswith('Read the following passage carefully and answer the questions based on the passage:[BR]')
PASSAGE_EN = PASSAGE_EN.split('[BR]', 1)[1]

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
    P = clean(HI[95]['comp'])
    assert all(clean(HI[i]['comp']) == P for i in range(95, 100)) and all(not HI[i]['comp'] for i in range(80, 95))
    for i in range(80, 100):
        q = HI[i]; n = i - 19
        t = clean(q['text'])
        for pair in HPD_STEM.get(n, []): t = edit(t, pair, n, 'HPD')
        if '[BR]' in t: t = t.replace('[BR]', '||', 1)
        if q['comp']:
            t = 'PASSAGE (Q76–Q80): ' + P + ' || ' + t
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
    for need in [r'\( \text{AZ300} : \text{CD440}', r'\( ? : \text{MM225}', r'\( 4740 : 4770', r'\( 867 : 1341', 'UQL162, WUR243', '.||DD, HZ', '.||OT, LQ',
                 'D: S\n', 'TEXT: [FIGURE-BASED] Two figures', r'\sqrt{\sqrt{108900} + \sqrt{12321}}', r'\ldots + 30^{2}', r'B: \( \dfrac{4}{7} \)',
                 r'D: \( 7 : 13 \)', r'D: \( \dfrac{55}{3} \)', r'\( \dfrac{1}{5} \)', 'Delhi', 'Other Backward Classes', 'Borrowings[BR]II. Taxation',
                 'p = 35.[BR]II.', 'D: spurrious\n', 'D: Aid\n', 'A: Each wall\n', '<u>the problem would aggravate into</u>',
                 '<u>keeps reverting back to her bad habits</u>', 'PASSAGE (Q76–Q80): Dehydration-related']:
        assert need in en, need
    for bad in ['Āō', 'Each wal\n', '\\frac{', '​', '?: MM', 'Backward Caste', 'Read the following passage', 'D: s\n', '.....']:
        assert bad not in en, bad
    assert en.count('[FIGURE-BASED]') == 2 and en.count('(figure 1)') == 2 and en.count('PASSAGE (Q76–Q80)') == 5
    assert hp.count('PASSAGE (Q76–Q80)') == 5 and '​' not in hp and 'क्या होगा:' not in hp
    for need in ['D: ज़मानत पर रिहा करना\n', 'क्या होगी?||गैर-सरकारी', 'अशुद्धि है:||मैंने राम को पूछा।']:
        assert need in hp, need
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['8']['opts'][3] == 'S' and 'दिल्ली' in h['26']['TEXT'] and 'उधार[BR]II. कराधान' in h['39']['TEXT'] and r'\( \dfrac{1}{5} \)' in h['57']['TEXT']
    assert h['46']['TEXT'].startswith('निम्नलिखित') and r'\sqrt{\sqrt{108900}' in h['46']['TEXT'] and h['9']['opts'] == ['(figure 1)', '(figure 2)', '(figure 3)', '(figure 4)']
    assert '\\frac{' not in json.dumps(h) and h['55']['opts'][3] == r'\( 7 : 13 \)' and r'\( ? : \text{MM225}' in h['12']['TEXT'] and 'UQL162, WUR243' in h['18']['TEXT']
    print('ok')
