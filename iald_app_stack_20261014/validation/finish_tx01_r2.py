import datetime
import hashlib
import json
from pathlib import Path

W = Path(__file__).resolve().parents[1]
V = W / 'validation'
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))
tests = read(V / 'tx01_r2_tests.json')
assert tests['passed'] and tests['tests'] == 21
for name, pin in tests['inputpins'].items():
    assert sha(name) == pin, name
plan = read(W / 'install_plan.json')
assert len(plan['files']) == 1257
for item in plan['files']:
    assert sha(item['source']) == item['sha256'], item['source']
    dest = Path(item['destination'])
    assert (sha(dest) if dest.exists() else None) == item['baseline'], str(dest)
target = V / 'review_final.json'
previous = target.read_bytes()
report = json.loads(previous)
assert report['status'] == 'CHANGES_REQUIRED'
assert report['reviewed_plan_sha256'] == sha(W / 'install_plan.json')
backup = target.with_name(target.name + '.bak_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
with backup.open('xb') as f:
    f.write(previous)
assert backup.read_bytes() == previous
report['status'] = 'PASS'
report['authorization'] = 'Independent technical review only; no deployment performed or authorized by this receipt'
report['round'] = 'R2: TX-01 only; prior independent R1 conclusions retained'
for name in ('plan', 'transaction', 'maintenance', 'deploy_controlled'):
    filename = 'install_plan.json' if name == 'plan' else name + '.py'
    report[name + '_sha256'] = sha(W / filename)
for finding in report['findings']:
    assert finding['id'] == 'TX-01'
    finding['status'] = 'RESOLVED_R2'
    finding['resolution'] = 'Exact supervisor/child identities; freeze both before quiet; terminate frozen child; require stopped supervisor and no web/listener during writes; finally resume and verify replacement child of same supervisor.'
    finding['r2_evidence'] = str(V / 'tx01_r2_tests.json')
report['open_findings'] = []
report['previous_review'] = {'path': str(backup), 'sha256': sha(backup)}
report['passed']['R2_TX01_offline_tests'] = 21
report['passed']['R2_plan_sources_and_baselines_rechecked'] = 1257
report['passed']['wallet_regression'] = 'Main receipt: 4 offline tests PASS; not rerun in TX-01 review'
report['limitations'].append('R2 uses simulated processes, sockets and HTTP only; actual Windows suspension/restart remains an operational verification, not measured here.')
report['real_process_operations'] = 0
report['production_writes'] = 0
for name in ('test_tx01_r2.py', 'tx01_r2_tests.json', 'tx01_r2_output.txt', 'wallet_regression.json', 'finish_tx01_r2.py'):
    p = V / name
    report['artifacts'].append({'path': str(p), 'sha256': sha(p)})
data = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
temp = target.with_name(target.name + '.r2.tmp')
with temp.open('xb') as f:
    f.write(data)
assert temp.read_bytes() == data and read(temp)['status'] == 'PASS'
temp.replace(target)
assert target.read_bytes() == data
print(json.dumps({'status': report['status'], 'review_sha256': sha(target), 'backup': str(backup), 'pins': {k: v for k, v in report.items() if k.endswith('_sha256')}}, indent=2))
