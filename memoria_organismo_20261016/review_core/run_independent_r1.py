"""Freeze verified builder bytes; run real tests in private stores with no network."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import time
import uuid

R=Path(__file__).resolve().parent;W=R.parent;F=R/'frozen_r1'
def pin(p):
 p=Path(p);raw=p.read_bytes()
 return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
def save(p,raw):
 assert not p.exists(),str(p)
 p.parent.mkdir(parents=True,exist_ok=True)
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
 with t.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==raw;os.rename(t,p)
def save_json(p,v):save(p,(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))

builder=W/'tests_core'/'CORE_TEST_RESULT_R1.json'
b=json.loads(builder.read_bytes())
assert b['status']=='PASS' and b['tests_run']==52 and not b['failures'] and not b['errors']
assert pin(builder)['sha256']=='02099c2c087801ea91a688fe31636d3a005bd055987dde472bf09579a9e00034'
expected={p['path']:p['sha256'] for p in b['pins']}
for row in json.loads((W/'tests_core'/'REGRESSION_PROVENANCE.json').read_bytes())['pins']:
 expected[row['path']]=row['sha256']
for name,h in expected.items():assert pin(name)['sha256']==h,(name,'changed')
copied=[]
for p in sorted((W/'staging/core/lib/iald_memory').glob('*.py')):
 target=F/p.relative_to(W);raw=p.read_bytes()
 assert hashlib.sha256(raw).hexdigest()==expected[str(p)]
 save(target,raw);copied.append({'source':pin(p),'frozen':pin(target)})
for name in ['test_activity.py','test_mission_regression.py','mission_cli.py']:
 p=W/'tests_core'/name;target=F/'tests_core'/name
 assert pin(p)['sha256']==expected[str(p)]
 save(target,p.read_bytes());copied.append({'source':pin(p),'frozen':pin(target)})
manifest={'builder_report':pin(builder),'files':copied,'independent_test':pin(R/'test_activity_adversarial_r1.py'),
 'source_pins_verified':len(expected),'freeze_confirmed_by_builder':True}
save_json(R/'FROZEN_MANIFEST_R1.json',manifest)
code='''import contextlib,importlib.util,io,json,os,socket,sys,time,unittest
from pathlib import Path
def no_network(*a,**k):raise RuntimeError('Network forbidden in independent core tests')
socket.socket.connect=no_network
socket.socket.connect_ex=no_network
socket.create_connection=no_network
root=Path(sys.argv[1]);frozen=root/'frozen_r1'
suite=unittest.TestSuite();ids=[]
for name,path in [('test_activity',frozen/'tests_core/test_activity.py'),('test_mission_regression',frozen/'tests_core/test_mission_regression.py'),('test_activity_independent',root/'test_activity_adversarial_r1.py')]:
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 tests=unittest.defaultTestLoader.loadTestsFromModule(m)
 for group in tests:ids += [t.id() for t in group]
 suite.addTests(tests)
log=io.StringIO();start=time.perf_counter()
with contextlib.redirect_stdout(log):result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
print(json.dumps({'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'test_ids':ids,'seconds':time.perf_counter()-start,'successful':result.wasSuccessful(),'log':log.getvalue()},ensure_ascii=False))
'''
env=dict(os.environ)
env['IALD_REVIEW_LIB']=str(F/'staging/core/lib')
env['IALD_MEMORY_SNAPSHOT_ARCHIVE_DIR']=str(R/'private_default_archive')
env['PYTHONDONTWRITEBYTECODE']='1'
start=time.perf_counter()
cp=subprocess.run([sys.executable,'-B','-X','utf8','-c',code,str(R)],capture_output=True,text=True,encoding='utf-8',env=env)
save(R/'TEST_STDERR_R1.txt',cp.stderr.encode('utf-8'))
if cp.returncode:
 save(R/'TEST_STDOUT_RAW_R1.txt',cp.stdout.encode('utf-8'))
 raise RuntimeError('Test runner failed; preserved stdout/stderr')
result=json.loads(cp.stdout);log=result.pop('log')
save(R/'TEST_LOG_R1.txt',log.encode('utf-8'))
for row in copied:
 assert pin(row['source']['path'])==row['source'],'Builder source changed during review'
 assert pin(row['frozen']['path'])==row['frozen'],'Frozen source changed during tests'
baseline=json.loads((W/'CORE_BASELINE.json').read_bytes())
baseline_ok=all(pin(x['path'])['sha256']==x['sha256'] for x in baseline)
assert baseline_ok
report={'schema':'organism-core-independent-tests/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
 'actor':'codex-mission-memory-review','verdict':'PASS' if result['successful'] else 'FAIL',
 **result,'elapsed_process_seconds':time.perf_counter()-start,
 'frozen_manifest':pin(R/'FROZEN_MANIFEST_R1.json'),'test_source':pin(R/'test_activity_adversarial_r1.py'),
 'log':pin(R/'TEST_LOG_R1.txt'),'stderr':pin(R/'TEST_STDERR_R1.txt'),
 'builder_tests_rerun':52,'independent_tests':result['tests_run']-52,
 'production_baseline_unchanged':baseline_ok,'source_bytes_unchanged':True,
 'network':'Main test process network disabled; subprocesses are inspected local CLI/store recovery only.',
 'production_installed':False,'provider_calls':0,'isolated_store_and_archive':True}
save_json(R/'TEST_RESULT_REVIEW_R1.json',report)
print(json.dumps({'report':pin(R/'TEST_RESULT_REVIEW_R1.json'),**{k:report[k] for k in ['verdict','tests_run','failures','errors','independent_tests','seconds']}},ensure_ascii=False,indent=2))
if not result['successful']:print(log[-14000:])
raise SystemExit(0 if result['successful'] else 1)
