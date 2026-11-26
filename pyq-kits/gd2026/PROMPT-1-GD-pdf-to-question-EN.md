PROMPT 1 (GD) — SSC GD CONSTABLE ADDA247 PAPER → QUESTION DOCS   (run in Claude / Opus)
======================================================================================
For **SSC GD Constable CBE** papers as Adda247 publishes them (file names like
`SSC-GD-CONSTABLE-04-02-2025-Shift-I-Paper.pdf`). This is a THIRD source shape — neither
the CGL Adda247 layout nor the CHSL Oliveboard response sheet — so use this prompt and not
either of those:

* the paper has a **real text layer** (verbatim text and the key both come from it);
* the key is the **colour of the option line** (green = correct, red = wrong), not a tick
  image and not a response-sheet cell;
* questions are numbered **Q.1–Q.20 inside every part** — the global number has to be
  derived;
* **Part D is printed twice**: once in English (20 Qs) and once in Hindi (20 different Qs).
  One PDF therefore yields 100 blocks: 80 for the English paper and 20 Hindi-language items
  that only the Hindi paper uses.

Attach the GD PDF, set the FILL-IN values, paste the block below.
Save the two outputs as `<PREFIX>-questions-EN.txt` and `<PREFIX>-questions-HI-partD.txt`.

Built from SSC GD 2025, 04 Feb Shift 1 (the first GD paper processed).

------------------------------- COPY BELOW -------------------------------

Convert the attached SSC GD Constable paper into two strict text files that a deterministic
converter will read. Output ONLY the doc text — no commentary, no markdown fences, nothing
before or after it.

FILL-IN (use these exact values):
EXAM   = ssc-gd
YEAR   = 2025
PAPER  = SSC GD Constable 2025 Feb 04 Shift 1
PREFIX = ssc-gd-2025-04-feb-shift-1

FILE 1 — `<PREFIX>-questions-EN.txt` — begins with this header (once):

# TRICKYSSC QUESTIONS
EXAM: <EXAM>
YEAR: <YEAR>
PAPER: <PAPER>
LANG: EN

then exactly 80 question blocks [Q1]…[Q80], in order, each shaped EXACTLY like:

[Q1]
SUBJECT: <General Intelligence & Reasoning | General Knowledge & General Awareness | Elementary Mathematics | English Language>
CONCEPT: <short English topic label, no paper name>
TEXT: <instruction>||<question body>
A: <option A>
B: <option B>
C: <option C>
D: <option D>
ANSWER: <A|B|C|D from the colour key>

FILE 2 — `<PREFIX>-questions-HI-partD.txt` — same header with `LANG: HI`, then exactly 20
blocks [Q61]…[Q80] with `SUBJECT: Hindi Language`, carrying the paper's Part-D-Hindi
questions in Devanagari, verbatim. CONCEPT stays an English label
(e.g. `Hindi — Paryayvachi (synonym)`, `Hindi — Sandhi`, `Hindi — Muhavara (idiom)`).

Each field is on its OWN line.

==========================================================================
STEP 0 — THREE THINGS TO DO BEFORE READING ANY QUESTION
==========================================================================

0a. SAVE THE PAGES FIRST. The uploaded PDF can age out of /mnt/user-data/uploads MID-TURN.
    Copy it to /home/claude/w with a retry-with-backoff loop, then render and save every
    page (300 DPI for analysis, 170 DPI for visual reading) as the very first action.
    Both mounts can throw transient `OSError: [Errno 5]` that clears on retry — never write
    straight to the mounts.

0b. CONFIRM THE DATE AND SHIFT PROGRAMMATICALLY. Page 1 carries a header table:
        Exam Date   04/02/2025
        Exam Time   9:00 AM - 10:00 AM
        Subject     Constable GD Examination 2025
    Regex the text layer of ALL pages for date / time strings; the header values must be
    the only ones in the document. The PDF prints NO shift number — derive it from the time
    (9:00 = Shift 1, 11:45 = Shift 2, 2:30 = Shift 3, 5:15 = Shift 4 on the 2025 timetable)
    and cross-check against the roman numeral in the file name (`Shift-I`). Report date,
    time and the derived shift before anything else — the user asks for this on every paper.

0c. DERIVE THE PART RANGES FROM THE `Section : Part-x-…` HEADINGS AND RENUMBER.
    The paper restarts at Q.1 in every part. The headings are:

        Part-A-General Intelligence and Reasoning      local Q.1–20  →  global Q1–20
        Part-B-General Knowledge and General awareness local Q.1–20  →  global Q21–40
        Part-C-Elementary Mathematics                  local Q.1–20  →  global Q41–60
        Part-D-English                                 local Q.1–20  →  global Q61–80  (FILE 1)
        Part-D-Hindi                                   local Q.1–20  →  global Q61–80  (FILE 2)

    Track the current part while walking pages in order (a heading page also holds the
    tail of the previous part — e.g. page 7 starts with Part-A Q.19–20 and then opens
    Part-B at Q.1). Global number = part offset + local number. NEVER number by page order
    or by counting blocks; a skipped ad page or a two-page question will shift everything.
    State the five heading pages you found.

    SKIP AD PAGES. Page 2 (and sometimes the last page) is a full-page Adda247 promo: no
    text layer, one 595×841 raster. It carries no questions — do not let it break the
    part-tracking or the image inventory.

==========================================================================
STEP 1 — THE ANSWER KEY (span colour, not tick images)
==========================================================================

Every option line is a text span `"<n>. <option text>"` whose COLOUR is the key:

    green  0x40c64b  (R 64, G 198, B 75)   = the correct option
    red    0xf61818  (R 246, G 24,  B 24)  = a wrong option
    body   0x252525                        = stem text

Read `page.get_text("dict")` and classify each span whose text matches `^\d\.\s` by its
`color`: green if G−R > 60 and G−B > 60; red if R−G > 100. The tick (✔) and cross (✘) are
tiny raster images (two xrefs reused on every page) — IGNORE them, they carry nothing the
colour does not.

**The numeral keeps its colour even when the option BODY is an image** (see Step 4 — maths
options such as `18%` or `16 4/5` are typeset rasters and the text layer shows only `1. `).
So the key is always recoverable from the `n.` span.

RECONCILIATION — all must hold, per file:
    exactly 4 option spans per question, exactly 1 green and 3 red
    80 greens in FILE 1, 20 greens in FILE 2, zero questions with 0 or 2 greens
Attach each option span to the LAST `Q.<n>` span at or above it (by y, carrying across a
page break — options often continue onto the next page). State the counts in your report.
If any question has ≠1 green, you have mis-attached a span across a page break — fix that,
never "pick the best mark".

RE-DERIVE EVERY REASONING AND MATHS KEY INDEPENDENTLY by solving the item, and report
agreement. Treat a disagreement under HONEST-KEY below.

==========================================================================
STEP 2 — TEXT: THE TEXT LAYER IS THE DRAFT, THE PAGE IMAGE IS THE AUTHORITY
==========================================================================

Pull every stem and option from the text layer first — it is verbatim for Parts A–C and
Part-D-English and gives you a free drift check. Then READ EVERY PAGE at ~170 DPI and
reconcile. Known places where the layer lies:

  • OPTION BODIES THAT ARE IMAGES (Part C). Percentages, mixed fractions, surds and whole
    expressions are typeset as small rasters (height ≤ 40 px) and the layer shows `1. `
    followed by nothing. Type them from the page as KaTeX (Step 4). On Feb 04 S1: C-Q9
    (18% / 82% / 20% / 80%), C-Q10 (18 2/5 … four mixed fractions, each built from 4–5
    tiny rasters), C-Q11 stem expression, C-Q14 options. A blank option in the layer is
    the tell — scan for `^\d\.\s*$` and resolve every hit visually.
  • HINDI (Part-D-Hindi). The layer's Devanagari has glyph-order faults
    (`वाक्यांांश` for `वाक्यांश`, broken matras). Use it as a draft only; every Hindi stem
    and option is read from the page and corrected. Zero tolerance for a doubled matra.
  • PASSAGES. Cloze/comprehension items print as:
        Comprehension:
        <instruction> <passage with (1)____ … (5)____>
        SubQuestion No : 20
        Q.20
        Select the most appropriate option to fill in blank no 5.
    Drop the `Comprehension:` and `SubQuestion No : N` lines. Carry the passage per Step 4.
  • Curly quotes (‘JAMB’) are real in the layer — keep them exactly.

==========================================================================
STEP 3 — SUBJECT, CONCEPT
==========================================================================

SUBJECT is fixed by the part the question sits under (Step 0c) — the four strings above
in FILE 1, `Hindi Language` in FILE 2. No other spelling.

CONCEPT is a short English label: `Coding-Decoding`, `Venn Diagram`, `Dice`, `Number
Series`, `Seating Arrangement`, `Indian Polity — Fundamental Rights`, `Profit & Loss`,
`Time & Work`, `Error Spotting`, `Cloze Test`, `Hindi — Vilom (antonym)` … For Part B
prefer `<Chapter> — <sub-topic>` so the GK coverage can be tracked later.

==========================================================================
STEP 4 — MARKUP RULES (TEXT and options are VERBATIM)
==========================================================================

Whatever you type lands in the cell, so YOU place every token:

• Instruction vs question → split with ||  (left = instruction, right = the thing being
  tested). If the instruction IS the whole question, use no ||.
• Line break inside a cell → [BR]  (never press Enter inside a field).
• A series or expression printed on its own line → `instruction||208 190 163 127 82 ?`.
• Target word the paper underlines or BOLDS → <u>word</u>. A plain instruction phrase
  ("correct spelling", "same meaning") gets no tag.
• Error-spotting → instruction || Seg A / Seg B / Seg C / Seg D
  GD prints the segments INLINE with letter labels `(A) … / (B) … / (C) … / (D) …` and the
  options as bare letters — expand the options to the full segment texts, keep the printed
  option order, and NEVER put <u> on any segment.
• Inequalities between variables → &lt; and &gt;. Keep ≤ ≥ ∠ ∴ π ° ₹ △ ± × ÷ √ x² Unicode.
• Figure question → TEXT: [FIGURE-BASED] <text>, options (figure 1) … (figure 4).
  A question whose STEM has a figure but whose options are text keeps its text options;
  a question whose OPTIONS are figures (Venn items) gets `(figure 1)…(figure 4)` even when
  the stem has no picture. Global numbering, so A-Q2 is `[Q2]`, A-Q11 is `[Q11]`.
• Passage / cloze → full passage before its first question, repeated per Q:
      PASSAGE (Q76–Q80): <full passage> || <the specific question>
  Keep the paper's blank markers `(1)__________` exactly; the question says which blank.
• Hindi file: the same rules; `||` and `[BR]` are ASCII and unaffected by Devanagari.
• Money stays as printed in question cells (`₹1,566`).

------------------------------------------------------------
MATHEMATICAL RENDERING
------------------------------------------------------------
The site renders math with KaTeX between \( ... \).
• Wrap stacked/nested math (fractions, mixed numbers, surds, bracketed expressions) in
  \( ... \) with BACKSLASH delimiters. Opening MUST be \( and closing MUST be \).
  Mixed number 16 4/5 → `\( 16\dfrac{4}{5} \)`. Image-typeset percentage → plain `18%`
  is fine (it is not stacked) — but it must be TYPED, never left blank.
• NEVER drop the leading backslash: frac{a}{b} / sqrt{3} / imes are all WRONG.
• Simple inline math (√2, x², ≤, π, ÷, ×) stays Unicode.
• EXCEPTION THAT OVERRIDES THE UNICODE RULE — B1 below.

==========================================================================
STEP 5 — THE B1 PADDED-COLON RULE
==========================================================================

The live renderer splits a PADDED colon, so `4 : 9` reaches the site as `4 :[BR]9`. Any
RATIO or ANALOGY written with spaces around its colons must be KaTeX-wrapped:

    4 : 9                     →   \( 4 : 9 \)
    234 : 9 :: 341 : ?        →   \( 234 : 9 :: 341 : ? \)
    CE : VX :: KG : ?         →   \( \text{CE} : \text{VX} :: \text{KG} : ? \)

B1 BEATS the "simple inline math stays Unicode" rule. TIGHT colons (`3:5:7`) are NOT B1
hits. A padded colon in ORDINARY PROSE cannot be wrapped — delete the stray space instead.
Feb 04 S1 C-Q7 ("ratio of 4 : 9") is a hit.

RUN THIS AS A SELF-CHECK BEFORE DELIVERY on every TEXT and option cell of BOTH files:
    blank the KaTeX spans with a placeholder carrying NO surrounding spaces —
    re.sub(r'\\\(.*?\\\)', 'KTX', s) — then flag any remaining `\s:`. Expected: ZERO hits.
Hindi stems use the danda `।`, not `:`, so the Hindi file should be naturally clean; a
hit there is usually a `: ` someone typed after `विकल्प`.

==========================================================================
STEP 6 — RECURRING TRAPS
==========================================================================

GLOBAL NUMBERING — the single GD-specific failure mode. `Q.5` appears five times in the
    PDF. Every reference you make (figure docx, flags, report) uses the GLOBAL number and
    names the part once: "Q45 (Part C local Q.5)".

TWO PART-Ds — never merge them. The English paper is A+B+C+D-English; D-Hindi goes ONLY to
    FILE 2. If a FILE 1 cell contains Devanagari, a Hindi item leaked.

IMAGE-TYPESET MATHS vs FIGURES — a small raster (≤ 40 px high) sitting on an option line
    in Part C is typeset maths: TYPE it, do not ship it as a figure. A raster ≥ 70 px with a
    drawing in it (dice, Venn, paper-folding, mirror, embedded figure, matrix) is a figure:
    `[FIGURE-BASED]`. Decide by looking, not by size alone, and list both sets.

÷-vs-+ / SIGN DEGRADATION — compute every sign-substitution and BODMAS item; if the printed
    reading balances to the keyed option, the glyphs are right. If not, re-render at
    700–1200 DPI before believing the page.

DUPLICATE OPTIONS — carry verbatim, flag on delivery, exempt that question in the check.

A LITERAL `||` INSIDE A STEM (`DE || BC`) collides with the field separator — write ∥.

HONEST-KEY POLICY — never silently change a coloured key and never silently carry a wrong
    one. If your independent working disagrees with the green option, re-test the rule
    against the worked examples first. If it still disagrees, CARRY THE GREEN LETTER and
    FLAG it plainly. Change it only on the user's explicit instruction.

UNRECOVERABLE CODING ITEMS — if a letter maps to two code letters across the examples, no
    substitution table exists; say so and carry the key.

VERBATIM ODDITIES ARE CARRIED, NOT FIXED — unspaced text, "Rs." vs "₹", a stray comma, an
    option in the wrong unit. Carry and list them so the user can decide.

==========================================================================
STEP 7 — FIGURES: INVENTORY, THEN BOX-CUT FROM NATIVE RASTERS
==========================================================================

Adda247 GD files embed each figure as its own raster, so the native route works.
Inventory with `get_images(full=True)` and `get_image_rects()`:

  • CHROME to exclude: any xref used on ≥5 pages (Adda247 logo, Google Play badge,
    watermark, the ✔ and ✘ glyphs) and the full-page ad raster.
  • Attach every remaining raster to the question whose `Q.<n>` span is the last one above
    its top edge; convert to the GLOBAL number.
  • Classify: ≥ 70 px tall with a drawing → figure (Part A: Venn options, dice, paper
    folding, mirror/water image, embedded figure, figure series, matrix); ≤ 40 px on an
    option line in Part C → typeset maths (Step 2).
  • Feb 04 S1 inventory for calibration: figure Qs = Q2 (4 option rasters, no stem),
    Q4 (stem only), Q11, Q14, Q16 (stem + 4 options) — five figure questions, 20 rasters;
    typeset-maths rasters at Q49, Q50, Q51 (stem), Q54 — zero figures in B, C, D.

Verify three ways before you say "N figure questions": your `[FIGURE-BASED]` count, a
keyword sweep of the stems (figure, diagram, dice, paper, mirror, water image, embedded,
Venn, matrix, "shown below", "given below"), and the raster inventory. The three must
agree; a disagreement is a mis-attached raster. The figures docx is built by PROMPT-2-GD.

==========================================================================
SELF-CHECK BEFORE FINISHING (run programmatically; all must pass)
==========================================================================
  1. FILE 1: exactly 80 blocks [Q1]–[Q80] in order; FILE 2: exactly 20 blocks [Q61]–[Q80];
     each block has SUBJECT, CONCEPT, TEXT, A–D, ANSWER.
  2. SUBJECT matches the band: Q1–20 Reasoning, Q21–40 GK, Q41–60 Maths, Q61–80 English
     (FILE 1) / Hindi Language (FILE 2) — exact strings.
  3. ANSWER is a single A/B/C/D; report the distribution for each file (sums 80 and 20).
  4. Colour reconciliation: 1 green + 3 red per question, 80 + 20 greens.
  5. Text-layer drift check on Parts A–C and D-English: every stem and non-image option is
     byte-identical to the layer after whitespace normalisation; list every deliberate
     departure (KaTeX wraps, B1, `||` placement).
  6. No blank option anywhere (the image-typeset ones must have been typed).
  7. B1 scan (Step 5) returns ZERO padded-colon hits in both files.
  8. No raw < or > outside <u> tags; inequalities use &lt;/&gt;.
  9. Error-spotting items carry no <u>; a `contains? a[n]?\b[^|]*error` regex is required.
 10. Every \( has a matching \); no bare frac{/sqrt{/times inside a span; no literal
     \uXXXX, no literal TAB. Use `(?<![\\A-Za-z])cmd(?![A-Za-z])` for bare-command
     detection — a \b anchor misses `2sqrt{10}`.
 11. FILE 1 contains NO Devanagari; every FILE 2 stem contains Devanagari and no doubled
     matra (`[ािीुूेैोौंः]{2}` with the same character twice is a layer fault).
 12. Duplicate-option check across A–D, with an exemption list for flagged paper defects.
 13. No literal `||` inside any stem beyond the single separator.
 14. Figure count agrees three ways (Step 7).
 15. NEGATIVE CONTROLS: mutate each finished file a dozen ways (drop a block, renumber a
     part, flip a subject, leak a Hindi stem into FILE 1, blank an option, break a bracket,
     add a padded colon…) and assert the checker FAILS on each. Assert the mutation actually
     changed the file — a silent no-op proves nothing.

Output doc text only.

------------------------------- COPY ABOVE -------------------------------

Save as `<PREFIX>-questions-EN.txt` and `<PREFIX>-questions-HI-partD.txt`, plain .txt
(not .docx — .docx flattens line breaks).

Slug convention for GD: `ssc-gd-<year>-<dd>-<mon>-shift-<n>` (same shape as CHSL — the
day keeps its dash), e.g. `ssc-gd-2025-04-feb-shift-1`. The CSV and figures-docx prefix is
the SAME slug; `batch-uploader.html` reads exam `ssc-gd`, year, `04-feb` → heldOn
2025-02-04 and `shift-1` from it.

These two files feed PROMPT-2-GD (figures docx) and PROMPT-5-GD (four CSVs).
