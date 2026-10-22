"""Independent five-module DEV review. All writes are confined to revisao."""
from pathlib import Path
import ast, datetime, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent
ROOT=REV.parent
PRE=Path((REV/'scalar_weight_gns_latest_run.txt').read_text().strip())
RUN=REV/('homogeneous_right_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b: hashlib.sha256(b).hexdigest()
load=lambda p: json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV)
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b
    tmp.replace(p)
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2).encode('utf-8'))
def imports(b):return re.findall(r'^import\s+([\w.]+)',b.decode('utf-8'),re.M)
def axioms(t):
    d={n:[a.strip() for a in v.split(',') if a.strip()] for n,v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",t,re.S)}
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",t):d.setdefault(n,[])
    return d
allowed={'propext','Classical.choice','Quot.sound'}
pm=load(PRE/'manifest.json');pc=load(PRE/'compilation.json')
assert all(pc[k] for k in ['complete','all_exit_zero','exact_60_targets','all_axioms_allowed','dependencies_preserved'])
catalog={n:{**r,'source':r['frozen_source'],'binary':r['frozen_binary'],'reviewer_origin':str(PRE)} for n,r in pm['dependencies'].items()}
for rel,s in pm['sources'].items():
    r=next(r for r in pc['records'] if r['module']==rel)
    assert r['returncode']==0 and r['source_sha256']==s['sha256']
    catalog[rel[:-5].replace('/','.') ]={'source':s['snapshot'],'binary':r['command'][2],
      'source_sha256':s['sha256'],'sha256':r['output_sha256'],'reviewer_origin':str(PRE)}
statusraw=(ROOT/'homogeneous_right_draft_status.json').read_bytes();status=json.loads(statusraw)
assert len(status['modules'])==5 and len(status['targets'])==28 and status['integrated'] is False
custodyraw=Path(status['parent_custody_path']).read_bytes();custody=json.loads(custodyraw)
assert sha(custodyraw)==status['parent_custody_sha256']
assert sha((ROOT/'um.py').read_bytes())==custody['working_sha256']==status['integrated_working_sha256']
doc=(ROOT/'RELATORIO_DIREITA_MODULAR_GNS_DEV.md').read_bytes();assert sha(doc)==status['report_sha256']
recorder=(ROOT/'record_homogeneous_right_memory.py').read_bytes();ast.parse(recorder.decode('utf-8-sig'))
evidence=load(ROOT/'kernel_incremental_evidence.json')
assert len(custody['remaining_flags'])==6 and all(evidence[k] is False for k in custody['remaining_flags'])
surfaces={p:sha(Path(p).read_bytes()) for p in custody['surface_sha256']}
assert len(surfaces)==34 and surfaces==custody['surface_sha256']
for n,b in [('homogeneous_right_draft_status.json',statusraw),('scalar_weight_gns_custody.json',custodyraw),
 ('RELATORIO_DIREITA_MODULAR_GNS_DEV.md',doc),('record_homogeneous_right_memory.py',recorder)]:write(RUN/n,b)
sources={};targets=[];history=[]
for name,pin in status['modules'].items():
    rel='TGLV350/'+name+'.lean';src=ROOT/'kernel'/rel;raw=src.read_bytes();snap=RUN/'sources'/rel
    assert sha(raw)==pin['source_sha256'];write(snap,raw)
    log=Path(pin['final_log']);lr=log.read_bytes();ar=json.loads(lr)
    assert sha(lr)==pin['final_log_sha256'] and ar['returncode']==ar['lean_returncode']==0
    assert ar['sha256']==sha(raw) and ar['source_unchanged_during_compile'] is True and ar['output_exists']
    binary=ROOT/'build'/Path(rel).with_suffix('.olean')
    assert Path(ar['command'][2])==binary and sha(binary.read_bytes())==pin['binary_sha256']==ar['output_sha256']
    out=Path(ar['stdout']).read_bytes();assert sha(out)==pin['stdout_sha256']
    printed=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)',raw.decode(),re.M)]
    assert len(printed)==pin['targets'] and set(printed)<=set(status['targets']);targets+=printed
    stripped=re.sub(r'/\-.*?\-/', '',raw.decode(),flags=re.S);stripped=re.sub(r'--[^\n]*','',stripped)
    named=['TGLV350.Regular.'+n for n in re.findall(r'^(?:def|theorem|abbrev|structure)\s+([\w.]+)',stripped,re.M)]
    assert set(printed)<=set(named)
    assert not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]|transparency',stripped)
    aa=axioms(out.decode());assert set(aa)==set(printed) and all(set(a)==set(status['targets'][n])<=allowed for n,a in aa.items())
    sources[rel]={'path':str(src),'snapshot':str(snap),'sha256':sha(raw),'lines':len(raw.splitlines()),'imports':imports(raw),
      'declarations':printed,'unprinted_helpers':sorted(set(named)-set(printed)),
      'author_log':str(log),'author_log_sha256':sha(lr),'author_binary':str(binary),'author_binary_sha256':sha(binary.read_bytes()),'author_axioms':aa}
    for lp in sorted((ROOT/'logs').glob(name+'_*.json')):
        jr=lp.read_bytes();record=json.loads(jr);write(RUN/'author_history'/lp.name,jr)
        item={'module':name,'log':str(lp),'log_sha256':sha(jr),'returncode':record['returncode'],'accepted_final':lp==log,'source_sha256':record['sha256']}
        for key in ['stdout','stderr']:
            p=Path(record[key]);b=p.read_bytes();write(RUN/'author_history'/p.name,b);item[key+'_sha256']=sha(b)
            if key=='stdout':item['errors_and_warnings']=[l for l in b.decode('utf-8',errors='replace').splitlines() if 'error:' in l or 'warning:' in l]
        history.append(item)
assert len(targets)==len(set(targets))==28 and set(targets)==set(status['targets'])
new={'TGLV350.'+n for n in status['modules']};needed=set();visiting=set();visited=set()
def visit(n):
    assert n not in visiting,n
    if n in visited:return
    if n in new:
        raw=Path(sources[n.replace('.','/')+'.lean']['snapshot']).read_bytes()
    elif n.split('.')[0] in {'TGLV350','TGLExt','TGL'}:
        assert n in catalog,n;needed.add(n);raw=Path(catalog[n]['source']).read_bytes()
    else:return
    visiting.add(n)
    for x in imports(raw):visit(x)
    visiting.remove(n);visited.add(n)
for n in new:visit(n)
deps={}
for n in sorted(needed):
    r=catalog[n].copy();raw=Path(r['source']).read_bytes();br=Path(r['binary']).read_bytes()
    assert Path(r['binary']).resolve().is_relative_to(REV)
    assert sha(raw)==r['source_sha256'] and sha(br)==r['sha256']
    rel=Path(*n.split('.'));live=(ROOT/'kernel'/rel.with_suffix('.lean')).read_bytes()
    if live!=raw:
        assert r.get('previously_reviewed_comment_only_erratum') is True,n
        assert raw.replace(r['frozen_old_comment'].encode(),r['live_corrected_comment'].encode())==live,n
    sp=RUN/'dependency_sources'/rel.with_suffix('.lean');bp=RUN/'build'/rel.with_suffix('.olean')
    write(sp,raw);write(bp,br)
    for p in Path(r['binary']).parent.glob(Path(r['binary']).name+'.*'):
        if p.is_file():write(bp.with_name(p.name),p.read_bytes())
    deps[n]={**r,'frozen_source':str(sp),'frozen_binary':str(bp),'imports':imports(raw),'live_source_sha256':sha(live)}
cfg=load(ROOT/'environment.json');env=os.environ.copy()
package_paths=pm['lean_path'].split(os.pathsep)[1:]
assert all('.lake\\packages\\' in p for p in package_paths)
env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+package_paths)
(RUN/'tmp').mkdir(exist_ok=True);env['TMP']=env['TEMP']=str(RUN/'tmp')
assert sha(Path(cfg['lean']).read_bytes())==pm['compiler_sha256']
package_pins={}
for p in package_paths:
    pkg=Path(p).parents[3]
    for f in ['lake-manifest.json','lean-toolchain']:
        if (pkg/f).is_file():package_pins[str(pkg/f)]=sha((pkg/f).read_bytes())
manifest={'run':str(RUN),'previous_run':str(PRE),'previous_manifest_sha256':sha((PRE/'manifest.json').read_bytes()),
 'previous_compilation_sha256':sha((PRE/'compilation.json').read_bytes()),'mode':'FIVE_DEV_MODULES_AND_28_TARGET_AUDITOR_ONLY',
 'sources':sources,'dependencies':deps,'declarations':targets,'lean_path':env['LEAN_PATH'],'compiler_sha256':pm['compiler_sha256'],
 'lean_version':pm['lean_version'],'package_metadata_pins':package_pins,'custody_sha256':sha(custodyraw),
 'draft_status_sha256':sha(statusraw),'report_sha256':sha(doc),'recorder_sha256':sha(recorder),
 'initial_um_sha256':sha((ROOT/'um.py').read_bytes()),'initial_gate_sha256':sha((ROOT/'gate_extension.py').read_bytes()),
 'six_flags':{k:evidence[k] for k in custody['remaining_flags']},'memory_surface_sha256':surfaces,
 'previous_reviews':{str(p):sha(p.read_bytes()) for p in REV.glob('REVIEW_*.md')}}
save(RUN/'manifest.json',manifest);save(RUN/'author_history.json',history)
write(REV/'homogeneous_right_latest_run.txt',str(RUN).encode())
audit='\n'.join('import TGLV350.'+n for n in status['modules'])+'\n'
audit+='set_option pp.universes true\nset_option pp.width 160\n'
for n in targets:audit+='#check '+n+'\n#print axioms '+n+'\n'
write(RUN/'sources/HomogeneousRightAudit.lean',audit.encode())
print(json.dumps({'run':str(RUN),'dependencies':len(deps),'targets':len(targets),'history_attempts':len(history)}),flush=True)
records=[]
for rel in list(sources)+['HomogeneousRightAudit.lean']:
    sp=RUN/'sources'/rel;op=RUN/'build'/Path(rel).with_suffix('.olean');op.parent.mkdir(parents=True,exist_ok=True);assert not op.exists()
    cmd=[cfg['lean'],'-o',str(op),str(sp)];t=time.monotonic()
    p=subprocess.run(cmd,capture_output=True,cwd=RUN/'sources',env=env)
    out=RUN/'logs'/(Path(rel).stem+'.stdout.txt');err=RUN/'logs'/(Path(rel).stem+'.stderr.txt')
    write(out,p.stdout);write(err,p.stderr);ax=axioms(p.stdout.decode('utf-8',errors='replace'))
    expected=set(sources[rel]['declarations']) if rel in sources else set(targets)
    r={'module':rel,'command':cmd,'returncode':p.returncode,'seconds':round(time.monotonic()-t,3),'source_sha256':sha(sp.read_bytes()),
      'output_sha256':sha(op.read_bytes()) if op.exists() else None,'axioms':ax,'axioms_allowed':bool(ax) and all(set(a)<=allowed for a in ax.values()),
      'exact_targets':set(ax)==expected,'stdout':str(out),'stderr':str(err),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)}
    if rel in sources:r['binary_equals_author']=r['output_sha256']==sources[rel]['author_binary_sha256']
    records.append(r);save(RUN/'compilation.json',{'complete':False,'records':records})
    print(json.dumps({k:r[k] for k in ['module','returncode','seconds','axioms_allowed','exact_targets']}),flush=True)
    if p.returncode:print(p.stdout.decode('utf-8',errors='replace'),flush=True);break
done=len(records)==6 and all(r['returncode']==0 for r in records)
c={'complete':len(records)==6,'records':records,'all_exit_zero':done,'all_axioms_allowed':all(r['axioms_allowed'] for r in records),
 'exact_28_targets':done and set(records[-1]['axioms'])==set(targets) and all(r['exact_targets'] for r in records),
 'five_binaries_equal_author':done and all(r.get('binary_equals_author',True) for r in records),
 'sources_and_author_binaries_unchanged':all(sha(Path(s['path']).read_bytes())==s['sha256'] and sha(Path(s['author_binary']).read_bytes())==s['author_binary_sha256'] for s in sources.values()),
 'dependencies_preserved':all(sha(Path(r['frozen_source']).read_bytes())==r['source_sha256'] and sha(Path(r['frozen_binary']).read_bytes())==r['sha256'] for r in deps.values()),
 'previous_reviews_preserved':all(sha(Path(p).read_bytes())==h for p,h in manifest['previous_reviews'].items()),
 'memory_surfaces_preserved':all(sha(Path(p).read_bytes())==h for p,h in surfaces.items()),
 'recorder_unchanged':sha((ROOT/'record_homogeneous_right_memory.py').read_bytes())==manifest['recorder_sha256'],
 'package_metadata_unchanged':all(sha(Path(p).read_bytes())==h for p,h in package_pins.items()),
 'um_unchanged':sha((ROOT/'um.py').read_bytes())==manifest['initial_um_sha256'],
 'gate_unchanged':sha((ROOT/'gate_extension.py').read_bytes())==manifest['initial_gate_sha256']}
save(RUN/'compilation.json',c);print(json.dumps({k:v for k,v in c.items() if k!='records'}),flush=True)
