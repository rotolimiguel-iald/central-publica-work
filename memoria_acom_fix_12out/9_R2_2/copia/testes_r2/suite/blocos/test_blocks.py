"""D5: aplicar_blocos.py on COPIES of the five instruction files, SESSION_BRIDGE.md and MEMORY.md.
Originals are never touched: every test works on a fresh copy inside its own temp folder."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
COPIAS = ROOT / 'blocos' / 'copias'
spec = importlib.util.spec_from_file_location('aplicar_blocos', ROOT / 'aplicar_blocos.py')
ab = importlib.util.module_from_spec(spec); spec.loader.exec_module(ab)
FIVE = {'CLAUDE_global.md': ('LF', 620, '3106d7234c7a3b71'), 'AGENTS.md': ('LF', 620, '3106d7234c7a3b71'),
        'CLAUDE_nativa.md': ('CRLF', 624, '2ca1cb060ecd2119'), 'README.md': ('LF', 620, '3106d7234c7a3b71'),
        'COORDINATOR.md': ('LF', 620, '3106d7234c7a3b71')}


def sha16(data):
    return hashlib.sha256(data).hexdigest()[:16]


class BlockTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)
        for name in list(FIVE) + ['MEMORY.md']:
            shutil.copyfile(COPIAS / name, self.work / name)
        shutil.copyfile(ROOT / 'originais' / 'C' / 'IALD' / 'MEMORIA_IALD' / 'SESSION_BRIDGE.md', self.work / 'SESSION_BRIDGE.md')
        self.base_lf = ab.bloco_novo_base(ROOT / 'SESSION_BRIDGE_v2.md')
        self.ordem = ab.ordem_sha16(ab.ORDEM_DEFAULT)

    def test_replace_block_exact_bytes_lf_and_crlf(self):
        for name, (ending, size, digest) in FIVE.items():
            with self.subTest(file=name):
                path = self.work / name; old = path.read_bytes()
                receipt = ab.aplicar_arquivo(path, self.base_lf, self.ordem)
                new = path.read_bytes(); nl = b'\r\n' if ending == 'CRLF' else b'\n'
                self.assertEqual((receipt['line_ending'], receipt['block_old_bytes'], receipt['block_old_sha16']), (ending, size, digest))
                self.assertTrue(new.startswith(ab.NEW_START + nl))
                self.assertEqual(new[receipt['block_new_bytes']:], old[size:])  # the rest is byte-identical
                block = new[:receipt['block_new_bytes']]
                self.assertTrue(block.endswith(ab.NEW_END + nl + nl)); self.assertEqual(block.count(b'\r\n'), block.count(b'\n') if ending == 'CRLF' else 0)
                self.assertTrue(new[receipt['block_new_bytes']:].startswith(b'#') or new[receipt['block_new_bytes']:].startswith(b'<!--'))
                registro = ('bloco anterior (%d B, sha16 %s) substituído em 12/10/2026 por ordem do operador («resolva a questão da memória», sha16 78ef70e6f9868281)' % (size, digest)).encode('utf-8')
                self.assertIn(registro, block)
                backup = Path(receipt['backup']); self.assertEqual(backup.read_bytes(), old)
                self.assertEqual(receipt['new_sha256'], hashlib.sha256(new).hexdigest())
                with self.assertRaises(ab.BlocoError):  # idempotence: the new block is not the old marker
                    ab.aplicar_arquivo(path, self.base_lf, self.ordem)

    def test_session_bridge_whole_file(self):
        path = self.work / 'SESSION_BRIDGE.md'; old = path.read_bytes()
        receipt = ab.aplicar_arquivo(path, self.base_lf, self.ordem)
        self.assertEqual((receipt['block_old_bytes'], receipt['block_old_sha16'], receipt['rest_bytes']), (len(old), sha16(old), 0))
        self.assertEqual((len(old), sha16(old)), (887, '49f1626d52d9cd6c'))
        new = path.read_bytes()
        self.assertTrue(new.startswith(ab.NEW_START + b'\n')); self.assertTrue(new.endswith(ab.NEW_END + b'\n\n'))
        self.assertIn(b'(887 B, sha16 49f1626d52d9cd6c)', new)

    def test_cas_abort_on_unexpected_head(self):
        path = self.work / 'AGENTS.md'; old = path.read_bytes()
        path.write_bytes(old[:100] + b'X' + old[101:])  # one byte inside the old block
        with self.assertRaises(ab.BlocoError) as ctx:
            ab.aplicar_arquivo(path, self.base_lf, self.ordem)
        self.assertIn('CAS', str(ctx.exception))
        self.assertEqual(path.read_bytes(), old[:100] + b'X' + old[101:]); self.assertEqual(list(self.work.glob('AGENTS.md.bak_*')), [])
        other = self.work / 'README.md'; other.write_bytes(b'# sem bloco\n' + other.read_bytes())
        with self.assertRaises(ab.BlocoError):
            ab.aplicar_arquivo(other, self.base_lf, self.ordem)

    def test_memory_md_single_line_and_limits(self):
        path = self.work / 'MEMORY.md'; old = path.read_bytes()
        receipt = ab.aplicar_memory_md(path)
        new = path.read_bytes(); old_lines, new_lines = old.split(b'\n'), new.split(b'\n')
        self.assertEqual(len(old_lines), len(new_lines))
        changed = [i for i, (a, b) in enumerate(zip(old_lines, new_lines)) if a != b]
        self.assertEqual(changed, [receipt['line_index'] - 1])
        self.assertTrue(new_lines[changed[0]].startswith(ab.MEMORY_LINE_PREFIX)); self.assertIn(b'SESSION_BRIDGE.md', new_lines[changed[0]])
        self.assertLessEqual(receipt['lines'], 200); self.assertLessEqual(receipt['bytes'], 24000)
        self.assertEqual(Path(receipt['backup']).read_bytes(), old)
        twice = self.work / 'MEMORY_twice.md'; twice.write_bytes(old + ab.MEMORY_LINE_PREFIX + b' outra\n')
        with self.assertRaises(ab.BlocoError):
            ab.aplicar_memory_md(twice)
        big = self.work / 'MEMORY_big.md'; big.write_bytes(old + b'- enchimento\n' * 40)
        before = big.read_bytes()
        with self.assertRaises(ab.BlocoError):
            ab.aplicar_memory_md(big)
        self.assertEqual(big.read_bytes(), before)

    def test_cli_dry_run_writes_nothing(self):
        targets = [str(self.work / n) for n in FIVE]
        before = {n: (self.work / n).read_bytes() for n in list(FIVE) + ['MEMORY.md']}
        recibo = self.work / 'recibo.json'
        status = ab.main(['--dry-run', '--recibo', str(recibo), '--memory-md', str(self.work / 'MEMORY.md')] + sum((['--alvo', t] for t in targets), []))
        self.assertEqual(status, 0)
        self.assertEqual({n: (self.work / n).read_bytes() for n in before}, before)
        self.assertEqual(list(self.work.glob('*.bak_*')), [])
        data = json.loads(recibo.read_text(encoding='utf-8'))
        self.assertEqual(len(data['arquivos']), 5); self.assertTrue(data['dry_run']); self.assertEqual(data['falhas'], [])
        self.assertEqual(data['ordem_sha16'], '78ef70e6f9868281')


if __name__ == '__main__':
    unittest.main(verbosity=2)
