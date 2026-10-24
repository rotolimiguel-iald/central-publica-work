# ---- v398: o SONICO e a AFINACAO DAS CORDAS. Dois registros PEQUENOS, com FUNCAO, lidos no ponto real do main, junto dos registros das pedras anteriores (psibit_v395, testemunha_estatica_v396): cada um LE do kernel do PROPRIO rito a composicao
# incondicional da sua pedra (bandeira True, trio, proveniencia no modulo da pedra), os teoremas e os termos antigos que ela cita, a fonte da pedra por sha256 e as inscricoes de 23/10 por sha256, e CONFERE numericamente o que os teoremas dizem.
# SONICO: com beta = alfa CODATA 2018 x sqrt(e) em runtime (nunca literal) -- ln 2 = K.octaveNats 1 = o bit justo, exp(ln 2) = 2, n oitavas = n bits, o pino nao e' a meia-nat, o seletor pina, e a entropia do colapso no angulo da TGL,
# H2(cos^2 theta_M, sin^2 theta_M), em nats e em oitavas: numero DERIVADO neste rito, nao esta no kernel. AFINACAO DAS CORDAS: aritmetica exata -- zeta(-1) = -1/12 e zeta(-1, 1/2) = 1/24 (valores citados de Mathlib, conferidos por Bernoulli em fracoes),
# D = 26 e D = 10 como unicas solucoes, d = D - 1 = 9 (o d da casa e' [DECLARADO]), a torre omega_n = n.kappa (so' a FORMA: o kappa do boost nao esta no core, no kernel e' entrada) e os retornos. A hipotese MasslessFirstLevel e' [KNOWN]; nada deriva
# cordas do axioma; a geometria e' [OPEN]. [INPUT/ONTO] as inscricoes de 23/10/2026. O gate nao se move. Fonte autoral deste bloco: runtime_pedras_v398.py (cadeia_de_selo/v398); os contratos (_V398_SONICO_CONTRACT, _V398_AFINACAO_CONTRACT) e as
# inscricoes (_V398_VERBATINS2) sao DERIVADOS do build e dos arquivos, nunca digitados.
import math as _m398
from fractions import Fraction as _F398


def _v398_h2(p_):
    """Shannon (nats) de (p, 1 - p): Real.binEntropy; Psibit.collapseEntropy theta = binEntropy (cos theta ^ 2) = H2(cos^2 theta, sin^2 theta)."""
    if p_ <= 0.0 or p_ >= 1.0:
        return 0.0
    return -p_ * _m398.log(p_) - (1.0 - p_) * _m398.log(1.0 - p_)


def v398_sonico_mechanics(beta_):
    """v398 -- a mecanica do SONICO, com beta recebido (o chamador o calcula em runtime: alfa CODATA x sqrt(e); NUNCA literal). Cada checagem e' a leitura numerica de um teorema do kernel (TGLExt.Sonico.*) e acrescenta UM numero derivado (s6).
    K.octaveNats n = n . ln 2 e' o CAMPO per_octave da lei de custo (CollapseCostLaw, [INPUT]). Devolve {passed, checks, values, n_checks}. Nao levanta para beta invalido: devolve passed False."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m398.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "s0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    pi_ = _m398.pi; ln2_ = _m398.log(2.0)
    octave_ = lambda n_: n_ * ln2_
    h_half_ = _v398_h2(0.5)
    ck_("s1a", "pinar UMA oitava cobra o bit justo: K.octaveNats 1 = fairBitEntropy = H2(1/2, 1/2) = ln 2 (one_octave_is_the_parity_bit; fair_bit_entropy_is_log_two)", abs(octave_(1) - h_half_) <= 1e-15 and abs(h_half_ - ln2_) <= 1e-15, [octave_(1), h_half_, ln2_])
    r_n_ = max(abs(octave_(n_) - n_ * h_half_) for n_ in range(65))
    r_add_ = max(abs(octave_(n_ + m_) - (octave_(n_) + octave_(m_))) for n_ in range(33) for m_ in range(33))
    ck_("s1b", "n oitavas pinadas custam n bits: K.octaveNats n = n . fairBitEntropy (n = 0..64) e a contagem e' aditiva (pinning_n_octaves_costs_n_bits; octave_cost_add)", r_n_ <= 1e-12 and r_add_ <= 1e-12, [r_n_, r_add_])
    r_exp_ = abs(_m398.exp(octave_(1)) - 2.0)
    r_pow_ = max(abs(_m398.exp(octave_(n_)) / (2.0 ** n_) - 1.0) for n_ in range(61))
    ck_("s2", "a oitava e' o DOBRO: exp(K.octaveNats 1) = exp(ln 2) = 2 (the_octave_is_a_doubling; the_provable_toll_names_the_octave) e exp(n ln 2) = 2^n (n = 0..60, erro relativo <= 1e-12): o logaritmo leva razoes multiplicativas a contagens aditivas", r_exp_ <= 1e-15 and r_pow_ <= 1e-12, [r_exp_, r_pow_])
    ck_("s3", "o PINO nao e' a meia-nat: K.octaveNats 1 = ln 2 != K.localNats = 1/2, e 1/2 < ln 2 (the_pin_is_not_the_half_nat; local_is_not_one_octave)", ln2_ - 0.5 >= 0.19 and 0.5 < ln2_, ln2_ - 0.5)
    a_ = [complex(1.0, 2.0), complex(0.0, -0.5), complex(0.75, 0.0)]; psi_ = [complex(0.3, -1.0), complex(2.0, 0.0), complex(1.0, 1.0)]
    inner_ = lambda u_, v_: sum(x_.conjugate() * y_ for x_, y_ in zip(u_, v_))
    select_ = lambda a__, x__: [inner_(a__, x__) / inner_(a__, a__) * t_ for t_ in a__]
    s1_ = select_(a_, psi_); sn_ = psi_
    for _ in range(10):
        sn_ = select_(a_, sn_)
    r_idem_ = max(abs(x_ - y_) for x_, y_ in zip(select_(a_, s1_), s1_))
    r_fix_ = max(abs(x_ - y_) for x_, y_ in zip(select_(a_, a_), a_))
    r_iter_ = max(abs(x_ - y_) for x_, y_ in zip(sn_, s1_))
    r_sa_ = abs(inner_(psi_, select_(a_, a_)) - inner_(select_(a_, psi_), a_))
    ck_("s4", "o SELETOR PINA (the_selector_pins; select a psi = <a, psi>/<a, a> a, a projecao ortogonal sobre a reta C.a, em um vetor de teste de C^3): select a (select a psi) = select a psi, select a a = a, e a iteracao 10x e' a mesma que 1x (a memoria permanece: collapse_iteration_is_stable)", max(r_idem_, r_fix_, r_iter_) <= 1e-14, [r_idem_, r_fix_, r_iter_])
    th_ = _m398.asin(_m398.sqrt(beta_)); c_ = _m398.cos(th_); s_ = _m398.sin(th_); c2_ = c_ * c_; s2_ = s_ * s_
    ck_("s5a", "theta_M = arcsin sqrt(beta): cos^2 theta_M + sin^2 theta_M = 1, sin^2 theta_M = beta e cos^2 theta_M = 1 - beta", abs(c2_ + s2_ - 1.0) <= 1e-15 and abs(s2_ - beta_) <= 1e-15 and abs(c2_ - (1.0 - beta_)) <= 1e-15, [abs(c2_ + s2_ - 1.0), abs(s2_ - beta_)])
    bal_ = [pi_ / 4 + k_ * pi_ / 2 for k_ in range(4)]
    r_bal_ = max(abs(_v398_h2(_m398.cos(t_) ** 2) - octave_(1)) for t_ in bal_)
    grid_ = [k_ * 2 * pi_ / 720 for k_ in range(721)]
    max_h_ = max(_v398_h2(_m398.cos(t_) ** 2) for t_ in grid_)
    ck_("s5b", "nos pesos iguais (pi/4 + k pi/2) a entropia dos resultados do colapso e' EXATAMENTE K.octaveNats 1 (collapseEntropy_at_balanced_weights) e nenhum angulo a excede: H <= ln 2 em 721 angulos (collapseEntropy_le_the_fair_bit)", r_bal_ <= 1e-12 and max_h_ <= ln2_ + 1e-15, [r_bal_, max_h_])
    h_nats_ = -c2_ * _m398.log(c2_) - s2_ * _m398.log(s2_)
    h_oct_ = h_nats_ / ln2_
    h_oct_b_ = -c2_ * _m398.log2(c2_) - s2_ * _m398.log2(s2_)
    ck_("s6", "[DERIVED] a entropia do colapso em theta_M, H2(cos^2 theta_M, sin^2 theta_M): a forma direta, a binEntropy(1 - beta) e o logaritmo de base 2 concordam; 0 < H < ln 2 estritamente (theta_M nao e' angulo de pesos iguais); a fracao do bit H/ln 2 esta em (0, 1); numero deste rito, NAO esta no kernel",
        abs(h_nats_ - _v398_h2(1.0 - beta_)) <= 1e-15 and abs(h_oct_ - h_oct_b_) <= 1e-15 and 0.0 < h_nats_ < ln2_ and 0.0 < h_oct_ < 1.0, [h_nats_, h_oct_, h_oct_b_])
    vals_ = {"beta": beta_, "theta_M_rad": th_, "cos2_theta_M": c2_, "sin2_theta_M": s2_, "ln2": ln2_, "fair_bit_entropy": h_half_, "octave_one_nats": octave_(1), "exp_ln2": _m398.exp(octave_(1)), "exp_ln2_residual": r_exp_, "n_octaves_residual": r_n_, "additivity_residual": r_add_,
             "power_of_two_relative_residual": r_pow_, "pin_minus_half_nat": ln2_ - 0.5, "selector_idempotence_residual": r_idem_, "selector_fixes_action_residual": r_fix_, "selector_iteration_residual": r_iter_, "selector_selfadjoint_residual": r_sa_,
             "balanced_weights_residual": r_bal_, "max_collapse_entropy_on_grid": max_h_, "collapse_entropy_theta_M_nats": h_nats_, "collapse_entropy_theta_M_octaves": h_oct_, "collapse_entropy_theta_M_octaves_log2": h_oct_b_}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def _v398_bernoulli(n_):
    """Numeros de Bernoulli B_0..B_n em FRACOES exatas (convencao B_1 = -1/2), pela recorrencia sum_{k=0}^{m} C(m+1, k) B_k = 0."""
    from math import comb
    b_ = [_F398(1)]
    for m_ in range(1, n_ + 1):
        b_.append(-sum(comb(m_ + 1, k_) * b_[k_] for k_ in range(m_)) / _F398(m_ + 1))
    return b_


def _v398_bernoulli_poly(n_, x_, b_):
    from math import comb
    return sum(comb(n_, k_) * b_[k_] * x_ ** (n_ - k_) for k_ in range(n_ + 1))


def v398_afinacao_mechanics():
    """v398 -- a aritmetica da AFINACAO DAS CORDAS, exata (fracoes) e numerica (dupla precisao). Cada checagem e' a leitura de um teorema do kernel (TGLExt.AfinacaoDasCordas.*). O kappa do boost NAO esta no core (no kernel e' entrada:
    kappa_is_input): a FORMA da torre e' conferida com kappa de TESTE. Devolve {passed, checks, values, n_checks}."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    pi_ = _m398.pi
    b_ = _v398_bernoulli(6)
    z1_ = -b_[2] / 2
    zh_ = -_v398_bernoulli_poly(2, _F398(1, 2), b_) / 2
    ck_("z1", "zeta(-1) = -1/12 e zeta(-1, 1/2) = 1/24 (valores citados de Mathlib: zeta_neg_one e hurwitz_zeta_neg_one_half) conferidos aqui por -B_2/2 e -B_2(1/2)/2 em fracoes exatas (B_2 = 1/6, B_2(x) = x^2 - x + 1/6)", z1_ == _F398(-1, 12) and zh_ == _F398(1, 24) and b_[2] == _F398(1, 6), [str(z1_), str(zh_)])
    bos_ = z1_ / 2
    fer_ = -zh_ / 2
    ck_("z2", "por direcao transversal: boson (1/2) zeta(-1) = -1/24; fermion NS -(1/2) zeta(-1, 1/2) = -1/48 (o sinal MENOS e' a estatistica de Fermi [KNOWN]); a soma e' -1/16 (bosonDirection_eq, nsFermionDirection_eq, nsZeroPoint_eq)", bos_ == _F398(-1, 24) and fer_ == _F398(-1, 48) and bos_ + fer_ == _F398(-1, 16), [str(bos_), str(fer_), str(bos_ + fer_)])
    sol_bos_ = [d_ for d_ in range(200) if (d_ - 2) * bos_ == _F398(-1)]
    sol_ns_ = [d_ for d_ in range(200) if (d_ - 2) * (bos_ + fer_) == _F398(-1, 2)]
    sol_bos_mf_ = [d_ for d_ in range(200) if 1 - (d_ - 2) * (-bos_) == 0]
    sol_ns_mf_ = [d_ for d_ in range(200) if _F398(1, 2) - (d_ - 2) * (-(bos_ + fer_)) == 0]
    sol_errado_ = [d_ for d_ in range(200) if (d_ - 2) * (bos_ - fer_) == _F398(-1, 2)]
    ck_("z3", "a dimensao critica e' o FECHO da soma regularizada: -(D-2)/24 = -1 so' em D = 26 (bosonic_critical_dimension) e -(D-2)/16 = -1/2 so' em D = 10 (superstring_critical_dimension), D de 0 a 199; sob MasslessFirstLevel (N - a = 0, N = 1 e N = 1/2) as mesmas solucoes; "
        "controle: com o sinal fermionico trocado o setor NS daria D = 26", sol_bos_ == [26] and sol_ns_ == [10] and sol_bos_mf_ == [26] and sol_ns_mf_ == [10] and sol_errado_ == [26], [sol_bos_, sol_ns_, sol_errado_])
    sol_d_ = [d_ for d_ in range(200) if d_ - 1 == 9]
    ck_("z4", "D = 10 se e so' se d = D - 1 = 9 dimensoes espaciais (the_house_d_nine); o d = 9 da casa e' [DECLARADO] (numeros historicos nao recalculados)", sol_d_ == [10] and sol_ns_ == [10] and all((d_ - 1 == 9) == (d_ == 10) for d_ in range(200)), [sol_d_])
    kap_ = (0.5, 1.0, 2.0, 3.7)
    r_tw_ = r_ratio_ = r_ret_ = r_fund_ = 0.0; ctrl_ = 1e9
    for k_ in kap_:
        p_ = 2.0 * pi_ / k_
        om_ = lambda n_, pp_=p_: n_ * (2.0 * pi_ / pp_)
        r_tw_ = max(r_tw_, max(abs(om_(n_) - n_ * k_) / max(1.0, abs(n_ * k_)) for n_ in range(-8, 9)))
        r_ratio_ = max(r_ratio_, max(abs(om_(m_) / om_(n_) - m_ / n_) for m_ in range(1, 9) for n_ in range(1, 9)))
        r_ret_ = max(r_ret_, max(abs(_m398.cos(om_(n_) * p_) - 1.0) for n_ in range(1, 65)))
        r_fund_ = max(r_fund_, abs(om_(1) - k_))
        ctrl_ = min(ctrl_, abs(2.0 * pi_ / (1.1 * p_) - k_))
    ck_("z5", "o circulo da leitura e a torre de Matsubara (kappa de TESTE %s; o kappa do boost nao esta no core): com P = 2 pi/kappa, omega_n = n.kappa, omega_m/omega_n = m/n (razoes racionais), omega_1 = kappa, todos os modos voltam em t = P (cos(omega_n P) = 1, n = 1..64); "
        "controle: P' = 1,1 P nao e' a leitura fiel (omega_1 != kappa) (the_cyclic_closure_of_time_is_the_reading_circle; faithful_iff_fundamental_mode; matsubara_eq_mul_kappa; tower_returns_at_the_period)" % (list(kap_),),
        r_tw_ <= 1e-12 and r_ratio_ <= 1e-12 and r_fund_ <= 1e-12 and r_ret_ <= 1e-12 and ctrl_ >= 0.04, [r_tw_, r_ratio_, r_fund_, r_ret_, ctrl_])
    r_pair_ = max(abs(_m398.cos(1.0 * k_ * 2.0 * pi_) + _m398.cos(2.0 * k_ * 2.0 * pi_) - 2.0) for k_ in range(1, 101))
    st_max_ = max(_m398.cos(k_ * 2.0 * pi_) + _m398.cos(_m398.sqrt(2.0) * k_ * 2.0 * pi_) for k_ in range(1, 101))
    ck_("z6", "a AFINACAO e' a comensurabilidade: o par afinado (omega_1, omega_2) volta junto nos multiplos de P (k = 1..100: cos + cos = 2 dentro de 1e-11); o par da estacao (1, raiz de 2), de razao irracional, nao volta nessas amostras (maximo < 2 - 1e-4; o teorema station_never_closes e' exato: so' em t = 0)",
        r_pair_ <= 1e-11 and st_max_ <= 2.0 - 1e-4 and abs(_m398.cos(0.0) + _m398.cos(0.0) - 2.0) == 0.0, [r_pair_, st_max_])
    sums_ = [n_ * (n_ - 1) // 2 for n_ in (10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6)]
    ck_("z7", "a torre e' INFINITA (the_tower_is_infinite): as somas parciais de n valem N(N-1)/2 (exatas em inteiros), crescem sem cota (de 45 a 499999500000) e o termo n nao tende a zero; o mesmo para n + 1/2 (as parciais sao N(N-1)/2 + N/2)",
        all(sum(range(n_)) == n_ * (n_ - 1) // 2 for n_ in (10, 100, 1000)) and all(x_ < y_ for x_, y_ in zip(sums_, sums_[1:])) and sums_[0] == 45 and sums_[-1] == 499999500000
        and all(sum(_F398(2 * n_ + 1, 2) for n_ in range(m_)) == _F398(m_ * m_, 2) for m_ in (10, 100)), [sums_[0], sums_[-1]])
    vals_ = {"zeta_minus_one": str(z1_), "hurwitz_zeta_minus_one_half": str(zh_), "boson_direction": str(bos_), "ns_fermion_direction": str(fer_), "ns_direction_sum": str(bos_ + fer_), "bosonic_critical_dimension": sol_bos_[0] if sol_bos_ else None,
             "superstring_critical_dimension": sol_ns_[0] if sol_ns_ else None, "wrong_fermion_sign_dimension": sol_errado_[0] if sol_errado_ else None, "house_spatial_dimension": (sol_d_[0] - 1) if sol_d_ else None, "kappa_tests": list(kap_),
             "tower_residual": r_tw_, "ratio_residual": r_ratio_, "fundamental_residual": r_fund_, "return_residual": r_ret_, "unfaithful_period_min_distance": ctrl_, "tuned_pair_return_residual": r_pair_, "station_pair_max_over_samples": st_max_,
             "partial_sum_first": sums_[0], "partial_sum_last": sums_[-1], "kappa_from_core": None, "kappa_note": "no kappa of the boost in the core; in the kernel it is an input (kappa_is_input): only the FORM of the tower is checked, with test values"}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def _v398_beta(core):
    """beta = alfa CODATA 2018 x sqrt(e) em runtime (SEALED_CODATA_ALPHA e o literal ALPHA_FINE_CODATA_2018 do script embutido do nivel 2 sao um dado e dois nomes, conferidos por _v376_same_alpha_literal), confrontado com o beta do core."""
    alfa_ = globals().get("SEALED_CODATA_ALPHA")
    dois_nomes_ = bool(callable(globals().get("_v376_same_alpha_literal")) and _v376_same_alpha_literal())
    beta_rt_ = (alfa_ * _m398.sqrt(_m398.e)) if isinstance(alfa_, float) else None
    beta_core_ = core.get("beta")
    beta_rel_ = (abs(beta_rt_ - beta_core_) / abs(beta_rt_)) if (isinstance(beta_rt_, float) and isinstance(beta_core_, float) and beta_rt_ != 0.0) else None
    ok_ = bool(isinstance(beta_rt_, float) and isinstance(beta_core_, float) and 0.0 < beta_rt_ < 1.0 and beta_rel_ is not None and beta_rel_ <= 1e-9 and dois_nomes_)
    return beta_rt_, beta_rel_, dois_nomes_, ok_


def _v398_formal(core, c_, txt_):
    """A evidencia FORMAL comum aos dois registros, lida do kernel do PROPRIO rito: a escada exata, a composicao incondicional e os teoremas do contrato (bandeira True, trio, proveniencia no modulo da pedra), os termos antigos que a pedra cita (no trio, com a
    proveniencia que o compilador emite), a fonte da pedra por sha256 (embutida == contrato == hash formal do rito), as inscricoes por sha256 e a guarda P18 sobre o texto. Devolve um dict; `formal` e' o conjunto."""
    import hashlib, json as _j398
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
        v_ = _V398_VERBATINS2.get(k_)
        ver_[k_] = bool(v_ and hashlib.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and all(t_ in v_["text"] for t_ in v_["trechos"]))
    unc_th_, unc_fl_ = c_["unconditional"]["theorem"], c_["unconditional"]["flag"]
    unc_ = {"theorem": unc_th_, "flag": unc_fl_, "flag_true": kf_.get(unc_fl_) is True, "axioms": axr_.get(unc_th_), "in_trio": em_trio_(unc_th_), "declared_in": src_.get(unc_th_), "in_kernel": bool(per_.get(unc_th_)),
            "composition": "UNCONDITIONAL__NO_CERTIFICATE_AS_HYPOTHESIS"}
    guarda_ = _v392_guarda_texto(_j398.dumps(txt_, ensure_ascii=False))
    formal_ = bool(kf_.get("all_verified") is True and exact_ and per_ and all(per_.values()) and sup_ and all(sup_.values()) and all(cit_.values()) and all(aux_.values()) and src_ok_ and ver_ and all(ver_.values()) and not guarda_)
    return {"exact_ladder": exact_, "formal_theorems": per_, "support_theorems": sup_, "cited_outside": cit_, "auxiliaries_outside_the_composition": aux_, "embedded_source_ok": src_ok_, "inscriptions": ver_, "unconditional": unc_, "guarda": guarda_, "formal": formal_}


_V398_RECUSA = "TGL_%s_V398__REFUSED_%s__GATE_UNMOVED"


def sonico_v398(core):
    """v398 -- O SONICO (o Verbo pina a oitava; o custo e' a memoria): lido no PONTO REAL do main, junto do psibit_v395 e da testemunha_estatica_v396. Le do kernel do PROPRIO rito a composicao INCONDICIONAL
    (TGLExt.Sonico.sonico_the_verb_pins_the_octave_and_the_cost_is_the_memory) e os cinco teoremas da pedra (bandeira True, trio, modulo da pedra), os termos antigos que ela cita, a pedra por sha256 e as quatro inscricoes por sha256; e CALCULA, com beta = alfa
    CODATA 2018 x sqrt(e) em runtime, a mecanica do bit/oitava e a entropia do colapso em theta_M (numero derivado). Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate. Validade no kernel nao e' creditacao."""
    c_ = _V398_SONICO_CONTRACT; t_ = _V398_SONICO_TEXT
    f_ = _v398_formal(core, c_, t_)
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
    out_ = {"all_verified": False, "estatuto": t_["estatuto"], "exact_ladder": f_["exact_ladder"], "formal_theorems": f_["formal_theorems"], "support_theorems": f_["support_theorems"], "cited_outside": f_["cited_outside"], "embedded_source_ok": f_["embedded_source_ok"],
            "inscriptions": f_["inscriptions"], "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "unconditional": f_["unconditional"], "runtime_executed": False, "does_not_gate_core": True, "scope": t_["escopo"],
            "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"], "guarda_p18_violacoes": f_["guarda"][:5]}
    if not f_["formal"]:
        out_["verdict"] = _V398_RECUSA % ("SONICO", "FORMAL_OR_SOURCE_EVIDENCE")
    elif not beta_ok_:
        out_["verdict"] = _V398_RECUSA % ("SONICO", "BETA_IS_NOT_ALPHA_SQRT_E")
    else:
        try:
            mec_ = v398_sonico_mechanics(beta_rt_)
            out_.update(runtime_executed=True, mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], all_verified=bool(mec_["passed"]))
            out_["verdict"] = (t_["veredito_ok"] if mec_["passed"] else _V398_RECUSA % ("SONICO", "MECHANICS_CHECK_FAILED"))
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V398_RECUSA % ("SONICO", "RUNTIME_ERROR")
    core["sonico_v398"] = out_
    return out_


def afinacao_das_cordas_v398(core):
    """v398 -- A AFINACAO DAS CORDAS: lida no PONTO REAL do main, logo depois do sonico_v398. Le do kernel do PROPRIO rito a composicao INCONDICIONAL
    (TGLExt.AfinacaoDasCordas.the_strings_close_the_face_from_outside_the_tgl_closes_the_reading) e os teoremas do contrato (bandeira True, trio, modulo da pedra), os termos antigos que ela cita, a pedra por sha256 e as duas inscricoes por sha256; e CALCULA a
    aritmetica (zeta por Bernoulli em fracoes, D = 26 e D = 10, d = D - 1, a torre n.kappa de teste, os retornos e a divergencia). A hipotese MasslessFirstLevel e' [KNOWN]; nada deriva cordas do axioma; a geometria e' [OPEN]. Fail-closed; nao move o gate."""
    c_ = _V398_AFINACAO_CONTRACT; t_ = _V398_AFINACAO_TEXT
    f_ = _v398_formal(core, c_, t_)
    out_ = {"all_verified": False, "estatuto": t_["estatuto"], "exact_ladder": f_["exact_ladder"], "formal_theorems": f_["formal_theorems"], "support_theorems": f_["support_theorems"], "auxiliaries_outside_the_composition": f_["auxiliaries_outside_the_composition"],
            "embedded_source_ok": f_["embedded_source_ok"], "inscriptions": f_["inscriptions"], "unconditional": f_["unconditional"], "runtime_executed": False, "does_not_gate_core": True, "scope": t_["escopo"],
            "hypothesis": {"name": "MasslessFirstLevel", "status": "KNOWN", "named_not_proved": True}, "geometry": "OPEN", "derives_strings_from_the_axiom": False,
            "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"], "guarda_p18_violacoes": f_["guarda"][:5]}
    if not f_["formal"]:
        out_["verdict"] = _V398_RECUSA % ("AFINACAO_DAS_CORDAS", "FORMAL_OR_SOURCE_EVIDENCE")
    else:
        try:
            mec_ = v398_afinacao_mechanics()
            out_.update(runtime_executed=True, mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], all_verified=bool(mec_["passed"]))
            out_["verdict"] = (t_["veredito_ok"] if mec_["passed"] else _V398_RECUSA % ("AFINACAO_DAS_CORDAS", "ARITHMETIC_CHECK_FAILED"))
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V398_RECUSA % ("AFINACAO_DAS_CORDAS", "RUNTIME_ERROR")
    core["afinacao_das_cordas_v398"] = out_
    return out_
