from pathlib import Path
import os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
s=(K/'TGLExt/V351RegularSpectralGraph.lean').read_text(encoding='utf8')
decls=re.findall(r'^(def|theorem) (\w+)',s,re.M)
assert len(decls)==3 and all(d[0]=='theorem' for d in decls)
audit='import TGLExt.V351RegularSpectralGraph\nset_option pp.universes true\n'
for kind,name in decls:audit+=f'#check TGLV350.Regular.{name}\n#print axioms TGLV350.Regular.{name}\n'
put(K/'TGLExt/AuditA1SpectralGraph.lean',audit.encode('utf8'))
bad='''import TGLExt.V351RegularSpectralGraph
open TGLExt TGLV350.Regular MeasureTheory
example (P : SiteProfile) (x y : RegularHilbert (TowerHilbert P)) :
    (x,y) ∈ (regularPositiveGenerator P).graph ↔
      ∀ᵐ ξ ∂volume, ((regularSpectralCoordinates P).symm y) ξ =
        (Real.exp (2*Real.pi*ξ) : ℂ) • ((regularSpectralCoordinates P).symm x) ξ := by
  exact regularPositiveGenerator_graph_iff P x y
'''
put(R/'probes/BadSpectralGeneratorSign.lean',bad.encode('utf8'))
run=(R/'run_positive_graph_replay.py').read_text(encoding='utf8')
for a,b in [('AUDITORIA_FOURIER_TRANSLACAO_A1B','AUDITORIA_GRAFO_POSITIVO_A1B'),('V351RegularPositiveGraph','V351RegularSpectralGraph'),('AuditA1PositiveGraph','AuditA1SpectralGraph'),('positive_graph_attempts','spectral_graph_attempts')]:run=run.replace(a,b)
put(R/'run_spectral_graph_replay.py',run.encode('utf8'))
audit=(R/'audit_positive_graph.py').read_text(encoding='utf8')
for a,b in [('V351RegularPositiveGraph','V351RegularSpectralGraph'),('AuditA1PositiveGraph','AuditA1SpectralGraph'),('BadPositiveGeneratorBound','BadSpectralGeneratorSign'),('positive_graph_attempts','spectral_graph_attempts'),('audit_positive_graph','audit_spectral_graph'),('len(targets)==15','len(targets)==3'),("t['kind']=='theorem' for t in targets)==12","t['kind']=='theorem' for t in targets)==3"),('AUTHOR_STANDALONE_POSITIVE_GRAPH_PASS__POWERS_AFFILIATION_TRACE_OPEN','AUTHOR_STANDALONE_SPECTRAL_GRAPH_PASS__POWERS_AFFILIATION_TRACE_OPEN'),('new_theorems=12','new_theorems=3'),('new_definitions=3','new_definitions=0'),('AUDITORIA_GRAFO_POSITIVO_A1B','AUDITORIA_GRAFO_ESPECTRAL_A1B')]:audit=audit.replace(a,b)
audit=audit.replace('positive_graph_constructed=True, regular_generator_identification_proved=False','spectral_graph_identified=True, regular_generator_powers_identified=False')
put(R/'audit_spectral_graph.py',audit.encode('utf8'))
wait=(R/'validate_positive_graph.py').read_text(encoding='utf8')
for a,b in [('positive_graph','spectral_graph'),('AUDITORIA_FOURIER_TRANSLACAO_A1B','AUDITORIA_GRAFO_POSITIVO_A1B'),('AUTHOR_POSITIVE_GRAPH','AUTHOR_SPECTRAL_GRAPH')]:wait=wait.replace(a,b)
# Detect a failed predecessor as well as the earlier sequential-chain failure.
wait=wait.replace("if failed.exists():", "if failed.exists() or any((R/'positive_graph_validation').glob('*/blocked.json')) or any(__import__('json').loads(p.read_text(encoding='utf8')).get('returncode',0) != 0 for p in (R/'positive_graph_validation').glob('*/*.json') if p.name in ('build.json','audit.json')):")
put(R/'validate_spectral_graph.py',wait.encode('utf8'))
print('Prepared3theorems0definitions')
