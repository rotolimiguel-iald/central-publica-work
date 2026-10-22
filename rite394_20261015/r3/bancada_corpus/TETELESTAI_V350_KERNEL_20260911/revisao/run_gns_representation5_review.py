"""Compile the final fifth module and cumulative auditor against the reviewer's frozen four-module tree."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
REVIEW=Path(__file__).resolve().parent
ROOT=REVIEW.parent
PREVIOUS=Path((REVIEW/'gns_representation4_latest_run.txt').read_text(encoding='utf-8'))
RUN=REVIEW/('gns_representation5_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b:hashlib.sha256(b).hexdigest()
ALLOWED={'propext','Classical.choice','Quot.sound'}
def write(p,b):
    assert p.resolve().is_relative_to(REVIEW)
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bak=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bak.open('xb') as f:f.write(old)
        assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b
    tmp.replace(p)
def save(p,o):write(p,json.dumps(o,ensure_ascii=False,indent=2).encode('utf-8'))
pm=json.loads((PREVIOUS/'manifest.json').read_bytes());pc=json.loads((PREVIOUS/'compilation.json').read_bytes())
assert all(pc[k] for k in ['complete','all_exit_zero','full_audit_names_exact','all_axioms_allowed','sources_unchanged','dependencies_unchanged','previous_reviews_preserved'])
statusraw=(ROOT/'gns_representation_draft_status.json').read_bytes();status=json.loads(statusraw)
write(RUN/'author_gns_representation_draft_status.json',statusraw)
sources=dict(pm['sources']);pins={}
for n,r in pm['dependencies'].items():
    for p,h in [(r['frozen_source'],r['source_sha256']),(r['frozen_binary'],r['sha256'])]:pins[p]=h
for rel,r in sources.items():
    c=next(c for c in pc['records'] if c['module']==rel)
    pins[r['snapshot']]=r['sha256']
    pins[str(PREVIOUS/'build'/Path(rel).with_suffix('.olean'))]=c['output_sha256']
    assert sha(Path(r['path']).read_bytes())==r['sha256']==status['records'][Path(rel).stem]['sha256']
for p,h in pins.items():assert sha(Path(p).read_bytes())==h,p
name='ScalarGNSRepresentation';rel='TGLV350/'+name+'.lean'
record=status['records'][name];src=Path(record['source']);raw=src.read_bytes()
log=Path(record['log']);author=json.loads(log.read_bytes())
assert sha(raw)==record['sha256']==author['sha256']
assert author['returncode']==0 and author['source_unchanged_during_compile'] is True
assert sha((ROOT/'build'/Path(rel).with_suffix('.olean')).read_bytes())==record['output_sha256']==author['output_sha256']
write(RUN/'sources'/rel,raw)
for p in [log,Path(author['stdout']),Path(author['stderr'])]:write(RUN/'author_logs'/p.name,p.read_bytes())
txt=raw.decode('utf-8').replace('\r\n','\n');ns=re.findall(r'^namespace\s+([\w.]+)$',txt,re.M)
assert len(ns)==1
decls=[ns[0]+'.'+n for n in re.findall(r'^#print axioms ([\w.]+)$',txt,re.M)]
named=[ns[0]+'.'+n for n in re.findall(r'^(?:noncomputable\s+)?(?:def|theorem|abbrev|structure|instance)\s+([\w.]+)',txt,re.M)]
assert len(decls)==4 and set(decls)==set(named)
imports=re.findall(r'^import\s+([\w.]+)',txt,re.M)
assert all(n.replace('.','/')+'.lean' in sources for n in imports)
sources[rel]={'path':str(src),'snapshot':str(RUN/'sources'/rel),'sha256':sha(raw),'lines':len(txt.splitlines()),'imports':imports,'namespace':ns[0],'declarations':decls,'all_named_declarations':named,'author_log':str(log),'author_binary_sha256':author['output_sha256']}
targets=pm['declarations']+decls;allnamed=pm['all_named_declarations']+named
assert len(targets)==21 and len(allnamed)==22
prior_orbit=Path((REVIEW/'gns_orbit_latest_run.txt').read_text(encoding='utf-8'))
om=json.loads((prior_orbit/'manifest.json').read_bytes())
assert set(targets+om['declarations'])==set(status['targets']) and len(status['targets'])==35
for r in om['sources'].values():assert sha(Path(r['path']).read_bytes())==r['sha256']==status['records'][Path(r['path']).stem]['sha256']
environment=json.loads((ROOT/'environment.json').read_bytes());env=os.environ.copy()
env['LEAN_PATH']=os.pathsep.join([str(RUN/'build'),str(PREVIOUS/'build')]+environment['lean_path'][2:])
(RUN/'tmp').mkdir();env['TMP']=env['TEMP']=str(RUN/'tmp')
assert not any(Path(p).resolve() in [ROOT/'build',ROOT/'kernel/.lake/build/lib/lean'] for p in env['LEAN_PATH'].split(os.pathsep))
version=subprocess.run([environment['lean'],'--version'],env=env,cwd=RUN,capture_output=True)
assert version.returncode==0
docs={}
for n in ['MINUTA_REPRESENTACAO_GNS.md','record_gns_representation_progress.py','verify_gns_representation_custody.py']:
    p=ROOT/n
    if p.exists():write(RUN/'documents'/n,p.read_bytes());docs[n]=sha(p.read_bytes())
manifest={'run':str(RUN),'previous_run':str(PREVIOUS),'prior_orbit_run':str(prior_orbit),'mode':'INDEPENDENT_FIFTH_MODULE_AND_CUMULATIVE_21_TARGET_AUDIT','sources':sources,'declarations':targets,'all_named_declarations':allnamed,'inherited_dependency_count':len(pm['dependencies']),'inherited_project_module_count':len(pm['dependencies'])+4,'dependency_manifest':str(PREVIOUS/'manifest.json'),'frozen_dependency_pins':pins,'lean_path':env['LEAN_PATH'],'lean_version':version.stdout.decode('utf-8').strip(),'compiler_sha256':sha(Path(environment['lean']).read_bytes()),'draft_status_sha256':sha(statusraw),'documents':docs,'previous_reviews':{str(p):sha(p.read_bytes()) for p in REVIEW.glob('REVIEW_*.md')}}
save(RUN/'manifest.json',manifest);write(REVIEW/'gns_representation_latest_run.txt',str(RUN).encode('utf-8'))
audit='\n'.join('import '+r[:-5].replace('/','.') for r in sources)+'\n'
for n in allnamed:
    audit+='set_option pp.universes true in\n#check '+n+'\n'
    if n in targets:audit+='#print axioms '+n+'\n'
write(RUN/'sources/GNSRepresentationFullAudit.lean',audit.encode('utf-8'))
print(json.dumps({'run':str(RUN),'reused_project_modules':len(pm['dependencies'])+4,'new_modules':1,'cumulative_targets':len(targets),'named_types':len(allnamed)}),flush=True)
records=[]
for rel in ['TGLV350/ScalarGNSRepresentation.lean','GNSRepresentationFullAudit.lean']:
    src=RUN/'sources'/rel;out=RUN/'build'/Path(rel).with_suffix('.olean');out.parent.mkdir(parents=True,exist_ok=True)
    assert not out.exists()
    cmd=[environment['lean'],'-o',str(out),str(src)];t=time.monotonic()
    proc=subprocess.run(cmd,env=env,cwd=RUN/'sources',capture_output=True)
    text=proc.stdout.decode('utf-8',errors='replace')
    ax={n:[a.strip() for a in b.split(',') if a.strip()] for n,b in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",text,re.S)}
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",text):ax.setdefault(n,[])
    stdout=RUN/'logs'/(Path(rel).stem+'.stdout.txt');stderr=RUN/'logs'/(Path(rel).stem+'.stderr.txt')
    write(stdout,proc.stdout);write(stderr,proc.stderr)
    result={'module':rel,'command':cmd,'returncode':proc.returncode,'seconds':round(time.monotonic()-t,3),'source_sha256':sha(src.read_bytes()),'output_sha256':sha(out.read_bytes()) if out.exists() else None,'axioms':ax,'axioms_allowed':bool(ax) and all(set(v)<=ALLOWED for v in ax.values()),'stdout':str(stdout),'stderr':str(stderr)}
    records.append(result);save(RUN/'compilation.json',{'complete':False,'records':records})
    print(json.dumps({k:result[k] for k in ['module','returncode','seconds','axioms_allowed']}),flush=True)
    if proc.returncode:print(text,flush=True);break
summary={'records':records,'complete':len(records)==2,'all_exit_zero':len(records)==2 and all(r['returncode']==0 for r in records),'full_audit_names_exact':len(records)==2 and set(records[-1]['axioms'])==set(targets),'all_axioms_allowed':all(r['axioms_allowed'] for r in records),'sources_unchanged':all(sha(Path(r['path']).read_bytes())==r['sha256'] for r in sources.values()),'dependencies_unchanged':all(sha(Path(p).read_bytes())==h for p,h in pins.items()),'previous_reviews_preserved':all(sha(Path(p).read_bytes())==h for p,h in manifest['previous_reviews'].items())}
save(RUN/'compilation.json',summary);print(json.dumps({k:v for k,v in summary.items() if k!='records'}),flush=True)
