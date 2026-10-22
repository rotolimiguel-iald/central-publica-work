"""Pin and record the private core tests. No production mutation or providers."""
from pathlib import Path
import contextlib
import datetime
import hashlib
import importlib.util
import io
import json
import os
import time
import unittest

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent

def pin(p):
    p = Path(p)
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

def save(p, raw):
    temp = p.with_suffix('.tmp')
    with temp.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert temp.read_bytes() == raw
    os.rename(temp, p)

suite = unittest.TestSuite()
ids = []
for name in ('test_activity', 'test_mission_regression'):
    spec = importlib.util.spec_from_file_location(name, ROOT/(name+'.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tests = unittest.defaultTestLoader.loadTestsFromModule(module)
    for group in tests:
        ids += [test.id() for test in group]
    suite.addTests(tests)
log = io.StringIO()
start = time.perf_counter()
with contextlib.redirect_stdout(log):
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
seconds = time.perf_counter() - start
save(ROOT/'CORE_TEST_LOG_R1.txt', log.getvalue().encode('utf-8'))
baseline = json.loads((WORK/'CORE_BASELINE.json').read_text(encoding='utf-8'))
baseline_ok = all(pin(row['path']) == row for row in baseline)
paths = list((WORK/'staging/core/lib/iald_memory').glob('*.py'))
paths += [ROOT/'test_activity.py', ROOT/'test_mission_regression.py', ROOT/'run_final.py',
          ROOT/'CORE_TEST_LOG_R1.txt', ROOT/'REGRESSION_PROVENANCE.json', WORK/'ACTIVITY_API_R1.txt']
report = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'PASS' if result.wasSuccessful() and baseline_ok else 'FAIL',
    'tests_run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
    'test_ids': ids, 'seconds': seconds, 'pins': [pin(p) for p in paths],
    'production_baseline_unchanged': baseline_ok, 'providers_called': 0,
    'production_installed': False, 'scope': 'Private stores; 24 new runtime tests plus 28 existing controller tests; external calls simulated.'}
save(ROOT/'CORE_TEST_RESULT_R1.json', (json.dumps(report, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
print(json.dumps({k: report[k] for k in ('status','tests_run','failures','errors','seconds','production_baseline_unchanged')}))
print(json.dumps(pin(ROOT/'CORE_TEST_RESULT_R1.json')))
raise SystemExit(0 if report['status'] == 'PASS' else 1)
