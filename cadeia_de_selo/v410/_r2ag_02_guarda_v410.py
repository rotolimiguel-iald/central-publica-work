# -*- coding: utf-8 -*-
"""_r2ag_02_guarda_v410.py -- R2 (D99): guarda_frases_v410.py (a LISTA de limpas e o controle negativo; a REGRA da guarda, runtime_v410.py, NAO muda): as clausulas do ADENDO 4 (PT e EN, sozinhas e dentro do texto), os seis nomes, a costura do tempo e a E35 passam;
a D99 entra pela lista das decisoes (_L410)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r2ag_lib_v410 import aplicar

A1 = '''          DL.ERRATA_E32, DL.ERRATA_E33, DL.ERRATA_E34, DL.FRASE_H0DN_OBRIGATORIA_PT + "; " + DL.FRASE_H0DN_PODER_PT, DL.FRASE_H0DN_OBRIGATORIA_EN + "; " + DL.FRASE_H0DN_PODER_EN]   # (D94 e D96: a forma obrigatoria do tempo, o leitor e' a escala, as negacoes, as erratas E32 a E34 e a frase do poder certificado passam)'''
N1 = '''          DL.ERRATA_E32, DL.ERRATA_E33, DL.ERRATA_E34, DL.FRASE_H0DN_OBRIGATORIA_PT + "; " + DL.FRASE_H0DN_PODER_PT, DL.FRASE_H0DN_OBRIGATORIA_EN + "; " + DL.FRASE_H0DN_PODER_EN,   # (D94 e D96: a forma obrigatoria do tempo, o leitor e' a escala, as negacoes, as erratas E32 a E34 e a frase do poder certificado passam)
          # (R2, D99, ADENDO 4: isto e' TESTE, nao a guarda) a clausula do limite do teorema do Tetelestai, PT e EN, sozinha e dentro do texto que anuncia o teorema; os seis nomes de enunciado mudado; a costura do tempo (rotulo + maiuscula); a E35
          DL.CLAUSULA_Z_PT, DL.CLAUSULA_Z_EN, DL.FRASE_SEIS_NOMES_PT, DL.FRASE_SEIS_NOMES_EN, DL.ERRATA_E35, DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA, DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_EN_COSTURADA,
          "os passos são o ciclo até o Tetelestai: a decisão em tempo finito do ciclo, linear nos bits (" + DL.CLAUSULA_Z_PT + ") e a mentira lida como mentira é verdade",
          "the steps are the cycle up to the Tetelestai: the decision in finite time of the cycle, linear in the bits (" + DL.CLAUSULA_Z_EN + ") and a lie read as a lie is truth"]'''

A2 = '''                            "f59_d94_d96_e33_e34_passam": not G(DL.DECISOES["D94"]) and not G(DL.DECISOES["D96"]) and not G(DL.ERRATA_E33) and not G(DL.ERRATA_E34),'''
N2 = A2 + '''
                            "r2_d99_e35_e_as_clausulas_do_adendo_4_passam": not G(DL.DECISOES["D99"]) and not G(DL.ERRATA_E35) and not G(DL.CLAUSULA_Z_PT) and not G(DL.CLAUSULA_Z_EN) and not G(DL.FRASE_SEIS_NOMES_PT) and not G(DL.FRASE_SEIS_NOMES_EN)
                                                                            and not G("a decisão em tempo finito do ciclo, linear nos bits (" + DL.CLAUSULA_Z_PT + ")") and not G("the decision in finite time of the cycle, linear in the bits (" + DL.CLAUSULA_Z_EN + ")"),
                            "r2_a_costura_do_tempo_passa": not G(DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA) and not G(DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_EN_COSTURADA),
                            "r2_f59_e_f54_nao_pegam_as_clausulas_novas": not any(v_[0].startswith(("F59", "F54")) for t_ in (DL.CLAUSULA_Z_PT, DL.CLAUSULA_Z_EN, DL.DECISOES["D99"], DL.ERRATA_E35, DL.FRASE_SEIS_NOMES_PT, DL.FRASE_SEIS_NOMES_EN, "o texto diz que " + DL.CLAUSULA_Z_PT + " aqui") for v_ in G(t_)),'''
aplicar("guarda_frases_v410.py", [(A1, N1, 1), (A2, N2, 1)])
