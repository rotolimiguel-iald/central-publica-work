from pathlib import Path
from collections import Counter
import ast, datetime, difflib, hashlib, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
OUT=REV/('square_resolvent_integrated_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
DEV=REV/'square_adjoint_final_independent_20260913_054955_334589'
PARENT_RUN=REV/'bidual_right_support_integrated_20260913_043432_221716'
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
def save(p,x):write(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def parse(b):
    t=ast.parse(b);ns=[n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(z,ast.Name) and z.id=='_EMBEDDED_KERNEL_FILES' for z in n.targets)]
    assert len(ns)==1;d=ast.literal_eval(ns[0].value);ns[0].value=ast.Constant('EXCLUDED_EMBEDDED_LEAN')
    return d,ast.dump(t,include_attributes=False)
files=['integration.json','bidual_right_support_custody.json','bidual_right_support_custody_verification.json','square_resolvent_draft_status.json','RELATORIO_RESOLVENTES_QUADRADOS_TESTE_ORIGINAL_DEV.md','make_square_resolvent_helpers.py','record_square_resolvent_draft.py','prepare_square_resolvent_stage.py','record_square_resolvent_progress.py','verify_square_resolvent_custody.py','PROXIMA_ETAPA_BLOCOS_GUIA_DE_TIPOS.md','integrate_v350.py','compile_integrated.py','test_gate_extension.py','gate_extension.py','environment.json']
for n in files:write(OUT/n,(ROOT/n).read_bytes())
P=load(OUT/'bidual_right_support_custody.json');PV=load(OUT/'bidual_right_support_custody_verification.json');D=load(OUT/'square_resolvent_draft_status.json');I=load(OUT/'integration.json');M=load(DEV/'manifest.json');C=load(DEV/'compilation.json');env=load(OUT/'environment.json')
assert PV['custody_ok'] and PV['custody_sha256']==hf(OUT/'bidual_right_support_custody.json')==D['parent_custody_sha256']
assert D['integrated_working_sha256']==P['working_sha256'] and hf(OUT/'square_resolvent_draft_status.json')==M['draft_sha256']
assert C['complete'] and C['all_exit_zero'] and C['exact_5_and_20_targets'] and C['all_axioms_allowed'] and C['new_binary_equal_author'] and C['inherited_two_binaries_preserved']
assert D['report_sha256']==hf(OUT/'RELATORIO_RESOLVENTES_QUADRADOS_TESTE_ORIGINAL_DEV.md')
review=REV/'REVIEW_SQUARE_RESOLVENT_DEV.md';write(OUT/'REVIEW_SQUARE_RESOLVENT_DEV.frozen.md',review.read_bytes())
assert 'SQUARE_RESOLVENT_DEV_REVIEW' in review.read_text(encoding='utf-8')
oldum=next(p for p in sorted(ROOT.glob('um.py.bak_*'),reverse=True) if hf(p)==P['working_sha256'])
old,oldast=parse(oldum.read_bytes());raw=(ROOT/'um.py').read_bytes();cur,newast=parse(raw)
assert oldast==newast and sha(raw)==I['working_sha256'] and len(cur)==I['embedded_files']==918
trans={};newmods=[]
for n,d in D['modules'].items():
    devrel='TGLV350/'+n+'.lean';key='TGLExt/V350'+n+'.lean';b=(ROOT/'kernel'/devrel).read_bytes();ib=(ROOT/'kernel'/key).read_bytes()
    assert b==Path(M['sources'][devrel]['snapshot']).read_bytes() and sha(b)==d['source_sha256']
    ownbin=DEV/'build'/Path(devrel).with_suffix('.olean')
    assert hf(ownbin)==hf(ROOT/'build'/Path(devrel).with_suffix('.olean'))==d['binary_sha256']
    assert re.sub(rb'^import TGLV350\.',b'import TGLExt.V350',b,flags=re.M)==ib==cur[key].encode()
    write(OUT/'sources'/key,ib);newmods.append(key[:-5].replace('/','.'))
    trans[n]={'dev_sha256':sha(b),'integrated_sha256':sha(ib),'own_DEV_binary':str(ownbin),'own_DEV_binary_sha256':hf(ownbin),'literal_import_rewrite_only':True,'embedded_bytes_equal':True,'targets':d['targets']}
rootkeys={'TGLExt.lean','TGL/Audit.lean'};newkeys={'TGLExt/V350'+n+'.lean' for n in D['modules']}
assert set(cur)-set(old)==newkeys and not(set(old)-set(cur)) and {k for k in old if old[k]!=cur[k]}==rootkeys
for key in rootkeys:
    assert (ROOT/'kernel'/key).read_bytes()==cur[key].encode()
    assert all(len(re.findall(r'^import TGLExt\.V350'+n+r'\s*$',cur[key],re.M))==1 for n in D['modules'])
    write(OUT/'sources'/key,cur[key].encode())
    write(OUT/(key.replace('/','_')+'.diff'),''.join(difflib.unified_diff(old[key].splitlines(True),cur[key].splitlines(True),fromfile=key+'.parent',tofile=key)).encode())
oa=re.findall(r"^#print axioms ([\w.']+)",old['TGL/Audit.lean'],re.M);na=re.findall(r"^#print axioms ([\w.']+)",cur['TGL/Audit.lean'],re.M)
assert len(set(oa))==P['audit_declarations']==7086 and len(set(na))==7106 and set(na)-set(oa)==set(D['targets'])
assert all(Counter(na)[n]==v for n,v in Counter(oa).items())
diffs={}
for n in ['integrate_v350.py','compile_integrated.py','test_gate_extension.py']:
    bp=next(p for p in sorted(ROOT.glob(n+'.bak_*'),reverse=True) if hf(p)==P['artifacts'][n]);a=bp.read_bytes();b=(OUT/n).read_bytes()
    ast.parse(b);write(OUT/(n+'.parent'),a);write(OUT/(n+'.diff'),''.join(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile=bp.name,tofile=n)).encode())
    diffs[n]={'parent_backup':str(bp),'parent_sha256':sha(a),'current_sha256':sha(b)}
assert hf(OUT/'gate_extension.py')==P['artifacts']['gate_extension.py']
for n in files:
    if n.endswith('.py'):ast.parse((OUT/n).read_bytes())
it=ast.parse((OUT/'integrate_v350.py').read_bytes());batch=ast.literal_eval(next(n.value for n in it.body if isinstance(n,ast.Assign) and any(isinstance(z,ast.Name) and z.id=='tomita_batch' for z in n.targets)))
assert batch[-3:]==list(D['modules']) and len(batch)==len(set(batch))
bt=sum(len(re.findall(r'^#print axioms ',(ROOT/'kernel/TGLV350'/(n+'.lean')).read_text(encoding='utf-8'),re.M)) for n in batch);assert bt==749
surfaces={}
for p,h in P['surface_sha256'].items():assert hf(p)==h;surfaces[p]=h
assert len(surfaces)==34 and all(hf(p)==h for p,h in P['review_sha256'].items())
assert all(v is False for v in P['remaining_flags'].values())
assert not any((ROOT/n).exists() for n in ['square_resolvent_custody.json','square_resolvent_custody_verification.json','RELATORIO_RESOLVENTES_QUADRADOS_TESTE_ORIGINAL_INTEGRADA.md'])
assert hf(env['original_source'])==hf(ROOT/'fontes/um_v350_original.py')==P['original_sha256']==I['base_sha256']
tree=ast.parse(raw);sel={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['evaluate_quantum_gravity_closure','prove_qg_closure_gate','evaluate_v350_kernel_frontier']};assert len(sel)==3
for name,node in sel.items():write(OUT/'gate_AST'/(name+'.py.txt'),ast.get_source_segment(raw.decode(),node).encode())
evaln=sel['evaluate_quantum_gravity_closure'];assert [a.arg for a in evaln.args.args]==['formal','physics','experiment']
assert not any(isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value.startswith(('qgf_','gpf_')) for n in ast.walk(evaln))
caller=sel['prove_qg_closure_gate'];assigns={n.targets[0].id:n for n in caller.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
assert 'qgc_' in ast.unparse(assigns['formal']) and 'qgp_' in ast.unparse(assigns['physics']) and 'experiment_feed' in ast.unparse(assigns['_feed'])
assert ast.unparse(assigns['gate'].value)=='evaluate_quantum_gravity_closure(formal, physics, experiment)'
annex=next(n for n in caller.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Subscript) and ast.unparse(n.targets[0])=="gate['kernel_frontier']");assert annex.lineno>assigns['gate'].lineno

# Freeze dependency closure. Never rename DEV oleans to integrated module names.
pb=PARENT_RUN/'integrated_compile.json';assert hf(pb)==P['artifacts']['integrated_compile.json'];PB=load(pb);write(OUT/'parent_integrated_compile.json',pb.read_bytes())
parentrows={str(Path(x['source']).relative_to(ROOT/'kernel').with_suffix('')).replace('\\','.').replace('/','.'):x for x in PB['records']}
newmods+=['TGLExt','TGL.Audit'];needed={};externals=set()
def imports(text):
    out=[]
    for line in text.splitlines():
        if re.match(r'^\s*(?:public\s+|private\s+)?import\s+',line):
            line=re.sub(r'^\s*(?:public\s+|private\s+)?import\s+','',line).split('--')[0]
            out.extend(line.split())
    return out
def visit(mod):
    if mod in needed:return
    key=mod.replace('.','/')+'.lean'
    if key not in cur:externals.add(mod);return
    assert (ROOT/'kernel'/key).read_bytes()==cur[key].encode(),key
    needed[mod]=key
    for imp in imports(cur[key]):visit(imp)
for n in newmods:visit(n)
deps={};kindcounts={}
basebin=Path(env['lean_path'][1]);compiler=Path(env['lean']);assert hf(compiler)==M['compiler_sha256']
for mod,key in needed.items():
    if mod in newmods:continue
    rel=Path(key).with_suffix('.olean');src=ROOT/'kernel'/key
    if mod in M['dependencies'] and hf(src)==M['dependencies'][mod]['source_sha256']:
        row=M['dependencies'][mod];bp=Path(row['frozen_binary']);assert hf(bp)==row['binary_sha256'];kind='OWN_PREVIOUS_PINNED_TREE'
    elif mod in parentrows:
        row=parentrows[mod];bp=ROOT/'build'/rel;assert row['returncode']==0 and row['output_exists'] and hf(src)==row['sha256'] and hf(bp)==row['output_sha256'];kind='AUTHOR_INTEGRATED_PARENT_CUSTODY_NOT_REBUILT'
    else:
        bp=basebin/rel;assert bp.exists(),(mod,bp)
        assert key in old and cur[key]==old[key];kind='CANONICAL_BASE_READONLY_NOT_INDEPENDENTLY_REBUILT'
    dest=OUT/'build'/rel;write(dest,bp.read_bytes());write(OUT/'dependency_sources'/key,src.read_bytes())
    companions={}
    for suffix in ['.olean.server','.olean.private','.olean.hash']:
        cp=bp.with_suffix(suffix)
        if cp.exists():to=dest.with_suffix(suffix);write(to,cp.read_bytes());companions[str(to)]=hf(cp)
    deps[mod]={'source':str(src),'source_sha256':hf(src),'origin_binary':str(bp),'binary_sha256':hf(bp),'frozen_binary':str(dest),'frozen_source':str(OUT/'dependency_sources'/key),'provenance':kind,'companions':companions}
    kindcounts[kind]=kindcounts.get(kind,0)+1
externalpins={}
packagepaths=env['lean_path'][2:]
for mod in sorted(externals):
    rel=Path(mod.replace('.','/')).with_suffix('.olean');matches=[Path(p)/rel for p in packagepaths if (Path(p)/rel).exists()]
    if not matches:
        matches=[compiler.parent.parent/'lib/lean'/rel]
    assert len(matches)==1 and matches[0].exists(),(mod,matches)
    ep=matches[0];externalpins[mod]={'binary':str(ep),'sha256':hf(ep)}
S={'timestamp':datetime.datetime.now().astimezone().isoformat(),'run':str(OUT),'status':'STATIC_VERIFIED_BUILD_TEST_FINAL_PENDING','working_sha256':I['working_sha256'],'parent_working_sha256':P['working_sha256'],'parent_working_backup':str(oldum),'parent_custody_sha256':hf(OUT/'bidual_right_support_custody.json'),'original_sha256':I['base_sha256'],'canonical_original_fresh_read':True,'embedded_files':len(cur),'transposition':trans,'python_AST_outside_embedded_equal':True,'python_AST_sha256':sha(newast.encode()),'gate_extension_equal_parent':True,'six_flags_not_direct_legacy_evaluator_inputs':True,'source_Audit_distinct':len(set(na)),'source_Audit_added':20,'source_Audit_old_multiplicities_preserved':True,'batch_targets':bt,'surface_pins':surfaces,'surface_count':34,'artifact_pins':{n:hf(OUT/n) for n in files},'preparation_diffs':diffs,'own_DEV_run':str(DEV),'own_DEV_review_sha256':hf(review),'own_DEV_compilation_sha256':hf(DEV/'compilation.json'),'dependency_provenance_counts':kindcounts,'no_author_code_executed':True,'final_review_complete':False,'P0':[],'P1':[],'P2':[],'pending':['own_five_integrated_compilations','author_final_build_and_test_notice','final_source_binary_log_stream_records','final_controls_Audit_metadata']}
assert all(hf(ROOT/n)==hf(OUT/n) for n in files) and hf(ROOT/'um.py')==I['working_sha256']
save(OUT/'static_verification.json',S)
save(OUT/'build_manifest.json',{'timestamp':S['timestamp'],'run':str(OUT),'compiler':str(compiler),'compiler_sha256':hf(compiler),'lean_path':'\u003b'.join([str(OUT/'build')]+packagepaths),'modules':newmods,'sources':{n:{'path':str(OUT/'sources'/needed[n]),'sha256':hf(OUT/'sources'/needed[n])} for n in newmods},'dependencies':deps,'external_direct_pins':externalpins,'provenance_counts':kindcounts,'author_build_path_on_LEAN_PATH':False,'author_parent_binaries_frozen_and_explicitly_inherited':True,'packages_rebuilt':False,'targets':D['targets'],'expected_full_Audit_names':sorted(set(na))})
write(REV/'square_resolvent_integrated_latest_run.txt',str(OUT).encode())
print(json.dumps({k:S[k] for k in ['run','working_sha256','embedded_files','source_Audit_distinct','surface_count','dependency_provenance_counts','pending']},ensure_ascii=False))
