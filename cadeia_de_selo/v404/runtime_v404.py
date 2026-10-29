# ---- v404: A PROJECAO TRANSVERSAL DA MEIA-NAT (o sen 45 graus do neutrino deixa de ser postulado), Jo 8,32 (o nome do operador para o triplo inteiro) E A ERRATA DE F2b (o canal retirado antes do dado, AO LADO). TRES registros PEQUENOS, com FUNCAO, lidos no ponto real do main,
# logo depois do bandeiras_do_gate_v403: dois leem do kernel do PROPRIO rito a composicao da pedra (bandeira True, trio, proveniencia no modulo da pedra), os teoremas do contrato e os termos antigos que ela cita, a fonte da pedra por sha256, as falas de 28/10 por sha256 e um TEXTO-CONTEXTO
# do kernel embutido, e CALCULAM, com beta = alfa CODATA 2018 x sqrt(e) em runtime (nunca literal), um modelo honesto de cada pedra: a Projecao Transversal (a Meia-Nat e' o angulo de 45 graus; o m_nu do programa = beta . sen(pi/4) . E0, com E0 = 1 eV DECLARADO; theta_M longe de pi/4;
# a derivada de sen^2 em pi/4 e' 1) e o Jo8v32 (a conjuncao das tres estrelas da v403: reler a mecanica numerica dos tres registros da v403 com o beta deste rito). O TERCEIRO registro, f2b_errata_v404, le o V1 do ramo B (v386, congelado por hash), a calibracao A (NOT_BLIND) e a previsao do par,
# todos do registro ramo_b_preregistration_v386 (a funcao que ja' os transcreve), e grava a ERRATA AO LADO da cobranca F2b: o canal passa de AWAITING a retirado antes do dado; nenhum desfecho; o V1 e o registro da v386 NAO sao reescritos. A identificacao da massa com a projecao transversal e a leitura
# por Jo 8,31-32 sao [ONTO], nao termos de kernel. O gate nao se move.
# Fonte autoral deste bloco: runtime_v404.py (cadeia_de_selo/v404); os contratos (_V404_CONTRACTS) e as falas (_V404_VERBATINS2) sao DERIVADOS do build e dos arquivos, nunca digitados.
import math as _m404


def _v404_close(a_, b_, e_=1e-11):
    return abs(a_ - b_) <= e_ * (1.0 + abs(a_) + abs(b_))


def v404_parse_deformacao(txt_):
    """v404 -- le a deformacao comum de A como o V1 a escreve («+0,072 [+0,015; +0,134]», virgula decimal): devolve (central, inferior, superior) ou None."""
    import re as _re404
    m_ = _re404.match(r"^\s*([+-]?\d+,\d+)\s*\[\s*([+-]?\d+,\d+)\s*;\s*([+-]?\d+,\d+)\s*\]", str(txt_ or ""))
    if not m_:
        return None
    return tuple(float(g_.replace(",", ".")) for g_ in m_.groups())


def v404_projecao_mechanics(beta_, core_, c_):
    """v404 -- a mecanica da PROJECAO TRANSVERSAL DA MEIA-NAT em dupla precisao: as leituras numericas dos teoremas da pedra (x = 1 - x => 1/2; sen^2(pi/4) = 1/2 e halfRoot; sqrt x = sen(pi/4); a unicidade em [0, pi/2]; a forma do neutrino beta . sen45 . E0 = sen^2(theta_M) . sen(pi/4) . E0;
    theta_M != pi/4; a derivada de sen^2 em pi/4) com beta recebido (o chamador o calcula em runtime: alfa CODATA x sqrt(e); NUNCA literal), a releitura do m_nu do programa (neutrino_mass.m_nu_meV) e o conferir do texto antigo do angle_status (que fica ao lado, intacto).
    Devolve {passed, checks, values, n_checks}. Nao levanta para beta invalido: devolve passed False."""
    import hashlib as _hl404
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m404.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "p0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    s4_ = _m404.sin(_m404.pi / 4.0)
    sq_ = lambda t_: _m404.sin(t_) ** 2
    lo_, hi_ = 0.0, 1.0
    for _ in range(200):
        mid_ = (lo_ + hi_) / 2.0
        if mid_ - (1.0 - mid_) < 0.0:
            lo_ = mid_
        else:
            hi_ = mid_
    raiz_ = (lo_ + hi_) / 2.0
    grade_ = [k_ / 1000.0 for k_ in range(0, 1001)]
    fixos_ = [x_ for x_ in grade_ if abs(x_ - (1.0 - x_)) <= 1e-15]
    ck_("p1", "★ half_from_self_conjugate e half_from_J_symmetry: o ponto fixo de x -> 1 - x, achado por bissecao, e' 1/2 (|x - 1/2| <= 1e-15), e na grade de 1001 pesos o UNICO peso autoconjugado e' 0,5; a J-simetria (peso de dentro = peso de fora, soma 1) da o mesmo 1/2",
        abs(raiz_ - 0.5) <= 1e-15 and fixos_ == [0.5], [raiz_, len(grade_)])
    ck_("p2", "★ half_amplitude_sq e half_amplitude_eq_halfRoot: sen^2(pi/4) = 1/2 (|erro| <= 1e-15) e a amplitude transversal sen(pi/4) e' a raiz da metade (o halfRoot da bancada angular), |sen(pi/4) - sqrt(1/2)| <= 1e-15",
        abs(s4_ ** 2 - 0.5) <= 1e-15 and abs(s4_ - _m404.sqrt(0.5)) <= 1e-15, [s4_ ** 2, s4_])
    ck_("p3", "★ transverse_amplitude_of_self_conjugate: para todo x autoconjugado (x = 1 - x), sqrt x = sen(pi/4) (|erro| <= 1e-15): de x = 1 - x ao angulo agudo",
        bool(fixos_) and all(abs(_m404.sqrt(x_) - s4_) <= 1e-15 for x_ in fixos_), [len(fixos_)])
    n4_ = 20000
    th_ = [k_ * (_m404.pi / 2.0) / n4_ for k_ in range(n4_ + 1)]
    g_ = [sq_(t_) - 0.5 for t_ in th_]
    zeros_ = [k_ for k_, v_ in enumerate(g_) if abs(v_) <= 1e-12]
    ck_("p4", "★ forty_five_unique: em [0, pi/2] (20001 pontos) sen^2 theta - 1/2 e' estritamente crescente e so' se anula (|.| <= 1e-12) em UM ponto, o de indice 10000 (o ponto do meio), onde theta = pi/4 (|theta - pi/4| <= 1e-15)",
        all(g_[k_ + 1] > g_[k_] for k_ in range(n4_)) and zeros_ == [n4_ // 2] and abs(th_[n4_ // 2] - _m404.pi / 4.0) <= 1e-15, [zeros_, n4_ + 1])
    e0_ = float(c_["neutrino"]["e0_declarado_eV"])
    thm_ = _m404.asin(_m404.sqrt(beta_))
    f1_ = beta_ * s4_ * e0_
    f2_ = sq_(thm_) * _m404.sin(_m404.pi / 4.0) * e0_
    m_meV_ = f1_ * 1000.0
    m_core_ = (core_.get("neutrino_mass") or {}).get("m_nu_meV")
    ck_("p5", "★★ neutrino_mass_form_eq: com beta = alfa x raiz de e (runtime) e theta_M = arcsin(raiz de beta), beta . sen45 . E0 = sen^2(theta_M) . sen(pi/4) . E0 (a 1e-12 relativo; E0 = 1 eV DECLARADO, nao derivado), e o m_nu do programa (neutrino_mass.m_nu_meV) e' beta . sen(pi/4) . 1 eV a 1e-12 relativo",
        abs(f1_ - f2_) <= 1e-12 * abs(f1_) and isinstance(m_core_, float) and abs(m_meV_ / m_core_ - 1.0) <= float(c_["neutrino"]["rel_tol"]), [m_meV_, m_core_])
    ck_("p6", "★ theta_miguel_ne_pi_div_four: beta != 1/2, logo theta_M != pi/4: theta_M = arcsin(raiz de beta) fica a mais de 0,5 rad de pi/4 (e abaixo dele): o angulo agudo do neutrino NAO e' o angulo de Miguel",
        beta_ != 0.5 and abs(thm_ - _m404.pi / 4.0) > 0.5 and thm_ < _m404.pi / 4.0, [thm_])
    h_ = 1e-6
    der_ = lambda t_: (sq_(t_ + h_) - sq_(t_ - h_)) / (2.0 * h_)
    pts_ = (0.1, 0.3, 0.7, _m404.pi / 4.0, 1.2, 1.5)
    ck_("p7", "★ transverse_weight_hasDerivAt_half: a derivada de sen^2 theta em pi/4 vale 1 (diferenca central, h = 1e-6, |erro| <= 1e-9) e coincide com sen 2theta nos pontos de teste (|erro| <= 1e-7); sen 2theta <= 1 em toda a grade com maximo EXATO em pi/4: o ponto autoconjugado e' onde a sombra muda mais depressa",
        abs(der_(_m404.pi / 4.0) - 1.0) <= 1e-9 and all(abs(der_(t_) - _m404.sin(2.0 * t_)) <= 1e-7 for t_ in pts_) and max(range(len(th_)), key=lambda k_: _m404.sin(2.0 * th_[k_])) == n4_ // 2 and all(_m404.sin(2.0 * t_) <= 1.0 for t_ in th_), [der_(_m404.pi / 4.0)])
    nm_ = core_.get("neutrino_mass") or {}
    ang_ = str(nm_.get("angle_status") or "")
    ck_("p8", "a errata do angulo e' AO LADO: o angle_status do programa (neutrino_mass) segue com o texto ANTIGO (comeca por «sin(45deg) e POSTULADO», sha256 do texto inteiro == o da v403 selada), o frozen_hash da regra de decisao e o veredito do canal NAO se moveram e o m_nu e' o da v403 a 1e-12 relativo",
        ang_.startswith(c_["neutrino"]["angle_status_antigo_prefixo"]) and _hl404.sha256(ang_.encode("utf-8")).hexdigest() == c_["neutrino"]["angle_status_antigo_sha256"] and nm_.get("frozen_hash") == c_["neutrino"]["frozen_hash_v403"] and nm_.get("verdict") == c_["neutrino"]["verdict_v403"]
        and isinstance(m_core_, float) and abs(m_core_ / float(c_["neutrino"]["m_nu_meV_v403"]) - 1.0) <= 1e-12, [nm_.get("verdict"), nm_.get("frozen_hash")])
    vals_ = {"beta": beta_, "sin_pi_over_4": s4_, "sin_sq_pi_over_4": s4_ ** 2, "theta_M": thm_, "theta_M_minus_pi_over_4": thm_ - _m404.pi / 4.0, "m_nu_meV_runtime": m_meV_, "m_nu_meV_core": m_core_, "m_nu_rel_diff": (m_meV_ / m_core_ - 1.0) if isinstance(m_core_, float) else None,
             "e0_eV_declared": e0_, "derivative_of_sin_sq_at_pi_over_4": der_(_m404.pi / 4.0), "grid_weights": len(grade_), "grid_angles": n4_ + 1, "self_conjugate_weights": fixos_}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def v404_jo8_mechanics(beta_, core_, c_):
    """v404 -- a mecanica do JO8v32 (a conjuncao das tres estrelas da v403 na ordem de Jo 8,31-32): (j1) as tres estrelas existem no kernel do rito, no trio, no modulo delas; (j2) os tres registros da v403 selaram neste rito e trazem essas estrelas entre os teoremas do contrato; (j3) a declaracao honesta: a conjuncao
    e' um termo sem hipoteses, mas Vida e Verdade carregam hipoteses NOMEADAS no enunciado delas (a Caminho nao); (j4) a mecanica numerica dos tres registros da v403, RELIDA com o beta deste rito (as funcoes v403_*_mechanics do proprio programa); (j5) o nome do operador e a ratificacao estao verbatim nas falas embutidas.
    Devolve {passed, checks, values, n_checks}. Nao levanta para beta invalido: devolve passed False."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m404.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "j0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    kf_ = core_.get("kernel_formalization") or {}; axr_ = kf_.get("axiom_report") or {}; src_ = kf_.get("declaration_sources_v394") or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and all(isinstance(x_, str) for x_ in axr_.get(n_)) and set(axr_.get(n_)) <= trio_)
    ordem_ = list(c_["order_of_the_verse"])
    ck_("j1", "as TRES estrelas da v403 que a conjuncao cita (caminho_e_a_ponte_da_escala_dual, verdade_e_a_esperanca_condicional, vida_e_a_queda_sem_geometria) existem no kernel do rito, no trio, cada uma no modulo dela (TGL_DECL_SOURCE), na ordem do versiculo: permanecer, conhecer, libertar",
        len(ordem_) == 3 and sorted(ordem_) == sorted(c_["support"]) and all(em_trio_(n_) and src_.get(n_) == c_["support"][n_] for n_ in ordem_), [[n_, src_.get(n_)] for n_ in ordem_])
    regs_ = (("caminho_v403", ordem_[0]), ("verdade_adendo_v403", ordem_[1]), ("vida_v403", ordem_[2]))
    ck_("j2", "os tres registros da v403 (caminho_v403, verdade_adendo_v403, vida_v403) selaram NESTE rito (all_verified) e trazem a estrela citada entre os teoremas do contrato deles (formal_theorems True)",
        all((core_.get(r_) or {}).get("all_verified") is True and ((core_.get(r_) or {}).get("formal_theorems") or {}).get(t_) is True for r_, t_ in regs_), [r_ for r_, _ in regs_])
    comp_ = {r_: ((core_.get(r_) or {}).get("unconditional") or {}).get("composition") for r_, _ in regs_}
    ck_("j3", "a declaracao das hipoteses: a conjuncao e' um termo SEM hipoteses, mas Vida (IsotropicPost) e Verdade (o indice 1/beta, hpp e hopt) carregam hipoteses NOMEADAS no enunciado delas e o Caminho nao (como os registros da v403 as declararam): citadas, nao pagas",
        comp_ == {"caminho_v403": "NO_CERTIFICATE_AS_HYPOTHESIS", "verdade_adendo_v403": "CONDITIONAL_ON_NAMED_HYPOTHESES_IN_THE_STATEMENT", "vida_v403": "CONDITIONAL_ON_NAMED_HYPOTHESES_IN_THE_STATEMENT"} and c_.get("named_hypotheses_in_the_statement") is True, comp_)
    r1_, r2_, r3_ = v403_caminho_mechanics(beta_), v403_vida_mechanics(beta_), v403_verdade_adendo_mechanics(beta_)
    ck_("j4", "a mecanica numerica dos tres registros da v403 RELIDA com o beta deste rito (as funcoes do proprio programa: 5 + 6 + 5 checagens) passa nas tres",
        r1_["passed"] and r2_["passed"] and r3_["passed"] and [r1_["n_checks"], r2_["n_checks"], r3_["n_checks"]] == list(c_["v403"]["n_checks"]), [r1_["n_checks"], r2_["n_checks"], r3_["n_checks"]])
    vn_ = _V404_VERBATINS2.get(c_["verbatins"][0]) or {}; vr_ = _V404_VERBATINS2.get(c_["verbatins"][1]) or {}
    ck_("j5", "o nome do operador esta verbatim na fala embutida («só consegui sintetizar assim: Jo8:32») e a ratificacao tambem («Perfeito, concordo com tudo»), cada fala com o sha256 do texto embutido",
        c_["name_phrase"] in (vn_.get("text") or "") and c_["ratification_phrase"] in (vr_.get("text") or ""), [vn_.get("sha256", "")[:16], vr_.get("sha256", "")[:16]])
    vals_ = {"beta": beta_, "v403_mechanics_checks": [r1_["n_checks"], r2_["n_checks"], r3_["n_checks"]], "v403_mechanics_passed": [r1_["passed"], r2_["passed"], r3_["passed"]], "order_of_the_verse": ordem_, "composition_declared": comp_,
             "p_plus_factor_at_beta": r1_["values"].get("pplus_factor_at_beta"), "post_weight_loss_per_unit": r2_["values"].get("loss_per_unit"), "alpha_squared": r3_["values"].get("alpha_squared")}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def _v404_formal(core, c_, txt_):
    """A evidencia FORMAL do registro, lida do kernel do PROPRIO rito: a escada exata, a composicao e os teoremas do contrato (bandeira True, trio, proveniencia no modulo da pedra), os termos antigos que a pedra cita (no trio, com a proveniencia que o compilador emite),
    a fonte da pedra por sha256 (embutida == contrato == hash formal do rito), as falas de 28/10 por sha256, o TEXTO-CONTEXTO no kernel embutido e a guarda P18 sobre o texto. Devolve um dict; `formal` e' o conjunto."""
    import hashlib, json as _j404
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
        v_ = _V404_VERBATINS2.get(k_)
        ver_[k_] = bool(v_ and hashlib.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and all(t_ in v_["text"] for t_ in v_["trechos"]))
    unc_th_, unc_fl_ = c_["unconditional"]["theorem"], c_["unconditional"]["flag"]
    unc_ = {"theorem": unc_th_, "flag": unc_fl_, "flag_true": kf_.get(unc_fl_) is True, "axioms": axr_.get(unc_th_), "in_trio": em_trio_(unc_th_), "declared_in": src_.get(unc_th_), "in_kernel": bool(per_.get(unc_th_)),
            "composition": "NO_CERTIFICATE_AS_HYPOTHESIS" if not c_.get("named_hypotheses_in_the_statement") else "CONDITIONAL_ON_NAMED_HYPOTHESES_IN_THE_STATEMENT"}
    key_th_, key_fl_ = c_["key_theorem"]["theorem"], c_["key_theorem"]["flag"]
    key_ = {"theorem": key_th_, "flag": key_fl_, "flag_true": kf_.get(key_fl_) is True, "in_trio": em_trio_(key_th_), "declared_in": src_.get(key_th_), "in_kernel": bool(per_.get(key_th_)), "statement": c_["key_statement"]}
    cx_ = c_["context"]; cb_ = _EMBEDDED_KERNEL_FILES.get(cx_["path"])
    ctx_ = {"path": cx_["path"], "needles": list(cx_["needles"]), "text_in_embedded_kernel": bool(isinstance(cb_, str) and all(n_ in cb_ for n_ in cx_["needles"]))}
    ctx_["ok"] = bool(ctx_["text_in_embedded_kernel"])
    guarda_ = _v392_guarda_texto(_j404.dumps(txt_, ensure_ascii=False))
    formal_ = bool(kf_.get("all_verified") is True and exact_ and per_ and all(per_.values()) and sup_ and all(sup_.values()) and all(cit_.values()) and all(aux_.values()) and src_ok_ and all(ver_.values()) and key_["in_kernel"] and unc_["in_kernel"] and ctx_["ok"] and not guarda_)
    return {"exact_ladder": exact_, "formal_theorems": per_, "support_theorems": sup_, "cited_outside": cit_, "auxiliaries_outside_the_composition": aux_, "embedded_source_ok": src_ok_, "inscriptions": ver_, "unconditional": unc_, "key_theorem": key_,
            "context": ctx_, "guarda": guarda_, "formal": formal_}


_V404_RECUSA = "TGL_%s_V404__REFUSED_%s__GATE_UNMOVED"


def _v404_registro(core, chave_, nome_, mec_, tag_):
    """v404 -- o miolo comum dos DOIS registros de pedra com FUNCAO: le o kernel do rito (evidencia FORMAL), confere o beta (alfa x raiz de e, nunca literal), CALCULA a mecanica da pedra e sela. Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate."""
    c_ = _V404_CONTRACTS[chave_]; t_ = _V404_TEXTS[chave_]
    f_ = _v404_formal(core, c_, t_)
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
    out_ = {"all_verified": False, "estatuto": t_["estatuto"], "exact_ladder": f_["exact_ladder"], "formal_theorems": f_["formal_theorems"], "support_theorems": f_["support_theorems"], "embedded_source_ok": f_["embedded_source_ok"],
            "inscriptions": f_["inscriptions"], "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "unconditional": f_["unconditional"], "key_theorem": f_["key_theorem"], "context": f_["context"],
            "runtime_executed": False, "does_not_gate_core": True, "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"], "guarda_p18_violacoes": f_["guarda"][:5]}
    out_.update(t_["extras"])
    if not f_["formal"]:
        out_["verdict"] = _V404_RECUSA % (tag_, "FORMAL_OR_SOURCE_EVIDENCE")
    elif not beta_ok_:
        out_["verdict"] = _V404_RECUSA % (tag_, "BETA_IS_NOT_ALPHA_SQRT_E")
    else:
        try:
            mec_r_ = mec_(beta_rt_, core, c_)
            out_.update(runtime_executed=True, mechanics={"passed": mec_r_["passed"], "n_checks": mec_r_["n_checks"], "checks": mec_r_["checks"]}, values=mec_r_["values"], all_verified=bool(mec_r_["passed"]))
            out_["verdict"] = (t_["veredito_ok"] if mec_r_["passed"] else _V404_RECUSA % (tag_, "MECHANICS_CHECK_FAILED"))
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V404_RECUSA % (tag_, "RUNTIME_ERROR")
    core[nome_] = out_
    return out_


def projecao_transversal_v404(core):
    """v404 -- A PROJECAO TRANSVERSAL DA MEIA-NAT (a pedra do sen 45 graus; nome PROVISORIO da gerencia c1, aceito pelo operador ate' ele dar outro): lida no PONTO REAL do main, logo depois das bandeiras do gate (v403). Le do kernel do PROPRIO rito a pedra (bandeira, trio, modulo), os termos que ela cita,
    a fonte por sha256, as falas de 28/10 e o cabecalho da pedra no kernel embutido; e CALCULA, com beta = alfa CODATA 2018 x sqrt(e) em runtime, as leituras numericas dos teoremas, o m_nu do programa e a errata AO LADO do angle_status. Fail-closed em cada elo; nao move o gate. Validade no kernel nao e' creditacao."""
    return _v404_registro(core, "projecao", "projecao_transversal_v404", v404_projecao_mechanics, "PROJECAO_TRANSVERSAL")


def jo8v32_v404(core):
    """v404 -- JO8v32 (o nome que o operador deu ao triplo inteiro Caminho . Verdade . Vida, 28/10/2026): lido logo depois da Projecao Transversal. Le do kernel do PROPRIO rito a pedra, as tres estrelas que ela cita (v403), as falas e o cabecalho no kernel embutido; e RELE, com o beta do rito,
    a mecanica numerica dos tres registros da v403. Fail-closed em cada elo; nao move o gate. Validade no kernel nao e' creditacao."""
    return _v404_registro(core, "jo8v32", "jo8v32_v404", v404_jo8_mechanics, "JO8V32")


def f2b_errata_v404(core):
    """v404 -- A ERRATA AO LADO DA COBRANCA F2b (o canal do ramo B do ringdown retirado antes do dado): lida logo depois da errata ao lado de R6 da v386, quando o V1 do ramo B, a errata da v386 e o livro da v383 ja' estao no core (licao da 1a tentativa do rito v404, 28/10/2026). Le o V1 do ramo B (v386, congelado por hash), a calibracao A (NOT_BLIND) e a previsao do par do registro ramo_b_preregistration_v386 (a funcao que ja' os transcreve do V1; nada e'
    recalculado dos dados) e o livro de cobrancas da v383; confere que o V1 e o livro NAO se moveram; mede que a previsao do par fica fora do intervalo de A e de sinal oposto; e, se tudo confere, grava o estado novo do CANAL F2b (F2b_status_now) AO LADO: o V1 e o registro da v386 NAO sao reescritos.
    Nenhum desfecho sai de A; o conjunto D nao e' aberto; beta, a lei do defasamento e R2 ficam. Fail-closed em cada elo (se algo falha, F2b_status_now repete o estado antigo); nao move o gate."""
    c_ = _V404_CONTRACTS["f2b"]; t_ = _V404_TEXTS["f2b"]
    import hashlib as _hl404f, json as _j404f
    checks_ = []
    out_ = {"all_verified": False, "estatuto": t_["estatuto"], "runtime_executed": False, "does_not_gate_core": True, "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"], "guarda_p18_violacoes": []}
    out_.update(t_["extras"])
    rb_ = core.get("ramo_b_preregistration_v386") or {}
    out_["F2b_status_now"] = rb_.get("F2b_status")
    try:
        def ck_(id_, desc_, ok_, val_=None):
            checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
        le_ = core.get("ledger_errata_v386") or {}; led_ = core.get("the_ledger_of_charges_v383") or {}
        v1_ = c_["v1"]
        ck_("f1", "o V1 do ramo B (v386) foi lido por hash NESTE rito e esta como antes: all_verified e read_ok True, o mesmo identificador e o mesmo sha256 do JSON da v403 selada, o veredito do V1 AWAITING_DATA, o estado F2b AWAITING e o conjunto D cego com n = 14",
            rb_.get("all_verified") is True and rb_.get("read_ok") is True and rb_.get("identificador_read") == v1_["identificador"] and (rb_.get("sha256_read") or {}).get("json") == v1_["json_sha256"] and rb_.get("veredito_do_V1") == v1_["veredito"]
            and rb_.get("F2b_status") == v1_["f2b_status_antes"] and rb_.get("conjunto_D_n") == v1_["conjunto_D_n"], [rb_.get("veredito_do_V1"), rb_.get("F2b_status"), rb_.get("conjunto_D_n")])
        ledger_ = led_.get("ledger") or []
        ck_("f2", "o livro de cobrancas da v383 segue INTACTO (all_verified, 11 cobrancas com os mesmos ids e as mesmas contagens, F2 e R2 intocados) e a cobranca F2b da v386 ainda diz AWAITING (a errata e' AO LADO: nada e' reescrito)",
            led_.get("all_verified") is True and [x_.get("id") for x_ in ledger_] == c_["ledger_v383"]["ids"] and dict(led_.get("counts") or {}) == c_["ledger_v383"]["contagens"] and le_.get("v383_ledger_intact") is True and le_.get("F2_untouched") is True and le_.get("R2_untouched") is True
            and (le_.get("charge_F2b") or {}).get("token") == c_["charge_F2b_antes"]["token"] and (le_.get("charge_F2b") or {}).get("desfecho") == c_["charge_F2b_antes"]["desfecho"], [len(ledger_), dict(led_.get("counts") or {})])
        cv_ = rb_.get("central_values_NOT_BLIND_read_from_V1") or {}
        ca_ = v404_parse_deformacao(cv_.get("A_31_deformacao_comum_GWTC5"))
        ck_("f3", "a calibracao A (deformacao comum dos 31 eventos publicos, NOT_BLIND) e' LIDA do V1 pela funcao que ja' a transcreve, no formato «+c [inf; sup]», com inf < c < sup, c > 0, e e' a mesma da v403 selada",
            ca_ is not None and ca_[1] < ca_[0] < ca_[2] and ca_[0] > 0.0 and cv_.get("A_31_deformacao_comum_GWTC5") == c_["calibracao_A"]["texto"] and list(ca_) == [c_["calibracao_A"]["central"], c_["calibracao_A"]["inferior"], c_["calibracao_A"]["superior"]], [list(ca_) if ca_ else None])
        pin_ = (rb_.get("pins") or {}).get("delta_pred_A31_exato") or {}
        pred_ = pin_.get("read")
        ck_("f4", "a previsao do par (leitura de amplitude x lei de atraso KMS, delta_pred_A31_exato) e' LIDA do pino do V1 (read == pinned, equal True), e' negativa e e' a mesma da v403 selada",
            isinstance(pred_, float) and pin_.get("equal") is True and pin_.get("pinned") == pred_ and pred_ < 0.0 and pred_ == c_["previsao_do_par"]["valor"], [pred_])
        fora_ = bool(ca_ is not None and isinstance(pred_, float) and not (ca_[1] <= pred_ <= ca_[2]) and pred_ < 0.0 < ca_[0])
        ck_("f5", "A MEDIDA: a previsao do par fica FORA do intervalo da calibracao A e de sinal oposto a deformacao comum (a previsao e' negativa; o intervalo e' positivo); e' calibracao NOT_BLIND (o V1 a declarava), nao desfecho",
            fora_ and "NOT_BLIND" in str(rb_.get("status") or ""), [pred_, list(ca_) if ca_ else None])
        ck_("f6", "NENHUM desfecho sai de A e D nao e' aberto: nothing_opened True, no_pe_run True, no_central_value_in_spec_or_D True; o veredito do V1 continua o de antes (a regra de morte so' vale em D)",
            rb_.get("nothing_opened") is True and rb_.get("no_pe_run") is True and rb_.get("no_central_value_in_spec_or_D") is True and rb_.get("veredito_do_V1") == v1_["veredito"], [rb_.get("nothing_opened"), rb_.get("no_pe_run")])
        beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
        r2_ = next((x_ for x_ in ledger_ if x_.get("id") == "R2"), {})
        ver_ = {}
        for k_ in ("bocas", "calibrar"):
            v_ = _V404_VERBATINS2.get(c_["verbatins"][0 if k_ == "bocas" else 1])
            ver_[k_] = bool(v_ and _hl404f.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and all(t_x_ in v_["text"] for t_x_ in v_["trechos"]))
        ck_("f7", "beta, a lei e R2 FICAM: beta do rito == alfa x raiz de e (nunca literal), a cobranca R2 do livro tem o mesmo desfecho da v403 selada, e as duas falas do operador (o pedagio lido na propagacao; calibrar nao significa validar) estao embutidas por sha256 e verbatim",
            beta_ok_ and r2_.get("outcome") == c_["ledger_v383"]["R2_outcome"] and all(ver_.values()), [beta_ok_, r2_.get("outcome"), ver_])
        todos_ = all(k_["ok"] for k_ in checks_)
        out_.update(runtime_executed=True, mechanics={"passed": todos_, "n_checks": len(checks_), "checks": checks_}, all_verified=bool(todos_), inscriptions=ver_, beta_ok=beta_ok_,
                    values={"calibracao_A_central": ca_[0] if ca_ else None, "calibracao_A_inferior": ca_[1] if ca_ else None, "calibracao_A_superior": ca_[2] if ca_ else None, "previsao_do_par": pred_,
                            "previsao_fora_do_intervalo_de_A": fora_, "distancia_da_previsao_ao_limite_inferior_de_A": (ca_[1] - pred_) if (ca_ and isinstance(pred_, float)) else None, "n_cobrancas_v383": len(ledger_), "conjunto_D_n": rb_.get("conjunto_D_n"), "beta": beta_rt_})
        out_["F2b_status_now"] = c_["token_novo"] if todos_ else rb_.get("F2b_status")
        out_["F2b_status_before"] = rb_.get("F2b_status")
        out_["verdict"] = (t_["veredito_ok"] if todos_ else _V404_RECUSA % ("F2B_ERRATA", "A_CHECK_FAILED_THE_CHANNEL_STAYS_AS_BEFORE"))
        out_["guarda_p18_violacoes"] = _v392_guarda_texto(_j404f.dumps(t_, ensure_ascii=False))[:5]
        if out_["guarda_p18_violacoes"]:
            out_["all_verified"] = False; out_["F2b_status_now"] = rb_.get("F2b_status"); out_["verdict"] = _V404_RECUSA % ("F2B_ERRATA", "P18_TEXT_GUARD")
    except Exception as e_:   # noqa: BLE001
        out_.update(runtime_executed=True, error=repr(e_)[:300])
        out_["F2b_status_now"] = rb_.get("F2b_status")
        out_["verdict"] = _V404_RECUSA % ("F2B_ERRATA", "RUNTIME_ERROR")
    core["f2b_errata_v404"] = out_
    return out_
