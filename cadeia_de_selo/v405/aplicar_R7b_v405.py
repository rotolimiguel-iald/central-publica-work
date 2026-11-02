# -*- coding: utf-8 -*-
"""aplicar_R7b_v405.py -- a errata R7 nos textos, registros, runtime, guarda e cadeia (ordem da gerencia c1, 01/11/2026, depois da segunda revisao de terceiro, que nao aprovou eaefcd095abbaee7: 1 ALTO, 4 MEDIO, 11 BAIXO).
Uso unico. Backup de BYTES de cada arquivo (.bak_<ts>_R7b); temporario -> conferir -> os.replace; cada ancora exatamente 1x. Nao toca as pedras."""
import os, re, time

HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")


def grava(nome, b, s):
    p = os.path.join(HERE, nome)
    open(p + ".bak_" + TS + "_R7b", "wb").write(b)
    t = p + ".tmp_R7b"
    open(t, "wb").write(s.encode("utf-8"))
    assert open(t, "rb").read() == s.encode("utf-8")
    os.replace(t, p)


def patch(nome, subs, troca_tudo=(), blocos=()):
    """subs: (ancora, novo), ancora exatamente 1x. troca_tudo: (ancora, novo, n), ancora exatamente n vezes. blocos: (inicio, fim, novo): troca de `inicio` (inclusive) ate' `fim` (exclusive), os dois exatamente 1x."""
    p = os.path.join(HERE, nome)
    b = open(p, "rb").read()
    s = b.decode("utf-8")
    for ini, fim, novo in blocos:
        assert s.count(ini) == 1, (nome, "inicio", s.count(ini), ini[:90])
        i = s.index(ini)
        j = s.index(fim, i)
        s = s[:i] + novo + s[j:]
    for a, c in subs:
        n = s.count(a)
        assert n == 1, (nome, n, a[:120])
        s = s.replace(a, c)
    for a, c, k in troca_tudo:
        n = s.count(a)
        assert n == k, (nome, n, k, a[:120])
        s = s.replace(a, c)
    grava(nome, b, s)
    print("ok", nome, len(subs) + len(troca_tudo) + len(blocos))


# ------------------------------------------------------------------------------------------- delta_v405.py
patch("delta_v405.py", [
    ("as demais notas ficam sustentadas, a escala e o tom ficam (modular, modular_sustenta, modular_mantem_a_escala, modular_nao_e_transposicao);",
     "as demais notas ficam sustentadas, elas e as razoes entre elas ficam (modular, modular_sustenta, modular_mantem_a_escala, modular_nao_e_transposicao), e o tom fica, na fala dele, sem termo no kernel;"),
    ("O GAP: o lock minimo tem gap 1, no angulo de Miguel le beta, na unidade posta Delta = beta.u, e as igualdades algebricas do fecho the_gap_closes).",
     "O GAP: o lock minimo tem gap espectral 1, em qualquer espaco de Hilbert, e na unidade posta vale u, o E0 da Lei do Diminuto; no angulo de Miguel o valor esperado do lock e' beta e, na unidade posta, Delta = beta.u, a energia retida, que NAO e' gap; o fecho the_gap_closes)."),
    ("gap_v405 (o gap lido do angulo de Miguel, ao lado)", "gap_v405 (o gap espectral do lock e o valor esperado dele no angulo de Miguel, ao lado)"),
    ("18:41, 18:56 e 19:02; recibos RECIBO_ERRATA_PEDRAS_01nov.json e _R2, _R3, _R4, _R5 e _R6)", "18:41, 18:56, 19:02 e 20:57; recibos RECIBO_ERRATA_PEDRAS_01nov.json e _R2, _R3, _R4, _R5, _R6 e _R7)"),
    ("# 163 = 21 + 15 + 15 + 26 + 39 + 14 + 13 + 20 (medido", "# 166 = 21 + 15 + 15 + 26 + 39 + 14 + 13 + 23 (medido"),
    ("GAP_N_CHECKS = 10 ", "GAP_N_CHECKS = 11 "),
    ('"TGLExt.PonteDaMassa.energia_retida_eq": _PDM, "TGLExt.LeiDoDiminuto.tonica": _LDD, "TGLExt.TonicaDoHamiltoniano.gammaB_is_the_canonical_law_at_the_systems_frequency"',
     '"TGLExt.PonteDaMassa.energia_retida_eq": _PDM, "TGLExt.LeiDoDiminuto.tonica": _LDD, "TGLExt.LeiDoDiminuto.tonica_eq": _LDD, "TGLExt.LeiDoDiminuto.leiDerivada_E0": _LDD, "TGLExt.TonicaDoHamiltoniano.gammaB_is_the_canonical_law_at_the_systems_frequency"'),
    ("o fator sen 45 graus tem duas leituras que coincidem por aritmetica), nao o numero nem o teste",
     "o fator sen 45 graus tem duas leituras que coincidem por aritmetica, e mais uma leitura do mesmo sen 45, tambem por aritmetica), nao o numero nem o teste"),
    ("(PontoZeroDoPsion; a coincidencia e' a aritmetica (1/2).sqrt2 = sen45); \"",
     "(PontoZeroDoPsion; a coincidencia e' a aritmetica (1/2).sqrt2 = sen45), e mais uma leitura do mesmo sen 45, por aritmetica: o psion como projecao transversal do modo autoconsistente (o_psion_e_a_projecao_do_modo); \""),
    ("as demais notas ficam sustentadas, a escala e o tom ficam: a escala e' o que fica parado, e a razao a tonica muda; E0 e' o valor da tonica modulada;",
     "as demais notas ficam sustentadas, elas e as razoes entre elas ficam: a escala e' o que fica parado, e a razao a tonica muda; o tom fica, na fala dele, sem termo no kernel; E0 e' o valor da tonica modulada;"),
    ("\"gap\": \"o sistema fisico que da' a medida da tonica por um gap com unidade e' o angulo de Miguel; ler tempoDoGap como o tau* do sistema e' leitura a ratificar pelo operador; kappa segue testemunha; a unidade segue posta [INPUT/ONTO]\"",
     "\"gap\": \"o sistema fisico que da' a medida da tonica por um gap com unidade e' o angulo de Miguel: leitura dele; o gap espectral do lock, na unidade posta, e' u, o E0 da Lei do Diminuto, e a tonica fica meio-tom acima dele; Delta = beta.u e' o valor esperado do lock no angulo de Miguel, a energia retida, e nao e' gap; ler tempoDoRetido como o tau* do sistema e' leitura a ratificar pelo operador; kappa segue testemunha; a unidade segue posta [INPUT/ONTO]\""),
    ("\"eletricidade\": \"a inscricao da luz que singulariza o sistema e' a eletricidade; a origem da medida e' o 1 absoluto, que representa 1 eV: como forma no kernel, zero_mode_weight_is_one e alpha_transport; isto nao deriva a unidade [ONTO]\"",
     "\"eletricidade\": \"a inscricao da luz que singulariza o sistema e' a eletricidade; a origem da medida e' o 1 absoluto, que representa 1 eV [ONTO]; os teoremas zero_mode_weight_is_one e alpha_transport existem [REAL]; le-los como a forma dessa fala e' leitura da gerencia [ONTO]: alphaKappa nao e' a alfa de estrutura fina, e kappa ali nao e' o relogio; isto nao deriva a unidade\""),
    ("{\"n\": 13, \"estatuto\": \"ONTO, a ratificar pelo operador\", \"leitura\": \"tempoDoGap lido como o tau* do sistema: e' tempo proprio, nao t_P, e nao mexe no ramo canonico\", \"definicao_lean\": \"TGLExt.PontoZeroDoPsion.tempoDoGap\",",
     "{\"n\": 13, \"estatuto\": \"ONTO, a ratificar pelo operador\", \"leitura\": \"tempoDoRetido lido como o tau* do sistema: e' tempo proprio, nao t_P, e nao mexe no ramo canonico\", \"definicao_lean\": \"TGLExt.PontoZeroDoPsion.tempoDoRetido\","),
    ("{\"n\": 14, \"estatuto\": \"ONTO\", \"leitura\": \"alfa lida como a inscricao eletrica que leva o gap a tonica: o enunciado de a_tonica_e_o_gap_sobre_alpha e' algebra; a leitura e' do operador\", \"definicao_lean\": \"TGLExt.PontoZeroDoPsion.a_tonica_e_o_gap_sobre_alpha\", \"modulo\": \"TGLExt/PontoZeroDoPsion.lean\", \"entra_como\": \"LEITURA, nao teorema\"}]",
     "{\"n\": 14, \"estatuto\": \"ONTO\", \"leitura\": \"alfa lida como a inscricao eletrica que leva o retido a tonica: o enunciado de a_tonica_e_o_retido_sobre_alpha e' algebra; a leitura e' do operador\", \"definicao_lean\": \"TGLExt.PontoZeroDoPsion.a_tonica_e_o_retido_sobre_alpha\", \"modulo\": \"TGLExt/PontoZeroDoPsion.lean\", \"entra_como\": \"LEITURA, nao teorema\"},\n"
     "                       {\"n\": 15, \"estatuto\": \"ONTO\", \"leitura\": \"o angulo de Miguel lido como o sistema que da' a medida da tonica por um gap com unidade: a fala e' do operador; o kernel prova o gap espectral do lock e o valor esperado no angulo de Miguel, nao que esse angulo seja esse sistema\", \"definicao_lean\": None, \"modulo\": None, \"entra_como\": \"LEITURA, nao teorema\"}]"),
])

# ------------------------------------------------------------------------------------------- runtime_v405.py
_F13 = r'''               ("F13_delta_nao_e_gap", _re.compile(r"\bgap(?:\s+espectral)?\s*(?:e'|é|eh|is|=|:|,|de|of|vale|equals)?\s*(?:a\s+|the\s+)?(?:[`$*\\]*(?:Δ|Delta)\b|energia\s+retida|retained\s+energy|(?:β|beta)\s*[·.*]\s*u\b|12[,.]03)|(?:Δ|\bDelta|energia\s+retida|retained\s+energy|(?:β|\bbeta)\s*[·.*]\s*u|12[,.]03\d*\s*meV)[`$*]*\s*,?\s*(?:e'|é|eh|is|=|:|como|as)\s*(?:o\s+|the\s+|um\s+|a\s+)?gap\b|\bgap\s+(?:lido|lida|read)\s+(?:do|no|from|at)\s+(?:the\s+)?(?:[âa]ngulo|angle)|\btempo\s+do\s+gap\b|\btime\s+of\s+the\s+gap\b|tempoDoGap|DELTA_IS_THE_GAP|THE_GAP_IS_DELTA|TIME_OF_THE_GAP|GAP_READ_FROM", _re.I)),
               ("F14_o_tom_nao_tem_termo", _re.compile(r"\ba\s+escala\s+e\s+o\s+tom\s+ficam\b|\bmantendo\s+a\s+escala\s+e\s+o\s+tom\b|\bthe\s+scale\s+and\s+the\s+key\s+stay\b", _re.I)),
'''
_F13B = r'''    for m_ in _re.finditer(r"\bgap\b[^.;\n]{0,60}12[,.]03|12[,.]03\d*\s*meV[^.;\n]{0,60}\bgap\b", str(txt_), _re.I):   # 12,03 meV e' o valor esperado do lock no angulo de Miguel, nao o gap (errata R7): a mencao so' passa dita como negacao
        volta_ = str(txt_)[max(0, m_.start() - 30):m_.end() + 30].lower()
        if not any(n_ in volta_ for n_ in ("não", "nao", "not ")):
            out_.append(("F13_delta_nao_e_gap", str(txt_)[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
'''
_MEC = r'''def v405_gap_mechanics(beta_, core_, c_):
    """v405 -- O GAP (a secao O GAP da pedra PontoZeroDoPsion; registro gap_v405, ao lado): o lock minimo 1 - P tem gap espectral 1, em qualquer espaco de Hilbert; na unidade posta o gap vale u, o E0 da Lei do Diminuto, com a tonica meio-tom acima; num estado a um angulo theta o valor esperado e' sen^2(theta); no angulo de Miguel, beta; na unidade posta esse valor esperado e' Delta = beta.u, a energia retida, que NAO e' gap; a tonica e' Delta/alfa; a massa e' a projecao transversal de Delta; o psion e' sqrt2.Delta; o tempo do retido, Gamma_B e Q; a medida negativa (E_fluxo nao e' E0); tau nao e' t_P; kappa so' como hipotese; K nao depende da inclinacao. Devolve {passed, checks, values, n_checks}."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m405.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "x0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    u_ = float(c_["u_posto_eV"]); hb_, ev_, G_, cl_ = float(c_["hbar_si"]), float(c_["eV_J"]), float(c_["G_si"]), float(c_["c_si"]); s4_ = _m405.sin(_m405.pi / 4.0)
    om3_ = (1.0, 0.0, 0.0); chi3_ = (0.0, 1.0, 0.0)                                          # um modelo de dimensao 3: os lemas valem em qualquer espaco de Hilbert
    ip_ = lambda a_, b_: sum(x_ * y_ for x_, y_ in zip(a_, b_))
    lockv_ = lambda v_: tuple(x_ - ip_(om3_, v_) * o_ for x_, o_ in zip(v_, om3_))            # lockDe: 1 - P, com P a projecao sobre a reta de Omega
    psi_ = lambda th_: tuple(_m405.cos(th_) * a_ + _m405.sin(th_) * b_ for a_, b_ in zip(om3_, chi3_))
    lock_ = lambda th_: ip_(psi_(th_), lockv_(psi_(th_)))                                    # o valor esperado do lock no estado a um angulo theta de Omega
    thetas_ = (0.0, 0.1, _m405.pi / 6.0, _m405.pi / 4.0, 1.2)
    ck_("x1", "★★★ o_lock_tem_gap_um e lock_no_angulo, num modelo de dimensao 3 (os lemas valem em qualquer espaco de Hilbert): o lock minimo 1 - P vale 0 em Omega e 1 no ortogonal (gap espectral 1), e num estado a um angulo theta de Omega tem valor esperado sen^2(theta) em cinco angulos",
        lockv_(om3_) == (0.0, 0.0, 0.0) and lockv_(chi3_) == chi3_ and all(abs(lock_(t_) - _m405.sin(t_) ** 2) <= 1e-15 for t_ in thetas_), [lock_(t_) for t_ in thetas_])
    th_m_ = _m405.asin(_m405.sqrt(beta_)); dl_ = beta_ * u_
    ck_("x2", "★★★ lock_no_angulo_de_miguel, o_retido_e_lido_do_angulo_de_miguel e o_retido_e_o_valor_esperado_do_lock: no angulo de Miguel o valor esperado do lock e' beta (|erro| <= 1e-14 relativo) e, na unidade posta, u.<lock> = sen^2(theta_M).u = beta.u = Delta, a energia retida; Delta carrega u, e nada aqui fixa u (U_E_NOT_DERIVED fica)",
        _v405_rel(lock_(th_m_), beta_) <= 1e-14 and _v405_rel(u_ * lock_(th_m_), dl_) <= 1e-14 and _v405_rel(_m405.sin(th_m_) ** 2 * u_, dl_) <= 1e-14, [th_m_, dl_])
    sq_e_ = _m405.exp(0.5); alfa_ = beta_ / sq_e_; m_core_ = (core_.get("neutrino_mass") or {}).get("m_nu_meV")
    ck_("x3", "★★ a_tonica_e_o_retido_sobre_alpha e a_massa_e_a_projecao_do_retido: a tonica e' Delta/alfa = sqrt e.u (|erro| <= 1e-15 relativo) e a massa e' Delta.sen45 = o m_nu do programa a 1e-12 relativo; ler alfa como a inscricao eletrica que leva o retido a tonica e' do operador [ONTO]",
        _v405_rel(dl_ / alfa_, sq_e_ * u_) <= 1e-15 and isinstance(m_core_, float) and _v405_rel(dl_ * s4_ * 1000.0, m_core_) <= float(c_["rel_tol"]), [dl_ / alfa_, dl_ * s4_ * 1000.0])
    om_ = _m405.sqrt(2.0 * beta_ * (beta_ * u_ ** 2)); tau_ = 1.0 / dl_
    ck_("x4", "★★★ o_psion_e_raiz_de_dois_retidos e a_frequencia_do_sistema_e_a_do_psion_iff: omega do psion = sqrt2.Delta (|erro| <= 1e-15 relativo); sqrt2/tau = omega do psion para tau = 1/Delta e, no controle negativo, nao para tau = 2/Delta nem tau = 1/(2.Delta): e' um se e so' se",
        _v405_rel(om_, _m405.sqrt(2.0) * dl_) <= 1e-15 and _v405_rel(_m405.sqrt(2.0) / tau_, om_) <= 1e-15 and _v405_rel(_m405.sqrt(2.0) / (2.0 * tau_), om_) > 0.1 and _v405_rel(_m405.sqrt(2.0) / (0.5 * tau_), om_) > 0.1, [om_, tau_])
    gam_ = beta_ / tau_; q_ = om_ / gam_
    qs_ = [(_m405.sqrt(2.0 * beta_ * (beta_ * w_ ** 2))) / (beta_ * (beta_ * w_)) for w_ in (0.5, 1.0, 7.0)]
    ck_("x5", "★ a_taxa_de_fronteira_no_psion e a_qualidade_nao_depende_da_unidade: (1/2).beta.tau.omega^2 = beta/tau = Gamma_B (|erro| <= 1e-15 relativo) e Q = omega/Gamma_B = sqrt2/beta, numero puro: igual para u em {0,5; 1; 7}",
        _v405_rel(0.5 * beta_ * tau_ * om_ ** 2, gam_) <= 1e-15 and _v405_rel(q_, _m405.sqrt(2.0) / beta_) <= 1e-15 and all(_v405_rel(x_, q_) <= 1e-14 for x_ in qs_), [gam_, q_])
    ck_("x6", "★ o_ponto_zero_autoconsistente_e_o_retido e o_psion_e_a_projecao_do_modo: (1/2).(2/tau) = Delta e omega do psion = (2/tau).sen45 (|erro| <= 1e-15 relativo): mais uma leitura do mesmo sen 45, por aritmetica; algebra da definicao de tau",
        _v405_rel(0.5 * (2.0 / tau_), dl_) <= 1e-15 and _v405_rel((2.0 / tau_) * s4_, om_) <= 1e-15, [0.5 * (2.0 / tau_)])
    ck_("x7", "★ o_relogio_do_retido: kappa entra como antecedente, testemunha (regra do operador de 24/08/2026, TheHorizonRate.lean): SE kappa da' uma volta em tau, entao kappa/2pi = Delta; nada aqui e' busca de valor; conferencia por construcao, a conta devolve o proprio antecedente",
        _v405_rel((2.0 * _m405.pi / tau_) / (2.0 * _m405.pi), dl_) <= 1e-15, "como antecedente")
    tau_s_ = hb_ / (dl_ * ev_); e_fluxo_j_ = cl_ ** 5 * tau_s_ / (4.0 * _m405.pi * G_); e_fluxo_ev_ = e_fluxo_j_ / ev_; t_p_ = _m405.sqrt(hb_ * G_ / cl_ ** 5)
    ck_("x8", "★★ a MEDIDA NEGATIVA: sob esta leitura, E_fluxo = c^5.tau/(4.pi.G) vale da ordem de 10^57 eV (56 < log10 < 58): NAO e' E0; a ponte E_fluxo = E0 do Kimi NAO vale aqui",
        56.0 < _m405.log10(e_fluxo_ev_) < 58.0 and e_fluxo_ev_ / u_ > 1.0e50, [e_fluxo_ev_])
    ck_("x9", "★★ tau = hbar/Delta e' tempo proprio, nao t_P: tau/t_P > 1e25; ler tempoDoRetido como o tau* do sistema e' leitura [ONTO] a ratificar pelo operador, e nao mexe no ramo canonico",
        tau_s_ / t_p_ > 1.0e25, [tau_s_, t_p_])
    incl_ = (0.01, 0.05, 0.2, 0.6); ks_ = [(4.0 * 9.8 / (0.1 * a_)) * (1.5 * 1.0 * 9.8 * 0.1 * a_) for a_ in incl_]
    ck_("x10", "★ o disco: o invariante K = Omega^2.E nao depende da inclinacao (Omega^2 = 4g/(a.ang), E = (3/2).M.g.a.ang, um disco de teste, em quatro inclinacoes, |erro| <= 1e-12 relativo), logo o angulo nao fixa K: K segue [OPEN]; conferencia por construcao: a inclinacao cancela na conta",
        all(_v405_rel(k_, 6.0 * 1.0 * 9.8 ** 2) <= 1e-12 for k_ in ks_), [ks_[0]])
    e0_rg_ = ((core_.get("lei_do_diminuto_v405") or {}).get("values") or {}).get("E0_eV"); tn_rg_ = ((core_.get("lei_do_diminuto_v405") or {}).get("values") or {}).get("tonica_eV")
    ck_("x11", "★★★ o_gap_com_unidade e o fecho the_gap_closes: o gap espectral na unidade posta e' u, o E0 da Lei do Diminuto (o E0 do registro lei_do_diminuto_v405 == u a 1e-12 relativo), e a tonica fica meio-tom acima dele (tonica.e^(-1/2) = u); Delta NAO e' gap: o gap e' 1/beta vezes Delta",
        isinstance(e0_rg_, float) and isinstance(tn_rg_, float) and _v405_rel(e0_rg_, u_) <= float(c_["rel_tol"]) and _v405_rel(tn_rg_ * _m405.exp(-0.5), u_) <= float(c_["rel_tol"]) and _v405_rel(u_ / dl_, 1.0 / beta_) <= 1e-15 and u_ / dl_ > 10.0, [u_, u_ / dl_])
    vals_ = {"beta": beta_, "u_posto_eV": u_, "gap_espectral_eV": u_, "gap_sobre_Delta": u_ / dl_, "theta_M": th_m_, "Delta_eV": dl_, "tau_por_eV": tau_, "tau_s": tau_s_, "Gamma_B_eV": gam_, "Q": q_, "omega_psion_eV": om_, "tonica_eV": dl_ / alfa_, "E_fluxo_eV": e_fluxo_ev_, "log10_E_fluxo_eV": _m405.log10(e_fluxo_ev_), "E_fluxo_sobre_E0": e_fluxo_ev_ / u_, "tau_sobre_t_planck": tau_s_ / t_p_, "m_nu_meV_core": m_core_}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


'''
patch("runtime_v405.py", [
    ('''               ("F5_token_de_veredito", _re.compile(''', _F13 + '''               ("F5_token_de_veredito", _re.compile('''),
    ('''    for m_ in _re.finditer(r"(?:κ|kappa)\\s*=\\s*F\\(", str(txt_), _re.I):''', _F13B + '''    for m_ in _re.finditer(r"(?:κ|kappa)\\s*=\\s*F\\(", str(txt_), _re.I):'''),
    ("o que a forma fixa e' a razao; a reescala e' a transposicao do acorde: o no-go fala do valor ABSOLUTO;", "o que a forma fixa e' a razao; a reescala corresponde a transposicao do acorde: o no-go fala do valor ABSOLUTO;"),
], blocos=[("def v405_gap_mechanics(beta_, core_, c_):", "def _v405_gap_registro(r_, core_, spec_):", _MEC)])

# ------------------------------------------------------------------------------------------- registros_v405.py
_GAP_SPEC = r'''def gap_spec(core0, fj):
    """O registro por especificacao gap_v405, AO LADO: le a secao O GAP da pedra PontoZeroDoPsion (a resposta do operador de 01/11/2026; errata R7: o gap espectral do lock e' 1, na unidade posta u; Delta = beta.u NAO e' gap, e' o valor esperado do lock no angulo de Miguel) e calcula em runtime Delta, tau, Gamma_B, Q e a medida negativa. Nao move o gate, nao fixa u, nao deriva tau* nem kappa. O nome do registro e o titulo O GAP ficam."""
    PZP = S["psion"]["rel"]
    nomes_ = ["o_lock_tem_gap_um", "o_gap_com_unidade", "lock_no_angulo", "lock_no_angulo_de_miguel", "o_retido_e_o_valor_esperado_do_lock", "HminMic_e_o_lock", "o_retido_e_lido_do_angulo_de_miguel", "a_tonica_e_o_retido_sobre_alpha", "a_massa_e_a_projecao_do_retido", "o_psion_e_raiz_de_dois_retidos", "a_frequencia_do_sistema_e_a_do_psion_iff", "a_taxa_de_fronteira_no_psion", "o_ponto_zero_autoconsistente_e_o_retido", "o_psion_e_a_projecao_do_modo", "a_qualidade_nao_depende_da_unidade", "o_relogio_do_retido", "the_gap_closes"]
    termos_ = ["TGLExt.PontoZeroDoPsion." + n_ for n_ in nomes_]
    extra_ = ["TGLExt.zero_mode_weight_is_one", "TGLExt.alpha_transport", "TGLExt.PontoZeroDoPsion.lockDe", "TGLExt.PontoZeroDoPsion.retidoNoAngulo", "TGLExt.PontoZeroDoPsion.tempoDoRetido"]
    return {
        "nome": DL.GAP_REGISTRO, "veredito_prefixo": "TGL_GAP_V405",
        "veredito_sufixo": "THE_MINIMAL_LOCK_HAS_SPECTRAL_GAP_ONE_IN_ANY_HILBERT_SPACE__IN_THE_POSTED_UNIT_THE_GAP_IS_U_THE_E0_OF_THE_DIMINISHED_LAW_WITH_THE_TONIC_A_HALF_TONE_ABOVE__THE_EXPECTED_VALUE_AT_THE_ANGLE_OF_MIGUEL_IS_THE_RETAINED_DELTA_NOT_A_GAP__HMINMIC_IS_AN_INSTANCE_CONDITIONAL_ON_A_FOCK_CERTIFICATE_THE_KERNEL_DOES_NOT_INHABIT__THAT_THE_ANGLE_IS_THAT_SYSTEM_IS_THE_OPERATORS_READING__DELTA_CARRIES_THE_POSTED_UNIT_AND_NOTHING_FIXES_IT__THE_TIME_OF_THE_RETAINED_ENERGY_IS_A_PROPER_TIME_NOT_THE_PLANCK_TIME_READING_IT_AS_THE_SYSTEMS_TAU_STAR_IS_AN_ONTO_READING_TO_BE_RATIFIED__KAPPA_STAYS_A_WITNESS__THE_FLUX_ENERGY_IS_NOT_E0__THE_ANGLE_DOES_NOT_FIX_K__THE_FIVE_NOTES_STAY_OPEN__U_E_NOT_DERIVED_STAYS__GATE_UNMOVED",
        "estatuto": "[REAL -- os lemas do lock, em qualquer espaco de Hilbert: gap espectral 1; na unidade posta, u; valor esperado sen^2(theta) no angulo theta; no angulo de Miguel, beta; o fecho the_gap_closes, lido do kernel do rito, no trio; o calculo em runtime; REAL, CONDICIONAL -- o HminMic do kernel e' instancia desses lemas (HminMic_e_o_lock), condicional a um FockCertificate, que o kernel nao habita; ONTO -- que o angulo de Miguel seja o sistema do gap com unidade, leitura do operador; ONTO, A RATIFICAR PELO OPERADOR -- ler tempoDoRetido como o tau* do sistema; INPUT -- a fala do operador, sha16 %s; OPEN -- K, as cinco notas, a unidade; kappa e' testemunha, regra do operador de 24/08/2026]" % S16(N_MODULA),
        "fontes": [CHAVE_DE_FONTE["psion"], CHAVE_RECIBO_ERRATA_R7], "verbatins": [CH_DE(N_MODULA)], "kernel_flags": [fj["bandeiras_do_contrato"]["psion"][t_] for t_ in termos_], "kernel_decls": termos_ + extra_,
        "constants": dict(CONSTANTES), "n_checks_runtime": DL.GAP_N_CHECKS,
        "checks": [CH("x_a", "o registro ponto_zero_do_psion_v405 selou neste rito", "core", ["ponto_zero_do_psion_v405", "all_verified"], "verdadeiro"),
                   CH("x_b", "o registro lei_do_diminuto_v405 selou neste rito", "core", ["lei_do_diminuto_v405", "all_verified"], "verdadeiro"),
                   CH("x_c", "o canal vivo do neutrino segue com o mesmo veredito: o gap vai AO LADO e nao move o canal", "core", ["neutrino_mass", "verdict"], "igual", core0["neutrino_mass"]["verdict"]),
                   CH("x_d", "o fecho the_gap_closes e' emitido pelo compilador no modulo da pedra (TGL_DECL_SOURCE)", "kf", ["declaration_sources_v394", "TGLExt.PontoZeroDoPsion.the_gap_closes"], "igual", PZP),
                   CH("x_e", "o relogio o_relogio_do_retido e' emitido no modulo da pedra: kappa so' aparece ali, como hipotese", "kf", ["declaration_sources_v394", "TGLExt.PontoZeroDoPsion.o_relogio_do_retido"], "igual", PZP),
                   CH("x_f", "o teorema citado zero_mode_weight_is_one segue no modulo dele", "kf", ["declaration_sources_v394", "TGLExt.zero_mode_weight_is_one"], "igual", "TGLExt/LocalBreuerGap.lean"),
                   CH("x_g", "o teorema citado alpha_transport segue no modulo dele", "kf", ["declaration_sources_v394", "TGLExt.alpha_transport"], "igual", "TGLExt/ContinuousModularZero.lean"),
                   CH("x_h", "o elo entre o lock e a energia retida, o_retido_e_o_valor_esperado_do_lock, e' emitido no modulo da pedra", "kf", ["declaration_sources_v394", "TGLExt.PontoZeroDoPsion.o_retido_e_o_valor_esperado_do_lock"], "igual", PZP),
                   CH("x_i", "o kernel segue sem habitante do FockCertificate: a instancia HminMic_e_o_lock e' condicional", "core", ["psibit_v395", "conditional_psion_face", "inhabitant_exhibited"], "falso")],
        "erratas": [],
        "limites": ["[REAL] U_E_NOT_DERIVED fica: o gap na unidade posta e' u, e Delta = beta.u carrega a mesma unidade; nada aqui fixa u; o registro nao muda o numero da massa nem o veredito do canal; validade no kernel nao e' creditacao; o gate nao se move",
                    "[REAL] Delta NAO e' gap: e' o valor esperado do lock no angulo de Miguel, a energia retida, 1/beta vezes menor que o gap; o estado inscrito nao e' autoestado do lock",
                    "[REAL, condicional] os lemas do lock valem em qualquer espaco de Hilbert; o HminMic do kernel e' instancia deles (HminMic_e_o_lock), condicional a um FockCertificate, que o kernel nao habita (psibit_v395.conditional_psion_face.inhabitant_exhibited = false)",
                    "[ONTO] a fala do operador diz «gap com unidade»: que o angulo de Miguel seja esse sistema e' leitura dele, nao teorema",
                    "[ONTO, a ratificar pelo operador] ler tempoDoRetido como o tau* do sistema: e' tempo proprio, nao t_P, e nao mexe no ramo canonico; tau* nao foi obtido aqui; os enunciados sao algebra dada essa leitura",
                    "[REAL + regra do operador de 24/08/2026, TheHorizonRate.lean] kappa e' testemunha: kappa = F(alfa, beta, theta_M) e' proibido como objetivo de busca; kappa so' aparece como hipotese em o_relogio_do_retido",
                    "[REAL, medida negativa] sob esta leitura, E_fluxo = c^5.tau/(4.pi.G) nao e' E0 (ordem de 10^57 eV): a ponte E_fluxo = E0 do Kimi NAO vale aqui",
                    "[OPEN] o disco: o invariante K nao depende da inclinacao, logo o angulo nao fixa K; a pentada: quais sao as cinco notas segue aberto; so' se sabe, por fala do operador, que o angulo de Miguel pertence a ela",
                    "[REAL] zero_mode_weight_is_one (o peso L2 de (1/2).sech(kappa/2) em toda a reta e' 1, faces 1/2) e alpha_transport (alphaKappa' = -(q/2).alphaKappa, gradiente negativo em kappa > 0) existem no kernel; [ONTO, da gerencia] le-los como a forma da fala do operador sobre a eletricidade e a origem da medida; homonimo: alphaKappa = sech(kappa/2) nao e' a alfa de estrutura fina, e kappa ali e' a profundidade modular, nao o relogio; a palavra cauda nao esta no teorema; isso nao deriva a unidade"],
        "diz": ["em qualquer espaco de Hilbert, o lock minimo 1 - P sobre um vetor Omega tem gap espectral 1: vale 0 em Omega e 1 em todo vetor ortogonal; na unidade posta o gap vale u, o E0 da Lei do Diminuto, e a tonica fica meio-tom acima dele",
                "num estado a um angulo theta de Omega, o lock tem valor esperado sen^2(theta); no angulo de Miguel, beta; na unidade posta esse valor esperado e' Delta = beta.u, a energia retida: Delta NAO e' gap, e' 1/beta vezes menor",
                "a tonica e' Delta/alfa; a massa e' a projecao transversal de Delta; o psion e' sqrt2.Delta; sqrt2/tau = omega do psion sse tau = 1/Delta",
                "o HminMic do kernel e' instancia do lock (HminMic_e_o_lock), condicional a um FockCertificate, que o kernel nao habita",
                "o calculo, com beta = alfa CODATA 2018 x sqrt(e) em runtime e u = 1 eV posto: Delta, tau, Gamma_B e Q = sqrt2/beta; a medida negativa: E_fluxo nao e' E0", "a fala do operador sobre o angulo de Miguel esta embutida por sha256 e vale como INPUT; que esse angulo seja o sistema do gap com unidade e' leitura dele [ONTO]"],
        "nao_diz": ["que a unidade u tenha sido fixada", "que Delta seja gap (e' o valor esperado do lock no angulo de Miguel)", "que o kernel habite o FockCertificate", "que o angulo de Miguel seja, por teorema, o sistema do gap com unidade (e' leitura do operador)", "que tau* tenha sido obtido (ler tempoDoRetido como tau* e' leitura a ratificar)", "que tau seja t_P ou que o ramo canonico tenha mudado", "que kappa seja funcao de alfa, beta ou theta_M", "que E_fluxo seja E0", "que o angulo de Miguel fixe K", "quais sao as cinco notas", "que a eletricidade tenha termo no kernel", "que alphaKappa seja a alfa de estrutura fina"],
        "leituras_do_operador": [_leitura(DL.FRASE_GAP, N_MODULA), _leitura(DL.FRASE_ELETRICIDADE, N_MODULA), _leitura(DL.FRASE_ORIGEM, N_MODULA)],
        "extras": {"assinatura": ASSINA, "leitura_tau_star": {"status": "ONTO, a ratificar pelo operador", "content": "tempoDoRetido lido como o tau* do sistema: tempo proprio, nao t_P; nao mexe no ramo canonico", "is_a_kernel_term": False},
                   "o_gap_e_o_retido": {"gap_espectral": "1 no lock; u na unidade posta (o_lock_tem_gap_um, o_gap_com_unidade): o E0 da Lei do Diminuto, com a tonica meio-tom acima", "retido": "Delta = beta.u (retidoNoAngulo): o valor esperado do lock no angulo de Miguel (o_retido_e_o_valor_esperado_do_lock), 1/beta vezes menor; NAO e' gap"},
                   "fock": {"status": "REAL, condicional", "content": "os lemas do lock valem em qualquer espaco de Hilbert; HminMic e' instancia, condicional a um FockCertificate que o kernel nao habita", "termo": "TGLExt.PontoZeroDoPsion.HminMic_e_o_lock"},
                   "kappa": {"status": "testemunha (regra do operador de 24/08/2026, TheHorizonRate.lean)", "onde_aparece": "so' como hipotese em o_relogio_do_retido"}, "unidade": "U_E_NOT_DERIVED fica: Delta carrega u e nada fixa u", "ponte_do_kimi": "E_fluxo = E0 NAO vale aqui", "disco": "K nao depende da inclinacao: o angulo nao fixa K [OPEN]",
                   "pentada": "quais sao as cinco notas segue [OPEN]; so' se sabe, por fala do operador, que o angulo de Miguel pertence a ela", "inscricao_e_medida": {"status": "ONTO, da gerencia: ler os dois teoremas como a forma da fala do operador", "content": DL.LEITURA_V405["eletricidade"], "teoremas_que_existem": ["TGLExt.zero_mode_weight_is_one", "TGLExt.alpha_transport"], "homonimos": "alphaKappa = sech(kappa/2) nao e' a alfa de estrutura fina; kappa ali e' a profundidade modular, nao o relogio; o gradiente e' negativo em kappa > 0; a palavra cauda nao esta no teorema", "deriva_a_unidade": False}, "fala_sha16": S16(N_MODULA)},
    }


'''
patch("registros_v405.py", [
    ('''RECIBO_ERRATA_R6_ARQ = os.path.join(DL.ESTUDO_E0, "RECIBO_ERRATA_PEDRAS_R6_01nov.json")
''', '''RECIBO_ERRATA_R6_ARQ = os.path.join(DL.ESTUDO_E0, "RECIBO_ERRATA_PEDRAS_R6_01nov.json")
CHAVE_RECIBO_ERRATA_R7 = "recibo_errata_r7_das_pedras_01nov"
RECIBO_ERRATA_R7_ARQ = os.path.join(DL.ESTUDO_E0, "RECIBO_ERRATA_PEDRAS_R7_01nov.json")
'''),
    ('''          {"chave": CHAVE_RECIBO_ERRATA_R6, "arquivo": os.path.join(INS, os.path.basename(RECIBO_ERRATA_R6_ARQ)), "papel": "o recibo da ERRATA R6 DAS PEDRAS (gerencia c1, 01/11/2026, uma docstring da Tonica): os oito sha256 vigentes, um mudou; nenhum codigo mudou''',
     '''          {"chave": CHAVE_RECIBO_ERRATA_R7, "arquivo": os.path.join(INS, os.path.basename(RECIBO_ERRATA_R7_ARQ)), "papel": "o recibo da ERRATA R7 DAS PEDRAS (gerencia c1, 01/11/2026, a segunda revisao de terceiro): os oito sha256 vigentes, tres mudaram; codigo novo na PontoZeroDoPsion; o resto e' docstring [DECLARADO na origem; o sha256 de cada pedra e os termos sao conferidos pelo gerador e pelo kernel do rito]"},
          {"chave": CHAVE_RECIBO_ERRATA_R6, "arquivo": os.path.join(INS, os.path.basename(RECIBO_ERRATA_R6_ARQ)), "papel": "o recibo da ERRATA R6 DAS PEDRAS (gerencia c1, 01/11/2026, uma docstring da Tonica): oito sha256, um mudou; nenhum codigo mudou'''),
    ('''    cks2.append(CH("n%d" % m, "o recibo da errata R6 das pedras (fonte pinada, a vigente) cobre as oito pedras", "fonte:" + CHAVE_RECIBO_ERRATA_R6, ["pedras"], "tamanho_igual", 8)); m += 1
''', '''    cks2.append(CH("n%d" % m, "o recibo da errata R7 das pedras (fonte pinada, a vigente) cobre as oito pedras", "fonte:" + CHAVE_RECIBO_ERRATA_R7, ["pedras"], "tamanho_igual", 8)); m += 1
    cks2.append(CH("n%d" % m, "o recibo da errata R6 das pedras (fonte pinada) cobre as oito pedras", "fonte:" + CHAVE_RECIBO_ERRATA_R6, ["pedras"], "tamanho_igual", 8)); m += 1
'''),
    ('''CHAVE_RECIBO_ERRATA_R5, CHAVE_RECIBO_ERRATA_R6, CHAVE_RECIBO_IDENTIDADE, CHAVE_RECIBO_OBSERVADOR], "verbatins": [CH_DE(N_NOMES),''',
     '''CHAVE_RECIBO_ERRATA_R5, CHAVE_RECIBO_ERRATA_R6, CHAVE_RECIBO_ERRATA_R7, CHAVE_RECIBO_IDENTIDADE, CHAVE_RECIBO_OBSERVADOR], "verbatins": [CH_DE(N_NOMES),'''),
    # achado 4: o tom
    ("as demais notas ficam sustentadas, a escala fica (as razoes entre as sustentadas nao mudam) e nenhum fator leva", "as demais notas ficam sustentadas, elas e as razoes entre elas ficam (a escala e' o que fica parado) e nenhum fator leva"),
    ("[ONTO] alfa como a magnitude (cauda) da inscricao no bulk e «no harmônico o diminuto é a espera»; [OPEN] quais sao as cinco notas\" %", "[ONTO] alfa como a magnitude (cauda) da inscricao no bulk e «no harmônico o diminuto é a espera»; [INPUT] o tom fica, na fala dele: o kernel nao tem termo para o tom; [OPEN] quais sao as cinco notas\" %"),
    ("as outras quatro ficam sustentadas (modular_sustenta); a escala e o tom ficam: a escala e' o que fica parado, as notas sustentadas e as razoes entre elas (modular_mantem_a_escala); a razao a tonica muda, e e' a tonica que se move;",
     "as outras quatro ficam sustentadas (modular_sustenta); as notas sustentadas e as razoes entre elas ficam: a escala e' o que fica parado (modular_mantem_a_escala); [INPUT] o tom fica, na fala dele: o kernel nao tem termo para o tom; a razao a tonica muda, e e' a tonica que se move;"),
    ('"que a razao a tonica seja a escala (a razao a tonica muda; a escala fica)", ', '"que a razao a tonica seja a escala (a razao a tonica muda; a escala fica)", "que o kernel tenha termo para o tom (o tom fica, na fala dele)", '),
    # BAIXO: a reescala corresponde a transposicao
    ("a reescala e' a transposicao do acorde, a liberdade do no-go, que fala do valor ABSOLUTO;", "a reescala corresponde a transposicao do acorde, a liberdade do no-go, que fala do valor ABSOLUTO;"),
    # a pedra do psion
    ("os termos do kernel (os 20 teoremas do contrato, no trio, no modulo da pedra; os termos de suporte: neutrinoMassForm,", "os termos do kernel (os 23 teoremas do contrato, no trio, no modulo da pedra; os termos de suporte: neutrinoMassForm,"),
    ("sin_sq_thetaMiguel, energia_retida_eq, tonica, gammaB_is_the_canonical_law_at_the_systems_frequency)", "sin_sq_thetaMiguel, energia_retida_eq, tonica, tonica_eq, leiDerivada_E0, gammaB_is_the_canonical_law_at_the_systems_frequency)"),
    ("(7) a secao O GAP, lida e calculada pelo registro gap_v405, ao lado: o lock minimo tem gap 1 e, no angulo de Miguel, le beta. \"", "(7) a secao O GAP, lida e calculada pelo registro gap_v405, ao lado: o lock minimo tem gap espectral 1 e, no angulo de Miguel, valor esperado beta. \""),
    ("os 20 teoremas do contrato e os termos de suporte sao lidos deste kernel", "os 23 teoremas do contrato e os termos de suporte sao lidos deste kernel"),
    ("(a projecao transversal da Meia-Nat e o ponto zero do psion sob R = beta.u^2): a errata E10 esta ao lado;", "(a projecao transversal da Meia-Nat e o ponto zero do psion sob R = beta.u^2), e mais uma leitura do mesmo sen 45, por aritmetica (o_psion_e_a_projecao_do_modo): a errata E10 esta ao lado;"),
    ('"duas_leituras_do_sen45": {"primeira":', '"duas_leituras_do_sen45": {"mais_uma_por_aritmetica": "o psion como projecao transversal do modo autoconsistente (o_psion_e_a_projecao_do_modo)", "primeira":'),
    ('''if l_["n"] in (4, 6, 7, 13, 14)]''', '''if l_["n"] in (4, 6, 7, 13, 14, 15)]'''),
    # achado 5: stealth
    ("KNOWN a ordem linear stealth;", "DERIVED a ordem linear stealth, condicional a Face C na ordem linear ((P1)-(P4) + T1; a derivacao e' da teoria: prove_ga_mass_audit, v98);"),
    ('"[KNOWN] nao discrimina da RG: na ordem linear M_TGL = M_RG (stealth)",', '"[DERIVED, condicional a Face C na ordem linear: (P1)-(P4) + T1; a derivacao e\' da teoria, prove_ga_mass_audit, v98] nao discrimina da RG: na ordem linear M_TGL = M_RG (stealth)",'),
], blocos=[("def gap_spec(core0, fj):", "def especs(", _GAP_SPEC)])

# ------------------------------------------------------------------------------------------- artigo PT
_GAP_PT = r'''    s.append(r"\textbf{O gap, ao lado.} \textsf{[INPUT]} O operador, em 01/11/2026: «o sistema físico que fornece a medidade da tônica por ujm gap com unidade e pertence à mesma pêntada é o ângulo de MIguel». \textsf{[ONTO]} Que o ângulo de Miguel seja esse sistema é leitura dele. \textsf{[REAL]} Em qualquer espaço de Hilbert, o lock mínimo $1-P$ sobre um vetor $\Omega$ (\texttt{lockDe}) tem gap espectral 1: vale 0 em $\Omega$ e 1 em todo vetor ortogonal (\texttt{o\_lock\_tem\_gap\_um}). Na unidade posta o gap vale $u$ (\texttt{o\_gap\_com\_unidade}), o $E_0$ da Lei do Diminuto, e a tônica fica meio-tom acima dele. Num estado a um ângulo $\theta$ de $\Omega$ o lock tem valor esperado $\sin^2\theta$ (\texttt{lock\_no\_angulo}); no ângulo de Miguel, $\beta$ (\texttt{lock\_no\_angulo\_de\_miguel}); na unidade posta esse valor esperado é $\Delta=\beta u$, a energia retida (\texttt{retidoNoAngulo}, \texttt{o\_retido\_e\_o\_valor\_esperado\_do\_lock}). $\Delta$ não é gap: é $1/\beta$ vezes menor. \textsf{[REAL, condicional]} O \texttt{HminMic} do kernel é instância desses lemas (\texttt{HminMic\_e\_o\_lock}), condicional a um \texttt{FockCertificate}, que o kernel não habita. \textsf{[REAL]} A tônica é $\Delta/\alpha$; a massa é a projeção transversal de $\Delta$; $\omega_\psi=\sqrt2\,\Delta$; e $\sqrt2/\tau=\omega_\psi$ se e só se $\tau=1/\Delta$ (\texttt{the\_gap\_closes}, registro \texttt{gap\_v405}). \textsf{[REAL]} Neste rito: $\Delta=" + _f405(_gv405.get("Delta_eV"), 9) + r"$ eV (o gap é " + _f405(_gv405.get("gap_sobre_Delta"), 1) + r" vezes $\Delta$), $\tau=" + _g405(_gv405.get("tau_s")) + r"$ s, $\Gamma_B=" + _g405(_gv405.get("Gamma_B_eV")) + r"$ eV, $Q=\sqrt2/\beta=" + _f405(_gv405.get("Q"), 3) + r"$. \textsf{[ONTO, a ratificar pelo operador]} Ler \texttt{tempoDoRetido} como o $\tau_\star$ do sistema: é tempo próprio, não $t_P$, e não mexe no ramo canônico. "
             r"\textsf{[REAL]} $\kappa$ segue testemunha: $\kappa=F(\alpha,\beta,\theta_M)$ é proibido como objetivo de busca, e $\kappa$ só aparece como hipótese em \texttt{o\_relogio\_do\_retido}. \texttt{U\_E\_NOT\_DERIVED} fica: $\Delta$ carrega $u$, e nada fixa $u$. Medida negativa: sob esta leitura, $E_{\mathrm{fluxo}}=c^5\tau/(4\pi G)$ vale $" + _g405(_gv405.get("E_fluxo_eV")) + r"$ eV: não é $E_0$, e a ponte $E_{\mathrm{fluxo}}=E_0$ do Kimi não vale aqui. \textsf{[OPEN]} Quais são as cinco notas; só se sabe, por fala dele, que o ângulo de Miguel pertence a elas.")
    s.append(r"\textbf{A inscrição e a medida.} \textsf{[ONTO]} O operador, em 01/11/2026: «a inscrição da luz que singulariza o sistema é a eletricidade», e «a origem da medida é a matemática, ou seja, o 1 absoluto, que representa 1 Eletrovolt». \textsf{[REAL]} Dois teoremas existem no kernel: \texttt{zero\_mode\_weight\_is\_one} (o peso $L^2$ de $\tfrac12\,\mathrm{sech}(\kappa/2)$ em toda a reta é 1, faces $\tfrac12$) e \texttt{alpha\_transport} ($\alpha'=-(q/2)\,\alpha$, com $\alpha=\mathrm{sech}(\kappa/2)$ e $q=\tanh(\kappa/2)$: o gradiente é negativo em $\kappa>0$). \textsf{[ONTO, da gerência]} Lê-los como a forma da fala do operador é leitura da gerência. Homônimo, dito: ali \texttt{alphaKappa} não é a $\alpha$ de estrutura fina, e $\kappa$ é a profundidade modular, não o relógio; a palavra cauda não está no teorema. Isso não deriva a unidade.")
'''
patch("artigo_pt_v405.pysnip", [
    (r"(13) \texttt{tempoDoGap} lido como o $\tau_\star$ do sistema, a ratificar pelo operador; (14) $\alpha$ lida como a inscrição elétrica que leva o gap à tônica.",
     r"(13) \texttt{tempoDoRetido} lido como o $\tau_\star$ do sistema, a ratificar pelo operador; (14) $\alpha$ lida como a inscrição elétrica que leva o retido à tônica; (15) o ângulo de Miguel como o sistema que dá a medida da tônica por um gap com unidade."),
    (r"(\texttt{modular\_sustenta}), a escala e o tom ficam (\texttt{modular\_mantem\_a\_escala}: a escala é o que fica parado, as notas sustentadas e as razões entre elas; a razão à tônica muda, e é a tônica que se move), e nenhum fator leva o acorde ao acorde modulado (\texttt{modular\_nao\_e\_transposicao}): o meio-tom pinado quebra a simetria do acorde, porque separa a tônica das notas sustentadas, mas não quebra a liberdade global. $E_0$ é o valor",
     r"(\texttt{modular\_sustenta}), elas e as razões entre elas ficam (\texttt{modular\_mantem\_a\_escala}: a escala é o que fica parado; a razão à tônica muda, e é a tônica que se move), e nenhum fator leva o acorde ao acorde modulado (\texttt{modular\_nao\_e\_transposicao}): o meio-tom pinado quebra a simetria do acorde, porque separa a tônica das notas sustentadas, mas não quebra a liberdade global. \textsf{[INPUT]} O tom fica, na fala dele: o kernel não tem termo para o tom. \textsf{[REAL]} $E_0$ é o valor"),
    ("a reescala é a transposição do acorde, a liberdade do no-go.", "a reescala corresponde à transposição do acorde, a liberdade do no-go."),
    (r"(a derivada da projeção transversal e o ponto zero do psíon), e $E_0=u=1$ eV é", r"(a derivada da projeção transversal e o ponto zero do psíon), e mais uma leitura do mesmo $\sin45^\circ$, por aritmética (\texttt{o\_psion\_e\_a\_projecao\_do\_modo}); e $E_0=u=1$ eV é"),
], blocos=[('    s.append(r"\\textbf{O gap, ao lado.}', '    s.append(r"\\textbf{O Disco de Euler.}', _GAP_PT)])

# ------------------------------------------------------------------------------------------- artigo EN
_GAP_EN = r'''    s.append(r"\textbf{The gap, alongside.} \textsf{[INPUT]} The operator, on 01/11/2026 (management translation, not a quotation): the physical system that gives the measure of the tonic by a gap with a unit, and that belongs to the same pentad, is the angle of Miguel. \textsf{[ONTO]} That the angle of Miguel is that system is his reading. \textsf{[REAL]} In any Hilbert space, the minimal lock $1-P$ over a vector $\Omega$ (\texttt{lockDe}) has spectral gap 1: it is 0 on $\Omega$ and 1 on every orthogonal vector (\texttt{o\_lock\_tem\_gap\_um}). In the posted unit the gap is $u$ (\texttt{o\_gap\_com\_unidade}), the $E_0$ of the law of the diminished, and the tonic stands a half tone above it. In a state at an angle $\theta$ from $\Omega$ the lock has expected value $\sin^2\theta$ (\texttt{lock\_no\_angulo}); at the angle of Miguel, $\beta$ (\texttt{lock\_no\_angulo\_de\_miguel}); in the posted unit that expected value is $\Delta=\beta u$, the retained energy (\texttt{retidoNoAngulo}, \texttt{o\_retido\_e\_o\_valor\_esperado\_do\_lock}). $\Delta$ is not a gap: it is $1/\beta$ times smaller. \textsf{[REAL, conditional]} The kernel's \texttt{HminMic} is an instance of these lemmas (\texttt{HminMic\_e\_o\_lock}), conditional on a \texttt{FockCertificate}, which the kernel does not inhabit. \textsf{[REAL]} The tonic is $\Delta/\alpha$; the mass is the transverse projection of $\Delta$; $\omega_\psi=\sqrt2\,\Delta$; and $\sqrt2/\tau=\omega_\psi$ if and only if $\tau=1/\Delta$ (\texttt{the\_gap\_closes}, record \texttt{gap\_v405}). \textsf{[REAL]} In this rite: $\Delta=" + _f405(_gv405.get("Delta_eV"), 9) + r"$ eV (the gap is " + _f405(_gv405.get("gap_sobre_Delta"), 1) + r" times $\Delta$), $\tau=" + _g405(_gv405.get("tau_s")) + r"$ s, $\Gamma_B=" + _g405(_gv405.get("Gamma_B_eV")) + r"$ eV, $Q=\sqrt2/\beta=" + _f405(_gv405.get("Q"), 3) + r"$. \textsf{[ONTO, to be ratified by the operator]} Reading \texttt{tempoDoRetido} as the system's $\tau_\star$: it is a proper time, not $t_P$, and it does not touch the canonical branch. "
             r"\textsf{[REAL]} $\kappa$ stays a witness: $\kappa=F(\alpha,\beta,\theta_M)$ is forbidden as a search target, and $\kappa$ only appears as a hypothesis in \texttt{o\_relogio\_do\_retido}. \texttt{U\_E\_NOT\_DERIVED} stays: $\Delta$ carries $u$, and nothing fixes $u$. Negative measurement: under this reading, $E_{\mathrm{flux}}=c^5\tau/(4\pi G)$ is $" + _g405(_gv405.get("E_fluxo_eV")) + r"$ eV: it is not $E_0$, and Kimi's bridge $E_{\mathrm{flux}}=E_0$ does not hold here. \textsf{[OPEN]} Which the five notes are; all that is known, from his saying, is that the angle of Miguel belongs to them.")
    s.append(r"\textbf{The inscription and the measure.} \textsf{[ONTO]} The operator, on 01/11/2026 (management translation, not a quotation): the inscription of the light that singularizes the system is electricity, and the origin of measure is the absolute 1, which represents 1 electronvolt. \textsf{[REAL]} Two theorems exist in the kernel: \texttt{zero\_mode\_weight\_is\_one} (the $L^2$ weight of $\tfrac12\,\mathrm{sech}(\kappa/2)$ on the whole line is 1, faces $\tfrac12$) and \texttt{alpha\_transport} ($\alpha'=-(q/2)\,\alpha$, with $\alpha=\mathrm{sech}(\kappa/2)$ and $q=\tanh(\kappa/2)$: the gradient is negative for $\kappa>0$). \textsf{[ONTO, the management's]} Reading them as the form of the operator's saying is the management's reading. Homonym, said: there \texttt{alphaKappa} is not the fine-structure $\alpha$, and $\kappa$ is the modular depth, not the clock; the word tail is not in the theorem. This does not derive the unit.")
'''
patch("artigo_en_v405.pysnip", [
    (r"(13) \texttt{tempoDoGap} read as the system's $\tau_\star$, to be ratified by the operator; (14) $\alpha$ read as the electric inscription that takes the gap to the tonic.",
     r"(13) \texttt{tempoDoRetido} read as the system's $\tau_\star$, to be ratified by the operator; (14) $\alpha$ read as the electric inscription that takes the retained energy to the tonic; (15) the angle of Miguel as the system that gives the measure of the tonic by a gap with a unit."),
    (r"(\texttt{modular\_sustenta}), the scale and the key stay (\texttt{modular\_mantem\_a\_escala}: the scale is what stays, the sustained notes and the ratios among them; the ratio to the tonic changes, and it is the tonic that moves), and no factor takes the chord to the modulated chord (\texttt{modular\_nao\_e\_transposicao}): the pinned half tone breaks the symmetry of the chord, because it separates the tonic from the sustained notes, but it does not break the global freedom. $E_0$ is the value",
     r"(\texttt{modular\_sustenta}), they and the ratios among them stay (\texttt{modular\_mantem\_a\_escala}: the scale is what stays; the ratio to the tonic changes, and it is the tonic that moves), and no factor takes the chord to the modulated chord (\texttt{modular\_nao\_e\_transposicao}): the pinned half tone breaks the symmetry of the chord, because it separates the tonic from the sustained notes, but it does not break the global freedom. \textsf{[INPUT]} The key stays, in his saying: the kernel has no term for the key. \textsf{[REAL]} $E_0$ is the value"),
    ("the rescaling is the transposition of the chord, the freedom of the no-go.", "the rescaling corresponds to the transposition of the chord, the freedom of the no-go."),
    (r"(the derivative of the transverse projection and the zero point of the psion), and $E_0=u=1$ eV is", r"(the derivative of the transverse projection and the zero point of the psion), and one more reading of the same $\sin45^\circ$, by arithmetic (\texttt{o\_psion\_e\_a\_projecao\_do\_modo}); and $E_0=u=1$ eV is"),
], blocos=[('    s.append(r"\\textbf{The gap, alongside.}', '    s.append(r"\\textbf{Euler\'s Disk.}', _GAP_EN)])

# ------------------------------------------------------------------------------------------- textos do pos-rito
_GAP_T = '''def _gap(V):
    d = _d(V); v = V["gap"]["values"]; ss = d["ss"]
    return _f("**O gap, ao lado** [REAL · ONTO · OPEN] (registro `gap_v405`, {n} checagens; fala do operador, `{s}`: {q}; que o ângulo de Miguel seja esse sistema é leitura dele [ONTO]): em qualquer espaço de Hilbert, o lock mínimo `1 − P` sobre um vetor `Ω` (`lockDe`) tem gap espectral 1 (`o_lock_tem_gap_um`); na unidade posta o gap vale `u` (`o_gap_com_unidade`), o `E₀` da Lei do Diminuto, e a tônica fica meio-tom acima dele. Num estado a um ângulo θ de `Ω` o lock tem valor esperado `sen²θ` (`lock_no_angulo`); no ângulo de Miguel, β (`lock_no_angulo_de_miguel`); na unidade posta esse valor esperado é `Δ = β · u`, a energia retida (`retidoNoAngulo`, `o_retido_e_o_valor_esperado_do_lock`). `Δ` não é gap: é 1/β vezes menor (o gap é {gd} vezes `Δ`). [REAL, condicional] O `HminMic` do kernel é instância desses lemas (`HminMic_e_o_lock`), condicional a um `FockCertificate`, que o kernel não habita. A tônica é `Δ/α`; a massa é a projeção transversal de `Δ`; o psíon é `√2 · Δ` (`the_gap_closes`). Neste rito: `Δ` = {dl} eV, `τ` = {tau} s, `Γ_B` = {gam} eV, `Q = √2/β` = {q_v}. "
              "[ONTO, a ratificar pelo operador] ler `tempoDoRetido` como o τ★ do sistema: é tempo próprio, não `t_P`, e não mexe no ramo canônico. `κ` segue testemunha: `κ = F(α, β, θ_M)` é proibido como objetivo de busca, e `κ` só aparece como hipótese em `o_relogio_do_retido`. `U_E_NOT_DERIVED` fica: `Δ` carrega `u`, e nada fixa `u`. Medida negativa: sob esta leitura, `E_fluxo = c⁵τ/(4πG)` vale {ef} eV, não é `E₀`, e a ponte `E_fluxo = E₀` do Kimi não vale aqui. O invariante `K` do disco não depende da inclinação, logo o ângulo não fixa `K` [OPEN]; quais são as cinco notas segue [OPEN], e só se sabe, por fala dele, que o ângulo de Miguel pertence a elas. "
              "[ONTO] {q_el}, e {q_or}. [REAL] `zero_mode_weight_is_one` e `alpha_transport` existem no kernel; [ONTO, da gerência] lê-los como a forma dessa fala é leitura da gerência. Homônimo, dito: `alphaKappa` não é a `α` de estrutura fina, e `κ` ali é a profundidade modular, não o relógio; o gradiente é negativo em `κ > 0`; a palavra cauda não está no teorema; isso não deriva a unidade.",
              n=V["gap"]["n_checks"], s=ss["mod"], q=_cita("o sistema físico que fornece a medidade da tônica por ujm gap com unidade e pertence à mesma pêntada é o ângulo de MIguel"), gd=_p(v["gap_sobre_Delta"], 1), dl=_p(v["Delta_eV"], 9), tau=_pe(v["tau_s"], 3), gam=_pe(v["Gamma_B_eV"], 3), q_v=_p(v["Q"], 3), ef=_pe(v["E_fluxo_eV"], 2), q_el=_cita("a inscrição da luz que singulariza o sistema é a eletricidade"), q_or=_cita("a origem da medida é a matemática, ou seja, o 1 absoluto, que representa 1 Eletrovolt"))


'''
patch(os.path.join("pos_rito", "textos_v405_novo.pysnip"), [
    ("# ga_reclassificacao_v405 (a classe nova do teste do Grande Atrator, ao lado) e kh_n1_cobertura_v405, e as secoes", "# ga_reclassificacao_v405 (a classe nova do teste do Grande Atrator, ao lado), gap_v405 (o gap espectral do lock e o valor esperado dele no angulo de Miguel, ao lado) e kh_n1_cobertura_v405, e as secoes"),
    ('"lock_no_angulo_de_miguel", "tempoDoGap", "o_relogio_do_gap", "zero_mode_weight_is_one", "alpha_transport")', '"lock_no_angulo_de_miguel", "tempoDoRetido", "o_relogio_do_retido", "retidoNoAngulo", "lockDe", "o_gap_com_unidade", "o_retido_e_o_valor_esperado_do_lock", "HminMic_e_o_lock", "HminMic", "FockCertificate", "alphaKappa", "o_psion_e_a_projecao_do_modo", "zero_mode_weight_is_one", "alpha_transport")'),
    ("as demais notas ficam sustentadas (`modular_sustenta`), a escala e o tom ficam (`modular_mantem_a_escala`: a escala é o que fica parado, e a razão à tônica muda), e nenhum fator leva o acorde ao acorde modulado (`modular_nao_e_transposicao`): o meio-tom quebra a simetria do acorde, porque separa a tônica das notas sustentadas, mas não quebra a liberdade global. `E₀` é",
     "as demais notas ficam sustentadas (`modular_sustenta`), elas e as razões entre elas ficam (`modular_mantem_a_escala`: a escala é o que fica parado, e a razão à tônica muda), e nenhum fator leva o acorde ao acorde modulado (`modular_nao_e_transposicao`): o meio-tom quebra a simetria do acorde, porque separa a tônica das notas sustentadas, mas não quebra a liberdade global. [INPUT] O tom fica, na fala dele: o kernel não tem termo para o tom. `E₀` é"),
    ("· REAL as medidas · KNOWN a ordem linear · INPUT/ONTO a ponte de fonte]", "· REAL as medidas · DERIVED a ordem linear, condicional à Face C · INPUT/ONTO a ponte de fonte]"),
    ("não discrimina da RG (na ordem linear `M_TGL = M_RG`). ", "não discrimina da RG (na ordem linear `M_TGL = M_RG` [DERIVED, condicional à Face C na ordem linear; a derivação é da teoria, `prove_ga_mass_audit`, v98]). "),
    ("o registro `gap_v405`{vg}: o gap lido do ângulo de Miguel, ao lado, com {nckg} checagens em runtime", "o registro `gap_v405`{vg}: o gap espectral do lock e o valor esperado dele no ângulo de Miguel, ao lado, com {nckg} checagens em runtime"),
    ("`tempoDoGap` lido como o τ★ do sistema (a ratificar) e as demais do registro.", "`tempoDoRetido` lido como o τ★ do sistema (a ratificar) e as demais do registro."),
    ("`tempoDoGap` como o τ★ do sistema, a ratificar; a inscrição da luz como a eletricidade e a origem da medida.", "`tempoDoRetido` como o τ★ do sistema, a ratificar; o ângulo de Miguel como o sistema do gap com unidade; a inscrição da luz como a eletricidade e a origem da medida."),
    ("as escolhas da partitura do Grande Atrator; a revisão independente.\") % (", "as escolhas da partitura do Grande Atrator; a ratificação da leitura de `tempoDoRetido` como o τ★ do sistema. A revisão de terceiro do pacote é condição da instalação, não pendência dele.\") % ("),
    ("`campos_fechados_e_leituras_v405`, `ga_reclassificacao_v405` e `kh_n1_cobertura_v405`; \"", "`campos_fechados_e_leituras_v405`, `ga_reclassificacao_v405`, `gap_v405` e `kh_n1_cobertura_v405`; \""),
    ("`campos_fechados_e_leituras_v405`, `ga_reclassificacao_v405`, `kh_n1_cobertura_v405`, `%s`\" % TOPICO_NOVO", "`campos_fechados_e_leituras_v405`, `ga_reclassificacao_v405`, `gap_v405`, `kh_n1_cobertura_v405`, `%s`\" % TOPICO_NOVO"),
    ("\"> - **O gap, ao lado** [REAL · ONTO · OPEN]: o lock mínimo tem gap 1; no ângulo de Miguel lê β, e na unidade posta `Δ = β · u`; ler `tempoDoGap` como o τ★ do sistema é leitura [ONTO], a ratificar pelo operador; `κ` segue testemunha; `Δ` carrega `u`, e nada fixa `u`.\",",
     "\"> - **O gap, ao lado** [REAL · ONTO · OPEN]: o lock mínimo tem gap espectral 1; na unidade posta, `u`, o `E₀` da Lei do Diminuto, e a tônica fica meio-tom acima dele. No ângulo de Miguel o valor esperado do lock é β, e na unidade posta `Δ = β · u`, a energia retida: `Δ` não é gap, é 1/β vezes menor. A fala do operador diz gap com unidade; que o ângulo de Miguel seja esse sistema é leitura dele [ONTO]; ler `tempoDoRetido` como o τ★ do sistema é leitura [ONTO], a ratificar por ele; `κ` segue testemunha; `Δ` carrega `u`, e nada fixa `u`.\","),
    ("o `sen 45°` tem duas leituras que coincidem na forma; E11,", "o `sen 45°` tem duas leituras que coincidem na forma, e mais uma leitura do mesmo `sen 45°`, por aritmética; E11,"),
    ("a ratificação da leitura de `tempoDoGap` como o τ★ do sistema; a ratificação das decisões D27 a D33", "a ratificação da leitura de `tempoDoRetido` como o τ★ do sistema; a ratificação das decisões D27 a D33"),
], blocos=[("def _gap(V):", "def _zero(V):", _GAP_T)])

# ------------------------------------------------------------------------------------------- o Mapa do pos-rito
patch(os.path.join("pos_rito", "registrar_mapa_v405_montar.pysnip"), [
    ("o registro gap_v405 le o gap do angulo de Miguel, ao lado, sem fixar u;", "o registro gap_v405 le o gap espectral do lock (u, na unidade posta) e o valor esperado dele no angulo de Miguel (Delta, que nao e' gap), ao lado, sem fixar u;"),
    ("revisao independente das quatro pedras.\"", "revisao independente das quatro pedras: ver o caderno revisao_terceiro do pacote v405.\""),
    ("revisao independente das pedras e dos derivados\"", "revisao independente das pedras e dos derivados: ver o caderno revisao_terceiro do pacote v405\""),
], troca_tudo=[("revisao independente da pedra", "revisao independente da pedra, ver o caderno revisao_terceiro do pacote v405", 4)])

# ------------------------------------------------------------------------------------------- a guarda
patch("guarda_frases_v405.py", [
    ('''"a escala absoluta segue livre", "a escala relativa está pinada", "the absolute scale stays free", "THE_ABSOLUTE_SCALE_STAYS_FREE"]
''', '''"a escala absoluta segue livre", "a escala relativa está pinada", "the absolute scale stays free", "THE_ABSOLUTE_SCALE_STAYS_FREE",
             "o gap é Δ", "o gap e' Delta", "o gap é a energia retida", "na unidade posta, o gap é a energia retida, Δ = β·u", "o gap é β·u", "o gap = beta.u", "o gap espectral é Δ", "gap Δ = β · u", "Δ é o gap", "`Δ` é o gap", "Delta e' o gap", "a energia retida é o gap", "β·u é o gap", "the gap is Δ", "the gap is the retained energy", "Δ is the gap", "the retained energy is the gap",
             "o gap de 12,03 meV", "um gap de 12.03 meV", "12,03 meV é o gap", "o gap vale 12,03 meV", "12,03 meV, o gap do lock", "the gap of 12.03 meV", "o gap lido do ângulo de Miguel", "the gap read from the angle of Miguel", "tempoDoGap", "o tempo do gap", "the time of the gap", "DELTA_IS_THE_GAP", "THE_TIME_OF_THE_GAP_IS_A_PROPER_TIME",
             "a escala e o tom ficam", "mantendo a escala e o tom", "the scale and the key stay"]
'''),
    ('''"transpor e' so' a liberdade do no-go", "o diminuto modula a tonica, mantendo a escala e o tom"]
''', '''"transpor e' so' a liberdade do no-go", "o diminuto modula a tonica, mantendo a escala",
         "`Δ` NÃO é gap: é o valor esperado, 1/β vezes menor que o gap", "Δ não é gap", "Delta NAO e' gap", "Δ is not a gap: it is 1/β times smaller", "o gap espectral do lock é 1", "na unidade posta o gap vale u, o E₀ da Lei do Diminuto", "o gap é 83,1 vezes Δ", "the gap is 83.1 times Δ", "o valor esperado do lock no ângulo de Miguel é β", "Δ = 12,03 meV não é gap", "12.03 meV is not the gap", "gap com unidade", "gap_v405", "the_gap_closes", "o_gap_com_unidade", "o_lock_tem_gap_um", "o tom fica, na fala dele: o kernel nao tem termo para o tom", "the key stays, in his saying"]
'''),
])

# ------------------------------------------------------------------------------------------- os lotes de regras
patch("derivar_encanamento_v405_regrasC2_ensaio.py", [
    ('[l_["n"] for l_ in R405["psion"]["leituras_que_entram"]] == [4, 6, 7, 13, 14]', '[l_["n"] for l_ in R405["psion"]["leituras_que_entram"]] == [4, 6, 7, 13, 14, 15]'),
    ('''U["gap_os_numeros_recalculados_aqui_com_o_beta_de_runtime"] = bool(abs(_gpv.get("Delta_eV", 0.0) / _bf5 - 1.0) <= 1e-14 and''', '''U["gap_os_numeros_recalculados_aqui_com_o_beta_de_runtime"] = bool(abs(_gpv.get("Delta_eV", 0.0) / _bf5 - 1.0) <= 1e-14 and _gpv.get("gap_espectral_eV") == 1.0 and abs(_gpv.get("gap_sobre_Delta", 0.0) * _bf5 - 1.0) <= 1e-13 and'''),
    ('''U["gap_cada_elo_recusa_beta_massa_e_as_frases"] = bool(all(r_["all_verified"] is False for r_ in _negsG.values()) and len(_negsG) == 4 and''',
     '''_gpD = list(_gpS["diz"]); _gpS["diz"][:] = _gpD + ["Delta e' o gap do lock"]
try:
    _negsG["frase_delta_gap"] = _GP_R(cs())
finally:
    _gpS["diz"][:] = _gpD
U["gap_cada_elo_recusa_beta_massa_e_as_frases"] = bool(all(r_["all_verified"] is False for r_ in _negsG.values()) and len(_negsG) == 5 and'''),
])
patch("derivar_encanamento_v405_regrasE1_p00.py", [
    ('''_cad = [(_rec_r6, _rec_r5), (_rec_r5, _rec_r4), (_rec_r4, _rec_r3), (_rec_r3, _rec_r2)]
''', '''_rec_r7 = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_R7_01nov.json"))
_cad = [(_rec_r7, _rec_r6), (_rec_r6, _rec_r5), (_rec_r5, _rec_r4), (_rec_r4, _rec_r3), (_rec_r3, _rec_r2)]
'''),
    ('''chk("[v405] as pedras sao as da ERRATA R6 da gerencia: o sha256 de cada arquivo == o sha256_depois do recibo vigente (oito arquivos), e a cadeia de custodia fecha: em R6 -> R5 -> R4 -> R3 -> R2,''', '''chk("[v405] as pedras sao as da ERRATA R7 da gerencia: o sha256 de cada arquivo == o sha256_depois do recibo vigente (oito arquivos), e a cadeia de custodia fecha: em R7 -> R6 -> R5 -> R4 -> R3 -> R2,'''),
    ('''for k_, v_ in _rec_r6["pedras"].items()) and len(_rec_r6["pedras"]) == 8 and all(all(''', '''for k_, v_ in _rec_r7["pedras"].items()) and len(_rec_r7["pedras"]) == 8 and all(all('''),
    ('''and len(_rec_err["arquivos"]) == 7, len(_rec_r6["pedras"]))''', '''and len(_rec_err["arquivos"]) == 7, len(_rec_r7["pedras"]))'''),
])
patch("derivar_encanamento_v405_regrasD2_instalar.py", [
    ('''    ("restaura os 9 backups de BYTES (um.py, core, selo, .md, manifesto, pilar, o sidecar um_absoluto_selo_acom.json, TGLExt.lean, TGL/Audit.lean)",''',
     '''    ("import datetime, glob, hashlib, json, os, shutil, sys\\n", "import datetime, glob, hashlib, json, os, shutil, sys\\nif sys.flags.optimize:\\n    raise SystemExit(\\"RECUSO: rodar sem -O / PYTHONOPTIMIZE\\")\\n", 1),
    ("Fail-closed: backup ausente => para sem tocar o que resta. Molde: reverter_v404.py.", "Fail-closed: backup ausente => para sem tocar o que resta. NAO restaura, como no molde: os .tex e os .pdf que o rito reescreve no Nos ficam como o rito os deixou, e o .lake do kernel nao e' limpo; a proxima rodada os regenera. Recusa -O, como o instalar. Molde: reverter_v404.py.", 1),
    ('print(json.dumps({"ok": rec["ok"], "um_py": umsha, "restaurados": len(rec["restaurado"]), "quarentena": len(rec["quarentena"]), "registro": reg}, ensure_ascii=False))', 'print(json.dumps({"ok": rec["ok"], "um_py": umsha, "restaurados": len(rec["restaurado"]), "quarentena": len(rec["quarentena"]), "registro": reg, "nao_restaura": "os .tex e os .pdf que o rito reescreve e o .lake do kernel"}, ensure_ascii=False))', 1),
    ("restaura os 9 backups de BYTES (um.py, core, selo, .md, manifesto, pilar, o sidecar um_absoluto_selo_acom.json, TGLExt.lean, TGL/Audit.lean)",'''),
    ('''os registros por spec novos do core v405 (cunhagens_v405, com as falas de 30/10 a 01/11, campos_fechados_e_leituras_v405,", 1),''', '''os registros por spec novos do core v405 (cunhagens_v405, com as falas de 30/10 a 01/11, campos_fechados_e_leituras_v405, ga_reclassificacao_v405, gap_v405,", 1),'''),
])
print("FEITO", TS)
