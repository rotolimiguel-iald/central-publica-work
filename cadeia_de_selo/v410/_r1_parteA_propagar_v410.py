# -*- coding: utf-8 -*-
"""_r1_parteA_propagar_v410.py -- R1, PARTE A, a PROPAGACAO do nucleo ao ensaio e aos conferidores da raiz (o pos_rito e' outro passo): as decisoes D63 a D92; as erratas E29 a E32 mais a dos pisos; os `numeros` do a_escala sem a tautologia escalar;
os dois controles negativos novos do a_escala (kernel nao verificado: c2; raiz sem o import: c3); as contagens das ancoras do a_escala LIDAS do delta e do contrato (sem numero digitado, para a pedra R3); a frase da parede de montagem no h0dn e a funcao de veredito com o MESMO sha256 de texto-fonte
da primeira preparacao (lido de ESPERADOS_v410.pre_r1fix.json); o marcador da frase no artigo PT/EN. Backup de BYTES; temporario -> substituir; ast.parse."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")


def aplicar(rel, trocas):
    p = os.path.join(HERE, rel); b0 = open(p, "rb").read(); crlf = b0.count(b"\r\n") > 0; t = b0.decode("utf-8").replace("\r\n", "\n")
    for a, b, n in trocas:
        c = t.count(a)
        assert (c >= 1 if n is None else c == n), (rel, c, n, a[:150]); t = t.replace(a, b)
    nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8"); ast.parse(nb)
    open(p + ".bak_" + TS + "_pre_r1_propagar", "wb").write(b0)
    open(p + ".tmp", "wb").write(nb); assert os.path.getsize(p + ".tmp") == len(nb); os.replace(p + ".tmp", p)
    print(rel, len(b0), "->", len(nb), "| sha16", hashlib.sha256(b0).hexdigest()[:16], "->", hashlib.sha256(nb).hexdigest()[:16])


aplicar("ensaio_a_seco_v410.py", [
    ('_er10 = _cn10x.get("erratas") or [{}, {}, {}, {}]', '_er10 = _cn10x.get("erratas") or [{}, {}, {}, {}, {}]', 1),
    ('U["cunhagens_v410_as_vinte_e_tres_falas_decisoes_d63_a_d87_erratas_e29_e30_e31_e_pisos_e_leituras"]', 'U["cunhagens_v410_as_vinte_e_tres_falas_decisoes_d63_a_d92_erratas_e29_a_e32_e_pisos_e_leituras"]', 1),
    ('len(DL.ERRATAS_V410) + 1 == 4 and', 'len(DL.ERRATAS_V410) + 1 == 5 and', 1),
    ('and DL.FRASE_D81_PT in str(_er10[2].get("agora"))', 'and DL.FRASE_D81_PT in str(_er10[2].get("agora")) and str(_er10[3].get("agora")).startswith("E32") and _er10[3].get("agora") == DL.ERRATA_E32', 1),
    ('"kh_n1_cobertura_v409" in str(_er10[3].get("ao_lado_de"))', '"kh_n1_cobertura_v409" in str(_er10[4].get("ao_lado_de"))', 1),
    ('for i_ in range(63, 88)}', 'for i_ in range(63, 93)}', 1),
    ('"face_sem_par_ao_quadrado": _hA * _hA, "meio_de_meio": _hA * _hA, ', '', 1),
    ('len(DL.ANCORAS_AESCALA) == DL.N_ANCORAS_AESCALA == 38 == len(_CPA["ancoras"])', 'len(DL.ANCORAS_AESCALA) == DL.N_ANCORAS_AESCALA == len(_CPA["ancoras"]) == _CPA["n_ancoras"] > 0', 1),
    ('"ancoras": _ancA_ok == len(DL.ANCORAS_AESCALA) == _vA.get("n_ancoras_ok") == 38,', '"ancoras": _ancA_ok == len(DL.ANCORAS_AESCALA) == _vA.get("n_ancoras_ok") > 0,', 1),
    ('_dA_ok = um.a_escala_v410(cs())\n',
     'c_ = _rapidoA(); c_["kernel_formalization"] = dict(c_["kernel_formalization"]); c_["kernel_formalization"]["all_verified"] = False; rr_ = um.a_escala_v410(c_)   # (R1, BAIXO 5: o kernel nao verificado)\n'
     '_detA["kernel_nao_verificado"] = {"falhos": _falhos6(rr_), "ok": _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c2"]}\n'
     '_rzA = um._EMBEDDED_KERNEL_FILES["TGLExt.lean"]; um._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = _rzA.replace("import " + _CPA["mod"], "-- retirado")   # (R1, BAIXO 5: a raiz embutida sem o import do modulo)\n'
     'try:\n'
     '    rr_ = um.a_escala_v410(_rapidoA())\n'
     'finally:\n'
     '    um._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = _rzA\n'
     '_detA["raiz_sem_o_import"] = {"falhos": _falhos6(rr_), "ok": _rzA.count("import " + _CPA["mod"]) == 1 and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c3"]}\n'
     '_dA_ok = um.a_escala_v410(cs())\n', 1),
    ('len(_detA) == 11 and', 'len(_detA) == 13 and', 1),
    ('rep["h0dn_bg1_v410_checagens_negadas"] = _detH\n',
     'rep["h0dn_bg1_v410_checagens_negadas"] = _detH\n'
     '# (R1, D92, MEDIO 3) a frase UNICA da parede de montagem do dado: no texto do registro (o_que_falta[0] e uma ressalva) e no contrato, PT e EN, lidas do delta; a funcao de veredito congelada tem o MESMO sha256 de texto-fonte da primeira preparacao (lido do ESPERADOS guardado ao lado)\n'
     '_ESP_R0 = json.load(open(os.path.join(HERE, "ESPERADOS_v410.pre_r1fix.json"), encoding="utf-8"))\n'
     'U["h0dn_bg1_v410_r1_a_frase_da_parede_de_montagem_no_texto_e_no_contrato_e_a_funcao_de_veredito_intocada"] = bool(DL.FRASE_H0DN_PAREDE_PT in rH["o_que_falta"][0] and any(DL.FRASE_H0DN_PAREDE_PT in x_ for x_ in rH["ressalvas"]) and _CPH["frase_parede_pt"] == DL.FRASE_H0DN_PAREDE_PT and _CPH["frase_parede_en"] == DL.FRASE_H0DN_PAREDE_EN\n'
     '                                                                                                                     and rH["veredito_h0dn_source_sha256"] == _ESP_R0["registros_funcao_v410"]["h0dn"]["values"]["veredito_h0dn_source_sha256"] and DL.FRASE_H0DN_OBRIGATORIA_PT in rH["ressalvas"][0] and not um._v410_guarda_frases(DL.FRASE_H0DN_PAREDE_PT) and not um._v410_guarda_frases(DL.FRASE_H0DN_PAREDE_EN))\n', 1),
    ('DEVE = {"pt": [TI410] + DI410 +', 'DEVE = {"pt": ["parede de montagem do dado"] + [TI410] + DI410 +', 1),
    ('        "en": [TI410E] + DI410E +', '        "en": ["a wall in assembling the data"] + [TI410E] + DI410E +', 1),
])
aplicar("conferir_rito_v410.py", [
    ('for n_ in (29, 30, 31))', 'for n_ in (29, 30, 31, 32))', 1),
    ('D63 a D87', 'D63 a D92', None),
    ('E29, E30 e E31', 'E29, E30, E31 e E32', None),
])
aplicar("gerar_esperados_v410.py", [
    ('D63 a D87', 'D63 a D92', None),
    ('E29, E30 e E31', 'E29, E30, E31 e E32', None),
    ('(E29, E30, E31)', '(E29, E30, E31, E32)', None),
])
aplicar("gerar_relatorio_v410.py", [
    ('D63 a D87', 'D63 a D92', None),
])
