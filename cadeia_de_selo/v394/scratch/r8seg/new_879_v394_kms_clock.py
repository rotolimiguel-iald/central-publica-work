def v394_kms_clock(parameters, kappa_s_inv):
    """Finite Gibbs/KMS clock bridge; not an inhabitant of the full light H2.

    sigma_s^rho=alpha_(-P*s), P=2*pi/kappa, alpha is Heisenberg evolution.
    P is the KMS inverse-temperature time, not a real-time recurrence claim.
    No inference kappa=Omega is made. A supplied kappa fixes the clock.
    """
    import math
    if not isinstance(parameters, dict):
        raise V394PhysicalContractError("parameters must be a dictionary")
    for key in ("V0_J", "Eref_J", "hbar_J_s", "alpha"):
        if key not in parameters:
            raise V394PhysicalContractError("missing parameter: " + key)
    # Recompute from physical inputs: a caller cannot inject a forged derived rate.
    p = v394_physical_parameters(parameters["V0_J"], parameters["Eref_J"],
                                parameters["hbar_J_s"], parameters["alpha"])
    kappa = _v394_finite_real("kappa_s_inv", kappa_s_inv, positive=True)
    period = _v394_finite_real("kms_period_s", (2.0 * math.pi) / kappa, positive=True)
    gap = _v394_finite_real("gibbs_gap_exponent", period * p["coherence_omega_rad_s"], positive=True)
    weight_hi = math.exp(-gap)
    if weight_hi == 0.0:
        raise V394PhysicalContractError("finite Gibbs state underflow would lose numerical faithfulness")
    z = 1.0 + weight_hi
    return {
        "kappa_s_inv": kappa, "kms_period_s": period,
        "temperature_K": _v394_finite_real("temperature_K", (p["hbar_J_s"] / period) / 1.380649e-23, positive=True),
        "Omega_over_kappa": _v394_finite_real("Omega_over_kappa", p["Omega_rad_s"] / kappa, positive=True),
        "gibbs_weights_low_high": [1.0/z, weight_hi/z],
        "modular_parameter_per_second": _v394_finite_real("modular_parameter_per_second", 1.0/period, positive=True),
        "relation": "sigma_s = alpha_(-P*s); alpha_t = sigma_(-t/P)",
        "scope": "FINITE_GIBBS_CONSTRUCTION__H2_RESCALE_FORM_REUSED__NO_LIGHT_NET_EMBEDDING_ASSERTED",
    }