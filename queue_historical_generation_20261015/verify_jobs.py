"""Local read-only Coordination.get harness; no constructor, replay or dispatch."""
from pathlib import Path
from contextlib import contextmanager
from unittest.mock import patch
import hashlib,json,sqlite3,sys,uuid,urllib.request
ROOT=Path(__file__).resolve().parent
BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.dont_write_bytecode=True;sys.path.insert(0,str(BASE))
import iald_orchestrator
candidate=sys.argv[1]=='candidate'
if candidate:iald_orchestrator.__path__.insert(0,str(ROOT/'candidate/iald_orchestrator'))
from iald_orchestrator import canonical_memory as m,operational_memory as o,providers
if candidate:
 m.BASE=BASE;m.ACTIVE=BASE/'state/canonical_memory/ACTIVE.json';m.RELEASES=BASE/'state/canonical_memory/releases';m.CATALOG=BASE/'project_fisica/MANIFESTO_LOCAL.json'
from iald_orchestrator.coordination import Coordination
IDS=['67df5266-7d17-4f33-a003-da2494c9bdc2','1e2c2f25-f6bf-4451-aad2-052ba9a1897d','ff9a08c5-5b3a-4b17-b0ea-319d59a978a2']
class ReadOnly:
 state_dir=BASE/'state';memory_root=o.COMMON_STATE
 @contextmanager
 def db(self):
  db=sqlite3.connect((self.state_dir/'tasks.sqlite3').as_uri()+'?mode=ro',uri=True);db.row_factory=sqlite3.Row
  db.execute('PRAGMA query_only=ON')
  try:yield db
  finally:db.close()
runtime=ReadOnly()
def h(b):return hashlib.sha256(b).hexdigest()
def inspect():
 with runtime.db() as db:
  jobs=[dict(db.execute('SELECT * FROM coordination_jobs WHERE id=?',(x,)).fetchone()) for x in IDS]
  attempts=[]
  for x in jobs:
   related=list(db.execute('SELECT id FROM tasks WHERE request_id=? OR memory_context_id=?',(str(uuid.uuid5(uuid.NAMESPACE_URL,'iald-coordination:'+x['id'])),x['memory_context_id'])))
   assert not related,'Existing execution: inspect without repeating'
   assert x['execution_task_id'] is None
  return jobs
def ro_sync(rt,reference):
 # Preserve the actual projection/verification; refuse any replayable outbox.
 with rt.db() as db:
  assert not db.execute('SELECT 1 FROM memory_outbox WHERE context_id=? AND receipt_json IS NULL',(reference,)).fetchone()
 return o.store(rt).get(reference,o.SCOPE)
originals=[BASE/'iald_orchestrator'/x for x in ('canonical_memory.py','nos_packet.py','request_controls.py')]
active=m.ACTIVE.read_bytes();pins={str(p):h(p.read_bytes()) for p in originals};before=inspect()
slots=BASE/'state/handoffs/slot_management.json';slot_before=slots.read_bytes()
def no_remote(*args,**kwargs):raise AssertionError('External execution forbidden by diagnostic')
co=object.__new__(Coordination);co.runtime=runtime
results=[]
with patch.object(o,'sync',side_effect=ro_sync),patch.object(providers,'execute',side_effect=no_remote),patch.object(urllib.request,'urlopen',side_effect=no_remote):
 for row in before:
  brief={'job_id':row['id'],'request_id':row['request_id'],'stage':row['stage'],'version':row['version'],'execution_task_id':row['execution_task_id'],'prompt_sha256':h(row['prompt'].encode()),'constraints_sha256':h((row['execution_constraints'] or 'null').encode()),'original_constraints':json.loads(row['execution_constraints'] or 'null')}
  try:
   value=co.get(row['id']);receipt=value['canonical_memory']['receipt'];brief.update(read_status='RECOVERED',generation_received=receipt['generation'],graph_generation=receipt.get('nos_vivo',{}).get('canonical_memory',{}).get('generation'),context_bytes=receipt['context_bytes'],packet_sha256=receipt['packet_sha256'],memory_mode=receipt['memory_mode'],sources=len(receipt['sources']))
   assert value['prompt']==row['prompt'] and value['execution_constraints']==json.loads(row['execution_constraints'] or 'null')
   expected=(brief['original_constraints'] or {}).get('memory_generation',json.loads(active)['generation'])
   assert receipt['generation']==expected
  except Exception as e:
   brief.update(read_status='REFUSED',error_type=type(e).__name__,error=str(e))
   if candidate:raise
   if row['id']==IDS[-1]:raise
   assert str(e)=='Geração canônica diferente da autorizada no pedido.'
  results.append(brief)
assert inspect()==before
assert m.ACTIVE.read_bytes()==active and slots.read_bytes()==slot_before
assert {str(p):h(p.read_bytes()) for p in originals}==pins
print(json.dumps({'candidate':candidate,'read_only_harness':'Original get method; read-only SQLite; outbox sync replaced ONLY by verified read after asserting no pending outbox, no replay/transitions.','jobs':results,'preserved':{'all_job_fields':True,'active':True,'installed_modules':True,'specific_approval_records':True},'provider_calls':0,'new_executions':0,'deployed':False},ensure_ascii=False))
