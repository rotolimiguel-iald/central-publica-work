"""Independent adversarial checks; all state stays in this review folder."""
from pathlib import Path
import concurrent.futures, copy, hashlib, json, sys, tempfile, threading, uuid

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'lib'))
from iald_memory import MemoryStore
from iald_memory.mission import MissionController, KEY, PROTOCOL

SCOPE = {'house': 'IALD', 'principal': 'independent-adversarial-review'}
AGENT = {'id': 'builder', 'kind': 'agent'}
REVIEWER = {'id': 'reviewer', 'kind': 'agent'}
MODEL = {'id': 'untrusted-model', 'kind': 'model'}
observations = []


class Case:
    def __init__(self, name):
        self.root = ROOT / name
        self.root.mkdir()
        self.store = MemoryStore(self.root / 'state')
        self.cid = str(uuid.uuid4())
        self.store.ensure_context(self.cid, objective='Review fixture: preserve original mission.',
                                  scope=SCOPE, actor=AGENT)
        self.file = self.root / 'evidence.txt'
        self.file.write_bytes(b'independently reproducible fixture')
        self.pin = {'path': str(self.file), 'sha256': hashlib.sha256(self.file.read_bytes()).hexdigest()}
        self.ctl = MissionController(self.store, self.cid, SCOPE)
        self.ctl.action({'operation': 'configure', 'actor': AGENT, 'event_id': 'configure',
                         'expected_revision': 0, 'requirements': [
                             {'id': 'A', 'criterion': 'Artifact has independent review.', 'depends_on': []}],
                         'sources': [self.pin]})

    def req(self, op, **extras):
        projection = self.ctl.project()
        return {'operation': op, 'task_id': 'A', 'actor': AGENT, 'event_id': str(uuid.uuid4()),
                'expected_revision': projection['receipt']['revision'],
                'projection_sha256': projection['projection_sha256'],
                'state_sha256': projection['receipt']['state_sha256'], **extras}

    def claim(self):
        return self.ctl.action(self.req('claim'))['task']['lease']['id']


case = Case('candidate_delta')
snapshot, state, previous = case.ctl.load()
task = copy.deepcopy(state['tasks']['A'])
task.update(status='satisfied', evidence=[case.pin], review_evidence=[case.pin],
            submitted_by=MODEL['id'], reviewed_by=MODEL['id'])
case.store.transition(case.cid, SCOPE, snapshot['revision'], 'model-injected', MODEL, {'records': [{
    'id': 'model-injected', 'kind': 'candidate', 'statute': 'DECLARADO',
    'text': 'A candidate proposing completion; this is not an authorized state transition.',
    'sources': [{'kind': 'model', 'ref': 'synthetic-local-model'}], 'supersedes': previous,
    'meta': {KEY: {'protocol': PROTOCOL, 'tasks': {'A': task}}}}]})
projection = case.ctl.project()['projection']
observations.append({'case': 'model_candidate_changes_operational_state',
                     'tetelestai': projection['tetelestai'],
                     'status': projection['settled'][0]['status'],
                     'same_submitter_and_reviewer': projection['settled'][0]['submitted_by'] == projection['settled'][0]['reviewed_by'],
                     'candidate_visible_in_current_records': bool(projection['current_records'])})

case = Case('correction_candidate')
revision = case.store.receipt(case.cid, SCOPE)['revision']
case.store.transition(case.cid, SCOPE, revision, 'instruction', AGENT, {'records': [{
    'id': 'human-order', 'kind': 'decision', 'statute': 'INPUT',
    'text': 'Do not call a provider until job J is reconciled.',
    'sources': [{'kind': 'artifact', 'ref': str(case.file), 'sha256': case.pin['sha256']}]}]})
case.store.transition(case.cid, SCOPE, revision + 1, 'candidate-correction', MODEL, {'records': [{
    'id': 'model-correction', 'kind': 'candidate', 'statute': 'DECLARADO',
    'text': 'Candidate: proceed normally.', 'supersedes': 'human-order',
    'sources': [{'kind': 'model', 'ref': 'synthetic-local-model'}]}]})
projection = case.ctl.project()['projection']
observations.append({'case': 'candidate_supersedes_mandatory_instruction',
                     'current_record_ids': [r['id'] for r in projection['current_records']],
                     'original_instruction_preserved_in_projection': 'Do not call a provider' in json.dumps(projection),
                     'original_preserved_in_acom_projection': 'Do not call a provider' in case.store.project(case.cid, SCOPE)['text']})

case = Case('flow_handles')
revision = case.store.receipt(case.cid, SCOPE)['revision']
case.store.transition(case.cid, SCOPE, revision, 'uncertain-dispatch', AGENT, {'flow': {
    'phase': 'dispatch_uncertain', 'next_action': 'Reconcile request before any repeat.',
    'handles': [{'id': 'request-123', 'job_id': 'job-123', 'status': 'dispatch_uncertain'}]}})
projection = case.ctl.project()['projection']
observations.append({'case': 'operational_flow_omitted_from_projection',
                     'has_flow': 'flow' in projection,
                     'has_uncertain_job': 'job-123' in json.dumps(projection),
                     'stored_p': case.store.get(case.cid, SCOPE)['p']})

case = Case('concurrent_idempotency')
request = case.req('claim')
barrier = threading.Barrier(2)
def call_same_request(_):
    store = MemoryStore(case.root / 'state')
    original = store.transition
    def synchronized_transition(*args, **kwargs):
        barrier.wait(timeout=10)
        return original(*args, **kwargs)
    store.transition = synchronized_transition
    ctl = MissionController(store, case.cid, SCOPE)
    try:
        return {'ok': True, 'result': ctl.action(copy.deepcopy(request))}
    except Exception as exc:
        return {'ok': False, 'error': type(exc).__name__, 'message': str(exc)}
with concurrent.futures.ThreadPoolExecutor(2) as executor:
    results = list(executor.map(call_same_request, range(2)))
observations.append({'case': 'simultaneous_identical_request', 'results': results,
                     'final_revision': case.store.receipt(case.cid, SCOPE)['revision']})

case = Case('hold_accept')
lease = case.claim()
case.ctl.action(case.req('hold', hold=True, reason='Stop ordered.', sources=[case.pin]))
case.ctl.action(case.req('submit', lease_id=lease, evidence=[case.pin]))
case.ctl.action(case.req('accept', actor=REVIEWER, review_evidence=[case.pin]))
projection = case.ctl.project()['projection']
observations.append({'case': 'submit_and_accept_while_held', 'hold': projection['hold'],
                     'tetelestai': projection['tetelestai']})

(ROOT / 'ADVERSARIAL_OBSERVATIONS.json').write_bytes(
    json.dumps(observations, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps(observations, ensure_ascii=False, indent=2))
