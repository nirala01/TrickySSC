# SSC GD 2026 PYQ kit — lives in the repo (no download needed)

Get it at the start of every chat (git clone works from the shell; github.io / raw URLs may be blocked):

    git clone --depth 1 --filter=blob:none --sparse https://github.com/nirala01/TrickySSC /home/claude/tssc-kit
    git -C /home/claude/tssc-kit sparse-checkout set --no-cone /pyq-kits/gd2026/
    # kit = /home/claude/tssc-kit/pyq-kits/gd2026

At the end of every chat: mark the shift `done` in SHIFTS.md, add its line under "## Done" below, and (Ashish's
standing yes, if given) commit + push ONLY pyq-kits/gd2026/ to main. Scripts: example-28-apr-shift-3 is the newest
(figure shift, paths are relative to the script folder); example-04-may-shift-1 is the first one.

# SSC GD 2026 PYQ conversion — method (set 2026-11-25, first paper: 04 May 2026 Shift 1, live)

## Source
- Question data: XamToppr's file store, `git clone --depth 1 https://github.com/xamtoppr/sscgdpyp2026.git`
  (github.io and cdn.testbook.com are blocked from the shell; git clone works).
  One HTML per shift: `SSC GD Constable 2026 Official Paper (Held On DD Mon, 2026 Shift N)_Multilingual.html`.
- Each file holds `Q_DATA_ALL = {en:[100], hi:[100], gu:[100]}`. Extract with node + vm (bracket-match the
  object literal). Fields: n, si (0 Reasoning, 1 GK, 2 Maths, 3 English, 4 Hindi), text, comp (passage),
  opts[4], cidx (0-3 = key), sol (Testbook's solution — DO NOT COPY, write our own).
- English paper = en[0..79] (si 0-3). Hindi paper Q1-60 = hi[0..59] (SSC's own Hindi — use it verbatim,
  do not translate). Hindi Part D = hi[80..99] (si 4) → global Q61-80 of the Hindi paper.
- 27 May Shift 2 has NO Hindi in the source — DROPPED by Ashish (2026-11-25). Do not build it.
- 27 May Shift 1 Q75 (English, error spotting) has only 3 options in the source (looking forward / to meet /
  my colleagues; key = "to meet"). Ashish's rule: add our own realistic 4th option D = `No error`, keep the
  official key B, and mention the added option in the delivery report. Same rule for any other item found
  with a missing option: write one realistic option, never change the key.
- Build order and status: SHIFTS.md (59 papers). The next shift = the first row marked `todo`.
- The data is copied from Testbook. Questions/options/keys are SSC's; solutions and figure watermarks are
  Testbook's. Figures: open the shift page in the user's Chrome (Claude in Chrome), rebuild the body with
  the figure <img>s at natural size (dpr 1), screenshot with save_to_disk, crop locally, threshold at 150
  to pure black/white (removes the faint Testbook watermark digits), save PNG. Never upscale.
- Dates/shifts were verified on 58/60 files against SSC's own response sheets (Part D only); keys for
  Part D can be spot-checked from the green "correct option" cells in those sheets.

## Output per shift (one folder, zip it)
`ssc-gd-2026-<dd>-<mon>-shift-<n>` prefix: questions-EN.txt, questions-HI-partD.txt, figures.docx (only if
the shift has figure Qs), questions-EN.csv, questions-HI.csv, solutions-EN.csv, solutions-HI.csv.
PAPER line: `SSC GD Constable 2026 <Mon> <DD> Shift <n>`; docx title `SSC GD Constable 2026 – DD Mon 2026 – Shift n – Figures`.
Questions CSV header: `qNum,subject,chapterId,exam,year,text,option_A,option_B,option_C,option_D,correct`.

## Ashish's standing rules (on top of PROMPT-1/2/5-GD + addendum)
- Reasoning and Maths solutions: AT LEAST 4 `Step`/`चरण` headings (a genuine check step is fine).
- GK solutions: AT LEAST 5 bullets + an Exam Facts / अतिरिक्त तथ्य block with AT LEAST 2 facts.
  Check every fact; don't state past events as future (e.g. Asian Games 2026 already happened).
- English Part D: 2-3 context bullets + one bullet per option. Hindi Part D: same, in Hindi, `याद रखें:` trick.
- Solve every question independently; honest-key policy (carry the key, flag disagreements).
- B1 padded colons KaTeX-wrapped in question cells AND solutions/tricks.
- GD 2026 Hindi Part D has many official-terminology items (Police custody, Remand, Memorandum …) with no
  chapter id — tag `hindi.other` and report the count.
- Run checks.py (0 failures) + controls.py (all caught) before delivery; then read the assembled text.
- Upload: Ashish drops the files into batch-uploader.html himself (file upload into his browser is not
  allowed from chat), then runs "Build SSC GD PYQ page". Claude can verify Firestore from his admin login
  and check the Pages deploy.

## Done
- 04 May 2026 Shift 1 — live (Q15 stem misprint flagged, key D carried; Q12 key C carried).
- 27 Apr 2026 Shift 2 — built 2026-11-25 (1 figure Q16; flags: Q23 Gaur dance key Holi carried, HI Q61 पिंजड़ा variant,
  Q72 option "0n" carried, Q10 "?" added, HI Q10 source cell rebuilt).
- 28 Apr 2026 Shift 1 — built 2026-11-25 (NO figure questions, so no figures.docx; flags: Q44 EN "6,25" read as 6.25 from
  the Hindi paper, Q20 Cyrillic "М" in SZHM normalised to Latin M, Q72 option "0n" carried, HI Part D Q66 बैज vs पहचान पत्र
  arguable — key A carried; HI Q46 source had a TAB for \t in \times — rebuilt; 6 hindi.other terminology items).
- 28 Apr 2026 Shift 2 — built 2026-11-25 (NO figure questions, no figures.docx). Corrections Ashish asked for: HI Part D Q71
  (source repeated Q70 "सूचना पट") REPLACED by our own item "नियंत्रण कक्ष" (key B); EN Q69/Q78 "0n" → "on", Q73 "al" → "at",
  Q78 "ät" → "at"; Q38 option D reworded to "Duty-free import of goods to develop the zone" (real SEZ developer incentive, key D kept);
  Q52 stem "5 times more than B" → "6 times B" (key 500% kept); HI Q51 option D 36 → 96; Q46 "*" → ×; 7 hindi.other.
  STANDING RULE from here: fix misprinted options (0n, al, ät …) to the intended word, replace a duplicated item with our own,
  and reword an ambiguous/wrong stem or option so the official key becomes right — never change the key letter; list each change.
- 28 Apr 2026 Shift 3 — built 2026-11-25 (figure Qs Q11, Q12 — stem + 4 options each). Source Q11 option 1 was Testbook's
  annotated SOLUTION image (handwritten arrows) — rebuilt as our own clean shaded heptagon in a frame (flood-filled copy of
  option 2's outline). Corrections: Q29 option A 1932 → 1950 (World Archery's own history: by 1950 the IOC recognised FITA;
  key A kept); Q30 stem had no question — added "Which satellite mission's data is best suited for this task?" (EN + HI);
  Q31 option "SSLP" → "SSLV"; Q61 missing blank inserted, option B "talk the wal" → "talk the wall"; Q73 option A
  "or" → "and"; Q77 passage "identify their ___B___ triggers" → "keep track of their ___B___ triggers" (unknown also fitted);
  Q78 option D "S0" → "too" (intended "so" would also have been correct); HI Q70 option A completed ("… इकट्ठा करना");
  HI Q72 "होगा:" → "होगी?"; HI Q74 stem reworded to "आधिकारिक लिखित रिपोर्ट" (पंचनामा was arguable); HI Q79 option D
  "गति और समयबद्धता से" → "सटीकता और समयबद्धता दोनों से". Carried verbatim: Q6 "atleast", Q42 "29 of 2". 6 hindi.other.

## Checker notes (fixed in example-04-may-shift-1 on 2026-11-25)
- checks.py: the word "times" in prose ("3 times as efficient") is no longer flagged; bare `times` is checked only inside \( \).
- checks.py: each docx image is hash-compared with fig/Q<n>_stem/opt1..4.png, so swapped option images are caught.
- base.py: the verdict shows ₹ instead of "Rs." when it quotes an option (question cells stay verbatim).
- For a shift with NO figure questions: set FIGQ = set() in checks.py, skip check_docx, and fail if a figures.docx is present; confirm zero figures three ways (no <img> in en[0..79] text/opts/comp, no [FIGURE-BASED], keyword sweep). Drop the docx controls in controls.py and add a "stray figures docx" control.
- Figures (2026-11-25, 28 Apr S3): cdn.testbook.com blocks fetch() from the page (CORS), so canvas export fails. Lay the
  imgs out with position:absolute inside one viewport (dpr 1), then use the `zoom` action with save_to_disk on a region —
  it returns a lossless PNG at 1:1 in /tmp/claude-tool-results/…, readable from the workspace (a plain screenshot is JPEG).
  Keep each zoom region inside what was captured (a crop past the edge fills black rows). Thin serif letters break up at
  threshold 150 — use 200 for letter/symbol figures (the watermark sits at 240–250, so it still disappears).
- If an option image is Testbook's annotated solution picture (arrows, handwriting, much larger than the others), do not
  ship it: rebuild that option cleanly and list it in the report.
