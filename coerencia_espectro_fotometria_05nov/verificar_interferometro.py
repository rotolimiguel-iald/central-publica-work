from __future__ import annotations

import json
from pathlib import Path

import numpy as np

OUT = Path(r"C:\IALD\Central de Patentes\work\coerencia_espectro_fotometria_05nov")


def case(a: complex, b: complex, gamma_t: float, phi: float) -> dict[str, object]:
    rho = np.array([[abs(a) ** 2, a * b.conjugate()], [a.conjugate() * b, abs(b) ** 2]], dtype=complex)
    q = float(np.exp(-gamma_t))
    rho_t = rho.copy()
    rho_t[0, 1] *= q
    rho_t[1, 0] *= q
    plus = (np.array([1.0, np.exp(1j * phi)]) / np.sqrt(2.0)).reshape(2, 1)
    minus = (np.array([1.0, -np.exp(1j * phi)]) / np.sqrt(2.0)).reshape(2, 1)
    i_plus = float((plus.conjugate().T @ rho_t @ plus)[0, 0].real)
    i_minus = float((minus.conjugate().T @ rho_t @ minus)[0, 0].real)
    n = abs(a) ** 2 + abs(b) ** 2
    phase_total = np.angle(a * b.conjugate()) + phi
    expected_plus = n / 2 + q * abs(a * b) * np.cos(phase_total)
    expected_minus = n / 2 - q * abs(a * b) * np.cos(phase_total)
    visibility = 2 * abs(a * b) / n * q
    assert np.isclose(i_plus + i_minus, n)
    assert np.isclose(i_plus, expected_plus)
    assert np.isclose(i_minus, expected_minus)
    assert np.isclose((i_plus - i_minus) / n, visibility * np.cos(phase_total))
    return {
        "a": [a.real, a.imag],
        "b": [b.real, b.imag],
        "gamma_T": gamma_t,
        "phi": phi,
        "I_plus": i_plus,
        "I_minus": i_minus,
        "I_total": i_plus + i_minus,
        "V_T": visibility,
        "trace_preserved": True,
        "formulas_passed": True,
    }


def main() -> None:
    cases = [
        case(1 / np.sqrt(2), 1 / np.sqrt(2), 0.0, 0.0),
        case(1 / np.sqrt(2), 1 / np.sqrt(2), 1.0, 0.0),
        case(1 / np.sqrt(2), 1 / np.sqrt(2), 1.0, np.pi / 2),
        case(0.8, 0.6, 0.7, np.pi / 3),
        case(0.5 + 0.2j, 0.4 - 0.3j, 0.4, 0.2),
    ]
    assert np.isclose(cases[0]["V_T"], 1.0)
    assert np.isclose(cases[1]["V_T"], np.exp(-1.0))
    assert np.isclose(cases[2]["I_plus"], 0.5)
    assert np.isclose(cases[2]["I_minus"], 0.5)
    payload = {
        "status": "ALL_INTERFEROMETER_CHECKS_PASSED",
        "model": "Single-photon Mach-Zehnder with path dephasing and balanced recombination",
        "cases": cases,
        "no_data_used": True,
    }
    (OUT / "VERIFICACAO_INTERFEROMETRO.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
