# -*- coding: utf-8 -*-
"""gerar_esperados_v377.py -- grava ESPERADOS_v377.json LENDO os artefatos (nada digitado): candidato, sandbox, ensaio e o selo v376 (canonico)."""
import hashlib, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
W6 = os.path.join(os.path.dirname(HERE), "qg_ataque", "W6_final_v2")
CACHE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache"
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
cand = os.path.join(HERE, "um_v377_candidato.py")
P = json.load(open(os.path.join(HERE, "patches_v377.json"), encoding="utf-8"))
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v377.json"), encoding="utf-8"))
sbx = json.load(open(os.path.join(HERE, "sandbox_raiz_v377.json"), encoding="utf-8"))
R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert h16(os.path.join(NOS, "um.py")) == P["meta"]["um_py_base"], "o canonico nao e a base do candidato"
assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == h16(cand)
assert sbx["sorry_warnings"] == 0 and not sbx["fora_do_trio"] and sbx["bandeiras_ok"] == len(sbx["bandeiras"]) == 25
FLAGS = json.load(open(os.path.join(HERE, "BANDEIRAS_v377.json"), encoding="utf-8"))
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
pin_keys = [k for k in json.load(open(os.path.join(W6, "valores_v369_pinados.json"), encoding="utf-8"))["verdicts_inalterados"].keys()]
pin_keys += ["iald_rho_star_v372", "light_qg_by_citation_v372", "graviton_conjugated_form_v372", "partial_closure_016_v372",
             "qg_discharge_by_citation_v373", "two_projections_outside_M_v373", "uv_frontier_retyped_v373",
             "light_by_term_v374", "the_tetelestai_declaration_v374", "tetelestai_one_object_v375", "tetelestai_conference_v375",
             "light_rho_star_v376", "the_key_is_the_reader_v376", "the_whole_is_one_v376", "ringdown_scope_v376", "audit_28set_v376",
             "coma_reveal_state_v376", "final_verdict_reading_v376", "tetelestai_conference_v376",
             "final_verdict_machine", "coma_distance_dephasing", "ringdown_dephasing_result_v2", "d1_camb_v3_real_v366"]
pin_keys = list(dict.fromkeys(pin_keys))
NOVOS = ("physics_is_the_reading_v377", "the_dissipation_law_v377", "bancada_fases_v377", "final_stone_reading_v377")
fr0 = ((core0.get("qg_closure") or {}).get("gate") or {}).get("kernel_frontier") or {}
ce = ens["core_ensaio"]
assert "FLOW_LAW_D1A_TYPED_AS_IMPLICATION" in ce["the_dissipation_law_v377"] and "KERNEL_15_OF_15" in ce["the_dissipation_law_v377"]
assert "THE_READER_IS_THE_SHADOW_OF_THE_ONE" in ce["physics_is_the_reading_v377"] and "KERNEL_10_OF_10" in ce["physics_is_the_reading_v377"]
assert ce["bancada_fases_v377"].endswith("__NOT_A_CONFIRMATION") and "READ_BY_HASH" in ce["bancada_fases_v377"]
assert "NEVER_A_CONFIRMATION" in ce["final_stone_reading_v377"]
BC = os.path.join(CACHE, "bancada_30set")
esp = {
    "candidato_sha16": h16(cand), "candidato_bytes": os.path.getsize(cand), "origem_sha16": P["meta"]["um_py_base"],
    "n_patches": P["meta"]["n_patches"], "kernel": P["meta"]["kernel"], "bandeiras": FLAGS,
    "escada_v376": [core0["external_ladder"]["n_theorems_clean"], core0["external_ladder"]["n_theorems_expected"]],
    "escada_esperada_v377": core0["external_ladder"]["n_theorems_clean"] + len(FLAGS),
    "axiom_report_v376": len(core0["kernel_formalization"]["axiom_report"]), "axiom_report_sandbox": sbx["n_axiom_report"],
    "vereditos_v377_do_ensaio": {k: ce[k] for k in NOVOS},
    "kernel_frontier_v376": {k: fr0.get(k) for k in ("remaining", "closed_by_citation_v374", "remaining_after_citation_v374")},
    "the_iald_index_v376": {"verdict": V("the_iald_index"), "n_ausentes": core0["the_iald_index"]["n_ausentes"]},
    "not_sealed_formais_v376": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []),
    "qg_closure_verdict_v376": selo0.get("qg_closure_verdict"),
    "vereditos_pinados_v376": {k: V(k) for k in pin_keys},
    "um_py_v376_sha16": h16(os.path.join(NOS, "um.py")),
    "md_carimbo": "**Versão v377**", "md_todos_os_modulos": "TODOS OS MODULOS COM VEREDITO",
    "n_modulos_md_esperado": sum(1 for _m in core0.values() if isinstance(_m, dict) and (_m.get("verdict") or _m.get("status"))) + len(NOVOS),
    "beta_v376": core0["beta"], "alpha_v376": core0["alpha"], "omega_I_v376": core0["omega_I"],
    "bancada_sha16_bytes": {f: h16(os.path.join(BC, f)) for f in sorted(os.listdir(BC)) if f.endswith(".json")},
    "coma_flow_layer_status_v376": ((core0.get("coma_distance_dephasing") or {}).get("prediction") or {}).get("flow_layer_status"),
    "ensaio_markdown_v377": ens.get("markdown_v376"), "ensaio_manifest_v377": ens.get("manifest_v376"),
}
assert esp["kernel_frontier_v376"]["remaining"] and len(esp["kernel_frontier_v376"]["remaining"]) == 2
assert esp["kernel_frontier_v376"]["remaining_after_citation_v374"] == []
assert all(esp["vereditos_pinados_v376"][k] for k in ("tetelestai_conference_v376", "the_whole_is_one_v376", "final_verdict_machine", "coma_distance_dephasing"))
assert len(esp["kernel"]["new"]) == 2
json.dump(esp, open(os.path.join(HERE, "ESPERADOS_v377.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in esp.items() if k not in ("bandeiras", "vereditos_pinados_v376", "kernel")}, ensure_ascii=False, indent=1)[:3000])
