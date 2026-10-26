"""Focused consumer checks against the actual approved DATA_READY schema."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import copy, runpy, unittest

C=Path(__file__).resolve().parent
m=runpy.run_path(str(C/'media_v401_worker.py'))
g=m['main'].__globals__
options=SimpleNamespace(data_ready=C/'DATA_READY.json')
original_load=m['load']

class SchemaTests(unittest.TestCase):
    def setUp(self):
        self.config=patch.dict(g,options=options);self.config.start()
    def tearDown(self): self.config.stop()
    def test_actual_ready_and_parent_pins(self):
        ready,frozen=m['readiness']()
        self.assertEqual(ready['status'],'DATA_READY')
        self.assertEqual(ready['source'],'v401')
        self.assertTrue(any(Path(x.get('path',x.get('file'))).name=='PARENT_NUMERIC_REVIEW.json' for x in frozen))
    def test_wrong_parent_ready_hash_rejected(self):
        def load(p):
            d=copy.deepcopy(original_load(p))
            if Path(p).name=='PARENT_NUMERIC_REVIEW.json':d['data_ready_sha256']='0'*64
            return d
        with patch.dict(g,load=load):
            with self.assertRaisesRegex(AssertionError,'parent numeric review pins another'):
                m['readiness']()
    def test_unexpected_numeric_difference_rejected(self):
        def load(p):
            d=copy.deepcopy(original_load(p))
            if Path(p).name=='NUMERIC_COMPARISON.json':d['unexpected_differences']=[{'synthetic':'not allowed'}]
            return d
        with patch.dict(g,load=load):
            with self.assertRaisesRegex(AssertionError,'unauthorized numeric difference'):
                m['readiness']()
    def test_unapproved_parent_rejected(self):
        def load(p):
            d=copy.deepcopy(original_load(p))
            if Path(p).name=='PARENT_NUMERIC_REVIEW.json':d['status']='PENDING'
            return d
        with patch.dict(g,load=load):
            with self.assertRaises(AssertionError):m['readiness']()

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SchemaTests))
    report={'status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,
        'failures':len(result.failures),'errors':len(result.errors),'worker':m['pin'](C/'media_v401_worker.py'),
        'test':m['pin'](Path(__file__)),'data_ready':m['pin'](options.data_ready),
        'parent_numeric_review':m['pin'](C/'PARENT_NUMERIC_REVIEW.json'),
        'scope':'Consumer contract and pin guards only; no repeated scientific comparison, renderer, TTS, encode or media validation.'}
    m['save_original'](C/'MEDIA_SCHEMA_FIX_TESTS.json',report)
    raise SystemExit(0 if result.wasSuccessful() else 1)
