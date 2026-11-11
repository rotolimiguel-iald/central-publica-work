"""Independent read-only check of the activation receipt and current pointer."""
import hashlib
import json
from pathlib import Path
import sys
from review_queue import W, Q, read, sha

d = read(Q / 'DELIVERY_TECHNICAL_R1.json')
assert d['release'] == 'v409'
assert d['status'] == 'ACTIVATED_VERIFIED_CURRENT_RECEIVED_GENERATION_CONFIRMED_NEW_PROCESS'
for row in [d['manifest'], d['active_pointer'], *d['receipts'].values()]:
    p = Path(row['path'])
    assert p.resolve(strict=True) == p and p.stat().st_size == row['bytes']
    assert sha(p) == row['sha256']
active = read(Path(d['active_pointer']['path']))
assert active['generation'] == d['generation'] and active['manifest_sha256'] == d['manifest']['sha256']
received = read(Q / 'promotion/RECEIVED_GENERATION.json')
assert received['check']['status'] == 'CURRENT'
assert received['check']['sealed_generation'] == d['generation']
assert len(received['received']) == 3
assert all(x['generation'] == d['generation'] for x in received['received'].values())
final = read(W / 'review/QUEUE_FINAL_PATHS.json')
assert (d['documents'], d['chunks']) == (final['docs'], final['chunks']) == (13, 33036)
report = {'status': 'PASS', 'reviewer': 'codex-app-01a094df', 'generation': d['generation'],
          'documents': d['documents'], 'chunks': d['chunks'], 'receipt_pins_verified': len(d['receipts']),
          'final_path_review': sha(W / 'review/QUEUE_FINAL_PATHS.json'),
          'scope': 'Pinned activation receipts, current pointer and three new-process retrieval receipts; no new science or provider call.'}
out = W / 'review/QUEUE_ACTIVATION_R1.json'
with out.open('xb') as f:
    f.write(json.dumps(report, indent=2).encode())
sys.path.insert(0, str(Q))
import session_ops as s
p = s.call('project')
r = s.call('accept', actor={'id': 'codex-app-01a094df', 'kind': 'agent'},
           expected_revision=p['receipt']['revision'], projection_sha256=p['projection_sha256'],
           task_id='activation', review_evidence=[{'path': str(out), 'sha256': sha(out)}],
           event_id='v409-queue-activation-independent-accept')
s.save('ACTIVATION_ACCEPT_R1.json', r)
print(json.dumps({'status': 'PASS', 'revision': r['receipt']['revision'], 'generation': d['generation']}))
