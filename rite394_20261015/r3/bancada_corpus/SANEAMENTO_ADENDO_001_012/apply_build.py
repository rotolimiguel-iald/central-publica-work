from support import *
import re, collections, subprocess, time, sys
sys.stdout.reconfigure(encoding='utf-8')
K=ROOT/'kernel'
paths={'.'.join(p.relative_to(K).with_suffix('').parts):p for p in list((K/'TGL').rglob('*.lean'))+list((K/'TGLExt').rglob('*.lean'))+list(K.glob('*.lean'))}
def graph():
 return {m:[i for line in p.read_text(encoding='utf-8-sig').splitlines() if re.match(r'^\s*(?:public\s+)?import\s+',line) for i in re.sub(r'^\s*(?:public\s+)?import\s+','',line).split('--')[0].split() if i in paths] for m,p in paths.items()}
def order(g):
 done=set(); active=[]; out=[]
 def visit(n):
  if n in active: raise RuntimeError('IMPORT CYCLE: '+str(active+[n]))
  if n in done:return
  active.append(n)
  for j in g[n]:visit(j)
  active.pop();done.add(n);out.append(n)
 for n in sorted(g):visit(n)
 return out
before=graph(); order(before)
mutations=[]
for p in sorted((ROOT/'proposal'/'TGLExt').glob('*.lean')):
 dest=K/'TGLExt'/p.name
 mutations.append(dict(path=str(dest),before=digest(dest) if dest.exists() else None,proposal_sha256=digest(p)))
 atomic(dest,p.read_bytes()); paths['TGLExt.'+p.stem]=dest
post=graph(); topo=order(post)
roots=['TGLExt.'+p.stem for p in (ROOT/'proposal'/'TGLExt').glob('*.lean')]
closures={}
for label,seed in [('b',[m for m in roots if m.split('.')[-1] in ['SectorFluidClosure','SectorFriedmann','ThermodynamicFriedmann','TheAngleReachesTheMetric']]),('d',['TGLExt.V351AntiunitaryResolventPhase']),('f',['TGLExt.SectorFriedmannAdditive'])]:
 chosen=set(seed)
 while True:
  more={m for m,im in post.items() if set(im)&chosen}-chosen
  if not more:break
  chosen|=more
 closures[label]=[m for m in topo if m in chosen]
allaffected=set(sum(closures.values(),[])); targets=[m for m in topo if m in allaffected]
record(ROOT/'GRAFO_REBUILD.json',dict(before_acyclic=True,after_acyclic=True,node_count=len(post),imports_before=before,imports_after=post,roots=roots,closures=closures,targets=targets,source_hashes={m:digest(paths[m]) for m in targets},mutations=mutations))
print('CLOSURES', {k:len(v) for k,v in closures.items()}, 'UNION',len(targets),flush=True)
print('\n'.join(targets),flush=True)
# Invalidate only artifacts owned by this root; preserve bytes in a local quarantine.
q=ROOT/'quarantine'/stamp(); quarantined=[]
gtargets=['TGLExt.MixedLadder','TGLExt.SecondCone','TGL.AreaScale']
for m in targets+gtargets:
 for family in ['lib/lean','ir']:
  folder=K/'.lake/build'/family/Path(*m.split('.')[:-1])
  if not folder.exists():continue
  for p in list(folder.glob(m.split('.')[-1]+'.*')):
   assert p.resolve().is_relative_to(K.resolve()) and p.is_file()
   dest=q/p.relative_to(K)
   dest.parent.mkdir(parents=True,exist_ok=True)
   h=digest(p); os.replace(p,dest); assert digest(dest)==h
   quarantined.append(dict(original=str(p),quarantine=str(dest),sha256=h))
record(ROOT/'QUARENTENA_OBJETOS.json',quarantined)
run=ROOT/'builds'/stamp(); run.mkdir(parents=True)
for m in targets+gtargets:atomic(run/'sources'/Path(*m.split('.')).with_suffix('.lean'),paths[m].read_bytes())
cmd=[str(BIN/'lake.exe'),'build',*targets,*gtargets]
record(run/'started.json',dict(command=cmd,cwd=str(K),source_hashes={m:digest(paths[m]) for m in targets+gtargets},started=stamp()))
print('BUILD',run,flush=True); start=time.monotonic()
r=subprocess.run(cmd,cwd=K,env=clean_env(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
atomic(run/'stdout.txt',r.stdout);atomic(run/'stderr.txt',r.stderr)
record(run/'run.json',dict(command=cmd,cwd=str(K),returncode=r.returncode,seconds=time.monotonic()-start,version=subprocess.check_output([str(BIN/'lean.exe'),'--version']).decode().strip(),finished=stamp()))
print('BUILD EXIT',r.returncode,flush=True)
if r.returncode: print('\n'.join(l for l in (r.stdout+r.stderr).decode('utf-8',errors='replace').splitlines() if 'error' in l.lower()))
sys.exit(r.returncode)
