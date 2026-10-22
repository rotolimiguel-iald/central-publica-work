"""Freeze staged A evidence; no production writes or provider calls."""
import ast
import datetime as dt
import difflib
import hashlib
import json
from pathlib import Path
import sys

WORK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(WORK))
import mission_io as io
APP=WORK/'staging/app'
PROD=Path(r'C:\IALD\projetos_pyhton\IALD')
OUT=WORK/'tests_app'
def pin(path):
    p=Path(path); return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
def lines(path,terms):
    text=Path(path).read_text(encoding='utf-8-sig').splitlines()
    return [{'line':i,'text':line.strip()} for i,line in enumerate(text,1) if any(t in line for t in terms)]

baseline=json.loads((OUT/'APP_SOURCE_BASELINE_R2.json').read_bytes())
files=[]; diffs=[]; unchanged=[]
for row in baseline['files']:
    target=Path(row['source']); candidate=Path(row['candidate'])
    assert pin(target)['sha256']==row['sha256'], f'Production baseline changed: {target.name}'
    if candidate.read_bytes()==target.read_bytes():
        unchanged.append(pin(target)); continue
    files.append(dict(source=pin(candidate),target=str(target),baseline_sha256=row['sha256'],action='replace'))
    diffs.extend(difflib.unified_diff(target.read_text(encoding='utf8').splitlines(True),candidate.read_text(encoding='utf8').splitlines(True),fromfile=str(target),tofile=str(candidate)))
for name in ('iald_activity_operations.py','iald_activity_ui.py'):
    assert not (PROD/name).exists(), 'New target already exists'
    files.append(dict(source=pin(APP/name),target=str(PROD/name),baseline_sha256=None,action='create'))
diff_path=OUT/'APP_DIFF_R2.txt'
assert not diff_path.exists()
diff_path.write_bytes(''.join(diffs).encode('utf8'))

mobile=PROD/'iald-app'
names=['capacitor.config.json','package.json','sincronizar_app.ps1','ios/App/ci_scripts/ci_post_clone.sh',
    'android/app/build.gradle','ios/App/App.xcodeproj/project.pbxproj','README.md']
sources=[]
for name in names:
    p=mobile/name
    sources.append(dict(**pin(p),anchors=lines(p,['webDir','server','url','version','sync','iald.js','www','CURRENT_PROJECT_VERSION','MARKETING_VERSION','gradlew','NODE_VERSION'])))
resource_paths=['www/iald.js','android/app/src/main/assets/public/iald.js','ios/App/App/public/iald.js']
io.save(OUT/'MOBILE_DELIVERY_DIAGNOSIS_R1.json',{
    'status':'REAL_READ_ONLY_DIAGNOSIS','sources':sources,'bundled_resources':[pin(mobile/p) for p in resource_paths],
    'mechanism':'Capacitor webDir=www and no server.url: client resources are bundled. Backend API is shared, but the new conversation button requires resource synchronization and platform builds/distribution.',
    'web_source':str(PROD/'app/iald.js'),
    'sync_entrypoint':str(mobile/'sincronizar_app.ps1'),
    'commands_documented':['powershell -File sincronizar_app.ps1 -ComSync','npm run sync:ios','npm run sync:android','./gradlew :app:bundleRelease :app:assembleRelease'],
    'version_scope':'Versions below are source values only, not current store availability or installed device state.',
    'source_versions':{'package':'4.1.0','android':'versionName 4.1; versionCode 27','ios':'MARKETING_VERSION 4.1; CURRENT_PROJECT_VERSION 30'},
    'channels':{'web':'staging only; backend and app/iald.js installation pending D','ios_internal_IALD_Equipe':'new resource build/distribution pending; not queried here','ios_external_IALD_Piloto':'new resource build/distribution pending; not queried here','android_APK_AAB':'new resource build/distribution pending; Play status not queried here'},
    'builds_or_pushes_executed':0,'physical_installation_verified':False})

test_source=OUT/'test_activity_app.py'
tests=[n.name for node in ast.parse(test_source.read_text(encoding='utf8')).body if isinstance(node,ast.ClassDef) for n in node.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
assert len(tests)==23
io.save(OUT/'APP_TEST_RESULTS_R1.json',{
    'status':'PASS','author':'codex-organism-app-build','timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
    'python':{'command':[r'C:\Python314\python.exe','-B','-X','utf8',str(test_source)],'tests_run':23,'elapsed_seconds':None,'exit_code':0,'tests':tests,'evidence':pin(OUT/'APP_TEST_EXECUTION_R1.json')},
    'javascript':{'fetch_real_function':{'web':{'calls':2,'passed':True},'app':{'calls':2,'passed':True},'exit_code':0,'chunk':'a88258'},'node_check':{'exit_code':0,'chunk':'eae077'}},
    'test_sources':[pin(test_source),pin(OUT/'test_fetch_activity.cjs')],
    'candidate_sources':[x['source'] for x in files],
    'dependencies':[pin(WORK/'staging/core/lib/iald_memory'/name) for name in ('activity.py','mission.py','store.py')]+[pin(WORK/'staging/native'/name) for name in ('iald_native_activity.py','iald_native_memory.py','holographic_memory.py')],
    'scope':'Real staged app functions, private MemoryStore and durable jobs, actual request handlers extracted by AST; transport functions are simulated. Production web server is not imported.',
    'provider_calls':0,'production_writes':0,
    'limits':['Not an independent review. Not a live deployment test. C2 cross-consumer validation and real JEV packet measurement will be separate after C2 freezes.','No mobile build, store distribution or physical installation.']})

coverage={
    'binding':'begin creates the authenticated operator activity once; durable request identity; ActivityRuntime projection in routing and prompts; steering freshness before operations and result integration',
    'jev':'actual post is preflighted and response custodied; Haja Luz/control/scientific contracts retained',
    'chat':'normal/stream/controller paths; response is submitted before DONE and remains review_pending',
    'providers_tools':'actual HTTP and tool effects are wrapped; single-use intents; partial/invalid UTF8 received bytes recovered from base64 with confidentiality guard before custody',
    'workers':'trusted Binding/envelope captured by server, context/scope/request/parent-operation validated; durable chat job ID admission, restart does not resend',
    'native':'N helper in automatic/legacy/operational native preparation, final native token counting preserved',
    'review':'authenticated account generation from server; existing CSRF/origin guard; optional selected batch with current revision and pinned evidence; model tools cannot accept',
    'version':'authenticated /api/activities?view=version exposes source hashes captured when UI module imports; no source paths, secrets or per-request disk rehash',
    'ui':'activity button on current conversation uses existing fetchIALD bearer/cookie behavior; progress, pending candidates and optional selected review; backend-served route retained'}
io.save(WORK/'APP_DELIVERY_R1.json',{
    'status':'DECLARADO','requirement':'A','requirement_accepted':False,'actor':'codex-organism-app-build',
    'reference':str(WORK/'SESSION_REFERENCE.json'),'mission_revision_at_resume':37,
    'files':files,'unchanged_excluded':unchanged,'baseline':pin(OUT/'APP_SOURCE_BASELINE_R2.json'),
    'test_results':pin(OUT/'APP_TEST_RESULTS_R1.json'),'diff':pin(diff_path),'mobile':pin(OUT/'MOBILE_DELIVERY_DIAGNOSIS_R1.json'),
    'coverage':coverage,
    'source_anchors':{name:lines(APP/name,terms) for name,terms in {
        'iald_app_memory.py':['def begin(','def dispatch(','def run_autonomous(','def thread_target(','def finish_result(','def observe_stream('],
        'iald_activity_operations.py':['class Lifecycle','class Operation','class Response','def validate_envelope','def _custody_raw'],
        'iald_web_server.py':['app_memory.http_call','app_memory.call','prepare_activity_payload','iald_activity_ui.register','activity_op ='],
        'iald_activity_ui.py':['IMPORT_RECEIPT =','def review(','def register('],
        'iald_chat_jobs.py':['def submit(','activity_binding','def admit(']}.items()},
    'growth_evidence':[pin(OUT/name) for name in ('APP_PROJECTION_GROWTH_FINDING_R1.json','APP_MEASUREMENT_SOURCE_R1.py','MULTITURN_MEASUREMENT_R2.json','HUMAN_REVIEW_GROWTH_R1.json')],
    'correction':'Legacy duplicate authenticated command inscription removed. New ActivityRuntime.begin is the single command event. Historical duplicates remain intact.',
    'limits':['Core C2 addresses measured mandatory projection growth; not claimed validated by A R1. Final cross-consumer validation remains V.','A new response is a candidate, never semantic success by DONE. Optional human batch review is authenticated outside model tools.','Exact replay of an interrupted direct request is refused locally, not re-dispatched. A persisted server chat job is the recovery route.','All artifacts remain in staging. Parent handles independent review, hash installation, restart, mobile synchronization/builds/distribution and memory.'],
    'production_writes':0,'provider_calls':0,'mobile_builds':0})
print(json.dumps({'delivery':pin(WORK/'APP_DELIVERY_R1.json'),'files':len(files),'new_targets':[x['target'] for x in files if x['action']=='create'],'test_results':pin(OUT/'APP_TEST_RESULTS_R1.json'),'mobile':pin(OUT/'MOBILE_DELIVERY_DIAGNOSIS_R1.json')},ensure_ascii=False))
