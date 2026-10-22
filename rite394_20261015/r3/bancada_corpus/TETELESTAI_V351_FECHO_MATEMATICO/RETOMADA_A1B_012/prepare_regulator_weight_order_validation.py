from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
    assert not p.exists() and p.is_relative_to(R),p
    b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
names=re.findall(r'^theorem (\w+)',(K/'TGLExt/V351RegulatorWeightOrder.lean').read_text(encoding='utf8'),re.M);assert len(names)==4
put(K/'TGLExt/AuditA1RegulatorWeightOrder.lean','import TGLExt.V351RegulatorWeightOrder\nset_option pp.universes true\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadRegulatorOrderIncreasing.lean','''import TGLExt.V351RegulatorWeightOrder
open TGLExt TGLV350.Regular
example (P : SiteProfile) (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) (hεη : ε ≤ η) :
    regularInverseGeneratorCutoff P ε ≤ regularInverseGeneratorCutoff P η := by
  exact regularInverseGeneratorCutoff_antitone P ε η hε hη hεη
''')
for old,new in [('run_all_positive_weight_order_replay.py','run_regulator_weight_order_replay.py'),('audit_all_positive_weight_order.py','audit_regulator_weight_order.py'),('validate_all_positive_weight_order.py','validate_regulator_weight_order.py')]:
    t=(R/old).read_text(encoding='utf8')
    for a,b in [('all_positive_weight_order','regulator_weight_order'),('V351AllPositiveWeightOrder','V351RegulatorWeightOrder'),('AuditA1AllPositiveWeightOrder','AuditA1RegulatorWeightOrder'),('ALL_POSITIVE_WEIGHT_ORDER','REGULATOR_WEIGHT_ORDER'),('BadAllPositiveWeightOrderReversed','BadRegulatorOrderIncreasing'),('AUDITORIA_ORDEM_TODOS_POSITIVOS_A1B','AUDITORIA_ORDEM_REGULADORES_A1B'),('AUDITORIA_COMUTACAO_CORTES_MEDIAS_A1B','AUDITORIA_ORDEM_TODOS_POSITIVOS_A1B')]:t=t.replace(a,b)
    t=t.replace("len(targets)==2 and sum(t['kind']=='theorem' for t in targets)==2","len(targets)==4 and sum(t['kind']=='theorem' for t in targets)==4")
    t=t.replace('new_theorems=2,','new_theorems=4,').replace('private_theorems=1,','private_theorems=2,')
    t=t.replace('all_positive_comparison_under_named_commutation=True','actual_regulator_order_all_positive_without_residual_commutation=True')
    put(R/new,t)
print(names)
