from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os
FOLDER = Path(__file__).resolve().parent
BASE = FOLDER.parent
def pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "lines": len(data.splitlines()),
            "sha256": hashlib.sha256(data).hexdigest()}
def atomic_new(path, data):
    if path.exists(): raise FileExistsError(str(path))
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as handle:
        handle.write(data); handle.flush(); os.fsync(handle.fileno())
    if temp.read_bytes() != data: raise RuntimeError("temporary byte verification failed")
    os.replace(temp, path)
inputs = [
BASE / "REGULARIDADE_KT_JATOS_20260909_224852/CERTIFICADO_POLINOMIAL_EINSTEIN_SIGMA.md",
BASE / "REGULARIDADE_KT_JATOS_20260909_224852/PRECISAO_CONSTRAINTS_E_COVARIANCIA.md",
BASE / "NORMALIDADE_RELATIVA_070_20260909_233414/NORMALIDADE_FORMAL_E_RESIDUO_SUAVE.md",
BASE / "TOPOLOGIA_BRST_SIGMA_070_20260909_233042_647697/TOPOLOGIA_ALVO_E_REDUCAO_H1.md",
BASE / "M2_SUAVE_RELATIVO_071_20260910_000347/M2_SUAVE_POR_COMPATIBILIDADE_E_SPENCER.md",
BASE / "M2_SUAVE_RELATIVO_071_20260910_000347/COROLARIO_H0_H1_E_FINITUDE.md",
BASE / "M2_SUAVE_RELATIVO_071_20260910_000347/PRECISAO_FATORACAO_FINITA_OPERADORES.md",
BASE / "M2_SUAVE_RELATIVO_071_20260910_000347/MANIFESTO_M2_SUAVE_RELATIVO_071.json",
]
reviews = [
BASE / "REVISOES_RAIZ_071_20260910/PARECER_COVARIANTIZACAO.md",
BASE / "REVISAO_COVARIANTIZACAO_071_20260910_001522/PARECER_COVARIANTIZACAO_SUAVE.md"
]
artifacts = [
FOLDER / "COVARIANTIZACAO_E_H2_GLOBAL.md",
FOLDER / "COROLARIO_H5_E_ANOMALIA_LOCAL.md",
FOLDER / "PRECISAO_GRADUACAO_E_COMPOSICAO.md"
]
before = {str(path): pin(path) for path in inputs + reviews + artifacts}
checks = []
for path in inputs + reviews + artifacts:
    current = pin(path)
    checks.append({"name": "byte_pin_stable", "path": str(path), "passed": current == before[str(path)]})
inherited_manifest = json.loads(inputs[-1].read_text(encoding="utf-8"))
for row in inherited_manifest["artifacts"]:
    current = pin(Path(row["path"]))
    checks.append({"name": "ordinary_input_matches_frozen_manifest", "path": row["path"],
                   "passed": current["bytes"] == row["bytes"] and current["sha256"] == row["sha256"]})
backup = list(FOLDER.glob("COROLARIO_H5_E_ANOMALIA_LOCAL.md.bak_*"))
checks.append({"name": "immediate_raw_byte_backup_exists_for_only_edit", "passed": len(backup) == 1})
checks.append({"name": "no_lean_or_um_artifacts_created_in_folder",
               "passed": not list(FOLDER.glob("*.lean")) and not list(FOLDER.glob("um.py"))})
failures = [x for x in checks if not x["passed"]]
manifest = {
"created_utc": datetime.now(timezone.utc).isoformat(),
"status": "DERIVED_WRITTEN__COVARIANT_H2_GLOBAL_TARGET__H5__LOCAL_H1_4_SMOOTH_VIELBEIN",
"documentary_checks_status": "PASS" if not failures else "FAIL",
"checks_passed": sum(x["passed"] for x in checks),
"checks_total": len(checks),
"failed_checks": failures,
"scope": "Finite smooth covariantization of ordinary characteristic degree2, global gluing on targetS3, and degree5/local anomaly corollary with coefficient class explicit.",
"results": [
{"claim": "H2_char_cov=0", "status": "DERIVED_WRITTEN", "class": "Natural tensors; finite polynomial differentiated jets; global smooth targetS3 coefficients; metric rational tensorial dependence; full Einstein-sigma ambient action."},
{"claim": "H5(s,B)=0", "status": "DERIVED_WRITTEN", "class": "Same covariant tensor algebra, ghosts and antifields; finite translation-ghost filtration."},
{"claim": "H1,4(s|d)=0", "status": "DERIVED_WRITTEN", "class": "Standard full local coordinate complex, smooth in vielbein values and globally smooth target coefficients, on a contractible spacetime chart; no spectator backgrounds."}
],
"mechanisms": [
"Ordinary smooth H0,H1,H2 + KT -> relative comparison.",
"Keep d(omega(x)) until zeroform BRST comparison.",
"Evaluate gauge jet pairs at an invertible vielbein, then finite Lorentz type projection.",
"Only4 translation +6 Lorentz ghosts remain: for a primitive of degree r, antigh<=10-r.",
"Finite Cech gluing retains s(partition of unity); H2(S3;R)=0 removes the constant obstruction.",
"Basic primitive beta0+F betaI0+F F betaIJ0; F^3=0 in4D.",
"Full smooth vielbein factor retains degrees0,3,6; rational dlogdet control prevents class promotion."
],
"limits": [
"Written proof, no Lean theorem or CAS verification.",
"Inputs L0-L2 are the explicit ordinary and KT written derivations pinned below.",
"No claim of an automatically admissible Q2 counterterm, especially with fixed spectator backgrounds.",
"No guarantee of a uniform derivative-order bound required by a particular renormalization scheme.",
"No QME, interacting physical state, background independence, global discrete anomaly classification or UV completeness claim.",
"No physical proof/confirmation of quantum gravity."
],
"artifacts": [before[str(p)] for p in artifacts],
"read_only_inputs": [before[str(p)] for p in inputs],
"review_documents": [{"pin": before[str(p)], "scope": "Independent analysis of principal H2 transport; not attributed as review of the separate H5 corollary."} for p in reviews],
"raw_byte_backups": [pin(p) for p in backup],
"measurement_script": pin(Path(__file__)),
"checks": checks,
"primary_sources": [
{"url": "https://arxiv.org/pdf/hep-th/9505173v2", "locations": "Sections3,4-7; AppendixC-E; equations3.6-3.8,6.7,6.15,E.11-E.20", "access": "Primary PDF via web tool; no local PDF digest asserted."},
{"url": "https://arxiv.org/pdf/hep-th/0002245v3", "locations": "Theorems6.2,7.1; Section7.3", "access": "Primary PDF via web tool; no local PDF digest asserted."},
{"url": "https://arxiv.org/pdf/math/9803115v1", "locations": "Section3.1; ordinary input scope", "access": "Primary PDF via web tool; no local PDF digest asserted."}
],
"executions": {"um_import_or_execution": False, "Lean": False, "CAS": False, "nature_tests": False, "Python_standard_library_document_generation_and_hashing": True},
"originals_or_frozen_inputs_modified": False,
"input_pins_stable_during_manifest_measurement": not failures,
"authorship": "Own written transport and corollary by selected_geometry_design. Reviews are existing documents read and pinned, not authored or approved on another agent's behalf."
}
path = FOLDER / "MANIFESTO_COVARIANTIZACAO_071.json"
atomic_new(path, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"manifest": pin(path), "status": manifest["documentary_checks_status"],
                  "checks_passed": manifest["checks_passed"], "checks_total": manifest["checks_total"],
                  "artifacts": manifest["artifacts"]}, ensure_ascii=False))
