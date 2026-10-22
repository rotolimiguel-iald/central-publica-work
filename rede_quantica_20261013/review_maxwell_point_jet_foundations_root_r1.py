"""Independent source/receipt review; does not claim an independent recompilation."""
import datetime as dt, json, re
from pathlib import Path
from diary_r1 import ROOT, new, pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
config=[('maxwell_global/FINAL_MAXWELL_POINT_JET_FOUNDATIONS_RECEIPT_R1.json', 'modules', 'MAXWELL_POINT_JET_FOUNDATIONS_SEMANTIC_REVIEW_ROOT_R1.json', 19, ['The actual regular H1 profile wave has all needed density moments. Its coordinate derivative is computed under the integral using the second L1 moment, and divergence vanishes by the on-shell identity on the full-measure chart.', 'Antisymmetry and Bianchi for the Cartesian p-wedge-screen representative are proved; the lowered Bianchi identity includes the explicit Lorentz signature factors.', 'A concrete nonnegative smooth momentum bump makes the 01 component of the wave strictly positive at the origin. Fourier surjectivity supplies a Schwartz spacetime label for a nonzero physical wave.', 'The polynomial stress jet equals its genuine coordinate derivative; its symmetry is algebraic. For a real antisymmetric field its energy is half the six independent squared components and is nonnegative.'], ['The nonzero spacetime label furnished by Fourier surjectivity is not asserted to be real or supported in a prescribed wedge.', 'The real profile field consumer must supply Bianchi/divergence for the full constructed jet before applying stress conservation.', 'Classical nonnegative energy does not assert positivity of a normal-ordered quantum stress for all states.', 'Tensor covariance, the Wick stress realization on Fock, integrated null charge and charge_link remain separate obligations.', 'Independent source/receipt review only; no independent recompilation is claimed.'])]
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
