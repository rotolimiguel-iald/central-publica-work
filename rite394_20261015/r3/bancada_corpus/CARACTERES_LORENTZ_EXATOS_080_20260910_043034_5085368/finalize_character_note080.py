"""Finalize new documentation; do not rerun the character computation."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent

def pin(path):
    content = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}

def emit(path, content):
    temporary = path.with_name(path.name + ".tmp_new")
    if path.exists() or temporary.exists():
        raise FileExistsError(path)
    with temporary.open("xb") as output:
        output.write(content)
    if temporary.read_bytes() != content:
        raise RuntimeError("Byte mismatch")
    temporary.rename(path)

calculation = HERE / "CARACTER_EXATO_LAMBDA3_WG_080.json"
script = HERE / "compute_lorentz_characters080.py"
draft = HERE / "DECOMPOSICAO_EXATA_LAMBDA3_E_TORRES_WEYL.md.pending"
before = [pin(calculation), pin(script), pin(draft)]
result = json.loads(calculation.read_bytes())
if result["script_before"] != pin(script) or result["script_after"] != pin(script):
    raise RuntimeError("Computation script pin mismatch")
if result["check_count"] != 15 or not all(row["pass"] for row in result["checks"]):
    raise RuntimeError("Character receipt is not PASS")

text = draft.read_text(encoding="utf-8")
start = text.index("Equivalentemente, se x,y")
end = text.index("## 2. Verificação independente", start)
replacement = r"""Equivalentemente, se x,y denotam as variáveis do caráter do toro, χΛ3 é o coeficiente de t³ do produto COMPLETO

\[
\left[\prod_{\epsilon,\delta=\pm1}(1+t x^\epsilon y^\delta)\right]
(1+tx^2)(1+t)(1+tx^{-2})
(1+ty^2)(1+t)(1+ty^{-2}).
\]

Há dez fatores lineares em t, incluindo duas cópias de (1+t). O parâmetro t nesta identidade é somente o contador da potência exterior, não uma identificação com o parâmetro de Rees do complexo BRST.

"""
text = text[:start] + replacement + text[end:]
links = re.findall(r"\]\(<(C:/[^>]+)>\)", text)
if not all(Path(path).is_file() for path in links):
    raise RuntimeError("Invalid local link")
note = HERE / "DECOMPOSICAO_EXATA_LAMBDA3_E_TORRES_WEYL.md"
emit(note, text.encode("utf-8"))
after = [pin(calculation), pin(script), pin(draft)]
if before != after:
    raise RuntimeError("Source changed")
manifest = {
    "status": "REAL measured files and exact arithmetic receipt; DERIVED finite-character interpretation",
    "sources_before": before,
    "sources_after": after,
    "sources_unchanged": True,
    "note": pin(note),
    "calculation_receipt": pin(calculation),
    "computation_script": pin(script),
    "documentation_script": pin(Path(__file__)),
    "arithmetic_checks": {"count": 15, "all_pass": True, "executions": 1},
    "documentation_only": {"source_pins_match": True, "local_link_count": len(links)},
    "historical_draft": {"path": draft.as_posix(), "role": "Preserved unpublished draft; abbreviated product typography replaced by the exact ten-factor product in the final note; not the final mathematical text"},
    "no_prior_sources_or_originals_modified": True,
    "no_sympy_lean_um_or_external_source_execution": True,
    "scope": "Finite representation only; no H3(s0) E4 classification or jet comparison",
}
emit(HERE / "MANIFESTO_CARACTERES_LORENTZ_080.json", json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8") + b"\n")
print(json.dumps({"note": pin(note), "manifest": pin(HERE / "MANIFESTO_CARACTERES_LORENTZ_080.json"), "calculation": pin(calculation)}, ensure_ascii=False))
