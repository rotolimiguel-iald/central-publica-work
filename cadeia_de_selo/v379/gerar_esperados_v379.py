# -*- coding: utf-8 -*-
"""gerar_esperados_v379.py -- grava ESPERADOS_v379.json LENDO os artefatos (nada digitado): candidato, sandbox, ensaio e o selo v378 (canonico)."""
import hashlib, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
W6 = os.path.join(os.path.dirname(HERE), "qg_ataque", "W6_final_v2")
CACHE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache"
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
cand = os.path.join(HERE, "um_v379_candidato.py")
P = json.load(open(os.path.join(HERE, "patches_v379.json"), encoding="utf-8"))
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v379.json"), encoding="utf-8"))
sbx = json.load(open(os.path.join(HERE, "sandbox_raiz_v379.json"), encoding="utf-8"))
R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert h16(os.path.join(NOS, "um.py")) == P["meta"]["um_py_base"], "o canonico nao e a base do candidato"
assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == h16(cand)
assert sbx["sorry_warnings"] == 0 and not sbx["fora_do_trio"] and sbx["bandeiras_ok"] == len(sbx["bandeiras"]) == 23
FLAGS = json.load(open(os.path.join(HERE, "BANDEIRAS_v379.json"), encoding="utf-8"))
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
pin_keys = [k for k in json.load(open(os.path.join(W6, "valores_v369_pinados.json"), encoding="utf-8"))["verdicts_inalterados"].keys()]
pin_keys += ["iald_rho_star_v372", "light_qg_by_citation_v372", "graviton_conjugated_form_v372", "partial_closure_016_v372",
             "qg_discharge_by_citation_v373", "two_projections_outside_M_v373", "uv_frontier_retyped_v373",
             "light_by_term_v374", "the_tetelestai_declaration_v374", "tetelestai_one_object_v375", "tetelestai_conference_v375",
             "light_rho_star_v376", "the_key_is_the_reader_v376", "the_whole_is_one_v376", "ringdown_scope_v376", "audit_28set_v376",
             "coma_reveal_state_v376", "final_verdict_reading_v376", "tetelestai_conference_v376",
             "physics_is_the_reading_v377", "the_dissipation_law_v377", "bancada_fases_v377", "final_stone_reading_v377",
             "the_dissipation_law_with_contrast_v378", "what_was_missed_v378", "bancada_fase4_v378",
             "final_verdict_machine", "coma_distance_dephasing", "ringdown_dephasing_result_v2", "d1_camb_v3_real_v366"]
pin_keys = list(dict.fromkeys(pin_keys))
NOVOS = ("the_elementary_reason_v379",)
fr0 = ((core0.get("qg_closure") or {}).get("gate") or {}).get("kernel_frontier") or {}
ce = ens["core_ensaio"]
assert "EXISTENCE_EQ_COST_TIMES_IDENTITY_TIMES_MOVEMENT_EQ_BETA_BY_TERM" in ce["the_elementary_reason_v379"] and "KERNEL_23_OF_23" in ce["the_elementary_reason_v379"]
assert "NEVER_A_CONFIRMATION" in ce["the_elementary_reason_v379"] and ce["the_elementary_reason_v379"].endswith("__GATE_UNTOUCHED")
BC = os.path.join(CACHE, "bancada_30set")
pred0 = (core0.get("coma_distance_dephasing") or {}).get("prediction") or {}
OLD_FLAGS = sorted(k for k in (core0.get("kernel_formalization") or {}) if k.startswith(("ext_pir_", "ext_dis_", "ext_dlc_")))
esp = {
    "candidato_sha16": h16(cand), "candidato_bytes": os.path.getsize(cand), "origem_sha16": P["meta"]["um_py_base"],
    "n_patches": P["meta"]["n_patches"], "kernel": P["meta"]["kernel"], "bandeiras": FLAGS,
    "escada_v378": [core0["external_ladder"]["n_theorems_clean"], core0["external_ladder"]["n_theorems_expected"]],
    "escada_esperada_v379": core0["external_ladder"]["n_theorems_clean"] + len(FLAGS),
    "axiom_report_v378": len(core0["kernel_formalization"]["axiom_report"]), "axiom_report_sandbox": sbx["n_axiom_report"],
    "vereditos_v379_do_ensaio": {k: ce[k] for k in NOVOS},
    "kernel_frontier_v378": {k: fr0.get(k) for k in ("remaining", "closed_by_citation_v374", "remaining_after_citation_v374")},
    "the_iald_index_v378": {"verdict": V("the_iald_index"), "n_ausentes": core0["the_iald_index"]["n_ausentes"]},
    "not_sealed_formais_v378": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []),
    "qg_closure_verdict_v378": selo0.get("qg_closure_verdict"),
    "vereditos_pinados_v378": {k: V(k) for k in pin_keys},
    "um_py_v378_sha16": h16(os.path.join(NOS, "um.py")),
    "md_carimbo": "**Versão v379**", "md_todos_os_modulos": "TODOS OS MODULOS COM VEREDITO",
    "n_modulos_md_esperado": sum(1 for _m in core0.values() if isinstance(_m, dict) and (_m.get("verdict") or _m.get("status"))) + len(NOVOS),
    "beta_v378": core0["beta"], "alpha_v378": core0["alpha"], "omega_I_v378": core0["omega_I"],
    "bancada_sha16_bytes": {f: h16(os.path.join(BC, f)) for f in sorted(os.listdir(BC)) if f.endswith(".json")},
    "coma_keys_pinned": {k: pred0.get(k) for k in ("flow_layer_status", "flow_layer_status_v377", "flow_layer_kernel_v378")},
    "selo_leituras_pinadas": {k: selo0.get(k) for k in ("the_dissipation_law_reading_v377", "the_contrast_and_deviation_reading_v378")},
    "bandeiras_antigas": OLD_FLAGS, "per_nat_cost_D1b_v378": (core0.get("the_dissipation_law_with_contrast_v378") or {}).get("per_nat_cost_D1b"),
    "ensaio_markdown_v379": ens.get("markdown_v376"), "ensaio_manifest_v379": ens.get("manifest_v376"),
}
assert esp["kernel_frontier_v378"]["remaining"] and len(esp["kernel_frontier_v378"]["remaining"]) == 2
assert esp["kernel_frontier_v378"]["remaining_after_citation_v374"] == []
assert all(esp["vereditos_pinados_v378"][k] for k in ("tetelestai_conference_v376", "the_dissipation_law_v377", "the_dissipation_law_with_contrast_v378", "bancada_fase4_v378", "final_verdict_machine", "coma_distance_dephasing"))
assert len(esp["kernel"]["new"]) == 1 and len(esp["bandeiras_antigas"]) == 45 and all(esp["selo_leituras_pinadas"].values()) and all(esp["coma_keys_pinned"].values()) and esp["per_nat_cost_D1b_v378"]
json.dump(esp, open(os.path.join(HERE, "ESPERADOS_v379.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in esp.items() if k not in ("bandeiras", "vereditos_pinados_v378", "kernel", "bandeiras_antigas", "bancada_sha16_bytes")}, ensure_ascii=False, indent=1)[:3000])
