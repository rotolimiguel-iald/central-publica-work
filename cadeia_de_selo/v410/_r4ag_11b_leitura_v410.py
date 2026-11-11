# -*- coding: utf-8 -*-
"""_r4ag_11b_leitura_v410.py -- a LEITURA (o portao) ganha o que confere da R4 e aceita as falas de 10/11; so' se acrescenta; nada e' afrouxado. (A parte 11 aplicou textos, custodia e mapa; esta aplica so' a leitura.)"""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from _r4ag_lib_v410 import aplicar

P = "pos_rito/"
# ---------------------------------------------------------------------------------------------------------------- leitura_v410.py (o portao: so' se acrescenta; nada se afrouxa)
L = []
L.append(("re.match(r'OPERADOR_0[6789]nov_', str((ec_[k_] or {}).get('nome', '')))", "re.match(r'OPERADOR_(?:0[6789]|10)nov_', str((ec_[k_] or {}).get('nome', '')))", 1))
L.append(("as inscricoes de 06 a 09/11 tem de ser TODAS falas do operador (OPERADOR_0[6789]nov_*)", "as inscricoes de 06 a 10/11 tem de ser TODAS falas do operador (OPERADOR_0[6789]nov_* e OPERADOR_10nov_*)", 1))
L.append(("as falas de 09/11 por sha256, os numeros [1/2 + 1/2 = 1;", "as falas de 09 e 10/11 por sha256, o ciclo (os passos sao o ciclo ate o Tetelestai), as ancoras novas e os teoremas da R4, a forma do tempo no texto, os numeros [1/2 + 1/2 = 1;", 1))
L.append(("                         and ea_v_.get('numeros') == dict(DL_.NUMEROS_AESCALA) and ea_v_.get('canonica_pt_no_texto') is True",
          "                         and (ea_v_.get('ciclo') or {}).get('ok') is True and (ea_v_.get('ciclo') or {}).get('n_bits') == DL_.CICLO_N_BITS and (ea_v_.get('ciclo') or {}).get('n_solucoes_sem') == 0 < (ea_v_.get('ciclo') or {}).get('n_solucoes_com') and (ea_v_.get('ciclo') or {}).get('Z_sem_solucao') < 1 <= (ea_v_.get('ciclo') or {}).get('Z_com_solucao')\n"
          "                         and set(ea_v_.get('ancoras_novas') or {}) == set(DL_.ANCORAS_NOVAS_AESCALA) and ea_v_.get('n_ancoras_novas_ok') == len(DL_.ANCORAS_NOVAS_AESCALA) and set(ea_v_.get('teoremas_r4') or {}) == set(DL_.TEOREMAS_R4_AESCALA) and all((ea_v_.get('teoremas_r4') or {}).values()) and ea_v_.get('tempo_pt_no_texto') is True and ea_v_.get('tempo_en_no_texto') is True\n"
          "                         and ea_v_.get('numeros') == dict(DL_.NUMEROS_AESCALA) and ea_v_.get('canonica_pt_no_texto') is True", 1))
L.append(("and ea_.get('ponte') == DL_.PONTE_AESCALA == CEA_.get('ponte') and (ea_v_.get('ponte') or {}).get('ok') is True)",
          "and ea_.get('ponte') == DL_.PONTE_AESCALA == CEA_.get('ponte') and (ea_v_.get('ponte') or {}).get('ok') is True\n"
          "                        and ea_.get('ciclo') == DL_.CICLO_AESCALA == CEA_.get('ciclo') and ea_.get('frase_tempo_pt') == DL_.FRASE_TEMPO_PT == CEA_.get('frase_tempo_pt') and ea_.get('frase_tempo_en') == DL_.FRASE_TEMPO_EN and list(ea_.get('teoremas_r4') or []) == list(DL_.TEOREMAS_R4_AESCALA) == list(CEA_.get('teoremas_r4') or []))",
          1))
aplicar(P + "leitura_v410.py", L)
