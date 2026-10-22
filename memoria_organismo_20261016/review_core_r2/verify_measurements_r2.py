"""Reproject the six pinned recorded snapshots; no historical get or new turns."""
import copy,hashlib,importlib.util,json,sys,time
from pathlib import Path
R=Path(__file__).resolve().parent;W=R.parent;sys.path[:0]=[str(W/'staging/core_r2/lib'),str(W)]
from mission_io import save,pin
from iald_memory import MemoryStore,ProjectionOverflow
from iald_memory.activity import ActivityRuntime,KEY
from iald_memory.mission import digest,is_mission_record
measurement=W/'tests_core_r2/GROWTH_RESULTS_FINAL_R1.json';m=json.loads(measurement.read_bytes())
assert pin(m['source']['path'])==m['source']
spec=importlib.util.spec_from_file_location('iald_memory.activity_review_baseline',W/'staging/core/lib/iald_memory/activity.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
class SnapshotView:
    project_snapshot=MemoryStore.project_snapshot
    def __init__(self,export):self.snapshot=export['snapshot'];self.root=Path(export['store_root'])
    def get(self,cid,scope):
        assert cid==self.snapshot['context_id'] and scope==self.snapshot['scope']
        return copy.deepcopy(self.snapshot)
rows=[]
for item in m['rows']:
    assert pin(item['snapshot']['path'])==item['snapshot']
    export=json.loads(Path(item['snapshot']['path']).read_bytes());snap=export['snapshot'];before=digest(snap)
    view=SnapshotView(export);actor={'kind':'agent','id':'fixture-server'}
    rt=ActivityRuntime(view,snap['context_id'],snap['scope'],actor)
    start=time.perf_counter();refused=False
    try:out=rt.project(24000)
    except ProjectionOverflow as exc:
        refused=True;out=rt.project(exc.required_chars)
    seconds=time.perf_counter()-start
    assert out['required_chars']==item['required_chars'] and refused==item['refused_24000']
    baseline=old.ActivityRuntime(view,snap['context_id'],snap['scope'],actor).project(2000000)
    assert baseline['required_chars']==item['baseline_required_chars_same_snapshot']
    body,_=json.JSONDecoder().raw_decode(out['text'][out['text'].index('{'):])
    wire=json.loads(out['text'].split('<IALD_ACTIVITY_V1>\n')[1].split('\n</IALD_ACTIVITY_V1>')[0])
    present={r['id']:r for r in body['records']};indexed=set(out['indexed_record_ids'])
    for r in snap['q']['records']:
        if not is_mission_record(r) and r['id'] not in indexed and r['kind']!='candidate':
            assert present[r['id']]==r
    assert wire['active']==out['activity']['active']
    for projected in wire['settled']:
        full=next(t for t in out['activity']['settled'] if t['id']==projected['id'])
        for key in ('criterion','depends_on','status','epoch','reviewed_by','note','evidence','review_evidence'):
            assert projected[key]==full[key]
    for index in out['terminal_execution_index']['rows']:
        recovered={'records':[r for r in snap['q']['records'] if r.get('meta',{}).get(KEY,{}).get('data',{}).get('request_id')==index[0]],'handles':[h for h in snap['p']['handles'] if h.get('request_id')==index[0]],'receipt':snap['receipt']}
        records=[r for r in recovered['records'] if r['meta'][KEY]['kind'] in ('request','intent')]
        handles=[h for h in recovered['handles'] if h.get('kind') in ('activity_request','activity_operation')]
        assert index[2]==digest(sorted(records,key=lambda r:r['id']))
        assert index[3]==digest(sorted(handles,key=lambda h:h['id']))
        assert recovered['receipt']==out['receipt']
    assert digest(snap)==before
    assert out['projection_sha256']==hashlib.sha256(out['text'].encode()).hexdigest()
    rows.append({'turns':item['turns'],'reviewed_fixture':item['reviewed_fixture'],
        'required_chars':out['required_chars'],'baseline_required_chars':baseline['required_chars'],
        'refused_24000':refused,'indexed_records':len(indexed),'projection_seconds':seconds,
        'semantic_records_exact':True,'criteria_notes_evidence_exact':True,'all_index_digests_verified_against_complete_snapshot':True,
        'snapshot_unchanged':True,'snapshot':item['snapshot']})
assert len(rows)==6 and {(r['turns'],r['reviewed_fixture']) for r in rows}=={(n,b) for n in (1,10,100) for b in (False,True)}
out=R/'C2_INDEPENDENT_MEASUREMENTS_R1.json'
save(out,{'status':'PASS','source_measurements':pin(measurement),'source':m['source'],'script':pin(__file__),'rows':rows,
    'scope':'Independent pure projection and complete-record/handle digest verification on six pinned exported snapshots with live artifact-byte checks. API recover was already verified in78tests; it is not repeated for every row. Not historical get, not recreated admissions, not production measurement.',
    'interrupted_prior_verifier':pin(R/'C2_MEASUREMENT_VERIFIER_INTERRUPTED_R1.json'),'providers_called':0,'new_turns':0,'production_modified':False})
print(json.dumps({'report':pin(out),'rows':[{k:r[k] for k in ('turns','reviewed_fixture','required_chars','baseline_required_chars','refused_24000')} for r in rows]},ensure_ascii=False))
