"""Independent parent review of Q R2, private transports only."""
from datetime import datetime, timezone
import json,os,subprocess,sys,time
from pathlib import Path
from mission_io import WORK,pin,project,save
OUT=WORK/'review_queue';OUT.mkdir(exist_ok=True)
report=OUT/'Q_REVIEW_R2.json'
if report.exists():raise SystemExit('Review already recorded')
p,pr=project()
q=next(t for t in p['projection']['active'] if t['id']=='Q')
assert q['status']=='review_pending' and q['submitted_by']!='codex-gerente-tgl'
delivery=json.loads((WORK/'tests_queue/QUEUE_DELIVERY_R2.json').read_bytes())
plan=json.loads(Path(delivery['installation_plan']['path']).read_bytes())
checked=[]
for item in [delivery[k] for k in ('installation_plan','api','tests','mcp_stdio')]+[f['source'] for f in plan['files']]:
    actual=pin(item['path']);assert actual['sha256']==item['sha256'];checked.append(actual)
for row in plan['files']:
    target=Path(row['destination']);expected=row['baseline']['sha256']
    assert (pin(target)['sha256'] if target.exists() else None)==expected
cmd=[sys.executable,'-B','-X','utf8','-m','unittest','test_queue_activity_r2','-v']
start=datetime.now(timezone.utc).isoformat();clock=time.perf_counter()
r=subprocess.run(cmd,cwd=WORK/'tests_queue',env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=OUT/'Q_REVIEW_TESTS_R2.log'
with log.open('xb') as f:f.write(r.stdout)
save(report,{'unit':'F9.MEMORIA_ORGANISMO_20261016','requirement':'Q',
    'reviewer':'codex-gerente-tgl','builder':'codex-organism-queue-build',
    'status':'PASS_WITH_LEGACY_MIGRATION_REQUIREMENT' if r.returncode==0 else 'FAIL',
    'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'seconds':time.perf_counter()-clock,
    'command':cmd,'exit':r.returncode,'pins_checked':checked,
    'evidence':[pin(WORK/'tests_queue/QUEUE_DELIVERY_R2.json'),pin(log),pin(pr)],
    'source_review':[
        'Admission checks exact server-owned task/coordination UUID, original prompt, parent stage, deterministic child UUID and single context.',
        'Provider dispatch has one durable intent, exact post-intent projection and final revision check; original scientific constraints and generation retained.',
        'R2 raw_return persists entire received JSON using immutable admission identity before validating current mutable binding; parent found and builder fixed R1 loss condition.',
        'Cancellation/epoch/premise changes refuse integration, preserve received result and do not retry. Local reconciliation is not semantic acceptance.',
        'CLI/MCP public arguments restrict identities to existing ledger IDs, no arbitrary actor/path/evidence or approval operation.',
        'External Bancada wrapper keeps exact admitted HTTP body and asynchronous task IDs; no Bancada code/numerical changes.',
        'Startup recover=False and drain preserve legacy/partial/uncertain rows. Existing legacy requests need a separate explicit migration path before further advancement.'
    ],
    'required_followup':'Q2: explicit privileged local migration for never-dispatched legacy requests, preserving IDs/payload/constraints/stages and refusing uncertain/terminal/external records. No production request is migrated by this review.',
    'live_ledger_read_only_counts':{'tasks_failed':33,'tasks_result_ready':132,'tasks_queued_running':0,'coord_awaiting_dispatch':1,'coord_prompt_ready':1},
    'scope':'29 tests reproduced with private SQLite/ACOM and fake transports. MCP smoke evidence reviewed; final V retests all consumers against C2.',
    'production_changed':False,'providers_called':0})
print(json.dumps({'exit':r.returncode,'report':str(report)}));raise SystemExit(r.returncode)
