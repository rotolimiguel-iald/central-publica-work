import sys
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from iald_memoria_canonica import CanonicalMemory, MemoryUnavailable


class Catalog:
    def context(self):
        return 'SOURCE_CATALOG_TEST'


class TemporalContextTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.atlas = self.root / 'TGL_ATLAS.md'
        self.index = self.root / 'TGL_INDICE_VIVO.md'
        self.atlas.write_text('## I. Núcleo\n### I.1 Identidade\nomega(I)=1\n'
                              '### I.6 Selo antigo\nOLD_GATE\n### I.7 Aberto\nOLD_PENDING\n'
                              '## II. Termos\nBreuer\n## V. Patentes\nPRIVATE_V\n'
                              '## VI. Casas\nPRIVATE_VI\n## VII. Régua\nNOT_FALSIFIED != CONFIRMED\n'
                              '## X. Diário\nPRIVATE_X\n', encoding='utf-8')
        self.write_index('CURRENT_TOWER_RESULT')
        self.core = self.root / 'core.txt'
        self.core.write_text('LAGRANGIAN_CONTENT\nMASTER_EQUATION\nEND_OF_COMPLETE_CORE', encoding='utf-8')
        manifest = self.root / 'core.json'
        manifest.write_text(json.dumps({'format': 1, 'entries': [
            {'id': 'core', 'path': str(self.core), 'role': 'Test source'}]}), encoding='utf-8')
        self.memory = CanonicalMemory(self.atlas, 'nucleo_kernel', nucleus_manifest=manifest)

    def write_index(self, result):
        self.index.write_text('# Índice v356\n## 0. Estado\nCURRENT_GATE\n'
                              '## 1. Histórico\nOLD_INDEX_VALUE\n'
                              '## 4. Folhas abertas\n' + result + '\nGENERAL_EXTENSION_OPEN\n'
                              '## 5. Processo\nPROCESS_PRIVATE\n'
                              '## 7. Anexos\nPRIVATE_DIARY\n', encoding='utf-8')

    @patch('iald_memoria_canonica.iald_fontes_publicas.context', return_value='PUBLIC_LINKS')
    @patch('iald_memoria_canonica.count_tokens', side_effect=lambda text: len(str(text)) // 4)
    def test_old_pending_is_searchable_but_not_a_permanent_instruction(self, *_):
        prompt, metadata = self.memory.prompt('', Catalog())
        self.assertIn('omega(I)=1', prompt)
        self.assertNotIn('OLD_PENDING', prompt)
        self.assertNotIn('OLD_GATE', prompt)
        self.assertIn('CURRENT_TOWER_RESULT', prompt)
        self.assertIn('GENERAL_EXTENSION_OPEN', prompt)
        self.assertNotIn('PRIVATE_DIARY', prompt)
        self.assertNotIn('PROCESS_PRIVATE', prompt)
        self.assertIn('OLD_PENDING', str(self.memory.search('OLD_PENDING')))
        self.assertIn('Hamiltoniano limitado inferiormente', prompt)
        self.assertIn('dephasing pelos operadores de Lindblad', prompt)
        self.assertIn('simulação deve dizer SIMULAÇÃO', prompt)
        self.assertIn(self.core.read_bytes().decode('utf-8'), prompt)
        self.assertTrue(metadata['fixed_nucleus_complete'])
        self.core.write_text('UPDATED_CORE\nEND_OF_COMPLETE_CORE', encoding='utf-8')
        self.write_index('NEW_CURRENT_RESULT')
        newer, changed = self.memory.prompt('', Catalog())
        self.assertIn('NEW_CURRENT_RESULT', newer)
        self.assertIn('UPDATED_CORE', newer)
        self.assertNotIn('CURRENT_TOWER_RESULT', newer)
        self.assertNotEqual(metadata['current_index_sha256'], changed['current_index_sha256'])
        self.index.unlink()
        with self.assertRaises(MemoryUnavailable):
            self.memory.prompt('', Catalog())

    @patch('iald_memoria_canonica.count_tokens', side_effect=lambda text: len(str(text)) // 4)
    def test_missing_required_core_is_visible_not_silently_omitted(self, *_):
        self.core.unlink()
        with self.assertRaises(MemoryUnavailable):
            self.memory.fixed_nucleus()

    @patch('iald_memoria_canonica.count_tokens', side_effect=lambda text: len(str(text)) // 4)
    def test_restricted_atlas_search_and_read_do_not_expose_live_index(self, *_):
        for result in (self.memory.search('PRIVATE', suppress=('V', 'VI', 'X')),
                       self.memory.read(1, 100, suppress=('V', 'VI', 'X'))):
            payload = str(result)
            self.assertNotIn('CURRENT_TOWER_RESULT', payload)
            self.assertNotIn('PRIVATE_V', payload)
            self.assertNotIn('PRIVATE_X', payload)


if __name__ == '__main__':
    unittest.main()
