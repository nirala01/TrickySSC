import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conv import clean
from concepts import CON_EN, CON_HI
HERE = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(f'{HERE}/raw/data.json'))
EN, HI = o['en'], o['hi']
PREFIX = 'ssc-gd-2026-19-may-shift-3'
PAPER = 'SSC GD Constable 2026 May 19 Shift 3'
SUBJ = {0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG = {18, 19, 20}      # [FIGURE-BASED] stems
FIGOPT = {18, 19, 20}   # options are figures too
def K(x): return r'\( ' + x + r' \)'
def T(s): return r'\text{' + s + '}'
def ana(s):
    return K(' '.join(T(t) if re.search('[A-Z]', t) else t for t in s.split(' ')))
def F(a, b): return K(r'\dfrac{' + a + '}{' + b + '}')
REP = {
 10:[('7650 : 7705 :: 8436 : ? :: 1123 : 1178', K('7650 : 7705 :: 8436 : ? :: 1123 : 1178'))],
 11:[('8209 : 8243 :: 8433 : ? :: 301 : 335', K('8209 : 8243 :: 8433 : ? :: 301 : 335'))],
 58:[('(1/2)', F('1', '2'))],
 60:[('3 : 5', K('3 : 5'))],
}
REP_EN = {35: [('I. Oxandrolone II. Oxabolone', 'I. Oxandrolone[BR]II. Oxabolone')]}
REP_HI = {35: [('I. ओक्सैंड्रोलोन II. ओक्साबोलोन', 'I. ओक्सैंड्रोलोन[BR]II. ओक्साबोलोन')]}
FIXED_STEM = {}
FIXED_STEM_L = {}
FIXED_OPTS = {
 9: [F('1','2'), F('1','3'), F('1','4'), F('1','6')],
 46: [F('13','16'), F('11','14'), F('15','18'), F('8','11')],
 59: [F('7','16'), F('9','16'), F('11','16'), F('13','16')],
}
KEY_FIX = {}
EN_EDIT = {
 # the award is the Green Society of India's 'Most Impactful Environmentalist' (5 June 2025); key A kept
 33: [('Who was honoured with the most influential environmentalist award on World environment Day 2025?',
       "Who was honoured with the 'Most Impactful Environmentalist' award by the Green Society of India on World Environment Day 2025?")],
 # in 1949 Cariappa became Commander-in-Chief; the title 'Chief of the Army Staff' came only in 1955; key B kept
 37: [('Who was the First Indian to become Chief of the Army Staff in 1949, and later became Field Marshal?',
       'Who became the first Indian Commander-in-Chief of the Indian Army in 1949 and was later made a Field Marshal?')],
 63: [('Global health experts warned that the next pandemic could emerge from zoonotick diseases transmitted',
       'Global health <u>experts</u> warned that the next <u>pandemic</u> could emerge from <u>zoonotick</u> diseases <u>transmitted</u>')],
 70: [('signed with a view of promoting bilateral trade relations between the two', 'signed <u>with a view of promoting bilateral trade relations between</u> the two')],
 71: [('Hariharan was terrified the roaring', 'Hariharan was terrified _____ the roaring')],
 72: [('silver. A. So, the Hail came.', 'silver.[BR]A. So, the Hail came.'), ('chimney pots down. D. Then', 'chimney pots down.[BR]D. Then')],
 # source underlined part = option B word for word, so B and D were both right; "Irregardless" (non-standard) restored; key B kept
 75: [('[BR]Regardless of the heavy rain and the muddy trails, they', '[BR]<u>Irregardless of the heavy rain and the muddy trails</u>, they')],
}
HI_EDIT = {
 33: [('विश्व पर्यावरण दिवस 2025 पर सबसे प्रभावशाली पर्यावरणविद् पुरस्कार से किसे सम्मानित किया गया?',
       "विश्व पर्यावरण दिवस 2025 पर ग्रीन सोसाइटी ऑफ इंडिया द्वारा 'मोस्ट इम्पैक्टफुल एनवायरनमेंटलिस्ट' (सबसे प्रभावशाली पर्यावरणविद्) पुरस्कार से किसे सम्मानित किया गया?")],
 37: [('1949 में सेनाध्यक्ष बनने वाले और बाद में फील्ड मार्शल बनने वाले पहले भारतीय कौन थे?',
       '1949 में भारतीय सेना के पहले भारतीय कमांडर-इन-चीफ (प्रधान सेनापति) बनने वाले और बाद में फील्ड मार्शल बनाए गए व्यक्ति कौन थे?')],
}
OPT_FIX = {}
# Q71 B "at" ("terrified at" is also used) -> "for"; Q76 C repeated B word for word -> our own wrong option
OPT_FIX_EN = {71: {'at': 'for'}, 76: {'Literary work as an isolated artistic creation#C': "Literary work as a record of the author's private feelings"}}
OPT_FIX_HI = {}
HI_STEM_FIX = {}
HPD_STEM = {
 64: [('निम्न में से कौन-सा एक योजक का चिन्ह है?', 'निम्न में से कौन-सा योजक चिह्न है?')],
 65: [("'गणतंत्र '", "'गणतंत्र'")],
 66: [("'घात '", "'घात'")],
 # "जिम्मेदारी को पूरा करना" is कर्तव्य-पालन, not उत्तरदायित्व itself; key C kept
 67: [('सुरक्षा कर्मी को दी गई जिम्मेदारी को पूरा करना क्या कहलाता है?', 'सुरक्षा कर्मी को सौंपी गई जिम्मेदारी को एक शब्द में क्या कहते हैं?')],
 # तलाशी also fitted "किसी स्थान की जांच"; key निरीक्षण kept
 79: [('पुलिस द्वारा किसी स्थान की जांच करना क्या कहलाता है?', 'किसी वरिष्ठ पुलिस अधिकारी द्वारा थाने या किसी स्थान की व्यवस्था और कामकाज को देख-परखकर जाँचना क्या कहलाता है?')],
 # लोक संपर्क / नागरिक संपर्क / सामाजिक संपर्क also fitted; stem sharpened and options replaced; key जन संवाद kept
 80: [('पुलिस द्वारा जनता से संपर्क की प्रक्रिया क्या कहलाती है?', 'पुलिस और जनता के बीच आपसी बातचीत द्वारा विश्वास बढ़ाने की प्रक्रिया क्या कहलाती है?')],
}
# Q71 B "मूल्यांकन लिए" -> "मूल्यांकन के लिए"; Q78 B/D "फाइल कक्ष"/"रजिस्टर कक्ष" also fitted -> "पूछताछ कक्ष"/"प्रतीक्षा कक्ष";
# Q80 B/C/D synonyms of the key -> "भीड़ नियंत्रण"/"जन निगरानी"/"नाकाबंदी"
HPD_OPT = {71: {1: 'कार्यों की प्रगति और सुरक्षा का मूल्यांकन करने के लिए'}, 78: {1: 'पूछताछ कक्ष', 3: 'प्रतीक्षा कक्ष'},
           80: {1: 'भीड़ नियंत्रण', 2: 'जन निगरानी', 3: 'नाकाबंदी'}}
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

# one RC passage for Q76-80 (all five copies identical); the inline instruction line is dropped
assert all(EN[i]['comp'] == EN[75]['comp'] for i in range(75, 80)) and all(not EN[i]['comp'] for i in range(75))
PASSAGE_EN = re.sub(r'^(<u>)?Read the following passage carefully and answer the questions based on the passage:\s*(</u>)?(\[BR\])?\s*', '', clean(EN[75]['comp']))
assert PASSAGE_EN.startswith("Sociological criticism enjoyed")
# Hindi Part D: the source hangs the passage on hi[95..99] (Q76-Q80), but the passage items are Q73-Q77 (hi[92..96]);
# Q78-Q80 are standalone police-terminology items
assert all(HI[i]['comp'] == HI[95]['comp'] for i in range(95, 100)) and all(not HI[i]['comp'] for i in range(80, 95))
HPD_PASSAGE = clean(HI[95]['comp'])
assert HPD_PASSAGE.startswith("आंतरिक सुरक्षा प्रणाली में नैतिकता")
HPD_RANGE = range(73, 78)

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
        if n in HPD_RANGE:
            t = 'PASSAGE (Q73–Q77): ' + HPD_PASSAGE + ' || ' + t
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
