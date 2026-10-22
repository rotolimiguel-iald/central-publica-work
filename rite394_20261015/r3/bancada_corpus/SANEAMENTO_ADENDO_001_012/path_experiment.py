from support import *
import subprocess,time
K=ROOT/'kernel';cur=json.loads((ROOT/'binary/REBUILD_ATUAL.json').read_text(encoding='utf-8'))
prior=json.loads(Path(cur['results']).read_text(encoding='utf-8'))
row=next(x for x in prior if x['module']=='TGL.AreaScale')
setup=Path(row['setup_path']);assert setup.exists()
D=ROOT/'binary/path_experiment'/stamp();D.mkdir(parents=True)
src=K/'TGL/AreaScale.lean';raw=D/'current.olean';env=clean_env();results=[]
for label,sp in [('absolute_1',str(src)),('relative','TGL/AreaScale.lean'),('absolute_2',str(src))]:
 assert not raw.exists();cmd=[str(BIN/'lake.exe'),'env','lean',sp,'-o',str(raw),'--setup',str(setup)]
 before=digest(src);t=time.monotonic();r=subprocess.run(cmd,cwd=K,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 atomic(D/(label+'.stdout.txt'),r.stdout);atomic(D/(label+'.stderr.txt'),r.stderr)
 out=D/(label+'.olean')
 if raw.exists():
  assert raw.resolve().is_relative_to(ROOT) and out.resolve().is_relative_to(ROOT);os.replace(raw,out)
 res=dict(label=label,command=cmd,cwd=str(K),returncode=r.returncode,seconds=time.monotonic()-t,source_sha256=before,source_unchanged=before==digest(src),output=str(out) if out.exists() else None,output_sha256=digest(out) if out.exists() else None,output_bytes=out.stat().st_size if out.exists() else None)
 results.append(res);record(D/(label+'.json'),res);print(label,r.returncode,flush=True)
 if r.returncode:print((r.stdout+r.stderr).decode('utf-8',errors='replace'));break
ok=len(results)==3 and all(x['returncode']==0 and x['source_unchanged'] for x in results)
comparison={}
if ok:
 a,b,c=[Path(x['output']).read_bytes() for x in results]
 comparison=dict(absolute_repeats_byte_identical=a==c,relative_differs_from_absolute=a!=b,absolute_path_occurrences=a.count(str(src).encode('utf-8')),relative_path_occurrences=b.count(b'TGL/AreaScale.lean'),absolute_path_present_in_relative=str(src).encode('utf-8') in b,absolute_1_bytes=len(a),relative_bytes=len(b),absolute_2_bytes=len(c),command_1_equals_3=results[0]['command']==results[2]['command'],command_1_vs_2_differences=[dict(index=i,first=x,second=y) for i,(x,y) in enumerate(zip(results[0]['command'],results[1]['command'])) if x!=y])
record(D/'RESULTADO.json',dict(all_compiled=ok,runs=results,comparison=comparison,scope='Ensaio ABA no mesmo fonte fisico, mesmos imports e destino, mudando so a grafia do argumento do fonte; nao reconstitui por si o historico das outras raizes.'))
record(ROOT/'binary/EXPERIMENTO_ATUAL.json',dict(report=str(D/'RESULTADO.json'),all_compiled=ok,comparison=comparison))
print(comparison,flush=True)
