from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,time
R=Path(__file__).resolve().parent
K=R.parent/'TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
requested=sys.argv[1]
namespace,module = requested.split('.',1) if '.' in requested else ('TGLExt',requested)
assert namespace in ('TGL','TGLExt') and module.replace('_','').isalnum()
src=R/'src'/namespace/(module+'.lean')
out=R/'dev_build'/namespace/(module+'.olean')
out.parent.mkdir(parents=True,exist_ok=True)
baseline=K/'.lake/build/lib/lean'
assert not (baseline/namespace/(module+'.olean')).exists(), 'Never compile over a borrowed module'
for namespace in ('TGL','TGLExt'):
 for old in (baseline/namespace).rglob('*'):
  if old.is_file() and ('.olean' in old.name or old.suffix=='.ilean'):
   target=R/'dev_build'/old.relative_to(baseline)
   target.parent.mkdir(parents=True,exist_ok=True)
   if not target.exists(): os.link(old,target)
A=R/'attempts'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
A.mkdir(parents=True)
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert not p.exists()
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
before=pin(src)
put(A/src.name,src.read_bytes())
env=os.environ.copy()
paths=[R/'dev_build',K/'.lake/build/lib/lean']
paths += sorted(p/'.lake/build/lib/lean' for p in (K/'.lake/packages').iterdir() if (p/'.lake/build/lib/lean').is_dir())
env['LEAN_PATH']=os.pathsep.join(map(str,paths))
env.pop('LEAN_SRC_PATH',None)
cmd=[str(BIN/'lean.exe'),'--root='+str(R/'src'),'-o',str(out),str(src)]
put(A/'START.json',json.dumps(dict(command=cmd,source=before,lean=pin(BIN/'lean.exe'),
 dependency_paths=list(map(str,paths)),mode='DEV_WITH_ACCEPTED_A1_CACHE_NOT_INDEPENDENT_REVIEW'),indent=2).encode())
start=time.monotonic()
print(str(A),flush=True)
with (A/'stdout.txt').open('wb') as so,(A/'stderr.txt').open('wb') as se:
 p=subprocess.Popen(cmd,cwd=R,env=env,stdout=so,stderr=se)
 put(A/'PROCESS.json',json.dumps(dict(pid=p.pid,command=cmd)).encode())
 rc=p.wait()
same=before==pin(src)
d=dict(returncode=rc,seconds=time.monotonic()-start,source_unchanged=same,
 stdout=pin(A/'stdout.txt'),stderr=pin(A/'stderr.txt'),source=before)
if rc==0: d['object']=pin(out)
put(A/'RESULT.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps(d,ensure_ascii=False),flush=True)
print((A/'stdout.txt').read_text(encoding='utf8')[-6000:])
print((A/'stderr.txt').read_text(encoding='utf8')[-2000:])
sys.exit(rc if same else 3)
