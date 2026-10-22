"""Copy the v350 project artifacts into the local build namespace, with byte provenance."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
env = json.loads((ROOT / 'environment.json').read_bytes())
original = Path(env['original_source'])
assert hashlib.sha256(original.read_bytes()).hexdigest() == env['original_sha256']
library = Path(env['lean_path'][1])
records = {}
for source in sorted(library.rglob('*')):
    if not source.is_file():
        continue
    relative = source.relative_to(library)
    target = ROOT / 'build' / relative
    raw = source.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if target.exists():
        assert hashlib.sha256(target.read_bytes()).hexdigest() == digest, str(target)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        temp = target.with_name(target.name + '.copy_tmp')
        temp.write_bytes(raw)
        assert hashlib.sha256(temp.read_bytes()).hexdigest() == digest
        temp.replace(target)
    records[relative.as_posix()] = {'sha256': digest, 'bytes': len(raw)}
assert hashlib.sha256(original.read_bytes()).hexdigest() == env['original_sha256']
path = ROOT / 'dependency_artifacts.json'
temp = path.with_suffix('.json.tmp')
temp.write_text(json.dumps({'source': str(library), 'base_source_sha256': env['original_sha256'],
                           'files': records}, indent=2), encoding='utf-8')
assert temp.stat().st_size > 0
temp.replace(path)
print(json.dumps({'files': len(records), 'bytes': sum(v['bytes'] for v in records.values()),
                  'copied_to': str(ROOT / 'build')}))
