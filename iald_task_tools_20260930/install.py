"""Install verified staged modules with byte backups and compare-and-swap."""
from pathlib import Path
from datetime import datetime
import hashlib,json,os,sys
W=Path(__file__).parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
digest=lambda b:hashlib.sha256(b).hexdigest()
baseline=json.loads((W/'baseline.json').read_bytes())
if '--update' in sys.argv:
    baseline={Path(r['path']).name:r['sha256'] for r in json.loads((W/'installed.json').read_bytes())}
checks=json.loads((W/'checks.json').read_bytes())
assert checks['passed'] and checks['tests_run']>=120,'Validated complete suite required'
names=['iald_task_policy.py','iald_task_artifacts.py','iald_task_sandbox.py','iald_task_session.py','iald_task_bridge.py','iald_auto_router.py','iald_app_providers.py','iald_motores.py','iald_web_server.py']
pending=[]
for name in names:
    path=ROOT/name;raw=(W/'stage'/name).read_bytes()
    assert digest(raw)==checks['files'][name], 'Stage changed after tests: '+name
    compile(raw,str(path),'exec')
    if name in baseline:
        before=path.read_bytes();assert digest(before)==baseline[name],'Concurrent change: '+name
    else:
        assert not path.exists(),'Unexpected existing module: '+name
        before=None
    pending.append((path,raw,before))
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');records=[]
for path,raw,before in pending:
    backup=None
    if before is not None:
        assert path.read_bytes()==before,'Concurrent edit: '+path.name
        backup=path.with_name(path.name+'.bak_'+stamp);backup.write_bytes(before)
        assert backup.read_bytes()==before
    temp=path.with_name(path.name+'.tmp_'+stamp);temp.write_bytes(raw)
    assert temp.read_bytes()==raw and temp.stat().st_size>0
    os.replace(temp,path);assert path.read_bytes()==raw
    records.append({'path':str(path),'sha256':digest(raw),'backup':str(backup) if backup else None})
(W/'installed.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print(json.dumps({'installed':len(records),'backup_stamp':stamp}))
