// V7 adapter. Geometry is [ONTO]; environment is [INPUT]. No external dependencies.
const sceneURL=new URL('../data/scene.json',import.meta.url);
const posterURL=new URL('../render/filme1_poster.jpg',import.meta.url);
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const finite=v=>typeof v==='number'&&Number.isFinite(v);
export const QUALITY_PRESETS=Object.freeze([0.5,0.75,1]);
export const BUDGET=Object.freeze({gpuMs:8,warmup:8,minSamples:30,window:120,maxPending:12,maxWidth:1280,maxHeight:720});
export function percentile95(values){if(!values.length)return null;const a=[...values].sort((x,y)=>x-y);return a[Math.ceil(a.length*.95)-1];}
export function budgetDecision(values){return values.length>=BUDGET.minSamples&&percentile95(values)>BUDGET.gpuMs;}
export function mount(canvas,options={}){
 if(!canvas||canvas.tagName!=='CANVAS')throw new TypeError('A canvas is required');
 let cinema=null,gl=null,ext=null,dead=false,raf=0,progress=0,pointer=[0,0],quality=.75,frames=0,waiting=0;
 let width=1,height=1;const begin=performance.now(),original=canvas.getAttribute('style'),abort=new AbortController();
 const pending=[],frameStats={gpuSamples:[],cpuSamples:[]};
 const stats={mode:'loading',reason:null,budget_ms:BUDGET.gpuMs,gpu_p95_ms:null,hardware:null,hardwareClass:'unverified',imageLoaded:false,frames:0};
 const push=(a,v)=>{a.push(v);if(a.length>BUDGET.window)a.shift();};
 function dispose(){if(gl)for(const q of pending)gl.deleteQuery(q.query);pending.length=0;if(cinema){try{cinema.destroy();}finally{cinema=null;}}}
 function fallback(reason){
  if(dead)return;cancelAnimationFrame(raf);stats.reason=reason;stats.mode='static';
  try{dispose();}catch(e){stats.disposalError=String(e.message);}
  canvas.width=canvas.width;canvas.style.backgroundImage=`url("${posterURL.href}")`;canvas.style.backgroundSize='cover';canvas.style.backgroundPosition='center';canvas.dataset.mode='static';
  const image=new Image();image.onload=()=>{if(!dead)stats.imageLoaded=true;};image.onerror=()=>{if(!dead){stats.imageLoaded=false;stats.imageError='Poster unavailable';}};image.src=posterURL.href;
 }
 function resize(w,h){
  if(dead)return api;const rect=canvas.getBoundingClientRect();w=w??rect.width??canvas.width;h=h??rect.height??canvas.height;
  if(!finite(w)||!finite(h)||w<=0||h<=0)throw new RangeError('Positive finite width and height required');
  const scale=Math.min(1,BUDGET.maxWidth/w,BUDGET.maxHeight/h);width=Math.max(1,Math.round(w*scale));height=Math.max(1,Math.round(h*scale));
  if(cinema)cinema.resize(width,height,quality);return api;
 }
 function render(){
  if(dead||!cinema||stats.mode!=='animated')return;
  try{
   if(gl.getParameter(ext.GPU_DISJOINT_EXT)){fallback('GPU timer disjoint');return;}
   for(let i=pending.length-1;i>=0;i--){const q=pending[i];if(gl.getQueryParameter(q.query,gl.QUERY_RESULT_AVAILABLE)){
    const ms=gl.getQueryParameter(q.query,gl.QUERY_RESULT)/1e6;gl.deleteQuery(q.query);pending.splice(i,1);
    if(q.frame>=BUDGET.warmup&&finite(ms)&&ms>=0)push(frameStats.gpuSamples,ms);
   }}
   stats.gpu_p95_ms=percentile95(frameStats.gpuSamples);
   if(budgetDecision(frameStats.gpuSamples)){fallback('GPU p95 exceeds 8 ms');return;}
   if(pending.length>=BUDGET.maxPending){if(++waiting>BUDGET.minSamples)fallback('GPU timer stalled');return;}
   waiting=0;const query=gl.createQuery();if(!query){fallback('GPU timer allocation failed');return;}
   const t=performance.now();gl.beginQuery(ext.TIME_ELAPSED_EXT,query);
   try{cinema.setPointer(...pointer);cinema.render(progress*180,(t-begin)/1000);}
   finally{gl.endQuery(ext.TIME_ELAPSED_EXT);pending.push({query,frame:frames});}
   push(frameStats.cpuSamples,performance.now()-t);stats.frames=++frames;canvas.dataset.mode='animated';
   if(frames>BUDGET.warmup+BUDGET.window&&!frameStats.gpuSamples.length)fallback('GPU timings unavailable');
  }catch(e){fallback('Renderer failure: '+e.message);}
 }
 function tick(){if(dead||stats.mode!=='animated')return;if(!document.hidden)render();if(stats.mode==='animated')raf=requestAnimationFrame(tick);}
 const lost=e=>{e.preventDefault();fallback('WebGL context lost');};canvas.addEventListener('webglcontextlost',lost);
 const observer=typeof ResizeObserver==='function'?new ResizeObserver(()=>{const r=canvas.getBoundingClientRect();if(r.width>0&&r.height>0)resize(r.width,r.height);}):null;observer?.observe(canvas);
 const api={
  get renderer(){return cinema?.renderer??null;},get scene(){return cinema?.scene??null;},get camera(){return cinema?.camera??null;},frameStats,
  render,resize,
  setProgress(v){if(!finite(v))throw new TypeError('Finite progress required');progress=clamp(v);return api;},
  setPointer(x,y){if(!finite(x)||!finite(y))throw new TypeError('Finite pointer required');pointer=[clamp(x,-1,1),clamp(y,-1,1)];return api;},
  setQuality(v){if(!QUALITY_PRESETS.includes(v))throw new RangeError('Quality presets: 0.5, 0.75, 1');quality=v;if(cinema)cinema.resize(width,height,quality);return api;},
  getDiagnostics(){return {...stats,progress,pointer:[...pointer],quality,width,height,dead,gpuSamples:[...frameStats.gpuSamples],cpuSamples:[...frameStats.cpuSamples],gpu_p95_ms:percentile95(frameStats.gpuSamples),budgetVerified:frameStats.gpuSamples.length>=BUDGET.minSamples&&percentile95(frameStats.gpuSamples)<=BUDGET.gpuMs,interpretation:'Measured renderer only; integrated GPU not inferred. Static fallback when GPU timing unavailable. Geometry [ONTO], environment [INPUT].'};},
  destroy(){if(dead)return;dead=true;abort.abort();cancelAnimationFrame(raf);observer?.disconnect();canvas.removeEventListener('webglcontextlost',lost);try{dispose();}finally{original===null?canvas.removeAttribute('style'):canvas.setAttribute('style',original);stats.mode='destroyed';canvas.dataset.mode='destroyed';}}
 };
 api.ready=(async()=>{try{
  if(options.reducedMotion??matchMedia('(prefers-reduced-motion: reduce)').matches){fallback('Reduced motion');return api;}
  const [{CinemaScene},response]=await Promise.all([import('../cinema/cinema-scene.mjs'),fetch(sceneURL,{signal:abort.signal})]);
  if(!response.ok)throw Error('Scene data HTTP '+response.status);const data=await response.json();if(dead)return api;
  cinema=new CinemaScene(canvas,data,{background:true});gl=cinema.renderer.getContext();ext=gl.getExtension('EXT_disjoint_timer_query_webgl2');
  const debug=gl.getExtension('WEBGL_debug_renderer_info');stats.hardware=gl.getParameter(debug?debug.UNMASKED_RENDERER_WEBGL:gl.RENDERER);
  if(!ext){fallback('GPU timing unavailable');return api;}
  stats.mode='animated';const rect=canvas.getBoundingClientRect();resize(rect.width||canvas.width,rect.height||canvas.height);
  if(options.autoRender!==false)raf=requestAnimationFrame(tick);
 }catch(e){if(!dead)fallback('Initialization: '+e.message);}return api;})();return api;
}
export const TGLBackground={mount};export default TGLBackground;
