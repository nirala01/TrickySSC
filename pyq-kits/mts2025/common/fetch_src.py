"""Split the GitHub source (akarohitmishra/repeatermock-subjectwise-db, SSC-MTS/pre/*/questions.jsonl, year 2025)
into one JSON per shift: src/<dd>-<mon>-s<n>.json keyed 'SUBJ|n'.
usage: python fetch_src.py <path-to-repeatermock-clone> <kit/src dir>
Clone first:  GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 --filter=blob:none --sparse https://github.com/akarohitmishra/repeatermock-subjectwise-db rm
              git -C rm sparse-checkout set SSC-MTS
"""
import sys, os, json, re, collections
root, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
P = collections.defaultdict(dict)
for s in ('MATH', 'REAS', 'GK', 'ENG'):
    for line in open(os.path.join(root, 'SSC-MTS', 'pre', s, 'questions.jsonl'), encoding='utf-8'):
        d = json.loads(line)
        if str(d['year']) != '2025': continue
        m = re.search(r'Held_On_(\d\d)_(\w{3})_2026_Shift_(\d)', d['paper'])
        P[f'{m.group(1)}-{m.group(2).lower()}-s{m.group(3)}'][f'{s}|{d["n"]}'] = d
for k, v in sorted(P.items()):
    assert len(v) == 90, (k, len(v))
    json.dump(v, open(os.path.join(out, k + '.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print(k, len(v))
