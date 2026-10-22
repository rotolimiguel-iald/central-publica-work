from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
s=(K/'TGLExt/V351ScalarMultiplierCalculus.lean').read_text(encoding='utf8')
decls=re.findall(r'^(def|theorem) (\w+)',s,re.M)
assert len(decls)==5 and sum(d[0]=='theorem' for d in decls)==3
audit='import TGLExt.V351ScalarMultiplierCalculus\nset_option pp.universes true\n'
for kind,name in decls:audit+=f'#check TGLV350.Regular.{name}\n#print axioms TGLV350.Regular.{name}\n'
put(K/'TGLExt/AuditA1MultiplierCalculus.lean',audit.encode('utf8'))
bad='''import TGLExt.V351ScalarMultiplierCalculus
open TGLExt TGLV350.Regular MeasureTheory
example (g : ℝ → ℝ) (hg : Continuous g) (h0 : ∀ x, 0 ≤ g x) (h1 : ∀ x, g x ≤ 1)
    (f : ℂ → ℂ) (hf : Continuous f) (u : RegularHilbert ℂ) :
    cfc f (realScalarMultiplier g hg h0 h1) u =ᵐ[volume]
      fun x => (2 * f (g x : ℂ)) • u x := by
  exact realScalarMultiplier_cfc_ae g hg h0 h1 f hf u
'''
put(R/'probes/BadMultiplierCalculusFactor.lean',bad.encode('utf8'))
run=(R/'run_spectral_graph_replay.py').read_text(encoding='utf8')
for a,b in [('AUDITORIA_GRAFO_POSITIVO_A1B','AUDITORIA_GRAFO_ESPECTRAL_A1B'),('V351RegularSpectralGraph','V351ScalarMultiplierCalculus'),('AuditA1SpectralGraph','AuditA1MultiplierCalculus'),('spectral_graph_attempts','multiplier_calculus_attempts')]:run=run.replace(a,b)
put(R/'run_multiplier_calculus_replay.py',run.encode('utf8'))
audit=(R/'audit_spectral_graph.py').read_text(encoding='utf8')
for a,b in [('V351RegularSpectralGraph','V351ScalarMultiplierCalculus'),('AuditA1SpectralGraph','AuditA1MultiplierCalculus'),('BadSpectralGeneratorSign','BadMultiplierCalculusFactor'),('spectral_graph_attempts','multiplier_calculus_attempts'),('audit_spectral_graph','audit_multiplier_calculus'),('len(targets)==3','len(targets)==5'),('AUTHOR_STANDALONE_SPECTRAL_GRAPH_PASS__POWERS_AFFILIATION_TRACE_OPEN','AUTHOR_STANDALONE_MULTIPLIER_CALCULUS_PASS__POWERS_AFFILIATION_TRACE_OPEN'),('new_definitions=0','new_definitions=2'),('AUDITORIA_GRAFO_ESPECTRAL_A1B','AUDITORIA_CALCULO_MULTIPLICADOR_A1B')]:audit=audit.replace(a,b)
audit=audit.replace('spectral_graph_identified=True, regular_generator_powers_identified=False','multiplier_calculus_identified=True, regular_generator_powers_identified=False')
put(R/'audit_multiplier_calculus.py',audit.encode('utf8'))
wait=(R/'validate_spectral_graph.py').read_text(encoding='utf8')
for a,b in [('spectral_graph','multiplier_calculus'),('AUDITORIA_GRAFO_POSITIVO_A1B','AUDITORIA_GRAFO_ESPECTRAL_A1B'),('AUTHOR_SPECTRAL_GRAPH','AUTHOR_MULTIPLIER_CALCULUS')]:wait=wait.replace(a,b)
put(R/'validate_multiplier_calculus.py',wait.encode('utf8'))
print('Prepared5declarations3theorems2defs')
