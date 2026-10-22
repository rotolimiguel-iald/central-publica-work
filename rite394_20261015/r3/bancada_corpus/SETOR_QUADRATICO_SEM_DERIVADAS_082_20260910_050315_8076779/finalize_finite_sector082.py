"""Finalize the new written result and documentary manifest; no arithmetic rerun."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent

def pin(path):
    data = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def emit(path, data):
    temporary = path.with_name(path.name + ".tmp_new")
    if path.exists() or temporary.exists():
        raise FileExistsError(path)
    with temporary.open("xb") as output:
        output.write(data)
    if temporary.read_bytes() != data:
        raise RuntimeError("Byte mismatch")
    temporary.rename(path)

receipt_path = HERE / "CONTROLES_SETOR_SEM_DERIVADAS_082.json"
provenance_path = HERE / "PROVENIENCIA_COPIA_ARITMETICA_082.json"
record = json.loads(receipt_path.read_bytes())
provenance = json.loads(provenance_path.read_bytes())
sources = [Path(item["path"]) for item in record["sources_before"]]
sources += [Path(provenance["source_before"]["path"]), Path(provenance["creator"]["path"]), Path(provenance["target"]["path"]), receipt_path, provenance_path]
before = [pin(path) for path in sources]
if record["sources_before"] != before[:4] or record["sources_after"] != before[:4]:
    raise RuntimeError("A source changed")
for key in ["source_before", "source_after", "creator", "target"]:
    if provenance[key] != pin(Path(provenance[key]["path"])):
        raise RuntimeError("Provenance pin mismatch")
if record["script"] != pin(Path(provenance["target"]["path"])):
    raise RuntimeError("Receipt script mismatch")
if len(record["checks"]) != 19 or not all(item["pass"] for item in record["checks"]):
    raise RuntimeError("Arithmetic receipt failure")
documentary = [item for item in record["checks"] if item["name"] == "sources_unchanged"]
if len(documentary) != 1:
    raise RuntimeError("Unexpected check classification")

pending = HERE / "IMAGEM_DO_DETECTOR_NO_SETOR_FINITO.md.pending"
note = HERE / "IMAGEM_DO_DETECTOR_NO_SETOR_FINITO.md"
if note.exists():
    raise FileExistsError(note)
data = pending.read_bytes()
if len(data) < 10000:
    raise RuntimeError("Unexpected note size")
links = re.findall(r"\]\(<(C:/[^>]+)>\)", data.decode("utf-8"))
if not all(Path(path).is_file() for path in links):
    raise RuntimeError("Missing local link")
pending.rename(note)
if note.read_bytes() != data:
    raise RuntimeError("Note byte mismatch")
after = [pin(path) for path in sources]
if before != after:
    raise RuntimeError("Source changed during finalization")
manifest = {
    "status": "DERIVED finite-sector theorem, awaiting independent review; REAL exact arithmetic and documentary pins",
    "sources_before": before, "sources_after": after, "all_sources_unchanged": True,
    "note": pin(note), "receipt": pin(receipt_path), "provenance": pin(provenance_path),
    "finalizer": pin(Path(__file__)),
    "checks": {"total": 19, "algebraic": 18, "source_preservation": 1, "all_pass": True, "arithmetic_executions": 1},
    "local_links_checked": len(links),
    "scope": "Ten invariant contractions with two undifferentiated Weyl tensors; detector image is one-dimensional and cannot match the required profile for all k",
    "not_claimed": ["All Weyl-jet classes excluded", "delta(K) zero", "minus A6 outside the full image", "QME or UV"],
    "only_new_files_under_chatgpt": True,
    "no_originals_or_frozen_sources_changed": True,
    "no_um_lean_sympy_or_old_script_execution": True,
}
destination = HERE / "MANIFESTO_SETOR_FINITO_082.json"
emit(destination, json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8") + b"\n")
print(json.dumps({"note": pin(note), "manifest": pin(destination), "receipt": pin(receipt_path)}, ensure_ascii=False))
