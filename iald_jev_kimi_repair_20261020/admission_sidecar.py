"""Offline forensic sidecar. Live SQLite connections are mode=ro only."""
import os,sys,json,sqlite3,hashlib,traceback,shutil,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
LIVE=Path(r'C:\IALD\MEMORIA_IALD\state\memory.sqlite3')
ISO=W/'isolated';ISO.mkdir(exist_ok=True)
os.environ['IALD_MEMORY_SNAPSHOT_ARCHIVE_DIR']=str(ISO/'archive')
A=json.loads((W/'affected_context.json').read_bytes());CID=A['context_id'];SCOPE=A['scope']
REQ='job_4ef92f316ef783c3690d6f150f52c78e93cb21ad18cd76bf47efa53b6bf64665'
def save(name,value):
 p=W/name;raw=json.dumps(value,ensure_ascii=False,indent=2).encode()
 with p.open('xb') as f:f.write(raw)
 assert p.read_bytes()==raw
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def clone():
 root=ISO/'baseline';root.mkdir(exist_ok=True);dst=root/'memory.sqlite3'
 with sqlite3.connect(dst.as_uri(),uri=True) as db:
  db.execute('ATTACH DATABASE ? AS live',(LIVE.as_uri()+'?mode=ro',))
  db.execute('BEGIN')
  schema=db.execute("SELECT type,name,sql FROM live.sqlite_master WHERE sql IS NOT NULL ORDER BY rowid").fetchall()
  for typ,name,sql in schema:
   if typ=='table':db.execute(sql)
  counts={}
  for typ,name,sql in schema:
   if typ!='table':continue
   cols=[x[1] for x in db.execute('PRAGMA live.table_info("'+name+'")')]
   if 'context_id' in cols:
    db.execute('INSERT INTO main."'+name+'" SELECT * FROM live."'+name+'" WHERE context_id=?',(CID,))
   elif name in ('metadata','snapshot_policy'):
    db.execute('INSERT INTO main."'+name+'" SELECT * FROM live."'+name+'"')
   else:raise RuntimeError('Unadmitted table '+name)
   counts[name]=db.execute('SELECT count(*) FROM main."'+name+'"').fetchone()[0]
  for typ,name,sql in schema:
   if typ!='table':db.execute(sql)
  assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
  assert db.execute('SELECT context_id FROM main.contexts').fetchall()==[(CID,)]
  db.commit()
 save('isolated/CLONE_RECEIPT.json',{'source_mode':'SQLite ATTACH URI mode=ro; one transaction','tables':counts,'schema':schema,'target':pin(dst),'only_context':CID,'source_paths_preserved':True})
 return root
def deny_network(event,args):
 if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen'):raise RuntimeError('OFFLINE_SIDECAR_DENIED:'+event)
def run():
 baseline=clone()
 jobs=R/'.iald_runtime'/'chat_jobs'/'jobs.sqlite3'
 with sqlite3.connect(jobs.as_uri()+'?mode=ro',uri=True) as db:
  row=db.execute('SELECT id,conversation_id,status FROM jobs WHERE id LIKE ? OR id LIKE ?',('5f073de0%','76315708%')).fetchall()
  if not row:raise RuntimeError('No matching jobs for identity fixture')
 conv=row[0][1]
 assert 'app_'+hashlib.sha256((SCOPE['principal']+':'+conv).encode()).hexdigest()==CID
 sys.addaudithook(deny_network)
 sys.path.insert(0,str(R));import iald_app_memory as m
 from iald_memory import MemoryStore
 from iald_memory.activity import ActivityRuntime,KEY
 from iald_memory import guard
 result={'jobs_metadata':row,'context':CID,'source_module':pin(Path(m.__file__)),'live_database_mutations':False,'provider_calls':0}
 for case in ('begin','complete'):
  root=ISO/('baseline_'+case);root.mkdir();shutil.copyfile(baseline/'memory.sqlite3',root/'memory.sqlite3')
  m._SHARED_ROOT=root
  store=MemoryStore(root,snapshot_archive_dir=ISO/'archive');snap=store.get(CID,SCOPE)
  try:
   if case=='begin':
    b=m.begin(R,SCOPE['principal'],conv,[{'role':'user','content':'Haja luz'}],request_id='isolated_admission_probe_20261020')
    val={'admitted':True,'context_id':b.context_id}
   else:
    rec=next(r for r in snap['q']['records'] if r.get('meta',{}).get(KEY,{}).get('kind')=='request' and r['meta'][KEY]['data']['request_id']==REQ)
    actor=rec['meta'][KEY]['data']['actor'];runtime=ActivityRuntime(store,CID,SCOPE,actor)
    recovery=runtime.recover(REQ)
    partial=[]
    for rec in snap['q']['records']:
     try:v=json.loads(rec['text'])
     except (ValueError,KeyError):continue
     if isinstance(v,dict) and isinstance(v.get('received_text'),str) and len(v['received_text'].encode())>400000:partial.append((rec,v))
    if len(partial)!=1:raise RuntimeError('Expected one preserved large stream: '+str(len(partial)))
    rec,v=partial[0];raw=v['received_text'];guard.assert_clean_text(raw,'sidecar.raw')
    op=next(h for h in recovery['handles'] if h.get('kind')=='activity_operation' and h['status']=='uncertain' and h.get('operation_id')!='response')
    opid=op.get('operation_id')
    result['complete_fixture']={'raw_bytes':len(raw.encode()),'raw_sha256':hashlib.sha256(raw.encode()).hexdigest(),'has_done':'[DONE]' in raw,'guard_pass':True,'operation':op,'partial_record_id':rec['id']}
    val=runtime.complete(recovery['ticket'],opid,{'http_status':200,'response':raw},terminal=False,refresh=True)
   result[case]={'ok':True,'result':val}
  except Exception as e:
   result[case]={'ok':False,'exception':type(e).__name__,'message':str(e),'details':getattr(e,'details',None),'traceback':traceback.format_exc()}
 save('admission_baseline.json',result)
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':run()
