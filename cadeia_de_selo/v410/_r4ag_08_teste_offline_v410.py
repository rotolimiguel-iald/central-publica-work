# -*- coding: utf-8 -*-
"""_r4ag_08_teste_offline_v410.py -- controles negativos novos do teste offline do a_escala_v410 (R4): o ciclo (uma instancia sem solucao com solucao; o epsilon fora do intervalo), a forma do tempo retirada do texto, um teorema da R4 fora das ancoras."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from _r4ag_lib_v410 import aplicar

T = []
T.append(('for k, (vd, fl) in R.items():\n    print("controle negativo (%s): %s | falhos %s" % (k, vd[:60], fl))\n',
          'C15 = copy.deepcopy(CONTR); C15["ciclo"]["custo_sem_solucao"][0] = 0; RTA._V410_AESCALA_CONTRACT = C15; r_ = RTA.a_escala_v410(core_de_ensaio()); R["ciclo_instancia_sem_solucao_com_solucao"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR   # (R4, D94)\n'
          'C16 = copy.deepcopy(CONTR); C16["ciclo"]["epsilon"] = "5"; RTA._V410_AESCALA_CONTRACT = C16; r_ = RTA.a_escala_v410(core_de_ensaio()); R["ciclo_epsilon_fora_do_intervalo"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR\n'
          'T17 = json.loads(json.dumps(TXT, ensure_ascii=False).replace(DL.FRASE_TEMPO_PT, "(retirada)")); RTA._V410_AESCALA_TEXT = T17; r_ = RTA.a_escala_v410(core_de_ensaio()); R["forma_do_tempo_retirada_do_texto"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT\n'
          'C18 = copy.deepcopy(CONTR); C18["teoremas_r4"] = list(C18["teoremas_r4"]) + ["teorema_que_nao_existe_na_pedra"]; RTA._V410_AESCALA_CONTRACT = C18; r_ = RTA.a_escala_v410(core_de_ensaio()); R["teorema_da_r4_fora_das_ancoras"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR\n'
          'for k, (vd, fl) in R.items():\n    print("controle negativo (%s): %s | falhos %s" % (k, vd[:60], fl))\n', 1))
T.append(('"ponte_caso_trocado": ["c6"], "ponte_fundo_em_n_oitavas_trocado": ["c6"]}',
          '"ponte_caso_trocado": ["c6"], "ponte_fundo_em_n_oitavas_trocado": ["c6"], "ciclo_instancia_sem_solucao_com_solucao": ["c6"], "ciclo_epsilon_fora_do_intervalo": ["c6"], "forma_do_tempo_retirada_do_texto": ["c8"], "teorema_da_r4_fora_das_ancoras": ["c2"]}', 1))
T.append(('and all(R[k_][1] == ["c6"] for k_ in ("ponte_caso_trocado", "ponte_fundo_em_n_oitavas_trocado"))',
          'and all(R[k_][1] == ["c6"] for k_ in ("ponte_caso_trocado", "ponte_fundo_em_n_oitavas_trocado", "ciclo_instancia_sem_solucao_com_solucao", "ciclo_epsilon_fora_do_intervalo")) and R["forma_do_tempo_retirada_do_texto"][1] == ["c8"] and R["teorema_da_r4_fora_das_ancoras"][1] == ["c2"]', 1))
aplicar("_teste_aescala_offline_v410.py", T)
