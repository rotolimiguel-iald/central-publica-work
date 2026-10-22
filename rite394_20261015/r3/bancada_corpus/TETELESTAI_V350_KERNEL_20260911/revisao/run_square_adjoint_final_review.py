from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
RUN=REV/('square_adjoint_final_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
PROBE=REV/'square_adjoint_probe_20260913_053747_825645'
PREV=Path((REV/'square_approximation_latest_run.txt').read_text().strip())
sha=lambda b:hashlib.sha256(b).hexdigest()
hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
allowed={'propext','Classical.choice','Quot.sound'}
def write(p,b):
    assert p.resolve().is_relative_to(REV);p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;os.replace(t,p)
def save(p,d):write(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
def axioms(s):
    d={}
    for n,a in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",s,re.S):
        assert n not in d;d[n]=sorted(x.strip() for x in a.split(',') if x.strip())
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",s):assert n not in d;d[n]=[]
    return d
pm=load(PROBE/'manifest.json');prev=load(PREV/'manifest.json');pc=load(PREV/'compilation.json')
assert pc['all_exit_zero'] and pc['exact_9_and_15_targets'] and pc['new_binary_equal_author'] and pc['inherited_first_binary_preserved'] and pc['dependencies_preserved']
assert prev['compiler_sha256']==pm['compiler_sha256']==hf(pm['compiler'])
dp=ROOT/'square_resolvent_draft_status.json';draft=load(dp);doc=Path(draft['report_path']);prep=ROOT/'prepare_square_resolvent_stage.py'
assert list(draft['modules'])==['SquareResolventSupport','ScalarRightSquareApproximation','ScalarSquareAdjointTest']
assert len(draft['targets'])==20 and hf(doc)==draft['report_sha256']
readonly={str(p):hf(p) for p in [PROBE/'manifest.json',PREV/'manifest.json',PREV/'compilation.json',REV/'REVIEW_SQUARE_RESOLVENT_DEV.md',dp,doc,prep]}
for p in [dp,doc,prep]:write(RUN/'document_snapshots'/p.name,p.read_bytes())
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
for name,pin in draft['modules'].items():
    rel='TGLV350/'+name+'.lean';src=ROOT/'kernel'/rel;raw=src.read_bytes();lp=Path(pin['final_log']);lr=load(lp);binary=Path(lr['command'][2])
    assert lr['returncode']==lr['lean_returncode']==0 and lr['source_unchanged_during_compile'] and lr['output_exists']
    assert Path(lr['source'])==src and sha(raw)==lr['sha256']==pin['source_sha256'] and hf(binary)==lr['output_sha256']==pin['binary_sha256']
    assert hf(lp)==pin['final_log_sha256'] and hf(lr['stdout'])==pin['stdout_sha256'] and hf(lr['stderr'])==pin['stderr_sha256']
    clean=re.sub(r'/\-.*?\-/','',raw.decode(),flags=re.S);clean=re.sub(r'--[^\n]*','',clean)
    assert not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]',clean)
    assert '600000' not in clean
    targets=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)$',raw.decode(),re.M)]
    ax=axioms(Path(lr['stdout']).read_text(encoding='utf-8'))
    assert len(targets)==pin['targets'] and set(ax)==set(targets) and all(set(x)<=allowed for x in ax.values()) and not Path(lr['stderr']).read_bytes()
    snap=RUN/'sources'/rel;write(snap,raw)
    sources[rel]={'path':str(src),'snapshot':str(snap),'sha256':sha(raw),'declarations':targets,'author_log':str(lp),'author_log_sha256':hf(lp),'author_binary':str(binary),'author_binary_sha256':hf(binary),'author_stdout_sha256':hf(lr['stdout']),'author_stderr_sha256':hf(lr['stderr'])}
    authorax.update(ax)
    for p in [src,lp,binary,Path(lr['stdout']),Path(lr['stderr'])]:readonly[str(p)]=hf(p)
    for p in [lp,Path(lr['stdout']),Path(lr['stderr'])]:write(RUN/'author_final'/p.name,p.read_bytes())
    actualfailed=[]
    for hp in sorted((ROOT/'logs').glob(name+'_*.json')):
        hd=load(hp);row={'module':name,'log':str(hp),'log_sha256':hf(hp),'returncode':hd['returncode'],'source_sha256':hd['sha256'],'accepted_final':hp==lp}
        write(RUN/'author_history'/hp.name,hp.read_bytes())
        for k in ['stdout','stderr']:
            b=Path(hd[k]).read_bytes();write(RUN/'author_history'/Path(hd[k]).name,b);row[k+'_sha256']=sha(b)
        if hd['returncode']!=0:actualfailed.append(str(hp))
        history.append(row)
    assert sorted(actualfailed)==sorted(pin['failed_attempts'])
    if name!='ScalarSquareAdjointTest':
        inherited=deps['TGLV350.'+name];assert inherited['source_sha256']==pin['source_sha256'] and inherited['sha256']==pin['binary_sha256']
        assert prev['sources'][rel]['sha256']==pin['source_sha256']
assert authorax==draft['targets'] and len(authorax)==20
parent=Path(draft['parent_custody_path']);pv=ROOT/'bidual_right_support_custody_verification.json';pd=load(parent);pvd=load(pv)
assert hf(parent)==draft['parent_custody_sha256']==pvd['custody_sha256'] and pvd['custody_ok']
assert hf(ROOT/'um.py')==pd['working_sha256']==draft['integrated_working_sha256'] and hf(ROOT/'gate_extension.py')==pd['artifacts']['gate_extension.py']
assert len(pd['remaining_flags'])==6 and all(x is False for x in pd['remaining_flags'].values())
for p in [parent,pv,ROOT/'um.py',ROOT/'gate_extension.py']:readonly[str(p)]=hf(p)
for p in [parent,pv]:write(RUN/p.name,p.read_bytes())
external=prev['external_direct_pins']
for d in external.values():assert hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256']
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+pm['lean_path'].split(os.pathsep)[1:]);assert str(ROOT/'build') not in env['LEAN_PATH']
(RUN/'tmp').mkdir();env['TMP']=env['TEMP']=str(RUN/'tmp')
aud='import TGLV350.ScalarSquareAdjointTest\n'+''.join('set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n' for n in authorax)
write(RUN/'sources/SquareAdjointAudit20.lean',aud.encode())
manifest={'run':str(RUN),'timestamp':datetime.datetime.now().astimezone().isoformat(),'scope':'FINAL_DEV_THREE_MODULES_20_TARGETS',
 'compiler':pm['compiler'],'compiler_sha256':hf(pm['compiler']),'lean_path':env['LEAN_PATH'],'sources':sources,'declarations':list(authorax),'author_axioms':authorax,
 'dependencies':deps,'external_direct_pins':external,'readonly_pins':readonly,'parent_custody_sha256':hf(parent),'parent_full_reaudit':False,
 'draft_sha256':hf(dp),'report_sha256':hf(doc),'prepare_helper_sha256':hf(prep),'inherited_15_run':str(PREV),'inherited_15_compilation_sha256':hf(PREV/'compilation.json'),
 'own_dependency_provenance':pm['origins'],'probe_manifest_sha256':hf(PROBE/'manifest.json'),'author_project_build_on_lean_path':False,'dependencies_rebuilt':False,'memory_writes':False}
save(RUN/'manifest.json',manifest);save(RUN/'author_history.json',history);write(REV/'square_adjoint_final_latest_run.txt',str(RUN).encode())
print(json.dumps({'run':str(RUN),'deps':len(deps),'targets':len(authorax),'third_rc1_excluded':len(draft['modules']['ScalarSquareAdjointTest']['failed_attempts'])}),flush=True)
records=[]
for rel in ['TGLV350/ScalarSquareAdjointTest.lean','SquareAdjointAudit20.lean']:
    sp=RUN/'sources'/rel;bp=RUN/'build'/Path(rel).with_suffix('.olean');bp.parent.mkdir(parents=True,exist_ok=True);assert not bp.exists()
    cmd=[pm['compiler'],'-o',str(bp),str(sp)];start=time.monotonic();r=subprocess.run(cmd,cwd=RUN/'sources',env=env,capture_output=True)
    out=RUN/'logs'/(Path(rel).stem+'.stdout.txt');err=RUN/'logs'/(Path(rel).stem+'.stderr.txt');write(out,r.stdout);write(err,r.stderr)
    ax=axioms(r.stdout.decode('utf-8',errors='replace'));expected=sources[rel]['declarations'] if rel in sources else list(authorax)
    row={'module':rel,'command':cmd,'returncode':r.returncode,'seconds':round(time.monotonic()-start,3),'source_sha256':hf(sp),'output_sha256':hf(bp) if bp.exists() else None,'stdout':str(out),'stderr':str(err),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'axioms':ax,'exact_targets':set(ax)==set(expected),'axioms_match_author':ax=={n:authorax[n] for n in expected},'axioms_allowed':bool(ax) and all(set(x)<=allowed for x in ax.values())}
    if rel in sources:row['binary_equals_author']=row['output_sha256']==sources[rel]['author_binary_sha256']
    records.append(row);save(RUN/'compilation.json',{'complete':False,'records':records})
    print(json.dumps({k:row[k] for k in ['module','returncode','seconds','exact_targets','axioms_allowed']}),flush=True)
    if r.returncode:print(r.stdout.decode('utf-8',errors='replace'),flush=True);break
result={'complete':len(records)==2,'records':records,'all_exit_zero':len(records)==2 and all(x['returncode']==0 for x in records),'exact_5_and_20_targets':len(records)==2 and all(x['exact_targets'] for x in records),'all_axioms_allowed':all(x['axioms_allowed'] for x in records),'all_axioms_match_author':all(x['axioms_match_author'] for x in records),'new_binary_equal_author':records[0].get('binary_equals_author',False),'inherited_two_binaries_preserved':all(hf(deps['TGLV350.'+n]['frozen_binary'])==draft['modules'][n]['binary_sha256'] for n in ['SquareResolventSupport','ScalarRightSquareApproximation']),'source_snapshots_preserved':all(hf(d['snapshot'])==d['sha256'] for d in sources.values()),'readonly_artifacts_preserved':all(hf(p)==h for p,h in readonly.items()),'dependencies_preserved':all(hf(d['frozen_source'])==d['source_sha256'] and hf(d['frozen_binary'])==d['sha256'] and hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256'] and all(hf(p)==h for p,h in d['companions'].items()) for d in deps.values()),'external_direct_pins_preserved':all(hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256'] for d in external.values())}
save(RUN/'compilation.json',result);print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
