"""Independent deployment controls: private files, SQLite and simulated processes only."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
import sqlite3
import unittest
import maintenance as m
import legacy_app_checks as legacy
import controlled as c
import transaction as tx
import test_transaction as original


class IndependentTransaction(unittest.TestCase):
    setUp = original.TransactionTests.setUp
    write_plan = original.TransactionTests.write_plan
    run_install = original.TransactionTests.run_install

    def test_two_file_failure_restores_both_in_reverse_order(self):
        target2 = self.dest/'second.py'; target2.write_bytes(b'y = 1\r\n')
        source2 = self.stage/'second.py'; source2.write_bytes(b'y = 2\n')
        self.payload['files'].append({'source':str(source2), 'destination':str(target2),
            'baseline':tx.sha(target2.read_bytes()), 'sha256':tx.sha(source2.read_bytes())})
        self.write_plan()
        def fail(index, target):
            if index == 1: raise RuntimeError('second installed')
        with self.assertRaises(RuntimeError):
            tx.install(self.plan,self.review,work_root=self.root,
                allowed_destinations=[self.target,target2],assert_quiesced=lambda:None,
                evidence_dir=self.root/'run',after_write=fail)
        self.assertEqual(self.target.read_bytes(),self.old)
        self.assertEqual(target2.read_bytes(),b'y = 1\r\n')
        result=tx.read_json(self.root/'run/FINAL_STATE.json')
        self.assertEqual([x['destination'] for x in result['rollback']],[str(target2),str(self.target)])

    def test_tampered_backup_never_restored_as_original(self):
        def corrupt(*_):
            next(self.dest.glob('*.bak_*')).write_bytes(b'corrupt')
            raise RuntimeError('fail after corrupt backup')
        with self.assertRaises(RuntimeError):self.run_install(after_write=corrupt)
        result=tx.read_json(self.root/'run/FINAL_STATE.json')
        self.assertEqual(result['status'],'FAILED')
        self.assertEqual(result['rollback'][0]['outcome'],'RESTORE_FAILED')
        self.assertEqual(self.target.read_bytes(),self.new)

    def test_lost_guard_refuses_unsafe_rollback_and_reports_partial(self):
        state={'frozen':True}
        def guard():
            if not state['frozen']:raise tx.DeploymentError('lost frozen window')
        def reopen(*_):state['frozen']=False
        with self.assertRaises(tx.DeploymentError):self.run_install(guard=guard,after_write=reopen)
        result=tx.read_json(self.root/'run/FINAL_STATE.json')
        self.assertEqual(result['status'],'FAILED')
        self.assertEqual(result['rollback'][0]['outcome'],'RESTORE_FAILED')
        self.assertEqual(self.target.read_bytes(),self.new)

    def test_changed_target_at_final_prewrite_is_preserved(self):
        calls=[]
        def guard():
            calls.append(1)
            if len(calls)==3:self.target.write_bytes(b'other = 3\n')
        with self.assertRaises(tx.DeploymentError):self.run_install(guard=guard)
        self.assertEqual(self.target.read_bytes(),b'other = 3\n')
        result=tx.read_json(self.root/'run/FINAL_STATE.json')
        self.assertEqual(result['rollback'],[])

    def test_code_allowlist_refuses_state_database(self):
        with patch.object(c,'APP',self.root):
            with self.assertRaises(tx.DeploymentError):
                c.allowed_targets({'files':[{'destination':str(self.root/'state.sqlite3')}]})

    def test_quiet_checks_real_private_ledgers_without_mutation(self):
        jobs=self.root/'.iald_runtime/chat_jobs/jobs.sqlite3'; jobs.parent.mkdir(parents=True)
        wallet=self.root/'.iald_runtime/monthly_wallet/wallet.sqlite3'; wallet.parent.mkdir(parents=True)
        db=sqlite3.connect(jobs)
        db.execute('CREATE TABLE jobs(status TEXT)'); db.execute("INSERT INTO jobs VALUES ('queued')")
        db.commit(); db.close()
        with patch.object(legacy,'ROOT',self.root):
            raw=jobs.read_bytes()
            with self.assertRaises(RuntimeError):legacy.quiet()
            self.assertEqual(jobs.read_bytes(),raw)
            db=sqlite3.connect(jobs); db.execute('DELETE FROM jobs'); db.commit(); db.close()
            db=sqlite3.connect(wallet)
            db.execute('CREATE TABLE tasks(status TEXT)');db.execute('CREATE TABLE calls(status TEXT)')
            db.execute("INSERT INTO calls VALUES ('pending')");db.commit();db.close()
            raw=wallet.read_bytes()
            with self.assertRaises(RuntimeError):legacy.quiet()
            self.assertEqual(wallet.read_bytes(),raw)


class IndependentMaintenance(unittest.TestCase):
    def setUp(self):
        self.parent=Mock();self.child=Mock()
        self.parent.pid=1001;self.child.pid=1002
        self.parent.create_time.return_value=123.0
        self.parent.status.return_value=m.psutil.STATUS_STOPPED
        self.child.status.return_value=m.psutil.STATUS_STOPPED
        self.parent.cmdline.return_value=['powershell.exe','C:/IALD/projetos_pyhton/IALD/start_iald_web.ps1']
        self.child.parent.return_value=self.parent
        self.patchers=[patch.object(m,'_web_processes',return_value=[self.child]),
            patch.object(m,'_listeners',return_value=[SimpleNamespace(pid=1002)]),
            patch.object(m,'_active',None)]
        for p in self.patchers:p.start();self.addCleanup(p.stop)

    def test_nonquiet_child_is_not_terminated_and_both_resume(self):
        def quiet():
            self.parent.suspend.assert_called_once();self.child.suspend.assert_called_once()
            raise RuntimeError('work remains')
        with self.assertRaises(RuntimeError):
            with m.stopped_web(quiet):self.fail('must refuse')
        self.child.terminate.assert_not_called()
        self.child.resume.assert_called_once();self.parent.resume.assert_called_once()
        self.assertIsNone(m._active)

    def test_install_failure_resumes_supervisor_after_verified_child_stop(self):
        with patch.object(m,'assert_quiesced') as guard:
            with self.assertRaises(RuntimeError):
                with m.stopped_web(lambda:None) as identity:
                    guard.assert_called_once()
                    self.assertEqual(identity['old_web_pid'],1002)
                    raise RuntimeError('install failed')
        self.child.terminate.assert_called_once();self.child.wait.assert_called_once()
        self.child.resume.assert_not_called();self.parent.resume.assert_called_once()
        self.assertIsNone(m._active)


if __name__=='__main__':unittest.main(verbosity=2)
