from pathlib import Path
import datetime,hashlib,json
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'square_resolvent_integrated_latest_run.txt').read_text().strip())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
V=load(RUN/'author_verification.json');C=load(RUN/'compilation.json');M=load(RUN/'build_manifest.json');S=load(RUN/'static_verification.json');H=load(RUN/'helper_static_inspection.json')
assert V['author_final_artifacts_validated'] and not V['complete']
assert C['complete'] and C['all_five_exit_zero'] and C['all_exact_targets'] and C['all_axioms_allowed'] and C['all_new_axioms_match_DEV'] and C['dependencies_preserved'] and C['external_direct_pins_preserved']
assert not any(V[k] or H[k] for k in ['P0','P1','P2'])
for r in V['new_records']:
    mod=r['file'][:-5].replace('/','.');own=next(x for x in C['records'] if x['module']==mod)
    assert own['source_sha256']==r['source_sha256'] and own['output_sha256']==r['binary_sha256'],mod
    assert hf(own['command'][2])==own['output_sha256'] and hf(own['command'][3])==own['source_sha256']
    r['own_recompiled_binary_equal']=True;r['own_compile_seconds']=own['seconds']
newrows={r['file']:r for r in V['new_records']}
V['records']=[newrows.get(r['file'],r) for r in V['records']]
assert C['records'][-1]['module']=='TGL.Audit' and C['records'][-1]['axioms']==load(RUN/'axioms.json')
for name,pin in V['artifact_pins'].items():assert hf(ROOT/name)==pin,name
assert hf(ROOT/'um.py')==V['working_sha256']
for r in V['records']:
    assert hf(ROOT/'kernel'/r['file'])==r['source_sha256'] and hf(ROOT/'build'/Path(r['file']).with_suffix('.olean'))==r['binary_sha256']
    for stream in ['stdout','stderr']:assert hf(r[stream+'_path'])==r[stream+'_sha256']
for p,h in S['surface_pins'].items():assert hf(p)==h,p
parent=load(RUN/'bidual_right_support_custody.json')
assert all(hf(p)==h for p,h in parent['review_sha256'].items())
assert hf(REV/'REVIEW_SQUARE_RESOLVENT_DEV.md')==S['own_DEV_review_sha256']
assert hf(load(ROOT/'environment.json')['original_source'])==hf(ROOT/'fontes/um_v350_original.py')==V['original_sha256']
assert not any((ROOT/n).exists() for n in V['new_custody_report_verification_absent'])
V.update({'timestamp':datetime.datetime.now().astimezone().isoformat(),'mode':'FINAL_INTEGRATION_INSPECTION_WITH_FIVE_OWN_COMPILATIONS_ON_EXPLICITLY_INHERITED_BINARY_DEPS','complete':True,'new_Lean_executions':5,'own_integrated_compilation_sha256':hf(RUN/'compilation.json'),'own_build_manifest_sha256':hf(RUN/'build_manifest.json'),'own_integrated_binaries_equal_author':True,'own_full_Audit_equals_author_stream':True,'dependency_provenance_counts':M['provenance_counts'],'binary_inheritance_limitation':C['limitation'],'author_artifacts_phase_sha256':hf(RUN/'author_verification.json'),'base_source_provenance_sha256':hf(RUN/'base_source_provenance.json')})
p=RUN/'verification.json';assert not p.exists();t=p.with_suffix('.json.tmp');raw=(json.dumps(V,ensure_ascii=False,indent=2)+'\n').encode()
with t.open('xb') as f:f.write(raw)
assert t.read_bytes()==raw;t.replace(p)
print(json.dumps({k:V[k] for k in ['complete','working_sha256','integrated_records','unchanged_parent_records','new_author_compilations','new_Lean_executions','own_integrated_binaries_equal_author','audit_distinct','gate_passed_author_records']}))
