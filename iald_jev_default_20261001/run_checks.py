"""Offline suite; the installed PPTX fallback is explicit, no provider calls."""
from pathlib import Path
import json,sys,unittest,hashlib
W=Path(__file__).parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(W/'stage'),str(ROOT)]
sys.path.append(str(ROOT/'.iald_runtime/task_dependencies'))
for file in (W/'stage').glob('*.py'):
    compile(file.read_bytes(),str(file),'exec')
names=['test_artifacts','test_sandbox','test_auto','test_routes','test_evaluation','test_tasks','test_task_integration','test_task_routes']
suite=unittest.TestSuite()
names += ['test_public_budgets','test_budget_remaining']
for name in names:
    if (W/(name+'.py')).exists():suite.addTests(unittest.defaultTestLoader.loadTestsFromName(name))
suite.addTests(unittest.defaultTestLoader.discover(str(W/'tests'),pattern='test_*.py'))
result=unittest.TextTestRunner(verbosity=1).run(suite)
record={'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'passed':result.wasSuccessful(),'provider_calls':'simulated','files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (W/'stage').glob('*.py')}}
(W/'checks.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
sys.exit(0 if result.wasSuccessful() else 1)
