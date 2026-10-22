from pathlib import Path
import hashlib,json,re,zipfile,datetime
W=Path(__file__).resolve().parent.parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
pin=lambda p:dict(path=str(p),sha256=sha(p))
checks=[]
def ok(name,condition):
    assert condition,name
    checks.append(name)
sources=['delivery.json','live_validation.json','availability.json','FINAL_RUNTIME_PINS.json','mobile_stage/IOS37_DISTRIBUTION.json','ANDROID32_DOWNLOAD.json','APK_PUBLICATION.json','mobile_stage/AUDIT.json','mobile_stage/COMMIT.json','mobile_stage/PUSH.json','LIVE_POST_EXECUTION.json','LIVE_POST_JOB_RESULT.json','LIVE_DIAGNOSIS.json','LIVE_JOB_RESULT.json','INSTALLED_VERIFICATION.json']
def verify_refs(obj):
    if isinstance(obj,dict):
        if isinstance(obj.get('path'),str) and isinstance(obj.get('sha256'),str):
            p=Path(obj['path'])
            if p==Path(r'C:\IALD\projetos_pyhton\IALD\iald_app_providers.py') and obj['sha256']==sha(W/'budget_fix/baseline/iald_app_providers.py'):
                ok('historical_provider_source_verified_in_budget_baseline',True)
            else:ok('ref:'+obj['path'],sha(p)==obj['sha256'])
        for v in obj.values():verify_refs(v)
    elif isinstance(obj,list):
        for v in obj:verify_refs(v)
for n in sources:verify_refs(load(W/n))
runtime={}
for prefix in ['', 'budget_fix/']:
    plan=load(W/(prefix+'install_plan.json'));dep=load(W/(prefix+'deployment.json'));rev=load(W/(prefix+'validation/review_final.json'));restart=load(W/(prefix+'restart.json'))
    ok(prefix+'review-deploy-plan',rev['status']=='PASS' and dep['plan_sha256']==rev['plan_sha256']==sha(W/(prefix+'install_plan.json')))
    ok(prefix+'restart',restart['status']=='PASS' and restart['http_status']==200 and restart['new_web_pid']!=restart['old_web_pid'])
    for f in plan['files']:
        p=Path(f['destination']);ok('runtime:'+str(p),sha(p)==f['sha256']==dep['files'][str(p.resolve())]);runtime[str(p)]=f['sha256']
        if f['baseline'] is not None and f['baseline']!=f['sha256']:
            ok('backup:'+str(p),sha(dep['backups'][str(p.resolve())])==f['baseline'])
ok('18runtime',len(runtime)==18)
science=load(W/'SCIENCE_BASELINE.json')['files'];ok('5science',len(science)==5)
for f in science:ok('science:'+f['path'],sha(f['path'])==f['sha256'])
audit=load(W/'mobile_stage/AUDIT.json');download=load(W/'ANDROID32_DOWNLOAD.json');pub=load(W/'APK_PUBLICATION.json')
for key in ['apk','aab']:ok(key+'hash',sha(audit[key])==audit[key+'_sha256'])
ok('apk_download_publication',sha(download['authenticated_browser_download'])==sha(pub['path'])==audit['apk_sha256']==download['sha256']==pub['sha256'])
ok('apk_download_size',Path(download['authenticated_browser_download']).stat().st_size==download['bytes']==4996628)
ok('anonymous_and_no_device_claim',download['anonymous_status']==302 and download['anonymous_apk_bytes']==0 and download['installed_on_device'] is False)
for key,prefix in [('apk','assets/public/'),('aab','base/assets/public/')]:
    with zipfile.ZipFile(audit[key]) as z:
        for n,h in audit['resources'].items():ok(key+':'+n,hashlib.sha256(z.read(prefix+n)).hexdigest()==h==sha(W/'integration/client_R2'/n))
logs={}
for name in ['apk_signature','baseline_signature','aab_certificate','aab_signature','badging','gradle']:
    rec=load(W/f'mobile_stage/build32/{name}.receipt.json');verify_refs(rec)
    ok(name+'exit',rec['exit_code']==0 and rec['filtered_lines']==0)
    logs[name]=Path(rec['log']['path']).read_text(encoding='utf-8')
cert=lambda t:re.findall(r'certificate SHA-256 digest:\s*([0-9a-fA-F]+)',t)
ok('APKsigner',bool(cert(logs['apk_signature'])) and cert(logs['apk_signature'])==cert(logs['baseline_signature']))
aabcert=re.findall(r'SHA256:\s*([0-9A-Fa-f:]+)',logs['aab_certificate'])
ok('AABsigner',len(aabcert)==1 and aabcert[0].replace(':','').lower()==cert(logs['apk_signature'])[0].lower())
ok('AABverified','jar verified.' in logs['aab_signature'].lower() and 'unsigned entries' not in logs['aab_signature'].lower())
ok('Android32',"versionCode='32'" in logs['badging'] and "versionName='4.1'" in logs['badging'])
commit=load(W/'mobile_stage/COMMIT.json');push=load(W/'mobile_stage/PUSH.json');ios=load(W/'mobile_stage/IOS37_DISTRIBUTION.json')
ok('commit_chain',commit['commit']==push['commit']==ios['commit'] and push['status']=='PUSHED_VERIFIED')
for name,h in commit['files'].items():ok('committed_worktree:'+name,sha(Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')/name)==h)
for group,file in [('IALD Equipe','IOS37_EQUIPE.txt'),('IALD Piloto','IOS37_PILOTO.txt')]:
    text=(W/'mobile_stage'/file).read_text(encoding='utf-8');part=text.split('row Compilação 4.1 (37)',1)[1].split('row Compilação',1)[0]
    ok(group+'document',group in text and 'Em testes' in part)
ok('ios_claim_scope',ios['physical_installation_verified'] is False and ios['exact_expiry_unknown'] is True)
live=load(W/'LIVE_POST_EXECUTION.json');summary=load(W/'live_validation.json');initial=load(W/'LIVE_JOB_RESULT.json')
ok('live_completed',live['job']['status']=='completed' and live['job']['acknowledged']==1 and live['done_received'] and not live['warnings'])
ok('exact_marker',live['output']['matches_expected_exact'] and live['output']['answer_sha256']==hashlib.sha256(live['output']['expected'].encode()).hexdigest())
ok('separate_job',live['job']['id']!=initial['job']['id'])
ok('one_observed_call',live['usage_cost']['calls']==1 and live['selection']['matched_jobs']==1 and live['selection']['other_job_intervals_overlapping']==0)
ok('reload',summary['recovered_after_reload'] and summary['new_jobs_after_reload']==0)
mem=load(W/'memory_prepare/FINAL_R1/PLAN.json');chunk=Path(mem['append']['path']).read_bytes();verify_refs(mem['receipts']);verify_refs(mem['append'])
ok('8surfaces',len(mem['surfaces'])==8 and not mem['board_route_included'])
for item in mem['surfaces']:
    before=Path(item['path']).read_bytes()
    ok('memory_precheck:'+item['path'],hashlib.sha256(before).hexdigest()==item['before_sha256'] and len(before)==item['before_bytes'])
    ok('memory_append:'+item['path'],hashlib.sha256(before+chunk).hexdigest()==item['expected_after_sha256'] and len(before+chunk)==item['expected_after_bytes'] and Path(item['path']).name!='MEMORY.md')
report={'status':'PASS','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'runtime_files':18,'science_files':5,'memory_surfaces_prechecked':8,'evidence':[pin(W/n) for n in sources],'memory_plan':pin(W/'memory_prepare/FINAL_R1/PLAN.json'),'scope':'Documentary/hash review, existing logs and zip resources only; no API, physical inspection, database decryption, Git or signature-tool execution.','limits':['Live wirebytes not measured','Cost estimate, not invoice; metric association temporal and unique, not native job foreign key','Deployment final acceptance awaits admin deadlines delivery/submission','Memory not applied by reviewer']}
(W/'review/MATERIAL_FINAL_CHECKS_R1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':'PASS','checks':len(checks),'runtime':18,'science':5,'memory':8}))
