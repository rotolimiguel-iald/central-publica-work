from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
RUN=REV/('phase_variational_final_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
PREV=Path((REV/'adjoint_polar_graph_final_latest_run.txt').read_text().strip())
FIRST=Path((REV/'phase_variational_latest_run.txt').read_text().strip())
sha=lambda b:hashlib.sha256(b).hexdigest()
hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
allowed={'propext','Classical.choice','Quot.sound'}
def write(p,b):
    assert p.resolve().is_relative_to(REV)
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes(); bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b;os.replace(tmp,p)
def save(p,d):write(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
def imports(b):return re.findall(r'^import\s+([\w.]+)',b.decode(),re.M)
def axioms(t):
    d={}
    for n,v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",t,re.S):
        a=sorted(x.strip() for x in v.split(',') if x.strip());assert n not in d or d[n]==a;d[n]=a
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",t):
        assert n not in d or not d[n];d[n]=[]
    return d
pm,pc=load(PREV/'manifest.json'),load(PREV/'compilation.json')
fm,fc=load(FIRST/'manifest.json'),load(FIRST/'compilation.json')
assert pc['complete'] and pc['all_exit_zero'] and pc['dependencies_preserved'] and pc['all_axioms_allowed']
assert fc['complete'] and fc['all_exit_zero'] and fc['exact_12_targets'] and fc['binary_equal_author']
assert fc['external_direct_pins_preserved'] and fc['all_axioms_allowed']
pkg=fm['lean_path'].split(os.pathsep)[1:]
assert len(pkg)==8 and pkg==pm['lean_path'].split(os.pathsep)[1:] and all('.lake\\packages\\' in x for x in pkg)
draftpath=ROOT/'phase_variational_draft_status.json';draft=load(draftpath)
parentpath=Path(draft['parent_custody_path']);parent=load(parentpath)
pvpath=ROOT/'adjoint_polar_graph_custody_verification.json';pv=load(pvpath)
assert hf(parentpath)==draft['parent_custody_sha256']==pv['custody_sha256'] and pv['custody_ok']
assert hf(ROOT/'um.py')==parent['working_sha256']==draft['integrated_working_sha256']
assert hf(ROOT/'gate_extension.py')==parent['artifacts']['gate_extension.py']
assert len(parent['remaining_flags'])==6 and all(v is False for v in parent['remaining_flags'].values())
assert hf(draft['report_path'])==draft['report_sha256']
assert set(draft['modules'])=={'RealPhaseVariational','ScalarPhaseVariational'}
assert sum(d['targets'] for d in draft['modules'].values())==len(draft['targets'])==21
readonly={str(p):hf(p) for p in [draftpath,parentpath,pvpath,Path(draft['report_path']),ROOT/'um.py',ROOT/'gate_extension.py',PREV/'manifest.json',PREV/'compilation.json',FIRST/'manifest.json',FIRST/'compilation.json',REV/'REVIEW_PHASE_VARIATIONAL_DEV.md']}
for p in [draftpath,parentpath,pvpath,Path(draft['report_path'])]:write(RUN/p.name,p.read_bytes())
sources={};raws={};targets=[];authorax={};history=[]
for name,d in draft['modules'].items():
    lp=Path(d['final_log']);lr=load(lp);src=ROOT/'kernel/TGLV350'/(name+'.lean');raw=src.read_bytes();ab=Path(lr['command'][2])
    assert lr['returncode']==lr['lean_returncode']==0 and lr['output_exists'] and lr['source_unchanged_during_compile']
    assert Path(lr['source'])==src and sha(raw)==lr['sha256']==d['source_sha256']
    assert hf(ab)==lr['output_sha256']==d['binary_sha256'] and hf(lp)==d['final_log_sha256']
    assert hf(lr['stdout'])==d['stdout_sha256'] and hf(lr['stderr'])==d['stderr_sha256']
    ns=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)$',raw.decode(),re.M)]
    assert len(ns)==len(set(ns))==d['targets']
    stripped=re.sub(r'/\-.*?\-/','',raw.decode(),flags=re.S);stripped=re.sub(r'--[^\n]*','',stripped)
    assert not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]',stripped)
    ax=axioms(Path(lr['stdout']).read_text(encoding='utf-8'))
    assert set(ax)==set(ns) and all(set(a)<=allowed for a in ax.values()) and not Path(lr['stderr']).read_bytes()
    targets.extend(ns);authorax.update(ax)
    rel='TGLV350/'+name+'.lean';snap=RUN/'sources'/rel;write(snap,raw);raws['TGLV350.'+name]=raw
    sources[rel]={'path':str(src),'snapshot':str(snap),'sha256':sha(raw),'declarations':ns,'imports':imports(raw),'author_binary':str(ab),'author_binary_sha256':hf(ab),'author_log':str(lp),'author_log_sha256':hf(lp),'author_stdout_sha256':d['stdout_sha256'],'author_stderr_sha256':d['stderr_sha256']}
    for p in [src,ab,lp,Path(lr['stdout']),Path(lr['stderr'])]:readonly[str(p)]=hf(p)
    for p in [lp,Path(lr['stdout']),Path(lr['stderr'])]:write(RUN/'author_final'/p.name,p.read_bytes())
    all_logs=sorted((ROOT/'logs').glob(name+'_*.json'))
    assert {str(p) for p in all_logs if load(p)['returncode']!=0}==set(d['failed_attempts'])
    for hp in all_logs:
        hr=load(hp);write(RUN/'author_history'/hp.name,hp.read_bytes())
        row={'module':name,'log':str(hp),'log_sha256':hf(hp),'returncode':hr['returncode'],'source_sha256':hr['sha256'],'accepted_final':hp==lp}
        for k in ['stdout','stderr']:
            b=Path(hr[k]).read_bytes();write(RUN/'author_history'/Path(hr[k]).name,b);row[k+'_sha256']=sha(b)
        history.append(row)
assert len(set(targets))==21 and authorax==draft['targets']
assert sum(d['returncode']!=0 for d in history)==6
assert fm['source_sha256']==sources['TGLV350/RealPhaseVariational.lean']['sha256']
fr=fc['records'][0];realbin=Path(fr['command'][2]);assert hf(realbin)==fm['author_binary_sha256']==fr['output_sha256']
write(RUN/'build/TGLV350/RealPhaseVariational.olean',realbin.read_bytes())
for cp in realbin.parent.glob(realbin.name+'.*'):
    if cp.is_file():write(RUN/'build/TGLV350'/cp.name,cp.read_bytes())
catalog={n:{**d,'source':d['frozen_source'],'binary':d['frozen_binary']} for n,d in pm['dependencies'].items()}
SECONDARY=REV/'closed_scalar_tomita_independent_20260912_100020_793911'
sm,sc=load(SECONDARY/'manifest.json'),load(SECONDARY/'compilation.json')
assert sc['complete'] and sc['all_exit_zero'] and sc['all_axioms_allowed'] and sc['dependencies_unchanged']
assert sm['compiler_sha256']==fm['compiler_sha256']
for n,d in sm['dependencies'].items():
    catalog.setdefault(n,{**d,'source':d['frozen_source'],'binary':d['frozen_binary'],'reviewer_origin':d.get('reviewer_origin',str(SECONDARY))})
for rel,d in sm['sources'].items():
    rec=next(x for x in sc['records'] if x['module']==rel)
    assert rec['returncode']==0 and rec['source_sha256']==d['sha256']
    catalog.setdefault(rel[:-5].replace('/','.'),{'source':d['snapshot'],'binary':rec['command'][2],'source_sha256':d['sha256'],'sha256':rec['output_sha256'],'reviewer_origin':str(SECONDARY)})
for p in [SECONDARY/'manifest.json',SECONDARY/'compilation.json']:readonly[str(p)]=hf(p)
needed=set();seen=set()
def visit(n):
    if n in seen:return
    seen.add(n)
    if n in raws:b=raws[n]
    elif n.split('.')[0] in {'TGL','TGLExt','TGLV350'}:
        assert n in catalog,n;needed.add(n);b=Path(catalog[n]['source']).read_bytes()
    else:return
    for x in imports(b):visit(x)
for n in raws:visit(n)
deps={}
for n in sorted(needed):
    d=catalog[n];sp=Path(d['source']);bp=Path(d['binary']);s=sp.read_bytes();b=bp.read_bytes()
    assert sp.resolve().is_relative_to(REV) and bp.resolve().is_relative_to(REV)
    assert sha(s)==d['source_sha256'] and sha(b)==d['sha256'],n
    rel=Path(*n.split('.'));live=(ROOT/'kernel'/rel.with_suffix('.lean')).read_bytes()
    if live!=s:
        assert d.get('previously_reviewed_comment_only_erratum') is True,n
        assert s.replace(d['frozen_old_comment'].encode(),d['live_corrected_comment'].encode())==live,n
    ds=RUN/'dependency_sources'/rel.with_suffix('.lean');db=RUN/'build'/rel.with_suffix('.olean')
    write(ds,s);write(db,b);companions={}
    for cp in bp.parent.glob(bp.name+'.*'):
        if cp.is_file():
            cb=cp.read_bytes();dest=db.with_name(cp.name);write(dest,cb);companions[str(dest)]=sha(cb)
    deps[n]={**d,'frozen_source':str(ds),'frozen_binary':str(db),'live_source_sha256':sha(live),'companions':companions,'inherited_from':str(PREV)}
external=fm['external_direct_pins']
for d in external.values():assert hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256']
cfg=load(ROOT/'environment.json');assert hf(cfg['lean'])==fm['compiler_sha256']==pm['compiler_sha256']
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+pkg)
assert str(ROOT/'build') not in env['LEAN_PATH']
(RUN/'tmp').mkdir();env['TMP']=env['TEMP']=str(RUN/'tmp')
aud='import TGLV350.ScalarPhaseVariational\n'+''.join('set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n' for n in targets)
write(RUN/'sources/PhaseVariationalAudit21.lean',aud.encode())
manifest={'run':str(RUN),'timestamp':datetime.datetime.now().astimezone().isoformat(),'scope':'FINAL_DEV_TWO_MODULES_21_TARGETS_CONCRETE_ONLY_NEW_COMPILE','sources':sources,'declarations':targets,'author_axioms':authorax,'dependencies':deps,'external_direct_pins':external,'readonly_pins':readonly,'compiler':cfg['lean'],'compiler_sha256':fm['compiler_sha256'],'lean_version':fm['lean_version'],'lean_path':env['LEAN_PATH'],'author_project_build_on_lean_path':False,'previous_own_dependencies':str(PREV),'previous_manifest_sha256':hf(PREV/'manifest.json'),'inherited_real_review':{'run':str(FIRST),'manifest_sha256':hf(FIRST/'manifest.json'),'compilation_sha256':hf(FIRST/'compilation.json'),'binary_sha256':hf(realbin)},'stage_draft_sha256':hf(draftpath),'parent_custody_sha256':hf(parentpath),'parent_full_reaudit':False,'packages_rebuilt':False,'memory_writes':False}
manifest['secondary_own_catalog']={'run':str(SECONDARY),'manifest_sha256':hf(SECONDARY/'manifest.json'),'compilation_sha256':hf(SECONDARY/'compilation.json')}
manifest['setup_attempt_excluded']=str(REV/'phase_variational_final_independent_20260913_034651_923295/setup_failure.json')
save(RUN/'manifest.json',manifest);save(RUN/'author_history.json',history)
write(REV/'phase_variational_final_latest_run.txt',str(RUN).encode())
print(json.dumps({'run':str(RUN),'new_modules':1,'inherited_module':1,'project_dependencies':len(deps),'targets':len(targets),'author_failures_excluded':6}),flush=True)
records=[]
for rel in ['TGLV350/ScalarPhaseVariational.lean','PhaseVariationalAudit21.lean']:
    sp=RUN/'sources'/rel;bp=RUN/'build'/Path(rel).with_suffix('.olean');bp.parent.mkdir(parents=True,exist_ok=True);assert not bp.exists()
    cmd=[cfg['lean'],'-o',str(bp),str(sp)];start=time.monotonic();r=subprocess.run(cmd,cwd=RUN/'sources',env=env,capture_output=True)
    out=RUN/'logs'/(Path(rel).stem+'.stdout.txt');err=RUN/'logs'/(Path(rel).stem+'.stderr.txt');write(out,r.stdout);write(err,r.stderr)
    ax=axioms(r.stdout.decode('utf-8',errors='replace'));expected=sources[rel]['declarations'] if rel in sources else targets
    row={'module':rel,'command':cmd,'returncode':r.returncode,'seconds':round(time.monotonic()-start,3),'source_sha256':hf(sp),'output_sha256':hf(bp) if bp.exists() else None,'stdout':str(out),'stderr':str(err),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'axioms':ax,'exact_targets':set(ax)==set(expected),'axioms_match_author':ax=={n:authorax[n] for n in expected},'axioms_allowed':bool(ax) and all(set(x)<=allowed for x in ax.values())}
    if rel in sources:row['binary_equals_author']=row['output_sha256']==sources[rel]['author_binary_sha256']
    records.append(row);save(RUN/'compilation.json',{'complete':False,'records':records})
    print(json.dumps({k:row[k] for k in ['module','returncode','seconds','exact_targets','axioms_allowed']}),flush=True)
    if r.returncode:print(r.stdout.decode('utf-8',errors='replace'),flush=True);break
result={'complete':len(records)==2,'records':records,'all_exit_zero':len(records)==2 and all(x['returncode']==0 for x in records),'exact_21_targets':len(records)==2 and all(x['exact_targets'] for x in records),'all_axioms_allowed':all(x['axioms_allowed'] for x in records),'all_axioms_match_author':all(x['axioms_match_author'] for x in records),'binary_equal_author':records[0].get('binary_equals_author',False),'inherited_real_binary_preserved':hf(RUN/'build/TGLV350/RealPhaseVariational.olean')==fr['output_sha256'],'source_snapshots_preserved':all(hf(d['snapshot'])==d['sha256'] for d in sources.values()),'readonly_artifacts_preserved':all(hf(p)==h for p,h in readonly.items()),'dependencies_preserved':all(hf(d['frozen_source'])==d['source_sha256'] and hf(d['frozen_binary'])==d['sha256'] and hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['sha256'] and all(hf(p)==h for p,h in d['companions'].items()) for d in deps.values()),'external_direct_pins_preserved':all(hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256'] for d in external.values())}
save(RUN/'compilation.json',result);print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
