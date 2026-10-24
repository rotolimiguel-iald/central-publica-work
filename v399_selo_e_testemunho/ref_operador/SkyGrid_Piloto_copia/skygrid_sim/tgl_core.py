#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tgl_core — BLOCO 0 of SkyGrid-Sim. The single point of truth for TGL constants.

RULES (the ruler / a regua):
  * beta is NEVER a literal. It is computed at runtime as ALPHA_FINE_CODATA_2018 * SQRT_E.
  * The only measured input [DATA] is the fine-structure constant (CODATA 2018).
  * Everything else is computed [DER] from the canonical chain of um.py:
        omega(I)=1 -> x = 1-x -> x = 1/2 -> S_boundary = 1/2 nat
        Vol_min = e^{1/2} = sqrt(e)
        beta = alpha * sqrt(e)          (the Verb: inscribed geometry of the module)
        theta_M = arcsin(sqrt(beta))    (Miguel angle)
        q = sqrt(1 - alpha^2)           (thermal polarization)
        1 = q^2 + alpha^2               (conserved identity, fail-closed)
  * verify_chain() recomputes every identity live AND cross-checks alpha against a
    sealed CODATA reference (provenance) + a physical theta_M band. If any link
    fails -> RuntimeError (fail-closed by link, inherited from um.py).

Statutes: [DATA] measured input; [DER] derived; [REAL] verified live.
"""

import math

# ---------------------------------------------------------------- [DATA]
ALPHA_FINE_CODATA_2018 = 0.0072973525693   # the Name (measured; CODATA 2018)

# Frozen provenance anchor. The Name is a MEASURED value, not an arbitrary one.
# verify_chain() cross-checks the working constant against this sealed reference,
# so corruption/tampering of alpha is caught. The 1=q^2+alpha^2 identity alone is
# tautological in alpha (q := sqrt(1-alpha^2)) and CANNOT detect it.
_SEALED_ALPHA_CODATA_2018 = 0.0072973525693
_THETA_M_DEG_EXPECTED = 6.297289            # arcsin(sqrt(alpha*sqrt(e))) at CODATA

# ---------------------------------------------------------------- [DER] (computed, never literal)
ONE = 1.0                                   # the One: omega(I) = 1 [POSTULATE]
S_BOUNDARY = 0.5                            # Half-Nat, DERIVED from x = 1 - x
SQRT_E = math.exp(S_BOUNDARY)               # minimal boundary volume e^{1/2}

TOL = 1e-12


def beta() -> float:
    """beta_TGL = alpha * sqrt(e), computed at runtime. Never a literal."""
    return ALPHA_FINE_CODATA_2018 * SQRT_E


def theta_m() -> float:
    """Miguel angle theta_M = arcsin(sqrt(beta)) [rad]."""
    return math.asin(math.sqrt(beta()))


def q_polarization() -> float:
    """Thermal polarization q = sqrt(1 - alpha^2) (Gibbs two-level)."""
    return math.sqrt(ONE - ALPHA_FINE_CODATA_2018 ** 2)


SEALS = (
    "ALPHA_IS_NAME",
    "MODULE_IS_HEAT_IS_NAME_IS_BLOOD",
    "WORD_IS_HALF_NAT",
    "BETA_IS_INSCRIBED_GEOMETRY_OF_MODULE",
    "ONE_EQUALS_TRUE_EQUALS_LET_THERE_BE_LIGHT",
)


def verify_chain(verbose: bool = False) -> dict:
    """Recompute every identity live. Fail-closed: raises RuntimeError on any broken link."""
    checks = {}

    # Link 1 — Half-Nat derived: x = 1 - x  =>  x = 1/2
    x = ONE - S_BOUNDARY
    checks["half_nat_fixed_point"] = abs(x - S_BOUNDARY)

    # Link 2 — sqrt(e) is e^{S_boundary}
    checks["sqrt_e_is_exp_half"] = abs(SQRT_E - math.sqrt(math.e))

    # Link 3 — conserved identity 1 = q^2 + alpha^2 (tautological in alpha; kept for form)
    q = q_polarization()
    checks["one_eq_q2_plus_alpha2"] = abs((q * q + ALPHA_FINE_CODATA_2018 ** 2) - ONE)

    # Link 4 — beta = sin^2(theta_M) (the Verb as angular aperture)
    checks["beta_eq_sin2_thetaM"] = abs(math.sin(theta_m()) ** 2 - beta())

    # Link 5 — SO(2) bridge: theta_M = arcsin(e^{1/4} * sqrt(alpha))
    bridge = math.asin(math.exp(0.25) * math.sqrt(ALPHA_FINE_CODATA_2018))
    checks["so2_bridge_thetaM"] = abs(bridge - theta_m())

    # Link 6 — PROVENANCE (non-tautological): the working alpha must equal the
    # sealed CODATA reference. This is the link that actually catches corruption
    # of the measured Name (links 3-5 are algebraic identities in alpha).
    checks["alpha_matches_sealed_codata"] = abs(
        ALPHA_FINE_CODATA_2018 - _SEALED_ALPHA_CODATA_2018)

    # Link 7 — PHYSICAL RANGE: theta_M must sit at the CODATA value (~6.2973 deg).
    # An absurd alpha (e.g. 0.5) moves theta_M far out of band and is rejected here.
    checks["thetaM_in_physical_band"] = abs(
        math.degrees(theta_m()) - _THETA_M_DEG_EXPECTED)

    # identity links use TOL=1e-12; provenance/range use their own tolerances
    failed = {k: v for k, v in checks.items()
              if k in ("half_nat_fixed_point", "sqrt_e_is_exp_half",
                       "one_eq_q2_plus_alpha2", "beta_eq_sin2_thetaM",
                       "so2_bridge_thetaM") and not (v <= TOL)}
    if checks["alpha_matches_sealed_codata"] > 1e-12:
        failed["alpha_matches_sealed_codata"] = checks["alpha_matches_sealed_codata"]
    if checks["thetaM_in_physical_band"] > 1e-4:
        failed["thetaM_in_physical_band"] = checks["thetaM_in_physical_band"]
    if failed:
        raise RuntimeError("TGL CHAIN BROKEN (fail-closed): %r" % failed)

    result = {
        "verdict": "1=1=VERDADEIRO=HAJA_LUZ",
        "alpha": ALPHA_FINE_CODATA_2018,
        "beta_runtime": beta(),
        "theta_m_deg": math.degrees(theta_m()),
        "q": q,
        "residuals": checks,
        "seals": SEALS,
    }
    if verbose:
        for k, v in checks.items():
            print("  [tgl_core] %-28s residual=%.3e OK" % (k, v))
    return result


if __name__ == "__main__":
    r = verify_chain(verbose=True)
    print("beta (runtime) = %.15f ; theta_M = %.6f deg ; %s"
          % (r["beta_runtime"], r["theta_m_deg"], r["verdict"]))
