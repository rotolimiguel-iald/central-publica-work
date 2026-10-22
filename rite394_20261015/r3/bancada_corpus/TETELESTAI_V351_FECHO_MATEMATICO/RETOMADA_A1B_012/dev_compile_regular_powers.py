from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
R=Path(__file__).resolve().parent;K=R/'k';D=R/'dev_dependencies'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
assert (R/'REAPROVEITAMENTO_A1B_POTENCIAS_REGULARES.json').exists()
A=R/'dev_regular_powers'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True)
deps=[]
for folder,mod in [('dev_multiplier_calculus/20260914_192424_032053','V351ScalarMultiplierCalculus'),('dev_spectral_graph/20260914_191213_503075','V351RegularSpectralGraph'),('dev_fourier_translation/20260914_183403_872821','V351FourierTranslation')]:
    old=R/folder;record=json.loads((old/'run.json').read_text(encoding='utf8'))
    assert record['returncode']==0 and pin(Path(record['source']['path']))==record['source']
    dest=D/'TGLExt'/f'{mod}.olean'
    if not dest.exists():put(dest,(old/f'{mod}.olean').read_bytes())
    assert dest.read_bytes()==(old/f'{mod}.olean').read_bytes()
    deps.append(dict(source=record['source'],run=pin(old/'run.json'),original_object=pin(old/f'{mod}.olean'),copy=pin(dest),status='DEV_ONLY'))
put(A/'dependencies.json',json.dumps(deps,ensure_ascii=False,indent=2).encode('utf8'))
s=K/'TGLExt/V351RegularImaginaryPowers.lean';put(A/s.name,s.read_bytes());source=pin(s)
paths=[D]+[p/'.lake/build/lib/lean' for p in sorted((K/'.lake/packages').iterdir()) if p.is_dir()]
env=os.environ.copy();env['LEAN_PATH']=';'.join(map(str,paths));env.pop('LEAN_SRC_PATH',None)
cmd=[str(BIN/'lean.exe'),'--root='+str(K),'-o',str(A/'V351RegularImaginaryPowers.olean'),str(s)]
p=subprocess.run(cmd,cwd=K,env=env,capture_output=True);put(A/'stdout.txt',p.stdout);put(A/'stderr.txt',p.stderr)
assert source==pin(s)
d=dict(status='DEV_ONLY_INHERITED_OBJECTS__NOT_STANDALONE_ACCEPTANCE',returncode=p.returncode,source=source,command=cmd,cwd=str(K),lean_path=list(map(str,paths)),stdout=pin(A/'stdout.txt'),stderr=pin(A/'stderr.txt'),later_lake_required=True)
put(A/'run.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'));print(A);print(p.stdout.decode('utf8'));print(p.stderr.decode('utf8'));sys.exit(p.returncode)
