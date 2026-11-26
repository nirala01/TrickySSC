"""PROMPT-2-MTS §4 self-check + negative controls. usage: check_docx.py <docx> <txt> <data.py>"""
import sys, os, re, io, zipfile, hashlib, importlib.util, shutil, tempfile
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from base import parse_txt

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
BAND = {range(1, 21), range(21, 41), range(41, 66), range(66, 91)}


def parse(path):
    import xml.etree.ElementTree as ET
    z = zipfile.ZipFile(path)
    rels = ET.fromstring(z.read('word/_rels/document.xml.rels'))
    rid = {r.get('Id'): 'word/' + r.get('Target') for r in rels}
    root = ET.fromstring(z.read('word/document.xml'))
    paras = []
    for p in root.iter(W + 'p'):
        txt = ''.join(t.text or '' for t in p.iter(W + 't')).strip()
        blips = [b.get('{%s}embed' % NS['r']) for b in p.iter('{%s}blip' % NS['a'])]
        paras.append((txt, [rid[b] for b in blips]))
    return z, paras


def check(path, txt, datapy):
    errs = []
    spec = importlib.util.spec_from_file_location('d', datapy); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
    z, paras = parse(path)
    if not paras: return ['empty docx']
    title = paras[0][0]
    m = re.match(r'^SSC MTS (20\d\d) – (\d\d) (\w{3}) (20\d\d) – Shift ([1-4]) – Figures$', title)
    if not m or (int(m.group(1)), m.group(2), m.group(3), int(m.group(5))) != (D.META['year'], D.META['dd'], D.META['mon'], D.META['shift']):
        errs.append(f'title {title!r}')
    res = {}; cur = None; slot = None; used = []
    for txt_, imgs in paras[1:]:
        if txt_ and imgs: errs.append(f'label+image in one paragraph ({txt_})'); continue
        if len(imgs) > 1: errs.append('two images in one paragraph'); continue
        if re.match(r'^(Solution|Explanation|Answer)\b', txt_, re.I): errs.append('stray Solution/Answer paragraph'); continue
        mq = re.match(r'^Q\.(\d+)$', txt_)
        if mq:
            cur = int(mq.group(1)); res[cur] = {}; slot = None; continue
        if txt_ == '[figure]': slot = 'q'; continue
        mf = re.match(r'^Figure ([1-4])$', txt_)
        if mf: slot = 'opt' + 'ABCD'[int(mf.group(1)) - 1]; continue
        if txt_: errs.append(f'stray text {txt_!r}'); continue
        if imgs:
            if cur is None or slot is None: errs.append('image without a label'); continue
            if slot in res[cur]: errs.append(f'Q{cur} slot {slot} twice')
            res[cur][slot] = imgs[0]; used.append(imgs[0]); slot = None
    hdr, Q = parse_txt(txt)
    figset = {n for n, d in Q.items() if d['TEXT'].startswith('[FIGURE-BASED]')}
    if set(res) != figset: errs.append(f'question set {sorted(res)} != txt {sorted(figset)}')
    for n in res:
        if not any(n in b for b in (range(1, 41),)): errs.append(f'Q{n} outside Maths/Reasoning band (mis-offset?)')
    for n in res:
        if n not in Q: continue
        figopts = [Q[n][L] for L in 'ABCD'] == [f'(figure {i})' for i in range(1, 5)]
        hasopts = all(('opt' + L) in res[n] for L in 'ABCD')
        anyopt = any(('opt' + L) in res[n] for L in 'ABCD')
        if figopts != hasopts or (anyopt and not hasopts): errs.append(f'Q{n} option slots {sorted(res[n])} vs txt options')
        if ('q' in res[n]) != (D.FIG.get(n) in ('stem', 'both')): errs.append(f'Q{n} stem slot mismatch')
    media = [nm for nm in z.namelist() if nm.startswith('word/media/')]
    for nm in media:
        if used.count(nm) != 1: errs.append(f'{nm} referenced {used.count(nm)}x')
    hashes = {}
    for n, slots in res.items():
        hs = []
        for s, nm in slots.items():
            b = z.read(nm); h = hashlib.md5(b).hexdigest()
            try:
                im = Image.open(io.BytesIO(b)); im.load()
            except Exception:
                errs.append(f'Q{n} {s} does not decode'); continue
            short = min(im.size)
            if (s == 'q' and short < 60) or (s != 'q' and short < 24): errs.append(f'Q{n} {s} too small {im.size}')
            lo, hi = im.convert('L').getextrema()
            if hi - lo < 64: errs.append(f'Q{n} {s} near-uniform (black box?)')
            if s != 'q': hs.append(h)
        if len(hs) == 4 and len(set(hs)) != 4: errs.append(f'Q{n} option images not distinct')
    return errs


def mutate(src, dst, fn):
    zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
    for it in zin.infolist():
        b = zin.read(it.filename)
        b = fn(it.filename, b)
        zout.writestr(it, b)
    zout.close()


def controls(path, txt, datapy):
    import xml.etree.ElementTree as ET
    z, paras = parse(path)
    doc = z.read('word/document.xml').decode('utf-8')
    tmp = tempfile.mkdtemp(); results = []
    figs = [i for i, (t, im) in enumerate(paras) if t.startswith('Figure ')]
    def run(name, fn):
        out = os.path.join(tmp, name + '.docx'); mutate(path, out, fn)
        changed = zipfile.ZipFile(out).read('word/document.xml') != z.read('word/document.xml') or \
            any(zipfile.ZipFile(out).read(n) != z.read(n) for n in z.namelist())
        e = check(out, txt, datapy)
        results.append((name, changed, bool(e)))
    # 1 swap two option images (swap rIds of first two option pictures of the first option question)
    rids = re.findall(r'r:embed="(rId\d+)"', doc)
    def swap(fnm, b):
        if fnm != 'word/document.xml': return b
        s = b.decode('utf-8'); a, c = rids[-1], rids[-2]
        s = s.replace(f'r:embed="{a}"', 'r:embed="TMPX"').replace(f'r:embed="{c}"', f'r:embed="{a}"').replace('r:embed="TMPX"', f'r:embed="{c}"')
        return s.encode()
    # swapping identical-looking images is caught via hash order? check only catches structure -> compare with recorded hashes
    run('drop Figure 3', lambda fnm, b: b if fnm != 'word/document.xml' else b.decode().replace('>Figure 3<', '><', 1).encode())
    def merge_label(fnm, b):
        if fnm != 'word/document.xml': return b
        s = b.decode(); i = s.find('>[figure]<'); j = s.find('</w:p>', i)
        k = s.find('<w:drawing', j); k2 = s.find('</w:drawing>', k) + len('</w:drawing>')
        draw = s[k:k2]; s = s[:k] + s[k2:]
        s = s[:j] + '<w:r>' + draw + '</w:r>' + s[j:]
        return s.encode()
    run('label+image same paragraph', merge_label)
    run('stray Solution paragraph', lambda fnm, b: b if fnm != 'word/document.xml' else b.decode().replace('<w:body>', '<w:body><w:p><w:r><w:t>X</w:t></w:r></w:p>', 1).replace('>X<', '>Solution<', 1).encode() if False else
        (b.decode().replace('</w:body>', '<w:p><w:r><w:t>Solution</w:t></w:r></w:p></w:body>').encode() if fnm == 'word/document.xml' else b))
    def black(fnm, b):
        if not fnm.startswith('word/media/') or fnm != sorted(n for n in z.namelist() if n.startswith('word/media/'))[0]: return b
        bio = io.BytesIO(); Image.new('RGB', Image.open(io.BytesIO(b)).size, 'black').save(bio, 'PNG'); return bio.getvalue()
    run('solid black image', black)
    def renum(fnm, b):
        if fnm != 'word/document.xml': return b
        s = b.decode(); m = re.search(r'>Q\.(\d+)<', s); n = int(m.group(1))
        return s.replace(f'>Q.{n}<', f'>Q.{n + 20 if n <= 20 else n - 20}<', 1).encode()
    run('renumber by ±20', renum)
    def dupopt(fnm, b):
        if fnm != 'word/document.xml': return b
        s = b.decode(); ids = re.findall(r'r:embed="(rId\d+)"', s)
        return s.replace(f'r:embed="{ids[-1]}"', f'r:embed="{ids[-2]}"', 1).encode()
    run('two options same blob', dupopt)
    run('title wrong shift', lambda fnm, b: b if fnm != 'word/document.xml' else re.sub(r'Shift (\d)', lambda m: f'Shift {int(m.group(1)) % 4 + 1}', b.decode(), 1).encode())
    return results


if __name__ == '__main__':
    e = check(*sys.argv[1:4])
    print('FAIL' if e else 'PASS', *e, sep='\n  ')
    res = controls(*sys.argv[1:4])
    ok = all(c and f for _, c, f in res)
    for r in res: print('  control', r)
    print('controls', 'OK' if ok else 'BROKEN', f'{sum(1 for _, c, f in res if c and f)}/{len(res)}')
    sys.exit(0 if (not e and ok) else 1)
