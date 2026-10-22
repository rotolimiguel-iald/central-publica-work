"""Standalone Lake build with immutable per-attempt source snapshots and logs."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
R=Path(__file__).resolve().parent
K=R/'kernel'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
A=R/'attempts'/stamp; A.mkdir(parents=True)
targets=sys.argv[1:] or ['TGLExt.TheSameBetaReadsThreeFaces','TGLExt.AuditSameBeta']
snapshots=[]
for target in targets:
    source=K/Path(*target.split('.')).with_suffix('.lean')
    if source.exists():
        b=source.read_bytes(); (A/source.name).write_bytes(b)
        snapshots.append(dict(path=str(source),sha256=hashlib.sha256(b).hexdigest()))
env=os.environ.copy()
env.pop('LEAN_PATH',None); env.pop('LEAN_SRC_PATH',None)
env['PATH']=str(BIN)+os.pathsep+env['PATH']
cmd=[str(BIN/'lake.exe'),'build',*targets]
print(str(A),flush=True)
with (A/'stdout.txt').open('wb') as out, (A/'stderr.txt').open('wb') as err:
    p=subprocess.Popen(cmd,cwd=K,env=env,stdout=out,stderr=err)
    (A/'process.json').write_text(json.dumps(dict(pid=p.pid,command=cmd,cwd=str(K)),indent=2),encoding='utf8')
    rc=p.wait()
record=dict(command=cmd,cwd=str(K),returncode=rc,snapshots=snapshots,
    lean_path_removed=True,package_tree=str(K/'.lake/packages'),
    lean_version=subprocess.check_output([str(BIN/'lean.exe'),'--version']).decode().strip())
(A/'run.json').write_text(json.dumps(record,indent=2),encoding='utf8')
print('EXIT',rc,flush=True)
for f in ['stdout.txt','stderr.txt']:
    text=(A/f).read_text(encoding='utf8',errors='replace')
    print(text[-16000:])
sys.exit(rc)
