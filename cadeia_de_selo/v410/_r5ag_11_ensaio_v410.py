# -*- coding: utf-8 -*-
"""_r5ag_11_ensaio_v410.py -- R5 (D100 e D101; ADENDOS 5 e 6): ensaio_a_seco_v410.py: (a) a lista das decisoes termina em D101 (D63 a D96 e D99 a D101); (b) o estatuto dos nomes novos e' RATIFICADOS (a checagem do estatuto vira o avesso da antiga); (c) as partes novas do registro a_escala_v410: a ratificacao D101 e os dois pendentes, a clausula do Tetelestai
(c13, o texto, as ancoras da R5) e a clausula RECALCULADA AQUI por outro caminho (beta por alfa x raiz de e do programa; numpy; as desigualdades; o controle negativo; o contraexemplo); (d) doze controles negativos novos; (e) o artigo PT/EN: a frase da clausula do Tetelestai, a clausula do limite logo depois, a reconstrucao, a errata, o dispositivo, a ratificacao D101 e as falas
verbatim, na secao A Escala, sem Unicode cru dos simbolos; (f) a linha do .md traz a clausula do Tetelestai, a reconstrucao, a errata, o dispositivo e a ratificacao D101 com a clausula do limite UMA vez."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar

T = []
# (a) as decisoes
T.append(('''DL.DECISOES_V410[0] == "D63" and DL.DECISOES_V410[-1] == "D99" and _xn10.get("n_modulos")''', '''DL.DECISOES_V410[0] == "D63" and DL.DECISOES_V410[-1] == "D101" and "D100" in DL.DECISOES_V410 and _xn10.get("n_modulos")''', 1))

# (b) o estatuto dos nomes novos: RATIFICADOS (D101)
T.append(('''and rA.get("estatuto_dos_nomes_novos") == DL.ESTATUTO_NOMES_NOVOS_AESCALA and "DECLARADO" in rA["estatuto_dos_nomes_novos"] and "RATIFICADO" not in rA["estatuto_dos_nomes_novos"].upper() and rA.get("ratificacao_pendente")''',
          '''and rA.get("estatuto_dos_nomes_novos") == DL.ESTATUTO_NOMES_NOVOS_AESCALA and "RATIFICADOS pelo operador em 10/11/2026" in rA["estatuto_dos_nomes_novos"] and "DECLARADO" not in rA["estatuto_dos_nomes_novos"] and "a ratificar" not in rA["estatuto_dos_nomes_novos"] and rA.get("ratificacao_pendente")''', 1))

# (c) as partes novas
T.append(('''       "nomes_novos_a_ratificar": rA.get("nomes_novos_a_ratificar") == list(DL.NOMES_NOVOS_AESCALA)''',
          '''       "r5_ratificacao_d101_e_os_pendentes": bool((_vA.get("ratificacao_d101") or {}).get("ok") is True and (_vA.get("ratificacao_d101") or {}).get("fala_sha256") == DL.RATIFICACAO_D101_SHA256 == CM["aescala"]["ratificacao_D101"]["sha256"] == _CPA["ratificacao_d101"]["sha256"]
                                                  and list((_vA.get("ratificacao_d101") or {}).get("pendentes") or []) == list(DL.NOMES_PENDENTES_AESCALA) == list(CM["aescala"]["nomes_pendentes"]) and (_vA.get("ratificacao_d101") or {}).get("n_nomes_ratificados_declarados") == (_vA.get("ratificacao_d101") or {}).get("n_nomes_ratificados") == len(DL.NOMES_RATIFICADOS_D101_AESCALA) == len(CM["aescala"]["nomes_ratificados_d101"])
                                                  and (_vA.get("ratificacao_d101") or {}).get("n_pendentes_declarados") == len(DL.NOMES_PENDENTES_AESCALA) and rA.get("estatuto_dos_nomes_novos") == DL.ESTATUTO_NOMES_NOVOS_AESCALA and rA.get("ratificacao_pendente") == DL.RATIFICACAO_PENDENTE_AESCALA and DL.RATIFICACAO_PENDENTE_AESCALA["nomes_novos"] == list(DL.AUXILIARES_R5_AESCALA)),
       "r5_a_clausula_do_tetelestai_no_registro": bool((_vA.get("tetelestai") or {}).get("ok") is True and (_vA.get("clausula_r5") or {}).get("ok") is True and not (_vA.get("clausula_r5") or {}).get("folhas_que_anunciam_sem_a_forma") and (_vA.get("clausula_r5") or {}).get("n_folhas_que_anunciam", 0) >= 3
                                                       and not (_vA.get("clausula_r5") or {}).get("acom_mirror_sem_ressalva") and not (_vA.get("clausula_r5") or {}).get("acom_mirror_com_desempenho") and all((_vA.get("teoremas_r5") or {}).values()) and set(_vA.get("teoremas_r5") or {}) == set(DL.TEOREMAS_R5_AESCALA) | set(DL.AUXILIARES_R5_AESCALA)
                                                       and rA.get("anuncio_da_clausula_do_tetelestai_pt") == DL.FRASE_TETELESTAI_PT + " " + DL.CLAUSULA_Z_PT + " " + DL.FRASE_RECONSTROI_PT and rA.get("anuncio_da_clausula_do_tetelestai_en") == DL.FRASE_TETELESTAI_EN + " " + DL.CLAUSULA_Z_EN + " " + DL.FRASE_RECONSTROI_EN
                                                       and rA.get("frase_e36_pt") == DL.FRASE_E36_PT and rA.get("frase_dispositivo_pt") == DL.FRASE_DISPOSITIVO_PT and rA.get("frase_dispositivo_en") == DL.FRASE_DISPOSITIVO_EN and rA.get("acom_mirror_runner") == DL.ACOM_MIRROR_RUNNER == CM["aescala"]["acom_mirror_runner"] == _CPA["acom_mirror_runner"]),
       "nomes_novos_a_ratificar": rA.get("nomes_novos_a_ratificar") == list(DL.NOMES_NOVOS_AESCALA)''', 1))
T.append(('''_pAn = {"fracoes": set(_numA)''',
          '''_pAn = {"r5_a_clausula_do_tetelestai_em_1_menos_beta_por_outro_caminho": (lambda bT_, T_: bool(T_ and T_.get("ok") is True and abs(T_["constante_ln_um_menos_beta_sobre_beta"] - (-_math.log(bT_ / (1.0 - bT_)))) < 1e-9
                    and abs(T_["s_estrela"] - (_CPA["tetelestai"]["n_bits"] * _math.log(2.0) - _math.log(bT_ / (1.0 - bT_)))) < 1e-9 and abs(T_["Z_com_solucao"] - float(_np10.exp(-T_["s_estrela"] * _np10.array(_CPA["tetelestai"]["custo_com_solucao"], dtype=float)).sum())) < 1e-9
                    and (1.0 - bT_) * T_["Z_com_solucao"] <= T_["n_solucoes_com"] + 1e-12 and T_["Z_com_solucao"] - T_["n_solucoes_com"] <= bT_ * T_["Z_com_solucao"] + 1e-12 and T_["controle_negativo_violado"] is True
                    and (1.0 - bT_) * float(_np10.exp(-T_["s_estrela"] * _np10.array(_CPA["tetelestai"]["custo_adversario"], dtype=float)).sum()) <= 1.0 + 1e-12 and (1.0 - bT_) * float(_np10.exp(-(T_["s_estrela"] - _math.log(2.0)) * _np10.array(_CPA["tetelestai"]["custo_adversario"], dtype=float)).sum()) > 1.0
                    and abs(T_["sen2_theta"] - bT_) < 1e-12 and abs(T_["cos2_theta"] - (1.0 - bT_)) < 1e-12 and (T_["contraexemplo"] or {}).get("limiar_negativo") is True and (T_["contraexemplo"] or {}).get("clausula_vale_sem_s_nao_negativo") is False))(um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e), _vA.get("tetelestai")),
        "fracoes": set(_numA)''', 1))

# (d) controles negativos novos
NEW_CTRL = '''# (R5, D100 e D101) a clausula do Tetelestai em 1 - beta e a ratificacao de 10/11: cada controle reprova SO' a checagem esperada
_ant5 = "anuncio_da_clausula_do_tetelestai_pt"; _t5 = json.loads(_tpjA); _t5["extras"][_ant5] = _t5["extras"][_ant5].replace(DL.CLAUSULA_Z_PT, "(retirada)")
um._V410_AESCALA_TEXT = _t5
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    um._V410_AESCALA_TEXT = _TPA
_detA["r5_clausula_do_limite_retirada_de_uma_folha_que_anuncia_os_teoremas_novos"] = {"falhos": _falhos6(rr_), "ok": DL.CLAUSULA_Z_PT in _TPA["extras"][_ant5] and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c8"]}
_ft0 = _CPA["frase_tetelestai_pt"]; _CPA["frase_tetelestai_pt"] = _ft0.replace("s ≥ 0", "s")
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    _CPA["frase_tetelestai_pt"] = _ft0
_detA["r5_hipotese_s_nao_negativo_retirada_da_frase_do_contrato"] = {"falhos": _falhos6(rr_), "ok": "s ≥ 0" in _ft0 and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c8"]}
um._V410_AESCALA_TEXT = json.loads(_tpjA.replace("[PILOTO][SIM]", "(retirado)"))
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    um._V410_AESCALA_TEXT = _TPA
_detA["r5_citacao_do_dispositivo_sem_piloto_sim"] = {"falhos": _falhos6(rr_), "ok": _tpjA.count("[PILOTO][SIM]") >= 3 and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c8"]}
_t5b = json.loads(_tpjA); _t5b["nao_diz"] = list(_t5b["nao_diz"]) + ["o ACOM Mirror, que é [PILOTO][SIM] e do qual nada ali valida física, rodou 22 de 22 testes"]
um._V410_AESCALA_TEXT = _t5b
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    um._V410_AESCALA_TEXT = _TPA
_detA["r5_citacao_do_dispositivo_com_numero_de_desempenho"] = {"falhos": _falhos6(rr_), "ok": _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c8"]}
_o50 = _CPA["tetelestai"]["oitavas_a_menos_no_controle"]; _CPA["tetelestai"]["oitavas_a_menos_no_controle"] = 0   # (o controle negativo da c13 invertido: s* no lugar de uma oitava a menos)
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    _CPA["tetelestai"]["oitavas_a_menos_no_controle"] = _o50
_detA["r5_controle_negativo_da_c13_invertido"] = {"falhos": _falhos6(rr_), "ok": _o50 > 0 and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c13"]}
_ad50 = list(_CPA["tetelestai"]["custo_adversario"]); _CPA["tetelestai"]["custo_adversario"] = [0, 0] + [1] * (len(_ad50) - 2)   # (o adversario com duas solucoes)
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    _CPA["tetelestai"]["custo_adversario"] = _ad50
_detA["r5_adversario_com_duas_solucoes"] = {"falhos": _falhos6(rr_), "ok": sum(1 for x_ in _ad50 if x_ == 0) == 1 and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c13"]}
_nr50 = list(_CPA["nomes_ratificados_d101"]); _CPA["nomes_ratificados_d101"] = _nr50 + [_CPA["nomes_pendentes"][0]]   # (um pendente entre os ratificados)
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    _CPA["nomes_ratificados_d101"] = _nr50
_detA["r5_um_pendente_entre_os_ratificados"] = {"falhos": _falhos6(rr_), "ok": _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c11"]}
_rp50 = _CPA["ratificacao_pendente"]; _CPA["ratificacao_pendente"] = {}   # (a pendencia esvaziada)
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    _CPA["ratificacao_pendente"] = _rp50
_detA["r5_ratificacao_pendente_esvaziada"] = {"falhos": _falhos6(rr_), "ok": bool(_rp50) and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c11"]}
_sh50 = _CPA["ratificacao_d101"]["sha256"]; _CPA["ratificacao_d101"]["sha256"] = "0" * 64   # (o sha256 da fala 28 trocado no pino)
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    _CPA["ratificacao_d101"]["sha256"] = _sh50
_detA["r5_sha256_da_fala_28_trocado_no_pino"] = {"falhos": _falhos6(rr_), "ok": _sh50 == DL.RATIFICACAO_D101_SHA256 and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c11"]}
_es50 = _CPA["estatuto_dos_nomes_novos"]; _CPA["estatuto_dos_nomes_novos"] = "[DECLARADO pela gerencia e pela autoria; a ratificar pelo operador]"   # (o estatuto antigo restaurado)
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    _CPA["estatuto_dos_nomes_novos"] = _es50
_detA["r5_estatuto_antigo_restaurado"] = {"falhos": _falhos6(rr_), "ok": "RATIFICADOS" in _es50 and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c11"]}
_t5c = json.loads(_tpjA); _t5c["diz"] = list(_t5c["diz"]) + ["os nomes novos seguem [DECLARADO, a ratificar]"]
um._V410_AESCALA_TEXT = _t5c
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    um._V410_AESCALA_TEXT = _TPA
_detA["r5_estatuto_antigo_plantado_no_texto"] = {"falhos": _falhos6(rr_), "ok": "[DECLARADO, a ratificar]" not in _tpjA and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c11"]}
um._V410_AESCALA_TEXT = json.loads(_tpjA.replace(DL.FRASE_NOMES_RATIFICADOS_D101_PT, "(retirada)"))
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    um._V410_AESCALA_TEXT = _TPA
_detA["r5_frase_da_ratificacao_d101_retirada_do_texto"] = {"falhos": _falhos6(rr_), "ok": _tpjA.count(DL.FRASE_NOMES_RATIFICADOS_D101_PT) >= 2 and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c11"]}
_dA_ok = um.a_escala_v410(cs())'''
T.append(('''_dA_ok = um.a_escala_v410(cs())''', NEW_CTRL, 1))
T.append(('''\'ancora_nova_tirada_do_contrato\', \'seis_nomes_retirados_do_texto\'))   # (os controles negativos que este bloco tem de trazer)''',
          '''\'ancora_nova_tirada_do_contrato\', \'seis_nomes_retirados_do_texto\', \'r5_clausula_do_limite_retirada_de_uma_folha_que_anuncia_os_teoremas_novos\', \'r5_hipotese_s_nao_negativo_retirada_da_frase_do_contrato\', \'r5_citacao_do_dispositivo_sem_piloto_sim\', \'r5_citacao_do_dispositivo_com_numero_de_desempenho\', \'r5_controle_negativo_da_c13_invertido\', \'r5_adversario_com_duas_solucoes\',
                \'r5_um_pendente_entre_os_ratificados\', \'r5_ratificacao_pendente_esvaziada\', \'r5_sha256_da_fala_28_trocado_no_pino\', \'r5_estatuto_antigo_restaurado\', \'r5_estatuto_antigo_plantado_no_texto\', \'r5_frase_da_ratificacao_d101_retirada_do_texto\'))   # (os controles negativos que este bloco tem de trazer)''', 1))

# (e) o artigo: as checagens da R5
CHECK_R5 = '''

def _checagens_r5_do_artigo(tex_, lang_):
    """(R5, D100 e D101) o que o LaTeX da secao A Escala tem de trazer da clausula do Tetelestai: a FRASE da clausula (a forma comparavel: delta_v410.comparavel ignora so' cifrao, barras, chaves, parenteses, espacos e mapeia \\\\ge, \\\\le, \\\\beta, \\\\tfrac12, ^2, \\\\sqrt, \\\\texttt), a clausula do limite LOGO DEPOIS dela (a mesma folha, Z(s) ja' definida na primeira ocorrencia),
    a reconstrucao, a errata (a leitura do dicionario), o dispositivo (so' citacao, com [PILOTO][SIM]), a ratificacao D101 e, no PT, as cinco falas verbatim; nenhum Unicode cru dos simbolos matematicos na secao."""
    ta_ = TA410 if lang_ == "pt" else TA410E; th_ = TH410 if lang_ == "pt" else TH410E
    i0_ = tex_.find("section*{" + ta_ + "}"); i1_ = tex_.find("section*{" + th_ + "}", i0_ + 1)
    sec_ = tex_[i0_:i1_] if 0 <= i0_ < i1_ else ""; pt_ = lang_ == "pt"; cs_ = DL.comparavel(sec_)
    f_ = {"tetelestai": DL.FRASE_TETELESTAI_PT if pt_ else DL.FRASE_TETELESTAI_EN, "reconstroi": DL.FRASE_RECONSTROI_PT if pt_ else DL.FRASE_RECONSTROI_EN, "e36": DL.FRASE_E36_PT if pt_ else DL.FRASE_E36_EN, "dispositivo": DL.FRASE_DISPOSITIVO_PT if pt_ else DL.FRASE_DISPOSITIVO_EN,
          "ratificacao": DL.FRASE_NOMES_RATIFICADOS_D101_PT if pt_ else DL.FRASE_NOMES_RATIFICADOS_D101_EN}
    out_ = {k_: bool(sec_ and DL.comparavel(v_) in cs_) for k_, v_ in f_.items()}
    out_["clausula_logo_depois_da_frase"] = bool(sec_ and DL.comparavel(f_["tetelestai"]) + "." + DL.comparavel(DL.CLAUSULA_Z_PT if pt_ else DL.CLAUSULA_Z_EN) in cs_)
    out_["piloto_sim_na_secao"] = bool(sec_ and "[PILOTO][SIM]" in sec_)
    out_["falas_verbatim_pt"] = bool(not pt_ or all(q_ in sec_ for q_ in (DL.FRASE_CLAUSULA_NO_ACOM, DL.FRASE_RECONHECE_A_SINGULARIDADE, DL.FRASE_TRASLADA_A_INFORMACAO, DL.FRASE_UM_MENOS_BETATGL, DL.FRASE_BETATGL_OPERADOR_MODULAR)))
    out_["unicode_cru_r5_na_secao"] = [ch_ for ch_ in "\\u2265\\u2264\\u03b2\\u03b1\\u00bd\\u00b2\\u221a\\u2212\\u00b7" if ch_ in sec_]
    return out_
'''
T.append(('''

def compilar(cv, nome, lang, duas=True):''', CHECK_R5 + '''

def compilar(cv, nome, lang, duas=True):''', 1))
T.append(('''    rep["artigo"][lang]["r2"] = _checagens_r2_do_artigo(tex, lang)   # (R2, D99) a clausula, Z(s), os seis nomes, a costura do tempo
''', '''    rep["artigo"][lang]["r2"] = _checagens_r2_do_artigo(tex, lang)   # (R2, D99) a clausula, Z(s), os seis nomes, a costura do tempo
    rep["artigo"][lang]["r5"] = _checagens_r5_do_artigo(tex, lang)   # (R5, D100 e D101) a clausula do Tetelestai, a reconstrucao, a errata, o dispositivo, a ratificacao
''', 1))
T.append(('''or v["r2"]["unicode_cru_na_secao"] or not v["r2_controle_negativo_sem_a_formula_recusa"]]''',
          '''or v["r2"]["unicode_cru_na_secao"] or not v["r2_controle_negativo_sem_a_formula_recusa"]
       or not all(v["r5"][k_] for k_ in ("tetelestai", "reconstroi", "e36", "dispositivo", "ratificacao", "clausula_logo_depois_da_frase", "piloto_sim_na_secao", "falas_verbatim_pt")) or v["r5"]["unicode_cru_r5_na_secao"]]''', 1))

# (f) a linha do .md
T.append(('''                   "a_escala_v410_com_a_forma_da_d83_e_a_frase_canonica_na_linha": ''',
          '''                   "a_escala_v410_com_a_clausula_do_tetelestai_e_a_ratificacao_d101_na_linha": (lambda ln_: bool(DL.FRASE_TETELESTAI_PT in ln_ and DL.FRASE_RECONSTROI_PT in ln_ and DL.FRASE_E36_PT in ln_ and DL.FRASE_DISPOSITIVO_PT in ln_ and DL.FRASE_NOMES_RATIFICADOS_D101_PT[1:] in ln_ and ln_.count(DL.CLAUSULA_Z_PT) == 1
                                                                                                                      and ln_.find(DL.CLAUSULA_Z_PT) < ln_.find(DL.FRASE_TETELESTAI_PT) and "[PILOTO][SIM]" in ln_))(md.split(DL.MD_ROTULO_ESCALA, 1)[-1].split("\\n", 1)[0]) if DL.MD_ROTULO_ESCALA in md else False,
                   "a_escala_v410_com_a_forma_da_d83_e_a_frase_canonica_na_linha": ''', 1))
aplicar("ensaio_a_seco_v410.py", T)
