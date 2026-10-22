from support import *
import subprocess,sys,time,re
K=ROOT/'k'
module=sys.argv[1]
src=K/Path(*module.split('.')).with_suffix('.lean')
assert src.is_file()
run=ROOT/'attempts'/stamp();run.mkdir(parents=True)
atomic(run/src.name,src.read_bytes())
env=clean_env()
paths=[K/'.lake/build/lib/lean']+sorted(p/'.lake/build/lib/lean' for p in (K/'.lake/packages').iterdir() if (p/'.lake/build/lib/lean').is_dir())
env['LEAN_PATH']=os.pathsep.join(map(str,paths))
imports=[]
for name in re.findall(r'^import ([A-Za-z0-9_.]+)',src.read_text(encoding='utf8'),re.M):
 rel=Path(*name.split('.')).with_suffix('.olean')
 found=next((folder/rel for folder in paths if (folder/rel).is_file()),None)
 if found:
  for candidate in found.parent.glob(found.name+'*'):
   if candidate.suffix!='.hash': imports.append(dict(path=str(candidate),sha256=digest(candidate)))
record(run/'IMPORTS_BEFORE.json',imports)
out=run/(src.stem+'.olean')
cmd=[str(BIN/'lean.exe'),'--root='+str(K),'-o',str(out),str(src)]
record(run/'START.json',dict(command=cmd,source=str(src),sha256=digest(src),lean_sha256=digest(BIN/'lean.exe'),dependency_paths=list(map(str,paths))))
t=time.monotonic();p=subprocess.run(cmd,cwd=K,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
atomic(run/'stdout.txt',p.stdout);atomic(run/'stderr.txt',p.stderr)
outputs=[]
imports_unchanged=all(digest(Path(i['path']))==i['sha256'] for i in imports)
source_unchanged=src.read_bytes()==(run/src.name).read_bytes()
if p.returncode==0 and imports_unchanged and source_unchanged:
 for obj in run.glob(src.stem+'.olean*'):
  dst=K/'.lake/build/lib/lean'/Path(*module.split('.')).parent/obj.name
  atomic(dst,obj.read_bytes());outputs.append(dict(path=str(dst),sha256=digest(dst)))
record(run/'RESULT.json',dict(module=module,returncode=p.returncode,seconds=time.monotonic()-t,source_sha256=digest(src),source_unchanged=source_unchanged,imports_unchanged=imports_unchanged,outputs=outputs))
print(str(run));print(p.stdout.decode('utf8'));print(p.stderr.decode('utf8'));sys.exit(p.returncode if source_unchanged and imports_unchanged else 3)
