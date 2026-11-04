# ---- v407: O PSION, O CANTO E O PAR ENTRAM NO um.py -- os 9 modulos do bundle (PsionCanto, Par e as sete pedras de 02/11 de nome ratificado, todos de TGLExt/) e UM registro com FUNCAO, psion_canto_v407, lido no ponto do rito depois dos registros da v406: ele le do kernel do PROPRIO rito
# as ANCORAS das nove pedras (os #print axioms das candidatas: o lema das duas faces TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces; a leitura de Jones do fluxo da luz pelo canto; o par TGLExt.Par.*), os nove modulos por sha256 (embutido == contrato == hash formal do rito), as falas do operador
# de 03/11 por sha256, as respostas dele conferidas pelos teoremas que ja existiam (o par ligado, CCI = 1/2; nunca se cancela; a leitura pela fase dobrada; o canto 4x4), a escada exata e as duas guardas de texto; e CONFERE que a chave testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma, que o um.py trazia como LITERAL False desde a v396, passou a ser LIDA do kernel.
# A ordem do operador (03/11/2026, sha16 b89e4c909f37e163): «o lema que liga o psion ao canto também já pode ser derivado»; a decisao (sha16 73466598d3419fb0): «o gráviton é o estado ligado de dois psions, portanto, eles nunca se cancelam …»; o nome do par (sha16 57250bbbaca9fd39): «“Par”».
# AS RESSALVAS, ditas em todo texto: o elo das duas faces e' de ESTRUTURA (Omega != Phi+, espacos distintos); o par na face de Fock e' [OPEN]; a ponte Bell-TT nao e' termo; K(O) != bot so' na cunha; o teste (d) so' por citacao do pre-registro; o motor continuo fora; os nomes das pedras sao do operador.
# Validade no kernel NAO e' creditacao; NOT_FALSIFIED nunca e' confirmacao; o GATE NAO SE MOVE; beta nunca literal.
# Fonte autoral deste bloco: runtime_v407.py (cadeia_de_selo/v407); o contrato (_V407_PSION_CONTRACT) e as falas (_V407_VERBATINS2) sao DERIVADOS do build do sandbox e dos arquivos, nunca digitados.


def _v407_guarda_frases(txt_):
    """v407 -- a GUARDA DAS FRASES que afirmam demais: herda as regras da v406 (_v406_guarda_frases) e acrescenta as da v407: «o par de psions na face de Fock esta provado/construido» ([OPEN]: o FockCertificate nao tem criacao como termo), «Omega = Phi+» / «o vacuo de Fock e o vetor de Bell» (o elo e' de estrutura, nao de vetores),
    «a ponte Bell-TT e' teorema» (nao e' termo) e os tokens de veredito correspondentes. A fala do operador nao passa por aqui: ela e' verbatim e fica fora do texto conferido."""
    import re as _re
    out_ = list(_v406_guarda_frases(txt_))
    regras_ = [("F20_par_na_face_de_fock_provado", _re.compile(r"\bpar\s+(?:de\s+ps(?:í|i)ons\s+)?na\s+face\s+de\s+Fock\s+(?:est(?:á|a)\s+|foi\s+)?(?:provad[oa]|constru(?:í|i)d[oa]|habitad[oa]|teorema)|\b(?:pair|pair\s+of\s+psions)\s+on\s+the\s+Fock\s+face\s+(?:is\s+|was\s+)?(?:proved|proven|constructed|inhabited)\b", _re.I)),
               ("F21_omega_igual_phi_mais", _re.compile(r"\b(?:Omega|Ω)\s*=\s*(?:Phi\s*\+|Φ\s*⁺|Φ\+)|\bo\s+v(?:á|a)cuo\s+de\s+Fock\s+(?:é|e)\s+o\s+vetor\s+de\s+Bell\b|\bthe\s+Fock\s+vacuum\s+is\s+the\s+Bell\s+vector\b", _re.I)),
               ("F22_ponte_bell_tt_teorema", _re.compile(r"\bponte\s+(?:entre\s+)?(?:o\s+espa(?:ç|c)o\s+de\s+)?Bell\s*(?:↔|<->|e|-|–)\s*TT\s+(?:(?:é|e)\s+|est(?:á|a)\s+)?(?:teorema|termo|provad[oa])|\bBell\s*[-–]\s*TT\s+bridge\s+(?:is\s+)?(?:a\s+)?(?:theorem|term|proved)\b", _re.I)),
               ("F23_token_de_veredito", _re.compile(r"(?:PAIR|PSION|CORNER|PSION_CANTO)_CONF" + r"IRMED|PAIR_ON_THE_FOCK_FACE_PROVED|FULLY_DERIVED|ALL_DERIVED"))]   # (a palavra banida e' montada por concatenacao: a guarda P18 varre este proprio texto)
    for nome_, rx_ in regras_:
        for m_ in rx_.finditer(str(txt_)):
            out_.append((nome_, str(txt_)[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    return out_


def _v407_elo_lido(kf_):
    """v407 -- LE do kernel do proprio rito se o LEMA DAS DUAS FACES do psion esta' no kernel: a ancora TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces no axiom_report, so' no trio, com a proveniencia que o compilador emite (TGL_DECL_SOURCE) no modulo TGLExt/PsionCanto.lean, e a fonte desse modulo
    embutida com o sha256 do contrato e do hash formal do rito. Nunca literal. Ate' a v406 a chave testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma era o literal False (o estado de entao; errata E18 AO LADO): agora e' esta leitura. O elo e' de ESTRUTURA (nao identifica Omega com Phi+).
    Nao move o gate: o lema e' validade no kernel, nao creditacao."""
    import hashlib as _h407
    kf_ = kf_ or {}
    c_ = globals().get("_V407_PSION_CONTRACT") or {}
    nome_ = c_.get("ancora_lema"); rel_ = ((c_.get("ancoras") or {}).get(nome_) or {}).get("rel")
    if not nome_ or not rel_:
        return False
    axr_ = kf_.get("axiom_report") or {}; src_ = kf_.get("declaration_sources_v394") or {}
    vals_ = axr_.get(nome_); trio_ = {"propext", "Classical.choice", "Quot.sound"}
    body_ = _EMBEDDED_KERNEL_FILES.get(rel_)
    esperado_ = (c_.get("source_sha256") or {}).get(rel_)
    sha_ok_ = bool(isinstance(body_, str) and isinstance(esperado_, str) and _h407.sha256(body_.encode("utf-8")).hexdigest() == esperado_ == (kf_.get("formal_files_sha256") or {}).get(rel_))
    return bool(kf_.get("all_verified") is True and isinstance(vals_, list) and vals_ and all(isinstance(v_, str) for v_ in vals_) and set(vals_) <= trio_ and src_.get(nome_) == rel_ and sha_ok_)   # com o kernel RECUSADO (all_verified False) a chave nunca le True


def _v407_chaves(core_):
    """as chaves de testemunha, LIDAS do core deste rito: a do lema (nova na v407) e as quatro da v406 (seguem lidas), ao lado do que o kernel diz."""
    kf_ = core_.get("kernel_formalization") or {}
    rf_ = core_.get("rede_fock_v394") or {}; pb_ = (core_.get("psibit_v395") or {}).get("conditional_psion_face") or {}; te_ = (core_.get("testemunha_estatica_v396") or {}).get("fock_face") or {}; wl_ = core_.get("witness_layers") or {}
    return {"kernel_reads_the_link": _v407_elo_lido(kf_),
            "testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma": te_.get("linked_to_the_corner_by_a_lemma"),
            "rede_fock_v394.whole_certificate_inhabited": rf_.get("whole_certificate_inhabited"),
            "psibit_v395.conditional_psion_face.inhabitant_exhibited": pb_.get("inhabitant_exhibited"),
            "testemunha_estatica_v396.fock_face.inhabitant_exhibited": te_.get("inhabitant_exhibited"),
            "witness_layers.canonical_full_witness_term_constructed": wl_.get("canonical_full_witness_term_constructed"),
            "witness_rigidity.trivial_inhabitant_exists": (core_.get("witness_rigidity") or {}).get("trivial_inhabitant_exists"),
            "qg_closure.gate.full_static_witness_exists": ((core_.get("qg_closure") or {}).get("gate") or {}).get("full_static_witness_exists")}


def v407_psion_mechanics(beta_, core_, c_):
    """o «calculo» do registro (nenhum numero novo da natureza entra: tudo e' leitura do kernel e do core deste rito): (1) as ancoras das nove pedras no trio, no modulo esperado, com bandeira True; (2) os 9 modulos embutidos com o sha256 do contrato == o hash formal do rito;
    (3) a raiz embutida traz os nove imports; (4) a chave do lema LIDA == o que o kernel diz (True); (5) o lema e o par (as 5 declaracoes do Par) no trio, nos modulos esperados; (6) as respostas do operador conferidas pelos teoremas que ja existiam; (7) cada um dos 9 modulos tem TODAS as suas ancoras;
    (8) o que fica False por teorema segue False; (9) a escada exata; (10) os registros antigos seguem selados (fechamento_v406, rede_fock_v394, psibit_v395, testemunha_estatica_v396); (11) as bandeiras todas True; (12) a proveniencia cobre o axiom_report; (13) beta = alfa x sqrt e (nunca literal);
    (14) o gate deste rito tem o mesmo veredito da base; (15) as quatro chaves da v406 seguem lidas (True); (16) o teste (d) so' consta por citacao do pre-registro (nenhum resultado)."""
    import hashlib as _h407
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
        if isinstance(body_, str) and _h407.sha256(body_.encode("utf-8")).hexdigest() == sha_ == ff_.get(rel_):
            n_mod_ok_ += 1
    raiz_ = _EMBEDDED_KERNEL_FILES.get("TGLExt.lean") or ""
    raiz_ok_ = all(l_ in raiz_.replace("\r\n", "\n") for l_ in c_["root_suffix"].replace("\r\n", "\n").split("\n") if l_.strip())
    ch_ = _v407_chaves(core_)
    por_mod_ = {rel_: bool(nomes_ and all(anc_.get(n_, {}).get("ok") for n_ in nomes_)) for rel_, nomes_ in c_["ancoras_por_modulo"].items()}
    par_ = [n_ for n_ in c_["ancoras_por_modulo"][c_["bundle"]["par"]]]
    resp_ = {r_["id"]: bool(r_["teoremas"] and all(em_trio_(t_["completo"]) and src_.get(t_["completo"]) == t_["rel"] for t_ in r_["teoremas"])) for r_ in c_["respostas"]}
    lad_ = core_.get("external_ladder") or {}
    cnt_ = [lad_.get("n_theorems_clean"), lad_.get("n_theorems_expected"), c_["expected_ladder"]]
    exact_ = all(type(x_) is int for x_ in cnt_) and len(set(cnt_)) == 1
    flags_true_ = sum(1 for k_ in c_["flags"] if kf_.get(k_) is True)
    gate_ = ((core_.get("qg_closure") or {}).get("gate") or {}).get("verdict")
    fontes_ = globals().get("_V407_FONTES") or {}
    td_ = c_["teste_d"]; fd_ = fontes_.get(td_["fonte_chave"]) or {}
    checks_ = [
        {"id": "c1", "descricao": "as %d ancoras das nove pedras no trio, declaradas no modulo esperado, com bandeira True onde ha' bandeira" % len(anc_), "ok": bool(anc_) and all(v_["ok"] for v_ in anc_.values())},
        {"id": "c2", "descricao": "os %d modulos do bundle embutidos com o sha256 do contrato == o hash formal do rito" % len(c_["source_sha256"]), "ok": n_mod_ok_ == len(c_["source_sha256"]) == c_["bundle"]["n"]},
        {"id": "c3", "descricao": "a raiz embutida TGLExt.lean traz os nove imports das pedras", "ok": raiz_ok_},
        {"id": "c4", "descricao": "testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma e' True e e' a leitura do kernel (nao literal)", "ok": ch_["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is True and ch_["kernel_reads_the_link"] is True},
        {"id": "c5", "descricao": "o lema das duas faces e as declaracoes do Par estao no trio, nos modulos esperados, com bandeira", "ok": bool(par_) and all(anc_.get(n_, {}).get("ok") for n_ in [c_["ancora_lema"]] + par_)},
        {"id": "c6", "descricao": "as respostas do operador de 03/11 conferem pelos teoremas que ja existiam (par ligado; nunca se cancela; leitura pela fase dobrada; canto 4x4): no trio, nos modulos de sempre", "ok": bool(resp_) and all(resp_.values())},
        {"id": "c7", "descricao": "cada um dos 9 modulos tem TODAS as suas ancoras no kernel (PsionCanto, Par e as sete pedras de 02/11)", "ok": len(por_mod_) == c_["bundle"]["n"] == 9 and all(por_mod_.values())},
        {"id": "c8", "descricao": "o que fica False por teorema segue False (full_static_witness_exists, trivial_inhabitant_exists)", "ok": ch_["qg_closure.gate.full_static_witness_exists"] is False and ch_["witness_rigidity.trivial_inhabitant_exists"] is False},
        {"id": "c9", "descricao": "a escada exata: limpos == esperados == a escada do contrato", "ok": exact_},
        {"id": "c10", "descricao": "fechamento_v406, rede_fock_v394, psibit_v395 e testemunha_estatica_v396 seguem SELADOS neste rito", "ok": all((core_.get(n_) or {}).get("all_verified") is True for n_ in ("fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396"))},
        {"id": "c11", "descricao": "as %d bandeiras do bundle sao True no kernel deste rito" % len(c_["flags"]), "ok": flags_true_ == len(c_["flags"]) == c_["n_flags"]},
        {"id": "c12", "descricao": "a proveniencia emitida pelo compilador cobre o axiom_report", "ok": (kf_.get("declaration_sources_status_v394") or {}).get("ok") is True},
        {"id": "c13", "descricao": "beta = alfa CODATA 2018 x sqrt(e) em runtime, igual ao beta do core (nunca literal)", "ok": isinstance(beta_, float) and isinstance(core_.get("beta"), float) and abs(beta_ - core_["beta"]) <= 1e-9 * abs(beta_)},
        {"id": "c14", "descricao": "o gate deste rito tem o MESMO veredito da base selada (o gate nao se move)", "ok": isinstance(gate_, str) and gate_ == c_["baseline"]["gate_verdict"]},
        {"id": "c15", "descricao": "as quatro chaves da v406 seguem lidas do kernel (True)", "ok": all(ch_[k_] is True for k_ in ("rede_fock_v394.whole_certificate_inhabited", "psibit_v395.conditional_psion_face.inhabitant_exhibited", "testemunha_estatica_v396.fock_face.inhabitant_exhibited", "witness_layers.canonical_full_witness_term_constructed"))},
        {"id": "c16", "descricao": "o teste (d) so' consta por CITACAO do pre-registro V1.1 (manifesto pinado por sha256); nenhum resultado no um.py: nenhuma chave do core com conjunto_d, teste_d_ ou ramo_b_resultado/veredito", "ok": td_.get("so_citado") is True and td_.get("resultado_no_um_py") is None and fd_.get("sha256") == td_["manifesto_sha256"] and td_["manifesto_sha256"].startswith(td_["manifesto_sha16"]) and not any(("conjunto_d" in str(k_).lower() or "teste_d_" in str(k_).lower() or ("ramo_b" in str(k_).lower() and ("resultado" in str(k_).lower() or "veredito" in str(k_).lower()))) for k_ in core_)},
    ]
    values_ = {"n_ancoras_ok": sum(1 for v_ in anc_.values() if v_["ok"]), "n_ancoras": len(anc_), "n_modulos_ok": n_mod_ok_, "n_modulos": c_["bundle"]["n"], "n_flags_true": flags_true_, "n_flags": c_["n_flags"], "escada": cnt_, "chaves": ch_, "ancoras": anc_, "por_modulo": por_mod_, "respostas": resp_,
               "gate_verdict": gate_, "beta": beta_, "elo_lido_do_kernel": ch_["kernel_reads_the_link"], "ressalvas": list(c_["ressalvas"]), "fica_false_por_teorema": list(c_["fica_false_por_teorema"]), "fica_aberto": dict(c_["fica_aberto"])}
    return {"passed": all(x_["ok"] for x_ in checks_), "n_checks": len(checks_), "checks": checks_, "values": values_}


def _v407_formal(core, c_, txt_):
    """A evidencia FORMAL do registro, lida do kernel do PROPRIO rito: a escada exata; as ancoras (trio, proveniencia no modulo esperado, bandeira); as 9 fontes por sha256 (embutida == contrato == hash formal do rito); as falas de 03/11 por sha256; as duas guardas de texto."""
    import hashlib as _h407, json as _j407
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
        srcs_[rel_] = bool(isinstance(body_, str) and _h407.sha256(body_.encode("utf-8")).hexdigest() == sha_ and ff_.get(rel_) == sha_)
    ver_ = {}
    for k_ in c_["verbatins"]:
        v_ = _V407_VERBATINS2.get(k_)
        ver_[k_] = bool(v_ and _h407.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and all(t_ in v_["text"] for t_ in v_["trechos"]))
    guarda_ = list(_v392_guarda_texto(_j407.dumps(txt_, ensure_ascii=False))) + list(_v407_guarda_frases(_j407.dumps(txt_, ensure_ascii=False)))
    formal_ = bool(kf_.get("all_verified") is True and exact_ and anc_ and all(anc_.values()) and srcs_ and all(srcs_.values()) and ver_ and all(ver_.values()) and not guarda_)
    return {"exact_ladder": exact_, "anchors": anc_, "embedded_sources_ok": all(srcs_.values()), "embedded_sources_n_ok": sum(1 for v_ in srcs_.values() if v_), "inscriptions": ver_, "guarda": guarda_, "formal": formal_}


_V407_RECUSA = "TGL_PSION_CANTO_V407__REFUSED_%s__GATE_UNMOVED"


def psion_canto_v407(core):
    """v407 -- O PSION, O CANTO E O PAR (ordem do operador, 03/11/2026: «o lema que liga o psion ao canto também já pode ser derivado»): lido no PONTO REAL do main, depois dos registros da v406. Le do kernel do PROPRIO rito as ancoras das nove pedras (o lema das duas faces, a leitura de Jones sob compressao,
    o par ligado, o canto 4x4 e as sete pedras de 02/11), os 9 modulos por sha256, as falas de 03/11 por sha256; confere que a chave do lema e' LIDA do kernel (nao literal), as respostas do operador pelos teoremas que ja existiam e que o que fica False por teorema segue False; o beta em runtime; o gate com o mesmo veredito da base.
    Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate. Validade no kernel nao e' creditacao; as ressalvas vao no registro."""
    c_ = _V407_PSION_CONTRACT; t_ = _V407_PSION_TEXT
    f_ = _v407_formal(core, c_, t_)
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
    out_ = {"all_verified": False, "estatuto": t_["estatuto"], "exact_ladder": f_["exact_ladder"], "anchors": f_["anchors"], "embedded_sources_ok": f_["embedded_sources_ok"], "embedded_sources_n_ok": f_["embedded_sources_n_ok"], "inscriptions": f_["inscriptions"],
            "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "link_read_from_the_kernel": _v407_elo_lido(core.get("kernel_formalization")), "lemma": c_["ancora_lema"], "pair_theorem": c_["ancora_par"],
            "keys": _v407_chaves(core), "pedras": list(c_["bundle"]["pedras"]), "nomes_do_operador": dict(c_["bundle"]["nomes_do_operador"]), "ressalvas": list(c_["ressalvas"]), "fica_false_por_teorema": list(c_["fica_false_por_teorema"]), "fica_aberto": dict(c_["fica_aberto"]),
            "teste_d": dict(c_["teste_d"]), "runtime_executed": False, "does_not_gate_core": True, "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"], "guarda_violacoes": f_["guarda"][:5]}
    out_.update(t_["extras"])
    if not f_["formal"]:
        out_["verdict"] = _V407_RECUSA % "FORMAL_OR_SOURCE_EVIDENCE"
    elif not beta_ok_:
        out_["verdict"] = _V407_RECUSA % "BETA_IS_NOT_ALPHA_SQRT_E"
    else:
        try:
            mec_ = v407_psion_mechanics(beta_rt_, core, c_)
            out_.update(runtime_executed=True, mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], all_verified=bool(mec_["passed"]))
            out_["verdict"] = (t_["veredito_ok"] if mec_["passed"] else _V407_RECUSA % "MECHANICS_CHECK_FAILED")
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V407_RECUSA % "RUNTIME_ERROR"
    core["psion_canto_v407"] = out_
    return out_
