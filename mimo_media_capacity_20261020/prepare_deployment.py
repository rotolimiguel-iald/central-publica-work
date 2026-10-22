"""Prepare audited deployment primitives; never install or restart at preparation."""
from pathlib import Path
import hashlib
import json

W = Path(__file__).resolve().parent
OLD = W.parent / 'mimo26_upgrade_20261020'
pins = []
for name in ('transaction.py', 'maintenance.py', 'deploy_controlled.py'):
    source = OLD / name
    raw = source.read_bytes()
    target = W / name
    with target.open('xb') as stream:
        stream.write(raw)
    assert target.read_bytes() == raw
    pins.append(dict(source=str(source), destination=str(target),
                     sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw)))
with (W / 'DEPLOYMENT_PRIMITIVES_PREPARED.json').open('xb') as stream:
    stream.write(json.dumps(dict(status='PREPARED_NOT_EXECUTED', files=pins),
                            ensure_ascii=False, indent=2).encode())
print('Prepared three existing audited primitives; no runtime changes')
