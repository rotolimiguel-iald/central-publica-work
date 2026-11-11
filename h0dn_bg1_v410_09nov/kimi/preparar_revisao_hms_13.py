from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

BASE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
HERE = Path(__file__).resolve().parent
OUT = HERE / "revisao_independente"
OUT.mkdir(exist_ok=True)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


network_path = BASE / "network/network.npz"
factor_source_path = BASE / "network/upstream/h0_constrainer/h0_constrainer/data_loader.py"
covariance_source_path = BASE / "network/build_network.py"
source_artifacts = {
    "network": {
        "path": str(network_path),
        "sha256": sha(network_path),
    },
    "factor_constructor": {
        "path": str(factor_source_path),
        "sha256": sha(factor_source_path),
        "lines": "493-503",
        "required_snippets": [
            'hms_errors = host_df["mu_error"].values[wh]',
            "mu_hms_error[i] = hms_errors[0]",
            "mu_hms_error[i] = np.min(hms_errors)",
        ],
    },
    "covariance_constructor": {
        "path": str(covariance_source_path),
        "sha256": sha(covariance_source_path),
        "lines": "348-355 and 381-383",
        "required_snippets": [
            "term -= np.diag(np.diag(term))",
            "HMS terms add only offdiagonal covariance, with diagonal already contained in host mu_error.",
        ],
    },
}
prior_receipts = {
    name: {"path": str(HERE / name), "sha256": sha(HERE / name)}
    for name in ["ENTREGA_H0DN_Y_OBS.json", "DIAGNOSTICO_HMS_COMPLETA.json"]
}

with np.load(network_path, allow_pickle=False) as net:
    C = net["C"].copy()
    F = net["factor_HMS"].copy()
T = F @ F.T
np.savez_compressed(
    OUT / "fator_HMS_e_matrizes.npz",
    factor_HMS=F,
    T_HMS=T,
    T_HMS_diagonal=np.diag(T),
    C_published=C,
    C_full_HMS_diagnostic=C + np.diag(np.diag(T)),
    evidence=np.array(["factor_HMS is built from mu_error itself; full diagonal duplicates shared variance unless original error budgets are decomposed"]),
)

extra13 = [
    {"CID": "2011iv", "host": "N1404", "status": "PRESENT_BUT_NOT_R22", "release_IS_CALIBRATOR": 0, "next": "Reconcile H0DN value with independent original source; no direct transplant of Pantheon+ covariance"},
    {"CID": "2007on", "host": "N1404", "status": "PRESENT_BUT_NOT_R22", "release_IS_CALIBRATOR": 0, "next": "Same; do not use arithmetic combinations from unrelated SN rows"},
    {"CID": "2021rhu", "host": "N7814", "status": "ABSENT_FROM_PANTHEON_RELEASE", "release_IS_CALIBRATOR": None, "next": "Use Dhawan/TRGB and original light-curve/error budget; do not infer from another ID"},
    {"CID": "1980N", "host": "N1316", "status": "PRESENT_BUT_NOT_R22", "release_IS_CALIBRATOR": 0, "next": "Reconcile original photometry and uncertainty model; no direct transplant"},
    {"CID": "1981D", "host": "N1316", "status": "PRESENT_BUT_NOT_R22", "release_IS_CALIBRATOR": 0, "next": "Reconcile original photometry and uncertainty model; no direct transplant"},
    {"CID": "2006dd", "host": "N1316", "status": "PRESENT_BUT_NOT_R22", "release_IS_CALIBRATOR": 0, "next": "Reconcile original photometry and uncertainty model; no direct transplant"},
    {"CID": "1998bu", "host": "M96", "status": "CANONICAL_REDSHIFT_ONLY_TOO_REDDENED_FOR_R22", "release_IS_CALIBRATOR": None, "next": "Use Jha et al. 1999 and original photometry; do not treat as a missing alias"},
    {"CID": "1989B", "host": "M66", "status": "CANONICAL_REDSHIFT_ONLY_TOO_REDDENED_FOR_R22", "release_IS_CALIBRATOR": None, "next": "Use Wells et al. 1994 and original photometry; do not treat as a missing alias"},
    {"CID": "1994D", "host": "N4526", "status": "ALIAS_CLOSED_BUT_NOT_R22", "release_IS_CALIBRATOR": 0, "next": "Alias 1994DRichmond is validated; use Richmond et al. 1995 error budget, not R22 covariance"},
    {"CID": "1992A", "host": "N1380", "status": "PRESENT_BUT_NOT_R22", "release_IS_CALIBRATOR": 0, "next": "Reconcile original photometry and uncertainty model; no direct transplant"},
    {"CID": "ASASSN-14lp", "host": "N4666", "status": "ABSENT_FROM_PANTHEON_RELEASE", "release_IS_CALIBRATOR": None, "next": "Use arXiv:1507.04257 and original ASAS-SN/SNooPy error budget; no SALT2 substitution"},
    {"CID": "2021J", "host": "N4414", "status": "ABSENT_FROM_PANTHEON_RELEASE", "release_IS_CALIBRATOR": None, "next": "Use Gallego-Cano et al. 2022, OSN/Swift/SNooPy error budget; no SALT2 substitution"},
    {"CID": "2020nvb", "host": "N4457", "status": "ABSENT_FROM_PANTHEON_RELEASE", "release_IS_CALIBRATOR": None, "next": "Use AAVSO 709 and the independent TRGB route; no identity or covariance borrowed from Pantheon+"},
]
source_queue = {
    "shared_HMS": "Original error budgets for every host equation, decomposed into independent and shared components with source lines",
    "original_sources": {
        "2021rhu": "Dhawan et al. 2022/TRGB and original ZTF/Swift photometry; Harvey et al. 2023 for transitional-SN treatment",
        "ASASSN-14lp": "https://arxiv.org/html/1507.04257v2",
        "2021J": "https://www.aanda.org/articles/aa/full_html/2022/10/aa43988-22/aa43988-22.html",
        "2020nvb": "AAVSO Alert Notice 709 plus https://arxiv.org/html/2508.20023 for independent TRGB route",
        "1998bu": "Jha et al. 1999, The Type Ia Supernova 1998bu in M96 and the Hubble Constant, doi:10.1086/313275",
        "1989B": "Wells et al. 1994 and original SN 1989B photometry",
        "1994D": "https://articles.adsabs.harvard.edu/pdf/1995AJ....109.2121R",
        "2008fv": "Tsvetkov & Elenin 2010 and Pantheon+ all_redshifts_PVs.csv for canonical identity",
        "2011iv/2007on/1980N/1981D/2006dd/1992A": "Original photometry/error budgets matching the H0DN values, not only Pantheon+ rows with IS_CALIBRATOR=0",
    },
    "prohibited": [
        "Adding the full HMS diagonal without removing the shared component already in mu_error",
        "Treating any missing ID as permission to assign a nearby alias",
        "Transplanting STAT+SYS wholesale and duplicating Cepheid-host covariance",
        "Choosing a covariance scenario because it raises power",
    ],
}

payload = {
    "status": "REVIEW_PACKAGE_READY__PHYSICAL_CLOSURE_OPEN",
    "source_artifacts": source_artifacts,
    "prior_support_receipts": prior_receipts,
    "proof_of_duplication": {
        "factor_source": "network/upstream/h0_constrainer/h0_constrainer/data_loader.py compute_host_extras, lines 493-503",
        "fact": "factor_HMS is built directly from mu_error values",
        "matrix_source": "network/build_network.py lines 348-355 and 381-383: HMS terms add only offdiagonal covariance, with diagonal already contained in host mu_error",
        "conclusion": "Adding full HMS diagonal repeats the shared variance instead of deriving independent information",
        "T_HMS_rank": int(np.linalg.matrix_rank(T)),
        "T_HMS_nonzero_diagonal_terms": int(np.count_nonzero(np.diag(T))),
    },
    "decomposition_current": {
        "host_rank": 94,
        "host_nullity": 72,
        "published_support_max_abs": 0.09312020264507931,
        "published_support_pass": False,
        "full_HMS_rank": 255,
        "full_HMS_support_pass": True,
        "full_HMS_admitted": False,
        "support_values_transferred_not_recomputed": True,
        "reason": "Duplication, not merely uncertainty about physical suitability",
    },
    "required_decomposition": {
        "independent_host_errors": "sigma_independent,i with source and exact row mapping",
        "shared_host_factors": "F_anchor, F_MAS, F_HMS with no duplication of the shared part already in sigma_independent",
        "sn_only": "G42 STATONLY, with intrinsic-scatter reconciliation",
        "cepheid_host": "Separate host covariance without double counting",
        "peculiar_velocity": "Separate PV covariance without duplicating H0DN's additional velocity variance",
        "extra_13": "Original covariance or explicit OPEN_NO_TRANSPLANT for each ID",
    },
    "extra_13": extra13,
    "source_queue": source_queue,
    "acceptance_tests": [
        "Reproduce current host rank 94/nullity 72 and max null projection 0.09312020264507931",
        "Reproduce full HMS rank 255, then demonstrate why it duplicates mu_error",
        "Reconstruct each independent/shared error budget with source lines and validate no duplicated variance",
        "Resolve each of the 13 IDs as source-backed covariance or explicit OPEN_NO_TRANSPLANT",
        "Re-run support only after physical decomposition is independently accepted; do not call estimator.evaluate before that acceptance",
    ],
    "no_evaluation": True,
    "no_new_R2_seed": True,
    "no_gate_change": True,
}
json_path = OUT / "DECOMPOSICAO_HMS_E_13.json"
json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

order = f"""# ORDEM DE REVISÃO INDEPENDENTE — HMS e os 13 calibradores

**Data:** 09/11/2026  
**De:** Kimi K3 Pro  
**Para:** revisor independente da gerência c1 ou ASTRA  
**Estado:** `REVIEW_PACKAGE_READY__PHYSICAL_CLOSURE_OPEN`

## Evidência que deve ser reproduzida

1. O bloco de hospedeiras tem posto 94 e nulidade 72; a projeção nula máxima do vetor é 0,09312020264507931.
2. A forma HMS completa tem posto 255 e passa no suporte, mas **não é admitida**: `factor_HMS` é construído dos próprios `mu_error`, e sua diagonal já está incluída em `mu_error`.
3. A matriz `fator_HMS_e_matrizes.npz` contém o fator, a matriz T = F Fᵀ, a matriz publicada e a forma HMS completa apenas diagnóstica.

## Missão do revisor

- Reconstruir a decomposição independente/compartilhada dos erros das 166 equações de hospedeiras, com fontes e linhas exatas.
- Decidir se a diagonal HMS pode ser usada sem duplicar variância; se não puder, declarar a obstrução em vez de forçar o posto 255.
- Resolver os 13 calibradores adicionais por fonte original ou marcar cada um `OPEN_NO_TRANSPLANT`.
- Conferir que Cepheid, dispersão intrínseca e velocidades peculiares não foram duplicados.
- Repetir os testes de suporte somente após aceitar a decomposição física; não calcular Z, t, h ou razão nesta revisão.

## Os 13 casos, sem atalhos

{json.dumps(extra13, ensure_ascii=False, indent=2)}

## Fontes exigidas

{json.dumps(source_queue, ensure_ascii=False, indent=2)}

## Critério de aceite

A revisão só pode fechar G3/G4 quando a decomposição original estiver completa, sem duplicação, e o vetor passar no suporte com uma matriz cuja origem física tenha sido aceita independentemente. Se isso não for possível, o resultado correto é `OBSTRUCTION_EXACT`, não uma covariância artificialmente de posto completo.

**Não execute estimator.evaluate, não ajuste dados, não gere novas sementes e não mova o gate.**
"""
order_path = OUT / "ORDEM_REVISAO_INDEPENDENTE_HMS_13.md"
order_path.write_text(order, encoding="utf-8")

validator = '''from pathlib import Path
import hashlib
import json
import numpy as np

HERE = Path(__file__).resolve().parent
EXPECTED_HASHES = {
    "fator_HMS_e_matrizes.npz": "__MATRICES_SHA256__",
    "DECOMPOSICAO_HMS_E_13.json": "__DECOMPOSITION_SHA256__",
    "ORDEM_REVISAO_INDEPENDENTE_HMS_13.md": "__ORDER_SHA256__",
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
(HERE / "VALIDACAO_PACOTE.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
if not validated:
    raise RuntimeError("Review package validation failed; inspect VALIDACAO_PACOTE.json")
'''
for token, path in {
    "__MATRICES_SHA256__": OUT / "fator_HMS_e_matrizes.npz",
    "__DECOMPOSITION_SHA256__": json_path,
    "__ORDER_SHA256__": order_path,
}.items():
    validator = validator.replace(token, sha(path))
validator_path = OUT / "verificar_pacote.py"
validator_path.write_text(validator, encoding="utf-8")

print(json.dumps({
    "package": str(OUT),
    "decomposition_sha256": sha(json_path),
    "order_sha256": sha(order_path),
    "validator_sha256": sha(validator_path),
    "matrices_sha256": sha(OUT / "fator_HMS_e_matrizes.npz"),
}, ensure_ascii=False, indent=2))
