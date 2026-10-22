import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

spec=importlib.util.spec_from_file_location('deadlines',Path(__file__).with_name('iald_deadlines.py'))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class DeadlineTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'deadlines.json'
        self.now=datetime(2026,9,22,13,tzinfo=timezone.utc)
    def write(self, expires):
        self.path.write_text(json.dumps({'items':{'anthropic_key':{'expires_at':expires,'secret':'DO_NOT_EXPOSE'}}}))
    def test_thresholds_and_expiry(self):
        for days,level in [(60,'ok'),(30,'attention'),(14,'warning'),(7,'warning'),(3,'critical'),(1,'critical'),(0,'expired'),(-1,'expired')]:
            with self.subTest(days=days):
                self.write((self.now+timedelta(days=days)).isoformat())
                result=module.snapshot(self.path,self.now)
                self.assertEqual(result['items'][0]['level'],level)
                self.assertNotIn('DO_NOT_EXPOSE',json.dumps(result))
    def test_timezone_equivalence(self):
        self.write('2026-09-22T10:00:00-03:00')
        self.assertEqual(module.snapshot(self.path,self.now)['items'][0]['level'],'expired')
    def test_invalid_unknown_and_missing_fail_visible(self):
        self.assertTrue(module.snapshot(self.path,self.now)['error'])
        for date in ['2026-09-22','invalid',123,None]:
            self.write(date)
            self.assertEqual(module.snapshot(self.path,self.now)['items'][0]['level'],'unknown')
    def test_renewal_read_without_restart(self):
        self.write(self.now.isoformat());self.assertEqual(module.snapshot(self.path,self.now)['items'][0]['level'],'expired')
        self.write((self.now+timedelta(days=60)).isoformat());self.assertEqual(module.snapshot(self.path,self.now)['items'][0]['level'],'ok')

if __name__=='__main__':unittest.main()
