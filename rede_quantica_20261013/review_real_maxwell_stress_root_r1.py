"""Independent source/receipt review; does not claim an independent recompilation."""
import datetime as dt, json, re
from pathlib import Path
from diary_r1 import ROOT, new, pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
config=[('maxwell_global/FINAL_REAL_MAXWELL_STRESS_RECEIPT_R1.json', 'modules', 'REAL_MAXWELL_STRESS_SEMANTIC_REVIEW_ROOT_R1.json', 25, ['The lowered on-shell Maxwell symbol is constructed from the same p-wedge-screen coefficient, with metric signs explicit in antisymmetry, Bianchi and divergence.', 'The first spacetime jet is obtained by dominated differentiation of the actual regular-profile integral. Maxwell equations are conclusions, not fields assumed in an input record.', 'The real-linear sqrt(2) projection yields a real classical field with the Segal coherent normalization. Product differentiation and the algebraic jet identity prove conservation of its actual stress.', 'The stress is real and symmetric, and its energy is a sum of squares. The existing nonnegative momentum bump gives a StrongRegularProfile with strictly positive energy; the zero profile has zero stress.'], ['This delivery is the classical real field on the existing H1 profile domain. A pointwise Wick tensor and its sesquilinear extension on the regular Fock domain remain separate consumers.', 'No positivity of normal-ordered stress in arbitrary quantum states, boost tensor covariance, null-plane integrated charge, charge_link, MaxwellCertificate inhabitant or observed physical source is inferred.', 'Independent source and receipt review, without independent recompilation. No production or gate modification.'])]
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
