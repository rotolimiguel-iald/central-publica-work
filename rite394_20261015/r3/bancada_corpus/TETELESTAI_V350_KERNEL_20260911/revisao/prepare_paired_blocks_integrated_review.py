from pathlib import Path
from collections import Counter
import ast,datetime,difflib,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
RUN=REV/('paired_blocks_integrated_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
OLD=REV/'square_resolvent_integrated_20260913_060615_561897'
DEV=REV/'paired_blocks27_independent_20260913_070702_176639'
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p)
def save(p,x):write(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def parse(b):
    t=ast.parse(b);nodes=[n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(z,ast.Name) and z.id=='_EMBEDDED_KERNEL_FILES' for z in n.targets)]
    assert len(nodes)==1;d=ast.literal_eval(nodes[0].value);nodes[0].value=ast.Constant('EXCLUDED_EMBEDDED_LEAN')
    return d,ast.dump(t,include_attributes=False)
names=['integration.json','square_resolvent_custody.json','square_resolvent_custody_verification.json','paired_blocks_draft_status.json','RELATORIO_BLOCOS_PARES_TESTE_PONDERADO_DEV.md','record_paired_blocks_draft.py','prepare_paired_blocks_stage.py','record_paired_blocks_progress.py','verify_paired_blocks_custody.py','PROXIMA_ETAPA_COTA_BLOCOS.md','proxima_etapa_cota_blocos_pins.json','integrate_v350.py','compile_integrated.py','test_gate_extension.py','gate_extension.py','environment.json']
for n in names:write(RUN/n,(ROOT/n).read_bytes())
P=load(RUN/'square_resolvent_custody.json');PV=load(RUN/'square_resolvent_custody_verification.json');D=load(RUN/'paired_blocks_draft_status.json');I=load(RUN/'integration.json');M=load(OLD/'build_manifest.json');C=load(OLD/'compilation.json');V=load(OLD/'verification.json');DM=load(DEV/'manifest.json');DC=load(DEV/'compilation.json')
assert PV['custody_ok'] and PV['custody_sha256']==hf(RUN/'square_resolvent_custody.json')==D['parent_custody_sha256']==DM['parent_custody_sha256']
assert C['complete'] and C['all_five_exit_zero'] and C['dependencies_preserved'] and V['complete'] and V['own_integrated_binaries_equal_author']
assert hf(OLD/'compilation.json')==V['own_integrated_compilation_sha256'] and hf(OLD/'build_manifest.json')==V['own_build_manifest_sha256']
assert DC['complete'] and DC['all_exit_zero'] and DC['exact_27_targets'] and DC['all_axioms_allowed'] and DC['new_binary_equal_author']
assert hf(RUN/'paired_blocks_draft_status.json')==DM['draft_sha256'] and D['report_sha256']==hf(RUN/'RELATORIO_BLOCOS_PARES_TESTE_PONDERADO_DEV.md')
review=REV/'REVIEW_PAIRED_BLOCKS_DEV.md';rp=load(DEV/'report_pin.json');assert hf(review)==rp['sha256']
write(RUN/'REVIEW_PAIRED_BLOCKS_DEV.frozen.md',review.read_bytes())
oldum=next(p for p in sorted(ROOT.glob('um.py.bak_*'),reverse=True) if hf(p)==P['working_sha256'])
old,oa=parse(oldum.read_bytes());raw=(ROOT/'um.py').read_bytes();cur,ca=parse(raw)
assert oa==ca and sha(raw)==I['working_sha256'] and len(cur)==I['embedded_files']==922
newmods=[];trans={}
for n,d in D['modules'].items():
    key='TGLExt/V350'+n+'.lean';devkey='TGLV350/'+n+'.lean';b=(ROOT/'kernel'/devkey).read_bytes();ib=(ROOT/'kernel'/key).read_bytes()
    ob=DEV/'build'/Path(devkey).with_suffix('.olean')
    assert sha(b)==d['source_sha256'] and hf(ob)==d['binary_sha256']
    assert re.sub(rb'^import TGLV350\.',b'import TGLExt.V350',b,flags=re.M)==ib==cur[key].encode()
    write(RUN/'sources'/key,ib);newmods.append(key[:-5].replace('/','.'))
    trans[n]={'dev_sha256':sha(b),'integrated_sha256':sha(ib),'own_DEV_binary':str(ob),'own_DEV_binary_sha256':hf(ob),'literal_import_rewrite_only':True,'embedded_bytes_equal':True,'targets':d['targets']}
rootkeys={'TGLExt.lean','TGL/Audit.lean'};newkeys={'TGLExt/V350'+n+'.lean' for n in D['modules']}
assert set(cur)-set(old)==newkeys and not(set(old)-set(cur)) and {k for k in old if old[k]!=cur[k]}==rootkeys
for key in sorted(rootkeys):
    assert (ROOT/'kernel'/key).read_bytes()==cur[key].encode()
    assert all(len(re.findall(r'^import TGLExt\.V350'+n+r'\s*$',cur[key],re.M))==1 for n in D['modules'])
    write(RUN/'sources'/key,cur[key].encode())
    write(RUN/(key.replace('/','_')+'.diff'),''.join(difflib.unified_diff(old[key].splitlines(True),cur[key].splitlines(True),fromfile=key+'.parent',tofile=key)).encode())
oldnames=re.findall(r"^#print axioms ([\w.']+)",old['TGL/Audit.lean'],re.M);newnames=re.findall(r"^#print axioms ([\w.']+)",cur['TGL/Audit.lean'],re.M)
assert len(set(oldnames))==P['audit_declarations']==7106 and len(set(newnames))==7133 and set(newnames)-set(oldnames)==set(D['targets'])
assert all(Counter(newnames)[n]==v for n,v in Counter(oldnames).items())
diffs={}
for n in ['integrate_v350.py','compile_integrated.py','test_gate_extension.py']:
    bp=next(p for p in sorted(ROOT.glob(n+'.bak_*'),reverse=True) if hf(p)==P['artifacts'][n]);a=bp.read_bytes();b=(RUN/n).read_bytes()
    ast.parse(b);write(RUN/(n+'.parent'),a);write(RUN/(n+'.diff'),''.join(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile=bp.name,tofile=n)).encode())
    diffs[n]={'parent_backup':str(bp),'parent_sha256':sha(a),'current_sha256':sha(b)}
assert hf(RUN/'gate_extension.py')==P['artifacts']['gate_extension.py']
for n in names:
    if n.endswith('.py'):ast.parse((RUN/n).read_bytes())
it=ast.parse((RUN/'integrate_v350.py').read_bytes());batch=ast.literal_eval(next(n.value for n in it.body if isinstance(n,ast.Assign) and any(isinstance(z,ast.Name) and z.id=='tomita_batch' for z in n.targets)))
assert batch[-4:]==list(D['modules']) and len(batch)==len(set(batch))
bt=sum(len(re.findall(r'^#print axioms ',(ROOT/'kernel/TGLV350'/(n+'.lean')).read_text(encoding='utf-8'),re.M)) for n in batch);assert bt==776
surfaces={}
for p,h in P['surface_sha256'].items():assert hf(p)==h;surfaces[p]=h
assert len(surfaces)==34 and all(hf(p)==h for p,h in P['review_sha256'].items())
assert all(v is False for v in P['remaining_flags'].values())
assert not any((ROOT/n).exists() for n in ['paired_blocks_custody.json','paired_blocks_custody_verification.json'])
env=load(RUN/'environment.json');assert hf(env['original_source'])==hf(ROOT/'fontes/um_v350_original.py')==P['original_sha256']==I['base_sha256']
# Freeze only the required inherited closure, from the previous review tree.
newmods+=['TGLExt','TGL.Audit'];needed={};external=set()
def visit(mod):
    if mod in needed:return
    key=mod.replace('.','/')+'.lean'
    if key not in cur:external.add(mod);return
    needed[mod]=key
    for line in cur[key].splitlines():
        if re.match(r'^\s*(?:public\s+|private\s+)?import\s+',line):
            for imp in re.sub(r'^\s*(?:public\s+|private\s+)?import\s+','',line).split('--')[0].split():visit(imp)
for n in newmods:visit(n)
oldrecords={x['module']:x for x in C['records']};deps={};kinds=Counter()
for mod,key in needed.items():
    if mod in newmods:continue
    rel=Path(key).with_suffix('.olean')
    if mod in M['dependencies']:
        row=M['dependencies'][mod];sp=Path(row['frozen_source']);bp=Path(row['frozen_binary']);sh=row['source_sha256'];bh=row['binary_sha256'];kind=row['provenance']
    else:
        row=oldrecords[mod];assert row['returncode']==0 and row['output_exists'];sp=Path(M['sources'][mod]['path']);bp=OLD/'build'/rel;sh=row['source_sha256'];bh=row['output_sha256'];kind='OWN_PREVIOUS_FRESH_INTEGRATED_SQUARE_DELTA'
    assert hf(sp)==sh and hf(bp)==bh and sha(cur[key].encode())==sh and hf(ROOT/'kernel'/key)==sh,(mod,'pin mismatch')
    fs=RUN/'dependency_sources'/key;fb=RUN/'build'/rel;write(fs,sp.read_bytes());write(fb,bp.read_bytes())
    companions={}
    for suffix in ['.olean.server','.olean.private','.olean.hash']:
        cp=bp.with_suffix(suffix)
        if cp.exists():dest=fb.with_suffix(suffix);write(dest,cp.read_bytes());companions[str(dest)]=hf(cp)
    deps[mod]={'source':str(ROOT/'kernel'/key),'source_sha256':sh,'origin_binary':str(bp),'binary_sha256':bh,'frozen_binary':str(fb),'frozen_source':str(fs),'provenance':kind,'immediate_origin':'PREVIOUS_REVIEW_TREE','companions':companions};kinds[kind]+=1
compiler=M['compiler'];assert hf(compiler)==M['compiler_sha256']
packagepaths=M['lean_path'].split(';')[1:];epins={}
for mod in sorted(external):
    rel=Path(mod.replace('.','/')).with_suffix('.olean');matches=[Path(p)/rel for p in packagepaths if (Path(p)/rel).exists()]
    if not matches:matches=[Path(compiler).parent.parent/'lib/lean'/rel]
    assert len(matches)==1 and matches[0].exists(),mod
    epins[mod]={'binary':str(matches[0]),'sha256':hf(matches[0])}
for mod,pin in M['external_direct_pins'].items():assert hf(pin['binary'])==pin['sha256']
assert all(hf(ROOT/n)==hf(RUN/n) for n in names) and hf(ROOT/'um.py')==I['working_sha256']
S={'timestamp':datetime.datetime.now().astimezone().isoformat(),'run':str(RUN),'status':'STATIC_VERIFIED__OWN_BUILD_AND_AUTHOR_FINAL_PENDING','working_sha256':I['working_sha256'],'parent_working_sha256':P['working_sha256'],'parent_working_backup':str(oldum),'parent_custody_sha256':hf(RUN/'square_resolvent_custody.json'),'embedded_files':len(cur),'transposition':trans,'python_AST_outside_embedded_equal':True,'python_AST_sha256':sha(ca.encode()),'gate_extension_equal_parent':True,'source_Audit_distinct':len(set(newnames)),'source_Audit_added':len(D['targets']),'source_Audit_old_multiplicities_preserved':True,'batch_targets':bt,'surface_pins':surfaces,'surface_count':34,'original_sha256':I['base_sha256'],'canonical_original_fresh_read':True,'artifact_pins':{n:hf(RUN/n) for n in names},'preparation_diffs':diffs,'own_DEV_run':str(DEV),'own_DEV_review_sha256':hf(review),'own_DEV_compilation_sha256':hf(DEV/'compilation.json'),'dependency_provenance_counts':dict(kinds),'parent_build_manifest_sha256':hf(OLD/'build_manifest.json'),'parent_build_compilation_sha256':hf(OLD/'compilation.json'),'no_author_code_executed':True,'final_review_complete':False,'P0':[],'P1':[],'P2':[],'pending':['own_six_integrated_compilations','author_final_notice_and_current_build_test_stream_records','final_helper_and_metadata_review']}
save(RUN/'static_verification.json',S)
save(RUN/'build_manifest.json',{'timestamp':S['timestamp'],'run':str(RUN),'compiler':compiler,'compiler_sha256':hf(compiler),'lean_path':';'.join([str(RUN/'build')]+packagepaths),'modules':newmods,'sources':{n:{'path':str(RUN/'sources'/needed[n]),'sha256':hf(RUN/'sources'/needed[n])} for n in newmods},'dependencies':deps,'external_direct_pins':epins,'provenance_counts':dict(kinds),'author_build_path_on_LEAN_PATH':False,'author_parent_binaries_frozen_and_explicitly_inherited':True,'packages_rebuilt':False,'targets':D['targets'],'expected_full_Audit_names':sorted(set(newnames))})
write(REV/'paired_blocks_integrated_latest_run.txt',str(RUN).encode())
print(json.dumps({k:S[k] for k in ['run','working_sha256','embedded_files','source_Audit_distinct','surface_count','dependency_provenance_counts','pending']},ensure_ascii=False))
