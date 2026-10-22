"""Parent's independent custody/regression review of N; no production effects."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from mission_io import WORK, pin, project, save

OUT = WORK/'review_native'
OUT.mkdir(exist_ok=True)
if (OUT/'N_REVIEW_R1.json').exists():
    raise SystemExit('Review evidence already exists')
projection, preflight = project()
n = next(t for t in projection['projection']['active'] if t['id'] == 'N')
assert n['status'] == 'review_pending' and n['submitted_by'] != 'codex-gerente-tgl'
delivery = json.loads((WORK/'NATIVE_DELIVERY_R1.json').read_bytes())
tests = json.loads((WORK/'tests_native/NATIVE_TEST_RESULT_R1.json').read_bytes())
checked = []
for item in delivery['implementation'] + [delivery['unchanged_supplier'],delivery['hooks'],delivery['baseline'],delivery['accepted_core']] + tests['pins']:
    actual = pin(item['path'])
    if actual['sha256'] != item['sha256']:
        raise RuntimeError('Reviewed candidate pin changed: '+item['path'])
    checked.append(actual)
cmd = [sys.executable,'-B','-X','utf8','-m','unittest','test_native_activity','test_server_hooks','-v']
start = datetime.now(timezone.utc).isoformat(); clock = time.perf_counter()
run = subprocess.run(cmd,cwd=WORK/'tests_native',env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log = OUT/'N_REVIEW_TESTS_R1.log'
with log.open('xb') as stream: stream.write(run.stdout)
save(OUT/'N_REVIEW_R1.json', {
    'unit':'F9.MEMORIA_ORGANISMO_20261016','requirement':'N','reviewer':'codex-gerente-tgl',
    'builder':delivery['author'],'status':'PASS' if run.returncode == 0 else 'FAIL',
    'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),
    'seconds':time.perf_counter()-clock,'command':cmd,'exit':run.returncode,
    'evidence':[pin(WORK/'NATIVE_DELIVERY_R1.json'),pin(preflight),pin(log)],'pins_checked':checked,
    'source_review':[
        'prepare_messages binds runtime/store/context/scope and refreshes the actual ticket before state or cache use.',
        'Full input/output kept in immutable SHA256 artifact; checkpoint candidates have source kind tool and DECLARADO status, namespace and source receipt.',
        'Checkpoint reads check namespace, exact local path/hash, algorithm and input/output digest; corruption is visible and not repaired silently.',
        'Shared singleton is not used for conversation compression. Prior algorithm byte identity and existing native functions AST preserved.',
        'Structured media/tool envelopes bypass compression; generated narrative uses assistant role; mandatory activity projection follows compression.',
        'Native final tokenizer receives actual payload/tools, and unavailable counter or overflow prevents generation.',
        'Same-call replay is read-only; new steering preserves candidate and refuses stale ticket; no semantic autoaccept.'
    ],
    'scope':'20 tests rerun independently in private stores. Source review covers new N module/helper. Actual A server remains separate candidate; final integration V must compare frozen A hooks.',
    'limitations':['HTTP counters/scientific readers simulated; no real native generation or live phone test.','Algorithm preservation is not measured cognitive improvement.'],
    'production_changed':False,'providers_called':0
})
print(json.dumps({'status':run.returncode,'review':str(OUT/'N_REVIEW_R1.json')}))
raise SystemExit(run.returncode)
