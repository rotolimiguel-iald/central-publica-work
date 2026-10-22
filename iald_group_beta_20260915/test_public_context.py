import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import iald_memoria_canonica as memory


class Catalog:
    def context(self):
        return 'FORMAL_KERNEL_CATALOG'


class PublicContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.doc = self.root / 'paper.txt'
        self.raw = b'FULL_PUBLIC_PAPER\r\nEQUATIONS_AT_END\r\n'
        self.doc.write_bytes(self.raw)
        self.manifest = self.root / 'nucleus.json'
        self.config = {'format': 1, 'entries': [{'id': 'paper', 'path': str(self.doc),
            'role': 'PUBLIC_PAPER', 'url': 'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/commit/paper.txt',
            'public_sha256': hashlib.sha256(self.raw).hexdigest()}]}
        self.save()
        self.memory = memory.CanonicalMemory(self.root / 'private_atlas.md', 'nucleo_kernel',
                                            nucleus_manifest=self.manifest)
        self.counter = patch.object(memory, 'count_tokens', side_effect=lambda text: len(text)//4)
        self.counter.start()
        self.addCleanup(self.counter.stop)

    def save(self):
        self.manifest.write_text(json.dumps(self.config), encoding='utf-8')

    def test_complete_public_context_never_reads_private_atlas_or_journal(self):
        with patch.object(self.memory, 'snapshot', side_effect=AssertionError('PRIVATE_ATLAS_READ')), \
             patch.object(self.memory, 'current_state', side_effect=AssertionError('PRIVATE_JOURNAL_READ')):
            body, meta = self.memory.prompt('', Catalog(), public=True)
        self.assertIn(self.raw.decode(), body)
        self.assertIn('FORMAL_KERNEL_CATALOG', body)
        self.assertEqual(meta['scope'], 'PUBLIC_FIXED_SOURCES')
        self.assertFalse(meta['private_atlas_included'])
        self.assertNotIn('atlas_sha256', meta)
        self.assertTrue(meta['fixed_nucleus_complete'])

    def test_changed_public_source_fails_closed(self):
        self.doc.write_bytes(self.raw + b'UNPUBLISHED_PRIVATE_APPEND')
        with self.assertRaises(memory.MemoryUnavailable):
            self.memory.prompt('', Catalog(), public=True)

    def test_missing_public_pin_or_unapproved_url_is_rejected(self):
        for field, value in [('public_sha256', None), ('url', 'https://example.com/private.txt')]:
            with self.subTest(field=field):
                saved = self.config['entries'][0][field]
                self.config['entries'][0][field] = value
                self.save()
                with self.assertRaises(memory.MemoryUnavailable):
                    self.memory.prompt('', Catalog(), public=True)
                self.config['entries'][0][field] = saved

    def test_operator_still_requires_private_canonical_source(self):
        with self.assertRaises(memory.MemoryUnavailable):
            self.memory.prompt('', Catalog())


if __name__ == '__main__':
    unittest.main(verbosity=2)
