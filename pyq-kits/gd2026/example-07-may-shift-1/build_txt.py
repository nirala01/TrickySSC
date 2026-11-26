import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-07-may-shift-1'
PAPER = 'SSC GD Constable 2026 May 07 Shift 1'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {11, 12, 18, 19}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 2:[('RMZ : PKX :: CPI : ? :: HQT : FOR', ana('RMZ : PKX :: CPI : ? :: HQT : FOR'))],
 3:[('AI : YB :: WL : ? :: SP : QI', ana('AI : YB :: WL : ? :: SP : QI'))],
 13:[('WF851 : UH823 :: QW270 : OY242 :: XS115 : ?', ana('WF851 : UH823 :: QW270 : OY242 :: XS115 : ?'))],
 14:[('ACD13 : ? :: KPS15 : JOR196 :: ZYO17 : YXN256', ana('ACD13 : ? :: KPS15 : JOR196 :: ZYO17 : YXN256'))],
 15:[('16 : 5832 :: 22 : 13824 :: 27 : ?', K('16 : 5832 :: 22 : 13824 :: 27 : ?'))],
 20:[('5 : 6', K('5 : 6')), ('6 : 7', K('6 : 7'))],
 56:[('2/3', K(r'\dfrac{2}{3}')), ('1/4', K(r'\dfrac{1}{4}'))],
}
REP_EN = {40: [('I. Forehand II. Backhand', 'I. Forehand[BR]II. Backhand')]}
REP_HI = {40: [('I. फ़ोरहैंड II. बैकहैंड', 'I. फ़ोरहैंड[BR]II. बैकहैंड')]}
FIXED_STEM = {
 43: K(r'3\dfrac{1}{2} + 33\dfrac{1}{2} + 333\dfrac{1}{2} + 3333\dfrac{1}{2} = ?'),
 44: K(r'\dfrac{(7.5 + 2.5)^{2} - (7.5 - 2.5)^{2}}{7.5 \times 2.5} = ?'),
 45: K(r'(\sqrt{5} + \sqrt{3})^{2} + (\sqrt{5} - \sqrt{3})^{2} = ?'),
 47: K(r'(5 + \sqrt{3})^{2} - (5 - \sqrt{3})^{2} - 4\sqrt{3} = ?'),
 48: K(r'(290 + 210)^{2} - (290 - 210)^{2} = ?'),
}
FIXED_OPTS = {
 20: [K('72 : 53'), K('73 : 86'), K('24 : 33'), K('63 : 59')],
 43: ['3702', '3704', K(r'3703\dfrac{1}{2}'), '3703'],
 48: ['530 × 430', '480 × 530', '580 × 420', '590 × 470'],
 60: [K('25 : 14'), K('14 : 25'), K('27 : 11'), K('30 : 19')],
}
KEY_FIX = {}
# Q35: the scheme was APPROVED by the Union Cabinet on 16 Jul 2025 (PM launched it on 11 Oct 2025);
# Q37: Paryatan Mitra & Paryatan Didi was launched on World Tourism Day, 27 Sep 2024 (Dec 2024 was a Lok Sabha reply);
# Q71: the blank was missing
EN_EDIT = {
 35: [('Launched in July 2025, PM Dhan-Dhaanya', 'Approved by the Union Cabinet in July 2025, PM Dhan-Dhaanya')],
 37: [('Ministry of Tourism in December 2024?', 'Ministry of Tourism in September 2024?')],
 71: [('girls are experimenting new types', 'girls are experimenting _______ new types')],
}
HI_EDIT = {
 17: [('एक घड़ी दोपहर 1 AM पर', 'एक घड़ी 1 AM पर')],
 35: [('जुलाई 2025 में शुरू की गई, पीएम धन-धान्य', 'जुलाई 2025 में केंद्रीय मंत्रिमंडल द्वारा स्वीकृत पीएम धन-धान्य')],
 37: [('दिसंबर 2024 में पर्यटन मंत्रालय', 'सितंबर 2024 में पर्यटन मंत्रालय')],
}
# Q66 C was an image of the word "see" (typed); Q31 D "D. Gukesh" was the same person as A "Gukesh" -> another real (wrong) GM
OPT_FIX = {}
# Q68 A "Uρ" (Greek rho) -> "Up"; Q71 A "oy" -> "of" ("on" would be arguable)
OPT_FIX_EN = {66: {'#C': 'see'}, 31: {'D. Gukesh': 'R. Praggnanandhaa'}, 68: {'Uρ': 'Up'}, 71: {'oy': 'of'}}
OPT_FIX_HI = {31: {'डी. गुकेश (D. Gukesh)': 'आर. प्रज्ञानानंद (R. Praggnanandhaa)'}}
HPD_STEM = {
 61: [('नीचे दिए गये वाक्य में किस प्रकार की <u>अशुद्धि</u> है:', 'नीचे दिए गए वाक्य में किस प्रकार की अशुद्धि है?')],
 62: [('नीचे दिए गये वाक्य में किस प्रकार की <u>अशुद्धि</u> है:', 'नीचे दिए गए वाक्य में किस प्रकार की अशुद्धि है?')],
 63: [('निम्नलिखित में वाक्य के <u>अशुद्ध</u> रूप का चयन कीजिए:', 'निम्नलिखित में से वाक्य के अशुद्ध रूप का चयन कीजिए।')],
 # the bare stem "तो वह क्या होता है?" did not say what is being asked
 65: [('तो वह क्या होता है?', 'तो वह अपने अधिकारी को लिखित रूप में क्या देता है?')],
 # a posting letter (तैनाती पत्र) also fixes duty; ask for the daily time and shift
 68: [('सुरक्षा कर्मी का समय निर्धारण किस दस्तावेज़ में होता है?', 'सुरक्षा कर्मियों की रोज़ की ड्यूटी का समय और पाली किस दस्तावेज़ में दर्ज की जाती है?')],
}
# HI Part D option fixes (index 0-3): Q71 D stray "में"; Q72 B "प्रमाणिकता परीक्षण" (also checks validity) -> "साक्ष्य संकलन"
HPD_OPT = {71: {3: 'प्रचार कार्यक्रम'}, 72: {1: 'साक्ष्य संकलन'}}

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

# one reading-comprehension passage for Q76-80 (all five copies identical, no instruction line)
PASSAGE_EN = clean(EN[75]['comp'])
assert all(clean(EN[i]['comp']) == PASSAGE_EN for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
HPD_PASSAGE = clean(HI[95]['comp'])
assert all(clean(HI[i]['comp']) == HPD_PASSAGE for i in range(95, 100)) and all(not HI[i]['comp'] for i in range(80, 95))

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
    en = open(f'{HERE}/out/{PREFIX}-questions-EN.txt', encoding='utf-8').read()
    hp = open(f'{HERE}/out/{PREFIX}-questions-HI-partD.txt', encoding='utf-8').read()
    for need in [r'\( \text{RMZ} : \text{PKX} :: \text{CPI} : ? ::', r'\( \text{AI} : \text{YB}', r'\( \text{WF851} : \text{UH823}', r'\( \text{ACD13} : ? ::',
                 r'\( 16 : 5832 :: 22 : 13824 :: 27 : ? \)', r"ratio of L and M's age was \( 5 : 6 \)", r'B: \( 73 : 86 \)', r'A: \( 25 : 14 \)',
                 r'3\dfrac{1}{2} + 33\dfrac{1}{2}', r'C: \( 3703\dfrac{1}{2} \)', r'\( \dfrac{(7.5 + 2.5)^{2}', r'(\sqrt{5} + \sqrt{3})^{2} +', r'- 4\sqrt{3} = ? \)',
                 r'\( (290 + 210)^{2}', 'B: 480 × 530\n', r'R did \( \dfrac{2}{3} \) part', r'did \( \dfrac{1}{4} \) part', 'Approved by the Union Cabinet in July 2025',
                 'Ministry of Tourism in September 2024?', 'D: R. Praggnanandhaa\n', 'C: see\n', 'A: Up\n', 'experimenting _______ new types', 'A: of\n',
                 'TEXT: [FIGURE-BASED] Two figures', 'TEXT: [FIGURE-BASED] In the following figure series', 'PASSAGE (Q76–Q80): Novels are', 'tennis?||I. Forehand[BR]II. Backhand']:
        assert need in en, need
    for bad in ['\\frac{', '​', 'December 2024', 'Launched in July', 'A: \n', 'C: \n', 'D. Gukesh', 'Uρ', 'A: oy', 'x 530', 'Read the following passage']:
        assert bad not in en, bad
    assert en.count('[FIGURE-BASED]') == 4 and en.count('(figure 1)') == 4 and en.count('PASSAGE (Q76–Q80)') == 5
    assert hp.count('PASSAGE (Q76–Q80): सुरक्षा व्यवस्था में तकनीक') == 5 and '​' not in hp and '<u>' not in hp and 'गये' not in hp
    for need in ['अशुद्धि है?||आँख में कौन पड़ गया।', 'अशुद्धि है?||उसे भारी प्यास लगी है।', 'अशुद्ध रूप का चयन कीजिए।', 'लिखित रूप में क्या देता है?',
                 'ड्यूटी का समय और पाली', 'D: प्रचार कार्यक्रम\n', 'B: साक्ष्य संकलन\n']:
        assert need in hp, need
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['31']['opts'][3].startswith('आर. प्रज्ञानानंद') and 'केंद्रीय मंत्रिमंडल द्वारा स्वीकृत' in h['35']['TEXT'] and 'सितंबर 2024' in h['37']['TEXT']
    assert 'दोपहर' not in h['17']['TEXT']
    assert h['43']['TEXT'].startswith('निम्नलिखित') and h['11']['opts'] == ['(figure 1)', '(figure 2)', '(figure 3)', '(figure 4)']
    assert r'\( \text{RMZ}' in h['2']['TEXT'] and r'\( 5 : 6 \)' in h['20']['TEXT'] and h['60']['opts'][0] == r'\( 25 : 14 \)' and r'\dfrac{2}{3}' in h['56']['TEXT']
    assert h['48']['opts'][1] == '480 × 530' and '\\frac' not in json.dumps(h)
    print('ok')
