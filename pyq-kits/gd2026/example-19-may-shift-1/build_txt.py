import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-19-may-shift-1'
PAPER = 'SSC GD Constable 2026 May 19 Shift 1'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {18, 19, 20}            # [FIGURE-BASED] stems
FIGOPT = {18, 19, 20}         # options are figures too
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 10:[('KK780 : OO420 :: ? : TZ130 :: AG510 : EK150', ana('KK780 : OO420 :: ? : TZ130 :: AG510 : EK150'))],
 11:[('TU100 : PO150 :: VW120 : ? :: JK140 : FE210', ana('TU100 : PO150 :: VW120 : ? :: JK140 : FE210'))],
 12:[('9243 : 9198 :: 7921 : 7876 :: ? : 7869', K('9243 : 9198 :: 7921 : 7876 :: ? : 7869'))],
 13:[('469 : 149 :: 551 : ? :: 892 : 572', K('469 : 149 :: 551 : ? :: 892 : 572'))],
 45:[('5 : 2', K('5 : 2')), ('5 : 4', K('5 : 4'))],
 47:[('(13/18)', K(r'\dfrac{13}{18}'))],
 54:[('2 : 5', K('2 : 5'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 46: K(r'9\dfrac{1}{2} + 99\dfrac{1}{6} + 999\dfrac{1}{12} + 9999\dfrac{1}{20} = ?'),
}
FIXED_STEM_L = {}
FIXED_OPTS = {
 46: [K(r'11106\dfrac{4}{5}'), K(r'11106\dfrac{5}{7}'), K(r'11106\dfrac{3}{5}'), K(r'11106\dfrac{7}{9}')],
 47: [K(r'\dfrac{7}{9}'), K(r'\dfrac{5}{6}'), K(r'\dfrac{11}{15}'), K(r'\dfrac{17}{24}')],
 50: [K(r'10\sqrt{2}'), K(r'4\sqrt{2}'), K(r'5\sqrt{2}'), K(r'20\sqrt{2}')],
 58: [K('1 : 4'), K('4 : 1'), K('3 : 2'), K('2 : 3')],
 59: ['1.5', K(r'\dfrac{31}{19}'), K(r'\dfrac{36}{19}'), '2'],
}
KEY_FIX = {}
EN_EDIT = {
 # Lonar is an impact crater (meteorite) in Deccan basalt, not a volcanic crater; key C Lonar kept
 23: [('Which Indian lake is of volcanic origin?', 'Which Indian lake was formed by a meteorite impact in the volcanic basalt rock of the Deccan Plateau?')],
 40: [("The titled 'Status Report", "The report titled 'Status Report")],
 67: [('[BR]fire, you must', '[BR]_____ fire, you must')],
 72: [('statement consistent to the facts presented earlier in', 'statement <u>consistent to the facts presented earlier</u> in')],
 73: [('lay. A. He had', 'lay.[BR]A. He had'), ('theatricals. C. And', 'theatricals.[BR]C. And'), ('deficiency. S2. Science', 'deficiency.[BR]S2. Science')],
 75: [('were fully tired after the long hike up the steep hill with', 'were <u>fully tired after the long hike up the steep hill</u> with')],
 80: [('disaster preparedness is :', 'disaster preparedness is:')],
}
HI_EDIT = {
 23: [('कौन सी भारतीय झील ज्वालामुखी मूल की है?', 'कौन-सी भारतीय झील दक्कन पठार की ज्वालामुखीय बेसाल्ट चट्टान में उल्कापिंड के टकराने से बनी है?')],
}
# Q3 option C "lJ" (lower-case L) is a misprint of "IJ"; Q32 option B "||" is a misprint of "II" (both languages)
OPT_FIX = {3: {'lJ': 'IJ'}, 32: {'||': 'II'}}
OPT_FIX_EN = {27: {'Policy thinks tank and cooperative federalism': 'Policy think tank and cooperative federalism'}}
OPT_FIX_HI = {}
HI_STEM_FIX = {39: [('नेटवर्क रेडिनेंस इंडेक्स', 'नेटवर्क रेडीनेस इंडेक्स'), ('नेटवर्क रेडिनेंस का', 'नेटवर्क रेडीनेस का')]}
HPD_STEM = {
 65: [("'अधिकारी '", "'अधिकारी'")],
 66: [("'आय '", "'आय'")],
 67: [("'आधार '", "'आधार'")],
 # रजिस्टर is still the most common way in many offices, so "most common" was arguable
 69: [('सुरक्षा कर्मियों की उपस्थिति दर्ज करने का सबसे प्रचलित माध्यम क्या है?', 'अंगूठे के निशान या चेहरे की पहचान से सुरक्षा कर्मियों की उपस्थिति अपने-आप दर्ज करने वाला साधन क्या है?')],
 # the options are purposes, not times
 71: [('"सुरक्षा सत्यापन" कब किया जाता है?', '"सुरक्षा सत्यापन" क्यों किया जाता है?')],
 72: [('नीचे दिए गए शब्द की <u>सही</u> पारिभाषिक शब्दावली क्या होगी:', 'नीचे दिए गए हिंदी शब्द के लिए सही अंग्रेज़ी पारिभाषिक शब्द क्या होगा?')],
}
# Q62 B "कन्नड" (without nukta) is also widely written -> a plain misspelling; Q73 C "जप्ती" -> standard "ज़ब्ती";
# Q74 A "घेराव" (usually a protesters' gherao) -> "घेराबंदी" (police cordon)
HPD_OPT = {62: {1: 'कनड़'}, 73: {2: 'ज़ब्ती'}, 74: {0: 'घेराबंदी'}}
HPD_PASSAGE = None
HPD_INSTR = '<u>उपरोक्त गद्यांश के आधार पर प्रश्न का उत्तर दें:</u>[BR]'

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
PASSAGE_EN = re.sub(r'^(<u>)?Read the following passage carefully and answer the questions based on the passage:\s*(</u>)?(\[BR\])?\s*', '', clean(EN[75]['comp']))
assert PASSAGE_EN.startswith("In the larger context of sustainable development")
assert all(HI[i]['comp'] == HI[95]['comp'] for i in range(95, 100)) and all(not HI[i]['comp'] for i in range(80, 95))
HPD_PASSAGE = clean(HI[95]['comp'])
assert HPD_PASSAGE.startswith("तकनीकी प्रगति ने 'डीपफेक'")

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
        if 76 <= n <= 80: t = edit(t, (HPD_INSTR, ''), n, 'HPD_INSTR')
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
