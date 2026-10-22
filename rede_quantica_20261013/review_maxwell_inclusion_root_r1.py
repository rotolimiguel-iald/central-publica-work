"""Independent source/receipt review; does not claim an independent recompilation."""
import datetime as dt, json, re
from pathlib import Path
from diary_r1 import ROOT, new, pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
config=[('orbital_rotation/FINAL_MAXWELL_INCLUSION_RECEIPT_R1.json', 'accepted', 'MAXWELL_INCLUSION_SEMANTIC_REVIEW_ROOT_R1.json', None, ['The strip boundary is identified with the actual positive angular Fourier transform and the existing Maxwell p-wedge-screen coefficient; metric flip, 2*pi normalization and the fixed circular basis are explicit.', 'Support in the right wedge supplies scalar strip analyticity and bounds. Finite exponential expansion supplies the Maxwell growth class. Gaussian regulation proves integrable contour shifts and the exp(2*pi^2*p) boundary balance.', 'Vector L2 Fubini interchange commutes with the actual partial Fourier transform by rank-one totality and continuity. Section L1 conditions are discharged for the regulated coefficient before transferring to the unbounded TW graph.', 'The Gaussian tends strongly to identity; closedness of the existing KWR then proves circularSmear_mem_KWR. Closed real span yields localized_rightWedge_le_KWR.', 'The uniqueness lemma does not infer equality from complex density alone: bounded complex-linear and antilinear regularizers, preservation, fixed equations and strong convergence remain explicit premises.'], ['Only inclusion of the physical right-wedge subspace in KWR is proved by this delivery. Reverse density, wedge_glue, causal locality and the complete covariant net remain separate obligations.', 'Global nonzero test functions do not establish a nonzero wedge-supported test. No such new witness is claimed here.', 'Independent source and receipt review, not independent recompilation. No production source or gate change.'])]
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
  rp=Path(row['receipt']['path']) if key in ('records','accepted') else Path(row['attempt'])/'RECEIPT.json'
  b=json.loads(rp.read_bytes());verify(b)
  assert type(b['exit_code']) is int and b['exit_code']==0
  assert b['readonly_dependencies_unchanged']
  assert b['source']['sha256']==row['source']['sha256']
  log=(rp.parent/'AXIOMS.txt').read_text(encoding='utf-8')
  assert 'sorryAx' not in log and 'error:' not in log
  for n,a in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",log,re.S):
   axs={x.strip() for x in a.split(',') if x.strip()};assert axs<={'propext','Classical.choice','Quot.sound'},(n,axs);decl[n]=sorted(axs)
 if count is not None: assert len(decl)==count,(name,len(decl),count)
 if key=='accepted':
  audits=[x for x in r[key] if 'Audit' in x['module']]
  assert len(audits)==1
  ap=Path(audits[0]['receipt']['path']); auditlog=(ap.parent/'AXIOMS.txt').read_text(encoding='utf-8')
  local=[]
  for line in auditlog.splitlines():
   if line.startswith('LOCAL_DECL\t'):
    parts=line.split('\t'); assert set(parts[2].split(','))-{''} <= {'propext','Classical.choice','Quot.sound'}
    local.append(parts[1])
  assert len(local)==220 and len(set(local))==220
  assert 'AUDITED_COUNT\t220' in auditlog
  findings.append('Aggregate Lean auditor enumerated all 220 local declarations by source module indices; no local axiom and only the allowed trio. Every source module and the auditor was read in this review.')
 target=out/'network_review'/name
 new(target,dict(status='PASS_WITH_STATED_SCOPE',reviewer='codex-root',created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),delivery=pin(delivery),source_files_read=[x['source'] for x in r[key]],pins_verified=len(checked),printed_declarations_verified=decl,independent_rebuild=False,material_findings=[],findings=findings,limits=limits,script=pin(__file__),production_modified=False,gate_modified=False))
 print(json.dumps(dict(review=pin(target),pins=len(checked),declarations=len(decl))))
