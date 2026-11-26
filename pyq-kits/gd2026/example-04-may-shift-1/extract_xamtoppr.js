const fs=require('fs'),path=require('path'),vm=require('vm');
const dir='repo', out={};
for(const f of fs.readdirSync(dir).filter(x=>x.endsWith('.html'))){
  const h=fs.readFileSync(path.join(dir,f),'utf8');
  const m=h.match(/(?:const|let|var)\s+Q_DATA_ALL\s*=\s*/); if(!m){out[f]={err:'no Q_DATA_ALL'};continue;}
  // find the object literal by bracket matching
  let i=m.index+m[0].length, d=0, s=i, inStr=null, esc=false;
  for(;i<h.length;i++){const c=h[i]; if(inStr){ if(esc)esc=false; else if(c==='\\')esc=true; else if(c===inStr)inStr=null; continue;} if(c==='"'||c==="'"||c==='`'){inStr=c;continue;} if(c==='{'||c==='[')d++; else if(c==='}'||c===']'){d--; if(d===0){i++;break;}}}
  const obj=vm.runInNewContext('('+h.slice(s,i)+')');
  out[f]=obj;
}
fs.writeFileSync('all.json',JSON.stringify(out));
for(const [f,o] of Object.entries(out)){ if(o.err){console.log(f,o.err);continue;} const k=Object.keys(o); console.log(f.replace(/SSC GD Constable 2026 Official Paper \(Held On |\)_Multilingual.html/g,''), k.map(x=>x+':'+(o[x]||[]).length).join(' ')); }
