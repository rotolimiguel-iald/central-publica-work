import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const source=fs.readFileSync(new URL('baseline/app/iald.js',import.meta.url),'utf8');
const durable=source.slice(source.indexOf('// Optional local module:'),source.indexOf('// Called only after a complete stream'));
const persistence=source.slice(source.indexOf('function persistirConversasBackground()'),source.indexOf('function desanexarRespostasBackground('));
const account='a'.repeat(64),id='a27ed052-2026-4221-9321-000000000001',observations=[];
function quotaStore(cap){const map=new Map();return {getItem:k=>map.get(k)??null,setItem(k,v){const next=new Map(map);next.set(k,v);const bytes=[...next].reduce((n,[a,b])=>n+2*(a.length+b.length),0);if(bytes>cap){const e=Error('synthetic quota exceeded');e.name='QuotaExceededError';throw e;}map.set(k,v);},bytes:()=>[...map].reduce((n,[a,b])=>n+2*(a.length+b.length),0)};}
for(const [kind,content] of [['image_1_2MB','data:image/png;base64,'+Buffer.alloc(1200000,7).toString('base64')],['document_1_4Mchars','PUBLIC_SYNTHETIC_DOCUMENT\n'+'x'.repeat(1400000)]]){
 const storage=quotaStore(5*1024*1024),requests=[];
 const c=vm.createContext({console,crypto:globalThis.crypto,TextEncoder,TextDecoder,Uint8Array,AbortController,setTimeout,clearTimeout,backgroundOwner:account,backgroundHistoryKey:a=>'iald_conversas_owner_v1:'+a,mediaAssertHistory:()=>{},localStorage:storage,S:{ativaId:'c1',conversas:[{id:'c1',mensagens:[{role:'user',content}]}]}});
 vm.runInContext(durable+'\n'+persistence+'\nglobalThis.make=createDurableChatJobs;',c);
 const jobs=c.make({storage,randomUUID:()=>id,request:async(path,options)=>{requests.push({path,method:options.method||'GET'});return new Response(JSON.stringify({account}));}});jobs.setOwner(account);
 vm.runInContext('persistirConversasBackground()',c);const historyBytes=storage.bytes();let error;
 try{await jobs.begin({iald_conv:'c1',stream:true,messages:[{role:'user',content}]});}catch(e){error=e;}
 assert(error?.message.includes('Sem espaço'));assert.equal(requests.filter(r=>r.method==='POST').length,0);
 observations.push({kind,quota_model:'Synthetic5MiB UTF16 WebStorage budget, not an iPhone measurement',history_bytes:historyBytes,payload_json_bytes:Buffer.byteLength(JSON.stringify({messages:[{role:'user',content}]})),failed_at:'begin.write before POST',error:error.message,http_posts:0});
}
const result={status:'REPRODUCED',observations,scope:'Actual baseline durable begin/write and history persistence in VM; synthetic storage quota only; no live browser/provider/runtime writes.'};
fs.writeFileSync(new URL('QUOTA_REPRODUCTION.json',import.meta.url),JSON.stringify(result,null,2));console.log(JSON.stringify(result));
