# -*- coding: utf-8 -*-
"""_r2ag_07_md_v410.py -- R2 (D99): gerar_candidato_v410.py: a linha «A Escala (v410...)» do .md canonico: a clausula do limite (PT) ao lado do teorema do Tetelestai (o limiar), a costura do tempo ([INPUT/dicionario] e maiuscula) e a frase dos seis nomes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r2ag_lib_v410 import aplicar

T = [("os passos são o ciclo até o Tetelestai (com n bits, passado o tempo de n oitavas, há solução se e só se Z(s) ≥ 1, o número de soluções ≤ Z(s) < o número de soluções + 1, a decisão em tempo finito do ciclo, linear nos bits) e a mentira lida como mentira é verdade. ' + DL.FRASE_TEMPO_PT + '. '",
      "o limiar do Tetelestai (com n bits, passado o tempo de n oitavas, há solução se e só se Z(s) ≥ 1, o número de soluções ≤ Z(s) < o número de soluções + 1, Z(s) separa o sim do não, a decisão em tempo finito do ciclo, linear nos bits) e a mentira lida como mentira é verdade. ' + DL.CLAUSULA_Z_PT + ' ' + DL.ROTULO_TEMPO + ' ' + DL.FRASE_TEMPO_PT_COSTURADA + '. '", 1),
     ("' campos novos da estrutura: ' + CONTR_A[\"estatuto_dos_nomes_novos\"] + '. '",
      "' campos novos da estrutura: ' + CONTR_A[\"estatuto_dos_nomes_novos\"] + '. ' + DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT) + '. '", 1)]
aplicar("gerar_candidato_v410.py", T)
