from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
    assert not p.exists() and p.is_relative_to(R),p
    b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
items=re.findall(r'^(def|theorem) (\w+)',(K/'TGLExt/V351InverseLimitWeight.lean').read_text(encoding='utf8'),re.M)
assert len(items)==15 and sum(k=='theorem' for k,n in items)==13
put(K/'TGLExt/AuditA1InverseLimitWeight.lean','import TGLExt.V351InverseLimitWeight\nset_option pp.universes true\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for k,n in items))
put(R/'probes/BadInverseLimitMultiplication.lean','''import TGLExt.V351InverseLimitWeight
open TGLExt TGLV350.Regular
example (P : SiteProfile) (X Y : PositiveCoreInput P) :
    scalarInverseLimitWeight P (X.add Y) = scalarInverseLimitWeight P X * scalarInverseLimitWeight P Y := by
  exact scalarInverseLimitWeight_add P X Y
''')
for old,new in [('run_regulator_weight_order_replay.py','run_inverse_limit_weight_replay.py'),('audit_regulator_weight_order.py','audit_inverse_limit_weight.py'),('validate_regulator_weight_order.py','validate_inverse_limit_weight.py')]:
    t=(R/old).read_text(encoding='utf8')
    for a,b in [('regulator_weight_order','inverse_limit_weight'),('V351RegulatorWeightOrder','V351InverseLimitWeight'),('AuditA1RegulatorWeightOrder','AuditA1InverseLimitWeight'),('REGULATOR_WEIGHT_ORDER','INVERSE_LIMIT_WEIGHT'),('BadRegulatorOrderIncreasing','BadInverseLimitMultiplication'),('AUDITORIA_ORDEM_REGULADORES_A1B','AUDITORIA_LEIS_PESO_LIMITE_A1B'),('AUDITORIA_ORDEM_TODOS_POSITIVOS_A1B','AUDITORIA_ORDEM_REGULADORES_A1B')]:t=t.replace(a,b)
    t=t.replace("len(targets)==4 and sum(t['kind']=='theorem' for t in targets)==4","len(targets)==15 and sum(t['kind']=='theorem' for t in targets)==13 and sum(t['kind']=='def' for t in targets)==2")
    t=t.replace('new_theorems=4,','new_theorems=13,').replace('new_definitions=0,','new_definitions=2,').replace('private_theorems=2,','private_theorems=0,')
    t=t.replace('actual_regulator_order_all_positive_without_residual_commutation=True','cutoff_and_limit_weight_laws=True')
    put(R/new,t)
print(items)
