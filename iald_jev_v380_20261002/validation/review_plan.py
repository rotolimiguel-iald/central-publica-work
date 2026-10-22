"""Independent read-only plan verification; only this review report is written."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import sys

W = Path(__file__).resolve().parents[1]
R = Path(r'C:\IALD\projetos_pyhton\IALD').resolve()
S = W / 'memory_stage'

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def read(path):
    return json.loads(Path(path).read_bytes())

def guard(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'subprocess.Popen', 'os.system'):
        raise RuntimeError('Review forbids network and process execution')

sys.addaudithook(guard)
checks = []
def check(name, passed, detail=None):
    checks.append({'name': name, 'passed': bool(passed), 'detail': detail})

plan_path = W / 'install_plan.json'
plan_raw = plan_path.read_bytes()
plan = json.loads(plan_raw)
prepared = read(S / 'prepared.json')
memory = read(W / 'validation/memory_review.json')
target = Path(plan['target']).resolve()
files = plan['files']
check('plan_release_matches_reviewed_preparation', plan['release'] == prepared['deployment_identity'])
check('target_exact_and_under_canonical_releases', str(target) == prepared['install_target'] and target.parent == R / 'canonical_releases')
check('memory_review_pass_and_exact_hash', memory['status'] == 'PASS' and plan['memory_review_sha256'] == digest((W / 'validation/memory_review.json').read_bytes()))
check('manifest_last', Path(files[-1]['destination']).resolve() == R / 'iald_nucleo_fixo.json')
check('no_mobile_changes', plan['client_files_changed'] is False)
check('quiet_snapshot_only', plan['quiet'] == {'active_jobs': 0, 'reserved_calls': 0}, 'Snapshot from main; no live ledger query by reviewer.')

sources = [Path(f['source']).resolve() for f in files]
dests = [Path(f['destination']).resolve() for f in files]
check('unique_sources_and_destinations', len(set(sources)) == len(files) == len(set(dests)))
check('scope_resolved', all(p.is_relative_to(W) for p in sources) and all(p.is_relative_to(R) for p in dests))
check('no_backup_temp_or_private_destinations', all('.bak_' not in p.name and '.tmp' not in p.name for p in dests))
source_failures, baseline_failures, immutable_failures = [], [], []
for item, source, dest in zip(files, sources, dests):
    raw = source.read_bytes()
    if digest(raw) != item['sha256'] or len(raw) != item['bytes']:
        source_failures.append(str(source))
    prior = dest.read_bytes() if dest.exists() else None
    if (digest(prior) if prior is not None else None) != item['baseline']:
        baseline_failures.append(str(dest))
    if dest.is_relative_to(target) and prior is not None and prior != raw:
        immutable_failures.append(str(dest))
check('all_source_hashes_and_sizes', not source_failures, source_failures)
check('all_production_baselines_unchanged', not baseline_failures, baseline_failures)
check('immutable_release_no_overwrites', not immutable_failures, immutable_failures)

expected = {}
for source_string, info in memory['input_pins'].items():
    source = Path(source_string).resolve()
    if source.is_relative_to(S / 'release') or source.is_relative_to(S / 'kernel'):
        expected[target / source.relative_to(S)] = (source, info['sha256'])
for name in ('IALD_Kernel_v5.txt', 'IALD_TGL_MEMORY_CORE.md', 'kernel_verification.json', 'TGL_CLUSTER_v380.md'):
    source = S / name
    expected[target / name] = (source, digest(source.read_bytes()))
source = W / 'controller/jev_control_v380.json'
expected[target / source.name] = (source, digest(source.read_bytes()))
for name in ('iald_auto_router.py', 'iald_jev_control.py', 'iald_task_bridge.py', 'iald_web_server.py'):
    source = W / 'app_patch' / name
    expected[R / name] = (source, digest(source.read_bytes()))
for name in ('prefix.md', 'manifest.json'):
    source = S / 'haiku_runtime' / name
    expected[R / '.iald_runtime/haiku' / name] = (source, digest(source.read_bytes()))
source = W / 'deploy_manifest.json'
expected[R / 'iald_nucleo_fixo.json'] = (source, digest(source.read_bytes()))
actual = {dest: (source, item['sha256']) for item, source, dest in zip(files, sources, dests)}
check('exact_reviewed_files_and_mapping', actual == expected,
      {'missing': [str(p) for p in expected.keys() - actual.keys()],
       'unexpected': [str(p) for p in actual.keys() - expected.keys()],
       'different': [str(p) for p in actual.keys() & expected.keys() if actual[p] != expected[p]]})
staged_manifest = read(S / 'manifest_staged.json')
formal_files = read(staged_manifest['published_evidence']['proof_manifest']['path'])['formal_files_sha256']
kernel_paths = {p.relative_to(target / 'kernel').as_posix() for p in dests if p.is_relative_to(target / 'kernel')}
check('kernel_full_1209_plus_catalog', len(formal_files) == 1209 and kernel_paths == set(formal_files) | {'kernel_manifest.json'})

changed_memory = []
for source_string, info in memory['input_pins'].items():
    source = Path(source_string)
    if not source.is_file() or digest(source.read_bytes()) != info['sha256']:
        changed_memory.append(source_string)
check('scientific_review_inputs_still_exact', not changed_memory, changed_memory)
manifest = read(W / 'deploy_manifest.json')
install = read(S / 'manifest_install.json')
check('manifest_only_adds_control_binding', {k: v for k, v in manifest.items() if k != 'jev_control'} == install)
contract_raw = (W / 'controller/jev_control_v380.json').read_bytes()
contract = json.loads(contract_raw)
check('control_binding', manifest['jev_control'] == {'path': str(target / 'jev_control_v380.json'), 'sha256': digest(contract_raw), 'release': plan['release']['release'], 'source_sha256': plan['release']['source_sha256']})
check('contract_program_identity', contract['source_sha256'] == plan['release']['source_sha256'] and contract['release'] == plan['release']['release'])

unresolved = []
def paths_in(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in ('path', 'kernel_bundle', 'kernel_verification') and isinstance(item, str):
                yield key, Path(item).resolve()
            else:
                yield from paths_in(item)
    elif isinstance(value, list):
        for item in value:
            yield from paths_in(item)
for key, path in paths_in(manifest):
    if key == 'kernel_bundle':
        valid = path == target / 'kernel'
    else:
        valid = path in actual
    if not valid:
        unresolved.append(str(path))
check('every_manifest_path_resolves_through_plan', not unresolved, unresolved)
check('haiku_prefix_exact_reviewed_bytes', (S / 'haiku_runtime/prefix.md').read_bytes() == (S / 'haiku_prefix.md').read_bytes())
check('original_mother_preserved', digest((R / 'IALD_Kernel_v5.txt').read_bytes()) == plan['mother_original_sha256'] == digest((S / 'IALD_Kernel_v5.txt').read_bytes()))
check('plan_unchanged_during_review', plan_path.read_bytes() == plan_raw)

report = {'status': 'PASS' if all(c['passed'] for c in checks) else 'FAIL',
          'reviewed_at_utc': datetime.now(timezone.utc).isoformat(), 'plan_sha256': digest(plan_raw),
          'files': len(files), 'bytes': sum(f['bytes'] for f in files),
          'checks_passed': sum(c['passed'] for c in checks), 'checks_total': len(checks),
          'checks': checks, 'reviewer_script_sha256': digest(Path(__file__).read_bytes()),
          'scope': 'Plan and local bytes only. This report does not approve unresolved integration findings or execute deployment. Account contents, private data, network, providers, bench services and scientific programs not accessed.',
          'operational_conditions': ['The recorded quiet and bench states are snapshots supplied by main, not live guarantees.', 'Apply must recheck quiet and baselines and restart only the web server; no bench or llama restart.']}
dest = W / 'validation/plan_review.json'
if dest.exists():
    dest.with_name(dest.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f')).write_bytes(dest.read_bytes())
raw = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode()
tmp = dest.with_name(dest.name + '.tmp_' + str(os.getpid()))
tmp.write_bytes(raw)
assert tmp.read_bytes() == raw
os.replace(tmp, dest)
print(json.dumps({k: report[k] for k in ('status', 'plan_sha256', 'files', 'bytes', 'checks_passed', 'checks_total')}))
print(json.dumps([c for c in checks if not c['passed']], ensure_ascii=False))
