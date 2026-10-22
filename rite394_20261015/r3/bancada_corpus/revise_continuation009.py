"""Apply exact replacements to unsealed continuation 009 sources, with byte backups."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import sys

root = Path(__file__).resolve().parent
allowed = {
    'SmoothMatrixCalculus', 'CurvatureJetAlgebra', 'CoordinateCurvature',
    'MetricCurvatureSymmetries', 'CovariantCurvatureBianchi', 'ContractedBianchi',
    'GeometricEinsteinReconstruction', 'CurvatureControls',
}
request = json.load(sys.stdin)
module = request['module']
if module not in allowed or (root / 'CONTINUACAO009_MANIFESTO.json').exists():
    raise RuntimeError('Only unsealed continuation 009 sources may be revised')
path = root / (module + '.lean')
raw = path.read_bytes()
text = raw.decode('utf-8')
for before, after in request['replacements']:
    if text.count(before) != 1:
        raise RuntimeError('Replacement must identify exactly one source span')
    text = text.replace(before, after, 1)
output = text.encode('utf-8')
backup = path.with_name(path.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with backup.open('xb') as stream:
    stream.write(raw)
if backup.read_bytes() != raw:
    raise RuntimeError('Byte backup verification failed')
temp = path.with_name(path.name + '.tmp')
with temp.open('xb') as stream:
    stream.write(output)
if temp.stat().st_size != len(output) or temp.read_bytes() != output:
    raise RuntimeError('Incomplete replacement')
temp.replace(path)
print(json.dumps({'file': str(path), 'backup': str(backup),
                  'bytes': len(output), 'sha256': hashlib.sha256(output).hexdigest()}))
