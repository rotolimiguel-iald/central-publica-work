"""Read-only final integration reconciliation; inherits the completed static preflight."""
from pathlib import Path
import ast,datetime,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
PRE=REV/'scalar_weight_gns_preflight_20260912_145351_129259'
DEV=Path((REV/'scalar_weight_gns_latest_run.txt').read_text().strip())
PAR=Path((REV/'scalar_tomita_involution_latest_run.txt').read_text().strip())
OLD=next(p for p in PAR.glob('integrated_*') if (p/'verification.json').exists())
OUT=DEV/('integrated_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
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
PREF=load(PRE/'preflight.json');P=load(ROOT/'tomita_involution_custody.json')
assert all(hf(ROOT/f)==h for f,h in PREF['artifact_pins'].items())
for f in PREF['artifact_pins']:write(OUT/f,(ROOT/f).read_bytes())
for f in ['integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json']:
    assert hf(OLD/f)==P['artifacts'][f];write(OUT/f,(ROOT/f).read_bytes())
B=load(OUT/'integrated_compile.json');G=load(OUT/'gate_tests.json');E=load(OUT/'kernel_incremental_evidence.json')
I=load(OUT/'integration.json');D=load(OUT/'scalar_weight_gns_draft_status.json')
M=load(DEV/'manifest.json');C=load(DEV/'compilation.json');CL=load(DEV/'closure_dev.json')
assert C['complete'] and C['all_exit_zero'] and C['exact_60_targets'] and hf(CL['report'])==CL['sha256']
ownax=C['records'][-1]['axioms'];assert len(ownax)==60 and {n:sorted(a) for n,a in ownax.items()}==D['targets']
assert hf(ROOT/'scalar_weight_gns_draft_status.json')==M['draft_status_sha256']
assert hf(ROOT/'tomita_involution_custody.json')==M['custody_sha256']==D['parent_custody_sha256']
assert B['incremental_build_ok'] and not B['full_monolithic_runtime_run']
oldum=Path(PREF['old_monolith_backup']);assert hf(oldum)==P['working_sha256']
before,oldast=embedded(oldum.read_bytes());current,newast=embedded((ROOT/'um.py').read_bytes())
assert oldast==newast and hf(ROOT/'um.py')==I['working_sha256']==G['working_um_sha256']==PREF['working_sha256']
assert len(current)==I['embedded_files']==854 and hf(ROOT/'gate_extension.py')==P['artifacts']['gate_extension.py']
trans={}
for rel,s in M['sources'].items():
    name=Path(rel).stem;key='TGLExt/V350'+name+'.lean';raw=Path(s['path']).read_bytes();new=(ROOT/'kernel'/key).read_bytes()
    assert sha(raw)==s['sha256'] and re.sub(rb'^import TGLV350\.',b'import TGLExt.V350',raw,flags=re.M)==new
    assert current[key].encode()==new and sha(new)==PREF['transposition'][name]['integrated_sha256']
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
assert len(set(oldnames))==6599 and len(set(newnames))==6659
assert set(newnames)-set(oldnames)==set(ownax) and all(newnames.count(n)==oldnames.count(n) for n in oldnames)
oldrows={Path(r['source']).relative_to(ROOT/'kernel').as_posix():r for r in load(OLD/'integrated_compile.json')['records']}
rows=[];maps={}
for r in B['records']:
    src=Path(r['source']).resolve();assert src.is_relative_to(ROOT/'kernel')
    rel=src.relative_to(ROOT/'kernel');key=rel.as_posix();bp=ROOT/'build'/rel.with_suffix('.olean')
    raw=src.read_bytes();br=bp.read_bytes()
    assert r['returncode']==0 and r['output_exists']
    if 'lean_returncode' in r:assert r['lean_returncode']==0
    assert sha(raw)==r['sha256'] and sha(br)==r['output_sha256']
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
    row['warnings']=[l for l in text.splitlines() if 'warning:' in l]
    rows.append(row)
    if key in newkeys:
        expected=trans[rel.stem[4:]]['targets'];a=axioms(text)
        assert a=={n:ownax[n] for n in expected};maps[key]=a
assert len(rows)==152 and {r['file'] for r in rows}==set(I['added_kernel_files']+I['updated_kernel_files'])
assert sum(r['same_record_as_parent'] for r in rows)==141
newrows=[r for r in rows if r['file'] in newkeys|roots]
assert len(newrows)==11 and all(r['source_unchanged_during_compile'] is True and r['lean_returncode']==0 and not r['same_record_as_parent'] for r in newrows)
ar=next(r for r in rows if r['file']=='TGL/Audit.lean')
fullax=axioms((OUT/'logs'/ar['log_name'].replace('.json','.stdout.txt')).read_text(encoding='utf-8'))
assert len(fullax)==G['axiom_report_entries']==6659 and fullax==E['axiom_report']
allowed={'propext','Classical.choice','Quot.sound'}
assert all(set(a)<=allowed for a in fullax.values()) and all(fullax[n]==a for n,a in ownax.items())
oldax=load(OLD/'axioms.json');assert len(oldax)==6599 and set(fullax)-set(oldax)==set(ownax)
assert all(fullax[n]==a for n,a in oldax.items())
og=load(OLD/'gate_tests.json');checks={c['name']:c['passed'] for c in G['checks']};oc={c['name']:c['passed'] for c in og['checks']}
assert len(checks)==len(G['checks'])==G['passed']==84 and all(checks.values())
assert all(checks.get(n)==v for n,v in oc.items())
added=sorted(set(checks)-set(oc))
assert added==sorted(n+'_does_not_discharge_KMS_trace_or_physical_frontier' for n in PREF['new_controls_static'])
assert G['legacy_gate']==og['legacy_gate'] and not G['frontier']['legacy_gate_changed'] and not G['frontier']['full_plan_complete']
assert not G['full_monolithic_runtime_run']
flags={k:E[k] for k in P['remaining_flags']};assert len(flags)==6 and all(v is False for v in flags.values())
surfaces={}
for p,h in P['surface_sha256'].items():
    raw=Path(p).read_bytes();assert sha(raw)==h==PREF['parent_surface_pins'][p]['sha256']
    surfaces[p]={'sha256':h,'bytes':len(raw),'matches_parent_before_any_new_recording':True}
assert len(surfaces)==34 and not any((ROOT/f).exists() for f in ['scalar_weight_gns_custody.json','scalar_weight_gns_custody_verification.json','RELATORIO_GNS_PESO_COMPLETO_INTEGRADO.md'])
cfg=load(ROOT/'environment.json');original=hf(cfg['original_source'])
assert original==hf(ROOT/'fontes/um_v350_original.py')==I['base_sha256']==P['original_sha256']
assert all(hf(p)==h for p,h in {**M['previous_reviews'],**P['review_sha256']}.items()) and hf(CL['report'])==CL['sha256']
legacy={k:{'stored_sha256':E[k],'unchanged_from_parent':E[k]==load(OLD/'kernel_incremental_evidence.json')[k],
 'equals_current_Audit_stdout':E[k]==ar['stdout_sha256']} for k in ['audit_stdout_sha256','audit_capture_sha256_full']}
assert all(v['unchanged_from_parent'] and not v['equals_current_Audit_stdout'] for v in legacy.values())
files=list(PREF['artifact_pins'])+['integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json']
assert all(hf(ROOT/f)==hf(OUT/f) for f in files) and hf(ROOT/'um.py')==PREF['working_sha256']
result={'timestamp':datetime.datetime.now().astimezone().isoformat(),'mode':'FINAL_INTEGRATION_INSPECTION_NO_REBUILD',
 'path':str(OUT),'preflight_path':str(PRE),'preflight_sha256':hf(PRE/'preflight.json'),'static_artifacts_unchanged_from_preflight':True,
 'working_sha256':I['working_sha256'],'parent_working_sha256':P['working_sha256'],'original_sha256':original,
 'parent_custody_sha256':hf(OUT/'tomita_involution_custody.json'),'embedded_files':854,
 'transposition':trans,'all_nine_import_rewrites_literal':True,'python_AST_outside_embedded_equal':True,'gate_extension_bytes_equal':True,
 'records':rows,'new_records':newrows,'integrated_records':152,'unchanged_parent_records':141,'new_author_compilations':11,
 'all_source_binary_log_stream_pins_match':True,'new_axioms_equal_own_DEV':60,'audit_distinct':6659,'parent_Audit_no_loss':True,
 'audit_all_allowed':True,'final_Audit_record':ar,'inherited_Audit_hash_fields':legacy,
 'gate_passed_author_records':84,'added_controls':added,'six_flags':flags,'legacy_gate_changed':False,'full_goal_complete':False,'full_runtime':False,
 'parent_surface_count':34,'parent_surface_pins':surfaces,'recorder_and_verifier_not_executed':True,
 'helper_full_static_read_in_preflight':True,'helper_binary_reread_preserved':True,'backup_atomicity_per_file_not_global_transaction':True,
 'original_base_read_only_reread':True,'own_DEV_closure':CL,'previous_reviews_preserved':True,
 'artifact_pins':{f:hf(OUT/f) for f in files},'new_Lean_executions':0,'author_programs_executed':False,'findings':[]}
save(OUT/'verification.json',result);save(OUT/'axioms.json',fullax);save(OUT/'new_module_axioms.json',maps)
print(json.dumps({k:v for k,v in result.items() if k not in ['transposition','records','new_records','parent_surface_pins','own_DEV_closure','artifact_pins']},ensure_ascii=False,indent=2))
