"""Isolated tests for provenance, fail-closed behavior and server routing."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(WORK))
import iald_core_indexado as core
import iald_memoria_canonica as memory


class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.doc = self.root / 'article.md'
        self.raw = ('# Informação\r\n' + ''.join(f'Lindblad linha {i}: α β Π± C±\r\n' for i in range(60))
                    + 'fim😀\u2028posição\n').encode()
        self.doc.write_bytes(self.raw)
        self.manifest = self.root / 'manifest.json'
        self.config = {'format': 1, 'document_mode': 'retrievable', 'entries': [{
            'id': 'article', 'path': str(self.doc), 'role': 'Published test article',
            'url': 'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/' + 'a' * 40 + '/article.md',
            'public_sha256': hashlib.sha256(self.raw).hexdigest()}]}
        self.save()
        self.corpus = core.DocumentCorpus(self.manifest)

    def save(self):
        self.manifest.write_text(json.dumps(self.config), encoding='utf-8')

    def test_unicode_crlf_pagination_preserves_every_character(self):
        offset, parts = 0, []
        while offset is not None:
            page = self.corpus.fetch('article', offset, 31)
            parts.append(page['text'])
            offset = page['next_offset']
        self.assertEqual(''.join(parts).encode(), self.raw)

    def test_search_coordinates_allow_exact_followup_fetch(self):
        for hit in self.corpus.search('Lindblad')['results']:
            page = self.corpus.fetch(hit['id'], hit['offset'], 200)
            self.assertTrue(page['text'].startswith(self.raw.decode().splitlines()[hit['line']-1]))
            self.assertEqual(hit['sha256'], hashlib.sha256(self.raw).hexdigest())

    def test_hash_change_blocks_both_operator_and_public(self):
        self.doc.write_bytes(self.raw + b'UNREVIEWED_APPEND')
        for public in (True, False):
            with self.assertRaises(ValueError):
                self.corpus.context(public=public)

    def test_source_must_be_pinned_to_exact_approved_repository_commit(self):
        for url in ('https://example.org/private', 'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/article.md',
                    'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary.evil/' + 'a'*40 + '/x'):
            self.config['entries'][0]['url'] = url
            self.save()
            with self.assertRaises(ValueError):
                self.corpus.fetch('article')

    def test_duplicate_ids_fail_instead_of_hiding_a_document(self):
        self.config['entries'].append(dict(self.config['entries'][0]))
        self.save()
        with self.assertRaises(ValueError):
            self.corpus.search('Lindblad')

    def test_tools_cannot_read_arbitrary_paths_or_accept_extra_arguments(self):
        for name, args in [('fetch_tgl', {'id': str(self.doc)}),
                           ('fetch_tgl', {'id': 'article', 'path': str(self.doc)}),
                           ('ratify_memory_candidate', {'id': 'article'})]:
            with self.assertRaises(ValueError):
                core.execute_tool(self.manifest, name, args)

    def test_empty_queries_and_out_of_range_offsets_are_rejected(self):
        for query in ('', '  ', 'x'*1001):
            with self.assertRaises(ValueError):
                self.corpus.search(query)
        for offset in (-1, len(self.raw.decode())+1):
            with self.assertRaises(ValueError):
                self.corpus.fetch('article', offset)

    def test_partial_page_is_not_claimed_as_full_document(self):
        self.assertFalse(self.corpus.fetch('article', max_chars=20)['whole_document'])
        self.assertTrue(self.corpus.fetch('article', max_chars=4500)['whole_document'])

    def test_public_prompt_does_not_read_private_atlas_or_journal(self):
        mem = memory.CanonicalMemory(self.root / 'private.md', 'nucleo_kernel', nucleus_manifest=self.manifest)
        with patch.object(mem, 'snapshot', side_effect=AssertionError('PRIVATE_READ')), \
             patch.object(mem, 'current_state', side_effect=AssertionError('JOURNAL_READ')), \
             patch.object(memory, 'count_tokens', side_effect=lambda s: len(s)//4):
            body, meta = mem.prompt('', types.SimpleNamespace(context=lambda: 'KERNEL'), public=True)
        self.assertNotIn(self.raw.decode(), body)
        self.assertTrue(meta['retrievable_documents_complete'])
        self.assertFalse(meta['fixed_nucleus_complete'])
        self.assertFalse(meta['private_atlas_included'])
        self.assertNotIn('atlas_sha256', meta)

    def install_core(self):
        path = self.root / 'core.md'
        path.write_bytes(b'COMPLETE_ORIGINAL_CORE\r\nHISTORICAL_v334\r\n')
        self.config['operational_core'] = {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'version': '1.0.0', 'current_release': 'v357', 'release_source_sha256': 'b'*64}
        self.save()
        return path

    def test_core_preserved_whole_with_historical_record(self):
        path = self.install_core()
        body, meta = core.operational_core(self.manifest)
        self.assertIn(path.read_bytes().decode(), body)
        self.assertEqual(meta['operational_core']['current_release'], 'v357')
        self.assertIn('retrato histórico', body)

    def test_core_change_is_not_silently_accepted(self):
        path = self.install_core()
        path.write_bytes(path.read_bytes() + b'UNRATIFIED')
        with self.assertRaises(ValueError):
            core.operational_core(self.manifest)

    def test_release_label_must_match_pinned_publication(self):
        self.install_core()
        mem = memory.CanonicalMemory(self.root/'private.md', 'nucleo_kernel', nucleus_manifest=self.manifest)
        with patch.object(memory, 'published_evidence', return_value=('', {'published_source_sha256': 'c'*64})), \
             self.assertRaises(memory.MemoryUnavailable):
            mem.prompt('', types.SimpleNamespace(context=lambda: 'KERNEL'), public=True)

    def test_missing_core_is_reported_as_memory_unavailable(self):
        path = self.install_core()
        path.unlink()
        mem = memory.CanonicalMemory(self.root/'private.md', 'nucleo_kernel', nucleus_manifest=self.manifest)
        with self.assertRaises(memory.MemoryUnavailable):
            mem.prompt('', types.SimpleNamespace(context=lambda: 'KERNEL'), public=True)


class RoutingTests(unittest.TestCase):
    def setUp(self):
        tree = ast.parse((WORK / 'iald_web_server.py').read_bytes())
        selected = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in {
            'execute_public_tool', '_executar_ferramenta_gratuito', '_ferramentas_externas', '_contexto_externo'}]
        self.fake_core = types.SimpleNamespace(execute_tool=Mock(return_value={'status': 'OK', 'text': 'published'}),
                                               tool_definitions=core.tool_definitions)
        self.cfg = types.SimpleNamespace(gratuito_atlas=False, memoria_modo='nucleo_kernel', ferramentas=[])
        self.mem = types.SimpleNamespace(nucleus_manifest='manifest.json', prompt=Mock(return_value=('PROMPT', {})))
        self.ns = {'json': json, 'iald_core_indexado': self.fake_core, 'MEMORIA_EXTERNA': self.mem,
                   'MOTORES_CFG': self.cfg, 'ERRO_MEMORIA_EXTERNA': '', 'KERNEL_EXTERNO': object(), 'PROMPT_EXTERNO': '',
                   'iald_kernel': types.SimpleNamespace(tool_definitions=lambda: []),
                   'iald_memoria_canonica': types.SimpleNamespace(tool_definitions=lambda: [{'function': {'name': 'PRIVATE_ATLAS'}}]),
                   'iald_fontes_publicas': types.SimpleNamespace(tool_definitions=lambda: [])}
        exec(compile(ast.Module(body=selected, type_ignores=[]), str(WORK/'iald_web_server.py'), 'exec'), self.ns)

    def test_testers_receive_corpus_tools_without_private_atlas(self):
        tools = self.ns['_ferramentas_externas'](self.cfg, {}, 'app', True)
        self.assertEqual({item['function']['name'] for item in tools}, {'search_tgl', 'fetch_tgl'})

    def test_free_executor_can_retrieve_published_document(self):
        result = self.ns['_executar_ferramenta_gratuito']('fetch_tgl', {'id': 'article'}, 'tester', True)
        self.assertEqual(json.loads(result)['text'], 'published')
        self.fake_core.execute_tool.assert_called_once_with('manifest.json', 'fetch_tgl', {'id': 'article'})

    def test_free_executor_still_denies_private_atlas(self):
        result = self.ns['_executar_ferramenta_gratuito']('iald_atlas_read', {}, 'tester', True)
        self.assertEqual(json.loads(result)['status'], 'UNAVAILABLE')
        self.fake_core.execute_tool.assert_not_called()

    def test_file_error_fails_closed_without_revealing_server_path(self):
        self.fake_core.execute_tool.side_effect = OSError('C:/private/path/secret')
        result = self.ns['execute_public_tool']('search_tgl', {'query': 'x'})
        self.assertEqual(json.loads(result)['status'], 'UNAVAILABLE')
        self.assertNotIn('private/path', result)

    def test_public_context_flag_reaches_memory_loader(self):
        self.ns['_contexto_externo'](public=True)
        self.assertTrue(self.mem.prompt.call_args.kwargs['public'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
