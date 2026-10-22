"""Private-store integration tests; science readers and HTTP counters simulated."""
from pathlib import Path
from copy import deepcopy
import ast
import hashlib
import importlib.util
import json
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
import subprocess

WORK = Path(__file__).resolve().parents[1]
NATIVE = WORK/'staging/native'
sys.path[:0] = [str(NATIVE), str(WORK/'staging/core/lib')]
for name, attrs in {
    'iald_core_indexado': {'DocumentCorpus': object},
    'iald_estado_publicado': {'published_evidence': None},
    'iald_release_binding': {'load_release': None},
    'iald_response_contract': {'deployment_contract': None, 'IDENTITY_PROTOCOL': '', 'SOLUTION_PROTOCOL': ''},
}.items():
    module = types.ModuleType(name)
    module.__dict__.update(attrs)
    sys.modules[name] = module
import iald_native_memory as native
import iald_native_activity as bridge
from holographic_memory import HolographicMemory
from iald_memory import MemoryStore
from iald_memory.activity import ActivityRuntime, ActivityError


class TestBinding:
    """Exact checkpoint shape agreed with A; authentication itself is out of scope."""
    def __init__(self, store, context='native-a', principal='account-generation-a', request='r1', ticket=None):
        self.store, self.context_id, self.request_id = store, context, request
        self.scope = {'house': 'IALD_APP', 'principal': principal}
        self.actor = {'kind': 'agent', 'id': 'synthetic-native-server'}
        self.store.ensure_context(context, objective='Preserve the original named objective.', scope=self.scope,
                                  actor={'kind': 'operator', 'id': 'synthetic-human'})
        self.activity = ActivityRuntime(store, context, self.scope, self.actor)
        self.ticket = ticket or self.activity.begin(request, 'Continue this same conversation.',
                                                   origin='authenticated_operator')['ticket']

    def snapshot(self):
        return self.store.get(self.context_id, self.scope)

    def checkpoint(self, label, value):
        text = bridge.canonical(value)
        event = 'app.' + hashlib.sha256((self.request_id+':checkpoint.'+label+':'+text).encode()).hexdigest()
        return self.store.transition(self.context_id, self.scope, self.snapshot()['revision'], event,
            {'kind': 'system', 'id': 'synthetic-native-server'}, {'records': [dict(id=event,
            kind='candidate', statute='DECLARADO', text=text,
            sources=[{'kind': 'tool', 'ref': 'app:'+self.request_id+':checkpoint.'+label}])]})

    def project_messages(self, messages):
        # Same boundary as app_memory.project_messages; actual formatter is tested by A.
        p = self.activity.project(200000)
        return deepcopy(messages) + [{'role': 'system', 'content': p['text']}]


def history():
    return [{'role': 'system', 'content': 'Canonical public science and explicit status remain intact.'}] + [
        {'role': 'user' if i % 2 == 0 else 'assistant',
         'content': f'Turn {i}. ' + ('A smooth function preserves an explicitly stated domain. '
             'The prior observation remains provisional. Numerical evidence has a source. ' * 14)}
        for i in range(20)]


class NativeTests(unittest.TestCase):
    def setUp(self):
        runs = WORK/'tests_native/runs'
        runs.mkdir(parents=True, exist_ok=True)
        self.root = Path(tempfile.mkdtemp(prefix='n_', dir=runs))
        self.store = MemoryStore(self.root/'s', snapshot_archive_dir=self.root/'a')
        self.binding = TestBinding(self.store)

    def prepare(self, binding=None, path='legacy', messages=None):
        return bridge.prepare_messages(history() if messages is None else messages,
            binding=binding or self.binding, path=path, window=8192, output_reserve=512)

    def last_checkpoint(self, binding=None):
        b = binding or self.binding
        row = next(r for r in reversed(b.snapshot()['q']['records'])
                   if r['sources'][0].get('ref', '').endswith(':checkpoint.'+bridge.LABEL))
        value = json.loads(row['text'])
        return row, value, json.loads(Path(value['artifact']['path']).read_text(encoding='utf-8'))

    def test_compressor_formulas_and_source_unchanged(self):
        baseline = json.loads((WORK/'NATIVE_BASELINE_R1.json').read_text(encoding='utf-8'))
        expected = next(p['sha256'] for p in baseline['sources'] if p['path'].endswith('holographic_memory.py'))
        self.assertEqual(hashlib.sha256((NATIVE/'holographic_memory.py').read_bytes()).hexdigest(), expected)
        a, b = HolographicMemory(), bridge.ScopedHolographicMemory()
        for engine in (a, b):
            engine._janela_real, engine.RESPONSE_BUDGET = 8192, 512
        self.assertEqual(a.compress_context(history()), b.compress_context(history()))

    def test_native_existing_functions_ast_unchanged(self):
        old = ast.parse(Path(r'C:\IALD\projetos_pyhton\IALD\iald_native_memory.py').read_text(encoding='utf-8'))
        new = ast.parse((NATIVE/'iald_native_memory.py').read_text(encoding='utf-8'))
        functions = {x.name: ast.dump(x) for x in new.body if isinstance(x, (ast.FunctionDef, ast.ClassDef))}
        for node in old.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                self.assertEqual(ast.dump(node), functions[node.name])

    def test_full_hash_distinguishes_same_200_character_prefix(self):
        a, b = 'a'*200+'one', 'a'*200+'two'
        self.assertNotEqual(bridge.ScopedHolographicMemory._content_hash(a), bridge.ScopedHolographicMemory._content_hash(b))

    def test_checkpoint_candidate_full_original_and_provenance(self):
        original = history()
        before = deepcopy(original)
        output, report = self.prepare(messages=original)
        self.assertEqual(original, before)
        self.assertEqual(report['status'], 'CHECKPOINTED_CANDIDATE')
        row, value, payload = self.last_checkpoint()
        self.assertEqual((row['kind'], row['statute']), ('candidate', 'DECLARADO'))
        self.assertEqual(payload['input_messages'], original)
        self.assertEqual(payload['output_messages'], output)
        self.assertTrue(payload['transformed_or_omitted_indices'])
        self.assertEqual(payload['namespace']['scope'], self.binding.scope)
        self.assertEqual(payload['state']['_compress_count'], 1)
        self.assertEqual(output[-6:], original[-6:])
        self.assertEqual(output[0], original[0])

    def test_same_request_input_replay_has_no_delta(self):
        first, _ = self.prepare()
        before = self.binding.snapshot()
        second, report = self.prepare()
        self.assertEqual(first, second)
        self.assertEqual(report['status'], 'REPLAYED_CHECKPOINT')
        self.assertEqual(before, self.binding.snapshot())

    def test_scopes_do_not_share_counter_or_content(self):
        self.prepare()
        other = TestBinding(self.store, context='native-b', principal='account-generation-b')
        messages = history()
        messages[1]['content'] += 'Only account B sees this.'
        _, report = self.prepare(binding=other, messages=messages)
        a = self.last_checkpoint()[2]
        b = self.last_checkpoint(other)[2]
        self.assertEqual(a['state']['_compress_count'], b['state']['_compress_count'])
        self.assertNotIn('Only account B sees this.', json.dumps(self.binding.snapshot()))
        self.assertNotEqual(report['artifact']['path'], self.last_checkpoint()[1]['artifact']['path'])

    def test_other_account_generation_fails(self):
        with self.assertRaises(Exception):
            TestBinding(self.store, context='native-a', principal='new-account-generation')

    def test_structured_media_and_tools_pass_unchanged(self):
        messages = history() + [{'role': 'assistant', 'content': '', 'tool_calls': [{'id': 'x', 'function': {'name': 'read'}}]},
                               {'role': 'tool', 'tool_call_id': 'x', 'content': 'Full reply'},
                               {'role': 'user', 'content': [{'type': 'image_url', 'image_url': {'url': 'synthetic:image'}}]}]
        before = self.binding.snapshot()
        output, report = self.prepare(messages=messages)
        self.assertEqual(output, messages)
        self.assertEqual(report['status'], 'PRESERVED_STRUCTURED_OR_DISABLED')
        self.assertEqual(before, self.binding.snapshot())

    def test_unbound_has_no_global_state_or_loss(self):
        messages = history()
        out, report = bridge.prepare_messages(messages, binding=None, path='unbound', window=8192)
        self.assertEqual(out, messages)
        self.assertEqual(report['status'], 'UNBOUND_NO_COMPRESSION_OR_SHARED_STATE')

    def test_restart_process_recovers_checkpoint_without_event(self):
        output, _ = self.prepare()
        rev = self.binding.snapshot()['revision']
        cfg = self.root/'restart.json'
        cfg.write_text(json.dumps({'ticket': self.binding.ticket}), encoding='utf-8')
        code = """import sys,json
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from test_native_activity import TestBinding,MemoryStore,bridge,history
s=MemoryStore(Path(sys.argv[2])/'s',snapshot_archive_dir=Path(sys.argv[2])/'a')
t=json.loads((Path(sys.argv[2])/'restart.json').read_text())['ticket']
b=TestBinding(s,ticket=t)
out,r=bridge.prepare_messages(history(),binding=b,path='legacy',window=8192,output_reserve=512)
print(json.dumps({'status':r['status'],'sha':bridge.digest(out),'revision':b.snapshot()['revision']}))
"""
        cp = subprocess.run([sys.executable, '-B', '-X', 'utf8', '-c', code, str(WORK/'tests_native'), str(self.root)],
                            capture_output=True, text=True, check=True)
        result = json.loads(cp.stdout)
        self.assertEqual(result, {'status': 'REPLAYED_CHECKPOINT', 'sha': bridge.digest(output), 'revision': rev})

    def test_auto_legacy_worker_same_context_projection_last_and_counted(self):
        observed = []
        def local_counter(url, endpoint, data=None):
            if endpoint == '/props': return {'default_generation_settings': {'n_ctx': 65536}}
            if endpoint == '/apply-template':
                observed.append(deepcopy(data))
                return {'prompt': json.dumps(data)}
            return {'tokens': list(range(len(data['content'])//4))}
        with patch.object(native, '_local_json', side_effect=local_counter):
            for route in ('automatic', 'legacy', 'worker_operational'):
                payload, report = native.prepare_activity_payload({'messages': history(), 'max_tokens':512},
                    binding=self.binding, project_messages=self.binding.project_messages,
                    window=65536, path=route, compress=route != 'worker_operational')
                measurement = native.check_text_window(payload, 65536)
                self.assertIn('<IALD_ACTIVITY_V1>', payload['messages'][-1]['content'])
                self.assertEqual(observed[-1]['messages'], payload['messages'])
                self.assertGreater(measurement['input_tokens'], 0)
                self.assertIn(self.binding.context_id, payload['messages'][-1]['content'])
        self.assertEqual(len(observed), 3)

    def test_counter_failure_and_measured_overflow_are_visible(self):
        payload, _ = native.prepare_activity_payload({'messages': history(), 'max_tokens':512},
            binding=self.binding, project_messages=self.binding.project_messages, window=8192, path='automatic')
        with patch.object(native, '_local_json', side_effect=OSError('counter unavailable')):
            with self.assertRaises(native.NativeCounterUnavailable): native.check_text_window(payload,8192)
        def counter(url, endpoint, data=None):
            if endpoint == '/props': return {'default_generation_settings':{'n_ctx':8192}}
            if endpoint == '/apply-template': return {'prompt':json.dumps(data)}
            return {'tokens':[1]*8100}
        with patch.object(native, '_local_json', side_effect=counter):
            with self.assertRaises(native.NativeContextError): native.check_text_window(payload,8192)

    def test_corrupt_checkpoint_refuses_without_repair(self):
        self.prepare()
        row, value, _ = self.last_checkpoint()
        p = Path(value['artifact']['path'])
        p.write_bytes(b'corrupt isolated fixture')
        with self.assertRaisesRegex(bridge.NativeActivityError,'holographic_checkpoint_hash_mismatch'):
            self.prepare()
        self.assertEqual(p.read_bytes(),b'corrupt isolated fixture')

    def test_changed_steering_preserves_checkpoint_before_refusal(self):
        checkpoint = self.binding.checkpoint
        def concurrent(label, value):
            r = checkpoint(label, value)
            self.binding.activity.begin('r2','New direction from human',origin='authenticated_operator')
            return r
        self.binding.checkpoint = concurrent
        with self.assertRaisesRegex(ActivityError,'steering_changed'): self.prepare()
        self.assertEqual(self.last_checkpoint()[0]['statute'],'DECLARADO')

    def test_scoped_parallel_preparation_has_independent_counters(self):
        other = TestBinding(self.store, context='native-b',principal='account-generation-b')
        with ThreadPoolExecutor(2) as pool:
            list(pool.map(lambda b:self.prepare(binding=b),[self.binding,other]))
        self.assertEqual(self.last_checkpoint()[2]['state']['_compress_count'],1)
        self.assertEqual(self.last_checkpoint(other)[2]['state']['_compress_count'],1)

    def test_generated_hologram_is_derived_assistant_narrative(self):
        messages = history()
        output, _ = bridge.prepare_messages(messages,binding=self.binding,path='legacy',window=4096,output_reserve=512)
        summaries = [m for m in output if m['content'].startswith('[DECLARADO — resumo holográfico')]
        self.assertTrue(summaries)
        self.assertTrue(all(m['role']=='assistant' for m in summaries))
        self.assertEqual([m for m in output if m['role']=='system'],[messages[0]])


if __name__ == '__main__':
    unittest.main(verbosity=2)
