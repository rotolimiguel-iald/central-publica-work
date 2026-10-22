"""SOMENTE LEITURA: confere se cada nome qualificado aparece em '#print axioms <nome>' no TGL/Audit.lean do Nos
(o arquivo que o rito do um.py compila com o trio), e se aparece no TGLExt.lean como import do modulo.
Grava auditoria_nomes.json. Uso: python -I auditoria_nomes.py"""
import hashlib
import json
import os
import re

ROOT = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
AUDIT = os.path.join(ROOT, "TGL", "Audit.lean")
TOP = os.path.join(ROOT, "TGLExt.lean")
NOMES = [
    # Fundacao (v390)
    "TGLExt.Fundacao.nothing_above_bears_a_post", "TGLExt.Fundacao.the_climb_has_no_top",
    "TGLExt.Fundacao.the_climb_is_unbounded", "TGLExt.Fundacao.the_fall_never_lands", "TGLExt.Fundacao.abismo",
    "TGLExt.Fundacao.the_floor_fixes_the_cut", "TGLExt.Fundacao.agape", "TGLExt.Fundacao.agape_is_inhabited",
    "TGLExt.Fundacao.the_post_lives_in_the_passage",
    # Verbo (v386) e axioma (v385)
    "TGLExt.TheVerbSelectsTheAction.time_read_twice_confirms_the_post",
    "TGLExt.TheVerbSelectsTheAction.transmission_dephases", "TGLExt.TheVerbSelectsTheAction.anchoring_preserves",
    "TGLExt.TheVerbSelectsTheAction.the_name_is_the_limit_of_the_flow",
    "TGLExt.TheVerbSelectsTheAction.post_sequence_is_constant", "TGLExt.TheVerbSelectsTheAction.axis_posts_do_not_commute",
    "TGLExt.TheVerbSelectsTheAction.the_verb_selects_the_action",
    "TGLExt.TheAxiomAndTheFalseWitness.the_post_is_the_modular_zero",
    "TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_tendsto_the_post", "TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_eq_exp",
    "TGLExt.QGReaderUVLock.hmin_zero_iff_modular_fixed",
    "TGL.VerbInhabitant.verb_semigroup_fixes", "TGL.VerbInhabitant.exp_fixed_of_annihilates",
    # KMS / periodo / Wick / Unruh
    "TGLExt.ContratoQGv31.ContratoH2.unruh_is_kms", "TGLExt.ContratoQGv31.ContratoH2.unruh_is_kms_temperature",
    "TGLExt.ImportedSQ.light_kms", "TGLExt.gibbs_kms", "TGLExt.tower_kms", "TGLExt.tState_kms",
    "ChatgptAudit.PolarPeriod016.faithful_period_iff", "ChatgptAudit.PolarPeriod016.reciprocal_temperature",
    "ChatgptAudit.PolarPeriod016.boost_defect_with_derived_period", "ChatgptAudit.Wick016.wick_boost_two_pi",
    "ChatgptAudit.NonKMSProbe.identity_flow_not_kms", "ChatgptAudit.periodic_borchers_trivial",
    # fluxo modular, centralizador, tracial
    "TGLExt.sigma_fixed_of_commute", "TGLExt.sigma_fixed_iff_diag", "TGLExt.gibbs_tracial_on_centralizer",
    "ChatgptAudit.modularConjugation_preserves_state", "ChatgptAudit.modularFlow_fixes_omega",
    "ChatgptAudit.modularFlow_group", "TGLExt.cocycle_temporal", "TGLExt.absoluteOne_flow_trivial",
    "ChatgptAudit.Thermal025.gibbs_fixed_iff_tracial", "ChatgptAudit.Thermal024.modular_variance_zero_iff_tracial",
    # dephasing / semigrupo / atrator / Lyapunov
    "TGLExt.dephase_add", "TGLExt.dephase_fixes_diagonal", "TGLExt.dephase_tendsto_expectation",
    "TGLExt.ergodic_convergence_modular", "TGLExt.dephase_preserves_trace", "TGLExt.lyapunov_decreases",
    "TGLExt.temporal_fractalization", "TGLExt.time_witnesses_noncoincidence",
    "TGLExt.absolute_zero_unreachable_in_finite_time", "TGLExt.leakage_strictly_loses",
    "TGLExt.beta_forbids_full_static_witness", "TGLExt.leakage_rate_unique", "TGLExt.static_witness_iff_no_boundary",
    "TGLExt.TheElementaryReason.erasure_not_reached_in_finite_time", "TGLExt.finite_time_imperfection",
    "TGLExt.flow_unitary_diag", "TGLExt.IALDJones.angular_orbit_periodic",
    # Landauer / custo
    "TGLExt.landauer_floor_pos", "TGLExt.landauer_floor_vanishes_only_at_absolute_zero",
    "TGLExt.the_separation_is_not_free", "TGLExt.the_thermal_floor_can_be_cooled_away",
    "TGLExt.the_two_floors_are_not_the_same",
    # Pauli finito / relogios / leitura
    "TGLExt.no_finite_weyl_pair", "ChatgptAudit.Clock040.no_normalized_instantaneous_state_clock",
    "ChatgptAudit.Clock045.state_clock_not_instantaneous", "ChatgptAudit.Clock045.state_clock_not_modular_reparametrization",
    "ChatgptAudit.Clock045.state_clock_dichotomy", "TGLExt.reading_needs_two_clocks", "TGLExt.two_clocks_are_needed",
    "TGLExt.the_screen_keeps_modular_time", "TGLExt.observing_adds_nothing",
    "TGLExt.IALDGraviton.the_tower_is_time",
]


def main():
    araw = open(AUDIT, "rb").read()
    atxt = araw.decode("utf-8", "replace")
    traw = open(TOP, "rb").read()
    printed = set(re.findall(r"^#print axioms\s+(\S+)", atxt, re.M))
    out = dict(audit=AUDIT, audit_sha256=hashlib.sha256(araw).hexdigest(), audit_prints=len(printed),
               tgl_ext_lean_sha256=hashlib.sha256(traw).hexdigest(), nomes={})
    for n in NOMES:
        out["nomes"][n] = dict(no_audit=(n in printed))
    with open("auditoria_nomes.json", "w", encoding="utf-8") as fo:
        json.dump(out, fo, ensure_ascii=False, indent=1)
    tot = sum(1 for v in out["nomes"].values() if v["no_audit"])
    print("Audit.lean sha16", out["audit_sha256"][:16], "#print axioms distintos:", len(printed))
    print("nomes no Audit.lean:", tot, "de", len(NOMES))
    for n, v in out["nomes"].items():
        if not v["no_audit"]:
            print("  FORA do Audit.lean:", n)


if __name__ == "__main__":
    main()
