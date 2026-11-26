import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-07-may-shift-2'
PAPER = 'SSC GD Constable 2026 May 07 Shift 2'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {9, 10}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 11:[('AE80 : DZ40 :: TK60 : JS20 :: LP70 : ?', ana('AE80 : DZ40 :: TK60 : JS20 :: LP70 : ?'))],
 12:[('DC11 : ? :: IK13 : OS168 :: JH15 : PP224', ana('DC11 : ? :: IK13 : OS168 :: JH15 : PP224'))],
 13:[('3641 : 3691 :: 1717 : 1767 :: ? : 5946', K('3641 : 3691 :: 1717 : 1767 :: ? : 5946'))],
 14:[('798 : 1272 :: 578 : 1052 :: ? : 889', K('798 : 1272 :: 578 : 1052 :: ? : 889'))],
 56:[('45/20', K(r'\dfrac{45}{20}'))],
 57:[('1/4', K(r'\dfrac{1}{4}')), ('1/2', K(r'\dfrac{1}{2}'))],
}
REP_EN = {37: [('I. Jains II. Christian', 'I. Jains[BR]II. Christian')]}
REP_HI = {37: [('I. जैन II. ईसाई', 'I. जैन[BR]II. ईसाई')]}
FIXED_STEM = {
 44: K(r'(12.35 - 7.65)^{2} + 4 \times 12.35 \times 7.65 = ?'),
 45: K(r'(\sqrt{3} + \sqrt{2})^{2} + (\sqrt{3} - \sqrt{2})^{2} = ?'),
 46: K(r'\dfrac{(6.203)^{2} - (5.797)^{2}}{0.812} = ?'),
 48: K(r'(412 - 388)^{2} + 4 \times 412 \times 388 = ?'),
}
FIXED_OPTS = {
 51: ['2A', 'A', '4A', K(r'\dfrac{A}{3}')],
}
KEY_FIX = {}
# Q32: the Central Legislative Assembly was created only by the GoI Act 1919, so the old stem fitted option D;
# reworded to the 1909 Act's real "first": election of Indian members + separate electorates (key C kept)
EN_EDIT = {
 32: [('Which act gave representation to Indians in the Central Legislative Assembly for the first time?',
       'Which act, for the first time, provided for the election of Indian members to the Imperial (Central) Legislative Council and introduced separate electorates for Muslims?')],
}
HI_EDIT = {
 32: [('किस अधिनियम ने पहली बार केंद्रीय विधान सभा में भारतीयों को प्रतिनिधित्व दिया?',
       'किस अधिनियम ने पहली बार इंपीरियल (केंद्रीय) विधान परिषद में भारतीय सदस्यों के निर्वाचन का प्रावधान किया और मुसलमानों के लिए पृथक निर्वाचक मंडल की व्यवस्था की?')],
 58: [('P से 8 गुना अधिक कार्यकुशल', 'P से 8 गुना कार्यकुशल'), ('Q से 5 गुना अधिक कार्यकुशल', 'Q से 5 गुना कार्यकुशल')],
}
# Q3 A was an image of the letters "HI" (typed, EN + HI); Q64 "Carefu" -> "Careful"; Q71 "ïn" -> "in"
OPT_FIX = {}
OPT_FIX_EN = {3: {'#A': 'HI'}, 64: {'Carefu': 'Careful'}, 71: {'ïn': 'in'}}
OPT_FIX_HI = {3: {'#A': 'HI'}}
HPD_STEM = {
 61: [('कौन-सा चिन्ह कोष्ठक चिन्ह को', 'कौन-सा चिह्न कोष्ठक चिह्न को')],
 62: [('हिंदी की शिक्षा अनिवार्य कर दिया गया, वाक्य में कौन-सी अशुद्धि है?', 'नीचे दिए गए वाक्य में कौन-सी अशुद्धि है?[BR]हिंदी की शिक्षा अनिवार्य कर दिया गया।')],
 63: [('हमारे सामानों का ख्याल रखियेगा, वाक्य में कौन-सी अशुद्धि है?', 'नीचे दिए गए वाक्य में कौन-सी अशुद्धि है?[BR]हमारे सामानों का ख्याल रखियेगा।')],
 # "एक दिन की छुट्टी" also fitted विश्राम; casual leave is short leave for an unforeseen personal need
 65: [('जब सुरक्षा कर्मी को काम से एक दिन की छुट्टी दी जाती है, तो वह क्या कहलाता है?',
       'जब किसी सुरक्षा कर्मी को अचानक आए किसी निजी काम के लिए एक-दो दिन की छुट्टी दी जाती है, तो वह छुट्टी क्या कहलाती है?')],
 # option A "रिपोर्ट" fitted "आधिकारिक रिपोर्ट" literally; ask for the first information of a cognizable offence
 69: [('पुलिस थाने में दर्ज की गई अपराध की आधिकारिक रिपोर्ट को क्या कहते हैं?',
       'किसी संज्ञेय अपराध की सूचना मिलने पर पुलिस थाने में सबसे पहले दर्ज की जाने वाली आधिकारिक सूचना को क्या कहते हैं?')],
 72: [('नीचे दिए गए शब्द की <u>सही</u> पारिभाषिक शब्दावली क्या होगा:', 'नीचे दिए गए शब्द की सही पारिभाषिक शब्दावली क्या होगी?')],
}
HPD_OPT = {}

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

# one reading-comprehension passage for Q76-80 (all five copies identical); drop the generic instruction line
INSTR = 'Read the following passage carefully and answer the questions based on the passage:[BR]'
_p = clean(EN[75]['comp'])
assert _p.startswith(INSTR)
PASSAGE_EN = _p[len(INSTR):]
assert all(clean(EN[i]['comp']) == clean(EN[75]['comp']) for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
# the source has NO passage for HI Part D Q76-Q80 (comp empty in en/hi/gu) - our own, written so each official key is the only right answer
assert all(not HI[i]['comp'] for i in range(80, 100))
HPD_PASSAGE = ('आज की सुरक्षा व्यवस्था में डेटा की भूमिका लगातार बढ़ रही है। सुरक्षा एजेंसियाँ अलग-अलग स्रोतों से मिलने वाली सूचनाओं, जैसे कॉल रिकॉर्ड, यात्रा विवरण, '
  'वित्तीय लेन-देन और सीसीटीवी फुटेज, को एकत्र करती हैं। किंतु इन सूचनाओं को केवल फाइलों में सँभालकर रखना पर्याप्त नहीं होता। जब विभिन्न सूचनाओं का आपस में '
  'तुलनात्मक अध्ययन किया जाता है, तभी उनका विश्लेषण संभव होता है और उनमें छिपे संबंधों की पहचान हो पाती है। इसी डेटा विश्लेषण से संदिग्ध गतिविधियों के पैटर्न '
  'पहचाने जाते हैं, जिससे यह अनुमान लगाया जा सकता है कि कहाँ और कब कोई खतरा उत्पन्न हो सकता है। पहले सुरक्षा एजेंसियाँ प्रायः घटना हो जाने के बाद ही प्रतिक्रिया '
  'करती थीं, किंतु अब वे केवल प्रतिक्रिया तक सीमित नहीं रहतीं, क्योंकि डेटा के सहारे उनमें रणनीति पहले से बनाने की क्षमता विकसित हो गई है। इस प्रकार डेटा अब '
  'केवल संग्रह की वस्तु नहीं, बल्कि एक रणनीतिक संसाधन बन गया है। स्पष्ट है कि आधुनिक सुरक्षा व्यवस्था खतरे के घटित होने की प्रतीक्षा करने के बजाय पहले से '
  'योजना बनाने पर आधारित सोच को अपना रही है।')

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
    for need in [r'\( \text{AE80} : \text{DZ40} :: \text{TK60}', r'\( \text{DC11} : ? ::', r'\( 3641 : 3691 :: 1717 : 1767 :: ? : 5946 \)', r'\( 798 : 1272 :: 578 : 1052 :: ? : 889 \)',
                 'A: HI\n', r'\( (12.35 - 7.65)^{2} + 4 \times', r'(\sqrt{3} + \sqrt{2})^{2} +', r'\( \dfrac{(6.203)^{2}', r'\( (412 - 388)^{2}', r'D: \( \dfrac{A}{3} \)',
                 r'is \( \dfrac{45}{20} \) of', r'empty \( \dfrac{1}{4} \) part', r'empty \( \dfrac{1}{2} \) part', 'A: Careful\n', 'B: in\n',
                 'election of Indian members to the Imperial (Central) Legislative Council', 'areas?||I. Jains[BR]II. Christian',
                 'TEXT: [FIGURE-BASED] Two figures', 'PASSAGE (Q76–Q80): In recent times, India has grown fast']:
        assert need in en, need
    for bad in ['\\frac{', '​', 'Carefu\n', 'ïn', 'A: \n', 'Read the following passage', 'Central Legislative Assembly', '^2 ']:
        assert bad not in en, bad
    assert en.count('[FIGURE-BASED]') == 2 and en.count('(figure 1)') == 2 and en.count('PASSAGE (Q76–Q80)') == 5
    assert hp.count('PASSAGE (Q76–Q80): आज की सुरक्षा व्यवस्था में डेटा') == 5 and '​' not in hp and '<u>' not in hp and 'चिन्ह' not in hp
    for need in ['अशुद्धि है?||हिंदी की शिक्षा अनिवार्य कर दिया गया।', 'अशुद्धि है?||हमारे सामानों का ख्याल रखियेगा।', 'अचानक आए किसी निजी काम',
                 'सबसे पहले दर्ज की जाने वाली आधिकारिक सूचना', 'क्या होगी?||सूचना पट्ट']:
        assert need in hp, need
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['3']['opts'][0] == 'HI' and 'पृथक निर्वाचक मंडल' in h['32']['TEXT'] and 'अधिक' not in h['58']['TEXT']
    assert h['44']['TEXT'].startswith('निम्नलिखित') and h['9']['opts'] == ['(figure 1)', '(figure 2)', '(figure 3)', '(figure 4)']
    assert r'\( \text{AE80}' in h['11']['TEXT'] and h['51']['opts'][3] == r'\( \dfrac{A}{3} \)' and r'\dfrac{45}{20}' in h['56']['TEXT']
    assert 'I. जैन[BR]II. ईसाई' in h['37']['TEXT'] and '\\frac' not in json.dumps(h)
    print('ok')
