# PROMPT-5 ADDENDUM — chapter tagging at CSV time (TrickySSC, Nov 2026)

Paste this block into PROMPT-5-GD (and PROMPT-5 for CGL / CHSL) under the questions-CSV section.
It adds ONE column so that every uploaded paper is already tagged for the chapter-wise PYQ tests —
no separate tagging run is needed afterwards. batch-uploader.html reads the column and writes
chapterId / chapterName / chapterConf = 1 on each question document.

--------------------------------------------------------------------------------------------------
## Chapter column (questions-EN.csv and questions-HI.csv)

Add a column named `chapterId` to BOTH questions CSVs (after `subject`). For every question put
exactly ONE id from the list below, chosen from the question's own subject list.

Rules
- The id must be copied verbatim from the list (lower-case, with the dot). Never invent an id.
- Prefer the most specific chapter. Use a subject's `.other` id only when nothing fits — it should
  be rare, and such questions do not appear in any chapter test.
- The paper section is a hint, not a rule: a number-system question printed in the reasoning
  section still gets a `quant.*` id; a GK fact in the English section gets a `ga.*` id.
- questions-HI.csv must carry the SAME chapterId as the English question with the same qNum
  (SSC GD: Q1–60 only — Part D on the Hindi paper is Hindi Language, tagged with `hindi.*` ids,
  while Part D on the English paper is tagged with `eng.*` ids).
- Ids marked (broad) are umbrella entries kept for old data — use the specific one instead.

Self-check (add to §7): every row has a chapterId that exists in the list; EN and HI ids match
by qNum (except GD Q61–80); the count of `.other` ids is reported and is below 3 per paper.

--------------------------------------------------------------------------------------------------
## Chapter ids


### General Intelligence & Reasoning

reason.analogy — Analogy (Word / Letter / Number) (broad)
reason.analogy-word — Word Analogy
reason.analogy-letter — Letter Analogy
reason.analogy-number — Number Analogy
reason.analogy-number-set — Number-Set & Triad Analogy
reason.analogy-mixed — Mixed Analogy (Letter–Number & Coded)
reason.classification — Classification (Odd One Out) (broad)
reason.classification-word — Word Classification
reason.classification-letter — Letter Classification
reason.classification-number — Number Classification
reason.classification-number-pair — Number-Pair & Triad Classification
reason.classification-mixed — Word-Pair & Mixed Classification
reason.series — Number & Letter Series
reason.coding-decoding — Letter & Number Coding
reason.blood-relation — Family Relations
reason.direction-distance — Direction Sense & Distance
reason.ranking-arrangement — Ranking, Order & Day Sequence
reason.seating-arrangement — Seating Arrangement
reason.syllogism — Syllogism
reason.statement-conclusion — Statement & Conclusion / Inference
reason.venn-diagram — Venn Diagram
reason.mathematical-operations — Mathematical Operations (BODMAS / Symbols)
reason.word-formation — Alphabet & Dictionary Order
reason.missing-number — Missing Number (Matrix)
reason.puzzle — Puzzle / Data Arrangement
reason.calendar-clock — Calendar & Clock
reason.mirror-image — Mirror & Water Image
reason.water-image — Water Image (broad)
reason.paper-folding — Paper Folding, Embedded & Figure Completion
reason.embedded-figure — Embedded / Hidden Figures (broad)
reason.figure-completion — Figure / Pattern Completion (broad)
reason.figure-series — Figure Series, Classification, Analogy & Counting
reason.figure-classification — Figure Classification (broad)
reason.figure-analogy — Figure Analogy (broad)
reason.counting-figures — Counting of Figures (Triangles etc.) (broad)
reason.dice — Dice, Cube, Cuboid & Dot Situation
reason.cube-cuboid — Cube & Cuboid (broad)
reason.dot-situation — Dot Situation (broad)
reason.other — Other / Uncategorized Reasoning

### General Awareness / General Knowledge

ga.history-ancient — History: Ancient India
ga.history-medieval — History: Medieval India
ga.history-modern — History: Modern India & Freedom Struggle
ga.art-culture — Art & Culture
ga.geography-india — Geography: India
ga.geography-world — Geography: World & Physical
ga.polity — Polity & Constitution
ga.economics — Economics
ga.physics — Science: Physics
ga.chemistry — Science: Chemistry
ga.biology — Science: Biology
ga.computer — Computer & Technology
ga.static-books-authors — Static: Books & Authors
ga.static-awards — Static: Awards & Honours
ga.static-days-events — Static: Important Days & Events
ga.static-sports — Static: Sports
ga.static-schemes — Govt Schemes
ga.static-organizations — National & International Organizations
ga.static-misc — Static GK: Misc (Dances, Festivals, Symbols, Superlatives)
ga.current-affairs — Current Affairs
ga.other — Other / Uncategorized GA

### Quantitative Aptitude / Elementary Mathematics

quant.number-system — Number System
quant.divisibility — Rule of Divisibility
quant.remainder-theorem — Remainder Theorem
quant.decimal-fraction — Decimal & Fraction
quant.lcm-hcf — LCM & HCF
quant.square-cube-root — Square, Square Root & Cube, Cube Root
quant.series-ap-gp — Series (AP & GP)
quant.simplification — Power, Indices & Surds
quant.algebraic-formula — Algebraic Formula
quant.algebraic-result — Algebraic Result
quant.percentage — Percentage
quant.profit-loss — Profit & Loss
quant.discount — Discount
quant.simple-interest — Simple Interest
quant.compound-interest — Compound Interest
quant.ratio-proportion — Ratio & Proportion
quant.partnership — Partnership
quant.average — Average
quant.ages — Age
quant.mixture-alligation — Mixture & Alligation
quant.time-work — Time & Work
quant.pipe-cistern — Pipe & Cistern
quant.time-speed-distance — Time, Speed, Distance & Train
quant.algebra — Algebraic Expression & Identities
quant.quadratic-equation — Quadratic Equation
quant.boat-stream — Boat & Stream
quant.race — Race
quant.trigonometry — Trigonometry
quant.height-distance — Height & Distance
quant.geometry — Geometry & Circle
quant.mensuration — Mensuration (2D & 3D)
quant.coordinate-geometry — Co-ordinate Geometry
quant.probability — Probability
quant.statistics — Statistics
quant.data-interpretation — Data Interpretation
quant.other — Other / Uncategorized Quant

### English Language

eng.error-spotting — Spot the Error
eng.sentence-improvement — Sentence Improvement
eng.fill-blanks — Fill in the Blanks
eng.active-passive — Active & Passive Voice
eng.narration — Direct & Indirect Narration
eng.para-jumbles — Sentence Rearrangement / Para Jumbles
eng.synonyms — Synonyms
eng.antonyms — Antonyms
eng.spelling — Spelling Correction
eng.idioms-phrases — Idioms & Phrases
eng.one-word — One Word Substitution
eng.homonyms — Homonyms
eng.cloze-test — Cloze Test
eng.reading-comprehension — Reading Comprehension
eng.other — Other / Uncategorized English

### Hindi Language (हिंदी भाषा — SSC GD Part D on the Hindi paper only)

hindi.sandhi — संधि एवं संधि-विच्छेद (Sandhi)
hindi.samas — समास (Samas)
hindi.upsarg-pratyay — उपसर्ग एवं प्रत्यय (Upsarg & Pratyay)
hindi.paryayvachi — पर्यायवाची शब्द (Synonyms)
hindi.vilom — विलोम शब्द (Antonyms)
hindi.anek-shabd — वाक्यांश के लिए एक शब्द (One Word Substitution)
hindi.muhavare-lokoktiyan — मुहावरे एवं लोकोक्तियाँ (Idioms & Proverbs)
hindi.vartani — शुद्ध वर्तनी (Spelling)
hindi.vakya-shuddhi — वाक्य शुद्धि / अशुद्ध वाक्य (Sentence Correction)
hindi.rikt-sthan — रिक्त स्थान की पूर्ति (Fill in the Blanks)
hindi.vakya-kram — वाक्य क्रम / वाक्य विन्यास (Sentence Rearrangement)
hindi.gadyansh — अपठित गद्यांश (Reading Comprehension)
hindi.shabd-bhed — तत्सम-तद्भव, देशज-विदेशज शब्द (Word Origin)
hindi.anekarthi-shabd — अनेकार्थी एवं समश्रुत भिन्नार्थक शब्द (Homonyms)
hindi.vyakaran — संज्ञा, सर्वनाम, विशेषण, क्रिया, लिंग, वचन, कारक, काल (Grammar)
hindi.vakya-bhed — वाक्य भेद एवं रचनांतरण (Sentence Types)
hindi.other — अन्य / अवर्गीकृत हिंदी (Other Hindi)

### Computer Knowledge (Tier II)

computer.fundamentals — Computer Fundamentals & Organization (CPU, I/O, Ports, Generations)
computer.memory-storage — Memory & Storage Devices
computer.os-windows — Operating System & Windows (Explorer, Shortcuts)
computer.ms-office — MS Office (Word, Excel, PowerPoint)
computer.internet-email — Internet, Web Browsing & E-mail (incl. e-Banking)
computer.networking — Networking (Devices & Protocols)
computer.cyber-security — Cyber Security (Virus, Hacking, Threats)
computer.other — Other / Uncategorized Computer

### Statistics (CGL Tier II Paper II)

statistics.data-collection — Collection, Classification & Presentation of Data
statistics.central-tendency — Measures of Central Tendency
statistics.dispersion — Measures of Dispersion
statistics.moments-skewness-kurtosis — Moments, Skewness & Kurtosis
statistics.correlation-regression — Correlation & Regression
statistics.probability — Probability Theory
statistics.random-variable — Random Variable & Probability Distributions
statistics.sampling — Sampling Theory
statistics.inference — Statistical Inference (Estimation & Testing)
statistics.anova — Analysis of Variance (ANOVA)
statistics.time-series — Time Series Analysis
statistics.index-numbers — Index Numbers
statistics.other — Other / Uncategorized Statistics

### Finance & Economics (CGL Tier II Paper III)

fineco.accounting-fundamentals — Financial Accounting: Nature, Concepts & Conventions (GAAP)
fineco.accounting-basics — Basic Accounting: Single/Double Entry, Journal, Ledger, Trial Balance
fineco.bank-reconciliation — Bank Reconciliation Statement
fineco.rectification-errors — Rectification of Errors
fineco.final-accounts — Final Accounts (Trading, P&L, Balance Sheet)
fineco.capital-revenue — Capital & Revenue Expenditure
fineco.depreciation — Depreciation Accounting
fineco.inventory-valuation — Valuation of Inventories
fineco.non-profit-accounts — Non-Profit Org Accounts (Receipts & Payments, Income & Expenditure)
fineco.bills-exchange — Bills of Exchange
fineco.self-balancing-ledgers — Self-Balancing Ledgers
fineco.constitutional-bodies — Constitutional Bodies: CAG & Finance Commission
fineco.economics-basics — Basic Concepts & Micro Economics Intro (PPC, Central Problems)
fineco.demand-supply — Theory of Demand & Supply (Elasticity, Consumer Behaviour)
fineco.production-cost — Theory of Production & Cost (Returns to Scale)
fineco.market-forms — Forms of Market & Price Determination
fineco.indian-economy — Indian Economy: Sectors (Agriculture, Industry, Services)
fineco.national-income — National Income (Concepts & Measurement)
fineco.population — Population & Growth
fineco.poverty-unemployment — Poverty & Unemployment
fineco.infrastructure — Infrastructure (Energy, Transport, Communication)
fineco.economic-reforms — Economic Reforms since 1991 (LPG & Disinvestment)
fineco.money-banking — Money & Banking (RBI, Commercial Banks, Monetary Policy)
fineco.budget-fiscal — Budget, Fiscal Deficit, BoP & FRBM Act
fineco.it-governance — Role of IT in Governance
fineco.other — Other / Uncategorized Finance & Economics
