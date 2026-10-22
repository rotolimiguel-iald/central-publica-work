from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
R=Path(__file__).resolve().parent;K=R/'k';D=R/'dev_dependencies'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert p.is_relative_to(R) and not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
left=R/'dev_left/20260914_174247_734758';d=json.loads((left/'run.json').read_text(encoding='utf8'))
assert d['returncode']==0 and pin(K/'TGLExt/V351ScalarImaginaryLeftTransport.lean')==d['source']
obj=left/'V351ScalarImaginaryLeftTransport.olean';target=D/'TGLExt'/obj.name
if not target.exists():
 put(target,obj.read_bytes());put(R/'DEV_LEFT_DEPENDENCY.json',json.dumps(dict(source=d['source'],origin=pin(obj),copy=pin(target)),indent=2).encode('utf8'))
assert obj.read_bytes()==target.read_bytes()
A=R/'dev_core'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True)
s=K/'TGLExt/V351ScalarImaginaryCoreAction.lean';put(A/s.name,s.read_bytes())
paths=[D]+[p/'.lake/build/lib/lean' for p in sorted((K/'.lake/packages').iterdir()) if p.is_dir()]
env=os.environ.copy();env['LEAN_PATH']=';'.join(map(str,paths));env.pop('LEAN_SRC_PATH',None)
cmd=[str(BIN/'lean.exe'),'--root='+str(K),'-o',str(A/'V351ScalarImaginaryCoreAction.olean'),str(s)]
p=subprocess.run(cmd,cwd=K,env=env,capture_output=True)
put(A/'stdout.txt',p.stdout);put(A/'stderr.txt',p.stderr)
d=dict(status='DEV_ONLY_INHERITED_OBJECTS__NOT_STANDALONE_ACCEPTANCE',returncode=p.returncode,source=pin(s),command=cmd,cwd=str(K),lean_path=list(map(str,paths)),stdout=pin(A/'stdout.txt'),stderr=pin(A/'stderr.txt'),later_lake_required=True)
put(A/'run.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
print(str(A));print(p.stdout.decode('utf8'));print(p.stderr.decode('utf8'));sys.exit(p.returncode)
