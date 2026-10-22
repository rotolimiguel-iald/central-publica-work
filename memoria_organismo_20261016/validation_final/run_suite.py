"""Run unchanged copied test assertions with the final integration tree."""
from pathlib import Path
import contextlib, hashlib, importlib, io, json, os, sys, time, unittest
ROOT=Path(__file__).resolve().parent
name=sys.argv[1]
groups={
 'core':('tests_core_r2',['test_activity','test_mission_regression','test_projection']),
 'native':('tests_native',['test_native_activity','test_server_hooks']),
 'queue':('tests_queue',['test_queue_activity_r3']),
 'app':('tests_app',['test_activity_app']),
 'jev':('tests_jev',['test_long_admission']),
}
folder,names=groups[name]
sys.path.insert(0,str(ROOT/folder))
suite=unittest.TestSuite()
for module in names:suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(importlib.import_module(module)))
if name=='queue':
    cls=importlib.import_module('test_legacy_migration_r2').LegacyMigrationTests
    suite.addTests(cls(n) for n in sorted(n for n in dir(cls) if n.startswith('migration_')))
def ids(s):
    for x in s:
        if isinstance(x,unittest.TestSuite):yield from ids(x)
        else:yield x.id()
test_ids=list(ids(suite));start=time.perf_counter();log=io.StringIO()
with contextlib.redirect_stdout(log):result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
elapsed=time.perf_counter()-start
target=ROOT/'results';target.mkdir(exist_ok=True)
with (target/(name+'_log.txt')).open('x',encoding='utf8') as f:f.write(log.getvalue())
report={'status':'PASS' if result.wasSuccessful() else 'FAIL','tests_run':result.testsRun,'seconds':elapsed,'failures':len(result.failures),'errors':len(result.errors),'test_ids':test_ids}
with (target/(name+'_result.json')).open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
print(json.dumps(report))
if not result.wasSuccessful():print(log.getvalue()[-22000:])
raise SystemExit(0 if result.wasSuccessful() else 1)
