def v394_physical_parameters(V0_J, Eref_J, hbar_J_s=None, alpha=None):
    """Return exact-form model parameters in one SI clock, evaluated as floats.

    Hg=-V0*sigma_y; Hpos=Eref*I+Hg; spectrum Eref+-V0, Eref>=V0.
    Root law: D[sqrt(beta/hbar)*sqrt(Hpos)]. Its off-diagonal rate is
    gamma=beta/(2*hbar)*(sqrt(Eref+V0)-sqrt(Eref-V0))**2.
    The rationalized expression below avoids cancellation for large Eref/V0.
    tau_eff matches the quadratic law for THIS gap only. echo_dt constructs
    a matched echo step; it does not replace the old echo's frozen dt=0.35.
    Floats with under/overflow in a strictly positive output are refused.
    """
    import math
    if hbar_J_s is None:
        hbar_J_s = 6.62607015e-34 / (2.0 * math.pi)
    if alpha is None:
        alpha = 7.2973525693e-3  # ALPHA_FINE_CODATA_2018 in the pinned source.
    v = _v394_finite_real("V0_J", V0_J, positive=True)
    e = _v394_finite_real("Eref_J", Eref_J, positive=True)
    hb = _v394_finite_real("hbar_J_s", hbar_J_s, positive=True)
    a = _v394_finite_real("alpha", alpha, positive=True)
    if e < v:
        raise V394PhysicalContractError("Eref_J must be >= V0_J for Hpos >= 0")
    beta = _v394_finite_real("beta", a * math.sqrt(math.e), positive=True)
    if beta >= 1.0:
        raise V394PhysicalContractError("0 < beta < 1 required")
    eta = _v394_finite_real("eta", 2.0 * math.sqrt(beta) * math.sqrt(1.0-beta), positive=True)
    if eta >= 1.0:
        raise V394PhysicalContractError("echo has no strictly contractive representable eta")
    omega = _v394_finite_real("Omega_rad_s", v / hb, positive=True)
    frequency = _v394_finite_real("coherence_omega_rad_s", 2.0 * omega, positive=True)
    q = _v394_finite_real("V0_over_Eref", v / e, positive=True)
    denominator = 1.0 + math.sqrt(max(0.0, (1.0-q)*(1.0+q)))
    ratio = _v394_finite_real("root_rate_ratio", q / denominator, positive=True)
    gamma = _v394_finite_real("gamma_s_inv", (beta * omega) * ratio, positive=True)
    tau = _v394_finite_real("tau_eff_s", (hb / e) / (2.0 * denominator), positive=True)
    echo_dt = _v394_finite_real("echo_dt_s", -math.log(eta) / gamma, positive=True)
    lo = _v394_finite_real("energy_lower_J", e-v, nonnegative=True)
    hi = _v394_finite_real("energy_upper_J", e+v, positive=True)
    return {
        "beta": beta, "Omega_rad_s": omega,
        "coherence_omega_rad_s": frequency, "gamma_s_inv": gamma,
        "tau_eff_s": tau, "echo_dt_s": echo_dt, "eta": eta,
        "energies_J": [lo, hi], "V0_J": v, "Eref_J": e,
        "hbar_J_s": hb, "alpha": a, "root_rate_ratio": ratio,
        "energy_representation": {
            "exact_from_inputs": "Eref_J plus/minus V0_J",
            "rounded_endpoints_coincide": lo == hi,
            "calculation_uses_center_and_half_gap": True,
        },
        "scope": "DERIVED_FINITE_TWO_LEVEL_POSITIVE_ENERGY__NOT_UNIVERSAL_CALIBRATION",
        "ground_zero_instance": e == v,
        "mu_do_rito": "q->0 (Thomson; Teorema da Escala)",
    }