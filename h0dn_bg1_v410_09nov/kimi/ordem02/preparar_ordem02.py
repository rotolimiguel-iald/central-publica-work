from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy import linalg

HERE = Path(__file__).resolve().parent
REVIEW = HERE / "PACOTE_REVISAO_R3"
REVIEW.mkdir(exist_ok=True)
BASE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
NET_PATH = BASE / "network/network.npz"
ROWS_PATH = BASE / "network/rows.json"
HOST_PATH = BASE / "network/upstream/data/host_data.dat"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path: Path) -> dict:
    return {"path": str(path), "sha256": sha(path), "bytes": path.stat().st_size}


seeds = {
    "status": "NO_ADMITTED_COVARIANCE__NO_SEEDS_GENERATED",
    "created_before_any_R3_random_draw": True,
    "rng_called": False,
    "new_seed_values": [],
    "new_seed_count": 0,
    "R2_seeds_read_or_touched": False,
    "reason": "No covariance variant has full physical admission; R3 power Monte Carlo is not evaluable.",
    "policy_if_a_variant_is_admitted_later": {
        "entropy_bits": 256,
        "generator": "PCG64 with streams identified by purpose, hypothesis, true variant and batch",
        "custody": "Register secret seeds and publish their SHA-256 before the first draw; freeze code, variants, counts and result schema",
        "no_opportunistic_extension": True,
    },
}
seeds_path = HERE / "SEEDS_R3_REGISTRADAS.json"
seeds_path.write_text(json.dumps(seeds, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

with np.load(NET_PATH, allow_pickle=False) as net:
    A = net["A"].copy()
    C = net["C"].copy()
    c = net["c_cepheid"].copy()
    h_index = int(net["h_index"])
    row_names = net["row_names"].copy()
    F_anchor = net["factor_anchor"].copy()
    F_anchor_names = net["factor_anchor_names"].copy()
    F_MAS = net["factor_MAS"].copy()
    F_MAS_names = net["factor_MAS_names"].copy()
    F_HMS = net["factor_HMS"].copy()
    F_HMS_names = net["factor_HMS_names"].copy()
rows = json.loads(ROWS_PATH.read_text(encoding="utf-8"))
host_lines = HOST_PATH.read_text(encoding="utf-8").splitlines()

# A1: exact shared-measurement decomposition, never an added diagonal.
F_host = F_HMS[:166]
counts = np.count_nonzero(F_host, axis=0)
triplet_cols = np.flatnonzero(counts == 3)
singleton_cols = np.flatnonzero(counts == 1)
assert len(triplet_cols) == 37 and len(singleton_cols) == 55
F_HMS_effective = F_host[:, triplet_cols].copy()
sigma_independent = np.zeros(166)
for j in singleton_cols:
    i = int(np.flatnonzero(F_host[:, j])[0])
    sigma_independent[i] = abs(F_host[i, j])
C_host = C[:166, :166]
C_reconstructed = (
    np.diag(sigma_independent ** 2)
    + F_HMS_effective @ F_HMS_effective.T
    + F_MAS[:166] @ F_MAS[:166].T
    + F_anchor[:166] @ F_anchor[:166].T
)
reconstruction_error = float(np.max(np.abs(C_reconstructed - C_host)))
assert reconstruction_error < 1e-14

# Explicit 72 exact constraints from the 37 R22 triplets.
B = np.zeros((166, 72))
for k in range(1, 37):
    v_nl = np.zeros(166)
    v_nl[[k, k + 37, 0, 37]] = [1.0, -1.0, -1.0, 1.0]
    v_nm = np.zeros(166)
    v_nm[[k, k + 74, 0, 74]] = [1.0, -1.0, -1.0, 1.0]
    B[:, 2 * (k - 1)] = v_nl
    B[:, 2 * (k - 1) + 1] = v_nm
null_host_error = float(np.max(np.abs(C_host @ B)))
null_design_error = float(np.max(np.abs(B.T @ A[:166])))
assert null_host_error < 1e-12 and null_design_error < 1e-10
assert np.linalg.matrix_rank(B) == 72

# Public covariance eigensupport and deterministic synthetic-only checks.
vals, U = linalg.eigh((C + C.T) / 2)
tol = 64 * np.finfo(float).eps * C.shape[0] * vals[-1]
keep = vals > tol
assert int(keep.sum()) == 183 and int((~keep).sum()) == 72
assert vals[0] >= -tol and np.min(vals[keep]) >= 100 * tol
U_pos = U[:, keep]
S_pos = vals[keep]
null_basis = U[:, ~keep]
W = U_pos.T / np.sqrt(S_pos)[:, None]
N_full = np.zeros((255, 72))
N_full[:166] = B

x0 = np.linspace(-0.03, 0.03, A.shape[1])
y0 = A @ x0
fit0 = np.linalg.lstsq(W @ A, W @ y0, rcond=None)[0]
err0 = float(np.max(np.abs(fit0 - x0)))
ext = np.column_stack([A, c])
x1 = np.linspace(0.02, -0.02, ext.shape[1])
y1 = ext @ x1
fit1 = np.linalg.lstsq(W @ ext, W @ y1, rcond=None)[0]
err1 = float(np.max(np.abs(fit1 - x1)))
assert err0 < 1e-7 and err1 < 1e-7
bad = null_basis[:, 0]
bad_detected = float(np.max(np.abs(null_basis.T @ bad))) > 1e-8
assert bad_detected

npz_path = HERE / "C_fisica_R3_A1_REDUCIDA.npz"
np.savez_compressed(
    npz_path,
    A=A,
    C=C,
    c_cepheid=c,
    h_index=np.array(h_index),
    row_names=row_names,
    eigenvalues_positive=S_pos,
    U_positive=U_pos,
    whitener=W,
    null_basis=null_basis,
    exact_host_constraints=B,
    full_explicit_constraints=N_full,
    sigma_independent=sigma_independent,
    F_HMS_effective=F_HMS_effective,
    F_MAS_host=F_MAS[:166],
    F_anchor_host=F_anchor[:166],
    factor_HMS_names=F_HMS_names[triplet_cols],
    factor_MAS_names=F_MAS_names,
    factor_anchor_names=F_anchor_names,
    support_dimension=np.array(183),
    variant_id=np.array("A1_PUBLICADA_REDUCIDA"),
    admission=np.array("A1_ALGEBRA_CLOSED__NOT_FULL_PHYSICAL_COVARIANCE_ADMISSION"),
)

host_records = []
for i in range(166):
    row = rows[i]
    hms_name = str(row["HMS"])
    hms_col = int(np.flatnonzero(F_HMS_names.astype(str) == hms_name)[0])
    is_triplet = bool(counts[hms_col] == 3)
    source_line = int(row["source_line"])
    mu_error = float(host_lines[source_line - 1].split()[2])
    host_records.append({
        "row_zero_based": i,
        "description": str(row_names[i]),
        "host": row["host"],
        "method": row["method"],
        "anchor": row["anchor"],
        "source": row["source"],
        "HMS": hms_name,
        "source_file": str(HOST_PATH),
        "source_line": source_line,
        "mu_error_published_mag": mu_error,
        "sigma_independent_mag": 0.0 if is_triplet else float(sigma_independent[i]),
        "sigma_HMS_shared_effective_mag": float(abs(F_host[i, hms_col])) if is_triplet else 0.0,
        "model_class": "EXACT_SHARED_MEASUREMENT__INDEPENDENT_ZERO" if is_triplet else "SINGLETON_DIAGONAL__NO_HMS_OFFDIAGONAL",
        "MAS_factors": [{"name": str(F_MAS_names[j]), "sigma": float(F_MAS[i, j])} for j in np.flatnonzero(F_MAS[i])],
        "anchor_factors": [{"name": str(F_anchor_names[j]), "sigma": float(F_anchor[i, j])} for j in np.flatnonzero(F_anchor[i])],
    })
host_payload = {
    "status": "A1_DECOMPOSITION_EXACT__NO_OBSERVED_SUPPORT_TEST",
    "formula": "C_host = diag(sigma_independent^2) + F_HMS_effective F_HMS_effective^T + F_MAS F_MAS^T + F_anchor F_anchor^T",
    "triplet_rule": "For 37 R22 host triplets, sigma_independent=0 and the common mu_error is represented once by a full rank-one shared HMS factor.",
    "singleton_rule": "For 55 singleton HMS groups, the published diagonal mu_error is retained and no HMS off-diagonal factor is added.",
    "reconstruction_max_abs": reconstruction_error,
    "host_rank": int(np.linalg.matrix_rank(C_host)),
    "host_nullity": 72,
    "R22_rows": 111,
    "R22_triplets": 37,
    "singleton_HMS_groups": 55,
    "explicit_constraint_rank": 72,
    "max_abs_Chost_times_constraints": null_host_error,
    "max_abs_constraints_transpose_times_Ahost": null_design_error,
    "public_sources": [
        {"url": "https://arxiv.org/html/2510.23823v1", "locator": "Appendix B.2", "fact": "255 equations but 183 distinct measurements; 72 superfluous/overconstrained equations"},
        {"url": "https://arxiv.org/html/2510.23823v1", "locator": "Appendix B.3.2", "fact": "Shared host/method/source implies covariance of the same within-host measurement"},
        {"path": str(BASE / "network/upstream/h0_constrainer/h0_constrainer/equations.py"), "lines": "334-376"},
        {"path": str(BASE / "network/upstream/h0_constrainer/h0_constrainer/data_loader.py"), "lines": "493-503"},
    ],
    "rows": host_records,
    "observed_vector_read": False,
    "observed_support_test": False,
}
host_json_path = HERE / "A1_HOST_DECOMPOSITION.json"
host_json_path.write_text(json.dumps(host_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

synthetic = {
    "status": "A1_SYNTHETIC_SUPPORT_AND_ESTIMATOR_PASS",
    "covariance_rank": 183,
    "covariance_nullity": 72,
    "rank_full_within_support": True,
    "psd_within_frozen_tolerance": True,
    "published_baseline_max_parameter_recovery_error": err0,
    "free_cepheid_model_max_parameter_recovery_error": err1,
    "out_of_support_synthetic_rejected": bad_detected,
    "deterministic_no_RNG": True,
    "observed_vector_read": False,
    "observed_support_tests": 0,
    "estimator_evaluate_called": False,
    "solver_on_observed_called": False,
    "note": "Only exact synthetic vectors built from A or [A,c] in the public support were fitted. A separate null-direction synthetic was rejected. No power was computed.",
}
synthetic_path = HERE / "A1_SINTETICOS.json"
synthetic_path.write_text(json.dumps(synthetic, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

decomposition = {
    "status": "A1_ALGEBRA_CLOSED__FULL_PHYSICAL_COVARIANCE_NOT_ADMITTED",
    "A1_host": {
        "verdict": "CLOSABLE_FROM_PUBLIC_SOURCES__EXACT_REDUNDANCIES",
        "cause": "37 R22 host triplets sharing the same measurement; 111 rows have rank 39 and nullity 72",
        "treatment": "Preserve singular public covariance; reduce to 183 distinct measurements or use Moore-Penrose after exact support validation; never add full HMS diagonal or jitter",
        "matrix": str(npz_path),
        "per_row_decomposition": str(host_json_path),
        "synthetic_receipt": str(synthetic_path),
        "observed_support_tests_now": 0,
    },
    "A2_SN_only": {
        "verdict": "CLOSED_ALGEBRAIC_CONDITIONAL__PHYSICAL_ERROR_MODEL_OPEN",
        "closed": "G42 STATONLY is substituted, not added; no second intrinsic-scatter diagonal is introduced",
        "open": "Aggregation remains source-candidate and release/H0DN error variables were not demonstrated identical",
        "source": "G1_G42_COVARIANCE_SCENARIOS.json and cross_rung/DELIVERY.json",
    },
    "A3_cepheid_host": {
        "verdict": "CLOSED_FOR_G42_STATONLY_ONLY__FULL_DECOMPOSITION_OPEN",
        "reason": "STATONLY does not import the Cepheid-host systematic block; STAT+SYS is not admitted",
    },
    "A4_peculiar_velocity": {
        "verdict": "NO_NEW_PV_FROM_G42_STATONLY__INHERITED_ACCOUNTING_OPEN",
        "reason": "H0DN Hubble-flow covariance already comes from full Pantheon+ and adds its own velocity variance; component-level duplication is unresolved",
        "required": "Original component decomposition before any added PV term",
    },
    "A5_extra13": {
        "all_covariances": "OPEN_NO_TRANSPLANT",
        "variants_declared_blind_before_any_D_or_power": [
            {"id": "EXTRA13_OUT", "rule": "Prospectively exclude only the 13 unresolved SN calibrator equations; preserve shared host/MAS/anchor/group factors and reassess design", "admission": "DESIGN_ADMISSIBLE__BLOCKED_BY_A2_A4_A6"},
            {"id": "EXTRA13_IN_CAP13", "rule": "Diagonal variance inflated by 13 as universal PSD upper bound for unknown internal correlation with fixed marginals", "admission": "ROBUSTNESS_ONLY__NOT_PHYSICAL_COVARIANCE", "missing": "Cross-covariances with 42, HF and hosts plus complete marginals"},
        ],
        "source": "revisao_independente/VALIDACAO_FONTES_13.json",
    },
    "A6_H0DN_BG1": {
        "verdict": "CONDITIONAL_INDEPENDENCE_ONLY__NOT_EMPIRICAL",
        "zero_cross_block": "Allowed only as an explicitly conditional scenario, not a measurement",
        "joint_bound": "For L,B,P require c^T S_BG^{-1} c <= V_L; separate Cauchy-Schwarz bounds are insufficient",
    },
    "admitted_physical_variants": [],
    "full_physical_covariance_closed": False,
    "opening_allowed": False,
    "observed_support_tests_now": 0,
}
decomp_path = HERE / "DECOMPOSICAO_FISICA_R3.json"
decomp_path.write_text(json.dumps(decomposition, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

certificate = {
    "certificate_kind": "COVARIANCE_ADMISSION_REFUSAL",
    "status": "BLOCKED_NO_ADMITTED_COVARIANCE",
    "veredito": "COVARIANCE_NOT_CLOSABLE_FROM_PUBLIC_SOURCES",
    "scope": "A1 is algebraically closable from public sources; the complete A1-A6 physical covariance is not closed by the inspected public sources",
    "admitted_variants": [],
    "D_conservador": None,
    "D_by_variant_and_model": {},
    "power_gate": "NOT_EVALUABLE",
    "mc_status": "NOT_RUN_NO_ADMITTED_COVARIANCE",
    "seed_status": "NO_SEEDS_GENERATED",
    "B1_expected_D": "NOT_EVALUABLE",
    "B2_monte_carlo": "NOT_RUN; no TGL, false-positive, falsification or cross-variant probabilities",
    "B3_variance_budget": {
        "status": "NOT_EVALUABLE",
        "required_disjoint_blocks": ["local_network_except_SN_and_HF", "G42", "extra13", "HF_intercept", "BG1", "all_cross_terms"],
        "reason": "No admitted covariance or influence exists for a physical R3 budget",
    },
    "B4_requirements_to_reach_power": [
        {"block": "A1 exact assembly", "required": "Recover full-precision/shared centers or validate 72 exact identities; then reduce/pseudoinverse without projecting y", "public_addition": "R22 full-precision Y/L/C products if an alternative nonredundant model is desired", "delta_D": "NOT_ESTIMABLE_BEFORE_ADMISSION"},
        {"block": "A2/A3 G42", "required": "Confirm aggregation and identity of error variables; preserve intrinsic scatter by substitution only", "public_addition": "Original aggregated-fit covariance or reproducible joint fit", "delta_D": "NOT_ESTIMABLE_BEFORE_ADMISSION"},
        {"block": "A4 PV", "required": "Separate existing Pantheon+ velocity components from H0DN added velocity variance", "public_addition": "Component-level HF covariance and velocity model", "delta_D": "NOT_ESTIMABLE_BEFORE_ADMISSION"},
        {"block": "A5 extra13", "required": "Either original fit covariance/cross-products or blind EXTRA13_OUT design after A2-A6 admission", "public_addition": "SNooPy/SALT2 internal matrices and cross-survey products; no transplants", "delta_D": "NOT_ESTIMABLE_BEFORE_ADMISSION"},
        {"block": "A6 local-BG1", "required": "Physical cross-covariance or an explicitly accepted bounded scenario", "public_addition": "Joint local/background calibration covariance", "delta_D": "NOT_ESTIMABLE_BEFORE_ADMISSION"},
    ],
    "D_thresholds_for_later_admitted_variants": {"power_80": 5.842, "power_90": 6.282, "power_95": 6.645, "relation": "power=Phi(D-5)"},
    "B5_rule": "POWER_CERTIFIED_REAL only if conservative D>=6.282 and independent review accepts; thresholds remain proposal until operator fixes the opening gate",
    "C_if_H0DN_cannot_reach_power": {
        "proposal_only_not_executed": "B1/conjunto D — PE only-220 under its existing frozen V1 preregistration",
        "route_id": "natureza.5sigma_fora_da_cosmologia_poder_27out",
        "requirement": "Use existing protocol; close physical/shared covariance before any combined significance; do not rewrite preregistration or repeat dead routes",
        "phase9_not_to_repeat": "d1.fase9.v2_c1_a_unica_palavra_23out",
    },
    "opening_allowed": False,
}
cert_path = HERE / "CERTIFICADO_DE_PODER_R3.json"
cert_path.write_text(json.dumps(certificate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

review_order = """# PACOTE DE REVISÃO INDEPENDENTE R3 — A1 e certificado bloqueado

**Estado:** `A1_ALGEBRA_CLOSED__FULL_PHYSICAL_COVARIANCE_OPEN__POWER_NOT_EVALUABLE`

## O revisor deve confirmar

1. As 111 linhas R22 formam 37 tripletes de uma mesma medida; não existem 111 erros independentes a recuperar.
2. A decomposição `diag(sigma_independent^2)+F_HMS_effective F_HMS_effective^T+F_MAS F_MAS^T+F_anchor F_anchor^T` reproduz o bloco publicado sem duplicação.
3. As 72 restrições explícitas têm posto 72, anulam C e A e correspondem às 72 equações redundantes do H0DN público.
4. A matriz permanece PSD, com posto 183 no suporte; somente vetores sintéticos determinísticos foram ajustados e uma direção nula sintética foi rejeitada.
5. A2–A6 continuam sem admissão física completa. Nenhuma variante tem D, poder ou semente R3; o certificado é de recusa de admissão, não `UNDERPOWERED`.
6. Nenhuma projeção de y, jitter, diagonal HMS completa, abertura observada ou teste de suporte observado foi feito nesta ordem.

## Futura única rota observada por variante admitida

Validar estrutura e hashes; montar y bruto; conferir as 72 identidades com tolerância pré-fixada; falhar sem reparo se houver violação; só então reduzir por QR ou usar pseudoinversa. Nunca projetar y para passar. A causa numérica da violação histórica não foi reexaminada.

## O que falta para poder real

Produtos internos/agregados G42, decomposição PV, covariâncias/cruzamentos dos 13 ou poda cega após admissão, covariância local–BG1 e revisão independente. Só então registrar sementes novas e executar D, orçamento de variância e Monte Carlo cruzado.
"""
review_order_path = REVIEW / "ORDEM_REVISAO_R3.md"
review_order_path.write_text(review_order, encoding="utf-8")

validator = r'''from pathlib import Path
import hashlib
import json
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED = {
    "SEEDS_R3_REGISTRADAS.json": "__SEEDS__",
    "C_fisica_R3_A1_REDUCIDA.npz": "__NPZ__",
    "A1_HOST_DECOMPOSITION.json": "__HOST__",
    "DECOMPOSICAO_FISICA_R3.json": "__DECOMP__",
    "CERTIFICADO_DE_PODER_R3.json": "__CERT__",
    "A1_SINTETICOS.json": "__SYN__",
    "PACOTE_REVISAO_R3/ORDEM_REVISAO_R3.md": "__ORDER__",
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

hashes = {name: sha(ROOT / name) for name in EXPECTED}
seeds = json.loads((ROOT / "SEEDS_R3_REGISTRADAS.json").read_text(encoding="utf-8"))
decomp = json.loads((ROOT / "DECOMPOSICAO_FISICA_R3.json").read_text(encoding="utf-8"))
cert = json.loads((ROOT / "CERTIFICADO_DE_PODER_R3.json").read_text(encoding="utf-8"))
syn = json.loads((ROOT / "A1_SINTETICOS.json").read_text(encoding="utf-8"))
with np.load(ROOT / "C_fisica_R3_A1_REDUCIDA.npz", allow_pickle=False) as d:
    A, C = d["A"], d["C"]
    B = d["exact_host_constraints"]
    sigma = d["sigma_independent"]
    FH = d["F_HMS_effective"]
    FM = d["F_MAS_host"]
    FA = d["F_anchor_host"]
    C_rec = np.diag(sigma ** 2) + FH @ FH.T + FM @ FM.T + FA @ FA.T
    host_error = float(np.max(np.abs(C_rec - C[:166, :166])))
    null_C = float(np.max(np.abs(C[:166, :166] @ B)))
    null_A = float(np.max(np.abs(B.T @ A[:166])))
    rank = int(np.linalg.matrix_rank(C))
    host_rank = int(np.linalg.matrix_rank(C[:166, :166]))
    symmetry = float(np.max(np.abs(C - C.T)))
    forbidden = sorted(set(d.files) & {"y", "y_obs", "local", "observed", "observed_y"})
checks = {
    "hashes_match": hashes == EXPECTED,
    "covariance_symmetric": symmetry < 1e-14,
    "full_support_rank_183": rank == 183,
    "host_rank_94": host_rank == 94,
    "constraint_rank_72": int(np.linalg.matrix_rank(B)) == 72,
    "constraint_null_C": null_C < 1e-12,
    "constraint_null_A": null_A < 1e-10,
    "host_reconstruction_exact": host_error < 1e-14,
    "synthetic_only_pass": syn["status"] == "A1_SYNTHETIC_SUPPORT_AND_ESTIMATOR_PASS" and syn["deterministic_no_RNG"] and syn["out_of_support_synthetic_rejected"],
    "synthetic_precision": syn["published_baseline_max_parameter_recovery_error"] < 1e-7 and syn["free_cepheid_model_max_parameter_recovery_error"] < 1e-7,
    "no_admitted_variant": decomp["admitted_physical_variants"] == [] and cert["admitted_variants"] == [],
    "power_not_evaluable": cert["power_gate"] == "NOT_EVALUABLE" and cert["D_by_variant_and_model"] == {} and cert["D_conservador"] is None,
    "mc_not_run": cert["mc_status"] == "NOT_RUN_NO_ADMITTED_COVARIANCE",
    "no_new_seeds": seeds["new_seed_count"] == 0 and seeds["rng_called"] is False and seeds["R2_seeds_read_or_touched"] is False,
    "opening_blocked": decomp["opening_allowed"] is False and cert["opening_allowed"] is False,
    "no_observed_arrays": len(forbidden) == 0,
    "no_observed_support_now": decomp["observed_support_tests_now"] == 0 and syn["observed_support_tests"] == 0,
}
validated = all(checks.values())
result = {
    "status": "R3_REVIEW_VALIDATED__A1_ALGEBRA_CLOSED__POWER_NOT_EVALUABLE" if validated else "R3_REVIEW_VALIDATION_FAILED",
    "A1_algebra_closed": True,
    "full_physical_covariance_closed": False,
    "admitted_variants": [],
    "D_conservador": None,
    "power_gate": "NOT_EVALUABLE",
    "mc_status": "NOT_RUN_NO_ADMITTED_COVARIANCE",
    "new_seed_count": 0,
    "observed_vector_read": False,
    "observed_support_tests_now": 0,
    "opening_allowed": False,
    "checks": checks,
    "metrics": {"host_reconstruction_max_abs": host_error, "constraint_C_max_abs": null_C, "constraint_A_max_abs": null_A, "covariance_rank": rank, "host_rank": host_rank},
    "hashes": hashes,
}
(HERE / "VALIDACAO_R3.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
if not validated:
    raise RuntimeError("R3 review validation failed")
'''
for token, path in {
    "__SEEDS__": seeds_path,
    "__NPZ__": npz_path,
    "__HOST__": host_json_path,
    "__DECOMP__": decomp_path,
    "__CERT__": cert_path,
    "__SYN__": synthetic_path,
    "__ORDER__": review_order_path,
}.items():
    validator = validator.replace(token, sha(path))
validator_path = REVIEW / "verificar_r3.py"
validator_path.write_text(validator, encoding="utf-8")
print(json.dumps({"seeds": pin(seeds_path), "matrix": pin(npz_path), "host": pin(host_json_path), "decomposition": pin(decomp_path), "certificate": pin(cert_path), "synthetic": pin(synthetic_path), "review_order": pin(review_order_path), "validator": pin(validator_path)}, ensure_ascii=False, indent=2))
