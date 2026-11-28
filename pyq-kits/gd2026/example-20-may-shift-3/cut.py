import json, os
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__))
im=Image.open(f'{HERE}/raw/shot.png').convert('L')
assert im.size==(1180,625), im.size
POS={"Q6_stem":[8,4,366,83],"Q6_opt1":[610,4,128,114],"Q6_opt2":[755,4,128,114],"Q6_opt3":[900,4,129,114],"Q6_opt4":[1045,4,128,114],"Q7_stem":[8,122,587,147],"Q7_opt1":[610,122,128,114],"Q7_opt2":[755,122,128,114],"Q7_opt3":[900,122,129,114],"Q7_opt4":[1045,122,128,114],"Q17_stem":[8,273,364,78],"Q17_opt1":[610,273,128,112],"Q17_opt2":[755,273,128,112],"Q17_opt3":[900,273,128,112],"Q17_opt4":[1045,273,127,112],"Q18_stem":[8,389,344,76],"Q18_opt1":[610,389,127,111],"Q18_opt2":[755,389,127,111],"Q18_opt3":[900,389,127,111],"Q18_opt4":[1045,389,126,111],"Q19_stem":[8,504,346,75],"Q19_opt1":[610,504,128,114],"Q19_opt2":[755,504,128,114],"Q19_opt3":[900,504,128,114],"Q19_opt4":[1045,504,129,114]}
GREY={'Q7_opt1','Q7_opt2','Q7_opt3','Q7_opt4','Q18_stem','Q18_opt1','Q18_opt2','Q18_opt3','Q18_opt4'}
os.makedirs(f'{HERE}/fig',exist_ok=True)
for k,(x,y,w,h) in POS.items():
    c=im.crop((x,y,x+w,y+h))
    if k in GREY:      # small serif letters (Q7 options) and thin curved hooks (Q18): greyscale, watermark only removed
        c=c.point(lambda p:255 if p>215 else p)
    else:              # line figures, and the teal Q7 stem (becomes clean black): threshold 200 removes the faint watermark
        c=c.point(lambda p:255 if p>200 else 0)
    c.save(f'{HERE}/fig/{k}.png')
print('cut',len(POS))
