"""Read-only plan audit; immutable receipts only inside this review workspace."""
import ast
import hashlib
import json
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORK))
import mission_io as io

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read(name):
    return json.loads((WORK/name).read_bytes())

plan = read('deployment_r2/INSTALL_PLAN_R1.json')
paths = ['APP_DELIVERY_R1.json', 'NATIVE_DELIVERY_R1.json', 'CORE_C2_DELIVERY_R1.json',
         'tests_jev/J_DELIVERY_R1.json', 'tests_queue/QUEUE_DELIVERY_R2.json',
         'tests_queue/Q2_DELIVERY_R1.json', 'tests_queue/QUEUE_INSTALL_PLAN_R2.json',
         'tests_queue/Q2_INSTALL_PLAN_R1.json', 'tests_app/MOBILE_EXACT_RESOURCE_PLAN_R1.json',
         'validation_final/V_DELIVERY_R1.json', 'validation_final/V_ROOT_REVIEW_R1.json',
         'validation_final/ASSEMBLY_PROVENANCE_R1.json',
         'review_deployment/P_PREPARATION_REVIEW_R1.json']
documents = {name: read(name) for name in paths}
catalog = {}
def collect(value, origin):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str):
            catalog.setdefault((value['path'], value['sha256']), []).append(origin)
        if isinstance(value.get('source'), str) and isinstance(value.get('sha256'), str):
            catalog.setdefault((value['source'], value['sha256']), []).append(origin)
        for child in value.values():
            collect(child, origin)
    elif isinstance(value, list):
        for child in value:
            collect(child, origin)

for name, data in documents.items():
    collect(data, name)

expected = {}
def register(source, destination, sha, baseline, origin):
    expected[destination] = dict(source=source, destination=destination, sha256=sha,
                                 baseline=baseline, origin=origin)

for row in documents['APP_DELIVERY_R1.json']['files']:
    register(row['source']['path'], row['target'], row['source']['sha256'],
             row['baseline_sha256'], 'A')
for row in documents['tests_jev/J_DELIVERY_R1.json']['files']:
    register(row['source'], row['destination'], row['sha256'], row['baseline'], 'J')
for name in ['tests_queue/QUEUE_INSTALL_PLAN_R2.json', 'tests_queue/Q2_INSTALL_PLAN_R1.json']:
    for row in documents[name]['files']:
        register(row['source']['path'], row['destination'], row['source']['sha256'],
                 row['baseline']['sha256'], name)
for row in documents['tests_app/MOBILE_EXACT_RESOURCE_PLAN_R1.json']['files']:
    register(row['source'], row['destination'], row['sha256'], row['baseline'], 'mobile')

rows = []
for row in plan['files']:
    source, target = Path(row['source']), Path(row['destination'])
    assert target.name not in {'iald_stack_v7.py', '.env'} and not target.name.startswith('iald_psion_state')
    assert digest(source) == row['sha256'], source
    assert (digest(target) if target.exists() else None) == row['baseline'], target
    provenance = catalog.get((str(source), row['sha256']), [])
    assert provenance, source
    if str(target) in expected:
        for key in ('source', 'destination', 'sha256', 'baseline'):
            assert row[key] == expected[str(target)][key], (target, key)
    if target.suffix == '.py':
        ast.parse(source.read_bytes(), filename=str(source))
    rows.append(dict(destination=str(target), source_sha256=row['sha256'],
                     baseline_sha256=row['baseline'], provenance=provenance))

assert len(plan['files']) == len({r['destination'] for r in plan['files']}) == 31
assert set(expected) <= {r['destination'] for r in plan['files']}
mobile = [r for r in plan['files'] if 'backup_directory' in r]
assert len(mobile) == 3
assert all(Path(r['backup_directory']) == WORK/'mobile_backups' for r in mobile)
assert {r['destination'] for r in mobile} == {
    r['destination'] for r in documents['tests_app/MOBILE_EXACT_RESOURCE_PLAN_R1.json']['files']}
assert digest(plan['final_integration']['path']) == plan['final_integration']['sha256']
for name in ['tests_queue/QUEUE_DELIVERY_R2.json', 'tests_queue/Q2_DELIVERY_R1.json']:
    p = documents[name]['installation_plan']; assert digest(p['path']) == p['sha256']
for name, key in [('validation_final/V_DELIVERY_R1.json', 'source_manifest'),
                  ('validation_final/V_ROOT_REVIEW_R1.json', 'delivery'),
                  ('tests_app/MOBILE_EXACT_RESOURCE_PLAN_R1.json', 'source_delivery')]:
    p = documents[name][key]; assert digest(p['path']) == p['sha256']

unchanged = []
for name in ('maintenance.py', 'legacy_app_checks.py', 'queue_lock.py',
             'test_transaction.py', 'test_controlled.py'):
    assert (WORK/'deployment'/name).read_bytes() == (WORK/'deployment_r2'/name).read_bytes()
    unchanged.append(name)
for row in documents['CORE_C2_DELIVERY_R1.json']['files']:
    if Path(row['path']).name not in {'activity.py', 'store.py', 'mission.py'}:
        assert digest(Path(r'C:\IALD\MEMORIA_IALD\lib\iald_memory')/Path(row['path']).name) == row['sha256']

freeze = WORK/'review_deployment_r2/frozen_r1'
freeze.mkdir(exist_ok=False)
frozen = []
for name in ('transaction.py', 'controlled.py', 'maintenance.py', 'legacy_app_checks.py',
             'queue_lock.py', 'test_transaction.py', 'test_controlled.py', 'test_mobile_backup.py'):
    src = WORK/'deployment_r2'/name
    with (freeze/name).open('xb') as out:
        out.write(src.read_bytes())
    assert digest(src) == digest(freeze/name)
    frozen.append({'source': io.pin(src), 'copy': io.pin(freeze/name)})
result = {'status':'PASS', 'plan':io.pin(WORK/'deployment_r2/INSTALL_PLAN_R1.json'),
          'destination_count':len(rows), 'sources_and_current_baselines':rows,
          'unchanged_from_P':unchanged, 'mobile_backups':len(mobile),
          'evidence':[io.pin(WORK/n) for n in paths], 'freeze':frozen,
          'all_other_core_files_match_installed':True, 'production_writes':False}
io.save(WORK/'review_deployment_r2/PLAN_VERIFICATION_R1.json', result)
print(json.dumps({'status':'PASS','destinations':len(rows),'external_backups':len(mobile),
                  'frozen':len(frozen)}, ensure_ascii=False))
