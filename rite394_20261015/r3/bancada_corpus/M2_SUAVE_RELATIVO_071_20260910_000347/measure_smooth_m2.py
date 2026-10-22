"""Create a new measured manifest for written smooth-relative M2 results."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent

def pin(path):
    data = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(data), "lines": len(data.splitlines()), "sha256": hashlib.sha256(data).hexdigest()}

notes = [
    BASE / "M2_SUAVE_POR_COMPATIBILIDADE_E_SPENCER.md",
    BASE / "COROLARIO_H0_H1_E_FINITUDE.md",
    BASE / "PRECISAO_FATORACAO_FINITA_OPERADORES.md",
]
inputs = [
    ROOT / "REGULARIDADE_KT_JATOS_20260909_224852" / "CERTIFICADO_POLINOMIAL_EINSTEIN_SIGMA.md",
    ROOT / "REGULARIDADE_KT_JATOS_20260909_224852" / "PRECISAO_CONSTRAINTS_E_COVARIANCIA.md",
    ROOT / "REGULARIDADE_KT_JATOS_20260909_224852" / "MANIFESTO_REGULARIDADE_KT.json",
    ROOT / "NORMALIDADE_RELATIVA_070_20260909_233414" / "NORMALIDADE_FORMAL_E_RESIDUO_SUAVE.md",
    ROOT / "NORMALIDADE_RELATIVA_070_20260909_233414" / "PRECISAO_HESSIANO_SIGMA.md",
    ROOT / "NORMALIDADE_RELATIVA_070_20260909_233414" / "MANIFESTO_NORMALIDADE_RELATIVA.json",
]
before = [pin(p) for p in inputs]
note_pins = [pin(p) for p in notes]
if any(p["bytes"] == 0 for p in note_pins):
    raise ValueError("Empty written artifact")
after = [pin(p) for p in inputs]
if before != after:
    raise RuntimeError("Read-only input changed during measurement")
manifest = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "Arco071: demonstracao escrita de M2 relativo suave LOCAL COORDENADO, por compatibilidade e Spencer; retorno covariante separado.",
    "status": "DERIVED_WRITTEN_SMOOTH_COORDINATE_RELATIVE_M2__COVARIANT_RETURN_OPEN",
    "coefficient_class": "C-infinity(x,g,y) on contractible value charts; finite polynomial in differentiated jets and antifields; coordinate-dependent primitives allowed.",
    "written_results": [
        "Finite prolonged compatibility H -> R-adjoint -> 0 by differentiating the polynomial triangular KT split.",
        "Finite differential-operator factorization through compatibility using polynomial matrix sections.",
        "Auxiliary-symbol homotopy sigma*h+h*sigma=(r+4-q)I with descending finite auxiliary differential order.",
        "E1(contact1,horizontal2)=ker R=0 and E1(p>0,q<=1)=0 in the stated subclass.",
        "Horizontal degree2 form lifted by two contact corrections to a total closed form, then contracted smoothly without a Taylor completion.",
        "Local coordinate H0=constants, H1=H2=0; relative H4_2(delta|dH)=0, in particular M2 elimination.",
    ],
    "limits": [
        "Primitives may depend explicitly on coordinates and smoothly, non-rationally, on metric values.",
        "No claim that the natural covariant subcomplex H2_char_cov vanishes.",
        "No automatic target-chart gluing, full anomaly removal, QME, background independence, interacting physical state or UV completion.",
        "Written mathematical derivation, not a Lean theorem or CAS replay.",
    ],
    "artifacts": note_pins,
    "measurement_script": pin(Path(__file__)),
    "read_only_inputs": before,
    "input_bytes_unchanged_during_measurement": True,
    "primary_sources": [
        {"url": "https://arxiv.org/pdf/math/9803115v1", "author": "Alexander Verbovetsky", "locations": "Secs2.2-2.3; Thm3.1; Cor3.3; k-line theorem", "access": "Web primary PDF text consulted; no local PDF hash claimed"},
        {"url": "https://arxiv.org/pdf/hep-th/0002245v3", "author": "Barnich, Brandt, Henneaux", "locations": "Thm4.2; Thm6.2; Thm6.4; Thm6.6/6.7 scope", "access": "Web primary PDF text consulted; no local PDF hash claimed"},
    ],
    "executions": {"um_import_or_execution": False, "Lean": False, "CAS": False, "nature_tests": False, "measurement_Python_standard_library": True},
    "originals_or_frozen_notes_modified": False,
    "authorship": "Own mathematical analysis of task finish_gibbs_realization; no approval attributed to other persons or agents.",
}
target = BASE / "MANIFESTO_M2_SUAVE_RELATIVO_071.json"
temp = BASE / "MANIFESTO_M2_SUAVE_RELATIVO_071.json.tmp_new"
if target.exists() or temp.exists():
    raise FileExistsError("Refusing to overwrite an existing artifact")
data = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
with temp.open("xb") as stream:
    stream.write(data)
    stream.flush()
    os.fsync(stream.fileno())
if temp.read_bytes() != data or not data:
    raise RuntimeError("Temporary bytes failed validation")
temp.rename(target)
print(json.dumps({"artifacts": note_pins, "manifest": pin(target), "input_bytes_unchanged": before == after}, ensure_ascii=False, indent=2))
