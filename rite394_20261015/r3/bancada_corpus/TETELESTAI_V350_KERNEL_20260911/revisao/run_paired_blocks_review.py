from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
RUN=REV/('paired_blocks_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
PHASE=REV/'square_adjoint_final_independent_20260913_054955_334589'
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
def imports(b):return re.findall(r'^import\s+([\w.]+)',b.decode(),re.M)
def axioms(t):
    d={}
    for n,v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",t,re.S):
        a=sorted(x.strip() for x in v.split(',') if x.strip());assert n not in d or d[n]==a;d[n]=a
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",t):d[n]=[]
    return d

pm,pc=load(PHASE/'manifest.json'),load(PHASE/'compilation.json')
assert pc['complete'] and pc['all_exit_zero'] and pc['all_axioms_allowed'] and pc['dependencies_preserved'] and pc['new_binary_equal_author']
pkg=pm['lean_path'].split(os.pathsep)[1:]
assert len(pkg)==8 and all('.lake\\packages\\' in p for p in pkg)
catalog={};readonly={}
for p in [PHASE/'manifest.json',PHASE/'compilation.json']:readonly[str(p)]=hf(p)
for n,d in pm['dependencies'].items():
    catalog[n]={**d,'source':d['frozen_source'],'binary':d['frozen_binary'],'sha256':d['binary_sha256'],'immediate_own_origin':str(PHASE)}
for rel,d in pm['sources'].items():
    row=next((x for x in pc['records'] if x['module']==rel),None)
    if row is None:continue
    assert row['returncode']==0 and row['source_sha256']==d['sha256']
    catalog[rel[:-5].replace('/','.')]=dict(source=d['snapshot'],binary=row['command'][2],source_sha256=d['sha256'],sha256=row['output_sha256'],immediate_own_origin=str(PHASE))

specs=[('ScalarPairedMultiplicationGraph','20260913_063138_562066',5,1),
       ('HilbertProjectionOrder','20260913_063505_616727',8,2)]
sources={}; targets=[]; authorax={}; history=[]; raw_sources=[]; module_targets={}
for name,stamp,count,failed_count in specs:
    lp=ROOT/'logs'/f'{name}_{stamp}.json';lr=load(lp)
    src=ROOT/'kernel/TGLV350'/f'{name}.lean';raw=src.read_bytes();ab=Path(lr['command'][2])
    assert lr['returncode']==lr['lean_returncode']==0 and lr['output_exists'] and lr['source_unchanged_during_compile']
    assert Path(lr['source'])==src and sha(raw)==lr['sha256'] and hf(ab)==lr['output_sha256']
    ts=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)$',raw.decode(),re.M)]
    assert len(ts)==len(set(ts))==count
    ax=axioms(Path(lr['stdout']).read_text(encoding='utf-8'))
    assert set(ax)==set(ts) and all(set(v)<=allowed for v in ax.values())
    assert not Path(lr['stderr']).read_bytes()
    clean=re.sub(r'/\-.*?\-/','',raw.decode(),flags=re.S);clean=re.sub(r'--[^\n]*','',clean)
    assert not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]',clean)
    for p in [src,ab,lp,Path(lr['stdout']),Path(lr['stderr'])]:readonly[str(p)]=hf(p)
    for p in [lp,Path(lr['stdout']),Path(lr['stderr'])]:write(RUN/'author_final'/p.name,p.read_bytes())
    rel=f'TGLV350/{name}.lean';snap=RUN/'sources'/rel;write(snap,raw)
    sources[rel]={'path':str(src),'snapshot':str(snap),'sha256':sha(raw),'author_binary':str(ab),
      'author_binary_sha256':hf(ab),'author_log':str(lp),'author_log_sha256':hf(lp),
      'author_stdout_sha256':hf(lr['stdout']),'author_stderr_sha256':hf(lr['stderr'])}
    targets+=ts;authorax.update(ax);raw_sources.append(raw);module_targets[rel]=ts
    mh=[]
    for p in sorted((ROOT/'logs').glob(name+'_*.json')):
        d=load(p);row={'log':str(p),'log_sha256':hf(p),'returncode':d['returncode'],
          'source_sha256':d['sha256'],'accepted_final':p==lp}
        write(RUN/'author_history'/p.name,p.read_bytes())
        for k in ['stdout','stderr']:
            bb=Path(d[k]).read_bytes();write(RUN/'author_history'/Path(d[k]).name,bb);row[k+'_sha256']=sha(bb)
        mh.append(row)
    assert sum(d['returncode']!=0 for d in mh)==failed_count
    history+=mh
assert len(targets)==len(set(targets))==13
parent=ROOT/'square_resolvent_custody.json';pv=ROOT/'square_resolvent_custody_verification.json'
pd=load(parent);pvd=load(pv)
assert pvd['custody_sha256']==hf(parent) and pvd['custody_ok']
assert hf(ROOT/'um.py')==pd['working_sha256']
assert len(pd['remaining_flags'])==6 and all(v is False for v in pd['remaining_flags'].values())
assert hf(ROOT/'gate_extension.py')==pd['artifacts']['gate_extension.py']
for p in [parent,pv,ROOT/'um.py',ROOT/'gate_extension.py']:readonly[str(p)]=hf(p)
for p in [parent,pv]:write(RUN/p.name,p.read_bytes())
for p,h in pd['review_sha256'].items():assert hf(p)==h;readonly[p]=h
for p,h in pd['surface_sha256'].items():assert hf(p)==h;readonly[p]=h
assert len(pd['surface_sha256'])==34

needed=set()
def visit(n):
    if n in needed or n.split('.')[0] not in {'TGL','TGLExt','TGLV350'}:return
    assert n in catalog,n
    needed.add(n)
    for x in imports(Path(catalog[n]['source']).read_bytes()):visit(x)
for raw in raw_sources:
    for n in imports(raw):visit(n)
deps={}
for n in sorted(needed):
    d=catalog[n];sp=Path(d['source']);bp=Path(d['binary']);s=sp.read_bytes();b=bp.read_bytes()
    assert sp.resolve().is_relative_to(REV) and bp.resolve().is_relative_to(REV)
    assert sha(s)==d['source_sha256'] and sha(b)==d['sha256'],n
    rel=Path(*n.split('.'));live=(ROOT/'kernel'/rel.with_suffix('.lean')).read_bytes()
    if live!=s:
        assert n=='TGLV350.DualSemifiniteIdeal',n
        old_comment=b'/-- A single bound for all vectors: this is finiteness of the output form\nas a bounded operator, not just finiteness on a chosen vector domain. -/'
        new_comment=b'/-- A single bound for all vectors: the output is a uniformly bounded\nquadratic form, not just finite on a chosen vector domain. Realization by\na bounded operator in the fixed algebra is a separate obligation. -/'
        if b'\r\n' in s:old_comment=old_comment.replace(b'\n',b'\r\n');new_comment=new_comment.replace(b'\n',b'\r\n')
        assert s.count(old_comment)==1 and s.replace(old_comment,new_comment)==live,n
        d={**d,'previously_reviewed_comment_only_erratum':True,'frozen_old_comment':old_comment.decode(),
           'live_corrected_comment':new_comment.decode(),'exact_literal_replacement_verified':True}

    ds=RUN/'dependency_sources'/rel.with_suffix('.lean');db=RUN/'build'/rel.with_suffix('.olean')
    write(ds,s);write(db,b);companions={}
    for cp in bp.parent.glob(bp.name+'.*'):
        if cp.is_file():
            cb=cp.read_bytes();dest=db.with_name(cp.name);write(dest,cb);companions[str(dest)]=sha(cb)
    deps[n]={**d,'frozen_source':str(ds),'frozen_binary':str(db),'live_source_sha256':sha(live),'companions':companions}
external=pm['external_direct_pins']
# Direct Mathlib import added by the second module; only read the installed package.
for n in sorted({x for raw in raw_sources for x in imports(raw) if x.startswith('Mathlib.')}):
    pp=next(Path(p) for p in pkg if (Path(p)/Path(*n.split('.')).with_suffix('.olean')).exists())
    bp=pp/Path(*n.split('.')).with_suffix('.olean')
    sp=pp.parents[3]/Path(*n.split('.')).with_suffix('.lean')
    assert sp.exists(),str(sp)
    external[n]={'source':str(sp),'binary':str(bp),'source_sha256':hf(sp),'binary_sha256':hf(bp)}
for d in external.values():assert hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256']
compiler=pm['compiler'];assert hf(compiler)==pm['compiler_sha256']
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+pkg)
assert str(ROOT/'build') not in env['LEAN_PATH']
(RUN/'tmp').mkdir();env['TMP']=env['TEMP']=str(RUN/'tmp')
aud=''.join('import '+rel[:-5].replace('/','.')+'\n' for rel in sources)+''.join('set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n' for n in targets)
write(RUN/'sources/PairedBlocksAudit13.lean',aud.encode())
manifest={'run':str(RUN),'timestamp':datetime.datetime.now().astimezone().isoformat(),'scope':'PARTIAL_DEV_PAIRED_BLOCKS_2_MODULES_13_TARGETS',
 'compiler':compiler,'compiler_sha256':hf(compiler),'lean_version_inherited':'4.31.0 — compiler hash inherited and reread','lean_path':env['LEAN_PATH'],
 'sources':sources,'declarations':targets,'module_targets':module_targets,'author_axioms':authorax,'dependencies':deps,
 'external_direct_pins':external,'readonly_pins':readonly,'parent_custody_path':str(parent),'parent_custody_sha256':hf(parent),
 'parent_full_reaudit':False,'author_project_build_on_lean_path':False,'packages_rebuilt':False,'memory_writes':False,'own_origin_runs':[str(PHASE)]}
save(RUN/'manifest.json',manifest);save(RUN/'author_history.json',history)
write(REV/'paired_blocks_latest_run.txt',str(RUN).encode())
print(json.dumps({'run':str(RUN),'new_modules':2,'targets':13,'project_dependencies':len(deps),'author_failures_excluded':3}),flush=True)
records=[]
for rel in list(sources)+['PairedBlocksAudit13.lean']:
    sp=RUN/'sources'/rel;bp=RUN/'build'/Path(rel).with_suffix('.olean');bp.parent.mkdir(parents=True,exist_ok=True);assert not bp.exists()
    cmd=[compiler,'-o',str(bp),str(sp)];start=time.monotonic();r=subprocess.run(cmd,cwd=RUN/'sources',env=env,capture_output=True)
    out=RUN/'logs'/(Path(rel).stem+'.stdout.txt');err=RUN/'logs'/(Path(rel).stem+'.stderr.txt');write(out,r.stdout);write(err,r.stderr)
    ax=axioms(r.stdout.decode('utf-8',errors='replace'))
    expected=module_targets.get(rel,targets);expectedax={n:authorax[n] for n in expected}
    row={'module':rel,'command':cmd,'returncode':r.returncode,'seconds':round(time.monotonic()-start,3),'source_sha256':hf(sp),'output_sha256':hf(bp) if bp.exists() else None,'stdout':str(out),'stderr':str(err),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'axioms':ax,'exact_targets':set(ax)==set(expected),'axioms_match_author':ax==expectedax,'axioms_allowed':bool(ax) and all(set(x)<=allowed for x in ax.values())}
    if rel.startswith('TGLV350/'):row['binary_equals_author']=row['output_sha256']==sources[rel]['author_binary_sha256']
    records.append(row);save(RUN/'compilation.json',{'complete':False,'records':records})
    print(json.dumps({k:row[k] for k in ['module','returncode','seconds','exact_targets','axioms_allowed']}),flush=True)
    if r.returncode:print(r.stdout.decode('utf-8',errors='replace'),flush=True);break
result={'complete':len(records)==3,'records':records,'all_exit_zero':len(records)==3 and all(x['returncode']==0 for x in records),'exact_13_targets':len(records)==3 and all(x['exact_targets'] for x in records),'all_axioms_allowed':all(x['axioms_allowed'] for x in records),'all_axioms_match_author':all(x['axioms_match_author'] for x in records),'binary_equal_author':len(records)==3 and all(x.get('binary_equals_author',False) for x in records[:2]),'source_snapshot_preserved':all(hf(d['snapshot'])==d['sha256'] for d in sources.values()),'readonly_artifacts_preserved':all(hf(p)==h for p,h in readonly.items()),'dependencies_preserved':all(hf(d['frozen_source'])==d['source_sha256'] and hf(d['frozen_binary'])==d['sha256'] and hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['sha256'] and all(hf(p)==h for p,h in d['companions'].items()) for d in deps.values()),'external_direct_pins_preserved':all(hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256'] for d in external.values())}
save(RUN/'compilation.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
