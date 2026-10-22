from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys,time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
PREV=Path((REV/'paired_blocks_latest_run.txt').read_text())
RUN=REV/('paired_blocks25_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b:hashlib.sha256(b).hexdigest()
hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
def put(p,b):
    assert p.resolve().is_relative_to(REV)
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b;os.replace(tmp,p)
def save(p,d):put(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
def imports(b):return re.findall(r'^import\s+([\w.]+)',b.decode(),re.M)
def axioms(t):
    d={}
    for n,v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",t,re.S):
        a=sorted(x.strip() for x in v.split(',') if x.strip());assert n not in d or d[n]==a;d[n]=a
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",t):d[n]=[]
    return d
allowed={'propext','Classical.choice','Quot.sound'}
pm=load(PREV/'manifest.json');pc=load(PREV/'compilation.json')
assert all(pc[k] for k in ['complete','all_exit_zero','exact_13_targets','all_axioms_allowed','all_axioms_match_author',
 'binary_equal_author','source_snapshot_preserved','readonly_artifacts_preserved','dependencies_preserved','external_direct_pins_preserved'])
readonly={str(PREV/'manifest.json'):hf(PREV/'manifest.json'),str(PREV/'compilation.json'):hf(PREV/'compilation.json')}
report=REV/'REVIEW_PAIRED_BLOCKS_DEV.md';readonly[str(report)]=hf(report)
catalog={n:{**d,'source':d['frozen_source'],'binary':d['frozen_binary'],'immediate_own_origin':str(PREV)} for n,d in pm['dependencies'].items()}
for rel,d in pm['sources'].items():
    row=next(x for x in pc['records'] if x['module']==rel);assert row['binary_equals_author']
    catalog[rel[:-5].replace('/','.')]=dict(source=d['snapshot'],binary=row['command'][2],
      source_sha256=d['sha256'],sha256=row['output_sha256'],immediate_own_origin=str(PREV))

name='ScalarPairedProjectionBlocks';rel=f'TGLV350/{name}.lean'
src=ROOT/'kernel'/rel;lp=ROOT/'logs'/f'{name}_20260913_065106_761132.json';lr=load(lp)
raw=src.read_bytes();ab=Path(lr['command'][2])
assert Path(lr['source'])==src and lr['returncode']==lr['lean_returncode']==0 and lr['output_exists'] and lr['source_unchanged_during_compile']
assert sha(raw)==lr['sha256'] and hf(ab)==lr['output_sha256']
newtargets=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)$',raw.decode(),re.M)]
assert len(newtargets)==len(set(newtargets))==12
targets=pm['declarations']+newtargets;assert len(targets)==len(set(targets))==25
authorax=axioms(Path(lr['stdout']).read_text(encoding='utf-8'))
assert set(authorax)==set(newtargets) and all(set(a)==allowed for a in authorax.values())
assert not Path(lr['stderr']).read_bytes()
allax={**pm['author_axioms'],**authorax}
clean=re.sub(r'/\-.*?\-/','',raw.decode(),flags=re.S);clean=re.sub(r'--[^\n]*','',clean)
assert not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]',clean)
for p in [src,ab,lp,Path(lr['stdout']),Path(lr['stderr'])]:readonly[str(p)]=hf(p)
for p in [lp,Path(lr['stdout']),Path(lr['stderr'])]:put(RUN/'author_final'/p.name,p.read_bytes())
snap=RUN/'sources'/rel;put(snap,raw)
history=[]
for p in sorted((ROOT/'logs').glob(name+'_*.json')):
    d=load(p);row={'log':str(p),'log_sha256':hf(p),'source_sha256':d['sha256'],'returncode':d['returncode'],'accepted_final':p==lp}
    put(RUN/'author_history'/p.name,p.read_bytes())
    for k in ['stdout','stderr']:
        b=Path(d[k]).read_bytes();put(RUN/'author_history'/Path(d[k]).name,b);row[k+'_sha256']=sha(b)
    history.append(row)

parent=Path(pm['parent_custody_path']);pd=load(parent)
assert hf(parent)==pm['parent_custody_sha256']
assert len(pd['surface_sha256'])==34 and len(pd['remaining_flags'])==6 and all(v is False for v in pd['remaining_flags'].values())
for p,h in {**pd['surface_sha256'],**pd['review_sha256']}.items():assert hf(p)==h;readonly[p]=h
for p,h in [(parent,pm['parent_custody_sha256']),(ROOT/'um.py',pd['working_sha256']),(ROOT/'gate_extension.py',pd['artifacts']['gate_extension.py'])]:assert hf(p)==h;readonly[str(p)]=h
put(RUN/parent.name,parent.read_bytes())

needed=set()
def visit(n):
    if n in needed or n.split('.')[0] not in {'TGL','TGLExt','TGLV350'}:return
    assert n in catalog,n
    needed.add(n)
    for q in imports(Path(catalog[n]['source']).read_bytes()):visit(q)
for n in imports(raw):visit(n)
deps={}
for n in sorted(needed):
    d=catalog[n];sp=Path(d['source']);bp=Path(d['binary']);s=sp.read_bytes();b=bp.read_bytes()
    assert sp.resolve().is_relative_to(REV) and bp.resolve().is_relative_to(REV)
    assert sha(s)==d['source_sha256'] and sha(b)==d['sha256'],n
    part=Path(*n.split('.'));live=(ROOT/'kernel'/part.with_suffix('.lean')).read_bytes()
    if live!=s:
        assert d.get('previously_reviewed_comment_only_erratum') is True,n
        assert s.count(d['frozen_old_comment'].encode())==1 and s.replace(d['frozen_old_comment'].encode(),d['live_corrected_comment'].encode())==live,n
    ds=RUN/'dependency_sources'/part.with_suffix('.lean');db=RUN/'build'/part.with_suffix('.olean')
    put(ds,s);put(db,b);companions={}
    for cp in bp.parent.glob(bp.name+'.*'):
        if cp.is_file():cb=cp.read_bytes();dest=db.with_name(cp.name);put(dest,cb);companions[str(dest)]=sha(cb)
    deps[n]={**d,'frozen_source':str(ds),'frozen_binary':str(db),'live_source_sha256':sha(live),'companions':companions}

external=pm['external_direct_pins']
for d in external.values():assert hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256']
compiler=pm['compiler'];assert hf(compiler)==pm['compiler_sha256']
pkg=pm['lean_path'].split(os.pathsep)[1:];assert len(pkg)==8 and all('.lake\\packages\\' in p for p in pkg)
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+pkg)
assert str(ROOT/'build') not in env['LEAN_PATH']
(RUN/'tmp').mkdir();env['TMP']=env['TEMP']=str(RUN/'tmp')
aud='import TGLV350.ScalarPairedProjectionBlocks\n'+''.join('set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n' for n in targets)
put(RUN/'sources/PairedBlocksAudit25.lean',aud.encode())
manifest={'run':str(RUN),'timestamp':datetime.datetime.now().astimezone().isoformat(),'scope':'PARTIAL_DEV25_13_INHERITED_12_NEW',
 'previous_own_run':str(PREV),'previous_compilation_sha256':hf(PREV/'compilation.json'),'previous_report_sha256':hf(report),
 'compiler':compiler,'compiler_sha256':hf(compiler),'lean_path':env['LEAN_PATH'],
 'sources':{rel:{'path':str(src),'snapshot':str(snap),'sha256':sha(raw),'author_binary':str(ab),'author_binary_sha256':hf(ab),'author_log':str(lp),
 'author_log_sha256':hf(lp),'author_stdout_sha256':hf(lr['stdout']),'author_stderr_sha256':hf(lr['stderr'])}},
 'declarations':targets,'new_declarations':newtargets,'author_axioms':allax,'dependencies':deps,'external_direct_pins':external,
 'readonly_pins':readonly,'parent_custody_path':str(parent),'parent_custody_sha256':hf(parent),
 'author_project_build_on_lean_path':False,'packages_rebuilt':False,'memory_writes':False,'parent_full_reaudit':False}
save(RUN/'manifest.json',manifest);save(RUN/'author_history.json',history)
put(REV/'paired_blocks25_latest_run.txt',str(RUN).encode())
print(json.dumps({'run':str(RUN),'new_modules':1,'new_targets':12,'cumulative_targets':25,'dependencies':len(deps),'author_failed_logs':sum(x['returncode']!=0 for x in history)}),flush=True)
records=[]
for module in [rel,'PairedBlocksAudit25.lean']:
    sp=RUN/'sources'/module;bp=RUN/'build'/Path(module).with_suffix('.olean');bp.parent.mkdir(parents=True,exist_ok=True);assert not bp.exists()
    cmd=[compiler,'-o',str(bp),str(sp)];start=time.monotonic();r=subprocess.run(cmd,cwd=RUN/'sources',env=env,capture_output=True)
    out=RUN/'logs'/(Path(module).stem+'.stdout.txt');err=RUN/'logs'/(Path(module).stem+'.stderr.txt');put(out,r.stdout);put(err,r.stderr)
    ax=axioms(r.stdout.decode('utf-8',errors='replace'));expected=newtargets if module==rel else targets
    row={'module':module,'command':cmd,'returncode':r.returncode,'seconds':round(time.monotonic()-start,3),'source_sha256':hf(sp),
      'output_sha256':hf(bp) if bp.exists() else None,'stdout':str(out),'stderr':str(err),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),
      'axioms':ax,'exact_targets':set(ax)==set(expected),'axioms_match_author':ax=={n:allax[n] for n in expected},
      'axioms_allowed':bool(ax) and all(set(x)==allowed for x in ax.values())}
    if module==rel:row['binary_equals_author']=row['output_sha256']==hf(ab)
    records.append(row);save(RUN/'compilation.json',{'complete':False,'records':records})
    print(json.dumps({k:row[k] for k in ['module','returncode','seconds','exact_targets','axioms_allowed']}),flush=True)
    if r.returncode:print(r.stdout.decode('utf-8',errors='replace'),flush=True);break
result={'complete':len(records)==2,'records':records,'all_exit_zero':len(records)==2 and all(x['returncode']==0 for x in records),
 'exact_25_targets':len(records)==2 and all(x['exact_targets'] for x in records),'all_axioms_allowed':all(x['axioms_allowed'] for x in records),
 'all_axioms_match_author':all(x['axioms_match_author'] for x in records),'new_binary_equal_author':records[0].get('binary_equals_author',False),
 'source_snapshot_preserved':hf(snap)==sha(raw),'readonly_artifacts_preserved':all(hf(p)==h for p,h in readonly.items()),
 'dependencies_preserved':all(hf(d['frozen_source'])==d['source_sha256'] and hf(d['frozen_binary'])==d['sha256'] and hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['sha256'] and all(hf(p)==h for p,h in d['companions'].items()) for d in deps.values()),
 'external_direct_pins_preserved':all(hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256'] for d in external.values())}
save(RUN/'compilation.json',result);print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
