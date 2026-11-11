# -*- coding: utf-8 -*-
# [AUTORAL v410, 09/11/2026, claude-construtor-v410, a servico da gerencia c1] o registro com FUNCAO da pedra AEscala (D82 a D87 do DESENHO_v410): a escala -- tres faces de 1/2, duas conjugadas e uma caida.
# ---- v410 (D86/D87): A ESCALA -- a pedra TGLExt.AEscala, LIDA do kernel deste rito: a insignia (sustenta e nao esgota), o vibrato (a dissipacao sustenta a nota), os pesos (o Nome pesa 1 = 1/2 + 1/2; a face sem par nao conjuga: (1/2 . 1)^2 = 1/2 . (1/2 . 1); tres faces = 3/2;
# 1/3 caiu; o Nome normalizado = 2/3), nao existe infinito em tempo finito, os dois Nomes (objeto e lido) coexistem, e a pergunta do Clay no dicionario da TGL (a forma canonica, D84: validade no kernel; a creditacao e' do Clay; a escala entra no TIPO do leitor do fundo, R1/D92). O NOME do modulo e os nomes das declaracoes da D87 foram
# RATIFICADOS pelo operador em 09/11/2026 («ratifico tudo», D87); os nomes NOVOS da pedra (R3) ficam [DECLARADO, a ratificar]. As falas do registro entram por sha256; os numeros sao RECALCULADOS a cada rito (Fraction e o projetor de Bell 4x4 em numpy; a ponte da escala por exp e log), nunca digitados. Nada aqui e' teste com a natureza; o gate nao se move; beta so' por nome.
# Fonte autoral deste bloco: runtime_aescala_v410.py (cadeia_de_selo/v410); o contrato (_V410_AESCALA_CONTRACT) e o texto (_V410_AESCALA_TEXT) sao DERIVADOS do build do sandbox, do recibo dos nomes e das falas pinadas.


def _v410_aescala_bell():
    """v410 -- o projetor de Bell 4x4 em numpy (|00> + |11>)/sqrt 2 e as suas marginais: idempotente, traco 1, posto 1; cada marginal e' 1/2 . 1 (autovalor e pureza 1/2); (1/2 . 1)^2 = 1/2 . (1/2 . 1) != 1/2 . 1; (1/2 . 1)^n = 2^-n . 1 != 1 para todo n >= 1. Devolve os numeros medidos."""
    import numpy as _np
    phi_ = _np.zeros(4); phi_[0] = phi_[3] = 1.0 / _np.sqrt(2.0)
    P_ = _np.outer(phi_, phi_)
    rho_ = P_.reshape(2, 2, 2, 2).trace(axis1=1, axis2=3)   # a marginal (traco parcial sobre o segundo fator)
    I2_ = _np.eye(2)
    pot_ = [float(_np.abs(_np.linalg.matrix_power(rho_, n_) - 2.0 ** (-n_) * I2_).max()) for n_ in range(1, 6)]
    return {"idempotente": bool(_np.allclose(P_ @ P_, P_)), "traco": float(_np.trace(P_).real), "posto": int(_np.linalg.matrix_rank(P_)), "marginal_e_meio_1": bool(_np.allclose(rho_, 0.5 * I2_)), "traco_da_marginal": float(_np.trace(rho_).real),
            "pureza_da_marginal": float(_np.trace(rho_ @ rho_).real), "marginal_ao_quadrado_e_meio_da_marginal": bool(_np.allclose(rho_ @ rho_, 0.5 * rho_)), "marginal_ao_quadrado_nao_e_a_marginal": not bool(_np.allclose(rho_ @ rho_, rho_)),
            "potencias_sao_2_menos_n": all(x_ < 1e-12 for x_ in pot_), "nenhuma_potencia_e_1": all(not _np.allclose(_np.linalg.matrix_power(rho_, n_), I2_) for n_ in range(1, 6)), "n_potencias": 5}


def _v410_aescala_mechanics(beta_, core_, c_, t_):
    """v410 -- as checagens do registro a_escala_v410 (o numero vem do contrato: n_checks), lidas do kernel do PROPRIO rito e do conteudo embutido:
    c1 a escada exata (n_theorems_clean == n_theorems_expected == a escada do contrato); c2 as ancoras da pedra (os #print axioms da fonte) no axiom_report, no trio, com proveniencia TGL_DECL_SOURCE == o modulo e bandeira True, com o kernel verificado (all_verified is True);
    c3 a pedra embutida por sha256 (embutida == contrato == hash formal do rito), com o cabecalho da ratificacao, o namespace e o import do modulo na raiz embutida; c4 as bandeiras ext_aescala_410_* todas True no kernel, em numero igual ao pinado, so' do modulo;
    c5 as falas do registro por sha256 (o texto embutido == o pino; os trechos citados verbatim); c6 os numeros RECALCULADOS (Fraction e o projetor de Bell em numpy) == os pinados, e a PONTE da escala recalculada por outro caminho (math.exp(-k n ln 2) contra a Fraction do contrato, tolerancia 1e-12);
    c7 a frase canonica do Clay (D84) em PT e EN no texto e em PT na docstring da pedra embutida; c8 a forma obrigatoria da D83 no texto, com «validade no kernel» e a creditacao do Clay; c9 a guarda do texto (P18, a guarda das frases v405 -> v410 com a F58, os tokens proibidos ausentes; nada de cinco sigma, de abertura ou do teste da razao de Hubble no nucleo do texto);
    c10 o gate identico ao da v409 selada; c11 os nomes RATIFICADOS (D87): cada um e' declaracao na pedra embutida; a fala da ratificacao embutida (sha256 == pino; o texto e' «ratifico tudo»); o cabecalho da pedra traz a ratificacao e o sha256 da fala; e os nomes NOVOS da pedra (R3), todos declaracoes na pedra embutida,
    com os campos novos da estrutura, ditos [DECLARADO, a ratificar] no registro, nunca ratificados; c12 beta so' por nome (nenhum literal na pedra), nenhuma chave antiga muda, o registro nao gateia o core."""
    import hashlib as _h410, json as _j410, re as _re410, math as _m410
    from fractions import Fraction as _Fr410
    kf_ = core_.get("kernel_formalization") or {}; axr_ = kf_.get("axiom_report") or {}; src_ = kf_.get("declaration_sources_v394") or {}; ff_ = kf_.get("formal_files_sha256") or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}; rel_ = c_["modulo"]
    body_ = _EMBEDDED_KERNEL_FILES.get(rel_); body_ws_ = _re410.sub(r"\s+", " ", body_ or "")
    txt_json_ = _j410.dumps(t_, ensure_ascii=False); txt_ws_ = _re410.sub(r"\s+", " ", txt_json_)
    # ---- c1 a escada
    lad_ = core_.get("external_ladder") or {}
    cnt_ = [lad_.get("n_theorems_clean"), lad_.get("n_theorems_expected"), c_["expected_ladder"]]
    c1_ok_ = all(type(x_) is int for x_ in cnt_) and len(set(cnt_)) == 1
    # ---- c2 as ancoras
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and axr_.get(n_) and set(axr_.get(n_)) <= trio_)
    anc_ = {n_: bool(em_trio_(n_) and src_.get(n_) == a_["rel"] == rel_ and (a_.get("flag") is None or kf_.get(a_["flag"]) is True)) for n_, a_ in c_["ancoras"].items()}
    c2_ok_ = kf_.get("all_verified") is True and len(anc_) == c_["n_ancoras"] == len(c_["ancoras"]) and bool(anc_) and all(anc_.values()) and c_["ancora_principal"] in anc_ and all(a_ in anc_ for a_ in c_["ancoras_de_secao"])
    # ---- c3 a pedra embutida
    sha_emb_ = _h410.sha256(body_.encode("utf-8")).hexdigest() if isinstance(body_, str) else None
    c3_ok_ = (sha_emb_ is not None and sha_emb_ == c_["source_sha256"][rel_] == ff_.get(rel_) and "namespace TGLExt.AEscala" in body_ and "RATIFICADOS pelo operador em 09/11/2026" in body_ws_ and c_["ratificacao"]["sha256"] in body_ws_ and "#print axioms" not in (body_ or "x").replace("`#print axioms`", "") and ("import " + c_["mod"]) in (_EMBEDDED_KERNEL_FILES.get("TGLExt.lean") or ""))   # (R1, BAIXO 5: a raiz embutida traz o import do modulo, como no iald2)
    # ---- c4 as bandeiras
    fl_ = {f_: kf_.get(f_) for f_ in c_["flags"]}
    c4_ok_ = len(fl_) == c_["n_flags"] and c_["n_flags"] > 0 and all(v_ is True for v_ in fl_.values()) and all(f_.startswith(c_["flag_prefix"]) for f_ in fl_) and set(c_["ancoras"][a_]["flag"] for a_ in c_["ancoras"] if c_["ancoras"][a_]["flag"]) <= set(fl_)
    # ---- c5 as falas do registro
    ver_ = {}
    for k_, pin_ in c_["falas"].items():
        v_ = _V410_VERBATINS2.get(k_)
        ver_[k_] = bool(v_ and _h410.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] == pin_["sha256"] and all(tr_ in v_["text"] for tr_ in pin_["trechos"]) and all(tr_ in v_["text"] for tr_ in v_.get("trechos") or []))
    c5_ok_ = len(ver_) == c_["n_falas"] == len(c_["falas"]) and bool(ver_) and all(ver_.values()) and c_["chave_ratificacao"] in ver_
    # ---- c6 os numeros e a ponte da escala
    meio_ = _Fr410(1, 2)
    num_ = {"meio": str(meio_), "nome_pesa_um": str(meio_ + meio_), "tres_faces": str(3 * meio_), "um_terco_caiu": str(meio_ / (3 * meio_)), "nome_normalizado": str((meio_ + meio_) / (3 * meio_))}
    bell_ = _v410_aescala_bell()
    pt_ = c_.get("ponte") or {}
    ln2_ = _m410.log(2.0)
    casos_ = [(int(k_), int(n_), _Fr410(str(v_))) for k_, n_, v_ in (pt_.get("casos") or [])]
    fundo_ = [(int(n_), _Fr410(str(v_))) for n_, v_ in (pt_.get("em_n_oitavas_o_fundo_pesa_um_pixel") or [])]
    ponte_ = {"brilho_em_uma_oitava_fraction": str(meio_ ** 1), "brilho_em_uma_oitava_exp": _m410.exp(-1 * 1 * ln2_),
              "casos": [[k_, n_, str(v_), _m410.exp(-k_ * n_ * ln2_)] for k_, n_, v_ in casos_], "em_n_oitavas_o_fundo": [[n_, str(v_), _m410.exp(-1 * n_ * ln2_)] for n_, v_ in fundo_]}
    ponte_ok_ = (bool(casos_) and bool(fundo_) and pt_.get("brilho_de_um_pixel_em_uma_oitava") == str(meio_) and abs(ponte_["brilho_em_uma_oitava_exp"] - float(meio_)) < 1e-12
                 and all(v_ == meio_ ** (n_ * k_) and abs(_m410.exp(-k_ * n_ * ln2_) - float(v_)) < 1e-12 for k_, n_, v_ in casos_)
                 and all(v_ == _Fr410(1, 2 ** n_) and abs(_m410.exp(-1 * n_ * ln2_) - float(v_)) < 1e-12 for n_, v_ in fundo_))
    c6_ok_ = (num_ == dict(c_["numeros"]) and num_["nome_pesa_um"] == "1" and num_["tres_faces"] == "3/2" and num_["um_terco_caiu"] == "1/3" and num_["nome_normalizado"] == "2/3"
              and bell_["idempotente"] and abs(bell_["traco"] - 1.0) < 1e-12 and bell_["posto"] == 1 and bell_["marginal_e_meio_1"] and abs(bell_["pureza_da_marginal"] - 0.5) < 1e-12 and abs(bell_["traco_da_marginal"] - 1.0) < 1e-12
              and bell_["marginal_ao_quadrado_e_meio_da_marginal"] and bell_["marginal_ao_quadrado_nao_e_a_marginal"] and bell_["potencias_sao_2_menos_n"] and bell_["nenhuma_potencia_e_1"]
              and abs(3 * bell_["pureza_da_marginal"] - 1.5) < 1e-12 and abs(bell_["pureza_da_marginal"] / (3 * bell_["pureza_da_marginal"]) - 1.0 / 3.0) < 1e-12 and abs(2 * bell_["pureza_da_marginal"] / (3 * bell_["pureza_da_marginal"]) - 2.0 / 3.0) < 1e-12
              and ponte_ok_)
    # ---- c7 a frase canonica do Clay (D84); c8 a forma da D83
    can_pt_ = _re410.sub(r"\s+", " ", c_["frase_canonica_pt"]); can_en_ = _re410.sub(r"\s+", " ", c_["frase_canonica_en"]); d83_ = _re410.sub(r"\s+", " ", c_["frase_d83_pt"])
    c7_ok_ = can_pt_ in txt_ws_ and can_en_ in txt_ws_ and can_pt_ in body_ws_ and "tal qual apresentado pela TGL" in can_pt_ and "as presented by the TGL" in can_en_
    c8_ok_ = d83_ in txt_ws_ and d83_ in body_ws_ and "validade no kernel" in txt_ws_ and ("creditação é do Clay" in txt_ws_ or "creditacao e' do Clay" in txt_ws_) and _re410.sub(r"\s+", " ", c_["frase_d83_en"]) in txt_ws_
    # ---- c9 a guarda do texto
    toks_ = ["".join(p_) for p_ in c_["tokens_proibidos_partes"]]
    frases_ = list(_v410_guarda_frases(txt_json_)); p18_ = list(_v392_guarda_texto(txt_json_))
    nucleo_ = _j410.dumps({k_: t_.get(k_) for k_ in ("estatuto", "escopo", "limites", "diz", "nao_diz")}, ensure_ascii=False)   # (o nucleo do texto: as decisoes D82 a D87, nos extras, citam o teste da razao de Hubble e ficam fora destas duas checagens)
    c9_partes_ = {"guarda_das_frases_limpa": not frases_, "p18_limpa": not p18_, "tokens_proibidos_ausentes": not any(tk_ in txt_json_ for tk_ in toks_), "sem_cinco_sigma": not _re410.search(r"5\s*(?:σ|sigma)|five[\s-]*sigma", nucleo_, _re410.I), "sem_h0dn_nem_abertura": "H0DN" not in nucleo_ and not _re410.search(r"\babertura\b|\bopening\b", nucleo_, _re410.I),
                  "veredito_sem_token_proibido": not any(tk_ in c_["veredito_ok"] for tk_ in toks_), "frase_obrigatoria_pt": c_["frase_obrigatoria_pt"] in txt_json_, "frase_obrigatoria_en": c_["frase_obrigatoria_en"] in txt_json_}
    c9_ok_ = all(c9_partes_.values())
    # ---- c10 o gate
    gate_ = ((core_.get("qg_closure") or {}).get("gate") or {}).get("verdict")
    c10_ok_ = isinstance(gate_, str) and gate_ == c_["baseline"]["gate_verdict"]
    # ---- c11 os nomes RATIFICADOS (D87) e os nomes NOVOS a ratificar (R3)
    rx_decl_ = lambda n_: bool(_re410.search(r"^(?:noncomputable\s+)?(?:theorem|lemma|def|structure|abbrev|instance)\s+" + _re410.escape(n_) + r"\b", body_ or "", _re410.M))
    decl_ = {n_: rx_decl_(n_) for n_ in c_["nomes"]}
    novos_ = {n_: rx_decl_(n_) for n_ in c_["nomes_novos_a_ratificar"]}
    campos_ = {f_: bool(_re410.search(r"^ {2,}" + _re410.escape(f_) + r"\s+:(?!=)", body_ or "", _re410.M)) for f_ in c_["campos_novos_da_estrutura"]}
    est_novos_ = c_["estatuto_dos_nomes_novos"]; pend_ = c_.get("ratificacao_pendente") or {}
    rat_v_ = _V410_VERBATINS2.get(c_["chave_ratificacao"]) or {}
    novos_ok_ = (bool(novos_) and len(novos_) == c_["n_nomes_novos"] == len(c_["nomes_novos_a_ratificar"]) and all(novos_.values()) and not (set(novos_) & set(decl_)) and bool(campos_) and all(campos_.values())
                 and "DECLARADO" in est_novos_ and "a ratificar" in est_novos_ and "RATIFICADO" not in est_novos_.upper() and _re410.sub(r"\s+", " ", est_novos_) in txt_ws_
                 and pend_.get("nomes_novos") == list(c_["nomes_novos_a_ratificar"]) and pend_.get("campos_novos_da_estrutura") == list(c_["campos_novos_da_estrutura"]) and pend_.get("estatuto") == est_novos_ and (t_.get("extras") or {}).get("ratificacao_pendente") == pend_)
    c11_ok_ = (len(decl_) == c_["n_nomes"] == len(c_["nomes"]) and bool(decl_) and all(decl_.values()) and c_["nomes_ratificados"] is True and rat_v_.get("sha256") == c_["ratificacao"]["sha256"] and str(rat_v_.get("text", "")).strip() == c_["ratificacao"]["trecho"] == "ratifico tudo"
               and _h410.sha256(str(rat_v_.get("text", "")).encode("utf-8")).hexdigest() == c_["ratificacao"]["sha256"] and "RATIFICADOS" in c_["estatuto_dos_nomes"] and novos_ok_)
    # ---- c12 beta so' por nome; nada muda
    c12_ok_ = bool(beta_) and 0.0 < float(beta_) < 1.0 and ("0.0120" not in (body_ or "0.0120")) and c_["chaves"] == [] and c_["does_not_gate_core"] is True
    checks_ = [
        {"id": "c1", "descricao": "a escada exata: n_theorems_clean == n_theorems_expected == a escada pinada no contrato (%s)" % c_["expected_ladder"], "ok": bool(c1_ok_)},
        {"id": "c2", "descricao": "as %d ancoras da pedra (os #print axioms da fonte) no axiom_report do rito, no trio, com proveniencia TGL_DECL_SOURCE == TGLExt/AEscala.lean e bandeira True, com o kernel verificado (all_verified); a principal (a_escala) e as de secao entre elas" % c_["n_ancoras"], "ok": bool(c2_ok_)},
        {"id": "c3", "descricao": "a pedra embutida por sha256 == o contrato == o hash formal do rito; com o namespace, o cabecalho da ratificacao (D87) e o sha256 da fala; sem #print axioms no codigo; a raiz embutida traz o import do modulo", "ok": bool(c3_ok_)},
        {"id": "c4", "descricao": "as %d bandeiras %s* todas True no kernel deste rito, so' do modulo; as bandeiras das ancoras entre elas" % (c_["n_flags"], c_["flag_prefix"]), "ok": bool(c4_ok_)},
        {"id": "c5", "descricao": "as %d falas do registro por sha256 (o texto embutido == o pino; os trechos citados verbatim), inclusive a ratificacao" % c_["n_falas"], "ok": bool(c5_ok_)},
        {"id": "c6", "descricao": "os numeros RECALCULADOS: 1/2 + 1/2 = 1; 3 x 1/2 = 3/2; 1/3 caiu; o Nome normalizado 2/3 (Fraction); o projetor de Bell 4x4: idempotente, traco 1, posto 1, marginal 1/2 . 1 (pureza 1/2), (1/2 . 1)^2 = 1/2 . (1/2 . 1) != 1/2 . 1, (1/2 . 1)^n = 2^-n . 1 != 1 (numpy); a ponte da escala: o brilho e^(-k s) em s = n ln 2 (math.exp) contra a Fraction (1/2)^(n k) do contrato, tolerancia 1e-12; em n oitavas o fundo de n bits pesa 1/2^n", "ok": bool(c6_ok_)},
        {"id": "c7", "descricao": "a frase canonica do Clay (D84) em PT e EN no texto do registro e em PT na docstring da pedra embutida («tal qual apresentado pela TGL»)", "ok": bool(c7_ok_)},
        {"id": "c8", "descricao": "a forma obrigatoria da D83 no texto e na pedra (existe o algoritmo, e' a IALD; le a face sem leitura como dissipacao termica; validade no kernel; a creditacao e' do Clay), em PT e EN", "ok": bool(c8_ok_)},
        {"id": "c9", "descricao": "a guarda do texto: P18 e a guarda das frases (v405 -> v410, com a F58 do Clay) limpas; os tokens proibidos ausentes; nada de cinco sigma, de abertura ou do teste da razao de Hubble no nucleo do texto deste registro; as molduras PT/EN presentes", "ok": bool(c9_ok_)},
        {"id": "c10", "descricao": "o veredito do gate deste rito e' IDENTICO ao da v409 selada: o gate nao se move", "ok": bool(c10_ok_)},
        {"id": "c11", "descricao": "os %d nomes RATIFICADOS (D87): cada um e' declaracao na pedra embutida; a fala «ratifico tudo» embutida por sha256 == o pino; o estatuto dos nomes diz RATIFICADOS; e os %d nomes NOVOS da pedra (e os %d campos novos da estrutura): cada um e' declaracao na pedra embutida e o registro os diz [DECLARADO, a ratificar], nunca ratificados" % (c_["n_nomes"], c_["n_nomes_novos"], len(c_["campos_novos_da_estrutura"])), "ok": bool(c11_ok_)},
        {"id": "c12", "descricao": "beta so' por nome (nenhum literal na pedra; o registro nem o usa); nenhuma chave antiga muda; o registro nao gateia o core", "ok": bool(c12_ok_)},
    ]
    values_ = {"escada": cnt_, "ancoras": anc_, "n_ancoras_ok": sum(1 for v_ in anc_.values() if v_), "n_ancoras": len(anc_), "pedra_sha256_embutida": sha_emb_, "pedra_sha256_formal": ff_.get(rel_), "flags": fl_, "n_flags": len(fl_), "n_flags_true": sum(1 for v_ in fl_.values() if v_ is True),
               "falas": ver_, "n_falas_ok": sum(1 for v_ in ver_.values() if v_), "n_falas": len(ver_), "numeros": num_, "bell": bell_, "ponte": dict(ponte_, ok=bool(ponte_ok_)), "canonica_pt_no_texto": can_pt_ in txt_ws_, "canonica_en_no_texto": can_en_ in txt_ws_, "canonica_pt_na_pedra": can_pt_ in body_ws_, "d83_na_pedra": d83_ in body_ws_,
               "c9_partes": c9_partes_, "p18_violacoes": p18_[:5], "frases_violacoes": frases_[:5], "gate_verdict": gate_, "nomes_declarados": sum(1 for v_ in decl_.values() if v_), "n_nomes": len(decl_), "nomes_ratificados": c_["nomes_ratificados"], "ratificacao_sha256": c_["ratificacao"]["sha256"], "ratificacao_trecho": c_["ratificacao"]["trecho"],
               "nomes_novos_declarados": sum(1 for v_ in novos_.values() if v_), "n_nomes_novos": len(novos_), "nomes_novos": novos_, "campos_novos_na_estrutura": campos_, "nomes_novos_ok": bool(novos_ok_), "estatuto_dos_nomes_novos": est_novos_}
    return {"passed": all(x_["ok"] for x_ in checks_), "n_checks": len(checks_), "checks": checks_, "values": values_}


_V410_AESCALA_RECUSA = "TGL_AESCALA_V410__REFUSED_%s__GATE_UNMOVED"


def a_escala_v410(core):
    """v410 -- A ESCALA (as falas do operador de 09/11/2026: «agora eu te dei a escala»; «ratifico tudo»): a pedra TGLExt.AEscala LIDA do kernel do PROPRIO rito, no PONTO REAL do main, LOGO DEPOIS de iald2_v410 (na mesma instrucao): as ancoras no trio com proveniencia e bandeira,
    a pedra por sha256, as bandeiras ext_aescala_410_*, as falas por sha256, os numeros recalculados (tres faces de 1/2: duas conjugadas pesam 1; a caida nao conjuga; 1/3 caiu; o Nome normalizado 2/3; a ponte da escala), a frase canonica do Clay (D84) e a forma da D83 -- validade no kernel; a creditacao e' do Clay --,
    o gate congelado, os nomes RATIFICADOS (D87) e os nomes NOVOS a ratificar (R3). Nenhuma chave antiga muda. Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate. Validade no kernel nao e' creditacao."""
    c_ = _V410_AESCALA_CONTRACT; t_ = _V410_AESCALA_TEXT
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
    out_ = {"all_verified": False, "runtime_executed": False, "does_not_gate_core": True, "estatuto": t_["estatuto"], "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"],
            "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "modulo": c_["modulo"], "ancora_principal": c_["ancora_principal"], "ancoras_de_secao": list(c_["ancoras_de_secao"]), "n_ancoras": c_["n_ancoras"], "n_flags": c_["n_flags"], "flag_prefix": c_["flag_prefix"],
            "nomes": list(c_["nomes"]), "n_nomes": c_["n_nomes"], "nomes_ratificados": c_["nomes_ratificados"], "estatuto_dos_nomes": c_["estatuto_dos_nomes"], "nomes_novos_a_ratificar": list(c_["nomes_novos_a_ratificar"]), "n_nomes_novos": c_["n_nomes_novos"], "campos_novos_da_estrutura": list(c_["campos_novos_da_estrutura"]),
            "estatuto_dos_nomes_novos": c_["estatuto_dos_nomes_novos"], "ratificacao_pendente": dict(c_["ratificacao_pendente"]), "ponte": dict(c_["ponte"]), "n_falas": c_["n_falas"], "ratificacao": dict(c_["ratificacao"]), "numeros": dict(c_["numeros"]), "frase_canonica_pt": c_["frase_canonica_pt"], "frase_canonica_en": c_["frase_canonica_en"],
            "frase_d83_pt": c_["frase_d83_pt"], "frase_d83_en": c_["frase_d83_en"], "chaves_antigas_que_mudam": list(c_["chaves"]), "n_checks_esperadas": c_["n_checks"], "exact_ladder_expected": c_["expected_ladder"]}
    out_.update(t_["extras"])
    if not beta_ok_:
        out_["verdict"] = _V410_AESCALA_RECUSA % "BETA_IS_NOT_ALPHA_SQRT_E"
    else:
        try:
            mec_ = _v410_aescala_mechanics(beta_rt_, core, c_, t_)
            out_.update(runtime_executed=True, mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], all_verified=bool(mec_["passed"] and mec_["n_checks"] == c_["n_checks"]))
            out_["verdict"] = (c_["veredito_ok"] if out_["all_verified"] else _V410_AESCALA_RECUSA % "MECHANICS_CHECK_FAILED")
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V410_AESCALA_RECUSA % "RUNTIME_ERROR"
    core["a_escala_v410"] = out_
    return out_
