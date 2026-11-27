import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-19-may-shift-2'
PAPER = 'SSC GD Constable 2026 May 19 Shift 2'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {6, 7, 17, 18, 19, 38}   # [FIGURE-BASED] stems
FIGOPT = {6, 7, 17, 18, 19}    # options are figures too (Q38: photo stem, text options)
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 # 6th term GJ is a misprint of GI (second letters fall -4, -5 ... -10: Q - 8 = I, I - 9 = Z)
 3:[(', GJ, LZ,', ', GI, LZ,')],
 8:[('AD182 : GD90 :: ET202 : ? :: FK312 : NI220', ana('AD182 : GD90 :: ET202 : ? :: FK312 : NI220'))],
 9:[('? : FTJ42 :: AKM32 : DNJ64 :: DMO26 : GPL52', ana('? : FTJ42 :: AKM32 : DNJ64 :: DMO26 : GPL52'))],
 10:[('854 : 803 :: 2210 : 2159 :: ? : 9585', K('854 : 803 :: 2210 : 2159 :: ? : 9585'))],
 11:[('151 : 299 :: 446 : 889 :: ? : 1641', K('151 : 299 :: 446 : 889 :: ? : 1641'))],
 20:[('5 : 12', K('5 : 12'))],
 58:[('2 : 3 : 4', K('2 : 3 : 4'))],
}
REP_EN = {35: [('I. Rabi II. Kharif', 'I. Rabi[BR]II. Kharif')]}
REP_HI = {35: [('I. रबी II. खरीफ', 'I. रबी[BR]II. खरीफ')]}
FIXED_STEM = {
 43: K(r'\sqrt[3]{0.027} + \sqrt{0.49} + \sqrt[3]{0.064} - \sqrt[3]{0.216} = ?'),
 45: K(r'\sqrt{\dfrac{0.16}{0.0004}} \times \sqrt{\dfrac{0.25}{0.49}} = ?'),
 49: K(r'2[(412)^{2} + (188)^{2}] - (412 - 188)^{2} = ?'),
}
# Q44: source radicand 0.00000030625 (6 zeros) has no square root among the options; 0.000175^2 = 0.000000030625 (7 zeros)
FIXED_STEM_L = {
 44: {'EN': 'If ' + K(r'\sqrt{306.25} = 17.5') + ', then what is the value of ' + K(r'\sqrt{0.000000030625}') + '?',
      'HI': 'यदि ' + K(r'\sqrt{306.25} = 17.5') + ' है, तो ' + K(r'\sqrt{0.000000030625}') + ' का मान क्या है?'},
}
FIXED_OPTS = {
 45: [K(r'\dfrac{100}{7}'), K(r'\dfrac{90}{7}'), K(r'\dfrac{100}{49}'), K(r'\dfrac{20}{7}')],
}
KEY_FIX = {}
EN_EDIT = {
 # Nallamalai is a range OF the Eastern Ghats, not another name for them; key D kept
 22: [('The Eastern Ghats are also known by which of the following names?', 'Which of the following hill ranges is a part of the Eastern Ghats in Andhra Pradesh?')],
 # the Third Plan (1961-66) ran its full term; it was hit by the 1962 and 1965 wars and followed by Plan Holidays; key C kept
 25: [('Which plan was terminated one year before completion due to the Indo-China war?', 'Which Five-Year Plan was badly affected by the Indo-China war of 1962 and was followed by the Plan Holidays (1966–69)?')],
 # "increased saving" read as the increase gives Rs. 13823.5, not an option; key Rs. 5000 needs the new saving
 56: [('The increased saving is Rs. 4700.', 'His saving after the increase is Rs. 4700.')],
 75: [('You need to come to terms with the fact that', 'You need to <u>come to terms with the fact</u> that')],
}
HI_EDIT = {
 22: [('पूर्वी घाट को निम्नलिखित में से किस अन्य नाम से भी जाना जाता है?', 'निम्नलिखित में से कौन-सी पहाड़ियाँ आंध्र प्रदेश में पूर्वी घाट का भाग हैं?')],
 25: [('भारत-चीन युद्ध के कारण कौन सी योजना अपने पूरा होने से एक वर्ष पहले समाप्त कर दी गई थी?', '1962 के भारत-चीन युद्ध से कौन-सी पंचवर्षीय योजना बुरी तरह प्रभावित हुई थी, जिसके बाद योजना अवकाश (1966–69) आया?')],
 56: [('बढ़ी हुई बचत 4700 रुपये है।', 'वृद्धि के बाद उसकी बचत 4700 रुपये है।')],
}
# Q2 B "7R" -> "ZR"; Q12 "In ta"/"Im ta" (capital I) -> "ln ta"/"lm ta" (the codes are ln, lm); Q4 D spacing; Q20/Q55 ratio spacing;
# Q30 official key C "64900" was WRONG (PIB: 84,902 SSWs validated till August 2025) -> options A and C swapped, key C kept
OPT_FIX = {2: {'7R': 'ZR'}, 4: {'(AW,YU,VN)': '(AW, YU, VN)'}, 12: {'In ta': 'ln ta', 'Im ta': 'lm ta'},
           20: {'1:3': '1 : 3', '7:9': '7 : 9'}, 55: {'3:1': '3 : 1'}, 30: {'84902#A': '64900', '64900#C': '84902'}}
# Q63 D "Jocular" is ALSO correctly spelt -> "Jokular" so only the key B is correct; Q69 D "n" -> "in"
OPT_FIX_EN = {63: {'Jocular': 'Jokular'}, 69: {'n': 'in'}}
OPT_FIX_HI = {}
HI_STEM_FIX = {}
HPD_STEM = {
 64: [('निम्न में से कौन-सा एक अल्पविराम का चिन्ह है?', 'निम्न में से कौन-सा अल्पविराम का चिह्न है?')],
 65: [("'अभियोजन का अधिकार क्षेत्र' का सही तकनीकी शब्द है?", "'अभियोजन का अधिकार क्षेत्र' के लिए सही तकनीकी (अंग्रेज़ी) शब्द है?")],
 # नियुक्ति पत्र fitted "appoint for a special task" better than the key स्थानांतरण पत्र
 67: [('किस पत्र से अधिकारी किसी विशेष कार्य के लिए कर्मी को नियुक्त करता है?', 'किस पत्र द्वारा अधिकारी किसी कर्मी को उसके वर्तमान स्थान से हटाकर दूसरे स्थान पर कार्य के लिए भेजता है?')],
 79: [('पुलिस कर्मियों के कार्य क्षेत्र को क्या कहा जाता है?', 'पुलिस कर्मियों को जिस क्षेत्र में अपना कार्य करना होता है, उसे एक शब्द में क्या कहा जाता है?')],
}
# Q72 C incomplete "एकत्र" -> "एकत्र करना"; Q79 B/D "सेवा क्षेत्र"/"ड्यूटी क्षेत्र" also fitted -> "आवास क्षेत्र"/"विश्राम क्षेत्र";
# Q80 B/C/D were synonyms of the key (जानकारी संग्रह, डेटा संकलन, विवरण संग्रह) -> "सूचना प्रसारण"/"सूचना विलोपन"/"सूचना वितरण"
HPD_OPT = {72: {2: 'सुरक्षा योजना के लिए जानकारी एकत्र करना'}, 79: {1: 'आवास क्षेत्र', 3: 'विश्राम क्षेत्र'},
           80: {1: 'सूचना प्रसारण', 2: 'सूचना विलोपन', 3: 'सूचना वितरण'}}
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

# one RC passage for Q76-80 (all five copies identical); the inline instruction line is dropped, and the sentence the source
# repeats ("As long as human nature remains as it is, ...") is kept once
assert all(EN[i]['comp'] == EN[75]['comp'] for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
PASSAGE_EN = re.sub(r'^(<u>)?Read the following passage carefully and answer the questions based on the passage:\s*(</u>)?(\[BR\])?\s*', '', clean(EN[75]['comp']))
DUP = ' As long as human nature remains as it is, physical needs will continue, and suffering will persist.'
assert DUP in PASSAGE_EN; PASSAGE_EN = PASSAGE_EN.replace(DUP, '', 1)
assert PASSAGE_EN.startswith("The miseries of the world")
# Hindi Part D passage is Q74-Q78 (hi[93..97]); Q61-Q73, Q79, Q80 standalone
assert all(HI[i]['comp'] == HI[93]['comp'] for i in range(93, 98)) and all(not HI[i]['comp'] for i in list(range(80, 93)) + [98, 99])
HPD_PASSAGE = clean(HI[93]['comp'])
assert HPD_PASSAGE.startswith("आंतरिक सुरक्षा तंत्र में प्रशिक्षण मूल्यांकन")

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
