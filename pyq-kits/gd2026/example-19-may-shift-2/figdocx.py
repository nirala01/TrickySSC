from docx import Document
from docx.shared import Inches
import os
HERE=os.path.dirname(os.path.abspath(__file__))
P='ssc-gd-2026-19-may-shift-2'
d=Document()
d.add_paragraph('SSC GD Constable 2026 – 19 May 2026 – Shift 2 – Figures')
for q in [6,7,17,18,19,38]:
    d.add_paragraph(f'Q.{q}')
    d.add_paragraph('[figure]'); d.add_paragraph().add_run().add_picture(f'{HERE}/fig/Q{q}_stem.png',width=Inches(4.5))
    if q == 38: continue
    for i in range(1,5):
        d.add_paragraph(f'Figure {i}'); d.add_paragraph().add_run().add_picture(f'{HERE}/fig/Q{q}_opt{i}.png',width=Inches(1.3))
d.save(f'{HERE}/out/{P}-figures.docx'); print('ok')
