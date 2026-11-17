#!/usr/bin/env python3
"""One-off: upload the topic-wise current affairs questions (ca-topics/kit/bank/*.csv) to Firestore
exactly as admin-chapterwise.html's CSV import does (questions collection, same fields), but with
fixed doc ids  ca_<chapter>_q<NNN>  so a rerun overwrites instead of duplicating.
Stops before writing if questions for any ca.* chapter already exist under other ids.
Runs in GitHub Actions with FIREBASE_SERVICE_ACCOUNT."""
import csv, glob, json, os, re, sys, time, collections
import requests
from google.oauth2 import service_account
import google.auth.transport.requests as gtr

PROJECT = "trickyssc-17bb3"
DB = f"projects/{PROJECT}/databases/(default)/documents"
BASE = f"https://firestore.googleapis.com/v1/{DB}"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
creds = service_account.Credentials.from_service_account_info(
    json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"]), scopes=["https://www.googleapis.com/auth/datastore"])

def tok():
    if not creds.valid: creds.refresh(gtr.Request())
    return creds.token

def H(): return {"Authorization": "Bearer " + tok()}

def val(v):
    if isinstance(v, bool): return {"booleanValue": v}
    if isinstance(v, int): return {"integerValue": str(v)}
    if isinstance(v, dict): return {"mapValue": {"fields": {k: val(x) for k, x in v.items()}}}
    return {"stringValue": "" if v is None else str(v)}

def post(url, body):
    for t in range(6):
        r = requests.post(url, json=body, headers=H(), timeout=120)
        if r.status_code == 200: return r.json()
        print("retry", r.status_code, r.text[:300]); time.sleep(3 * (t + 1))
    sys.exit("Firestore call failed: " + r.text[:500])

def ids_for(chapter):
    out = []
    j = post(BASE + ":runQuery", {"structuredQuery": {"from": [{"collectionId": "questions"}],
          "where": {"fieldFilter": {"field": {"fieldPath": "chapterId"}, "op": "EQUAL", "value": {"stringValue": chapter}}},
          "select": {"fields": [{"fieldPath": "__name__"}]}}})
    for row in j:
        if row.get("document"): out.append(row["document"]["name"].rsplit("/", 1)[1])
    return out

idx = json.load(open(os.path.join(ROOT, "ca-topics/index.json"), encoding="utf-8"))
NAME = {t["id"]: t["name"] for t in idx["topics"]}
rows = []
for f in sorted(glob.glob(os.path.join(ROOT, "ca-topics/kit/bank/*.csv"))):
    with open(f, encoding="utf-8", newline="") as fh:
        rows += list(csv.DictReader(fh))
want = collections.Counter(r["chapter"] for r in rows)
print("rows:", len(rows), dict(want))
assert set(want) <= set(NAME), "unknown chapter in bank"

def doc_id(r): return f"ca_{r['chapter'].replace('.', '_').replace('-', '_')}_q{int(r['qNum']):03d}"
mine = {doc_id(r) for r in rows}
assert len(mine) == len(rows), "duplicate doc ids"

# 1. guard against duplicates from an earlier manual upload
clash = {}
for ch in want:
    other = [i for i in ids_for(ch) if i not in mine]
    if other: clash[ch] = len(other)
if clash:
    sys.exit(f"STOP: these chapters already have questions under other ids (would duplicate): {clash}")

# 2. write (same fields as admin-chapterwise.html importCSV)
writes = []
for r in rows:
    ch = r["chapter"]
    data = {"text": r["text"], "exam": r["exam"] or "ssc-cgl", "tier": "tier1", "year": r["year"],
            "type": r["type"] or "chapterwise", "subject": r["subject"] or "gk", "chapter": ch,
            "language": r["language"] or "en", "chapterId": ch, "chapterName": NAME[ch],
            "level": int(r["level"] or 1), "testNum": int(r["testNum"]), "difficulty": r["difficulty"] or "medium",
            "qNum": int(r["qNum"]),
            "options": {"A": r["option_A"], "B": r["option_B"], "C": r["option_C"], "D": r["option_D"]},
            "correct": r["correct"], "explanation": r["explanation"], "trick": "", "imageUrl": "", "concept": ""}
    writes.append({"update": {"name": f"{DB}/questions/{doc_id(r)}", "fields": {k: val(v) for k, v in data.items()}},
                   "updateTransforms": [{"fieldPath": "createdAt", "setToServerValue": "REQUEST_TIME"}]})
for i in range(0, len(writes), 400):
    post(BASE + ":commit", {"writes": writes[i:i + 400]})
    print(f"written {min(i + 400, len(writes))}/{len(writes)}")

# 3. verify
bad = {}
for ch, n in want.items():
    got = len(ids_for(ch))
    print(f"{ch}: {got} in Firestore (expected {n})")
    if got != n: bad[ch] = (got, n)
if bad: sys.exit(f"COUNT MISMATCH: {bad}")
print("ALL OK:", len(rows), "questions")
