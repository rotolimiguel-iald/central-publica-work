"""Offline reproducer: cache publication cannot safely replace a live generation."""
import ast
import hashlib
import json
from pathlib import Path
import socket
import sys
import tempfile
import unittest
from unittest.mock import patch

WORK = Path(__file__).resolve().parent
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.path.insert(0, str(BASE))
sys.dont_write_bytecode = True
from iald_orchestrator import canonical_memory as memory
from iald_orchestrator.safe_files import replace_bytes, save_json


class RefreshSafety(unittest.TestCase):
    def setUp(self):
        fixture = WORK / 'fixtures'
        fixture.mkdir(exist_ok=True)
        # Keep immediate backups from this session, including test fixtures.
        self.root = Path(tempfile.mkdtemp(dir=fixture))
        self.source = self.root / 'um_absoluto_forma_canonica.md'
        self.old = b'OLD_GENERATION fixture canonical text.\n'
        self.new = b'NEW_GENERATION fixture canonical text.\n'
        replace_bytes(self.source, self.old)
        self.catalog = self.root / 'catalog.json'
        save_json(self.catalog, {'files': [{'source': str(self.source),
                                          'sha256': hashlib.sha256(self.old).hexdigest()}]})
        self.cache = self.root / 'cache'
        self.before = memory.build(directory=self.cache, catalog=self.catalog)

    def update(self):
        replace_bytes(self.source, self.new)
        return memory.build(directory=self.cache, catalog=self.catalog)

    def test_builder_preserves_immediate_byte_backups(self):
        old_index = (self.cache / 'index.sqlite3').read_bytes()
        old_manifest = (self.cache / 'manifest.json').read_bytes()
        self.update()
        self.assertTrue(any(p.read_bytes() == old_index for p in self.cache.glob('index.sqlite3.bak_*')))
        self.assertTrue(any(p.read_bytes() == old_manifest for p in self.cache.glob('manifest.json.bak_*')))

    def test_prepared_payload_is_immutable_across_a_rebuild(self):
        packet = memory.prepare('canonical', directory=self.cache)
        raw = json.dumps(packet, sort_keys=True)
        after = self.update()
        self.assertNotEqual(after['generation'], packet['receipt']['generation'])
        self.assertEqual(json.dumps(packet, sort_keys=True), raw)

    def test_reader_can_label_new_bytes_with_old_generation(self):
        original_load = memory.load
        def interleaved(directory):
            old = original_load(directory, refresh=False)
            self.update()  # Legal interleaving after load releases its local lock.
            return old
        with patch.object(memory, 'load', side_effect=interleaved):
            packet = memory.prepare('canonical', directory=self.cache)
        self.assertEqual(packet['receipt']['generation'], self.before['generation'])
        self.assertIn('NEW_GENERATION', packet['prompt'])
        self.assertEqual(packet['receipt']['sources'][0]['sha256'], hashlib.sha256(self.old).hexdigest())

    def test_pinned_generation_is_refused_not_silently_rebound(self):
        after = self.update()
        tree = ast.parse((BASE / 'iald_orchestrator/request_controls.py').read_bytes())
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'enforce_packet')
        namespace = {}
        exec(compile(ast.Module(body=[fn], type_ignores=[]), '<enforce-only>', 'exec'), namespace)
        packet = {'prompt': 'fixture', 'receipt': {'generation': after['generation'], 'sources': []}}
        with self.assertRaisesRegex(ValueError, 'Geração canônica diferente'):
            namespace['enforce_packet'](packet, {'max_projection_chars': None,
                'memory_generation': self.before['generation']}, '')


if __name__ == '__main__':
    with patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden')):
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(RefreshSafety)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    save_json(WORK / 'safety_tests.json', {'tests': result.testsRun,
        'failures': len(result.failures), 'errors': len(result.errors),
        'passed': result.wasSuccessful(), 'known_concurrency_gap_reproduced': result.wasSuccessful(),
        'scope': 'SYNTHETIC_OFFLINE_FIXTURES__NO_LIVE_CACHE_WRITES'})
    raise SystemExit(0 if result.wasSuccessful() else 1)
