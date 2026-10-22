import sys, json, unittest, os
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.dont_write_bytecode=True
sys.path.insert(0,str(BASE))
import iald_orchestrator
iald_orchestrator.__path__.insert(0,str(ROOT/'candidate/iald_orchestrator'))
from iald_orchestrator import canonical_memory as m
m.BASE=BASE;m.ACTIVE=BASE/'state/canonical_memory/ACTIVE.json';m.RELEASES=BASE/'state/canonical_memory/releases';m.CATALOG=BASE/'project_fisica/MANIFESTO_LOCAL.json'
assert str(ROOT/'candidate') in m.__file__
import types
reg=types.ModuleType('historical_pin_tests');reg.__dict__['WORK']=ROOT
exec(compile((ROOT/'test_historical_pin.py').read_bytes(),str(ROOT/'test_historical_pin.py'),'exec'),reg.__dict__)
suite=unittest.defaultTestLoader.loadTestsFromModule(reg)
for name in ('test_canonical_memory','test_nos_jev_integration','test_request_controls'):
 suite.addTests(unittest.defaultTestLoader.loadTestsFromName(name))
r=unittest.TextTestRunner(verbosity=1).run(suite)
print(json.dumps({'tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'success':r.wasSuccessful(),'providers':'ALL_MOCKED','candidate_only':True}))
raise SystemExit(0 if r.wasSuccessful() else 1)
