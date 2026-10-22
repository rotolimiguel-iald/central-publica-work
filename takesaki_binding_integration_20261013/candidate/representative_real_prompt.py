
import sys,json,sqlite3,hashlib,os
from pathlib import Path
from contextlib import closing
sys.dont_write_bytecode=True
from test_integration import IntegratedBinding
from iald_orchestrator import operational_memory as om,scientific_binding as sb
base=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
uid='ff9a08c5-5b3a-4b17-b0ea-319d59a978a2'
with closing(sqlite3.connect((base/'state/tasks.sqlite3').as_uri()+'?mode=ro',uri=True)) as db:
 db.row_factory=sqlite3.Row;row=dict(db.execute('SELECT * FROM coordination_jobs WHERE id=?',(uid,)).fetchone())
assert row['execution_constraints'] in (None,'null')
assert om.digest(row['prompt'])=='4c4fe67c0d53f80408ab38b8bb7a19a83214eadedd0f728e7e61790595d9a4a0'
cp=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.TAKESAKI\CONTRATO_TAKESAKI_R1.json')
raw=cp.read_bytes();assert sb.sha(raw)=='8bf4c80cf5f42312181da97b8e47601a4aeee7b775d3e764c3fbb2fa1241b95d'
prepared=base/'state/handoffs/ff9a08c5-5b3a-4b17-b0ea-319d59a978a2_prepared_supplement_20261013_175915_150606.txt'
pb=prepared.read_bytes();assert sb.sha(pb)=='4ca36f482ffc27a8d5ad07e5c7c286e06e78b7ee329b3fca927ca9a62fe71fd4'
case=IntegratedBinding();case.setUp()
try:
 # Only the disposable queue receives a copy of the original live row.
 with case.r.db() as db:
  names=list(row)
  db.execute('INSERT INTO coordination_jobs('+','.join(names)+') VALUES('+','.join('?' for _ in names)+')',[row[n] for n in names])
  om.stage(db,row['memory_context_id'],row['prompt'],None,'replica:original:0',
   phase='awaiting_dispatch',handle_id=uid,next_action='Disposable representative fixture; no dispatch.')
 om.sync(case.r,row['memory_context_id'])
 case.uid=uid;case.ref=row['memory_context_id'];case.prompt=row['prompt'];case.cp.write_bytes(raw);case.pin=sb.sha(raw);case.supp=pb.decode('utf-8')
 case.contract=json.loads(raw)
 case.authority.update(job_id=uid,request_id=row['request_id'],contract_sha256=case.pin,
  order_sha256=case.contract['authenticated_scope_order']['source']['sha256'],
  source_thread_id=case.contract['authenticated_scope_order']['thread_id'])
 case.ap.write_text(json.dumps(case.authority));case.ah=sb.sha(case.ap.read_bytes())
 result=case.bind(expected_version=row['version']);j=case.c.get(uid)
 projected=j['operational_memory']
 before=om.store(case.r).get(case.ref,om.SCOPE)
 p=case.c.act(uid,'prepare_without_work',{'reason':'assistance_not_needed'})
 assert len(p['prepared_prompt'])<=24000
 assert p['prompt']==row['prompt'] and p['execution_constraints'] is None
 assert case.supp.strip() in p['prepared_prompt'] and projected['receipt']['scientific_binding']['supplement_sha256']==case.pin
 assert before['constraints']=={} and projected['receipt'].get('scientific_binding')
 report={'status':'PASS_DISPOSABLE_REPRESENTATIVE','original_job_id':uid,'original_prompt_sha256':om.digest(row['prompt']),
 'original_prompt_chars':len(row['prompt']),'prepared_supplement_bytes':len(pb),'prepared_supplement_chars':len(case.supp),
 'combined_prepared_chars':len(p['prepared_prompt']),'normalized_supplement_chars':len(case.supp.strip()),'supplement_normalization':'existing validate_prompt.strip; raw source retained by pin','transport_original_retained':True,'projection_chars':len(projected['text']),
 'binding_record_included':'binding_'+case.pin in projected['included_record_ids'],
 'effective_required_provider':p['effective_execution_constraints']['required_provider'],'anchor_constraints':before['constraints'],
 'provider_calls':0,'work_calls':0,
 'scope':'Copied only scientific coordination row from mode=ro DB; new isolated ACOM recreated initial objective/constraints/flow, not a byte clone of whole live memory; authority/board/graph fixture explicitly simulated; source pins and prepared supplement real.'}
finally:case.tearDown()
out=Path(__file__).parent/'REPRESENTATIVE_REAL_PROMPT.json';data=json.dumps(report,ensure_ascii=False,indent=2).encode();assert not out.exists();tmp=out.with_suffix('.tmp')
with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==data;os.replace(tmp,out);print(json.dumps(report));print('sha256',hashlib.sha256(data).hexdigest())
