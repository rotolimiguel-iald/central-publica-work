"""Independent regression and handoff tests on isolated ACOM state."""
from pathlib import Path
import concurrent.futures, copy, hashlib, importlib.util, json, subprocess, sys, threading, unittest, uuid
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'lib'))
from iald_memory import MemoryStore
from iald_memory.mission import MissionController, MissionError, KEY, PROTOCOL, evidence_pin
SCOPE = {'house': 'IALD', 'principal': 'review-r2'}
AGENT = {'id': 'builder', 'kind': 'agent'}
REVIEWER = {'id': 'reviewer', 'kind': 'agent'}
MODEL = {'id': 'model', 'kind': 'model'}

class Checks(unittest.TestCase):
    def setUp(self):
        self.root = ROOT / ('case_' + uuid.uuid4().hex)
        self.root.mkdir()
        self.store = MemoryStore(self.root / 'state')
        self.cid = str(uuid.uuid4())
        self.snap = self.store.ensure_context(self.cid, objective='Preserve all obligations.', scope=SCOPE, actor=AGENT)
        self.file = self.root / 'fixture.txt'
        self.file.write_bytes(b'review fixture')
        self.pin = {'path': str(self.file), 'sha256': hashlib.sha256(self.file.read_bytes()).hexdigest()}
        self.ctl = MissionController(self.store, self.cid, SCOPE)
        self.ctl.action({'operation': 'configure', 'actor': AGENT, 'event_id': 'configure', 'expected_revision': 0,
                         'requirements': [{'id': 'A', 'criterion': 'independent review', 'depends_on': []}],
                         'sources': [self.pin]})
    def req(self, op, **kw):
        p = self.ctl.project()
        return {'operation': op, 'task_id': 'A', 'actor': AGENT, 'event_id': str(uuid.uuid4()),
                'expected_revision': p['receipt']['revision'], 'projection_sha256': p['projection_sha256'],
                'state_sha256': p['receipt']['state_sha256'], **kw}
    def record(self, actor, **kw):
        revision = self.store.receipt(self.cid, SCOPE)['revision']
        self.store.transition(self.cid, SCOPE, revision, str(uuid.uuid4()), actor, {'records': [kw]})
    def test_candidate_metadata_does_not_execute(self):
        snap, state, prev = self.ctl.load()
        task = copy.deepcopy(state['tasks']['A'])
        task.update(status='satisfied', evidence=[self.pin], review_evidence=[self.pin], submitted_by='model', reviewed_by='model')
        self.record(MODEL, id='candidate', kind='candidate', statute='DECLARADO', text='Proposed completion.',
                    sources=[{'kind': 'model', 'ref': 'local-test'}], supersedes=prev,
                    meta={KEY: {'protocol': PROTOCOL, 'tasks': {'A': task}}})
        p = self.ctl.project()['projection']
        self.assertFalse(p['tetelestai'])
        self.assertEqual(p['active'][0]['status'], 'open')
        self.assertEqual(p['current_records'][0]['id'], 'candidate')
    def instruction(self):
        self.record(AGENT, id='instruction', kind='decision', statute='INPUT',
                    text='No external calls. Review is due Friday.',
                    sources=[{'kind': 'artifact', 'ref': str(self.file), 'sha256': self.pin['sha256']}])
    def test_candidate_preserves_instruction(self):
        self.instruction()
        self.record(MODEL, id='candidate', kind='candidate', statute='DECLARADO', text='Candidate change.',
                    sources=[{'kind': 'model', 'ref': 'local-test'}], supersedes='instruction')
        self.assertIn('No external calls.', json.dumps(self.ctl.project()['projection']))
    def test_partial_erratum_preserves_instruction(self):
        self.instruction()
        self.record(AGENT, id='erratum', kind='erratum', statute='INPUT', text='Correction: review due Monday.',
                    sources=[{'kind': 'artifact', 'ref': str(self.file), 'sha256': self.pin['sha256']}], supersedes='instruction')
        p = self.ctl.project()['projection']
        (self.root / 'ERRATUM_OBSERVATION.json').write_bytes(json.dumps({'mission': p,
            'acom': self.store.project(self.cid, SCOPE)['text']}, indent=2).encode('utf-8'))
        self.assertIn('No external calls.', json.dumps(p))
    def test_flow_preserved(self):
        self.store.transition(self.cid, SCOPE, 1, 'flow', AGENT, {'flow': {
            'phase': 'uncertain', 'next_action': 'Reconcile.', 'handles': [{'id': 'req-1', 'job_id': 'job-1'}]}})
        self.assertEqual(self.ctl.project()['projection']['flow'], self.store.get(self.cid, SCOPE)['p'])
    def test_duplicate_concurrent_request(self):
        request = self.req('claim'); barrier = threading.Barrier(2)
        def run(_):
            store = MemoryStore(self.root / 'state'); original = store.transition
            def wrapped(*args, **kwargs):
                barrier.wait(timeout=10)
                return original(*args, **kwargs)
            store.transition = wrapped
            return MissionController(store, self.cid, SCOPE).action(copy.deepcopy(request))
        with concurrent.futures.ThreadPoolExecutor(2) as pool:
            results = list(pool.map(run, range(2)))
        self.assertEqual(sum(r['replayed'] for r in results), 1)
        self.assertEqual(self.store.receipt(self.cid, SCOPE)['revision'], 2)
    def test_oversized_prefix_refused(self):
        path = ROOT.parent / 'review_core_r1' / 'oversized_evidence.bin'
        with path.open('rb') as stream:
            prefix = hashlib.sha256(stream.read(64 * 1024 * 1024 + 1)).hexdigest()
        with self.assertRaisesRegex(MissionError, 'evidence_too_large'):
            evidence_pin({'path': str(path), 'sha256': prefix})
    def test_handoff_snapshot_and_stale_rejection(self):
        lease = self.ctl.action(self.req('claim'))['task']['lease']['id']
        request = self.req('handoff', reference='exact-review-reference', lease_id=lease)
        result = self.ctl.handoff(request)
        self.assertEqual(result['reference'], request['reference'])
        self.assertEqual(result['preflight']['receipt'], result['receipt'])
        self.assertEqual(result['preflight']['projection_sha256'], result['projection_sha256'])
        self.ctl.action(self.req('hold', hold=True, reason='pause', sources=[self.pin]))
        with self.assertRaisesRegex(MissionError, 'stale_revision'):
            self.ctl.handoff(request)
    def test_pause_acceptance(self):
        lease = self.ctl.action(self.req('claim'))['task']['lease']['id']
        self.ctl.action(self.req('hold', hold=True, reason='pause', sources=[self.pin]))
        self.ctl.action(self.req('submit', lease_id=lease, evidence=[self.pin]))
        with self.assertRaisesRegex(MissionError, 'mission_on_hold'):
            self.ctl.action(self.req('accept', actor=REVIEWER, review_evidence=[self.pin]))
    def test_bridge_delegates_to_real_isolated_cli(self):
        spec = importlib.util.spec_from_file_location('review_bridge', ROOT / 'mission_bridge.py')
        bridge = importlib.util.module_from_spec(spec); spec.loader.exec_module(bridge)
        reference = self.root / 'REFERENCE.json'
        reference.write_bytes(json.dumps({'protocol': 'iald-memory-session/v1', 'store': str(self.root / 'state'),
            'context_id': self.cid, 'scope': SCOPE, 'objective_sha256': self.snap['objective_sha256']}).encode('utf-8'))
        class Server:
            def __init__(self): self.methods = {}
            def tool(self):
                def wrap(fn): self.methods[fn.__name__] = fn; return fn
                return wrap
        server = Server(); bridge.register_tools(server)
        self.assertEqual(len(server.methods), 4)
        real_run = subprocess.run
        def isolated_run(args, **kwargs):
            return real_run([sys.executable, '-B', '-X', 'utf8', str(ROOT / 'mission_cli.py'),
                '--core-root', str(ROOT / 'lib'), '--store', str(self.root / 'state'),
                '--session-adapter', r'C:\IALD\MEMORIA_IALD\session_memory.py'], **kwargs)
        with patch.object(bridge.subprocess, 'run', side_effect=isolated_run):
            result = server.methods['iald_mission_sync'](str(reference))
            self.assertEqual(result, self.ctl.project())
            lease = self.ctl.action(self.req('claim'))['task']['lease']['id']
            request = self.req('handoff', reference=str(reference), lease_id=lease)
            handoff = server.methods['iald_mission_handoff'](str(reference), 'A', 'builder', lease,
                request['expected_revision'], request['projection_sha256'])
            self.assertEqual(handoff['preflight']['receipt'], handoff['receipt'])
            with self.assertRaisesRegex(ValueError, 'reference_scope_mismatch'):
                bridge.invoke({'operation': 'project', 'reference': str(reference),
                    'scope': {'house': 'IALD', 'principal': 'other'}})

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Checks)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    (ROOT / 'INDEPENDENT_TEST_RESULT.json').write_bytes(json.dumps({
        'run': result.testsRun, 'failures': [(str(t), msg) for t, msg in result.failures],
        'errors': [(str(t), msg) for t, msg in result.errors]}, indent=2).encode('utf-8'))
    raise SystemExit(not result.wasSuccessful())
