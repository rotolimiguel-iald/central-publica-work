from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
 assert not p.exists() and p.is_relative_to(R),p
 b=s.encode('utf8');q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
names=re.findall(r'^theorem (\w+)',(K/'TGLExt/V351WeightAverageRecovery.lean').read_text(encoding='utf8'),re.M);assert len(names)==1
put(K/'TGLExt/AuditA1WeightAverageRecovery.lean','import TGLExt.V351WeightAverageRecovery\nset_option pp.universes true\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadAverageRecoverySingleCut.lean',"""import TGLExt.V351WeightAverageRecovery
open TGLExt TGLV350.Regular
example (P : SiteProfile) (A : (regularCoreAlgebra P).toStarSubalgebra) :
    dualQuadraticIntegral (star A.val*A.val) (regularVacuum P) =
      dualQuadraticIntegral
        (star (A.val*regularAverage P 1)*(A.val*regularAverage P 1)) (regularVacuum P) := by
  exact scalarWeight_square_eq_iSup_averages P A
""")
for old,new in [('run_perturbed_weight_order_replay.py','run_weight_average_recovery_replay.py'),('audit_perturbed_weight_order.py','audit_weight_average_recovery.py'),('validate_perturbed_weight_order.py','validate_weight_average_recovery.py')]:
 t=(R/old).read_text(encoding='utf8')
 for a,b in [('perturbed_weight_order','weight_average_recovery'),('V351PerturbedWeightOrder','V351WeightAverageRecovery'),('AuditA1PerturbedWeightOrder','AuditA1WeightAverageRecovery'),('PERTURBED_WEIGHT_ORDER','WEIGHT_AVERAGE_RECOVERY'),('BadPerturbedWeightOrderReversed','BadAverageRecoverySingleCut'),('AUDITORIA_ORDEM_PESO_PERTURBADO_A1B','AUDITORIA_RECUPERACAO_MEDIAS_A1B'),('AUDITORIA_NORMA_PESO_PERTURBADO_A1B','AUDITORIA_ORDEM_PESO_PERTURBADO_A1B')]:t=t.replace(a,b)
 t=t.replace('private_theorems=1','private_theorems=0')
 t=t.replace('perturbed_order_on_existing_weight_domain=True','square_values_recovered_including_infinity=True')
 put(R/new,t)
print(names)

