import fs from 'node:fs';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {studyCurve} from '../web/study-curves.mjs';
const root=new URL('../',import.meta.url),read=p=>JSON.parse(fs.readFileSync(new URL(p,root),'utf8')),F=read('data/frames.json'),S=read('data/scene.json');
let checks=0;const eq=(a,b)=>{assert.deepEqual(a,b);checks++};
const expected={mirror:[F.mirror.refl,F.mirror.trans],modular:[F.breuer.density],light:[F.light_J.Kx,F.light_J.JKJx],sheet:[S.optical.rows.map(r=>r.area)],transport:[F.solder.path.map(r=>r[0]),F.solder.path.map(r=>r[1])],throat:[F.schwarzschild.rays_Et,F.schwarzschild.rays_Er],spin:[F.spin2.h_plus,F.spin2.h_cross],identity:[F.identity.resid_true,F.identity.resid_false]};
const keys=[...new Set([1,2].flatMap(i=>{const d=read('data/film'+i+'.json');return(d.chapters??d.scenes).map(c=>c.key)}))];
for(const key of keys.filter(k=>k!=='gravity'))for(const p of [0,.5,1]){
 const got=studyCurve(F,S,key,p);eq(got.series,expected[key]??[]);eq(got.progress,p);
 for(const series of got.series){eq(series.every(Number.isFinite),true);if(got.domain)eq(series.length,got.domain.length)}
 if(key!=='modular')eq(got.series.includes(F.breuer.density),false);
}
const boundaries=[];
for(const [t,key,local] of [[120,'transport',0],[124,'transport',.5],[127.999,'transport',.999875],[128,'throat',0],[132,'throat',.5],[135.999,'throat',.999875],[136,'spin',0],[140,'spin',.5],[143.999,'spin',.999875],[144,'spin',1]]){
 const got=studyCurve(F,S,'gravity',(t-120)/24);eq(got.series,expected[key]);eq(Math.abs(got.progress-local)<1e-12,true);boundaries.push({time:t,key,progress:got.progress});
}
for(const key of [...keys,'unknown'])eq(studyCurve(null,null,key,.5).series,[]);
eq(studyCurve(F,S,'gravity',-1).series,expected.transport);eq(studyCurve(F,S,'gravity',2).series,expected.spin);
console.log(JSON.stringify({status:'PASS',checks,boundaries,scope:'Direct ESM execution with current real arrays; no browser/DOM/render'}));
