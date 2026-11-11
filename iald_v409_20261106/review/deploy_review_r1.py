"""Independent installed-byte/receipt review, no installed loader execution."""
from pathlib import Path
import hashlib,json,http.client,sys
import psutil
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent.parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
read=lambda p:json.loads(Path(p).read_bytes())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
pin=lambda p:{'path':str(p),'sha256':sha(p)}
plan=read(W/'install_plan.json');review=read(W/'validation/review_final.json')
d=read(W/'deployment.json');restart=read(W/'restart.json');maintenance=read(W/'maintenance.json')
assert review['status']=='PASS' and sha(W/'install_plan.json')==review['plan_sha256']==d['plan_sha256']
for stem in ('transaction','maintenance','deploy_controlled','verify_installed','preservation_guard'):
    assert sha(W/(stem+'.py'))==review[stem+'_sha256']
assert sha(W/'PRESERVATION_BASELINE.json')==review['preservation_baseline_sha256']
approval=read(W/'APROVACAO_V409.json')
assert approval['release']=='v409' and approval['restart_web_8082'] is True
assert Path(approval['operator_reply_path']).resolve()==W/'OPERATOR_APPROVAL_V409.txt'
assert sha(approval['operator_reply_path'])==approval['operator_reply_sha256']
assert sha(W/'APROVACAO_V409.json')=='c251afda9a2c1ab80680f646949b2e48212a04203d79367ceb201eb6fd67a005'
assert set(d['files'])=={r['destination'] for r in plan['files']} and len(d['files'])==1788
backups=0
for row in plan['files']:
    dest=Path(row['destination'])
    assert sha(dest)==row['sha256']==d['files'][str(dest)]
    if row['baseline'] is not None and row['baseline']!=row['sha256']:
        saved=Path(d['backups'][str(dest)])
        assert saved.parent==dest.parent and sha(saved)==row['baseline'];backups+=1
for row in read(W/'PRESERVATION_BASELINE.json')['files']:assert sha(row['path'])==row['sha256']
plan_by_path={row['destination']:row for row in plan['files']}
baseline_unchanged=baseline_planned=0
for row in read(W/'app/RUNTIME_BASELINE.json')['files']:
    if row['path'] in plan_by_path:
        planned=plan_by_path[row['path']]
        assert planned['baseline']==row['sha256'] and sha(row['path'])==planned['sha256']
        baseline_planned+=1
    else:
        assert sha(row['path'])==row['sha256'];baseline_unchanged+=1
assert restart['status']=='PASS' and restart['http_status']==200 and restart['resume_allowed'] is True
for key in ('old_web_pid','supervisor_pid','supervisor_created'):assert restart[key]==maintenance[key]
assert restart['new_web_pid']!=restart['old_web_pid']
assert maintenance['status']=='ADMISSIONS_STOPPED'
scope=d['scope_measurement']
assert not scope['errors'] and not scope['state_changed'] and not scope['client_changed']
assert not scope['state_unreadable'] and not scope['client_unreadable']
assert scope['state_aggregate_before']==scope['state_aggregate_after'] and scope['client_aggregate_before']==scope['client_aggregate_after']
assert scope['listeners_before']==scope['listeners_after'] and not scope['local_model_changed']
assert not scope['plan_overlap_before'] and not scope['plan_overlap_after']
assert d['accounts_modified'] is False and d['client_files_changed'] is False and d['bench_restarted'] is False
installed=read(R/'iald_nucleo_fixo.json')
assert installed['operational_core']['current_release']=='v409' and installed['jev_control']['release']=='v409'
assert installed['operational_core']['release_source_sha256']==plan['deployment_identity']['source_sha256']
assert sha(installed['jev_control']['path'])==installed['jev_control']['sha256']
# Fresh independent process observation, without process control methods.
web=psutil.Process(restart['new_web_pid']);parent=web.parent()
assert parent.pid==restart['supervisor_pid'] and parent.create_time()==restart['supervisor_created']
def script_is(proc,name):
    expected=str((R/name).resolve()).casefold()
    return any(str(Path(a).resolve()).casefold()==expected for a in proc.cmdline()[1:] if a and not a.startswith('-'))
assert script_is(web,'iald_web_server.py') and script_is(parent,'start_iald_web.ps1')
listeners=[c for c in psutil.net_connections(kind='tcp') if c.status==psutil.CONN_LISTEN and c.laddr.port==8082]
assert len(listeners)==1 and listeners[0].pid==web.pid
conn=http.client.HTTPConnection('127.0.0.1',8082,timeout=10)
try:
    conn.request('GET','/login');response=conn.getresponse();assert response.status==200;response.read()
finally:conn.close()
out={'status':'PASS','reviewer':'codex-app-v409-review','task_id':'deploy','plan_sha256':review['plan_sha256'],
 'installed_files_verified':1788,'backup_original_hashes_verified':backups,'preservation_pins_verified':13,
 'runtime_baseline_unchanged':baseline_unchanged,'baseline_files_changed_exactly_as_plan':baseline_planned,
 'current_web_pid':web.pid,'same_supervisor_pid':parent.pid,'same_supervisor_creation_time':parent.create_time(),
 'current_login_http':200,'installed_manifest_release':'v409','installed_JEV_pin_verified':True,
 'historical_scope_receipt':{'state_files':scope['state_files'],'client_files':scope['client_files'],'state_and_client_aggregates_equal':True,'bench_listeners_absent_before_and_after':not any(scope['bench_running_before'].values()) and not any(scope['bench_running_after'].values())},
 'scope':'Independent current installed byte hashes, prior backup hashes, authorization binding, process identity/listener and HTTP login. Historical idle/frozen checks and before/after state aggregates are reviewed receipts, not reenacted.',
 'limitations':['verify_installed.py was not executed; loader verification belongs to next requirement.','No paid model/live conversation or physical device verification.','First sandbox Expected one web attempt is user-reported; not treated as deployment success or reexecuted.'],
 'findings':[],'provider_calls':0,'process_mutations':0,'verify_installed_executed':False,
 'evidence':[pin(W/name) for name in ('deployment.json','restart.json','maintenance.json','APROVACAO_V409.json','OPERATOR_APPROVAL_V409.txt','install_plan.json','validation/review_final.json')]}
for e in out['evidence']:assert sha(e['path'])==e['sha256']
with (W/'validation/review_deploy.json').open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2)
print(json.dumps({'status':'PASS','files':1788,'backups':backups,'web_pid':web.pid,'http':200}))
