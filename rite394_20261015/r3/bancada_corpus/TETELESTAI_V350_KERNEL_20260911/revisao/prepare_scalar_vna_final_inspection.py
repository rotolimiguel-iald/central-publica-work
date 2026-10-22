from pathlib import Path
import ast
REV=Path(__file__).resolve().parent
t=(REV/'verify_right_vector_integration_final.py').read_text(encoding='utf-8')
t=t.replace("OUT = Path((REV / 'right_vector_integrated_latest_run.txt')", "OUT = Path((REV / 'scalar_vna_integrated_latest_run.txt')")
t=t.replace("OLD = Path((REV / 'paired_right_integrated_latest_run.txt')", "OLD = Path((REV / 'right_vector_integrated_latest_run.txt')")
t=t.replace("DEV = Path((REV / 'right_vector_final_latest_run.txt')", "DEV = Path((REV / 'scalar_vna_final_latest_run.txt')")
t=t.replace("P = load(OUT / 'paired_right_custody.json')", "P = load(OUT / 'right_vector_custody.json')")
t=t.replace("D = load(OUT / 'right_vector_draft_status.json')", "D = load(OUT / 'scalar_vna_draft_status.json')")
t=t.replace("DV = load(DEV / 'verification.json')\nassert hf(DEV / 'verification.json') == S['own_DEV_verification_sha256']", "assert hf(DEV / 'compilation.json') == S['own_DEV_compilation_sha256']")
t=t.replace('REVIEW_RIGHT_VECTOR_DEV.md','REVIEW_SCALAR_VNA_DEV.md')
t=t.replace("for m in DV['modules']:\n    n = m['name']", "for n,m in S['transposition'].items():")
t=t.replace("hf(m['own_binary']) == D['modules'][n]['binary_sha256']", "hf(m['own_binary']) == D['modules'][n]['binary_sha256']")
for a,b in [('== 899','== 903'),('== 25','== 27'),('== 197','== 201'),('== 192','== 195'),('== 5 and {r','== 6 and {r'),('rows[-5:]','rows[-6:]'),("== 6955 and a", "== 6982 and a"),('== 6930 and set(a)', '== 6955 and set(a)'),("== 100 and all", "== 101 and all"),("'unchanged_parent_records': 192", "'unchanged_parent_records': 195"),("'new_author_compilations': 5", "'new_author_compilations': 6"),('all_three_literal_import_rewrites','all_four_literal_import_rewrites'),('dense_right_vectors_and_closable_original_involution_does_not_discharge_KMS_trace_or_physical_frontier','actual_scalar_GNS_image_von_neumann_does_not_discharge_KMS_trace_or_physical_frontier')]:
    assert a in t,a
    t=t.replace(a,b)
t=t.replace("S = load(OUT / 'static_verification.json')", "assert '--author-green-notice' in sys.argv, 'Run only after author final build/test notice'\nS = load(OUT / 'static_verification.json')")
ast.parse(t)
out=REV/'verify_scalar_vna_integration_final.py';assert not out.exists()
tmp=out.with_name(out.name+'.tmp');raw=t.encode()
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;tmp.replace(out)
print(out)
