from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time, difflib
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV);p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;os.replace(t,p)
def save(p,d):write(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
if len(sys.argv)==1:
    run=REV/('square_adjoint_probe_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    bases=[Path((REV/p).read_text().strip()) for p in ['square_approximation_latest_run.txt','bidual_support_final_latest_run.txt','right_graph_core_final_latest_run.txt']]
    catalog={};origins=[]
    for b in bases:
        m=load(b/'manifest.json');c=load(b/'compilation.json');assert c['all_exit_zero'] and c['dependencies_preserved']
        origins.append({'run':str(b),'manifest_sha256':hf(b/'manifest.json'),'compilation_sha256':hf(b/'compilation.json')})
        for n,d in m['dependencies'].items():
            catalog.setdefault(n,dict(source=d['frozen_source'],binary=d['frozen_binary'],source_sha256=d['source_sha256'],binary_sha256=d['sha256']))
        for rel,d in m['sources'].items():
            row=next((r for r in c['records'] if r['module']==rel),None)
            if row is not None:catalog[rel[:-5].replace('/','.')]=dict(source=d['snapshot'],binary=row['command'][2],source_sha256=d['sha256'],binary_sha256=row['output_sha256'])
        if 'inherited_bidual' in m:
            q=m['inherited_bidual'];d=m['sources']['TGLV350/ScalarTomitaBidual.lean']
            catalog['TGLV350.ScalarTomitaBidual']=dict(source=d['snapshot'],binary=q['binary'],source_sha256=d['sha256'],binary_sha256=q['binary_sha256'])
    src=ROOT/'kernel/TGLV350/ScalarSquareAdjointTest.lean';raw=src.read_bytes();write(run/'author_snapshot.lean',raw)
    needed=set()
    def visit(n):
        if n in needed or n.split('.')[0] not in {'TGL','TGLExt','TGLV350'}:return
        assert n in catalog,n;needed.add(n)
        for x in re.findall(r'^import\s+([\w.]+)',Path(catalog[n]['source']).read_text(encoding='utf-8'),re.M):visit(x)
    for n in re.findall(r'^import\s+([\w.]+)',raw.decode(),re.M):visit(n)
    deps={}
    for n in sorted(needed):
        d=catalog[n];sp=Path(d['source']);bp=Path(d['binary'])
        assert sp.resolve().is_relative_to(REV) and bp.resolve().is_relative_to(REV)
        assert hf(sp)==d['source_sha256'] and hf(bp)==d['binary_sha256'],n
        rel=Path(*n.split('.'));dst=run/'build'/rel.with_suffix('.olean');write(dst,bp.read_bytes());cp={}
        for p in bp.parent.glob(bp.name+'.*'):
            if p.is_file():q=dst.with_name(p.name);write(q,p.read_bytes());cp[str(q)]=hf(q)
        deps[n]={**d,'copied_binary':str(dst),'companions':cp}
    lp=os.pathsep.join([str(run/'build')]+m['lean_path'].split(os.pathsep)[1:]);assert str(ROOT/'build') not in lp
    assert hf(m['compiler'])==m['compiler_sha256']
    manifest={'run':str(run),'author_source':str(src),'snapshot_sha256':sha(raw),'origins':origins,'dependencies':deps,'compiler':m['compiler'],'compiler_sha256':m['compiler_sha256'],'lean_path':lp,'scope':'DIAGNOSTIC_ONLY_NO_DEV_ACCEPTANCE'}
    save(run/'manifest.json',manifest)
    s=raw.decode()
    # Syntax repair requested separately by author; preserve the docstrings.
    s=re.sub(r'(/\*\*.*?\*/)',r'\1',s,flags=re.S)
    s=re.sub(r'(/--[^\n]*-/)\n(set_option maxHeartbeats 600000 in)\n',r'\2\n\1\n',s)
    a=s.index('private theorem differencePairing ');z=s.index('\nprivate theorem pairingConstraintClosed',a)
    block=s[a:z]
    block=block.replace('{H B : Type} [NormedAddCommGroup H]\n    [InnerProductSpace ℂ H] [AddCommGroup B] [Module ℂ B] [Mul B]\n    (j : B →ₗ[ℂ] H) (a u v : B)',
      '{H : Type} [NormedAddCommGroup H]\n    [InnerProductSpace ℂ H] [CompleteSpace H]\n    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H))\n    (j : E →ₗ[ℂ] H) (a u v : E)')
    assert '[Mul B]' not in block;s=s[:a]+block+s[z:]
    old='''  exact differencePairing (H := ScalarGNSHilbert P) (B := scalarPairedRightAlgebra P)
    (scalarRightPairVector P)
    (scalarRightSquareApproximation P a ha n)
    (a+scalarRightSquareCutoff P a ha n) (a-scalarRightSquareCutoff P a ha n) y z
    (scalarRightSquareApproximation_difference_of_squares P a ha n) hp hm'''
    new='''  refine differencePairing (H := ScalarGNSHilbert P) (scalarPairedRightAlgebra P)
    (scalarRightPairVector P)
    (scalarRightSquareApproximation P a ha n)
    (a+scalarRightSquareCutoff P a ha n) (a-scalarRightSquareCutoff P a ha n) y z ?_ ?_ ?_
  · exact scalarRightSquareApproximation_difference_of_squares P a ha n
  · exact hp
  · exact hm'''
    assert old in s;s=s.replace(old,new,1)
    a=s.index('private theorem fixedVectorTest ');z=s.index('\n/-- Exact test characterization',a) if '\n/-- Exact test characterization' in s[a:] else s.index('\nset_option maxHeartbeats 600000 in',a)
    block=s[a:z]
    block=block.replace('{H B : Type} [NormedAddCommGroup H]\n    [InnerProductSpace ℂ H] [AddCommGroup B] [Module ℂ B] [Star B]\n    (j : B →ₗ[ℂ] H)',
      '{H : Type} [NormedAddCommGroup H]\n    [InnerProductSpace ℂ H] [CompleteSpace H]\n    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H))\n    (j : E →ₗ[ℂ] H)')
    block=block.replace('(hj : ∀ a : B,','(hj : ∀ a : E,').replace('(a : B) (ha : star a=a)','(a : E) (ha : star a=a)')
    assert '[Star B]' not in block;s=s[:a]+block+s[z:]
    old='''    exact fixedVectorTest (H := ScalarGNSHilbert P) (B := scalarPairedRightAlgebra P)
      (scalarRightPairVector P) (scalarTomitaAdjointDomain P)
      (fun x => scalarTomitaAdjoint P x) (fun a => scalarRightPairVector_original_adjoint P a) y z
      ((scalarClosedTomita_bidual_graph_iff P y z).mp h) (b*b) hs'''
    new='''    refine fixedVectorTest (H := ScalarGNSHilbert P) (scalarPairedRightAlgebra P)
      (scalarRightPairVector P) (scalarTomitaAdjointDomain P)
      (fun x => scalarTomitaAdjoint P x) ?_ y z ?_ (b*b) hs
    · intro a
      exact scalarRightPairVector_original_adjoint P a
    · exact (scalarClosedTomita_bidual_graph_iff P y z).mp h'''
    assert old in s;s=s.replace(old,new,1)
    write(run/'SubalgebraBridge.lean',s.encode())
    diff=''.join(difflib.unified_diff(raw.decode().splitlines(True),s.splitlines(True),fromfile='author_snapshot.lean',tofile='SubalgebraBridge.lean'))
    write(run/'SubalgebraBridge.patch',diff.encode())
    print(json.dumps({'prepared':str(run),'dependencies':len(deps),'snapshot_sha256':sha(raw)}),flush=True);mode='SubalgebraBridge'
else:run=Path(sys.argv[1]);mode=sys.argv[2];manifest=load(run/'manifest.json')
env=os.environ.copy();env['LEAN_PATH']=manifest['lean_path'];(run/'tmp').mkdir(exist_ok=True);env['TMP']=env['TEMP']=str(run/'tmp')
sp=run/(mode+'.lean');bp=run/(mode+'.olean');assert not bp.exists()
cmd=[manifest['compiler'],'-o',str(bp),str(sp)];start=time.monotonic()
with (run/(mode+'.stdout.txt')).open('xb') as out, (run/(mode+'.stderr.txt')).open('xb') as err:
    r=subprocess.run(cmd,cwd=run,env=env,stdout=out,stderr=err)
stdout=(run/(mode+'.stdout.txt')).read_bytes();stderr=(run/(mode+'.stderr.txt')).read_bytes()
ax={n:sorted(x.strip() for x in a.split(',') if x.strip()) for n,a in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",stdout.decode(errors='replace'),re.S)}
row={'command':cmd,'returncode':r.returncode,'seconds':round(time.monotonic()-start,3),'source_sha256':hf(sp),'stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr),'output_sha256':hf(bp) if bp.exists() else None,'axioms':ax,'all_five_trio':len(ax)==5 and all(set(x)<={'propext','Classical.choice','Quot.sound'} for x in ax.values()),'dependencies_preserved':all(hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256'] and hf(d['copied_binary'])==d['binary_sha256'] for d in manifest['dependencies'].values())}
save(run/(mode+'.json'),row);print(json.dumps(row),flush=True);print(stdout.decode('utf-8',errors='replace'),flush=True)
