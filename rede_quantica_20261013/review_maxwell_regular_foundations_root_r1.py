"""Independent source/receipt review; does not claim an independent recompilation."""
import datetime as dt, json, re
from pathlib import Path
from diary_r1 import ROOT, new, pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
config=[('maxwell_global/FINAL_MAXWELL_REGULAR_FOUNDATIONS_RECEIPT_R1.json', 'modules', 'MAXWELL_REGULAR_FOUNDATIONS_SEMANTIC_REVIEW_ROOT_R1.json', 16, ['All polynomial L1 and quadratic L2 moments follow from the concrete proper Schwartz restriction and existing temperate-growth integrability theorem. The L2 statement is separately proved, not inferred from L1.', 'The same screen strength times the actual global photon coefficient gives the wave density. The orbital 1/E weight is accounted for; E=0 is handled explicitly rather than divided through.', 'Energy comparison is proved for the existing shell boost, using the Lorentz matrix and its inverse almost everywhere. This is the correct quantitative input to transport a moment domain.', 'Dedekind independence of distinct multiplicative coherent characters proves linear independence of the actual exponential vectors; injectivity of synthesis supplies unique finite coefficients.'], ['The full regular photon domain and its boost/translation invariant Fock realization remain subsequent consumers.', 'No pointwise Wick stress, integrated charge, charge_link or MaxwellCertificate inhabitant is supplied here.', 'This review verifies source, pins and build evidence; it does not claim an independent recompilation.'])]
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
