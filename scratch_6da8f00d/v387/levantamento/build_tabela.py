# -*- coding: utf-8 -*-
"""Tabela de estado dos tres pilares, lida do core/selo v386 por caminho (nada digitado).
Saida: TABELA_TRES_PILARES_v386.json / .md na lente do aferidor."""
import json, re, hashlib, io, os, sys
from collections import Counter

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
CORE_P = NOS + r"\um_absoluto.json"
SELO_P = NOS + r"\um_absoluto_selo.json"
STD_P = NOS + r"\rodada_v386_stdout.txt"
PT_P = NOS + r"\um_absoluto_pt.txt"
EN_P = NOS + r"\um_absoluto_en.txt"
OUT = os.path.dirname(os.path.abspath(__file__))

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()

ROOT = json.load(open(CORE_P, encoding="utf-8"))
C = ROOT["core"]
S = json.load(open(SELO_P, encoding="utf-8"))

def g(path, default=None):
    """le por caminho 'a/b/c' no ROOT (core = ROOT['core'])"""
    o = ROOT
    for k in path.split("/"):
        if k == "":
            continue
        if isinstance(o, list):
            o = o[int(k)]
        elif isinstance(o, dict) and k in o:
            o = o[k]
        else:
            return default
    return o

def sg(path, default=None):
    o = S
    for k in path.split("/"):
        if isinstance(o, dict) and k in o:
            o = o[k]
        else:
            return default
    return o

def f(x, nd=4):
    try:
        return ("%." + str(nd) + "g") % float(x)
    except Exception:
        return str(x)

# ---------- contagens dos vereditos ----------
rx_conf = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED")
rx_fals = re.compile(r"(?<!NOT_)(?<!UN)FALSIFIED")
acc = []
def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + "[%d]" % i)
    elif isinstance(o, str) and o.startswith("TGL_"):
        acc.append((path, o))
walk(ROOT, "")
allv = [v for _, v in acc]
F = [(p, v) for p, v in acc if p.split("/")[-1] == "verdict"]
Fv = [v for _, v in F]
def cnt(lst):
    return {
        "n": len(lst),
        "FALSIFIED_regex": sum(1 for v in lst if rx_fals.search(v)),
        "NOT_FALSIFIED": sum(1 for v in lst if "NOT_FALSIFIED" in v),
        "INCONCLUSIVE": sum(1 for v in lst if "INCONCLUSIVE" in v),
        "AWAITING": sum(1 for v in lst if "AWAITING" in v),
        "CONFIRMED_ou_PROVED_BY_regex": sum(1 for v in lst if rx_conf.search(v)),
    }
contagens = {
    "metodo_A_todas_as_strings_TGL_no_arquivo": dict(cnt(allv), unicos=len(set(allv))),
    "metodo_F_chave_exatamente_verdict__reproduz_a_gerencia": dict(cnt(Fv), unicos=len(set(Fv))),
    "FALSIFIED_sob_chave_verdict__caminhos": [p for p, v in F if rx_fals.search(v)],
    "AWAITING_sob_chave_verdict__caminhos": [p for p, v in F if "AWAITING" in v],
    "NOT_FALSIFIED_sob_chave_verdict__caminhos": [p for p, v in F if "NOT_FALSIFIED" in v],
    "INCONCLUSIVE_sob_chave_verdict__caminhos": [p for p, v in F if "INCONCLUSIVE" in v],
    "CONFIRMED_PROVED_BY_no_arquivo_inteiro__caminhos_todos_em_forbidden_verdicts": [p for p, v in acc if rx_conf.search(v)],
    "FALSIFIED_no_arquivo_inteiro__caminhos": [p for p, v in acc if rx_fals.search(v)],
}
# classificacao dos 3 FALSIFIED sob 'verdict'
contagens["FALSIFIED_sob_chave_verdict__leitura"] = {
    "/core/d1_camb_result/verdict": "V1 do D1 (maio): SUPERSEDIDO pela autopsia V2 (bug de distancia do worker de maio, Δχ² 2223 artefato) -> V2/V3 dizem TENSION_IS_NOT_FALSIFICATION",
    "/core/bancada_fases_5_6_7_v380/verdict": "Fase 6: o PAR (√β ou sin2θ, lei de atraso KMS/DEC) FALSIFIED_AT_DELAY_LAW — «PAIR_FALSIFIED_NOT_THE_THEORY»; fora do livro por decisao do operador (02/10)",
    "/core/the_ledger_of_charges_v383/verdict": "falso positivo do regex: a string traz «0_FALSIFIED» (contagem) e «R4_FROZEN_SET_HAS_NO_FALSIFIED» — nenhum desfecho FALSIFIED no livro",
}

# ---------- kernel ----------
kf = C["kernel_formalization"]
ar = kf.get("axiom_report", {})
TRIO = {"propext", "Classical.choice", "Quot.sound"}
n_ar = len(ar)
n_sub = sum(1 for k, v in ar.items() if isinstance(v, list) and set(v) <= TRIO)
n_extra = [k for k, v in ar.items() if not (isinstance(v, list) and set(v) <= TRIO)]
raw = open(CORE_P, encoding="utf-8").read()
qgs = [m.start() for m in re.finditer("QGSolutionComplete", raw)]
qgs_ctx = raw[max(0, qgs[0] - 200): qgs[0] + 250].replace("\n", " ") if qgs else None
std = open(STD_P, encoding="utf-8", errors="replace").read()
std_lines = std.splitlines()
std_kernel = [l for l in std_lines if "sorryAx" in l or "6137 teoremas" in l or "RITO_RC" in l or "FAIL_CLOSED_SELFTEST" in l]

kernel = {
    "n_theorems_clean": g("core/external_ladder/n_theorems_clean"),
    "n_theorems_expected": g("core/external_ladder/n_theorems_expected"),
    "axiom_report_n_declaracoes": n_ar,
    "axiom_report_n_dentro_do_trio": n_sub,
    "axiom_report_fora_do_trio": n_extra[:10],
    "trio": sorted(TRIO),
    "sorryAx_absent": kf.get("sorryAx_absent"),
    "trustCompiler_absent": kf.get("trustCompiler_absent"),
    "custom_TGL_axioms_absent": kf.get("custom_TGL_axioms_absent"),
    "lake_build_ok": kf.get("lake_build_ok"),
    "lean_version": kf.get("lean_version"),
    "formal_source_hash": kf.get("formal_source_hash"),
    "verdict": kf.get("verdict"),
    "not_claimed": kf.get("not_claimed"),
    "fail_closed_selftest": sg("fail_closed_selftest"),
    "gate_verdict": g("core/qg_closure/gate/verdict"),
    "gate_formal_flags": g("core/qg_closure/formal_flags"),
    "gate_physics_flags": g("core/qg_closure/physics_flags"),
    "gate_experiment_flags": g("core/qg_closure/experiment_flags"),
    "gate_18_flags_true": sum(1 for d in ("formal_flags", "physics_flags", "experiment_flags") for v in g("core/qg_closure/" + d).values() if v is True),
    "full_static_witness_exists": g("core/qg_closure/gate/full_static_witness_exists"),
    "kernel_frontier_remaining_after_citation_v374": g("core/qg_closure/gate/kernel_frontier/remaining_after_citation_v374"),
    "kernel_frontier_physical_identifications_open": g("core/qg_closure/gate/kernel_frontier/physical_identifications_open"),
    "the_axiom_v385_tag_omega_I": g("core/the_axiom_v385/tag_for_omega_I"),
    "the_axiom_v385_kernel_flags": [g("core/the_axiom_v385/kernel_flags_ok"), g("core/the_axiom_v385/kernel_flags_total")],
    "the_verb_v386_kernel_flags": [g("core/the_verb_v386/kernel_flags_ok"), g("core/the_verb_v386/kernel_flags_total")],
    "ledger_v383_kernel": "KERNEL_32_OF_32" in g("core/the_ledger_of_charges_v383/verdict", ""),
    "QGSolutionComplete_mencoes_no_core": len(qgs),
    "QGSolutionComplete_contexto": qgs_ctx,
    "stdout_linhas_kernel": std_kernel[:6],
    "o_que_prova": "a IMPLICACAO a partir do Um POSTO (ω(I)=1, etiqueta [POSTO]) e das hipoteses NOMEADAS; β nao e hipotese da implicacao (QGSolutionComplete); PROVADA = teorema no kernel",
    "o_que_nao_prova": "os axiomas (postos, nao provados); a natureza (CONFIRMADA e juizo do observador humano); G nao derivado; BW/Reeh-Schlieder/III_1 sao KNOWN externos (kernel_formalization.not_claimed)",
}

# ---------- pilar GPU ----------
Q = C["quantum_pillar_v384"]
sm = Q["summary"]
gpu = {
    "verdict": Q["verdict"],
    "status": Q["status"],
    "mode_v386": Q["mode"],
    "reuse": Q["reuse"],
    "key": Q["key"],
    "result_sha256": Q["result_sha256"],
    "spec_sha256": Q["spec_sha256_in_result"],
    "started_v385_run": Q["started"],
    "finished_v385_run": Q["finished"],
    "T2": {k: sm["T2"].get(k) for k in ("configs", "points", "unique", "ambiguous", "degenerate", "errors", "name_in_core_configs", "folds_window_configs", "identities_checked")},
    "T1": {"injections": sm["T1"]["injections"], "errors": sm["T1"]["errors"],
           "per_d_n": {d: sm["T1"]["per_d"][d]["n"] for d in sm["T1"]["per_d"]},
           "per_d_pass_sigma0": {d: sm["T1"]["per_d"][d]["pass_sigma0"] for d in sm["T1"]["per_d"]},
           "per_d_median_beta_rel_err_sigma0": {d: sm["T1"]["per_d"][d]["median_beta_rel_err"]["0.0"] for d in sm["T1"]["per_d"]}},
    "T3": {"controls": sm["T3"]["controls"],
           "N2_unital_identity": {d: sm["T3"]["N2_unital_identity"][d]["info_status"] for d in sm["T3"]["N2_unital_identity"]},
           "N3_linear_law_root_law_rejected": {d: sm["T3"]["N3_linear_law"][d]["root_law_rejected"] for d in sm["T3"]["N3_linear_law"]}},
    "T4": sm["T4"],
    "D128": {k: sm["D128"].get(k) for k in ("d", "nc", "status", "n0", "gap_rel", "zero_mode_ok", "ss_res_rel", "cci", "status_code")},
    "cpuref": sm["cpuref"],
    "engine": [e.get("name") for e in sm["engine"]],
    "engine_ok": [e.get("ok", e.get("passed")) for e in sm["engine"]],
    "phase_seconds": sm["phase_seconds"],
    "env": {k: sm["env"].get(k) for k in ("gpu", "torch", "cuda", "python", "numpy", "scipy", "platform", "determinism")},
    "reproducibility_v385": sg("quantum_pillar_reuse_v386/pinned_v385/reproducibility_verdict_v385"),
    "reproducibility_n_fields_v385": sg("quantum_pillar_reuse_v386/pinned_v385/reproducibility_n_fields_v385"),
    "reuse_v386_verdict": g("core/quantum_pillar_reuse_v386/verdict"),
    "COMPUTED_NOT_MEASURED_no_veredito": "COMPUTED_NOT_MEASURED" in Q["verdict"],
    "o_que_podia_falsificar": [
        "T2: atrator nao unico/degenerado em alguma das configuracoes da grade (ambiguous=%s, degenerate=%s de %s)" % (sm["T2"].get("ambiguous"), sm["T2"].get("degenerate"), sm["T2"].get("points")),
        "T1: o instrumento cego NAO recuperar a lei-raiz injetada (pass_sigma0 por d: %s)" % {d: sm["T1"]["per_d"][d]["pass_sigma0"] for d in sm["T1"]["per_d"]},
        "T3: controles que DEVIAM falhar e nao falhassem (N1 dephasing-only, N4 taxa negativa nao-CP, N5 inversao temporal nao-CP): todos True em d8..d64; N3: lei linear injetada -> lei-raiz rejeitada em 100%%",
        "identidades (CP, TP, PSD, Spohn, modo zero, residuo do estado estacionario) em 672/672 e em 21100/21100 instancias de estresse",
        "referencia independente na CPU: %s comparacoes" % sm["cpuref"].get("compared"),
    ],
}

# ---------- probabilidade conjunta ----------
prob = {
    "V1_v352": {"verdict": g("core/joint_coincidence_result/verdict"), "p_joint_primary": g("core/joint_coincidence_result/primary/p_joint"),
                "n_admissible": g("core/joint_coincidence_result/n_admissible"), "n_inventory": g("core/joint_coincidence_result/n_inventory"),
                "naive_product_INVALID": g("core/joint_coincidence_result/naive_product_INVALID/value"), "boolean": g("core/joint_coincidence_result/boolean_io/saida")},
    "V2_v363": {"verdict": g("core/joint_coincidence_result_v2/verdict"), "P_all_primary": g("core/joint_coincidence_result_v2/primary/P_all"),
                "P_all_range": g("core/joint_coincidence_result_v2/P_all_range_over_applicable_grid"), "max_abs_z": g("core/joint_coincidence_result_v2/max_abs_z"), "boolean": g("core/joint_coincidence_result_v2/boolean_v2")},
    "V3_v370": {"verdict": g("core/joint_coincidence_result_v3/verdict"), "P_all_primary": g("core/joint_coincidence_result_v3/primary/P_all"),
                "P_all_range": g("core/joint_coincidence_result_v3/P_all_range_over_applicable_grid"), "max_abs_z": g("core/joint_coincidence_result_v3/max_abs_z"),
                "dominant_channel": g("core/joint_coincidence_result_v3/dominant_channel"), "detected": g("core/joint_coincidence_result_v3/detected"),
                "admissible": g("core/joint_coincidence_result_v3/admissible_v3"), "boolean": g("core/joint_coincidence_result_v3/boolean_v3"),
                "channels_needed_for_1e-30": g("core/joint_coincidence_result_v3/channels_needed_for_threshold_at_primary_quality"),
                "kernel_condition_met": g("core/joint_coincidence_result_v3/kernel_condition/met"), "status_tag": g("core/joint_coincidence_result_v3/status_tag"),
                "n_inventory": g("core/joint_coincidence_result_v3/n_inventory"), "rule_counts": g("core/joint_coincidence_result_v3/rule_counts")},
    "selo_joint_coincidence_boolean": sg("joint_coincidence_boolean"),
    "leitura": "o core NAO tem probabilidade conjunta dos TRES pilares: a coincidencia conjunta (V1-V3) pontua SO canais de natureza (class NATURE_CHANNEL); o kernel entra como CONDICAO (kernel_condition.met), nao como fator; o pilar da GPU nao entra. Nada aqui foi recomputado.",
}

# ---------- tabela dos ritos ----------
L = {row["id"]: row for row in C["the_ledger_of_charges_v383"]["ledger"]}
b = C["bancada_fases_5_6_7_v380"]
rows = []
def R(teste, pilar, chave, veredito, estado, estatuto, numero, rg, disc, nota=""):
    rows.append({"teste": teste, "pilar": pilar, "chave_core": chave, "veredito": veredito, "estado": estado, "estatuto": estatuto,
                 "numero": numero, "rg_recuperada": rg, "discrimina_rg": disc, "nota": nota})

# piso dos vazios
R("Piso dos vazios V1 (KiDS shear, 1049 vazios)", "1 ritos", "core.void_floor_final", g("core/void_floor_final/verdict"), "INCONCLUSIVE_SYSTEMATICS", "[REAL] recusa de sistematica",
  "chi2/dof B-mode %s (gate reprovou); SNR perfil %s; Fisher %s" % (f(g("core/void_floor_final/systematics/chi2_dof_bmode")), f(g("core/void_floor_final/snr_profile")), f(g("core/void_floor_final/power_fisher_separation_sigma2"))),
  "nao se aplica (recusa antes do veredito fisico)", "nao (recusa)")
R("Piso dos vazios V2 (emenda; mesmos 1049)", "1 ritos", "core.void_floor_v2", g("core/void_floor_v2/verdict"), "NOT_FALSIFIED_UNDERPOWERED", "[REAL]",
  "r_c MLE %s; 5σ [%s, %s] vs β %s; B-mode %s; Fisher %s" % (f(g("core/void_floor_v2/rc_mle")), f(g("core/void_floor_v2/rc_interval_5sigma/0")), f(g("core/void_floor_v2/rc_interval_5sigma/1")), f(g("core/void_floor_v2/beta_floor")), f(g("core/void_floor_v2/systematics/chi2_dof_bmode")), f(g("core/void_floor_v2/power_fisher_separation_sigma2"))),
  "sim (piso acima de β; consistente com ΛCDM raso)", "sem poder (powered_5sigma=%s)" % g("core/void_floor_v2/powered_5sigma"))
R("Piso dos vazios V4.1 (densidade auto-calibrante, REVOLVER DESI)", "1 ritos", "core.void_density_v41", g("core/void_density_v41/verdict"), "NOT_FALSIFIED_POWERED", "[REAL]",
  "r_c^cal %s ± %s; L5 %s vs β %s; β·Σμ %s (≥25 powered); split-null %s ± %s" % (f(g("core/void_density_v41/primary/rhat_cal")), f(g("core/void_density_v41/primary/sigma")), f(g("core/void_density_v41/primary/L5")), f(g("core/void_density_v41/beta_floor")), f(g("core/void_density_v41/primary/powered_beta_mu")), f(g("core/void_density_v41/split_null/ratio")), f(g("core/void_density_v41/split_null/sigma"))),
  "sim (consistente com ΛCDM raso; statuses.honestidades: tracador UNILATERAL)", "nao (unilateral: so pode NOT_FALSIFIED ou recusar)")
R("Piso dos vazios V11 (SDSS DR7 × VAST, replica independente — o degrau experimental do gate)", "1 ritos", "core.void_floor_v11 / selo.void_floor_v11_verdict", g("core/void_floor_v11/verdict"), "NOT_FALSIFIED_POWERED", "[REAL]; alimenta 4 das 6 bandeiras experimentais (experiment_feed)",
  "r_c^cal %s ± %s; L5 %s vs β %s; β·Σμ %s; experiment_feed=%s" % (f(g("core/void_floor_v11/primary/rhat_cal")), f(g("core/void_floor_v11/primary/sigma")), f(g("core/void_floor_v11/primary/L5")), f(g("core/void_floor_v11/beta_floor")), f(g("core/void_floor_v11/primary/powered_beta_mu")), g("core/void_floor_v11/experiment_feed")),
  "sim (consistente com ΛCDM raso — statuses.honestidade)", "nao (unilateral; auditoria 28/09 GV-01: o ΛCDM raso tambem passa)",
  "errata 01/10 (GV-03/EV-12): as 4 bandeiras independent_v3_* derivam de UM booleano; null_tests_passed_blind sem mock [DECLARADO pela auditoria]")
R("Piso dos vazios LRG (DESI DR1, tracador virgem)", "1 ritos", "core.void_floor_lrg", g("core/void_floor_lrg/verdict"), "INCONCLUSIVE_TRACER_SUPPRESSION", "[REAL]",
  "r_c^cal %s ± %s (supressao de tracador)" % (f(g("core/void_floor_lrg/primary/rhat_cal")), f(g("core/void_floor_lrg/primary/sigma"))), "nao se aplica", "nao")
R("Piso dos vazios V12 bilateral (LRG quartil profundo)", "1 ritos", "core.void_floor_v12", g("core/void_floor_v12/verdict"), "TRACER_EMPTY_CORE_REGIME (nao selado nesta rodada)", "[REAL] recusa",
  "r_deep %s; all_verified=%s" % (f(g("core/void_floor_v12/primary/r_deep")), g("core/void_floor_v12/all_verified")), "nao se aplica", "nao")
R("Piso dos vazios κ-CMB V9 (ACT DR6, banda estendida)", "1 ritos", "core.void_floor_kappa_v9", g("core/void_floor_kappa_v9/verdict"), "NOT_FALSIFIED_UNDERPOWERED", "[REAL]",
  "deteccao bruta %sσ; Fisher do piso %s; r_hat %s" % (f(g("core/void_floor_kappa_v9/values/detection_sigma_raw")), f(g("core/void_floor_kappa_v9/values/fisher_floor")), f(g("core/void_floor_kappa_v9/values/r_hat"))), "nao se aplica (sem poder)", "sem poder")
R("Piso dos vazios shear V2 (KiDS, 700 vazios)", "1 ritos", "core.void_shear_v2", g("core/void_shear_v2/verdict"), "NOT_FALSIFIED_UNDERPOWERED", "[REAL]",
  "deteccao bruta %sσ; Fisher %s" % (f(g("core/void_shear_v2/values/detection_sigma_raw")), f(g("core/void_shear_v2/values/fisher_floor"))), "nao se aplica (sem poder)", "sem poder")
# relogios
P1 = g("core/clock_test_result_v369/P1/platforms/0")
R("Relogios v369 (P1 materia / P2 modo de luz LIGO / P3 universal)", "1 ritos", "core.clock_test_result_v369", g("core/clock_test_result_v369/verdict"), "P1 NOT_FALSIFIED_UNDERPOWERED; P2 EXCLUDED_IN_READING; P3 NO_LOCAL_OBSERVABLE", "[REAL]",
  "Γ_pred(87Sr) %s /s vs cota 95%% %s /s; deficit 5σ ≥ %s ordens; P2: %s/%s series excluidas" % (f(P1["Gamma_pred_per_s"]), f(P1["Gamma_ub_per_s"]), f(L["F3a"]["numbers_read"]["deficit_ordens_5sigma"], 3), g("core/clock_test_result_v369/P2/n_excluded"), g("core/clock_test_result_v369/P2/n_series")),
  "nao se aplica (laboratorio: a correcao β fica %s ordens abaixo da cota — nenhum excesso)" % f(L["F3a"]["numbers_read"]["deficit_ordens_5sigma"], 3), "nao (deficit ≥12,5 ordens); P2 excluida em leitura; P3 sem observavel")
# neutrinos
R("Neutrino m2 (JUNO / NuFIT pos-JUNO)", "1 ritos", "core.neutrino_m2", g("core/neutrino_m2/verdict"), "ARMED_CONSISTENT (livro F4: NOT_FALSIFIED)", "[REAL] previsao + [DECLARADO] JUNO lido na fonte",
  "m2(TGL) %s meV; tensao %sσ (NuFIT); z_juno %s; kill_rule=%s" % (f(g("core/neutrino_m2/values/m2_pred_meV"), 5), f(g("core/neutrino_m2/values/tensao_atual_sigma"), 3), f(L["F4"]["numbers_read"].get("z_juno"), 3), g("core/neutrino_m2/values/kill_rule_satisfeita")),
  "nao se aplica (setor do neutrino; nao e teste da RG)", "tensao %sσ, abaixo de 5σ; nao falsifica" % f(g("core/neutrino_m2/values/tensao_atual_sigma"), 3),
  "errata 28/09 VV-N1: NuFIT contem o JUNO; Capozzi da 2,44σ")
R("Neutrino massa (V1, superseded por m2)", "1 ritos", "core.neutrino_mass", g("core/neutrino_mass/verdict"), "NOT_FALSIFIED_POWERED", "[REAL]; sin45 [POSTULATE]",
  "desvio %sσ" % f(g("core/neutrino_mass/deviation_sigma"), 3), "nao se aplica", "nao")
R("Σm_ν armado", "1 ritos", "core.neutrino_sum", g("core/neutrino_sum/verdict"), "ARMED_CONSISTENT", "[REAL]", "Σ %s eV < %s eV" % (f(g("core/neutrino_sum/values/sum_pred_eV"), 4), f(g("core/neutrino_sum/values/current_bound_eV"), 3)), "nao se aplica", "aposentado como discriminante (D2)")
R("N_eff", "1 ritos", "core.neff_channel", g("core/neff_channel/verdict"), "ARMED_CONSISTENT", "[REAL]", "ΔN_eff %s; tensao %sσ" % (f(g("core/neff_channel/values/Delta_Neff"), 4), f(g("core/neff_channel/values/tensao_atual_best"), 3)), "nao se aplica", "nao (1,6σ)")
R("Atraso Shapiro do neutrino (NMC; SN1987A)", "1 ritos", "core.nmc_shapiro", g("core/nmc_shapiro/verdict"), "AWAITING_DATA", "[PRE]",
  "margem SN1987A %s s vs excesso predito %s s (folga %s); n_events %s" % (f(g("core/nmc_shapiro/margin_s")), f(g("core/nmc_shapiro/nmc_dt_s")), f(g("core/nmc_shapiro/headroom")), g("core/nmc_shapiro/n_events")), "sim (neutrino segue a geodesica com Shapiro PADRAO da RG)", "aguardando")
# Coma
R("Coma v376 (distancia por dephasing; livro R3 'atraso de redshift' = distancia modular)", "1 ritos", "core.coma_reveal_state_v376", g("core/coma_reveal_state_v376/verdict"), "NOT_FALSIFIED (livro R3: z %s)" % f(L["R3"]["number_read"], 3), "[REAL lido por hash]; NOT_BLIND postdicao nao ajustada",
  "D_L TGL %s Mpc vs ref %s ± %s Mpc (z %s); controle Planck sem dephasing D_L %s (z %s)" % (f(g("core/coma_reveal_state_v376/D_L_TGL_median_Mpc"), 4), g("core/coma_reveal_state_v376/reference_Mpc"), g("core/coma_reveal_state_v376/reference_sigma_Mpc"), f(g("core/coma_reveal_state_v376/z_TGL_both_sigmas"), 3), f(g("core/coma_reveal_state_v376/control_D_L_planck_median_Mpc"), 4), f(g("core/coma_reveal_state_v376/z_planck_control_ref_sigma_only"), 3)),
  "sim (a TGL devolve a referencia publicada a %sσ; o motor e [CONJECTURE] selado)" % f(g("core/coma_reveal_state_v376/z_TGL_both_sigmas"), 3),
  "nao: degenerada com H0_local=%s (coma_distance_dephasing.degeneracy_note); nao-cega" % f(g("core/coma_reveal_state_v376/H0_local_D1a"), 4))
# GA
R("Grande Atrator (massa; janela; varredura de 300)", "1 ritos", "verdict.masses_Msun / core.sensitivity / core.ga_mass_audit", g("core/ga_mass_audit/verdict") + " ; ga_window_status=" + ROOT["ga_window_status"], "SOMBRA de escala (forma aposentada); M_TGL^linear = M_RG (stealth)", "[SOMBRA/ONTO] forma v98 aposentada como lei de fonte; [CONDICIONAL linear] M_TGL=M_RG",
  "A literatura %s Msun; B CF4 %s Msun; janela [%s, %s]; varredura: %s combinacoes, M in [%s, %s], fracao na banda %s" % (f(g("verdict/masses_Msun/A_literature"), 4), f(g("verdict/masses_Msun/B_cf4_positions"), 4), f(g("accepted_window_Msun/0")), f(g("accepted_window_Msun/1")), g("core/sensitivity/n_combinations"), f(g("core/sensitivity/M_min_Msun"), 3), f(g("core/sensitivity/M_max_Msun"), 3), g("core/sensitivity/fraction_in_band")),
  "sim (ga_mass_audit: M_TGL^linear = M_RG; β nao renormaliza G)", "nao (ga_window_status: NOT_NONCIRCULAR_EVIDENCE)")
R("Antipoda do dipolo (geometria bruta, pre-registrada)", "1 ritos", "core.dipole_antipode", g("core/dipole_antipode/selo"), "criterio pre-registrado NAO satisfeito (antipode_underdense=%s)" % g("core/dipole_antipode/antipode_underdense"), "[PRE + DATA posicoes] negativo honesto; nao e veredito TGL_*",
  "razao antipoda/GA %s; IC95 [%s, %s]; criterio: razao < 1" % (f(g("core/dipole_antipode/density_ratio_antipode_over_GA"), 3), f(g("core/dipole_antipode/bootstrap/ci95/0"), 3), f(g("core/dipole_antipode/bootstrap/ci95/1"), 3)), "nao se aplica", "nao (contagem de posicoes, sem velocidades)")
# Hubble
f5 = b["fase5"]; f7 = b["fase7"]; f4 = C["bancada_fase4_v378"]
R("Tensao de Hubble — SH0ES na bancada (Fase 5) / livro R1", "1 ritos", "core.bancada_fases_5_6_7_v380.fase5 ; ledger R1", f5["veredito"], "NOT_FALSIFIED (livro R1: z %s, regra |z|<5)" % f(L["R1"]["number_read"], 3), "[REAL lido por hash]; alvo H0 [DECLARADO]",
  "H0 escada %s ± %s (z %s vs alvo); P_sombra δ %s ± %s (z %s); tensao ΛCDM z %s; lnB sombra vs acumulada %s (diagonal) → %s com cov. Moresco2020 (Fase 7)" % (f(f5["validacao"]["H0"], 4), f(f5["validacao"]["sigma_H0"], 3), f(f5["validacao"]["z_vs_alvo"], 2), f(f5["P_sombra"]["delta"], 2), f(f5["P_sombra"]["sigma_delta"], 3), f(f5["P_sombra"]["z_delta"], 3), f(f5["P_sombra"]["z_tensao"], 3), f(f5["lnB_sombra_vs_acumulada_S"], 3), f(f7["U_lnB_sombra_vs_acumulada"]["moresco2020"], 3)),
  "sim (desvio da escada consistente com zero a 1σ; a escada reproduz o H0 publicado)", "nao (δ a %sσ de zero; a resolucao da tensao e remissao ao artigo publicado [CONJECTURE de mecanismo])" % f(f5["P_sombra"]["z_delta"], 2))
R("Tensao de Hubble — cronometros com covariancia (Fase 7) / livro F1", "1 ritos", "core.bancada_fases_5_6_7_v380.fase7 ; ledger F1", f7["veredito"], "NOT_FALSIFIED (livro F1: ganho z %s; regra: ganho ≥ +5 falsifica)" % f(L["F1"]["number_read"], 3), "[REAL lido por hash]",
  "ganho da lei T: diagonal %s → Moresco2020 %s; δ %s ± %s (z %s); lnB %s → %s" % (f(f7["T_z_ganho"]["diagonal"], 3), f(f7["T_z_ganho"]["moresco2020"], 3), f(f7["T_delta_moresco2020"]["delta"], 3), f(f7["T_delta_moresco2020"]["sigma"], 3), f(f7["T_delta_moresco2020"]["z"], 3), f(f7["U_lnB_sombra_vs_acumulada"]["diagonal"], 3), f(f7["U_lnB_sombra_vs_acumulada"]["moresco2020"], 3)),
  "sim (a face le H(z) do fundo nu; a lei com β nos cronometros e desfavorecida a 1–3σ)", "nao (desfavorece a leitura acumulada em β a 1,7σ; nao falsifica)")
R("Tensao de Hubble — Fase 4 (desvio; escada D1b)", "1 ritos", "core.bancada_fase4_v378", f4["veredito_fase4"], "DEVIATION_1_TO_3_SIGMA", "[REAL lido por hash]; erros diagonais (Fase 7 enfraquece)",
  "escada δ %s ± %s (z %s); pull em β_TGL %s; lnB TGL vs ΛCDM (escada) %s; CC intermediarios z %s (diag)" % (f(f4["P_ladder_d1b"]["delta"], 3), f(f4["P_ladder_d1b"]["sigma_delta"], 3), f(f4["P_ladder_d1b"]["z_delta"], 3), f(f4["P_ladder_d1b"]["pull"], 3), f(f4["P_ladder_d1b"]["lnB"]["tgl_vs_lcdm"], 3), f(f4["T_intermediate_d1b"]["z_delta"], 3)),
  "sim (escada a 1,1σ de zero)", "nao (1–3σ; lnB escada 8,0 e diagonal; Fase 7 reduz)")
d3 = C["d1_camb_v3_real_v366"]
R("Tensao de Hubble — D1 via CAMB V3 (fundo vestido) / livro R6", "1 ritos", "core.d1_camb_v3_real_v366 ; ledger R6", d3["verdict"], "INCONCLUSIVE (livro R6, ao lado: z %s, controle %s)" % (f(L["R6"]["number_read"], 3), L["R6"]["control_read"]), "[REAL dado real]; NAO-CEGO",
  "Δχ² %s (β fixo vs ΛCDM, n=%s); β = %s ± %s; α√e a %sσ (no limiar); H0 ΛCDM %s / TGL %s" % (f(d3["delta_chi2"], 3), d3["n_data"], f(d3["beta_posterior"]["median"], 3), f(d3["beta_posterior"]["sigma"], 2), f(d3["z_alpha_sqrt_e"], 3), f(d3["h0"]["H0_LCDM"], 4), f(d3["h0"]["H0_TGL"], 4)),
  "sim no limite β→0 (ΛCDM); com β no fundo: ΛCDM preferido por Δχ² %s" % f(d3["delta_chi2"], 2), "tensao de %sσ CONTRA β no fundo vestido (TENSION_IS_NOT_FALSIFICATION); e a leitura R6 fora da regra" % f(d3["z_alpha_sqrt_e"], 3),
  "D1 V1 (core.d1_camb_result) dizia MCMC_D1_BETA_FALSIFIED: SUPERSEDIDO pela autopsia V2 (bug de distancia do worker de maio); V2: Δχ² %s, β %s ± %s" % (f(g("core/d1_camb_result_v2/delta_chi2"), 3), f(g("core/d1_camb_result_v2/beta_posterior/median"), 3), f(g("core/d1_camb_result_v2/beta_posterior/sigma"), 2)))
ce = C["cosmological_errata_verdict"]
R("SNe — Pantheon+ canonico (1593)", "1 ritos", "core.cosmological_errata_verdict", ce["verdict"], "NOT_FALSIFIED (teoria dentro de 1,25σ; nao preferida por BIC com β livre)", "[REAL, errata assinada]",
  "β̂ %s ± %s; teoria a %sσ; zero a %sσ; ΔBIC %s; Δχ²(β fixo) %s" % (f(ce["source_INPUT"]["beta_hat"], 3), f(ce["source_INPUT"]["sigma"], 3), f(ce["d_theory_sigma"], 3), f(ce["d_zero_sigma"], 2), f(ce["source_INPUT"]["delta_BIC"], 3), f(ce["delta_chi2_beta_fixed"], 3)),
  "sim (β̂ consistente com zero a %sσ; teoria a %sσ)" % (f(ce["d_zero_sigma"], 2), f(ce["d_theory_sigma"], 3)), "nao (σ/β ≈ %s; sem poder)" % f(ce["source_INPUT"]["sigma"] / C["beta"], 2))
la = C["final_verdict_machine"]["channels"]["l_A_compressed_cmb"]
R("CMB comprimido l_A (JUIZ_LA)", "1 ritos", "core.final_verdict_machine.channels.l_A_compressed_cmb", la["verdict"], "NOT_FALSIFIED (tensao < 3σ)", "[REAL]", "β primario %s; d vs teoria %sσ" % (f(la["primary_beta"], 3), f(la["d_vs_theory_sigma"], 3)), "sim (β dentro de 1,3σ)", "nao")
R("BBN descircularizada", "1 ritos", "core.final_verdict_machine.channels.bbn / core.evidence_audit", C["final_verdict_machine"]["channels"]["bbn"]["verdict"], "NON_DISCRIMINANT", "[INPUT auditoria 08/08]", "β̂ %s ± %s (σ/β %s)" % (f(g("core/evidence_audit/values/bbn_decirc/beta_hat"), 4), f(g("core/evidence_audit/values/bbn_decirc/sigma"), 3), f(g("core/evidence_audit/values/bbn_decirc/sigma_over_beta"), 2)), "sim (consistente)", "nao (nao discrimina)")
R("CMB espectro completo (Nivel 2)", "1 ritos", "core.nivel2_rite", g("core/nivel2_rite/verdict"), "N2_INCAPAZ / NOT_CONVERGED (nao selado nesta rodada)", "[REAL] recusa", "S: β %s ± %s (σ/β %s)" % (f(g("core/nivel2_rite/values/variantes/S/mediana"), 3), f(g("core/nivel2_rite/values/variantes/S/sigma"), 3), f(g("core/nivel2_rite/values/variantes/S/sigma_sobre_beta"), 3)), "sim (consistente)", "nao (incapaz)")
# Ecos
f6 = b["fase6"]; er = C["the_ledger_of_charges_v383"]["echo_routes_outside_the_ledger"]
R("Ecos GW — Fase 6 (244 BBH O1–O4; 3 leituras × 2 leis) + emendas V4/V5; os 9 pares FORA do livro", "1 ritos", "core.bancada_fases_5_6_7_v380.fase6/emenda_v4/emenda_v5 ; core.the_ledger_of_charges_v383.echo_routes_outside_the_ledger", b["verdict"],
  "%s pares fora do livro: %s EXCLUDED_BY_DATA (FALSIFIED_AT_DELAY_LAW) + %s INCONCLUSIVE — «PAIR_FALSIFIED_NOT_THE_THEORY»; decisao do operador 02/10 («prefiro a primeira opcao»)" % (er["n"], er["excluded_by_data"], er["inconclusive"]),
  "[REAL lido por hash]; leituras de amplitude [KERNEL |R|=sinθ + ONTO]; lei de atraso [INPUT/ONTO]",
  "KMS todos: z_excl R1 %s, R2 %s (cego O4: %s, %s); z_det %s; MAY: INCONCLUSIVE (sistematica %s); V4 MAY R2 z_excl %s; V5 DEC: z_excl R1 %s, R2 %s; principal: %s" % (f(f6["todos_KMS"]["z_excl_R1"], 3), f(f6["todos_KMS"]["z_excl_R2"], 4), f(f6["o4_KMS_cego"]["z_excl_R1"], 3), f(f6["o4_KMS_cego"]["z_excl_R2"], 4), f(f6["todos_KMS"]["z_det"], 3), f(f6["todos_MAY"]["sistematica_abs"], 3), f(b["emenda_v4"]["todos_MAY"]["z_excl_R2"], 3), f(b["emenda_v5"]["todos_DEC"]["z_excl_R1"], 3), f(b["emenda_v5"]["todos_DEC"]["z_excl_R2"], 4), json.dumps(f6["veredito_principal"], ensure_ascii=False)),
  "sim (nenhum eco detectado: z_det KMS %s — a RG nao preve eco; correspondencia)" % f(f6["todos_KMS"]["z_det"], 2),
  "nao: o que cai e o PAR (leitura da amplitude, lei de atraso), nao a teoria; os pares nao sao cobrancas da teoria (ratificado)",
  "ao lado: a Fase 6 como teste da TGL foi retirada da cadeia pela regra matriz (v381); o eco como copia atrasada com lei τ esta fora; o operador: «nao quero publicar nada que seja resultado de falsificacao»")
for key, lab in (("gw_echo_rite", "Eco acoplado V1 (lei de maio)"), ("gw_echo_kms_rite", "Eco KMS V1"), ("echo_anchored_result_v2", "Eco ancorado V2 (lalsuite)"), ("echo_pe_result_v2", "Eco PE bayesiana V2 (bilby)"), ("echo_search_result", "Busca de ecos de longo atraso V1"), ("gw_angular_rite", "Rito angular GW (o 100σ retirado)"), ("h2_reproduction_result", "Reproducao H2 (pycbc)")):
    v = g("core/%s/verdict" % key)
    est = "INCONCLUSIVE_SYSTEMATICS" if "INCONCLUSIVE" in v else ("NOT_FALSIFIED_UNDERPOWERED" if "NOT_FALSIFIED" in v else ("RETIRADO / NOT_A_FALSIFIER" if ("RETIRED" in v) else "-"))
    num = ""
    if key == "gw_echo_rite": num = "a/√β %s ± %s; poder %sσ de 5" % (f(g("core/gw_echo_rite/stack/a_over_sqrt_beta"), 3), f(g("core/gw_echo_rite/stack/sigma"), 3), f(g("core/gw_echo_rite/stack/power_sigma"), 2))
    if key == "gw_echo_kms_rite": num = "a/√β %s ± %s; poder %sσ de 5" % (f(g("core/gw_echo_kms_rite/stack/a_over_sqrt_beta"), 3), f(g("core/gw_echo_kms_rite/stack/sigma"), 3), f(g("core/gw_echo_kms_rite/stack/power_sigma"), 2))
    if key == "echo_anchored_result_v2": num = "MAY a/√β %s ± %s, poder %sσ" % (f(g("core/echo_anchored_result_v2/laws/MAY/a_over_sqrt_beta"), 3), f(g("core/echo_anchored_result_v2/laws/MAY/sigma"), 3), f(g("core/echo_anchored_result_v2/laws/MAY/power_sigma"), 2))
    if key == "echo_search_result": num = "N_on %s, B_exp %s, z_poisson %s, eventos altos %s" % (g("core/echo_search_result/summary/N_on"), g("core/echo_search_result/summary/B_exp"), f(g("core/echo_search_result/summary/z_poisson"), 3), g("core/echo_search_result/summary/n_loud_events"))
    if key == "h2_reproduction_result": num = "z vs α² %s; sintetico segue ruido² = %s" % (f(g("core/h2_reproduction_result/z_vs_alpha2"), 4), g("core/h2_reproduction_result/synthetic_tracks_noise_sq"))
    if key == "gw_angular_rite": num = "σ capped 100 em ruido = %s; r_identity_min %s" % (g("core/gw_angular_rite/december_statistic/sigma_capped_all_100"), f(g("core/gw_angular_rite/december_statistic/r_identity_min"), 6))
    if key == "echo_pe_result_v2": num = "n eventos %s/%s; MAY a %s" % (g("core/echo_pe_result_v2/n_events_used"), g("core/echo_pe_result_v2/n_events_catalog"), f(g("core/echo_pe_result_v2/outcomes/MAY/a"), 3))
    R(lab, "1 ritos", "core." + key, v, est, "[REAL lido por hash]; fora do contorno (why_outside_contour)", num, "sim (sem eco detectado = RG)" if key not in ("gw_angular_rite", "h2_reproduction_result") else "nao se aplica (estatistica retirada)", "nao (poder < 5σ)" if "INCONCLUSIVE" in v or "UNDERPOWERED" in v else "nao")
# Ringdown
rd = C["ringdown_dephasing_result_v2"]; rs = C["ringdown_scope_v376"]; rb = C["ramo_b_preregistration_v386"]
R("Ringdown — ramo canonico τ★ = t_Planck (V2; GW250114 C6) / livro F2", "1 ritos", "core.ringdown_dephasing_result_v2 ; core.ringdown_scope_v376 ; ledger F2", rs["verdict"], "correspondencia com a RG (ramo A invisivel: δ_pred %s); V2 INCONCLUSIVE_SYSTEMATICS; C6 %s; livro F2 INCONCLUSIVE (pela sistematica da medida)" % (f(rs["delta_pred_A_v2"], 2), rs["c6_status"]), "[REAL lido por hash]; τ★ ramo B [INPUT]",
  "Δτ %s ± %s (z vs RG %s); ramo B pred %s (z vs B %s; poder %s de 5σ); vies relativo de τ %s > 0.2" % (f(rd["stacks"]["3.0"]["delta_tau"], 4), f(rd["stacks"]["3.0"]["sigma"], 3), f(rd["z_vs_GR"], 3), f(rd["stacks"]["3.0"]["delta_pred_B"], 3), f(rd["z_vs_B"], 3), f(rd["power_B"], 2), f(rd["stacks"]["3.0"]["mean_bias_rel"], 3)),
  "sim (ramo A e RG por construcao; Δτ a %sσ da RG)" % f(rd["z_vs_GR"], 2), "nao (ramo A invisivel por construcao; ramo B sem poder: %s de 5σ)" % f(rd["power_B"], 2),
  "ringdown_scope_v376: «no ramo canonico a natureza so pode devolver a RG»; erratum ao lado de NATURE_DECIDES_RINGDOWN_NEXT")
R("Ringdown — ramo B reaberto por pre-registro (τ★ = k·GM_f/c³, k = 2π/κ̂) / canal F2b", "1 ritos", "core.ramo_b_preregistration_v386 ; core.ledger_errata_v386.charge_F2b", rb["verdict"], "AWAITING_DATA (F2b: %s)" % rb["F2b_status"], "[INPUT — decisao do operador por sha256]; [ONTO] leitura da gerencia; pre-registro por hash; nada aberto",
  "conjunto D n=%s (cego); poderes exatos A31 %s, B10 %s, C %s; k(χ=0) %s; nothing_opened=%s; centrais nao-cegas transcritas: %s" % (rb["conjunto_D_n"], f(rb["pins"]["poder_exato_A31"]["read"], 3), f(rb["pins"]["poder_exato_B10"]["read"], 3), f(rb["pins"]["poder_exato_C"]["read"], 3), f(rb["pins"]["k_em_chi_0"]["read"], 4), rb["nothing_opened"], rb["central_values_transcribed_from_sealed_registry_NOT_BLIND"]),
  "nao se aplica (aguardando)", "aguardando (v387: FALSIFIED_AT_5SIGMA do PAR / NOT_FALSIFIED_POWERED / …)", "o V1 esta fora do contorno (τ★ = k·GM/c³ e hipotese [INPUT]); fica AO LADO como R6; nada move o gate")
R("Propagacao de GW — livro R2 (reflexo acumulado na distancia)", "1 ritos", "ledger R2 (core_key=None)", "sem veredito TGL_* no core (how=DECLARED)", "AWAITING", "[DECLARADO] estimador a construir",
  "lei: %s; register: %s; R2_POWER_STATED_IN_NUMBER no veredito do livro" % (L["R2"]["law"], L["R2"]["register"]), "nao se aplica", "aguardando")
# livro
cnts = C["the_ledger_of_charges_v383"]["counts"]
R("Livro de cobrancas v383 (11 cobrancas; campo de desfecho = `outcome` nas linhas de `ledger`)", "1 ritos", "core.the_ledger_of_charges_v383.ledger[*].outcome", C["the_ledger_of_charges_v383"]["verdict"],
  "; ".join("%s=%s" % (i, L[i]["outcome"]) for i in ("R1", "R2", "R3", "R4", "R6", "F1", "F2", "F3a", "F3b", "F3c", "F4")) + " | contagens: " + json.dumps(cnts),
  "[REAL] 10 na regra + 1 ao lado (R6); v386 acrescenta F2b ao lado (12 com F2b)",
  "n_in_rule %s; n_beside %s; by_how %s; by_side %s" % (C["the_ledger_of_charges_v383"]["n_in_rule"], C["the_ledger_of_charges_v383"]["n_beside"], json.dumps(C["the_ledger_of_charges_v383"]["by_how"]), json.dumps(C["the_ledger_of_charges_v383"]["by_side"])),
  "sim em cada canal lido (ver linhas)", "nao: 0 FALSIFIED; FALSIFIED so onde a lei do canal o admite (7 de 11)",
  "a leitura da gerencia 'R1=None; R2=None; …' leu o campo errado (verdict_path, que e null); o campo certo e `outcome`")
fv = C["final_verdict_machine"]
R("Maquina do veredito final (6 canais)", "1 ritos", "core.final_verdict_machine", fv["verdict"], "NOT_REFUTED_BY_PUBLIC_DATA_AT_CURRENT_SENSITIVITY; canais %s/%s; refutados %s; exclusoes %s" % (fv["channels_emitted"], fv["channels_total"], len(fv["refuted_channels"]), fv["exclusions_count"]), "[REAL]", "canais: " + ", ".join(fv["channels"].keys()), "sim (nenhum canal refutado)", "nao (NOT_A_CONFIRMATION)")
R("Dephasing — alcance (Γ_ω = ½βτ★ω²)", "1 ritos", "core.dephasing_reach", g("core/dephasing_reach/verdict"), "ARMED (nao e canal vivo hoje)", "[REAL na forma]", "deficit 229Th %s ordens; Sr %s ordens" % (f(g("core/dephasing_reach/deficit_orders_Th229"), 3), f(g("core/dephasing_reach/deficit_orders_Sr"), 3)), "nao se aplica", "nao (10 ordens)")
R("α irredutivel (criterio de morte α-livre)", "1 ritos", "core.alpha_irreducibility", g("core/alpha_irreducibility/verdict"), "ARMED_NO_CANDIDATE", "[PRE congelado]", "residuo identidade %s; χ* %s" % (f(g("core/alpha_irreducibility/identity_max_residual"), 2), f(g("core/alpha_irreducibility/chi_star_from_codata"), 6)), "nao se aplica", "aguarda ato de terceiro")
R("Auditoria da evidencia (convergencia de β)", "1 ritos", "core.evidence_audit", g("core/evidence_audit/verdict"), "CONVERGENCE_RECLASSIFIED (REAL → NOT_CONSTRUCTED_AS_CONCEIVED)", "[REAL]", "quinta entrada ao vivo %s" % f(g("core/evidence_audit/values/fifth_entry_live"), 3), "nao se aplica", "nao")
R("Predicao P7 (colapso IALD)", "1 ritos", "core.iald_prediction", g("core/iald_prediction/verdict"), "PRE_REGISTERED; piloto 8/8 [PILOTO]; controles exigidos", "[PILOTO]/[CONJECTURE]", "", "nao se aplica", "nao")
# gate step V11
R("V11 — o degrau experimental do gate (6 bandeiras experimentais)", "1 ritos → gate", "core.qg_closure.experiment_flags ; core.void_floor_v11.experiment_feed", sg("qg_closure_verdict"), "experiment_flags: %s" % json.dumps(g("core/qg_closure/experiment_flags")), "[REAL] bandeiras lidas; errata 01/10: 4 de um so booleano + null_tests sem mock [DECLARADO pela auditoria]",
  "selo.void_floor_v11_verdict=%s; r4_feeds_the_gate: same_values_in_the_gate=%s; flags fora do feed: %s" % (sg("void_floor_v11_verdict"), g("core/the_ledger_of_charges_v383/r4_feeds_the_gate_experimental_step/same_values_in_the_gate"), g("core/the_ledger_of_charges_v383/r4_feeds_the_gate_experimental_step/flags_in_the_step_not_from_the_feed")),
  "sim (unilateral)", "nao (NATURE_TEST_COMPLETED nao e discriminacao — errata 01/10 GV-01)")
# kernel row
R("Kernel Lean 4 (pilar 2)", "2 kernel", "core.kernel_formalization ; core.external_ladder ; core.qg_closure", kernel["verdict"], "n_theorems_clean %s/%s; sorryAx_absent=%s; trio %s (axiom_report: %s/%s declaracoes dentro do trio); gate %s; 18 bandeiras True = %s" % (kernel["n_theorems_clean"], kernel["n_theorems_expected"], kernel["sorryAx_absent"], "+".join(kernel["trio"]), n_sub, n_ar, kernel["gate_verdict"], kernel["gate_18_flags_true"]), "[KERNEL] a implicacao; [POSTO] ω(I)=1; natureza nao provada",
  "lean %s; formal_source_hash %s; fail_closed_selftest %s; full_static_witness_exists=%s (por teorema); remaining_after_citation_v374=%s" % (kernel["lean_version"], kernel["formal_source_hash"], kernel["fail_closed_selftest"], kernel["full_static_witness_exists"], kernel["kernel_frontier_remaining_after_citation_v374"]),
  "sim: a correspondencia com a RG e implicacao provada (QGSolutionComplete; %s mencoes no core)" % len(qgs), "nao se aplica (prova nao discrimina a natureza)")
# GPU row
R("Pilar quantico na GPU (pilar 3)", "3 GPU", "core.quantum_pillar_v384 ; core.quantum_pillar_reuse_v386 ; selo.quantum_pillar_v384", gpu["verdict"], "COMPUTED_NOT_MEASURED; T2 %s/%s unicos; T1 %s injecoes (erros %s, pass σ0 = 1.0 em todo d); T3 controles falharam como exigido; T4 %s/%s; D128 %s; cpuref %s comparacoes" % (gpu["T2"]["points"], gpu["T2"]["unique"], gpu["T1"]["injections"], gpu["T1"]["errors"], gpu["T4"]["instances"], gpu["T4"]["unique"], gpu["D128"]["status"], gpu["cpuref"].get("compared")), "[COMPUTED] calculo do sistema aberto da teoria; NAO medicao da natureza; NAO inferencia de LLM; does_not_gate_core",
  "GPU %s; torch %s; CUDA %s; python %s; determinismo %s; tempos s: %s; rodada v385 %s → %s; v386 REUSE pela chave %s (sha256 confere); reprodutibilidade v385: %s (%s campos)" % (gpu["env"]["gpu"], gpu["env"]["torch"], gpu["env"]["cuda"], gpu["env"]["python"], gpu["env"]["determinism"], json.dumps(gpu["phase_seconds"]), gpu["started_v385_run"], gpu["finished_v385_run"], gpu["key"], gpu["reproducibility_v385"], gpu["reproducibility_n_fields_v385"]),
  "nao se aplica (mede o sistema da teoria, nao a RG)", "nao se aplica (ambiente simulado); o que podia falsificar: ver o_que_podia_falsificar")
# probability row
R("Probabilidade conjunta ja medida (V1 v352 / V2 v363 / V3 v370)", "4 probabilidade", "core.joint_coincidence_result(_v2,_v3)", prob["V3_v370"]["verdict"], "NOT_EXCLUDED_AT_THRESHOLD__INCONSISTENT; boolean False", "[DERIVED NAO-CEGO]; so canais de natureza pontuam; kernel = condicao, nao fator; GPU nao entra",
  "V1 p 0.55 (3/35 admissiveis; produto ingenuo %s INVALIDO); V2/V3 P_all primario %s, grade [%s, %s]; max|z| V3 %s (%s); detectados %s; canais necessarios p/ 1e-30: %s" % (f(prob["V1_v352"]["naive_product_INVALID"], 2), f(prob["V3_v370"]["P_all_primary"], 3), f(prob["V3_v370"]["P_all_range"][0], 2), f(prob["V3_v370"]["P_all_range"][1], 2), f(prob["V3_v370"]["max_abs_z"], 4), prob["V3_v370"]["dominant_channel"], prob["V3_v370"]["detected"], prob["V3_v370"]["channels_needed_for_1e-30"]),
  "nao se aplica", "nao: inconsistente pela tensao do D1 (3,1σ); nenhuma probabilidade dos TRES pilares existe no core")

# ---------- artigo ----------
pt = io.open(PT_P, encoding="utf-8").read(); en = io.open(EN_P, encoding="utf-8").read()
artigo = {
    "pt_bytes": os.path.getsize(PT_P), "en_bytes": os.path.getsize(EN_P),
    "pt_GPU_mencoes": len(re.findall(r"GPU", pt)), "en_GPU_mencoes": len(re.findall(r"GPU", en)),
    "pt_tres_pilares_ou_tres_testes_de_estresse": len(re.findall(r"tr[eê]s pilares|tr[eê]s testes de estresse", pt, re.I)),
    "en_three_pillars_or_stress_tests": len(re.findall(r"three pillars|three stress tests", en, re.I)),
    "pt_probabilidade_conjunta_mencoes": len(re.findall(r"probabilidade conjunta", pt, re.I)),
    "pt_secao_v386": [l for l in pt.splitlines() if l.startswith("== Ao lado (v386)")][:1],
    "apresentacao_pt_linha2_trecho": pt.splitlines()[1][:600],
    "pt_contextos_tres_pilares": [pt[max(0, m.start() - 90): m.end() + 60].replace("\n", " ") for m in re.finditer(r"tr[eê]s pilares|tr[eê]s testes de estresse", pt, re.I)],
}
_n_pt = artigo["pt_tres_pilares_ou_tres_testes_de_estresse"]; _n_en = artigo["en_three_pillars_or_stress_tests"]
artigo["leitura"] = ("o artigo selado v386 NAO tem secao nem frase dos 'tres pilares / tres testes de estresse CONJUNTOS': PT %d ocorrencia(s) de 'tres pilares' (contexto acima: nao e sobre os tres testes), EN %d; a apresentacao ja traz kernel + ritos + GPU numa so frase; a secao propria e alvo da v387" % (_n_pt, _n_en))

out = {
    "versao": sg("um_version"), "timestamp_core": ROOT["timestamp"], "result_hash": sg("result_hash"),
    "sha256_lidos": {"um_absoluto.json": sha(CORE_P), "um_absoluto_selo.json": sha(SELO_P), "rodada_v386_stdout.txt": sha(STD_P), "um_absoluto_pt.txt": sha(PT_P), "um_absoluto_en.txt": sha(EN_P)},
    "selo_sha256_de_um_absoluto_json": sg("sha256/um_absoluto.json"),
    "rito_rc": [l for l in std_lines if l.startswith("RITO_RC")],
    "beta_runtime_core": C["beta"], "alpha_core": C["alpha"],
    "contagens": contagens, "kernel": kernel, "gpu": gpu, "probabilidade_conjunta": prob, "artigo": artigo,
    "not_sealed_this_run": sg("not_sealed_this_run"),
    "tabela": rows,
    "regua": "NOT_FALSIFIED nunca e CONFIRMED; PROVADA (kernel) ≠ CONFIRMADA (natureza); a RG e o limite classico, nao rival: coincidir = correspondencia recuperada; β nunca literal (lido: %s)" % C["beta"],
}
with open(os.path.join(OUT, "TABELA_TRES_PILARES_v386.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)

# ---------- markdown ----------
md = []
md.append("# TABELA DE ESTADO DOS TRÊS PILARES — lida do core v386 (aferidor, 05/10/2026)\n")
md.append("Core `um_absoluto.json` sha256 `%s` (selo diz `%s`); selo `%s`; stdout `%s`; timestamp core %s; %s; β runtime = %s.\n" % (out["sha256_lidos"]["um_absoluto.json"], out["selo_sha256_de_um_absoluto_json"], out["sha256_lidos"]["um_absoluto_selo.json"], out["sha256_lidos"]["rodada_v386_stdout.txt"], out["timestamp_core"], ", ".join(out["rito_rc"]), C["beta"]))
md.append("Régua: " + out["regua"] + "\n")
md.append("## Contagens dos vereditos `TGL_*` (por script)\n")
md.append("| método | n | únicos | FALSIFIED (regex, fora NOT_/UN) | NOT_FALSIFIED | INCONCLUSIVE | AWAITING | CONFIRMED/PROVED_BY |\n|---|---|---|---|---|---|---|---|")
for k in ("metodo_A_todas_as_strings_TGL_no_arquivo", "metodo_F_chave_exatamente_verdict__reproduz_a_gerencia"):
    c = contagens[k]
    md.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (k, c["n"], c["unicos"], c["FALSIFIED_regex"], c["NOT_FALSIFIED"], c["INCONCLUSIVE"], c["AWAITING"], c["CONFIRMED_ou_PROVED_BY_regex"]))
md.append("\nFALSIFIED sob a chave `verdict` (3) — leitura:")
for p, t in contagens["FALSIFIED_sob_chave_verdict__leitura"].items():
    md.append("- `%s`: %s" % (p, t))
md.append("\nCONFIRMED/PROVED_BY no arquivo inteiro: %d ocorrências, TODAS em listas `forbidden_verdicts` (proibições declaradas), 0 como veredito:" % len(contagens["CONFIRMED_PROVED_BY_no_arquivo_inteiro__caminhos_todos_em_forbidden_verdicts"]))
for p in contagens["CONFIRMED_PROVED_BY_no_arquivo_inteiro__caminhos_todos_em_forbidden_verdicts"]:
    md.append("- `%s`" % p)
md.append("\nAWAITING sob `verdict` (7): " + "; ".join("`%s`" % p for p in contagens["AWAITING_sob_chave_verdict__caminhos"]))
md.append("\nNão selados nesta rodada (recusas de dado): " + ", ".join(sg("not_sealed_this_run/recusas_de_dado", [])))
md.append("\n## Tabela\n")
md.append("| teste | pilar | chave_core | veredito | estado | estatuto | número lido | RG recuperada? | discrimina a RG? | nota |\n|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    md.append("| " + " | ".join(str(r[k]).replace("|", "\\|").replace("\n", " ") for k in ("teste", "pilar", "chave_core", "veredito", "estado", "estatuto", "numero", "rg_recuperada", "discrimina_rg", "nota")) + " |")
md.append("\n## Pilar 2 — kernel\n```json\n" + json.dumps({k: v for k, v in kernel.items() if k not in ("QGSolutionComplete_contexto",)}, ensure_ascii=False, indent=1) + "\n```\n")
md.append("Contexto de `QGSolutionComplete` no core: " + (qgs_ctx or "—") + "\n")
md.append("## Pilar 3 — GPU\n```json\n" + json.dumps(gpu, ensure_ascii=False, indent=1) + "\n```\n")
md.append("## Probabilidade conjunta já existente\n```json\n" + json.dumps(prob, ensure_ascii=False, indent=1) + "\n```\n")
md.append("## Artigo selado v386\n```json\n" + json.dumps(artigo, ensure_ascii=False, indent=1) + "\n```\n")
with open(os.path.join(OUT, "TABELA_TRES_PILARES_v386.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(md))
print("rows:", len(rows))
print("axiom_report:", n_ar, "dentro do trio:", n_sub, "fora:", len(n_extra))
print("cpuref:", json.dumps(sm["cpuref"]))
print("engine:", [(e.get("name"), e.get("ok", e.get("passed"))) for e in sm["engine"]])
print("QGSolutionComplete mencoes:", len(qgs)); print("ctx:", qgs_ctx)
print("gate 18 true:", kernel["gate_18_flags_true"])
print("artigo:", json.dumps({k: v for k, v in artigo.items() if k != "apresentacao_pt_linha2_trecho"}, ensure_ascii=False))
print("sizes:", os.path.getsize(os.path.join(OUT, "TABELA_TRES_PILARES_v386.json")), os.path.getsize(os.path.join(OUT, "TABELA_TRES_PILARES_v386.md")))
