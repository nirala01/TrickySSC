import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/x/s2804_3.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-28-apr-shift-3'
PAPER = 'SSC GD Constable 2026 Apr 28 Shift 3'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {11, 12}
def K(x): return r'\( ' + x + r' \)'
# exact replacements in the stem, BOTH languages (anchor must exist)
REP = {
 3: [('EN : YM :: DP : XK :: ? : DJ', K(r'\text{EN} : \text{YM} :: \text{DP} : \text{XK} :: ? : \text{DJ}'))],
 13:[('ST110 : ? :: AL220 : MB240 :: JK330 : LK350', K(r'\text{ST110} : ? :: \text{AL220} : \text{MB240} :: \text{JK330} : \text{LK350}'))],
 14:[('? : DZ445 :: DZ155 : GG355 :: BK605 : ER805', K(r'? : \text{DZ445} :: \text{DZ155} : \text{GG355} :: \text{BK605} : \text{ER805}'))],
 15:[('7084 : ? :: 5191 : 5245 :: 8259 : 8313', K('7084 : ? :: 5191 : 5245 :: 8259 : 8313'))],
 16:[('14 : 1728 :: 19 : 4913 :: 29 : ?', K('14 : 1728 :: 19 : 4913 :: 29 : ?'))],
}
# stems typed fresh (source KaTeX normalised to \dfrac)
FIXED_STEM = {
 43: K(r'7\dfrac{2}{7} + 9\dfrac{1}{3} - 5\dfrac{3}{4} = ?'),
 44: K(r'\dfrac{\sqrt{0.09}}{0.6} \times \dfrac{0.4}{\sqrt{0.36}} \times \dfrac{1.8}{\sqrt{0.36}} = ?'),
 45: K(r'\sqrt{18^{2} + 8 \times 8 - 5 \times 22 + 11} = ?'),
}
FIXED_OPTS = {
 43: [K(r'12\dfrac{31}{84}'), K(r'11\dfrac{31}{84}'), K(r'13\dfrac{7}{12}'), K(r'10\dfrac{73}{84}')],
}
# EN-specific stem edits (corrections listed in the delivery report)
EN_EDIT = {
 30: ("An engineer is assigned to monitor Earth's surface changes using radar, even through clouds and at night.",
      "An engineer is assigned to monitor Earth's surface changes using radar, even through clouds and at night. Which satellite mission's data is best suited for this task?"),
 59: ('(5/9)', K(r'\dfrac{5}{9}')),
 61: ('Politicians ought to to retain', 'Politicians ought to _______ to retain'),
 73: ('conducive of innovation and inclusivity.', '<u>conducive of innovation and inclusivity</u>.'),
 75: ("more sustainable than their's.", "<u>more sustainable than their's</u>."),
}
HI_EDIT = {
 30: ('यहाँ तक कि बादलों के माध्यम से और रात में भी।',
      'यहाँ तक कि बादलों के माध्यम से और रात में भी। इस कार्य के लिए किस उपग्रह मिशन का डेटा सबसे उपयुक्त है?'),
}
# option corrections: {n: {old: new}} (both languages unless noted)
OPT_FIX = {29: {'1932': '1950'}, 31: {'SSLP': 'SSLV'}}
OPT_FIX_EN = {61: {'talk the wal': 'talk the wall'}, 73: {'conducive to innovation or inclusivity': 'conducive to innovation and inclusivity'},
              78: {'S0': 'too'}}
OPT59_EN = [K(r'\dfrac{6}{7}') + ' of cost price', K(r'\dfrac{7}{6}') + ' of cost price', K(r'\dfrac{9}{7}') + ' of cost price', K(r'\dfrac{7}{9}') + ' of cost price']
OPT59_HI = ['क्रय मूल्य का ' + K(r'\dfrac{6}{7}'), 'क्रय मूल्य का ' + K(r'\dfrac{7}{6}'), 'क्रय मूल्य का ' + K(r'\dfrac{9}{7}'), 'क्रय मूल्य का ' + K(r'\dfrac{7}{9}')]
# Cloze passage correction ("identify their known triggers" -> unknown also fitted)
COMP_FIX = ('to identify their ___B___ triggers', 'to keep track of their ___B___ triggers')
# Hindi Part D corrections
HPD_STEM = {72: ('शब्दावली क्या होगा:', 'शब्दावली क्या होगी?'), 74: ('पुलिस द्वारा तैयार किया गया आधिकारिक लिखित विवरण क्या कहलाता है?',
                 'पुलिस द्वारा किसी घटना या कार्य के बारे में अधिकारियों को दी जाने वाली आधिकारिक लिखित रिपोर्ट क्या कहलाती है?')}
HPD_OPT = {70: {'खुफिया जानकारी इकट्ठा': 'खुफिया जानकारी इकट्ठा करना'}, 79: {'गति और समयबद्धता से': 'सटीकता और समयबद्धता दोनों से'}}

def edit(t, pair, n, tag):
    a, b = pair
    if a not in t: raise SystemExit(f'Q{n} {tag}: anchor missing {a!r}')
    return t.replace(a, b, 1)

def stem(q, n, lang):
    if n in FIXED_STEM: return FIXED_STEM[n]
    t = clean(q['text'])
    t = re.sub(r'\\\(\s*(.*?)\s*\\\)', lambda m: m.group(1), t)
    for pair in REP.get(n, []): t = edit(t, pair, n, lang)
    if lang == 'EN' and n in EN_EDIT: t = edit(t, EN_EDIT[n], n, 'EN_EDIT')
    if lang == 'HI' and n in HI_EDIT: t = edit(t, HI_EDIT[n], n, 'HI_EDIT')
    if lang == 'HI' and n == 59: t = edit(t, (r'(5/9)', K(r'\dfrac{5}{9}')), n, 'HI59')
    if '[BR]' in t and '||' not in t: t = t.replace('[BR]', '||', 1)
    if n in FIG: t = '[FIGURE-BASED] ' + t
    return t

def opts(q, n, lang):
    if n in FIG: return [f'(figure {i})' for i in range(1, 5)]
    if n in FIXED_OPTS: return FIXED_OPTS[n]
    if n == 59: return OPT59_EN if lang == 'EN' else OPT59_HI
    out = []
    for x in q['opts']:
        v = clean(x)
        v = OPT_FIX.get(n, {}).get(v, v)
        if lang == 'EN': v = OPT_FIX_EN.get(n, {}).get(v, v)
        out.append(v)
    return out

def block(n, subj, concept, text, op, ans):
    return f"[Q{n}]\nSUBJECT: {subj}\nCONCEPT: {concept}\nTEXT: {text}\nA: {op[0]}\nB: {op[1]}\nC: {op[2]}\nD: {op[3]}\nANSWER: {ans}\n"

def header(lang): return f"# TRICKYSSC QUESTIONS\nEXAM: ssc-gd\nYEAR: 2026\nPAPER: {PAPER}\nLANG: {lang}\n"

def build_en():
    out = [header('EN')]
    for i in range(80):
        q = EN[i]; n = i + 1
        t = stem(q, n, 'EN')
        if q['comp']:
            c = clean(q['comp']); c = edit(c, COMP_FIX, n, 'COMP')
            t = 'PASSAGE (Q76–Q80): ' + c + ' || ' + t
        op = opts(q, n, 'EN')
        out.append(block(n, SUBJ[q['si']], CON_EN[n], t, op, 'ABCD'[q['cidx']]))
    return '\n'.join(out)

def build_hi_partd():
    out = [header('HI')]
    for i in range(80, 100):
        q = HI[i]; n = i - 19
        t = clean(q['text'])
        if n in HPD_STEM: t = edit(t, HPD_STEM[n], n, 'HPD')
        if '[BR]' in t: t = t.replace('[BR]', '||', 1)
        if q['comp']: t = 'PASSAGE (Q76–Q80): ' + clean(q['comp']) + ' || ' + t
        op = [HPD_OPT.get(n, {}).get(clean(x), clean(x)) for x in q['opts']]
        out.append(block(n, 'Hindi Language', CON_HI[n], t, op, 'ABCD'[q['cidx']]))
    return '\n'.join(out)

def hi_q1_60():
    D = {}
    for i in range(60):
        q = HI[i]; n = i + 1
        t = stem(q, n, 'HI')
        if not re.search('[ऀ-ॿ]', t): t = 'निम्नलिखित व्यंजक का मान ज्ञात कीजिए।||' + t
        D[n] = dict(TEXT=t, opts=opts(q, n, 'HI'), ANSWER='ABCD'[q['cidx']])
    return D

if __name__ == '__main__':
    os.makedirs(f'{HERE}/out', exist_ok=True)
    open(f'{HERE}/out/{PREFIX}-questions-EN.txt', 'w', encoding='utf-8').write(build_en())
    open(f'{HERE}/out/{PREFIX}-questions-HI-partD.txt', 'w', encoding='utf-8').write(build_hi_partd())
    json.dump(hi_q1_60(), open(f'{HERE}/hi_q1_60.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    # verify every option fix landed
    en = open(f'{HERE}/out/{PREFIX}-questions-EN.txt', encoding='utf-8').read()
    hp = open(f'{HERE}/out/{PREFIX}-questions-HI-partD.txt', encoding='utf-8').read()
    for need in ['A: 1950', 'C: SSLV', 'B: talk the wall', 'A: conducive to innovation and inclusivity', 'D: too', 'keep track of their ___B___']:
        assert need in en, need
    for need in ['खुफिया जानकारी इकट्ठा करना', 'सटीकता और समयबद्धता दोनों से', 'आधिकारिक लिखित रिपोर्ट क्या कहलाती है']:
        assert need in hp, need
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['29']['opts'][0] == '1950' and h['31']['opts'][2] == 'SSLV'
    print('ok')
