import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-18-may-shift-1'
PAPER = 'SSC GD Constable 2026 May 18 Shift 1'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {6, 7, 17, 18, 19}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 8:[('TK460 : SN360 :: PR320 : ? :: JQ210 : IT110', ana('TK460 : SN360 :: PR320 : ? :: JQ210 : IT110'))],
 9:[('LPR110 : KOQ210 :: PRT40 : ? :: ZKW90 : YJV190', ana('LPR110 : KOQ210 :: PRT40 : ? :: ZKW90 : YJV190'))],
 10:[('3249 : 3289 :: 3658 : 3698 :: ? : 8635', K('3249 : 3289 :: 3658 : 3698 :: ? : 8635'))],
 # source "?: 1836" -> "? : 1836"
 11:[('?: 1836 :: 523 : 1050 :: 513 : 1030', K('? : 1836 :: 523 : 1050 :: 513 : 1030'))],
 20:[('1 : 5', K('1 : 5'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 43: K(r'\dfrac{8(4.5)^{3} - 1}{(10)^{2} - 9} = ?'),
 45: K(r'(\sqrt{6} + \sqrt{2}) + \dfrac{1}{\sqrt{6} - \sqrt{2}} = ?'),
 49: K(r'(460 + 240)^{2} - 4 \times 460 \times 240 = ?'),
}
FIXED_STEM_L = {
 44: {'EN': r'If \( \sqrt{x} = \dfrac{100}{\sqrt{2025}} \), then what is the value of x?',
      'HI': r'यदि \( \sqrt{x} = \dfrac{100}{\sqrt{2025}} \) है, तो x का मान क्या है?'},
}
FIXED_OPTS = {
 44: [K(r'\dfrac{100}{81}'), K(r'\dfrac{400}{81}'), K(r'\dfrac{250}{81}'), K(r'\dfrac{900}{81}')],
 # source option A had a stray ")" after the KaTeX span
 45: [K(r'\dfrac{5}{4}(\sqrt{6} + \sqrt{2})'), K(r'\dfrac{3}{2}(\sqrt{6} + \sqrt{2})'), K(r'\dfrac{7}{4}(\sqrt{6} + \sqrt{2})'), K(r'2(\sqrt{6} + \sqrt{2})')],
 46: [K(r'10\sqrt{2}'), '40', K(r'10\sqrt{3}'), K(r'7\sqrt{2}')],
}
KEY_FIX = {}
EN_EDIT = {
 75: [('at the art of running with the hounds and hunting with the hare.', 'at the art of <u>running with the hounds and hunting with the hare</u>.')],
 76: [('The following question refers to the passage provided: ', '')],
 # all four options were true of the passage; the stem now asks for the direct statement about the material side (key A kept)
 78: [('In what ways does the passage reconceptualize the American Dream beyond just attaining material success?',
       'Which of the following restates what the passage directly says about the material side of the American Dream?')],
}
HI_EDIT = {}
OPT_FIX = {}
# Q65 had NO misspelt word (all four correct) - the GU copy keeps the misspelling the key intends; Q66 "Partia" -> "Partial";
# Q79 option B was a near-paraphrase of the passage ("recognised regardless of birth") -> a clearly wrong option (key D kept)
OPT_FIX_EN = {65: {'Miscellaneous': 'Miscellanious'}, 66: {'Partia': 'Partial'},
              79: {'Hard work and talent should be recognized regardless of background': 'Luck matters more than ability or achievement'}}
OPT_FIX_HI = {}
# "6 गुना अधिक कुशल" read as 7 times; EN says "6 times as good"
HI_STEM_FIX = {57: [('6 गुना अधिक कुशल', '6 गुना कुशल')]}
HPD_STEM = {
 64: [('निम्न में से कौन-सा एक उद्धरण का चिन्ह है?', 'निम्न में से कौन-सा उद्धरण चिह्न है?')],
 65: [('"अपराध का तरीका" का सही तकनीकी शब्द है:', '"अपराध का तरीका" के लिए सही तकनीकी (अंग्रेज़ी) शब्द क्या है?')],
 # समय पत्रक (time sheet) also fitted "ड्यूटी के समय का चार्ट"
 66: [('सुरक्षा कर्मी की ड्यूटी के समय का चार्ट क्या कहलाता है?', 'सुरक्षा कर्मियों की ड्यूटी का समय, स्थान और पाली (शिफ्ट) दर्शाने वाली तालिका क्या कहलाती है?')],
 # the bare stem gave the key away and सजा also fitted
 68: [('सुरक्षा कर्मी की गलती पर जो चेतावनी दी जाती है, वह क्या कहलाती है?', 'सुरक्षा कर्मी की गलती पर उसे सुधार के लिए लिखित रूप में दी जाने वाली चेतावनी क्या कहलाती है?')],
 69: [('किसी अपराध स्थल को घेरने और साक्ष्य जुटाने की प्रक्रिया क्या होती है?', 'अपराध होने के बाद पुलिस द्वारा उसी स्थान पर पहुँचकर उसे घेरने और वहाँ से साक्ष्य जुटाने की प्रक्रिया क्या कहलाती है?')],
 76: [('इससे व्यवस्था में क्या वृद्धि होती है?', 'गद्यांश के अनुसार, संस्थाओं के नैतिक मानकों पर कार्य करने से व्यवस्था में किसकी वृद्धि होती है?')],
 # the bare stem gave the key away (सुरक्षा जानकारी) and जन/सार्वजनिक सूचना also fitted
 79: [('पुलिस द्वारा नागरिकों को दी गई सुरक्षा जानकारी क्या कहलाती है?', 'पुलिस द्वारा नागरिकों को चोरी, ठगी या किसी खतरे से बचाव के बारे में दी जाने वाली जानकारी क्या कहलाती है?')],
 # पुष्टि पत्र / सत्यापन पत्र also fitted "लिखित पुष्टि"; the stem now asks for the act, not the letter
 80: [('पुलिस द्वारा किसी कार्य की लिखित पुष्टि क्या कहलाती है?', 'पुलिस द्वारा किसी दस्तावेज़ या तथ्य को जाँचकर उसके सही होने की आधिकारिक पुष्टि करना क्या कहलाता है?')],
}
# Q63 options A and C were both "खदान" -> A "खद्दान"; Q65 D "Pattern of offence" (a literal gloss of the stem) -> "Nature of offence";
# Q69 A छानबीन (a general word for investigation) -> गश्त; Q79 A/B जन सूचना / सार्वजनिक सूचना -> गुप्त सूचना / अपराध सूचना
HPD_OPT = {63: {0: 'खद्दान'}, 65: {3: 'Nature of offence'}, 69: {0: 'गश्त'}, 79: {0: 'गुप्त सूचना', 1: 'अपराध सूचना'}}
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
assert all(EN[i]['comp'] == EN[75]['comp'] for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
PASSAGE_EN = re.sub(r'^<u>Read the following passage carefully and answer the questions based on the passage:\s*</u>\[BR\]', '', clean(EN[75]['comp']))
assert PASSAGE_EN.startswith("Most of us understand the American Dream")
assert all(HI[i]['comp'] == HI[93]['comp'] for i in range(93, 98)) and all(not HI[i]['comp'] for i in list(range(80, 93)) + [98, 99])
HPD_PASSAGE = clean(HI[93]['comp'])
assert HPD_PASSAGE.startswith('आंतरिक सुरक्षा में नैतिकता')

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
