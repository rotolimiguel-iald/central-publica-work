from pathlib import Path
import ast,datetime,hashlib,json,os
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'right_projection_pair_latest_run.txt').read_text().strip())
names=['make_right_graph_core_helpers.py','record_right_graph_core_draft.py','prepare_right_graph_core_stage.py','record_right_graph_core_progress.py','verify_right_graph_core_custody.py']
def sha(b):return hashlib.sha256(b).hexdigest()
def create(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;os.replace(q,p)
rows={}
for name in names:
    p=ROOT/name;raw=p.read_bytes();tree=ast.parse(raw);snap=RUN/'helper_sources'/name;create(snap,raw)
    rows[name]={'path':str(p),'snapshot':str(snap),'sha256':sha(raw),'bytes':len(raw),'ast_parses':True,'top_level_functions':[n.name for n in tree.body if isinstance(n,ast.FunctionDef)]}
res={'timestamp':datetime.datetime.now().astimezone().isoformat(),'mode':'READ_ONLY_STATIC_SOURCE_INSPECTION_NO_AUTHOR_HELPER_EXECUTED','helpers':rows,'parent_custody':'scalar_vna_custody.json','parent_custody_sha256':sha((ROOT/'scalar_vna_custody.json').read_bytes()),'intended_module_count':6,'intended_target_count':57,'intended_batch_transition':[625,682],'memory_surface_count_required_in_recorder':34,'requires_dev_review_marker_and_review_read_for_prepare':True,'requires_dev_and_integrated_review_markers_for_memory_recording':True,'preserves_byte_backups_and_prefixes_before_atomic_replace':True,'verifier_rereads_record_source_and_binary_hashes':True,'audits_current_stdout_hash_and_preserves_historical_metadata':True,'remarks':['Counts 6/57 and concrete graph equality in templates are intended future assertions; no final DEV or integration approval in this capture.','Maker is provenance; it was parsed and read, never rerun.','Recorder/verifier were read only; no memory recording or custody execution is claimed.','The ordinary product H x H for the antilinear graph is distinguished from the complex auxiliary Hilbert product.','Templates explicitly keep inverse commutant inclusion, modular flow/KMS, trace, gate consumption and runtime open.'],'P0':[],'P1':[],'P2':[]}
create(RUN/'helper_static_inspection.json',(json.dumps(res,ensure_ascii=False,indent=2)+'\n').encode())
assert all(sha((ROOT/n).read_bytes())==d['sha256'] for n,d in rows.items())
print(json.dumps({'output':str(RUN/'helper_static_inspection.json'),'helpers':{n:d['sha256'] for n,d in rows.items()},'executed_author_helpers':False},ensure_ascii=False))
