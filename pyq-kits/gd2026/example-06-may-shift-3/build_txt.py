import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-06-may-shift-3'
PAPER = 'SSC GD Constable 2026 May 06 Shift 3'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {9, 10}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 11:[('? : RS650 :: AR190 : YO690 :: YT240 : WQ740', ana('? : RS650 :: AR190 : YO690 :: YT240 : WQ740'))],
 12:[('TUV11 : OPB169 :: LMO15 : GHU289 :: ? : LOR121', ana('TUV11 : OPB169 :: LMO15 : GHU289 :: ? : LOR121'))],
 13:[('5945 : 5894 :: 6244 : 6193 :: 3370 : ?', K('5945 : 5894 :: 6244 : 6193 :: 3370 : ?'))],
 14:[('220 : ? :: 157 : 384 :: 516 : 743', K('220 : ? :: 157 : 384 :: 516 : 743'))],
 45:[(r'\rm x=\sqrt{484}\div \sqrt{121}+\sqrt{64}', K(r'x = \sqrt{484} \div \sqrt{121} + \sqrt{64}')), ('x^{2}', K('x^{2}'))],
 53:[('2/5', K(r'\dfrac{2}{5}'))],
 56:[('35/20', K(r'\dfrac{35}{20}'))],
 58:[('1/3', K(r'\dfrac{1}{3}'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 41: K(r'73 + 92 - 61 + (41 + 21) - 78 + 33 = ?'),
 44: K(r'(4.2)^{2} \times 4.2 - 3 \times 0.2 \times (4.2)^{2} + 3 \times 4.2 \times (0.2)^{2} - (0.2)^{3} = ?'),
 46: K(r'(5 + \sqrt{3})^{2} + (5 - \sqrt{3})^{2} - 40 = ?'),
}
FIXED_OPTS = {
 55: [K('13 : 11'), K('11 : 13'), K('3 : 2'), K('2 : 3')],
 57: [K(r'\dfrac{1}{5}'), K(r'\dfrac{1}{4}'), K(r'\dfrac{1}{6}'), K(r'\dfrac{1}{3}')],
}
KEY_FIX = {}
# Q40: the 2025 Quad Leaders' Summit was due in India but was never held, so "will be held" is reworded (key India kept)
EN_EDIT = {
 40: [("The QUAD leader's summit-2025 will be held in ____.", "Which country was chosen to host the Quad Leaders' Summit due in 2025?")],
}
HI_EDIT = {
 40: [('क्वाड (QUAD) शिखर सम्मेलन-2025 ____ में आयोजित किया जाएगा।', '2025 में होने वाले क्वाड (QUAD) नेताओं के शिखर सम्मेलन की मेजबानी के लिए किस देश को चुना गया था?')],
}
# Q16 C "TFIX T" had a stray space
OPT_FIX = {16: {'TFIX T': 'TFIXT'}}
# Q63 A "Incipient" (correct, so two options were correctly spelt) -> "Incepient" as in the HI/GU copies; Q65 D "Laure" -> "Laurel";
# Q66 A "Additiona" -> "Additional"; Q71 A was an image of the word "in" (typed)
OPT_FIX_EN = {63: {'Incipient': 'Incepient'}, 65: {'Laure': 'Laurel'}, 66: {'Additiona': 'Additional'}, 71: {'#A': 'in'}}
OPT_FIX_HI = {39: {'सब्सिडी (सब्सिडी)': 'सब्सिडी'}}
HPD_STEM = {
 61: [('किस प्रकार की <u>अशुद्धि</u> है:', 'किस प्रकार की अशुद्धि है?')],
 62: [('इस विषय पर एक भी अच्छी पुस्तकें नहीं है, वाक्य में कौन-सी <u>अशुद्धि</u> है?', 'नीचे दिए गए वाक्य में कौन-सी अशुद्धि है?[BR]इस विषय पर एक भी अच्छी पुस्तकें नहीं है।')],
 63: [('नीचे दिए गये वाक्य में किस प्रकार की <u>अशुद्धि</u> है:', 'नीचे दिए गए वाक्य में किस प्रकार की अशुद्धि है?')],
 64: [('का <u>सही</u> तकनीकी शब्द है:', 'का सही तकनीकी शब्द क्या है?')],
 # a plain-clothes (secret) duty also fits the bare stem; say the order was for uniform
 65: [('जब सुरक्षा कर्मी बिना वर्दी ड्यूटी पर आता है, तो वह क्या है?',
       'वर्दी में ड्यूटी करने का आदेश होने पर भी जब कोई सुरक्षा कर्मी बिना वर्दी के ड्यूटी पर आता है, तो यह क्या है?')],
 72: [('की <u>सही</u> पारिभाषिक शब्दावली क्या होगा:', 'की सही पारिभाषिक शब्दावली क्या होगी?')],
}
# HI Part D option fixes (index 0-3): Q70 B "वह क्षेत्र जहाँ किसी अधिकारी का नियंत्रण" (incomplete) -> "… नियंत्रण हो";
# Q71 D "परिवहन की निगरानी हेतु" (traffic surveillance is also a use) -> "वाहनों की मरम्मत हेतु"
HPD_OPT = {70: {1: 'वह क्षेत्र जहाँ किसी अधिकारी का नियंत्रण हो'}, 71: {3: 'वाहनों की मरम्मत हेतु'}}
# The source has NO passage for HI Part D Q76-Q80 (comp empty in en/hi/gu) - our own passage, written to fit the five items and keys
HPD_PASSAGE = ('आंतरिक सुरक्षा केवल पुलिस और प्रशासन का कार्य नहीं है; इसमें आम नागरिकों की भागीदारी भी उतनी ही आवश्यक है। '
 'इसी उद्देश्य से पुलिस समय-समय पर सामुदायिक जागरूकता अभियान चलाती है। इन अभियानों का उद्देश्य केवल जानकारी देना या प्रशिक्षण देना नहीं, '
 'बल्कि लोगों की सोच में परिवर्तन लाना है। जब जागरूकता सूचना के स्तर से आगे बढ़कर सोच के स्तर तक पहुँचती है, तब नागरिक सुरक्षा उपायों को '
 'सरकारी काम या कानूनी दबाव न मानकर अपनी व्यक्तिगत जिम्मेदारी के रूप में देखने लगते हैं। वे संदिग्ध गतिविधियों की सूचना पुलिस को देते हैं, '
 'यातायात नियमों का पालन करते हैं और अपने मोहल्ले की सुरक्षा में सहयोग करते हैं। इस सोच से बनी सुरक्षा व्यवस्था केवल डर या दंड पर नहीं टिकती, '
 'इसलिए वह लंबे समय तक टिकाऊ रहती है। पुलिस और जनता की ऐसी साझेदारी से समाज अधिक सुरक्षित बनता है।')

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

# one reading-comprehension passage for Q76-80 (all five copies identical); the generic instruction line is dropped;
# 'eminent' (= famous) -> 'immanent' (Husserl's term: what lies within consciousness)
INSTR = 'Read the following passage carefully and answer the questions based on the passage:[BR]'
PASSAGE_EN = clean(EN[75]['comp'])
assert all(clean(EN[i]['comp']) == PASSAGE_EN for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
assert PASSAGE_EN.startswith(INSTR)
PASSAGE_EN = PASSAGE_EN[len(INSTR):]
assert PASSAGE_EN.count("'eminent'") == 1
PASSAGE_EN = PASSAGE_EN.replace("'eminent'", "'immanent'")

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
    assert all(not HI[i]['comp'] for i in range(80, 100))
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
    for need in [r'\( ? : \text{RS650} :: \text{AR190}', r'\( \text{TUV11} : \text{OPB169}', r'\( 5945 : 5894', r'\( 220 : ? :: 157', 'C: TFIXT\n',
                 r'(4.2)^{2} \times 4.2', r'\( x = \sqrt{484} \div \sqrt{121} + \sqrt{64} \)', r'value of \( x^{2} \)?', r'(5 + \sqrt{3})^{2}',
                 r'\( \dfrac{2}{5} \) of 60', r'\( \dfrac{35}{20} \)', r'complete \( \dfrac{1}{3} \) part', r'C: \( 3 : 2 \)', r'B: \( \dfrac{1}{4} \)',
                 "chosen to host the Quad Leaders' Summit due in 2025?", 'A: Incepient\n', 'D: Laurel\n', 'A: Additional\n', 'A: in\n',
                 'TEXT: [FIGURE-BASED] Two figures', "PASSAGE (Q76–Q80): Phenomenology is", "'immanent'"]:
        assert need in en, need
    for bad in ['\\frac{', '​', '\\rm', 'will be held', 'A: \n', 'D: \n', 'Read the following passage', "'eminent'", 'TFIX T', 'Additiona\n']:
        assert bad not in en, bad
    assert en.count('[FIGURE-BASED]') == 2 and en.count('(figure 1)') == 2 and en.count('PASSAGE (Q76–Q80)') == 5
    assert hp.count('PASSAGE (Q76–Q80)') == 5 and '​' not in hp and '<u>अशुद्धि</u>' not in hp and '<u>सही</u>' not in hp and 'गये' not in hp
    for need in ['B: वह क्षेत्र जहाँ किसी अधिकारी का नियंत्रण हो\n', 'D: वाहनों की मरम्मत हेतु\n', 'अशुद्धि है?||इस विषय पर एक भी अच्छी पुस्तकें नहीं है।',
                 'अशुद्धि है?||हमने यह काम करना है।', 'अशुद्धि है?||वे विविध विषय से परिचित हैं।', 'वर्दी में ड्यूटी करने का आदेश', 'शब्दावली क्या होगी?||<u>गैर न्यायिक</u>']:
        assert need in hp, need
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['16']['opts'][2] == 'TFIXT' and h['39']['opts'][0] == 'सब्सिडी' and 'किस देश को चुना गया था' in h['40']['TEXT']
    assert h['41']['TEXT'].startswith('निम्नलिखित') and h['9']['opts'] == ['(figure 1)', '(figure 2)', '(figure 3)', '(figure 4)']
    assert r'\( x = \sqrt{484}' in h['45']['TEXT'] and r'\( x^{2} \) का मान' in h['45']['TEXT'] and h['55']['opts'][2] == r'\( 3 : 2 \)'
    assert r'\( \text{TUV11}' in h['12']['TEXT'] and r'\( \dfrac{2}{5} \)' in h['53']['TEXT'] and '\\rm' not in json.dumps(h)
    print('ok')
