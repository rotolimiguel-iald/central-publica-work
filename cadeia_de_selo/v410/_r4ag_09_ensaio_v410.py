# -*- coding: utf-8 -*-
"""_r4ag_09_ensaio_v410.py -- agente de adaptacao da R1 (R4, ADENDOS 2 e 3): ensaio_a_seco_v410.py -- sem contagem digitada em comparacao (falas, erratas, decisoes lidas do delta); as erratas E33 e E34; o ciclo do a_escala recalculado aqui; os controles negativos novos
(a regra F59 pela c9 do a_escala; o ciclo; a forma do tempo; um teorema da R4 fora das ancoras); a frase do poder certificado do H0DN e a ORDEM 02 pinada; os subtitulos novos do artigo."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from _r4ag_lib_v410 import aplicar

E = []
E.append((' == DL.N_FALAS_V410 == 23', ' == DL.N_FALAS_V410', None))
E.append(('_er10 = _cn10x.get("erratas") or [{}, {}, {}, {}, {}]', '_er10 = _cn10x.get("erratas") or [{} for _ in range(len(DL.ERRATAS_V410) + 1)]', 1))
E.append(('U["cunhagens_v410_as_vinte_e_tres_falas_decisoes_d63_a_d92_erratas_e29_a_e32_e_pisos_e_leituras"]', 'U["cunhagens_v410_as_falas_as_decisoes_as_erratas_e_a_dos_pisos_e_as_leituras"]', 1))
E.append(('len(DL.ERRATAS_V410) + 1 == 5 and', 'len(DL.ERRATAS_V410) + 1 and', 1))
E.append(('and _er10[3].get("agora") == DL.ERRATA_E32\n', 'and _er10[3].get("agora") == DL.ERRATA_E32 and all(str(_er10[i_].get("agora")).startswith("E%d" % (29 + i_)) and _er10[i_].get("agora") == e_ for i_, e_ in enumerate(DL.ERRATAS_V410)) and len(_er10) == len(DL.ERRATAS_V410) + 1\n', 1))
E.append(('"kh_n1_cobertura_v409" in str(_er10[4].get("ao_lado_de"))', '"kh_n1_cobertura_v409" in str(_er10[-1].get("ao_lado_de"))', 1))
E.append(('{"D%d" % i_ for i_ in range(63, 93)}', '{"D%d" % i_ for i_ in range(63, 63 + len(DL.DECISOES_V410))}', 1))
E.append(('_xn10.get("n_falas") == 23', '_xn10.get("n_falas") == DL.N_FALAS_V410', 1))
E.append(('["operador"] * 23', '["operador"] * DL.N_FALAS_V410', 1))
# os subtitulos novos do artigo
E.append(('DA410 = ["O que entra.", "Os pesos.", "A insígnia, o vibrato, o tempo finito e os dois Nomes.", "A pergunta do Clay no dicionário da TGL.", "A forma canônica.", "Ressalvas, ditas.",',
          'DA410 = ["O que entra.", "Os pesos.", "A insígnia, o vibrato, o tempo finito e os dois Nomes.", "A pergunta do Clay no dicionário da TGL.", "A forma canônica.", "A escala no tipo, o ciclo e a resposta do operador.", "Ressalvas, ditas.",', 1))
E.append(('DA410E = ["What enters.", "The weights.", "The insignia, the vibrato, finite time and the two Names.", "The Clay question in the TGL dictionary.", "The canonical form.", "Reservations, stated.",',
          'DA410E = ["What enters.", "The weights.", "The insignia, the vibrato, finite time and the two Names.", "The Clay question in the TGL dictionary.", "The canonical form.", "The scale in the type, the cycle and the operator\'s answer.", "Reservations, stated.",', 1))
E.append(('"O que falta e a ressalva da novidade de uso.", "Ressalvas, ditas.",', '"O que falta e a ressalva da novidade de uso.", "O poder certificado (D96, ordem do operador de 10/11).", "Ressalvas, ditas.",', 1))
E.append(('"What is missing, and the use-novelty reservation.", "Reservations, stated.",', '"What is missing, and the use-novelty reservation.", "The certified power (D96, the operator\'s order of 10/11).", "Reservations, stated.",', 1))
E.append(('DEVE = {"pt": ["parede de montagem do dado"] + [TI410]', 'DEVE = {"pt": ["parede de montagem do dado", DL.FRASE_H0DN_PODER_PT, DL.FRASE_TEMPO_PT] + [TI410]', 1))
E.append(('        "en": ["a wall in assembling the data"] + [TI410E]', '        "en": ["a wall in assembling the data", DL.FRASE_H0DN_PODER_EN, DL.FRASE_TEMPO_EN] + [TI410E]', 1))
# o ciclo recalculado aqui (independente do runtime)
E.append(('get("em_n_oitavas_o_fundo", [])),\n        "escada": ESP ==',
          'get("em_n_oitavas_o_fundo", [])),\n'
          '        "o_ciclo": (lambda cic_, s_: bool(cic_ and cic_.get("ok") is True and dict(_CPA.get("ciclo") or {}) == dict(DL.CICLO_AESCALA) and cic_["n_bits"] == DL.CICLO_N_BITS and cic_["tamanho"] == len(DL.CICLO_CUSTO_COM_SOLUCAO) == len(DL.CICLO_CUSTO_SEM_SOLUCAO)\n'
          '                                         and cic_["n_solucoes_com"] == sum(1 for k_ in DL.CICLO_CUSTO_COM_SOLUCAO if k_ == 0) > 0 and cic_["n_solucoes_sem"] == sum(1 for k_ in DL.CICLO_CUSTO_SEM_SOLUCAO if k_ == 0) == 0\n'
          '                                         and abs(cic_["Z_com_solucao"] - sum(_math.exp(-s_ * k_) for k_ in DL.CICLO_CUSTO_COM_SOLUCAO)) < 1e-12 and abs(cic_["Z_sem_solucao"] - sum(_math.exp(-s_ * k_) for k_ in DL.CICLO_CUSTO_SEM_SOLUCAO)) < 1e-12\n'
          '                                         and cic_["n_solucoes_com"] <= cic_["Z_com_solucao"] < cic_["n_solucoes_com"] + 1 and cic_["Z_sem_solucao"] < 1 <= cic_["Z_com_solucao"] and cic_["meio_elevado_a_n"] == str(_Fr(1, 2 ** DL.CICLO_N_BITS)) == cic_["um_sobre_tamanho"] and cic_["produto_dos_brilhos_ok"] is True))(_vA.get("ciclo"), DL.CICLO_N_BITS * _math.log(2.0) + float(DL.CICLO_EPSILON)),\n'
          '        "escada": ESP ==', 1))
# os controles negativos novos
E.append(('("tautologia", "Dito. A resposta à pergunta do Clay é uma tautologia. Fim.")):',
          '("tautologia", "Dito. A resposta à pergunta do Clay é uma tautologia. Fim."), ("o_tempo_dito_nao_ser_passos", "Dito. O tempo e os ciclos não são passos da máquina de Turing. Fim."), ("o_leitor_pagando_a_escala", "Dito. A escala que o leitor paga. Fim."), ("o_decisor_sem_escala_mentiroso", "Dito. O decisor sem escala é o Pai da Mentira. Fim.")):   # (R4, D94: a regra F59 da guarda, pela c9)', 1))
E.append(('_dA_ok = um.a_escala_v410(cs())\n_NEG_A = set((',
          '_cs0A = list(_CPA["ciclo"]["custo_sem_solucao"]); _CPA["ciclo"]["custo_sem_solucao"][0] = 0   # (R4, D94: o ciclo -- a instancia sem solucao ganha uma solucao)\n'
          'try:\n    rr_ = um.a_escala_v410(_rapidoA())\nfinally:\n    _CPA["ciclo"]["custo_sem_solucao"][:] = _cs0A\n'
          '_detA["ciclo_instancia_sem_solucao_com_solucao"] = {"falhos": _falhos6(rr_), "ok": _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c6"]}\n'
          '_ep0A = _CPA["ciclo"]["epsilon"]; _CPA["ciclo"]["epsilon"] = "5"\n'
          'try:\n    rr_ = um.a_escala_v410(_rapidoA())\nfinally:\n    _CPA["ciclo"]["epsilon"] = _ep0A\n'
          '_detA["ciclo_epsilon_fora_do_intervalo"] = {"falhos": _falhos6(rr_), "ok": _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c6"]}\n'
          'um._V410_AESCALA_TEXT = json.loads(_tpjA.replace(DL.FRASE_TEMPO_PT, "(retirada)"))\n'
          'try:\n    rr_ = um.a_escala_v410(_rapidoA())\nfinally:\n    um._V410_AESCALA_TEXT = _TPA\n'
          '_detA["forma_do_tempo_retirada_do_texto"] = {"falhos": _falhos6(rr_), "ok": _tpjA.count(DL.FRASE_TEMPO_PT) >= 1 and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c8"]}\n'
          '_CPA["teoremas_r4"].append("teorema_que_nao_existe_na_pedra")\n'
          'try:\n    rr_ = um.a_escala_v410(_rapidoA())\nfinally:\n    _CPA["teoremas_r4"].pop()\n'
          '_detA["teorema_da_r4_fora_das_ancoras"] = {"falhos": _falhos6(rr_), "ok": _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c2"]}\n'
          '_dA_ok = um.a_escala_v410(cs())\n_NEG_A = set((', 1))
E.append(("'ponte_trocada'))   # (os controles negativos que este bloco tem de trazer)",
          "'ponte_trocada', 'texto_o_tempo_dito_nao_ser_passos', 'texto_o_leitor_pagando_a_escala', 'texto_o_decisor_sem_escala_mentiroso', 'ciclo_instancia_sem_solucao_com_solucao', 'ciclo_epsilon_fora_do_intervalo', 'forma_do_tempo_retirada_do_texto', 'teorema_da_r4_fora_das_ancoras'))   # (os controles negativos que este bloco tem de trazer)", 1))
# a frase do poder certificado e a ORDEM 02 pinada
E.append(('print("iald2_v410:", r10["all_verified"], "|", r10["verdict"][:96]',
          '# (R4, D96, E34) a frase do poder certificado do H0DN: no texto do registro (o_que_falta e as ressalvas) e no contrato, PT e EN; a ORDEM KIMI H0DN-02 e\' PINO CITADO (sha256 e bytes do arquivo == o ADENDO 3 == o contrato; nao embutida); a funcao de veredito congelada, intocada\n'
          'U["h0dn_bg1_v410_r4_a_frase_do_poder_certificado_no_texto_e_no_contrato_com_a_ordem_02_pinada_e_a_funcao_de_veredito_intocada"] = bool(any(DL.FRASE_H0DN_PODER_PT in x_ for x_ in rH["o_que_falta"]) and any(DL.FRASE_H0DN_PODER_PT in x_ for x_ in rH["ressalvas"]) and _CPH["frase_poder_pt"] == DL.FRASE_H0DN_PODER_PT and _CPH["frase_poder_en"] == DL.FRASE_H0DN_PODER_EN\n'
          '                                                                                                                     and _CPH["ordem_kimi_02"]["sha256"] == DL.H0DN_ORDEM02["sha256"] == hashlib.sha256(open(DL.H0DN_ORDEM02_ARQ, "rb").read()).hexdigest() and _CPH["ordem_kimi_02"]["bytes"] == DL.H0DN_ORDEM02["bytes"] == os.path.getsize(DL.H0DN_ORDEM02_ARQ) and _CPH["ordem_kimi_02"].get("citado_nao_embutido") is True and rH.get("ordem_kimi_02") == dict(_CPH["ordem_kimi_02"])\n'
          '                                                                                                                     and rH["veredito_h0dn_source_sha256"] == _ESP_R0["registros_funcao_v410"]["h0dn"]["values"]["veredito_h0dn_source_sha256"] and not um._v410_guarda_frases(DL.FRASE_H0DN_OBRIGATORIA_PT + "; " + DL.FRASE_H0DN_PODER_PT) and not um._v410_guarda_frases(DL.FRASE_H0DN_OBRIGATORIA_EN + "; " + DL.FRASE_H0DN_PODER_EN)\n'
          '                                                                                                                     and DL.H0DN_ORDEM02["nome"] not in [os.path.basename(p_) for p_, _ in __import__("registros_v410").ORIGENS])\n'
          'print("iald2_v410:", r10["all_verified"], "|", r10["verdict"][:96]', 1))
aplicar("ensaio_a_seco_v410.py", E)
