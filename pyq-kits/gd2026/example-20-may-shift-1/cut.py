import json, os
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__))
im=Image.open(f'{HERE}/raw/shot.png').convert('L')
assert im.size==(1170,610), im.size
POS={"Q6_stem":[8,8,418,99],"Q6_opt1":[440,8,127,112],"Q6_opt2":[585,8,128,113],"Q6_opt3":[730,8,129,112],"Q6_opt4":[875,8,127,112],"Q7_stem":[8,128,415,95],"Q7_opt1":[440,128,128,114],"Q7_opt2":[585,128,128,114],"Q7_opt3":[730,128,129,114],"Q7_opt4":[875,128,128,114],"Q17_stem":[8,248,364,85],"Q17_opt1":[440,248,127,112],"Q17_opt2":[585,248,127,112],"Q17_opt3":[730,248,127,112],"Q17_opt4":[875,248,126,112],"Q18_stem":[8,368,357,72],"Q18_opt1":[440,368,127,112],"Q18_opt2":[585,368,127,111],"Q18_opt3":[730,368,127,111],"Q18_opt4":[875,368,126,111],"Q19_stem":[8,488,368,79],"Q19_opt1":[440,488,126,112],"Q19_opt2":[585,488,126,112],"Q19_opt3":[730,488,126,112],"Q19_opt4":[875,488,83,79],"Q37_stem":[1030,8,125,236]}
os.makedirs(f'{HERE}/fig',exist_ok=True)
for k,(x,y,w,h) in POS.items():
    c=im.crop((x,y,x+w,y+h))
    if k=='Q37_stem': pass                      # the umpire photo is kept as cut
    elif k.startswith(('Q7_','Q17_')):         # tiny arrow heads / thin diagonals: greyscale, watermark only removed
        c=c.point(lambda p:255 if p>215 else p)
    else:                                       # line figures: threshold 200 removes the faint watermark
        c=c.point(lambda p:255 if p>200 else 0)
    # Q17: the one-flip-per-step figure sat in option slot 1 while the official key is option 4 -> the two option
    # images are swapped so that the key D is the correct figure (key letter not changed)
    k2={'Q17_opt1':'Q17_opt4','Q17_opt4':'Q17_opt1'}.get(k,k)
    c.save(f'{HERE}/fig/{k2}.png')
print('cut',len(POS))
