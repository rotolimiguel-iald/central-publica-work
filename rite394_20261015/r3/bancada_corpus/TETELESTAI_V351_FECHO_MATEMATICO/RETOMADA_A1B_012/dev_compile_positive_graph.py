from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
R=Path(__file__).resolve().parent;K=R/'k';D=R/'dev_dependencies'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
assert (R/'REAPROVEITAMENTO_A1B_GERADOR_POSITIVO.json').exists()
A=R/'dev_positive_graph'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True)
old=R/'dev_absorption/20260914_182118_370442';record=json.loads((old/'run.json').read_text(encoding='utf8'))
assert record['returncode']==0 and pin(Path(record['source']['path']))==record['source']
dest=D/'TGLExt/V351RegularFlowAbsorption.olean'
if not dest.exists():put(dest,(old/'V351RegularFlowAbsorption.olean').read_bytes())
assert dest.read_bytes()==(old/'V351RegularFlowAbsorption.olean').read_bytes()
put(A/'dependency.json',json.dumps(dict(source=record['source'],run=pin(old/'run.json'),original_object=pin(old/'V351RegularFlowAbsorption.olean'),copy=pin(dest),status='DEV_ONLY'),ensure_ascii=False,indent=2).encode('utf8'))
s=K/'TGLExt/V351RegularPositiveGraph.lean';put(A/s.name,s.read_bytes());source=pin(s)
paths=[D]+[p/'.lake/build/lib/lean' for p in sorted((K/'.lake/packages').iterdir()) if p.is_dir()]
env=os.environ.copy();env['LEAN_PATH']=';'.join(map(str,paths));env.pop('LEAN_SRC_PATH',None)
cmd=[str(BIN/'lean.exe'),'--root='+str(K),'-o',str(A/'V351RegularPositiveGraph.olean'),str(s)]
p=subprocess.run(cmd,cwd=K,env=env,capture_output=True);put(A/'stdout.txt',p.stdout);put(A/'stderr.txt',p.stderr)
assert source==pin(s)
d=dict(status='DEV_ONLY_INHERITED_OBJECTS__NOT_STANDALONE_ACCEPTANCE',returncode=p.returncode,source=source,command=cmd,cwd=str(K),lean_path=list(map(str,paths)),stdout=pin(A/'stdout.txt'),stderr=pin(A/'stderr.txt'),later_lake_required=True)
put(A/'run.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'));print(A);print(p.stdout.decode('utf8'));print(p.stderr.decode('utf8'));sys.exit(p.returncode)
