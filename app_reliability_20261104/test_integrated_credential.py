"""Offline credential integration tests; synthetic values, no server import."""
from pathlib import Path
import ast
import importlib.util
import json
import os
import sys
import tempfile
import types
import unittest
import uuid
from unittest.mock import patch

W=Path(__file__).resolve().parent
sys.path.insert(0,str(W))
from prepare_release import staged_bytes
spec=importlib.util.spec_from_file_location('candidate_credential',W/'credential/iald_openai_credential.py')
loader=importlib.util.module_from_spec(spec);spec.loader.exec_module(loader)
sys.path.insert(0,r'C:\IALD\MEMORIA_IALD\lib')
from iald_memory.guard import path_reason


class CredentialTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='credential-fixture-',dir=W)
        self.path=Path(self.tmp.name)/'test.key'
    def tearDown(self):self.tmp.cleanup()
    def test_missing(self):self.assertIsNone(loader.load(self.path))
    def test_invalid(self):
        self.path.write_bytes(b'invalid')
        self.assertEqual('',loader.load(self.path))
    def test_valid(self):
        sample=b'sk-'+b'X'*30
        self.path.write_bytes(sample)
        self.assertEqual(sample.decode(),loader.load(self.path))
    def test_oversize(self):
        self.path.write_bytes(b'sk-'+b'X'*6000)
        self.assertEqual('',loader.load(self.path))
    def test_directory(self):
        self.assertEqual('',loader.load(Path(self.tmp.name)))
    def test_secret_paths_are_blocked(self):
        self.assertTrue(path_reason(loader.KEY_PATH))
        self.assertTrue(path_reason(loader.KEY_PATH.with_name('.openai_enrollment_test.key')))
    def test_integrated_precedence(self):
        raw=staged_bytes()['iald_web_server.py']
        tree=ast.parse(raw)
        function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_segredo')
        ns={'os':os,'__file__':str(Path(self.tmp.name)/'fixture.py')}
        exec(compile(ast.Module(body=[function],type_ignores=[]),'<credential-fixture>','exec'),ns)
        module=types.ModuleType('iald_openai_credential')
        with patch.dict(sys.modules,{'iald_openai_credential':module}),patch.dict(os.environ,{'IALD_OPENAI_API_KEY':'legacy','OTHER_KEY':'unrelated'}):
            module.load=lambda:'dedicated'
            self.assertEqual('dedicated',ns['_segredo']('IALD_OPENAI_API_KEY'))
            self.assertEqual('unrelated',ns['_segredo']('OTHER_KEY'))
            module.load=lambda:None
            self.assertEqual('legacy',ns['_segredo']('IALD_OPENAI_API_KEY'))
            module.load=lambda:''
            self.assertEqual('',ns['_segredo']('IALD_OPENAI_API_KEY'))


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CredentialTests))
    payload={'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
             'status':'PASS' if result.wasSuccessful() else 'FAIL','network_calls':0,'real_credentials_read':False}
    with (W/'CREDENTIAL_INTEGRATION_TESTS_R2.json').open('x',encoding='utf8') as handle:json.dump(payload,handle,indent=2)
    raise SystemExit(0 if result.wasSuccessful() else 1)
