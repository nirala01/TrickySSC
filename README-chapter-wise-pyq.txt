TrickySSC — Chapter-wise PYQ (combined across SSC exams) + PYQ cards + mock-plan offer
=====================================================================================
ONE zip, ONE upload. Every file keeps its path. Nothing to run on your PC.

WHERE TO UPLOAD WHAT
--------------------
scripts/build_pyq_chapters.py                 -> scripts/ folder (create it if missing)
.github/workflows/build-pyq-chapters.yml      -> .github/workflows/ (next to your other workflows)
everything else (.html, build_pyq_page.py)    -> repo root, replacing the existing files
PROMPT-5-chapter-tagging-addendum.md          -> not a site file: keep it with your PROMPT-5 prompts (uploading it is harmless)
README-chapter-wise-pyq.txt                   -> don't upload

THEN: GitHub -> Actions -> "Build chapter-wise PYQ tests" -> Run workflow (once).
It commits pyq-chapters/ (test lists), ssc-pyq-chapterwise.html, ssc-<subject>-chapter-wise-pyq.html,
ssc-<chapter>-pyq.html and the sitemap block, and after that runs by itself every night (02:55 IST).
Run it by hand after you upload + tag a new paper if you don't want to wait.

HOW IT IS ORGANISED (combined, not per exam)
--------------------------------------------
ssc-pyq-chapterwise.html             one hub for all SSC exams (shows CGL / CHSL / GD / … counts)
ssc-quant-chapter-wise-pyq.html      subject pages: reasoning, gk, quant, english, hindi, computer, statistics, finance
ssc-percentage-pyq.html              ONE chapter page per chapter: Percentage questions of CGL + CHSL + GD (+ any exam
                                     uploaded later — MTS, CPO … — joins automatically; the script reads every exam)
pyq-chapter-test.html?exam=ssc&tier=all&chapter=quant.percentage&test=1
                                     the player; every question shows "Asked in SSC CGL 2024 · Tier II · 25 Sep 2024 · Shift 1 · Q12"
Tests are 25 questions, in paper date order across exams; a new paper only adds a new test at the END,
so Test 3 never changes. First test of a chapter opens at 10 questions. Low-confidence tags (< 0.7) are
excluded until corrected in admin-pyq-chapter-tag.html.

OTHER FILES IN THIS ZIP
-----------------------
dashboard.html          chapter-wise PYQ attempts shown with a "PYQ · CHAPTER" tag, retry/review links
batch-uploader.html     a chapterId column in a questions CSV is saved at upload (auto-tag)
ssc-cgl-chapterwise.html  link card to the new PYQ hub
build_pyq_page.py, ssc-cgl-pyq.html, ssc-cgl-tier-2-pyq.html, ssc-chsl-pyq.html, ssc-gd-pyq.html
                        the two cards (Chapter-wise PYQs with blinking NEW · Section-wise PYQs) on every PYQ page;
                        the CGL script carries the same markup so its 6-hourly rebuild keeps them
index.html              "SSC Exams Chapter-wise Previous Year Questions" card with blinking NEW on the homepage
test*.html (8 players)  mock test series & plans (CHSL ₹49 / CGL ₹49 / combo ₹79, ₹29 upgrade) after every PYQ attempt
