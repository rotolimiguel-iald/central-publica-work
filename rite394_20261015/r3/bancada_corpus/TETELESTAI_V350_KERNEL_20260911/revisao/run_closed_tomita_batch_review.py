"""Recompile the 15 frozen DEV modules; inspect integration only by import rewrite."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
RUN=REV/('closed_tomita_batch_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,b):
    assert p.resolve().is_relative_to(REV)
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bak=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bak.open('xb') as f:f.write(old)
        assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b;tmp.replace(p)
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2).encode())
def imports(b):return re.findall(r'^import\s+([\w.]+)',b.decode(),re.M)
groups={
 'cyclic_cut_gns':['ScalarCutVacuum','ScalarCutCyclicSpace','ScalarCutVectorFunctional','ScalarCutGNSProperties'],
 'gaussian_closability':['L2PositiveMultiplier','L2GaussianProfile','FibreVonNeumann','ScalarGaussianVacuum','SeparatingCyclicCommutant','DualOrbitVonNeumann','ScalarGaussianGNSMap','VectorTomitaClosability','ScalarGaussianClosureTransport'],
 'closed_scalar_tomita':['ScalarClosedTomita','ScalarTomitaStandardSubspace']}
catalog={};previous={};sources={};targets=[]
for key,names in groups.items():
    prior=Path((REV/(key+'_latest_run.txt')).read_text(encoding='utf-8'))
    m=json.loads((prior/'manifest.json').read_bytes());c=json.loads((prior/'compilation.json').read_bytes())
    assert c['all_exit_zero'] and c['all_axioms_allowed']
    previous[key]={'run':str(prior),'manifest_sha256':sha((prior/'manifest.json').read_bytes()),'compilation_sha256':sha((prior/'compilation.json').read_bytes())}
    for n,r in m['dependencies'].items():
        catalog.setdefault(n,{**r,'source':r['frozen_source'],'binary':r['frozen_binary'],'reviewer_origin':str(prior)})
    for rel,r in m['sources'].items():
        cr=next(x for x in c['records'] if x['module']==rel)
        catalog[rel[:-5].replace('/','.')]={'source':r['snapshot'],'binary':str(prior/'build'/Path(rel).with_suffix('.olean')),'sha256':cr['output_sha256'],'source_sha256':r['sha256'],'reviewer_origin':str(prior)}
    for name in names:
        rel='TGLV350/'+name+'.lean';r=m['sources'][rel];raw=Path(r['path']).read_bytes()
        assert sha(raw)==r['sha256'] and raw==Path(r['snapshot']).read_bytes()
        integrated=ROOT/'kernel/TGLExt'/('V350'+name+'.lean');ib=integrated.read_bytes()
        assert re.sub(rb'^import TGLV350\.',b'import TGLExt.V350',raw,flags=re.M)==ib,name
        snap=RUN/'sources'/rel;write(snap,raw);write(RUN/'integrated_sources/TGLExt'/integrated.name,ib)
        sources[rel]={**r,'snapshot':str(snap),'prior_snapshot':r['snapshot'],'prior_binary':catalog[rel[:-5].replace('/','.')]['binary'],'prior_binary_sha256':catalog[rel[:-5].replace('/','.')]['sha256'],'integrated_path':str(integrated),'integrated_sha256':sha(ib),'only_imports_changed':True}
        targets+=r['declarations']
assert len(sources)==15 and len(targets)==99 and len(set(targets))==99
new={rel[:-5].replace('/','.') for rel in sources};needed=set()
def visit(n):
    if n in new:
        for i in sources[n.replace('.','/')+'.lean']['imports']:visit(i)
    elif n.split('.')[0] in {'TGL','TGLExt','TGLV350'} and n not in needed:
        assert n in catalog,n
        needed.add(n)
        for i in imports(Path(catalog[n]['source']).read_bytes()):visit(i)
for n in new:visit(n)
deps={}
for n in sorted(needed):
    r=catalog[n].copy();raw=Path(r['source']).read_bytes();binary=Path(r['binary']).read_bytes()
    assert sha(raw)==r['source_sha256'] and sha(binary)==r['sha256'],n
    rel=Path(*n.split('.'));live=(ROOT/'kernel'/rel.with_suffix('.lean')).read_bytes()
    if sha(live)!=sha(raw):
        assert r.get('previously_reviewed_comment_only_erratum') is True,n
        assert raw.replace(r['frozen_old_comment'].encode(),r['live_corrected_comment'].encode())==live,n
    sp=RUN/'dependency_sources'/rel.with_suffix('.lean');bp=RUN/'build'/rel.with_suffix('.olean')
    write(sp,raw);write(bp,binary)
    for p in Path(r['binary']).parent.glob(Path(r['binary']).name+'.*'):
        if p.is_file():write(bp.with_name(p.name),p.read_bytes())
    deps[n]={**r,'frozen_source':str(sp),'frozen_binary':str(bp),'live_source_sha256':sha(live)}
cfg=json.loads((ROOT/'environment.json').read_bytes());env=os.environ.copy()
env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+cfg['lean_path'][2:])
(RUN/'tmp').mkdir();env['TMP']=env['TEMP']=str(RUN/'tmp')
version=subprocess.run([cfg['lean'],'--version'],capture_output=True,cwd=RUN,env=env)
assert version.returncode==0
m={'run':str(RUN),'mode':'INDEPENDENT_RECOMPILE_15_DEV_99_TYPES_AXIOMS__INTEGRATED_IMPORT_REWRITE_INSPECTION','previous':previous,'sources':sources,'dependencies':deps,'declarations':targets,'lean_path':env['LEAN_PATH'],'compiler_sha256':sha(Path(cfg['lean']).read_bytes()),'lean_version':version.stdout.decode().strip(),'previous_reviews':{str(p):sha(p.read_bytes()) for p in REV.glob('REVIEW_*.md')},'working_sha256':sha((ROOT/'um.py').read_bytes())}
save(RUN/'manifest.json',m);write(REV/'closed_tomita_batch_latest_run.txt',str(RUN).encode())
audit='\n'.join('import '+n for n in sorted(new))+'\n'
for n in targets:audit+='set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n'
write(RUN/'sources/ClosedTomitaBatchAudit.lean',audit.encode())
print(json.dumps({'run':str(RUN),'dependencies':len(deps),'modules':15,'targets':99}),flush=True)
records=[];allowed={'propext','Classical.choice','Quot.sound'}
for rel in list(sources)+['ClosedTomitaBatchAudit.lean']:
    sp=RUN/'sources'/rel;op=RUN/'build'/Path(rel).with_suffix('.olean');op.parent.mkdir(parents=True,exist_ok=True)
    assert not op.exists()
    command=[cfg['lean'],'-o',str(op),str(sp)];start=time.monotonic()
    p=subprocess.run(command,capture_output=True,cwd=RUN/'sources',env=env)
    out=p.stdout.decode('utf-8',errors='replace')
    ax={n:[x.strip() for x in a.split(',') if x.strip()] for n,a in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",out,re.S)}
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",out):ax.setdefault(n,[])
    stdout=RUN/'logs'/(Path(rel).stem+'.stdout.txt');stderr=RUN/'logs'/(Path(rel).stem+'.stderr.txt')
    write(stdout,p.stdout);write(stderr,p.stderr)
    r={'module':rel,'command':command,'returncode':p.returncode,'seconds':round(time.monotonic()-start,3),'source_sha256':sha(sp.read_bytes()),'output_sha256':sha(op.read_bytes()) if op.exists() else None,'axioms':ax,'axioms_allowed':bool(ax) and all(set(a)<=allowed for a in ax.values()),'stdout':str(stdout),'stderr':str(stderr),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)}
    if rel in sources:r['same_binary_as_previous_independent_compile']=r['output_sha256']==sources[rel]['prior_binary_sha256']
    records.append(r);save(RUN/'compilation.json',{'complete':False,'records':records})
    print(json.dumps({k:r[k] for k in ['module','returncode','seconds','axioms_allowed']}),flush=True)
    if p.returncode:print(out,flush=True);break
c={'complete':len(records)==16,'records':records,'all_exit_zero':len(records)==16 and all(r['returncode']==0 for r in records),'all_axioms_allowed':all(r['axioms_allowed'] for r in records),'exact_99_audited':len(records)==16 and set(records[-1]['axioms'])==set(targets),'same_15_binaries_as_previous_independent':len(records)==16 and all(r.get('same_binary_as_previous_independent_compile',True) for r in records),'sources_unchanged':all(sha(Path(r['path']).read_bytes())==r['sha256'] and sha(Path(r['integrated_path']).read_bytes())==r['integrated_sha256'] for r in sources.values()),'dependencies_preserved':all(sha(Path(r['frozen_source']).read_bytes())==r['source_sha256'] and sha(Path(r['frozen_binary']).read_bytes())==r['sha256'] for r in deps.values()),'previous_reviews_preserved':all(sha(Path(p).read_bytes())==h for p,h in m['previous_reviews'].items())}
save(RUN/'compilation.json',c);print(json.dumps({k:v for k,v in c.items() if k!='records'}),flush=True)
