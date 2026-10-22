from pathlib import Path
import re,os
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
 assert p.is_relative_to(R) and not p.exists(),p
 b=s.encode('utf8');q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
s=(K/'TGLExt/V351ScalarRightActionAlgebra.lean').read_text(encoding='utf8')
names=re.findall(r'^(?:def|theorem) (\w+)',s,re.M)
assert len(names)==12
put(K/'TGLExt/AuditA1RightActionAlgebra.lean','import TGLExt.V351ScalarRightActionAlgebra\nset_option pp.universes true\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadRightActionProductOrder.lean',"""import TGLExt.V351ScalarRightActionAlgebra
open TGLExt TGLV350.Regular
example (P : SiteProfile) (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : ScalarPolarRight P b) (hc : ScalarPolarRight P c)
    (A : scalarWeightLeftIdeal P) :
    ∃ h : A.val*(b*c) ∈ scalarWeightLeftIdeal P,
      scalarWeightGNSEmbedding P ⟨A.val*(b*c),h⟩ =
        antiunitaryConjugate (scalarTomitaPolarFactor P)
          (scalarGNSRepresentation P (star (c*b))) (scalarWeightGNSEmbedding P A) := by
  exact scalarPolarRight_mul P b c hb hc A
""")
for old,new in [('run_right_action_limits_replay.py','run_right_action_algebra_replay.py'),('audit_right_action_limits.py','audit_right_action_algebra.py'),('validate_right_action_limits.py','validate_right_action_algebra.py')]:
 t=(R/old).read_text(encoding='utf8')
 for a,b in [('right_action_limits','right_action_algebra'),('RightActionLimits','RightActionAlgebra'),('RIGHT_ACTION_LIMITS','RIGHT_ACTION_ALGEBRA'),('BadRightActionMissingStar','BadRightActionProductOrder'),('AUDITORIA_LIMITES_ACAO_DIREITA_A1B','AUDITORIA_ALGEBRA_ACAO_DIREITA_A1B'),('AUDITORIA_ESCALA_DUAL_REGULAR_A1B','AUDITORIA_LIMITES_ACAO_DIREITA_A1B'),('AUTHOR_INVERSE_CUTOFF_VALIDATED','AUTHOR_RIGHT_ACTION_ALGEBRA_VALIDATED')]:t=t.replace(a,b)
 t=t.replace("len(targets)==2 and sum(t['kind']=='theorem' for t in targets)==2","len(targets)==12 and sum(t['kind']=='theorem' for t in targets)==10")
 t=t.replace('new_theorems=2, new_definitions=0','new_theorems=10, new_definitions=2').replace('new_theorems=2,new_definitions=0','new_theorems=10,new_definitions=2')
 t=t.replace('right_identity_stable_bounded_strongStar=True','right_identity_norm_closed_star_algebra=True, ambient_cfc_consumed=True')
 put(R/new,t)
print('prepared',names)

