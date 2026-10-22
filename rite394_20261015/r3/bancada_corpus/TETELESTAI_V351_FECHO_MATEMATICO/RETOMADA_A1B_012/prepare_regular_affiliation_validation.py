from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
s=(K/'TGLExt/V351RegularGeneratorAffiliation.lean').read_text(encoding='utf8')
decls=re.findall(r'^(def|theorem) (\w+)',s,re.M)
assert len(decls)==3 and all(d[0]=='theorem' for d in decls)
audit='import TGLExt.V351RegularGeneratorAffiliation\nset_option pp.universes true\n'
for kind,name in decls:audit+=f'#check TGLV350.Regular.{name}\n#print axioms TGLV350.Regular.{name}\n'
put(K/'TGLExt/AuditA1RegularAffiliation.lean',audit.encode('utf8'))
bad='''import TGLExt.V351RegularGeneratorAffiliation
open TGLExt TGLV350.Regular
example (P : SiteProfile)
    (B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hB : B ∈ (regularCoreAlgebra P).commutant)
    (x y : RegularHilbert (TowerHilbert P))
    (hxy : (x,y) ∈ (regularPositiveGenerator P).graph) :
    (B x,2 • B y) ∈ (regularPositiveGenerator P).graph := by
  exact regularPositiveGenerator_commutant_graph P B hB x y hxy
'''
put(R/'probes/BadAffiliationGraphFactor.lean',bad.encode('utf8'))
run=(R/'run_regular_powers_replay.py').read_text(encoding='utf8')
for a,b in [('AUDITORIA_CALCULO_MULTIPLICADOR_A1B','AUDITORIA_POTENCIAS_REGULARES_A1B'),('V351RegularImaginaryPowers','V351RegularGeneratorAffiliation'),('AuditA1RegularPowers','AuditA1RegularAffiliation'),('regular_powers_attempts','regular_affiliation_attempts')]:run=run.replace(a,b)
put(R/'run_regular_affiliation_replay.py',run.encode('utf8'))
audit=(R/'audit_regular_powers.py').read_text(encoding='utf8')
for a,b in [('V351RegularImaginaryPowers','V351RegularGeneratorAffiliation'),('AuditA1RegularPowers','AuditA1RegularAffiliation'),('BadRegularPowerTime','BadAffiliationGraphFactor'),('regular_powers_attempts','regular_affiliation_attempts'),('audit_regular_powers','audit_regular_affiliation'),('len(targets)==4','len(targets)==3'),("t['kind']=='theorem' for t in targets)==4","t['kind']=='theorem' for t in targets)==3"),('AUTHOR_STANDALONE_REGULAR_POWERS_PASS__AFFILIATION_TRACE_OPEN','AUTHOR_STANDALONE_REGULAR_AFFILIATION_PASS__DUAL_SCALING_TRACE_OPEN'),('new_theorems=4','new_theorems=3'),('AUDITORIA_POTENCIAS_REGULARES_A1B','AUDITORIA_AFILIACAO_REGULAR_A1B')]:audit=audit.replace(a,b)
audit=audit.replace('regular_generator_powers_identified=True, regular_generator_affiliation_proved=False','regular_generator_affiliation_proved=True, regular_generator_dual_scaling_proved=False')
put(R/'audit_regular_affiliation.py',audit.encode('utf8'))
wait=(R/'validate_regular_powers.py').read_text(encoding='utf8')
for a,b in [('regular_powers','regular_affiliation'),('AUDITORIA_CALCULO_MULTIPLICADOR_A1B','AUDITORIA_POTENCIAS_REGULARES_A1B'),('AUTHOR_REGULAR_POWERS','AUTHOR_REGULAR_AFFILIATION')]:wait=wait.replace(a,b)
put(R/'validate_regular_affiliation.py',wait.encode('utf8'))
print('Prepared3theorems0defs')
