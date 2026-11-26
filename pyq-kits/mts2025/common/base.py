"""Shared base for SSC MTS 2023 PYQ builds (official SSC response-sheet PDFs).

Bands, .txt parser, solution HTML helpers, opt_bullets / hi_opts, CSV writers.
"""
import re, csv, io

MATHS_BAND = range(1, 21)
REASON_BAND = range(21, 41)
GA_BAND = range(41, 66)
ENG_BAND = range(66, 91)
TRANSLATED = range(1, 66)
N_Q = 90
EXAM = "ssc-mts"

SUBJECT = {}
for n in MATHS_BAND: SUBJECT[n] = "Numerical and Mathematical Ability"
for n in REASON_BAND: SUBJECT[n] = "Reasoning Ability and Problem Solving"
for n in GA_BAND: SUBJECT[n] = "General Awareness"
for n in ENG_BAND: SUBJECT[n] = "English Language and Comprehension"

DEVA = re.compile(r'[ऀ-ॿ]')


def parse_txt(path):
    """Return (header dict, {n: {SUBJECT, CONCEPT, TEXT, A, B, C, D, ANSWER}})."""
    raw = open(path, encoding='utf-8').read()
    head, _, body = raw.partition('\n[Q1]')
    body = '[Q1]' + body
    hdr = {}
    for line in head.splitlines():
        m = re.match(r'^(EXAM|YEAR|PAPER|LANG):\s*(.*)$', line)
        if m: hdr[m.group(1)] = m.group(2).strip()
    Q = {}
    for blk in re.split(r'\n(?=\[Q\d+\]\n)', body.strip()):
        lines = blk.split('\n')
        n = int(re.match(r'^\[Q(\d+)\]$', lines[0]).group(1))
        d = {}
        for line in lines[1:]:
            if not line.strip(): continue
            m = re.match(r'^(SUBJECT|CONCEPT|TEXT|A|B|C|D|ANSWER): ?(.*)$', line)
            if not m: raise ValueError(f'Q{n}: stray line {line!r}')
            if m.group(1) in d: raise ValueError(f'Q{n}: duplicate field {m.group(1)}')
            d[m.group(1)] = m.group(2)
        Q[n] = d
    return hdr, Q


# ---------------------------------------------------------------- solution HTML
def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def h_step(t):
    return f'<div class="sol-step">{esc(t)}</div>'


def h_bul(t):
    return f'<div class="sol-bullet"><span class="sol-bullet-mk">—</span><span>{esc(t)}</span></div>'


def h_sec(t):
    return f'<div class="sol-section">{esc(t)}</div>'


def h_line(t):
    return f'<div class="sol-line">{esc(t)}</div>'


def h_verdict(letter, opt_text, lang):
    plain = re.sub(r'</?u>', '', opt_text)
    show = f' — {plain}' if len(plain) <= 70 else ''
    lab = f'Correct answer: Option ({letter}){show}' if lang == 'en' else f'सही उत्तर: विकल्प ({letter}){show}'
    return f'<div class="sol-verdict"><span class="vmk">✓</span><span>{esc(lab)}</span></div>'


VERDICT_RE = re.compile(r'<div class="sol-verdict">.*?</div>\s*$', re.S)
STEP_RE = re.compile(r'^(Step|चरण)\s+\d+\s*:')


def to_html(raw, facts=None, lang='en'):
    out = []
    for line in raw.split('\n'):
        line = line.strip()
        if not line: continue
        if STEP_RE.match(line): out.append(h_step(line))
        elif line.startswith('-> '): out.append(h_bul(line[3:].strip()))
        else: out.append(h_line(line))
    if facts:
        out.append(h_sec('Exam Facts' if lang == 'en' else 'अतिरिक्त तथ्य'))
        out += [h_bul(f) for f in facts]
    return ''.join(out)


def explanation(raw, facts, letter, opt_text, lang):
    return to_html(raw, facts, lang) + h_verdict(letter, opt_text, lang)


# ---------------------------------------------------------------- helpers
def make_helpers(Q_EN):
    def opt_bullets(n, opt):
        assert n in ENG_BAND, f"Q{n}: opt_bullets is for the English band"
        texts = [Q_EN[n][L] for L in "ABCD"]
        miss = [t for t in texts if t not in opt]
        extra = [k for k in opt if k not in texts]
        assert not miss, f"Q{n} missing keys {miss}"
        assert not extra, f"Q{n} extra keys {extra}"
        out = []
        for L, t in zip("ABCD", texts):
            plain = re.sub(r'</?u>', '', t)
            out.append(f'-> Option ({L}) “{plain}” — {opt[t]}' if len(plain) <= 60
                       else f'-> Option ({L}) — {opt[t]}')
        return "\n".join(out)

    def hi_opts(n, mp):
        assert n in TRANSLATED, f"Q{n}: Q66-90 are copied from EN, never translated"
        texts = [Q_EN[n][L] for L in "ABCD"]
        extra = [k for k in mp if k not in texts]
        assert not extra, f"Q{n} extra keys {extra}"
        return [mp.get(t, t) for t in texts]
    return opt_bullets, hi_opts


def write_csv(path, header, rows):
    with open(path, 'w', encoding='utf-8-sig', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for r in rows: w.writerow(r)


QHDR = ['qNum', 'subject', 'chapterId', 'exam', 'year', 'text', 'option_A', 'option_B', 'option_C', 'option_D', 'correct']
SHDR = ['qNum', 'explanation', 'trick', 'concept']
