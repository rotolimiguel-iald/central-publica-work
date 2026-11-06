"""Verificação algébrica do lock arbitrário no Mach–Zehnder de um fóton.

Não usa dados observacionais. beta é apenas uma escala positiva de verificação;
não é uma calibração física nem um ajuste.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

BETA = 0.2
T = 50.0  # beta*T = 10
OUT = Path(__file__).with_name("VERIFICACAO_LOCK_GERAL.json")


def unit(v):
    v = np.asarray(v, dtype=complex)
    return v / np.linalg.norm(v)


def ket(*entries):
    return np.asarray(entries, dtype=complex)


def rho_of(psi):
    return np.outer(psi, psi.conj())


def evolve(K, psi, time=T):
    """Solução exata para L=sqrt(beta*K), com K hermitiano positivo."""
    values, vectors = np.linalg.eigh(K)
    values = np.clip(values, 0.0, None)
    ell = np.sqrt(BETA * values)
    rho0_e = vectors.conj().T @ rho_of(psi) @ vectors
    attenuation = np.exp(-0.5 * (ell[:, None] - ell[None, :]) ** 2 * time)
    rho_t_e = rho0_e * attenuation
    rho_t = vectors @ rho_t_e @ vectors.conj().T
    return rho_t, values, 0.5 * BETA * (np.sqrt(values[1]) - np.sqrt(values[0])) ** 2


def lock_reference_solution(omega, psi, time=T):
    """Mesma evolução na base explícita paralela/ortogonal a QOmega."""
    projected = omega[:2]
    r2 = float(np.vdot(projected, projected).real)
    if r2 == 0:
        return rho_of(psi), None
    u, v = projected / np.sqrt(r2)
    E = np.array([[u, -np.conj(v)], [v, np.conj(u)]], dtype=complex)
    gamma = 0.5 * BETA * (1.0 - np.sqrt(max(0.0, 1.0 - r2))) ** 2
    rho0_e = E.conj().T @ rho_of(psi) @ E
    f = np.exp(-gamma * time)
    rho_t_e = np.array([
        [rho0_e[0, 0], f * rho0_e[0, 1]],
        [f * rho0_e[1, 0], rho0_e[1, 1]],
    ])
    return E @ rho_t_e @ E.conj().T, gamma


def clean(x):
    return float(np.real_if_close(x))


cases = [
    ("vacuum_outside_paths", ket(0, 0, 1), unit(ket(1, 1j))),
    ("path_aligned_full_r1", ket(1, 0, 0), unit(ket(1, 1j))),
    ("path_aligned_partial_r06", ket(0.6, 0, 0.8), unit(ket(1, 1j))),
    ("generic_reference", ket(0.36, 0.48, 0.8), unit(ket(1, 2j))),
    ("self_lock_balanced", unit(ket(1, 1j, 0)), unit(ket(1, 1j))),
    ("symmetric_lock_path_input", unit(ket(1, 1, 0)), ket(1, 0)),
]

results = []
for name, omega, psi in cases:
    omega = unit(omega)
    psi = unit(psi)
    projected = omega[:2]
    r2 = float(np.vdot(projected, projected).real)
    K = np.eye(3, dtype=complex) - np.outer(omega, omega.conj())
    K2 = K[:2, :2]
    rho0 = rho_of(psi)
    rho_t, eigenvalues, gamma_eigen = evolve(K2, psi)
    rho_reference, gamma_reference = lock_reference_solution(omega, psi)

    expected_eigenvalues = np.array([1.0 - r2, 1.0])
    expected_gamma = 0.5 * BETA * (1.0 - np.sqrt(max(0.0, 1.0 - r2))) ** 2
    eigen_error = float(np.max(np.abs(np.sort(eigenvalues) - expected_eigenvalues)))
    gamma_error = abs(float(gamma_eigen) - expected_gamma)
    if gamma_reference is not None:
        gamma_error = max(gamma_error, abs(float(gamma_reference) - expected_gamma))
        reference_error = float(np.max(np.abs(rho_t - rho_reference)))
    else:
        reference_error = float(np.max(np.abs(rho_t - rho0)))

    population_change = float(np.max(np.abs(np.diag(rho_t) - np.diag(rho0))))
    trace_error = abs(complex(np.trace(rho_t)) - 1.0)
    min_density_eigenvalue = float(np.min(np.linalg.eigvalsh(rho_t)))
    initial_coherence = abs(rho0[0, 1])
    visibility_ratio = None if initial_coherence < 1e-12 else float(abs(rho_t[0, 1]) / initial_coherence)

    assert eigen_error < 1e-10, (name, eigen_error)
    assert gamma_error < 1e-10, (name, gamma_error)
    assert reference_error < 1e-10, (name, reference_error)
    assert trace_error < 1e-10, (name, trace_error)
    assert min_density_eigenvalue > -1e-10, (name, min_density_eigenvalue)

    results.append({
        "case": name,
        "r2": r2,
        "K_path": [[[float(z.real), float(z.imag)] for z in row] for row in K2],
        "eigenvalues_K_path": eigenvalues.tolist(),
        "expected_eigenvalues": expected_eigenvalues.tolist(),
        "Gamma": float(gamma_eigen),
        "expected_Gamma": expected_gamma,
        "eigen_error": eigen_error,
        "gamma_error": gamma_error,
        "reference_solution_error": reference_error,
        "population_change": population_change,
        "trace_error": trace_error,
        "min_density_eigenvalue": min_density_eigenvalue,
        "visibility_ratio_if_defined": visibility_ratio,
    })

by_name = {r["case"]: r for r in results}
assert by_name["vacuum_outside_paths"]["r2"] == 0.0
assert by_name["vacuum_outside_paths"]["Gamma"] == 0.0
assert by_name["vacuum_outside_paths"]["population_change"] < 1e-12
assert abs(by_name["path_aligned_full_r1"]["Gamma"] - BETA / 2) < 1e-12
assert by_name["path_aligned_full_r1"]["population_change"] < 1e-12
assert by_name["path_aligned_partial_r06"]["population_change"] < 1e-12
assert by_name["self_lock_balanced"]["population_change"] < 1e-12
assert abs(by_name["self_lock_balanced"]["visibility_ratio_if_defined"] - 1.0) < 1e-12
assert np.hypot(*by_name["symmetric_lock_path_input"]["K_path"][0][1]) > 0.1
assert by_name["symmetric_lock_path_input"]["population_change"] > 0.1

payload = {
    "status": "ALL_GENERAL_LOCK_CHECKS_PASSED",
    "no_data_used": True,
    "model": "K=I-|Omega><Omega|, L=sqrt(beta*K), single-photon path subspace",
    "beta_test_scale_only": BETA,
    "T_test": T,
    "general_formulas": {
        "r2": "||Q Omega||^2",
        "eigenvalues": [ "1-r2", "1" ],
        "Gamma": "beta/2 * (1-sqrt(1-r2))^2",
        "full_0_1_requirement": "r2=1 and QOmega aligned to one path for path-diagonal populations",
        "vacuum_result": "r2=0 => k_A=k_B=1 => Gamma=0",
        "self_lock_result": "initial state is the lock zero mode => no evolution",
    },
    "results": results,
}
OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps({
    "status": payload["status"],
    "cases": [
        {
            "case": r["case"],
            "r2": r["r2"],
            "Gamma": r["Gamma"],
            "population_change": r["population_change"],
            "visibility_ratio_if_defined": r["visibility_ratio_if_defined"],
        }
        for r in results
    ],
    "output": str(OUT),
}, indent=2, ensure_ascii=False))
