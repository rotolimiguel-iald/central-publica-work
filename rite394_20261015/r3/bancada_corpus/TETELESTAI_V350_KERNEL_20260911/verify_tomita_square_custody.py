"""Verify reviewed adjoint/square integration and exact-byte memory lineage."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

path = ROOT / 'tomita_square_custody.json'
c = json.loads(path.read_bytes())
original = Path(json.loads((ROOT / 'environment.json').read_bytes())['original_source'])
assert c['original_unchanged'] and digest(original) == c['original_sha256']
assert digest(ROOT / 'fontes/um_v350_original.py') == c['original_sha256']
assert digest(ROOT / 'um.py') == c['working_sha256']
assert digest(ROOT / 'closed_tomita_custody.json') == c['previous_custody_sha256']
previous = json.loads((ROOT / 'closed_tomita_custody.json').read_bytes())
assert digest(Path(c['previous_working_copy'])) == previous['working_sha256']
for name, pin in c['artifacts'].items():
    assert digest(ROOT / name) == pin, name
for name, pin in c['review_sha256'].items():
    assert digest(Path(name)) == pin, name
assert digest(ROOT / 'RELATORIO_ADJUNTO_QUADRADO_INTEGRADO.md') == c['report_sha256']
for name, pins in c['modules'].items():
    assert digest(ROOT / 'kernel/TGLV350' / (name + '.lean')) == pins['development_sha256']
    assert digest(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')) == pins['integrated_sha256']
prefixes = 0
for name, pin in c['surface_sha256'].items():
    surface, backup = Path(name), Path(c['backups'][name])
    assert digest(surface) == pin, name
    old, new = backup.read_bytes(), surface.read_bytes()
    assert new.startswith(old) and len(new) > len(old)
    assert digest(backup) == c['surface_before_sha256'][name]
    if name in previous['surface_sha256']:
        assert c['intervening_memory_change_since_previous'][name] == (
            digest(backup) != previous['surface_sha256'][name])
    prefixes += 1
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
assert build['incremental_build_ok'] and len(build['records']) == c['integrated_records']
for row in build['records']:
    source = Path(row['source'])
    output = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert row['returncode'] == 0 and digest(source) == row['sha256']
    assert digest(output) == row['output_sha256']
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
assert tests['passed'] == len(tests['checks']) == c['controls']
assert all(row['passed'] for row in tests['checks'])
assert tests['axiom_report_entries'] == c['audit_declarations']
assert not tests['full_monolithic_runtime_run'] and not tests['frontier']['full_plan_complete']
assert not tests['frontier']['legacy_gate_changed']
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
assert all(value is False and evidence[name] is False for name,value in c['remaining_flags'].items())
for name, axioms in c['targets'].items():
    assert evidence['axiom_report'][name] == axioms
    assert set(axioms) <= {'propext','Classical.choice','Quot.sound'}
assert c['group_target_counts'] == {'adjoint':23,'composition':18,'resolvent':6,'selfadjoint':6}
result = {'timestamp': datetime.datetime.now().astimezone().isoformat(),
          'custody_sha256': digest(path), 'custody_ok': True,
          'exact_prefix_and_backup_pairs': prefixes, 'new_targets': len(c['targets']),
          'full_goal_complete': False, 'full_runtime': False}
out = ROOT / 'tomita_square_custody_verification.json'
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
if out.exists():
    before = out.read_bytes()
    backup = out.with_name(out.name + '.bak_' + stamp)
    with backup.open('xb') as stream:
        stream.write(before)
    assert backup.read_bytes() == before
raw = json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8')
temp = out.with_name(out.name + '.tmp_' + stamp)
with temp.open('xb') as stream:
    stream.write(raw)
assert temp.read_bytes() == raw and temp.stat().st_size == len(raw) > 0
temp.replace(out)
assert out.read_bytes() == raw
print(json.dumps(result))
