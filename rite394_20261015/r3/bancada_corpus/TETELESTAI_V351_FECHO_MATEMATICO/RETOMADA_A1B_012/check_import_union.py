from pathlib import Path
import hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';OLD=R.parent
V350=OLD.parent/'TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel';D=R/'dev_dependencies'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
A=R/'dev_import_union';assert not A.exists();A.mkdir()
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert p.is_relative_to(R) and not p.exists();p.parent.mkdir(parents=True,exist_ok=True)
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
seen=set();rows=[]
def walk(n):
 if n in seen or not n.startswith(('TGL.','TGLExt.')):return
 seen.add(n);rel=Path(*n.split('.'));src=K/rel.with_suffix('.lean')
 for line in re.findall(r'^import (.+)$',src.read_text(encoding='utf8'),re.M):
  for x in line.split():walk(x)
 target=D/rel.with_suffix('.olean')
 if target.exists():return
 obj=OLD/'build'/rel.with_suffix('.olean');origin=OLD/'kernel'/rel.with_suffix('.lean')
 if not obj.exists():obj=V350/'.lake/build/lib/lean'/rel.with_suffix('.olean');origin=V350/rel.with_suffix('.lean')
 assert obj.exists() and src.read_bytes()==origin.read_bytes(),n
 put(target,obj.read_bytes());rows.append(dict(module=n,source=pin(src),object=pin(obj),copy=pin(target)))
for n in ['TGLExt.V350BasePolarStrongLimit','TGLExt.V350ScalarGNSGeneratorTransport']:walk(n)
put(A/'additional_dev_dependencies.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
source=A/'CheckUnion.lean'
put(source,b'import TGLExt.V351ScalarTomitaImaginaryConjugation\nimport TGLExt.V350BasePolarStrongLimit\nimport TGLExt.V350ScalarGNSGeneratorTransport\n#print axioms TGLV350.Regular.antiunitaryConjugate_add\n#print axioms TGLV350.Regular.scalarGNS_commutation_from_generators\n')
paths=[D]+[p/'.lake/build/lib/lean' for p in sorted((K/'.lake/packages').iterdir()) if p.is_dir()]
env=os.environ.copy();env['LEAN_PATH']=';'.join(map(str,paths));env.pop('LEAN_SRC_PATH',None)
cmd=[str(BIN/'lean.exe'),str(source)];p=subprocess.run(cmd,cwd=K,env=env,capture_output=True)
put(A/'stdout.txt',p.stdout);put(A/'stderr.txt',p.stderr)
put(A/'run.json',json.dumps(dict(status='DEV_IMPORT_UNION_ONLY__INHERITED_OBJECTS',command=cmd,returncode=p.returncode,source=pin(source),stdout=pin(A/'stdout.txt'),stderr=pin(A/'stderr.txt')),ensure_ascii=False,indent=2).encode('utf8'))
print(p.returncode);print(p.stdout.decode('utf8'));print(p.stderr.decode('utf8'))
