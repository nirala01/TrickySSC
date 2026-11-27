import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-18-may-shift-2'
PAPER = 'SSC GD Constable 2026 May 18 Shift 2'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {11, 12, 18, 19, 39}          # [FIGURE-BASED] stems
FIGOPT = {11, 12, 18, 19}           # options are figures too (Q39: photo stem, text options)
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 3:[('JH : OS :: ? : RZ :: RC : WX', ana('JH : OS :: ? : RZ :: RC : WX'))],
 5:[('BV : UE :: CJ : ? :: XA : QZ', ana('BV : UE :: CJ : ? :: XA : QZ'))],
 13:[('CP10 : ER38 :: ? : KO56 :: VS40 : XU68', ana('CP10 : ER38 :: ? : KO56 :: VS40 : XU68'))],
 14:[('AK120 : FD250 :: LL210 : QE340 :: KM250 : ?', ana('AK120 : FD250 :: LL210 : QE340 :: KM250 : ?'))],
 15:[('540 : 272 :: 210 : 107 :: 134 : ?', K('540 : 272 :: 210 : 107 :: 134 : ?'))],
 20:[('11 : 5', K('11 : 5'))],
 53:[('2 : 5', K('2 : 5'))],
}
REP_EN = {49:[('90 metres x 50 metres', '90 metres × 50 metres')]}
REP_HI = {}
FIXED_STEM = {
 42: K(r'\sqrt{0.81 \times 0.04} = ?'),
 43: K(r'\sqrt[3]{3.375} \times \sqrt{0.81} = ?'),
 44: K(r'\dfrac{(\sqrt{3} + \sqrt{2})^{2}}{\sqrt{3} - \sqrt{2}} = ?'),
 # exact value √25.6 = 5.0596…; stem now asks for the approximate value and option A reads 5.06 (key A kept)
 46: K(r'\sqrt{\dfrac{0.064 \times 0.256}{0.004 \times 0.16}} \approx ?'),
 47: K(r'3 + 6 + 9 + 12 + \ldots + 300 = ?'),
}
FIXED_STEM_L = {}
def R(a, b): return K(f'{a} : {b}')
FIXED_OPTS = {
 44: [K(r'9\sqrt{3} - 11\sqrt{2}'), K(r'9\sqrt{3} + 14\sqrt{2}'), K(r'9\sqrt{3} + 11\sqrt{2}'), K(r'9\sqrt{3} - 14\sqrt{2}')],
 46: ['5.06', '5.89', '5.15', '6.25'],
 50: [K(r'\dfrac{N}{3}'), K(r'\dfrac{N}{2}'), K(r'\dfrac{N}{5}'), K(r'\dfrac{N}{6}')],
 55: [R(1, 4), R(4, 1), R(3, 7), R(5, 3)],
 56: [K(r'\dfrac{1}{5}'), K(r'\dfrac{1}{4}'), K(r'\dfrac{1}{6}'), K(r'\dfrac{1}{3}')],
 58: [R(3, 1), R(9, 2), R(11, 3), R(6, 5)],
 59: [R(2, 1), R(3, 1), R(3, 2), R(4, 3)],
}
KEY_FIX = {}
EN_EDIT = {
 # the GD 2026 national record moved on (Kuldeep Kumar 5.41 m, 2 May 2026) before this shift, so "holds" was no longer true
 36: [('Dev Meena holds the national record in pole vault with 5.40 metres set in _____.', "Dev Meena set a men's pole vault national record of 5.40 metres in _____.")],
 63: [('urges governence for data centres to report energy, water use, and carbon emissions, ensuring accountable AI deployments.',
       'urges <u>governence</u> for data centres to report energy, water use, and carbon <u>emissions</u>, ensuring <u>accountable</u> AI <u>deployments</u>.')],
 66: [('The villagers prayed for rain during the long summer', 'The villagers prayed for rain during the long summer _______.')],
 75: [('in a view to providing their children with', '<u>in a view to providing their children with</u>')],
 78: [('What does the word "masquerade" means?', 'What does the word "masquerade" mean as it is used in the passage?')],
}
HI_EDIT = {}
# Q2 options C/D and Q3 option A are images of letters in the source (both languages)
OPT_FIX = {2: {'#C': 'M', '#D': 'P'}, 3: {'#A': 'MZ'}}
# Q38 key B said "concentric circles outside" (that is a straight wire) - outside a solenoid the lines are like a bar magnet's;
# Q63 option showed the correct "governance" while the sentence has the misspelling; Q64 had NO misspelt word (HI/GU keep "Inevitible");
# Q72 "ãl"/"01" -> "at"/"on"
OPT_FIX_EN = {38: {'Parallel straight lines inside the solenoid and concentric circles outside.': "Parallel straight lines inside the solenoid and like those of a bar magnet outside."},
              63: {'governance': 'governence'}, 64: {'Inevitable': 'Inevitible'}, 72: {'ãl': 'at', '01': 'on'},
              # Q75 B/C ('for the purpose of providing', 'in order to provide') were also correct replacements -> two clearly wrong forms (key A kept)
              75: {'for the purpose of providing their children with': 'in view to providing their children with', 'in order to provide their children with': 'with a view to provide their children with'}}
OPT_FIX_HI = {38: {'परिनालिका के अंदर समानांतर सीधी रेखाएँ और बाहर संकेंद्रित वृत्त।': 'परिनालिका के अंदर समानांतर सीधी रेखाएँ और बाहर छड़ चुंबक जैसी रेखाएँ।'}}
# EN says "Intra state" - the Hindi had अंतर्राज्यीय (inter-state)
HI_STEM_FIX = {30: [('कोसी मेची अंतर्राज्यीय', 'कोसी मेची अंतःराज्यीय')]}
HPD_STEM = {
 61: [('नीचे दिए गये वाक्य में किस प्रकार की अशुद्धि है-', 'नीचे दिए गए वाक्य में किस प्रकार की अशुद्धि है?')],
 # "मैंने नहीं जाना" is also a correct past tense of जानना - the sentence now has only the कारक error (मैंने -> मुझे)
 62: [('नीचे दिए गये वाक्य में किस प्रकार की अशुद्धि है:', 'नीचे दिए गए वाक्य में किस प्रकार की अशुद्धि है?'), ('मैंने नहीं जाना।', 'मैंने घर नहीं जाना है।')],
 63: [('निम्नलिखित में वाक्य के शुद्ध रूप का चयन करें:', 'निम्नलिखित में से वाक्य के शुद्ध रूप का चयन कीजिए।')],
 # रिपोर्टिंग टाइम also fitted "काम का समय" loosely; the stem now asks for the fixed working period
 65: [('सुरक्षा कर्मी के काम का समय क्या कहलाता है?', 'सुरक्षा कर्मी के काम करने की निर्धारित अवधि क्या कहलाती है?')],
 # नोटबुक also fitted "जो बातें लिखी जाती हैं"
 66: [('ड्यूटी पर रहते हुए जो बातें लिखी जाती हैं, वे कहाँ दर्ज होती हैं?', 'ड्यूटी के दौरान हुई घटनाओं और किए गए कार्यों का आधिकारिक लिखित रिकॉर्ड किसमें दर्ज किया जाता है?')],
 # "विवरण मांगा जाता है" described जवाबदेही better than the key प्रतिवेदन
 67: [('जब सुरक्षा कर्मी से उसकी ड्यूटी का विवरण मांगा जाता है, तो यह क्या कहलाता है?', 'जब सुरक्षा कर्मी अपनी ड्यूटी का लिखित विवरण अपने अधिकारी को प्रस्तुत करता है, तो वह क्या कहलाता है?')],
 77: [('नागरिकों का विश्वास किसे मजबूत करता है?', 'गद्यांश के अनुसार, नागरिकों के विश्वास से क्या बेहतर होता है?')],
 79: [('यह मॉडल किस प्रकार की सुरक्षा को दर्शाता है?', 'गद्यांश में वर्णित सुरक्षा का मॉडल किस प्रकार की सुरक्षा को दर्शाता है?')],
}
# Q61 option A लिंग (का/की agrees with gender, so arguable) -> काल; Q63 option A "अँधेरा घिरा था" (अँधेरा घिरना is idiomatic) -> "घनी अँधेरा छाया था";
# Q72 B/C न्याय में बाधा / साक्ष्य हस्तक्षेप (both also describe threatening a witness) -> मानहानि / संपत्ति अपराध
HPD_OPT = {61: {0: 'काल'}, 63: {0: 'वहाँ घनी अँधेरा छाया था'}, 72: {1: 'मानहानि', 2: 'संपत्ति अपराध'}}
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

# one RC passage for Q76-80 (Q76's copy has "governments and and employment websites"; Q77-80 copies are clean), no instruction line
assert all(EN[i]['comp'] == EN[76]['comp'] for i in range(76, 80)) and all(not EN[i]['comp'] for i in range(75))
PASSAGE_EN = clean(EN[76]['comp'])
assert PASSAGE_EN.startswith("The rise of job applications") and 'and and' not in PASSAGE_EN
assert all(HI[i]['comp'] == HI[95]['comp'] for i in range(95, 100)) and all(not HI[i]['comp'] for i in range(80, 95))
HPD_PASSAGE = clean(HI[95]['comp'])
assert HPD_PASSAGE.startswith('सीमावर्ती क्षेत्रों में')

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
