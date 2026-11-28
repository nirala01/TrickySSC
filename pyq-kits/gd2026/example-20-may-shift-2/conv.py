import json,re,html
def clean(s, keep_u=True):
    s=str(s or '')
    s=re.sub(r'\r','',s)
    s=re.sub(r'<img[^>]*>','',s)
    s=re.sub(r'<br\s*/?>\s*','[BR]',s,flags=re.I)
    s=re.sub(r'</p>\s*<p[^>]*>','[BR]',s,flags=re.I)
    s=re.sub(r'<sup>(.*?)</sup>',lambda m:'^{'+m.group(1)+'}',s)
    s=re.sub(r'<(strong|b|u)>(.*?)</\1>',lambda m:'<u>'+m.group(2)+'</u>' if keep_u else m.group(2),s,flags=re.S)
    s=re.sub(r'<(?!/?u>)[^>]+>','',s)
    s=html.unescape(s).replace('\xa0',' ')
    s=re.sub(r'[ \t]*\n[ \t]*',' ',s)
    s=re.sub(r'(\[BR\]\s*)+','[BR]',s)
    s=re.sub(r'^\s*(\[BR\])+|(\[BR\])+\s*$','',s)
    s=re.sub(r'\s+\[BR\]','[BR]',s); s=re.sub(r'\[BR\]\s+','[BR]',s)
    s=re.sub(r' {2,}',' ',s).strip()
    return s
