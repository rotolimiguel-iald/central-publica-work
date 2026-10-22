from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
RUN=REV/('scalar_vna_partial_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b:hashlib.sha256(b).hexdigest()
hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
allowed={'propext','Classical.choice','Quot.sound'}
def write(p,b):
    assert p.resolve().is_relative_to(REV)
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bak.open('xb') as f:f.write(old)
        assert bak.read_bytes()==old
    q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;os.replace(q,p)
def save(p,x):write(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def imports(b):return re.findall(r'^import\s+([\w.]+)',b.decode(),re.M)
def axioms(t):
    d={}
    for n,v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",t,re.S):
        a=sorted(x.strip() for x in v.split(',') if x.strip());assert n not in d or d[n]==a;d[n]=a
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",t):
        assert n not in d or not d[n];d[n]=[]
    return d
origins=[REV/'core_polar_independent_20260912_203148_639288',REV/'gaussian_polar_independent_20260912_210534_399150',Path((REV/'right_vector_final_latest_run.txt').read_text().strip())]
catalog={};originpins={};pkg=None
for origin in origins:
    m=load(origin/'manifest.json');c=load(origin/'compilation.json')
    assert c['complete'] and c['all_exit_zero'] and c['all_axioms_allowed'] and c['dependencies_preserved']
    originpins[str(origin)]={'manifest_sha256':hf(origin/'manifest.json'),'compilation_sha256':hf(origin/'compilation.json')}
    for n,x in m['dependencies'].items():
        catalog[n]={**x,'source':x['frozen_source'],'binary':x['frozen_binary'],'inherited_from':str(origin)}
    for rel,x in m['sources'].items():
        n=rel[:-5].replace('/','.');z=next(z for z in c['records'] if z['module']==rel)
        assert z['returncode']==0 and z['source_sha256']==x['sha256']
        catalog[n]={'source':x['snapshot'],'binary':z['command'][2],'source_sha256':x['sha256'],'sha256':z['output_sha256'],'reviewer_origin':str(origin),'inherited_from':str(origin)}
    p=m['lean_path'].split(os.pathsep)[1:]
    assert len(p)==8 and all('.lake\\packages\\' in x for x in p)
    assert pkg is None or pkg==p;pkg=p
parent=load(ROOT/'right_vector_custody.json');pv=load(ROOT/'right_vector_custody_verification.json')
assert pv['custody_ok'] and pv['custody_sha256']==hf(ROOT/'right_vector_custody.json')
assert hf(ROOT/'um.py')==parent['working_sha256']
for n in ['right_vector_custody.json','right_vector_custody_verification.json']:write(RUN/n,(ROOT/n).read_bytes())
spec=[('ReducingCommutantCompression','20260913_004856_171552',5),('ReducingBicommutantLift','20260913_005130_648272',7),('SeparatingRestrictionVonNeumann','20260913_005436_519208',5)]
sources={};raws={};targets=[];history=[]
for name,stamp,count in spec:
    rel='TGLV350/'+name+'.lean';src=ROOT/'kernel'/rel;raw=src.read_bytes();sp=RUN/'sources'/rel;write(sp,raw);raws['TGLV350.'+name]=raw
    lp=ROOT/'logs'/(name+'_'+stamp+'.json');lr=load(lp);ab=Path(lr['command'][2])
    assert lr['returncode']==lr['lean_returncode']==0 and lr['source_unchanged_during_compile'] and lr['output_exists']
    assert Path(lr['source'])==src and lr['sha256']==sha(raw) and hf(ab)==lr['output_sha256']
    names=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)$',raw.decode(),re.M)]
    assert len(names)==len(set(names))==count
    stripped=re.sub(r'/\-.*?\-/','',raw.decode(),flags=re.S);stripped=re.sub(r'--[^\n]*','',stripped)
    assert not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]',stripped)
    output=Path(lr['stdout']).read_bytes();err=Path(lr['stderr']).read_bytes();ax=axioms(output.decode())
    assert set(ax)==set(names) and all(set(x)<=allowed for x in ax.values()) and not err
    sources[rel]={'path':str(src),'snapshot':str(sp),'sha256':sha(raw),'imports':imports(raw),'declarations':names,'author_binary':str(ab),'author_binary_sha256':hf(ab),'author_log':str(lp),'author_log_sha256':hf(lp),'author_stdout':lr['stdout'],'author_stderr':lr['stderr'],'author_stdout_sha256':sha(output),'author_stderr_sha256':sha(err)}
    targets.extend(names)
    for hl in sorted((ROOT/'logs').glob(name+'_*.json')):
        hb=hl.read_bytes();hr=json.loads(hb);write(RUN/'author_history'/hl.name,hb)
        row={'module':name,'log':str(hl),'log_sha256':sha(hb),'returncode':hr['returncode'],'source_sha256':hr['sha256'],'accepted_final':hl==lp}
        for k in ['stdout','stderr']:
            b=Path(hr[k]).read_bytes();write(RUN/'author_history'/Path(hr[k]).name,b);row[k+'_sha256']=sha(b)
        history.append(row)
assert len(targets)==len(set(targets))==17
needed=set();seen=set()
def visit(n):
    if n in seen:return
    seen.add(n)
    if n in raws:b=raws[n]
    elif n.split('.')[0] in {'TGLV350','TGLExt','TGL'}:
        assert n in catalog,n;needed.add(n);b=Path(catalog[n]['source']).read_bytes()
    else:return
    for i in imports(b):visit(i)
for n in raws:visit(n)
deps={}
for n in sorted(needed):
    d=catalog[n];b=Path(d['source']).read_bytes();o=Path(d['binary']).read_bytes()
    assert Path(d['source']).resolve().is_relative_to(REV) and Path(d['binary']).resolve().is_relative_to(REV)
    assert sha(b)==d['source_sha256'] and sha(o)==d['sha256'],n
    rp=Path(*n.split('.'));live=(ROOT/'kernel'/rp.with_suffix('.lean')).read_bytes()
    if live!=b:
        assert d.get('previously_reviewed_comment_only_erratum') is True,n
        assert b.replace(d['frozen_old_comment'].encode(),d['live_corrected_comment'].encode())==live,n
    ds=RUN/'dependency_sources'/rp.with_suffix('.lean');db=RUN/'build'/rp.with_suffix('.olean')
    write(ds,b);write(db,o);companions={}
    for cp in Path(d['binary']).parent.glob(Path(d['binary']).name+'.*'):
        if cp.is_file():
            cb=cp.read_bytes();dest=db.with_name(cp.name);write(dest,cb);companions[str(dest)]=sha(cb)
    deps[n]={**d,'frozen_source':str(ds),'frozen_binary':str(db),'live_source_sha256':sha(live),'companions':companions}
external=m['external_direct_pins']
for d in external.values():assert hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256']
cfg=load(ROOT/'environment.json');assert hf(cfg['lean'])==m['compiler_sha256']
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+pkg)
assert str(ROOT/'build') not in env['LEAN_PATH']
(RUN/'tmp').mkdir(exist_ok=True);env['TMP']=env['TEMP']=str(RUN/'tmp')
artifacts={str(p):hf(p) for p in [ROOT/'right_vector_custody.json',ROOT/'right_vector_custody_verification.json',REV/'REVIEW_RIGHT_VECTOR_DEV.md',REV/'REVIEW_RIGHT_VECTOR_INTEGRATED.md',ROOT/'um.py',ROOT/'gate_extension.py']}
manifest={'run':str(RUN),'timestamp':datetime.datetime.now().astimezone().isoformat(),'origins':originpins,'compiler':cfg['lean'],'compiler_sha256':m['compiler_sha256'],'lean_version':m['lean_version'],'lean_path':env['LEAN_PATH'],'sources':sources,'dependencies':deps,'external_direct_pins':external,'declarations':targets,'artifacts_readonly':artifacts,'parent_custody_full_reaudit':False,'memory_writes':False,'author_build_on_lean_path':False,'scope':'PARTIAL_THREE_MODULES_ONLY'}
save(RUN/'manifest.json',manifest);save(RUN/'author_history.json',history);write(REV/'scalar_vna_partial_latest_run.txt',str(RUN).encode())
audit=''.join('import TGLV350.'+n+'\n' for n,_,_ in spec)
for n in targets:audit+='set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n'
write(RUN/'sources/ScalarVNAPartialAudit.lean',audit.encode())
print(json.dumps({'run':str(RUN),'dependencies':len(deps),'targets':len(targets),'excluded_author_rc1':sum(x['returncode']!=0 for x in history)}),flush=True)
records=[]
for module in list(sources)+['ScalarVNAPartialAudit.lean']:
    sp=RUN/'sources'/module;op=RUN/'build'/Path(module).with_suffix('.olean');op.parent.mkdir(parents=True,exist_ok=True);assert not op.exists()
    cmd=[cfg['lean'],'-o',str(op),str(sp)];start=time.monotonic();p=subprocess.run(cmd,capture_output=True,cwd=RUN/'sources',env=env)
    stdout=RUN/'logs'/(Path(module).stem+'.stdout.txt');stderr=RUN/'logs'/(Path(module).stem+'.stderr.txt');write(stdout,p.stdout);write(stderr,p.stderr)
    ax=axioms(p.stdout.decode('utf-8',errors='replace'));expected=sources[module]['declarations'] if module in sources else targets
    row={'module':module,'command':cmd,'returncode':p.returncode,'seconds':round(time.monotonic()-start,3),'source_sha256':hf(sp),'output_sha256':hf(op) if op.exists() else None,'stdout':str(stdout),'stderr':str(stderr),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),'axioms':ax,'exact_targets':set(ax)==set(expected),'axioms_allowed':bool(ax) and all(set(x)<=allowed for x in ax.values())}
    if module in sources:row['binary_equals_author']=row['output_sha256']==sources[module]['author_binary_sha256']
    records.append(row);save(RUN/'compilation.json',{'complete':False,'records':records})
    print(json.dumps({k:row[k] for k in ['module','returncode','seconds','exact_targets','axioms_allowed']}),flush=True)
    if p.returncode:print(p.stdout.decode('utf-8',errors='replace'),flush=True);break
result={'complete':len(records)==4,'records':records,'all_exit_zero':len(records)==4 and all(x['returncode']==0 for x in records),'exact_17_targets':len(records)==4 and all(x['exact_targets'] for x in records),'all_axioms_allowed':all(x['axioms_allowed'] for x in records),'three_binaries_equal_author':len(records)>=3 and all(x.get('binary_equals_author',False) for x in records[:3]),'author_source_binary_preserved':all(hf(x['path'])==x['sha256'] and hf(x['author_binary'])==x['author_binary_sha256'] for x in sources.values()),'dependencies_preserved':all(hf(d['frozen_source'])==d['source_sha256'] and hf(d['frozen_binary'])==d['sha256'] and all(hf(p)==h for p,h in d['companions'].items()) for d in deps.values()),'external_direct_pins_preserved':all(hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256'] for d in external.values()),'read_only_artifacts_preserved':all(hf(p)==h for p,h in artifacts.items()),'author_final_log_streams_preserved':all(hf(x['author_log'])==x['author_log_sha256'] and hf(x['author_stdout'])==x['author_stdout_sha256'] and hf(x['author_stderr'])==x['author_stderr_sha256'] for x in sources.values())}
save(RUN/'compilation.json',result);print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
