"""Real private-store tests; no network, provider or production imports."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor

WORK = Path(__file__).resolve().parents[1]
LIB = WORK / 'staging/core_r2/lib'
sys.path.insert(0, str(LIB))
from iald_memory import MemoryStore, ScopeViolation, RevisionConflict, ProjectionOverflow
from iald_memory.activity import ActivityRuntime, ActivityError, KEY
from iald_memory.mission import MissionController, MissionError, is_mission_record


class ActivityTests(unittest.TestCase):
    def setUp(self):
        runs = WORK / 'tests_core_r2/runs'
        runs.mkdir(parents=True, exist_ok=True)
        self.root = Path(tempfile.mkdtemp(prefix='activity_', dir=runs))
        self.scope = {'house': 'IALD_APP', 'principal': 'test-account-generation-a'}
        self.actor = {'kind': 'agent', 'id': 'test-server'}
        self.store = MemoryStore(self.root / 'store', snapshot_archive_dir=self.root / 'archive')
        self.store.ensure_context('conversation-a', objective='Original command retained.',
            scope=self.scope, actor={'kind': 'operator', 'id': 'test-human'},
            constraints={'permission_source': 'test_authenticated_server'})
        self.rt = ActivityRuntime(self.store, 'conversation-a', self.scope, self.actor)

    def start(self, request_id='r1', command='Build a reviewable candidate.'):
        return self.rt.begin(request_id, command, origin='authenticated_operator')['ticket']

    def snap(self):
        return self.store.get('conversation-a', self.scope)

    def append(self, rid, text, *, kind='fact', statute='REAL', source_kind='tool'):
        s = self.snap()
        return self.store.transition('conversation-a', self.scope, s['revision'], rid,
            self.actor, {'records': [{'id': rid, 'kind': kind, 'statute': statute,
            'text': text, 'sources': [{'kind': source_kind, 'ref': 'synthetic:' + rid}]}]})

    def test_begin_idempotent_payload_and_anchor(self):
        before = self.snap()
        t = self.start()
        after = self.snap()
        replay = self.rt.begin('r1', 'Build a reviewable candidate.', origin='authenticated_operator')
        self.assertTrue(replay['replayed'])
        self.assertEqual(after['revision'], self.snap()['revision'])
        self.assertEqual(before['anchor_sha256'], after['anchor_sha256'])
        self.assertEqual(before['objective_bytes_b64'], after['objective_bytes_b64'])
        with self.assertRaisesRegex(ActivityError, 'request_payload_conflict'):
            self.rt.begin('r1', 'Different command', origin='authenticated_operator')
        self.assertEqual(t['task_id'], replay['ticket']['task_id'])

    def test_scope_actor_and_tampered_ticket(self):
        t = self.start()
        with self.assertRaises(ScopeViolation):
            ActivityRuntime(self.store, 'conversation-a', {'house': 'IALD_APP', 'principal': 'other'}, self.actor)
        other = ActivityRuntime(self.store, 'conversation-a', self.scope, {'kind': 'agent', 'id': 'other'})
        with self.assertRaises(ActivityError):
            other.preflight(t, 'provider')
        forged = dict(t, epoch=t['epoch'] + 1)
        with self.assertRaisesRegex(ActivityError, 'ticket_server_binding_mismatch'):
            self.rt.preflight(forged, 'provider')
        with self.assertRaises(ActivityError):
            ActivityRuntime(self.store, 'conversation-a', self.scope, {'kind': 'model', 'id': 'model'})

    def test_multiple_operations_final_only_submits(self):
        t = self.start()
        p = self.rt.preflight(t, 'routing')
        mid = self.rt.complete(p['ticket'], 'routing', {'route': 'native'}, terminal=False)
        state = self.rt.controller.load()[1]
        self.assertEqual(state['tasks'][t['task_id']]['status'], 'working')
        p2 = self.rt.preflight(mid['ticket'], 'provider')
        end = self.rt.complete(p2['ticket'], 'provider', 'Candidate answer')
        self.assertFalse(end['accepted'])
        self.assertEqual(self.rt.controller.load()[1]['tasks'][t['task_id']]['status'], 'review_pending')
        self.assertFalse(self.rt.project(125000)['activity']['tetelestai'])
        rows = [r for r in self.snap()['q']['records'] if r.get('meta', {}).get(KEY, {}).get('kind') == 'result']
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r['kind'] == 'candidate' and r['statute'] == 'DECLARADO' for r in rows))
        rev = self.snap()['revision']
        again = self.rt.complete(p2['ticket'], 'provider', 'Candidate answer')
        self.assertTrue(again['replayed'])
        self.assertEqual(rev, self.snap()['revision'])

    def test_external_intent_never_resends(self):
        t = self.start()
        p = self.rt.preflight(t, 'provider')
        with self.assertRaisesRegex(ActivityError, 'operation_already_started'):
            self.rt.preflight(p['ticket'], 'provider')
        self.rt.mark_uncertain(p['ticket'], 'provider', 'Connection lost after dispatch')
        rev = self.snap()['revision']
        recovered = self.rt.recover('r1')
        self.assertFalse(recovered['automatic_retry'])
        self.assertTrue(any(h['status'] == 'uncertain' for h in recovered['handles']))
        self.assertEqual(rev, self.snap()['revision'])
        t2 = self.start('r2', 'New instruction; inspect old call.')
        self.assertNotEqual(t2['request_id'], t['request_id'])
        self.assertTrue(any(h.get('status') == 'uncertain' for h in self.snap()['p']['handles']))
        self.assertFalse(self.rt.project(125000)['activity']['tetelestai'])

    def test_stale_steering_result_is_preserved_first(self):
        p = self.rt.preflight(self.start(), 'provider')
        self.start('r2', 'New direction from authenticated user.')
        before = self.snap()['revision']
        with self.assertRaisesRegex(ActivityError, 'stale_result_preserved') as err:
            self.rt.complete(p['ticket'], 'provider', 'Late candidate', refresh=True)
        self.assertEqual(err.exception.details['cause'], 'steering_changed')
        row = self.rt._record(self.snap(), err.exception.details['candidate_record_id'])
        self.assertEqual(row['kind'], 'candidate')
        self.assertIn('Late candidate', row['text'])
        self.assertGreater(self.snap()['revision'], before)
        self.assertEqual(self.rt.controller.load()[1]['tasks'][p['ticket']['task_id']]['status'], 'working')

    def test_external_authenticated_erratum_invalidates(self):
        t = self.start()
        self.append('human-correction', 'Preserve new constraint', kind='erratum', statute='INPUT', source_kind='operator')
        with self.assertRaisesRegex(ActivityError, 'steering_changed'):
            self.rt.refresh(t)

    def test_mechanical_change_requires_explicit_refresh(self):
        t = self.start()
        self.append('progress-note', 'Observed intermediate progress')
        with self.assertRaisesRegex(ActivityError, 'revision_changed_explicit_refresh_required'):
            self.rt.preflight(t, 'provider')
        p = self.rt.preflight(t, 'provider', refresh=True)
        self.assertTrue(p['dispatch_allowed_once'])
        self.append('progress-note-two', 'Further mechanical progress')
        with self.assertRaisesRegex(ActivityError, 'stale_result_preserved'):
            self.rt.complete(p['ticket'], 'provider', 'Answer')
        end = self.rt.complete(p['ticket'], 'provider', 'Answer', refresh=True)
        self.assertTrue(end['integrated'])

    def test_snapshot_composition_reads_once_and_preserves_required(self):
        self.start()
        self.append('old-decision', 'Keep all observations', kind='decision', statute='INPUT', source_kind='operator')
        self.append('old-candidate', 'Optional text ' * 300, kind='candidate', statute='DECLARADO', source_kind='model')
        before = self.snap()
        original = self.store.get
        count = []
        def racing_get(*args, **kwargs):
            s = original(*args, **kwargs)
            count.append(s['revision'])
            if len(count) == 1:
                self.store.transition('conversation-a', self.scope, s['revision'], 'racing-progress', self.actor,
                    {'records': [{'id': 'racing-progress', 'kind': 'fact', 'statute': 'REAL', 'text': 'After snapshot',
                                  'sources': [{'kind': 'tool', 'ref': 'synthetic:race'}]}]})
            return s
        self.store.get = racing_get
        try:
            result = self.rt.project(125000)
        finally:
            self.store.get = original
        self.assertEqual(len(count), 1)
        self.assertEqual(result['receipt']['revision'], before['revision'])
        self.assertEqual(result['activity']['revision'], before['revision'])
        self.assertIn('old-decision', result['required_record_ids'])
        self.assertNotIn('racing-progress', result['text'])
        self.assertNotIn('Operational mission transition:', result['text'])
        self.assertNotEqual(result['projection_sha256'], result['mission_projection_sha256'])
        with self.assertRaises(ProjectionOverflow):
            self.rt.project(256)

    def test_original_projection_api_unchanged(self):
        self.start()
        snapshot = self.snap()
        old = self.store.project('conversation-a', self.scope, max_chars=125000)
        same = self.store.project_snapshot(snapshot, max_chars=125000)
        self.assertEqual(old, same)
        self.assertEqual(self.rt.controller.project(125000), self.rt.controller.project_snapshot(snapshot, 125000))

    def test_restart_in_another_process_recovers_without_call(self):
        p = self.rt.preflight(self.start(), 'provider')
        code = '''import sys,json
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from iald_memory import MemoryStore
from iald_memory.activity import ActivityRuntime
s=MemoryStore(sys.argv[2],snapshot_archive_dir=sys.argv[3])
r=ActivityRuntime(s,'conversation-a',{'house':'IALD_APP','principal':'test-account-generation-a'}, {'kind':'agent','id':'test-server'})
v=r.recover('r1')
print(json.dumps({'revision':v['receipt']['revision'],'statuses':[h['status'] for h in v['handles']], 'automatic_retry':v['automatic_retry']}))
'''
        cp = subprocess.run([sys.executable, '-B', '-X', 'utf8', '-c', code, str(LIB), str(self.root/'store'), str(self.root/'archive')], capture_output=True, text=True, check=True)
        v = json.loads(cp.stdout)
        self.assertEqual(v['revision'], self.snap()['revision'])
        self.assertIn('dispatching', v['statuses'])
        self.assertFalse(v['automatic_retry'])

    def test_cas_two_writers_only_one_dispatch(self):
        t = self.start()
        barrier = threading.Barrier(2)
        transition = self.store.transition
        def synchronized(*args, **kwargs):
            if args[3].startswith('activity_op_'):
                barrier.wait(timeout=10)
            return transition(*args, **kwargs)
        self.store.transition = synchronized
        def worker():
            try:
                return self.rt.preflight(t, 'provider')
            except (RevisionConflict, ActivityError) as exc:
                return exc
        try:
            with ThreadPoolExecutor(2) as pool:
                results = list(pool.map(lambda _: worker(), range(2)))
        finally:
            self.store.transition = transition
        self.assertEqual(sum(isinstance(x, dict) for x in results), 1)
        self.assertEqual(len([h for h in self.snap()['p']['handles'] if h.get('operation_id') == 'provider']), 1)

    def test_epoch_change_and_independent_accept(self):
        t = self.start()
        p = self.rt.preflight(t, 'provider')
        end = self.rt.complete(p['ticket'], 'provider', 'Evidence candidate')
        review = self.root/'review.json'
        review.write_text('{"verdict":"pass in isolated test"}', encoding='utf-8')
        pin = {'path': str(review), 'sha256': hashlib.sha256(review.read_bytes()).hexdigest()}
        projection = self.rt.controller.project(125000)
        accept = {'operation': 'accept', 'task_id': t['task_id'], 'actor': self.actor,
                  'event_id': 'test-accept', 'expected_revision': projection['receipt']['revision'],
                  'projection_sha256': projection['projection_sha256'], 'review_evidence': [pin]}
        with self.assertRaisesRegex(MissionError, 'independent_reviewer_required'):
            self.rt.controller.action(accept)
        accept['actor'] = {'kind': 'agent', 'id': 'separate-test-reviewer'}
        # Synthetic actor in a unit test only, never a production approval.
        self.rt.controller.action(accept)
        done = self.rt.project(125000)
        self.assertTrue(done['activity']['tetelestai'])
        self.assertFalse(done['activity']['active'])
        state = self.snap()
        self.rt.controller.action({'operation': 'invalidate', 'task_id': t['task_id'],
            'actor': self.actor, 'event_id': 'invalidate-test', 'expected_revision': state['revision'],
            'state_sha256': state['receipt']['state_sha256'], 'reason': 'Changed premise', 'sources': [pin]})
        self.assertFalse(self.rt.project(125000)['activity']['tetelestai'])
        with self.assertRaisesRegex(ActivityError, 'task_epoch_changed'):
            self.rt.refresh(t)

    def test_unresolved_operation_blocks_final_submit(self):
        t = self.start()
        p = self.rt.preflight(t, 'provider1')
        p2 = self.rt.preflight(p['ticket'], 'provider2')
        with self.assertRaisesRegex(ActivityError, 'other_operations_unresolved'):
            self.rt.complete(p2['ticket'], 'provider2', 'Known second return')
        self.assertEqual(self.rt.controller.load()[1]['tasks'][t['task_id']]['status'], 'working')
        self.assertTrue(any('Known second return' in r['text'] for r in self.snap()['q']['records']))

    def test_artifact_corruption_and_read_no_repair(self):
        t = self.start()
        row = self.rt._record(self.snap(), self.rt._ids('r1')['request'])
        path = Path(row['sources'][0]['ref'])
        path.write_bytes(b'corrupted synthetic artifact')
        with self.assertRaisesRegex(ActivityError, 'artifact_bytes_mismatch'):
            self.rt.recover('r1')
        self.assertEqual(path.read_bytes(), b'corrupted synthetic artifact')

    def test_divergent_return_preserved_but_refused(self):
        p = self.rt.preflight(self.start(), 'provider')
        self.rt.complete(p['ticket'], 'provider', 'First return', terminal=False)
        with self.assertRaisesRegex(ActivityError, 'result_identity_conflict'):
            self.rt.complete(p['ticket'], 'provider', 'Different return', terminal=False, refresh=True)
        rows = self.snap()['q']['records']
        self.assertTrue(any('First return' in r['text'] for r in rows))
        self.assertTrue(any('Different return' in r['text'] for r in rows))

    def test_projection_cost_no_event_growth(self):
        self.start()
        before = self.snap()
        started = time.perf_counter()
        projections = [self.rt.project(125000) for _ in range(12)]
        elapsed = time.perf_counter() - started
        after = self.snap()
        self.assertEqual(before, after)
        self.assertEqual(len({p['projection_sha256'] for p in projections}), 1)
        measured = {'calls': 12, 'seconds': elapsed, 'mean_ms': elapsed/12*1000,
                    'event_growth': after['revision']-before['revision'],
                    'actual_chars': projections[-1]['actual_chars'], 'private_store': str(self.root)}
        (self.root/'projection_cost.json').write_text(json.dumps(measured, indent=2), encoding='utf-8')
        print('COST ' + json.dumps(measured))

    def test_delegated_system_origins_never_forge_operator(self):
        human = self.start()
        before = self.rt._steering(self.snap())
        for origin in ('delegated', 'system'):
            t = self.rt.begin(origin, 'Server authenticated delegated work.',
                             origin=origin, origin_ref='trusted-parent:' + human['request_id'])['ticket']
            self.assertEqual(t['steering_sha256'], before)
            command = self.rt._record(self.snap(), self.rt._ids(origin)['steering'])
            self.assertEqual(command['kind'], 'fact')
            self.assertTrue(all(s['kind'] == 'tool' for s in command['sources']))
            self.assertEqual(t['origin'], origin)
        self.assertEqual(self.rt._steering(self.snap()), before)
        with self.assertRaisesRegex(ActivityError, 'delegation_reference_required'):
            self.rt.begin('unbound-worker', 'Do work.', origin='delegated')
        with self.assertRaisesRegex(ActivityError, 'invalid_origin'):
            self.rt.begin('model-order', 'Do work.', origin='model')

    def test_crash_after_submit_reconciles_request_handle(self):
        p = self.rt.preflight(self.start(), 'provider')
        original = self.store.transition
        def crash(*args, **kwargs):
            if args[3].startswith('activity_finished_'):
                raise OSError('Synthetic process crash after durable submit')
            return original(*args, **kwargs)
        self.store.transition = crash
        try:
            with self.assertRaises(OSError):
                self.rt.complete(p['ticket'], 'provider', 'Durable candidate')
        finally:
            self.store.transition = original
        self.assertEqual(self.rt.controller.load()[1]['tasks'][p['ticket']['task_id']]['status'], 'review_pending')
        self.assertTrue(any(h['status'] == 'prepared' for h in self.rt.recover('r1')['handles']))
        recovered = ActivityRuntime(self.store, 'conversation-a', self.scope, self.actor)
        result = recovered.complete(p['ticket'], 'provider', 'Durable candidate')
        self.assertTrue(result['replayed'])
        self.assertTrue(all(h['status'] == 'completed' for h in recovered.recover('r1')['handles']))

    def test_return_custody_retries_local_cas_then_refuses_stale(self):
        p = self.rt.preflight(self.start(), 'provider')
        original = self.store.transition
        fired = []
        def race(*args, **kwargs):
            if args[3].startswith('activity_result_') and not fired:
                fired.append(True)
                self.append('concurrent-progress', 'Another worker advanced.')
            return original(*args, **kwargs)
        self.store.transition = race
        try:
            with self.assertRaisesRegex(ActivityError, 'stale_result_preserved') as err:
                self.rt.complete(p['ticket'], 'provider', 'Received once')
        finally:
            self.store.transition = original
        row = self.rt._record(self.snap(), err.exception.details['candidate_record_id'])
        self.assertIn('Received once', row['text'])
        self.assertTrue(self.rt.complete(p['ticket'], 'provider', 'Received once', refresh=True)['integrated'])

    def test_identical_payload_artifacts_scoped_to_context(self):
        first = self.rt._artifact({'value': 'Same bytes'})
        self.store.ensure_context('conversation-b', objective='Original command retained.',
            scope={'house': 'IALD_APP', 'principal': 'test-account-generation-b'},
            actor={'kind': 'operator', 'id': 'test-human-b'})
        other = ActivityRuntime(self.store, 'conversation-b',
            {'house': 'IALD_APP', 'principal': 'test-account-generation-b'}, self.actor)
        second = other._artifact({'value': 'Same bytes'})
        self.assertNotEqual(first['sha256'], second['sha256'])
        self.assertNotEqual(first['path'], second['path'])

    def test_admission_source_pin_checked(self):
        t = self.start()
        source = Path(t['source']['path'])
        source.write_bytes(b'Synthetic changed admission')
        with self.assertRaisesRegex(MissionError, 'evidence_hash_mismatch'):
            self.rt.preflight(t, 'provider')

    def test_broken_admission_still_preserves_received_candidate(self):
        p = self.rt.preflight(self.start(), 'provider')
        Path(p['ticket']['source']['path']).write_bytes(b'Synthetic changed admission')
        with self.assertRaisesRegex(ActivityError, 'stale_result_preserved') as err:
            self.rt.complete(p['ticket'], 'provider', 'Returned before corruption discovered')
        row = self.rt._record(self.snap(), err.exception.details['candidate_record_id'])
        self.assertEqual(row['kind'], 'candidate')

    def test_authenticated_pending_changes_steering(self):
        t = self.start()
        self.append('new-human-pending', 'Await human choice before action',
                    kind='pending', statute='OPEN', source_kind='operator')
        with self.assertRaisesRegex(ActivityError, 'steering_changed'):
            self.rt.refresh(t)

    def test_preflight_rechecks_steering_after_intent(self):
        t = self.start()
        original = self.store.transition
        def race(*args, **kwargs):
            receipt = original(*args, **kwargs)
            if args[3].startswith('activity_op_'):
                self.append('new-direction-after-intent', 'Stop this request and revise',
                            kind='erratum', statute='INPUT', source_kind='operator')
            return receipt
        self.store.transition = race
        try:
            with self.assertRaisesRegex(ActivityError, 'preflight_changed_after_intent'):
                self.rt.preflight(t, 'provider', refresh=True)
        finally:
            self.store.transition = original
        self.assertTrue(any(h['status'] == 'dispatching' for h in self.rt.recover('r1')['handles']))
        with self.assertRaises(ActivityError):
            self.rt.preflight(t, 'provider', refresh=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
