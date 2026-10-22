import copy,json,tempfile,unittest
from pathlib import Path
import prepare_memories as p
import atomic_append as a
class PrepareTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=p.HERE,prefix='synthetic_test_');self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        payloads=dict(deployment=dict(status='INSTALLED_RESTART_REQUIRED'),live=dict(status='PASS_NO_MODEL_CALLS'),mobile=dict(status='FINAL_SNAPSHOT_WITH_PENDING_CHANNELS',web='verified',ios_internal='PENDING_CLOUD',ios_external='PENDING_REVIEW',android='LOCAL_SIGNED_ONLY',google_play='NOT_PUBLISHED',physical_installation_verified=False,pending=['iOS groups not yet available']))
        self.config=dict(final_snapshot=True,receipts={})
        for role,value in payloads.items():
            f=self.root/(role+'.json');raw=json.dumps(value).encode();f.write_bytes(raw);self.config['receipts'][role]=dict(path=str(f),sha256=p.sha(raw))
    def test_missing_receipt_refused(self):
        del self.config['receipts']['live']
        with self.assertRaisesRegex(ValueError,'missing final receipt role'):p.validate(self.config)
    def test_absent_file_refused(self):
        Path(self.config['receipts']['mobile']['path']).unlink()
        with self.assertRaisesRegex(ValueError,'missing final receipt'):p.validate(self.config)
    def test_broken_pin_refused(self):
        self.config['receipts']['deployment']['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'pin mismatch'):p.validate(self.config)
    def test_not_final_refused(self):
        self.config['final_snapshot']=False
        with self.assertRaisesRegex(ValueError,'FINAL'):p.validate(self.config)
    def test_pending_channels_and_physical_preserved(self):
        rec,pins,matrix=p.validate(self.config);text=p.render(rec,pins,matrix).decode()
        self.assertIn('PENDING_CLOUD',text);self.assertIn('NOT_PUBLISHED',text);self.assertIn('não verificada',text);self.assertIn('experimental',text);self.assertIn('deflate sem perdas',text)
        self.assertNotIn('todos os canais atualizados.',text)
    def test_no_apply_default(self):
        path=self.root/'synthetic_memory.txt';path.write_bytes(b'CRLF\r\n')
        with self.assertRaisesRegex(RuntimeError,'PREPARE_ONLY'):a.append_reviewed(path,b'append',p.sha(path.read_bytes()),p.sha(path.read_bytes()+b'append'))
        self.assertEqual(path.read_bytes(),b'CRLF\r\n');self.assertEqual(list(self.root.glob('*.bak_*')),[])
    def test_backup_bytes_atomic_append_synthetic_only(self):
        path=self.root/'synthetic_memory.txt';before=b'CRLF\r\nraw\xff\r\n';path.write_bytes(before);chunk='ação\n'.encode()
        receipt=a.append_reviewed(path,chunk,p.sha(before),p.sha(before+chunk),apply=True)
        self.assertEqual(Path(receipt['backup']).read_bytes(),before);self.assertEqual(path.read_bytes(),before+chunk)
    def test_stale_target_refused_without_backup(self):
        path=self.root/'synthetic_memory.txt';path.write_bytes(b'changed')
        with self.assertRaisesRegex(RuntimeError,'target changed'):a.append_reviewed(path,b'x','0'*64,'0'*64,apply=True)
        self.assertFalse(list(self.root.glob('*.bak_*')))
if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PrepareTests))
    report=dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,live_memory_files_written=0,scope='Synthetic receipts and byte/CRLF fixtures under memory_prepare only; no canonical surface modified.',failures=[str(t)+s for t,s in result.failures+result.errors])
    (p.HERE/'TEST_RESULTS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
