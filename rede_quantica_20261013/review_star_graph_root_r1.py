"""Independent byte-preserving reconstruction of the real star-graph bridge."""
from pathlib import Path
import datetime as dt
import hashlib, json, os, re, subprocess, time

BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
OUT=BASE/'star_graph_root_review_r1'
K=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
SOURCES=[BASE/'gamma_unbounded/BicommutantTwoVectorR2.lean',BASE/'star_graph_density/StarGraphDensityR3.lean',BASE/'star_graph_density/BicommutantStarGraphR1.lean']
def pin(p):
    p=Path(p); b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def save(p,b):
    if isinstance(b,str): b=b.encode('utf-8')
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()

assert not OUT.exists()
OUT.mkdir()
before=[pin(p) for p in SOURCES]
for p in SOURCES: save(OUT/p.name,p.read_bytes())
roots=[OUT,K/'.lake/build/lib/lean']+sorted(K.glob('.lake/packages/*/.lake/build/lib/lean'))+[LEAN.parent.parent/'lib/lean']
lp=os.pathsep.join(map(str,roots)); env=dict(os.environ,LEAN_PATH=lp)
version=subprocess.check_output([str(LEAN),'--version'],text=True).strip()
builds=[]
def compile_file(p):
    cmd=[str(LEAN),'-R',str(OUT),'-o',str(p.with_suffix('.olean')),str(p)]
    start=now(); t=time.perf_counter(); r=subprocess.run(cmd,cwd=OUT,env=env,capture_output=True)
    seconds=time.perf_counter()-t; end=now()
    text=(r.stdout+r.stderr).decode('utf-8','replace')
    save(OUT/(p.stem+'.stdout.log'),r.stdout); save(OUT/(p.stem+'.stderr.log'),r.stderr)
    ax={n:[v.strip() for v in vs.split(',') if v.strip()] for n,vs in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",text,re.S)}
    meta=dict(start_utc=start,end_utc=end,seconds=seconds,command=cmd,toolchain=version,LEAN_PATH=lp,exit_code=r.returncode,source=pin(p),axioms=ax,stdout=pin(OUT/(p.stem+'.stdout.log')),stderr=pin(OUT/(p.stem+'.stderr.log')))
    if p.with_suffix('.olean').exists(): meta['olean']=pin(p.with_suffix('.olean'))
    save(OUT/(p.stem+'.build.json'),json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    assert r.returncode==0,text
    assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in ax.values()) and 'sorryAx' not in text
    builds.append(meta); print(json.dumps({'module':p.stem,'exit':r.returncode,'seconds':seconds}),flush=True)
    return text
for p in SOURCES: compile_file(OUT/p.name)
template=(BASE/'graph_core_review/all_local/AllLocalAuditR1.lean').read_text(encoding='utf-8')
for old,new in zip(['PairedExponentialPolarizationR3','PairedExponentialClosureR4','WeylExponentialGraphCoreR4'],[p.stem for p in SOURCES]): template=template.replace(old,new)
audit=OUT/'AllStarGraphAuditR1.lean'; save(audit,template)
audited=compile_file(audit)
count=int(re.search(r'AUDITED_COUNT\s+(\d+)',audited).group(1))
assert [pin(p) for p in SOURCES]==before
review=dict(unit='F1.FECHO_20261015',claim_event=845,reviewer='codex-root; independent of star-graph and two-vector constructors',status='PASS_WITH_STATED_SCOPE',created_utc=now(),sources_unchanged=before,builds=builds,all_declarations_including_private=count,script=pin(__file__),findings=[],scope=[
    'The unital star algebra orbit in H plus H is reducing; its orthogonal projection blocks commute with A. Membership of a in the bicommutant gives simultaneous approximation on any two vectors.',
    'A real continuous functional on H times H is represented by two Riesz vectors. The adjoint identity turns its second star-graph coordinate into b acting on the second vector; the two-vector density forces every annihilating functional to vanish at the target pair.',
    'The closed real submodule conclusion therefore controls both the input and the adjoint image. This is not a claim of uniform operator-norm bounded approximants or global strong-star convergence.',
    'The generic theorem permits zero Omega. It asserts a closure property for every Omega and does not assert a cyclic or separating vector; those hypotheses must be established in the concrete application.',
    'No Fock polar decomposition, self-adjoint exponential lift, KMS theorem or scaled trace follows from this module alone.'],production_modified=False,gate_moved=False)
save(OUT/'REVISAO_STAR_GRAPH_ROOT_R1.json',json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'review':pin(OUT/'REVISAO_STAR_GRAPH_ROOT_R1.json'),'all_declarations':count},ensure_ascii=False),flush=True)
