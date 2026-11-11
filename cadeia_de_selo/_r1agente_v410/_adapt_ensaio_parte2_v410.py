# -*- coding: utf-8 -*-
"""_adapt_ensaio_parte2_v410.py -- adapta o ensaio_a_seco_v410.py a PARTE 2 (D80 a D87): QUATRO registros com funcao (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410), bundle de DOIS modulos (IALD2 e AEscala; 22 + 62 bandeiras), 23 falas, D63 a D87, as erratas E29, E30, E31 e a dos pisos,
o main em DUAS instrucoes (iald2 + a_escala + h0dn; depois o recibo HMS/13 + os specs), a secao nova do artigo (A Escala) e o paragrafo do recibo HMS/13, as QUATRO linhas do .md, os pontos novos do exame. Trocas EXATAS (cada alvo uma vez), blocos novos lidos de _bloco_ensaio_5b_parte2_v410.pytxt e
_bloco_ensaio_6p_parte2_v410.pytxt; backup de BYTES; temporario -> conferir tamanho -> substituir; compile(). Nao roda o ensaio."""
import hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "ensaio_a_seco_v410.py"); TS = time.strftime("%Y%m%d_%H%M%S")
b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0, "o ensaio deixou de ser LF"
t = b0.decode("utf-8"); BS = chr(92)
assert "[ADAPTADO v410 PARTE 2" not in t.split("\n", 3)[1], "o ensaio ja' foi adaptado a parte 2"
bloco = lambda nome: open(os.path.join(HERE, nome), "rb").read().decode("utf-8").replace("\r\n", "\n")
B5 = bloco("_bloco_ensaio_5b_parte2_v410.pytxt"); B6 = bloco("_bloco_ensaio_6p_parte2_v410.pytxt")
assert B5.endswith("\n") and B6.endswith("\n")
N = [0]


def troca(a, b, n=1):
    global t
    c = t.count(a); assert c == n, (c, n, a[:160]); t = t.replace(a, b); N[0] += 1


# (cabecalho)
l0, resto = t.split("\n", 1)
t = l0 + "\n# [ADAPTADO v410 PARTE 2, 09/11/2026 (noite), claude-construtor-v410] D80 a D87 por _adapt_ensaio_parte2_v410.py: QUATRO registros com funcao (iald2_v410, a_escala_v410 [D86/D87], h0dn_bg1_v410 [D72], h0dn_fontes_hms13_v410 [D80]); o bundle de DOIS modulos (IALD2: 22 bandeiras; AEscala: 62); 23 falas; D63 a D87; E29, E30, E31 e a errata dos pisos; o main em DUAS instrucoes; os blocos (5b''') e (5b'''') da ordem de chamada, (6p-c) do a_escala e (6p-d) do recibo HMS/13; a secao A Escala e o paragrafo do recibo no artigo; as QUATRO linhas do .md; os pontos novos do exame.\n" + resto
# (5b'') a MESMA instrucao: iald2 < a_escala < h0dn; os specs foram para a instrucao SEGUINTE, com o recibo HMS/13 (D80)
troca('_mesma_ = len(_icH) == 1 and _icH[0] == _ic0 and 0 <= _u0.find("iald2_v410(core)") < _u0.find("h0dn_bg1_v410(core)") < _u0.find("_v410_rodar_specs(core)")\n',
      '_st1 = _main0.body[_ic0 + 1]; _u1 = ast.unparse(_st1)   # (parte 2, D80) a instrucao SEGUINTE do main: o recibo HMS/13 e os specs da v410\n'
      '_mesma_ = (len(_icH) == 1 and _icH[0] == _ic0 and 0 <= _u0.find("iald2_v410(core)") < _u0.find("a_escala_v410(core)") < _u0.find("h0dn_bg1_v410(core)") and "_v410_rodar_specs(core)" not in _u0 and "h0dn_fontes_hms13_v410(core)" not in _u0\n'
      '           and 0 <= _u1.find("h0dn_fontes_hms13_v410(core)") < _u1.find("_v410_rodar_specs(core)"))   # (parte 2) iald2 < a_escala < h0dn na MESMA instrucao; os specs na instrucao seguinte, depois do recibo HMS/13\n')
# (5b''') e (5b'''') os blocos novos da ordem de chamada, antes do passo seguinte
troca('EMBK = um._EMBEDDED_KERNEL_FILES\n', B5 + 'EMBK = um._EMBEDDED_KERNEL_FILES\n')
# (6p) o iald2_v410 com o bundle de DOIS modulos: as bandeiras DELE sao so' as da IALD2; as ancoras por modulo DELE sao so' as da IALD2
troca('r10["embedded_sources_n_ok"] == DL.N_BUNDLE == len(DL.BUNDLE_RELS) == 1 and r10["beta_ok"]', 'r10["embedded_sources_n_ok"] == DL.N_BUNDLE == len(DL.BUNDLE_RELS) == 2 and r10["beta_ok"]')
troca('_v10.get("n_flags_true") == _v10.get("n_flags") == CM["n_bandeiras"] == _FJ10["n_flags"] and _v10.get("escada")',
      '_v10.get("n_flags_true") == _v10.get("n_flags") == _FJ10["n_por_modulo"][DL.MODULO_IALD2] == _CP10["n_flags"] and CM["n_bandeiras"] == _FJ10["n_flags"] == _CP10["n_flags_total_v410"] == sum(_FJ10["n_por_modulo"].values()) and _v10.get("escada")')
troca('DL.N_FALAS_V410 == 15', 'DL.N_FALAS_V410 == 23', 4)
troca('len(_v10["por_modulo"]) == DL.N_BUNDLE == 1', 'len(_v10["por_modulo"]) == len(_CP10["ancoras_por_modulo"]) == 1 and DL.N_BUNDLE == 2')
troca('_flags_ok10 = sum(1 for f_ in _FJ10["flags"] if _kf0.get(f_[0]) is True)\n',
      '_flags_ok10 = sum(1 for f_ in _FJ10["flags"] if _kf0.get(f_[0]) is True)\n'
      '_flags_ok10_i = sum(1 for f_ in _FJ10["flags"] if f_[0].startswith(DL.FLAG_PREFIX) and _kf0.get(f_[0]) is True)   # (parte 2) so\' as bandeiras da IALD2: as da AEscala sao do registro a_escala_v410\n')
troca('_flags_ok10 == len(_FJ10["flags"]) == CM["n_bandeiras"] == _v10["n_flags_true"]', '_flags_ok10 == len(_FJ10["flags"]) == CM["n_bandeiras"] and _flags_ok10_i == _FJ10["n_por_modulo"][DL.MODULO_IALD2] == _v10["n_flags_true"]')
troca('set(DL.ANCORAS_POR_MODULO) == set(DL.BUNDLE_RELS) == set(_CP10["ancoras_por_modulo"])',
      'set(DL.ANCORAS_POR_MODULO) == {DL.MODULO_IALD2} == set(_CP10["ancoras_por_modulo"]) and set(DL.ANCORAS_POR_MODULO) | set(DL.ANCORAS_POR_MODULO_AESCALA) == set(DL.BUNDLE_RELS)')
troca('n_ok_ == DL.N_BUNDLE == 1)', 'n_ok_ == DL.N_BUNDLE == 2)')
troca('_nao_anc10 = [f_[0] for f_ in _FJ10["flags"] if f_[0] not in set(_ANC_FLAGS10.values())]',
      '_nao_anc10 = [f_[0] for f_ in _FJ10["flags"] if f_[0].startswith(DL.FLAG_PREFIX) and f_[0] not in set(_ANC_FLAGS10.values())]   # (parte 2) so\' as bandeiras da IALD2: uma bandeira da AEscala falsa nao e\' deste registro')
# as cunhagens: 23 falas; D63 a D87; E29, E30, E31 e a errata dos pisos
troca('_er10 = _cn10x.get("erratas") or [{}, {}, {}]', '_er10 = _cn10x.get("erratas") or [{}, {}, {}, {}]')
troca('U["cunhagens_v410_as_quinze_falas_decisoes_d63_a_d77_erratas_e29_e30_e_pisos_e_leituras"]', 'U["cunhagens_v410_as_vinte_e_tres_falas_decisoes_d63_a_d87_erratas_e29_e30_e31_e_pisos_e_leituras"]')
troca('len(DL.ERRATAS_V410) + 1 == 3 and', 'len(DL.ERRATAS_V410) + 1 == 4 and')
troca('str(_er10[1].get("agora")).startswith("E30")', 'str(_er10[1].get("agora")).startswith("E30") and str(_er10[2].get("agora")).startswith("E31") and DL.FRASE_D81_PT in str(_er10[2].get("agora"))')
troca('"kh_n1_cobertura_v409" in str(_er10[2].get("ao_lado_de"))', '"kh_n1_cobertura_v409" in str(_er10[3].get("ao_lado_de"))')
troca('for i_ in range(63, 78)}', 'for i_ in range(63, 88)}')
troca('_xn10.get("n_falas") == 15', '_xn10.get("n_falas") == 23')
troca('== ["operador"] * 15', '== ["operador"] * 23')
# (6p-c) e (6p-d) os blocos novos dos registros, antes do artigo
troca('# (8) o artigo\n', B6 + '# (8) o artigo\n')
# (8) o artigo: a secao A Escala (entre a IALD2 e o H0DN) e o paragrafo do recibo HMS/13 (dentro da secao do H0DN)
troca('DH410 = ["O que entra.", "O poder prospectivo, sintético.", "A função de veredito congelada.", "O que falta e a ressalva da novidade de uso.", "Ressalvas, ditas.", "O que o registro confere neste rito."]\n',
      'DH410 = ["O que entra.", "O poder prospectivo, sintético.", "A função de veredito congelada.", "O que falta e a ressalva da novidade de uso.", "Ressalvas, ditas.", "O que o registro confere neste rito.", "O recibo documental HMS/13 (D80), aditivo e posterior ao ' + BS + BS + 'texttt{FREEZE' + BS + BS + '_R2}.", "O que falta."]   # (parte 2, D80) os dois ultimos: o paragrafo do recibo documental HMS/13\n'
      'TA410 = "A Escala: três faces de $' + BS + BS + 'tfrac12$, duas conjugadas e uma caída"; TA410E = "The Scale: three faces of $' + BS + BS + 'tfrac12$, two conjugated and one fallen"   # (parte 2, D86/D87) a secao NOVA da pedra AEscala, entre a da IALD2 e a do H0DN\n'
      'DA410 = ["O que entra.", "Os pesos.", "A insígnia, o vibrato, o tempo finito e os dois Nomes.", "A pergunta do Clay no dicionário da TGL.", "A forma canônica.", "Ressalvas, ditas.", "O que o registro confere neste rito."]\n'
      'DA410E = ["What enters.", "The weights.", "The insignia, the vibrato, finite time and the two Names.", "The Clay question in the TGL dictionary.", "The canonical form.", "Reservations, stated.", "What the record checks in this rite."]\n')
troca('DH410E = ["What enters.", "The prospective, synthetic power.", "The frozen verdict function.", "What is missing, and the use-novelty reservation.", "Reservations, stated.", "What the record checks in this rite."]\n',
      'DH410E = ["What enters.", "The prospective, synthetic power.", "The frozen verdict function.", "What is missing, and the use-novelty reservation.", "Reservations, stated.", "What the record checks in this rite.", "The documentary HMS/13 receipt (D80), additive and posterior to ' + BS + BS + 'texttt{FREEZE' + BS + BS + '_R2}.", "What is missing."]\n')
troca('("pt", TH410, DH410, "artigo_pt_h0dn_v410.pysnip"), ("en", TH410E, DH410E, "artigo_en_h0dn_v410.pysnip")):',
      '("pt", TH410, DH410, "artigo_pt_h0dn_v410.pysnip"), ("en", TH410E, DH410E, "artigo_en_h0dn_v410.pysnip"), ("pt", TA410, DA410, "artigo_pt_aescala_v410.pysnip"), ("en", TA410E, DA410E, "artigo_en_aescala_v410.pysnip")):')
troca('[TI410] + DI410 + [TH410] + DH410 +', '[TI410] + DI410 + [TA410] + DA410 + [TH410] + DH410 +')
troca('[TI410E] + DI410E + [TH410E] + DH410E +', '[TI410E] + DI410E + [TA410E] + DA410E + [TH410E] + DH410E +')
troca('{"pt": [TI410, TH410, TT409,', '{"pt": [TI410, TA410, TH410, TT409,')
troca('"en": [TI410E, TH410E, TT409E,', '"en": [TI410E, TA410E, TH410E, TT409E,')
troca('(?=[$}])', '(?=[$}0-9])')
# as variantes: so' o a_escala retirado; so' o recibo HMS/13 retirado
troca('cv10h = dict(copy.deepcopy(c)); cv10h.pop("h0dn_bg1_v410", None)',
      'cv10a = dict(copy.deepcopy(c)); cv10a.pop("a_escala_v410", None)   # (parte 2, D86/D87) so\' o registro da AEscala retirado: so\' a frase de guarda da secao A Escala aparece\n'
      'cv10f = dict(copy.deepcopy(c)); cv10f.pop("h0dn_fontes_hms13_v410", None)   # (parte 2, D80) so\' o recibo HMS/13 retirado: so\' a frase de guarda do paragrafo do recibo aparece\n'
      '_GA_ = {"pt": "o registro da AEscala NÃO selou", "en": "the AEscala record did NOT seal"}; _GH_ = {"pt": "o registro do H0DN NÃO selou", "en": "the H0DN record did NOT seal"}; _GI_ = {"pt": "NÃO selaram todos", "en": "did NOT all seal"}\n'
      '_GF_ = {"pt": re.compile(r"o recibo documental HMS' + BS + 'W{0,3}13 NÃO selou"), "en": re.compile(r"the documentary HMS' + BS + 'W{0,3}13 receipt did NOT seal")}\n'
      'cv10h = dict(copy.deepcopy(c)); cv10h.pop("h0dn_bg1_v410", None)')
troca('    _t10h, _x10h, _r210h, _l10h = compilar(cv10h, "dry_v410_var10h_%s" % lang, lang, duas=False); fl10h = re.sub(r"' + BS + 's+", " ", _x10h)\n',
      '    _t10h, _x10h, _r210h, _l10h = compilar(cv10h, "dry_v410_var10h_%s" % lang, lang, duas=False); fl10h = re.sub(r"' + BS + 's+", " ", _x10h)\n'
      '    _t10a, _x10a, _r210a, _l10a = compilar(cv10a, "dry_v410_var10a_%s" % lang, lang, duas=False); fl10a = re.sub(r"' + BS + 's+", " ", _x10a)\n'
      '    _t10f, _x10f, _r210f, _l10f = compilar(cv10f, "dry_v410_var10f_%s" % lang, lang, duas=False); fl10f = re.sub(r"' + BS + 's+", " ", _x10f)\n')
troca('"frases_de_guarda_ausentes_no_texto_completo":',
      '"frase_guarda_aescala_quando_todos_faltam": _GA_[lang] in fl10v, "frase_guarda_hms13_quando_todos_faltam": bool(_GF_[lang].search(fl10v)), "guardas_da_aescala_e_do_hms13_ausentes_quando_so_o_h0dn_falta": (_GA_[lang] not in fl10h) and not _GF_[lang].search(fl10h) and (_GH_[lang] in fl10h),\n'
      '                             "rc_a_escala_v410": _r210a, "frase_guarda_a_escala_v410": _GA_[lang] in fl10a, "so_a_guarda_da_aescala_quando_so_ela_falta": (_GI_[lang] not in fl10a) and (_GH_[lang] not in fl10a) and not _GF_[lang].search(fl10a),\n'
      '                             "rc_hms13_v410": _r210f, "frase_guarda_hms13_v410": bool(_GF_[lang].search(fl10f)), "so_a_guarda_do_hms13_quando_so_ele_falta": (_GI_[lang] not in fl10f) and (_GH_[lang] not in fl10f) and (_GA_[lang] not in fl10f),\n'
      '                             "frases_de_guarda_ausentes_no_texto_completo":')
troca('or v["frase_guarda_iald2_ausente_quando_so_o_h0dn_falta"] or not v["frases_de_guarda_ausentes_no_texto_completo"]]',
      'or v["frase_guarda_iald2_ausente_quando_so_o_h0dn_falta"] or not v["frases_de_guarda_ausentes_no_texto_completo"]\n'
      '           or not v["frase_guarda_aescala_quando_todos_faltam"] or not v["frase_guarda_hms13_quando_todos_faltam"] or not v["guardas_da_aescala_e_do_hms13_ausentes_quando_so_o_h0dn_falta"] or v["rc_a_escala_v410"] != [0] or not v["frase_guarda_a_escala_v410"] or not v["so_a_guarda_da_aescala_quando_so_ela_falta"]\n'
      '           or v["rc_hms13_v410"] != [0] or not v["frase_guarda_hms13_v410"] or not v["so_a_guarda_do_hms13_quando_so_ele_falta"]]   # (parte 2) as duas variantes novas e as guardas especificas')
# (9) o .md: as QUATRO linhas da v410 na ordem (IALD2 < A Escala < H0DN < Recibo HMS/13 < v409)
_MI = '"**IALD2 (v410, 06/11/2026):**"'; _MA = '"**A Escala (v410, 09/11/2026; D82 a D87):**"'; _MH = '"**H0DN × BG1 pré-registrado (v410, 09/11/2026):**"'; _MF = '"**Recibo documental HMS/13 (v410, 09/11/2026; D80):**"'; _MT = '"**Tradução às classes de Turing (v409, 05/11/2026):**"'
troca('"iald2_v410": ' + _MI + ' in md and md.find(' + _MI + ') < md.find(' + _MH + '), "h0dn_v410": ' + _MH + ' in md and md.find(' + _MH + ') < md.find(' + _MT + '),',
      '"iald2_v410": ' + _MI + ' in md and md.find(' + _MI + ') < md.find(' + _MA + '), "a_escala_v410": ' + _MA + ' in md and md.find(' + _MA + ') < md.find(' + _MH + '),\n'
      '                   "a_escala_v410_com_a_forma_da_d83_e_a_frase_canonica_na_linha": ((DL.FRASE_D83_OBRIGATORIA_PT in md.split(' + _MA + ', 1)[-1].split("' + BS + 'n", 1)[0]) and (DL.FRASE_CLAY_CANONICA_PT in md.split(' + _MA + ', 1)[-1].split("' + BS + 'n", 1)[0])) if ' + _MA + ' in md else False,\n'
      '                   "h0dn_v410": ' + _MH + ' in md and md.find(' + _MH + ') < md.find(' + _MF + '), "hms13_v410": ' + _MF + ' in md and md.find(' + _MF + ') < md.find(' + _MT + '),\n'
      '                   "hms13_v410_com_as_duas_obrigacoes_na_linha": ((DL.FRASE_HMS13_OBRIGATORIA_PT in md.split(' + _MF + ', 1)[-1].split("' + BS + 'n", 1)[0]) and (DL.FRASE_H0DN_OBRIGATORIA_PT in md.split(' + _MF + ', 1)[-1].split("' + BS + 'n", 1)[0])) if ' + _MF + ' in md else False,')
# (12) o exame: os pontos novos
troca('"ponto_h0dn": _ej.get("ponto_h0dn"),', '"ponto_h0dn": _ej.get("ponto_h0dn"), "ponto_aescala": _ej.get("ponto_aescala"), "ponto_hms13": _ej.get("ponto_hms13"),')
troca('and (_ej.get("ponto_h0dn") or {}).get("observed_vector_read") is False)',
      'and (_ej.get("ponto_h0dn") or {}).get("observed_vector_read") is False\n'
      '                and (_ej.get("ponto_aescala") or {}).get("all_verified") is True and (_ej.get("ponto_hms13") or {}).get("all_verified") is True and (_ej.get("ponto_hms13") or {}).get("observed_vector_read") is False and (_ej.get("ponto_hms13") or {}).get("le_em_rito") is False)   # (parte 2) os pontos de chamada reais do a_escala e do recibo HMS/13')
# (0, fim) o veto: o recibo HMS/13 tambem mediu
troca('"limite": "mede este processo',
      '"registro_hms13_tambem_mediu": {"n_caminhos_tocados": ((rep.get("h0dn_fontes_hms13_v410") or {}).get("values") or {}).get("n_caminhos_tocados"), "sob_pasta_vedada": ((rep.get("h0dn_fontes_hms13_v410") or {}).get("values") or {}).get("sob_pasta_vedada"), "com_nome_vedado": ((rep.get("h0dn_fontes_hms13_v410") or {}).get("values") or {}).get("com_nome_vedado")},\n'
      '                            "limite": "mede este processo')
nb = t.encode("utf-8"); compile(nb, P, "exec")
open(P + ".bak_" + TS + "_pre_parte2", "wb").write(b0)
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb) > len(b0); os.replace(P + ".tmp", P)
print("ensaio_a_seco_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16], "| trocas", N[0], "| linhas", nb.count(b"\n"))
# os titulos e subtitulos tipados TEM de estar nos snippets (a mesma conferencia que o ensaio faz ao rodar)
ns = {}
for ln in t.split("\n"):
    if ln.startswith(("TA410 = ", "DA410 = ", "DA410E = ", "DH410 = ", "DH410E = ", "TH410 = ")):
        exec(ln, ns)
for _l7, _t7, _d7, _sn_ in (("pt", ns["TH410"], ns["DH410"], "artigo_pt_h0dn_v410.pysnip"), ("en", ns["TH410E"], ns["DH410E"], "artigo_en_h0dn_v410.pysnip"), ("pt", ns["TA410"], ns["DA410"], "artigo_pt_aescala_v410.pysnip"), ("en", ns["TA410E"], ns["DA410E"], "artigo_en_aescala_v410.pysnip")):
    _sn7 = open(os.path.join(HERE, _sn_), encoding="utf-8").read()
    faltam = [h_ for h_ in _d7 if ("textbf{" + h_ + "}") not in _sn7]
    assert ("section*{" + _t7 + "}") in _sn7 and not faltam, ("o titulo/subtitulo nao esta no snippet", _l7, _sn_, faltam)
print("titulos e subtitulos novos conferidos nos quatro snippets")
