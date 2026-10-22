"""B2 runner: snapshot every new B2 source, preserving the sealed B1 runner."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
R=Path(__file__).resolve().parent
K=R/'kernel'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
A=R/'attempts'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
A.mkdir(parents=True)
def save(path, value):
    data=json.dumps(value,ensure_ascii=False,indent=2).encode('utf8')
    tmp=path.with_name(path.name+'.tmp');tmp.write_bytes(data)
    assert tmp.read_bytes()==data;os.replace(tmp,path)
sources=[]
for source in sorted((K/'TGLExt').glob('*FLRW*.lean')):
    data=source.read_bytes();target=A/source.name
    target.write_bytes(data);assert target.read_bytes()==data
    sources.append(dict(path=str(source),snapshot=str(target),sha256=hashlib.sha256(data).hexdigest()))
save(A/'sources.json',sources)
targets=sys.argv[1:] or ['TGLExt.FLRWFieldEquations']
env=os.environ.copy()
env.pop('LEAN_PATH',None);env.pop('LEAN_SRC_PATH',None)
env['PATH']=str(BIN)+os.pathsep+env['PATH']
cmd=[str(BIN/'lake.exe'),'build',*targets]
print(str(A),flush=True)
with (A/'stdout.txt').open('wb') as out,(A/'stderr.txt').open('wb') as err:
    proc=subprocess.Popen(cmd,cwd=K,env=env,stdout=out,stderr=err)
    save(A/'process.json',dict(pid=proc.pid,command=cmd,cwd=str(K)))
    rc=proc.wait()
same=all(hashlib.sha256(Path(s['path']).read_bytes()).hexdigest()==s['sha256'] for s in sources)
save(A/'run.json',dict(returncode=rc,command=cmd,cwd=str(K),snapshots=sources,
    sources_unchanged_during_build=same,lean_path_removed=True,
    lean_version=subprocess.check_output([str(BIN/'lean.exe'),'--version']).decode().strip()))
print('EXIT',rc,'SOURCES_UNCHANGED',same,flush=True)
log=(A/'stdout.txt').read_text(encoding='utf8',errors='replace')
first=log.find('error: TGLExt/FLRW')
if first<0:first=log.find('error: TGLExt/AuditFLRW')
if first>=0:print(log[first:first+18000])
else:print('\n'.join(line for line in log.splitlines() if 'FLRW' in line or 'Build completed' in line)[-8000:])
print((A/'stderr.txt').read_text(encoding='utf8',errors='replace')[-1000:])
sys.exit(rc if same else 2)
