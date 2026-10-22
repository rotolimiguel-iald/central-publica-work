// Stateless byte transport control. Browser-native APIs; no Node imports, network or keys.
export const PROTOCOL='iald-byte-envelope/1', CODEC='deflate-base64', QUERY='iald-byte-envelope-v1';
export const REQUEST_LIMIT=20*1024*1024, PAGE_LIMIT=2*16*1024*1024+262144, WIRE_LIMIT=20*1024*1024;
// Identity pages follow legacy JSON semantics. Derived from retained event bytes,
// worst-case JSON escapes (6x), and 256 KiB metadata under the current page schema.
// Recalculate if storage cipher, event cap or page schema changes.
export const IDENTITY_PAGE_LIMIT=6*16*1024*1024+262144;
export function identityPageJSON(raw){
  need(raw instanceof Uint8Array&&raw.byteLength<=IDENTITY_PAGE_LIMIT,'page_wire_limit');
  try{return JSON.parse(new TextDecoder('utf-8').decode(raw));}
  catch{throw new WireError('invalid_utf8_json');}
}
const MAX_DEPTH=128,MAX_NODES=500000,enc=new TextEncoder();
export class WireError extends Error { constructor(code){super(code);this.code=code;this.noRetry=true;} }
const need=(ok,code)=>{if(!ok)throw new WireError(code);};
const exact=(o,keys)=>o!==null&&typeof o==='object'&&!Array.isArray(o)&&Object.keys(o).sort().join('|')===[...keys].sort().join('|');
const id=s=>typeof s==='string'&&/^[A-Za-z0-9_-]{1,100}$/.test(s);
const scopeOK=s=>typeof s==='string'&&s.length>0&&s.length<=256&&![...s].some(c=>c.charCodeAt(0)<32);
const jsonBytes=value=>enc.encode(JSON.stringify(value));
function bindingCheck(b){
  if(b?.kind==='request')need(exact(b,['kind','request_id','conversation'])&&id(b.request_id)&&id(b.conversation)&&b.conversation.length<=64,'invalid_binding');
  else need(exact(b,['kind','job_id','after'])&&b.kind==='page'&&id(b.job_id)&&Number.isSafeInteger(b.after)&&b.after>=0,'invalid_binding');
}
function bindingEqual(a,b){bindingCheck(a);bindingCheck(b);return a.kind===b.kind&&(a.kind==='request'?a.request_id===b.request_id&&a.conversation===b.conversation:a.job_id===b.job_id&&a.after===b.after);}
export function strictJSON(raw,limit){
  need(raw instanceof Uint8Array&&raw.byteLength<=limit,'decoded_limit');
  let text;try{text=new TextDecoder('utf-8',{fatal:true,ignoreBOM:true}).decode(raw);}catch{throw new WireError('invalid_utf8_json');}
  let i=0,nodes=0;
  const ws=()=>{while(i<text.length&&/[\x20\x09\x0a\x0d]/.test(text[i]))i++;};
  function str(){
    const start=i++;let escaped=false;
    while(i<text.length){const c=text[i++];if(!escaped&&c==='"'){try{return JSON.parse(text.slice(start,i));}catch{throw new WireError('invalid_utf8_json');}}if(!escaped&&c==='\\')escaped=true;else escaped=false;}
    throw new WireError('invalid_utf8_json');
  }
  function value(depth){
    need(depth<=MAX_DEPTH&&++nodes<=MAX_NODES,'json_structure_limit');ws();const c=text[i];
    if(c==='"'){str();return;}
    if(c==='{'){
      i++;ws();const keys=new Set();if(text[i]==='}'){i++;return;}
      while(true){need(text[i]==='"','invalid_utf8_json');const key=str();need(!keys.has(key),'duplicate_json_key');keys.add(key);ws();need(text[i++]===':','invalid_utf8_json');value(depth+1);ws();const end=text[i++];if(end==='}')return;need(end===',','invalid_utf8_json');ws();}
    }
    if(c==='['){i++;ws();if(text[i]===']'){i++;return;}while(true){value(depth+1);ws();const end=text[i++];if(end===']')return;need(end===',','invalid_utf8_json');}}
    for(const literal of ['true','false','null'])if(text.startsWith(literal,i)){i+=literal.length;return;}
    const m=/-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/y;m.lastIndex=i;const found=m.exec(text);
    need(!!found,'invalid_utf8_json');need(Number.isFinite(Number(found[0])),'nonfinite_json');i=m.lastIndex;
  }
  value(0);ws();need(i===text.length,'invalid_utf8_json');
  try{return JSON.parse(text);}catch{throw new WireError('invalid_utf8_json');}
}
async function hash(raw){need(!!globalThis.crypto?.subtle,'crypto_unavailable');return [...new Uint8Array(await crypto.subtle.digest('SHA-256',raw))].map(v=>v.toString(16).padStart(2,'0')).join('');}
function b64(raw){let text='';for(let i=0;i<raw.length;i+=8192)text+=String.fromCharCode(...raw.subarray(i,i+8192));return btoa(text);}
function unb64(text){
  need(typeof text==='string'&&text.length<=4*Math.ceil(WIRE_LIMIT/3),'wire_limit');
  need(text.length%4===0,'invalid_base64');
  let end=text.length;if(end&&text[end-1]==='=')end--;if(end&&text[end-1]==='=')end--;
  for(let i=0;i<end;i++){const c=text.charCodeAt(i);need((c>=65&&c<=90)||(c>=97&&c<=122)||(c>=48&&c<=57)||c===43||c===47,'invalid_base64');}
  need(text.length-end<=2,'invalid_base64');
  let value;try{const decoded=atob(text);value=new Uint8Array(decoded.length);for(let i=0;i<decoded.length;i++)value[i]=decoded.charCodeAt(i);}catch{throw new WireError('invalid_base64');}
  need(value.length<=WIRE_LIMIT&&b64(value)===text,'invalid_base64_or_wire_limit');return value;
}
async function collect(stream,limit){
  const reader=stream.getReader(),parts=[];let size=0;
  try{while(true){const {value,done}=await reader.read();if(done)break;size+=value.byteLength;need(size<=limit,'decoded_limit');parts.push(value);}}
  catch(e){try{await reader.cancel(e);}catch{}throw e instanceof WireError?e:new WireError('invalid_deflate');}
  const out=new Uint8Array(size);let offset=0;for(const part of parts){out.set(part,offset);offset+=part.length;}return out;
}
async function deflate(raw){return collect(new Blob([raw]).stream().pipeThrough(new CompressionStream('deflate')),WIRE_LIMIT);}
async function inflate(raw,limit){return collect(new Blob([raw]).stream().pipeThrough(new DecompressionStream('deflate')),limit);}
let probePromise;
export async function codecAvailable(){
  if(!probePromise)probePromise=(async()=>{
    if(typeof CompressionStream!=='function'||typeof DecompressionStream!=='function'||!globalThis.crypto?.subtle)return false;
    try{
      const wire=await deflate(enc.encode('{}'));need(new TextDecoder().decode(await inflate(wire,2))==='{}','probe_roundtrip');
      const extra=new Uint8Array(wire.length+1);extra.set(wire);extra[wire.length]=120;
      try{await inflate(extra,64);return false;}catch{}
      const concat=new Uint8Array(wire.length*2);concat.set(wire);concat.set(wire,wire.length);
      try{await inflate(concat,64);return false;}catch{}
      return true;
    }catch{return false;}
  })();return probePromise;
}
export async function encodeEnvelope(raw,scope,binding,limit){
  need(scopeOK(scope),'invalid_scope');bindingCheck(binding);strictJSON(raw,limit);
  const compressed=await deflate(raw);
  return {protocol:PROTOCOL,codec:CODEC,scope,binding,raw_bytes:raw.length,sha256:await hash(raw),data:b64(compressed)};
}
export async function decodeEnvelope(e,scope,binding,limit){
  need(scopeOK(scope),'invalid_scope');bindingCheck(binding);
  need(exact(e,['protocol','codec','scope','binding','raw_bytes','sha256','data']),'invalid_envelope');
  need(e.protocol===PROTOCOL&&e.codec===CODEC,'unsupported_codec');
  need(e.scope===scope&&bindingEqual(e.binding,binding),'scope_or_binding_mismatch');
  need(Number.isSafeInteger(e.raw_bytes)&&e.raw_bytes>=0&&e.raw_bytes<=limit,'decoded_limit');
  need(typeof e.sha256==='string'&&/^[a-f0-9]{64}$/.test(e.sha256),'invalid_hash');
  const raw=await inflate(unb64(e.data),e.raw_bytes);need(raw.length===e.raw_bytes,'deflate_length_or_trailing');
  need(await hash(raw)===e.sha256,'hash_mismatch');strictJSON(raw,limit);return raw;
}
function requestBinding(obj){const b={kind:'request',request_id:obj?.request_id,conversation:obj?.iald_conv};bindingCheck(b);return b;}
function worth(raw,packet){return packet.length<=WIRE_LIMIT&&raw.length-packet.length>=Math.max(1024,Math.ceil(raw.length*.05));}
export async function prepareRequest(raw,session,{available=codecAvailable,compress=encodeEnvelope}={}){
  const obj=strictJSON(raw,REQUEST_LIMIT);need(scopeOK(session?.account)&&obj&&obj.account===session.account,'account_changed');const binding=requestBinding(obj);
  const cap=session.transport;
  if(cap?.protocol!==PROTOCOL||cap.codec!==CODEC||cap.bases!==false||!await available())return {body:raw,mode:'identity',reason:'not_negotiated_or_unavailable'};
  // Compression exceptions are local PRE-SEND fallback only. Validation above never falls back.
  let packet;
  try{packet=jsonBytes({account:obj.account,request_id:obj.request_id,iald_conv:obj.iald_conv,iald_transport:await compress(raw,obj.account,binding,REQUEST_LIMIT)});}
  catch{return {body:raw,mode:'identity',reason:'local_compression_unavailable'};}
  return worth(raw,packet)?{body:packet,mode:'envelope',reason:'smaller',raw_bytes:raw.length,wire_bytes:packet.length}:{body:raw,mode:'identity',reason:'not_smaller'};
}
export async function sendOnce(raw,session,send,options={}){
  const prepared=await prepareRequest(raw,session,options);
  try{return {prepared,response:await send(prepared.body),attempts:1};}
  catch{const e=new WireError('send_uncertain_no_retry');e.sent=true;e.attempts=1;throw e;}
}
export async function decodeRequest(wire,scope){
  const outer=strictJSON(wire,WIRE_LIMIT);need(exact(outer,['account','request_id','iald_conv','iald_transport']),'invalid_request_wrapper');
  need(outer.account===scope,'account_changed');const binding=requestBinding(outer);
  const raw=await decodeEnvelope(outer.iald_transport,scope,binding,REQUEST_LIMIT),obj=strictJSON(raw,REQUEST_LIMIT);
  need(obj?.account===scope&&bindingEqual(requestBinding(obj),binding),'inner_outer_mismatch');need(!Object.hasOwn(obj,'iald_transport'),'nested_envelope');return raw;
}
export async function decodePage(wire,scope,binding){
  const obj=identityPageJSON(wire);
  if(obj&&typeof obj==='object'&&Object.hasOwn(obj,'iald_transport')){
    need(exact(obj,['iald_transport'])&&wire.length<=WIRE_LIMIT,'invalid_page_wrapper');
    const strict=strictJSON(wire,WIRE_LIMIT);
    return decodeEnvelope(strict.iald_transport,scope,binding,PAGE_LIMIT);
  }return wire;
}
export async function pageCandidate(raw,scope,binding){
  strictJSON(raw,PAGE_LIMIT);need(scopeOK(scope),'invalid_scope');bindingCheck(binding);
  let packet;try{packet=jsonBytes({iald_transport:await encodeEnvelope(raw,scope,binding,PAGE_LIMIT)});}catch(e){if(e.code==='decoded_limit')return raw;throw e;}return worth(raw,packet)?packet:raw;
}
