"""Fail-closed documentary R1 gate for a future Fase 9 runner.

This verifies archived source bytes and transcription. Statistical admission and
cross-reader covariance remain separate decisions. It never runs the V1 model.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


# Generated from the archived binding bytes when this candidate was created.
# Do not accept a caller-supplied manifest without an independently pinned hash.
EXPECTED_BINDING_SHA256 = "d37d7507f24bafd6960a7ff6cc5c375dea6d08fcbfadfc9d38ede2f1871b5bb0"
EXPECTED_READER_IDS = frozenset(
    {"L1_sh0es_r22", "L2_cchp", "L3_sbf", "L4_masers", "L5_tdcosmo"}
)


class ReaderGateError(ValueError):
    """A source or frozen transcription failed verification."""


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ReaderGateError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _read_json(path: Path) -> tuple[dict, bytes]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ReaderGateError(f"unreadable JSON: {path}") from exc
    if not isinstance(value, dict):
        raise ReaderGateError(f"JSON root is not an object: {path}")
    return value, raw


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _resolve_existing(path: Path) -> Path:
    try:
        return Path(path).resolve(strict=True)
    except OSError as exc:
        raise ReaderGateError(f"file missing or inaccessible: {path}") from exc


def _pinned_bytes(path: Path, pin: dict) -> bytes:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise ReaderGateError(f"source unreadable: {path}") from exc
    if len(data) != pin["bytes"] or _digest(data) != pin["sha256"]:
        raise ReaderGateError(f"source bytes/hash mismatch: {path}")
    return data


def _reconstruct_sigma(reader: dict) -> float:
    components = reader["sigma_published_components"]
    if not components or not all(isinstance(x, (int, float)) and x > 0 for x in components):
        raise ReaderGateError("invalid sigma components")
    mode = reader["local_transform"]
    if mode == "identity" and len(components) == 1:
        return float(components[0])
    if mode == "quadrature":
        return math.sqrt(sum(float(x) ** 2 for x in components))
    if mode == "arithmetic_mean" and len(components) == 2:
        return sum(components) / 2
    raise ReaderGateError(f"unsupported sigma transform: {mode}")


def verify_readers(
    binding_path: Path,
    *,
    expected_binding_sha256: str,
    allowed_source_root: Path,
) -> dict:
    """Return verified ids; raise on any missing, changed or inconsistent source.

    The binding hash must come from an independent pin. The binding itself pins
    the frozen V1 and each archived source. No statistical admission is implied.
    """
    binding_path = _resolve_existing(binding_path)
    binding, binding_raw = _read_json(binding_path)
    if _digest(binding_raw) != expected_binding_sha256:
        raise ReaderGateError("binding hash mismatch")
    if binding["schema"] != "F9_SCALAR_V1_DOCUMENTARY_BINDING_V1":
        raise ReaderGateError("unexpected binding schema")
    if binding["statistical_admission_decided"] is not False:
        raise ReaderGateError("binding unexpectedly claims statistical admission")

    frozen_pin = binding["frozen_v1"]
    frozen_path = _resolve_existing(Path(frozen_pin["path"]))
    frozen, _ = _read_json(frozen_path)
    _pinned_bytes(frozen_path, frozen_pin)
    frozen_readers = frozen["spec"]["leitores"]

    records = binding["readers"]
    ids = [record["reader_id"] for record in records]
    if len(ids) != len(set(ids)) or set(ids) != EXPECTED_READER_IDS:
        raise ReaderGateError("reader ids incomplete, duplicated or unexpected")

    root = _resolve_existing(Path(allowed_source_root))
    verified = {}
    for record in records:
        reader_id = record["reader_id"]
        source_pin = record["source"]
        source_path = _resolve_existing(Path(source_pin["path"]))
        if not source_path.is_relative_to(root):
            raise ReaderGateError(f"source outside archive: {reader_id}")
        source = _pinned_bytes(source_path, source_pin)
        anchor = record["short_literal_anchor"].encode("utf-8")
        if not anchor or anchor not in source:
            raise ReaderGateError(f"literal anchor absent: {reader_id}")

        expected = frozen_readers[reader_id]
        if expected != record["frozen_metadata"]:
            raise ReaderGateError(f"frozen metadata changed: {reader_id}")
        h0 = float(record["H0_published"])
        sigma = _reconstruct_sigma(record)
        if not (math.isfinite(h0) and math.isfinite(sigma)):
            raise ReaderGateError(f"nonfinite numeric value: {reader_id}")
        if not math.isclose(h0, expected["H0"], rel_tol=0, abs_tol=1e-12):
            raise ReaderGateError(f"H0 transcription mismatch: {reader_id}")
        if not math.isclose(sigma, expected["sigma"], rel_tol=0, abs_tol=1e-12):
            raise ReaderGateError(f"sigma transcription mismatch: {reader_id}")
        if not record["numeric_transcription_matches"]:
            raise ReaderGateError(f"unapproved numeric transcription: {reader_id}")
        verified[reader_id] = {
            "source_sha256": _digest(source),
            "source_bytes": len(source),
            "status": "REAL_DOCUMENTARY_HASH_ONLY",
            "statistical_admission": "OPEN",
        }

    return {
        "binding_sha256": _digest(binding_raw),
        "frozen_v1_sha256": _digest(frozen_path.read_bytes()),
        "verified_readers": verified,
        "statistical_admission": "OPEN",
        "cross_covariance": "OPEN",
    }


def official_archive_check() -> dict:
    root = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
    return verify_readers(
        root / "f9_scalar_reader_sources" / "VINCULO_DOCUMENTAL_CINCO_LEITORES.json",
        expected_binding_sha256=EXPECTED_BINDING_SHA256,
        allowed_source_root=root,
    )


if __name__ == "__main__":
    print(json.dumps(official_archive_check(), ensure_ascii=False, indent=2))
