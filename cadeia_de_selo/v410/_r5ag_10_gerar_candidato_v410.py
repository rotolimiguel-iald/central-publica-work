# -*- coding: utf-8 -*-
"""_r5ag_10_gerar_candidato_v410.py -- R5 (D100 e D101): gerar_candidato_v410.py: a linha impressa do bloco A ESCALA no rito (os nomes novos RATIFICADOS em 10/11 e os auxiliares pendentes); o assert do contrato (o estatuto dos nomes novos e' RATIFICADOS, nao [DECLARADO]);
a linha «A Escala» do .md canonico (a frase da ratificacao D101 e, depois da clausula do limite, a clausula do Tetelestai em 1 - beta com a reconstrucao, a leitura do dicionario e a citacao do dispositivo); o manifesto do candidato (aescala): os campos da R5 e a nota."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar

T = []
T.append(('''nome e %s nomes ratificados; %s nomes novos a ratificar [DECLARADO]]" % (_a410v.get("n_nomes"), _a410v.get("n_nomes_novos")))''',
          '''nome e %s nomes ratificados; %s nomes novos RATIFICADOS em 10/11/2026 (D101) e %s auxiliares da autoria [DECLARADO pela autoria]; a clausula do Tetelestai em 1 - beta (R5, D100) com beta de runtime]" % (_a410v.get("n_nomes"), (_a410v.get("ratificacao_d101") or {}).get("n_nomes_ratificados"), len((_a410v.get("ratificacao_d101") or {}).get("pendentes") or [])))''', 1))
T.append(('''and "RATIFICADO" not in CONTR_A["estatuto_dos_nomes_novos"].upper()''',
          '''and "RATIFICADOS pelo operador em 10/11/2026" in CONTR_A["estatuto_dos_nomes_novos"] and "a ratificar" not in CONTR_A["estatuto_dos_nomes_novos"] and CONTR_A["nomes_pendentes"] == list(DL.NOMES_PENDENTES_AESCALA) and CONTR_A["nomes_ratificados_d101"] == list(DL.NOMES_RATIFICADOS_D101_AESCALA) and CONTR_A["ratificacao_d101"]["sha256"] == DL.RATIFICACAO_D101_SHA256 \\
    and CONTR_A["tetelestai"] == DL.TETELESTAI_AESCALA and CONTR_A["teoremas_r5"] == list(DL.TEOREMAS_R5_AESCALA) and CONTR_A["acom_mirror_runner"] == DL.ACOM_MIRROR_RUNNER''', 1))
T.append((''' âncoras no trio; ' + str(CONTR_A["n_nomes_novos"]) + ' nomes novos da pedra e ' + str(len(CONTR_A["campos_novos_da_estrutura"])) + ' campos novos da estrutura: ' + CONTR_A["estatuto_dos_nomes_novos"] + '. ' + DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT) + '. \'''',
          ''' âncoras no trio; ' + DL.FRASE_NOMES_RATIFICADOS_D101_PT + '. ' + DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT) + '. \'''', 1))
T.append(('''DL.CLAUSULA_Z_PT + ' ' + DL.ROTULO_TEMPO + ' ' + DL.FRASE_TEMPO_PT_COSTURADA + '. '
              'Leituras do operador, não termos:''',
          '''DL.CLAUSULA_Z_PT + ' ' + DL.ROTULO_TEMPO + ' ' + DL.FRASE_TEMPO_PT_COSTURADA + '. '
              'A cláusula do Tetelestai em 1 − β (R5, D100) [REAL]: ' + DL.FRASE_TETELESTAI_PT + '. ' + DL.FRASE_RECONSTROI_PT + '. [INPUT/dicionário] ' + DL.FRASE_E36_PT + '. [PILOTO][SIM] ' + DL.FRASE_DISPOSITIVO_PT + '. '
              'Leituras do operador, não termos:''', 1))
T.append(('''"ratificacao_D87": CONTR_A["ratificacao"], "numeros": CONTR_A["numeros"],''',
          '''"ratificacao_D87": CONTR_A["ratificacao"], "ratificacao_D101": CONTR_A["ratificacao_d101"], "teoremas_r5": CONTR_A["teoremas_r5"], "auxiliares_r5": CONTR_A["auxiliares_r5"], "nomes_ratificados_d101": CONTR_A["nomes_ratificados_d101"], "campos_ratificados_d101": CONTR_A["campos_ratificados_d101"], "nomes_pendentes": CONTR_A["nomes_pendentes"],
                   "tetelestai": CONTR_A["tetelestai"], "acom_mirror_runner": CONTR_A["acom_mirror_runner"], "numeros": CONTR_A["numeros"],''', 1))
T.append((''' nomes ratificados pelo operador em 09/11/2026; " + str(CONTR_A["n_nomes_novos"]) + " nomes novos [DECLARADO], a ratificar"},''',
          ''' nomes ratificados pelo operador em 09/11/2026; " + str(len(CONTR_A["nomes_ratificados_d101"])) + " nomes novos RATIFICADOS em 10/11/2026 (D101); " + str(len(CONTR_A["nomes_pendentes"])) + " auxiliares da autoria [DECLARADO pela autoria]"},''', 1))
aplicar("gerar_candidato_v410.py", T)
