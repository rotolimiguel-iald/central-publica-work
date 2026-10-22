from datetime import datetime
import hashlib,json,re
from pathlib import Path
import sys
WORK=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT))
from iald_kernel import KernelCatalog
from iald_memoria_canonica import CanonicalMemory
source=json.loads((WORK/'source_inspection.json').read_bytes())
assert json.loads((WORK/'suite_gate.json').read_bytes())['passed']
installed=json.loads((WORK/'code_installed.json').read_bytes())
for row in installed['files']:
    assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256'],'Concurrent code change'
target=ROOT/'iald_nucleo_fixo.json'
before=target.read_bytes()
assert hashlib.sha256(before).hexdigest()==source['baseline'][target.name]
catalog=KernelCatalog(ROOT/'.iald_runtime'/('kernel-'+source['kernel']['source_sha256']))
_,info=CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=WORK/'iald_nucleo_fixo.json').prompt('',catalog)
assert info['context_tokens']+32000<480000 and info['published_evidence_checked']
envpath=ROOT/'.env'
envbefore=envpath.read_bytes()
pattern=rb'(?m)^(IALD_OPENAI_JANELA\s*=\s*)400000(\s*\r?)$'
envafter,count=re.subn(pattern,lambda m:m[1]+b'480000'+m[2],envbefore)
assert count==1,'Context window changed or absent'
assert envafter.replace(b'IALD_OPENAI_JANELA=480000',b'IALD_OPENAI_JANELA=400000')==envbefore,'Unexpected env delta'
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def create(path,data):
    with path.open('xb') as f:f.write(data)
    assert path.read_bytes()==data
rows=[]
for path,old,new in [(envpath,envbefore,envafter),(target,before,(WORK/'iald_nucleo_fixo.json').read_bytes())]:
    backup=path.with_name(path.name+'.bak_'+stamp);create(backup,old)
    tmp=path.with_name(path.name+'.tmp_'+stamp);create(tmp,new)
    assert path.read_bytes()==old,'Concurrent configuration change'
    tmp.replace(path);assert path.read_bytes()==new
    row={'path':str(path),'backup':str(backup)}
    if path.name!='.env':row['sha256']=hashlib.sha256(new).hexdigest()
    rows.append(row)
report={'at':datetime.now().astimezone().isoformat(),'status':'CONFIG_INSTALLED_RESTART_PENDING','files':rows,
    'window_before':400000,'window_after':480000,'other_env_fields_changed':False,'nucleus':info}
create(WORK/'activation.json',json.dumps(report,ensure_ascii=False,indent=2).encode())
print(json.dumps({'window':480000,'context_tokens':info['context_tokens'],'evidence_checked':True,'restart_pending':True}))
