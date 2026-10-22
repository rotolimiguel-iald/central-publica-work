"""Exercise the real alert endpoint body without importing the production server."""
import ast
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parent))
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')

class AccessTests(unittest.TestCase):
    def setUp(self):
        source=ast.parse((ROOT/'iald_web_server.py').read_text(encoding='utf-8'))
        fn=next(n for n in source.body if isinstance(n,ast.FunctionDef) and n.name=='api_alertas')
        fn.decorator_list=[]
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.ns={'session':{'username':'test'},'load_users_estrito':lambda:{'test':{'admin':False}},
                 'UsuariosIlegiveis':RuntimeError,'SALDO_OPENAI':types.SimpleNamespace(estado=lambda:{'nivel':'ok'}),
                 'jsonify':lambda x:x,'os':os,'SERVE_DIR':self.tmp.name}
        exec(compile(ast.Module(body=[fn],type_ignores=[]),'<real-alert-endpoint>','exec'),self.ns)
    def test_standard_user_has_no_operational_metadata(self):
        self.assertEqual(self.ns['api_alertas'](),{'alertas':[]})
    def test_operator_gets_dates_never_arbitrary_json_values(self):
        self.ns['load_users_estrito']=lambda:{'test':{'admin':True}}
        Path(self.tmp.name,'iald_deadlines.json').write_text(json.dumps({'items':{'anthropic_key':{'expires_at':'2026-11-29T10:00:00-03:00','credential':'MUST_NOT_LEAK'}}}))
        result=self.ns['api_alertas']()
        self.assertIn('prazos',result)
        self.assertNotIn('MUST_NOT_LEAK',json.dumps(result))
    def test_unreadable_registry_fails_closed(self):
        def bad():raise RuntimeError()
        self.ns['load_users_estrito']=bad
        self.assertEqual(self.ns['api_alertas']()[1],503)

if __name__=='__main__':unittest.main()
