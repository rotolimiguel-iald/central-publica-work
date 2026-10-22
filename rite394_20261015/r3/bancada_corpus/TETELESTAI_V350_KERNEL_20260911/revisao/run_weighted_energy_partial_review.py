from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys,time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
PREV=REV/'paired_blocks27_independent_20260913_070702_176639'
RUN=REV/('weighted_energy_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
def put(p,b):
    assert p.resolve().is_relative_to(REV);p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p)
def save(p,x):put(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def axioms(text):
    d={}
    for n,v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",text,re.S):
        a=sorted(x.strip() for x in v.split(',') if x.strip());assert n not in d or d[n]==a;d[n]=a
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",text):assert n not in d or not d[n];d[n]=[]
    return d
imports=lambda b:re.findall(r'^import\s+([\w.]+)',b.decode(),re.M)
PM=load(PREV/'manifest.json');PC=load(PREV/'compilation.json')
assert all(PC[k] for k in ['complete','all_exit_zero','exact_27_targets','all_axioms_allowed','all_axioms_match_author','new_binary_equal_author','dependencies_preserved','external_direct_pins_preserved'])
catalog={n:{**d,'source':d['frozen_source'],'binary':d['frozen_binary'],'immediate_own_origin':str(PREV)} for n,d in PM['dependencies'].items()}
name='WeightedVariationalEnergy';rel='TGLV350/'+name+'.lean';src=ROOT/'kernel'/rel
lp=ROOT/'logs/WeightedVariationalEnergy_20260913_074553_539505.json';lr=load(lp);ab=Path(lr['command'][2]);raw=src.read_bytes()
assert Path(lr['source'])==src and lr['returncode']==lr['lean_returncode']==0 and lr['output_exists'] and lr['source_unchanged_during_compile']
assert sha(raw)==lr['sha256'] and hf(ab)==lr['output_sha256']
targets=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)$',raw.decode(),re.M)]
assert len(targets)==len(set(targets))==7
authorax=axioms(Path(lr['stdout']).read_text(encoding='utf-8'));allow={'propext','Classical.choice','Quot.sound'}
assert set(authorax)==set(targets) and all(set(a)==allow for a in authorax.values()) and not Path(lr['stderr']).read_bytes()
clean=re.sub(r'/\-.*?\-/','',raw.decode(),flags=re.S);clean=re.sub(r'--[^\n]*','',clean)
assert not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]',clean)
readonly={str(p):hf(p) for p in [src,ab,lp,Path(lr['stdout']),Path(lr['stderr']),PREV/'manifest.json',PREV/'compilation.json']}
for p in [lp,Path(lr['stdout']),Path(lr['stderr'])]:put(RUN/'author_final'/p.name,p.read_bytes())
snap=RUN/'sources'/rel;put(snap,raw)
history=[]
for p in sorted((ROOT/'logs').glob(name+'_*.json')):
    d=load(p);row={'log':str(p),'log_sha256':hf(p),'returncode':d['returncode'],'source_sha256':d['sha256'],'accepted_final':p==lp}
    put(RUN/'author_history'/p.name,p.read_bytes())
    for k in ['stdout','stderr']:
        b=Path(d[k]).read_bytes();put(RUN/'author_history'/Path(d[k]).name,b);row[k+'_sha256']=sha(b)
    history.append(row)
assert len(history)==3 and sum(x['returncode']!=0 for x in history)==2
parent=ROOT/'paired_blocks_custody.json';pd=load(parent);pv=load(ROOT/'paired_blocks_custody_verification.json')
assert pv['custody_ok'] and hf(parent)==pv['custody_sha256']
assert len(pd['surface_sha256'])==34 and len(pd['remaining_flags'])==6 and all(v is False for v in pd['remaining_flags'].values())
for p,h in {**pd['surface_sha256'],**pd['review_sha256']}.items():assert hf(p)==h;readonly[p]=h
for p,h in [(parent,hf(parent)),(ROOT/'um.py',pd['working_sha256']),(ROOT/'gate_extension.py',pd['artifacts']['gate_extension.py'])]:assert hf(p)==h;readonly[str(p)]=h
put(RUN/parent.name,parent.read_bytes());put(RUN/'paired_blocks_custody_verification.json',(ROOT/'paired_blocks_custody_verification.json').read_bytes())
needed=set()
def visit(n):
    if n in needed or n.split('.')[0] not in {'TGL','TGLExt','TGLV350'}:return
    assert n in catalog,n
    needed.add(n)
    for q in imports(Path(catalog[n]['source']).read_bytes()):visit(q)
for n in imports(raw):visit(n)
deps={}
for n in sorted(needed):
    d=catalog[n];sp=Path(d['source']);bp=Path(d['binary']);sb=sp.read_bytes();bb=bp.read_bytes()
    assert sp.resolve().is_relative_to(REV) and bp.resolve().is_relative_to(REV)
    assert sha(sb)==d['source_sha256'] and sha(bb)==d['sha256']
    part=Path(*n.split('.'));live=(ROOT/'kernel'/part.with_suffix('.lean')).read_bytes()
    if live!=sb:
        assert d.get('previously_reviewed_comment_only_erratum') is True,n
        assert sb.count(d['frozen_old_comment'].encode())==1 and sb.replace(d['frozen_old_comment'].encode(),d['live_corrected_comment'].encode())==live,n
    ds=RUN/'dependency_sources'/part.with_suffix('.lean');db=RUN/'build'/part.with_suffix('.olean');put(ds,sb);put(db,bb);companions={}
    for cp in bp.parent.glob(bp.name+'.*'):
        if cp.is_file():cb=cp.read_bytes();dest=db.with_name(cp.name);put(dest,cb);companions[str(dest)]=sha(cb)
    deps[n]={**d,'frozen_source':str(ds),'frozen_binary':str(db),'live_source_sha256':sha(live),'companions':companions}
external=PM['external_direct_pins']
for d in external.values():assert hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256']
compiler=PM['compiler'];assert hf(compiler)==PM['compiler_sha256']
pkg=PM['lean_path'].split(os.pathsep)[1:];assert len(pkg)==8 and all('.lake\\packages\\' in p for p in pkg)
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+pkg);assert str(ROOT/'build') not in env['LEAN_PATH']
(RUN/'tmp').mkdir();env['TMP']=env['TEMP']=str(RUN/'tmp')
audit='import TGLV350.WeightedVariationalEnergy\n'+''.join('set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n' for n in targets)
put(RUN/'sources/WeightedEnergyAudit7.lean',audit.encode())
M={'timestamp':datetime.datetime.now().astimezone().isoformat(),'run':str(RUN),'scope':'PARTIAL_DEV7_ONE_MODULE_ONLY','previous_own_run':str(PREV),'previous_manifest_sha256':hf(PREV/'manifest.json'),'previous_compilation_sha256':hf(PREV/'compilation.json'),'compiler':compiler,'compiler_sha256':hf(compiler),'lean_path':env['LEAN_PATH'],'sources':{rel:{'path':str(src),'snapshot':str(snap),'sha256':sha(raw),'author_binary':str(ab),'author_binary_sha256':hf(ab),'author_log':str(lp),'author_log_sha256':hf(lp),'author_stdout_sha256':hf(lr['stdout']),'author_stderr_sha256':hf(lr['stderr'])}},'declarations':targets,'author_axioms':authorax,'dependencies':deps,'external_direct_pins':external,'readonly_pins':readonly,'parent_custody_path':str(parent),'parent_custody_sha256':hf(parent),'author_project_build_on_lean_path':False,'packages_rebuilt':False,'memory_writes':False,'parent_full_reaudit':False,'stage_draft_not_required_for_partial':True}
save(RUN/'manifest.json',M);save(RUN/'author_history.json',history);put(REV/'weighted_energy_latest_run.txt',str(RUN).encode())
print(json.dumps({'run':str(RUN),'new_modules':1,'targets':7,'dependencies':len(deps),'author_failed_attempts_excluded':2}),flush=True)
records=[]
for mod in [rel,'WeightedEnergyAudit7.lean']:
    sp=RUN/'sources'/mod;bp=RUN/'build'/Path(mod).with_suffix('.olean');bp.parent.mkdir(parents=True,exist_ok=True);assert not bp.exists()
    cmd=[compiler,'-o',str(bp),str(sp)];start=time.monotonic();print(json.dumps({'starting':mod}),flush=True)
    rr=subprocess.run(cmd,cwd=RUN/'sources',env=env,capture_output=True)
    out=RUN/'logs'/(Path(mod).stem+'.stdout.txt');err=RUN/'logs'/(Path(mod).stem+'.stderr.txt');put(out,rr.stdout);put(err,rr.stderr)
    ax=axioms(rr.stdout.decode('utf-8',errors='replace'))
    row={'module':mod,'command':cmd,'returncode':rr.returncode,'seconds':round(time.monotonic()-start,3),'source_sha256':hf(sp),'output_exists':bp.exists(),'output_sha256':hf(bp) if bp.exists() else None,'stdout':str(out),'stderr':str(err),'stdout_sha256':sha(rr.stdout),'stderr_sha256':sha(rr.stderr),'axioms':ax,'exact_targets':set(ax)==set(targets),'axioms_match_author':ax==authorax,'axioms_allowed':bool(ax) and all(set(x)==allow for x in ax.values())}
    if mod==rel:row['binary_equals_author']=row['output_sha256']==hf(ab)
    records.append(row);save(RUN/'compilation.json',{'complete':False,'records':records});print(json.dumps({k:row[k] for k in ['module','returncode','seconds','exact_targets','axioms_allowed']}),flush=True)
    if rr.returncode:print(rr.stdout.decode('utf-8',errors='replace'),flush=True);break
res={'complete':len(records)==2,'records':records,'all_exit_zero':len(records)==2 and all(x['returncode']==0 for x in records),'exact_7_targets':len(records)==2 and all(x['exact_targets'] for x in records),'all_axioms_allowed':all(x['axioms_allowed'] for x in records),'all_axioms_match_author':all(x['axioms_match_author'] for x in records),'binary_equal_author':records[0].get('binary_equals_author',False),'source_snapshot_preserved':hf(snap)==sha(raw),'readonly_artifacts_preserved':all(hf(p)==h for p,h in readonly.items()),'dependencies_preserved':all(hf(d['frozen_source'])==d['source_sha256'] and hf(d['frozen_binary'])==d['sha256'] and hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['sha256'] and all(hf(p)==h for p,h in d['companions'].items()) for d in deps.values()),'external_direct_pins_preserved':all(hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256'] for d in external.values())}
save(RUN/'compilation.json',res);print(json.dumps({k:v for k,v in res.items() if k!='records'}),flush=True)
