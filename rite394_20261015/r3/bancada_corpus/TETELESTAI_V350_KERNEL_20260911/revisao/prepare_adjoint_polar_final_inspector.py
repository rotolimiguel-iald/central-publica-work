from pathlib import Path
REV=Path(__file__).resolve().parent
s=(REV/'verify_right_graph_core_integration_final.py').read_text(encoding='utf-8')
for a,b in [('right_graph_core','adjoint_polar_graph'),('RIGHT_GRAPH_CORE','ADJOINT_POLAR_GRAPH'),('scalar_vna','right_graph_core'),
 ('== 909','== 911'),('== 57','== 17'),('== 207','== 209'),('== 199','== 205'),
 ('len(changed) == 8','len(changed) == 4'),('rows[-8:]','rows[-4:]'),('== 7039','== 7056'),('== 6982','== 7039'),
 ('== 102','== 103'),("right_pair_graph_core_equals_original_F_does_not_discharge_KMS_trace_or_physical_frontier", "original_adjoint_polar_graph_transport_does_not_discharge_KMS_trace_or_physical_frontier"),
 ("'unchanged_parent_records': 199","'unchanged_parent_records': 205"),("'new_author_compilations': 8","'new_author_compilations': 4"),
 ('all_six_literal_import_rewrites','all_two_literal_import_rewrites')]:
 s=s.replace(a,b)
p=REV/'verify_adjoint_polar_graph_integration_final.py'
assert not p.exists()
b=s.encode();q=p.with_suffix('.py.tmp')
with q.open('xb') as f:f.write(b)
assert q.read_bytes()==b;q.replace(p)
print(str(p))
