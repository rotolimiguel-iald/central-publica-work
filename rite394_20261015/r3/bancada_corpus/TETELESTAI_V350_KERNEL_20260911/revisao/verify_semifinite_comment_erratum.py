"""Static erratum verification; never runs author code or Lean."""
from pathlib import Path
import ast, datetime, difflib, hashlib, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / "dual_semifinite_ideal_latest_run.txt").read_text(encoding="utf-8"))
OLD = RUN / "final_integrated_20260912_035324_363904"
ERR = max(RUN.glob("comment_erratum_*"))
DEST = RUN / ("erratum_final_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
DEST.mkdir()
sha = lambda b: hashlib.sha256(b).hexdigest()
def write(p, raw):
    assert p.resolve().is_relative_to(REVIEW) and not p.exists()
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    with tmp.open("xb") as f: f.write(raw)
    assert tmp.read_bytes() == raw
    tmp.replace(p)
def save(p, obj): write(p, json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8"))
def emb_rest(raw):
    tree = ast.parse(raw)
    nodes = [n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_EMBEDDED_KERNEL_FILES" for t in n.targets)]
    assert len(nodes) == 1
    emb = ast.literal_eval(nodes[0].value)
    tree.body.remove(nodes[0])
    return emb, ast.dump(tree, include_attributes=False)
def ax(raw):
    txt = raw.decode("utf-8")
    result = {n: [x.strip() for x in a.split(",") if x.strip()] for n,a in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",txt,re.S)}
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",txt): result.setdefault(n,[])
    return result
names = ["integration.json", "integrated_compile.json", "gate_tests.json", "kernel_incremental_evidence.json", "gate_extension.py", "test_gate_extension.py", "MINUTA_IDEAL_SEMIFINITO.md", "record_semifinite_ideal_progress.py", "verify_semifinite_ideal_custody.py"]
for n in names: write(DEST/n, (ROOT/n).read_bytes())
I,B,G,E = [json.loads((DEST/n).read_bytes()) for n in names[:4]]
V = json.loads((OLD/"verification.json").read_bytes())
OB = json.loads((OLD/"integrated_compile.json").read_bytes())
old_records = {r["source"]:r for r in OB["records"]}
old_hashes = {r["file"]:r for r in V["records"]}
records = []
for row in B["records"]:
    src = Path(row["source"]); rel = src.relative_to(ROOT/"kernel")
    raw = src.read_bytes(); binary = ROOT/"build"/rel.with_suffix(".olean")
    r = {"file":rel.as_posix(),"returncode":row["returncode"],"timestamp":row["timestamp"],"source_sha256":sha(raw),"binary_sha256":sha(binary.read_bytes()),"source_hash_matches":sha(raw)==row["sha256"],"binary_hash_matches":sha(binary.read_bytes())==row["output_sha256"],"source_unchanged_during_compile":row.get("source_unchanged_during_compile"),"same_record_timestamp_as_previous":row["timestamp"]==old_records[row["source"]]["timestamp"]}
    records.append(r); write(DEST/"sources"/rel,raw)
    for stream in ["stdout","stderr"]:
        p = Path(row[stream]); write(DEST/"logs"/p.name,p.read_bytes())
auditrow = next(r for r in B["records"] if r["source"].endswith("TGL\\Audit.lean"))
AX = ax(Path(auditrow["stdout"]).read_bytes())
oldAX = json.loads((OLD/"axioms.json").read_bytes())
devlog = ROOT/"logs/DualSemifiniteIdeal_20260912_035730_251164.json"
D = json.loads(devlog.read_bytes()); write(DEST/"logs"/devlog.name,devlog.read_bytes())
for stream in ["stdout","stderr"]:
    p=Path(D[stream]); write(DEST/"logs"/p.name,p.read_bytes())
dev = Path(D["source"]).read_bytes(); before=(ERR/"DualSemifiniteIdeal.before.lean").read_bytes()
after = (ERR/"DualSemifiniteIdeal.after.lean").read_bytes()
write(DEST/"DualSemifiniteIdeal.lean",dev)
def splitcomment(raw):
    a=raw.index(b'/-- A single bound for all vectors:'); b=raw.index(b'-/',a)+2
    return raw[:a],raw[a:b],raw[b:]
oldparts,newparts=splitcomment(before),splitcomment(dev)
currentum=(ROOT/"um.py").read_bytes(); embedded,rest=emb_rest(currentum)
oldumfile=next(p for p in sorted(ROOT.glob("um.py.bak_*"),reverse=True) if sha(p.read_bytes())==V["um_sha256"])
oldum=oldumfile.read_bytes(); oldembedded,oldrest=emb_rest(oldum)
mod="TGLExt/V350DualSemifiniteIdeal.lean"
source_matches={}
for name in ["RegularApproximation","FourierL1L2","RegularFiniteWeight","DualSemifiniteIdeal"]:
    raw=(ROOT/"kernel/TGLV350"/(name+".lean")).read_bytes(); rel="TGLExt/V350"+name+".lean"; integ=(ROOT/"kernel"/rel).read_bytes()
    source_matches[name]={"dev_sha256":sha(raw),"integrated_sha256":sha(integ),"only_import_rewrite":integ.decode("utf-8")==raw.decode("utf-8").replace("import TGLV350.","import TGLExt.V350"),"embedded_byte_equal":embedded[rel].encode("utf-8")==integ,"same_as_previous_dev":sha(raw)==V["source_matches"][name]["dev_sha256"]}
doc={}
for n in names[6:]:
    raw=(DEST/n).read_bytes(); previous=(RUN/"final_recorder"/n).read_bytes()
    doc[n]={"sha256":sha(raw),"same_as_reviewed":raw==previous}
    if n.endswith(".py"): ast.parse(raw)
    if raw!=previous: write(DEST/(n+".diff"),"".join(difflib.unified_diff(previous.decode("utf-8").splitlines(True),raw.decode("utf-8").splitlines(True))).encode("utf-8"))
C=json.loads((RUN/"compilation.json").read_bytes())
M=json.loads((RUN/"manifest.json").read_bytes())
flags=["qgf_continuous_modular_realization_constructed","qgf_unconditional_continuous_corner_proved","qgf_full_TGL_witness_constructed","gpf_H1_internal_susy_relative_gap_discharged","gpf_H2_smooth_modular_four_frame_discharged","gpf_H3_local_horizon_equilibrium_discharged"]
result={"mode":"STATIC_LITERAL_DIFF_AST_HASH_AND_AUTHOR_LOG_INSPECTION__NO_NEW_INDEPENDENT_COMPILATION_OR_TEST", "timestamp":datetime.datetime.now().astimezone().isoformat(),"path":str(DEST),"previous_snapshot_sha256":sha(oldum),"current_snapshot_sha256":sha(currentum),"um_matches_integration_and_gate":sha(currentum)==I["working_sha256"]==G["working_um_sha256"],"old_comment_source_sha256":sha(before),"corrected_source_sha256":sha(dev),"comment_only":oldparts[0]==newparts[0] and oldparts[2]==newparts[2],"corrected_source_still_frozen":dev==after,"new_comment":newparts[1].decode("utf-8"),"dev_log_source_matches":sha(dev)==D["sha256"],"dev_log_rc":D["returncode"],"dev_source_unchanged_reported":D["source_unchanged_during_compile"],"dev_binary_sha256":sha((ROOT/"build/TGLV350/DualSemifiniteIdeal.olean").read_bytes()),"dev_binary_matches":sha((ROOT/"build/TGLV350/DualSemifiniteIdeal.olean").read_bytes())==D["output_sha256"],"dev_audited_axioms":ax(Path(D["stdout"]).read_bytes()),"integrated_records":len(records),"all_records_rc0_and_hashes_match":all(r["returncode"]==0 and r["source_hash_matches"] and r["binary_hash_matches"] for r in records),"records":records,"recompiled_record_names":[r["file"] for r in records if not r["same_record_timestamp_as_previous"]],"retained_record_count":sum(r["same_record_timestamp_as_previous"] for r in records),"all_retained_source_and_binary_unchanged":all(r["source_sha256"]==old_hashes[r["file"]]["source_sha256"] and r["binary_sha256"]==old_hashes[r["file"]]["binary_sha256"] for r in records if r["same_record_timestamp_as_previous"]),"embedded_files":len(embedded),"added_embedded":sorted(set(embedded)-set(oldembedded)),"removed_embedded":sorted(set(oldembedded)-set(embedded)),"changed_embedded":sorted(n for n in embedded if n in oldembedded and embedded[n]!=oldembedded[n]),"python_ast_outside_embedded_unchanged":rest==oldrest,"gate_byte_unchanged":(DEST/"gate_extension.py").read_bytes()==(OLD/"gate_extension.py").read_bytes(),"test_script_byte_unchanged":(DEST/"test_gate_extension.py").read_bytes()==(OLD/"test_gate_extension.py").read_bytes(),"source_matches":source_matches,"audit_distinct":len(AX),"audit_same_as_previous":AX==oldAX,"audit_equal_evidence":AX==E["axiom_report"],"axioms_allowed":all(set(v)<={"propext","Classical.choice","Quot.sound"} for v in AX.values()),"independent_40_axioms_same":len(C["records"][-1]["axioms"])==40 and all(AX[n]==a for n,a in C["records"][-1]["axioms"].items()),"author_tests_passed":G["passed"],"author_test_count":len(G["checks"]),"author_all_tests_passed":all(c["passed"] for c in G["checks"]),"gate_audit_count_matches":G["axiom_report_entries"]==len(AX),"incremental_build_ok":B["incremental_build_ok"] and E["incremental_build_ok"],"dependency_hashes_verified_author_report":E["dependency_hashes_verified"],"six_flags":{f:E[f] for f in flags},"legacy_gate_changed":G["frontier"]["legacy_gate_changed"],"full_plan_complete":G["frontier"]["full_plan_complete"],"full_monolithic_runtime_run":E["full_monolithic_runtime_run"],"documents":doc,"previous_custodied_reviews_preserved":all(sha(Path(p).read_bytes())==h for p,h in M["previous_reviews"].items() if Path(p).name!="REVIEW_REGULAR_SEMIFINITE_ROUTE.md"),"report_before_append_sha256":sha((REVIEW/"REVIEW_REGULAR_SEMIFINITE_ROUTE.md").read_bytes()),"draft_excluded_from_reading":True,"draft_absent_from_embedded":not any("BoundedDualValues" in p for p in embedded),"snapshot_files_sha256":{n:sha((DEST/n).read_bytes()) for n in names},"live_snapshot_files_still_identical":all((ROOT/n).read_bytes()==(DEST/n).read_bytes() for n in names)}
save(DEST/"verification.json",result)
print(json.dumps({k:v for k,v in result.items() if k not in ["records","dev_audited_axioms"]},ensure_ascii=False,indent=2))
