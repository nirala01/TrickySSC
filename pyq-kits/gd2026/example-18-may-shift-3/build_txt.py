import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-18-may-shift-3'
PAPER = 'SSC GD Constable 2026 May 18 Shift 3'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {6, 7, 17, 18, 19}            # [FIGURE-BASED] stems
FIGOPT = {6, 7, 17, 18, 19}         # options are figures too
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 # second letters of the series fall -4, -5, -6 ... -10, so the sixth term is DY (G - 8 = Y), not DV (key NC unchanged)
 1:[(', DV, ', ', DY, ')],
 8:[('TT250 : QQ204 :: JP354 : ? :: MS444 : PJ398', ana('TT250 : QQ204 :: JP354 : ? :: MS444 : PJ398'))],
 9:[('ACK320 : FFB420 :: DLM140 : ? :: PSJ180 : EVQ280', ana('ACK320 : FFB420 :: DLM140 : ? :: PSJ180 : EVQ280'))],
 10:[('?: 5011 :: 4146 : 4188 :: 2034 : 2076', K('? : 5011 :: 4146 : 4188 :: 2034 : 2076'))],
 11:[('2655 : 887 :: ? : 461 :: 2694 : 900', K('2655 : 887 :: ? : 461 :: 2694 : 900'))],
 20:[('5 : 3', K('5 : 3')), ('7 : 5', K('7 : 5'))],
 53:[('2 : 5', K('2 : 5'))],
 58:[('1/6', K(r'\dfrac{1}{6}'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 43: K(r'\sqrt[3]{2.197} \times \sqrt{1.21} = ?'),
 49: K(r'\sqrt{\sqrt{400} + \sqrt{25}} = ?'),
}
FIXED_STEM_L = {
 44: {'EN': 'If ' + K(r'x = \sqrt{225} \div \sqrt{25} + \sqrt{81}') + ', then what is the value of 2x?',
      'HI': 'यदि ' + K(r'x = \sqrt{225} \div \sqrt{25} + \sqrt{81}') + ' है, तो 2x का मान क्या है?'},
}
FIXED_OPTS = {}
KEY_FIX = {}
EN_EDIT = {
 # EPI 2024 ranks China 154th (Table ES-1); stem garbled
 40: [('China ranked has been ____ in the Environment Performance Index 2024.', 'China was ranked ____ in the Environmental Performance Index 2024.')],
 # "4 times more than B" could also mean 5 times B or 4 times B; key 80% needs A = 5B
 54: [('If A is 4 times more than B,', 'If A is 5 times B,')],
 # "increased saving" could mean the increase in saving (that gives Rs. 30000, not an option); key Rs. 10000 = new saving
 56: [('The increased saving is Rs. 7500.', 'His saving after the increase is Rs. 7500.')],
 61: [('has the meaning? Wealthy', 'has the meaning?||Wealthy')],
 62: [('has the meaning? The entirety', 'has the meaning?||The entirety')],
 67: [('for the following. A person', 'for the following.||A person')],
 68: [('for the following. The use', 'for the following.||The use')],
 75: [('tried for vain to make amends', '<u>tried for vain to make amends</u>')],
}
HI_EDIT = {
 54: [('यदि A, B से 4 गुना अधिक है,', 'यदि A, B का 5 गुना है,')],
 56: [('बढ़ी हुई बचत 7500 रुपये है।', 'वृद्धि के बाद उसकी बचत 7500 रुपये है।')],
}
# Q3 option C "G|" is a misprint of "GI" (both languages)
OPT_FIX = {3: {'G|': 'GI'}}
# Q40: China was 154th in EPI 2024, so option A 156th -> 154th (key A kept); "111st" -> "111th"
# Q63: "Abrogate" is also correctly spelt - the HI/GU copies keep "Abrogiate" (key Apropos)
OPT_FIX_EN = {40: {'156th': '154th', '111st': '111th'}, 63: {'Abrogate': 'Abrogiate'}}
OPT_FIX_HI = {40: {'156वाँ': '154वाँ'}}
HI_STEM_FIX = {}
HPD_STEM = {
 61: [('किसी एक <u>सही</u> वर्तनी', 'किसी एक सही वर्तनी')],
 62: [('किसी एक <u>सही</u> वर्तनी', 'किसी एक सही वर्तनी')],
 63: [('<u>शुद्ध</u> शब्द', 'शुद्ध शब्द')],
 64: [('कौन-सा एक विस्मयादिबोधक का चिन्ह है?', 'कौन-सा विस्मयादिबोधक चिह्न है?')],
 65: [("कौन-सा 'साक्ष्य का दबाव' का <u>सही</u> तकनीकी शब्द है?", "कौन-सा 'साक्ष्य का भार' के लिए सही तकनीकी (अंग्रेज़ी) शब्द है?")],
 # the bare stem gave the key away and स्थानांतरण also loosely fitted "भेजा जाता है"
 66: [('जब सुरक्षा कर्मी को प्रशिक्षण के लिए भेजा जाता है, तो यह क्या होता है?', 'सुरक्षा कर्मी को प्रशिक्षण पर भेजने के लिए जारी किया गया आधिकारिक लिखित आदेश क्या कहलाता है?')],
 # ड्यूटी डायरी also shows where a person is on duty
 68: [('किस दस्तावेज़ से पता चलता है कि कर्मी कहाँ तैनात है?', 'किसी कर्मी को किसी विशेष स्थान या ड्यूटी पर तैनात करने के लिए जारी किया गया आधिकारिक दस्तावेज़ क्या कहलाता है?')],
 79: [('इस व्यवस्था से कौन-सी स्थिति कम होती है?', 'गद्यांश के अनुसार, स्पष्ट समन्वय से किसकी स्थिति कम होती है?')],
}
# Q63 B घबड़ाना is an accepted variant of घबराना -> a plain misspelling; Q79 C देरी (faster decisions also cut delay) -> अनुशासन
HPD_OPT = {63: {1: 'घभराना'}, 79: {2: 'अनुशासन'}}
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

# one RC passage for Q76-80 (all five copies identical); the generic instruction line is dropped
assert all(EN[i]['comp'] == EN[75]['comp'] for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
PASSAGE_EN = re.sub(r'^(<u>)?Read the following passage carefully and answer the questions based on the passage:\s*(</u>)?\[BR\]', '', clean(EN[75]['comp']))
assert PASSAGE_EN.startswith("Inclusive education revolves")
assert all(HI[i]['comp'] == HI[95]['comp'] for i in range(95, 100)) and all(not HI[i]['comp'] for i in range(80, 95))
HPD_PASSAGE = clean(HI[95]['comp'])
assert HPD_PASSAGE.startswith('आंतरिक सुरक्षा व्यवस्था में')

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
    print('ok')
