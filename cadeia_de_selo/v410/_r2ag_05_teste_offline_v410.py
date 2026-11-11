# -*- coding: utf-8 -*-
"""_r2ag_05_teste_offline_v410.py -- R2 (D99): _teste_aescala_offline_v410.py ganha os controles negativos da clausula do limite (PT em todo lugar, PT so' no campo diz[4], EN), da ancora nova tirada do contrato (B1) e dos seis nomes (B3)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r2ag_lib_v410 import aplicar

T = []
T.append(('''for k, (vd, fl) in R.items():
    print("controle negativo (%s): %s | falhos %s" % (k, vd[:60], fl))''',
          '''# (R2, D99; ADENDO 4) a clausula do limite do teorema do Tetelestai: retirada de todo o texto; retirada so' de UM campo que anuncia o teorema (diz); a EN retirada; (B1) uma ancora nova tirada do contrato; (B3) a frase dos seis nomes retirada do texto
T19 = json.loads(json.dumps(TXT, ensure_ascii=False).replace(DL.CLAUSULA_Z_PT, "(retirada)")); RTA._V410_AESCALA_TEXT = T19; r_ = RTA.a_escala_v410(core_de_ensaio()); R["clausula_do_limite_retirada_do_texto"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
T20 = copy.deepcopy(TXT); T20["diz"] = [x_.replace(DL.CLAUSULA_Z_PT, "(retirada)") for x_ in T20["diz"]]; assert T20["diz"] != TXT["diz"] and any(DL.CLAUSULA_Z_PT in x_ for x_ in T20["escopo"].split("\\n") + T20["limites"]), "o controle de um campo so' faz sentido se a clausula esta em mais de um campo"
RTA._V410_AESCALA_TEXT = T20; r_ = RTA.a_escala_v410(core_de_ensaio()); R["clausula_do_limite_retirada_de_um_campo"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
T21 = json.loads(json.dumps(TXT, ensure_ascii=False).replace(DL.CLAUSULA_Z_EN, "(removed)")); RTA._V410_AESCALA_TEXT = T21; r_ = RTA.a_escala_v410(core_de_ensaio()); R["clausula_do_limite_em_ingles_retirada"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
C22 = copy.deepcopy(CONTR); C22["ancoras_novas"] = list(C22["ancoras_novas"])[1:]; RTA._V410_AESCALA_CONTRACT = C22; r_ = RTA.a_escala_v410(core_de_ensaio()); R["ancora_nova_tirada_do_contrato"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
T23 = json.loads(json.dumps(TXT, ensure_ascii=False).replace(DL.FRASE_SEIS_NOMES_PT, "(retirada)")); RTA._V410_AESCALA_TEXT = T23; r_ = RTA.a_escala_v410(core_de_ensaio()); R["seis_nomes_retirados_do_texto"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
for k, (vd, fl) in R.items():
    print("controle negativo (%s): %s | falhos %s" % (k, vd[:60], fl))''', 1))

T.append(('''"forma_do_tempo_retirada_do_texto": ["c8"], "teorema_da_r4_fora_das_ancoras": ["c2"]}''',
          '''"forma_do_tempo_retirada_do_texto": ["c8"], "teorema_da_r4_fora_das_ancoras": ["c2"], "clausula_do_limite_retirada_do_texto": ["c8"], "clausula_do_limite_retirada_de_um_campo": ["c8"], "clausula_do_limite_em_ingles_retirada": ["c8"], "ancora_nova_tirada_do_contrato": ["c2"], "seis_nomes_retirados_do_texto": ["c11"]}''', 1))
T.append(('''and R["forma_do_tempo_retirada_do_texto"][1] == ["c8"] and R["teorema_da_r4_fora_das_ancoras"][1] == ["c2"]''',
          '''and R["forma_do_tempo_retirada_do_texto"][1] == ["c8"] and R["teorema_da_r4_fora_das_ancoras"][1] == ["c2"] and all(R[k_][1] == ["c8"] for k_ in ("clausula_do_limite_retirada_do_texto", "clausula_do_limite_retirada_de_um_campo", "clausula_do_limite_em_ingles_retirada")) and R["ancora_nova_tirada_do_contrato"][1] == ["c2"] and R["seis_nomes_retirados_do_texto"][1] == ["c11"]''', 1))
T.append(('''a ponte da escala trocada (dois pontos).''',
          '''a ponte da escala trocada (dois pontos); (R2, D99) a clausula do limite do teorema do Tetelestai retirada (de todo o texto, de um so' campo, a EN); (B1) uma ancora nova tirada do contrato; (B3) a frase dos seis nomes retirada.''', 1))
aplicar("_teste_aescala_offline_v410.py", T)
