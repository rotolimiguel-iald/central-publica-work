"""TX-01 R2: fake psutil processes and HTTP only; writes stay in test fixtures."""
from pathlib import Path
from contextlib import contextmanager
import hashlib, importlib.util, io, json, os, sys, types, unittest
from unittest.mock import Mock, patch
sys.dont_write_bytecode=True
V=Path(__file__).resolve().parent;W=V.parent
FIX=V/'tx01_r2_fixtures';FIX.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
INPUTS={str(W/n):sha((W/n).read_bytes()) for n in ('install_plan.json','maintenance.py','transaction.py','deploy_controlled.py')}
def guard(event,args):
    if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):raise RuntimeError('Real external operations forbidden')
    if event=='open':
        p,mode,flags=args
        if isinstance(p,int):return
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and not Path(p).resolve().is_relative_to(V):raise RuntimeError('Write outside validation')
    if event in ('os.remove','os.mkdir','os.rmdir','os.rename'):
        for p in args[:2] if event=='os.rename' else args[:1]:
            if isinstance(p,(str,bytes)) and not Path(os.fsdecode(p)).resolve().is_relative_to(V):raise RuntimeError('Mutation outside validation')
sys.addaudithook(guard)

class Gone(Exception):pass
class FakeProcess:
    def __init__(self,env,pid,name,script,parent=None):
        self.env=env;self.pid=pid;self.info={'name':name};self.script=script;self.parent_proc=parent
        self.created=float(pid);self.state='running';self.alive=True;self.extra=[];self.fail=None
    def cmdline(self):return [self.info['name'],str(self.script),*self.extra]
    def parent(self):return self.parent_proc
    def ppid(self):return self.parent_proc.pid
    def create_time(self):return self.created
    def status(self):return self.state
    def suspend(self):
        self.env.log.append(('suspend',self.pid))
        if self.fail=='suspend':raise RuntimeError('suspend failure')
        self.state='stopped'
    def resume(self):
        self.env.log.append(('resume',self.pid))
        if not self.alive:raise Gone()
        self.state='running'
    def terminate(self):
        self.env.log.append(('terminate',self.pid))
        if self.fail=='terminate':raise RuntimeError('terminate failure')
        self.alive=False
    def wait(self,timeout):
        self.env.log.append(('wait',self.pid))
        if self.fail=='wait':raise RuntimeError('wait failure')
        return 0

class Environment:
    def __init__(self):
        self.root=Path('C:/IALD/projetos_pyhton/IALD');self.log=[];self.port_override=None
        self.parent=FakeProcess(self,10,'powershell.exe',self.root/'start_iald_web.ps1')
        self.child=FakeProcess(self,20,'python.exe',self.root/'iald_web_server.py',self.parent)
        self.others=[FakeProcess(self,30,'llama-server.exe',self.root/'llama-server.exe'),
                     FakeProcess(self,40,'python.exe',self.root/'bancada.py'),
                     FakeProcess(self,50,'cloudflared.exe',self.root/'cloudflared.exe')]
        self.processes=[self.parent,self.child,*self.others]
        self.ps=types.ModuleType('psutil');self.ps.NoSuchProcess=Gone
        self.ps.STATUS_STOPPED='stopped';self.ps.CONN_LISTEN='LISTEN'
        self.ps.process_iter=lambda attrs:[p for p in self.processes if p.alive]
        self.ps.net_connections=lambda kind:self.listeners()
    def listeners(self):
        pids=self.port_override
        if pids is None:pids=[p.pid for p in self.processes if p.alive and p.script==self.root/'iald_web_server.py']
        return [types.SimpleNamespace(status='LISTEN',laddr=types.SimpleNamespace(port=8082),pid=p) for p in pids]
    def quiet(self):
        self.log.append(('quiet',None))
        assert self.parent.state==self.child.state=='stopped'
    def admissions_possible(self):return any(p.alive and p.state=='running' and p.script==self.root/'iald_web_server.py' for p in self.processes)

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class MaintenanceR2(unittest.TestCase):
    def setUp(self):
        self.env=Environment();self.mods=patch.dict(sys.modules,{'psutil':self.env.ps});self.mods.start();self.addCleanup(self.mods.stop)
        self.m=module('maintenance',W/'maintenance.py')
        self.mm=patch.dict(sys.modules,{'maintenance':self.m});self.mm.start();self.addCleanup(self.mm.stop)
        self.tx=module('transaction',W/'transaction.py')
    def tearDown(self):
        self.assertFalse(any(pid in (30,40,50) for action,pid in self.env.log))
    def test_success_freezes_before_quiet_and_resumes_same_parent(self):
        with self.m.stopped_web(self.env.quiet) as identity:
            self.m.assert_quiesced();self.assertFalse(self.env.admissions_possible())
            self.assertEqual(identity['supervisor_created'],10.0)
        self.assertEqual(self.env.log[:3],[('suspend',10),('suspend',20),('quiet',None)])
        self.assertEqual(self.env.log[-1],('resume',10));self.assertFalse(self.env.child.alive)
        self.assertIsNone(self.m._active)
    def test_busy_or_unreadable_frozen_ledger_resumes_both(self):
        def busy():self.env.quiet();raise RuntimeError('active job or unreadable ledger')
        with self.assertRaises(RuntimeError):
            with self.m.stopped_web(busy):self.fail('window must not open')
        self.assertTrue(self.env.child.alive);self.assertEqual(self.env.child.state,'running');self.assertEqual(self.env.parent.state,'running')
        self.assertNotIn(('terminate',20),self.env.log)
    def test_body_failure_still_resumes_supervisor(self):
        with self.assertRaisesRegex(RuntimeError,'fixture'):
            with self.m.stopped_web(self.env.quiet):raise RuntimeError('fixture')
        self.assertEqual(self.env.parent.state,'running');self.assertIsNone(self.m._active)
    def test_child_suspend_failure_resumes_parent(self):
        self.env.child.fail='suspend'
        with self.assertRaises(RuntimeError):
            with self.m.stopped_web(self.env.quiet):pass
        self.assertEqual(self.env.parent.state,'running');self.assertNotIn(('terminate',20),self.env.log)
    def test_termination_failure_resumes_both(self):
        self.env.child.fail='terminate'
        with self.assertRaises(RuntimeError):
            with self.m.stopped_web(self.env.quiet):pass
        self.assertEqual(self.env.parent.state,'running');self.assertEqual(self.env.child.state,'running')
    def test_bad_supervisor_no_mutation(self):
        self.env.parent.script=self.env.root/'wrong.ps1'
        with self.assertRaises(RuntimeError):
            with self.m.stopped_web(self.env.quiet):pass
        self.assertEqual(self.env.log,[])
    def test_no_supervise_refused(self):
        self.env.parent.extra=['-NoSupervise']
        with self.assertRaises(RuntimeError):
            with self.m.stopped_web(self.env.quiet):pass
        self.assertEqual(self.env.log,[])
    def test_wrong_listener_refused(self):
        self.env.port_override=[999]
        with self.assertRaises(RuntimeError):
            with self.m.stopped_web(self.env.quiet):pass
        self.assertEqual(self.env.log,[])
    def test_duplicate_web_refused(self):
        self.env.processes.append(FakeProcess(self.env,21,'python.exe',self.env.child.script,self.env.parent))
        with self.assertRaises(RuntimeError):
            with self.m.stopped_web(self.env.quiet):pass
        self.assertEqual(self.env.log,[])
    def test_no_context_refused_before_plan_read(self):
        with self.assertRaisesRegex(RuntimeError,'No controlled'):
            self.tx.apply_plan(FIX/'does_not_exist.json')
    def test_nested_context_refused(self):
        with self.m.stopped_web(self.env.quiet):
            with self.assertRaisesRegex(RuntimeError,'Nested'):
                with self.m.stopped_web(self.env.quiet):pass
    def test_guard_rejects_creationtime_status_new_web_and_port(self):
        with self.m.stopped_web(self.env.quiet):
            self.env.parent.created=11
            with self.assertRaises(RuntimeError):self.m.assert_quiesced()
            self.env.parent.created=10;self.env.parent.state='running'
            with self.assertRaises(RuntimeError):self.m.assert_quiesced()
            self.env.parent.state='stopped';self.env.child.alive=True
            with self.assertRaises(RuntimeError):self.m.assert_quiesced()
            self.env.child.alive=False;self.env.port_override=[999]
            with self.assertRaises(RuntimeError):self.m.assert_quiesced()
    def fixture(self):
        base=FIX/self._testMethodName;root=base/'runtime';work=base/'work';root.mkdir(parents=True);(work/'validation').mkdir(parents=True)
        rows=[]
        for name in ('a.txt','b.txt'):
            (root/name).write_bytes(b'old');(work/name).write_bytes(b'new')
            rows.append({'source':str(work/name),'destination':str(root/name),'sha256':sha(b'new'),'baseline':sha(b'old')})
        path=work/'plan.json';path.write_text(json.dumps({'files':rows}));pin=sha(path.read_bytes())
        (work/'validation/final_checks.json').write_text(json.dumps({'passed':True,'plan_sha256':pin}))
        (work/'validation/review_final.json').write_text(json.dumps({'status':'PASS','plan_sha256':pin}))
        return root,work,path
    def test_transaction_closes_original_admission_race(self):
        root,work,path=self.fixture();attempts=[];atomic=self.tx.atomic
        def write(p,raw):
            attempts.append(self.env.admissions_possible());atomic(p,raw)
        with patch.object(self.tx,'ROOT',root),patch.object(self.tx,'WORK',work),patch.object(self.tx,'quiet'),patch.object(self.tx,'atomic',side_effect=write):
            with self.m.stopped_web(self.env.quiet):receipt=self.tx.apply_plan(path)
        self.assertEqual(receipt['status'],'INSTALLED_RESTART_REQUIRED');self.assertFalse(any(attempts))
        self.assertEqual((root/'a.txt').read_bytes(),b'new')
    def test_guard_failure_after_writes_rolls_back(self):
        root,work,path=self.fixture();atomic=self.tx.atomic
        def write(p,raw):
            atomic(p,raw)
            if Path(p)==root/'b.txt' and raw==b'new':self.env.port_override=[999]
        with patch.object(self.tx,'ROOT',root),patch.object(self.tx,'WORK',work),patch.object(self.tx,'quiet'),patch.object(self.tx,'atomic',side_effect=write):
            with self.assertRaises(RuntimeError):
                with self.m.stopped_web(self.env.quiet):self.tx.apply_plan(path)
        self.assertEqual((root/'a.txt').read_bytes(),b'old');self.assertEqual((root/'b.txt').read_bytes(),b'old')
        self.assertFalse((work/'deployment.json').exists());self.assertEqual(self.env.parent.state,'running')
    def test_guard_before_writes_rejects_resumed_parent(self):
        root,work,path=self.fixture();backup=self.tx.backup
        def save(p,stamp):
            value=backup(p,stamp);self.env.parent.state='running';return value
        with patch.object(self.tx,'ROOT',root),patch.object(self.tx,'WORK',work),patch.object(self.tx,'quiet'),patch.object(self.tx,'backup',side_effect=save):
            with self.assertRaises(RuntimeError):
                with self.m.stopped_web(self.env.quiet):self.tx.apply_plan(path)
        self.assertEqual((root/'a.txt').read_bytes(),b'old');self.assertEqual((root/'b.txt').read_bytes(),b'old')
    def restart(self,status=200,wrong_parent=False,wrong_port=False):
        self.env.child.alive=False
        child=FakeProcess(self.env,21,'python.exe',self.env.child.script,self.env.parent);self.env.processes.append(child)
        if wrong_parent:self.env.parent.created=11
        if wrong_port:self.env.port_override=[999]
        conn=Mock();conn.getresponse.return_value=types.SimpleNamespace(status=status,read=lambda:b'')
        identity={'old_web_pid':20,'supervisor_pid':10,'supervisor_created':10.0}
        with patch('http.client.HTTPConnection',return_value=conn),patch.object(self.m.time,'sleep'),patch.object(self.m.time,'monotonic',side_effect=[0,0,2]):
            return self.m.await_restart(identity,timeout=1)
    def test_restart_checks_http_listener_and_same_parent(self):
        self.assertEqual(self.restart()['new_web_pid'],21)
    def test_restart_refuses_wrong_creationtime(self):
        with self.assertRaisesRegex(RuntimeError,'identity'):self.restart(wrong_parent=True)
    def test_restart_refuses_wrong_listener(self):
        with self.assertRaisesRegex(RuntimeError,'not verified'):self.restart(wrong_port=True)
    def test_restart_refuses_http_failure(self):
        with self.assertRaisesRegex(RuntimeError,'not verified'):self.restart(status=500)
    def wrapper(self):
        with patch.dict(sys.modules,{'transaction':self.tx,'maintenance':self.m}):return module('controlled_wrapper',W/'deploy_controlled.py')
    def wrapper_fixture(self):
        work=FIX/self._testMethodName; (work/'validation').mkdir(parents=True)
        for n in ('transaction.py','maintenance.py','install_plan.json'):(work/n).write_bytes((W/n).read_bytes())
        review={'status':'PASS',**{key:sha((work/n).read_bytes()) for key,n in (('transaction_sha256','transaction.py'),('maintenance_sha256','maintenance.py'),('plan_sha256','install_plan.json'))}}
        (work/'validation/review_final.json').write_text(json.dumps(review));return work
    def test_wrapper_refuses_each_changed_hash_before_process_access(self):
        work=self.wrapper_fixture();wrapper=self.wrapper()
        for n in ('transaction.py','maintenance.py','install_plan.json'):
            original=(work/n).read_bytes();(work/n).write_bytes(original+b' ')
            with patch.object(wrapper,'W',work),patch.object(wrapper,'quiet') as quiet,patch.object(wrapper,'stopped_web') as stopped:
                with self.assertRaises(AssertionError):wrapper.main()
                quiet.assert_not_called();stopped.assert_not_called()
            (work/n).write_bytes(original)
    def test_wrapper_apply_exception_resumes_then_verifies_restart(self):
        work=self.wrapper_fixture();wrapper=self.wrapper();events=[]
        @contextmanager
        def stopped(q):
            events.append('freeze');yield {'old_web_pid':20,'supervisor_pid':10,'supervisor_created':10}
        @contextmanager
        def stopped_finally(q):
            try:
                with stopped(q) as identity:yield identity
            finally:events.append('resume')
        def restart(identity):events.append('restart');return {'status':'PASS'}
        with patch.object(wrapper,'W',work),patch.object(wrapper,'quiet'),patch.object(wrapper,'stopped_web',side_effect=stopped_finally),patch.object(wrapper,'apply_plan',side_effect=RuntimeError('apply failed')),patch.object(wrapper,'await_restart',side_effect=restart),patch.object(wrapper,'write_evidence'):
            with self.assertRaisesRegex(RuntimeError,'apply failed'):wrapper.main()
        self.assertEqual(events,['freeze','resume','restart'])

if __name__=='__main__':
    out=io.StringIO();result=unittest.TextTestRunner(stream=out,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(MaintenanceR2))
    assert all(sha(Path(p).read_bytes())==h for p,h in INPUTS.items())
    (V/'tx01_r2_output.txt').write_text(out.getvalue(),encoding='utf8')
    report={'passed':result.wasSuccessful(),'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'inputpins':INPUTS,'real_process_operations':0,'network_calls':0,'production_writes':0}
    (V/'tx01_r2_tests.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    print(out.getvalue());sys.exit(not result.wasSuccessful())
