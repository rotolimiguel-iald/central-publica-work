from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
    assert not p.exists() and p.is_relative_to(R),p
    b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
names=re.findall(r'^theorem (\w+)',(K/'TGLExt/V351InverseLimitScaling.lean').read_text(encoding='utf8'),re.M);assert len(names)==4
put(K/'TGLExt/AuditA1InverseLimitScaling.lean','import TGLExt.V351InverseLimitScaling\nset_option pp.universes true\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadInverseLimitScalingSign.lean','''import TGLExt.V351InverseLimitScaling
open TGLExt TGLV350.Regular
open scoped ENNReal
example (P : SiteProfile) (s : ℝ) (X : PositiveCoreInput P) :
    scalarInverseLimitWeight P (TGLV351.positiveDual P s X) =
      ENNReal.ofReal (Real.exp s) * scalarInverseLimitWeight P X := by
  exact scalarInverseLimitWeight_dual P s X
''')
for kind in ['run','audit','validate']:
    old=(f'run_inverse_limit_faithful_replay.py' if kind=='run' else kind+'_inverse_limit_faithful.py')
    new=old.replace('inverse_limit_faithful','inverse_limit_scaling')
    s=(R/old).read_text(encoding='utf8')
    for a,b in [('inverse_limit_faithful','inverse_limit_scaling'),('V351InverseLimitFaithful','V351InverseLimitScaling'),('AuditA1InverseLimitFaithful','AuditA1InverseLimitScaling'),('INVERSE_LIMIT_FAITHFUL','INVERSE_LIMIT_SCALING'),('BadInverseLimitFaithfulNegated','BadInverseLimitScalingSign'),('AUDITORIA_FIDELIDADE_PESO_LIMITE_A1B','AUDITORIA_ESCALA_PESO_LIMITE_A1B'),('AUDITORIA_LEIS_PESO_LIMITE_A1B','AUDITORIA_FIDELIDADE_PESO_LIMITE_A1B')]:s=s.replace(a,b)
    s=s.replace("len(targets)==2 and sum(t['kind']=='theorem' for t in targets)==2","len(targets)==4 and sum(t['kind']=='theorem' for t in targets)==4")
    s=s.replace('new_theorems=2','new_theorems=4').replace('constructed_limit_weight_faithful=True','constructed_limit_weight_dual_scaling=True')
    put(R/new,s)
print(names)
