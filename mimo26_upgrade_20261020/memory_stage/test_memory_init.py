import sys, tempfile, sqlite3, unittest, json
from contextlib import closing
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'lib'))
from iald_memory import MemoryStore, IntegrityError
class Regression(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=Path(__file__).parent);self.addCleanup(self.tmp.cleanup)
  root=Path(self.tmp.name);self.s=MemoryStore(root/'state',snapshot_archive_dir=root/'archive')
  self.args=dict(objective='Synthetic objective',scope={'house':'IALD','principal':'synthetic'},actor={'id':'test','kind':'agent'})
 def test_init_replay_and_verify(self):
  a=self.s.ensure_context('test',**self.args);b=self.s.ensure_context('test',**self.args)
  self.assertEqual(a['objective_sha256'],b['objective_sha256']);self.assertTrue(b['receipt']['replayed'])
  self.s.verify('test',self.args['scope'])
 def test_sqlite_failure_is_named_and_rolled_back(self):
  original=self.s._snapshot_if_due
  def fail(conn):conn.execute('SELECT * FROM synthetic_missing_table')
  self.s._snapshot_if_due=fail
  with self.assertRaises(IntegrityError) as raised:self.s.ensure_context('test',**self.args)
  self.assertEqual(str(raised.exception),'Context transaction failed [SQLITE_ERROR]')
  self.assertIsInstance(raised.exception.__cause__,sqlite3.Error)
  with closing(sqlite3.connect(self.s.db_path)) as c:self.assertEqual(c.execute('SELECT count(*) FROM contexts').fetchone()[0],0)
  self.s._snapshot_if_due=original;self.s.ensure_context('test',**self.args)
 def test_immutability_guard_preserved(self):
  self.s.ensure_context('test',**self.args)
  with closing(sqlite3.connect(self.s.db_path)) as c:
   with self.assertRaises(sqlite3.IntegrityError):c.execute('DELETE FROM contexts')
 def test_private_message_and_untrusted_errorname_not_exposed(self):
  for name in (None,'PRIVATE_SENTINEL_42'):
   def fail(conn):
    error=sqlite3.OperationalError('PRIVATE_SENTINEL_42')
    if name is not None:error.sqlite_errorname=name
    raise error
   self.s._snapshot_if_due=fail
   with self.assertRaises(IntegrityError) as raised:self.s.ensure_context('test',**self.args)
   self.assertEqual(str(raised.exception),'Context transaction failed [SQLITE_ERROR_UNKNOWN]')
   self.assertNotIn('PRIVATE_SENTINEL_42',str(raised.exception))
if __name__=='__main__':unittest.main(verbosity=2)
