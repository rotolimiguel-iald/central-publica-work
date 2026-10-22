"""One fresh audited process for the two specifically authorized R3 units."""
from pathlib import Path
import sys,os,json,hashlib,marshal,inspect,subprocess,time
ROOT=Path(r'C:\IALD\Central de Patentes')
BASE=ROOT/'Chatgpt/IALD_ORQUESTRACAO_20260923'
OUT=ROOT/'work/rede_transport_20261014_R3'
sys.path.insert(0,str(BASE))
from iald_orchestrator.worker_identity import require_expected_identity
identity=require_expected_identity()
from iald_orchestrator.coordination import Coordination
from iald_orchestrator.process_lock import process_lock
from iald_orchestrator import mimo,deepseek
from iald_orchestrator.safe_files import utc_now
def new(name,value):
 p=OUT/(name+'.json')
 raw=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
 tmp=p.with_name(p.name+'.tmp_'+str(os.getpid()))
 with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert tmp.read_bytes()==raw
 os.rename(tmp,p)
pre=json.loads((OUT/'PREFLIGHT.json').read_bytes())
assert hashlib.sha256(Path(pre['authorization']['path']).read_bytes()).hexdigest()==pre['authorization']['sha256']
c=Coordination()
with c.runtime.db() as db:
 assert db.execute("select count(*) from tasks where status in ('queued','running')").fetchone()[0]==0
 assert db.execute("select count(*) from coordination_jobs where stage not in ('completed','failed','cancelled')").fetchone()[0]<=5
with process_lock(c.runtime.db_path,blocking=False) as idle:assert idle,'Existing worker drain active'
process_start=subprocess.check_output(['powershell','-NoProfile','-Command',f"(Get-Process -Id {os.getpid()}).StartTime.ToUniversalTime().ToString('o')"],text=True,creationflags=subprocess.CREATE_NO_WINDOW).strip()
for item in pre['units']:
 j=c.get(item['job_id'])
 assert j['request_id']==item['request_id'] and j['stage']=='awaiting_dispatch' and j['execution_task_id'] is None
 assert hashlib.sha256(j['prompt'].encode()).hexdigest()==item['prompt_sha256']
 assert j['execution_constraints']==item['constraints']
 assert j['canonical_memory']['receipt']['generation']==pre['generation']
 preview=c.runtime.preview(j['prompt'],j['execution_constraints'],memory_context_id=j['memory_context_id'])
 assert preview['selected']==item['provider']
 mod={'mimo':mimo,'deepseek':deepseek}[item['provider']]
 original=mod.execute
 loaded={'module_path':str(Path(mod.__file__).resolve()),'adapter_source_sha256':hashlib.sha256(Path(mod.__file__).read_bytes()).hexdigest(),'execute_code_fingerprint':hashlib.sha256(marshal.dumps(original.__code__)).hexdigest(),'execute_source_sha256':hashlib.sha256(inspect.getsource(original).encode()).hexdigest(),'model':mod.MODEL}
 proof={'at':utc_now(),'identity':identity,'process_started_at':process_start,'loaded_adapter':loaded,'job_id':j['id'],'request_id':j['request_id'],'provider':item['provider'],'canonical_generation':pre['generation'],'authorization':pre['authorization'],'scope':'Specific human approval; one call per unit; fresh audited MiMo process; no retry'}
 new(item['job_id']+'_worker_proof',proof)
 def make_wrapper(original,loaded,proof,item):
  def audited(prompt,**kwargs):
   assert os.getpid()==identity['pid']
   require_expected_identity()
   live=c.get(item['job_id'])
   assert live['stage']=='execution_waiting' and live['execution_task_id']
   task=live['execution']
   assert task['status']=='running' and task['decision']['selected']==item['provider']
   assert task['effective_execution_constraints']==item['constraints']
   assert hashlib.sha256(marshal.dumps(original.__code__)).hexdigest()==loaded['execute_code_fingerprint']
   new(item['job_id']+'_provider_entry',{**proof,'entered_at':utc_now(),'execution_task_id':live['execution_task_id'],'wire_prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'wire_prompt_bytes':len(prompt.encode()),'max_output':kwargs.get('max_output')})
   return original(prompt,**kwargs)
  return audited
 mod.execute=make_wrapper(original,loaded,proof,item)
new('EXECUTION_INTENT',{'at':utc_now(),'identity':identity,'units':pre['units'],'authorization':pre['authorization'],'no_retry':True})
for item in pre['units']:
 j=c.act(item['job_id'],'prepare_without_work',{'reason':'assistance_not_needed'})
 assert j['stage']=='prompt_ready'
 j=c.act(item['job_id'],'execute')
 assert j['stage']=='execution_waiting'
 print(json.dumps({'job_id':j['id'],'provider':item['provider'],'stage':j['stage'],'execution_task_id':j['execution_task_id'],'pid':os.getpid()}),flush=True)
while True:
 jobs=[c.get(item['job_id']) for item in pre['units']]
 if all((j.get('execution') or {}).get('status') not in ('queued','running') for j in jobs) and not c.runtime.worker_lock.locked():break
 time.sleep(1)
for item in pre['units']:
 j=c.act(item['job_id'],'sync_execution')
 if j['stage']=='synthesis_ready':
  j=c.act(item['job_id'],'complete_without_work',{'reason':'assistance_not_needed'})
 result=(j.get('execution') or {}).get('result') or {}
 outcome={'at':utc_now(),'job_id':j['id'],'request_id':j['request_id'],'provider':item['provider'],'stage':j['stage'],'execution_task_id':j.get('execution_task_id'),'execution_status':(j.get('execution') or {}).get('status'),'error':j.get('error'),'result_chars':len(result.get('text') or ''),'usage':result.get('usage'),'generation':(result.get('canonical_memory') or {}).get('generation'),'work_used':False,'scientific_statute':'DECLARADO; no independent scientific validation','provider_entry_measured':(OUT/(item['job_id']+'_provider_entry.json')).exists()}
 new(item['job_id']+'_outcome',outcome)
 print(json.dumps(outcome,ensure_ascii=False),flush=True)
