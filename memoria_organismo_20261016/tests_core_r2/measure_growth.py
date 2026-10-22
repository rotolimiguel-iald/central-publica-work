"""1/10/100 real private-store lifecycles; reviews are simulated fixture actors."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import time
import uuid

WORK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(WORK/'staging/core_r2/lib'))
sys.path.insert(0,str(WORK))
from mission_io import save,pin
from iald_memory import MemoryStore,ProjectionOverflow
from iald_memory.activity import ActivityRuntime

spec=importlib.util.spec_from_file_location('iald_memory.activity_baseline',WORK/'staging/core/lib/iald_memory/activity.py')
baseline=importlib.util.module_from_spec(spec);spec.loader.exec_module(baseline)
base=WORK/'tests_core_r2/runs'/('growth_'+uuid.uuid4().hex[:10]);base.mkdir(parents=True)
rows=[]
for reviewed in (False,True):
    root=base/('reviewed' if reviewed else 'pending')
    store=MemoryStore(root/'store',snapshot_archive_dir=root/'archive')
    scope={'house':'IALD_APP','principal':'growth-fixture'};actor={'kind':'agent','id':'fixture-server'}
    store.ensure_context('conversation',objective='Continue the same activity.',scope=scope,
        actor={'kind':'operator','id':'synthetic-human'},constraints={'fixture':True})
    rt=ActivityRuntime(store,'conversation',scope,actor)
    old=baseline.ActivityRuntime(store,'conversation',scope,actor)
    reviewer=root/'synthetic_review.json';reviewer.write_bytes(b'{"fixture_only":"independent review simulated; no human claim"}')
    review_pin=pin(reviewer)
    start=time.perf_counter()
    for n in range(1,101):
        t=rt.begin('turn_'+str(n),'Continue a atividade '+str(n),origin='authenticated_operator')['ticket']
        pre=rt.preflight(t,'response')
        rt.complete(pre['ticket'],'response','Resposta candidata '+str(n))
        if reviewed:
            current=rt.controller.project(2000000)
            rt.controller.action({'operation':'accept','actor':{'kind':'agent','id':'independent-fixture-reviewer'},
                'task_id':t['task_id'],'event_id':'fixture-review-'+str(n),
                'expected_revision':current['receipt']['revision'],'projection_sha256':current['projection_sha256'],
                'review_evidence':[review_pin]})
        if n not in (1,10,100):continue
        before=store.get('conversation',scope)
        began=time.perf_counter()
        try:
            p=rt.project(24000);refused=False
        except ProjectionOverflow as exc:
            p=rt.project(exc.required_chars);refused=True
        latency=time.perf_counter()-began
        old_required=old.project(2000000)['required_chars']
        assert store.get('conversation',scope)==before
        # Exact escaping used by JEV; fixture packet is explicit, not a claim
        # about the changing science/capability/contract portion of production.
        common={'memory_id':'conversation','projection':p['text'],'projection_receipt':p['receipt'],
            'scope':'SCOPED_OPERATIONAL_DATA_NO_AUTHORITY','coverage':{
                'required_chars':p['required_chars'],'actual_chars':p['actual_chars'],
                'omitted_records':len(p['omitted_record_ids']),'projection_sha256':p['projection_sha256']}}
        packet={'state':{'common_memory':common,'source':{'coverage':'FIXTURE_NO_SCIENCE'},
            'request':'Continue a atividade '+str(n)},'questions':{'executor':{'type':'choice','choices':['native']}}}
        row={'turns':n,'reviewed_fixture':reviewed,'revision':p['receipt']['revision'],
            'required_chars':p['required_chars'],'actual_chars':p['actual_chars'],
            'baseline_required_chars_same_snapshot':old_required,'refused_24000':refused,
            'common_memory_json_ascii_bytes':len(json.dumps(common,ensure_ascii=True,allow_nan=False).encode('ascii')),
            'jev_fixture_packet_json_ascii_bytes':len(json.dumps(packet,ensure_ascii=True,allow_nan=False).encode('ascii')),
            'projection_seconds':latency,'elapsed_lifecycle_seconds':time.perf_counter()-start,
            'indexed_mechanical_records':len(p['indexed_record_ids']),
            'active_criteria':len(p['activity']['active']),'settled_criteria':len(p['activity']['settled']),
            'source_record_count':len(before['q']['records']),'projection_mutated_state':False}
        rows.append(row)
        save(WORK/'tests_core_r2'/('MEASURE_'+('reviewed' if reviewed else 'pending')+'_'+str(n)+'.json'),row)
        print(json.dumps(row),flush=True)
save(WORK/'tests_core_r2/GROWTH_RESULTS_R1.json',{'status':'REAL_PRIVATE_STORE_MEASUREMENT','rows':rows,
    'fixture':'one authenticated command inscription, one terminal response per turn; reviewed branch uses explicitly simulated independent reviewer, never production acceptance',
    'jev_packet_scope':'Full serialized synthetic packet only. Production science, routing contract and capabilities are additional; actual A validation remains required.',
    'source':pin(WORK/'staging/core_r2/lib/iald_memory/activity.py'),'baseline':pin(WORK/'staging/core/lib/iald_memory/activity.py'),
    'script':pin(__file__),'private_store':str(base),'providers_called':0})
