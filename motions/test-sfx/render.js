// usage: node render.js page.html outdir fps dur [t1,t2,...]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [page_,out,fps,dur,list]=process.argv.slice(2);fs.mkdirSync(out,{recursive:true});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+page_);await p.waitForFunction('window.READY===true');
const cv=await p.$('#c');
const times=list?list.split(',').map(Number):Array.from({length:Math.round(dur*fps)},(_,i)=>i/fps);
for(let i=0;i<times.length;i++){await p.evaluate(t=>draw(t),times[i]);
 await cv.screenshot({path:`${out}/f${String(i).padStart(4,'0')}.png`});}
console.log('frames',times.length,'errors',errs);await b.close()})();
