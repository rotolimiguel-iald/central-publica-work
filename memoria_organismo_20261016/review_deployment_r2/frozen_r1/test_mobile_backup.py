"""Mobile assets keep recovery bytes outside bundles; no production IO."""
from pathlib import Path
import unittest
from test_transaction import TransactionTests
import transaction as tx

class MobileBackupTests(TransactionTests):
    def setUp(self):
        super().setUp()
        self.target.unlink()
        self.target=self.dest/'iald.js';self.target.write_bytes(self.old)
        self.payload['files'][0].update(destination=str(self.target),
            backup_directory=str(self.root/'mobile_backups'))
        self.write_plan()

    def test_external_backup_is_not_bundled(self):
        r=self.run_install()
        b=Path(r['files'][0]['backup'])
        self.assertTrue(b.is_relative_to(self.root/'mobile_backups'))
        self.assertEqual(b.read_bytes(),self.old)
        self.assertEqual(list(self.dest.glob('*.bak_*')),[])

    def test_backup_escape_rejected(self):
        self.payload['files'][0]['backup_directory']=str(self.root/'other')
        self.write_plan()
        with self.assertRaises(tx.DeploymentError):self.run_install()
        self.assertEqual(self.target.read_bytes(),self.old)

    def test_invalid_python_rejected(self):
        # JS syntax is independently checked by A; this case exercises the
        # external-backup restriction for Python rather than its parser.
        self.target.unlink();self.target=self.dest/'module.py';self.target.write_bytes(self.old)
        self.payload['files'][0]['destination']=str(self.target);self.write_plan()
        with self.assertRaises(tx.DeploymentError):self.run_install()

if __name__=='__main__':unittest.main(verbosity=2)
