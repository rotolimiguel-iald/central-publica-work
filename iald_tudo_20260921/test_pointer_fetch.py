import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

WORK = Path(__file__).resolve().parent
sys.path.insert(0, r'C:\IALD\projetos_pyhton\IALD')
spec = importlib.util.spec_from_file_location('pointer_candidate', WORK / 'iald_core_indexado_candidate.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PointerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.doc = root / 'published.json'
        self.data = {'core': {'a/b': {'~x': ['αβ' * 3000, False, 0]}, 'n_q': 1, 'N_q': 2}}
        raw = json.dumps(self.data, ensure_ascii=False).encode()
        self.doc.write_bytes(raw)
        self.manifest = root / 'manifest.json'
        self.manifest.write_text(json.dumps({'format': 1, 'entries': [{
            'id': 'published', 'path': str(self.doc), 'role': 'test',
            'public_sha256': hashlib.sha256(raw).hexdigest(),
            'url': 'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/' + 'a'*40 + '/published.json'}]}))

    def fetch(self, **kwargs):
        return module.execute_tool(self.manifest, 'fetch_tgl', {'id': 'published', **kwargs})

    def test_pages_reconstruct_selected_unicode_value(self):
        pages, offset = [], 0
        while True:
            row = self.fetch(pointer='/core/a~1b/~0x/0', offset=offset, max_chars=1000)
            self.assertFalse(row['whole_document'])
            self.assertEqual(row['offset_scope'], 'SELECTED_JSON_VALUE')
            pages.append(row['text'])
            if row['next_offset'] is None:
                break
            offset = row['next_offset']
        self.assertEqual(json.loads(''.join(pages)), self.data['core']['a/b']['~x'][0])

    def test_false_zero_and_case_are_not_missing(self):
        self.assertEqual(self.fetch(pointer='/core/a~1b/~0x/1')['text'], 'false')
        self.assertEqual(self.fetch(pointer='/core/a~1b/~0x/2')['text'], '0')
        self.assertEqual(self.fetch(pointer='/core/N_q')['text'], '2')

    def test_invalid_paths_fail_without_fallback(self):
        for pointer in ('core', '/missing', '/core/a~2b', '/core/a~1b/~0x/-1', '/core/a~1b/~0x/00', '/core/N_q/x'):
            with self.subTest(pointer=pointer), self.assertRaises(ValueError):
                self.fetch(pointer=pointer)

    def test_changed_source_fails_integrity(self):
        self.doc.write_bytes(b'{}')
        with self.assertRaises(ValueError):
            self.fetch(pointer='/core')

    def test_legacy_document_read_still_works(self):
        row = self.fetch(max_chars=20)
        self.assertEqual(row['text'], self.doc.read_text(encoding='utf-8')[:20])
        self.assertNotIn('pointer', row)
        self.assertFalse(row['whole_document'])


if __name__ == '__main__':
    unittest.main()
