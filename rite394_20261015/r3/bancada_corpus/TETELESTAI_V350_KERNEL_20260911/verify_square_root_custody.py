"""Verify the exact stage and recording-time backups without touching memories."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
c = json.loads((ROOT / 'square_root_custody.json').read_bytes())
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

for name, key in [('um.py', 'working_sha256'),
                  ('RELATORIO_ENERGIA_E_RAIZ_DUAL.md', 'report_sha256'),
                  ('revisao/REVIEW_DUAL_ENERGY_AND_SQUARE_ROOT.md', 'review_sha256'),
                  ('next_energy_checkpoint.json', 'energy_checkpoint_sha256')]:
    assert digest(ROOT / name) == c[key], name
for name, expected in c['modules'].items():
    assert digest(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')) == expected
verified = {}
for name, expected in c['surface_sha256'].items():
    p = Path(name)
    assert digest(p) == expected, name
    backup = Path(c['backups'][name])
    old, new = backup.read_bytes(), p.read_bytes()
    assert new.startswith(old) and len(new) > len(old), name
    assert new.count(b'TETELESTAI_V350_DUAL_SQUARE_ROOT_20260912') == 1, name
    verified[name] = {'backup': str(backup), 'before_bytes': len(old),
                      'after_bytes': len(new), 'before_sha256': digest(backup)}
checkpoint = json.loads((ROOT / 'next_energy_checkpoint.json').read_bytes())
assert checkpoint['integrated'] and checkpoint['independent_review']
assert checkpoint['review_sha256'] == c['review_sha256']
assert digest(Path(checkpoint['source'])) == checkpoint['compile']['sha256']
assert digest(ROOT / 'build/TGLV350/DualEnergyOnResolvent.olean') == checkpoint['compile']['output_sha256']
result = {'custody_ok': True, 'exact_prefix_backups': verified,
          'energy_checkpoint_integrated_and_reviewed': True}
raw = json.dumps(result, ensure_ascii=False, indent=2).encode()
target = ROOT / 'square_root_custody_verification.json'
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
if target.exists():
    old = target.read_bytes()
    backup = target.with_name(target.name + '.bak_' + stamp)
    with backup.open('xb') as f:
        f.write(old)
    assert backup.read_bytes() == old
temp = target.with_name(target.name + '.tmp_' + stamp)
with temp.open('xb') as f:
    f.write(raw)
assert temp.read_bytes() == raw and len(raw) > 0
temp.replace(target)
assert target.read_bytes() == raw
print(json.dumps({'custody_ok': True, 'exact_prefix_backups': len(verified),
                  'energy_checkpoint_integrated_and_reviewed': True}))
