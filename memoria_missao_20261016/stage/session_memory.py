"""Trusted local adapter for the shared IALD memory core; no remote calls."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid
from datetime import datetime, timezone

PROTOCOL = "iald-memory-session/v1"
MAX_INPUT_BYTES = 2 * 1024 * 1024
# D4 (12/10/2026): name/identity/content filters live in iald_memory.guard (fail-closed);
# the former exact-name sets FORBIDDEN_NAMES/FORBIDDEN_PARTS were removed (they let
# iald_psion_state_32B.json, *.bak_*, .env.local, hard links and NFD names through).
OPS = {"init", "get", "project", "transition", "verify"}
ALLOWED_ACTORS = {"model", "agent"}
GUARD_LOG_NAME = "guard_refusals.jsonl"
# R2 (13/10/2026, review finding 4): a reference file is read only through the guard and only these keys are
# accepted. Anything else in the file (e.g. a confidential JSON that happens to carry the identity keys) is a
# visible refusal; nothing from such a file is ever echoed back.
REFERENCE_KEYS = frozenset({"protocol", "store", "context_id", "scope", "objective_sha256", "source",
                            "request_id", "authority"})
REFERENCE_SOURCE_KEYS = frozenset({"path", "sha256", "bytes"})
MAX_REFERENCE_BYTES = 64 * 1024

class ProtocolError(ValueError):
    pass

def digest(data):
    return hashlib.sha256(data).hexdigest()

def _guard():
    # Imported lazily: main() puts --core-root on sys.path before any operation.
    from iald_memory import guard
    return guard

def _guarded_read(raw_path, max_bytes, log_path, where, not_file, too_large):
    # R2.1 (review N3): the requested and resolved NAMES are checked before any open; then the guard opens a
    # handle with READ access and without FILE_SHARE_DELETE (R2.2: comment corrected; it is not an attributes-only
    # handle), checks hard-link count, identity and the FINAL path of THAT handle, and reads the same file object
    # (never the name again). R2.2 (N1): the path SHAPE is refused before realpath. The refusal names the rule,
    # never the bytes.
    guard = _guard()
    try:
        final, data = guard.read_checked(raw_path, max_bytes=max_bytes, log_path=log_path, where=where)
    except guard.PathRefused as exc:
        raise ProtocolError("source_path_not_allowed:" + exc.reason) from None
    except guard.NotRegularFile:
        raise ProtocolError(not_file) from None
    if len(data) > max_bytes:
        raise ProtocolError(too_large)
    return Path(final), data

def read_allowed_file(raw_path, log_path=None):
    return _guarded_read(raw_path, MAX_INPUT_BYTES, log_path, "read_allowed_file", "source_is_not_file",
                         "source_too_large")

def guarded_reference_path(raw_path, log_path=None, where="write_reference"):
    """Refuse (before exists/read/create) a reference path the guard classifies as confidential."""
    reason = _guard().is_confidential_path(raw_path, log_path=log_path, where=where)
    if reason:
        raise ProtocolError("source_path_not_allowed:" + reason)  # same code as every guarded read
    return Path(raw_path)

def load_reference(raw_path, log_path=None, where="reference"):
    """Read a reference through the guard; accept only the protocol keys; return a clean copy."""
    # Same code as every guarded read (source_path_not_allowed:<rule>); R2.1: read through the handle (N3).
    _, raw = _guarded_read(raw_path, MAX_REFERENCE_BYTES, log_path, where, "reference_is_not_file",
                           "reference_too_large")
    try:
        ref = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        raise ProtocolError("reference_not_json") from None
    if not isinstance(ref, dict):
        raise ProtocolError("reference_not_object")
    unexpected = set(ref) - REFERENCE_KEYS
    if unexpected:
        # Key NAMES are not echoed either: only their count.
        raise ProtocolError("reference_unexpected_keys:%d" % len(unexpected))
    source = ref.get("source")
    if source is not None and (not isinstance(source, dict) or set(source) - REFERENCE_SOURCE_KEYS):
        raise ProtocolError("reference_source_unexpected_keys")
    # Defence in depth: the accepted keys are scanned like any text that leaves the process.
    _guard().assert_clean_text(json.dumps(ref, ensure_ascii=False, sort_keys=True), where + ".content", log_path=log_path)
    return dict(ref)

def create_reference(path, data):
    """References are immutable: publish complete bytes without overwrite."""
    path = Path(path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise ProtocolError("reference_already_exists")
    temp = path.with_name(path.name + ".tmp_" + uuid.uuid4().hex)
    try:
        with temp.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if temp.stat().st_size != len(data) or temp.read_bytes() != data:
            raise ProtocolError("temporary_verification_failed")
        # Hard-link publication fails if another process won. No check/replace gap.
        os.link(temp, path)
        if path.read_bytes() != data:
            raise ProtocolError("final_verification_failed")
    finally:
        if temp.exists():
            temp.unlink()

def actor_for(request):
    actor = request.get("actor") or {"id": "local-session", "kind": "model"}
    if not isinstance(actor, dict) or set(actor) != {"id", "kind"}:
        raise ProtocolError("actor_requires_id_and_kind")
    if actor["kind"] not in ALLOWED_ACTORS or not isinstance(actor["id"], str) or not actor["id"].strip():
        raise ProtocolError("actor_must_be_local_model_or_agent")
    return actor

def reference_for(request, store_root, log_path=None):
    raw = request.get("reference")
    if raw:
        ref = load_reference(raw, log_path, where="reference")
        if ref.get("protocol") != PROTOCOL:
            raise ProtocolError("unsupported_reference_protocol")
        if Path(ref["store"]).resolve() != store_root:
            raise ProtocolError("reference_store_mismatch")
        if request.get("context_id", ref["context_id"]) != ref["context_id"]:
            raise ProtocolError("reference_context_mismatch")
        if request.get("scope", ref["scope"]) != ref["scope"]:
            raise ProtocolError("reference_scope_mismatch")
        _guard().assert_scope_allowed(ref["scope"])  # D6: Escritório never enters this bank.
        return ref
    if not request.get("context_id") or not request.get("scope"):
        raise ProtocolError("context_id_and_scope_or_reference_required")
    _guard().assert_scope_allowed(request["scope"])
    return {"protocol": PROTOCOL, "store": str(store_root),
            "context_id": request["context_id"], "scope": request["scope"]}

def dispatch(request, store_root, MemoryStore):
    if not isinstance(request, dict) or request.get("operation") not in OPS:
        raise ProtocolError("operation_must_be_init_get_project_transition_verify")
    op = request["operation"]
    if op != "init" and not (store_root / "memory.sqlite3").is_file():
        raise ProtocolError("memory_store_missing")
    guard = _guard()
    log_path = store_root / GUARD_LOG_NAME  # refusals are recorded beside the bank, never the text
    store = MemoryStore(store_root)
    if op == "init":
        source, raw = read_allowed_file(request["objective_file"], log_path)
        actual = digest(raw)
        if request.get("objective_sha256") != actual:
            raise ProtocolError("objective_source_hash_mismatch")
        objective = raw.decode("utf-8")  # Do not normalize CRLF or strip the original.
        # D4: keys, Escritório paths and confidential names never enter the bank (visible refusal).
        guard.assert_clean_text(objective, "init.objective", log_path=log_path)
        scope = request["scope"]
        guard.assert_scope_allowed(scope)  # D6
        request_id = str(uuid.UUID(request["request_id"]))
        identity = json.dumps([scope, request_id], sort_keys=True, separators=(",", ":"))
        context_id = request.get("context_id") or str(uuid.uuid5(uuid.NAMESPACE_URL, "iald-memory-session:" + identity))
        # Rebinding a session must not replace the original inscription actor.
        # A reference already bound to another identity is rejected before writes.
        write_reference = request.get("write_reference")
        if write_reference:
            # R2: the guard decides BEFORE exists/read/create (finding 4: a confidential-named JSON was read and echoed).
            write_reference = guarded_reference_path(write_reference, log_path)
        if write_reference and write_reference.exists():
            existing = load_reference(write_reference, log_path, where="write_reference")
            expected = {"protocol": PROTOCOL, "store": str(store_root), "context_id": context_id,
                        "scope": scope, "objective_sha256": actual, "request_id": request_id}
            if any(existing.get(k) != value for k, value in expected.items()):
                raise ProtocolError("existing_reference_identity_mismatch")
        from iald_memory import ContextNotFound
        actor = actor_for(request)
        parent_id = request.get("parent_id")
        effective_constraints = request.get("constraints")
        if effective_constraints is not None and not isinstance(effective_constraints, dict):
            raise ProtocolError("constraints_object_required")
        if parent_id is not None:
            # Resolve inheritance identically for creation and later attachment.
            # Reading the parent through get also checks the exact same scope.
            parent = store.get(parent_id, scope)
            if effective_constraints is None:
                effective_constraints = parent["constraints"]
            elif effective_constraints != parent["constraints"]:
                raise ProtocolError("child_constraints_must_preserve_parent")
        elif effective_constraints is None:
            effective_constraints = {}
        try:
            snapshot = store.get(context_id, scope)
        except ContextNotFound:
            snapshot = store.ensure_context(context_id, objective=objective, scope=scope,
                actor=actor, constraints=effective_constraints, parent_id=parent_id)
        else:
            if (snapshot["objective"] != objective
                    or snapshot["constraints"] != effective_constraints
                    or snapshot["parent_id"] != parent_id):
                raise ProtocolError("existing_context_anchor_mismatch")
        ref = {"protocol": PROTOCOL, "store": str(store_root), "context_id": context_id,
            "scope": snapshot["scope"], "objective_sha256": snapshot["objective_sha256"],
            "source": {"path": str(source), "sha256": actual, "bytes": len(raw)},
            "request_id": request_id,
            "authority": "local_os_access_only_not_external_identity_authentication"}
        if write_reference:
            ref_path = guarded_reference_path(Path(write_reference).resolve(), log_path)
            if ref_path.exists():
                existing = load_reference(ref_path, log_path, where="write_reference")
                if any(existing.get(k) != ref.get(k) for k in ("protocol", "store", "context_id", "scope", "objective_sha256", "request_id")):
                    raise ProtocolError("existing_reference_identity_mismatch")
                ref = existing  # Preserve the first reference and its source provenance.
            else:
                create_reference(ref_path, (json.dumps(ref, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        # Defence in depth: a re-attached legacy context is scanned before its state leaves the process.
        guard.assert_clean_text(json.dumps(snapshot, ensure_ascii=False), "init.snapshot", log_path=log_path)
        return {"reference": ref, "snapshot": snapshot, "source_verified": True}
    ref = reference_for(request, store_root, log_path)
    context_id, scope = ref["context_id"], ref["scope"]
    current = store.get(context_id, scope)
    if ref.get("objective_sha256") and current["objective_sha256"] != ref["objective_sha256"]:
        raise ProtocolError("reference_anchor_mismatch")
    if op == "get":
        guard.assert_clean_text(json.dumps(current, ensure_ascii=False), "get", log_path=log_path)
        return current
    if op == "project":
        result = store.project(context_id, scope, max_chars=request.get("max_chars", 24000),
                               current_input=request.get("current_input", ""))
        # The projection goes to the session's provider: it is scanned before it is returned.
        guard.assert_clean_text(result["text"], "project", log_path=log_path)
        return result
    if op == "verify":
        return store.verify(context_id, scope)
    changes = request.get("changes")
    if "changes_file" in request:
        if changes is not None:
            raise ProtocolError("changes_or_changes_file_not_both")
        _, raw = read_allowed_file(request["changes_file"], log_path)
        expected = request.get("changes_sha256")
        if expected != digest(raw):
            raise ProtocolError("changes_source_hash_mismatch")
        changes = json.loads(raw.decode("utf-8"))
    if not isinstance(changes, dict):
        raise ProtocolError("changes_object_required")
    guard.assert_clean_text(json.dumps(changes, ensure_ascii=False), "transition.changes", log_path=log_path)
    return store.transition(context_id, scope,
        expected_revision=request["expected_revision"], event_id=request["event_id"],
        actor=actor_for(request), changes=changes)

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument("--core-root", type=Path, default=base / "lib",
                        help="Directory containing the installed iald_memory package.")
    parser.add_argument("--store", type=Path, default=base / "state")
    args = parser.parse_args(argv)
    sys.path.insert(0, str(args.core_root.resolve()))
    try:
        from iald_memory import MemoryStore
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ProtocolError("request_too_large")
        request = json.loads(raw.decode("utf-8"))
        result = dispatch(request, args.store.resolve(), MemoryStore)
        print(json.dumps({"ok": True, "protocol": PROTOCOL, "result": result}, ensure_ascii=False))
        return 0
    except Exception as exc:
        # Expected fail-closed errors are explicit. No network, fallback, or retry is performed.
        print(json.dumps({"ok": False, "protocol": PROTOCOL,
                          "error": type(exc).__name__, "message": str(exc)}, ensure_ascii=False))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
