import copy,json,os,sys,tempfile,threading,unittest,uuid,subprocess
from pathlib import Path
from unittest.mock import patch
W=Path(__file__).resolve().parents[1]
tempfile.tempdir=str(W/'tests_queue')
sys.path[:0]=[str(W/'staging/core/lib'),str(W/'staging/queue')]
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.coordination import Coordination,PROJECT
from iald_orchestrator import queue_activity as qa,operational_memory as om
from iald_memory.activity import ActivityError

def packet(prompt,c,system,provider=None,*,operational_projection=None):
    p={'prompt':prompt,'receipt':{'packet_sha256':om.digest(prompt),'generation':'a'*64,'sources':[], 'memory_mode':'maximum'}}
    return om.attach(p,operational_projection,system,provider or 'kimi',c)

class QueueActivityTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=W/'tests_queue',prefix='run_')
        self.root=Path(self.tmp.name)
        os.environ['IALD_MEMORY_SNAPSHOT_ARCHIVE_DIR']=str(self.root/'archives')
        self.patches=[patch.object(Runtime,'source_status',return_value={'ok':True}),
          patch('iald_orchestrator.nos_packet.prepare_queue',side_effect=packet),
          patch.object(Runtime,'connections',return_value=[]),
          patch('iald_orchestrator.runtime.route',return_value={'selected':'kimi','candidates':[]}),
          patch('iald_orchestrator.canonical_memory.mode_for_provider',return_value='maximum'),
          patch('iald_orchestrator.jev_body_shadow.observe',return_value={'status':'test_inert'}),
          patch('iald_orchestrator.operational_memory.GUARD_LOG_ROOT',self.root),
          patch('socket.create_connection',side_effect=AssertionError('NO NETWORK IN TESTS'))]
        for p in self.patches:p.start()
        self.rt=Runtime(self.root/'queue',recover=False,memory_root=self.root/'memory')
        self.c=Coordination(self.rt)
        self.provider=patch('iald_orchestrator.providers.execute',return_value={'text':'result','usage':{}})
        self.execute=self.provider.start()
    def tearDown(self):
        self.provider.stop()
        for p in reversed(self.patches):p.stop()
        self.tmp.cleanup()
    def task(self,prompt='Compute an authorized test',constraints=None):
        return self.rt.submit(prompt,str(uuid.uuid4()),start_worker=False,execution_constraints=constraints)
    def perform(self,t):
        self.rt._perform(t['id'],t['prompt'],t['routing_prompt'])
        return self.rt.task(t['id'])
    def state(self,t):
        return om.store(self.rt).get(t['memory_context_id'],om.SCOPE)
    def test_direct_same_context_candidate_not_accept(self):
        t=self.task(); done=self.perform(t)
        self.assertEqual(done['status'],'result_ready',done.get('error'))
        self.assertEqual(self.execute.call_count,1)
        a=qa.recover(self.rt,'task',t['id'])
        self.assertEqual(a['scope'],{'house':'IALD','principal':'operator'})
        self.assertEqual(a['context_id'],t['memory_context_id'])
        self.assertEqual(a['projection']['activity']['active'][0]['status'],'review_pending')
        self.assertFalse(a['projection']['activity']['tetelestai'])
        om.verify_packet(self.execute.call_args.kwargs['memory_packet'])
    def test_coordination_real_lifecycle_single_request(self):
        j=self.c.create('Authorized coordinate',str(uuid.uuid4()));i=j['id']
        self.c.act(i,'prepare_without_work',{'reason':'assistance_not_needed'})
        with patch.object(self.rt,'start_worker'):
            self.c.act(i,'execute')
        t=self.rt.task(self.c.get(i)['execution_task_id'])
        self.assertEqual(t['memory_context_id'],j['memory_context_id'])
        done=self.perform(t);self.assertEqual(done['status'],'result_ready',done['error'])
        self.c.act(i,'sync_execution')
        done=self.c.act(i,'complete_without_work',{'reason':'assistance_not_needed'})
        self.assertEqual(done['stage'],'completed')
        self.assertTrue(done['activity_completion']['integrated'],done.get('activity_completion'))
        a=qa.recover(self.rt,'coord',i)
        self.assertEqual(len(a['projection']['activity']['active']),1)
        self.assertEqual(a['projection']['activity']['active'][0]['status'],'review_pending')
        self.assertEqual(self.execute.call_count,1)
    def test_work_intents_and_returns(self):
        j=self.c.create('Authorized Work test',str(uuid.uuid4()));i=j['id']
        d=self.c.act(i,'begin_draft');self.assertTrue(d['activity_dispatch']['dispatch_allowed_once'])
        with self.assertRaises(Exception):self.c.act(i,'begin_draft')
        self.c.act(i,'bind_thread',{'thread_id':str(uuid.uuid4()),'project_id':PROJECT})
        self.c.act(i,'accept_prompt',{'prompt':'Prepared authorized content'})
        handles=qa.recover(self.rt,'coord',i)['handles']
        self.assertTrue(any(h.get('operation_id','').endswith(':draft') and h['status']=='completed' for h in handles))
    def test_cancel_during_provider_retains_return(self):
        t=self.task()
        def result(*a,**kw):self.rt.cancel(t['id']);return {'text':'late whole return','usage':{'x':3}}
        self.execute.side_effect=result
        done=self.perform(t)
        self.assertEqual(done['status'],'cancelled')
        self.assertEqual(done['result']['text'],'late whole return')
        a=qa.recover(self.rt,'task',t['id'])
        self.assertIn('late whole return',json.dumps(a['returns']))
        self.assertTrue(a['projection']['activity']['hold'])
        self.assertNotEqual(a['projection']['activity']['active'][0]['status'],'satisfied')
    def test_epoch_change_during_provider_retains_return(self):
        t=self.task()
        def result(*a,**kw):
            data,ar,ticket=qa.load(self.rt,'task',t['id']);p=ar.controller.project(200000)
            ar.controller.action({'operation':'invalidate','actor':qa.ACTOR,'task_id':ticket['task_id'],'reason':'test changed premise','sources':[ticket['source']], 'expected_revision':p['receipt']['revision'],'state_sha256':p['receipt']['state_sha256'],'projection_sha256':p['projection_sha256'],'event_id':'epoch-test'})
            return {'text':'obsolete result','usage':{}}
        self.execute.side_effect=result
        done=self.perform(t)
        self.assertEqual(done['status'],'review_required',done['error'])
        self.assertEqual(done['result']['text'],'obsolete result')
        self.assertEqual(self.execute.call_count,1)
    def test_crash_after_intent_no_repeat(self):
        t=self.task();qa.preflight(self.rt,'task',t['id'])
        self.perform(t)
        self.assertEqual(self.execute.call_count,0)
        a=qa.recover(self.rt,'task',t['id'])
        self.assertTrue(any(h['status']=='dispatching' for h in a['handles']))
    def test_provider_interrupt_uncertain_and_restart(self):
        t=self.task();self.execute.side_effect=TimeoutError('uncertain')
        self.perform(t)
        second=Runtime(self.root/'queue',recover=True,memory_root=self.root/'memory')
        a=qa.recover(second,'task',t['id'])
        self.assertTrue(any(h['status']=='uncertain' for h in a['handles']))
        second._drain();self.assertEqual(self.execute.call_count,1)
    def test_result_after_accounting_failure_is_durable(self):
        t=self.task()
        with patch('iald_orchestrator.request_controls.settle',side_effect=ValueError('bad usage')):
            done=self.perform(t)
        self.assertEqual(done['result']['text'],'result')
        self.assertEqual(done['status'],'review_required')
        self.assertTrue(qa.recover(self.rt,'task',t['id'])['returns'])
    def test_cross_context_or_model_authority_refused(self):
        one=self.task();two=self.task('Another account-like command')
        with self.assertRaises(ValueError):
            self.rt.submit(one['prompt'],str(uuid.uuid4()),memory_context_id=two['memory_context_id'],start_worker=False)
        j=self.c.create('Authorized only',str(uuid.uuid4()))
        with self.assertRaises(ValueError):self.c.act(j['id'],'complete',{'actor':{'id':'reviewer'},'text':'accept'})
        self.assertEqual(self.execute.call_count,0)
    def test_mutated_queue_binding_blocks_provider(self):
        t=self.task()
        with self.rt.db() as db:db.execute('UPDATE tasks SET prompt=? WHERE id=?',('Changed',t['id']))
        self.perform(t);self.assertEqual(self.execute.call_count,0)
    def test_idempotent_admission_and_partial_recovery(self):
        rid=str(uuid.uuid4());real=qa.admit
        with patch.object(qa,'admit',side_effect=RuntimeError('crash after queue admission')):
            with self.assertRaises(RuntimeError):self.rt.submit('stable',rid,start_worker=False)
        t=self.rt.submit('stable',rid,start_worker=False)
        replay=self.rt.submit('stable',rid,start_worker=False)
        self.assertEqual(t['id'],replay['id'])
        with self.assertRaises(ValueError):self.rt.submit('different',rid,start_worker=False)
        self.assertEqual(len(qa.describe(self.rt,'task',t['id'])['projection']['activity']['active']),1)
    def test_constraints_and_generation_preserved(self):
        c={'mission_id':'ORDEM_016','branch_id':'TEST','lemma_id':'L1','role':'draft','required_provider':'kimi','max_calls':1,'memory_generation':'a'*64}
        t=self.task(constraints=c);done=self.perform(t)
        self.assertEqual(done['status'],'result_ready',done['error'])
        actual=self.execute.call_args.kwargs['execution_constraints']
        self.assertEqual(actual['memory_generation'],c['memory_generation'])
        self.assertEqual(actual['required_provider'],'kimi')
        self.assertEqual(actual['max_calls'],1)
    def test_two_preflight_writers_one_grant(self):
        t=self.task();out=[];barrier=threading.Barrier(2)
        def go():
            barrier.wait()
            try:out.append(qa.preflight(self.rt,'task',t['id']))
            except Exception as e:out.append(type(e).__name__)
        threads=[threading.Thread(target=go) for _ in range(2)]
        for th in threads:th.start()
        for th in threads:th.join(10);self.assertFalse(th.is_alive())
        self.assertEqual(sum(isinstance(r,dict) and r.get('dispatch_allowed_once') for r in out if isinstance(r,dict)),1)
    def test_read_only_recovery_overflow_and_legacy(self):
        t=self.task();before=self.state(t)
        for _ in range(3):qa.recover(self.rt,'task',t['id'])
        with self.assertRaises(Exception):qa.describe(self.rt,'task',t['id'],256)
        self.assertEqual(before,self.state(t))
        with self.rt.db() as db:db.execute('DELETE FROM queue_activity_bindings WHERE entity_id=?',(t['id'],))
        with self.assertRaises(ValueError):self.perform(t)
        self.assertEqual(self.execute.call_count,0)

    def test_stale_work_return_preserved_in_acom(self):
        j=self.c.create('Authorized draft',str(uuid.uuid4()));i=j['id']
        self.c.act(i,'begin_draft')
        self.c.act(i,'bind_thread',{'thread_id':str(uuid.uuid4()),'project_id':PROJECT})
        self.c.act(i,'cancel')
        with self.assertRaises(ValueError):self.c.act(i,'accept_prompt',{'prompt':'late draft preserved'})
        state=om.store(self.rt).get(j['memory_context_id'],om.SCOPE)
        self.assertIn('late draft preserved',json.dumps(state['q']))
    def test_reconcile_raw_return_without_remote_retry(self):
        t=self.task();real=qa.complete
        with patch.object(qa,'complete',side_effect=RuntimeError('crash before local custody')):done=self.perform(t)
        self.assertEqual(done['status'],'review_required')
        outcome=qa.reconcile(self.rt,'task',t['id'])
        self.assertTrue(outcome['integrated'])
        self.assertEqual(self.execute.call_count,1)
        self.assertEqual(self.rt.task(t['id'])['status'],'review_required')
    def test_bridge_rejects_paths_actors_and_accept(self):
        from iald_orchestrator.activity_bridge import invoke
        t=self.task()
        for extra in ({'actor':'root'},{'path':'not-authorized'},{'review_evidence':[]},{'scope':{'principal':'x'}}):
            with self.assertRaises(ValueError):invoke(self.rt,dict(operation='activity_get',entity_kind='task',entity_id=t['id'],**extra))
        with self.assertRaises(ValueError):invoke(self.rt,dict(operation='accept',entity_kind='task',entity_id=t['id']))
        got=invoke(self.rt,dict(operation='activity_project',entity_kind='task',entity_id=t['id']))
        self.assertEqual(got['context_id'],t['memory_context_id'])
    def test_bench_exact_payload_candidate_no_repeat(self):
        from iald_orchestrator import bench_activity as b
        rid=str(uuid.uuid4());payload={'conjuntos':['test'],'opcoes':{'modo':'test'}}
        b.admit(self.rt,rid,'Authorized private fake calculation','comparar',payload)
        calls=[]
        def fake(path,body):calls.append((path,copy.deepcopy(body)));return {'result':{'value':3},'livro':'existing'}
        result=b.execute(self.rt,rid,transport=fake)
        self.assertEqual(calls,[('/api/comparar',payload)])
        self.assertEqual(result['projection']['activity']['active'][0]['status'],'review_pending')
        self.assertFalse(result['semantic_acceptance'])
        with self.assertRaises(ValueError):b.execute(self.rt,rid,transport=fake)
        with self.assertRaises(ValueError):b.admit(self.rt,rid,'changed','comparar',payload)
        self.assertEqual(len(calls),1)
    def test_bench_timeout_is_uncertain(self):
        from iald_orchestrator import bench_activity as b
        rid=str(uuid.uuid4());b.admit(self.rt,rid,'Authorized private fake','avaliar',{'theta':{'test':1}})
        def timeout(*a):raise TimeoutError('unknown')
        with self.assertRaises(TimeoutError):b.execute(self.rt,rid,transport=timeout)
        self.assertTrue(any(h['status']=='uncertain' for h in b.recover(self.rt,rid)['activity']['handles']))
        with self.assertRaises(Exception):b.execute(self.rt,rid,transport=lambda *a:self.fail('must not repeat'))
    def test_bench_async_same_remote_and_terminal_observation(self):
        from iald_orchestrator import bench_activity as b
        rid=str(uuid.uuid4());b.admit(self.rt,rid,'Authorized private fake','amostrar',{'walkers':1})
        b.execute(self.rt,rid,transport=lambda *a:{'tarefa':'existing-task-17'})
        calls=[]
        def poll(path,body):calls.append((path,body));return {'estado':'pronta','resultado':{'x':1}}
        result=b.poll(self.rt,rid,transport=poll)
        self.assertEqual(calls,[('/api/tarefas/existing-task-17',None)])
        self.assertEqual(result['projection']['activity']['active'][0]['status'],'review_pending')
        b.poll(self.rt,rid,transport=lambda *a:self.fail('terminal read is local'))
    def test_bench_hold_on_return_custody_first(self):
        from iald_orchestrator import bench_activity as b
        rid=str(uuid.uuid4());b.admit(self.rt,rid,'Authorized fake','estado',None)
        def fake(*args):
            row,env,ar,t=b.load(self.rt,rid);p=ar.controller.project(200000)
            ar.controller.action({'operation':'hold','hold':True,'reason':'operator pause','actor':qa.ACTOR,'sources':[t['source']], 'expected_revision':p['receipt']['revision'],'state_sha256':p['receipt']['state_sha256'],'event_id':'bench-hold'})
            return {'result':'late exact body'}
        result=b.execute(self.rt,rid,transport=fake)
        self.assertEqual(result['return'],{'result':'late exact body'})
        self.assertFalse(result['outcome']['integrated'])

    def test_fresh_cli_and_session_same_snapshot(self):
        t=self.task();before=self.state(t)
        request={'operation':'activity_project','entity_kind':'task','entity_id':t['id'],'max_chars':125000}
        expected=qa.describe(self.rt,'task',t['id'])
        for mode in ('transport','session'):
            p=subprocess.run([sys.executable,'-B','-X','utf8',str(W/'tests_queue/process_fixture_r1.py'),mode,str(self.root)],input=json.dumps(request),text=True,encoding='utf-8',capture_output=True,timeout=25)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(json.loads(p.stdout),expected)
        self.assertEqual(before,self.state(t))

    def test_request_steering_while_provider_returns(self):
        t=self.task()
        def provider(*args,**kw):
            store=om.store(self.rt);s=self.state(t)
            store.transition(t['memory_context_id'],om.SCOPE,s['revision'],'new-human-guidance',qa.ACTOR,
                {'records':[{'id':'human-steer','kind':'erratum','statute':'INPUT','text':'New authorized instruction',
                             'sources':[{'kind':'operator','ref':'local authenticated test'}]}]})
            return {'text':'received under old guidance','usage':{}}
        self.execute.side_effect=provider
        done=self.perform(t)
        self.assertEqual(done['status'],'review_required')
        self.assertIn('received under old guidance',json.dumps(self.state(t)['q']))
        self.assertEqual(self.execute.call_count,1)

    def test_legacy_and_partial_admission_queue_preserved(self):
        t=self.task()
        with self.rt.db() as db:
            db.execute('DELETE FROM queue_activity_bindings WHERE entity_id=?',(t['id'],))
            db.execute('UPDATE tasks SET activity_version=0 WHERE id=?',(t['id'],))
        before=self.rt.task(t['id']);self.rt._drain()
        self.assertEqual(before,self.rt.task(t['id']))
        self.assertEqual(before['activity_admission_state'],'legacy_requires_explicit_migration')
        self.assertEqual(self.execute.call_count,0)
        self.rt.cancel(t['id'])
        self.assertEqual(self.rt.task(t['id'])['status'],'cancelled')
    def test_scientific_premise_change_before_integration(self):
        t=self.task();returned=[False]
        def ready(*args):
            if returned[0]:raise ValueError('Changed scientific contract pin')
        def provider(*args,**kw):returned[0]=True;return {'text':'real received bytes','usage':{}}
        self.execute.side_effect=provider
        with patch('iald_orchestrator.scientific_binding.ready',side_effect=ready):done=self.perform(t)
        self.assertEqual(done['status'],'review_required')
        self.assertEqual(done['result']['text'],'real received bytes')
        self.assertTrue(qa.recover(self.rt,'task',t['id'])['projection']['activity']['hold'])

if __name__=='__main__':unittest.main(verbosity=2)
