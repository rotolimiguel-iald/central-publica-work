from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
R=Path(__file__).resolve().parent;K=R/'k'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_bytes(b)
    assert q.read_bytes()==b;os.replace(q,p)
def load(p):return json.loads(p.read_text(encoding='utf8'))
assert (R/'CACHE_PROVENIENCIA.json').exists()
records=load(R/'FONTES_REPLAY.json')
for p in records:
    assert pin(Path(p['original']['path']))==p['original']
    assert pin(Path(p['copy']['path']))==p['copy']
A=R/'attempts'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True)
targets=sys.argv[1:] or ['TGLExt.AuditA1Orphans']
env=os.environ.copy();env.pop('LEAN_PATH',None);env.pop('LEAN_SRC_PATH',None)
env['PATH']=str(BIN)+os.pathsep+env['PATH']
packages=sorted(p for p in (K/'.lake/packages').iterdir() if (p/'.git').exists())
env['GIT_CONFIG_COUNT']=str(len(packages))
for i,p in enumerate(packages):env[f'GIT_CONFIG_KEY_{i}']='safe.directory';env[f'GIT_CONFIG_VALUE_{i}']=str(p)
cmd=[str(BIN/'lake.exe'),'build',*targets]
sources=[pin(p) for p in (K/'TGLExt').glob('*.lean') if p.name.startswith('V351') or p.name=='AuditA1Orphans.lean']
put(A/'sources.json',json.dumps(sources,ensure_ascii=False,indent=2).encode('utf8'))
print(str(A),flush=True)
with (A/'stdout.txt').open('wb') as out,(A/'stderr.txt').open('wb') as err:
    proc=subprocess.Popen(cmd,cwd=K,env=env,stdout=out,stderr=err)
    put(A/'process.json',json.dumps(dict(pid=proc.pid,command=cmd,cwd=str(K)),ensure_ascii=False,indent=2).encode('utf8'))
    rc=proc.wait()
same=all(pin(Path(p['path']))==p for p in sources)
data=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),returncode=rc,command=cmd,cwd=str(K),sources=sources,
    sources_unchanged_during_build=same,lean_path_removed=True,external_package_cache_inherited=True,project_objects_inherited=False,
    lean_version=subprocess.check_output([str(BIN/'lean.exe'),'--version']).decode().strip(),stdout=pin(A/'stdout.txt'),stderr=pin(A/'stderr.txt'))
put(A/'run.json',json.dumps(data,ensure_ascii=False,indent=2).encode('utf8'))
print('EXIT',rc,'UNCHANGED',same,flush=True)
text=(A/'stdout.txt').read_text(encoding='utf8',errors='replace')
errors=[i for i,l in enumerate(text.splitlines()) if l.startswith('error:')]
if errors:print('\n'.join(text.splitlines()[errors[0]:errors[0]+90]))
else:print('\n'.join(text.splitlines()[-8:]))
sys.exit(rc if same else 2)
