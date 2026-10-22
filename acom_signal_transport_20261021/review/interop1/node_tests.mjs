import fs from 'node:fs';
import {performance} from 'node:perf_hooks';
import * as c from './chat_wire_codec.mjs';
const dir=process.argv[2], spec=JSON.parse(fs.readFileSync(`${dir}/cases.json`)), results=[], bench=[];
const bytes=p=>new Uint8Array(fs.readFileSync(`${dir}/${p}`));
const equal=(a,b)=>Buffer.from(a).equals(Buffer.from(b));
async function test(name,fn){try{await fn();results.push({name,pass:true});}catch(e){results.push({name,pass:false,error:String(e.stack)});}}
const assert=(x)=>{if(!x)throw Error('assertion failed');};
await test('native_api_probe_strict_trailing_and_concat',async()=>assert(await c.codecAvailable()));
for(const item of spec.good){
 await test(`Python_to_Node_${item.name}`,async()=>{
  const wire=bytes(item.packet),raw=bytes(item.raw),t=performance.now();
  const out=await c.decodeEnvelope(JSON.parse(new TextDecoder().decode(wire)),spec.scope,item.binding,item.limit);
  assert(equal(raw,out));bench.push({case:item.name,operation:'decode_python_packet',ms:performance.now()-t,raw_bytes:raw.length,packet_bytes:wire.length});
 });
 await test(`Node_to_Python_${item.name}`,async()=>{
  const raw=bytes(item.raw),t=performance.now(),env=await c.encodeEnvelope(raw,spec.scope,item.binding,item.limit);
  const packet=JSON.stringify(env);fs.writeFileSync(`${dir}/node_${item.name}.json`,packet);
  bench.push({case:item.name,operation:'encode',ms:performance.now()-t,raw_bytes:raw.length,packet_bytes:Buffer.byteLength(packet)});
 });
}
for(const item of spec.bad){await test(`reject_${item.name}`,async()=>{
 let refused=false;try{await c.decodeEnvelope(JSON.parse(fs.readFileSync(`${dir}/${item.packet}`,'utf8')),item.scope??spec.scope,item.binding??spec.binding,c.REQUEST_LIMIT);}catch(e){refused=e instanceof c.WireError;}
 assert(refused);
});}
for(const [name,text] of [['duplicate','{"x":1,"x":2}'],['utf8',null],['nonfinite','1e999'],['trailingjson','{}x'],['deep','['.repeat(130)+'0'+']'.repeat(130)]])await test(`json_${name}`,async()=>{
 let refused=false;try{c.strictJSON(text===null?new Uint8Array([255]):new TextEncoder().encode(text),c.REQUEST_LIMIT);}catch(e){refused=e instanceof c.WireError;}assert(refused);
});
const raw=bytes(spec.request_raw),small=bytes(spec.small_raw),cap={protocol:c.PROTOCOL,codec:c.CODEC,bases:false},session={account:spec.scope,transport:cap};
for(const [name,ss,options] of [['missing_caps',{account:spec.scope},{}],['unavailable',session,{available:async()=>false}],['local_compress_failure',session,{available:async()=>true,compress:async()=>{throw Error('local');}}]])await test(`fallback_before_send_${name}`,async()=>{
 let calls=0;const r=await c.sendOnce(raw,ss,async body=>{calls++;assert(equal(body,raw));return {status:200};},options);assert(calls===1&&r.prepared.mode==='identity');
});
await test('no_gain_identity',async()=>{const r=await c.prepareRequest(small,session);assert(r.mode==='identity'&&equal(r.body,small));});
await test('incompressible_multimegabyte_identity',async()=>{const r=await c.prepareRequest(bytes(spec.incompressible_request),session);assert(r.mode==='identity');});
await test('request_roundtrip_exact_utf8_whitespace',async()=>{const r=await c.prepareRequest(raw,session);assert(r.mode==='envelope');assert(equal(await c.decodeRequest(r.body,spec.scope),raw));});
await test('uncertain_exactly_one_attempt',async()=>{let calls=0,ok=false;try{await c.sendOnce(raw,session,async()=>{calls++;throw Error('lost response');});}catch(e){ok=e.code==='send_uncertain_no_retry'&&e.attempts===1;}assert(ok&&calls===1);});
await test('no_dispatch_refusal_never_auto_retry',async()=>{let calls=0;const r=await c.sendOnce(raw,session,async()=>{calls++;return {status:409,no_dispatch_this_submission:true};});assert(calls===1&&r.response.status===409);});
await test('independent_pages_cursor_replay_rejected',async()=>{
 const b={kind:'page',job_id:'job1',after:0},r=await c.pageCandidate(raw,spec.scope,b);assert(equal(await c.decodePage(r,spec.scope,b),raw));
 let refused=false;try{await c.decodePage(r,spec.scope,{...b,after:1});}catch{refused=true;}assert(refused);
});
await test('request_over_20MiB_refused_before_send',async()=>{let calls=0,refused=false;try{await c.sendOnce(new Uint8Array(c.REQUEST_LIMIT+1),session,async()=>{calls++;});}catch{refused=true;}assert(refused&&calls===0);});
fs.writeFileSync(`${dir}/node_results.json`,JSON.stringify({node:process.version,results,bench},null,2));
if(results.some(r=>!r.pass))process.exitCode=1;
