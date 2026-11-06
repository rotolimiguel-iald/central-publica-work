"""Verificação algébrica do par de Bell sob fases locais e canal de espelho.

Sem dados observacionais. beta=0.1 é apenas uma escala simples de teste,
não uma calibração nem um ajuste da TGL.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

BETA = 0.1
ETA = 2.0 * np.sqrt(BETA * (1.0 - BETA))
OUT = Path(__file__).with_name("VERIFICACAO_BELL_ESPELHAMENTO.json")


def projector(v):
    return np.outer(v, v.conj())


def ptr_second(rho):
    return np.trace(rho.reshape(2, 2, 2, 2), axis1=1, axis2=3)


def ptr_first(rho):
    return np.trace(rho.reshape(2, 2, 2, 2), axis1=0, axis2=2)


def rz(phi):
    return np.diag([np.exp(-0.5j * phi), np.exp(0.5j * phi)])


def coherence(rho, P, Q):
    return 2.0 * float(np.sum(np.linalg.svd(P @ rho @ Q, compute_uv=False)))


def max_error(*matrices):
    return float(max(np.max(np.abs(m)) for m in matrices))


sqrt2 = np.sqrt(2.0)
phi_plus = np.array([1, 0, 0, 1], dtype=complex) / sqrt2
phi_minus = np.array([1, 0, 0, -1], dtype=complex) / sqrt2
psi_plus = np.array([0, 1, 1, 0], dtype=complex) / sqrt2
psi_minus = np.array([0, 1, -1, 0], dtype=complex) / sqrt2
P = projector(phi_plus)
R = projector(phi_minus)
X = np.outer(phi_plus, phi_minus.conj())
Q = np.eye(4, dtype=complex) - P

sin_theta_M = np.sqrt(BETA)
cos_theta_M = np.sqrt(1.0 - BETA)
M0 = cos_theta_M * P + sin_theta_M * Q
M1 = sin_theta_M * P + cos_theta_M * Q
M0_inv = (1.0 / cos_theta_M) * P + (1.0 / sin_theta_M) * Q

results = []
for phi in [0.0, np.pi / 8, np.pi / 4, 3 * np.pi / 8, np.pi / 2]:
    theta = 2.0 * phi
    c = np.cos(theta / 2.0)
    s = np.sin(theta / 2.0)

    # Os dois lados compartilham a fase: U=Rz(phi)⊗Rz(phi), logo theta=2phi.
    U_two = np.kron(rz(phi), rz(phi))
    U_one = np.kron(rz(phi), np.eye(2))
    chi_two = U_two @ phi_plus
    chi_one = U_one @ phi_plus
    chi_formula = c * phi_plus - 1j * s * phi_minus
    chi_formula_one = np.cos(phi / 2.0) * phi_plus - 1j * np.sin(phi / 2.0) * phi_minus

    rho = projector(chi_two)
    rho_formula = c**2 * P + s**2 * R + 1j * c * s * X - 1j * c * s * X.conj().T

    assert max_error(chi_two - chi_formula, chi_one - chi_formula_one) < 1e-10
    assert max_error(rho - rho_formula) < 1e-10
    assert max_error(ptr_first(rho) - np.eye(2) / 2, ptr_second(rho) - np.eye(2) / 2) < 1e-10
    assert abs(np.trace(rho) - 1.0) < 1e-10
    assert max_error(rho @ rho - rho) < 1e-10

    # Inversão exata do ramo, não do canal não-seletivo inteiro.
    branch = M0 @ rho @ M0
    branch_reconstructed = M0_inv @ branch @ M0_inv
    branch_error = max_error(branch_reconstructed - rho)
    assert branch_error < 1e-10

    rho_n = rho.copy()
    powers = []
    for n in range(5):
        expected_cross = (ETA**n) * 1j * c * s * X
        actual_cross = P @ rho_n @ Q
        expected_rho_n = c**2 * P + s**2 * R + (ETA**n) * (1j * c * s * X - 1j * c * s * X.conj().T)
        expected_visibility = abs(np.sin(theta)) * ETA**n
        actual_visibility = coherence(rho_n, P, Q)
        error = max_error(actual_cross - expected_cross, rho_n - expected_rho_n)
        assert error < 1e-10, (phi, n, error)
        assert abs(actual_visibility - expected_visibility) < 1e-10
        assert abs(np.trace(rho_n) - 1.0) < 1e-10
        assert np.min(np.linalg.eigvalsh(rho_n)) > -1e-10
        assert max_error(P @ rho_n @ P - c**2 * P, Q @ rho_n @ Q - s**2 * R) < 1e-10

        # Verificação direta dos projetores interferométricos do documento.
        detector_error = 0.0
        for chi_det in [-0.4, np.pi / 2, 1.0]:
            det_plus = (phi_plus + np.exp(-1j * chi_det) * phi_minus) / sqrt2
            det_minus = (phi_plus - np.exp(-1j * chi_det) * phi_minus) / sqrt2
            I_plus = np.vdot(det_plus, rho_n @ det_plus)
            I_minus = np.vdot(det_minus, rho_n @ det_minus)
            expected_I_plus = 0.5 * (1.0 + 2.0 * ETA**n * c * s * np.sin(chi_det))
            expected_I_minus = 0.5 * (1.0 - 2.0 * ETA**n * c * s * np.sin(chi_det))
            detector_error = max(
                detector_error,
                abs(I_plus - expected_I_plus),
                abs(I_minus - expected_I_minus),
                abs(I_plus + I_minus - 1.0),
            )
        assert detector_error < 1e-10, (phi, n, detector_error)

        powers.append({
            "n": n,
            "visibility_PQ": actual_visibility,
            "expected_visibility": expected_visibility,
            "cross_error": error,
            "detector_formula_error": detector_error,
            "trace": float(np.real(np.trace(rho_n))),
            "min_density_eigenvalue": float(np.min(np.linalg.eigvalsh(rho_n))),
        })
        rho_n = M0 @ rho_n @ M0 + M1 @ rho_n @ M1

    results.append({
        "phi_each_side": float(phi),
        "theta_relative_pair": float(theta),
        "input_is_phi_plus": max_error(chi_two - phi_plus) < 1e-10,
        "input_is_phi_minus_up_to_phase": max_error(chi_two + 1j * phi_minus) < 1e-10,
        "input_PQ_coherence": coherence(rho, P, Q),
        "one_side_PQ_coherence": coherence(projector(chi_one), P, Q),
        "expected_two_side_coherence": abs(np.sin(2.0 * phi)),
        "expected_one_side_coherence": abs(np.sin(phi)),
        "marginal_first": ptr_first(rho).real.tolist(),
        "marginal_second": ptr_second(rho).real.tolist(),
        "branch_reconstruction_error": branch_error,
        "powers": powers,
    })

by_phase = {round(r["phi_each_side"], 12): r for r in results}
zero = by_phase[round(0.0, 12)]
max_case = by_phase[round(np.pi / 4, 12)]
transfer = by_phase[round(np.pi / 2, 12)]
assert zero["input_is_phi_plus"]
assert zero["input_PQ_coherence"] < 1e-12
assert abs(max_case["input_PQ_coherence"] - 1.0) < 1e-12
assert abs(max_case["powers"][1]["visibility_PQ"] - ETA) < 1e-12
assert transfer["input_is_phi_minus_up_to_phase"]
assert transfer["input_PQ_coherence"] < 1e-12
for r in results:
    assert abs(r["input_PQ_coherence"] - r["expected_two_side_coherence"]) < 1e-10
    assert abs(r["one_side_PQ_coherence"] - r["expected_one_side_coherence"]) < 1e-10

payload = {
    "status": "ALL_BELL_MIRROR_CHECKS_PASSED",
    "no_data_used": True,
    "beta_test_scale_only": BETA,
    "eta_test": ETA,
    "definitions": {
        "P": "|Phi+><Phi+|",
        "Q": "I-P",
        "input": "Rz(phi)⊗Rz(phi) |Phi+>",
        "theta": "2*phi",
        "chi": "cos(theta/2)|Phi+> - i sin(theta/2)|Phi->",
        "PQ_visibility": "2 ||P rho Q||_1 = |sin(theta)|",
        "mirror_visibility_after_n": "|sin(theta)| * eta^n",
        "eta": "2 sqrt(beta(1-beta))",
        "maximum_coherence_input": "phi=pi/4 each side => theta=pi/2",
        "full_transfer_input": "phi=pi/2 each side => theta=pi => |Phi-> up to phase, no PQ coherence",
    },
    "results": results,
}
OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps({
    "status": payload["status"],
    "eta_test": ETA,
    "cases": [
        {
            "phi_each_side": r["phi_each_side"],
            "theta_pair": r["theta_relative_pair"],
            "initial_PQ_visibility": r["input_PQ_coherence"],
            "after_one_crossing": r["powers"][1]["visibility_PQ"],
            "branch_reconstruction_error": r["branch_reconstruction_error"],
        }
        for r in results
    ],
    "output": str(OUT),
}, indent=2, ensure_ascii=False))
