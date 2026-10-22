from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
    assert not p.exists() and p.is_relative_to(R),p
    b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
names=re.findall(r'^theorem (\w+)',(K/'TGLExt/V351AllPositiveWeightOrder.lean').read_text(encoding='utf8'),re.M);assert len(names)==2
put(K/'TGLExt/AuditA1AllPositiveWeightOrder.lean','import TGLExt.V351AllPositiveWeightOrder\nset_option pp.universes true\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadAllPositiveWeightOrderReversed.lean','''import TGLExt.V351AllPositiveWeightOrder
open TGLExt TGLV350.Regular
example (P : SiteProfile) (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (hc : c ∈ scalarPolarRightAlgebra P)
    (hbc : b * star b ≤ c * star c)
    (hbe : ∀ δ : ℝ, Commute b.val (regularAverage P δ))
    (hce : ∀ δ : ℝ, Commute c.val (regularAverage P δ)) (X : PositiveCoreInput P) :
    dualQuadraticIntegral (star c.val * X.val * c.val) (regularVacuum P) ≤
      dualQuadraticIntegral (star b.val * X.val * b.val) (regularVacuum P) := by
  exact scalarWeight_right_perturbed_mono_all_positive P b c hb hc hbc hbe hce X
''')
for old,new in [('run_cutoff_average_commutation_replay.py','run_all_positive_weight_order_replay.py'),('audit_cutoff_average_commutation.py','audit_all_positive_weight_order.py'),('validate_cutoff_average_commutation.py','validate_all_positive_weight_order.py')]:
    t=(R/old).read_text(encoding='utf8')
    for a,b in [('cutoff_average_commutation','all_positive_weight_order'),('V351CutoffAverageCommutation','V351AllPositiveWeightOrder'),('AuditA1CutoffAverageCommutation','AuditA1AllPositiveWeightOrder'),('CUTOFF_AVERAGE_COMMUTATION','ALL_POSITIVE_WEIGHT_ORDER'),('BadCutoffAverageAnticommutation','BadAllPositiveWeightOrderReversed'),('AUDITORIA_COMUTACAO_CORTES_MEDIAS_A1B','AUDITORIA_ORDEM_TODOS_POSITIVOS_A1B'),('AUDITORIA_RECUPERACAO_MEDIAS_A1B','AUDITORIA_COMUTACAO_CORTES_MEDIAS_A1B')]:t=t.replace(a,b)
    t=t.replace("len(targets)==3 and sum(t['kind']=='theorem' for t in targets)==3","len(targets)==2 and sum(t['kind']=='theorem' for t in targets)==2")
    t=t.replace('new_theorems=3,','new_theorems=2,')
    t=t.replace('actual_all_positive_weight_order_identified=True','all_positive_comparison_under_named_commutation=True')
    put(R/new,t)
print(names)
