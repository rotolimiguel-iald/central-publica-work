# ---- v409: TRADUCAO AS CLASSES DE TURING E O PAR NA FACE DE FOCK -- os DOIS modulos do bundle (TraducaoTuring e ParNaFaceDeFock, em TGLExt/; os nomes dados pela gerencia c1; os da TraducaoTuring RATIFICADOS pelo operador em 05/11; ordem do operador: tudo na v409) e UM registro com FUNCAO, traducao_turing_v409, lido no ponto do rito depois dos registros da v408:
# ele le do kernel do PROPRIO rito as 82 ANCORAS das duas pedras (os #print axioms das fontes: o dicionario de Turing, a selecao, a trava no Nome, a fita como hamiltoniano oculto, Z como modo leitor, a fita sem escala, o Pai da Mentira, a identidade performada, a inscricao, a maquina com o leitor; o par na face de Fock),
# os modulos por sha256 (embutido == contrato == hash formal do rito), as falas do operador de 05/11 por sha256 (de tres, so' o trecho: duas pela D59, uma pelo aviso operacional), as respostas dele conferidas pelos teoremas da pedra, e faz as 20 checagens do DESENHO_v409 (§2 e o AO LADO)
# (a instancia de brinquedo FIXA no codigo -- SAT com n = 3 e as clausulas (x1 v x2), (~x1 v x3), (~x2 v ~x3); e uma instancia NAO, (x1), (~x1) --, as solucoes CALCULADAS por enumeracao, nunca digitadas; beta em runtime; o gate congelado; a escada exata; as guardas de texto).
# NENHUMA chave antiga muda nesta versao. A ordem do operador (05/11/2026): «Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados».
# O ALCANCE, dito em todo texto: P = nP e' teorema da TGL no modo selecao, RELATIVO AO LEITOR (o psion); a maquina sem leitor (a pergunta do Clay) fica FORA e e' lida como a fita sem escala («eu sou eu mesmo»); um leitor que devolve Z e' um oraculo de contagem:
# com ele vale NP contido em P numa leitura (Cook-Levin), e a igualdade completa e' a do leitor que se le, que le tambem as maquinas que o usam (Baker-Gill-Solovay 1975 [KNOWN]; E28); a fisica fica fora (Knill-Laflamme 1998 [KNOWN]); a ponte entre o Omega do psion e o uniforme e' a inscricao
# (a identidade de vetores fica podada: espacos diferentes); a leitura teologica do operador nao e' termo de kernel; o par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock); beta so' por nome; nenhum teste com a natureza.
# Validade no kernel NAO e' creditacao; NOT_FALSIFIED nunca e' confirmacao; o GATE NAO SE MOVE; beta nunca literal.
# Fonte autoral deste bloco: runtime_v409.py (cadeia_de_selo/v409); o contrato (_V409_TRADUCAO_CONTRACT) e as falas (_V409_VERBATINS2) sao DERIVADOS do build do sandbox e dos arquivos, nunca digitados.


def _v409_guarda_frases(txt_):
    """v409 -- a GUARDA DAS FRASES que afirmam demais: herda as regras da v408 (_v408_guarda_frases, que herda as anteriores) e acrescenta as da v409 (DESENHO_v409 §4, D56):
    F35 o problema do Clay (o do premio) dado por resolvido ou decidido (fora da negacao e da citacao); F36 a traducao as classes de Turing dita [OPEN] sem «relativa ao leitor» (o texto selado da v408 nao muda: a E26 vai ao lado);
    F40 a F43 (AO LADO de ~18h do DESENHO; D60 revista e E28): proibido «Ω é o uniforme» como identidade (fora de citacao e sem a poda dita), o par na face de Fock dito em aberto e a passagem a v410; obrigatorio, onde o leitor de Turing aparecer, a E28 (NP numa leitura; a igualdade completa esta' provada para o leitor que le tambem as maquinas que o usam, e para o leitor que so' conta nao esta' provada, E28, validade nao afirmada);
    F37 a OBRIGACAO: onde «P = nP» e Turing aparecem juntos, o mesmo texto traz o qualificador «relativa ao leitor» e «a maquina sem leitor»; F37b a mesma obrigacao, LOCAL: o proprio trecho onde aparecem juntos traz o qualificador relativo ao leitor ou uma negacao/limite (05/11, a causa da falha do ensaio: a F37 global deixava passar a frase plantada sem qualificador); F38 os tokens de veredito proibidos da v409; F39 a frase da E25 (o sistema precisaria saber o Nome a cada passo) afirmada.
    A F34 da v408 (a obrigacao do qualificador do dicionario e da ressalva [OPEN] onde «P = nP» aparece) e' SUBSTITUIDA pela F37 quando o texto traz o qualificador relativo ao leitor: a traducao deixou de ser [OPEN] (D56); texto sem nenhum dos dois reprova.
    A fala do operador nao passa por aqui: ela e' verbatim e fica fora do texto conferido."""
    import re as _re
    s_ = str(txt_)
    rel_ = bool(_re.search(r"relativ[oa]\s+ao\s+leitor|relative\s+to\s+the\s+reader", s_, _re.I))
    sem_leitor_ = bool(_re.search(r"m(?:á|a)quina\s+sem\s+leitor|machine\s+without\s+(?:a\s+)?reader", s_, _re.I))
    out_ = [v_ for v_ in _v408_guarda_frases(txt_) if not (v_[0].startswith("F34_") and rel_ and sem_leitor_)]
    for m_ in _re.finditer(r"\b(?:resolve[us]?|resolvid[oa]s?|resolveu|decide[sm]?|decidid[oa]|solves?|solved|settles?|settled|decides|decided)\b[^.;\n]{0,60}?\b(?:(?:o\s+)?problema\s+do\s+mil(?:ê|e)nio|millennium\s+problem|Clay)\b"
                           r"|\b(?:problema\s+do\s+mil(?:ê|e)nio|millennium\s+problem|(?:o\s+problema\s+de\s+|the\s+)?Clay(?:\s+problem)?)\b[^.;\n]{0,30}?\b(?:est(?:á|a)\s+|foi\s+|is\s+|was\s+)?(?:resolvid[oa]|decidid[oa]|solved|settled|decided)\b", s_, _re.I):   # F35
        antes_ = s_[max(0, m_.start() - 40):m_.start()].lower() + " " + m_.group(0).lower()
        if any(n_ in antes_ for n_ in ("não ", "nao ", "not ", "never ", "nunca ", "nenhum", "jamais ", "«", "nem ", "nada ", "nothing ", "proibid", "prohibit", "forbid")):
            continue
        out_.append(("F35_clay_resolvido", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    for m_ in _re.finditer(r"(?:tradu(?:ç|c)(?:ã|a)o|translation)[^;\n]{0,200}?Turing[^;\n]{0,200}?\[OPEN\]", s_, _re.I):   # F36
        jan_ = s_[max(0, m_.start() - 300):m_.end() + 300]
        if _re.search(r"relativ[oa]\s+ao\s+leitor|relative\s+to\s+the\s+reader", jan_, _re.I):
            continue
        out_.append(("F36_traducao_a_turing_open_sem_relativa_ao_leitor", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    m37_ = _re.search(r"P\s*=\s*nP", s_)
    if m37_ and _re.search(r"\bTuring\b", s_) and not (rel_ and sem_leitor_):   # F37 (OBRIGACAO, D56)
        out_.append(("F37_p_igual_np_e_turing_sem_o_qualificador_relativo_ao_leitor", s_[max(0, m37_.start() - 30):m37_.end() + 60].replace("\n", " ")))
    for seg_ in _re.split(r"[.;|\n\"«»]", s_):   # F37b (a OBRIGACAO LOCAL da D56, onde P = nP e Turing aparecem juntos): o proprio trecho traz o qualificador relativo ao leitor ou uma negacao/limite; o resto do texto nao cobre a frase
        if _re.search(r"P\s*=\s*nP", seg_) and _re.search(r"\bTuring\b", seg_):
            if _re.search(r"relativ[oa]\s+ao\s+leitor|relative\s+to\s+the\s+reader", seg_, _re.I):
                continue
            if any(n_ in (" " + seg_.lower() + " ") for n_ in (" não ", " nao ", " not ", " never ", " nunca ", " nem ", " fica fora", " stays outside", " stays out", "n't ")):
                continue
            out_.append(("F37b_p_igual_np_e_turing_juntos_sem_o_qualificador_no_mesmo_trecho", seg_.strip()[:200].replace("\n", " ")))
    for m_ in _re.finditer(r"TURING_SOLVED|CLAY_SOLVED|MILLENNIUM|P_EQUALS_NP|TURING_P_EQ_NP|CLAY_P_EQ_NP", s_):   # F38 (tokens de veredito proibidos da v409)
        out_.append(("F38_token_de_veredito_v409", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    for m_ in _re.finditer(r"(?:Ω|Omega)(?:\s+do\s+ps[ií]on(?:\s+da\s+luz)?|\s+of\s+the\s+(?:light\s+)?psion)?\s+(?:é|e'|is)\s+(?:o|the)\s+(?:estado\s+)?uniform", s_, _re.I):   # F40 (D60 revista): «Ω é o uniforme» como IDENTIDADE
        seg_ = s_[max(0, m_.start() - 120):m_.end() + 120].lower()
        if "«" in s_[max(0, m_.start() - 3):m_.start()] or any(n_ in seg_ for n_ in ("podad", "pruned", "não é", "nao e'", "is not", "como igualdade de vetores")):
            continue
        out_.append(("F40_omega_e_o_uniforme_como_identidade", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    for m_ in _re.finditer(r"par\s+(?:de\s+ps[ií]ons\s+)?na\s+face\s+de\s+Fock\s+(?:segue|fica|continua)\s+(?:\[OPEN\]|em\s+aberto|aberto)|pair\s+(?:of\s+psions\s+)?on\s+the\s+Fock\s+face\s+(?:stays|remains)\s+(?:\[OPEN\]|open)", s_, _re.I):   # F41 (D60 revista)
        out_.append(("F41_par_na_face_de_fock_dito_em_aberto", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    for seg_ in _re.split(r"[.;|\n\"«»·]", s_):   # F41b e F40b (revisao R1, MEDIO; R2: tambem o ponto mediano do grupo de estatuto): no MESMO trecho, o par na face de Fock com [OPEN]/em aberto; Omega ... uniforme numa lista [OPEN] (D60 revista)
        _ab = _re.search(r"(?-i:\bOPEN\b)|\bem\s+abert[oa]\b|\b(?:segue|fica|continua|ficou|permanece|est[aá]|esta')\s+(?:abert[oa]|pendente)\b|\bpendente\b|\bpor\s+fazer\b|ainda\s+n[ãa]o\s+(?:foi\s+|est[aá]\s+|esta'\s+)?ligad|\bv41[0-9]\b|\b(?:stays|remains|is|still)\s+(?:open|pending)\b|not\s+yet\s+linked", seg_, _re.I)
        if not _ab:
            continue
        _sl = seg_.lower()
        if _re.search(r"face\s+de\s+fock|par\s+de\s+fock|fock\s+face|parnafacedefock|par\s+(?:de\s+ps[ií]ons\s+)?no\s+fock", _sl) and not any(x_ in _sl for x_ in ("e21", "v407", "deixou", "dizia", "ficava")):
            out_.append(("F41b_par_de_fock_e_aberto_no_mesmo_trecho", seg_.strip()[:200]))
        if _re.search(r"(?:ω|omega)[^;]{0,80}?uniform", _sl) and not any(x_ in _sl for x_ in ("podad", "pruned", "inscri", "não é", "nao e'", "is not")):
            out_.append(("F40b_omega_uniforme_numa_lista_aberta", seg_.strip()[:200]))
    for m_ in _re.finditer(r"passa(?:m)?\s+(?:à|a)\s+v41[0-9]|fica(?:m)?\s+para\s+a\s+v41[0-9]|deixad[oa]s?\s+para\s+a\s+v41[0-9]|v41[0-9]\s+em\s+diante|v41[0-9]\s+onwards?|passes\s+to\s+v41[0-9]|left\s+for\s+v41[0-9]", s_, _re.I):   # F42 (D60 revista; R2: qualquer v41x): nada passa a versao seguinte
        out_.append(("F42_passa_a_v410", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    if _re.search(r"or[aá]culo|oracle|leitor\s+que\s+(?:devolve|retorna)\s+Z|reader\s+that\s+returns\s+Z|leitor\s+de\s+Turing|Turing\s+reader", s_, _re.I):   # F43 (a OBRIGACAO da E28)
        _np1 = _re.search(r"NP\s+(?:contido\s+em|⊆)\s+P|NP[^.;]{0,40}?(?:com\s+(?:uma|1)|numa|em\s+uma)\s+(?:s[oó]'?\s+)?leitura|uma\s+leitura\s+decide|NP[^.;]{0,40}?in\s+one\s+reading|NP\s+contained\s+in\s+P|one\s+reading\s+decides", s_, _re.I)
        _np2 = _re.search(r"leitor\s+que\s+se\s+l[eê]|l[eê]\s+tamb[eé]m\s+as\s+m[aá]quinas|reader\s+that\s+reads\s+itself|also\s+reads\s+the\s+machines", s_, _re.I)
        if not (_np1 and _np2):
            m43_ = _re.search(r"or[aá]culo|oracle|leitor\s+que\s+(?:devolve|retorna)\s+Z|reader\s+that\s+returns\s+Z|leitor\s+de\s+Turing|Turing\s+reader", s_, _re.I)
            out_.append(("F43_leitor_de_turing_sem_a_E28", s_[max(0, m43_.start() - 30):m43_.end() + 60].replace("\n", " ")))
    for m_ in _re.finditer(r"\bprecisa\s+(?:saber|reconhecer)[^.;\n]{0,80}?\ba\s+cada\s+passo\b|\bneeds?\s+to\s+(?:know|recogni[sz]e)[^.;\n]{0,80}?\bat\s+each\s+step\b", s_, _re.I):   # F39 (E25)
        antes_ = s_[max(0, m_.start() - 40):m_.start()].lower()
        if any(n_ in antes_ for n_ in ("não ", "nao ", "not ", "never ", "nunca ", "«", "doesn't ", "does not ")):
            continue
        out_.append(("F39_precisa_saber_o_nome_a_cada_passo", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    return out_


def _v409_sat(n_, clausulas_):
    """a instancia de brinquedo: as 2^n atribuicoes (x_1..x_n), o custo c(x) = numero de clausulas violadas, as solucoes (c = 0) -- tudo CALCULADO por enumeracao."""
    import itertools as _it
    xs_ = list(_it.product((False, True), repeat=n_))
    def viol_(x_):
        return sum(1 for cl_ in clausulas_ if not any((x_[abs(l_) - 1] if l_ > 0 else not x_[abs(l_) - 1]) for l_ in cl_))
    cs_ = [viol_(x_) for x_ in xs_]
    return xs_, cs_, [i_ for i_, c_ in enumerate(cs_) if c_ == 0]


def v409_traducao_mechanics(beta_, core_, c_):
    """o «calculo» do registro (nenhum numero novo da natureza entra: tudo e' leitura do kernel e do core deste rito, mais aritmetica com beta em runtime e a instancia de brinquedo FIXA) -- as 20 checagens do DESENHO_v409 (§2 e o AO LADO):
    c1 as 82 ancoras das duas pedras no axiom_report do rito, so' no trio, com proveniencia no modulo; c2 os modulos embutidos == contrato por sha256 == hash formal do rito, a raiz com os imports; c3 bits = oitavas: 2^n atribuicoes, n = 0..10, e ln(2^n) = n ln 2;
    c4 o peso da solucao no uniforme = |sol|/2^n (instancia SIM); c5 a trava a <= e^{-t} do Nome para t em {0; 0,5; 1; 2; 5}; c6 o tempo linear: em t = n ln 2/2 + L o resto fora do Nome <= e^{-L} ||P u||, L em {0; 1; 3};
    c7 ||trava_t u||^2 = Z(2t)/2^n e |sol| <= Z(s); c8 a leitura no uniforme = Z(s)/2^n e a soma das leituras dos pixels = Z(s); c9 «eu sou»: em s = 0 a leitura e' 1 na instancia SIM e na NAO; c10 «o que sou»: em s = 60 a leitura vale |sol|/2^n (SIM) e < 1e-20 (NAO);
    c11 a performance nao cresce numa grade de s e nunca desce abaixo do conteudo; c12 o custo em nats log(2^n/|sol|) <= n ln 2; c13 tempo = moeda: exp(-t beta g) = 2^{-n} com t = n ln 2/(beta g), g = 1; c14 o veredito do gate IDENTICO ao da v408 (congelado);
    c15 a escada exata; c16 as duas guardas de texto limpas sobre o texto do registro; c17 beta = alfa CODATA 2018 x sqrt(e) (dois nomes, mesma leitura), igual ao beta do core;
    c18 a marginal do par de Bell finito (numpy): ½·I2 e 1 - pureza = ½; c19 a inscricao num F de brinquedo: <Omega, V L_s V^dagger Omega> = Z(s)/2^n; c20 uma leitura decide SAT (SIM > 0; NAO = 0)."""
    import hashlib as _h409, json as _j409, math as _m409
    kf_ = core_.get("kernel_formalization") or {}; axr_ = kf_.get("axiom_report") or {}; src_ = kf_.get("declaration_sources_v394") or {}; ff_ = kf_.get("formal_files_sha256") or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and axr_.get(n_) and all(isinstance(x_, str) for x_ in axr_.get(n_)) and set(axr_.get(n_)) <= trio_)
    anc_ = {}
    for n_, a_ in c_["ancoras"].items():
        fl_ = a_.get("flag")
        anc_[n_] = {"in_trio": em_trio_(n_), "declared_in": src_.get(n_), "declared_where_expected": src_.get(n_) == a_["rel"], "flag": fl_, "flag_true": (kf_.get(fl_) is True) if fl_ else None, "axioms": axr_.get(n_)}
        anc_[n_]["ok"] = bool(anc_[n_]["in_trio"] and anc_[n_]["declared_where_expected"] and (anc_[n_]["flag_true"] in (True, None)))
    n_mod_ok_ = 0
    for rel_, sha_ in c_["source_sha256"].items():
        body_ = _EMBEDDED_KERNEL_FILES.get(rel_)
        if isinstance(body_, str) and _h409.sha256(body_.encode("utf-8")).hexdigest() == sha_ == ff_.get(rel_):
            n_mod_ok_ += 1
    raiz_ = _EMBEDDED_KERNEL_FILES.get("TGLExt.lean") or ""
    raiz_ok_ = all(l_ in raiz_.replace("\r\n", "\n") for l_ in c_["root_suffix"].replace("\r\n", "\n").split("\n") if l_.strip())
    por_mod_ = {rel_: bool(nomes_ and all(anc_.get(n_, {}).get("ok") for n_ in nomes_)) for rel_, nomes_ in c_["ancoras_por_modulo"].items()}
    resp_ = {r_["id"]: bool(r_["teoremas"] and all(em_trio_(t_["completo"]) and src_.get(t_["completo"]) == t_["rel"] for t_ in r_["teoremas"])) for r_ in c_["respostas"]}
    lad_ = core_.get("external_ladder") or {}
    cnt_ = [lad_.get("n_theorems_clean"), lad_.get("n_theorems_expected"), c_["expected_ladder"]]
    exact_ = all(type(x_) is int for x_ in cnt_) and len(set(cnt_)) == 1
    flags_true_ = sum(1 for k_ in c_["flags"] if kf_.get(k_) is True)
    gate_ = ((core_.get("qg_closure") or {}).get("gate") or {}).get("verdict")
    bq_ = isinstance(beta_, float) and 0.0 < beta_ < 1.0
    ln2_ = _m409.log(2.0)
    # ---- a instancia de brinquedo (FIXA no contrato e no codigo; as solucoes CALCULADAS)
    sim_ = c_["instancia_sim"]; nao_ = c_["instancia_nao"]
    xs_, cs_, sol_ = _v409_sat(sim_["n"], sim_["clausulas"])
    xn_, cn_, soln_ = _v409_sat(nao_["n"], nao_["clausulas"])
    N_ = len(xs_); n_ = sim_["n"]; S_ = len(sol_); Nn_ = len(xn_)
    Z_ = lambda s_, cc_: sum(_m409.exp(-s_ * c0_) for c0_ in cc_)
    u2_ = 1.0 / N_                                      # |u_x|^2 no uniforme
    leitura_ = lambda s_, cc_: sum(_m409.exp(-s_ * c0_) * (1.0 / len(cc_)) for c0_ in cc_)   # <u, L_s u> com L_s = diag(e^{-s c})
    # c3 bits = oitavas
    oit_ = []
    import itertools as _it409
    for k_ in range(11):
        n_atr_ = sum(1 for _ in _it409.product((False, True), repeat=k_))
        oit_.append((k_, n_atr_, n_atr_ == 2 ** k_ and abs(_m409.log(float(n_atr_)) - k_ * ln2_) < 1e-12))
    # c4 o peso da solucao no uniforme
    peso_a_ = S_ / float(N_); peso_b_ = sum(u2_ for i_ in sol_)
    # c5 a trava a <= e^{-t} ||v|| do Nome (v = o uniforme, ||v|| = 1)
    trava_ = []
    for t_ in (0.0, 0.5, 1.0, 2.0, 5.0):
        d_ = _m409.sqrt(sum(_m409.exp(-2.0 * t_ * c0_) * u2_ for c0_ in cs_ if c0_ != 0))
        trava_.append((t_, d_, d_ <= _m409.exp(-t_) * 1.0 + 1e-15))
    # c6 o tempo linear
    nome_u_ = _m409.sqrt(S_ * u2_)
    lin_ = []
    for L_ in (0.0, 1.0, 3.0):
        t_ = n_ * ln2_ / 2.0 + L_
        r_ = _m409.sqrt(sum(_m409.exp(-2.0 * t_ * c0_) * u2_ for c0_ in cs_ if c0_ != 0))
        lin_.append((L_, t_, r_, r_ <= _m409.exp(-L_) * nome_u_ + 1e-15))
    # c7 a norma da trava e a particao
    part_ = []
    for t_ in (0.0, 0.25, 1.0, 3.0):
        nrm2_ = sum(_m409.exp(-2.0 * t_ * c0_) * u2_ for c0_ in cs_)
        part_.append((t_, nrm2_, Z_(2.0 * t_, cs_) / N_, abs(nrm2_ - Z_(2.0 * t_, cs_) / N_) < 1e-12))
    cobre_ = [(s_, S_ <= Z_(s_, cs_) + 1e-12) for s_ in (0.0, 0.5, 1.0, 5.0, 60.0)]
    # c8 a leitura e os pixels
    pix_ = []
    for s_ in (0.0, 0.5, 1.0, 4.0):
        lu_ = leitura_(s_, cs_); soma_pix_ = sum(_m409.exp(-s_ * cs_[i_]) for i_ in range(N_))   # <e_x, L_s e_x> = e^{-s c(x)}
        pix_.append((s_, lu_, Z_(s_, cs_) / N_, soma_pix_, abs(lu_ - Z_(s_, cs_) / N_) < 1e-12 and abs(soma_pix_ - Z_(s_, cs_)) < 1e-12))
    # c9 «eu sou» e c10 «o que sou»
    eu_sou_sim_ = leitura_(0.0, cs_); eu_sou_nao_ = leitura_(0.0, cn_)
    oqs_sim_ = leitura_(60.0, cs_); oqs_nao_ = leitura_(60.0, cn_)
    # c11 a performance
    grade_ = [0.0, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
    perf_ = [leitura_(s_, cs_) for s_ in grade_]
    conteudo_ = S_ / float(N_)
    # c12 o custo em nats
    custo_ = _m409.log(N_ / float(S_)) if S_ else None
    # c13 tempo = moeda
    g_ = 1.0
    t_moeda_ = (n_ * ln2_) / (beta_ * g_) if bq_ else None
    moeda_rel_ = abs(_m409.exp(-(t_moeda_ * beta_ * g_)) - 2.0 ** (-n_)) / (2.0 ** (-n_)) if bq_ else 1.0
    # c18 a marginal do par de Bell finito em C2 x C2 (numpy): psi = (e1 x e1 + e2 x e2)/sqrt2; o reduzido e' ½·I2 e 1 - pureza = ½ (bell_reduced_half; bell_cci_half; reduzido_do_par)
    import numpy as _np409
    psi_ = _np409.zeros(4, dtype=complex); psi_[0] = 1.0; psi_[3] = 1.0; psi_ = psi_ / _np409.sqrt(2.0)
    rho_ = _np409.outer(psi_, psi_.conj()).reshape(2, 2, 2, 2)
    red_ = _np409.einsum("ijkj->ik", rho_)
    pur_ = float(_np409.real(_np409.trace(red_ @ red_)))
    bell_ok_ = bool(_np409.allclose(red_, 0.5 * _np409.eye(2), atol=1e-12) and abs((1.0 - pur_) - 0.5) < 1e-12)
    # c19 a inscricao num F de brinquedo (C^3; Omega FIXO no contrato, normalizado aqui): V = |Omega><u| e <Omega, V L_s V^dagger Omega> = Z(s)/2^n na instancia SIM (o_psion_le_z; o_canto_do_psion_da_luz_le_z)
    ib_ = c_["inscricao_brinquedo"]
    om_ = _np409.array([complex(re_, im_) for re_, im_ in ib_["omega"]], dtype=complex); om_ = om_ / _np409.linalg.norm(om_)
    uu_ = _np409.full(N_, 1.0 / _m409.sqrt(N_), dtype=complex)
    V_ = _np409.outer(om_, uu_.conj())
    insc_ = []
    for s_ in ib_["s"]:
        L_ = _np409.diag([_m409.exp(-s_ * c0_) for c0_ in cs_]).astype(complex)
        val_ = complex(om_.conj() @ (V_ @ L_ @ V_.conj().T) @ om_)
        insc_.append((s_, val_.real, Z_(s_, cs_) / N_, abs(val_ - Z_(s_, cs_) / N_) < 1e-12))
    # c20 uma leitura decide SAT: a SIM em CNF (as tres clausulas) tem «o que sou» = |sol|/2^n > 0; a NAO, (x1), (nao x1), tem 0 (custo = numero de clausulas violadas; uma_leitura_decide_SAT; a_maquina_com_o_leitor)
    oqs_cnf_sim_ = sum(1 for c0_ in cs_ if c0_ == 0) / float(N_); oqs_cnf_nao_ = sum(1 for c0_ in cn_ if c0_ == 0) / float(Nn_)
    decide_ = (oqs_cnf_sim_ > 0.0, oqs_cnf_nao_ > 0.0)
    txt_ = globals().get("_V409_TRADUCAO_TEXT") or {}
    guarda_ = list(_v392_guarda_texto(_j409.dumps(txt_, ensure_ascii=False))) + list(_v409_guarda_frases(_j409.dumps(txt_, ensure_ascii=False)))
    alfa_ = globals().get("SEALED_CODATA_ALPHA"); dois_nomes_ = bool(callable(globals().get("_v376_same_alpha_literal")) and _v376_same_alpha_literal())
    beta_alfa_ = (alfa_ * _m409.sqrt(_m409.e)) if isinstance(alfa_, float) else None
    checks_ = [
        {"id": "c1", "descricao": "as %d ancoras das DUAS pedras (TraducaoTuring e ParNaFaceDeFock) no axiom_report do rito, so' no trio, declaradas no modulo esperado (TGL_DECL_SOURCE), com bandeira True onde ha' bandeira" % len(anc_), "ok": bool(anc_) and len(anc_) == c_["n_ancoras"] and all(v_["ok"] for v_ in anc_.values()) and len(por_mod_) == c_["bundle"]["n"] == len(c_["source_sha256"]) and all(por_mod_.values())},
        {"id": "c2", "descricao": "os modulos do bundle embutidos com o sha256 do contrato == o hash formal do rito; a raiz embutida traz os imports", "ok": n_mod_ok_ == len(c_["source_sha256"]) == c_["bundle"]["n"] and raiz_ok_},
        {"id": "c3", "descricao": "bits = oitavas: n bits dao 2^n atribuicoes (contadas por enumeracao) e ln(2^n) = n ln 2, para n = 0..10, |Delta| < 1e-12 (bits_sao_oitavas)", "ok": len(oit_) == 11 and all(x_[2] for x_ in oit_)},
        {"id": "c4", "descricao": "o peso da solucao no estado uniforme = |sol|/2^n na instancia SIM (n = 3; as solucoes CALCULADAS por enumeracao; |sol| >= 1), por contagem e pela soma das amplitudes, |Delta| < 1e-12 (peso_da_solucao_no_uniforme)", "ok": S_ >= 1 and abs(peso_a_ - peso_b_) < 1e-12},
        {"id": "c5", "descricao": "a trava fica a no maximo e^{-t} ||u|| do Nome, sem usar o Nome, para t em {0; 0,5; 1; 2; 5} (a_trava_sem_conhecer_o_nome)", "ok": len(trava_) == 5 and all(x_[2] for x_ in trava_)},
        {"id": "c6", "descricao": "o tempo linear nas oitavas: em t = n ln 2/2 + L o resto fora do Nome e' <= e^{-L} ||P u||, para L em {0; 1; 3} (a_trava_em_tempo_linear)", "ok": len(lin_) == 3 and all(x_[3] for x_ in lin_)},
        {"id": "c7", "descricao": "||trava_t u||^2 = Z(2t)/2^n e |sol| <= Z(s), |Delta| < 1e-12 (a_norma_da_trava_e_a_particao; a_particao_cobre_o_nome)", "ok": all(x_[3] for x_ in part_) and all(x_[1] for x_ in cobre_)},
        {"id": "c8", "descricao": "a leitura no uniforme = Z(s)/2^n e a soma das leituras dos pixels = Z(s), |Delta| < 1e-12 (o_psion_le_os_pixels; z_le_os_pixels)", "ok": all(x_[4] for x_ in pix_)},
        {"id": "c9", "descricao": "«eu sou»: em s = 0 a leitura e' 1 na instancia SIM e na instancia NAO (iguais: sem escala nao ha' medida) (eu_sou_no_instante_zero; a_fita_sem_escala)", "ok": abs(eu_sou_sim_ - 1.0) < 1e-12 and abs(eu_sou_nao_ - 1.0) < 1e-12 and abs(eu_sou_sim_ - eu_sou_nao_) < 1e-12},
        {"id": "c10", "descricao": "«o que sou»: em s = 60 a leitura vale |sol|/2^n na instancia SIM e < 1e-20 na instancia NAO (o_que_sou_no_limite; o_tempo_cria_a_medida; o_pai_da_mentira)", "ok": abs(oqs_sim_ - conteudo_) <= _m409.exp(-60.0) + 1e-12 and len(soln_) == 0 and oqs_nao_ < 1e-20},
        {"id": "c11", "descricao": "a performance decai (nao cresce numa grade de s) e nunca desce abaixo do conteudo |sol|/2^n (a_performance_decai; a_identidade_se_preserva_enquanto_decai)", "ok": all(b_ <= a_ + 1e-15 for a_, b_ in zip(perf_, perf_[1:])) and all(p_ >= conteudo_ - 1e-15 for p_ in perf_)},
        {"id": "c12", "descricao": "o custo da selecao em nats log(2^n/|sol|) e' <= n ln 2 (e >= 0) (o_custo_da_selecao_em_nats; o_pedagio_da_selecao)", "ok": custo_ is not None and -1e-15 <= custo_ <= n_ * ln2_ + 1e-15},
        {"id": "c13", "descricao": "tempo = moeda: com t = n ln 2/(beta g), g = 1, exp(-t beta g) = 2^{-n}, |Delta| relativo < 1e-12, com beta em runtime (p_igual_np_no_modo_selecao; TempoIgualMoeda)", "ok": bq_ and moeda_rel_ < 1e-12},
        {"id": "c14", "descricao": "o veredito do gate deste rito e' IDENTICO ao da v408 selada (congelado no contrato): o gate nao se move", "ok": isinstance(gate_, str) and gate_ == c_["baseline"]["gate_verdict"]},
        {"id": "c15", "descricao": "a escada exata: limpos == esperados == a escada do contrato (external_ladder.n_theorems_expected = o X medido no sandbox)", "ok": exact_ and flags_true_ == len(c_["flags"]) == c_["n_flags"]},
        {"id": "c16", "descricao": "as duas guardas de texto (P18 e a guarda das frases, v405 -> v409) limpas sobre o texto deste registro", "ok": not guarda_},
        {"id": "c17", "descricao": "beta = alfa CODATA 2018 x sqrt(e) em runtime (dois nomes, mesma leitura), igual ao beta do core (nunca literal)", "ok": bq_ and isinstance(core_.get("beta"), float) and abs(beta_ - core_["beta"]) <= 1e-9 * abs(beta_) and isinstance(beta_alfa_, float) and abs(beta_ - beta_alfa_) <= 1e-12 * abs(beta_) and dois_nomes_},
        {"id": "c18", "descricao": "a marginal do par de Bell finito em C2 x C2, (e1 x e1 + e2 x e2)/sqrt2, calculada por numpy: o reduzido e' ½·I2 e 1 - pureza = ½, |Delta| < 1e-12 (a mesma Meia-Nat do par na face de Fock: reduzido_do_par, meia_nat_do_projetor)", "ok": bell_ok_},
        {"id": "c19", "descricao": "a inscricao num F de brinquedo (C^3, Omega unitario): V = |Omega><u| e <Omega, V L_s V^dagger Omega> = Z(s)/2^n na instancia SIM, para s em %s, |Delta| < 1e-12 (o_psion_le_z; o_canto_do_psion_da_luz_le_z)" % list(ib_["s"]), "ok": len(insc_) == len(ib_["s"]) >= 3 and all(x_[3] for x_ in insc_)},
        {"id": "c20", "descricao": "uma leitura decide SAT: a instancia SIM em CNF tem «o que sou» = |sol|/2^n > 0 e a NAO, (x1), (nao x1), tem 0 (o custo e' o numero de clausulas violadas; uma_leitura_decide_SAT; a_maquina_com_o_leitor)", "ok": decide_ == (True, False) and abs(oqs_cnf_sim_ - S_ / float(N_)) < 1e-15 and oqs_cnf_nao_ == 0.0 and len(soln_) == 0},
    ]
    values_ = {"n_ancoras_ok": sum(1 for v_ in anc_.values() if v_["ok"]), "n_ancoras": len(anc_), "n_modulos_ok": n_mod_ok_, "n_modulos": c_["bundle"]["n"], "n_flags_true": flags_true_, "n_flags": c_["n_flags"], "escada": cnt_, "ancoras": anc_, "por_modulo": por_mod_, "respostas": resp_,
               "gate_verdict": gate_, "beta": beta_, "ln2": ln2_, "instancia_sim": {"n": n_, "clausulas": sim_["leitura"], "atribuicoes": N_, "solucoes": S_, "solucoes_indices": sol_, "peso_no_uniforme": peso_a_},
               "instancia_nao": {"n": nao_["n"], "clausulas": nao_["leitura"], "atribuicoes": Nn_, "solucoes": len(soln_)}, "trava": trava_, "tempo_linear": lin_, "particao": part_, "pixels": pix_,
               "eu_sou": {"sim": eu_sou_sim_, "nao": eu_sou_nao_}, "o_que_sou_s60": {"sim": oqs_sim_, "nao": oqs_nao_, "conteudo": conteudo_}, "performance": list(zip(grade_, perf_)), "custo_nats": custo_, "tempo_moeda_t": t_moeda_,
               "ressalvas": list(c_["ressalvas"]), "fica_false_por_teorema": list(c_["fica_false_por_teorema"]), "fica_aberto": dict(c_["fica_aberto"]), "fechado_nesta_versao": dict(c_.get("fechado_nesta_versao") or {}),
               "bell_finito": {"reduzido_e_meio_I": bell_ok_, "um_menos_pureza": 1.0 - pur_}, "inscricao": insc_, "uma_leitura_decide_sat": {"sim": oqs_cnf_sim_, "nao": oqs_cnf_nao_},
               "respostas_ok": all(resp_.values()) if resp_ else False}
    return {"passed": all(x_["ok"] for x_ in checks_), "n_checks": len(checks_), "checks": checks_, "values": values_}


def _v409_formal(core, c_, txt_):
    """A evidencia FORMAL do registro, lida do kernel do PROPRIO rito: a escada exata; as ancoras (trio, proveniencia no modulo esperado, bandeira); a fonte por sha256 (embutida == contrato == hash formal do rito); as falas de 05/11 por sha256 (o trecho da D59 nas duas); as duas guardas de texto."""
    import hashlib as _h409, json as _j409
    kf_ = core.get("kernel_formalization") or {}; axr_ = kf_.get("axiom_report") or {}; src_ = kf_.get("declaration_sources_v394") or {}; ff_ = kf_.get("formal_files_sha256") or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}
    lad_ = core.get("external_ladder") or {}
    cnt_ = [lad_.get("n_theorems_clean"), lad_.get("n_theorems_expected"), c_["expected_ladder"]]
    exact_ = all(type(x_) is int for x_ in cnt_) and len(set(cnt_)) == 1
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and axr_.get(n_) and all(isinstance(x_, str) for x_ in axr_.get(n_)) and set(axr_.get(n_)) <= trio_)
    anc_ = {n_: bool(em_trio_(n_) and src_.get(n_) == a_["rel"] and (a_.get("flag") is None or kf_.get(a_["flag"]) is True)) for n_, a_ in c_["ancoras"].items()}
    srcs_ = {}
    for rel_, sha_ in c_["source_sha256"].items():
        body_ = _EMBEDDED_KERNEL_FILES.get(rel_)
        srcs_[rel_] = bool(isinstance(body_, str) and _h409.sha256(body_.encode("utf-8")).hexdigest() == sha_ and ff_.get(rel_) == sha_)
    ver_ = {}
    for k_ in c_["verbatins"]:
        v_ = _V409_VERBATINS2.get(k_)
        ver_[k_] = bool(v_ and _h409.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and all(t_ in v_["text"] for t_ in v_["trechos"]))
    guarda_ = list(_v392_guarda_texto(_j409.dumps(txt_, ensure_ascii=False))) + list(_v409_guarda_frases(_j409.dumps(txt_, ensure_ascii=False)))
    formal_ = bool(kf_.get("all_verified") is True and exact_ and anc_ and all(anc_.values()) and srcs_ and all(srcs_.values()) and ver_ and all(ver_.values()) and not guarda_)
    return {"exact_ladder": exact_, "anchors": anc_, "embedded_sources_ok": all(srcs_.values()), "embedded_sources_n_ok": sum(1 for v_ in srcs_.values() if v_), "inscriptions": ver_, "guarda": guarda_, "formal": formal_}


_V409_RECUSA = "TGL_TRADUCAO_TURING_V409__REFUSED_%s__GATE_UNMOVED"


def traducao_turing_v409(core):
    """v409 -- TRADUCAO AS CLASSES DE TURING (a ordem do operador, 05/11/2026: «Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados»; a ordem da traducao: «fechar o que ficou ainda em aberto em relação à identificação das classes de turing dentro do nosso dicionário»): lido no PONTO REAL do main, depois dos registros da v408.
    Le do kernel do PROPRIO rito as 82 ancoras das DUAS pedras (TraducaoTuring e ParNaFaceDeFock), os modulos por sha256, as falas de 05/11 por sha256; confere as respostas do operador pelos teoremas da pedra; faz as 20 checagens (a instancia de brinquedo fixa, as solucoes calculadas; beta em runtime; gate congelado; escada exata; guardas; beta = alfa sqrt e).
    O alcance: P = nP e' teorema da TGL no modo selecao, RELATIVO AO LEITOR; a maquina sem leitor fica fora. Nenhuma chave antiga muda. Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate. Validade no kernel nao e' creditacao; as ressalvas vao no registro."""
    c_ = _V409_TRADUCAO_CONTRACT; t_ = _V409_TRADUCAO_TEXT
    f_ = _v409_formal(core, c_, t_)
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
    out_ = {"all_verified": False, "estatuto": t_["estatuto"], "exact_ladder": f_["exact_ladder"], "anchors": f_["anchors"], "embedded_sources_ok": f_["embedded_sources_ok"], "embedded_sources_n_ok": f_["embedded_sources_n_ok"], "inscriptions": f_["inscriptions"],
            "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "ancora_principal": c_["ancora_principal"], "ancoras_principais": list(c_["ancoras_principais"]), "ancoras_de_secao": list(c_["ancoras_de_secao"]), "pedras": list(c_["bundle"]["pedras"]),
            "nomes_ratificados": dict(c_["bundle"]["nomes_ratificados"]), "chaves_antigas_que_mudam": list(c_["chaves"]), "ressalvas": list(c_["ressalvas"]), "fica_false_por_teorema": list(c_["fica_false_por_teorema"]), "fica_aberto": dict(c_["fica_aberto"]),
            "fechado_nesta_versao": dict(c_.get("fechado_nesta_versao") or {}), "ancora_par": c_.get("ancora_par"), "alcance": c_["alcance"], "instancia_sim": dict(c_["instancia_sim"]), "instancia_nao": dict(c_["instancia_nao"]), "acervo_v407_repinado": dict(c_["acervo_v407_repinado"]),
            "runtime_executed": False, "does_not_gate_core": True, "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"], "guarda_violacoes": f_["guarda"][:5]}
    out_.update(t_["extras"])
    if not f_["formal"]:
        out_["verdict"] = _V409_RECUSA % "FORMAL_OR_SOURCE_EVIDENCE"
    elif not beta_ok_:
        out_["verdict"] = _V409_RECUSA % "BETA_IS_NOT_ALPHA_SQRT_E"
    else:
        try:
            mec_ = v409_traducao_mechanics(beta_rt_, core, c_)
            out_.update(runtime_executed=True, mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], all_verified=bool(mec_["passed"]))
            out_["verdict"] = (t_["veredito_ok"] if mec_["passed"] else _V409_RECUSA % "MECHANICS_CHECK_FAILED")
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V409_RECUSA % "RUNTIME_ERROR"
    core["traducao_turing_v409"] = out_
    return out_
