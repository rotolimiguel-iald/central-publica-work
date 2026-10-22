"""Seal C2 candidate evidence after every final local measurement exists."""
from pathlib import Path
import datetime
import json
import sys

WORK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(WORK))
from mission_io import save,pin

freeze=json.loads((WORK/'CORE_R2_SOURCE_FREEZE_R1.json').read_bytes())
assert all(pin(p['path'])==p for p in freeze['files'])
baseline=json.loads((WORK/'CORE_R2_BASELINE_R1.json').read_bytes())
assert all(pin(p['source']['path'])==p['source'] for p in baseline['files'])
test=json.loads((WORK/'tests_core_r2/CORE_R2_TEST_RESULT_R1.json').read_bytes())
growth=json.loads((WORK/'tests_core_r2/GROWTH_RESULTS_FINAL_R1.json').read_bytes())
assert test['status']=='PASS' and test['tests_run']==70
assert {(r['turns'],r['reviewed_fixture']) for r in growth['rows']}=={(n,b) for n in (1,10,100) for b in (False,True)}
assert growth['source']==pin(WORK/'staging/core_r2/lib/iald_memory/activity.py')
for row in growth['rows']:assert pin(row['snapshot']['path'])==row['snapshot']
artifact_names=['CORE_R2_SOURCE_FREEZE_R1.json','CORE_R2_BASELINE_R1.json','C2_BUILD_HANDOFF_R1.json',
    'ACTIVITY_API_R1.txt','ACTIVITY_API_C2_R1.txt','tests_core_r2/CORE_R2_TEST_RESULT_R1.json',
    'tests_core_r2/CORE_R2_TEST_LOG_R1.txt','tests_core_r2/GROWTH_RESULTS_FINAL_R1.json',
    'tests_core_r2/APP_ROUTING_MEASUREMENT_FINAL_R1.json','tests_core_r2/APP_OBSERVED_FINAL_R1.json',
    'tests_app/APP_PROJECTION_GROWTH_FINDING_R1.json','tests_app/JEV_REAL_C2_MEASUREMENT_R1.json',
    'tests_core_r2/measure_final.py','tests_core_r2/measure_app_final.py','tests_core_r2/build_delivery.py']
report={'schema':'organism-core-projection-delivery/v1','unit':'F9.MEMORIA_ORGANISMO_20261016',
    'requirement':'C2','reference':str(WORK/'SESSION_REFERENCE.json'),
    'author':'codex-organism-core-projection-build','status':'CANDIDATE_TESTED_REQUIRES_INDEPENDENT_REVIEW',
    'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'source_tree':str(WORK/'staging/core_r2'),'files':freeze['files'],'evidence':[pin(WORK/p) for p in artifact_names],
    'scope':['Only existing project changed plus a private index helper; other public APIs and original core remain unchanged.',
        'Terminal request/intent receipts are indexed only after exact schema, artifact, admission, command, submitter/epoch, final custody and completed runtime handles are verified.',
        'Execution completion is independent of semantic review: review_pending criterion remains active. No autoaccept, authorization or retry is added.',
        'Commands, facts, scientific content, errata/corrections, criteria, note/evidence/review_evidence remain integral. Unknown/uncertain/conflicting execution stays complete or refuses visibly.',
        'Text avoids duplicate objective/constraints/flow; structured activity API remains full. Candidate result retrieval policy is unchanged.',
        'recover/get retain complete current records. Revision/state hash/digests distinguish current recovery from journal history.',
        'Combined overflow minimum is exact, even when the mission suffix alone exceeds the requested budget.'],
    'tests':{'passed':70,'failed':0,'regression':52,'new':18,'private_stores_only':True},
    'measurements':growth['rows'],
    'integration':{'current_binding_10_turns_5_tools':'PASS local real functions; synthetic science/contract; no human review required',
        'actual_JEV_contract':'1 admitted, 10 and 100 refused under existing local 30000-byte policy; source tests_app/JEV_REAL_C2_MEASUREMENT_R1.json. Admission policy is separate requirement J.',
        'no_claim_of_old_jev_window_sufficiency':True},
    'limitations':['100 genuine commands/criteria exceed24k even after mechanical indexing; no mandatory state is truncated.',
        'Review fixtures use explicitly simulated independent actors. They are not claims of human approval.',
        'Latency reported is a local measurement; 100-entry full integrity checks cost more than 1/10 and are not a low-latency guarantee.',
        'No production install, provider call, permission change, autoaccept or retry. V/D remain separate.'],
    'original_core_unchanged':True,'providers_called':0,'production_installed':False,'requirement_satisfied_by_author':False}
save(WORK/'CORE_C2_DELIVERY_R1.json',report)
print(json.dumps(pin(WORK/'CORE_C2_DELIVERY_R1.json')))
