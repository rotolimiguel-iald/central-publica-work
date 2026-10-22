from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
    assert not p.exists() and p.is_relative_to(R),p
    b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
names=re.findall(r'^theorem (\w+)',(K/'TGLExt/V351InverseLimitSemifiniteness.lean').read_text(encoding='utf8'),re.M);assert len(names)==3
put(K/'TGLExt/AuditA1InverseLimitSemifiniteness.lean','import TGLExt.V351InverseLimitSemifiniteness\nset_option pp.universes true\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadLimitSemifiniteInfiniteCut.lean','''import TGLExt.V351InverseLimitSemifiniteness
open TGLExt TGLV350.Regular
open scoped ENNReal
example (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) (a : scalarWeightLeftIdeal P) :
    scalarInverseLimitWeight P (TGLV351.positiveSquare P (a.val*regularDomainCut P δ)) = ⊤ := by
  exact scalarInverseLimitWeight_domainCut_finite P δ hδ a
''')
for kind in ['run','audit','validate']:
    old=('run_inverse_limit_scaling_replay.py' if kind=='run' else kind+'_inverse_limit_scaling.py')
    new=old.replace('inverse_limit_scaling','inverse_limit_semifinite')
    s=(R/old).read_text(encoding='utf8')
    for a,b in [('inverse_limit_scaling','inverse_limit_semifinite'),('V351InverseLimitScaling','V351InverseLimitSemifiniteness'),('AuditA1InverseLimitScaling','AuditA1InverseLimitSemifiniteness'),('INVERSE_LIMIT_SCALING','INVERSE_LIMIT_SEMIFINITE'),('BadInverseLimitScalingSign','BadLimitSemifiniteInfiniteCut'),('AUDITORIA_ESCALA_PESO_LIMITE_A1B','AUDITORIA_SEMIFINITUDE_PESO_LIMITE_A1B'),('AUDITORIA_FIDELIDADE_PESO_LIMITE_A1B','AUDITORIA_CORTE_DOMINIO_A1B')]:s=s.replace(a,b)
    s=s.replace("len(targets)==4 and sum(t['kind']=='theorem' for t in targets)==4","len(targets)==3 and sum(t['kind']=='theorem' for t in targets)==3")
    s=s.replace('new_theorems=4','new_theorems=3').replace('constructed_limit_weight_dual_scaling=True','constructed_limit_weight_usual_semifinite=True')
    put(R/new,s)
print(names)
