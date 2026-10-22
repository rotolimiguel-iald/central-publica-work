_QG_FRONTIER_FLAGS = {
    "unconditional_continuous_corner_proved": "TGLExt.qgFrontier_unconditionalContinuousCorner",
    "modular_realization_constructed": "TGLExt.qgFrontier_modularRealization",
    "continuous_modular_realization_constructed": "TGLExt.qgFrontier_continuousModularRealization",
    "full_TGL_witness_constructed": "TGLExt.qgFrontier_fullTGLWitness",
}

_GRAVITY_PRICE_FLAGS = {
    "H1_internal_susy_relative_gap_discharged": "TGLExt.qgPrice_H1_internalSusyRelativeGap_discharged",
    "H2_smooth_modular_four_frame_discharged": "TGLExt.qgPrice_H2_smoothModularFourFrame_discharged",
    "H3_local_horizon_equilibrium_discharged": "TGLExt.qgPrice_H3_localHorizonEquilibrium_discharged",
    "tower_act_III_inhabitant_constructed": "TGLExt.qgPrice_towerActIII_inhabitantConstructed",
}

_V350_MODULAR_CONTRACTS = {
    "red_clause_JMJ_contains": (
        "TGLExt.qgConverse_JMJ_contains_commutant",
        "TGLExt.V350Gate.checkedConverse"),
    "qgf_modular_realization_constructed": (
        "TGLExt.qgFrontier_modularRealization",
        "TGLExt.V350Gate.checkedModular"),
    "gpf_tower_act_III_inhabitant_constructed": (
        "TGLExt.qgPrice_towerActIII_inhabitantConstructed",
        "TGLExt.V350Gate.checkedActIII"),
}

def verify_v350_modular_provenance(kernel):
    """Require a successful build/audit and BOTH the term and its exact-type bridge."""
    kf = kernel or {}
    axioms = kf.get("axiom_report") or {}
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    built = (kf.get("lake_build_ok") is True or (
        kf.get("incremental_build_ok") is True
        and kf.get("dependency_hashes_verified") is True
        and kf.get("changed_source_hashes_verified") is True))
    verified = (built
                and kf.get("audit_returncode") == 0
                and kf.get("all_verified") is True)
    return {
        flag: bool(verified and all(
            isinstance(axioms.get(name), list)
            and all(isinstance(a, str) and a in allowed for a in axioms[name])
            for name in names))
        for flag, names in _V350_MODULAR_CONTRACTS.items()
    }

def finalize_v350_modular_frontier(kernel):
    """A name alone cannot light any of the three newly constructed targets."""
    proofs = verify_v350_modular_provenance(kernel)
    kernel.update(proofs)
    kernel["v350_typed_modular_proofs"] = proofs
    kernel["v350_modular_scope"] = "PRODUCT_TOWER__J_M_J_EQUALS_COMMUTANT"
    return kernel

def v350_frontier_flag_has_proof(kernel, flag):
    """Replace a historical 'must stay false' check with a proof obligation."""
    if not kernel.get(flag):
        return True
    return verify_v350_modular_provenance(kernel).get(flag) is True

def v350_gravity_flags_have_proof(kernel):
    return all(v350_frontier_flag_has_proof(kernel, key)
               for key in kernel if key.startswith("gpf_") and kernel.get(key))

def evaluate_v350_kernel_frontier(kernel):
    """Only the currently checked scope can advance; no name opens later stages."""
    proofs = verify_v350_modular_provenance(kernel)
    modular = all(proofs.values())
    return {
        "verification": "LEAN_EXACT_TYPE_BRIDGES_AND_AXIOM_WHITELIST",
        "modular_duality_constructed": modular,
        "proofs": proofs,
        "scope": "PRODUCT_TOWER__J_M_J_EQUALS_COMMUTANT",
        "remaining": [
            "continuous_core_and_finite_Three_Locks_corner_on_same_realization",
            "H1_relative_gap_beyond_finite_face",
            "H2_smooth_modular_four_frame_and_geometric_identification",
            "H3_area_heat_equilibrium_on_the_same_physical_horizon",
            "interacting_quantum_state_BRST_QME_anomalies_and_UV_scope",
        ],
        "verdict": (
            "MODULAR_DUALITY_CONSTRUCTED__CONTINUOUS_GEOMETRY_AND_QUANTUM_INTERACTIONS_OPEN"
            if modular else "MODULAR_DUALITY_OPEN"),
        "legacy_gate_changed": False,
        "full_plan_complete": False,
    }
