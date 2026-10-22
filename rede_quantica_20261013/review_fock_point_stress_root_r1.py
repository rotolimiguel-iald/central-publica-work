"""Independent source/receipt review; does not claim an independent recompilation."""
import datetime as dt, json, re
from pathlib import Path
from diary_r1 import ROOT, new, pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
config=[('maxwell_global/FINAL_FOCK_POINT_STRESS_RECEIPT_R1.json', 'modules', 'FOCK_POINT_STRESS_SEMANTIC_REVIEW_ROOT_R1.json', 47, ['The off-diagonal coherent Maxwell kernel is built from conjugate and unconjugated actual on-shell waves. Maxwell differentiation, antisymmetry, Bianchi and divergence are proved for regular profiles.', 'The coherent stress includes the actual exponential overlap. Finite coherent coefficients are unique on the existing regular Fock domain, so the finite sesquilinear extension is well defined on Fock vectors, not on arbitrary presentations.', 'The resulting pointwise form is Hermitian, symmetric and conserved. Its diagonal is real; the vacuum has zero stress and an existing coherent witness has strictly positive energy.', 'Generic compact-test weak conservation uses integration by parts with continuity and derivative hypotheses explicit. Fourier wave pairing proves joint integrability and tracks angular 2pi scaling and the half tensor contraction.'], ['The domain is the regular finite coherent span. This receipt does not prove density of that restricted domain, a closed stress operator, or equality with the earlier smeared Wick form.', 'The conservation statement is a form identity on this domain. Arbitrary quantum states are not claimed to have positive normal-ordered local energy.', 'Concrete weak conservation, global boost tensor covariance, null-plane charge convergence and charge_link still require their consumers. Fourier normalization relative to the physical integrated generator remains to be established.', 'Independent source and receipt review, without independent recompilation. No production or gate modification.'])]
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
