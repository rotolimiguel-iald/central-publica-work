from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys,time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'square_resolvent_integrated_latest_run.txt').read_text().strip())
M=json.loads((RUN/'build_manifest.json').read_bytes());D=json.loads((RUN/'square_resolvent_draft_status.json').read_bytes())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,b):
    assert p.resolve().is_relative_to(REV);p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p)
def save(p,x):write(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def axioms(s):
    ax={};occurrences=[]
    for n,a in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",s,re.S):
        v=sorted(x.strip() for x in a.split(',') if x.strip());assert n not in ax or ax[n]==v;ax[n]=v;occurrences.append(n)
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",s):assert n not in ax or ax[n]==[];ax[n]=[];occurrences.append(n)
    return ax,len(occurrences)
assert hf(M['compiler'])==M['compiler_sha256']
assert all(hf(d['frozen_binary'])==d['binary_sha256'] for d in M['dependencies'].values())
assert all(hf(d['binary'])==d['sha256'] for d in M['external_direct_pins'].values())
env=os.environ.copy();env['LEAN_PATH']=M['lean_path'];assert str(ROOT/'build') not in env['LEAN_PATH']
(RUN/'tmp').mkdir(exist_ok=True);env['TMP']=env['TEMP']=str(RUN/'tmp')
records=[];allow={'propext','Classical.choice','Quot.sound'}
for mod in M['modules']:
    sp=Path(M['sources'][mod]['path']);bp=RUN/'build'/Path(mod.replace('.','/')).with_suffix('.olean');bp.parent.mkdir(parents=True,exist_ok=True)
    assert hf(sp)==M['sources'][mod]['sha256'] and not bp.exists()
    cmd=[M['compiler'],'-o',str(bp),str(sp)];start=time.monotonic()
    print(json.dumps({'starting':mod,'time':datetime.datetime.now().astimezone().isoformat()}),flush=True)
    res=subprocess.run(cmd,cwd=RUN/'sources',env=env,capture_output=True)
    out=RUN/'logs'/(mod+'.stdout.txt');err=RUN/'logs'/(mod+'.stderr.txt');write(out,res.stdout);write(err,res.stderr)
    ax,num=axioms(res.stdout.decode('utf-8',errors='replace'))
    if mod=='TGL.Audit':expected=set(M['expected_full_Audit_names'])
    elif mod=='TGLExt':expected=set()
    else:expected={'TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)$',sp.read_text(encoding='utf-8'),re.M)}
    row={'module':mod,'command':cmd,'cwd':str(RUN/'sources'),'returncode':res.returncode,'seconds':round(time.monotonic()-start,3),'source_sha256':hf(sp),'source_unchanged':hf(sp)==M['sources'][mod]['sha256'],'output_exists':bp.exists(),'output_sha256':hf(bp) if bp.exists() else None,'stdout':str(out),'stderr':str(err),'stdout_sha256':sha(res.stdout),'stderr_sha256':sha(res.stderr),'axioms':ax,'print_occurrences':num,'distinct_axioms':len(ax),'exact_targets':set(ax)==expected,'axioms_allowed':all(set(a)<=allow for a in ax.values()),'new_target_axioms_match_DEV':all(ax[n]==D['targets'][n] for n in expected&set(D['targets']))}
    records.append(row);save(RUN/'compilation.json',{'complete':False,'records':records})
    print(json.dumps({k:row[k] for k in ['module','returncode','seconds','distinct_axioms','exact_targets','axioms_allowed']}),flush=True)
    if res.returncode:print(res.stdout.decode('utf-8',errors='replace')[-12000:],flush=True);break
result={'complete':len(records)==5,'records':records,'all_five_exit_zero':len(records)==5 and all(x['returncode']==0 for x in records),'all_exact_targets':all(x['exact_targets'] for x in records),'all_axioms_allowed':all(x['axioms_allowed'] for x in records),'all_new_axioms_match_DEV':all(x['new_target_axioms_match_DEV'] for x in records),'dependencies_preserved':all(hf(d['frozen_binary'])==d['binary_sha256'] and hf(d['origin_binary'])==d['binary_sha256'] and hf(d['source'])==d['source_sha256'] and all(hf(p)==h for p,h in d['companions'].items()) for d in M['dependencies'].values()),'external_direct_pins_preserved':all(hf(d['binary'])==d['sha256'] for d in M['external_direct_pins'].values()),'dependency_provenance_counts':M['provenance_counts'],'limitation':'FRESH_EXECUTION_OF_FIVE_ONLY__PROJECT_DEPENDENCIES_INCLUDE_PINNED_AUTHOR_PARENT_AND_CANONICAL_BASE','author_integrated_results_compared':False,'no_author_code_executed':True}
save(RUN/'compilation.json',result);print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
