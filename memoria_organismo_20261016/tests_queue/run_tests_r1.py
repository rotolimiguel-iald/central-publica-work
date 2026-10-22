import hashlib,io,json,os,time,unittest,uuid
from pathlib import Path
from test_queue_activity_r1 import QueueActivityTests,W
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
def save(p,data):
    if not isinstance(data,bytes):data=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    os.rename(t,p)
baseline=json.loads((W/'tests_queue/QUEUE_BASELINE_R1.json').read_bytes())
for p in baseline['core']:assert pin(Path(p['path']))==p
sources=[p for p in (W/'staging/queue').rglob('*.py')]+list((W/'staging/sessions').glob('*.py'))+list((W/'staging/bench_wrapper').glob('*.py'))
before=[pin(p) for p in sources]
suite=unittest.defaultTestLoader.loadTestsFromTestCase(QueueActivityTests)
buffer=io.StringIO();start=time.monotonic()
result=unittest.TextTestRunner(stream=buffer,verbosity=2).run(suite)
elapsed=time.monotonic()-start
log=W/'tests_queue/QUEUE_TEST_LOG_R1.txt';save(log,buffer.getvalue().encode())
assert before==[pin(p) for p in sources]
for item in baseline['files']:assert pin(Path(item['source']['path']))==item['source']
for p in baseline['core']:assert pin(Path(p['path']))==p
report={'verdict':'PASS' if result.wasSuccessful() else 'FAIL','tests_run':result.testsRun,
    'failures':len(result.failures),'errors':len(result.errors),'seconds':elapsed,'sources':before,
    'log':pin(log),'test_source':pin(W/'tests_queue/test_queue_activity_r1.py'),'runner':pin(Path(__file__)),
    'baseline':pin(W/'tests_queue/QUEUE_BASELINE_R1.json'),'source_bytes_unchanged':True,
    'production_baseline_unchanged':True,'core_frozen_unchanged':True,
    'provider_calls':0,'real_bench_http_calls':0,'scope':'Real queue/coordination/ACOM/Activity/SQLite in private roots; model/canonical packet/shadow and HTTP are inert fixtures; CLI runs actual source in fresh process.'}
path=W/'tests_queue/QUEUE_TEST_RESULT_R1.json';save(path,report)
print(json.dumps({'result':pin(path),'verdict':report['verdict'],'tests_run':result.testsRun,'seconds':elapsed},ensure_ascii=False))
if not result.wasSuccessful():print(buffer.getvalue()[-16000:]);raise SystemExit(1)
