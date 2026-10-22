"""Integrate the frozen, independently reviewed homogeneous right GNS batch."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
assert '--review-read' in sys.argv

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)

def save(path, text):
    assert path.resolve().is_relative_to(ROOT)
    before = path.read_bytes()
    backup = path.with_name(path.name + '.bak_' + STAMP)
    with backup.open('xb') as stream:
        stream.write(before)
    assert backup.read_bytes() == before
    raw = text.encode('utf-8')
    assert len(raw) > len(before)
    temporary = path.with_name(path.name + '.tmp_' + STAMP)
    with temporary.open('xb') as stream:
        stream.write(raw)
    assert temporary.read_bytes() == raw and path.read_bytes() == before
    temporary.replace(path)
    assert path.read_bytes() == raw

parent_path = ROOT / 'scalar_weight_gns_custody.json'
parent = json.loads(parent_path.read_bytes())
memory_path = ROOT / 'homogeneous_right_dev_custody.json'
memory = json.loads(memory_path.read_bytes())
data = json.loads((ROOT / 'homogeneous_right_draft_status.json').read_bytes())
review = ROOT / 'revisao/REVIEW_HOMOGENEOUS_RIGHT_GNS.md'
assert 'HOMOGENEOUS_RIGHT_GNS_DEV_REVIEW' in review.read_text(encoding='utf-8')
assert sha(review) == memory['review_sha256']
assert sha(ROOT / 'um.py') == parent['working_sha256'] == data['integrated_working_sha256']
assert memory['previous_custody_sha256'] == data['parent_custody_sha256'] == sha(parent_path)
assert data['right_adjoint_pairing_on_same_full_GNS'] and not data['integrated']
for path, pin in memory['surface_sha256'].items():
    assert sha(Path(path)) == pin, path
for path, pin in parent['artifacts'].items():
    assert sha(ROOT / path) == pin, path
names, targets = list(data['modules']), list(data['targets'])
assert len(names) == 5 and len(targets) == 28
for name, row in data['modules'].items():
    assert sha(ROOT / 'kernel/TGLV350' / (name + '.lean')) == row['source_sha256']
    assert sha(ROOT / 'build/TGLV350' / (name + '.olean')) == row['binary_sha256']

path = ROOT / 'integrate_v350.py'
text = path.read_text(encoding='utf-8')
tree = ast.parse(text)
old = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == 'tomita_batch' for t in n.targets)))
old_targets = sum(len(re.findall(r'^#print axioms ', (ROOT / 'kernel/TGLV350' /
    (name + '.lean')).read_text(encoding='utf-8'), re.M)) for name in old)
assert old_targets == 302 and not set(names).intersection(old)
text = once(text, "'ScalarWeightStarCore', 'ScalarWeightTomitaIdentification']",
    "'ScalarWeightStarCore', 'ScalarWeightTomitaIdentification',\n                " +
    ', '.join(map(repr, names)) + ']')
text = once(text, '== 302', '== 330')
save(path, text)

path = ROOT / 'compile_integrated.py'
text = path.read_text(encoding='utf-8')
anchor = "'TGLExt/V350ScalarWeightTomitaIdentification.lean',\n"
text = once(text, anchor, anchor + ''.join("                 'TGLExt/V350" + name +
    ".lean',\n" for name in names))
save(path, text)

path = ROOT / 'test_gate_extension.py'
text = path.read_text(encoding='utf-8')
anchor = "        'scalarClosedTomita_extends_weight_star'),\n"
text = once(text, anchor, anchor + '''    'homogeneous_right_full_scalar_weight_domain': (
        'homogeneous_commutant_dual_intertwines', 'hasFiniteScalarSquare_iff_memLp',
        'scalarWeight_right_homogeneous_finite', 'scalarOrbit_right_matrixUnit'),
    'homogeneous_right_same_GNS_adjoint_pairing': (
        'homogeneousRightAmbient_preserves_GNS', 'homogeneousRightGNS_intertwines',
        'homogeneousRightGNS_adjoint', 'matrixUnit_scalarWeight_pairing'),
''')
save(path, text)
print(json.dumps({'prepared_modules': names, 'new_targets': len(targets),
    'tomita_batch_targets': old_targets + len(targets), 'gate_changed': False}))
