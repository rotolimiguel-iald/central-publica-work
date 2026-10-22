def v394_gibbs_root_parameters(V0_J, kappa_s_inv, hbar_J_s=None, alpha=None):
    """Construct Eref from a specified faithful finite Gibbs state and clock.

    P=2*pi/kappa; Omega=V0/hbar; rho=exp(-P*Hg/hbar)/Z.
    Hpos=(hbar/P)*(-log rho)=Hg+Eref*I, Eref=(hbar/P)*log(2*cosh(P*Omega)).
    This choice removes the free Eref inside this Gibbs-based finite instance.
    It does not identify the density Hamiltonian with a full modular generator
    or choose a physical kappa. The same proper time t uses dissipative u=t/P
    and oriented modular parameter s=-t/P; no negative diffusion is introduced.
    """
    import math
    ground = v394_physical_parameters(V0_J, V0_J, hbar_J_s, alpha)
    clock = v394_kms_clock(ground, kappa_s_inv)
    period = clock["kms_period_s"]
    x = _v394_finite_real("P_Omega", period*ground["Omega_rad_s"], positive=True)
    low_k = _v394_finite_real("K_rho_low", math.log1p(math.exp(-2*x)), positive=True)
    high_k = _v394_finite_real("K_rho_high", 2*x+low_k, positive=True)
    low_energy = _v394_finite_real("density_energy_low_J", (ground["hbar_J_s"]/period)*low_k, positive=True)
    origin = _v394_finite_real("Eref_Gibbs_J", ground["V0_J"]+low_energy, positive=True)
    if origin <= ground["V0_J"]:
        raise V394PhysicalContractError("Gibbs energy offset is below float resolution; use higher precision")
    result = v394_physical_parameters(ground["V0_J"], origin, ground["hbar_J_s"], ground["alpha"])
    # Preserve the small eigenvalue directly; subtracting the rounded center
    # from V0 lost 1.40e-10 relative precision in the preregistered R1 check.
    # The scientific tolerance is unchanged. Derive all anchored quantities
    # from the same positive density spectrum, without cancellation.
    high_energy = _v394_finite_real("density_energy_high_J", 2*ground["V0_J"]+low_energy, positive=True)
    root_sum = math.sqrt(low_k)+math.sqrt(high_k)
    root_ratio = _v394_finite_real("density_root_ratio", (2*x/root_sum)/root_sum, positive=True)
    gamma = _v394_finite_real("density_gamma", ground["beta"]*ground["Omega_rad_s"]*root_ratio, positive=True)
    result["gamma_s_inv"] = gamma
    result["root_rate_ratio"] = root_ratio
    result["tau_eff_s"] = _v394_finite_real("density_tau_eff", root_ratio/(2*ground["Omega_rad_s"]), positive=True)
    result["echo_dt_s"] = _v394_finite_real("density_echo_dt", -math.log(ground["eta"])/gamma, positive=True)
    result["energies_J"] = [low_energy, high_energy]
    result["energy_representation"] = {
        "exact_from_state": "(hbar/P)*K_rho eigenvalues; low computed directly, high=low+2V0",
        "center_is_rounded_presentation": True,
        "rounded_endpoints_coincide": low_energy==high_energy,
        "scientific_tolerance_unchanged": True,
    }
    result["energy_origin_selection"] = "Hpos = (hbar/P)*(-log rho_Gibbs); rho_Gibbs fixed by Hg and specified kappa"
    result["energy_origin_statute"] = "DERIVED_IN_FINITE_GIBBS_INSTANCE; GIBBS_AND_CLOCK_CHOICE_EXPLICIT"
    result["density_surprise_eigenvalues"] = [low_k,high_k]
    result["kms_clock"] = clock
    result["dissipative_time_conversion"] = "u=t/P >=0; modular orientation s=-t/P"
    result["scope"] = "FINITE_GIBBS_ROOT_CONTRACT__NOT_MINUS_LOG_DELTA__NO_UNIVERSAL_CALIBRATION"
    return result