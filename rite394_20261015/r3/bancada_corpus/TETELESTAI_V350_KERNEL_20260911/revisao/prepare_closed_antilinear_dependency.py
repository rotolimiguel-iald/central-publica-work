"""Compile the existing generic dependency in an independent project tree."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
REVIEW=Path(__file__).resolve().parent;ROOT=REVIEW.parent
RUN=REVIEW/('closed_antilinear_dependency_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b):
    assert p.resolve().is_relative_to(REVIEW) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
def save(p,o):write(p,json.dumps(o,ensure_ascii=False,indent=2).encode('utf-8'))
rel='TGLExt/ClosedAntilinearStandardSubspace.lean';src=ROOT/'kernel'/rel
snapshot=RUN/'sources'/rel;raw=src.read_bytes();write(snapshot,raw)
envdata=json.loads((ROOT/'environment.json').read_bytes());env=os.environ.copy()
env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+envdata['lean_path'][2:])
(RUN/'tmp').mkdir();env['TMP']=env['TEMP']=str(RUN/'tmp')
out=RUN/'build'/Path(rel).with_suffix('.olean');out.parent.mkdir(parents=True)
version=subprocess.run([envdata['lean'],'--version'],env=env,cwd=RUN,capture_output=True);assert version.returncode==0
m={'run':str(RUN),'mode':'INDEPENDENT_RECOMPILE_EXISTING_GENERIC_DEPENDENCY','dependencies':{},
   'sources':{rel:{'path':str(src),'snapshot':str(snapshot),'sha256':sha(src)}},
   'compiler_sha256':sha(Path(envdata['lean'])),'lean_version':version.stdout.decode().strip(),
   'lean_path':env['LEAN_PATH'],'project_author_build_excluded':True}
save(RUN/'manifest.json',m)
command=[envdata['lean'],'-o',str(out),str(snapshot)];t=time.monotonic()
p=subprocess.run(command,env=env,cwd=RUN/'sources',capture_output=True)
stdout=RUN/'logs/ClosedAntilinearStandardSubspace.stdout.txt';stderr=RUN/'logs/ClosedAntilinearStandardSubspace.stderr.txt'
write(stdout,p.stdout);write(stderr,p.stderr)
txt=p.stdout.decode('utf-8',errors='replace')
ax={n:[x.strip() for x in body.split(',') if x.strip()] for n,body in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",txt,re.S)}
allowed=bool(ax) and all(set(x)<={'propext','Classical.choice','Quot.sound'} for x in ax.values())
record={'module':rel,'command':command,'returncode':p.returncode,'seconds':round(time.monotonic()-t,3),
        'source_sha256':sha(snapshot),'output_sha256':sha(out) if out.exists() else None,
        'axioms':ax,'axioms_allowed':allowed,'stdout':str(stdout),'stderr':str(stderr)}
c={'complete':True,'all_exit_zero':p.returncode==0,'all_axioms_allowed':allowed,
   'source_unchanged':sha(src)==sha(snapshot),'records':[record]}
save(RUN/'compilation.json',c)
assert p.returncode==0 and allowed and c['source_unchanged'],txt
pointer=REVIEW/'closed_antilinear_dependency_latest_run.txt';write(pointer,str(RUN).encode('utf-8'))
print(json.dumps({'run':str(RUN),'rc':p.returncode,'source_sha256':sha(snapshot),'olean_sha256':sha(out),
                  'axiom_targets':len(ax),'all_axioms_allowed':allowed,'seconds':record['seconds']},ensure_ascii=False),flush=True)
