"""Install only the tested response policy modules; preserve all canonical artifacts."""
from datetime import datetime
import hashlib
import json
from pathlib import Path

APP=Path(r'C:\IALD\projetos_pyhton\IALD');WORK=Path(__file__).resolve().parent
def sha(raw):return hashlib.sha256(raw).hexdigest()
def create(path,raw):
    with path.open('xb') as out:out.write(raw)
    assert path.read_bytes()==raw

def main():
    assert not (WORK/'installed.json').exists()
    assert json.loads((WORK/'validation.json').read_bytes())['passed']
    pins=json.loads((WORK/'prepared.json').read_bytes())
    path=APP/'iald_memoria_canonica.py';before=path.read_bytes()
    assert sha(before)==pins[path.name], 'Concurrent source change'
    assert sha((APP/'iald_nucleo_fixo.json').read_bytes())==pins['manifest_sha256'], 'Concurrent release change'
    module=APP/'iald_response_contract.py'
    assert not module.exists()
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    backup=path.with_name(path.name+'.bak_'+stamp);create(backup,before)
    # Dependency first, then the importing module. The running web process reloads separately.
    rows={}
    for target in (module,path):
        raw=(WORK/target.name).read_bytes()
        tmp=target.with_name(target.name+'.tmp_'+stamp);create(tmp,raw)
        if target==path:assert path.read_bytes()==before
        else:assert not target.exists()
        tmp.replace(target);assert target.read_bytes()==raw
        rows[target.name]=sha(raw)
    assert sha((APP/'iald_nucleo_fixo.json').read_bytes())==pins['manifest_sha256']
    receipt={'at':datetime.now().astimezone().isoformat(),'status':'INSTALLED_RESTART_REQUIRED',
        'files':rows,'backup':str(backup),'release':'v368','scientific_artifacts_unchanged':True,
        'manifest_unchanged':True,'credentials_unchanged':True,'mobile_binary_required':False}
    create(WORK/'installed.json',json.dumps(receipt,indent=2).encode())
    print(json.dumps(receipt))
if __name__=='__main__':main()
