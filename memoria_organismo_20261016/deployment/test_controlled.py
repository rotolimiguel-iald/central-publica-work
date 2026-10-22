"""Maintenance guards with a private ledger and simulated process identities."""
from pathlib import Path
from contextlib import contextmanager
import sqlite3
import tempfile
import unittest
from unittest.mock import Mock, patch
import controlled as c


@contextmanager
def database(path, **kwargs):
    db = sqlite3.connect(path, **kwargs)
    try:
        with db:
            yield db
    finally:
        db.close()


class MaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='maintenance_', dir=Path(__file__).parent)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'state').mkdir()
        self.path = self.root/'state/tasks.sqlite3'
        with database(self.path) as db:
            db.execute('CREATE TABLE tasks(id TEXT PRIMARY KEY,status TEXT)')
            db.execute("INSERT INTO tasks VALUES ('queued-1','queued')")
        self.patch = patch.object(c, 'QUEUE', self.root)
        self.patch.start(); self.addCleanup(self.patch.stop)

    def test_queue_freeze_preserves_rows_and_rejects_admission(self):
        with c.paused_queue() as db:
            self.assertTrue(db.in_transaction)
            with database(self.path, timeout=0.01) as another:
                with self.assertRaises(sqlite3.OperationalError):
                    another.execute("INSERT INTO tasks VALUES ('new','queued')")
        with database(self.path) as db:
            self.assertEqual(db.execute('SELECT * FROM tasks').fetchall(), [('queued-1','queued')])
            db.execute("INSERT INTO tasks VALUES ('new','queued')")

    def test_unresolved_running_refused_without_recovery(self):
        with database(self.path) as db:
            db.execute("INSERT INTO tasks VALUES ('unknown-send','running')")
        with self.assertRaises(c.DeploymentError):
            with c.paused_queue(): self.fail('Must not enter')
        with database(self.path) as db:
            self.assertEqual(db.execute("SELECT status FROM tasks WHERE id='unknown-send'").fetchone()[0], 'running')

    def test_existing_drain_lock_refused(self):
        with c.process_lock(self.path, blocking=False) as acquired:
            self.assertTrue(acquired)
            with self.assertRaises(c.DeploymentError):
                with c.paused_queue(): self.fail('Must not enter')

    def test_failure_releases_database_and_drain_locks(self):
        with self.assertRaisesRegex(RuntimeError, 'injected'):
            with c.paused_queue(): raise RuntimeError('injected')
        with c.paused_queue() as db:
            self.assertTrue(db.in_transaction)

    def guard(self, *, created=123.0, status=None, old=False, port=1, transaction=True):
        parent = Mock()
        parent.create_time.return_value = created
        parent.status.return_value = status or c.psutil.STATUS_STOPPED
        probe = Mock(); probe.connect_ex.return_value = port
        socket = Mock(); socket.__enter__ = Mock(return_value=probe); socket.__exit__ = Mock(return_value=False)
        with patch.object(c.psutil,'Process',return_value=parent), patch.object(c.psutil,'pid_exists',return_value=old), patch.object(c.socket,'socket',return_value=socket):
            c.assert_frozen({'supervisor_pid':1,'supervisor_created':123.0,'old_web_pid':2}, Mock(in_transaction=transaction))

    def test_guard_exact_identity_required(self):
        with self.assertRaises(c.DeploymentError): self.guard(created=124.0)

    def test_guard_refuses_resumed_supervisor_or_lost_sql_lock(self):
        with self.assertRaises(c.DeploymentError): self.guard(status=c.psutil.STATUS_RUNNING)
        with self.assertRaises(c.DeploymentError): self.guard(transaction=False)

    def test_guard_refuses_existing_web_or_new_listener(self):
        with self.assertRaises(c.DeploymentError): self.guard(old=True)
        with self.assertRaises(c.DeploymentError): self.guard(port=0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
