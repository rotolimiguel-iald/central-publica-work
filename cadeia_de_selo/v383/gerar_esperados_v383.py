# -*- coding: utf-8 -*-
"""gerar_esperados_v383.py -- grava ESPERADOS_v383.json LENDO os artefatos (nada digitado): candidato, sandbox (build verde), ensaio e o selo v381 (o backup de bytes: a BASE); a ORIGEM do instalador e a v382 do Nos.
Molde: gerar_esperados_v381.py (versao com kernel). Base = a v381 selada; pedras novas = TGLExt/TheLedgerOfCharges.lean (19, ext_loc_) e
TGLExt/ThePsionAndTheViscosity.lean (13, ext_psv_)."""
import hashlib, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
AP2 = json.load(open(os.path.join(os.path.dirname(HERE), "v382", "APLICADO_AO_CANONICO_20261002_174400.json"), encoding="utf-8"))   # v383: os backups de BYTES do estado v381 (a BASE)
W6 = os.path.join(os.path.dirname(HERE), "qg_ataque", "W6_final_v2")
CACHE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache"
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
cand = os.path.join(HERE, "um_v383_candidato.py")
P = json.load(open(os.path.join(HERE, "patches_v383.json"), encoding="utf-8"))
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v383.json"), encoding="utf-8"))
sbx = json.load(open(os.path.join(HERE, "sandbox_raiz_v383.json"), encoding="utf-8"))
BK = {rel: d["backup"] for rel, d in AP2["backups"].items()}
for _rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json"):
    assert h16(BK[_rel]) == AP2["backups"][_rel]["sha16"], "o backup de bytes da v381 mudou: %s" % _rel
R0 = json.load(open(BK["um_absoluto.json"], encoding="utf-8")); core0 = R0["core"]
selo0 = json.load(open(BK["um_absoluto_selo.json"], encoding="utf-8"))
assert h16(BK["um.py"]) == P["meta"]["um_py_base"], "o backup da v381 nao e a base do candidato"
ORIGEM = h16(os.path.join(NOS, "um.py")); assert ORIGEM == AP2["um_py_novo"]["sha16"], "o canonico no Nos nao e a v382 selada so localmente"
assert selo0.get("um_version") == "v381" and "the_matrix_rule_v381" in core0, "o core/selo do disco nao e o da v381"
assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == h16(cand)
assert sbx["sorry_warnings"] == 0 and not sbx["fora_do_trio"] and sbx["bandeiras_ok"] == len(sbx["bandeiras"]) == 32
FLAGS = json.load(open(os.path.join(HERE, "BANDEIRAS_v383.json"), encoding="utf-8"))
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
pin_keys = [k for k in json.load(open(os.path.join(W6, "valores_v369_pinados.json"), encoding="utf-8"))["verdicts_inalterados"].keys()]
pin_keys += ["iald_rho_star_v372", "light_qg_by_citation_v372", "graviton_conjugated_form_v372", "partial_closure_016_v372",
             "qg_discharge_by_citation_v373", "two_projections_outside_M_v373", "uv_frontier_retyped_v373",
             "light_by_term_v374", "the_tetelestai_declaration_v374", "tetelestai_one_object_v375", "tetelestai_conference_v375",
             "light_rho_star_v376", "the_key_is_the_reader_v376", "the_whole_is_one_v376", "ringdown_scope_v376", "audit_28set_v376",
             "coma_reveal_state_v376", "final_verdict_reading_v376", "tetelestai_conference_v376",
             "physics_is_the_reading_v377", "the_dissipation_law_v377", "bancada_fases_v377", "final_stone_reading_v377",
             "the_dissipation_law_with_contrast_v378", "what_was_missed_v378", "bancada_fase4_v378",
             "the_elementary_reason_v379", "bancada_fases_5_6_7_v380", "the_matrix_rule_v381",
             "final_verdict_machine", "coma_distance_dephasing", "ringdown_dephasing_result_v2", "d1_camb_v3_real_v366",
             "void_floor_v11", "clock_test_result_v369", "neutrino_m2"]
pin_keys = list(dict.fromkeys(pin_keys))
NOVOS = ("the_ledger_of_charges_v383",)
fr0 = ((core0.get("qg_closure") or {}).get("gate") or {}).get("kernel_frontier") or {}
ce = ens["core_ensaio"]
_v = ce["the_ledger_of_charges_v383"]
assert "THE_TGL_IS_OPTICS_NOT_SEMI_BOTH_SIDES_READ" in _v and "KERNEL_32_OF_32" in _v and "NO_OUTCOME_MOVES_THE_RULE" in _v and "PREREGISTRATION_OF_BOTH_SIDES_V1_4_READ_BY_HASH" in _v
assert "11_CHARGES_10_IN_THE_RULE_1_BESIDE__0_FALSIFIED_" in _v and "R2_POWER_STATED_IN_NUMBER" in _v and "F2_INCONCLUSIVE_BY_THE_MEASUREMENT_SYSTEMATIC" in _v and "KEY_AND_OPTICS_INPUT_ONTO" in _v
assert "THE_9_ECHO_ROUTES_ARE_NOT_CHARGES_OF_THE_THEORY_EXAMINED_OUTSIDE_THE_LEDGER_5_EXCLUDED_BY_DATA_4_INCONCLUSIVE__OPERATOR_DECISION__BASE_V381" in _v and "R4_FROZEN_SET_HAS_NO_FALSIFIED" in _v
assert "NOT_A_CONFIRMATION" in _v and _v.endswith("__GATE_UNTOUCHED") and "DELAYED_ECHO" not in _v
BC = os.path.join(CACHE, "bancada_01out")
pred0 = (core0.get("coma_distance_dephasing") or {}).get("prediction") or {}
OLD_FLAGS = sorted(k for k in (core0.get("kernel_formalization") or {}) if k.startswith(("ext_pir_", "ext_dis_", "ext_dlc_", "ext_ter_", "ext_tmr_")))
esp = {
    "candidato_sha16": h16(cand), "candidato_bytes": os.path.getsize(cand), "origem_sha16": ORIGEM, "base_build_sha16": P["meta"]["um_py_base"], "v382_so_local_sha16": ORIGEM,
    "n_patches": P["meta"]["n_patches"], "kernel": P["meta"]["kernel"], "bandeiras": FLAGS, "preregistro_sha256": P["meta"]["preregistro_sha256"],
    "homonimos_novos": P["meta"]["homonimos_novos"],
    "escada_v381": [core0["external_ladder"]["n_theorems_clean"], core0["external_ladder"]["n_theorems_expected"]],
    "escada_esperada_v383": core0["external_ladder"]["n_theorems_clean"] + len(FLAGS),
    "axiom_report_v381": len(core0["kernel_formalization"]["axiom_report"]), "axiom_report_sandbox": sbx["n_axiom_report"],
    "vereditos_v383_do_ensaio": {k: ce[k] for k in NOVOS},
    "kernel_frontier_v381": {k: fr0.get(k) for k in ("remaining", "closed_by_citation_v374", "remaining_after_citation_v374")},
    "the_iald_index_v381": {"verdict": V("the_iald_index"), "n_ausentes": core0["the_iald_index"]["n_ausentes"]},
    "not_sealed_formais_v381": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []),
    "qg_closure_verdict_v381": selo0.get("qg_closure_verdict"),
    "vereditos_pinados_v381": {k: V(k) for k in pin_keys},
    "um_py_v381_sha16": h16(BK["um.py"]),
    "md_carimbo": "**Versão v383**", "md_todos_os_modulos": "TODOS OS MODULOS COM VEREDITO",
    "n_modulos_md_esperado": sum(1 for _m in core0.values() if isinstance(_m, dict) and (_m.get("verdict") or _m.get("status"))) + len(NOVOS),
    "beta_v381": core0["beta"], "alpha_v381": core0["alpha"], "omega_I_v381": core0["omega_I"],
    "bancada_sha16_bytes": {f: h16(os.path.join(BC, f)) for f in sorted(os.listdir(BC)) if f.endswith(".json")},
    "coma_keys_pinned": {k: pred0.get(k) for k in ("flow_layer_status", "flow_layer_status_v377", "flow_layer_kernel_v378")},
    "selo_leituras_pinadas": {k: selo0.get(k) for k in ("the_dissipation_law_reading_v377", "the_contrast_and_deviation_reading_v378", "the_elementary_reason_reading_v379",
                                                        "the_bancada_fases_5_6_7_reading_v380", "the_matrix_rule_reading_v381")},
    "selo_chaves_ev06": ["joint_coincidence_result_v3_verdict", "d1_camb_v3_real_v366_verdict"],
    "bandeiras_antigas": OLD_FLAGS, "per_nat_cost_D1b_v378": (core0.get("the_dissipation_law_with_contrast_v378") or {}).get("per_nat_cost_D1b"),
    "ensaio_markdown_v383": ens.get("markdown_v376"), "ensaio_manifest_v383": ens.get("manifest_v376"),
}
assert esp["kernel_frontier_v381"]["remaining"] and len(esp["kernel_frontier_v381"]["remaining"]) == 2
assert esp["kernel_frontier_v381"]["remaining_after_citation_v374"] == []
assert all(esp["vereditos_pinados_v381"][k] for k in ("tetelestai_conference_v376", "the_dissipation_law_v377", "the_elementary_reason_v379", "bancada_fases_5_6_7_v380", "the_matrix_rule_v381",
                                                     "final_verdict_machine", "coma_distance_dephasing", "void_floor_v11", "clock_test_result_v369", "neutrino_m2"))
assert len(esp["kernel"]["new"]) == 2 and len(esp["bandeiras_antigas"]) == 92 and all(esp["selo_leituras_pinadas"].values()) and all(esp["coma_keys_pinned"].values()) and esp["per_nat_cost_D1b_v378"]
assert all(k in selo0 for k in esp["selo_chaves_ev06"])
json.dump(esp, open(os.path.join(HERE, "ESPERADOS_v383.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in esp.items() if k not in ("bandeiras", "vereditos_pinados_v381", "kernel", "bandeiras_antigas", "bancada_sha16_bytes", "vereditos_v383_do_ensaio")}, ensure_ascii=False, indent=1)[:2500])
print("ESPERADOS_v383.json:", {k: esp[k] for k in ("candidato_sha16", "origem_sha16", "base_build_sha16", "escada_esperada_v383", "n_modulos_md_esperado")}, "| bandeiras antigas", len(OLD_FLAGS), "| pinados", len(pin_keys))
