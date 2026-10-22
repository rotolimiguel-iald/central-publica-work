"""Independent byte-preserving reconstruction of the concrete same-Fock polar factor and bounded Gamma."""
from pathlib import Path
import datetime as dt
import hashlib, json, os, re, subprocess, time

BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
OUT=BASE/'polar_root_review_r1'
K=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
SOURCES=[BASE/'gamma_unbounded'/n for n in ['BoundedTensorMapR2.lean','BoundedBosonicGammaR2.lean','BoundedGammaPropertiesR2.lean','GammaGraphParametersR3.lean','PartialSquareGraphR2.lean','CanonicalFockPolarR1.lean']]

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
original=json.loads((BASE/'gamma_unbounded/attempts/20261015T195659_806887Z/RECEIPT.json').read_bytes())
readonly=original['dependencies']
assert all(pin(p['path'])['sha256']==p['sha256'] for p in readonly)
roots=list(dict.fromkeys([OUT]+[Path(p) for p in original['LEAN_PATH'].split(os.pathsep)]))
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
template=template.replace('import PairedExponentialPolarizationR3\nimport PairedExponentialClosureR4\nimport WeylExponentialGraphCoreR4','\n'.join('import '+p.stem for p in SOURCES))
template=template.replace('[`PairedExponentialPolarizationR3, `PairedExponentialClosureR4, `WeylExponentialGraphCoreR4]', '['+', '.join('`'+p.stem for p in SOURCES)+']')
audit=OUT/'AllPolarAuditR1.lean'; save(audit,template)

audited=compile_file(audit)
count=int(re.search(r'AUDITED_COUNT\s+(\d+)',audited).group(1))
assert [pin(p) for p in SOURCES]==before
assert all(pin(p['path'])['sha256']==p['sha256'] for p in readonly)
review=dict(unit='F1.FECHO_20261015',claim_event=845,reviewer='codex-root; independent of bounded Gamma and concrete polar constructor',status='PASS_WITH_STATED_SCOPE',created_utc=now(),sources_unchanged=before,builds=builds,all_declarations_including_private=count,script=pin(__file__),findings=[],scope=[
 'The bounded tensor norm estimate uses a finite-dimensional orthonormal expansion; continuous extension to the completed SAME Fock sectors is constructed, not assumed.',
 'The Gamma contraction acts on every existing particle sector, fixes vacuum, and acts on exponential vectors by f to A f. Totality proves self-adjointness, commutation and dense range; dense range plus symmetry gives injectivity.',
 'GA=Gamma(WA) and GB=Gamma(WB) satisfy the actual closed exponential-lift graph by totality and closure. WA squared plus WB squared is used only on one particle; the false second-quantized square-sum identity is absent.',
 'The independently reviewed maximality criterion therefore makes the concrete lift G self-adjoint; its proved positivity and equality of actual Tomita with JG identify the positive factor on the unchanged Weyl algebra and vacuum.',
 'The antilinear adjoint domain is characterized in both directions. Delta is G squared on the genuine two-application domain and its graph is S-dagger S, with positive quadratic energy.',
 'This R1 layer does not yet prove standalone self-adjointness of Delta, spectral imaginary powers, KMS, a scaled trace, global net or full certificate inhabitation. Those are separate consumers.',
 'Source semantic review was performed directly by root; a separate earlier bounded-Gamma source-only review is additional evidence, not substituted for these independent rebuilds.'
],production_modified=False,gate_moved=False)
save(OUT/'REVISAO_POLAR_ROOT_R1.json',json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'review':pin(OUT/'REVISAO_POLAR_ROOT_R1.json'),'all_declarations':count},ensure_ascii=False),flush=True)
