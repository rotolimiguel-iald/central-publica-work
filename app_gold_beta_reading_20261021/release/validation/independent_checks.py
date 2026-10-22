from pathlib import Path
import ast,datetime,hashlib,json,subprocess,sys
w=Path('work/app_gold_beta_reading_20261021/release').resolve();v=w/'validation';v.mkdir(exist_ok=True);root=Path('C:/IALD/projetos_pyhton/IALD').resolve();mobile=root/'iald-app'
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
checks=[]
def check(name,cond,**data):
 if not cond:raise AssertionError(name)
 checks.append(dict(name=name,passed=True,**data))
def pin(p):return {'path':str(Path(p).resolve()),'sha256':h(p)}
def save_new(p,data):
 raw=json.dumps(data,ensure_ascii=False,indent=2).encode();tmp=p.with_name(p.name+'.tmp_review');assert not tmp.exists();tmp.write_bytes(raw);assert tmp.read_bytes()==raw
 if p.exists():
  bak=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));bak.write_bytes(p.read_bytes());assert bak.read_bytes()==p.read_bytes()
 tmp.replace(p);assert p.read_bytes()==raw
plan=load(w/'install_plan.json');planhash=h(w/'install_plan.json');ui=load(w.parent/'UI_STAGE.json');uireview=load(w.parent/'review/UI_REVIEW.json');life=load(w.parent/'review/TEST_RESULTS_R1.json');pipeline=load(w.parent/'review/PIPELINE_TESTS.json')
check('UI_review_and_lifecycle_reused_not_rerun',uireview['status']=='PASS' and life['status']=='PASS' and life['tests']==13)
for f in uireview['files']:check('UI_pin_'+Path(f['path']).name,h(f['path'])==f['sha256'])
for f in uireview['evidence']:check('UI_evidence_pin_'+Path(f['path']).name,h(f['path'])==f['sha256'])
check('pipeline_isolated_tests',pipeline['status']=='PASS',cases=len(pipeline['tests']))
for name,digest in pipeline['source_pins'].items():check('tested_script_unchanged_'+Path(name).name,h(name)==digest)
surfaces=(root/'app',mobile/'www',mobile/'ios/App/App/public',mobile/'android/app/src/main/assets/public');natives=(mobile/'ios/App/App.xcodeproj/project.pbxproj',mobile/'android/app/build.gradle');expected={s/n for s in surfaces for n in ['iald.js','iald.css']}|set(natives);actual={Path(f['destination']).resolve() for f in plan['files']}
check('exact_10_destinations_8_assets_2_versions',len(plan['files'])==10 and actual==expected and len(actual)==10)
check('manifest_client_only',load(w/'INPUT_MANIFEST.json').get('runtime')==[] and set(plan['assets'])=={'iald.js','iald.css'})
check('input_manifest_pin',plan['input_manifest_sha256']==h(w/'INPUT_MANIFEST.json'))
rows=[]
for f in plan['files']:
 p=Path(f['source']).resolve();d=Path(f['destination']).resolve();check('frozen_stage_and_target_baseline_'+str(d.relative_to(root)),p.is_relative_to(w) and h(p)==f['sha256'] and h(d)==f['baseline']);rows.append({'source':str(p),'destination':str(d),'stage_sha256':h(p),'current_destination_sha256':h(d)})
 if d.suffix in ['.js','.css']:check('asset_matches_accepted_UI_'+str(d.relative_to(root)),h(p)==next(x['sha256'] for x in ui['files'] if Path(x['path']).name==d.name))
for d,old,new,count in [(natives[0],b'CURRENT_PROJECT_VERSION = 38;',b'CURRENT_PROJECT_VERSION = 39;',2),(natives[1],b'versionCode 33',b'versionCode 34',1)]:
 f=next(x for x in plan['files'] if Path(x['destination']).resolve()==d);before=d.read_bytes();after=Path(f['source']).read_bytes();check('native_only_version_diff_'+d.name,before.count(old)==count and after==before.replace(old,new))
science=load(w/'SCIENCE_BASELINE.json');check('science_manifest_pin',plan['science_sha256']==h(w/'SCIENCE_BASELINE.json'))
for x in science['files']:check('science_unchanged_hash_only_'+x['role'],h(x['path'])==x['sha256'])
toolplan=load(w/'mobile_prepare/TOOL_PLAN.json')
for x in toolplan['tool_pins']+[toolplan['baseline_apk']]:check('mobile_tool_or_baseline_pin_'+Path(x['path']).name,h(x['path'])==x['sha256'])
# Only local Git reads, no remote queries or writes.
def git(*args):
 p=subprocess.run(['git','-C',str(mobile),*args],capture_output=True);assert p.returncode==0;return p.stdout.decode().strip()
gitstate={'branch':git('branch','--show-current'),'fetch_url':git('remote','get-url','origin'),'push_url':git('remote','get-url','--push','origin'),'HEAD':git('rev-parse','HEAD'),'status':git('status','--porcelain=v1')}
private=load(w/'PRIVATE_GIT_PLAN.json');url='https://github.com/rotolimiguel-iald/iald-app.git';check('original_authorized_repository_local_identity',gitstate['branch']==private['branch']=='codex/mobile-release' and gitstate['fetch_url']==gitstate['push_url']==private['repository']==url and gitstate['status']=='')
gitrows={str(Path(f['destination']).resolve().relative_to(mobile)).replace('\\','/'):f['sha256'] for f in plan['files'] if Path(f['destination']).resolve().is_relative_to(mobile) and not Path(f['destination']).resolve().is_relative_to(surfaces[3])}
check('private_Git_exact_6_assets_and_versions',len(private['files'])==6 and {x['path']:x['sha256'] for x in private['files']}==gitrows)
check('no_prior_application_or_build_intent',not any((w/p).exists() for p in ['STATIC_APPLY_INTENT.json','deployment.json','mobile_stage/build34','mobile_stage/COMMIT_INTENT.json','mobile_stage/PUSH_INTENT.json','APK_PUBLICATION_INTENT.json']))
required={'prepare.py','guards.py','transaction.py','maintenance.py','deploy_controlled.py','mobile_release.py','android34.init.gradle','mobile_prepare/build_log.py','mobile_prepare/TOOL_PLAN.json','SCIENCE_BASELINE.json','NATIVE_PLAN.json','INPUT_MANIFEST.json','PRIVATE_GIT_PLAN.json','publish_apk34.py','apply_static.py'}
tools={n:h(w/n) for n in required}
# Confirm required guard set exactly from its AST, not an inferred contract.
guard=ast.parse((w/'guards.py').read_bytes());reqnode=next(x.value for x in ast.walk(guard) if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='required' for t in x.targets));check('guard_toolpin_contract_exact',ast.literal_eval(reqnode)==required)
existing=pin(v/'final_checks.json') if (v/'final_checks.json').exists() else None
base={'passed':True,'status':'PASS_PREINSTALL_INDEPENDENT_REVIEW','reviewer':'codex-gold-reviewer','plan_sha256':planhash,'files':10,'checks':checks,'rows':rows,'pipeline_tests':pin(w.parent/'review/PIPELINE_TESTS.json'),'ui_review':pin(w.parent/'review/UI_REVIEW.json'),'ui_lifecycle':pin(w.parent/'review/TEST_RESULTS_R1.json'),'ui_tests_reused':13,'ui_tests_rerun':False,'git_local_readonly':gitstate,'tool_pins':tools,'science_files':len(science['files']),'original_preparation_checks':existing,'installed':False,'restart_required':False,'network_calls':0,'provider_calls':0,'scope':'Pre-install engineering validation only. Hash reads of current destinations/science/tools; no source, production or Git writes. Remote private visibility not re-queried; explicit authorized original destination and local remote configuration checked.'}
save_new(v/'final_checks.json',base)
review={'status':'PASS','reviewer':'codex-gold-reviewer','reviewer_origin':'Independent reviewer in current task; real review and separate evidence, not created by release author. Actor name is not cryptographic authentication.','plan_sha256':planhash,'transaction_sha256':h(w/'transaction.py'),'maintenance_sha256':h(w/'maintenance.py'),'verifier_sha256':h(w/'verify_final.py'),'tool_pins':tools,'final_checks':pin(v/'final_checks.json'),'review_evidence':[pin(w.parent/'review/UI_REVIEW.json'),pin(w.parent/'review/PIPELINE_TESTS.json'),pin(w.parent/'review/test_pipeline.py')],'checks_passed':len(checks),'pipeline_test_cases':len(pipeline['tests']),'ui_tests_reused':13,'scope':'Reviewed exact10-destination client-only plan, static application entry point, guards, isolated Android build/audit, allowlisted original private Git commit/push, additive APK publishing gate and final read-only verifier. Parent executes. No release acceptance/distribution assertion.','reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'findings':[{'severity':'LOW','blocking':False,'description':'UI forced-colors dark theme residue already documented in UI_REVIEW.json; accepted UI is unchanged.'},{'severity':'LOW','blocking':False,'description':'Static application is atomic per file, not a transaction over10 files; a partial failure leaves explicit STOPPED/INTENT receipts and requires reconciliation without automatic repeat. Parent should verify final installed pins immediately.'}],'constraints':['Use apply_static.py --apply only; deploy_controlled.py retired and maintenance functions not on client-only execution path.','Fresh delivery lease/preflight, target CAS, tool pins and byte backups mandatory at execution.','Build34, private commit/push, APK publication and official iOS39 group availability are subsequent actions with their own receipts/reviews.','APK publishing requires separate mobile_review.json pinned to actual audit and publisher; this report does not fabricate that future review.','No physical installation or remote/model test was performed.','No review of theoretical claims; science preservation checked only by bytes.']}
save_new(v/'review_final.json',review)
print(json.dumps({'status':'PASS','checks':len(checks),'isolated_tests':len(pipeline['tests']),'ui_tests_reused':13,'plan_sha256':planhash,'review_sha256':h(v/'review_final.json'),'final_checks_sha256':h(v/'final_checks.json')}))
