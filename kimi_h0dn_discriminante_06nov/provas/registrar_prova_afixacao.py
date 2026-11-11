from pathlib import Path
import hashlib
import json
import re
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "AfixacaoTemporalR1.lean"
LOG = HERE / "AfixacaoTemporalR1_build.log"
OUT = HERE / "AfixacaoTemporalR1_receipt.json"
EXPECTED = ["propext", "Classical.choice", "Quot.sound"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


source = SOURCE.read_text(encoding="utf-8")
log = LOG.read_text(encoding="utf-8")
declared = re.findall(r"^(?:lemma|theorem)\s+([A-Za-z0-9_]+)", source, re.MULTILINE)
reported = {
    name: [item.strip() for item in axioms.split(",")]
    for name, axioms in re.findall(
        r"'TGLExt.AfixacaoTemporal.([A-Za-z0-9_]+)' depends on axioms: \[([^]]*)\]", log
    )
}
assert set(declared) == set(reported), (set(declared) - set(reported), set(reported) - set(declared))
assert len(declared) == 13
assert "sorryAx" not in log
assert "error:" not in log
assert all(axioms == EXPECTED for axioms in reported.values())

receipt = {
    "status": "AFIXACAO_TEMPORAL_R1_COMPILED",
    "stone_status": "CANDIDATE_R1_NOT_SEALED",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "source": str(SOURCE),
    "source_sha256": sha(SOURCE),
    "build_log": str(LOG),
    "build_log_sha256": sha(LOG),
    "build_exit_code": 0,
    "compiler_errors": 0,
    "lean_version": "4.31.0",
    "mathlib_input_rev": "v4.31.0",
    "theorem_count": len(declared),
    "theorems": declared,
    "axiom_report": reported,
    "all_theorems_in_standard_trio": True,
    "sorryAx_absent": True,
    "scope": {
        "physical_instrument_implemented": False,
        "optical_rival_measured": False,
        "axis_PQ_fixed_in_nature": False,
        "new_nature_test": False,
        "gate_moved": False,
        "aggregation_rule_source_confirmation": "OPEN",
        "physical_covariance": "OPEN",
    },
}
OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "status": receipt["status"],
    "theorem_count": len(declared),
    "source_sha256": receipt["source_sha256"],
    "log_sha256": receipt["build_log_sha256"],
    "receipt": str(OUT),
}, indent=2))
