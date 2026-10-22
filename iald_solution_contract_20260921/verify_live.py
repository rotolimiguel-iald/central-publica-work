"""Check installed context and shared backend without any inference or external API call."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import sys
import requests
APP=Path(r'C:\IALD\projetos_pyhton\IALD');WORK=Path(__file__).resolve().parent
sys.path.insert(0,str(APP))
os.environ['TIKTOKEN_CACHE_DIR']=str(APP/'.iald_runtime/tokenizer_cache')
from iald_kernel import KernelCatalog
from iald_memoria_canonica import CanonicalMemory
from iald_response_contract import SOLUTION_PROTOCOL
manifest=json.loads((APP/'iald_nucleo_fixo.json').read_bytes());cfg=manifest['active_cluster']
catalog=KernelCatalog(cfg['kernel_bundle'],cfg['kernel_verification'])
memory=CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',
                       nucleus_manifest=APP/'iald_nucleo_fixo.json')
contexts={}
for public in (True,False):
    body,meta=memory.prompt('',catalog,public=public)
    assert meta['deployed_release']=='v368' and SOLUTION_PROTOCOL in body
    assert meta['cluster_always_present'] and meta['published_evidence_checked']
    contexts['public' if public else 'operator']={key:meta.get(key) for key in
        ('context_tokens','deployed_release','working_index_release','private_atlas_included','cluster_always_present')}
credential=json.loads(Path(r'C:\Users\rotol\.iald_keys\apple-beta\review-account.json').read_bytes())
session=requests.Session();session.trust_env=False
login=session.post('http://127.0.0.1:8082/api/entrar/senha',
    json={'usuario':credential['username'],'senha':credential['password']},timeout=20)
assert login.status_code==200
session.headers['Authorization']='Bearer '+login.json()['token']
response=session.get('http://127.0.0.1:8082/api/motor',timeout=60)
assert response.status_code==200
info=response.json()
assert info['disponivel'] and info['modelo']=='gpt-5.6-luna'
assert not any(x.startswith('iald_atlas_') for x in info['limites']['ferramentas'])
surfaces={}
for rel in ('app/iald.js','iald-app/www/iald.js','iald-app/ios/App/App/public/iald.js',
            'iald-app/android/app/src/main/assets/public/iald.js'):
    path=APP/rel
    if path.exists():
        raw=path.read_bytes()
        assert b'https://demo.iald.ia.br' in raw
        surfaces[rel]={'shared_backend':'https://demo.iald.ia.br','sha256':hashlib.sha256(raw).hexdigest()}
report={'at':datetime.now().astimezone().isoformat(),'model_available':True,'model':info['modelo'],
        'contexts':contexts,'api_motor_http':response.status_code,'inference_called':False,
        'surfaces':surfaces,'testflight_last_verified':'4.1 (17) Em testes, interno e externo, 21/09/2026',
        'android_last_known':'build 16; Google Play pendente de cadastro DUNS',
        'physical_device_tested':False,'new_binary_required_for_this_server_change':False}
with (WORK/'runtime_live.json').open('xb') as out:out.write(json.dumps(report,indent=2).encode())
print(json.dumps(report))
