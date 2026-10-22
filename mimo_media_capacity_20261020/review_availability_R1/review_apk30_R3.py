import copy,hashlib,importlib.util,io,json,shutil,subprocess,sys,unittest
from pathlib import Path
W=Path(__file__).resolve().parent.parent;H=W/'mobile_stage/apk30_publication/FINAL_R3';O=W/'review_apk30_R3';O.mkdir(exist_ok=False)
sys.path.insert(0,str(W));import task
current=task.project()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=sha(p),bytes=Path(p).stat().st_size)
def save(p,d):
    raw=json.dumps(d,ensure_ascii=False,indent=2).encode();tmp=p.with_suffix(p.suffix+'.tmp')
    assert not p.exists()
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.replace(p)
P=H/'APK30_ADDITIVE_PUBLICATION_PLAN_FINAL_R3.json';plan=json.loads(P.read_bytes());relay=json.loads((H/'PLANCK_FINAL_SHORT_RELAY.json').read_bytes())
for key in ('plan','candidate','tests','preview'):
    e=relay[key];assert sha(e['path'])==e['sha256']
for e in [plan['source'],plan['result'],plan['archive_audit'],plan['candidate'],plan['endpoint_source']['pin'],*plan['source_pins'],*plan['preserve_existing_apks']]:
    assert sha(e['path'])==e['sha256']
old=json.loads((W/'mobile_stage/apk30_publication/FINAL_R2/APK30_ADDITIVE_PUBLICATION_PLAN_FINAL_R2.json').read_bytes())
for k in ('source','result','archive_audit','destination','preserve_existing_apks','certificate_sha256'):assert plan[k]==old[k]
assert plan['endpoint_source']['path']=='/downloads/IALD-4.1-30.apk'
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
pub=load('publish_apk30',H/'publish_apk30.py')
assert pub.WORK==W and pub.REFERENCE==W/'SESSION_REFERENCE.json'
pub.verify_plan(plan) # Entire current artifact, signature, endpoint and15APK proof; no writes.
pub.HERE=O
tests=load('review_apk30_test_publisher',H/'test_publisher.py');log=io.StringIO()
result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(tests))
assert result.wasSuccessful() and result.testsRun==6
save(O/'REPLAY.json',dict(passed=True,tests=result.testsRun,log=log.getvalue(),fixture_writes_only=True,production_writes=False))
# Authorization controls stay fully synthetic/in memory; no GO receipt is created.
review=dict(actor=plan['reviewer_actor'],technical_go=True,plan=pin(P),candidate=plan['candidate'],four_checks={k:'PASS' for k in plan['review']['checks_required']},_actual_sha256='a'*64)
go=dict(go=True,actor=pub.OWNER,plan_sha256=sha(P),review_sha256='a'*64,candidate_sha256=plan['candidate']['sha256'],reference=str(pub.REFERENCE))
pub.authorize(review,go,pin(P),plan)
count=0
for key,value in [('go',False),('actor','other'),('plan_sha256','0'*64),('review_sha256','0'*64),('candidate_sha256','0'*64),('reference','other')]:
    bad=dict(go);bad[key]=value
    try:pub.authorize(review,bad,pin(P),plan)
    except RuntimeError:count+=1
    else:raise AssertionError(key)
assert count==6
preview=subprocess.run([sys.executable,'-B','-X','utf8',str(H/'publish_apk30.py')],capture_output=True,check=True)
assert json.loads(preview.stdout)['mode']=='PREVIEW_ONLY'
assert not Path(plan['destination']).exists()
for e in plan['preserve_existing_apks']:assert sha(e['path'])==e['sha256']
save(O/'OWN_CONTROLS.json',dict(passed=True,authorization_mismatch_refusals=6,preview=json.loads(preview.stdout),source_and15old_apks_rechecked=True,endpoint_pin_current=True,no_publication=True))
report=dict(status='PASS',technical_go=True,phase='TECHNICAL_PUBLICATION_GO_HTTP_AFTER_PUBLICATION',final_delivery='FINAL_DELIVERY_NOT_ACCEPTED',actor='codex-mimo-capacity-reviewer',reference=str(W/'SESSION_REFERENCE.json'),reviewed_revision=current['receipt']['revision'],plan=pin(P),candidate=plan['candidate'],four_checks={k:'PASS' for k in plan['review']['checks_required']},findings=[],resolved_findings=['APK30_EXECUTABLE_NOT_BOUND','STALE_ENDPOINT_SOURCE_METADATA'],tests_replayed=6,own_authorization_negative_controls=6,existing_apks_verified=15,source=plan['source'],endpoint=plan['endpoint_source'],evidence=[pin(O/'REPLAY.json'),pin(O/'OWN_CONTROLS.json'),pin(Path(__file__))],
    four_checks_scope={'artifact_result_audit_certificate_pins':'Current source/result/audit pins and unchanged signature-continuity evidence verified; prior R2 artifact review reused.','single_target_additive_all_existing_apks_preserved':'Exact APK30 target absent, all15 older APKs hash checked, nonreplacement Windows rename and exclusive intent replayed only in temporary fixtures.','authenticated_route_anonymous_zero_apk_bytes':'Exact current auth/download AST offline: anonymous redirect delivers zero APK bytes; authenticated fixture permitted. Actual HTTP30 follows publication.','fresh_owner_preflight_go_and_no_repeat_atomic_create':'Executable reviewed; own exact mission/current owner lease/revision and plan-review-candidate GO linkage enforced before intent. Fresh real preflight and owner GO remain execution-time obligations, not fabricated here.'},
    conclusion='Technical approval permits parent/authorized executor to publish the one exact APK30 with this reviewed candidate, explicit owner GO and fresh preflight, THEN verify authenticated download. No requirement to prove download before file publication; no final mission acceptance.',
    limits=['Post-publication authenticated GET must hash to source; anonymous GET with redirects disabled must yield zero APK bytes (302/login HTML allowed).','Existing target or durable prior intent refuses even if identical; reconcile uncertainty without repeating under a new ID.','No APK published, runtime changed, HTTP/model called, or task accepted by reviewer.','iOS35 Cloud SUCCESS/group observations and Apple-reported installed35 are operator reports in this bounded review, not independently inspected here; physical installation not verified.','Provider perception limitations and final coordinated availability matrix remain for final delivery review.'])
save(H/'REVIEW_TECHNICAL_GO_R3.json',report)
save(W/'REVIEW_APK30_PUBLICATION_FINAL_R3.json',report)
print(json.dumps(dict(status='PASS',technical_go=True,tests=6,negative_controls=6,review=pin(H/'REVIEW_TECHNICAL_GO_R3.json'))))
