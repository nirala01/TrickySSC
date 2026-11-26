import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-08-may-shift-1'
PAPER = 'SSC GD Constable 2026 May 08 Shift 1'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {9, 10}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 11:[('ZP54 : BR108 :: CR60 : ET120 :: ? : ZL126', ana('ZP54 : BR108 :: CR60 : ET120 :: ? : ZL126'))],
 12:[('RKB110 : ENU330 :: CLM220 : POF440 :: DSJ140 : ?', ana('RKB110 : ENU330 :: CLM220 : POF440 :: DSJ140 : ?'))],
 13:[('9058 : 9106 :: 7804 : 7852 :: ? : 7472', K('9058 : 9106 :: 7804 : 7852 :: ? : 7472'))],
 14:[('530 : ? :: 561 : 2253 :: 859 : 3445', K('530 : ? :: 561 : 2253 :: 859 : 3445'))],
 57:[('2/3', K(r'\dfrac{2}{3}'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 44: K(r'\dfrac{(0.7)^{4} - (0.3)^{4}}{(0.7)^{2} - (0.3)^{2}} = ?'),
 50: K(r'1^{2} + 2^{2} + 3^{2} + \ldots + 60^{2} = ?'),
}
FIXED_STEM_L = {
 45: {'EN': r'If \( x = \sqrt{100} \div \sqrt{25} + \sqrt{64} \), then what is the value of 2x?',
      'HI': r'यदि \( x = \sqrt{100} \div \sqrt{25} + \sqrt{64} \) है, तो 2x का मान क्या है?'},
 46: {'EN': r'If \( \sqrt{20.25} + \sqrt{16 + x} = 9.5 \), then what is the value of x?',
      'HI': r'यदि \( \sqrt{20.25} + \sqrt{16 + x} = 9.5 \) है, तो x का मान क्या है?'},
}
FIXED_OPTS = {
 49: ['P − 14', 'P − 21', 'P − 18', 'P − 17'],
 60: [K(r'\dfrac{3}{2}'), K(r'\dfrac{5}{3}'), K(r'\dfrac{6}{5}'), K(r'\dfrac{7}{5}')],
}
KEY_FIX = {}
# Q34: the real names are the "5th Marine Fisheries Census" and the "Coastal States Fisheries Meet 2025" (Mumbai, 28 Apr 2025)
EN_EDIT = {
 34: [('5th Marine Census in the "Coastal state fisheries conference 2025"', '5th Marine Fisheries Census at the "Coastal States Fisheries Meet 2025"')],
}
HI_EDIT = {
 34: [('5वीं समुद्री जनगणना', '5वीं समुद्री मत्स्य जनगणना')],
 57: [('4 गुना अधिक कार्यकुशल', '4 गुना कार्यकुशल')],
}
# Q17 option "0X414" (zero) -> "OX414" as in the stem; Q22 "Vijayakalakshmi" -> "Vijaya Lakshmi" (HI already विजया लक्ष्मी)
# Q63: HI/GU copies keep the misspellings "Gregarous"/"Glutony" the key intends; EN had three correct spellings
# Q71: en/hi/gu cidx = B "with" but Testbook's solution says "to"; "affectionate to/towards" is also standard -> C "to" -> "at", key B kept
OPT_FIX = {17: {'0X414': 'OX414'}}
OPT_FIX_EN = {22: {'Vijayakalakshmi Pandit': 'Vijaya Lakshmi Pandit'}, 63: {'Gregarious': 'Gregarous', 'Gluttony': 'Glutony'}, 71: {'to#C': 'at'}}
OPT_FIX_HI = {}
HPD_STEM = {
 61: [('किस चिन्ह का प्रयोग हुआ है-[BR]', 'किस चिह्न का प्रयोग हुआ है?[BR]')],
 62: [('किस चिन्ह का प्रयोग हुआ है-[BR]', 'किस चिह्न का प्रयोग हुआ है?[BR]')],
 63: [('कौन-सा चिन्ह लोप चिन्ह को', 'कौन-सा चिह्न लोप चिह्न को')],
 64: [('का सही तकनीकी शब्द है:', 'का सही तकनीकी (अंग्रेज़ी) शब्द क्या है?')],
 # पोस्टर / विज्ञापन also fitted "सूचना को दीवार पर लगाने के लिए"
 65: [('किसी महत्वपूर्ण सूचना को दीवार पर लगाने के लिए क्या उपयोग किया जाता है?',
       'कार्यालय या थाने में महत्वपूर्ण सूचनाएँ और आदेश सबके पढ़ने के लिए लगाने हेतु दीवार पर स्थायी रूप से लगाया गया बोर्ड क्या कहलाता है?')],
 72: [('क्या होगा:[BR]', 'क्या होगी?[BR]')],
}
# Q62 C पूर्ण विराम (the sentence ends with one) -> विस्मयादिबोधक चिह्न; Q69 B "जप्ती" -> "जब्ती"; Q79 D "केंद्रकृत" -> "केंद्रीकृत"
HPD_OPT = {62: {2: 'विस्मयादिबोधक चिह्न'}, 69: {1: 'जब्ती'}, 79: {3: 'केंद्रीकृत सोच'}}

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
PASSAGE_EN = PASSAGE_EN[len(INSTR):].replace('higher- income', 'higher-income')
HPD_PASSAGE = clean(HI[94]['comp'])
assert all(clean(HI[i]['comp']) == HPD_PASSAGE for i in range(94, 99)) and all(not HI[i]['comp'] for i in list(range(80, 94)) + [99])

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
        if 75 <= n <= 79:
            t = 'PASSAGE (Q75–Q79): ' + HPD_PASSAGE + ' || ' + t
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
    for need in [r'\( \text{ZP54} : \text{BR108} ::', r'\( \text{RKB110} : \text{ENU330}', r'\( 9058 : 9106 :: 7804 : 7852 :: ? : 7472 \)', r'\( 530 : ? :: 561 : 2253 :: 859 : 3445 \)',
                 'B: OX414\n', 'D: Vijaya Lakshmi Pandit\n', 'A: Gregarous\n', 'C: Glutony\n', 'A: of\nB: with\nC: at\nD: by\n', r'\( \dfrac{(0.7)^{4}', r'+ \ldots + 60^{2}',
                 r'If \( x = \sqrt{100} \div', r'If \( \sqrt{20.25} + \sqrt{16 + x} = 9.5 \)', r'A: \( 3 : 2 \)', r'A: \( \dfrac{3}{2} \)', 'A: P − 14\n', r'complete \( \dfrac{2}{3} \) part',
                 'Marine Fisheries Census at the "Coastal States Fisheries Meet 2025"', 'TEXT: [FIGURE-BASED] Two figures', 'PASSAGE (Q76–Q80): Poverty, unemployment', 'higher-income groups']:
        assert need in en, need
    for bad in ['\\frac{', '​', 'A: \n', 'C: \n', 'D: \n', '0X414', '\\rm', 'Read the following passage', 'higher- income', 'Gregarious', 'C: to\n']:
        assert bad not in en, bad
    assert en.count('[FIGURE-BASED]') == 2 and en.count('(figure 1)') == 2 and en.count('PASSAGE (Q76–Q80)') == 5
    assert hp.count('PASSAGE (Q75–Q79): आंतरिक सुरक्षा में जोखिम') == 5 and '​' not in hp and 'चिन्ह' not in hp
    for need in ['चिह्न का प्रयोग हुआ है?||वृक्षों पर', 'चिह्न का प्रयोग हुआ है?||हाँ, लिख', 'C: विस्मयादिबोधक चिह्न\n', 'B: जब्ती\n', 'D: केंद्रीकृत सोच\n', 'क्या होगी?||notice of motion',
                 'स्थायी रूप से लगाया गया बोर्ड', 'शब्द क्या है?\n']:
        assert need in hp, need
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['17']['opts'][1] == 'OX414' and h['9']['opts'] == ['(figure 1)', '(figure 2)', '(figure 3)', '(figure 4)'] and '4 गुना कार्यकुशल' in h['57']['TEXT']
    assert h['41']['TEXT'].startswith('निम्नलिखित') and h['44']['TEXT'].startswith('निम्नलिखित') and h['45']['TEXT'].startswith('यदि \\(') and h['60']['opts'][0] == r'\( \dfrac{3}{2} \)'
    assert r'\( \text{ZP54}' in h['11']['TEXT'] and r'\( \dfrac{2}{3} \)' in h['57']['TEXT'] and 'मत्स्य जनगणना' in h['34']['TEXT'] and h['47']['opts'][0] == r'\( 3 : 2 \)'
    assert '\\frac' not in json.dumps(h) and '\\rm' not in json.dumps(h)
    print('ok')
