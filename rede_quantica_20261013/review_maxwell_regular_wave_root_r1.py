"""Independent source/receipt review; does not claim an independent recompilation."""
import datetime as dt, json, re
from pathlib import Path
from diary_r1 import ROOT, new, pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
config=[('maxwell_global/FINAL_MAXWELL_REGULAR_WAVE_RECEIPT_R1.json', 'modules', 'MAXWELL_REGULAR_WAVE_SEMANTIC_REVIEW_ROOT_R1.json', 25, ['The concrete H1 domain requires all polynomial L1 moments and, separately, all quadratic L2 energy moments in the original orbital measure. Physical Schwartz smears inhabit both, with a proved nonzero witness.', 'The 1/E orbital density and zero-energy case are handled in the moment estimates. Finite energy is the m=1 quadratic moment, not inferred from L1 regularity.', 'The existing U1 preserves profile norms almost everywhere; B0 acts by the existing measure-preserving coordinate boost. The two-sided energy bound supplies integrability after that change of variables.', 'The same mass-shell wave uses exp(-i p.x), is continuous by domination, and its coordinate derivative is proved under the integral with the first energy moment as a majorant. No exchange of differentiation/integration is assumed.'], ['This is a one-particle regular domain and a coherent wave kernel. The invariant coherent Fock domain and pointwise divergence consumers are separate modules.', 'No local Wick stress, null-plane integrated charge, charge_link, tensor covariance or MaxwellCertificate inhabitant is established by this lot.', 'This independent source and receipt review checks hashes and existing compilation evidence; it does not claim independent recompilation.'])]
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
