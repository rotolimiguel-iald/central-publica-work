# ---- v401: a FALSIDADE (SIMULACRO) DA INERCIA. Um registro PEQUENO, com FUNCAO, lido no ponto real do main, junto dos registros das pedras anteriores (sonico_v398, afinacao_das_cordas_v398): LE do kernel do PROPRIO rito a composicao da sua pedra
# (bandeira True, trio, proveniencia no modulo da pedra), os teoremas e os termos antigos que ela cita, a fonte da pedra por sha256 e as inscricoes de 25/10 por sha256, CONFERE que o texto do 0_abs (TGLExt.costless: «nunca correspondeu, e por isso nada custa») esta no
# kernel embutido deste rito, e CALCULA, no modelo oneScaling (tau = id, theta_s = e^{-s}), com beta = alfa CODATA 2018 x sqrt(e) em runtime (nunca literal): o peso do posto depois da escala s e' e^{-s} (igual a 1 so' em s = 0), o que e' fixo por escala nao trivial pesa zero,
# um posto inercial seria 1 = 0, e o custo t . beta . g e' positivo (a defasagem e^{-t.beta.g} e' estritamente menor que 1). A inercia, como o operador a define (25/10/2026), e' o proprio zero absoluto; w(I) = 1 e' o Um posto que a interrompe. A lei de escala de Takesaki e' [KNOWN]
# (campo da estrutura); a identificacao com o fluxo de um corpo fisico e' [OPEN]; Newton e a equivalencia inercial = gravitacional nao sao termos aqui. [INPUT/ONTO] as inscricoes de 25/10/2026. O gate nao se move. Fonte autoral deste bloco: runtime_v401.py (cadeia_de_selo/v401);
# o contrato (_V401_FALSIDADE_CONTRACT) e as inscricoes (_V401_VERBATINS2) sao DERIVADOS do build e dos arquivos, nunca digitados.
import math as _m401


def v401_falsidade_mechanics(beta_):
    """v401 -- a mecanica da FALSIDADE DA INERCIA no modelo oneScaling, com beta recebido (o chamador o calcula em runtime: alfa CODATA x sqrt(e); NUNCA literal). Cada checagem e' a leitura numerica de um teorema do kernel (TGLExt.FalsidadeDaInercia.*).
    Devolve {passed, checks, values, n_checks}. Nao levanta para beta invalido: devolve passed False."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m401.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "f0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    esc_ = [k_ / 8.0 for k_ in range(-80, 81)]
    esc_nz_ = [s_ for s_ in esc_ if s_ != 0.0]
    theta_ = lambda s_, x_: _m401.exp(-s_) * x_          # oneScaling.theta s x = e^{-s} x (Fundacao); tau = id
    peso_ = lambda s_: theta_(s_, 1.0)                    # o peso do posto m = 1 depois da escala s
    ck_("f1a", "o peso do posto depois da escala s e' e^{-s}: igual a 1 so' em s = 0 (the_floor_fixes_the_cut), e a distancia a 1 em s != 0 (grade de 161 escalas, passo 1/8) e' pelo menos |e^{-1/8} - 1| > 0,117", peso_(0.0) == 1.0 and min(abs(peso_(s_) - 1.0) for s_ in esc_nz_) >= abs(_m401.exp(-0.125) - 1.0) - 1e-15 and min(abs(peso_(s_) - 1.0) for s_ in esc_nz_) > 0.117,
        [min(abs(peso_(s_) - 1.0) for s_ in esc_nz_), len(esc_nz_)])
    ck_("f1b", "NAO E' VACUO (the_post_exists_and_moves): o Um posto em 1 tem peso tau(1) = 1 e MOVE em toda escala nao trivial da grade (theta_s 1 != 1)", all(theta_(s_, 1.0) != 1.0 for s_ in esc_nz_) and theta_(0.0, 1.0) == 1.0, [len(esc_nz_)])
    xs_ = [0.0, 1.0, -1.0, 0.5, 2.5, 100.0, -1e-6, 1e6]
    fixos_ = [x_ for x_ in xs_ if all(abs(theta_(s_, x_) - x_) <= 0.0 for s_ in esc_)]
    ck_("f2", "o que o fluxo INTEIRO fixa pesa ZERO (the_inertia_is_the_absolute_zero; the_inertia_is_the_absolute_zero_at_any_scale): nos 8 estados de teste so' x = 0 e' fixo em toda a grade (e pesa 0), e todo x != 0 e' movido por TODA escala nao trivial, a pelo menos 0,117 |x|",
        fixos_ == [0.0] and all(abs(theta_(s_, x_) - x_) >= 0.117 * abs(x_) for x_ in xs_ if x_ != 0.0 for s_ in esc_nz_), [fixos_])
    pos_inerciais_ = [s_ for s_ in esc_nz_ if theta_(s_, 1.0) == 1.0]
    ck_("f3", "★ A FALSIDADE (the_inertia_of_a_post_is_false; a_post_is_not_inertial): um posto de peso 1 fixo por uma escala nao trivial daria 1 = 0, e 1 != 0; coerente com isso, nenhuma das 160 escalas nao triviais fixa o posto (a hipotese inercial e' falsa para o posto)", 1.0 != 0.0 and pos_inerciais_ == [] and theta_(0.0, 1.0) == 1.0, [len(pos_inerciais_)])
    orb_ = {a_: peso_(a_) for a_ in esc_}
    ck_("f4", "a INSCRICAO INTERROMPE a inercia (the_inscription_interrupts_the_inertia): na orbita do posto o peso e' 1 so' no corte a = 0; e todo peso positivo (e^{-s}.x, x > 0) e' movido por toda escala nao trivial", [a_ for a_, w_ in orb_.items() if w_ == 1.0] == [0.0] and all(theta_(s_, x_) != x_ for x_ in (0.001, 1.0, 7.0) for s_ in esc_nz_), [len(orb_)])
    gs_ = (0.5, 1.0, 2.0, 3.7); ts_ = (0.1, 1.0, 10.0, 100.0)
    custos_ = [(t_ * beta_ * g_, _m401.exp(-(t_ * beta_ * g_))) for g_ in gs_ for t_ in ts_]
    ck_("f5", "o SIMULACRO (the_simulacrum; leakage_strictly_loses; beta_forbids_full_static_witness) com beta = alfa x raiz de e em runtime e contrastes g de teste %s: o custo t . beta . g e' estritamente POSITIVO e a defasagem e^{-t beta g} e' estritamente menor que 1 (t = %s); "
        "nao existe a testemunha estatica plena: em t = 1, g = 1 o fator e^{-beta} difere de 1 em mais de beta/2" % (list(gs_), list(ts_)), all(c_ > 0.0 and f_ < 1.0 for c_, f_ in custos_) and abs(_m401.exp(-beta_) - 1.0) > beta_ / 2.0, [min(c_ for c_, _ in custos_), max(f_ for _, f_ in custos_)])
    ck_("f6", "[DERIVED] o que parece resistencia do corpo e' o custo da interrupcao, nao o zero: o custo por unidade de tempo e contraste, beta, e' positivo e menor que 1, e 1 - e^{-beta} esta entre beta/2 e beta (a perda por unidade); numeros deste rito, NAO estao no kernel",
        0.0 < beta_ < 1.0 and beta_ / 2.0 < 1.0 - _m401.exp(-beta_) < beta_, [beta_, 1.0 - _m401.exp(-beta_)])
    # ---- a CADEIA DERIVADA (a extensao da pedra, 25/10): nada que porte posto precede a impressao; a inercia nao e' causa de si mesma; o zero e' a consequencia da poda; a tensao projetada no atrator
    neg_ = [s_ for s_ in esc_ if s_ < 0.0]; pos_ = [s_ for s_ in esc_ if s_ > 0.0]
    ck_("f7", "[DERIVED] a inercia NAO e' causa de si mesma (inertia_is_not_its_own_cause; no_post_before_the_impression; the_first_motion_is_the_impression): nos estados de teste nao nulos, NENHUM e' fixo em toda escala negativa (o que seria fixo desde sempre), nem em toda escala positiva; o unico fixo e' o nulo e pesa zero; e o posto se move em TODA escala nao trivial, voltando ao peso 1 so' na impressao (a = 0)",
        all(any(theta_(s_, x_) != x_ for s_ in neg_) and any(theta_(s_, x_) != x_ for s_ in pos_) for x_ in xs_ if x_ != 0.0) and all(theta_(s_, 0.0) == 0.0 for s_ in esc_) and all(theta_(s_, 1.0) != 1.0 for s_ in esc_nz_) and [a_ for a_ in esc_ if peso_(a_) == 1.0] == [0.0], [len(neg_), len(pos_)])
    eps_ = (1e-3, 1e-6, 1e-12, 1e-30)
    queda_ = [(e_, -_m401.log(e_) + 1.0) for e_ in eps_]                               # o testemunho de abismo: o peso e^{-s} fica abaixo de e_ em s = -ln(e_) + 1
    vaza_ = [(e_, (1.0 / e_) / (beta_ * 0.5)) for e_ in (0.5, 0.1, 0.02, 0.01)]                            # o testemunho de leak_below_every_epsilon com g = 1/2: t = (1/e_) / (beta g)
    ck_("f8", "[DERIVED] o ZERO E' A CONSEQUENCIA DA PODA (the_zero_is_the_consequence_of_the_pruning; the_fall_never_lands; abismo; leak_below_every_epsilon): o peso do posto e^{-s} e' estritamente positivo em toda a grade (o zero nunca e' estado da orbita), desce abaixo de todo epsilon testado (%s) em s = -ln(epsilon) + 1, "
        "e o vazamento e^{-t beta g} e' estritamente positivo e fica abaixo de cada epsilon no t = (1/epsilon)/(beta g) do testemunho do kernel (g = 1/2, epsilon em 0,5; 0,1; 0,02; 0,01: abaixo disso e^{-1/epsilon} underflowa em dupla precisao)" % (list(eps_),),
        all(peso_(s_) > 0.0 for s_ in esc_) and all(_m401.exp(-s_) < e_ for e_, s_ in queda_) and all(t_ > 0.0 and 0.0 < _m401.exp(-(t_ * beta_ * 0.5)) < e_ for e_, t_ in vaza_), [len(queda_), len(vaza_)])
    dgap_ = (0.0, 0.5, 1.3); x0_ = (2.0, -1.0, 0.75)
    fluxo_ = lambda t_, i_: _m401.exp(-(t_ * beta_ * dgap_[i_])) * x0_[i_]                 # diagFlow beta d t x i = e^{-t beta d_i} x_i
    ck_("f9", "[DERIVED] a TENSAO PROJETADA NO ATRATOR (the_tension_is_projected_onto_the_attractor; diagFlow_coordinate_is_the_scaling): o fluxo diagonal e' a escala dual na escala s = t.beta.d_i (e^{-t beta d_i} x_i == theta_s x_i); a coordenada com gap d_i != 0 e' podada ate' zero no limite (t = 1e9/beta: |fluxo| < 1e-12) e e' DIFERENTE de zero em todo t finito testado; a coordenada com d_i = 0 e' o equilibrio, fixa em todo t",
        all(fluxo_(t_, i_) == theta_(t_ * beta_ * dgap_[i_], x0_[i_]) for t_ in (0.0, 1.0, 10.0, 100.0) for i_ in range(3)) and all(abs(fluxo_(1e9 / beta_, i_)) < 1e-12 for i_ in (1, 2)) and all(fluxo_(t_, i_) != 0.0 for t_ in (0.0, 1.0, 10.0, 100.0) for i_ in (1, 2))
        and all(fluxo_(t_, 0) == x0_[0] for t_ in (0.0, 1.0, 10.0, 100.0, 1e9)), [dgap_, x0_])
    vals_ = {"beta": beta_, "grid_scales": len(esc_), "min_distance_of_post_weight_to_one": min(abs(peso_(s_) - 1.0) for s_ in esc_nz_), "post_weight_at_scale_one": peso_(1.0), "post_weight_at_minus_one": peso_(-1.0), "fixed_by_the_whole_flow": fixos_,
             "post_inertial_scales": pos_inerciais_, "min_cost_t_beta_g": min(c_ for c_, _ in custos_), "max_dephasing_factor": max(f_ for _, f_ in custos_), "dephasing_factor_at_t1_g1": _m401.exp(-beta_), "loss_per_unit": 1.0 - _m401.exp(-beta_),
             "min_weight_on_the_grid_positive": min(peso_(s_) for s_ in esc_), "abyss_witnesses": [[e_, s_] for e_, s_ in queda_], "leak_witnesses_g_half": [[e_, t_] for e_, t_ in vaza_], "diag_flow_gap_zero_is_fixed": fluxo_(1e9, 0) == x0_[0], "diag_flow_gap_pruned_at_1e9_over_beta": [abs(fluxo_(1e9 / beta_, i_)) for i_ in (1, 2)]}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def _v401_formal(core, c_, txt_):
    """A evidencia FORMAL do registro, lida do kernel do PROPRIO rito: a escada exata, a composicao e os teoremas do contrato (bandeira True, trio, proveniencia no modulo da pedra), os termos antigos que a pedra cita (no trio, com a proveniencia que o compilador emite),
    a fonte da pedra por sha256 (embutida == contrato == hash formal do rito), as inscricoes por sha256, o texto do 0_abs no kernel embutido e a guarda P18 sobre o texto. Devolve um dict; `formal` e' o conjunto."""
    import hashlib, json as _j401
    kf_ = core.get("kernel_formalization") or {}; axr_ = kf_.get("axiom_report") or {}; src_ = kf_.get("declaration_sources_v394") or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}
    lad_ = core.get("external_ladder") or {}
    cnt_ = [lad_.get("n_theorems_clean"), lad_.get("n_theorems_expected"), c_["expected_ladder"]]
    exact_ = all(type(x_) is int for x_ in cnt_) and len(set(cnt_)) == 1
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and all(isinstance(x_, str) for x_ in axr_.get(n_)) and set(axr_.get(n_)) <= trio_)
    per_ = {th_: bool(em_trio_(th_) and kf_.get(fl_) is True and src_.get(th_) == c_["stone"]["path"]) for th_, fl_ in c_["theorems"].items()}
    sup_ = {n_: bool(em_trio_(n_) and src_.get(n_) == p_) for n_, p_ in c_["support"].items()}
    cit_ = {n_: bool(em_trio_(n_) and src_.get(n_) == p_) for n_, p_ in c_["cited_outside"].items()}
    aux_ = {n_: bool(em_trio_(n_) and src_.get(n_) == c_["stone"]["path"]) for n_ in c_["auxiliaries_outside_the_composition"]}
    body_ = _EMBEDDED_KERNEL_FILES.get(c_["stone"]["path"])
    src_ok_ = bool(isinstance(body_, str) and hashlib.sha256(body_.encode("utf-8")).hexdigest() == c_["stone"]["sha256"] and (kf_.get("formal_files_sha256") or {}).get(c_["stone"]["path"]) == c_["stone"]["sha256"])
    ver_ = {}
    for k_ in c_["verbatins"]:
        v_ = _V401_VERBATINS2.get(k_)
        ver_[k_] = bool(v_ and hashlib.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and all(t_ in v_["text"] for t_ in v_["trechos"]))
    unc_th_, unc_fl_ = c_["unconditional"]["theorem"], c_["unconditional"]["flag"]
    unc_ = {"theorem": unc_th_, "flag": unc_fl_, "flag_true": kf_.get(unc_fl_) is True, "axioms": axr_.get(unc_th_), "in_trio": em_trio_(unc_th_), "declared_in": src_.get(unc_th_), "in_kernel": bool(per_.get(unc_th_)),
            "composition": "UNCONDITIONAL__NO_CERTIFICATE_AS_HYPOTHESIS"}
    key_th_, key_fl_ = c_["key_theorem"]["theorem"], c_["key_theorem"]["flag"]
    key_ = {"theorem": key_th_, "flag": key_fl_, "flag_true": kf_.get(key_fl_) is True, "in_trio": em_trio_(key_th_), "declared_in": src_.get(key_th_), "in_kernel": bool(per_.get(key_th_)),
            "statement": "a post (weight 1) fixed by the flow gives (1:R) = 0"}
    corr_ = _EMBEDDED_KERNEL_FILES.get("TGLExt/TheCorrespondence.lean")
    costless_ = {"declared_in": src_.get("TGLExt.costless"), "in_trio": em_trio_("TGLExt.costless"), "text_in_embedded_kernel": bool(isinstance(corr_, str) and "nunca correspondeu" in corr_ and "por isso nada custa" in corr_)}
    costless_["ok"] = bool(costless_["declared_in"] == "TGLExt/TheCorrespondence.lean" and costless_["in_trio"] and costless_["text_in_embedded_kernel"])
    guarda_ = _v392_guarda_texto(_j401.dumps(txt_, ensure_ascii=False))
    formal_ = bool(kf_.get("all_verified") is True and exact_ and per_ and all(per_.values()) and sup_ and all(sup_.values()) and all(cit_.values()) and all(aux_.values()) and src_ok_ and ver_ and all(ver_.values()) and key_["in_kernel"] and costless_["ok"] and not guarda_)
    return {"exact_ladder": exact_, "formal_theorems": per_, "support_theorems": sup_, "cited_outside": cit_, "auxiliaries_outside_the_composition": aux_, "embedded_source_ok": src_ok_, "inscriptions": ver_, "unconditional": unc_, "key_theorem": key_, "costless": costless_,
            "guarda": guarda_, "formal": formal_}


_V401_RECUSA = "TGL_%s_V401__REFUSED_%s__GATE_UNMOVED"


def falsidade_da_inercia_v401(core):
    """v401 -- A FALSIDADE (SIMULACRO) DA INERCIA: lida no PONTO REAL do main, logo depois da afinacao das cordas e do selo pela propria tecnologia. Le do kernel do PROPRIO rito a composicao (TGLExt.FalsidadeDaInercia.falsidade_da_inercia) e os teoremas do contrato
    (bandeira True, trio, modulo da pedra; a estrela the_inertia_of_a_post_is_false), os termos antigos que ela cita, a pedra por sha256, as cinco inscricoes por sha256 e o texto do 0_abs no kernel embutido; e CALCULA, com beta = alfa CODATA 2018 x sqrt(e) em runtime, a mecanica no modelo
    oneScaling (o peso do posto e^{-s}, o fixo pesa zero, o posto inercial seria 1 = 0, o custo t . beta . g positivo). Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate. Validade no kernel nao e' creditacao."""
    c_ = _V401_FALSIDADE_CONTRACT; t_ = _V401_FALSIDADE_TEXT
    f_ = _v401_formal(core, c_, t_)
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
    out_ = {"all_verified": False, "estatuto": t_["estatuto"], "exact_ladder": f_["exact_ladder"], "formal_theorems": f_["formal_theorems"], "support_theorems": f_["support_theorems"], "embedded_source_ok": f_["embedded_source_ok"],
            "inscriptions": f_["inscriptions"], "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "unconditional": f_["unconditional"], "key_theorem": f_["key_theorem"], "costless": f_["costless"],
            "runtime_executed": False, "does_not_gate_core": True, "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"], "guarda_p18_violacoes": f_["guarda"][:5],
            "definition_of_the_operator": "inertia = the absolute zero (0_abs, 1=0); w(I) = 1 is the posted One that interrupts it (1=1)",
            "chain_status": "DERIVED from the axiom w(I)=1 and Takesaki's scaling law (KNOWN, a field of the structure); nothing precedes the impression of the posted One", "named_hypothesis": {"name": "H_tau", "status": "OPEN", "content": "tau is Newton's mass and Einstein's metric", "used_by_a_theorem": False, "pending_external": "ORDEM 025 to Codex (sha16 3fd2b5a801071343): types it by the Bisognano-Wichmann light front"}, "adendum_reading_superseded": "w(I)=1 is the INERTIA (adendo of 03-04/09/2026, the scribe's reading)"}
    if not f_["formal"]:
        out_["verdict"] = _V401_RECUSA % ("FALSIDADE_DA_INERCIA", "FORMAL_OR_SOURCE_EVIDENCE")
    elif not beta_ok_:
        out_["verdict"] = _V401_RECUSA % ("FALSIDADE_DA_INERCIA", "BETA_IS_NOT_ALPHA_SQRT_E")
    else:
        try:
            mec_ = v401_falsidade_mechanics(beta_rt_)
            out_.update(runtime_executed=True, mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], all_verified=bool(mec_["passed"]))
            out_["verdict"] = (t_["veredito_ok"] if mec_["passed"] else _V401_RECUSA % ("FALSIDADE_DA_INERCIA", "MECHANICS_CHECK_FAILED"))
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V401_RECUSA % ("FALSIDADE_DA_INERCIA", "RUNTIME_ERROR")
    core["falsidade_da_inercia_v401"] = out_
    return out_
