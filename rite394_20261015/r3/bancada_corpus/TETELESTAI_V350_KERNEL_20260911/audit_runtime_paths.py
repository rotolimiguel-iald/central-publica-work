"""Read selected materialization/build functions as AST data, without executing um.py."""
import ast
import datetime
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
path = root / 'um.py'
raw = path.read_bytes()
tree = ast.parse(raw)
text = raw.decode('utf-8')
targets = {'_ensure_prebuilt_packages', 'materialize_embedded_kernel',
           'selftest_fail_closed', '_find_lake', 'run_process_checked',
           'verify_tgl_kernel_formalization', 'compile_pdf'}
functions = {}
assignments = {}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in targets:
        functions[node.name] = {
            'line': node.lineno, 'end_line': node.end_lineno,
            'source_sha256': hashlib.sha256(ast.get_source_segment(text, node).encode()).hexdigest(),
        }
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in {'BASE', 'OUT', 'FORMAL_DIR', 'TGL_FORMAL_MODE'}:
                assignments[target.id] = {'line': node.lineno, 'expression': ast.unparse(node.value)}
assert targets == functions.keys()
assert set(assignments) == {'BASE', 'OUT', 'FORMAL_DIR', 'TGL_FORMAL_MODE'}
result = {
    'timestamp': datetime.datetime.now().astimezone().isoformat(),
    'status': 'PARTIAL_STATIC_INSPECTION__NOT_RUNTIME_CLEARANCE',
    'um_sha256': hashlib.sha256(raw).hexdigest(),
    'executed_or_imported_um': False,
    'top_level_assignments': assignments,
    'selected_functions': functions,
    'observations': [
        'BASE is the directory of this copy; OUT is BASE; FORMAL_DIR is BASE/tgl_kernel.',
        '_ensure_prebuilt_packages can create a directory junction to donor/.lake/packages.',
        'materialize_embedded_kernel writes differing embedded files under FORMAL_DIR.',
        'verify_tgl_kernel_formalization runs lake build and lake env lean in FORMAL_DIR.',
        'The full selftest temporarily changes HalfNat and rebuilds, then restores embedded source.',
        'A junction to canonical writable package artifacts is not an isolated runtime workspace.',
    ],
    'required_before_full_run': [
        'Finish inspection of all materialization, subprocess and data paths, including embedded helpers.',
        'Prepare the full runtime under the authorized copy with dependencies isolated from originals.',
        'Validate all final resolved write targets and any junction/reparse targets.',
        'Run the actual monolith with input 1 and capture main/tampered/restored evidence separately.',
        'Do not treat current incremental proofs or this partial path inventory as a completed full run.',
    ],
}
assert path.read_bytes() == raw
destination = root / 'runtime_path_preflight.json'
assert not destination.exists()
payload = json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8')
temporary = destination.with_suffix('.json.tmp')
with temporary.open('xb') as handle:
    handle.write(payload)
assert temporary.read_bytes() == payload
temporary.replace(destination)
print(json.dumps({'source_unchanged': True, 'functions_read': len(functions),
                  'runtime_executed': False, 'output': str(destination)}))
