"""Offline transaction regressions, confined to reviewer temporary directories."""
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch
import hashlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest

W = Path(__file__).resolve().parents[1]
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def guard(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'subprocess.Popen', 'os.system'):
        raise RuntimeError('No network or child processes in review')
sys.addaudithook(guard)
pin = sha(W / 'transaction.py')
spec = importlib.util.spec_from_file_location('reviewed_transaction', W / 'transaction.py')
tx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tx)

class TransactionReview(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(dir=W)
        self.addCleanup(temp.cleanup)
        self.work = Path(temp.name) / 'review'
        self.root = Path(temp.name) / 'app'
        self.work.mkdir(); self.root.mkdir()
        (self.work / 'validation').mkdir()
        self.old = b'{"version": 1}\r\n'
        self.new = b'{"version": 2}\n'
        self.files = []
        for name in ('runtime.json', 'iald_nucleo_fixo.json'):
            src = self.work / name; dest = self.root / name
            src.write_bytes(self.new); dest.write_bytes(self.old)
            self.files.append({'source': str(src), 'destination': str(dest), 'sha256': sha(src), 'baseline': sha(dest)})
        self.plan = self.work / 'plan.json'
        self.plan.write_text(json.dumps({'files': self.files}), encoding='utf-8')
        for name, status in [('final_checks.json', {'passed': True}), ('review_final.json', {'status': 'PASS'})]:
            (self.work / 'validation' / name).write_text(json.dumps(dict(status, plan_sha256=sha(self.plan))), encoding='utf-8')
        for name, value in [('WORK', self.work), ('ROOT', self.root), ('quiet', lambda: {})]:
            p = patch.object(tx, name, value); p.start(); self.addCleanup(p.stop)

    def test_backups_keep_exact_crlf_bytes_and_manifest_written_last(self):
        order = []
        original = tx.atomic
        def record(path, raw):
            if Path(path).is_relative_to(self.root):
                # All replaced files already have immediate byte backups.
                for item in self.files:
                    backups = list(Path(item['destination']).parent.glob(Path(item['destination']).name + '.bak_*'))
                    self.assertEqual(len(backups), 1)
                    self.assertEqual(backups[0].read_bytes(), self.old)
                order.append(Path(path).name)
            original(path, raw)
        with patch.object(tx, 'atomic', record): tx.apply_plan(self.plan)
        self.assertEqual(order, ['runtime.json', 'iald_nucleo_fixo.json'])
        self.assertEqual((self.root / 'iald_nucleo_fixo.json').read_bytes(), self.new)

    def test_failure_after_manifest_commit_restores_all_original_bytes(self):
        original = tx.atomic
        failed = [False]
        def inject(path, raw):
            original(path, raw)
            if Path(path).name == 'iald_nucleo_fixo.json' and not failed[0]:
                failed[0] = True
                raise OSError('Synthetic post-manifest failure')
        with patch.object(tx, 'atomic', inject):
            with self.assertRaises(OSError): tx.apply_plan(self.plan)
        for item in self.files:
            self.assertEqual(Path(item['destination']).read_bytes(), self.old)
        self.assertFalse((self.work / 'deployment.json').exists())

    def test_unreviewed_plan_causes_no_backup_or_destination_write(self):
        review = self.work / 'validation/review_final.json'
        review.write_text(json.dumps({'status': 'PASS', 'plan_sha256': '0' * 64}), encoding='utf-8')
        with self.assertRaises(ValueError): tx.apply_plan(self.plan)
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ['iald_nucleo_fixo.json', 'runtime.json'])
        for item in self.files: self.assertEqual(Path(item['destination']).read_bytes(), self.old)

    def test_concurrent_foreign_content_is_not_overwritten_by_rollback(self):
        original = tx.atomic
        def inject(path, raw):
            original(path, raw)
            if Path(path).name == 'iald_nucleo_fixo.json':
                Path(path).write_bytes(b'foreign concurrent content\n')
                raise OSError('Synthetic concurrent replacement')
        with patch.object(tx, 'atomic', inject):
            with self.assertRaises(OSError): tx.apply_plan(self.plan)
        self.assertEqual((self.root / 'runtime.json').read_bytes(), self.old)
        self.assertEqual((self.root / 'iald_nucleo_fixo.json').read_bytes(), b'foreign concurrent content\n')

if __name__ == '__main__':
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TransactionReview))
    report = {'status': 'PASS' if result.wasSuccessful() and sha(W / 'transaction.py') == pin else 'FAIL',
              'reviewed_at_utc': datetime.now(timezone.utc).isoformat(), 'tests': result.testsRun,
              'transaction_sha256': pin, 'reviewer_script_sha256': sha(__file__), 'output': stream.getvalue(),
              'scope': 'Only synthetic temporary files under W; production not written; no service or provider calls.',
              'limit': 'New immutable release files may remain after rollback; old manifest and changed existing files are restored. Concurrent foreign changes are preserved.'}
    dest = W / 'validation/transaction_review.json'
    if dest.exists(): dest.with_name(dest.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f')).write_bytes(dest.read_bytes())
    raw = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode()
    tmp = dest.with_name(dest.name + '.tmp_' + str(os.getpid()))
    tmp.write_bytes(raw); assert tmp.read_bytes() == raw; os.replace(tmp, dest)
    print(json.dumps({'status': report['status'], 'tests': result.testsRun, 'sha256': sha(dest), 'transaction_sha256': pin}))
    if not result.wasSuccessful(): print(stream.getvalue())
