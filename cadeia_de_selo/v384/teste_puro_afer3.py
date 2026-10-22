# -*- coding: utf-8 -*-
"""Teste PURO das correcoes da 3a afericao no trabalhador: compare_cpuref e derive_verdict com entradas SINTETICAS (nenhum operador da teoria, nenhuma GPU)."""
import importlib.util, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sp_ = importlib.util.spec_from_file_location("w", os.path.join(HERE, "pilar_quantico_worker.py")); w = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(w)
ct = {"cci": 1e-9, "purity": 1e-9, "folds_n_c1": 1e-9, "gap_rel_rel": 1e-6, "choi_min": 1e-9, "min_gap_rel_for_compare": 1e-6}
sp8 = {"cpuref": {"tol": ct}}; me = {"run_id": "r", "spec_sha256": "x", "beta_hex": "0x1p-7", "worker_sha256": "w"}
g = {"status": "UNIQUE", "gap_rel": 1e-3, "cci": 0.5, "purity": 0.4, "folds": [{"n": 2.9}, {"n": 2.1}], "choi_min": 0.0}
c = {"status": "UNIQUE", "gap_rel": 1e-3, "cci": 0.5, "purity": 0.4, "folds_n_c1": 2.9, "folds_n_c2": 2.1, "choi_min": 0.0}
res = {}
res["igual"] = w.compare_cpuref(sp8, {"a": g, "b": g}, dict(me, items={"a": c, "b": c}), me, 0)
res["cci_fora"] = w.compare_cpuref(sp8, {"a": g, "b": g}, dict(me, items={"a": c, "b": dict(c, cci=0.5 + 1e-6)}), me, 0)
res["so_nc2"] = w.compare_cpuref(sp8, {"a": g}, dict(me, items={"a": dict(c, folds_n_c2=2.1 + 1e-5)}), me, 0)
res["perto"] = w.compare_cpuref(sp8, {"a": dict(g, gap_rel=1e-8)}, dict(me, items={"a": dict(c, gap_rel=1e-8)}), me, 0)
res["rc_filho_1"] = w.compare_cpuref(sp8, {"a": g}, dict(me, items={"a": c}), me, 1)
for k, v in res.items():
    print(k, {kk: v[kk] for kk in ("read", "compared", "near_threshold_not_compared", "not_comparable", "disagreements", "ok", "informative_only")})
assert res["igual"]["ok"] and not res["cci_fora"]["ok"] and res["so_nc2"]["ok"] and res["perto"]["not_comparable"] and not res["perto"]["ok"] and not res["rc_filho_1"]["ok"]
# a arvore: um R sintetico de sucesso, depois as variacoes
spec = {"tolerances": {"identity_abs": 1e-12, "identity_rel": 1e-12}}
cfg = {"n_points": 4, "unique": 4, "identity_violations": 0, "folds_window": [1, 2, 3], "cci_half_window": [1, 2, 2]}
R0 = {"engine_selftest": {"all_ok": True},
      "T3": {"d8": {"N1_dephasing_only": {"failed_as_required": True}, "N4_negative_rate_not_cp": {"failed_as_required": True}, "N5_time_reversal_not_cp": {"failed_as_required": True},
                    "N2_unital_identity": {"identity_ok": True}}, "N3_linear_law": {"8": {"sigma_0.0": {"pass_frac": 1.0, "root_law_rejected_frac": 1.0}, "errors": 0}}},
      "T2": {"configs": [cfg], "identities": {"sin2_thetaM_minus_beta": 0.0}, "instance_errors": 0},
      "T1": {"8": {"sigma_0.0": {"pass_frac": 1.0}, "errors": 0}},
      "T4": {"8": {"n": 10, "UNIQUE": 10, "all_identities_checked": 10, "viol": {}, "ERROR": 0}},
      "cpuref_compare": {"ok": True},
      "D128": {"ran": True, "status": "UNIQUE", "status_code": "RAN", "zero_mode_ok": True}}
import copy
V = {}
V["sucesso"] = w.derive_verdict(spec, R0)
R1 = copy.deepcopy(R0); R1["D128"]["zero_mode_ok"] = False; R1["D128"]["status"] = "AMBIGUOUS"; V["d128_sem_zero"] = w.derive_verdict(spec, R1)
R2 = copy.deepcopy(R0); R2["cpuref_compare"] = {"ok": False, "not_comparable": True}; V["cpu_nao_comparavel"] = w.derive_verdict(spec, R2)
R3 = copy.deepcopy(R0); R3["cpuref_compare"] = {"ok": False, "not_comparable": False, "disagreements": 1}; V["cpu_discorda"] = w.derive_verdict(spec, R3)
R4 = copy.deepcopy(R0); R4["fatal"] = "x"; R4["parent_gone"] = True; V["pai_morto"] = w.derive_verdict(spec, R4)
for k, v in V.items():
    print(k, v)
assert V["sucesso"].startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__") and "IDENTITY_VIOLATED_1" in V["d128_sem_zero"]
assert "CPU_REFERENCE_NOT_COMPARABLE" in V["cpu_nao_comparavel"] and "CPU_REFERENCE_DISAGREES_OR_ABSENT" in V["cpu_discorda"] and "PARENT_GONE" in V["pai_morto"]
# ParentGone atravessa um except Exception
try:
    try:
        raise w.ParentGone("x")
    except Exception:
        print("ENGOLIDO (errado)"); raise SystemExit(1)
except w.ParentGone:
    print("ParentGone atravessa except Exception: ok")
print("TUDO OK")
