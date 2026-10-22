"""Execute extracted real native server functions with actual staged App Binding.

No server import/start, user database, canonical science load or HTTP generation.
Only external scientific readers and the read/count HTTP endpoints are simulated.
"""
from test_native_activity import WORK, MemoryStore, native, history
from pathlib import Path
from copy import deepcopy
import ast, importlib.util, json, sys, tempfile, types, unittest
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor

APP = WORK/'staging/app'
sys.path.insert(0, str(APP))


class RealHooksTests(unittest.TestCase):
    def setUp(self):
        runs = WORK/'tests_native/runs'
        runs.mkdir(parents=True, exist_ok=True)
        self.root = Path(tempfile.mkdtemp(prefix='h_', dir=runs))
        spec = importlib.util.spec_from_file_location('native_test_app_memory', APP/'iald_app_memory.py')
        self.app = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = self.app
        spec.loader.exec_module(self.app)
        self.app._SHARED_ROOT = self.root/'s'
        self.app.MemoryStore = lambda root: MemoryStore(root, snapshot_archive_dir=self.root/'a')
        self.binding = self.app.begin(self.root, 'synthetic-account-generation', 'conversation',
                                     [{'role':'user','content':'Preserve current objective and constraints.'}], request_id='native-hooks')
        self.source = (APP/'iald_web_server.py').read_text(encoding='utf-8')
        tree = ast.parse(self.source)
        wanted = {'_prepare_native_payload', '_operational_native_payload'}
        nodes = [n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted]
        self.assertEqual({n.name for n in nodes}, wanted)
        self.release = types.SimpleNamespace(identity={'release':'synthetic-public'}, check_manifest=lambda:None)
        self.env = {'native_memory':native, 'app_memory':self.app,
            'MEMORIA_EXTERNA':types.SimpleNamespace(nucleus_manifest={'test':True}),
            'KERNEL_EXTERNO':types.SimpleNamespace(source_sha='synthetic-source'),
            'ACTIVE_MODEL_ID':'native-test', 'LLAMA_URL':'http://127.0.0.1:8081',
            'MODELS':{'native-test':{'cmd':['test-model','-c','65536']}},
            '_ferramentas_para':lambda surface:[{'type':'function','function':{'name':'test_tool','parameters':{}}}],
            'iald_kernel':types.SimpleNamespace(tool_definitions=lambda:[]),
            'iald_core_indexado':types.SimpleNamespace(tool_definitions=lambda:[])}
        exec(compile(ast.Module(body=nodes,type_ignores=[]),str(APP/'iald_web_server.py'),'exec'),self.env)
        self.observed = []
        def count(url, endpoint, data=None):
            if endpoint == '/props':return {'default_generation_settings':{'n_ctx':65536}}
            if endpoint == '/apply-template':
                self.observed.append(deepcopy(data))
                return {'prompt':json.dumps(data)}
            return {'tokens':[1]*(len(data['content'])//4)}
        self.patches = [patch.object(native,'load_native_context',return_value=('PUBLIC_CANONICAL_PREFIX',self.release.identity)),
                        patch.object(native,'load_release',return_value=self.release),
                        patch.object(native,'_local_json',side_effect=count)]
        for p in self.patches:p.start()
        self.addCleanup(lambda:[p.stop() for p in reversed(self.patches)])

    def test_real_auto_and_legacy_preparation_projection_and_actual_tools_count(self):
        with self.app.bound(self.binding):
            for path in ('automatic','legacy'):
                payload, definitions, check = self.env['_prepare_native_payload'](
                    {'messages':history(),'max_tokens':512},'app',native_path=path)
                self.assertIn('PUBLIC_CANONICAL_PREFIX',payload['messages'][0]['content'])
                self.assertIn('<IALD_ACTIVITY_V1>',payload['messages'][0]['content'])
                payload['tools'] = definitions
                check(payload)
                self.assertEqual(self.observed[-1]['tools'],definitions)
                self.assertEqual(self.observed[-1]['messages'],payload['messages'])

    def test_real_worker_thread_binding_propagates_only_own_context(self):
        def call():
            self.assertEqual(self.app.current().context_id,self.binding.context_id)
            return self.env['_operational_native_payload']({'messages':history(),'max_tokens':512})
        with self.app.bound(self.binding):
            run = self.app.thread_target(call)
        self.assertIsNone(self.app.current())
        with ThreadPoolExecutor(1) as pool:payload = pool.submit(run).result()
        self.assertIn(self.binding.context_id,payload['messages'][0]['content'])
        self.assertEqual(self.observed[-1]['messages'],payload['messages'])

    def test_server_hooks_reach_auto_legacy_and_remove_global_compressor(self):
        tree = ast.parse(self.source)
        calls = [n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)
                 and n.func.id == '_prepare_native_payload']
        self.assertTrue(any(any(k.arg=='native_path' and isinstance(k.value,ast.Constant)
                        and k.value.value=='automatic' for k in n.keywords) for n in calls))
        self.assertTrue(any(not n.keywords for n in calls))
        self.assertFalse(any(isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name)
                             and n.value.id=='HOLO_MEMORY' and n.attr=='compress_context' for n in ast.walk(tree)))

    def test_real_binding_checkpoint_recovery_and_read_only_restart(self):
        with self.app.bound(self.binding):
            first, receipt = native.prepare_activity_payload({'messages':history(),'max_tokens':512},
                binding=self.binding,project_messages=self.app.project_messages,window=8192,path='legacy')
            self.assertEqual(receipt['status'],'CHECKPOINTED_CANDIDATE')
            before = self.binding.snapshot()
            second, replay = native.prepare_activity_payload({'messages':history(),'max_tokens':512},
                binding=self.binding,project_messages=self.app.project_messages,window=8192,path='legacy')
            self.assertEqual(replay['status'],'REPLAYED_CHECKPOINT')
            self.assertEqual(before,self.binding.snapshot())
            self.assertEqual(first,second)


if __name__ == '__main__':unittest.main(verbosity=2)
