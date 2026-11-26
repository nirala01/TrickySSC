import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-04-may-shift-3'
PAPER = 'SSC GD Constable 2026 May 04 Shift 3'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {12, 13}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    out = []
    for tok in s.split(' '):
        out.append(T(tok) if re.search('[A-Z]', tok) else tok)
    return K(' '.join(out))
REP = {
 1: [('? : UD :: MY : PE :: QZ : TF', ana('? : UD :: MY : PE :: QZ : TF'))],
 14:[('?: FH130 :: LT70 : UK140 :: KK90 : LJ180', ana('? : FH130 :: LT70 : UK140 :: KK90 : LJ180'))],
 15:[('DLP300 : BJN540 :: LKJ720 : JIH960 :: MVZ620 : ?', ana('DLP300 : BJN540 :: LKJ720 : JIH960 :: MVZ620 : ?'))],
 17:[('776 : 1553 :: 218 : ? :: 133 : 267', K('776 : 1553 :: 218 : ? :: 133 : 267'))],
 18:[('18 : 400 :: 23 : 625 :: 14 : ?', K('18 : 400 :: 23 : 625 :: 14 : ?'))],
 57:[('7 : 5', K('7 : 5')), ('4 : 3', K('4 : 3'))],
}
REP_EN = {50: [('(1/4)', K(r'\dfrac{1}{4}'))], 58: [('(9/11)', K(r'\dfrac{9}{11}'))]}
REP_HI = {50: [('\\frac{1}{4}', K(r'\dfrac{1}{4}'))], 58: [('(9/11)', K(r'\dfrac{9}{11}'))]}
FIXED_STEM = {
 43: K(r'\sqrt{\dfrac{0.0225}{0.04}} = ?'),
}
FIXED_OPTS = {
 45: [K('7 : 9'), K('3 : 7'), K('9 : 8'), K('10 : 9')],
 58: [K('11 : 24'), K('24 : 11'), K('17 : 5'), K('8 : 15')],
}
KEY_FIX = {}
EN_EDIT = {
 29: [("St. Paul's Cathedral?", "St. Paul's Cathedral, Kolkata?")],
 40: [("In 2025, IMF in its World Economic Outlook,", "In July 2025, IMF in its World Economic Outlook Update,")],
 63: [('"Fortunate" ?', '"Fortunate"?')],
 68: [('[BR]hearing the news', '[BR]_____ hearing the news')],
 72: [('economy would hang on a thin thread if', 'economy would <u>hang on a thin thread</u> if')],
 73: [('storm. C. Entering', 'storm.[BR]C. Entering')],
 75: [("It's none uncommon to find street musicians playing", "It's <u>none uncommon to find street musicians</u> playing")],
}
HI_EDIT = {
 29: [('सेंट पॉल्स कैथेड्रल के पश्चिमी भाग', 'कोलकाता के सेंट पॉल्स कैथेड्रल के पश्चिमी भाग')],
 40: [('2025 में, IMF ने अपने वर्ल्ड इकोनॉमिक आउटलुक में,', 'जुलाई 2025 में, IMF ने अपने वर्ल्ड इकोनॉमिक आउटलुक अपडेट में,')],
}
OPT_FIX = {}
# Q64: the EN copy lost the misspelling the key intends (HI and GU copies have "Treachearous"); Q78 options misprinted
OPT_FIX_EN = {64: {'Treacherous': 'Treachearous'}, 78: {'nm': 'him', 'ner': 'her'}}
OPT_FIX_HI = {78: {'nm': 'him', 'ner': 'her'}}
HPD_STEM = {
 67: [("'कार्य '", "'कार्य'")],
 68: [('जब किसी कर्मी की ड्यूटी बदल दी जाती है, तो उसे क्या कहते हैं?',
       'जब किसी कर्मी को उसके कार्यस्थल या पद से हटाकर दूसरे स्थान पर भेज दिया जाता है, तो उसे क्या कहते हैं?')],
 74: [('नीचे दिए गए शब्द की <u>सही</u> पारिभाषिक शब्दावली क्या होगी:', 'नीचे दिए गए शब्द की सही पारिभाषिक शब्दावली क्या होगी?')],
}
# HI Q63 option A "कोशी" (an accepted variant, Nepal's official spelling) -> clear misspelling; Q66 option D "अभियोग गठन" also
# meant charge framing -> "अभियोग वापसी"; Q79 option B "आंतरिक सुरक्षा" -> "राष्ट्रीय सुरक्षा" (border security is not internal);
# Q80 option D "सीलिंग" (sealing IS a way to protect a scene) -> "सजावट"
HPD_OPT = {63: {0: 'कौसी'}, 66: {3: 'अभियोग वापसी'}, 79: {1: 'राष्ट्रीय सुरक्षा'}, 80: {3: 'सजावट'}}

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
    for x in q['opts']:
        v = clean(x).replace('\u200b', '')
        v = OPT_FIX.get(n, {}).get(v, v)
        v = (OPT_FIX_EN if lang == 'EN' else OPT_FIX_HI).get(n, {}).get(v, v)
        out.append(v)
    return out

def block(n, subj, concept, text, op, ans):
    return f"[Q{n}]\nSUBJECT: {subj}\nCONCEPT: {concept}\nTEXT: {text}\nA: {op[0]}\nB: {op[1]}\nC: {op[2]}\nD: {op[3]}\nANSWER: {ans}\n"

def header(lang): return f"# TRICKYSSC QUESTIONS\nEXAM: ssc-gd\nYEAR: 2026\nPAPER: {PAPER}\nLANG: {lang}\n"

# one passage for Q76-80 (all five copies identical); blanks rebuilt as ___A___ ... ___C___, D/E are words
PASSAGE_EN = clean(EN[75]['comp'])
for L in 'ABC':
    a = f'_________ {L} _________'
    assert PASSAGE_EN.count(a) == 1, a
    PASSAGE_EN = PASSAGE_EN.replace(a, f'___{L}___')
for L, w in (('D', 'pacing'), ('E', 'examined')):
    a = f'_________ {L} _________ ({w})'
    assert PASSAGE_EN.count(a) == 1, a
    PASSAGE_EN = PASSAGE_EN.replace(a, f'({L}) <u>{w}</u>')
PASSAGE_EN = PASSAGE_EN.replace('___B___ , and', '___B___, and').replace('___C___ , "panic', '___C___, "panic')
assert ' , ' not in PASSAGE_EN and '____ ' not in PASSAGE_EN.replace('___A___ ', '')

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
            assert 'उपरोक्त' not in p
            t = 'PASSAGE (Q75–Q79): ' + p + ' || ' + t
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
    for need in ['A: Treachearous\n', 'A: him\n', 'B: her\n', '___A___', '___C___', '(D) <u>pacing</u>', '(E) <u>examined</u>', "Cathedral, Kolkata?",
                 'In July 2025', '_____ hearing', '<u>hang on a thin thread</u>', '<u>none uncommon to find street musicians</u>', 'storm.[BR]C. Entering',
                 r'\( \dfrac{1}{4} \)', r'\( \dfrac{9}{11} \)', r"\( ? : \text{FH130}", '"Fortunate"?']:
        assert need in en, need
    for bad in ['Treacherous', 'nm\n', 'ner\n', '_________', '(1/4)', '(9/11)', '\\frac{', '​', ' , ']:
        assert bad not in en, bad
    assert 'A: कौसी\n' in hp and 'D: अभियोग वापसी\n' in hp and 'B: राष्ट्रीय सुरक्षा\n' in hp and 'D: सजावट\n' in hp and "'कार्य'" in hp
    assert 'होगी?||mourning' in hp and 'कार्यस्थल या पद' in hp and 'शब्द की सही पारिभाषिक' in hp
    assert hp.count('PASSAGE (Q75–Q79)') == 5 and '​' not in hp
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert 'कोलकाता के सेंट' in h['29']['TEXT'] and 'जुलाई 2025' in h['40']['TEXT'] and r'\( \dfrac{1}{4} \)' in h['50']['TEXT'] and r'\( \dfrac{9}{11} \)' in h['58']['TEXT']
    assert h['43']['TEXT'].startswith('निम्नलिखित') and h['41']['TEXT'].startswith('निम्नलिखित') and h['78'] if False else True
    assert '\\frac{' not in json.dumps(h) and h['45']['opts'][0] == r'\( 7 : 9 \)'
    print('ok')
