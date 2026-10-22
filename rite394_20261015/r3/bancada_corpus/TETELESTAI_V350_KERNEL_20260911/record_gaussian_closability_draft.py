"""Pin the exact compiled Gaussian closability package, without integration."""
from pathlib import Path
import datetime
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
MODULES = ['L2PositiveMultiplier', 'L2GaussianProfile', 'FibreVonNeumann',
           'ScalarGaussianVacuum', 'SeparatingCyclicCommutant', 'DualOrbitVonNeumann',
           'ScalarGaussianGNSMap', 'VectorTomitaClosability', 'ScalarGaussianClosureTransport']

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p, raw):
    assert p.resolve().is_relative_to(ROOT)
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old = p.read_bytes()
        backup = p.with_name(p.name + '.bak_' + stamp)
        with backup.open('xb') as f:
            f.write(old)
        assert backup.read_bytes() == old
    temp = p.with_name(p.name + '.tmp_' + stamp)
    with temp.open('xb') as f:
        f.write(raw)
    assert temp.read_bytes() == raw and len(raw) > 0
    temp.replace(p)
    assert p.read_bytes() == raw

records, targets = {}, {}
for name in MODULES:
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    matches = []
    for log in (ROOT / 'logs').glob(name + '_*.json'):
        row = json.loads(log.read_bytes())
        if row['returncode'] == 0 and row['sha256'] == digest(source):
            matches.append((log, row))
    assert matches, name
    log, row = max(matches, key=lambda pair: pair[1]['timestamp'])
    assert row['source_unchanged_during_compile']
    assert row['output_sha256'] == digest(ROOT / 'build/TGLV350' / (name + '.olean'))
    output = Path(row['stdout']).read_text(encoding='utf-8')
    for short in re.findall(r'^#print axioms ([\w.]+)$', source.read_text(encoding='utf-8'), re.M):
        full = 'TGLV350.Regular.' + short
        m = re.search(re.escape("'" + full + "' depends on axioms:") + r'\s*\[([^\]]*)\]', output)
        assert m, full
        axioms = {s.strip() for s in m.group(1).split(',') if s.strip()}
        assert axioms <= {'propext', 'Classical.choice', 'Quot.sound'}, (full, axioms)
        targets[full] = sorted(axioms)
    records[name] = {'log': str(log), 'log_sha256': digest(log), **row}
assert len(targets) == 49
base = json.loads((ROOT / 'gns_cut_maps_custody.json').read_bytes())
assert digest(ROOT / 'um.py') == base['working_sha256']
data = {
    'timestamp': datetime.datetime.now().astimezone().isoformat(),
    'status': 'DEVELOPMENT_COMPILED__NOT_INTEGRATED__NOT_INDEPENDENTLY_REVIEWED',
    'records': records, 'targets': targets,
    'integrated_custody': 'gns_cut_maps_custody.json',
    'integrated_custody_sha256': digest(ROOT / 'gns_cut_maps_custody.json'),
    'working_sha256': base['working_sha256'],
    'report_sha256': digest(ROOT / 'RELATORIO_FECHABILIDADE_GAUSSIANA_DEV.md'),
    'existing_scalar_GNS_graph_preserved': True,
    'positive_multiplier_injective': True,
    'gaussian_vector_separates_actual_image': True,
    'dual_orbit_image_von_neumann': True,
    'Tomita_graph_closure_single_valued': True,
    'Tomita_operator_packaged_in_this_stage': False,
    'GNS_maximal_scalar_domain_identified': False,
    'KMS_proved': False, 'canonical_trace_constructed': False,
    'integrated': False, 'independently_reviewed': False,
    'full_runtime': False, 'full_goal_complete': False,
}
save(ROOT / 'gaussian_closability_draft_status.json',
     json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'development_modules': len(records), 'development_targets': len(targets),
                  'graph_closure_single_valued': True, 'integrated': False,
                  'independently_reviewed': False}))
