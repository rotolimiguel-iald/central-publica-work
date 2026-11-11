# -*- coding: utf-8 -*-
"""_r5ag_05_runtime_aescala_v410.py -- R5 (D100 e D101; ADENDOS 5 e 6): runtime_aescala_v410.py (o registro a_escala_v410; as checagens passam de 12 a 13). A c13 (a clausula do Tetelestai em 1 - beta, com beta de RUNTIME): a constante, s*, as desigualdades nas instancias
(com solucao, de UMA solucao, o adversario), o par da matriz-S, a constante independente do tamanho, a reconstrucao em norma ao quadrado, o CONTROLE NEGATIVO (uma oitava a menos viola a desigualdade) e o contraexemplo da hipotese s >= 0 -- calculada DENTRO de
_v410_aescala_ciclo (sem funcao de topo nova). A c2 confere os teoremas e os auxiliares da R5 entre as ancoras novas; a c5 as falas 27 e 28; a c8 toda folha que anuncia os teoremas novos (FRASE da lingua + CLAUSULA do limite + s >= 0), a presenca das frases e a citacao do dispositivo so'
com as ressalvas; a c11 a ratificacao D101 (a fala por sha256 == o pino == o cabecalho da pedra; os 22 nomes e os 3 campos; os 2 pendentes; nunca o estatuto antigo). beta so' por nome (o `beta_` que a mechanics recebe e' o de runtime)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar

T = []

# ---- 1. cabecalhos
T.append(('''# RATIFICADOS pelo operador em 09/11/2026 («ratifico tudo», D87); os nomes NOVOS da pedra (R3) ficam [DECLARADO, a ratificar].''',
          '''# RATIFICADOS pelo operador em 09/11/2026 («ratifico tudo», D87); os nomes NOVOS da pedra (R3, R4 e R5) foram RATIFICADOS pelo operador em 10/11/2026 (D101), salvo os dois lemas auxiliares da autoria, que ficam [DECLARADO pela autoria].''', 1))
T.append(('''# Fonte autoral deste bloco: runtime_aescala_v410.py (cadeia_de_selo/v410); o contrato''',
          '''# (R5, D100 e D101, ADENDOS 5 e 6) a c13 confere a CLAUSULA DO TETELESTAI em 1 - beta com o beta de RUNTIME (a constante, o tempo s*, as desigualdades nas instancias com solucao, de UMA solucao e adversaria, o par da matriz-S, a constante independente do tamanho, a reconstrucao, o controle negativo e o contraexemplo da hipotese s >= 0); c8 tambem confere,
# ao lado de TODA folha que anuncia os teoremas novos, a FRASE da lingua, a CLAUSULA do limite e a hipotese s >= 0, e a citacao do dispositivo so' com as ressalvas; c2 os teoremas e auxiliares da R5; c5 as falas 27 e 28; c11 a ratificacao D101 (a fala por sha256 == o pino == o cabecalho da pedra) e os dois auxiliares pendentes
# Fonte autoral deste bloco: runtime_aescala_v410.py (cadeia_de_selo/v410); o contrato''', 1))

# ---- 2. _v410_aescala_ciclo: a clausula do Tetelestai em 1 - beta (dentro do ciclo; sem funcao de topo nova)
T.append(('''def _v410_aescala_ciclo(cic_):''', '''def _v410_aescala_ciclo(cic_, tet_=None, beta_=None):''', 1))
T.append(('''o brilho e^(-s k) em s = n ln 2 + epsilon e o produto dos brilhos em n ln 2 e em epsilon. Devolve os numeros medidos e o ok."""''',
          '''o brilho e^(-s k) em s = n ln 2 + epsilon e o produto dos brilhos em n ln 2 e em epsilon. Devolve os numeros medidos e o ok.
    (R5, D100) Com `tet_` (as instancias da clausula do contrato) e `beta_` (o beta de RUNTIME) calcula tambem a CLAUSULA DO TETELESTAI em 1 - beta (o_tetelestai_e_um_menos_beta; o_sistema_reconhece_a_singularidade_do_sinal; beta_e_o_operador_modular_do_tetelestai; a_informacao_completa_se_reconstroi;
    ate_meio_o_tempo_do_tetelestai_nao_e_negativo): com a constante ln((1 - beta)/beta) e s* = n ln 2 + constante, (1 - beta) Z(s*) <= o numero de solucoes e Z(s*) - o numero de solucoes <= beta Z(s*); o par da matriz-S (sen^2 = beta, cos^2 = 1 - beta); a constante nao depende do tamanho; a reconstrucao em
    norma ao quadrado; o controle negativo (uma oitava a menos viola a desigualdade no adversario); o contraexemplo de s < 0. Devolve em res_["tetelestai"] os numeros e o ok."""''', 1))
T.append(('''    return {"n_bits": n_, "tamanho": N_, "s": s_, "epsilon": str(eps_),''', '''    res_ = {"n_bits": n_, "tamanho": N_, "s": s_, "epsilon": str(eps_),''', 1))
T.append(('''"produto_dos_brilhos_ok": bool(prod_), "ok": bool(ok_)}


def _v410_aescala_mechanics(''',
          '''"produto_dos_brilhos_ok": bool(prod_), "ok": bool(ok_)}
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
        ok_iv_ = bool(abs(R2_ - b_) <= tol_ and abs(T2_ - (1.0 - b_)) <= tol_ and abs(R2_ + T2_ - 1.0) <= tol_ and T2_ * Zc2_ <= Nc_ + tol_ and Zc2_ - Nc_ <= R2_ * Zc2_ + tol_)   # (iv) o par da matriz-S: |R|^2 = beta, |T|^2 = 1 - beta; |T|^2 Z <= numero de solucoes; o residuo <= |R|^2 Z
        ms_ = [int(x_) for x_ in tet_["m_da_constante"]]
        ok_v_ = bool(ms_ and all(abs(((m_ * ln2_ + const_) - m_ * ln2_) - const_) <= tol_ for m_ in ms_))   # (v) a constante alem das m oitavas e' a mesma para todo m
        t2_ = sst_ / 2.0; ok_vi_ = bool(t2_ >= nt_ * ln2_ / 2.0 and t2_ >= nt_ * ln2_ / 2.0 + const_ / 2.0 - tol_ and (Zf_(com2_, 2.0 * t2_) - Nc_) / Nt_ <= (b_ / (1.0 - b_)) * (Nc_ / Nt_) + tol_)   # (vi) a reconstrucao: em norma ao quadrado, (Z(2t) - n_sol)/|X| <= (beta/(1 - beta)) n_sol/|X| (o quadrado da cota)
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


def _v410_aescala_mechanics(''', 1))
T.append(('''c11 os nomes RATIFICADOS (D87): cada um e' declaracao na pedra embutida; a fala da ratificacao embutida (sha256 == pino; o texto e' «ratifico tudo»); o cabecalho da pedra traz a ratificacao e o sha256 da fala; e os nomes NOVOS da pedra (R3), todos declaracoes na pedra embutida,
    com os campos novos da estrutura, ditos [DECLARADO, a ratificar] no registro, nunca ratificados; c12 beta so' por nome''',
          '''c11 os nomes RATIFICADOS (D87): cada um e' declaracao na pedra embutida; a fala da ratificacao embutida (sha256 == pino; o texto e' «ratifico tudo»); o cabecalho da pedra traz a ratificacao e o sha256 da fala; e os nomes NOVOS da pedra (R3, R4 e R5), todos declaracoes na pedra embutida,
    com os campos novos da estrutura, ditos RATIFICADOS em 10/11/2026 (D101: a fala 28 por sha256 == o pino == o cabecalho da pedra; a regra do nome), os dois auxiliares da autoria ditos [DECLARADO pela autoria] e unicos pendentes; c12 beta so' por nome''', 1))
T.append(('''(nenhum literal na pedra), nenhuma chave antiga muda, o registro nao gateia o core."""''',
          '''(nenhum literal na pedra), nenhuma chave antiga muda, o registro nao gateia o core; c13 a clausula do Tetelestai em 1 - beta com beta de runtime (R5, D100)."""''', 1))

# ---- 3. c2: os teoremas e auxiliares da R5 entre as ancoras novas
T.append(('''    c2_ok_ = kf_.get("all_verified") is True and len(anc_)''',
          '''    r5_ = {n_: bool(anc_.get(c_["mod"] + "." + n_) is True and (c_["mod"] + "." + n_) in c_["ancoras_novas"]) for n_ in list(c_["teoremas_r5"]) + list(c_["auxiliares_r5"])}   # (R5, D100: os teoremas da clausula do Tetelestai e os dois lemas auxiliares entre as ancoras novas, no trio, com bandeira)
    c2_ok_ = kf_.get("all_verified") is True and len(anc_)''', 1))
T.append(('''and len(c_["ancoras_novas"]) == c_["n_nomes_novos"] == len(c_["nomes_novos_a_ratificar"])   # (R2, B1: o numero de ancoras novas == o de nomes novos a ratificar)''',
          '''and len(c_["ancoras_novas"]) == c_["n_nomes_novos"] == len(c_["nomes_novos_a_ratificar"]) and bool(r5_) and all(r5_.values())   # (R2, B1: o numero de ancoras novas == o de nomes novos; R5: os da R5 entre elas)''', 1))

# ---- 4. c5: a ratificacao de 10/11 (D101) entre as falas
T.append(('''    c5_ok_ = len(ver_) == c_["n_falas"] == len(c_["falas"]) and bool(ver_) and all(ver_.values()) and c_["chave_ratificacao"] in ver_''',
          '''    c5_ok_ = len(ver_) == c_["n_falas"] == len(c_["falas"]) and bool(ver_) and all(ver_.values()) and c_["chave_ratificacao"] in ver_ and c_["chave_ratificacao_d101"] in ver_ and c_["chave_clausula_tetelestai"] in ver_   # (R5: as falas 27 e 28 entre as do registro)''', 1))

# ---- 5. c6: o ciclo com a clausula (a c13 le o resultado)
T.append(('''    cic_ = _v410_aescala_ciclo(c_["ciclo"])''', '''    cic_ = _v410_aescala_ciclo(c_["ciclo"], c_["tetelestai"], beta_)   # (R5: tambem a clausula do Tetelestai em 1 - beta, com o beta de RUNTIME)''', 1))

# ---- 6. c8: a clausula do Tetelestai (R5) ao lado de todo texto que a anuncia, as frases, e a citacao do dispositivo so' com as ressalvas
C8 = '''    # (R5, D100; ADENDO 5) a clausula do Tetelestai em 1 - beta: toda folha que ANUNCIA os teoremas novos (o nome de um teorema ou auxiliar da R5 junto de ln((1 - b)/b), ln((1 - beta)/beta), (1 - b)·Z ou (1 - beta)·Z) traz a FRASE da sua lingua (exata), a CLAUSULA do limite da mesma lingua e a hipotese do tempo (s >= 0);
    # o registro traz as frases (a clausula, a reconstrucao, a errata, o dispositivo) nas duas linguas; TODA folha com «ACOM Mirror» traz «[PILOTO][SIM]» e «nada ali valida fisica» (ou o equivalente em ingles) e nenhum padrao de desempenho (percentual, «x mais rapido», «N de N testes»)
    r5_nomes_ = tuple(c_["teoremas_r5"]) + tuple(c_["auxiliares_r5"])
    r5_marca_ = _re410.compile(r"ln\\s*\\(\\s*\\(\\s*1\\s*[\\u2212-]\\s*[b\\u03b2]\\s*\\)\\s*/\\s*[b\\u03b2]\\s*\\)|\\(\\s*1\\s*[\\u2212-]\\s*[b\\u03b2]\\s*\\)\\s*[\\u00b7*]\\s*Z")
    tet_pt_ = ws_(c_["frase_tetelestai_pt"]); tet_en_ = ws_(c_["frase_tetelestai_en"]); rec_pt_ = ws_(c_["frase_reconstroi_pt"]); rec_en_ = ws_(c_["frase_reconstroi_en"])
    e36_pt_ = ws_(c_["frase_e36_pt"]); e36_en_ = ws_(c_["frase_e36_en"]); dis_pt_ = ws_(c_["frase_dispositivo_pt"]); dis_en_ = ws_(c_["frase_dispositivo_en"])
    anuncia_r5_ = lambda x_: bool(any(n_ in x_ for n_ in r5_nomes_) and r5_marca_.search(x_))
    sem_r5_ = sorted(cam_ for cam_, x_ in folhas_ if anuncia_r5_(x_) and not ((tet_pt_ in x_ and clz_pt_ in x_) or (tet_en_ in x_ and clz_en_ in x_)))
    n_anunciam_r5_ = sum(1 for cam_, x_ in folhas_ if anuncia_r5_(x_))
    mir_ = [(cam_, x_) for cam_, x_ in folhas_ if "ACOM Mirror" in x_]
    mir_sem_ressalva_ = sorted(cam_ for cam_, x_ in mir_ if not ("[PILOTO][SIM]" in x_ and _re410.search(r"nada ali valida f[i\\u00ed]sica|nothing there validates physics", x_)))
    mir_com_desempenho_ = sorted(cam_ for cam_, x_ in mir_ if _re410.search(r"\\d+\\s*%|\\d+\\s*[x\\u00d7]\\s*(?:mais\\s+r[a\\u00e1]pid|faster)|\\b\\d+\\s+de\\s+\\d+\\s+testes\\b|\\b\\d+\\s+of\\s+\\d+\\s+tests\\b", x_, _re410.I))
    clausula_r5_ok_ = bool(n_anunciam_r5_ >= 3 and not sem_r5_ and "s \\u2265 0" in tet_pt_ and "s \\u2265 0" in tet_en_ and all(f_ in txt_ws_ for f_ in (tet_pt_, tet_en_, rec_pt_, rec_en_, e36_pt_, e36_en_, dis_pt_, dis_en_)) and bool(mir_) and not mir_sem_ressalva_ and not mir_com_desempenho_
                           and "[PILOTO][SIM]" in dis_pt_ and "[PILOTO][SIM]" in dis_en_ and "nada ali valida f\\u00edsica" in dis_pt_ and "nothing there validates physics" in dis_en_)
    c8_ok_ = d83_ in txt_ws_ and d83_ in body_ws_'''
T.append(('''    c8_ok_ = d83_ in txt_ws_ and d83_ in body_ws_''', C8, 1))
T.append(('''and "os_passos_sao_o_ciclo_ate_o_tetelestai" in txt_ws_ and clausula_ok_
''', '''and "os_passos_sao_o_ciclo_ate_o_tetelestai" in txt_ws_ and clausula_ok_ and clausula_r5_ok_
''', 1))

# ---- 7. c11: a ratificacao D101 e os dois auxiliares pendentes
T.append(('''                 and "DECLARADO" in est_novos_ and "a ratificar" in est_novos_ and "RATIFICADO" not in est_novos_.upper() and _re410.sub(r"\\s+", " ", est_novos_) in txt_ws_
                 and pend_.get("nomes_novos") == list(c_["nomes_novos_a_ratificar"]) and pend_.get("campos_novos_da_estrutura") == list(c_["campos_novos_da_estrutura"]) and pend_.get("estatuto") == est_novos_ and (t_.get("extras") or {}).get("ratificacao_pendente") == pend_)''',
          '''                 and "RATIFICADOS pelo operador em 10/11/2026" in est_novos_ and "DECLARADO" not in est_novos_ and "a ratificar" not in est_novos_ and _re410.sub(r"\\s+", " ", est_novos_) in txt_ws_
                 and pend_.get("nomes_novos") == list(c_["nomes_pendentes"]) and pend_.get("campos_novos_da_estrutura") == [] and pend_.get("estatuto") == c_["estatuto_dos_nomes_pendentes"] and "DECLARADO pela autoria" in pend_.get("estatuto", "") and pend_.get("decisao") == "D101" and (t_.get("extras") or {}).get("ratificacao_pendente") == pend_)''', 1))
T.append(('''    c11_ok_ = (len(decl_) == c_["n_nomes"] == len(c_["nomes"])''',
          '''    # (R5, D101) a ratificacao de 10/11: os 22 nomes e os 3 campos RATIFICADOS (declaracoes na pedra), os 2 auxiliares pendentes (declaracoes na pedra, [DECLARADO pela autoria], nunca ratificados), a fala 28 embutida por sha256 == o pino == o cabecalho da pedra, a regra do nome no texto, e NUNCA o estatuto antigo
    rd_ = c_["ratificacao_d101"]; rv2_ = _V410_VERBATINS2.get(c_["chave_ratificacao_d101"]) or {}; txt2_ = str(rv2_.get("text", ""))
    rat_decl_ = {n_: rx_decl_(n_) for n_ in c_["nomes_ratificados_d101"]}; pen_decl_ = {n_: rx_decl_(n_) for n_ in c_["nomes_pendentes"]}
    rat_d101_ok_ = bool(rv2_.get("sha256") == rd_["sha256"] and _h410.sha256(txt2_.encode("utf-8")).hexdigest() == rd_["sha256"] and rd_["trecho"] in txt2_ and rd_["sha256"] in body_ws_ and "RATIFICADOS pelo operador em 10/11/2026" in body_ws_ and rd_["decisao"] == "D101"
                        and bool(rat_decl_) and all(rat_decl_.values()) and bool(pen_decl_) and all(pen_decl_.values()) and set(c_["nomes_ratificados_d101"]) | set(c_["nomes_pendentes"]) == set(c_["nomes_novos_a_ratificar"]) and not (set(c_["nomes_ratificados_d101"]) & set(c_["nomes_pendentes"]))
                        and c_["campos_ratificados_d101"] == list(c_["campos_novos_da_estrutura"]) and all(campos_.get(f_) is True for f_ in c_["campos_ratificados_d101"]) and set(c_["teoremas_r5"]) <= set(c_["nomes_ratificados_d101"]) and set(c_["auxiliares_r5"]) == set(c_["nomes_pendentes"])
                        and ws_(c_["frase_nomes_ratificados_d101_pt"]) in txt_ws_ and ws_(c_["frase_nomes_ratificados_d101_en"]) in txt_ws_ and ws_(rd_["trecho"]) in txt_ws_ and "[DECLARADO, a ratificar]" not in txt_json_ and "DECLARADO pela autoria" in txt_ws_
                        and all(n_ not in c_["nomes_ratificados_d101"] for n_ in c_["nomes_pendentes"]))
    c11_ok_ = (len(decl_) == c_["n_nomes"] == len(c_["nomes"])''', 1))
T.append(('''and "RATIFICADOS" in c_["estatuto_dos_nomes"] and novos_ok_ and seis_ok_)''', '''and "RATIFICADOS" in c_["estatuto_dos_nomes"] and novos_ok_ and seis_ok_ and rat_d101_ok_)''', 1))

# ---- 8. as descricoes das checagens e o c13
T.append(('''as ancoras novas == os nomes novos a ratificar (R2, B1)" % c_["n_ancoras"]''', '''as ancoras novas == os nomes novos (R2, B1), com os teoremas e os auxiliares da R5 entre elas (D100)" % c_["n_ancoras"]''', 1))
T.append(('''(o texto embutido == o pino; os trechos citados verbatim), inclusive a ratificacao"''', '''(o texto embutido == o pino; os trechos citados verbatim), inclusive a ratificacao de 09/11 (D87) e a de 10/11 (D101), e a clausula do Tetelestai"''', 1))
T.append(('''a clausula do limite do teorema do Tetelestai (ADENDO 4, D99), PT e EN, ao lado de todo texto que o anuncia", "ok": bool(c8_ok_)}''',
          '''a clausula do limite do teorema do Tetelestai (ADENDO 4, D99), PT e EN, ao lado de todo texto que o anuncia; a clausula do Tetelestai em 1 - beta (R5, D100: a frase da lingua, a clausula do limite e a hipotese s >= 0 ao lado de toda folha que anuncia os teoremas novos; a errata e a citacao do dispositivo, esta so' com as ressalvas: [PILOTO][SIM], nada ali valida fisica, nenhum numero de desempenho)", "ok": bool(c8_ok_)}''', 1))
T.append(('''cada um e' declaracao na pedra embutida e o registro os diz [DECLARADO, a ratificar], nunca ratificados; os seis nomes de enunciado mudado ditos (R2, B3)" % (c_["n_nomes"], c_["n_nomes_novos"], len(c_["campos_novos_da_estrutura"])), "ok": bool(c11_ok_)},''',
          '''cada um e' declaracao na pedra embutida e o registro os diz RATIFICADOS pelo operador em 10/11/2026 (D101: a fala por sha256 == o pino == o cabecalho da pedra; a regra do nome), nunca com o estatuto antigo; os %d auxiliares da autoria ditos [DECLARADO pela autoria], os unicos pendentes; os seis nomes de enunciado mudado ditos com a forma vigente (R2, B3; D101)" % (c_["n_nomes"], c_["n_nomes_novos"], len(c_["campos_novos_da_estrutura"]), len(c_["nomes_pendentes"])), "ok": bool(c11_ok_)},''', 1))
T.append(('''        {"id": "c12", "descricao": "beta so' por nome (nenhum literal na pedra; o registro nem o usa); nenhuma chave antiga muda; o registro nao gateia o core", "ok": bool(c12_ok_)},
    ]''',
          '''        {"id": "c12", "descricao": "beta so' por nome (nenhum literal na pedra; o registro nem o usa); nenhuma chave antiga muda; o registro nao gateia o core", "ok": bool(c12_ok_)},
        {"id": "c13", "descricao": "a clausula do Tetelestai em 1 - beta (R5, D100), com o beta de RUNTIME (alfa CODATA x raiz de e): a constante ln((1 - beta)/beta) e s* = n ln 2 + constante; (1 - beta) Z(s*) <= o numero de solucoes e Z(s*) - o numero de solucoes <= beta Z(s*) na instancia com solucao; o pixel do Nome carrega pelo menos 1 - beta na de UMA solucao; o par da matriz-S (sen^2 = beta, cos^2 = 1 - beta; |T|^2 Z <= o numero de solucoes; o residuo <= |R|^2 Z); a constante e' a mesma para m = 1, 3, 8 oitavas; a reconstrucao em norma ao quadrado; o CONTROLE NEGATIVO (no adversario vale em s* e uma oitava a menos VIOLA); o contraexemplo da hipotese s >= 0 (b = 9/10, n = 1, custos 0 e 2: o limiar e' negativo e nele a desigualdade falha; com s = 0 vale)", "ok": bool(cic_["tetelestai"]["ok"])},
    ]''', 1))
T.append(('''"ciclo": cic_, "tempo_pt_no_texto": tempo_pt_ in txt_ws_,''', '''"ciclo": cic_, "tetelestai": cic_["tetelestai"], "teoremas_r5": r5_, "clausula_r5": {"n_folhas_que_anunciam": n_anunciam_r5_, "folhas_que_anunciam_sem_a_forma": sem_r5_, "n_folhas_com_acom_mirror": len(mir_), "acom_mirror_sem_ressalva": mir_sem_ressalva_, "acom_mirror_com_desempenho": mir_com_desempenho_, "ok": bool(clausula_r5_ok_)}, "ratificacao_d101": {"ok": bool(rat_d101_ok_), "fala_sha256": rd_["sha256"], "n_nomes_ratificados_declarados": sum(1 for v_ in rat_decl_.values() if v_), "n_nomes_ratificados": len(rat_decl_), "n_pendentes_declarados": sum(1 for v_ in pen_decl_.values() if v_), "pendentes": list(c_["nomes_pendentes"])}, "tempo_pt_no_texto": tempo_pt_ in txt_ws_,''', 1))
aplicar("runtime_aescala_v410.py", T)
