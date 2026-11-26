# SSC GD 2026 PYQ kit — lives in the repo (no download needed)

Get it at the start of every chat (git clone works from the shell; github.io / raw URLs may be blocked):

    git clone --depth 1 --filter=blob:none --sparse https://github.com/nirala01/TrickySSC /home/claude/tssc-kit
    git -C /home/claude/tssc-kit sparse-checkout set --no-cone /pyq-kits/gd2026/
    # kit = /home/claude/tssc-kit/pyq-kits/gd2026

At the end of every chat: mark the shift `done` in SHIFTS.md, add its line under "## Done" below, and (Ashish's
standing yes, if given) commit + push ONLY pyq-kits/gd2026/ to main. Scripts: example-30-apr-shift-1 is the newest
(figure shift, paths are relative to the script folder); example-30-apr-shift-1 adds KEY_FIX (key override), HPD_OPT (Hindi
Part D option fix) and the cloze-passage blank rebuild; example-04-may-shift-1 is the first one.

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
ZIP LAYOUT (Ashish, 2026-11-25): the zip holds ONE folder named <prefix>/ (added first), and inside it the files in
this order: questions-EN.csv, questions-HI.csv, solutions-EN.csv, solutions-HI.csv, then questions-EN.txt,
questions-HI-partD.txt, then figures.docx (if any). Do not ask the user to attach the kit — clone it as shown above.
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
- 29 Apr 2026 Shift 1 — built 2026-11-25 (figure Qs Q12, Q13 — stem + 4 options each, all clean, threshold 150). Source Q68
  option A was a 10×11 px image of the word "in" — typed as text. Corrections: Q36 stem "largest saltwater lake" →
  "largest brackish-water (saltwater) lagoon" (EN) / "खारे पानी की लैगून झील" (HI) — Sambhar is the largest inland salt lake,
  so the old stem was arguable; key C Chilika kept. Q71 missing blank inserted ("tripped _____ the heap"); Q72 and Q75
  underlines restored (<u>aimed at bringing up</u>, <u>reaffirmed again his commitment</u>); Q78 option "shal" → "shall";
  HI Q63 option C "अकसर" (an accepted variant spelling of अक्सर) → "अकसार" so only the key B is correct; HI Q74
  "<u>सही</u> … क्या होगी:" → plain "सही … क्या होगी?". Hindi Part D passage is Q75–Q79 (Q80 standalone), not Q76–Q80.
  Carried verbatim: Q14 option D "U064", Q47 "What are the measure", option casing in Q64/Q65/Q78/Q80. All keys agreed.
  10 hindi.other (terminology / police-duty meaning items).
- 29 Apr 2026 Shift 2 — built 2026-11-26 (figure Qs Q11, Q12 — stem + 4 options each; Q12 stem has serif letters, cut at
  threshold 200, the rest at 150). All 80 EN keys and 20 HI Part D keys agreed. Corrections: Q32 stem adds "take g = 10 m/s²
  on Earth" (EN + HI) — 117 N is 700 ÷ 6, so g = 10 was assumed; Q38 stem "schools?" → "schools." (HI "की?" → "की।");
  Q66 options "Trivia" → "Trivial", "Usefu" → "Useful"; Q69 missing blank inserted ("blind _____ their own faults");
  Q72 option "10" → "on" (not "to": "look to the matter" is arguable); Q73 underline restored and options "n accordance
  for/on" → "in accordance for/on"; Q75 underline restored; Q76–80 cloze passage had bare letters for blanks — rebuilt as
  ___A___, ___B___, ___D___ and "(C) <u>cognitive</u>", "(E) <u>influence</u>"; Q80 stem adds "as it is used in the passage"
  (Weakness opposes the noun, Neglect the verb); HI Q72 "होगाः" → "होगी?"; HI Q77 option "एजसी" → "एजेंसी"; HI passage
  "चेन्" → "चेन". Carried verbatim: Q25 option "Kala Aur Budhdha Chand", option casing in Q65/Q67/Q68, HI Q62 "तीरथ",
  HI Q73 key ड्यूटी डायरी (रोज़नामचा/general diary is the formal term). 6 hindi.other.
  NOTE: in this file the English cloze passage sits INSIDE each Q76–80 stem (comp is empty) — split instruction /
  passage / question in build_txt.cloze(); the Hindi passage is in comp with a trailing "[BR]उपरोक्त गद्यांश …" line.
- 29 Apr 2026 Shift 3 — built 2026-11-26 (figure Qs Q12, Q13 — stem + 4 options each, all clean, threshold 200; every cut padded
  with a 4 px white margin because Q12 option 1 is natively 65×58 and the docx check needs ≥ 60 px — never upscale, pad instead).
  Figures were fetched same-origin: open one cdn.testbook.com image URL in Chrome, rebuild the page with all 10 imgs at natural
  size (dpr 1), one zoom with save_to_disk, crop locally. All 80 EN keys and 20 HI Part D keys agreed. Corrections: Q1 option
  "BZ1" → "BZJ" (EN + HI; ? = XVF + 4); Q37 stem "In June 2024" → "In August 2024" (EN) / "जून" → "अगस्त" (HI) — the PMAY-G
  2 crore rural houses were approved on 9 Aug 2024, the 10 Jun 2024 decision was 3 crore rural + urban, so option 3 was arguable;
  key 2 kept. Q71 option D "into" → "onto" ("translate from Sanskrit into English" is also right; key "to" kept); Q72 and Q75
  underlines restored; Q73 stray punctuation removed ("felt: ill", "when; he", "he; leaned", "distance: his"); Q79 options
  "shal" → "shall", "Wil" → "will"; Q76–80 one passage used for all five (source had uneven blank lengths/quote styles);
  HI Q29 option "पॉन्डिक्षेरी" → "पॉन्डिचेरी"; HI Part D Q67 stray space in 'कुख्यात '; HI Q74 "<u>सही</u> … क्या होगी:" →
  plain "सही … क्या होगी?". Hindi Part D passage is Q75–Q79 (Q80 standalone). Carried verbatim: Q24 "kalbelia", Q27 "literateur",
  Q58 options "25 percentage", Q60 "fourth proportion", option casing in Q63/Q66/Q68. Q5 (LCM) and Q6 (notes) sit in Reasoning
  but are tagged quant.lcm-hcf / quant.number-system. 8 hindi.other.
- 30 Apr 2026 Shift 1 — built 2026-11-26 (figure Qs Q11, Q12 — stem + 4 options each, all clean, threshold 200, native size, no padding
  needed). KEY: Q28 (5000 m race walk record 19:24.48) — source en/hi cidx = A "Tushar Panwar", but the source's own GU cidx = C and
  Testbook's solution in all three languages says Nitin Gupta, who set the record (20th National Youth Athletics Championships, Patna,
  10 Mar 2025) — so the official key is C; shipped C in EN + HI (KEY_FIX in build_txt.py). All other 79 EN and 20 HI Part D keys agreed.
  Corrections: Q17 option "SBlU" → "SBIU" (EN + HI); Q66 option "Concea" → "Conceal"; Q72 options "al"/"ïn"/"01" → "at"/"in"/"on";
  Q73 and Q75 underlines restored; Q76–80 passage blanks rebuilt as ___A___, ___B___, ___E___ and "(C) <u>gallantry</u>",
  "(D) <u>conspicuous</u>" (Q78/Q79 test those words), one passage for all five (Q80's copy had "different different"); HI Q11
  "(: :)" → "(::)" (B1); HI Q17 "रूप रूप" → "रूप"; HI Part D Q61 option A "बारात" (an accepted variant of बरात) → "बारत" so only the key
  B is correct; HI Q72 "<u>सही</u> … क्या होगा:" → plain "सही … क्या होगी?"; HI Q75 stem reworded to "…अपने सभी थानों और कार्यालयों को एक
  साथ भेजी जाने वाली आधिकारिक लिखित सूचना…" (key परिपत्र; the bare stem also fitted सूचना पत्र); HI Q76 stem was a copy of Q75 — replaced
  by "गद्यांश में भारत की आंतरिक सुरक्षा के लिए तैनात किन अर्धसैनिक बलों के उदाहरण दिए गए हैं?" (options/key C unchanged). Hindi Part D
  passage is Q76–Q80 (Q75 standalone). Carried verbatim: Q42 "(19 of 2)", Q30 option "Space tourism and station support" (best fit,
  key C), option casing in Q66/Q67. 11 hindi.other (Q65–Q75 police/office terminology and duty-meaning items).

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
- KEY CROSS-CHECK (2026-11-26, 30 Apr S1): compare en/hi cidx with gu cidx for all 100 items AND with the "correct answer is …"
  line of the source solution. A mismatch in en/hi only (gu + solution agree) is a Testbook entry error — use the gu/solution key
  and list it. 30 Apr S1 Q28 was the first such case.
