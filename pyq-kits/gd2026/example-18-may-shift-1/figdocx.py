from docx import Document
from docx.shared import Inches
import os
HERE=os.path.dirname(os.path.abspath(__file__))
P='ssc-gd-2026-18-may-shift-1'
d=Document()
d.add_paragraph('SSC GD Constable 2026 – 18 May 2026 – Shift 1 – Figures')
for q in [6,7,17,18,19]:
    d.add_paragraph(f'Q.{q}')
    d.add_paragraph('[figure]'); d.add_paragraph().add_run().add_picture(f'{HERE}/fig/Q{q}_stem.png',width=Inches(4.5))
    for i in range(1,5):
        d.add_paragraph(f'Figure {i}'); d.add_paragraph().add_run().add_picture(f'{HERE}/fig/Q{q}_opt{i}.png',width=Inches(1.3))
d.save(f'{HERE}/out/{P}-figures.docx'); print('ok')
