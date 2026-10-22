from support import *
import subprocess,time
K=ROOT/'kernel';B=ROOT.parent/'TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA'
D=ROOT/'binary/rebuild'/stamp();D.mkdir(parents=True)
g=json.loads((ROOT/'GRAFO_REBUILD.json').read_text(encoding='utf-8'))['imports_after']
def ancestors(m):
 out=set()
 def add(x):
  if x in out:return
  out.add(x)
  for i in g[x]:add(i)
 add(m);return out
mods=['TGLExt.MixedLadder','TGLExt.SecondCone','TGL.AreaScale']
affected=set(json.loads((ROOT/'GRAFO_REBUILD.json').read_text(encoding='utf-8'))['targets'])|{'TGLExt.ModularFlowAlgebra'}
for m in mods:assert not (ancestors(m)&affected), (m,ancestors(m)&affected)
rows=[]
for m in mods:
 rel=Path(*m.split('.'));src=K/rel.with_suffix('.lean');rundir=D/m;rundir.mkdir()
 atomic(rundir/src.name,src.read_bytes())
 old_setup=B/'kernel/.lake/build/ir'/rel.with_suffix('.setup.json')
 setup=old_setup.read_text(encoding='utf-8').replace(str(B/'kernel').replace('\\','\\\\'),str(K).replace('\\','\\\\'))
 obj=json.loads(setup)
 assert all(str(K) in p for vals in obj['importArts'].values() for p in vals)
 localsetup=rundir/'setup.json';atomic(localsetup,setup)
 out=rundir/'objects'/src.stem;out.parent.mkdir()
 cmd=[str(BIN/'lake.exe'),'env','lean',str(src),'-o',str(out.with_suffix('.olean')),'-i',str(out.with_suffix('.ilean')),'-c',str(out.with_suffix('.c')),'--setup',str(localsetup)]
 before=digest(src);t=time.monotonic();r=subprocess.run(cmd,cwd=K,env=clean_env(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 atomic(rundir/'stdout.txt',r.stdout);atomic(rundir/'stderr.txt',r.stderr)
 art=out.with_suffix('.olean')
 compare=[]
 if r.returncode==0:
  for tag in ['kernel','s']:
   op=B/tag/'.lake/build/lib/lean'/rel.with_suffix('.olean');compare.append(dict(root=tag,path=str(op),sha256=digest(op),matches_new=digest(op)==digest(art)))
 row=dict(module=m,source=str(src),source_sha256=before,source_unchanged=before==digest(src),command=cmd,setup_path=str(localsetup),setup_sha256=digest(localsetup),returncode=r.returncode,seconds=time.monotonic()-t,output=str(art) if art.exists() else None,output_sha256=digest(art) if art.exists() else None,comparisons=compare,log=str(rundir/'stdout.txt'),log_sha256=digest(rundir/'stdout.txt'))
 record(rundir/'run.json',row);rows.append(row)
 print(m,'rc',r.returncode,'matching',[x['root'] for x in compare if x['matches_new']],flush=True)
 if r.returncode:print((r.stdout+r.stderr).decode('utf-8',errors='replace'))
record(D/'RESULTADO.json',rows)
record(ROOT/'binary/REBUILD_ATUAL.json',dict(directory=str(D),results=str(D/'RESULTADO.json'),all_compiled=len(rows)==3 and all(r['returncode']==0 for r in rows)))
