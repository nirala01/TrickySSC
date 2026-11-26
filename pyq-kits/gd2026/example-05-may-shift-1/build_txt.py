import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-05-may-shift-1'
PAPER = 'SSC GD Constable 2026 May 05 Shift 1'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = set()
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    out = []
    for tok in s.split(' '):
        out.append(T(tok) if re.search('[A-Z]', tok) else tok)
    return K(' '.join(out))
REP = {
 2: [('EQ : ZK :: CJ : XD :: ? : IR', ana('EQ : ZK :: CJ : XD :: ? : IR'))],
 16:[('LQT150 : ? :: TVP250 : SYW470 :: UKL350 : ONX570', ana('LQT150 : ? :: TVP250 : SYW470 :: UKL350 : ONX570'))],
 18:[('546 : 511 :: 9745 : 9710 :: 5736 : ?', K('546 : 511 :: 9745 : 9710 :: 5736 : ?'))],
 56:[('3 : 1', K('3 : 1')), ('5 : 3', K('5 : 3'))],
}
REP_EN = {55: [('p-q : q-r : r-s = 3 : 4 : 7', K('p - q : q - r : r - s = 3 : 4 : 7')), ('(p+s) : r', K('(p + s) : r'))],
          57: [('(7/5)', K(r'\dfrac{7}{5}')), ('(6/7)', K(r'\dfrac{6}{7}'))]}
REP_HI = {55: [('p - q : q - r : r - s = 3 : 4 : 7', K('p - q : q - r : r - s = 3 : 4 : 7')), ('(p + s) : r', K('(p + s) : r'))],
          57: [('(7/5)', K(r'\dfrac{7}{5}')), ('(6/7)', K(r'\dfrac{6}{7}'))]}
FIXED_STEM = {
 43: K(r'\dfrac{(0.625 \times 0.4) + (0.25 \times 0.8)}{0.18} = ?'),
 45: K(r'\sqrt{15^{2} + 5 \times 7 - 4 \times 18 + 8} = ?'),
}
FIXED_OPTS = {
 46: [K(r'12\sqrt{3}'), K(r'10\sqrt{2}'), K(r'12\sqrt{2}'), '48'],
 53: [K(r'\dfrac{27}{19}'), K(r'\dfrac{26}{15}'), K(r'\dfrac{27}{20}'), K(r'\dfrac{27}{13}')],
 54: [K(r'\dfrac{2}{3}'), K(r'\dfrac{3}{4}'), K(r'\dfrac{5}{7}'), K(r'\dfrac{3}{8}')],
 55: [K('2 : 1'), K('1 : 2'), K('3 : 1'), K('1 : 3')],
}
KEY_FIX = {}
EN_EDIT = {
 7: [(' II. C is to the immediate left', '[BR]II. C is to the immediate left')],
 22: [],
 33: [("'Fred Darrington Award for Excellence in Art and Culture' in 2025", "'Fred Darrington Sand Master Award' in 2025")],
 34: [("Which river is known as the 'Dakshina Ganga'?", "Which river, the longest river of peninsular India, is known as the 'Dakshina Ganga'?")],
 40: [(' II. The Ganga Plains', '[BR]II. The Ganga Plains')],
 68: [('for the following. Something that', 'for the following.[BR]Something that')],
 73: [('where did they go? D. And I said', 'where did they go?[BR]D. And I said')],
 74: [('everything and everywhere. A. Abruptly', 'everything and everywhere.[BR]A. Abruptly'),
      ("sweet stuff shop. B. After", "sweet stuff shop.[BR]B. After"),
      ("with a certain care. C. Dusk", "with a certain care.[BR]C. Dusk"),
      ("they were treading. D. The inspector", "they were treading.[BR]D. The inspector"),
      ("Hampstead Heath. S2. He was", "Hampstead Heath.[BR]S2. He was")],
 75: [('We bought an antique mirror from the flea market with a gilded frame.', 'We bought an antique mirror <u>from the flea market with a gilded frame</u>.')],
}
HI_EDIT = {
 7: [(' II. C, W के ठीक बाईं ओर है।', '[BR]II. C, W के ठीक बाईं ओर है।')],
 16:[('फिर 1 and 3 पर', 'फिर 1 और 3 पर')],
 33: [("'कला और संस्कृति में उत्कृष्टता के लिए फ्रेड डारिंगटन पुरस्कार'", "'फ्रेड डारिंगटन सैंड मास्टर पुरस्कार'")],
 34: [("किस नदी को 'दक्षिण गंगा' के नाम से जाना जाता है?", "प्रायद्वीपीय भारत की सबसे लंबी नदी, जिसे 'दक्षिण गंगा' के नाम से जाना जाता है, कौन-सी है?")],
 40: [(' II. गंगा का मैदान', '[BR]II. गंगा का मैदान')],
}
OPT_FIX = {2: {'N': 'NY'}, 22: {'Dhol, Harmonium, and Manjira': 'Dhol and Tirududi (jingle sticks)', 'ढोल, हारमोनियम और मंजीरा': 'ढोल और तिरुडुडी (घुँघरू वाली छड़ियाँ)'}}
# Q63: options C and D were both "Exaggerate" (also in GU) -> C made a misspelling so only the key D is correct; Q66 "Professiona" -> "Professional"
OPT_FIX_EN = {63: {'Exaggerate#C': 'Exagerate'}, 66: {'Professiona': 'Professional'}}
OPT_FIX_HI = {51: {'4900': '4850'}}
HPD_STEM = {
 67: [('जब किसी सुरक्षा कर्मी को प्रशंसा दी जाती है, तो वह क्या कहलाता है?',
       'जब किसी सुरक्षा कर्मी को अच्छे कार्य के लिए प्रशंसा-पत्र या पदक दिया जाता है, तो वह क्या कहलाता है?')],
 73: [('अपराध स्थल पर मौजूद व्यक्ति को क्या कहा जाता है?',
       'अपराध होते समय घटनास्थल पर मौजूद रहकर घटना को अपनी आँखों से देखने वाले व्यक्ति को क्या कहा जाता है?')],
 74: [('पुलिस द्वारा कानून के अनुसार किया गया कार्य क्या कहलाता है?',
       'किसी मामले में पुलिस द्वारा कानून के अनुसार उठाया गया कदम क्या कहलाता है?')],
 75: [('पुलिस द्वारा किसी क्षेत्र में अतिरिक्त सुरक्षा लगाना क्या कहलाता है?',
       'किसी क्षेत्र में शांति बनाए रखने के लिए पुलिस बल की तैनाती और ज़रूरी प्रबंध करना क्या कहलाता है?')],
}
HPD_OPT = {72: {1: 'गवाह से विरोधी पक्ष द्वारा पूछताछ (जिरह)'}, 77: {3: 'शिक्षा का'}}

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
    for k, x in enumerate(q['opts']):
        v = clean(x).replace('\u200b', '').strip()
        v = OPT_FIX.get(n, {}).get(v, v)
        fx = (OPT_FIX_EN if lang == 'EN' else OPT_FIX_HI).get(n, {})
        v = fx.get(v + '#' + 'ABCD'[k], fx.get(v, v))
        out.append(v)
    return out

def block(n, subj, concept, text, op, ans):
    return f"[Q{n}]\nSUBJECT: {subj}\nCONCEPT: {concept}\nTEXT: {text}\nA: {op[0]}\nB: {op[1]}\nC: {op[2]}\nD: {op[3]}\nANSWER: {ans}\n"

def header(lang): return f"# TRICKYSSC QUESTIONS\nEXAM: ssc-gd\nYEAR: 2026\nPAPER: {PAPER}\nLANG: {lang}\n"

# one RC passage for Q76-80 (all five copies identical); the generic instruction line is dropped (the PASSAGE label replaces it)
PASSAGE_EN = clean(EN[75]['comp'])
assert all(clean(EN[i]['comp']) == PASSAGE_EN for i in range(75, 80))
PASSAGE_EN = PASSAGE_EN.replace('Read the following passage carefully and answer the questions based on the passage:[BR]', '', 1)
assert not PASSAGE_EN.startswith('Read')

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
            p = p.replace('[BR]उपरोक्त गद्यांश के आधार पर प्रश्न का उत्तर दें:', '')
            p = p.replace('आपसी विश्वास विश्वास और', 'आपसी विश्वास और')
            assert 'उपरोक्त' not in p and 'विश्वास विश्वास' not in p
            t = 'PASSAGE (Q76–Q80): ' + p + ' || ' + t
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
    for need in ['A: NY\n', 'C: Exagerate\n', 'D: Exaggerate\n', 'C: Professional\n', 'A: Dhol and Tirududi (jingle sticks)\n', 'Sand Master Award',
                 'longest river of peninsular India', '[BR]II. C is', '[BR]II. The Ganga', 'following.||Something', 'go?[BR]D. And I said',
                 '[BR]S2. He was', '<u>from the flea market with a gilded frame</u>', r'\( \dfrac{27}{20} \)', r'\( \dfrac{7}{5} \)',
                 r'\( p - q : q - r', r'\( 3 : 1 \)', r'\( \text{EQ} : \text{ZK}', r'\( 546 : 511', 'PASSAGE (Q76–Q80): Lord of the Flies']:
        assert need in en, need
    for bad in ['Professiona\n', 'Exaggeratte\nB: Ecaxaggerate\nC: Exaggerate', '\\frac{', '​', ' , ', 'Read the following passage']:
        assert bad not in en, bad
    assert hp.count('PASSAGE (Q76–Q80)') == 5 and 'विश्वास विश्वास' not in hp and 'D: शिक्षा का\n' in hp and 'जिरह' in hp
    assert 'प्रशंसा-पत्र या पदक' in hp and 'अपनी आँखों से' in hp and 'उठाया गया कदम' in hp and 'बल की तैनाती' in hp and '​' not in hp
    h = json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8'))
    assert h['51']['opts'][3] == '4850' and h['2']['opts'][0] == 'NY' and 'तिरुडुडी' in h['22']['opts'][0] and '1 और 3' in h['16']['TEXT']
    assert 'सैंड मास्टर' in h['33']['TEXT'] and 'सबसे लंबी नदी' in h['34']['TEXT'] and '[BR]II. गंगा' in h['40']['TEXT'] and '[BR]II. C, W' in h['7']['TEXT']
    assert h['43']['TEXT'].startswith('निम्नलिखित') and h['45']['TEXT'].startswith('निम्नलिखित') and r'\( \dfrac{7}{5} \)' in h['57']['TEXT']
    assert '\\frac{' not in json.dumps(h) and h['55']['opts'][0] == r'\( 2 : 1 \)'
    print('ok')
