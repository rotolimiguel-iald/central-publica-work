"""Offline adversarial tests; only AST-selected functions from the real server."""
import ast
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import socket
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

STAGE = Path(__file__).resolve().parents[1]
WORK = STAGE.parent
PRODUCTION = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0] = [str(STAGE), str(PRODUCTION)]
import iald_native_memory as native
from iald_release_binding import load_release
from claude_memory_package import load_package
from claude_profiles import HAIKU, context_budget
import iald_kernel
import iald_core_indexado


def digest(value):
    return hashlib.sha256(value).hexdigest()


def server_namespace(*names):
    tree = ast.parse((STAGE / 'iald_web_server.py').read_bytes())
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert len(functions) == len(names)
    for function in functions:
        function.decorator_list = []
    namespace = {'json': json, 'os': os, 'native_memory': native,
                 'iald_kernel': iald_kernel, 'iald_core_indexado': iald_core_indexado}
    exec(compile(ast.Module(body=functions, type_ignores=[]), '<server-functions-only>', 'exec'), namespace)
    return namespace


class Fixture(unittest.TestCase):
    def setUp(self):
        parent = STAGE / 'test_tmp'
        parent.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = self.root / 'canonical.json'
        core = b'Essential formulas and current release [DERIVED].'
        cluster = b'Cluster\n### verified section\nreference'
        (self.root / 'core.md').write_bytes(core)
        (self.root / 'cluster.md').write_bytes(cluster)
        (self.root / 'doc.txt').write_bytes(b'Public source.')
        self.source = 'a' * 64  # Fixture, never a claimed artifact hash.
        self.config = {
            'format': 1, 'document_mode': 'retrievable',
            'operational_core': {'path': str(self.root / 'core.md'), 'sha256': digest(core),
                'version': 'fixture', 'current_release': 'v378', 'release_source_sha256': self.source},
            'active_cluster': {'path': str(self.root / 'cluster.md'), 'sha256': digest(cluster),
                'release': 'v378', 'release_source_sha256': self.source,
                'commit': 'b' * 40, 'core_sections': 1},
            'entries': [{'id': 'source', 'path': str(self.root / 'doc.txt'),
                'public_sha256': digest(b'Public source.'), 'role': 'fixture',
                'url': 'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/' + 'b' * 40 + '/doc.txt'}],
            'published_evidence': {'fixture': True},
        }
        self.save_config()
        self.identity = load_release(self.manifest).identity
        prefix = b'Measured prefix fixture, no provider count performed.'
        (self.root / 'prefix.md').write_bytes(prefix)
        self.package = {'schema': 'iald.claude.memory.v1', 'model': HAIKU.model,
            'prefix_file': 'prefix.md', 'prefix_sha256': digest(prefix), 'tools_sha256': 'c' * 64,
            'deployment': self.identity,
            'budget': context_budget(HAIKU.model, counted_model=HAIKU.model,
                permanent_tokens=183000, request_input_tokens=184500, reserved_output_tokens=4096)}
        self.save_package()
        self.catalog = SimpleNamespace(source_sha=self.source, context=lambda: 'PUBLIC KERNEL CATALOG',
            status=lambda: {'lean_files': 3, 'source_sha256': self.source})
        self.evidence = patch.object(native, 'published_evidence', return_value=('VERY LONG EXTRACT', {
            'published_evidence_checked': True, 'published_source_sha256': self.source}))
        self.evidence.start()
        self.addCleanup(self.evidence.stop)
        self.no_network = patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden'))
        self.no_network.start()
        self.addCleanup(self.no_network.stop)

    def save_config(self):
        self.manifest.write_text(json.dumps(self.config), encoding='utf-8')

    def save_package(self):
        (self.root / 'manifest.json').write_text(json.dumps(self.package), encoding='utf-8')

    def load(self):
        return load_package(self.root, canonical_manifest=self.manifest, source_sha=self.source)


class BindingTests(Fixture):
    def test_valid_bound_package(self):
        self.assertEqual(self.load().tools_sha256, self.package['tools_sha256'])

    def test_old_package_without_binding_rejected(self):
        del self.package['deployment']
        self.save_package()
        with self.assertRaises(ValueError): self.load()

    def test_every_binding_field_is_enforced(self):
        for field in self.identity:
            with self.subTest(field=field):
                self.package['deployment'] = dict(self.identity, **{field: 'stale'})
                self.save_package()
                with self.assertRaises(ValueError): self.load()

    def test_cluster_release_disagreement(self):
        self.config['active_cluster']['release'] = 'v377'
        self.save_config()
        with self.assertRaises(ValueError): self.load()

    def test_catalog_source_disagreement(self):
        with self.assertRaises(ValueError):
            load_package(self.root, canonical_manifest=self.manifest, source_sha='f' * 64)

    def test_cluster_source_disagreement(self):
        self.config['active_cluster']['release_source_sha256'] = 'f' * 64
        self.save_config()
        with self.assertRaises(ValueError): self.load()

    def test_tampered_core(self):
        (self.root / 'core.md').write_bytes(b'tampered')
        with self.assertRaises(ValueError): self.load()

    def test_tampered_cluster(self):
        (self.root / 'cluster.md').write_bytes(b'tampered')
        with self.assertRaises(ValueError): self.load()

    def test_tampered_prefix(self):
        (self.root / 'prefix.md').write_bytes(b'tampered')
        with self.assertRaises(ValueError): self.load()

    def test_missing_canonical_manifest(self):
        self.manifest.unlink()
        with self.assertRaises(OSError): self.load()

    def test_no_implicit_unbound_compatibility(self):
        with self.assertRaises((OSError, ValueError)): load_package(self.root)

    def test_changed_manifest_during_read_is_rejected(self):
        original = native.load_release.__globals__['operational_core']
        def changed(path):
            value = original(path)
            self.config['active_cluster']['release'] = 'v377'
            self.save_config()
            return value
        with patch('iald_release_binding.operational_core', side_effect=changed):
            with self.assertRaises(ValueError): self.load()

    def test_budget_integrity_still_required(self):
        self.package['budget']['remaining_tokens'] = 99999
        self.save_package()
        with self.assertRaises(ValueError): self.load()


class NativeTests(Fixture):
    def prepare_namespace(self):
        ns = server_namespace('_prepare_native_payload', '_ferramentas_para')
        ns.update(MEMORIA_EXTERNA=SimpleNamespace(nucleus_manifest=self.manifest),
            KERNEL_EXTERNO=self.catalog, ACTIVE_MODEL_ID='native',
            MODELS={'native': {'cmd': ['llama-server', '-c', '131072']}},
            PUBLIC_TOOLS=[{'function': {'name': 'search_web'}}, {'function': {'name': 'commercial'}}],
            FERRAMENTAS_FORA_DA_LOJA={'commercial'})
        return ns

    def test_current_release_formulas_and_partial_scope(self):
        prefix, identity = native.load_native_context(self.manifest, self.catalog)
        self.assertEqual(identity, self.identity)
        self.assertIn('v378', prefix)
        self.assertIn('rho_dot=', prefix)
        self.assertIn('H_3L=', prefix)
        self.assertIn('NÃO foi injetado integralmente', prefix)
        self.assertNotIn('VERY LONG EXTRACT', prefix)
        self.assertIn('PUBLIC KERNEL CATALOG', prefix)

    def test_client_history_and_vision_unchanged(self):
        messages = [{'role': 'system', 'content': 'Client preferences'},
            {'role': 'user', 'content': [{'type': 'image_url', 'image_url': {'url': 'fixture'}}]},
            {'role': 'system', 'content': 'Profile'}]
        before = deepcopy(messages)
        output = native.attach_context(messages, 'Server current release')
        self.assertEqual(messages, before)
        self.assertEqual(output[1], messages[1])
        self.assertEqual(output[0]['content'], 'Client preferences\n\nProfile\n\nServer current release')

    def test_native_tools_keep_store_filter_and_no_private_atlas(self):
        ns = self.prepare_namespace()
        payload, definitions, check = ns['_prepare_native_payload'](
            {'messages': [{'role': 'user', 'content': 'TGL'}], 'max_tokens': 4096}, 'app')
        names = [t['function']['name'] for t in definitions]
        self.assertIn('fetch_tgl', names)
        self.assertIn('search_tgl', names)
        self.assertIn('iald_kernel_read', names)
        self.assertIn('search_web', names)
        self.assertNotIn('commercial', names)
        self.assertFalse(any(n.startswith('iald_atlas_') for n in names))
        self.assertEqual(len(names), len(set(names)))
        self.assertIsInstance(check(payload), dict)

    def test_checked_again_after_tool_result_and_release_change(self):
        ns = self.prepare_namespace()
        payload, definitions, check = ns['_prepare_native_payload'](
            {'messages': [{'role': 'user', 'content': 'TGL'}]}, 'web')
        (self.root / 'cluster.md').write_bytes(b'changed after tool')
        with self.assertRaises(ValueError): check(payload)

    def test_model_switch_is_visible_failure(self):
        ns = self.prepare_namespace()
        payload, _, check = ns['_prepare_native_payload']({'messages': [{'role': 'user', 'content': 'TGL'}]}, 'web')
        ns['ACTIVE_MODEL_ID'] = 'different'
        with self.assertRaises(ValueError): check(payload)

    def test_whole_payload_growth_is_blocked_without_truncation(self):
        payload = {'messages': [{'role': 'tool', 'content': 'x' * 131072}], 'max_tokens': 4096}
        before = deepcopy(payload)
        with self.assertRaises(native.NativeContextError): native.check_text_window(payload, 131072)
        self.assertEqual(payload, before)

    def test_invalid_output_reserves(self):
        for output in (-1, 0, True, '4096', 131072, float('nan')):
            with self.subTest(output=output), self.assertRaises(native.NativeContextError):
                native.check_text_window({'messages': [], 'max_tokens': output}, 131072)

    def test_images_are_preserved_and_not_claimed_as_counted(self):
        payload = {'messages': [{'role': 'user', 'content': [{'type': 'image_url',
            'image_url': {'url': 'data:image/jpeg;base64,' + 'A' * 500000}}]}]}
        before = deepcopy(payload)
        self.assertFalse(native.check_text_window(payload, 131072)['media_tokens_measured'])
        self.assertEqual(payload, before)

    def test_formula_requests_route_to_readers_but_greetings_do_not(self):
        for text in ('Explique a TGL', 'Leia um.py v378', 'Hamiltoniano', 'Fórmulas da gravidade quântica'):
            self.assertTrue(native.needs_canonical_tools(text), text)
        self.assertFalse(native.needs_canonical_tools('Bom dia'))

    def test_startup_log_has_only_allowed_metadata(self):
        self.assertEqual(native.startup_summary(self.manifest, self.catalog),
            '[IALD-CANONICAL-CATALOG] release=v378 source_sha256=' + self.source[:16] + ' lean_files=3')

    def test_server_haiku_loader_passes_real_catalog_binding(self):
        ns = server_namespace('_load_haiku_package')
        load = Mock(side_effect=RuntimeError('loader intercepted'))
        ns.update(KERNEL_EXTERNO=self.catalog, SERVE_DIR=str(self.root), load_package=load,
            _load_haiku_snapshot=lambda directory, loader: loader(directory))
        with self.assertRaisesRegex(RuntimeError, 'intercepted'): ns['_load_haiku_package']()
        self.assertEqual(load.call_args.kwargs, {'canonical_manifest': str(self.root / 'iald_nucleo_fixo.json'),
                                              'source_sha': self.source})

    def test_agent_guard_prevents_any_dispatch(self):
        ns = server_namespace('agent_loop')
        post = Mock(side_effect=AssertionError('Model dispatch forbidden'))
        ns.update(MAX_AGENT_LOOPS=6, LLAMA_URL='http://fixture.invalid', req_lib=SimpleNamespace(post=post))
        def reject(payload): raise native.NativeContextError('fixture context refusal')
        output = list(ns['agent_loop']([{'role': 'user', 'content': 'TGL'}], ferramentas=[], verificar_payload=reject))
        self.assertIn('fixture context refusal', ''.join(output))
        self.assertIn('[DONE]', ''.join(output))
        post.assert_not_called()

    def tool_loop(self, result, check):
        ns = server_namespace('agent_loop')
        sent = []
        def post(url, **kwargs):
            sent.append(deepcopy(kwargs['json']))
            return len(sent)
        def lines(send):
            turn = send()
            delta = ({'tool_calls': [{'index': 0, 'id': 'read1', 'function': {
                'name': 'fetch_tgl', 'arguments': '{"id":"source"}'}}]} if turn == 1
                else {'content': 'fixture final'})
            yield 'line', 'data: ' + json.dumps({'choices': [{'delta': delta,
                'finish_reason': 'tool_calls' if turn == 1 else 'stop'}]})
        def keepalive(fn):
            if False: yield None
            return fn()
        ns.update(MAX_AGENT_LOOPS=6, LLAMA_URL='http://fixture.invalid',
            req_lib=SimpleNamespace(post=post), _linhas_do_stream=lines,
            _com_keepalive=keepalive, _ROTULO_FERRAMENTA={},
            auth_log=lambda *a, **kw: None, log_request=lambda *a, **kw: None,
            task_session=SimpleNamespace(NAMES=set()), AGENT_MAX_RESULT_CHARS=3200,
            BUSCA_INDISPONIVEL_PREFIXO='unavailable')
        output = list(ns['agent_loop']([{'role': 'user', 'content': 'TGL'}],
            ferramentas=[{'function': {'name': 'fetch_tgl'}}], executar=lambda *a, **kw: result,
            verificar_payload=check))
        return sent, output

    def test_full_json_canonical_page_survives_tool_round(self):
        result = json.dumps({'text': 'source ' * 650, 'next_offset': 4500,
                             'sha256': self.source, 'scope': 'fixture'})
        checks = []
        sent, output = self.tool_loop(result, lambda p: checks.append(deepcopy(p)))
        self.assertEqual(len(sent), 2)
        self.assertEqual(len(checks), 2)
        self.assertEqual(json.loads(sent[1]['messages'][-1]['content']), json.loads(result))
        self.assertIn('fixture final', ''.join(output))

    def test_oversized_tool_result_blocks_second_dispatch(self):
        checks = []
        def check(payload):
            checks.append(True)
            native.check_text_window(payload, 131072)
        sent, output = self.tool_loop('x' * 131072, check)
        self.assertEqual(len(sent), 1)
        self.assertEqual(len(checks), 2)
        self.assertIn('Contexto textual nativo excede', ''.join(output))
        self.assertIn('choices', ''.join(output))


class SourceContracts(unittest.TestCase):
    def test_route_injection_after_compression_and_after_auth(self):
        source = (STAGE / 'iald_web_server.py').read_text(encoding='utf-8')
        tree = ast.parse(source)
        route = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'api_post')
        text = ast.get_source_segment(source, route)
        self.assertLess(text.index('_caminho_nativo_permitido'), text.index('_prepare_native_payload'))
        self.assertLess(text.index('HOLO_MEMORY.compress_context'), text.index('_prepare_native_payload'))
        for route_name in ('_chat_automatico', '_chat_avaliacao', '_chat_claude', '_chat_openai'):
            self.assertLess(text.index(route_name), text.index('_prepare_native_payload'))
        self.assertLess(text.index('_prepare_native_payload'), text.index('_stream_proxy'))
        self.assertIn('verificar_payload=native_check', text)

    def test_native_model_window_and_kernel_v13_preserved(self):
        def assignments(path):
            tree = ast.parse(path.read_bytes())
            wanted = {'MODELS', 'ACTIVE_MODEL_ID', 'KERNEL_FILE'}
            return {t.id: ast.dump(n.value) for n in tree.body if isinstance(n, ast.Assign)
                for t in n.targets if isinstance(t, ast.Name) and t.id in wanted}
        self.assertEqual(assignments(STAGE / 'iald_web_server.py'),
                         assignments(STAGE / 'baseline/iald_web_server.py'))

    def test_canonical_results_do_not_enter_generic_text_truncation(self):
        source = (STAGE / 'iald_web_server.py').read_text(encoding='utf-8')
        self.assertIn("tool_name not in ('search_tgl', 'fetch_tgl')", source)


if __name__ == '__main__':
    unittest.main(verbosity=2)
