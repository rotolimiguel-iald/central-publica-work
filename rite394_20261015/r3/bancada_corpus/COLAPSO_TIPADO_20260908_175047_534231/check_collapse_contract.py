"""Exact mathematical and adversarial checks; all records here are synthetic fixtures."""
from dataclasses import replace
from fractions import Fraction as F
import json
from collapse_contract_proposal import (
    RationalQubit, CollapseMode, CollapseCostComponents, CollapseEvent,
    ReflectionRecord, EvidenceVerdict, audit_collapse_event, collapse_event_digest,
)

checks = []
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

plus = RationalQubit(F(1, 2), F(1, 2))
minus = RationalQubit(F(1, 2), -F(1, 2))
imaginary = RationalQubit(F(1, 2), F(0), F(1, 2))
mixed = plus.diagonalize()
check("distinct_pure_phases_collide", plus != minus and plus.diagonalize() == minus.diagonalize())
check("imaginary_phase_collides_too", imaginary.diagonalize() == mixed)
check("coherence_is_lost_not_the_trace", mixed.coherence_real == 0 and mixed.trace == plus.trace == 1)
check("fixed_state_is_not_unique", RationalQubit(F(0)).is_fixed and RationalQubit(F(1)).is_fixed)
check("local_and_octave_costs_stay_separate", CollapseCostComponents(3).local_nats == F(1, 2) and CollapseCostComponents(3).octave_nats_symbolic == "3 * ln(2)")
for p in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
    for real in (F(0), F(1, 8), -F(1, 8)):
        for imag in (F(0), F(1, 8), -F(1, 8)):
            try:
                state = RationalQubit(p, real, imag)
            except ValueError:
                continue
            final = state.diagonalize()
            check(f'branch_partition_{p}_{real}_{imag}', state.branch_weight(0) + state.branch_weight(1) == 1)
            check(f"idempotence_{p}_{real}_{imag}", final.diagonalize() == final)
            check(f"identity_{p}_{real}_{imag}", state.trace == final.trace == 1)
            for outcome in (0, 1):
                probability = state.branch_weight(outcome)
                if probability:
                    branch = state.conditioned_on(outcome)
                    check(f"branch_{p}_{real}_{imag}_{outcome}", branch.is_fixed and branch.trace == 1 and branch.population_zero == 1 - outcome)
event = CollapseEvent("SYNTHETIC_EVENT_057", "SYNTHETIC_PRODUCER", plus, mixed,
                      CollapseMode.NONSELECTIVE, None, CollapseCostComponents(2))
report = audit_collapse_event(event)
check("missing_record_never_auto_attests", report.model_checks_passed and report.attestation_status == "PENDING_EXTERNAL_REFLECTION")
fixture = ReflectionRecord(collapse_event_digest(event), "SYNTHETIC_REVIEWER",
                           "TEST_FIXTURE_NOT_PHYSICAL_EVIDENCE", mixed, None)
check("missing_verifier_never_auto_attests", audit_collapse_event(event, fixture).attestation_status == "PENDING_EXTERNAL_VERIFICATION")
mock_accept = lambda e, r: EvidenceVerdict.VERIFIED_WITHIN_PROTOCOL
check("self_testimony_is_refused", audit_collapse_event(event, replace(fixture, recorder_id=event.producer_id), mock_accept).attestation_status == "REFUSED")
check("mismatched_binding_is_refused", audit_collapse_event(event, replace(fixture, event_digest="INVALID"), mock_accept).attestation_status == "REFUSED")
check("mismatched_output_is_refused", audit_collapse_event(event, replace(fixture, observed_after=plus), mock_accept).attestation_status == "REFUSED")
check("missing_reference_is_refused", audit_collapse_event(event, replace(fixture, evidence_reference=""), mock_accept).attestation_status == "REFUSED")
check("wrong_output_is_refused", not audit_collapse_event(replace(event, after=plus)).model_checks_passed)
check("unchanged_input_not_charged_as_new_transition", audit_collapse_event(replace(event, before=mixed)).attestation_status == "NO_CHANGED_TRANSITION")
check("nonselective_has_no_outcome", not audit_collapse_event(replace(event, outcome=0)).model_checks_passed)
recorded = replace(event, mode=CollapseMode.RECORDED_BRANCH, outcome=0, after=plus.conditioned_on(0))
check("possible_recorded_branch_model", audit_collapse_event(recorded).model_checks_passed)
check("recorded_branch_still_needs_reflection", audit_collapse_event(recorded).attestation_status == "PENDING_EXTERNAL_REFLECTION")
impossible = replace(recorded, before=RationalQubit(F(0)))
check("zero_weight_branch_is_refused", not audit_collapse_event(impossible).model_checks_passed)
check("no_outcome_sampled_from_mixture", not audit_collapse_event(replace(recorded, outcome=None)).model_checks_passed)
check("raw_boolean_is_not_external_verdict", audit_collapse_event(event, fixture, lambda e, r: True).attestation_status == "NOT_ATTESTED")
def broken_verifier(e, r):
    raise RuntimeError("Synthetic verification failure")
check("verifier_failure_is_visible", audit_collapse_event(event, fixture, broken_verifier).attestation_status == "EXTERNAL_VERIFICATION_FAILED")
accepted_fixture = audit_collapse_event(event, fixture, mock_accept)
check("mock_acceptance_is_only_conditional", accepted_fixture.attestation_status == "ATTESTED_WITHIN_SUPPLIED_PROTOCOL")
check("mock_acceptance_never_proves_physics_or_pays_cost", not accepted_fixture.physical_collapse_proven and accepted_fixture.cost_payment_status == "NOT_MEASURED" and not accepted_fixture.qg_gate_moved)
for invalid in (-1, True, 0.5):
    try:
        CollapseCostComponents(invalid)
    except (TypeError, ValueError):
        check(f"invalid_cost_{invalid!r}", True)
    else:
        check(f"invalid_cost_{invalid!r}", False)
for constructor in (
    lambda: RationalQubit(F(1, 2), F(1)),
    lambda: RationalQubit(0.5),
    lambda: RationalQubit(F(2)),
):
    try:
        constructor()
    except (TypeError, ValueError):
        check(f"invalid_state_{len(checks)}", True)
    else:
        check("invalid_state_accepted", False)
print(json.dumps({
    "status": "PASS_EXACT_CHECKS", "checks": len(checks),
    "records": "SYNTHETIC_TEST_FIXTURES_ONLY",
    "external_physical_attestation": False, "canonical_um_executed": False,
    "checks_run": checks,
}, ensure_ascii=False, indent=2))
