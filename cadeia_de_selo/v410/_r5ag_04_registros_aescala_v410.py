# -*- coding: utf-8 -*-
"""_r5ag_04_registros_aescala_v410.py -- R5 (D100 e D101; ADENDOS 5 e 6): registros_aescala_v410.py: o contrato ganha as chaves novas (teoremas_r5, auxiliares_r5, tetelestai, as frases, ratificacao_d101, os 22 nomes ratificados, os 3 campos, os 2 pendentes, o pino citado do runner do ACOM Mirror);
NOMES_FALAS 10 -> 12; D100 e D101 nas decisoes, E36 e E37 nas erratas, as duas leituras novas; o texto: o estatuto, o escopo (um item novo, A CLAUSULA DO TETELESTAI, e o item dos nomes novos reescrito: RATIFICADOS em 10/11 e os 2 pendentes), os limites, diz, nao_diz e extras.
Regra do texto (c8): toda folha que anuncia os teoremas novos traz a FRASE da lingua e a CLAUSULA do limite juntas (ANUNCIO_PT / ANUNCIO_EN); as frases da errata e do dispositivo vao em folhas proprias (nao anunciam os teoremas)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar

T = []
T.append(('''DL.N_RATIFICO_TUDO, DL.N_PASSOS_CICLO, DL.N_MENTIRA_LIDA)   # (as falas que o registro pina por sha256;''',
          '''DL.N_RATIFICO_TUDO, DL.N_PASSOS_CICLO, DL.N_MENTIRA_LIDA, DL.N_CLAUSULA_TETELESTAI, DL.N_CONFIRMO_TUDO)   # (as falas que o registro pina por sha256;''', 1))
T.append(('''"D94", "D95", "D99")''', '''"D94", "D95", "D99", "D100", "D101")''', 1))
T.append(('''ERRATAS_AESCALA = (DL.ERRATA_E31, DL.ERRATA_E32, DL.ERRATA_E33, DL.ERRATA_E35)''', '''ERRATAS_AESCALA = (DL.ERRATA_E31, DL.ERRATA_E32, DL.ERRATA_E33, DL.ERRATA_E35, DL.ERRATA_E36, DL.ERRATA_E37)''', 1))
T.append(('''"os_passos_sao_o_ciclo_e_o_leitor_e_a_escala", "a_mentira_lida_como_mentira_e_verdade")''', '''"os_passos_sao_o_ciclo_e_o_leitor_e_a_escala", "a_mentira_lida_como_mentira_e_verdade", "a_clausula_do_tetelestai", "a_regra_do_nome")''', 1))

# ---- o contrato
T.append(('''por_nome[DL.N_RATIFICO_TUDO]["text"].strip() == DL.TRECHO_RATIFICO_TUDO
''', '''por_nome[DL.N_RATIFICO_TUDO]["text"].strip() == DL.TRECHO_RATIFICO_TUDO
    chave_rat_d101 = por_nome[DL.N_CONFIRMO_TUDO]["chave"]; chave_clausula = por_nome[DL.N_CLAUSULA_TETELESTAI]["chave"]   # (R5, D101 e D100: as falas 28 e 27)
    assert por_nome[DL.N_CONFIRMO_TUDO]["sha256"] == DL.RATIFICACAO_D101_SHA256 and DL.FRASE_NOMEIO_O_NUMERO_CORRIGE in por_nome[DL.N_CONFIRMO_TUDO]["text"] and por_nome[DL.N_CLAUSULA_TETELESTAI]["sha256"] == DL.CLAUSULA_TETELESTAI_SHA256 and DL.FRASE_UM_MENOS_BETATGL in por_nome[DL.N_CLAUSULA_TETELESTAI]["text"]
''', 1))
T.append(('''"leituras": {k_: DL.LEITURA_V410[k_] for k_ in LEITURAS_AESCALA}, "regra_do_4_44": DL.REGRA_DO_4_44}''',
          '''"leituras": {k_: DL.LEITURA_V410[k_] for k_ in LEITURAS_AESCALA}, "regra_do_4_44": DL.REGRA_DO_4_44,
            # (R5, D100 e D101) a clausula do Tetelestai em 1 - beta e a ratificacao de 10/11: tudo lido do delta (que le dos adendos, das falas e dos recibos)
            "teoremas_r5": list(DL.TEOREMAS_R5_AESCALA), "auxiliares_r5": list(DL.AUXILIARES_R5_AESCALA), "tetelestai": copy.deepcopy(DL.TETELESTAI_AESCALA),
            "frase_tetelestai_pt": DL.FRASE_TETELESTAI_PT, "frase_tetelestai_en": DL.FRASE_TETELESTAI_EN, "frase_reconstroi_pt": DL.FRASE_RECONSTROI_PT, "frase_reconstroi_en": DL.FRASE_RECONSTROI_EN,
            "frase_e36_pt": DL.FRASE_E36_PT, "frase_e36_en": DL.FRASE_E36_EN, "frase_dispositivo_pt": DL.FRASE_DISPOSITIVO_PT, "frase_dispositivo_en": DL.FRASE_DISPOSITIVO_EN,
            "frase_nomes_ratificados_d101_pt": DL.FRASE_NOMES_RATIFICADOS_D101_PT, "frase_nomes_ratificados_d101_en": DL.FRASE_NOMES_RATIFICADOS_D101_EN,
            "ratificacao_d101": {"fala": DL.N_CONFIRMO_TUDO, "sha256": DL.RATIFICACAO_D101_SHA256, "trecho": DL.FRASE_NOMEIO_O_NUMERO_CORRIGE, "quando": "10/11/2026 (~08:33)", "decisao": "D101",
                                 "o_que_ratifica": "os seis nomes de enunciado mudado (com o enunciado novo), os nomes novos das pedras R3 e R4 e os campos novos da estrutura, e os nomes da clausula do Tetelestai (R5) dados pela gerencia; pela regra do nome"},
            "chave_ratificacao_d101": chave_rat_d101, "chave_clausula_tetelestai": chave_clausula, "nomes_ratificados_d101": list(DL.NOMES_RATIFICADOS_D101_AESCALA), "campos_ratificados_d101": list(DL.CAMPOS_RATIFICADOS_D101_AESCALA),
            "nomes_pendentes": list(DL.NOMES_PENDENTES_AESCALA), "estatuto_dos_nomes_pendentes": DL.ESTATUTO_NOMES_PENDENTES_AESCALA, "acom_mirror_runner": dict(DL.ACOM_MIRROR_RUNNER)}''', 1))

# ---- o texto
T.append(('''    PENDENTE = ("%d nomes novos da pedra (a escala no tipo) e %d campos novos da estrutura, %s; os %d nomes anteriores seguem RATIFICADOS (D87); " % (n_nov, n_cam, EST_NOVOS, n_nom)) + DL.FRASE_SEIS_NOMES_PT
''',
          '''    RATIF = DL.FRASE_NOMES_RATIFICADOS_D101_PT; RATIFICADOS = ", ".join(DL.NOMES_RATIFICADOS_D101_AESCALA); PEND = ", ".join(DL.NOMES_PENDENTES_AESCALA)   # (R5, D101: os nomes novos da pedra e os campos, RATIFICADOS em 10/11; os dois auxiliares da autoria, pendentes)
    PENDENTE = RATIF + "; os %d nomes anteriores seguem RATIFICADOS (D87); " % n_nom + DL.FRASE_SEIS_NOMES_PT
    ANUNCIO_PT = DL.FRASE_TETELESTAI_PT + " " + DL.CLAUSULA_Z_PT + " " + DL.FRASE_RECONSTROI_PT   # (R5, D100: a FRASE da clausula do Tetelestai, a CLAUSULA do limite e a reconstrucao, juntas na MESMA folha: a c8 as exige juntas)
    ANUNCIO_EN = DL.FRASE_TETELESTAI_EN + " " + DL.CLAUSULA_Z_EN + " " + DL.FRASE_RECONSTROI_EN
    _ce = DL.TETELESTAI_AESCALA["contraexemplo_s_negativo"]
    NUMEROS_TET = ("[DERIVED] os numeros da clausula, recalculados a cada rito com beta de runtime (a c13): a constante e o tempo s* (n oitavas mais a constante); as desigualdades nas instancias (com solucao, de UMA solucao e adversaria); o par da matriz-S; a constante igual para m = " + ", ".join(str(m_) for m_ in DL.TETELESTAI_AESCALA["m_da_constante"])
                   + " oitavas; a reconstrucao em norma ao quadrado; o controle negativo (no adversario a desigualdade vale em s* e uma oitava a menos a VIOLA); o contraexemplo da hipotese s >= 0 (b = " + _ce["b"] + ", n = " + str(_ce["n_bits"]) + ", custos " + " e ".join(str(x_) for x_ in _ce["custos"]) + ")")
    CLAUSULA_ESTATUTO = ("[REAL] a clausula do Tetelestai em 1 - beta (R5, D100; " + ", ".join(DL.TEOREMAS_R5_AESCALA) + "): o limiar de tempo em n oitavas mais uma constante que so' depende de beta; " + NUMEROS_TET
                         + "; [INPUT/dicionario] a leitura do operador (que esse limiar E' o Tetelestai e que beta e' o seu operador modular); [PILOTO][SIM] a evidencia de dispositivo, so' como citacao")
''', 1))
T.append(('''+ "[INPUT] %s; " % R + PENDENTE + "; [DECLARADO -> REAL]''', '''+ "[INPUT] %s; " % R + PENDENTE + "; " + CLAUSULA_ESTATUTO + "; [DECLARADO -> REAL]''', 1))
T.append(('''                  + "(9) OS NOMES NOVOS [DECLARADO, a ratificar]: " + NOVOS + "; campos novos da estrutura: " + CAMPOS + ". "
''',
          '''                  + "(9) OS NOMES NOVOS, RATIFICADOS pelo operador em 10/11/2026 (D101), pela regra do nome: " + RATIFICADOS + "; campos novos da estrutura: " + CAMPOS + "; ainda [DECLARADO pela autoria], so' os auxiliares: " + PEND + ". "
                  + "(10) A CLAUSULA DO TETELESTAI (R5, D100; " + "; ".join(DL.TEOREMAS_R5_AESCALA) + "): " + ANUNCIO_PT + ". [INPUT/dicionario] " + DL.FRASE_E36_PT + ". [PILOTO][SIM] " + DL.FRASE_DISPOSITIVO_PT + ". " + NUMEROS_TET + ". "
''', 1))
T.append(('''as frases canonicas no texto e na pedra; o gate; os %d nomes ratificados e os %d nomes novos (declaracoes na pedra, ditos a ratificar). Nenhuma chave antiga muda." % (n_anc, n_fal, n_nom, n_nov),''',
          '''as frases canonicas no texto e na pedra; o gate; os %d nomes ratificados e os %d nomes novos (declaracoes na pedra, ditos RATIFICADOS em 10/11/2026, D101, salvo os %d auxiliares da autoria, ditos [DECLARADO pela autoria]); a clausula do Tetelestai em 1 - beta com beta de runtime (a c13). Nenhuma chave antiga muda." % (n_anc, n_fal, n_nom, n_nov, len(DL.NOMES_PENDENTES_AESCALA)),''', 1))
T.append(('''                    PENDENTE + ": " + NOVOS + "; campos: " + CAMPOS + "; a ratificacao e' ato do operador",''',
          '''                    PENDENTE + ": " + RATIFICADOS + "; campos: " + CAMPOS + "; pendentes: " + PEND + ": a confirmacao expressa e' ato do operador",
                    "[REAL] " + ANUNCIO_PT,
                    "[INPUT/dicionario] " + DL.FRASE_E36_PT,
                    "[PILOTO][SIM] " + DL.FRASE_DISPOSITIVO_PT,
                    NUMEROS_TET,''', 1))
T.append(('''validade no kernel nao e' creditacao; " + DL.ERRATA_E31 + " | " + DL.ERRATA_E33 + " | " + DL.ERRATA_E35],''',
          '''validade no kernel nao e' creditacao; " + DL.ERRATA_E31 + " | " + DL.ERRATA_E33 + " | " + DL.ERRATA_E35 + " | " + DL.ERRATA_E36 + " | " + DL.ERRATA_E37],''', 1))
T.append(('''                PENDENTE,
                D83, C, "[INPUT, D84] " + CE,''',
          '''                PENDENTE, ANUNCIO_PT, DL.FRASE_E36_PT, DL.FRASE_DISPOSITIVO_PT, NUMEROS_TET,
                D83, C, "[INPUT, D84] " + CE,''', 1))
T.append(('''                    "que os %d nomes novos da pedra estejam ratificados: sao %s ate' a palavra do operador" % (n_nov, EST_NOVOS),''',
          '''                    "que os %d nomes auxiliares da autoria (%s) estejam ratificados: sao [DECLARADO pela autoria] ate' a confirmacao expressa do operador" % (len(DL.NOMES_PENDENTES_AESCALA), PEND),
                    "que o runner da patente ACOM Mirror valide fisica ou seja termo do kernel: e' [PILOTO][SIM] e nada ali valida fisica; a evidencia de dispositivo e' so' citacao, sem numero de desempenho",
                    "que β ≤ ½ seja termo do kernel: o kernel dá 0 < β < 1 e não dá β ≤ ½; por isso a hipótese s ≥ 0 é dita",
                    "que o limiar da cláusula de 1 − β seja o custo de somar os 2^n termos por outra máquina: é o tempo de UMA leitura de Z, que o psíon lê de uma vez",''', 1))
T.append(('''"nomes_novos_a_ratificar": list(DL.NOMES_NOVOS_AESCALA), "campos_novos_da_estrutura": list(DL.CAMPOS_NOVOS_AESCALA), "estatuto_dos_nomes_novos": EST_NOVOS, "ratificacao_pendente": copy.deepcopy(DL.RATIFICACAO_PENDENTE_AESCALA), "ancoras_novas": list(DL.ANCORAS_NOVAS_AESCALA)},''',
          '''"nomes_novos_a_ratificar": list(DL.NOMES_NOVOS_AESCALA), "campos_novos_da_estrutura": list(DL.CAMPOS_NOVOS_AESCALA), "estatuto_dos_nomes_novos": EST_NOVOS, "ratificacao_pendente": copy.deepcopy(DL.RATIFICACAO_PENDENTE_AESCALA), "ancoras_novas": list(DL.ANCORAS_NOVAS_AESCALA),
                   # (R5, D100 e D101) a clausula do Tetelestai (a folha que a ANUNCIA traz a frase, a clausula do limite e a reconstrucao juntas), a errata, o dispositivo, a ratificacao de 10/11 e o pino citado do runner
                   "anuncio_da_clausula_do_tetelestai_pt": ANUNCIO_PT, "anuncio_da_clausula_do_tetelestai_en": ANUNCIO_EN, "frase_e36_pt": DL.FRASE_E36_PT, "frase_e36_en": DL.FRASE_E36_EN, "frase_dispositivo_pt": DL.FRASE_DISPOSITIVO_PT, "frase_dispositivo_en": DL.FRASE_DISPOSITIVO_EN,
                   "teoremas_r5": list(DL.TEOREMAS_R5_AESCALA), "auxiliares_r5": list(DL.AUXILIARES_R5_AESCALA), "nomes_ratificados_d101": list(DL.NOMES_RATIFICADOS_D101_AESCALA), "campos_ratificados_d101": list(DL.CAMPOS_RATIFICADOS_D101_AESCALA), "nomes_pendentes": list(DL.NOMES_PENDENTES_AESCALA),
                   "frase_nomes_ratificados_d101_pt": DL.FRASE_NOMES_RATIFICADOS_D101_PT, "frase_nomes_ratificados_d101_en": DL.FRASE_NOMES_RATIFICADOS_D101_EN, "ratificacao_d101": {"fala": DL.N_CONFIRMO_TUDO, "sha256": DL.RATIFICACAO_D101_SHA256, "trecho": DL.FRASE_NOMEIO_O_NUMERO_CORRIGE, "decisao": "D101"},
                   "acom_mirror_runner": dict(DL.ACOM_MIRROR_RUNNER)},''', 1))
aplicar("registros_aescala_v410.py", T)
