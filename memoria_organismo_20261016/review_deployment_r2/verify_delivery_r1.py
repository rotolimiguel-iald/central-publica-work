"""Read-only final delivery pins and local Git object verification; no network."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

w = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(w))
import mission_io as m
d = json.loads((w/'DELIVERY_D_R1.json').read_bytes())
verified = []
for pin in d['evidence'] + [d['reference']]:
    assert m.pin(pin['path'])['sha256'] == pin['sha256'], pin['path']
    verified.append(pin)
mobile = next(x for x in d['availability'] if x['surface'] == 'Android')
for key in ('apk', 'aab'):
    pin = mobile[key]
    assert m.pin(pin['path'])['sha256'] == pin['sha256']
    verified.append(pin)
archive = json.loads((w/'mobile_build/ARCHIVE_REVIEW_R1.json').read_bytes())
for key in ('build_result', 'build_plan', 'audit_script', 'reference'):
    pin = archive[key]
    assert m.pin(pin['path'])['sha256'] == pin['sha256']
    verified.append(pin)
assert all(archive['checks'].values())
pub = json.loads((w/'live_validation/MOBILE_SOURCE_PUBLISH_R1.json').read_bytes())
repo = Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
def git(*args):
    cp = subprocess.run(['git', '-C', str(repo), *args], capture_output=True)
    assert cp.returncode == 0, cp.stderr.decode('utf-8', errors='replace')
    return cp.stdout

files = git('diff-tree', '--no-commit-id', '--name-only', '-r', pub['commit']).decode().splitlines()
assert set(files) == set(pub['files'])
assert git('rev-parse', pub['commit']+'^').decode().strip() == pub['prior_head']
js = m.pin(w/'staging/app/app/iald.js')['sha256']
for file in files:
    assert hashlib.sha256(git('show', pub['commit']+':'+file)).hexdigest() == js
branch = git('branch', '--show-current').decode().strip()
remote_tracking = git('rev-parse', 'refs/remotes/origin/codex/mobile-release').decode().strip()
assert remote_tracking == pub['commit']
plan = json.loads((w/'deployment_r2/INSTALL_PLAN_R1.json').read_bytes())
for file in plan['files']:
    assert m.pin(file['destination'])['sha256'] == file['sha256']
result = {'status':'PASS','verified_evidence':verified,
          'installed_destinations_rechecked':len(plan['files']),
          'private_push_local_evidence':{'commit':pub['commit'],'prior_head':pub['prior_head'],
              'files':files,'both_assets_sha256':js,'branch':branch,
              'remote_tracking_head':remote_tracking,'remote_network_query_performed':False},
          'mobile_archive_review_reused':m.pin(w/'mobile_build/ARCHIVE_REVIEW_R1.json'),
          'new_builds_tests_provider_calls':0,'verification_script':m.pin(__file__)}
m.save(w/'review_deployment_r2/FINAL_DELIVERY_PINS_R1.json',result)
print(json.dumps({'evidence_pins':len(verified),'installed':len(plan['files']),
                  'commit':pub['commit'],'private_files':files,'branch':branch},ensure_ascii=False))
