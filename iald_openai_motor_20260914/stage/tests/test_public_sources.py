import json
from pathlib import Path
import tempfile
import unittest
from urllib.parse import quote
import iald_fontes_publicas as sources
from iald_memoria_canonica import CanonicalMemory


class PublicSourcesTests(unittest.TestCase):
    def test_generated_paths_are_exact_and_encoded(self):
        data = sources.catalog()
        for entry in data['entries']:
            if 'path' in entry:
                self.assertEqual(entry['url'], data['raw_base'] + quote(entry['path'], safe='/'))
        self.assertEqual(len(data['entries']), 15)

    def test_addresses_and_boundaries_accompany_every_prompt(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'atlas.md'
            path.write_bytes('## I. Núcleo\nAxioma\n## II. Documentos\nOutro\n## VII. Régua\nEstatutos'.encode())
            memory = CanonicalMemory(path, 'nucleo_kernel')
            kernel = type('Kernel', (), {'context': lambda self: 'Kernel local'})()
            for question in range(2):
                prompt, _ = memory.prompt('', kernel)
                for entry in sources.catalog()['entries']:
                    self.assertIn(entry['url'], prompt)
                self.assertIn('TGL = ATLAS. IALD = ÍNDICE(TGL).', prompt)
                self.assertIn('ferramenta de internet estiver indisponível', prompt)
                self.assertIn('versão pública pode diferir da local', prompt)

    def test_missing_or_foreign_source_fails_visibly(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'missing.json'
            with self.assertRaises(OSError):
                sources.catalog(path)
            data = sources.catalog()
            data['entries'][0]['url'] = 'http://127.0.0.1/private'
            path.write_bytes(json.dumps(data).encode())
            with self.assertRaises(ValueError):
                sources.catalog(path)


if __name__ == '__main__':
    unittest.main()
