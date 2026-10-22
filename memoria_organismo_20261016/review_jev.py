"""Independent review of the frozen JEV admission layer; no real dispatch."""
import json, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
from mission_io import WORK, pin, project, save

out=WORK/'review_jev'; out.mkdir(exist_ok=True)
target=out/'J_REVIEW_R1.json'
if target.exists(): raise SystemExit('Immutable review already exists')
p, receipt=project()
t=next(x for x in p['projection']['active'] if x['id']=='J')
assert t['status']=='review_pending' and t['submitted_by']!='codex-gerente-tgl'
delivery_path=WORK/'tests_jev/J_DELIVERY_R1.json'
d=json.loads(delivery_path.read_bytes())
checked=[]
def walk(value):
    if isinstance(value,dict):
        if 'path' in value and 'sha256' in value:
            actual=pin(value['path']); assert actual['sha256']==value['sha256']; checked.append(actual)
        for v in value.values(): walk(v)
    elif isinstance(value,list):
        for v in value: walk(v)
walk(d)
for row in d['files']:
    assert pin(row['source'])['sha256']==row['sha256']
    assert pin(row['destination'])['sha256']==row['baseline']
cmd=[sys.executable,'-B','-X','utf8','-m','unittest','test_long_admission','-v']
start=datetime.now(timezone.utc).isoformat(); clock=time.perf_counter()
cp=subprocess.run(cmd,cwd=WORK/'tests_jev',env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=out/'J_REVIEW_R1.log'
with log.open('xb') as f: f.write(cp.stdout)
save(target,{'status':'PASS' if cp.returncode==0 else 'FAIL','author':'codex-gerente-tgl',
    'builder':d['author'],'requirement':'J','started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),
    'seconds':time.perf_counter()-clock,'command':cmd,'exit':cp.returncode,'cases':13,
    'pins_checked':checked,'evidence':[pin(delivery_path),pin(log),pin(receipt)],
    'source_review':[
        'Diff is limited to admission, official long-context header and public payload receipt fields.',
        'Short limits remain unchanged; optional retrieval is minimized first. Long mode is chosen before the single request.',
        'Real transport receives the selected header; authorization, model, wallet, timeout and confidence rules are unchanged.',
        'Nonfinite/cyclic/deep/invalid Unicode input refuses. Conservative escaped-byte bounds are explicitly not exact tokenization.',
        'Independent reproduction covers 1/10/100 synthetic turns, unchanged mandatory commands, actual requests encoding, rejection and timeout without retry.',
    ],'limitations':['No live provider validation in this review. Server eligibility, latency and actual restart are D.','Long-context documents warn of lower accuracy/slower answers. No cognitive improvement measured.'],
    'production_writes':0,'provider_inference_calls':0})
print(json.dumps({'exit':cp.returncode,'review':pin(target)}))
raise SystemExit(cp.returncode)
