"""Verify existing hidden updater process and its observed installed identity."""
from pathlib import Path
import hashlib,json,time,psutil
A=Path(__file__).resolve().parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
runner=R/'canonical_releases/v410_608b7108977e/continuous_update/continuous_update_adapter.py'
status=R/'.iald_runtime/science_update/status.json'
for attempt in range(12):
 if status.is_file():break
 time.sleep(5)
state=json.loads(status.read_bytes());active=json.loads((R/'iald_nucleo_fixo.json').read_bytes())['operational_core']
assert state['phase'] in ('CURRENT','ACTIVE'),state.get('phase')
assert state.get('active',{}).get('release')==active['current_release']
assert state['active']['source_sha256']==active['release_source_sha256']
found=[]
for p in psutil.process_iter(['pid','name','cmdline']):
 try:
  if any(str(arg).casefold()==str(runner).casefold() for arg in (p.info['cmdline'] or [])):found.append(p.pid)
 except (psutil.NoSuchProcess,psutil.AccessDenied):pass
assert len(found)==1,found
observation=status.with_name('observation.json')
if observation.exists():assert json.loads(observation.read_bytes()).get('readable') is not False
out={'status':'PASS','worker_pid':found[0],'phase':state['phase'],'active':state['active'],'status_sha256':hashlib.sha256(status.read_bytes()).hexdigest(),'automatic_review_consumer':False,'scope':'One local process and current installed release observed; future candidates require actual distinct review; no generation'}
with (A/'UPDATER_RUNNING_VERIFIED.json').open('xb') as f:f.write(json.dumps(out,indent=2).encode())
print(json.dumps(out))
