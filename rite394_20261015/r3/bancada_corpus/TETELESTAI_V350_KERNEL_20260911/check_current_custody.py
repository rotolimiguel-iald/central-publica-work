"""Read and validate a chosen custody without rewriting any artifact."""
from pathlib import Path
import hashlib
import json
import sys
root = Path(__file__).resolve().parent
path = root / sys.argv[1]
data = json.loads(path.read_bytes())
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(root / 'um.py') == data['working_sha256']
for name, pin in data['artifacts'].items():
    assert sha(root / name) == pin, name
for name, pin in data['surface_sha256'].items():
    assert sha(Path(name)) == pin, name
for name, pin in data['review_sha256'].items():
    assert sha(Path(name)) == pin, name
print(json.dumps({'custody': str(path), 'sha256': sha(path),
                  'current_pins_valid': True, 'surfaces': len(data['surface_sha256']),
                  'previous_turn': 'PROGRESS'}))
