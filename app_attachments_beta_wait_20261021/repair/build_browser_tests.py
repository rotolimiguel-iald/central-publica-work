from pathlib import Path
import json
p=Path(r'C:/IALD/Central de Patentes/work/app_attachments_beta_wait_20261021/repair')
s=(p/'stage/app/iald.js').read_text(encoding='utf-8');durable=s[s.index('// Optional local module:'):s.index('// Called only after a complete stream')];persist=s[s.index('function persistirConversasBackground()'):s.index('function desanexarRespostasBackground(')]
tests=r'''
const results = [], observations = [];
const account='a'.repeat(64), second='b'.repeat(64);
let counter=0;
const nextId=()=> 'a27ed052-2026-4221-9321-'+String(++counter).padStart(12,'0');
const equal=(a,b)=>{if(JSON.stringify(a)!==JSON.stringify(b))throw Error('not equal');};
const ok=v=>{if(!v)throw Error('assertion failed');};
const rejects=async fn=>{let caught=false;try{await fn();}catch(_){caught=true;}ok(caught);};
const test=async(name,fn)=>{try{await fn();results.push({name,status:'PASS'});}catch(e){results.push({name,status:'FAIL',error:String(e.stack||e)});}};
function quotaStore(cap=5*1024*1024){const map=new Map();return {getItem:k=>map.get(k)??null,setItem(k,v){const next=new Map(map);next.set(k,v);const bytes=[...next].reduce((n,[a,b])=>n+2*(a.length+b.length),0);if(bytes>cap)throw Error('synthetic quota');map.set(k,v);},removeItem:k=>map.delete(k),bytes:()=>[...map].reduce((n,[a,b])=>n+2*(a.length+b.length),0),map};}
let localStorage=quotaStore(),backgroundOwner=account,backgroundEpoch=0,backgroundHistoryWrites=Promise.resolve(),S={conversas:[],ativaId:'c1'};
const chatLocalStore=createChatLocalStore();
const backgroundHistoryKey=a=>'iald_conversas_owner_v1:'+a;
const mediaAssertHistory=()=>{};
function make(store=chatLocalStore,mode={}){
 const calls=[];let id;
 const request=async(path,options={})=>{
  calls.push({path,method:options.method||'GET',body:options.body});
  if(path.endsWith('/session'))return new Response(JSON.stringify({account:mode.account||account}));
  if(options.method==='POST' && path==='/api/chat-jobs'){
    const raw=typeof options.body==='string'?options.body:new TextDecoder('utf-8',{fatal:true}).decode(options.body);
    const body=JSON.parse(raw);id=body.request_id;mode.sent=body;
    if(mode.uncertain)throw TypeError('simulated loss after POST');
    return new Response(JSON.stringify({id,status:'running',conversation_id:'c1'}));
  }
  if(path.endsWith('/ack'))return new Response('{}');
  const recovered=path.split('/').pop().split('?')[0];
  if(path.includes('?after='))return new Response(JSON.stringify({id:recovered,status:'completed',conversation_id:'c1',cursor:2,has_more:false,events:[{seq:1,data:JSON.stringify({choices:[{delta:{content:'PUBLIC_OK'}}]})},{seq:2,data:'[DONE]'}]}));
  return new Response(JSON.stringify({id:recovered,status:'completed',conversation_id:'c1'}));
 };
 const jobs=createDurableChatJobs({request,storage:localStorage,payloadStore:store,randomUUID:nextId});jobs.setOwner(account);
 return {jobs,calls,mode};
}
const drain=async(jobs,record)=>{const lines=[];for await(const l of jobs.stream(record))lines.push(l);return lines;};
await test('IDB full multiMB exact UTF8/hash, reopen and account isolation',async()=>{
 const raw=JSON.stringify({text:'🙂文'.repeat(500000)});const ref=await chatLocalStore.put(account,'payload',raw);
 equal(await createChatLocalStore().get(account,'payload',ref),raw);
 await rejects(()=>chatLocalStore.get(second,'payload',ref));
 await rejects(()=>chatLocalStore.get(account,'payload',{...ref,key:ref.key.slice(0,-1)+'x'}));
});
await test('real IDB: corrupt record hash and missing ref refuse',async()=>{
 const ref=await chatLocalStore.put(account,'payload','PUBLIC_CORRUPT');
 const db=await new Promise((resolve,reject)=>{const r=indexedDB.open('iald-chat-durable-json-v1',1);r.onsuccess=()=>resolve(r.result);r.onerror=reject;});
 await new Promise((resolve,reject)=>{const tx=db.transaction('json','readwrite');tx.objectStore('json').put({owner:account,kind:'payload',raw:'ALTERED',sha256:'0'.repeat(64),bytes:7},ref.key);tx.oncomplete=resolve;tx.onabort=reject;});db.close();
 await rejects(()=>chatLocalStore.get(account,'payload',ref));
 await rejects(()=>chatLocalStore.get(account,'payload',{v:1,owner:account,kind:'payload',key:account+':payload:'+'0'.repeat(64)}));
});
for(const [kind,content] of [['image_1_2MB','data:image/png;base64,'+btoa(String.fromCharCode(7).repeat(1200000))],['document_1_4Mchars','PUBLIC_SYNTHETIC_DOCUMENT\n'+'x'.repeat(1400000)]]){
 await test(kind+' history+outbox below synthetic quota, exact body restart and ack',async()=>{
  localStorage=quotaStore();S={ativaId:'c1',conversas:[{id:'c1',mensagens:[{role:'user',content}]}]};
  await persistirConversasBackground();const pointer=JSON.parse(localStorage.getItem(backgroundHistoryKey(account)));
  equal(JSON.parse(await chatLocalStore.get(account,'history',pointer.chat_local_history_v1)),{conversas:S.conversas,ativa:'c1'});
  let client=make();const record=await client.jobs.begin({iald_conv:'c1',stream:true,messages:[{role:'user',content}]});
  ok(!client.calls.some(c=>c.method==='POST'));
  const persisted=client.jobs.pending()[0];equal(persisted.payload,null);ok(persisted.payload_ref);
  client=make();const restored=client.jobs.pending()[0];await drain(client.jobs,restored);
  equal(client.mode.sent.messages[0].content,content);equal(client.mode.sent.request_id,record.request_id);
  let saved=false;await client.jobs.delivered(restored,async()=>{await persistirConversasBackground();saved=true;});ok(saved);
  equal(client.calls.filter(c=>c.path==='/api/chat-jobs'&&c.method==='POST').length,1);
  equal(client.calls.filter(c=>c.path.endsWith('/ack')).length,1);equal(client.jobs.pending(),[]);
  observations.push({kind,webstorage_bytes:localStorage.bytes(),content_chars:content.length,posts:1});
 });
}
await test('uncertain POST restart only GET even if payload storage is unavailable',async()=>{
 localStorage=quotaStore();let c=make(chatLocalStore,{uncertain:true});const r=await c.jobs.begin({iald_conv:'c1',messages:[{role:'user',content:'public'}]});
 await rejects(()=>drain(c.jobs,r));equal(c.calls.filter(x=>x.method==='POST').length,1);ok(c.jobs.pending()[0].attempted);
 c=make({get:async()=>{throw Error('unavailable');}});await drain(c.jobs,c.jobs.pending()[0]);equal(c.calls.filter(x=>x.method==='POST').length,0);
});
await test('payload transaction failure prevents outbox and POST',async()=>{
 localStorage=quotaStore();const c=make({put:async()=>{throw Error('commit abort');}});
 await rejects(()=>c.jobs.begin({iald_conv:'c1',messages:[]}));equal(c.jobs.pending(),[]);equal(c.calls.filter(x=>x.method==='POST').length,0);
});
await test('WebStorage metadata quota failure after payload commit prevents POST',async()=>{
 localStorage=quotaStore(5);const c=make();await rejects(()=>c.jobs.begin({iald_conv:'c1',messages:[]}));equal(c.calls.filter(x=>x.method==='POST').length,0);
});
await test('account switch while payload commit prevents intent/POST',async()=>{
 localStorage=quotaStore();let c;const store={put:async(...args)=>{const ref=await chatLocalStore.put(...args);c.jobs.setOwner(second);return ref;}};c=make(store);
 await rejects(()=>c.jobs.begin({iald_conv:'c1',messages:[]}));equal(c.calls.filter(x=>x.method==='POST').length,0);equal(c.jobs.pending(),[]);
});
await test('no acknowledgement after history save rejection',async()=>{
 localStorage=quotaStore();const c=make();const r=await c.jobs.begin({iald_conv:'c1',messages:[{role:'user',content:'ok'}]});await drain(c.jobs,r);
 await rejects(()=>c.jobs.delivered(r,async()=>{throw Error('history commit failed');}));equal(c.calls.filter(x=>x.path.endsWith('/ack')).length,0);ok(c.jobs.pending().length===1);
});
await test('legacy inline pending body retained and exact on POST',async()=>{
 localStorage=quotaStore();const c=make(null),r=await c.jobs.begin({iald_conv:'c1',messages:[{role:'user',content:'legacy🙂'}]});ok(c.jobs.pending()[0].payload);await drain(c.jobs,c.jobs.pending()[0]);equal(c.mode.sent.messages[0].content,'legacy🙂');
});
await test('serial history saves retain latest full snapshot',async()=>{
 localStorage=quotaStore();S={ativaId:'c1',conversas:[{id:'c1',text:'first'}]};const first=persistirConversasBackground();S.conversas[0].text='last🙂';const last=persistirConversasBackground();await Promise.all([first,last]);
 const ref=JSON.parse(localStorage.getItem(backgroundHistoryKey(account))).chat_local_history_v1;equal(JSON.parse(await chatLocalStore.get(account,'history',ref)).conversas[0].text,'last🙂');
});
await test('Uint8Array Request body preserves multiMB exact bytes on browser fetch API',async()=>{
 const raw=new TextEncoder().encode(JSON.stringify({text:'🙂Z'.repeat(500000)}));const req=new Request('https://example.invalid/local-only',{method:'POST',body:raw});const received=new Uint8Array(await req.arrayBuffer());equal(received.length,raw.length);ok(received.every((x,i)=>x===raw[i]));
});
await test('no IndexedDB fails closed without transient fallback',async()=>{const unavailable=createChatLocalStore({indexedDB:null});await rejects(()=>unavailable.put(account,'payload','raw'));});
const result={status:results.every(x=>x.status==='PASS')?'PASS':'FAIL',tests:results.length,results,observations,scope:'Real Chromium IndexedDB transactions with account-scoped test database in isolated profile; app durable and persistence functions extracted unchanged; stub HTTP, zero provider/network. Synthetic quota; not iOS/WebKit validation.'};
document.body.textContent=JSON.stringify(result);document.title=result.status;
'''
html='<!doctype html><meta charset="utf-8"><body>RUNNING</body><script type="module">\n'+durable+'\n'+persist+'\n'+tests+'\n</script>'
(p/'test_storage_browser.html').write_text(html,encoding='utf-8')
print('browser harness ready')
