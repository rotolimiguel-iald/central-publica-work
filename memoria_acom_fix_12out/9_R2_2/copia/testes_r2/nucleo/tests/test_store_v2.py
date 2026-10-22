"""Tests of schema v2 (state by delta, journal, byte snapshots, migration) — 12/10/2026.

Runs only inside the 1_NUCLEO folder (temporary directories under its tmp/, the
snapshot archive under tmp/ as well). Never touches production.
"""
import hashlib
import json
import math
import multiprocessing
import os
from pathlib import Path
import shutil
import sqlite3
import statistics
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
import warnings

import iald_memory
from iald_memory import (
    MemoryStore, IntegrityError, SchemaMigrationRequired, InvariantViolation, RevisionConflict,
)
from iald_memory import store as store_module
from iald_memory import journal, snapshots, migrate
import store_v1_frozen
from test_store import crash_after_insert

SCOPE = {'house': 'IALD', 'principal': 'operator'}
OPERATOR = {'id': 'operator', 'kind': 'operator'}
AGENT = {'id': 'coordinator', 'kind': 'agent'}
HERE = Path(__file__).resolve().parent
NUCLEO = HERE.parent
EVID = Path(os.environ.get('NUCLEO_EVIDENCIAS', NUCLEO / 'evidencias'))
SCRIPTS = NUCLEO / 'copia' / 'MEMORIA_IALD'
# Same shape as the audit's synthetic candidate (~1.313 B of canonical record JSON).
TEXT = ('heartbeat sample response text ' * 40)[:1200]

V1_SNAPSHOT_KEYS = {'context_id', 'scope', 'objective', 'objective_bytes_b64', 'objective_sha256', 'anchor_sha256',
                    'constraints', 'parent_id', 'anchor_actor', 'revision', 'q', 'p', 'state_sha256', 'receipt'}
V1_RECEIPT_KEYS = {'context_id', 'scope', 'revision', 'event_id', 'event_hash', 'objective_sha256', 'anchor_sha256',
                   'state_sha256', 'replayed'}
V1_PROJECTION_KEYS = {'text', 'receipt', 'required_record_ids', 'included_record_ids', 'omitted_record_ids', 'overflow',
                      'required_chars', 'actual_chars', 'projection_sha256', 'current_input_sha256'}
V1_VERIFY_KEYS = {'ok', 'event_count', 'objective_bytes', 'receipt', 'validation_scope'}
V1_EXPORTS = {'MemoryStore', 'MemoryError', 'InvalidInput', 'ContextNotFound', 'ScopeViolation', 'AnchorConflict',
              'RevisionConflict', 'IdempotencyConflict', 'IntegrityError', 'ProjectionOverflow', 'InvariantViolation'}


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def candidate(name, text=TEXT):
    return {'id': name, 'text': text, 'statute': 'DECLARADO', 'source': {'kind': 'executor', 'ref': 'job:' + name}}


def changes_for(i, text=TEXT):
    return {'candidates': [candidate(f'c{i}', text)], 'flow': {'phase': f'cycle-{i}'}}


def journal_lines(root, context_id):
    path = journal.path_for(Path(root) / 'journal', context_id)
    return [json.loads(line) for line in path.read_text('ascii').splitlines() if line]


def make_v1(root, plan, backups=False):
    """Build a schema-v1 database with the frozen v1 code. plan: {context_id: n_transitions}."""
    with patch.object(store_v1_frozen.MemoryStore, '_backup', lambda self: None) if not backups else _noop():
        store = store_v1_frozen.MemoryStore(root)
        heads = {}
        for context_id, count in plan.items():
            store.ensure_context(context_id, objective=f'Objective of {context_id}\r\n'.encode(), scope=SCOPE,
                                 actor=OPERATOR, constraints={'max_calls': 1})
            for i in range(count):
                store.transition(context_id, SCOPE, i, f'e{i}', AGENT, changes_for(i, TEXT[:200]))
            heads[context_id] = store.get(context_id, SCOPE)
        return heads


class _noop:
    def __enter__(self):
        return None

    def __exit__(self, *exc):
        return False


class Base(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'state'
        self.archive = Path(self.temp.name) / 'arquivo_D'
        self.warned = warnings.catch_warnings(record=True)
        self.caught = self.warned.__enter__()
        warnings.simplefilter('always')

    def tearDown(self):
        self.warned.__exit__(None, None, None)
        self.temp.cleanup()

    def store(self, root=None):
        return MemoryStore(root or self.root, snapshot_archive_dir=self.archive)

    def fill(self, store, context_id, count, start=0):
        receipt = None
        for i in range(start, start + count):
            receipt = store.transition(context_id, SCOPE, i, f'e{i}', AGENT, changes_for(i))
        return receipt


class FrozenAndContract(Base):
    def test_v1_frozen_copy_is_pinned(self):
        pinned = (HERE / 'store_v1_frozen.sha256').read_text('ascii').split()[0]
        self.assertEqual(sha256_file(HERE / 'store_v1_frozen.py'), pinned)
        self.assertTrue(pinned.startswith('2d4f6214fa433534'))
        self.assertEqual(store_v1_frozen.SCHEMA_VERSION, 1)
        self.assertEqual(store_module.SCHEMA_VERSION, 2)

    def test_public_contract_fields_unchanged(self):
        store = self.store()
        snapshot = store.ensure_context('context', objective='Objective', scope=SCOPE, actor=OPERATOR)
        self.assertEqual(set(snapshot), V1_SNAPSHOT_KEYS)
        receipt = store.transition('context', SCOPE, 0, 'e0', AGENT, changes_for(0))
        self.assertEqual(set(receipt), V1_RECEIPT_KEYS)
        self.assertEqual(set(store.get('context', SCOPE)), V1_SNAPSHOT_KEYS)
        self.assertEqual(set(store.receipt('context', SCOPE)), V1_RECEIPT_KEYS)
        self.assertEqual(set(store.project('context', SCOPE)), V1_PROJECTION_KEYS)
        verification = store.verify('context', SCOPE)
        self.assertTrue(V1_VERIFY_KEYS <= set(verification))
        self.assertEqual(verification['validation_scope'], 'local_integrity_and_replay_only')
        self.assertTrue(V1_EXPORTS <= set(iald_memory.__all__))
        self.assertIn('SchemaMigrationRequired', iald_memory.__all__)
        self.assertTrue(issubclass(SchemaMigrationRequired, IntegrityError))
        # Semantics preserved: CAS, idempotent replay, model invariant.
        replay = store.transition('context', SCOPE, 0, 'e0', AGENT, changes_for(0))
        self.assertTrue(replay['replayed'])
        with self.assertRaises(RevisionConflict):
            store.transition('context', SCOPE, 0, 'e1', AGENT, changes_for(1))
        with self.assertRaises(InvariantViolation):
            store.transition('context', SCOPE, 1, 'e1', {'id': 'm', 'kind': 'model'}, {'flow': {'phase': 'x'}})


class DeltaReplay(Base):
    def test_delta_events_store_no_state_and_replay_from_snapshot(self):
        with patch.object(store_module, 'SNAPSHOT_EVERY_EVENTS', 4):
            store = self.store()
            store.ensure_context('context', objective='Objective', scope=SCOPE, actor=OPERATOR)
            self.fill(store, 'context', 10)
            con = sqlite3.connect(str(store.db_path))
            states = con.execute("SELECT revision, state_json FROM events WHERE context_id='context' ORDER BY revision").fetchall()
            self.assertEqual([s for r, s in states if r > 0], [''] * 10)
            self.assertEqual(json.loads(states[0][1]), store_module._initial_state())
            self.assertEqual([r[0] for r in con.execute("SELECT revision FROM snapshots ORDER BY revision")], [4, 8])
            self.assertEqual(con.execute("SELECT revision FROM context_state").fetchone()[0], 10)
            con.close()
            verification = store.verify('context', SCOPE)
            self.assertEqual(verification['replay_from_revision'], 8)
            self.assertEqual((verification['legacy_events'], verification['delta_events'], verification['snapshot_rows']), (0, 10, 2))
            self.assertEqual(verification['event_count'], 11)
            deep = store.verify('context', SCOPE, deep=True)
            self.assertTrue(deep['ok'] and deep['deep'])
            self.assertEqual(deep['replay_from_revision'], 0)
            state = store.get('context', SCOPE)
            self.assertEqual([r['id'] for r in state['q']['records']], [f'c{i}' for i in range(10)])
            self.assertEqual(state['p']['phase'], 'cycle-9')

    def test_errata_and_handles_replay_identically_through_snapshots(self):
        with patch.object(store_module, 'SNAPSHOT_EVERY_EVENTS', 2):
            store = self.store()
            store.ensure_context('context', objective='Objective', scope=SCOPE, actor=OPERATOR)
            store.transition('context', SCOPE, 0, 'a', AGENT, {'candidates': [candidate('r1', 'original')],
                                                                 'flow': {'handles': [{'id': 'job', 'job_id': 'x', 'status': 'sent'}]}})
            correction = {'id': 'fix', 'kind': 'erratum', 'text': 'corrected', 'statute': 'INPUT',
                          'sources': [{'kind': 'operator', 'ref': 'turn:2'}], 'supersedes': 'r1'}
            store.transition('context', SCOPE, 1, 'b', OPERATOR, {'records': [correction]})
            store.transition('context', SCOPE, 2, 'c', AGENT, {'flow': {'handles': [{'id': 'job', 'status': 'uncertain'}, {'id': 'other', 'n': 1}]}})
            store.transition('context', SCOPE, 3, 'd', AGENT, {'flow': {'phase': 'done', 'next_action': ''}})
            state = store.get('context', SCOPE)
            self.assertEqual(state['p']['handles'], [{'id': 'job', 'job_id': 'x', 'status': 'uncertain'}, {'id': 'other', 'n': 1}])
            self.assertEqual([r['id'] for r in state['q']['records']], ['r1', 'fix'])
            self.assertEqual(store.verify('context', SCOPE)['replay_from_revision'], 4)
            self.assertTrue(store.verify('context', SCOPE, deep=True)['ok'])
            with self.assertRaises(InvariantViolation):
                store.transition('context', SCOPE, 4, 'dup', AGENT, {'candidates': [candidate('r1')]})
            projected = store.project('context', SCOPE)
            self.assertEqual(projected['required_record_ids'], ['r1', 'fix'])

    def test_stored_json_digest_equals_v1_formula_and_falls_back_when_noncanonical(self):
        """The fast digest over stored canonical JSON is the v1 formula; a row whose stored JSON is
        not canonical (impossible through the store, possible in a hand-built database) is still
        judged by the v1 formula itself, never by a different one."""
        store = self.store()
        store.ensure_context('context', objective='Objective', scope=SCOPE, actor=OPERATOR)
        self.fill(store, 'context', 3)
        con = sqlite3.connect(str(store.db_path))
        con.row_factory = sqlite3.Row
        rows = con.execute("SELECT * FROM events WHERE context_id='context' ORDER BY revision").fetchall()
        con.close()
        cid = store_module._json_str('context')
        for e in rows:
            fast = store_module._event_hash_stored(cid, e['revision'], e['event_id'], e['actor_json'], e['changes_json'],
                                                   e['state_sha256'], e['previous_hash'], e['created_at'])
            full = store_module._event_hash('context', e['revision'], e['event_id'], e['actor_json'], e['changes_json'],
                                            e['state_sha256'], e['previous_hash'], e['created_at'])
            self.assertEqual(fast, full)
            self.assertEqual(full, e['event_hash'])
        # Hand-built context whose event 1 stores NON-canonical JSON (spaces, unsorted keys) but a
        # correct v1 digest: the v2 reader must accept it (fallback), v1 frozen code agrees on the digest.
        head = store.get('context', SCOPE)
        actor_nc = '{"kind": "agent", "id": "coordinator"}'
        changes = store_module._changes(changes_for(3), AGENT)
        changes_nc = json.dumps(changes, ensure_ascii=False, indent=1)
        state = store_module._apply({'q': head['q'], 'p': head['p']}, changes)
        state_json = store_module._dump(state)
        state_sha = store_module._sha(state_json.encode('utf-8'))
        at = store_module._now()
        digest = store_v1_frozen._event_hash('context', 4, 'e3', actor_nc, changes_nc, state_sha, head['receipt']['event_hash'], at)
        self.assertNotEqual(digest, store_module._event_hash_stored(cid, 4, 'e3', actor_nc, changes_nc, state_sha,
                                                                    head['receipt']['event_hash'], at))
        con = sqlite3.connect(str(store.db_path), isolation_level=None)
        con.execute('BEGIN IMMEDIATE')
        con.execute('INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?)',
                    ('context', 4, 'e3', actor_nc, changes_nc, '', state_sha, head['receipt']['event_hash'], digest, at))
        con.execute('DROP TRIGGER context_state_no_delete')
        con.execute("DELETE FROM context_state WHERE context_id='context'")
        con.execute('INSERT INTO context_state VALUES (?,?,?,?,?,?)', ('context', 4, state_json, state_sha, digest, at))
        con.execute("CREATE TRIGGER context_state_no_delete BEFORE DELETE ON context_state BEGIN SELECT RAISE(ABORT,'materialized state is not deletable'); END")
        con.commit()
        con.close()
        read = store.get('context', SCOPE)
        self.assertEqual((read['revision'], read['receipt']['event_hash']), (4, digest))
        self.assertEqual([r['id'] for r in read['q']['records']], ['c0', 'c1', 'c2', 'c3'])
        # Tampering the non-canonical row (same parsed content is impossible to fake: any byte change
        # alters the v1 digest) is still refused.
        con = sqlite3.connect(str(store.db_path), isolation_level=None)
        con.execute('DROP TRIGGER events_no_update')
        con.execute("UPDATE events SET actor_json=? WHERE context_id='context' AND revision=4", ('{"kind": "agent", "id": "other"}',))
        con.execute("CREATE TRIGGER events_no_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT,'append-only event'); END")
        con.close()
        with self.assertRaises(IntegrityError):
            store.get('context', SCOPE)


class TamperFailsClosed(Base):
    def prepared(self):
        with patch.object(store_module, 'SNAPSHOT_EVERY_EVENTS', 3):
            store = self.store()
            store.ensure_context('context', objective='Objective', scope=SCOPE, actor=OPERATOR)
            self.fill(store, 'context', 5)
        return store

    def test_materialized_row_tamper_fails_closed(self):
        store = self.prepared()
        con = sqlite3.connect(str(store.db_path))
        con.execute("UPDATE context_state SET state_json='{}'")
        con.commit()
        con.close()
        with self.assertRaises(IntegrityError) as caught:
            store.get('context', SCOPE)
        self.assertIn('Materialized', str(caught.exception))
        with self.assertRaises(IntegrityError):
            store.transition('context', SCOPE, 5, 'e5', AGENT, changes_for(5))

    def test_context_state_revision_lag_fails_closed(self):
        store = self.prepared()
        con = sqlite3.connect(str(store.db_path))
        con.execute('UPDATE context_state SET revision=revision-1')
        con.commit()
        con.close()
        with self.assertRaises(IntegrityError) as caught:
            store.get('context', SCOPE)
        self.assertIn('lags', str(caught.exception))

    def test_snapshot_row_tamper_fails_closed(self):
        store = self.prepared()
        con = sqlite3.connect(str(store.db_path))
        for query in ['DELETE FROM snapshots', "UPDATE snapshots SET state_json='{}'", 'DELETE FROM context_state']:
            with self.assertRaises(sqlite3.IntegrityError):
                con.execute(query)
            con.rollback()
        trigger = con.execute("SELECT sql FROM sqlite_master WHERE name='snapshots_no_update'").fetchone()[0]
        con.execute('DROP TRIGGER snapshots_no_update')
        con.execute("UPDATE snapshots SET state_json=replace(state_json, 'cycle-2', 'cycle-X') WHERE revision=3")
        con.execute(trigger)
        con.commit()
        con.close()
        with self.assertRaises(IntegrityError) as caught:
            store.get('context', SCOPE)
        self.assertIn('snapshot', str(caught.exception).lower())
        with self.assertRaises(IntegrityError):
            store.verify('context', SCOPE, deep=True)

    def test_delta_event_tamper_fails_closed(self):
        store = self.prepared()
        con = sqlite3.connect(str(store.db_path))
        trigger = con.execute("SELECT sql FROM sqlite_master WHERE name='events_no_update'").fetchone()[0]
        con.execute('DROP TRIGGER events_no_update')
        con.execute("UPDATE events SET changes_json=replace(changes_json, 'cycle-4', 'cycle-Z') WHERE revision=5")
        con.execute(trigger)
        con.commit()
        con.close()
        with self.assertRaises(IntegrityError) as caught:
            store.get('context', SCOPE)
        self.assertIn('digest', str(caught.exception).lower())

    def test_stray_snapshot_beyond_head_fails_closed(self):
        store = self.prepared()
        con = sqlite3.connect(str(store.db_path))
        row = con.execute("SELECT state_json, state_sha256, event_hash, created_at FROM snapshots WHERE revision=3").fetchone()
        con.execute('INSERT INTO snapshots VALUES (?,?,?,?,?,?,?)', ('context', 9, *row, 'test'))
        con.commit()
        con.close()
        with self.assertRaises(IntegrityError):
            store.get('context', SCOPE)


class Journal(Base):
    def test_journal_written_before_commit_and_orphan_voided(self):
        store = self.store()
        store.ensure_context('context', objective='Objective', scope=SCOPE, actor=OPERATOR)
        original = store._read
        calls = 0
        def failing(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise IntegrityError('Simulated failure after journal append, before commit')
            return original(*args, **kwargs)
        with patch.object(store, '_read', side_effect=failing):
            with self.assertRaises(IntegrityError):
                store.transition('context', SCOPE, 0, 'lost', AGENT, changes_for(0))
        self.assertEqual(self.store().get('context', SCOPE)['revision'], 0)
        lines = journal_lines(self.root, 'context')
        self.assertEqual([l['kind'] for l in lines], ['anchor', 'event'])
        self.assertEqual(lines[1]['event_id'], 'lost')
        verification = store.verify('context', SCOPE)
        self.assertTrue(verification['journal_ok'])
        self.assertEqual(verification['journal_orphans'], 1)
        receipt = store.transition('context', SCOPE, 0, 'kept', AGENT, changes_for(0))
        lines = journal_lines(self.root, 'context')
        self.assertEqual([l['kind'] for l in lines], ['anchor', 'event', 'void', 'event'])
        self.assertEqual(lines[2]['voids_seq'], 2)
        self.assertEqual(lines[2]['voids_line_sha256'], lines[1]['line_sha256'])
        self.assertEqual(lines[2]['reason'], 'not_committed')
        self.assertEqual(lines[3]['event_hash'], receipt['event_hash'])
        self.assertEqual([l['seq'] for l in lines], [1, 2, 3, 4])
        self.assertTrue(journal.verify_lines(lines)['chain_ok'])
        verification = store.verify('context', SCOPE)
        self.assertTrue(verification['ok'] and verification['journal_ok'])
        self.assertEqual((verification['journal_voided'], verification['journal_orphans'], verification['journal_lines']), (1, 0, 4))

    def test_abrupt_exit_after_journal_append_voids_orphan(self):
        store = self.store()
        store.ensure_context('context', objective='Objective', scope=SCOPE, actor=OPERATOR)
        ctx = multiprocessing.get_context('spawn')
        process = ctx.Process(target=crash_after_insert, args=(str(self.root),))
        process.start()
        process.join(timeout=30)
        self.assertEqual(process.exitcode, 73)
        self.assertEqual([l['kind'] for l in journal_lines(self.root, 'context')], ['anchor', 'event'])
        self.assertEqual(self.store().get('context', SCOPE)['revision'], 0)
        store.transition('context', SCOPE, 0, 'after', AGENT, changes_for(0))
        self.assertEqual([l['kind'] for l in journal_lines(self.root, 'context')], ['anchor', 'event', 'void', 'event'])
        self.assertTrue(store.verify('context', SCOPE)['ok'])

    def test_journal_missing_or_truncated_is_visible(self):
        store = self.store()
        store.ensure_context('context', objective='Objective', scope=SCOPE, actor=OPERATOR)
        self.fill(store, 'context', 2)
        path = journal.path_for(self.root / 'journal', 'context')
        raw = path.read_bytes()
        path.write_bytes(raw + b'{"seq":4,"kind":"event","partial')  # crash mid-write
        verification = store.verify('context', SCOPE)
        self.assertTrue(verification['journal_ok'])
        self.assertEqual(verification['journal_malformed_lines'], 1)
        store.transition('context', SCOPE, 2, 'e2', AGENT, changes_for(2))
        lines = journal_lines(self.root, 'context') if False else None
        parsed, malformed, ends = journal.read_all(path)
        self.assertEqual((len(parsed), malformed, ends), (4, 1, True))
        self.assertTrue(journal.verify_lines(parsed)['chain_ok'])
        path.unlink()
        verification = store.verify('context', SCOPE)
        self.assertFalse(verification['ok'])
        self.assertFalse(verification['journal_ok'])
        self.assertEqual(verification['journal_missing_events'], 4)
        self.assertEqual(store.get('context', SCOPE)['revision'], 3)  # reads never depend on the journal

    def test_journal_chain_and_rebuild_equals_db(self):
        with patch.object(store_module, 'SNAPSHOT_EVERY_EVENTS', 3):
            store = self.store()
            store.ensure_context('alpha', objective=b'Alpha\r\n original bytes', scope=SCOPE, actor=OPERATOR, constraints={'k': [1, 2]})
            store.ensure_context('beta:child', objective='Beta', scope=SCOPE, actor=AGENT, parent_id='alpha')
            self.fill(store, 'alpha', 7)
            store.transition('beta:child', SCOPE, 0, 'x', AGENT, {'candidates': [candidate('r1', 'original')],
                                                                   'flow': {'handles': [{'id': 'job', 'status': 'sent'}]}})
            store.transition('beta:child', SCOPE, 1, 'y', OPERATOR, {'records': [{'id': 'fix', 'kind': 'erratum', 'text': 'corr', 'statute': 'INPUT',
                                                                                    'sources': [{'kind': 'operator', 'ref': 't'}], 'supersedes': 'r1'}]})
            before = {c: store.get(c, SCOPE) for c in ('alpha', 'beta:child')}
            self.assertTrue((self.root / 'journal' / 'beta%3Achild.events.jsonl').exists())
            out = Path(self.temp.name) / 'rebuilt'
            report = migrate.rebuild_from_journal(self.root / 'journal', out, snapshot_archive_dir=self.archive)
            self.assertTrue(report['ok'])
            rebuilt = MemoryStore(out, snapshot_archive_dir=self.archive)
            for context_id, snapshot in before.items():
                after = rebuilt.get(context_id, SCOPE)
                self.assertEqual(after, snapshot)
                deep = rebuilt.verify(context_id, SCOPE, deep=True)
                self.assertTrue(deep['ok'] and deep['journal_ok'])
                self.assertEqual(deep['receipt'], snapshot['receipt'])
            with self.assertRaises(IntegrityError):
                migrate.rebuild_from_journal(self.root / 'journal', out, snapshot_archive_dir=self.archive)

    def test_journal_tail_cache_validated_by_stat_across_instances(self):
        """Two store instances on the same root alternate appends: a stale in-memory tail must be
        rejected by the stat check (size + mtime_ns) and re-read, so the chain stays unbroken and
        no void line is written. A cache hit never skips a real orphan either."""
        a = self.store()
        b = self.store()
        a.ensure_context('context', objective='Objective', scope=SCOPE, actor=OPERATOR)
        a.transition('context', SCOPE, 0, 'a0', AGENT, changes_for(0))   # a: cache hit path (own tail)
        self.assertEqual(a._journal_tails['context']['last']['revision'], 1)
        b.transition('context', SCOPE, 1, 'b1', AGENT, changes_for(1))   # b: no cache, reads the file
        a.transition('context', SCOPE, 2, 'a2', AGENT, changes_for(2))   # a: stale cache -> stat mismatch -> re-read
        b.transition('context', SCOPE, 3, 'b3', AGENT, changes_for(3))
        lines = journal_lines(self.root, 'context')
        self.assertEqual([l['kind'] for l in lines], ['anchor', 'event', 'event', 'event', 'event'])
        self.assertEqual([l['revision'] for l in lines], [0, 1, 2, 3, 4])
        self.assertTrue(journal.verify_lines(lines)['chain_ok'])
        for store in (a, b):
            verification = store.verify('context', SCOPE)
            self.assertTrue(verification['ok'] and verification['journal_ok'])
            self.assertEqual((verification['journal_voided'], verification['journal_orphans']), (0, 0))
        # A failed transition drops the cache entry; the orphan is voided on the next append.
        original = a._read
        calls = {'n': 0}
        def failing(*args, **kwargs):
            calls['n'] += 1
            if calls['n'] == 2:
                raise IntegrityError('Simulated failure after journal append, before commit')
            return original(*args, **kwargs)
        with patch.object(a, '_read', side_effect=failing):
            with self.assertRaises(IntegrityError):
                a.transition('context', SCOPE, 4, 'a4', AGENT, changes_for(4))
        self.assertNotIn('context', a._journal_tails)
        a.transition('context', SCOPE, 4, 'a4bis', AGENT, changes_for(4))
        lines = journal_lines(self.root, 'context')
        self.assertEqual([l['kind'] for l in lines][-3:], ['event', 'void', 'event'])
        self.assertTrue(journal.verify_lines(lines)['chain_ok'])
        verification = a.verify('context', SCOPE)
        self.assertTrue(verification['ok'] and verification['journal_ok'])
        self.assertEqual((verification['journal_voided'], verification['journal_orphans']), (1, 0))


class SnapshotPolicy(Base):
    def test_snapshot_policy_50_mutations(self):
        store = self.store()
        store.ensure_context('context', objective='Objective', scope=SCOPE, actor=OPERATOR)
        self.fill(store, 'context', 48)  # 49 mutations
        self.assertEqual(snapshots.list_snapshots(self.root / 'snapshots'), [])
        policy = store.snapshot_policy()
        self.assertEqual((policy['mutations_since_snapshot'], policy['snapshots_taken']), (49, 0))
        self.fill(store, 'context', 1, start=48)  # 50th mutation
        taken = snapshots.list_snapshots(self.root / 'snapshots')
        self.assertEqual(len(taken), 1)
        digest = sha256_file(taken[0])
        self.assertTrue(taken[0].name.endswith('_' + digest[:16]))
        self.assertEqual(Path(str(taken[0]) + '.sha256').read_text('ascii').split()[0], digest)
        copy = sqlite3.connect(f'file:{taken[0].as_posix()}?mode=ro', uri=True)
        self.assertEqual(copy.execute("SELECT max(revision) FROM events WHERE context_id='context'").fetchone()[0], 48)
        copy.close()
        policy = store.snapshot_policy()
        self.assertEqual((policy['mutations_since_snapshot'], policy['snapshots_taken']), (0, 1))
        self.assertEqual(policy['last_snapshot'], taken[0].name)
        self.fill(store, 'context', 49, start=49)
        self.assertEqual(len(snapshots.list_snapshots(self.root / 'snapshots')), 1)
        self.fill(store, 'context', 1, start=98)
        self.assertEqual(len(snapshots.list_snapshots(self.root / 'snapshots')), 2)
        self.assertEqual(list(self.root.glob('memory.sqlite3.bak_*')), [])
        self.assertFalse((self.root / 'snapshot_policy.json').exists())  # the counter is a row of the database
        con = sqlite3.connect(str(store.db_path))
        try:
            row = json.loads(con.execute('SELECT policy_json FROM snapshot_policy WHERE id=1').fetchone()[0])
            with self.assertRaises(sqlite3.IntegrityError):
                con.execute('DELETE FROM snapshot_policy')
        finally:
            con.close()
        self.assertEqual(row, store.snapshot_policy())
        self.assertEqual((row['mutations_since_snapshot'], row['snapshots_taken']), (0, 2))

    def test_snapshot_policy_counts_committed_mutations_only(self):
        """A mutation that fails after the policy was evaluated does not advance the counter."""
        store = self.store()
        store.ensure_context('context', objective='Objective', scope=SCOPE, actor=OPERATOR)
        self.fill(store, 'context', 2)
        self.assertEqual(store.snapshot_policy()['mutations_since_snapshot'], 3)
        original = store._read
        calls = {'n': 0}
        def failing(*args, **kwargs):
            calls['n'] += 1
            if calls['n'] == 2:
                raise RuntimeError('simulated failure after insert')
            return original(*args, **kwargs)
        with patch.object(store, '_read', side_effect=failing):
            with self.assertRaises(RuntimeError):
                store.transition('context', SCOPE, 2, 'e2', AGENT, changes_for(2))
        self.assertEqual(store.snapshot_policy()['mutations_since_snapshot'], 3)
        self.assertEqual(store.get('context', SCOPE)['revision'], 2)

    def test_snapshot_policy_60_minutes(self):
        store = self.store()
        clock = [1_800_000_000.0]
        store._clock = lambda: clock[0]
        store.ensure_context('context', objective='Objective', scope=SCOPE, actor=OPERATOR)
        clock[0] += 3599
        self.fill(store, 'context', 1)
        self.assertEqual(snapshots.list_snapshots(self.root / 'snapshots'), [])
        clock[0] += 1  # 3600 s since the window started
        self.fill(store, 'context', 1, start=1)
        self.assertEqual(len(snapshots.list_snapshots(self.root / 'snapshots')), 1)
        policy = store.snapshot_policy()
        self.assertEqual(policy['mutations_since_snapshot'], 0)
        self.assertEqual(policy['window_started_at'], clock[0])
        clock[0] += 3599
        self.fill(store, 'context', 1, start=2)
        self.assertEqual(len(snapshots.list_snapshots(self.root / 'snapshots')), 1)
        clock[0] += 1
        self.fill(store, 'context', 1, start=3)
        self.assertEqual(len(snapshots.list_snapshots(self.root / 'snapshots')), 2)

    def test_snapshot_keep3_and_archive_move_verified(self):
        with patch.object(snapshots, 'SNAPSHOT_EVERY_MUTATIONS', 2):
            store = self.store()
            store.ensure_context('context', objective='Objective', scope=SCOPE, actor=OPERATOR)
            self.fill(store, 'context', 11)  # 12 mutations -> 6 snapshots
        local = snapshots.list_snapshots(self.root / 'snapshots')
        archived = snapshots.list_snapshots(self.archive)
        self.assertEqual((len(local), len(archived)), (3, 3))
        self.assertLess(max(p.name for p in archived), min(p.name for p in local))
        manifest = [json.loads(l) for l in (self.archive / 'MANIFEST.jsonl').read_text('utf-8').splitlines()]
        self.assertEqual([m['name'] for m in manifest], [p.name for p in archived])
        for entry, path in zip(manifest, archived):
            self.assertEqual(sha256_file(path), entry['sha256'])
            self.assertEqual(path.stat().st_size, entry['bytes'])
            self.assertEqual(Path(str(path) + '.sha256').read_text('ascii').split()[0], entry['sha256'])
        for path in local:
            self.assertEqual(Path(str(path) + '.sha256').read_text('ascii').split()[0], sha256_file(path))
        self.assertEqual(len(list((self.root / 'snapshots').glob('*.sha256'))), 3)
        self.assertEqual(self.caught, [])

    def test_archive_unavailable_keeps_local_copies(self):
        blocked = Path(self.temp.name) / 'arquivo_D'
        blocked.write_bytes(b'not a directory')  # the archive path cannot be created
        with patch.object(snapshots, 'SNAPSHOT_EVERY_MUTATIONS', 2):
            store = MemoryStore(self.root, snapshot_archive_dir=blocked)
            store.ensure_context('context', objective='Objective', scope=SCOPE, actor=OPERATOR)
            self.fill(store, 'context', 11)
        self.assertEqual(len(snapshots.list_snapshots(self.root / 'snapshots')), 6)
        avisos = [json.loads(l) for l in (self.root / 'snapshots' / 'AVISOS.jsonl').read_text('utf-8').splitlines()]
        self.assertGreaterEqual(len(avisos), 3)
        self.assertTrue(all('local snapshot kept' in a['message'] for a in avisos))
        self.assertTrue(any(issubclass(w.category, RuntimeWarning) for w in self.caught))
        self.assertEqual(store.get('context', SCOPE)['revision'], 11)  # mutations never blocked by the archive

    def test_due_snapshot_that_does_not_verify_fails_the_mutation(self):
        with patch.object(snapshots, 'SNAPSHOT_EVERY_MUTATIONS', 2):
            store = self.store()
            store.ensure_context('context', objective='Objective', scope=SCOPE, actor=OPERATOR)
            with patch.object(snapshots, 'sha256_file', lambda path: '0' * 64):
                with self.assertRaises(IntegrityError):
                    self.fill(store, 'context', 1)
            self.assertEqual(store.get('context', SCOPE)['revision'], 0)
            self.assertEqual(snapshots.list_snapshots(self.root / 'snapshots'), [])


class ArchiveLegacyBackups(Base):
    def synthetic_state(self, count):
        state = Path(self.temp.name) / f'state_{count}'
        state.mkdir()
        (state / 'memory.sqlite3').write_bytes(b'LIVE DATABASE BYTES')
        (state / 'snapshots').mkdir()
        (state / 'snapshots' / 'memory.sqlite3.snap_x').write_bytes(b'snap')
        (state / 'journal').mkdir()
        (state / 'journal' / 'c.events.jsonl').write_bytes(b'{}\n')
        names = []
        for i in range(count):
            name = f'memory.sqlite3.bak_20261010_{90000 + i:06d}_{i:06d}_{i:08x}'
            (state / name).write_bytes(os.urandom(64) + bytes([i]))
            names.append(name)
        return state, names

    def test_archive_legacy_backups_mover_manifest_and_sha(self):
        state, names = self.synthetic_state(12)
        before = {n: sha256_file(state / n) for n in names}
        dest = Path(self.temp.name) / 'D_backups'
        plan = snapshots.archive_legacy_backups(state, dest, keep=3, dry_run=True)
        self.assertEqual((plan['to_move'], plan['moved']), (9, 0))
        self.assertFalse(dest.exists())
        report = snapshots.archive_legacy_backups(state, dest, keep=3)
        self.assertEqual((report['found'], report['to_move'], report['moved'], report['failed']), (12, 9, 9, None))
        self.assertEqual(report['kept'], names[-3:])
        self.assertEqual(sorted(p.name for p in state.glob('memory.sqlite3.bak_*')), names[-3:])
        self.assertEqual((state / 'memory.sqlite3').read_bytes(), b'LIVE DATABASE BYTES')
        self.assertTrue((state / 'snapshots' / 'memory.sqlite3.snap_x').exists())
        self.assertTrue((state / 'journal' / 'c.events.jsonl').exists())
        manifest = [json.loads(l) for l in (dest / 'MANIFEST.jsonl').read_text('utf-8').splitlines()]
        self.assertEqual([m['name'] for m in manifest], names[:9])
        for entry in manifest:
            self.assertEqual(sha256_file(dest / entry['name']), entry['sha256'])
            self.assertEqual(entry['sha256'], before[entry['name']])
        consolidated = json.loads((dest / 'MANIFEST.json').read_text('utf-8'))
        self.assertEqual((consolidated['moved'], consolidated['manifest_lines']), (9, 9))
        self.assertEqual(consolidated['manifest_jsonl_sha256'], sha256_file(dest / 'MANIFEST.jsonl'))
        again = snapshots.archive_legacy_backups(state, dest, keep=3)
        self.assertEqual((again['found'], again['to_move'], again['moved']), (3, 0, 0))

    def test_archive_legacy_backups_corrupt_copy_aborts_without_deleting(self):
        state, names = self.synthetic_state(5)
        dest = Path(self.temp.name) / 'D_backups'
        real = snapshots._copy_bytes
        def corrupting(src, dst):
            if Path(src).name == names[2]:
                Path(dst).write_bytes(b'corrupted copy')
                return len(b'corrupted copy'), hashlib.sha256(b'corrupted copy').hexdigest()
            return real(src, dst)
        with patch.object(snapshots, '_copy_bytes', corrupting):
            report = snapshots.archive_legacy_backups(state, dest, keep=0)
        self.assertEqual((report['moved'], report['failed']['name']), (2, names[2]))
        self.assertEqual(sorted(p.name for p in state.glob('memory.sqlite3.bak_*')), names[2:])
        self.assertTrue(any(p.name.endswith('.mismatch') for p in dest.iterdir()))
        self.assertFalse((dest / names[2]).exists())


class Migration(Base):
    def migrated(self, plan=None):
        plan = plan or {'alpha': 200, 'beta': 5, 'gamma': 0}
        heads = make_v1(self.root, plan)
        con = sqlite3.connect(str(self.root / 'memory.sqlite3'))
        rows_before = con.execute('SELECT * FROM events ORDER BY context_id, revision').fetchall()
        contexts_before = con.execute('SELECT * FROM contexts ORDER BY context_id').fetchall()
        con.close()
        return heads, rows_before, contexts_before

    def test_legacy_v1_db_refused_without_migration(self):
        make_v1(self.root, {'alpha': 3})
        digest = sha256_file(self.root / 'memory.sqlite3')
        with self.assertRaises(SchemaMigrationRequired):
            MemoryStore(self.root)
        with self.assertRaises(IntegrityError):
            MemoryStore(self.root)
        self.assertEqual(sha256_file(self.root / 'memory.sqlite3'), digest)
        self.assertFalse((self.root / 'journal').exists())
        self.assertEqual(migrate.inspect(self.root)['schema_version'], '1')

    def test_migration_dry_run_writes_nothing(self):
        heads, _, _ = self.migrated({'alpha': 20})
        digest = sha256_file(self.root / 'memory.sqlite3')
        receipt = migrate.migrate(self.root, apply=False, snapshot_archive_dir=self.archive)
        self.assertTrue(receipt['dry_run'])
        self.assertEqual(receipt['contexts']['alpha']['head_state_sha256'], heads['alpha']['state_sha256'])
        self.assertEqual(sha256_file(self.root / 'memory.sqlite3'), digest)
        self.assertEqual(list(self.root.glob('memory.sqlite3.pre_v2_*')), [])
        self.assertFalse((self.root / 'journal').exists())
        with self.assertRaises(SchemaMigrationRequired):
            MemoryStore(self.root)

    def test_migration_preserves_head_state_sha_and_chain(self):
        heads, rows_before, contexts_before = self.migrated()
        second = Path(self.temp.name) / 'D_pre_v2'
        receipt = migrate.migrate(self.root, apply=True, second_copy_dir=second, snapshot_archive_dir=self.archive)
        self.assertTrue(receipt['ok'] and not receipt['already_migrated'] and receipt['head_mismatches'] == [])
        backup = Path(receipt['backup']['path'])
        self.assertTrue(backup.exists() and backup.name.startswith('memory.sqlite3.pre_v2_'))
        self.assertEqual(sha256_file(backup), receipt['backup']['sha256'])
        self.assertEqual(Path(str(backup) + '.sha256').read_text('ascii').split()[0], receipt['backup']['sha256'])
        self.assertEqual(sha256_file(second / backup.name), receipt['backup']['sha256'])
        con = sqlite3.connect(str(self.root / 'memory.sqlite3'))
        self.assertEqual(con.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()[0], '2')
        self.assertIsNotNone(con.execute("SELECT value FROM metadata WHERE key='schema_upgrade_2_at'").fetchone())
        self.assertEqual(con.execute('SELECT * FROM events ORDER BY context_id, revision').fetchall(), rows_before)
        self.assertEqual(con.execute('SELECT * FROM contexts ORDER BY context_id').fetchall(), contexts_before)
        snaps = con.execute('SELECT context_id, revision, reason FROM snapshots ORDER BY context_id').fetchall()
        self.assertEqual(snaps, [('alpha', 200, 'migration_v2'), ('beta', 5, 'migration_v2'), ('gamma', 0, 'migration_v2')])
        self.assertEqual(con.execute('SELECT context_id, revision FROM context_state ORDER BY context_id').fetchall(),
                         [('alpha', 200), ('beta', 5), ('gamma', 0)])
        with self.assertRaises(sqlite3.IntegrityError):
            con.execute("UPDATE metadata SET value='3' WHERE key='schema_version'")
        con.rollback()
        con.close()
        store = self.store()
        for context_id, head in heads.items():
            verification = store.verify(context_id, SCOPE, deep=True)
            self.assertTrue(verification['ok'] and verification['journal_ok'])
            self.assertEqual(verification['receipt'], head['receipt'])
            self.assertEqual(verification['legacy_events'], head['revision'])
            self.assertEqual(verification['delta_events'], 0)
            self.assertEqual(verification['replay_from_revision'], 0)
            self.assertEqual(store.verify(context_id, SCOPE)['replay_from_revision'], head['revision'])
            after = store.get(context_id, SCOPE)
            self.assertEqual(after, head)
            lines = journal_lines(self.root, context_id)
            self.assertEqual(len(lines), head['revision'] + 1)
            self.assertTrue(all(l['legacy'] for l in lines))
            self.assertEqual(lines[0]['kind'], 'anchor')
            self.assertEqual(lines[-1]['event_hash'], head['receipt']['event_hash'])
        self.assertEqual(receipt['verify_after']['alpha']['receipt']['state_sha256'], heads['alpha']['state_sha256'])

    def test_migration_is_idempotent(self):
        self.migrated({'alpha': 10})
        migrate.migrate(self.root, apply=True, snapshot_archive_dir=self.archive)
        digest = sha256_file(self.root / 'memory.sqlite3')
        journal_bytes = (self.root / 'journal' / 'alpha.events.jsonl').stat().st_size
        backups = sorted(self.root.glob('memory.sqlite3.pre_v2_*'))
        again = migrate.migrate(self.root, apply=True, snapshot_archive_dir=self.archive)
        self.assertTrue(again['already_migrated'])
        self.assertTrue(all(v['ok'] for v in again['verify_after'].values()))
        self.assertEqual(sha256_file(self.root / 'memory.sqlite3'), digest)
        self.assertEqual((self.root / 'journal' / 'alpha.events.jsonl').stat().st_size, journal_bytes)
        self.assertEqual(sorted(self.root.glob('memory.sqlite3.pre_v2_*')), backups)
        # Journal bootstrap is idempotent on its own as well (partial re-run).
        con = migrate._connect(self.root / 'memory.sqlite3')
        try:
            chain = migrate.replay_v1_context(con, 'alpha')['chain']
        finally:
            con.close()
        self.assertEqual(journal.append_many(self.root / 'journal', 'alpha', chain), 0)

    def test_mixed_legacy_delta_replay(self):
        heads, _, _ = self.migrated({'alpha': 200})
        migrate.migrate(self.root, apply=True, snapshot_archive_dir=self.archive)
        store = self.store()
        self.fill(store, 'alpha', 60, start=200)
        state = store.get('alpha', SCOPE)
        self.assertEqual(state['revision'], 260)
        self.assertEqual(len(state['q']['records']), 260)
        self.assertEqual(state['p']['phase'], 'cycle-259')
        self.assertEqual(store.project('alpha', SCOPE, 4000)['receipt'], state['receipt'])
        verification = store.verify('alpha', SCOPE)
        self.assertTrue(verification['ok'])
        self.assertEqual((verification['legacy_events'], verification['delta_events']), (200, 60))
        self.assertEqual(verification['replay_from_revision'], 256)
        self.assertEqual(verification['snapshot_rows'], 2)
        self.assertTrue(store.verify('alpha', SCOPE, deep=True)['ok'])
        con = sqlite3.connect(str(self.root / 'memory.sqlite3'))
        empties = con.execute("SELECT revision FROM events WHERE context_id='alpha' AND state_json='' ORDER BY revision").fetchall()
        self.assertEqual([r[0] for r in empties], list(range(201, 261)))
        self.assertEqual(con.execute("SELECT revision, reason FROM snapshots WHERE context_id='alpha' ORDER BY revision").fetchall(),
                         [(200, 'migration_v2'), (256, 'periodic')])
        con.close()
        self.assertEqual(len(journal_lines(self.root, 'alpha')), 261)

    def test_v1_code_refuses_v2_schema(self):
        self.migrated({'alpha': 3})
        migrate.migrate(self.root, apply=True, snapshot_archive_dir=self.archive)
        with self.assertRaises(store_v1_frozen.IntegrityError) as caught:
            store_v1_frozen.MemoryStore(self.root)
        self.assertIn('Unsupported or missing memory schema', str(caught.exception))

    def test_covering_index_serves_chain_reads_without_legacy_state(self):
        big = TEXT * 4  # ~5 KB per candidate -> legacy state_json grows to ~0.6 MB
        with patch.object(store_v1_frozen.MemoryStore, '_backup', lambda self: None):
            v1 = store_v1_frozen.MemoryStore(self.root)
            v1.ensure_context('heavy', objective='Heavy', scope=SCOPE, actor=OPERATOR)
            for i in range(120):
                v1.transition('heavy', SCOPE, i, f'e{i}', AGENT, changes_for(i, big))
            t0 = time.perf_counter()
            v1_get = v1.get('heavy', SCOPE)
            v1_seconds = time.perf_counter() - t0
        inspected = migrate.inspect(self.root)
        migrate.migrate(self.root, apply=True, snapshot_archive_dir=self.archive)
        store = self.store()
        con = sqlite3.connect(str(self.root / 'memory.sqlite3'))
        plan = ' '.join(r[3] for r in con.execute(
            f'EXPLAIN QUERY PLAN SELECT {store_module._CHAIN_COLUMNS} FROM events WHERE context_id=? ORDER BY revision', ('heavy',)))
        con.close()
        self.assertIn('COVERING INDEX events_chain_idx', plan)
        times = []
        for _ in range(5):
            t0 = time.perf_counter()
            v2_get = store.get('heavy', SCOPE)
            times.append(time.perf_counter() - t0)
        self.assertEqual(v2_get, v1_get)
        evidence = {'legacy_sum_state_json_chars': inspected['sum_state_json_chars'], 'events': 121,
                    'v1_get_seconds': round(v1_seconds, 4), 'v2_get_seconds_median': round(statistics.median(times), 4),
                    'query_plan': plan}
        (EVID / 'indice_cobertura_legado.json').write_text(json.dumps(evidence, indent=1), encoding='utf-8')
        self.assertLess(statistics.median(times), v1_seconds)


class Scripts(Base):
    def run_script(self, name, *args):
        env = dict(os.environ)
        proc = subprocess.run([sys.executable, '-X', 'utf8', str(SCRIPTS / name), *args], capture_output=True,
                              text=True, encoding='utf-8', env=env, cwd=str(self.temp.name))
        return proc.returncode, proc.stdout, proc.stderr

    def test_migrar_para_delta_cli_dry_run_apply_verify(self):
        make_v1(self.root, {'alpha': 8, 'beta': 2})
        archive = ['--snapshot-archive-dir', str(self.archive)]
        code, out, err = self.run_script('migrar_para_delta.py', '--state', str(self.root), *archive)
        self.assertEqual(code, 0, err)
        self.assertTrue(json.loads(out)['dry_run'])
        receipt_path = Path(self.temp.name) / 'MIGRACAO_RECIBO.json'
        code, out, err = self.run_script('migrar_para_delta.py', '--state', str(self.root), '--apply',
                                         '--second-copy-dir', str(Path(self.temp.name) / 'D_pre_v2'),
                                         '--receipt', str(receipt_path), *archive)
        self.assertEqual(code, 0, err)
        receipt = json.loads(receipt_path.read_text('utf-8'))
        self.assertTrue(receipt['ok'] and receipt['backup']['second_copy'])
        self.assertEqual(receipt['after']['schema_version'], '2')
        code, out, err = self.run_script('migrar_para_delta.py', '--state', str(self.root), '--verify-only', '--deep', *archive)
        self.assertEqual(code, 0, err)
        self.assertTrue(json.loads(out)['ok'])
        code, out, err = self.run_script('migrar_para_delta.py', '--state', str(self.root), '--apply', *archive)
        self.assertEqual(code, 0, err)
        self.assertTrue(json.loads(out)['already_migrated'])
        rebuilt = Path(self.temp.name) / 'rebuilt'
        code, out, err = self.run_script('migrar_para_delta.py', '--state', str(self.root), '--rebuild-from-journal', str(rebuilt), *archive)
        self.assertEqual(code, 0, err)
        self.assertTrue(json.loads(out)['ok'])
        self.assertEqual(MemoryStore(rebuilt, snapshot_archive_dir=self.archive).get('alpha', SCOPE), self.store().get('alpha', SCOPE))
        code, out, err = self.run_script('migrar_para_delta.py', '--state', str(Path(self.temp.name) / 'nowhere'))
        self.assertEqual(code, 1)
        self.assertFalse(json.loads(out)['ok'])

    def test_mover_backups_antigos_cli(self):
        state = Path(self.temp.name) / 'state_bak'
        state.mkdir()
        (state / 'memory.sqlite3').write_bytes(b'LIVE')
        names = [f'memory.sqlite3.bak_20261011_{100000 + i:06d}_{i:06d}_{i:08x}' for i in range(6)]
        for i, name in enumerate(names):
            (state / name).write_bytes(bytes([i]) * 100)
        dest = Path(self.temp.name) / 'D_backups'
        code, out, err = self.run_script('mover_backups_antigos.py', '--state', str(state), '--dest', str(dest), '--keep', '3', '--dry-run')
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)['to_move'], 3)
        self.assertEqual(len(list(state.glob('memory.sqlite3.bak_*'))), 6)
        code, out, err = self.run_script('mover_backups_antigos.py', '--state', str(state), '--dest', str(dest), '--keep', '3')
        self.assertEqual(code, 0, err)
        report = json.loads(out)
        self.assertEqual((report['moved'], report['ok'], report['kept']), (3, True, names[3:]))
        self.assertEqual(sorted(p.name for p in state.glob('memory.sqlite3.bak_*')), names[3:])
        self.assertEqual((state / 'memory.sqlite3').read_bytes(), b'LIVE')
        self.assertEqual(sorted(p.name for p in dest.iterdir() if p.name.startswith('memory.sqlite3.bak_')), names[:3])


class GrowthN300(unittest.TestCase):
    """N=300 candidates of ~1.3 KB in one context: bytes of the database, the journal and the
    byte snapshots at N=100/200/300 and the time per transition. The audit measured v1 exponents
    of 1.87 (database), 2.78 (per-mutation backups) and 1.36 (time) between N=50 and N=150."""
    N = 300
    metrics = None

    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        root, archive = Path(cls.temp.name) / 'state', Path(cls.temp.name) / 'arquivo_D'
        store = MemoryStore(root, snapshot_archive_dir=archive)
        store.ensure_context('growth', objective='Growth objective', scope=SCOPE, actor=OPERATOR)
        changes_bytes, seconds, checkpoints = [], [], {}
        for i in range(cls.N):
            changes = changes_for(i)
            changes_bytes.append(len(store_module._dump(store_module._changes(changes, AGENT)).encode('utf-8')))
            t0 = time.perf_counter()
            store.transition('growth', SCOPE, i, f'e{i}', AGENT, changes)
            seconds.append(time.perf_counter() - t0)
            n = i + 1
            if n in (100, 200, 300):
                local = snapshots.list_snapshots(root / 'snapshots')
                archived = snapshots.list_snapshots(archive)
                gets = []
                for _ in range(5):
                    t0 = time.perf_counter()
                    store.get('growth', SCOPE)
                    gets.append(time.perf_counter() - t0)
                checkpoints[n] = {
                    'db_bytes': (root / 'memory.sqlite3').stat().st_size,
                    'journal_bytes': (root / 'journal' / 'growth.events.jsonl').stat().st_size,
                    'snapshots_local': len(local), 'snapshots_archived': len(archived),
                    'snapshots_local_bytes': sum(p.stat().st_size for p in local),
                    'snapshots_archived_bytes': sum(p.stat().st_size for p in archived),
                    'transition_seconds_median_last100': statistics.median(seconds[n - 100:n]),
                    'transition_seconds_p90_last100': sorted(seconds[n - 100:n])[89],
                    'get_seconds_median': statistics.median(gets),
                }
        cls.metrics = {'N': cls.N, 'changes_json_bytes_mean': statistics.mean(changes_bytes),
                       'changes_json_bytes_total': sum(changes_bytes), 'checkpoints': checkpoints,
                       'transition_seconds_median_all': statistics.median(seconds),
                       'transition_seconds_max': max(seconds), 'seconds_total': sum(seconds)}
        cls.store, cls.root, cls.archive = store, root, archive

    @classmethod
    def tearDownClass(cls):
        EVID.mkdir(parents=True, exist_ok=True)
        (EVID / 'crescimento_n300.json').write_text(json.dumps(cls.metrics, indent=1, sort_keys=True), encoding='utf-8')
        cls.temp.cleanup()

    @staticmethod
    def exponent(c, key):
        return math.log(c[300][key] / c[100][key]) / math.log(3)

    def test_growth_n300_bytes_db_journal_snapshots(self):
        c = self.metrics['checkpoints']
        m = self.metrics
        increment_ratio = (c[300]['db_bytes'] - c[200]['db_bytes']) / (c[200]['db_bytes'] - c[100]['db_bytes'])
        m['db_increment_ratio_300_200_over_200_100'] = increment_ratio
        m['exponent_db_bytes_100_to_300'] = self.exponent(c, 'db_bytes')
        m['exponent_journal_bytes_100_to_300'] = self.exponent(c, 'journal_bytes')
        total_snap = {n: c[n]['snapshots_local_bytes'] + c[n]['snapshots_archived_bytes'] for n in c}
        m['exponent_snapshot_total_bytes_100_to_300'] = math.log(total_snap[300] / total_snap[100]) / math.log(3)
        m['v1_audit_exponents'] = {'db_bytes': 1.87, 'backups_bytes': 2.78, 'time': 1.36,
                                   'v1_db_bytes_at_n150': 15_000_000, 'v1_backups_bytes_at_n150': 756_000_000,
                                   'v1_transition_seconds_at_n150': 0.41}
        m['v1_db_bytes_extrapolated_n300'] = 15_000_000 * (300 / 150) ** 1.87
        m['v1_backups_bytes_extrapolated_n300'] = 756_000_000 * (300 / 150) ** 2.78
        expected_journal = m['changes_json_bytes_total'] + 600 * (self.N + 1)
        m['journal_expected_bytes_spec'] = expected_journal
        m['journal_deviation_from_spec'] = c[300]['journal_bytes'] / expected_journal - 1
        self.assertGreaterEqual(increment_ratio, 0.7)
        self.assertLessEqual(increment_ratio, 1.5)
        self.assertLess(c[300]['db_bytes'], 6_000_000)
        self.assertLess(m['exponent_db_bytes_100_to_300'], 1.3)
        self.assertLess(m['exponent_journal_bytes_100_to_300'], 1.1)
        self.assertLessEqual(abs(m['journal_deviation_from_spec']), 0.2)
        self.assertEqual((c[300]['snapshots_local'], c[300]['snapshots_archived']), (3, 3))
        for path in snapshots.list_snapshots(self.root / 'snapshots') + snapshots.list_snapshots(self.archive):
            self.assertEqual(Path(str(path) + '.sha256').read_text('ascii').split()[0], sha256_file(path))
        self.assertEqual(list(self.root.glob('memory.sqlite3.bak_*')), [])
        verification = self.store.verify('growth', SCOPE)
        self.assertTrue(verification['ok'] and verification['journal_ok'])
        self.assertEqual((verification['delta_events'], verification['replay_from_revision']), (300, 256))
        self.assertTrue(self.store.verify('growth', SCOPE, deep=True)['ok'])

    def test_transition_time_bounded_n300(self):
        c = self.metrics['checkpoints']
        self.assertLess(self.metrics['transition_seconds_median_all'], 0.050)
        self.assertLess(c[300]['transition_seconds_median_last100'], 0.050)
        self.assertLess(c[300]['get_seconds_median'], 0.050)


if __name__ == '__main__':
    unittest.main(verbosity=2)
