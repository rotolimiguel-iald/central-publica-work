from pathlib import Path
import hashlib
import json
import numpy as np

HERE = Path(__file__).resolve().parent
EXPECTED_HASHES = {
    "fator_HMS_e_matrizes.npz": "6b88c64c55ac9b2a1832a3ac89d6e9e9af5cdfaad81c2db20cf9bffb34d8c89f",
    "DECOMPOSICAO_HMS_E_13.json": "d13ca238f6593674bcb3328a86f91411ba5237c65643d5981c2df7969d9ba9b5",
    "ORDEM_REVISAO_INDEPENDENTE_HMS_13.md": "6a1eb8adfd86ec90ac3098d08a4c0e1f6c79d461d621c3fe464ac00ddf918627",
}
EXPECTED_IDS = [
    "2011iv", "2007on", "2021rhu", "1980N", "1981D", "2006dd", "1998bu",
    "1989B", "1994D", "1992A", "ASASSN-14lp", "2021J", "2020nvb",
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

actual_hashes = {name: sha(HERE / name) for name in EXPECTED_HASHES}
decomposition = json.loads((HERE / "DECOMPOSICAO_HMS_E_13.json").read_text(encoding="utf-8"))
source_results = {}
for label, record in decomposition["source_artifacts"].items():
    path = Path(record["path"])
    source_ok = path.is_file() and sha(path) == record["sha256"]
    if label != "network":
        text = path.read_text(encoding="utf-8")
        source_ok = source_ok and all(snippet in text for snippet in record["required_snippets"])
    source_results[label] = bool(source_ok)
prior_results = {
    name: Path(record["path"]).is_file() and sha(Path(record["path"])) == record["sha256"]
    for name, record in decomposition["prior_support_receipts"].items()
}

with np.load(HERE / "fator_HMS_e_matrizes.npz", allow_pickle=False) as data:
    F = data["factor_HMS"].copy()
    T = data["T_HMS"].copy()
    C = data["C_published"].copy()
    C_hms = data["C_full_HMS_diagnostic"].copy()
with np.load(decomposition["source_artifacts"]["network"]["path"], allow_pickle=False) as source:
    F_source = source["factor_HMS"].copy()
    C_source = source["C"].copy()

host_rank = int(np.linalg.matrix_rank(C[:166, :166]))
host_nullity = int(166 - host_rank)
full_rank = int(np.linalg.matrix_rank(C_hms))
ids = [case["CID"] for case in decomposition["extra_13"]]
checks = {
    "package_hashes_match": actual_hashes == EXPECTED_HASHES,
    "source_hashes_and_snippets_match": all(source_results.values()),
    "prior_support_receipt_hashes_match": all(prior_results.values()),
    "factor_matches_source_network": bool(np.array_equal(F, F_source)),
    "covariance_matches_source_network": bool(np.array_equal(C, C_source)),
    "T_equals_FF_transpose": bool(np.allclose(T, F @ F.T, rtol=1e-12, atol=1e-15)),
    "full_HMS_is_C_plus_T_diagonal": bool(np.allclose(C_hms, C + np.diag(np.diag(T)), rtol=1e-12, atol=1e-15)),
    "published_host_rank_94": host_rank == 94,
    "published_host_nullity_72": host_nullity == 72,
    "full_HMS_rank_255": full_rank == 255,
    "factor_constructor_uses_mu_error": source_results.get("factor_constructor", False),
    "offdiagonal_only_semantics_confirmed": source_results.get("covariance_constructor", False),
    "full_HMS_not_admitted": decomposition["decomposition_current"]["full_HMS_admitted"] is False,
    "support_values_transferred_not_recomputed": decomposition["decomposition_current"]["support_values_transferred_not_recomputed"] is True,
    "no_evaluation_flags": decomposition["no_evaluation"] is True and decomposition["no_new_R2_seed"] is True and decomposition["no_gate_change"] is True,
    "extra_13_exact_ids": ids == EXPECTED_IDS and len(set(ids)) == 13,
    "extra_13_all_have_source_instruction": all(bool(case.get("next")) for case in decomposition["extra_13"]),
}
factor_identity = all(checks[name] for name in [
    "factor_matches_source_network", "covariance_matches_source_network",
    "T_equals_FF_transpose", "full_HMS_is_C_plus_T_diagonal",
    "factor_constructor_uses_mu_error", "offdiagonal_only_semantics_confirmed",
])
validated = all(checks.values()) and factor_identity
result = {
    "status": "REVIEW_PACKAGE_VALIDATED__CLOSURE_STILL_OPEN" if validated else "REVIEW_PACKAGE_VALIDATION_FAILED",
    "factor_identity": bool(factor_identity),
    "published_host_rank": host_rank,
    "published_host_nullity": host_nullity,
    "full_HMS_rank": full_rank,
    "full_HMS_admitted": bool(decomposition["decomposition_current"]["full_HMS_admitted"]),
    "opening_allowed": False,
    "observed_vector_read_by_validator": False,
    "observed_statistics_recomputed": False,
    "reason": "Full HMS diagonal repeats shared variance already included in mu_error; rank 255 is diagnostic only.",
    "checks": checks,
    "source_results": source_results,
    "prior_support_receipt_results": prior_results,
    "hashes": actual_hashes,
}
(HERE / "VALIDACAO_PACOTE.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
if not validated:
    raise RuntimeError("Review package validation failed; inspect VALIDACAO_PACOTE.json")
