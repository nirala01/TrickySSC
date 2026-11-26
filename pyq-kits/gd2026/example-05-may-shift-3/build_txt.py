import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-05-may-shift-3'
PAPER = 'SSC GD Constable 2026 May 05 Shift 3'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {11, 12, 18, 19}
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
REP = {
 3: [('RF : TI :: XA : ZD :: QC : ?', ana('RF : TI :: XA : ZD :: QC : ?'))],
 4: [('? , UF, RC', '?, UF, RC')],
 5: [('CH : AS :: TK : RP :: ? : LH', ana('CH : AS :: TK : RP :: ? : LH'))],
 13:[('ZA300 : YZ154 :: TQ700 : ? :: WY500 : VX354', ana('ZA300 : YZ154 :: TQ700 : ? :: WY500 : VX354'))],
 14:[('KPL22 : JOK441 :: ? : TKQ625 :: IRO28 : HQN729', ana('KPL22 : JOK441 :: ? : TKQ625 :: IRO28 : HQN729'))],
 15:[('?: 991 :: 282 : 138 :: 1166 : 580', K('? : 991 :: 282 : 138 :: 1166 : 580'))],
 20:[('5 : 7', K('5 : 7'))],
 45:[(r'x =\sqrt{196} ÷ \sqrt{49} + \sqrt{81}', K(r'x = \sqrt{196} \div \sqrt{49} + \sqrt{81}'))],
 54:[('3 : 5', K('3 : 5'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 43: K(r'\dfrac{1}{3} + \dfrac{1}{15} + \dfrac{1}{35} + \dfrac{1}{63} = ?'),
 44: K(r'(2.85 - 1.15)^{2} + 4 \times 2.85 \times 1.15 = ?'),
 48: K(r'\sqrt{\dfrac{(4.1)^{2} + (41.1)^{2} + (411.1)^{2}}{(0.41)^{2} + (4.11)^{2} + (41.11)^{2}}} = ?'),
 50: K(r'2[(530)^{2} + (270)^{2}] - (530 - 270)^{2} = ?'),
}
# Q2 options A and C were images of the letters J and H; option B "∈" is a misprint of the letter E
FIXED_OPTS = {
 2: ['J', 'E', 'H', 'G'],
 20: [K('10 : 21'), K('13 : 21'), K('12 : 23'), K('11 : 23')],
 43: [K(r'\dfrac{5}{7}'), K(r'\dfrac{4}{9}'), K(r'\dfrac{5}{11}'), K(r'\dfrac{8}{13}')],
 54: [K('2 : 3'), K('3 : 2'), K('2 : 5'), K('5 : 2')],
}
KEY_FIX = {}
EN_EDIT = {
 40: [('What position will it naturally attain?', 'In which position will the plane of the loop naturally settle with respect to the field lines?')],
 63: [("The musician's work was full of profound lyrics, deep symbolism, and lilting meloudies.",
       "The <u>musician's</u> work was full of <u>profound</u> lyrics, deep <u>symbolism</u>, and lilting <u>meloudies</u>.")],
 74: [('We must take the bull by the head and', 'We must <u>take the bull by the head</u> and')],
 75: [('you might drive on for hours until', 'you might drive on for hour until')],
}
HI_EDIT = {
 40: [('यह स्वाभाविक रूप से कौन सी स्थिति प्राप्त करेगा?', 'क्षेत्र रेखाओं के सापेक्ष लूप का तल स्वाभाविक रूप से किस स्थिति में आ जाएगा?')],
 57: [('P से 5 गुना अधिक कुशल हैं', 'P से 5 गुना कुशल हैं'), ('Q से 3 गुना अधिक कुशल हैं', 'Q से 3 गुना कुशल हैं')],
}
OPT_FIX = {}
# Q63 D "melodies" -> "meloudies" (the misspelt word as it stands in the sentence); Q64 "silhouette" -> "silouette"
# (the HI/GU copies keep the misspelling the key intends; EN had all four correct); Q71 "ower" -> "over";
# Q75 C "for hours" -> "for hour" (the error Testbook's own solution describes; the cleaned-up sentence had no error);
# Q78 "harmfu" -> "harmful"
OPT_FIX_EN = {63: {'melodies': 'meloudies'}, 64: {'silhouette': 'silouette'}, 71: {'ower': 'over'},
              75: {'might drive on for hours': 'might drive on for hour'}, 78: {'harmfu': 'harmful'}}
OPT_FIX_HI = {}
HPD_STEM = {
 64: [('कौन -सा', 'कौन-सा'), ('<u>सही</u>', 'सही')],
 65: [('जब किसी सुरक्षा कर्मी को एक स्थान से दूसरे स्थान पर भेजा जाता है, तो उसे क्या कहते हैं?',
       'जब किसी सुरक्षा कर्मी को उसके वर्तमान कार्यस्थल से हटाकर दूसरे स्थान पर नियुक्त कर दिया जाता है, तो उसे क्या कहते हैं?')],
 68: [('सुरक्षा कर्मियों को प्रशिक्षण देने की प्रक्रिया क्या कहलाती है?',
       'सुरक्षा कर्मियों को उनके काम के लिए आवश्यक कौशल, अभ्यास और जानकारी देने की प्रक्रिया क्या कहलाती है?')],
 69: [('जब कोई सुरक्षा कर्मी समय पर ड्यूटी पर नहीं आता, तो वह क्या कहलाता है?',
       'जब कोई सुरक्षा कर्मी अपनी निर्धारित ड्यूटी पर आता ही नहीं, तो वह क्या कहलाता है?')],
}
# HI Part D option fixes (index 0-3): Q62 A "गोलियों की बाढ़" (बाढ़ = volley of fire, also correct) -> "गोलियों के बौछार";
# Q63 C "कई बैंक कर्मचारियों ने प्रदर्शन किया" (also a correct sentence) -> "बैंक के कई कर्मचारियों ने प्रदर्शन किए"
HPD_OPT = {62: {0: 'गोलियों के बौछार'}, 63: {2: 'बैंक के कई कर्मचारियों ने प्रदर्शन किए'}}

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

# one reading-comprehension passage for Q76-80 (all five copies identical); dash restored as quoted in Q79
PASSAGE_EN = clean(EN[75]['comp'])
assert all(clean(EN[i]['comp']) == PASSAGE_EN for i in range(75, 80))
assert PASSAGE_EN.count('osteoporosis a condition') == 1
PASSAGE_EN = PASSAGE_EN.replace('osteoporosis a condition', 'osteoporosis—a condition')

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
    P = clean(HI[95]['comp'])
    assert all(clean(HI[i]['comp']) == P for i in range(95, 100)) and all(not HI[i]['comp'] for i in range(80, 95))
    for i in range(80, 100):
        q = HI[i]; n = i - 19
        t = clean(q['text'])
        for pair in HPD_STEM.get(n, []): t = edit(t, pair, n, 'HPD')
        if '[BR]' in t: t = t.replace('[BR]', '||', 1)
        if q['comp']:
            t = 'PASSAGE (Q76–Q80): ' + P + ' || ' + t
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
    for need in ['A: J\nB: E\nC: H\nD: G\n', r'\( \text{RF} : \text{TI}', r'\( \text{CH} : \text{AS}', r'\( ? : 991 :: 282', 'TEXT: [FIGURE-BASED] Two figures',
                 r'\( x = \sqrt{196} \div \sqrt{49} + \sqrt{81} \)', r'A: \( \dfrac{5}{7} \)', r'4 \times 2.85 \times 1.15', 'plane of the loop',
                 "<u>musician's</u>", '<u>meloudies</u>', 'D: meloudies\n', 'A: silouette\n', 'A: over\n', '<u>take the bull by the head</u>',
                 'drive on for hour until', 'C: might drive on for hour\n', 'A: harmful\n', 'osteoporosis—a condition', 'PASSAGE (Q76–Q80): Iron and calcium']:
        assert need in en, need
    for bad in ['∈', 'ower\n', 'harmfu\n', '\\frac{', '​', '? , UF', ' x 2.85', 'for hours until', 'silhouette']:
        assert bad not in en, bad
    assert en.count('[FIGURE-BASED]') == 4 and en.count('(figure 1)') == 4 and en.count('PASSAGE (Q76–Q80)') == 5
    assert hp.count('PASSAGE (Q76–Q80)') == 5 and '​' not in hp and '<u>सही</u>' not in hp and 'कौन -सा' not in hp
    for need in ['A: गोलियों के बौछार\n', 'C: बैंक के कई कर्मचारियों ने प्रदर्शन किए\n', 'वर्तमान कार्यस्थल से हटाकर', 'कौशल, अभ्यास और जानकारी', 'आता ही नहीं']:
        assert need in hp, need
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['2']['opts'] == ['J', 'E', 'H', 'G'] and 'लूप का तल' in h['40']['TEXT'] and 'अधिक' not in h['57']['TEXT']
    assert h['43']['TEXT'].startswith('निम्नलिखित') and r'\( x = \sqrt{196}' in h['45']['TEXT'] and h['11']['opts'] == ['(figure 1)', '(figure 2)', '(figure 3)', '(figure 4)']
    assert '\\frac{' not in json.dumps(h) and h['54']['opts'][0] == r'\( 2 : 3 \)' and r'\( 5 : 7 \)' in h['20']['TEXT']
    print('ok')
