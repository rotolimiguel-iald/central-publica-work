"""Reread integrated proof pins, lineage and exact-byte memory backups."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

p = ROOT / 'scalar_weight_gns_custody.json'
c = json.loads(p.read_bytes())
original = Path(json.loads((ROOT / 'environment.json').read_bytes())['original_source'])
assert sha(original) == sha(ROOT / 'fontes/um_v350_original.py') == c['original_sha256']
assert sha(ROOT / 'um.py') == c['working_sha256']
parent_path = Path(c['previous_custody_path'])
assert sha(parent_path) == c['previous_custody_sha256']
parent = json.loads(parent_path.read_bytes())
assert c['surface_before_sha256'] == parent['surface_sha256']
assert c['full_scalar_weight_GNS_identified'] and c['full_scalar_weight_closed_graph_identified']
assert c['polar_involution_proved'] and not c['KMS_proved']
assert not c['literal_ideal_equality_claimed'] and not c['raw_graph_equals_closed_graph_claimed']
for name, pin in c['artifacts'].items():
    assert sha(ROOT / name) == pin, name
for name, pin in c['review_sha256'].items():
    assert sha(Path(name)) == pin, name
assert sha(Path(c['report_path'])) == c['report_sha256']
compiled = json.loads((ROOT / 'integrated_compile.json').read_bytes())
assert compiled['incremental_build_ok'] and len(compiled['records']) == c['integrated_records']
for row in compiled['records']:
    source = Path(row['source']).resolve()
    assert source.is_relative_to(ROOT / 'kernel')
    binary = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert row['returncode'] == 0 and row['output_exists']
    assert sha(source) == row['sha256'] and sha(binary) == row['output_sha256']
for name, pin in c['surface_sha256'].items():
    surface, backup = Path(name), Path(c['backups'][name])
    assert sha(surface) == pin and sha(backup) == c['surface_before_sha256'][name]
    assert surface.read_bytes().startswith(backup.read_bytes())
    assert surface.stat().st_size > backup.stat().st_size
for name, row in c['modules'].items():
    assert sha(ROOT / 'kernel/TGLV350' / (name + '.lean')) == row['development_sha256']
    assert sha(ROOT / 'build/TGLV350' / (name + '.olean')) == row['development_binary_sha256']
    assert sha(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')) == row['integrated_sha256']
assert not any(c['remaining_flags'].values())
assert not c['gate_changed'] and not c['full_runtime'] and not c['full_goal_complete']
out = ROOT / 'scalar_weight_gns_custody_verification.json'
assert not out.exists()
raw = json.dumps({'timestamp': datetime.datetime.now().astimezone().isoformat(),
    'custody_sha256': sha(p), 'custody_ok': True,
    'compiled_source_binary_pairs_reread': len(compiled['records']),
    'immediate_byte_backups_and_prefixes': len(c['surface_sha256']),
    'original_unchanged': True, 'gate_changed': False, 'full_goal_complete': False}, indent=2).encode()
temp = out.with_suffix('.json.tmp')
with temp.open('xb') as stream:
    stream.write(raw)
assert temp.read_bytes() == raw
temp.replace(out)
assert out.read_bytes() == raw
print(raw.decode())
