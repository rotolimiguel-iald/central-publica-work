import sys
sys.dont_write_bytecode=True
import hashlib,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import installer as m
ROOT=Path(__file__).resolve().parent
class IsolatedInstall(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT);self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.work=self.root/'work';self.base=self.root/'base'
        (self.work/'envelope').mkdir(parents=True);(self.base/'iald_orchestrator').mkdir(parents=True)
        self.rows=[];self.original={}
        for i in range(5):
            src=self.work/f'source{i}.py';dst=self.base/'iald_orchestrator'/f'module{i}.py';src.write_bytes(f'# candidate {i}\r\n'.encode())
            old=None if i<2 else f'# baseline {i}\r\n'.encode()
            if old is not None:dst.write_bytes(old)
            self.original[dst]=old
            self.rows.append(dict(source=str(src),destination=str(dst),sha256=m.digest(src.read_bytes()),baseline=m.digest(old) if old else None))
        self.plan=self.work/'plan.json';self.plan.write_text(json.dumps({'files':self.rows}));self.planhash=m.digest(self.plan.read_bytes())
        for name,value in [('WORK',self.work),('BASE',self.base)]:
            p=patch.object(m,name,value);p.start();self.addCleanup(p.stop)
    def run_install(self):return m.run(self.plan,self.planhash,self.work/'receipt.json',True)
    def unchanged(self):
        for p,b in self.original.items():self.assertEqual(p.read_bytes() if p.exists() else None,b)
    def test_five_targets_and_exact_backups(self):
        r,code=self.run_install();self.assertEqual(code,0);self.assertEqual(r['status'],'INSTALLED_VERIFIED_NO_RESTART')
        for item in r['pins']:
            self.assertEqual(item['observed_current_sha256'],item['source_sha256'])
            if item['baseline']:self.assertEqual(Path(item['backup']).read_bytes(),self.original[Path(item['destination'])])
        self.assertFalse((self.base/'iald_orchestrator/.reviewed_install.lock').exists())
    def test_all_baselines_validated_before_first_write(self):
        dst=Path(self.rows[-1]['destination']);dst.write_bytes(b'third party');self.original[dst]=b'third party'
        r,code=self.run_install();self.assertNotEqual(code,0);self.assertEqual(r['status'],'FAILED_NO_COMPLETE_INSTALL');self.unchanged()
        self.assertEqual(list(self.base.rglob('*.bak_*')),[])
    def fail_last_replace(self,conflict=False):
        original=m.os.replace;last=Path(self.rows[-1]['destination'])
        def replace(src,dst):
            if Path(dst)==last and '.tmp_' in Path(src).name:
                if conflict:Path(self.rows[0]['destination']).write_bytes(b'NEW_EXTERNAL_WRITE')
                raise OSError('synthetic replace failure')
            return original(src,dst)
        return patch.object(m.os,'replace',side_effect=replace)
    def test_mid_batch_rollback_restores_old_and_retains_new(self):
        with self.fail_last_replace():r,code=self.run_install()
        self.assertNotEqual(code,0);self.assertEqual(r['status'],'FAILED_ROLLED_BACK');self.unchanged()
        retained=[x for x in r['rollback'] if x['status']=='NEW_FILE_RETAINED_TARGET_ABSENT']
        self.assertEqual(len(retained),2);self.assertTrue(all(Path(x['retained']).is_file() for x in retained))
    def test_rollback_never_overwrites_concurrent_writer(self):
        with self.fail_last_replace(True):r,code=self.run_install()
        self.assertNotEqual(code,0);self.assertEqual(r['status'],'FAILED_ROLLBACK_CONFLICT_NEEDS_PARENT')
        self.assertEqual(Path(self.rows[0]['destination']).read_bytes(),b'NEW_EXTERNAL_WRITE')
        self.assertTrue(any(x['error']=='rollback_current_pin_conflict' for x in r['rollback'] if 'error' in x))
    def test_cas_recheck_detects_mid_batch_source_change(self):
        original=m.recheck;last=Path(self.rows[-1]['destination'])
        def recheck(entry):
            if entry['destination']==last:entry['source'].write_bytes(b'changed after plan validation')
            return original(entry)
        with patch.object(m,'recheck',side_effect=recheck):r,code=self.run_install()
        self.assertNotEqual(code,0);self.assertEqual(r['error'],'source_changed_before_commit');self.unchanged()

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(IsolatedInstall))
    report=dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,failures=[(str(t),s) for t,s in result.failures+result.errors],scope='Five synthetic targets under review temp directory; original runtime never targeted',provider_calls=0)
    (ROOT/'TEST_RESULTS.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    raise SystemExit(not result.wasSuccessful())
