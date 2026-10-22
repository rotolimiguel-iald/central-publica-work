"""Independent source/receipt review; does not claim an independent recompilation."""
import datetime as dt, json, re
from pathlib import Path
from diary_r1 import ROOT, new, pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
config=[('takesaki_fock/FOCK_COEFFICIENT_UNITARY_RECEIPT_R1.json', 'records', 'FOCK_COEFFICIENT_UNITARY_SEMANTIC_REVIEW_ROOT_R1.json', 11, ['Right regularization places each scalar-weight orbit in the closed normalized-Fourier coefficient range. The proved GNS completion inclusion follows by closure, using the previously established equality with the full finite-weight domain.', 'The opposite inclusion uses the already constructed coefficient embedding. Both inclusions prove equality of ranges; surjectivity is proved and then used to define an actual complex linear isometry equivalence.', 'The pairing-defined antilinear square relation is identified with the exact maximal-adjoint composition for the closed dense Tomita input. Resolvent membership and its inverse are proved from that equation; no imaginary-power equality is assumed.'], ['This receipt does not yet identify the actual GNS Tomita graph with the coefficient Tomita graph, nor the two modular groups.', 'The scalar dual weight is not asserted to be a trace; semifinite scaled trace and PF remain separate constructions.', 'This is an independent source and receipt review, with no independent recompilation.'])]
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
