"""Prepare the reviewed exact-domain and antiunitary batches for isolated integration."""
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
assert (ROOT / 'revisao/REVIEW_SCALAR_TOMITA_POLAR.md').is_file()

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

parent = json.loads((ROOT / 'tomita_root_custody.json').read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
names, targets = [], []
for manifest in ['tomita_root_domain_draft_status.json', 'tomita_polar_draft_status.json']:
    data = json.loads((ROOT / manifest).read_bytes())
    for name, row in data['modules'].items():
        assert sha(ROOT / 'kernel/TGLV350' / (name + '.lean')) == row['source_sha256']
        assert sha(ROOT / 'build/TGLV350' / (name + '.olean')) == row['binary_sha256']
        names.append(name)
    targets.extend(data['targets'])
assert len(names) == len(set(names)) == 9
assert len(targets) == len(set(targets)) == 41

path = ROOT / 'integrate_v350.py'
text = path.read_text(encoding='utf-8')
tree = ast.parse(text)
old = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == 'tomita_batch' for t in n.targets)))
old_targets = sum(len(re.findall(r'^#print axioms ', (ROOT / 'kernel/TGLV350' /
    (name + '.lean')).read_text(encoding='utf-8'), re.M)) for name in old)
assert old_targets == 182 and not set(names).intersection(old)
text = once(text, "'PartialSquareEnergy', 'ScalarTomitaRootEnergy']",
    "'PartialSquareEnergy', 'ScalarTomitaRootEnergy',\n                " +
    ', '.join(map(repr, names)) + ']')
text = once(text, '== 182', '== ' + str(old_targets + len(targets)))
save(path, text)

path = ROOT / 'compile_integrated.py'
text = path.read_text(encoding='utf-8')
anchor = "'TGLExt/V350ScalarTomitaRootEnergy.lean',\n"
text = once(text, anchor, anchor + ''.join("                 'TGLExt/V350" + name +
    ".lean',\n" for name in names))
save(path, text)

path = ROOT / 'test_gate_extension.py'
text = path.read_text(encoding='utf-8')
anchor = "        'scalarTomitaPositiveRoot_zero_only'),\n"
text = once(text, anchor, anchor + '''    'exact_root_domain_and_full_energy': (
        'scalarTomitaSquare_graph_core', 'scalarTomitaSquare_root_graph_core',
        'scalarTomitaPositiveRoot_domain_eq', 'scalarTomitaPositiveRoot_energy'),
    'same_GNS_polar_antiunitary_without_modular_promotion': (
        'scalarTomitaPositiveRoot_denseRange', 'scalarTomitaRootImage_denseRange',
        'scalarTomitaPolarFactor_factorization', 'scalarTomitaPolarFactor_surjective'),
''')
save(path, text)
print(json.dumps({'prepared_modules': names, 'new_targets': len(targets),
    'tomita_batch_targets': old_targets + len(targets), 'gate_changed': False}))
