"""Finalize new note and measured manifest without rerunning any mathematics."""
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

receipt = HERE / "CONTROLES_DETECTOR_WEYL_QUADRATICO_081.json"
script = HERE / "compute_odd_weyl081.py"
draft = HERE / "CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md.pending"
record = json.loads(receipt.read_bytes())
before = [pin(Path(item["path"])) for item in record["sources_before"]]
own_before = [pin(receipt), pin(script), pin(draft)]
if before != record["sources_before"] or before != record["sources_after"]:
    raise RuntimeError("A mathematical source changed")
if pin(script) != record["script"]:
    raise RuntimeError("Calculation script changed")
if record["check_count"] != 14 or not all(item["pass"] for item in record["checks"]):
    raise RuntimeError("Arithmetic receipt failed")

text = draft.read_text(encoding="utf-8")
marker = "Para os Killing escolhidos, a naturalidade de W[1] e o fato de Lie_Cg0=0 implicam s1J=Lie_CJ=C^μ∂μJ na avaliação. J é par. Logo"
replacement = r"""A passagem para a derivada de Lie pode ser conferida na série completa, antes de avaliar. Defina o pseudoscalar natural da métrica ativa por

\[
\mathcal J(g)=\frac{\operatorname{tr}(W(g)\wedge W(g))}{\operatorname{vol}_g},
\qquad
\mathcal J(g_0+t h)=t^2J+t^3J_3+O(t^4).
\]

Não há termos anteriores porque W(g0)=0; o coeficiente quadrático é exatamente (3), já que a primeira variação do volume multiplicaria W0. A covariância do pseudoscalar sob difeomorfismos locais que preservam orientação dá s𝒥=t C·∂𝒥. Comparar o coeficiente de t³, com s=s0+t s1 nos campos, produz a identidade OFF-SHELL

\[
\boxed{s_1J+s_0J_3=C^\mu\partial_\mu J.}
\tag{18a}
\]

J3 é um coeficiente natural finito em jatos da série junto ao fundo não degenerado. Na avaliação por Killing, s0J3 contém R0C e seus prolongamentos e é zero. Portanto ev(s1J)=ev(C·∂J). A igualdade sem o termo s0J3 não foi afirmada universalmente antes da avaliação. Isso coincide com o argumento de equivariância de W[1] pelas isometrias de g0. J é par. Logo"""
if text.count(marker) != 1:
    raise RuntimeError("Unexpected note insertion marker")
text = text.replace(marker, replacement)
links = re.findall(r"\]\(<(C:/[^>]+)>\)", text)
if not all(Path(path).is_file() for path in links):
    raise RuntimeError("Invalid local link")
note = HERE / "CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md"
emit(note, text.encode("utf-8"))
after = [pin(Path(item["path"])) for item in record["sources_before"]]
own_after = [pin(receipt), pin(script), pin(draft)]
if before != after or own_before != own_after:
    raise RuntimeError("A source changed during note finalization")
manifest = {
    "status": "REAL measured files and 14 exact controls; DERIVED mathematical counterexample, pending independent review",
    "sources_before": before, "sources_after": after,
    "own_inputs_before": own_before, "own_inputs_after": own_after,
    "all_sources_unchanged": True,
    "note": pin(note), "arithmetic_receipt": pin(receipt),
    "calculation_script": pin(script), "finalizer_script": pin(Path(__file__)),
    "arithmetic": {"checks": 14, "all_pass": True, "executions": 1},
    "local_links": len(links),
    "historical_draft_role": "Preserved unpublished draft; final note additionally gives the explicit off-shell identity s1J+s0J3=C partial J. Only the final .md is the delivered mathematical note.",
    "result": "A closed E5 candidate has nonzero odd detector; delta(K) is not zero in the fixed category, without deciding whether minus A6 belongs to that image",
    "no_original_079_080_or_canonical_file_modified": True,
    "no_sympy_lean_um_or_external_source_execution": True,
}
destination = HERE / "MANIFESTO_DETECTOR_QUADRATICO_081.json"
emit(destination, json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8") + b"\n")
print(json.dumps({"note": pin(note), "manifest": pin(destination), "arithmetic": pin(receipt)}, ensure_ascii=False))
