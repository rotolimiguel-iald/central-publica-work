"""Prepare a frozen, independently reviewed scalar-weight GNS batch for integration."""
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
review = ROOT / 'revisao/REVIEW_SCALAR_WEIGHT_GNS.md'
assert 'SCALAR_WEIGHT_GNS_DEV_REVIEW' in review.read_text(encoding='utf-8')

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

parent_path = ROOT / 'tomita_involution_custody.json'
parent = json.loads(parent_path.read_bytes())
data = json.loads((ROOT / 'scalar_weight_gns_draft_status.json').read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256'] == data['integrated_working_sha256']
assert data['parent_custody_sha256'] == sha(parent_path)
assert data['full_scalar_weight_closed_graph_identified'] and not data['integrated']
names = list(data['modules'])
targets = list(data['targets'])
assert len(names) == 9 and len(targets) == 60
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
assert old_targets == 242 and not set(names).intersection(old)
text = once(text, "'AntiunitaryPositiveConjugation', 'ScalarTomitaPolarInvolution']",
    "'AntiunitaryPositiveConjugation', 'ScalarTomitaPolarInvolution',\n                " +
    ', '.join(map(repr, names)) + ']')
text = once(text, '== 242', '== 302')
save(path, text)

path = ROOT / 'compile_integrated.py'
text = path.read_text(encoding='utf-8')
anchor = "'TGLExt/V350ScalarTomitaPolarInvolution.lean',\n"
text = once(text, anchor, anchor + ''.join("                 'TGLExt/V350" + name +
    ".lean',\n" for name in names))
save(path, text)

path = ROOT / 'test_gate_extension.py'
text = path.read_text(encoding='utf-8')
anchor = "        'scalarTomitaPolar_sqrt_complement', 'scalarTomitaPolarFactor_involutive'),\n"
text = once(text, anchor, anchor + '''    'full_scalar_weight_GNS_completion_identification': (
        'scalarWeightOrbit_norm_sq', 'scalarWeight_completion_eq',
        'scalarWeightGNSAction_intertwines', 'scalarWeightGNSEmbedding_denseRange'),
    'full_scalar_weight_closed_Tomita_graph_identification': (
        'scalarWeightGNSEmbedding_sandwich_tendsto',
        'scalarWeightTomitaGraph_closure_eq', 'scalarClosedTomita_graph_eq_weight',
        'scalarClosedTomita_extends_weight_star'),
''')
save(path, text)
print(json.dumps({'prepared_modules': names, 'new_targets': len(targets),
    'tomita_batch_targets': old_targets + len(targets), 'gate_changed': False}))
