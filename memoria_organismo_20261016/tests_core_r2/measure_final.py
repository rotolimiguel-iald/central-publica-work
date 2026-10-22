"""Final frozen-source measurements; reuse the already executed 100-turn store."""
from pathlib import Path
import importlib.util
import json
import sys
import time
import uuid

WORK=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(WORK/'staging/core_r2/lib'),str(WORK)]
from mission_io import save,pin
from iald_memory import MemoryStore,ProjectionOverflow
from iald_memory.activity import ActivityRuntime
source=pin(WORK/'staging/core_r2/lib/iald_memory/activity.py')
spec=importlib.util.spec_from_file_location('iald_memory.activity_baseline',WORK/'staging/core/lib/iald_memory/activity.py')
baseline=importlib.util.module_from_spec(spec);spec.loader.exec_module(baseline)
scope={'house':'IALD_APP','principal':'growth-fixture'};actor={'kind':'agent','id':'fixture-server'}
rows=[]

def setup(root,create):
    store=MemoryStore(root/'store',snapshot_archive_dir=root/'archive')
    if create:store.ensure_context('conversation',objective='Continue the same activity.',scope=scope,
        actor={'kind':'operator','id':'synthetic-human'},constraints={'fixture':True})
    return ActivityRuntime(store,'conversation',scope,actor)

def accept(rt,task_id,label):
    f=Path(rt.store.root).parent/'review_final_fixture.json'
    if not f.exists():
        with f.open('xb') as out:out.write(b'{"fixture_only":"simulated independent reviewer, no human approval claimed"}')
    p=rt.controller.project(2000000)
    rt.controller.action({'operation':'accept','actor':{'kind':'agent','id':'independent-fixture-reviewer'},
        'task_id':task_id,'event_id':'review-final-'+label,'expected_revision':p['receipt']['revision'],
        'projection_sha256':p['projection_sha256'],'review_evidence':[pin(f)],
        'note':'Fixture reviewer retained scope; not a real human approval.'})

def measure(rt,n,reviewed):
    before=rt._get();started=time.perf_counter()
    try:p=rt.project(24000);refused=False
    except ProjectionOverflow as exc:p=rt.project(exc.required_chars);refused=True
    latency=time.perf_counter()-started
    old=baseline.ActivityRuntime(rt.store,'conversation',scope,actor)
    old_required=old.project(2000000)['required_chars']
    assert before==rt._get()
    content,_=json.JSONDecoder().raw_decode(p['text'][p['text'].index('{'):])
    wire=json.loads(p['text'].split('<IALD_ACTIVITY_V1>\n')[1].split('\n</IALD_ACTIVITY_V1>')[0])
    size=lambda v:len(json.dumps(v,ensure_ascii=True,allow_nan=False).encode('ascii'))
    common={'memory_id':'conversation','projection':p['text'],'projection_receipt':p['receipt'],
        'scope':'SCOPED_OPERATIONAL_DATA_NO_AUTHORITY','coverage':{'required_chars':p['required_chars'],
        'actual_chars':p['actual_chars'],'omitted_records':len(p['omitted_record_ids']),
        'projection_sha256':p['projection_sha256']}}
    packet={'state':{'common_memory':common,'source':{'coverage':'FIXTURE_NO_SCIENCE'},
        'request':'Continue a atividade '+str(n)},'questions':{'executor':{'type':'choice','choices':['native']}}}
    snapshot_path=WORK/'tests_core_r2'/('SNAPSHOT_'+('reviewed' if reviewed else 'pending')+'_'+str(n)+'.json')
    save(snapshot_path,{'snapshot':before,'store_root':str(rt.store.root),'artifact_root':str(rt.artifacts),
        'scope':'Read-only private snapshot. get returns current state; compare revision. Export represents this recorded revision only.',
        'projection_source':source})
    row={'turns':n,'reviewed_fixture':reviewed,'revision':before['revision'],
        'required_chars':p['required_chars'],'actual_chars':p['actual_chars'],
        'baseline_required_chars_same_snapshot':old_required,'refused_24000':refused,
        'common_memory_json_ascii_bytes':size(common),'jev_fixture_packet_json_ascii_bytes':size(packet),
        'projection_seconds_including_exact_overflow_resize':latency,'indexed_records':len(p['indexed_record_ids']),
        'active_criteria':len(p['activity']['active']),'settled_criteria':len(p['activity']['settled']),
        'mandatory_record_count':len(p['required_record_ids']),'state_unchanged':True,'snapshot':pin(snapshot_path),
        'component_json_ascii_bytes':{'content_records':size(content['records']),'active_criteria':size(wire['active']),
            'settled_criteria':size(wire['settled']),'execution_index':size(wire['terminal_execution_index'])}}
    rows.append(row);print(json.dumps(row),flush=True)

# The preliminary source only changed project(); begin/complete/store bytes are
# unchanged. Reuse the already completed real lifecycle, avoiding 100 duplicate
# local fixture admissions. No external call occurred in either generation.
candidates=list((WORK/'tests_core_r2/runs').glob('growth_*/pending/store/memory.sqlite3'))
assert len(candidates)==1,candidates
hundred=setup(candidates[0].parent.parent,False)
assert len(hundred._mission(hundred._get())['projection']['active'])==100
measure(hundred,100,False)
newroot=WORK/'tests_core_r2/runs'/('final_'+uuid.uuid4().hex[:10])
for reviewed in (False,True):
    rt=setup(newroot/('reviewed' if reviewed else 'pending'),True)
    for n in range(1,11):
        t=rt.begin('turn_'+str(n),'Continue a atividade '+str(n),origin='authenticated_operator')['ticket']
        pre=rt.preflight(t,'response');rt.complete(pre['ticket'],'response','Resposta candidata '+str(n))
        if reviewed:accept(rt,t['task_id'],str(n))
        if n in (1,10):measure(rt,n,reviewed)
for n,task in enumerate(list(hundred._mission(hundred._get())['projection']['active'])):
    accept(hundred,task['id'],str(n))
measure(hundred,100,True)
assert pin(source['path'])==source
save(WORK/'tests_core_r2/GROWTH_RESULTS_FINAL_R1.json',{'status':'REAL_PRIVATE_STORE_MEASUREMENT',
    'source':source,'script':pin(__file__),'rows':sorted(rows,key=lambda r:(r['reviewed_fixture'],r['turns'])),
    'scope':'One authenticatable command per turn in a private fixture. Semantic reviewer is simulated, not a human or production acceptance. JSON packet has synthetic routing fields; actual app admission measured separately.',
    'prior_attempt':'measure_growth.py built 100 real pending turns and exposed inherited lower-bound overflow counting; final project corrects exact required size. No earlier row or source pin is used as final measurement.',
    'providers_called':0,'production_modified':False})
