from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone
import re

BASE = Path(__file__).resolve().parent
TITLE = "POTENCIA_DERIVADAS_E_MITTAG_LEFFLER.md"

def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def new_atomic(path, data):
    if path.exists():
        raise RuntimeError(f"Refusing existing destination: {path}")
    temporary = path.with_name(path.name + ".staged")
    with temporary.open("xb") as stream:
        stream.write(data)
    if not data or temporary.read_bytes() != data:
        raise RuntimeError("Atomic staging verification failed")
    temporary.rename(path)
    if path.read_bytes() != data:
        raise RuntimeError("Final bytes mismatch")

draft = (BASE / (TITLE + ".pending")).read_text(encoding="utf-8")
prefix, middle = draft.split("## 6. Contraexemplo calculado", 1)
section, suffix = middle.split("## 7. Consequência delimitada", 1)
section = section.replace("Seja R=R[x] ou", "Seja A=ℝ[x] ou")
section = section.replace("s não atua em x", "o diferencial não atua em x")
section = section.replace("D_N^2=R^{N+1}", "D_N^2=A^{N+1}")
section = section.replace("D_N^3=R^N", "D_N^3=A^N")
section = section.replace("r\\in R", "r\\in A")
section = section.replace("H²(D_N)≃R", "H²(D_N)≃A")
section = section.replace("R\\supset xR\\supset x^2R", "A\\supset xA\\supset x^2A")
section = section.replace("Em R[x]", "Em ℝ[x]")
section = section.replace("a torre R[x] --x← R[x] --x←⋯", "a torre ℝ[x] --x← ℝ[x] --x←⋯")
section = section.replace("\\pmod{R[x]}", "\\pmod{\\mathbb R[x]}")
section = section.replace("R[[x]]/R[x]", "\\mathbb R[[x]]/\\mathbb R[x]")
old = "Na última fórmula, R nos símbolos \\mathbb R[[x]]/\\mathbb R[x] denota o corpo real, como de costume; o anel de coeficientes do exemplo é R[x]. "
original_sentence = "Na última fórmula, R nos símbolos R[[x]], R[x] denota o corpo real, como de costume; o anel de coeficientes do exemplo é R[x]. "
section = section.replace(original_sentence, "Na fórmula (9), o anel de coeficientes é A=ℝ[x]. ")
section = section.replace(old, "Na fórmula (9), o anel de coeficientes é A=ℝ[x]. ")
text = prefix + "## 6. Contraexemplo calculado" + section + "## 7. Consequência delimitada" + suffix
new_atomic(BASE / TITLE, text.encode("utf-8"))

before = json.loads((BASE / "PINS_INICIAIS.json").read_text(encoding="utf-8"))
after = []
for expected in before:
    actual = pin(Path(expected["path"]))
    actual["unchanged"] = actual["bytes"] == expected["bytes"] and actual["sha256"] == expected["sha256"]
    if not actual["unchanged"]:
        raise RuntimeError(f"Source changed: {actual['path']}")
    after.append(actual)

links = []
for raw in re.findall(r"\]\(<(C:/[^>]+)>\)", text):
    target = Path(raw)
    if not target.is_file():
        raise RuntimeError(f"Missing local link: {raw}")
    links.append(raw)

manifest = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "author": "/root/finish_gibbs_realization",
    "status": "DERIVED_POWER_BOUND_AND_PRECISE_OBSTRUCTIONS_TO_FINITE_ML_INFERENCE",
    "source_pins_after": after,
    "new_artifacts": [pin(BASE / TITLE), pin(BASE / "PINS_INICIAIS.json"), pin(Path(__file__)), pin(BASE / (TITLE + ".pending"))],
    "draft_status": "The retained .pending is an unsealed first draft. The .md is the final note, with coefficient-ring notation A and real field distinguished.",
    "local_links_verified": links,
    "primary_sources_read": [
        {"url": "https://arxiv.org/pdf/0705.3340v4", "scope": "Theorem2 and equations256-259; multilinear normalization and scaling"},
        {"url": "https://arxiv.org/pdf/1710.01937", "scope": "Theorem6.2 proof, positive derivative weights and admissibility hypothesis; no direct BV import"}
    ],
    "claims": [
        "Conditional graph recursion yields D<=2+2L for two-derivative initial vertices and compatible recursive normalization",
        "Fixed L/E/engineering weight does not bound jet order of the cochains C_N actually defined",
        "No claim that displayed high-jet cycles are cohomologically independent",
        "Finite rank over spectator coefficients and finite fibers do not imply Mittag-Leffler",
        "The auxiliary polynomial tower has lim1 equal to real formal power series modulo polynomials",
        "No identification of the auxiliary tower with the Einstein-sigma differential"
    ],
    "classical_loop_grade_preserved": True,
    "einstein_sigma_ml_proved_or_refuted": False,
    "um_executed_or_imported": False,
    "lean_or_cas_executed": False,
    "originals_written": False
}
destination = BASE / "MANIFESTO_FINITUDE_ML_078.json"
new_atomic(destination, json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8"))
print(json.dumps({"note": pin(BASE / TITLE), "manifest": pin(destination), "sources_unchanged": len(after), "local_links": len(links)}, ensure_ascii=False))
