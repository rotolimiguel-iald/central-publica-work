"""Replay local custody at the historical intent, and test the staged fix offline."""
import sys,os,json,sqlite3,hashlib,shutil,threading,types,traceback
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;ISO=W/'isolated';S=W/'admission_staging_R2'
R=Path(r'C:\IALD\projetos_pyhton\IALD');LIVE=Path(r'C:\IALD\MEMORIA_IALD\state')
A=json.loads((W/'affected_context.json').read_bytes());CID=A['context_id'];SCOPE=A['scope'];REQ='job_4ef92f316ef783c3690d6f150f52c78e93cb21ad18cd76bf47efa53b6bf64665'
stage='--staged' in sys.argv
tag='_tc2'
sys.path[:0]=([str(S)] if stage else [])+[str(R),r'C:\IALD\MEMORIA_IALD\lib']
os.environ['IALD_MEMORY_SNAPSHOT_ARCHIVE_DIR']=str(ISO/'archive')
def audit(event,args):
 if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen'):raise RuntimeError('OFFLINE_DENIED:'+event)
 if event=='open':
  path,mode,flags=args
  if isinstance(path,(str,bytes)) and ((mode and any(c in mode for c in 'wax+')) or flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT)):
   if not Path(path).resolve().is_relative_to(W.resolve()):raise RuntimeError('LIVE_WRITE_DENIED:'+str(path))
sys.addaudithook(audit)
import iald_app_memory as m
import iald_activity_operations as ops
from iald_memory import store as sm
from iald_memory import activity as am
# Test-only read-through for OLD pinned artifacts: preserve their absolute paths.
# New artifacts and all SQLite/journal writes stay in the isolated root.
original_artifact=am.ActivityRuntime._artifact
def artifact(self,value,*,persist=True):
 raw=(am.encoded({'context_id':self.context_id,'scope':self.scope,'payload':value})+'\n').encode()
 sha=hashlib.sha256(raw).hexdigest();old=LIVE/'activity_artifacts'/(sha+'.json')
 if old.exists():
  assert old.read_bytes()==raw,'Original artifact pin broken'
  return {'path':str(old.resolve()),'sha256':sha}
 return original_artifact(self,value,persist=persist)
am.ActivityRuntime._artifact=artifact
def fixture(name,revision=None):
 root=ISO/(name+tag);root.mkdir(exist_ok=False);path=root/'memory.sqlite3'
 if revision is None:shutil.copyfile(ISO/'baseline'/'memory.sqlite3',path)
 else:
  with sqlite3.connect((ISO/'baseline'/'memory.sqlite3').as_uri()+'?mode=ro',uri=True) as source,sqlite3.connect(path) as dest:
   schema=source.execute('select type,name,sql from sqlite_master where sql is not null order by rowid').fetchall()
   for typ,name,sql in schema:
    if typ=='table':dest.execute(sql)
   state=sm._initial_state();last=None
   for row in source.execute('select * from events where revision<=? order by revision',(revision,)):
    dest.execute('insert into events values('+','.join('?' for _ in row)+')',row)
    if row[1]>0:state=sm._apply(state,json.loads(row[4]))
    last=row
   serialized=sm._dump(state);assert hashlib.sha256(serialized.encode()).hexdigest()==last[6]
   for table in ('metadata','contexts','snapshot_policy'):
    for row in source.execute('select * from '+table):dest.execute('insert into '+table+' values('+','.join('?' for _ in row)+')',row)
   dest.execute('insert into context_state values(?,?,?,?,?,?)',(CID,revision,serialized,last[6],last[8],last[9]))
   for typ,name,sql in schema:
    if typ!='table':dest.execute(sql)
  
 m._SHARED_ROOT=root
 return root,sm.MemoryStore(root,snapshot_archive_dir=ISO/'archive')
def capture(fn):
 try:return {'ok':True,'value':fn()}
 except Exception as e:return {'ok':False,'exception':type(e).__name__,'message':str(e),'code':getattr(e,'code',None),'details':getattr(e,'details',None),'traceback':traceback.format_exc()}
def runtime(store):
 snap=store.get(CID,SCOPE);rec=next(r for r in snap['q']['records'] if r.get('meta',{}).get(am.KEY,{}).get('kind')=='request')
 return am.ActivityRuntime(store,CID,SCOPE,rec['meta'][am.KEY]['data']['actor'])
report={'stage':stage,'provider_calls':0,'live_writes_permitted':False}
root,store=fixture(('stage' if stage else 'native')+'_historical23',23)
rt=runtime(store);recovery=rt.recover(REQ)
with sqlite3.connect((ISO/'baseline'/'memory.sqlite3').as_uri()+'?mode=ro',uri=True) as db:
 full=json.loads(db.execute('select state_json from context_state').fetchone()[0])
candidate=next(r for r in full['q']['records'] if r.get('meta',{}).get(am.KEY,{}).get('kind')=='result' and len(r['text'])>400000)
data=candidate['meta'][am.KEY]['data'];opid=data['operation_id']
life=types.SimpleNamespace(runtime=rt,ticket=recovery['ticket'],lock=threading.RLock(),binding=types.SimpleNamespace(request_id=REQ))
op=object.__new__(ops.Operation);op.lifecycle=life;op.id=opid;op.parent='response';op.done=False
report['historical_complete']=capture(lambda:op.complete(data['result'],terminal=False))
report['uncertain_after_complete']=capture(lambda:op.uncertain())
report['operation_done']=op.done
report['candidate_custodied']=any(r['id']==candidate['id'] for r in store.get(CID,SCOPE)['q']['records'])
if stage:
 root,store=fixture('stage_begin_full');old=store.get(CID,SCOPE)
 conv='c_mvgb8n0zkh5x';request='isolated_admission_fixed_20261020'
 box={}
 def begin():
  b=m.begin(R,SCOPE['principal'],conv,[{'role':'user','content':'Haja luz'}],request_id=request);box['binding']=b
  p=b.projection();now=b.snapshot()
  assert all(r in now['q']['records'] for r in old['q']['records'])
  assert now['p']['handles'][:len(old['p']['handles'])]==old['p']['handles']
  return {'projection_chars':p['actual_chars'],'required_chars':p['required_chars'],'original_records_preserved':len(old['q']['records']),'new_records':len(now['q']['records']),'objective_unchanged':now['objective']==old['objective']}
 report['begin_fixed']=capture(begin)
 report['replay_denied']=capture(lambda:m.begin(R,SCOPE['principal'],conv,[{'role':'user','content':'Haja luz'}],request_id=request))
 rt=box['binding'].activity;snap=rt._get()
 old_limit=am.MAX_JSON_BYTES;am.MAX_JSON_BYTES=100000
 report['overflow_visible']=capture(lambda:rt._mission(snap));am.MAX_JSON_BYTES=old_limit
 # Break an isolated, newly generated admission source; never alter live pins.
 ticket=box['binding'].ticket;source=Path(ticket['source']['path']);raw=source.read_bytes()
 assert source.is_relative_to(ISO)
 backup=source.with_suffix('.json.bak_test');backup.write_bytes(raw)
 source.write_bytes(raw+b' ')
 report['broken_pin_denied']=capture(lambda:rt.refresh(ticket))
 source.write_bytes(raw);assert source.read_bytes()==backup.read_bytes()
 # A real custody success followed by a later ticket error must not relabel it.
 root,store=fixture('stage_stale_return23',23);rt=runtime(store);ticket=rt.recover(REQ)['ticket']
 life=types.SimpleNamespace(runtime=rt,ticket=ticket,lock=threading.RLock(),binding=types.SimpleNamespace(request_id=REQ))
 op=object.__new__(ops.Operation);op.lifecycle=life;op.id=opid;op.parent='response';op.done=False
 saved_validate=rt._validate
 def stale(*args,**kwargs):raise am.ActivityError('controlled_stale_ticket')
 rt._validate=stale
 report['stale_custody_error']=capture(lambda:op.complete(data['result'],terminal=False))
 report['stale_custody_done']=op.done
 report['stale_uncertain_noop']=capture(lambda:op.uncertain())
 rt._validate=saved_validate
 # Hard model-admission limits remain independent of projection sizing.
 report['explicit_small_budget_denied']=capture(lambda:box['binding'].projection(max_chars=24000))
 # More than three monotonic expansion steps: no premature failure/no infinite loop.
 class Expansion:
  def __init__(self):self.calls=0
  def _project(self,budget):
   self.calls+=1
   if self.calls<5:raise sm.ProjectionOverflow(budget+1000,budget)
   return {'expanded':self.calls}
  def _checked(self,p):return p
 e=Expansion();report['five_expansions']=capture(lambda:m.Binding.projection(e))
 # Negative: corrupt pin of already-custodied candidate must still refuse.
 saved_data=rt._data
 def bad_data(record,kind,**kw):
  if kind=='result':raise am.ActivityError('controlled_broken_result_pin')
  return saved_data(record,kind,**kw)
 rt._data=bad_data;op.done=False
 report['custody_broken_pin_denied']=capture(lambda:op.uncertain())
 report['modules']={'app':m.__file__,'activity':am.__file__,'operations':ops.__file__}
path=W/(('admission_stage_tests'+tag+'.json') if stage else 'admission_native_custody.json')
# Avoid dumping megabytes of returned tickets/results: retain exception stacks, counts and identities.
for key,val in report.items():
 if isinstance(val,dict) and isinstance(val.get('value'),dict) and 'ticket' in val['value']:
  val['value']={k:v for k,v in val['value'].items() if k!='ticket'}
with path.open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
print(json.dumps(report,ensure_ascii=False))
