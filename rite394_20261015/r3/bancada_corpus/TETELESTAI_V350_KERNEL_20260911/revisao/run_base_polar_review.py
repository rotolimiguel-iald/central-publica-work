"""Isolated final module build and full 19-target base-polar auditor, with reviewer-owned project dependencies."""
from pathlib import Path
import ast,datetime,hashlib,json,os,re,subprocess,sys,time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=REV/('base_polar_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b:hashlib.sha256(b).hexdigest();hf=lambda p:sha(Path(p).read_bytes());load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV)
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b;tmp.replace(p)
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2).encode('utf-8'))
def imports(b):return re.findall(r'^import\s+([\w.]+)',b.decode('utf-8'),re.M)
def axioms(t):
    d={}
    for n,v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",t,re.S):
        a=[x.strip() for x in v.split(',') if x.strip()];assert n not in d or d[n]==a;d[n]=a
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",t):assert n not in d or not d[n];d[n]=[]
    return d
allowed={'propext','Classical.choice','Quot.sound'}
catalog={};origins={};compiler_hash=None
for pointer in ['local_base_polar_latest_run.txt']:
    origin=Path((REV/pointer).read_text().strip());m=load(origin/'manifest.json');c=load(origin/'compilation.json')
    assert c['complete'] and c['all_exit_zero'] and c['all_axioms_allowed'] and c['dependencies_preserved']
    assert compiler_hash in [None,m['compiler_sha256']];compiler_hash=m['compiler_sha256']
    for n,r in m['dependencies'].items():
        if n in catalog:assert catalog[n]['source_sha256']==r['source_sha256'] and catalog[n]['sha256']==r['sha256'],n
        catalog[n]={**r,'source':r['frozen_source'],'binary':r['frozen_binary'],'reviewer_origin':str(origin)}
    for rel,s in m['sources'].items():
        row=next(r for r in c['records'] if r['module']==rel);n=rel[:-5].replace('/','.')
        assert row['returncode']==0 and row['source_sha256']==s['sha256']
        if n in catalog:assert catalog[n]['source_sha256']==s['sha256'] and catalog[n]['sha256']==row['output_sha256'],n
        catalog[n]={'source':s['snapshot'],'binary':row['command'][2],'source_sha256':s['sha256'],
          'sha256':row['output_sha256'],'reviewer_origin':str(origin)}
    origins[str(origin)]={'manifest_sha256':hf(origin/'manifest.json'),'compilation_sha256':hf(origin/'compilation.json')}
package_paths=m['lean_path'].split(os.pathsep)[1:];lean_version=m['lean_version']
assert len(package_paths)==8 and all('.lake\\packages\\' in p for p in package_paths)
artifacts=['matrix_polar_custody.json','matrix_polar_custody_verification.json','base_polar_draft_status.json',
 'RELATORIO_CONJUGACAO_POLAR_BASE_DEV.md','make_base_polar_helpers.py','prepare_base_polar_stage.py',
 'record_base_polar_progress.py','verify_base_polar_custody.py']
for n in artifacts:write(RUN/n,(ROOT/n).read_bytes())
P=load(RUN/artifacts[0]);PV=load(RUN/artifacts[1])
assert hf(ROOT/artifacts[0])==PV['custody_sha256']
assert PV['custody_ok'] and PV['compiled_source_binary_pairs_reread']==176 and PV['immediate_byte_backups_and_prefixes']==34
assert hf(ROOT/'um.py')==P['working_sha256']
assert all(hf(p)==h for p,h in P['review_sha256'].items())
final_logs={'BasePolarStrongLimit':('20260912_194158_376425',3)}
D={'modules':{},'targets':{}}
for name,(timestamp,count) in final_logs.items():
 log=ROOT/'logs'/(name+'_'+timestamp+'.json');ar=load(log)
 out=Path(ar['stdout']).read_bytes();err=Path(ar['stderr']).read_bytes()
 D['modules'][name]={'source_sha256':ar['sha256'],'final_log':str(log),'final_log_sha256':hf(log),
  'binary_sha256':ar['output_sha256'],'stdout_sha256':sha(out),'stderr_sha256':sha(err),'targets':count,
  'failed_attempts':[str(lp) for lp in sorted((ROOT/'logs').glob(name+'_*.json')) if load(lp)['returncode']]}
 D['targets'].update({n:sorted(v) for n,v in axioms(out.decode()).items()})
F=load(ROOT/'base_polar_draft_status.json')
assert len(F['modules'])==4 and len(F['targets'])==19
assert F['parent_custody_sha256']==hf(ROOT/'matrix_polar_custody.json')
assert F['integrated_working_sha256']==P['working_sha256']
assert F['report_sha256']==hf(F['report_path'])
assert not any(F[k] for k in ['KMS_proved','modular_square_flow_identified','independent_review_complete','integrated','gate_changed','full_goal_complete'])
full_checks={};full_ax={}
for name,pin in F['modules'].items():
    sp=ROOT/'kernel/TGLV350'/(name+'.lean');bp=ROOT/'build/TGLV350'/(name+'.olean');lp=Path(pin['final_log']);ar=load(lp)
    assert hf(sp)==pin['source_sha256']==ar['sha256'] and hf(bp)==pin['binary_sha256']==ar['output_sha256']
    assert hf(lp)==pin['final_log_sha256'] and ar['source_unchanged_during_compile'] and ar['output_exists']
    assert ar['returncode']==ar['lean_returncode']==0
    assert hf(ar['stdout'])==pin['stdout_sha256'] and hf(ar['stderr'])==pin['stderr_sha256']
    aa=axioms(Path(ar['stdout']).read_text(encoding='utf-8'));assert len(aa)==pin['targets']
    full_ax.update({n:sorted(v) for n,v in aa.items()})
    if name in D['modules']:assert D['modules'][name]==pin
    else:
        n='TGLV350.'+name;assert catalog[n]['source_sha256']==pin['source_sha256'] and catalog[n]['sha256']==pin['binary_sha256']
    full_checks[name]={'source_sha256':hf(sp),'binary_sha256':hf(bp),'log_sha256':hf(lp),'matches_previous_own_build':name not in D['modules']}
assert full_ax==F['targets']
for name in artifacts:
    if name.endswith('.py'):ast.parse((ROOT/name).read_bytes())

save(RUN/'reviewer_input_pins.json',D)
surfaces={}
for p,h in P['surface_sha256'].items():
    sp=Path(p);bp=Path(P['backups'][p]);raw=sp.read_bytes();old=bp.read_bytes()
    assert sp.parent==bp.parent and sha(raw)==h and sha(old)==P['surface_before_sha256'][p]
    assert raw.startswith(old) and len(raw)>len(old)
    surfaces[p]={'sha256':h,'backup':str(bp),'before_sha256':sha(old),'exact_prefix':True,'bytes':len(raw)}
assert len(surfaces)==34
E=load(ROOT/'kernel_incremental_evidence.json');flags={k:E[k] for k in P['remaining_flags']}
assert len(flags)==6 and all(x is False for x in flags.values()) and not P['full_runtime']
sources={};targets=[];history=[]
for name,pin in D['modules'].items():
    rel='TGLV350/'+name+'.lean';src=ROOT/'kernel'/rel;raw=src.read_bytes();sp=RUN/'sources'/rel
    assert sha(raw)==pin['source_sha256'];write(sp,raw)
    log=Path(pin['final_log']);lr=log.read_bytes();ar=json.loads(lr)
    assert sha(lr)==pin['final_log_sha256'] and ar['returncode']==ar['lean_returncode']==0
    assert ar['source_unchanged_during_compile'] and ar['output_exists'] and ar['sha256']==sha(raw)
    binary=ROOT/'build'/Path(rel).with_suffix('.olean')
    assert Path(ar['command'][2])==binary and hf(binary)==pin['binary_sha256']==ar['output_sha256']
    out=Path(ar['stdout']).read_bytes();err=Path(ar['stderr']).read_bytes()
    assert sha(out)==pin['stdout_sha256'] and sha(err)==pin['stderr_sha256'] and not err
    printed=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)',raw.decode(),re.M)]
    assert len(printed)==pin['targets'];targets+=printed
    stripped=re.sub(r'/\-.*?\-/', '',raw.decode(),flags=re.S);stripped=re.sub(r'--[^\n]*','',stripped)
    named=['TGLV350.Regular.'+n for n in re.findall(r'^(?:def|theorem|abbrev|structure)\s+([\w.]+)',stripped,re.M)]
    assert set(printed)<=set(named) and not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]',stripped)
    aa=axioms(out.decode());assert set(aa)==set(printed) and all(set(x)==allowed and sorted(x)==D['targets'][n] for n,x in aa.items())
    sources[rel]={'path':str(src),'snapshot':str(sp),'sha256':sha(raw),'imports':imports(raw),'declarations':printed,
      'author_log':str(log),'author_log_sha256':sha(lr),'author_binary':str(binary),'author_binary_sha256':hf(binary),
      'author_stdout_sha256':sha(out),'author_stderr_sha256':sha(err),'unprinted_definitions':sorted(set(named)-set(printed))}
    failed=[]
    for lp in sorted((ROOT/'logs').glob(name+'_*.json')):
        rawlog=lp.read_bytes();r=json.loads(rawlog);write(RUN/'author_history'/lp.name,rawlog)
        item={'module':name,'log':str(lp),'log_sha256':sha(rawlog),'returncode':r['returncode'],'accepted_final':lp==log}
        for key in ['stdout','stderr']:
            p=Path(r[key]);b=p.read_bytes();write(RUN/'author_history'/p.name,b);item[key+'_sha256']=sha(b)
        if r['returncode']:failed.append(str(lp))
        history.append(item)
    assert failed==pin['failed_attempts']
    for item in history:
        if item['module']!=name or item['returncode']==0:continue
        failedlog=load(item['log']);matches=[]
        for backup in sorted(src.parent.glob(src.name+'.bak*')):
            b=backup.read_bytes()
            if sha(b)==failedlog['sha256']:
                write(RUN/'author_source_history'/backup.name,b)
                matches.append({'path':str(backup),'sha256':sha(b)})
        # Historical source copies, when available, are evidence only; final source pin governs acceptance.
        item['failed_source_backups']=matches

assert len(targets)==len(set(targets))==3 and set(targets)==set(D['targets'])
new_targets=list(targets)
prior_local=Path((REV/'local_base_polar_latest_run.txt').read_text().strip())
prior_local_manifest=load(prior_local/'manifest.json')
targets=prior_local_manifest['declarations']+targets
assert len(set(targets))==19
new={'TGLV350.'+n for n in D['modules']};seen=set();visiting=set();needed=set()
def visit(n):
    assert n not in visiting,n
    if n in seen:return
    if n in new:raw=Path(sources[n.replace('.','/')+'.lean']['snapshot']).read_bytes()
    elif n.split('.')[0] in {'TGLV350','TGLExt','TGL'}:
        assert n in catalog,n;needed.add(n);raw=Path(catalog[n]['source']).read_bytes()
    else:return
    visiting.add(n)
    for i in imports(raw):visit(i)
    visiting.remove(n);seen.add(n)
for n in new:visit(n)
deps={}
for n in sorted(needed):
    r=catalog[n];raw=Path(r['source']).read_bytes();br=Path(r['binary']).read_bytes()
    assert Path(r['binary']).resolve().is_relative_to(REV) and sha(raw)==r['source_sha256'] and sha(br)==r['sha256']
    rel=Path(*n.split('.'));live=(ROOT/'kernel'/rel.with_suffix('.lean')).read_bytes()
    if live!=raw:
        assert r.get('previously_reviewed_comment_only_erratum') is True,n
        assert raw.replace(r['frozen_old_comment'].encode(),r['live_corrected_comment'].encode())==live,n
    sp=RUN/'dependency_sources'/rel.with_suffix('.lean');bp=RUN/'build'/rel.with_suffix('.olean')
    write(sp,raw);write(bp,br)
    for cp in Path(r['binary']).parent.glob(Path(r['binary']).name+'.*'):
        if cp.is_file():write(bp.with_name(cp.name),cp.read_bytes())
    deps[n]={**r,'frozen_source':str(sp),'frozen_binary':str(bp),'live_source_sha256':sha(live),'imports':imports(raw)}
package_pins={}
for rel in ['Mathlib/Analysis/CStarAlgebra/PositiveLinearMap',
            'Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Range',
            'Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic']:
 candidates=[Path(p)/(rel+'.olean') for p in package_paths if (Path(p)/(rel+'.olean')).is_file()]
 assert len(candidates)==1,rel
 bp=candidates[0];src=next(q/(rel+'.lean') for q in bp.parents if (q/(rel+'.lean')).is_file())
 package_pins[rel]={'source':str(src),'source_sha256':hf(src),'binary':str(bp),'binary_sha256':hf(bp),'readonly_external_package':True}
cfg=load(ROOT/'environment.json');assert hf(cfg['lean'])==compiler_hash
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+package_paths)
(RUN/'tmp').mkdir(exist_ok=True);env['TMP']=env['TEMP']=str(RUN/'tmp')
m={'run':str(RUN),'origins':origins,'compiler_sha256':compiler_hash,'lean_version':lean_version,'lean_path':env['LEAN_PATH'],
 'sources':sources,'dependencies':deps,'external_direct_pins':package_pins,'declarations':targets,'new_declarations':new_targets,'full_draft_checks':full_checks,'memory_surfaces':surfaces,
 'artifact_pins':{n:hf(RUN/n) for n in artifacts},'working_sha256':hf(ROOT/'um.py'),'gate_sha256':hf(ROOT/'gate_extension.py'),
 'six_flags':flags,'previous_reviews':{str(p):hf(p) for p in REV.glob('REVIEW_*.md')},'parent_integrated_reaudit':False}
save(RUN/'manifest.json',m);save(RUN/'author_history.json',history);write(REV/'base_polar_latest_run.txt',str(RUN).encode())
audit='\n'.join('import TGLV350.'+n for n in F['modules'])+'\n'
for n in targets:audit+='set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n'
write(RUN/'sources/BasePolarAudit.lean',audit.encode())
print(json.dumps({'run':str(RUN),'dependencies':len(deps),'targets':len(targets),'memory_backups_verified':len(surfaces)}),flush=True)
records=[]
for rel in list(sources)+['BasePolarAudit.lean']:
    sp=RUN/'sources'/rel;op=RUN/'build'/Path(rel).with_suffix('.olean');op.parent.mkdir(parents=True,exist_ok=True);assert not op.exists()
    cmd=[cfg['lean'],'-o',str(op),str(sp)];t=time.monotonic();p=subprocess.run(cmd,capture_output=True,cwd=RUN/'sources',env=env)
    out=RUN/'logs'/(Path(rel).stem+'.stdout.txt');err=RUN/'logs'/(Path(rel).stem+'.stderr.txt');write(out,p.stdout);write(err,p.stderr)
    ax=axioms(p.stdout.decode('utf-8',errors='replace'));expected=set(sources[rel]['declarations']) if rel in sources else set(targets)
    row={'module':rel,'command':cmd,'returncode':p.returncode,'seconds':round(time.monotonic()-t,3),'source_sha256':hf(sp),
      'output_sha256':hf(op) if op.exists() else None,'axioms':ax,'axioms_allowed':bool(ax) and all(set(x)==allowed for x in ax.values()),
      'exact_targets':set(ax)==expected,'stdout':str(out),'stderr':str(err),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)}
    if rel in sources:row['binary_equals_author']=row['output_sha256']==sources[rel]['author_binary_sha256']
    records.append(row);save(RUN/'compilation.json',{'complete':False,'records':records})
    print(json.dumps({k:row[k] for k in ['module','returncode','seconds','axioms_allowed','exact_targets']}),flush=True)
    if p.returncode:print(p.stdout.decode('utf-8',errors='replace'),flush=True);break
done=len(records)==2 and all(r['returncode']==0 for r in records)
c={'complete':len(records)==2,'records':records,'all_exit_zero':done,'all_axioms_allowed':all(r['axioms_allowed'] for r in records),
 'exact_19_targets':done and set(records[-1]['axioms'])==set(targets) and all(r['exact_targets'] for r in records),
 'one_binary_equals_author':done and all(r.get('binary_equals_author',True) for r in records),
 'sources_author_binaries_unchanged':all(hf(s['path'])==s['sha256'] and hf(s['author_binary'])==s['author_binary_sha256'] for s in sources.values()),
 'dependencies_preserved':all(hf(r['frozen_source'])==r['source_sha256'] and hf(r['frozen_binary'])==r['sha256'] for r in deps.values()),
 'memory_and_backups_preserved':all(hf(p)==r['sha256'] and hf(r['backup'])==r['before_sha256'] for p,r in surfaces.items()),
 'previous_reviews_preserved':all(hf(p)==h for p,h in m['previous_reviews'].items()),
 'artifacts_unchanged':all(hf(ROOT/n)==h for n,h in m['artifact_pins'].items()),
 'external_direct_dependencies_preserved':all(hf(r['source'])==r['source_sha256'] and hf(r['binary'])==r['binary_sha256'] for r in package_pins.values()),
 'um_unchanged':hf(ROOT/'um.py')==m['working_sha256'],'gate_unchanged':hf(ROOT/'gate_extension.py')==m['gate_sha256']}
save(RUN/'compilation.json',c);print(json.dumps({k:x for k,x in c.items() if k!='records'}),flush=True)
