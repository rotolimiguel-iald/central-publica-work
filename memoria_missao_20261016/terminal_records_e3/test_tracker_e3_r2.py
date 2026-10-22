"""Offline tracker tests: mocks never call the common memory or a provider."""
from support_e3 import *
import copy, contextlib, io, tempfile, unittest

sys.path.insert(0,str(OUT/'mission_resume_20261016'))
import track_build_r45 as tracker

class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.other=dict(id='provider-job',kind='provider',status='uncertain',request_id='original')
        self.pin=dict(path='fixture.json',sha256='a'*64)

    def test_preserves_other_handles_and_source(self):
        original=[copy.deepcopy(self.other)]
        value=tracker.update_handles(original,'stamp','R8','running',self.pin)
        self.assertEqual(original,[self.other])
        self.assertEqual(value[0],self.other)
        self.assertEqual(len(value),2)

    def test_idempotent_same_receipt(self):
        v=tracker.update_handles([], 'stamp','R8','completed',self.pin)
        self.assertEqual(v,tracker.update_handles(v,'stamp','R8','completed',self.pin))

    def test_no_terminal_reopen(self):
        v=tracker.update_handles([], 'stamp','R8','completed',self.pin)
        for status in ['running','failed','terminated']:
            with self.subTest(status=status),self.assertRaises(ValueError):
                tracker.update_handles(v,'stamp','R8',status,self.pin)

    def test_changed_pin_refused(self):
        v=tracker.update_handles([], 'stamp','R8','running',self.pin)
        with self.assertRaises(ValueError):
            tracker.update_handles(v,'stamp','R8','running',dict(path='fixture.json',sha256='b'*64))

    def test_duplicate_and_wrong_task_refused(self):
        v=tracker.update_handles([], 'stamp','R8','running',self.pin)
        with self.assertRaises(ValueError):tracker.update_handles(v+v,'stamp','R8','running',self.pin)
        with self.assertRaises(ValueError):tracker.update_handles(v,'stamp','R7','running',self.pin)

    def test_foreign_and_uncertain_states_refused(self):
        for prior in ['done','cancelled','closed','accepted','returned','uncertain',None,'unknown']:
            h=dict(id='build-stamp',kind='lean_build',task_id='R8',status=prior)
            with self.subTest(prior=prior),self.assertRaises(ValueError):
                tracker.update_handles([h],'stamp','R8','running',self.pin)

    def test_conflicting_phase_refused(self):
        h=dict(id='build-stamp',kind='lean_build',task_id='R8',status='completed',phase='running')
        with self.assertRaises(ValueError):tracker.update_handles([h],'stamp','R8','completed',self.pin)

    def test_phase_transitions_atomically(self):
        h=dict(id='build-stamp',kind='lean_build',task_id='R8',status='running',phase='running')
        v=tracker.update_handles([h],'stamp','R8','completed',self.pin)
        self.assertEqual(v[0]['status'],'completed')
        self.assertEqual(v[0]['phase'],'completed')
        self.assertEqual(h['phase'],'running')

    def test_real_main_writes_only_flow(self):
        saved_out, saved_call, saved_argv=tracker.OUT,tracker.live.call,sys.argv
        calls=[]
        state=dict(revision=9,p=dict(handles=[self.other]))
        def mock_call(cli,payload,name):
            calls.append(copy.deepcopy(payload))
            return (copy.deepcopy(state) if payload['operation']=='get' else {'revision':10}),Path('mock.json')
        try:
            with tempfile.TemporaryDirectory(dir=BASE,prefix='tracker_test_') as directory:
                tracker.OUT=Path(directory)
                attempt=tracker.OUT/'orbital_rotation/attempts/stamp'
                attempt.mkdir(parents=True)
                (attempt/'RECEIPT.json').write_text('{"exit_code":0}',encoding='utf-8')
                tracker.live.call=mock_call
                sys.argv=['tracker','stamp','R8','completed']
                with contextlib.redirect_stdout(io.StringIO()):tracker.main()
                self.assertEqual(set(calls[-1]['changes']),{'flow'})
                self.assertEqual(calls[-1]['changes']['flow']['handles'][0],self.other)
                self.assertEqual(calls[-1]['expected_revision'],9)
                self.assertEqual(len(calls),2)
        finally:
            tracker.OUT,tracker.live.call,sys.argv=saved_out,saved_call,saved_argv

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TrackerTests))
    new('TRACKER_TEST_RESULTS_E3_R2.json',dict(ok=result.wasSuccessful(),tests=result.testsRun,
        failures=len(result.failures),errors=len(result.errors),tracker=pin(Path(tracker.__file__)),
        test=pin(Path(__file__)),providers_called=False,real_memory_called=False))
    if not result.wasSuccessful():raise SystemExit(1)
