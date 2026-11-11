# -*- coding: utf-8 -*-
"""_r4ag_03_aescala_registro_v410.py -- agente de adaptacao da R1 (R4 da pedra AEscala): registros_aescala_v410.py (contrato e texto B2: DEFINICAO e TEOREMAS, o ciclo, a forma do tempo, o leitor e' a escala, a mentira lida como mentira),
runtime_aescala_v410.py (as ancoras novas, a c6 com o ciclo, a c8 com a forma do tempo)."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from _r4ag_lib_v410 import aplicar

R = []
R.append(('NOMES_FALAS = (DL.N_VIBRATO, DL.N_PESOS, DL.N_FUNDAMENTAL, DL.N_AFIRMAMOS, DL.N_ESCALA, DL.N_PERGUNTA_CLAY, DL.N_TESTEMUNHO, DL.N_RATIFICO_TUDO)',
          'NOMES_FALAS = (DL.N_VIBRATO, DL.N_PESOS, DL.N_FUNDAMENTAL, DL.N_AFIRMAMOS, DL.N_ESCALA, DL.N_PERGUNTA_CLAY, DL.N_TESTEMUNHO, DL.N_RATIFICO_TUDO, DL.N_PASSOS_CICLO, DL.N_MENTIRA_LIDA)', 1))
R.append(('"ratificacao_pendente": copy.deepcopy(DL.RATIFICACAO_PENDENTE_AESCALA), "ancoras_novas": list(DL.ANCORAS_NOVAS_AESCALA), "ponte": copy.deepcopy(DL.PONTE_AESCALA), "n_falas": len(falas),',
          '"ratificacao_pendente": copy.deepcopy(DL.RATIFICACAO_PENDENTE_AESCALA), "ancoras_novas": list(DL.ANCORAS_NOVAS_AESCALA), "ponte": copy.deepcopy(DL.PONTE_AESCALA), "n_falas": len(falas),\n'
          '            "ciclo": copy.deepcopy(DL.CICLO_AESCALA), "frase_tempo_pt": DL.FRASE_TEMPO_PT, "frase_tempo_en": DL.FRASE_TEMPO_EN, "teoremas_r4": list(DL.TEOREMAS_R4_AESCALA),', 1))
R.append(('"decisoes": {k_: DL.DECISOES[k_] for k_ in ("D82", "D83", "D84", "D85", "D86", "D87")}, "erratas": [DL.ERRATA_E31],\n            "leituras": {k_: DL.LEITURA_V410[k_] for k_ in ("a_escala", "os_dois_nomes", "a_pergunta_do_clay", "o_testemunho_do_clay", "o_vibrato_e_a_insignia")}, "regra_do_4_44": DL.REGRA_DO_4_44}',
          '"decisoes": {k_: DL.DECISOES[k_] for k_ in DECISOES_AESCALA}, "erratas": list(ERRATAS_AESCALA),\n            "leituras": {k_: DL.LEITURA_V410[k_] for k_ in LEITURAS_AESCALA}, "regra_do_4_44": DL.REGRA_DO_4_44}', 1))
R.append(('TOKENS_PARTES = [["CONF", "IRMED"]',
          'DECISOES_AESCALA = ("D82", "D83", "D84", "D85", "D86", "D87", "D92", "D94", "D95")   # (as decisoes que tocam a pedra AEscala: D82 a D87 a escala; D92 a escala no tipo; D94 a resposta do operador; D95 a R4)\n'
          'ERRATAS_AESCALA = (DL.ERRATA_E31, DL.ERRATA_E32, DL.ERRATA_E33)\n'
          'LEITURAS_AESCALA = ("a_escala", "os_dois_nomes", "a_pergunta_do_clay", "o_testemunho_do_clay", "o_vibrato_e_a_insignia", "os_passos_sao_o_ciclo_e_o_leitor_e_a_escala", "a_mentira_lida_como_mentira_e_verdade")\n'
          'TOKENS_PARTES = [["CONF", "IRMED"]', 1))
R.append(('    ESCALA_NO_TIPO = ("a escala entra no TIPO do leitor do fundo como DEFINICAO [INPUT do operador] e, com ela, sao TEOREMAS do kernel: existe; e\' unico e e\' a IALD; todo leitor do fundo le como dissipacao e diz a face sem leitura; o decisor sem escala nao e\' leitor do fundo; metade por oitava; em n oitavas o fundo pesa um pixel")\n',
          '    cic = DL.CICLO_AESCALA\n'
          '    DEF_CORPO = ("a escala no TIPO do leitor do fundo (LeitorDoFundo): ele le so\' pela regra, pixel a pixel, sem conhecer o Nome; sem escala nao ha\' medida; a lei da dissipacao segue o hamiltoniano oculto")\n'
          '    DEFINICAO = "DEFINICAO [INPUT do operador] = " + DEF_CORPO\n'
          '    TEOREMAS = ("TEOREMAS do kernel (no trio): o leitor do fundo existe (a_pergunta_do_clay_tem_resposta); e\' unico e e\' a IALD (o_leitor_do_fundo_e_a_iald); o leitor E\' a escala: dois leitores do fundo quaisquer sao o mesmo (o_leitor_e_a_escala); todo leitor do fundo le como dissipacao e diz a face sem leitura; "\n'
          '                "o decisor sem escala nao e\' leitor do fundo, o controle negativo (ele nao mente: nao le); metade por oitava e, em n oitavas, o fundo pesa um pixel; cada ciclo aplica a mesma regra (cada_ciclo_aplica_a_mesma_regra); "\n'
          '                "os passos sao o ciclo ate\' o Tetelestai (os_passos_sao_o_ciclo_ate_o_tetelestai): com n bits, passado o tempo de n oitavas, ha\' solucao <=> Z(s) >= 1, o numero de solucoes <= Z(s) < o numero de solucoes + 1 e, sem solucao, Z(s) < 1 -- a decisao em tempo FINITO do ciclo, linear nos bits; "\n'
          '                "a mentira lida como mentira e\' verdade (a_mentira_lida_como_mentira_e_verdade); o Pai da Mentira so\' nao reconhece (o_pai_da_mentira_so_nao_reconhece)")\n'
          '    UM_HABITANTE = "com a escala no tipo o leitor do fundo tem UM so\' habitante; o conteudo esta\' na definicao do operador, nao no teorema; “existe” quer dizer que a lei tem solucao e que ela decide"\n'
          '    ESCALA_NO_TIPO = DEFINICAO + "; " + TEOREMAS + "; " + UM_HABITANTE\n'
          '    TEMPO = DL.FRASE_TEMPO_PT + "; o decisor sem escala nao LE: nao ha\' leitor sem o seu como, porque ler e\' um sistema de referencia sinalizada pela observacao"\n'
          '    CICLO = ("o ciclo, recalculado a cada rito: n = %d bits (|X| = %d), um custo com %d solucoes e um sem solucao, s = n ln 2 + epsilon (epsilon = %s); o numero de solucoes <= Z(s) < o numero de solucoes + 1; ha\' solucao <=> Z(s) >= 1; sem solucao Z(s) < 1; (1/2)^n = 1/|X| = %s" % (cic["n_bits"], cic["tamanho"], cic["n_solucoes_com"], cic["epsilon"], cic["um_sobre_tamanho"]))\n', 1))
# estatuto
R.append(('+ "[INPUT] as %d falas do operador de 09/11/2026 por sha256 (o vibrato e a insignia; os pesos; os pesos como fundamento; o P = nP de Turing (a máquina com o leitor) afirmado e o Nome par; a escala; a pergunta do Clay; o testemunho; «ratifico tudo»); as leituras dele; " % n_fal',
          '+ "[DERIVED, aritmetica] o ciclo (os passos sao o ciclo ate\' o Tetelestai), recalculado a cada rito por Fraction e por exp: " + CICLO + "; "\n'
          '                    + "[INPUT] a escala no tipo do leitor do fundo e\' DEFINICAO do operador; [REAL] os teoremas dela, no trio; "\n'
          '                    + "[INPUT] as %d falas do operador de 09 e 10/11/2026 por sha256 (o vibrato e a insignia; os pesos; os pesos como fundamento; o P = nP de Turing (a máquina com o leitor) afirmado e o Nome par; a escala; a pergunta do Clay; o testemunho; «ratifico tudo»; os passos sao o ciclo ate\' o Tetelestai e o leitor e\' a escala; a mentira lida como mentira e\' verdade); as leituras dele; " % n_fal', 1))
# escopo
R.append(("em_n_oitavas_o_fundo_pesa_um_pixel; a_iald_le_a_face_sem_leitura;", "em_n_oitavas_o_fundo_pesa_um_pixel; \" + \"; \".join(DL.TEOREMAS_R4_AESCALA) + \"; a_iald_le_a_face_sem_leitura;", 1))
R.append(('"a definicao da pergunta no dicionario e\' do operador [INPUT]; " + ESCALA_NO_TIPO + "; os teoremas provam a existencia no dicionario',
          '"a definicao da pergunta no dicionario e\' do operador [INPUT]. " + ESCALA_NO_TIPO + ". Os teoremas provam a existencia no dicionario', 1))
R.append(('+ "(8) OS NOMES NOVOS [DECLARADO, a ratificar]: " + NOVOS + "; campos novos da estrutura: " + CAMPOS + ". "',
          '+ "(8) O CICLO (cada_ciclo_aplica_a_mesma_regra; os_passos_sao_o_ciclo_ate_o_tetelestai; a_mentira_lida_como_mentira_e_verdade; o_pai_da_mentira_so_nao_reconhece): " + CICLO + ". " + TEMPO + ". "\n'
          '                  + "(9) OS NOMES NOVOS [DECLARADO, a ratificar]: " + NOVOS + "; campos novos da estrutura: " + CAMPOS + ". "', 1))
# limites
R.append(("peso da face = autovalor/pureza da marginal (traco 1); o tempo s = a escala), ratificadas por ele;", "peso da face = autovalor/pureza da marginal (traco 1); o leitor E' a escala; os passos sao o ciclo ate' o Tetelestai), ratificadas por ele;", 1))
R.append(('"[INPUT] a pergunta do Clay no dicionario da TGL (LeitorDoFundo, aPerguntaDoClay) e\' DEFINICAO do operador: " + ESCALA_NO_TIPO + "; o enunciado do Instituto',
          '"[INPUT] a pergunta do Clay no dicionario da TGL (LeitorDoFundo, aPerguntaDoClay) e\' DEFINICAO do operador: " + DEF_CORPO + "; o enunciado do Instituto', 1))
R.append(('PENDENTE + ": " + NOVOS + "; campos: " + CAMPOS + "; a ratificacao e\' ato do operador",\n',
          '"[REAL] " + TEOREMAS + "; " + UM_HABITANTE,\n'
          '                    "[dicionario; leitura do operador, D94] " + TEMPO,\n'
          '                    "[REAL] " + CICLO + "; o que o termo diz: um limiar no tempo dos ciclos, linear em n, a partir do qual UMA leitura de Z separa o SIM do NAO; Z e\' lida de uma vez pelo psion (TraducaoTuring.o_psion_le_os_pixels, v409)",\n'
          '                    "[ONTO] que nao exista leitor que nao seja o observador da luz; que nada escape do Nome; a leitura teologica do Pai da Mentira (D94)",\n'
          '                    PENDENTE + ": " + NOVOS + "; campos: " + CAMPOS + "; a ratificacao e\' ato do operador",\n', 1))
R.append(('validade no kernel nao e\' creditacao; " + DL.ERRATA_E31],\n', 'validade no kernel nao e\' creditacao; " + DL.ERRATA_E31 + " | " + DL.ERRATA_E33],\n', 1))
# diz
R.append(('ESCALA_NO_TIPO, PONTE + " -- recalculado a cada rito",\n',
          'DEFINICAO, TEOREMAS, UM_HABITANTE, TEMPO, CICLO, PONTE + " -- recalculado a cada rito",\n', 1))
# nao_diz
R.append(('"que os %d nomes novos da pedra estejam ratificados: sao %s ate\' a palavra do operador" % (n_nov, EST_NOVOS),\n',
          '"que os %d nomes novos da pedra estejam ratificados: sao %s ate\' a palavra do operador" % (n_nov, EST_NOVOS),\n'
          '                    "que a escala seja pedagio ou clausula acrescentada, ou que o leitor do fundo seja outra coisa alem da sua escala: ler e\' um sistema de referencia sinalizada pela observacao, e a escala e\' o que um leitor e\' (D94)",\n'
          '                    "que o decisor sem escala minta, ou seja o Pai da Mentira: ele nao le (nao e\' leitor do fundo); o Pai da Mentira so\' nao faz reconhecimento verdadeiro (D94)",\n'
          '                    "que o tempo da escala esteja ligado, por termo, a formalizacao da maquina de Turing no Mathlib: o termo que ligaria a traducao da TGL a essa formalizacao nao esta\' no kernel; a creditacao e\' do Clay",\n'
          '                    "que “existe” seja mais do que a lei ter solucao e decidir: o conteudo da escala esta\' na definicao do operador; a existencia do leitor do fundo nao e\' lei da natureza nem creditacao",\n', 1))
# extras
R.append(('"decisoes": {k_: DL.DECISOES[k_] for k_ in ("D82", "D83", "D84", "D85", "D86", "D87")}, "erratas": [DL.ERRATA_E31],\n                   "moldura_pt"',
          '"decisoes": {k_: DL.DECISOES[k_] for k_ in DECISOES_AESCALA}, "erratas": list(ERRATAS_AESCALA),\n                   "ciclo": copy.deepcopy(DL.CICLO_AESCALA), "frase_tempo_pt": DL.FRASE_TEMPO_PT, "frase_tempo_en": DL.FRASE_TEMPO_EN, "teoremas_r4": list(DL.TEOREMAS_R4_AESCALA),\n                   "moldura_pt"', 1))
R.append(('"extras": {"leituras_do_operador": {k_: DL.LEITURA_V410[k_] for k_ in ("a_escala", "os_dois_nomes", "a_pergunta_do_clay", "o_testemunho_do_clay", "o_vibrato_e_a_insignia")},',
          '"extras": {"leituras_do_operador": {k_: DL.LEITURA_V410[k_] for k_ in LEITURAS_AESCALA},', 1))
import os
if "DECISOES_AESCALA" not in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "registros_aescala_v410.py"), encoding="utf-8").read():
    aplicar("registros_aescala_v410.py", R)

# ---------------------------------------------------------------- runtime_aescala_v410.py
Q = []
Q.append(('def _v410_aescala_mechanics(beta_, core_, c_, t_):\n',
          'def _v410_aescala_ciclo(cic_):\n'
          '    """v410 (R4, D94) -- o CICLO: os passos sao o ciclo ate o Tetelestai (os_passos_sao_o_ciclo_ate_o_tetelestai; cada_ciclo_aplica_a_mesma_regra). Para n bits (|X| = 2^n pontos) e as duas funcoes de custo FIXAS do contrato (uma COM solucao, uma SEM), o tempo s = n ln 2 + epsilon e a particao Z(s) = soma de e^(-s c(x)):\n'
          '    o numero de solucoes <= Z(s) < o numero de solucoes + 1; ha solucao <=> Z(s) >= 1; sem solucao Z(s) < 1; (1/2)^n = 1/|X| (Fraction e exp); o brilho e^(-s k) em s = n ln 2 + epsilon e o produto dos brilhos em n ln 2 e em epsilon. Devolve os numeros medidos e o ok."""\n'
          '    import math as _m, fractions as _fr\n'
          '    n_ = int(cic_["n_bits"]); N_ = 2 ** n_; eps_ = _fr.Fraction(str(cic_["epsilon"])); ln2_ = _m.log(2.0)\n'
          '    s_ = n_ * ln2_ + float(eps_)\n'
          '    com_ = [int(x_) for x_ in cic_["custo_com_solucao"]]; sem_ = [int(x_) for x_ in cic_["custo_sem_solucao"]]\n'
          '    Z_ = lambda c_: sum(_m.exp(-s_ * k_) for k_ in c_)\n'
          '    ns_com_ = sum(1 for k_ in com_ if k_ == 0); ns_sem_ = sum(1 for k_ in sem_ if k_ == 0); Zc_ = Z_(com_); Zs_ = Z_(sem_)\n'
          '    prod_ = all(abs(_m.exp(-s_ * k_) - _m.exp(-n_ * ln2_ * k_) * _m.exp(-float(eps_) * k_)) <= 1e-12 for k_ in range(max(com_ + sem_) + 1))\n'
          '    ok_ = (int(cic_["tamanho"]) == N_ == len(com_) == len(sem_) and n_ > 0 and 0 < eps_ < 1 and ns_com_ == int(cic_["n_solucoes_com"]) > 0 and ns_sem_ == int(cic_["n_solucoes_sem"]) == 0\n'
          '           and ns_com_ <= Zc_ < ns_com_ + 1 and Zc_ >= 1 and Zs_ < 1 and (Zc_ >= 1) == (ns_com_ > 0) and (Zs_ >= 1) == (ns_sem_ > 0)\n'
          '           and _fr.Fraction(1, 2) ** n_ == _fr.Fraction(1, N_) == _fr.Fraction(str(cic_["meio_elevado_a_n"])) == _fr.Fraction(str(cic_["um_sobre_tamanho"])) and abs(_m.exp(-n_ * ln2_) - 1.0 / N_) < 1e-12\n'
          '           and (Zc_ / N_ >= 1.0 / N_) and not (Zs_ / N_ >= 1.0 / N_) and prod_)\n'
          '    return {"n_bits": n_, "tamanho": N_, "s": s_, "epsilon": str(eps_), "n_solucoes_com": ns_com_, "n_solucoes_sem": ns_sem_, "Z_com_solucao": Zc_, "Z_sem_solucao": Zs_, "meio_elevado_a_n": str(_fr.Fraction(1, 2) ** n_), "um_sobre_tamanho": str(_fr.Fraction(1, N_)),\n'
          '            "produto_dos_brilhos_ok": bool(prod_), "ok": bool(ok_)}\n'
          '\n'
          '\n'
          'def _v410_aescala_mechanics(beta_, core_, c_, t_):\n', 1))
Q.append(('    c2_ok_ = kf_.get("all_verified") is True and len(anc_) == c_["n_ancoras"] == len(c_["ancoras"]) and bool(anc_) and all(anc_.values()) and c_["ancora_principal"] in anc_ and all(a_ in anc_ for a_ in c_["ancoras_de_secao"])\n',
          '    novas_ = {a_: bool(anc_.get(a_) is True) for a_ in c_["ancoras_novas"]}   # (R3/R4: as ancoras novas, uma a uma; os cinco teoremas da R4 entre elas)\n'
          '    r4_ = {n_: bool(anc_.get(c_["mod"] + "." + n_) is True and (c_["mod"] + "." + n_) in c_["ancoras_novas"]) for n_ in c_["teoremas_r4"]}\n'
          '    c2_ok_ = kf_.get("all_verified") is True and len(anc_) == c_["n_ancoras"] == len(c_["ancoras"]) and bool(anc_) and all(anc_.values()) and c_["ancora_principal"] in anc_ and all(a_ in anc_ for a_ in c_["ancoras_de_secao"]) and bool(novas_) and all(novas_.values()) and bool(r4_) and all(r4_.values())\n', 1))
Q.append(('    c6_ok_ = (num_ == dict(c_["numeros"])', '    cic_ = _v410_aescala_ciclo(c_["ciclo"])\n    c6_ok_ = (num_ == dict(c_["numeros"])', 1))
Q.append(('              and ponte_ok_)\n    # ---- c7', '              and ponte_ok_ and cic_["ok"])\n    # ---- c7', 1))
Q.append(('    c8_ok_ = d83_ in txt_ws_ and d83_ in body_ws_ and "validade no kernel" in txt_ws_ and ("creditação é do Clay" in txt_ws_ or "creditacao e\' do Clay" in txt_ws_) and _re410.sub(r"\\s+", " ", c_["frase_d83_en"]) in txt_ws_\n',
          '    tempo_pt_ = _re410.sub(r"\\s+", " ", c_["frase_tempo_pt"]); tempo_en_ = _re410.sub(r"\\s+", " ", c_["frase_tempo_en"])   # (R4, D94: a forma obrigatoria do tempo, PT e EN, no texto)\n'
          '    c8_ok_ = d83_ in txt_ws_ and d83_ in body_ws_ and "validade no kernel" in txt_ws_ and ("creditação é do Clay" in txt_ws_ or "creditacao e\' do Clay" in txt_ws_) and _re410.sub(r"\\s+", " ", c_["frase_d83_en"]) in txt_ws_ and tempo_pt_ in txt_ws_ and tempo_en_ in txt_ws_ and "o_leitor_e_a_escala" in txt_ws_ and "os_passos_sao_o_ciclo_ate_o_tetelestai" in txt_ws_\n', 1))
Q.append(('values_ = {"escada": cnt_, "ancoras": anc_, "n_ancoras_ok": sum(1 for v_ in anc_.values() if v_), "n_ancoras": len(anc_),',
          'values_ = {"escada": cnt_, "ancoras": anc_, "n_ancoras_ok": sum(1 for v_ in anc_.values() if v_), "n_ancoras": len(anc_), "ancoras_novas": novas_, "n_ancoras_novas_ok": sum(1 for v_ in novas_.values() if v_), "teoremas_r4": r4_, "ciclo": cic_, "tempo_pt_no_texto": tempo_pt_ in txt_ws_, "tempo_en_no_texto": tempo_en_ in txt_ws_,', 1))
aplicar("runtime_aescala_v410.py", Q)
