# -*- coding: utf-8 -*-
"""_r5ag_08_teste_offline_v410.py -- R5 (D100 e D101): _teste_aescala_offline_v410.py ganha os controles negativos da clausula do Tetelestai (a clausula do limite retirada de uma folha que anuncia os teoremas novos; a hipotese s >= 0 retirada da frase, no contrato e numa folha; a citacao do dispositivo sem [PILOTO][SIM];
a citacao com numero de desempenho; o controle negativo da c13 invertido (s* no lugar de uma oitava a menos); o adversario com duas solucoes; o contraexemplo com b <= 1/2) e da ratificacao D101 (um pendente entre os ratificados; ratificacao_pendente esvaziada; o sha256 da fala 28 trocado; a fala 28 adulterada;
o estatuto antigo restaurado; o estatuto antigo plantado no texto; a frase da ratificacao retirada; um ratificado retirado)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar

T = []
NEW = '''# (R5, D100 e D101) a clausula do Tetelestai em 1 - beta e a ratificacao de 10/11: cada controle tem de reprovar so' a checagem esperada
_ant_pt = "anuncio_da_clausula_do_tetelestai_pt"
T24 = copy.deepcopy(TXT); _lf = T24["extras"][_ant_pt]; assert DL.CLAUSULA_Z_PT in _lf and DL.FRASE_TETELESTAI_PT in _lf; T24["extras"][_ant_pt] = _lf.replace(DL.CLAUSULA_Z_PT, "(retirada)")
RTA._V410_AESCALA_TEXT = T24; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_clausula_do_limite_retirada_de_uma_folha_que_anuncia_os_teoremas_novos"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
T25 = copy.deepcopy(TXT); T25["extras"][_ant_pt] = T25["extras"][_ant_pt].replace(DL.FRASE_TETELESTAI_PT, DL.FRASE_TETELESTAI_PT.replace("s ≥ 0", "s")); assert T25["extras"][_ant_pt] != TXT["extras"][_ant_pt]
RTA._V410_AESCALA_TEXT = T25; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_hipotese_s_nao_negativo_retirada_de_uma_folha"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
C26 = copy.deepcopy(CONTR); C26["frase_tetelestai_pt"] = DL.FRASE_TETELESTAI_PT.replace("s ≥ 0", "s"); assert C26["frase_tetelestai_pt"] != CONTR["frase_tetelestai_pt"]
RTA._V410_AESCALA_CONTRACT = C26; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_hipotese_s_nao_negativo_retirada_da_frase_do_contrato"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
T27 = json.loads(json.dumps(TXT, ensure_ascii=False).replace("[PILOTO][SIM]", "(retirado)")); RTA._V410_AESCALA_TEXT = T27; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_citacao_do_dispositivo_sem_piloto_sim"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
T28 = copy.deepcopy(TXT); T28["nao_diz"] = list(T28["nao_diz"]) + ["o ACOM Mirror, que é [PILOTO][SIM] e do qual nada ali valida física, rodou 22 de 22 testes"]
RTA._V410_AESCALA_TEXT = T28; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_citacao_do_dispositivo_com_numero_de_desempenho"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
C29 = copy.deepcopy(CONTR); C29["tetelestai"]["oitavas_a_menos_no_controle"] = 0; RTA._V410_AESCALA_CONTRACT = C29; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_controle_negativo_invertido_s_estrela_no_lugar_de_uma_oitava_a_menos"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C30 = copy.deepcopy(CONTR); C30["tetelestai"]["custo_adversario"] = [0, 0] + [1] * (2 ** C30["tetelestai"]["n_bits"] - 2); RTA._V410_AESCALA_CONTRACT = C30; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_adversario_com_duas_solucoes"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C31 = copy.deepcopy(CONTR); C31["tetelestai"]["contraexemplo_s_negativo"]["b"] = "1/10"; RTA._V410_AESCALA_CONTRACT = C31; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_contraexemplo_com_b_no_meio_ou_abaixo"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C32 = copy.deepcopy(CONTR); C32["nomes_ratificados_d101"] = list(C32["nomes_ratificados_d101"]) + [C32["nomes_pendentes"][0]]; RTA._V410_AESCALA_CONTRACT = C32; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_um_pendente_entre_os_ratificados"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C33 = copy.deepcopy(CONTR); C33["ratificacao_pendente"] = {}; RTA._V410_AESCALA_CONTRACT = C33; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_ratificacao_pendente_esvaziada"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C34 = copy.deepcopy(CONTR); C34["ratificacao_d101"]["sha256"] = "0" * 64; RTA._V410_AESCALA_CONTRACT = C34; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_sha256_da_fala_28_trocado_no_pino"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
V35 = copy.deepcopy(VERB); V35[CONTR["chave_ratificacao_d101"]]["text"] = V35[CONTR["chave_ratificacao_d101"]]["text"] + "x"; RTA._V410_VERBATINS2 = V35; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_fala_28_adulterada"] = (r_["verdict"], _f(r_)); RTA._V410_VERBATINS2 = VERB
C36 = copy.deepcopy(CONTR); C36["estatuto_dos_nomes_novos"] = "[DECLARADO pela gerencia e pela autoria; a ratificar pelo operador]"; RTA._V410_AESCALA_CONTRACT = C36; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_estatuto_antigo_restaurado"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
T37 = copy.deepcopy(TXT); T37["diz"] = list(T37["diz"]) + ["os nomes novos seguem [DECLARADO, a ratificar]"]; RTA._V410_AESCALA_TEXT = T37; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_estatuto_antigo_plantado_no_texto"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
T38 = json.loads(json.dumps(TXT, ensure_ascii=False).replace(DL.FRASE_NOMES_RATIFICADOS_D101_PT, "(retirada)")); RTA._V410_AESCALA_TEXT = T38; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_frase_da_ratificacao_d101_retirada_do_texto"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
C39 = copy.deepcopy(CONTR); C39["nomes_ratificados_d101"] = list(C39["nomes_ratificados_d101"])[1:]; RTA._V410_AESCALA_CONTRACT = C39; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_um_ratificado_retirado"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
for k, (vd, fl) in R.items():
    print("controle negativo (%s): %s | falhos %s" % (k, vd[:60], fl))'''
T.append(('''for k, (vd, fl) in R.items():
    print("controle negativo (%s): %s | falhos %s" % (k, vd[:60], fl))''', NEW, 1))
T.append(('''"ancora_nova_tirada_do_contrato": ["c2"], "seis_nomes_retirados_do_texto": ["c11"]}''',
          '''"ancora_nova_tirada_do_contrato": ["c2"], "seis_nomes_retirados_do_texto": ["c11"],
       "r5_clausula_do_limite_retirada_de_uma_folha_que_anuncia_os_teoremas_novos": ["c8"], "r5_hipotese_s_nao_negativo_retirada_de_uma_folha": ["c8"], "r5_hipotese_s_nao_negativo_retirada_da_frase_do_contrato": ["c8"], "r5_citacao_do_dispositivo_sem_piloto_sim": ["c8"], "r5_citacao_do_dispositivo_com_numero_de_desempenho": ["c8"],
       "r5_controle_negativo_invertido_s_estrela_no_lugar_de_uma_oitava_a_menos": ["c13"], "r5_adversario_com_duas_solucoes": ["c13"], "r5_contraexemplo_com_b_no_meio_ou_abaixo": ["c13"], "r5_um_pendente_entre_os_ratificados": ["c11"], "r5_ratificacao_pendente_esvaziada": ["c11"], "r5_sha256_da_fala_28_trocado_no_pino": ["c11"],
       "r5_fala_28_adulterada": ["c5", "c11"], "r5_estatuto_antigo_restaurado": ["c11"], "r5_estatuto_antigo_plantado_no_texto": ["c11"], "r5_frase_da_ratificacao_d101_retirada_do_texto": ["c11"], "r5_um_ratificado_retirado": ["c11"]}''', 1))
T.append(('''and R["ancora_nova_tirada_do_contrato"][1] == ["c2"] and R["seis_nomes_retirados_do_texto"][1] == ["c11"]''',
          '''and R["ancora_nova_tirada_do_contrato"][1] == ["c2"] and R["seis_nomes_retirados_do_texto"][1] == ["c11"] and all(R[k_][1] == esp[k_] for k_ in esp if k_.startswith("r5_"))   # (R5: cada controle novo reprova EXATAMENTE a checagem esperada)''', 1))
T.append(('''a ponte da escala trocada (dois pontos);''', '''a ponte da escala trocada (dois pontos); (R5, D100 e D101) a clausula do Tetelestai em 1 - beta (a clausula do limite retirada de uma folha que a anuncia; a hipotese s >= 0 retirada; a citacao do dispositivo sem [PILOTO][SIM] ou com numero de desempenho; o controle negativo da c13 invertido; o adversario com duas solucoes; o contraexemplo com b <= 1/2) e a ratificacao de 10/11 (um pendente entre os ratificados; ratificacao_pendente esvaziada; o sha256 da fala 28 trocado; a fala adulterada; o estatuto antigo restaurado ou plantado; a frase da ratificacao retirada; um ratificado retirado);''', 1))
T.append(('''e imprime as 12 checagens.''', '''e imprime as 13 checagens.''', 1))
aplicar("_teste_aescala_offline_v410.py", T)
