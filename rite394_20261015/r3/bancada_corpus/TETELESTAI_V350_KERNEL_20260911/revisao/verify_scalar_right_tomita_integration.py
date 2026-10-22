"""Read final integrated records and streams after author green; no builds or author code execution."""
from pathlib import Path
import ast,datetime,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
OUT=Path((REV/'scalar_right_tomita_integrated_latest_run.txt').read_text().strip())
OLD=REV/'homogeneous_right_integrated_20260912_155452_339076'
sha=lambda b:hashlib.sha256(b).hexdigest();hf=lambda p:sha(Path(p).read_bytes());load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p)
def save(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))
def axioms(s):
    d={}
    for n,v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",s,re.S):
        a=[t.strip() for t in v.split(',') if t.strip()];assert n not in d or d[n]==a;d[n]=a
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",s):assert n not in d or d[n]==[];d[n]=[]
    return d
S=load(OUT/'static_verification.json');P=load(OUT/'homogeneous_right_custody.json')
for f,h in S['artifact_pins'].items():assert hf(ROOT/f)==h==hf(OUT/f)
assert hf(ROOT/'um.py')==S['working_sha256']
files=['integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json']
for f in files:write(OUT/f,(ROOT/f).read_bytes())
B=load(OUT/files[0]);G=load(OUT/files[1]);E=load(OUT/files[2]);I=load(OUT/'integration.json')
assert B['incremental_build_ok'] and not B['full_monolithic_runtime_run']
assert G['working_um_sha256']==I['working_sha256']==S['working_sha256']
ownax=load(OUT/'own_DEV_axioms.json');assert len(ownax)==17
t=ast.parse((ROOT/'um.py').read_bytes())
embedded=ast.literal_eval(next(n.value for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='_EMBEDDED_KERNEL_FILES' for x in n.targets)))
newkeys={'TGLExt/V350'+n+'.lean' for n in S['transposition']};roots={'TGLExt.lean','TGL/Audit.lean'}
oldrows={Path(r['source']).relative_to(ROOT/'kernel').as_posix():r for r in load(OLD/'integrated_compile.json')['records']}
rows=[];rowkeys=set();newmaps={}
for r in B['records']:
    src=Path(r['source']).resolve();assert src.is_relative_to(ROOT/'kernel')
    rel=src.relative_to(ROOT/'kernel');key=rel.as_posix();bp=ROOT/'build'/rel.with_suffix('.olean')
    assert key not in rowkeys;rowkeys.add(key)
    sr=src.read_bytes();br=bp.read_bytes()
    assert r['returncode']==0 and r['output_exists']
    if 'lean_returncode' in r:assert r['lean_returncode']==0
    assert Path(r['command'][2])==bp and Path(r['command'][3])==src
    assert sha(sr)==r['sha256'] and sha(br)==r['output_sha256'] and embedded[key].encode('utf-8')==sr
    row={'file':key,'source_sha256':sha(sr),'binary_sha256':sha(br),'returncode':0,'timestamp':r['timestamp'],
      'same_record_as_parent':key in oldrows and r==oldrows[key], 'lean_returncode':r.get('lean_returncode'),
      'source_unchanged_during_compile':r.get('source_unchanged_during_compile')}
    for k in ['stdout','stderr']:
        lp=Path(r[k]);lb=lp.read_bytes();write(OUT/'logs'/lp.name,lb);row[k+'_sha256']=sha(lb);row[k+'_path']=str(lp)
    log=Path(r['stdout']).with_name(Path(r['stdout']).name.replace('.stdout.txt','.json'))
    lb=log.read_bytes();assert json.loads(lb)==r;write(OUT/'logs'/log.name,lb)
    row['log_sha256']=sha(lb);row['log_name']=log.name
    text=Path(r['stdout']).read_text(encoding='utf-8');assert not re.search(r'error(?:\([^)]*\))?:',text)
    row['warnings']=[l for l in text.splitlines() if 'warning:' in l]
    if key in newkeys:
        expected=S['transposition'][rel.stem[4:]]['targets'];a=axioms(text)
        assert a=={n:ownax[n] for n in expected};newmaps[key]=a
    if key in newkeys|roots:
        assert (OUT/'sources'/rel).read_bytes()==sr
        deps=[]
        for n in re.findall(r'^import\s+([\w.]+)',sr.decode('utf-8'),re.M):
            if n.split('.')[0] in {'TGL','TGLExt','TGLV350'}:
                dep=ROOT/'build'/Path(*n.split('.')).with_suffix('.olean')
                assert dep.is_file() and dep.stat().st_mtime_ns<=bp.stat().st_mtime_ns
                deps.append({'module':n,'binary_sha256':hf(dep),'fresh':True})
        row['direct_project_dependencies']=deps
    rows.append(row)
assert len(rows)==160 and rowkeys==set(I['added_kernel_files']+I['updated_kernel_files'])
assert sum(r['same_record_as_parent'] for r in rows)==155
changed=[r for r in rows if not r['same_record_as_parent']]
assert len(changed)==5 and {r['file'] for r in changed}==newkeys|roots
assert all(r['source_unchanged_during_compile'] is True and r['lean_returncode']==0 for r in changed)
assert [Path(r['source']).relative_to(ROOT/'kernel').as_posix() for r in B['records'][-5:]]==[
 'TGLExt/V350ScalarRightStarGraph.lean','TGLExt/V350ScalarRightClosedTomita.lean',
 'TGLExt/V350ScalarRightTomitaAdjoint.lean','TGLExt.lean','TGL/Audit.lean']
ar=next(r for r in rows if r['file']=='TGL/Audit.lean')
assert ar['log_name']=='Audit_20260912_162254_767979.json'
fullax=axioms(Path(ar['stdout_path']).read_text(encoding='utf-8'))
assert len(fullax)==G['axiom_report_entries']==6704 and fullax==E['axiom_report']
allowed={'propext','Classical.choice','Quot.sound'}
assert all(set(a)<=allowed for a in fullax.values()) and all(fullax[n]==a for n,a in ownax.items())
oldax=load(OLD/'axioms.json');assert oldax==load(OLD/'kernel_incremental_evidence.json')['axiom_report']
assert len(oldax)==6687 and set(fullax)-set(oldax)==set(ownax) and all(fullax[n]==a for n,a in oldax.items())
assert E['audit_stdout_sha256']==E['audit_capture_sha256_full']==ar['stdout_sha256']
assert E['audit_stdout_path']==ar['stdout_path'] and E['audit_hash_scope']=='CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES'
assert E['historical_v350_audit_metadata']==S['historical_Audit_metadata_expected']
assert E['historical_v350_audit_metadata']=={k:load(OLD/'kernel_incremental_evidence.json')[k] for k in ['audit_stdout_sha256','audit_capture_sha256_full']}
og=load(OLD/'gate_tests.json');checks={x['name']:x['passed'] for x in G['checks']};oc={x['name']:x['passed'] for x in og['checks']}
assert len(checks)==len(G['checks'])==G['passed']==90 and all(checks.values())
assert all(checks.get(n)==v for n,v in oc.items())
added=sorted(set(checks)-set(oc))
expected_added=['current_audit_hashes_match_current_raw_stream','historical_v350_audit_hashes_preserved_as_history']+[
 n+'_does_not_discharge_KMS_trace_or_physical_frontier' for n in ['right_preserves_same_closed_Tomita_domain','left_preserves_same_maximal_Tomita_adjoint_domain']]
assert added==sorted(expected_added)
assert G['legacy_gate']==og['legacy_gate'] and G['frontier']==og['frontier']
assert not G['frontier']['legacy_gate_changed'] and not G['frontier']['full_plan_complete'] and not G['full_monolithic_runtime_run']
flags={k:E[k] for k in P['remaining_flags']};assert len(flags)==6 and all(v is False for v in flags.values())
for p,r in S['immediate_memory_surfaces'].items():
    assert hf(p)==r['sha256'] and hf(r['backup'])==r['backup_sha256']
    assert Path(p).read_bytes().startswith(Path(r['backup']).read_bytes())
assert not any((ROOT/n).exists() for n in S['future_custody_artifacts_absent'])
assert hf(REV/'REVIEW_SCALAR_RIGHT_CLOSED_TOMITA.md')==S['own_DEV_review_sha256']
assert all(hf(ROOT/f)==hf(OUT/f) for f in files) and hf(ROOT/'um.py')==I['working_sha256']
v={'timestamp':datetime.datetime.now().astimezone().isoformat(),'mode':'FINAL_INTEGRATED_BYTE_AND_LOG_INSPECTION_NO_REBUILD',
 'path':str(OUT),'working_sha256':I['working_sha256'],'original_sha256':S['original_sha256'],
 'mathematical_parent_sha256':S['mathematical_parent_sha256'],'immediate_memory_parent_sha256':S['immediate_memory_parent_sha256'],
 'static_verification_sha256':hf(OUT/'static_verification.json'),'embedded_files':862,
 'all_three_import_rewrites_literal':True,'python_AST_outside_embedded_equal':True,'gate_extension_bytes_equal':True,
 'records':rows,'new_records':changed,'integrated_records':160,'unchanged_parent_records':155,'new_author_compilations':5,
 'all_source_binary_log_stream_pins_match':True,'new_axioms_equal_own_DEV':17,'audit_distinct':6704,'parent_Audit_no_loss':True,
 'audit_all_allowed':True,'final_Audit_record':ar,'current_Audit_global_hashes_verified':True,
 'historical_Audit_metadata_preserved':E['historical_v350_audit_metadata'],'gate_passed_author_records':90,
 'added_controls':added,'six_flags':flags,'legacy_gate_changed':False,'full_goal_complete':False,'full_runtime':False,
 'immediate_memory_surface_count':34,'immediate_memory_pins_preserved':True,
 'new_custody_report_verification_absent':S['future_custody_artifacts_absent'],
 'artifact_pins':{**S['artifact_pins'],**{f:hf(OUT/f) for f in files}},'own_DEV_review_sha256':S['own_DEV_review_sha256'],
 'new_Lean_executions':0,'author_programs_executed':False,'memory_written':False,
 'P0':[],'P1':[],'P2':[]}
save(OUT/'verification.json',v);save(OUT/'axioms.json',fullax);save(OUT/'new_module_axioms.json',newmaps)
print(json.dumps({k:v[k] for k in ['path','integrated_records','unchanged_parent_records','new_author_compilations',
 'gate_passed_author_records','audit_distinct','current_Audit_global_hashes_verified','historical_Audit_metadata_preserved','added_controls']},ensure_ascii=False))
