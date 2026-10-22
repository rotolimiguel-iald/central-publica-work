from datetime import datetime
import hashlib,json
from pathlib import Path
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
WORK=Path(__file__).resolve().parent
baseline=json.loads((WORK/'source_inspection.json').read_bytes())['baseline']
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def create(path,data):
    with path.open('xb') as f:f.write(data)
    assert path.read_bytes()==data
def install(target,data,expected=None):
    old=target.read_bytes() if target.exists() else None
    if expected is not None: assert hashlib.sha256(old).hexdigest()==expected,'Concurrent code change'
    else: assert old is None,'Unexpected existing file'
    backup=None
    if old is not None:
        backup=target.with_name(target.name+'.bak_'+stamp);create(backup,old)
    tmp=target.with_name(target.name+'.tmp_'+stamp);create(tmp,data)
    assert (target.read_bytes() if target.exists() else None)==old
    tmp.replace(target)
    assert target.read_bytes()==data
    return {'path':str(target),'backup':str(backup) if backup else None,'sha256':hashlib.sha256(data).hexdigest()}
rows=[]
for name in ['iald_estado_publicado.py','iald_memoria_canonica.py']:
    data=(WORK/name).read_bytes();compile(data,str(ROOT/name),'exec')
    rows.append(install(ROOT/name,data,baseline.get(name)))
test=(WORK/'test_evidence.py').read_text(encoding='utf-8')
test=test.replace('from iald_estado_publicado import',"import sys\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\nfrom iald_estado_publicado import",1)
rows.append(install(ROOT/'tests/test_published_evidence.py',test.encode()))
create(WORK/'code_installed.json',json.dumps({'at':datetime.now().astimezone().isoformat(),'status':'CODE_ONLY_RESTART_AND_MANIFEST_PENDING','files':rows},ensure_ascii=False,indent=2).encode())
print('Code installed; active process, old manifest and limits unchanged pending regression gate.')
