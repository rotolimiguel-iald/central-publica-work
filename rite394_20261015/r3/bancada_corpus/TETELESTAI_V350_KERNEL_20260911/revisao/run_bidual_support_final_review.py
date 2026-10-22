from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
FIRST=Path((REV/'bidual_partial_latest_run.txt').read_text().strip())
RUN=REV/('bidual_support_final_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b:hashlib.sha256(b).hexdigest()
hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
allowed={'propext','Classical.choice','Quot.sound'}
def write(p,b):
    assert p.resolve().is_relative_to(REV)
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b;os.replace(tmp,p)
def save(p,d):write(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
def axioms(t):
    d={}
    for n,v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",t,re.S):
        a=sorted(x.strip() for x in v.split(',') if x.strip());assert n not in d or d[n]==a;d[n]=a
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",t):d[n]=[]
    return d
fm,fc=load(FIRST/'manifest.json'),load(FIRST/'compilation.json')
assert fc['complete'] and fc['all_exit_zero'] and fc['exact_2_targets'] and fc['all_axioms_allowed'] and fc['binary_equal_author'] and fc['dependencies_preserved'] and fc['external_direct_pins_preserved']
draftpath=ROOT/'bidual_right_support_draft_status.json';draft=load(draftpath)
parent=Path(draft['parent_custody_path']);pd=load(parent);report=Path(draft['report_path'])
assert hf(parent)==draft['parent_custody_sha256']==fm['parent_custody_sha256']
assert hf(report)==draft['report_sha256'] and hf(ROOT/'um.py')==draft['integrated_working_sha256']==pd['working_sha256']
assert set(draft['modules'])=={'ScalarTomitaBidual','ScalarRightFunctionalStability'}
assert len(draft['targets'])==sum(d['targets'] for d in draft['modules'].values())==9
readonly={str(p):hf(p) for p in [FIRST/'manifest.json',FIRST/'compilation.json',draftpath,parent,report,ROOT/'um.py',ROOT/'gate_extension.py']}
for p in [draftpath,parent,report]:write(RUN/p.name,p.read_bytes())
sources={};targets=[];authorax={};history=[]
for name,d in draft['modules'].items():
    lp=Path(d['final_log']);lr=load(lp);src=ROOT/'kernel/TGLV350'/(name+'.lean');raw=src.read_bytes();ab=Path(lr['command'][2])
    assert lr['returncode']==lr['lean_returncode']==0 and lr['output_exists'] and lr['source_unchanged_during_compile']
    assert Path(lr['source'])==src and sha(raw)==lr['sha256']==d['source_sha256']
    assert hf(ab)==lr['output_sha256']==d['binary_sha256'] and hf(lp)==d['final_log_sha256']
    assert hf(lr['stdout'])==d['stdout_sha256'] and hf(lr['stderr'])==d['stderr_sha256']
    ns=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)$',raw.decode(),re.M)]
    assert len(ns)==len(set(ns))==d['targets']
    ax=axioms(Path(lr['stdout']).read_text(encoding='utf-8'));assert set(ax)==set(ns) and all(set(v)<=allowed for v in ax.values())
    clean=re.sub(r'/\-.*?\-/','',raw.decode(),flags=re.S);clean=re.sub(r'--[^\n]*','',clean)
    assert not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]',clean)
    targets.extend(ns);authorax.update(ax)
    rel='TGLV350/'+name+'.lean';snap=RUN/'sources'/rel;write(snap,raw)
    sources[rel]={'path':str(src),'snapshot':str(snap),'sha256':sha(raw),'declarations':ns,'author_binary':str(ab),'author_binary_sha256':hf(ab),'author_log':str(lp),'author_log_sha256':hf(lp),'author_stdout_sha256':d['stdout_sha256'],'author_stderr_sha256':d['stderr_sha256']}
    for p in [src,ab,lp,Path(lr['stdout']),Path(lr['stderr'])]:readonly[str(p)]=hf(p)
    for p in [lp,Path(lr['stdout']),Path(lr['stderr'])]:write(RUN/'author_final'/p.name,p.read_bytes())
    logs=sorted((ROOT/'logs').glob(name+'_*.json'))
    assert {str(p) for p in logs if load(p)['returncode']!=0}==set(d['failed_attempts'])
    for p in logs:
        h=load(p);row={'module':name,'log':str(p),'log_sha256':hf(p),'returncode':h['returncode'],'accepted_final':p==lp,'source_sha256':h['sha256']}
        write(RUN/'author_history'/p.name,p.read_bytes())
        for k in ['stdout','stderr']:
            b=Path(h[k]).read_bytes();write(RUN/'author_history'/Path(h[k]).name,b);row[k+'_sha256']=sha(b)
        history.append(row)
assert authorax==draft['targets'] and len(set(targets))==9 and sum(h['returncode']!=0 for h in history)==2
firstrec=fc['records'][0];firstbin=Path(firstrec['command'][2])
assert hf(firstbin)==firstrec['output_sha256']==sources['TGLV350/ScalarTomitaBidual.lean']['author_binary_sha256']
assert hf(fm['sources']['TGLV350/ScalarTomitaBidual.lean']['snapshot'])==sources['TGLV350/ScalarTomitaBidual.lean']['sha256']
readonly[str(firstbin)]=hf(firstbin)
deps=dict(fm['dependencies'])
EXTRA=Path((REV/'adjoint_polar_graph_final_latest_run.txt').read_text().strip())
em,ec=load(EXTRA/'manifest.json'),load(EXTRA/'compilation.json')
assert ec['complete'] and ec['all_exit_zero'] and ec['all_axioms_allowed'] and ec['dependencies_preserved']
assert em['compiler_sha256']==fm['compiler_sha256']
for p in [EXTRA/'manifest.json',EXTRA/'compilation.json']:readonly[str(p)]=hf(p)
catalog={**em['dependencies'],**deps}
seen=set()
def visit(n):
    if n in seen or n.split('.')[0] not in {'TGL','TGLExt','TGLV350'}:return
    seen.add(n);assert n in catalog,n
    for x in re.findall(r'^import\s+([\w.]+)',Path(catalog[n]['frozen_source']).read_text(encoding='utf-8'),re.M):visit(x)
for x in re.findall(r'^import\s+([\w.]+)',Path(sources['TGLV350/ScalarRightFunctionalStability.lean']['snapshot']).read_text(encoding='utf-8'),re.M):visit(x)
extra_copied=[]
for n in sorted(seen-set(deps)):
    d=catalog[n];sp=Path(d['frozen_source']);bp=Path(d['frozen_binary']);s=sp.read_bytes();b=bp.read_bytes()
    assert sp.resolve().is_relative_to(REV) and bp.resolve().is_relative_to(REV)
    assert sha(s)==d['source_sha256'] and sha(b)==d['sha256']
    rel=Path(*n.split('.'));assert (ROOT/'kernel'/rel.with_suffix('.lean')).read_bytes()==s
    ds=RUN/'dependency_sources'/rel.with_suffix('.lean');db=RUN/'build'/rel.with_suffix('.olean')
    write(ds,s);write(db,b);companions={}
    for cp in bp.parent.glob(bp.name+'.*'):
        if cp.is_file():
            cb=cp.read_bytes();dest=db.with_name(cp.name);write(dest,cb);companions[str(dest)]=sha(cb)
    deps[n]={**d,'frozen_source':str(ds),'frozen_binary':str(db),'companions':companions,'additional_own_origin':str(EXTRA)}
    extra_copied.append(n)
for n,d in list(deps.items()):
    bp=Path(d['frozen_binary'])
    if bp.resolve().is_relative_to(RUN):continue
    sp=Path(d['frozen_source']);s=sp.read_bytes();b=bp.read_bytes()
    assert sha(s)==d['source_sha256'] and sha(b)==d['sha256']
    rel=Path(*n.split('.'));ds=RUN/'dependency_sources'/rel.with_suffix('.lean');db=RUN/'build'/rel.with_suffix('.olean')
    write(ds,s);write(db,b);companions={}
    for cp in bp.parent.glob(bp.name+'.*'):
        if cp.is_file():
            cb=cp.read_bytes();dest=db.with_name(cp.name);write(dest,cb);companions[str(dest)]=sha(cb)
    deps[n]={**d,'inherited_source':str(sp),'inherited_binary':str(bp),'frozen_source':str(ds),'frozen_binary':str(db),'companions':companions}
localfirst=RUN/'build/TGLV350/ScalarTomitaBidual.olean';write(localfirst,firstbin.read_bytes())
for cp in firstbin.parent.glob(firstbin.name+'.*'):
    if cp.is_file():write(localfirst.with_name(cp.name),cp.read_bytes())
def check_deps():
    return all(Path(d['frozen_source']).resolve().is_relative_to(REV) and Path(d['frozen_binary']).resolve().is_relative_to(REV)
        and hf(d['frozen_source'])==d['source_sha256'] and hf(d['frozen_binary'])==d['sha256']
        and all(hf(p)==h for p,h in d['companions'].items()) for d in deps.values())
assert check_deps()
ext=fm['external_direct_pins']
for d in ext.values():assert hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256']
compiler=fm['compiler'];assert hf(compiler)==fm['compiler_sha256']
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+fm['lean_path'].split(os.pathsep)[1:])
assert str(ROOT/'build') not in env['LEAN_PATH']
(RUN/'tmp').mkdir();env['TMP']=env['TEMP']=str(RUN/'tmp')
aud='import TGLV350.ScalarTomitaBidual\nimport TGLV350.ScalarRightFunctionalStability\n'+''.join('set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n' for n in targets)
write(RUN/'sources/BidualSupportAudit9.lean',aud.encode())
manifest={'run':str(RUN),'timestamp':datetime.datetime.now().astimezone().isoformat(),'scope':'FINAL_DEV_2_MODULES_9_TARGETS_SECOND_ONLY_NEW_COMPILE',
 'compiler':compiler,'compiler_sha256':hf(compiler),'lean_version_inherited':fm['lean_version_inherited'],'lean_path':env['LEAN_PATH'],'sources':sources,'declarations':targets,'author_axioms':authorax,
 'dependencies':deps,'external_direct_pins':ext,'readonly_pins':readonly,'needed_project_dependencies_second':sorted(seen),'own_dependency_tree':str(FIRST),'additional_own_catalog':str(EXTRA),'additional_own_dependencies_copied':extra_copied,
 'inherited_bidual':{'run':str(FIRST),'manifest_sha256':hf(FIRST/'manifest.json'),'compilation_sha256':hf(FIRST/'compilation.json'),'binary':str(firstbin),'binary_sha256':hf(firstbin)},
 'draft_sha256':hf(draftpath),'report_sha256':hf(report),'parent_custody_sha256':hf(parent),'parent_full_reaudit':False,'author_project_build_on_lean_path':False,'packages_rebuilt':False,'memory_writes':False}
save(RUN/'manifest.json',manifest);save(RUN/'author_history.json',history);write(REV/'bidual_support_final_latest_run.txt',str(RUN).encode())
print(json.dumps({'run':str(RUN),'new_modules':1,'inherited_module':1,'targets':9,'dependency_tree':len(deps),'needed_second':len(seen)}),flush=True)
records=[]
for rel in ['TGLV350/ScalarRightFunctionalStability.lean','BidualSupportAudit9.lean']:
    sp=RUN/'sources'/rel;bp=RUN/'build'/Path(rel).with_suffix('.olean');bp.parent.mkdir(parents=True,exist_ok=True);assert not bp.exists()
    cmd=[compiler,'-o',str(bp),str(sp)];start=time.monotonic();r=subprocess.run(cmd,cwd=RUN/'sources',env=env,capture_output=True)
    out=RUN/'logs'/(Path(rel).stem+'.stdout.txt');err=RUN/'logs'/(Path(rel).stem+'.stderr.txt');write(out,r.stdout);write(err,r.stderr)
    ax=axioms(r.stdout.decode('utf-8',errors='replace'));ns=sources[rel]['declarations'] if rel in sources else targets
    row={'module':rel,'command':cmd,'returncode':r.returncode,'seconds':round(time.monotonic()-start,3),'source_sha256':hf(sp),'output_sha256':hf(bp) if bp.exists() else None,'stdout':str(out),'stderr':str(err),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'axioms':ax,'exact_targets':set(ax)==set(ns),'axioms_match_author':ax=={n:authorax[n] for n in ns},'axioms_allowed':bool(ax) and all(set(x)<=allowed for x in ax.values())}
    if rel in sources:row['binary_equals_author']=row['output_sha256']==sources[rel]['author_binary_sha256']
    records.append(row);save(RUN/'compilation.json',{'complete':False,'records':records});print(json.dumps({k:row[k] for k in ['module','returncode','seconds','exact_targets','axioms_allowed']}),flush=True)
    if r.returncode:print(r.stdout.decode('utf-8',errors='replace'),flush=True);break
result={'complete':len(records)==2,'records':records,'all_exit_zero':len(records)==2 and all(x['returncode']==0 for x in records),'exact_9_targets':len(records)==2 and all(x['exact_targets'] for x in records),'all_axioms_allowed':all(x['axioms_allowed'] for x in records),'all_axioms_match_author':all(x['axioms_match_author'] for x in records),'new_binary_equal_author':records[0].get('binary_equals_author',False),'inherited_bidual_binary_preserved':hf(firstbin)==firstrec['output_sha256'],'source_snapshots_preserved':all(hf(d['snapshot'])==d['sha256'] for d in sources.values()),'readonly_artifacts_preserved':all(hf(p)==h for p,h in readonly.items()),'dependencies_preserved':check_deps(),'external_direct_pins_preserved':all(hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256'] for d in ext.values())}
save(RUN/'compilation.json',result);print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
