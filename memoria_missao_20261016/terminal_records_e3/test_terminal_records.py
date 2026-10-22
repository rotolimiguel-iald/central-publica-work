"""E3: real isolated ACOM/CLI; no live mission transitions or provider calls."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import os
import sys
import unittest
from unittest.mock import patch

import test_e2_regression as fixture
from iald_memory.mission import MissionController, MissionError, digest, encoded

ROOT, RUN = fixture.ROOT, fixture.RUN
SCOPE, OWNER, REVIEWER = fixture.SCOPE, fixture.OWNER, fixture.REVIEWER
MEASUREMENTS = {}
spec = importlib.util.spec_from_file_location('iald_memory.e2_baseline',
    fixture.CORE / 'lib' / 'iald_memory' / 'mission.py')
e2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e2)


class TerminalRecordTests(unittest.TestCase):
    setUp = fixture.TerminalProjectionTests.setUp
    transition = fixture.TerminalProjectionTests.transition
    request = fixture.TerminalProjectionTests.request
    cli = fixture.TerminalProjectionTests.cli

    def build(self, number=1, status='completed'):
        stamp = f'20261016T120000_{number:06d}Z'
        directory = self.root / 'attempts' / stamp
        directory.mkdir(parents=True, exist_ok=True)
        pins = {}
        for label, name in [('running', 'START_RECEIPT.json'), (status, 'RECEIPT.json')]:
            file = directory / name
            file.write_bytes(json.dumps({'attempt': stamp, 'status': label, 'pid': 12345,
                'exit_code': None if label == 'running' else (0 if label == 'completed' else 1)}).encode())
            pins[label] = {'path': str(file), 'sha256': hashlib.sha256(file.read_bytes()).hexdigest()}
        handle = {'id': 'build-' + stamp, 'kind': 'lean_build', 'task_id': 'A',
                  'no_repeat': True, 'status': status, 'start_receipt': pins['running'],
                  'receipt': pins[status], 'detail': 'Complete details remain in get.'}
        records = [{'id': f'track-build-{stamp}-{label}', 'kind': 'fact', 'statute': 'REAL',
                    'text': f'A sandbox build {stamp} {label}. Full requirement remains open.',
                    'sources': [{'kind': 'artifact', 'ref': pins[label]['path'],
                                 'sha256': pins[label]['sha256']}]} for label in ['running', status]]
        return handle, records

    def populated(self):
        handle, records = self.build()
        self.transition({'records': records, 'flow': {'handles': [handle]}})
        return handle, records, self.ctl.load()

    def state_bytes(self):
        return {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in (self.root / 'state').rglob('*') if p.is_file()}

    def test_capacity_get_digest_determinism_and_no_persistent_mutation(self):
        handles, records = [], []
        for i in range(100):
            h, r = self.build(i)
            handles.append(h)
            records.extend(r)
        pending = {'id': 'uncertain-execution', 'phase': 'dispatch_uncertain',
                   'no_repeat': True, 'detail': 'Do not repeat.'}
        self.transition({'records': records, 'flow': {'handles': handles + [pending]}})
        before = self.store.get(self.cid, SCOPE)
        before_bytes = self.state_bytes()
        old = e2.MissionController(self.store, self.cid, SCOPE).project(2000000)
        new = self.ctl.project(100000)
        self.assertGreater(old['actual_chars'], 100000)
        body = new['projection']
        self.assertEqual(len(body['terminal_build_records']), 200)
        self.assertEqual(body['current_records'], [])
        self.assertEqual(body['unresolved_handles'], [pending])
        self.assertFalse(body['tetelestai'])
        self.assertEqual(self.ctl.project(100000), new)
        self.assertEqual(self.cli('project', max_chars=100000), new)
        full = self.cli('get')
        self.assertEqual(full, before)
        rec = body['terminal_build_records_recovery']
        self.assertEqual(rec['field'], 'q.records')
        self.assertEqual(rec['revision'], full['revision'])
        self.assertEqual(rec['state_sha256'], full['receipt']['state_sha256'])
        self.assertIn('current state', rec['instruction'])
        self.assertIn('journal replay', rec['instruction'])
        originals = {r['id']: r for r in full['q']['records']}
        for row in body['terminal_build_records']:
            self.assertEqual(row['record_sha256'], digest(originals[row['id']]))
        self.assertEqual(self.state_bytes(), before_bytes)
        self.assertEqual(self.store.get(self.cid, SCOPE), before)
        self.assertTrue(self.store.verify(self.cid, SCOPE, deep=True)['ok'])
        self.assertEqual(self.ctl.project(new['actual_chars']), new)
        with self.assertRaisesRegex(MissionError, 'projection_overflow'):
            self.ctl.project(new['actual_chars'] - 1)
        MEASUREMENTS['capacity'] = {'records': 200, 'terminal_builds': 100,
            'pending': 1, 'e2_chars': old['actual_chars'], 'e3_chars': new['actual_chars'],
            'full_get_identical': True, 'all_persistent_files_byte_identical': True}

    def test_negative_record_schemas_stay_complete(self):
        h, records, (snap, state, previous) = self.populated()
        cases = {
            'extra_text': lambda r: r.update(text=r['text'] + ' Extra order.'),
            'whitespace': lambda r: r.update(text=r['text'] + '\n'),
            'decision': lambda r: r.update(kind='decision'),
            'candidate': lambda r: r.update(kind='candidate', statute='DECLARADO'),
            'declared_fact': lambda r: r.update(statute='DECLARADO'),
            'extra_field': lambda r: r.update(meta={'order': 'preserve'}),
            'erratum': lambda r: r.update(kind='erratum', supersedes=records[0]['id']),
            'id_partial': lambda r: r.update(id=r['id'] + '-extra'),
            'id_prefix': lambda r: r.update(id='x' + r['id']),
            'timestamp_invalid': lambda r: r.update(id=r['id'].replace('20261016', '20261399')),
            'missing_sources': lambda r: r.pop('sources'),
            'extra_source': lambda r: r['sources'].append(copy.deepcopy(r['sources'][0])),
            'source_field': lambda r: r['sources'][0].update(extra='keep'),
            'source_kind': lambda r: r['sources'][0].update(kind='external'),
            'source_hash': lambda r: r['sources'][0].update(sha256='0' * 64),
            'source_path': lambda r: r['sources'][0].update(ref=r['sources'][0]['ref'] + '.other'),
            'task_text': lambda r: r.update(text=r['text'].replace('A sandbox', 'B sandbox')),
        }
        for name, change in cases.items():
            with self.subTest(name=name):
                s = copy.deepcopy(snap)
                record = s['q']['records'][-1]
                change(record)
                body = self.ctl._project(s, state, previous, 100000)['projection']
                self.assertIn(record, body['current_records'])
                self.assertNotIn(record['id'], [x['id'] for x in body['terminal_build_records']])
        MEASUREMENTS['negative_record_cases'] = len(cases)

    def test_negative_handles_and_pins_stay_complete(self):
        h, records, (snap, state, previous) = self.populated()
        cases = {
            'kind': lambda h: h.update(kind='other'),
            'no_repeat_false': lambda h: h.update(no_repeat=False),
            'no_repeat_integer': lambda h: h.update(no_repeat=1),
            'task_missing': lambda h: h.pop('task_id'),
            'task_unknown': lambda h: h.update(task_id='unknown'),
            'active': lambda h: h.update(status='running'),
            'unknown': lambda h: h.update(status='new_terminal_word'),
            'nonstring_status': lambda h: h.update(status=[]),
            'conflicting_active': lambda h: h.update(phase='uncertain'),
            'conflicting_terminal': lambda h: h.update(phase='failed'),
            'nonstring_phase': lambda h: h.update(phase=None),
            'status_missing': lambda h: h.pop('status'),
            'receipt_absent': lambda h: h.pop('receipt'),
            'receipt_no_pin': lambda h: h.update(receipt=h['receipt']['path']),
            'receipt_extra': lambda h: h['receipt'].update(extra='keep'),
            'receipt_hash': lambda h: h['receipt'].update(sha256='0' * 64),
            'different_terminal': lambda h: h.update(status='failed'),
        }
        for name, change in cases.items():
            with self.subTest(name=name):
                s = copy.deepcopy(snap)
                change(s['p']['handles'][0])
                body = self.ctl._project(s, state, previous, 100000)['projection']
                self.assertIn(records[-1], body['current_records'])
        s = copy.deepcopy(snap)
        s['p']['handles'] = []
        body = self.ctl._project(s, state, previous, 100000)['projection']
        self.assertEqual(body['current_records'], records)
        MEASUREMENTS['negative_handle_cases'] = len(cases) + 1

    def test_receipt_missing_mutated_or_guard_failure_keeps_record(self):
        h, records, (snap, state, previous) = self.populated()
        file = Path(h['receipt']['path'])
        original = file.read_bytes()
        file.write_bytes(original + b' changed')
        self.assertIn(records[-1], self.ctl.project()['projection']['current_records'])
        file.unlink()
        self.assertIn(records[-1], self.ctl.project()['projection']['current_records'])
        file.write_bytes(original)
        with patch('iald_memory.mission.guard.read_checked', side_effect=OSError('unreadable')):
            self.assertEqual(self.ctl.project()['projection']['current_records'], records)

    def test_ambiguous_terminal_receipts_and_start_without_terminal_remain_visible(self):
        h, records, (snap, state, previous) = self.populated()
        file = Path(h['receipt']['path'])
        for raw in [b'not json', b'[]', b'{"exit_code":1}', b'{"exit_code":false}',
                    b'{"exit_code":null}', b'{}', b'{"exit_code":0,"exit_code":1}',
                    b'{"exit_code":0,"detail":NaN}', b'[' * 2000 + b']' * 2000]:
            with self.subTest(raw=raw):
                file.write_bytes(raw)
                s = copy.deepcopy(snap)
                sha = hashlib.sha256(raw).hexdigest()
                s['p']['handles'][0]['receipt']['sha256'] = sha
                s['q']['records'][-1]['sources'][0]['sha256'] = sha
                body = self.ctl._project(s, state, previous, 100000)['projection']
                self.assertEqual(body['current_records'], s['q']['records'][1:])
                self.assertEqual(body['terminal_build_records'], [])
        s = copy.deepcopy(snap)
        s['p']['handles'][0].pop('receipt')
        body = self.ctl._project(s, state, previous, 100000)['projection']
        self.assertEqual(body['current_records'], records)

    def test_duplicates_preserve_every_record(self):
        h, records, (snap, state, previous) = self.populated()
        s = copy.deepcopy(snap)
        s['q']['records'].append(copy.deepcopy(records[-1]))
        body = self.ctl._project(s, state, previous, 100000)['projection']
        self.assertEqual(body['current_records'].count(records[-1]), 2)
        self.assertNotIn(records[-1]['id'], [x['id'] for x in body['terminal_build_records']])
        s = copy.deepcopy(snap)
        s['p']['handles'].append(copy.deepcopy(h))
        body = self.ctl._project(s, state, previous, 100000)['projection']
        self.assertEqual(body['current_records'], records)
        self.assertEqual(body['terminal_build_records'], [])

    def test_pinned_bytes_change_projection_hash_without_revision_change(self):
        h, records, _ = self.populated()
        before = self.ctl.project()
        request = self.request('claim')
        file = Path(h['receipt']['path'])
        original = file.read_bytes()
        file.write_bytes(original + b' mutation')
        after = self.ctl.project()
        self.assertEqual(before['receipt'], after['receipt'])
        self.assertNotEqual(before['projection_sha256'], after['projection_sha256'])
        with self.assertRaisesRegex(MissionError, 'stale_projection'):
            self.ctl.action(request)
        file.write_bytes(original)
        self.assertEqual(self.ctl.project(), before)

    def test_preflight_handoff_bridge_and_stale_e2_hash(self):
        h, records, _ = self.populated()
        wrong = self.request('claim')
        wrong['projection_sha256'] = e2.MissionController(self.store, self.cid, SCOPE).project()['projection_sha256']
        with self.assertRaisesRegex(MissionError, 'stale_projection'):
            self.ctl.action(wrong)
        lease = self.ctl.action(self.request('claim'))['task']['lease']['id']
        p = self.ctl.project()
        req = self.request('handoff', lease_id=lease, max_chars=p['actual_chars'])
        self.assertTrue(self.ctl.check(req)['ready'])
        self.assertEqual(self.ctl.handoff(req)['projection'], p['projection'])
        with self.assertRaisesRegex(MissionError, 'projection_overflow'):
            self.ctl.handoff({**req, 'max_chars': p['actual_chars'] - 1})
        bridge_path = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\iald_orchestrator\mission_bridge.py')
        spec = importlib.util.spec_from_file_location('e3_bridge', bridge_path)
        bridge = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bridge)
        class Server:
            def __init__(self): self.tools = {}
            def tool(self):
                def register(f): self.tools[f.__name__] = f; return f
                return register
        server = Server()
        bridge.register_tools(server)
        self.assertEqual(len(server.tools), 4)
        def local_cli(request):
            r = dict(request)
            operation = r.pop('operation')
            r.pop('reference')
            return self.cli(operation, **r)
        with patch.object(bridge, 'invoke', side_effect=local_cli):
            sync = server.tools['iald_mission_sync'](str(self.ref), max_chars=100000)
            self.assertEqual(sync, self.ctl.project(100000))
            args = dict(reference=str(self.ref), task_id='A', actor_id=OWNER['id'],
                lease_id=lease, expected_revision=sync['receipt']['revision'],
                projection_sha256=sync['projection_sha256'])
            self.assertTrue(server.tools['iald_mission_preflight'](**args)['ready'])
            self.assertEqual(server.tools['iald_mission_handoff'](**args, max_chars=100000)['projection'], sync['projection'])
        MEASUREMENTS['bridge'] = {'tools': 4, 'real_isolated_cli': True,
            'mcp_stdio': False, 'bridge_sha256': hashlib.sha256(bridge_path.read_bytes()).hexdigest()}

    def test_scientific_records_and_overflow_remain_visible(self):
        h, records, _ = self.populated()
        order = {'id': 'order', 'kind': 'decision', 'statute': 'INPUT',
                 'text': 'Mandatory order. ' + 'x' * 50000,
                 'sources': [{'kind': 'artifact', 'ref': 'isolated-order'}]}
        self.transition({'records': [order]})
        with self.assertRaisesRegex(MissionError, 'projection_overflow'):
            self.ctl.project(24000)
        self.assertIn(order, self.ctl.project(100000)['projection']['current_records'])

    def test_projection_copy_does_not_alias_and_all_terminal_outcomes(self):
        h, records, (snap, state, previous) = self.populated()
        saved = copy.deepcopy(snap)
        body = self.ctl._project(snap, state, previous, 100000)['projection']
        body['terminal_build_records'][0]['record_status'] = 'tampered'
        self.assertEqual(snap, saved)
        for n, status in [(2, 'failed'), (3, 'terminated')]:
            h, rs = self.build(n, status)
            self.transition({'records': rs, 'flow': {'handles': [h]}})
        body = self.ctl.project()['projection']
        self.assertEqual(len(body['terminal_build_records']), 6)
        self.assertEqual(body['current_records'], [])
        self.assertFalse(body['tetelestai'])


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TerminalRecordTests))
    report = {'ok': result.wasSuccessful(), 'tests_run': result.testsRun,
        'failures': [{'test': str(t), 'detail': detail} for t, detail in result.failures + result.errors],
        'run_directory': str(RUN), 'measurements': MEASUREMENTS,
        'candidate_sha256': hashlib.sha256((ROOT / 'mission_candidate_r2.py').read_bytes()).hexdigest(),
        'test_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': 'Real isolated ACOM and CLI; bridge registration exercised with inert server, not MCP stdio; no live transitions/providers/Lean.'}
    target = ROOT / ('TEST_RESULT_E3_' + RUN.name + '.json')
    raw = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode()
    temporary = target.with_suffix('.tmp')
    with temporary.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temporary.read_bytes() == raw
    os.rename(temporary, target)
    print(json.dumps({'report': str(target), 'ok': report['ok'], 'tests_run': result.testsRun,
                      'measurements': MEASUREMENTS}))
    sys.exit(0 if result.wasSuccessful() else 1)
