from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
HERE = Path(__file__).resolve().parent
inputs = [
    ROOT / "COHOMOLOGIA_ESPECTADOR_B0_073_20260910" / "PRIMITIVA_ORDINARIA_COM_B0_E_LIMITE_ADMISSIVEL.md",
    ROOT / "COVARIANTIZACAO_SUAVE_071_20260910_001058_826723" / "COVARIANTIZACAO_E_H2_GLOBAL.md",
    ROOT / "COVARIANTIZACAO_SUAVE_071_20260910_001058_826723" / "COROLARIO_H5_E_ANOMALIA_LOCAL.md",
]


def pin(path):
    data = path.read_bytes()
    if data != path.read_bytes():
        raise RuntimeError(f"Unstable file: {path}")
    return {"path": str(path), "bytes": len(data), "lines": len(data.decode("utf-8").splitlines()), "sha256": hashlib.sha256(data).hexdigest(), "double_read_stable": True}


record = {
    "arc": "074",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "DERIVED_WRITTEN_RESULTS_AND_PRECISE_OPEN_CONTRACTS",
    "inputs_read_only": [pin(p) for p in inputs],
    "new_artifacts": [pin(HERE / "NORMALIZACAO_S_E_OBSTRUCAO_EULER.md"), pin(Path(__file__).resolve())],
    "primary_sources_consulted": [
        "https://arxiv.org/pdf/hep-th/9505173v2",
        "https://arxiv.org/pdf/hep-th/0002245v3",
        "https://math.mit.edu/juvitop/pastseminars/notes_2019_Fall/Chern-Simons.pdf",
        "https://annals.math.princeton.edu/1974/99-1/p03",
    ],
    "claims": {
        "s_transport": "Normal spectator jets plus finite Lorentz projection transport an existing ordinary s-primitive in the same formal class.",
        "relative_counterexample": "Background Euler is ordinarily exact but not naturally weakly exact at ghost0/form4, via a Lorentzian on-shell constant-curvature isotropy argument.",
        "relative_transgression": "Euler(g)-Euler(g0) admits a natural formal local transgression; background Euler is not removed.",
        "anomaly": "No nonzero ghost1 anomaly or full natural vanishing theorem asserted; precise sufficient degree-five criterion documented.",
    },
    "no_original_modification": True,
    "no_um_execution_import": True,
    "no_lean_cas_execution": True,
    "no_external_approval_claim": True,
}
target = HERE / "MANIFESTO_NATURALIDADE_EULER_074.json"
tmp = HERE / "MANIFESTO_NATURALIDADE_EULER_074.json.pending"
if target.exists() or tmp.exists():
    raise FileExistsError("New files only")
data = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
with tmp.open("xb") as stream:
    stream.write(data)
if tmp.read_bytes() != data or tmp.stat().st_size != len(data):
    raise RuntimeError("Temporary verification failed")
tmp.rename(target)
print(json.dumps({"manifest": pin(target), "note": record["new_artifacts"][0]}, ensure_ascii=False, indent=2))
