"""Integration-only review: static source/AST comparisons and read-only binary/log pins."""
from pathlib import Path
import ast,datetime,difflib,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_tomita_polar_latest_run.txt').read_text().strip())
DOMAIN=Path((REV/'scalar_tomita_domain_latest_run.txt').read_text().strip())
PARENT=Path((REV/'scalar_tomita_root_latest_run.txt').read_text().strip())
OLD=max(p for p in PARENT.glob('final_integrated_*') if (p/'verification.json').exists())
DEST=RUN/('integrated_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b:hashlib.sha256(b).hexdigest();hf=lambda p:sha(Path(p).read_bytes());load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p)
def save(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))
def embedded(raw):
    t=ast.parse(raw);ns=[n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='_EMBEDDED_KERNEL_FILES' for x in n.targets)];assert len(ns)==1
    d=ast.literal_eval(ns[0].value);ns[0].value=ast.Constant('EMBEDDED_EXCLUDED');return d,ast.dump(t,include_attributes=False)
def axioms(text):
    d={}
    for n,a in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",text,re.S):
        aa=[v.strip() for v in a.split(',') if v.strip()];assert n not in d or d[n]==aa;d[n]=aa
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",text):assert n not in d or not d[n];d[n]=[]
    return d
parent=load(ROOT/'tomita_root_custody.json');oldV=load(OLD/'verification.json')
assert oldV['working_sha256']==parent['working_sha256']
files=['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json','gate_extension.py',
 'integrate_v350.py','compile_integrated.py','compile_lean.py','test_gate_extension.py','record_tomita_polar_progress.py',
 'verify_tomita_polar_custody.py','test_polar_custody_binary_check.py','polar_custody_binary_check.json',
 'tomita_root_custody.json','tomita_root_custody_verification.json','tomita_root_domain_draft_status.json','tomita_polar_draft_status.json',
 'RELATORIO_DOMINIO_RAIZ_TOMITA_DEV.md','RELATORIO_FATOR_POLAR_TOMITA_DEV.md',
 'tomita_resolvent_flip_draft_status.json','RELATORIO_TROCA_RESOLVENTE_TOMITA_DEV.md']
for f in files:write(DEST/f,(ROOT/f).read_bytes())
for f in files:
    if f.endswith('.py'):ast.parse((DEST/f).read_bytes())
for f in ['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json','gate_extension.py','integrate_v350.py','compile_integrated.py','test_gate_extension.py']:
    assert hf(OLD/f)==parent['artifacts'][f]
B=load(DEST/'integrated_compile.json');I=load(DEST/'integration.json');G=load(DEST/'gate_tests.json');E=load(DEST/'kernel_incremental_evidence.json')
assert B['incremental_build_ok'] and not B['full_monolithic_runtime_run']
oldum=next(p for p in sorted(ROOT.glob('um.py.bak_*'),reverse=True) if hf(p)==parent['working_sha256'])
before,oldast=embedded(oldum.read_bytes());current,newast=embedded((ROOT/'um.py').read_bytes())
assert oldast==newast and hf(ROOT/'um.py')==I['working_sha256']==G['working_um_sha256'] and len(current)==I['embedded_files']==841
assert (ROOT/'gate_extension.py').read_bytes()==(OLD/'gate_extension.py').read_bytes()
trans={};ownax={};devclosures=[];all_previous_reviews={}
for run,statusname,expected in [(DOMAIN,'tomita_root_domain_draft_status.json',25),(RUN,'tomita_polar_draft_status.json',16)]:
    m=load(run/'manifest.json');c=load(run/'compilation.json');cl=load(run/'closure_dev.json');st=load(DEST/statusname)
    assert c['complete'] and c['all_exit_zero'] and c['exact_'+str(expected)+'_targets'] and c['dependencies_preserved']
    assert hf(ROOT/statusname)==m['draft_status_sha256'] and st['parent_custody_sha256']==hf(ROOT/'tomita_root_custody.json')
    assert st['integrated_working_sha256']==parent['working_sha256'] and hf(cl['review_path'])==cl['review_sha256']
    assert {n:sorted(a) for n,a in c['records'][-1]['axioms'].items()}==st['targets'];ownax.update(c['records'][-1]['axioms'])
    devclosures.append(cl);all_previous_reviews.update(m['previous_reviews'])
    for rel,s in m['sources'].items():
        name=Path(rel).stem;key='TGLExt/V350'+name+'.lean';raw=Path(s['path']).read_bytes();new=(ROOT/'kernel'/key).read_bytes()
        assert sha(raw)==s['sha256'] and re.sub(rb'^import TGLV350\.',b'import TGLExt.V350',raw,flags=re.M)==new
        assert current[key].encode()==new and hf(ROOT/'build'/Path(rel).with_suffix('.olean'))==s['author_binary_sha256']
        trans[name]={'dev_sha256':s['sha256'],'integrated_sha256':sha(new),'literal_import_rewrite_only':True,'embedded_equal':True,'targets':s['declarations'],'own_run':str(run)}
assert len(trans)==9 and len(ownax)==41
newkeys={'TGLExt/V350'+n+'.lean' for n in trans}
assert set(current)-set(before)==newkeys and not(set(before)-set(current))
assert {k for k in before if before[k]!=current[k]}=={'TGLExt.lean','TGL/Audit.lean'}
for root in ['TGLExt.lean','TGL/Audit.lean']:
    raw=(ROOT/'kernel'/root).read_bytes();assert current[root].encode()==raw
    assert all(len(re.findall(r'^import TGLExt\.V350'+n+r'\s*$',raw.decode(),re.M))==1 for n in trans)
    write(DEST/(root.replace('/','_')+'.diff.txt'),'\n'.join(difflib.unified_diff(before[root].splitlines(),current[root].splitlines(),lineterm='')).encode())
ot=re.findall(r'^#print axioms ([\w.]+)',before['TGL/Audit.lean'],re.M);nt=re.findall(r'^#print axioms ([\w.]+)',current['TGL/Audit.lean'],re.M)
assert set(nt)-set(ot)==set(ownax) and len(nt)-len(ot)==41 and all(nt.count(n)==ot.count(n) for n in ot)
oldrows={r['file']:r for r in oldV['records']};rows=[];permodule={}
for r in B['records']:
    src=Path(r['source']);rel=src.relative_to(ROOT/'kernel');bp=ROOT/'build'/rel.with_suffix('.olean');raw=src.read_bytes();br=bp.read_bytes()
    assert r['returncode']==0 and r['output_exists'] and sha(raw)==r['sha256'] and sha(br)==r['output_sha256']
    o=oldrows.get(rel.as_posix());row={'file':rel.as_posix(),'source_sha256':sha(raw),'binary_sha256':sha(br),'returncode':0,'timestamp':r['timestamp'],
     'same_as_parent':bool(o and sha(raw)==o['source_sha256'] and sha(br)==o['binary_sha256']),'source_unchanged_during_compile':r.get('source_unchanged_during_compile')}
    write(DEST/'sources'/rel,raw)
    for k in ['stdout','stderr']:
        lp=Path(r[k]);lb=lp.read_bytes();write(DEST/'logs'/lp.name,lb);row[k+'_sha256']=sha(lb)
    lp=Path(r['stdout']).with_name(Path(r['stdout']).name.replace('.stdout.txt','.json'));lb=lp.read_bytes();assert json.loads(lb)==r
    write(DEST/'logs'/lp.name,lb);row['log_sha256']=sha(lb);row['log_name']=lp.name
    text=Path(r['stdout']).read_text(encoding='utf-8');assert not re.search(r'error(?:\([^)]*\))?:',text)
    row['warnings']=[l for l in text.splitlines() if 'warning:' in l];rows.append(row)
    if rel.as_posix() in newkeys:
        expected=trans[rel.stem[4:]]['targets'];ax=axioms(text);assert ax=={n:ownax[n] for n in expected};permodule[rel.as_posix()]=ax
assert len(rows)==139 and {r['file'] for r in rows}==set(I['added_kernel_files']+I['updated_kernel_files'])
newrows=[r for r in rows if r['file'] in newkeys|{'TGLExt.lean','TGL/Audit.lean'}]
assert len(newrows)==11 and all(r['source_unchanged_during_compile'] is True for r in newrows)
assert sum(r['same_as_parent'] for r in rows)==128
ar=next(r for r in rows if r['file']=='TGL/Audit.lean');ax=axioms((DEST/'logs'/ar['log_name'].replace('.json','.stdout.txt')).read_text(encoding='utf-8'))
assert len(ax)==G['axiom_report_entries']==6580 and ax==E['axiom_report']
assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in ax.values()) and all(ax[n]==a for n,a in ownax.items())
oldax=load(OLD/'axioms.json');assert set(ax)-set(oldax)==set(ownax) and all(ax[n]==a for n,a in oldax.items())
checks={c['name']:c['passed'] for c in G['checks']};og=load(OLD/'gate_tests.json');oldchecks={c['name']:c['passed'] for c in og['checks']}
assert G['passed']==len(checks)==len(G['checks'])==80 and all(checks.values()) and all(checks.get(n)==v for n,v in oldchecks.items())
added=sorted(set(checks)-set(oldchecks));assert len(added)==2
assert not G['frontier']['legacy_gate_changed'] and not G['frontier']['full_plan_complete'] and not G['full_monolithic_runtime_run'] and G['legacy_gate']==og['legacy_gate']
flags={k:E[k] for k in parent['remaining_flags']};assert len(flags)==6 and all(v is False for v in flags.values())
for f in ['integrate_v350.py','compile_integrated.py','test_gate_extension.py']:
    write(DEST/(f+'.diff.txt'),'\n'.join(difflib.unified_diff((OLD/f).read_text(encoding='utf-8').splitlines(),(DEST/f).read_text(encoding='utf-8').splitlines(),fromfile='root/'+f,tofile='polar/'+f,lineterm='')).encode())
test=ast.parse((DEST/'test_gate_extension.py').read_bytes());oldtest=ast.parse((OLD/'test_gate_extension.py').read_bytes());newentries={}
names=['exact_root_domain_and_full_energy','same_GNS_polar_antiunitary_without_modular_promotion']
for n in ast.walk(test):
    if not isinstance(n,ast.Dict):continue
    keep=[]
    for k,v in zip(n.keys,n.values):
        if isinstance(k,ast.Constant) and k.value in names:newentries[k.value]=ast.literal_eval(v)
        else:keep.append((k,v))
    n.keys=[k for k,v in keep];n.values=[v for k,v in keep]
assert len(newentries)==2 and ast.dump(test,include_attributes=False)==ast.dump(oldtest,include_attributes=False)
assert added==sorted(n+'_does_not_discharge_KMS_trace_or_physical_frontier' for n in names)
ct=ast.parse((DEST/'compile_integrated.py').read_bytes())
clist=next(ast.literal_eval(n.iter) for n in ct.body if isinstance(n,ast.For) and isinstance(n.iter,ast.List) and any(isinstance(x,ast.Constant) and x.value=='TGL/Audit.lean' for x in n.iter.elts))
assert clist[-11:]==['TGLExt/V350'+n+'.lean' for n in trans]+['TGLExt.lean','TGL/Audit.lean']
verify=ast.parse((DEST/'verify_tomita_polar_custody.py').read_bytes());rv=ast.parse((ROOT/'verify_tomita_root_custody.py').read_bytes())
for name in ['sha','verify_compile_record']:
    a=next(n for n in verify.body if isinstance(n,ast.FunctionDef) and n.name==name);b=next(n for n in rv.body if isinstance(n,ast.FunctionDef) and n.name==name)
    assert ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False)
bc=load(DEST/'polar_custody_binary_check.json');assert bc['verifier_sha256']==hf(DEST/'verify_tomita_polar_custody.py') and bc['actual_source_binary_pairs_verified']==139
assert all(bc[k] for k in ['isolated_copy_positive_control','modified_binary_rejected','restored_copy_accepted','compiled_original_binary_unchanged'])
fixture=Path(bc['fixture']).resolve();assert fixture.is_relative_to(ROOT/'tests')
reference=next(r for r in rows if r['file']=='TGLExt/V350PartialSquareEnergy.lean')
assert hf(fixture/'kernel/Control.lean')==reference['source_sha256'] and hf(fixture/'build/Control.olean')==reference['binary_sha256']
surfaces={p:{'sha256':hf(p),'bytes':Path(p).stat().st_size} for p in parent['surface_sha256']}
assert len(surfaces)==34 and all(v['sha256']==parent['surface_sha256'][p] for p,v in surfaces.items())
assert all('revisao' not in Path(p).parts for p in surfaces)
for p,h in {**all_previous_reviews,**parent['review_sha256']}.items():assert hf(p)==h
cfg=load(ROOT/'environment.json');assert hf(cfg['original_source'])==hf(ROOT/'fontes/um_v350_original.py')==I['base_sha256']==parent['original_sha256']
later=load(DEST/'tomita_resolvent_flip_draft_status.json');assert len(later['modules'])==2 and len(later['targets'])==4
assert not(set(later['targets']) & set(ax)) and not({'TGLExt/V350'+n+'.lean' for n in later['modules']} & set(current))
rec=ast.parse((DEST/'record_tomita_polar_progress.py').read_bytes())
arts=next(n.value for n in rec.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='artifact_names' for t in n.targets))
draftnames=['tomita_root_domain_draft_status.json','tomita_polar_draft_status.json'];anames=ast.literal_eval(arts.left)+draftnames
assert all((ROOT/n).is_file() for n in anames)
extra_pins={n:hf(ROOT/n) for n in anames if n not in files}
assert not any((ROOT/n).exists() for n in ['tomita_polar_custody.json','tomita_polar_custody_verification.json','RELATORIO_FATOR_POLAR_TOMITA_INTEGRADO.md'])
legacy={k:{'stored':E[k],'unchanged_from_parent':E[k]==load(OLD/'kernel_incremental_evidence.json')[k],'equals_final_stream':E[k]==ar['stdout_sha256']} for k in ['audit_stdout_sha256','audit_capture_sha256_full']}
data={'timestamp':datetime.datetime.now().astimezone().isoformat(),'path':str(DEST),'mode':'INTEGRATION_INSPECTION__NO_LEAN_OR_AUTHOR_PROGRAM_EXECUTION',
 'working_sha256':I['working_sha256'],'parent_working_sha256':parent['working_sha256'],'parent_custody_sha256':hf(DEST/'tomita_root_custody.json'),
 'original_sha256':I['base_sha256'],'embedded_files':841,'transposition':trans,'all_nine_import_rewrites_literal':True,
 'python_AST_outside_embedded_equal':True,'gate_extension_bytes_equal':True,'records':rows,'new_records':newrows,
 'all_source_binary_stream_log_pins_match':True,'integrated_records':139,'reused_records':128,'new_author_compilations':11,
 'new_axioms_equal_own_DEV':41,'audit_distinct':6580,'audit_all_trio':True,'final_Audit_stdout_sha256':ar['stdout_sha256'],
 'inherited_Audit_hash_fields':legacy,'gate_passed':80,'added_controls':added,'old_test_AST_preserved':True,'new_test_entries':newentries,
 'six_flags':flags,'legacy_gate_changed':False,'full_goal_complete':False,'full_runtime':False,
 'verifier_binary_function_same_as_corrected_parent':True,'author_binary_regression_report_pin_matches':True,'restored_fixture_pins_match':True,
 'author_negative_control_not_rerun':True,'parent_surface_count':34,'parent_surfaces_current_pins':surfaces,
 'later_DEV_metadata_only':True,'later_DEV_proofs_or_logs_inspected':False,'new_custody_not_yet_executed':True,
 'own_DEV_closures':devclosures,'previous_reviews_preserved':True,'artifacts':{f:hf(DEST/f) for f in files},
 'extra_recorder_artifact_pins_existence_only':extra_pins,'new_Lean_executions':0,'author_scripts_executed':False,'findings':[]}
save(DEST/'verification.json',data);save(DEST/'axioms.json',ax);save(DEST/'module_axioms.json',permodule)
print(json.dumps({k:v for k,v in data.items() if k not in ['transposition','records','new_records','own_DEV_closures','parent_surfaces_current_pins','artifacts','extra_recorder_artifact_pins_existence_only']},ensure_ascii=False,indent=2))
