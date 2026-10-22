from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
    assert not p.exists() and p.is_relative_to(R),p
    b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
names=re.findall(r'^theorem (\w+)',(K/'TGLExt/V351InverseLimitFaithful.lean').read_text(encoding='utf8'),re.M);assert len(names)==2
put(K/'TGLExt/AuditA1InverseLimitFaithful.lean','import TGLExt.V351InverseLimitFaithful\nset_option pp.universes true\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadInverseLimitFaithfulNegated.lean','''import TGLExt.V351InverseLimitFaithful
open TGLExt TGLV350.Regular
example (P : SiteProfile) (X : PositiveCoreInput P) :
    scalarInverseLimitWeight P X = 0 ↔ X ≠ PositiveCoreInput.zero P := by
  exact scalarInverseLimitWeight_faithful P X
''')
for old,new in [('run_all_positive_weight_order_replay.py','run_inverse_limit_faithful_replay.py'),('audit_all_positive_weight_order.py','audit_inverse_limit_faithful.py'),('validate_all_positive_weight_order.py','validate_inverse_limit_faithful.py')]:
    t=(R/old).read_text(encoding='utf8')
    for a,b in [('all_positive_weight_order','inverse_limit_faithful'),('V351AllPositiveWeightOrder','V351InverseLimitFaithful'),('AuditA1AllPositiveWeightOrder','AuditA1InverseLimitFaithful'),('ALL_POSITIVE_WEIGHT_ORDER','INVERSE_LIMIT_FAITHFUL'),('BadAllPositiveWeightOrderReversed','BadInverseLimitFaithfulNegated'),('AUDITORIA_ORDEM_TODOS_POSITIVOS_A1B','AUDITORIA_FIDELIDADE_PESO_LIMITE_A1B'),('AUDITORIA_COMUTACAO_CORTES_MEDIAS_A1B','AUDITORIA_LEIS_PESO_LIMITE_A1B')]:t=t.replace(a,b)
    t=t.replace('all_positive_comparison_under_named_commutation=True','constructed_limit_weight_faithful=True')
    put(R/new,t)
print(names)
