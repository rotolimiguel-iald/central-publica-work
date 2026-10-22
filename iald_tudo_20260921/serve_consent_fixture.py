from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import re
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD\app')
js=ROOT.joinpath('iald.js').read_text(encoding='utf-8')
html=ROOT.joinpath('index.html').read_text(encoding='utf-8')
sheet=html[html.index('<div class="folha-fundo" id="folha-consentimento"'):html.index('<!-- Bibliotecas embarcadas')]
functions=js[js.index('function abrirConsentimento('):js.index('async function alternarConsentimento(')]
page='''<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="/iald.css">
<h1>Teste local do consentimento</h1><label>Resposta simulada <select id="scenario"><option>success</option><option>offline</option><option>wrong-provider</option><option>invalid-json</option><option>conflict</option></select></label>
<button id="open">Abrir aviso</button><p id="result" role="status"></p>'''+sheet+r'''<script>
const S={motor:{provedor:'Anthropic',consentimento:{provedor:'Anthropic'},consentimentos:[]}};
const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text)n.textContent=text;return n};
const avisar=(text)=>{document.getElementById('result').textContent=text};
const pintarMotor=()=>{};
const carregarMotor=async()=>{};
const consentimentoDe=()=>({texto:terms,provedor:'Anthropic',versao:2});
const fecharFolhas=()=>{document.getElementById('folha-consentimento').dataset.aberta=''};
const abrirFolha=id=>{document.getElementById(id).dataset.aberta='1'};
const reenviarUltima=()=>{document.getElementById('result').textContent='Mensagem reenviada após aceite confirmado'};
let requests=0;
const fetchIALD=async(path,opts)=>{
 const scenario=document.getElementById('scenario').value;requests++;
 document.getElementById('result').textContent='Requisições: '+requests;
 await new Promise(r=>setTimeout(r,500));
 if(scenario==='offline')throw new Error('offline');
 return {ok:scenario!=='conflict',status:scenario==='conflict'?409:200,json:async()=>{
 if(scenario==='invalid-json')throw new Error('not JSON');
 return {ok:true,consentido:true,provedor:scenario==='wrong-provider'?'OpenAI':'Anthropic',error:scenario==='conflict'?'Modelo alterado':undefined};}};
};
const terms=('Aviso fictício para teste de interface. Nada é enviado à Anthropic. Os termos reais não são alterados por esta bancada. Leia o conteúdo antes de decidir.\n\n').repeat(18);
'''+functions+'''
document.getElementById('btn-consentir').onclick=consentirEContinuar;
document.getElementById('btn-recusar-consentimento').onclick=fecharFolhas;
document.querySelector('[data-fechar]').onclick=fecharFolhas;
document.getElementById('open').onclick=()=>abrirConsentimento(terms,'Anthropic',1);
abrirConsentimento(terms,'Anthropic',1);
</script>'''
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  data=ROOT.joinpath('iald.css').read_bytes() if self.path=='/iald.css' else page.encode()
  self.send_response(200);self.send_header('Content-Type','text/css' if self.path=='/iald.css' else 'text/html; charset=utf-8');self.end_headers();self.wfile.write(data)
 def log_message(self,*args):pass
print('Consent fixture at http://127.0.0.1:8794',flush=True)
HTTPServer(('127.0.0.1',8794),Handler).serve_forever()
