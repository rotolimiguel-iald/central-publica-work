"""Independent proof-source and immutable receipt review; no rebuild claim."""
import datetime as dt,json,re
from pathlib import Path
from diary_r1 import ROOT,new,pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
delivery=out/'orbital_rotation/FINAL_PHYSICAL_LOCALIZATION_RECEIPT_R1.json'
r=json.loads(delivery.read_bytes());checked={};decl={}
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
for row in r['accepted']:
 rp=Path(row['receipt']['path']);b=json.loads(rp.read_bytes());verify(b)
 assert b['exit_code']==0 and b['readonly_dependencies_unchanged']
 assert b['source']['sha256']==row['source']['sha256']
 log=(rp.parent/'AXIOMS.txt').read_text(encoding='utf8')
 assert 'sorryAx' not in log and 'error:' not in log
 for line in log.splitlines():
  if line.startswith('LOCAL_DECL\t'):
   _,n,a=line.split('\t',2);axs={x.strip() for x in a.split(',') if x.strip()}
   assert axs<={'propext','Classical.choice','Quot.sound'};decl[n]=sorted(axs)
assert len(decl)==r['all_local_decl_count']==95
result=out/'network_review/PHYSICAL_LOCALIZATION_SEMANTIC_REVIEW_ROOT_R1.json'
new(result,dict(status='PASS_WITH_STATED_SCOPE',reviewer='codex-root',created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),delivery=pin(delivery),source_files_read=[x['source'] for x in r['accepted']],pins_verified=len(checked),local_declarations_verified=decl,independent_rebuild=False,material_findings=[],findings=[
 'The positive angular inverse Fourier is proved to transform test translations by the exact canonical U1 phase, including the 2*pi rescaling and Minkowski pairing. The prior negative convention is retained separately.',
 'The physical Maxwell map uses the same H1 and the actual circularH1.symm. Supported real test generators yield closed real subspaces. Their isotony and translation equivalence are proved by generators and closure, without extra locality axioms.',
 'The lower-rapidity strip estimates use genuine right-wedge support and m>=0. Schwartz integrability dominates the integral; the first moment gives a local derivative dominator. Analyticity inside and continuity on the closed strip are derived.',
 'The lower pi boundary is the conjugate of the real boundary at opposite transverse momenta for real scalar tests. The generic contour result uses Cauchy-Goursat with precisely closed-strip continuity and interior differentiability.',
 'The compiler audit covers all 95 local declarations, including generated/private declarations, and refuses local axioms beyond the allowed imported trio.'
],limits=[
 'The vector p-wedge-screen boundary and L2 weighted domain for TW are not yet proved by these scalar strip lemmas.',
 'Horizontal integrability and vanishing vertical limit are explicit hypotheses in the generic contour result; they must be supplied by its actual consumer.',
 'Global nonzero smearing does not establish a compactly supported wedge witness. Causal locality, boost covariance of the localized subspaces and wedge_glue equality remain separate obligations.',
 'The review verifies proof sources, hashes and build receipts, without claiming an independent recompilation.'
],script=pin(__file__),production_modified=False,gate_modified=False))
print(json.dumps(dict(review=pin(result),pins=len(checked),declarations=len(decl))))
