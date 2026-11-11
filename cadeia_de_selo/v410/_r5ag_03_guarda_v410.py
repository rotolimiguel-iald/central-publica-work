# -*- coding: utf-8 -*-
"""_r5ag_03_guarda_v410.py -- R5 (D100 e D101): guarda_frases_v410.py so' ACRESCENTA frases limpas e controles (nenhuma regra muda): as decisoes D100 e D101, as erratas E36 e E37, as frases da clausula do Tetelestai, da reconstrucao, da errata, do dispositivo e da ratificacao D101 (PT e EN), as duas leituras novas e as duas falas
entre aspas passam; as regras F44, F54, F58 e F59 nao pegam a clausula."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar

T = []
T.append(('''          "the steps are the cycle up to the Tetelestai: the decision in finite time of the cycle, linear in the bits (" + DL.CLAUSULA_Z_EN + ") and a lie read as a lie is truth"]''',
          '''          "the steps are the cycle up to the Tetelestai: the decision in finite time of the cycle, linear in the bits (" + DL.CLAUSULA_Z_EN + ") and a lie read as a lie is truth",
          # (R5, D100 e D101: isto e' TESTE, nao a guarda) a clausula do Tetelestai em 1 - beta com a clausula do limite, a reconstrucao, a errata, o dispositivo (so' citacao) e a ratificacao de 10/11, PT e EN; as erratas E36 e E37; as leituras novas
          DL.ERRATA_E36, DL.ERRATA_E37, DL.FRASE_TETELESTAI_PT, DL.FRASE_TETELESTAI_EN, DL.FRASE_RECONSTROI_PT, DL.FRASE_RECONSTROI_EN, DL.FRASE_E36_PT, DL.FRASE_E36_EN, DL.FRASE_DISPOSITIVO_PT, DL.FRASE_DISPOSITIVO_EN, DL.FRASE_NOMES_RATIFICADOS_D101_PT, DL.FRASE_NOMES_RATIFICADOS_D101_EN,
          DL.FRASE_TETELESTAI_PT + " " + DL.CLAUSULA_Z_PT + " " + DL.FRASE_RECONSTROI_PT, DL.FRASE_TETELESTAI_EN + " " + DL.CLAUSULA_Z_EN + " " + DL.FRASE_RECONSTROI_EN, DL.LEITURA_V410["a_clausula_do_tetelestai"], DL.LEITURA_V410["a_regra_do_nome"]]''', 1))
T.append(('''                            "f59_a_regra_nao_pegou_a_pedra_da_r4":''',
          '''                            # (R5, D100 e D101) as decisoes, as erratas e as frases novas passam; F44, F54, F58 e F59 nao pegam a clausula; as falas 27 e 28 entre aspas passam
                            "r5_d100_d101_e36_e37_passam": not G(DL.DECISOES["D100"]) and not G(DL.DECISOES["D101"]) and not G(DL.ERRATA_E36) and not G(DL.ERRATA_E37),
                            "r5_as_frases_da_clausula_passam": not any(G(x_) for x_ in (DL.FRASE_TETELESTAI_PT, DL.FRASE_TETELESTAI_EN, DL.FRASE_RECONSTROI_PT, DL.FRASE_RECONSTROI_EN, DL.FRASE_E36_PT, DL.FRASE_E36_EN, DL.FRASE_DISPOSITIVO_PT, DL.FRASE_DISPOSITIVO_EN, DL.FRASE_NOMES_RATIFICADOS_D101_PT, DL.FRASE_NOMES_RATIFICADOS_D101_EN)),
                            "r5_f44_f54_f58_f59_nao_pegam_a_clausula": not any(v_[0].startswith(("F44", "F54", "F58", "F59")) for t_ in (DL.FRASE_TETELESTAI_PT, DL.FRASE_TETELESTAI_EN, DL.FRASE_E36_PT, DL.FRASE_E36_EN, DL.DECISOES["D100"], DL.DECISOES["D101"], DL.ERRATA_E36, DL.ERRATA_E37, DL.FRASE_DISPOSITIVO_PT, DL.FRASE_DISPOSITIVO_EN) for v_ in G(t_)),
                            "r5_as_falas_27_e_28_entre_aspas_passam": not G(sem_falas("«" + DL.FRASE_CLAUSULA_NO_ACOM + "»; «" + DL.FRASE_UM_MENOS_BETATGL + "»; «" + DL.FRASE_BETATGL_OPERADOR_MODULAR + "»; «" + DL.FRASE_CONFIRMO_TUDO + "»; «" + DL.FRASE_NOMEIO_O_NUMERO_CORRIGE + "»", falas_)[0]),
                            "r5_a_forma_antiga_da_ratificacao_nao_e_a_vigente": "a ratificar" not in DL.ESTATUTO_NOMES_NOVOS_AESCALA and "DECLARADO" not in DL.ESTATUTO_NOMES_NOVOS_AESCALA and "RATIFICADOS pelo operador em 10/11/2026" in DL.ESTATUTO_NOMES_NOVOS_AESCALA,
                            "f59_a_regra_nao_pegou_a_pedra_da_r4":''', 1))
aplicar("guarda_frases_v410.py", T)
