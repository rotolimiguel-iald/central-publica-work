"""Prepare only the reviewed involution batch for isolated integration."""
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
assert (ROOT / 'revisao/REVIEW_SCALAR_TOMITA_INVOLUTION.md').is_file()

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

parent = json.loads((ROOT / 'tomita_polar_custody.json').read_bytes())
memory = json.loads((ROOT / 'tomita_involution_dev_memory_custody.json').read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256'] == memory['working_sha256']
assert memory['parent_custody_sha256'] == sha(ROOT / 'tomita_polar_custody.json')
data = json.loads((ROOT / 'tomita_involution_draft_status.json').read_bytes())
assert data['polar_involution_proved'] and not data['integrated']
names = list(data['modules'])
targets = list(data['targets'])
for name, row in data['modules'].items():
    assert sha(ROOT / 'kernel/TGLV350' / (name + '.lean')) == row['source_sha256']
    assert sha(ROOT / 'build/TGLV350' / (name + '.olean')) == row['binary_sha256']
assert len(names) == 4 and len(targets) == 19

path = ROOT / 'integrate_v350.py'
text = path.read_text(encoding='utf-8')
tree = ast.parse(text)
old = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == 'tomita_batch' for t in n.targets)))
old_targets = sum(len(re.findall(r'^#print axioms ', (ROOT / 'kernel/TGLV350' /
    (name + '.lean')).read_text(encoding='utf-8'), re.M)) for name in old)
assert old_targets == 223 and not set(names).intersection(old)
text = once(text, "'DenseAntilinearExtension', 'ScalarTomitaPolarFactor']",
    "'DenseAntilinearExtension', 'ScalarTomitaPolarFactor',\n                " +
    ', '.join(map(repr, names)) + ']')
text = once(text, '== 223', '== 242')
save(path, text)

path = ROOT / 'compile_integrated.py'
text = path.read_text(encoding='utf-8')
anchor = "'TGLExt/V350ScalarTomitaPolarFactor.lean',\n"
text = once(text, anchor, anchor + ''.join("                 'TGLExt/V350" + name +
    ".lean',\n" for name in names))
save(path, text)

path = ROOT / 'test_gate_extension.py'
text = path.read_text(encoding='utf-8')
anchor = "        'scalarTomitaPolarFactor_factorization', 'scalarTomitaPolarFactor_surjective'),\n"
text = once(text, anchor, anchor + '''    'same_GNS_resolvent_transport_without_weight_identification': (
        'scalarTomitaResolvent_flip', 'scalarTomitaPositiveRoot_resolvent_graph',
        'scalarTomitaPolarFactor_resolvent'),
    'same_GNS_polar_involution_without_KMS_promotion': (
        'antiunitaryConjugate_sqrt', 'scalarTomitaPolar_sqrt_resolvent',
        'scalarTomitaPolar_sqrt_complement', 'scalarTomitaPolarFactor_involutive'),
''')
save(path, text)
print(json.dumps({'prepared_modules': names, 'new_targets': len(targets),
    'tomita_batch_targets': old_targets + len(targets), 'gate_changed': False}))
