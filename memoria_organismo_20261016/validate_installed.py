"""Verify installed bytes and real read-only service use; no scientific run."""
import hashlib, json, sys, uuid, urllib.request
from pathlib import Path
from datetime import datetime, timezone
from mission_io import WORK, pin, save, check

APP=Path(r'C:\IALD\projetos_pyhton\IALD')
QUEUE=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
CORE=Path(r'C:\IALD\MEMORIA_IALD\lib')
sys.path[:0]=[str(CORE),str(APP),str(QUEUE)]
check('D')
out=WORK/'live_validation';out.mkdir(exist_ok=False)
plan=json.loads((WORK/'deployment_r2/INSTALL_PLAN_R1.json').read_bytes())
installed=[]
for row in plan['files']:
    p=pin(row['destination']);assert p['sha256']==row['sha256'];installed.append(p)
run=WORK/'deployment_r2/runs/activation_r1'
deployment=json.loads((run/'FINAL_STATE.json').read_bytes())
assert deployment['status']=='INSTALLED'
for row in deployment['files']:
    if row['backup']:assert pin(row['backup'])['sha256']==row['baseline']
from iald_memory import activity,mission,store
import iald_app_memory,iald_activity_operations,iald_activity_ui
import iald_auto_router,iald_jev_control,iald_native_memory,iald_native_activity
from iald_orchestrator import runtime,queue_activity,bench_activity,legacy_activity_migration
modules=[activity,mission,store,iald_app_memory,iald_activity_operations,iald_activity_ui,
    iald_auto_router,iald_jev_control,iald_native_memory,iald_native_activity,
    runtime,queue_activity,bench_activity,legacy_activity_migration]
loaded=[pin(m.__file__) for m in modules]
save(out/'INSTALLED_R1.json',{'status':'PASS','time_utc':datetime.now(timezone.utc).isoformat(),
    'files':installed,'new_process_imports':loaded,'backups_verified':sum(bool(x['backup']) for x in deployment['files']),
    'restart':pin(run/'RESTART.json'),'actual_web_import_receipt':'PENDING_AUTHENTICATED_ACTIVITY_HTTP',
    'scope':'Installed sources, new-process imports and supervisor restart. No assertion that every web branch executed.'})

# Private durable ledger, installed wrapper and exact production GET route.
# No data payload, scientific calculation, admission to the real queue or worker.
rt=runtime.Runtime(state_dir=out/'bench_state',recover=False)
rid=str(uuid.uuid4())
bench_activity.admit(rt,rid,'Read only the current Bancada status to validate the installed activity wrapper.', 'estado',None)
requests=[]
def http(path,body):
    assert path=='/api/estado' and body is None and not requests
    requests.append(path)
    req=urllib.request.Request('http://127.0.0.1:18777'+path,
        headers={'Content-Type':'application/json','X-Cliente':'mcp:iald-activity'})
    with urllib.request.urlopen(req,timeout=20) as response:
        raw=response.read(4*1024*1024+1)
        if len(raw)>4*1024*1024:raise ValueError('Response exceeds verification scope')
        return json.loads(raw)
try:
    result=bench_activity.execute(rt,rid,transport=http)
    save(out/'BENCH_GET_R1.json',{'status':'RETURNED','request_id':rid,'requests':requests,
        'result':result,'recovery':bench_activity.recover(rt,rid),'calculation_requested':False,
        'production_ledger_changed':False,'accepted':False})
except Exception as exc:
    save(out/'BENCH_GET_R1.json',{'status':'FAILED_OR_UNCERTAIN','request_id':rid,'requests':requests,
        'error_type':type(exc).__name__,'recovery':bench_activity.recover(rt,rid),'repeated':False})
print(json.dumps({'installed':len(installed),'imports':len(loaded),'evidence':str(out)}))
