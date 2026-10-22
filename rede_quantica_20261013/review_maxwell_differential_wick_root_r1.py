"""Independent source/receipt review; does not claim an independent recompilation."""
import datetime as dt, json, re
from pathlib import Path
from diary_r1 import ROOT, new, pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
config=[('maxwell_global/FINAL_MAXWELL_DIFFERENTIAL_WICK_RECEIPT_R1.json', 'modules', 'MAXWELL_DIFFERENTIAL_WICK_SEMANTIC_REVIEW_ROOT_R1.json', 20, ['The physical inverse-angular Fourier derivative is proved from SchwartzMap.fourierInv_lineDerivOp_eq with metricFlip/(2*pi); constant tensor injection commutes with the actual Fourier integral.', 'The spacetime divergence test is a finite sum of actual coordinate line derivatives. Its Fourier image is -i times the contracted momentum tensor; existing on-shell nullity then gives a zero H1 smear.', 'The source-free Maxwell identity holds for the actual Segal operator on its dense exponential domain. Its matrix elements form a continuous REAL-linear Schwartz distribution, with no false complex-linearity claim.', 'The bilocal normal-ordered quadratic form is built from actual annihilation operators and adjunction-compatible matrix elements. It has the explicit coherent kernel, zero vacuum expectation and Hermitian swap. Positivity is proved only on diagonal coherent vectors.'], ['Coincident-point Wick stress, conservation of that stress, integrated charge and charge_link are not supplied by this receipt.', 'No invariance under products of unbounded creation operators is assumed. No positivity of every normal-ordered square is claimed.', 'This review checks proof source, hashes and build evidence; it is not an independent recompilation.'])]
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
