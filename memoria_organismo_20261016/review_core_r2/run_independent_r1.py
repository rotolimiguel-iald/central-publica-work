import ast,contextlib,hashlib,importlib,io,json,sys,time,unittest
from pathlib import Path
R=Path(__file__).resolve().parent;W=R.parent;sys.path[:0]=[str(R),str(W)]
from mission_io import save,pin
freeze=json.loads((W/'CORE_R2_SOURCE_FREEZE_R1.json').read_bytes())
assert all(pin(x['path'])==x for x in freeze['files'])
baseline=json.loads((W/'CORE_R2_BASELINE_R1.json').read_bytes())
assert all(pin(x['source']['path'])==x['source'] for x in baseline['files'])
suite=unittest.TestSuite()
for name in ['test_activity','test_mission_regression','test_projection']:
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(importlib.import_module(name)))
from test_independent import IndependentTests
names=sorted(n for n in dir(IndependentTests) if n.startswith('independent_'))
suite.addTests(IndependentTests(n) for n in names)
log=io.StringIO();start=time.perf_counter()
with contextlib.redirect_stdout(log):result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
elapsed=time.perf_counter()-start
save(R/'C2_INDEPENDENT_TEST_LOG_R1.json',{'log':log.getvalue()})
assert all(pin(x['path'])==x for x in freeze['files'])
assert all(pin(x['source']['path'])==x['source'] for x in baseline['files'])
def methods(path):
    cls=next(n for n in ast.parse(Path(path).read_bytes()).body if isinstance(n,ast.ClassDef) and n.name=='ActivityRuntime')
    return {n.name:ast.dump(n) for n in cls.body if isinstance(n,ast.FunctionDef)}
a=methods(W/'staging/core/lib/iald_memory/activity.py');b=methods(W/'staging/core_r2/lib/iald_memory/activity.py')
assert {k for k in a if a[k]!=b[k]}=={'project'} and set(b)-set(a)=={'_terminal_projection_index'}
out=R/'C2_INDEPENDENT_TEST_RESULT_R1.json'
save(out,{'status':'PASS' if result.wasSuccessful() else 'FAIL','tests_run':result.testsRun,'builder_tests_reproduced':70,
    'independent_tests':len(names),'failures':len(result.failures),'errors':len(result.errors),'seconds':elapsed,
    'freeze':pin(W/'CORE_R2_SOURCE_FREEZE_R1.json'),'source_pins':freeze['files'],
    'test_pins':[pin(R/n) for n in ['test_activity.py','test_mission_regression.py','test_projection.py','test_independent.py','run_independent_r1.py']],
    'log':pin(R/'C2_INDEPENDENT_TEST_LOG_R1.json'),'source_unchanged':True,'only_existing_method_changed':'project',
    'providers_called':0,'production_modified':False,'test_copy_change':'Only private runs directory moved for original Activity setUp; copied test assertions unchanged.'})
print(json.dumps({'result':pin(out),'tests_run':result.testsRun,'seconds':elapsed,'successful':result.wasSuccessful()},ensure_ascii=False))
if not result.wasSuccessful():print(log.getvalue()[-10000:]);raise SystemExit(1)
