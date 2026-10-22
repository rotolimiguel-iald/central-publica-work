"""Independent source/receipt review; does not claim an independent recompilation."""
import datetime as dt, json, re
from pathlib import Path
from diary_r1 import ROOT, new, pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
config=[
 ('takesaki_fock/FOCK_FULL_WEIGHT_TOMITA_RECEIPT_R1.json','records','FULL_WEIGHT_TOMITA_SEMANTIC_REVIEW_ROOT_R1.json',26,[
 'The full nonunital star algebra is n_nu intersect n_nu_star using the scalar finite weight on the SAME represented Fock core; closure under products uses the left ideal property on both adjoints.',
 'The full-weight embedding agrees with the earlier uniform embedding and uses the same scalar orbit and Haar normalization.',
 'The sandwich approximates A and A_star simultaneously in GNS norm. The adjoint approximation uses the existing contraction theorem, not a false continuity of adjunction for strong operator topology.',
 'The inclusion of the full raw graph in the original closed graph and the reverse inclusion from the uniform star core prove equality of closures; the existing closed Tomita operator therefore has the full-weight graph as its core.'
 ],[
 'No modular-flow equality with regular conjugation, KMS strip or scaled semifinite trace is proved in this block.',
 'The raw graph is not asserted closed; graph equality is an equality after closure.'
 ]),
 ('maxwell_global/FINAL_GLOBAL_MAXWELL_SCHWARTZ_RECEIPT_R1.json','modules','GLOBAL_MAXWELL_SCHWARTZ_SEMANTIC_REVIEW_ROOT_R1.json',40,[
 'The actual massless shell has proper norm control and at-most-linear energy growth. The real O16 bivector agrees with its measurable Cartesian representative off a proved null axis.',
 'Each bivector component is bounded by E. Its square cancels the shell density 1/E; Schwartz seminorm decay proves actual global L2 integrability, rather than taking it as a record assumption.',
 'The mass-shell restriction is a continuous complex-linear map into the original H1, with a majorant using finitely many Schwartz seminorms. The Fourier convention is explicitly negative with 2*pi and Minkowski metric flip.',
 'An antisymmetric 01 momentum bump supplies a nonzero H1 vector. Fourier surjectivity supplies a spacetime Schwartz test, and real/imaginary decomposition supplies an existential real nonzero test.',
 'The same Segal operator is essentially self-adjoint with its existing exponential core and nonzero vacuum excitation. This does not assert complex linearity of self-adjoint fields in complex labels.'
 ],[
 'A physical positive angular Fourier adapter is required before identifying this smearing with U1 translations or the chosen wedge boundary. The existing convention does not invalidate integrability or continuity.',
 'No compact spacetime support follows from a compact momentum bump; no wedge_glue, causal locality, stress tensor, charge_link or MaxwellCertificate inhabitant follows from this delivery.',
 'The supplied receipt correctly leaves circular-basis transport and global distributional differential identities to separate consumers.'
 ])]
for rel,key,name,count,findings,limits in config[1:]:
 limits.append("Editorial correction: the sibling message reported 43 prints; the archived logs contain 40 unique printed declarations, all checked. The source proofs are unaffected.")
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
