from datetime import datetime
import json
from pathlib import Path
import sys
import requests
APP=Path(r'C:\IALD\projetos_pyhton\IALD');WORK=Path(__file__).resolve().parent
sys.path.insert(0,str(APP))
from iald_kernel import KernelCatalog
from iald_memoria_canonica import CanonicalMemory
manifest=json.loads((APP/'iald_nucleo_fixo.json').read_bytes())
cfg=manifest['active_cluster']
catalog=KernelCatalog(cfg['kernel_bundle'],cfg['kernel_verification'])
memory=CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=APP/'iald_nucleo_fixo.json')
_,meta=memory.prompt('',catalog,public=True)
credential=json.loads(Path(r'C:\Users\rotol\.iald_keys\apple-beta\review-account.json').read_bytes())
session=requests.Session();session.trust_env=False
login=session.post('http://127.0.0.1:8082/api/entrar/senha',json={'usuario':credential['username'],'senha':credential['password']},timeout=20)
assert login.status_code==200
session.headers['Authorization']='Bearer '+login.json()['token']
response=session.get('http://127.0.0.1:8082/api/motor',timeout=60)
assert response.status_code==200
info=response.json()
assert info['disponivel'],info.get('indisponivel')
assert info['modelo']=='gpt-5.6-luna'
assert not any(x.startswith('iald_atlas_') for x in info['limites']['ferramentas'])
assert meta['cluster_always_present'] and meta['published_evidence_checked']
report={'at':datetime.now().astimezone().isoformat(),'model_available':True,'model':info['modelo'],
        'release':cfg['release'],'public_context_tokens':meta['context_tokens'],
        'private_atlas_included':meta['private_atlas_included'],'kernel_files':len(catalog.records),
        'commit':cfg['commit'],'api_motor_http':response.status_code,'inference_called':False}
(WORK/'runtime_live.json').write_bytes(json.dumps(report,indent=2).encode())
print(json.dumps(report))
