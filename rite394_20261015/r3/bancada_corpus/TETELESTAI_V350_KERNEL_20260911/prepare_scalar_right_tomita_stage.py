"""Prepare the reviewed three-module bridge for the same S and its maximal adjoint."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
NAMES = ['ScalarRightStarGraph', 'ScalarRightClosedTomita', 'ScalarRightTomitaAdjoint']
assert '--review-read' in sys.argv

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)

def save(path, text):
    assert path.resolve().is_relative_to(ROOT)
    before = path.read_bytes()
    raw = text.encode('utf-8')
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

parent_path = ROOT / 'homogeneous_right_custody.json'
parent = json.loads(parent_path.read_bytes())
memory = json.loads((ROOT / 'scalar_right_tomita_draft_memory.json').read_bytes())
draft = json.loads((ROOT / 'scalar_right_tomita_draft_status.json').read_bytes())
extra = json.loads((ROOT / 'scalar_right_adjoint_draft_status.json').read_bytes())
review = ROOT / 'revisao/REVIEW_SCALAR_RIGHT_CLOSED_TOMITA.md'
assert 'SCALAR_RIGHT_CLOSED_TOMITA_DEV_REVIEW' in review.read_text(encoding='utf-8')
assert sha(ROOT / 'um.py') == parent['working_sha256'] == memory['working_sha256']
assert draft['parent_custody_sha256'] == memory['previous_custody_sha256'] == sha(parent_path)
assert extra['parent_draft_sha256'] == sha(ROOT / 'scalar_right_tomita_draft_status.json')
assert extra['parent_memory_sha256'] == sha(ROOT / 'scalar_right_tomita_draft_memory.json')
for path, pin in memory['surface_sha256'].items():
    assert sha(Path(path)) == pin, path
for path, pin in parent['artifacts'].items():
    assert sha(ROOT / path) == pin, path
modules = dict(draft['modules'])
modules[extra['module']] = extra
assert set(modules) == set(NAMES)
for name, row in modules.items():
    assert sha(ROOT / 'kernel/TGLV350' / (name + '.lean')) == row['source_sha256']
    assert sha(ROOT / 'build/TGLV350' / (name + '.olean')) == row['binary_sha256']
targets = dict(draft['targets'])
assert not set(targets).intersection(extra['targets'])
targets.update(extra['targets'])
assert len(targets) == 17

path = ROOT / 'integrate_v350.py'
text = path.read_text(encoding='utf-8')
tree = ast.parse(text)
old = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == 'tomita_batch' for t in n.targets)))
count = sum(len(re.findall(r'^#print axioms ', (ROOT / 'kernel/TGLV350' /
    (name + '.lean')).read_text(encoding='utf-8'), re.M)) for name in old)
assert count == 330 and not set(NAMES).intersection(old)
text = once(text, "'HomogeneousRightData', 'ScalarHomogeneousRightGNS']",
    "'HomogeneousRightData', 'ScalarHomogeneousRightGNS',\n                " +
    ', '.join(map(repr, NAMES)) + ']')
text = once(text, '== 330', '== 347')
save(path, text)

path = ROOT / 'compile_integrated.py'
text = path.read_text(encoding='utf-8')
anchor = "'TGLExt/V350ScalarHomogeneousRightGNS.lean',\n"
text = once(text, anchor, anchor + ''.join("                 'TGLExt/V350" + name +
    ".lean',\n" for name in NAMES))
save(path, text)

path = ROOT / 'test_gate_extension.py'
text = path.read_text(encoding='utf-8')
text = once(text, "blob = Path(audit_record['stdout']).read_text(encoding='utf-8')",
    "audit_raw = Path(audit_record['stdout']).read_bytes()\n"
    "audit_stream_sha256 = hashlib.sha256(audit_raw).hexdigest()\n"
    "blob = audit_raw.decode('utf-8')")
text = once(text, "           'verification_mode': compiled['mode'],\n",
    "           'verification_mode': compiled['mode'],\n"
    "           'audit_stdout_sha256': audit_stream_sha256,\n"
    "           'audit_capture_sha256_full': audit_stream_sha256,\n"
    "           'audit_stdout_path': audit_record['stdout'],\n"
    "           'audit_hash_scope': 'CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES',\n"
    "           'historical_v350_audit_metadata': {key: baseline.get(key) for key in\n"
    "               ('audit_stdout_sha256', 'audit_capture_sha256_full')},\n")
text = once(text, "check('real_compiled_exact_type_bridges', all(proofs(kf).values()))",
    "check('current_audit_hashes_match_current_raw_stream',\n"
    "      kf['audit_stdout_sha256'] == kf['audit_capture_sha256_full'] ==\n"
    "      hashlib.sha256(Path(kf['audit_stdout_path']).read_bytes()).hexdigest())\n"
    "check('historical_v350_audit_hashes_preserved_as_history',\n"
    "      kf['historical_v350_audit_metadata'] == {key: baseline.get(key) for key in\n"
    "          ('audit_stdout_sha256', 'audit_capture_sha256_full')})\n"
    "check('real_compiled_exact_type_bridges', all(proofs(kf).values()))")
anchor = "        'homogeneousRightGNS_adjoint', 'matrixUnit_scalarWeight_pairing'),\n"
text = once(text, anchor, anchor + '''    'right_preserves_same_closed_Tomita_domain': (
        'homogeneousRightGraphMap_preserves_closed_graph', 'scalarRight_mem_closedTomitaDomain',
        'scalarClosedTomita_right_intertwines', 'matrixUnit_closedTomita_right_intertwines'),
    'left_preserves_same_maximal_Tomita_adjoint_domain': (
        'scalarRightTomitaAdjoint_pairing', 'scalarRightTomitaAdjoint_maximal',
        'scalarTomitaAdjoint_left_intertwines', 'matrixUnit_TomitaAdjoint_left_intertwines'),
''')
save(path, text)
print(json.dumps({'prepared_modules': NAMES, 'new_targets': len(targets),
    'tomita_batch_targets': count + len(targets), 'gate_changed': False}))
