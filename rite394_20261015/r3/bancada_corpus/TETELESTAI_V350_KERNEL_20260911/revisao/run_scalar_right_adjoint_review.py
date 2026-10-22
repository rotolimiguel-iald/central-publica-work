"""Review-owned isolated build of the separate five-target maximal-adjoint addendum."""
from pathlib import Path
import ast, datetime, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
RUN=REV/('scalar_right_adjoint_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
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
    assert tmp.read_bytes()==b; tmp.replace(p)
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2).encode('utf-8'))
def imports(b):return re.findall(r'^import\s+([\w.]+)',b.decode('utf-8'),re.M)
def axioms(t):
    d={n:[a.strip() for a in v.split(',') if a.strip()] for n,v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",t,re.S)}
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",t):d.setdefault(n,[])
    return d
allowed={'propext','Classical.choice','Quot.sound'}
catalog={}; origins={}; compiler_hash=None
for pointer in ['scalar_tomita_involution_latest_run.txt','scalar_right_tomita_latest_run.txt']:
    origin=Path((REV/pointer).read_text().strip()); m=load(origin/'manifest.json'); c=load(origin/'compilation.json')
    assert c['complete'] and c['all_exit_zero'] and c['all_axioms_allowed'] and c['dependencies_preserved']
    assert compiler_hash in [None,m['compiler_sha256']]; compiler_hash=m['compiler_sha256']
    for n,r in m['dependencies'].items():
        if n in catalog:assert catalog[n]['source_sha256']==r['source_sha256'] and catalog[n]['sha256']==r['sha256'],n
        catalog[n]={**r,'source':r['frozen_source'],'binary':r['frozen_binary'],'reviewer_origin':str(origin)}
    for rel,s in m['sources'].items():
        row=next(r for r in c['records'] if r['module']==rel); n=rel[:-5].replace('/','.')
        assert row['returncode']==0 and row['source_sha256']==s['sha256']
        if n in catalog:assert catalog[n]['source_sha256']==s['sha256'] and catalog[n]['sha256']==row['output_sha256'],n
        catalog[n]={'source':s['snapshot'],'binary':row['command'][2],'source_sha256':s['sha256'],
          'sha256':row['output_sha256'],'reviewer_origin':str(origin)}
    origins[str(origin)]={'manifest_sha256':hf(origin/'manifest.json'),'compilation_sha256':hf(origin/'compilation.json')}
    if pointer=='scalar_right_tomita_latest_run.txt':base_run=origin; base=m; base_compile=c
package_paths=base['lean_path'].split(os.pathsep)[1:]
assert len(package_paths)==8 and all('.lake\\packages\\' in p for p in package_paths)
artifacts=['scalar_right_adjoint_draft_status.json','record_scalar_right_adjoint_draft.py',
 'scalar_right_tomita_draft_status.json','scalar_right_tomita_draft_memory.json']
for n in artifacts:write(RUN/n,(ROOT/n).read_bytes())
D=load(RUN/artifacts[0]); MEM=load(RUN/artifacts[3])
assert D['module']=='ScalarRightTomitaAdjoint' and len(D['targets'])==5
assert not any(D[k] for k in ['KMS_proved','independent_review_complete','integrated','gate_changed'])
assert D['memory_update_pending_review_in_this_turn'] and D['same_maximal_adjoint']
assert hf(ROOT/artifacts[2])==D['parent_draft_sha256']==base['artifact_pins'][artifacts[2]]
assert hf(ROOT/artifacts[3])==D['parent_memory_sha256']==base['artifact_pins'][artifacts[3]]
assert hf(ROOT/'um.py')==D['working_sha256']==base['working_sha256']
assert len(base['memory_surfaces'])==34 and base_compile['memory_and_backups_preserved']
for p,r in base['memory_surfaces'].items():
    old=Path(r['backup']).read_bytes(); raw=Path(p).read_bytes()
    assert sha(raw)==r['sha256'] and sha(old)==r['before_sha256'] and raw.startswith(old)
ast.parse((RUN/'record_scalar_right_adjoint_draft.py').read_bytes())
rel='TGLV350/ScalarRightTomitaAdjoint.lean'; src=ROOT/'kernel'/rel; raw=src.read_bytes(); sp=RUN/'sources'/rel
assert sha(raw)==D['source_sha256'];write(sp,raw)
log=Path(D['log_path']); lr=log.read_bytes(); ar=json.loads(lr)
assert sha(lr)==D['log_sha256'] and ar['returncode']==ar['lean_returncode']==0
assert ar['source_unchanged_during_compile'] and ar['output_exists'] and ar['sha256']==sha(raw)
binary=ROOT/'build'/Path(rel).with_suffix('.olean')
assert Path(ar['command'][2])==binary and hf(binary)==D['binary_sha256']==ar['output_sha256']
out=Path(ar['stdout']).read_bytes();err=Path(ar['stderr']).read_bytes()
assert sha(out)==D['stdout_sha256'] and sha(err)==D['stderr_sha256'] and not err
targets=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)',raw.decode(),re.M)]
stripped=re.sub(r'/\-.*?\-/', '',raw.decode(),flags=re.S);stripped=re.sub(r'--[^\n]*','',stripped)
named=['TGLV350.Regular.'+n for n in re.findall(r'^(?:def|theorem|abbrev|structure)\s+([\w.]+)',stripped,re.M)]
assert len(targets)==len(set(targets))==5 and set(targets)==set(named)==set(D['targets'])
assert not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]',stripped)
aa=axioms(out.decode());assert set(aa)==set(targets) and all(set(x)==allowed and sorted(x)==D['targets'][n] for n,x in aa.items())
sources={rel:{'path':str(src),'snapshot':str(sp),'sha256':sha(raw),'imports':imports(raw),'declarations':targets,
 'author_log':str(log),'author_log_sha256':sha(lr),'author_binary':str(binary),'author_binary_sha256':hf(binary),
 'author_stdout_sha256':sha(out),'author_stderr_sha256':sha(err)}}
history=[]
for lp in sorted((ROOT/'logs').glob('ScalarRightTomitaAdjoint_*.json')):
    rawlog=lp.read_bytes(); r=json.loads(rawlog);write(RUN/'author_history'/lp.name,rawlog)
    item={'log':str(lp),'log_sha256':sha(rawlog),'returncode':r['returncode'],'accepted_final':lp==log}
    for key in ['stdout','stderr']:
        p=Path(r[key]);b=p.read_bytes();write(RUN/'author_history'/p.name,b);item[key+'_sha256']=sha(b)
    history.append(item)
seen=set(); visiting=set(); needed=set()
def visit(n):
    assert n not in visiting,n
    if n in seen:return
    if n=='TGLV350.ScalarRightTomitaAdjoint':b=raw
    elif n.split('.')[0] in {'TGLV350','TGLExt','TGL'}:
        assert n in catalog,n;needed.add(n);b=Path(catalog[n]['source']).read_bytes()
    else:return
    visiting.add(n)
    for i in imports(b):visit(i)
    visiting.remove(n);seen.add(n)
visit('TGLV350.ScalarRightTomitaAdjoint')
deps={}
for n in sorted(needed):
    r=catalog[n];b=Path(r['source']).read_bytes();br=Path(r['binary']).read_bytes()
    assert Path(r['binary']).resolve().is_relative_to(REV) and sha(b)==r['source_sha256'] and sha(br)==r['sha256']
    rr=Path(*n.split('.'));live=(ROOT/'kernel'/rr.with_suffix('.lean')).read_bytes()
    if live!=b:
        assert r.get('previously_reviewed_comment_only_erratum') is True,n
        assert b.replace(r['frozen_old_comment'].encode(),r['live_corrected_comment'].encode())==live,n
    fs=RUN/'dependency_sources'/rr.with_suffix('.lean');fb=RUN/'build'/rr.with_suffix('.olean')
    write(fs,b);write(fb,br)
    for cp in Path(r['binary']).parent.glob(Path(r['binary']).name+'.*'):
        if cp.is_file():write(fb.with_name(cp.name),cp.read_bytes())
    deps[n]={**r,'frozen_source':str(fs),'frozen_binary':str(fb),'live_source_sha256':sha(live),'imports':imports(b)}
cfg=load(ROOT/'environment.json');assert hf(cfg['lean'])==compiler_hash
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+package_paths)
(RUN/'tmp').mkdir(exist_ok=True);env['TMP']=env['TEMP']=str(RUN/'tmp')
m={'run':str(RUN),'origins':origins,'compiler_sha256':compiler_hash,'lean_version':base['lean_version'],
 'lean_path':env['LEAN_PATH'],'sources':sources,'dependencies':deps,'declarations':targets,
 'initial_12_run':str(base_run),'initial_12_manifest_sha256':hf(base_run/'manifest.json'),
 'initial_12_compilation_sha256':hf(base_run/'compilation.json'),
 'memory_surfaces':base['memory_surfaces'],'artifact_pins':{n:hf(RUN/n) for n in artifacts},
 'working_sha256':hf(ROOT/'um.py'),'gate_sha256':hf(ROOT/'gate_extension.py'),'six_flags':base['six_flags'],
 'previous_reviews':{str(p):hf(p) for p in REV.glob('REVIEW_*.md')},'parent_integrated_reaudit':False}
save(RUN/'manifest.json',m);save(RUN/'author_history.json',history)
write(REV/'scalar_right_adjoint_latest_run.txt',str(RUN).encode())
audit='import TGLV350.ScalarRightTomitaAdjoint\n'
for n in targets:audit+='set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n'
write(RUN/'sources/ScalarRightAdjointAudit.lean',audit.encode())
print(json.dumps({'run':str(RUN),'dependencies':len(deps),'targets':len(targets),'unchanged_memory_backups':34}),flush=True)
records=[]
for rr in [rel,'ScalarRightAdjointAudit.lean']:
    s=RUN/'sources'/rr;o=RUN/'build'/Path(rr).with_suffix('.olean');o.parent.mkdir(parents=True,exist_ok=True);assert not o.exists()
    cmd=[cfg['lean'],'-o',str(o),str(s)];t=time.monotonic();p=subprocess.run(cmd,capture_output=True,cwd=RUN/'sources',env=env)
    stdout=RUN/'logs'/(Path(rr).stem+'.stdout.txt');stderr=RUN/'logs'/(Path(rr).stem+'.stderr.txt')
    write(stdout,p.stdout);write(stderr,p.stderr);ax=axioms(p.stdout.decode('utf-8',errors='replace'))
    row={'module':rr,'command':cmd,'returncode':p.returncode,'seconds':round(time.monotonic()-t,3),'source_sha256':hf(s),
     'output_sha256':hf(o) if o.exists() else None,'axioms':ax,'axioms_allowed':bool(ax) and all(set(x)==allowed for x in ax.values()),
     'exact_targets':set(ax)==set(targets),'stdout':str(stdout),'stderr':str(stderr),
     'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)}
    if rr==rel:row['binary_equals_author']=row['output_sha256']==D['binary_sha256']
    records.append(row);save(RUN/'compilation.json',{'complete':False,'records':records})
    print(json.dumps({k:row[k] for k in ['module','returncode','seconds','axioms_allowed','exact_targets']}),flush=True)
    if p.returncode:print(p.stdout.decode('utf-8',errors='replace'),flush=True);break
done=len(records)==2 and all(r['returncode']==0 for r in records)
c={'complete':len(records)==2,'records':records,'all_exit_zero':done,
 'all_axioms_allowed':all(r['axioms_allowed'] for r in records),'exact_5_targets':done and all(r['exact_targets'] for r in records),
 'binary_equals_author':done and records[0]['binary_equals_author'],
 'sources_author_binaries_unchanged':hf(src)==D['source_sha256'] and hf(binary)==D['binary_sha256'],
 'dependencies_preserved':all(hf(r['frozen_source'])==r['source_sha256'] and hf(r['frozen_binary'])==r['sha256'] for r in deps.values()),
 'memory_and_backups_preserved':all(hf(p)==r['sha256'] and hf(r['backup'])==r['before_sha256'] for p,r in m['memory_surfaces'].items()),
 'initial_12_evidence_preserved':hf(base_run/'manifest.json')==m['initial_12_manifest_sha256'] and hf(base_run/'compilation.json')==m['initial_12_compilation_sha256'],
 'previous_reviews_preserved':all(hf(p)==h for p,h in m['previous_reviews'].items()),
 'artifacts_unchanged':all(hf(ROOT/n)==h for n,h in m['artifact_pins'].items()),
 'um_unchanged':hf(ROOT/'um.py')==m['working_sha256'],'gate_unchanged':hf(ROOT/'gate_extension.py')==m['gate_sha256']}
save(RUN/'compilation.json',c);print(json.dumps({k:x for k,x in c.items() if k!='records'}),flush=True)
