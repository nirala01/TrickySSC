# PROMPT-5 (GD) — Question `.txt` files → 4 TrickySSC CSVs

For **SSC GD Constable CBE** papers. The CHSL PROMPT-5 is 100-question / four-band shaped
and assumes Part D exists only in English; on GD that silently ships a Hindi paper whose
language part is a translation of the English questions instead of the paper's own Hindi
questions — use this version instead.

**Purpose.** Given `<PREFIX>-questions-EN.txt` (80 blocks, the source of truth for Q1–80 of
the English paper), `<PREFIX>-questions-HI-partD.txt` (20 blocks, the paper's Hindi
Part D, source of truth for Q61–80 of the Hindi paper) and the GD PDF (key/figure
reference), produce four CSVs — questions and solutions, EN and HI — with high-accuracy
multi-step solutions.

**Produce exactly four files**, then `present_files` them (questions-EN first):
```
<PREFIX>-questions-EN.csv
<PREFIX>-questions-HI.csv
<PREFIX>-solutions-EN.csv
<PREFIX>-solutions-HI.csv
```
GD slug convention: `ssc-gd-2025-04-feb-shift-1` — the CSV prefix is the SAME slug as the
`.txt` (as on CHSL).

---

## 1. THE THINGS THAT MAKE THIS FILE DIFFERENT — 80 QUESTIONS, TWO PART-Ds

GD is 20/20/20/20, and the language part differs by paper:

| Band | Part | Subject string (EN files) | Subject string (HI files) | Depth bar | HI questions | HI solutions |
|---|---|---|---|---|---|---|
| Q1–20 | A | `General Intelligence & Reasoning` | same | ≥3 `Step` headings | translated | translated |
| Q21–40 | B | `General Knowledge & General Awareness` | same | ≥4 bullets + Exam-Facts block | translated | translated |
| Q41–60 | C | `Elementary Mathematics` | same | ≥3 `Step` headings, every step KaTeX | translated | translated |
| Q61–80 | D | `English Language` | **`Hindi Language`** | 2–3 context bullets + 1 bullet per option | **the paper's own Hindi items from `-HI-partD.txt`** | **written in Hindi, about the Hindi item** |

**So the HI files are NOT "EN translated".** Q1–60 are translations of the English items;
Q61–80 are different questions entirely (the Hindi paper's Part D), with their own key,
options and solutions. Nothing in the English band stays English in the Hindi files —
there is no "reuse the EN string" rule on GD. Every rule the CHSL prompt writes as
"Q1–25 stays English in both Hindi files" is DELETED here, and every "keys identical
across EN and HI" check is LIMITED TO Q1–60.

```python
REASON_BAND  = range(1, 21)      # Part A
GK_BAND      = range(21, 41)     # Part B
MATHS_BAND   = range(41, 61)     # Part C
LANG_BAND    = range(61, 81)     # Part D: English items in EN files, Hindi items in HI files
TRANSLATED   = range(1, 61)      # HI = translation of EN
N_Q          = 80

SUBJECT_EN = {}
for n in REASON_BAND: SUBJECT_EN[n] = "General Intelligence & Reasoning"
for n in GK_BAND:     SUBJECT_EN[n] = "General Knowledge & General Awareness"
for n in MATHS_BAND:  SUBJECT_EN[n] = "Elementary Mathematics"
for n in LANG_BAND:   SUBJECT_EN[n] = "English Language"
SUBJECT_HI = dict(SUBJECT_EN)
for n in LANG_BAND:   SUBJECT_HI[n] = "Hindi Language"
```

Confirm the bands against the SUBJECT lines of both `.txt` files before building; if a
future paper prints a different order, take the bands from that paper.

**Every band-dependent CHECKER rule is re-pointed**: the stray-`Option (X)` exemption
(language band, both files), the no-Devanagari rule (EN files only — the HI files are
Devanagari throughout), the facts-block rule (GK band), the KaTeX rule (Maths band), the
key-identity rule (Q1–60 only), the HI≠EN rule (Q1–60 only; Q61–80 are compared to the
`-HI-partD.txt` instead).

---

## 2. STEP ZERO — AUDIT BOTH SOURCE `.txt` FILES BEFORE ANY CSV WORK

**2a. Diff the live `.txt` files against the copies already delivered to outputs.** A
parallel surface may have edited them mid-run. If one differs, diff first, then run the
scan that would justify the edit, before overriding — an unexplained edit is often a
documented fix.

**2b. B1 padded-colon scan** on every TEXT and option cell of both files:
```python
s = re.sub(r'\\\(.*?\\\)', 'KTX', cell)   # NOT ' KTX ' — that manufactures a space
hits = re.findall(r'\s:', s)
```
Fix at SOURCE by KaTeX-wrapping the ratio/analogy, rebuild, re-deliver the `.txt`.
Tight colons are not hits. **B1 beats "simple math stays Unicode" — never revert a wrap.**

**2c. Blank-option scan.** `^\s*$` on any option, either file, is a PROMPT-1 miss (an
image-typeset maths option was never typed). Stop and fix the `.txt`.

**2d. Hindi source hygiene.** Every stem of `-HI-partD.txt` contains Devanagari; no doubled
matra (`(?P<m>[ािीुूेैोौंः])(?P=m)`), no `SubQuestion`, no `Comprehension:` residue.

**2e. Check `/home/claude/p5` for an inherited build.** Import every inherited module first
(a syntax error is the cheapest catch), then verify CONTENT — not just dict coverage.

---

## 3. Output schemas

**Questions CSV** header, exactly:
```
qNum,subject,exam,year,text,option_A,option_B,option_C,option_D,correct
```
`text` and `option_A…D` copied **verbatim** from the `.txt` (keep `||`, `[BR]`, `\( \)`,
`<u>`, `[FIGURE-BASED]`, `(figure N)`). `subject` per §1 — note it DIFFERS between the EN and
HI questions files in the language band. `exam` = `ssc-gd`, `year` = the header value,
`correct` a single `A/B/C/D`.

**Solutions CSV** header, exactly:
```
qNum,explanation,trick,concept
```
`concept` = the `.txt` CONCEPT value, **English in all four files** (the Hindi items carry
an English label such as `Hindi — Sandhi`).

**Encoding:** UTF-8 **with BOM** (`utf-8-sig`), `csv.writer`, **80 data rows per file**.

---

## 4. Solution quality bar

Author in raw text using two primitives: lines beginning `Step N:` (`चरण N:` in Hindi)
become bold headings; lines beginning `-> ` become orange bullets.

**GD level, not CGL level.** The paper is 10th-standard; a three-step solution that a
first-attempt candidate can follow beats a six-step derivation. Never pad to hit a bar —
if an item is one idea, write two sharp steps and a verdict and let the trick carry it.
Minimums: Reasoning and Maths ≥3 `Step`; GK ≥4 bullets plus a facts block; language
bands 2–3 context bullets plus one bullet per option.

**GK solutions teach, not just verify** (standing instruction from student feedback): the
facts block is a SHORT related fact or two that the next GD shift could ask — the sibling
article, the year, the other scheme in the same ministry — never a paragraph.

**MATH MUST RENDER, NOT SIT AS PLAIN TEXT.** Wrap every formula, fraction, ratio, power,
percentage and arithmetic step in `\( … \)`: fractions → `\dfrac{a}{b}` never `a/b`;
roots → `\sqrt{x}`; `\times` / `\div`; `19\%`. Write `\( 12 \times 62 = 744 \)`, not
`12 x 62 = 744`. **Single backslashes** (CSV, not JSON). Keep the real `₹`, never `₹`.
`esc()` escapes `& < >` for you — author real `<`/`>`/`&`, do not pre-escape.

**Money in solutions uses `₹`, not `Rs.`** Question cells stay verbatim.

**Never change the answer key.** Verify, don't recompute. If your working disagrees, carry
the `.txt` letter and flag it; change only on the user's explicit instruction.

**Do not hard-code option letters** in any Q1–60 explanation — SSC randomises option order
per candidate. Name the thing ("the +2 shift", "the dice face opposite R"), never the
letter. The generated verdict line carries the letter. The language band Q61–80 is exempt
in BOTH languages because its bar requires one bullet per option.

**A conceptual maths item will trip the "every maths solution uses KaTeX" rule.** The right
fix is to ADD a genuine formula step in both languages, never to exempt the question.

**Hindi-language items (HI files Q61–80)** are grammar/vocabulary questions in Hindi:
explain the rule in Hindi (संधि-विच्छेद, समास का भेद, विलोम, पर्यायवाची, मुहावरे का अर्थ,
वर्तनी), one bullet per option in letter order via `opt_bullets` on the HI option texts,
a `याद रखें:` line as the trick. No English in these cells beyond grammatical labels in
parentheses where they help.

---

## 5. Two helpers that make misalignment structurally impossible

```python
def opt_bullets(n, opt, src="EN"):
    """opt = {<exact option text>: <note>}; emits one bullet per option in letter order.
    src="EN" reads the EN .txt options; src="HI" reads the -HI-partD.txt options (Q61-80)."""
    Qs = Q_EN if src == "EN" else Q_HI
    texts = [Qs[n][L] for L in "ABCD"]
    assert not [t for t in texts if t not in opt], f"Q{n} missing keys"
    assert not [k for k in opt if k not in texts], f"Q{n} extra keys"
    out = []
    for L, t in zip("ABCD", texts):
        plain = re.sub(r'</?u>', '', t)
        lab = "Option" if src == "EN" else "विकल्प"
        out.append(f'-> {lab} ({L}) “{plain}” — {opt[t]}' if len(plain) <= 60
                   else f'-> {lab} ({L}) — {opt[t]}')
    return "\n".join(out)

def hi_opts(n, mp):
    """Q1-60 only. mp = {<exact EN option text>: <HI option text>}; options absent from mp stay English."""
    assert n in TRANSLATED, f"Q{n}: Q61-80 come from -HI-partD.txt, never from hi_opts"
    texts = [Q_EN[n][L] for L in "ABCD"]
    assert not [k for k in mp if k not in texts], f"Q{n} extra keys"
    return [mp.get(t, t) for t in texts]
```
The **letter never appears in the authoring data**, so a rebalance cannot desync it.
Options that must stay English in the Hindi Q1–60 (letter/number series, coding strings,
single letters, KaTeX ratios, `(figure N)`) are simply omitted from the map.

Both helpers assert coverage, so a misspelt option is a build-time error. Expect the
assertion to fire on **typographic** mismatches — a curly apostrophe where the `.txt` has a
straight one. Fix the KEY to match the `.txt` byte for byte; never edit the `.txt`.

**The Hindi questions file is assembled from two sources, by band:**
```python
for n in range(1, 81):
    if n in TRANSLATED:  row = (n, SUBJECT_HI[n], EXAM, YEAR, hi_stem(n), *hi_opts(n, HI_MAP[n]), Q_EN[n]["ANSWER"])
    else:                row = (n, "Hindi Language", EXAM, YEAR, Q_HI[n]["TEXT"], *[Q_HI[n][L] for L in "ABCD"], Q_HI[n]["ANSWER"])
```
Note the key for Q61–80 comes from `-HI-partD.txt`, not from the EN file.

---

## 6. Hindi rules

- **Q1–60 questions:** translate the stem to natural Hindi. Keep in English: letter and
  number series and clusters, coding letters, all maths/KaTeX, figure labels, official
  English scheme names (with Devanagari gloss where common: `प्रधानमंत्री जन धन योजना (PMJDY)`).
  Indian proper nouns → Devanagari.
- **Q1–60 solutions:** `चरण N:` headings, Hindi bullets, `अतिरिक्त तथ्य:` facts block for GK.
- **Q61–80 (Hindi Language):** questions verbatim from `-HI-partD.txt`; solutions per §4.
- `subject` per §1 (`Hindi Language` in the HI questions file for Q61–80); `concept` stays
  English everywhere; the key is identical across EN and HI for Q1–60 and comes from the
  Hindi source for Q61–80.
- **Devanagari inside a KaTeX `\text{}` does not render.** Move the Hindi word OUTSIDE the
  span and use a bare symbol defined in Hindi prose. Scan tricks and facts, not just steps.
  **Locate the literals by grepping the SOURCE** for `text\{[^}]*[अ-ॿ]`.
- Bare-expression maths items have no prose to translate — add a natural Hindi instruction
  before the `||`.
- Raw Hindi solution text carries a **bare `&`**; typing `&amp;` makes `esc()` emit `&amp;amp;`.
- `(figure N)` option labels stay exactly `(figure N)` in the Hindi file — the engine
  swaps them for the uploaded images by that label.

---

## 7. The raw-string traps — five variants

All trace to `create_file` writing text literally.

1. **`\uXXXX` inside a raw string survives verbatim.** The only reliable test is to scan the
   EMITTED value — import the modules and regex the assembled `steps + facts + trick`.
2. **`\"` inside a raw string survives.** A pre-import `chr(92)+chr(34)` scan is the only
   catch; fix by converting the pair to curly quotes.
3. **A non-raw `"...\times..."`** emits `\t` as a literal TAB. Author every KaTeX-bearing
   string as a raw string — including `trick` values and `facts` entries — and run under
   `-W error::SyntaxWarning`.
4. **`\n` INSIDE A RAW STRING.** Bullets authored as `r"-> text\n"` emit a literal
   backslash-n, fusing the bullets into one. **The tell is a BULLET COUNT below the bar,
   not any escape scan.** Fix: replace `\n"` with `" "\n"` so adjacent-literal
   concatenation supplies a real newline. `\neq` is a legitimate false positive.
5. **`<u>…</u>` must not appear in SOLUTION text** — `esc()` turns it into a literal
   `<u>its</u>` on the site. Author emphasis as curly quotes. `opt_bullets` strips `</?u>`
   from option text, so only hand-authored steps and tricks are exposed — check both
   languages.

---

## 8. Module split that works (12 modules)

`base.py` (bands, both parsers, `esc`/`h_step`/`h_bul`/`h_verdict`/`to_html`, `opt_bullets`,
`hi_opts`, `write_q`, `write_s`) · `sol_en_1..4` (Q1-20 / 21-40 / 41-60 / 61-80) ·
`hi_q_1..3` (Q1-20 / 21-40 / 41-60 — there is no `hi_q_4`; Q61–80 come from the source) ·
`hi_sol_1..4` (Q1-20 / 21-40 / 41-60 / 61-80 Hindi-language solutions) · `assemble.py` ·
`checks.py` · `controls.py`.

Module names are `HQ_1`/`HS_1`, not `HQ1`. Write outputs to a LOCAL dir and copy to
`/mnt/user-data/outputs` in a retry loop — never write straight to the mounts.

---

## 9. Self-check (all must pass, locally AND on the md5-matched mount copies)

1. Headers exactly per §3; UTF-8 BOM present on all four; **80 rows**; `qNum` 1..80 in order.
2. `subject` per §1 in **each** question file — `English Language` in EN, `Hindi Language`
   in HI for Q61–80, the three shared strings for Q1–60; `exam` = `ssc-gd` and `year`
   constant in **both** (a wrong year in questions-HI has slipped through before).
3. Keys: EN CSV key == `-questions-EN.txt` key row by row (Q1–80); HI CSV key == EN key for
   Q1–60 and == `-HI-partD.txt` key for Q61–80; report both A/B/C/D distributions.
4. Question `text` and all four options: EN rows byte-identical to the EN `.txt`; HI rows
   Q61–80 byte-identical to `-HI-partD.txt`.
5. Every explanation ends with a verdict whose letter equals that file's `correct`. Strip
   the verdict div before any other explanation scan.
6. No stray option letters outside the language band, case-insensitive and Hindi-aware:
   `(?:[Oo]ption|विकल्प)\s*\(([A-D])\)` on Q1–60 of both solution files.
7. **Depth by band** (§1): Reasoning and Maths ≥3 `Step`/`चरण`; GK ≥4 bullets plus a facts
   block (`Exam Facts` / `अतिरिक्त तथ्य`); language band ≥6 bullets with `Option (A)…(D)` /
   `विकल्प (A)…(D)` present in letter order. Check EN and HI.
8. Every maths explanation contains `\(` in both languages.
9. Hindi files: every Q1–80 stem and solution contains Devanagari; for Q1–60 the HI solution
   ≠ EN solution and `||` is preserved where the EN stem has it; for Q61–80 the HI solution
   mentions at least two of the four HI option texts (it is about THAT item, not a copy).
   EN files: zero Devanagari anywhere.
10. **Hindi option alignment, three ways (Q1–60):** digit-multiset per letter; a HI option
    equal to a DIFFERENT English option fails; and recompute every Hindi row through
    `hi_opts` from the imported `hi_q` modules, comparing stem and all four options.
    **(Q61–80):** options equal the `-HI-partD.txt` options in order.
11. No Devanagari inside any `\( … \)` span, in any cell.
12. KaTeX integrity: balanced `\(`/`\)`; no literal `\uXXXX`, TAB, or doubled backslash.
    Split the bare-command scan in two — (a) brace-taking (`frac dfrac tfrac sqrt text
    operatorname`) on the WHOLE cell for `cmd{` not preceded by backslash or letter;
    (b) symbol commands (`times div pi theta cdot circ`) INSIDE spans only. The span
    lookbehind must exclude `{` too. **`"[" + BS + BS + "A-Za-z]"` — write the doubled
    backslash from the start**; the single form is a bad-escape crash.
13. Unknown-command whitelist wide enough for real prose; after widening, PROVE it still
    catches a dropped backslash (`dfrac{`) and `\costheta`.
14. No plain-text math in SOLUTION cells only (`\bRs\.?\s*\d`, `\d\s*x\s*\d`).
15. B1 padded-colon scan returns zero on every question cell of both files.
16. Every cell non-empty (`trick` exempt only in the questions files); no `(figure N)`
    label without a matching figure question in the `.txt`.
17. All four files re-open cleanly with `csv.DictReader`.

**Then READ the assembled text.** Content defects have been caught only by reading. On
figure items, compare EN against HI — where one language is concrete and the other
generic, the generic one is usually the defect. On Q61–80 read the Hindi solution against
the Hindi question, not against the English one.

---

## 10. Negative controls — row-level, never string replacement

Parse with `csv.DictReader`, edit ONE named cell of ONE `qNum`, **assert the cell actually
changed**, rewrite with `csv.writer`, then require `checks.py` to FAIL. Catch `Exception`.
Locate every anchor programmatically with a `find()` helper that asserts `index >= 0`.

Proven set to carry over (re-pointed to GD bands), plus the GD-specific ones in bold:
question text drift · option text altered · EN key flip · HI key flip only (Q1–60) ·
**HI key flip in Q61–80** · wrong subject · **`English Language` left in the HI file for
Q61–80** · **`Hindi Language` leaking into the EN file** · wrong exam · wrong year in the HI
file · dropped row · **81st row** · renamed header · stripped BOM · empty cell · concept
drift · concept translated · verdict removed · wrong verdict letter · steps<3 EN · steps<3
HI · GK facts removed EN/HI · language-band option bullet dropped (EN and **HI**) ·
hard-coded `Option (X)` · hard-coded `विकल्प (X)` · Devanagari leaking into an EN file ·
HI stem losing Devanagari · HI solution merely copying EN (Q1–60) · **HI Q61–80 options
not equal to the Hindi source** · **HI Q61–80 solution copied from the EN Q61–80 solution**
· HI stem losing `||` · HI option digit-set broken · HI option swapped to another EN
option · HI option ≠ recomputed module · dropped backslash on dfrac · dropped backslash on
times · constructed `\costheta` · unbalanced paren · injected `\uXXXX` · injected TAB ·
doubled backslash · B1 padded colon · plain-text `Rs` · plain-text `x` math · Devanagari
inside a span · **`(figure 2)` rewritten as `(चित्र 2)`**.

Retargeting rules for no-ops: anchor Reasoning/Maths mutations on `</strong></div>` (no
bullets there); a "steps < 3" mutation needs a solution with EXACTLY 3 steps; find a
`\dfrac` row programmatically; CONSTRUCT the `\cmd\cmd` adjacency by injecting `\costheta`;
edit BOTH files when a check compares them.

---

## 11. Sanity notes specific to GD

- **Four files of similar size.** With 80 rows and a short paper, expect roughly
  questions-EN 25 KB, questions-HI 35 KB, solutions-EN 120–150 KB, solutions-HI 130–160 KB.
  `solutions-HI` is usually LARGER than EN on GD because Q61–80 are full Hindi solutions,
  not a reuse. Check depth with §9, not with file size.
- **Figures:** Feb 04 S1 had five figure questions (Q2, Q4, Q11, Q14, Q16) — GD Reasoning
  almost always has some. The docx comes from PROMPT-2-GD; the CSVs only carry the labels.
- **The two Part-Ds share numbers 61–80 but nothing else.** A check that "EN and HI keys
  are identical" over the whole file is WRONG on GD and will fail on a correct build.

## 12. Deliver

`present_files` the four CSVs, questions-EN first. Report: checks run and failures, control
score, the four file sizes, the A/B/C/D key distributions (EN, HI Q1–60, HI Q61–80), and
any defect you carried or flagged.

Then upload with `batch-uploader.html` (prefix `ssc-gd-2025-04-feb-shift-1`, exam
auto-detected as `ssc-gd`, tier stays `tier1`, keep "upload figure images" and the
`papers` card ticked); the GD PYQ page rebakes itself from the `papers` card within 6 h.
