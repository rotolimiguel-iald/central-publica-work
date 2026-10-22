"""Offline guards only; never invoke Gradle/signature tools/Git push."""
from pathlib import Path
import ast,hashlib,json,subprocess,sys,uuid
S=Path(__file__).resolve().parent;D=S/'android30_R3'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=sha(p))
checks={}
for n in ['run_android30_R1.py','audit_android30_R1.py','private_mobile_publish_R1.py']:
    ast.parse((D/n).read_bytes());checks[n+'_syntax']=True
build=json.loads((D/'ANDROID30_BUILD_PLAN_R1.json').read_bytes());pub=json.loads((D/'PRIVATE_MOBILE_PUBLISH_PLAN_R1.json').read_bytes())
checks['version30_and_client6']=build['versionCode']==30 and len(json.loads(Path(build['resource_plan']['path']).read_bytes())['files'])==6
checks['exact_private_allowlist']=set(pub['files'])=={'www/iald.js','ios/App/App/public/iald.js','ios/App/App.xcodeproj/project.pbxproj','android/app/build.gradle'}
checks['raw_byte_git_staging']="'hash-object','-w','--no-filters'" in (D/'private_mobile_publish_R1.py').read_text() and "git(root,'add'" not in (D/'private_mobile_publish_R1.py').read_text()
cp=subprocess.run([sys.executable,'-B',str(D/'run_android30_R1.py')],capture_output=True)
checks['unbound_refuses_before_build']=cp.returncode==2 and not (D/'RUN_INTENT_R1.json').exists() and b'UNBOUND' in cp.stdout
tree=ast.parse((D/'run_android30_R1.py').read_bytes());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='verify_main_plan')
ns=dict(Path=Path,json=json,digest=sha);exec(compile(ast.Module(body=[node],type_ignores=[]),'isolated plan guard','exec'),ns)
temp=D/('guard_fixture_'+uuid.uuid4().hex);temp.mkdir();p=temp/'plan.json';p.write_bytes(json.dumps({'files':[{}]*18,'fixture_only':True}).encode())
test=dict(main_plan_current_pin=pin(p),main_plan_frozen_pin=pin(p),main_plan_file_count=18)
ns['verify_main_plan'](test);checks['matching_pin_accepted']=True
p.write_bytes(json.dumps({'files':[{}]*17,'fixture_only':True}).encode())
try:ns['verify_main_plan'](test)
except RuntimeError:checks['changed_plan_refused']=True
else:checks['changed_plan_refused']=False
checks['runtime_baselines_unchanged']=all(sha(x['destination'])==x['baseline'] for x in json.loads(Path(build['resource_plan']['path']).read_bytes())['files'])
assert all(checks.values()),checks
result=dict(status='PASS_OFFLINE_RUNNER_GUARDS',checks=checks,build_started=False,commit=False,push=False,signature_commands=False,plan=pin(D/'ANDROID30_BUILD_PLAN_R1.json'))
with (D/'WORKFLOW_TEST_RESULTS_R3.json').open('xb') as f:f.write(json.dumps(result,indent=2).encode())
print(json.dumps({'status':result['status'],'checks':len(checks)}))
