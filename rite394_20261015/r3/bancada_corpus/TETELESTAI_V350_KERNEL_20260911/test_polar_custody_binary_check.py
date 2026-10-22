"""Exercise the verifier's actual function on actual records and an isolated byte-copy control."""
import ast
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
tree = ast.parse((ROOT / 'verify_tomita_polar_custody.py').read_bytes())
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ('sha', 'verify_compile_record')]
assert len(functions) == 2
namespace = {'ROOT': ROOT, 'Path': Path, 'hashlib': hashlib}
exec(compile(ast.Module(body=functions, type_ignores=[]), '<verifier-functions-only>', 'exec'), namespace)
records = json.loads((ROOT / 'integrated_compile.json').read_bytes())['records']
for row in records:
    namespace['verify_compile_record'](row)
fixture = ROOT / 'tests' / ('polar_custody_binary_control_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
(fixture / 'kernel').mkdir(parents=True)
(fixture / 'build').mkdir()
reference = next(r for r in records if r['source'].endswith('V350PartialSquareEnergy.lean'))
source = Path(reference['source'])
binary = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
source_copy, binary_copy = fixture / 'kernel/Control.lean', fixture / 'build/Control.olean'
source_copy.write_bytes(source.read_bytes())
binary_bytes = binary.read_bytes()
binary_copy.write_bytes(binary_bytes)
row = dict(reference, source=str(source_copy))
namespace['ROOT'] = fixture
namespace['verify_compile_record'](row)
binary_copy.write_bytes(binary_bytes + b'EXPLICIT_NEGATIVE_CONTROL_NOT_A_PROOF')
rejected = False
try:
    namespace['verify_compile_record'](row)
except AssertionError:
    rejected = True
assert rejected
binary_copy.write_bytes(binary_bytes)
namespace['verify_compile_record'](row)
assert binary.read_bytes() == binary_bytes
report = {'timestamp': datetime.datetime.now().astimezone().isoformat(),
    'verifier_sha256': hashlib.sha256((ROOT / 'verify_tomita_polar_custody.py').read_bytes()).hexdigest(),
    'actual_source_binary_pairs_verified': len(records), 'isolated_copy_positive_control': True,
    'modified_binary_rejected': rejected, 'restored_copy_accepted': True,
    'compiled_original_binary_unchanged': True, 'fixture': str(fixture),
    'scope': 'Integrity regression, not a new Lean proof or a monolithic runtime.'}
out = ROOT / 'polar_custody_binary_check.json'
assert not out.exists()
raw = json.dumps(report, ensure_ascii=False, indent=2).encode()
temp = out.with_suffix('.json.tmp')
with temp.open('xb') as stream:
    stream.write(raw)
assert temp.read_bytes() == raw
temp.replace(out)
print(json.dumps(report, ensure_ascii=False))
