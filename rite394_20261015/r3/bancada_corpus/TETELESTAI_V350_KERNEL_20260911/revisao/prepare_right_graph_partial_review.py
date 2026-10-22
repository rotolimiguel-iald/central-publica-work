from pathlib import Path
import ast
REV=Path(__file__).resolve().parent
t=(REV/'run_scalar_vna_partial_review.py').read_text(encoding='utf-8')
t=t.replace("'scalar_vna_partial_independent_'", "'right_graph_partial_independent_'")
t=t.replace("Path((REV/'right_vector_final_latest_run.txt').read_text().strip())]", "Path((REV/'right_vector_final_latest_run.txt').read_text().strip()),Path((REV/'scalar_vna_final_latest_run.txt').read_text().strip())]")
t=t.replace('right_vector_custody','scalar_vna_custody').replace('REVIEW_RIGHT_VECTOR_DEV.md','REVIEW_SCALAR_VNA_DEV.md').replace('REVIEW_RIGHT_VECTOR_INTEGRATED.md','REVIEW_SCALAR_VNA_INTEGRATED.md')
a=t.index('spec=[');b=t.index('\nsources=',a)
t=t[:a]+"spec=[('ComplexGraphProjection','20260913_012424_268265',12),('ScalarRightMultiplicationGraph','20260913_012642_923549',10)]"+t[b:]
t=t.replace('==17','==22').replace('PARTIAL_THREE_MODULES_ONLY','PARTIAL_TWO_MODULES_ONLY_22_TARGETS')
t=t.replace('ScalarVNAPartialAudit','RightGraphPartialAudit').replace("'scalar_vna_partial_latest_run.txt'", "'right_graph_partial_latest_run.txt'")
t=t.replace('len(records)==4','len(records)==3').replace('exact_17_targets','exact_22_targets').replace('three_binaries_equal_author','two_binaries_equal_author').replace('len(records)>=3','len(records)>=2').replace('records[:3]','records[:2]')
t=t.replace("external=m['external_direct_pins']", """external=dict(m['external_direct_pins'])
mathlibbuild=next(Path(p) for p in pkg if '\\\\mathlib\\\\' in p)
for name in sorted({i for b in raws.values() for i in imports(b) if i.startswith('Mathlib.')}):
    rel=Path(*name.split('.'));src=mathlibbuild.parents[3]/rel.with_suffix('.lean');binary=mathlibbuild/rel.with_suffix('.olean')
    external[name]={'source':str(src),'source_sha256':hf(src),'binary':str(binary),'binary_sha256':hf(binary)}""")
ast.parse(t);out=REV/'run_right_graph_partial_review.py';assert not out.exists()
raw=t.encode();tmp=out.with_name(out.name+'.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;tmp.replace(out);print(out)
