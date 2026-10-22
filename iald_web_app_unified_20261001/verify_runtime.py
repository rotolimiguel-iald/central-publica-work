from pathlib import Path
from datetime import datetime
import hashlib,json,urllib.request
W=Path(__file__).parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
d=json.loads((W/'deployment.json').read_bytes());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert all(sha(R/n)==h for n,h in d['installed'].items())
assert all(sha(R/n)==h for n,h in d['preserved_sha256'].items())
with urllib.request.urlopen('http://127.0.0.1:8082/health',timeout=10) as r:assert r.status==200
with urllib.request.urlopen('http://127.0.0.1:8082/manifest.json',timeout=10) as r:
 assert r.status==200 and r.url.endswith('/manifest.json')
 manifest=r.read();assert hashlib.sha256(manifest).hexdigest()==d['installed']['manifest.json']
 assert json.loads(manifest)['start_url']=='/app/index.html'
for path in ('/','/iald_chat.html','/app/index.html'):
 with urllib.request.urlopen('http://127.0.0.1:8082'+path,timeout=10) as r:
  assert r.url=='http://127.0.0.1:8082/login'
result={'at':datetime.now().astimezone().isoformat(),'health':200,'installed_files_match':True,'preserved_files_match':True,'public_manifest_bytes_match':True,'unauthenticated_routes_require_login':True,'remote_authenticated_javascript_hash':'NOT_MEASURED','provider_calls':0}
(W/'runtime.json').write_bytes(json.dumps(result,indent=2).encode());print(json.dumps(result))
