"""Installation and failure checks run only in private temporary directories."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import transaction as tx


class TransactionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='deploy_', dir=Path(__file__).parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.stage = self.root / 'stage'; self.stage.mkdir()
        self.dest = self.root / 'dest'; self.dest.mkdir()
        self.old = b'# intact CRLF\r\nx = 1\r\n'
        self.new = b'# candidate\nx = 2\n'
        self.target = self.dest / 'module.py'; self.target.write_bytes(self.old)
        self.source = self.stage / 'module.py'; self.source.write_bytes(self.new)
        self.plan = self.root / 'plan.json'
        self.review = self.root / 'review.json'
        self.payload = {'author': 'fixture-builder', 'files': [{
            'source': str(self.source), 'destination': str(self.target),
            'sha256': tx.sha(self.new), 'baseline': tx.sha(self.old)}]}
        self.write_plan()

    def write_plan(self):
        self.plan.write_text(json.dumps(self.payload), encoding='utf-8')
        self.review.write_text(json.dumps({'status': 'PASS', 'author': 'fixture-reviewer',
            'plan_sha256': tx.sha(self.plan.read_bytes()),
            'installer_sha256': tx.sha(Path(tx.__file__).read_bytes())}), encoding='utf-8')

    def run_install(self, **kw):
        return tx.install(self.plan, self.review, work_root=self.root,
            allowed_destinations=[self.target], assert_quiesced=kw.pop('guard', lambda: None),
            evidence_dir=self.root/'run', **kw)

    def test_success_backup_exact_bytes(self):
        result = self.run_install()
        self.assertEqual(result['status'], 'INSTALLED')
        self.assertEqual(self.target.read_bytes(), self.new)
        self.assertEqual(Path(result['files'][0]['backup']).read_bytes(), self.old)
        final = tx.read_json(self.root/'run/FINAL_STATE.json')
        self.assertIn('finished_utc', final)

    def test_failed_write_restores_exact_bytes(self):
        def fail(*_): raise RuntimeError('injected after replacement')
        with self.assertRaises(RuntimeError): self.run_install(after_write=fail)
        self.assertEqual(self.target.read_bytes(), self.old)
        self.assertEqual(tx.read_json(self.root/'run/FINAL_STATE.json')['rollback'][0]['outcome'], 'RESTORED_BYTES')

    def test_concurrent_edit_not_overwritten_by_rollback(self):
        def change(_, target):
            target.write_bytes(b'# another writer\n')
            raise RuntimeError('another writer')
        with self.assertRaises(RuntimeError): self.run_install(after_write=change)
        self.assertEqual(self.target.read_bytes(), b'# another writer\n')
        self.assertEqual(tx.read_json(self.root/'run/FINAL_STATE.json')['rollback'][0]['outcome'], 'CONCURRENT_EDIT_PRESERVED')

    def test_stale_baseline_refuses_before_backup(self):
        self.target.write_bytes(b'x = 3\n')
        with self.assertRaises(tx.DeploymentError): self.run_install()
        self.assertEqual(len(list(self.dest.glob('*.bak_*'))), 0)

    def test_source_mutation_refuses(self):
        self.source.write_bytes(b'x = 4\n')
        with self.assertRaises(tx.DeploymentError): self.run_install()
        self.assertEqual(self.target.read_bytes(), self.old)

    def test_review_pin_required(self):
        self.review.write_text('{}')
        with self.assertRaises(tx.DeploymentError): self.run_install()

    def test_distinct_reviewer_required(self):
        d = tx.read_json(self.review); d['author'] = 'fixture-builder'
        self.review.write_text(json.dumps(d))
        with self.assertRaises(tx.DeploymentError): self.run_install()

    def test_installer_hash_required(self):
        d = tx.read_json(self.review); d['installer_sha256'] = '0'*64
        self.review.write_text(json.dumps(d))
        with self.assertRaises(tx.DeploymentError): self.run_install()

    def test_allowlist_exact(self):
        self.payload['files'][0]['destination'] = str(self.dest/'unlisted.py')
        self.payload['files'][0]['baseline'] = None
        self.write_plan()
        with self.assertRaises(tx.DeploymentError): self.run_install()

    def test_invalid_python_rejected(self):
        self.source.write_bytes(b'this is invalid python:')
        self.payload['files'][0]['sha256'] = tx.sha(self.source.read_bytes()); self.write_plan()
        with self.assertRaises(SyntaxError): self.run_install()

    def test_maintenance_required(self):
        def reject(): raise tx.DeploymentError('not idle')
        with self.assertRaises(tx.DeploymentError): self.run_install(guard=reject)
        self.assertEqual(self.target.read_bytes(), self.old)

    def test_new_file_rollback(self):
        self.target.unlink(); self.payload['files'][0]['baseline'] = None; self.write_plan()
        def fail(*_): raise RuntimeError('injected')
        with self.assertRaises(RuntimeError): self.run_install(after_write=fail)
        self.assertFalse(self.target.exists())

    def test_repeated_run_refused(self):
        self.run_install()
        self.target.write_bytes(self.old)
        with self.assertRaises(FileExistsError): self.run_install()
        self.assertEqual(self.target.read_bytes(), self.old)

    def test_immutable_receipt_not_overwritten(self):
        p = self.root/'immutable.json'
        tx.write_new(p, b'original')
        with self.assertRaises(FileExistsError): tx.write_new(p, b'new')
        self.assertEqual(p.read_bytes(), b'original')


if __name__ == '__main__':
    unittest.main(verbosity=2)
