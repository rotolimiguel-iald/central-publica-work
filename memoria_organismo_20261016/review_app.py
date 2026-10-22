"""Independent source/pin review and reproduction of app boundaries in private stores."""
from datetime import datetime, timezone
import json, os, subprocess, sys, time
from pathlib import Path
from mission_io import WORK, pin, project, save

out = WORK/'review_app'
out.mkdir(exist_ok=True)
target = out/'A_REVIEW_R1.json'
if target.exists():
    raise SystemExit('Immutable review exists')
state, projection_receipt = project()
task = next(t for t in state['projection']['active'] if t['id']=='A')
assert task['status']=='review_pending' and task['submitted_by']!='codex-gerente-tgl'
delivery_path = WORK/'APP_DELIVERY_R1.json'
delivery = json.loads(delivery_path.read_bytes())
checked=[]
for p in [x['source'] for x in delivery['files']] + [delivery[k] for k in ('baseline','test_results','diff','mobile')]:
    actual=pin(p['path'])
    assert actual['sha256']==p['sha256']
    checked.append(actual)
for row in delivery['files']:
    p=Path(row['target'])
    assert (pin(p)['sha256'] if p.exists() else None)==row['baseline_sha256']
command=[sys.executable,'-B','-X','utf8','-m','unittest','test_activity_app','-v']
started=datetime.now(timezone.utc).isoformat()
clock=time.perf_counter()
run=subprocess.run(command,cwd=WORK/'tests_app',env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),
                   stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=out/'A_REVIEW_TESTS_R1.log'
with log.open('xb') as stream: stream.write(run.stdout)
save(target,{
    'unit':'F9.MEMORIA_ORGANISMO_20261016','requirement':'A',
    'reviewer':'codex-gerente-tgl','builder':delivery['actor'],
    'status':'PASS' if run.returncode==0 else 'FAIL',
    'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
    'seconds':time.perf_counter()-clock,'command':command,'exit':run.returncode,
    'pins_checked':checked,'evidence':[pin(delivery_path),pin(log),pin(projection_receipt)],
    'review_findings_resolved':[
        'Parent found received-byte loss for partial/invalid UTF8. Candidate now scans readable text and preserves received byte chunks as base64/hash, without bypassing confidentiality checks.',
        'Parent found clean EOF could count as SSE success without terminator. Candidate recognizes fragmented DONE and Claude message_stop; missing terminator preserves uncertain result and raises.',
        'iter_lines custody explicitly describes LF reconstruction of requests-delivered lines; it does not claim original HTTP delimiters.',
        'User input is inscribed by ActivityRuntime once; legacy command records remain intact.',
    ],
    'source_review':[
        'Authenticated account generation determines scope. UI cannot choose principal, actor, evidence path or lease.',
        'Review endpoint is not a model tool; uses existing authentication/JSON/origin guard, explicit selection and current revision. No automatic semantic acceptance.',
        'HTTP, tool, worker and response boundaries share server-owned Binding. Unique durable intents precede effects; stale premise preserves candidate but refuses integration.',
        'Existing output remains accessible while review is pending; no mandatory click per response.',
        'Native helper is called by operational/automatic/legacy native paths and actual token checking is retained.',
        'Imported source receipt is captured once, not substituted by later disk rehash. It distinguishes import from path execution.',
    ],
    'scope':'23 private integration tests reproduced, real extracted server/auth functions and fake transports. Final V must test all consumers with C2 and real local routing packet. No claim of live provider or loaded production validation here.',
    'mobile':'Client JS is bundled in Capacitor. Backend memory serves existing clients; the new optional progress button requires resource/build distribution, tracked separately in D.',
    'production_changed':False,'providers_called':0,
})
print(json.dumps({'exit':run.returncode,'report':str(target)}))
raise SystemExit(run.returncode)
