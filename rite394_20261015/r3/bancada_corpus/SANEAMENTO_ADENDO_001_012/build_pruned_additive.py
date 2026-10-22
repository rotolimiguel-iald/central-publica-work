from support import *
import subprocess,time,sys
K=ROOT/'kernel';D=ROOT/'direct_builds'/stamp();D.mkdir(parents=True)
m='TGLExt.SectorFriedmannAdditive';p=K/'TGLExt/SectorFriedmannAdditive.lean';before=digest(p);atomic(D/p.name,p.read_bytes());out=D/'objects'/p.stem;out.parent.mkdir()
cmd=[str(BIN/'lake.exe'),'env','lean','--root='+str(K),str(p),'-o',str(out.with_suffix('.olean')),'-i',str(out.with_suffix('.ilean')),'-c',str(out.with_suffix('.c'))]
record(D/'started.json',dict(command=cmd,cwd=str(K),source_sha256=before,started=stamp()))
t=time.monotonic();r=subprocess.run(cmd,cwd=K,env=clean_env(),capture_output=True);atomic(D/'stdout.txt',r.stdout);atomic(D/'stderr.txt',r.stderr)
artifacts=[]
if r.returncode==0:
 for a in out.parent.glob(p.stem+'.*'):
  dst=K/('.lake/build/ir/TGLExt' if a.suffix=='.c' else '.lake/build/lib/lean/TGLExt')/a.name;atomic(dst,a.read_bytes());artifacts.append(dict(path=str(dst),sha256=digest(dst),bytes=dst.stat().st_size))
row=dict(module=m,command=cmd,cwd=str(K),returncode=r.returncode,seconds=time.monotonic()-t,source_sha256=before,source_unchanged=before==digest(p),artifacts=artifacts,stdout=str(D/'stdout.txt'),stdout_sha256=digest(D/'stdout.txt'),stderr=str(D/'stderr.txt'),stderr_sha256=digest(D/'stderr.txt'))
record(D/'run.json',row)
if r.returncode==0 and row['source_unchanged']:
 prev=json.loads((ROOT/'BUILD_ATUAL.json').read_text(encoding='utf-8'));old=json.loads(Path(prev['report']).read_text(encoding='utf-8'))
 runs=[row if x['module']==m else x for x in old['runs']]
 for x in runs:
  assert digest(K/Path(*x['module'].split('.')).with_suffix('.lean'))==x['source_sha256']
  for a in x['artifacts']:assert digest(Path(a['path']))==a['sha256']
 report=D/'BUILD_FINAL.json';record(report,dict(status='PASS',targets=old['targets'],runs=runs,preceding_report=prev['report'],changed_module=m,coverage='28 fontes atuais cobertos: 27 execucoes anteriores preservadas e validas, uma recompilacao apos poda; auditoria comum separada porque tambem mudou.'))
 record(ROOT/'BUILD_ATUAL.json',dict(directory=str(D),report=str(report),ok=True,passed=len(runs),expected=len(runs)))
print('PRUNED ADDITIVE',r.returncode)
if r.returncode:print((r.stdout+r.stderr).decode('utf-8',errors='replace'))
sys.exit(r.returncode)
