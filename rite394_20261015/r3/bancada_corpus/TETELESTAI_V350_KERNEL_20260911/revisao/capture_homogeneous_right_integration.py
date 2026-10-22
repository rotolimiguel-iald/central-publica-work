"""Inspect integrated bytes/logs and custody preparation. No author code executes."""
from pathlib import Path
import ast,datetime,difflib,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
DEV=Path((REV/'homogeneous_right_latest_run.txt').read_text().strip())
SCALAR=Path((REV/'scalar_weight_gns_latest_run.txt').read_text().strip())
OLD=SCALAR/'integrated_20260912_150136_734138'
OUT=REV/('homogeneous_right_integrated_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
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
def embedded(raw):
    t=ast.parse(raw);ns=[n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='_EMBEDDED_KERNEL_FILES' for x in n.targets)]
    assert len(ns)==1;d=ast.literal_eval(ns[0].value);ns[0].value=ast.Constant('EXCLUDED_EMBEDDED_LEAN')
    return d,ast.dump(t,include_attributes=False)
files=['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json',
 'scalar_weight_gns_custody.json','homogeneous_right_dev_custody.json','homogeneous_right_dev_verification.json',
 'homogeneous_right_draft_status.json','RELATORIO_DIREITA_MODULAR_GNS_DEV.md','RELATORIO_DIREITA_MODULAR_GNS_REVISADO.md',
 'prepare_homogeneous_right_stage.py','record_homogeneous_right_progress.py','verify_homogeneous_right_custody.py',
 'integrate_v350.py','compile_integrated.py','test_gate_extension.py','gate_extension.py']
for f in files:write(OUT/f,(ROOT/f).read_bytes())
P=load(OUT/'scalar_weight_gns_custody.json');MEM=load(OUT/'homogeneous_right_dev_custody.json')
MV=load(OUT/'homogeneous_right_dev_verification.json');D=load(OUT/'homogeneous_right_draft_status.json')
B=load(OUT/'integrated_compile.json');G=load(OUT/'gate_tests.json');E=load(OUT/'kernel_incremental_evidence.json');I=load(OUT/'integration.json')
M=load(DEV/'manifest.json');C=load(DEV/'compilation.json');V=load(DEV/'verification.json')
assert all(C[k] for k in ['complete','all_exit_zero','all_axioms_allowed','exact_28_targets','five_binaries_equal_author'])
assert hf(DEV/'compilation.json')==V['compilation_sha256'] and hf(DEV/'manifest.json')==V['manifest_sha256']
assert hf(ROOT/'homogeneous_right_draft_status.json')==M['draft_status_sha256']==MEM['draft_sha256']
assert hf(ROOT/'revisao/REVIEW_HOMOGENEOUS_RIGHT_GNS.md')==MEM['review_sha256']
assert MEM['previous_custody_sha256']==D['parent_custody_sha256']==hf(ROOT/'scalar_weight_gns_custody.json')
assert MV['custody_ok'] and MV['custody_sha256']==hf(ROOT/'homogeneous_right_dev_custody.json')
assert MEM['working_sha256']==P['working_sha256']==D['integrated_working_sha256']
assert MEM['surface_before_sha256']==P['surface_sha256'] and len(MEM['surface_sha256'])==34
for f in ['integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json']:
    assert hf(OLD/f)==P['artifacts'][f]
ownax=C['records'][-1]['axioms'];assert len(ownax)==28 and {n:sorted(a) for n,a in ownax.items()}==D['targets']
assert B['incremental_build_ok'] and not B['full_monolithic_runtime_run']
oldum=next(p for p in sorted(ROOT.glob('um.py.bak_*'),reverse=True) if hf(p)==P['working_sha256'])
before,oldast=embedded(oldum.read_bytes());rawum=(ROOT/'um.py').read_bytes();current,newast=embedded(rawum)
assert oldast==newast and sha(rawum)==I['working_sha256']==G['working_um_sha256']
assert len(current)==I['embedded_files']==859 and hf(ROOT/'gate_extension.py')==P['artifacts']['gate_extension.py']
trans={}
for rel,s in M['sources'].items():
    name=Path(rel).stem;key='TGLExt/V350'+name+'.lean';raw=Path(s['path']).read_bytes();new=(ROOT/'kernel'/key).read_bytes()
    assert sha(raw)==s['sha256']==D['modules'][name]['source_sha256']
    assert re.sub(rb'^import TGLV350\.',b'import TGLExt.V350',raw,flags=re.M)==new
    assert current[key].encode()==new
    assert hf(ROOT/'build'/Path(rel).with_suffix('.olean'))==s['author_binary_sha256']
    trans[name]={'dev_sha256':s['sha256'],'integrated_sha256':sha(new),'literal_import_rewrite_only':True,
      'embedded_bytes_equal':True,'targets':s['declarations']}
newkeys={'TGLExt/V350'+n+'.lean' for n in trans};roots={'TGLExt.lean','TGL/Audit.lean'}
assert set(current)-set(before)==newkeys and not(set(before)-set(current))
assert {k for k in before if before[k]!=current[k]}==roots
for root in roots:
    assert (ROOT/'kernel'/root).read_bytes()==current[root].encode()
    assert all(len(re.findall(r'^import TGLExt\.V350'+n+r'\s*$',current[root],re.M))==1 for n in trans)
oldnames=re.findall(r"^#print axioms ([\w.']+)",before['TGL/Audit.lean'],re.M)
newnames=re.findall(r"^#print axioms ([\w.']+)",current['TGL/Audit.lean'],re.M)
assert len(set(oldnames))==P['audit_declarations']==6659 and len(set(newnames))==6687
assert set(newnames)-set(oldnames)==set(ownax) and all(newnames.count(n)==oldnames.count(n) for n in oldnames)
oldrows={Path(r['source']).relative_to(ROOT/'kernel').as_posix():r for r in load(OLD/'integrated_compile.json')['records']}
rows=[];maps={};rowkeys=set()
for r in B['records']:
    src=Path(r['source']).resolve();assert src.is_relative_to(ROOT/'kernel')
    rel=src.relative_to(ROOT/'kernel');key=rel.as_posix();bp=ROOT/'build'/rel.with_suffix('.olean')
    assert key not in rowkeys;rowkeys.add(key)
    raw=src.read_bytes();br=bp.read_bytes()
    assert r['returncode']==0 and r['output_exists']
    if 'lean_returncode' in r:assert r['lean_returncode']==0
    assert Path(r['command'][2])==bp and Path(r['command'][3])==src
    assert sha(raw)==r['sha256'] and sha(br)==r['output_sha256'] and current[key].encode()==raw
    row={'file':key,'source_sha256':sha(raw),'binary_sha256':sha(br),'returncode':0,'timestamp':r['timestamp'],
      'same_record_as_parent':key in oldrows and r==oldrows[key], 'lean_returncode':r.get('lean_returncode'),
      'source_unchanged_during_compile':r.get('source_unchanged_during_compile')}
    write(OUT/'sources'/rel,raw)
    for k in ['stdout','stderr']:
        lp=Path(r[k]);lb=lp.read_bytes();write(OUT/'logs'/lp.name,lb);row[k+'_sha256']=sha(lb)
    log=Path(r['stdout']).with_name(Path(r['stdout']).name.replace('.stdout.txt','.json'))
    lb=log.read_bytes();assert json.loads(lb)==r;write(OUT/'logs'/log.name,lb)
    row['log_sha256']=sha(lb);row['log_name']=log.name
    text=Path(r['stdout']).read_text(encoding='utf-8');assert not re.search(r'error(?:\([^)]*\))?:',text)
    row['warnings']=[l for l in text.splitlines() if 'warning:' in l];rows.append(row)
    if key in newkeys:
        expected=trans[rel.stem[4:]]['targets'];a=axioms(text)
        assert a=={n:ownax[n] for n in expected};maps[key]=a
assert len(rows)==157 and rowkeys==set(I['added_kernel_files']+I['updated_kernel_files'])
assert sum(r['same_record_as_parent'] for r in rows)==150
newrows=[r for r in rows if r['file'] in newkeys|roots]
assert len(newrows)==7 and all(r['source_unchanged_during_compile'] is True and r['lean_returncode']==0 and not r['same_record_as_parent'] for r in newrows)
ar=next(r for r in rows if r['file']=='TGL/Audit.lean')
fullax=axioms((OUT/'logs'/ar['log_name'].replace('.json','.stdout.txt')).read_text(encoding='utf-8'))
assert len(fullax)==G['axiom_report_entries']==6687 and fullax==E['axiom_report']
allowed={'propext','Classical.choice','Quot.sound'}
assert all(set(a)<=allowed for a in fullax.values()) and all(fullax[n]==a for n,a in ownax.items())
oldax=load(OLD/'axioms.json');assert len(oldax)==6659 and set(fullax)-set(oldax)==set(ownax)
assert all(fullax[n]==a for n,a in oldax.items())
og=load(OLD/'gate_tests.json');checks={x['name']:x['passed'] for x in G['checks']};oc={x['name']:x['passed'] for x in og['checks']}
assert len(checks)==len(G['checks'])==G['passed']==86 and all(checks.values())
assert all(checks.get(n)==x for n,x in oc.items())
added=sorted(set(checks)-set(oc))
assert added==sorted(n+'_does_not_discharge_KMS_trace_or_physical_frontier' for n in ['homogeneous_right_full_scalar_weight_domain','homogeneous_right_same_GNS_adjoint_pairing'])
assert G['legacy_gate']==og['legacy_gate'] and G['frontier']==og['frontier']
assert not G['frontier']['legacy_gate_changed'] and not G['frontier']['full_plan_complete'] and not G['full_monolithic_runtime_run']
flags={k:E[k] for k in P['remaining_flags']};assert len(flags)==6 and all(x is False for x in flags.values())
surfaces={}
for p,h in MEM['surface_sha256'].items():
    raw=Path(p).read_bytes();assert sha(raw)==h
    backup=Path(MEM['backups'][p]);bb=backup.read_bytes()
    assert sha(bb)==MEM['surface_before_sha256'][p] and raw.startswith(bb) and len(raw)>len(bb)
    surfaces[p]={'sha256':h,'bytes':len(raw),'matches_immediate_DEV_custody':True,'DEV_prefix_backup_valid':True,
       'math_parent_sha256':P['surface_sha256'][p],'differs_from_math_parent':h!=P['surface_sha256'][p]}
assert len(surfaces)==34
pending=['homogeneous_right_custody.json','homogeneous_right_custody_verification.json','RELATORIO_DIREITA_MODULAR_GNS_INTEGRADA.md']
assert not any((ROOT/f).exists() for f in pending)
cfg=load(ROOT/'environment.json');original=hf(cfg['original_source'])
assert original==hf(ROOT/'fontes/um_v350_original.py')==I['base_sha256']==P['original_sha256']==MEM['original_sha256']
assert all(hf(p)==h for p,h in P['review_sha256'].items()) and hf(ROOT/'revisao/REVIEW_HOMOGENEOUS_RIGHT_GNS.md')==MEM['review_sha256']
legacy={k:{'stored_sha256':E[k],'unchanged_from_parent':E[k]==load(OLD/'kernel_incremental_evidence.json')[k],
 'equals_current_Audit_stdout':E[k]==ar['stdout_sha256']} for k in ['audit_stdout_sha256','audit_capture_sha256_full']}
assert all(x['unchanged_from_parent'] and not x['equals_current_Audit_stdout'] for x in legacy.values())
helpers={}
for f in ['prepare_homogeneous_right_stage.py','record_homogeneous_right_progress.py','verify_homogeneous_right_custody.py']:
    raw=(OUT/f).read_bytes();ast.parse(raw)
    helpers[f]={'sha256':sha(raw),'lines':len(raw.splitlines()),'static_only_not_executed_by_reviewer':True}
diffs={}
for f in ['integrate_v350.py','compile_integrated.py','test_gate_extension.py']:
    old=next(p for p in sorted(ROOT.glob(f+'.bak_*'),reverse=True) if hf(p)==P['artifacts'][f])
    a=old.read_bytes();b=(ROOT/f).read_bytes();ast.parse(b)
    diff=''.join(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile=old.name,tofile=f))
    write(OUT/(f+'.diff'),diff.encode());write(OUT/(f+'.parent'),a)
    diffs[f]={'parent_backup':str(old),'parent_sha256':sha(a),'current_sha256':sha(b)}
assert all(hf(ROOT/f)==hf(OUT/f) for f in files) and hf(ROOT/'um.py')==I['working_sha256']
result={'timestamp':datetime.datetime.now().astimezone().isoformat(),'mode':'FINAL_INTEGRATION_INSPECTION_NO_REBUILD',
 'path':str(OUT),'working_sha256':I['working_sha256'],'parent_working_sha256':P['working_sha256'],
 'parent_working_backup':str(oldum),'original_sha256':original,
 'mathematical_parent_sha256':hf(OUT/'scalar_weight_gns_custody.json'),
 'immediate_memory_parent_sha256':hf(OUT/'homogeneous_right_dev_custody.json'),'embedded_files':859,
 'transposition':trans,'all_five_import_rewrites_literal':True,'python_AST_outside_embedded_equal':True,'gate_extension_bytes_equal':True,
 'records':rows,'new_records':newrows,'integrated_records':157,'unchanged_parent_records':150,'new_author_compilations':7,
 'all_source_binary_log_stream_pins_match':True,'new_axioms_equal_own_DEV':28,'audit_distinct':6687,'parent_Audit_no_loss':True,
 'audit_all_allowed':True,'final_Audit_record':ar,'inherited_Audit_hash_fields':legacy,
 'gate_passed_author_records':86,'added_controls':added,'six_flags':flags,'legacy_gate_changed':False,'full_goal_complete':False,'full_runtime':False,
 'immediate_memory_surface_count':34,'immediate_memory_surface_pins':surfaces,'new_recorder_and_verifier_not_executed':True,
 'new_custody_and_memory_recording_not_created':pending,'helpers':helpers,'preparation_diffs':diffs,
 'original_base_read_only_reread':True,'DEV_review_sha256':MEM['review_sha256'],
 'own_DEV_verification_sha256':hf(DEV/'verification.json'),'previous_reviews_preserved':True,
 'artifact_pins':{f:hf(OUT/f) for f in files},'new_Lean_executions':0,'author_programs_executed':False}
save(OUT/'verification.json',result);save(OUT/'axioms.json',fullax);save(OUT/'new_module_axioms.json',maps)
print(json.dumps({k:result[k] for k in ['path','working_sha256','mathematical_parent_sha256','immediate_memory_parent_sha256','integrated_records','unchanged_parent_records','new_author_compilations','gate_passed_author_records','audit_distinct','all_five_import_rewrites_literal','python_AST_outside_embedded_equal','parent_Audit_no_loss']},ensure_ascii=False))
