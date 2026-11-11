# -*- coding: utf-8 -*-
# [AUTORAL v410, 09/11/2026, claude-construtor-v410, a servico da gerencia c1] o TERCEIRO registro com FUNCAO da v410 (D80 do DESENHO_v410): o recibo documental HMS/13 do Kimi, ADITIVO e POSTERIOR ao FREEZE_R2.
# ---- v410 (D80): H0DN FONTES HMS/13 -- A COBERTURA DOCUMENTAL DAS 18 FONTES PRIMARIAS DOS 13 CALIBRADORES: cobertura documental de fontes, não covariância física fechada; nada aberto. A ordem do operador (09/11/2026), ratificada por sha256
# (a frase final da fala; a cunhagem que a antecede nao entra por este registro: e' a pedra da D82, parte 2), incorporou a ORDEM do Kimi K3 Pro ao um.py como registro novo, aditivo e posterior ao FREEZE_R2 (os 9 pinos do congelamento e os 11 do registro h0dn_bg1_v410 nao mudam). O BUILD leu os quatro artefatos
# documentais (mapa, manifesto, validacao, levantamento) por bytes e sha256 e os embutiu; em RITO nenhum arquivo da pasta do Kimi e' aberto: este registro confere so' o conteudo embutido (os pinos, os 13 IDs, as 18 fontes, os dez campos obrigatorios, a guarda numerica,
# o gate, a posterioridade ao FREEZE_R2, a ratificacao por sha256, a funcao de veredito do H0DN intocada). H0DN x BG1: pré-registrado; nenhum dado observado lido. Fonte autoral deste bloco: runtime_hms13_v410.py (cadeia_de_selo/v410); o contrato (_V410_HMS13_CONTRACT),
# o texto (_V410_HMS13_TEXT) e os insumos (_V410_HMS13_INSUMOS) sao DERIVADOS dos arquivos pinados, nunca digitados.


def _v410_hms13_numeros(obj_, permitidos_, proibidos_len_, caminho_=""):
    """v410 (D80 §5) -- percorre um JSON embutido: devolve (permitidos, proibidos, listas_numericas). Todo numero (fora bool) e' permitido so' se a chave traz um dos radicais permitidos (bytes, contagem, linha, caracteres de texto, componente de erro);
    toda lista numerica e' proibida, e as de comprimento 255 ou 64 (o vetor observado; os valores publicados) sao marcadas a parte."""
    perm_, proib_, arrays_ = [], [], []
    if isinstance(obj_, dict):
        for k_, v_ in obj_.items():
            p_, q_, a_ = _v410_hms13_numeros(v_, permitidos_, proibidos_len_, caminho_ + "/" + str(k_)); perm_ += p_; proib_ += q_; arrays_ += a_
    elif isinstance(obj_, list):
        if obj_ and all(isinstance(x_, (int, float)) and not isinstance(x_, bool) for x_ in obj_):
            arrays_.append((caminho_, len(obj_), len(obj_) in proibidos_len_))
        for i_, v_ in enumerate(obj_):
            p_, q_, a_ = _v410_hms13_numeros(v_, permitidos_, proibidos_len_, caminho_ + "[%d]" % i_); perm_ += p_; proib_ += q_; arrays_ += a_
    elif isinstance(obj_, (int, float)) and not isinstance(obj_, bool):
        chave_ = caminho_.rsplit("/", 1)[-1].lower()
        (perm_ if any(r_ in chave_ for r_ in permitidos_) else proib_).append((caminho_, obj_))
    return perm_, proib_, arrays_


def _v410_hms13_mechanics(core_, c_, t_, insumos_, tocados_=None):
    """v410 -- as 12 checagens do registro documental HMS/13 (D80), so' sobre o conteudo EMBUTIDO (nada e' lido da pasta do Kimi em rito):
    c1 os quatro artefatos embutidos batem por sha256 e bytes com os pinos do contrato (que o build conferiu contra o HANDOFF e a ORDEM); os seis pinos do build (os quatro + ORDEM + HANDOFF) sao sha256 de 64 hex;
    c2 os 13 IDs exatos: os mesmos no mapa, na validacao (object_checks e coverage_checks, todos verdadeiros) e no manifesto (coverage); c3 as 18 fontes: source_count == len(sources) == 18 == archive_checks (todos verdadeiros); as fontes de cada objeto no mapa == a cobertura do manifesto e todas estao no manifesto;
    c4 os dez campos obrigatorios da ORDEM exatamente, e as bandeiras de fechamento falsas nos tres artefatos (mapa.admission, validacao, manifesto); c5 os estatutos: REAL_DOCUMENTAL__PHYSICS_OPEN no contrato; SOURCES_VALIDATED__COVARIANCE_PHYSICS_OPEN na validacao; os status do mapa e do manifesto == os pinados; o levantamento traz o seu estado;
    c6 a guarda numerica (D80 §5): nos tres JSON nenhum numero fora das chaves permitidas e nenhuma lista numerica; no levantamento nenhuma linha com um vetor de numeros; c7 nenhum dado observado: as bandeiras observed_* falsas no mapa e na validacao; nenhum caminho sob a pasta vedada tocado durante esta mecanica (instrumentado); le_em_rito False;
    c8 a guarda do texto: P18 e a guarda das frases limpas; os tokens proibidos do H0DN ausentes; a frase obrigatoria do HMS/13 e a do H0DN presentes; os nomes vedados de dado observado ausentes do texto e do contrato; c9 o gate identico ao da v409 selada;
    c10 ADITIVO e POSTERIOR ao FREEZE_R2: o registro h0dn_bg1_v410 deste rito selou com o veredito pre-registrado, com os 11 pinos e os 9 do congelamento, e nenhum artefato daqui repete um arquivo do congelamento; c11 a ratificacao do operador: o sha256 do trecho citado == o pinado, o trecho esta' no texto entre « », e o sha256 do arquivo inteiro == o do DESENHO (D80);
    c12 a funcao de veredito do H0DN intocada: o sha256 do texto-fonte de veredito_h0dn neste rito == o que o registro h0dn_bg1_v410 gravou; o HANDOFF em estado HANDOFF_READY__ADDITIVE_DOCUMENTARY_ONLY e a ORDEM com os limites como contrato."""
    import hashlib as _h410, inspect as _insp, json as _j410, os as _os410, re as _re410
    toks_ = ["".join(p_) for p_ in c_["tokens_proibidos_partes"]]; vedados_ = ["".join(p_) for p_ in c_["nomes_vedados_partes"]]
    raw_ = _v410_h0dn_decode(c_, insumos_)   # (o mesmo decodificador do H0DN: base64 -> sha256 e bytes == pino, fail-closed)
    mapa_ = _j410.loads(raw_["MAPA_FONTES_E_COVARIANCIA_13.json"].decode("utf-8")); manif_ = _j410.loads(raw_["MANIFEST_FONTES_PRIMARIAS.json"].decode("utf-8")); valid_ = _j410.loads(raw_["VALIDACAO_FONTES_13.json"].decode("utf-8")); lev_ = raw_["LEVANTAMENTO_FONTES_PRIMARIAS_13.md"].decode("utf-8")
    # ---- c1 os pinos
    pb_ = c_["pinos_build"]
    c1_ok_ = (len(raw_) == len(c_["insumos"]) == 4 and all(_h410.sha256(raw_[k_]).hexdigest() == c_["insumos"][k_]["sha256"] == pb_[k_]["sha256"] and len(raw_[k_]) == c_["insumos"][k_]["bytes"] == pb_[k_]["bytes"] for k_ in c_["insumos"])
              and len(pb_) == 6 and all(isinstance(v_["sha256"], str) and len(v_["sha256"]) == 64 and int(v_["bytes"]) > 0 for v_ in pb_.values()) and c_["handoff"]["sha256"] == pb_["HANDOFF_CLAUDE_UMPY_HMS_13.json"]["sha256"] and c_["ordem"]["sha256"] == pb_["ORDEM_CLAUDE_UMPY_HMS_13.md"]["sha256"] and c_["ordem"]["sha256"][:16] == c_["ordem"]["sha16_do_desenho"]
              and valid_["hashes"]["MAPA_FONTES_E_COVARIANCIA_13.json"] == c_["insumos"]["MAPA_FONTES_E_COVARIANCIA_13.json"]["sha256"] and valid_["hashes"]["fontes_primarias/MANIFEST_FONTES_PRIMARIAS.json"] == c_["insumos"]["MANIFEST_FONTES_PRIMARIAS.json"]["sha256"] and valid_["hashes"]["LEVANTAMENTO_FONTES_PRIMARIAS_13.md"] == c_["insumos"]["LEVANTAMENTO_FONTES_PRIMARIAS_13.md"]["sha256"])
    # ---- c2 os 13 IDs; c3 as 18 fontes
    ids_ = [o_.get("CID") for o_ in mapa_.get("objects") or []]
    c2_ok_ = (len(ids_) == 13 == len(set(ids_)) == c_["campos"]["calibradores"] and sorted(ids_) == sorted(c_["ids_calibradores"]) and set(valid_.get("object_checks") or {}) == set(ids_) and all(valid_["object_checks"].values())
              and set(valid_.get("coverage_checks") or {}) == set(ids_) and all(valid_["coverage_checks"].values()) and set(manif_.get("coverage") or {}) == set(ids_) and valid_["checks"].get("exact_13_ids") is True)
    fontes_ = [s_.get("key") for s_ in manif_.get("sources") or []]
    cob_ok_ = all(set(o_.get("primary_sources") or []) <= set(manif_["coverage"].get(o_.get("CID")) or []) <= set(fontes_) for o_ in mapa_["objects"])   # (mapa ⊆ cobertura do manifesto ⊆ fontes)
    cob_extra_ = {o_.get("CID"): sorted(set(manif_["coverage"].get(o_.get("CID")) or []) - set(o_.get("primary_sources") or [])) for o_ in mapa_["objects"] if set(manif_["coverage"].get(o_.get("CID")) or []) - set(o_.get("primary_sources") or [])}   # (a assimetria MEDIDA no build e' a mesma deste rito)
    statuses_ = sorted({str(s_.get("archive_status")) for s_ in manif_.get("sources") or []})
    c3_ok_ = (manif_.get("source_count") == len(fontes_) == 18 == len(set(fontes_)) == c_["campos"]["fontes_primarias"] and sorted(fontes_) == sorted(c_["fontes_primarias"]) and set(valid_.get("archive_checks") or {}) == set(fontes_) and all(valid_["archive_checks"].values()) and cob_ok_
              and cob_extra_ == {k_: list(v_) for k_, v_ in c_["cobertura_extra_no_manifesto"].items()} and statuses_ == list(c_["archive_statuses"]) and valid_["checks"].get("all_object_source_lists_match_manifest") is True
              and all(isinstance(s_.get("sha256"), str) and len(s_["sha256"]) == 64 and isinstance(s_.get("text_sha256"), str) and len(s_["text_sha256"]) == 64 and s_.get("archive_status") in statuses_ for s_ in manif_["sources"]) and valid_["checks"].get("source_count_18") is True)
    # ---- c4 os dez campos e as bandeiras falsas nos tres; c5 os estatutos
    camp_ = c_["campos"]; adm_ = mapa_.get("admission") or {}
    c4_ok_ = (camp_ == {"estatuto": "REAL_DOCUMENTAL__PHYSICS_OPEN", "fontes_primarias": 18, "calibradores": 13, "partial_components_only": True, "full_13x13_covariance_available": False, "within_SN_full_decomposition_available": False, "physical_covariance_closed": False, "independent_physical_review_complete": False, "full_HMS_admitted": False, "opening_allowed": False}
              and adm_.get("opening_allowed") is False and adm_.get("physical_covariance_closed") is False and adm_.get("full_13x13_covariance_available") is False and adm_.get("within_SN_full_decomposition_available") is False and adm_.get("independent_physical_review_complete") is False and adm_.get("partial_factor_map_available") is True and adm_.get("primary_source_archive_complete") is True
              and mapa_.get("opening_allowed") is False and mapa_.get("full_HMS_admitted") is False and valid_.get("opening_allowed") is False and valid_.get("full_HMS_admitted") is False and valid_.get("physical_covariance_closed") is False and valid_.get("full_13x13_covariance_available") is False and valid_.get("source_archive_complete") is True and valid_.get("all_13_have_primary_sources") is True
              and manif_.get("opening_allowed") is False and manif_.get("physical_covariance_closed") is False and valid_["checks"].get("physical_closure_flags_false") is True and valid_["checks"].get("all_full_covariances_remain_open") is True)
    se_ = c_["status_esperados"]
    c5_ok_ = (camp_["estatuto"] == "REAL_DOCUMENTAL__PHYSICS_OPEN" and valid_.get("status") == se_["validacao"] == "SOURCES_VALIDATED__COVARIANCE_PHYSICS_OPEN" and mapa_.get("status") == se_["mapa"] and manif_.get("status") == se_["manifest"] and se_["levantamento"] in lev_ and lev_.lstrip().startswith("# Levantamento")
              and all(o_.get("covariance_status") == c_["estados_cobertura"].get(o_.get("CID")) and "OPEN_NO_TRANSPLANT" in str(o_.get("covariance_status")) for o_ in mapa_["objects"]) and list(mapa_.get("prohibitions") or []) == list(c_["proibicoes_do_mapa"]))
    # ---- c6 a guarda numerica
    perm_n_ = 0; proib_ = []; arrays_ = []
    for nm_, ob_ in (("MAPA", mapa_), ("MANIFEST", manif_), ("VALIDACAO", valid_)):
        p_, q_, a_ = _v410_hms13_numeros(ob_, tuple(c_["numeros_permitidos"]), tuple(c_["comprimentos_proibidos"])); perm_n_ += len(p_); proib_ += [(nm_,) + x_ for x_ in q_]; arrays_ += [(nm_,) + x_ for x_ in a_]
    vet_md_ = [l_[:80] for l_ in lev_.splitlines() if len(_re410.findall(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w.])", l_)) >= 20]
    c6_ok_ = perm_n_ == int(c_["guarda_numerica_no_build"]["permitidos"]) and not proib_ and not arrays_ and not vet_md_ and c_["guarda_numerica_no_build"]["ok"] is True
    # ---- c7 nenhum dado observado; nada da pasta vedada tocado em rito
    _nrm = lambda p_: _os410.path.normcase(_os410.path.normpath(str(p_)))
    vedada_ = _nrm(c_["pasta_vedada"]); toc_ = sorted({_nrm(p_) for p_ in (tocados_ or [])})
    sob_vedada_ = [p_ for p_ in toc_ if p_.startswith(vedada_ + _os410.sep) or p_ == vedada_]; nomes_vedados_ = [p_ for p_ in toc_ if any(n_.lower() in _os410.path.basename(p_).lower() for n_ in vedados_)]
    c7_ok_ = (mapa_.get("observed_vector_read") is False and mapa_.get("observed_statistics_computed") is False and valid_.get("observed_vector_read_by_validator") is False and valid_.get("observed_statistics_computed") is False and valid_["checks"].get("no_observed_work_flags") is True
              and c_["le_em_rito"] is False and c_["observed_vector_read"] is False and not c_["observed_paths"] and tocados_ is not None and not sob_vedada_ and not nomes_vedados_)
    # ---- c8 a guarda do texto
    txt_json_ = _j410.dumps(t_, ensure_ascii=False); frases_ = list(_v410_guarda_frases(txt_json_)); p18_ = list(_v392_guarda_texto(txt_json_)); ctr_json_ = _j410.dumps({k_: v_ for k_, v_ in c_.items() if k_ not in ("nomes_vedados_partes", "tokens_proibidos_partes")}, ensure_ascii=False)
    c8_partes_ = {"guarda_das_frases_limpa": not frases_, "p18_limpa": not p18_, "tokens_proibidos_ausentes_do_texto": not any(tk_ in txt_json_ for tk_ in toks_), "tokens_proibidos_ausentes_do_veredito": not any(tk_ in c_["veredito_ok"] for tk_ in toks_),
                  "frase_obrigatoria_pt_presente": c_["frase_obrigatoria_pt"] in txt_json_, "frase_obrigatoria_en_presente": c_["frase_obrigatoria_en"] in txt_json_, "obrigacao_h0dn_presente": "pré-registrado; nenhum dado observado lido" in txt_json_,
                  "nomes_vedados_ausentes_do_texto": not any(n_ in txt_json_ for n_ in vedados_), "nomes_vedados_ausentes_do_contrato": not any(n_ in ctr_json_ for n_ in vedados_), "veredito_sem_a_palavra_do_livro": "NOT_FALSIFIED" not in c_["veredito_ok"]}
    c8_ok_ = all(c8_partes_.values())
    # ---- c9 o gate
    gate_ = ((core_.get("qg_closure") or {}).get("gate") or {}).get("verdict")
    c9_ok_ = isinstance(gate_, str) and gate_ == c_["baseline"]["gate_verdict"]
    # ---- c10 aditivo e posterior ao FREEZE_R2
    h_ = core_.get("h0dn_bg1_v410") or {}; hv_ = h_.get("values") or {}
    c10_ok_ = (h_.get("all_verified") is True and h_.get("verdict") == c_["h0dn"]["veredito_ok"] and hv_.get("n_pinos") == c_["h0dn"]["n_pinos"] == 11 and hv_.get("n_pinos_freeze") == c_["h0dn"]["n_pinos_freeze"] == 9 and h_.get("observed_vector_read") is False
               and ((h_.get("insumos_pinados") or {}).get("FREEZE_R2.json") or {}).get("sha256") == c_["h0dn"]["freeze_r2_sha256"] and not (set(pb_) & set(c_["h0dn"]["freeze_r2_arquivos"])) and c_["aditivo_posterior_ao_freeze_r2"] is True)
    # ---- c11 a ratificacao do operador
    r_ = c_["ratificacao"]
    c11_ok_ = (_h410.sha256(r_["trecho"].encode("utf-8")).hexdigest() == r_["sha256_do_trecho"] and ("«" + r_["trecho"] + "»") in txt_json_ and isinstance(r_["sha256"], str) and len(r_["sha256"]) == 64 and r_.get("aponta_o_handoff") is True and r_.get("autor") == "operador" and "vibrato" not in txt_json_.lower() and "vibrato" not in ctr_json_.lower())   # (o nome do arquivo da fala resume a cunhagem que nao entra por este registro: nao se cita)
    # ---- c12 a funcao de veredito do H0DN intocada; o HANDOFF e a ORDEM
    fonte_sha_ = _h410.sha256(_insp.getsource(veredito_h0dn).encode("utf-8")).hexdigest()
    c12_ok_ = (fonte_sha_ == h_.get("veredito_h0dn_source_sha256") and c_["handoff"]["status"].startswith("HANDOFF_READY__ADDITIVE_DOCUMENTARY_ONLY") and "OPENING_NOT_ALLOWED" in c_["handoff"]["status"] and c_["handoff"]["rehash_required_immediately_before_build"] is True and c_["ordem"]["limites_valem_como_contrato"] is True
               and set(c_["pergunta_nas_quatro_linguas"]) == {"tgl", "teologica", "linguistica", "juridica"})
    checks_ = [
        {"id": "c1", "descricao": "os 4 artefatos documentais embutidos (mapa, manifesto, validacao, levantamento) batem por sha256 e bytes com os pinos do contrato, que o build conferiu contra o HANDOFF e a ORDEM do Kimi (6 pinos: os 4 mais ORDEM e HANDOFF); a validacao pina os mesmos artefatos", "ok": bool(c1_ok_)},
        {"id": "c2", "descricao": "os 13 IDs dos calibradores sao exatamente os mesmos no mapa, na validacao (object_checks e coverage_checks, todos verdadeiros) e no manifesto", "ok": bool(c2_ok_)},
        {"id": "c3", "descricao": "as 18 fontes primarias: source_count == len(sources) == archive_checks (todos verdadeiros); as fontes de cada objeto no mapa ⊆ a cobertura do manifesto ⊆ as fontes, com a cobertura extra do manifesto igual a' medida no build (%s); os estados de arquivo pinados (%s); cada fonte com sha256 do arquivo e do texto" % (cob_extra_ or "nenhuma", ", ".join(statuses_)), "ok": bool(c3_ok_)},
        {"id": "c4", "descricao": "os dez campos obrigatorios da ORDEM (§3.7) exatamente, e as bandeiras de fechamento FALSAS nos tres artefatos (admissao do mapa, validacao, manifesto); partial_components_only verdadeiro", "ok": bool(c4_ok_)},
        {"id": "c5", "descricao": "os estatutos: REAL_DOCUMENTAL__PHYSICS_OPEN; SOURCES_VALIDATED__COVARIANCE_PHYSICS_OPEN; os status do mapa e do manifesto pinados; o levantamento com o seu estado; todo calibrador OPEN_NO_TRANSPLANT; as proibicoes do mapa pinadas", "ok": bool(c5_ok_)},
        {"id": "c6", "descricao": "a guarda numerica (D80 §5): %d numeros nos tres JSON, todos em chaves permitidas (%s); nenhum proibido; nenhuma lista numerica (255 ou 64 inclusive); nenhuma linha do levantamento com vetor de numeros" % (perm_n_, ", ".join(c_["numeros_permitidos"])), "ok": bool(c6_ok_)},
        {"id": "c7", "descricao": "nenhum dado observado: as bandeiras observed_* falsas no mapa e na validacao; %d caminhos tocados durante esta mecanica (instrumentados), nenhum sob a pasta vedada (a entrega do Kimi) nem com nome vedado; nada e' lido em rito" % len(toc_), "ok": bool(c7_ok_)},
        {"id": "c8", "descricao": "a guarda do texto: P18 e a guarda das frases (v405 -> v410) limpas; os tokens proibidos do H0DN ausentes; a frase obrigatoria do HMS/13 (%s) e a do H0DN presentes; nenhum nome vedado de dado observado no texto nem no contrato" % c_["frase_obrigatoria_pt"], "ok": bool(c8_ok_)},
        {"id": "c9", "descricao": "o veredito do gate deste rito e' IDENTICO ao da v409 selada (congelado no contrato): o gate nao se move", "ok": bool(c9_ok_)},
        {"id": "c10", "descricao": "ADITIVO e POSTERIOR ao FREEZE_R2: o registro h0dn_bg1_v410 deste rito selou com o veredito pre-registrado, os 11 pinos e os 9 do congelamento; o FREEZE_R2 pinado e' o mesmo; nenhum artefato daqui repete um arquivo do congelamento", "ok": bool(c10_ok_)},
        {"id": "c11", "descricao": "a ratificacao do operador (09/11): o sha256 do trecho citado == o pinado; o trecho esta' no texto entre « »; o arquivo inteiro entra por sha256 (o do DESENHO, D80); so' a frase final, que aponta o HANDOFF; a cunhagem anterior nao entra por este registro (D82: a pedra nova, parte 2); o nome do arquivo da fala nao e' citado", "ok": bool(c11_ok_)},
        {"id": "c12", "descricao": "a funcao de veredito do H0DN intocada (o sha256 do texto-fonte de veredito_h0dn neste rito == o gravado pelo registro h0dn_bg1_v410); o HANDOFF em HANDOFF_READY__ADDITIVE_DOCUMENTARY_ONLY (abertura nao permitida; rehash obrigatorio antes do build); a ORDEM com os limites como contrato; a pergunta nas quatro linguas", "ok": bool(c12_ok_)},
    ]
    values_ = {"ids_calibradores": ids_, "n_calibradores": len(ids_), "fontes_primarias": fontes_, "n_fontes_primarias": len(fontes_), "cobertura": {k_: list(v_) for k_, v_ in (manif_.get("coverage") or {}).items()}, "cobertura_extra_no_manifesto": cob_extra_, "archive_statuses": statuses_, "estados_cobertura": {o_.get("CID"): o_.get("covariance_status") for o_ in mapa_["objects"]},
               "campos": dict(camp_), "status": {"mapa": mapa_.get("status"), "manifest": manif_.get("status"), "validacao": valid_.get("status")}, "numeros": {"permitidos": perm_n_, "proibidos": proib_, "listas_numericas": arrays_, "linhas_do_levantamento_com_vetor": vet_md_},
               "pinos": {k_: {"sha256_ok": _h410.sha256(raw_[k_]).hexdigest() == v_["sha256"], "bytes_ok": len(raw_[k_]) == v_["bytes"], "embutido": True} for k_, v_ in c_["insumos"].items()}, "pinos_build_n": len(pb_), "n_embutidos": len(raw_), "gate_verdict": gate_,
               "veredito_h0dn_source_sha256": fonte_sha_, "h0dn_selado": h_.get("all_verified"), "freeze_r2_sha256": c_["h0dn"]["freeze_r2_sha256"], "ratificacao_sha256": r_["sha256"], "ratificacao_trecho": r_["trecho"],
               "observed_vector_read": False, "le_em_rito": False, "caminhos_tocados": toc_, "n_caminhos_tocados": len(toc_), "sob_pasta_vedada": sob_vedada_, "com_nome_vedado": nomes_vedados_, "pasta_vedada": c_["pasta_vedada"], "p18_violacoes": p18_[:5], "frases_violacoes": frases_[:5], "c8_partes": c8_partes_,
               "estruturas_compartilhadas": sorted(mapa_.get("shared_structures") or {}), "n_linhas_levantamento": lev_.count("\n") + 1}
    return {"passed": all(x_["ok"] for x_ in checks_), "n_checks": len(checks_), "checks": checks_, "values": values_}


_V410_HMS13_RECUSA = "TGL_H0DN_FONTES_HMS13_V410__REFUSED_%s__GATE_UNMOVED"


def h0dn_fontes_hms13_v410(core):
    """v410 -- H0DN FONTES HMS/13 (D80; a ordem do operador de 09/11/2026, ratificada por sha256: «o kimi fezz o trabalho e já te entregou» + o caminho do HANDOFF): o recibo DOCUMENTAL das 18 fontes primarias dos 13 calibradores, ADITIVO e POSTERIOR ao FREEZE_R2,
    lido no PONTO REAL do main, LOGO DEPOIS de h0dn_bg1_v410 (na mesma instrucao). Cobertura documental de fontes, não covariância física fechada; nada aberto: os quatro artefatos embutidos e pinados por sha256 (lidos no build; nada lido em rito), os 13 IDs, as 18 fontes,
    os dez campos da ORDEM, a guarda numerica, o gate, a posterioridade ao FREEZE_R2, a ratificacao, a funcao de veredito do H0DN intocada. Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate. H0DN x BG1: pré-registrado; nenhum dado observado lido."""
    c_ = _V410_HMS13_CONTRACT; t_ = _V410_HMS13_TEXT; i_ = _V410_HMS13_INSUMOS
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)   # (beta entra so' por nome: o registro e' documental)
    out_ = {"all_verified": False, "runtime_executed": False, "does_not_gate_core": True, "observed_vector_read": False, "le_em_rito": False, "estatuto": t_["estatuto"], "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"],
            "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "campos": dict(c_["campos"]), "n_checks_esperadas": c_["n_checks"], "insumos_pinados": {k_: dict(v_) for k_, v_ in c_["insumos"].items()}, "pinos_build": {k_: dict(v_) for k_, v_ in c_["pinos_build"].items()},
            "cadeia_de_autoridade": list(c_["cadeia_de_autoridade"]), "ratificacao": {k_: v_ for k_, v_ in c_["ratificacao"].items() if k_ != "arquivo"}, "handoff": dict(c_["handoff"]), "ordem": dict(c_["ordem"]), "pergunta_nas_quatro_linguas": dict(c_["pergunta_nas_quatro_linguas"]), "o_que_falta": list(t_["o_que_falta"]), "ressalvas": list(t_["ressalvas"]),
            "aditivo_posterior_ao_freeze_r2": c_["aditivo_posterior_ao_freeze_r2"]}
    out_.update(t_["extras"])
    if not beta_ok_:
        out_["verdict"] = _V410_HMS13_RECUSA % "BETA_IS_NOT_ALPHA_SQRT_E"
    else:
        try:
            tocados_, restaura_ = _v410_h0dn_vigia_arquivos()   # (D80: nenhum arquivo da pasta do Kimi e' aberto em rito; a c7 o mede)
            try:
                mec_ = _v410_hms13_mechanics(core, c_, t_, i_, tocados_)
            finally:
                restaura_()
            out_.update(runtime_executed=True, mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], all_verified=bool(mec_["passed"] and mec_["n_checks"] == c_["n_checks"]))
            out_["verdict"] = (c_["veredito_ok"] if out_["all_verified"] else _V410_HMS13_RECUSA % "MECHANICS_CHECK_FAILED")
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V410_HMS13_RECUSA % "RUNTIME_ERROR"
    core["h0dn_fontes_hms13_v410"] = out_
    return out_
