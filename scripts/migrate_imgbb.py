#!/usr/bin/env python3
"""
Move every imgbb figure used by TrickySSC tests into this repo (figs/) and point
the questions in Firestore at the new copies (https://trickyssc.com/figs/...).

Runs in GitHub Actions (migrate-imgbb.yml) in three steps:

  download  find questions that still link to i.ibb.co, download each figure once,
            save it as figs/<ab>/<hash>.<ext>, record old -> new in figs/map.json,
            and write the Firestore changes to .migrate/patches.json
  wait      (after the workflow has pushed figs/) wait until the new files are
            live on trickyssc.com, so no student ever gets a broken link
  rewrite   apply .migrate/patches.json to Firestore (only the changed fields,
            and only if the question was not edited since it was read)

Scan modes
  quick  only questions whose imageUrl / solutionImage / optionImages.A-D still
         start with the imgbb address (cheap: reads only those docs)
  full   every question, every field (also catches imgbb links inside question
         text, options and solutions, e.g. [IMG]...[/IMG] or <img src=...>)

Needs the secret FIREBASE_SERVICE_ACCOUNT (the JSON key of the Firebase
service account) for the Firestore reads and writes.
"""
import argparse, concurrent.futures as cf, hashlib, io, json, os, re, sys, time
from pathlib import Path

import requests

PROJECT   = os.environ.get("FIREBASE_PROJECT", "trickyssc-17bb3")
FS        = os.environ.get("FS_BASE", f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents")
SITE      = os.environ.get("SITE_BASE", "https://trickyssc.com")
ROOT      = Path(__file__).resolve().parent.parent
FIGS      = ROOT / "figs"
MAP_FILE  = FIGS / "map.json"
MISS_FILE = FIGS / "missing.json"   # imgbb links that answered 404: {url: {"days": [...]}}
WORK      = ROOT / ".migrate"
COLL      = "questions"

IBB_RE    = re.compile(r"https?://i\.ibb\.co/[^\s\"'<>\[\]()\\]*[^\s\"'<>\[\]()\\.,;:!?]", re.I)
IBB_PFX   = ["https://i.ibb.co/", "http://i.ibb.co/"]
QUICK_FIELDS = ["imageUrl", "solutionImage",
                "optionImages.A", "optionImages.B", "optionImages.C", "optionImages.D"]
EXT       = {"image/png": "png", "image/jpeg": "jpg", "image/jpg": "jpg", "image/gif": "gif",
             "image/webp": "webp", "image/svg+xml": "svg", "image/bmp": "png"}
MAX_W     = 1400          # wider figures are scaled down (shown at <= ~600 css px)
MAX_BYTES = 8_000_000
SITE_CAP  = 800_000_000   # GitHub Pages sites must stay under 1 GB
SAME_HASH_LIMIT = 12      # one picture behind more than this many different links
                          # is almost surely imgbb's "unavailable" placeholder


def log(*a):
    print(*a, flush=True)


def summary(md):
    """Append to the Actions run summary (and print it)."""
    print(md, flush=True)
    p = os.environ.get("GITHUB_STEP_SUMMARY")
    if p:
        with open(p, "a", encoding="utf-8") as f:
            f.write(md + "\n")


# ── auth ─────────────────────────────────────────────────────────────────────
_tok = {"v": None, "exp": 0}

def token():
    if os.environ.get("FS_TOKEN"):                       # local testing
        return os.environ["FS_TOKEN"]
    if _tok["v"] and time.time() < _tok["exp"] - 120:
        return _tok["v"]
    raw = os.environ.get("FIREBASE_SERVICE_ACCOUNT", "").strip()
    if not raw:
        sys.exit("FIREBASE_SERVICE_ACCOUNT secret is missing — add the service-account JSON "
                 "in GitHub: Settings → Secrets and variables → Actions.")
    from google.oauth2 import service_account
    import google.auth.transport.requests as gtr
    creds = service_account.Credentials.from_service_account_info(
        json.loads(raw), scopes=["https://www.googleapis.com/auth/datastore"])
    creds.refresh(gtr.Request())
    _tok["v"], _tok["exp"] = creds.token, time.time() + 3000
    return creds.token


def fs_post(url, body, tries=5):
    for i in range(tries):
        try:
            r = requests.post(url, json=body, timeout=120,
                              headers={"Authorization": "Bearer " + token()})
            if r.status_code in (429, 500, 502, 503, 504):
                raise RuntimeError(f"HTTP {r.status_code}")
            if r.status_code != 200:
                sys.exit(f"Firestore error {r.status_code}: {r.text[:500]}")
            return r.json()
        except (requests.RequestException, RuntimeError) as e:
            if i == tries - 1:
                raise
            log(f"  Firestore busy ({e}) — retrying")
            time.sleep(3 * (i + 1))


# ── Firestore typed-value helpers ────────────────────────────────────────────
def walk_strings(v, fn):
    """Return a copy of typed value v with fn applied to every string inside it."""
    if "stringValue" in v:
        return {"stringValue": fn(v["stringValue"])}
    if "arrayValue" in v:
        return {"arrayValue": {"values": [walk_strings(x, fn) for x in v["arrayValue"].get("values", [])]}}
    if "mapValue" in v:
        return {"mapValue": {"fields": {k: walk_strings(x, fn) for k, x in v["mapValue"].get("fields", {}).items()}}}
    return v


def ibb_urls(v):
    found = []
    walk_strings(v, lambda s: (found.extend(IBB_RE.findall(s)), s)[1])
    return found


def fpath(name):
    return name if re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", name) else "`" + name.replace("`", "\\`") + "`"


# ── scanning ─────────────────────────────────────────────────────────────────
def run_query(where=None, order_field=None, page=300):
    """Yield whole question documents, paged."""
    cursor = None
    while True:
        order = ([{"field": {"fieldPath": order_field}, "direction": "ASCENDING"}] if order_field else []) + \
                [{"field": {"fieldPath": "__name__"}, "direction": "ASCENDING"}]
        q = {"from": [{"collectionId": COLL}], "orderBy": order, "limit": page}
        if where:
            q["where"] = where
        if cursor:
            q["startAt"] = {"values": cursor, "before": False}
        rows = fs_post(f"{FS}:runQuery", {"structuredQuery": q})
        docs = [r["document"] for r in rows if r.get("document")]
        for d in docs:
            yield d
        if len(docs) < page:
            return
        last = docs[-1]
        cursor = []
        if order_field:
            v = {"mapValue": {"fields": last.get("fields", {})}}
            for part in order_field.split("."):
                v = v.get("mapValue", {}).get("fields", {}).get(part, {})
            cursor.append(v or {"nullValue": None})
        cursor.append({"referenceValue": last["name"]})


def range_filter(field, prefix):
    hi = prefix[:-1] + chr(ord(prefix[-1]) + 1)
    return {"compositeFilter": {"op": "AND", "filters": [
        {"fieldFilter": {"field": {"fieldPath": field}, "op": "GREATER_THAN_OR_EQUAL", "value": {"stringValue": prefix}}},
        {"fieldFilter": {"field": {"fieldPath": field}, "op": "LESS_THAN", "value": {"stringValue": hi}}}]}}


def scan(full):
    docs = {}
    if full:
        log("Full scan of every question …")
        n = 0
        for d in run_query():
            n += 1
            if n % 2000 == 0:
                log(f"  {n} questions read")
            if any(ibb_urls(v) for v in d.get("fields", {}).values()):
                docs[d["name"]] = d
        log(f"  {n} questions read, {len(docs)} still use imgbb")
    else:
        log("Quick scan (figure fields that still point to imgbb) …")
        for f in QUICK_FIELDS:
            for p in IBB_PFX:
                for d in run_query(range_filter(f, p), order_field=f):
                    docs[d["name"]] = d
        log(f"  {len(docs)} questions still use imgbb")
    return docs


# ── downloading ──────────────────────────────────────────────────────────────
UA = {"User-Agent": "TrickySSC-figure-migration/1.0 (+https://trickyssc.com)"}

def _get(url):
    r = requests.get(url, timeout=(10, 30), headers=UA, allow_redirects=True)
    ct = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
    if r.status_code == 404:
        raise FileNotFoundError("404 — image deleted on imgbb")
    if r.status_code != 200 or not ct.startswith("image/") or len(r.content) <= 60:
        raise RuntimeError(f"HTTP {r.status_code} {ct}")
    if len(r.content) > MAX_BYTES:
        raise RuntimeError(f"too large ({len(r.content)} bytes)")
    return r.content, ct


def fetch(url, tries=2):
    """Return (bytes, content_type) or raise.
    Tries imgbb directly; if imgbb is slow or refuses, gets the same file through the
    wsrv.nl image cache (the same one mock-test.html uses)."""
    last, gone = None, False
    via = "https://wsrv.nl/?url=" + requests.utils.quote(re.sub(r"^https?://", "", url), safe="")
    for i in range(tries):
        for src in (url, via):
            try:
                return _get(src)
            except FileNotFoundError as e:
                gone, last = True, e
            except Exception as e:
                last = e
        if gone:
            break
        time.sleep(3)
    if gone:
        raise FileNotFoundError("404 — image deleted on imgbb")
    raise last


def shrink(data, ct):
    """Scale down very wide figures and re-save PNGs with better compression (lossless)."""
    if ct not in ("image/png", "image/jpeg", "image/jpg", "image/bmp"):
        return data, ct
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(data))
        im.load()
        changed = False
        if im.width > MAX_W:
            h = round(im.height * MAX_W / im.width)
            im = im.resize((MAX_W, h), Image.LANCZOS)
            changed = True
        out = io.BytesIO()
        if ct in ("image/png", "image/bmp"):
            if im.mode not in ("1", "L", "LA", "P", "RGB", "RGBA"):
                im = im.convert("RGBA")
            im.save(out, "PNG", optimize=True)
            ct = "image/png"
        elif changed:
            if im.mode not in ("RGB", "L"):
                im = im.convert("RGB")
            im.save(out, "JPEG", quality=88, optimize=True, progressive=True)
        else:
            return data, ct
        new = out.getvalue()
        return (new, ct) if (changed or len(new) < len(data)) else (data, ct)
    except Exception as e:
        log(f"  (kept original bytes: {e})")
        return data, ct


def figs_size():
    return sum(p.stat().st_size for p in FIGS.rglob("*") if p.is_file()) if FIGS.exists() else 0


def cmd_download(a):
    FIGS.mkdir(exist_ok=True)
    WORK.mkdir(exist_ok=True)
    mp = json.loads(MAP_FILE.read_text()) if MAP_FILE.exists() else {}
    full = a.full == "yes" or (a.full == "auto" and time.gmtime().tm_wday == 6)   # Sundays: full
    docs = scan(full)

    urls = sorted({u for d in docs.values() for v in d.get("fields", {}).values() for u in ibb_urls(v)})
    miss = json.loads(MISS_FILE.read_text()) if MISS_FILE.exists() else {}
    # figures that answered 404 before go last, so new ones are always tried first
    todo = sorted((u for u in urls if u not in mp), key=lambda u: len(miss.get(u, {}).get("days", [])))[: a.max_images]
    log(f"{len(urls)} different imgbb links in use; {len(urls) - len([u for u in urls if u not in mp])} already copied; downloading {len(todo)}")

    got, failed, gone = {}, {}, []
    def one(u):
        time.sleep(0.4)          # be gentle: too many requests in a row make imgbb refuse
        try:
            return u, fetch(u), None
        except Exception as e:
            return u, None, e
    # Never let one run spend hours here: after the time budget, keep what we have
    # (it is saved and used) and leave the rest for the next run.
    deadline = time.time() + a.budget_min * 60
    stopped = 0
    ex = cf.ThreadPoolExecutor(max_workers=3)
    futs = [ex.submit(one, u) for u in todo]
    try:
        for i, f in enumerate(cf.as_completed(futs, timeout=max(1, deadline - time.time())), 1):
            u, res, err = f.result()
            if res:
                got[u] = res
            elif isinstance(err, FileNotFoundError):
                gone.append(u)
            else:
                failed[u] = str(err)
            if i % 25 == 0 or i == len(todo):
                log(f"  {i}/{len(todo)} done — {len(got)} ok, {len(failed)} failed, {len(gone)} deleted on imgbb")
    except cf.TimeoutError:
        stopped = sum(1 for f in futs if not f.done())
        log(f"  time budget reached — {stopped} figures left for the next run")
    ex.shutdown(wait=False, cancel_futures=True)

    # imgbb sometimes answers with its own "service unavailable" picture (HTTP 200).
    # The same picture behind many different links is that placeholder — never save it.
    by_hash = {}
    for u, (data, ct) in got.items():
        by_hash.setdefault(hashlib.sha256(data).hexdigest(), []).append(u)
    suspicious = {h for h, us in by_hash.items() if len(us) > SAME_HASH_LIMIT}
    held = []
    for h in suspicious:
        held += by_hash[h]
        for u in by_hash[h]:
            got.pop(u, None)

    new_files, cap_hit = [], False
    size = figs_size()
    for u in sorted(got):
        data, ct = shrink(*got[u])
        h = hashlib.sha256(data).hexdigest()[:20]
        rel = f"figs/{h[:2]}/{h}.{EXT.get(ct, 'png')}"
        p = ROOT / rel
        if not p.exists():
            if size + len(data) > SITE_CAP:
                cap_hit = True
                break
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
            size += len(data)
            new_files.append(rel)
        mp[u] = rel
    MAP_FILE.write_text(json.dumps(dict(sorted(mp.items())), indent=0, ensure_ascii=False) + "\n")

    # Firestore changes: every imgbb link that now has a copy → its new address
    def swap(s):
        return IBB_RE.sub(lambda m: f"{SITE}/{mp[m.group(0)]}" if m.group(0) in mp else m.group(0), s)
    patches = []
    for name, d in docs.items():
        changed = {}
        for f, v in d.get("fields", {}).items():
            nv = walk_strings(v, swap)
            if nv != v:
                changed[f] = nv
        if changed:
            patches.append({"name": name, "updateTime": d.get("updateTime"), "fields": changed})
    (WORK / "patches.json").write_text(json.dumps(patches))
    (WORK / "new_files.txt").write_text("\n".join(new_files))

    left = len([u for u in urls if u not in mp])
    summary("## imgbb → trickyssc.com/figs\n")
    summary(f"- Scan: **{'full' if full else 'quick'}** — {len(docs)} questions still link to imgbb, "
            f"{len(urls)} different figures")
    summary(f"- New figures saved this run: **{len(new_files)}** (figs/ is now {size/1e6:.1f} MB)")
    summary(f"- Questions to update in Firestore: **{len(patches)}**")
    if failed:
        summary(f"- ⚠️ {len(failed)} figure(s) could not be downloaded now (imgbb busy?) — the next run tries again")
        for u, e in list(failed.items())[:15]:
            summary(f"  - {u} — {e}")
    # A single 404 is not proof: imgbb also answers 404 when it is refusing too many
    # requests. A figure counts as deleted only after 404s on 3 different days.
    today = time.strftime("%Y-%m-%d")
    for u in got:
        miss.pop(u, None)
    for u in gone:
        days = miss.setdefault(u, {"days": []})["days"]
        if today not in days:
            days.append(today)
    for u in list(miss):
        if u not in urls:
            miss.pop(u)
    if not a.dry_run:
        MISS_FILE.write_text(json.dumps(dict(sorted(miss.items())), indent=0) + "\n")
    sure = sorted(u for u in gone if len(miss[u]["days"]) >= 3)
    if gone:
        summary(f"- {len(gone)} figure(s) answered 404 (not found) this run — retried on the next days; "
                f"{len(sure)} of them have now failed on 3 different days")
    if sure:
        summary("- ❌ Deleted on imgbb (404 on 3 different days) — upload these figures again in admin:")
        for u in sure[:60]:
            ids = [n.rsplit('/', 1)[-1] for n, d in docs.items()
                   if any(u in ibb_urls(v) for v in d.get('fields', {}).values())]
            summary(f"  - {u} → question {', '.join(ids[:5])}")
    if held:
        summary(f"- ⚠️ {len(held)} link(s) returned the same picture (imgbb's 'unavailable' placeholder?) — skipped, retried next run")
    if cap_hit:
        summary("- 🛑 Stopped: figs/ is near the GitHub Pages size limit (1 GB). Tell Claude before running again.")
    if stopped:
        summary(f"- ⏱ Time budget reached: {stopped} figures were not tried yet — run the workflow again to continue")
    if left - len(failed) - len(gone) - len(held) - stopped > 0 and not cap_hit:
        summary(f"- {left} figure(s) still to copy — they are done in the next runs (limit {a.max_images} per run)")
    if a.dry_run:
        summary("- **Dry run**: nothing will be committed or changed in Firestore.")


# ── wait until live ──────────────────────────────────────────────────────────
def cmd_wait(a):
    files = [l for l in (WORK / "new_files.txt").read_text().split("\n") if l] if (WORK / "new_files.txt").exists() else []
    if not files:
        mp = json.loads(MAP_FILE.read_text()) if MAP_FILE.exists() else {}
        files = list(dict.fromkeys(mp.values()))[-1:]
    if not files:
        log("Nothing to wait for.")
        return
    probe = list(dict.fromkeys([files[0], files[len(files) // 2], files[-1]]))
    log(f"Waiting for GitHub Pages to publish {len(files)} new files (checking {len(probe)}) …")
    deadline = time.time() + a.timeout
    while time.time() < deadline:
        ok = 0
        for rel in probe:
            try:
                r = requests.head(f"{SITE}/{rel}", timeout=30, headers=UA, allow_redirects=True)
                ok += r.status_code == 200
            except requests.RequestException:
                pass
        if ok == len(probe):
            log("  live ✓")
            return
        time.sleep(20)
    sys.exit("The new figures did not go live on trickyssc.com in time — Firestore was NOT changed. "
             "Run the workflow again later.")


# ── rewrite Firestore ────────────────────────────────────────────────────────
def cmd_rewrite(a):
    pf = WORK / "patches.json"
    patches = json.loads(pf.read_text()) if pf.exists() else []
    if not patches:
        summary("- Firestore: nothing to update.")
        return
    done = conflict = bad = 0
    for i in range(0, len(patches), 200):
        chunk = patches[i:i + 200]
        writes = []
        for p in chunk:
            w = {"update": {"name": p["name"], "fields": p["fields"]},
                 "updateMask": {"fieldPaths": [fpath(f) for f in p["fields"]]}}
            if p.get("updateTime"):
                w["currentDocument"] = {"updateTime": p["updateTime"]}   # skip if edited meanwhile
            writes.append(w)
        res = fs_post(f"{FS}:batchWrite", {"writes": writes})
        for st in res.get("status", [{}] * len(writes)):
            code = st.get("code", 0)
            if code == 0:
                done += 1
            elif code == 9:          # FAILED_PRECONDITION: question changed since it was read
                conflict += 1
            else:
                bad += 1
                log(f"  write failed: {st}")
        log(f"  {min(i + 200, len(patches))}/{len(patches)} questions written")
    summary(f"- Firestore: **{done}** questions now use trickyssc.com figures"
            + (f"; {conflict} were edited during the run and will be done next run" if conflict else "")
            + (f"; ⚠️ {bad} writes failed (see log)" if bad else ""))
    if bad:
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    d = sp.add_parser("download")
    d.add_argument("--full", default="auto", choices=["yes", "no", "auto"])
    d.add_argument("--max-images", type=int, default=4000)
    d.add_argument("--dry-run", action="store_true")
    d.add_argument("--budget-min", type=float, default=40)
    w = sp.add_parser("wait")
    w.add_argument("--timeout", type=int, default=900)
    sp.add_parser("rewrite")
    a = ap.parse_args()
    {"download": cmd_download, "wait": cmd_wait, "rewrite": cmd_rewrite}[a.cmd](a)


if __name__ == "__main__":
    main()
