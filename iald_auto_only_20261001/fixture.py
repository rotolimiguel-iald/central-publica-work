from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
import mimetypes,json
W=Path(__file__).parent;R=Path(r'C:\IALD\projetos_pyhton\IALD\app')
class H(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  u=urlsplit(self.path);rel=u.path.lstrip('/') or 'index.html';p=(R/rel).resolve()
  if not p.is_relative_to(R) or not p.is_file() or p.suffix not in ('.js','.css','.html','.png','.woff2','.woff','.ttf','.ico','.svg') or '.bak_' in rel:
   self.send_error(404);return
  data=(W/'stage/app/iald.js').read_bytes() if rel=='iald.js' else p.read_bytes()
  if rel=='iald.js':
   js="""
// Isolated synthetic fixture; real APIs blocked by CSP.
const fixtureManual = new URLSearchParams(location.search).get('account') === 'luiz';
S.motor = {motor:'automatico', motor_selecao:'automatico', rotulo:'IALD Automática', provedor:'TypeSafe (JEV)',
  pode_escolher:fixtureManual, opcoes:fixtureManual ? [{id:'automatico',rotulo:'IALD Automática',disponivel:true},{id:'mimo',rotulo:'MiMo',disponivel:true},{id:'claude-sonnet',rotulo:'Sonnet',disponivel:true}] : [],
  consentimento:{necessario:true,dado:true,provedor:'TypeSafe (JEV)'},
  provedores_automaticos:[{provedor:'Moonshot AI',dado:false,versao:1,texto:'Aviso de teste: somente dados sintéticos.'}],
  consentimentos:[{provedor:'OpenAI',dado:true}]};
pintarMotor();
"""
   data+=js.encode()
  self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(rel)[0] or 'application/octet-stream');self.send_header('Cache-Control','no-store')
  self.send_header('Content-Security-Policy',"default-src 'self' data: blob:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'none'")
  self.end_headers();self.wfile.write(data)
print('Synthetic UI fixture 127.0.0.1:8798',flush=True)
ThreadingHTTPServer(('127.0.0.1',8798),H).serve_forever()
