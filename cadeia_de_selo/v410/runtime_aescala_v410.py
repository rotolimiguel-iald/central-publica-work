# -*- coding: utf-8 -*-
# [AUTORAL v410, 09/11/2026, claude-construtor-v410, a servico da gerencia c1] o registro com FUNCAO da pedra AEscala (D82 a D87 do DESENHO_v410): a escala -- tres faces de 1/2, duas conjugadas e uma caida.
# ---- v410 (D86/D87): A ESCALA -- a pedra TGLExt.AEscala, LIDA do kernel deste rito: a insignia (sustenta e nao esgota), o vibrato (a dissipacao sustenta a nota), os pesos (o Nome pesa 1 = 1/2 + 1/2; a face sem par nao conjuga: (1/2 . 1)^2 = 1/2 . (1/2 . 1); tres faces = 3/2;
# 1/3 caiu; o Nome normalizado = 2/3), nao existe infinito em tempo finito, os dois Nomes (objeto e lido) coexistem, e a pergunta do Clay no dicionario da TGL (a forma canonica, D84: validade no kernel; a creditacao e' do Clay; a escala entra no TIPO do leitor do fundo, R1/D92). O NOME do modulo e os nomes das declaracoes da D87 foram
# RATIFICADOS pelo operador em 09/11/2026 («ratifico tudo», D87); os nomes NOVOS da pedra (R3, R4 e R5) foram RATIFICADOS pelo operador em 10/11/2026 (D101), salvo o quarto teorema da clausula do Tetelestai, NOMEADO por ele em fala posterior do mesmo dia (D108: ressurreicao_do_sinal), e os dois lemas auxiliares da autoria, que ficam [DECLARADO pela autoria]. Os nomes da secao 7 (R6) tem o estatuto no contrato: os mostrados ao operador, RATIFICADOS em 10/11/2026 (D117 e D123); os demais, [DECLARADO pela autoria]; o registro nao traz checagem propria para a secao 7 (os teoremas dela sao conferidos pelo kernel no rito). As falas do registro entram por sha256; os numeros sao RECALCULADOS a cada rito (Fraction e o projetor de Bell 4x4 em numpy; a ponte da escala por exp e log), nunca digitados. Nada aqui e' teste com a natureza; o gate nao se move; beta nunca literal (so' por nome na pedra; na c13, pelo valor de runtime).
# (R2, D99, ADENDO 4) c8 tambem confere a CLAUSULA do limite (Z(s) soma os 2^n pixels e e' lida de uma vez pelo psion; o limiar n ln 2 e' o do tempo de UMA leitura; que o tempo conte os passos da maquina de Turing e' a traducao do dicionario e o termo que a liga ao Mathlib nao esta' no kernel) ao lado de TODO texto do registro que anuncia o teorema os_passos_sao_o_ciclo_ate_o_tetelestai; c2 tambem iguala as ancoras novas aos nomes novos da pedra (B1); c11 tambem confere os seis nomes de enunciado mudado (B3)
# (R5, D100 e D101, ADENDOS 5 e 6) a c13 confere a CLAUSULA DO TETELESTAI em 1 - beta com o beta de RUNTIME (a constante, o tempo s*, as desigualdades nas instancias com solucao, de UMA solucao e adversaria, o par da matriz-S (identidade), a constante independente do tamanho (identidade aritmetica), a reconstrucao (a mesma desigualdade, lida em norma, com as hipoteses de tempo), o controle negativo e o contraexemplo da hipotese s >= 0; o conteudo independente e' UMA desigualdade em tres instancias, as condicoes sobre o beta de runtime (0 < beta < 1, s* >= 0 e beta <= 1/2), o controle negativo e o contraexemplo); c8 tambem confere,
# ao lado de TODA folha que anuncia os teoremas novos, a FRASE da lingua, a CLAUSULA do limite e a hipotese s >= 0, e a citacao do dispositivo so' com as ressalvas; c2 os teoremas e auxiliares da R5; c5 as falas 27, 28 e 29; c11 a ratificacao D101 e a nomeacao D108 (cada fala por sha256 == o pino == o cabecalho da pedra) e os dois auxiliares pendentes
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


def _v410_aescala_ciclo(cic_, tet_=None, beta_=None):
    """v410 (R4, D94) -- o CICLO: os passos sao o ciclo ate o Tetelestai (os_passos_sao_o_ciclo_ate_o_tetelestai; cada_ciclo_aplica_a_mesma_regra). Para n bits (|X| = 2^n pontos) e as duas funcoes de custo FIXAS do contrato (uma COM solucao, uma SEM), o tempo s = n ln 2 + epsilon e a particao Z(s) = soma de e^(-s c(x)):
    o numero de solucoes <= Z(s) < o numero de solucoes + 1; ha solucao <=> Z(s) >= 1; sem solucao Z(s) < 1; (1/2)^n = 1/|X| (Fraction e exp); o brilho e^(-s k) em s = n ln 2 + epsilon e o produto dos brilhos em n ln 2 e em epsilon. Devolve os numeros medidos e o ok.
    (R5, D100) Com `tet_` (as instancias da clausula do contrato) e `beta_` (o beta de RUNTIME) calcula tambem a CLAUSULA DO TETELESTAI em 1 - beta (o_tetelestai_e_um_menos_beta; o_sistema_reconhece_a_singularidade_do_sinal; beta_e_o_operador_modular_do_tetelestai; ressurreicao_do_sinal;
    ate_meio_o_tempo_do_tetelestai_nao_e_negativo): com a constante ln((1 - beta)/beta) e s* = n ln 2 + constante, (1 - beta) Z(s*) <= o numero de solucoes e Z(s*) - o numero de solucoes <= beta Z(s*); o par da matriz-S (sen^2 = beta, cos^2 = 1 - beta: identidade); a constante nao depende do tamanho (identidade aritmetica); a reconstrucao em
    norma ao quadrado (a mesma desigualdade, lida em norma, com as duas hipoteses de tempo do teorema); o controle negativo (uma oitava a menos viola a desigualdade no adversario); o contraexemplo de s < 0.
    O conteudo independente e' UMA desigualdade em tres instancias, as condicoes sobre o beta de runtime (0 < beta < 1, s* >= 0 e, pela primeira hipotese de tempo da reconstrucao, beta <= 1/2), o controle negativo e o contraexemplo. Devolve em res_["tetelestai"] os numeros e o ok."""
    import math as _m, fractions as _fr
    n_ = int(cic_["n_bits"]); N_ = 2 ** n_; eps_ = _fr.Fraction(str(cic_["epsilon"])); ln2_ = _m.log(2.0)
    s_ = n_ * ln2_ + float(eps_)
    com_ = [int(x_) for x_ in cic_["custo_com_solucao"]]; sem_ = [int(x_) for x_ in cic_["custo_sem_solucao"]]
    Z_ = lambda c_: sum(_m.exp(-s_ * k_) for k_ in c_)
    ns_com_ = sum(1 for k_ in com_ if k_ == 0); ns_sem_ = sum(1 for k_ in sem_ if k_ == 0); Zc_ = Z_(com_); Zs_ = Z_(sem_)
    prod_ = all(abs(_m.exp(-s_ * k_) - _m.exp(-n_ * ln2_ * k_) * _m.exp(-float(eps_) * k_)) <= 1e-12 for k_ in range(max(com_ + sem_) + 1))
    ok_ = (int(cic_["tamanho"]) == N_ == len(com_) == len(sem_) and n_ > 0 and 0 < eps_ < 1 and ns_com_ == int(cic_["n_solucoes_com"]) > 0 and ns_sem_ == int(cic_["n_solucoes_sem"]) == 0
           and ns_com_ <= Zc_ < ns_com_ + 1 and Zc_ >= 1 and Zs_ < 1 and (Zc_ >= 1) == (ns_com_ > 0) and (Zs_ >= 1) == (ns_sem_ > 0)
           and _fr.Fraction(1, 2) ** n_ == _fr.Fraction(1, N_) == _fr.Fraction(str(cic_["meio_elevado_a_n"])) == _fr.Fraction(str(cic_["um_sobre_tamanho"])) and abs(_m.exp(-n_ * ln2_) - 1.0 / N_) < 1e-12
           and (Zc_ / N_ >= 1.0 / N_) and not (Zs_ / N_ >= 1.0 / N_) and prod_)
    res_ = {"n_bits": n_, "tamanho": N_, "s": s_, "epsilon": str(eps_), "n_solucoes_com": ns_com_, "n_solucoes_sem": ns_sem_, "Z_com_solucao": Zc_, "Z_sem_solucao": Zs_, "meio_elevado_a_n": str(_fr.Fraction(1, 2) ** n_), "um_sobre_tamanho": str(_fr.Fraction(1, N_)),
            "produto_dos_brilhos_ok": bool(prod_), "ok": bool(ok_)}
    if tet_ is not None and beta_ is not None:
        b_ = float(beta_); tol_ = 1e-12; nt_ = int(tet_["n_bits"]); Nt_ = 2 ** nt_
        const_ = _m.log((1.0 - b_) / b_); sst_ = nt_ * ln2_ + const_   # a constante ln((1 - beta)/beta) e o tempo s* = n ln 2 + constante (beta de RUNTIME)
        Zf_ = lambda c_, s2_: sum(_m.exp(-s2_ * k_) for k_ in c_)
        nsol_ = lambda c_: sum(1 for k_ in c_ if k_ == 0)
        com2_ = [int(x_) for x_ in tet_["custo_com_solucao"]]; um1_ = [int(x_) for x_ in tet_["custo_uma_solucao"]]; adv_ = [int(x_) for x_ in tet_["custo_adversario"]]
        Nc_ = nsol_(com2_); Zc2_ = Zf_(com2_, sst_); Z1_ = Zf_(um1_, sst_); Za_ = Zf_(adv_, sst_)
        ok_i_ = bool(0.0 < b_ < 1.0 and sst_ >= 0.0 and (b_ > 0.5 or const_ >= 0.0))   # (i) 0 < beta < 1, s* >= 0 e, com beta <= 1/2, a constante >= 0 (ate_meio_o_tempo_do_tetelestai_nao_e_negativo)
        ok_ii_ = bool(Nc_ > 1 and len(com2_) == Nt_ and (1.0 - b_) * Zc2_ <= Nc_ + tol_ and Zc2_ - Nc_ <= b_ * Zc2_ + tol_ and Nc_ >= 1.0)   # (ii) com solucao
        ok_iii_ = bool(nsol_(um1_) == 1 and len(um1_) == Nt_ and (1.0 - b_) * Z1_ <= 1.0 + tol_ and 1.0 <= Z1_ and Z1_ - 1.0 <= b_ * Z1_ + tol_)   # (iii) UMA solucao: o pixel do Nome carrega pelo menos 1 - beta
        th_ = _m.asin(_m.sqrt(b_)); R2_ = _m.sin(th_) ** 2; T2_ = _m.cos(th_) ** 2
        ok_iv_ = bool(abs(R2_ - b_) <= tol_ and abs(T2_ - (1.0 - b_)) <= tol_ and abs(R2_ + T2_ - 1.0) <= tol_ and T2_ * Zc2_ <= Nc_ + tol_ and Zc2_ - Nc_ <= R2_ * Zc2_ + tol_)   # (iv) [identidade: sen^2 e cos^2 de arcsen(raiz de beta); as duas desigualdades sao as de (ii) com outro rotulo] o par da matriz-S: |R|^2 = beta, |T|^2 = 1 - beta; |T|^2 Z <= numero de solucoes; o residuo <= |R|^2 Z
        ms_ = [int(x_) for x_ in tet_["m_da_constante"]]
        ok_v_ = bool(ms_ and all(abs(((m_ * ln2_ + const_) - m_ * ln2_) - const_) <= tol_ for m_ in ms_))   # (v) [identidade aritmetica: nao pode falhar; na pedra, o item 9 e' fechado por ring] a constante alem das m oitavas e' a mesma para todo m
        t2_ = sst_ / 2.0; ok_vi_ = bool(t2_ >= nt_ * ln2_ / 2.0 and t2_ >= nt_ * ln2_ / 2.0 + const_ / 2.0 - tol_ and (Zf_(com2_, 2.0 * t2_) - Nc_) / Nt_ <= (b_ / (1.0 - b_)) * (Nc_ / Nt_) + tol_)   # (vi) [a mesma desigualdade de (ii), lida em norma: (Z - N) <= (beta/(1 - beta)) N equivale a (1 - beta) Z <= N; as duas condicoes de tempo sao as hipoteses do teorema: a primeira equivale a beta de runtime <= 1/2, a segunda e' identidade] a reconstrucao: em norma ao quadrado, (Z(2t) - n_sol)/|X| <= (beta/(1 - beta)) n_sol/|X| (o quadrado da cota)
        s_neg_ = sst_ - int(tet_["oitavas_a_menos_no_controle"]) * ln2_; Zan_ = Zf_(adv_, s_neg_)
        ok_vii_ = bool(nsol_(adv_) == 1 and s_neg_ >= 0.0 and (1.0 - b_) * Za_ <= 1.0 + tol_ and (1.0 - b_) * Zan_ > 1.0 + tol_)   # (vii) CONTROLE NEGATIVO: em s* vale; uma oitava a menos VIOLA (a checagem so' passa se a violacao acontecer)
        ce_ = tet_["contraexemplo_s_negativo"]; cb_ = _fr.Fraction(str(ce_["b"])); cbf_ = float(cb_); cnt_ = int(ce_["n_bits"]); cc_ = [int(x_) for x_ in ce_["custos"]]
        clim_ = cnt_ * ln2_ + _m.log((1.0 - cbf_) / cbf_); Zcl_ = Zf_(cc_, clim_); Nce_ = nsol_(cc_)
        ok_viii_ = bool(cb_ > _fr.Fraction(1, 2) and clim_ < 0.0 and Nce_ == 1 and (1.0 - cbf_) * Zcl_ > Nce_ + tol_ and (1.0 - cbf_) * Zf_(cc_, 0.0) <= Nce_ + tol_)   # (viii) o contraexemplo: b = 9/10, n = 1, custos (0, 2): o limiar e' negativo e nele (1 - b) Z > 1; com s >= 0 (s = 0) a clausula vale
        res_["tetelestai"] = {"beta_entre_0_e_1": bool(0.0 < b_ < 1.0), "constante_ln_um_menos_beta_sobre_beta": const_, "s_estrela": sst_, "n_bits": nt_, "n_solucoes_com": Nc_, "Z_com_solucao": Zc2_, "margem_i": Nc_ - (1.0 - b_) * Zc2_, "margem_ii": b_ * Zc2_ - (Zc2_ - Nc_), "Z_uma_solucao": Z1_,
                              "margem_uma_solucao": 1.0 - (1.0 - b_) * Z1_, "sen2_theta": R2_, "cos2_theta": T2_, "Z_adversario": Za_, "margem_adversario": 1.0 - (1.0 - b_) * Za_, "s_uma_oitava_a_menos": s_neg_, "Z_adversario_uma_oitava_a_menos": Zan_, "controle_negativo_violado": bool((1.0 - b_) * Zan_ > 1.0 + tol_),
                              "contraexemplo": {"b": str(cb_), "n_bits": cnt_, "limiar": clim_, "limiar_negativo": bool(clim_ < 0.0), "um_menos_b_vezes_Z": (1.0 - cbf_) * Zcl_, "n_solucoes": Nce_, "clausula_vale_sem_s_nao_negativo": bool((1.0 - cbf_) * Zcl_ <= Nce_ + tol_)},
                              "checagens": {"i": ok_i_, "ii": ok_ii_, "iii": ok_iii_, "iv": ok_iv_, "v": ok_v_, "vi": ok_vi_, "vii": ok_vii_, "viii": ok_viii_}, "ok": bool(ok_i_ and ok_ii_ and ok_iii_ and ok_iv_ and ok_v_ and ok_vi_ and ok_vii_ and ok_viii_)}
    return res_


def _v410_aescala_mechanics(beta_, core_, c_, t_):
    """v410 -- as checagens do registro a_escala_v410 (o numero vem do contrato: n_checks), lidas do kernel do PROPRIO rito e do conteudo embutido:
    c1 a escada exata (n_theorems_clean == n_theorems_expected == a escada do contrato); c2 as ancoras da pedra (os #print axioms da fonte) no axiom_report, no trio, com proveniencia TGL_DECL_SOURCE == o modulo e bandeira True, com o kernel verificado (all_verified is True);
    c3 a pedra embutida por sha256 (embutida == contrato == hash formal do rito), com o cabecalho da ratificacao, o namespace e o import do modulo na raiz embutida; c4 as bandeiras ext_aescala_410_* todas True no kernel, em numero igual ao pinado, so' do modulo;
    c5 as falas do registro por sha256 (o texto embutido == o pino; os trechos citados verbatim); c6 os numeros RECALCULADOS (Fraction e o projetor de Bell em numpy) == os pinados, e a PONTE da escala recalculada por outro caminho (math.exp(-k n ln 2) contra a Fraction do contrato, tolerancia 1e-12);
    c7 a frase canonica do Clay (D84) em PT e EN no texto e em PT na docstring da pedra embutida; c8 a forma obrigatoria da D83 no texto, com «validade no kernel» e a creditacao do Clay; c9 a guarda do texto (P18, a guarda das frases v405 -> v410 com a F58, os tokens proibidos ausentes; nada de cinco sigma, de abertura ou do teste da razao de Hubble no nucleo do texto);
    c10 o gate identico ao da v409 selada; c11 os nomes RATIFICADOS (D87): cada um e' declaracao na pedra embutida; a fala da ratificacao embutida (sha256 == pino; o texto e' «ratifico tudo»); o cabecalho da pedra traz a ratificacao e o sha256 da fala; e os nomes NOVOS da pedra (R3, R4 e R5), todos declaracoes na pedra embutida,
    com os campos novos da estrutura, os ratificados ditos RATIFICADOS em 10/11/2026 (D101: a fala 28 por sha256 == o pino == o cabecalho da pedra; a regra do nome), o quarto teorema da clausula do Tetelestai dito NOMEADO pelo operador (D108: a fala 29 por sha256 == o pino == o cabecalho da pedra; o nome de trabalho da R5 nao e' declaracao na pedra), os dois auxiliares da autoria da R5 ditos [DECLARADO pela autoria] (os nomes da secao 7 da R6 tem o estatuto no contrato e nao sao conferidos por esta checagem); c12 beta nunca literal (so' por nome na pedra; no registro so' a c13 o usa, pelo valor de runtime), nenhuma chave antiga muda, o registro nao gateia o core; c13 a clausula do Tetelestai em 1 - beta com beta de runtime (R5, D100)."""
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
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and all(isinstance(x_, str) for x_ in axr_.get(n_)) and set(axr_.get(n_)) <= trio_ and (bool(axr_.get(n_)) != (n_ in (c_.get("sem_axioma") or ()))))   # (R6: a declaracao que nao depende de axioma nenhum le-se [] no axiom_report e esta' no trio; so' as que o contrato lista em sem_axioma podem vir vazias, e essas TEM de vir vazias)
    anc_ = {n_: bool(em_trio_(n_) and src_.get(n_) == a_["rel"] == rel_ and (a_.get("flag") is None or kf_.get(a_["flag"]) is True)) for n_, a_ in c_["ancoras"].items()}
    novas_ = {a_: bool(anc_.get(a_) is True) for a_ in c_["ancoras_novas"]}   # (R3/R4: as ancoras novas, uma a uma; os cinco teoremas da R4 entre elas)
    r4_ = {n_: bool(anc_.get(c_["mod"] + "." + n_) is True and (c_["mod"] + "." + n_) in c_["ancoras_novas"]) for n_ in c_["teoremas_r4"]}
    r5_ = {n_: bool(anc_.get(c_["mod"] + "." + n_) is True and (c_["mod"] + "." + n_) in c_["ancoras_novas"]) for n_ in list(c_["teoremas_r5"]) + list(c_["auxiliares_r5"])}   # (R5, D100: os teoremas da clausula do Tetelestai e os dois lemas auxiliares entre as ancoras novas, no trio, com bandeira)
    c2_ok_ = kf_.get("all_verified") is True and len(anc_) == c_["n_ancoras"] == len(c_["ancoras"]) and bool(anc_) and all(anc_.values()) and c_["ancora_principal"] in anc_ and all(a_ in anc_ for a_ in c_["ancoras_de_secao"]) and bool(novas_) and all(novas_.values()) and bool(r4_) and all(r4_.values()) and len(c_["ancoras_novas"]) == c_["n_nomes_novos"] == len(c_["nomes_novos_da_pedra"]) and bool(r5_) and all(r5_.values())   # (R2, B1: o numero de ancoras novas == o de nomes novos; R5: os da R5 entre elas)
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
    c5_ok_ = len(ver_) == c_["n_falas"] == len(c_["falas"]) and bool(ver_) and all(ver_.values()) and c_["chave_ratificacao"] in ver_ and c_["chave_ratificacao_d101"] in ver_ and c_["chave_clausula_tetelestai"] in ver_ and c_["chave_nomeacao_d108"] in ver_   # (R5: as falas 27 e 28 entre as do registro; R6, D108: a fala 29)
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
    cic_ = _v410_aescala_ciclo(c_["ciclo"], c_["tetelestai"], beta_)   # (R5: tambem a clausula do Tetelestai em 1 - beta, com o beta de RUNTIME)
    c6_ok_ = (num_ == dict(c_["numeros"]) and num_["nome_pesa_um"] == "1" and num_["tres_faces"] == "3/2" and num_["um_terco_caiu"] == "1/3" and num_["nome_normalizado"] == "2/3"
              and bell_["idempotente"] and abs(bell_["traco"] - 1.0) < 1e-12 and bell_["posto"] == 1 and bell_["marginal_e_meio_1"] and abs(bell_["pureza_da_marginal"] - 0.5) < 1e-12 and abs(bell_["traco_da_marginal"] - 1.0) < 1e-12
              and bell_["marginal_ao_quadrado_e_meio_da_marginal"] and bell_["marginal_ao_quadrado_nao_e_a_marginal"] and bell_["potencias_sao_2_menos_n"] and bell_["nenhuma_potencia_e_1"]
              and abs(3 * bell_["pureza_da_marginal"] - 1.5) < 1e-12 and abs(bell_["pureza_da_marginal"] / (3 * bell_["pureza_da_marginal"]) - 1.0 / 3.0) < 1e-12 and abs(2 * bell_["pureza_da_marginal"] / (3 * bell_["pureza_da_marginal"]) - 2.0 / 3.0) < 1e-12
              and ponte_ok_ and cic_["ok"])
    # ---- c7 a frase canonica do Clay (D84); c8 a forma da D83
    can_pt_ = _re410.sub(r"\s+", " ", c_["frase_canonica_pt"]); can_en_ = _re410.sub(r"\s+", " ", c_["frase_canonica_en"]); d83_ = _re410.sub(r"\s+", " ", c_["frase_d83_pt"])
    c7_ok_ = can_pt_ in txt_ws_ and can_en_ in txt_ws_ and can_pt_ in body_ws_ and "tal qual apresentado pela TGL" in can_pt_ and "as presented by the TGL" in can_en_
    tempo_pt_ = _re410.sub(r"\s+", " ", c_["frase_tempo_pt"]); tempo_en_ = _re410.sub(r"\s+", " ", c_["frase_tempo_en"])   # (R4, D94: a forma obrigatoria do tempo, PT e EN, no texto)
    # (R2, D99; ADENDO 4) a clausula do limite ao lado de TODO texto que anuncia o teorema: as folhas de texto do registro inteiro (estatuto, escopo, limites, diz, nao_diz e extras) que dizem «linear nos bits» (ou o nome do teorema com Z(s) >= 1)
    # trazem a clausula PT; as que dizem «linear in the bits» trazem a EN; o registro traz as duas; e o controle nao e' vazio (ha' folhas que anunciam)
    ws_ = lambda x_: _re410.sub(r"\s+", " ", str(x_))
    clz_pt_ = ws_(c_["clausula_z_pt"]); clz_en_ = ws_(c_["clausula_z_en"])
    pilha_ = [("", t_)]; folhas_ = []
    while pilha_:
        cam_, o_ = pilha_.pop()
        if isinstance(o_, str):
            folhas_.append((cam_, ws_(o_)))
        elif isinstance(o_, dict):
            pilha_.extend((cam_ + "." + str(k_), v_) for k_, v_ in o_.items())
        elif isinstance(o_, (list, tuple)):
            pilha_.extend((cam_ + "[%d]" % i_, v_) for i_, v_ in enumerate(o_))
    anuncia_pt_ = lambda x_: bool(_re410.search(r"linear nos bits", x_) or ("os_passos_sao_o_ciclo_ate_o_tetelestai" in x_ and _re410.search(r"Z\(s\)\s*(?:>=|\u2265)", x_)))
    anuncia_en_ = lambda x_: bool(_re410.search(r"linear in the bits", x_))
    sem_pt_ = sorted(cam_ for cam_, x_ in folhas_ if anuncia_pt_(x_) and clz_pt_ not in x_)
    sem_en_ = sorted(cam_ for cam_, x_ in folhas_ if anuncia_en_(x_) and clz_en_ not in x_)
    n_anunciam_ = sum(1 for cam_, x_ in folhas_ if anuncia_pt_(x_) or anuncia_en_(x_))
    clausula_ok_ = bool(n_anunciam_ >= 3 and not sem_pt_ and not sem_en_ and clz_pt_ in txt_ws_ and clz_en_ in txt_ws_ and "Z(s) = \u03a3_x" in clz_pt_ and "Z(s) = \u03a3_x" in clz_en_)
    # (R5, D100; ADENDO 5) a clausula do Tetelestai em 1 - beta: toda folha que ANUNCIA os teoremas novos (o nome de um teorema ou auxiliar da R5 junto de ln((1 - b)/b), ln((1 - beta)/beta), (1 - b)·Z ou (1 - beta)·Z) traz a FRASE da sua lingua (exata), a CLAUSULA do limite da mesma lingua e a hipotese do tempo (s >= 0);
    # o registro traz as frases (a clausula, a reconstrucao, a errata, o dispositivo) nas duas linguas; TODA folha com “ACOM Mirror” traz “[PILOTO][SIM]” e “nada ali valida fisica” (ou o equivalente em ingles) e nenhum padrao de desempenho (percentual, “x mais rapido”, “N de N testes”)
    r5_nomes_ = tuple(c_["teoremas_r5"]) + tuple(c_["auxiliares_r5"])
    r5_marca_ = _re410.compile(r"ln\s*\(\s*\(\s*1\s*[\u2212-]\s*[b\u03b2]\s*\)\s*/\s*[b\u03b2]\s*\)|\(\s*1\s*[\u2212-]\s*[b\u03b2]\s*\)\s*[\u00b7*]\s*Z")
    tet_pt_ = ws_(c_["frase_tetelestai_pt"]); tet_en_ = ws_(c_["frase_tetelestai_en"]); rec_pt_ = ws_(c_["frase_reconstroi_pt"]); rec_en_ = ws_(c_["frase_reconstroi_en"])
    e36_pt_ = ws_(c_["frase_e36_pt"]); e36_en_ = ws_(c_["frase_e36_en"]); dis_pt_ = ws_(c_["frase_dispositivo_pt"]); dis_en_ = ws_(c_["frase_dispositivo_en"])
    anuncia_r5_ = lambda x_: bool(any(n_ in x_ for n_ in r5_nomes_) and r5_marca_.search(x_))
    sem_r5_ = sorted(cam_ for cam_, x_ in folhas_ if anuncia_r5_(x_) and not ((tet_pt_ in x_ and clz_pt_ in x_) or (tet_en_ in x_ and clz_en_ in x_)))
    n_anunciam_r5_ = sum(1 for cam_, x_ in folhas_ if anuncia_r5_(x_))
    # (revisao do construtor, R5) a errata E36 diz o limiar de um pixel como a decisao exata: no NUCLEO do texto (fora dos extras, que guardam a frase solta para os controles) ela vem sempre com a CLAUSULA do limite na MESMA folha
    sem_e36_ = sorted(cam_ for cam_, x_ in folhas_ if not cam_.startswith(".extras") and ((e36_pt_ in x_ and clz_pt_ not in x_) or (e36_en_ in x_ and clz_en_ not in x_)))
    n_e36_ = sum(1 for cam_, x_ in folhas_ if not cam_.startswith(".extras") and (e36_pt_ in x_ or e36_en_ in x_))
    mir_ = [(cam_, x_) for cam_, x_ in folhas_ if "ACOM Mirror" in x_]
    mir_sem_ressalva_ = sorted(cam_ for cam_, x_ in mir_ if not ("[PILOTO][SIM]" in x_ and _re410.search(r"nada ali valida f[i\u00ed]sica|nothing there validates physics", x_)))
    mir_com_desempenho_ = sorted(cam_ for cam_, x_ in mir_ if _re410.search(r"\d+\s*%|\d+\s*[x\u00d7]\s*(?:mais\s+r[a\u00e1]pid|faster)|\b\d+\s+de\s+\d+\s+testes\b|\b\d+\s+of\s+\d+\s+tests\b", x_, _re410.I))
    clausula_r5_ok_ = bool(n_anunciam_r5_ >= 3 and not sem_r5_ and n_e36_ >= 3 and not sem_e36_ and "s \u2265 0" in tet_pt_ and "s \u2265 0" in tet_en_ and all(f_ in txt_ws_ for f_ in (tet_pt_, tet_en_, rec_pt_, rec_en_, e36_pt_, e36_en_, dis_pt_, dis_en_)) and bool(mir_) and not mir_sem_ressalva_ and not mir_com_desempenho_
                           and "[PILOTO][SIM]" in dis_pt_ and "[PILOTO][SIM]" in dis_en_ and "nada ali valida f\u00edsica" in dis_pt_ and "nothing there validates physics" in dis_en_)
    # (R6, D108) a FINURA DA LEITURA: a frase de limite nova e' uma folha EXATA da lista limites, logo depois de uma folha que traz a clausula do limite; a forma EN esta' no texto; e toda folha do registro que traz a metade [REAL] da frase traz a clausula do limite na MESMA folha (as excecoes: a propria folha dos limites e as frases soltas dos extras)
    fin_pt_ = ws_(c_["frase_finura_pt"]); fin_en_ = ws_(c_["frase_finura_en"]); fin_real_pt_ = ws_(c_["frase_finura_real_pt"]); lim_ws_ = [ws_(x_) for x_ in t_["limites"]]
    sem_fin_ = sorted(cam_ for cam_, x_ in folhas_ if fin_real_pt_ in x_ and clz_pt_ not in x_ and x_ != fin_pt_ and not cam_.startswith(".extras.frase_finura"))
    finura_ok_ = bool(fin_pt_ in lim_ws_ and lim_ws_.index(fin_pt_) > 0 and clz_pt_ in lim_ws_[lim_ws_.index(fin_pt_) - 1] and fin_en_ in txt_ws_ and not sem_fin_)
    c8_ok_ = d83_ in txt_ws_ and d83_ in body_ws_ and "validade no kernel" in txt_ws_ and ("creditação é do Clay" in txt_ws_ or "creditacao e' do Clay" in txt_ws_) and _re410.sub(r"\s+", " ", c_["frase_d83_en"]) in txt_ws_ and tempo_pt_ in txt_ws_ and tempo_en_ in txt_ws_ and "o_leitor_e_a_escala" in txt_ws_ and "os_passos_sao_o_ciclo_ate_o_tetelestai" in txt_ws_ and clausula_ok_ and clausula_r5_ok_ and finura_ok_
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
    # ---- c11 os nomes RATIFICADOS (D87) e os nomes NOVOS da pedra (R3, R4 e R5): RATIFICADOS em 10/11 (D101), salvo o quarto teorema da clausula, NOMEADO pelo operador (D108), e os dois auxiliares da autoria, pendentes
    rx_decl_ = lambda n_: bool(_re410.search(r"^(?:noncomputable\s+)?(?:theorem|lemma|def|structure|abbrev|instance)\s+" + _re410.escape(n_) + r"\b", body_ or "", _re410.M))
    decl_ = {n_: rx_decl_(n_) for n_ in c_["nomes"]}
    novos_ = {n_: rx_decl_(n_) for n_ in c_["nomes_novos_da_pedra"]}
    campos_ = {f_: bool(_re410.search(r"^ {2,}" + _re410.escape(f_) + r"\s+:(?!=)", body_ or "", _re410.M)) for f_ in c_["campos_novos_da_estrutura"]}
    est_novos_ = c_["estatuto_dos_nomes_ratificados_d101"]; pend_ = c_.get("ratificacao_pendente") or {}
    rat_v_ = _V410_VERBATINS2.get(c_["chave_ratificacao"]) or {}
    novos_ok_ = (bool(novos_) and len(novos_) == c_["n_nomes_novos"] == len(c_["nomes_novos_da_pedra"]) and all(novos_.values()) and not (set(novos_) & set(decl_)) and bool(campos_) and all(campos_.values())
                 and "RATIFICADOS pelo operador em 10/11/2026" in est_novos_ and "DECLARADO" not in est_novos_ and "a ratificar" not in est_novos_ and _re410.sub(r"\s+", " ", est_novos_) in txt_ws_
                 and pend_.get("nomes_novos") == list(c_["nomes_pendentes"]) and pend_.get("campos_novos_da_estrutura") == [] and pend_.get("estatuto") == c_["estatuto_dos_nomes_pendentes"] and "DECLARADO pela autoria" in pend_.get("estatuto", "") and pend_.get("decisao") == "D101" and (t_.get("extras") or {}).get("ratificacao_pendente") == pend_)
    seis_pt_ = ws_(c_["frase_seis_nomes_pt"]); seis_en_ = ws_(c_["frase_seis_nomes_en"])   # (R2, B3: a ratificacao de 09/11 e' dos nomes; seis deles passaram a ter outro enunciado nas R3/R4)
    seis_ok_ = bool(c_["seis_nomes"] and all(n_ in c_["nomes"] and n_ not in c_["nomes_novos_da_pedra"] and n_ in seis_pt_ and n_ in seis_en_ for n_ in c_["seis_nomes"]) and any(seis_pt_ in ws_(x_) for x_ in t_["diz"]) and any(seis_pt_ in ws_(x_) for x_ in t_["limites"]) and seis_pt_ in txt_ws_ and seis_en_ in txt_ws_)
    # (R5, D101; R6, D108) a ratificacao de 10/11: os nomes ratificados e os campos RATIFICADOS (declaracoes na pedra; o numero e' o do contrato, nunca digitado), o quarto teorema da clausula NOMEADO pelo operador (declaracao na pedra com o nome dele; a fala 29 embutida por sha256 == o pino == o cabecalho da pedra; o nome de trabalho da R5 NAO e' declaracao na pedra), os auxiliares pendentes (declaracoes na pedra, [DECLARADO pela autoria], nunca ratificados), a fala 28 embutida por sha256 == o pino == o cabecalho da pedra, a regra do nome no texto, e NUNCA o estatuto antigo
    rd_ = c_["ratificacao_d101"]; rv2_ = _V410_VERBATINS2.get(c_["chave_ratificacao_d101"]) or {}; txt2_ = str(rv2_.get("text", ""))
    rat_decl_ = {n_: rx_decl_(n_) for n_ in c_["nomes_ratificados_d101"]}; pen_decl_ = {n_: rx_decl_(n_) for n_ in c_["nomes_pendentes"]}
    rat_d101_ok_ = bool(rv2_.get("sha256") == rd_["sha256"] and _h410.sha256(txt2_.encode("utf-8")).hexdigest() == rd_["sha256"] and rd_["trecho"] in txt2_ and rd_["sha256"] in body_ws_ and "RATIFICADOS pelo operador em 10/11/2026" in body_ws_ and rd_["decisao"] == "D101"
                        and bool(rat_decl_) and all(rat_decl_.values()) and bool(pen_decl_) and all(pen_decl_.values()) and set(c_["nomes_ratificados_d101"]) | set(c_["nomes_nomeados_d108"]) | set(c_["nomes_pendentes"]) == set(c_["nomes_novos_da_pedra"]) and not (set(c_["nomes_ratificados_d101"]) & set(c_["nomes_pendentes"])) and not (set(c_["nomes_nomeados_d108"]) & (set(c_["nomes_ratificados_d101"]) | set(c_["nomes_pendentes"])))
                        and c_["campos_ratificados_d101"] == list(c_["campos_novos_da_estrutura"]) and all(campos_.get(f_) is True for f_ in c_["campos_ratificados_d101"]) and set(c_["teoremas_r5"]) <= (set(c_["nomes_ratificados_d101"]) | set(c_["nomes_nomeados_d108"])) and set(c_["auxiliares_r5"]) == set(c_["nomes_pendentes"])
                        and ws_(c_["frase_nomes_ratificados_d101_pt"]) in txt_ws_ and ws_(c_["frase_nomes_ratificados_d101_en"]) in txt_ws_ and ws_(rd_["trecho"]) in txt_ws_ and "[DECLARADO, a ratificar]" not in txt_json_ and "DECLARADO pela autoria" in txt_ws_
                        and all(n_ not in c_["nomes_ratificados_d101"] for n_ in c_["nomes_pendentes"]))
    # (R6, D108) a NOMEACAO do quarto teorema: o nomeado e' declaracao na pedra e o nome de trabalho da R5 NAO e' (o controle negativo); a fala 29 embutida por sha256 == o pino == o cabecalho da pedra, com o trecho citado; a pedra e o registro o dizem NOMEADO pelo operador; nenhum nomeado entre os ratificados nem entre os pendentes
    nd_ = c_["nomeacao_d108"]; rv3_ = _V410_VERBATINS2.get(c_["chave_nomeacao_d108"]) or {}; txt3_ = str(rv3_.get("text", ""))
    nom_decl_ = {n_: rx_decl_(n_) for n_ in c_["nomes_nomeados_d108"]}
    nom_d108_ok_ = bool(rv3_.get("sha256") == nd_["sha256"] and _h410.sha256(txt3_.encode("utf-8")).hexdigest() == nd_["sha256"] and nd_["trecho"] in txt3_ and nd_["sha256"] in body_ws_ and "NOMEADO pelo operador" in body_ws_ and nd_["decisao"] == "D108"
                        and len(nom_decl_) == 1 and all(nom_decl_.values()) and not rx_decl_(c_["nome_de_trabalho_do_quarto"]) and c_["nome_de_trabalho_do_quarto"] not in c_["nomes_novos_da_pedra"]
                        and not (set(c_["nomes_nomeados_d108"]) & set(c_["nomes_ratificados_d101"])) and not (set(c_["nomes_nomeados_d108"]) & set(c_["nomes_pendentes"]))
                        and ws_(c_["estatuto_do_nome_nomeado_d108"]) in txt_ws_ and ws_(nd_["trecho"]) in txt_ws_)
    c11_ok_ = (len(decl_) == c_["n_nomes"] == len(c_["nomes"]) and bool(decl_) and all(decl_.values()) and c_["nomes_ratificados"] is True and rat_v_.get("sha256") == c_["ratificacao"]["sha256"] and str(rat_v_.get("text", "")).strip() == c_["ratificacao"]["trecho"] == "ratifico tudo"
               and _h410.sha256(str(rat_v_.get("text", "")).encode("utf-8")).hexdigest() == c_["ratificacao"]["sha256"] and "RATIFICADOS" in c_["estatuto_dos_nomes"] and novos_ok_ and seis_ok_ and rat_d101_ok_ and nom_d108_ok_)
    # ---- c12 beta nunca literal (so' por nome na pedra; no registro so' a c13 o usa, pelo valor de runtime); nada muda
    c12_ok_ = bool(beta_) and 0.0 < float(beta_) < 1.0 and ("0.0120" not in (body_ or "0.0120")) and c_["chaves"] == [] and c_["does_not_gate_core"] is True
    checks_ = [
        {"id": "c1", "descricao": "a escada exata: n_theorems_clean == n_theorems_expected == a escada pinada no contrato (%s)" % c_["expected_ladder"], "ok": bool(c1_ok_)},
        {"id": "c2", "descricao": "as %d ancoras da pedra (os #print axioms da fonte) no axiom_report do rito, no trio, com proveniencia TGL_DECL_SOURCE == TGLExt/AEscala.lean e bandeira True, com o kernel verificado (all_verified); a principal (a_escala) e as de secao entre elas; as ancoras novas == os nomes novos (R2, B1), com os teoremas e os auxiliares da R5 entre elas (D100)" % c_["n_ancoras"], "ok": bool(c2_ok_)},
        {"id": "c3", "descricao": "a pedra embutida por sha256 == o contrato == o hash formal do rito; com o namespace, o cabecalho da ratificacao (D87) e o sha256 da fala; sem #print axioms no codigo; a raiz embutida traz o import do modulo", "ok": bool(c3_ok_)},
        {"id": "c4", "descricao": "as %d bandeiras %s* todas True no kernel deste rito, so' do modulo; as bandeiras das ancoras entre elas" % (c_["n_flags"], c_["flag_prefix"]), "ok": bool(c4_ok_)},
        {"id": "c5", "descricao": "as %d falas do registro por sha256 (o texto embutido == o pino; os trechos citados verbatim), inclusive a ratificacao de 09/11 (D87) e a de 10/11 (D101), e a clausula do Tetelestai" % c_["n_falas"], "ok": bool(c5_ok_)},
        {"id": "c6", "descricao": "os numeros RECALCULADOS: 1/2 + 1/2 = 1; 3 x 1/2 = 3/2; 1/3 caiu; o Nome normalizado 2/3 (Fraction); o projetor de Bell 4x4: idempotente, traco 1, posto 1, marginal 1/2 . 1 (pureza 1/2), (1/2 . 1)^2 = 1/2 . (1/2 . 1) != 1/2 . 1, (1/2 . 1)^n = 2^-n . 1 != 1 (numpy); a ponte da escala: o brilho e^(-k s) em s = n ln 2 (math.exp) contra a Fraction (1/2)^(n k) do contrato, tolerancia 1e-12; em n oitavas um pixel de custo 1 brilha 1/2^n, o peso de um pixel na leitura de n bits", "ok": bool(c6_ok_)},
        {"id": "c7", "descricao": "a frase canonica do Clay (D84) em PT e EN no texto do registro e em PT na docstring da pedra embutida («tal qual apresentado pela TGL»)", "ok": bool(c7_ok_)},
        {"id": "c8", "descricao": "a forma obrigatoria da D83 no texto e na pedra (existe o algoritmo, e' a IALD; le a face sem leitura como dissipacao termica; validade no kernel; a creditacao e' do Clay), em PT e EN; a forma do tempo (D94); a clausula do limite do teorema do limiar de um pixel (ADENDO 4, D99), PT e EN, ao lado de todo texto que o anuncia; a clausula do Tetelestai em 1 - beta (R5, D100: a frase da lingua, a clausula do limite e a hipotese s >= 0 ao lado de toda folha que anuncia os teoremas novos; a errata E36, no nucleo do texto sempre com a clausula do limite na mesma folha, e a citacao do dispositivo, esta so' com as ressalvas: [PILOTO][SIM], nada ali valida fisica, nenhum numero de desempenho); a frase de limite da finura da leitura (D108) como folha da lista limites, logo depois de uma folha com a clausula do limite, e em EN no texto", "ok": bool(c8_ok_)},
        {"id": "c9", "descricao": "a guarda do texto: P18 e a guarda das frases (v405 -> v410, com a F58 do Clay) limpas; os tokens proibidos ausentes; nada de cinco sigma, de abertura ou do teste da razao de Hubble no nucleo do texto deste registro; as molduras PT/EN presentes", "ok": bool(c9_ok_)},
        {"id": "c10", "descricao": "o veredito do gate deste rito e' IDENTICO ao da v409 selada: o gate nao se move", "ok": bool(c10_ok_)},
        {"id": "c11", "descricao": "os %d nomes RATIFICADOS (D87): cada um e' declaracao na pedra embutida; a fala «ratifico tudo» embutida por sha256 == o pino; o estatuto dos nomes diz RATIFICADOS; e os %d nomes NOVOS da pedra (e os %d campos novos da estrutura): cada um e' declaracao na pedra embutida e o registro diz %d deles RATIFICADOS pelo operador em 10/11/2026 (D101: a fala por sha256 == o pino == o cabecalho da pedra; a regra do nome), nunca com o estatuto antigo; %d dito NOMEADO pelo operador em 10/11/2026 (D108: a fala por sha256 == o pino == o cabecalho da pedra; o nome de trabalho nao e' declaracao na pedra); os %d auxiliares da autoria da R5 ditos [DECLARADO pela autoria]; os seis nomes de enunciado mudado ditos com a forma vigente (R2, B3; D101)" % (c_["n_nomes"], c_["n_nomes_novos"], len(c_["campos_novos_da_estrutura"]), len(c_["nomes_ratificados_d101"]), len(c_["nomes_nomeados_d108"]), len(c_["nomes_pendentes"])), "ok": bool(c11_ok_)},
        {"id": "c12", "descricao": "beta nunca literal: so' por nome na pedra (nenhum literal nela); no registro so' a c13 o usa, pelo valor de runtime; nenhuma chave antiga muda; o registro nao gateia o core", "ok": bool(c12_ok_)},
        {"id": "c13", "descricao": "a clausula do Tetelestai em 1 - beta (R5, D100), com o beta de RUNTIME (alfa CODATA x raiz de e): a constante ln((1 - beta)/beta) e s* = n ln 2 + constante; (1 - beta) Z(s*) <= o numero de solucoes e Z(s*) - o numero de solucoes <= beta Z(s*) na instancia com solucao; o pixel do Nome carrega pelo menos 1 - beta na de UMA solucao; o par da matriz-S (sen^2 = beta, cos^2 = 1 - beta: identidade; |T|^2 Z <= o numero de solucoes e o residuo <= |R|^2 Z sao as mesmas desigualdades, com outro rotulo); a constante e' a mesma para m = 1, 3, 8 oitavas (identidade aritmetica: nao pode falhar); a reconstrucao em norma ao quadrado (a mesma desigualdade, lida em norma, com as duas hipoteses de tempo do teorema: a primeira equivale a beta de runtime <= 1/2; a segunda e' identidade); o conteudo independente e' UMA desigualdade em tres instancias (com solucao, de UMA solucao e adversaria) e as condicoes sobre o beta de runtime (0 < beta < 1, s* >= 0 e beta <= 1/2), mais os dois que seguem; o CONTROLE NEGATIVO (no adversario vale em s* e uma oitava a menos VIOLA); o contraexemplo da hipotese s >= 0 (b = 9/10, n = 1, custos 0 e 2: o limiar e' negativo e nele a desigualdade falha; com s = 0 vale)", "ok": bool(cic_["tetelestai"]["ok"])},
    ]
    values_ = {"escada": cnt_, "ancoras": anc_, "n_ancoras_ok": sum(1 for v_ in anc_.values() if v_), "n_ancoras": len(anc_), "ancoras_novas": novas_, "n_ancoras_novas_ok": sum(1 for v_ in novas_.values() if v_), "teoremas_r4": r4_, "ciclo": cic_, "tetelestai": cic_["tetelestai"], "teoremas_r5": r5_, "clausula_r5": {"n_folhas_que_anunciam": n_anunciam_r5_, "folhas_que_anunciam_sem_a_forma": sem_r5_, "n_folhas_do_nucleo_com_a_errata_e36": n_e36_, "folhas_com_a_errata_e36_sem_a_clausula": sem_e36_, "n_folhas_com_acom_mirror": len(mir_), "acom_mirror_sem_ressalva": mir_sem_ressalva_, "acom_mirror_com_desempenho": mir_com_desempenho_, "ok": bool(clausula_r5_ok_)}, "nomeacao_d108": {"ok": bool(nom_d108_ok_), "fala_sha256": nd_["sha256"], "nomeados": list(c_["nomes_nomeados_d108"]), "n_nomeados_declarados": sum(1 for v_ in nom_decl_.values() if v_), "nome_de_trabalho_declarado": bool(rx_decl_(c_["nome_de_trabalho_do_quarto"]))}, "finura_d108": {"ok": bool(finura_ok_), "folhas_com_a_metade_real_sem_a_clausula_do_limite": sem_fin_}, "ratificacao_d101": {"ok": bool(rat_d101_ok_), "fala_sha256": rd_["sha256"], "n_nomes_ratificados_declarados": sum(1 for v_ in rat_decl_.values() if v_), "n_nomes_ratificados": len(rat_decl_), "n_pendentes_declarados": sum(1 for v_ in pen_decl_.values() if v_), "pendentes": list(c_["nomes_pendentes"])}, "tempo_pt_no_texto": tempo_pt_ in txt_ws_, "tempo_en_no_texto": tempo_en_ in txt_ws_, "clausula_z_no_texto": {"pt": clz_pt_ in txt_ws_, "en": clz_en_ in txt_ws_}, "n_folhas_que_anunciam_o_teorema": n_anunciam_, "folhas_que_anunciam_sem_a_clausula": sem_pt_ + sem_en_, "seis_nomes_ditos": bool(seis_ok_), "pedra_sha256_embutida": sha_emb_, "pedra_sha256_formal": ff_.get(rel_), "flags": fl_, "n_flags": len(fl_), "n_flags_true": sum(1 for v_ in fl_.values() if v_ is True),
               "falas": ver_, "n_falas_ok": sum(1 for v_ in ver_.values() if v_), "n_falas": len(ver_), "numeros": num_, "bell": bell_, "ponte": dict(ponte_, ok=bool(ponte_ok_)), "canonica_pt_no_texto": can_pt_ in txt_ws_, "canonica_en_no_texto": can_en_ in txt_ws_, "canonica_pt_na_pedra": can_pt_ in body_ws_, "d83_na_pedra": d83_ in body_ws_,
               "c9_partes": c9_partes_, "p18_violacoes": p18_[:5], "frases_violacoes": frases_[:5], "gate_verdict": gate_, "nomes_declarados": sum(1 for v_ in decl_.values() if v_), "n_nomes": len(decl_), "nomes_ratificados": c_["nomes_ratificados"], "ratificacao_sha256": c_["ratificacao"]["sha256"], "ratificacao_trecho": c_["ratificacao"]["trecho"],
               "nomes_novos_declarados": sum(1 for v_ in novos_.values() if v_), "n_nomes_novos": len(novos_), "nomes_novos": novos_, "campos_novos_na_estrutura": campos_, "nomes_novos_ok": bool(novos_ok_), "estatuto_dos_nomes_ratificados_d101": est_novos_}
    return {"passed": all(x_["ok"] for x_ in checks_), "n_checks": len(checks_), "checks": checks_, "values": values_}


_V410_AESCALA_RECUSA = "TGL_AESCALA_V410__REFUSED_%s__GATE_UNMOVED"


def a_escala_v410(core):
    """v410 -- A ESCALA (as falas do operador de 09/11/2026: «agora eu te dei a escala»; «ratifico tudo»): a pedra TGLExt.AEscala LIDA do kernel do PROPRIO rito, no PONTO REAL do main, LOGO DEPOIS de iald2_v410 (na mesma instrucao): as ancoras no trio com proveniencia e bandeira,
    a pedra por sha256, as bandeiras ext_aescala_410_*, as falas por sha256, os numeros recalculados (tres faces de 1/2: duas conjugadas pesam 1; a caida nao conjuga; 1/3 caiu; o Nome normalizado 2/3; a ponte da escala), a frase canonica do Clay (D84) e a forma da D83 -- validade no kernel; a creditacao e' do Clay --,
    o gate congelado, os nomes RATIFICADOS (D87) e os nomes NOVOS da pedra (R3, R4 e R5): RATIFICADOS em 10/11 (D101), salvo o quarto teorema da clausula, NOMEADO pelo operador (D108), e os dois auxiliares da autoria, pendentes. Nenhuma chave antiga muda. Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate. Validade no kernel nao e' creditacao."""
    c_ = _V410_AESCALA_CONTRACT; t_ = _V410_AESCALA_TEXT
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
    out_ = {"all_verified": False, "runtime_executed": False, "does_not_gate_core": True, "estatuto": t_["estatuto"], "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"],
            "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "modulo": c_["modulo"], "ancora_principal": c_["ancora_principal"], "ancoras_de_secao": list(c_["ancoras_de_secao"]), "n_ancoras": c_["n_ancoras"], "n_flags": c_["n_flags"], "flag_prefix": c_["flag_prefix"],
            "nomes": list(c_["nomes"]), "n_nomes": c_["n_nomes"], "nomes_ratificados": c_["nomes_ratificados"], "estatuto_dos_nomes": c_["estatuto_dos_nomes"], "nomes_novos_da_pedra": list(c_["nomes_novos_da_pedra"]), "n_nomes_novos": c_["n_nomes_novos"], "campos_novos_da_estrutura": list(c_["campos_novos_da_estrutura"]),
            "estatuto_dos_nomes_ratificados_d101": c_["estatuto_dos_nomes_ratificados_d101"], "ratificacao_pendente": dict(c_["ratificacao_pendente"]), "ponte": dict(c_["ponte"]), "n_falas": c_["n_falas"], "ratificacao": dict(c_["ratificacao"]), "numeros": dict(c_["numeros"]), "frase_canonica_pt": c_["frase_canonica_pt"], "frase_canonica_en": c_["frase_canonica_en"],
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
