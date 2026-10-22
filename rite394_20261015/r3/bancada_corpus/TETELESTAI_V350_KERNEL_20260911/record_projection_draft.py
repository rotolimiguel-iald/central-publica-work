"""Record compiled development sources without claiming integration or review."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
MODULES = ['UnitIntervalProjection', 'TranslationCorrelation',
           'UnitIntervalShiftProjection', 'ConstantFibreCandidate']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


records, targets = {}, {}
for name in MODULES:
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    output = ROOT / 'build/TGLV350' / (name + '.olean')
    candidates = [json.loads(p.read_bytes()) for p in sorted((ROOT / 'logs').glob(name + '_*.json'))]
    row = next(r for r in reversed(candidates) if r['returncode'] == 0
               and r['sha256'] == digest(source) and r['output_sha256'] == digest(output)
               and r['source_unchanged_during_compile'])
    stdout = Path(row['stdout']).read_text(encoding='utf-8')
    found = dict(re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", stdout))
    expected = ['TGLV350.Regular.' + n for n in
                re.findall(r'^#print axioms ([\w.]+)$', source.read_text(encoding='utf-8'), re.M)]
    assert set(found) == set(expected)
    for target, raw_axioms in found.items():
        axioms = [a.strip() for a in raw_axioms.split(',') if a.strip()]
        assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}
        targets[target] = axioms
    records[name] = row
assert len(targets) == 17
custody = json.loads((ROOT / 'fixed_locality_custody.json').read_bytes())
assert digest(ROOT / 'um.py') == custody['working_sha256']
data = {
    'timestamp': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
    'status': 'DEVELOPMENT_COMPILED__NOT_INTEGRATED__NOT_INDEPENDENTLY_REVIEWED',
    'records': records, 'targets': targets, 'target_count': len(targets),
    'current_integrated_custody': 'fixed_locality_custody.json',
    'integrated_working_sha256': custody['working_sha256'],
    'projection_as_cut_translation_integral': True,
    'fixed_algebra_commutes_unit_interval_projection': True,
    'candidate_action_on_unit_interval_constants': True,
    'candidate_equals_entire_operator': False,
    'fixed_algebra_identified_with_base': False,
    'independent_review': False, 'integrated': False,
    'canonical_trace_constructed': False, 'full_goal_complete': False,
    'full_runtime': False, 'next_route': 'ROTA_FIBRA_CONSTANTE_RASCUNHO.md',
}
p = ROOT / 'projection_draft_status.json'
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
if p.exists():
    before = p.read_bytes()
    backup = p.with_name(p.name + '.bak_' + stamp)
    with backup.open('xb') as handle:
        handle.write(before)
    assert backup.read_bytes() == before
raw = json.dumps(data, ensure_ascii=False, indent=2).encode()
temporary = p.with_name(p.name + '.tmp_' + stamp)
with temporary.open('xb') as handle:
    handle.write(raw)
assert temporary.read_bytes() == raw and len(raw) > 0
temporary.replace(p)
assert p.read_bytes() == raw
print(json.dumps({'status': data['status'], 'target_count': len(targets),
                  'integrated_working_sha256': data['integrated_working_sha256']}))
