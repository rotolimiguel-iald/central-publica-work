"""Readonly terminal failure capture, exact owner/job/conversation; never retries."""
import json,sys
from decimal import Decimal
from pathlib import Path
import capture_manual_audio as c
W=Path(__file__).resolve().parent
jobid='e89e858e-da86-4de0-b481-b3adcd9ab413';conversation='c_mvh8m9ahjiqg'
with c.connect(c.R/'.iald_runtime/chat_jobs/jobs.sqlite3') as db:
 job=dict(db.execute('SELECT id,owner,conversation_id,status,seq,created,updated,error FROM jobs WHERE id=?',(jobid,)).fetchone())
 assert job.pop('owner')==c.digest(b'iald-chat-job:luiz') and job['conversation_id']==conversation and job['status']=='failed'
 events=[];hashes=[]
 for row in db.execute('SELECT seq,data FROM events WHERE job=? ORDER BY seq',(jobid,)):
  raw=c.cipher.open(row['data']);hashes.append(raw);value=raw.decode();events.append({'seq':row['seq'],'value':value if value.strip()=='[DONE]' else json.loads(value)})
with c.connect(c.M/'memory.sqlite3') as db:
 contexts=db.execute('SELECT DISTINCT context_id FROM events WHERE changes_json LIKE ?',('%'+jobid+'%',)).fetchall();assert len(contexts)==1
 context=contexts[0]['context_id'];scope=json.loads(db.execute('SELECT scope_json FROM contexts WHERE context_id=?',(context,)).fetchone()['scope_json'])
 state=db.execute('SELECT * FROM context_state WHERE context_id=?',(context,)).fetchone();assert c.digest(state['state_json'].encode())==state['state_sha256']
 last=db.execute('SELECT revision,state_sha256,event_hash FROM events WHERE context_id=? ORDER BY revision DESC LIMIT 1',(context,)).fetchone()
 assert all(state[k]==last[k] for k in ['revision','state_sha256','event_hash']);snapshot=json.loads(state['state_json'])
with c.connect(c.R/'.iald_runtime/private_media/media.sqlite3') as db:
 generations=db.execute('SELECT DISTINCT generation FROM media WHERE owner=? AND conversation=?',('luiz',conversation)).fetchall()
assert len(generations)==1 and scope=={'house':'IALD_APP','principal':generations[0]['generation']}
request='job_'+c.digest((scope['principal']+':'+jobid).encode());assert context=='app_'+c.digest((scope['principal']+':'+conversation).encode())
handles=[h for h in snapshot['p']['handles'] if h.get('request_id')==request];assert any(h['status']=='uncertain' for h in handles)
custody=[];partials=[];models=set()
for record in snapshot['q']['records']:
 for source in record.get('sources',[]):
  if source.get('kind')=='artifact' and not source['ref'].startswith('acom:'):
   c.checked_artifact(source,context,scope);custody.append({'record_id':record['id'],'ref':source['ref'],'sha256':source['sha256'],'verified':True})
 try:value=json.loads(record.get('text',''))
 except (ValueError,TypeError):continue
 transport=value.get('transport') if isinstance(value,dict) else None
 if not transport:continue
 payload=c.checked_artifact({'ref':transport['ref']['path'],'sha256':transport['ref']['sha256']},context,scope)
 wire=payload['wire_utf8'];assert c.digest(wire.encode())==payload['wire_sha256']==transport['sha256'];assert len(wire.encode())==transport['bytes']
 chunks=[]
 for line in wire.splitlines():
  if line.startswith('data:'):
   try:chunk=json.loads(line[5:].strip())
   except ValueError:continue
   if chunk.get('model'):models.add(chunk['model'])
   # Keep received partial wire locally, including any reasoning, never display it.
   chunks.append({'model':chunk.get('model'),'usage':chunk.get('usage'),'finish_reasons':[x.get('finish_reason') for x in chunk.get('choices',[])]})
 partials.append({'transport':transport,'hash_and_scope_verified':True,'wire_done':'[DONE]' in wire,'chunks_summary':chunks})
with c.connect(c.R/'.iald_runtime/monthly_wallet/wallet.sqlite3') as db:
 ledger={table:[dict(r) for r in db.execute('SELECT * FROM '+table+' WHERE task_id=?',(jobid,))] for table in ['tasks','calls','entries']}
assert ledger['tasks'] and all(r['owner']==scope['principal'] for rows in ledger.values() for r in rows)
assert all(r['status']=='settled' for r in ledger['calls'])
cap=sum(r['cap'] for r in ledger['calls']);debit=-sum(r['delta'] for r in ledger['entries'] if r['kind']=='cost')
assert cap==debit and all(r['cost_status']=='estimated' for r in ledger['entries'] if r['kind']=='cost')
amount=Decimal(debit)/Decimal(10**9);prior=Decimal('0.19306')
result={'status':'CAPTURED_TERMINAL_FAILED_UNCERTAIN_NO_RETRY','job':job,'elapsed_seconds':job['updated']-job['created'],'owner_verified':'luiz','events':events,'events_sha256':c.digest(b''.join(hashes)),'terminal_done_event':events[-1]['value'].strip()=='[DONE]','model_declared_by_app':'mimo-v2.6-pro','models_in_received_partial_wire':sorted(models),'text':'','acom':{'context_id':context,'scope':scope,'request_id':request,'revision':state['revision'],'state_sha256':state['state_sha256'],'latest_event_hash_verified':True,'handles':handles,'custody':custody,'partial_transport':partials,'complete_response_custody':False,'uncertain':True},'ledger':ledger,'video_reserved_cap_usd':str(amount),'video_debit_usd':str(amount),'cost_status':'ESTIMATED_CAP_NOT_PROVIDER_MEASURED_OR_INVOICE','ledger_debit_equals_reserved_cap':True,'budget':{'operator_prior_approx_usd':str(prior),'prior_plus_video_pessimistic_approx_usd':str(prior+amount),'remaining_budget_usd':None,'reason':'No total mission ceiling supplied here; prior subtotal is operator approximation, not recounted unrelated jobs.'},'lifecycle':{'job':'failed','wallet_task':[r['status'] for r in ledger['tasks']],'discrepancy_preserved_no_financial_changes':True},'limitations':['Job delivery DONE is not provider stream completion.','Partial transport custody does not establish complete provider usage or billed cost.','Earlier success-only capture refused missing model usage metrics; no matching metric invented.','No retry/reopen/remote calls or runtime/ledger changes.'],'remote_calls':0,'retry':False,'runtime_writes':False}
with (W/'MANUAL_VIDEO_RESULT.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps({'job_status':job['status'],'elapsed':result['elapsed_seconds'],'partial_custody_verified':len(partials),'models':sorted(models),'reserved_and_debited_usd':str(amount),'cost_status':result['cost_status'],'approx_total_usd':str(prior+amount),'uncertain':True,'retry':False}))
