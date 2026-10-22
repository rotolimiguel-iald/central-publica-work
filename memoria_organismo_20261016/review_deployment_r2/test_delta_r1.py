"""Independent installation delta controls; all mutation stays in private fixtures."""
import io
import json
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE/'frozen_r1'))
import transaction as tx
import controlled as controlled
from test_transaction import TransactionTests
from test_mobile_backup import MobileBackupTests

class DeltaTests(MobileBackupTests):
    def test_two_same_named_assets_restore_distinct_bytes(self):
        dest2 = self.dest/'ios'; dest2.mkdir()
        target2 = dest2/'iald.js'; old2 = b'// iOS baseline\r\n'; target2.write_bytes(old2)
        self.payload['files'].append(dict(self.payload['files'][0],
            destination=str(target2), baseline=tx.sha(old2)))
        self.write_plan()
        def fail(index, _target):
            if index == 1:
                raise RuntimeError('both assets replaced')
        with self.assertRaises(RuntimeError):
            tx.install(self.plan, self.review, work_root=self.root,
                allowed_destinations=[self.target,target2], assert_quiesced=lambda:None,
                evidence_dir=self.root/'run', after_write=fail)
        result = tx.read_json(self.root/'run/FINAL_STATE.json')
        backups = [Path(row['backup']) for row in result['files']]
        self.assertEqual(len(set(backups)), 2)
        self.assertEqual([p.read_bytes() for p in backups], [self.old,old2])
        self.assertEqual(self.target.read_bytes(), self.old)
        self.assertEqual(target2.read_bytes(), old2)
        self.assertEqual([r['outcome'] for r in result['rollback']], ['RESTORED_BYTES']*2)
        self.assertFalse(list(self.dest.rglob('*.bak_*')))

    def test_corrupt_external_backup_is_visible_and_not_restored(self):
        def corrupt_then_fail(_index, _target):
            row = tx.read_json(self.root/'run/0000_prepared.json')
            Path(row['backup']).write_bytes(b'corrupt')
            raise RuntimeError('injected corruption')
        with self.assertRaises(RuntimeError):
            self.run_install(after_write=corrupt_then_fail)
        result = tx.read_json(self.root/'run/FINAL_STATE.json')
        self.assertEqual(result['status'], 'FAILED')
        self.assertEqual(result['rollback'][0]['outcome'], 'RESTORE_FAILED')
        self.assertEqual(self.target.read_bytes(), self.new)

    def test_mobile_allowlist_and_nonmobile_external_backup(self):
        with patch.object(controlled,'APP',self.root/'app'), \
             patch.object(controlled,'CORE',self.root/'core'), \
             patch.object(controlled,'QUEUE',self.root/'queue'):
            mobile = [self.root/'app'/x for x in (
                'iald-app/www/iald.js', 'iald-app/android/app/src/main/assets/public/iald.js',
                'iald-app/ios/App/App/public/iald.js')]
            p = {'files':[{'destination':str(x),'backup_directory':str(self.root/'mobile_backups')} for x in mobile]}
            self.assertEqual(controlled.allowed_targets(p), mobile)
            for name in ('app/iald.js', 'iald_activity_operations.py', 'iald_jev_control.py'):
                with self.assertRaises(tx.DeploymentError):
                    controlled.allowed_targets({'files':[{'destination':str(self.root/'app'/name),
                        'backup_directory':str(self.root/'mobile_backups')}]})
            with self.assertRaises(tx.DeploymentError):
                controlled.allowed_targets({'files':[{'destination':str(self.root/'app/iald-app/www/other.js')}]})

    def test_external_backup_traversal_refuses_before_changes(self):
        self.payload['files'][0]['backup_directory'] = str(self.root/'mobile_backups'/'..'/'outside')
        self.write_plan()
        with self.assertRaises(tx.DeploymentError):
            self.run_install()
        self.assertEqual(self.target.read_bytes(), self.old)
        self.assertFalse((self.root/'outside').exists())

    def test_changed_backup_route_requires_new_review_pin(self):
        payload = json.loads(self.plan.read_bytes())
        payload['files'][0]['backup_directory'] = str(self.root/'mobile_backups'/'changed')
        self.plan.write_text(json.dumps(payload),encoding='utf-8')
        with self.assertRaises(tx.DeploymentError):
            self.run_install()
        self.assertEqual(self.target.read_bytes(), self.old)

if __name__ == '__main__':
    reused = ['test_external_backup_is_not_bundled','test_backup_escape_rejected',
              'test_invalid_python_rejected','test_failed_write_restores_exact_bytes',
              'test_concurrent_edit_not_overwritten_by_rollback','test_stale_baseline_refuses_before_backup',
              'test_new_file_rollback']
    own = [name for name in DeltaTests.__dict__ if name.startswith('test_')]
    suite = unittest.TestSuite([MobileBackupTests(name) for name in reused] + [DeltaTests(name) for name in own])
    log = io.StringIO(); start = time.monotonic()
    result = unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
    sys.path.insert(0,str(HERE.parent));import mission_io as mio
    with (HERE/'TEST_LOG_R1.txt').open('xb') as out:out.write(log.getvalue().encode('utf-8'))
    data = {'status':'PASS' if result.wasSuccessful() else 'FAIL','tests_run':result.testsRun,
            'reused_with_external_backup':len(reused),'independent_cases':len(own),
            'failures':len(result.failures),'errors':len(result.errors),'seconds':time.monotonic()-start,
            'log':mio.pin(HERE/'TEST_LOG_R1.txt'),'source':mio.pin(__file__),
            'production_writes':False,'providers_called':0}
    mio.save(HERE/'TEST_RESULT_R1.json',data)
    print(json.dumps(data,ensure_ascii=False))
    if not result.wasSuccessful():
        print(log.getvalue())
        raise SystemExit(1)
