"""Record native tests and immutable source pins; no production writes."""
from pathlib import Path
import contextlib, datetime, hashlib, importlib, io, json, os, sys, time, unittest

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent
sys.path.insert(0,str(ROOT))

def pin(path):
    p=Path(path)
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def save(path,value):
    raw=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8') if not isinstance(value,str) else value.encode('utf-8')
    temp=path.with_suffix('.tmp')
    with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert temp.read_bytes()==raw
    os.rename(temp,path)

paths=list((WORK/'staging/native').glob('*.py'))+[WORK/'staging/native/SERVER_HOOKS_R1.txt']
paths+=list((ROOT/'app_snapshot_r1').glob('*.py'))
paths += [ROOT/n for n in ['test_native_activity.py','test_server_hooks.py','run_final.py','APP_SNAPSHOT_PROVENANCE_R1.json']]
pins=[pin(p) for p in paths]
suite=unittest.TestSuite();names=[]
for name in ['test_native_activity','test_server_hooks']:
    module=importlib.import_module(name)
    loaded=unittest.defaultTestLoader.loadTestsFromModule(module)
    for group in loaded:names.extend(t.id() for t in group)
    suite.addTests(loaded)
log=io.StringIO();started=time.perf_counter()
with contextlib.redirect_stdout(log):
    result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
seconds=time.perf_counter()-started
save(ROOT/'NATIVE_TEST_LOG_R1.txt',log.getvalue())
baseline=json.loads((WORK/'NATIVE_BASELINE_R1.json').read_text(encoding='utf-8'))
baseline_ok=all(pin(p['path'])==p for p in baseline['sources'])
core=json.loads((WORK/'CORE_DELIVERY_R1.json').read_text(encoding='utf-8'))
core_ok=all(pin(p['path'])==p for p in core['implementation'])
stable=all(pin(p['path'])==p for p in pins)
report={'status':'PASS' if result.wasSuccessful() and baseline_ok and core_ok and stable else 'FAIL',
    'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tests_run':result.testsRun,
    'failures':len(result.failures),'errors':len(result.errors),'seconds':seconds,'test_ids':names,
    'pins':pins+[pin(ROOT/'NATIVE_TEST_LOG_R1.txt')], 'production_unchanged':baseline_ok,
    'accepted_core_unchanged':core_ok,'source_bytes_stable_during_tests':stable,
    'scope':'Real private MemoryStore, real ActivityRuntime, unchanged holographic algorithm, actual App Binding and extracted native server functions from immutable A snapshot; science readers and read/count HTTP endpoints simulated.',
    'provider_calls':0,'runtime_probes':0,'services_restarted':0,'installed':False,
    'limits':'No real model tokenizer or live user/phone test; final native counter ordering/failure/overflow verified with simulated count responses. Joint integration V still required.'}
save(ROOT/'NATIVE_TEST_RESULT_R1.json',report)
print(json.dumps({k:report[k] for k in ['status','tests_run','failures','errors','seconds','production_unchanged','accepted_core_unchanged']}))
print(json.dumps(pin(ROOT/'NATIVE_TEST_RESULT_R1.json')))
raise SystemExit(0 if report['status']=='PASS' else 1)
