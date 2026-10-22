"""Independent reconstruction and semantic review of positive energy on the same Fock."""
from pathlib import Path
import datetime as dt
import hashlib, json, os, re, subprocess, time

BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
OUT=BASE/'gamma_positive_root_review_r2'
K=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
SOURCES=[BASE/'gamma_positive'/n for n in ['BoundedWeakAnalyticR6.lean','OrbitalContractionAnalyticR1.lean','CanonicalGammaPositiveR3.lean']]

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
original=json.loads((BASE/'gamma_positive/attempts/20261015T202147_434535Z/RECEIPT.json').read_bytes())
readonly=[pin(q) for root in dict.fromkeys(original['LEAN_PATH'].split(os.pathsep)) if not Path(root).is_relative_to(K) for q in Path(root).glob('*.olean')]
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
audit=OUT/'AllPositiveAuditR1.lean'; save(audit,template)

audited=compile_file(audit)
count=int(re.search(r'AUDITED_COUNT\s+(\d+)',audited).group(1))
assert [pin(p) for p in SOURCES]==before
assert all(pin(p['path'])['sha256']==p['sha256'] for p in readonly)
review=dict(unit='F1.FECHO_20261015',claim_event=845,reviewer='codex-root; independent of Gamma-positive constructor',status='PASS_WITH_STATED_SCOPE',created_utc=now(),sources_unchanged=before,builds=builds,all_declarations_including_private=count,script=pin(__file__),findings=[],scope=[
 'V(z) is a concrete contractive multiplication operator on the same massless orbital H1 for Im z >= 0. Its real boundary equals the existing U1 translations.',
 'Actual one-particle coefficients are spectral integrals against the finite state-density measure. Positivity of p.a is derived from the forward cone. Polarization extends diagonal analyticity to mixed coefficients.',
 'Actual bounded second quantization on the same Fock maps e(f) to e(V(z)f), has norm <=1, and agrees with gamma(U1(t a)) at the real boundary by exponential totality.',
 'Uniform coefficient estimates, locally uniform holomorphic convergence, and two closed-span inductions extend analyticity and boundary continuity to arbitrary vectors; no Fock analyticity is assumed.',
 'The coefficient bound is norm(psi)^2. The old one-particle-positive-energy premise is unused because the actual orbital construction proves the stronger conclusion directly.',
 'This proves exactly Gamma_positive. It does not assert Gamma_no_fixed, KMS, spectral-readout of the modular boost, a scaled trace, global net or full certificate inhabitation.'
],production_modified=False,gate_moved=False)
save(OUT/'REVISAO_GAMMA_POSITIVE_ROOT_R2.json',json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'review':pin(OUT/'REVISAO_GAMMA_POSITIVE_ROOT_R2.json'),'all_declarations':count},ensure_ascii=False),flush=True)
