/* Classic worker for the pinned Pyodide 0.27.7. Loaded only on explicit click. */
let used=false;
self.onmessage=async ({data})=>{
 if(used)return;used=true;
 try {
  const {manifest,baseURL,excerpt,scalar,runner}=data;
  const base=new URL(baseURL),vendor=new URL(manifest.vendor_url,base);
  if(vendor.origin!==self.location.origin)throw Error('external runtime forbidden');
  const nativeFetch=self.fetch.bind(self),allowed=new Map(),verified=new Map();
  const hash=async b=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',b)),x=>x.toString(16).padStart(2,'0')).join('');
  for(const f of manifest.vendor.files) allowed.set(new URL(f.name,vendor).href,f);
  // Every runtime fetch is same-origin and hash verified; no CDN fallback.
  self.fetch=async (input,options)=>{
   const url=new URL(typeof input==='string'||input instanceof URL?input:input.url,vendor).href;
   const f=allowed.get(url);if(!f)throw Error('unlisted runtime request');
   if(verified.has(url))return new Response(verified.get(url).slice(0),{headers:{'Content-Type':f.name.endsWith('.wasm')?'application/wasm':'application/octet-stream'}});
   const response=await nativeFetch(url,{...options,cache:'no-store',credentials:'same-origin'});
   if(!response.ok)throw Error('runtime HTTP '+response.status);
   const bytes=await response.arrayBuffer();if(await hash(bytes)!==f.sha256)throw Error('runtime hash '+f.name);
   verified.set(url,bytes);return new Response(bytes.slice(0),{headers:{'Content-Type':f.name.endsWith('.wasm')?'application/wasm':'application/octet-stream'}});
  };
  for(const [name,text] of [['um_nucleo_filme.py',excerpt],['um_scalar_excerpt.py',scalar],['replay_runner.py',runner]])
   if(await hash(new TextEncoder().encode(text))!==manifest.assets[name].sha256)throw Error('excerpt hash '+name);
  // Preflight every required byte before Pyodide startup: WASM loader failures can otherwise hang.
  await Promise.all(manifest.vendor.files.map(async f=>{await (await self.fetch(new URL(f.name,vendor))).arrayBuffer();}));
  self.postMessage({type:'progress',stage:'Carregando Python e NumPy locais'});
  importScripts(new URL('pyodide.js',vendor).href);
  const py=await loadPyodide({indexURL:vendor.href,packageCacheDir:vendor.href});
  await py.loadPackage('numpy');
  py.globals.set('_film_excerpt',excerpt);py.globals.set('_film_scalar',scalar);
  py.globals.set('_film_progress',s=>self.postMessage({type:'progress',stage:String(s)}));
  py.runPython(runner);
  const result=JSON.parse(py.runPython('json.dumps(calculate(_film_excerpt, _film_scalar, _film_progress), allow_nan=False)'));
  self.postMessage({type:'result',result});
 }catch(e){self.postMessage({type:'error',message:'NOT_SEALED: '+String(e.message||e)});}
};
