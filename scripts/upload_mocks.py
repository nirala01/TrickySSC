#!/usr/bin/env python3
"""
Put finished mock tests on the site straight from the repo (TSSC-MOCKPUSH-V1).

A mock chat drops one folder per mock into mock-uploads/<exam>/<prefix>/:
    <prefix>-questions-EN.csv  <prefix>-questions-HI.csv
    <prefix>-solutions-EN.csv  <prefix>-solutions-HI.csv
    <prefix>-figures-upload.docx           (only if the mock has figures)
and pushes. The "Upload mocks to Firebase" workflow then runs this script:

  prepare  find every mock folder whose files changed since the last upload
           (ledger: mock-uploads/uploaded.json), check the four CSVs and the docx
           the same way the batch uploaders do, and copy the figures into
           figs/<ab>/<sha>.png (served as https://trickyssc.com/figs/...).
           Writes the work list to .mockpush/plan.json.
  wait     (after the workflow has pushed figs/) wait until every new figure is
           live on trickyssc.com, so no student ever sees a broken image.
  write    write the questions (EN + HI, with solutions and figure URLs) and the
           two mock_tests cards to Firestore, read them back, record the upload in
           mock-uploads/uploaded.json and delete the mock's folder (the files are not
           left on the live site; push the folder again to re-upload a corrected mock).

Writes are the same documents batch-uploader-ntpc-mock.html writes: doc id
<mockId>_qNNN in `questions`, doc id <mockId> in `mock_tests`, merged, so a
re-upload of a corrected mock overwrites in place.

Needs the secret FIREBASE_SERVICE_ACCOUNT (Firebase service-account JSON key).
"""
import argparse, csv, datetime, hashlib, io, json, os, re, sys, time, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT    = Path(__file__).resolve().parent.parent
UPL     = ROOT / "mock-uploads"
LEDGER  = UPL / "uploaded.json"
WORK    = ROOT / ".mockpush"
FIGS    = ROOT / "figs"
SITE    = os.environ.get("SITE_BASE", "https://trickyssc.com")
PROJECT = os.environ.get("FIREBASE_PROJECT", "trickyssc-17bb3")
FS      = f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents"
DB      = f"projects/{PROJECT}/databases/(default)/documents"
IST     = datetime.timezone(datetime.timedelta(hours=5, minutes=30))

# One entry per series this pipeline may publish. The prefix decides the series.
SERIES = {
    "rrb-sm": dict(
        prefix_re=r"^rrb-sm-(20\d\d)-mock-(\d{1,2})$",
        exam="rrb-sm", tier="cbt1", rows=100, title="RRB Station Master — Mock Test {n}",
        series="rrb-sm-2026", module="rrb-sm-mocks", free_upto=3,
        duration=120, per_mark=1, neg_mark=0.33, mixed=True,
        english_rows=range(66, 81),           # reading comprehension stays English on the Hindi paper
        sections=[{"name": "Basic Science, Mathematical and Analytical Capability", "from": 1, "to": 60},
                  {"name": "Logical Capability", "from": 61, "to": 80},
                  {"name": "Mental Reasoning", "from": 81, "to": 100}],
        subjects={"Basic Science", "Mathematics", "Data Analysis and Interpretation",
                  "Logical Reasoning", "Reading Comprehension", "Mental Reasoning"},
    ),
}
QHDR = ["qNum", "subject", "exam", "year", "chapter", "difficulty", "text",
        "option_A", "option_B", "option_C", "option_D", "correct"]
SHDR = ["qNum", "explanation", "trick", "concept"]


def log(*a):
    print(*a, flush=True)


def summary(md):
    print(md, flush=True)
    p = os.environ.get("GITHUB_STEP_SUMMARY")
    if p:
        with open(p, "a", encoding="utf-8") as f:
            f.write(md + "\n")


def fail(msg):
    summary(f"**Stopped:** {msg}")
    sys.exit(1)


# ── reading one mock folder ──────────────────────────────────────────────────
def read_csv(path, hdr):
    raw = path.read_bytes().decode("utf-8-sig")
    rows = list(csv.reader(io.StringIO(raw, newline="")))
    if not rows or [h.strip() for h in rows[0]] != hdr:
        raise ValueError(f"{path.name}: header is not {','.join(hdr)}")
    out = []
    for r in rows[1:]:
        if not any(c.strip() for c in r):
            continue
        out.append({h: (r[i] if i < len(r) else "").strip() for i, h in enumerate(hdr)})
    return out


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def read_docx(path):
    """{qNum: png bytes} — each picture belongs to the last 'Q.n' paragraph above it."""
    z = zipfile.ZipFile(path)
    rels = ET.fromstring(z.read("word/_rels/document.xml.rels"))
    target = {r.get("Id"): r.get("Target") for r in rels}
    body = ET.fromstring(z.read("word/document.xml")).find(W + "body")
    out, cur = {}, None
    for p in body.iter(W + "p"):
        txt = "".join(t.text or "" for t in p.iter(W + "t")).strip()
        m = re.match(r"^Q\.?\s*(\d{1,3})\s*$", txt)
        if m:
            cur = int(m.group(1))
            continue
        for blip in p.iter(A + "blip"):
            rid = blip.get(R + "embed")
            if cur is None or not rid or rid not in target:
                continue
            name = "word/" + target[rid].lstrip("/").replace("word/", "", 1)
            if cur in out:
                raise ValueError(f"docx: two pictures under Q.{cur}")
            out[cur] = z.read(name)
    return out


def png(data):
    from PIL import Image
    im = Image.open(io.BytesIO(data)); im.load()
    if im.width > 1400:
        im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
    if im.mode not in ("1", "L", "LA", "P", "RGB", "RGBA"):
        im = im.convert("RGBA")
    b = io.BytesIO(); im.save(b, "PNG", optimize=True)
    return b.getvalue()


def folder_hash(files):
    h = hashlib.sha256()
    for f in sorted(files, key=lambda p: p.name):
        h.update(f.name.encode()); h.update(hashlib.sha256(f.read_bytes()).digest())
    return h.hexdigest()


def check_mock(folder, cfg):
    prefix = folder.name
    m = re.match(cfg["prefix_re"], prefix)
    if not m:
        raise ValueError(f"folder name {prefix} does not match {cfg['prefix_re']}")
    year, n = m.group(1), int(m.group(2))
    f = {k: folder / f"{prefix}-{k}.csv" for k in ("questions-EN", "questions-HI", "solutions-EN", "solutions-HI")}
    for k, p in f.items():
        if not p.exists():
            raise ValueError(f"{prefix}: {p.name} is missing")
    qe, qh = read_csv(f["questions-EN"], QHDR), read_csv(f["questions-HI"], QHDR)
    se, sh = read_csv(f["solutions-EN"], SHDR), read_csv(f["solutions-HI"], SHDR)
    errs = []
    want = list(range(1, cfg["rows"] + 1))
    for name, rows in (("questions-EN", qe), ("questions-HI", qh), ("solutions-EN", se), ("solutions-HI", sh)):
        nums = [int(r["qNum"]) if r["qNum"].isdigit() else -1 for r in rows]
        if nums != want:
            errs.append(f"{name}: qNum is not 1..{cfg['rows']} in order ({len(rows)} rows)")
    if not errs:
        for e, h in zip(qe, qh):
            k = e["qNum"]
            if e["correct"] not in "ABCD" or len(e["correct"]) != 1:
                errs.append(f"Q{k}: key '{e['correct']}'")
            if e["correct"] != h["correct"]:
                errs.append(f"Q{k}: EN key {e['correct']} but HI key {h['correct']}")
            if e["subject"] not in cfg["subjects"] or h["subject"] != e["subject"]:
                errs.append(f"Q{k}: subject '{e['subject']}' / '{h['subject']}'")
            if e["exam"] != cfg["exam"] or h["exam"] != cfg["exam"]:
                errs.append(f"Q{k}: exam '{e['exam']}'")
            for r, lang in ((e, "EN"), (h, "HI")):
                if not r["text"] or any(not r["option_" + L] for L in "ABCD"):
                    errs.append(f"Q{k} {lang}: empty text or option")
            if int(k) in cfg["english_rows"] and any(e[c] != h[c] for c in ("text", "option_A", "option_B", "option_C", "option_D")):
                errs.append(f"Q{k}: reading-comprehension row differs between EN and HI")
        for rows, lang in ((se, "EN"), (sh, "HI")):
            for r in rows:
                if "&there4;" not in r["explanation"]:
                    errs.append(f"solutions-{lang} Q{r['qNum']}: no verdict line")
    docx = folder / f"{prefix}-figures-upload.docx"
    figs = read_docx(docx) if docx.exists() else {}
    fig_q = [int(r["qNum"]) for r in qe if r["text"].startswith("[FIGURE-BASED]")]
    shared = [int(r["qNum"]) for r in qe if re.search(r"Refer to the figure of Q\.\d+", r["text"])]
    for q in fig_q:
        if q not in shared and q not in figs:
            errs.append(f"Q{q}: figure-based but no picture under Q.{q} in the docx")
    for q in figs:
        if q not in fig_q:
            errs.append(f"docx: picture under Q.{q}, which is not a figure-based question")
    if errs:
        raise ValueError(f"{prefix}: " + "; ".join(errs[:12]) + (f" … ({len(errs)} problems)" if len(errs) > 12 else ""))
    files = list(f.values()) + ([docx] if docx.exists() else [])
    return dict(prefix=prefix, year=year, n=n, rows=dict(qEn=qe, qHi=qh, sEn=se, sHi=sh),
                figs=figs, hash=folder_hash(files))


# ── stage 1: prepare ─────────────────────────────────────────────────────────
def load_ledger():
    return json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {}


def cmd_prepare(a):
    ledger = load_ledger()
    WORK.mkdir(exist_ok=True)
    plan = []
    for exam, cfg in SERIES.items():
        base = UPL / exam
        if not base.is_dir():
            continue
        for folder in sorted(p for p in base.iterdir() if p.is_dir()):
            if a.only and folder.name not in a.only.split(","):
                continue
            try:
                mk = check_mock(folder, cfg)
            except Exception as e:
                fail(str(e))
            done = ledger.get(mk["prefix"], {})
            if done.get("hash") == mk["hash"] and not a.force:
                log(f"{mk['prefix']}: already on the site (unchanged) — skipped")
                continue
            urls = {}
            for q, data in sorted(mk["figs"].items()):
                b = png(data)
                sha = hashlib.sha256(b).hexdigest()
                rel = f"figs/{sha[:2]}/{sha[2:22]}.png"
                p = ROOT / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                if not p.exists():
                    p.write_bytes(b)
                urls[q] = f"{SITE}/{rel}"
            plan.append(dict(exam=exam, prefix=mk["prefix"], year=mk["year"], n=mk["n"], hash=mk["hash"],
                             folder=str(folder.relative_to(ROOT)), figures=urls))
            log(f"{mk['prefix']}: checked — 4 CSVs × {cfg['rows']} rows, {len(urls)} figure(s)")
    (WORK / "plan.json").write_text(json.dumps(plan, indent=1), encoding="utf-8")
    if not plan:
        summary("Nothing new to upload.")
    else:
        summary("Mocks to upload: " + ", ".join(p["prefix"] for p in plan))


# ── stage 2: wait for the figures ────────────────────────────────────────────
def cmd_wait(a):
    import requests
    plan = json.loads((WORK / "plan.json").read_text(encoding="utf-8"))
    urls = sorted({u for p in plan for u in p["figures"].values()})
    if not urls:
        return
    t0, left = time.time(), list(urls)
    while left and time.time() - t0 < a.timeout:
        nxt = []
        for u in left:
            try:
                r = requests.head(u, timeout=20, allow_redirects=True)
                if r.status_code != 200:
                    nxt.append(u)
            except requests.RequestException:
                nxt.append(u)
        left = nxt
        if left:
            log(f"  {len(left)}/{len(urls)} figure(s) not live yet — waiting")
            time.sleep(20)
    if left:
        fail(f"{len(left)} figure(s) still not live after {a.timeout}s, e.g. {left[0]}. Re-run the workflow.")
    log(f"All {len(urls)} figure(s) are live.")


# ── stage 3: write to Firestore ──────────────────────────────────────────────
_tok = {"v": None, "exp": 0}


def token():
    if os.environ.get("FS_TOKEN"):
        return os.environ["FS_TOKEN"]
    if _tok["v"] and time.time() < _tok["exp"] - 120:
        return _tok["v"]
    raw = os.environ.get("FIREBASE_SERVICE_ACCOUNT", "").strip()
    if not raw:
        fail("the FIREBASE_SERVICE_ACCOUNT secret is missing.")
    from google.oauth2 import service_account
    import google.auth.transport.requests as gtr
    creds = service_account.Credentials.from_service_account_info(
        json.loads(raw), scopes=["https://www.googleapis.com/auth/datastore"])
    creds.refresh(gtr.Request())
    _tok["v"], _tok["exp"] = creds.token, time.time() + 3000
    return creds.token


def fs(method, url, body=None, tries=5):
    import requests
    for i in range(tries):
        try:
            r = requests.request(method, url, json=body, timeout=120,
                                 headers={"Authorization": "Bearer " + token()})
            if r.status_code in (429, 500, 502, 503, 504):
                raise RuntimeError(f"HTTP {r.status_code}")
            if r.status_code != 200:
                fail(f"Firestore error {r.status_code}: {r.text[:400]}")
            return r.json()
        except Exception as e:
            if i == tries - 1:
                raise
            log(f"  Firestore busy ({e}) — retrying")
            time.sleep(3 * (i + 1))


def tv(v):
    """Python value -> Firestore typed value."""
    if isinstance(v, bool):
        return {"booleanValue": v}
    if isinstance(v, int):
        return {"integerValue": str(v)}
    if isinstance(v, float):
        return {"doubleValue": v}
    if isinstance(v, datetime.datetime):
        return {"timestampValue": v.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}
    if isinstance(v, dict):
        return {"mapValue": {"fields": {k: tv(x) for k, x in v.items()}}}
    if isinstance(v, (list, tuple)):
        return {"arrayValue": {"values": [tv(x) for x in v]}}
    if v is None:
        return {"nullValue": None}
    return {"stringValue": str(v)}


def fpath(k):
    return k if re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", k) else "`" + k + "`"


def upsert(doc_path, data):
    return {"update": {"name": f"{DB}/{doc_path}", "fields": {k: tv(v) for k, v in data.items()}},
            "updateMask": {"fieldPaths": [fpath(k) for k in data]}}


def existing_ids(mock_id):
    q = {"structuredQuery": {"from": [{"collectionId": "questions"}],
                             "where": {"fieldFilter": {"field": {"fieldPath": "mockId"}, "op": "EQUAL",
                                                       "value": {"stringValue": mock_id}}},
                             "select": {"fields": [{"fieldPath": "qNum"}]}, "limit": 1000}}
    rows = fs("POST", f"{FS}:runQuery", q)
    return {r["document"]["name"].rsplit("/", 1)[-1] for r in rows if r.get("document")}


def commit(writes):
    for i in range(0, len(writes), 400):
        fs("POST", f"{FS}:commit", {"writes": writes[i:i + 400]})


def cmd_write(a):
    plan = json.loads((WORK / "plan.json").read_text(encoding="utf-8"))
    if not plan:
        log("Nothing to write.")
        return
    ledger = load_ledger()
    lines = ["| Mock | EN | HI | Figures | Cards |", "|---|---|---|---|---|"]
    for p in plan:
        cfg = SERIES[p["exam"]]
        mk = check_mock(ROOT / p["folder"], cfg)
        figs = {int(k): v for k, v in p["figures"].items()}
        now = datetime.datetime.now(datetime.timezone.utc)
        counts = {}
        for lang in ("en", "hi"):
            mid = f"{cfg['exam']}_{cfg['tier']}_mock{p['n']}_{lang}"
            have = existing_ids(mid)
            qrows = mk["rows"]["qEn" if lang == "en" else "qHi"]
            sol = {int(r["qNum"]): r for r in mk["rows"]["sEn" if lang == "en" else "sHi"]}
            writes, keep = [], set()
            for r in qrows:
                n = int(r["qNum"])
                did = f"{mid}_q{n:03d}"
                keep.add(did)
                opts = {L: r["option_" + L] for L in "ABCD"}
                d = dict(mockId=mid, exam=cfg["exam"], tier=cfg["tier"], type="mock", language=lang, lang=lang,
                         mockNum=p["n"], mockSeriesNum=p["n"], qNum=n, subject=r["subject"],
                         chapter=r["chapter"], difficulty=r["difficulty"] or "medium", text=r["text"],
                         options=opts, option_A=opts["A"], option_B=opts["B"], option_C=opts["C"],
                         option_D=opts["D"], correct=r["correct"].upper(), year=p["year"], updatedAt=now,
                         explanation=sol[n]["explanation"], trick=sol[n]["trick"], concept=sol[n]["concept"],
                         section=next(s["name"] for s in cfg["sections"] if s["from"] <= n <= s["to"]))
                if did not in have:
                    d["createdAt"] = now
                if n in figs:
                    d.update(imageUrl=figs[n], optionImages={L: "" for L in "ABCD"}, solutionImage="")
                writes.append(upsert(f"questions/{did}", d))
            for gone in sorted(have - keep):                       # a corrected mock with fewer rows
                writes.append({"delete": f"{DB}/questions/{gone}"})
            commit(writes)
            subj = {}
            for r in qrows:
                subj[r["subject"]] = subj.get(r["subject"], 0) + 1
            card = dict(mockId=mid, exam=cfg["exam"], tier=cfg["tier"], lang=lang, language=lang,
                        seriesNum=p["n"], mockNum=p["n"], title=cfg["title"].format(n=p["n"]),
                        totalQuestions=len(qrows), subjectCounts=subj, duration=cfg["duration"],
                        totalMarks=round(len(qrows) * cfg["per_mark"]), marksPerQuestion=cfg["per_mark"],
                        negativeMarks=cfg["neg_mark"], series=cfg["series"], paywallModule=cfg["module"],
                        sessions=[{"from": 1, "to": len(qrows), "minutes": cfg["duration"], "negative": cfg["neg_mark"]}],
                        sections=cfg["sections"], mixedOrder=cfg["mixed"], isFree=p["n"] <= cfg["free_upto"],
                        isPublished=True, year=p["year"], updatedAt=now)
            commit([upsert(f"mock_tests/{mid}", card)])
            # read back
            back = existing_ids(mid)
            if back != keep:
                fail(f"{p['prefix']} {lang}: read back {len(back)} questions, expected {len(keep)}")
            c = fs("GET", f"{FS}/mock_tests/{mid}")
            if c.get("fields", {}).get("isPublished", {}).get("booleanValue") is not True:
                fail(f"{p['prefix']} {lang}: mock card not published after write")
            counts[lang] = len(back)
        ledger[p["prefix"]] = dict(hash=p["hash"], exam=cfg["exam"], mockNum=p["n"],
                                   mockIds=[f"{cfg['exam']}_{cfg['tier']}_mock{p['n']}_{l}" for l in ("en", "hi")],
                                   questions=counts, figures=len(figs),
                                   uploadedAt=datetime.datetime.now(IST).strftime("%Y-%m-%d %H:%M IST"))
        lines.append(f"| {p['prefix']} | {counts['en']} | {counts['hi']} | {len(figs)} | published |")
        # The files are in Firestore now; take them out of the repo so the live site never serves them.
        import shutil
        shutil.rmtree(ROOT / p["folder"], ignore_errors=True)
        log(f"{p['prefix']}: {counts['en']} EN + {counts['hi']} HI questions and both cards are in Firestore")
    LEDGER.write_text(json.dumps(ledger, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    summary("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("prepare"); p1.add_argument("--only", default=""); p1.add_argument("--force", action="store_true")
    p2 = sub.add_parser("wait"); p2.add_argument("--timeout", type=int, default=1200)
    sub.add_parser("write")
    a = ap.parse_args()
    {"prepare": cmd_prepare, "wait": cmd_wait, "write": cmd_write}[a.cmd](a)
