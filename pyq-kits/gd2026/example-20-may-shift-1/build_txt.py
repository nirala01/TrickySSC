import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-20-may-shift-1'
PAPER = 'SSC GD Constable 2026 May 20 Shift 1'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {6, 7, 17, 18, 19, 37}   # [FIGURE-BASED] stems
FIGOPT = {6, 7, 17, 18, 19}    # options are figures too (Q37: umpire-signal photo stem, text options)
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
def F(a, b, tail): return K(r'\dfrac{' + a + '}{' + b + '}' + tail)
REP = {
 8:[('? : FI68 :: MO44 : PR91 :: UZ28 : XC75', ana('? : FI68 :: MO44 : PR91 :: UZ28 : XC75'))],
 9:[('TUE150 : LZW370 :: KJR230 : ? :: RAC340 : JFU560', ana('TUE150 : LZW370 :: KJR230 : ? :: RAC340 : JFU560'))],
 10:[('1382 : 1435 :: ? : 4398 :: 1354 : 1407', K('1382 : 1435 :: ? : 4398 :: 1354 : 1407'))],
 11:[('658 : 2641 :: 644 : ? :: 859 : 3445', K('658 : 2641 :: 644 : ? :: 859 : 3445'))],
 # the source dropped the comma between the 2nd and 3rd terms
 14:[('BLA2027 CKB1854', 'BLA2027, CKB1854')],
 20:[('10 : 13', K('10 : 13'))],
 56:[('9 : 11', K('9 : 11'))],
 57:[('(3/4)', K(r'\dfrac{3}{4}'))],
}
REP_EN = {}
REP_HI = {}
FIXED_STEM = {
 43: K(r'\dfrac{8(1.5)^{3} + 1}{(3)^{2} - 2} = ?'),
 44: K(r'\sqrt{45} \times \sqrt{5} = ?'),
 45: K(r'(\sqrt{10} + \sqrt{3}) + \dfrac{1}{\sqrt{10} - \sqrt{3}} = ?'),
 49: K(r'2[(345)^{2} + (155)^{2}] - (345 - 155)^{2} = ?'),
}
FIXED_STEM_L = {}
FIXED_OPTS = {
 45: [F('7', '8', r'(\sqrt{10} + \sqrt{3})'), F('8', '7', r'(\sqrt{10} + \sqrt{3})'), F('4', '7', r'(\sqrt{10} + \sqrt{3})'), K(r'\sqrt{10} + \sqrt{3}')],
}
KEY_FIX = {}
EN_EDIT = {
 # 1102 per sq km is the PROVISIONAL Census 2011 figure for Bihar; the final figure is 1106; key B kept
 32: [('According to the Census of India 2011, the population density',
       'According to the provisional population totals of the Census of India 2011, the population density')],
 63: [('With trepidition,', 'With <u>trepidition</u>,')],
 69: [('sentence.[BR]bringing your identity proof', 'sentence.[BR]_____ bringing your identity proof')],
 73: [('The Golden Temple was crowded by millions of devotees from all around the world on the day of Baisakhi.',
       'The Golden Temple was / crowded by millions of devotees / from all around the world / on the day of Baisakhi.')],
 75: [('stakeholders are in the same page before', 'stakeholders are <u>in the same page</u> before')],
}
HI_EDIT = {
 32: [('भारत की जनगणना 2011 के अनुसार,', 'भारत की जनगणना 2011 के अनंतिम (प्रोविज़नल) आँकड़ों के अनुसार,')],
}
# Q56 options "7:3"/"3:7" spaced like the other two (then KaTeX-wrapped)
OPT_FIX = {56: {'7:3': '7 : 3', '3:7': '3 : 7'}}
# Q64 B "Wisper" -> "Whisper" (misprint in a synonym item); Q65 D "Paralle" (truncated, so C and D were both misspelt) -> "Parallel"
OPT_FIX_EN = {64: {'Wisper': 'Whisper'}, 65: {'Paralle': 'Parallel'}}
OPT_FIX_HI = {}
HI_STEM_FIX = {}
HPD_STEM = {
 64: [('निम्न में से कौन-सा एक अर्धविराम का चिन्ह है?', 'निम्न में से कौन-सा अर्धविराम का चिह्न है?')],
 65: [("'अभियोजन की विफल दलील' का सही तकनीकी शब्द है?", "'अभियोजन की विफल दलील' के लिए सही तकनीकी (अंग्रेज़ी) शब्द है?")],
 # वायरलेस सेट (and the other two) also fitted the bare stem "पुलिस द्वारा उपयोग किया जाने वाला संचार साधन"; key B रेडियो प्रणाली kept
 79: [('पुलिस द्वारा उपयोग किया जाने वाला संचार साधन क्या कहलाता है?',
       'पुलिस के नियंत्रण कक्ष, थानों और गश्ती वाहनों के बीच बिना तार के तुरंत संदेश भेजने और पाने की पूरी व्यवस्था क्या कहलाती है?')],
}
# Q62 A "तूफ़ान" (the nukta form is also standard; key B तूफान) -> "तूफ़ाण"; Q63 C/D repeated A/B (उधम, ऊधम) -> "उद्धम"/"ऊध्म";
# Q79 A "वायरलेस सेट" -> "डाक प्रणाली"
HPD_OPT = {62: {0: 'तूफ़ाण'}, 63: {2: 'उद्धम', 3: 'ऊध्म'}, 79: {0: 'डाक प्रणाली'}}
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

# one RC passage for Q76-80 (all five copies identical, no instruction line in comp); the instruction sits at the start of each stem
assert all(EN[i]['comp'] == EN[75]['comp'] for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
PASSAGE_EN = clean(EN[75]['comp'])
assert PASSAGE_EN.startswith("In the 1920s, Albert Einstein") and '[BR]' not in PASSAGE_EN
RC_INSTR = 'Read the following passage carefully and answer the questions based on the passage:||'
# Hindi Part D passage is Q74-Q78 (hi[93..97]); Q61-Q73, Q79, Q80 standalone
assert all(HI[i]['comp'] == HI[93]['comp'] for i in range(93, 98)) and all(not HI[i]['comp'] for i in list(range(80, 93)) + [98, 99])
HPD_PASSAGE = clean(HI[93]['comp'])
assert HPD_PASSAGE.startswith("शहरी क्षेत्रों में बढ़ती जनसंख्या")

def build_en():
    out = [header('EN')]
    for i in range(80):
        q = EN[i]; n = i + 1
        t = stem(q, n, 'EN')
        if q['comp']:
            assert t.startswith(RC_INSTR), n
            t = 'PASSAGE (Q76–Q80): ' + PASSAGE_EN + ' || ' + t[len(RC_INSTR):]
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
