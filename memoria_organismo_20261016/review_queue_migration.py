"""Independent review of the local legacy migration; private fixtures only."""
from datetime import datetime, timezone
import json, os, subprocess, sys, time
from pathlib import Path
from mission_io import WORK, pin, project, save
out=WORK/'review_queue'; report=out/'Q2_REVIEW_R1.json'
if report.exists(): raise SystemExit('Review exists')
state, pr=project()
task=next(t for t in state['projection']['active'] if t['id']=='Q2')
assert task['status']=='review_pending' and task['submitted_by']!='codex-gerente-tgl'
dpath=WORK/'tests_queue/Q2_DELIVERY_R1.json'
d=json.loads(dpath.read_bytes()); checked=[]
for p in d['implementation']+[d[k] for k in ('installation_plan','api','tests')]:
    actual=pin(p['path']); assert actual['sha256']==p['sha256']; checked.append(actual)
source="import unittest;from test_legacy_migration_r2 import LegacyMigrationTests as T;s=unittest.TestSuite(T(n) for n in sorted(dir(T)) if n.startswith('migration_'));r=unittest.TextTestRunner(verbosity=2).run(s);raise SystemExit(not r.wasSuccessful())"
cmd=[sys.executable,'-B','-X','utf8','-c',source]
start=datetime.now(timezone.utc).isoformat(); clock=time.perf_counter()
r=subprocess.run(cmd,cwd=WORK/'tests_queue',env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=out/'Q2_REVIEW_TESTS_R1.log'
with log.open('xb') as f:f.write(r.stdout)
save(report,{'unit':'F9.MEMORIA_ORGANISMO_20261016','requirement':'Q2',
    'reviewer':'codex-gerente-tgl','builder':d['author']['id'],
    'status':'PASS' if r.returncode==0 else 'FAIL',
    'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'seconds':time.perf_counter()-clock,
    'command':cmd,'exit':r.returncode,'pins_checked':checked,'evidence':[pin(dpath),pin(log),pin(pr)],
    'source_review':[
        'Privileged local CLI accepts only existing job UUID and exact row/memory versions, hashes and stable event; it is not exposed as an MCP/model tool.',
        'Eligibility checks stages, original context/prompt/constraints, coordination event history, deterministic child, attempts/reservations, pending outbox and external handles.',
        'Queue lock and SQLite CAS guard durable migration intent. Each ACOM transition has a durable step intent and receipt; local crash replay never dispatches.',
        'Concurrent row/supplement or ACOM revision changes refuse. No implicit rebase to a different goal/context.',
        'Only activity_version and version change in the original semantic row. Binding is enabled only after the verified ACOM chain; stages/prompts/constraints/generation remain exact.',
        'Previously completed migration returns its historical receipt with replay marker; it does not claim current state or authorize dispatch.',
    ],'scope':'15 migration cases independently reproduced. Builder44 includes29 Q regressions already independently reproduced separately. Final V retests against C2.',
    'real_migrations':0,'production_changed':False,'providers_called':0})
print(json.dumps({'exit':r.returncode,'report':str(report)}));raise SystemExit(r.returncode)
