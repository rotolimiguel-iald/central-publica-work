"""Independent static integration inspection; never executes author code or Lean."""
from pathlib import Path
import ast,datetime,difflib,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'tomita_square_latest_run.txt').read_text().strip())
M=json.loads((RUN/'manifest.json').read_bytes());C=json.loads((RUN/'compilation.json').read_bytes())
DEV=json.loads((RUN/'verification_dev.json').read_bytes());CLOSE=json.loads((RUN/'closure_dev.json').read_bytes())
STAMP=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');DEST=RUN/('integrated_'+STAMP)
sha=lambda b:hashlib.sha256(b).hexdigest()
hashfile=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p)
def save(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))
def parse(raw):
    t=ast.parse(raw);nodes=[n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='_EMBEDDED_KERNEL_FILES' for x in n.targets)]
    assert len(nodes)==1
    d=ast.literal_eval(nodes[0].value);nodes[0].value=ast.Constant('EMBEDDED_KERNEL_EXCLUDED')
    return d,ast.dump(t,include_attributes=False)
def axioms(text):
    d={}
    for n,a in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",text,re.S):
        aa=[v.strip() for v in a.split(',') if v.strip()]
        assert n not in d or d[n]==aa
        d[n]=aa
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",text):
        assert n not in d or not d[n]
        d[n]=[]
    return d

previous=load(ROOT/'closed_tomita_custody.json')
OLD=max(p for p in (REV/'closed_tomita_batch_independent_20260912_101455_759612').glob('final_integrated_*') if (p/'verification.json').exists())
OLDV=load(OLD/'verification.json')
assert OLDV['working_sha256']==previous['working_sha256']
for f in ['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json','gate_extension.py','integrate_v350.py','compile_integrated.py','test_gate_extension.py']:
    assert hashfile(OLD/f)==previous['artifacts'][f],f
files=['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json',
 'closed_tomita_custody.json','gate_extension.py','integrate_v350.py','compile_integrated.py','compile_lean.py',
 'test_gate_extension.py','record_tomita_square_progress.py','verify_tomita_square_custody.py',
 'tomita_square_draft_status.json','RELATORIO_ADJUNTO_QUADRADO_DEV.md','runtime_io_inventory.json']
for f in files:write(DEST/f,(ROOT/f).read_bytes())
B=load(DEST/'integrated_compile.json');I=load(DEST/'integration.json');G=load(DEST/'gate_tests.json');E=load(DEST/'kernel_incremental_evidence.json')
assert B['incremental_build_ok'] and not B['full_monolithic_runtime_run']
oldum=next(p for p in sorted(ROOT.glob('um.py.bak_*'),reverse=True) if hashfile(p)==previous['working_sha256'])
before,oldast=parse(oldum.read_bytes());current,newast=parse((ROOT/'um.py').read_bytes())
assert newast==oldast and hashfile(ROOT/'um.py')==I['working_sha256']==G['working_um_sha256']
assert (ROOT/'gate_extension.py').read_bytes()==(OLD/'gate_extension.py').read_bytes()
assert len(current)==I['embedded_files']==827
trans={}
for rel,s in DEV['sources'].items():
    name=Path(rel).stem;key='TGLExt/V350'+name+'.lean';raw=Path(s['path']).read_bytes();new=(ROOT/'kernel'/key).read_bytes()
    assert sha(raw)==s['sha256'] and re.sub(rb'^import TGLV350\.',b'import TGLExt.V350',raw,flags=re.M)==new
    assert current[key].encode()==new
    write(DEST/'sources'/key,new)
    trans[name]={'dev_sha256':sha(raw),'integrated_sha256':sha(new),'literal_only_import_rewrite':True,'embedded_bytes_equal':True,'targets':s['declarations']}
newkeys={'TGLExt/V350'+n+'.lean' for n in trans}
assert set(current)-set(before)==newkeys and not(set(before)-set(current))
assert {k for k in before if before[k]!=current[k]}=={'TGLExt.lean','TGL/Audit.lean'}
roots={}
for root in ['TGLExt.lean','TGL/Audit.lean']:
    raw=(ROOT/'kernel'/root).read_bytes();assert current[root].encode()==raw
    roots[root]={'source_sha256':sha(raw),'each_import_once':all(len(re.findall(r'^import TGLExt\.V350'+n+r'\s*$',raw.decode(),re.M))==1 for n in trans)}
    assert roots[root]['each_import_once']
    diff='\n'.join(difflib.unified_diff(before[root].splitlines(),current[root].splitlines(),fromfile='parent/'+root,tofile='current/'+root,lineterm=''))
    write(DEST/(root.replace('/','_')+'.diff.txt'),diff.encode())
ot=re.findall(r'^#print axioms ([\w.]+)',before['TGL/Audit.lean'],re.M);nt=re.findall(r'^#print axioms ([\w.]+)',current['TGL/Audit.lean'],re.M)
assert set(nt)-set(ot)==set(M['declarations']) and len(nt)-len(ot)==53
assert all(nt.count(n)==ot.count(n) for n in ot)

oldrows={r['file']:r for r in OLDV['records']};rows=[]
for r in B['records']:
    src=Path(r['source']);rel=src.relative_to(ROOT/'kernel');binary=ROOT/'build'/rel.with_suffix('.olean');raw=src.read_bytes();br=binary.read_bytes()
    assert r['returncode']==0 and sha(raw)==r['sha256'] and sha(br)==r['output_sha256']
    o=oldrows.get(rel.as_posix()); row={'file':rel.as_posix(),'source_sha256':sha(raw),'binary_sha256':sha(br),'returncode':0,'timestamp':r['timestamp'],
       'same_source_binary_as_previous':bool(o and sha(raw)==o['source_sha256'] and sha(br)==o['binary_sha256']),
       'source_unchanged_during_compile':r.get('source_unchanged_during_compile')}
    p=DEST/'sources'/rel
    if p.exists():assert p.read_bytes()==raw
    else:write(p,raw)
    for k in ['stdout','stderr']:
        lp=Path(r[k]);lb=lp.read_bytes();write(DEST/'logs'/lp.name,lb);row[k+'_sha256']=sha(lb)
    lp=Path(r['stdout']).with_name(Path(r['stdout']).name.replace('.stdout.txt','.json'));lb=lp.read_bytes()
    assert json.loads(lb)==r
    write(DEST/'logs'/lp.name,lb);row['log_sha256']=sha(lb);row['log_name']=lp.name
    row['warnings']=[l for l in Path(r['stdout']).read_text(encoding='utf-8').splitlines() if 'warning:' in l]
    assert not any('error:' in l for l in Path(r['stdout']).read_text(encoding='utf-8').splitlines())
    rows.append(row)
assert len(rows)==125 and {r['file'] for r in rows}==set(I['added_kernel_files']+I['updated_kernel_files'])
newfiles=newkeys|{'TGLExt.lean','TGL/Audit.lean'}
newrows=[r for r in rows if r['file'] in newfiles]
assert len(newrows)==9 and all(r['source_unchanged_during_compile'] is True for r in newrows)
assert sum(r['same_source_binary_as_previous'] for r in rows)==116
for r in newrows:
    if r['file'] in roots:roots[r['file']].update(r)
    else:
        name=Path(r['file']).stem[4:];out=DEST/'logs'/r['log_name'].replace('.json','.stdout.txt')
        ax=axioms(out.read_text(encoding='utf-8'));expected=DEV['sources']['TGLV350/'+name+'.lean']['author_axioms']
        assert ax==expected
ar=next(r for r in rows if r['file']=='TGL/Audit.lean')
ax=axioms((DEST/'logs'/ar['log_name'].replace('.json','.stdout.txt')).read_text(encoding='utf-8'))
assert len(ax)==G['axiom_report_entries']==6509 and ax==E['axiom_report']
assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in ax.values())
assert all(ax[n]==a for n,a in C['records'][-1]['axioms'].items())
oldax=load(OLD/'axioms.json')
assert set(ax)-set(oldax)==set(M['declarations']) and all(ax[n]==a for n,a in oldax.items())
checks={c['name']:c['passed'] for c in G['checks']};og=load(OLD/'gate_tests.json');oldchecks={c['name']:c['passed'] for c in og['checks']}
assert G['passed']==len(G['checks'])==len(checks)==77 and all(checks.values())
assert all(checks.get(n)==v for n,v in oldchecks.items())
addedchecks=sorted(set(checks)-set(oldchecks));assert len(addedchecks)==2
assert not G['frontier']['legacy_gate_changed'] and not G['frontier']['full_plan_complete'] and not G['full_monolithic_runtime_run']
assert G['legacy_gate']==og['legacy_gate']
flags={k:E[k] for k in previous['remaining_flags']};assert len(flags)==6 and all(v is False for v in flags.values())
for f in ['integrate_v350.py','compile_integrated.py','test_gate_extension.py']:
    diff='\n'.join(difflib.unified_diff((OLD/f).read_text(encoding='utf-8').splitlines(),(DEST/f).read_text(encoding='utf-8').splitlines(),fromfile='parent/'+f,tofile='current/'+f,lineterm=''))
    write(DEST/(f+'.diff.txt'),diff.encode())
oldtree=ast.parse((OLD/'test_gate_extension.py').read_bytes())
newtree=ast.parse((DEST/'test_gate_extension.py').read_bytes())
added_dict={}
for node in ast.walk(newtree):
    if not isinstance(node,ast.Dict):continue
    keep=[]
    for k,v in zip(node.keys,node.values):
        if isinstance(k,ast.Constant) and k.value in ['maximal_antilinear_adjoint','positive_selfadjoint_Tomita_square']:
            assert k.value not in added_dict
            added_dict[k.value]=ast.literal_eval(v)
        else:keep.append((k,v))
    node.keys=[k for k,v in keep];node.values=[v for k,v in keep]
assert len(added_dict)==2 and ast.dump(newtree,include_attributes=False)==ast.dump(oldtree,include_attributes=False)
save(DEST/'added_test_dictionary.json',added_dict)
for f in ['record_tomita_square_progress.py','verify_tomita_square_custody.py']:ast.parse((DEST/f).read_bytes())
surfaces=list(previous['surface_sha256'])+[str(ROOT/'RELATORIO_TOMITA_FECHADO_INTEGRADO.md'),str(ROOT/'ROTA_APOS_TOMITA_FECHADO.md')]
assert len(surfaces)==len(set(surfaces))==32 and all(Path(p).is_file() for p in surfaces)
surface_status={p:{'sha256':hashfile(p),'bytes':Path(p).stat().st_size} for p in surfaces}
for p in surfaces:assert p not in previous['review_sha256'] and 'revisao' not in Path(p).parts
assert not (ROOT/'tomita_square_custody.json').exists() and not(ROOT/'tomita_square_custody_verification.json').exists()
assert not(ROOT/'RELATORIO_ADJUNTO_QUADRADO_INTEGRADO.md').exists()
cfg=load(ROOT/'environment.json');oh=hashfile(cfg['original_source'])
assert oh==hashfile(ROOT/'fontes/um_v350_original.py')==I['base_sha256']==previous['original_sha256']
assert hashfile(ROOT/'closed_tomita_custody.json')==M['custody_sha256']
assert hashfile(REV/'REVIEW_SCALAR_TOMITA_ADJOINT.md')==CLOSE['review_sha256']
for p,h in previous['review_sha256'].items():assert hashfile(p)==h
for p,h in M['previous_reviews'].items():
    if Path(p)!=REV/'REVIEW_SCALAR_TOMITA_ADJOINT.md':assert hashfile(p)==h
data={'timestamp':datetime.datetime.now().astimezone().isoformat(),'path':str(DEST),
 'mode':'INDEPENDENT_STATIC_TRANSPOSE_AST_AND_AUTHOR_LOG_PIN_INSPECTION__NO_NEW_LEAN_EXECUTIONS',
 'working_sha256':I['working_sha256'],'parent_working_sha256':previous['working_sha256'],'parent_working_path':str(oldum),'original_sha256':oh,
 'python_AST_outside_embedded_equal':True,'python_AST_sha256':sha(newast.encode()),'gate_extension_byte_equal':True,
 'embedded_files':len(current),'added_embedded':sorted(newkeys),'changed_old_embedded':['TGLExt.lean','TGL/Audit.lean'],
 'transposition':trans,'roots':roots,'records':rows,'all_source_binary_log_pins_match':True,
 'integrated_records':len(rows),'reused_identical_source_binary_records':116,'new_author_compilations':9,'new_records':newrows,
 'audit_distinct':len(ax),'audit_all_axioms_allowed':True,'audit_53_equal_own_DEV':True,'old_audit_targets_preserved':True,
 'gate_controls':len(checks),'gate_passed':G['passed'],'added_controls':addedchecks,'old_controls_AST_preserved':True,
 'six_flags':flags,'legacy_gate_changed':False,'full_plan_complete':False,'full_runtime':False,
 'recorder_expected_surfaces':surface_status,'recorder_surface_count':len(surfaces),'recorder_and_verifier_syntax_valid':True,
 'new_custody_report_and_verification_absent':True,'own_DEV_closure':CLOSE,'previous_reviews_preserved':True,
 'artifacts':{f:hashfile(DEST/f) for f in files},'source_bin_PIN_scope':'125 integrated records; external packages and remaining base inherited',
 'author_programs_executed_by_reviewer':False,'Lean_executions_this_addendum':0,'other_DEV_sources_inspected':False}
save(DEST/'verification.json',data);save(DEST/'axioms.json',ax)
write(REV/('tomita_square_integration_run_'+STAMP+'.txt'),str(DEST).encode())
print(json.dumps({k:v for k,v in data.items() if k not in ['transposition','roots','records','recorder_expected_surfaces','own_DEV_closure','artifacts','new_records']},ensure_ascii=False,indent=2))
