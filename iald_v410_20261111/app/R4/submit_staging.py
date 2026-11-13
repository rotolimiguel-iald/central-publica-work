"""Submit final staging evidence under the builder's existing lease; no acceptance."""
from pathlib import Path
import hashlib,json,sys
S=Path(__file__).resolve().parent;W=S.parent.parent;sys.path.insert(0,str(W));import task
assert task.check('app',actor='v410_builder')['ready']
paths=[W/'install_plan.json',W/'RUNTIME_DELTA_R4.json',S/'release_final/release.json',S/'SNAPSHOT_TESTS_FINAL.json',S/'NATIVE_FINAL_COUNT.json',S/'SHARED_ADMISSION_FINAL.json',S/'CLAUDE_TRANSPORT_BOUNDED_TEST_R1.json',S/'BOUNDED_GUARD_TESTS_R1.json',S/'RUNTIME_SYNTAX_FINAL.json',S/'CONTINUOUS_UPDATE_FILES.json']
paths += sorted((S/'certificates_final').rglob('*_result.json'))+sorted((S/'certificates_final').rglob('manifest.json'))
pins=[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in paths]
report={'status':'STAGED_READY_FOR_INDEPENDENT_REVIEW','builder':'v410_builder','reference':str(task.REF),'source_documents':15,'operational_documents':2,'private_queue_source_excluded':'DA_IRMA: not found in pinned public commit','scope':'Whole admitted public corpus retained; bounded fixed core plus per-call partial version-pinned retrieval; no deployment or generation.','limitations':['Native 32768 window remains; standard output4096, thinking8192 may refuse when required context exceeds window.','Kimi has local pre-retrieval and explicit subsequent-turn paging; no interactive tools during its stream.','Lexical retrieval is partial and zero matches do not establish absence; response quality and physical devices not tested.','Future updates stop at independent review pending unless a distinct authorized reviewer supplies bound evidence; no automatic semantic acceptance.'],'artifacts':pins}
path=S/'BUILDER_DELIVERY_R4.json';task.new('app/R4/BUILDER_DELIVERY_R4.json',report)
p=task.project();t=next(x for x in p['projection']['active'] if x['id']=='app')
r=task.act('submit',actor='v410_builder',task_id='app',lease_id=t['lease']['id'],evidence=[{'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}],event_id='v410-app-bounded-corpus-staging-submit-r4')
task.new('APP_STAGING_SUBMITTED_R4.json',r);print(json.dumps(r['receipt']))
