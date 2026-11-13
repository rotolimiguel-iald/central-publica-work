"""Etapa 1: montagem documental raw_MAS e teste SOMENTE sintético R22.

Sem --fixture, qualquer produção é recusada antes da leitura de tabela externa
se o manifesto estiver incompleto, se precisão/quantização/tolerâncias não
estiverem documentadas ou se a Etapa 2 não estiver autorizada.

Não lê y_obs nem saídas observadas; não chama solver/evaluate; não calcula
D/H0/razão; não usa RNG, projeção, jitter, FREEZE_R2 ou v410.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
WORK09 = ROOT.parents[1]
ORDER04 = WORK09 / "ORDEM_KIMI_H0DN_04_11nov.md"
A1_DOC = ROOT.parent / "ordem03B" / "A1_HIPOTESES_DO_VETOR.md"
PROTOCOL_DOC = ROOT.parent / "ordem03B" / "PROTOCOLO_CONFERENCIA_FUTURA.md"
OUTPUT = ROOT / "VALIDACAO_FIXTURES.json"
NUMERIC_TOLERANCE = 1.0e-12
HOSTS = [
    "N7250", "N4536", "N3972", "N4424", "N4639", "N4038", "M101",
    "N2442", "N1365", "N5643", "N5584", "N1559", "N5468", "N1448",
    "N2525", "N3370", "N5861", "N3147", "N3021", "N1309", "N3982",
    "N1015", "N3447", "N5917", "U9391", "N3583", "N2608", "N7541",
    "N0691", "N3254", "N5728", "N7678", "M1337", "N4680", "N7329",
    "N0976", "N0105",
]
ANCHORS = ["N4258", "LMC", "MW"]
SELF_REFERENCE_HOSTS = {"N4258", "LMC", "MW", "SMC", "M31", "ALL"}
EXCLUDED_HOSTS = {"N4151"}
OFFSETS = {"N4258": 0.31, "LMC": -0.17, "MW": 0.23}
REF_ERRORS = {"N4258": 0.011, "LMC": 0.012, "MW": 0.013}
GEOMETRIC_ERRORS = {"N4258": 0.021, "LMC": 0.022, "MW": 0.023}
THETA_HOST = {host: 10.0 + 0.01 * k for k, host in enumerate(HOSTS)}
VARIANT_ID = "H0DN_PUBLICADO_REDUZIDO_183__EXTRA13_OUT__raw_MAS"


class ProductionRefused(RuntimeError):
    """A deliberate, pre-read production stop."""


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def parse_host_table_lines(text: str) -> list[dict]:
    """Explicit seven-column parser; no pandas inference and no data files."""
    records = []
    for line_number, original in enumerate(text.splitlines(), 1):
        cleaned = re.split(r"[#;]", original, maxsplit=1)[0].strip()
        if not cleaned or cleaned.lower().startswith("host "):
            continue
        fields = cleaned.split()
        if len(fields) != 7:
            raise ValueError(f"TABLE_PARSE_ERROR line={line_number}: expected 7 fields, got {len(fields)}")
        host, mu_text, error_text, method, anchor, source, pgc = fields
        try:
            mu_host = float(mu_text)
            mu_error = float(error_text)
        except ValueError as exc:
            raise ValueError(f"TABLE_PARSE_ERROR line={line_number}: nonnumeric center/error") from exc
        if not np.isfinite(mu_host) or not np.isfinite(mu_error) or mu_error < 0:
            raise ValueError(f"TABLE_PARSE_ERROR line={line_number}: invalid center/error")
        records.append({
            "host": host,
            "mu_host": mu_host,
            "mu_error": mu_error,
            "method": method,
            "anchor": anchor,
            "source": source,
            "PGC": pgc,
            "mu_host_lexeme": mu_text,
            "mu_error_lexeme": error_text,
            "source_line": line_number,
        })
    if not records:
        raise ValueError("TABLE_PARSE_ERROR: no data rows")
    return records


def select_r22_rows(records: list[dict]) -> tuple[list[dict], list[dict], dict]:
    """Select exactly 37 hosts x 3 anchors, with explicit exclusions."""
    references = []
    candidates = []
    counts = {
        "excluded_N4151_rows": 0,
        "excluded_MAS_self_reference_rows": 0,
        "excluded_other_method_source_or_anchor_rows": 0,
    }
    for row in records:
        if row["host"] in EXCLUDED_HOSTS:
            counts["excluded_N4151_rows"] += 1
            continue
        if row["host"] in SELF_REFERENCE_HOSTS:
            references.append(row)
            counts["excluded_MAS_self_reference_rows"] += 1
            continue
        if row["method"] != "ceph_hst" or row["source"] != "R22" or row["anchor"] not in ANCHORS:
            counts["excluded_other_method_source_or_anchor_rows"] += 1
            continue
        candidates.append(row)

    lookup = {}
    for row in candidates:
        key = (row["host"], row["anchor"])
        if key in lookup:
            raise ValueError(f"ROW_MAP_ERROR: duplicate {key}")
        lookup[key] = row
    expected = {(host, anchor) for anchor in ANCHORS for host in HOSTS}
    if set(lookup) != expected:
        missing = sorted(expected - set(lookup))
        extra = sorted(set(lookup) - expected)
        raise ValueError(f"ROW_MAP_ERROR: missing={missing}, extra={extra}")
    canonical = [lookup[(host, anchor)] for anchor in ANCHORS for host in HOSTS]
    assert len(canonical) == 111
    return canonical, references, counts


def build_r22_host_block(rows: list[dict], references: list[dict], anchor_errors: dict) -> dict:
    """Build A,C,y without adding or subtracting mas_ref_value."""
    n = len(rows)
    host_index = {host: i for i, host in enumerate(HOSTS)}
    A = np.zeros((n, len(HOSTS)), dtype=float)
    y = np.zeros(n, dtype=float)
    C = np.zeros((n, n), dtype=float)
    for i, row in enumerate(rows):
        A[i, host_index[row["host"]]] = 1.0
        # raw_MAS: the table center is copied exactly; no MAS-center arithmetic.
        y[i] = float(row["mu_host_lexeme"])
        C[i, i] = row["mu_error"] ** 2

    ref_error_by_mas = {}
    for ref in references:
        if ref["method"] == "ceph_hst" and ref["source"] == "R22" and ref["anchor"] in ANCHORS:
            key = f"{ref['method']}&{ref['anchor']}&{ref['source']}"
            if key in ref_error_by_mas:
                raise ValueError(f"MAS_REFERENCE_ERROR: duplicate {key}")
            ref_error_by_mas[key] = ref["mu_error"]
    expected_mas = {f"ceph_hst&{anchor}&R22" for anchor in ANCHORS}
    if set(ref_error_by_mas) != expected_mas:
        raise ValueError("MAS_REFERENCE_ERROR: expected exactly one R22 reference per anchor")

    hms_error = {}
    for row in rows:
        hms = f"{row['host']}&{row['method']}&{row['source']}"
        hms_error[hms] = min(row["mu_error"], hms_error.get(hms, row["mu_error"]))
    for i, row_i in enumerate(rows):
        mas_i = f"{row_i['method']}&{row_i['anchor']}&{row_i['source']}"
        hms_i = f"{row_i['host']}&{row_i['method']}&{row_i['source']}"
        for j, row_j in enumerate(rows):
            if row_i["anchor"] == row_j["anchor"]:
                C[i, j] += float(anchor_errors[row_i["anchor"]]) ** 2
            mas_j = f"{row_j['method']}&{row_j['anchor']}&{row_j['source']}"
            if mas_i == mas_j:
                C[i, j] += ref_error_by_mas[mas_i] ** 2
            hms_j = f"{row_j['host']}&{row_j['method']}&{row_j['source']}"
            if i != j and hms_i == hms_j:
                # Public rule: minimum group error, off-diagonal only; the
                # diagonal is already present in each row's own mu_error.
                C[i, j] += hms_error[hms_i] ** 2
    return {"A": A, "C": C, "y": y, "rows": rows, "references": references}


def second_difference_matrix(rows: list[dict]) -> tuple[np.ndarray, list[dict]]:
    lookup = {(row["host"], row["anchor"]): i for i, row in enumerate(rows)}
    vectors = []
    metadata = []
    identity_id = 0
    for k in range(1, len(HOSTS)):
        for other, pair in [("LMC", "N4258-LMC"), ("MW", "N4258-MW")]:
            identity_id += 1
            indices = [
                lookup[(HOSTS[k], "N4258")], lookup[(HOSTS[k], other)],
                lookup[(HOSTS[0], "N4258")], lookup[(HOSTS[0], other)],
            ]
            vector = np.zeros(len(rows), dtype=float)
            vector[indices] = [1.0, -1.0, -1.0, 1.0]
            vectors.append(vector)
            metadata.append({
                "identity_id": identity_id,
                "k": k,
                "host": HOSTS[k],
                "reference_host": HOSTS[0],
                "pair": pair,
                "row_indices_zero_based": indices,
                "coefficients": [1, -1, -1, 1],
            })
    return np.asarray(vectors), metadata


def synthetic_table() -> str:
    lines = ["host mu_host mu_error method anchor source PGC"]
    for i, anchor in enumerate(ANCHORS):
        lines.append(
            f"{anchor} {OFFSETS[anchor]:.17g} {REF_ERRORS[anchor]:.17g} "
            f"ceph_hst {anchor} R22 {800000 + i} # synthetic MAS self-reference"
        )
    for anchor in ANCHORS:
        for k, host in enumerate(HOSTS):
            center = THETA_HOST[host] + OFFSETS[anchor]
            error = 0.04 + 0.0005 * k
            lines.append(
                f"{host} {center:.17g} {error:.17g} ceph_hst {anchor} R22 {900000 + k}"
            )
        # Deliberate distractor proving that N4151 is excluded, never renamed.
        lines.append(f"N4151 {90.0 + OFFSETS[anchor]:.17g} 0.09 ceph_hst {anchor} R22 999999")
    return "\n".join(lines) + "\n"


def manifest_for_guard_unit_test() -> dict:
    """In-memory synthetic guard input; never written as MANIFESTO."""
    return {
        "variant_id": VARIANT_ID,
        "center_convention": "raw_MAS",
        "reference_host": "N7250",
        "anchor_order": ANCHORS,
        "host_order": HOSTS,
        "source_fits_and_versions": ["SYNTHETIC_ONLY"],
        "row_map_path_and_sha256": "synthetic://" + "0" * 64,
        "code_sha256": "0" * 64,
        "protocol_sha256": "0" * 64,
        "route_name": "synthetic.guard.only",
        "route_sequence_number": 0,
        "cell_precision": {
            f"{host}|{anchor}": {"least_significant_unit": 0.0}
            for anchor in ANCHORS for host in HOSTS
        },
        "quantization_rule": "SYNTHETIC_EXACT_DECIMAL_NO_ROUNDING",
        "identity_tolerances": [NUMERIC_TOLERANCE] * 72,
        "numeric_tolerance": NUMERIC_TOLERANCE,
        "covariance_public": {"geometric_anchor_errors": GEOMETRIC_ERRORS},
        "stage2_authorized": True,
    }


def validate_production_manifest(manifest: dict) -> dict:
    """Validate everything before any external table is opened."""
    if not isinstance(manifest, dict):
        raise ProductionRefused("MANIFESTO_INCOMPLETE")
    required = [
        "variant_id", "center_convention", "reference_host", "anchor_order", "host_order",
        "source_fits_and_versions", "row_map_path_and_sha256", "code_sha256",
        "protocol_sha256", "route_name", "route_sequence_number", "cell_precision",
        "quantization_rule", "identity_tolerances", "numeric_tolerance", "covariance_public",
        "stage2_authorized",
    ]
    if any(key not in manifest for key in required):
        raise ProductionRefused("MANIFESTO_INCOMPLETE")
    if manifest["center_convention"] != "raw_MAS":
        raise ProductionRefused("CENTER_CONVENTION_NOT_RAW_MAS")
    if manifest["reference_host"] != "N7250" or manifest["anchor_order"] != ANCHORS or manifest["host_order"] != HOSTS:
        raise ProductionRefused("MANIFESTO_ROW_MAP_MISMATCH")
    expected_cells = {f"{host}|{anchor}" for anchor in ANCHORS for host in HOSTS}
    precision = manifest["cell_precision"]
    if not isinstance(precision, dict) or set(precision) != expected_cells:
        raise ProductionRefused("PRECISION_NOT_DOCUMENTED")
    for cell in precision.values():
        if not isinstance(cell, dict) or "least_significant_unit" not in cell:
            raise ProductionRefused("PRECISION_NOT_DOCUMENTED")
        try:
            quantum = float(cell["least_significant_unit"])
        except (TypeError, ValueError) as exc:
            raise ProductionRefused("PRECISION_NOT_DOCUMENTED") from exc
        if not np.isfinite(quantum) or quantum < 0:
            raise ProductionRefused("PRECISION_NOT_DOCUMENTED")
    quantization = manifest["quantization_rule"]
    if not isinstance(quantization, str) or not quantization.strip() or quantization.strip().upper() in {"OPEN", "UNKNOWN", "TBD"}:
        raise ProductionRefused("QUANTIZATION_NOT_DOCUMENTED")
    tolerances = manifest["identity_tolerances"]
    if not isinstance(tolerances, list) or len(tolerances) != 72:
        raise ProductionRefused("TOLERANCES_NOT_DOCUMENTED")
    try:
        numeric_tolerances = np.asarray(tolerances, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ProductionRefused("TOLERANCES_NOT_DOCUMENTED") from exc
    if not np.isfinite(numeric_tolerances).all() or (numeric_tolerances < 0).any():
        raise ProductionRefused("TOLERANCES_NOT_DOCUMENTED")
    if float(manifest["numeric_tolerance"]) != NUMERIC_TOLERANCE:
        raise ProductionRefused("NUMERIC_TOLERANCE_MISMATCH")
    errors = manifest["covariance_public"].get("geometric_anchor_errors")
    if not isinstance(errors, dict) or set(errors) != set(ANCHORS):
        raise ProductionRefused("PUBLIC_COVARIANCE_INPUT_INCOMPLETE")
    if any(not np.isfinite(float(errors[a])) or float(errors[a]) < 0 for a in ANCHORS):
        raise ProductionRefused("PUBLIC_COVARIANCE_INPUT_INCOMPLETE")
    if manifest["stage2_authorized"] is not True:
        raise ProductionRefused("STAGE2_NOT_AUTHORIZED")
    return manifest


def guard_unit_tests() -> dict:
    results = {}
    try:
        validate_production_manifest({})
        results["incomplete_manifest_refused"] = False
    except ProductionRefused as exc:
        results["incomplete_manifest_refused"] = str(exc) == "MANIFESTO_INCOMPLETE"
    missing_quantization = manifest_for_guard_unit_test()
    del missing_quantization["quantization_rule"]
    try:
        validate_production_manifest(missing_quantization)
        results["missing_quantization_refused"] = False
    except ProductionRefused as exc:
        results["missing_quantization_refused"] = str(exc) == "MANIFESTO_INCOMPLETE"
    undocumented_quantization = manifest_for_guard_unit_test()
    undocumented_quantization["quantization_rule"] = "OPEN"
    try:
        validate_production_manifest(undocumented_quantization)
        results["open_quantization_refused"] = False
    except ProductionRefused as exc:
        results["open_quantization_refused"] = str(exc) == "QUANTIZATION_NOT_DOCUMENTED"
    missing_tolerances = manifest_for_guard_unit_test()
    missing_tolerances["identity_tolerances"] = []
    try:
        validate_production_manifest(missing_tolerances)
        results["undocumented_tolerances_refused"] = False
    except ProductionRefused as exc:
        results["undocumented_tolerances_refused"] = str(exc) == "TOLERANCES_NOT_DOCUMENTED"
    stage2_closed = manifest_for_guard_unit_test()
    stage2_closed["stage2_authorized"] = False
    try:
        validate_production_manifest(stage2_closed)
        results["stage2_false_refused"] = False
    except ProductionRefused as exc:
        results["stage2_false_refused"] = str(exc) == "STAGE2_NOT_AUTHORIZED"
    return results


def run_fixture() -> dict:
    table_text = synthetic_table()
    parsed = parse_host_table_lines(table_text)
    rows, references, exclusions = select_r22_rows(parsed)
    model = build_r22_host_block(rows, references, GEOMETRIC_ERRORS)
    A, C, y = model["A"], model["C"], model["y"]
    B, identity_metadata = second_difference_matrix(rows)
    theta = np.asarray([THETA_HOST[host] for host in HOSTS], dtype=float)
    y_theta = A @ theta
    O = np.asarray([OFFSETS[row["anchor"]] for row in rows], dtype=float)
    expected_raw = y_theta + O
    residual_raw = B @ y
    residual_theta = B @ y_theta
    rank_C = int(np.linalg.matrix_rank(C, tol=1.0e-10))
    rank_B = int(np.linalg.matrix_rank(B, tol=1.0e-12))
    raw_center_max_error = float(np.max(np.abs(y - np.asarray([r["mu_host"] for r in rows]))))
    raw_generative_max_error = float(np.max(np.abs(y - expected_raw)))
    max_raw = float(np.max(np.abs(residual_raw)))
    max_theta = float(np.max(np.abs(residual_theta)))
    max_BA = float(np.max(np.abs(B @ A)))
    max_BCB = float(np.max(np.abs(B @ C @ B.T)))
    lookup = {(row["host"], row["anchor"]): i for i, row in enumerate(rows)}
    separations = []
    for host in HOSTS:
        separations.extend([
            abs(y[lookup[(host, "N4258")]] - y[lookup[(host, "LMC")]]),
            abs(y[lookup[(host, "N4258")]] - y[lookup[(host, "MW")]]),
            abs(y[lookup[(host, "LMC")]] - y[lookup[(host, "MW")]]),
        ])
    minimum_separation = float(min(separations))
    recovered_offsets = {
        ref["anchor"]: ref["mu_host"] for ref in references
        if ref["method"] == "ceph_hst" and ref["source"] == "R22" and ref["anchor"] in ANCHORS
    }
    checks = {
        "exact_37_hosts_x_3_anchors": len(rows) == 111 and len({r["host"] for r in rows}) == 37,
        "N4151_excluded": exclusions["excluded_N4151_rows"] == 3,
        "MAS_self_references_excluded_from_hosts": exclusions["excluded_MAS_self_reference_rows"] == 3,
        "raw_centers_copied_without_MAS_arithmetic": raw_center_max_error == 0.0,
        "raw_generative_equation_pass": raw_generative_max_error <= NUMERIC_TOLERANCE,
        "all_72_raw_second_differences_pass": max_raw <= NUMERIC_TOLERANCE,
        "all_72_A_theta_identities_pass": max_theta <= NUMERIC_TOLERANCE,
        "constraint_rank_72_pass": rank_B == 72,
        "R22_covariance_rank_39_pass": rank_C == 39,
        "R22_covariance_nullity_72_pass": 111 - rank_C == 72,
        "BA_zero_pass": max_BA <= NUMERIC_TOLERANCE,
        "BCBT_zero_pass": max_BCB <= NUMERIC_TOLERANCE,
        "MAS_offsets_nonzero": all(OFFSETS[a] != 0 for a in ANCHORS) and recovered_offsets == OFFSETS,
        "triplets_not_forced_equal": minimum_separation > 0.0,
        "no_projection_or_jitter": True,
    }
    guards = guard_unit_tests()
    checks.update(guards)
    passed = all(checks.values())
    identity_results = []
    for meta, raw, synthetic in zip(identity_metadata, residual_raw, residual_theta):
        identity_results.append({
            **meta,
            "residual_raw_mag": float(raw),
            "residual_A_theta_mag": float(synthetic),
            "synthetic_numeric_tolerance_mag": NUMERIC_TOLERANCE,
            "pass": bool(abs(raw) <= NUMERIC_TOLERANCE and abs(synthetic) <= NUMERIC_TOLERANCE),
        })
    source_documents = []
    for path in [ORDER04, A1_DOC, PROTOCOL_DOC]:
        source_documents.append({"path": str(path), "sha256": sha256_path(path)})
    result = {
        "status": "FIXTURES_PASS__VARIANT_NOT_ADMITTED" if passed else "FIXTURES_FAIL__VARIANT_NOT_ADMITTED",
        "stage": "ETAPA_1_FIXTURES_ONLY",
        "stage1_complete": False,
        "etapa1_complete": False,
        "variant_id": VARIANT_ID,
        "variant_admitted": False,
        "center_convention": "raw_MAS",
        "tolerances_status": "NOT_AUTHORIZED",
        "stage2_authorized": False,
        "observed_vector_read": False,
        "observed_support_tests": 0,
        "flags": {
            "observed_vector_read": False,
            "observed_support_tests": 0,
            "observed_outputs_read": False,
            "solver_called": False,
            "estimator_evaluate_called": False,
            "D_H0_or_ratio_computed": False,
            "new_seed_or_monte_carlo": False,
            "projection_or_jitter_used": False,
            "mas_ref_value_added_or_subtracted": False,
            "historical_result_tolerance_used": False,
            "manifest_or_entrega_written": False,
            "freeze_R2_v410_or_gate_modified": False,
        },
        "scope": {
            "fixture": "Synthetic R22 host block only: 37 hosts x 3 anchors = 111 raw table rows and 37 host-distance parameters.",
            "generative_equations": ["y_raw = A @ theta + O_MAS", "y_theta = A @ theta (separate support-vector test)"],
            "included": ["explicit line parsing", "N4151 exclusion", "MAS self-reference exclusion", "raw center copy", "A,C,y host-block construction", "72 second differences", "rank/nullity", "production guard unit tests"],
            "excluded": ["observed vector and outputs", "SNe/HF/SBF/megamasers", "full 183-measurement or 255-row network", "solver/evaluate", "D/H0/ratio", "Etapa 2"],
            "meaning": "Passing validates only this synthetic raw_MAS code path; it does not complete Etapa 1 or admit the variant."
        },
        "open_issues": [
            "The documentary bridge from published centers to fits 9/10/11 remains open.",
            "Cell precision and the production quantization rule remain open.",
            "The 72 production tolerances are therefore NOT_AUTHORIZED; only the predeclared synthetic numeric tolerance 1e-12 mag was used here."
        ],
        "execution": {
            "parsed_table_rows_including_distractors": len(parsed),
            "canonical_R22_rows": len(rows),
            "host_count": len({r["host"] for r in rows}),
            "anchor_count": len({r["anchor"] for r in rows}),
            "exclusions": exclusions,
            "A_shape": list(A.shape),
            "C_shape": list(C.shape),
            "R22_covariance_rank": rank_C,
            "R22_covariance_nullity": 111 - rank_C,
            "constraint_rank": rank_B,
            "raw_center_copy_max_abs_mag": raw_center_max_error,
            "raw_generative_max_abs_mag": raw_generative_max_error,
            "raw_72_residual_max_abs_mag": max_raw,
            "A_theta_72_residual_max_abs_mag": max_theta,
            "BA_max_abs": max_BA,
            "BCBT_max_abs": max_BCB,
            "minimum_within_triplet_anchor_separation_mag": minimum_separation,
            "synthetic_numeric_tolerance_mag": NUMERIC_TOLERANCE,
            "checks": checks,
            "production_guard_unit_tests": guards,
        },
        "identity_results": identity_results,
        "hashes": {
            "algorithm": "sha256",
            "montar_variante_py": sha256_path(Path(__file__).resolve()),
            "synthetic_table_text": hashlib.sha256(table_text.encode("utf-8")).hexdigest(),
            "synthetic_parameters_canonical_json": canonical_sha256({
                "hosts": HOSTS, "anchors": ANCHORS, "offsets": OFFSETS,
                "reference_errors": REF_ERRORS, "geometric_errors": GEOMETRIC_ERRORS,
                "theta_host": THETA_HOST, "numeric_tolerance": NUMERIC_TOLERANCE,
            }),
            "source_documents": source_documents,
        },
        "limitations": [
            "Etapa 1 is not complete and the variant is not ready or admitted.",
            "No claim is made about observed centers, physical covariance, the full network, H0, power, or Etapa 2.",
            "Production remains blocked until a complete manifesto, documented precision/quantization/tolerances and explicit Stage 2 authorization exist."
        ],
    }
    return result


def reject_forbidden_path(path: Path) -> None:
    lowered = path.name.lower()
    if "y_obs" in lowered or lowered == "construcao_y_obs.json":
        raise ProductionRefused("OBSERVED_INPUT_FORBIDDEN")


def run_production(args: argparse.Namespace) -> dict:
    if not args.manifest:
        raise ProductionRefused("MANIFESTO_INCOMPLETE")
    manifest_path = Path(args.manifest)
    reject_forbidden_path(manifest_path)
    if not manifest_path.is_file():
        raise ProductionRefused("MANIFESTO_INCOMPLETE")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProductionRefused("MANIFESTO_INCOMPLETE") from exc
    manifest = validate_production_manifest(manifest)
    if not args.table:
        raise ProductionRefused("TABLE_REQUIRED_AFTER_MANIFEST_VALIDATION")
    table_path = Path(args.table)
    reject_forbidden_path(table_path)
    if not table_path.is_file():
        raise ProductionRefused("TABLE_NOT_FOUND")
    # This path is reachable only with a complete manifest and Stage 2 authorization.
    records = parse_host_table_lines(table_path.read_text(encoding="utf-8"))
    rows, references, exclusions = select_r22_rows(records)
    model = build_r22_host_block(rows, references, manifest["covariance_public"]["geometric_anchor_errors"])
    B, metadata = second_difference_matrix(rows)
    residuals = B @ model["y"]
    tolerances = np.asarray(manifest["identity_tolerances"], dtype=float)
    passed = bool(np.all(np.abs(residuals) <= tolerances))
    return {
        "status": "PASS" if passed else "ASSEMBLY_CONSTRAINT_VIOLATION",
        "center_convention": "raw_MAS",
        "identity_count": len(metadata),
        "observed_support_tests": 1,
        "exclusions": exclusions,
        "projection_or_jitter_used": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", action="store_true", help="Run only the built-in synthetic R22 fixture")
    parser.add_argument("--manifest", help="Production manifest; refused unless complete and authorized")
    parser.add_argument("--table", help="Production table; never opened before all guards pass")
    args = parser.parse_args()
    try:
        if args.fixture:
            if args.manifest or args.table:
                raise ProductionRefused("FIXTURE_REFUSED__NO_EXTERNAL_INPUT")
            result = run_fixture()
            OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({
                "status": result["status"],
                "checks": result["execution"]["checks"],
                "raw_72_residual_max_abs_mag": result["execution"]["raw_72_residual_max_abs_mag"],
                "A_theta_72_residual_max_abs_mag": result["execution"]["A_theta_72_residual_max_abs_mag"],
                "stage2_authorized": False,
                "observed_vector_read": False,
                "observed_support_tests": 0,
                "output": str(OUTPUT),
            }, ensure_ascii=False, indent=2))
            if not result["status"].startswith("FIXTURES_PASS"):
                raise SystemExit(1)
        else:
            result = run_production(args)
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except ProductionRefused as exc:
        print(json.dumps({"status": "PRODUCTION_REFUSED", "reason": str(exc), "observed_vector_read": False}), file=sys.stderr)
        raise SystemExit(2) from None


if __name__ == "__main__":
    main()
