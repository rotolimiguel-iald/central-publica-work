import tempfile, threading, time, unittest, uuid
from unittest.mock import patch
from urllib.parse import parse_qs,urlparse
from iald_orchestrator.coordination import Coordination,PROJECT
from iald_orchestrator.runtime import Runtime
from test_orchestrator import connections

class CoordinationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.runtime=Runtime(self.tmp.name)
        self.c=Coordination(self.runtime)
        self.patches=[patch('iald_orchestrator.providers.discover',return_value=connections())]
        for p in self.patches:p.start()
    def tearDown(self):
        for p in self.patches:p.stop()
        with self.runtime.worker_lock:pass
        self.tmp.cleanup()
    def job(self):return self.c.create('Escreva uma função de soma em Python.',str(uuid.uuid4()))
    def ready(self):
        j=self.job();i=j['id'];self.c.act(i,'begin_draft')
        self.c.act(i,'bind_thread',{'thread_id':str(uuid.uuid4()),'project_id':PROJECT})
        self.c.act(i,'accept_prompt',{'prompt':'Sem inventar prova: escreva def add(a,b): return a+b.'})
        return i
    def wait(self,i):
        deadline=time.monotonic()+5
        while time.monotonic()<deadline:
            j=self.c.act(i,'sync_execution')
            if j['stage']!='execution_waiting':return j
            time.sleep(.01)
        self.fail('worker failed to settle')
    def test_idempotent_button_contains_no_original_prompt_in_url(self):
        rid=str(uuid.uuid4());a=self.c.create('PRIVATE TEST CONTENT',rid);b=self.c.create('PRIVATE TEST CONTENT',rid)
        self.assertEqual(a['id'],b['id']);self.assertNotIn('PRIVATE',a['codex_url'])
        url=urlparse(a['codex_url']);self.assertEqual(url.scheme,'codex')
        self.assertIn(a['id'],parse_qs(url.query)['prompt'][0])
        self.assertIsInstance(a['automatic_polling'],bool)
        with self.assertRaises(ValueError):self.c.create('different',rid)
    def test_claim_and_project_binding_are_fail_closed(self):
        i=self.job()['id'];self.c.act(i,'begin_draft')
        with self.assertRaises(ValueError):self.c.act(i,'begin_draft')
        with self.assertRaises(ValueError):self.c.act(i,'bind_thread',{'thread_id':str(uuid.uuid4()),'project_id':'wrong'})
        with self.assertRaises(ValueError):self.c.act(i,'complete',{'text':'premature'})
    def test_full_lifecycle_preserves_original_classification_and_single_execution(self):
        i=self.ready()
        with patch('iald_orchestrator.providers.execute',return_value={'text':'def add(a,b): return a+b','usage':{'input_tokens':10},'elapsed_seconds':.1}) as run:
            self.c.act(i,'execute')
            with self.assertRaises(ValueError):self.c.act(i,'execute')
            j=self.wait(i);self.assertEqual(j['stage'],'synthesis_ready')
            self.assertEqual(j['execution']['decision']['selected'],'local')
            self.assertEqual(run.call_count,1)
            self.assertIn('PEDIDO DO OPERADOR',run.call_args.args[1])
            self.c.act(i,'begin_synthesis');self.c.act(i,'synthesis_sent')
            done=self.c.act(i,'complete',{'text':'Resposta final conferida quanto ao texto.'})
            self.assertEqual(done['stage'],'completed')
            self.assertEqual(self.c.act(i,'cancel')['stage'],'completed')
    def test_cancel_during_dispatch_prevents_model_call(self):
        i=self.ready();original=self.runtime.submit
        def racing_submit(*args,**kw):
            task=original(*args,**kw);self.c.act(i,'cancel');return task
        with patch.object(self.runtime,'submit',side_effect=racing_submit),patch('iald_orchestrator.providers.execute') as run:
            with self.assertRaises(ValueError):self.c.act(i,'execute')
            self.assertEqual(run.call_count,0)
            self.assertEqual(self.c.get(i)['stage'],'cancelled')
            with self.runtime.db() as db:self.assertEqual(db.execute('SELECT status FROM tasks').fetchone()[0],'cancelled')
    def test_two_runtimes_share_serial_execution_and_recovery_does_not_interrupt(self):
        second=Runtime(self.tmp.name,recover=False);entered=threading.Event();release=threading.Event()
        running=[];peak=[0];lock=threading.Lock()
        def execute(*args,**kw):
            with lock:running.append(1);peak[0]=max(peak[0],len(running))
            entered.set();self.assertTrue(release.wait(4))
            with lock:running.pop()
            return {'text':'ok','usage':{},'elapsed_seconds':.1}
        with patch('iald_orchestrator.providers.execute',side_effect=execute):
            a=self.runtime.submit('Soma um.',str(uuid.uuid4()));self.assertTrue(entered.wait(3))
            recovery=Runtime(self.tmp.name)
            self.assertEqual(recovery.task(a['id'])['status'],'running')
            b=second.submit('Soma dois.',str(uuid.uuid4()));release.set()
            deadline=time.monotonic()+5
            while time.monotonic()<deadline and second.task(b['id'])['status'] in ('running','queued'):time.sleep(.01)
            with second.worker_lock:pass
            self.assertEqual(second.task(b['id'])['status'],'result_ready');self.assertEqual(peak[0],1)
    def test_failed_execution_never_creates_synthesis(self):
        i=self.ready()
        with patch('iald_orchestrator.providers.execute',side_effect=RuntimeError('Visible failure')):
            self.c.act(i,'execute');self.assertEqual(self.wait(i)['stage'],'failed')
            with self.assertRaises(ValueError):self.c.act(i,'begin_synthesis')

if __name__=='__main__':unittest.main(verbosity=2)
