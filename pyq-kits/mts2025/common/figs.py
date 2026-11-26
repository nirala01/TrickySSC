"""Make the figure PNGs for a paper into <paperdir>/fig/ and build <PREFIX>-figures.docx.
usage: python figs.py <paperdir>
data.FIGSRC per figure question:
  ('pie_pct', [(label, %)...], title)   our own clean pie, labels "S1 22%"
  ('pie_deg', [(label, deg)...], title) our own clean pie, labels "A 72°"
  ('bar', [(label, value)...], title)   our own clean bar graph, value on each bar
  ('pdf', stem_xref, [4 option xrefs] or None)  raster from <paperdir>/src.pdf (Testbook PDF), thresholded to pure
                                                black/white so the faint watermark digits vanish; native size, never upscaled
docx grammar (PROMPT-2): title "SSC MTS <year> – DD Mon YYYY – Shift n – Figures", then per question
"Q.N", "[figure]", picture, and for option figures "Figure 1".."Figure 4" each followed by its picture.
"""
import sys, os, io, importlib.util
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches

pdir = sys.argv[1]
spec = importlib.util.spec_from_file_location('data', os.path.join(pdir, 'data.py'))
D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
fdir = os.path.join(pdir, 'fig'); os.makedirs(fdir, exist_ok=True)
THRESH = getattr(D, 'THRESH', 185)


def pie(items, unit, fn):
    fig, ax = plt.subplots(figsize=(4.2, 4.2), dpi=110)
    vals = [v for _, v in items]
    labels = [f'{k}\n{v}{unit}' for k, v in items]
    ax.pie(vals, labels=None, startangle=90, counterclock=False,
           wedgeprops=dict(edgecolor='black', linewidth=1.2, facecolor='white'))
    import math
    tot = sum(vals); a = 90.0
    for (k, v), lab in zip(items, labels):
        mid = a - v / tot * 180.0; a -= v / tot * 360.0
        r = 0.62 if v / tot >= 0.08 else 1.2
        ax.text(r * math.cos(math.radians(mid)), r * math.sin(math.radians(mid)), lab, ha='center', va='center', fontsize=11)
    ax.set_aspect('equal'); ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.45, 1.45); ax.axis('off')
    fig.savefig(fn, bbox_inches='tight', pad_inches=0.08, facecolor='white'); plt.close(fig)


def bar(items, ylab, fn):
    fig, ax = plt.subplots(figsize=(max(4.2, 0.75 * len(items) + 1.5), 3.4), dpi=110)
    ks = [k for k, _ in items]; vs = [v for _, v in items]
    b = ax.bar(ks, vs, color='white', edgecolor='black', linewidth=1.2, width=0.5)
    for r, v in zip(b, vs):
        ax.text(r.get_x() + r.get_width() / 2, v, f'{v}', ha='center', va='bottom', fontsize=10)
    ax.set_ylabel(ylab, fontsize=10); ax.set_ylim(0, max(vs) * 1.18)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    fig.savefig(fn, bbox_inches='tight', pad_inches=0.08, facecolor='white'); plt.close(fig)


def raster(doc, xref, fn):
    info = doc.extract_image(xref)
    im = Image.open(io.BytesIO(info['image'])).convert('L')
    im = im.point(lambda p: 255 if p >= THRESH else 0).convert('1')
    im.save(fn)
    return im.size


def main():
    files = {}
    pdf = None
    for n in sorted(D.FIG):
        src = D.FIGSRC[n]; kind = src[0]
        stem = os.path.join(fdir, f'q{n:02d}_stem.png'); opts = []
        if kind == 'pie_pct': pie(src[1], '%', stem)
        elif kind == 'pie_deg': pie(src[1], '°', stem)
        elif kind == 'bar': bar(src[1], src[2], stem)
        elif kind == 'pdf':
            if pdf is None:
                import pymupdf
                pdf = pymupdf.open(os.path.join(pdir, 'src.pdf'))
            raster(pdf, src[1], stem)
            for i, x in enumerate(src[2] or []):
                fn = os.path.join(fdir, f'q{n:02d}_opt{i + 1}.png'); raster(pdf, x, fn); opts.append(fn)
        else:
            raise ValueError(kind)
        assert (D.FIG[n] == 'both') == bool(opts), f'Q{n} FIG kind vs option rasters'
        files[n] = (stem, opts)
    m = D.META
    docx = Document()
    docx.add_paragraph(f'SSC MTS {m["year"]} – {m["dd"]} {m["mon"]} {m["date"][-4:]} – Shift {m["shift"]} – Figures')
    for n, (stem, opts) in files.items():
        docx.add_paragraph(f'Q.{n}')
        docx.add_paragraph('[figure]')
        w = Image.open(stem).size[0]
        docx.add_paragraph().add_run().add_picture(stem, width=Inches(min(5.5, w / 110)))
        for i, fn in enumerate(opts):
            docx.add_paragraph(f'Figure {i + 1}')
            docx.add_paragraph().add_run().add_picture(fn, width=Inches(min(2.2, Image.open(fn).size[0] / 110)))
    out = os.path.join(pdir, 'out', f'{m["prefix"]}-figures.docx')
    docx.save(out); print('wrote', out, {n: (os.path.basename(s), len(o)) for n, (s, o) in files.items()})


main()
