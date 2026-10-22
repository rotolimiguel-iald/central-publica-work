"""Adapt a reviewer-owned read-only checker; no author code is run."""
from pathlib import Path
import ast
R=Path(__file__).resolve().parent
t=(R/'review_gaussian_polar_integration.py').read_text(encoding='utf-8')
# Rename stage-specific filenames and identifiers before switching the parent.
t=t.replace('gaussian_polar','right_regularization').replace('GAUSSIAN_POLAR','RIGHT_REGULARIZATION')
t=t.replace('POLAR_GAUSSIANO_CICLICO','REGULARIZACAO_COMUTANTE')
t=t.replace('core_polar','gaussian_polar')
t=t.replace("V['dependency_manifest_sha256']", "V['manifest_sha256']")
for a,b in [
    ('four-module','two-module'),('all_four_import_rewrites_literal','all_two_import_rewrites_literal'),
    ("len(M['sources'])==4", "len(M['sources'])==2"),
    ('len(ownax)==34','len(ownax)==19'),
    ('==891','==893'),("'embedded_files':891","'embedded_files':893"),
    ('==6848','==6882'),('==6882','==6901'),
    ("'source_Audit_distinct':6882", "'source_Audit_distinct':6901"),
    ("'source_Audit_added':34", "'source_Audit_added':19"),
    ('len(rows)==189','len(rows)==191'),
    ("for r in rows)==183", "for r in rows)==187"),
    ('len(changed)==6','len(changed)==4'),('rows[-6:]','rows[-4:]'),
    ('G[\'passed\']==97', 'G[\'passed\']==98'),
    ("'integrated_records':189", "'integrated_records':191"),
    ("'unchanged_parent_records':183", "'unchanged_parent_records':187"),
    ("'new_author_compilations':6", "'new_author_compilations':4"),
    ("'new_axioms_equal_own_DEV':34", "'new_axioms_equal_own_DEV':19"),
    ("'audit_distinct':6882", "'audit_distinct':6901"),
    ("'gate_passed_author_records':97", "'gate_passed_author_records':98"),
    ('gaussian_unitary_and_same_GNS_cyclic_separating_vector_does_not_discharge_KMS_trace_or_physical_frontier',
     'full_weight_right_regularization_and_commutant_approximation_does_not_discharge_KMS_trace_or_physical_frontier'),
]:
    assert a in t, a
    t=t.replace(a,b)
# Avoid cascading the two parent/current Audit substitutions above.
t=t.replace("P['audit_declarations']==6901", "P['audit_declarations']==6882")
t=t.replace('len(oldax)==6901', 'len(oldax)==6882')
ast.parse(t)
p=R/'review_right_regularization_integration.py'
assert not p.exists()
raw=t.encode('utf-8');q=p.with_name(p.name+'.tmp')
with q.open('xb') as f:f.write(raw)
assert q.read_bytes()==raw
q.replace(p)
print(p)
