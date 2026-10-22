"""Focused E2 checks. Real ACOM/CLI, private stores, no production transitions."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid

ROOT = Path(__file__).resolve().parent
CORE = Path(r'C:\IALD\MEMORIA_IALD')
RUN = Path(tempfile.mkdtemp(prefix='isolated_e2_', dir=ROOT))
STAGE = RUN / 'lib'
shutil.copytree(CORE / 'lib' / 'iald_memory', STAGE / 'iald_memory',
                ignore=shutil.ignore_patterns('__pycache__'))
shutil.copyfile(ROOT / 'mission_candidate.py', STAGE / 'iald_memory' / 'mission.py')
sys.path.insert(0, str(STAGE))
from iald_memory import MemoryStore
from iald_memory.mission import MissionController, MissionError, encoded

spec = importlib.util.spec_from_file_location('iald_memory.installed_baseline', CORE / 'lib' / 'iald_memory' / 'mission.py')
baseline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)

SCOPE = {'house': 'IALD', 'principal': 'terminal-projection-test'}
OWNER = {'id': 'isolated-builder', 'kind': 'agent'}
REVIEWER = {'id': 'isolated-reviewer', 'kind': 'agent'}
MEASUREMENTS = {}


class TerminalProjectionTests(unittest.TestCase):
    def setUp(self):
        self.root = RUN / self._testMethodName
        self.root.mkdir()
        self.store = MemoryStore(self.root / 'state')
        self.cid = str(uuid.uuid4())
        anchor = self.store.ensure_context(self.cid, objective='Original objective\r\nKeep all orders.',
                                          scope=SCOPE, actor=OWNER, constraints={'no_repeat': True})
        self.ctl = MissionController(self.store, self.cid, SCOPE)
        self.legacy = baseline.MissionController(self.store, self.cid, SCOPE)
        f = self.root / 'evidence.txt'
        f.write_bytes(b'Isolated technical evidence, no scientific acceptance.')
        self.pin = {'path': str(f), 'sha256': hashlib.sha256(f.read_bytes()).hexdigest()}
        self.ref = self.root / 'REFERENCE.json'
        self.ref.write_text(json.dumps({'protocol': 'iald-memory-session/v1', 'store': str(self.root / 'state'),
                                       'context_id': self.cid, 'scope': SCOPE,
                                       'objective_sha256': anchor['objective_sha256']}), encoding='utf-8')
        self.ctl.action({'operation': 'configure', 'event_id': 'configure', 'actor': OWNER,
                         'expected_revision': 0, 'requirements': [{'id': 'A', 'criterion': 'One isolated requirement',
                                                                  'depends_on': []}], 'sources': [self.pin]})

    def transition(self, changes):
        return self.store.transition(self.cid, SCOPE, self.store.receipt(self.cid, SCOPE)['revision'],
                                     str(uuid.uuid4()), OWNER, changes)

    def request(self, operation, **extra):
        p = self.ctl.project(200000)
        return {'operation': operation, 'task_id': 'A', 'actor': OWNER, 'event_id': str(uuid.uuid4()),
                'expected_revision': p['receipt']['revision'], 'projection_sha256': p['projection_sha256'],
                'reference': str(self.ref), **extra}

    def cli(self, operation, **extra):
        command = [sys.executable, '-B', '-X', 'utf8', str(CORE / 'mission_cli.py'),
                   '--core-root', str(STAGE), '--store', str(self.root / 'state'),
                   '--session-adapter', str(CORE / 'session_memory.py')]
        proc = subprocess.run(command, input=json.dumps({'operation': operation, 'reference': str(self.ref), **extra}),
                              text=True, encoding='utf-8', capture_output=True, timeout=40)
        self.assertEqual(proc.returncode, 0, proc.stdout[:2000] + proc.stderr)
        return json.loads(proc.stdout)['result']

    def test_1000_large_terminals_recovery_and_no_mutation(self):
        terminal = [{'id': f't{i:04}', 'status': 'completed', 'phase': 'returned', 'task_id': 'A',
                     'no_repeat': True, 'detail': ('event-' + str(i) + '\n') * 650,
                     'receipt': {'exit_code': 0, 'path': f'isolated/{i}/receipt.json'}} for i in range(1000)]
        pending = [{'id': 'pending', 'status': 'running', 'detail': 'pending details survive'},
                   {'id': 'unknown', 'phase': 'unrecognized', 'detail': 'unknown details survive'},
                   {'id': 'conflict', 'status': 'done', 'phase': 'dispatch_uncertain', 'detail': 'conflict survives'}]
        self.transition({'flow': {'handles': list(reversed(terminal)) + pending}})
        before = self.store.get(self.cid, SCOPE)
        journals = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in (self.root / 'state').rglob('*') if p.is_file() and 'journal' in str(p).lower()}
        with self.assertRaisesRegex(baseline.MissionError, 'projection_overflow_required_'):
            self.legacy.project(200000)
        p = self.ctl.project(200000)
        body = p['projection']
        self.assertLess(p['actual_chars'], 110000)
        self.assertEqual(body['flow']['handles'], sorted(pending, key=lambda h: h['id']))
        self.assertEqual(body['unresolved_handles'], body['flow']['handles'])
        self.assertEqual(body['terminal_handles'], [
            {k: h[k] for k in ('id', 'status', 'phase', 'task_id', 'no_repeat') if k in h} for h in terminal])
        self.assertFalse(body['tetelestai'])
        self.assertEqual(self.ctl.project(200000), p)
        self.assertEqual(self.cli('project', max_chars=200000), p)
        recovered = self.cli('get')
        self.assertEqual(recovered, before)
        recovery = body['terminal_handles_recovery']
        self.assertEqual(recovery['operation'], 'get')
        self.assertEqual(recovery['context_id'], self.cid)
        self.assertEqual(recovery['revision'], recovered['revision'])
        self.assertEqual(recovery['state_sha256'], recovered['receipt']['state_sha256'])
        self.assertIn('current state', recovery['instruction'])
        self.assertIn('journal replay', recovery['instruction'])
        self.assertEqual(self.store.get(self.cid, SCOPE), before)
        self.assertEqual(journals, {str(f): hashlib.sha256(f.read_bytes()).hexdigest()
                                  for f in (self.root / 'state').rglob('*')
                                  if f.is_file() and 'journal' in str(f).lower()})
        self.assertTrue(self.store.verify(self.cid, SCOPE, deep=True)['ok'])
        MEASUREMENTS['large'] = {'handles': 1003, 'terminals': 1000, 'unresolved': 3,
                                 'full_flow_chars': len(encoded(before['p'])), 'projection_chars': p['actual_chars'],
                                 'revision': before['revision'], 'state_sha256': before['receipt']['state_sha256'],
                                 'get_matches_full_snapshot': True, 'journal_hashes_unchanged': True}

    def test_exact_existing_classification_and_only_present_keys(self):
        terminal_states = ['completed', 'returned', 'failed', 'cancelled', 'closed', 'accepted', 'consumed', 'done', 'terminated']
        terminals = [{'id': 's_' + t, 'status': t, 'detail': 'full'} for t in terminal_states]
        terminals += [{'id': 'p_only', 'phase': 'completed', 'detail': 'full'},
                      {'id': 'both_terminal', 'phase': 'failed', 'status': 'completed', 'task_id': None, 'no_repeat': False}]
        unresolved = [{'id': 'absent', 'detail': 'preserve'}, {'id': 'null', 'status': None},
                      {'id': 'number', 'phase': 3}, {'id': 'bool', 'status': True}, {'id': 'empty', 'phase': ''},
                      {'id': 'unknown', 'status': 'COMPLETED'}, {'id': 'conflict1', 'status': 'done', 'phase': 'running'},
                      {'id': 'conflict2', 'phase': 'done', 'status': 'uncertain'},
                      {'id': 'present_null', 'phase': 'done', 'status': None}]
        self.transition({'flow': {'handles': terminals + unresolved}})
        new = self.ctl.project()['projection']
        old = self.legacy.project()['projection']
        self.assertEqual(new['unresolved_handles'], sorted(old['unresolved_handles'], key=lambda h: h['id']))
        self.assertEqual(new['unresolved_handles'], sorted(unresolved, key=lambda h: h['id']))
        self.assertEqual(new['tetelestai'], old['tetelestai'])
        rows = {h['id']: h for h in new['terminal_handles']}
        self.assertEqual(set(rows['s_done']), {'id', 'status'})
        self.assertEqual(set(rows['p_only']), {'id', 'phase'})
        self.assertIsNone(rows['both_terminal']['task_id'])
        self.assertIs(rows['both_terminal']['no_repeat'], False)

    def test_deterministic_order_and_snapshot_not_aliased(self):
        self.transition({'flow': {'handles': [{'id': 'z', 'status': 'done', 'nested': [1]},
                                              {'id': 'c', 'phase': 'running', 'nested': [2]},
                                              {'id': 'a', 'status': 'failed'}, {'id': 'b', 'phase': 'unknown'}]}})
        snap, state, previous = self.ctl.load()
        untouched = copy.deepcopy(snap)
        first = self.ctl._project(snap, state, previous, 24000)
        other = copy.deepcopy(snap)
        other['p']['handles'].reverse()
        self.assertEqual(first, self.ctl._project(other, state, previous, 24000))
        first['projection']['flow']['handles'][1]['nested'].append(99)
        self.assertEqual(snap, untouched)

    def test_partial_flow_merge_preserves_terminal_details(self):
        terminal = {'id': 'finished', 'status': 'failed', 'detail': 'preserve full receipt', 'no_repeat': True}
        self.transition({'flow': {'handles': [terminal, {'id': 'pending', 'phase': 'running'}]}})
        projected_flow = self.ctl.project()['projection']['flow']
        self.transition({'flow': projected_flow})
        self.transition({'flow': {'handles': [{'id': 'pending', 'phase': 'completed'}]}})
        full = {h['id']: h for h in self.store.get(self.cid, SCOPE)['p']['handles']}
        self.assertEqual(full['finished'], terminal)
        self.assertEqual(full['pending']['phase'], 'completed')
        self.assertEqual(len(self.ctl.project()['projection']['terminal_handles']), 2)
        self.assertTrue(self.store.verify(self.cid, SCOPE, deep=True)['ok'])

    def test_cas_stale_hash_terminal_detail_and_idempotence(self):
        self.transition({'flow': {'handles': [{'id': 'terminal', 'status': 'done', 'detail': 'before'}]}})
        before = self.ctl.project()
        old_request = self.request('claim')
        self.transition({'flow': {'handles': [{'id': 'terminal', 'detail': 'after'}]}})
        after = self.ctl.project()
        self.assertEqual(before['projection']['terminal_handles'], after['projection']['terminal_handles'])
        self.assertNotEqual(before['projection_sha256'], after['projection_sha256'])
        with self.assertRaisesRegex(MissionError, 'stale_revision'):
            self.ctl.action(old_request)
        old_request['expected_revision'] = after['receipt']['revision']
        with self.assertRaisesRegex(MissionError, 'stale_projection'):
            self.ctl.action(old_request)
        req = self.request('claim')
        first = self.ctl.action(req)
        repeated = self.ctl.action(req)
        self.assertTrue(repeated['replayed'])
        self.assertEqual(first['receipt'], repeated['receipt'])
        changed = {**req, 'lease_seconds': 70}
        with self.assertRaisesRegex(MissionError, 'idempotency_conflict'):
            self.ctl.action(changed)
        recovery = before['projection']['terminal_handles_recovery']
        current = self.cli('get')
        self.assertNotEqual(recovery['revision'], current['revision'])
        self.assertNotEqual(recovery['state_sha256'], current['receipt']['state_sha256'])

    def test_preflight_handoff_and_legacy_projection_hash_refusal(self):
        self.transition({'flow': {'handles': [{'id': 'terminal', 'phase': 'done', 'detail': 'x' * 10000}]}})
        old = self.legacy.project(100000)
        wrong = self.request('claim')
        wrong['projection_sha256'] = old['projection_sha256']
        with self.assertRaisesRegex(MissionError, 'stale_projection'):
            self.ctl.action(wrong)
        lease = self.ctl.action(self.request('claim'))['task']['lease']['id']
        p = self.ctl.project()
        req = self.request('handoff', lease_id=lease, max_chars=p['actual_chars'])
        self.assertTrue(self.ctl.check(req)['ready'])
        handoff = self.ctl.handoff(req)
        self.assertEqual(handoff['projection'], p['projection'])
        self.assertEqual(handoff['projection_sha256'], p['projection_sha256'])
        self.assertEqual(handoff['preflight']['receipt'], p['receipt'])
        self.assertEqual(self.cli('handoff', **{k: v for k, v in req.items()
                                               if k not in {'operation', 'reference'}}), handoff)
        with self.assertRaisesRegex(MissionError, 'projection_overflow'):
            self.ctl.handoff({**req, 'max_chars': p['actual_chars'] - 1})
        with self.assertRaisesRegex(MissionError, 'lease_owner_mismatch'):
            self.ctl.check({**req, 'actor': REVIEWER})

    def test_current_records_and_overflow_are_preserved(self):
        records = [{'id': 'order', 'kind': 'decision', 'statute': 'INPUT', 'text': 'No provider repeat. ' + 'a' * 30000,
                    'sources': [{'kind': 'artifact', 'ref': 'isolated-order'}]},
                   {'id': 'erratum', 'kind': 'erratum', 'statute': 'INPUT', 'text': 'Only the deadline changes.',
                    'supersedes': 'order', 'sources': [{'kind': 'artifact', 'ref': 'isolated-correction'}]},
                   {'id': 'fact', 'kind': 'fact', 'statute': 'REAL', 'text': 'Measured obligation remains.',
                    'sources': [{'kind': 'artifact', 'ref': 'isolated-measurement'}]}]
        self.transition({'records': records})
        with self.assertRaisesRegex(MissionError, 'projection_overflow_required_'):
            self.ctl.project(24000)
        p = self.ctl.project(100000)
        full = self.store.get(self.cid, SCOPE)
        self.assertEqual(p['projection']['current_records'], full['q']['records'][1:])
        self.assertEqual(self.ctl.project(p['actual_chars']), p)
        with self.assertRaisesRegex(MissionError, 'projection_overflow'):
            self.ctl.project(p['actual_chars'] - 1)
        for budget in [True, 255, 2000001]:
            with self.assertRaisesRegex(MissionError, 'invalid_projection_budget'):
                self.ctl.project(budget)

    def test_tetelestai_matches_existing_rule(self):
        lease = self.ctl.action(self.request('claim'))['task']['lease']['id']
        self.ctl.action(self.request('submit', lease_id=lease, evidence=[self.pin]))
        self.ctl.action(self.request('accept', actor=REVIEWER, review_evidence=[self.pin]))
        cases = [{'id': 'x', 'status': 'done'}, {'id': 'x', 'phase': 'completed'},
                 {'id': 'x', 'status': 'done', 'phase': 'uncertain'}, {'id': 'x', 'status': None},
                 {'id': 'x', 'phase': 'terminated', 'status': 'cancelled'}]
        for h in cases:
            self.transition({'flow': {'handles': [h]}})
            actual = self.ctl.project()['projection']
            original = self.legacy.project()['projection']
            self.assertEqual(actual['tetelestai'], original['tetelestai'])
            self.assertEqual(bool(actual['flow']['handles']), bool(original['unresolved_handles']))
        self.assertTrue(self.ctl.project()['projection']['tetelestai'])


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TerminalProjectionTests))
    report = {'ok': result.wasSuccessful(), 'tests_run': result.testsRun,
              'failures': [{'test': str(t), 'detail': detail} for t, detail in result.failures + result.errors],
              'run_directory': str(RUN), 'measurements': MEASUREMENTS,
              'candidate_sha256': hashlib.sha256((ROOT / 'mission_candidate.py').read_bytes()).hexdigest(),
              'test_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope': 'Real isolated ACOM/CLI; zero production transitions, providers, or Lean builds.'}
    target = ROOT / ('TEST_RESULT_' + RUN.name + '.json')
    raw = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    temp = target.with_suffix('.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    os.rename(temp, target)
    print(json.dumps({'report': str(target), 'ok': report['ok'], 'tests_run': result.testsRun,
                      'measurements': MEASUREMENTS}, ensure_ascii=False))
    sys.exit(0 if result.wasSuccessful() else 1)
