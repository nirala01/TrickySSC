# TrickySSC Topic-wise Current Affairs Kit

Repo: nirala01/TrickySSC (main = live site). Everything this kit makes lives in `ca-topics/`.
The app (flutter_app) and the website both read these files, so they stay in sync. Do not change the app.

## 0. House rules
- Reply in English, short answers. Never ask for keys or tokens. No helper scripts for Ashish to run.
- Work straight through all 12 sections. Do not stop to ask between sections.
- Standing yes to commit and push inside `ca-topics/` only. Anything else (landing pages, sitemap, other files) needs a fresh yes.
- Fetch live files from raw.githubusercontent.com/nirala01/TrickySSC/main/. If the repo cannot be reached or pushed, say so, hand over the files in chat, and stop.
- If a PDF cannot be read fully, say which pages before doing anything else.

## 1. Sections (id = name), fixed order
1. ca.international = International
2. ca.national = National
3. ca.economic = Economic
4. ca.science-tech = Science and Technology
5. ca.sports = Sports Affairs
6. ca.awards = Awards and Honours
7. ca.conferences = Conferences, Meetings, Fairs, Festivals and Exhibitions
8. ca.appointments = Election and Appointments
9. ca.military = Campaigns, Operations and Military Exercises
10. ca.important-days = Important Days
11. ca.economic-survey = Economic Survey (no month)
12. ca.budget = Budget 2026 (no month)

**Ignore the Rajasthan section of every PDF completely** (and any other state-specific section): no notes and no questions from it. Ids never change.

## 2. Files in ca-topics/
- `index.json` : `{"months":["2026-01",...], "topics":[{"id":"ca.international","name":"International"},...]}`
  `months` = the rolling window, oldest to newest. The app builds the heading ("Jan 2026 to Oct 2026") and filters questions from it.
- `<section id>.json` : `{"parts":[{"month":"2026-10","title":"October 2026","html":"..."}]}` , newest month first, one part per month.
  Economic Survey and Budget: one part, `"month":""`, title = the section name.
- `kit/state.json` : the ledger (section 5).
- `kit/bank/<YYYY-MM>.csv` : that month's questions for all sections (section 4). `kit/bank/special.csv` for Economic Survey and Budget.
- `kit/KIT.md` : this file.

## 3. Notes rules
- Only what SSC / Railway exams ask. Leave out routine figures (monthly GST collection, index values, daily prices and that type).
- The PDF is only a topic list. For every news item: write a fresh heading, then research it on the internet (WebSearch; official PIB/ministry pages first) and take the facts from there. Never copy or paraphrase the PDF's sentences. If the web and the PDF disagree, go with the web and fix any question that used the PDF fact.
- Style: points as `<b>Keyword</b> – fact`, grouped under your own themes, in your own order.
- Check before pushing: no point may share a 6-word run with the PDF text, except official names, themes and titles.
- Short points, one fact per point, key names and numbers in `<b>`.
- Anything special (scheme, project, mission, important organisation, award, summit, exercise) gets a box:
  `<div class="slip"><b>Name</b>: what it is, who runs it, when started, HQ / key facts.</div>`
- Allowed tags only: h3, h4, p, ul, li, b, table, tr, th, td, div class="slip". No inline styles, no images, no links.
- Typical size: 8 to 20 points per section per month, depending on the PDF.

## 4. Question rules and the bank CSV
- 10 to 15 questions per section per month (so 100 to 150 per section over ten months). Economic Survey and Budget: 50 each.
- Every question must be answerable from that month's notes of the same section. One clear correct option, four options, no "all / none of the above".
- No questions on routine figures. No repeats: before writing, read the earlier `kit/bank/*.csv` files and do not repeat a fact already asked in that section.
- Explanation: 4 to 5 short points as `<ul><li>...</li></ul>` (one fact per point). Point 1 states the answer with the key word in `<b>`; the rest add context from the notes plus one or two sure static exam facts. Escape & as &amp;.
- Columns, exactly in this order:
  `text,option_A,option_B,option_C,option_D,correct,explanation,exam,type,subject,chapter,language,level,testNum,qNum,year,difficulty`
- Fixed values: exam=ssc-cgl, type=chapterwise, subject=gk, language=en, level=1, chapter=<section id>, difficulty=easy|medium|hard.
- `year` = the month as YYYY-MM (blank for Economic Survey and Budget). This is the month id the app uses.
- `qNum` = running number per section, never reused. Take the next number from state.json.
- `testNum` = ceil(qNum / 25).
- Standard CSV quoting (quote any field with a comma, quote or line break). UTF-8.

## 5. state.json
`{"monthsDone":["2026-01"], "nextQ":{"ca.international":14, ...}, "specialDone":{"ca.economic-survey":false,"ca.budget":false}, "finalDone":false, "log":["2026-01: 148 questions"]}`
Read it first in every chat, update it last. If the month in the prompt is already in monthsDone, stop and say so.

## 6. Jobs

### MONTH (one PDF, one month)
1. Read state.json, index.json and the earlier bank files.
2. For each section 1 to 10: list the news items, research each on the web, write the notes part, then the questions from those notes.
3. Update each `<section id>.json` (add the part, keep newest first), `index.json` months, `kit/bank/<YYYY-MM>.csv`, `kit/state.json`.
4. Check: JSON files parse; CSV has 17 columns in every row; qNum has no gaps or repeats; `correct` is A/B/C/D.
5. Push `ca-topics/` (standing yes). Report a small table: section, points, questions. Do not paste the notes or the CSV in chat.
6. If finalDone is true (the upload CSVs were already given), also hand over this month's upload CSVs as in FINAL step 2.
7. End with the ready-to-copy prompt for the next month, in a code block, with the next month's name already filled in:
   `TrickySSC current affairs kit. Open https://raw.githubusercontent.com/nirala01/TrickySSC/main/ca-topics/kit/KIT.md and follow it exactly. Job: MONTH. Month: <next month>. PDF attached. Ignore the Rajasthan section of the PDF. Standing yes to push inside ca-topics/ only. Work straight through, don't ask in between.`
   After the last month of the window (October 2026 the first time), give the SPECIAL prompts for Economic Survey and Budget if not done, then the FINAL prompt, instead.

### SPECIAL (Economic Survey or Budget PDF)
Same as MONTH for that one section: one notes part with month "", 50 questions into `kit/bank/special.csv` with year blank.

### FINAL (all CSVs in one place)
1. Read state.json and every bank file. List any month between the first and last that is missing.
2. Build the upload CSVs: one file per section per test, 25 rows each (the last may be shorter): `CA-<section>-T<testNum>.csv`, rows in qNum order, same 17 columns. Give them all in this one chat, zipped, plus a table of section, tests, questions.
3. Set finalDone true in state.json and push.
4. Ask yes for the landing pages: one page per section reading `ca-topics/<id>.json`, a hub page linking all sections, sitemap.xml entries. Match the look of current-affairs.html.
Ashish uploads the CSVs himself with admin-chapterwise.html (leave the override boxes blank so the CSV's own chapter, level and testNum are used).

### ROLL (later: add a month, drop a month)
- Add: run MONTH for the new month.
- Drop: remove that month's part from every section file and the month from index.json `months`. Leave the bank file and Firebase alone; the app stops asking that month by itself. Push and confirm the new heading.
