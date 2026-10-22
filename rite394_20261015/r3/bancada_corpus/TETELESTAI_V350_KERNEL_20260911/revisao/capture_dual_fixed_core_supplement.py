"""Inspect the final author evidence and recorder as data, without executing them."""
from pathlib import Path
import ast, json, hashlib, datetime, re, difflib, sys
sys.stdout.reconfigure(encoding="utf-8")
REVIEW=Path(__file__).resolve().parent
ROOT=REVIEW.parent
RUN=Path((REVIEW/"dual_fixed_core_latest_run.txt").read_text(encoding="utf-8"))
CAP=max(RUN.glob("final_integrated_*"))
V=json.loads((CAP/"verification.json").read_bytes())
sha=lambda raw:hashlib.sha256(raw).hexdigest()
for name in ["kernel_incremental_evidence.json","record_fixed_resolvent_progress.py"]:
    raw=(ROOT/name).read_bytes()
    out=CAP/name
    with out.open("xb") as f:f.write(raw)
    assert out.read_bytes()==raw
E=json.loads((CAP/"kernel_incremental_evidence.json").read_bytes())
G=json.loads((CAP/"gate_tests.json").read_bytes())
B=json.loads((CAP/"integrated_compile.json").read_bytes())
AX=json.loads((CAP/"axioms.json").read_bytes())
M=json.loads((RUN/"manifest.json").read_bytes())
C=json.loads((RUN/"compilation.json").read_bytes())
rec=(CAP/"record_fixed_resolvent_progress.py").read_bytes()
ast.parse(rec)
previous=Path(V["previous_layer"])
oldG=json.loads((previous/"gate_tests.json").read_bytes())
diff="".join(difflib.unified_diff((previous/"test_gate_extension.py").read_text(encoding="utf-8").splitlines(True),(CAP/"test_gate_extension.py").read_text(encoding="utf-8").splitlines(True),fromfile="previous44",tofile="current_final"))
with (CAP/"test_gate_extension.diff").open("xb") as f:f.write(diff.encode("utf-8"))
newfiles=set(V["new_compilations_relative_to_44"])
flags=["qgf_continuous_modular_realization_constructed","qgf_unconditional_continuous_corner_proved","qgf_full_TGL_witness_constructed","gpf_H1_internal_susy_relative_gap_discharged","gpf_H2_smooth_modular_four_frame_discharged","gpf_H3_local_horizon_equilibrium_discharged"]
all_decl=M["prior_declarations_in_full_audit"]+M["declarations"]
source_prints=set()
for row in V["source_matches"]:
    raw=(ROOT/"kernel/TGLV350"/(row+".lean")).read_text(encoding="utf-8")
    source_prints.update("TGLV350.Regular."+n for n in re.findall(r"^#print axioms ([\w.]+)$",raw,re.M))
summary={"mode":"STATIC_INSPECTION_ONLY_NO_TEST_OR_RECORDER_EXECUTION","timestamp":datetime.datetime.now().astimezone().isoformat(),
"evidence_sha256":sha((CAP/"kernel_incremental_evidence.json").read_bytes()),"recorder_sha256":sha(rec),
"recorder_matches_reviewed_snapshot":rec==(RUN/"final_recorder/record_fixed_resolvent_progress.py").read_bytes(),
"evidence_axioms_equal_actual_Audit_log":E["axiom_report"]==AX,"evidence_audit_count":len(E["axiom_report"]),
"incremental_build_ok":E["incremental_build_ok"],"dependency_hashes_verified_reported":E["dependency_hashes_verified"],
"changed_source_hashes_verified_reported":E["changed_source_hashes_verified"],"full_monolithic_runtime_run":E["full_monolithic_runtime_run"],
"open_flags":{f:E[f] for f in flags},"all_six_open_flags_false":all(E[f] is False for f in flags),
"test_report_count_matches_passed":len(G["checks"])==G["passed"],"test_report_audit_count_matches_log":G["axiom_report_entries"]==len(AX),
"new_test_names":[c["name"] for c in G["checks"] if c["name"] not in {x["name"] for x in oldG["checks"]}],
"independent_declarations_count":len(all_decl),"printed_source_targets":len(source_prints),
"all_printed_targets_in_integrated_Audit":source_prints <= set(AX),
"only_independent_extra_declarations":[n for n in all_decl if n not in AX],
"independent_and_author_axioms_match_on_printed_targets":all(C["records"][-1]["axioms"][n]==AX[n] for n in source_prints),
"new_records_source_unchanged_during_compile":all(row.get("source_unchanged_during_compile") is True for row in B["records"] if Path(row["source"]).relative_to(ROOT/"kernel").as_posix() in newfiles)}
with (CAP/"supplemental_verification.json").open("xb") as f:f.write(json.dumps(summary,ensure_ascii=False,indent=2).encode("utf-8"))
print(json.dumps(summary,ensure_ascii=False,indent=2))
print(diff)
