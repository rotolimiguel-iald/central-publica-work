from pathlib import Path
from datetime import datetime
import ast,hashlib,json,os,sqlite3,sys
W=Path(__file__).parent;R=Path(r'C:\IALD\projetos_pyhton\IALD');S=W/'stage'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,raw):
 t=p.with_name(p.name+'.tmp_unified_'+str(os.getpid()))
 with t.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==raw and raw
 os.replace(t,p);assert p.read_bytes()==raw
def quiet():
 with sqlite3.connect((R/'.iald_runtime/chat_jobs/jobs.sqlite3').as_uri()+'?mode=ro',uri=True) as db:
  assert db.execute("SELECT count(*) FROM jobs WHERE status IN ('queued','running')").fetchone()[0]==0,'Active chat work'
 for p in [*R.glob('*.reservas.sqlite3'),R/'.iald_runtime/app_evaluation/public_spend.sqlite3']:
  if p.is_file():
   with sqlite3.connect(p.as_uri()+'?mode=ro',uri=True) as db:
    assert db.execute("SELECT count(*) FROM calls WHERE status='reserved'").fetchone()[0]==0,'Active reservation'
 return {'jobs':0,'reservations':0}
def deploy():
 assert not (W/'deployment.json').exists()
 assert (W/'review.txt').is_file()
 checks=json.loads((W/'checks.json').read_bytes());assert checks['passed']
 base=json.loads((W/'baseline.json').read_bytes());assert set(base)=={'iald_web_server.py','manifest.json'}
 old={};new={}
 for n,h in base.items():
  assert sha(R/n)==h,('Concurrent change',n)
  assert sha(S/n)==checks['stage_sha256'][n],('Staged file changed',n)
  old[n]=(R/n).read_bytes();new[n]=(S/n).read_bytes()
 ast.parse(new['iald_web_server.py']);json.loads(new['manifest.json'])
 activity=quiet();stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
 preserve=['iald_users.json','iald_nucleo_fixo.json','IALD_Kernel_v5.txt','.iald_runtime/haiku/prefix.md','.iald_runtime/haiku/manifest.json','app/index.html','app/iald.js','app/iald.css','iald_chat.html']
 pins={n:sha(R/n) for n in preserve};backups={};written=[]
 for n,raw in old.items():
  b=(R/n).with_name(n+'.bak_'+stamp)
  with b.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
  assert b.read_bytes()==raw;backups[n]=str(b)
 try:
  for n,raw in new.items():
   assert (R/n).read_bytes()==old[n];atomic(R/n,raw);written.append(n)
 except BaseException:
  for n in reversed(written):
   if (R/n).read_bytes()==new[n]:atomic(R/n,old[n])
  raise
 assert all(sha(R/n)==h for n,h in pins.items())
 data={'at':datetime.now().astimezone().isoformat(),'installed':{n:sha(R/n) for n in new},'preserved_sha256':pins,'activity':activity,'backups':backups,'restart_required':True,'shared_client_changed':False,'provider_calls':0}
 atomic(W/'deployment.json',json.dumps(data,indent=2).encode());print(json.dumps({'installed':list(new),'preserved':len(pins),'restart_required':True}))
if __name__=='__main__':
 if sys.argv[1]=='quiet':print(json.dumps(quiet()))
 elif sys.argv[1]=='deploy':deploy()
