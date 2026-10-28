import {replayTrust} from './replay-trust.mjs';
import {verifyBytes,compareAnchors} from './replay-verify.mjs';
const labels={fractal_dephasing:'Defasagem',smatrix_closure:'Matriz S',solder_4d:'Solda 4D',local_breuer_gap:'Gap local de Breuer',minimal_solder:'Solda mínima',schwarzschild_step:'Schwarzschild estático',graviton_polarization:'Spin 2',the_TGL_identity_equation:'Identidade',light_is_J:'J',powers_ladder:'Powers'};
/** Mounts an inert button. run() is explicit; destroy() cancels worker/fetches.
 * options: manifestURL, expectedManifestSHA256, timeoutMs, onResult.
 * Hash override is for a separately trusted release/test manifest, never URL query input.
 */
export function startReplay(container,options={}) {
 if(!container?.append)throw new TypeError('container DOM required');
 const root=document.createElement('section'),button=document.createElement('button'),cancel=document.createElement('button'),status=document.createElement('p'),details=document.createElement('pre');
 root.className='replay-panel';button.type=cancel.type='button';button.textContent='Reproduzir no navegador';cancel.textContent='Cancelar';cancel.hidden=true;
 status.setAttribute('role','status');status.setAttribute('aria-live','polite');status.textContent='Python exato · carregamento somente ao clicar';
 details.style.cssText='white-space:pre-wrap;overflow-wrap:anywhere;max-height:24rem;overflow:auto;font-size:.8em';
 root.append(button,cancel,status,details);container.append(root);
 let worker,abort,timer,busy=false,destroyed=false,generation=0;
 const manifestURL=new URL(options.manifestURL||replayTrust.manifestURL,import.meta.url);
 const expected=options.expectedManifestSHA256||replayTrust.sha256;
 async function checked(url,pin,signal) {
  if(url.origin!==location.origin)throw Error('NOT_SEALED: recurso externo recusado');
  const r=await fetch(url,{cache:'no-store',signal});if(!r.ok)throw Error('NOT_SEALED: HTTP '+r.status);
  return verifyBytes(await r.arrayBuffer(),pin,url.pathname.split('/').pop());
 }
 function stop(){abort?.abort();worker?.terminate();worker=null;clearTimeout(timer);busy=false;button.disabled=false;cancel.hidden=true;}
 function failed(message,id){if(id!==generation||destroyed)return;status.textContent=message.startsWith('NOT_SEALED')?message:'NOT_SEALED: '+message;stop();}
 async function run(){
  if(busy||destroyed)return;busy=true;const id=++generation;abort=new AbortController();button.disabled=true;cancel.hidden=false;details.textContent='';status.textContent='Verificando integridade…';
  timer=setTimeout(()=>failed('NOT_SEALED: tempo excedido; cálculo não concluído',id),options.timeoutMs||180000);
  try {
   const decode=b=>new TextDecoder('utf-8',{fatal:true}).decode(b);
   const m=JSON.parse(decode(await checked(manifestURL,expected,abort.signal)));
   const entries=await Promise.all(Object.entries(m.assets).map(async ([key,a])=>[key,decode(await checked(new URL(a.url,manifestURL),a.sha256,abort.signal))]));
   if(id!==generation||destroyed)return;
   const a=Object.fromEntries(entries),anchors=JSON.parse(a['anchors.json']),hud=JSON.parse(a.hud);
   const workerURL=new URL('./replay-worker.js',import.meta.url);
   await checked(workerURL,m.worker_sha256,abort.signal);
   details.textContent=`um.py ${m.source.version} · SHA256 ${m.source.sha256}\nRecorte SHA256 ${m.assets['um_nucleo_filme.py'].sha256}\nEscalares SHA256 ${m.assets['um_scalar_excerpt.py'].sha256}\n${m.anchor_count} âncoras numéricas; ${m.hud_documentary_only.length} campos documentais fora do recálculo.\nMatemática do kernel sob hipóteses; este replay mede sombras numéricas.\n`;
   worker=new Worker(workerURL);worker.onerror=e=>failed('NOT_SEALED: '+e.message,id);
   worker.onmessage=({data})=>{
    if(id!==generation||destroyed)return;
    if(data.type==='progress')status.textContent=labels[data.stage]||'Carregando runtime local…';
    else if(data.type==='error')failed(data.message,id);
    else if(data.type==='result'){
     try{
      const result=compareAnchors(data.result.values,anchors,hud,m);
      result.timings_seconds=data.result.timings_seconds;result.numpy_version=data.result.numpy_version;
      status.textContent=`${result.status} · ${result.rows.filter(x=>x.ok).length}/${result.rows.length} comparações · Python exato`;
      details.textContent+=result.rows.map(x=>`${x.ok?'OK':'NOT_SEALED'} ${x.kind} ${x.key}: recalculado=${x.actual}; âncora=${x.expected}; resíduo=${x.residual}; tolerância=${x.atol}`).join('\n');
      stop();root.dispatchEvent(new CustomEvent('replay-result',{detail:result,bubbles:true}));options.onResult?.(result);
     }catch(e){failed(e.message,id);}
    }
   };
   worker.postMessage({manifest:m,baseURL:manifestURL.href,excerpt:a['um_nucleo_filme.py'],scalar:a['um_scalar_excerpt.py'],runner:a['replay_runner.py']});
  }catch(e){failed(e.message,id);}
 }
 button.addEventListener('click',run);cancel.addEventListener('click',()=>{generation++;stop();status.textContent='NOT_SEALED: execução cancelada, sem resultado';});
 return {run,destroy(){destroyed=true;generation++;stop();root.remove();},element:root};
}
