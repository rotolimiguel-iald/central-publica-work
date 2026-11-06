from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_05nov")
SOURCE = ROOT / "BellEspelhamentoR1.lean"
LOG = ROOT / "BellEspelhamentoR1_build.log"
RECEIPT = ROOT / "BellEspelhamentoR1_receipt.json"
NUMERIC = Path(
    r"C:\IALD\Central de Patentes\work\coerencia_espectro_fotometria_05nov"
    r"\VERIFICACAO_BELL_ESPELHAMENTO.json"
)
MANIFEST = Path(
    r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\lake-manifest.json"
)
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
NAMESPACE = "TGLExt.BellEspelhamento"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


source_text = SOURCE.read_text(encoding="utf-8")
log_text = LOG.read_text(encoding="utf-8")
declared = re.findall(r"^(?:lemma|theorem)\s+([A-Za-z0-9_]+)", source_text, re.MULTILINE)
reported = {
    name: [item.strip() for item in axioms.split(",")]
    for name, axioms in re.findall(
        rf"'{re.escape(NAMESPACE)}\.([A-Za-z0-9_]+)' depends on axioms: \[([^]]*)\]",
        log_text,
    )
}

assert len(declared) == len(set(declared)), "Declarações Lean duplicadas"
assert set(declared) == set(reported), (
    f"Auditoria incompleta: faltam {set(declared) - set(reported)}; "
    f"sobram {set(reported) - set(declared)}"
)
assert "sorryAx" not in log_text, "sorryAx encontrado no log"
assert "error:" not in log_text, "Erro de compilação encontrado no log"
assert all(axioms == EXPECTED_AXIOMS for axioms in reported.values()), reported

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
mathlib = next(package for package in manifest["packages"] if package["name"] == "mathlib")
numeric = json.loads(NUMERIC.read_text(encoding="utf-8"))
assert numeric["status"] == "ALL_BELL_MIRROR_CHECKS_PASSED"

receipt = {
    "status": "BELL_MIRROR_STONE_R1_COMPILED",
    "stone_status": "CANDIDATE_R1_NOT_SEALED",
    "created_at_local": datetime.now().astimezone().isoformat(),
    "source": str(SOURCE),
    "source_sha256": sha256(SOURCE),
    "build_log": str(LOG),
    "build_log_sha256": sha256(LOG),
    "build_exit_code": 0,
    "compiler_errors": 0,
    "linter_warnings_nonfatal": log_text.count("warning:"),
    "toolchain": {
        "lake_executable": r"C:\Users\rotol\.elan\bin\lake.exe",
        "lean_version": "4.31.0",
        "lean_commit": "68218e876d2a38b1985b8590fff244a83c321783",
        "lean_toolchain_file": "leanprover/lean4:v4.31.0",
        "mathlib_input_rev": mathlib["inputRev"],
        "mathlib_rev": mathlib["rev"],
    },
    "build_command": (
        "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory "
        "GIT_CONFIG_VALUE_0='*' "
        r'"C:\Users\rotol\.elan\bin\lake.exe" env lean '
        r'"C:\IALD\Central de Patentes\work\pedras_candidatas_05nov\BellEspelhamentoR1.lean"'
    ),
    "namespace": NAMESPACE,
    "theorem_count": len(declared),
    "theorems": declared,
    "axiom_report": reported,
    "axiom_audit_complete": True,
    "all_theorems_in_standard_trio": True,
    "sorryAx_absent": True,
    "numeric_crosscheck": {
        "path": str(NUMERIC),
        "sha256": sha256(NUMERIC),
        "status": numeric["status"],
        "no_data_used": numeric["no_data_used"],
    },
    "scope": {
        "new_nature_test": False,
        "new_data": False,
        "gate_moved": False,
        "beta_identification_external_to_lean": True,
        "bell_fock_tt_bridge": "OPEN",
        "physical_channel_realization": "OPEN",
        "physical_validity_established": False,
    },
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "status": receipt["status"],
    "theorem_count": len(declared),
    "all_theorems_in_standard_trio": True,
    "sorryAx_absent": True,
    "source_sha256": receipt["source_sha256"],
    "receipt": str(RECEIPT),
}, ensure_ascii=False, indent=2))
