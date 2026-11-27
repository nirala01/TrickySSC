import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-09-may-shift-3'
PAPER = 'SSC GD Constable 2026 May 09 Shift 3'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {11, 12, 18, 19}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 2:[('EIS : JNX :: KZL : PEQ :: ? : VSR', ana('EIS : JNX :: KZL : PEQ :: ? : VSR'))],
 4:[('NS : JM :: RY : NS :: ? : HO', ana('NS : JM :: RY : NS :: ? : HO'))],
 13:[('AF14 : EB196 :: KO15 : ? :: LT17 : SM289', ana('AF14 : EB196 :: KO15 : ? :: LT17 : SM289'))],
 # source "?: :" misprint -> "? ::"
 14:[('KAR220 : LBS340 :: CRT280 : ?: : RSV200 : STW320', ana('KAR220 : LBS340 :: CRT280 : ? :: RSV200 : STW320'))],
 15:[('416 : 877 :: 639 : ? :: 774 : 1235', K('416 : 877 :: 639 : ? :: 774 : 1235'))],
 20:[('1 : 3', K('1 : 3')), ('2 : 5', K('2 : 5'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 42: K(r'\dfrac{0.08}{0.4} - \dfrac{0.024}{0.6} = ?'),
 43: K(r'(7.75 + 2.75)^{2} - 4 \times 7.75 \times 2.75 = ?'),
 46: K(r'(15)^{3} + (5)^{3} + 3 \times 15 \times 5 \times 20 = ?'),
}
FIXED_STEM_L = {
 44: {'EN': r'If \( \sqrt{210.25} = 14.5 \), then what is the value of \( \sqrt{0.00021025} \)?',
      'HI': r'यदि \( \sqrt{210.25} = 14.5 \) है, तो \( \sqrt{0.00021025} \) का मान क्या है?'},
 48: {'EN': r'If \( x = \sqrt{1671 + \sqrt{93 + \sqrt{49}}} \), then what is the value of x?',
      'HI': r'यदि \( x = \sqrt{1671 + \sqrt{93 + \sqrt{49}}} \) है, तो x का मान क्या है?'},
}
FIXED_OPTS = {
 56: [K(r'\dfrac{1}{2}'), K(r'\dfrac{3}{8}'), K(r'\dfrac{5}{9}'), K(r'\dfrac{4}{9}')],
}
KEY_FIX = {}
EN_EDIT = {
 # four separate underlines restored (source had none)
 63: [('as prolonged droughts', 'as <u>prolonged</u> droughts'), ('from cereals to', 'from <u>cereals</u> to'),
      ('—promting many', '—<u>promting</u> many'), ('explore diversified income', 'explore <u>diversified</u> income')],
 75: [('The employees, having completing the rigorous training program, felt', '<u>The employees, having completing the rigorous training program,</u> felt')],
}
HI_EDIT = {}
# Q1 option D was an image of the letter "B"; Q4 option A "L" was truncated (all others are two-letter clusters) -> "LT" (does not fit; key D LU kept);
# Q5 option C braces "{EI, GO, IN}" -> "(EI, GO, IN)"; Q58 option A "3:2" padded like the other three
OPT_FIX = {1: {'#D': 'B'}, 4: {'L': 'LT'}, 5: {'{EI, GO, IN}': '(EI, GO, IN)'}, 58: {'3:2': '3 : 2'}}
OPT_FIX_EN = {}
OPT_FIX_HI = {24: {}}
HI_STEM_FIX = {24: [('चंद्र पुरस्कर', 'चंद्र पुरस्कार')]}
HPD_STEM = {
 61: [('नीचे दिए गये वाक्य में किस प्रकार की अशुद्धि है:', 'नीचे दिए गए वाक्य में किस प्रकार की अशुद्धि है?')],
 62: [('नीचे दिए गये वाक्य में किस प्रकार की अशुद्धि है:', 'नीचे दिए गए वाक्य में किस प्रकार की अशुद्धि है?')],
 63: [('निम्नलिखित में वाक्य के शुद्ध रूप का चयन करें:', 'निम्नलिखित में से वाक्य के शुद्ध रूप का चयन कीजिए।')],
 64: [("'अदालती कार्यवाही' का उपयुक्त अंग्रेज़ी पारिभाषिक शब्द है:", "'अदालती कार्यवाही' का उपयुक्त अंग्रेज़ी पारिभाषिक शब्द क्या है?")],
 # bare "लगाए गए नियमों" also fitted आदेश
 65: [('कार्यालय में सुरक्षा कर्मियों के लिए लगाए गए नियमों को क्या कहते हैं?', 'कार्यालय में सुरक्षा कर्मियों के लिए लिखित रूप में तय किए गए नियमों के संग्रह को क्या कहते हैं?')],
 # leaving early is not by itself "disobedience"; the stem now says he left against the officer's order
 67: [('अगर कोई सुरक्षा कर्मी समय से पहले कार्यालय छोड़ देता है, तो यह क्या माना जाता है?', 'अगर कोई सुरक्षा कर्मी अधिकारी के स्पष्ट आदेश के बावजूद बिना अनुमति समय से पहले ड्यूटी छोड़ देता है, तो यह क्या माना जाता है?')],
 # "कानून की सीमाओं का उल्लंघन" fitted कानूनी अतिक्रमण / कानून भंग as well as the key
 72: [('जब कोई अधिकारी कानून की सीमाओं का उल्लंघन करके कार्य करे, तो उसे क्या कहा जाता है?', "'Violation of an Act' के लिए उपयुक्त हिंदी पारिभाषिक शब्द क्या है?")],
}
# Q63 C "गूथ" (an accepted variant of गूँथ) -> "गूँध" (गूँधना = to knead) so only the key A is correct; Q75 B made precise
HPD_OPT = {63: {2: 'राधा ने माला गूँध ली'}, 75: {1: 'कानून की किसी धारा का उप-भाग'}}
# the Q76-Q80 passage is MISSING in the source (comp empty in en/hi/gu) - our own, written to the five questions
HPD_PASSAGE = ('किसी भी क्षेत्र की सुरक्षा योजना बनाने से पहले उस क्षेत्र का गहन विश्लेषण आवश्यक होता है। क्षेत्रीय विश्लेषण का आधार उस क्षेत्र की '
 'सामाजिक संरचना, भौगोलिक स्थिति और जनसंख्या घनत्व होते हैं। घनी आबादी वाले किसी शहरी बाज़ार की सुरक्षा ज़रूरतें किसी दूरस्थ पहाड़ी गाँव या '
 'सीमावर्ती जंगल से बिल्कुल अलग होती हैं। इसलिए सुरक्षा रणनीतियाँ स्थानीय परिस्थितियों के आधार पर तय की जाती हैं। एक ही नीति को हर स्थान पर '
 'समान रूप से लागू करना उचित नहीं माना जाता, क्योंकि हर क्षेत्र की स्थानीय आवश्यकताएँ अलग होती हैं। जब पुलिस और सुरक्षा बल स्थानीय लोगों, '
 'भू-भाग और अपराध के स्वरूप को समझकर योजना बनाते हैं, तो एक स्थानीयकृत और अनुकूल सुरक्षा प्रणाली बनती है, जो बदलती परिस्थितियों के अनुसार '
 'स्वयं को ढाल लेती है। यह दृष्टिकोण क्षेत्र-आधारित रणनीतिक सोच का उदाहरण है, जिसमें केवल अपराध दर या केवल तकनीकी संसाधनों पर नहीं, बल्कि '
 'पूरे क्षेत्र की वास्तविक स्थिति पर ध्यान दिया जाता है।')

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
PASSAGE_EN = clean(EN[75]['comp'])
assert PASSAGE_EN.startswith("India's startup ecosystem")
assert all(not HI[i]['comp'] for i in range(80, 100))

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
