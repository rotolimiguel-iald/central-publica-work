"""Finite computational adaptation; provider semantics are engineering inputs.

Sources: one_supercondutor.py (ACOM, support, H_min and pinching).
This module neither executes the sealed runner nor asserts a physical effect.
The provider-admissibility projector is NEW; it is not the runner's q_F.
"""
from __future__ import annotations

import math

ALPHA_FINE_CODATA_2018 = 0.0072973525693


def beta() -> float:
    return ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)


def matmul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def projector(mask):
    return [[float(i == j and flag) for j in range(len(mask))] for i, flag in enumerate(mask)]


def pinching(matrix, mask):
    return [[value if mask[i] == mask[j] else 0.0 for j, value in enumerate(row)]
            for i, row in enumerate(matrix)]


def select_support(ids, weights, mask):
    """ACOM round-trip -> pinching -> support -> normalized decision weights.

Finite damping is recorded, NEVER used as an authorization filter. Ineligible
channels are removed exactly by Q; argmax is a separate engineering decision.
"""
    if not ids or len(ids) > 64 or len(set(ids)) != len(ids):
        raise ValueError("Invalid candidate identities")
    if len(weights) != len(ids) or len(mask) != len(ids) or any(type(v) is not bool for v in mask):
        raise ValueError("Invalid matrix dimensions or support")
    if any(not math.isfinite(w) or w < 0 for w in weights):
        raise ValueError("Weights must be finite and nonnegative")
    if sum(weights) <= 0:
        raise ValueError("Empty input mass")
    reflected = [math.sqrt(w) for w in weights]
    recovered = [g * g for g in reflected]
    residual = max(abs(a - b) for a, b in zip(weights, recovered)) / max(1.0, max(weights))
    if residual > 1e-12:
        raise ValueError("ACOM reconstruction failed")
    scale = max(recovered)
    scaled = [w / scale for w in recovered]
    total = sum(scaled)
    amplitudes = [math.sqrt(w / total) for w in scaled]
    rho = [[a * b for b in amplitudes] for a in amplitudes]
    q = projector(mask)
    h = projector([not flag for flag in mask])
    e = pinching(rho, mask)
    projected = matmul(matmul(q, e), q)
    retained = sum(projected[i][i] for i in range(len(ids)))
    if retained <= 0:
        return {"status": "NO_ELIGIBLE_PROVIDER", "selected": None, "probabilities": {},
                "support": mask, "acom_residual": residual, "discarded_mass": 1.0}
    probabilities = {name: projected[i][i] / retained for i, name in enumerate(ids)}
    selected = max((name for name, flag in zip(ids, mask) if flag), key=probabilities.get)
    damping = [1.0 if flag else math.exp(-beta()) for flag in mask]
    return {"status": "SELECTED", "selected": selected, "probabilities": probabilities,
            "support": mask, "rho": rho, "pinched_rho": e, "q_admissible": q, "h_min": h,
            "damping_diagonal": damping, "beta_runtime": beta(), "acom_residual": residual,
            "discarded_mass": max(0.0, 1.0 - retained),
            "scope": "DERIVED: finite matrix operations; INPUT: provider mapping and utility; physical_verdict_allowed=false"}
