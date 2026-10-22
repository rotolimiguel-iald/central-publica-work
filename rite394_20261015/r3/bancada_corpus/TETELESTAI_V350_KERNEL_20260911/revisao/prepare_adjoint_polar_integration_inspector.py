from pathlib import Path
REV = Path(__file__).resolve().parent
s = (REV / 'inspect_right_graph_core_integration_static.py').read_text(encoding='utf-8')
for a,b in [('right_graph_core','adjoint_polar_graph'),('RIGHT_GRAPH_CORE','ADJOINT_POLAR_GRAPH'),
            ('scalar_vna','right_graph_core'),('RELATORIO_GRAPH_CORE_ADJUNTO_ORIGINAL_F','RELATORIO_ADJUNTO_POLAR_GRAFOS_ORIGINAIS'),
            ('exact_57_targets','exact_17_targets'),('909','911'),('6982','7039'),('==7039','==7056'),
            ('==57','==17'),("'source_Audit_added':57","'source_Audit_added':17"),('all_six_literal_import_rewrites','all_two_literal_import_rewrites')]:
    s=s.replace(a,b)
s=s.replace("C['inherited_sources_binaries_preserved'] and C['new_binary_equals_author']", "C['inherited_first_preserved'] and C['new_binary_equal_author']")
s=s.replace("assert D==load(DEV/'final_documents/adjoint_polar_graph_draft_status.json') and D['report_sha256']==hf(OUT/'RELATORIO_ADJUNTO_POLAR_GRAFOS_ORIGINAIS_DEV.md')", "assert hf(ROOT/'adjoint_polar_graph_draft_status.json')==M['document_pins'][str(ROOT/'adjoint_polar_graph_draft_status.json')] and D['report_sha256']==hf(OUT/'RELATORIO_ADJUNTO_POLAR_GRAFOS_ORIGINAIS_DEV.md')")
s=s.replace("for name,pin in HS['helpers'].items():\n assert hf(ROOT/name)==pin['sha256'];ast.parse((ROOT/name).read_bytes());helpers[name]=pin", "for name in files:\n if 'adjoint_polar_graph' in name and name.endswith('.py'):\n  ast.parse((ROOT/name).read_bytes());helpers[name]={'sha256':hf(ROOT/name),'inspection':'static_only_no_execution'}")
# The parent has 7039 declarations; the current source has 7056.
s=s.replace("len(set(oldnames))==P['audit_declarations']==7056", "len(set(oldnames))==P['audit_declarations']==7039")
p=REV/'inspect_adjoint_polar_graph_integration_static.py'
assert not p.exists()
b=s.encode('utf-8');q=p.with_suffix('.py.tmp')
with q.open('xb') as f:f.write(b)
assert q.read_bytes()==b;q.replace(p)
print(str(p))
