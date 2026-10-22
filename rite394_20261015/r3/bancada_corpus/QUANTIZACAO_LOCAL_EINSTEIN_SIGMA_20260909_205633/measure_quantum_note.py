"""Measure this new note and its read-only local inputs; never import um.py."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parent
CHATGPT = ROOT.parent


def measure(path, role):
    data = path.read_bytes()
    info = path.stat()
    return {
        "path": str(path),
        "role": role,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "mtime_ns": info.st_mtime_ns,
        "lines": len(data.splitlines()),
    }


def write_new_json(path, obj):
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite {path}")
    payload = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temporary = path.with_name(path.name + ".new")
    with temporary.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.stat().st_size != len(payload) or temporary.read_bytes() != payload:
        raise RuntimeError("Temporary file verification failed")
    os.rename(temporary, path)
    if path.read_bytes() != payload:
        raise RuntimeError("Final file verification failed")


inputs = [
    ("HABITANTE_CURVO_SIGMA_20260909_202000/HABITANTE_CURVO_SIGMA_E_AREA.md", "written on-shell background derivation"),
    ("HABITANTE_CURVO_SIGMA_20260909_202000/VERIFICACAO_SIMBOLICA.json", "prior exact CAS background receipt; not Lean"),
    ("HABITANTE_CURVO_SIGMA_20260909_202000/MANIFESTO_HABITANTE_CURVO.json", "prior measured background manifest"),
    ("METRICA_FISHER_SELECIONADA_20260909_195323_635574/SelectedFisherLorentzMetric.lean", "read-only selected Fisher source"),
    ("METRICA_FISHER_SELECIONADA_20260909_195323_635574/BUILD_20260909_200624_640468/BUILD_RESULT.json", "historical receipt for Fisher source; no new compilation here"),
    ("VARIACAO_ESCALAR_DENSIDADE_20260909_200600/ScalarMatterDensityVariation.lean", "read-only scalar density metric variation source"),
    ("VARIACAO_ESCALAR_DENSIDADE_20260909_200600/BUILD_20260909_200520_881623/BUILD_RESULT.json", "historical density variation build; no new compilation here"),
    ("DEGENERESCENCIA_VARIACIONAL_FISHER_20260909_205440_2995947/NOTA_DEGENERESCENCIA_E_RECIPROCO.md", "related independent written degeneracy analysis; not a premise of minimal-family proof"),
]

references = [
    {"authors": "Bär, Ginoux, Pfäffle", "title": "Wave Equations on Lorentzian Manifolds and Quantization", "url": "https://arxiv.org/abs/0806.1036", "used_scope": "normally hyperbolic Green operators on globally hyperbolic spacetime"},
    {"authors": "Hack, Schenkel", "title": "Linear bosonic and fermionic quantum gauge theories on curved spacetimes", "url": "https://arxiv.org/html/1205.3484v2", "used_scope": "linear gauge causal algebra framework, sections 3-4"},
    {"authors": "Hack", "title": "Quantization of the linearised Einstein-Klein-Gordon system on arbitrary backgrounds", "url": "https://arxiv.org/html/1403.3957v2", "used_scope": "on-shell coupled scalar-gravity antecedent, not target-S3 theorem"},
    {"authors": "Fewster, Strohmaier", "title": "On the construction of Hadamard states from Feynman propagators", "url": "https://arxiv.org/html/2510.11492v2", "used_scope": "Theorem 4 and Corollary 5 for positive real finite-rank bundles; applies to fixed-metric J"},
    {"authors": "Gérard", "title": "Hadamard states for linearized gravity on spacetimes with compact Cauchy surfaces", "url": "https://arxiv.org/abs/2311.11043", "used_scope": "explicit non-applicability: Einstein spacetime and compact Cauchy assumptions"},
    {"authors": "Fredenhagen, Rejzner", "title": "Batalin-Vilkovisky formalism in perturbative algebraic quantum field theory", "url": "https://arxiv.org/html/1110.5232v3", "used_scope": "renormalized BV and anomalous Master Ward Identity"},
    {"authors": "Brunetti, Fredenhagen, Rejzner", "title": "Quantum gravity from the point of view of locally covariant quantum field theory", "url": "https://arxiv.org/html/1306.1058v4", "used_scope": "pure gravity formal-series construction and representation limitations; not full sigma theorem"},
    {"authors": "Barnich, Brandt, Henneaux", "title": "Local BRST cohomology in Einstein-Yang-Mills theory", "url": "https://arxiv.org/pdf/hep-th/9505173", "used_scope": "candidate local anomalies, sections 2,4,10.4; sigma formal-completion applicability remains a contract"},
    {"authors": "Hollands, Wald", "title": "Conservation of the stress tensor in perturbative interacting quantum field theory in curved spacetimes", "url": "https://arxiv.org/abs/gr-qc/0404074", "used_scope": "fixed-background interacting polynomial scalar conservation, not coupled sigma construction"},
    {"authors": "Carfora, Dappiaggi, Drago, Rinaldi", "title": "Ricci Flow from the Renormalization of Nonlinear Sigma Models in the Framework of Euclidean Algebraic Quantum Field Theory", "url": "https://arxiv.org/html/1809.07652v2", "used_scope": "two-dimensional Euclidean sigma source; does not cover Lorentzian four-dimensional Einstein-sigma"},
]

note = ROOT / "OPERADOR_JACOBI_GAUGE_E_ESCOPO.md"
report = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "DERIVED_WRITTEN_WITH_EXPLICIT_KNOWN_INPUTS",
    "new_lean_compilation": False,
    "um_executed_or_imported": False,
    "originals_modified": False,
    "authorship": "Own mathematical derivation; no approval attributed to another person or agent",
    "outputs": [measure(note, "new written proof"), measure(Path(__file__).resolve(), "measurement script")],
    "inputs": [measure(CHATGPT / path, role) for path, role in inputs],
    "byte_backups_of_own_note": [measure(p, "immediate byte backup before local revision") for p in sorted(ROOT.glob("*.bak_*"))],
    "web_sources": references,
    "proved_in_writing": [
        "Tangent sigma Jacobi operator J=D^2-2/a^2 on rank3 bundle",
        "Exact metric-matter linearization, offdiagonal differential order at most1",
        "Gauge-fixed Hessian algebraically normally hyperbolic on rank13 bundle",
        "Ghost normally hyperbolic and exact gauge Green intertwining identities",
        "Presymplectic quotient and causal CCR algebra for coupled linear theory",
        "Fixed-metric matter Hadamard theorem hypotheses verified including commutator normalization",
        "Classical BRST nilpotence and classical master equation for explicitly chosen ambient action",
        "All induced perturbations of minimal five-category full-rank family are local pure gauge",
    ],
    "open_or_conditional": [
        "Coupled physical Hadamard positive state compatible with gauge identities",
        "Sigma formal-jet extension of local cohomology classification and renormalized counterterms",
        "Quantum identification of ambient independent fields with a probabilistic extension having physical modes",
        "Global topology, boundaries, UV completion and empirical calibration",
    ],
}

target = ROOT / "MANIFESTO_QUANTIZACAO_LOCAL.json"
write_new_json(target, report)
print(json.dumps({"note": measure(note, "final note"), "manifest": measure(target, "new measured manifest"), "input_count": len(inputs), "web_source_count": len(references)}, ensure_ascii=False, indent=2))
