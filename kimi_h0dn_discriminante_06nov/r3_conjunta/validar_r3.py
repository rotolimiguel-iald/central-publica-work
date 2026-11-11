from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAN_PATH = HERE / "analysis_plan_r3.json"
DOC_PATH = HERE / "PRE_REGISTRO_R3_DISCRIMINACAO_CONJUNTA.md"
DIAGNOSTIC_PATH = HERE / "R3_DIAGNOSTICO_ESCORES_R2.json"
OUT_PATH = HERE / "PREFLIGHT_R3.json"
OBSERVED_PATH = HERE / "OBSERVED_RESULTS_R3.json"


def pin(path: Path) -> dict:
    return {
        "path": str(path.resolve()),
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the blocked R3 preregistration without opening data.")
    parser.add_argument("--request-observed-opening", action="store_true")
    args = parser.parse_args()

    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    diagnostic = json.loads(DIAGNOSTIC_PATH.read_text(encoding="utf-8"))
    if plan["status"] != "CANDIDATE_BLOCKED_NOT_FROZEN":
        raise ValueError("R3 status is not the expected blocked candidate")
    if plan["opening"]["enabled"] or plan["opening"]["opening_allowed_now"]:
        raise ValueError("Candidate plan unexpectedly enables observed opening")
    if plan["opening"]["observed_fit_performed"]:
        raise ValueError("Observed fit flag is not false")
    if diagnostic["score_blocks_hash_verified"] != 56:
        raise ValueError("R2 score verification is incomplete")
    if diagnostic["observed_fit"] or diagnostic["observed_data_used"]:
        raise ValueError("Diagnostic violates the no-observed-fit rule")

    primary = plan["primary_model"]
    secondary = plan["secondary_diagnostic_model"]
    primary_ref = diagnostic["summary_no_nuisance"][f"{primary}__hypothesis_1"]
    secondary_ref = diagnostic["summary_no_nuisance"][f"{secondary}__hypothesis_1"]
    if primary_ref["exact_joint"]["estimate"] != plan["power_gate"]["current_r2_reference_exact_joint_power"]:
        raise ValueError("Primary reference power mismatch")
    if secondary_ref["exact_joint"]["estimate"] != plan["power_gate"]["current_r2_reference_secondary_exact_joint_power"]:
        raise ValueError("Secondary reference power mismatch")

    open_gates = [gate["id"] for gate in plan["required_gates"] if gate["status"] != "CLOSED"]
    opening_gates = [gate for gate in open_gates if not gate.startswith("G10_")]
    reasons = [f"REQUIRED_GATE_OPEN:{gate}" for gate in opening_gates]
    current_power = primary_ref["exact_joint"]["estimate"]
    if current_power < plan["power_gate"]["minimum_primary_exact_joint_power_for_confirmatory_opening"]:
        reasons.append(f"PRIMARY_POWER_BELOW_CONFIRMATION_GATE:{current_power}<0.90")

    observed_present = OBSERVED_PATH.exists()
    if observed_present:
        reasons.append("FORBIDDEN_OBSERVED_RESULTS_FILE_PRESENT")

    pins = [pin(PLAN_PATH), pin(DOC_PATH), pin(Path(__file__)), pin(DIAGNOSTIC_PATH)]
    pins.extend(pin(Path(source)) for source in plan["sources"] if Path(source) != DIAGNOSTIC_PATH)
    payload = {
        "status": "R3_PREFLIGHT_BLOCKED",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "candidate_is_not_freeze": True,
        "opening_requested_by_cli": bool(args.request_observed_opening),
        "opening_allowed": False,
        "opening_refusal_reasons": reasons,
        "required_gates_not_closed": open_gates,
        "G10_scope": "Required before any claim beyond one determination; not required merely to save this candidate plan",
        "observed_results_file_present": observed_present,
        "observed_fit_performed": False,
        "new_seeds_generated": False,
        "plan_consistency": "PASS",
        "source_integrity": "PINNED_CURRENT_BYTES",
        "primary_reference_exact_joint_power": current_power,
        "secondary_reference_exact_joint_power": secondary_ref["exact_joint"]["estimate"],
        "confirmatory_power_threshold": plan["power_gate"]["minimum_primary_exact_joint_power_for_confirmatory_opening"],
        "nature_verdict": False,
        "gate_effect": "NONE",
        "pins": pins,
    }
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": payload["status"],
        "opening_allowed": False,
        "opening_refusal_reasons": reasons,
        "observed_results_file_present": observed_present,
        "output": str(OUT_PATH),
        "output_sha256": pin(OUT_PATH)["sha256"],
    }, ensure_ascii=False, indent=2))
    if observed_present:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
