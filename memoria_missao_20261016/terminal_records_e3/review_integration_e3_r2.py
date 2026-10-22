"""Independent E3 integration checks; all writes under this new sandbox."""
from pathlib import Path
import ast,copy,hashlib,importlib.util,json,os,sys,uuid
BASE=Path(__file__).resolve().parent
RUN=BASE/'independent_integration_r2';RUN.mkdir(exist_ok=False)
sys.path.insert(0,r'C:\IALD\MEMORIA_IALD\lib')
from iald_memory import MemoryStore

def pin(p):
 p=Path(p);return {'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def new(p,v):
 raw=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
 temp=p.with_suffix('.tmp')
 with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert temp.read_bytes()==raw
 os.rename(temp,p)

src=BASE/'mission_candidate_r2.py'
spec=importlib.util.spec_from_file_location('iald_memory.independent_r2',src)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
SCOPE={'house':'IALD','principal':'independent-e3-review'}
OWNER={'id':'isolated-author','kind':'agent'}
REVIEWER={'id':'isolated-independent','kind':'agent'}
cid=str(uuid.uuid4());store=MemoryStore(RUN/'state')
store.ensure_context(cid,objective='Keep the original order.\r\nDo not claim science.',scope=SCOPE,actor=OWNER,constraints={'no_repeat':True})
e=RUN/'technical-evidence.txt';e.write_bytes(b'Test fixture; no scientific conclusion.')
ctl=m.MissionController(store,cid,SCOPE)
ctl.action({'operation':'configure','event_id':'configure','actor':OWNER,'expected_revision':0,'requirements':[{'id':'A','criterion':'Preserve actual evidence.','depends_on':[]}],'sources':[pin(e)]})
def trans(changes):return store.transition(cid,SCOPE,store.receipt(cid,SCOPE)['revision'],str(uuid.uuid4()),OWNER,changes)
def req(op,actor=OWNER,**extra):
 p=ctl.project(200000)
 return dict(operation=op,event_id=str(uuid.uuid4()),actor=actor,task_id='A',expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256'],**extra)
def statepins():return {str(p):pin(p)['sha256'] for p in (RUN/'state').rglob('*') if p.is_file()}

stamp='20261016T175000_654321Z';attempt=RUN/stamp;attempt.mkdir()
receipt=attempt/'RECEIPT.json';receipt.write_bytes(b'{"exit_code":0}')
h=dict(id='build-'+stamp,kind='lean_build',task_id='A',status='completed',no_repeat=True,receipt=pin(receipt))
r=dict(id='track-build-'+stamp+'-completed',kind='fact',statute='REAL',text=f'A sandbox build {stamp} completed. Full requirement remains open.',sources=[dict(kind='artifact',ref=str(receipt),sha256=pin(receipt)['sha256'])])
ordinary=[dict(id='operator',kind='decision',statute='INPUT',text='Keep every part of this order.',sources=[{'kind':'artifact','ref':str(e)}]),dict(id='erratum',kind='fact',statute='REAL',text='Correction beside the original. Charge remains open.',sources=[{'kind':'artifact','ref':str(e)}])]
trans({'records':[r]+ordinary,'flow':{'handles':[h]}})
full=store.get(cid,SCOPE);before=statepins();p=ctl.project(200000)
assert p['projection']['current_records']==ordinary
assert p['projection']['terminal_build_records']==[{'id':r['id'],'record_sha256':m.digest(r),'handle_id':h['id'],'record_status':'completed'}]
assert ctl.project(200000)==p and store.get(cid,SCOPE)==full and before==statepins()
recovery=p['projection']['terminal_build_records_recovery']
assert recovery['context_id']==cid and recovery['revision']==full['revision'] and recovery['state_sha256']==full['receipt']['state_sha256']
claim=ctl.action(req('claim'));lease=claim['task']['lease']['id']
check=req('check',lease_id=lease);assert ctl.check(check)['ready']
receipt.write_bytes(b'{"exit_code":1}')
assert r in ctl.project(200000)['projection']['current_records']
try:ctl.check(check);raise AssertionError('stale projection accepted')
except m.MissionError as error:assert 'stale_projection' in str(error)
receipt.write_bytes(b'{"exit_code":0}')
ctl.action(req('submit',lease_id=lease,evidence=[pin(e)]))
try:ctl.action(req('accept',review_evidence=[pin(e)]));raise AssertionError('author accepted own work')
except m.MissionError as error:assert 'reviewer' in str(error) or 'different' in str(error)
ctl.action(req('accept',actor=REVIEWER,review_evidence=[pin(e)]))
assert ctl.project(200000)['projection']['tetelestai']
trans({'flow':{'handles':[h,{'id':'uncertain','status':'dispatch_uncertain','detail':'Keep all fields.','no_repeat':True}]}})
assert not ctl.project(200000)['projection']['tetelestai']
assert ctl.project(200000)['projection']['unresolved_handles'][0]['detail']=='Keep all fields.'
assert store.verify(cid,SCOPE,deep=True)['ok']

baseline=Path(r'C:\IALD\MEMORIA_IALD\lib\iald_memory\mission.py')
def definitions(path):
 t=ast.parse(path.read_text(encoding='utf-8'));out={}
 for x in t.body:
  if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef)):out[x.name]=ast.dump(x,include_attributes=False)
  if isinstance(x,ast.ClassDef):
   for y in x.body:
    if isinstance(y,(ast.FunctionDef,ast.AsyncFunctionDef)):out[x.name+'.'+y.name]=ast.dump(y,include_attributes=False)
 return out
old,newdefs=definitions(baseline),definitions(src)
changed=[k for k in old if old[k]!=newdefs[k]]
added=[k for k in newdefs if k not in old]
assert changed==['MissionController._project']
assert set(added)=={'_legacy_build_receipt','_legacy_terminal_build_records'}
result=dict(ok=True,candidate=pin(src),baseline=pin(baseline),script=pin(Path(__file__)),checks=['exact partition and full-record hash','general order/erratum intact','deterministic project','all persisted file bytes unchanged by project/get','same-reference recovery revision/hash','claim/preflight','changed receipt visible','stale projection refused','author cannot self-accept in protocol','distinct local reviewer field accepted in isolated fixture; not authentication','tetelestai satisfied then blocked by uncertain handle','deep journal verify','AST scope limited'],changed_existing=changed,added=added,real_mission_mutations=0,providers=0)
new(RUN/'RESULTS.json',result)
print(json.dumps({'ok':True,'checks':len(result['checks']),'result':str(RUN/'RESULTS.json')}))
