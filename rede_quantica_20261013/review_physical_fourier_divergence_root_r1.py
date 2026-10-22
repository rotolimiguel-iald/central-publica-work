"""Independent source/receipt review; does not claim an independent recompilation."""
import datetime as dt, json, re
from pathlib import Path
from diary_r1 import ROOT, new, pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
config=[('maxwell_global/FINAL_PHYSICAL_FOURIER_DIVERGENCE_RECEIPT_R1.json','modules','PHYSICAL_FOURIER_DIVERGENCE_SEMANTIC_REVIEW_ROOT_R1.json',10,[
 'The physical adapter composes inverse Fourier with metricFlip(p)/(2*pi). It is surjective by its explicit inverse, so no nonzero image is lost by the convention change.',
 'The existing continuous momentum map composed with this adapter is continuous and complex-linear into the SAME H1. Real/imaginary decomposition supplies a real nonzero test; Segal closure, exponential core and nonzero vacuum excitation are inherited from actual existing terms.',
 'The divergence identity is transported from the actual real O16 screen to the Cartesian representative on the regular chart. The proved nullity of the exceptional axis permits exact Lp equality on the whole Schwartz momentum-test domain.',
 'The finite tensor sums contract the lower momentum with p wedge epsilon. The zero is a proved on-shell symbol identity, not a record field or a substituted scalar toy.'
 ],[
 'The Fourier integral translation consumer and the spacetime differential consumer are separate obligations; neither is inferred merely from the inverse-Fourier definition.',
 'Locality, wedge_glue, stress, charge_link, and a joint MaxwellCertificate inhabitant are not claimed by these two modules. The real screen basis still needs circularH1.symm in the helicity consumer.',
 'This review verifies proof source, logs and pins; it does not claim independent recompilation.'
 ])]
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
