"""Verify the exact stage and recording-time backups without touching memories."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
c = json.loads((ROOT / 'fixed_weight_custody.json').read_bytes())
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

for name, key in [('um.py', 'working_sha256'),
                  ('RELATORIO_PESO_FORMA_FIXA.md', 'report_sha256'),
                  ('revisao/REVIEW_DUAL_FIXED_WEIGHT.md', 'review_sha256')]:
    assert digest(ROOT / name) == c[key], name
assert digest(ROOT / 'runtime_io_inventory.json') == c['runtime_io_inventory_sha256']
assert digest(ROOT / 'MINUTA_PESO_FORMA_FIXA.md') == c['reviewed_template_sha256']
for name, expected in c['modules'].items():
    assert digest(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')) == expected
verified = {}
for name, expected in c['surface_sha256'].items():
    p = Path(name)
    assert digest(p) == expected, name
    backup = Path(c['backups'][name])
    old, new = backup.read_bytes(), p.read_bytes()
    assert new.startswith(old) and len(new) > len(old), name
    assert new.count(b'TETELESTAI_V350_DUAL_FIXED_WEIGHT_20260912') == 1, name
    verified[name] = {'backup': str(backup), 'before_bytes': len(old),
                      'after_bytes': len(new), 'before_sha256': digest(backup)}
result = {'custody_ok': True, 'exact_prefix_backups': verified,
          'dual_fixed_weight_integrated_and_reviewed': True}
raw = json.dumps(result, ensure_ascii=False, indent=2).encode()
target = ROOT / 'fixed_weight_custody_verification.json'
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
                  'dual_fixed_weight_integrated_and_reviewed': True}))
