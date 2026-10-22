from pathlib import Path
import os,sys,json,hashlib,sqlite3,ast
from datetime import datetime
W=Path(__file__).parent;R=Path(r'C:\IALD\projetos_pyhton\IALD');S=W/'stage'
sha=lambda x:hashlib.sha256(x).hexdigest()
def atomic(p,raw):
 t=p.with_name(p.name+'.tmp_'+str(os.getpid()));t.write_bytes(raw);assert t.read_bytes()==raw and raw;os.replace(t,p);assert p.read_bytes()==raw
def quiet():
 p=R/'.iald_runtime/chat_jobs/jobs.sqlite3'
 with sqlite3.connect(p.as_uri()+'?mode=ro',uri=True) as db:n=db.execute("SELECT count(*) FROM jobs WHERE status IN ('queued','running')").fetchone()[0]
 assert not n,'Active chat work'
 for p in [*R.glob('*.reservas.sqlite3'),R/'.iald_runtime/app_evaluation/public_spend.sqlite3']:
  if p.is_file():
   with sqlite3.connect(p.as_uri()+'?mode=ro',uri=True) as db:n=db.execute("SELECT count(*) FROM calls WHERE status='reserved'").fetchone()[0]
   assert not n,'Active reservation'
 return {'jobs':0,'reservations':0}
def deploy():
 assert not (W/'deployment.json').exists()
 checks=json.loads((W/'checks.json').read_bytes());assert checks['passed']
 assert (W/'review_closed.txt').exists(),'Closed review required'
 baseline=json.loads((W/'baseline.json').read_bytes());payload={};old={}
 for name,digest in baseline.items():
  before=(R/name).read_bytes();assert sha(before)==digest,('Concurrent edit',name)
  raw=(S/name).read_bytes()
  if name.endswith('.py'):
   assert sha(raw)==checks['sha256'][Path(name).name];ast.parse(raw)
  if raw!=before:payload[name]=raw;old[name]=before
 state=quiet();stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');backups={};written=[]
 scientific={n:sha((R/n).read_bytes()) for n in ['iald_nucleo_fixo.json','IALD_Kernel_v5.txt','.iald_runtime/haiku/prefix.md','.iald_runtime/haiku/manifest.json']}
 users=sha((R/'iald_users.json').read_bytes())
 backupdir=W/'backups'/('web_'+stamp);backupdir.mkdir(parents=True)
 for name,raw in old.items():
  p=R/name
  b=(backupdir/name.replace('/','__')) if name.startswith('app/') else p.with_name(p.name+'.bak_'+stamp)
  atomic(b,raw);backups[name]=str(b)
 try:
  for name,raw in payload.items():
   assert (R/name).read_bytes()==old[name];atomic(R/name,raw);written.append(name)
 except BaseException:
  for name in reversed(written):
   if (R/name).read_bytes()==payload[name]:atomic(R/name,old[name])
  raise
 receipt={'at':datetime.now().astimezone().isoformat(),'files':{n:sha(b) for n,b in payload.items()},'backups':backups,'activity':state,'scientific_unchanged':scientific,'users_sha_before':users,'status':'INSTALLED_RESTART_REQUIRED','remote_test_calls':0}
 atomic(W/'deployment.json',json.dumps(receipt,indent=2).encode());print(json.dumps({'installed':list(payload),'scientific_release':'preserved'}))
if __name__=='__main__':
 if sys.argv[1]=='quiet':print(json.dumps(quiet()))
 elif sys.argv[1]=='deploy':deploy()
