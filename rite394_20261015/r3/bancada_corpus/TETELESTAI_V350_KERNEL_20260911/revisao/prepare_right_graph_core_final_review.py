from pathlib import Path
import ast
REV=Path(__file__).resolve().parent
t=(REV/'run_right_projection_pair_review.py').read_text(encoding='utf-8')
t=t.replace("'right_projection_pair_independent_'", "'right_graph_core_final_independent_'")
t=t.replace("Path((REV/'right_fixed_graph_latest_run.txt').read_text().strip())]", "Path((REV/'right_fixed_graph_latest_run.txt').read_text().strip()),Path((REV/'right_projection_pair_latest_run.txt').read_text().strip())]")
t=t.replace("spec=[('ScalarRightProjectionPair','20260913_014137_777731',6)]", "spec=[('ScalarRightGraphCore','20260913_020653_255405',3)]")
t=t.replace("prior=Path((REV/'right_fixed_graph_latest_run.txt').read_text().strip())", "prior=Path((REV/'right_projection_pair_latest_run.txt').read_text().strip())")
t=t.replace("prior_c['exact_48_targets']", "prior_c['exact_54_targets']").replace("len(prior_m['declarations'])==48", "len(prior_m['declarations'])==54").replace('len(inherited_sources)==4','len(inherited_sources)==5')
t=t.replace('assert len(targets)==len(set(targets))==54','assert len(targets)==len(set(targets))==57')
t=t.replace("'PARTIAL_FIVE_ACCEPTED_MODULES_6_NEW_54_CUMULATIVE_TARGETS'", "'FINAL_WRAPPER_3_NEW_57_CUMULATIVE_TARGETS_SIX_MODULES'")
t=t.replace("'right_projection_pair_latest_run.txt',str(RUN).encode()", "'right_graph_core_final_latest_run.txt',str(RUN).encode()")
t=t.replace('RightProjectionPairAudit','RightGraphCoreFinalAudit').replace("'exact_54_targets':len(records)", "'exact_57_targets':len(records)")
ast.parse(t);out=REV/'run_right_graph_core_final_review.py';assert not out.exists()
raw=t.encode();tmp=out.with_name(out.name+'.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;tmp.replace(out);print(out)
