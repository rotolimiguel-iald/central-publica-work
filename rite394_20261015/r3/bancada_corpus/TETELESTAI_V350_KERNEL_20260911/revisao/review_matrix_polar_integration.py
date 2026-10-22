"""Static capture or final read-only verification of this eight-module integration; no author execution."""
from pathlib import Path
import ast,datetime,difflib,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
OLD=Path((REV/'regular_polar_integrated_latest_run.txt').read_text().strip())
DEV=Path((REV/'matrix_polar_latest_run.txt').read_text().strip())
FINAL='--final' in sys.argv
PTR=REV/'matrix_polar_integrated_latest_run.txt'
OUT=Path(PTR.read_text().strip()) if FINAL else REV/('matrix_polar_integrated_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b:hashlib.sha256(b).hexdigest();hf=lambda p:sha(Path(p).read_bytes());load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p)
def save(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))
def embedded(raw):
    t=ast.parse(raw);ns=[n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='_EMBEDDED_KERNEL_FILES' for x in n.targets)]
    assert len(ns)==1;d=ast.literal_eval(ns[0].value);ns[0].value=ast.Constant('EXCLUDED_EMBEDDED_LEAN')
    return d,ast.dump(t,include_attributes=False)
def axioms(text):
    d={}
    for n,v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",text,re.S):
        a=[x.strip() for x in v.split(',') if x.strip()];assert n not in d or d[n]==a;d[n]=a
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",text):assert n not in d or not d[n];d[n]=[]
    return d
if not FINAL:
    files=['integration.json','regular_polar_custody.json','regular_polar_custody_verification.json',
     'matrix_polar_draft_status.json','RELATORIO_CONJUGACAO_POLAR_MATRICIAL_DEV.md',
     'prepare_matrix_polar_stage.py','record_matrix_polar_progress.py','verify_matrix_polar_custody.py',
     'integrate_v350.py','compile_integrated.py','test_gate_extension.py','gate_extension.py']
    for f in files:write(OUT/f,(ROOT/f).read_bytes())
    P=load(OUT/'regular_polar_custody.json');D=load(OUT/'matrix_polar_draft_status.json');I=load(OUT/'integration.json')
    M=load(DEV/'manifest.json');C=load(DEV/'compilation.json');V=load(DEV/'verification.json')
    assert all(v is True for k,v in C.items() if k!='records')
    assert hf(DEV/'manifest.json')==V['runs'][-1]['manifest_sha256'] and hf(DEV/'compilation.json')==V['runs'][-1]['compilation_sha256']
    DOC=max(REV.glob('matrix_polar_documentation_review_*'),key=lambda p:p.name)
    DV=load(DOC/'verification.json');assert DV['finding_P2_resolved']
    assert D['parent_custody_sha256']==hf(OUT/'regular_polar_custody.json')
    assert D['integrated_working_sha256']==P['working_sha256']
    assert hf(OUT/'matrix_polar_draft_status.json')==DV['manifest_after_sha256']
    assert D['report_sha256']==hf(OUT/'RELATORIO_CONJUGACAO_POLAR_MATRICIAL_DEV.md')
    assert hf(REV/'REVIEW_MATRIX_POLAR_DEV.md')==DV['review_after_sha256']
    assert D['modules']==load(DEV/'matrix_polar_draft_status.json')['modules'] and D['targets']==load(DEV/'matrix_polar_draft_status.json')['targets']
    M['sources']={'TGLV350/'+name+'.lean':s for name,s in V['modules'].items()}
    V['report_sha256']=DV['review_after_sha256']
    write(OUT/'DEV_P2_resolution.json',(DOC/'verification.json').read_bytes())
    for f in ['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json']:
        assert hf(OLD/f)==P['artifacts'][f]
    ownax=C['records'][-1]['axioms'];assert len(ownax)==32 and {n:sorted(a) for n,a in ownax.items()}==D['targets']
    oldum=next(p for p in sorted(ROOT.glob('um.py.bak_*'),reverse=True) if hf(p)==P['working_sha256'])
    old,oldast=embedded(oldum.read_bytes());um=(ROOT/'um.py').read_bytes();cur,newast=embedded(um)
    assert oldast==newast and sha(um)==I['working_sha256'] and len(cur)==I['embedded_files']==878
    assert hf(ROOT/'gate_extension.py')==P['artifacts']['gate_extension.py']
    trans={}
    for rel,s in M['sources'].items():
        n=Path(rel).stem;key='TGLExt/V350'+n+'.lean';raw=Path(s['path']).read_bytes();b=(ROOT/'kernel'/key).read_bytes()
        assert sha(raw)==s['sha256']==D['modules'][n]['source_sha256'] and hf(s['snapshot'])==sha(raw)
        assert hf(s['author_binary'])==s['author_binary_sha256']==D['modules'][n]['binary_sha256']
        assert re.sub(rb'^import TGLV350\.',b'import TGLExt.V350',raw,flags=re.M)==b and cur[key].encode()==b
        write(OUT/'sources'/key,b)
        trans[n]={'dev_sha256':sha(raw),'integrated_sha256':sha(b),'literal_import_rewrite_only':True,'embedded_bytes_equal':True,'targets':s['declarations']}
    newkeys={'TGLExt/V350'+n+'.lean' for n in trans};roots={'TGLExt.lean','TGL/Audit.lean'}
    assert set(cur)-set(old)==newkeys and not(set(old)-set(cur)) and {k for k in old if old[k]!=cur[k]}==roots
    for key in roots:
        assert (ROOT/'kernel'/key).read_bytes()==cur[key].encode()
        assert all(len(re.findall(r'^import TGLExt\.V350'+n+r'\s*$',cur[key],re.M))==1 for n in trans)
        write(OUT/'sources'/key,cur[key].encode())
        write(OUT/(key.replace('/','_')+'.diff'),''.join(difflib.unified_diff(old[key].splitlines(True),cur[key].splitlines(True),fromfile=key+'.parent',tofile=key)).encode())
    oldnames=re.findall(r"^#print axioms ([\w.']+)",old['TGL/Audit.lean'],re.M)
    names=re.findall(r"^#print axioms ([\w.']+)",cur['TGL/Audit.lean'],re.M)
    assert len(set(oldnames))==P['audit_declarations']==6769 and len(set(names))==6801
    assert set(names)-set(oldnames)==set(ownax) and all(names.count(n)==oldnames.count(n) for n in oldnames)
    helpers={}
    for f in files:
        if f.endswith('.py'):
            b=(OUT/f).read_bytes();ast.parse(b);helpers[f]={'sha256':sha(b),'lines':len(b.splitlines()),'executed_by_reviewer':False}
    diffs={}
    for f in ['integrate_v350.py','compile_integrated.py','test_gate_extension.py']:
        bp=next(p for p in sorted(ROOT.glob(f+'.bak_*'),reverse=True) if hf(p)==P['artifacts'][f])
        a=bp.read_bytes();b=(OUT/f).read_bytes()
        write(OUT/(f+'.parent'),a);write(OUT/(f+'.diff'),''.join(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile=bp.name,tofile=f)).encode())
        diffs[f]={'parent_backup':str(bp),'parent_sha256':sha(a),'current_sha256':sha(b)}
    surfaces={}
    for p,h in P['surface_sha256'].items():
        sp=Path(p);bp=Path(P['backups'][p])
        if not sp.resolve().is_relative_to(ROOT):
            surfaces[p]={'sha256':h,'backup':str(bp),'backup_sha256':P['surface_before_sha256'][p],'external_pin_inherited_not_reread':True}
            continue
        raw=sp.read_bytes();b=bp.read_bytes()
        assert sha(raw)==h and sha(b)==P['surface_before_sha256'][p] and raw.startswith(b) and len(raw)>len(b) and sp.parent==bp.parent
        surfaces[p]={'sha256':h,'backup':str(bp),'backup_sha256':sha(b),'exact_byte_prefix':True}
    assert len(surfaces)==34
    pending=['matrix_polar_custody.json','matrix_polar_custody_verification.json','RELATORIO_CONJUGACAO_POLAR_MATRICIAL_INTEGRADA.md']
    assert not any((ROOT/f).exists() for f in pending)
    original=hf(ROOT/'fontes/um_v350_original.py')
    assert original==I['base_sha256']==P['original_sha256']
    assert all(hf(p)==h for p,h in P['review_sha256'].items())
    baseline=load(ROOT/'fontes/um_absoluto.json')['core']['kernel_formalization']
    historical={k:baseline.get(k) for k in ['audit_stdout_sha256','audit_capture_sha256_full']}
    assert all(hf(ROOT/f)==hf(OUT/f) for f in files) and hf(ROOT/'um.py')==I['working_sha256']
    tree=ast.parse(um)
    selected={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['evaluate_quantum_gravity_closure','prove_qg_closure_gate','evaluate_v350_kernel_frontier']}
    assert len(selected)==3
    for name,node in selected.items():
        write(OUT/'gate_AST'/(name+'.py.txt'),ast.get_source_segment(um.decode('utf-8'),node).encode())
    evaluator=selected['evaluate_quantum_gravity_closure']
    assert [a.arg for a in evaluator.args.args]==['formal','physics','experiment']
    assert not any(isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value.startswith(('qgf_','gpf_')) for n in ast.walk(evaluator))
    caller=selected['prove_qg_closure_gate']
    assigns={n.targets[0].id:n for n in caller.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
    assert 'qgc_' in ast.unparse(assigns['formal']) and 'qgp_' in ast.unparse(assigns['physics'])
    assert 'experiment_feed' in ast.unparse(assigns['_feed'])
    assert ast.unparse(assigns['gate'].value)=='evaluate_quantum_gravity_closure(formal, physics, experiment)'
    addon=next(n for n in caller.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Subscript) and ast.unparse(n.targets[0])=="gate['kernel_frontier']")
    assert addon.lineno>assigns['gate'].lineno and ast.unparse(addon.value)=='evaluate_v350_kernel_frontier(kf99)'
    save(OUT/'gate_wiring.json',{'evaluator_line':evaluator.lineno,'caller_line':caller.lineno,'formal_line':assigns['formal'].lineno,'physics_line':assigns['physics'].lineno,'feed_line':assigns['_feed'].lineno,'call_line':assigns['gate'].lineno,'annex_line':addon.lineno,'six_frontier_flags_not_direct_evaluator_inputs':True,'read_only_AST_no_execution':True})
    S={'timestamp':datetime.datetime.now().astimezone().isoformat(),'mode':'STATIC_ONLY_BUILD_NOT_CONSUMED',
     'path':str(OUT),'working_sha256':I['working_sha256'],'parent_working_sha256':P['working_sha256'],'parent_working_backup':str(oldum),
     'original_sha256':original,'canonical_original_freshly_reread':False,'parent_custody_sha256':hf(OUT/'regular_polar_custody.json'),
     'embedded_files':878,'transposition':trans,'all_eight_import_rewrites_literal':True,'python_AST_outside_embedded_equal':True,
     'gate_extension_bytes_equal':True,'source_Audit_distinct':6801,'source_Audit_added':32,'source_Audit_parent_no_loss':True,
     'own_DEV_run':str(DEV),'own_DEV_runs':V['runs'],'own_DEV_review_sha256':V['report_sha256'],'own_DEV_compilation_sha256':hf(DEV/'compilation.json'),
     'helpers':helpers,'preparation_diffs':diffs,'memory_surfaces':surfaces,'surface_count':34,'future_custody_artifacts_absent':pending,
     'historical_Audit_metadata_expected':historical,'artifact_pins':{f:hf(OUT/f) for f in files},'new_Lean_executions':0,
     'author_programs_executed':False,'memory_written':False,'pending':['final_compile_records','final_Audit_stream','final_controls']}
    save(OUT/'static_verification.json',S);save(OUT/'own_DEV_axioms.json',ownax);write(PTR,str(OUT).encode())
    print(json.dumps({k:S[k] for k in ['path','working_sha256','all_eight_import_rewrites_literal','python_AST_outside_embedded_equal','embedded_files','source_Audit_distinct','pending']}))
    sys.exit(0)
S=load(OUT/'static_verification.json');P=load(OUT/'regular_polar_custody.json');I=load(OUT/'integration.json')
for f,h in S['artifact_pins'].items():assert hf(ROOT/f)==h
assert hf(ROOT/'um.py')==S['working_sha256']
files=['integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json']
for f in files:write(OUT/f,(ROOT/f).read_bytes())
B=load(OUT/files[0]);G=load(OUT/files[1]);E=load(OUT/files[2])
assert B['incremental_build_ok'] and not B['full_monolithic_runtime_run'] and G['working_um_sha256']==I['working_sha256']
cur,_=embedded((ROOT/'um.py').read_bytes());ownax=load(OUT/'own_DEV_axioms.json')
newkeys={'TGLExt/V350'+n+'.lean' for n in S['transposition']};roots={'TGLExt.lean','TGL/Audit.lean'}
oldrows={Path(r['source']).relative_to(ROOT/'kernel').as_posix():r for r in load(OLD/'integrated_compile.json')['records']}
rows=[];seen=set();maps={}
for r in B['records']:
    src=Path(r['source']).resolve();assert src.is_relative_to(ROOT/'kernel');rel=src.relative_to(ROOT/'kernel');key=rel.as_posix();bp=ROOT/'build'/rel.with_suffix('.olean')
    assert key not in seen;seen.add(key);raw=src.read_bytes();br=bp.read_bytes()
    assert r['returncode']==0 and r['output_exists'] and r.get('lean_returncode',0)==0
    assert Path(r['command'][2])==bp and Path(r['command'][3])==src
    assert sha(raw)==r['sha256'] and sha(br)==r['output_sha256'] and cur[key].encode()==raw
    row={'file':key,'source_sha256':sha(raw),'binary_sha256':sha(br),'returncode':0,'timestamp':r['timestamp'],
     'same_record_as_parent':key in oldrows and r==oldrows[key],'lean_returncode':r.get('lean_returncode'),
     'source_unchanged_during_compile':r.get('source_unchanged_during_compile')}
    for k in ['stdout','stderr']:
        lp=Path(r[k]);b=lp.read_bytes();write(OUT/'logs'/lp.name,b);row[k+'_sha256']=sha(b);row[k+'_path']=str(lp)
    lp=Path(r['stdout']).with_name(Path(r['stdout']).name.replace('.stdout.txt','.json'));b=lp.read_bytes();assert json.loads(b)==r
    write(OUT/'logs'/lp.name,b);row['log_name']=lp.name;row['log_sha256']=sha(b)
    text=Path(r['stdout']).read_text(encoding='utf-8');assert not re.search(r'error(?:\([^)]*\))?:',text)
    row['warnings']=[l for l in text.splitlines() if 'warning:' in l]
    if key in newkeys:
        names=S['transposition'][rel.stem[4:]]['targets'];a=axioms(text);assert a=={n:ownax[n] for n in names};maps[key]=a
    if key in newkeys|roots:
        assert (OUT/'sources'/rel).read_bytes()==raw
        deps=[]
        for n in re.findall(r'^import\s+([\w.]+)',raw.decode(),re.M):
            if n.split('.')[0] in {'TGL','TGLExt','TGLV350'}:
                dp=ROOT/'build'/Path(*n.split('.')).with_suffix('.olean');assert dp.is_file() and dp.stat().st_mtime_ns<=bp.stat().st_mtime_ns
                deps.append({'module':n,'binary_sha256':hf(dp),'fresh':True})
        row['direct_dependencies']=deps
    rows.append(row)
assert len(rows)==176 and seen==set(I['added_kernel_files']+I['updated_kernel_files'])
assert sum(r['same_record_as_parent'] for r in rows)==166
changed=[r for r in rows if not r['same_record_as_parent']]
assert len(changed)==10 and {r['file'] for r in changed}==newkeys|roots
assert all(r['source_unchanged_during_compile'] is True and r['lean_returncode']==0 for r in changed)
assert [r['file'] for r in rows[-10:]]==['TGLExt/V350'+n+'.lean' for n in S['transposition']]+['TGLExt.lean','TGL/Audit.lean']
ar=rows[-1];a=axioms(Path(ar['stdout_path']).read_text(encoding='utf-8'));oldax=load(OLD/'axioms.json')
assert oldax==load(OLD/'kernel_incremental_evidence.json')['axiom_report']
assert len(a)==G['axiom_report_entries']==6801 and a==E['axiom_report'] and len(oldax)==6769
assert set(a)-set(oldax)==set(ownax) and all(a[n]==x for n,x in oldax.items()) and all(a[n]==x for n,x in ownax.items())
assert all(set(x)<={'propext','Classical.choice','Quot.sound'} for x in a.values())
assert E['audit_stdout_sha256']==E['audit_capture_sha256_full']==ar['stdout_sha256'] and E['audit_stdout_path']==ar['stdout_path']
assert E['audit_hash_scope']=='CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES'
assert E['historical_v350_audit_metadata']==S['historical_Audit_metadata_expected']==load(OLD/'kernel_incremental_evidence.json')['historical_v350_audit_metadata']
og=load(OLD/'gate_tests.json');checks={c['name']:c['passed'] for c in G['checks']};oc={c['name']:c['passed'] for c in og['checks']}
assert len(checks)==len(G['checks'])==G['passed']==94 and all(checks.values()) and all(checks.get(n)==x for n,x in oc.items())
added=sorted(set(checks)-set(oc));assert added==['same_polar_matrix_unit_root_scaling_does_not_discharge_KMS_trace_or_physical_frontier']
assert G['legacy_gate']==og['legacy_gate'] and G['frontier']==og['frontier']
assert not G['frontier']['legacy_gate_changed'] and not G['frontier']['full_plan_complete'] and not G['full_monolithic_runtime_run']
flags={k:E[k] for k in P['remaining_flags']};assert len(flags)==6 and all(x is False for x in flags.values())
for p,r in S['memory_surfaces'].items():
    if not r.get('external_pin_inherited_not_reread'):assert hf(p)==r['sha256'] and hf(r['backup'])==r['backup_sha256']
assert not any((ROOT/n).exists() for n in S['future_custody_artifacts_absent'])
assert hf(REV/'REVIEW_MATRIX_POLAR_DEV.md')==S['own_DEV_review_sha256'] and all(hf(ROOT/f)==hf(OUT/f) for f in files)
v={'timestamp':datetime.datetime.now().astimezone().isoformat(),'mode':'FINAL_INTEGRATION_INSPECTION_NO_REBUILD','path':str(OUT),
 'working_sha256':I['working_sha256'],'original_sha256':S['original_sha256'],'parent_custody_sha256':S['parent_custody_sha256'],
 'embedded_files':878,'all_eight_import_rewrites_literal':True,'python_AST_outside_embedded_equal':True,'gate_extension_bytes_equal':True,
 'records':rows,'new_records':changed,'integrated_records':176,'unchanged_parent_records':166,'new_author_compilations':10,
 'all_source_binary_log_stream_pins_match':True,'new_axioms_equal_own_DEV':32,'audit_distinct':6801,'parent_Audit_no_loss':True,'audit_all_allowed':True,
 'final_Audit_record':ar,'current_Audit_global_hashes_verified':True,'historical_Audit_metadata_preserved':E['historical_v350_audit_metadata'],
 'gate_passed_author_records':94,'added_controls':added,'six_flags':flags,'legacy_gate_changed':False,'full_goal_complete':False,'full_runtime':False,
 'memory_surface_count':34,'memory_pins_inside_ROOT_preserved':True,'external_memory_pins_inherited':sum(r.get('external_pin_inherited_not_reread',False) for r in S['memory_surfaces'].values()),'new_custody_report_verification_absent':S['future_custody_artifacts_absent'],
 'artifact_pins':{**S['artifact_pins'],**{f:hf(OUT/f) for f in files}},'static_verification_sha256':hf(OUT/'static_verification.json'),
 'own_DEV_review_sha256':S['own_DEV_review_sha256'],'new_Lean_executions':0,'author_programs_executed':False,'memory_written':False,'P0':[],'P1':[],'P2':[]}
save(OUT/'verification.json',v);save(OUT/'axioms.json',a);save(OUT/'new_module_axioms.json',maps)
print(json.dumps({k:v[k] for k in ['path','working_sha256','integrated_records','unchanged_parent_records','new_author_compilations','gate_passed_author_records','audit_distinct','current_Audit_global_hashes_verified','added_controls']}))
