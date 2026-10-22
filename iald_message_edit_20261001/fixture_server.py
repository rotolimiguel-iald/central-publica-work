from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlsplit, parse_qs, unquote
import json, mimetypes
W=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD\app')
class H(BaseHTTPRequestHandler):
 def log_message(self,*args): pass
 def do_GET(self):
  u=urlsplit(self.path); p=unquote(u.path); q=parse_qs(u.query)
  version=p.split('/')[1] if len(p.split('/'))>1 else ''
  if version not in ('old','new'): self.send_error(404); return
  rel='/'.join(p.split('/')[2:]) or 'index.html'
  target=(R/rel).resolve()
  if not target.is_relative_to(R) or not target.is_file() or target.suffix not in ('.js','.css','.html','.png','.svg','.woff2','.woff','.ttf','.ico'):
   self.send_error(404);return
  data=((W/'stage'/rel) if version=='new' and rel in ('iald.js','iald.css') else target).read_bytes()
  if rel=='index.html':
   text='Mensagem de teste: quero editar este texto sem perder as palavras.\nSegunda linha com acentos: ação, coração e fórmula β.'
   if q.get('long')==['1']: text='\n'.join(f'Linha {i+1}: texto longo para verificar a edição e a posição do cursor.' for i in range(30))
   c=dict(id='fixture_editor',titulo='Teste de edição',criada=1,atualizada=1,mensagens=[dict(role='user',content=text),dict(role='assistant',content='Resposta interrompida de demonstração.')])
   values={'iald_conversas_v2':[c], 'iald_conversa_ativa_v2':c['id'], 'iald_tema':q.get('theme',['claro'])[0]}
   seed=''.join('localStorage.setItem('+json.dumps(k)+','+json.dumps(json.dumps(v))+');' for k,v in values.items())
   # Synthetic isolated localhost storage, no real user data or network.
   data=data.replace(b'<head>',('<head><script>'+seed+'</script>').encode())
  self.send_response(200)
  self.send_header('Content-Type',mimetypes.guess_type(rel)[0] or 'application/octet-stream')
  self.send_header('Cache-Control','no-store')
  self.send_header('Content-Security-Policy',"default-src 'self' data: blob:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'none'")
  self.end_headers();self.wfile.write(data)
print('Local isolated editor fixture on 127.0.0.1:8799',flush=True)
ThreadingHTTPServer(('127.0.0.1',8799),H).serve_forever()
