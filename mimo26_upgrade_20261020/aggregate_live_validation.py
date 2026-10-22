"""Aggregate existing evidence only. No runtime writes, HTTP or new model calls."""
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
from pathlib import Path

W=Path(__file__).resolve().parent;L=W/'live_stage';R=Path('C:/IALD/projetos_pyhton/IALD')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_bytes())
out=W/'live_validation.json'
assert not out.exists(),'Existing live validation preserved; create a separately named revision'
cost=read(L/'FOUR_CALLS_COST.json')
results={name:read(L/(name+'_RESULT.json')) for name in ('IMAGE','AUDIO','VIDEO','AUDIO_POST')}
tests=[]
for name,result in results.items():
    path=L/(name+'_RESULT.json')
    assert sha(path)==cost['sources'][path.name]
    assert result['job']['status']=='completed' and result['done'] and not result['terminal_warnings']
    assert result['acom']['state_hash_verified'] and result['acom']['response_matches_events']
    assert result['model_real']=='mimo-v2.6-pro'
    handles=[h for h in result['acom']['activity_handles'] if h.get('kind')=='activity_operation']
    assert handles and all(h['status']=='completed' for h in handles)
    tests.append({'test':name,'job_id':result['job']['id'],'conversation_id':result['job']['conversation_id'],
        'transport_status':'PASS','task_outcome':'PERCEPTION_FAILURE_RECORDED' if name=='AUDIO' else 'EXPECTED_RESPONSE_OBSERVED',
        'provider':result['provider_real'],'model':result['model_real'],'response_text':result['text'],
        'duration_seconds':result['duration_seconds'],'warnings':result['terminal_warnings'],
        'usage':result['usage'],'known_cost_estimate_usd':cost['jobs'][name]['known_cost_estimate_usd'],
        'custody_verified':True,'activity_operations_completed':len(handles),'semantic_acceptance_inferred':False,
        'evidence':{'path':str(path),'sha256':sha(path)}})
baseline=read(W/'SCIENCE_BASELINE.json');science=[]
for item in baseline['files']:
    path=Path(item['path']);actual=sha(path);assert actual==item['sha256']
    assert path.stat().st_size==item['bytes']
    science.append({'role':item['role'],'path':str(path),'sha256':actual,'bytes':path.stat().st_size,'matches_baseline':True})
post=results['AUDIO_POST']['post_install_verification']
prefix=R/'.iald_runtime/haiku/prefix.md'
assert sha(prefix)==post['runtime_science_sha256']==read(L/'AUDIO_OFFLINE_REPLAY.json')['scientific_prefix_sha256']
provider=R/'iald_app_providers.py';assert sha(provider)==post['installed_provider_sha256']
deployment=read(W/'audio_followup/deployment.json')
assert sha(provider)==deployment['files'][str(provider)]
assert sha(W/'audio_followup/install_plan.json')==deployment['plan_sha256']

android_path=W/'mobile_stage/ANDROID29_AUTHENTICATED_DOWNLOAD.json';android=read(android_path)
assert android['status']=='PASS' and android['authenticated_browser_download'] is True
apk=Path(android['path']);assert sha(apk)==android['sha256'] and apk.stat().st_size==android['bytes']
ios_path=W/'mobile_stage/IOS34_DISTRIBUTION.json';ios=read(ios_path)
assert ios['status']=='IOS34_BOTH_GROUPS_IN_TESTING'
for item in ios['evidence']:assert sha(Path(item['path']))==item['sha256']
amount=sum(Decimal(cost['jobs'][name]['known_cost_estimate_usd']) for name in results)
assert str(amount)==cost['known_cost_estimate_usd']
report={'schema':'iald.mimo26.live-validation/v1','status':'PASS_WITH_RECORDED_INITIAL_AUDIO_FAILURE',
    'passed':True,'passed_scope':'Four terminal transports and custody verified; image/video/post-guidance audio expected responses observed. Original audio perception failure remains recorded. Not universal model accuracy or causal confirmation.',
    'generated_utc':datetime.now(timezone.utc).isoformat(),'tests':tests,
    'costs':{'known_estimate_usd':str(amount),'test_count':4,'components':'MiMo measured token usage at configured rates plus exact-job linked JEV estimate','scope':cost['cost_scope'],'evidence':{'path':str(L/'FOUR_CALLS_COST.json'),'sha256':sha(L/'FOUR_CALLS_COST.json')}},
    'science':{'release':baseline['release'],'baseline_files_verified':science,'complete_prefix_sha256':sha(prefix),'complete_prefix_unchanged':True,'post_job_metric_memory_sha256':results['AUDIO_POST']['metric_memory_sha256'],'kernel_or_gate_changed':False},
    'installed_followup':{'provider_sha256':sha(provider),'matches_deployment_and_one_file_plan':True,'same_audio_and_question_verified':post['same_audio_and_question_objective_bytes'],'restart_receipt':str(W/'audio_followup/restart.json'),'restart_receipt_sha256':sha(W/'audio_followup/restart.json'),'new_web_pid_from_receipt':post['restart_receipt_new_web_pid'],'causal_effect_measured':False},
    'mobile':{'android':{'status':'AUTHENTICATED_DOWNLOAD_HASH_VERIFIED','receipt':str(android_path),'receipt_sha256':sha(android_path),'version':'4.1(29)','apk_bytes':apk.stat().st_size,'apk_sha256':sha(apk),'physical_installation_verified':False},
        'ios':{'status':ios['status'],'version':ios['version'],'groups':ios['groups'],'receipt':str(ios_path),'receipt_sha256':sha(ios_path),'evidence_hashes_verified_locally':True,'fresh_apple_session_inspected_here':False,'physical_installation_verified':False}},
    'limitations':['Original audio job completed transport but did not identify tone; preserved in its original receipt.',
        'Post-guidance same audio/question produced expected tone answer; uncontrolled comparison, no causal attribution.',
        'Offline replay used original media and installed functions; full historical outbound request bytes were not archived.',
        'Metric linkage uses job-scoped ACOM response wire model/usage plus time interval, not direct metric job foreign key.',
        'Costs are estimates, not invoice; moderation/other overhead not independently totalled.',
        'ACOM operations completed and custody verified; no automatic semantic review/acceptance inferred.',
        'Browser/device multimedia compatibility and installed mobile app not verified by this aggregate.',
        'Android authenticated download and Apple distribution are supported by pre-existing receipts; no remote UI session used here.',
        'No native MiMo image/video generation or hosted Python capability claimed.'],
    'aggregate_action':{'local_read_only_runtime':True,'new_provider_calls':0,'new_remote_calls':0,'retries':0,'production_writes':0,'historical_receipts_overwritten':False},
    'task_reference':str(W/'SESSION_REFERENCE.json')}
temp=out.with_suffix('.json.tmp')
with temp.open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
assert read(temp)['costs']['known_estimate_usd']==str(amount)
temp.rename(out)
print(json.dumps({'path':str(out),'sha256':sha(out),'tests':len(tests),'known_cost_estimate_usd':str(amount),'science_files_verified':len(science),'android_download_hash_verified':True,'status':report['status']},ensure_ascii=False))
