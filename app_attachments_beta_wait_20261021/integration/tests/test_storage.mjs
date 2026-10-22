import fs from 'node:fs';import vm from 'node:vm';import assert from 'node:assert/strict';
const root=new URL('.',import.meta.url);
function fakeIndexedDB(){const databases=new Map(),fault={abortNextWrite:false};let completions=0;
 return {fault,get completions(){return completions;},open(name){const request={};queueMicrotask(()=>{let data=databases.get(name),fresh=!data;if(!data){data=new Map();databases.set(name,data);}const db={close(){},createObjectStore(){return {};},transaction(_store,mode){let ended=false;const pending=structuredClone(data);const tx={abort(){if(!ended){ended=true;queueMicrotask(()=>tx.onabort?.());}},objectStore(){const operation=(action)=>{const r={};queueMicrotask(()=>{if(ended)return;r.result=action();r.onsuccess?.();queueMicrotask(()=>{if(ended)return;if(mode==='readwrite'&&fault.abortNextWrite){fault.abortNextWrite=false;ended=true;tx.onabort?.();return;}ended=true;if(mode==='readwrite'){data.clear();for(const [k,v]of pending)data.set(k,v);}completions++;tx.oncomplete?.();});});return r;};return {put:(v,k)=>operation(()=>{pending.set(k,structuredClone(v));return k;}),get:k=>operation(()=>structuredClone(pending.get(k))),delete:k=>operation(()=>{if(typeof k==='object'){for(const x of pending.keys())if(x>=k.lower&&x<=k.upper)pending.delete(x);return;}return pending.delete(k);}),getAllKeys:k=>operation(()=>[...pending.keys()].filter(x=>!k||(x>=k.lower&&x<=k.upper)))};}};return tx;}};request.result=db;if(fresh)request.onupgradeneeded?.();request.onsuccess?.();});return request;}};
}
let html=fs.readFileSync(new URL('test_storage_browser.html',root),'utf8');let js=html.slice(html.indexOf('<script type="module">')+22,html.lastIndexOf('</script>'));
js=js.replace("scope:'Real Chromium IndexedDB transactions with account-scoped test database in isolated profile; app durable and persistence functions extracted unchanged; stub HTTP, zero provider/network. Synthetic quota; not iOS/WebKit validation.'","scope:'Node VM with simulated transactional IndexedDB and synthetic WebStorage quota; actual staged app functions; stub HTTP, zero provider/network/runtime edits. Browser harness prepared but headless executables returned no test output; no Chromium/WebKit or iPhone validation claimed.'");
js=js.replace('on browser fetch API','on Node WHATWG Request API');
js=js.replace("'real IDB: corrupt record hash and missing ref refuse'","'simulated IDB corrupt record hash and missing ref refuse'");
js=js.replace("document.body.textContent=JSON.stringify(result);document.title=result.status;",'globalThis.testResult=result;globalThis.helper=createChatLocalStore();globalThis.helperFactory=createChatLocalStore;');
js=js.replace('const result={',`await test('12MP real JPEG exact history/body below quota with same request identity',async()=>{
 localStorage=quotaStore();const content=[{type:'image_url',image_url:{url:fixture12}},{type:'text',text:'PUBLIC_COLORS'}];S={ativaId:'c1',conversas:[{id:'c1',mensagens:[{role:'user',content}]}]};await persistirConversasBackground();const c=make(),r=await c.jobs.begin({iald_conv:'c1',stream:true,messages:[{role:'user',content}]});await drain(c.jobs,c.jobs.pending()[0]);equal(c.mode.sent.messages[0].content,content);equal(c.mode.sent.request_id,r.request_id);ok(localStorage.bytes()<5000);observations.push({kind:'real_jpeg12mp',webstorage_bytes:localStorage.bytes(),encoded_chars:fixture12.length,posts:c.calls.filter(x=>x.method==='POST').length});
});
const result={`);
const fixture12='data:image/jpeg;base64,'+fs.readFileSync(new URL('../../repair/synthetic_12mp.jpg',root)).toString('base64');
const indexedDB=fakeIndexedDB();const context=vm.createContext({IDBKeyRange:{bound:(lower,upper)=>({lower,upper})},fixture12,indexedDB,crypto:globalThis.crypto,TextEncoder,TextDecoder,Uint8Array,AbortController,setTimeout,clearTimeout,Response,Request,btoa,console});
await vm.runInContext('(async()=>{'+js+'})()',context);
let result=context.testResult;
// Commit must precede resolution, including abort AFTER request success.

indexedDB.fault.abortNextWrite=true;await assert.rejects(()=>context.helper.put('a'.repeat(64),'payload','ABORT_AFTER_REQUEST_SUCCESS'));
result.results.push({name:'transaction abort after request success refuses commit',status:'PASS'});
for(const event of ['onblocked','onerror']) {
 const unavailable={open(){const r={};queueMicrotask(()=>r[event]?.());return r;}};
 context.unavailable=unavailable;
 const blocked=vm.runInContext('helperFactory({indexedDB:unavailable})',context);
 await assert.rejects(()=>blocked.put('a'.repeat(64),'payload','raw'));
 result.results.push({name:'IDB open '+event+' refuses',status:'PASS'});
}
const one=await context.helper.put('a'.repeat(64),'payload','DELETE_ACCOUNT_ONLY');
const two=await context.helper.put('b'.repeat(64),'payload','KEEP_OTHER_ACCOUNT');
await context.helper.purge('a'.repeat(64));
await assert.rejects(()=>context.helper.get('a'.repeat(64),'payload',one));
assert.equal(await context.helper.get('b'.repeat(64),'payload',two),'KEEP_OTHER_ACCOUNT');
result.results.push({name:'account deletion purges only authenticated owner durable namespace',status:'PASS'});
result.tests=result.results.length;result.status=result.results.every(x=>x.status==='PASS')?'PASS':'FAIL';result.transaction_completions=indexedDB.completions;
fs.writeFileSync(new URL('FRONTEND_TESTS.json',root),JSON.stringify(result,null,2));console.log(JSON.stringify(result));
process.exitCode=result.status==='PASS'?0:1;
