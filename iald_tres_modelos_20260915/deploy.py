from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from dotenv import dotenv_values

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
APP = ROOT/'iald-app'
receipt = WORK/'deployment.json'
assert not receipt.exists()
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
baseline = json.loads((WORK/'deployment_baseline.json').read_text())
changes = []
for name, expected in baseline.items():
    path = ROOT/name
    before = path.read_bytes() if path.exists() else None
    assert (hashlib.sha256(before).hexdigest() if before is not None else None) == expected, 'Concurrent edit: '+name
    after = (WORK/'stage'/name).read_bytes()
    if name.endswith('.py'): compile(after,str(path),'exec')
    changes.append((path,before,after))

values = json.loads((WORK/'quota_values.json').read_text())
env_path = ROOT/'.env'
env_before = env_path.read_bytes()
env_values = dotenv_values(env_path)
text = env_before.decode('utf-8')
newline = '\r\n' if b'\r\n' in env_before else '\n'
for key, value in values.items():
    pattern = re.compile(r'^'+re.escape(key)+r'=[^\r\n]*',re.M)
    assert len(pattern.findall(text)) <= 1, 'Duplicate configuration: '+key
    if pattern.search(text): text = pattern.sub(key+'='+value,text)
    else: text = text.rstrip('\r\n')+newline+key+'='+value+newline
env_after = text.encode('utf-8')
changes.append((env_path,env_before,env_after))

def create(path,data,sensitive=False):
    path.parent.mkdir(parents=True,exist_ok=True)
    if sensitive:
        with path.open('xb'): pass
        subprocess.run(['icacls.exe',str(path),'/inheritance:r','/grant:r',os.environ['USERNAME']+':(F)','SYSTEM:(F)'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        with path.open('r+b') as f: f.write(data); f.flush(); os.fsync(f.fileno())
    else:
        with path.open('xb') as f: f.write(data)
    assert path.read_bytes()==data

rows=[]
for path,before,after in changes:
    assert (path.read_bytes() if path.exists() else None)==before,'Concurrent edit before backup: '+path.name
    sensitive=path==env_path
    backup=None
    if before is not None:
        if path.is_relative_to(APP) and path.relative_to(APP).parts[0] in ('www','ios','android'):
            backup=APP/('_backups_'+stamp)/path.relative_to(APP)
        else: backup=path.with_name(path.name+'.bak_'+stamp)
        create(backup,before,sensitive)
    temp=path.with_name(path.name+'.tmp_'+stamp)
    create(temp,after,sensitive)
    assert (path.read_bytes() if path.exists() else None)==before
    os.replace(temp,path)
    assert path.read_bytes()==after
    row={'path':str(path),'backup':str(backup) if backup else None}
    if not sensitive: row['sha256']=hashlib.sha256(after).hexdigest()
    rows.append(row)

new_env=dotenv_values(env_path)
assert {k:v for k,v in new_env.items() if k not in values}=={k:v for k,v in env_values.items() if k not in values}
assert all(new_env[k]==v for k,v in values.items())
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT))
import iald_motores as mt
cfg=mt.carregar_config(lambda key:new_env.get(key,''))
assert cfg.cota_global_usd==3 and cfg.cota_usuario_usd==.6
account=json.loads((ROOT/'iald_users.json').read_bytes())['luiz']
assert mt.config_da_conta(cfg,account).somente_limite_global
report={'status':'INSTALLED_FULL_SUITE_AND_RESTART_PENDING','at':datetime.now().astimezone().isoformat(),
        'files':rows,'nonsecret_env_values':values,'other_env_fields_unchanged':True,
        'account_records_changed':False,'luiz_shares_global_usd_day':3,
        'sol_added':False,'native_model_restarted':False,
        'free_plan_full_nucleus':'OPEN: unchanged free-plan memory protections; no budget/memory exception added'}
create(receipt,json.dumps(report,ensure_ascii=False,indent=2).encode())
print(json.dumps({k:v for k,v in report.items() if k!='files'},ensure_ascii=True))
