"""Create or revise unsealed continuation 011 artifacts with exact-byte backups."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
ALLOWED = {
    'FiniteEntropyAlgebra.lean', 'TowerEntropyScaling.lean', 'SchmidtCutPurification.lean',
    'BoundaryEntropyBridge.lean', 'EntropyGeometryControls.lean',
    'CONTINUACAO011_DERIVACAO_PREVIA.md', 'CONTINUACAO011_PARECER.md', 'audit_continuation011.py',
}
request = json.load(sys.stdin)
name = request['file']
if name not in ALLOWED or (ROOT / 'CONTINUACAO011_MANIFESTO.json').exists():
    raise RuntimeError('Only unsealed continuation 011 artifacts may be changed')
path = ROOT / name
raw = path.read_bytes() if path.exists() else None
if 'content' in request:
    if raw is not None:
        raise RuntimeError('Creation cannot replace an existing file')
    output = request['content'].encode('utf-8')
else:
    if raw is None:
        raise RuntimeError('Revision requires an existing file')
    text = raw.decode('utf-8')
    for before, after in request['replacements']:
        if text.count(before) != 1:
            raise RuntimeError('Replacement must match exactly once')
        text = text.replace(before, after, 1)
    output = text.encode('utf-8')
if not output:
    raise RuntimeError('Empty artifact refused')
if raw is not None:
    backup = path.with_name(path.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    with backup.open('xb') as stream:
        stream.write(raw)
    if backup.read_bytes() != raw:
        raise RuntimeError('Backup byte verification failed')
temporary = path.with_name(path.name + '.tmp')
with temporary.open('xb') as stream:
    stream.write(output)
if temporary.stat().st_size != len(output) or temporary.read_bytes() != output:
    raise RuntimeError('Temporary byte verification failed')
temporary.replace(path)
if path.read_bytes() != output:
    raise RuntimeError('Final byte verification failed')
print(json.dumps({'file': str(path), 'bytes': len(output),
                  'sha256': hashlib.sha256(output).hexdigest()}))
