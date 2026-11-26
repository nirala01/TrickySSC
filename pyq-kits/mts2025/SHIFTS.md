# SSC MTS 2025 PYQ — shift list and build status

Exam held 4–18 Feb 2026 (SSC calls it "SSC MTS 2025"). 16 shifts in the source (GitHub repo akarohitmishra/repeatermock-subjectwise-db).
The NEXT shift = the first row marked `todo`. Update this file in every chat.
Figures? = how many figure questions the shift has. EVERY shift needs Ashish's upload of its Testbook PDF (link in the last column): the GitHub data lacks the RC passage and has cut stems, and figure shifts need the pictures.

| # | Paper | Prefix | Figures? | Status | Testbook PDF |
|---|---|---|---|---|---|
| 1 | 04 Feb 2026 Shift 3 | ssc-mts-2025-04-feb-shift-3 | 6 | done | https://cdn.testbook.com/1782458884308-SSC%20MTS%2004%20Feb%2C%202026%20Shift%203_English_1781246623.pdf/1782458901.pdf |
| 2 | 05 Feb 2026 Shift 1 | ssc-mts-2025-05-feb-shift-1 | 0 | in progress — needs PDF | https://cdn.testbook.com/1782458884308-SSC%20MTS%2005%20Feb%2C%202026%20Shift%201_English_1781246679.pdf/1782458901.pdf |
| 3 | 05 Feb 2026 Shift 2 | ssc-mts-2025-05-feb-shift-2 | 6 | todo | https://cdn.testbook.com/1782458884308-SSC%20MTS%2005%20Feb%2C%202026%20Shift%202_English_1781246654.pdf/1782458901.pdf |
| 4 | 05 Feb 2026 Shift 3 | ssc-mts-2025-05-feb-shift-3 | 5 | todo | https://cdn.testbook.com/1782458884308-SSC%20MTS%2005%20Feb%2C%202026%20Shift%203_English_1781246640.pdf/1782458901.pdf |
| 5 | 06 Feb 2026 Shift 2 | ssc-mts-2025-06-feb-shift-2 | 7 | todo | https://cdn.testbook.com/1782458893450-SSC%20MTS%2006%20Feb%2C%202026%20Shift%202_English_1781248463.pdf/1782458901.pdf |
| 6 | 06 Feb 2026 Shift 3 | ssc-mts-2025-06-feb-shift-3 | 10 | todo | https://cdn.testbook.com/1782458893450-SSC%20MTS%2006%20Feb%2C%202026%20Shift%203_English_1781248164.pdf/1782458901.pdf |
| 7 | 09 Feb 2026 Shift 1 | ssc-mts-2025-09-feb-shift-1 | 0 | todo | https://cdn.testbook.com/1782458884308-SSC%20MTS%2009%20Feb%2C%202026%20Shift%201_English_1781246730.pdf/1782458901.pdf |
| 8 | 09 Feb 2026 Shift 2 | ssc-mts-2025-09-feb-shift-2 | 9 | todo | https://cdn.testbook.com/1782458884308-SSC%20MTS%2009%20Feb%2C%202026%20Shift%202_English_1781246750.pdf/1782458901.pdf |
| 9 | 09 Feb 2026 Shift 3 | ssc-mts-2025-09-feb-shift-3 | 11 | todo | https://cdn.testbook.com/1782458884308-SSC%20MTS%2009%20Feb%2C%202026%20Shift%203_English_1781246766.pdf/1782458901.pdf |
| 10 | 10 Feb 2026 Shift 1 | ssc-mts-2025-10-feb-shift-1 | 0 | todo | https://cdn.testbook.com/1782459294657-SSC%20MTS%2010%20Feb%2C%202026%20Shift%201_English_1781246787%20%281%29.pdf/1782459311.pdf |
| 11 | 10 Feb 2026 Shift 2 | ssc-mts-2025-10-feb-shift-2 | 10 | todo | https://cdn.testbook.com/1782458884308-SSC%20MTS%2010%20Feb%2C%202026%20Shift%202_English_1781246814.pdf/1782458901.pdf |
| 12 | 10 Feb 2026 Shift 3 | ssc-mts-2025-10-feb-shift-3 | 11 | todo | https://cdn.testbook.com/1782458884308-SSC%20MTS%2010%20Feb%2C%202026%20Shift%203_English_1781246827.pdf/1782458901.pdf |
| 13 | 11 Feb 2026 Shift 1 | ssc-mts-2025-11-feb-shift-1 | 0 | todo | https://cdn.testbook.com/1782458884308-SSC%20MTS%2011%20Feb%2C%202026%20Shift%201_English_1781246865.pdf/1782458901.pdf |
| 14 | 11 Feb 2026 Shift 2 | ssc-mts-2025-11-feb-shift-2 | 9 | todo | https://cdn.testbook.com/1782458884308-SSC%20MTS%2011%20Feb%2C%202026%20Shift%202_English_1781246898.pdf/1782458901.pdf |
| 15 | 11 Feb 2026 Shift 3 | ssc-mts-2025-11-feb-shift-3 | 10 | todo | https://cdn.testbook.com/1782458884308-SSC%20MTS%2011%20Feb%2C%202026%20Shift%203_English_1781246954.pdf/1782458901.pdf |
| 16 | 18 Feb 2026 Shift 3 | ssc-mts-2025-18-feb-shift-3 | 8 | todo | none on Testbook — figures need Ashish's screenshots or Claude in Chrome |

## In progress
- 05 Feb 2026 Shift 1 — 2026-11-27: data.py / sol_en.py / hi.py written for all 90 questions and saved in
  wip-05-feb-shift-1/ (checks PASS, controls 55/55 with placeholders). The Testbook PDF did not reach the chat, so two items are
  still `PENDING-PDF` in data.py: `Q3_D` (the GitHub data has only 3 options for Q3) and `PASSAGE_TEXT` (Q86–Q90 Mary
  Wollstonecraft passage). To finish: copy the folder to /home/claude/w/p02, type those two from the PDF, check the RC
  notes in sol_en.py E[86..90] against the passage, then run steps 2, 5 and 6, and mark the shift done.
  Q33's cut stem is already completed from the source's worked solution.

