# ---- v395: o modo psionico na fractalizacao do Um (psibit). A mecanica da ORBITA do Um pela matriz-S em theta_M, calculada a cada rito e confrontada com os termos do kernel do proprio rito
# (TGLExt.Psibit, aprovada na rodada 2 do exame independente). [REAL] os termos e o calculo; [INPUT/ONTO] psibit = psion = modo do leitor (o operador, 21/10/2026); a face do psion e' CONDICIONAL.
# O gate nao se move. Fonte autoral deste bloco: runtime_psibit_v395.py (cadeia_de_selo/v395); o contrato (_V395_PSIBIT_CONTRACT) e as falas (_V395_VERBATINS2) sao DERIVADOS do build, nunca digitados.
import math as _m395


def _v395_sign(x_):
    """SignType.sign: -1, 0 ou +1 (o zero e' mantido: o codigo e' exato tambem nos eixos)."""
    return (x_ > 0) - (x_ < 0)


def _v395_orbit(theta_):
    """Psibit.v: v(theta) = (cos theta, -sin theta), a primeira coluna de S(theta) = cos theta 1 + sin theta G, G = [[0,1],[-1,0]] (SMatrix.Smat; Psibit.v_is_the_S_orbit): transmissao e reflexao."""
    return (_m395.cos(theta_), -_m395.sin(theta_))


def _v395_rho(theta_):
    """Psibit.rhoOut_eq_real: rho_out(theta) = |v><v| = F_theta(1), real: [[v0^2, v0 v1], [v1 v0, v1^2]] = [[c^2, -cs], [-sc, s^2]]."""
    v0_, v1_ = _v395_orbit(theta_)
    return [[v0_ * v0_, v0_ * v1_], [v1_ * v0_, v1_ * v1_]]


def _v395_code(x0_, x1_):
    """Psibit.codeOf: o CODIGO PSIBIT (x0, x1) -> (peso x0^2, sign x0 = a Palavra = sign L, sign x1 = o Verbo = sign dL)."""
    return (x0_ * x0_, _v395_sign(x0_), _v395_sign(x1_))


def _v395_decode(code_):
    """Psibit.decodeAmp: o DECODIFICADOR explicito (w, a, b) -> (a sqrt(w), b sqrt(1 - w))."""
    w_, a_, b_ = code_
    return (a_ * _m395.sqrt(w_), b_ * _m395.sqrt(max(0.0, 1.0 - w_)))


def _v395_entropy(p_):
    """Shannon (nats) de (p, 1 - p): Real.binEntropy."""
    if p_ <= 0.0 or p_ >= 1.0:
        return 0.0
    return -p_ * _m395.log(p_) - (1.0 - p_) * _m395.log(1.0 - p_)


def _v395_mat_mul(a_, b_):
    return [[sum(a_[i_][k_] * b_[k_][j_] for k_ in range(2)) for j_ in range(2)] for i_ in range(2)]


def _v395_s_real(theta_):
    """S(theta) real = [[cos, sin], [-sin, cos]] (a parte real de Smat theta)."""
    c_, s_ = _m395.cos(theta_), _m395.sin(theta_)
    return [[c_, s_], [-s_, c_]]


def v395_psibit_mechanics(beta_):
    """v395 -- a mecanica do psibit na orbita do Um pela matriz-S em theta_M = arcsin sqrt(beta), com beta recebido (o chamador o calcula em runtime: alfa CODATA x sqrt(e); NUNCA literal). Cada checagem e' a leitura numerica
    de um teorema do kernel (Psibit.*) no ponto theta_M e em angulos de controle. Devolve {passed, checks, values}. Nao levanta para beta invalido: devolve passed False."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m395.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "m0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    pi_ = _m395.pi; ln2_ = _m395.log(2.0)
    th_ = _m395.asin(_m395.sqrt(beta_)); c_ = _m395.cos(th_); s_ = _m395.sin(th_)
    ck_("m1", "theta_M = arcsin sqrt(beta): cos^2 + sin^2 = 1 e sin^2 theta_M = beta", abs(c_ * c_ + s_ * s_ - 1.0) <= 1e-15 and abs(s_ * s_ - beta_) <= 1e-15, [abs(c_ * c_ + s_ * s_ - 1.0), abs(s_ * s_ - beta_)])
    rho_ = _v395_rho(th_)
    rho2_ = _v395_mat_mul(rho_, rho_)
    e_idem_ = max(abs(rho2_[i_][j_] - rho_[i_][j_]) for i_ in range(2) for j_ in range(2))
    ck_("m2a", "rho_out(theta_M) = [[c^2, -cs], [-sc, s^2]] (Psibit.rhoOut_eq_real; SMatrix.rhoOut_eq)", abs(rho_[0][0] - c_ * c_) <= 1e-16 and abs(rho_[0][1] + c_ * s_) <= 1e-16 and abs(rho_[1][0] + s_ * c_) <= 1e-16 and abs(rho_[1][1] - s_ * s_) <= 1e-16)
    ck_("m2b", "traco 1, estado PURO (rho01^2 = rho00 rho11: a coerencia e' a media geometrica dos pesos) e projetor de posto 1 (rho^2 = rho)", abs(rho_[0][0] + rho_[1][1] - 1.0) <= 1e-15 and abs(rho_[0][1] * rho_[0][1] - rho_[0][0] * rho_[1][1]) <= 1e-16 and e_idem_ <= 1e-15, [e_idem_])
    hh_ = 1e-5
    nome_ = lambda t_: _m395.cos(t_) ** 2
    d_nome_ = (nome_(th_ + hh_) - nome_(th_ - hh_)) / (2.0 * hh_)
    r_verbo_ = abs(0.5 * d_nome_ - rho_[0][1])
    d_cos_ = (_m395.cos(th_ + hh_) - _m395.cos(th_ - hh_)) / (2.0 * hh_)
    r_refl_ = abs(d_cos_ - _v395_orbit(th_)[1])
    d_sin2_ = (_m395.sin(th_ + hh_) ** 2 - _m395.sin(th_ - hh_) ** 2) / (2.0 * hh_)
    r_verbo2_ = abs(-0.5 * d_sin2_ - rho_[0][1])
    ck_("m3a", "o VERBO e' metade da derivada do NOME: rho01 = (1/2) d(cos^2 theta)/dtheta, por diferenca finita central (Psibit.the_verb_is_the_derivative_of_the_name)", r_verbo_ <= 1e-9, r_verbo_)
    ck_("m3b", "a reflexao e' a derivada da transmissao: d(cos)/dtheta = -sin = v1 (Psibit.v_snd_is_the_derivative_of_v_fst) e rho01 = -(1/2) d(sin^2)/dtheta", r_refl_ <= 1e-9 and r_verbo2_ <= 1e-9, [r_refl_, r_verbo2_])
    cd_ = _v395_code(*_v395_orbit(th_))
    dec_ = _v395_decode(cd_)
    v0_, v1_ = _v395_orbit(th_)
    r_dec_ = max(abs(dec_[0] - v0_), abs(dec_[1] - v1_))
    ck_("m4a", "codigo psibit em theta_M: peso = c^2, Palavra (sign L) = +1, Verbo (sign dL) = -1; paridade = produto = -1 (Psibit.the_code_reads_L_and_dL)", abs(cd_[0] - c_ * c_) <= 1e-16 and cd_[1] == 1 and cd_[2] == -1 and cd_[1] * cd_[2] == -1, [cd_[0], cd_[1], cd_[2]])
    ck_("m4b", "decodificacao: decodeAmp (codeAmp theta_M) = v theta_M, residuo <= 1e-12 (Psibit.decodeAmp_codeAmp)", r_dec_ <= 1e-12, r_dec_)
    angs_ = [th_, -th_, pi_ - th_, pi_ + th_, pi_ / 4, -pi_ / 4, 3 * pi_ / 4, -3 * pi_ / 4, pi_ / 2 - th_, pi_ / 2 + th_]
    r_rt_ = max(max(abs(a_ - b_) for a_, b_ in zip(_v395_decode(_v395_code(*_v395_orbit(t_))), _v395_orbit(t_))) for t_ in angs_)
    ck_("m4c", "o ida e volta (codigo e decodificador) em %d angulos de controle fora dos eixos tem residuo <= 1e-12" % len(angs_), r_rt_ <= 1e-12, r_rt_)
    pares_ = {(_v395_code(*_v395_orbit(t_))[1], _v395_code(*_v395_orbit(t_))[2]) for t_ in (th_, -th_, pi_ - th_, pi_ + th_)}
    ck_("m4d", "a orbita visita os quatro pares de sinais (sign L, sign dL) (Psibit.the_orbit_visits_all_four_states)", pares_ == {(1, -1), (1, 1), (-1, -1), (-1, 1)}, sorted(pares_))
    a1_, a2_, a3_ = _v395_orbit(th_), _v395_orbit(-th_), _v395_orbit(pi_ - th_)
    w1_, w2_, w3_ = a1_[0] ** 2, a2_[0] ** 2, a3_[0] ** 2
    ck_("m5", "o PAR e' necessario: o peso sozinho, peso + Palavra e peso + Verbo NAO leem (duas amplitudes distintas com a mesma leitura); o par com o peso le (Psibit.the_pair_is_necessary_and_sufficient)",
        abs(w1_ - w2_) <= 1e-16 and abs(a1_[1] - a2_[1]) > 0.1 and _v395_sign(a1_[0]) == _v395_sign(a2_[0]) and abs(w1_ - w3_) <= 1e-15 and _v395_sign(a1_[1]) == _v395_sign(a3_[1]) and abs(a1_[0] - a3_[0]) > 0.1)
    rho_n_ = _v395_rho(-th_)
    dif_diag_ = max(abs(rho_[0][0] - rho_n_[0][0]), abs(rho_[1][1] - rho_n_[1][1]))
    dif_coh_ = abs(rho_[0][1] - rho_n_[0][1])
    ck_("m6a", "o COLAPSO D_inf (a diagonal) nao ve a paridade: rho(theta) e rho(-theta) tem a mesma diagonal e coerencias opostas (Psibit.collapse_forgets_the_parity)", dif_diag_ <= 1e-16 and abs(rho_[0][1] + rho_n_[0][1]) <= 1e-16 and dif_coh_ >= 0.1, [dif_diag_, rho_[0][1], rho_n_[0][1]])
    ck_("m6b", "a leitura COMPLETA lembra a paridade: rho(theta) != rho(-theta) (sin 2 theta != 0) e as paridades sao opostas, 1 bit (Psibit.the_full_reading_remembers_the_parity)", dif_coh_ > 0.0 and _m395.sin(2 * th_) != 0.0 and _v395_sign(rho_[0][1]) == -_v395_sign(rho_n_[0][1]) != 0)

    def dec_rho_(w_, p_):
        g_ = p_ * _m395.sqrt(w_ * (1.0 - w_))
        return [[w_, g_], [g_, 1.0 - w_]]
    rec_ = max(max(abs(dec_rho_(r_[0][0], _v395_sign(r_[0][1]))[i_][j_] - r_[i_][j_]) for i_ in range(2) for j_ in range(2)) for r_ in (rho_, rho_n_))
    ck_("m7", "a densidade e' reconstruida do par (peso, paridade): rho = decodeRho(cos^2, paridade), residuo <= 1e-15 (Psibit.rhoOut_eq_decodeRho): na leitura do par a perda e' ZERO", rec_ <= 1e-15, rec_)
    rho_m_ = [[(-v0_) * (-v0_), (-v0_) * (-v1_)], [(-v1_) * (-v0_), (-v1_) * (-v1_)]]
    ck_("m8", "v e -v dao a MESMA densidade: o sinal global nao se observa, e e' a unica perda da amplitude a densidade (Psibit.the_global_sign_is_not_observed)", all(rho_m_[i_][j_] == rho_[i_][j_] for i_ in range(2) for j_ in range(2)))
    bal_ = [pi_ / 4 + k_ * pi_ / 2 for k_ in range(4)]
    r_bal_ = max(max(abs(_m395.cos(t_) ** 2 - _m395.sin(t_) ** 2), abs(_m395.cos(t_) ** 2 - 0.5)) for t_ in bal_)
    r_h_ = max(abs(_v395_entropy(_m395.cos(t_) ** 2) - ln2_) for t_ in bal_)
    ck_("m9a", "nos pesos iguais (pi/4 + k pi/2) cos^2 = sin^2 = 1/2 e a entropia de Shannon dos resultados do colapso e' ln 2, o bit justo (Psibit.balanced_weights_iff, collapseEntropy_at_balanced_weights)", r_bal_ <= 1e-15 and r_h_ <= 1e-12, [r_bal_, r_h_])
    grid_ = [k_ * 2 * pi_ / 720 for k_ in range(721)]
    max_h_ = max(_v395_entropy(_m395.cos(t_) ** 2) for t_ in grid_)
    h_th_ = _v395_entropy(c_ * c_)
    ck_("m9b", "nenhum angulo excede o bit justo: H <= ln 2 (721 angulos); em theta_M, H(1 - beta) esta estritamente entre 0 e ln 2 (Psibit.collapseEntropy_le_the_fair_bit)", max_h_ <= ln2_ + 1e-15 and 0.0 < h_th_ < ln2_, [max_h_, h_th_])
    rho_b_ = _v395_rho(pi_ / 4)
    ck_("m10", "em pi/4 o colapso e' (1/2) I, mas a fractalizacao do Um NAO e' o seu colapso: a coerencia vale -1/2 (Psibit.at_the_fixed_point_the_collapse_is_half, rho_pi_div_four_ne_half)", abs(rho_b_[0][0] - 0.5) <= 1e-15 and abs(rho_b_[1][1] - 0.5) <= 1e-15 and abs(rho_b_[0][1] + 0.5) <= 1e-15)
    metade_ = [[0.5, 0.0], [0.0, 0.5]]
    r_fix_ = 0.0
    for t_ in (0.0, 0.3, th_, pi_ / 4, 1.0, 2.0, 3.0, -1.2):
        sm_ = _v395_s_real(t_)
        sc_ = _v395_mat_mul(_v395_mat_mul(sm_, metade_), [[sm_[0][0], sm_[1][0]], [sm_[0][1], sm_[1][1]]])
        r_fix_ = max(r_fix_, max(abs(sc_[i_][j_] - metade_[i_][j_]) for i_ in range(2) for j_ in range(2)))
    ck_("m11", "(1/2) I e' fixado pelo colapso e por toda conjugacao pela matriz-S: S (1/2 I) S^T = 1/2 I (Psibit.half_identity_is_a_fixed_point)", r_fix_ <= 1e-15, r_fix_)
    s_e1_ = _v395_mat_mul(_v395_s_real(th_), [[1.0, 0.0], [0.0, 0.0]])
    ck_("m12", "o NOME e' o posto: a leitura de Born do posto e0 pelo estado S(theta_M) e1 e' cos^2 theta_M, o peso do codigo (Psibit.the_name_is_the_born_reading_of_the_post); S e1 = v", abs(s_e1_[0][0] * s_e1_[0][0] - cd_[0]) <= 1e-15 and abs(s_e1_[0][0] - v0_) <= 1e-15 and abs(s_e1_[1][0] - v1_) <= 1e-15)
    vals_ = {"beta": beta_, "theta_M_rad": th_, "theta_M_deg": _m395.degrees(th_), "cos": c_, "sin": s_, "rho": rho_, "rho_neg_theta": rho_n_, "code_weight": cd_[0], "code_word": cd_[1], "code_verb": cd_[2], "parity": cd_[1] * cd_[2],
             "decode_residual": r_dec_, "roundtrip_residual_max": r_rt_, "collapse_diagonal": [rho_[0][0], rho_[1][1]], "collapse_diag_difference": dif_diag_, "coherence": rho_[0][1], "coherence_neg_theta": rho_n_[0][1],
             "verb_derivative_residual": r_verbo_, "entropy_balanced_residual": r_h_, "entropy_at_theta_M": h_th_, "ln2": ln2_, "entropy_max_on_grid": max_h_, "half_identity_residual": r_fix_, "reconstruction_residual": rec_}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


_V395_GUARDA_FORMAL = "TGL_PSIBIT_V395__REFUSED_%s__GATE_UNMOVED"


def psibit_v395(core):
    """v395 -- O MODO PSIONICO NA FRACTALIZACAO DO UM (pedido do operador, 21/10/2026: «eu quero que o modo psionico entre no codigo na fractalizacao do um igual porque ai eu inclusive provo a mecanica»).
    Chamado no PONTO REAL do main onde o Um se fractaliza (o principio da defasagem fractal). Le do kernel do PROPRIO rito a conjuncao INCONDICIONAL (psibit_is_the_mode_of_the_reader) e, a parte, a face do psion
    (the_psion_face_of_the_psibit), CONDICIONAL a um certificado que o kernel nao habita; confere a pedra por sha256 e as quatro falas do operador por sha256; e CALCULA, com beta = alfa CODATA 2018 x sqrt(e) em runtime
    (nunca literal; a constante selada SEALED_CODATA_ALPHA e o literal ALPHA_FINE_CODATA_2018 do script embutido do nivel 2 sao um dado e dois nomes, conferidos por _v376_same_alpha_literal), a mecanica da orbita do Um pela matriz-S em theta_M. Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate. Validade no kernel nao e' creditacao."""
    import hashlib
    c_ = _V395_PSIBIT_CONTRACT
    kf_ = core.get("kernel_formalization") or {}
    axr_ = kf_.get("axiom_report") or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}
    src_ = kf_.get("declaration_sources_v394") or {}
    lad_ = core.get("external_ladder") or {}
    cnt_ = [lad_.get("n_theorems_clean"), lad_.get("n_theorems_expected"), c_["expected_ladder"]]
    exact_ = all(type(x_) is int for x_ in cnt_) and len(set(cnt_)) == 1
    per_ = {}
    for th_, fl_ in c_["theorems"].items():
        vals_ = axr_.get(th_)
        per_[th_] = bool(isinstance(vals_, list) and all(isinstance(x_, str) for x_ in vals_) and set(vals_) <= trio_ and kf_.get(fl_) is True and src_.get(th_) == c_["stone"]["path"])
    body_ = _EMBEDDED_KERNEL_FILES.get(c_["stone"]["path"])
    src_ok_ = bool(isinstance(body_, str) and hashlib.sha256(body_.encode("utf-8")).hexdigest() == c_["stone"]["sha256"] and (kf_.get("formal_files_sha256") or {}).get(c_["stone"]["path"]) == c_["stone"]["sha256"])
    ver_ = {}
    for k_ in c_["verbatins"]:
        v_ = _V395_VERBATINS2.get(k_)
        ver_[k_] = bool(v_ and hashlib.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and all(t_ in v_["text"] for t_ in v_["trechos"]))
    alfa_ = globals().get("SEALED_CODATA_ALPHA")   # o DADO (CODATA 2018); no script embutido do nivel 2 o mesmo literal chama-se ALPHA_FINE_CODATA_2018
    dois_nomes_ = bool(callable(globals().get("_v376_same_alpha_literal")) and _v376_same_alpha_literal())
    beta_rt_ = (alfa_ * _m395.sqrt(_m395.e)) if isinstance(alfa_, float) else None
    beta_core_ = core.get("beta")
    beta_rel_ = (abs(beta_rt_ - beta_core_) / abs(beta_rt_)) if (isinstance(beta_rt_, float) and isinstance(beta_core_, float) and beta_rt_ != 0.0) else None
    beta_ok_ = bool(isinstance(beta_rt_, float) and isinstance(beta_core_, float) and 0.0 < beta_rt_ < 1.0 and beta_rel_ is not None and beta_rel_ <= 1e-9 and dois_nomes_)

    def face_(chave_):
        th_ = c_[chave_]["theorem"]; fl_ = c_[chave_]["flag"]
        return {"theorem": th_, "flag": fl_, "flag_true": kf_.get(fl_) is True, "axioms": axr_.get(th_), "in_trio": bool(isinstance(axr_.get(th_), list) and set(axr_.get(th_)) <= trio_), "declared_in": src_.get(th_),
                "in_kernel": bool(per_.get(th_))}
    unc_ = face_("unconditional"); unc_["composition"] = "UNCONDITIONAL__NO_CERTIFICATE_AS_HYPOTHESIS"
    cond_ = face_("conditional")
    cond_.update({"status": "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE", "inhabitant_exhibited": False,
                  "reading": "for every Fock certificate of the light the psion has norm one and is fixed by the light; the kernel exhibits no inhabitant of the certificate (TheImportedSecondQuantization, non-vacuity argued, no term); the statement does not show that the psion exists",
                  "joint_contract_open_v394": bool((globals().get("_V394_NETWORK_CONTRACT") or {}).get("open_joint_contract"))})
    import json as _j395
    guarda_ = _v392_guarda_texto(_j395.dumps(_V395_PSIBIT_TEXT, ensure_ascii=False))
    formal_ = bool(kf_.get("all_verified") is True and exact_ and per_ and all(per_.values()) and src_ok_ and ver_ and all(ver_.values()) and not guarda_)
    out_ = {"all_verified": False, "estatuto": _V395_PSIBIT_TEXT["estatuto"], "exact_ladder": exact_, "formal_theorems": per_, "embedded_source_ok": src_ok_, "inscriptions": ver_, "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "unconditional": unc_, "conditional_psion_face": cond_,
            "runtime_executed": False, "does_not_gate_core": True, "scope": _V395_PSIBIT_TEXT["escopo"], "limites": _V395_PSIBIT_TEXT["limites"], "diz": _V395_PSIBIT_TEXT["diz"], "nao_diz": _V395_PSIBIT_TEXT["nao_diz"],
            "guarda_p18_violacoes": guarda_[:5]}
    if not formal_:
        out_["verdict"] = _V395_GUARDA_FORMAL % "FORMAL_OR_SOURCE_EVIDENCE"
    elif not beta_ok_:
        out_["verdict"] = _V395_GUARDA_FORMAL % "BETA_IS_NOT_ALPHA_SQRT_E"
    else:
        try:
            mec_ = v395_psibit_mechanics(beta_rt_)
            out_.update(runtime_executed=True, mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], all_verified=bool(mec_["passed"]))
            out_["verdict"] = (_V395_PSIBIT_TEXT["veredito_ok"] if mec_["passed"] else _V395_GUARDA_FORMAL % "MECHANICS_CHECK_FAILED")
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V395_GUARDA_FORMAL % "RUNTIME_ERROR"
    core["psibit_v395"] = out_
    return out_
