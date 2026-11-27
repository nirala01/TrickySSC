const fs=require('fs'),vm=require('vm');
const f=process.argv[2], o=process.argv[3];
const h=fs.readFileSync(f,'utf8');
const m=h.match(/(?:const|let|var)\s+Q_DATA_ALL\s*=\s*/);
let i=m.index+m[0].length, d=0, s=i, inStr=null, esc=false;
for(;i<h.length;i++){const c=h[i]; if(inStr){ if(esc)esc=false; else if(c==='\\')esc=true; else if(c===inStr)inStr=null; continue;} if(c==='"'||c==="'"||c==='`'){inStr=c;continue;} if(c==='{'||c==='[')d++; else if(c==='}'||c===']'){d--; if(d===0){i++;break;}}}
const obj=vm.runInNewContext('('+h.slice(s,i)+')');
fs.writeFileSync(o,JSON.stringify(obj));
console.log(Object.keys(obj).map(k=>k+':'+obj[k].length).join(' '));
