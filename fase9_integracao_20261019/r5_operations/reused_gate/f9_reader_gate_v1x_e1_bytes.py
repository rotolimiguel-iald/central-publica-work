"""F3.1.E1 byte-lineage documentary gate for a relocated two-witness package.

Re-read F3.4, R5, R5.1 and R5.2 bytes at each invocation. Historic paths
in pinned metadata remain documentary strings; actual reads map under the
bundle containing this binding. No admission, opening, freeze or verdict.
"""

from __future__ import annotations

import copy
from decimal import Decimal, InvalidOperation
import hashlib
import json
import math
from pathlib import Path
import re

import f9_reader_gate as base


ReaderGateError = base.ReaderGateError
BINDING_SCHEMA = "F9_SCALAR_V1X_DOCUMENTARY_BINDING_V2_DRAFT"
F34_DRAFT_SHA256 = "ca59870c4e840bf6c87b7b5051cc1b4e6ff25a88d026fca38893291fdd14153f"
F34_SPEC_SHA256 = "dbe01f4cef9e6d155d51cbf2930014289144761bb8b948a3b3195615bc609e1b"
ORIGINAL_R4_SHA256 = "3f4017bf3229903106d2c85388bde9ebfd57e076428e48af5be33c873d5c2d00"
F34_RESOLUTION_SHA256 = "01b6a50e6d1fe3a2531b6400880f028b603f22f787c05dacb563d715d2db535d"
R51_SHA256 = "f73bee1d8b45c43575e73bea8f4adf10724d039f1b96a50542cd7e70ae100c60"
R52_DRAFT_SHA256 = "6b6769da821b03dd96728202b478d3c0920b51f68cb6ca013916899390c517cd"
R5_SHA256 = "ab84d493c9ac54083eb78495e19e9da93782392ca5ffa5981e5ac7c83ce76f09"
R52_SPEC_SHA256 = "9c7f05a1821ccb88936c0190934db524f4dca1de20ab2c98c5206a4c157cbb7c"
R52_FUNCTION_SHA256 = "544f60ef928c32620f2956665618daca4cb4116419d91197a09880c91c5274a5"
R52_STATE = "RASCUNHO_DOCUMENTAL_R5_2_NAO_CONGELADO"
E1_DRAFT_SHA256 = "81a970926345832ad34d4963b0fadf70827003086e2876295d07024f83ffcca7"
E1_SPEC_SHA256 = "406d9d2dde90d6d250d71938ffbaaf3b881fdd459629630770cdc27c0d52bf58"
EXPECTED_READER_IDS = frozenset({
    "L1_sh0es_r22", "L1b_sh0es_r25", "L2_cchp", "L3_sbf",
    "L4_masers_5", "L4_masers_6", "L5_tdcosmo", "L6_sirenes",
})
PRIMARY_READER_IDS = frozenset({
    "L1_sh0es_r22", "L2_cchp", "L3_sbf", "L4_masers_5", "L5_tdcosmo",
})
DECLARED_ONLY_IDS = frozenset({"L1b_sh0es_r25", "L6_sirenes"})
MASER_READER_IDS = frozenset({"L4_masers_5", "L4_masers_6"})
PESCE_PDF_SHA256 = "c9f2d2b626fee60d77928856d217a2cbe546f06c69cd9e7ac804f4ab652e731a"
PESCE_PAGE6_SHA256 = "e5a8eef8c099fa01b9d2d761567e7b22a5a66c8332f10b5c16dde24a4cf79d7a"
MASER_TABLE_LITERALS = {
    "L4_masers_5": "NGC 4258\n73.6+3.1\n−3.0",
    "L4_masers_6": "Fit using all galaxies:\n73.9+3.0\n−3.0",
}
HISTORICAL_V1_SHA256 = "1893261e730994b3508d14dd2105f8aae3a764d3d217e28bd5939cb58f865273"
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")

HISTORIC_ARCHIVE_ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT")
ANCESTOR_NAMES = (
    ("F3.4", "PREREGISTRO_FASE9_V2_R4_F34_DUAS_TESTEMUNHAS_20261008.json", F34_DRAFT_SHA256),
    ("R5", "PREREGISTRO_FASE9_V2_R5_F31_20261008.json", R5_SHA256),
    ("R5.1", "PREREGISTRO_FASE9_V2_R5_1_F31_20261008.json", R51_SHA256),
    ("R5.2", "PREREGISTRO_FASE9_V2_R5_2_F31_20261008.json", R52_DRAFT_SHA256),
    ("F3.1.E1", "PREREGISTRO_FASE9_V2_R5_2_F31_LABELS_E1_20261008.json", E1_DRAFT_SHA256),
)


def _bundle_root(binding_path: Path) -> Path:
    path = base._resolve_existing(binding_path)
    if path.parent.name != "F3.2" or path.parent.parent.name != "ORDEM_019":
        raise ReaderGateError("binding outside portable F3.2 package")
    return path.parents[2]


def _relocated_path(documentary_path: str, bundle_root: Path, subtree: str) -> Path:
    original = Path(documentary_path)
    try:
        relative = original.relative_to(HISTORIC_ARCHIVE_ROOT)
    except ValueError as exc:
        raise ReaderGateError("documentary path outside historic package") from exc
    expected = Path(subtree)
    if relative != expected and not relative.is_relative_to(expected):
        raise ReaderGateError("documentary path outside expected subtree")
    destination = base._resolve_existing(bundle_root / relative)
    allowed = base._resolve_existing(bundle_root / expected)
    if not destination.is_relative_to(allowed):
        raise ReaderGateError("relocated path escaped expected subtree")
    return destination


def _verify_ancestor_bytes(binding: dict, draft_pin: dict, draft: dict,
                           draft_raw: bytes, bundle_root: Path) -> list[dict]:
    records = binding.get("r52_ancestor_files")
    if not isinstance(records, list) or len(records) != 5:
        raise ReaderGateError("five lineage file pins required")
    actual = []
    previous = None
    for index, (role, name, expected_sha) in enumerate(ANCESTOR_NAMES):
        pin = _pin(records[index], f"ancestor[{index}]")
        documentary = HISTORIC_ARCHIVE_ROOT / "ORDEM_019" / "F3.1" / name
        if pin.get("role") != role or pin["path"] != str(documentary) or pin["sha256"] != expected_sha:
            raise ReaderGateError(f"ancestor identity differs: {role}")
        if index == 4:
            if pin != {**draft_pin, "role": role}:
                raise ReaderGateError("F3.1.E1 projection pin differs from draft pin")
            obj, raw = draft, draft_raw
        else:
            path = _relocated_path(pin["path"], bundle_root, "ORDEM_019/F3.1")
            obj, raw = base._read_json(path)
        digest = base._digest(raw)
        if len(raw) != pin["bytes"] or digest != expected_sha:
            raise ReaderGateError(f"ancestor bytes/hash mismatch: {role}")
        if previous is not None and obj.get("derived_from") != previous:
            raise ReaderGateError(f"ancestor parent does not bind bytes: {role}")
        actual.append({"role": role, "sha256": digest, "bytes": len(raw)})
        previous = {"path": pin["path"], "bytes": pin["bytes"], "sha256": pin["sha256"]}
    return actual


def _object(value: object, name: str) -> dict:
    if not isinstance(value, dict):
        raise ReaderGateError(f"{name} must be an object")
    return value


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ReaderGateError(f"{name} must be nonempty text")
    return value


def _number(value: object, name: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ReaderGateError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0):
        raise ReaderGateError(f"{name} must be finite and valid")
    return result


def _pin(value: object, name: str) -> dict:
    pin = _object(value, name)
    _text(pin.get("path"), f"{name}.path")
    if isinstance(pin.get("bytes"), bool) or not isinstance(pin.get("bytes"), int) or pin["bytes"] <= 0:
        raise ReaderGateError(f"{name}.bytes must be positive integer")
    digest = _text(pin.get("sha256"), f"{name}.sha256")
    if not _SHA256.fullmatch(digest):
        raise ReaderGateError(f"{name}.sha256 malformed")
    return pin


def _window(value: object, expected: float, source: bytes, name: str) -> None:
    """Pin a verbatim source window containing the actual declared number."""
    window = _object(value, name)
    literal = _text(window.get("literal"), f"{name}.literal")
    numeral = _text(window.get("numeric_literal"), f"{name}.numeric_literal")
    if len(literal) > 4096 or len(numeral) > 64:
        raise ReaderGateError(f"{name} too long")
    # A bare numeral is ambiguous in the CCHP source (1.33 occurs three
    # times). The quote must carry a recognisable source label as context.
    if len(literal) < 16 or re.search(r"[A-Za-z]{3,}", literal) is None:
        raise ReaderGateError(f"{name} lacks minimum source context")
    try:
        lexical = Decimal(numeral.replace(",", "."))
    except InvalidOperation as exc:
        raise ReaderGateError(f"{name} has invalid numeric literal") from exc
    if not lexical.is_finite() or lexical != Decimal(str(expected)):
        raise ReaderGateError(f"{name} numeric literal differs from transcription")
    # Reject a generic anchor or a number embedded in another number.
    pattern = rf"(?<![0-9.,]){re.escape(numeral)}(?![0-9.,])"
    if re.search(pattern, literal) is None:
        raise ReaderGateError(f"{name} does not contain its numeric literal")
    occurrences = source.count(literal.encode("utf-8"))
    if occurrences == 0:
        raise ReaderGateError(f"{name} is absent from pinned source bytes")
    if occurrences != 1:
        raise ReaderGateError(f"{name} is ambiguous in pinned source bytes: {occurrences} occurrences")


def _signed_source_sides(windows: dict, h0: float, plus: float, minus: float,
                         reader_id: str) -> None:
    """Bind both uncertainty sides to the signs next to H0 in source text.

    Matching two unsigned numerals separately accepts a coherent exchange of
    plus and minus in the binding. This check consumes the pinned H0 window,
    which is also required to occur verbatim in pinned source bytes.
    """
    row = _object(windows.get("H0"), f"{reader_id}.H0_window")
    literal = _text(row.get("literal"), f"{reader_id}.H0_window.literal")
    center = re.escape(str(h0))
    upper = re.escape(str(plus))
    lower = re.escape(str(minus))
    signed_row = (
        rf"(?<![0-9.,]){center}(?![0-9.,])[^0-9]{{0,12}}"
        rf"\+{upper}(?![0-9.,])[^0-9]{{0,12}}[-−]{lower}(?![0-9.,])"
    )
    if re.search(signed_row, literal) is None:
        raise ReaderGateError(f"source signs do not bind asymmetric sides: {reader_id}")


def _pinned_file(value: object, name: str, root: Path, bundle_root: Path) -> tuple[dict, Path, bytes]:
    pin = _pin(value, name)
    path = _relocated_path(pin["path"], bundle_root, "ORDEM_018")
    if root is not None and not path.is_relative_to(root):
        raise ReaderGateError(f"{name} outside archive")
    raw = base._pinned_bytes(path, pin)
    return pin, path, raw


def _source_text(record: dict, reader_id: str, root: Path, bundle_root: Path) -> tuple[bytes, bytes]:
    source_pin, source_path, source = _pinned_file(record.get("source"), f"{reader_id}.source", root, bundle_root)
    if reader_id not in MASER_READER_IDS:
        if record.get("text_projection") is not None or record.get("projection_receipt") is not None:
            raise ReaderGateError(f"unexpected projection: {reader_id}")
        return source, source
    if source_path.suffix.lower() != ".pdf":
        raise ReaderGateError(f"maser source must be pinned PDF: {reader_id}")
    if source_pin["sha256"] != PESCE_PDF_SHA256:
        raise ReaderGateError(f"maser PDF pin differs from Pesce archive: {reader_id}")
    projection_pin, _, projection = _pinned_file(
        record.get("text_projection"), f"{reader_id}.text_projection", root, bundle_root
    )
    if projection_pin["sha256"] != PESCE_PAGE6_SHA256:
        raise ReaderGateError(f"maser Table 2 projection pin differs: {reader_id}")
    _, _, receipt_raw = _pinned_file(
        record.get("projection_receipt"), f"{reader_id}.projection_receipt", root, bundle_root
    )
    try:
        receipt = json.loads(receipt_raw.decode("utf-8"), object_pairs_hook=base._unique_object)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ReaderGateError("PDF extraction receipt unreadable") from exc
    receipt = _object(receipt, "PDF extraction receipt")
    if receipt.get("sha256") != source_pin["sha256"] or receipt.get("bytes") != source_pin["bytes"]:
        raise ReaderGateError("PDF extraction receipt does not bind source")
    pages = receipt.get("extracted_pages")
    if not isinstance(pages, list) or not any(
        isinstance(page, dict)
        and page.get("page") == 6
        and page.get("sha256") == projection_pin["sha256"]
        and page.get("bytes") == projection_pin["bytes"]
        for page in pages
    ):
        raise ReaderGateError("PDF extraction receipt does not bind page 6")
    return source, projection


def verify_v1x_binding(
    binding_path: Path,
    *,
    expected_binding_sha256: str,
    allowed_source_root: Path,
    expected_spec_sha256: str | None = None,
) -> dict:
    """Verify new V1.x documentary binding; return its single-read V2 spec snapshot.

    Source byte verification is not operator admission, likelihood reconstruction,
    independence, a real-data opening, or a frozen preregistration.
    """
    if not isinstance(expected_binding_sha256, str) or not _SHA256.fullmatch(expected_binding_sha256):
        raise ReaderGateError("binding pin malformed")
    binding_path = base._resolve_existing(binding_path)
    bundle_root = _bundle_root(binding_path)
    binding, binding_raw = base._read_json(binding_path)
    if base._digest(binding_raw) != expected_binding_sha256:
        raise ReaderGateError("binding hash mismatch")
    if binding.get("schema") != BINDING_SCHEMA:
        raise ReaderGateError("unexpected V1.x binding schema")
    if binding.get("statistical_admission_decided") is not False or binding.get("source_admission_decided") is not False:
        raise ReaderGateError("binding claims admission")

    draft_pin = _pin(binding.get("draft_v2"), "draft_v2")
    if draft_pin["sha256"] == HISTORICAL_V1_SHA256:
        raise ReaderGateError("historical V1 cannot serve as V1.x")
    draft_path = _relocated_path(draft_pin["path"], bundle_root, "ORDEM_019/F3.1")
    # Read the draft exactly once: the same bytes yield the pin, spec, and return snapshot.
    draft, draft_raw = base._read_json(draft_path)
    if len(draft_raw) != draft_pin["bytes"] or base._digest(draft_raw) != draft_pin["sha256"]:
        raise ReaderGateError("V2 draft bytes/hash mismatch")
    if draft_pin["sha256"] != E1_DRAFT_SHA256:
        raise ReaderGateError("F3.1.E1 projection pin differs")
    if draft.get("state") != R52_STATE:
        raise ReaderGateError("V2 draft state is not the expected non-frozen state")
    if draft.get("derived_from", {}).get("sha256") != R52_DRAFT_SHA256:
        raise ReaderGateError("F3.1.E1 projection parent pin differs")
    decision = _object(binding.get("f34_decision"), "F3.4 decision")
    if decision != {"quadro_event": 462, "resolution_sha256": F34_RESOLUTION_SHA256,
                    "scalar_original_r4_sha256": ORIGINAL_R4_SHA256,
                    "scalar_projection_sha256": F34_DRAFT_SHA256,
                    "joint_witness_separate": True, "no_pooling": True, "opening": False}:
        raise ReaderGateError("F3.4 decision binding differs")
    if binding.get("r52_lineage") != {"f34_sha256": F34_DRAFT_SHA256,
            "r5_sha256": R5_SHA256, "r51_sha256": R51_SHA256,
            "r52_sha256": R52_DRAFT_SHA256, "r52_spec_sha256": R52_SPEC_SHA256,
            "r52_function_sha256": R52_FUNCTION_SHA256}:
        raise ReaderGateError("R5.2 lineage binding differs")
    if binding.get("e1_projection") != {
            "parent_sha256": R52_DRAFT_SHA256,
            "projection_sha256": E1_DRAFT_SHA256,
            "spec_sha256": E1_SPEC_SHA256,
            "function_sha256": R52_FUNCTION_SHA256,
            "freeze": False, "opening": False}:
        raise ReaderGateError("F3.1.E1 projection binding differs")
    ancestor_receipt = _verify_ancestor_bytes(binding, draft_pin, draft, draft_raw, bundle_root)
    spec = _object(draft.get("spec"), "draft spec")
    witness = _object(spec.get("f34_duas_testemunhas"), "F3.4 witness")
    if (witness.get("quadro_f34") != {"status": "FECHADA", "evento": 462}
            or witness.get("congelamento") is not False or witness.get("abertura") is not False
            or witness.get("fonte_ratificacao", {}).get("sha256") != F34_RESOLUTION_SHA256
            or any(str(x).startswith("F3.4 ") for x in spec.get("pending_operator_decisions", []))):
        raise ReaderGateError("F3.4 witness contract differs")
    spec_raw = json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    spec_sha256 = hashlib.sha256(spec_raw).hexdigest()
    if draft.get("spec_sha256") != spec_sha256 or binding.get("spec_sha256") != spec_sha256:
        raise ReaderGateError("V2 spec hash mismatch")
    if spec_sha256 != E1_SPEC_SHA256:
        raise ReaderGateError("F3.1.E1 spec pin differs")
    if expected_spec_sha256 is not None and expected_spec_sha256 != spec_sha256:
        raise ReaderGateError("independent V2 spec pin mismatch")
    verdict_record = _object(spec.get("funcao_de_veredito"), "draft verdict function")
    source = _text(verdict_record.get("fonte"), "draft verdict source")
    if (verdict_record.get("nome") != "veredito_fase9_v2_r5_2_proposta"
            or verdict_record.get("sha256") != R52_FUNCTION_SHA256
            or hashlib.sha256(source.encode("utf-8")).hexdigest() != R52_FUNCTION_SHA256):
        raise ReaderGateError("R5.2 verdict function pin differs")
    readers = _object(spec.get("leitores"), "draft readers")
    if set(readers) != EXPECTED_READER_IDS:
        raise ReaderGateError("V2 reader ids differ")
    families = _object(spec.get("familias"), "draft families")
    primary = _object(families.get("P_primaria"), "primary family")
    primary_ids = primary.get("ids")
    if not isinstance(primary_ids, list) or not all(isinstance(item, str) for item in primary_ids):
        raise ReaderGateError("V2 primary family ids malformed")
    if set(primary_ids) != PRIMARY_READER_IDS or len(primary_ids) != 5:
        raise ReaderGateError("V2 primary family must use five distinct readers")

    records = binding.get("readers")
    if not isinstance(records, list) or len(records) != len(EXPECTED_READER_IDS):
        raise ReaderGateError("binding reader list incomplete")
    ids = [_text(_object(record, "reader").get("reader_id"), "reader_id") for record in records]
    if len(set(ids)) != len(ids) or set(ids) != EXPECTED_READER_IDS:
        raise ReaderGateError("reader ids incomplete, duplicated or unexpected")

    root = base._resolve_existing(allowed_source_root)
    if root != base._resolve_existing(bundle_root / "ORDEM_018"):
        raise ReaderGateError("source root differs from relocated ORDEM_018")
    verified = {}
    for record in records:
        reader_id = record["reader_id"]
        expected = _object(readers[reader_id], f"{reader_id}.draft_metadata")
        if record.get("draft_metadata") != expected:
            raise ReaderGateError(f"draft metadata changed: {reader_id}")
        h0 = _number(record.get("H0_published"), f"{reader_id}.H0")
        components = record.get("sigma_published_components")
        if not isinstance(components, list) or not components:
            raise ReaderGateError(f"sigma components missing: {reader_id}")
        parts = [_number(x, f"{reader_id}.sigma_component", positive=True) for x in components]
        transform = _text(record.get("local_transform"), f"{reader_id}.local_transform")
        try:
            sigma = base._reconstruct_sigma(record)
        except (KeyError, TypeError, ValueError, OverflowError) as exc:
            raise ReaderGateError(f"invalid sigma transform: {reader_id}") from exc
        if not math.isclose(h0, _number(expected.get("H0"), f"{reader_id}.draft_H0"), abs_tol=1e-12, rel_tol=0):
            raise ReaderGateError(f"H0 transcription mismatch: {reader_id}")
        if not math.isclose(sigma, _number(expected.get("sigma"), f"{reader_id}.draft_sigma", positive=True), abs_tol=1e-12, rel_tol=0):
            raise ReaderGateError(f"sigma transcription mismatch: {reader_id}")
        asymmetric = record.get("asymmetric_sigma")
        if transform == "arithmetic_mean":
            asymmetric = _object(asymmetric, f"{reader_id}.asymmetric_sigma")
            if len(parts) != 2 or asymmetric.get("plus") != parts[0] or asymmetric.get("minus") != parts[1]:
                raise ReaderGateError(f"asymmetric sigma sides changed: {reader_id}")
            if ("sigma_plus" in expected or "sigma_minus" in expected) and (expected.get("sigma_plus") != parts[0] or expected.get("sigma_minus") != parts[1]):
                raise ReaderGateError(f"asymmetric sides disagree with draft metadata: {reader_id}")
        elif asymmetric is not None:
            raise ReaderGateError(f"unexpected asymmetric sigma: {reader_id}")

        status = record.get("documentary_status")
        if status == "DECLARADO_UNVERIFIED" and reader_id in DECLARED_ONLY_IDS:
            if record.get("source") is not None or record.get("numeric_windows") is not None:
                raise ReaderGateError(f"unverified reader claims source evidence: {reader_id}")
            verified[reader_id] = {
                "status": status, "source_sha256": None,
                "sigma_compression": transform, "asymmetric_sigma": asymmetric,
                "statistical_admission": "OPEN",
            }
            continue
        if status != "REAL_DOCUMENTARY_HASH_ONLY":
            raise ReaderGateError(f"reader documentary status invalid: {reader_id}")
        source, source_text = _source_text(record, reader_id, root, bundle_root)
        windows = _object(record.get("numeric_windows"), f"{reader_id}.numeric_windows")
        if reader_id in MASER_READER_IDS:
            table_literal = MASER_TABLE_LITERALS[reader_id]
            h0_window = _object(windows.get("H0"), f"{reader_id}.H0_window")
            if h0_window.get("literal") != table_literal:
                raise ReaderGateError(f"maser Table 2 row missing: {reader_id}")
        _window(windows.get("H0"), h0, source_text, f"{reader_id}.H0_window")
        if transform == "arithmetic_mean":
            _signed_source_sides(windows, h0, parts[0], parts[1], reader_id)
        sigma_windows = windows.get("sigma_components")
        if not isinstance(sigma_windows, list) or len(sigma_windows) != len(parts):
            raise ReaderGateError(f"sigma source windows incomplete: {reader_id}")
        for index, (window, part) in enumerate(zip(sigma_windows, parts)):
            if reader_id in MASER_READER_IDS and _object(window, f"{reader_id}.sigma_window_{index}").get("literal") != MASER_TABLE_LITERALS[reader_id]:
                raise ReaderGateError(f"maser Table 2 sigma row missing: {reader_id}")
            _window(window, part, source_text, f"{reader_id}.sigma_window_{index}")
            if reader_id == "L2_cchp" and index == 1:
                context = _object(window, f"{reader_id}.sigma_window_{index}")["literal"]
                if not all(token in context for token in ("TRGB", "H_0", "(sys)")):
                    raise ReaderGateError("CCHP 1.33 source window lacks sys/TRGB context")
        verified[reader_id] = {
            "status": status, "source_sha256": base._digest(source),
            "sigma_compression": transform, "asymmetric_sigma": asymmetric,
            "statistical_admission": "OPEN",
        }
    if any(verified[reader_id]["status"] != "REAL_DOCUMENTARY_HASH_ONLY" for reader_id in PRIMARY_READER_IDS):
        raise ReaderGateError("a primary reader lacks documentary hash verification")
    return {
        "binding_sha256": base._digest(binding_raw),
        "draft_v2_sha256": base._digest(draft_raw),
        "ancestor_bytes_rechecked": ancestor_receipt,
        "projection": "F3.1.E1",
        "spec_sha256": spec_sha256,
        "spec_snapshot": copy.deepcopy(spec),
        "verified_readers": verified,
        "statistical_admission": "OPEN",
        "source_admission": "OPEN",
        "cross_covariance": "OPEN",
        "v2_frozen": False,
    }


verify_readers = verify_v1x_binding
