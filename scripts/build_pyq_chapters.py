#!/usr/bin/env python3
"""
build_pyq_chapters.py — chapter-wise PYQ tests for TrickySSC, COMBINED across SSC exams.

Runs in GitHub Actions (build-pyq-chapters.yml). Pure stdlib, no secrets.

One chapter page holds that chapter's questions from EVERY SSC exam on the site —
Number System has the CGL, CHSL and GD Number System questions together, and any exam
uploaded later (MTS, CPO, …) joins automatically: the script reads every paper and
every PYQ question in Firestore, whatever its exam.

What it does
  1. Reads every previous-year question from Firestore (public REST read, the same web
     key the site pages use) — only the small fields it needs.
  2. Keeps the questions that have a confident chapter tag:
        chapterId set, not an "…other" chapter, chapterConf >= 0.7 (missing conf = hand-set = fine).
     Low-confidence tags are left out until they are corrected in admin-pyq-chapter-tag.html.
  3. Pairs each English question with its Hindi twin (same paper, same qNum).
     SSC GD Part D on the Hindi paper (हिंदी भाषा, hindi.* chapters) has no English twin.
  4. Cuts every chapter into fixed 25-question tests. Order is STABLE: papers keep the
     sequence they were first seen in (pyq-chapters/state.json), so a newly uploaded
     paper only adds questions at the END — Test 3 stays Test 3. A new test appears when
     25 more questions have collected; a chapter with no full test yet shows one test once
     it has 10 questions (that test grows until it reaches 25).
  5. Writes pyq-chapters/all/<chapterId>.json — the question ids of each test with the
     exam, paper and shift each came from — read by pyq-chapter-test.html with ONE batchGet.
  6. Generates the pages: ssc-pyq-chapterwise.html (hub), ssc-<subject>-chapter-wise-pyq.html
     (subject lists) and ssc-<chapter>-pyq.html (one per chapter), and refreshes their
     block in sitemap.xml.

Usage
    python scripts/build_pyq_chapters.py
    python scripts/build_pyq_chapters.py --dump DIR     # build from a saved dump (tests)
"""
import argparse, datetime as dt, html, json, os, re, sys, urllib.request

PROJECT = "trickyssc-17bb3"
API_KEY = "AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA"          # public web key — read-only use
FS = f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "pyq-chapters")
SITE = "https://trickyssc.com"
SET_SIZE, MIN_FIRST_SET, CONF_MIN = 25, 10, 0.7
TODAY = dt.date.today().isoformat()
HUB = "ssc-pyq-chapterwise.html"
PLAYER_EXAM, PLAYER_TIER = "ssc", "all"      # what pyq-chapter-test.html and the attempt records use

# Known exams: display name, whether tiers matter in the label, their PYQ page and mock page.
# Any other exam found in Firestore is shown too, with a name derived from its slug.
EXAMS = {
    "ssc-cgl":  {"name": "SSC CGL",  "tiered": True,  "hub": "ssc-cgl-pyq.html",  "mock": "ssc-cgl-mock-test.html",  "cw": "ssc-cgl-chapterwise.html"},
    "ssc-chsl": {"name": "SSC CHSL", "tiered": True,  "hub": "ssc-chsl-pyq.html", "mock": "ssc-chsl-mock-test.html", "cw": ""},
    "ssc-gd":   {"name": "SSC GD",   "tiered": False, "hub": "ssc-gd-pyq.html",   "mock": "ssc-gd-mock-test.html",   "cw": ""},
    "ssc-mts":  {"name": "SSC MTS",  "tiered": False, "hub": "ssc-mts-pyq.html",  "mock": "",                        "cw": ""},
    "ssc-cpo":  {"name": "SSC CPO",  "tiered": True,  "hub": "ssc-cpo-pyq.html",  "mock": "",                        "cw": ""},
}
EXAM_ORDER = list(EXAMS)
def exam_meta(exam):
    if exam in EXAMS: return EXAMS[exam]
    return {"name": exam.upper().replace("-", " "), "tiered": True, "hub": f"{exam}-pyq.html", "mock": "", "cw": ""}
def exam_name(exam): return exam_meta(exam)["name"]
def short_name(exam): return exam_name(exam).replace("SSC ", "")
TIER_LABEL = {"tier1": "Tier I", "tier2": "Tier II"}
# canonical subject key -> site subject slug, label, colour, icon, order
SUBJECTS = {
    "reasoning":         ("reasoning",  "General Intelligence & Reasoning", "#8B5CF6", "🧠", 1),
    "ga":                ("gk",         "General Awareness (GK)",            "#0EA5E9", "🌍", 2),
    "quant":             ("quant",      "Quantitative Aptitude (Maths)",     "#00A86B", "🔢", 3),
    "english":           ("english",    "English Language",                 "#FF6B00", "✍️", 4),
    "hindi":             ("hindi",      "Hindi Language (हिंदी भाषा)",       "#138808", "📝", 5),
    "computer":          ("computer",   "Computer Knowledge",               "#EC4899", "💻", 6),
    "statistics":        ("statistics", "Statistics",                       "#14B8A6", "📊", 7),
    "finance_economics": ("finance",    "Finance & Economics",              "#6366F1", "💰", 8),
}

CANON = {"hindi": [["hindi.sandhi", "संधि एवं संधि-विच्छेद (Sandhi)"], ["hindi.samas", "समास (Samas)"], ["hindi.upsarg-pratyay", "उपसर्ग एवं प्रत्यय (Upsarg & Pratyay)"], ["hindi.paryayvachi", "पर्यायवाची शब्द (Synonyms)"], ["hindi.vilom", "विलोम शब्द (Antonyms)"], ["hindi.anek-shabd", "वाक्यांश के लिए एक शब्द (One Word Substitution)"], ["hindi.muhavare-lokoktiyan", "मुहावरे एवं लोकोक्तियाँ (Idioms & Proverbs)"], ["hindi.vartani", "शुद्ध वर्तनी (Spelling)"], ["hindi.vakya-shuddhi", "वाक्य शुद्धि / अशुद्ध वाक्य (Sentence Correction)"], ["hindi.rikt-sthan", "रिक्त स्थान की पूर्ति (Fill in the Blanks)"], ["hindi.vakya-kram", "वाक्य क्रम / वाक्य विन्यास (Sentence Rearrangement)"], ["hindi.gadyansh", "अपठित गद्यांश (Reading Comprehension)"], ["hindi.shabd-bhed", "तत्सम-तद्भव, देशज-विदेशज शब्द (Word Origin)"], ["hindi.anekarthi-shabd", "अनेकार्थी एवं समश्रुत भिन्नार्थक शब्द (Homonyms)"], ["hindi.vyakaran", "संज्ञा, सर्वनाम, विशेषण, क्रिया, लिंग, वचन, कारक, काल (Grammar)"], ["hindi.vakya-bhed", "वाक्य भेद एवं रचनांतरण (Sentence Types)"], ["hindi.other", "अन्य / अवर्गीकृत हिंदी (Other Hindi)"]], "reasoning": [["reason.analogy", "Analogy (Word / Letter / Number)"], ["reason.analogy-word", "Word Analogy"], ["reason.analogy-letter", "Letter Analogy"], ["reason.analogy-number", "Number Analogy"], ["reason.analogy-number-set", "Number-Set & Triad Analogy"], ["reason.analogy-mixed", "Mixed Analogy (Letter–Number & Coded)"], ["reason.classification", "Classification (Odd One Out)"], ["reason.classification-word", "Word Classification"], ["reason.classification-letter", "Letter Classification"], ["reason.classification-number", "Number Classification"], ["reason.classification-number-pair", "Number-Pair & Triad Classification"], ["reason.classification-mixed", "Word-Pair & Mixed Classification"], ["reason.series", "Number & Letter Series"], ["reason.coding-decoding", "Letter & Number Coding"], ["reason.blood-relation", "Family Relations"], ["reason.direction-distance", "Direction Sense & Distance"], ["reason.ranking-arrangement", "Ranking, Order & Day Sequence"], ["reason.seating-arrangement", "Seating Arrangement"], ["reason.syllogism", "Syllogism"], ["reason.statement-conclusion", "Statement & Conclusion / Inference"], ["reason.venn-diagram", "Venn Diagram"], ["reason.mathematical-operations", "Mathematical Operations (BODMAS / Symbols)"], ["reason.word-formation", "Alphabet & Dictionary Order"], ["reason.missing-number", "Missing Number (Matrix)"], ["reason.puzzle", "Puzzle / Data Arrangement"], ["reason.calendar-clock", "Calendar & Clock"], ["reason.mirror-image", "Mirror & Water Image"], ["reason.water-image", "Water Image"], ["reason.paper-folding", "Paper Folding, Embedded & Figure Completion"], ["reason.embedded-figure", "Embedded / Hidden Figures"], ["reason.figure-completion", "Figure / Pattern Completion"], ["reason.figure-series", "Figure Series, Classification, Analogy & Counting"], ["reason.figure-classification", "Figure Classification"], ["reason.figure-analogy", "Figure Analogy"], ["reason.counting-figures", "Counting of Figures (Triangles etc.)"], ["reason.dice", "Dice, Cube, Cuboid & Dot Situation"], ["reason.cube-cuboid", "Cube & Cuboid"], ["reason.dot-situation", "Dot Situation"], ["reason.other", "Other / Uncategorized Reasoning"]], "ga": [["ga.history-ancient", "History: Ancient India"], ["ga.history-medieval", "History: Medieval India"], ["ga.history-modern", "History: Modern India & Freedom Struggle"], ["ga.art-culture", "Art & Culture"], ["ga.geography-india", "Geography: India"], ["ga.geography-world", "Geography: World & Physical"], ["ga.polity", "Polity & Constitution"], ["ga.economics", "Economics"], ["ga.physics", "Science: Physics"], ["ga.chemistry", "Science: Chemistry"], ["ga.biology", "Science: Biology"], ["ga.computer", "Computer & Technology"], ["ga.static-books-authors", "Static: Books & Authors"], ["ga.static-awards", "Static: Awards & Honours"], ["ga.static-days-events", "Static: Important Days & Events"], ["ga.static-sports", "Static: Sports"], ["ga.static-schemes", "Govt Schemes"], ["ga.static-organizations", "National & International Organizations"], ["ga.static-misc", "Static GK: Misc (Dances, Festivals, Symbols, Superlatives)"], ["ga.current-affairs", "Current Affairs"], ["ga.other", "Other / Uncategorized GA"]], "quant": [["quant.number-system", "Number System"], ["quant.divisibility", "Rule of Divisibility"], ["quant.remainder-theorem", "Remainder Theorem"], ["quant.decimal-fraction", "Decimal & Fraction"], ["quant.lcm-hcf", "LCM & HCF"], ["quant.square-cube-root", "Square, Square Root & Cube, Cube Root"], ["quant.series-ap-gp", "Series (AP & GP)"], ["quant.simplification", "Power, Indices & Surds"], ["quant.algebraic-formula", "Algebraic Formula"], ["quant.algebraic-result", "Algebraic Result"], ["quant.percentage", "Percentage"], ["quant.profit-loss", "Profit & Loss"], ["quant.discount", "Discount"], ["quant.simple-interest", "Simple Interest"], ["quant.compound-interest", "Compound Interest"], ["quant.ratio-proportion", "Ratio & Proportion"], ["quant.partnership", "Partnership"], ["quant.average", "Average"], ["quant.ages", "Age"], ["quant.mixture-alligation", "Mixture & Alligation"], ["quant.time-work", "Time & Work"], ["quant.pipe-cistern", "Pipe & Cistern"], ["quant.time-speed-distance", "Time, Speed, Distance & Train"], ["quant.algebra", "Algebraic Expression & Identities"], ["quant.quadratic-equation", "Quadratic Equation"], ["quant.boat-stream", "Boat & Stream"], ["quant.race", "Race"], ["quant.trigonometry", "Trigonometry"], ["quant.height-distance", "Height & Distance"], ["quant.geometry", "Geometry & Circle"], ["quant.mensuration", "Mensuration (2D & 3D)"], ["quant.coordinate-geometry", "Co-ordinate Geometry"], ["quant.probability", "Probability"], ["quant.statistics", "Statistics"], ["quant.data-interpretation", "Data Interpretation"], ["quant.other", "Other / Uncategorized Quant"]], "english": [["eng.error-spotting", "Spot the Error"], ["eng.sentence-improvement", "Sentence Improvement"], ["eng.fill-blanks", "Fill in the Blanks"], ["eng.active-passive", "Active & Passive Voice"], ["eng.narration", "Direct & Indirect Narration"], ["eng.para-jumbles", "Sentence Rearrangement / Para Jumbles"], ["eng.synonyms", "Synonyms"], ["eng.antonyms", "Antonyms"], ["eng.spelling", "Spelling Correction"], ["eng.idioms-phrases", "Idioms & Phrases"], ["eng.one-word", "One Word Substitution"], ["eng.homonyms", "Homonyms"], ["eng.cloze-test", "Cloze Test"], ["eng.reading-comprehension", "Reading Comprehension"], ["eng.other", "Other / Uncategorized English"]], "computer": [["computer.fundamentals", "Computer Fundamentals & Organization (CPU, I/O, Ports, Generations)"], ["computer.memory-storage", "Memory & Storage Devices"], ["computer.os-windows", "Operating System & Windows (Explorer, Shortcuts)"], ["computer.ms-office", "MS Office (Word, Excel, PowerPoint)"], ["computer.internet-email", "Internet, Web Browsing & E-mail (incl. e-Banking)"], ["computer.networking", "Networking (Devices & Protocols)"], ["computer.cyber-security", "Cyber Security (Virus, Hacking, Threats)"], ["computer.other", "Other / Uncategorized Computer"]], "statistics": [["statistics.data-collection", "Collection, Classification & Presentation of Data"], ["statistics.central-tendency", "Measures of Central Tendency"], ["statistics.dispersion", "Measures of Dispersion"], ["statistics.moments-skewness-kurtosis", "Moments, Skewness & Kurtosis"], ["statistics.correlation-regression", "Correlation & Regression"], ["statistics.probability", "Probability Theory"], ["statistics.random-variable", "Random Variable & Probability Distributions"], ["statistics.sampling", "Sampling Theory"], ["statistics.inference", "Statistical Inference (Estimation & Testing)"], ["statistics.anova", "Analysis of Variance (ANOVA)"], ["statistics.time-series", "Time Series Analysis"], ["statistics.index-numbers", "Index Numbers"], ["statistics.other", "Other / Uncategorized Statistics"]], "finance_economics": [["fineco.accounting-fundamentals", "Financial Accounting: Nature, Concepts & Conventions (GAAP)"], ["fineco.accounting-basics", "Basic Accounting: Single/Double Entry, Journal, Ledger, Trial Balance"], ["fineco.bank-reconciliation", "Bank Reconciliation Statement"], ["fineco.rectification-errors", "Rectification of Errors"], ["fineco.final-accounts", "Final Accounts (Trading, P&L, Balance Sheet)"], ["fineco.capital-revenue", "Capital & Revenue Expenditure"], ["fineco.depreciation", "Depreciation Accounting"], ["fineco.inventory-valuation", "Valuation of Inventories"], ["fineco.non-profit-accounts", "Non-Profit Org Accounts (Receipts & Payments, Income & Expenditure)"], ["fineco.bills-exchange", "Bills of Exchange"], ["fineco.self-balancing-ledgers", "Self-Balancing Ledgers"], ["fineco.constitutional-bodies", "Constitutional Bodies: CAG & Finance Commission"], ["fineco.economics-basics", "Basic Concepts & Micro Economics Intro (PPC, Central Problems)"], ["fineco.demand-supply", "Theory of Demand & Supply (Elasticity, Consumer Behaviour)"], ["fineco.production-cost", "Theory of Production & Cost (Returns to Scale)"], ["fineco.market-forms", "Forms of Market & Price Determination"], ["fineco.indian-economy", "Indian Economy: Sectors (Agriculture, Industry, Services)"], ["fineco.national-income", "National Income (Concepts & Measurement)"], ["fineco.population", "Population & Growth"], ["fineco.poverty-unemployment", "Poverty & Unemployment"], ["fineco.infrastructure", "Infrastructure (Energy, Transport, Communication)"], ["fineco.economic-reforms", "Economic Reforms since 1991 (LPG & Disinvestment)"], ["fineco.money-banking", "Money & Banking (RBI, Commercial Banks, Monetary Policy)"], ["fineco.budget-fiscal", "Budget, Fiscal Deficit, BoP & FRBM Act"], ["fineco.it-governance", "Role of IT in Governance"], ["fineco.other", "Other / Uncategorized Finance & Economics"]]}

CH_ICON = {"quant.number-system": "🔢", "quant.divisibility": "➗", "quant.remainder-theorem": "🧮", "quant.decimal-fraction": "½", "quant.lcm-hcf": "🔗", "quant.square-cube-root": "√", "quant.series-ap-gp": "📶", "quant.simplification": "⚡", "quant.algebraic-formula": "x&sup2;", "quant.algebraic-result": "x+1/x", "quant.algebra": "𝑥", "quant.percentage": "%", "quant.profit-loss": "💰", "quant.discount": "🏷️", "quant.simple-interest": "🏦", "quant.compound-interest": "📈", "quant.ratio-proportion": "⚖️", "quant.partnership": "🤝", "quant.average": "x̄", "quant.ages": "🎂", "quant.mixture-alligation": "🧪", "quant.time-work": "🛠️", "quant.pipe-cistern": "🚰", "quant.time-speed-distance": "🚄", "quant.quadratic-equation": "ax²", "quant.boat-stream": "⛵", "quant.race": "🏁", "quant.trigonometry": "📐", "quant.height-distance": "🗼", "quant.geometry": "⭕", "quant.mensuration": "📦", "quant.coordinate-geometry": "🧭", "quant.probability": "🎲", "quant.statistics": "📉", "quant.data-interpretation": "📊", "reason.analogy-word": "🔤", "reason.analogy-letter": "🔡", "reason.analogy-number": "🧮", "reason.analogy-number-set": "🎲", "reason.analogy-mixed": "🔣", "reason.classification-word": "🧩", "reason.classification-letter": "🔠", "reason.classification-number": "🔟", "reason.classification-number-pair": "🔀", "reason.classification-mixed": "🔗", "reason.series": "🔢", "reason.coding-decoding": "🔐", "reason.blood-relation": "👨‍👩‍👦", "reason.direction-distance": "🧭", "reason.ranking-arrangement": "🏅", "reason.seating-arrangement": "💺", "reason.syllogism": "⭕", "reason.statement-conclusion": "💭", "reason.venn-diagram": "◑", "reason.mathematical-operations": "➗", "reason.word-formation": "🔤", "reason.missing-number": "❓", "reason.puzzle": "🧠", "reason.calendar-clock": "📅", "reason.mirror-image": "🪞", "reason.paper-folding": "📄", "reason.figure-series": "🔷", "reason.dice": "🎲", "eng.error-spotting": "🔍", "eng.sentence-improvement": "✨", "eng.fill-blanks": "✏️", "eng.active-passive": "🔄", "eng.narration": "💬", "eng.para-jumbles": "🧩", "eng.synonyms": "🟰", "eng.antonyms": "↔️", "eng.spelling": "🔤", "eng.idioms-phrases": "🗣️", "eng.one-word": "🎯", "eng.homonyms": "👂", "eng.cloze-test": "📄", "eng.reading-comprehension": "📖", "ga.history-ancient": "🏛️", "ga.history-medieval": "🕌", "ga.history-modern": "🇮🇳", "ga.art-culture": "🎭", "ga.geography-india": "🗺️", "ga.geography-world": "🌍", "ga.polity": "⚖️", "ga.economics": "💹", "ga.physics": "⚛️", "ga.chemistry": "🧪", "ga.biology": "🧬", "ga.computer": "💻", "ga.static-books-authors": "📚", "ga.static-awards": "🏆", "ga.static-days-events": "📅", "ga.static-sports": "🏏", "ga.static-schemes": "🏗️", "ga.static-organizations": "🏢", "ga.static-misc": "💃", "ga.current-affairs": "📰"}   # chapter icons, same as the chapter-wise test pages

NAME = {}; SUBJ_OF = {}
for _s, _l in CANON.items():
    for _id, _n in _l:
        NAME[_id] = _n; SUBJ_OF[_id] = _s


# ── Firestore ────────────────────────────────────────────────────────────────
def _val(v):
    if v is None: return None
    for k in ("stringValue", "booleanValue"):
        if k in v: return v[k]
    if "integerValue" in v: return int(v["integerValue"])
    if "doubleValue" in v: return float(v["doubleValue"])
    if "timestampValue" in v: return v["timestampValue"]
    if "mapValue" in v: return {k: _val(x) for k, x in (v["mapValue"].get("fields") or {}).items()}
    return None

def _post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (TrickySSC pyq-chapters builder)"}, method="POST")
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read().decode())

def run_query(collection, filters, fields, page=4000):
    """All docs matching the equality filters (none = whole collection), selected fields only, paged by __name__."""
    out, cursor = [], None
    while True:
        q = {"from": [{"collectionId": collection}],
             "select": {"fields": [{"fieldPath": f} for f in fields]},
             "orderBy": [{"field": {"fieldPath": "__name__"}, "direction": "ASCENDING"}],
             "limit": page}
        ff = [{"fieldFilter": {"field": {"fieldPath": f}, "op": "EQUAL", "value": {"stringValue": v}}} for f, v in filters]
        if len(ff) == 1: q["where"] = ff[0]
        elif ff: q["where"] = {"compositeFilter": {"op": "AND", "filters": ff}}
        if cursor: q["startAt"] = {"values": [{"referenceValue": cursor}], "before": False}
        rows = _post(f"{FS}:runQuery?key={API_KEY}", {"structuredQuery": q})
        docs = [r["document"] for r in rows if r.get("document")]
        for d in docs:
            rec = {k: _val(v) for k, v in (d.get("fields") or {}).items()}
            rec["_id"] = d["name"].rsplit("/", 1)[-1]
            out.append(rec)
        if len(docs) < page: break
        cursor = docs[-1]["name"]
    return out

def fetch_all():
    papers = run_query("papers", [], ["paperId", "exam", "year", "tier", "shift", "heldOn", "language", "type", "mockId", "questionCount"])
    qs = run_query("questions", [("type", "pyq")], ["paperId", "exam", "qNum", "language", "subject", "chapterId", "chapterConf", "tier", "year", "shift", "heldOn"])
    return papers, qs


# ── shaping ──────────────────────────────────────────────────────────────────
def norm_lang(v):
    return "hi" if re.match(r"^\s*h", str(v or ""), re.I) else "en"

def norm_tier(v):
    return "tier2" if re.search(r"2|ii", str(v or ""), re.I) else "tier1"

def norm_shift(v):
    d = re.findall(r"\d+", str(v or ""))
    return ("Shift " + d[0]) if d else str(v or "").strip()

def norm_exam(v):
    v = str(v or "").strip().lower().replace("_", "-").replace(" ", "-")
    return v if v.startswith("ssc-") else ("ssc-" + v if v else "")

def pretty_date(held):
    try:
        d = dt.date.fromisoformat(str(held)[:10]); return d.strftime("%d %b %Y").lstrip("0")
    except Exception:
        return str(held or "")

def is_hindi_subject(v):
    return bool(re.search(r"हिंदी|हिन्दी|hindi", str(v or ""), re.I))

def eligible(q):
    cid = q.get("chapterId") or ""
    if not cid or cid not in NAME or cid.endswith(".other"): return False
    conf = q.get("chapterConf")
    if conf is None: return True
    try: return float(conf) >= CONF_MIN
    except Exception: return True

def paper_key(exam, p):
    return exam + "|" + "|".join(str(p.get(k) or "") for k in ("year", "tier", "shift", "heldOn"))

def paper_label(exam, c):
    tier = f" · {TIER_LABEL[c['tier']]}" if exam_meta(exam)["tiered"] else ""
    return f"{exam_name(exam)} {c['year']}{tier} · {pretty_date(c['heldOn'])} · {c['shift']}".replace(" ·  ·", " ·").strip(" ·")

def build_all(papers, qs):
    # paper cards → one per exam/year/tier/shift/date (ignore mocks)
    cards = {}
    for p in papers:
        if str(p.get("type") or "").lower() == "mock" or p.get("mockId"): continue
        exam = norm_exam(p.get("exam"))
        if not exam: continue
        k = paper_key(exam, p)
        c = cards.setdefault(k, {"exam": exam, "year": str(p.get("year") or ""), "tier": norm_tier(p.get("tier")), "shift": norm_shift(p.get("shift")), "heldOn": str(p.get("heldOn") or ""), "ids": set()})
        if p.get("paperId"): c["ids"].add(p["paperId"])
        c["ids"].add(p["_id"])
    by_pid = {pid: k for k, c in cards.items() for pid in c["ids"]}
    def qkey(q):
        pid = q.get("paperId") or ""
        if pid in by_pid: return by_pid[pid]
        alt = re.sub(r"_(hi|hindi|en|english)$", "", pid)
        for suf in ("_en", "_hi", "_english", "_hindi"):
            if alt + suf in by_pid: return by_pid[alt + suf]
        exam = norm_exam(q.get("exam"))
        if not exam: return None
        k = paper_key(exam, {"year": q.get("year"), "tier": q.get("tier"), "shift": q.get("shift"), "heldOn": q.get("heldOn")})
        if k not in cards and q.get("heldOn"):
            cards[k] = {"exam": exam, "year": str(q.get("year") or ""), "tier": norm_tier(q.get("tier")), "shift": norm_shift(q.get("shift")), "heldOn": str(q.get("heldOn") or ""), "ids": {pid}}
        return k if k in cards else None

    grid = {}   # key -> {"en": {qNum: doc}, "hi": {qNum: doc}}
    for q in qs:
        k = qkey(q)
        if not k: continue
        L = norm_lang(q.get("language"))
        try: n = int(q.get("qNum") or 0)
        except Exception: n = 0
        if n: grid.setdefault(k, {"en": {}, "hi": {}})[L][n] = q

    # stable paper order across ALL exams: first seen first; new papers appended by date
    state_path = os.path.join(OUT, "state.json")
    state = json.load(open(state_path, encoding="utf-8")) if os.path.exists(state_path) else {"order": []}
    order = [k for k in state["order"] if k in grid]
    new = sorted([k for k in grid if k not in order], key=lambda k: (cards[k]["heldOn"], cards[k]["exam"], cards[k]["tier"], cards[k]["shift"]))
    order += new
    state["order"] = order; state["updated"] = TODAY
    os.makedirs(OUT, exist_ok=True)
    json.dump(state, open(state_path, "w", encoding="utf-8"), ensure_ascii=False, indent=0)

    chapters = {}  # cid -> list of {en, hi, p, q, x}
    counts = {"papers": len(order), "questions": 0, "eligible": 0, "excluded_low": 0, "untagged": 0}
    exams_seen = {}
    for k in order:
        c = cards[k]; exam = c["exam"]; label = paper_label(exam, c)
        exams_seen.setdefault(exam, {"papers": 0, "questions": 0, "years": set()})
        exams_seen[exam]["papers"] += 1
        if c["year"]: exams_seen[exam]["years"].add(c["year"])
        g = grid[k]
        def add(q, en_id, hi_id, n):
            counts["questions"] += 1
            if not q.get("chapterId"): counts["untagged"] += 1; return
            if not eligible(q): counts["excluded_low"] += 1; return
            counts["eligible"] += 1; exams_seen[exam]["questions"] += 1
            chapters.setdefault(q["chapterId"], []).append({"en": en_id, "hi": hi_id, "p": label, "q": n, "x": exam})
        for n in sorted(g["en"]):
            q = g["en"][n]; hi = g["hi"].get(n)
            if hi and is_hindi_subject(hi.get("subject")): hi = None     # GD Part D: a different question on the Hindi paper
            add(q, q["_id"], hi["_id"] if hi else None, n)
        for n in sorted(g["hi"]):                                        # Hindi-paper-only questions
            if n in g["en"] and not is_hindi_subject(g["hi"][n].get("subject")): continue
            q = g["hi"][n]; add(q, None, q["_id"], n)

    index = {}   # subject -> [chapter summary]
    written = 0
    d = os.path.join(OUT, "all"); os.makedirs(d, exist_ok=True)
    for cid, items in sorted(chapters.items()):
        full = len(items) // SET_SIZE
        sets = [{"n": i + 1, "qs": items[i * SET_SIZE:(i + 1) * SET_SIZE]} for i in range(full)]
        rem = items[full * SET_SIZE:]
        if not sets and len(rem) >= MIN_FIRST_SET:
            sets = [{"n": 1, "qs": rem}]; rem = []
        subj = SUBJ_OF[cid]
        by_exam = {}
        for x in items: by_exam[x["x"]] = by_exam.get(x["x"], 0) + 1
        summary = {"id": cid, "name": NAME[cid], "subject": subj, "count": len(items), "tests": len(sets),
                   "waiting": len(rem), "hi": any(x["hi"] for s in sets for x in s["qs"]), "en": any(x["en"] for s in sets for x in s["qs"]),
                   "exams": dict(sorted(by_exam.items(), key=lambda kv: (EXAM_ORDER.index(kv[0]) if kv[0] in EXAM_ORDER else 99, kv[0]))),
                   "years": sorted({m.group(1) for x in items for m in [re.search(r"\b(20\d\d)\b", x["p"])] if m})}
        index.setdefault(subj, []).append(summary)
        if sets:
            data = {"exam": PLAYER_EXAM, "tier": PLAYER_TIER, "chapter": cid, "name": NAME[cid], "subject": subj, "count": len(items), "built": TODAY, "sets": sets}
            path = os.path.join(d, cid + ".json")
            txt = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
            if (json.loads(old).get("sets") != sets) if old else True:
                open(path, "w", encoding="utf-8").write(txt); written += 1
    for subj in index:
        index[subj].sort(key=lambda c: (-c["tests"], -c["count"], c["name"]))
    exams = {e: {"name": exam_name(e), "papers": v["papers"], "questions": v["questions"], "years": sorted(v["years"])} for e, v in exams_seen.items()}
    json.dump({"built": TODAY, "counts": counts, "exams": exams, "subjects": index}, open(os.path.join(OUT, "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ex_txt = ", ".join("%s %dp/%dq" % (e, v["papers"], v["questions"]) for e, v in exams.items())
    print(f"all exams: {counts} · exams {ex_txt} → {sum(len(v) for v in index.values())} chapters, {written} test files changed")
    return index, counts, exams


# ── pages ────────────────────────────────────────────────────────────────────
E = lambda s: html.escape(str(s), quote=True)

def slug_of(cid):
    # reason/ga/quant/eng chapters keep a plain slug (ssc-percentage-pyq.html); the Tier-II
    # modules and Hindi keep their prefix so e.g. quant.probability / statistics.probability can't clash
    pre, rest = cid.split(".", 1)
    return rest if pre in ("reason", "ga", "quant", "eng") else f"{pre}-{rest}"

def chapter_file(cid):  return f"ssc-{slug_of(cid)}-pyq.html"
def subject_file(subj): return f"ssc-{SUBJECTS[subj][0]}-chapter-wise-pyq.html"
def subj_label(subj):   return SUBJECTS[subj][1]
def subj_short(subj):   return SUBJECTS[subj][1].split(" (")[0]

def exams_line(exams, sep=" · "):
    """'CGL 48 · CHSL 30 · GD 12' from a {exam: count} dict"""
    return sep.join(f"{short_name(e)} {n}" for e, n in exams.items())

def exams_sentence(exams):
    names = [exam_name(e) for e in sorted(exams, key=lambda e: (EXAM_ORDER.index(e) if e in EXAM_ORDER else 99, e))]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]

ACCOUNT_JS = """
<script type="module">
import { initializeApp, getApps } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
const FIRE_CFG={apiKey:"AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA",authDomain:"trickyssc-17bb3.firebaseapp.com",projectId:"trickyssc-17bb3",storageBucket:"trickyssc-17bb3.firebasestorage.app",messagingSenderId:"450627057220",appId:"1:450627057220:web:366267bf437d94f20c6e11"};
const app=getApps().length?getApps()[0]:initializeApp(FIRE_CFG); const auth=getAuth(app);
function first(n){ return (String(n||'').trim().split(/\\s+/)[0])||'Account'; }
function paint(u){ const el=document.getElementById('navAccount'); if(!el) return;
  if(u&&u.uid){ const fn=first(u.name), ini=(fn[0]||'A').toUpperCase();
    const av=u.photoURL?('<img class="acct-av" src="'+u.photoURL+'" alt="" referrerpolicy="no-referrer">'):('<span class="acct-av">'+ini+'</span>');
    el.innerHTML='<div class="acct"><a class="acct-chip" href="https://trickyssc.com/index.html" title="My dashboard">'+av+'<span class="acct-name">'+fn+'</span></a><button class="acct-out" type="button" onclick="tsscLogout()">Log out</button></div>';
  } else el.innerHTML='<a class="nav-cta" href="https://trickyssc.com/login.html" onclick="tsscStashReturn()">👤 Login</a>'; }
window.tsscStashReturn=()=>{ try{ localStorage.setItem('loginReturnTo', location.href); }catch(e){} };
window.tsscLogout=async()=>{ try{ await signOut(auth); }catch(e){} try{ localStorage.removeItem('tssc_user'); }catch(e){} paint(null); };
try{ const c=JSON.parse(localStorage.getItem('tssc_user')||'null'); if(c&&c.uid) paint(c); }catch(e){}
onAuthStateChanged(auth, async user=>{
  if(user){ const data={uid:user.uid,name:user.displayName||'Student',phone:user.phoneNumber||'',email:user.email||'',photoURL:user.photoURL||'',loginMethod:user.phoneNumber?'phone':'google'};
    try{ const c=JSON.parse(localStorage.getItem('tssc_user')||'null'); if(c&&c.uid===user.uid){ if((!data.name||data.name==='Student')&&c.name) data.name=c.name; if(!data.photoURL&&c.photoURL) data.photoURL=c.photoURL; } }catch(e){}
    try{ localStorage.setItem('tssc_user', JSON.stringify(data)); }catch(e){} paint(data);
    if(window.tsscPaintAttempts){ try{ window.tsscPaintAttempts(user); }catch(e){} }
  } else { try{ localStorage.removeItem('tssc_user'); }catch(e){} paint(null); }
});
</script>
"""


# ── pages (same look as the chapter-wise test pages: white nav, hero card, chapter rows, test tiles) ──
ACCENT = {   # subject -> (accent, soft, dark, shadow)   — same colours as ssc-cgl-<subject>-chapter-wise-test.html
    "quant":             ("#00A86B", "rgba(0,168,107,.10)",  "#00885A", "rgba(0,168,107,.32)"),
    "reasoning":         ("#8B5CF6", "rgba(139,92,246,.10)", "#7C3AED", "rgba(139,92,246,.32)"),
    "english":           ("#0EA5E9", "rgba(14,165,233,.10)", "#0284C7", "rgba(14,165,233,.32)"),
    "ga":                ("#F59E0B", "rgba(245,158,11,.12)", "#D97706", "rgba(245,158,11,.34)"),
    "hindi":             ("#138808", "rgba(19,136,8,.10)",   "#0F6B06", "rgba(19,136,8,.32)"),
    "computer":          ("#EC4899", "rgba(236,72,153,.10)", "#DB2777", "rgba(236,72,153,.32)"),
    "statistics":        ("#14B8A6", "rgba(20,184,166,.10)", "#0D9488", "rgba(20,184,166,.32)"),
    "finance_economics": ("#6366F1", "rgba(99,102,241,.10)", "#4F46E5", "rgba(99,102,241,.32)"),
}
SUBJ_ICON = {"quant": "🔢", "reasoning": "🧠", "english": "✍️", "ga": "🌍", "hindi": "📝", "computer": "💻", "statistics": "📊", "finance_economics": "💰"}
def accent_css(subj):
    a, s, d, sh = ACCENT.get(subj, ACCENT["quant"])
    return f"--accent:{a};--accent-soft:{s};--accent-dark:{d};--accent-shadow:{sh};"
def icon_of(cid):
    return CH_ICON.get(cid) or SUBJ_ICON.get(SUBJ_OF.get(cid, ""), "📘")

CSS = """
:root{--accent:#FF6B00;--accent-soft:rgba(255,107,0,.10);--accent-dark:#E05E00;--accent-shadow:rgba(255,107,0,.32);}
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Hind',sans-serif;background:#F5F7FA;color:#1A202C;line-height:1.7;}
a{color:var(--accent);}
.wrap{max-width:1100px;margin:0 auto;padding:0 1.25rem;}
.nav{background:#fff;border-bottom:1px solid #E2E8F0;position:sticky;top:0;z-index:100;box-shadow:0 2px 8px rgba(0,0,0,.06);}
.nav-inner{max-width:1100px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;height:60px;padding:0 1.25rem;}
.logo{font-family:'Baloo 2',cursive;font-size:1.5rem;font-weight:800;text-decoration:none;color:#1A202C;white-space:nowrap;}
.logo span{color:#FF6B00;}
.nav-links{display:flex;gap:1.1rem;flex-wrap:wrap;}
.nav-links a{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.85rem;letter-spacing:.4px;text-transform:uppercase;color:#4A5568;text-decoration:none;}
.nav-links a:hover,.nav-links a.on{color:#FF6B00;}
@media(max-width:820px){.nav-links{display:none;}}
.nav-acct{display:flex;align-items:center;gap:.5rem;flex-shrink:0;}
.nav-cta{display:inline-flex;align-items:center;gap:.35rem;background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff!important;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.85rem;padding:.4rem .9rem;border-radius:100px;text-decoration:none;box-shadow:0 4px 14px rgba(255,107,0,.3);}
.acct{display:flex;align-items:center;gap:.5rem;}
.acct-chip{display:inline-flex;align-items:center;gap:.5rem;padding:.28rem .75rem .28rem .3rem;border:1px solid #E2E8F0;border-radius:100px;background:#fff;text-decoration:none;}
.acct-chip:hover{border-color:#FF6B00;box-shadow:0 4px 14px rgba(255,107,0,.16);}
.acct-av{width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;display:flex;align-items:center;justify-content:center;font-family:'Baloo 2',cursive;font-weight:800;font-size:.85rem;flex-shrink:0;object-fit:cover;}
img.acct-av{border:1px solid #E2E8F0;}
.acct-name{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.9rem;color:#1A202C;max-width:110px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.acct-out{border:1px solid #E2E8F0;background:#fff;color:#64748B;border-radius:100px;padding:.32rem .8rem;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.82rem;cursor:pointer;}
.acct-out:hover{border-color:#FCA5A5;color:#DC2626;background:#FEF2F2;}
@media(max-width:520px){.acct-name{max-width:70px;}.acct-out{padding:.3rem .6rem;font-size:.76rem;}}
.breadcrumb{font-size:.82rem;color:#A0AEC0;padding:1.1rem 0 .4rem;font-family:'Rajdhani',sans-serif;font-weight:600;letter-spacing:.5px;}
.breadcrumb a{color:#A0AEC0;text-decoration:none;}.breadcrumb a:hover{color:#FF6B00;}
.hero{background:#fff;border:1px solid #E2E8F0;border-left:6px solid var(--accent);border-radius:18px;padding:1.8rem;box-shadow:0 2px 12px rgba(0,0,0,.06);margin-bottom:1.4rem;}
.hero-top{display:flex;align-items:center;gap:1rem;margin-bottom:.7rem;}
.hero-ic{width:56px;height:56px;border-radius:16px;background:var(--accent-soft);display:flex;align-items:center;justify-content:center;font-size:1.7rem;flex-shrink:0;}
h1{font-family:'Baloo 2',cursive;font-size:1.85rem;font-weight:800;line-height:1.22;margin-bottom:.5rem;}
.hero .lede{color:#4A5568;font-size:1rem;}
.chips{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:1.1rem;}
.chip{background:#F7FAFC;border:1px solid #E2E8F0;border-radius:100px;padding:.35rem .9rem;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.85rem;color:#4A5568;}
.chip b{color:var(--accent);}
.cw-free{display:flex;align-items:center;gap:.75rem;flex-wrap:wrap;margin:.9rem 0 0;padding:.7rem .95rem;border-radius:14px;background:linear-gradient(135deg,#ECFDF5,#D1FAE5);border:1.5px solid #6EE7B7;box-shadow:0 4px 14px rgba(16,185,129,.12);}
.cw-free-tag{flex:0 0 auto;font-family:'Rajdhani',sans-serif;font-weight:800;font-size:.8rem;letter-spacing:1.2px;color:#fff;background:linear-gradient(135deg,#059669,#10B981);border-radius:100px;padding:.3rem .75rem;}
.cw-free-txt{flex:1 1 220px;min-width:0;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.98rem;color:#065F46;line-height:1.35;}
.cw-free-txt small{display:block;font-family:'Hind',sans-serif;font-weight:500;font-size:.82rem;color:#047857;margin-top:.1rem;}
section{margin-bottom:2.2rem;}
h2{font-family:'Baloo 2',cursive;font-size:1.4rem;font-weight:800;margin:0 0 .7rem;padding-top:.4rem;}
h3{font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;margin:1.1rem 0 .4rem;color:#2D3748;}
p{margin-bottom:.9rem;color:#2D3748;}
.types-card{display:flex;gap:.9rem;align-items:flex-start;background:linear-gradient(135deg,#EEF2FF,#F5F3FF);border:1px solid #C7D2FE;border-left:6px solid #6366F1;border-radius:14px;padding:.95rem 1.1rem;margin-bottom:1.1rem;}
.tc-ico{flex:0 0 42px;height:42px;display:flex;align-items:center;justify-content:center;background:#fff;border-radius:11px;font-size:1.35rem;box-shadow:0 1px 4px rgba(0,0,0,.08);}
.tc-body{flex:1 1 auto;min-width:0;}
.tc-title{font-family:'Baloo 2',cursive;font-weight:800;font-size:1.08rem;color:#312E81;line-height:1.3;}
.tc-sub{font-size:.86rem;color:#4338CA;margin-top:.25rem;line-height:1.5;}
.note{background:#FFF7ED;border:1px solid #FED7AA;border-radius:12px;padding:.85rem 1.1rem;font-size:.92rem;color:#7C2D12;margin-bottom:1.1rem;}
.subj-nav{display:flex;flex-wrap:wrap;gap:.45rem;margin:0 0 1rem;}
.subj-nav a{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.84rem;padding:.32rem .8rem;border-radius:100px;background:#fff;border:1px solid #E2E8F0;color:#4A5568;text-decoration:none;}
.subj-nav a:hover{border-color:var(--accent);color:var(--accent);}
.search{display:flex;align-items:center;gap:.5rem;background:#fff;border:1px solid #E2E8F0;border-radius:100px;padding:.5rem 1rem;color:#718096;font-size:.92rem;margin:0 0 1rem;}
.search input{border:0;outline:0;flex:1;font:inherit;background:transparent;color:#1A202C;}
/* chapter rows */
.ch-list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1.05rem;}
.ch-item{list-style:none;margin:0;}
.ch-top{position:relative;}
.ch-row{display:flex;align-items:center;gap:1rem;background:#fff;border:1px solid #E2E8F0;border-radius:14px;padding:.8rem 3.6rem .8rem 1.1rem;text-decoration:none;position:relative;overflow:hidden;transition:transform .16s ease,box-shadow .16s ease,border-color .16s ease;}
.ch-row.no-exp{padding-right:1.1rem;}
.ch-row::before{content:'';position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--accent);opacity:0;transition:opacity .16s ease;}
.ch-row:hover{border-color:var(--accent);box-shadow:0 8px 22px rgba(0,0,0,.08);transform:translateX(3px);}
.ch-row:hover::before{opacity:1;}
.ch-ico{flex:0 0 46px;height:46px;border-radius:13px;background:var(--accent-soft);display:flex;align-items:center;justify-content:center;font-size:1.3rem;line-height:1;font-family:'Rajdhani',sans-serif;font-weight:700;color:var(--accent);}
.ch-body{flex:1 1 auto;min-width:0;}
.ch-name{display:block;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.06rem;color:#1A202C;line-height:1.3;}
.ch-meta{display:block;font-size:.79rem;color:#718096;margin-top:.1rem;}
.ch-meta b{font-weight:800;color:var(--accent);}
.ch-ex{display:inline-flex;flex-wrap:wrap;gap:.25rem;margin-top:.3rem;}
.ch-ex i{font-style:normal;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.68rem;letter-spacing:.4px;color:#4A5568;background:#F7FAFC;border:1px solid #E2E8F0;border-radius:6px;padding:.12rem .42rem;}
.ch-count{flex:0 0 auto;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.8rem;color:#718096;white-space:nowrap;min-width:64px;text-align:right;}
.ch-count .ch-n{font-size:1.15rem;font-weight:800;color:var(--accent);}
.ch-count.soon{color:#B45309;background:#FFF7ED;border:1px solid #FED7AA;border-radius:100px;padding:.2rem .65rem;font-size:.75rem;min-width:0;}
.ch-cta{flex:0 0 auto;display:inline-flex;align-items:center;gap:.4rem;padding:.5rem 1.1rem;border-radius:100px;background:linear-gradient(135deg,var(--accent),var(--accent-dark));color:#fff;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.86rem;letter-spacing:.4px;white-space:nowrap;box-shadow:0 3px 10px var(--accent-shadow);}
.ch-cta em{font-style:normal;font-size:1rem;line-height:1;transition:transform .16s ease;}
.ch-row:hover .ch-cta em{transform:translateX(3px);}
.ch-item.is-soon .ch-row{opacity:.85;pointer-events:none;}
.ch-item.is-soon .ch-ico{filter:grayscale(1);background:#F1F5F9;color:#94A3B8;}
.ch-item.is-soon .ch-cta{display:none;}
.ch-exp{position:absolute;right:.8rem;top:50%;transform:translateY(-50%);width:34px;height:34px;display:flex;align-items:center;justify-content:center;background:var(--accent-soft);border:none;border-radius:50%;cursor:pointer;color:var(--accent);font-size:.8rem;transition:background .15s;}
.ch-exp:hover,.ch-exp[aria-expanded="true"]{background:var(--accent);color:#fff;}
.ch-exp span{display:block;transition:transform .2s ease;line-height:1;}
.ch-exp[aria-expanded="true"] span{transform:rotate(180deg);}
.ch-panel{margin:.55rem 0 .2rem;padding:1rem 1.1rem;background:#fff;border:1px solid var(--accent);border-radius:14px;box-shadow:0 10px 26px rgba(0,0,0,.08);}
.ch-panel[hidden]{display:none;}
.cp-h{display:flex;align-items:center;gap:.5rem;margin-bottom:.55rem;flex-wrap:wrap;}
.cp-b{font-family:'Rajdhani',sans-serif;font-weight:800;font-size:.72rem;letter-spacing:.8px;text-transform:uppercase;color:#fff;background:var(--accent);border-radius:100px;padding:.16rem .6rem;}
.cp-t{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.9rem;color:#2D3748;}
.cp-c{font-size:.78rem;color:#A0AEC0;}
@media(max-width:700px){
  .ch-cta{padding:.42rem .8rem;font-size:.8rem;gap:.3rem;}
  .ch-row{padding:.7rem 3.1rem .7rem .8rem;gap:.7rem;}
  .ch-row.no-exp{padding-right:.85rem;}
  .ch-ico{flex-basis:40px;height:40px;font-size:1.12rem;border-radius:11px;}
  .ch-name{font-size:1rem;}
  .ch-count{min-width:0;font-size:.72rem;}.ch-count .ch-n{font-size:.98rem;}
  .ch-exp{right:.55rem;width:30px;height:30px;font-size:.72rem;}
  .ch-ex{display:none;}
}
@media(max-width:400px){.ch-cta span{display:none;}.ch-cta{padding:.45rem .62rem;}}
/* test tiles */
.test-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.65rem;}
.tt{display:flex;flex-direction:column;align-items:center;gap:.3rem;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:.8rem .6rem;transition:transform .15s ease,box-shadow .15s ease,border-color .15s ease,background .15s ease;}
.tt:hover{background:#fff;border-color:var(--accent);transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,0,0,.09);}
.tt-n{font-family:'Rajdhani',sans-serif;font-weight:800;font-size:1rem;color:#1A202C;}
.tt-q{font-size:.74rem;color:#718096;margin-bottom:.3rem;}
.tt-go{display:block;width:100%;text-align:center;padding:.4rem;border-radius:100px;background:linear-gradient(135deg,var(--accent),var(--accent-dark));color:#fff;text-decoration:none;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.8rem;letter-spacing:.3px;margin-top:.25rem;}
.tt-go:hover{opacity:.92;}
.tt-go.tt-hi{background:#fff;color:var(--accent);border:1.5px solid var(--accent);}
.tt.is-done{background:#FFFBEB;border-color:#FCD34D;}
.tt-done{font-size:.68rem;font-family:'Rajdhani',sans-serif;font-weight:800;letter-spacing:.3px;color:#92400E;background:#FDE68A;border-radius:100px;padding:.08rem .55rem;margin-bottom:.18rem;}
.tt-go.is-re{background:linear-gradient(135deg,#F59E0B,#D97706);color:#fff;}
.tt-go.tt-hi.is-re{background:#fff;color:#B45309;border-color:#F59E0B;}
.tt-rev{display:block;width:100%;text-align:center;margin-top:.32rem;font-size:.72rem;font-family:'Rajdhani',sans-serif;font-weight:700;color:#0F766E;text-decoration:none;}
.tt-rev:hover{text-decoration:underline;}
.waiting{font-size:.84rem;color:#718096;margin-top:.6rem;}
/* tables, faq, link rows */
.tbl-wrap{overflow-x:auto;background:#fff;border:1px solid #E2E8F0;border-radius:12px;}
table{width:100%;border-collapse:collapse;font-size:.92rem;min-width:420px;}
th{background:#F7FAFC;text-align:left;padding:.7rem .9rem;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.85rem;letter-spacing:.4px;text-transform:uppercase;color:#4A5568;border-bottom:1px solid #E2E8F0;}
td{padding:.65rem .9rem;border-bottom:1px solid #EDF2F7;color:#2D3748;}
tr:last-child td{border-bottom:none;}
td.num{font-weight:700;color:var(--accent);white-space:nowrap;}
.faq{background:#fff;border:1px solid #E2E8F0;border-radius:12px;overflow:hidden;}
.faq details{border-bottom:1px solid #EDF2F7;}.faq details:last-child{border-bottom:none;}
.faq summary{cursor:pointer;padding:.9rem 1.1rem;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1rem;color:#1A202C;list-style:none;}
.faq summary::-webkit-details-marker{display:none;}
.faq summary::before{content:'+';color:var(--accent);font-weight:800;margin-right:.6rem;}
.faq details[open] summary::before{content:'–';}
.faq .ans{padding:0 1.1rem 1rem 2.2rem;font-size:.94rem;color:#4A5568;}
.link-row{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:.8rem;}
.link-row a{display:block;background:#fff;border:1px solid #E2E8F0;border-radius:12px;padding:.85rem 1rem;text-decoration:none;font-family:'Rajdhani',sans-serif;font-weight:700;color:#2D3748;font-size:.95rem;}
.link-row a:hover{border-color:var(--accent);color:var(--accent);}
.link-row span{display:block;font-family:'Hind',sans-serif;font-weight:400;font-size:.8rem;color:#718096;}
.hidden{display:none!important;}
footer{background:#1A202C;color:#A0AEC0;padding:1.8rem 0;margin-top:2rem;font-size:.88rem;}
footer a{color:#CBD5E0;text-decoration:none;margin-right:1rem;}footer a:hover{color:#FF6B00;}
@media(max-width:640px){.wrap{padding:0 .9rem;}h1{font-size:1.42rem;}h2{font-size:1.22rem;}.hero{padding:1.2rem 1rem;border-radius:15px;}.hero .lede{font-size:.93rem;}.chip{font-size:.76rem;padding:.3rem .7rem;}.ch-name{font-size:.95rem;}.ch-meta{font-size:.73rem;}.faq summary{font-size:.94rem;padding:.8rem .9rem;}.faq .ans{font-size:.88rem;padding:0 .9rem .9rem 1.9rem;}section{margin-bottom:1.8rem;}}
@media(prefers-reduced-motion:reduce){.ch-row,.ch-cta em,.tt,.ch-exp span{transition:none;}.ch-row:hover,.tt:hover{transform:none;}}
"""

# attempted / review state on test tiles — one small REST read of the student's attempts, cached 10 min
ATTEMPT_JS = """
<script>
window.tsscPaintAttempts=async function(user){
  const KEY='tsscPyqChAtt:all:'+user.uid, TTL=10*60*1000;
  let rows=null; try{ const c=JSON.parse(localStorage.getItem(KEY)||'null'); if(c&&(Date.now()-c.t)<TTL) rows=c.r; }catch(e){}
  if(!rows){
    let token=''; try{ token=await user.getIdToken(); }catch(e){}
    const headers={'Content-Type':'application/json'}; if(token) headers['Authorization']='Bearer '+token;
    const body={structuredQuery:{from:[{collectionId:'attempts'}],
      where:{compositeFilter:{op:'AND',filters:[{fieldFilter:{field:{fieldPath:'uid'},op:'EQUAL',value:{stringValue:user.uid}}},{fieldFilter:{field:{fieldPath:'type'},op:'EQUAL',value:{stringValue:'pyq-chapter'}}}]}},
      select:{fields:[{fieldPath:'exam'},{fieldPath:'tier'},{fieldPath:'chapterId'},{fieldPath:'testNum'},{fieldPath:'language'},{fieldPath:'analyticsV'}]},limit:1000}};
    try{
      const r=await fetch('https://firestore.googleapis.com/v1/projects/trickyssc-17bb3/databases/(default)/documents:runQuery?key=AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA',{method:'POST',headers,body:JSON.stringify(body)});
      if(!r.ok) return; const j=await r.json(); rows=[];
      (j||[]).forEach(x=>{ const d=x&&x.document; if(!d||!d.fields) return; const f=d.fields, v=k=>f[k]&&(f[k].stringValue||f[k].integerValue||'');
        rows.push({id:d.name.split('/').pop(),exam:v('exam'),tier:v('tier'),ch:v('chapterId'),tn:parseInt(v('testNum'))||0,lang:v('language')==='hi'?'hi':'en',rev:!!f.analyticsV}); });
      try{ localStorage.setItem(KEY,JSON.stringify({t:Date.now(),r:rows})); }catch(e){}
    }catch(e){ return; }
  }
  rows.forEach(a=>{
    document.querySelectorAll('.tt[data-ch="'+a.ch+'"][data-n="'+a.tn+'"]').forEach(t=>{
      t.classList.add('is-done');
      if(!t.querySelector('.tt-done')){ const b=document.createElement('span'); b.className='tt-done'; b.textContent='\\u2713 ATTEMPTED'; t.insertBefore(b, t.querySelector('.tt-q')); }
      const go=t.querySelector('.tt-go[data-lang="'+a.lang+'"]'); if(go){ go.classList.add('is-re'); go.innerHTML=(a.lang==='hi'?'\\u0926\\u094b\\u092c\\u093e\\u0930\\u093e':'Re-attempt')+' &rarr;'; }
      if(a.rev && !t.querySelector('a.tt-rev')){ const l=document.createElement('a'); l.className='tt-rev'; l.innerHTML='\\uD83D\\uDCC4 Review solutions &rarr;'; l.href=t.getAttribute('data-href')+'&lang='+a.lang+'&review='+encodeURIComponent(a.id); t.appendChild(l); }
    });
  });
};
</script>
"""

TOGGLE_JS = """
<script>
document.addEventListener('click',function(e){
  var b=e.target.closest('.ch-exp'); if(!b) return;
  var p=b.closest('.ch-item').querySelector('.ch-panel'); var open=b.getAttribute('aria-expanded')==='true';
  b.setAttribute('aria-expanded',open?'false':'true'); if(open) p.setAttribute('hidden',''); else p.removeAttribute('hidden');
});
</script>
"""

NAV_EXAMS = [("ssc-cgl", "SSC CGL"), ("ssc-chsl", "SSC CHSL"), ("ssc-gd", "SSC GD")]
def nav():
    return f"""<nav class="nav"><div class="nav-inner">
  <a class="logo" href="/index.html">Tricky<span>SSC</span></a>
  <div class="nav-links">
    <a href="/index.html">Home</a>
    <a href="/{HUB}" class="on">Chapter-wise PYQ</a>
    {''.join(f'<a href="/{EXAMS[e]["hub"]}">{n} PYQ</a>' for e, n in NAV_EXAMS)}
    <a href="/ssc-cgl-chapterwise.html">Chapter Tests</a>
    <a href="/ssc-cgl-mock-test.html">Mock Tests</a>
  </div>
  <div class="nav-acct" id="navAccount"><a class="nav-cta" href="/login.html" onclick="tsscStashReturn&amp;&amp;tsscStashReturn()">👤 Login</a></div>
</div></nav>"""

def foot(index):
    links = [f'<a href="/index.html">Home</a>', f'<a href="/{HUB}">Chapter-wise PYQ</a>']
    links += [f'<a href="/{subject_file(s)}">{E(subj_short(s))} PYQ</a>' for s in sorted(index, key=lambda s: SUBJECTS[s][4])]
    links += [f'<a href="/{EXAMS[e]["hub"]}">{n} PYQ</a>' for e, n in NAV_EXAMS]
    return f"""<footer><div class="wrap">{''.join(links)}
<p style="margin-top:.9rem;font-size:.82rem;">&copy; {dt.date.today().year} TrickySSC — free SSC previous year questions, chapter-wise, for every SSC exam. Chapter-wise PYQ tests are rebuilt automatically from the papers on this site; a new paper adds new tests at the end of its chapters.</p></div></footer>"""

def page(title, desc, canonical, body, index, subj=None, extra_head="", extra_js=""):
    root = f"<style>:root{{{accent_css(subj)}}}</style>" if subj else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{SITE}/{canonical}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:site_name" content="TrickySSC"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{SITE}/{canonical}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Baloo+2:wght@400;600;700;800&family=Hind:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="/favicon.png">
{extra_head}
<style>{CSS}</style>{root}
</head>
<body data-exam="{PLAYER_EXAM}">
{nav()}
<div class="wrap">
{body}
</div>
{foot(index)}
{ACCOUNT_JS}{TOGGLE_JS}{extra_js}
</body>
</html>
"""

def crumbs(items):
    return '<div class="breadcrumb">' + " / ".join(f'<a href="{h}">{t}</a>' if h else f"<span>{t}</span>" for t, h in items) + "</div>"

FREE = """<div class="cw-free" role="note"><span class="cw-free-tag">100% FREE</span><span class="cw-free-txt">All chapter-wise PYQ tests are completely free &mdash; every chapter, every test, in English &amp; हिंदी.<small>No pass or payment needed. Just sign in and start practising. <span lang="hi">सभी चैप्टर-वाइज़ PYQ टेस्ट बिल्कुल फ्री हैं।</span></small></span></div>"""

def hero(h1, lede, chips, icon=None):
    top = f'<div class="hero-top"><div class="hero-ic" aria-hidden="true">{icon}</div><h1>{h1}</h1></div>' if icon else f"<h1>{h1}</h1>"
    return f"""<header class="hero">{top}<p class="lede">{lede}</p>
<div class="chips">{''.join(f'<span class="chip">{c}</span>' for c in chips if c)}</div>{FREE}</header>"""

def test_href(cid, n): return f"/pyq-chapter-test.html?exam={PLAYER_EXAM}&tier={PLAYER_TIER}&chapter={cid}&test={n}"

def tiles(ch):
    cid = ch["id"]; out = []
    for i in range(1, ch["tests"] + 1):
        h = test_href(cid, i); nq = SET_SIZE if (i < ch["tests"] or ch["count"] >= SET_SIZE * ch["tests"]) else ch["count"]
        en = f'<a class="tt-go" data-lang="en" href="{h}&lang=en">English &rarr;</a>' if ch["en"] else ""
        hi = f'<a class="tt-go tt-hi" data-lang="hi" href="{h}&lang=hi">हिंदी &rarr;</a>' if ch["hi"] else ""
        out.append(f'<div class="tt" data-ch="{cid}" data-n="{i}" data-href="{h}"><span class="tt-n">Test {i}</span><span class="tt-q">{nq} questions</span>{en}{hi}</div>')
    return '<div class="test-grid">' + "".join(out) + "</div>"

def exam_tags(exams):
    return '<span class="ch-ex">' + "".join(f"<i>{E(short_name(e))} {n}</i>" for e, n in exams.items()) + "</span>"

def chapter_row(ch):
    cid = ch["id"]; live = ch["tests"] > 0
    yrs = (f"{ch['years'][0]}–{ch['years'][-1]}" if len(ch["years"]) > 1 else (ch["years"][0] if ch["years"] else ""))
    meta = f"<b>{ch['count']}</b> PYQs" + (f" · {yrs} papers" if yrs else "") + (f" · +{ch['waiting']} waiting for the next test" if live and ch["waiting"] else "")
    count = f'<span class="ch-count"><span class="ch-n">{ch["tests"]}</span> test{"s" if ch["tests"] != 1 else ""}</span>' if live else f'<span class="ch-count soon">Collecting · {ch["count"]}/{MIN_FIRST_SET}</span>'
    panel = (f'<div class="ch-panel" hidden><div class="cp-h"><span class="cp-b">PYQ</span><span class="cp-t">{E(ch["name"])} — {ch["tests"]} test{"s" if ch["tests"] != 1 else ""}</span><span class="cp-c">{SET_SIZE} questions each · paper order · {E(exams_line(ch["exams"]))}</span></div>{tiles(ch)}</div>') if live else ""
    exp = '<button class="ch-exp" type="button" aria-expanded="false" aria-label="Show tests"><span>&#9662;</span></button>' if live else ""
    return f"""<li class="ch-item{'' if live else ' is-soon'}" data-name="{E(ch['name']).lower()}">
<div class="ch-top"><a class="ch-row{'' if live else ' no-exp'}" href="/{chapter_file(cid)}">
<span class="ch-ico" aria-hidden="true">{icon_of(cid)}</span>
<span class="ch-body"><span class="ch-name">{E(ch['name'])}</span><span class="ch-meta">{meta}</span>{exam_tags(ch['exams'])}</span>
{count}<span class="ch-cta"><span>Practice</span><em>&rarr;</em></span></a>{exp}</div>{panel}</li>"""

def exam_strip(exams):
    return "".join(f'<span class="chip"><b>{E(v["name"])}</b> {v["papers"]} papers · {v["questions"]} PYQs</span>' for e, v in sorted(exams.items(), key=lambda kv: (EXAM_ORDER.index(kv[0]) if kv[0] in EXAM_ORDER else 99, kv[0])))

def all_subjects(index):
    return sorted(index, key=lambda s: SUBJECTS[s][4])

def subj_totals(chs):
    by_exam = {}
    for c in chs:
        for e, n in c["exams"].items(): by_exam[e] = by_exam.get(e, 0) + n
    by_exam = dict(sorted(by_exam.items(), key=lambda kv: (EXAM_ORDER.index(kv[0]) if kv[0] in EXAM_ORDER else 99, kv[0])))
    return sum(c["count"] for c in chs), sum(c["tests"] for c in chs), sum(1 for c in chs if c["tests"]), by_exam

def gen_subject_page(index, exams, subj):
    short = subj_short(subj); chs = index[subj]
    total_q, total_t, n_ch, by_exam = subj_totals(chs)
    top = sorted(chs, key=lambda c: -c["count"])[:8]
    table = "".join(f'<tr><td><a href="/{chapter_file(c["id"])}">{E(c["name"])}</a></td><td class="num">{c["count"]}</td><td>{E(exams_line(c["exams"]))}</td><td class="num">{c["tests"]}</td></tr>' for c in top)
    body = crumbs([("Home", "/index.html"), ("Chapter-wise PYQ", "/" + HUB), (short, "")])
    body += hero(f"SSC {E(short)} Previous Year Questions Chapter Wise — {E(exams_line(by_exam, ' · '))}",
                 f"Pick a {E(short)} chapter and practise the real questions SSC asked in {E(exams_sentence(by_exam))} papers — 25 at a time, with full solutions and the exam, date and shift under every question, in English or हिंदी.",
                 [f"<b>{n_ch}</b> Chapters live", f"<b>{total_t}</b> Tests", f"<b>{total_q}</b> PYQs", f"<b>{SET_SIZE}</b> Questions per Test", "English &amp; <b>हिंदी</b>"] + [f"<b>{E(short_name(e))}</b> {n}" for e, n in by_exam.items()],
                 SUBJ_ICON.get(subj))
    body += f"""<main>
<section id="chapters">
<h2>All {len(chs)} SSC {E(short)} Chapters — Pick a Chapter to Practice</h2>
<p>Every chapter below holds that chapter's previous year questions from every SSC exam on TrickySSC. Tap <b>Practice</b> for the chapter page, or the arrow to open its tests right here.</p>
<div class="types-card"><div class="tc-ico" aria-hidden="true">🎯</div><div class="tc-body"><div class="tc-title">Real questions. Every SSC exam. One chapter at a time.</div><div class="tc-sub">Not model questions — these are the actual {E(short)} questions from {E(exams_sentence(by_exam))} papers, sorted by chapter and cut into {SET_SIZE}-question tests. The count beside each chapter grows automatically as new papers are uploaded.</div></div></div>
<div class="search">🔍 <input placeholder="Search a chapter…" oninput="var v=this.value.toLowerCase();document.querySelectorAll('.ch-item').forEach(function(c){{c.classList.toggle('hidden',v&&c.getAttribute('data-name').indexOf(v)<0)}})"></div>
<div class="subj-nav">{''.join(f'<a href="/{subject_file(s)}">{E(subj_short(s))}</a>' for s in all_subjects(index) if s != subj)}</div>
<ol class="ch-list">{''.join(chapter_row(c) for c in chs)}</ol>
</section>
<section id="weightage"><h2>Which {E(short)} chapters does SSC ask most?</h2><p>Counted across every SSC exam paper on this site — use it to decide where to spend your time first.</p>
<div class="tbl-wrap"><table><thead><tr><th>Chapter</th><th>PYQs</th><th>By exam</th><th>Tests</th></tr></thead><tbody>{table}</tbody></table></div></section>
<section id="how"><h2>How these tests work</h2>
<p>Every question here was asked in a real SSC paper — {E(exams_sentence(by_exam))}. A chapter's questions from all exams sit together in paper order: Test 1 holds the oldest papers, the last test the newest. When a new paper of any exam is uploaded and tagged, its questions join the end of the chapter and a new test appears once {SET_SIZE} have collected, so tests you have already attempted never change.</p>
<p>Tests run with an optional 15-minute timer, carry +2 / −0.5 marking like the chapter tests, and show a step-by-step solution for every question in English and Hindi. Attempted tests are marked and keep a Review link.</p></section>
<section id="more"><h2>More free practice</h2><div class="link-row">
<a href="/{HUB}">All chapter-wise PYQ subjects<span>{E(', '.join(subj_short(s) for s in all_subjects(index)))}</span></a>
{''.join(f'<a href="/{EXAMS[e]["hub"]}">{n} previous year papers<span>Full shift-wise papers with solutions</span></a>' for e, n in NAV_EXAMS)}
<a href="/ssc-cgl-chapterwise.html">SSC CGL chapter-wise tests<span>Model questions, two levels, 25 per test</span></a></div></section>
</main>"""
    title = f"SSC {short} PYQ Chapter Wise — {total_q} Previous Year Questions ({exams_line(by_exam, ', ')}) in {n_ch} Chapters | TrickySSC"
    desc = f"Free SSC {short} previous year questions chapter wise from {exams_sentence(by_exam)} papers: {total_q} PYQs in {total_t} tests of {SET_SIZE}, English and Hindi, with the exam, paper and shift under every question."
    return page(title, desc, subject_file(subj), body, index, subj=subj, extra_js=ATTEMPT_JS)

def gen_hub(index, counts, exams):
    rows = []
    for s in all_subjects(index):
        chs = index[s]; total_q, total_t, n_ch, by_exam = subj_totals(chs)
        top = ", ".join(c["name"].split(" (")[0] for c in chs[:4])
        rows.append(f"""<li class="ch-item" style="{accent_css(s)}"><div class="ch-top"><a class="ch-row no-exp" href="/{subject_file(s)}">
<span class="ch-ico" aria-hidden="true">{SUBJ_ICON.get(s, '📘')}</span>
<span class="ch-body"><span class="ch-name">{E(subj_label(s))}</span><span class="ch-meta"><b>{n_ch}</b> chapters · <b>{total_q}</b> PYQs · most asked: {E(top)}</span>{exam_tags(by_exam)}</span>
<span class="ch-count"><span class="ch-n">{total_t}</span> tests</span><span class="ch-cta"><span>Open chapters</span><em>&rarr;</em></span></a></div></li>""")
    tot_q = sum(c["count"] for v in index.values() for c in v); tot_t = sum(c["tests"] for v in index.values() for c in v); tot_c = sum(1 for v in index.values() for c in v if c["tests"])
    names = exams_sentence(exams)
    body = crumbs([("Home", "/index.html"), ("Chapter-wise PYQ", "")])
    body += hero("SSC Exams Chapter-wise Previous Year Questions — Free PYQ Tests in English &amp; हिंदी",
                 f"Every question from the {counts['papers']} {E(names)} papers on TrickySSC, sorted by chapter. One chapter page holds that chapter's questions from every SSC exam — practise exactly what SSC has asked, {SET_SIZE} questions at a time, with the exam, paper and shift under every question.",
                 [f"<b>{counts['papers']}</b> Papers", f"<b>{tot_q}</b> PYQs", f"<b>{tot_c}</b> Chapters", f"<b>{tot_t}</b> Tests", "English &amp; <b>हिंदी</b>"], "📌")
    body += f"""<main>
<section id="subjects"><h2>Choose a subject</h2><p>Each subject page lists every chapter with its tests. Attempted tests are marked and keep a Review link.</p>
<div class="chips" style="margin:0 0 1rem">{exam_strip(exams)}</div>
<ol class="ch-list">{''.join(rows)}</ol></section>
<section id="why"><h2>Why chapter-wise PYQs across all SSC exams?</h2>
<p>Solving a full paper tells you your score. Solving the same questions chapter-wise tells you <b>which chapters</b> cost you marks — and shows the exact patterns SSC repeats year after year. CGL, CHSL, GD, MTS and CPO are set by the same commission from the same syllabus, so a chapter's questions from every exam together give you the complete picture of how it is asked. These tests are built only from real previous-year questions, so the difficulty is the real difficulty.</p>
<p>Questions are added automatically whenever a new paper of any SSC exam is uploaded to TrickySSC. Each chapter's tests are fixed in paper order, so Test 3 is always the same Test 3 — new questions open a new test at the end.</p></section>
<section id="faq"><h2>Frequently asked questions</h2><div class="faq">
<details><summary>Are the questions really from previous SSC papers?</summary><div class="ans">Yes. Every question comes from a {E(names)} paper hosted on TrickySSC, and the exam, date and shift are shown under the question in the test.</div></details>
<details><summary>Why are CGL, CHSL and GD questions together in one test?</summary><div class="ans">The chapter is the same; only the exam differs. Seeing every way SSC has asked a chapter — across exams and years — is the fastest way to master it. The label under each question tells you which exam and shift it came from.</div></details>
<details><summary>How many questions are in one test?</summary><div class="ans">{SET_SIZE}. A new chapter shows its first test once {MIN_FIRST_SET} questions have been tagged; that test grows to {SET_SIZE}, after which every further test is a full {SET_SIZE}.</div></details>
<details><summary>Can I take the tests in Hindi?</summary><div class="ans">Yes — the हिंदी button opens the same test in Hindi wherever the Hindi paper is available, with a View in English toggle on every question.</div></details>
<details><summary>Is there negative marking?</summary><div class="ans">Tests use +2 for a correct answer and −0.5 for a wrong one, like the chapter tests. Unattempted questions score zero.</div></details>
</div></section>
<section id="more"><h2>More free SSC practice</h2><div class="link-row">
{''.join(f'<a href="/{EXAMS[e]["hub"]}">{n} previous year papers<span>Full shift-wise papers with solutions</span></a>' for e, n in NAV_EXAMS)}
<a href="/ssc-cgl-chapterwise.html">SSC CGL chapter-wise tests<span>Model questions in two levels</span></a>
<a href="/ssc-cgl-mock-test.html">SSC CGL mock tests<span>Full-length, real sectional timing</span></a>
<a href="/ssc-chsl-mock-test.html">SSC CHSL mock tests<span>Tier I + Tier II, ₹49 a year</span></a></div></section>
</main>"""
    title = f"SSC Chapter-wise PYQ {dt.date.today().year} — {tot_q} Previous Year Questions of CGL, CHSL, GD by Chapter, Free Tests | TrickySSC"
    desc = f"Free SSC chapter-wise previous year questions: {tot_q} PYQs from {counts['papers']} {names} papers in {tot_c} chapters, {SET_SIZE}-question tests in English and Hindi with solutions. One chapter, every SSC exam."
    return page(title, desc, HUB, body, index)

def gen_chapter_page(index, ch):
    subj = ch["subject"]; short = subj_short(subj); name = ch["name"]; ex = ch["exams"]; names = exams_sentence(ex)
    years = ch["years"]; yr = f"{years[0]}–{years[-1]}" if len(years) > 1 else (years[0] if years else "")
    wait = f'<div class="waiting">+{ch["waiting"]} more questions collected — the next test opens at {SET_SIZE}.</div>' if ch["waiting"] else ""
    siblings = [c for c in index[subj] if c["id"] != ch["id"] and c["tests"]][:12]
    sib = "".join(f'<a href="/{chapter_file(c["id"])}">{icon_of(c["id"])} {E(c["name"])}<span>{c["count"]} PYQs · {c["tests"]} tests</span></a>' for c in siblings)
    exam_rows = "".join(f'<tr><td>{E(exam_name(e))}</td><td class="num">{n}</td><td><a href="/{exam_meta(e)["hub"]}">{E(exam_name(e))} papers</a></td></tr>' for e, n in ex.items())
    body = crumbs([("Home", "/index.html"), ("Chapter-wise PYQ", "/" + HUB), (short, "/" + subject_file(subj)), (name, "")])
    body += hero(f"{E(name)} Previous Year Questions {yr} — SSC {E(exams_line(ex, ' · '))}",
                 f"{ch['count']} real SSC questions on {E(name)} from the {E(names)} {yr} papers, served as {SET_SIZE}-question tests. Every question shows the exam, paper and shift it came from, and has a step-by-step solution in English and हिंदी.",
                 [f"<b>{ch['count']}</b> PYQs", f"<b>{ch['tests']}</b> Tests", f"<b>{SET_SIZE}</b> Questions per Test", f"<b>{yr}</b> Papers" if yr else "", "English &amp; <b>हिंदी</b>"] + [f"<b>{E(short_name(e))}</b> {n}" for e, n in ex.items()],
                 icon_of(ch["id"]))
    body += f"""<main>
<section id="tests"><h2>{E(name)} Tests — Pick a Test and Start</h2>
<p>Tests are in paper order: Test 1 has the oldest papers, the last test the newest. Attempted tests are marked and keep a Review link.</p>
{tiles(ch)}{wait}</section>
<section id="about"><h2>About these {E(name)} questions</h2>
<p>These are the actual {E(name)} questions SSC asked in the {E(names)} {yr} papers on TrickySSC — not model questions. Questions from every exam sit together in paper order, and a new test opens at the end whenever {SET_SIZE} more questions are tagged from a newly uploaded paper of any SSC exam, so the tests you have attempted never change.</p>
<div class="tbl-wrap"><table><thead><tr><th>Exam</th><th>{E(name)} PYQs</th><th>Full papers</th></tr></thead><tbody>{exam_rows}</tbody></table></div>
<p style="margin-top:.9rem">Use the हिंदी button for the Hindi paper's wording, and the View in English toggle inside the test to compare. After submitting, the review shows every solution, your time per question and where you stand on the leaderboard for that test.</p></section>
<section id="related"><h2>Other {E(short)} chapters</h2><div class="link-row">{sib}<a href="/{subject_file(subj)}">All {E(short)} chapters<span>Full chapter list with PYQ counts</span></a></div></section>
<section id="more"><h2>More free practice</h2><div class="link-row">
<a href="/{HUB}">Chapter-wise PYQ — all subjects<span>Every chapter, every SSC exam</span></a>
{''.join(f'<a href="/{EXAMS[e]["hub"]}">{n} previous year papers<span>Full shift-wise papers</span></a>' for e, n in NAV_EXAMS)}
<a href="/ssc-cgl-mock-test.html">SSC CGL mock tests<span>Full-length, real sectional timing</span></a></div></section>
</main>"""
    title = f"{name} PYQ {yr} — {ch['count']} SSC Previous Year Questions ({exams_line(ex, ', ')}), Chapter Wise Tests | TrickySSC"
    desc = f"Practise {ch['count']} real SSC {name} previous year questions from {names} ({yr}) as {SET_SIZE}-question tests, in English and Hindi, with solutions and the exam, paper and shift under every question."
    ld = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/index.html"},
        {"@type": "ListItem", "position": 2, "name": "Chapter-wise PYQ", "item": f"{SITE}/{HUB}"},
        {"@type": "ListItem", "position": 3, "name": short, "item": f"{SITE}/{subject_file(subj)}"},
        {"@type": "ListItem", "position": 4, "name": name, "item": f"{SITE}/{chapter_file(ch['id'])}"}]}, ensure_ascii=False)
    return page(title, desc, chapter_file(ch["id"]), body, index, subj=subj, extra_head=f'<script type="application/ld+json">{ld}</script>', extra_js=ATTEMPT_JS)

def write_if_changed(path, txt):
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if old != txt:
        open(path, "w", encoding="utf-8").write(txt); return True
    return False

def gen_pages(index, counts, exams):
    files = [HUB]; write_if_changed(os.path.join(ROOT, HUB), gen_hub(index, counts, exams))
    for s in all_subjects(index):
        files.append(subject_file(s)); write_if_changed(os.path.join(ROOT, subject_file(s)), gen_subject_page(index, exams, s))
    for s, chs in index.items():
        for c in chs:
            if not c["tests"]: continue
            files.append(chapter_file(c["id"]))
            write_if_changed(os.path.join(ROOT, chapter_file(c["id"])), gen_chapter_page(index, c))
    return files

def update_sitemap(all_files):
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path): return
    s = open(path, encoding="utf-8").read()
    block = "<!-- PYQCH:START (generated by scripts/build_pyq_chapters.py — do not edit by hand) -->\n" + "".join(
        f"  <url>\n    <loc>{SITE}/{f}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{'0.8' if f == HUB or 'chapter-wise-pyq' in f else '0.6'}</priority>\n  </url>\n" for f in all_files) + "<!-- PYQCH:END -->\n"
    if "<!-- PYQCH:START" in s:
        s = re.sub(r"<!-- PYQCH:START.*?<!-- PYQCH:END -->\n?", lambda _m: block, s, flags=re.S)
    else:
        s = s.replace("</urlset>", block + "</urlset>")
    write_if_changed(path, s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump", help="directory with papers.json / questions.json (offline build for tests)")
    a = ap.parse_args()
    try:
        if a.dump:
            papers = json.load(open(os.path.join(a.dump, "papers.json"), encoding="utf-8"))
            qs = json.load(open(os.path.join(a.dump, "questions.json"), encoding="utf-8"))
        else:
            papers, qs = fetch_all()
    except Exception as e:
        print(f"could not read Firestore ({e}) — leaving existing files as they are", file=sys.stderr); sys.exit(0)
    if not qs:
        print("no PYQ questions found — nothing built"); return
    index, counts, exams = build_all(papers, qs)
    files = gen_pages(index, counts, exams)
    json.dump(sorted(set(files)), open(os.path.join(OUT, "pages.json"), "w", encoding="utf-8"), indent=0)
    update_sitemap(sorted(set(files)))
    print("done")

if __name__ == "__main__":
    main()
