PROMPT 2 (GD) — FIGURE QUESTIONS → `<PREFIX>-figures.docx`   (run in Claude / Opus)
====================================================================================
For SSC GD Constable papers (Adda247 PDF). Run after PROMPT-1-GD, with the PDF and the
finished `<PREFIX>-questions-EN.txt` attached. The docx is read by `batch-uploader.html`
(`parseFiguresDocx`), so the paragraph grammar below is not a style choice — anything else
mis-slots an image or loses it.

Skip this prompt only when PROMPT-1-GD reported **zero** figure questions three ways
(no `[FIGURE-BASED]`, no keyword hits, no figure rasters). Feb 04 S1 had five (Q2, Q4,
Q11, Q14, Q16 — all in Part A); expect 3–7 per GD shift, essentially always Reasoning.

------------------------------- COPY BELOW -------------------------------

Build `<PREFIX>-figures.docx` for the attached SSC GD Constable paper, with
PREFIX = ssc-gd-2025-04-feb-shift-1. Use python-docx. Output only the file and a short
report.

==========================================================================
1. WHICH QUESTIONS
==========================================================================
Exactly the `[FIGURE-BASED]` blocks of `<PREFIX>-questions-EN.txt`, by GLOBAL number.
Re-derive the list from the PDF independently (raster inventory, PROMPT-1-GD Step 7) and
stop if the two lists differ. Never include a typeset-maths raster (Part C option
images such as `18%` or `16 4/5`) — those were typed as KaTeX and are not figures.

==========================================================================
2. CUTTING THE IMAGES
==========================================================================
Adda247 GD files embed every figure as its own raster, so extract NATIVELY:
`doc.extract_image(xref)` for each non-chrome xref, placed by `page.get_image_rects(xref)`.
Chrome (exclude): any xref used on ≥ 5 pages, and the full-page ad raster.

* Attach each raster to the question whose `Q.<n>` text span is the last one above the
  raster's top edge, then convert to the global number (Part A offset 0).
* Option rasters are ordered by their y (top to bottom) = option 1…4. Confirm against the
  coloured `n.` span sitting to the LEFT of each raster (same y ± 6 pt) — the span order
  and the raster order must agree, or the option images are mis-slotted.
* Keep native resolution; PNG; never upscale or recompress. If a figure is split into
  several rasters (seen on mixed-number options, not on diagrams), box-cut the region from
  a 300 DPI page render instead and say so.
* Reasoning "figure series" or "matrix" items whose stem AND options are one wide raster:
  stem raster → `[figure]`; if the options are inside the same raster the options stay
  text `(figure 1)…(figure 4)` in the .txt and the docx carries the stem only — flag it.

==========================================================================
3. DOCX GRAMMAR (the parser's rules — exact)
==========================================================================
Paragraph 1 (title, the parser reads it to match the paper):
    SSC GD Constable 2025 – 04 Feb 2025 – Shift 1 – Figures
It must contain the year, the day+month and `Shift 1`; nothing else on that line.

Then, per figure question in ascending global order:
    Q.2                      ← its own paragraph: "Q." + global number, nothing else
    [figure]                 ← only if the STEM has a picture; its own paragraph
    <stem image>             ← the image alone in the next paragraph
    Figure 1                 ← its own paragraph
    <option-1 image>         ← the image alone in the next paragraph
    Figure 2
    <option-2 image>
    Figure 3
    <option-3 image>
    Figure 4
    <option-4 image>

Rules the parser depends on:
* A label (`[figure]`, `Figure N`) sits in its OWN paragraph and the image in the paragraph
  AFTER it — never put text and an image in the same paragraph, never two images in one.
* A Venn/option-only item (Q2 on Feb 04 S1) has NO `[figure]` and goes straight from `Q.2`
  to `Figure 1`. Without the labels the parser would steal option 1 for the stem slot.
* A stem-only item (Q4, dice) has `[figure]` + image and no `Figure N` lines.
* No other text between questions — no captions, no "Answer", no "Solution" (the word
  `Solution` switches the parser into solution-image mode).
* Images are inline pictures (`add_picture`), width ≤ 4.5 in for stems, ≤ 2.2 in for
  options; the parser ignores size but Word must not float them.

==========================================================================
4. SELF-CHECK (run programmatically on the saved docx; all must pass)
==========================================================================
 1. Re-parse the docx with the same grammar (unzip `word/document.xml`, walk `w:p`, read
    `w:t` text and `a:blip r:embed`) and rebuild `{qNum: {q?, optA..optD?}}`.
 2. The question set equals the `[FIGURE-BASED]` set of the .txt, as global numbers.
 3. For each question: the .txt options are `(figure 1)…(figure 4)` ⇔ the docx has optA–optD;
    the .txt stem starts `[FIGURE-BASED]` and the PDF has a stem raster ⇔ the docx has `q`.
 4. Every image in `word/media` is referenced exactly once; no unassigned blobs.
 5. Every image decodes (PIL) and is ≥ 60 px on its shorter side; none is a ✔/✘ glyph or
    a logo (reject anything ≤ 40 px tall).
 6. Option images for one question are four DIFFERENT blobs (hash them) — identical hashes
    mean a mis-cut.
 7. Title line matches `^SSC GD Constable (20\d\d) – (\d\d) (\w{3}) \1 – Shift ([1-4]) – Figures$`
    and the date/shift equal PROMPT-1-GD's confirmed values.
 8. NEGATIVE CONTROLS: swap two option images, drop a `Figure 3` label, put a label and an
    image in one paragraph, add a stray "Solution" paragraph — assert the checker FAILS on
    each. Assert each mutation actually changed the parse.

Deliver the docx and report: the figure questions (global numbers, part, stem/option
counts), the raster xrefs used, any box-cut fallbacks, and any flag from §2.

------------------------------- COPY ABOVE -------------------------------

The docx goes to the same shift folder as the .txt and the four CSVs
(`E:\…\PYQ\<year>\<date>\<shift>\`) and is dropped into `batch-uploader.html` together with
the CSVs; the uploader matches it to the paper by prefix, or by the title line if the
file name carries no prefix.
