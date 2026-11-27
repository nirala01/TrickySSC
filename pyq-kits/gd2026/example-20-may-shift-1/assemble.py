import re, importlib, os
from base import *
SE={}; SH={}
for m in ['sol_en_1','sol_en_2','sol_en_3','sol_en_4']: SE.update(importlib.import_module(m).S)
for m in ['hi_sol_1','hi_sol_2','hi_sol_3','hi_sol_4']: SH.update(importlib.import_module(m).S)
assert sorted(SE)==list(range(1,81)) and sorted(SH)==list(range(1,81))
import add_en, add_hi
def enrich(S,A,hdr):
    for n,v in A.STEP.items(): S[n]=dict(S[n],raw=S[n]['raw'].rstrip('\n')+'\n'+v)
    for n,(b,f) in A.GK.items():
        raw=S[n]['raw']; assert ('## '+hdr) in raw, n
        raw=raw.replace('## '+hdr, b+'\n## '+hdr,1).rstrip('\n')+'\n'+f
        S[n]=dict(S[n],raw=raw)
enrich(SE,add_en,'Exam Facts'); enrich(SH,add_hi,'अतिरिक्त तथ्य')
os.makedirs('out',exist_ok=True)
qe=[];qh=[];se=[];sh=[]
for n in range(1,81):
    e=Q_EN[n]
    qe.append([n,SUBJECT_EN[n],CH[n],EXAM,YEAR,e['TEXT'],e['A'],e['B'],e['C'],e['D'],e['ANSWER']])
    if n in TRANSLATED:
        h=HI_SRC[n]; assert h['ANSWER']==e['ANSWER'],n
        qh.append([n,SUBJECT_HI[n],CH[n],EXAM,YEAR,h['TEXT'],*h['opts'],h['ANSWER']]); hopts=h['opts']; hans=h['ANSWER']
    else:
        h=Q_HI[n]
        qh.append([n,SUBJECT_HI[n],CH_HI[n],EXAM,YEAR,h['TEXT'],h['A'],h['B'],h['C'],h['D'],h['ANSWER']]); hopts=[h[L] for L in 'ABCD']; hans=h['ANSWER']
    eo=[e[L] for L in 'ABCD']
    se.append([n,to_html(SE[n]['raw'],e['ANSWER'],eo['ABCD'.index(e['ANSWER'])],'EN'),SE[n]['trick'],CON_EN[n]])
    con_h = CON_EN[n] if n in TRANSLATED else CON_HI[n]
    sh.append([n,to_html(SH[n]['raw'],hans,hopts['ABCD'.index(hans)],'HI'),SH[n]['trick'],con_h])
QH=['qNum','subject','chapterId','exam','year','text','option_A','option_B','option_C','option_D','correct']
SHD=['qNum','explanation','trick','concept']
write_csv(f'out/{PREFIX}-questions-EN.csv',QH,qe); write_csv(f'out/{PREFIX}-questions-HI.csv',QH,qh)
write_csv(f'out/{PREFIX}-solutions-EN.csv',SHD,se); write_csv(f'out/{PREFIX}-solutions-HI.csv',SHD,sh)
print('written')
