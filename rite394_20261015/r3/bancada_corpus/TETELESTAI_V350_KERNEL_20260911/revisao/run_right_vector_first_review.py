from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,time,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
RUN=REV/('right_vector_first_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b:hashlib.sha256(b).hexdigest()
hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
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
def save(p,x):write(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def imports(b):return re.findall(r'^import\s+([\w.]+)',b.decode(),re.M)
def axioms(t):
    result={}
    for n,v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",t,re.S):
        a=[x.strip() for x in v.split(',') if x.strip()]
        assert n not in result or result[n]==a
        result[n]=a
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",t):
        assert n not in result or not result[n];result[n]=[]
    return result
allowed={'propext','Classical.choice','Quot.sound'}
origin=REV/'paired_right_final_independent_20260912_225451_634240'
m=load(origin/'manifest.json'); c=load(origin/'compilation.json')
assert all(c[k] for k in ['complete','all_exit_zero','all_axioms_allowed','dependencies_preserved','exact_29_targets','three_binaries_equal_author'])
catalog={}
for n,x in m['dependencies'].items():catalog[n]={**x,'source':x['frozen_source'],'binary':x['frozen_binary']}
for n,x in m['reused_current_modules'].items():catalog[n]={**x,'binary':x['frozen_binary']}
for rel,x in m['sources'].items():
    n=rel[:-5].replace('/','.')
    rows=[z for z in c['records'] if z['module']==rel]
    if rows:
        z=rows[0];assert z['returncode']==0 and z['source_sha256']==x['sha256']
        catalog[n]={'source':x['snapshot'],'binary':z['command'][2],'source_sha256':x['sha256'],'sha256':z['output_sha256'],'reviewer_origin':str(origin)}
    else:assert n in catalog
pkg=m['lean_path'].split(os.pathsep)[1:]
assert len(pkg)==8 and all('.lake\\packages\\' in p for p in pkg)
parent=load(ROOT/'paired_right_custody.json'); pv=load(ROOT/'paired_right_custody_verification.json')
assert pv['custody_ok'] and hf(ROOT/'paired_right_custody.json')==pv['custody_sha256']
assert hf(ROOT/'um.py')==parent['working_sha256']
for n in ['paired_right_custody.json','paired_right_custody_verification.json']:
    write(RUN/n,(ROOT/n).read_bytes())
name='ScalarGaussianRightPairs'; rel='TGLV350/'+name+'.lean'; src=ROOT/'kernel'/rel
raw=src.read_bytes(); sp=RUN/'sources'/rel;write(sp,raw)
log=ROOT/'logs'/f'{name}_20260912_233325_289127.json'; a=load(log)
assert a['returncode']==a['lean_returncode']==0 and a['source_unchanged_during_compile'] and a['output_exists']
assert Path(a['source'])==src and a['sha256']==sha(raw)
ab=Path(a['command'][2]);assert hf(ab)==a['output_sha256']
targets=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)',raw.decode(),re.M)]
assert len(targets)==len(set(targets))==6
stripped=re.sub(r'/\-.*?\-/','',raw.decode(),flags=re.S);stripped=re.sub(r'--[^\n]*','',stripped)
assert not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]',stripped)
output=Path(a['stdout']).read_bytes();err=Path(a['stderr']).read_bytes();aa=axioms(output.decode())
assert set(aa)==set(targets) and all(set(x)==allowed for x in aa.values()) and not err
history=[]
for lp in sorted((ROOT/'logs').glob(name+'_*.json')):
    lb=lp.read_bytes();lr=json.loads(lb);write(RUN/'author_history'/lp.name,lb)
    row={'log':str(lp),'log_sha256':sha(lb),'returncode':lr['returncode'],'source_sha256':lr['sha256'],'accepted_final':lp==log}
    for k in ['stdout','stderr']:
        b=Path(lr[k]).read_bytes();write(RUN/'author_history'/Path(lr[k]).name,b);row[k+'_sha256']=sha(b)
    history.append(row)
assert sum(x['accepted_final'] for x in history)==1
seen=set();needed=set()
def visit(n):
    if n in seen:return
    seen.add(n)
    if n=='TGLV350.'+name:b=raw
    elif n.split('.')[0] in {'TGLV350','TGLExt','TGL'}:
        assert n in catalog,n;needed.add(n);b=Path(catalog[n]['source']).read_bytes()
    else:return
    for i in imports(b):visit(i)
visit('TGLV350.'+name)
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
    write(ds,b);write(db,o)
    companions={}
    for cp in Path(d['binary']).parent.glob(Path(d['binary']).name+'.*'):
        if cp.is_file():
            cb=cp.read_bytes();dest=db.with_name(cp.name);write(dest,cb);companions[str(dest)]=sha(cb)
    deps[n]={**d,'frozen_source':str(ds),'frozen_binary':str(db),'live_source_sha256':sha(live),'companions':companions}
external=m['external_direct_pins']
for d in external.values():
    assert hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256']
cfg=load(ROOT/'environment.json');assert hf(cfg['lean'])==m['compiler_sha256']
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+pkg)
(RUN/'tmp').mkdir(exist_ok=True);env['TMP']=env['TEMP']=str(RUN/'tmp')
source={'path':str(src),'snapshot':str(sp),'sha256':sha(raw),'author_binary':str(ab),'author_binary_sha256':hf(ab),'author_log':str(log),'author_log_sha256':hf(log),'author_stdout_sha256':sha(output),'author_stderr_sha256':sha(err),'imports':imports(raw),'declarations':targets}
artifacts={str(p):hf(p) for p in [ROOT/'paired_right_custody.json',ROOT/'paired_right_custody_verification.json',REV/'REVIEW_PAIRED_RIGHT_DEV.md',REV/'REVIEW_PAIRED_RIGHT_INTEGRATED.md',ROOT/'um.py',ROOT/'gate_extension.py']}
manifest={'run':str(RUN),'timestamp':datetime.datetime.now().astimezone().isoformat(),'origin':str(origin),'origin_manifest_sha256':hf(origin/'manifest.json'),'origin_compilation_sha256':hf(origin/'compilation.json'),'compiler':cfg['lean'],'compiler_sha256':m['compiler_sha256'],'lean_version':m['lean_version'],'lean_path':env['LEAN_PATH'],'sources':{rel:source},'dependencies':deps,'external_direct_pins':external,'declarations':targets,'artifacts_readonly':artifacts,'parent_custody_full_reaudit':False,'memory_writes':False,'author_build_on_lean_path':False}
save(RUN/'manifest.json',manifest);save(RUN/'author_history.json',history)
write(REV/'right_vector_first_latest_run.txt',str(RUN).encode())
audit='import TGLV350.ScalarGaussianRightPairs\n'
for n in targets:audit+='set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n'
write(RUN/'sources/RightVectorFirstAudit.lean',audit.encode())
print(json.dumps({'run':str(RUN),'project_dependencies':len(deps),'targets':len(targets),'historical_rc1':sum(x['returncode']!=0 for x in history)}),flush=True)
records=[]
for module in [rel,'RightVectorFirstAudit.lean']:
    s=RUN/'sources'/module;o=RUN/'build'/Path(module).with_suffix('.olean');o.parent.mkdir(parents=True,exist_ok=True);assert not o.exists()
    cmd=[cfg['lean'],'-o',str(o),str(s)];start=time.monotonic()
    p=subprocess.run(cmd,capture_output=True,cwd=RUN/'sources',env=env)
    stdout=RUN/'logs'/(Path(module).stem+'.stdout.txt');stderr=RUN/'logs'/(Path(module).stem+'.stderr.txt')
    write(stdout,p.stdout);write(stderr,p.stderr); ax=axioms(p.stdout.decode('utf-8',errors='replace'))
    row={'module':module,'command':cmd,'returncode':p.returncode,'seconds':round(time.monotonic()-start,3),'source_sha256':hf(s),'output_sha256':hf(o) if o.exists() else None,'stdout':str(stdout),'stderr':str(stderr),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),'axioms':ax,'exact_targets':set(ax)==set(targets),'axioms_allowed':bool(ax) and all(set(x)==allowed for x in ax.values())}
    if module==rel:row['binary_equals_author']=row['output_sha256']==source['author_binary_sha256']
    records.append(row);save(RUN/'compilation.json',{'complete':False,'records':records})
    print(json.dumps({k:row[k] for k in ['module','returncode','seconds','exact_targets','axioms_allowed']}),flush=True)
    if p.returncode:
        print(p.stdout.decode('utf-8',errors='replace'),flush=True);break
result={'complete':len(records)==2,'records':records,'all_exit_zero':len(records)==2 and all(x['returncode']==0 for x in records),'exact_6_targets':len(records)==2 and all(x['exact_targets'] for x in records),'all_axioms_allowed':all(x['axioms_allowed'] for x in records),'binary_equals_author':bool(records) and records[0].get('binary_equals_author',False),'author_source_binary_preserved':hf(src)==source['sha256'] and hf(ab)==source['author_binary_sha256'],'dependencies_preserved':all(hf(d['frozen_source'])==d['source_sha256'] and hf(d['frozen_binary'])==d['sha256'] and all(hf(p)==h for p,h in d['companions'].items()) for d in deps.values()),'external_direct_pins_preserved':all(hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256'] for d in external.values()),'read_only_artifacts_preserved':all(hf(p)==h for p,h in artifacts.items()),'author_final_log_streams_preserved':hf(log)==source['author_log_sha256'] and hf(a['stdout'])==source['author_stdout_sha256'] and hf(a['stderr'])==source['author_stderr_sha256']}
save(RUN/'compilation.json',result);print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
