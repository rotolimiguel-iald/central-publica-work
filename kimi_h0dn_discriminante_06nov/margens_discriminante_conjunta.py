from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import norm

BASE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
OUT = Path(r"C:\IALD\Central de Patentes\work\kimi_h0dn_discriminante_06nov\MARGENS_DISCRIMINANTE_CONJUNTA.json")
Q = float(norm.ppf(0.975))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def joint_gaussian(mu_x: float, mu_y: float, rho: float) -> float:
    conditional_sd = math.sqrt(max(1e-30, 1 - rho * rho))

    def integrand(y: float) -> float:
        mean_x = mu_x + rho * (y - mu_y)
        return float(norm.pdf(y - mu_y) * norm.sf((5 - mean_x) / conditional_sd))

    value, error = quad(integrand, -Q, Q, epsabs=2e-12, epsrel=2e-11, limit=200)
    if error > 1e-7:
        raise ValueError(("quadrature_failed", value, error))
    return float(value)


bg = json.loads((BASE / "background/BG1.json").read_text(encoding="utf-8"))
with np.load(BASE / "network/network.npz", allow_pickle=False) as net:
    V = net["parameter_covariance_free_cepheid"].copy()
    ih = int(net["h_index"])

cb = np.asarray(bg["covariance"], dtype=float)
gh = np.asarray(bg["gradient_h"], dtype=float)
gk = np.asarray(bg["gradient_k"], dtype=float)
logk = float(bg["logK"])
vb = float(gh @ cb @ gh)
vbt = float((gh + gk) @ cb @ (gh + gk))
cross_bg = float(gh @ cb @ (gh + gk))
vh0 = float(V[ih, ih])
vc = float(V[-1, -1])
hc = float(V[ih, -1])


def scales(vh: float) -> tuple[float, float, float, float]:
    sd0 = math.sqrt(vh + vb)
    sdt = math.sqrt(vh + vbt)
    d = logk / sd0
    rho = (vh + cross_bg) / (sd0 * sdt)
    return d, rho, sd0, sdt


def power_joint(vh: float) -> float:
    d, rho, _, _ = scales(vh)
    return joint_gaussian(d, 0.0, rho)


def false_joint(vh: float) -> float:
    _, rho, _, sdt = scales(vh)
    return joint_gaussian(0.0, -logk / sdt, rho)


base = {
    "network_variance_h": vh0,
    "D": scales(vh0)[0],
    "correlation": scales(vh0)[1],
    "joint_power": power_joint(vh0),
    "null_joint": false_joint(vh0),
    "null_only_power": float(norm.sf(5 - scales(vh0)[0])),
}

targets = []
asymptotic_maximum = power_joint(1e-14)
for target in (0.5, 0.9, 0.95):
    if target >= asymptotic_maximum - 1e-12:
        targets.append({
            "target_joint_power": target,
            "attainable_with_finite_network_variance": False,
            "reason": "With marginal 95% TGL compatibility, the joint event is a strict subset and approaches 95% only as network variance tends to zero.",
        })
        continue
    if target < base["joint_power"]:
        upper = vh0
        while power_joint(upper) > target:
            upper *= 2
        target_vh = brentq(lambda vh: power_joint(vh) - target, vh0, upper, xtol=1e-16)
    else:
        target_vh = brentq(lambda vh: power_joint(vh) - target, 1e-14, vh0, xtol=1e-16)
    d, rho, sd0, sdt = scales(target_vh)
    if target_vh < vh0:
        needed_prior_var = hc * hc / (vh0 - target_vh) - vc
        Vnew = V - np.outer(V[:, -1], V[-1, :]) / (vc + needed_prior_var)
        updated_vh = float(Vnew[ih, ih])
        if not math.isclose(updated_vh, target_vh, rel_tol=2e-8, abs_tol=1e-12):
            raise ValueError(("full_update_mismatch", target, updated_vh, target_vh))
        prior_sd = math.sqrt(needed_prior_var) if needed_prior_var >= 0 else None
    else:
        needed_prior_var = None
        updated_vh = target_vh
        prior_sd = None
    targets.append({
        "target_joint_power": target,
        "attainable_with_finite_network_variance": True,
        "required_D": d,
        "maximum_network_variance_logH": target_vh,
        "maximum_network_sigma_logH": math.sqrt(target_vh),
        "sigma_reduction_fraction": 1 - math.sqrt(target_vh / vh0),
        "independent_external_cepheid_prior_sd_mag": prior_sd,
        "full_precision_updated_network_variance": updated_vh,
        "achieved_joint_power": power_joint(updated_vh),
        "null_only_power_at_same_design": float(norm.sf(5 - d)),
        "joint_false_positive_under_null": false_joint(updated_vh),
        "correlation_at_target": rho,
    })

payload = {
    "status": "EXPLORATORY_PROSPECTIVE_MARGINS_FOR_JOINT_DISCRIMINATION",
    "rule_candidate": "z_null >= 5 AND abs(z_tgl) <= 1.959963984540054",
    "rule_status": "REQUIRES_PROSPECTIVE_FREEZE; NOT_A_NEW_ADMISSION_REQUIREMENT",
    "observed_data_used": False,
    "new_constraint_asserted": False,
    "model": "free_cepheid_host_differential_bias plus a hypothetical independent Gaussian Cepheid-bias constraint",
    "background_variance_logH": vb,
    "background_variance_logHK": vbt,
    "cov_h_cepheid": hc,
    "sigma_cepheid_internal_mag": math.sqrt(vc),
    "baseline": base,
    "targets": targets,
    "interpretation": "Targets for joint rejection of the null and 95% TGL compatibility. The external constraints are design requirements only, not available measurements.",
    "sources": [
        {"path": str(BASE / "network/network.npz"), "sha256": sha(BASE / "network/network.npz")},
        {"path": str(BASE / "background/BG1.json"), "sha256": sha(BASE / "background/BG1.json")},
    ],
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload, ensure_ascii=False, indent=2))
print(json.dumps({"output": str(OUT), "sha256": sha(OUT)}, indent=2))
