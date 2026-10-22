"""Verify the recorded stage and its exact recording-time backups, read-only."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
custody = json.loads((ROOT / 'support_operator_custody.json').read_bytes())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


for name, key in [('um.py', 'working_sha256'),
                  ('RELATORIO_SUPORTE_E_OPERADOR_DUAL.md', 'report_sha256'),
                  ('revisao/REVIEW_DUAL_SUPPORT_OPERATOR.md', 'review_sha256'),
                  ('next_energy_checkpoint.json', 'unintegrated_development_checkpoint_sha256')]:
    assert digest(ROOT / name) == custody[key], name
for name, expected in custody['modules'].items():
    assert digest(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')) == expected

# A lexicographic maximum is wrong: old backups may have named prefixes such
# as .bak_XIIIc_*. Select the timestamp of this custody record, not such labels.
stamp = datetime.datetime.fromisoformat(custody['timestamp']).strftime('%Y%m%d_%H%M%S')
backups = {}
for name, expected in custody['surface_sha256'].items():
    path = Path(name)
    assert digest(path) == expected, name
    matches = list(path.parent.glob(path.name + '.bak_' + stamp + '_*'))
    assert len(matches) == 1, (name, matches)
    backup = matches[0]
    before, after = backup.read_bytes(), path.read_bytes()
    assert after.startswith(before) and len(after) > len(before), name
    assert after.count(b'TETELESTAI_V350_DUAL_SUPPORT_OPERATOR_20260912') == 1, name
    backups[str(path)] = {'backup': str(backup), 'before_sha256': digest(backup),
                          'before_bytes': len(before), 'after_bytes': len(after)}

checkpoint = json.loads((ROOT / 'next_energy_checkpoint.json').read_bytes())
assert digest(Path(checkpoint['source'])) == checkpoint['compile']['sha256']
assert checkpoint['compile']['returncode'] == 0
assert not checkpoint['integrated'] and not checkpoint['independent_review']
assert digest(ROOT / 'build/TGLV350/DualEnergyOnResolvent.olean') == checkpoint['compile']['output_sha256']

result = {'custody_ok': True, 'exact_prefix_backups': backups,
          'unintegrated_energy_checkpoint_current': True,
          'verification_correction': 'Initial ad-hoc lexicographic backup selection picked an old '
              'named Atlas backup; no artifact was damaged. Timestamp-specific selection verifies '
              'the exact backups made by this recording.'}
raw = json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8')
target = ROOT / 'support_operator_custody_verification.json'
if target.exists():
    prior = target.read_bytes()
    backup = target.with_name(target.name + '.bak_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    with backup.open('xb') as handle:
        handle.write(prior)
    assert backup.read_bytes() == prior
temp = target.with_name(target.name + '.tmp_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with temp.open('xb') as handle:
    handle.write(raw)
assert temp.read_bytes() == raw and temp.stat().st_size == len(raw)
temp.replace(target)
assert target.read_bytes() == raw
print(json.dumps({'custody_ok': True, 'exact_prefix_backups': len(backups),
                  'unintegrated_energy_checkpoint_current': True}))
