"""Static integration capture only; never execute author programs or consume in-flight build reports."""
from pathlib import Path
import ast,datetime,difflib,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
OUT=REV/('scalar_right_tomita_integrated_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
OLD=REV/'homogeneous_right_integrated_20260912_155452_339076'
sha=lambda b:hashlib.sha256(b).hexdigest();hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
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
files=['integration.json','homogeneous_right_custody.json','homogeneous_right_custody_verification.json',
 'scalar_right_tomita_draft_memory.json','scalar_right_tomita_draft_status.json','scalar_right_adjoint_draft_status.json',
 'prepare_scalar_right_tomita_stage.py','record_scalar_right_tomita_progress.py','verify_scalar_right_tomita_custody.py',
 'integrate_v350.py','compile_integrated.py','test_gate_extension.py','gate_extension.py']
for f in files:write(OUT/f,(ROOT/f).read_bytes())
P=load(OUT/'homogeneous_right_custody.json');MEM=load(OUT/'scalar_right_tomita_draft_memory.json')
D=load(OUT/'scalar_right_tomita_draft_status.json');X=load(OUT/'scalar_right_adjoint_draft_status.json');I=load(OUT/'integration.json')
assert D['parent_custody_sha256']==MEM['previous_custody_sha256']==hf(OUT/'homogeneous_right_custody.json')
assert X['parent_draft_sha256']==hf(OUT/'scalar_right_tomita_draft_status.json')
assert X['parent_memory_sha256']==hf(OUT/'scalar_right_tomita_draft_memory.json')
assert D['integrated_working_sha256']==MEM['working_sha256']==X['working_sha256']==P['working_sha256']
for f in ['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json']:
    assert hf(OLD/f)==P['artifacts'][f]
own_sources={};own_axioms={};own_runs={}
for pointer in ['scalar_right_tomita_latest_run.txt','scalar_right_adjoint_latest_run.txt']:
    r=Path((REV/pointer).read_text().strip());m=load(r/'manifest.json');c=load(r/'compilation.json')
    assert all(v is True for k,v in c.items() if k!='records')
    assert not set(own_sources)&set(m['sources']) and not set(own_axioms)&set(c['records'][-1]['axioms'])
    own_sources.update(m['sources']);own_axioms.update(c['records'][-1]['axioms'])
    own_runs[str(r)]={'manifest_sha256':hf(r/'manifest.json'),'compilation_sha256':hf(r/'compilation.json')}
assert len(own_sources)==3 and len(own_axioms)==17
expected={**D['targets'],**X['targets']};assert {n:sorted(a) for n,a in own_axioms.items()}==expected
review=REV/'REVIEW_SCALAR_RIGHT_CLOSED_TOMITA.md';rv=load(REV/'scalar_right_tomita_report_verification.json')
assert hf(review)==rv['report_sha256'] and rv['cumulative_targets']==17 and rv['own_executions_rc0']==5
assert 'SCALAR_RIGHT_CLOSED_TOMITA_DEV_REVIEW' in review.read_text(encoding='utf-8')
oldum=next(p for p in sorted(ROOT.glob('um.py.bak_*'),reverse=True) if hf(p)==P['working_sha256'])
old,oldast=embedded(oldum.read_bytes());rawum=(ROOT/'um.py').read_bytes();cur,newast=embedded(rawum)
assert oldast==newast and sha(rawum)==I['working_sha256']
assert len(cur)==I['embedded_files']==862 and hf(ROOT/'gate_extension.py')==P['artifacts']['gate_extension.py']
trans={}
for rel,s in own_sources.items():
    n=Path(rel).stem;key='TGLExt/V350'+n+'.lean';raw=Path(s['path']).read_bytes();b=(ROOT/'kernel'/key).read_bytes()
    assert sha(raw)==s['sha256'] and hf(s['snapshot'])==s['sha256'] and hf(s['author_binary'])==s['author_binary_sha256']
    assert re.sub(rb'^import TGLV350\.',b'import TGLExt.V350',raw,flags=re.M)==b
    assert cur[key].encode('utf-8')==b
    write(OUT/'sources'/key,b)
    trans[n]={'dev_sha256':s['sha256'],'integrated_sha256':sha(b),'literal_import_rewrite_only':True,
      'embedded_bytes_equal':True,'targets':s['declarations'],'DEV_binary_sha256':s['author_binary_sha256']}
newkeys={'TGLExt/V350'+n+'.lean' for n in trans};roots={'TGLExt.lean','TGL/Audit.lean'}
assert set(cur)-set(old)==newkeys and not(set(old)-set(cur))
assert {k for k in old if old[k]!=cur[k]}==roots
for key in roots:
    assert (ROOT/'kernel'/key).read_bytes()==cur[key].encode('utf-8')
    assert all(len(re.findall(r'^import TGLExt\.V350'+n+r'\s*$',cur[key],re.M))==1 for n in trans)
    write(OUT/'sources'/key,cur[key].encode())
    diff=''.join(difflib.unified_diff(old[key].splitlines(True),cur[key].splitlines(True),fromfile=key+'.parent',tofile=key))
    write(OUT/(key.replace('/','_')+'.diff'),diff.encode())
oldnames=re.findall(r"^#print axioms ([\w.']+)",old['TGL/Audit.lean'],re.M)
newnames=re.findall(r"^#print axioms ([\w.']+)",cur['TGL/Audit.lean'],re.M)
assert len(set(oldnames))==P['audit_declarations']==6687 and len(set(newnames))==6704
assert set(newnames)-set(oldnames)==set(own_axioms)
assert all(newnames.count(n)==oldnames.count(n) for n in oldnames)
helpers={}
for f in files:
    if f.endswith('.py'):
        b=(OUT/f).read_bytes();ast.parse(b);helpers[f]={'sha256':sha(b),'lines':len(b.splitlines()),'execution_by_reviewer':False}
diffs={}
for f in ['integrate_v350.py','compile_integrated.py','test_gate_extension.py']:
    oldfile=next(p for p in sorted(ROOT.glob(f+'.bak_*'),reverse=True) if hf(p)==P['artifacts'][f])
    a=oldfile.read_bytes();b=(OUT/f).read_bytes()
    diff=''.join(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile=oldfile.name,tofile=f))
    write(OUT/(f+'.diff'),diff.encode());write(OUT/(f+'.parent'),a)
    diffs[f]={'parent_backup':str(oldfile),'parent_sha256':sha(a),'current_sha256':sha(b)}
surfaces={}
for p,h in MEM['surface_sha256'].items():
    sp=Path(p);bp=Path(MEM['backups'][p]);raw=sp.read_bytes();oldb=bp.read_bytes()
    assert sha(raw)==h and sha(oldb)==MEM['surface_before_sha256'][p]
    assert sp.parent==bp.parent and raw.startswith(oldb) and len(raw)>len(oldb)
    assert MEM['surface_before_sha256'][p]==P['surface_sha256'][p]
    surfaces[p]={'sha256':h,'backup':str(bp),'backup_sha256':sha(oldb),'bytes':len(raw),'exact_byte_prefix':True}
assert len(surfaces)==34
pending=['scalar_right_tomita_custody.json','scalar_right_tomita_custody_verification.json','RELATORIO_DOMINIOS_TOMITA_ADJUNTO_INTEGRADOS.md']
assert not any((ROOT/f).exists() for f in pending)
cfg=load(ROOT/'environment.json');original=hf(cfg['original_source'])
assert original==hf(ROOT/'fontes/um_v350_original.py')==I['base_sha256']==P['original_sha256']
assert all(hf(p)==h for p,h in P['review_sha256'].items())
baseline=load(ROOT/'fontes/um_absoluto.json')['core']['kernel_formalization']
historical={k:baseline.get(k) for k in ['audit_stdout_sha256','audit_capture_sha256_full']}
assert all(hf(ROOT/f)==hf(OUT/f) for f in files) and hf(ROOT/'um.py')==I['working_sha256']
v={'timestamp':datetime.datetime.now().astimezone().isoformat(),'mode':'STATIC_ONLY_FINAL_BUILD_NOT_YET_CONSUMED',
 'path':str(OUT),'working_sha256':I['working_sha256'],'parent_working_sha256':P['working_sha256'],
 'parent_working_backup':str(oldum),'original_sha256':original,
 'mathematical_parent_sha256':hf(OUT/'homogeneous_right_custody.json'),
 'immediate_memory_parent_sha256':hf(OUT/'scalar_right_tomita_draft_memory.json'),
 'embedded_files':862,'transposition':trans,'all_three_import_rewrites_literal':True,
 'python_AST_outside_embedded_equal':True,'gate_extension_bytes_equal':True,'only_three_modules_and_two_roots_changed':True,
 'source_Audit_distinct':6704,'source_Audit_new_targets':17,'source_Audit_parent_no_loss':True,
 'own_DEV_runs':own_runs,'own_DEV_review_sha256':hf(review),'helpers':helpers,'preparation_diffs':diffs,
 'immediate_memory_surface_count':34,'immediate_memory_surfaces':surfaces,'future_custody_artifacts_absent':pending,
 'historical_Audit_metadata_expected':historical,'artifact_pins':{f:hf(OUT/f) for f in files},
 'new_Lean_executions':0,'author_programs_executed':False,'memory_written':False,'pending':['final_compile_records','final_Audit_stream','final_controls_and_evidence']}
save(OUT/'static_verification.json',v);save(OUT/'own_DEV_axioms.json',own_axioms)
pointer=REV/'scalar_right_tomita_integrated_latest_run.txt';assert not pointer.exists();write(pointer,str(OUT).encode())
print(json.dumps({k:v[k] for k in ['path','working_sha256','original_sha256','embedded_files','all_three_import_rewrites_literal','python_AST_outside_embedded_equal','source_Audit_distinct','source_Audit_new_targets','immediate_memory_surface_count','pending']},ensure_ascii=False))
