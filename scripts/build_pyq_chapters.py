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
    print(f"all exams: {counts} · exams {', '.join(f'{e} {v['papers']}p/{v['questions']}q' for e, v in exams.items())} → {sum(len(v) for v in index.values())} chapters, {written} test files changed")
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
CSS = """
:root{--orange:#FF6B00;--orange2:#FF8C38;--bg:#F1F5F9;--card:#fff;--border:#E2E8F0;--green:#00A86B;--gold:#F59E0B;--text:#1A202C;--dim:#4A5568;--muted:#64748B;--ink:#0F172A;--shadow:0 1px 2px rgba(16,24,40,.05)}
*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Hind','Inter',sans-serif;background:var(--bg);color:var(--text);line-height:1.7;-webkit-font-smoothing:antialiased}a{color:inherit;text-decoration:none}
nav{position:sticky;top:0;z-index:1000;background:rgba(255,255,255,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--border)}.nav-inner{max-width:1180px;margin:0 auto;padding:.65rem 1.25rem;display:flex;align-items:center;justify-content:space-between;gap:1rem}
.brand{display:flex;align-items:center;gap:.55rem}.brand-icon{width:38px;height:38px;border-radius:11px;background:linear-gradient(135deg,var(--orange),var(--orange2));display:flex;align-items:center;justify-content:center;font-size:1.15rem;box-shadow:0 4px 16px rgba(255,107,0,.35)}
.brand-name{font-family:'Baloo 2',cursive;font-weight:800;font-size:1.4rem;color:var(--text);line-height:1}.brand-name span{color:var(--orange)}
.nav-links{display:flex;align-items:center;gap:.2rem;list-style:none}.nav-links a{font-family:'Rajdhani',sans-serif;font-weight:600;font-size:.95rem;color:var(--dim);padding:.45rem .9rem;border-radius:100px}.nav-links a:hover{color:var(--orange);background:rgba(255,107,0,.08)}
.nav-cta{background:linear-gradient(135deg,var(--orange),var(--orange2));color:#fff!important;font-weight:700}
.acct{display:flex;align-items:center;gap:.5rem}.acct-chip{display:inline-flex;align-items:center;gap:.5rem;padding:.28rem .75rem .28rem .3rem;border:1px solid var(--border);border-radius:100px;background:#fff}.acct-av{width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,var(--orange),var(--orange2));color:#fff;display:flex;align-items:center;justify-content:center;font-family:'Baloo 2',cursive;font-weight:800;font-size:.85rem;object-fit:cover}
.acct-name{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.92rem;max-width:130px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.acct-out{border:1px solid var(--border);background:#fff;color:var(--muted);border-radius:100px;padding:.35rem .85rem;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.85rem;cursor:pointer}
.nav-toggle{display:none;width:42px;height:42px;border:1px solid var(--border);background:#fff;border-radius:11px;cursor:pointer;align-items:center;justify-content:center}.nav-toggle span,.nav-toggle span::before,.nav-toggle span::after{content:'';display:block;width:19px;height:2px;border-radius:2px;background:var(--dim)}.nav-toggle span{position:relative}.nav-toggle span::before{position:absolute;top:-6px;left:0}.nav-toggle span::after{position:absolute;top:6px;left:0}
@media(max-width:820px){.nav-toggle{display:flex}.nav-links{position:absolute;top:100%;left:0;right:0;flex-direction:column;align-items:stretch;background:#fff;padding:.6rem 1.25rem 1rem;border-bottom:1px solid var(--border);display:none}.nav-links.open{display:flex}.nav-links a{padding:.75rem .9rem}}
.hero{position:relative;overflow:hidden;background:linear-gradient(150deg,#1A202C 0%,#0F172A 55%,#1E3A2F 100%);color:#fff}.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 12% 45%,rgba(255,107,0,.16),transparent 55%),radial-gradient(ellipse at 90% 8%,rgba(0,168,107,.13),transparent 52%)}
.hero-in{position:relative;z-index:1;max-width:1180px;margin:0 auto;padding:1.3rem 1.25rem 1.9rem}.crumb{display:flex;flex-wrap:wrap;gap:.4rem;font-size:.82rem;color:rgba(255,255,255,.55);margin-bottom:1rem}.crumb a{color:rgba(255,255,255,.72)}.crumb .here{color:#fff;font-weight:600}
h1{font-family:'Baloo 2',cursive;font-weight:800;font-size:2rem;line-height:1.15;letter-spacing:-.4px}.hero p.lede{color:rgba(255,255,255,.72);font-size:.98rem;margin-top:.55rem;max-width:720px;line-height:1.6}
.pill-row{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1.1rem}.pill{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.8rem;padding:.38rem .8rem;border-radius:100px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);color:rgba(255,255,255,.85)}.pill b{color:#fff}
.cw-free{display:flex;gap:.7rem;align-items:center;background:rgba(0,168,107,.12);border:1px solid rgba(0,168,107,.35);border-radius:12px;padding:.6rem .9rem;margin-top:1rem;font-size:.86rem;color:#d9fbe9}.cw-free-tag{background:var(--green);color:#fff;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.75rem;padding:.2rem .55rem;border-radius:6px;white-space:nowrap}
.wrap{max-width:1180px;margin:0 auto;padding:1.5rem 1.25rem 3rem}section{margin-bottom:2.2rem}h2{font-family:'Baloo 2',cursive;font-weight:800;font-size:1.45rem;line-height:1.25;margin-bottom:.6rem}h3{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.1rem;margin:1rem 0 .3rem}p{margin-bottom:.8rem;color:var(--dim)}
.tier-label{display:flex;align-items:center;gap:.8rem;margin:1.4rem 0 .8rem}.tier-label .t{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.9rem;color:var(--muted);text-transform:uppercase;letter-spacing:.6px;white-space:nowrap}.tier-label .line{flex:1;height:1px;background:var(--border)}
.subj-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1rem}.sc{position:relative;display:flex;flex-direction:column;background:var(--card);border:1px solid var(--border);border-radius:18px;padding:1.25rem;box-shadow:var(--shadow);border-top:4px solid var(--c)}
.sc-top{display:flex;gap:.8rem;align-items:center;margin-bottom:.7rem}.sc-ic{width:44px;height:44px;border-radius:12px;background:var(--csoft);display:flex;align-items:center;justify-content:center;font-size:1.35rem}.sc-name{font-family:'Baloo 2',cursive;font-weight:800;font-size:1.15rem;line-height:1.2}.sc-sub{font-size:.8rem;color:var(--muted)}
.sc-live{display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem;margin-bottom:.9rem;padding:.7rem .6rem;border-radius:14px;background:var(--csoft)}.sc-stat{text-align:center}.sc-stat b{display:block;font-family:'Baloo 2',cursive;font-weight:800;font-size:1.35rem;color:var(--c);line-height:1.1}.sc-stat span{font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.4px}
.sc-desc{font-size:.88rem;color:var(--dim);flex:1}.sc-btn{display:inline-flex;align-items:center;justify-content:center;gap:.4rem;margin-top:.9rem;padding:.7rem 1rem;border-radius:12px;background:var(--c);color:#fff;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1rem}
.chap-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:.85rem}.chap{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:.95rem 1rem;box-shadow:var(--shadow);border-top:4px solid var(--c)}
.chap-top{display:flex;justify-content:space-between;align-items:flex-start;gap:.5rem;margin-bottom:.5rem}.chap-name{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.05rem;line-height:1.25}.chap-name a:hover{color:var(--c)}.chap-meta{font-size:.78rem;color:var(--muted)}
.qcount{font-family:'Baloo 2',cursive;font-weight:800;font-size:1.25rem;color:var(--c);white-space:nowrap;line-height:1;text-align:right}.qcount small{display:block;font-family:'Hind';font-weight:500;font-size:.68rem;color:var(--muted)}
.tests{display:flex;flex-wrap:wrap;gap:.4rem}.test{display:inline-flex;align-items:center;border:1px solid var(--border);border-radius:9px;overflow:hidden;font-size:.78rem;background:#fff}.test .n{padding:.3rem .55rem;font-family:'Rajdhani',sans-serif;font-weight:700;background:#F8FAFC;border-right:1px solid var(--border);color:var(--ink)}
.test a{padding:.3rem .5rem;color:var(--dim);font-weight:600}.test a+a{border-left:1px solid var(--border)}.test a:hover{background:var(--csoft);color:var(--c)}.test.done .n{background:var(--green);color:#fff;border-color:var(--green)}.test.part .n{background:var(--gold);color:#fff}
.test a.rv{font-size:.72rem;color:var(--muted)}.waiting{font-size:.78rem;color:var(--muted);margin-top:.4rem}.soon{font-size:.82rem;color:var(--muted)}
.legend{display:flex;flex-wrap:wrap;gap:1rem;font-size:.8rem;color:var(--muted);margin:0 0 1rem}.legend i{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-1px;margin-right:.3rem}
.controls{display:flex;flex-wrap:wrap;gap:.7rem;align-items:center;margin-bottom:1rem}.search{flex:1;min-width:220px;display:flex;align-items:center;gap:.5rem;background:#fff;border:1px solid var(--border);border-radius:100px;padding:.45rem .9rem;color:var(--muted);font-size:.9rem}.search input{border:0;outline:0;flex:1;font:inherit;background:transparent}
.subj-nav{display:flex;flex-wrap:wrap;gap:.4rem}.subj-nav a{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.82rem;padding:.3rem .75rem;border-radius:100px;background:#fff;border:1px solid var(--border);color:var(--dim)}
.subject{margin-bottom:1.8rem}.subj-head{display:flex;align-items:center;gap:.7rem;margin-bottom:.7rem}.subj-ic{width:38px;height:38px;border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:1.15rem;background:var(--csoft)}.subj-head h2{margin:0;font-size:1.3rem}.subj-head small{display:block;color:var(--muted);font-size:.82rem}
.faq{background:var(--card);border:1px solid var(--border);border-radius:14px;overflow:hidden;box-shadow:var(--shadow)}.faq details{border-bottom:1px solid var(--border)}.faq details:last-child{border-bottom:0}.faq summary{cursor:pointer;padding:.85rem 1rem;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1rem;list-style:none}.faq summary::-webkit-details-marker{display:none}.faq .ans{padding:0 1rem .9rem;color:var(--dim);font-size:.92rem}
.link-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:.8rem}.link-row a{display:block;background:var(--card);border:1px solid var(--border);border-radius:14px;padding:.95rem 1.1rem;font-family:'Rajdhani',sans-serif;font-weight:700;color:var(--text);font-size:.98rem;box-shadow:var(--shadow)}.link-row a span{display:block;font-family:'Hind';font-weight:400;font-size:.82rem;color:var(--muted);margin-top:.15rem}
.tbl{width:100%;border-collapse:collapse;font-size:.9rem;background:#fff;border:1px solid var(--border);border-radius:14px;overflow:hidden}.tbl th,.tbl td{padding:.55rem .8rem;border-bottom:1px solid var(--border);text-align:left}.tbl th{background:#F8FAFC;font-family:'Rajdhani',sans-serif;font-size:.8rem;text-transform:uppercase;letter-spacing:.4px;color:var(--muted)}
.foot{max-width:1180px;margin:0 auto;padding:1.5rem 1.25rem 2.5rem;font-size:.82rem;color:var(--muted)}.foot .fl{display:flex;flex-wrap:wrap;gap:.4rem 1rem;margin-bottom:.6rem}.foot a{color:var(--dim)}
.hidden{display:none!important}@media(max-width:640px){h1{font-size:1.5rem}.wrap{padding:1rem 1rem 2.5rem}}
"""

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
    document.querySelectorAll('.test[data-ch="'+a.ch+'"][data-n="'+a.tn+'"]').forEach(t=>{
      t.classList.add('done');
      if(a.rev && !t.querySelector('a.rv')){ const l=document.createElement('a'); l.className='rv'; l.textContent='Review'; l.href=t.getAttribute('data-href')+'&lang='+a.lang+'&review='+encodeURIComponent(a.id); t.appendChild(l); }
    });
  });
};
</script>
"""

EXTRA_CSS = """
.xb{display:inline-flex;flex-wrap:wrap;gap:.3rem;margin-top:.3rem}.xb span{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.72rem;letter-spacing:.3px;padding:.12rem .5rem;border-radius:100px;background:#F1F5F9;border:1px solid var(--border);color:var(--dim)}.xb span b{color:var(--ink)}
.exam-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:.7rem;margin-top:1.2rem}.exam-strip a{display:flex;align-items:center;gap:.6rem;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:.55rem .8rem;color:#fff}.exam-strip a b{font-family:'Baloo 2',cursive;font-size:1.05rem;line-height:1.1;display:block}.exam-strip a small{display:block;color:rgba(255,255,255,.65);font-size:.74rem}
.exam-strip a i{font-style:normal;font-size:1.3rem}
"""

NAV_EXAMS = [("ssc-cgl", "SSC CGL"), ("ssc-chsl", "SSC CHSL"), ("ssc-gd", "SSC GD")]
def nav():
    return f"""<nav><div class="nav-inner">
  <a class="brand" href="https://trickyssc.com/index.html" aria-label="TrickySSC home"><span class="brand-icon">⚡</span><span class="brand-name">Tricky<span>SSC</span></span></a>
  <button class="nav-toggle" id="navToggle" aria-label="Toggle menu" aria-expanded="false" onclick="var m=document.getElementById('navLinks');var o=m.classList.toggle('open');this.setAttribute('aria-expanded',o);"><span></span></button>
  <ul class="nav-links" id="navLinks">
    <li><a href="https://trickyssc.com/index.html">Home</a></li>
    <li><a href="https://trickyssc.com/{HUB}">Chapter-wise PYQ</a></li>
    {''.join(f'<li><a href="https://trickyssc.com/{EXAMS[e]["hub"]}">{n} PYQ</a></li>' for e, n in NAV_EXAMS)}
    <li><a href="https://trickyssc.com/ssc-cgl-mock-test.html">Mock Tests</a></li>
    <li id="navAccount"><a class="nav-cta" href="https://trickyssc.com/login.html" onclick="tsscStashReturn&&tsscStashReturn()">👤 Login</a></li>
  </ul></div></nav>"""

def foot(index):
    links = [f'<a href="https://trickyssc.com/index.html">Home</a>', f'<a href="https://trickyssc.com/{HUB}">Chapter-wise PYQ</a>']
    for subj in sorted(index, key=lambda s: SUBJECTS[s][4]):
        links.append(f'<a href="https://trickyssc.com/{subject_file(subj)}">{E(subj_short(subj))} PYQ</a>')
    for e, n in NAV_EXAMS:
        links.append(f'<a href="https://trickyssc.com/{EXAMS[e]["hub"]}">{n} papers</a>')
    return f"""<div class="foot"><div class="fl">{''.join(links)}</div><div>Free SSC exam prep · <a href="https://trickyssc.com/index.html">TrickySSC.com</a></div>
<div style="margin-top:.4rem;">Chapter-wise PYQ tests are rebuilt automatically from the previous-year papers of every SSC exam on this site. New papers add new tests at the end of each chapter.</div></div>"""

def page(title, desc, canonical, body, index, extra_head="", extra_js=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="{SITE}/{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="TrickySSC"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{SITE}/{canonical}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700;800&family=Baloo+2:wght@600;700;800&family=Hind:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="/favicon.png">
{extra_head}
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body data-exam="{PLAYER_EXAM}">
{nav()}
{body}
{foot(index)}
{ACCOUNT_JS}{extra_js}
</body>
</html>
"""

def hero(crumbs, h1, lede, pills, free_line, extra=""):
    c = " <span class=\"sep\">/</span> ".join(crumbs)
    return f"""<header class="hero"><div class="hero-in">
  <div class="crumb">{c}</div>
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
  <div class="pill-row">{''.join(f'<span class="pill">{p}</span>' for p in pills if p)}</div>
  {extra}
  <div class="cw-free" role="note"><span class="cw-free-tag">100% FREE</span><span>{free_line}</span></div>
</div></header>"""

def test_tiles(ch, limit=None):
    cid = ch["id"]; n = ch["tests"]
    out = []
    for i in range(1, n + 1):
        href = f"pyq-chapter-test.html?exam={PLAYER_EXAM}&tier={PLAYER_TIER}&chapter={cid}&test={i}"
        en = f'<a href="{href}&lang=en">EN</a>' if ch["en"] else ""
        hi = f'<a href="{href}&lang=hi">हिंदी</a>' if ch["hi"] else ""
        out.append(f'<span class="test" data-ch="{cid}" data-tier="{PLAYER_TIER}" data-n="{i}" data-href="{href}"><span class="n">T{i}</span>{en}{hi}</span>')
    if limit and n > limit:
        shown = "".join(out[:limit]); more = "".join(out[limit:])
        return f'{shown}<span class="more-wrap hidden">{more}</span><a class="test" href="#" onclick="this.previousElementSibling.classList.remove(\'hidden\');this.remove();return false;" style="padding:.3rem .55rem;color:var(--muted)">+{n-limit} more ▾</a>'
    return "".join(out)

def exam_badges(exams):
    return '<div class="xb">' + "".join(f'<span><b>{E(short_name(e))}</b> {n}</span>' for e, n in exams.items()) + '</div>'

def chapter_card(ch, limit=6):
    cid = ch["id"]
    meta = f"{ch['tests']} test{'s' if ch['tests']!=1 else ''}" + (f" · {ch['years'][0]}–{ch['years'][-1]} papers" if len(ch["years"]) > 1 else (f" · {ch['years'][0]} papers" if ch["years"] else ""))
    body = test_tiles(ch, limit) if ch["tests"] else f'<div class="soon">Collecting — the first test opens at {MIN_FIRST_SET} tagged questions.</div>'
    wait = f'<div class="waiting">+{ch["waiting"]} more collected — next test opens at {SET_SIZE}</div>' if ch["waiting"] and ch["tests"] else ""
    return f"""<article class="chap" data-name="{E(ch['name']).lower()}"><div class="chap-top"><div><div class="chap-name"><a href="{chapter_file(cid)}">{E(ch['name'])}</a></div><div class="chap-meta">{meta}</div>{exam_badges(ch['exams'])}</div><div class="qcount">{ch['count']}<small>PYQs</small></div></div>
<div class="tests">{body}</div>{wait}</article>"""

LEGEND = '<div class="legend"><span><i style="background:#00A86B"></i>Attempted</span><span><i style="background:#F8FAFC;border:1px solid #E2E8F0"></i>Not attempted</span><span>EN / हिंदी open the same test in that language</span></div>'

def exam_strip(exams):
    items = []
    for e in sorted(exams, key=lambda e: (EXAM_ORDER.index(e) if e in EXAM_ORDER else 99, e)):
        v = exams[e]; yrs = f"{v['years'][0]}–{v['years'][-1]}" if len(v["years"]) > 1 else (v["years"][0] if v["years"] else "")
        items.append(f'<a href="https://trickyssc.com/{exam_meta(e)["hub"]}"><i>📄</i><span><b>{E(v["name"])}</b><small>{v["papers"]} papers · {v["questions"]} tagged PYQs{(" · " + yrs) if yrs else ""}</small></span></a>')
    return '<div class="exam-strip">' + "".join(items) + "</div>"

def all_subjects(index):
    return sorted(index, key=lambda s: SUBJECTS[s][4])

def gen_subject_page(index, exams, subj):
    sl, _, color, icon, _ = SUBJECTS[subj]; label = subj_label(subj); short = subj_short(subj)
    csoft = color + "22"
    chs = index[subj]
    total_q = sum(c["count"] for c in chs); total_t = sum(c["tests"] for c in chs); n_ch = sum(1 for c in chs if c["tests"])
    by_exam = {}
    for c in chs:
        for e, n in c["exams"].items(): by_exam[e] = by_exam.get(e, 0) + n
    by_exam = dict(sorted(by_exam.items(), key=lambda kv: (EXAM_ORDER.index(kv[0]) if kv[0] in EXAM_ORDER else 99, kv[0])))
    top = sorted(chs, key=lambda c: -c["count"])[:8]
    table = "".join(f"<tr><td><a href=\"{chapter_file(c['id'])}\">{E(c['name'])}</a></td><td>{c['count']}</td><td>{E(exams_line(c['exams']))}</td><td>{c['tests']}</td></tr>" for c in top)
    body = hero(
        [f'<a href="https://trickyssc.com/index.html">Home</a>', f'<a href="{HUB}">Chapter-wise PYQ</a>', f'<span class="here">{E(short)}</span>'],
        f"SSC {E(short)} Previous Year Questions — Chapter-wise PYQ Tests ({E(exams_line(by_exam, ' · '))})",
        f"Every {E(short)} question from the {E(exams_sentence(by_exam))} previous-year papers on TrickySSC, sorted into chapters and served as {SET_SIZE}-question tests. Each question shows the exam, paper and shift it was asked in, so you see exactly how SSC frames this subject across its exams.",
        [f"<b>{n_ch}</b> chapters live", f"<b>{total_t}</b> tests", f"<b>{total_q}</b> PYQs", f"<b>{SET_SIZE}</b> questions / test", "🌐 English + हिंदी"],
        f"All chapter-wise PYQ tests are free — sign in and start. Attempted tests turn green and keep a Review link.")
    body += f"""<div class="wrap">
<div class="controls"><div class="search">🔍 <input id="chSearch" placeholder="Search a chapter…" oninput="var v=this.value.toLowerCase();document.querySelectorAll('.chap').forEach(function(c){{c.classList.toggle('hidden',v&&c.getAttribute('data-name').indexOf(v)<0)}})"></div>
<div class="subj-nav">{''.join(f'<a href="{subject_file(s)}">{E(subj_short(s))}</a>' for s in all_subjects(index) if s != subj)}</div></div>
{LEGEND}
<section style="--c:{color};--csoft:{csoft}"><div class="chap-grid">{''.join(chapter_card(c) for c in chs)}</div></section>
<section><h2>Which {E(short)} chapters does SSC ask most?</h2><p>Counted across every SSC exam paper on this site. Use it to decide where to spend your time first.</p>
<table class="tbl"><thead><tr><th>Chapter</th><th>PYQs</th><th>By exam</th><th>Tests</th></tr></thead><tbody>{table}</tbody></table></section>
<section><h2>How these tests work</h2>
<p>Every question here was asked in a real SSC paper — {E(exams_sentence(by_exam))}. A chapter's questions from all exams sit together, in paper order: Test 1 holds the oldest papers, the last test the newest. When a new paper of any exam is uploaded and tagged, its questions join the end of the chapter and a new test appears once {SET_SIZE} have collected, so tests you have already attempted never change.</p>
<p>Tests run with a 15-minute timer by default (you can switch it off on the start screen), carry +2 / −0.5 marking like the chapter tests, and show a step-by-step solution for every question in English and Hindi. The exam, paper and shift are shown under every question.</p></section>
<section><h2>More free practice</h2><div class="link-row">
<a href="{HUB}">All chapter-wise PYQ subjects<span>{E(', '.join(subj_short(s) for s in all_subjects(index)))}</span></a>
{''.join(f'<a href="https://trickyssc.com/{EXAMS[e]["hub"]}">{n} previous year papers<span>Full shift-wise papers with solutions</span></a>' for e, n in NAV_EXAMS)}
<a href="https://trickyssc.com/ssc-cgl-chapterwise.html">SSC CGL chapter-wise tests<span>Model questions, two levels, 25 per test</span></a></div></section>
</div>"""
    title = f"SSC {short} PYQ Chapter-wise — {total_q} Previous Year Questions ({exams_line(by_exam, ', ')}) in {n_ch} Chapters | TrickySSC"
    desc = f"Free SSC {short} previous year questions sorted chapter-wise from {exams_sentence(by_exam)} papers: {total_q} PYQs in {total_t} tests of {SET_SIZE}, English and Hindi, with the exam, paper and shift shown under every question."
    return page(title, desc, subject_file(subj), body, index, extra_js=ATTEMPT_JS)

def gen_hub(index, counts, exams):
    cs = []
    for s in all_subjects(index):
        sl, _, color, icon, _ = SUBJECTS[s]; chs = index[s]
        nq = sum(c["count"] for c in chs); nt = sum(c["tests"] for c in chs); nc = sum(1 for c in chs if c["tests"])
        by_exam = {}
        for c in chs:
            for e, n in c["exams"].items(): by_exam[e] = by_exam.get(e, 0) + n
        by_exam = dict(sorted(by_exam.items(), key=lambda kv: (EXAM_ORDER.index(kv[0]) if kv[0] in EXAM_ORDER else 99, kv[0])))
        top = ", ".join(c["name"].split(" (")[0] for c in chs[:5])
        cs.append(f"""<article class="sc" style="--c:{color};--csoft:{color}22"><div class="sc-top"><div class="sc-ic">{icon}</div><div><div class="sc-name">{E(subj_label(s))}</div><div class="sc-sub">{E(exams_line(by_exam))} PYQs</div></div></div>
<div class="sc-live"><div class="sc-stat"><b>{nc}</b><span>chapters</span></div><div class="sc-stat"><b>{nt}</b><span>tests</span></div><div class="sc-stat"><b>{nq}</b><span>PYQs</span></div></div>
<p class="sc-desc">Most asked: {E(top)}.</p><a class="sc-btn" href="{subject_file(s)}">Open {E(subj_short(s))} chapters <em>&rarr;</em></a></article>""")
    tot_q = sum(c["count"] for v in index.values() for c in v); tot_t = sum(c["tests"] for v in index.values() for c in v); tot_c = sum(1 for v in index.values() for c in v if c["tests"])
    names = exams_sentence(exams)
    body = hero([f'<a href="https://trickyssc.com/index.html">Home</a>', '<span class="here">Chapter-wise PYQ</span>'],
        "SSC Exams Chapter-wise Previous Year Questions — Free PYQ Tests in English &amp; हिंदी",
        f"Every question from the {counts['papers']} {E(names)} papers on TrickySSC, sorted by chapter and served as {SET_SIZE}-question tests. One chapter page holds that chapter's questions from every SSC exam — practise exactly what SSC has asked, chapter by chapter, with the exam, paper and shift shown under every question.",
        [f"<b>{counts['papers']}</b> papers", f"<b>{tot_q}</b> PYQs", f"<b>{tot_c}</b> chapters", f"<b>{tot_t}</b> tests", "🌐 English + हिंदी"],
        "Chapter-wise PYQ tests are completely free. Sign in to keep your progress, rank and review on your dashboard.",
        extra=exam_strip(exams))
    body += f"""<div class="wrap">
<section><h2>Choose a subject</h2><p>Each subject page lists every chapter with its tests. Tests you have attempted turn green and keep a Review link.</p><div class="subj-grid">{''.join(cs)}</div></section>
<section><h2>Why chapter-wise PYQs across all SSC exams?</h2>
<p>Solving a full paper tells you your score. Solving the same questions chapter-wise tells you <b>which chapters</b> cost you marks — and shows the exact patterns SSC repeats year after year. CGL, CHSL, GD, MTS and CPO are set by the same commission from the same syllabus, so a chapter's questions from every exam together give you the complete picture of how it is asked. These tests are built only from real previous-year questions, so the difficulty is the real difficulty.</p>
<p>Questions are added automatically whenever a new paper of any SSC exam is uploaded to TrickySSC. Each chapter's tests are fixed in paper order, so Test 3 is always the same Test 3 — new questions open a new test at the end.</p></section>
<section><h2>Frequently asked questions</h2><div class="faq">
<details><summary>Are the questions really from previous SSC papers?</summary><div class="ans">Yes. Every question comes from a {E(names)} paper hosted on TrickySSC, and the exam, date and shift are shown under the question in the test.</div></details>
<details><summary>Why are CGL, CHSL and GD questions mixed in one test?</summary><div class="ans">The chapter is the same; only the exam differs. Seeing every way SSC has asked a chapter — across exams and years — is the fastest way to master it. The label under each question tells you which exam and shift it came from.</div></details>
<details><summary>How many questions are in one test?</summary><div class="ans">{SET_SIZE}. A new chapter shows its first test once {MIN_FIRST_SET} questions have been tagged; that test grows to {SET_SIZE}, after which every further test is a full {SET_SIZE}.</div></details>
<details><summary>Can I take the tests in Hindi?</summary><div class="ans">Yes — the हिंदी button opens the same test in Hindi wherever the Hindi paper is available, with a View in English toggle on every question.</div></details>
<details><summary>Is there negative marking?</summary><div class="ans">Tests use +2 for a correct answer and −0.5 for a wrong one, like the chapter tests. Unattempted questions score zero.</div></details>
</div></section>
<section><h2>More free SSC practice</h2><div class="link-row">
{''.join(f'<a href="https://trickyssc.com/{EXAMS[e]["hub"]}">{n} previous year papers<span>Full shift-wise papers with solutions</span></a>' for e, n in NAV_EXAMS)}
<a href="https://trickyssc.com/ssc-cgl-chapterwise.html">SSC CGL chapter-wise tests<span>Model questions in two levels</span></a>
<a href="https://trickyssc.com/ssc-cgl-mock-test.html">SSC CGL mock tests<span>Full-length, real sectional timing</span></a>
<a href="https://trickyssc.com/ssc-chsl-mock-test.html">SSC CHSL mock tests<span>Tier I + Tier II, ₹49 a year</span></a>
<a href="https://trickyssc.com/current-affairs.html">Daily current affairs<span>Updated every day</span></a></div></section>
</div>"""
    title = f"SSC Chapter-wise PYQ {dt.date.today().year} — {tot_q} Previous Year Questions of CGL, CHSL, GD by Chapter, Free Tests | TrickySSC"
    desc = f"Free SSC chapter-wise previous year questions: {tot_q} PYQs from {counts['papers']} {names} papers in {tot_c} chapters, {SET_SIZE}-question tests in English and Hindi with solutions. One chapter, every SSC exam."
    return page(title, desc, HUB, body, index)

def gen_chapter_page(index, ch):
    subj = ch["subject"]; sl, _, color, icon, _ = SUBJECTS[subj]; short = subj_short(subj)
    tiles = test_tiles(ch) if ch["tests"] else f'<div class="soon">Collecting — {ch["count"]} tagged so far; the first test opens at {MIN_FIRST_SET}.</div>'
    wait = f'<div class="waiting">+{ch["waiting"]} more collected — next test opens at {SET_SIZE}</div>' if ch["waiting"] and ch["tests"] else ""
    years = ch["years"]; yr = f"{years[0]}–{years[-1]}" if len(years) > 1 else (years[0] if years else "")
    siblings = [c for c in index[subj] if c["id"] != ch["id"]][:12]
    sib_links = "".join(f'<a href="{chapter_file(c["id"])}">{E(c["name"])}<span>{c["count"]} PYQs · {c["tests"]} tests</span></a>' for c in siblings)
    name = ch["name"]; ex = ch["exams"]; names = exams_sentence(ex)
    exam_rows = "".join(f"<tr><td>{E(exam_name(e))}</td><td>{n}</td><td><a href=\"https://trickyssc.com/{exam_meta(e)['hub']}\">{E(exam_name(e))} papers</a></td></tr>" for e, n in ex.items())
    body = hero([f'<a href="https://trickyssc.com/index.html">Home</a>', f'<a href="{HUB}">Chapter-wise PYQ</a>', f'<a href="{subject_file(subj)}">{E(short)}</a>', f'<span class="here">{E(name)}</span>'],
        f"{E(name)} Previous Year Questions {yr} — SSC {E(exams_line(ex, ' · '))} · Chapter-wise PYQ Tests",
        f"{ch['count']} real SSC questions on {E(name)} from the {E(names)} {yr} papers, served as {SET_SIZE}-question tests. Every question shows the exam, paper and shift it came from, and has a step-by-step solution in English and Hindi.",
        [f"<b>{ch['count']}</b> PYQs", f"<b>{ch['tests']}</b> tests", f"<b>{SET_SIZE}</b> questions / test", f"📅 {yr} papers" if yr else "", "🌐 English + हिंदी"] + [f"<b>{E(short_name(e))}</b> {n}" for e, n in ex.items()],
        "Free for everyone — sign in to keep your progress and rank.")
    body += f"""<div class="wrap">
<section><h2>{E(name)} — pick a test and start</h2>{LEGEND}<div class="tests" style="--c:{color};--csoft:{color}22">{tiles}</div>{wait}</section>
<section><h2>About these {E(name)} questions</h2>
<p>These are the actual {E(name)} questions SSC asked in the {E(names)} {yr} papers on TrickySSC — not model questions. Questions from every exam sit together in paper order: Test 1 has the oldest papers, the last test the newest, and a new test opens at the end whenever {SET_SIZE} more questions are tagged from a newly uploaded paper of any SSC exam.</p>
<table class="tbl"><thead><tr><th>Exam</th><th>{E(name)} PYQs</th><th>Full papers</th></tr></thead><tbody>{exam_rows}</tbody></table>
<p style="margin-top:.8rem">Use the हिंदी button for the Hindi paper's wording, and the View in English toggle inside the test to compare. After submitting, the review shows every solution, your time per question and where you stand on the leaderboard for that test.</p></section>
<section><h2>Other {E(short)} chapters</h2><div class="link-row">{sib_links}<a href="{subject_file(subj)}">All {E(short)} chapters<span>Full chapter list with PYQ counts</span></a></div></section>
<section><h2>More free practice</h2><div class="link-row">
<a href="{HUB}">Chapter-wise PYQ — all subjects<span>Every chapter, every SSC exam</span></a>
{''.join(f'<a href="https://trickyssc.com/{EXAMS[e]["hub"]}">{n} previous year papers<span>Full shift-wise papers</span></a>' for e, n in NAV_EXAMS)}
<a href="https://trickyssc.com/ssc-cgl-mock-test.html">SSC CGL mock tests<span>Full-length, real sectional timing</span></a></div></section>
</div>"""
    title = f"{name} PYQ {yr} — {ch['count']} SSC Previous Year Questions ({exams_line(ex, ', ')}), Chapter-wise Tests | TrickySSC"
    desc = f"Practise {ch['count']} real SSC {name} previous year questions from {names} ({yr}) as {SET_SIZE}-question tests, in English and Hindi, with solutions and the exam, paper and shift under every question."
    ld = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/index.html"},
        {"@type": "ListItem", "position": 2, "name": "Chapter-wise PYQ", "item": f"{SITE}/{HUB}"},
        {"@type": "ListItem", "position": 3, "name": short, "item": f"{SITE}/{subject_file(subj)}"},
        {"@type": "ListItem", "position": 4, "name": name, "item": f"{SITE}/{chapter_file(ch['id'])}"}]}, ensure_ascii=False)
    return page(title, desc, chapter_file(ch["id"]), body, index, extra_head=f'<script type="application/ld+json">{ld}</script>', extra_js=ATTEMPT_JS)

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
