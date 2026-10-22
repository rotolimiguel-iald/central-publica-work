from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
 assert not p.exists() and p.is_relative_to(R),p
 b=s.encode('utf8');q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
s=(K/'TGLExt/V351PerturbedWeightOrder.lean').read_text(encoding='utf8')
names=re.findall(r'^theorem (\w+)',s,re.M);assert len(names)==1
put(K/'TGLExt/AuditA1PerturbedWeightOrder.lean','import TGLExt.V351PerturbedWeightOrder\nset_option pp.universes true\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadPerturbedWeightOrderReversed.lean',"""import TGLExt.V351PerturbedWeightOrder
open TGLExt TGLV350.Regular
example (P : SiteProfile)
    (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (hc : c ∈ scalarPolarRightAlgebra P)
    (hbc : b * star b ≤ c * star c) (A : scalarWeightLeftIdeal P) :
    dualQuadraticIntegral (star c.val*(star A.val.val*A.val.val)*c.val) (regularVacuum P) ≤
    dualQuadraticIntegral (star b.val*(star A.val.val*A.val.val)*b.val) (regularVacuum P) := by
  exact scalarWeight_right_perturbed_mono P b c hb hc hbc A
""")
for old,new in [('run_perturbed_weight_norm_replay.py','run_perturbed_weight_order_replay.py'),('audit_perturbed_weight_norm.py','audit_perturbed_weight_order.py'),('validate_perturbed_weight_norm.py','validate_perturbed_weight_order.py')]:
 t=(R/old).read_text(encoding='utf8')
 for a,b in [('perturbed_weight_norm','perturbed_weight_order'),('V351PerturbedWeightNorm','V351PerturbedWeightOrder'),('AuditA1PerturbedWeightNorm','AuditA1PerturbedWeightOrder'),('PERTURBED_WEIGHT_NORM','PERTURBED_WEIGHT_ORDER'),('BadPerturbedWeightWithoutJ','BadPerturbedWeightOrderReversed'),('AUDITORIA_NORMA_PESO_PERTURBADO_A1B','AUDITORIA_ORDEM_PESO_PERTURBADO_A1B'),('AUDITORIA_CFC_CORTES_A1B','AUDITORIA_NORMA_PESO_PERTURBADO_A1B')]:t=t.replace(a,b)
 t=t.replace("len(targets)==2 and sum(t['kind']=='theorem' for t in targets)==2","len(targets)==1 and sum(t['kind']=='theorem' for t in targets)==1")
 t=t.replace('new_theorems=2, new_definitions=0, private_theorems=0, private_definitions=0','new_theorems=1, new_definitions=0, private_theorems=1, private_definitions=0')
 t=t.replace('new_theorems=2,new_definitions=0,private_theorems=0,private_definitions=0','new_theorems=1,new_definitions=0,private_theorems=1,private_definitions=0')
 t=t.replace('perturbed_values_on_existing_weight_domain=True','perturbed_order_on_existing_weight_domain=True')
 put(R/new,t)
print(names)

