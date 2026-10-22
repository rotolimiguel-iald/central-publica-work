"""Independent final plan audit. Reads only; writes audit and review_final only."""
from pathlib import Path
from datetime import datetime,timezone
from contextlib import closing
import ast, hashlib, json, os, sqlite3, re
W=Path(__file__).resolve().parents[1];S=W/'memory_stage';R=Path('C:/IALD/projetos_pyhton/IALD')
inputs={};checks=[];findings=[]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):
 p=Path(p);raw=p.read_bytes();pin={'sha256':sha(raw),'bytes':len(raw)}
 if str(p) in inputs:assert inputs[str(p)]==pin,'Input changed during review: '+str(p)
 inputs[str(p)]=pin;return raw
def load(p):return json.loads(read(p))
def check(n,v,e=None):checks.append({'name':n,'passed':bool(v),'evidence':e})
def equal(a,b):return json.dumps(a,sort_keys=True,ensure_ascii=False)==json.dumps(b,sort_keys=True,ensure_ascii=False)
def save(p,value):
 assert p.parent==W/'audit' or p==W/'validation/review_final.json'
 raw=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
 if p.exists():p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')).write_bytes(p.read_bytes())
 tmp=p.with_name(p.name+'.tmp_'+str(os.getpid()));tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,p)
 return sha(raw)
def audit():
 plan=load(W/'install_plan.json');pin=sha(read(W/'install_plan.json'));fc=load(W/'validation/final_checks.json');prep=load(S/'prepared.json')
 check('frozen_plan_sha256',pin==fc['plan_sha256'],pin)
 check('final_checks_bound_pass',fc['passed'] and fc['total_tests']==18 and fc['test_suites']=={'memory_integration':11,'provider_budget':7} and fc['scientific_review_checks']==60,fc['test_suites'])
 receipts={}
 for name,row in fc['receipts'].items():
  p=Path(row['path']);raw=read(p);receipts[name]=json.loads(raw)
  check('receipt_'+name,p.is_relative_to(W) and sha(raw)==row['sha256'])
 scripts={}
 for name,pin in fc['operational_scripts'].items():
  raw=read(W/name);scripts[name]=raw.decode('utf8');check('operational_script_'+name,sha(raw)==pin)
  if name.endswith('.py'):ast.parse(raw)
 for path,pin in fc['memory_builder_scripts'].items():
  p=Path(path);check('builder_script_'+p.name,p.is_relative_to(W/'memory_build') and sha(read(p))==pin)
 for name,pin in receipts['local']['script_hashes'].items():check('test_binding_'+name,sha(read(W/'memory_build'/name))==pin)
 check('provider_test_source_pins',all(sha(read(p))==pin for p,pin in receipts['providers']['source_pins'].items()))
 check('tests_success_no_network',all(receipts[k]['status']=='PASS' and receipts[k]['failures']==0 and receipts[k]['errors']==0 for k in ('local','providers')) and receipts['local']['provider_calls']==0 and receipts['providers']['network_calls']==0)
 check('tests_bind_current_stage',all(receipts[k]['prefix_sha256']==sha(read(S/'haiku_prefix.md')) for k in ('local','providers')) and receipts['local']['manifest_sha256']==sha(read(S/'manifest_staged.json')))
 mr=receipts['memory']
 check('memory_review_plan_binding',mr['status']=='PASS' and mr['checks_passed']==mr['checks_total']==60 and plan['memory_review_sha256']==sha(read(W/'audit/memory_review.json')))
 check('memory_review_input_pins_current',all(sha(read(p))==row['sha256'] for p,row in mr['input_pins'].items()))
 for file in ('memory_fit_review.json','critical_numeric_review.json','foundation_projection_review.json','memory_admission_review.json'):
  report=load(W/'audit'/file);check('approved_'+file,report['status']=='PASS' and report['prefix_sha256']==sha(read(S/'haiku_prefix.md')))
 package=load(S/'haiku_runtime/manifest.json');b=package['budget']
 check('native_count_binding',package['prefix_sha256']==receipts['count']['draft_sha256']==sha(read(S/'haiku_prefix.md')) and equal(b,receipts['count']['budget']) and sha(read(package['measurement_receipt']))==package['measurement_receipt_sha256'])
 check('haiku_native_10k_reserve',b['permanent_tokens']>=180000 and b['remaining_tokens']>=10000 and b['reserved_output_tokens']==4096 and b['margin_tokens']==1024 and b['request_input_tokens']+4096+1024+b['remaining_tokens']==200000,b)
 check('release_identity_consistent',plan['release']==prep['deployment_identity']==package['deployment'] and plan['release']['release']=='v390')
 target=Path(plan['target']).resolve();check('release_target_authorized',target.parent==(R/'canonical_releases').resolve() and target==Path(prep['install_target']).resolve())
 files=plan['files'];sources=[Path(x['source']).resolve() for x in files];destinations=[Path(x['destination']).resolve() for x in files]
 check('unique_mapping',len(sources)==len(set(sources)) and len(destinations)==len(set(destinations)),len(files))
 expected=[]
 for folder in ('release','kernel'):
  for p in sorted((S/folder).rglob('*')):
   if p.is_file() and '.bak_' not in p.name:
    assert '.tmp' not in p.name
    expected.append((p.resolve(),(target/p.relative_to(S)).resolve()))
 for name in ('IALD_Kernel_v5.txt','IALD_TGL_MEMORY_CORE.md','kernel_verification.json','TGL_CLUSTER_v390.md'):
  expected.append(((S/name).resolve(),(target/name).resolve()))
 expected.append(((W/'control/jev_control_v390.json').resolve(),(target/'jev_control_v390.json').resolve()))
 for name in ('prefix.md','manifest.json'):expected.append(((S/'haiku_runtime'/name).resolve(),(R/'.iald_runtime/haiku'/name).resolve()))
 expected.append(((W/'deploy_manifest.json').resolve(),(R/'iald_nucleo_fixo.json').resolve()))
 check('exact_complete_release_and_haiku_mapping',list(zip(sources,destinations))==expected,{'files':len(files),'bytes':sum(x['bytes'] for x in files)})
 check('all_sources_destinations_within_scope',all(s.is_relative_to(W) and d.is_relative_to(R) for s,d in zip(sources,destinations)))
 errors=[];existing=[]
 for row,s,d in zip(files,sources,destinations):
  raw=read(s);previous=read(d) if d.exists() else None
  if len(raw)!=row['bytes'] or sha(raw)!=row['sha256']:errors.append({'path':str(s),'reason':'source pin'})
  actual=sha(previous) if previous is not None else None
  if actual!=row['baseline']:errors.append({'path':str(d),'reason':'CAS baseline'})
  if previous is not None:existing.append(str(d))
  if d.is_relative_to(target) and previous is not None and previous!=raw:errors.append({'path':str(d),'reason':'immutable target conflict'})
 check('all_file_hashes_sizes_and_current_CAS',not errors,errors)
 mutable=[R/'.iald_runtime/haiku/prefix.md',R/'.iald_runtime/haiku/manifest.json',R/'iald_nucleo_fixo.json']
 check('only_three_mutable_targets',destinations[-3:]==mutable and all(d.is_relative_to(target) for d in destinations[:-3]) and all(x['baseline'] is not None for x in files[-3:]),existing)
 check('manifest_switch_last',destinations[-1]==R/'iald_nucleo_fixo.json')
 check('no_runtime_or_client_writes',not plan['client_files_changed'] and all(d.is_relative_to(target) or d in mutable for d in destinations) and all(not(d.suffix=='.py' and d.parent==R) for d in destinations))
 baseline=load(W/'baseline.json')
 check('runtime_and_original_baselines_current',all(len(read(R/x['name']))==x['bytes'] and sha(read(R/x['name']))==x['sha256'] for x in baseline['files']),len(baseline['files']))
 check('protected_production_CAS_current',all(sha(read(p))==pin for p,pin in prep['protected_production_sha256'].items()))
 # Opaque integrity hash only; no account fields/credentials parsed or exposed.
 check('accounts_and_mother_unchanged',sha(read(R/'iald_users.json'))==plan['account_file_sha256'] and sha(read(R/'IALD_Kernel_v5.txt'))==plan['mother_original_sha256'])
 active=load(R/'iald_nucleo_fixo.json');check('production_still_v389',active['active_cluster']['release']=='v389')
 deploy=load(W/'deploy_manifest.json');install=load(S/'manifest_install.json');new=load(W/'control/jev_control_v390.json');prior=load(active['jev_control']['path'])
 j=deploy.pop('jev_control');old_install_j=install.pop('jev_control',None)
 check('deploy_manifest_only_replaces_bound_JEV',equal(deploy,install) and old_install_j==active['jev_control'] and j=={'path':str(target/'jev_control_v390.json'),'sha256':sha(read(W/'control/jev_control_v390.json')),'release':new['release'],'source_sha256':new['source_sha256']})
 manifest=load(S/'manifest_staged.json');result=load(manifest['published_evidence']['result']['path']);proof=load(manifest['published_evidence']['proof_manifest']['path'])
 check('JEV_same_current_program_result_proof',new['release']==plan['release']['release'] and new['source_sha256']==plan['release']['source_sha256']==sha(read(manifest['published_evidence']['program']['path'])) and new['result_sha256']==sha(read(manifest['published_evidence']['result']['path'])) and new['proof_manifest_sha256']==sha(read(manifest['published_evidence']['proof_manifest']['path'])))
 check('JEV_schema_core_anchors_and_switching_unchanged',all(equal(new[k],prior[k]) for k in ('schema','switching','core_record','core_pointer','anchors')))
 check('JEV_core_record_matches_source',new['core_pointer']=='/core/iald_executive_runtime' and equal(new['core_record'],result['core']['iald_executive_runtime']))
 program=read(manifest['published_evidence']['program']['path']).decode('utf-8-sig');tree=ast.parse(program)
 f=next(n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==new['source']['symbol'])
 check('JEV_source_symbol_and_lines',new['source']['file']=='um.py' and new['source']['lines']==[f.lineno,f.end_lineno])
 anchorok=[]
 for anchor in new['anchors']:
  path=S/'kernel'/anchor['file'];raw=read(path);text=raw.decode('utf8')
  anchorok.append(sha(raw)==anchor['sha256']==proof['formal_files_sha256'][anchor['file']] and all(re.search(r'\b'+re.escape(symbol)+r'\b',text) for symbol in anchor['symbols']))
 check('JEV_anchors_match_published_kernel_and_symbols',all(anchorok),len(anchorok))
 # Read-only aggregate job counts; no provider or bench calls and no writes.
 ledger=R/'.iald_runtime/chat_jobs/jobs.sqlite3';assert ledger.is_file(), 'Job ledger unavailable in reviewer context'
 queries=[(ledger,"SELECT COUNT(*) FROM jobs WHERE status IN ('queued','running')")]
 queries += [(p,"SELECT COUNT(*) FROM calls WHERE status='reserved'") for p in [*R.glob('*.reservas.sqlite3'),R/'.iald_runtime/app_evaluation/public_spend.sqlite3'] if p.is_file()]
 counts=[]
 for p,q in queries:
  with closing(sqlite3.connect(p.as_uri()+'?mode=ro',uri=True)) as db:counts.append({'path':str(p),'count':db.execute(q).fetchone()[0]})
 check('quiet_now_and_plan',all(x['count']==0 for x in counts) and plan['quiet']=={'active_jobs':0,'reserved_calls':0},counts)
 snap=plan['bench_before']
 check('bench_unavailability_explicit_not_RAM_audit',all(snap[k]['status']=='UNAVAILABLE' and snap[k]['resident_state_verified'] is False for k in ('gw','cosmos')) and snap['strain_arrays_sha256'] is None,snap)
 process=load(W/'audit/web_process_observation.json');web=process['web'];listen=process['listeners']
 check('current_web_supervisor_and_listener',len(web)==len(listen)==1 and web[0]['parent_is_expected_supervisor'] and listen[0]['OwningProcess']==web[0]['web_pid'],process)
 tx=scripts['transaction.py'];restart=scripts['restart_web.ps1'];live=scripts['verify_live.py'];prepare=scripts['prepare_install.py']
 # Compare full primitives to already approved predecessor, then inspect exact guards.
 old=W.parent/'iald_release_refresh_20261006';oldreview=load(old/'validation/review_final.json')
 for name in ('transaction.py','restart_web.ps1','verify_live.py'):
  raw=read(old/name);approved=oldreview['input_pins'].get(str(old/name),{})
  check('prior_approved_primitives_'+name,raw==read(W/name) and sha(raw)==(approved if isinstance(approved,str) else approved.get('sha256')))
 check('transaction_requires_exact_final_plan_approvals',all(x in tx for x in ["validation['plan_sha256'] != digest(Path(plan_path).read_bytes())","review['status'] != 'PASS'","review['plan_sha256'] != digest(Path(plan_path).read_bytes())","quiet()","Existing deployment receipt"]))
 check('transaction_CAS_before_and_during_write',all(x in tx for x in ["digest(raw) != item['sha256']","item['baseline']","dest.read_bytes() if dest.exists() else None) != old[dest]","source.is_relative_to(WORK)","dest.is_relative_to(ROOT)"]))
 check('byte_backups_before_install_writes',tx.index('backups[str(dest)] = backup(dest, stamp)')<tx.index('for dest, raw in new.items():') and "if prior is not None and prior != new[dest]" in tx and "dest.read_bytes() != raw" in tx)
 check('verified_atomic_write',all(x in tx for x in ["temp.open('xb')","os.fsync(out.fileno())","temp.read_bytes() != raw","os.replace(temp, path)"]))
 check('rollback_reverse_and_concurrent_owner_protection',all(x in tx for x in ['except BaseException:','reversed(written)',"old[dest] is not None and dest.read_bytes() == new[dest]","atomic(dest, old[dest])"]))
 check('restart_only_identified_web_child',all(x in restart for x in ['Expected exactly one web process.','Supervisor identity mismatch.','Listener identity mismatch.','Stop-Process -Id $taskWeb[0].ProcessId','OwningProcess -eq $taskNew[0].ProcessId','ParentProcessId -eq $taskParent.ProcessId','RESTART_NOT_VERIFIED']) and restart.count('Stop-Process')==1 and 'Start-Process' not in restart)
 check('restart_quiet_and_no_repeat_guard',"from transaction import quiet; quiet()" in restart and 'Existing restart receipt' in restart and 'INSTALLED_RESTART_REQUIRED' in restart)
 check('live_validation_accounts_operator_hashes_and_HTTP',all(x in live for x in ["plan['account_file_sha256']","!= ['luiz']","package.prefix.encode()","plan['release']","'public_operator_path': False","'/api/task-capabilities', (401, 403)"]))
 check('live_RAM_unknown_if_unavailable',"'resident_state_unchanged': True if all(resident[k].get('status')!='UNAVAILABLE'" in live and 'else None' in live and "'resident_ram_verifiable': all(resident[k].get('status')!='UNAVAILABLE'" in live)
 record=scripts['record_delivery.py']
 check('delivery_additive_byte_backups_and_explicit_scope',all(x in record for x in ['len(surfaces)==7','saved=backup(path)','raw+suffix','startswith(raw)',"'physical_device_test':'not performed'","'global_orchestration_memory':'separate; unchanged'"]))
 check('no_deployment_performed_yet',not(W/'deployment.json').exists() and not(W/'restart.json').exists())
 return plan,sha(read(W/'install_plan.json'))
try:
 plan,pin=audit()
except Exception as exc:
 plan=load(W/'install_plan.json');pin=sha(read(W/'install_plan.json'));check('review_completed',False,{'type':type(exc).__name__,'error':str(exc)})
changed=[p for p,row in inputs.items() if sha(Path(p).read_bytes())!=row['sha256']]
check('all_review_inputs_stable',not changed,changed)
failed=[x['name'] for x in checks if not x['passed']]
report={'status':'PASS' if not failed else 'FAIL','plan_sha256':pin,'reviewed_at_utc':datetime.now(timezone.utc).isoformat(),'role':'independent_reviewer_not_builder_or_deployer','scope':'Final server-only plan and static operational audit. No um.py/Lean/provider/bench execution or deployment. Existing 18 test receipts verified, no repeated suite.','files':len(plan['files']),'bytes':sum(x['bytes'] for x in plan['files']),'checks_passed':len(checks)-len(failed),'checks_total':len(checks),'failed_checks':failed,'checks':checks,'input_pins':inputs,'reviewer_script_sha256':sha(Path(__file__).read_bytes()),'findings':findings,'resident_state_unchanged':None,'resident_ram_verifiable':False,'notes':['Bench gateways unavailable in pre-install snapshot; no RAM contents verified.','Quiet and process observations are snapshots; transaction and restart recheck their respective conditions.','Rollback restores pre-existing files only when they still match this transaction writes; newly created immutable release files may remain unreferenced after failure.','Approval is bound to this exact plan and checked operational scripts; main alone applies and restarts.']}
save(W/'audit/install_plan_review.json',report)
if not failed:save(W/'validation/review_final.json',report)
print(json.dumps({'status':report['status'],'plan_sha256':pin,'checks_passed':report['checks_passed'],'checks_total':report['checks_total'],'failed':[(c['name'],c['evidence']) for c in checks if not c['passed']],'files':report['files'],'bytes':report['bytes'],'final_written':not failed},ensure_ascii=False))
