from support import *
import subprocess,time,sys
sys.stdout.reconfigure(encoding='utf-8')
K=ROOT/'kernel';D=ROOT/'direct_builds'/stamp();D.mkdir(parents=True)
g=json.loads((ROOT/'GRAFO_REBUILD.json').read_text(encoding='utf-8'))
# Restore the local pre-experiment B6 cache; their fresh outputs get separate destinations.
restored=[]
for row in json.loads((ROOT/'QUARENTENA_OBJETOS.json').read_text(encoding='utf-8')):
 p=Path(row['original'])
 if p.name.split('.')[0] in ['MixedLadder','SecondCone','AreaScale']:
  b=Path(row['quarantine']).read_bytes();assert digest(Path(row['quarantine']))==row['sha256'];atomic(p,b);restored.append(row)
record(D/'RESTAURO_CACHE_LOCAL_B6.json',restored)
needed=set()
def add(m):
 if m in needed:return
 for q in g['imports_after'][m]:add(q)
 needed.add(m)
for m in g['targets']:add(m)
ordered=[];done=set()
def visit(m):
 if m in done:return
 for q in g['imports_after'][m]:visit(q)
 done.add(m);ordered.append(m)
for m in sorted(needed):visit(m)
obj=lambda m: K/'.lake/build/lib/lean'/Path(*m.split('.')).with_suffix('.olean')
targets=[m for m in ordered if m in g['targets'] or not obj(m).exists()]
record(D/'PLANO.json',dict(targets=targets,forced_reverse_closure=g['targets'],additional_missing=[m for m in targets if m not in g['targets']],cached_ancestors=[dict(module=m,path=str(obj(m)),sha256=digest(obj(m))) for m in ordered if m not in targets],lean_version=subprocess.check_output([str(BIN/'lean.exe'),'--version']).decode().strip()))
print('DIRECT TARGETS',len(targets),flush=True)
rows=[]
for index,m in enumerate(targets):
 p=K/Path(*m.split('.')).with_suffix('.lean');before=digest(p)
 moddir=D/m;moddir.mkdir()
 atomic(moddir/p.name,p.read_bytes());out=moddir/'objects'/p.stem;out.parent.mkdir()
 cmd=[str(BIN/'lake.exe'),'env','lean','--root='+str(K),str(p),'-o',str(out.with_suffix('.olean')),'-i',str(out.with_suffix('.ilean')),'-c',str(out.with_suffix('.c'))]
 record(moddir/'started.json',dict(command=cmd,cwd=str(K),source_sha256=before,started=stamp()))
 t=time.monotonic();r=subprocess.run(cmd,cwd=K,env=clean_env(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 atomic(moddir/'stdout.txt',r.stdout);atomic(moddir/'stderr.txt',r.stderr)
 artifacts=[]
 if r.returncode==0:
  for art in sorted(out.parent.glob(p.stem+'.*')):
   dest=K/('.lake/build/ir' if art.suffix=='.c' else '.lake/build/lib/lean')/Path(*m.split('.')[:-1])/art.name
   atomic(dest,art.read_bytes());artifacts.append(dict(path=str(dest),sha256=digest(dest),bytes=dest.stat().st_size))
 row=dict(module=m,command=cmd,cwd=str(K),returncode=r.returncode,seconds=time.monotonic()-t,source_sha256=before,source_unchanged=digest(p)==before,artifacts=artifacts,stdout=str(moddir/'stdout.txt'),stdout_sha256=digest(moddir/'stdout.txt'),stderr=str(moddir/'stderr.txt'),stderr_sha256=digest(moddir/'stderr.txt'))
 record(moddir/'run.json',row);rows.append(row)
 print(f'{index+1}/{len(targets)} {m} rc={r.returncode} ({row["seconds"]:.1f}s)',flush=True)
 if r.returncode or digest(p)!=before:
  print((r.stdout+r.stderr).decode('utf-8',errors='replace'),flush=True);break
ok=len(rows)==len(targets) and all(r['returncode']==0 and r['source_unchanged'] for r in rows)
record(D/'BUILD.json',dict(status='PASS' if ok else 'FAIL',targets=targets,runs=rows,coverage='Fecho reverso b/d/f completo + dependencias locais sem objeto; pacotes e demais fornecedores via cache isolado, nao reconstruidos integralmente.'))
record(ROOT/'BUILD_ATUAL.json',dict(directory=str(D),report=str(D/'BUILD.json'),ok=ok,passed=sum(r['returncode']==0 for r in rows),expected=len(targets)))
sys.exit(0 if ok else 1)
