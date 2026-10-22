"""Pin the closed finite-ideal Tomita operator and its real standard subspace."""
from pathlib import Path
import datetime
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
MODULES = ['ScalarClosedTomita', 'ScalarTomitaStandardSubspace']
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, raw):
    assert path.resolve().is_relative_to(ROOT) and raw
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    if path.exists():
        before = path.read_bytes()
        backup = path.with_name(path.name + '.bak_' + stamp)
        with backup.open('xb') as stream:
            stream.write(before)
        assert backup.read_bytes() == before
    temp = path.with_name(path.name + '.tmp_' + stamp)
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw and temp.stat().st_size == len(raw)
    temp.replace(path)
    assert path.read_bytes() == raw

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
        match = re.search(re.escape("'" + full + "' depends on axioms:") + r'\s*\[([^\]]*)\]', output)
        assert match, full
        axioms = {s.strip() for s in match.group(1).split(',') if s.strip()}
        assert axioms <= ALLOWED, (full, axioms)
        targets[full] = sorted(axioms)
    records[name] = {'log': str(log), 'log_sha256': digest(log), **row}
assert len(targets) == 24
previous = json.loads((ROOT / 'gns_cut_maps_custody.json').read_bytes())
assert digest(ROOT / 'um.py') == previous['working_sha256']
review = ROOT / 'revisao/REVIEW_GAUSSIAN_CLOSABILITY.md'
assert review.is_file()
data = {
    'timestamp': datetime.datetime.now().astimezone().isoformat(),
    'status': 'DEVELOPMENT_COMPILED__NOT_INTEGRATED__REVIEW_PENDING',
    'records': records, 'targets': targets,
    'gaussian_review_sha256': digest(review),
    'gaussian_draft_sha256': digest(ROOT / 'gaussian_closability_draft_status.json'),
    'working_sha256': digest(ROOT / 'um.py'),
    'integrated_custody_sha256': digest(ROOT / 'gns_cut_maps_custody.json'),
    'report_sha256': digest(ROOT / 'RELATORIO_TOMITA_FECHADO_DEV.md'),
    'original_GNS_Hilbert_preserved': True,
    'closed_antilinear_operator_on_original_graph': True,
    'dense_domain_and_involution': True,
    'real_standard_subspace_constructed': True,
    'maximal_weight_domain_identified': False,
    'polar_decomposition_identified': False,
    'KMS_proved': False, 'canonical_trace_constructed': False,
    'independently_reviewed': False, 'integrated': False,
    'gate_changed': False, 'full_runtime': False, 'full_goal_complete': False,
}
save(ROOT / 'tomita_closed_draft_status.json',
     json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(records), 'targets': len(targets),
                  'closed_operator': True, 'standard_real_subspace': True,
                  'independently_reviewed': False, 'integrated': False}))
