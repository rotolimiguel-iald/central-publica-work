"""Independent source/receipt review; does not claim an independent recompilation."""
import datetime as dt, json, re
from pathlib import Path
from diary_r1 import ROOT, new, pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
config=[('takesaki_fock/FOCK_COEFFICIENT_INTERVALS_RECEIPT_R2.json', 'records', 'FOCK_COEFFICIENT_INTERVALS_SEMANTIC_REVIEW_ROOT_R1.json', 43, ['The concrete normalized Fourier coefficient embedding is isometric and has range contained in the actual scalar-weight GNS, using interval totality and the existing cyclic Weyl vacuum. This batch proves that direction, not surjectivity.', 'Translated regular averages with bounded base fibres and their adjoints have finite uniform dual square. Right multiplication is proved only for base fibres; no false two-sided ideal assertion is made.', 'The two Fourier coefficients of each actual finite adjunction pair are evaluated with the correct Haar normalization, reflected intervals and boost factors. Only null interval endpoints are discarded in L2.', 'The closed GNS adjunction graph is a real linear closed subspace, retaining the antilinear scalar rule. The concrete embedding is not an arbitrary Hilbert-space isomorphism.'], ['The DenseR6 docstring says onto before its displayed result establishes only range inclusion. The receipt correctly limits that statement; surjectivity requires the separately compiled reverse inclusion and the subsequent unitary wrapper.', 'No equality of coefficient and GNS Tomita graphs, modular identification, scaled NSF trace or full certificate is supplied by this lot.', 'All fifteen sources were read and existing pins/build receipts checked. This review is independent of their constructor but is not an independent recompilation.'])]
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
