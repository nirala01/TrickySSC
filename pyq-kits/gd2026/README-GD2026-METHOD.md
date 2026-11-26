# SSC GD 2026 PYQ kit — lives in the repo (no download needed)

Get it at the start of every chat (git clone works from the shell; github.io / raw URLs may be blocked):

    git clone --depth 1 --filter=blob:none --sparse https://github.com/nirala01/TrickySSC /home/claude/tssc-kit
    git -C /home/claude/tssc-kit sparse-checkout set --no-cone /pyq-kits/gd2026/
    # kit = /home/claude/tssc-kit/pyq-kits/gd2026

At the end of every chat: mark the shift `done` in SHIFTS.md, add its line under "## Done" below, and (Ashish's
standing yes, if given) commit + push ONLY pyq-kits/gd2026/ to main. Scripts: example-08-may-shift-3 is the newest (figure shift with
TWO figure Qs Q9, Q10 — 10 images fetched same-origin, laid out at natural size in one 1000×240 region, one zoom save_to_disk after moving the
mouse away, threshold 200, no padding; EN RC passage instruction line stripped via INSTR; HI Part D passage is Q73–Q77 (Q78–Q80 standalone);
HPD_OPT used to replace arguable Hindi Part D options; controls.py anchors retargeted); example-08-may-shift-2 is the one before (figure shift with FOUR figure Qs Q11, Q12, Q18, Q19 — 20 images + the Q3 option C
image (typed "FA") fetched same-origin, laid out at natural size in one 1200×530 region, one zoom save_to_disk after moving the mouse away,
threshold 200, no padding; EN RC passage Q76–80 has no instruction line; HI Part D passage is Q76–Q80 (Q61–Q75 standalone); Step headings
with pairs like "LI : HD" trip the solution B1 check — write "LI → HD"; controls.py anchors retargeted); example-08-may-shift-1 is the one before (figure shift with
TWO figure Qs Q9, Q10 — 10 images fetched same-origin, laid out at natural size in one 640×520 region, one zoom save_to_disk after moving the
mouse away, threshold 200, no padding; EN RC passage instruction line stripped via INSTR; HI Part D passage is Q75–Q79 (Q80 standalone);
checks.py whitelist adds \pm; controls.py anchors retargeted to this paper); example-07-may-shift-3 is the one before (figure shift with
FOUR figure Qs Q11, Q12, Q18, Q19 — 20 images + 6 small text-option images (Q2 A/C/D, Q4 C, Q5 A, Q66 D) laid out in one 960×480 region,
fetched same-origin, one zoom save_to_disk, threshold 200; OPT_FIX now merges into OPT_FIX_EN/HI ('#A'-style keys work in both);
FIXED_STEM_L for a stem that needs its own KaTeX in each language; ratio options "a : b" auto-wrapped (B1); HI Part D passage from comp;
controls.py anchors retargeted); example-07-may-shift-2 is the one before (figure shift with
TWO figure Qs Q9, Q10 — 10 images, fetched same-origin and laid out at natural size, one zoom save_to_disk, threshold 200; the HI Part D
Q76–Q80 passage is MISSING in the source again — build_txt.HPD_PASSAGE holds our own; EN RC instruction line stripped via INSTR;
Q3 option A image typed via OPT_FIX_EN/HI '#A'; controls.py anchors retargeted to this paper); example-07-may-shift-1 is the one before (figure shift with
FOUR figure Qs Q11, Q12, Q18, Q19 — 20 images + the Q66 option image; FASTER FIGURE ROUTE: open one cdn.testbook.com image URL in
Chrome, fetch() every image same-origin into data URLs, lay them out at natural size (dpr 1), one zoom save_to_disk after moving the
mouse away, crop by the logged positions, threshold 200; English RC passage Q76–80 and HI Part D passage Q76–Q80 both come from comp
with no instruction line; REP_EN/REP_HI split "I. … II. …" statements onto their own lines; OPT_FIX_EN keys '#C' type an option image);
example-06-may-shift-3 is the one before (figure shift with
TWO figure Qs Q9, Q10 — 10 images + Q71 option image laid out in one 1000×240 region, one zoom save_to_disk after moving the mouse away,
threshold 200; the HI Part D Q76–Q80 passage is MISSING in the source (comp empty in en/hi/gu) — build_txt.HPD_PASSAGE holds our own;
EN passage instruction line stripped via INSTR; checks.py needs PROMPT-5-chapter-tagging-addendum.md copied into the script folder);
example-06-may-shift-2 is the one before (figure shift with
FOUR figure Qs Q11, Q12, Q18, Q19 — 20 images laid out in one 1366×540 region, one zoom save_to_disk after moving the mouse away,
threshold 200; source option images Q2 A / Q3 D typed via OPT_FIX keyed '' / '#D'; Hindi Part D passage is Q74–Q78; English RC passage
has no instruction line; checks.py whitelist adds \sin); example-06-may-shift-1 is the one before (figure shift with TWO figure Qs Q9, Q10 — 10 images laid out in one 1130×264 region,
one zoom save_to_disk, threshold 200; FIXED_STEM for a nested root; RC passage Q76–80 with the generic instruction line dropped;
HPD_STEM/HPD_OPT for Hindi Part D fixes); example-05-may-shift-3 is the one before (figure shift with
FOUR figure Qs Q11, Q12, Q18, Q19 — 20 images laid out in one 1060×505 region, one zoom save_to_disk; Q2 option images typed via
FIXED_OPTS; RC passage Q76–80 (comp, all five identical); HI Part D passage Q76–Q80; run the scripts WITHOUT python -I, or base.py
cannot be imported — only the source data is untrusted and it is read as JSON); example-05-may-shift-2 is the one before (figure shift with
THREE figure Qs Q12, Q13, Q20 — 15 images laid out in one 1100×420 region, one zoom save_to_disk, move the mouse away first
or the cursor lands in the cut; cloze blanks "______ A ______" rebuilt; HPD_OPT used for spelling variants); example-05-may-shift-1
is the one before and the FIRST NO-FIGURE example (FIGQ = set(), checks.py fails if a figures.docx is present or [FIGURE-BASED] appears, docx controls
replaced by a 'stray figures docx' control; RC passage Q76–80 with the generic instruction line dropped; OPT_FIX_EN keys may be
'value#L' to fix one of two identical options); example-04-may-shift-3 is the one before
(figure shift; figures fetched same-origin from cdn.testbook.com, laid out absolutely, one zoom save_to_disk; Hindi Part D passage
label Q75–Q79 set in build_txt; cloze words (D)/(E) rebuilt as "(D) <u>pacing</u>"); example-04-may-shift-2 is the one before
(figure shift; REP_EN / REP_HI for language-specific stem anchors such as a source KaTeX fraction that only one language has;
checks.py exempts SSC bilingual HI options like 'आदित्य-एल1 (Aditya-L1)' from the digit-set test and knows \overline / \ldots);
example-30-apr-shift-3 is the one before that
(figure shift, paths relative to the script folder; HPD_OPT keyed by option INDEX; hi_sol_4 maps option keys through NFC so
composed/decomposed nukta letters in the source never break opt_bullets); example-30-apr-shift-2 is the one before; example-30-apr-shift-1 adds KEY_FIX (key override), HPD_OPT (Hindi
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
- 30 Apr 2026 Shift 2 — built 2026-11-26 (figure Qs Q12, Q13 — stem + 4 options each, all clean, threshold 200, native size, no padding).
  All 80 EN and 20 HI Part D keys agreed (en/hi cidx = gu cidx = source solution line on all 100). Corrections: Q1 options A "A" and
  D "Y" were truncated in the source (EN + HI) — rebuilt as "IA" and "JY" (neither fits; key B IY kept); Q10 EN options "2400"/"1920"
  → "240O"/"192O" (the HI paper already had O); Q11 option "2160" → "216O" (EN + HI); Q14 EN option "J0310" → "JO310" (as in HI) and
  stem "?: MS710" → "? : MS710" inside the KaTeX span; Q29 stem had no distance information — added "An exoplanet orbits its star at
  the same distance at which the Earth orbits the Sun." (EN + HI), key "Similar temperature" kept; Q64 had NO misspelt word (all four
  correct) — option D "Unscrupulous" → "Unscrupilous" (the misspelling the key intends); Q68 "sentence ._____" → "sentence.||_____";
  Q72 and Q75 underlines restored; Q77 option "shal" → "shall"; Q76–80 one passage (Q76's copy), blanks ___A___/___B___/___C___ and
  "(D) <u>restriction</u>", "(E) <u>illustrates</u>". HI Part D: Q68 stem reworded to "सुरक्षा कर्मियों की ड्यूटी का समय, स्थान और कार्य
  तय करने वाली योजना क्या कहलाती है?" (प्रक्रिया also fitted the bare stem; key ड्यूटी प्लान); Q70 duplicate option D "खेल के लिए" →
  "यात्रा के लिए"; Q74 "<u>सही</u> … क्या होगी:" → plain "सही … क्या होगी?"; Q79 option C "आंतरिक" → "राष्ट्रीय" (BSF guards the
  borders, so "internal" was arguable; key C kept). Hindi Part D passage is Q75–Q79 (Q80 standalone). Carried verbatim: Q23 Nati
  "fast-paced, vigorous" (best fit), option casing in Q63/Q65, Q5 (LCM) and Q6 (SI) in Reasoning tagged quant.lcm-hcf /
  quant.simple-interest. 9 hindi.other (Q64–66, Q70–74, Q80); Q67–69 tagged hindi.anek-shabd.
- 30 Apr 2026 Shift 3 — built 2026-11-26 (figure Qs Q11, Q12 — stem + 4 options each, all clean, threshold 200, native size, no padding;
  Q11 option 3 is a TCS snip of a different size (105×128) but a clean letter figure — shipped as is). All 80 EN and 20 HI Part D keys
  agreed (en/hi cidx = gu cidx = source solution line). Corrections: Q7 option C was an image of the word "UNIFORM" — typed (EN + HI);
  Q33 stem "in February 2025" → "in November 2024" (EN) / "फरवरी 2025" → "नवंबर 2024" (HI) — K. Sanjay Murthy was named CAG on 18 Nov and
  sworn in on 21 Nov 2024; Q34 stem "The Manmohan Singh Committee (1991) is known for:" → "The economic reforms of 1991, launched under
  Finance Minister Manmohan Singh, are mainly known for:" (EN + HI; there is no such committee, key A kept); Q38 stem reworded to "According
  to a study published in 2024, about ___ … lack the diversity in diet suggested by the WHO" (EN + HI; it was a 2024 NMJI study, not a WHO
  suggestion; key 77% kept); Q63 bold word restored (<u>considerable</u>); Q65 EN option "Wretchedness" → "Wrechedness" (the HI/GU copies
  keep the misspelling the key intends; EN had all four correct); Q72 options "0n"/"ãI" → "on"/"at"; Q73 and Q75 underlines restored; Q74
  "C. … milk. D. They looked" split onto its own line; Q76–80 one passage (Q76's copy), blanks ___A___/___B___/___C___ and "(D) <u>vibrant</u>",
  "(E) <u>heritage</u>"; Q80 stem adds "as it is used in the passage" (inheritance is the legal sense). HI Part D: Q63 option D "ढांकना"
  (ढाँकना is an accepted variant) → "ढ़कना" so only the key A is correct; Q72 "<u>सही</u> … क्या होगी:" → plain "सही … क्या होगी?"; Q74 stem
  → "पुलिस विभाग के कार्य-नियमों की संकलित पुस्तक क्या कहलाती है?" (संहिता also fitted the bare stem; key नियमावली); Q75 stem → "अपराध होने पर
  पुलिस द्वारा अपराधियों के विरुद्ध उठाया गया कदम क्या कहलाता है?" (उपाय fitted the old "अपराध रोकने के लिए" stem better; key कार्रवाई); Q77
  zero-width space removed from option C; Q80 option "व्यापार बढाना" → "बढ़ाना"; passage "रहता है है कि" → "रहता है कि". Hindi Part D passage is
  Q76–Q80 (Q75 standalone). Carried verbatim: Q42 "(24 of 1)" / "(24 का 1)", Q39 "did … ultimately annexed", Q46 "One of the diagonal", option
  casing in Q63/Q65/Q67/Q68. 6 hindi.other (Q65, Q68–Q72).
- 04 May 2026 Shift 2 — built 2026-11-26 (figure Qs Q10, Q11 — stem + 4 options each, all clean, threshold 200, native size, no padding).
  All 80 EN and 20 HI Part D keys agreed (en/hi cidx = gu cidx on all 100). Source images typed as text: Q1 option D "PC" (EN + HI),
  Q69 option B "in". Corrections: Q35 stem "artificial intelligence action plan launched … in 2025" → "national artificial intelligence
  mission approved by the Union Cabinet in March 2024" (EN + HI; IndiaAI Mission was approved on 7 Mar 2024; key A kept); Q37 stem
  "provides" → "provided … until 2020" (EN + HI; MEIS was withdrawn from 1 Jan 2021); Q39 stem "fight with the British in Jhansi" →
  "Rani Lakshmi Bai of Jhansi fight against the British in 1857–58" (EN + HI; "with" was ambiguous); Q50 "5 times more than B" → "6 times B"
  (EN + HI; 80% fitted the other reading; key 83.33% kept); Q44 EN stem "0.63̅" → \( 0.6\overline{3} \) and EN options A/D "0.64"/"0.69" →
  recurring \( 0.6\overline{4} \) / \( 0.6\overline{9} \) as in the HI paper; Q47 EN option "4:3" padded and KaTeX-wrapped like the other
  three; Q61 missing blank inserted ("leave his friend to _____."); Q65 EN option "Valedictory" → "Validictory" (the HI/GU copies keep the
  misspelling the key intends; EN had all four correct); Q70 stem "stiches" → "stitches"; Q73 and Q75 underlines restored; Q76–80 passage
  blanks rebuilt as ___A___ … ___E___ (all five copies identical). HI Part D: Q64 option A "बीबी" (an accepted variant of बीवी) → "बीवि" so only
  the key B is correct; Q66/Q67 stray space in 'अस्वस्थ ' / 'आजाद '; Q72 "होगाः" → "होगी?"; Q74 stem "किसी क्षेत्र की स्थिति का निरीक्षण
  करना क्या कहलाता है?" (gave away the key) → "पुलिस अधिकारी द्वारा किसी थाने, चौकी या क्षेत्र की व्यवस्था को मौके पर जाकर जाँचना-परखना क्या
  कहलाता है?" (key निरीक्षण). Hindi Part D passage is Q76–Q80 (Q75 standalone). Carried verbatim: Q42 "(28 of 2)", Q46/Q47 "One of the
  diagonal", Q57 "A car cover", Q62 option "The lightening open", Q64 option "complain", Q33 key Visvesvaraya, HI Q5 masculine verbs for
  girls, HI Q70 option "आपरेशन". 4 hindi.other (Q65, Q70–Q72).
- 04 May 2026 Shift 3 — built 2026-11-26 (figure Qs Q12, Q13 — stem + 4 options each, all clean, threshold 200, native size, no padding).
  All 80 EN and 20 HI Part D keys agreed (en/hi cidx = gu cidx = source solution line on all 100). Corrections: Q29 stem "St. Paul's
  Cathedral" → "St. Paul's Cathedral, Kolkata" (EN) / "कोलकाता के सेंट पॉल्स कैथेड्रल" (HI) — Burne-Jones's west window is in Kolkata, not
  London; Q40 stem "In 2025, IMF in its World Economic Outlook" → "In July 2025, IMF in its World Economic Outlook Update" (EN + HI; April
  2025 said 6.2%, July 6.4%; key 6.4% kept); Q63 '"Fortunate" ?' → '"Fortunate"?'; Q64 had NO misspelt word (all four correct) — EN option A
  "Treacherous" → "Treachearous" (the HI/GU copies keep the misspelling the key intends); Q68 missing blank inserted ("_____ hearing the
  news"); Q72 and Q75 underlines restored; Q73 "storm. C. Entering" split onto its own line; Q76–80 one passage, blanks ___A___/___B___/___C___
  and "(D) <u>pacing</u>", "(E) <u>examined</u>", stray " ," removed; Q78 options "nm"/"ner" → "him"/"her" (EN + HI copy). HI Part D: Q63
  option A "कोशी" (Nepal's official spelling, an accepted variant) → "कौसी" so only the key B कोसी is correct; Q66 option D "अभियोग गठन" (also
  meant charge framing) → "अभियोग वापसी" (key B आरोप निर्धारण); Q67 stray space in 'कार्य '; Q68 stem "जब किसी कर्मी की ड्यूटी बदल दी जाती है"
  → "जब किसी कर्मी को उसके कार्यस्थल या पद से हटाकर दूसरे स्थान पर भेज दिया जाता है" (प्रमोशन also changes duty; key स्थानांतरण); Q74
  "<u>सही</u> … क्या होगी:" → plain "सही … क्या होगी?"; Q79 option B "आंतरिक सुरक्षा" → "राष्ट्रीय सुरक्षा" (border security is not internal;
  key B kept); Q80 option D "सीलिंग" (sealing IS a way to protect a scene) → "सजावट" (key B सुरक्षा). Hindi Part D passage is Q75–Q79 (Q80
  standalone). Carried verbatim: Q42 "(28 of 1)" (EN + HI), Q45/Q46 "One of the diagonal", Q57 "two number", Q66 option "sore" and Q68 option
  casing, Q70 key "Take the injured man…" (imperative active), Q73 "something alarming, her suitcase" comma splice. Q5 and Q6 sit in Reasoning
  but are tagged quant.number-system / quant.average. 8 hindi.other (Q64–66, Q69, Q71–74).
- 05 May 2026 Shift 1 — built 2026-11-26 (NO figure questions, so no figures.docx; zero figures confirmed three ways: no <img> in
  en[0..79] text/opts/comp or hi[0..99], no [FIGURE-BASED], keyword sweep). All 80 EN and 20 HI Part D keys agreed (en/hi cidx = gu cidx
  on all 100). Corrections: Q2 option A "N" was truncated in the source (EN + HI) — rebuilt as "NY" (does not fit; key C NX kept); Q22
  option A "Dhol, Harmonium, and Manjira" → "Dhol and Tirududi (jingle sticks)" (EN) / "ढोल और तिरुडुडी (घुँघरू वाली छड़ियाँ)" (HI) —
  harmonium and manjira are not the Gaur Maria accompaniment; key A kept; Q33 stem "Fred Darrington Award for Excellence in Art and
  Culture" → "Fred Darrington Sand Master Award" (EN + HI; the real name, Weymouth UK, April 2025; key A kept); Q34 stem adds "the
  longest river of peninsular India" (EN + HI; the Cauvery is also called Dakshin Ganga in some books; key Godavari kept); Q63
  options C and D were both "Exaggerate" (GU too) — C → "Exagerate" so only the key D is correct; Q66 option "Professiona" →
  "Professional"; Q7/Q40 statement II moved to its own line; Q68 "following. Something" → "following.||Something"; Q73/Q74
  jumbled sentences split onto their own lines; Q75 underline restored (<u>from the flea market with a gilded frame</u>); Q43/Q45/
  Q46/Q53–Q57 KaTeX rebuilt (EN plain "2 : 1", "(7/5)", "12\(\sqrt{3}\)" made like the HI paper); HI Q16 note "1 and 3" →
  "1 और 3"; HI Q51 option D 4900 → 4850 (as in EN/GU). HI Part D: Q67 stem → "…अच्छे कार्य के लिए प्रशंसा-पत्र या पदक दिया जाता है…"
  (key पुरस्कार); Q72 option B "गवाह से दोबारा पूछताछ" (sounded like re-examination) → "गवाह से विरोधी पक्ष द्वारा पूछताछ (जिरह)"
  (key B kept); Q73 stem → "अपराध होते समय घटनास्थल पर मौजूद रहकर घटना को अपनी आँखों से देखने वाले व्यक्ति…" (आरोपी/संदिग्ध also
  fitted "मौजूद व्यक्ति"; key साक्षी); Q74 stem "…किया गया कार्य…" → "किसी मामले में पुलिस द्वारा कानून के अनुसार उठाया गया कदम…"
  (option कार्य fitted the old stem; key कार्रवाई); Q75 stem "अतिरिक्त सुरक्षा लगाना" → "शांति बनाए रखने के लिए पुलिस बल की तैनाती और
  ज़रूरी प्रबंध करना" (सुरक्षा विस्तार also fitted; key सुरक्षा व्यवस्था); passage "विश्वास विश्वास" → "विश्वास"; Q77 option "शिक्षा
  शिक्षा का" → "शिक्षा का". Hindi Part D passage is Q76–Q80 (Q75 standalone). English Q76–80 is a reading-comprehension passage
  (not a cloze), tagged eng.reading-comprehension. Carried verbatim: Q5/Q6 hypothetical calendar data, Q42 "(33 of 2)", Q60 "fourth
  proportion", Q56 "two number", option casing in Q66/Q67/Q72, Q58/Q59 "Rs." in options, HI Q61–Q63 underlined अशुद्ध/शुद्ध. Q12
  (heads and legs) sits in Reasoning but is tagged quant.algebra. 9 hindi.other (Q64–Q72).
- 05 May 2026 Shift 2 — built 2026-11-26 (figure Qs Q12, Q13, Q20 — stem + 4 options each, all clean, threshold 200, native size, no padding;
  first shift with three figure questions). All 80 EN and 20 HI Part D keys agreed with my own solving (en/hi cidx = gu cidx on all 100).
  KEY NOTE: HI Part D Q64 — Testbook's solution text names कमज़ोर (A) but en/hi/gu cidx all say B कमजोर; both spellings are standard, so
  option A was made a misspelling and key B carried. Corrections: Q2 stem "GT : JY" → "GT : IY" (EN + HI; J is +3 while FR : HW is +2, +5,
  so no single rule gave the key KS); Q16 nonce words "Disgarge"/"Disguse" → "Disgorge"/"Disguise" (EN + HI; order and key 12345 unchanged);
  Q40 stem "In 2025, IMF in its World Economic Outlook" → "In July 2025, IMF in its World Economic Outlook Update" (EN + HI; April 2025 said
  6.3% for 2026, July 6.4%; key kept); Q61 missing blank inserted ("Rahul _____ on the Army…") and option "threw in the towe" → "towel"; Q63
  option C "Raucous" (also correctly spelt) → "Raucus"; Q64 bold word restored (<u>agony</u>); Q66 "Concea" → "Conceal"; Q71 and Q75
  underlines restored; Q73 "warren. D. One little boy" split onto its own line; Q76–80 one cloze passage, blanks ___A___/___B___/___C___ and
  "(D) <u>reminisce</u>", "(E) <u>evolves</u>"; Q80 option B "Grows" (evolve = develop/grow) → "Slows"; Q43/Q44/Q46/Q49/Q55/Q58/Q59 KaTeX
  rebuilt (EN plain "4/7", "2^{5} x 3^{2}", "4:7" made like the HI paper, all four Q46 ratios padded and wrapped); HI Q33 options B–D were
  English → "18 से 60 वर्ष" etc.; HI Q42 "22 x 2" → "22 × 2". HI Part D: Q62 option B "व्यक्ति" (a correct word) → "वयक्तिक"; Q63 options C
  "मसजिद" (older accepted variant) → "मसजीद" and D "मस्जिदों" (correct plural) → "मस्जीद"; Q64 option A "कमज़ोर" → "कमजौर"; Q70 option D
  "अग्रेषण" (forwarding also fitted "भेजी जाती है") → "आदेश"; Q71 option D "सील ज़ोन" (also a sealed-off area) → "पार्किंग ज़ोन"; Q75
  "<u>सही</u> … क्या होगी:" → plain "सही … क्या होगी?". Hindi Part D passage is Q76–Q80 (Q75 standalone). Carried verbatim: Q21 option
  "Panj Piaras", Q36 "chieftains", Q46/Q47 "One of the diagonal", Q52 "is Rs. 6000 and Rs. 8000", Q56 "employed in a work", Q73 "parent’s",
  Q75 option casing ("she made …"), Q80 option "Repeat", HI Q56 "A और B … लगाया गया है". 6 hindi.other (Q65–Q67, Q73–Q75); Q69–Q72 tagged
  hindi.anek-shabd.

- 05 May 2026 Shift 3 — built 2026-11-26 (figure Qs Q11, Q12, Q18, Q19 — stem + 4 options each, all clean, threshold 200, native size, no
  padding; first shift with four figure questions). All 80 EN and 20 HI Part D keys agreed with my own solving (en/hi cidx = gu cidx on all
  100). Source images typed as text: Q2 options A "J" and C "H" (EN + HI). Corrections: Q2 option B "∈" → "E" (EN + HI; key G kept); Q4 "? ,"
  → "?,"; Q40 stem "What position will it naturally attain?" → "In which position will the plane of the loop naturally settle with respect to
  the field lines?" (EN) / "क्षेत्र रेखाओं के सापेक्ष लूप का तल स्वाभाविक रूप से किस स्थिति में आ जाएगा?" (HI) — key "Perpendicular" is true of the
  plane, not of the loop's axis; Q63 four underlines restored and option D "melodies" → "meloudies" (the misspelt word as it stands in the
  sentence); Q64 EN option "silhouette" → "silouette" (the HI/GU copies keep the misspelling the key intends; EN had all four correct); Q71
  option "ower" → "over"; Q74 underline restored; Q75 had NO error after Testbook's clean-up — "for hours" → "for hour" in stem and option C
  (the error Testbook's own solution describes; key C kept); Q78 "harmfu" → "harmful"; RC passage "osteoporosis a condition" →
  "osteoporosis—a condition" (as quoted in Q79); B1 wraps Q3/Q5/Q13/Q14/Q15/Q20/Q54; Q43/Q44/Q45/Q48/Q50 KaTeX rebuilt (\frac → \dfrac,
  EN "x" → \times, split \sqrt spans joined); HI Q57 "5 गुना अधिक कुशल" / "3 गुना अधिक कुशल" → "5 गुना कुशल" / "3 गुना कुशल" (as in EN "5 times as
  efficient"). HI Part D: Q62 option A "गोलियों की बाढ़" (बाढ़ = a volley of fire, also correct) → "गोलियों के बौछार"; Q63 option C "कई बैंक
  कर्मचारियों ने प्रदर्शन किया" (also a correct sentence) → "बैंक के कई कर्मचारियों ने प्रदर्शन किए"; Q64 "कौन -सा" → "कौन-सा" and "<u>सही</u>" →
  plain "सही"; Q65 stem → "…उसके वर्तमान कार्यस्थल से हटाकर दूसरे स्थान पर नियुक्त कर दिया जाता है…" (तैनाती also fitted "भेजा जाता है"; key
  स्थानांतरण); Q68 stem "प्रशिक्षण देने की प्रक्रिया" (gave away the key) → "उनके काम के लिए आवश्यक कौशल, अभ्यास और जानकारी देने की प्रक्रिया" (key
  प्रशिक्षण); Q69 stem "समय पर ड्यूटी पर नहीं आता" (= late, not absent) → "अपनी निर्धारित ड्यूटी पर आता ही नहीं" (key अनुपस्थित). Hindi Part D
  passage is Q76–Q80. Carried verbatim: Q7 hypothetical day (21 Sep 2024 was really a Saturday), Q24 "Adhvarya", Q27 stem (3600/4000 is a
  distractor; key 1.1 times = 1 ÷ 0.9), Q55 "employee are matriculates", Q60 "Rs." in options, Q76 option "Was", HI Q61–Q63 underlined शुद्ध,
  HI Q72 अभियोजन दोष (the only prosecution-specific term). Q20 (ages) sits in Reasoning but is tagged quant.ages. 10 hindi.other (Q64, Q65,
  Q68–Q75).

- 06 May 2026 Shift 1 — built 2026-11-26 (figure Qs Q9, Q10 — stem + 4 options each, all clean, threshold 200, native size, no padding).
  All 80 EN and 20 HI Part D keys agreed with my own solving (en/hi cidx = gu cidx on all 100; Testbook's solution line for Q4 says
  "Option 3" but BF is option 2 and all three keys say B — carried B). Corrections: Q46 stem \( \sqrt{108900 + \sqrt{12321}} \) (= 330.17,
  no option fits) → \( \sqrt{\sqrt{108900} + \sqrt{12321}} \) = √441 = 21 (EN + HI; key A kept); Q26 stem "largest contributor to urban
  PM2.5 in India" → "According to source-apportionment studies of Delhi's air, … the largest overall contributor to PM2.5" (EN + HI;
  nationally the answer varies by study and city; CEEW's comparison of Delhi studies puts transport first; key C vehicle exhaust kept);
  Q33 statement II "Other Backward Caste" → "Other Backward Classes" (EN; HI already अन्य पिछड़ा वर्ग); Q8 option D "s" → "S" (as in HI);
  Q18 missing comma "UQL162 WUR243" → "UQL162, WUR243" (EN + HI); Q39/Q51 statement II moved to its own line (EN + HI); Q4/Q5 series
  split with ||; B1 wraps Q11–Q14, Q52, Q54, Q55; Q44/Q45/Q48 KaTeX rebuilt (\frac → \dfrac, "....." → \ldots), Q45/Q58 options and Q57
  "1/5" as \dfrac, Q55 option "7:13" padded and wrapped; Q63 had TWO correctly spelt words (Sanguine and spurious) — option D "spurious" →
  "spurrious" so only the key B is correct; Q66 option D "Āō" (garbage in EN/HI/GU) → "Aid" (a synonym; key impede kept); Q70 option A
  "Each wal" → "Each wall"; Q72 and Q75 underlines restored; RC passage instruction line dropped. HI Part D: Q72 "क्या होगा:" → "क्या होगी?";
  Q74 option D "नज़र के अंतर्गत बंद करना" (also describes custody) → "ज़मानत पर रिहा करना" (key C किसी को निगरानी में रखना). Hindi Part D passage is
  Q76–Q80 (Q75 standalone); Q61–Q63 are karak-error items (all key A कारक, as in the source). Carried verbatim: Q42 "18 of 1" / "18 का 1",
  Q47 "is build", Q50 "join", Q58 "A and B both the left", Q33 "is a target groups", Q64 option casing, Q77 key "these pathogens" (best
  fit), HI Q72 option "non governmental organization". 10 hindi.other (Q64–Q66, Q69–Q75); Q67/Q68 tagged hindi.shabd-bhed.

- 06 May 2026 Shift 2 — built 2026-11-26 (figure Qs Q11, Q12, Q18, Q19 — stem + 4 options each, all clean, threshold 200, native size, no padding;
  Q12 option 2 is a smaller TCS snip (80×74) but a clean figure — shipped as is). All 80 EN and 20 HI Part D keys agreed with my own solving
  except Q32 (en/hi/gu cidx all D). Source images typed as text: Q2 option A "I", Q3 option D "NN" (EN + HI). KEY: Q32 (theme states of the
  38th Surajkund International Crafts Mela 2025) — official key D "Punjab and Haryana" is wrong; the theme states were Odisha and Madhya
  Pradesh (then option B). Per the standing rule the key letter D was kept and the options rewritten: D → "Madhya Pradesh and Odisha",
  B → "Uttar Pradesh and Meghalaya" (the 2026 theme states) (EN + HI). Corrections: Q25 stem "0.5°" → "0.524°" (EN + HI; 0.5° gives
  3316 km, no option; 0.524° gives the keyed 3475 km) and "3.8×10^{8}" KaTeX-wrapped; Q28 stem "Which was the first Asian country" → "Which
  were the first Asian countries" (EN) / "पहले एशियाई देश कौन-से थे" (HI) — key "South Korea, Japan"; Q63 option B "inconsistent" →
  "inconsistant" (the misspelt word as it stands in the sentence); Q72 sentence C "He said in the car" → "He sat in the car"; HI Q37
  option C "राष्ट्रीय स्वास्थ्य नीति 2010" → "राष्ट्रीय फिटनेस नीति 2010" (as in EN); HI Q57 "2/1.5 गुना अधिक कार्यकुशल" → "2/1.5 गुना कार्यकुशल"
  (as in EN "times as efficient"); B1 wraps Q3/Q5/Q13/Q14/Q15 and Q20 options; Q43/Q44/Q45/Q47/Q50 KaTeX rebuilt (\frac → \dfrac, sup → ^{}).
  HI Part D: Q61 "दिए गये … <u>अशुद्धि</u> है:" → "दिए गए … अशुद्धि है?"; Q63 option B "पुनरुक्ति-संबंधी" (also describes "गुप्त रहस्य")
  → "लिंग-संबंधी" (key C अधिकपदत्व); Q70 duplicate option D "मीडिया को" → "आम जनता को"; Q72 stem "…मानसिक तैयारी में था…" (mere intent is not an
  attempt) → "जब कोई आरोपी अपराध करने के इरादे से उसकी ओर कदम उठा लेता है, पर अपराध पूरा नहीं होता, तो कानूनी भाषा में यह क्या कहलाता है?"
  (key प्रयास अपराध); Q80 option A "चेतावनी सूचना" (repeated the stem) → "सम्मन" (key अलर्ट). Hindi Part D passage is Q74–Q78 (Q79, Q80
  standalone); English Q76–80 is a reading-comprehension passage with no instruction line. Carried verbatim: Q31 option "Shubhman Gill",
  Q47 options B and D equal in value (15√15/50 = 3√15/10, both wrong), Q61 option "the sweets is made", option casing in Q62/Q68, HI Q62/Q63
  underlined शुद्ध/अशुद्धि. Q20 (ages) sits in Reasoning but is tagged quant.ages. 10 hindi.other (Q64–66, Q69–73, Q79, Q80).

- 06 May 2026 Shift 3 — built 2026-11-26 (figure Qs Q9, Q10 — stem + 4 options each, all clean, threshold 200, native size, no padding).
  All 80 EN and 20 HI Part D keys agreed with my own solving (en/hi cidx = gu cidx = source solution line on all 100). Source image typed as
  text: Q71 option A "in". HI PART D PASSAGE: the source has NO passage for HI Q76–Q80 (comp empty in all three languages; the five items
  only make sense with one) — our own passage written (community awareness → change in thinking → personal responsibility → durable,
  participation-based security) so every official key C/C/D/C/A is the only right answer; listed in the delivery report. Corrections:
  Q16 option C "TFIX T" → "TFIXT" (EN + HI); Q40 stem "The QUAD leader's summit-2025 will be held in ____." → "Which country was chosen to
  host the Quad Leaders' Summit due in 2025?" (EN) / "2025 में होने वाले क्वाड (QUAD) नेताओं के शिखर सम्मेलन की मेजबानी के लिए किस देश को चुना
  गया था?" (HI) — India was the host but no leaders' summit was held in 2025; key India kept; Q63 EN option A "Incipient" → "Incepient" (the
  HI/GU copies keep the misspelling the key intends; EN had two correct spellings); Q65 option D "Laure" → "Laurel"; Q66 option A
  "Additiona" → "Additional"; Q76–80 passage instruction line dropped and "'eminent'" → "'immanent'" (Husserl's term); B1 wraps Q11–Q14
  and Q55 options; Q41/Q44/Q46 KaTeX rebuilt, Q45 "\rm" removed, Q53/Q56/Q58 stem and Q57 option fractions → \dfrac; HI Q39 option
  "सब्सिडी (सब्सिडी)" → "सब्सिडी". HI Part D: Q61/Q63 "<u>अशुद्धि</u> है:" → "अशुद्धि है?" ("गये" → "गए"); Q62 restructured to "नीचे दिए गए
  वाक्य में कौन-सी अशुद्धि है?||इस विषय पर एक भी अच्छी पुस्तकें नहीं है।"; Q64/Q72 "<u>सही</u> … :" → plain "सही … ?" ("क्या होगा" → "क्या
  होगी"); Q65 stem → "वर्दी में ड्यूटी करने का आदेश होने पर भी जब कोई सुरक्षा कर्मी बिना वर्दी के ड्यूटी पर आता है, तो यह क्या है?" (गुप्त ड्यूटी
  fitted the bare stem; key अनुशासनहीनता); Q70 option B completed ("… नियंत्रण हो"); Q71 option D "परिवहन की निगरानी हेतु" (also a use of
  surveillance) → "वाहनों की मरम्मत हेतु" (key C). Carried verbatim: Q42 "42 of 1" / "42 का 1", Q48 "is build", Q50 "One of the diagonal",
  Q52 "is to tiled", Q47 "number is", Q54 options "Rs.1680"/"Rs. 1620", option casing in Q64/Q66/Q67. Q67/Q68 (तत्सम) tagged hindi.shabd-bhed.
  10 hindi.other (Q64–66, Q69–75).

- 07 May 2026 Shift 1 — built 2026-11-26 (figure Qs Q11, Q12, Q18, Q19 — stem + 4 options each, all clean, threshold 200, native size, no padding).
  All 80 EN and 20 HI Part D keys agreed with my own solving (en/hi cidx = gu cidx on all 100). Source image typed as text: Q66 option C
  "see". Corrections: Q35 stem "Launched in July 2025" → "Approved by the Union Cabinet in July 2025" (EN) / "जुलाई 2025 में शुरू की गई" →
  "जुलाई 2025 में केंद्रीय मंत्रिमंडल द्वारा स्वीकृत" (HI) — Cabinet approval was 16 Jul 2025, the PM launched it on 11 Oct 2025; key 6 kept;
  Q37 stem "December 2024" → "September 2024" (EN) / "दिसंबर" → "सितंबर" (HI) — Paryatan Mitra & Paryatan Didi was launched on World Tourism
  Day, 27 Sep 2024 (2 Dec 2024 was only a Lok Sabha reply); Q31 option D "D. Gukesh" (the same person as option A "Gukesh") → "R. Praggnanandhaa"
  (EN) / "आर. प्रज्ञानानंद (R. Praggnanandhaa)" (HI), key B Harikrishnan A Ra kept; Q40 statement II moved to its own line (EN + HI); Q48 EN
  option "480 x 530" → "480 × 530" (as in HI) and stem KaTeX-wrapped; Q43/Q44/Q45/Q47 KaTeX rebuilt (\frac → \dfrac), Q56 "2/3", "1/4" → \dfrac;
  B1 wraps Q2/Q3/Q13/Q14/Q15/Q20 stems and Q20/Q60 options; Q68 option "Uρ" (Greek rho) → "Up"; Q71 missing blank inserted ("experimenting
  _______ new types") and option "oy" → "of" ("on" would be arguable; key "with" kept); HI Q17 "दोपहर 1 AM" → "1 AM". HI Part D: Q61/Q62
  "दिए गये … <u>अशुद्धि</u> है:" → "दिए गए … अशुद्धि है?"; Q63 "<u>अशुद्ध</u> रूप … :" → "निम्नलिखित में से वाक्य के अशुद्ध रूप का चयन कीजिए।";
  Q65 stem "…तो वह क्या होता है?" → "…तो वह अपने अधिकारी को लिखित रूप में क्या देता है?" (key प्रार्थना पत्र); Q68 stem → "सुरक्षा कर्मियों की रोज़ की
  ड्यूटी का समय और पाली किस दस्तावेज़ में दर्ज की जाती है?" (तैनाती पत्र also fitted "समय निर्धारण"; key ड्यूटी चार्ट); Q71 option D stray "में"
  removed; Q72 option B "प्रमाणिकता परीक्षण" (also means checking validity) → "साक्ष्य संकलन" (key C साक्ष्य सत्यापन). English Q76–80 is a reading-
  comprehension passage (no instruction line); Hindi Part D passage is Q76–Q80 (Q75 standalone). Carried verbatim: Q27 "duration … including
  breaks, in terms of innings", Q41 "(18 of 2)" / "(18 का 2)", Q58 "a another train", Q53/Q54 "Rs.", Q62/Q65 option casing, Q31 option A
  "Gukesh". Q20 (ages) sits in Reasoning but is tagged quant.ages; Q66 (sea/see/scene) tagged eng.homonyms. 10 hindi.other (Q64, Q65, Q68–Q75).

- 07 May 2026 Shift 2 — built 2026-11-26 (figure Qs Q9, Q10 — stem + 4 options each, all clean, threshold 200, native size, no padding).
  All 80 EN and 20 HI Part D keys agreed with my own solving (en/hi cidx = gu cidx on all 100). Source image typed as text: Q3 option A
  "HI" (EN + HI). HI PART D PASSAGE: the source has NO passage for HI Q76–Q80 (comp empty in all three languages) — our own passage written
  (data from many sources → comparative study for analysis and identification → patterns of suspicious activity → strategy made in advance,
  not mere reaction → data as a strategic resource → pre-planning-based security thinking) so every official key A/B/C/D/A is the only right
  answer. Corrections: Q32 stem "Which act gave representation to Indians in the Central Legislative Assembly for the first time?" →
  "Which act, for the first time, provided for the election of Indian members to the Imperial (Central) Legislative Council and introduced
  separate electorates for Muslims?" (EN + HI) — the Central Legislative Assembly was created only by the GoI Act 1919, so the old stem
  fitted option D; key C 1909 kept; Q64 option "Carefu" → "Careful"; Q71 option "ïn" → "in"; Q37 statement II moved to its own line
  (EN + HI); RC passage instruction line dropped; B1 wraps Q11–Q14; Q44/Q45/Q46/Q48 stems rebuilt as KaTeX (\frac → \dfrac, ^2 → ^{2},
  × → \times), Q56 "45/20" and Q57 "1/4", "1/2" → \dfrac, Q51 option "A/3" → \dfrac{A}{3}; HI Q58 "8/5 गुना अधिक कार्यकुशल" → "8/5 गुना
  कार्यकुशल" (as in EN "times as efficient"). HI Part D: Q61 "चिन्ह" → "चिह्न" (twice); Q62/Q63 restructured to "नीचे दिए गए वाक्य में कौन-सी
  अशुद्धि है?||<sentence>।"; Q65 stem → "…अचानक आए किसी निजी काम के लिए एक-दो दिन की छुट्टी…" (विश्राम fitted "एक दिन की छुट्टी"; key
  आकस्मिक अवकाश); Q69 stem → "किसी संज्ञेय अपराध की सूचना मिलने पर पुलिस थाने में सबसे पहले दर्ज की जाने वाली आधिकारिक सूचना…" (option
  रिपोर्ट fitted "आधिकारिक रिपोर्ट"; key प्राथमिकी); Q72 "<u>सही</u> … क्या होगा:" → plain "सही … क्या होगी?". Carried verbatim: Q22 "union
  territory has", Q37 "religious group … Christian", Q54/Q55 "Rs." in options, Q66 option "ordinary" (lower case), Q67 option "Tetratlon",
  Q70 error segment, Q76–80 passage "need poor segment to participate", HI Q63 "रखियेगा", HI Q75 "का हिंदी में अर्थ". Q61 (कोष्ठक चिह्न)
  tagged hindi.vyakaran; Q67/Q68 (तत्सम/तद्भव) tagged hindi.shabd-bhed. 10 hindi.other (Q64–Q66, Q69–Q75).

- 07 May 2026 Shift 3 — built 2026-11-26 (figure Qs Q11, Q12, Q18, Q19 — stem + 4 options each, all clean, threshold 200, native size, no padding).
  en/hi/gu cidx agree on all 100. My own solving disagreed with TWO official keys — both fixed through the option texts, key letters kept:
  Q32 (National Cooperation Policy 2025 unveiled on 24 Jul 2025; official key A was "January") → options A/B swapped to A "July", B "January"
  (EN + HI); Q72 (Baldwin's "Thirty More Famous Stories Retold" has the order C-A-D-B; official key D was "CBAD") → options C/D swapped to
  C "CBAD", D "CADB". Source images typed as text: Q2 A/C/D "L"/"M"/"H", Q4 C "MZ", Q5 A "UW" (EN + HI), Q66 D "laud". Corrections: Q20 stem
  "The sum of their ages is 57.6 years ago from now, what was …" → "The sum of their ages is 57 years. What was the ratio … 6 years ago?"
  (HI "योग 57 है" → "57 वर्ष है"); Q63 option C "discrimination" (spelt correctly) → "discrmination", the underlined misspelling the key intends;
  B1 wraps Q3/Q4/Q13/Q14/Q15/Q20 stems and Q20/Q59/Q60 options; Q23 options "7.6 × 10^{6} s" → KaTeX; Q44/Q45/Q47/Q50 stems and Q48 (\frac →
  \dfrac, x² + y² wrapped) rebuilt; HI Q35 "घोषित घोषणा" → "की गई घोषणा", HI Q39 option "शार्ंगदेव" → "शारंगदेव", HI Q40 "सबसे सर्वोत्तम" → "सर्वोत्तम".
  HI Part D: Q61/Q62 "दिए गये … अशुद्धि है-/:" → "दिए गए … अशुद्धि है?"; Q61 option C "क्रिया" (the verb ले लो also changes) → "कारक" (key सर्वनाम);
  Q63 option A "युवा अवस्था" → "युवावस्था" and stem "निम्नलिखित में वाक्य … कीजिए:" → "निम्नलिखित में से वाक्य … कीजिए।" (यौवन + अवस्था is
  redundant; key A); Q67 stem → "पुलिस और सशस्त्र बलों में वरिष्ठ अधिकारी द्वारा जवानों की शिकायतें और समस्याएँ सीधे सुनकर … बैठक" (सभा fitted
  the bare stem; key दरबार); Q68 stem "कार्य के मूल्यांकन को क्या कहते हैं?" (gave the key away) → "किसी कर्मचारी के कार्य की गुणवत्ता और प्रदर्शन को
  परखकर उसका स्तर आँकने की प्रक्रिया …" (key मूल्यांकन); Q69 option B "पहचान" (a badge also identifies) → "उपस्थिति" (key रैंक और पद); Q72 option A
  "अपराध पूर्व अभ्यास" (a literal gloss of the stem) → "अपराध पश्चात विश्लेषण" (key ड्राई रन); Q73 "है ?" → "है?". English Q76–80 is a reading-
  comprehension passage (no instruction line); Hindi Part D passage is Q76–Q80 (Q75 standalone). Carried verbatim: Q61 option "the le monde",
  Q62/Q65/Q78 option casing, Q75 "with one foot limping", Q60 "Rs. X", Q24 key Jupiter ("stormy planet"), HI Q28 "नरेंद्र सिंह कपानी".
  Q20 (ages) sits in Reasoning but is tagged quant.ages; Q66 (lord/lured/load/laud) tagged eng.homonyms; Q65/Q66/Q73 tagged hindi.paryayvachi.
  9 hindi.other (Q64, Q67–Q72, Q74, Q75).

- 08 May 2026 Shift 1 — built 2026-11-26 (figure Qs Q9, Q10 — stem + 4 options each, all clean, threshold 200, native size, no padding).
  en/hi/gu cidx agree on all 100, and all 80 EN and 20 HI Part D keys agreed with my own solving. KEY NOTE: Q71 ("affectionate ____ all our
  family members") — cidx B "with" in all three languages, but Testbook's solution line says "to"; "affectionate to/towards" is also standard
  usage, so option C "to" → "at" and key B carried. Corrections: Q17 option "0X414" (zero) → "OX414" (EN + HI, as in the stem); Q22 EN option
  "Vijayakalakshmi Pandit" → "Vijaya Lakshmi Pandit" (HI already विजया लक्ष्मी पंडित); Q34 stem "5th Marine Census in the "Coastal state fisheries
  conference 2025"" → "5th Marine Fisheries Census at the "Coastal States Fisheries Meet 2025"" (EN) / "समुद्री जनगणना" → "समुद्री मत्स्य जनगणना" (HI)
  — Mumbai, 28 Apr 2025, key kept; Q63 (correctly spelt) had THREE correct words — EN "Gregarious"/"Gluttony" → "Gregarous"/"Glutony" (the HI/GU
  copies keep the misspellings the key intends; key D Gaffe); Q49 options normalised to "P − 14" etc.; Q76–80 RC passage instruction line dropped,
  "higher- income" → "higher-income"; B1 wraps Q11–Q14 and Q47 options; Q44/Q45/Q46/Q50 stems rebuilt as KaTeX (\frac → \dfrac, \rm removed,
  "......" → \ldots), Q57 "2/3" and Q60 options → \dfrac; HI Q57 "4 गुना अधिक कार्यकुशल" → "4 गुना कार्यकुशल" (as in EN "4 times as efficient").
  HI Part D: Q61–Q63 "चिन्ह" → "चिह्न" and "है-[BR]" → "है?||"; Q62 option C "पूर्ण विराम" (the sentence "हाँ, लिख सकता हूँ।" also ends with one)
  → "विस्मयादिबोधक चिह्न" (key A अल्पविराम); Q64 "का सही तकनीकी शब्द है:" → "का सही तकनीकी (अंग्रेज़ी) शब्द क्या है?"; Q65 stem "किसी महत्वपूर्ण सूचना
  को दीवार पर लगाने के लिए क्या उपयोग किया जाता है?" (पोस्टर also fitted) → "कार्यालय या थाने में … दीवार पर स्थायी रूप से लगाया गया बोर्ड क्या कहलाता
  है?" (key सूचना पट्ट); Q69 option B "जप्ती" → "जब्ती"; Q72 "क्या होगा:" → "क्या होगी?"; Q79 option D "केंद्रकृत" → "केंद्रीकृत". Hindi Part D passage
  is Q75–Q79 (Q80 standalone); English Q76–80 is a reading-comprehension passage. Carried verbatim: Q32 option "Council of Minister", Q33 option
  "Paris New Year", Q38 option "vladivostok", Q42 "(28 of 2)" / "(28 का 2)", Q47 "length 5 cm" shorter than the breadth, Q54 "Rs." in options,
  Q67 option "chiropodist" (lower case), Q80 option C repeating Q79's option C. 7 hindi.other (Q64, Q68–Q72, Q80); Q73/Q74 (meaning) tagged
  hindi.paryayvachi, Q61–Q63 (विराम चिह्न) hindi.vyakaran, Q65 hindi.anek-shabd.
- 08 May 2026 Shift 2 — built 2026-11-26 (figure Qs Q11, Q12, Q18, Q19 — stem + 4 options each, all clean, threshold 200, native size, no padding).
  en/hi/gu cidx agree on all 100, and all 80 EN and 20 HI Part D keys agreed with my own solving. Source image typed: Q3 option C "FA" (EN + HI).
  Corrections: Q2 stem "ABQ : CDS : ? : RJK : RMN : TOP" (single colons) → "ABQ : CDS :: ? : RJK :: RMN : TOP" (EN + HI, the form the stem
  describes; key PHI kept); Q28 stem "launched in 2025" → "launched by the Ministry of Ayush in 2021" (EN) / "2025 में शुरू की गई" → "आयुष मंत्रालय
  द्वारा 2021 में शुरू की गई" (HI) — AOGUSY was approved in March 2021, key C kept; Q47 stem exponent 1/2 → 2 (EN + HI; (√320)^(1/2) ≈ 4.23
  matched no option, key 320 needs the square); Q43/Q44/Q47/Q49 stems rebuilt as KaTeX (\frac → \dfrac), Q45 "x^{2}" put inside KaTeX and \rm
  removed, Q49 options normalised to \( 4\sqrt{3} \) etc.; B1 wraps Q2, Q4, Q13–Q15 stems and Q20 stem + options; Q61 option D "mmigrated here" →
  "immigrated here"; Q62 option A "resilience" → "resillience" (the underlined misspelling the key intends — the option showed the correct
  spelling); Q70 option A "The quest" → "The guest" (as in the sentence). HI Part D: Q61 sentence "मैंने नहीं जाना।" (also a correct past tense of
  जानना) → "मैंने घर जाना है।" and "है-" → "है?" (key सर्वनाम); Q62 "आप आपका काम करो।" (also a क्रिया error) → "आप आपका काम करें।" and "है:" → "है?"
  (key सर्वनाम); Q69 option C देशज (ढूँढना is listed as देशज in many books) → संकर so only the key तद्भव fits; Q72 option A "साक्ष्य मिटाना" (also
  means destroying evidence) → "साक्ष्य संकलन" (key साक्ष्य नाश); Q75 stem "'कानूनी रूप से पकड़ना' शब्द का उपयुक्त हिंदी अर्थ क्या है?" → "… के लिए
  उपयुक्त शब्द क्या है?" (key गिरफ़्तार). Hindi Part D passage is Q76–Q80 (Q61–Q75 standalone); English Q76–80 is an RC passage (Jaipur Literature
  Festival). Carried verbatim: Q8 hyphen minus signs, Q41 "38 of 1", Q52 "Rs." in options, Q60 "sold it a price", Q61 option "crossed the boarder",
  Q65 stem without full stop, Q75 option "changeable" (lower case), HI Q61/Q62 "दिए गये". Q20 (ages) sits in Reasoning but is tagged quant.ages.
  7 hindi.other (Q64–Q67, Q70–Q72); Q61–Q63 hindi.vakya-shuddhi, Q68/Q69 hindi.shabd-bhed, Q73/Q74 hindi.paryayvachi, Q75 hindi.anek-shabd.
- 08 May 2026 Shift 3 — built 2026-11-26 (figure Qs Q9, Q10 — stem + 4 options each, all clean, threshold 200, native size, no padding).
  en/hi/gu cidx agree on all 100, and all 80 EN and 20 HI Part D keys agreed with my own solving. Corrections: Q35 stem "has only _____" →
  "has only about _____" (EN) / "केवल _____" → "केवल लगभग _____" (HI) — Rajasthan had 5.66% of India's population in 2011, key 5.5% kept;
  Q39 EN option "Dada Bhai Naurauji" → "Dadabhai Naoroji"; Q65 had NO misspelt word (all four correct) — EN option A "Criticism" → "Critisism"
  (the GU copy keeps the misspelling the key intends); Q76 stem "according to the descriptions given below" → "according to the passage";
  Q76–80 RC passage instruction line dropped; B1 wraps Q11–Q14 stems, Q52 "3 : 7" and Q46/Q60 options; Q44/Q48 stems rebuilt as KaTeX
  (\frac → \dfrac), Q57 "1/3" and Q58 options → \dfrac, Q49 options normalised to \( 7\sqrt{8} \) etc. HI Part D: Q61 "चिन्ह … है-" →
  "चिह्न … है?"; Q62 sentence "लड़की ने जोर से हँस दी" (the real error was ने with intransitive हँसना — a कारक error, not among the options) →
  "लड़की जोर से हँस दिया" and option D क्रिया → वचन (key लिंग); Q63 option B सर्वनाम (सब is a pronoun, arguable) → क्रिया (key वचन); Q64
  "का सही तकनीकी शब्द है:" → "का सही तकनीकी (अंग्रेज़ी) शब्द क्या है?"; Q69 stem "सुरक्षा व्यवस्था की पूर्व योजना" (आकस्मिक योजना also fitted) →
  "सुरक्षा व्यवस्था के लक्ष्य और उपाय पहले से तय करने वाली समग्र योजना" (key रणनीति); Q72 "<u>सही</u> … क्या होगा:" → plain "सही … क्या होगी?";
  Q78 stem adds "आवागमन … अस्थायी" and option D रुकावट (a plain synonym of अवरोधक) → पहरा (key बैरिकेड); Q79 stem "भविष्य की कार्य योजना" (gave
  the key away) → "भविष्य में किए जाने वाले कार्यों की पहले से बनाई गई रूपरेखा" (key योजना). Hindi Part D passage is Q73–Q77 (Q78–Q80
  standalone); English Q76–80 is an RC passage (Act East Policy). Carried verbatim: Q37 "did … won", Q38 "recently is located", Q42 "(27 of 2)" /
  "18 of 2", Q49 "4 times of its breadth", Q64 option "LOSS", option casing in Q65/Q66/Q67, HI Q66 option "पराक". 9 hindi.other (Q64, Q65,
  Q68, Q69, Q71, Q72, Q78–Q80); Q61 hindi.vyakaran, Q62/Q63 hindi.vakya-shuddhi, Q66/Q67 hindi.upsarg-pratyay, Q70 hindi.sandhi.

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
