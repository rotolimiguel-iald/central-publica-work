from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit
import mimetypes

ROOT=Path(r'C:\IALD\projetos_pyhton\IALD\app')
STAGE=Path(__file__).parent/'stage/app'
EXTRA=r'''
const fixture = document.createElement('section');
fixture.id='fixture-results';
fixture.style.cssText='position:fixed;inset:0;background:var(--bg,#101820);z-index:99999;overflow:auto;padding:16px';
document.body.append(fixture);
const h=document.createElement('h2');h.textContent='Teste local · streaming e fórmulas';fixture.append(h);
const status=document.createElement('p');fixture.append(status);
const preview=document.createElement('div');preview.style.cssText='max-width:360px;margin:10px auto;border:1px solid #789;padding:12px';fixture.append(preview);
const formula=String.raw`\[H_{3L}=D_c^\dagger D_c+D_b^\dagger D_b+D_z^\dagger D_z\geq0\]`;
const response=String.raw`A expressão é preservada durante a resposta.

\[\beta_{\mathrm{TGL}}=\alpha\sqrt e\]

\[\dot\rho=-i[H,\rho]+\sum_k\left(L_k\rho L_k^\dagger-\frac12\{L_k^\dagger L_k,\rho\}\right)\]

\[H_{3L}=\sum_j D_j^\dagger D_j\geq0\]

Cada fórmula usa a mesma renderização para todos os modelos.`;
let checks=0;
try {
  for(const value of [formula,String.raw`$$\beta=\alpha\sqrt e$$`,String.raw`\(J^2=I\)`]) {
    const a=renderMarkdown(value,true),b=renderMarkdown(value,false);
    if(!a.querySelector('.katex')||a.querySelector('.katex-error')||a.innerHTML!==b.innerHTML)throw Error('Renderização divergiu');checks++;
  }
  for(let n=2;n<formula.length;n++) {
    const block=renderMarkdown(formula.slice(0,n),true);
    if(block.querySelector('.katex-error')||!block.querySelector('.iald-math-pending'))throw Error('Expressão incompleta renderizada');checks++;
  }
  const unsafe=renderMarkdown('<img src=x onerror="alert(1)"><script>alert(1)</script>'+String.raw`\(\href{javascript:alert(1)}{x}\)`);
  if(unsafe.querySelector('script,[onerror]'))throw Error('Saneamento falhou');checks++;
  status.textContent=checks+' verificações DOM aprovadas. Exemplo a 360 px abaixo.';
  preview.append(renderMarkdown(response));
} catch(error){status.textContent='FALHA: '+error.message;}
'''
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        rel=unquote(urlsplit(self.path).path).lstrip('/') or 'index.html'
        if rel.startswith(('api/','health','v1/')):
            self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(b'{}');return
        candidate=(STAGE/rel) if (STAGE/rel).is_file() else (ROOT/rel)
        if not candidate.resolve().is_relative_to(ROOT) and not candidate.resolve().is_relative_to(STAGE):self.send_error(403);return
        if '.bak_' in rel or candidate.suffix not in {'.html','.js','.css','.png','.svg','.woff','.woff2','.ttf','.ico'} or not candidate.is_file():self.send_error(404);return
        raw=candidate.read_bytes()
        if rel=='iald.js':raw+=EXTRA.encode()
        self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(rel)[0] or 'application/octet-stream');self.end_headers();self.wfile.write(raw)
    def log_message(self,*_):pass
if __name__=='__main__':
    print('Fixture http://127.0.0.1:8796/?demo=1',flush=True)
    ThreadingHTTPServer(('127.0.0.1',8796),Handler).serve_forever()
