"""Freeze validation of the C2 candidate, solely private-store tests."""
from pathlib import Path
import ast
import contextlib
import importlib.util
import io
import json
import sys
import time
import unittest

ROOT=Path(__file__).resolve().parent;WORK=ROOT.parent
sys.path[:0]=[str(ROOT),str(WORK)]
from mission_io import save,pin
freeze=json.loads((WORK/'CORE_R2_SOURCE_FREEZE_R1.json').read_bytes())
assert all(pin(p['path'])==p for p in freeze['files'])
baseline=json.loads((WORK/'CORE_R2_BASELINE_R1.json').read_bytes())
assert all(pin(p['source']['path'])==p['source'] for p in baseline['files'])
old=WORK/'staging/core/lib/iald_memory/activity.py';new=WORK/'staging/core_r2/lib/iald_memory/activity.py'
def methods(path):
    tree=ast.parse(path.read_bytes());node=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='ActivityRuntime')
    return {x.name:ast.dump(x) for x in node.body if isinstance(x,ast.FunctionDef)}
before,after=methods(old),methods(new)
assert {k for k in before if before[k]!=after[k]}=={'project'}
assert set(after)-set(before)=={'_terminal_projection_index'}
unchanged=[]
for row in baseline['files']:
    if Path(row['copy']['path'])!=new:
        assert pin(row['copy']['path'])==row['copy'];unchanged.append(row['copy'])
suite=unittest.TestSuite()
for name in ('test_activity','test_mission_regression','test_projection'):
    module=importlib.import_module(name);suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
log=io.StringIO();started=time.perf_counter()
with contextlib.redirect_stdout(log):result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
elapsed=time.perf_counter()-started
with (ROOT/'CORE_R2_TEST_LOG_R1.txt').open('xb') as f:f.write(log.getvalue().encode('utf8'))
assert all(pin(p['path'])==p for p in freeze['files'])
report={'status':'PASS' if result.wasSuccessful() else 'FAIL','tests_run':result.testsRun,
    'failures':len(result.failures),'errors':len(result.errors),'seconds':elapsed,
    'original_core_unchanged':True,'only_changed_existing_method':'ActivityRuntime.project',
    'new_private_helper':'ActivityRuntime._terminal_projection_index','unchanged_files':unchanged,
    'source_freeze':pin(WORK/'CORE_R2_SOURCE_FREEZE_R1.json'),
    'pins':[pin(ROOT/n) for n in ['test_activity.py','test_mission_regression.py','test_projection.py','run_final.py','CORE_R2_TEST_LOG_R1.txt','REGRESSION_PROVENANCE.json']],
    'providers_called':0,'production_installed':False}
save(ROOT/'CORE_R2_TEST_RESULT_R1.json',report)
print(json.dumps({k:report[k] for k in ('status','tests_run','failures','errors','seconds')}))
if not result.wasSuccessful():print(log.getvalue())
raise SystemExit(0 if result.wasSuccessful() else 1)
