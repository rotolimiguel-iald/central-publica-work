"""Loopback-only, synthetic codec probe. Serves exactly two public test assets."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parent
codec=(W/'client_server_stage/chat_wire_codec.mjs').read_bytes()
html='''<!doctype html><meta charset="utf-8"><title>IALD — Teste local do transporte</title>
<style>body{font:16px system-ui;max-width:800px;margin:40px auto}pre{white-space:pre-wrap}</style>
<h1>Teste local do transporte IALD</h1><p>Dados sintéticos; nenhuma mensagem enviada a modelos.</p>
<button id="run">Executar teste</button><pre id="result">Aguardando.</pre>
<script type="module">
import {codecAvailable,encodeEnvelope,decodeEnvelope,prepareRequest,PROTOCOL,CODEC,REQUEST_LIMIT} from './codec.mjs';
const out=document.querySelector('#result');
document.querySelector('#run').onclick=async()=>{try{
 const available=await codecAvailable();
 const binding={kind:'request',request_id:'browser-control-1',conversation:'synthetic'};
 const raw=new TextEncoder().encode(JSON.stringify({account:'synthetic-account',request_id:binding.request_id,iald_conv:'synthetic',messages:[{role:'user',content:'Teste sintético: identidade, Unicode β, fórmula e linha.\\n'.repeat(2000)}]}));
 const start=performance.now();
 if(!available){out.textContent=JSON.stringify({status:'IDENTITY_FALLBACK',available},null,2);return;}
 const packet=await encodeEnvelope(raw,'synthetic-account',binding,REQUEST_LIMIT);
 const restored=await decodeEnvelope(packet,'synthetic-account',binding,REQUEST_LIMIT);
 const equal=raw.length===restored.length&&raw.every((v,i)=>v===restored[i]);
 const prepared=await prepareRequest(raw,{account:'synthetic-account',transport:{protocol:PROTOCOL,codec:CODEC,bases:false}});
 let rejected=false;try{await decodeEnvelope({...packet,sha256:'0'.repeat(64)},'synthetic-account',binding,REQUEST_LIMIT);}catch{rejected=true;}
 out.textContent=JSON.stringify({status:equal&&rejected?'PASS':'FAIL',available,exact_bytes:equal,corrupt_hash_rejected:rejected,raw_bytes:raw.length,wire_bytes:prepared.body.length,mode:prepared.mode,local_ms:Math.round(performance.now()-start),model_calls:0},null,2);
}catch(e){out.textContent=JSON.stringify({status:'FAIL',reason:e.code||e.name});}};
</script>'''.encode()
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data,kind=(html,'text/html; charset=utf-8') if self.path=='/' else (codec,'text/javascript; charset=utf-8') if self.path=='/codec.mjs' else (b'Not found','text/plain')
        self.send_response(200 if self.path in ('/','/codec.mjs') else 404)
        self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)
    def log_message(self,*args):pass
server=HTTPServer(('127.0.0.1',0),Handler)
print(json.dumps({'port':server.server_port,'codec_sha256':hashlib.sha256(codec).hexdigest()}),flush=True)
server.serve_forever()
