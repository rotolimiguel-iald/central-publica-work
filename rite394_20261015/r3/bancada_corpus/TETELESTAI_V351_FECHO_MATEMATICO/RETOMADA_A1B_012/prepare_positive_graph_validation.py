from pathlib import Path
import hashlib,json,os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
s=(K/'TGLExt/V351RegularPositiveGraph.lean').read_text(encoding='utf8')
decls=re.findall(r'^(def|theorem) (\w+)',s,re.M)
assert len(decls)==15 and sum(d[0]=='theorem' for d in decls)==12
audit='import TGLExt.V351RegularPositiveGraph\nset_option pp.universes true\n'
for kind,name in decls:audit+=f'#check TGLV350.Regular.{name}\n#print axioms TGLV350.Regular.{name}\n'
put(K/'TGLExt/AuditA1PositiveGraph.lean',audit.encode('utf8'))
bad='''import TGLExt.V351RegularPositiveGraph
open TGLExt TGLV350.Regular
example (P : SiteProfile) : regularSpectralResolvent P ≤ 0 := by
  exact regularSpectralResolvent_le_one P
'''
put(R/'probes/BadPositiveGeneratorBound.lean',bad.encode('utf8'))
run=(R/'run_absorption_replay.py').read_text(encoding='utf8')
for a,b in [('AUDITORIA_ACAO_CORE_A1B','AUDITORIA_FOURIER_TRANSLACAO_A1B'),('V351RegularFlowAbsorption','V351RegularPositiveGraph'),('AuditA1Absorption','AuditA1PositiveGraph'),('absorption_attempts','positive_graph_attempts')]:run=run.replace(a,b)
put(R/'run_positive_graph_replay.py',run.encode('utf8'))
audit=(R/'audit_absorption.py').read_text(encoding='utf8')
for a,b in [('V351RegularFlowAbsorption','V351RegularPositiveGraph'),('AuditA1Absorption','AuditA1PositiveGraph'),('BadAbsorptionTime','BadPositiveGeneratorBound'),('absorption_attempts','positive_graph_attempts'),('audit_absorption','audit_positive_graph'),('len(targets)==6','len(targets)==15'),("t['kind']=='theorem' for t in targets)==4","t['kind']=='theorem' for t in targets)==12"),('AUTHOR_STANDALONE_ABSORPTION_PASS__POSITIVE_GENERATOR_AND_TRACE_OPEN','AUTHOR_STANDALONE_POSITIVE_GRAPH_PASS__POWERS_AFFILIATION_TRACE_OPEN'),('new_theorems=4','new_theorems=12'),('new_definitions=2','new_definitions=3'),('AUDITORIA_ABSORCAO_A1B','AUDITORIA_GRAFO_POSITIVO_A1B')]:audit=audit.replace(a,b)
# Accurate distinction: graph constructed, regular-generator identification still open.
audit=audit.replace('positive_generator_constructed=False','positive_graph_constructed=True, regular_generator_identification_proved=False')
put(R/'audit_positive_graph.py',audit.encode('utf8'))
print('Prepared15declarations,12theorems3definitions')
