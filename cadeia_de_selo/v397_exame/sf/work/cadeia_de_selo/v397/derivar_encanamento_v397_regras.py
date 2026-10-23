# -*- coding: utf-8 -*-
# regras de derivar_encanamento_v397.py (exec no escopo dele: `entrada(src, dst=None, regras=[(antigo_depois_do_mapa, novo, contagem), ...])`)
# O MAPA muda 395 -> 396 e 396 -> 397 em todo o texto, MENOS nos identificadores protegidos (nomes nascidos no um.py); as regras abaixo corrigem o que o mapa nao pode saber: conteudo especifico da pedra
# (TestemunhaEstatica -> Token), o ponto de chamada novo (o registro de veracidade logo depois do bloco do V1, nao junto do psibit), quatro falas em vez de tres e datas.
# Arquivos escritos a mao (nao derivados): delta, registros, runtime_quadro, gerar_candidato, os .pysnip, conferir_citacoes, conferir_rito, gerar_esperados, ensaio_a_seco, gerar_estado, gerar_registro_mapa_prep,
# comparar, simular_arvore_do_nos, exame_pontos, p00_precondicoes e o pos_rito.

# ------------------------------------------------------------------------------------------- copiar_base (so' o mapa)
entrada("copiar_base_v396.py")

# ------------------------------------------------------------------------------------------- preparar_kernel
entrada("preparar_kernel_v396.py", regras=[
    ('"/XF", "TestemunhaEstatica*.bak_*", "TGLExt.lean.bak_*",', '"/XF", "Token*.bak_*", "TGLExt.lean.bak_*",', 1),
    ("Parte de C:\\\\t\\\\k397\\\\final (copia do tgl_kernel do Nos v396 com a pedra TestemunhaEstatica ja' compilada em .lake/build numa versao anterior do texto; sem a pasta probe\\\\ de rascunhos nem as sondas do construtor nem os .bak_ da pedra), e GERA",
     "Parte de C:\\\\t\\\\k396c\\\\final (o sandbox da v396, com a v396 compilada em .lake/build; sem a pasta probe\\\\ nem os .bak_ de backup), e GERA", 1),
    ("A pedra e' a fonte autoral (work\\\\testemunha_estatica_v396\\\\TestemunhaEstatica.lean; so' ajustes de docstring depois do exame independente, que a aprovou), copiada para o sandbox quando difere (o sha16 e' LIDO na hora da geracao).",
     "A pedra e' a fonte autoral (v397\\\\pedra\\\\Token.lean; o nome «token» e' do operador, 23/10/2026), copiada para o sandbox quando difere (o sha16 e' LIDO na hora da geracao).", 1),
    ("# a raiz e o Audit de partida do sandbox (copia de k397\\final) == os da v396 embutida == os do Nos", "# a raiz e o Audit de partida do sandbox (copia de k396c\\final) == os da v396 embutida == os do Nos", 1),
])

# ------------------------------------------------------------------------------------------- construir_kernel
entrada("construir_kernel_v396.sh", regras=[
    ("(C:\\t\\k397c\\final; nunca o do Nos nem C:\\t\\k397): um `lake build` INCREMENTAL (a pedra TestemunhaEstatica pode ja' estar compilada em .lake/build numa versao anterior do texto, e o Lake a recompila se a fonte mudou; muda a raiz TGLExt e o Audit)",
     "(C:\\t\\k397c\\final; nunca o do Nos nem C:\\t\\k396c): um `lake build` INCREMENTAL (a v396 ja' esta compilada em .lake/build e a pedra Token foi compilada sozinha antes; muda a raiz TGLExt e o Audit)", 1),
])

# ------------------------------------------------------------------------------------------- pos_build_kernel
entrada("pos_build_kernel_v396.py", regras=[
    ("linha Built/Replayed da pedra TestemunhaEstatica, da raiz e do Audit", "linha Built/Replayed da pedra Token, da raiz e do Audit", 1),
    ("a unica pedra do recibo e' TestemunhaEstatica, nao a LightNetStandardWedgeDataBGL", "a unica pedra do recibo e' Token, nao a LightNetStandardWedgeDataBGL", 1),
    ("linha Built/Replayed do modulo novo (TestemunhaEstatica), da raiz", "linha Built/Replayed do modulo novo (Token), da raiz", 1),
    ("o recibo v397 lista so' a pedra NOVA TestemunhaEstatica e a LightNetStandardWedgeDataBGL.lean", "o recibo v397 lista so' a pedra NOVA Token e a LightNetStandardWedgeDataBGL.lean", 1),
    ("o compilador a emite no modulo de Psibit (v396), nao no da pedra", "o compilador a emite no modulo de Psibit (v395), nao no da pedra", 1),
    ('DL.STONE_MOD, "testemunha_estatica_nomeada"]', 'DL.STONE_MOD, "token_nomeada"]', 1),
    ('"por_origem": {"testemunha_estatica_nomeada": len(flags_v397)}', '"por_origem": {"token_nomeada": len(flags_v397)}', 1),
    ('"por_grupo_bandeiras": {"testemunha_estatica": len(flags_v397)}', '"por_grupo_bandeiras": {"token": len(flags_v397)}', 1),
    ("(decisao da gerencia c1, 22/10/2026; a regra e' a da v394 e v396,", "(decisao da gerencia c1, 23/10/2026; a regra e' a da v394, v395 e v396,", 1),
    ("(preparacao, 22/10/2026); NAO conferido", "(preparacao, 23/10/2026); NAO conferido", 1),
])

# ------------------------------------------------------------------------------------------- comparar (AST): nada da v396 perdido
entrada("comparar_v395_v396.py", regras=[
    ('"_EMBEDDED_KERNEL_FILES": "K00/K01: +1 modulo (TGLExt/TestemunhaEstatica.lean) e a raiz TGLExt.lean e o TGL/Audit.lean com o import da pedra",', '"_EMBEDDED_KERNEL_FILES": "K00/K01: +1 modulo (TGLExt/Token.lean) e a raiz TGLExt.lean e o TGL/Audit.lean com o import da pedra",', 1),
    ("V01: +bandeiras so' de declaracao nomeada da pedra TestemunhaEstatica (FLAGS_v397.json)", "V01: +bandeiras so' de declaracao nomeada da pedra Token (FLAGS_v397.json)", 1),
    ('"_ESQUELETO_STONES": "V03: o ledger de pedras ganha a TestemunhaEstatica",', '"_ESQUELETO_STONES": "V03: o ledger de pedras ganha a Token",', 1),
    ('    "_V395_PSIBIT_CONTRACT": "C12: so\' o numero expected_ladder (o psibit_v395 exige a igualdade exata com a escada do rito)",\n    "_V395_SPECS": "C13: kh_n1_cobertura_v395 passa a piso em h2, h3, h6 e a tamanho minimo em h8 (+ errata assinada); os outros dois specs nao mudam",',
     '    "_V395_PSIBIT_CONTRACT": "C12: so\' o numero expected_ladder (o psibit_v395 exige a igualdade exata com a escada do rito)",\n    "_V396_TESTEMUNHA_CONTRACT": "C12: so\' o numero expected_ladder (a testemunha_estatica_v396 exige a igualdade exata com a escada do rito)",\n'
     '    "_V396_SPECS": "C13: kh_n1_cobertura_v396 passa a piso em h2, h3, h6 e a tamanho minimo em h8 (+ errata assinada); o outro spec nao muda",', 1),
    ('"main": "N00/N01/N02: a chamada de testemunha_estatica_v396 na fractalizacao do Um (logo depois do bloco psibit_v395), a chamada dos registros por spec da v397 e o selo (testemunha_estatica_v396, registros_v397)",',
     '"main": "N00/N01/N02: a chamada do registro teste_de_veracidade_fase9_v397 logo depois do bloco hubble_ratio_opening_v388 (ao lado do V1), a chamada dos registros por spec da v397 e o selo (teste_de_veracidade_fase9_v397, registros_v397)",', 1),
    ('"build_pt": "W04: a secao v397 do artigo PT, antes da v396",', '"build_pt": "W04/W06: a secao v397 do artigo PT, antes da v396, e o quadro «O Teste da Unica Palavra» logo abaixo do titulo",', 1),
    ('"build_en": "W05: a secao v397 do artigo EN, antes da v396",', '"build_en": "W05/W07: a secao v397 do artigo EN, antes da v396, e o quadro «The Test of the Only Word» logo abaixo do titulo",', 1),
    ('"emit_canonical_md": "W07: a linha da v397 no .md canonico",', '"emit_canonical_md": "W08/W09: o quadro do Teste da Unica Palavra no topo do .md canonico e a linha da v397",', 1),
])

# ------------------------------------------------------------------------------------------- simular_arvore_do_nos
entrada("simular_arvore_do_nos_v396.py", regras=[
    ("roda o indice, o psibit_v395, a testemunha_estatica_v396 e os registros por spec\nv394, v396 e v397 sobre esse kf. Molde: simular_arvore_do_nos_v396.py.",
     "roda o indice, o psibit_v395, a testemunha_estatica_v396, o teste_de_veracidade_fase9_v397 (spec do V2 da Fase 9, lido por hash) e os registros por spec\nv394, v395, v396 e v397 sobre esse kf. Molde: simular_arvore_do_nos_v396.py.", 1),
    ("um._v394_rodar_specs(core); um._v395_rodar_specs(core); um._v396_rodar_specs(core)\n",
     "um._v394_rodar_specs(core); um._v395_rodar_specs(core); um._v396_rodar_specs(core)\ncore[\"teste_de_veracidade_fase9_v397\"] = um._v392_registro(um._V397_VERACIDADE_SPEC, core); um._v397_rodar_specs(core)   # (v397: o spec de veracidade roda no ponto do V1 no main; aqui, antes dos specs que o leem)\n", 1),
    ('for k in ("testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "psibit_v395",', 'for k in ("teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "psibit_v395",', 1),
])

# ------------------------------------------------------------------------------------------- exame_pontos
_VER_BLOCO = r'''# (4a') o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397 (v397): a instrucao do main (um `try` + o `print` [v397]) que vem IMEDIATAMENTE depois do bloco do V1 (hubble_ratio_opening_v388), depois do psibit e da testemunha e antes do bloco da v393
iv = [i for i, s_ in enumerate(unp) if 'core["teste_de_veracidade_fase9_v397"] = _v392_registro(_V397_VERACIDADE_SPEC, core)' in s_ or "core['teste_de_veracidade_fase9_v397'] = _v392_registro(_V397_VERACIDADE_SPEC, core)" in s_]
assert len(iv) == 1, ("a instrucao do main que chama o registro de veracidade nao e' unica", len(iv))
iv = iv[0]
assert "[v388]" in unp[iv - 1] and "hubble_ratio_opening_v388" in unp[iv - 1], ("o registro de veracidade nao vem logo depois do print do bloco do V1 (hubble_ratio_opening_v388)", unp[iv - 1][:160])
assert "[v397]" in unp[iv + 1] and "teste_de_veracidade_fase9_v397" in unp[iv + 1], ("a instrucao seguinte nao e' o print do registro de veracidade", unp[iv + 1][:160])
R["ponto_veracidade"] = {"indice_no_main": iv, "linha": main.body[iv].lineno, "depois_do_psibit_e_da_testemunha": iv > ipt, "antes_do_bloco_v393": iv < i0, "instrucao_anterior": unp[iv - 1][:160].replace("\n", " | ")}
builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[iv], main.body[iv + 1]], type_ignores=[])), "<main:teste_de_veracidade_fase9_v397>", "exec"), g); errv = None
except Exception as e:
    import traceback; errv = repr(e) + traceback.format_exc()[-900:]
finally:
    stdout_ver = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
tv = core.get("teste_de_veracidade_fase9_v397") or {}
res9 = json.load(open(os.path.join(H, "insumos", "fase9", "RESULTADO_FASE9_V2_C1_20261023_122926.json"), encoding="utf-8"))   # a copia duravel, byte a byte do resultado pinado
lidos9 = tv.get("lido") or {}
num9 = {k_: (lidos9.get(k_) == DL.lido(res9, c_)) for k_, c_ in DL.F9_CAMINHOS.items()}
R["ponto_veracidade"].update({"erro": errv, "avisos": [l for l in stdout_ver.splitlines() if "AVISO" in l], "stdout": stdout_ver.splitlines(), "verdict": tv.get("verdict"), "all_verified": tv.get("all_verified"), "n_checks": len(tv.get("checks") or []),
                              "checks_falhos": [c_.get("descricao") for c_ in (tv.get("checks") or []) if not c_.get("ok")], "numeros_lidos_iguais_ao_resultado_pinado": num9, "fontes_ok": [f_["ok"] for f_ in (tv.get("fontes") or [])]})
out["core.teste_de_veracidade_fase9_v397"] = {"all_verified": tv.get("all_verified"), "verdict": str(tv.get("verdict"))[:300], "falhas": falhas_de(tv)}
'''
_VER_FALSO = r'''pv = R["ponto_veracidade"]
if (pv.get("erro") or pv.get("avisos") or pv.get("all_verified") is not True or not pv.get("depois_do_psibit_e_da_testemunha") or not pv.get("antes_do_bloco_v393")
        or not all((pv.get("numeros_lidos_iguais_ao_resultado_pinado") or {False: False}).values()) or not all(pv.get("fontes_ok") or [False])): falsos.append("ponto_veracidade")
'''
entrada("exame_pontos_v396.py", regras=[
    ("logo_depois_do_psibit_v396", "logo_depois_do_psibit_v395", 2),
    # docstring
    ("achadas por\n     ast e conferida como a que vem logo depois do principio da defasagem fractal, na fractalizacao do Um) e, em seguida, TODAS",
     "achadas por\n     ast e conferida como a que vem logo depois do principio da defasagem fractal, na fractalizacao do Um), DEPOIS o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397 (a instrucao do main logo depois do bloco do V1, hubble_ratio_opening_v388; os numeros\n     lidos conferidos contra o resultado pinado) e, em seguida, TODAS", 1),
    # o fluxo recria tambem os registros da v396 (o core0 e' a v396 SELADA)
    ('["psibit_v395"] + list(um._V395_NOMES_REGISTROS):\n    core.pop(n_, None)   # o fluxo os recria', '["psibit_v395"] + list(um._V395_NOMES_REGISTROS) + ["testemunha_estatica_v396"] + list(um._V396_NOMES_REGISTROS):\n    core.pop(n_, None)   # o fluxo os recria', 1),
    # o ponto novo
    ("# (4b) as instrucoes do main da v393 em diante (ate emit_figures), executadas como estao no candidato\n", _VER_BLOCO + "# (4b) as instrucoes do main da v393 em diante (ate emit_figures), executadas como estao no candidato\n", 1),
    ('"v396": [k for k in ["psibit_v395"] + list(um._V395_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n',   # (o mapa subiu o ROTULO "v395" para "v396": volta e acrescenta o novo)
     '"v395": [k for k in ["psibit_v395"] + list(um._V395_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n                   "v396": [k for k in ["testemunha_estatica_v396"] + list(um._V396_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n', 1),
    ('"testemunha_estatica_v396": {x: (seal.get("testemunha_estatica_v396") or {}).get(x) for x in ("verdict", "all_verified")}}',
     '"testemunha_estatica_v396": {x: (seal.get("testemunha_estatica_v396") or {}).get(x) for x in ("verdict", "all_verified")},\n                 "teste_de_veracidade_fase9_v397": {x: (seal.get("teste_de_veracidade_fase9_v397") or {}).get(x) for x in ("verdict", "all_verified")},\n'
     '                 "registros_v397": {n_: ((seal.get("registros_v397") or {}).get(n_) or {}).get("all_verified") for n_ in um._V397_NOMES_REGISTROS}}', 1),
    ('if R["main_bloco_executado"]["erro"] or R["main_bloco_executado"]["avisos"]: falsos.append("main_bloco")\n', _VER_FALSO + 'if R["main_bloco_executado"]["erro"] or R["main_bloco_executado"]["avisos"]: falsos.append("main_bloco")\n', 1),
])

# ------------------------------------------------------------------------------------------- p00_precondicoes (as strings a casar sao o ORIGINAL v396 passado por bump(): robusto ao mapa)
entrada("p00_precondicoes_v396.py", regras=[
    (bump('for n in ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit")))'), 'for n in ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica")))', 1),
    (bump("as pedras da v394 e da v395 estao"), "as pedras da v394, v395 e v396 estao", 1),
    (bump('chk("as tres cunhagens de 22/10: arquivo duravel == sha256 == fonte original", len([k for k in MI if k.startswith("cunhagens/")]) == 3'), 'chk("as quatro cunhagens de 23/10: arquivo duravel == sha256 == fonte original", len([k for k in MI if k.startswith("cunhagens/")]) == 4', 1),
    (bump('sim["testemunha_estatica_v396"]["all_verified"] is True and sim["psibit_v395"]["all_verified"] is True and sim["kf_all_verified"] is True,'),
     'sim["testemunha_estatica_v396"]["all_verified"] is True and sim["psibit_v395"]["all_verified"] is True and sim["teste_de_veracidade_fase9_v397"]["all_verified"] is True and sim["cunhagens_v397"]["all_verified"] is True and sim["kf_all_verified"] is True,', 1),
    (bump('exm["ponto_testemunha"]["logo_depois_do_psibit_v395"] is True, exm.get("algum_falso"))'),
     'exm["ponto_testemunha"]["logo_depois_do_psibit_v395"] is True and exm["ponto_veracidade"]["all_verified"] is True and exm["ponto_veracidade"]["depois_do_psibit_e_da_testemunha"] is True and exm["ponto_veracidade"]["antes_do_bloco_v393"] is True and all(exm["ponto_veracidade"]["numeros_lidos_iguais_ao_resultado_pinado"].values()), exm.get("algum_falso"))', 1),
    (bump("o do psibit_v395 vem logo depois do principio da defasagem fractal e o da testemunha_estatica_v396 logo depois do psibit_v395)"), "o do psibit_v395 vem logo depois do principio da defasagem fractal, o da testemunha_estatica_v396 logo depois do psibit_v395 e o do teste_de_veracidade_fase9_v397 logo depois do bloco do V1)", 1),
    (bump('"runtime_testemunha_v396.py"'), '"runtime_quadro_v397.py"', 1),
    (bump('"guarda_p18_v396.py"):'), '"guarda_p18_v397.py", "derivar_encanamento_v397.py", "derivar_encanamento_v397_regras.py", "derivar_encanamento_v397_regras_B.py", "quadro_v397.py"):', 1),
    (bump('prova = json.load(open(os.path.join(HERE, "PROVA_PRODUCAO_INTACTA_v396_pre_selo.json"), encoding="utf-8"))\n'),
     'prova = json.load(open(os.path.join(HERE, "PROVA_PRODUCAO_INTACTA_v397_pre_selo.json"), encoding="utf-8"))\n'
     'F9 = DL.f9_fontes(os.path.join(HERE, "insumos", "fase9"))\n'
     'chk("o Teste da Unica Palavra: o resultado e os tres recibos (copias duraveis em insumos\\\\fase9) == as origens (sha256, pasta fase9_v2_c1_23out so\' leitura); o resultado == o sha256 que a ordem da gerencia deu; as QUATRO falas de 23/10 tem os prefixos de sha256 da ordem",\n'
     '    all(sha(rd(f["arquivo"])) == f["sha256"] == sha(rd(f["origem"])) for f in F9) and F9[0]["sha256"] == DL.F9_RESULTADO_SHA256_DA_ORDEM and len(DL.verbatins(os.path.join(HERE, "insumos", "cunhagens"))) == 4, [f["sha256"][:16] for f in F9])\n', 1),
    (bump('chk("o ensaio a seco e\' deste candidato e deu TUDO PASSOU (e o ESPERADOS pina o ensaio)", ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"]'),
     'chk("o ensaio a seco e\' deste candidato e deu TUDO PASSOU (e o ESPERADOS pina o ensaio); o QUADRO do Teste da Unica Palavra esta no topo do artigo PT/EN e do .md e os numeros do quadro == os do resultado pinado", ens["veredito"] == "TUDO PASSOU" and ens["quadro"]["ok"] is True and ens["sha16"] == CM["sha16"]', 1),
])
