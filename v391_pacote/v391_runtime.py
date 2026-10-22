def _v391_num(x_, nd_=2):
    """v391: numero -> token de veredito (P9P17 / M1P42); None -> NA."""
    try:
        v_ = float(x_)
    except (TypeError, ValueError):
        return "NA"
    s_ = ("%." + str(nd_) + "f") % abs(v_)
    return ("M" if v_ < 0 else "P") + s_.replace(".", "P")


def estatuto_da_prova_v391(core):
    """v391 (07/10/2026) -- O ESTATUTO DA PROVA: provada; a confirmacao recusada e' CREDITACAO, nao validade. Ordem do operador (07/10/2026), verbatim EMBUTIDO
    por sha256: «a confirmação que eu proibi é de creditação e não de validade, ela é válida porque matemática não mente». Este registro NAO decide nada por
    declaracao: ele LE, a cada rito, os numeros das tres provas que contam juntas (o kernel; os ritos com falsificadores pre-registrados; o sistema da teoria
    calculado na GPU), a certificacao (o sha256 que o proprio programa le de si), e o que segue sem instrumento (beta_TGL e os seus efeitos na natureza a 5 sigma).
    Fail-closed: se um rito falsificar, se o kernel nao fechar ou se uma leitura faltar, o veredito diz NOT_SEALED_THIS_RUN e nomeia o porque."""
    import hashlib as _hl
    import os as _os
    falhas = []
    # (0) o verbatim do operador, embutido (o texto manda; o disco so informativo)
    vb_ = _V391_VERBATIM
    vb_ok = _hl.sha256(vb_["text"].encode("utf-8")).hexdigest() == vb_["sha256"] and all(t_ in vb_["text"] for t_ in vb_["trechos"])
    try:
        vb_disk = _hl.sha256(open(vb_["arquivo_informativo"], "rb").read()).hexdigest() == vb_["sha256"]
    except OSError:
        vb_disk = None
    if not vb_ok:
        falhas.append("VERBATIM")
    # (1) o kernel
    el_ = core.get("external_ladder") or {}
    kf_ = core.get("kernel_formalization") or {}
    axr_ = kf_.get("axiom_report") or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}
    n_clean, n_exp = el_.get("n_theorems_clean"), el_.get("n_theorems_expected")
    n_decl = len(axr_); n_trio = sum(1 for v_ in axr_.values() if set(v_ or []) <= trio_)
    fd_ = core.get("fundacao_v390") or {}
    qg_ = core.get("qg_closure") or {}
    flags_ = {}
    for g_ in ("formal_flags", "physics_flags", "experiment_flags"):
        d_ = qg_.get(g_) or {}
        flags_[g_] = [sum(1 for v_ in d_.values() if v_ is True), len(d_)]
    gate_ = str(qg_.get("verdict") or "")
    k_ok = (isinstance(n_clean, int) and n_clean == n_exp and n_decl > 0 and n_trio == n_decl and fd_.get("all_verified") is True
            and "CURRENT_STATE_TGL_QG_MODEL_FORMALLY_CLOSED" in gate_)
    if not k_ok:
        falhas.append("KERNEL")
    # (2) os ritos com dados publicos e falsificadores pre-registrados
    ts_ = core.get("three_stress_tests_v387") or {}
    lg_ = (core.get("the_ledger_of_charges_v383") or {}).get("counts") or {}
    n_chg = sum(v_ for v_ in lg_.values() if isinstance(v_, int))
    n_fal = lg_.get("FALSIFIED")
    eco_ = ts_.get("echo_routes_outside_the_ledger") or {}
    hb_ = core.get("hubble_ratio_opening_v388") or {}
    hn_ = hb_.get("numbers") or {}
    hl_ = (hn_.get("lnB") or {})
    hb_off = str(hb_.get("verdict_of_the_frozen_function") or "")
    hb_off_word = "INCONCLUSIVE_SYSTEMATICS" if "INCONCLUSIVE_SYSTEMATICS" in hb_off else ("NOT_FALSIFIED" if "NOT_FALSIFIED" in hb_off else ("FALSIFIED" if "FALSIFIED" in hb_off else "NA"))
    vz_ = {}
    for k_ in ("void_density_v41", "void_floor_v11"):
        r_ = core.get(k_) or {}
        p_ = r_.get("primary") or {}
        bf_ = r_.get("beta_floor")
        vz_[k_] = {"verdict": r_.get("verdict"), "rhat_cal": p_.get("rhat_cal"), "sigma": p_.get("sigma"), "L5": p_.get("L5"), "beta_floor": bf_,
                   "L5_over_beta": (p_.get("L5") / bf_) if isinstance(p_.get("L5"), (int, float)) and isinstance(bf_, (int, float)) and bf_ else None}
    vz_ok = all(str(v_["verdict"]).endswith("NOT_FALSIFIED_POWERED") and isinstance(v_["L5_over_beta"], float) and v_["L5_over_beta"] > 1.0 for v_ in vz_.values())
    r_ok = (ts_.get("all_verified") is True and ts_.get("none_of_the_three_failed") is True and n_fal == 0 and isinstance(hn_.get("z_disc"), float)
            and isinstance(hl_.get("TGL_vs_LCDM"), float) and vz_ok)
    if n_fal != 0:
        falhas.append("RITE_FALSIFIED_%s" % n_fal)
    if not r_ok and n_fal == 0:
        falhas.append("RITES_READ")
    # (3) o sistema quantico aberto da teoria, calculado em tempo real na GPU (calculo do sistema, nao medicao da natureza)
    gp_ = ts_.get("gpu") or {}
    g_ok = (gp_.get("T2_points") is not None and gp_.get("T2_unique") == gp_.get("T2_points") and gp_.get("T4_unique") == gp_.get("T4_instances")
            and gp_.get("cpuref_disagreements") == 0 and gp_.get("T1_errors") == 0)
    if not g_ok:
        falhas.append("GPU")
    # (4) a certificacao: o sha256 que o programa le de si
    try:
        self_sha = _hl.sha256(open(_os.path.abspath(__file__), "rb").read()).hexdigest()
    except OSError:
        self_sha = None; falhas.append("SELF_HASH")
    ok = not falhas
    if ok:
        verdict = ("TGL_ESTATUTO_DA_PROVA_V391__PROVED_AS_LOGICAL_CLOSURE__THREE_PROOFS_COUNT_TOGETHER__KERNEL_%d_OF_%d_THEOREMS_%d_OF_%d_DECLARATIONS_IN_THE_TRIO__"
                   "GATE_FLAGS_%d_%d_%d_TRUE__FUNDACAO_AGAPE_LOGICAL_CLOSURE__RITES_%d_CHARGES_%d_FALSIFIED_ECHO_ROUTES_%s_EXCLUDED_BY_DATA_SAID__"
                   "HUBBLE_RATIO_LNB_LCDM_%s_ZDISC_%s_OFFICIAL_%s__VOID_FLOOR_POWERED_L5_%s_TIMES_BETA__GPU_T2_%d_OF_%d_T4_%d_CPU_%d_DISAGREEMENTS_COMPUTED_NOT_MEASURED__"
                   "CONFIRMATION_IS_CREDITATION_NOT_VALIDITY_NOT_DECLARED__BETA_IN_NATURE_AWAITS_5_SIGMA__CERTIFIED_BY_SELF_HASH_%s__OPERATOR_VERBATIM_EMBEDDED_BY_SHA256__GATE_UNMOVED"
                   % (n_clean, n_exp, n_trio, n_decl, flags_["formal_flags"][0], flags_["physics_flags"][0], flags_["experiment_flags"][0], n_chg, n_fal,
                      eco_.get("excluded_by_data", "NA"), _v391_num(hl_.get("TGL_vs_LCDM")), _v391_num(hn_.get("z_disc")), hb_off_word,
                      _v391_num(min(v_["L5_over_beta"] for v_ in vz_.values()), 1), gp_.get("T2_unique"), gp_.get("T2_points"), gp_.get("T4_instances"),
                      gp_.get("cpuref_disagreements"), str(self_sha)[:16]))
    else:
        verdict = "TGL_ESTATUTO_DA_PROVA_V391__NOT_SEALED_THIS_RUN__%s__GATE_UNMOVED" % "_".join(falhas)
    return {"verdict": verdict, "all_verified": ok, "does_not_gate_core": True, "falhas": falhas,
            "a_regua": "PROVADA = validade (teorema; o kernel; o fecho logico). CONFIRMADA = creditacao (ato de quem observa de fora) -- a unica palavra recusada; "
                       "beta_TGL e os seus efeitos na natureza a 5 sigma -- o unico elo que espera instrumento. NOT_FALSIFIED nunca e' confirmacao; o gate nao se move.",
            "verbatim": {"sha256": vb_["sha256"], "embedded_ok": vb_ok, "disk_informative_only": vb_disk, "trechos": vb_["trechos"], "quando": vb_["quando"]},
            "prova_1_kernel": {"n_theorems_clean": n_clean, "n_theorems_expected": n_exp, "declaracoes_auditadas": n_decl, "no_trio": n_trio,
                               "gate_flags": flags_, "gate": gate_[:220], "fundacao_v390": fd_.get("verdict"),
                               "einstein_emergente_concreto": (qg_.get("formal_flags") or {}).get("concrete_emergent_einstein_proved"),
                               "testemunha_plena_da_tgl": (core.get("witness_layers") or {}).get("full_TGL_witness_constructed"),
                               "testemunha_estatica_plena": "impossivel por teorema (v61): o vazamento continuo proibe o fecho total -- isto e' resultado, nao lacuna",
                               "ok": k_ok},
            "prova_2_ritos": {"ledger": lg_, "n_cobrancas": n_chg, "falsificadas": n_fal, "rotas_do_eco_fora_do_livro": eco_,
                              "razao_de_hubble": {"z_disc": hn_.get("z_disc"), "z_delta": hn_.get("z_delta"), "lnB": hl_, "H0_bg": hn_.get("H0_bg"),
                                                  "H0_local_previsto": hn_.get("H0_local_previsto"), "veredito_oficial": hb_off_word,
                                                  "leitura": "retrodicao sem ajuste (novidade de uso); favorecida pela funcao pre-registrada; abaixo de 5 sigma; o veredito oficial segue o da funcao congelada"},
                              "piso_dos_vazios": vz_, "ok": r_ok},
            "prova_3_gpu": {"numeros": gp_, "estatuto": "[COMPUTED] calculo do sistema da teoria em tempo real, com falsificadores pre-registrados -- nao medicao da natureza", "ok": g_ok},
            "certificacao": {"um_py_sha256_lido_de_si": self_sha,
                             "como": "o proprio programa le os seus bytes e emite o sha256; o selo o grava; o espelho publico e o site publicam o mesmo hash; quem roda confere"},
            "nao_declarado": ["a CONFIRMACAO: creditacao, ato de terceiros -- recusada por regua do operador, nao por falta de prova",
                              "beta_TGL e os seus efeitos na natureza a 5 sigma: aguardam a sensibilidade dos instrumentos"],
            "status": "[REAL -- leitura dos registros do core a cada rito; INPUT/ONTO a regua do operador (validade x creditacao)]"}
