import tempfile,time,unittest,uuid
from unittest.mock import patch
from iald_orchestrator.coordination import Coordination
from iald_orchestrator.runtime import Runtime
from iald_orchestrator import canonical_memory
from test_orchestrator import connections

class OptionalWorkTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.r=Runtime(self.temp.name,recover=False);self.c=Coordination(self.r)
        p='Scientific context';packet={'prompt':p,'receipt':{'packet_sha256':canonical_memory.digest(p.encode()),'sources':[],'generation':'a'*64}}
        self.patches=[patch.object(Runtime,'source_status',return_value={'ok':True}),patch('iald_orchestrator.providers.discover',return_value=connections()),patch.object(canonical_memory,'prepare',return_value=packet)]
        for p in self.patches:p.start()
    def tearDown(self):
        with self.r.worker_lock:pass
        for p in self.patches:p.stop()
        self.temp.cleanup()
    def job(self):
        c=dict(mission_id='ORDEM_016',branch_id='optional',lemma_id='optional',role='draft',required_provider='local',max_calls=1)
        return self.c.create('Somar dois valores.',str(uuid.uuid4()),c)['id']
    def exhaust_work(self):
        from iald_orchestrator.runtime import now
        with self.r.db() as db:
            for _ in range(3):db.execute('INSERT INTO coordination_events(job_id,at,action,from_stage,to_stage) VALUES(?,?,?,?,?)',('fixture',now(),'begin_draft','awaiting_dispatch','draft_dispatching'))
    def execute(self,i):
        self.c.act(i,'execute');deadline=time.monotonic()+3
        while time.monotonic()<deadline:
            j=self.c.act(i,'sync_execution')
            if j['stage']!='execution_waiting':return j
            time.sleep(.01)
        self.fail('executor did not finish')
    def test_work_budget_exhausted_still_completes_one_executor_call(self):
        i=self.job();self.exhaust_work()
        j=self.c.act(i,'begin_draft');self.assertEqual(j['stage'],'prompt_ready');self.assertIsNone(j['thread_id'])
        with patch('iald_orchestrator.providers.execute',return_value={'text':'2','usage':{}}) as call:
            self.assertEqual(self.execute(i)['stage'],'synthesis_ready')
            j=self.c.act(i,'begin_synthesis');self.assertEqual(j['stage'],'completed');self.assertEqual(j['synthesis_source'],'executor_direct')
            self.assertIn('sem revisão independente',j['final_text']);self.assertEqual(call.call_count,1)
            with self.assertRaises(ValueError):self.c.act(i,'execute')
        with self.r.db() as db:self.assertEqual(db.execute("SELECT count(*) FROM coordination_events WHERE action IN ('begin_draft','begin_synthesis')").fetchone()[0],3)
    def test_optional_local_preparation_preserves_original_and_constraints(self):
        i=self.job();j=self.c.act(i,'prepare_without_work',{'reason':'assistance_not_needed','prompt':'Apresente o cálculo.'})
        self.assertIn('Somar dois valores.',j['prepared_prompt']);self.assertEqual(j['execution_constraints']['required_provider'],'local');self.assertEqual(j['draft_source'],'iald_coordinator')
    def test_uncertain_work_dispatch_is_not_skipped(self):
        i=self.job();self.c.act(i,'begin_draft')
        with self.assertRaises(ValueError):self.c.act(i,'prepare_without_work',{'reason':'work_unavailable'})
        self.assertEqual(self.c.get(i)['stage'],'draft_dispatching')
    def test_confirmed_unavailable_work_can_be_released_without_new_call(self):
        from iald_orchestrator.coordination import PROJECT
        i=self.job();self.c.act(i,'begin_draft');self.c.act(i,'bind_thread',{'thread_id':str(uuid.uuid4()),'project_id':PROJECT})
        with self.assertRaises(ValueError):self.c.act(i,'prepare_without_work',{'reason':'work_unavailable'})
        j=self.c.act(i,'prepare_without_work',{'reason':'provider_limit_reported','evidence':'Official app reported usage limit for this turn.'})
        self.assertEqual(j['stage'],'prompt_ready');self.assertIsNotNone(j['thread_id'])
    def test_failed_executor_cannot_be_presented_as_local_completion(self):
        i=self.job();self.c.act(i,'prepare_without_work',{'reason':'assistance_not_needed'})
        with patch('iald_orchestrator.providers.execute',side_effect=TimeoutError) as call:
            self.assertEqual(self.execute(i)['stage'],'failed')
            with self.assertRaises(ValueError):self.c.act(i,'complete_without_work',{'reason':'work_unavailable','text':'false success'})
            self.assertEqual(call.call_count,1)
    def test_local_synthesis_can_label_its_own_review_without_work(self):
        i=self.job();self.c.act(i,'prepare_without_work',{'reason':'assistance_not_needed'})
        with patch('iald_orchestrator.providers.execute',return_value={'text':'2','usage':{}}):self.execute(i)
        j=self.c.act(i,'complete_without_work',{'reason':'assistance_not_needed','text':'Resposta revisada localmente: 2. Não houve revisão Work.'})
        self.assertEqual(j['stage'],'completed');self.assertEqual(j['synthesis_source'],'iald_coordinator')
    def test_cannot_invent_budget_exhaustion(self):
        i=self.job()
        with self.assertRaises(ValueError):self.c.act(i,'prepare_without_work',{'reason':'local_work_budget_reached'})
