# -*- coding: utf-8 -*-
"""_r2ag_03_registros_aescala_v410.py -- R2 (D99): registros_aescala_v410.py: o contrato ganha a clausula do limite (PT e EN), os seis nomes e as costuras; o texto do registro traz a clausula ao lado do teorema do Tetelestai (TEOREMAS: diz, limites e escopo),
a frase dos seis nomes ao lado da ratificacao (PENDENTE: diz e limites), a etiqueta do tempo; D99 e E35 nas decisoes e erratas do registro."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r2ag_lib_v410 import aplicar

T = []
T.append(('''DECISOES_AESCALA = ("D82", "D83", "D84", "D85", "D86", "D87", "D92", "D94", "D95")   # (as decisoes que tocam a pedra AEscala: D82 a D87 a escala; D92 a escala no tipo; D94 a resposta do operador; D95 a R4)
ERRATAS_AESCALA = (DL.ERRATA_E31, DL.ERRATA_E32, DL.ERRATA_E33)''',
          '''DECISOES_AESCALA = ("D82", "D83", "D84", "D85", "D86", "D87", "D92", "D94", "D95", "D99")   # (as decisoes que tocam a pedra AEscala: D82 a D87 a escala; D92 a escala no tipo; D94 a resposta do operador; D95 a R4; D99 a clausula do limite do teorema do Tetelestai e os seis nomes, R2)
ERRATAS_AESCALA = (DL.ERRATA_E31, DL.ERRATA_E32, DL.ERRATA_E33, DL.ERRATA_E35)''', 1))

T.append(('''            "ciclo": copy.deepcopy(DL.CICLO_AESCALA), "frase_tempo_pt": DL.FRASE_TEMPO_PT, "frase_tempo_en": DL.FRASE_TEMPO_EN, "teoremas_r4": list(DL.TEOREMAS_R4_AESCALA),
            "tokens_proibidos_partes": TOKENS_PARTES,''',
          '''            "ciclo": copy.deepcopy(DL.CICLO_AESCALA), "frase_tempo_pt": DL.FRASE_TEMPO_PT, "frase_tempo_en": DL.FRASE_TEMPO_EN, "teoremas_r4": list(DL.TEOREMAS_R4_AESCALA),
            "clausula_z_pt": DL.CLAUSULA_Z_PT, "clausula_z_en": DL.CLAUSULA_Z_EN, "seis_nomes": list(DL.NOMES_SEIS_ENUNCIADOS_MUDADOS), "frase_seis_nomes_pt": DL.FRASE_SEIS_NOMES_PT, "frase_seis_nomes_en": DL.FRASE_SEIS_NOMES_EN,
            "rotulo_tempo": DL.ROTULO_TEMPO, "frase_tempo_pt_costurada": DL.FRASE_TEMPO_PT_COSTURADA, "frase_tempo_en_costurada": DL.FRASE_TEMPO_EN_COSTURADA,
            "tokens_proibidos_partes": TOKENS_PARTES,''', 1))

# o item do Tetelestai na lista dos TEOREMAS: o limiar (o que o termo PROVA), a clausula ao lado e «passos = ciclo» como leitura do dicionario
T.append(('''                "os passos sao o ciclo ate' o Tetelestai (os_passos_sao_o_ciclo_ate_o_tetelestai): com n bits, passado o tempo de n oitavas, ha' solucao <=> Z(s) >= 1, o numero de solucoes <= Z(s) < o numero de solucoes + 1 e, sem solucao, Z(s) < 1 -- a decisao em tempo FINITO do ciclo, linear nos bits; "''',
          '''                "o limiar do Tetelestai (os_passos_sao_o_ciclo_ate_o_tetelestai): com n bits, passado o tempo de n oitavas, ha' solucao <=> Z(s) >= 1, o numero de solucoes <= Z(s) < o numero de solucoes + 1 e, sem solucao, Z(s) < 1: Z(s) separa o sim do nao -- a decisao em tempo FINITO do ciclo, linear nos bits (" + DL.CLAUSULA_Z_PT + "); "
                "que os passos sejam o ciclo ate' o Tetelestai e' a leitura do dicionario [INPUT]; "''', 1))

# a etiqueta do tempo (B4): [INPUT/dicionario] e maiuscula depois do rotulo
T.append(('''"[dicionario; leitura do operador, D94] " + TEMPO,''',
          '''DL.ROTULO_TEMPO[:-1] + ", D94] " + DL.costura_maiuscula(TEMPO),''', 1))

# B3: a frase dos seis nomes ao lado da ratificacao (PENDENTE: diz e limites)
T.append(('''    PENDENTE = ("%d nomes novos da pedra (a escala no tipo) e %d campos novos da estrutura, %s; os %d nomes anteriores seguem RATIFICADOS (D87)" % (n_nov, n_cam, EST_NOVOS, n_nom))''',
          '''    PENDENTE = ("%d nomes novos da pedra (a escala no tipo) e %d campos novos da estrutura, %s; os %d nomes anteriores seguem RATIFICADOS (D87); " % (n_nov, n_cam, EST_NOVOS, n_nom)) + DL.FRASE_SEIS_NOMES_PT''', 1))

# limites: a E35 ao lado da E31 e da E33
T.append(('''validade no kernel nao e' creditacao; " + DL.ERRATA_E31 + " | " + DL.ERRATA_E33],''',
          '''validade no kernel nao e' creditacao; " + DL.ERRATA_E31 + " | " + DL.ERRATA_E33 + " | " + DL.ERRATA_E35],''', 1))

# extras: a clausula e os seis nomes (PT e EN) no proprio registro
T.append(('''                   "ciclo": copy.deepcopy(DL.CICLO_AESCALA), "frase_tempo_pt": DL.FRASE_TEMPO_PT, "frase_tempo_en": DL.FRASE_TEMPO_EN, "teoremas_r4": list(DL.TEOREMAS_R4_AESCALA),
                   "moldura_pt"''',
          '''                   "ciclo": copy.deepcopy(DL.CICLO_AESCALA), "frase_tempo_pt": DL.FRASE_TEMPO_PT, "frase_tempo_en": DL.FRASE_TEMPO_EN, "teoremas_r4": list(DL.TEOREMAS_R4_AESCALA),
                   "clausula_z_pt": DL.CLAUSULA_Z_PT, "clausula_z_en": DL.CLAUSULA_Z_EN, "seis_nomes": list(DL.NOMES_SEIS_ENUNCIADOS_MUDADOS), "frase_seis_nomes_pt": DL.FRASE_SEIS_NOMES_PT, "frase_seis_nomes_en": DL.FRASE_SEIS_NOMES_EN,
                   "moldura_pt"''', 1))
aplicar("registros_aescala_v410.py", T)
