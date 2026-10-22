"""Prepare the independently reviewed Gaussian polar and cyclic vector."""
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
    before, raw = path.read_bytes(), text.encode('utf-8')
    assert len(raw) > len(before)
    backup = path.with_name(path.name + '.bak_' + STAMP)
    with backup.open('xb') as stream:
        stream.write(before)
    assert backup.read_bytes() == before
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw and path.read_bytes() == before
    temp.replace(path)
    assert path.read_bytes() == raw

parent_path = ROOT / 'core_polar_custody.json'
parent = json.loads(parent_path.read_bytes())
draft = json.loads((ROOT / 'gaussian_polar_draft_status.json').read_bytes())
review = ROOT / 'revisao/REVIEW_GAUSSIAN_POLAR_DEV.md'
assert 'GAUSSIAN_POLAR_DEV_REVIEW' in review.read_text(encoding='utf-8')
assert draft['parent_custody_sha256'] == sha(parent_path)
assert sha(ROOT / 'um.py') == draft['integrated_working_sha256'] == parent['working_sha256']
for name, pin in parent['artifacts'].items():
    assert sha(ROOT / name) == pin, name
for name, pin in parent['surface_sha256'].items():
    assert sha(Path(name)) == pin, name
names = list(draft['modules'])
assert names == ['DenseLinearPolarExtension', 'BoundedInjectivePolar', 'ScalarGaussianImage', 'ScalarGaussianUnitary']
assert len(draft['targets']) == 34
for name, row in draft['modules'].items():
    assert sha(ROOT / 'kernel/TGLV350' / (name + '.lean')) == row['source_sha256']
    assert sha(ROOT / 'build/TGLV350' / (name + '.olean')) == row['binary_sha256']

path = ROOT / 'integrate_v350.py'
text = path.read_text(encoding='utf-8')
tree = ast.parse(text)
old = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == 'tomita_batch' for t in n.targets)))
count = sum(len(re.findall(r'^#print axioms ', (ROOT / 'kernel/TGLV350' /
    (name + '.lean')).read_text(encoding='utf-8'), re.M)) for name in old)
assert count == 491 and not set(names).intersection(old)
text = once(text, "'ScalarGNSGeneratorTransport', 'CorePolarInclusion']",
    "'ScalarGNSGeneratorTransport', 'CorePolarInclusion',\n                " +
    ', '.join(map(repr, names)) + ']')
text = once(text, '== 491', '== 525')
save(path, text)

path = ROOT / 'compile_integrated.py'
text = path.read_text(encoding='utf-8')
anchor = "'TGLExt/V350CorePolarInclusion.lean',\n"
text = once(text, anchor, anchor + ''.join("                 'TGLExt/V350" + name +
    ".lean',\n" for name in names))
save(path, text)

path = ROOT / 'test_gate_extension.py'
text = path.read_text(encoding='utf-8')
anchor = "        'scalarGNS_commutation_from_generators', 'scalarTomitaPolar_core_commutant_mem'),\n"
text = once(text, anchor, anchor + "    'gaussian_unitary_and_same_GNS_cyclic_separating_vector': (\n"
    "        'boundedInjectivePolar_intertwines', 'scalarGaussianImage_eq_orbit',\n"
    "        'scalarGaussianUnitary_intertwines', 'scalarGNSCyclicVector_separating',\n"
    "        'scalarGNSCyclicVector_cyclic'),\n")
save(path, text)
print(json.dumps({'prepared_modules': names, 'new_targets': 34,
    'tomita_batch_targets': count + 34, 'gate_changed': False}))
