from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
 assert not p.exists() and p.is_relative_to(R),p
 b=s.encode('utf8');q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
names=re.findall(r'^theorem (\w+)',(K/'TGLExt/V351PerturbedWeightNorm.lean').read_text(encoding='utf8'),re.M)
assert len(names)==2
put(K/'TGLExt/AuditA1PerturbedWeightNorm.lean','import TGLExt.V351PerturbedWeightNorm\nset_option pp.universes true\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadPerturbedWeightWithoutJ.lean',"""import TGLExt.V351PerturbedWeightNorm
open TGLExt TGLV350.Regular
example (P : SiteProfile)
    (b : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (A : scalarWeightLeftIdeal P) :
    dualQuadraticIntegral (star b.val * (star A.val.val*A.val.val) * b.val)
      (regularVacuum P) =
    ENNReal.ofReal (‖scalarGNSRepresentation P (star b)
      (scalarWeightGNSEmbedding P A)‖^2) := by
  exact scalarWeight_right_perturbed_norm P b hb A
""")
for old,new in [('run_cutoff_cfc_replay.py','run_perturbed_weight_norm_replay.py'),('audit_cutoff_cfc.py','audit_perturbed_weight_norm.py'),('validate_cutoff_cfc.py','validate_perturbed_weight_norm.py')]:
 t=(R/old).read_text(encoding='utf8')
 for a,b in [('cutoff_cfc','perturbed_weight_norm'),('V351InverseCutoffCFC','V351PerturbedWeightNorm'),('AuditA1CutoffCFC','AuditA1PerturbedWeightNorm'),('CUTOFF_CFC','PERTURBED_WEIGHT_NORM'),('BadCutoffCFCMirror','BadPerturbedWeightWithoutJ'),('AUDITORIA_CFC_CORTES_A1B','AUDITORIA_NORMA_PESO_PERTURBADO_A1B'),('AUDITORIA_APROXIMANTES_SENO_A1B','AUDITORIA_CFC_CORTES_A1B')]:t=t.replace(a,b)
 t=t.replace("len(targets)==7 and sum(t['kind']=='theorem' for t in targets)==6","len(targets)==2 and sum(t['kind']=='theorem' for t in targets)==2")
 t=t.replace('new_theorems=6, new_definitions=1, private_theorems=2, private_definitions=0','new_theorems=2, new_definitions=0, private_theorems=0, private_definitions=0')
 t=t.replace('new_theorems=6,new_definitions=1,private_theorems=2,private_definitions=0','new_theorems=2,new_definitions=0,private_theorems=0,private_definitions=0')
 t=t.replace('actual_cutoff_cfc_identified=True, actual_cutoff_root_right_action_proved=True','perturbed_values_on_existing_weight_domain=True, all_positive_extension_proved=False')
 put(R/new,t)
print(names)

