"""Bounded local observation of one authorized video job. No model calls/retries."""
from pathlib import Path
import hashlib,json,sqlite3,time
import capture_manual_audio as cap
W=Path(__file__).resolve().parent
job='e89e858e-da86-4de0-b481-b3adcd9ab413';conversation='c_mvh8m9ahjiqg'
cap.JOBS={'MANUAL_VIDEO':(job,conversation)}
start=time.monotonic();deadline=start+50
while True:
 with cap.connect(cap.R/'.iald_runtime/chat_jobs/jobs.sqlite3') as db:
  row=dict(db.execute('SELECT id,owner,conversation_id,status,seq,created,updated,error FROM jobs WHERE id=?',(job,)).fetchone())
 assert row.pop('owner')==cap.digest(b'iald-chat-job:luiz') and row['conversation_id']==conversation
 if row['status'] in ('completed','failed','cancelled','interrupted'):break
 remaining=deadline-time.monotonic()
 if remaining<=0:break
 time.sleep(min(5,remaining))
if row['status'] not in ('completed','failed','cancelled','interrupted'):
 result={'status':'PENDING_AT_BOUNDED_OBSERVATION','job':row,'owner_verified':'luiz','elapsed_seconds':time.monotonic()-start,'remote_calls':0,'retry':False,'financial_changes':False}
 target=W/'MANUAL_VIDEO_PENDING_R1.json'
else:
 result=cap.capture('MANUAL_VIDEO')
 with cap.connect(cap.R/'.iald_runtime/monthly_wallet/wallet.sqlite3') as db:
  ledger={table:[dict(r) for r in db.execute('SELECT * FROM '+table+' WHERE task_id=?',(job,))] for table in ('tasks','calls','entries')}
 with cap.connect(cap.M/'memory.sqlite3') as db:
  principal=json.loads(db.execute('SELECT scope_json FROM contexts WHERE context_id=?',(result['acom']['context_id'],)).fetchone()['scope_json'])['principal']
 assert ledger['tasks'] and all(r['owner']==principal for records in ledger.values() for r in records)
 result['ledger']=ledger
 result['ledger_cost_usd']=-sum(r['delta'] for r in ledger['entries'] if r['kind']=='cost')/1e9
 result['ledger_matches_metric_cost']=abs(result['ledger_cost_usd']-result['known_cost_estimate_usd'])<1e-10
 result['lifecycle_statuses']={'job':row['status'],'wallet_tasks':[r['status'] for r in ledger['tasks']]}
 result['financial_changes']=False
 original=W/'MANUAL_VIDEO_RESULT_CAPTURE_ORIGINAL.json'
 with original.open('xb') as f:f.write((W/'MANUAL_VIDEO_RESULT.json').read_bytes())
 target=W/'MANUAL_VIDEO_RESULT_ENRICHED.tmp'
 with target.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
 target.replace(W/'MANUAL_VIDEO_RESULT.json');target=None
if target is not None:
 with target.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps({'status':result['status'],'job_status':row['status'],'seq':row['seq'],'text':result.get('text'),'cost_usd':result.get('known_cost_estimate_usd'),'lifecycle':result.get('lifecycle_statuses'),'elapsed_seconds':time.monotonic()-start},ensure_ascii=False))
