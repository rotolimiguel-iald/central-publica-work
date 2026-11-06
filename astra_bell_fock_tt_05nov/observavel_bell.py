"""Reproduce the Bell-channel algebra and a conservative prospective counting design."""
import hashlib
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ONE = np.eye(4)
A = np.array([1, 0, 0, 1]) / math.sqrt(2)
B = np.array([1, 0, 0, -1]) / math.sqrt(2)
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.diag([1, -1])
TOL = 3e-13


def outer(ket):
    return np.outer(ket, ket.conj())


def close(actual, expected):
    np.testing.assert_allclose(actual, expected, atol=TOL, rtol=0)


def verify_algebra(beta):
    p, r = outer(A), outer(B)
    q = ONE - p
    u, v = math.sqrt(1 - beta), math.sqrt(beta)
    eta = 2 * u * v
    m0, m1 = u * p + v * q, v * p + u * q
    w = p - q
    env_p = np.array([[u, -v], [v, u]])
    env_q = np.array([[v, -u], [u, v]])
    joint = np.kron(p, env_p) + np.kron(q, env_q)
    close(joint.conj().T @ joint, np.eye(8))
    close(m0.conj().T @ m0 + m1.conj().T @ m1, ONE)
    flip_probability = (1 - eta) / 2
    swap = ONE[[0, 2, 1, 3]]
    symmetric = (ONE + swap) / 2
    collective_y = np.kron(Y, Y)
    close(w, -collective_y @ swap)
    close(w @ symmetric, -collective_y @ symmetric)
    # Tagged ports: A is fixed at 0; only the preparation at B changes.
    left_one = np.diag([0, 0, 1, 1])
    left_response = []
    for ket in (ONE[0], ONE[1]):
        initial = outer(ket)
        final = m0 @ initial @ m0 + m1 @ initial @ m1
        left_response.append(float(np.trace(left_one @ final).real))
    close(left_response, [flip_probability, 0])
    # Matrix units form a basis, so this tests the entire superoperator.
    for unit in np.eye(16).reshape(16, 4, 4):
        out = m0 @ unit @ m0 + m1 @ unit @ m1
        close(out, (1 - flip_probability) * unit + flip_probability * w @ unit @ w)
        dilation = joint @ np.kron(unit, np.diag([1, 0])) @ joint.conj().T
        close(out, dilation.reshape(4, 2, 4, 2).trace(axis1=1, axis2=3))
    dplus, dminus = (outer((A + s * 1j * B) / math.sqrt(2)) for s in (-1, 1))
    leakage = ONE - p - r
    close(dplus + dminus + leakage, ONE)
    close(dplus - dminus, (np.kron(X, Y) + np.kron(Y, X)) / 2)
    cross = np.outer(A, B)
    close(cross.reshape(2, 2, 2, 2).trace(axis1=1, axis2=3), Z / 2)
    close(min(u, v) * np.linalg.inv(m0) @ m0, min(u, v) * ONE)
    for phi in np.linspace(-math.pi, math.pi, 17):
        # Standard optical/qubit R_z(phi)=exp(-i phi Z/2).
        ket = math.cos(phi) * A - 1j * math.sin(phi) * B
        axis = math.cos(phi) * X + math.sin(phi) * Y
        even_readout = (ONE + np.kron(axis, axis)) / 2
        rho = outer(ket)
        for n in range(4):
            measured = np.trace(even_readout @ rho).real
            expected = 1 - (1 - eta ** n) * math.sin(2 * phi) ** 2 / 2
            close(measured, expected)
            close(np.linalg.svd(p @ rho @ q, compute_uv=False).sum() * 2,
                  abs(math.sin(2 * phi)) * eta ** n)
            for chi in np.linspace(-math.pi, math.pi, 11):
                detector = outer((A + np.exp(1j * chi) * B) / math.sqrt(2))
                close(np.trace(detector @ rho),
                      (1 - eta ** n * math.sin(2 * phi) * math.sin(chi)) / 2)
            rho = m0 @ rho @ m0 + m1 @ rho @ m1
    return {"eta": eta, "gamma_per_crossing": -math.log(eta), "phase_flip_probability": flip_probability,
            "ideal_difference_one_pass": flip_probability, "ideal_harmonic_amplitude": flip_probability / 2,
            "tagged_port_left_one_given_B0_B1": left_response}


def design(eta, contrast, error_bound_per_model, miss_rate=0.05):
    # Four independent equal-size arms per laboratory. A hard bound on conventional
    # anisotropy after sham subtraction must be established outside the test sample.
    alpha = math.erfc(5 / math.sqrt(2)) / 2
    prediction = contrast * (1 - eta) / 2
    null_upper = error_bound_per_model
    signal_lower = prediction - error_bound_per_model
    gap = signal_lower - null_upper
    if gap <= 0:
        raise ValueError("Os conjuntos de previsões se tocam")
    count = math.ceil(2 * (math.sqrt(-math.log(alpha)) + math.sqrt(-math.log(miss_rate))) ** 2 / gap ** 2)
    threshold = null_upper + math.sqrt(-2 * math.log(alpha) / count)
    miss_bound = math.exp(-count * (signal_lower - threshold) ** 2 / 2)
    assert threshold < signal_lower and miss_bound <= miss_rate
    return {"contrast_lower_bound_assumed": contrast, "systematic_bound_each_assumed": error_bound_per_model,
            "one_sided_size": alpha, "min_power_per_lab": 1 - miss_rate, "predicted_D_at_contrast_bound": prediction,
            "conservative_gap": gap, "trials_per_arm_sufficient": count, "trials_per_lab": 4 * count,
            "strict_rejection_threshold": threshold, "miss_probability_bound": miss_bound,
            "joint_power_bound_independent_labs": (1 - miss_bound) ** 2}


def main():
    raw = (HERE / "BANCADA_SINTETICA.json").read_bytes()
    bench = json.loads(raw)
    beta = bench["contract"]["alpha"] * math.sqrt(math.e)
    close(beta, bench["contract"]["beta_tgl"])
    algebra = verify_algebra(beta)
    eta = algebra["eta"]
    matches = {}
    for label, sample in bench["samples"].items():
        reply = sample["response"]
        assert reply["synthetic"] and reply["data_opened"] is False and reply["nature_sigma"] is None
        assert reply["canonical"]["um_py_sha256"] == bench["contract"]["um_py_sha256"]
        result = reply["result"]
        damping = result["damping"][0][1]
        close(damping, math.exp(-beta * sample["request"]["s"] / 2))
        close(result["diagonal_population_max_change"], 0)
        matches[label] = damping
    close(matches["equivalencia_algebrica_uma_passagem"], eta)
    close(matches["equivalencia_algebrica_duas_passagens"], eta ** 2)
    receipt = {"status": "PROSPECTIVO_CONDICIONAL", "data_opened": False,
               "input_sha256": hashlib.sha256(raw).hexdigest(),
               "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "algebra": algebra, "bench_damping": matches, "design": design(eta, 0.90, 0.02)}
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
