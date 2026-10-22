"""Pure validation prototype; no persistence, authentication, dispatch or deployment."""
from dataclasses import dataclass
import hashlib
import json
import re


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


@dataclass(frozen=True)
class Snapshot:
    job_id: str
    request_id: str
    context_id: str
    prompt_sha256: str
    version: int = 0
    stage: str = "awaiting_dispatch"
    original_constraints_json: str = "null"
    memory_anchor_constraints_json: str = "{}"
    memory_objective_sha256: str = ""
    actions: tuple = ("create",)
    prepared_prompt_exists: bool = False
    thread_exists: bool = False
    task_exists: bool = False
    attempt_exists: bool = False
    pending_memory_outbox: bool = False


@dataclass(frozen=True)
class Authority:
    # This is a trusted caller seam, NOT evidence that authentication occurred.
    # Production must construct it only from an independently verified human order.
    kind: str
    thread_id: str
    unit: str
    order_sha256: str


@dataclass(frozen=True)
class Proposal:
    event_id: str
    supplement_sha256: str
    original_constraints_json: str
    effective_constraints_json: str
    event_json: str
    replay: bool


def propose(snapshot, raw, expected_sha256, expected_version, authority,
            verified_pins, normalize, prior=None):
    """Validate a proposed append, or exact read-only replay of an existing one.

    verified_pins is a caller-measured mapping path -> (sha256, byte length).
    normalize is the installed request_controls.normalize (in tests).
    No source read, file write, SQL, ACOM or provider call occurs here.
    """
    if digest(raw) != expected_sha256:
        raise ValueError("supplement bytes changed")
    contract = json.loads(raw)
    if contract.get("schema") != "iald-scientific-contract-supplement/v1":
        raise ValueError("unsupported supplement schema")
    identities = {"job_id": snapshot.job_id, "request_id": snapshot.request_id,
                  "original_memory_context_id": snapshot.context_id,
                  "original_prompt_sha256": snapshot.prompt_sha256}
    if any(contract.get(k) != v for k, v in identities.items()):
        raise ValueError("original identity mismatch")
    if contract.get("preserve_original") is not True:
        raise ValueError("original preservation required")
    order = contract["authenticated_scope_order"]
    pin = order["source"]
    if authority.kind != "verified_direct_human_order":
        raise ValueError("model or unverified actor cannot authorize binding")
    if (authority.thread_id != order["thread_id"] or authority.unit != contract["unit"]
            or authority.order_sha256 != pin["sha256"]):
        raise ValueError("authority does not cover supplement")
    pins = [pin, *contract["primary_source_pins"], contract["working_v392"]]
    for item in pins:
        if not re.fullmatch("[0-9a-f]{64}", item["sha256"]):
            raise ValueError("invalid source pin")
        if type(item["bytes"]) is not int or item["bytes"] <= 0:
            raise ValueError("invalid source size")
        if verified_pins.get(item["path"]) != (item["sha256"], item["bytes"]):
            raise ValueError("source unreadable or pin changed")
    effective = normalize(contract["execution_constraints"])
    if not effective or effective["branch_id"] != contract["unit"]:
        raise ValueError("unit and routing branch differ")
    effective_json = canonical(effective)
    if snapshot.original_constraints_json != "null":
        raise ValueError("original constraints must remain null")
    if snapshot.memory_anchor_constraints_json != "{}":
        raise ValueError("immutable ACOM anchor differs")
    if snapshot.memory_objective_sha256 != snapshot.prompt_sha256:
        raise ValueError("immutable ACOM objective differs")
    event_id = "scientific-contract:" + snapshot.job_id + ":" + expected_sha256
    event = {"schema": "scientific-contract-binding/v1", "job_id": snapshot.job_id,
             "request_id": snapshot.request_id, "memory_context_id": snapshot.context_id,
             "original_prompt_sha256": snapshot.prompt_sha256,
             "original_constraints": None, "effective_constraints": effective,
             "supplement_sha256": expected_sha256, "authority_sha256": authority.order_sha256,
             "authority_thread_id": authority.thread_id, "unit": authority.unit,
             "source_pins": pins, "statute": "INPUT"}
    encoded = canonical(event)
    if prior is not None:
        # Retrieval of a prior exact append is harmless even after dispatch.
        # It MUST NOT append, alter stage, synchronize providers or restart work.
        if prior.event_id != event_id or prior.event_json != encoded:
            raise ValueError("rebinding or changed supplement forbidden")
        return Proposal(event_id, expected_sha256, "null", effective_json, encoded, True)
    if snapshot.version != expected_version:
        raise ValueError("stale coordination version")
    if snapshot.stage != "awaiting_dispatch" or snapshot.actions != ("create",):
        raise ValueError("binding must precede every draft or dispatch action")
    if any((snapshot.prepared_prompt_exists, snapshot.thread_exists, snapshot.task_exists,
            snapshot.attempt_exists, snapshot.pending_memory_outbox)):
        raise ValueError("work or unresolved memory checkpoint already exists")
    return Proposal(event_id, expected_sha256, "null", effective_json, encoded, False)
