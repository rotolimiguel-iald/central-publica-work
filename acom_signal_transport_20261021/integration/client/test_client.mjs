import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {webcrypto} from 'node:crypto';
import * as codec from './chat_wire_codec.mjs';

const root=new URL('./',import.meta.url);
const source=fs.readFileSync(new URL('iald.js',root),'utf8');
const durable=source.slice(source.indexOf('// Optional local module:'),source.indexOf('// Called only after a complete stream'));
const fetchSource=source.slice(source.indexOf('async function fetchIALD('),source.indexOf('// Embedded into iald.js by build_client.py'));
assert(durable.includes('function createDurableChatJobs')&&fetchSource.includes('return response;'));
const ACCOUNT='a'.repeat(64), ID='12345678-1234-4234-8234-123456789abc';
const cap={protocol:codec.PROTOCOL,codec:codec.CODEC,query:codec.QUERY,bases:false};
const job={id:ID,status:'running',conversation_id:'conversation1'};
const encode=x=>new TextEncoder().encode(JSON.stringify(x));
const reply=(x,status=200)=>new Response(JSON.stringify(x),{status,headers:{'Content-Type':'application/json'}});
const results=[];
async function test(name,fn){try{await fn();results.push({name,pass:true});}catch(e){results.push({name,pass:false,error:e.stack});}}

async function harness({transport=cap,unsupported=false,importFailure=false,onFetch}={}) {
  const calls=[],memory=new Map(),modules=new Map();let imports=0;
  const context=vm.createContext({console,TextEncoder,TextDecoder,Uint8Array,ArrayBuffer,DataView,
    Blob,Response,Request,URL,AbortController,setTimeout,clearTimeout,
    CompressionStream:unsupported?undefined:CompressionStream,DecompressionStream,
    crypto:webcrypto,atob,btoa,BASE:'https://stub.invalid',SUPERFICIE:'app',
    tokenApp:()=> 'synthetic-token',limparTokenApp:()=>{},avaliarPortao:()=>{},erroDoPortao:()=>{},
    fetch:async(url,options)=>{
      const path=url.replace('https://stub.invalid','');calls.push({path,options});
      if(path==='/api/chat-jobs/session')return reply({account:ACCOUNT,transport});
      return onFetch(path,options,calls);
    }});
  async function load(spec){
    assert(['./iald_transport.mjs','./chat_wire_codec.mjs'].includes(spec));
    if(modules.has(spec))return modules.get(spec);
    const mod=new vm.SourceTextModule(fs.readFileSync(new URL(spec,root),'utf8'),{context,identifier:spec});
    modules.set(spec,mod);await mod.link(load);return mod;
  }
  const mod=new vm.SourceTextModule(durable+'\n'+fetchSource+'\nexport {createDurableChatJobs,fetchIALD};',{
    context,identifier:'actual-staged-client-slices',importModuleDynamically:async spec=>{
      imports++;if(importFailure)throw Error('module unavailable');const loaded=await load(spec);await loaded.evaluate();return loaded;
    }});
  await mod.link(()=>{throw Error('unexpected import')});await mod.evaluate();
  const jobs=mod.namespace.createDurableChatJobs({request:mod.namespace.fetchIALD,
    storage:{getItem:k=>memory.get(k)??null,setItem:(k,v)=>memory.set(k,v),removeItem:k=>memory.delete(k)},
    randomUUID:()=>ID,sleep:async()=>{throw Error('unexpected wait')}});
  jobs.setOwner(ACCOUNT);
  return {jobs,calls,memory,imports:()=>imports};
}
const input={iald_conv:'conversation1',messages:[{role:'user',content:'Ação íntegra 🧪 e\u0301\r\n'.repeat(2500)}]};
async function drain(h,r){const values=[];for await(const v of h.jobs.stream(r))values.push(v);return values;}

await test('actual_client_authenticated_single_post_utf8_and_two_verified_pages',async()=>{
  let original;
  const h=await harness({onFetch:async(path,o)=>{
    if(path==='/api/chat-jobs'){
      assert.equal(o.method,'POST');assert.equal(o.headers.Authorization,'Bearer synthetic-token');
      assert.equal(o.credentials,'omit');assert.equal(o.headers['X-IALD-Context'],'anthropic-native-v1');
      const restored=await codec.decodeRequest(o.body,ACCOUNT);
      assert.equal(new TextDecoder().decode(restored),original);return reply(job);
    }
    const url=new URL(path,'https://stub.invalid');assert.equal(url.searchParams.get('transport'),codec.QUERY);
    const after=Number(url.searchParams.get('after'));
    const page=after===0?{...job,events:[{seq:1,data:JSON.stringify({choices:[{delta:{content:'resposta'.repeat(2000)}}]})}],cursor:1,has_more:true}
      :{...job,status:'completed',events:[{seq:2,data:'[DONE]'}],cursor:2,has_more:false};
    return new Response(await codec.pageCandidate(encode(page),ACCOUNT,{kind:'page',job_id:ID,after}));
  }});
  const record=await h.jobs.begin(input);original=JSON.stringify(record.payload);
  const values=await drain(h,record);assert.equal(values.length,2);assert.equal(values.at(-1),'data: [DONE]');
  assert.equal(JSON.stringify(record.payload),original);assert.equal(h.calls.filter(x=>x.options.method==='POST').length,1);
  assert.equal(h.imports(),1);assert.equal(h.calls.filter(x=>x.path==='/api/chat-jobs/session').length,2);
});

for(const [name,options] of [['no_capability',{transport:null}],['missing_browser_api',{unsupported:true}],['failed_lazy_import',{importFailure:true}]]) {
 await test(name+'_identity_before_send',async()=>{
   const h=await harness({...options,onFetch:async(path,o)=>{
     if(path==='/api/chat-jobs'){assert.equal(typeof o.body,'string');assert(!JSON.parse(o.body).iald_transport);return reply(job);}
     assert(!path.includes('transport='));return reply({...job,status:'completed',events:[{seq:1,data:'[DONE]'}],cursor:1,has_more:false});
   }});
   const r=await h.jobs.begin(input);await drain(h,r);
   assert.equal(h.calls.filter(x=>x.options.method==='POST').length,1);
   assert.equal(h.imports(),name==='no_capability'?0:1);
 });
}

await test('post_timeout_no_fallback_no_resubmit_on_resume',async()=>{
 const h=await harness({onFetch:async(path,o)=>{if(o.method==='POST')throw Error('lost response');return reply({error:'not found'},404);}});
 const r=await h.jobs.begin(input);await assert.rejects(()=>drain(h,r));assert(r.attempted);
 await assert.rejects(()=>drain(h,r));assert.equal(h.calls.filter(x=>x.options.method==='POST').length,1);
 assert(h.calls.some(x=>x.path==='/api/chat-jobs/'+ID));
});
await test('post_http_error_no_identity_retry',async()=>{
 const h=await harness({onFetch:async()=>reply({error:'unsupported'},415)});
 const r=await h.jobs.begin(input);await assert.rejects(()=>drain(h,r));
 assert.equal(h.calls.filter(x=>x.options.method==='POST').length,1);
});
await test('corrupt_compressed_page_no_event_no_cursor_advance_no_repost',async()=>{
 const h=await harness({onFetch:async(path,o)=>{
   if(o.method==='POST')return reply(job);
   const page={...job,status:'completed',events:[{seq:1,data:'[DONE]'}],cursor:1,has_more:false};
   const env=await codec.encodeEnvelope(encode(page),ACCOUNT,{kind:'page',job_id:ID,after:0},codec.PAGE_LIMIT);
   env.sha256='0'.repeat(64);return reply({iald_transport:env});
 }});
 const r=await h.jobs.begin(input);let emitted=0;
 await assert.rejects(async()=>{for await(const x of h.jobs.stream(r))emitted++;});
 assert.equal(emitted,0);assert.equal(r.status,'running');
 assert(!h.calls.some(x=>x.path.includes('after=1')));
 await assert.rejects(()=>drain(h,r));assert.equal(h.calls.filter(x=>x.options.method==='POST').length,1);
});
await test('wrong_page_binding_refused_before_cursor',async()=>{
 const h=await harness({onFetch:async(path,o)=>{
   if(o.method==='POST')return reply(job);
   const env=await codec.encodeEnvelope(encode({...job,events:[],cursor:1,has_more:false}),ACCOUNT,{kind:'page',job_id:ID,after:9},codec.PAGE_LIMIT);
   return reply({iald_transport:env});
 }});const r=await h.jobs.begin(input);await assert.rejects(()=>drain(h,r));assert(!h.calls.some(x=>x.path.includes('after=1')));
});
await test('negotiated_small_payload_identity_without_truncation',async()=>{
 const h=await harness({onFetch:async(path,o)=>{
   if(o.method==='POST'){const data=JSON.parse(new TextDecoder().decode(o.body));assert.equal(data.messages[0].content,'ç');assert(!data.iald_transport);return reply(job);}
   return reply({...job,status:'completed',events:[{seq:1,data:'[DONE]'}],cursor:1,has_more:false});
 }});const r=await h.jobs.begin({iald_conv:'conversation1',messages:[{role:'user',content:'ç'}]});await drain(h,r);
});
await test('expired_negotiated_page_retains_terminal_410',async()=>{
 const h=await harness({onFetch:async(path,o)=>o.method==='POST'?reply(job):reply({},410)});
 const r=await h.jobs.begin(input);await assert.rejects(()=>drain(h,r));assert.equal(r.status,'expired');
});

await test('concurrent_streams_share_persisted_attempt_and_never_double_post',async()=>{
 const h=await harness({onFetch:async(path,o)=>o.method==='POST'?reply(job):
   reply({...job,status:'completed',events:[{seq:1,data:'[DONE]'}],cursor:1,has_more:false})});
 const r=await h.jobs.begin(input),r2=JSON.parse(JSON.stringify(r));
 await Promise.allSettled([drain(h,r),drain(h,r2)]);
 assert.equal(h.calls.filter(x=>x.options.method==='POST').length,1);
});
await test('account_generation_change_during_post_stops_page_processing',async()=>{
 let h;
 h=await harness({onFetch:async()=>{h.jobs.setOwner('b'.repeat(64));return reply(job);}});
 const r=await h.jobs.begin(input);await assert.rejects(()=>drain(h,r));
 assert.equal(h.calls.filter(x=>x.options.method==='POST').length,1);
 assert(!h.calls.some(x=>x.path.includes('after=')));
});
await test('moderation_withdrawal_sequence_exception_and_done_preserved',async()=>{
 const h=await harness({onFetch:async(path,o)=>{
   if(o.method==='POST')return reply(job);
   const page={...job,status:'completed',events:[
     {seq:5,data:JSON.stringify({iald_aviso:{retirar_resposta:true}})},
     {seq:6,data:'[DONE]'}],cursor:6,has_more:false};
   return new Response(await codec.pageCandidate(encode(page),ACCOUNT,{kind:'page',job_id:ID,after:0}));
 }});const r=await h.jobs.begin(input);const values=await drain(h,r);
 assert.equal(values.length,2);assert(values[0].includes('retirar_resposta'));assert.equal(values[1],'data: [DONE]');
});
await test('bounded_page_stream_cancels_overflow_before_any_event',async()=>{
 let cancelled=false;
 const h=await harness({onFetch:async(path,o)=>{
   if(o.method==='POST')return reply(job);
   return new Response(new ReadableStream({pull(controller){controller.enqueue(new Uint8Array(1024*1024));},cancel(){cancelled=true;}}));
 }});const r=await h.jobs.begin(input);let emitted=0;
 await assert.rejects(async()=>{for await(const x of h.jobs.stream(r))emitted++;});
 assert.equal(emitted,0);assert(cancelled);assert(!h.calls.some(x=>x.path.includes('after=1')));
});

const report={status:results.every(x=>x.pass)?'PASS':'FAIL',checks:results.length,results,
 scope:'VM executes actual staged durable-client and authenticated fetchIALD source slices, actual ESM wrapper and pinned codec; network stub only. UI startup and real WebViews not executed.',network_calls:0,provider_calls:0};
fs.writeFileSync(new URL('TEST_RESULTS.json',root),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report));if(report.status!=='PASS')process.exitCode=1;
