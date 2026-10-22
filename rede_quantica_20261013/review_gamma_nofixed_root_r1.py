"""Independent reconstruction and semantic review of absence of nonvacuum fixed vectors on the same Fock."""
from pathlib import Path
import datetime as dt
import hashlib, json, os, re, subprocess, time

BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
OUT=BASE/'gamma_nofixed_root_review_r1'
K=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
SOURCES=[BASE/'gamma_no_fixed'/n for n in ['TensorContractionR5.lean','TensorContractionPropertiesR3.lean','TensorNoFixedR2.lean','CanonicalGammaNoFixedR4.lean']]

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
original=json.loads((BASE/'gamma_no_fixed/attempts/20261015T210614_394253Z/RECEIPT.json').read_bytes())
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
audited=''
for p in SOURCES: audited=compile_file(OUT/p.name)
count=int(re.search(r'AUDITED_COUNT\s+(\d+)',audited).group(1))
assert [pin(p) for p in SOURCES]==before
assert all(pin(p['path'])['sha256']==p['sha256'] for p in readonly)
review=dict(unit='F1.FECHO_20261015',claim_event=845,reviewer='codex-root; independent of Gamma-no-fixed constructor; three root helpers are rechecked but not independently authored',status='PASS_WITH_STATED_SCOPE',created_utc=now(),sources_unchanged=before,builds=builds,all_declarations_including_private=count,script=pin(__file__),findings=[],scope=[
 'The map z to C_z is constructed on completed tensors, bounded, compact and injective, rather than postulated. Finite-rank tensor approximations and norm closure establish compactness.',
 'A fixed tensor intertwines the conjugated first unitary representation with the second. Its positive compact square commutes with the first. A nonzero compact eigenspace would give a common projective eigenvector, contradicting precisely hno.',
 'Each positive existing symmetric tensor sector embeds in H1 tensor its predecessor, and is therefore zero for a fixed vector. Sector zero is proved to be exactly the vacuum line.',
 'The exported theorem has exactly the general family, group and no-common-projective-eigenvector premises of the old Gamma_no_fixed field. Continuity is accepted but unnecessary for this proof.',
 'No replacement of the canonical Fock, no trivial model, no additional assumption equivalent to the conclusion. KMS, full modular boost, scaled trace and global net remain separate obligations.'
],production_modified=False,gate_moved=False)
save(OUT/'REVISAO_GAMMA_NO_FIXED_ROOT_R1.json',json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'review':pin(OUT/'REVISAO_GAMMA_NO_FIXED_ROOT_R1.json'),'all_declarations':count},ensure_ascii=False),flush=True)
