from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
RUN=REV/('square_approximation_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
PROBE=REV/'difference_squares_probe_20260913_050749_578468'
FIRST=Path((REV/'square_resolvent_latest_run.txt').read_text().strip())
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
def axioms(s):
    d={}
    for n,a in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",s,re.S):
        assert n not in d;d[n]=sorted(x.strip() for x in a.split(',') if x.strip())
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",s):
        assert n not in d;d[n]=[]
    return d
pm=load(PROBE/'manifest.json');fm=load(FIRST/'manifest.json');fc=load(FIRST/'compilation.json')
assert fc['all_exit_zero'] and fc['exact_6_targets'] and fc['binary_equal_author'] and fc['dependencies_preserved']
assert fm['compiler_sha256']==pm['compiler_sha256']==hf(pm['compiler'])
readonly={str(p):hf(p) for p in [PROBE/'manifest.json',FIRST/'manifest.json',FIRST/'compilation.json',REV/'REVIEW_SQUARE_RESOLVENT_DEV.md']}
deps={}
for n,d in pm['dependencies'].items():
    sp=Path(d['source']);bp=Path(d['copied_binary'])
    assert sp.resolve().is_relative_to(REV) and bp.resolve().is_relative_to(REV)
    assert hf(sp)==d['source_sha256'] and hf(bp)==d['binary_sha256'],n
    rel=Path(*n.split('.'));ns=RUN/'dependency_sources'/rel.with_suffix('.lean');nb=RUN/'build'/rel.with_suffix('.olean')
    write(ns,sp.read_bytes());write(nb,bp.read_bytes());companions={}
    for old,h in d.get('companions',{}).items():
        assert hf(old)==h;dest=nb.with_name(Path(old).name);write(dest,Path(old).read_bytes());companions[str(dest)]=h
    deps[n]={**d,'frozen_source':str(ns),'frozen_binary':str(nb),'sha256':d['binary_sha256'],'companions':companions}
sources={};authorax={};history=[]
logs={'TGLV350/SquareResolventSupport.lean':'SquareResolventSupport_20260913_044645_335207.json',
      'TGLV350/ScalarRightSquareApproximation.lean':'ScalarRightSquareApproximation_20260913_051502_178209.json'}
for rel,log in logs.items():
    src=ROOT/'kernel'/rel;lp=ROOT/'logs'/log;lr=load(lp);raw=src.read_bytes();binary=Path(lr['command'][2])
    assert lr['returncode']==lr['lean_returncode']==0 and lr['source_unchanged_during_compile'] and lr['output_exists']
    assert Path(lr['source'])==src and sha(raw)==lr['sha256'] and hf(binary)==lr['output_sha256']
    clean=re.sub(r'/\-.*?\-/','',raw.decode(),flags=re.S);clean=re.sub(r'--[^\n]*','',clean)
    assert not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]',clean)
    targets=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)$',raw.decode(),re.M)]
    ax=axioms(Path(lr['stdout']).read_text(encoding='utf-8'))
    assert set(ax)==set(targets) and all(set(x)<=allowed for x in ax.values()) and not Path(lr['stderr']).read_bytes()
    snap=RUN/'sources'/rel;write(snap,raw)
    sources[rel]={'path':str(src),'snapshot':str(snap),'sha256':sha(raw),'declarations':targets,'author_log':str(lp),'author_log_sha256':hf(lp),'author_binary':str(binary),'author_binary_sha256':hf(binary),'author_stdout_sha256':hf(lr['stdout']),'author_stderr_sha256':hf(lr['stderr'])}
    authorax.update(ax)
    for p in [src,lp,binary,Path(lr['stdout']),Path(lr['stderr'])]:readonly[str(p)]=hf(p)
    for p in [lp,Path(lr['stdout']),Path(lr['stderr'])]:write(RUN/'author_final'/p.name,p.read_bytes())
    for hp in sorted((ROOT/'logs').glob(Path(rel).stem+'_*.json')):
        hd=load(hp);row={'log':str(hp),'log_sha256':hf(hp),'returncode':hd['returncode'],'source_sha256':hd['sha256'],'accepted_final':hp==lp}
        write(RUN/'author_history'/hp.name,hp.read_bytes())
        for k in ['stdout','stderr']:
            b=Path(hd[k]).read_bytes();write(RUN/'author_history'/Path(hd[k]).name,b);row[k+'_sha256']=sha(b)
        history.append(row)
assert len(authorax)==15
first=sources['TGLV350/SquareResolventSupport.lean'];firstdep=deps['TGLV350.SquareResolventSupport']
assert first['sha256']==firstdep['source_sha256'] and first['author_binary_sha256']==firstdep['sha256']
assert first['sha256']==fm['sources']['TGLV350/SquareResolventSupport.lean']['sha256']
parent=ROOT/'bidual_right_support_custody.json';pv=ROOT/'bidual_right_support_custody_verification.json';pd=load(parent);pvd=load(pv)
assert pvd['custody_sha256']==hf(parent) and pvd['custody_ok']
assert hf(ROOT/'um.py')==pd['working_sha256'] and hf(ROOT/'gate_extension.py')==pd['artifacts']['gate_extension.py']
assert len(pd['remaining_flags'])==6 and all(x is False for x in pd['remaining_flags'].values())
for p in [parent,pv,ROOT/'um.py',ROOT/'gate_extension.py']:readonly[str(p)]=hf(p)
for p in [parent,pv]:write(RUN/p.name,p.read_bytes())
external=fm['external_direct_pins']
for d in external.values():assert hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256']
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+pm['lean_path'].split(os.pathsep)[1:]);assert str(ROOT/'build') not in env['LEAN_PATH']
(RUN/'tmp').mkdir();env['TMP']=env['TEMP']=str(RUN/'tmp')
aud='import TGLV350.ScalarRightSquareApproximation\n'+''.join('set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n' for n in authorax)
write(RUN/'sources/SquareApproximationAudit15.lean',aud.encode())
manifest={'run':str(RUN),'timestamp':datetime.datetime.now().astimezone().isoformat(),'scope':'DEV_TWO_MODULES_15_TARGETS_NO_THIRD_MODULE',
 'compiler':pm['compiler'],'compiler_sha256':hf(pm['compiler']),'lean_path':env['LEAN_PATH'],'sources':sources,'declarations':list(authorax),'author_axioms':authorax,
 'dependencies':deps,'external_direct_pins':external,'readonly_pins':readonly,'parent_custody_sha256':hf(parent),'parent_full_reaudit':False,
 'inherited_first_run':str(FIRST),'inherited_first_compilation_sha256':hf(FIRST/'compilation.json'),'own_dependency_provenance':pm['origins'],'probe_manifest_sha256':hf(PROBE/'manifest.json'),
 'author_project_build_on_lean_path':False,'dependencies_rebuilt':False,'memory_writes':False}
save(RUN/'manifest.json',manifest);save(RUN/'author_history.json',history);write(REV/'square_approximation_latest_run.txt',str(RUN).encode())
print(json.dumps({'run':str(RUN),'deps':len(deps),'targets':len(authorax),'author_rc1_excluded':sum(r['returncode']!=0 for r in history)}),flush=True)
records=[]
for rel in ['TGLV350/ScalarRightSquareApproximation.lean','SquareApproximationAudit15.lean']:
    sp=RUN/'sources'/rel;bp=RUN/'build'/Path(rel).with_suffix('.olean');bp.parent.mkdir(parents=True,exist_ok=True);assert not bp.exists()
    cmd=[pm['compiler'],'-o',str(bp),str(sp)];start=time.monotonic();r=subprocess.run(cmd,cwd=RUN/'sources',env=env,capture_output=True)
    out=RUN/'logs'/(Path(rel).stem+'.stdout.txt');err=RUN/'logs'/(Path(rel).stem+'.stderr.txt');write(out,r.stdout);write(err,r.stderr)
    ax=axioms(r.stdout.decode('utf-8',errors='replace'));expected=sources[rel]['declarations'] if rel in sources else list(authorax)
    row={'module':rel,'command':cmd,'returncode':r.returncode,'seconds':round(time.monotonic()-start,3),'source_sha256':hf(sp),'output_sha256':hf(bp) if bp.exists() else None,'stdout':str(out),'stderr':str(err),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'axioms':ax,'exact_targets':set(ax)==set(expected),'axioms_match_author':ax=={n:authorax[n] for n in expected},'axioms_allowed':bool(ax) and all(set(x)<=allowed for x in ax.values())}
    if rel in sources:row['binary_equals_author']=row['output_sha256']==sources[rel]['author_binary_sha256']
    records.append(row);save(RUN/'compilation.json',{'complete':False,'records':records})
    print(json.dumps({k:row[k] for k in ['module','returncode','seconds','exact_targets','axioms_allowed']}),flush=True)
    if r.returncode:print(r.stdout.decode('utf-8',errors='replace'),flush=True);break
result={'complete':len(records)==2,'records':records,'all_exit_zero':len(records)==2 and all(x['returncode']==0 for x in records),'exact_9_and_15_targets':len(records)==2 and all(x['exact_targets'] for x in records),'all_axioms_allowed':all(x['axioms_allowed'] for x in records),'all_axioms_match_author':all(x['axioms_match_author'] for x in records),'new_binary_equal_author':records[0].get('binary_equals_author',False),'inherited_first_binary_preserved':hf(firstdep['frozen_binary'])==first['author_binary_sha256'],'source_snapshots_preserved':all(hf(d['snapshot'])==d['sha256'] for d in sources.values()),'readonly_artifacts_preserved':all(hf(p)==h for p,h in readonly.items()),'dependencies_preserved':all(hf(d['frozen_source'])==d['source_sha256'] and hf(d['frozen_binary'])==d['sha256'] and hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256'] and all(hf(p)==h for p,h in d['companions'].items()) for d in deps.values()),'external_direct_pins_preserved':all(hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256'] for d in external.values())}
save(RUN/'compilation.json',result);print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
