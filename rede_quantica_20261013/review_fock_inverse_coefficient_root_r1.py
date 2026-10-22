"""Independent source/receipt review; does not claim an independent recompilation."""
import datetime as dt, json, re
from pathlib import Path
from diary_r1 import ROOT, new, pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
config=[('takesaki_fock/FOCK_INVERSE_AND_COEFFICIENT_INCLUSION_RECEIPT_R1.json', 'records', 'FOCK_INVERSE_COEFFICIENT_SEMANTIC_REVIEW_ROOT_R1.json', 36, ['The supremum functional is on the actual Fock crossed-product positive cone. Its faithfulness uses the actual cutoff at regulator one, injectivity and faithfulness of the dual weight; additivity is not inferred from subadditivity.', 'Finite translated interval coefficients identify concrete pairs in the full-weight GNS Tomita graph. Closure of these pairs gives inclusion of the Fourier-coefficient graph in the actual GNS graph.', 'The regular right action has group, adjoint, unitarity and strong-continuity laws and commutes with the full left representation; conjugation by left and right regular flows yields the actual fibre flow.', 'The root-graph transport theorem proves functional calculus compatibility under an explicit unitary. It does not assume or prove the remaining reverse GNS graph inclusion.'], ['Reverse graph inclusion and full modular identification remain outside this receipt.', 'No additivity, traciality or semifiniteness of the supremum functional is claimed.', 'Independent source and receipt review, without independent recompilation. All seven sources were read. No production or gate modification.'])]
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
