# SSC MTS 2025 PYQ kit — lives in the repo (no download needed)

Get it at the start of every chat (git clone works from the shell; github.io / raw URLs may be blocked):

    git clone --depth 1 --filter=blob:none --sparse https://github.com/nirala01/TrickySSC /home/claude/tssc-kit
    git -C /home/claude/tssc-kit sparse-checkout set --no-cone /pyq-kits/mts2025/
    K=/home/claude/tssc-kit/pyq-kits/mts2025
    mkdir -p /home/claude/w && cp -r $K/common /home/claude/w/ && cd /home/claude/w
    pip install --break-system-packages -q pymupdf python-docx matplotlib

Source data (all 16 shifts, English only, with keys) — split into src/<dd>-<mon>-s<n>.json:

    GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 --filter=blob:none --sparse https://github.com/akarohitmishra/repeatermock-subjectwise-db /home/claude/rm
    git -C /home/claude/rm sparse-checkout set SSC-MTS
    python3 common/fetch_src.py /home/claude/rm /home/claude/w/src

At the end of every chat: mark the shift `done` in SHIFTS.md, add its line under "## Done", copy the paper's
data.py / sol_en.py / hi.py to example-<dd>-<mon>-shift-<n>/, and (Ashish's standing yes) commit + push ONLY
pyq-kits/mts2025/ to main. End the reply with the ready-to-copy prompt for the next `todo` shift.

## Source facts
- GitHub JSON (repeatermock, copied from Testbook): question, options, `correct` (1-4), `chapter`, Testbook `solution`
  (DO NOT COPY — write our own). Paper order: Q1-20 Maths (MATH n 1-20), Q21-40 Reasoning (REAS), Q41-65 GA (GK 1-25),
  Q66-90 English (ENG 1-25). `common/srckey.py` maps it.
- The JSON text has broken KaTeX (`{ km}`, `sqrt 3`, `overline 72`, `times`, `div`, `\%`) and some stems are CUT
  (e.g. 04 Feb S3 Q29 ended in `<span c`); the RC passage is MISSING. So data.py types ALL 90 stems/options cleanly
  (instruction || content, [BR] line breaks, KaTeX \( \) for maths, padded ratios/analogies KaTeX-wrapped for B1).
- The Testbook PDF (Ashish uploads it; links in SHIFTS.md) has the full stems, the passage and the figures. Use
  `pymupdf` text (`page.get_text()`) for stems/passage; its Hindi text layer is garbled, so it is NOT used.
- Hindi: Ashish chose (2026-11-26) that Claude writes its own Hindi for Q1-65 (no SSC Hindi source). Q66-90 stay
  English in the HI files (identical rows, the assembler reuses the EN objects).
- Year: `year = 2025` (the exam cycle). The prefix `ssc-mts-2025-<dd>-<mon>-shift-<n>` makes batch-uploader guess the
  held-on date as 2025-<mm>-<dd>; ASHISH MUST SET THE DATE TO 2026-02-<dd> in the uploader table.

## Figures (common/figs.py)
- DI charts (pie / bar): REDRAW our own clean chart with matplotlib from the values in the PDF picture (FIGSRC
  'pie_pct' / 'pie_deg' / 'bar'). Read the values from the PDF image itself — the repeatermock solution tables can
  differ (04 Feb S3 Q5: JSON said A108/B72/C72/D48/E60, the PDF picture shows A72/B144/C108/D12/E24; same answer).
- Figure reasoning (analogy, series, mirror, paper folding …): FIGSRC ('pdf', stem_xref, [opt xrefs]) — the raster is
  pulled from the PDF with `doc.extract_image(xref)` and thresholded (THRESH 185) to pure black/white so the Testbook
  watermark vanishes. Find xrefs with `page.get_image_info(xrefs=True)`; xref 94-style images that repeat on every page
  are the watermark. Each option appears twice (EN/HI columns) — take the four distinct xrefs in A-D order.
- The Testbook PDF can reuse a WRONG image (04 Feb S3: Q7 batsman chart = Q6's vehicle chart). Then rebuild the chart
  with the values the solution/question fix and our own values for the rest, keep the key, and report it.
- docx: title `SSC MTS 2025 – DD Mon 2026 – Shift n – Figures`, then `Q.N`, `[figure]`, picture, `Figure 1..4` + picture.

## Per paper (folder pNN with data.py, sol_en.py, hi.py, src.pdf if figures)
1. Write pNN/data.py (copy the example: META with prefix/src, FIG, FIGSRC, T for all 90, PASSAGE + PASSAGE_TEXT,
   CONCEPT, CHAPTER, FIXES). Solve EVERY question yourself first; carry the key; fix misprints per the rules below.
2. `python3 -W error::SyntaxWarning common/build_txt.py pNN && python3 common/check_txt.py pNN/out/<prefix>-questions-EN.txt pNN/data.py`
3. `python3 common/figs.py pNN && python3 common/check_docx.py pNN/out/<prefix>-figures.docx pNN/out/<prefix>-questions-EN.txt pNN/data.py`
   (skip both when FIG = {}; then there is no docx). LOOK at every figure PNG.
4. Write pNN/sol_en.py (M: Q1-40 (raw, trick); G: Q41-65 (raw, facts, trick); E: Q66-90 (context, {option: note}, trick))
   and pNN/hi.py (HQ: Q1-65 (stem_hi, {EN option: HI option}); HM: Q1-40; HG: Q41-65).
5. `python3 -W error::SyntaxWarning common/assemble.py pNN && python3 common/checks.py pNN && python3 common/controls.py pNN`
   → checks PASS, controls 55/55. Then READ the assembled text.
6. `bash common/package.sh pNN` → /mnt/user-data/outputs/<prefix>.zip (one folder: 4 CSVs, then .txt, then docx).

## Ashish's standing rules
- Maths and Reasoning solutions: AT LEAST 4 `Step`/`चरण` headings. GA: AT LEAST 5 bullets + Exam Facts / अतिरिक्त तथ्य
  (the checker wants 3 facts). English: 2-3 context bullets + one bullet per option (opt_bullets). Check every fact.
- Never change the key letter. Fix misprinted options to the intended word, replace an option so only the key is right,
  reword a wrong/ambiguous stem so the official key becomes right, complete a cut stem from the PDF — list every change.
- No option letters in Q1-65 solutions (SSC shuffles options). No Devanagari in EN files or inside \( \). ₹ not Rs.
- Chapter ids from common/chapters.py (same list as batch-uploader.html); fewer than 3 `.other`.
- Upload: Ashish drops the zip's files into batch-uploader.html himself (and fixes the held-on date), then runs
  "Build SSC MTS PYQ page".

## Done
- 04 Feb 2026 Shift 3 — built 2026-11-26 (figures Q4–Q7 redrawn charts, Q31/Q32 PDF rasters). Fixes: Q7 chart missing
  in both sources (PDF repeats Q6's graph) — rebuilt with Y3 10000, Y6 12000, Y7 11000 from the solution and our own
  Y1 9000, Y2 8000, Y4 13000, Y5 9500, key Y7 kept; Q5 chart from the PDF picture; Q29 cut stem completed from the PDF;
  Q61 "total decentralisation" → "total denationalisation"; Q69 option D "volatility" → "volatelity" (the misspelt
  underlined word); Q70 option D "Ignoreamus" → "Ignoramus" (two misspelt options); Q86–90 passage from the PDF;
  bare-expression stems Q1–3, Q18 given "Find the value of the following expression." All 90 keys agreed when solved.
