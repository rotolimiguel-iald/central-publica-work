import {CinemaScene} from "./cinema-scene.mjs";
import {CinemaComposition} from "./cinema-composition.mjs";
import {loadProduction} from "./timeline.mjs";
const $=s=>document.querySelector(s),status=$("#status"),data=await loadProduction();
await Promise.all([document.fonts.load('68px "Cormorant Garamond"'),document.fonts.load('24px Outfit'),document.fonts.load('24px "JetBrains Mono"')]);
const stage=new CinemaScene($("#stage"),data.S),frame=document.createElement("canvas"),comp=new CinemaComposition(frame,stage,data),preview=$("#preview").getContext("2d");
let time=72,film=1;
$('#film').options[0].textContent='Filme 1 · '+data.T1.total_seconds+' segundos';$('#film').options[1].textContent='Filme 2 · '+data.T2.duration+' segundos';$('#timeline').max=data.T1.total_seconds;
function show(){frame.getContext("2d").getImageData(0,0,1,1);preview.drawImage(frame,0,0,1280,720);}
function draw(){const state=comp.render(film,time);show();return state;}
function lock(value){document.querySelectorAll("button,select,input").forEach(e=>e.disabled=value);}
async function post(url,body,type="application/json",headers={}){
 const payload=body instanceof Blob?body:JSON.stringify(body),attempts=url.includes('/video/chunk/')?4:1;
 for(let attempt=0;attempt<attempts;attempt++){
  try {const r=await fetch(url,{method:"POST",headers:{"Content-Type":type,...headers},body:payload});
   if(!r.ok)throw Error(await r.text());return await r.json();
  }catch(error){if(!(error instanceof TypeError)||attempt===attempts-1)throw error;
   status.textContent='Reconectando bloco local '+headers['X-TGL-Chunk'];await new Promise(resolve=>setTimeout(resolve,300*(attempt+1)));
  }
 }
}

$("#film").onchange=e=>{film=Number(e.target.value);$("#timeline").max=film===1?data.T1.total_seconds:data.T2.duration;time=Math.min(time,Number($("#timeline").max));$("#timeline").value=time;draw();};
$("#timeline").oninput=e=>{time=Number(e.target.value);draw();status.textContent="Filme "+film+" · "+time.toFixed(2)+" s";};
$("#snapshot").onclick=async()=>{
 lock(true);try{comp.resize(3840,2160);draw();await new Promise(requestAnimationFrame);draw();const coverage=stage.measureCoverage(),blob=await new Promise(r=>frame.toBlob(r,"image/png"));
 const result=await post("/cinema/export-frame",blob,"image/png",{"X-TGL-State":JSON.stringify({film,time,coverage,source:data.H.seal_version,source_sha256:data.H.seal_pin})});status.textContent=JSON.stringify(result,null,2);
 }catch(e){status.textContent=e.stack;}finally{comp.resize(1920,1080);draw();lock(false);}
};
$("#audit").onclick=async()=>{
 lock(true);try{const duration=film===1?data.T1.total_seconds:data.T2.duration,rows=[];comp.resize(1920,1080);
 for(let t=0;t<duration;t++){const state=comp.render(film,t),coverage=stage.measureCoverage();rows.push({...state,...coverage,transition:state.transition||coverage.transition});if(t%5===0){show();$("#progress").value=t/duration;status.textContent="Auditando "+t+" / "+duration+" s";await new Promise(requestAnimationFrame);}}
 const failures=rows.filter(r=>!r.transition&&r.width_fraction<.60);const report={kind:"coverage",film,status:failures.length?"FAIL":"PASS",rows,failures,method:"Opaque object mask at 480x270; no sky, glow, beams or ray shader in the mask. One sample per second."};
 await post("/api/cinema/diagnostics",report);status.textContent=JSON.stringify({kind:report.kind,film,status:report.status,samples:rows.length,minWidth:Math.min(...rows.filter(r=>!r.transition).map(r=>r.width_fraction)),failures},null,2);
 }catch(e){status.textContent=e.stack;}finally{draw();lock(false);}
};
$("#encode").onclick=async()=>{
 lock(true);status.dataset.encode="RUNNING";let encoder;
 try{
  const choice=$("#kind").value,loop=choice==="loop",kind=loop?"loop":choice==="preview"?"preview":"film"+film,duration=loop?16:choice==="preview"?8:(film===1?data.T1.total_seconds:data.T2.duration),start=choice==="preview"?(film===1?55:110):0;
  const width=loop?1920:3840,height=loop?1080:2160,fps=60,total=Math.round(duration*fps);comp.resize(width,height);
  for(const t of (film===1?data.T1.scenes:data.T2.chapters).map(c=>c.start+2)){comp.render(film,t,{clean:loop});frame.getContext("2d").getImageData(0,0,1,1);await new Promise(requestAnimationFrame);}
  const config={codec:"avc1.640034",width,height,framerate:fps,bitrate:loop?10000000:40000000,hardwareAcceleration:"no-preference",latencyMode:"quality",avc:{format:"annexb"}};
  if(!(await VideoEncoder.isConfigSupported(config)).supported)throw Error("H.264 encoder unavailable");
  const job=await post("/api/cinema/video/start",{kind,film,width,height,fps,duration:total/fps,total,startTime:start,version:"delivery_v7",source:data.H.seal_version,source_sha256:data.H.seal_pin,subtitleMode:"External selectable captions; no burned subtitles"});
  let chunks=[],encoded=0,seq=0,error=null;const started=performance.now(),samples=[];let sceneCpuTotal=0,overlayCpuTotal=0;
  encoder=new VideoEncoder({output(chunk){const bytes=new Uint8Array(chunk.byteLength);chunk.copyTo(bytes);chunks.push(bytes);encoded++;},error(e){error=e;}});encoder.configure(config);
  async function drain(){await encoder.flush();if(error)throw error;if(chunks.length){const blob=new Blob(chunks);chunks=[];await post("/api/cinema/video/chunk/"+job.id,blob,"application/octet-stream",{"X-TGL-Chunk":String(seq),"X-TGL-Frames":String(encoded)});seq++;}}
  for(let i=0;i<total;i++){
   const t=loop?i/(total-1)*24:start+i/fps,state=comp.render(film,t,{clean:loop,loop});
   sceneCpuTotal+=state.scene_cpu_submit_ms;overlayCpuTotal+=state.overlay_cpu_ms;const vf=new VideoFrame(frame,{timestamp:Math.round(i*1e6/fps),duration:Math.round(1e6/fps)});encoder.encode(vf,{keyFrame:i%120===0});vf.close();
   if(i%60===0){const coverage=stage.measureCoverage();samples.push({...state,...coverage,transition:state.transition||coverage.transition});}
   if(i%30===29||i===total-1){await drain();show();$("#progress").value=(i+1)/total;status.textContent=JSON.stringify({kind,frame:i+1,total,encoded,elapsed_s:(performance.now()-started)/1000});await new Promise(resolve=>{const channel=new MessageChannel();channel.port1.onmessage=()=>{channel.port1.close();channel.port2.close();resolve();};channel.port2.postMessage(null);});}
  }
  await drain();encoder.close();encoder=null;if(encoded!==total)throw Error("Missing frames");
  const result=await post("/api/cinema/video/finish/"+job.id,{encoded,elapsed_s:(performance.now()-started)/1000,samples,scene_cpu_submit_seconds:sceneCpuTotal/1000,overlay_cpu_seconds:overlayCpuTotal/1000,cost_scope:"Browser CPU submission wall-clock, not isolated GPU duration"});
  status.textContent=JSON.stringify({kind,status:"COMPLETE",id:result.id,file:result.file,frames:encoded,bytes:result.bytes});status.dataset.encode="COMPLETE";status.dataset.job=job.id;
 }catch(e){status.textContent=e.stack;status.dataset.encode="FAIL";encoder?.close();}finally{lock(false);}
};
comp.resize(1920,1080);draw();status.textContent="Pronto · cosmos, material físico e câmera contínua";status.dataset.ready="true";

const stillButton=document.createElement("button");stillButton.textContent="Preparar stills";document.querySelector("nav").append(stillButton);
stillButton.onclick=async()=>{lock(true);try{comp.resize(3840,2160);const shots=data.T1.scenes.map(ch=>({film:1,time:(ch.start+ch.end)/2,key:ch.key,clean:true}));shots.push(...[0,40,80,120,160,200,240,280,300,312,332,350,357].map(time=>({film:2,time,key:"review_"+time,clean:false})));
for(const shot of shots){comp.render(shot.film,shot.time,{clean:shot.clean});frame.getContext("2d").getImageData(0,0,1,1);await new Promise(requestAnimationFrame);comp.render(shot.film,shot.time,{clean:shot.clean});const blob=await new Promise(r=>frame.toBlob(r,"image/png"));await post("/cinema/export-frame",blob,"image/png",{"X-TGL-State":JSON.stringify({...shot,source:data.H.seal_version,source_sha256:data.H.seal_pin})});status.textContent="Still "+shot.key;}status.textContent="STILLS COMPLETE";
}catch(e){status.textContent=e.stack;}finally{comp.resize(1920,1080);draw();lock(false);}};

const pipeline=new URLSearchParams(location.search).get('pipeline');
async function runPipeline(){
 const ids=pipeline==='all'?[1,2]:[Number(pipeline)];
 await stillButton.onclick();if(status.textContent.includes('Error'))throw Error(status.textContent);
 for(const id of ids){film=id;$('#film').value=String(id);$('#kind').value='film';await $('#encode').onclick();if(status.dataset.encode!=='COMPLETE')throw Error(status.textContent);}
 if(pipeline==='all'){$('#kind').value='loop';film=1;await $('#encode').onclick();if(status.dataset.encode!=='COMPLETE')throw Error(status.textContent);}
 status.textContent='PIPELINE RENDER COMPLETE';status.dataset.pipeline='COMPLETE';
}
if(pipeline)runPipeline().catch(e=>{status.textContent=e.stack;status.dataset.pipeline='FAIL'});
