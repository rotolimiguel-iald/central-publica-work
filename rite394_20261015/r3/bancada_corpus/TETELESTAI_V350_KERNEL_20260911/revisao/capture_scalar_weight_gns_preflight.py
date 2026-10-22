"""Static-only integration preflight. Never execute author code or inspect a running build as final."""
from pathlib import Path
import ast,datetime,difflib,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
DEV=Path((REV/'scalar_weight_gns_latest_run.txt').read_text().strip())
OUT=REV/('scalar_weight_gns_preflight_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b:hashlib.sha256(b).hexdigest();hf=lambda p:sha(Path(p).read_bytes());load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p)
def save(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))
def embedded(raw):
    t=ast.parse(raw);ns=[n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='_EMBEDDED_KERNEL_FILES' for x in n.targets)]
    assert len(ns)==1;d=ast.literal_eval(ns[0].value)
    ns[0].value=ast.Constant('EXCLUDED_EMBEDDED_LEAN');return d,ast.dump(t,include_attributes=False)
files=['integration.json','gate_extension.py','integrate_v350.py','compile_integrated.py','test_gate_extension.py',
 'prepare_scalar_weight_gns_stage.py','record_scalar_weight_gns_progress.py','verify_scalar_weight_gns_custody.py',
 'scalar_weight_gns_draft_status.json','RELATORIO_GNS_PESO_COMPLETO_DEV.md','tomita_involution_custody.json',
 'tomita_involution_custody_verification.json']
for f in files:write(OUT/f,(ROOT/f).read_bytes())
for f in files:
    if f.endswith('.py'):ast.parse((OUT/f).read_bytes())
M=load(DEV/'manifest.json');C=load(DEV/'compilation.json');CL=load(DEV/'closure_dev.json')
P=load(OUT/'tomita_involution_custody.json');I=load(OUT/'integration.json');D=load(OUT/'scalar_weight_gns_draft_status.json')
assert C['complete'] and C['all_exit_zero'] and C['exact_60_targets'] and C['nine_binaries_equal_author']
assert hf(CL['report'])==CL['sha256'] and hf(OUT/'scalar_weight_gns_draft_status.json')==M['draft_status_sha256']
assert hf(OUT/'tomita_involution_custody.json')==D['parent_custody_sha256']==M['custody_sha256']
assert D['integrated_working_sha256']==P['working_sha256']
backups={}
for name in ['integrate_v350.py','compile_integrated.py','test_gate_extension.py']:
    p=next(p for p in sorted(ROOT.glob(name+'.bak_*'),reverse=True) if hf(p)==P['artifacts'][name])
    raw=p.read_bytes();write(OUT/'parent_scripts'/name,raw)
    backups[name]={'path':str(p),'sha256':sha(raw),'matches_parent':True}
    diff='\n'.join(difflib.unified_diff(raw.decode().splitlines(),(OUT/name).read_text(encoding='utf-8').splitlines(),fromfile='parent/'+name,tofile='current/'+name,lineterm=''))
    write(OUT/(name+'.diff.txt'),diff.encode())
oldum=next(p for p in sorted(ROOT.glob('um.py.bak_*'),reverse=True) if hf(p)==P['working_sha256'])
old,oldast=embedded(oldum.read_bytes());rawum=(ROOT/'um.py').read_bytes();new,newast=embedded(rawum)
assert oldast==newast and sha(rawum)==I['working_sha256'] and len(new)==I['embedded_files']==854
assert len(old)==845
assert hf(ROOT/'gate_extension.py')==P['artifacts']['gate_extension.py']
trans={};ownaxioms=C['records'][-1]['axioms'];allowed={'propext','Classical.choice','Quot.sound'}
assert len(ownaxioms)==60 and all(set(a)==allowed for a in ownaxioms.values())
for rel,s in M['sources'].items():
    name=Path(rel).stem;key='TGLExt/V350'+name+'.lean';raw=Path(s['path']).read_bytes();integrated=(ROOT/'kernel'/key).read_bytes()
    assert sha(raw)==s['sha256'] and re.sub(rb'^import TGLV350\.',b'import TGLExt.V350',raw,flags=re.M)==integrated
    assert new[key].encode('utf-8')==integrated
    assert hf(ROOT/'build'/Path(rel).with_suffix('.olean'))==s['author_binary_sha256']
    printed=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)',integrated.decode(),re.M)]
    assert printed==s['declarations'] and all(set(ownaxioms[n])==set(D['targets'][n]) for n in printed)
    write(OUT/'sources'/key,integrated)
    trans[name]={'dev_sha256':s['sha256'],'integrated_sha256':sha(integrated),'literal_import_rewrite_only':True,
       'embedded_bytes_equal':True,'targets':printed,'axioms_from_prior_own_DEV':{n:ownaxioms[n] for n in printed}}
newkeys={'TGLExt/V350'+n+'.lean' for n in trans}
assert set(new)-set(old)==newkeys and not(set(old)-set(new))
changed={k for k in old if old[k]!=new[k]};assert changed=={'TGLExt.lean','TGL/Audit.lean'}
for root in sorted(changed):
    raw=(ROOT/'kernel'/root).read_bytes();assert new[root].encode()==raw
    write(OUT/'sources'/root,raw);write(OUT/'parent_sources'/root,old[root].encode())
    assert all(len(re.findall(r'^import TGLExt\.V350'+n+r'\s*$',raw.decode(),re.M))==1 for n in trans)
    diff='\n'.join(difflib.unified_diff(old[root].splitlines(),new[root].splitlines(),fromfile='parent/'+root,tofile='current/'+root,lineterm=''))
    write(OUT/(root.replace('/','_')+'.diff.txt'),diff.encode())
ot=re.findall(r'^#print axioms ([\w.]+)',old['TGL/Audit.lean'],re.M);nt=re.findall(r'^#print axioms ([\w.]+)',new['TGL/Audit.lean'],re.M)
assert set(nt)-set(ot)==set(ownaxioms) and len(nt)-len(ot)==60
assert all(nt.count(n)==ot.count(n) for n in ot)
ct=ast.parse((OUT/'compile_integrated.py').read_bytes());oct=ast.parse((OUT/'parent_scripts/compile_integrated.py').read_bytes())
clist=next(n.iter for n in ct.body if isinstance(n,ast.For) and isinstance(n.iter,ast.List) and any(isinstance(x,ast.Constant) and x.value=='TGL/Audit.lean' for x in n.iter.elts))
schedule=ast.literal_eval(clist)
assert schedule[-11:]==['TGLExt/V350'+n+'.lean' for n in trans]+['TGLExt.lean','TGL/Audit.lean']
clist.elts=[n for n in clist.elts if n.value not in newkeys]
assert ast.dump(ct,include_attributes=False)==ast.dump(oct,include_attributes=False)
tt=ast.parse((OUT/'test_gate_extension.py').read_bytes());ott=ast.parse((OUT/'parent_scripts/test_gate_extension.py').read_bytes())
controls=['full_scalar_weight_GNS_completion_identification','full_scalar_weight_closed_Tomita_graph_identification'];added={}
for n in ast.walk(tt):
    if not isinstance(n,ast.Dict):continue
    keep=[]
    for k,v in zip(n.keys,n.values):
        if isinstance(k,ast.Constant) and k.value in controls:added[k.value]=ast.literal_eval(v)
        else:keep.append((k,v))
    n.keys=[k for k,v in keep];n.values=[v for k,v in keep]
assert set(added)==set(controls) and ast.dump(tt,include_attributes=False)==ast.dump(ott,include_attributes=False)
assert all('TGLV350.Regular.'+t in ownaxioms for ts in added.values() for t in ts)
it=ast.parse((OUT/'integrate_v350.py').read_bytes());oit=ast.parse((OUT/'parent_scripts/integrate_v350.py').read_bytes())
batch=next(n.value for n in it.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='tomita_batch' for t in n.targets))
beforebatch=next(ast.literal_eval(n.value) for n in oit.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='tomita_batch' for t in n.targets))
assert ast.literal_eval(batch)==beforebatch+list(trans)
batch.elts=batch.elts[:-9]
replaced=0
for n in ast.walk(it):
    if isinstance(n,ast.Constant) and n.value==302:n.value=242;replaced+=1
assert replaced==1 and ast.dump(it,include_attributes=False)==ast.dump(oit,include_attributes=False)
surfaces={}
for p,h in P['surface_sha256'].items():
    f=Path(p);raw=f.read_bytes();assert sha(raw)==h
    permitted=f.resolve().is_relative_to(ROOT) or f.resolve() in [(ROOT.parent.parent/'memory/TGL_ATLAS.md').resolve(),(ROOT.parent.parent/'memory/TGL_INDICE_VIVO.md').resolve()]
    assert permitted and 'revisao' not in f.parts
    surfaces[p]={'sha256':h,'bytes':len(raw),'permitted_by_recorder_guard':True,'parent_pin_current':True}
assert len(surfaces)==34
rec=ast.parse((OUT/'record_scalar_weight_gns_progress.py').read_bytes())
artnames=ast.literal_eval(next(n.value for n in rec.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='artifact_names' for t in n.targets)))
assert all((ROOT/n).is_file() for n in artnames)
extra={n:hf(ROOT/n) for n in artnames if n not in files and n not in ['integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json']}
assert not (ROOT/'scalar_weight_gns_custody.json').exists()
assert not (ROOT/'scalar_weight_gns_custody_verification.json').exists()
assert not (ROOT/'revisao/REVIEW_SCALAR_WEIGHT_GNS_INTEGRATED.md').exists()
cfg=load(ROOT/'environment.json');original=hf(cfg['original_source'])
assert original==hf(ROOT/'fontes/um_v350_original.py')==I['base_sha256']==P['original_sha256']
assert all(hf(p)==h for p,h in {**M['previous_reviews'],**P['review_sha256']}.items())
assert hf(CL['report'])==CL['sha256']
assert all(hf(ROOT/f)==hf(OUT/f) for f in files) and hf(ROOT/'um.py')==sha(rawum)
result={'timestamp':datetime.datetime.now().astimezone().isoformat(),'mode':'STATIC_PREFLIGHT_ONLY_BUILD_OUTPUTS_DEFERRED',
 'working_sha256':sha(rawum),'parent_working_sha256':P['working_sha256'],'original_sha256':original,
 'parent_custody_sha256':hf(OUT/'tomita_involution_custody.json'),'embedded_files':len(new),'previous_embedded_files':len(old),
 'transposition':trans,'python_AST_outside_embedded_equal':True,'gate_extension_bytes_unchanged':True,
 'unchanged_embedded_old_files':len(old)-len(changed),'changed_embedded_old_files':sorted(changed),
 'parent_script_backups':backups,'old_monolith_backup':str(oldum),'old_Audit_distinct_names':len(set(ot)),
 'new_Audit_distinct_names_in_source':len(set(nt)),'new_Audit_targets_in_source':60,'old_Audit_source_entries_preserved':True,
 'new_controls_static':added,'old_test_AST_preserved':True,'compile_schedule':schedule,'compile_logic_AST_unchanged':True,
 'integrator_only_batch_plus_60_change':True,'projected_records_from_schedule':len(schedule),
 'expected_recompiled_modules':9,'expected_recompiled_roots':2,'parent_surface_count':34,'parent_surface_pins':surfaces,
 'new_custody_not_executed':True,'final_integrated_review_not_present':True,'previous_reviews_preserved':True,
 'prior_DEV_review':CL,'artifact_pins':{f:hf(OUT/f) for f in files},'extra_recorder_pins_existence_only':extra,
 'new_Lean_executions':0,'author_programs_executed':False,'integrated_build_logs_evaluated_as_final':False,
 'integrated_binaries_validated':False,'final_controls_validated':False,'findings':[]}
save(OUT/'preflight.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['transposition','parent_surface_pins','compile_schedule','extra_recorder_pins_existence_only','artifact_pins','prior_DEV_review']},ensure_ascii=False,indent=2))
print('PREFLIGHT_PATH='+str(OUT))
