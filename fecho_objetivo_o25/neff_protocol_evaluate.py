#!/usr/bin/env python3
"""Deterministic evaluator for TGL_NEFF_CMBHD_SO_20261026_V1.

This program evaluates data; it does not acquire them and never turns a synthetic
smoke test into a natural measurement. It uses only the Python standard library.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
PROTOCOL_PATH = ROOT / "NEFF_PROSPECTIVE_PROTOCOL_V1.json"
EXPECTED_PROTOCOL_SHA256 = "c2c731afe3fa14bfd6a396205a63981a0b09ba07f39818164de27370d8b189f3"
POSITIVE = "MATCHED_PROSPECTIVELY_ABOVE_5SIGMA_WITH_INDEPENDENT_REPLICATION"
SIGMA_KEYS = [
    "sigma_stat",
    "sigma_systematic",
    "sigma_foreground",
    "sigma_delensing",
    "sigma_theory_implementation",
]


def load_protocol() -> dict[str, Any]:
    raw = PROTOCOL_PATH.read_bytes()
    actual = sha256(raw).hexdigest()
    if actual != EXPECTED_PROTOCOL_SHA256:
        raise ValueError(f"Protocol hash mismatch: expected {EXPECTED_PROTOCOL_SHA256}, got {actual}")
    protocol = json.loads(raw)
    if not protocol.get("prediction_frozen"):
        raise ValueError("Protocol is not frozen")
    return protocol


def sigma_total(record: dict[str, Any]) -> float:
    values = []
    for key in SIGMA_KEYS:
        value = float(record.get(key, 0.0))
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{key} must be finite and nonnegative")
        values.append(value * value)
    total = math.sqrt(sum(values))
    if not math.isfinite(total) or total <= 0:
        raise ValueError("Total sigma must be strictly positive")
    return total


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"Naive timestamp is not eligible: {value}")
    return parsed.astimezone(timezone.utc)


def joint_measurement(hd: dict[str, Any], so: dict[str, Any], covariance: float) -> tuple[float, float]:
    """Inverse-covariance combination for two measurements and their cross-covariance."""
    a, b = sigma_total(hd) ** 2, sigma_total(so) ** 2
    if not math.isfinite(covariance) or a * b - covariance * covariance <= 0:
        raise ValueError("Cross-covariance must define a positive-definite covariance matrix")
    denominator = a + b - 2 * covariance
    if denominator <= 0:
        raise ValueError("Combined variance must be positive")
    mean = ((b - covariance) * float(hd["n_eff"]) +
            (a - covariance) * float(so["n_eff"])) / denominator
    variance = (a * b - covariance * covariance) / denominator
    return mean, math.sqrt(variance)


def evaluate(protocol: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    kind = payload.get("input_kind")
    if kind not in {"PROSPECTIVE_NEW_DATA", "SYNTHETIC_SMOKE_TEST"}:
        raise ValueError("input_kind must be PROSPECTIVE_NEW_DATA or SYNTHETIC_SMOKE_TEST")
    synthetic = kind == "SYNTHETIC_SMOKE_TEST"
    hd, so = payload["hd"], payload["so"]
    n_tgl = float(protocol["prediction"]["N_eff_TGL"])
    n_sm = float(protocol["prediction"]["N_SM"])
    threshold = float(protocol["power"]["sigma_required_for_nominal_5sigma_separation"])
    hd_sigma, so_sigma = sigma_total(hd), sigma_total(so)
    joint_n, joint_sigma = joint_measurement(hd, so, float(payload.get("cross_covariance", 0.0)))
    frozen_at = parse_time(protocol["created_at_utc"])
    hd_new = parse_time(hd["data_frozen_utc"]) > frozen_at
    so_new = parse_time(so["data_frozen_utc"]) > frozen_at
    eligible_dates = hd_new and so_new
    gates = bool(hd.get("validation_gates_passed")) and bool(so.get("validation_gates_passed"))
    independent = bool(so.get("independent_from_primary"))

    hd_match = abs(float(hd["n_eff"]) - n_tgl) / hd_sigma <= 1
    hd_separation = (float(hd["n_eff"]) - n_sm) / hd_sigma
    so_replication = ((float(so["n_eff"]) - n_sm) > 0 and
                      abs(float(so["n_eff"]) - n_tgl) / so_sigma <= 2 and independent)
    joint_separation = (joint_n - n_sm) / joint_sigma
    hd_away = abs(float(hd["n_eff"]) - n_tgl) / hd_sigma
    so_away = abs(float(so["n_eff"]) - n_tgl) / so_sigma
    matched_conditions = (hd_match and hd_separation >= 5 and so_replication and
                          joint_separation >= 5 and independent)
    falsified_conditions = hd_away >= 5 and so_away >= 5

    if not gates:
        verdict = "INCONCLUSIVE_SYSTEMATICS"
    elif not eligible_dates:
        verdict = "INELIGIBLE_HISTORICAL_DATA"
    elif not independent:
        verdict = "INCONCLUSIVE_INDEPENDENCE"
    elif falsified_conditions:
        verdict = "TGL_NEFF_FALSIFIED"
    elif matched_conditions:
        verdict = POSITIVE
    elif hd_sigma > threshold:
        verdict = "NOT_FALSIFIED_UNDERPOWERED"
    elif hd_away >= 3 or so_away >= 3:
        verdict = "TGL_NEFF_TENSION"
    else:
        verdict = "NOT_FALSIFIED_INCONCLUSIVE"
    if synthetic:
        verdict = "SYNTHETIC_ONLY__" + verdict

    return {
        "schema": "tgl.prospective-evaluation.v1",
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": EXPECTED_PROTOCOL_SHA256,
        "input_kind": kind,
        "synthetic_input": synthetic,
        "nature_result": "NOT_RUN_SYNTHETIC" if synthetic else "EVALUATED_NEW_DATA",
        "verdict": verdict,
        "experimental_confirmation_claimed": False,
        "metrics": {
            "N_eff_TGL": n_tgl,
            "N_SM": n_sm,
            "HD_n_eff": float(hd["n_eff"]),
            "HD_sigma_total": hd_sigma,
            "HD_separation_from_SM_sigma": hd_separation,
            "HD_distance_from_TGL_sigma": hd_away,
            "SO_n_eff": float(so["n_eff"]),
            "SO_sigma_total": so_sigma,
            "SO_distance_from_TGL_sigma": so_away,
            "joint_n_eff": joint_n,
            "joint_sigma_total": joint_sigma,
            "joint_separation_from_SM_sigma": joint_separation,
            "cross_covariance": float(payload.get("cross_covariance", 0.0)),
        },
        "gates": {
            "validation_passed": gates,
            "eligible_new_dates": eligible_dates,
            "independent_replication": independent,
            "primary_match": hd_match,
            "primary_separation_at_least_5sigma": hd_separation >= 5,
            "replication_rule_passed": so_replication,
            "global_separation_at_least_5sigma": joint_separation >= 5,
        },
        "interpretation": "Synthetic pipeline validation only; not natural evidence" if synthetic else
            "Prospective rule evaluation; MATCHED is not CONFIRMED and systematics/independence remain mandatory",
    }


def smoke_payload(center: float, *, kind: str = "SYNTHETIC_SMOKE_TEST") -> dict[str, Any]:
    record = lambda sigma: {
        "n_eff": center,
        "sigma_stat": sigma,
        "sigma_systematic": 0.0,
        "sigma_foreground": 0.0,
        "sigma_delensing": 0.0,
        "sigma_theory_implementation": 0.0,
        "validation_gates_passed": True,
        "data_frozen_utc": "2027-01-01T00:00:00Z",
    }
    return {
        "input_kind": kind,
        "cross_covariance": 0.0,
        "hd": record(0.014),
        "so": record(0.045) | {"independent_from_primary": True},
    }


def self_test(protocol: dict[str, Any]) -> None:
    n_tgl = float(protocol["prediction"]["N_eff_TGL"])
    n_sm = float(protocol["prediction"]["N_SM"])
    assert evaluate(protocol, smoke_payload(n_tgl))["verdict"] == "SYNTHETIC_ONLY__" + POSITIVE
    independent_case = smoke_payload(n_tgl)
    joint_n, joint_sigma = joint_measurement(independent_case["hd"], independent_case["so"], 0.0)
    expected_sigma = math.sqrt((0.014 ** 2 * 0.045 ** 2) / (0.014 ** 2 + 0.045 ** 2))
    assert math.isclose(joint_n, n_tgl, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(joint_sigma, expected_sigma, rel_tol=0.0, abs_tol=1e-12)
    correlated_case = smoke_payload(n_tgl)
    correlated_case["cross_covariance"] = 0.00005
    assert evaluate(protocol, correlated_case)["verdict"] == "SYNTHETIC_ONLY__" + POSITIVE
    assert evaluate(protocol, smoke_payload(n_sm))["verdict"] == "SYNTHETIC_ONLY__TGL_NEFF_TENSION"
    assert evaluate(protocol, smoke_payload(2.0))["verdict"] == "SYNTHETIC_ONLY__TGL_NEFF_FALSIFIED"
    low_power = smoke_payload(n_tgl)
    low_power["hd"]["sigma_stat"] = 0.1
    assert evaluate(protocol, low_power)["verdict"] == "SYNTHETIC_ONLY__NOT_FALSIFIED_UNDERPOWERED"
    historical = smoke_payload(n_tgl)
    historical["hd"]["data_frozen_utc"] = "2026-01-01T00:00:00Z"
    assert evaluate(protocol, historical)["verdict"] == "SYNTHETIC_ONLY__INELIGIBLE_HISTORICAL_DATA"
    systematics = smoke_payload(n_tgl)
    systematics["so"]["validation_gates_passed"] = False
    assert evaluate(protocol, systematics)["verdict"] == "SYNTHETIC_ONLY__INCONCLUSIVE_SYSTEMATICS"
    dependent = smoke_payload(n_tgl)
    dependent["so"]["independent_from_primary"] = False
    assert evaluate(protocol, dependent)["verdict"] == "SYNTHETIC_ONLY__INCONCLUSIVE_INDEPENDENCE"
    print("SELF_TEST_PASS: positive, tension, falsification, power, dates, systematics, independence")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, help="JSON measurement input")
    parser.add_argument("-o", "--output", type=Path, help="Write the evaluation receipt here")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    protocol = load_protocol()
    if args.self_test:
        self_test(protocol)
        return
    if args.input is None:
        parser.error("input is required unless --self-test is used")
    raw = args.input.read_bytes()
    payload = json.loads(raw)
    result = evaluate(protocol, payload)
    result["evaluated_at_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    result["input_sha256"] = sha256(raw).hexdigest()
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
