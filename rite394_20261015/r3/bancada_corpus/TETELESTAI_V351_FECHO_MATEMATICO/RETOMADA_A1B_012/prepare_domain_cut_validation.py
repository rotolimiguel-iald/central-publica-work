from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
    assert not p.exists() and p.is_relative_to(R),p
    b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
names=re.findall(r'^(?:def|theorem) (\w+)',(K/'TGLExt/V351RegularDomainCut.lean').read_text(encoding='utf8'),re.M);assert len(names)==7
put(K/'TGLExt/AuditA1RegularDomainCut.lean','import TGLExt.V351RegularDomainCut\nset_option pp.universes true\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadDomainCutProductReversed.lean','''import TGLExt.V351RegularDomainCut
open TGLExt TGLV350.Regular
example (P : SiteProfile) (ε δ : ℝ) (hε : 0 < ε) (hδ : 0 < δ) :
    (δ⁻¹ : ℂ) • 1 ≤ regularInverseGeneratorCutoff P ε *
      (regularDomainCut P δ).val * (regularDomainCut P δ).val := by
  exact regularDomainCut_product_bound P ε δ hε hδ
''')
for kind in ['run','audit','validate']:
    old=('run_inverse_limit_scaling_replay.py' if kind=='run' else kind+'_inverse_limit_scaling.py')
    new=old.replace('inverse_limit_scaling','domain_cut')
    s=(R/old).read_text(encoding='utf8')
    for a,b in [('inverse_limit_scaling','domain_cut'),('V351InverseLimitScaling','V351RegularDomainCut'),('AuditA1InverseLimitScaling','AuditA1RegularDomainCut'),('INVERSE_LIMIT_SCALING','DOMAIN_CUT'),('BadInverseLimitScalingSign','BadDomainCutProductReversed'),('AUDITORIA_ESCALA_PESO_LIMITE_A1B','AUDITORIA_CORTE_DOMINIO_A1B'),('AUDITORIA_FIDELIDADE_PESO_LIMITE_A1B','AUDITORIA_ESCALA_PESO_LIMITE_A1B')]:s=s.replace(a,b)
    s=s.replace("len(targets)==4 and sum(t['kind']=='theorem' for t in targets)==4","len(targets)==7 and sum(t['kind']=='theorem' for t in targets)==6")
    s=s.replace('new_theorems=4','new_theorems=6').replace('new_definitions=0','new_definitions=1').replace('private_theorems=1','private_theorems=4').replace('constructed_limit_weight_dual_scaling=True','domain_cut_uniform_bound_and_strong_limit=True')
    put(R/new,s)
print(names)
