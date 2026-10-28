import {studyCurve} from './study-curves.mjs';
// Dynamic V7 study player; no scientific numbers are embedded here.

export function normalizeTimeline(data){

 const chapters=data.chapters??data.scenes;if(!Array.isArray(chapters)||!chapters.length)throw Error('Capítulos ausentes');

 const duration=Number(data.total_seconds??data.duration??chapters.at(-1).end);

 if(!Number.isFinite(duration)||duration<=0)throw Error('Duração inválida');

 const normalized=chapters.map((c,i)=>{const start=Number(c.start),end=Number(c.end??(start+Number(c.duration)));if(!Number.isFinite(start)||!Number.isFinite(end)||start<0||end<=start||end>duration+.01||(i&&start<Number(chapters[i-1].end??(Number(chapters[i-1].start)+Number(chapters[i-1].duration)))-.01))throw Error('Capítulo inválido: '+i);return {...c,start,end};});

 return {chapters:normalized,duration,fps:Number(data.fps)>0?Number(data.fps):null};

}

export const chapterIndex=(chapters,t)=>Math.max(0,chapters.findLastIndex(c=>t>=c.start));

export const mediaPath=(film,audio)=>`../render/filme${film}_1080p${audio==='pt-BR'?'_pt-BR':''}.mp4`;

const $=s=>document.querySelector(s),video=$('#filmVideo'),status=$('#status');

const SAFE_IDS=new Set('omega_I half meia_nat_residual S_boundary sqrt_e beta theta_M leak leak_resid tau_trans r_unit powers_ratio powers_chain breuer_gap zero_mode_weight J_cross J_inv J_id wigner KK R_rec plaq sch_Et sch_Er hel pol einstein flags id_true id_false theorems outside_trio n_formal um_sha16 proof_ladder_clean proof_ladder_total formal_count declaration_count flags_computed flags_literal ray_count z_disc p_disc z_delta threshold_sigma lnB_lcdm'.split(' '));

const NATURE_IDS=['z_disc','p_disc','threshold_sigma','z_delta','lnB_lcdm'];

const safeValue=h=>typeof h?.value==='number'&&Number.isFinite(h.value)?String(h.value):(h?.id==='um_sha16'&&/^[a-f0-9]{16,64}$/i.test(h.value)?h.value:'NOT_SEALED');

const safeStatute=h=>/PROVED/i.test(h?.statute??'')?'PROVED in kernel · sob hipóteses':/INPUT/.test(h?.statute??'')?'INPUT':/DER/.test(h?.statute??'')?'DERIVED':/AX/.test(h?.statute??'')?'POSTULATE':/REAL/.test(h?.statute??'')?'REAL':'OPEN';

const clock=t=>`${String(Math.floor(t/60)).padStart(2,'0')}:${String(Math.floor(t%60)).padStart(2,'0')}`;

const fetchJSON=async name=>{const r=await fetch(new URL('../data/'+name,import.meta.url));if(!r.ok)throw Error(name+' · HTTP '+r.status);return r.json();};

const text=v=>typeof v==='object'&&v!==null?(v['pt-BR']??v.en??JSON.stringify(v)):String(v??'');

let timelines,H,F,S,V,N=[],film=1,chapters=[],duration=0,fps=null,raf=0,generation=0,lastToken='',resume=null;

const originalCaptions=new WeakMap(),captionMeasure=document.createElement('canvas').getContext('2d');
// Explicit line breaks avoid native cue clipping after custom font sizing.
function wrapCaption(value,width){
 const lines=[];let line='';
 for(const character of value){
  if(character==='\n'){lines.push(line);line='';continue;}
  if(line&&captionMeasure.measureText(line+character).width>width){
   const space=line.lastIndexOf(' ');
   if(space>0){lines.push(line.slice(0,space));line=line.slice(space+1)+character;}
   else{lines.push(line);line=character;}
  }else line+=character;
 }
 if(line)lines.push(line);return lines.join('\n');
}
function captions(){
 const width=Math.max(100,video.getBoundingClientRect().width*.86);
 captionMeasure.font=`${Math.min(28,Math.max(10,innerWidth*.017))}px Outfit`;
 for(const t of video.textTracks){
  if(t.kind==='subtitles')for(const cue of t.cues??[]){
   if(!originalCaptions.has(cue))originalCaptions.set(cue,cue.text);
   cue.text=wrapCaption(originalCaptions.get(cue),width);
   cue.snapToLines=false;cue.line=cue.text.split('\n').length>3?32:48;
   cue.position=50;cue.size=92;cue.align='center';
  }
  t.mode=t.kind==='subtitles'&&t.language===$('#language').value?'showing':'disabled';
 }
}
const captionResize=new ResizeObserver(captions);captionResize.observe(video);
document.fonts.ready.then(captions);
document.addEventListener('fullscreenchange',captions);

function seek(t){if(!duration)return;const time=Math.max(0,Math.min(duration,t));try{video.currentTime=time;}catch{resume={time,playing:false};}update(time);}

function selectFilm(value,preserve=false){

 const previous={time:video.currentTime||0,playing:!video.paused};video.pause();cancelAnimationFrame(raf);film=value;generation++;lastToken='';

 ({chapters,duration,fps}=normalizeTimeline(timelines[film-1]));resume=preserve?previous:{time:0,playing:false};

 video.replaceChildren();video.src=mediaPath(film,$('#audio').value);video.poster=`../render/filme${film}_poster.jpg`;

 for(const [lang,label] of [['pt-BR','Português'],['en','English'],['fr','Français'],['zh-Hans','简体中文']]){const track=document.createElement('track');track.kind='subtitles';track.srclang=lang;track.label=label;track.src=`../subs/filme${film}/sync-${$('#audio').value}/${lang}.vtt`;track.default=lang===$('#language').value;track.onload=captions;video.append(track);}

 const track=document.createElement('track');track.kind='chapters';track.src=`../subs/filme${film}/chapters.vtt`;track.srclang='pt-BR';video.append(track);

 $('#seek').max=duration;$('#chapters').replaceChildren();

 chapters.forEach((c,i)=>{const b=document.createElement('button'),n=document.createElement('span');n.textContent=String(i+1).padStart(2,'0')+' · '+clock(c.start);b.append(n,document.createTextNode(text(c.title??c.name??c.key??`Capítulo ${i+1}`)));b.onclick=()=>seek(c.start);$('#chapters').append(b);});

 $('#download1080').href=mediaPath(film,$('#audio').value);$('#download720').href=`../render/filme${film}_720p${$('#audio').value==='pt-BR'?'_pt-BR':''}.mp4`;

 $('#back').disabled=$('#next').disabled=!fps;$('#back').title=$('#next').title=fps?'Passo de um quadro segundo o FPS do arquivo de dados':'FPS não informado nos dados';

 status.textContent='Carregando '+( $('#audio').value==='pt-BR'?'narração em português.':'English narration.');video.load();update(resume.time);

}

function chart(index,p){

 const selection=studyCurve(F,S,String(chapters[index]?.key??''),p);let {series,title,statute}=selection;p=selection.progress;
 series=series.filter(a=>Array.isArray(a)&&a.length>1&&a.every(Number.isFinite));

 const ctx=$('#chart').getContext('2d');ctx.clearRect(0,0,960,300);ctx.fillStyle='#09151e';ctx.fillRect(0,0,960,300);

 if(!series.length){ctx.fillStyle='#b6cbd2';ctx.font='22px Outfit';ctx.fillText('Examine os valores e as hipóteses deste capítulo abaixo.',50,150);$('#chart').setAttribute('aria-label','Este capítulo apresenta relações e valores; não há curva evolutiva.');$('#chartLabel').textContent='Relações e valores da fonte';$('#statute').textContent='A navegação muda o instante da apresentação; não acrescenta uma simulação física.';return;}

 let min=Infinity,max=-Infinity;for(const a of series)for(const v of a){min=Math.min(min,v);max=Math.max(max,v);}const range=Math.max(1e-12,max-min);

 ctx.strokeStyle='#263a45';ctx.lineWidth=1;for(let k=0;k<5;k++){ctx.beginPath();ctx.moveTo(50,25+k*55);ctx.lineTo(915,25+k*55);ctx.stroke();}

 series.forEach((a,j)=>{ctx.strokeStyle=['#72cbd9','#d8b878'][j%2];ctx.lineWidth=2.5;ctx.beginPath();a.forEach((v,i)=>{const x=50+i/(a.length-1)*865,y=245-(v-min)/range*215;i?ctx.lineTo(x,y):ctx.moveTo(x,y);});ctx.stroke();});

 ctx.strokeStyle='#ead4a0';ctx.beginPath();ctx.moveTo(50+p*865,20);ctx.lineTo(50+p*865,255);ctx.stroke();ctx.font='17px "JetBrains Mono"';ctx.fillStyle='#d8b878';const sample=series.map(a=>Number(a[Math.round(p*(a.length-1))]).toPrecision(5)).join(' · ');ctx.fillText(sample,50,281);

 const at=Math.round(p*(series[0].length-1)),coordinate=selection.domain?.[at];const domain=Number.isFinite(coordinate)?`${selection.axis} = ${coordinate.toPrecision(5)}`:`amostra ${at+1}/${series[0].length}`;$('#chart').setAttribute('aria-label',title+'; '+domain+'; valores: '+sample);$('#chartLabel').textContent=title+' · '+selection.labels.join(' / ')+' · '+domain;$('#statute').textContent=statute;

}

function update(forced){

 if(!chapters.length)return;const t=Math.max(0,Math.min(duration,typeof forced==='number'?forced:video.currentTime||0)),index=chapterIndex(chapters,t),c=chapters[index];

 $('#seek').value=t;$('#seek').setAttribute('aria-valuetext',clock(t)+' de '+clock(duration));$('#clock').textContent=clock(t)+' / '+clock(duration);

 [...$('#chapters').children].forEach((b,j)=>b.setAttribute('aria-current',String(j===index)));

 $('#chapterTag').textContent=`CAPÍTULO ${String(index+1).padStart(2,'0')} · ${t.toFixed(2)} s`;$('#chapterTitle').textContent=text(c.title??c.name??c.key);

 const live=(N[film-1]?.cues?.[$('#audio').value]??[]).filter(x=>t>=x.start&&t<x.end);const cues=(c.cues??[]).filter(x=>t>=Number(x.start??c.start)&&t<Number(x.end??c.end));$('#explanation').textContent=live.map(x=>x.translations?.[$('#language').value]??x.translations?.['pt-BR']??x.text??'').join(' ')||cues.map(x=>text(x['pt-BR']??x.text)).join(' ')||text(c.description??c.subtitle??'Examine os valores e as hipóteses da fonte no mesmo instante do filme.');

 if(lastToken!==film+':'+index){lastToken=film+':'+index;$('#metrics').replaceChildren();let items=c.metrics?.map(id=>V.get(id))??H.items.filter(h=>Number(h.scene)===Number(c.scene??index+1));

  if(c.key==='gravity')items=[...new Set([...items,...['sch_Er','hel','KK','plaq'].map(id=>V.get(id))])];items=items.filter(h=>h&&SAFE_IDS.has(h.id));

  const nature=index===chapters.length-1||items.some(h=>NATURE_IDS.includes(h.id));

  if(nature)items=[...new Set([...items,...NATURE_IDS.map(id=>V.get(id)).filter(Boolean)])];

  for(const h of items){const d=document.createElement('div');d.className='metric';for(const [tag,value]of[['small',h.label],['b',safeValue(h)],['small',safeStatute(h)]]){const e=document.createElement(tag);e.textContent=text(value);d.append(e);}$('#metrics').append(d);}

  if(nature){const d=document.createElement('div');d.className='metric nature-test';const z=V.get('z_disc'),p=V.get('p_disc'),threshold=V.get('threshold_sigma');d.textContent=z&&p&&threshold?`z_disc ${safeValue(z)} ${z.value<threshold.value?'<':'≥'} ${safeValue(threshold)} σ · p unilateral ${safeValue(p)}. ln B não é σ. NOT_FALSIFIED.`:'NOT_SEALED · Quadro estatístico incompleto.';$('#metrics').append(d);}



 }

 if($('#inspect').open)chart(index,Math.max(0,Math.min(1,(t-c.start)/(c.end-c.start))));

}

function tick(){update();if(!video.paused&&!video.ended)raf=requestAnimationFrame(tick);}

video.addEventListener('timeupdate',()=>update());video.addEventListener('seeked',()=>update());video.addEventListener('play',()=>{cancelAnimationFrame(raf);tick();});video.addEventListener('pause',()=>{cancelAnimationFrame(raf);update();});

video.addEventListener('loadedmetadata',()=>{video.playbackRate=Number($('#speed').value);captions();const state=resume;resume=null;if(state){seek(state.time);if(state.playing)video.play().catch(()=>{status.textContent='Use Reproduzir para continuar.';});}status.textContent='Pronto para assistir ou estudar.';if(Number.isFinite(video.duration)&&Math.abs(video.duration-duration)>.25)status.textContent='Atenção: duração da mídia difere da timeline; confira esta edição.';update();});

video.addEventListener('error',()=>{status.textContent='Arquivo de vídeo indisponível nesta edição. Os dados continuam consultáveis; nenhuma faixa alternativa foi selecionada.';});

$('#film').onchange=e=>selectFilm(Number(e.target.value));$('#audio').onchange=()=>selectFilm(film,true);$('#speed').onchange=e=>video.playbackRate=Number(e.target.value);$('#language').onchange=captions;$('#seek').oninput=e=>seek(Number(e.target.value));

$('#minus').onclick=()=>seek(video.currentTime-10);$('#plus').onclick=()=>seek(video.currentTime+10);$('#back').onclick=()=>{video.pause();if(fps)seek(video.currentTime-1/fps);};$('#next').onclick=()=>{video.pause();if(fps)seek(video.currentTime+1/fps);};$('#inspect').ontoggle=()=>update();

// Agent C contract: startReplay(container, options) -> {run,destroy,element}. Loaded only on a human click.

let replayController=null;$('#replayButton').onclick=async()=>{const button=$('#replayButton'),slot=$('#replaySlot');slot.hidden=false;button.setAttribute('aria-expanded','true');button.disabled=true;try{const mod=await import('./replay-panel.mjs');if(typeof mod.startReplay!=='function')throw Error('Contrato startReplay indisponível');replayController??=mod.startReplay(slot);button.hidden=true;await replayController.run();}catch(e){slot.textContent='Reprodução indisponível: '+e.message;button.disabled=false;button.hidden=false;}};

window.addEventListener('pagehide',()=>{cancelAnimationFrame(raf);captionResize.disconnect();replayController?.destroy?.();});

try{

 [timelines,H]=await Promise.all([Promise.all(['film1.json','film2.json'].map(fetchJSON)),fetchJSON('hud.json')]);

 if(!Array.isArray(H.items)||!H.seal_version||!H.seal_pin||!H.seal_timestamp)throw Error('HUD sem identificação completa do selo');V=new Map(H.items.map(h=>[h.id,h]));

 const version=String(H.seal_version).replace(/^v/,'');$('#pin').textContent=`rendered from um.py v${version} · pin ${H.seal_pin} · ${H.seal_timestamp}`;

 Promise.allSettled(['film1_narration_timeline.json','film2_narration_timeline.json'].map(fetchJSON)).then(r=>{N=r.map(x=>x.status==='fulfilled'?x.value:null);update();});selectFilm(1);Promise.allSettled(['frames.json','scene.json'].map(fetchJSON)).then(results=>{F=results[0].status==='fulfilled'?results[0].value:null;S=results[1].status==='fulfilled'?results[1].value:null;update();});

}catch(e){status.textContent='NOT_SEALED · '+e.message;for(const control of document.querySelectorAll('.toolbar select,.transport button,.transport input'))control.disabled=true;}

