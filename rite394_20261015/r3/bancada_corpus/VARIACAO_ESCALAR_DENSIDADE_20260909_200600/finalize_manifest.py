"""Measure a successful fresh leaf and the separate analytical note; no um.py execution."""
from pathlib import Path
import datetime, hashlib, json, os, re, sys

ROOT = Path(__file__).resolve().parent
ALLOWED = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
assert ROOT.is_relative_to(ALLOWED)

def record(path):
    data = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def new(path, data):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    assert temporary.read_bytes() == data
    os.rename(temporary, path)
    assert path.read_bytes() == data

build = Path(sys.argv[1]).resolve()
assert build.parent == ROOT
receipt_path = build / "BUILD_RESULT.json"
receipt = json.loads(receipt_path.read_bytes())
assert receipt["status"] == "PASS_COMPILED_SCOPE"
assert receipt["boundary_unchanged"]
assert len(receipt["runs"]) == 2
assert all(item["exit_code"] == 0 for item in receipt["runs"])
source = ROOT / "ScalarMatterDensityVariation.lean"
assert source.read_bytes() == (build / source.name).read_bytes()
assert receipt["sources"] == [record(source)]
source_text = source.read_text(encoding="utf-8")
declarations = re.findall(r"(?m)^(def|theorem) (\w+)", source_text)
prints = re.findall(r"(?m)^#print axioms (\w+)$", source_text)
assert {name for _, name in declarations} == set(prints)
assert len(prints) == len(declarations) == len(receipt["axiom_rows"])
assert all(set(row["axioms"]) <= {"propext", "Classical.choice", "Quot.sound"}
           for row in receipt["axiom_rows"])
logs = [build / (item["module"] + ".log") for item in receipt["runs"]]
warning_lines = sum("warning:" in line for path in logs
                    for line in path.read_text(encoding="utf-8").splitlines())
assert warning_lines == 0
anchors = [{"kind": match.group(1), "name": match.group(2), "line": number}
           for number, line in enumerate(source_text.splitlines(), 1)
           if (match := re.match(r"^(def|theorem) (\w+)", line))]
note = ROOT / "ACAO_VARIACAO_E_REALIZACAO_HADAMARD.md"
manifest = {
    "status": "PASS_COMPILED_LEAF__ANALYTICAL_NOTE_SEPARATE",
    "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "source": record(source), "note": record(note),
    "build_receipt": record(receipt_path), "logs": [record(path) for path in logs],
    "builder": record(ROOT / "build_source.py"),
    "builder_config": record(ROOT / "CONFIG_BUILD.json"),
    "manifest_script": record(Path(__file__).resolve()),
    "theorems": receipt["theorems"], "definitions": receipt["definitions"],
    "axiom_rows": len(receipt["axiom_rows"]), "warning_lines": warning_lines,
    "axioms_outside_standard_trio": [], "source_matches_build_copy": True,
    "anchors": anchors,
    "statuses": {
        "REAL": "Fresh Lean leaf and importer compiled; determinant, volume, inverse, finite scalar density and raised stress contraction are audited in this scope.",
        "INPUT_POSTULATE": "Minimal scalar action, global potentials where used, Lorentzian signature, globally hyperbolic background for CCR realization, and fixed renormalization prescription.",
        "DERIVED_WRITTEN": "Integrated scalar Euler-Lagrange equations, topology conditions, coherent Hadamard displacement and relative renormalized stress identity; these are not Lean results.",
        "OPEN": "Interacting quantized metric, quantum BRST/BV of the coupled model, identification with Gibbs tower, physical area correspondence, absolute semiclassical backreaction and UV completion."
    },
    "references": [
        {"url": "https://arxiv.org/abs/gr-qc/0404074", "role": "Primary source: local renormalized scalar stress tensor and conservation."},
        {"url": "https://arxiv.org/html/1306.1058v4", "role": "Primary source: locally covariant perturbative quantum gravity framework; pure gravity directly, not an already-proved coupled extension."}
    ],
    "scope": receipt["scope"], "scope_note": receipt["scope_note"],
    "original_files_modified": False, "um_py_executed_or_imported": False,
    "independent_approval_claimed": False, "gate_moved": False
}
target = ROOT / "MANIFESTO_VARIACAO_ESCALAR.json"
new(target, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"manifest": record(target), "source": manifest["source"],
                  "note": manifest["note"], "theorems": manifest["theorems"],
                  "definitions": manifest["definitions"], "axiom_rows": manifest["axiom_rows"],
                  "warning_lines": warning_lines}, ensure_ascii=False))
