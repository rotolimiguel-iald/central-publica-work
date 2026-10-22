from pathlib import Path
import sys,unittest,json,types
ROOT=Path(__file__).resolve().parent;BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.dont_write_bytecode=True;sys.path.insert(0,str(BASE))
mode=sys.argv[1]
import iald_orchestrator
if mode!='baseline':iald_orchestrator.__path__.insert(0,str(ROOT/'candidate/iald_orchestrator'))
from iald_orchestrator import canonical_memory as m
if mode!='baseline':
 m.BASE=BASE;m.ACTIVE=BASE/'state/canonical_memory/ACTIVE.json';m.RELEASES=BASE/'state/canonical_memory/releases';m.CATALOG=BASE/'project_fisica/MANIFESTO_LOCAL.json'
if mode=='new':
 reg=types.ModuleType('historical_pin_tests');reg.__dict__['WORK']=ROOT
 exec(compile((ROOT/'test_historical_pin.py').read_bytes(),str(ROOT/'test_historical_pin.py'),'exec'),reg.__dict__)
 suite=unittest.defaultTestLoader.loadTestsFromModule(reg)
else:
 suite=unittest.TestSuite()
 for name in ('test_canonical_memory','test_nos_jev_integration','test_request_controls'):suite.addTests(unittest.defaultTestLoader.loadTestsFromName(name))
r=unittest.TextTestRunner(verbosity=1).run(suite)
print(json.dumps({'mode':mode,'tests':r.testsRun,'failures':[x[0].id() for x in r.failures],'errors':[x[0].id() for x in r.errors],'success':r.wasSuccessful(),'providers':'ALL_MOCKED'}))
raise SystemExit(0 if r.wasSuccessful() else 1)
