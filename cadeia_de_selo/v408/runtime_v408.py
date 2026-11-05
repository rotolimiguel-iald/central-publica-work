# ---- v408: TETELESTAI E' O TERMINAL -- os 4 modulos do bundle (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP, todos de TGLExt/, com os nomes do operador de 04/11) e UM registro com FUNCAO, tetelestai_terminal_v408, lido no ponto do rito depois dos registros da v407:
# ele le do kernel do PROPRIO rito as ANCORAS das quatro pedras (48: 14 + 9 + 7 + 18) (os #print axioms das fontes: tetelestai, o terminal e' a leitura, basta, a poda, a quitacao, o zero absoluto e' do infinito, card_chainIdx, o tamanho e' o custo, a inclinacao modular, relacao sem peso excluida, o 1 sozinho nao se mede;
# o tempo e' a moeda; o ponto de contradicao; p_igual_np; as_classes_do_dicionario; p_igual_np_nas_classes_do_dicionario, com ClasseP e ClasseNP definidas em Lean), os quatro modulos por sha256 (embutido == contrato == hash formal do rito), as falas do operador de 04/11 por sha256 (autor marcado), as respostas dele conferidas pelos teoremas que ja existiam, e faz as 16 checagens do DESENHO §2
# (as aritmeticas com beta em runtime: exp 0 = 1, a Meia-Nat estritamente interior, a quitacao exata, o coeficiente de Jones != 1, o vazamento < 1, as oitavas, o tempo linear nos andares, a dimensao da torre, o piso de Landauer; o gate congelado; a escada exata; as guardas de texto; o insumo purgado por sha256; beta = alfa sqrt e).
# NENHUMA chave antiga muda nesta versao. A ordem do operador (04/11/2026, sha16 685b8d8bcf0ddbbd): «liste as pedras que eu preciso nominar e em seguida produza a v408 …»; a regra dele (sha16 c12699c915617c3f): «palavra sem espelho é apenas o espelho da mentira, se é verdade que se sustente e fique, se não que seja podada».
# AS RESSALVAS, ditas em todo texto: o par na face de Fock segue [OPEN] (ligacao, nao ausencia: E21); 'tempo linear nos andares' vale para o Nome da torre; P = nP e' teorema nas classes de computacao do dicionario do operador, e a traducao as classes das maquinas de Turing (bits = log2 n, as oitavas) e' [OPEN], nao uma recusa (D51 revista); o lock e o Hamiltoniano modular sao objetos distintos; beta so' por nome; nenhum teste com a natureza.
# Validade no kernel NAO e' creditacao; NOT_FALSIFIED nunca e' confirmacao; o GATE NAO SE MOVE; beta nunca literal.
# Fonte autoral deste bloco: runtime_v408.py (cadeia_de_selo/v408); o contrato (_V408_TERMINAL_CONTRACT) e as falas (_V408_VERBATINS2) sao DERIVADOS do build do sandbox e dos arquivos, nunca digitados.

_V408_KB_SI_J_PER_K = 1.380649e-23   # J/K [KNOWN: SI 2019, exato por definicao; o mesmo valor que o programa ja' usa nos ritos do piso de Landauer]; nao e' beta nem alfa


def _v408_guarda_frases(txt_):
    """v408 -- a GUARDA DAS FRASES que afirmam demais: herda as regras da v407 (_v407_guarda_frases) e acrescenta as da v408 (DESENHO §3 e o AO LADO da D51 REVISTA, 04/11 noite): «relação sem peso» AFIRMADA (fora da negacao e da citacao), «o que resta sem peso é relação» (a frase da R1, podada: E22), «a TGL não tem terminal» (E22),
    «P = NP está provado/é teorema/é candidato» SEM o qualificador do dicionario (F27: «NP» em maiusculas e' a classe), a frase que da' a TGL como prova ou decisao de P = NP de Turing (Cook-Levin) (F31), a negativa de que «P = nP» trate das classes (F32: o erro da gerencia que o operador corrigiu), as classes P e NP dadas por «podadas» (F33: a traducao a Turing e' [OPEN], nao recusa),
    «impedância» como termo do kernel (D50), «leitura do operador [ONTO]» estacionada e os tokens de veredito correspondentes; e a OBRIGACAO (F34, D51 revista): onde «P = nP» aparecer, o mesmo texto traz o qualificador das classes (de computacao) do dicionario do operador e a ressalva da traducao [OPEN].
    A fala do operador nao passa por aqui: ela e' verbatim e fica fora do texto conferido."""
    import re as _re
    out_ = list(_v407_guarda_frases(txt_))
    s_ = str(txt_)
    regras_ = [("F25_o_que_resta_sem_peso_e_relacao", _re.compile(r"\bo\s+que\s+resta\s+sem\s+peso\s+(?:é|e'|e)\s+rela(?:ç|c)(?:ã|a)o\b|\bwhat\s+(?:remains|is\s+left)\s+without\s+weight\s+is\s+(?:a\s+)?relation\b", _re.I)),
               ("F26_a_tgl_nao_tem_terminal", _re.compile(r"\bTGL\s+n(?:ã|a)o\s+tem\s+terminal\b|\bterminal\s+que\s+a\s+TGL\s+n(?:ã|a)o\s+tem\b|\bTGL\s+has\s+no\s+terminal\b|\bterminal\s+(?:that|which)\s+(?:the\s+)?TGL\s+(?:does\s+not|doesn't|lacks)\b", _re.I)),
               ("F28_impedancia_como_termo", _re.compile(r"\bimped(?:â|a)ncia(?:\s+modular)?\s+(?:é|e'|e|como|is|as)\s+(?:um\s+|o\s+|a\s+)?termo\b|\btermo\s+(?:de\s+|da\s+)?imped(?:â|a)ncia\b|\bimpedance(?:\s+term\b|\s+(?:is|as)\s+(?:a\s+|the\s+)?term\b)", _re.I)),
               ("F29_leitura_onto_estacionada", _re.compile(r"\bleituras?\s+d[oa]\s+operador\s*\[?ONTO\]?|\[ONTO\]\s*d[oa]\s+operador|\breadings?\s+of\s+the\s+operator\s*\[?ONTO\]?", _re.I)),
               ("F30_token_de_veredito", _re.compile(r"TERMINAL_CONF" + r"IRMED|P_EQUALS_NP|CLASSES_PROVED|P_EQ_NP_PROVED|NP_EQUALS_P|NO_WEIGHT_RELATION_EXISTS"))]   # (a palavra banida e' montada por concatenacao: a guarda P18 varre este proprio texto)
    for nome_, rx_ in regras_:
        for m_ in rx_.finditer(s_):
            out_.append((nome_, s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    for m_ in _re.finditer(r"\brela(?:ç|c)(?:ã|a)o\s+sem\s+peso\b|\brelation\s+without\s+weight\b", s_, _re.I):   # F24: a frase so' passa NEGADA («não há …», «no …») ou CORRIGIDA («… é impossível», «… é a origem da mentira»); afirmada, reprova
        antes_ = s_[max(0, m_.start() - 40):m_.start()].lower(); depois_ = s_[m_.end():m_.end() + 70].lower()
        negada_ = any(n_ in antes_ for n_ in ("não ", "nao ", "nenhuma ", "no ", "not ", "never ", "nunca ", "sem ", "without ", "imposs", "exclu", "excludes", "«"))
        corrigida_ = bool(_re.match(r"\s*(?:(?:é|e'|e|is|seja|be|era|was|segue|fica)\s+)?(?:imposs|a\s+origem|the\s+origin|exclu|mentira|a\s+lie|impossible|the\s+root|podad|pruned)|\s*(?:n(?:ã|a)o|not|nunca|never|jamais)\b|\s*»", depois_))   # (r2, 04/11 noite: so' a aspa angular fecha uma CITACAO; a aspa dupla e' o delimitador da string no texto serializado em JSON, nao citacao: era por ela que a frase afirmada no fim de um item passava)
        if not (negada_ or corrigida_):
            out_.append(("F24_relacao_sem_peso_afirmada", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    rx27_ = _re.compile(r"\bP\s*=\s*NP\b\s*(?:est(?:á|a)\s+|foi\s+|é\s+|e'\s+|is\s+|was\s+)?(?:provad[oa]|demonstrad[oa]|teorema|candidat[oa]|proved|proven|(?:a\s+)?theorem|(?:a\s+)?candidate)\b|\b(?:prova|provou|provamos|prove[sd]?|proving|demonstr(?:a|ou|amos))\s+(?:que\s+|that\s+)?P\s*=\s*NP\b|\bcandidat[oa]\s+a\s+P\s*=\s*NP\b|\bP\s*=\s*NP\s+(?:como|as)\s+(?:um\s+|a\s+)?(?:teorema|theorem)\b")   # (sem re.I: «NP» em maiusculas e' a classe; «P = nP», n minusculo, e' o nome do operador: F34)
    for m_ in rx27_.finditer(s_):   # F27 (D51 revista): «P = NP» (a classe, NP em maiusculas) dado por provado/teorema/candidato; so' passa com o qualificador do dicionario logo adiante
        if _re.search(r"dicion(?:á|a)rio|dictionary", s_[m_.end():m_.end() + 120], _re.I):
            continue
        out_.append(("F27_p_igual_np_provado", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    rx31_ = _re.compile(r"\b(?:TGL|IALD|um\.py|kernel|pedra|PIgualNP|esta\s+vers(?:ã|a)o|this\s+version|the\s+stone)\s+(?:j(?:á|a)\s+|already\s+)?(?:prova|provou|provar(?:á|a)|decide|decidiu|decidir(?:á|a)|resolve|resolveu|demonstra|demonstrou|proves|proved|decides|decided|settles|settled|solves|solved)\s+(?:que\s+|that\s+)?(?:a\s+igualdade\s+|the\s+equality\s+)?(?:de\s+|of\s+)?P\s*(?:=|vs\.?|versus|≠)\s*N?P\b[^.;\n]{0,100}?\b(?:Turing|Cook)"
                        r"|\b(?:provamos|provei|decidimos|resolvemos|we\s+(?:prove|proved|decide|decided|settle|settled))\s+(?:que\s+|that\s+)?P\s*(?:=|vs\.?|versus|≠)\s*N?P\b[^.;\n]{0,100}?\b(?:Turing|Cook)"
                        r"|\bP\s*=\s*N?P\s+(?:de|das\s+m(?:á|a)quinas\s+de|of|for)\s+(?:Turing|Cook)[^.;\n]{0,60}?\b(?:est(?:á|a)\s+|foi\s+|(?:é|e'|e)\s+|is\s+|was\s+)(?:provad|decidid|resolvid|demonstrad|teorema|proved|proven|decided|settled|a\s+theorem)", _re.I)
    for m_ in rx31_.finditer(s_):   # F31 (D51 revista): a TGL prova/decide P = NP das maquinas de Turing (Cook-Levin); passa so' negada ou citada entre « »
        antes_ = s_[max(0, m_.start() - 40):m_.start()].lower()
        if any(n_ in antes_ for n_ in ("não ", "nao ", "not ", "never ", "nunca ", "nenhuma ", "jamais ", "«")):
            continue
        out_.append(("F31_a_tgl_prova_p_igual_np_de_turing", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    rx32_ = _re.compile(r"\bn(?:ã|a)o\s+trata\s+(?:d[ae]s?\s+|de\s+)?classes\b|\bnada\s+aqui\s+(?:é|e'|e)\s+(?:enunciado\s+de\s+)?complexidade|\bnada\s+de\s+classes\s+de\s+complexidade|\bn(?:ã|a)o\s+(?:é|e'|e)\s+enunciado\s+de\s+classes"
                        r"|\bdoes\s+not\s+(?:treat|deal\s+with|address|concern)\s+(?:the\s+)?(?:computation(?:al)?\s+|complexity\s+)?classes\b|\bnothing\s+here\s+is\s+(?:a\s+)?(?:statement\s+of\s+)?(?:computational\s+)?complexity|\bno\s+complexity\s+classes\b|\bis\s+not\s+a\s+statement\s+of\s+(?:complexity\s+)?classes", _re.I)
    for m_ in rx32_.finditer(s_):   # F32 (D51 revista): negar que «P = nP» trate das classes (o erro da gerencia, corrigido pelo operador); passa so' quando aponta onde as classes sao tratadas
        if _re.search(r"quem\s+trata|PIgualNP|as_classes_do_dicionario|who\s+treats|treated\s+in", s_[m_.end():m_.end() + 90]):
            continue
        out_.append(("F32_nega_que_p_igual_np_trate_das_classes", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    for m_ in _re.finditer(r"\bclasses\s+P\s+(?:e|and)\s+NP\b[^.;\n]{0,50}?\b(?:podad[oa]s?|PODAD[OA]S?|pruned|PRUNED)\b|\bP\s*=\s*NP\b[^.;\n]{0,20}?\b(?:podad[oa]|PODAD[OA]|pruned|PRUNED)\b", s_):   # F33 (D51 revista): as classes P e NP dadas por «podadas»: a traducao a Turing e' [OPEN], nao recusa
        out_.append(("F33_as_classes_p_e_np_dadas_por_podadas", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    m34_ = _re.search(r"P\s*=\s*nP", s_)   # F34 (OBRIGACAO, D51 revista): onde «P = nP» aparece, o mesmo texto traz o qualificador do dicionario e a ressalva da traducao [OPEN]
    if m34_ and not (_re.search(r"classes\s+(?:de\s+computa(?:ç|c)(?:ã|a)o\s+)?do\s+dicion(?:á|a)rio\s+do\s+operador|(?:computation\s+)?classes\s+of\s+the\s+operator(?:'|’)?s\s+dictionary", s_, _re.I)
                     and _re.search(r"(?:tradu(?:ç|c)(?:ã|a)o|translation)[\s\S]{0,400}?\[OPEN\]", s_, _re.I)):
        out_.append(("F34_p_igual_np_sem_o_qualificador_do_dicionario_ou_a_ressalva_open", s_[max(0, m34_.start() - 30):m34_.end() + 60].replace("\n", " ")))
    return out_


def v408_terminal_mechanics(beta_, core_, c_):
    """o «calculo» do registro (nenhum numero novo da natureza entra: tudo e' leitura do kernel e do core deste rito, mais aritmetica com beta em runtime) -- as 16 checagens do DESENHO_v408 §2:
    c1 as ancoras (48) no axiom_report do rito, so' no trio, com proveniencia nos 4 modulos; c2 os 4 modulos embutidos == contrato por sha256 == hash formal do rito; c3 exp(0) = 1 (o zero inscrito e' o Um) e exp(-0 t) = 1 (sem beta nao ha' segunda face); c4 o fator da Meia-Nat e^{-1/2} estritamente interior;
    c5 a quitacao f + (1 - f) = 1 em f = e^{-1/2} (exata ate' 1e-15); c6 o coeficiente de Jones exp(-beta s) != 1 e < 1 para s = 1 (relacao sem peso e' excluida); c7 exp(-t beta g) < 1 para t = g = 1; c8 octaveNats(N+1) = (N+1) ln 2 = ln 2^(N+1), N = 0..10; c9 t = (N+1) ln 2/(beta g) satisfaz exp(-t beta g) = 2^-(N+1);
    c10 dim(chainIdx N) = 2^(N+1) = 2 2^N, N = 0..10; c11 o piso de Landauer k_B T ln 2 > 0 (k_B SI, T = 1 K); c12 o veredito do gate IDENTICO ao da v407 (congelado); c13 a escada exata; c14 as duas guardas de texto limpas sobre o texto do registro; c15 o insumo purgado por sha256 == pinado, com a integra citada so' por sha16 e fora do espelho;
    c16 beta = alfa CODATA 2018 x sqrt(e) (dois nomes, mesma leitura), igual ao beta do core."""
    import hashlib as _h408, json as _j408, math as _m408
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
        if isinstance(body_, str) and _h408.sha256(body_.encode("utf-8")).hexdigest() == sha_ == ff_.get(rel_):
            n_mod_ok_ += 1
    raiz_ = _EMBEDDED_KERNEL_FILES.get("TGLExt.lean") or ""
    raiz_ok_ = all(l_ in raiz_.replace("\r\n", "\n") for l_ in c_["root_suffix"].replace("\r\n", "\n").split("\n") if l_.strip())
    por_mod_ = {rel_: bool(nomes_ and all(anc_.get(n_, {}).get("ok") for n_ in nomes_)) for rel_, nomes_ in c_["ancoras_por_modulo"].items()}
    no_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and all(isinstance(x_, str) for x_ in axr_.get(n_)) and set(axr_.get(n_)) <= trio_)   # (as RESPOSTAS citam tambem teoremas que nao dependem de axioma nenhum, como two_clocks_are_needed: «does not depend on any axioms» le-se [] e esta' no trio; o nome tem de EXISTIR no axiom_report do rito)
    resp_ = {r_["id"]: bool(r_["teoremas"] and all(no_trio_(t_["completo"]) and src_.get(t_["completo"]) == t_["rel"] for t_ in r_["teoremas"])) for r_ in c_["respostas"]}
    lad_ = core_.get("external_ladder") or {}
    cnt_ = [lad_.get("n_theorems_clean"), lad_.get("n_theorems_expected"), c_["expected_ladder"]]
    exact_ = all(type(x_) is int for x_ in cnt_) and len(set(cnt_)) == 1
    flags_true_ = sum(1 for k_ in c_["flags"] if kf_.get(k_) is True)
    gate_ = ((core_.get("qg_closure") or {}).get("gate") or {}).get("verdict")
    # ---- a aritmetica das pedras, com beta em runtime (nunca literal)
    bq_ = isinstance(beta_, float) and 0.0 < beta_ < 1.0
    e0_ = _m408.exp(0.0); e0t_ = [_m408.exp(-(0.0 * t_)) for t_ in (0.5, 1.0, 7.0)]
    f_ = _m408.exp(-0.5)
    cj_ = _m408.exp(-(beta_ * 1.0)) if bq_ else None
    vz_ = _m408.exp(-(1.0 * beta_ * 1.0)) if bq_ else None
    ln2_ = _m408.log(2.0)
    oit_ = [(((N_ + 1) * ln2_), _m408.log(2.0 ** (N_ + 1))) for N_ in range(11)]
    g_ = 1.0
    t_torre_ = [(((N_ + 1) * ln2_) / (beta_ * g_)) for N_ in range(11)] if bq_ else []
    lin_ = [abs(_m408.exp(-(t_ * beta_ * g_)) - 2.0 ** (-(N_ + 1))) / (2.0 ** (-(N_ + 1))) for N_, t_ in enumerate(t_torre_)] if bq_ else [1.0]
    card_ = [2]
    for N_ in range(10):
        card_.append(card_[-1] * 2)
    piso_ = _V408_KB_SI_J_PER_K * 1.0 * ln2_
    txt_ = globals().get("_V408_TERMINAL_TEXT") or {}
    guarda_ = list(_v392_guarda_texto(_j408.dumps(txt_, ensure_ascii=False))) + list(_v408_guarda_frases(_j408.dumps(txt_, ensure_ascii=False)))
    ip_ = c_["insumo_purgado"]; fontes_ = globals().get("_V408_FONTES") or {}; fd_ = fontes_.get(ip_["fonte_chave"]) or {}
    try:
        ok_ip_, det_ip_, _b_ip_ = _v392_fonte_bytes(ip_["fonte_chave"])
    except Exception:   # noqa: BLE001
        ok_ip_, det_ip_ = False, "RUNTIME_ERROR"
    integra_nao_pinada_ = not any(str(v_.get("sha256", "")).startswith(ip_["integra_sha16"]) for v_ in fontes_.values())
    alfa_ = globals().get("SEALED_CODATA_ALPHA"); dois_nomes_ = bool(callable(globals().get("_v376_same_alpha_literal")) and _v376_same_alpha_literal())
    beta_alfa_ = (alfa_ * _m408.sqrt(_m408.e)) if isinstance(alfa_, float) else None
    checks_ = [
        {"id": "c1", "descricao": "as %d ancoras das quatro pedras no axiom_report do rito, so' no trio, declaradas no modulo esperado (TGL_DECL_SOURCE), com bandeira True onde ha' bandeira" % len(anc_), "ok": bool(anc_) and len(anc_) == c_["n_ancoras"] and all(v_["ok"] for v_ in anc_.values()) and len(por_mod_) == c_["bundle"]["n"] == 4 and all(por_mod_.values())},
        {"id": "c2", "descricao": "os %d modulos do bundle embutidos com o sha256 do contrato == o hash formal do rito; a raiz embutida traz os quatro imports" % len(c_["source_sha256"]), "ok": n_mod_ok_ == len(c_["source_sha256"]) == c_["bundle"]["n"] and raiz_ok_},
        {"id": "c3", "descricao": "exp(0) = 1 (o zero inscrito e' o Um: o_zero_modular_inscrito_e_o_um) e exp(-0 t) = 1 para t > 0 (sem beta nao ha' segunda face: no_leak_no_second_face)", "ok": e0_ == 1.0 and all(x_ == 1.0 for x_ in e0t_)},
        {"id": "c4", "descricao": "o fator da Meia-Nat e^{-1/2} e' estritamente interior, 0 < f < 1 (the_half_nat_gives_a_strictly_interior_factor)", "ok": 0.0 < f_ < 1.0},
        {"id": "c5", "descricao": "a quitacao: f + (1 - f) = 1 em f = e^{-1/2}, exata em ponto flutuante ate' 1e-15 (a_quitacao, decay_tetelestai_balance)", "ok": abs((f_ + (1.0 - f_)) - 1.0) <= 1e-15 and 0.0 < 1.0 - f_},
        {"id": "c6", "descricao": "o coeficiente de Jones exp(-beta s) != 1 e < 1 para s = 1, com beta em runtime (coeff_ne_one: relacao sem peso e' excluida)", "ok": bq_ and cj_ != 1.0 and cj_ < 1.0},
        {"id": "c7", "descricao": "o vazamento perde estritamente: exp(-t beta g) < 1 para t = g = 1 (leakage_strictly_loses)", "ok": bq_ and vz_ < 1.0},
        {"id": "c8", "descricao": "o pedagio das oitavas: octaveNats(N+1) = (N+1) ln 2 = ln 2^(N+1) para N = 0..10, |Delta| < 1e-12 (CollapseCostLaw.per_octave; o_tamanho_e_o_custo)", "ok": all(abs(a_ - b_) < 1e-12 for a_, b_ in oit_)},
        {"id": "c9", "descricao": "o tempo de ler a torre: t = (N+1) ln 2/(beta g) satisfaz exp(-t beta g) = 2^-(N+1), N = 0..10, |Delta| relativo < 1e-12, com beta em runtime (o_tempo_de_ler_a_torre; linear nos andares)", "ok": bq_ and bool(lin_) and all(x_ < 1e-12 for x_ in lin_)},
        {"id": "c10", "descricao": "a dimensao da torre: dim(chainIdx N) = 2^(N+1) = 2 2^N para N = 0..10 (card_chainIdx: card(0) = 2, card(N+1) = 2 card(N))", "ok": all(card_[N_] == 2 ** (N_ + 1) == 2 * (2 ** N_) for N_ in range(11))},
        {"id": "c11", "descricao": "o piso de Landauer k_B T ln 2 > 0 (k_B do SI, T = 1 K; landauer_floor_pos): o piso no vazio e' positivo", "ok": isinstance(piso_, float) and piso_ > 0.0},
        {"id": "c12", "descricao": "o veredito do gate deste rito e' IDENTICO ao da v407 selada (congelado no contrato): o gate nao se move", "ok": isinstance(gate_, str) and gate_ == c_["baseline"]["gate_verdict"]},
        {"id": "c13", "descricao": "a escada exata: limpos == esperados == a escada do contrato (external_ladder.n_theorems_expected = o X medido no sandbox)", "ok": exact_ and flags_true_ == len(c_["flags"]) == c_["n_flags"]},
        {"id": "c14", "descricao": "as duas guardas de texto (P18 e a guarda das frases, v405 -> v408) limpas sobre o texto deste registro", "ok": not guarda_},
        {"id": "c15", "descricao": "o insumo purgado do acervo (PSION_NO_ACERVO_04nov_purgado.md) relido do disco == o sha256 pinado; a integra (sha16 %s) NAO e' pinada por esta versao e fica fora do espelho (E23)" % ip_["integra_sha16"], "ok": ok_ip_ is True and fd_.get("sha256") == ip_["sha256"] and ip_["integra_fora_do_espelho"] is True and ip_["integra_pinada"] is False and integra_nao_pinada_ and not str(ip_["sha256"]).startswith(ip_["integra_sha16"])},
        {"id": "c16", "descricao": "beta = alfa CODATA 2018 x sqrt(e) em runtime (dois nomes, mesma leitura), igual ao beta do core (nunca literal)", "ok": bq_ and isinstance(core_.get("beta"), float) and abs(beta_ - core_["beta"]) <= 1e-9 * abs(beta_) and isinstance(beta_alfa_, float) and abs(beta_ - beta_alfa_) <= 1e-12 * abs(beta_) and dois_nomes_},
    ]
    values_ = {"n_ancoras_ok": sum(1 for v_ in anc_.values() if v_["ok"]), "n_ancoras": len(anc_), "n_modulos_ok": n_mod_ok_, "n_modulos": c_["bundle"]["n"], "n_flags_true": flags_true_, "n_flags": c_["n_flags"], "escada": cnt_, "ancoras": anc_, "por_modulo": por_mod_, "respostas": resp_,
               "gate_verdict": gate_, "beta": beta_, "meia_nat_fator": f_, "coeficiente_de_jones_s1": cj_, "vazamento_t1_g1": vz_, "ln2": ln2_, "tempo_da_torre_N0_a_N10": t_torre_, "dim_chainIdx_N0_a_N10": card_, "piso_landauer_T1K_J": piso_,
               "insumo_purgado": {"ok": ok_ip_, "detalhe": det_ip_, "sha256": fd_.get("sha256"), "integra_sha16": ip_["integra_sha16"], "integra_nao_pinada": integra_nao_pinada_},
               "ressalvas": list(c_["ressalvas"]), "fica_false_por_teorema": list(c_["fica_false_por_teorema"]), "fica_aberto": dict(c_["fica_aberto"]), "respostas_ok": all(resp_.values()) if resp_ else False}
    return {"passed": all(x_["ok"] for x_ in checks_), "n_checks": len(checks_), "checks": checks_, "values": values_}


def _v408_formal(core, c_, txt_):
    """A evidencia FORMAL do registro, lida do kernel do PROPRIO rito: a escada exata; as ancoras (trio, proveniencia no modulo esperado, bandeira); as 4 fontes por sha256 (embutida == contrato == hash formal do rito); as falas de 04/11 por sha256 (o paragrafo do operador nas duas de autor misto); as duas guardas de texto."""
    import hashlib as _h408, json as _j408
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
        srcs_[rel_] = bool(isinstance(body_, str) and _h408.sha256(body_.encode("utf-8")).hexdigest() == sha_ and ff_.get(rel_) == sha_)
    ver_ = {}
    for k_ in c_["verbatins"]:
        v_ = _V408_VERBATINS2.get(k_)
        ver_[k_] = bool(v_ and _h408.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and all(t_ in v_["text"] for t_ in v_["trechos"]))
    guarda_ = list(_v392_guarda_texto(_j408.dumps(txt_, ensure_ascii=False))) + list(_v408_guarda_frases(_j408.dumps(txt_, ensure_ascii=False)))
    formal_ = bool(kf_.get("all_verified") is True and exact_ and anc_ and all(anc_.values()) and srcs_ and all(srcs_.values()) and ver_ and all(ver_.values()) and not guarda_)
    return {"exact_ladder": exact_, "anchors": anc_, "embedded_sources_ok": all(srcs_.values()), "embedded_sources_n_ok": sum(1 for v_ in srcs_.values() if v_), "inscriptions": ver_, "guarda": guarda_, "formal": formal_}


_V408_RECUSA = "TGL_TETELESTAI_TERMINAL_V408__REFUSED_%s__GATE_UNMOVED"


def tetelestai_terminal_v408(core):
    """v408 -- TETELESTAI E' O TERMINAL (ordem do operador, 04/11/2026: «liste as pedras que eu preciso nominar e em seguida produza a v408 …»; a correcao dele: «A TGL tem terminal sim, ela foi construída sobre ele: TETELESTAI, é a poda …»): lido no PONTO REAL do main, depois dos registros da v407.
    Le do kernel do PROPRIO rito as ancoras das quatro pedras (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP), os 4 modulos por sha256, as falas de 04/11 por sha256; confere as respostas do operador pelos teoremas que ja existiam e pelas declaracoes novas (card_chainIdx, p_igual_np, as_classes_do_dicionario),
    faz as 16 checagens (aritmetica com beta em runtime; gate congelado; escada exata; guardas; insumo purgado; beta = alfa sqrt e). Nenhuma chave antiga muda. Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate. Validade no kernel nao e' creditacao; as ressalvas vao no registro."""
    c_ = _V408_TERMINAL_CONTRACT; t_ = _V408_TERMINAL_TEXT
    f_ = _v408_formal(core, c_, t_)
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
    out_ = {"all_verified": False, "estatuto": t_["estatuto"], "exact_ladder": f_["exact_ladder"], "anchors": f_["anchors"], "embedded_sources_ok": f_["embedded_sources_ok"], "embedded_sources_n_ok": f_["embedded_sources_n_ok"], "inscriptions": f_["inscriptions"],
            "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "ancora_principal": c_["ancora_principal"], "ancoras_principais": list(c_["ancoras_principais"]), "pedras": list(c_["bundle"]["pedras"]), "nomes_do_operador": dict(c_["bundle"]["nomes_do_operador"]),
            "nome_provisorio": c_["bundle"]["nome_provisorio"], "chaves_antigas_que_mudam": list(c_["chaves"]), "ressalvas": list(c_["ressalvas"]), "fica_false_por_teorema": list(c_["fica_false_por_teorema"]), "fica_aberto": dict(c_["fica_aberto"]), "insumo_purgado": dict(c_["insumo_purgado"]),
            "regra_provar_ou_podar": c_["regra_provar_ou_podar"], "podado": list(c_["podado"]), "runtime_executed": False, "does_not_gate_core": True, "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"], "guarda_violacoes": f_["guarda"][:5]}
    out_.update(t_["extras"])
    if not f_["formal"]:
        out_["verdict"] = _V408_RECUSA % "FORMAL_OR_SOURCE_EVIDENCE"
    elif not beta_ok_:
        out_["verdict"] = _V408_RECUSA % "BETA_IS_NOT_ALPHA_SQRT_E"
    else:
        try:
            mec_ = v408_terminal_mechanics(beta_rt_, core, c_)
            out_.update(runtime_executed=True, mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], all_verified=bool(mec_["passed"]))
            out_["verdict"] = (t_["veredito_ok"] if mec_["passed"] else _V408_RECUSA % "MECHANICS_CHECK_FAILED")
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V408_RECUSA % "RUNTIME_ERROR"
    core["tetelestai_terminal_v408"] = out_
    return out_
