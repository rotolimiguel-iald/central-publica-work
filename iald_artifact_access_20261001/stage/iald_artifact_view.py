"""Private artifact previews. Generated HTML never runs in the app's origin."""
import hashlib
import html
import re
from urllib.parse import urlsplit
from iald_task_artifacts import PUBLIC_BASE_URL, _static_html, MAX_ARTIFACT_BYTES

PRIVATE_HEADERS = {'Cache-Control':'private, no-store','Referrer-Policy':'no-referrer',
                   'X-Content-Type-Options':'nosniff','X-Robots-Tag':'noindex, nofollow'}
PREVIEW_CSP = "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"
PAGE_CSP = "default-src 'none'; style-src 'unsafe-inline'; frame-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"

def _checked_html(path, meta):
    if meta['kind'] != 'website': return None
    raw=path.read_bytes()
    if len(raw)>MAX_ARTIFACT_BYTES or len(raw)!=meta['bytes'] or hashlib.sha256(raw).hexdigest()!=meta['sha256']:
        raise ValueError('Artifact changed during preview')
    # Recheck the static allowlist on every view, not only at creation time.
    # Only this derived preview is normalized; the original download stays intact.
    return _static_html(raw.decode('utf-8')).decode('utf-8')

def describe(store, owner, artifact_id):
    path,meta=store.resolve(owner,artifact_id)
    data={key:meta[key] for key in ('id','kind','filename','bytes','sha256')}
    source=_checked_html(path,meta)
    if source is not None:data['preview_html']=source
    return data

def access(store,owner,artifact_id):
    _,meta=store.resolve(owner,artifact_id)
    url=store.issue_ticket(owner,artifact_id)
    token=url.rsplit('/',1)[-1]
    _,issued=store.resolve_ticket(artifact_id,token)
    return {'id':artifact_id,'download_url':url,
            'preview_url':PUBLIC_BASE_URL+'/task-view/'+artifact_id+'/'+token if meta['kind']=='website' else None,
            'expires_at':issued['expires_at']}

def preview_document(source):
    policy='<meta http-equiv="Content-Security-Policy" content="'+html.escape(PREVIEW_CSP,quote=True)+'">'
    policy+='<meta name="viewport" content="width=device-width,initial-scale=1">'
    policy+='<style>:root{overflow-wrap:anywhere}*,*::before,*::after{box-sizing:border-box}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style>'
    if '<head>' in source:return source.replace('<head>','<head>'+policy,1)
    return '<!doctype html><html><head>'+policy+'</head><body>'+source+'</body></html>'

def ticket_page(store,artifact_id,token):
    path,meta=store.resolve_ticket(artifact_id,token)
    source=_checked_html(path,meta)
    if source is None:raise ValueError('No HTML preview')
    title=html.escape(meta['filename'],quote=True)
    # ID/token already passed the store's strict capability validation.
    download=PUBLIC_BASE_URL+'/task-download/'+artifact_id+'/'+token
    back=PUBLIC_BASE_URL+'/app/index.html?artifact='+artifact_id
    return '''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>'''+title+''' · IALD</title><style>
*{box-sizing:border-box}body{margin:0;font:15px system-ui,sans-serif;background:#10191f;color:#fff}
header{padding:max(16px,env(safe-area-inset-top)) 18px 12px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
strong{flex:1;overflow-wrap:anywhere}a{color:#fff;padding:10px 14px;border:1px solid #6b9299;border-radius:12px;text-decoration:none}
p{margin:0;padding:0 18px 14px;color:#bcd0d6;font-size:13px}iframe{display:block;width:100%;height:calc(100vh - 140px);height:calc(100dvh - 140px);min-height:280px;border:0;background:#fff}
</style></head><body><header><strong>'''+title+'''</strong><a href="'''+html.escape(back,quote=True)+'''">Voltar à IALD</a>
<a href="'''+html.escape(download,quote=True)+'''" rel="noreferrer">Baixar HTML</a></header>
<p>Prévia privada. Se o link expirar, abra o arquivo novamente na IALD.</p>
<iframe title="Prévia da página" sandbox="" referrerpolicy="no-referrer" srcdoc="'''+html.escape(preview_document(source),quote=True)+'''"></iframe></body></html>'''
