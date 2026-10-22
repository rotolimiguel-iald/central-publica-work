"""Correct only the reviewer's printer option; do not rebuild the five modules."""
from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys,time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'homogeneous_right_latest_run.txt').read_text().strip())
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV)
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b;tmp.replace(p)
m=load(RUN/'manifest.json');c=load(RUN/'compilation.json');cfg=load(ROOT/'environment.json')
assert len(c['records'])==6 and all(r['returncode']==0 and r['binary_equals_author'] for r in c['records'][:5])
assert c['records'][-1]['returncode']==1
old_auditor=c['records'][-1]
assert 'Unknown option `pp.width`' in Path(old_auditor['stdout']).read_text(encoding='utf-8')
rel='HomogeneousRightAuditFinal.lean';sp=RUN/'sources'/rel;op=RUN/'build'/Path(rel).with_suffix('.olean')
audit='\n'.join('import '+p[:-5].replace('/','.') for p in m['sources'])+'\n'
for n in m['declarations']:audit+='set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n'
write(sp,audit.encode('utf-8'));assert not op.exists()
env=os.environ.copy();env['LEAN_PATH']=m['lean_path'];env['TMP']=env['TEMP']=str(RUN/'tmp')
cmd=[cfg['lean'],'-o',str(op),str(sp)];t=time.monotonic()
p=subprocess.run(cmd,capture_output=True,cwd=RUN/'sources',env=env)
out=RUN/'logs/HomogeneousRightAuditFinal.stdout.txt';err=RUN/'logs/HomogeneousRightAuditFinal.stderr.txt'
write(out,p.stdout);write(err,p.stderr)
ax={n:[a.strip() for a in v.split(',') if a.strip()] for n,v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",p.stdout.decode('utf-8'),re.S)}
allowed={'propext','Classical.choice','Quot.sound'}
r={'module':rel,'command':cmd,'returncode':p.returncode,'seconds':round(time.monotonic()-t,3),'source_sha256':sha(sp.read_bytes()),
 'output_sha256':sha(op.read_bytes()) if op.exists() else None,'axioms':ax,
 'axioms_allowed':bool(ax) and all(set(v)==allowed for v in ax.values()),'exact_targets':set(ax)==set(m['declarations']),
 'stdout':str(out),'stderr':str(err),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)}
c['excluded_auditor_attempts']=[{**old_auditor,'reason':'REVIEWER_UNKNOWN_PRINTER_OPTION_pp.width; universe-qualified axiom names not normalized in initial parser'}]
c['records']=c['records'][:5]+[r]
c['all_exit_zero']=p.returncode==0
c['all_axioms_allowed']=all(x['axioms_allowed'] for x in c['records'])
c['exact_28_targets']=p.returncode==0 and r['exact_targets']
c['five_binaries_equal_author']=all(x['binary_equals_author'] for x in c['records'][:5])
c['sources_and_author_binaries_unchanged']=all(sha(Path(s['path']).read_bytes())==s['sha256'] and sha(Path(s['author_binary']).read_bytes())==s['author_binary_sha256'] for s in m['sources'].values())
c['dependencies_preserved']=all(sha(Path(x['frozen_source']).read_bytes())==x['source_sha256'] and sha(Path(x['frozen_binary']).read_bytes())==x['sha256'] for x in m['dependencies'].values())
c['auditor_only_retry']=True
write(RUN/'compilation.json',json.dumps(c,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps({k:v for k,v in r.items() if k not in ['axioms','command']},ensure_ascii=False))
if p.returncode:print(p.stdout.decode('utf-8'))
