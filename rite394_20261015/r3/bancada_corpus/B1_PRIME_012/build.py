from support import *
import subprocess,sys,time
sys.stdout.reconfigure(encoding="utf-8")
K=ROOT/"kernel"
A=ROOT/"attempts"/stamp(); A.mkdir(parents=True)
targets=sys.argv[1:] or ["TGLExt.TheSameBetaReadsFourFaces","TGLExt.AuditSameBetaFourFaces"]
snaps=[]
for target in targets:
    p=K/Path(*target.split(".")).with_suffix(".lean")
    if p.exists():
        atomic(A/p.name,p.read_bytes());snaps.append(dict(path=str(p),sha256=digest(p)))
cmd=[str(BIN/"lake.exe"),"build",*targets]
record(A/"started.json",dict(command=cmd,cwd=str(K),source_snapshots=snaps,started_utc=stamp()))
print(str(A),flush=True)
t=time.monotonic()
p=subprocess.run(cmd,cwd=K,env=clean_env(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
atomic(A/"stdout.txt",p.stdout); atomic(A/"stderr.txt",p.stderr)
record(A/"run.json",dict(command=cmd,cwd=str(K),returncode=p.returncode,seconds=time.monotonic()-t,source_snapshots=snaps,lean_version=subprocess.check_output([str(BIN/"lean.exe"),"--version"]).decode().strip(),finished_utc=stamp()))
print("Raw stdout/stderr saved; EXIT",p.returncode,flush=True)
if p.returncode: print("\n".join(line for line in p.stdout.decode("utf-8",errors="replace").splitlines() if line.startswith("error:")))
sys.exit(p.returncode)
