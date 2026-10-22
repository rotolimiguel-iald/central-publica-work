import base64
import hashlib
import json
import multiprocessing
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from iald_memory import (
    MemoryStore, AnchorConflict, ScopeViolation, RevisionConflict,
    IdempotencyConflict, IntegrityError, InvariantViolation, InvalidInput,
    ProjectionOverflow, ContextNotFound,
)

SCOPE = {'house': 'IALD', 'principal': 'operator'}
OPERATOR = {'id': 'operator', 'kind': 'operator'}
AGENT = {'id': 'coordinator', 'kind': 'agent'}
MODEL = {'id': 'external-model', 'kind': 'model'}


def candidate(name, text='A contribution, not an established fact.'):
    return {'id': name, 'text': text, 'statute': 'DECLARADO',
            'source': {'kind': 'executor', 'ref': 'job:' + name}}


def process_writer(root, number, queue):
    try:
        store = MemoryStore(root)
        store.ensure_context('shared', objective='Concurrent objective', scope=SCOPE,
                             actor=OPERATOR, constraints={'max_calls': 1})
        changes = {'candidates': [candidate('record-' + str(number))],
                   'flow': {'handles': [{'id': 'job-' + str(number), 'status': 'result_ready'}]}}
        for _ in range(30):
            state = store.get('shared', SCOPE)
            try:
                receipt = store.transition('shared', SCOPE, state['revision'],
                                           'event-' + str(number), AGENT, changes)
                queue.put(('ok', receipt['revision']))
                return
            except RevisionConflict:
                continue
        queue.put(('error', 'exhausted CAS retries'))
    except Exception as exc:
        queue.put(('error', repr(exc)))


def crash_after_insert(root):
    store = MemoryStore(root)
    original = store._read
    calls = 0
    def crash(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 2:
            os._exit(73)
        return original(*args, **kwargs)
    store._read = crash
    store.transition('context', SCOPE, 0, 'crashed-event', AGENT,
                     {'candidates': [candidate('crashed-record')], 'flow': {'phase': 'unsafe-partial'}})


class MemoryStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store = MemoryStore(self.root)
        self.raw = b'First instruction\r\nKeep original whitespace.  \r\n'
        self.initial = self.store.ensure_context(
            'context', objective=self.raw, scope=SCOPE, actor=OPERATOR,
            constraints={'max_calls': 1, 'must_preserve': ['sources', 'scope'], 'authorization': 'operator_input_only'})

    def tearDown(self):
        self.temp.cleanup()

    def append(self, event='event-1', record='record-1', text='Candidate text', actor=AGENT):
        return self.store.transition('context', SCOPE, self.store.get('context', SCOPE)['revision'], event, actor,
                                     {'candidates': [candidate(record, text)],
                                      'flow': {'phase': 'result_ready', 'next_action': 'verify sources'}})

    def test_original_bytes_and_strict_idempotent_anchor(self):
        state = self.store.get('context', SCOPE)
        self.assertEqual(base64.b64decode(state['objective_bytes_b64']), self.raw)
        self.assertEqual(state['objective_sha256'], hashlib.sha256(self.raw).hexdigest())
        again = self.store.ensure_context('context', objective=self.raw, scope=SCOPE, actor=OPERATOR,
                                         constraints=state['constraints'])
        self.assertTrue(again['receipt']['replayed'])
        with self.assertRaises(AnchorConflict):
            self.store.ensure_context('context', objective=self.raw.replace(b'\r\n', b'\n'),
                                      scope=SCOPE, actor=OPERATOR, constraints=state['constraints'])
        self.assertEqual(self.store.get('context', SCOPE)['revision'], 0)

    def test_state_and_flow_commit_together_and_survive_restart(self):
        receipt = self.append()
        fresh = MemoryStore(self.root).get('context', SCOPE)
        self.assertEqual(fresh['revision'], 1)
        self.assertEqual(fresh['q']['records'][0]['id'], 'record-1')
        self.assertEqual(fresh['p']['phase'], 'result_ready')
        self.assertEqual(fresh['receipt'], receipt)
        backups = list(self.root.glob('memory.sqlite3.bak_*'))
        self.assertEqual(len(backups), 2)
        previous = sqlite3.connect(str(backups[-1]))
        self.assertEqual(previous.execute('SELECT count(*) FROM events').fetchone()[0], 1)
        previous.close()

    def test_cas_and_stable_replay(self):
        payload = {'candidates': [candidate('r')]}
        receipt = self.store.transition('context', SCOPE, 0, 'e', AGENT, payload)
        self.append('later', 'later-record')
        replay = self.store.transition('context', SCOPE, 0, 'e', AGENT, payload)
        self.assertTrue(replay['replayed'])
        self.assertEqual(replay['event_hash'], receipt['event_hash'])
        self.assertEqual(replay['revision'], 1)
        with self.assertRaises(RevisionConflict) as caught:
            self.store.transition('context', SCOPE, 0, 'fresh', AGENT, {'candidates': [candidate('fresh')]})
        self.assertEqual(caught.exception.actual_revision, 2)
        with self.assertRaises(IdempotencyConflict):
            self.store.transition('context', SCOPE, 2, 'e', AGENT, {'candidates': [candidate('r', 'changed')]})
        self.assertEqual(self.store.get('context', SCOPE)['revision'], 2)

    def test_cross_scope_all_entry_points(self):
        wrong = {'house': 'IALD', 'principal': 'somebody-else'}
        operations = [
            lambda: self.store.get('context', wrong),
            lambda: self.store.project('context', wrong),
            lambda: self.store.receipt('context', wrong),
            lambda: self.store.transition('context', wrong, 0, 'e', AGENT, {'candidates': [candidate('r')]}),
            lambda: self.store.ensure_context('context', objective=self.raw, scope=wrong, actor=OPERATOR),
            lambda: self.store.ensure_context('child', objective='Delegate', scope=wrong, actor=AGENT, parent_id='context'),
        ]
        for operation in operations:
            with self.assertRaises(ScopeViolation):
                operation()
        with self.assertRaises(ContextNotFound):
            self.store.get('missing', SCOPE)

    def test_model_cannot_establish_anchor_or_flow_or_promote_output(self):
        with self.assertRaises(InvariantViolation):
            self.store.ensure_context('model-goal', objective='New authority', scope=SCOPE, actor=MODEL)
        for changes in [
            {'flow': {'phase': 'approved'}},
            {'records': [{'id': 'claim', 'kind': 'fact', 'text': 'True', 'statute': 'REAL',
                          'sources': [{'kind': 'artifact', 'ref': 'model-asserted'}]}]},
        ]:
            with self.assertRaises(InvariantViolation):
                self.store.transition('context', SCOPE, 0, 'e', MODEL, changes)
        record = {'id': 'claim', 'kind': 'fact', 'text': 'True', 'statute': 'REAL',
                  'sources': [{'kind': 'executor', 'ref': 'model-output'}]}
        with self.assertRaises(InvariantViolation):
            self.store.transition('context', SCOPE, 0, 'e', AGENT, {'records': [record]})
        self.store.transition('context', SCOPE, 0, 'e', MODEL, {'candidates': [candidate('r')]})
        self.assertEqual(self.store.get('context', SCOPE)['q']['records'][0]['statute'], 'DECLARADO')

    def test_constraints_immutable_and_children_inherit(self):
        child = self.store.ensure_context('child', objective='Subtask', scope=SCOPE, actor=AGENT, parent_id='context')
        self.assertEqual(child['constraints'], self.initial['constraints'])
        with self.assertRaises(InvariantViolation):
            self.store.ensure_context('bad-child', objective='Subtask', scope=SCOPE, actor=AGENT,
                                      parent_id='context', constraints={'max_calls': 100})
        with self.assertRaises(InvalidInput):
            self.store.transition('context', SCOPE, 0, 'e', AGENT, {'constraints': {'max_calls': 100}})

    def test_errata_are_additive_and_handles_merge(self):
        self.append()
        state = self.store.get('context', SCOPE)
        correction = {'id': 'correction', 'kind': 'erratum', 'text': 'Independent correction', 'statute': 'INPUT',
                      'sources': [{'kind': 'operator', 'ref': 'turn:2'}], 'supersedes': 'record-1'}
        self.store.transition('context', SCOPE, state['revision'], 'correction-event', OPERATOR,
                               {'records': [correction], 'flow': {'handles': [{'id': 'job', 'job_id': 'remote-1', 'status': 'sent'}]}})
        self.store.transition('context', SCOPE, 2, 'status-event', AGENT,
                               {'flow': {'handles': [{'id': 'job', 'status': 'uncertain'}]}})
        state = self.store.get('context', SCOPE)
        self.assertEqual(len(state['q']['records']), 2)
        self.assertEqual(state['q']['records'][0]['id'], 'record-1')
        self.assertEqual(state['p']['handles'], [{'id': 'job', 'job_id': 'remote-1', 'status': 'uncertain'}])
        with self.assertRaises(InvariantViolation):
            self.append('duplicate-record', 'record-1')

    def test_projection_is_bounded_auditable_and_does_not_destroy(self):
        for n in range(5):
            self.append('e-' + str(n), 'r-' + str(n), ('long candidate ' + str(n) + ' ') * 100)
        before = self.store.get('context', SCOPE)
        projection = self.store.project('context', SCOPE, max_chars=3000, current_input='candidate 4')
        self.assertTrue(projection['overflow'])
        self.assertLessEqual(len(projection['text']), 3000)
        self.assertEqual(len(projection['included_record_ids']) + len(projection['omitted_record_ids']), 5)
        body = json.loads(projection['text'].split('\n', 2)[2])
        self.assertEqual(body['objective'].encode('utf-8'), self.raw)
        self.assertEqual(body['constraints'], before['constraints'])
        self.assertEqual(body['flow'], before['p'])
        self.assertEqual(self.store.get('context', SCOPE), before)
        self.assertEqual(self.store.project('context', SCOPE, 3000, 'candidate 4'), projection)
        with self.assertRaises(ProjectionOverflow) as caught:
            self.store.project('context', SCOPE, 256)
        self.assertGreater(caught.exception.required_chars, 256)

    def test_projection_never_separates_original_and_correction(self):
        self.append(text='Original short candidate')
        correction = {'id': 'correction', 'kind': 'erratum', 'text': 'Correction ' * 300,
                      'statute': 'INPUT', 'sources': [{'kind': 'operator', 'ref': 'turn:2'}],
                      'supersedes': 'record-1'}
        self.store.transition('context', SCOPE, 1, 'correction-event', OPERATOR, {'records': [correction]})
        with self.assertRaises(ProjectionOverflow):
            self.store.project('context', SCOPE, 2300)
        projected = self.store.project('context', SCOPE, 12000)
        self.assertEqual(projected['required_record_ids'], ['record-1', 'correction'])
        self.assertEqual(projected['included_record_ids'], ['record-1', 'correction'])
        self.assertEqual(projected['omitted_record_ids'], [])
        self.assertTrue(self.store.verify('context', SCOPE)['ok'])
        self.assertEqual(self.store.verify('context', SCOPE)['event_count'], 3)

    def test_steering_after_original_goal_is_required_or_overflows(self):
        self.store.ensure_context('steering', objective='Deliver route A', scope=SCOPE, actor=OPERATOR)
        before = self.store.project('steering', SCOPE)
        decision = {'id': 'route-b', 'kind': 'decision', 'text': 'Deliver route B instead. ' * 50,
                    'statute': 'INPUT', 'sources': [{'kind': 'operator', 'ref': 'turn:2'}]}
        self.store.transition('steering', SCOPE, 0, 'steering-event', OPERATOR, {'records': [decision]})
        with self.assertRaises(ProjectionOverflow):
            self.store.project('steering', SCOPE, before['actual_chars'] + 10, current_input='route A')
        projected = self.store.project('steering', SCOPE)
        self.assertIn('route-b', projected['required_record_ids'])
        self.assertIn(decision['text'], projected['text'])
        self.assertIn('Deliver route A', projected['text'])
        self.assertEqual(self.store.get('steering', SCOPE)['objective'], 'Deliver route A')

    def test_all_consolidated_record_types_cannot_disappear_under_compaction(self):
        records = []
        for kind in ['fact', 'decision', 'contradiction', 'pending', 'erratum']:
            records.append({'id': kind, 'kind': kind, 'text': (kind + ' validated state ') * 20,
                            'statute': 'INPUT', 'sources': [{'kind': 'operator', 'ref': 'turn:' + kind}]})
        self.store.transition('context', SCOPE, 0, 'consolidation', OPERATOR,
                              {'records': records, 'candidates': [candidate('optional', 'optional output ' * 500)]})
        full = self.store.project('context', SCOPE, 12000)
        self.assertEqual(full['required_record_ids'], [r['id'] for r in records])
        compact = self.store.project('context', SCOPE, full['required_chars'])
        self.assertEqual(compact['included_record_ids'], full['required_record_ids'])
        self.assertEqual(compact['omitted_record_ids'], ['optional'])
        with self.assertRaises(ProjectionOverflow):
            self.store.project('context', SCOPE, full['required_chars'] - 1)
        self.assertEqual(len(self.store.get('context', SCOPE)['q']['records']), 6)

    def test_explicitly_required_candidate_never_drops_and_remains_unverified(self):
        item = candidate('required-candidate', 'Unverified but needed ' * 60)
        item['meta'] = {'required': True}
        self.store.transition('context', SCOPE, 0, 'required-event', AGENT,
                              {'candidates': [item, candidate('optional', 'Optional ' * 200)]})
        full = self.store.project('context', SCOPE)
        compact = self.store.project('context', SCOPE, full['required_chars'])
        self.assertEqual(compact['required_record_ids'], ['required-candidate'])
        self.assertEqual(compact['included_record_ids'], ['required-candidate'])
        self.assertEqual(compact['omitted_record_ids'], ['optional'])
        record = self.store.get('context', SCOPE)['q']['records'][0]
        self.assertEqual((record['kind'], record['statute']), ('candidate', 'DECLARADO'))
        with self.assertRaises(ProjectionOverflow):
            self.store.project('context', SCOPE, full['required_chars'] - 1)

    def test_database_update_delete_guards(self):
        con = sqlite3.connect(self.store.db_path)
        for query in ['DELETE FROM contexts', 'DELETE FROM events', 'UPDATE events SET state_json=\'{}\'']:
            with self.assertRaises(sqlite3.IntegrityError):
                con.execute(query)
            con.rollback()
        con.close()

    def test_tampered_blob_and_missing_guard_fail_closed(self):
        con = sqlite3.connect(self.store.db_path)
        con.execute('DROP TRIGGER contexts_no_update')
        con.execute("UPDATE contexts SET objective_blob=x'00'")
        con.commit()
        con.close()
        with self.assertRaises(IntegrityError):
            self.store.get('context', SCOPE)
        with self.assertRaises(IntegrityError):
            MemoryStore(self.root)

    def test_tampered_chain_with_guards_restored_fails(self):
        self.append()
        con = sqlite3.connect(self.store.db_path)
        trigger = con.execute("SELECT sql FROM sqlite_master WHERE name='events_no_update'").fetchone()[0]
        con.execute('DROP TRIGGER events_no_update')
        con.execute("UPDATE events SET event_hash=? WHERE revision=1", ('0' * 64,))
        con.execute(trigger)
        con.commit()
        con.close()
        with self.assertRaises(IntegrityError):
            self.store.get('context', SCOPE)

    def test_failure_after_insert_rolls_back_q_and_p(self):
        original = self.store._read
        calls = 0
        def failing(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise IntegrityError('Simulated failure before commit')
            return original(*args, **kwargs)
        with patch.object(self.store, '_read', side_effect=failing):
            with self.assertRaises(IntegrityError):
                self.store.transition('context', SCOPE, 0, 'e', AGENT,
                                      {'candidates': [candidate('r')], 'flow': {'phase': 'result_ready'}})
        state = MemoryStore(self.root).get('context', SCOPE)
        self.assertEqual(state['revision'], 0)
        self.assertEqual(state['q']['records'], [])
        self.assertEqual(state['p']['phase'], 'registered')

    def test_abrupt_process_exit_recovers_whole_previous_state(self):
        ctx = multiprocessing.get_context('spawn')
        process = ctx.Process(target=crash_after_insert, args=(str(self.root),))
        process.start()
        process.join(timeout=20)
        self.assertFalse(process.is_alive())
        self.assertEqual(process.exitcode, 73)
        recovered = MemoryStore(self.root).get('context', SCOPE)
        self.assertEqual(recovered['revision'], 0)
        self.assertEqual(recovered['q']['records'], [])
        self.assertEqual(recovered['p']['phase'], 'registered')
        self.append('recovered-event', 'recovered-record')
        self.assertEqual(self.store.get('context', SCOPE)['revision'], 1)

    def test_tampered_objective_with_guards_restored_fails(self):
        con = sqlite3.connect(self.store.db_path)
        trigger = con.execute("SELECT sql FROM sqlite_master WHERE name='contexts_no_update'").fetchone()[0]
        con.execute('DROP TRIGGER contexts_no_update')
        con.execute("UPDATE contexts SET objective_blob=x'00'")
        con.execute(trigger)
        con.commit()
        con.close()
        with self.assertRaises(IntegrityError):
            self.store.get('context', SCOPE)

    def test_validation_rejects_path_identifiers_and_nonfinite_values(self):
        for context in ['../escape', 'a/b', 'a\\b', '', 'x' * 161, 7]:
            with self.assertRaises(InvalidInput):
                self.store.ensure_context(context, objective='x', scope=SCOPE, actor=OPERATOR)
        with self.assertRaises(InvalidInput):
            self.store.ensure_context('bad', objective='x', scope=SCOPE, actor=OPERATOR, constraints={'n': float('nan')})
        with self.assertRaises(InvalidInput):
            self.store.transition('context', SCOPE, True, 'e', AGENT, {'candidates': [candidate('r')]})
        with self.assertRaises(InvalidInput):
            self.store.transition('context', SCOPE, 0, 'anchor', AGENT, {'candidates': [candidate('r')]})

    def test_concurrent_processes_no_lost_records_or_handles(self):
        ctx = multiprocessing.get_context('spawn')
        queue = ctx.Queue()
        processes = [ctx.Process(target=process_writer, args=(str(self.root), i, queue)) for i in range(5)]
        for process in processes:
            process.start()
        for process in processes:
            process.join(timeout=25)
            self.assertFalse(process.is_alive())
            self.assertEqual(process.exitcode, 0)
        results = [queue.get(timeout=5) for _ in processes]
        self.assertTrue(all(status == 'ok' for status, _ in results), results)
        state = self.store.get('shared', SCOPE)
        self.assertEqual(state['revision'], 5)
        self.assertEqual(len(state['q']['records']), 5)
        self.assertEqual(len(state['p']['handles']), 5)
        self.assertEqual({r['id'] for r in state['q']['records']}, {'record-' + str(i) for i in range(5)})
        queue.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)