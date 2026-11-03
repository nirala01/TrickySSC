#!/usr/bin/env python3
"""
build_pyq_chapters.py — chapter-wise PYQ tests for TrickySSC (SSC CGL, CHSL, GD).

Runs in GitHub Actions (build-pyq-chapters.yml). Pure stdlib, no secrets.

What it does
  1. Reads every previous-year question of each exam from Firestore (public REST
     read, the same web key the site pages use) — only the small fields it needs.
  2. Keeps the questions that have a confident chapter tag:
        chapterId set, not an "…other" chapter, chapterConf >= 0.7 (missing conf = hand-set = fine).
     Low-confidence tags are left out until they are corrected in admin-pyq-chapter-tag.html.
  3. Pairs each English question with its Hindi twin (same paper, same qNum).
     SSC GD Part D on the Hindi paper (हिंदी भाषा, hindi.* chapters) has no English twin.
  4. Cuts every chapter into fixed 25-question tests. Order is STABLE: papers keep the
     sequence they were first seen in (pyq-chapters/state-<exam>.json), so a newly uploaded
     paper only adds questions at the END — Test 3 stays Test 3. A new test appears when
     25 more questions have collected; a chapter with no full test yet shows one test once
     it has 10 questions (that test grows until it reaches 25).
  5. Writes pyq-chapters/<exam>/<tier>/<chapterId>.json — the question ids of each test with
     the paper each came from — read by pyq-chapter-test.html with ONE batchGet per test.
  6. Generates the pages: <exam>-pyq-chapterwise.html (hub), <exam>-<subject>-chapter-wise-pyq.html
     (subject lists) and <exam>-<chapter>-pyq.html (one per chapter), and refreshes their
     block in sitemap.xml.

Usage
    python scripts/build_pyq_chapters.py              # all exams
    python scripts/build_pyq_chapters.py --exam ssc-gd
    python scripts/build_pyq_chapters.py --dry        # build from a saved dump (tests)
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

EXAMS = {
    "ssc-cgl":  {"name": "SSC CGL",  "tiers": ["tier1", "tier2"], "hub": "ssc-cgl-pyq.html",  "exam_page": "ssc-cgl.html",  "cw": "ssc-cgl-chapterwise.html", "mock": "ssc-cgl-mock-test.html"},
    "ssc-chsl": {"name": "SSC CHSL", "tiers": ["tier1", "tier2"], "hub": "ssc-chsl-pyq.html", "exam_page": "ssc-chsl.html", "cw": "",                         "mock": "ssc-chsl-mock-test.html"},
    "ssc-gd":   {"name": "SSC GD",   "tiers": ["tier1"],          "hub": "ssc-gd-pyq.html",   "exam_page": "ssc-gd.html",   "cw": "",                         "mock": "ssc-gd-mock-test.html"},
}
TIER_LABEL = {"tier1": "Tier I", "tier2": "Tier II"}
# canonical subject key -> site subject slug, label, colour, icon, order
SUBJECTS = {
    "reasoning":         ("reasoning",  "General Intelligence & Reasoning", "#8B5CF6", "🧠", 1),
    "ga":                ("gk",         "General Awareness",                "#0EA5E9", "🌍", 2),
    "quant":             ("quant",      "Quantitative Aptitude",            "#00A86B", "🔢", 3),
    "english":           ("english",    "English Language",                 "#FF6B00", "✍️", 4),
    "hindi":             ("hindi",      "Hindi Language (हिंदी भाषा)",       "#138808", "📝", 5),
    "computer":          ("computer",   "Computer Knowledge",               "#EC4899", "💻", 6),
    "statistics":        ("statistics", "Statistics",                       "#14B8A6", "📊", 7),
    "finance_economics": ("finance",    "Finance & Economics",              "#6366F1", "💰", 8),
}
GD_SUBJECT_LABEL = {"ga": "General Knowledge & General Awareness", "quant": "Elementary Mathematics"}

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
    """All docs matching the equality filters, selected fields only, paged by __name__."""
    out, cursor = [], None
    while True:
        q = {"from": [{"collectionId": collection}],
             "where": {"compositeFilter": {"op": "AND", "filters": [{"fieldFilter": {"field": {"fieldPath": f}, "op": "EQUAL", "value": {"stringValue": v}}} for f, v in filters]}},
             "select": {"fields": [{"fieldPath": f} for f in fields]},
             "orderBy": [{"field": {"fieldPath": "__name__"}, "direction": "ASCENDING"}],
             "limit": page}
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

def fetch_exam(exam):
    papers = run_query("papers", [("exam", exam)], ["paperId", "year", "tier", "shift", "heldOn", "language", "type", "mockId", "questionCount"])
    qs = run_query("questions", [("exam", exam), ("type", "pyq")], ["paperId", "qNum", "language", "subject", "chapterId", "chapterConf", "tier", "year", "shift", "heldOn"])
    return papers, qs


# ── shaping ──────────────────────────────────────────────────────────────────
def norm_lang(v):
    return "hi" if re.match(r"^\s*h", str(v or ""), re.I) else "en"

def norm_tier(v):
    return "tier2" if re.search(r"2|ii", str(v or ""), re.I) else "tier1"

def norm_shift(v):
    d = re.findall(r"\d+", str(v or ""))
    return ("Shift " + d[0]) if d else str(v or "").strip()

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

def paper_key(p):
    return "|".join(str(p.get(k) or "") for k in ("year", "tier", "shift", "heldOn"))

def build_exam(exam, papers, qs):
    meta = EXAMS[exam]
    # paper cards → label per key (ignore mocks)
    cards = {}
    for p in papers:
        if str(p.get("type") or "").lower() == "mock" or p.get("mockId"): continue
        k = paper_key(p)
        c = cards.setdefault(k, {"year": str(p.get("year") or ""), "tier": norm_tier(p.get("tier")), "shift": norm_shift(p.get("shift")), "heldOn": str(p.get("heldOn") or ""), "ids": set()})
        if p.get("paperId"): c["ids"].add(p["paperId"])
        c["ids"].add(p["_id"])
    # question → paper key (by paperId, else by its own year/tier/shift/heldOn)
    by_pid = {pid: k for k, c in cards.items() for pid in c["ids"]}
    def qkey(q):
        pid = q.get("paperId") or ""
        if pid in by_pid: return by_pid[pid]
        alt = re.sub(r"_(hi|hindi|en|english)$", "", pid)
        for suf in ("_en", "_hi", "_english", "_hindi"):
            if alt + suf in by_pid: return by_pid[alt + suf]
        k = paper_key({"year": q.get("year"), "tier": q.get("tier"), "shift": q.get("shift"), "heldOn": q.get("heldOn")})
        if k not in cards and q.get("heldOn"):
            cards[k] = {"year": str(q.get("year") or ""), "tier": norm_tier(q.get("tier")), "shift": norm_shift(q.get("shift")), "heldOn": str(q.get("heldOn") or ""), "ids": {pid}}
        return k if k in cards else None

    # group questions per paper / lang / qNum
    grid = {}   # key -> {"en": {qNum: doc}, "hi": {qNum: doc}}
    for q in qs:
        k = qkey(q)
        if not k: continue
        L = norm_lang(q.get("language"))
        try: n = int(q.get("qNum") or 0)
        except Exception: n = 0
        if n: grid.setdefault(k, {"en": {}, "hi": {}})[L][n] = q

    # stable paper order
    state_path = os.path.join(OUT, f"state-{exam}.json")
    state = json.load(open(state_path, encoding="utf-8")) if os.path.exists(state_path) else {"order": []}
    order = [k for k in state["order"] if k in grid]
    new = sorted([k for k in grid if k not in order], key=lambda k: (cards[k]["heldOn"], cards[k]["shift"]))
    order += new
    state["order"] = order; state["updated"] = TODAY
    os.makedirs(OUT, exist_ok=True)
    json.dump(state, open(state_path, "w", encoding="utf-8"), ensure_ascii=False, indent=0)

    # collect eligible questions per (tier, chapter) in stable order
    chapters = {}  # (tier, cid) -> list of {en, hi, p, q}
    counts = {"papers": len(order), "questions": 0, "eligible": 0, "excluded_low": 0, "untagged": 0}
    for k in order:
        c = cards[k]; tier = c["tier"]
        label = f"{meta['name']} {c['year']} · {TIER_LABEL[tier]} · {pretty_date(c['heldOn'])} · {c['shift']}".replace(" ·  ·", " ·").strip(" ·")
        g = grid[k]
        for n in sorted(g["en"]):
            q = g["en"][n]; counts["questions"] += 1
            if not q.get("chapterId"): counts["untagged"] += 1; continue
            if not eligible(q): counts["excluded_low"] += 1; continue
            counts["eligible"] += 1
            hi = g["hi"].get(n)
            if hi and is_hindi_subject(hi.get("subject")): hi = None     # GD Part D: different question on the Hindi paper
            chapters.setdefault((tier, q["chapterId"]), []).append({"en": q["_id"], "hi": hi["_id"] if hi else None, "p": label, "q": n})
        # Hindi-paper-only questions (GD Part D Hindi Language, or papers with no English doc)
        for n in sorted(g["hi"]):
            if n in g["en"] and not is_hindi_subject(g["hi"][n].get("subject")): continue
            q = g["hi"][n]; counts["questions"] += 1
            if not q.get("chapterId"): counts["untagged"] += 1; continue
            if not eligible(q): counts["excluded_low"] += 1; continue
            counts["eligible"] += 1
            chapters.setdefault((tier, q["chapterId"]), []).append({"en": None, "hi": q["_id"], "p": label, "q": n})

    # cut into sets, write JSON
    index = {}   # tier -> subject -> [chapter summary]
    written = 0
    for (tier, cid), items in sorted(chapters.items()):
        full = len(items) // SET_SIZE
        sets = [{"n": i + 1, "qs": items[i * SET_SIZE:(i + 1) * SET_SIZE]} for i in range(full)]
        rem = items[full * SET_SIZE:]
        if not sets and len(rem) >= MIN_FIRST_SET:
            sets = [{"n": 1, "qs": rem}]; rem = []
        subj = SUBJ_OF[cid]
        summary = {"id": cid, "name": NAME[cid], "subject": subj, "count": len(items), "tests": len(sets),
                   "waiting": len(rem), "hi": sum(1 for s in sets for x in s["qs"] if x["hi"]) > 0,
                   "en": sum(1 for s in sets for x in s["qs"] if x["en"]) > 0,
                   "years": sorted({re.search(r"\b(20\d\d)\b", x["p"]).group(1) for x in items if re.search(r"\b(20\d\d)\b", x["p"])})}
        index.setdefault(tier, {}).setdefault(subj, []).append(summary)
        if sets:
            d = os.path.join(OUT, exam, tier); os.makedirs(d, exist_ok=True)
            data = {"exam": exam, "tier": tier, "chapter": cid, "name": NAME[cid], "subject": subj, "count": len(items), "built": TODAY, "sets": sets}
            path = os.path.join(d, cid + ".json")
            txt = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
            if json.loads(old).get("sets") != sets if old else True:
                open(path, "w", encoding="utf-8").write(txt); written += 1
    for tier in index:
        for subj in index[tier]:
            index[tier][subj].sort(key=lambda c: (-c["tests"], -c["count"], c["name"]))
    json.dump({"exam": exam, "built": TODAY, "counts": counts, "tiers": index}, open(os.path.join(OUT, f"index-{exam}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{exam}: {counts} → {sum(len(v) for t in index.values() for v in t.values())} chapters, {written} test files changed")
    return index, counts


# ── pages ────────────────────────────────────────────────────────────────────
E = lambda s: html.escape(str(s), quote=True)

def slug_of(cid):
    # reason/ga/quant/eng chapters keep a plain slug (ssc-cgl-percentage-pyq.html); the Tier-II
    # modules and Hindi keep their prefix so e.g. quant.probability / statistics.probability can't clash
    pre, rest = cid.split(".", 1)
    return rest if pre in ("reason", "ga", "quant", "eng") else f"{pre}-{rest}"

def chapter_file(exam, cid):
    return f"{exam}-{slug_of(cid)}-pyq.html"

def subject_file(exam, subj):
    return f"{exam}-{SUBJECTS[subj][0]}-chapter-wise-pyq.html"

def hub_file(exam):
    return f"{exam}-pyq-chapterwise.html"

def subj_label(exam, subj):
    return GD_SUBJECT_LABEL.get(subj, SUBJECTS[subj][1]) if exam == "ssc-gd" else SUBJECTS[subj][1]

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
  const EXAM=document.body.getAttribute('data-exam'), KEY='tsscPyqChAtt:'+EXAM+':'+user.uid, TTL=10*60*1000;
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
  rows.filter(a=>a.exam===EXAM).forEach(a=>{
    document.querySelectorAll('.test[data-ch="'+a.ch+'"][data-tier="'+a.tier+'"][data-n="'+a.tn+'"]').forEach(t=>{
      t.classList.add('done');
      if(a.rev && !t.querySelector('a.rv')){ const l=document.createElement('a'); l.className='rv'; l.textContent='Review'; l.href=t.getAttribute('data-href')+'&lang='+a.lang+'&review='+encodeURIComponent(a.id); t.appendChild(l); }
    });
  });
};
</script>
"""

def nav(exam):
    m = EXAMS[exam]
    return f"""<nav><div class="nav-inner">
  <a class="brand" href="https://trickyssc.com/index.html" aria-label="TrickySSC home"><span class="brand-icon">⚡</span><span class="brand-name">Tricky<span>SSC</span></span></a>
  <button class="nav-toggle" id="navToggle" aria-label="Toggle menu" aria-expanded="false" onclick="var m=document.getElementById('navLinks');var o=m.classList.toggle('open');this.setAttribute('aria-expanded',o);"><span></span></button>
  <ul class="nav-links" id="navLinks">
    <li><a href="https://trickyssc.com/index.html">Home</a></li>
    <li><a href="https://trickyssc.com/{m['exam_page']}">{m['name']}</a></li>
    <li><a href="https://trickyssc.com/{m['hub']}">PYQ Bank</a></li>
    <li><a href="https://trickyssc.com/{hub_file(exam)}">Chapter-wise PYQ</a></li>
    <li><a href="https://trickyssc.com/{m['mock']}">Mock Tests</a></li>
    <li id="navAccount"><a class="nav-cta" href="https://trickyssc.com/login.html" onclick="tsscStashReturn&&tsscStashReturn()">👤 Login</a></li>
  </ul></div></nav>"""

def foot(exam, index):
    m = EXAMS[exam]
    links = [f'<a href="https://trickyssc.com/index.html">Home</a>', f'<a href="https://trickyssc.com/{m["hub"]}">{m["name"]} PYQ</a>', f'<a href="https://trickyssc.com/{hub_file(exam)}">Chapter-wise PYQ</a>']
    seen = set()
    for tier in m["tiers"]:
        for subj in sorted(index.get(tier, {}), key=lambda s: SUBJECTS[s][4]):
            if subj in seen: continue
            seen.add(subj); links.append(f'<a href="https://trickyssc.com/{subject_file(exam, subj)}">{E(subj_label(exam, subj))} PYQ</a>')
    return f"""<div class="foot"><div class="fl">{''.join(links)}</div><div>Free SSC exam prep · <a href="https://trickyssc.com/index.html">TrickySSC.com</a></div>
<div style="margin-top:.4rem;">Chapter-wise PYQ tests are rebuilt automatically from the previous-year papers on this site. New papers add new tests at the end of each chapter.</div></div>"""

def page(exam, title, desc, canonical, body, index, extra_head="", extra_js=""):
    m = EXAMS[exam]
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
<style>{CSS}</style>
</head>
<body data-exam="{exam}">
{nav(exam)}
{body}
{foot(exam, index)}
{ACCOUNT_JS}{extra_js}
</body>
</html>
"""

def hero(exam, crumbs, h1, lede, pills, free_line):
    c = " <span class=\"sep\">/</span> ".join(crumbs)
    return f"""<header class="hero"><div class="hero-in">
  <div class="crumb">{c}</div>
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
  <div class="pill-row">{''.join(f'<span class="pill">{p}</span>' for p in pills)}</div>
  <div class="cw-free" role="note"><span class="cw-free-tag">100% FREE</span><span>{free_line}</span></div>
</div></header>"""

def test_tiles(exam, tier, ch, limit=None):
    cid = ch["id"]; n = ch["tests"]
    out = []
    for i in range(1, n + 1):
        href = f"pyq-chapter-test.html?exam={exam}&tier={tier}&chapter={cid}&test={i}"
        en = f'<a href="{href}&lang=en">EN</a>' if ch["en"] else ""
        hi = f'<a href="{href}&lang=hi">हिंदी</a>' if ch["hi"] else ""
        out.append(f'<span class="test" data-ch="{cid}" data-tier="{tier}" data-n="{i}" data-href="{href}"><span class="n">T{i}</span>{en}{hi}</span>')
    if limit and n > limit:
        shown = "".join(out[:limit]); more = "".join(out[limit:])
        return f'{shown}<span class="more-wrap hidden">{more}</span><a class="test" href="#" onclick="this.previousElementSibling.classList.remove(\'hidden\');this.remove();return false;" style="padding:.3rem .55rem;color:var(--muted)">+{n-limit} more ▾</a>'
    return "".join(out)

def chapter_card(exam, tier, ch, limit=6):
    cid = ch["id"]
    meta = f"{ch['tests']} test{'s' if ch['tests']!=1 else ''}" + (f" · {ch['years'][0]}–{ch['years'][-1]} papers" if len(ch["years"]) > 1 else (f" · {ch['years'][0]} papers" if ch["years"] else ""))
    body = test_tiles(exam, tier, ch, limit) if ch["tests"] else f'<div class="soon">Collecting — the first test opens at {MIN_FIRST_SET} tagged questions.</div>'
    wait = f'<div class="waiting">+{ch["waiting"]} more collected — next test opens at {SET_SIZE}</div>' if ch["waiting"] and ch["tests"] else ""
    return f"""<article class="chap" data-name="{E(ch['name']).lower()}"><div class="chap-top"><div><div class="chap-name"><a href="{chapter_file(exam, cid)}">{E(ch['name'])}</a></div><div class="chap-meta">{meta}</div></div><div class="qcount">{ch['count']}<small>PYQs</small></div></div>
<div class="tests">{body}</div>{wait}</article>"""

LEGEND = '<div class="legend"><span><i style="background:#00A86B"></i>Attempted</span><span><i style="background:#F8FAFC;border:1px solid #E2E8F0"></i>Not attempted</span><span>EN / हिंदी open the same test in that language</span></div>'

def gen_subject_page(exam, index, subj):
    m = EXAMS[exam]; sl, _, color, icon, _ = SUBJECTS[subj]; label = subj_label(exam, subj)
    csoft = color + "22"
    tiers = [t for t in m["tiers"] if subj in index.get(t, {})]
    total_q = sum(c["count"] for t in tiers for c in index[t][subj]); total_t = sum(c["tests"] for t in tiers for c in index[t][subj]); n_ch = sum(1 for t in tiers for c in index[t][subj] if c["tests"])
    sections = []
    for t in tiers:
        chs = index[t][subj]
        tl = f'<div class="tier-label"><span class="t">{TIER_LABEL[t]} — {sum(c["count"] for c in chs)} PYQs</span><span class="line"></span></div>' if len(m["tiers"]) > 1 else ""
        sections.append(tl + '<div class="chap-grid">' + "".join(chapter_card(exam, t, c) for c in chs) + "</div>")
    top = sorted((c for t in tiers for c in index[t][subj]), key=lambda c: -c["count"])[:6]
    table = "".join(f"<tr><td><a href=\"{chapter_file(exam, c['id'])}\">{E(c['name'])}</a></td><td>{c['count']}</td><td>{c['tests']}</td></tr>" for c in top)
    body = hero(exam,
        [f'<a href="https://trickyssc.com/index.html">Home</a>', f'<a href="https://trickyssc.com/{m["exam_page"]}">{m["name"]}</a>', f'<a href="{hub_file(exam)}">Chapter-wise PYQ</a>', f'<span class="here">{E(label)}</span>'],
        f"{m['name']} {E(label)} Previous Year Questions — Chapter-wise PYQ Tests",
        f"Every {m['name']} {E(label)} question from the previous-year papers on TrickySSC, sorted into chapters and served as 25-question tests. Each question shows the paper and shift it was asked in, so you see exactly how SSC frames this subject.",
        [f"<b>{n_ch}</b> chapters live", f"<b>{total_t}</b> tests", f"<b>{total_q}</b> PYQs", f"<b>{SET_SIZE}</b> questions / test", "🌐 English + हिंदी"],
        f"All chapter-wise PYQ tests are free — sign in and start. Attempted tests turn green and keep a Review link.")
    body += f"""<div class="wrap">
<div class="controls"><div class="search">🔍 <input id="chSearch" placeholder="Search a chapter…" oninput="var v=this.value.toLowerCase();document.querySelectorAll('.chap').forEach(function(c){{c.classList.toggle('hidden',v&&c.getAttribute('data-name').indexOf(v)<0)}})"></div>
<div class="subj-nav">{''.join(f'<a href="{subject_file(exam, s)}">{E(subj_label(exam, s)).split(" (")[0]}</a>' for s in all_subjects(index) if s != subj)}</div></div>
{LEGEND}
<section style="--c:{color};--csoft:{csoft}">{''.join(sections)}</section>
<section><h2>Which {E(label)} chapters does SSC ask most?</h2><p>Counted from the papers on this site. Use it to decide where to spend your time first.</p>
<table class="tbl"><thead><tr><th>Chapter</th><th>PYQs</th><th>Tests</th></tr></thead><tbody>{table}</tbody></table></section>
<section><h2>How these tests work</h2>
<p>Every question here was asked in a real {m['name']} paper. Each chapter is cut into fixed tests of {SET_SIZE} questions in paper order — Test 1 holds the oldest questions, the last test the newest. When a new paper is uploaded and tagged, its questions join the end of the chapter and a new test appears once {SET_SIZE} have collected, so tests you have already attempted never change.</p>
<p>Tests run with a 15-minute timer by default (you can switch it off on the start screen), carry +2 / −0.5 marking like the chapter tests, and show a step-by-step solution for every question in English and Hindi. The paper and shift are shown under every question.</p></section>
<section><h2>More {m['name']} practice</h2><div class="link-row">
<a href="{hub_file(exam)}">All chapter-wise PYQ subjects<span>Reasoning, GK, Maths, English{', Hindi' if exam=='ssc-gd' else ''}</span></a>
<a href="https://trickyssc.com/{m['hub']}">{m['name']} previous year papers<span>Full shift-wise papers with solutions</span></a>
{f'<a href="https://trickyssc.com/{m["cw"]}">{m["name"]} chapter-wise tests<span>Model questions, two levels, 25 per test</span></a>' if m['cw'] else ''}
<a href="https://trickyssc.com/{m['mock']}">{m['name']} mock tests<span>Full-length, real sectional timing</span></a></div></section>
</div>"""
    title = f"{m['name']} {label} PYQ Chapter-wise — {total_q} Previous Year Questions in {n_ch} Chapters | TrickySSC"
    desc = f"Free {m['name']} {label} previous year questions sorted chapter-wise: {total_q} PYQs in {total_t} tests of {SET_SIZE}, English and Hindi, with the paper and shift shown under every question."
    return page(exam, title, desc, subject_file(exam, subj), body, index, extra_js=ATTEMPT_JS)

def all_subjects(index):
    seen = []
    for t in sorted(index):
        for s in index[t]:
            if s not in seen: seen.append(s)
    return sorted(seen, key=lambda s: SUBJECTS[s][4])

def gen_hub(exam, index, counts):
    m = EXAMS[exam]
    cards = []
    for t in m["tiers"]:
        if t not in index: continue
        subs = sorted(index[t], key=lambda s: SUBJECTS[s][4])
        tl = f'<div class="tier-label"><span class="t">{TIER_LABEL[t]}</span><span class="line"></span></div>' if len(m["tiers"]) > 1 else ""
        cs = []
        for s in subs:
            sl, _, color, icon, _ = SUBJECTS[s]; chs = index[t][s]
            nq = sum(c["count"] for c in chs); nt = sum(c["tests"] for c in chs); nc = sum(1 for c in chs if c["tests"])
            top = ", ".join(c["name"].split(" (")[0] for c in chs[:5])
            cs.append(f"""<article class="sc" style="--c:{color};--csoft:{color}22"><div class="sc-top"><div class="sc-ic">{icon}</div><div><div class="sc-name">{E(subj_label(exam, s))}</div><div class="sc-sub">{TIER_LABEL[t]} · previous year questions</div></div></div>
<div class="sc-live"><div class="sc-stat"><b>{nc}</b><span>chapters</span></div><div class="sc-stat"><b>{nt}</b><span>tests</span></div><div class="sc-stat"><b>{nq}</b><span>PYQs</span></div></div>
<p class="sc-desc">Most asked: {E(top)}.</p><a class="sc-btn" href="{subject_file(exam, s)}">Open {E(subj_label(exam, s)).split(' (')[0]} chapters <em>&rarr;</em></a></article>""")
        cards.append(tl + '<div class="subj-grid">' + "".join(cs) + "</div>")
    tot_q = sum(c["count"] for t in index.values() for v in t.values() for c in v); tot_t = sum(c["tests"] for t in index.values() for v in t.values() for c in v); tot_c = sum(1 for t in index.values() for v in t.values() for c in v if c["tests"])
    body = hero(exam, [f'<a href="https://trickyssc.com/index.html">Home</a>', f'<a href="https://trickyssc.com/{m["exam_page"]}">{m["name"]}</a>', f'<a href="https://trickyssc.com/{m["hub"]}">Previous Year Papers</a>', '<span class="here">Chapter-wise PYQ</span>'],
        f"{m['name']} Chapter-wise Previous Year Questions — Free PYQ Tests in English &amp; हिंदी",
        f"Every question from the {counts['papers']} {m['name']} papers on TrickySSC, sorted by chapter and served as {SET_SIZE}-question tests. Practise exactly what SSC has asked, chapter by chapter, with the paper and shift shown under every question.",
        [f"<b>{counts['papers']}</b> papers", f"<b>{tot_q}</b> PYQs", f"<b>{tot_c}</b> chapters", f"<b>{tot_t}</b> tests", "🌐 English + हिंदी"],
        "Chapter-wise PYQ tests are completely free. Sign in to keep your progress, rank and review on your dashboard.")
    body += f"""<div class="wrap">
<section><h2>Choose a subject</h2><p>Each subject page lists every chapter with its tests. Tests you have attempted turn green and keep a Review link.</p>{''.join(cards)}</section>
<section><h2>Why chapter-wise PYQs?</h2>
<p>Solving a full paper tells you your score. Solving the same questions chapter-wise tells you <b>which chapters</b> cost you marks — and shows the exact patterns SSC repeats year after year. These tests are built only from real previous-year questions, so the difficulty is the real difficulty.</p>
<p>Questions are added automatically whenever a new paper is uploaded to TrickySSC. Each chapter's tests are fixed in paper order, so Test 3 is always the same Test 3 — new questions open a new test at the end.</p></section>
<section><h2>Frequently asked questions</h2><div class="faq">
<details><summary>Are the questions really from previous {m['name']} papers?</summary><div class="ans">Yes. Every question comes from a {m['name']} paper hosted on TrickySSC, and the paper, date and shift are shown under the question in the test.</div></details>
<details><summary>How many questions are in one test?</summary><div class="ans">{SET_SIZE}. A new chapter shows its first test once {MIN_FIRST_SET} questions have been tagged; that test grows to {SET_SIZE}, after which every further test is a full {SET_SIZE}.</div></details>
<details><summary>Can I take the tests in Hindi?</summary><div class="ans">Yes — the हिंदी button opens the same test in Hindi wherever the Hindi paper is available, with a View in English toggle on every question.</div></details>
<details><summary>Is there negative marking?</summary><div class="ans">Tests use the real {m['name']} marking: +2 for a correct answer and −0.5 for a wrong one{' (−0.25 for SSC GD)' if exam=='ssc-gd' else ''}. Unattempted questions score zero.</div></details>
</div></section>
<section><h2>More free {m['name']} practice</h2><div class="link-row">
<a href="https://trickyssc.com/{m['hub']}">{m['name']} previous year papers<span>Full shift-wise papers with solutions</span></a>
{f'<a href="https://trickyssc.com/{m["cw"]}">{m["name"]} chapter-wise tests<span>Model questions in two levels</span></a>' if m['cw'] else ''}
<a href="https://trickyssc.com/{m['mock']}">{m['name']} mock tests<span>Full-length, real sectional timing</span></a>
<a href="https://trickyssc.com/current-affairs.html">Daily current affairs<span>Updated every day</span></a></div></section>
</div>"""
    title = f"{m['name']} Chapter-wise PYQ {dt.date.today().year} — {tot_q} Previous Year Questions, Free Tests | TrickySSC"
    desc = f"Free {m['name']} chapter-wise previous year questions: {tot_q} PYQs from {counts['papers']} papers in {tot_c} chapters, {SET_SIZE}-question tests in English and Hindi with solutions."
    return page(exam, title, desc, hub_file(exam), body, index)

def gen_chapter_page(exam, index, tier, ch):
    m = EXAMS[exam]; subj = ch["subject"]; sl, _, color, icon, _ = SUBJECTS[subj]; label = subj_label(exam, subj)
    # the same chapter may exist in both tiers: one page lists both
    blocks = []
    for t in m["tiers"]:
        c2 = next((c for c in index.get(t, {}).get(subj, []) if c["id"] == ch["id"]), None)
        if not c2: continue
        tl = f'<div class="tier-label"><span class="t">{TIER_LABEL[t]} — {c2["count"]} PYQs · {c2["tests"]} tests</span><span class="line"></span></div>' if len(m["tiers"]) > 1 else ""
        tiles = test_tiles(exam, t, c2) if c2["tests"] else f'<div class="soon">Collecting — {c2["count"]} tagged so far; the first test opens at {MIN_FIRST_SET}.</div>'
        wait = f'<div class="waiting">+{c2["waiting"]} more collected — next test opens at {SET_SIZE}</div>' if c2["waiting"] and c2["tests"] else ""
        blocks.append(f'{tl}<div class="tests" style="--c:{color};--csoft:{color}22">{tiles}</div>{wait}')
    total = sum(c["count"] for t in m["tiers"] for c in index.get(t, {}).get(subj, []) if c["id"] == ch["id"])
    tests = sum(c["tests"] for t in m["tiers"] for c in index.get(t, {}).get(subj, []) if c["id"] == ch["id"])
    years = sorted({y for t in m["tiers"] for c in index.get(t, {}).get(subj, []) if c["id"] == ch["id"] for y in c["years"]})
    yr = f"{years[0]}–{years[-1]}" if len(years) > 1 else (years[0] if years else "")
    siblings = [c for t in m["tiers"] for c in index.get(t, {}).get(subj, []) if c["id"] != ch["id"]][:12]
    seen = set(); sib_links = []
    for c in siblings:
        if c["id"] in seen: continue
        seen.add(c["id"]); sib_links.append(f'<a href="{chapter_file(exam, c["id"])}">{E(c["name"])}<span>{c["count"]} PYQs · {c["tests"]} tests</span></a>')
    name = ch["name"]
    body = hero(exam, [f'<a href="https://trickyssc.com/index.html">Home</a>', f'<a href="https://trickyssc.com/{m["exam_page"]}">{m["name"]}</a>', f'<a href="{hub_file(exam)}">Chapter-wise PYQ</a>', f'<a href="{subject_file(exam, subj)}">{E(label).split(" (")[0]}</a>', f'<span class="here">{E(name)}</span>'],
        f"{m['name']} {E(name)} Previous Year Questions {yr} — Chapter-wise PYQ Tests",
        f"{total} real {m['name']} questions on {E(name)}, taken from the {yr} papers and served as {SET_SIZE}-question tests. Every question shows the paper and shift it came from, and has a step-by-step solution in English and Hindi.",
        [f"<b>{total}</b> PYQs", f"<b>{tests}</b> tests", f"<b>{SET_SIZE}</b> questions / test", f"📅 {yr} papers" if yr else "", "🌐 English + हिंदी"],
        "Free for everyone — sign in to keep your progress and rank.")
    body += f"""<div class="wrap">
<section><h2>{E(name)} — pick a test and start</h2>{LEGEND}{''.join(blocks)}</section>
<section><h2>About these {E(name)} questions</h2>
<p>These are the actual {E(name)} questions SSC asked in the {m['name']} {yr} papers on TrickySSC — not model questions. They sit in paper order: Test 1 has the oldest papers, the last test the newest, and a new test opens at the end whenever {SET_SIZE} more questions are tagged from a newly uploaded paper.</p>
<p>Use the हिंदी button for the Hindi paper's wording, and the View in English toggle inside the test to compare. After submitting, the review shows every solution, your time per question and where you stand on the leaderboard for that test.</p></section>
<section><h2>Other {E(label).split(' (')[0]} chapters</h2><div class="link-row">{''.join(sib_links)}<a href="{subject_file(exam, subj)}">All {E(label).split(' (')[0]} chapters<span>Full chapter list with PYQ counts</span></a></div></section>
<section><h2>More {m['name']} practice</h2><div class="link-row">
<a href="{hub_file(exam)}">Chapter-wise PYQ — all subjects<span>Every chapter, every test</span></a>
<a href="https://trickyssc.com/{m['hub']}">{m['name']} previous year papers<span>Full shift-wise papers</span></a>
{f'<a href="https://trickyssc.com/{m["cw"]}">{m["name"]} chapter-wise tests<span>Model questions, two levels</span></a>' if m['cw'] else ''}
<a href="https://trickyssc.com/{m['mock']}">{m['name']} mock tests<span>Full-length, real sectional timing</span></a></div></section>
</div>"""
    title = f"{m['name']} {name} PYQ {yr} — {total} Previous Year Questions, Chapter-wise Tests | TrickySSC"
    desc = f"Practise {total} real {m['name']} {name} previous year questions ({yr}) as {SET_SIZE}-question tests, in English and Hindi, with solutions and the paper and shift under every question."
    ld = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/index.html"},
        {"@type": "ListItem", "position": 2, "name": m["name"], "item": f"{SITE}/{m['exam_page']}"},
        {"@type": "ListItem", "position": 3, "name": "Chapter-wise PYQ", "item": f"{SITE}/{hub_file(exam)}"},
        {"@type": "ListItem", "position": 4, "name": name, "item": f"{SITE}/{chapter_file(exam, ch['id'])}"}]}, ensure_ascii=False)
    return page(exam, title, desc, chapter_file(exam, ch["id"]), body, index, extra_head=f'<script type="application/ld+json">{ld}</script>', extra_js=ATTEMPT_JS)

def write_if_changed(path, txt):
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if old != txt:
        open(path, "w", encoding="utf-8").write(txt); return True
    return False

def gen_pages(exam, index, counts):
    files = []
    files.append(hub_file(exam)); write_if_changed(os.path.join(ROOT, hub_file(exam)), gen_hub(exam, index, counts))
    for s in all_subjects(index):
        files.append(subject_file(exam, s)); write_if_changed(os.path.join(ROOT, subject_file(exam, s)), gen_subject_page(exam, index, s))
    done = set()
    for t in EXAMS[exam]["tiers"]:
        for s, chs in index.get(t, {}).items():
            for c in chs:
                if c["id"] in done or not c["tests"]: continue
                done.add(c["id"]); files.append(chapter_file(exam, c["id"]))
                write_if_changed(os.path.join(ROOT, chapter_file(exam, c["id"])), gen_chapter_page(exam, index, t, c))
    return files

def update_sitemap(all_files):
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path): return
    s = open(path, encoding="utf-8").read()
    block = "<!-- PYQCH:START (generated by scripts/build_pyq_chapters.py — do not edit by hand) -->\n" + "".join(
        f"  <url>\n    <loc>{SITE}/{f}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{'0.8' if f.endswith('pyq-chapterwise.html') or 'chapter-wise-pyq' in f else '0.6'}</priority>\n  </url>\n" for f in all_files) + "<!-- PYQCH:END -->\n"
    if "<!-- PYQCH:START" in s:
        s = re.sub(r"<!-- PYQCH:START.*?<!-- PYQCH:END -->\n?", lambda _m: block, s, flags=re.S)
    else:
        s = s.replace("</urlset>", block + "</urlset>")
    write_if_changed(path, s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exam", choices=list(EXAMS), help="one exam only")
    ap.add_argument("--dump", help="directory with <exam>-papers.json / <exam>-questions.json (offline build for tests)")
    a = ap.parse_args()
    all_files = []
    for exam in ([a.exam] if a.exam else list(EXAMS)):
        try:
            if a.dump:
                papers = json.load(open(os.path.join(a.dump, f"{exam}-papers.json"), encoding="utf-8"))
                qs = json.load(open(os.path.join(a.dump, f"{exam}-questions.json"), encoding="utf-8"))
            else:
                papers, qs = fetch_exam(exam)
        except Exception as e:
            print(f"{exam}: could not read Firestore ({e}) — leaving existing files as they are", file=sys.stderr); continue
        if not qs:
            print(f"{exam}: no PYQ questions found — skipped"); continue
        index, counts = build_exam(exam, papers, qs)
        all_files += gen_pages(exam, index, counts)
    if all_files:
        existing = json.load(open(os.path.join(OUT, "pages.json"), encoding="utf-8")) if os.path.exists(os.path.join(OUT, "pages.json")) else []
        merged = sorted(set(existing) | set(all_files)) if a.exam else sorted(set(all_files))
        json.dump(merged, open(os.path.join(OUT, "pages.json"), "w", encoding="utf-8"), indent=0)
        update_sitemap(merged)
    print("done")

if __name__ == "__main__":
    main()
