# -*- coding: utf-8 -*-
"""gerar_esperados_v380_base_v379.py (tentativa 2: a base v379 lida dos BACKUPS do instalador, porque o core do disco era o da tentativa 1) -- grava ESPERADOS_v380.json LENDO os artefatos (nada digitado): candidato, ensaio e o selo v379 (canonico). SEM kernel novo:
a escada, o relatorio de axiomas e TODAS as bandeiras ext_* ficam como estao (v379)."""
import hashlib, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
V9 = os.path.join(os.path.dirname(HERE), "v379")
CACHE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache"
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
cand = os.path.join(HERE, "um_v380_candidato.py")
P = json.load(open(os.path.join(HERE, "patches_v380.json"), encoding="utf-8"))
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v380.json"), encoding="utf-8"))
E9 = json.load(open(os.path.join(V9, "ESPERADOS_v379.json"), encoding="utf-8"))
R0 = json.load(open(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json.bak_20261001_173616", encoding="utf-8")); core0 = R0["core"]
selo0 = json.load(open(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json.bak_20261001_173616", encoding="utf-8"))
UMBASE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py.bak_20261001_173616"; assert h16(UMBASE) == P["meta"]["um_py_base"], "o backup nao e a base do candidato"
assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == h16(cand)
assert P["meta"]["kernel"]["unchanged"] is True and P["meta"]["n_bandeiras"] == 0
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
pin_keys = list(E9["vereditos_pinados_v378"].keys()) + ["the_elementary_reason_v379"]
pin_keys = list(dict.fromkeys(pin_keys))
NOVOS = ("bancada_fases_5_6_7_v380",)
fr0 = ((core0.get("qg_closure") or {}).get("gate") or {}).get("kernel_frontier") or {}
ce = ens["core_ensaio"]
assert "KMS_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_AT_DELAY_LAW" in ce["bancada_fases_5_6_7_v380"] and ce["bancada_fases_5_6_7_v380"].endswith("__NOT_A_CONFIRMATION__GATE_UNTOUCHED")
BC = os.path.join(CACHE, "bancada_01out")
pred0 = (core0.get("coma_distance_dephasing") or {}).get("prediction") or {}
ALL_FLAGS = sorted(k for k in (core0.get("kernel_formalization") or {}) if k.startswith(("ext_pir_", "ext_dis_", "ext_dlc_", "ext_ter_")))
KT = os.path.join(NOS, "tgl_kernel")
arq16 = lambda rel: hashlib.sha256(open(os.path.join(KT, *rel.split("/")), "r", encoding="utf-8", newline="").read().encode("utf-8")).hexdigest()[:16]
esp = {
    "candidato_sha16": h16(cand), "candidato_bytes": os.path.getsize(cand), "origem_sha16": P["meta"]["um_py_base"],
    "n_patches": P["meta"]["n_patches"], "kernel": P["meta"]["kernel"], "bandeiras": [],
    "escada_v379": [core0["external_ladder"]["n_theorems_clean"], core0["external_ladder"]["n_theorems_expected"]],
    "escada_esperada_v380": core0["external_ladder"]["n_theorems_clean"],
    "axiom_report_v379": len(core0["kernel_formalization"]["axiom_report"]), "axiom_report_sandbox": len(core0["kernel_formalization"]["axiom_report"]),
    "kernel_pinado_sha16": {rel: arq16(rel) for rel in ("TGLExt.lean", "TGL/Audit.lean", "TGLExt/TheElementaryReason.lean", "TGLExt/TheFlowLawContrast.lean")},
    "vereditos_v380_do_ensaio": {k: ce[k] for k in NOVOS},
    "kernel_frontier_v379": {k: fr0.get(k) for k in ("remaining", "closed_by_citation_v374", "remaining_after_citation_v374")},
    "the_iald_index_v379": {"verdict": V("the_iald_index"), "n_ausentes": core0["the_iald_index"]["n_ausentes"]},
    "not_sealed_formais_v379": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []),
    "qg_closure_verdict_v379": selo0.get("qg_closure_verdict"),
    "vereditos_pinados_v379": {k: V(k) for k in pin_keys},
    "um_py_v379_sha16": h16(UMBASE),
    "md_carimbo": "**Versão v380**", "md_todos_os_modulos": "TODOS OS MODULOS COM VEREDITO",
    "n_modulos_md_esperado": sum(1 for _m in core0.values() if isinstance(_m, dict) and (_m.get("verdict") or _m.get("status"))) + len(NOVOS),
    "beta_v379": core0["beta"], "alpha_v379": core0["alpha"], "omega_I_v379": core0["omega_I"],
    "bancada_sha16_bytes": {f: h16(os.path.join(BC, f)) for f in sorted(os.listdir(BC)) if f.endswith(".json")},
    "coma_keys_pinned": {k: pred0.get(k) for k in ("flow_layer_status", "flow_layer_status_v377", "flow_layer_kernel_v378")},
    "selo_leituras_pinadas": {k: selo0.get(k) for k in ("the_dissipation_law_reading_v377", "the_contrast_and_deviation_reading_v378", "the_elementary_reason_reading_v379")},
    "selo_chaves_ev06": ["joint_coincidence_result_v3_verdict", "d1_camb_v3_real_v366_verdict"],
    "bandeiras_antigas": ALL_FLAGS,
    "ensaio_markdown_v380": ens.get("markdown_v376"), "ensaio_manifest_v380": ens.get("manifest_v376"),
}
assert esp["kernel_frontier_v379"]["remaining"] and len(esp["kernel_frontier_v379"]["remaining"]) == 2 and len(ALL_FLAGS) == 68
out = os.path.join(HERE, "ESPERADOS_v380.json")
json.dump(esp, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ESPERADOS_v380.json:", {k: esp[k] for k in ("candidato_sha16", "origem_sha16", "escada_esperada_v380", "n_modulos_md_esperado")}, "| bandeiras antigas", len(ALL_FLAGS), "| pinados", len(pin_keys))
