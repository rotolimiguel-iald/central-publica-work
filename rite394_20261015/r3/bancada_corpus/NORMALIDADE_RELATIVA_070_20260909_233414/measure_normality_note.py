"""Measure the new note and read-only input pins; never import the project."""
from pathlib import Path
import hashlib
import json
import os
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent

def pin(path):
    raw = path.read_bytes()
    return {
        "path": str(path.resolve()),
        "bytes": len(raw),
        "lines": len(raw.splitlines()),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }

note = BASE / "NORMALIDADE_FORMAL_E_RESIDUO_SUAVE.md"
inputs = [
    ROOT / "REGULARIDADE_KT_JATOS_20260909_224852" / "CERTIFICADO_POLINOMIAL_EINSTEIN_SIGMA.md",
    ROOT / "REGULARIDADE_KT_JATOS_20260909_224852" / "PRECISAO_CONSTRAINTS_E_COVARIANCIA.md",
    ROOT / "REGULARIDADE_KT_JATOS_20260909_224852" / "MANIFESTO_REGULARIDADE_KT.json",
]
manifest = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "Arco 070: normalidade formal, transporte finito em Lambda, reducibilidade sigma e residuo M2 suave.",
    "author": "Analise propria da tarefa finish_gibbs_realization; nao constitui aprovacao em nome de terceiros.",
    "classification": "DERIVED escrito + KNOWN fontes primarias; REAL somente medicao dos arquivos.",
    "note": pin(note),
    "measurement_script": pin(Path(__file__)),
    "read_only_inputs": [pin(p) for p in inputs],
    "primary_sources_consulted": [
        {"url": "https://arxiv.org/pdf/hep-th/9405109v2", "locations": "sec.10 pp.30-33; sec.11 pp.33-34", "access": "web PDF text; no local PDF download or hash claimed"},
        {"url": "https://arxiv.org/pdf/hep-th/0002245v3", "locations": "secs.6.4.1-6.4.4; Thms6.4-6.7", "access": "web PDF text; no local PDF download or hash claimed"},
        {"url": "https://arxiv.org/pdf/hep-th/9505173v2", "locations": "Appendix E, LemmaE.2 pp.55-57", "access": "web PDF text; no local PDF download or hash claimed"},
    ],
    "established_written": [
        "Errata: Lambda alone is not excluded by the primary definition and examples of Einstein normality.",
        "K=N_derivatives+2N_field_antifields+3N_ghost_antifields; delta_Lambda=delta_0+Lambda delta_minus2.",
        "Finite descending-K transport of bounded-K relative primitives from Lambda0, conditional on base exactness in the same coefficient class.",
        "No universal local reducibility parameter: dphi1,dphi2,dphi3,dQ form a basis on dense stationary jets; no gradient denominator introduced.",
        "Normality of Lambda0 Einstein-sigma in the formal completion, via Pauli-Fierz plus three scalar quadratic fields and free KT regularity.",
        "Relative H4_2 vanishes in that formal completion using normality, reducibility elimination and finite Lambda transport.",
    ],
    "open_in_this_note": [
        "Pure quadratic-antifield lemma M2 with bounded-K natural C-infinity(U) primitives.",
        "Covariant smooth characteristic degree-two homotopy, or a precise primary theorem providing it in the same class.",
        "No claim of all H1,4(s|d), global anomalies, UV completion or nonperturbative functional measure.",
    ],
    "executions": {"um_py": False, "lean": False, "cas": False, "nature_tests": False, "measurement_python_stdlib": True},
    "originals_or_frozen_files_modified": False,
}
target = BASE / "MANIFESTO_NORMALIDADE_RELATIVA.json"
temp = BASE / "MANIFESTO_NORMALIDADE_RELATIVA.json.tmp_new"
raw = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
if target.exists() or temp.exists():
    raise FileExistsError("Refusing to overwrite an existing artifact")
with temp.open("xb") as stream:
    stream.write(raw)
    stream.flush()
    os.fsync(stream.fileno())
if temp.read_bytes() != raw or not raw:
    raise RuntimeError("Temporary output failed exact-byte verification")
temp.rename(target)
print(json.dumps({"note": pin(note), "manifest": pin(target), "inputs": manifest["read_only_inputs"]}, ensure_ascii=False, indent=2))
