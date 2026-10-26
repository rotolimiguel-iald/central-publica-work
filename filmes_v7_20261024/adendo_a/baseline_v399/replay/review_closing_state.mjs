import fs from 'node:fs';import vm from 'node:vm';import assert from 'node:assert/strict';import crypto from 'node:crypto';import {performance} from 'node:perf_hooks';
const R='C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/video_um/delivery_v7',read=p=>fs.readFileSync(R+'/'+p,'utf8'),obj=p=>JSON.parse(read(p));
const helpers=read('cinema/render-support.mjs').split(/\r?\n/).slice(2,7).join('\n').replaceAll('export ','');
const scene=read('cinema/cinema-scene.mjs').match(/export function sceneState[\s\S]*?\n}/)[0].replace('export ','');
const strip=s=>s.replace(/^import .*?;\s*$/gm,'').replaceAll('export ','').replaceAll('import.meta.url',"'unused-no-fetch'");
const src=helpers+'\n'+scene+'\n'+strip(read('cinema/timeline.mjs'))+'\n'+strip(read('cinema/cinema-composition.mjs'))+'\n({sceneState,CinemaComposition})';
const api=vm.runInNewContext(src,{performance,Math,console});
const H=obj('data/hud.json'),data={H,F:obj('data/frames.json'),S:obj('data/scene.json'),T1:obj('data/film1.json'),T2:obj('data/film2.json'),V:Object.fromEntries(H.items.map(x=>[x.id,x]))};
const ctx={save(){},restore(){},setTransform(){},drawImage(){}},canvas={width:1920,height:1080,dataset:{},getContext(){return ctx}};
let state;
const stage={canvas:{},core:{position:{y:0}},camera:{position:{y:0}},resize(){},render(p,t,opts){state=api.sceneState(p,data.S,opts);return state}};
const comp=new api.CinemaComposition(canvas,stage,data);let checks=0;const rows=[];
for(const [film,total] of [[1,224],[2,360]]){
 let excluded=0,held=0;
 for(let t=0;t<total;t++){const shot=comp.render(film,t,{clean:true});const transition=shot.transition||state.collapse>0;assert.equal(transition,t<2||t>total-3);checks++;
 if(t<=total-3){assert.equal(state.collapse,0);checks++;if(state.ret>0){assert.equal(state.sheet,1);assert.equal(state.radius,6.4);checks+=2;held++;}}if(transition)excluded++;}
 for(const t of [total-3,total-3+.01,total]){comp.render(film,t,{clean:true});assert.equal(state.collapse>0,t>total-3);checks++;}
 rows.push({film,total,excluded_one_second_samples:excluded,return_samples_full_radius_and_opacity:held});
}
comp.render(1,15,{clean:true,loop:true});assert.equal(state.collapse,0);checks++;
assert(read('cinema/cinema-scene.mjs').includes('transition:this.state.collapse>0'));checks++;
console.log(JSON.stringify({status:'PASS',checks,films:rows,scope:'Actual composition/shotState/sceneState with no-op canvas/scene adapter; import.meta replaced only in unused loader. No WebGL/pixel test.',pins:Object.fromEntries(['cinema/cinema-scene.mjs','cinema/cinema-composition.mjs','make_v7.py'].map(p=>[p,crypto.createHash('sha256').update(fs.readFileSync(R+'/'+p)).digest('hex')]))}));