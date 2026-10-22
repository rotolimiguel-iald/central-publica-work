from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
 assert not p.exists() and p.is_relative_to(R),p
 b=s.encode('utf8');q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
s=(K/'TGLExt/V351SineResolventApprox.lean').read_text(encoding='utf8')
names=re.findall(r'^(?:def|theorem) (\w+)',s,re.M);assert len(names)==11
put(K/'TGLExt/AuditA1SineResolvent.lean','import TGLExt.V351SineResolventApprox\nset_option pp.universes true\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadSineResolventLimit.lean',"""import TGLExt.V351SineResolventApprox
open TGLExt TGLV350.Regular Filter
open scoped Topology
example (P : SiteProfile) (u : RegularHilbert (TowerHilbert P)) :
    Tendsto (fun n : ℕ => regularSineResolvent P ((n : ℝ)+1) u) atTop
      (𝓝 ((1-regularSpectralResolvent P) u)) := by
  exact regularSineResolvent_tendsto P u
""")
for old,new in [('run_right_action_algebra_replay.py','run_sine_resolvent_replay.py'),('audit_right_action_algebra.py','audit_sine_resolvent.py'),('validate_right_action_algebra.py','validate_sine_resolvent.py')]:
 t=(R/old).read_text(encoding='utf8')
 for a,b in [('right_action_algebra','sine_resolvent'),('V351ScalarRightActionAlgebra','V351SineResolventApprox'),('AuditA1RightActionAlgebra','AuditA1SineResolvent'),('RIGHT_ACTION_ALGEBRA','SINE_RESOLVENT'),('BadRightActionProductOrder','BadSineResolventLimit'),('AUDITORIA_ALGEBRA_ACAO_DIREITA_A1B','AUDITORIA_APROXIMANTES_SENO_A1B'),('AUDITORIA_LIMITES_ACAO_DIREITA_A1B','AUDITORIA_ALGEBRA_ACAO_DIREITA_A1B')]:t=t.replace(a,b)
 t=t.replace("len(targets)==12 and sum(t['kind']=='theorem' for t in targets)==10","len(targets)==11 and sum(t['kind']=='theorem' for t in targets)==9")
 t=t.replace('new_theorems=10, new_definitions=2','new_theorems=9, new_definitions=2, private_theorems=6, private_definitions=1')
 t=t.replace('new_theorems=10,new_definitions=2','new_theorems=9,new_definitions=2,private_theorems=6,private_definitions=1')
 t=t.replace('right_identity_norm_closed_star_algebra=True, ambient_cfc_consumed=True, approximating_family_constructed=False','actual_resolvent_right_action_proved=True, approximating_family_constructed=True')
 put(R/new,t)
print(names)

