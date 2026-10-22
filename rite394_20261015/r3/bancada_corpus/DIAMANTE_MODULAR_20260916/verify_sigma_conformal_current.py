"""Independent quadrature/difference checks of the adopted classical background.

This is not a modular-spectrum computation or a quantum-state/UV test.
All products are written next to this script; sources are read only.
"""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import tempfile

import numpy as np

ROOT = Path(__file__).resolve().parent


def atomic_json(name, value):
    path = ROOT / name
    content = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if path.exists():
        old = path.read_bytes()
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup = path.with_name(path.name + ".bak_" + stamp)
        with backup.open("xb") as stream:
            stream.write(old)
        assert backup.read_bytes() == old
    fd, temp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=ROOT)
    with os.fdopen(fd, "wb") as stream:
        stream.write(content)
    assert Path(temp).read_bytes() == content
    os.replace(temp, path)
    assert path.read_bytes() == content


def scale(eta):
    return 2.0 / np.cosh(eta)


def xi(eta, chi, eta_center, angular_radius):
    tau = eta - eta_center
    denominator = np.sin(angular_radius)
    return ((np.cos(tau) * np.cos(chi) - np.cos(angular_radius)) / denominator,
            -np.sin(tau) * np.sin(chi) / denominator)


def current_densities(eta, chi, eta_center, angular_radius, c):
    temporal, radial = xi(eta, chi, eta_center, angular_radius)
    measure = scale(eta) ** 4 * np.sin(chi) ** 2
    energy_density = 3 * c / (2 * scale(eta) ** 2)
    minus_pressure = c / (2 * scale(eta) ** 2)
    return measure * energy_density * temporal, measure * minus_pressure * radial


def charge(eta, eta_center, angular_radius, c, order=96):
    points, weights = np.polynomial.legendre.leggauss(order)
    chi = angular_radius * (points + 1) / 2
    temporal, _ = xi(eta, chi, eta_center, angular_radius)
    integral = angular_radius / 2 * np.dot(weights, temporal * np.sin(chi) ** 2)
    # 2*pi modular normalization, 4*pi angular volume, rho=3*c/(2*a^2).
    return 12 * np.pi ** 2 * c * scale(eta) ** 2 * integral


def main():
    records = []
    for eta_center, radius, c in [(1.2, .2, 1.0), (1.2, .5, .7), (1.5, .9, 1.3)]:
        radial_integral = (2 + np.cos(radius) ** 2) / 6 - radius / (2 * np.tan(radius))
        expected_charge = 12 * np.pi ** 2 * c * scale(eta_center) ** 2 * radial_integral
        expected_derivative = -24 * np.pi ** 2 * c * scale(eta_center) ** 2 * np.tanh(eta_center) * radial_integral
        quadrature_error = abs(charge(eta_center, eta_center, radius, c) - expected_charge)
        assert quadrature_error < 2e-11 * max(1.0, abs(expected_charge))
        derivative_errors = []
        divergence_errors = []
        for step in [1e-3, 5e-4, 2.5e-4]:
            measured_derivative = (charge(eta_center + step, eta_center, radius, c)
                                   - charge(eta_center - step, eta_center, radius, c)) / (2 * step)
            derivative_errors.append(abs(measured_derivative - expected_derivative))
            eta = eta_center + radius / 5
            chi = radius / 3
            temporal, _ = xi(eta, chi, eta_center, radius)
            conformal_factor = (-np.sin(eta - eta_center) * np.cos(chi) / np.sin(radius)
                                - np.tanh(eta) * temporal)
            expected_divergence = 3 * c / scale(eta) ** 2 * conformal_factor
            time_derivative = (current_densities(eta + step, chi, eta_center, radius, c)[0]
                               - current_densities(eta - step, chi, eta_center, radius, c)[0]) / (2 * step)
            space_derivative = (current_densities(eta, chi + step, eta_center, radius, c)[1]
                                - current_densities(eta, chi - step, eta_center, radius, c)[1]) / (2 * step)
            measured_divergence = (time_derivative + space_derivative) / (scale(eta) ** 4 * np.sin(chi) ** 2)
            divergence_errors.append(abs(measured_divergence - expected_divergence))
        assert derivative_errors[-1] < derivative_errors[0] / 10
        assert divergence_errors[-1] < divergence_errors[0] / 10
        assert expected_derivative < 0
        records.append({"eta_center": eta_center, "angular_radius": radius, "c_test": c,
                        "charge": expected_charge, "quadrature_error": quadrature_error,
                        "d_charge_d_eta": expected_derivative,
                        "centered_difference_errors": derivative_errors,
                        "divergence_difference_errors": divergence_errors})
    # Small-ball leading coefficient from quadrature, avoiding cancellation in cot(r).
    asymptotic = []
    for radius in [.1, .05, .025]:
        eta, c = 1.0, 1.0
        integral = charge(eta, eta, radius, c) / (12 * np.pi ** 2 * c * scale(eta) ** 2)
        asymptotic.append({"angular_radius": radius, "I_over_radius_fourth": integral / radius ** 4,
                           "error_to_one_over_fifteen": abs(integral / radius ** 4 - 1/15)})
    assert asymptotic[-1]["error_to_one_over_fifteen"] < asymptotic[0]["error_to_one_over_fifteen"] / 10
    # Negative control: falsely substituting a trace-free source must be rejected.
    negative_control_residual = abs(records[1]["d_charge_d_eta"])
    assert negative_control_residual > 1e-3
    result = {"timestamp": datetime.now().astimezone().isoformat(), "status": "PASS",
              "scope": "CLASSICAL_ADOPTED_EINSTEIN_SIGMA_BACKGROUND_ONLY",
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "cases": records, "small_ball": asymptotic,
              "false_trace_free_control": {"status": "REJECTED", "residual": negative_control_residual},
              "modular_remainder_coefficient_measured": False,
              "reeh_schlieder_numerically_certified": False,
              "gate_changed": False}
    atomic_json("SIGMA_CONFORMAL_CURRENT_CHECKS.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
