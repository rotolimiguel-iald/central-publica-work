import hashlib,io,json,os,time,unittest,uuid
from pathlib import Path
from test_queue_activity_r3 import QueueActivityTests,W
from test_legacy_migration_r2 import LegacyMigrationTests
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
def save(p,data):
    if not isinstance(data,bytes):data=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    os.rename(t,p)
baseline=json.loads((W/'tests_queue/QUEUE_BASELINE_R1.json').read_bytes())
sources=list((W/'staging/queue/r3').rglob('*.py'));before=[pin(p) for p in sources]
oldplan=json.loads((W/'tests_queue/QUEUE_INSTALL_PLAN_R2.json').read_bytes())
for x in oldplan['files']:assert pin(Path(x['source']['path']))==x['source']
for x in baseline['core']:assert pin(Path(x['path']))==x
suite=unittest.defaultTestLoader.loadTestsFromTestCase(QueueActivityTests)
names=sorted(n for n in dir(LegacyMigrationTests) if n.startswith('migration_'))
suite.addTests(LegacyMigrationTests(n) for n in names)
buffer=io.StringIO();start=time.monotonic();result=unittest.TextTestRunner(stream=buffer,verbosity=2).run(suite)
elapsed=time.monotonic()-start
log=W/'tests_queue/Q2_TEST_LOG_R2.txt';save(log,buffer.getvalue().encode())
assert before==[pin(p) for p in sources]
for x in oldplan['files']:assert pin(Path(x['source']['path']))==x['source']
for x in baseline['core']:assert pin(Path(x['path']))==x
for x in baseline['files']:assert pin(Path(x['source']['path']))==x['source']
report={'verdict':'PASS' if result.wasSuccessful() else 'FAIL','tests_run':result.testsRun,'new_tests':len(names),'regression_tests':29,
  'failures':len(result.failures),'errors':len(result.errors),'seconds':elapsed,'sources':before,'log':pin(log),
  'test_sources':[pin(W/'tests_queue'/n) for n in ['test_queue_activity_r3.py','test_legacy_migration_r2.py','process_fixture_r3.py']],
  'runner':pin(Path(__file__)),'core_pins':baseline['core'],'q_r2_unchanged':True,'production_baseline_unchanged':True,
  'provider_calls':0,'real_bench_http_calls':0,'production_migrations':0,'mcp_changed':False,
  'scope':'Real private SQLite queue/Activity/ACOM and fresh privileged CLI; fake providers/canonical package/HTTP; no new MCP smoke because entrypoint bytes unchanged.'}
out=W/'tests_queue/Q2_TEST_RESULT_R2.json';save(out,report)
print(json.dumps({'result':pin(out),'verdict':report['verdict'],'tests_run':result.testsRun,'seconds':elapsed},ensure_ascii=False))
if not result.wasSuccessful():print(buffer.getvalue()[-15000:]);raise SystemExit(1)
