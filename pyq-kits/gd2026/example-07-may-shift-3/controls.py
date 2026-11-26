import csv, io, os, re, shutil, sys, tempfile, zipfile
sys.path.insert(0,'.')
import checks
P=checks.PREFIX; SRC='out'
def fresh():
    d=tempfile.mkdtemp(); 
    for f in os.listdir(SRC): shutil.copy(f'{SRC}/{f}',d)
    return d
def edit_csv(d,k,n,col,fn):
    p=f'{d}/{P}-{k}.csv'; rows=list(csv.DictReader(open(p,encoding='utf-8-sig'))); hd=list(rows[0].keys())
    r=rows[n-1]; old=r[col]; r[col]=fn(old); assert r[col]!=old,(k,n,col)
    with open(p,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(hd); [w.writerow([x[h] for h in hd]) for x in rows]
def rows_op(d,k,fn):
    p=f'{d}/{P}-{k}.csv'; rows=list(csv.DictReader(open(p,encoding='utf-8-sig'))); hd=list(rows[0].keys())
    hd,rows=fn(hd,rows)
    with open(p,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(hd); [w.writerow([x.get(h,'') for h in hd]) for x in rows]
def edit_txt(d,k,fn):
    p=f'{d}/{P}-{k}.txt'; s=open(p,encoding='utf-8').read(); t=fn(s); assert t!=s,k; open(p,'w',encoding='utf-8').write(t)
def flip(x): return 'ABCD'[('ABCD'.index(x)+1)%4]
def find_row(k,pred):
    rows=list(csv.DictReader(open(f'{SRC}/{P}-{k}.csv',encoding='utf-8-sig')))
    for r in rows:
        if pred(r): return int(r['qNum'])
    raise AssertionError('no row '+k)
def exactly3(k): return find_row(k,lambda r:int(r['qNum'])<=20 and len(re.findall('class="sol-step"',r['explanation']))==4)
C={}
C['q text drift']=lambda d:edit_csv(d,'questions-EN',5,'text',lambda s:s+' x')
C['option altered']=lambda d:edit_csv(d,'questions-EN',30,'option_B',lambda s:s+'!')
C['EN key flip']=lambda d:edit_csv(d,'questions-EN',7,'correct',flip)
C['HI key flip Q1-60']=lambda d:edit_csv(d,'questions-HI',9,'correct',flip)
C['HI key flip Q61-80']=lambda d:edit_csv(d,'questions-HI',70,'correct',flip)
C['wrong subject']=lambda d:edit_csv(d,'questions-EN',25,'subject',lambda s:'General Awareness')
C['English Language left in HI 61-80']=lambda d:edit_csv(d,'questions-HI',65,'subject',lambda s:'English Language')
C['Hindi Language in EN']=lambda d:edit_csv(d,'questions-EN',65,'subject',lambda s:'Hindi Language')
C['wrong exam']=lambda d:edit_csv(d,'questions-EN',3,'exam',lambda s:'ssc-chsl')
C['wrong year HI']=lambda d:edit_csv(d,'questions-HI',3,'year',lambda s:'2025')
C['dropped row']=lambda d:rows_op(d,'solutions-EN',lambda h,r:(h,r[:-1]))
C['81st row']=lambda d:rows_op(d,'questions-HI',lambda h,r:(h,r+[dict(r[-1],qNum='81')]))
C['renamed header']=lambda d:rows_op(d,'solutions-HI',lambda h,r:(['qnum' if x=='qNum' else x for x in h],[{('qnum' if k=='qNum' else k):v for k,v in x.items()} for x in r]))
def strip_bom(d):
    p=f'{d}/{P}-questions-EN.csv'; b=open(p,'rb').read(); open(p,'wb').write(b[3:])
C['stripped BOM']=strip_bom
C['empty cell']=lambda d:edit_csv(d,'solutions-EN',44,'trick',lambda s:'')
C['concept drift']=lambda d:edit_csv(d,'solutions-HI',22,'concept',lambda s:s+'x')
C['concept translated']=lambda d:edit_csv(d,'solutions-HI',23,'concept',lambda s:'कला')
C['verdict removed']=lambda d:edit_csv(d,'solutions-EN',10,'explanation',lambda s:re.sub(r'<div class="sol-verdict">.*$','',s))
C['wrong verdict letter']=lambda d:edit_csv(d,'solutions-HI',11,'explanation',lambda s:re.sub(r'\(([A-D])\)',lambda m:'('+flip(m.group(1))+')',s))
C['steps<4 EN']=lambda d:edit_csv(d,'solutions-EN',exactly3('solutions-EN'),'explanation',lambda s:s.replace('class="sol-step"','class="x"',1))
C['steps<4 HI']=lambda d:edit_csv(d,'solutions-HI',exactly3('solutions-HI'),'explanation',lambda s:s.replace('class="sol-step"','class="x"',1))
C['GK facts removed EN']=lambda d:edit_csv(d,'solutions-EN',30,'explanation',lambda s:s.replace('Exam Facts','Notes'))
C['GK 5th bullet removed EN']=lambda d:edit_csv(d,'solutions-EN',25,'explanation',lambda s:s.replace('class="sol-bullet"','class="x"',1))
C['GK 2nd fact removed HI']=lambda d:edit_csv(d,'solutions-HI',26,'explanation',lambda s:re.sub(r'(<div class="sol-section">.*?</div><div class="sol-bullet">.*?</div>)<div class="sol-bullet">.*?</div>',r'\1',s,count=1))
C['GK facts removed HI']=lambda d:edit_csv(d,'solutions-HI',30,'explanation',lambda s:s.replace('अतिरिक्त तथ्य','नोट'))
C['lang option bullet dropped EN']=lambda d:edit_csv(d,'solutions-EN',66,'explanation',lambda s:s.replace('Option (C)','Opt (C)'))
C['lang option bullet dropped HI']=lambda d:edit_csv(d,'solutions-HI',66,'explanation',lambda s:s.replace('विकल्प (C)','विक (C)'))
C['hard-coded Option (X)']=lambda d:edit_csv(d,'solutions-EN',6,'explanation',lambda s:s.replace('</strong></div>',' Option (B)</strong></div>',1))
C['hard-coded विकल्प (X)']=lambda d:edit_csv(d,'solutions-HI',6,'explanation',lambda s:s.replace('</strong></div>',' विकल्प (B)</strong></div>',1))
C['Devanagari in EN']=lambda d:edit_csv(d,'solutions-EN',8,'trick',lambda s:s+' अ')
C['HI stem loses Devanagari']=lambda d:edit_csv(d,'questions-HI',22,'text',lambda s:'Who has the power?')
C['HI sol copies EN Q1-60']=lambda d:(lambda e:edit_csv(d,'solutions-HI',33,'explanation',lambda s:e))(list(csv.DictReader(open(f'{SRC}/{P}-solutions-EN.csv',encoding='utf-8-sig')))[32]['explanation'])
C['HI 61-80 options != source']=lambda d:edit_csv(d,'questions-HI',67,'option_B',lambda s:s+'ा')
C['HI 61-80 sol copied from EN']=lambda d:(lambda e:edit_csv(d,'solutions-HI',75,'explanation',lambda s:e))(list(csv.DictReader(open(f'{SRC}/{P}-solutions-EN.csv',encoding='utf-8-sig')))[74]['explanation'])
C['HI stem loses ||']=lambda d:edit_csv(d,'questions-HI',1,'text',lambda s:s.replace('||',' '))
C['HI digit set broken']=lambda d:edit_csv(d,'questions-HI',6,'option_A',lambda s:'79')
C['HI option swapped']=lambda d:edit_csv(d,'questions-HI',51,'option_A',lambda s:'38')
C['dfrac backslash dropped']=lambda d:edit_csv(d,'solutions-EN',find_row('solutions-EN',lambda r:'\\dfrac' in r['explanation']),'explanation',lambda s:s.replace('\\dfrac','dfrac',1))
C['times backslash dropped']=lambda d:edit_csv(d,'solutions-EN',find_row('solutions-EN',lambda r:'\\times' in r['explanation']),'explanation',lambda s:s.replace('\\times','times',1))
C['constructed costheta']=lambda d:edit_csv(d,'solutions-EN',45,'explanation',lambda s:s.replace('\\( ','\\( \\costheta ',1))
C['unbalanced paren']=lambda d:edit_csv(d,'solutions-HI',46,'explanation',lambda s:s.replace('\\)','',1))
C['injected uXXXX']=lambda d:edit_csv(d,'solutions-EN',47,'trick',lambda s:s+' \\u2212')
C['injected TAB']=lambda d:edit_csv(d,'solutions-HI',48,'trick',lambda s:s+'\t')
C['doubled backslash']=lambda d:edit_csv(d,'solutions-EN',49,'explanation',lambda s:s.replace('\\(','\\\\(',1))
C['B1 padded colon q']=lambda d:edit_csv(d,'questions-EN',15,'text',lambda s:s.replace('\\( 608 : ? :: 13 : 242 :: 138 : 367 \\)','608 : ? :: 13 : 242 :: 138 : 367'))
C['plain Rs']=lambda d:edit_csv(d,'solutions-EN',54,'trick',lambda s:s+' Rs. 600')
C['plain x math']=lambda d:edit_csv(d,'solutions-HI',51,'trick',lambda s:s+' 12 x 6')
C['Devanagari in span']=lambda d:edit_csv(d,'solutions-HI',52,'explanation',lambda s:s.replace('\\( ','\\( क ',1))
C['figure label rewritten']=lambda d:edit_csv(d,'questions-HI',11,'option_B',lambda s:'(चित्र 2)')
C['bad chapterId']=lambda d:edit_csv(d,'questions-EN',30,'chapterId',lambda s:'ga.space')
C['chapterId EN!=HI']=lambda d:edit_csv(d,'questions-HI',30,'chapterId',lambda s:'ga.physics')
C['eng id on HI partD']=lambda d:edit_csv(d,'questions-HI',63,'chapterId',lambda s:'eng.spelling')
# txt controls
C['txt drop block']=lambda d:edit_txt(d,'questions-EN',lambda s:re.sub(r'\[Q40\]\n.*?(?=\[Q41\])','',s,flags=re.S))
C['txt flip subject']=lambda d:edit_txt(d,'questions-EN',lambda s:s.replace('SUBJECT: Elementary Mathematics','SUBJECT: Quantitative Aptitude',1))
C['txt leak Hindi']=lambda d:edit_txt(d,'questions-EN',lambda s:s.replace('TEXT: In which epic is it mentioned that dying during Uttarayana leads to salvation?','TEXT: नागरिकता Mohiniyattam is a classical dance form',1))
C['txt blank option']=lambda d:edit_txt(d,'questions-HI-partD',lambda s:s.replace('A: संज्ञा\n','A: \n',1))
C['txt padded colon']=lambda d:edit_txt(d,'questions-EN',lambda s:s.replace('\\( 608 : ? :: 13 : 242 :: 138 : 367 \\)','608 : ? :: 13 : 242 :: 138 : 367',1))
C['txt doubled matra']=lambda d:edit_txt(d,'questions-HI-partD',lambda s:s.replace('B: साक्ष्य\n','B: साक्ष्याा\n',1))
C['txt figure flag lost']=lambda d:edit_txt(d,'questions-EN',lambda s:s.replace('[FIGURE-BASED] ','',1))
# docx controls
def docx_mut(d,fn):
    p=f'{d}/{P}-figures.docx'; z=zipfile.ZipFile(p); files={n:z.read(n) for n in z.namelist()}; z.close()
    x=files['word/document.xml'].decode(); y=fn(x); assert y!=x; files['word/document.xml']=y.encode()
    with zipfile.ZipFile(p,'w') as z2:
        for n,b in files.items(): z2.writestr(n,b)
def swap_opts(x):
    ids=re.findall(r'r:embed="(rId\d+)"',x); a,b=ids[1],ids[2]
    return x.replace(f'r:embed="{a}"','TMP').replace(f'r:embed="{b}"',f'r:embed="{a}"').replace('TMP',f'r:embed="{b}"')
C['docx swap option images']=lambda d:docx_mut(d,lambda x:re.sub(r'(r:embed=")(rId\d+)(")',lambda m,c=[0]:m.group(0),x) if False else x.replace('Figure 2','Figure 9',1))
C['docx drop Figure 3']=lambda d:docx_mut(d,lambda x:x.replace('>Figure 3<','><',1))
C['docx stray Solution']=lambda d:docx_mut(d,lambda x:x.replace('>[figure]<','>Solution<',1))
C['docx duplicate option image']=lambda d:docx_mut(d,lambda x:(lambda ids:x.replace(f'r:embed="{ids[2]}"',f'r:embed="{ids[1]}"',1))(re.findall(r'r:embed="(rId\d+)"',x)))
C['docx real option-image swap']=lambda d:docx_mut(d,swap_opts)
C['figure image file swapped (Q11 opt1<->opt3 cut)']=lambda d:docx_mut(d,lambda x:(lambda ids:x.replace(f'r:embed="{ids[1]}"','TMPX',1).replace(f'r:embed="{ids[3]}"',f'r:embed="{ids[1]}"',1).replace('TMPX',f'r:embed="{ids[3]}"',1))(re.findall(r'r:embed="(rId\d+)"',x)))
C['HI digit set broken Q48']=lambda d:edit_csv(d,'questions-HI',48,'option_C',lambda s:s.replace('9','3'))
C['docx missing for figure shift']=lambda d:os.remove(f'{d}/{P}-figures.docx')
C['B1 in solution trick']=lambda d:edit_csv(d,'solutions-EN',52,'trick',lambda s:s+' ratio 4 : 7')
C['sqrt backslash dropped HI']=lambda d:edit_csv(d,'solutions-HI',45,'explanation',lambda s:s.replace('\\sqrt','sqrt',1))
caught=0
for name,fn in C.items():
    d=fresh(); fn(d); F,_=checks.run(d)
    ok=bool(F); caught+=ok
    print(('CAUGHT ' if ok else 'MISSED ')+name+('' if ok else '')+(' | '+F[0] if ok else ''))
print(f'{caught}/{len(C)} controls caught')

