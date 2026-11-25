# RRB NTPC UG PYQ — convert one "Paper Set" PDF (TrickySSC)

Attached: ONE QMaths PDF named like `Set_NN_DDMonYYYY_HHMMAM_to_HHMMPM.pdf`. The kit (this file, the scripts, the chapter list and the finished Set 1 as a worked example) lives in the repo at `pyq-kits/NTPC-UG-PYQ-KIT.zip` and is downloaded in step 0.

Do the whole set end to end without stopping to ask. Deliver one zip; then end with the ready-to-copy prompt for the next set (Set NN+1).

## 0. Setup
```
mkdir -p /home/claude && cd /home/claude
curl -sLO https://raw.githubusercontent.com/nirala01/TrickySSC/main/pyq-kits/NTPC-UG-PYQ-KIT.zip
unzip -o NTPC-UG-PYQ-KIT.zip                                         # gives tools/ p5/ ref-set01/
# if curl is blocked: git clone --depth 1 https://github.com/nirala01/TrickySSC repo && unzip -o repo/pyq-kits/NTPC-UG-PYQ-KIT.zip
pip install --break-system-packages -q pymupdf python-docx pillow
mkdir -p w/sNN out && cp <the PDF> w/sNN/src.pdf                    # NN = set number, no leading zero (w/s2)
```
Uploads can fail to copy once; retry with `sleep 2`.

## 1. The paper
- QMaths "Paper Set N" PDFs: header line `Paper Set N · DD Mon 2026 · HH:MM - HH:MM · English`.
- 100 questions, subject printed on each (`Quant` 30 → `Mathematics`, `GA` 40 → `General Awareness`, `Reasoning` 30 → `General Intelligence and Reasoning`). The extractor maps them; never re-classify.
- Key = the option whose label `X.` is coloured `#065f46` (green box, ✓). The extractor reads it; it must find exactly 100 greens.
- Stray answer-key ids are glued to some stems (`…formed?5289`, a line `11026`). The builder strips them and prints `stray digits stripped` — check each one.
- Image-typeset maths (fractions, exponents, vinculum, π, cm²) appears as images or flattened text (`243` for 24³, `m/s2`). Render the page (`pdftoppm -r 110 -f P -l P`), read it, and retype as KaTeX in `TEXT` / `OPTS` of `edits.py`.
- A question that needs a picture to answer (Venn diagram, chart, figure series) gets `TEXT` starting `[FIGURE-BASED] ` and an entry in `FIGURES = {qNum: "qNN"}`; `build_figs_ug.py` crops its stem image into the figures docx.

## 2. Names (derive from the header)
- Shift from the time: 9:00 AM = 1, 12:45 PM = 2, 4:30 PM = 3.
- `META = dict(K=N, EXAM="rrb-ntpc-ug", YEAR="2026", DATE="DD/MM/2026", TIME="…", SHIFT=s, PAPER="RRB NTPC UG CBT-1 2026 Mon DD Shift s", PREFIX="rrb-ntpc-ug-2026-DD-mon-shift-s")`
  e.g. Set 1 → `rrb-ntpc-ug-2026-07-may-shift-2`. The prefix MUST contain `ntpc-ug` (the uploader routes on it).
- Zip folder: `Set-NN_<PREFIX>`; zip name `Set-NN_<PREFIX>.zip`.

## 3. Steps
1. `python3 -W ignore tools/ug_extract.py w/sNN/src.pdf` → must print `bad []`.
2. Dump all 100 (see `ref-set01/` for the dump code in this file's §6) and **solve every Maths and Reasoning question yourself**. Check doubtful GA / current-affairs keys with web search.
3. Write `w/sNN/edits.py` (copy the shape of `ref-set01/edits.py`): META, CONCEPT (all 100), CH (chapterId, all 100, family must match the subject: `ga.*`, `quant.*`, `reason.*`, only ids in `p5/chapter_ids.txt`, at most 3 `.other`), TEXT and OPTS overrides, FIGURES, FLAGS.
   - Use `[BR]` for real line breaks (statements, code lists, series lines, "In a certain code language," lists). Use `||` + `[BR]` table rows only if the paper has a table.
   - KaTeX-wrap any `a : b` ratio/analogy (no space before a bare colon outside `\( \)`), and any fraction, power, root, π.
   - Use `×` not `x` for the code-language operator.
4. `python3 -W ignore tools/build_txt_ug.py NN` → `FAILURES: []`, subjects 40/30/30, controls all caught.
5. If FIGURES is not empty: `python3 -W ignore tools/build_figs_ug.py NN`, then view the PNG to confirm it is whole.
6. Author `w/sNN/a1.py … a4.py` (dict `D`, same keys as `ref-set01`): a1 = Q1–30 Maths, a2 = Q31–50 GA, a3 = Q51–70 GA, a4 = Q71–100 Reasoning (follow the paper's actual subject ranges if they differ; each Q in exactly one file).
   - `es` / `hx`: Maths and Reasoning = at least 3 lines `Step n:` / `चरण n:`, every Maths step with KaTeX `\( … \)`; GA = at least 4 lines `-> …` plus `ef` / `hf` lists of 2+ extra exam facts.
   - `et` / `ht`: one-line trick. `hs`: full Hindi stem (same `[BR]`, `||`, `[FIGURE-BASED]`, KaTeX as EN). `ho`: Hindi option map `{exact EN option: HI}`; leave out options that stay English (letters, numbers). HI options keep exactly the same digits.
   - Never write "option A/B…" or "विकल्प A…" in a solution or trick (the verdict line is added automatically). No `Rs`, no `2 x 3` outside KaTeX, no Devanagari inside KaTeX, ₹ outside KaTeX, no `<`/`>` (use ≤ ≥ or words).
   - Official key is never changed. If your derivation disagrees, keep the key, say so plainly in both EN and HI solutions ("the official key marks … ; RRB may revise this key"), and add it to FLAGS. Printing errors: carry verbatim, explain in the solution.
7. `cd p5 && python3 -W error::SyntaxWarning assemble.py NN && python3 checks.py NN && python3 -W ignore controls.py NN` → `FAILURES: 0` and `controls caught X/X`.
8. Replay the uploader's prefix detection (batch-uploader.html `metaFromPrefix`, from the public repo raw file) on PREFIX → exam `rrb-ntpc-ug`, correct heldOn and Shift.
9. Zip `Set-NN_<PREFIX>/` with: `<PREFIX>-questions-EN.txt`, the four CSVs, and `<PREFIX>-figures.docx` if any. Send the zip.

## 4. Report (short)
Set, date, shift, prefix; subjects 40/30/30; key A/B/C/D counts; figure questions; flagged keys and printing errors; checks and controls result. Then:
- Upload: `batch-uploader.html` → drop the four CSVs (+ figures docx, tick "upload figure images" if present). Exam auto-detects as `rrb-ntpc-ug`, tier `tier1`, keep the papers card ticked.
- Then run the GitHub workflow "Build RRB NTPC UG PYQ page" (or wait for the weekly run).

## 5. Next-set prompt to print at the end
```
Convert RRB NTPC UG PYQ Set <N+1>. Attached: the Set <N+1> PDF. First download the kit: curl -sLO https://raw.githubusercontent.com/nirala01/TrickySSC/main/pyq-kits/NTPC-UG-PYQ-KIT.zip, unzip it in /home/claude, then follow PROMPT-NTPC-UG-SET.md in it end to end without asking, deliver the Set-<N+1> zip, and end with this same prompt for Set <N+2>.
```

## 6. Dump snippet
```python
import sys; sys.path.insert(0,'/home/claude/tools')
from ug_extract import extract
Q,h=extract('/home/claude/w/sNN/src.pdf'); print(h)
for n in range(1,101):
    q=Q[n]; print(f"Q{n} [{q['subj'][:4]}] p{q['pno']+1} imgs={len(q['stem_imgs'])}+{[len(o['imgs']) for o in q['opts']]}")
    print('  ', ' / '.join(''.join(s['text'] for s in l['spans']) for l in q['stem']))
    for o in q['opts']: print('    ', '*' if o['g'] else ' ', o['L'], o['t'])
```
