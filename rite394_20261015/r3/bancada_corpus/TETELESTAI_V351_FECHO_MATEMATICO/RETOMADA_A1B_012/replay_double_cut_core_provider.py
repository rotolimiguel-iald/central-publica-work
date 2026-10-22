from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
R=Path(__file__).resolve().parent;K=R/'k'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert p.is_relative_to(R) and not p.exists()
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
A=R/'replay_double_cut_core_provider'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True)
before={str(p):pin(p) for p in (K/'TGLExt').glob('*.lean')}
objects={str(p):pin(p) for p in (K/'.lake/build/lib/lean/TGLExt').glob('*.olean')}
env=os.environ.copy();env.pop('LEAN_PATH',None);env.pop('LEAN_SRC_PATH',None);env['PATH']=str(BIN)+os.pathsep+env['PATH']
packages=sorted(p for p in (K/'.lake/packages').iterdir() if (p/'.git').exists())
env['GIT_CONFIG_COUNT']=str(len(packages))
for i,p in enumerate(packages):
 env[f'GIT_CONFIG_KEY_{i}']='safe.directory';env[f'GIT_CONFIG_VALUE_{i}']=str(p)
cmd=[str(BIN/'lake.exe'),'build','TGLExt.V350CorePolarInclusion']
with (A/'stdout.txt').open('wb') as o,(A/'stderr.txt').open('wb') as e:
 p=subprocess.run(cmd,cwd=K,env=env,stdout=o,stderr=e)
same=all(pin(Path(p))==q for p,q in before.items())
after={str(p):pin(p) for p in (K/'.lake/build/lib/lean/TGLExt').glob('*.olean')}
changed=[v for k,v in after.items() if k not in objects or v!=objects[k]]
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),returncode=p.returncode,command=cmd,source_bytes_unchanged=same,new_or_changed_objects=changed,old_providers_not_new_theorems=True,dev_objects_used=False,stdout=pin(A/'stdout.txt'),stderr=pin(A/'stderr.txt'))
put(A/'run.json',json.dumps(d,ensure_ascii=False,indent=2).encode())
print(A);print('rc',p.returncode,'unchanged',same,'new/changed',len(changed));print((A/'stdout.txt').read_text(encoding='utf8')[-2500:]);sys.exit(p.returncode if same else 2)

