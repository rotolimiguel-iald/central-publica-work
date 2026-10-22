"""Read-only release checks and atomic independent-review reports; never deploys."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os

W = Path(r'C:\IALD\Central de Patentes\work\iald_haiku55_jev_20261007')
R = Path(r'C:\IALD\projetos_pyhton\IALD').resolve()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def read_json(path):
    return json.loads(path.read_bytes())

def write_report(path, value):
    assert path.resolve().is_relative_to(W.resolve())
    raw = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    assert len(raw) > 100 and json.loads(raw) == value
    if path.exists():
        old = path.read_bytes()
        backup = path.with_name(path.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as out:
            out.write(old)
            out.flush()
            os.fsync(out.fileno())
        assert backup.read_bytes() == old
    temp = path.with_name(path.name + '.tmp_review_' + str(os.getpid()))
    with temp.open('xb') as out:
        out.write(raw)
        out.flush()
        os.fsync(out.fileno())
    assert temp.read_bytes() == raw
    os.replace(temp, path)
    assert path.read_bytes() == raw
    return {'path': str(path), 'sha256': sha(raw), 'bytes': len(raw)}

plan_bytes = (W/'plan.json').read_bytes()
plan = json.loads(plan_bytes)
plan_sha = sha(plan_bytes)
phase1_bytes = (W/'independent_review.json').read_bytes()
phase1 = json.loads(phase1_bytes)
previous = read_json(W/'independent_review_phase2.json')
old_inspection = read_json(W/'validation/independent_plan_inspection.json')
baseline = read_json(W/'baseline.json')
assert phase1['status'] == 'PASS'
assert sha(phase1_bytes) == previous['phase1_report_sha256']
assert sha((W/'baseline.json').read_bytes()) == phase1['artifacts']['baseline.json']['sha256']
phase1_files = {v['file']: v for v in phase1['files']}

# Pins measured from the reviewed bytes and printed by scripts in this review round.
reviewed_phase2 = {
    'iald_execution_guide.py': 'e68ab199fa600d9017d260a7b7fc603a366fe8555407d0024681a00f744c30c1',
    'iald_auto_router.py': '256a11f661dd70f88ca0952796e58825d9ed797c38cc739b88368aad356fcfff',
    'iald_task_policy.py': '5f7e968a5c2b881f00065b7dc83f582dbcb6915956d0cbba5a706d8a10737ec2',
}
for name, expected in reviewed_phase2.items():
    assert sha((W/'stage'/name).read_bytes()) == expected, name
changed = set()
for name, entry in baseline.items():
    assert sha((W/'original'/name).read_bytes()) == entry['sha256'], name
    assert sha((R/name).read_bytes()) == entry['sha256'], name
    current = sha((W/'stage'/name).read_bytes())
    if name not in reviewed_phase2:
        assert current == phase1_files[name]['stage_sha256'], name
    if current != entry['sha256']:
        changed.add(name)

expected_pairs = {(W/'stage'/n).resolve(): (R/n).resolve() for n in changed | {'iald_execution_guide.py'}}
for name in ['prefix.md', 'manifest.json']:
    source = W/'package'/name
    assert sha(source.read_bytes()) == phase1['artifacts']['package/'+name]['sha256']
    expected_pairs[source.resolve()] = (R/'.iald_runtime/haiku55'/name).resolve()
assert len(plan['files']) == len(expected_pairs) == 20
assert plan['no_client_change'] is True and plan['no_credentials'] is True
rows, source_bytes, seen_destinations = [], {}, set()
for item in plan['files']:
    source, dest = Path(item['source']).resolve(), Path(item['destination']).resolve()
    assert source in expected_pairs and expected_pairs[source] == dest
    assert source not in source_bytes and dest not in seen_destinations
    assert source.is_relative_to(W.resolve()) and dest.is_relative_to(R)
    raw = source.read_bytes()
    old = dest.read_bytes() if dest.exists() else None
    assert sha(raw) == item['sha256']
    assert (sha(old) if old is not None else None) == item['baseline'], str(dest)
    if source.suffix == '.py':
        ast.parse(raw)
    if dest.parent == R and dest.name in baseline:
        assert item['baseline'] == baseline[dest.name]['sha256']
    source_bytes[source] = raw
    seen_destinations.add(dest)
    rows.append({'source': str(source), 'destination': str(dest), 'stage_sha256': sha(raw),
                 'runtime_sha256': sha(old) if old is not None else None, 'cas': 'MATCH', 'new': old is None})
assert sum(r['new'] for r in rows) == 3
scripts = {n: sha((W/n).read_bytes()) for n in ['transaction.py', 'restart_web.ps1']}
assert scripts == old_inspection['script_hashes']

audit = read_json(W/'bench_capability_audit.json')
assert len(audit['operation_catalog']) == audit['metadata_extraction']['adapter_count'] == 34
for name in ['cosmos_status', 'universe_event']:
    operation = next(x for x in audit['operation_catalog'] if x['operation'] == name)
    assert operation['requires_plan'] is True
bench_pins = []
for name in ['app/iald_bench_catalog.py', 'app/iald_research_routes.py', 'app/iald_operator_bench.py', 'bench/app.py']:
    ref = audit['source_references'][name]
    actual = sha(Path(ref['path']).read_bytes())
    assert actual == ref['sha256']
    bench_pins.append({'source_ref': name, 'path': ref['path'], 'sha256': actual})

now = datetime.now(timezone.utc).isoformat()
inspection = dict(old_inspection)
inspection.update(status='PASS', utc=now, plan_sha256=plan_sha, files=rows,
                  deployment_approved=True, blocking=None, script_hashes=scripts)
inspection['approval_scope'] = 'Static independent approval for this exact plan only; installation/restart and live operational checks belong to main.'
inspection['bench_snapshot_caution'] = 'transaction.bench_snapshot is not called by apply_plan/restart. Its cosmos status GET may initialize a cache; do not describe that helper as a zero-effect passive probe.'
inspection_result = write_report(W/'validation/independent_plan_inspection.json', inspection)

report = dict(previous)
resolved = report.setdefault('resolved_findings', [])
for finding in report['findings']:
    resolved.append({**finding, 'status': 'RESOLVED', 'resolution_utc': now,
                     'resolution': 'Both MEDIA account_access fields removed. Public catalog contains no internal credential diagnostic; independent regression test passes.'})
report.update(status='PASS', utc=now, deployment_approved=True, findings=[])
report['scope'] = 'Final three-file phase2 review including bench audit guidance and P2-R1 fix; exact 20-file plan CAS and phase1 hash continuity. No future modules, private Atlas, new credentials or runtime quota changes approved.'
commands = [
    {'command': f'C:\\Python314\\python.exe -B -X utf8 "{W / "reviewextra/test_phase2_review.py"}"', 'tests': 10, 'result': 'PASS'},
    {'command': 'C:\\Python314\\python.exe -B -X utf8 -',
     'stdin': "import sys,unittest\nfrom pathlib import Path\nW=Path(r'"+str(W)+"')\nsys.path[:0]=[str(W/'stage'),r'"+str(R)+"',r'C:\\Users\\rotol\\AppData\\Roaming\\Python\\Python314\\site-packages']\ns=unittest.defaultTestLoader.discover(str(W/'jev_tests'))\nr=unittest.TextTestRunner(verbosity=1).run(s)\nraise SystemExit(not r.wasSuccessful())",
     'tests': 35, 'result': 'PASS'},
    {'command': f'C:\\Python314\\python.exe -B -X utf8 "{W / "test_server_routing.py"}"', 'tests': 8, 'result': 'PASS'},
    {'command': f'C:\\Python314\\python.exe -B -X utf8 "{W / "test_migration.py"}"', 'tests': 17, 'result': 'PASS'},
]
report['tests'].update(total=70, passed=70, failed=0, provider_calls=0, commands=commands)
report['tests']['independent_checks'] += [
    'Final full public catalog has no account_access, credential scope/date or denied-key diagnostic.',
    'Haiku-only migration regressions rerun: signed schema retained, preflight/host moderation binding preserved, overflow refuses before send, legacy executor denied and other providers retain compact bytes.',
    'All 20 source hashes, baseline CAS, unique destinations and exact approved source-to-destination mapping match. Both unchanged runtime modules omitted from the plan also match baseline.',
]
report['notes'] = [
    'independent_check remains an instruction; the connector does not enforce a different provider from the manager. The enum alone is not independent validation.',
    'Typed collaboration only narrows host rights; a delegation preference is not proof that delegation ran.',
    'No quota values, consent records, credentials or accounts were read or changed. Operational quota confirmation remains with main/operator.',
    'Bench audit supports guidance from static implementations, not present RAM residency, endpoint availability, scientific model quality or a new Lean compilation.',
    'The public v390 package remains the exact phase1 package; its size is not a claim of private Atlas coverage or every Lean source verbatim.',
    'No image/video generation executor is enabled. Real code-generated PNG/PDF plots remain a separate sandbox artifact capability.',
    'On deployment failure new targets can remain for reconciliation; transaction rollback is not a complete rollback of newly created files.',
    'Any subsequent source, package or plan change invalidates this exact-plan approval.',
]
report['files'] = [{'file': name, 'sha256': sha((W/'stage'/name).read_bytes()),
                    'bytes': (W/'stage'/name).stat().st_size,
                    'phase1_sha256': phase1_files.get(name, {}).get('stage_sha256'),
                    'new': name not in baseline} for name in reviewed_phase2]
report['bench_audit_review'] = {
    'path': str(W/'bench_capability_audit.json'), 'sha256': sha((W/'bench_capability_audit.json').read_bytes()),
    'status': 'GUIDANCE_CONSISTENT_WITH_STATIC_AUDIT', 'adapter_count': 34,
    'source_pins_rechecked': bench_pins,
    'checks': ['Historical bench index v368 is explicitly distinct from current app v390.',
               'GET cosmos_status/universe_event still requires plan/run; bench_map can import ledger history.',
               'Effective map query/offset and result paging limits are stated; upstream truncation stays partial.',
               'GPU telemetry is not a connected scientific GPU solver; conditional ringdown and diagnostic cosmology are labelled.',
               'Concrete Fundacao/IALD kernel lookups retain source hypotheses and KERNEL/KNOWN/INPUT/ONTO distinctions.'],
    'not_verified': audit['remaining_unverified'],
}
report['live_scenarios_evidence'] = {'path': str(W/'validation/live_jev_scenarios.json'),
    'sha256': sha((W/'validation/live_jev_scenarios.json').read_bytes()),
    'performed_by': 'Main, not reviewer', 'receipt': read_json(W/'validation/live_jev_scenarios.json'),
    'interpretation': 'Two router-only scenarios. No executor/bench dispatched. Receipt is supporting evidence, not an end-to-end deployment or fresh proof of final guide output quality.'}
report['plan_review'] = {'path': str(W/'plan.json'), 'sha256': plan_sha,
    'content_and_cas': 'PASS', 'file_count': 20, 'new_files': 3,
    'destinations': inspection['approval_scope'], 'script_hashes': scripts, 'approval': 'PASS_EXACT_PLAN',
    'inspection_report': inspection_result}
report['review_rounds'].append({'utc': now, 'result': 'PASS', 'resolved': ['P2-R1'],
    'scope': 'Final bench-guide enrichment, public media fix, 70 offline regressions, exact plan CAS', 'plan_sha256': plan_sha})
report.pop('last_backup', None)
report['test_artifacts'] = [{ 'path': str(p), 'sha256': sha(p.read_bytes())} for p in
    [W/'reviewextra/test_phase2_review.py', W/'test_server_routing.py', W/'test_migration.py', *sorted((W/'jev_tests').glob('test_*.py'))]]
report['phase1_report_sha256'] = sha(phase1_bytes)
phase2_result = write_report(W/'independent_review_phase2.json', report)
sequence = W/'validation'/('independent_review_phase2_' + datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f') + '.json')
sequence_result = write_report(sequence, report)

# Final compare immediately before issuing the approval token.
assert (W/'plan.json').read_bytes() == plan_bytes
for source, raw in source_bytes.items():
    assert source.read_bytes() == raw
for item in plan['files']:
    dest = Path(item['destination'])
    assert (sha(dest.read_bytes()) if dest.exists() else None) == item['baseline']
assert {n: sha((W/n).read_bytes()) for n in scripts} == scripts
checks = read_json(W/'validation/final_checks.json')
final = {
    'status': 'PASS', 'plan_sha256': plan_sha, 'reviewed_at_utc': now,
    'reviewer': 'Independent reviewer; not builder Heisenberg',
    'scope': 'Exact 20-file Haiku5.5 and bounded JEV release described by this plan; no future changes.',
    'files': rows, 'offline_tests': {'total': 70, 'passed': 70, 'failed': 0},
    'phase1_report': {'path': str(W/'independent_review.json'), 'sha256': sha(phase1_bytes)},
    'phase2_report': phase2_result, 'sequential_report': sequence_result,
    'plan_inspection': inspection_result, 'script_hashes': scripts,
    'main_final_checks_observed': {'passed': checks.get('passed'), 'plan_sha256': checks.get('plan_sha256'),
                                  'matches_reviewed_plan': checks.get('plan_sha256') == plan_sha},
    'conditions': ['Installer must recheck exact plan hash and per-file CAS; changed bytes require new independent review.',
                   'Main final_checks must be PASS and bound to the same plan; installer enforces this independently.',
                   'Main performs guarded deployment/restart and live availability verification; this reviewer did not deploy.'],
    'production_modified': False, 'stage_modified': False, 'env_read': False,
    'provider_calls_by_reviewer': 0, 'bench_execution_by_reviewer': False,
}
result = write_report(W/'validation/review_final.json', final)
print(json.dumps({'status': 'PASS', 'plan_sha256': plan_sha, 'file_count': len(rows),
                  'cas': 'MATCH', 'offline_tests': 70, 'review_final': result,
                  'phase2_report': phase2_result, 'sequential_report': sequence_result,
                  'main_checks_match': final['main_final_checks_observed']['matches_reviewed_plan']}, indent=2))
