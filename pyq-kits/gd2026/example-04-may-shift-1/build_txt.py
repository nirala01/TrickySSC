import json,re,sys
sys.path.insert(0,'.')
from conv import clean
o=json.load(open('/home/claude/gd26/x/s0405_1.json'))
EN,HI=o['en'],o['hi']
PREFIX='ssc-gd-2026-04-may-shift-1'
SUBJ={0:'General Intelligence & Reasoning',1:'General Knowledge & General Awareness',2:'Elementary Mathematics',3:'English Language'}
FIG={12,13}
def K(x): return r'\( '+x+r' \)'
def T(*ls): return ' '.join(r'\text{%s}'%l if re.match(r'^[A-Z]',l) else l for l in ls)
# exact-string replacements applied to BOTH languages (stem body / options)
REP={
 1:[('RD : ? :: HM : KN :: XG : AT',K(r'\text{RD} : ? :: \text{HM} : \text{KN} :: \text{XG} : \text{AT}'))],
 14:[('TV120 : ? :: AC300 : CG240 :: PK125 : RO65',K(r'\text{TV120} : ? :: \text{AC300} : \text{CG240} :: \text{PK125} : \text{RO65}'))],
 15:[('UXY80 : UTQ120 :: TSK60 : ? :: LRP40 : LNH60',K(r'\text{UXY80} : \text{UTQ120} :: \text{TSK60} : ? :: \text{LRP40} : \text{LNH60}'))],
 17:[('527 : 2114 :: 408 : ? :: 965 : 3866',K('527 : 2114 :: 408 : ? :: 965 : 3866'))],
 18:[('398 : 120 :: 719 : ? :: 84 : -194',K('398 : 120 :: 719 : ? :: 84 : -194'))],
 43:[('(1/4)',K(r'\dfrac{1}{4}')),('(3/4)',K(r'\dfrac{3}{4}'))],
 44:[('(9.8 + 1.8)^{2} - 4 × 9.8 × 1.8',K(r'(9.8 + 1.8)^{2} - 4 \times 9.8 \times 1.8'))],
 46:[('4 : 5',K('4 : 5'))],
 48:[('9 : 4',K('9 : 4'))],
 53:[('2/3',K(r'\dfrac{2}{3}')),('1/4',K(r'\dfrac{1}{4}'))],
 57:[('5 : 3',K('5 : 3')),('3 : 2',K('3 : 2'))],
 58:[('(5/14)',K(r'\dfrac{5}{14}'))],
 72:[('was able to find a solution to the pressing','<u>was able to find a solution</u> to the pressing')],
 75:[('there was no one to blame but oneself','<u>there was no one to blame but oneself</u>')],
 78:[('(C) : (untamed)','(C): (untamed)')],
}
OPTREP={43:{'7/11':K(r'\dfrac{7}{11}'),'11/13':K(r'\dfrac{11}{13}'),'9/11':K(r'\dfrac{9}{11}'),'15/17':K(r'\dfrac{15}{17}')}}
def unk(t):
    t=re.sub(r'\\\(\s*(.*?)\s*\\\)',lambda m:m.group(1),t)
    t=re.sub(r'\^(\d)(?!\})',r'^{\1}',t).replace('\\times','×')
    return t
def stem(q,n,lang):
    t=unk(clean(q['text']))
    for a,b in REP.get(n,[]):
        if a in t: t=t.replace(a,b)
        elif lang=='EN' or n not in (72,75,78): raise SystemExit(f'Q{n} {lang}: anchor missing {a!r}')
    if '[BR]' in t and '||' not in t:
        t=t.replace('[BR]','||',1)
    if n in FIG: t='[FIGURE-BASED] '+t
    return t
def opts(q,n):
    if n in FIG: return [f'(figure {i})' for i in range(1,5)]
    return [OPTREP.get(n,{}).get(unk(clean(x)),unk(clean(x))) for x in q['opts']]
def passage(q,rng):
    return f"PASSAGE (Q{rng[0]}–Q{rng[1]}): "+clean(q['comp'])+' || '
def block(n,subj,concept,text,op,ans):
    return f"[Q{n}]\nSUBJECT: {subj}\nCONCEPT: {concept}\nTEXT: {text}\nA: {op[0]}\nB: {op[1]}\nC: {op[2]}\nD: {op[3]}\nANSWER: {ans}\n"
from concepts import CON_EN, CON_HI
def build_en():
    out=["# TRICKYSSC QUESTIONS\nEXAM: ssc-gd\nYEAR: 2026\nPAPER: SSC GD Constable 2026 May 04 Shift 1\nLANG: EN\n"]
    for i in range(80):
        q=EN[i]; n=i+1
        t=stem(q,n,'EN')
        if q['comp']: t=passage(q,(76,80))+t
        out.append(block(n,SUBJ[q['si']],CON_EN[n],t,opts(q,n),'ABCD'[q['cidx']]))
    return '\n'.join(out)
def build_hi_partd():
    out=["# TRICKYSSC QUESTIONS\nEXAM: ssc-gd\nYEAR: 2026\nPAPER: SSC GD Constable 2026 May 04 Shift 1\nLANG: HI\n"]
    for i in range(80,100):
        q=HI[i]; n=i-19
        t=clean(q['text'])
        if '[BR]' in t: t=t.replace('[BR]','||',1)
        if q['comp']: t=f"PASSAGE (Q75–Q79): "+clean(q['comp'])+' || '+t
        out.append(block(n,'Hindi Language',CON_HI[n],t,[clean(x) for x in q['opts']],'ABCD'[q['cidx']]))
    return '\n'.join(out)
def hi_q1_60():
    D={}
    for i in range(60):
        q=HI[i]; n=i+1
        t=stem(q,n,'HI')
        if not re.search('[\u0900-\u097F]',t): t='निम्नलिखित व्यंजक का मान ज्ञात कीजिए।||'+t
        D[n]=dict(TEXT=t,opts=opts(q,n),ANSWER='ABCD'[q['cidx']])
    return D
if __name__=='__main__':
    import os; os.makedirs('out',exist_ok=True)
    open(f'out/{PREFIX}-questions-EN.txt','w',encoding='utf-8').write(build_en())
    open(f'out/{PREFIX}-questions-HI-partD.txt','w',encoding='utf-8').write(build_hi_partd())
    json.dump(hi_q1_60(),open('hi_q1_60.json','w'),ensure_ascii=False,indent=0)
    print('ok')
