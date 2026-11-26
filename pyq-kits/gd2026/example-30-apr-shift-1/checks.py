import csv, re, sys, os, zipfile, hashlib, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
PREFIX = 'ssc-gd-2026-30-apr-shift-1'
DEV = re.compile(r'[ऀ-ॿ]')
BS = chr(92)
SUBJ = {}
for n in range(1,21): SUBJ[n]='General Intelligence & Reasoning'
for n in range(21,41): SUBJ[n]='General Knowledge & General Awareness'
for n in range(41,61): SUBJ[n]='Elementary Mathematics'
for n in range(61,81): SUBJ[n]='English Language'
FIGQ = {11, 12}

def chapter_ids():
    ids=set()
    for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'PROMPT-5-chapter-tagging-addendum.md'),encoding='utf-8'):
        m=re.match(r'^([a-z]+\.[a-z0-9-]+) — ',line)
        if m: ids.add(m.group(1))
    return ids

def parse_txt(path):
    src=open(path,encoding='utf-8').read(); Q={}
    for m in re.finditer(r'^\[Q(\d+)\]\n(.*?)(?=^\[Q\d+\]|\Z)',src,re.S|re.M):
        d={}
        for line in m.group(2).strip('\n').split('\n'):
            k,_,v=line.partition(': '); d[k]=v
        Q[int(m.group(1))]=d
    return src,Q

def b1(s): return re.findall(r'\s:', re.sub(r'\\\(.*?\\\)','KTX',s))

def check_txt(d, F):
    src,Q=parse_txt(f'{d}/{PREFIX}-questions-EN.txt'); hs,H=parse_txt(f'{d}/{PREFIX}-questions-HI-partD.txt')
    if sorted(Q)!=list(range(1,81)): F.append('EN txt block numbers')
    if sorted(H)!=list(range(61,81)): F.append('HI txt block numbers')
    for n,q in Q.items():
        for k in ['SUBJECT','CONCEPT','TEXT','A','B','C','D','ANSWER']:
            if not q.get(k,'').strip(): F.append(f'EN txt Q{n} missing {k}')
        if q.get('SUBJECT')!=SUBJ.get(n): F.append(f'EN txt Q{n} subject')
        if q.get('ANSWER') not in list('ABCD'): F.append(f'EN txt Q{n} answer')
        cells=[q.get('TEXT','')]+[q.get(L,'') for L in 'ABCD']
        for c in cells:
            if DEV.search(c): F.append(f'EN txt Q{n} Devanagari')
            if b1(c): F.append(f'EN txt Q{n} B1')
            if c.count(BS+'(')!=c.count(BS+')'): F.append(f'EN txt Q{n} katex balance')
            if '\t' in c or re.search(r'\\u[0-9a-fA-F]{4}',c): F.append(f'EN txt Q{n} escape')
            if re.search(r'(?<![\\A-Za-z])(frac|dfrac|sqrt)\{',c) or any(re.search(r'(?<![\\A-Za-z])times(?![A-Za-z])',sp) for sp in re.findall(r'\\\((.*?)\\\)',c)): F.append(f'EN txt Q{n} bare cmd')
            if re.search(r'<(?!/?u>)',c): F.append(f'EN txt Q{n} raw <')
        if len(set(cells[1:]))<4: F.append(f'EN txt Q{n} duplicate options')
        if q.get('TEXT','').count('||')>1 and not q['TEXT'].startswith('PASSAGE'): F.append(f'EN txt Q{n} multiple ||')
        if (n in FIGQ)!=q.get('TEXT','').startswith('[FIGURE-BASED]'): F.append(f'EN txt Q{n} figure flag')
        if n in FIGQ and [q[L] for L in 'ABCD']!=[f'(figure {i})' for i in range(1,5)]: F.append(f'EN txt Q{n} figure options')
        if re.search(r'contains? a[n]?\b[^|]*error',q.get('TEXT','')) and '<u>' in q['TEXT']: F.append(f'EN txt Q{n} u in error item')
    for n,q in H.items():
        if q.get('SUBJECT')!='Hindi Language': F.append(f'HI txt Q{n} subject')
        if q.get('ANSWER') not in list('ABCD'): F.append(f'HI txt Q{n} answer')
        if not DEV.search(q.get('TEXT','')): F.append(f'HI txt Q{n} no Devanagari')
        for c in [q.get('TEXT','')]+[q.get(L,'') for L in 'ABCD']:
            if re.search(r'([ािीुूेैोौंः])\1',c): F.append(f'HI txt Q{n} doubled matra')
            if b1(c): F.append(f'HI txt Q{n} B1')
            if not c.strip(): F.append(f'HI txt Q{n} blank')
    return Q,H

def read(d,k):
    p=f'{d}/{PREFIX}-{k}.csv'
    raw=open(p,'rb').read()
    if not raw.startswith(b'\xef\xbb\xbf'): raise AssertionError(f'{k} no BOM')
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))

def check_csv(d, F, Q, H):
    ids=chapter_ids()
    QH=['qNum','subject','chapterId','exam','year','text','option_A','option_B','option_C','option_D','correct']
    SHD=['qNum','explanation','trick','concept']
    R={}
    for k,hd in [('questions-EN',QH),('questions-HI',QH),('solutions-EN',SHD),('solutions-HI',SHD)]:
        rows=read(d,k); R[k]=rows
        if list(rows[0].keys())!=hd: F.append(f'{k} header')
        if [r['qNum'] for r in rows]!=[str(i) for i in range(1,81)]: F.append(f'{k} rows/qNum')
        for r in rows:
            for c,v in r.items():
                if c=='trick' and k.startswith('questions'): continue
                if not (v or '').strip(): F.append(f'{k} Q{r["qNum"]} empty {c}')
    qe={int(r['qNum']):r for r in R['questions-EN']}; qh={int(r['qNum']):r for r in R['questions-HI']}
    se={int(r['qNum']):r for r in R['solutions-EN']}; sh={int(r['qNum']):r for r in R['solutions-HI']}
    others=0
    for n in range(1,81):
        e,h=qe.get(n),qh.get(n)
        if not e or not h: continue
        if e['subject']!=SUBJ[n]: F.append(f'qEN Q{n} subject')
        if h['subject']!=(SUBJ[n] if n<61 else 'Hindi Language'): F.append(f'qHI Q{n} subject')
        for r,lab in [(e,'qEN'),(h,'qHI')]:
            if r['exam']!='ssc-gd' or r['year']!='2026': F.append(f'{lab} Q{n} exam/year')
            if r['chapterId'] not in ids: F.append(f'{lab} Q{n} bad chapterId {r["chapterId"]}')
            if r['chapterId'].endswith('.other'): others+=1
            for c in ['text','option_A','option_B','option_C','option_D']:
                if b1(r[c]): F.append(f'{lab} Q{n} B1 {c}')
        if n<61 and e['chapterId']!=h['chapterId']: F.append(f'Q{n} chapterId EN!=HI')
        if n<61 and not e['chapterId'].split('.')[0] in ('reason','ga','quant'): F.append(f'Q{n} chapter subject family')
        if n>60 and not e['chapterId'].startswith('eng.'): F.append(f'qEN Q{n} not eng.*')
        if n>60 and not h['chapterId'].startswith('hindi.'): F.append(f'qHI Q{n} not hindi.*')
        q=Q.get(n,{})
        if [e['text'],e['option_A'],e['option_B'],e['option_C'],e['option_D'],e['correct']]!=[q.get('TEXT'),q.get('A'),q.get('B'),q.get('C'),q.get('D'),q.get('ANSWER')]: F.append(f'qEN Q{n} != txt')
        if n<61:
            if h['correct']!=e['correct']: F.append(f'Q{n} HI key != EN key')
            if not DEV.search(h['text']): F.append(f'qHI Q{n} no Devanagari')
            if '||' in e['text'] and '||' not in h['text']: F.append(f'qHI Q{n} lost ||')
            for L in 'ABCD':
                de=sorted(re.findall(r'\d',e['option_'+L])); dh=sorted(re.findall(r'\d',h['option_'+L]))
                if de!=dh: F.append(f'qHI Q{n} digit set {L}')
                for M in 'ABCD':
                    if M!=L and h['option_'+L]==e['option_'+M] and e['option_'+M]!=e['option_'+L]: F.append(f'qHI Q{n} option {L} swapped')
            if (n in FIGQ) and [h['option_'+L] for L in 'ABCD']!=[f'(figure {i})' for i in range(1,5)]: F.append(f'qHI Q{n} figure labels')
        else:
            hq=H.get(n,{})
            if [h['text'],h['option_A'],h['option_B'],h['option_C'],h['option_D'],h['correct']]!=[hq.get('TEXT'),hq.get('A'),hq.get('B'),hq.get('C'),hq.get('D'),hq.get('ANSWER')]: F.append(f'qHI Q{n} != HI txt')
        for r,lab in [(e,'qEN')]:
            for c in r.values():
                if DEV.search(c): F.append(f'{lab} Q{n} Devanagari')
        # solutions
        for s,qq,lab,lang in [(se.get(n),e,'sEN','EN'),(sh.get(n),h,'sHI','HI')]:
            if not s: continue
            ex=s['explanation']
            m=re.search(r'<div class="sol-verdict"><span class="vmk">✓</span><span>(.*?)</span></div>$',ex)
            if not m: F.append(f'{lab} Q{n} verdict missing'); continue
            if f'({qq["correct"]})' not in m.group(1): F.append(f'{lab} Q{n} verdict letter')
            body=ex[:m.start()]
            steps=len(re.findall(r'class="sol-step"><strong>(Step|चरण) \d+:',body))
            bul=len(re.findall(r'class="sol-bullet"',body))
            if n<=20 or 41<=n<=60:
                if steps<4: F.append(f'{lab} Q{n} steps<4')
            if 21<=n<=40:
                hdr=('Exam Facts' if lang=='EN' else 'अतिरिक्त तथ्य')
                if hdr not in body: F.append(f'{lab} Q{n} facts block')
                else:
                    pre,post=body.split(f'<div class="sol-section">{hdr}</div>',1)
                    if pre.count('class="sol-bullet"')<5: F.append(f'{lab} Q{n} bullets<5')
                    if post.count('class="sol-bullet"')<2: F.append(f'{lab} Q{n} facts<2')
            if 41<=n<=60 and BS+'(' not in body: F.append(f'{lab} Q{n} no katex')
            if n<=60 and re.search(r'(?:[Oo]ption|विकल्प)\s*\(([A-D])\)',body): F.append(f'{lab} Q{n} hard-coded option letter')
            if n>60:
                lab2='Option' if lang=='EN' else 'विकल्प'
                pos=[body.find(f'{lab2} ({L})') for L in 'ABCD']
                if bul<6 or -1 in pos or pos!=sorted(pos): F.append(f'{lab} Q{n} option bullets')
            allc=ex+s['trick']
            if lang=='EN' and DEV.search(allc+s['concept']): F.append(f'{lab} Q{n} Devanagari')
            if lang=='HI' and not DEV.search(body): F.append(f'{lab} Q{n} no Devanagari')
            if allc.count(BS+'(')!=allc.count(BS+')'): F.append(f'{lab} Q{n} katex balance')
            if '\t' in allc or re.search(r'\\u[0-9a-fA-F]{4}',allc) or BS+BS in allc: F.append(f'{lab} Q{n} escape')
            if re.search(r'(?<![\\A-Za-z{])(frac|dfrac|tfrac|sqrt|text|operatorname)\{',allc): F.append(f'{lab} Q{n} bare brace cmd')
            for sp in re.findall(r'\\\((.*?)\\\)',allc):
                if re.search(r'(?<![\\A-Za-z{])(times|div|pi|theta|cdot|circ)(?![A-Za-z])',sp): F.append(f'{lab} Q{n} bare symbol cmd')
                if DEV.search(sp): F.append(f'{lab} Q{n} Devanagari in span')
                for c in re.findall(r'\\([A-Za-z]+)',sp):
                    if c not in {'dfrac','frac','sqrt','times','div','text','Rightarrow','approx','circ','le','ge','cdot','pi','theta','left','right'}: F.append(f'{lab} Q{n} unknown cmd {c}')
            if re.search(r'\bRs\.?\s*\d',allc) or re.search(r'\d\s*x\s*\d',allc): F.append(f'{lab} Q{n} plain-text math')
            if '&lt;u&gt;' in ex: F.append(f'{lab} Q{n} u tag in solution')
            if b1(re.sub(r'<[^>]+>',' ',ex)) or b1(s['trick']): F.append(f'{lab} Q{n} B1 in solution')
        if se.get(n) and sh.get(n):
            if n<61 and se[n]['explanation']==sh[n]['explanation']: F.append(f'sHI Q{n} copies EN')
            if n>60:
                hits=sum(1 for L in 'ABCD' if re.sub(r'</?u>','',h['option_'+L]) in sh[n]['explanation'])
                if hits<2: F.append(f'sHI Q{n} not about Hindi item')
                if se[n]['explanation']==sh[n]['explanation']: F.append(f'sHI Q{n} copies EN')
            if se[n]['concept']!=qe and (DEV.search(se[n]['concept']) or DEV.search(sh[n]['concept'])): F.append(f'Q{n} concept not English')
            if n<61 and se[n]['concept']!=sh[n]['concept']: F.append(f'Q{n} concept drift')
            if se[n]['concept']!=(Q.get(n,{}).get('CONCEPT')): F.append(f'sEN Q{n} concept != txt')
            if n>60 and sh[n]['concept']!=(H.get(n,{}).get('CONCEPT')): F.append(f'sHI Q{n} concept != HI txt')
    for lab,qq in [('qEN',qe),('qHI',qh)]:
        for n,r in qq.items():
            for L in 'ABCD':
                if re.match(r'\(figure \d\)',r['option_'+L]) and n not in FIGQ: F.append(f'{lab} Q{n} stray figure label')
    return others

def check_docx(d, F):
    z=zipfile.ZipFile(f'{d}/{PREFIX}-figures.docx'); xml=z.read('word/document.xml').decode()
    rels=z.read('word/_rels/document.xml.rels').decode()
    rid={m.group(1):m.group(2) for m in re.finditer(r'Id="(rId\d+)"[^>]*Target="([^"]+)"',rels)}
    paras=re.findall(r'<w:p[ >].*?</w:p>',xml,re.S)
    items=[]
    for p in paras:
        t=''.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>',p)); im=re.findall(r'r:embed="(rId\d+)"',p)
        if t and im: F.append('docx text+image in one paragraph')
        if len(im)>1: F.append('docx two images in one paragraph')
        items.append((t,im[0] if im else None))
    if not items or not re.match(r'^SSC GD Constable (20\d\d) – (\d\d) (\w{3}) \1 – Shift ([1-4]) – Figures$',items[0][0]) or items[0][0]!='SSC GD Constable 2026 – 30 Apr 2026 – Shift 1 – Figures': F.append('docx title')
    out={}; cur=None; slot=None; used=[]
    for t,im in items[1:]:
        if t:
            if re.fullmatch(r'Q\.\d+',t): cur=int(t[2:]); out[cur]={}; slot=None
            elif t=='[figure]': slot='q'
            elif re.fullmatch(r'Figure [1-4]',t): slot='opt'+'ABCD'[int(t[-1])-1]
            else: F.append(f'docx stray text {t!r}')
        elif im:
            if cur is None or slot is None or slot in out[cur]: F.append('docx unassigned image')
            else: out[cur][slot]=rid[im]; used.append(rid[im]); slot=None
    if set(out)!=FIGQ: F.append('docx question set')
    for q,v in out.items():
        if sorted(v)!=['optA','optB','optC','optD','q']: F.append(f'docx Q{q} slots {sorted(v)}')
        hs=[hashlib.md5(z.read('word/'+v[k])).hexdigest() for k in ['optA','optB','optC','optD'] if k in v]
        if len(set(hs))!=len(hs): F.append(f'docx Q{q} duplicate option images')
        figd=os.path.join(os.path.dirname(os.path.abspath(__file__)),'fig')
        for k,fn in [('q','stem'),('optA','opt1'),('optB','opt2'),('optC','opt3'),('optD','opt4')]:
            p=os.path.join(figd,f'Q{q}_{fn}.png')
            if k in v and os.path.exists(p) and hashlib.md5(z.read('word/'+v[k])).hexdigest()!=hashlib.md5(open(p,'rb').read()).hexdigest(): F.append(f'docx Q{q} {k} image is not the cut {fn}')
    media=[n for n in z.namelist() if n.startswith('word/media/')]
    if sorted('word/'+u for u in used)!=sorted(media) or len(set(used))!=len(used): F.append('docx media not referenced exactly once')
    from PIL import Image
    for m in media:
        im=Image.open(io.BytesIO(z.read(m)))
        if min(im.size)<60: F.append(f'docx small image {m}')

def run(d):
    F=[]
    try:
        Q,H=check_txt(d,F); others=check_csv(d,F,Q,H); check_docx(d,F)
    except Exception as ex:
        F.append(f'CRASH {type(ex).__name__}: {ex}'); others=None
    return F,others

if __name__=='__main__':
    d=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(os.path.abspath(__file__)),'out')
    F,others=run(d)
    print('FAILURES:',len(F)); [print(' -',f) for f in F[:60]]
    print('.other ids:',others)
