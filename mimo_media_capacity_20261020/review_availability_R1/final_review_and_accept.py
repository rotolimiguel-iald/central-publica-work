import hashlib,json,sys
from pathlib import Path
W=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(W));import task
ACTOR='codex-mimo-capacity-reviewer'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=sha(p))
def save(path,d):
    data=json.dumps(d,ensure_ascii=False,indent=2).encode();temp=path.with_suffix(path.suffix+'.tmp')
    assert not path.exists() and not temp.exists()
    with temp.open('xb') as f:f.write(data)
    assert temp.read_bytes()==data;temp.replace(path);assert path.read_bytes()==data
current=task.project();deploy=next(t for t in current['projection']['active'] if t['id']=='deploy')
assert deploy['status']=='review_pending' and deploy['submitted_by']!=ACTOR
assert deploy['criterion']=='Revisão distinta, instalação controlada, testes proporcionais e distribuição coordenada web/iOS/Android.'
submitted=json.loads((W/'DEPLOY_SUBMITTED_RFINAL.json').read_bytes())
assert submitted['receipt']['revision']==current['receipt']['revision']
for e in deploy['evidence']:
    assert sha(e['path'])==e['sha256']
delivery=json.loads((W/'delivery.json').read_bytes());delivery_hash=sha(W/'delivery.json')
assert delivery['status']=='ENGINEERING_DEPLOYED_WITH_DOCUMENTED_PROVIDER_LIMITS'
assert delivery['final_mission_acceptance'] is False
assert delivery['additional_paid_test']=='PENDING_EXPLICIT_USER_REPLY_UP_TO_USD0.50'
for e in delivery['sources']:
    assert sha(e['path'])==e['sha256']
    if 'bytes' in e:assert Path(e['path']).stat().st_size==e['bytes']
assert delivery['availability']==json.loads((W/'AVAILABILITY_MATRIX.json').read_bytes())
runtime=json.loads((W/'FINAL_RUNTIME_PINS_R8.json').read_bytes());science=json.loads((W/'SCIENCE_BASELINE.json').read_bytes())
assert len(runtime['files'])==19 and len(science['files'])==5
for r in runtime['files']+science['files']:assert sha(r['path'])==r['sha256']
# Verify every current memory output against immediate original backup and reviewed suffix.
H=W/'memory_stage/FINAL_R4';plan=json.loads((H/'PLAN.json').read_bytes());applied=json.loads((H/'APPLIED.json').read_bytes())
assert applied['plan_sha256']==sha(H/'PLAN.json')
rows={r['path']:r for r in applied['applied']};assert len(rows)==8
for r in plan['surfaces']:
    record=rows[r['path']];backup=Path(record['backup']);target=Path(r['path']);suffix=Path(r['append']['path'])
    assert backup.parent==target.parent and sha(backup)==r['before_sha256']
    assert sha(target)==r['expected_after_sha256']==record['after_sha256']
    assert target.read_bytes()==backup.read_bytes()+suffix.read_bytes()
for e in plan['sources']['sources']:assert sha(e['path'])==e['sha256']
assert len(plan['sources']['sources'])==59
assert sha(plan['index_policy']['path'])==plan['index_policy']['sha256']
pending=json.loads((W/'extra_test_pending_unit.json').read_bytes());assert pending[0]['status']=='AGUARDA_OPERADOR'
audio=json.loads((W/'live_stage/MANUAL_AUDIO_RESULT.json').read_bytes());video=json.loads((W/'live_stage/MANUAL_VIDEO_RESULT.json').read_bytes());ui=json.loads((W/'WEB_LIVE_SCOPE.json').read_bytes())
assert audio['job']['status']=='completed' and 'Não consigo perceber' in audio['text']
assert video['cost_status']=='ESTIMATED_CAP_NOT_PROVIDER_MEASURED_OR_INVOICE'
assert ui['new_conversation_opens'] is True and ui['automatic_post_fix_provider_test']=='PENDING_USER_EXTRA_TEST_DECISION'
android_plan=json.loads((W/'mobile_stage/apk30_publication/FINAL_R3/APK30_ADDITIVE_PUBLICATION_PLAN_FINAL_R3.json').read_bytes())
for e in android_plan['preserve_existing_apks']:assert sha(e['path'])==e['sha256']
auth=json.loads((W/'mobile_stage/ANDROID30_AUTHENTICATED_DOWNLOAD.json').read_bytes())
assert sha(auth['path'])==sha(android_plan['destination'])==android_plan['source']['sha256']
anon=json.loads((W/'mobile_stage/ANDROID30_ANONYMOUS_DOWNLOAD.json').read_bytes());assert all(x['apk_bytes_delivered']==0 for x in anon['checks'])
ios=json.loads((W/'mobile_stage/IOS35_DISTRIBUTION.json').read_bytes())
for e in ios['sources']:assert sha(e['path'])==e['sha256']
assert len(ios['groups'])==2 and all(r['status']=='Em testes' for r in ios['groups']) and ios['physical_installation_verified'] is False
previous=[W/'REVIEW_DISTRIBUTION_POSTPUBLICATION_R1.json',W/'REVIEW_MEMORY_APPLIED_R4.json',W/'mobile_stage/apk30_publication/FINAL_R3/REVIEW_TECHNICAL_GO_R3.json',H/'REVIEW_MEMORY_8_SURFACES_R4.json']
report=dict(status='PASS',verdict='ENGINEERING_DEPLOYED_WITH_DOCUMENTED_PROVIDER_LIMITS',actor=ACTOR,reference=str(W/'SESSION_REFERENCE.json'),reviewed_revision=current['receipt']['revision'],criterion=deploy['criterion'],review_scope='Independent final documentary/hash verification of the submitted engineering deployment, proportional tests and coordinated distribution; no full vendor perception guarantee.',delivery=pin(W/'delivery.json'),submission=pin(W/'DEPLOY_SUBMITTED_RFINAL.json'),submitted_evidence=deploy['evidence'],prior_independent_reviews=[pin(p) for p in previous],checks=dict(actual_submission_and_distinct_reviewer=True,immutable_delivery_and_all_source_pins=True,current_runtime19_and_science5=True,controlled_install_reviews_and_receipts_previously_verified=True,proportional_offline_and_live_negative_test_results_preserved=True,android30_published_authenticated_hash_and15old_apks=True,anonymous_receipts_zero_apk_bytes=True,ios35_cloud_both_groups_and_operator_documented=True,memory8_exact_backup_plus_append_and59sources=True,index_unchanged=True,extra050_awaiting_operator_no_authorization_inferred=True),findings=[],
    criterion_reason='The actual criterion requires reviewed controlled installation, proportional testing and coordinated web/iOS/Android distribution. Submitted immutable evidence establishes those engineering/distribution acts and records failed/uncertain provider outcomes without representing them as full perception PASS. The optional paid follow-up remains a separate pending human decision; it is not silently authorized by accepting this bounded deploy requirement.',
    residual_limits=['Audio120s transport completed but perception failed; larger-media perception generally unvalidated.','Video30s failed/uncertain; no retry, complete provider usage unknown, reserved-cap estimate not invoice.','Completed job versus cancelled wallet-task discrepancy remains an unresolved bookkeeping diagnostic.','No new post-fix automatic provider test was performed; extra USD0.50 remains AGUARDA_OPERADOR with no human answer.','Apple reports installed35; physical iOS/Android tests not verified; GooglePlay not published.','Acceptance covers deploy requirement only; no claim of all functionality, full mission tetelestai, scientific confirmation or resolution of uncertain remote operations.'],
    actions=dict(new_provider_calls=0,new_network_requests=0,production_writes=False,delivery_modified=False))
save(W/'FINAL_REVIEW.json',report)
# Controller reprojects immediately and applies fresh CAS with the real independent actor.
accepted=task.act('accept',actor=ACTOR,task_id='deploy',review_evidence=[pin(W/'FINAL_REVIEW.json')],event_id='media-capacity-independent-deploy-accept-rfinal')
save(W/'DEPLOY_ACCEPTED_RFINAL.json',accepted)
assert sha(W/'delivery.json')==delivery_hash
after=task.project()
save(W/'FINAL_ACCEPTANCE_PROJECT.json',after)
print(json.dumps(dict(receipt=str(W/'DEPLOY_ACCEPTED_RFINAL.json'),acceptance=accepted.get('task'),revision=accepted.get('receipt',{}).get('revision'),delivery_unchanged=True),ensure_ascii=False))
