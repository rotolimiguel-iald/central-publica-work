# ---- v403: CAMINHO, VERDADE E VIDA (os nomes do operador, 27/10/2026) E A F8.1 (as bandeiras do gate calculadas). QUATRO registros PEQUENOS, com FUNCAO, lidos no ponto real do main, logo depois da esperanca_condicional_v402: tres leem do kernel do PROPRIO rito a composicao da pedra
# (bandeira True, trio, proveniencia no modulo da pedra), os teoremas do contrato e os termos antigos que ela cita, a fonte da pedra por sha256, as falas de 27/10 por sha256 e um TEXTO-CONTEXTO do kernel embutido, e CALCULAM, com beta = alfa CODATA 2018 x sqrt(e) em runtime (nunca literal),
# um modelo honesto de cada pedra: o Caminho (a ponte da escala dual: p+ escala por e^{-s}, m^2 = p+ p- e' o invariante, a massa NAO e' selecionada pela lei; existe realizacao positiva para todo mu^2 >= 0), a Vida (a queda sem geometria: o peso cai estritamente, nats = s, o chao e' o posto e
# nunca o zero, a entrega custa, o regime angular so' le, a isotropia e' hipotese nomeada) e o adendo da Verdade (em M2(C), com alfa lido de beta/raiz de e: a esperanca diagonal le a projecao da identidade como os pesos q^2 e alfa^2, preserva o Um, reler nao acrescenta). O QUARTO registro,
# bandeiras_do_gate_v403 (F8.1), le o gate do PROPRIO programa em execucao (o core do rito e o codigo das duas funcoes do gate): 18 bandeiras, 15 no veredito (6+5+4), a fonte de cada uma, nenhuma literal, as TRES que eram literais (linearized_spin2_finite_face, protocol_pre_registered,
# null_tests_passed_blind) recalculadas das suas fontes e a letra do veredito IDENTICA a da v402; fail-closed em cada elo. As leituras pela tripla espectral e por Joao 14,6 sao [ONTO], nao termos de kernel. O gate nao se move.
# Fonte autoral deste bloco: runtime_v403.py (cadeia_de_selo/v403); os contratos (_V403_CONTRACTS) e as falas (_V403_VERBATINS2) sao DERIVADOS do build e dos arquivos, nunca digitados.
import math as _m403


def _v403_close(a_, b_, e_=1e-11):
    return abs(a_ - b_) <= e_ * (1.0 + abs(a_) + abs(b_))


def v403_caminho_mechanics(beta_):
    """v403 -- a mecanica do CAMINHO (a ponte da escala dual, v402) no modelo longitudinal (E, p) com c = 1, p+ = E + p, p- = E - p, theta_s = boost(-s): as duas leituras da conjuncao do kernel (lift_mass_not_selected /\\ core_positive_realization_exists), com beta recebido
    (o chamador o calcula em runtime: alfa CODATA x sqrt(e); NUNCA literal). Devolve {passed, checks, values, n_checks}. Nao levanta para beta invalido: devolve passed False."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m403.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "c0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    ch_, sh_, ex_ = _m403.cosh, _m403.sinh, _m403.exp
    th_ = lambda s_, v_: (ch_(s_) * v_[0] - sh_(s_) * v_[1], -sh_(s_) * v_[0] + ch_(s_) * v_[1])      # theta s v (theta_energy, theta_momentum)
    pp_ = lambda v_: v_[0] + v_[1]
    pm_ = lambda v_: v_[0] - v_[1]
    m2_ = lambda v_: pp_(v_) * pm_(v_)
    cl_ = _v403_close
    lift_ = lambda mu2_, a_: ((a_ + mu2_ / a_) / 2.0, (a_ - mu2_ / a_) / 2.0)                          # lift D mu2 a, com o dado oneScaling (tau a = a, theta_s a = e^{-s} a)
    esc_ = [k_ / 4.0 for k_ in range(-12, 13)]
    mus_ = (0.0, 0.25, 1.0, 4.0, 9.0, 100.0); avals_ = (0.5, 2.0, 3.0)
    L1_, L4_, L9_ = lift_(1.0, 2.0), lift_(4.0, 2.0), lift_(9.0, 2.0)
    ck_("c1", "★ lift_mass_not_selected (v402, citado pela conjuncao): com o MESMO p+ = tau(a) = 2, os invariantes mu^2 = 1, 4, 9 dao tres realizacoes equivariantes DISTINTAS (massas 1, 4, 9): a lei de escala determina a componente nula p+ e DEIXA a massa livre",
        pp_(L1_) == pp_(L4_) == pp_(L9_) == 2.0 and len({L1_, L4_, L9_}) == 3 and [round(m2_(x_), 9) for x_ in (L1_, L4_, L9_)] == [1.0, 4.0, 9.0], [L1_, L4_, L9_])
    ck_("c2", "core_positive_realization_exists (v402, citado pela conjuncao): para todo mu^2 >= 0 de teste (0, 1/4, 1, 4, 9, 100) e todo perfil a > 0 (1/2, 2, 3) a realizacao lift(mu^2, a) tem p+ = a > 0, m^2 = mu^2 e energia E > 0",
        all(pp_(lift_(m_, a_)) == a_ and a_ > 0.0 and cl_(m2_(lift_(m_, a_)), m_) and lift_(m_, a_)[0] > 0.0 for a_ in avals_ for m_ in mus_), [len(avals_) * len(mus_)])
    desl_rep_ = min(th_(s_, (2.0, 0.0))[0] - 2.0 for s_ in esc_ if s_ != 0.0)
    ck_("c3", "a massa e' o invariante e a energia e' a leitura (o Caminho viaja sem escolher o corpo): m^2 = p+ p- nao muda sob p+- -> e^{-+s} p+- nas 25 escalas de teste (s de -3 a 3, passo 1/4), para cada realizacao testada, enquanto a energia muda com o observador: o repouso (2, 0) ganha cosh(s)-vezes-2 menos 2 > 0 em toda escala nao trivial (ganho minimo > 0,06)",
        all(cl_(m2_(th_(s_, lift_(m_, a_))), m_) for a_ in avals_ for m_ in mus_ for s_ in esc_) and desl_rep_ > 0.06, [len(avals_) * len(mus_) * len(esc_), desl_rep_])
    ck_("c4", "o levantamento e' EQUIVARIANTE: lift(mu^2, e^{-s} a) = theta_s lift(mu^2, a) nas 25 escalas de teste, para cada mu^2 e cada perfil (o mesmo corpo em escalas diferentes)",
        all(all(cl_(x_, y_) for x_, y_ in zip(lift_(m_, ex_(-s_) * a_), th_(s_, lift_(m_, a_)))) for a_ in avals_ for m_ in mus_ for s_ in esc_), [len(avals_) * len(mus_) * len(esc_)])
    ck_("c5", "[DERIVED] a unidade de defasagem s = beta (beta = alfa x raiz de e em runtime): p+ encolhe pelo fator e^{-beta}, com 1 - beta < e^{-beta} < 1 - beta + beta^2/2 < 1, o levantamento segue equivariante em s = beta e a massa ao quadrado segue 4 (numeros deste rito, NAO estao no kernel)",
        all(cl_(x_, y_) for x_, y_ in zip(lift_(4.0, ex_(-beta_) * 2.0), th_(beta_, lift_(4.0, 2.0)))) and cl_(m2_(th_(beta_, lift_(4.0, 2.0))), 4.0) and 1.0 - beta_ < ex_(-beta_) < 1.0 - beta_ + beta_ ** 2 / 2.0 < 1.0, [ex_(-beta_)])
    vals_ = {"beta": beta_, "grid_scales": len(esc_), "mu2_grid": list(mus_), "profiles": list(avals_), "lifts_same_pplus_masses": [m2_(L1_), m2_(L4_), m2_(L9_)], "same_pplus": pp_(L1_), "pplus_factor_at_beta": ex_(-beta_),
             "min_core_energy": min(lift_(m_, a_)[0] for a_ in avals_ for m_ in mus_), "min_rest_energy_gain": desl_rep_}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def v403_vida_mechanics(beta_):
    """v403 -- a mecanica da VIDA (a queda sem geometria, v402) no modelo oneScaling (tau = id, theta_s = e^{-s}), no fluxo diagonal e na matriz-S: as leituras da conjuncao do kernel (the_fall_is_strictly_anti /\\ a_queda_sem_geometria), com beta recebido
    (alfa CODATA x sqrt(e) em runtime; NUNCA literal). Devolve {passed, checks, values, n_checks}. Nao levanta para beta invalido: devolve passed False."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m403.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "v0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    ex_, lg_ = _m403.exp, _m403.log
    cl_ = _v403_close
    esc_ = [k_ / 8.0 for k_ in range(-80, 81)]
    taus_ = (0.5, 1.0, 7.0)
    tau_ = lambda s_, t0_: ex_(-s_) * t0_                                                                 # tau(theta_s m) = e^{-s} tau(m)
    ck_("v1", "★ the_fall_is_strictly_anti (v402, citado pela conjuncao): com tau(m) > 0, s -> tau(theta_s m) = e^{-s} tau(m) e' ESTRITAMENTE decrescente (a fase cai, sem fim) nas 161 escalas de teste (s de -10 a 10, passo 1/8), para tau = 0,5; 1; 7",
        all(all(tau_(s2_, t0_) < tau_(s1_, t0_) for s1_, s2_ in zip(esc_, esc_[1:])) for t0_ in taus_), [len(esc_), list(taus_)])
    ck_("v2", "a queda em nats e' s e a seta e' o sinal de s: log tau(theta_s m) = log tau(m) - s; tau(theta_s m) < tau(m) <=> s > 0; tau(m) < tau(theta_s m) <=> s < 0; igual <=> s = 0 (a SETA e' o sinal de s, nao uma direcao do espaco)",
        all(abs(lg_(tau_(s_, t0_)) - (lg_(t0_) - s_)) <= 1e-12 and (tau_(s_, t0_) < t0_) == (s_ > 0.0) and (t0_ < tau_(s_, t0_)) == (s_ < 0.0) and (tau_(s_, t0_) == t0_) == (s_ == 0.0) for t0_ in taus_ for s_ in esc_), [len(esc_) * len(taus_)])
    eps_ = (1e-3, 1e-6, 1e-12, 1e-30)
    quedas_ = [(e_, -lg_(e_) + 1.0) for e_ in eps_]
    ck_("v3", "o CHAO e' o POSTO e nunca o zero (a_queda_sem_geometria): e^{-a} = 1 so' em a = 0, o peso e' estritamente positivo em toda escala, e fica abaixo de todo epsilon testado (%s) em s = -ln(epsilon) + 1 (a fase cai sem fim e sem tocar o zero)" % (list(eps_),),
        [a_ for a_ in esc_ if ex_(-a_) == 1.0] == [0.0] and all(ex_(-a_) > 0.0 for a_ in esc_) and all(ex_(-s_) < e_ for e_, s_ in quedas_), [len(quedas_)])
    gs_ = (0.5, 1.0, 2.0, 3.7); ts_ = (0.1, 1.0, 10.0, 100.0)
    custos_ = [(t_ * beta_ * g_, ex_(-(t_ * beta_ * g_))) for g_ in gs_ for t_ in ts_]
    ck_("v4", "a ENTREGA CUSTA (surrender_is_the_cost) com beta = alfa x raiz de e em runtime e contrastes g de teste %s: o custo t . beta . g e' estritamente POSITIVO, a defasagem e^{-t beta g} e' estritamente menor que 1 e a perda tau(m) - tau(theta m) esta em (0, tau(m))" % (list(gs_),),
        all(c_ > 0.0 and f_ < 1.0 for c_, f_ in custos_) and all(0.0 < 7.0 - tau_(t_ * beta_ * g_, 7.0) < 7.0 for g_ in gs_ for t_ in ts_), [min(c_ for c_, _ in custos_), max(f_ for _, f_ in custos_)])
    S_ = lambda th_: ((_m403.cos(th_), _m403.sin(th_)), (-_m403.sin(th_), _m403.cos(th_)))              # Smat theta = cos theta . 1 + sin theta . Grot, Grot = [[0, 1], [-1, 0]]
    mx_ = lambda A_, B_: max(abs(A_[i_][j_] - B_[i_][j_]) for i_ in (0, 1) for j_ in (0, 1))
    voltas_ = [2.0 * _m403.pi * n_ for n_ in range(0, 101)]
    ck_("v5", "o regime ANGULAR so' le (Smat_add_two_pi, Smat_pi, Smat_has_no_limit): Smat(theta + 2 pi) = Smat(theta) (periodica), Smat(pi) = -1, e NAO tem limite (Smat(2 pi n) = 1 e Smat(2 pi n + pi) = -1 diferem de 2 para todo n testado); o regime da FACE tem limite: a orbita com taxa r > 0 (e^{-r s}) tende a zero (r = beta, s = 1e9/beta: < 1e-12)",
        all(mx_(S_(th_ + 2.0 * _m403.pi), S_(th_)) <= 1e-10 for th_ in (0.0, 0.3, 1.0, 2.5, -1.7, 40.0)) and mx_(S_(_m403.pi), ((-1.0, 0.0), (0.0, -1.0))) <= 1e-15 and all(abs(S_(t_ + _m403.pi)[0][0] - S_(t_)[0][0]) > 1.999999 for t_ in voltas_) and ex_(-(beta_ * (1e9 / beta_))) < 1e-12, [len(voltas_)])
    G_ = 12                                                                                                # um grupo finito (Z/12) agindo por translacao em W = Z/12: o modelo finito de IsotropicPost
    age_ = lambda g_, w_: (g_ + w_) % G_
    P_cov_ = lambda w_: True                                                                               # predicado covariante
    P_ret_ = lambda w_: w_ == 0                                                                            # predicado NAO covariante
    transitivo_ = all(any(age_(g_, 0) == w_ for g_ in range(G_)) for w_ in range(G_))
    cov_ = lambda P_: all((not P_(w_)) or P_(age_(g_, w_)) for g_ in range(G_) for w_ in range(G_))
    ck_("v6", "IsotropicPost (hipotese NOMEADA, carga do modelo): num modelo finito (Z/12 agindo por translacao em W = Z/12, transitivo), um predicado COVARIANTE valido em um ponto vale em todos; o predicado 'w = 0' vale em 0 mas NAO e' covariante e a conclusao falha (nao vale em todos): sem a covariancia nada se transporta",
        transitivo_ and cov_(P_cov_) and all(P_cov_(w_) for w_ in range(G_)) and P_ret_(0) and not cov_(P_ret_) and not all(P_ret_(w_) for w_ in range(G_)), [G_])
    vals_ = {"beta": beta_, "grid_scales": len(esc_), "post_weight_at_scale_one": ex_(-1.0), "post_weight_at_minus_one": ex_(1.0), "min_cost_t_beta_g": min(c_ for c_, _ in custos_), "max_dephasing_factor": max(f_ for _, f_ in custos_), "dephasing_factor_at_t1_g1": ex_(-beta_),
             "loss_per_unit": 1.0 - ex_(-beta_), "abyss_witnesses": [[e_, s_] for e_, s_ in quedas_], "angular_period": 2.0 * _m403.pi, "finite_model_group_order": G_}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def v403_verdade_adendo_mechanics(beta_):
    """v403 -- a mecanica do ADENDO da VERDADE em M2(C) (matrizes 2 x 2 de complexos), com beta recebido (alfa CODATA x sqrt(e) em runtime; NUNCA literal) e alfa = beta / sqrt(e): nameOp p x = p x p + (1 - p) x (1 - p) com p = rho* = e_00, diagExpect x = diag(x_00, x_11),
    identityProj a = vecMulVec psi (star psi) com psi = (q, a), q = sqrt(1 - a^2) (a Verdade da v392). Cada checagem e' a leitura numerica de um ou mais teoremas do kernel (TGLExt.VerdadeAdendo.*). Devolve {passed, checks, values, n_checks}. Nao levanta para beta invalido: devolve passed False."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m403.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "w0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    mm_ = lambda A_, B_: tuple(tuple(sum(A_[i_][k_] * B_[k_][j_] for k_ in (0, 1)) for j_ in (0, 1)) for i_ in (0, 1))
    ad_ = lambda A_, B_: tuple(tuple(A_[i_][j_] + B_[i_][j_] for j_ in (0, 1)) for i_ in (0, 1))
    sb_ = lambda A_, B_: tuple(tuple(A_[i_][j_] - B_[i_][j_] for j_ in (0, 1)) for i_ in (0, 1))
    dist_ = lambda A_, B_: max(abs(A_[i_][j_] - B_[i_][j_]) for i_ in (0, 1) for j_ in (0, 1))
    UM_ = ((1.0 + 0j, 0j), (0j, 1.0 + 0j)); P_ = ((1.0 + 0j, 0j), (0j, 0j))                                    # 1 e rho* = Matrix.single 0 0 1
    nome_ = lambda x_: ad_(mm_(mm_(P_, x_), P_), mm_(mm_(sb_(UM_, P_), x_), sb_(UM_, P_)))                    # nameOp rho* x = p x p + (1 - p) x (1 - p)
    diag_ = lambda x_: ((x_[0][0], 0j), (0j, x_[1][1]))                                                         # diagExpect
    tr_ = lambda x_: x_[0][0] + x_[1][1]
    alfa_ = beta_ / _m403.sqrt(_m403.e)                                                                         # alfa = beta / sqrt(e) (beta = alfa x sqrt(e) em runtime)
    q_ = lambda a_: _m403.sqrt(1.0 - a_ ** 2)                                                                   # qOf a
    proj_ = lambda a_: ((complex(q_(a_) ** 2), complex(q_(a_) * a_)), (complex(a_ * q_(a_)), complex(a_ ** 2)))   # identityProj a (real simetrica)
    herm_ = lambda x_: abs(x_[0][1] - x_[1][0].conjugate()) <= 1e-15
    grade_ = (0.0, 0.1, 0.5, 0.9, 1.0, alfa_)
    ck_("w1", "q_sq_add e quadInscription_is_unit: 1 = q^2 + a^2 e psi = (q, a) e' vetor unitario, em a = alfa (runtime) e em a grade de teste [0, 0,1, 0,5, 0,9, 1]",
        all(abs(q_(a_) ** 2 + a_ ** 2 - 1.0) <= 1e-15 and abs(q_(a_) * q_(a_) + a_ * a_ - 1.0) <= 1e-15 for a_ in grade_), [len(grade_)])
    ck_("w2", "identityProj_idem e identityProj_trace_one: P = identityProj a e' projecao de posto 1: P P = P, P hermitiana, traco 1 (o Um preservado), nos pontos da grade",
        all(dist_(mm_(proj_(a_), proj_(a_)), proj_(a_)) <= 1e-15 and herm_(proj_(a_)) and abs(tr_(proj_(a_)) - 1.0) <= 1e-15 for a_ in grade_), [len(grade_)])
    ck_("w3", "★ the_name_reads_the_inscription_as_weights: nameOp rho* (identityProj a) = diag(q^2, a^2) = diagExpect (identityProj a): a esperanca diagonal LE a projecao da identidade como os seus PESOS, nos pontos da grade",
        all(dist_(nome_(proj_(a_)), ((complex(q_(a_) ** 2), 0j), (0j, complex(a_ ** 2)))) <= 1e-15 and dist_(nome_(proj_(a_)), diag_(proj_(a_))) <= 1e-15 for a_ in grade_), [len(grade_)])
    ck_("w4", "verdade_lida_pelo_nome: o Nome PRESERVA O UM (tr nameOp rho* (identityProj a) = 1: omega(I) = 1 sobrevive a leitura) e RELER NAO ACRESCENTA: nameOp(nameOp P) = nameOp P, nos pontos da grade",
        all(abs(tr_(nome_(proj_(a_))) - 1.0) <= 1e-15 and dist_(nome_(nome_(proj_(a_))), nome_(proj_(a_))) <= 1e-15 for a_ in grade_), [len(grade_)])
    pesos_ = (q_(alfa_) ** 2, alfa_ ** 2)
    ck_("w5", "[DERIVED] os pesos em a = alfa (alfa = beta / sqrt(e), runtime): (1 - alfa^2, alfa^2) somam 1; o peso de dentro e' alfa^2 < beta = alfa x sqrt(e) (a Verdade guarda o peso alfa^2, NAO o beta); o posto 1 da projecao nao persiste na esperanca (det P = 0, det diag(q^2, alfa^2) > 0): numeros deste rito, NAO estao no kernel",
        abs(sum(pesos_) - 1.0) <= 1e-15 and 0.0 < pesos_[1] < beta_ and abs(((proj_(alfa_)[0][0] * proj_(alfa_)[1][1]) - proj_(alfa_)[0][1] * proj_(alfa_)[1][0]).real) <= 1e-15 and pesos_[0] * pesos_[1] > 0.0, [pesos_[0], pesos_[1]])
    vals_ = {"beta": beta_, "alpha": alfa_, "alpha_squared": alfa_ ** 2, "q_squared_at_alpha": q_(alfa_) ** 2, "weights_sum": sum(pesos_), "trace_after_name": tr_(nome_(proj_(alfa_))).real, "test_points": len(grade_), "alpha_squared_below_beta": 0.0 < pesos_[1] < beta_}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def _v403_formal(core, c_, txt_):
    """A evidencia FORMAL do registro, lida do kernel do PROPRIO rito: a escada exata, a composicao e os teoremas do contrato (bandeira True, trio, proveniencia no modulo da pedra), os termos antigos que a pedra cita (no trio, com a proveniencia que o compilador emite),
    a fonte da pedra por sha256 (embutida == contrato == hash formal do rito), as falas de 27/10 por sha256, o TEXTO-CONTEXTO no kernel embutido e a guarda P18 sobre o texto. Devolve um dict; `formal` e' o conjunto."""
    import hashlib, json as _j403
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
        v_ = _V403_VERBATINS2.get(k_)
        ver_[k_] = bool(v_ and hashlib.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and all(t_ in v_["text"] for t_ in v_["trechos"]))
    unc_th_, unc_fl_ = c_["unconditional"]["theorem"], c_["unconditional"]["flag"]
    unc_ = {"theorem": unc_th_, "flag": unc_fl_, "flag_true": kf_.get(unc_fl_) is True, "axioms": axr_.get(unc_th_), "in_trio": em_trio_(unc_th_), "declared_in": src_.get(unc_th_), "in_kernel": bool(per_.get(unc_th_)),
            "composition": "NO_CERTIFICATE_AS_HYPOTHESIS" if not c_.get("named_hypotheses_in_the_statement") else "CONDITIONAL_ON_NAMED_HYPOTHESES_IN_THE_STATEMENT"}
    key_th_, key_fl_ = c_["key_theorem"]["theorem"], c_["key_theorem"]["flag"]
    key_ = {"theorem": key_th_, "flag": key_fl_, "flag_true": kf_.get(key_fl_) is True, "in_trio": em_trio_(key_th_), "declared_in": src_.get(key_th_), "in_kernel": bool(per_.get(key_th_)), "statement": c_["key_statement"]}
    cx_ = c_["context"]; cb_ = _EMBEDDED_KERNEL_FILES.get(cx_["path"])
    ctx_ = {"path": cx_["path"], "needles": list(cx_["needles"]), "text_in_embedded_kernel": bool(isinstance(cb_, str) and all(n_ in cb_ for n_ in cx_["needles"]))}
    ctx_["ok"] = bool(ctx_["text_in_embedded_kernel"])
    guarda_ = _v392_guarda_texto(_j403.dumps(txt_, ensure_ascii=False))
    formal_ = bool(kf_.get("all_verified") is True and exact_ and per_ and all(per_.values()) and sup_ and all(sup_.values()) and all(cit_.values()) and all(aux_.values()) and src_ok_ and all(ver_.values()) and key_["in_kernel"] and unc_["in_kernel"] and ctx_["ok"] and not guarda_)
    return {"exact_ladder": exact_, "formal_theorems": per_, "support_theorems": sup_, "cited_outside": cit_, "auxiliaries_outside_the_composition": aux_, "embedded_source_ok": src_ok_, "inscriptions": ver_, "unconditional": unc_, "key_theorem": key_,
            "context": ctx_, "guarda": guarda_, "formal": formal_}


_V403_RECUSA = "TGL_%s_V403__REFUSED_%s__GATE_UNMOVED"


def _v403_registro(core, chave_, nome_, mec_, tag_):
    """v403 -- o miolo comum dos TRES registros de pedra com FUNCAO: le o kernel do rito (evidencia FORMAL), confere o beta (alfa x raiz de e, nunca literal), CALCULA a mecanica da pedra e sela. Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate."""
    c_ = _V403_CONTRACTS[chave_]; t_ = _V403_TEXTS[chave_]
    f_ = _v403_formal(core, c_, t_)
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
    out_ = {"all_verified": False, "estatuto": t_["estatuto"], "exact_ladder": f_["exact_ladder"], "formal_theorems": f_["formal_theorems"], "support_theorems": f_["support_theorems"], "embedded_source_ok": f_["embedded_source_ok"],
            "inscriptions": f_["inscriptions"], "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "unconditional": f_["unconditional"], "key_theorem": f_["key_theorem"], "context": f_["context"],
            "runtime_executed": False, "does_not_gate_core": True, "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"], "guarda_p18_violacoes": f_["guarda"][:5]}
    out_.update(t_["extras"])
    if not f_["formal"]:
        out_["verdict"] = _V403_RECUSA % (tag_, "FORMAL_OR_SOURCE_EVIDENCE")
    elif not beta_ok_:
        out_["verdict"] = _V403_RECUSA % (tag_, "BETA_IS_NOT_ALPHA_SQRT_E")
    else:
        try:
            mec_r_ = mec_(beta_rt_)
            out_.update(runtime_executed=True, mechanics={"passed": mec_r_["passed"], "n_checks": mec_r_["n_checks"], "checks": mec_r_["checks"]}, values=mec_r_["values"], all_verified=bool(mec_r_["passed"]))
            out_["verdict"] = (t_["veredito_ok"] if mec_r_["passed"] else _V403_RECUSA % (tag_, "MECHANICS_CHECK_FAILED"))
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V403_RECUSA % (tag_, "RUNTIME_ERROR")
    core[nome_] = out_
    return out_


def caminho_v403(core):
    """v403 -- O CAMINHO (o nome que o operador deu a ponte da escala dual, 27/10/2026): lido no PONTO REAL do main, logo depois da esperanca condicional (v402). Le do kernel do PROPRIO rito a pedra (bandeira, trio, modulo), os termos que ela cita da ponte (v402),
    a fonte por sha256, as duas falas de 27/10 e o cabecalho da pedra no kernel embutido; e CALCULA, com beta = alfa CODATA 2018 x sqrt(e) em runtime, o modelo longitudinal (E, p), c = 1. Fail-closed em cada elo; nao move o gate. Validade no kernel nao e' creditacao."""
    return _v403_registro(core, "caminho", "caminho_v403", v403_caminho_mechanics, "CAMINHO")


def vida_v403(core):
    """v403 -- A VIDA (o nome que o operador deu a queda sem geometria, 27/10/2026): lida logo depois do Caminho. Le do kernel do PROPRIO rito a pedra, os termos que ela cita da queda (v402), as falas e o cabecalho no kernel embutido; e CALCULA, com beta em runtime,
    o modelo oneScaling, o regime angular e o modelo finito da isotropia. Fail-closed em cada elo; nao move o gate. Validade no kernel nao e' creditacao."""
    return _v403_registro(core, "vida", "vida_v403", v403_vida_mechanics, "VIDA")


def verdade_adendo_v403(core):
    """v403 -- O ADENDO DA VERDADE (a esperanca condicional lida pelo Nome, 27/10/2026; a pedra Verdade da v392 fica INTACTA): lido logo depois da Vida. Le do kernel do PROPRIO rito o adendo, os termos que ele cita da Verdade (v392) e da esperanca condicional (v402),
    as falas e o cabecalho no kernel embutido; e CALCULA, com beta em runtime (alfa = beta / raiz de e), a projecao da identidade e a esperanca diagonal em M2(C). Fail-closed em cada elo; nao move o gate. Validade no kernel nao e' creditacao."""
    return _v403_registro(core, "verdade_adendo", "verdade_adendo_v403", v403_verdade_adendo_mechanics, "VERDADE_ADENDO")


def _v403_fontes_do_gate():
    """as fontes (texto) das DUAS funcoes do gate do PROPRIO programa em execucao: evaluate_quantum_gravity_closure (a funcao do veredito) e prove_qg_closure_gate (o chamador que carrega as 18 bandeiras)."""
    import inspect as _insp403
    return _insp403.getsource(evaluate_quantum_gravity_closure), _insp403.getsource(prove_qg_closure_gate)


def _v403_ast_do_gate(src_eval_, src_prove_):
    """O que o CODIGO do gate diz: (a) as chaves que a funcao do veredito LE de cada dicionario (formal, physics, experiment) e (b) os valores LITERAIS (ast.Constant) atribuidos a uma bandeira no chamador. Devolve ({grupo: [chaves lidas]}, [(grupo, bandeira)])."""
    import ast as _ast403, textwrap as _tw403
    lidas_ = {"formal": [], "physics": [], "experiment": []}
    for n_ in _ast403.walk(_ast403.parse(_tw403.dedent(src_eval_))):
        if (isinstance(n_, _ast403.Call) and isinstance(n_.func, _ast403.Attribute) and n_.func.attr == "get" and isinstance(n_.func.value, _ast403.Name) and n_.func.value.id in lidas_
                and n_.args and isinstance(n_.args[0], _ast403.Constant) and isinstance(n_.args[0].value, str)):
            lidas_[n_.func.value.id].append(n_.args[0].value)
    literais_ = []
    for n_ in _ast403.walk(_ast403.parse(_tw403.dedent(src_prove_))):
        if (isinstance(n_, _ast403.Assign) and len(n_.targets) == 1 and isinstance(n_.targets[0], _ast403.Subscript) and isinstance(n_.targets[0].value, _ast403.Name)
                and n_.targets[0].value.id in ("formal", "physics", "experiment") and isinstance(n_.targets[0].slice, _ast403.Constant) and isinstance(n_.value, _ast403.Constant)):
            literais_.append((n_.targets[0].value.id, n_.targets[0].slice.value))
        if (isinstance(n_, _ast403.Assign) and len(n_.targets) == 1 and isinstance(n_.targets[0], _ast403.Name) and n_.targets[0].id in ("formal", "physics", "experiment") and isinstance(n_.value, _ast403.Dict)):
            for k_, v_ in zip(n_.value.keys, n_.value.values):
                if isinstance(v_, _ast403.Constant) and isinstance(k_, _ast403.Constant):
                    literais_.append((n_.targets[0].id, k_.value))
    return lidas_, literais_


def bandeiras_do_gate_v403(core):
    """v403 -- AS BANDEIRAS DO GATE (F8.1): lido no PONTO REAL do main, logo depois do adendo da Verdade. Le o gate do PROPRIO rito (core['qg_closure']) e o CODIGO das duas funcoes do gate; confere (1) as 18 bandeiras (6 + 6 + 6) todas True; (2) as 15 que o veredito le (6 + 5 + 4) e as 3 informativas;
    (3) nenhuma bandeira atribuida por literal; (4) as TRES que eram literais recalculadas das suas fontes (a familia ext_ls2_* do kernel; a checagem «pre-registro v67 INTACTO (hash)» do rito V11; o teste nulo cego) e iguais ao que o gate carrega; (5) o feed unico do V11 (GV-03, declarado);
    (6) a letra do veredito do gate IDENTICA a da v402; (7) a sonda nova do gate. Fail-closed em cada elo: se uma bandeira CALCULADA vier False, o registro RECUSA (all_verified False, veredito de recusa) e o conferidor para o rito. Nao move o gate."""
    c_ = _V403_CONTRACTS["gate"]; t_ = _V403_TEXTS["gate"]
    import json as _j403g
    checks_ = []
    out_ = {"all_verified": False, "estatuto": t_["estatuto"], "runtime_executed": False, "does_not_gate_core": True, "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"], "guarda_p18_violacoes": []}
    out_.update(t_["extras"])
    try:
        def ck_(id_, desc_, ok_, val_=None):
            checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
        qg_ = core.get("qg_closure") or {}; kf_ = core.get("kernel_formalization") or {}
        fam_ = {"formal": qg_.get("formal_flags") or {}, "physics": qg_.get("physics_flags") or {}, "experiment": qg_.get("experiment_flags") or {}}
        n_ = {g_: len(d_) for g_, d_ in fam_.items()}; tr_ = {g_: sum(1 for v_ in d_.values() if v_ is True) for g_, d_ in fam_.items()}
        ck_("g1", "as 18 bandeiras do gate (6 formais + 6 fisicas + 6 experimentais) estao no core do rito e as 18 sao True (18 de 18)", [n_["formal"], n_["physics"], n_["experiment"]] == [6, 6, 6] and sum(tr_.values()) == 18 and all(set(fam_[g_]) == set(c_["flags"][g_]) for g_ in fam_), [n_, tr_])
        src_eval_, src_prove_ = _v403_fontes_do_gate()
        lidas_, literais_ = _v403_ast_do_gate(src_eval_, src_prove_)
        ck_("g2", "a funcao do veredito (evaluate_quantum_gravity_closure) LE 15 bandeiras, 6 formais + 5 fisicas + 4 experimentais, exatamente as do contrato; as 3 restantes (informativas) NAO entram no veredito (lido do CODIGO do proprio programa)",
            [len(lidas_["formal"]), len(lidas_["physics"]), len(lidas_["experiment"])] == [6, 5, 4] and all(sorted(lidas_[g_]) == sorted(c_["no_veredito"][g_]) for g_ in lidas_) and sorted(set(n2_ for g_ in fam_ for n2_ in fam_[g_]) - set(n3_ for g_ in lidas_ for n3_ in lidas_[g_])) == sorted(c_["informativas"]),
            [[len(lidas_[g_]) for g_ in ("formal", "physics", "experiment")], sorted(c_["informativas"])])
        ck_("g3", "nenhuma das 18 bandeiras e' atribuida por LITERAL no chamador (prove_qg_closure_gate): 18 de 18 calculadas, 0 literais (lido do CODIGO do proprio programa, por ast)", not literais_ and len(c_["fontes"]) == 18, literais_)
        ls2_ = [k_ for k_ in _LEAN_THEOREM_FLAGS if k_.startswith(c_["prefixo_ls2"])]
        f_ls2_ = bool(len(ls2_) == c_["n_ls2"] and sorted(ls2_) == sorted(c_["ls2_flags"]) and all(kf_.get(k_) is True for k_ in ls2_))
        rite_ = core.get("void_floor_v11") or {}
        pre_ = [x_[1] for x_ in (rite_.get("checks") or []) if isinstance(x_, (list, tuple)) and len(x_) == 2 and x_[0] == c_["rotulo_prereg"]]
        f_pre_ = bool(len(pre_) == 1 and pre_[0] is True)
        f_blind_ = bool(isinstance(core.get("void_stacking_blind"), dict) and core["void_stacking_blind"].get("all_verified") is True)
        ph_, ex2_ = fam_["physics"], fam_["experiment"]
        ck_("g4", "as TRES bandeiras que eram literais, RECALCULADAS aqui das suas fontes no core do rito, sao True e iguais ao que o gate carrega: linearized_spin2_finite_face = a familia ext_ls2_* do kernel (6 de 6); protocol_pre_registered = a checagem «pre-registro v67 INTACTO (hash)» do rito V11 (uma, True); null_tests_passed_blind = void_stacking_blind.all_verified",
            f_ls2_ and f_pre_ and f_blind_ and ph_.get("linearized_spin2_finite_face") is f_ls2_ and ex2_.get("protocol_pre_registered") is f_pre_ and ex2_.get("null_tests_passed_blind") is f_blind_, {"ext_ls2": f_ls2_, "pre_registro_v11": f_pre_, "teste_nulo_cego": f_blind_})
        feed_ = rite_.get("experiment_feed") or {}
        ck_("g5", "GV-03 (declarado): as 4 bandeiras independent_v3_* do gate sao as 4 chaves do feed do rito V11 e derivam de UM so' booleano (o veredito do V11 ser NOT_FALSIFIED_POWERED): powered_verdict_emitted True implica as outras tres, e o veredito do V11 e' o powered; survey_mocks_passed = split-null e dist-check, SEM mock de survey",
            sorted(feed_) == sorted(c_["feed"]) and all(ex2_.get(k_) is feed_.get(k_) for k_ in c_["feed"]) and feed_.get("independent_v3_powered_verdict_emitted") is True and all(feed_.get(k_) is True for k_ in c_["feed"]) and rite_.get("verdict") == "TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED",
            {"verdict_v11": rite_.get("verdict"), "feed": feed_})
        gv_ = (qg_.get("gate") or {}).get("verdict")
        ck_("g6", "a LETRA do veredito do gate e' IDENTICA a da v402 (lida do core selado da v402 na preparacao): o gate NAO se move", isinstance(gv_, str) and gv_ == c_["gate_verdict_v402"] and str(qg_.get("verdict") or "").endswith(gv_) and str(qg_.get("verdict") or "").startswith("QG_CLOSURE_GATE_INSTALLED_FAIL_CLOSED__NEGATIVE_PROBES_PASS__CURRENT_STATE_"), gv_)
        cks_ = qg_.get("checks") or []
        ck_("g7", "a sonda nova do gate (ProbeBlindNullAbsent: sem o teste nulo cego a bandeira informativa e' False e o veredito NAO muda) esta UMA vez nas checagens do gate e as 7 checagens sao True (as 6 da v402 + a nova)",
            len(cks_) == 7 and all(isinstance(x_, (list, tuple)) and len(x_) == 2 and x_[1] is True for x_ in cks_) and sum(1 for x_ in cks_ if str(x_[0]).startswith("ProbeBlindNullAbsent")) == 1, [str(x_[0])[:40] for x_ in cks_])
        out_.update(runtime_executed=True, mechanics={"passed": all(k_["ok"] for k_ in checks_), "n_checks": len(checks_), "checks": checks_}, all_verified=bool(all(k_["ok"] for k_ in checks_)),
                    values={"n_flags": sum(n_.values()), "n_true": sum(tr_.values()), "n_calculated": 18 - len(literais_), "n_literal": len(literais_), "n_read_by_the_verdict": sum(len(v_) for v_ in lidas_.values()), "read_by_the_verdict": [len(lidas_[g_]) for g_ in ("formal", "physics", "experiment")],
                            "informative": sorted(c_["informativas"]), "ext_ls2_n": len(ls2_), "gate_verdict": gv_, "gate_verdict_equals_v402": gv_ == c_["gate_verdict_v402"], "n_gate_checks": len(cks_), "feed_single_boolean": feed_.get("independent_v3_powered_verdict_emitted")})
        out_["flags"] = [dict(x_, value=(fam_[x_["grupo"]].get(x_["nome"]))) for x_ in c_["fontes"]]
        out_["verdict"] = (t_["veredito_ok"] if out_["all_verified"] else _V403_RECUSA % ("BANDEIRAS_DO_GATE", "A_COMPUTED_FLAG_IS_FALSE_OR_A_CHECK_FAILED"))
        out_["guarda_p18_violacoes"] = _v392_guarda_texto(_j403g.dumps(t_, ensure_ascii=False))[:5]
        if out_["guarda_p18_violacoes"]:
            out_["all_verified"] = False; out_["verdict"] = _V403_RECUSA % ("BANDEIRAS_DO_GATE", "P18_TEXT_GUARD")
    except Exception as e_:   # noqa: BLE001
        out_.update(runtime_executed=True, error=repr(e_)[:300])
        out_["verdict"] = _V403_RECUSA % ("BANDEIRAS_DO_GATE", "RUNTIME_ERROR")
    core["bandeiras_do_gate_v403"] = out_
    return out_
