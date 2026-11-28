import json, os
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__))
im=Image.open(f'{HERE}/raw/shot.png').convert('L')
assert im.size==(1010,390), im.size
POS={"Q18_stem":[8,8,395,90],"Q18_opt1":[440,8,127,111],"Q18_opt2":[585,8,127,111],"Q18_opt3":[730,8,127,111],"Q18_opt4":[875,8,126,111],"Q19_stem":[8,135,418,84],"Q19_opt1":[440,135,128,113],"Q19_opt2":[585,135,128,113],"Q19_opt3":[730,135,128,113],"Q19_opt4":[875,135,129,113],"Q20_stem":[8,262,399,77],"Q20_opt1":[440,262,128,113],"Q20_opt2":[585,262,128,113],"Q20_opt3":[730,262,128,113],"Q20_opt4":[875,262,128,113]}
os.makedirs(f'{HERE}/fig',exist_ok=True)
for k,(x,y,w,h) in POS.items():
    c=im.crop((x,y,x+w,y+h))
    c=c.point(lambda p:255 if p>200 else 0)   # line figures: threshold 200 removes the faint watermark
    c.save(f'{HERE}/fig/{k}.png')
print('cut',len(POS))
