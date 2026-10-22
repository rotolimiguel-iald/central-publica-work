"""Independent source/receipt review; does not claim an independent recompilation."""
import datetime as dt, json, re
from pathlib import Path
from diary_r1 import ROOT, new, pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
config=[('takesaki_fock/FOCK_COEFFICIENT_FOUNDATIONS_RECEIPT_R1.json','records','COEFFICIENT_FOUNDATIONS_SEMANTIC_REVIEW_ROOT_R1.json',75,[
 'The regular right ambient group is characterMultiplier times fibre shift; the right weight invariance uses the explicitly named invariant test vector. Strong continuity is proved from the existing shift and character actions.',
 'The spectral code f(a) -> shift(a)testVector(f(a)) is a concrete isometry. Normalized Fourier rescales by 2*pi with sqrt(2*pi)^(-1); its inverse and norm are proved, and fibre/shift intertwining is explicit.',
 'The interval-average coefficient formula matches the actual dualHaarFactor. L1/L2 Fourier agreement is used only on the integrable interval orbit; arbitrary L2 vectors are not assigned unjustified Fourier integrals.',
 'The range projection of the isometry commutes with generators and their adjoints; the existing star-bicommutant transport yields reduction for the full represented core, not just the algebraic generators.',
 'Interval totality follows from Lebesgue differentiation and separability of each AE range. No separability of the entire Hilbert space is inserted. The closed-submodule restriction computes the adjoint using reducing invariance.'
 ],[
 'The coefficient map onto the actual weight GNS completion, the full Tomita equality and the modular implementation remain separate unfinished consumers.',
 'No scaled trace is constructed by this batch; dual weight and trace are distinct.',
 'Source, dependency and build evidence reviewed. This is not an independent recompilation or actual main execution.'
 ])]
for rel,key,name,count,findings,limits in config:
 delivery=out/rel;r=json.loads(delivery.read_bytes());checked={}; decl={}
 def verify(v):
  if isinstance(v,dict):
   if {'path','sha256'}<=v.keys():
    a=pin(v['path']);assert a['sha256']==v['sha256'],v['path']
    if 'bytes' in v:assert a['bytes']==v['bytes'],v['path']
    checked[v['path']]=a
   for x in v.values():verify(x)
  elif isinstance(v,list):
   for x in v:verify(x)
 verify(r)
 for row in r[key]:
  rp=Path(row['receipt']['path']) if key=='records' else Path(row['attempt'])/'RECEIPT.json'
  b=json.loads(rp.read_bytes());verify(b)
  assert type(b['exit_code']) is int and b['exit_code']==0
  assert b['readonly_dependencies_unchanged']
  assert b['source']['sha256']==row['source']['sha256']
  log=(rp.parent/'AXIOMS.txt').read_text(encoding='utf-8')
  assert 'sorryAx' not in log and 'error:' not in log
  for n,a in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",log,re.S):
   axs={x.strip() for x in a.split(',') if x.strip()};assert axs<={'propext','Classical.choice','Quot.sound'},(n,axs);decl[n]=sorted(axs)
 assert len(decl)==count,(name,len(decl),count)
 target=out/'network_review'/name
 new(target,dict(status='PASS_WITH_STATED_SCOPE',reviewer='codex-root',created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),delivery=pin(delivery),source_files_read=[x['source'] for x in r[key]],pins_verified=len(checked),printed_declarations_verified=decl,independent_rebuild=False,material_findings=[],findings=findings,limits=limits,script=pin(__file__),production_modified=False,gate_modified=False))
 print(json.dumps(dict(review=pin(target),pins=len(checked),declarations=len(decl))))
