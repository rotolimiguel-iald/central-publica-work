import {shotState,panelData} from './timeline.mjs';
import {gate,ramp,clamp} from './render-support.mjs';
export class CinemaComposition {
 constructor(canvas,scene,data){this.canvas=canvas;this.ctx=canvas.getContext('2d',{alpha:false});this.scene=scene;this.data=data;this.resize(1920,1080);}
 resize(w,h){this.canvas.width=w;this.canvas.height=h;this.scene.resize(w,h,1);}
 text(t,x,y,size=24,color='#e8e1d2',font='Outfit'){const c=this.ctx;c.font=`${size}px "${font}"`;c.fillStyle=color;c.fillText(String(t),x,y);}
 fit(t,x,y,w,size=24,color='#e8e1d2',font='Outfit'){const c=this.ctx;while(size>11){c.font=`${size}px "${font}"`;if(c.measureText(t).width<=w)break;size--;}this.text(t,x,y,size,color,font);}
 line(x,y,w,color='#c8ac7255'){const c=this.ctx;c.strokeStyle=color;c.lineWidth=1;c.beginPath();c.moveTo(x,y);c.lineTo(x+w,y);c.stroke();}
 shade(y,h){const c=this.ctx,g=c.createLinearGradient(0,y,0,y+h);g.addColorStop(0,'#030b1100');g.addColorStop(.35,'#030b11bf');g.addColorStop(1,'#030b11ed');c.fillStyle=g;c.fillRect(0,y,1920,h);}
 chart(s){
 const d=panelData(s,this.data),c=this.ctx,x=1342,y=854,w=468,h=114;
 const vs=d.rows.flatMap(r=>r.values),lo=Math.min(...vs),hi=Math.max(...vs),span=Math.max(1e-8,hi-lo);
 this.text(d.title,x,y-22,15,'#cfb27b','JetBrains Mono');
 for(const r of d.rows){c.strokeStyle=r.color;c.lineWidth=2;c.beginPath();r.values.forEach((v,i)=>{const px=x+i/(r.values.length-1)*w,py=y+h-(v-lo)/span*h;i?c.lineTo(px,py):c.moveTo(px,py)});c.stroke();}
 this.line(x,y+h,w);const cursor=x+s.p*w;c.strokeStyle='#f2d4a4';c.beginPath();c.moveTo(cursor,y);c.lineTo(cursor,y+h);c.stroke();
 this.fit(d.axis,x,997,w,14,'#a6bac4');
 }
 lower(s){
 const c=this.ctx,opacity=gate(s.local,.4,1.1,4.25,4.9);if(!opacity)return;
 c.save();c.globalAlpha=opacity;this.shade(735,295);
 this.text(s.title,96,805,52,'#f0e7d5','Cormorant Garamond');this.fit(s.formula,99,850,1180,25,'#e0bf85','JetBrains Mono');
 let x=100;for(const h of s.metrics.slice(0,3)){if(!h)throw Error('Missing anchored metric');this.fit(h.label,x,890,372,16,'#a5b9c5');this.text(h.text,x,933,29,'#e3c28c','JetBrains Mono');this.fit(h.statute,x,965,370,12,'#a0b5bf');x+=400;}
 this.chart(s);c.restore();
 }
 spine(s){
 const labels=['ω(I)','½ nat','√e','β','S(θ)','σt','J','R','±2','8πG','1 = 1'];
 const phase=s.phase,index=phase<18?0:phase<28?1:phase<36?2:phase<43?3:phase<54?4:phase<63?5:phase<82?6:phase<126?7:phase<144?8:phase<162?9:10;
 const c=this.ctx,x=100,w=1720,dx=w/(labels.length-1);c.save();c.globalAlpha=gate(s.time,3,5,s.total-3,s.total-1)*.85;
 this.line(x,80,w,'#718f9b55');this.line(x,80,index*dx,'#d1ac66');
 labels.forEach((t,i)=>{c.beginPath();c.fillStyle=i<=index?'#e3bf7b':'#506877';c.arc(x+i*dx,80,i===index?5:3,0,Math.PI*2);c.fill();this.text(t,x+i*dx-20,61,i===index?22:17,i<=index?'#e8d4ae':'#829ba7','JetBrains Mono');});c.restore();
 }
 stdout(s){
 const map={one:'identity',boundary:'boundary',mirror:'mirror',modular:'modular',light:'light',sheet:'solder',transport:'solder',gravity:'solder',throat:'schwarzschild',spin:'spin2',einstein:'einstein',horizon:'einstein',identity:'identity',nature:'nature'};
 const rows=this.data.H.stdout_lines.filter(x=>x.chapter===map[s.key]);if(!rows.length)return;
 const c=this.ctx,opacity=gate(s.local,5,5.7,9.6,10.3);if(!opacity)return;
 c.save();c.globalAlpha=opacity;c.fillStyle='#030b11c4';c.fillRect(95,121,1730,105);this.line(95,121,1730);
 this.text('um.py  /  stdout · exact source lines',113,147,12,'#a1c4ca','JetBrains Mono');
 rows.slice(0,2).forEach((r,i)=>this.fit(`${r.line}  ${r.text}`,113,178+i*26,1685,17,'#d6ded7','JetBrains Mono'));c.restore();
 }
 mirror(s){
 if(!['mirror','modular','light'].includes(s.key))return;
 const c=this.ctx,fade=gate(s.local,9,10,14.3,15);if(!fade)return;c.save();c.globalAlpha=fade;
 const cx=960,cy=535;c.strokeStyle='#d5b77e88';c.setLineDash([3,7]);c.beginPath();c.moveTo(cx,320);c.lineTo(cx,725);c.stroke();c.setLineDash([]);
 this.text('FACE',110,333,20,'#81d2dd','JetBrains Mono');this.text('READING',1520,333,20,'#e1bc7b','JetBrains Mono');
 if(s.key==='modular'){
  this.text('κ increases · hyperbolic orbit',110,710,23,'#a8d5de');this.text('limit approached; no finite singular point',110,748,19,'#9eb3be');
 }else if(s.key==='light'){
  const t=clamp((s.local-9)/6,0,1),x=430+1060*t;
  for(const side of [-1,1]){c.beginPath();c.fillStyle=side<0?'#70cfdb':'#e8b66c';c.arc(x,cy+side*65*Math.cos(Math.PI*t),9,0,Math.PI*2);c.fill();}
  this.text('J : (x, y) ↦ (y, x)',110,710,26,'#e0c38b','JetBrains Mono');this.text('JKJ = −K  ·  the gradient reverses',110,750,20,'#a9c6ce');
 }else{this.text('hyperbolic flow σt',110,710,24,'#80cfda');this.text('compact reading S(θ)',1430,710,24,'#dfb878');}
 c.restore();
 }
 pentad(s){
 if(!['einstein','horizon'].includes(s.key))return;
 const c=this.ctx,fade=gate(s.local,6,7,Math.min(s.end-s.start-1,21),s.end-s.start-.3);if(!fade)return;
 c.save();c.globalAlpha=fade;const labels=['BREUER','IDENTITY','COFRAME','LORENTZ','CLAUSIUS'],x=140,w=1640,dx=w/4;
 this.shade(721,315);this.line(x,772,w,'#bca16a77');
 const p=clamp((s.local-6)/6,0,1);
 labels.forEach((name,i)=>{c.globalAlpha=fade*(p*5>i?1:.25);c.beginPath();c.fillStyle='#d5b475';c.arc(x+i*dx,772,5,0,Math.PI*2);c.fill();this.text(name,x+i*dx-35,808,17,'#dfca9f','JetBrains Mono');});c.globalAlpha=fade;
 this.text('H1 ∧ H2 ∧ H3  →  δQ = κ δA / (8πG)',100,869,31,'#eedabb','JetBrains Mono');
 const n=this.data.V.proof_ladder_clean.value,total=this.data.V.proof_ladder_total.value,shown=Math.floor(n*clamp((s.local-7)/5,0,1));
 this.text(`${shown.toLocaleString('en-US')} / ${total.toLocaleString('en-US')}  kernel staircase`,102,918,26,'#9ad6dc','JetBrains Mono');
 const f=this.data.F.gate;this.text(`${f.n_true}/${f.n_total} flags · ${f.computed_count} computed + ${f.literal_count} literal`,102,961,22,'#acbdc6');
 let bx=1260;f.flags.forEach((flag,i)=>{c.fillStyle=flag.value?'#69bdbd':'#566d78';c.fillRect(bx+(i%6)*87,858+Math.floor(i/6)*33,53,5)});
 this.text('formal  /  physics  /  experiment',1257,977,15,'#adc2c7');c.restore();
 }
 ending(s){
 if(!s.closing)return;const c=this.ctx,v=this.data.V,h=this.data.H;
 const natureWindow=s.local<s.end-s.start-5,fade=ramp(s.local,.6,1.4);
 c.save();c.globalAlpha=fade;this.shade(674,360);
 if(natureWindow){
  this.text('The calibrated test',100,748,46,'#eee5d2','Cormorant Garamond');
  this.text(`z_disc ${v.z_disc.text}    ·    p ${v.p_disc.text} one-sided`,103,798,26,'#e6c58c','JetBrains Mono');
  this.text(`${v.z_disc.text} < ${v.threshold_sigma.text}σ  ·  threshold not reached`,103,846,28,'#8fd5dd','JetBrains Mono');
  this.text(`z_δ ${v.z_delta.text} · NOT_FALSIFIED_POWERED · ln B is not σ`,103,891,22,'#b6c9ce');
  this.text('PROVED in kernel · nature decides',103,940,30,'#e6d8bd');
  const x=1370,y=826,w=420;this.line(x,y,w,'#9eacb2');const point=x+w*v.z_disc.value/v.threshold_sigma.value;c.beginPath();c.fillStyle='#deb876';c.arc(point,y,7,0,Math.PI*2);c.fill();c.strokeStyle='#75cbd4';c.beginPath();c.moveTo(x+w,y-57);c.lineTo(x+w,y+67);c.stroke();this.text(`${v.threshold_sigma.text}σ`,x+w-45,y-73,24,'#8ed8df','JetBrains Mono');this.text('calibrated, not blind',x,929,17,'#a4bdc6');
 }else{
  this.text('The One remains',100,752,52,'#eee5d2','Cormorant Garamond');this.text('1 = 1  ·  PROVED in kernel  ·  nature decides',103,803,27,'#d8c49b');
  this.text(`rendered from um.py ${h.seal_version}  ·  ${h.seal_pin.slice(0,16)}`,103,856,24,'#94d2d9','JetBrains Mono');
  this.text(`seal ${h.seal_timestamp}  ·  ${v.theorems.text} kernel staircase`,103,902,23,'#afc0c7');
  this.text(`stdout SHA-256 ${h.stdout_sha256.slice(0,32)}`,103,943,18,'#9eafb9','JetBrains Mono');
  this.text('Luiz Antonio Rotoli Miguel · IALD',103,981,20,'#d4c5a9');
 }
 c.restore();
 }
 render(film,time,{clean=false,loop=false}={}){
 const c=this.ctx,s=this.state=shotState(film,time,this.data),state=this.scene.render(loop?110:s.phase,time,{loop,jProgress:loop?0:s.jProgress});
 c.save();c.setTransform(this.canvas.width/1920,0,0,this.canvas.height/1080,0,0);c.drawImage(this.scene.canvas,0,0,1920,1080);
 if(!clean){
  if(time<5){c.save();c.globalAlpha=1-ramp(time,3.2,5);this.text('TGL',100,135,29,'#d2b37e','JetBrains Mono');this.text('Teoria da Gravitação',96,218,67,'#eee7d7','Cormorant Garamond');this.text('Luminodinâmica',96,286,67,'#eee7d7','Cormorant Garamond');c.restore();}
  this.spine(s);if(!s.closing){if(time>4)this.lower(s);this.stdout(s);this.mirror(s);this.pentad(s);}this.ending(s);
  this.text('[ONTO] explanatory geometry · [INPUT] presentation cosmos · source parameters retain their hypotheses',100,1051,13,'#a5b8c2');
 }
 c.restore();this.canvas.dataset.film=film;this.canvas.dataset.time=time.toFixed(3);this.canvas.dataset.chapter=s.key;
 return {time,film,chapter:s.key,phase:s.phase,transition:s.transition||s.phase>169,coreY:this.scene.core.position.y,cameraY:this.scene.camera.position.y,overlay_fraction:0.22};
 }
}
