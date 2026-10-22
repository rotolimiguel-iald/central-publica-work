"""Read-only artifact audit; never imports or executes canonical um.py."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")
OUT = Path(__file__).resolve().parent
BASE = Path("C:/IALD/Central de Patentes/Chatgpt/MEMORIA_V334_20260909_074841_104169/EVIDENCIAS_20260909_075828_204767.json")

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def record(path, raw=None):
    raw = path.read_bytes() if raw is None else raw
    return {"path": path.as_posix(), "bytes": len(raw), "sha256": digest(raw)}

def write_new(name, raw):
    path = OUT / name
    assert not path.exists(), path
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == raw
    os.rename(tmp, path)
    return path

stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
tracked = ["um.py", "um_absoluto_selo.json", "tgl_kernel_proof_manifest.json", "um_absoluto.json"]
raws = {name: (ROOT / name).read_bytes() for name in tracked}
seal = json.loads(raws["um_absoluto_selo.json"])
manifest = json.loads(raws["tgl_kernel_proof_manifest.json"])
baseline = json.loads(BASE.read_bytes())
sealed = []
for name, expected in seal["sha256"].items():
    path = ROOT / name
    rec = record(path, raws.get(name))
    sealed.append({**rec, "expected": expected, "matches": rec["sha256"] == expected})
formal = []
for name, expected in manifest["formal_files_sha256"].items():
    rec = record(ROOT / "tgl_kernel" / name)
    formal.append({"relative_path": name, **rec, "expected": expected, "matches": rec["sha256"] == expected})
base_files = {r["path"].split("/tgl_kernel/", 1)[1]: r["sha256"] for r in baseline["formal_source_records"]}
current_files = manifest["formal_files_sha256"]
changes = {
    "added": sorted(current_files.keys() - base_files.keys()),
    "removed": sorted(base_files.keys() - current_files.keys()),
    "changed": sorted(k for k in current_files.keys() & base_files.keys() if current_files[k] != base_files[k]),
}
tree = ast.parse(raws["um.py"].decode("utf-8-sig"))
embedded = None
for node in tree.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_EMBEDDED_KERNEL_FILES" for t in node.targets):
        embedded = ast.literal_eval(node.value)
assert isinstance(embedded, dict)
normalize = lambda s: s.replace("\r\n", "\n").replace("\r", "\n")
axioms = manifest["axiom_report"]
trio = {"propext", "Classical.choice", "Quot.sound"}
outside = {k: v for k, v in axioms.items() if not set(v) <= trio}
modules = []
for name in changes["added"]:
    if not name.endswith(".lean"):
        continue
    path = ROOT / "tgl_kernel" / name
    raw = path.read_bytes()
    source = raw.decode("utf-8-sig")
    terms = re.findall(r"(?m)^theorem\s+([\w.]+)", source)
    modules.append({"relative_path": name, **record(path, raw),
        "embedded_equal_after_newline_normalization": normalize(source) == normalize(embedded[name]),
        "terms": {"TGLExt." + term: {"present": "TGLExt." + term in axioms, "axioms": axioms.get("TGLExt." + term)} for term in terms}})
logs = {}
for name, field in [("tgl_kernel_build_capture.txt", "build_stdout_sha256"), ("tgl_kernel_audit_capture.txt", "audit_stdout_sha256")]:
    path = ROOT / name
    raw = path.read_bytes()
    capture = normalize(raw.decode("utf-8-sig"))
    head = re.match(r"# cmd: ([^\n]*)\n# returncode: (-?\d+)\n# len\(stdout\)=(\d+) len\(stderr\)=(\d+)\n--- STDOUT ---\n", capture)
    rec = record(path, raw)
    if head:
        out = capture[head.end():head.end() + int(head.group(3))]
        rec.update(returncode=int(head.group(2)), stdout_sha256=digest(out.encode()),
            stdout_matches_manifest=digest(out.encode()) == manifest[field],
            expected_stdout_sha256=manifest[field])
    else:
        rec["parse_error"] = "Capture header not recognized"
    logs[name] = rec
rounds = {}
for name in ["rodada_v336_stdout.txt", "rodada_v336_stdout_INTERMEDIARIA.txt"]:
    path = ROOT / name
    raw = path.read_bytes()
    txt = normalize(raw.decode("utf-8", errors="replace"))
    rounds[name] = {**record(path, raw),
        "clean_theorem_counts": re.findall(r"teoremas limpos:\s*(\d+)/(\d+)", txt),
        "completion_marker": "TETELESTAI. O UM foi inscrito." in txt,
        "selftest_pass_marker": ">>> FAIL_CLOSED_SELFTEST_PASSED <<<" in txt,
        "exit_lines": re.findall(r"(?m)^exit=.*$", txt),
        "checkpoint_lines": [line for line in txt.splitlines() if line.startswith("[selo] rite_checkpoints:")],
        "tail": txt[-800:],
        "note": "Intermediate completion is not a receipt for the subsequent full run."}
stable = {name: digest((ROOT / name).read_bytes()) == digest(raw) for name, raw in raws.items()}
data = {"created_utc": datetime.now(timezone.utc).isoformat(), "version": "v336",
    "scope": "Read existing source, seal, manifest and logs. No original execution or fresh Lean build.",
    "um": record(ROOT / "um.py", raws["um.py"]),
    "seal": record(ROOT / "um_absoluto_selo.json", raws["um_absoluto_selo.json"]),
    "seal_timestamp": seal.get("timestamp"), "gate": seal.get("qg_closure_verdict"),
    "selftest_in_current_seal": seal.get("fail_closed_selftest"),
    "checkpoints_in_current_seal": seal.get("rite_checkpoints"),
    "sealed_artifacts": sealed, "formal_source_records": formal,
    "comparison_with_v334": changes, "new_modules": modules,
    "axiom_terms": len(axioms), "without_axioms": sum(not value for value in axioms.values()),
    "outside_standard_trio": outside, "manifest_statuses": manifest["statuses"],
    "captures": logs, "rounds": rounds, "stable_during_read": stable,
    "current_round_fully_receipted": bool(seal.get("fail_closed_selftest")) and rounds["rodada_v336_stdout.txt"]["completion_marker"],
    "canonical_files_modified": False, "source_um_executed": False}
for name in ["um_absoluto_selo.json", "tgl_kernel_proof_manifest.json"]:
    write_new("SNAPSHOT_" + stamp + "_" + name, raws[name])
output = write_new("EVIDENCIAS_" + stamp + ".json", (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode())
print(json.dumps({"report": output.as_posix(), "um": data["um"],
    "sealed_matches": [sum(r["matches"] for r in sealed), len(sealed)],
    "formal_matches": [sum(r["matches"] for r in formal), len(formal)],
    "changes": changes, "new_theorems": sum(len(r["terms"]) for r in modules),
    "new_embedded_matches": all(r["embedded_equal_after_newline_normalization"] for r in modules),
    "new_terms_in_report": all(t["present"] for r in modules for t in r["terms"].values()),
    "axiom_terms": len(axioms), "outside_trio": len(outside),
    "captures": {k: {f: v.get(f) for f in ["returncode", "stdout_matches_manifest"]} for k, v in logs.items()},
    "rounds": {k: {f: v[f] for f in ["clean_theorem_counts", "completion_marker", "selftest_pass_marker", "exit_lines"]} for k, v in rounds.items()},
    "stable_during_read": stable, "current_round_fully_receipted": data["current_round_fully_receipted"]}, ensure_ascii=False))
