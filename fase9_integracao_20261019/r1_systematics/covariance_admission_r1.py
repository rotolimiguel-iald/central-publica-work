"""Candidate matrix coverage contract; no data reader, fit or physical admission.

The caller pins the reviewed catalog. Hashes certify byte identity, not a model's
adequacy. Complete *declared* coverage is not proof of complete physical coverage.
Published/inferred bounds admit one conditional matrix, never all matrices in a
box. There is no silent zero, covariance clipping, jitter or implicit map.
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
from pathlib import Path


class AdmissionError(ValueError):
    pass


HERE = Path(__file__).resolve().parent


def _read_pin(path, digest):
    raw = Path(path).read_bytes()
    if type(digest) is not str or hashlib.sha256(raw).hexdigest() != digest:
        raise AdmissionError("PIN_MISMATCH")
    return raw


def _definitions(raw, names, scope):
    tree = ast.parse(raw.decode("utf-8-sig"))
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))
             and n.name in names]
    if {n.name for n in nodes} != set(names):
        raise AdmissionError("REUSED_DEFINITION_MISSING")
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "pinned_pure_reuse", "exec"), scope)
    return scope


def _reuse():
    pins = json.loads((HERE / "REUSE_PINS_R1.json").read_text(encoding="utf-8"))
    jp, sp = pins["joint_builder"], pins["scalar_runner"]
    joint = _definitions(_read_pin(jp["path"], jp["sha256"]),
                         ["CovarianceError", "_require", "_keys"], {})
    scalar = _definitions(_read_pin(sp["path"], sp["sha256"]), ["_cholesky"],
                          {"math": math, "ReaderGateError": AdmissionError})
    return joint, scalar["_cholesky"]


_JOINT, _CHOLESKY = _reuse()


def _keys(obj, names, label):
    try:
        _JOINT["_keys"](obj, names, label)
    except _JOINT["CovarianceError"] as exc:
        raise AdmissionError(str(exc)) from exc


def _number(value, label):
    if type(value) not in (int, float):
        raise AdmissionError("NONNUMERIC_OR_BOOL:" + label)
    try:
        x = float(value)
    except (ValueError, OverflowError) as exc:
        raise AdmissionError("NUMERIC_RANGE:" + label) from exc
    if not math.isfinite(x):
        raise AdmissionError("NONFINITE:" + label)
    return x


def _pair(a, b):
    return "|".join(sorted((a, b)))


def load_catalog(path, digest):
    raw = _read_pin(path, digest)
    try:
        catalog = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise AdmissionError("CATALOG_JSON") from exc
    if catalog.get("schema") != "F9_SYSTEMATICS_CATALOG_R1":
        raise AdmissionError("CATALOG_SCHEMA")
    for pin in catalog["sources"].values():
        _read_pin(pin["path"], pin["sha256"])
    return catalog


def _references(rec, catalog):
    refs = rec.get("references")
    if type(refs) is not list or not refs:
        raise AdmissionError("MISSING_DOCUMENTARY_REFERENCE")
    for ref in refs:
        _keys(ref, ("source_id", "line_start", "line_end"), "reference")
        if (ref["source_id"] not in catalog["sources"] or
                type(ref["line_start"]) is not int or type(ref["line_end"]) is not int or
                ref["line_start"] < 1 or ref["line_end"] < ref["line_start"]):
            raise AdmissionError("INVALID_DOCUMENTARY_REFERENCE")


def unresolved(catalog, family):
    """Documentary missing-input inventory, not a matrix admission."""
    ids = catalog["families"][family]
    result = []
    for i, a in enumerate(ids):
        m = catalog["observable_maps"].get(a)
        if not m or m["status"] == "OPEN":
            result.append("MAP:" + a)
        for b in ids[i + 1:]:
            p = _pair(a, b)
            if p not in catalog["pairs"]:
                result.append("PAIR:" + p)
                continue
            for c, rec in catalog["pairs"][p]["components"].items():
                if rec["status"] == "OPEN" or rec.get("interval") is None:
                    result.append("COMPONENT:" + p + ":" + c)
    return result


def admit_covariance(request, *, catalog_path, catalog_sha256):
    """Qualify an explicit candidate matrix. Never emits a physical/run permit.

    Synthetic mode accepts only synthetic maps/components. Conditional mode
    requires non-synthetic documented maps plus explicit published/inferred/zero
    component bounds. OPEN components always refuse, including explicit zeros.
    """
    _keys(request, ("mode", "family", "reader_ids", "matrix", "unit", "pairs"), "request")
    mode = request["mode"]
    if mode not in ("SYNTHETIC_QUALIFICATION", "CONDITIONAL_MATRIX_ONLY"):
        raise AdmissionError("PHYSICAL_OR_OBSERVED_ADMISSION_NOT_IMPLEMENTED")
    catalog = load_catalog(catalog_path, catalog_sha256)
    family = request["family"]
    if type(family) is not str or family not in catalog["families"]:
        raise AdmissionError("UNKNOWN_FAMILY")
    ids = request["reader_ids"]
    if (type(ids) is not list or not ids or any(type(i) is not str for i in ids)
            or len(set(ids)) != len(ids) or ids != catalog["families"][family]):
        raise AdmissionError("READER_ID_OR_ORDER_MISMATCH")
    if request["unit"] != catalog["covariance_unit"]:
        raise AdmissionError("UNIT_MISMATCH")
    expected = [_pair(a, b) for i, a in enumerate(ids) for b in ids[i + 1:]]
    _keys(request["pairs"], expected, "ALL_EXPLICIT_PAIRS_REQUIRED")
    missing = unresolved(catalog, family)
    if missing:
        raise AdmissionError("OPEN_COVERAGE:" + ";".join(missing))
    for a in ids:
        rec = catalog["observable_maps"][a]
        allowed = ("SYNTHETIC_MAP",) if mode == "SYNTHETIC_QUALIFICATION" else ("DERIVED_MAP_WITH_SCOPE",)
        if rec["status"] not in allowed or not rec.get("references"):
            raise AdmissionError("MAP_NOT_QUALIFIED:" + a)
        _references(rec, catalog)
    n = len(ids)
    raw = request["matrix"]
    if type(raw) is not list or len(raw) != n or any(type(row) is not list or len(row) != n for row in raw):
        raise AdmissionError("MATRIX_SHAPE")
    c = [[_number(v, f"matrix[{i},{j}]") for j, v in enumerate(row)] for i, row in enumerate(raw)]
    if any(c[i][i] <= 0 for i in range(n)):
        raise AdmissionError("DIAGONAL_NONPOSITIVE")
    for i in range(n):
        for j in range(i):
            if c[i][j] != c[j][i]:
                raise AdmissionError("NONSYMMETRIC_NO_AUTOREPAIR")
            key = _pair(ids[i], ids[j])
            components = catalog["pairs"][key]["components"]
            _keys(request["pairs"][key], components.keys(), "ALL_EXPLICIT_COMPONENTS_REQUIRED:" + key)
            contributions = []
            for name, rec in components.items():
                allowed = ("SYNTHETIC_INPUT",) if mode == "SYNTHETIC_QUALIFICATION" else ("PUBLISHED_BOUND", "INFERRED_BOUND", "STRUCTURAL_ZERO")
                if rec["status"] not in allowed or not rec.get("references"):
                    raise AdmissionError("COMPONENT_STATUS:" + key + ":" + name)
                _references(rec, catalog)
                interval = rec["interval"]
                if type(interval) is not list or len(interval) != 2:
                    raise AdmissionError("INTERVAL_SCHEMA")
                lo, hi = [_number(v, "bound") for v in interval]
                value = _number(request["pairs"][key][name], "component")
                if lo > hi or not lo <= value <= hi:
                    raise AdmissionError("OUTSIDE_DECLARED_BOUND")
                if lo == hi == 0 and not rec.get("zero_reason"):
                    raise AdmissionError("ZERO_WITHOUT_EXPLICIT_REASON")
                contributions.append(value)
            try:
                total = math.fsum(contributions)
            except (OverflowError, ValueError) as exc:
                raise AdmissionError("COMPONENT_SUM_RANGE") from exc
            if not math.isfinite(total) or not math.isclose(total, c[i][j], rel_tol=1e-12, abs_tol=1e-12):
                raise AdmissionError("COMPONENTS_DO_NOT_RECONSTRUCT_MATRIX")
    try:
        scale = [math.sqrt(c[i][i]) for i in range(n)]
        correlation = [[c[i][j] / scale[i] / scale[j] for j in range(n)] for i in range(n)]
        if any(not math.isfinite(v) for row in correlation for v in row):
            raise AdmissionError("NORMALIZATION_RANGE")
        lower = _CHOLESKY(correlation)
        if any(not math.isfinite(v) for row in lower for v in row):
            raise AdmissionError("CHOLESKY_NONFINITE")
    except (OverflowError, ZeroDivisionError) as exc:
        raise AdmissionError("NUMERIC_RANGE") from exc
    # The reused solver admits strictly positive pivots >1e-12. Singular PSD
    # matrices are refused; no unsupported singular-likelihood normalization.
    return {"status": "SYNTHETIC_MATRIX_QUALIFIED" if mode == "SYNTHETIC_QUALIFICATION" else "CONDITIONAL_MATRIX_QUALIFIED_NOT_PHYSICAL_ADMISSION",
            "catalog_sha256": catalog_sha256,
            "matrix_sha256": hashlib.sha256(json.dumps(c, separators=(",", ":"), allow_nan=False).encode()).hexdigest(),
            "reader_ids": ids, "unit": request["unit"], "pairs_checked": len(expected),
            "positive_definite_under_pivot_policy": True, "singular_psd_supported": False,
            "physical_admission": False, "robust_over_covariance_box": False,
            "observed_data_opened": False, "gate_changed": False}
