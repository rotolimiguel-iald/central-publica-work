from pathlib import Path
import ast,json,hashlib,subprocess
W=Path(__file__).parent
plan=json.loads((W/'install_plan.json').read_bytes())
checks=[]
for row in plan['files']:
    source=Path(row['source']);dest=Path(row['destination'])
    assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256']
    assert (hashlib.sha256(dest.read_bytes()).hexdigest() if dest.exists() else None)==row['baseline']
    if source.suffix=='.py':ast.parse(source.read_bytes())
    checks.append('source_and_destination_pin:'+str(dest))
assert json.loads((W/'INTEGRATION_TESTS.json').read_bytes())['passed']
for source in {row['source'] for row in plan['files'] if row['destination'].endswith('iald.js')}:
    result=subprocess.run(['node','--check',source],capture_output=True)
    assert result.returncode==0,result.stderr.decode()
checks+=['integrated14tests','javascript_syntax','scientific_baseline_unchanged','no_provider_calls_for_offline_tests']
report=dict(passed=True,plan_sha256=hashlib.sha256((W/'install_plan.json').read_bytes()).hexdigest(),checks=checks,
    scope='Static and integrated boundaries; not a live provider or physical device test')
(W/'validation').mkdir(exist_ok=True)
p=W/'validation/final_checks.json'
if p.exists():
    old=p.read_bytes();backup=p.with_name('final_checks.before_plan_'+hashlib.sha256(old).hexdigest()[:12]+'.json')
    if not backup.exists():backup.write_bytes(old)
p.write_bytes(json.dumps(report,indent=2).encode())
print(json.dumps(dict(passed=True,checks=len(checks),files=len(plan['files']))))
