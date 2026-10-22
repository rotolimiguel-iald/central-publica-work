
import json,uuid,tempfile,unittest,threading,hashlib,sys
from pathlib import Path
from contextlib import closing
from unittest.mock import patch,Mock
sys.dont_write_bytecode=True
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.coordination import Coordination
from iald_orchestrator import runtime as rt,scientific_binding as sb,operational_memory as om
from iald_orchestrator import canonical_memory

class IntegratedBinding(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  self.r=Runtime(self.root/'queue',recover=False,memory_root=self.root/'acom')
  self.r.source_status=lambda:{'ok':True}
  self.r.connections=lambda:[{'id':'kimi','status':'ready'}]
  self.r.start_worker=Mock()
  om.GUARD_LOG_ROOT=self.root/'guard'
  def packet(prompt,c,system,*args,operational_projection=None):
   return {'prompt':prompt+'\\n'+(operational_projection or {}).get('text',''),
     'receipt':{'generation':'f'*64,'sources':[],'memory_mode':canonical_memory.mode_for_provider('kimi',c),
       'operational_memory':(operational_projection or {}).get('receipt',{})}}
  self.patches=[patch.object(rt.nos_packet,'prepare_queue',side_effect=packet),
     patch.object(rt,'route',return_value={'selected':'kimi','candidates':[]}),
     patch.object(rt.providers,'execute',side_effect=AssertionError('Unexpected provider call')),
     patch.object(rt.jev_body_shadow,'observe',return_value={'status':'test_stub'})]
  for p in self.patches:p.start()
  self.c=Coordination(self.r);self.prompt='Scientific modular trace covariance, original immutable request.'
  j=self.c.create(self.prompt,str(uuid.uuid4()),None);self.uid=j['id'];self.ref=j['memory_context_id']
  def artifact(name,raw):
   p=self.root/name;p.write_bytes(raw);return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
  order=artifact('operator.txt',b'Authenticated human source fixture, not a model response.')
  source=artifact('source.lean',b'theorem fixture : True := by trivial')
  self.contract={'schema':'iald-scientific-contract-supplement/v1','preserve_original':True,'unit':'F1.TAKESAKI',
    'job_id':self.uid,'request_id':j['request_id'],'original_memory_context_id':self.ref,
    'original_prompt_sha256':om.digest(self.prompt),
    'execution_constraints':{'mission_id':'TGL_BANCADA_OFICIAL','branch_id':'F1.TAKESAKI','lemma_id':'test_takesaki','role':'draft','required_provider':'kimi','max_calls':1,'max_projection_chars':None},
    'authenticated_scope_order':{'source':order,'thread_id':'01a11878-6e36-7d10-83c4-cd72e757fdd0'},
    'primary_source_pins':[source],'working_v392':source}
  self.cp=self.root/'contract.json';self.cp.write_text(json.dumps(self.contract));self.pin=sb.sha(self.cp.read_bytes())
  board=artifact('board.json',json.dumps({'unidades':[{'id':'F1.TAKESAKI','status':'EM_CURSO'}]}).encode())
  import sqlite3
  gp=self.root/'graph.sqlite3'
  with closing(sqlite3.connect(gp)) as db:
   db.execute('CREATE TABLE nos(id TEXT PRIMARY KEY,tipo TEXT)')
   db.execute('INSERT INTO nos VALUES(?,?)',('unidade:F1.TAKESAKI','unidade'));db.commit()
  graph={'path':str(gp),'sha256':sb.sha(gp.read_bytes()),'bytes':gp.stat().st_size}
  self.authority={'schema':'scientific-binding-authority/v1','job_id':self.uid,'request_id':j['request_id'],'unit':'F1.TAKESAKI',
   'contract_sha256':self.pin,'order_sha256':order['sha256'],'source_thread_id':self.contract['authenticated_scope_order']['thread_id'],
   'verified_by':'codex-coordenadora','human_message_ids':['human-official-fixture'],'board_path':board['path'],'board_sha256':board['sha256'],
   'graph_path':graph['path'],'graph_sha256':graph['sha256'],'graph_unit':'F1.TAKESAKI'}
  self.ap=self.root/'authority.json';self.ap.write_text(json.dumps(self.authority));self.ah=sb.sha(self.ap.read_bytes())
  self.supp='Explicit v392 source excerpt, status pending ratification. '+source['sha256']

 def tearDown(self):
  self.assertEqual(rt.providers.execute.call_count,0)
  for p in reversed(self.patches):p.stop()
  import gc;gc.collect()
  self.tmp.cleanup()

 def bind(self,**kw):
  args=dict(expected_version=0,authority_path=str(self.ap),authority_sha=self.ah,prepared_supplement=self.supp);args.update(kw)
  return self.c.bind_scientific_contract(self.uid,str(self.cp),self.pin,**args)

 def count(self,table):
  with self.r.db() as db:return db.execute('SELECT count(*) FROM '+table).fetchone()[0]

 def test_prepare_dispatch_identity_and_receipt(self):
  first=self.bind();j=self.c.get(self.uid)
  self.assertIsNone(j['execution_constraints']);self.assertEqual(j['effective_execution_constraints']['required_provider'],'kimi')
  self.assertEqual(om.store(self.r).get(self.ref,om.SCOPE)['constraints'],{})
  self.assertNotIn(str(self.root),j['operational_memory']['text'])
  self.assertEqual(j['operational_memory']['receipt']['scientific_binding']['supplement_sha256'],self.pin)
  p=self.c.act(self.uid,'prepare_without_work',{'reason':'assistance_not_needed'})
  self.assertIn(self.supp,p['prepared_prompt']);self.assertEqual(p['prompt'],self.prompt)
  done=self.c.act(self.uid,'execute');task=done['execution']
  self.assertIsNone(task['execution_constraints']);self.assertEqual(task['effective_execution_constraints']['max_calls'],1)
  self.assertEqual(task['memory_context_id'],self.ref)
  self.assertEqual(task['request_id'],str(uuid.uuid5(uuid.NAMESPACE_URL,'iald-coordination:'+self.uid)))
  self.r.start_worker.assert_called_once()
  # Worker must use the effective route while memory still receives {}.
  with patch.object(rt.providers,'execute',return_value={'text':'DECLARADO fixture','usage':{}}) as provider:
   self.r._perform(task['id'],task['prompt'],task['routing_prompt'])
   self.assertEqual(provider.call_count,1)
   self.assertEqual(provider.call_args.kwargs['execution_constraints']['required_provider'],'kimi')
   self.assertEqual(provider.call_args.kwargs['memory_packet']['receipt']['operational_memory']['scientific_binding']['supplement_sha256'],self.pin)
  self.assertEqual(self.r.task(task['id'])['status'],'result_ready')
  self.assertEqual(om.store(self.r).get(self.ref,om.SCOPE)['constraints'],{})
  with self.assertRaises(ValueError):self.c.act(self.uid,'execute')

 def test_exact_replay_no_new_outbox_or_version(self):
  self.bind();before=(self.count('memory_outbox'),self.count('coordination_events'))
  self.assertTrue(self.bind()['replay']);self.assertEqual(before,(self.count('memory_outbox'),self.count('coordination_events')))
  with self.assertRaises(ValueError):self.bind(prepared_supplement=self.supp+' changed')
  with self.r.db() as db:
   with self.assertRaises(Exception):db.execute('DELETE FROM scientific_contract_bindings')

 def test_stale_and_after_prepare(self):
  with self.assertRaises(ValueError):self.bind(expected_version=1)
  self.c.act(self.uid,'prepare_without_work',{'reason':'assistance_not_needed'})
  with self.assertRaises(ValueError):self.bind()
  self.assertEqual(self.count('scientific_contract_bindings'),0)

 def test_terminal_and_draft_refused(self):
  for stage in ('draft_dispatching','failed','cancelled','completed'):
   with self.r.db() as db:db.execute('UPDATE coordination_jobs SET stage=? WHERE id=?',(stage,self.uid))
   with self.subTest(stage=stage),self.assertRaises(ValueError):self.bind()
  self.assertEqual(self.count('scientific_contract_bindings'),0)

 def test_source_tamper(self):
  Path(self.contract['primary_source_pins'][0]['path']).write_bytes(b'changed')
  with self.assertRaises(ValueError):self.bind()
  self.assertEqual(self.count('scientific_contract_bindings'),0)

 def test_authority_wrong_actor_and_proof(self):
  self.authority['verified_by']='model';self.ap.write_text(json.dumps(self.authority));self.ah=sb.sha(self.ap.read_bytes())
  with self.assertRaises(ValueError):self.bind()
  self.authority['verified_by']='codex-coordenadora';self.authority['human_message_ids']=[]
  self.ap.write_text(json.dumps(self.authority));self.ah=sb.sha(self.ap.read_bytes())
  with self.assertRaises(ValueError):self.bind()
  self.assertEqual(self.count('scientific_contract_bindings'),0)

 def test_rollback_outbox_insert_failure(self):
  with self.r.db() as db:db.execute('''CREATE TRIGGER deny_binding_outbox BEFORE INSERT ON memory_outbox
   WHEN NEW.event_id LIKE 'scientific-contract:%' BEGIN SELECT RAISE(ABORT,'test crash'); END''')
  with self.assertRaises(Exception):self.bind()
  self.assertEqual(self.count('scientific_contract_bindings'),0);self.assertEqual(self.count('coordination_events'),0)
  with self.r.db() as db:self.assertEqual(db.execute('SELECT version FROM coordination_jobs').fetchone()[0],0)

 def test_crash_after_commit_recovery(self):
  with patch.object(sb,'ready',side_effect=RuntimeError('test crash after queue commit')):
   with self.assertRaises(RuntimeError):self.bind()
  self.assertEqual(self.count('scientific_contract_bindings'),1)
  with self.r.db() as db:self.assertIsNone(db.execute("SELECT receipt_json FROM memory_outbox WHERE event_id LIKE 'scientific-contract:%'").fetchone()[0])
  self.c.get(self.uid)
  with self.r.db() as db:self.assertIsNotNone(db.execute("SELECT receipt_json FROM memory_outbox WHERE event_id LIKE 'scientific-contract:%'").fetchone()[0])
  self.assertTrue(self.bind()['replay'])

 def test_crash_after_memory_commit_before_queue_ack(self):
  core=om.core();real=core.MemoryStore.transition;once=[False]
  def interrupted(store,*args,**kwargs):
   result=real(store,*args,**kwargs)
   if 'scientific-contract:' in str(args) and not once[0]:
    once[0]=True;raise RuntimeError('test crash after ACOM commit')
   return result
  with patch.object(core.MemoryStore,'transition',interrupted):
   with self.assertRaises(RuntimeError):self.bind()
  state=om.store(self.r).get(self.ref,om.SCOPE);revision=state['revision']
  self.c.get(self.uid)
  self.assertEqual(om.store(self.r).get(self.ref,om.SCOPE)['revision'],revision)

 def test_record_omission_blocks_prepare(self):
  self.bind()
  real=om.projection
  def missing(*a,**k):
   p=real(*a,**k);p['included_record_ids']=[];return p
  with patch.object(om,'projection',side_effect=missing):
   with self.assertRaises(ValueError):self.c.act(self.uid,'prepare_without_work',{'reason':'assistance_not_needed'})
  with self.r.db() as db:self.assertEqual(db.execute('SELECT stage FROM coordination_jobs').fetchone()[0],'awaiting_dispatch')

 def test_concurrent_bind_single_event(self):
  errors=[];results=[]
  def run():
   try:results.append(self.bind())
   except Exception as e:errors.append(type(e).__name__)
  threads=[threading.Thread(target=run) for _ in range(2)]
  for t in threads:t.start()
  for t in threads:t.join()
  self.assertEqual(self.count('scientific_contract_bindings'),1)
  self.assertEqual(self.count('coordination_events'),1)
  self.assertTrue(results)
  self.assertEqual(self.count('attempts'),0)

 def test_direct_task_bypass_refused(self):
  result=self.bind();c=result['binding']['effective_constraints']
  with self.assertRaises(ValueError):self.r.submit('changed prompt',str(uuid.uuid5(uuid.NAMESPACE_URL,'iald-coordination:'+self.uid)),
    routing_prompt=self.prompt,execution_constraints=c,memory_context_id=self.ref,scientific_binding_job_id=self.uid,start_worker=False)
  self.assertEqual(self.count('tasks'),0)


 def dispatched(self):
  self.bind();self.c.act(self.uid,'prepare_without_work',{'reason':'assistance_not_needed'})
  return self.c.act(self.uid,'execute')['execution']

 def test_drain_real_preserves_running_anchor(self):
  task=self.dispatched()
  with patch.object(rt.providers,'execute',return_value={'text':'DECLARADO drain','usage':{}}) as provider:
   self.r._drain()
   self.assertEqual(provider.call_count,1)
  self.assertEqual(self.r.task(task['id'])['status'],'result_ready')
  self.assertEqual(om.store(self.r).get(self.ref,om.SCOPE)['constraints'],{})
  with self.r.db() as db:
   rows=db.execute('SELECT constraints_json FROM memory_outbox').fetchall()
   self.assertTrue(all(json.loads(row[0])=={} for row in rows))

 def test_source_changes_during_return_preserves_return(self):
  task=self.dispatched()
  def returned(*a,**kw):
   Path(self.contract['primary_source_pins'][0]['path']).write_bytes(b'changed DURING model')
   return {'text':'DECLARADO durable return','usage':{}}
  with patch.object(rt.providers,'execute',side_effect=returned) as provider:
   self.r._drain();self.r._drain()
   self.assertEqual(provider.call_count,1)
  result=self.r.task(task['id'])
  self.assertEqual(result['status'],'result_ready');self.assertIn('durable',result['result']['text'])
  with self.r.db() as db:self.assertEqual(db.execute('SELECT status FROM attempts').fetchone()[0],'returned')

 def test_source_changes_before_send_no_attempt(self):
  task=self.dispatched()
  Path(self.contract['primary_source_pins'][0]['path']).write_bytes(b'changed BEFORE model')
  self.r._drain()
  self.assertEqual(self.count('attempts'),0);self.assertEqual(self.r.task(task['id'])['status'],'failed')

 def test_executor_failure_no_repeat(self):
  task=self.dispatched()
  with patch.object(rt.providers,'execute',side_effect=TimeoutError('fake uncertain failure')) as provider:
   self.r._drain();self.r._drain()
   self.assertEqual(provider.call_count,1)
  self.assertEqual(self.r.task(task['id'])['status'],'failed')
  with self.r.db() as db:self.assertEqual(db.execute('SELECT status FROM attempts').fetchone()[0],'failed_or_interrupted')

 def test_same_raw_supplement_whitespace_replay(self):
  self.supp='  '+self.supp+'\n'
  first=self.bind()
  self.assertTrue(self.bind()['replay'])
  self.assertEqual(first['binding']['prepared_supplement'],self.supp.strip())

 def test_replay_after_board_change(self):
  self.bind();before=(self.count('memory_outbox'),self.count('coordination_events'))
  Path(self.authority['board_path']).write_bytes(b'new unrelated board event')
  self.assertTrue(self.bind()['replay'])
  self.assertEqual(before,(self.count('memory_outbox'),self.count('coordination_events')))

 def test_unclaimed_board_or_missing_graph(self):
  import sqlite3
  Path(self.authority['board_path']).write_text(json.dumps({'unidades':[{'id':'F1.TAKESAKI','status':'CANCELADA'}]}))
  self.authority['board_sha256']=sb.sha(Path(self.authority['board_path']).read_bytes())
  self.ap.write_text(json.dumps(self.authority));self.ah=sb.sha(self.ap.read_bytes())
  with self.assertRaises(ValueError):self.bind()
  Path(self.authority['board_path']).write_text(json.dumps({'unidades':[{'id':'F1.TAKESAKI','status':'EM_CURSO'}]}))
  self.authority['board_sha256']=sb.sha(Path(self.authority['board_path']).read_bytes())
  with closing(sqlite3.connect(self.authority['graph_path'])) as db:db.execute('DELETE FROM nos');db.commit()
  self.authority['graph_sha256']=sb.sha(Path(self.authority['graph_path']).read_bytes())
  self.ap.write_text(json.dumps(self.authority));self.ah=sb.sha(self.ap.read_bytes())
  with self.assertRaises(ValueError):self.bind()

 def test_complete_prepared_payload_cap_not_raised(self):
  self.supp='x'*23990;self.bind()
  with self.assertRaises(ValueError):self.c.act(self.uid,'prepare_without_work',{'reason':'assistance_not_needed'})
  with self.r.db() as db:self.assertEqual(db.execute('SELECT stage FROM coordination_jobs').fetchone()[0],'awaiting_dispatch')

 def test_projection_measured_budget(self):
  self.bind()
  state=om.store(self.r).get(self.ref,om.SCOPE)
  # Actual durable q growth forces a projection above old default, while preserving mandatory record.
  om.store(self.r).transition(self.ref,om.SCOPE,state['revision'],'test-q-growth',om.ACTOR,
   {'records':[{'id':'extra','kind':'fact','text':'y'*9000,'statute':'DECLARADO','sources':[{'kind':'artifact','ref':'fixture'}]}]})
  j=self.c.get(self.uid)
  self.assertGreater(len(j['operational_memory']['text']),6500)
  self.assertIn('binding_'+self.pin,j['operational_memory']['included_record_ids'])

if __name__=='__main__':unittest.main(verbosity=2)
