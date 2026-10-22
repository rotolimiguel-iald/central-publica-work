"""Independent tests: copied candidate, snapshot fixture, no production store writes."""
import ast
import copy
import hashlib
import importlib.util
import json
import pathlib
import sys
import time
import unittest

BASE = pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, r'C:\IALD\MEMORIA_IALD\lib')
from iald_memory import store


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = module('iald_memory.review_e2_candidate', BASE / 'mission_candidate.py')
baseline = json.loads((BASE / 'SOURCE_BASELINE.json').read_text(encoding='utf-8'))
O = module('iald_memory.review_e2_original', pathlib.Path(baseline['installed']['path']))
live = json.loads((BASE / 'memory-e2-reviewer-running_GET.json').read_text(encoding='utf-8'))['result']['result']
metrics = {}


class ReadOnlyFixture:
    def __init__(self, value):
        self.value = copy.deepcopy(value)

    def get(self, *args):
        return copy.deepcopy(self.value)

    def transition(self, *args, **kwargs):
        raise AssertionError('No store mutation allowed in independent review')


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.snap = copy.deepcopy(live)
        self.fixture = ReadOnlyFixture(self.snap)
        self.ctl = C.MissionController(self.fixture, self.snap['context_id'], self.snap['scope'])
        _, self.state, self.previous = self.ctl.load()

    def project(self, handles, state=None):
        snap = copy.deepcopy(self.snap)
        snap['p']['handles'] = copy.deepcopy(handles)
        return self.ctl._project(snap, state or self.state, self.previous, 2000000)

    def test_live_shrinks_without_losing_required_content(self):
        old = O.MissionController(self.fixture, self.snap['context_id'], self.snap['scope']).project(2000000)
        new = self.ctl.project(2000000)
        changed = {'flow', 'terminal_handles', 'terminal_handles_recovery', 'unresolved_handles'}
        self.assertEqual({k: v for k, v in old['projection'].items() if k not in changed},
                         {k: v for k, v in new['projection'].items() if k not in changed})
        self.assertEqual(sorted(old['projection']['unresolved_handles'], key=lambda h: h['id']),
                         new['projection']['flow']['handles'])
        self.assertLess(new['actual_chars'], old['actual_chars'])
        self.assertEqual(len(new['projection']['terminal_handles']) + len(new['projection']['flow']['handles']),
                         len(self.snap['p']['handles']))
        metrics.update(snapshot_revision=self.snap['revision'], before_chars=old['actual_chars'],
                       after_chars=new['actual_chars'], terminal_count=len(new['projection']['terminal_handles']),
                       unresolved_count=len(new['projection']['flow']['handles']))

    def test_state_classification_matrix(self):
        terminals = ['completed', 'returned', 'failed', 'cancelled', 'closed', 'accepted', 'consumed', 'done', 'terminated']
        unknown = [{}, {'status': 'running'}, {'phase': 'unknown'}, {'status': None},
                   {'status': 0}, {'status': 'completed', 'phase': 'running'},
                   {'phase': 'done', 'status': {}}, {'status': 'DONE'}]
        for i, data in enumerate([{'status': x} for x in terminals] + [{'phase': x} for x in terminals] + unknown):
            h = {'id': 'case-' + str(i), 'detail': {'payload': 'preserve'}, **data}
            p = self.project([h])['projection']
            if i < 18:
                self.assertEqual(p['flow']['handles'], [])
                self.assertEqual(p['terminal_handles'][0]['id'], h['id'])
            else:
                self.assertEqual(p['flow']['handles'], [h])
                self.assertEqual(p['terminal_handles'], [])
        both = self.project([{'id': 'terminal-pair', 'phase': 'completed', 'status': 'failed'}])['projection']
        self.assertEqual(len(both['terminal_handles']), 1)
        metrics['classification_cases'] = 27
        metrics['both_known_terminal_labels'] = 'indexed, matching installed classifier; no success inference'

    def test_projection_idempotent_and_detached_flow(self):
        before = copy.deepcopy(self.fixture.value)
        a, b = self.ctl.project(2000000), self.ctl.project(2000000)
        self.assertEqual(a, b)
        a['projection']['flow']['handles'].append({'id': 'output-only'})
        self.assertEqual(self.fixture.value, before)
        self.assertEqual(self.ctl.project(2000000), b)

    def test_current_get_contains_all_handles(self):
        p = self.ctl.project(2000000)['projection']
        recovered = self.fixture.get()
        self.assertEqual(recovered['p']['handles'], self.snap['p']['handles'])
        self.assertEqual(p['terminal_handles_recovery']['revision'], recovered['revision'])
        self.assertEqual(p['terminal_handles_recovery']['state_sha256'], recovered['receipt']['state_sha256'])
        self.assertIn('current state', p['terminal_handles_recovery']['instruction'])

    def test_old_projection_hash_refused(self):
        old = O.MissionController(self.fixture, self.snap['context_id'], self.snap['scope']).project(2000000)
        request = {'expected_revision': self.snap['revision'], 'projection_sha256': old['projection_sha256']}
        with self.assertRaisesRegex(C.MissionError, 'stale_projection_refresh_required'):
            self.ctl._current(request, self.snap, self.state, self.previous)
        new = self.ctl.project(2000000)
        self.ctl._current({'expected_revision': self.snap['revision'], 'projection_sha256': new['projection_sha256']},
                          self.snap, self.state, self.previous)

    def test_budget_refuses_without_truncating(self):
        p = self.ctl.project(2000000)
        with self.assertRaisesRegex(C.MissionError, 'projection_overflow_required_'):
            self.ctl.project(p['actual_chars'] - 1)
        self.assertEqual(self.ctl.project(p['actual_chars']), p)

    def test_partial_flow_merge_preserves_hidden_handles(self):
        initial = {'q': {'records': []}, 'p': {'phase': 'old', 'next_action': 'old', 'handles': [
            {'id': 'terminal', 'status': 'completed', 'payload': 'kept'},
            {'id': 'pending', 'status': 'running', 'payload': 'kept'}]}}
        changed = store._apply(initial, {'records': [], 'flow': {'handles': [{'id': 'pending', 'status': 'returned'}]}})
        self.assertEqual(changed['p']['handles'][0], initial['p']['handles'][0])
        self.assertEqual(changed['p']['handles'][1]['payload'], 'kept')
        phase_only = store._apply(changed, {'records': [], 'flow': {'phase': 'new'}})
        self.assertEqual(phase_only['p']['handles'], changed['p']['handles'])
        self.assertEqual(initial['p']['handles'][1]['status'], 'running')

    def test_no_other_ast_change_and_docs_prefix_exact(self):
        trees = [ast.parse(pathlib.Path(v['path']).read_text(encoding='utf-8')) for v in (baseline['installed'], baseline['candidate'])]
        for tree in trees:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == '_project':
                    node.body = []
        self.assertEqual(ast.dump(trees[0], include_attributes=False), ast.dump(trees[1], include_attributes=False))
        for row in json.loads((BASE / 'DOC_PLAN_E2.json').read_text(encoding='utf-8'))['files']:
            original = pathlib.Path(row['before']['path']).read_bytes()
            candidate = pathlib.Path(row['candidate']['path']).read_bytes()
            self.assertEqual(hashlib.sha256(original).hexdigest(), row['before']['sha256'])
            self.assertEqual(hashlib.sha256(candidate).hexdigest(), row['candidate']['sha256'])
            self.assertTrue(candidate.startswith(original))

    def test_poll_unchanged_no_store_write(self):
        result = self.ctl.poll(self.snap['revision'], 0, 2000000)
        self.assertFalse(result['changed'])
        self.assertEqual(result['receipt']['revision'], self.snap['revision'])


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ReviewTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    metrics.update(tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                   success=result.wasSuccessful(), production_writes=0, provider_calls=0,
                   candidate_sha256=hashlib.sha256((BASE / 'mission_candidate.py').read_bytes()).hexdigest())
    raw = (json.dumps(metrics, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    output = BASE / 'INDEPENDENT_TEST_RESULTS_E2.json'
    with output.open('xb') as stream:
        stream.write(raw)
    assert output.read_bytes() == raw
    print(json.dumps(metrics, ensure_ascii=False))
    raise SystemExit(0 if result.wasSuccessful() else 1)
