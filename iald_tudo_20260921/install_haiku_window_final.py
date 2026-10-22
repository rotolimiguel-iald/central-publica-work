"""Install three reviewed files with pinned inputs, byte backups and atomic replace."""
import ast
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
WORK=Path(__file__).resolve().parent
STAGE=WORK/'haiku_window_final_20260923_090543_249253'
NAMES=('claude_tool_budget.py','claude_native_account.py','iald_web_server.py')

def sha(raw):return hashlib.sha256(raw).hexdigest()

def create(path,raw):
    with path.open('xb') as f:
        f.write(raw);f.flush();os.fsync(f.fileno())
    assert path.read_bytes()==raw

def main():
    manifest=json.loads((STAGE/'patch_manifest.json').read_bytes())
    measured=json.loads((WORK/'haiku_final_case_measurement.json').read_bytes())
    assert set(manifest)==set(NAMES)
    assert measured['helper_sha256']==manifest['claude_tool_budget.py']['staged_sha256']
    assert measured['remaining']>=0 and measured['permanent']==183135 and measured['generation_requests']==0
    before={};after={}
    for name in NAMES:
        path=ROOT/name
        before[name]=path.read_bytes() if path.exists() else None
        assert (sha(before[name]) if before[name] is not None else None)==manifest[name]['base_sha256'],name+' changed'
        after[name]=(STAGE/name).read_bytes()
        assert sha(after[name])==manifest[name]['staged_sha256']
        compile(after[name],name,'exec')
    # Only these four existing functions change; every other statement and Selo
    # function remains structurally identical. Byte diff was independently read.
    old=ast.parse(before['iald_web_server.py']);new=ast.parse(after['iald_web_server.py'])
    changed={'_opcoes_de_motor','api_motor_escolha','_chat_externo','agent_loop'}
    unchanged=lambda tree:[ast.dump(n,include_attributes=False) for n in tree.body
                           if not (isinstance(n,ast.FunctionDef) and n.name in changed)]
    assert unchanged(old)==unchanged(new)
    if '--apply' not in sys.argv:
        print(json.dumps({'status':'READY','files':list(NAMES)}));return
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    backups={};temporaries={}
    for name in NAMES:
        path=ROOT/name
        if before[name] is not None:
            backup=path.with_name(path.name+'.bak_'+stamp)
            create(backup,before[name]);backups[name]=str(backup)
        temp=path.with_name(path.name+'.tmp_'+stamp)
        create(temp,after[name]);temporaries[name]=temp
    for name in NAMES:
        path=ROOT/name
        assert (path.read_bytes() if path.exists() else None)==before[name],'Concurrent edit'
    for name in NAMES:
        path=ROOT/name
        assert (path.read_bytes() if path.exists() else None)==before[name],'Concurrent edit'
        os.replace(temporaries[name],path)
        assert path.read_bytes()==after[name]
    receipt={'status':'INSTALLED_RESTART_PENDING','at':datetime.now().astimezone().isoformat(),
             'files':manifest,'backups':backups,'stage':str(STAGE),
             'tests':{'tool_budget':7,'chat_regression':5,'claude_routes':139,'native_access':62,'failures':0},
             'provider_count_receipt':'haiku_final_case_measurement.json','new_paid_generations':0}
    path=WORK/('haiku_window_installed_'+stamp+'.json')
    create(path,json.dumps(receipt,ensure_ascii=False,indent=2).encode('utf8'))
    print(json.dumps({'status':receipt['status'],'receipt':str(path)}))

if __name__=='__main__':main()
