# ---- v406: O FECHAMENTO ENTRA NO um.py -- os 301 modulos do bundle (os 300 da bancada do ChatGPT, missao F1.FECHO_20261015, 15 e 16/10/2026, recompilados do fonte na integracao R3 de 02/11/2026; e a candidata CanonicalFullTGLWitnessR1 da gerencia)
# e UM registro com FUNCAO, fechamento_v406, lido no ponto do rito depois dos registros da v405: ele le do kernel do PROPRIO rito as OITO ancoras (o habitante dos 21 campos da passagem para o continuo, modularCoreInput; o CERTIFICADO DE FOCK habitado sobre a rede
# fisica, physicalFockCertificate; o traco do certificado = o traco ciclico; a rede fisica physicalCanonicalNet e a sua nao-trivialidade NA CUNHA; o termo canonico da testemunha completa, canonicalFullTGLWitness, e o Nonempty), a fonte dos 301 modulos por sha256
# (embutida == contrato == hash formal do rito), as falas do operador de 02/11 por sha256, a escada exata e as duas guardas de texto; e CONFERE que as QUATRO chaves de testemunha que o um.py trazia como LITERAL False desde a v394 passaram a ser LIDAS do kernel.
# A ordem do operador (02/11/2026, sha16 f3998f01262aad6b): «precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento.»; a prioridade (sha16 9978862f60cfbf29): «a construção da passagem para o contínuo é o que mais importa».
# AS RESSALVAS (ratificacao R10 da gerencia, 02/11/2026), ditas em todo texto: K(O) != bot para O compacto NAO esta' provado (so' na cunha); «nucleo II_inf» e' [KNOWN/DECLARADO]; o traco e' ENNReal e ciclico, nao linear; R7 foi Codex x Codex (a revisao distinta e' do Sonnet);
# R4/R5 ficam fora; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA; o nome da candidata e' provisorio da gerencia. Validade no kernel NAO e' creditacao; NOT_FALSIFIED nunca e' confirmacao; o GATE NAO SE MOVE; beta nunca literal.
# Fonte autoral deste bloco: runtime_v406.py (cadeia_de_selo/v406); o contrato (_V406_FECHO_CONTRACT) e as falas (_V406_VERBATINS2) sao DERIVADOS do build do sandbox e dos arquivos, nunca digitados.


def _v406_guarda_frases(txt_):
    """v406 -- a GUARDA DAS FRASES que afirmam demais: herda as regras da v405 (_v405_guarda_frases) e acrescenta as da v406: «a luz nao tem autovetor» (a frase da gerencia que o operador corrigiu em 02/11; errata E15), «unico autovetor» (o certo e' «unico vetor fixo»),
    «certificado/fechamento/gravidade quantica confirmad(o/a)» (confirmacao e' creditacao, proibida), «K(O) != bot provado» (so' na cunha) e os tokens de veredito correspondentes. A fala do operador nao passa por aqui: ela e' verbatim e fica fora do texto conferido."""
    import re as _re
    out_ = list(_v405_guarda_frases(txt_))
    regras_ = [("F15_a_luz_nao_tem_autovetor", _re.compile(r"(?<!«)\ba\s+luz\s+n(?:ã|a)o\s+tem\s+autovetor|(?<!«)\bthe\s+light\s+has\s+no\s+eigenvector", _re.I)),   # a MENCAO entre « » (a errata E15 cita a frase errada para corrigi-la) passa; o USO reprova
               ("F16_unico_autovetor", _re.compile(r"\b(?:ú|u)nico\s+autovetor\b|\b(?:only|sole|unique)\s+eigenvector\b", _re.I)),
               ("F17_confirmacao_e_creditacao", _re.compile(r"\b(?:certificad[oa]|fechamento|gravidade\s+qu(?:â|a)ntica|gravita(?:ç|c)(?:ã|a)o\s+qu(?:â|a)ntica|passagem)\s+(?:est(?:á|a)\s+|foi\s+|ficou\s+)?confirmad[oa]\b|\b(?:certificate|closure|quantum\s+gravity|passage)\s+(?:is\s+|was\s+)?confirmed\b", _re.I)),
               ("F18_k_do_compacto_provado", _re.compile(r"K\s*\(\s*O\s*\)\s*(?:≠|!=|\\ne|\\neq)\s*(?:⊥|bot|\\bot)\s+(?:est(?:á|a)\s+)?(?:provad[oa]|e'\s+teorema|é\s+teorema|is\s+(?:a\s+)?theorem|proved)", _re.I)),
               ("F19_token_de_veredito", _re.compile(r"(?:CERTIFICATE|CLOSURE|QG|QUANTUM_GRAVITY)_CONF" + r"IRMED|FULLY_DERIVED|ALL_DERIVED|NOTHING_REMAINS_OPEN"))]   # (a palavra banida e' montada por concatenacao: a guarda P18 varre este proprio texto)
    for nome_, rx_ in regras_:
        for m_ in rx_.finditer(str(txt_)):
            out_.append((nome_, str(txt_)[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    return out_


def _v406_certificado_habitado(kf_):
    """v406 -- LE do kernel do proprio rito se o certificado de Fock esta' HABITADO: a ancora physicalFockCertificate (F1Fecho.CanonicalFockModularCoreInputR1) no axiom_report, so' no trio, com a proveniencia que o compilador emite (TGL_DECL_SOURCE) no modulo do topo
    do fecho, e a fonte desse modulo embutida com o sha256 do contrato e do hash formal do rito. Nunca literal. Antes da v406 as chaves rede_fock_v394.whole_certificate_inhabited, psibit_v395...inhabitant_exhibited e testemunha_estatica_v396...inhabitant_exhibited eram
    o literal False (o estado de entao; errata E14 AO LADO): agora sao esta leitura. Nao move o gate: o certificado habitado e' validade no kernel, nao creditacao."""
    import hashlib as _h406
    kf_ = kf_ or {}
    c_ = globals().get("_V406_FECHO_CONTRACT") or {}
    nome_ = c_.get("ancora_certificado"); rel_ = ((c_.get("ancoras") or {}).get(nome_) or {}).get("rel")
    if not nome_ or not rel_:
        return False
    axr_ = kf_.get("axiom_report") or {}; src_ = kf_.get("declaration_sources_v394") or {}
    vals_ = axr_.get(nome_); trio_ = {"propext", "Classical.choice", "Quot.sound"}
    body_ = _EMBEDDED_KERNEL_FILES.get(rel_)
    esperado_ = (c_.get("source_sha256") or {}).get(rel_)
    sha_ok_ = bool(isinstance(body_, str) and isinstance(esperado_, str) and _h406.sha256(body_.encode("utf-8")).hexdigest() == esperado_ == (kf_.get("formal_files_sha256") or {}).get(rel_))
    return bool(kf_.get("all_verified") is True and isinstance(vals_, list) and vals_ and all(isinstance(v_, str) for v_ in vals_) and set(vals_) <= trio_ and src_.get(nome_) == rel_ and sha_ok_)   # com o kernel RECUSADO (all_verified False) a chave nunca le True


def _v406_chaves(core_):
    """as QUATRO chaves de testemunha, LIDAS do core deste rito (o que os registros da v394, v395, v396 e o witness_layers gravaram), ao lado do que o kernel diz (a leitura)."""
    kf_ = core_.get("kernel_formalization") or {}
    lida_ = _v406_certificado_habitado(kf_)
    rf_ = core_.get("rede_fock_v394") or {}; pb_ = (core_.get("psibit_v395") or {}).get("conditional_psion_face") or {}; te_ = (core_.get("testemunha_estatica_v396") or {}).get("fock_face") or {}; wl_ = core_.get("witness_layers") or {}
    return {"kernel_reads_the_certificate_as_inhabited": lida_,
            "rede_fock_v394.whole_certificate_inhabited": rf_.get("whole_certificate_inhabited"),
            "psibit_v395.conditional_psion_face.inhabitant_exhibited": pb_.get("inhabitant_exhibited"), "psibit_v395.conditional_psion_face.status": pb_.get("status"),
            "testemunha_estatica_v396.fock_face.inhabitant_exhibited": te_.get("inhabitant_exhibited"), "testemunha_estatica_v396.fock_face.status": te_.get("status"),
            "testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma": te_.get("linked_to_the_corner_by_a_lemma"),
            "witness_layers.canonical_full_witness_term_constructed": wl_.get("canonical_full_witness_term_constructed"),
            "witness_rigidity.trivial_inhabitant_exists": (core_.get("witness_rigidity") or {}).get("trivial_inhabitant_exists"),
            "qg_closure.gate.full_static_witness_exists": ((core_.get("qg_closure") or {}).get("gate") or {}).get("full_static_witness_exists")}


def v406_fechamento_mechanics(beta_, core_, c_):
    """o «calculo» do fechamento (nenhum numero novo da natureza entra: tudo e' leitura do kernel e do core deste rito): (1) as oito ancoras no trio, no modulo esperado, com bandeira True; (2) os 301 modulos embutidos com o sha256 do contrato == o hash formal do rito;
    (3) a raiz embutida traz os dois imports; (4-7) as quatro chaves lidas == o que o kernel diz (True) e os status novos; (8) o que FICA False por teorema segue False e o lema que falta segue False; (9) a escada exata; (10) os tres registros que leem a chave seguem selados;
    (11) as bandeiras do bundle todas True; (12) a proveniencia cobre o axiom_report; (13) beta = alfa x sqrt e (nunca literal); (14) o gate deste rito tem o mesmo veredito da base (o gate nao se move)."""
    import hashlib as _h406
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
        if isinstance(body_, str) and _h406.sha256(body_.encode("utf-8")).hexdigest() == sha_ == ff_.get(rel_):
            n_mod_ok_ += 1
    raiz_ = _EMBEDDED_KERNEL_FILES.get("TGLExt.lean") or ""
    raiz_ok_ = all(l_ in raiz_.replace("\r\n", "\n") for l_ in c_["root_suffix"].replace("\r\n", "\n").split("\n") if l_.strip())
    ch_ = _v406_chaves(core_)
    lad_ = core_.get("external_ladder") or {}
    cnt_ = [lad_.get("n_theorems_clean"), lad_.get("n_theorems_expected"), c_["expected_ladder"]]
    exact_ = all(type(x_) is int for x_ in cnt_) and len(set(cnt_)) == 1
    flags_true_ = sum(1 for k_ in c_["flags"] if kf_.get(k_) is True)
    gate_ = ((core_.get("qg_closure") or {}).get("gate") or {}).get("verdict")
    checks_ = [
        {"id": "c1", "descricao": "as oito ancoras no trio, declaradas no modulo esperado, com bandeira True onde ha' bandeira", "ok": all(v_["ok"] for v_ in anc_.values()) and len(anc_) == 8},
        {"id": "c2", "descricao": "os %d modulos do bundle embutidos com o sha256 do contrato == o hash formal do rito" % len(c_["source_sha256"]), "ok": n_mod_ok_ == len(c_["source_sha256"]) == c_["bundle"]["n"]},
        {"id": "c3", "descricao": "a raiz embutida TGLExt.lean traz os dois imports do fecho", "ok": raiz_ok_},
        {"id": "c4", "descricao": "rede_fock_v394.whole_certificate_inhabited e' True e e' a leitura do kernel (nao literal)", "ok": ch_["rede_fock_v394.whole_certificate_inhabited"] is True and ch_["kernel_reads_the_certificate_as_inhabited"] is True},
        {"id": "c5", "descricao": "psibit_v395: a face do psion le o habitante (True) e o status novo", "ok": ch_["psibit_v395.conditional_psion_face.inhabitant_exhibited"] is True and ch_["psibit_v395.conditional_psion_face.status"] == c_["status_habitado"]},
        {"id": "c6", "descricao": "testemunha_estatica_v396: a face de Fock le o habitante (True) e o status novo", "ok": ch_["testemunha_estatica_v396.fock_face.inhabitant_exhibited"] is True and ch_["testemunha_estatica_v396.fock_face.status"] == c_["status_habitado"]},
        {"id": "c7", "descricao": "witness_layers.canonical_full_witness_term_constructed e' True (o nome exato canonicalFullTGLWitness esta' no axiom_report)", "ok": ch_["witness_layers.canonical_full_witness_term_constructed"] is True and em_trio_(c_["ancora_testemunha"])},
        {"id": "c8", "descricao": "o que fica False por teorema segue False (full_static_witness_exists, trivial_inhabitant_exists) e o lema que falta segue False (linked_to_the_corner_by_a_lemma)", "ok": ch_["qg_closure.gate.full_static_witness_exists"] is False and ch_["witness_rigidity.trivial_inhabitant_exists"] is False and ch_["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is False},
        {"id": "c9", "descricao": "a escada exata: limpos == esperados == a escada do contrato", "ok": exact_},
        {"id": "c10", "descricao": "rede_fock_v394, psibit_v395 e testemunha_estatica_v396 seguem SELADOS neste rito", "ok": all((core_.get(n_) or {}).get("all_verified") is True for n_ in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396"))},
        {"id": "c11", "descricao": "as %d bandeiras do bundle sao True no kernel deste rito" % len(c_["flags"]), "ok": flags_true_ == len(c_["flags"]) == c_["n_flags"]},
        {"id": "c12", "descricao": "a proveniencia emitida pelo compilador cobre o axiom_report", "ok": (kf_.get("declaration_sources_status_v394") or {}).get("ok") is True},
        {"id": "c13", "descricao": "beta = alfa CODATA 2018 x sqrt(e) em runtime, igual ao beta do core (nunca literal)", "ok": isinstance(beta_, float) and isinstance(core_.get("beta"), float) and abs(beta_ - core_["beta"]) <= 1e-9 * abs(beta_)},
        {"id": "c14", "descricao": "o gate deste rito tem o MESMO veredito da base selada (o gate nao se move)", "ok": isinstance(gate_, str) and gate_ == c_["baseline"]["gate_verdict"]},
    ]
    values_ = {"n_ancoras_ok": sum(1 for v_ in anc_.values() if v_["ok"]), "n_modulos_ok": n_mod_ok_, "n_modulos": c_["bundle"]["n"], "n_flags_true": flags_true_, "n_flags": c_["n_flags"], "escada": cnt_, "chaves": ch_, "ancoras": anc_, "gate_verdict": gate_,
               "beta": beta_, "certificado_habitado_lido_do_kernel": ch_["kernel_reads_the_certificate_as_inhabited"], "ressalvas": list(c_["ressalvas"]), "fica_false_por_teorema": list(c_["fica_false_por_teorema"])}
    return {"passed": all(x_["ok"] for x_ in checks_), "n_checks": len(checks_), "checks": checks_, "values": values_}


def _v406_formal(core, c_, txt_):
    """A evidencia FORMAL do registro, lida do kernel do PROPRIO rito: a escada exata; as oito ancoras (trio, proveniencia no modulo esperado, bandeira); as 301 fontes por sha256 (embutida == contrato == hash formal do rito); as falas de 02/11 por sha256; as duas guardas de texto."""
    import hashlib as _h406, json as _j406
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
        srcs_[rel_] = bool(isinstance(body_, str) and _h406.sha256(body_.encode("utf-8")).hexdigest() == sha_ and ff_.get(rel_) == sha_)
    ver_ = {}
    for k_ in c_["verbatins"]:
        v_ = _V406_VERBATINS2.get(k_)
        ver_[k_] = bool(v_ and _h406.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and all(t_ in v_["text"] for t_ in v_["trechos"]))
    guarda_ = list(_v392_guarda_texto(_j406.dumps(txt_, ensure_ascii=False))) + list(_v406_guarda_frases(_j406.dumps(txt_, ensure_ascii=False)))
    formal_ = bool(kf_.get("all_verified") is True and exact_ and anc_ and all(anc_.values()) and srcs_ and all(srcs_.values()) and ver_ and all(ver_.values()) and not guarda_)
    return {"exact_ladder": exact_, "anchors": anc_, "embedded_sources_ok": all(srcs_.values()), "embedded_sources_n_ok": sum(1 for v_ in srcs_.values() if v_), "inscriptions": ver_, "guarda": guarda_, "formal": formal_}


_V406_RECUSA = "TGL_FECHAMENTO_V406__REFUSED_%s__GATE_UNMOVED"


def fechamento_v406(core):
    """v406 -- O FECHAMENTO (ordem do operador, 02/11/2026: «construir tudo»): lido no PONTO REAL do main, depois dos registros da v405. Le do kernel do PROPRIO rito as oito ancoras (modularCoreInput, physicalModularCoreInput, physicalFockCertificate, physical_trace,
    physicalCanonicalNet, physical_canonical_net_nonzero, canonicalFullTGLWitness, canonical_full_witness_inhabited), os 301 modulos por sha256, as falas de 02/11 por sha256; confere que as QUATRO chaves de testemunha sao LIDAS do kernel (nao literal) e que o que fica
    False por teorema segue False; o beta em runtime; o gate com o mesmo veredito da base. Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate. Validade no kernel nao e' creditacao; as ressalvas vao no registro."""
    c_ = _V406_FECHO_CONTRACT; t_ = _V406_FECHO_TEXT
    f_ = _v406_formal(core, c_, t_)
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
    out_ = {"all_verified": False, "estatuto": t_["estatuto"], "exact_ladder": f_["exact_ladder"], "anchors": f_["anchors"], "embedded_sources_ok": f_["embedded_sources_ok"], "embedded_sources_n_ok": f_["embedded_sources_n_ok"], "inscriptions": f_["inscriptions"],
            "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "certificate_inhabited": _v406_certificado_habitado(core.get("kernel_formalization")), "inhabited_by": c_["ancora_certificado"], "canonical_full_witness_term": c_["ancora_testemunha"],
            "four_keys": _v406_chaves(core), "ressalvas": list(c_["ressalvas"]), "fica_false_por_teorema": list(c_["fica_false_por_teorema"]), "runtime_executed": False, "does_not_gate_core": True, "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"],
            "guarda_violacoes": f_["guarda"][:5], "nome_provisorio_da_candidata": c_["candidata"]["nome_provisorio_da_gerencia"]}
    out_.update(t_["extras"])
    if not f_["formal"]:
        out_["verdict"] = _V406_RECUSA % "FORMAL_OR_SOURCE_EVIDENCE"
    elif not beta_ok_:
        out_["verdict"] = _V406_RECUSA % "BETA_IS_NOT_ALPHA_SQRT_E"
    else:
        try:
            mec_ = v406_fechamento_mechanics(beta_rt_, core, c_)
            out_.update(runtime_executed=True, mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], all_verified=bool(mec_["passed"]))
            out_["verdict"] = (t_["veredito_ok"] if mec_["passed"] else _V406_RECUSA % "MECHANICS_CHECK_FAILED")
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V406_RECUSA % "RUNTIME_ERROR"
    core["fechamento_v406"] = out_
    return out_
