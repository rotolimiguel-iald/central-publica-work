from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
s=(K/'TGLExt/V351RegularImaginaryPowers.lean').read_text(encoding='utf8')
decls=re.findall(r'^(def|theorem) (\w+)',s,re.M)
assert len(decls)==4 and all(d[0]=='theorem' for d in decls)
audit='import TGLExt.V351RegularImaginaryPowers\nset_option pp.universes true\n'
for kind,name in decls:audit+=f'#check TGLV350.Regular.{name}\n#print axioms TGLV350.Regular.{name}\n'
put(K/'TGLExt/AuditA1RegularPowers.lean',audit.encode('utf8'))
bad='''import TGLExt.V351RegularImaginaryPowers
open TGLExt TGLV350.Regular MeasureTheory
example (P : SiteProfile) (t : ℝ) (u : RegularHilbert (TowerHilbert P)) :
    resolventImaginaryPower (regularSpectralResolvent P)
      (regularSpectralResolvent_nonneg P) (regularSpectralResolvent_le_one P)
      (regularSpectralResolvent_injective P) (regularSpectralResolvent_complement_injective P)
      t u = regularUnitary P (-t) u := by
  exact regularPositiveGenerator_imaginaryPower P t u
'''
put(R/'probes/BadRegularPowerTime.lean',bad.encode('utf8'))
run=(R/'run_multiplier_calculus_replay.py').read_text(encoding='utf8')
for a,b in [('AUDITORIA_GRAFO_ESPECTRAL_A1B','AUDITORIA_CALCULO_MULTIPLICADOR_A1B'),('V351ScalarMultiplierCalculus','V351RegularImaginaryPowers'),('AuditA1MultiplierCalculus','AuditA1RegularPowers'),('multiplier_calculus_attempts','regular_powers_attempts')]:run=run.replace(a,b)
put(R/'run_regular_powers_replay.py',run.encode('utf8'))
audit=(R/'audit_multiplier_calculus.py').read_text(encoding='utf8')
for a,b in [('V351ScalarMultiplierCalculus','V351RegularImaginaryPowers'),('AuditA1MultiplierCalculus','AuditA1RegularPowers'),('BadMultiplierCalculusFactor','BadRegularPowerTime'),('multiplier_calculus_attempts','regular_powers_attempts'),('audit_multiplier_calculus','audit_regular_powers'),('len(targets)==5','len(targets)==4'),("t['kind']=='theorem' for t in targets)==3","t['kind']=='theorem' for t in targets)==4"),('AUTHOR_STANDALONE_MULTIPLIER_CALCULUS_PASS__POWERS_AFFILIATION_TRACE_OPEN','AUTHOR_STANDALONE_REGULAR_POWERS_PASS__AFFILIATION_TRACE_OPEN'),('new_theorems=3','new_theorems=4'),('new_definitions=2','new_definitions=0'),('AUDITORIA_CALCULO_MULTIPLICADOR_A1B','AUDITORIA_POTENCIAS_REGULARES_A1B')]:audit=audit.replace(a,b)
audit=audit.replace('multiplier_calculus_identified=True, regular_generator_powers_identified=False','regular_generator_powers_identified=True, regular_generator_affiliation_proved=False')
put(R/'audit_regular_powers.py',audit.encode('utf8'))
wait=(R/'validate_multiplier_calculus.py').read_text(encoding='utf8')
for a,b in [('multiplier_calculus','regular_powers'),('AUDITORIA_GRAFO_ESPECTRAL_A1B','AUDITORIA_CALCULO_MULTIPLICADOR_A1B'),('AUTHOR_MULTIPLIER_CALCULUS','AUTHOR_REGULAR_POWERS')]:wait=wait.replace(a,b)
put(R/'validate_regular_powers.py',wait.encode('utf8'))
print('Prepared4theorems0defs')
