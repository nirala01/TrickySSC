import re, json, csv, html, os
from concepts import CON_EN, CON_HI, CH, CH_HI
PREFIX = 'ssc-gd-2026-18-may-shift-1'
EXAM, YEAR = 'ssc-gd', '2026'
REASON_BAND, GK_BAND, MATHS_BAND, LANG_BAND = range(1,21), range(21,41), range(41,61), range(61,81)
TRANSLATED = range(1,61)
SUBJECT_EN = {}
for n in REASON_BAND: SUBJECT_EN[n] = "General Intelligence & Reasoning"
for n in GK_BAND: SUBJECT_EN[n] = "General Knowledge & General Awareness"
for n in MATHS_BAND: SUBJECT_EN[n] = "Elementary Mathematics"
for n in LANG_BAND: SUBJECT_EN[n] = "English Language"
SUBJECT_HI = dict(SUBJECT_EN)
for n in LANG_BAND: SUBJECT_HI[n] = "Hindi Language"
HERE = os.path.dirname(os.path.abspath(__file__))

def parse_txt(path):
    src = open(path, encoding='utf-8').read()
    Q = {}
    for m in re.finditer(r'^\[Q(\d+)\]\n(.*?)(?=^\[Q\d+\]|\Z)', src, re.S | re.M):
        n = int(m.group(1)); d = {}
        for line in m.group(2).strip('\n').split('\n'):
            k, _, v = line.partition(': ')
            d[k] = v
        Q[n] = d
    return Q

Q_EN = parse_txt(f'{HERE}/out/{PREFIX}-questions-EN.txt')
Q_HI = parse_txt(f'{HERE}/out/{PREFIX}-questions-HI-partD.txt')
HI_SRC = {int(k): v for k, v in json.load(open(f'{HERE}/hi_q1_60.json', encoding='utf-8')).items()}

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def to_html(raw, letter, opt_text, lang):
    out = []
    for line in raw.strip('\n').split('\n'):
        line = line.strip()
        if not line: continue
        if re.match(r'^(Step|चरण) \d+:', line):
            out.append(f'<div class="sol-step"><strong>{esc(line)}</strong></div>')
        elif line.startswith('-> '):
            out.append(f'<div class="sol-bullet"><span class="sol-bullet-mk">—</span><span>{esc(line[3:])}</span></div>')
        elif line.startswith('## '):
            out.append(f'<div class="sol-section">{esc(line[3:])}</div>')
        else:
            out.append(f'<div class="sol-line">{esc(line)}</div>')
    plain = re.sub(r'Rs\.\s*', '₹', re.sub(r'</?u>', '', opt_text))
    show = len(plain) <= 60 and '\\(' not in plain and not plain.startswith('(figure')
    if lang == 'EN':
        v = f'Hence, option ({letter}) “{plain}” is the correct answer.' if show else f'Hence, option ({letter}) is the correct answer.'
    else:
        v = f'अतः विकल्प ({letter}) “{plain}” सही उत्तर है।' if show else f'अतः विकल्प ({letter}) सही उत्तर है।'
    out.append(f'<div class="sol-verdict"><span class="vmk">✓</span><span>{esc(v)}</span></div>')
    return ''.join(out)

def opt_bullets(n, opt, src="EN"):
    Qs = Q_EN if src == "EN" else Q_HI
    texts = [Qs[n][L] for L in "ABCD"]
    assert not [t for t in texts if t not in opt], f"Q{n} missing keys {[t for t in texts if t not in opt]}"
    assert not [k for k in opt if k not in texts], f"Q{n} extra keys {[k for k in opt if k not in texts]}"
    out = []
    for L, t in zip("ABCD", texts):
        plain = re.sub(r'</?u>', '', t)
        lab = "Option" if src == "EN" else "विकल्प"
        out.append(f'-> {lab} ({L}) “{plain}” — {opt[t]}' if len(plain) <= 60 else f'-> {lab} ({L}) — {opt[t]}')
    return "\n".join(out)

def write_csv(path, header, rows):
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
