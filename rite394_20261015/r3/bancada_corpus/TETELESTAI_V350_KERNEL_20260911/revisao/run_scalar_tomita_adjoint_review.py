"""Independent DEV build: frozen sources and reviewer-owned project dependencies only."""
from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys,time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
PRE=Path((REV/'closed_tomita_batch_latest_run.txt').read_text(encoding='utf-8'))
RUN=REV/('scalar_tomita_adjoint_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
NAMES={'AntilinearAdjointGraph':'20260912_103611_347285','ScalarTomitaAdjoint':'20260912_104146_918776'}
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,b):
    assert p.resolve().is_relative_to(REV)
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2).encode())
def imports(b):return re.findall(r'^import\s+([\w.]+)',b.decode(),re.M)
def axioms(s):
    d={n:[a.strip() for a in b.split(',') if a.strip()] for n,b in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",s,re.S)}
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",s):d.setdefault(n,[])
    return d
pm=json.loads((PRE/'manifest.json').read_bytes());pc=json.loads((PRE/'compilation.json').read_bytes())
assert pc['all_exit_zero'] and pc['all_axioms_allowed']
catalog={n:{**r,'source':r['frozen_source'],'binary':r['frozen_binary'],'reviewer_origin':str(PRE)} for n,r in pm['dependencies'].items()}
for rel,r in pm['sources'].items():
    c=next(x for x in pc['records'] if x['module']==rel)
    catalog[rel[:-5].replace('/','.') ]={'source':r['snapshot'],'binary':str(PRE/'build'/Path(rel).with_suffix('.olean')),'source_sha256':r['sha256'],'sha256':c['output_sha256'],'reviewer_origin':str(PRE)}
custody_raw=(ROOT/'closed_tomita_custody.json').read_bytes();custody=json.loads(custody_raw)
cv_raw=(ROOT/'closed_tomita_custody_verification.json').read_bytes();cv=json.loads(cv_raw)
assert cv['custody_sha256']==sha(custody_raw) and cv['custody_ok']
for p,h in custody['review_sha256'].items():assert sha(Path(p).read_bytes())==h
assert sha((ROOT/'um.py').read_bytes())==custody['working_sha256']
write(RUN/'closed_tomita_custody.json',custody_raw);write(RUN/'closed_tomita_custody_verification.json',cv_raw)
sources={};targets=[];history=[];allowed={'propext','Classical.choice','Quot.sound'}
for name,stamp in NAMES.items():
    rel='TGLV350/'+name+'.lean';src=ROOT/'kernel'/rel;raw=src.read_bytes();snap=RUN/'sources'/rel;write(snap,raw)
    log=ROOT/'logs'/(name+'_'+stamp+'.json');lr=log.read_bytes();a=json.loads(lr)
    assert a['sha256']==sha(raw) and a['returncode']==0 and a['source_unchanged_during_compile'] is True
    binary=ROOT/'build'/Path(rel).with_suffix('.olean');assert sha(binary.read_bytes())==a['output_sha256']
    txt=raw.decode();ns=re.findall(r'^namespace\s+([\w.]+)',txt,re.M);assert ns==['TGLV350.Regular']
    printed=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)',txt,re.M)]
    named=['TGLV350.Regular.'+n for n in re.findall(r'^(?:noncomputable\s+)?(?:def|theorem|abbrev|structure|instance)\s+([\w.]+)',txt,re.M)]
    assert set(named)==set(printed);targets+=printed
    finalax=axioms(Path(a['stdout']).read_text(encoding='utf-8'));assert set(finalax)==set(printed) and all(set(v)<=allowed for v in finalax.values())
    sources[rel]={'path':str(src),'snapshot':str(snap),'sha256':sha(raw),'lines':len(txt.splitlines()),'imports':imports(raw),'namespace':ns[0],'declarations':printed,'all_named_declarations':named,'author_log':str(log),'author_log_sha256':sha(lr),'author_binary_sha256':sha(binary.read_bytes()),'author_axioms':finalax}
    for lp in sorted((ROOT/'logs').glob(name+'_*.json')):
        jb=lp.read_bytes();jr=json.loads(jb);write(RUN/'author_history'/lp.name,jb)
        item={'module':name,'log':str(lp),'log_sha256':sha(jb),'timestamp':jr['timestamp'],'returncode':jr['returncode'],'sha256':jr['sha256'],'accepted_final':lp==log}
        for key in ['stdout','stderr']:
            p=Path(jr[key]);b=p.read_bytes();write(RUN/'author_history'/p.name,b);item[key+'_sha256']=sha(b)
            if key=='stdout':item['errors_and_warnings']=[l for l in b.decode('utf-8',errors='replace').splitlines() if 'error:' in l or 'warning:' in l]
        history.append(item)
assert len(targets)==len(set(targets))==23
new={'TGLV350.'+n for n in NAMES};needed=set()
def visit(n):
    if n in new:
        for x in sources[n.replace('.','/')+'.lean']['imports']:visit(x)
    elif n.split('.')[0] in {'TGLV350','TGLExt','TGL'} and n not in needed:
        assert n in catalog,n;needed.add(n)
        for x in imports(Path(catalog[n]['source']).read_bytes()):visit(x)
for n in new:visit(n)
deps={}
for n in sorted(needed):
    r=catalog[n].copy();raw=Path(r['source']).read_bytes();br=Path(r['binary']).read_bytes();assert sha(raw)==r['source_sha256'] and sha(br)==r['sha256']
    rel=Path(*n.split('.'));live=(ROOT/'kernel'/rel.with_suffix('.lean')).read_bytes()
    if live!=raw:
        assert r.get('previously_reviewed_comment_only_erratum') is True,n
        assert raw.replace(r['frozen_old_comment'].encode(),r['live_corrected_comment'].encode())==live,n
    sp=RUN/'dependency_sources'/rel.with_suffix('.lean');bp=RUN/'build'/rel.with_suffix('.olean');write(sp,raw);write(bp,br)
    for p in Path(r['binary']).parent.glob(Path(r['binary']).name+'.*'):
        if p.is_file():write(bp.with_name(p.name),p.read_bytes())
    deps[n]={**r,'frozen_source':str(sp),'frozen_binary':str(bp),'imports':imports(raw),'live_source_sha256':sha(live)}
cfg=json.loads((ROOT/'environment.json').read_bytes());env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+cfg['lean_path'][2:]);(RUN/'tmp').mkdir();env['TMP']=env['TEMP']=str(RUN/'tmp')
ver=subprocess.run([cfg['lean'],'--version'],capture_output=True,env=env,cwd=RUN);assert ver.returncode==0
manifest={'run':str(RUN),'previous_run':str(PRE),'previous_manifest_sha256':sha((PRE/'manifest.json').read_bytes()),'previous_compilation_sha256':sha((PRE/'compilation.json').read_bytes()),'mode':'INDEPENDENT_TWO_DEV_MODULES_23_TYPES_AXIOMS','sources':sources,'dependencies':deps,'declarations':targets,'lean_path':env['LEAN_PATH'],'compiler_sha256':sha(Path(cfg['lean']).read_bytes()),'lean_version':ver.stdout.decode().strip(),'custody_sha256':sha(custody_raw),'custody_verification_sha256':sha(cv_raw),'initial_um_sha256':sha((ROOT/'um.py').read_bytes()),'previous_reviews':{str(p):sha(p.read_bytes()) for p in REV.glob('REVIEW_*.md')}}
save(RUN/'manifest.json',manifest);save(RUN/'author_history.json',history);write(REV/'scalar_tomita_adjoint_latest_run.txt',str(RUN).encode())
audit='\n'.join('import TGLV350.'+n for n in NAMES)+'\n'
for n in targets:audit+='set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n'
write(RUN/'sources/ScalarTomitaAdjointAudit.lean',audit.encode())
print(json.dumps({'run':str(RUN),'dependencies':len(deps),'targets':len(targets),'history_attempts':len(history)}),flush=True)
records=[]
for rel in list(sources)+['ScalarTomitaAdjointAudit.lean']:
    sp=RUN/'sources'/rel;op=RUN/'build'/Path(rel).with_suffix('.olean');op.parent.mkdir(parents=True,exist_ok=True);assert not op.exists()
    cmd=[cfg['lean'],'-o',str(op),str(sp)];t=time.monotonic();p=subprocess.run(cmd,capture_output=True,cwd=RUN/'sources',env=env)
    stdout=RUN/'logs'/(Path(rel).stem+'.stdout.txt');stderr=RUN/'logs'/(Path(rel).stem+'.stderr.txt');write(stdout,p.stdout);write(stderr,p.stderr);ax=axioms(p.stdout.decode('utf-8',errors='replace'))
    r={'module':rel,'command':cmd,'returncode':p.returncode,'seconds':round(time.monotonic()-t,3),'source_sha256':sha(sp.read_bytes()),'output_sha256':sha(op.read_bytes()) if op.exists() else None,'axioms':ax,'axioms_allowed':bool(ax) and all(set(v)<=allowed for v in ax.values()),'stdout':str(stdout),'stderr':str(stderr),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)}
    if rel in sources:r['binary_equals_author']=r['output_sha256']==sources[rel]['author_binary_sha256']
    records.append(r);save(RUN/'compilation.json',{'complete':False,'records':records});print(json.dumps({k:r[k] for k in ['module','returncode','seconds','axioms_allowed']}),flush=True)
    if p.returncode:print(p.stdout.decode('utf-8',errors='replace'),flush=True);break
c={'complete':len(records)==3,'records':records,'all_exit_zero':len(records)==3 and all(r['returncode']==0 for r in records),'all_axioms_allowed':all(r['axioms_allowed'] for r in records),'exact_23_targets':len(records)==3 and set(records[-1]['axioms'])==set(targets),'two_binaries_equal_author':len(records)==3 and all(r.get('binary_equals_author',True) for r in records),'sources_unchanged':all(sha(Path(r['path']).read_bytes())==r['sha256'] for r in sources.values()),'dependencies_preserved':all(sha(Path(r['frozen_source']).read_bytes())==r['source_sha256'] and sha(Path(r['frozen_binary']).read_bytes())==r['sha256'] for r in deps.values()),'previous_reviews_preserved':all(sha(Path(p).read_bytes())==h for p,h in manifest['previous_reviews'].items()),'um_unchanged':sha((ROOT/'um.py').read_bytes())==manifest['initial_um_sha256']}
save(RUN/'compilation.json',c);print(json.dumps({k:v for k,v in c.items() if k!='records'}),flush=True)
