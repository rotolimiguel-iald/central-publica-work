from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
 assert not p.exists() and p.is_relative_to(R),p
 b=s.encode('utf8');q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
names=re.findall(r'^theorem (\w+)',(K/'TGLExt/V351CutoffAverageCommutation.lean').read_text(encoding='utf8'),re.M);assert len(names)==3
put(K/'TGLExt/AuditA1CutoffAverageCommutation.lean','import TGLExt.V351CutoffAverageCommutation\nset_option pp.universes true\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadCutoffAverageAnticommutation.lean',"""import TGLExt.V351CutoffAverageCommutation
open TGLExt TGLV350.Regular
example (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) (δ : ℝ) :
    hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) * regularAverage P δ =
      -(regularAverage P δ * hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) := by
  exact (regularInverseCutoffSqrt_commutes_average P ε hε δ).eq
""")
for old,new in [('run_perturbed_weight_order_replay.py','run_cutoff_average_commutation_replay.py'),('audit_perturbed_weight_order.py','audit_cutoff_average_commutation.py'),('validate_perturbed_weight_order.py','validate_cutoff_average_commutation.py')]:
 t=(R/old).read_text(encoding='utf8')
 for a,b in [('perturbed_weight_order','cutoff_average_commutation'),('V351PerturbedWeightOrder','V351CutoffAverageCommutation'),('AuditA1PerturbedWeightOrder','AuditA1CutoffAverageCommutation'),('PERTURBED_WEIGHT_ORDER','CUTOFF_AVERAGE_COMMUTATION'),('BadPerturbedWeightOrderReversed','BadCutoffAverageAnticommutation'),('AUDITORIA_ORDEM_PESO_PERTURBADO_A1B','AUDITORIA_COMUTACAO_CORTES_MEDIAS_A1B'),('AUDITORIA_NORMA_PESO_PERTURBADO_A1B','AUDITORIA_RECUPERACAO_MEDIAS_A1B')]:t=t.replace(a,b)
 t=t.replace("len(targets)==1 and sum(t['kind']=='theorem' for t in targets)==1","len(targets)==3 and sum(t['kind']=='theorem' for t in targets)==3")
 t=t.replace('new_theorems=1,','new_theorems=3,')
 t=t.replace('perturbed_order_on_existing_weight_domain=True','original_cutoff_roots_commute_with_original_averages=True')
 put(R/new,t)
print(names)

