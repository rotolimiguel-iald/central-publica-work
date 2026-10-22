"""Independent source/receipt review; does not claim an independent recompilation."""
import datetime as dt, json, re
from pathlib import Path
from diary_r1 import ROOT, new, pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
config=[('maxwell_global/FINAL_MAXWELL_FOCK_DOMAIN_WAVE_RECEIPT_R1.json', 'modules', 'MAXWELL_FOCK_DOMAIN_WAVE_SEMANTIC_REVIEW_ROOT_R1.json', 18, ['The wave is defined by an integrable mass-shell amplitude of the actual H1 profile. Its agreement with the Schwartz wave is almost-everywhere, and its U1 covariance uses the measured phase identity with x-a.', 'The regular finite coherent domain is the range of synthesis on profiles with both L1 and quadratic L2 energy moments. Exponential independence supplies injective synthesis and unique coefficients; vacuum and the existing U1/B0 preserve this same domain in both directions.', 'The spacetime divergence is zero by the established derivative-under-integral theorem and the on-shell symbol on the full-measure regular chart.', 'The finite-dimensional bilinear stress-jet identity is derived from antisymmetry, Bianchi and divergence under a diagonal signature with squares one. These are explicit hypotheses of the reusable identity.'], ['Density of the restricted regular coherent domain is not established by this receipt.', 'The bilinear complex tensor is an algebraic identity. Its application to a real field or a sesquilinear/polarized quantum matrix element requires the corresponding consumer; it alone is not the physical Maxwell stress tensor.', 'The Bianchi consumer, Wick stress on this domain, tensor covariance, integrated null charge and charge_link remain separate obligations.', 'This independent source/receipt review verifies existing build evidence; no independent recompilation is claimed.'])]
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
