import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {webcrypto} from 'node:crypto';
import * as codec from './fixtures/client_control/chat_wire_codec.mjs';
import {spawn} from 'node:child_process';
import readline from 'node:readline';
import {fileURLToPath} from 'node:url';

const root=new URL('./fixtures/client_control/',import.meta.url);
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

const child=spawn('C:/Python314/python.exe',['-B','-X','utf8',fileURLToPath(new URL('flask_rpc.py',import.meta.url))],{stdio:['pipe','pipe','pipe']});
let stderr='';child.stderr.on('data',b=>stderr+=b);const pending=[];
readline.createInterface({input:child.stdout}).on('line',line=>{const item=pending.shift();try{item.resolve(JSON.parse(line));}catch(e){item.reject(e);}});
const done=new Promise((resolve,reject)=>child.on('exit',code=>code===0?resolve():reject(Error(stderr||'bridge failed '+code))));
async function rpc(path,o){
 const body=o.body===undefined?Buffer.alloc(0):Buffer.from(o.body);
 const result=await new Promise((resolve,reject)=>{pending.push({resolve,reject});child.stdin.write(JSON.stringify({path,method:o.method||'GET',headers:o.headers||{},body:body.toString('base64')})+'\n');});
 return new Response(Buffer.from(result.body,'base64'),{status:result.status,headers:result.headers});
}
await test('actual_staged_client_to_real_Flask_R2_no_network',async()=>{
 const h=await harness({onFetch:rpc});
 const record=await h.jobs.begin({iald_conv:'conversation1',stream:true,messages:[{role:'user',content:'ação 🧪 sem perdas '.repeat(3000)}]});
 const values=[];for await(const v of h.jobs.stream(record))values.push(v);
 assert.equal(h.calls.filter(r=>r.options.method==='POST').length,1);
 assert(h.calls.filter(r=>r.path.includes('transport='+codec.QUERY)).length>=2);
 assert(values.some(v=>v.includes('resposta íntegra')));assert.equal(values.at(-1),'data: [DONE]');
});
child.stdin.end();await done;
const report={status:results.every(x=>x.pass)?'PASS':'FAIL',results,network_calls:0,provider_calls:0,scope:'Actual pinned staged client durable/fetchIALD/transport/codec in VM -> stdio bridge -> real R2 Flask register/ChatJobs/media guard, synthetic account/memory/cipher/SSE. HTTPS public Origin over HTTP test host.'};
fs.writeFileSync(new URL('INTEGRATED_TEST_RESULTS.json',import.meta.url),JSON.stringify(report,null,2));
console.log(JSON.stringify(report));if(report.status!=='PASS')process.exitCode=1;
