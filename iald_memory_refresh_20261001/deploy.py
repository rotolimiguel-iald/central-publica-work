"""Prepare measured compact memory; activate server files together with byte backups."""
from pathlib import Path
from datetime import datetime
import sys,os,json,hashlib,sqlite3,ast
W=Path(__file__).resolve().parent;R=Path(r'C:\IALD\projetos_pyhton\IALD');S=W/'native_release_patch';sys.path[:0]=[str(S),str(R)]
sha=lambda b:hashlib.sha256(b).hexdigest()
def atomic(p,b):
 p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp_'+str(os.getpid()))
 with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==b and b;os.replace(t,p);assert p.read_bytes()==b

def quiet():
 p=R/'.iald_runtime/chat_jobs/jobs.sqlite3';assert p.is_file()
 with sqlite3.connect(p.as_uri()+'?mode=ro',uri=True) as db:active=db.execute("SELECT count(*) FROM jobs WHERE status IN ('queued','running')").fetchone()[0]
 assert active==0,'Active chat work'
 for p in list(R.glob('*.reservas.sqlite3'))+[R/'.iald_runtime/app_evaluation/public_spend.sqlite3']:
  if not p.is_file():continue
  with sqlite3.connect(p.as_uri()+'?mode=ro',uri=True) as db:n=db.execute("SELECT count(*) FROM calls WHERE status='reserved'").fetchone()[0]
  assert n==0,'Active reservation'
 return {'active_jobs':active,'active_reservations':0}

def prepare(receipt_path):
 from iald_release_binding import load_release
 from claude_memory_package import load_package
 count=json.loads(Path(receipt_path).read_bytes());budget=count['budget'];assert budget['ready'] and budget['remaining_tokens']>=10000 and budget['permanent_tokens']>=180000
 prefix=Path(count['draft_path']).read_bytes();assert sha(prefix)==count['draft_sha256'];release=load_release(W/'manifest_install.json')
 assert count['source_sha256']==release.identity['source_sha256'] and count['cluster_sha256']==release.identity['cluster_sha256']
 manifest={'schema':'iald.claude.memory.v1','status':'MEASURED_READY','model':count['model'],'prefix_file':'prefix.md','prefix_sha256':sha(prefix),'budget':budget,'tools_sha256':count['native_tools_sha256'],'measurement_receipt':str(Path(receipt_path).resolve()),'source_draft':Path(count['draft_path']).name,'scope':count['scope'],'deployment':release.identity}
 dest=W/'haiku_runtime'
 for n,b in [('prefix.md',prefix),('manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2).encode())]:
  p=dest/n
  if p.exists() and p.read_bytes()!=b:
   backup=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'));atomic(backup,p.read_bytes());atomic(p,b)
  elif not p.exists():atomic(p,b)
 package=load_package(dest,canonical_manifest=W/'manifest_install.json',source_sha=release.identity['source_sha256']);assert package.prefix.encode()==prefix
 print(json.dumps({'package':'READY_NOT_ACTIVATED','deployment':release.identity,'budget':budget}))

def activate():
 assert not (W/'deployment.json').exists(),'Already deployed'
 assert json.loads((W/'audit_staging.json').read_bytes())['status']=='PASS'
 checks=json.loads((W/'checks_final.json').read_bytes());assert checks['passed']
 prep=json.loads((W/'prepared.json').read_bytes());assert sha((R/'iald_nucleo_fixo.json').read_bytes())==prep['source_manifest_sha256']
 names=checks['code_files'];payload={};old={}
 for name,digest in names.items():
  source=S/name;raw=source.read_bytes();assert sha(raw)==digest;ast.parse(raw);payload[name]=raw
  original=R/name;base=S/'baseline'/name
  if base.exists():assert original.read_bytes()==base.read_bytes();old[name]=original.read_bytes()
  else:assert not original.exists();old[name]=None
 payload['.iald_runtime/haiku/prefix.md']=(W/'haiku_runtime/prefix.md').read_bytes();payload['.iald_runtime/haiku/manifest.json']=(W/'haiku_runtime/manifest.json').read_bytes();payload['iald_nucleo_fixo.json']=(W/'manifest_install.json').read_bytes()
 for n in payload:
  if n not in old:old[n]=(R/n).read_bytes()
 state=quiet();stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');backups={};written=[]
 try:
  for n,b in old.items():
   if b is not None:
    p=R/n;assert p.read_bytes()==b;bak=p.with_name(p.name+'.bak_'+stamp);atomic(bak,b);backups[n]=str(bak)
  for n,b in payload.items():
   p=R/n;assert (p.read_bytes() if p.exists() else None)==old[n];atomic(p,b);written.append(n)
 except BaseException:
  for n in reversed(written):
   if old[n] is not None and (R/n).read_bytes()==payload[n]:atomic(R/n,old[n])
  raise
 report={'installed_at':datetime.now().astimezone().isoformat(),'release':prep['release'],'source_sha256':prep['source_sha256'],'commit':prep['commit'],'files':{n:sha(b) for n,b in payload.items()},'backups':backups,'activity':state,'client_changes':False,'status':'INSTALLED_RESTART_REQUIRED'};atomic(W/'deployment.json',json.dumps(report,ensure_ascii=False,indent=2).encode());print(json.dumps({k:report[k] for k in ('release','status','client_changes')}))
if __name__=='__main__':
 if sys.argv[1]=='prepare':prepare(sys.argv[2])
 elif sys.argv[1]=='activate':activate()
 elif sys.argv[1]=='quiet':print(json.dumps(quiet()))
 else:raise ValueError('Unknown action')
