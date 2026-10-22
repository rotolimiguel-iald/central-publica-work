"""Typed integration proposal for um.py; no I/O, sampling, or gate mutation.

Scope: rational qubit density matrices. Numerical model checks and external
attestation remain separate. A supplied verifier is a trust input, not a proof
of the physical origin of a record. The canonical um.py is never imported.
"""
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from hashlib import sha256
import json
from typing import Callable


class CollapseMode(str, Enum):
    NONSELECTIVE = "NONSELECTIVE"
    RECORDED_BRANCH = "RECORDED_BRANCH"


class EvidenceVerdict(str, Enum):
    VERIFIED_WITHIN_PROTOCOL = "VERIFIED_WITHIN_PROTOCOL"
    REJECTED = "REJECTED"
    UNAVAILABLE = "UNAVAILABLE"


@dataclass(frozen=True)
class RationalQubit:
    population_zero: Fraction
    coherence_real: Fraction = Fraction(0)
    coherence_imag: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        values = (self.population_zero, self.coherence_real, self.coherence_imag)
        if any(type(value) is not Fraction for value in values):
            raise TypeError("Exact Fraction values are required.")
        p = self.population_zero
        if not Fraction(0) <= p <= Fraction(1):
            raise ValueError("Populations must lie in [0, 1].")
        if self.coherence_real**2 + self.coherence_imag**2 > p * (1 - p):
            raise ValueError("Density matrix is not positive semidefinite.")

    @property
    def trace(self) -> Fraction:
        return self.population_zero + (1 - self.population_zero)

    @property
    def is_fixed(self) -> bool:
        return self.coherence_real == 0 and self.coherence_imag == 0

    def diagonalize(self) -> "RationalQubit":
        return RationalQubit(self.population_zero)

    def branch_weight(self, outcome: int) -> Fraction:
        if type(outcome) is not int or outcome not in (0, 1):
            raise ValueError("Outcome must be an explicit 0 or 1.")
        return self.population_zero if outcome == 0 else 1 - self.population_zero

    def conditioned_on(self, outcome: int) -> "RationalQubit":
        if self.branch_weight(outcome) <= 0:
            raise ValueError("An impossible branch cannot be normalized.")
        return RationalQubit(Fraction(1 - outcome))


@dataclass(frozen=True)
class CollapseCostComponents:
    """TGL input law, in nats; an assigned cost is not a measured payment."""
    octaves: int

    def __post_init__(self) -> None:
        if type(self.octaves) is not int or self.octaves < 0:
            raise ValueError("Octave count must be a nonnegative integer.")

    @property
    def local_nats(self) -> Fraction:
        return Fraction(1, 2)

    @property
    def octave_nats_symbolic(self) -> str:
        return f"{self.octaves} * ln(2)"

    @property
    def status(self) -> str:
        return "INPUT_TGL_COST_LAW"

    # No total is provided: addition of distinct components needs its own law.


@dataclass(frozen=True)
class CollapseEvent:
    event_id: str
    producer_id: str
    before: RationalQubit
    after: RationalQubit
    mode: CollapseMode
    outcome: int | None
    cost: CollapseCostComponents

    def __post_init__(self) -> None:
        if not self.event_id.strip() or not self.producer_id.strip():
            raise ValueError("An event and its producer must be identified.")
        if type(self.before) is not RationalQubit or type(self.after) is not RationalQubit:
            raise TypeError("Both states must be exact rational qubit states.")
        if type(self.cost) is not CollapseCostComponents:
            raise TypeError("Costs must have their own typed components.")
        if type(self.mode) is not CollapseMode:
            raise TypeError("An explicit typed mode is required.")


@dataclass(frozen=True)
class ReflectionRecord:
    event_digest: str
    recorder_id: str
    evidence_reference: str
    observed_after: RationalQubit
    observed_outcome: int | None


@dataclass(frozen=True)
class CollapseAudit:
    model_checks_passed: bool
    attestation_status: str
    reason: str
    cost_status: str = "INPUT_TGL_COST_LAW"
    cost_payment_status: str = "NOT_MEASURED"
    physical_collapse_proven: bool = False
    qg_gate_moved: bool = False


def _fraction_payload(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def _state_payload(state: RationalQubit) -> dict:
    return {
        "population_zero": _fraction_payload(state.population_zero),
        "coherence_real": _fraction_payload(state.coherence_real),
        "coherence_imag": _fraction_payload(state.coherence_imag),
    }


def collapse_event_digest(event: CollapseEvent) -> str:
    """Byte integrity binding only; a hash is not independent testimony."""
    payload = {
        "schema": "TGL_COLLAPSE_CONTRACT_PROPOSAL_057",
        "event_id": event.event_id,
        "producer_id": event.producer_id,
        "before": _state_payload(event.before),
        "after": _state_payload(event.after),
        "mode": event.mode.value,
        "outcome": event.outcome,
        "local_nats": _fraction_payload(event.cost.local_nats),
        "octaves": event.cost.octaves,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    return sha256(raw).hexdigest()


def audit_collapse_event(
    event: CollapseEvent,
    record: ReflectionRecord | None = None,
    verify_external: Callable[[CollapseEvent, ReflectionRecord], EvidenceVerdict] | None = None,
) -> CollapseAudit:
    """Check a supplied event, then a separately supplied reflection record.

    This function cannot certify who controls an identifier or produced a
    physical record. The external verifier must be connected and independently
    audited by the integrating session. No default verifier claims success.
    """
    if event.mode is CollapseMode.NONSELECTIVE:
        if event.outcome is not None:
            return CollapseAudit(False, "REFUSED", "Nonselective mode has no selected outcome.")
        expected = event.before.diagonalize()
    elif event.mode is CollapseMode.RECORDED_BRANCH:
        try:
            expected = event.before.conditioned_on(event.outcome)
        except (ValueError, TypeError):
            return CollapseAudit(False, "REFUSED", "Missing, invalid, or zero-weight branch.")
    else:
        return CollapseAudit(False, "REFUSED", "Unknown transition mode.")
    if event.after != expected:
        return CollapseAudit(False, "REFUSED", "Output does not satisfy the specified map.")
    if not event.after.is_fixed or event.after.trace != event.before.trace:
        return CollapseAudit(False, "REFUSED", "Fixed point or normalization check failed.")
    if event.before == event.after:
        return CollapseAudit(False, "NO_CHANGED_TRANSITION", "Input was already the reported fixed point.")
    if record is None:
        return CollapseAudit(True, "PENDING_EXTERNAL_REFLECTION", "No reflection record supplied.")
    if type(record) is not ReflectionRecord:
        return CollapseAudit(True, "REFUSED", "Invalid record type.")
    if not record.recorder_id.strip() or record.recorder_id == event.producer_id:
        return CollapseAudit(True, "REFUSED", "Self-declaration is not accepted as external testimony.")
    if not record.evidence_reference.strip():
        return CollapseAudit(True, "REFUSED", "Evidence reference is missing.")
    if record.event_digest != collapse_event_digest(event):
        return CollapseAudit(True, "REFUSED", "Record is not bound to this event.")
    if record.observed_after != event.after or record.observed_outcome != event.outcome:
        return CollapseAudit(True, "REFUSED", "Reflection disagrees with the event output.")
    if verify_external is None:
        return CollapseAudit(True, "PENDING_EXTERNAL_VERIFICATION", "No external verification protocol supplied.")
    try:
        verdict = verify_external(event, record)
    except Exception as failure:
        return CollapseAudit(True, "EXTERNAL_VERIFICATION_FAILED", type(failure).__name__)
    if verdict is not EvidenceVerdict.VERIFIED_WITHIN_PROTOCOL:
        return CollapseAudit(True, "NOT_ATTESTED", "External evidence was rejected or unavailable.")
    return CollapseAudit(
        True, "ATTESTED_WITHIN_SUPPLIED_PROTOCOL",
        "Conditional on the supplied verifier; physical provenance and cost payment are not certified here.",
    )
