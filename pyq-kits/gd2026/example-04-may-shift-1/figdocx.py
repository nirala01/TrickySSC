from docx import Document
from docx.shared import Inches
P='ssc-gd-2026-04-may-shift-1'
d=Document()
d.add_paragraph('SSC GD Constable 2026 – 04 May 2026 – Shift 1 – Figures')
for q in [12,13]:
    d.add_paragraph(f'Q.{q}')
    d.add_paragraph('[figure]'); d.add_paragraph().add_run().add_picture(f'fig/Q{q}_stem.png',width=Inches(4.5))
    for i in range(1,5):
        d.add_paragraph(f'Figure {i}'); d.add_paragraph().add_run().add_picture(f'fig/Q{q}_opt{i}.png',width=Inches(1.3))
d.save(f'out/{P}-figures.docx'); print('ok')
