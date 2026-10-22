"""Pin compiled development proofs without promoting them to reviewed integration."""
from pathlib import Path
import datetime
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
MODULES = ['ScalarGNSCutMaps', 'ScalarGNSCutNorm']
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(p, raw):
    assert p.resolve().is_relative_to(ROOT)
    if p.exists():
        before = p.read_bytes()
        b = p.with_name(p.name + '.bak_' + STAMP)
        with b.open('xb') as f:
            f.write(before)
        assert b.read_bytes() == before
    t = p.with_name(p.name + '.tmp_' + STAMP)
    with t.open('xb') as f:
        f.write(raw)
    assert t.read_bytes() == raw and len(raw) > 0
    t.replace(p)
    assert p.read_bytes() == raw


records = {}
targets = {}
for name in MODULES:
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    matches = []
    for log in (ROOT / 'logs').glob(name + '_*.json'):
        row = json.loads(log.read_bytes())
        if row['sha256'] == sha(source) and row['returncode'] == 0:
            matches.append((log, row))
    assert matches, name
    log, row = sorted(matches, key=lambda pair: pair[1]['timestamp'])[-1]
    assert row['source_unchanged_during_compile']
    assert row['output_sha256'] == sha(ROOT / 'build/TGLV350' / (name + '.olean'))
    output = Path(row['stdout']).read_text(encoding='utf-8')
    names = re.findall(r'^#print axioms ([\w.]+)$', source.read_text(encoding='utf-8'), re.M)
    for target in names:
        full = 'TGLV350.Regular.' + target
        m = re.search(re.escape("'" + full + "' depends on axioms:") + r'\s*\[([^\]]*)\]', output)
        assert m, full
        axioms = {s.strip() for s in m.group(1).split(',')}
        assert axioms <= {'propext', 'Classical.choice', 'Quot.sound'}, (full, axioms)
        targets[full] = sorted(axioms)
    records[name] = {'log': str(log), **row}
assert len(targets) == 9
base = json.loads((ROOT / 'bounded_scalar_cuts_custody.json').read_bytes())
assert sha(ROOT / 'um.py') == base['working_sha256']
result = {
    'timestamp': datetime.datetime.now().astimezone().isoformat(),
    'status': 'DEVELOPMENT_COMPILED__NOT_INTEGRATED__NOT_INDEPENDENTLY_REVIEWED',
    'records': records, 'targets': targets,
    'integrated_custody': 'bounded_scalar_cuts_custody.json',
    'integrated_custody_sha256': sha(ROOT / 'bounded_scalar_cuts_custody.json'),
    'working_sha256': base['working_sha256'],
    'draft_note_sha256': sha(ROOT / 'ROTA_MAPAS_GNS_DE_CORTE_RASCUNHO.md'),
    'full_runtime': False, 'canonical_trace_constructed': False,
    'GNS_finite_ideal_completion_constructed': True,
    'GNS_finite_ideal_representation_faithful': True,
    'GNS_maximal_scalar_domain_identified': False,
    'GNS_representation_order_normality_proved': True,
    'bounded_scalar_positive_cuts_constructed': True,
    'scalar_weight_is_supremum_of_bounded_cuts': True,
    'bounded_cuts_monotone_convergence_criterion_proved': True,
    'bounded_cuts_GNS_intertwiners_constructed': True,
    'bounded_cuts_GNS_target': 'EXISTING_AMBIENT_L2_NOT_NEW_CYCLIC_GNS_SPACE',
    'bounded_cuts_GNS_norm_identity_proved': True,
    'bounded_cuts_GNS_joint_injectivity_proved': True,
    'GNS_star_domain_norm_dense': True,
    'Tomita_initial_graph_single_valued': True,
    'Tomita_initial_graph_swap_invariant': True,
    'Tomita_initial_domain_dense': True,
    'Tomita_graph_closure_single_valued': False,
    'Tomita_operator_constructed_for_scalar_weight': False,
    'KMS_proved': False, 'full_goal_complete': False,
}
save(ROOT / 'gns_cut_maps_draft_status.json', json.dumps(result, ensure_ascii=False, indent=2).encode())
print(json.dumps({'development_modules': len(records), 'development_targets': len(targets),
                  'integrated': False, 'independently_reviewed': False}))
