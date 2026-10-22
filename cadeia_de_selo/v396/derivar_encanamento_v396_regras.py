# -*- coding: utf-8 -*-
# regras de derivar_encanamento_v396.py (exec no escopo dele: `entrada(src, dst=None, regras=[(antigo_depois_do_mapa, novo, contagem), ...])`)
# O MAPA muda 394 -> 395 e 395 -> 396 em TODO o texto; as regras abaixo corrigem o que o mapa nao pode saber: nomes de objetos que moram no um.py base com o nome da versao em que nasceram
# (parse_lean_*_v394, declaration_sources_v394, F1Fecho394, ...), conteudo especifico da pedra (Psibit -> TestemunhaEstatica) e datas.
# Arquivos escritos a mao (nao derivados): delta, registros, runtime, gerar_candidato, conferir_citacoes, conferir_rito, gerar_esperados, ensaio_a_seco, gerar_estado, gerar_registro_mapa_prep, os .pysnip e o pos_rito.

# ------------------------------------------------------------------------------------------- copiar_base (so' o mapa)
entrada("copiar_base_v395.py")

# ------------------------------------------------------------------------------------------- preparar_kernel
entrada("preparar_kernel_v395.py", regras=[
    (r"com a pedra Psibit ja' compilada em .lake/build; sem a pasta probe\\ de rascunhos nem os .bak_ da pedra)", r"com a pedra TestemunhaEstatica ja' compilada em .lake/build numa versao anterior do texto; sem a pasta probe\\ de rascunhos nem as sondas do construtor nem os .bak_ da pedra)", 1),
    (r"A pedra e' a fonte autoral (work\\psibit_v396\\Psibit.lean; 2a versao," + "\n" + "aprovada na rodada 2 do exame independente), conferida byte a byte contra a do sandbox de origem.",
     r"A pedra e' a fonte autoral (work\\testemunha_estatica_v396\\TestemunhaEstatica.lean; so' ajustes de docstring depois do exame independente, que a aprovou), copiada para o sandbox quando difere (o sha16 e' LIDO na hora da geracao).", 1),
    ('"/XF", "Psibit.lean.bak_*", "TGLExt.lean.bak_*",', '"/XF", "TestemunhaEstatica*.bak_*", "TGLExt.lean.bak_*",', 1),
])

# ------------------------------------------------------------------------------------------- construir_kernel
entrada("construir_kernel_v395.sh", regras=[
    ("(a pedra Psibit ja' estava compilada em .lake/build; muda a raiz TGLExt e o Audit)", "(a pedra TestemunhaEstatica pode ja' estar compilada em .lake/build numa versao anterior do texto, e o Lake a recompila se a fonte mudou; muda a raiz TGLExt e o Audit)", 1),
])

# ------------------------------------------------------------------------------------------- pos_build_kernel
entrada("pos_build_kernel_v395.py", regras=[
    # os leitores do Audit moram no um.py base com o nome da versao em que nasceram (v394): NAO sobem
    ("parse_lean_axioms_v395", "parse_lean_axioms_v394", 4),
    ("parse_lean_provenance_v395", "parse_lean_provenance_v394", 4),
    ('"nao_lidas_pelo_leitor_v395": 0', '"nao_lidas_pelo_leitor_v394": 0', 1),
    # docstring e rotulos da pedra
    ("linha Built/Replayed da pedra Psibit, da raiz e do Audit", "linha Built/Replayed da pedra TestemunhaEstatica, da raiz e do Audit", 1),
    ("(x19 = 'nao': a unica pedra do recibo e' Psibit, nao a LightNetStandardWedgeDataBGL)", "(x19 = 'nao': a unica pedra do recibo e' TestemunhaEstatica, nao a LightNetStandardWedgeDataBGL)", 1),
    ("linha Built/Replayed do modulo novo (Psibit), da raiz (TGLExt) e do Audit (TGL.Audit)", "linha Built/Replayed do modulo novo (TestemunhaEstatica), da raiz (TGLExt) e do Audit (TGL.Audit)", 1),
    # a pedra v396 nao tem teorema condicional (a face de Fock mora em Psibit.lean); o registro CONFERE que ela segue la
    ('chk("os dois teoremas do registro (incondicional e condicional) estao no Audit, no modulo da pedra, nomeados, no trio", all(t in nomeadas and set(axm[t]) <= TRIO for t in (DL.THEOREM, DL.THEOREM_COND)), [t for t in (DL.THEOREM, DL.THEOREM_COND) if t not in nomeadas])',
     'chk("o teorema do registro (a composicao incondicional) esta no Audit, no modulo da pedra, nomeado, no trio", DL.THEOREM in nomeadas and set(axm[DL.THEOREM]) <= TRIO, [t for t in (DL.THEOREM,) if t not in nomeadas])\n'
     'chk("a face de Fock do psion NAO esta nesta pedra: o compilador a emite no modulo de Psibit (v395), nao no da pedra; e os %d termos de suporte (kernel antigo) estao no Audit, no trio" % len(DL.SUPPORT_THEOREMS),\n'
     '    srcm.get(DL.FOCK_FACE_THEOREM) == DL.FOCK_FACE_PATH and DL.FOCK_FACE_THEOREM not in nomeadas and all(t in axm and set(axm[t]) <= TRIO and t in srcm for t in DL.SUPPORT_THEOREMS), [srcm.get(DL.FOCK_FACE_THEOREM), [t for t in DL.SUPPORT_THEOREMS if t not in axm][:3]])', 1),
    ('chk("o teorema incondicional e o condicional dependem so\' do trio (conferido por inclusao)", set(axm[DL.THEOREM]) <= TRIO and set(axm[DL.THEOREM_COND]) <= TRIO, [axm[DL.THEOREM], axm[DL.THEOREM_COND]])',
     'chk("o teorema incondicional depende so\' do trio (conferido por inclusao)", set(axm[DL.THEOREM]) <= TRIO, [axm[DL.THEOREM]])', 1),
    ('"psibit_nomeada"] for i, n in enumerate(nomeadas)]', '"testemunha_estatica_nomeada"] for i, n in enumerate(nomeadas)]', 1),
    ("(a pratica selada da v392, v393 e v395)", "(a pratica selada da v392, v393, v394 e v395)", 1),
    ("(decisao da gerencia c1, 21/10/2026; a regra e' a da v395, os numeros saem do Audit desta geracao)", "(decisao da gerencia c1, 22/10/2026; a regra e' a da v394 e v395, os numeros saem do Audit desta geracao)", 1),
    ('"por_origem": {"psibit_nomeada": len(flags_v396)},', '"por_origem": {"testemunha_estatica_nomeada": len(flags_v396)},', 1),
    ('"por_grupo_bandeiras": {"psibit": len(flags_v396)},', '"por_grupo_bandeiras": {"testemunha_estatica": len(flags_v396)},', 1),
    ('"bandeira_do_teorema_incondicional": chave_de[DL.THEOREM], "bandeira_do_teorema_condicional": chave_de[DL.THEOREM_COND],',
     '"bandeira_do_teorema_incondicional": chave_de[DL.THEOREM], "suporte_do_contrato": {t: srcm[t] for t in DL.SUPPORT_THEOREMS}, "fock_face_declarada_em": srcm[DL.FOCK_FACE_THEOREM],', 1),
    # ACHADO MEDIDO (22/10): a proveniencia do compilador atribui a pedra 70 declaracoes, mas so' 69 sao NOVAS (TOTAL 29.228 - 29.159): o Lean gera TGLExt.diagFlow.eq_1 (auxiliar eq_1, ja' no axiom_report da v395, antes atribuida a
    # TGLExt/TheGreatAttractor.lean) tambem no modulo da pedra, e na ordem de import do Audit a proveniencia dela passa a ser a da pedra. A checagem separa as NOVAS das REATRIBUIDAS e exige que as reatribuidas sejam auxiliares sem bandeira.
    ('chk("declaracoes do modulo novo (publicas + privadas), por proveniencia == TOTAL(v396) - TOTAL(v395)", len(novas_todas) == kh_cov[0] - int(cov395.get("decl", -1)), [len(novas_todas), kh_cov[0], cov395.get("decl")])',
     'reatribuidas = {n: {"antes": (core395["kernel_formalization"].get("declaration_sources_v394") or {}).get(n), "agora": srcm[n]} for n in sorted(novas_todas) if n in axr395}   # ja\' no axiom_report da v395 e agora atribuidas a pedra pela proveniencia (o Lean gera a auxiliar eq_1 de TGLExt.diagFlow tambem nela)\n'
     'novas_reais = [n for n in novas_todas if n not in axr395]\n'
     'chk("declaracoes NOVAS do modulo novo (publicas + privadas, por proveniencia, menos as reatribuidas) == TOTAL(v396) - TOTAL(v395); as reatribuidas sao auxiliares (sem bandeira)", len(novas_reais) == kh_cov[0] - int(cov395.get("decl", -1)) and all(DL.classe(n) != "nomeada" for n in reatribuidas), [len(novas_reais), kh_cov[0], cov395.get("decl"), reatribuidas])', 1),
    ('"publicas_no_modulo": len(pub), "privadas_no_modulo": len(priv), "decl_totais_modulo_novo": len(novas_todas),', '"publicas_no_modulo": len(pub), "privadas_no_modulo": len(priv), "decl_totais_modulo_novo": len(novas_todas), "decl_novas_do_modulo": len(novas_reais), "reatribuidas_a_pedra": reatribuidas,', 1),
    ('"decl_do_modulo_novo": len(novas_todas)', '"decl_do_modulo_novo": len(novas_todas), "decl_novas_do_modulo": len(novas_reais), "reatribuidas_a_pedra": reatribuidas', 1),
    ("(preparacao, 21/10/2026)", "(preparacao, 22/10/2026)", 1),
    ("(a pedra ja' estava compilada em C:/t/k396/final; o rito real do Nos compila a frio)", "(a pedra pode ja' estar compilada em C:/t/k396/final numa versao anterior do texto; o rito real do Nos compila a frio)", 1),
    ("como na v393/v395). x19='nao': o recibo v396 lista so' a pedra NOVA Psibit e", "como na v393, v394 e v395). x19='nao': o recibo v396 lista so' a pedra NOVA TestemunhaEstatica e", 1),
])

# ------------------------------------------------------------------------------------------- guarda P18 (identica; so' o mapa e o nome)
entrada("guarda_p18_v395.py")

# ------------------------------------------------------------------------------------------- refazer_* (sandbox, arvore pos-selo, candidato)
entrada("refazer_arvore_v395_pos_selo.py", regras=[("Escrito em 21/10/2026", "Escrito em 22/10/2026", 1)])
entrada("refazer_sandbox_v395.sh", regras=[
    ("acrescenta a pedra Psibit e GERA", "acrescenta a pedra TestemunhaEstatica e GERA", 1),
])
entrada("refazer_sandbox_v395_pos_selo.sh")
entrada("refazer_candidato_v395.sh", regras=[("runtime_psibit_v396.py", "runtime_testemunha_v396.py", 1)])

# ------------------------------------------------------------------------------------------- comparar (AST): nada da v395 perdido
entrada("comparar_v394_v395.py", regras=[
    ('"_EMBEDDED_KERNEL_FILES": "K00/K01: +1 modulo (TGLExt/Psibit.lean) e a raiz TGLExt.lean e o TGL/Audit.lean com o import da pedra",', '"_EMBEDDED_KERNEL_FILES": "K00/K01: +1 modulo (TGLExt/TestemunhaEstatica.lean) e a raiz TGLExt.lean e o TGL/Audit.lean com o import da pedra",', 1),
    ("V01: +bandeiras so' de declaracao nomeada da pedra Psibit (FLAGS_v396.json)", "V01: +bandeiras so' de declaracao nomeada da pedra TestemunhaEstatica (FLAGS_v396.json)", 1),
    ('"_ESQUELETO_STONES": "V03: o ledger de pedras ganha a Psibit",', '"_ESQUELETO_STONES": "V03: o ledger de pedras ganha a TestemunhaEstatica",', 1),
    ('"_V395_FORMAL_CONTRACT": ', '"_V394_FORMAL_CONTRACT": ', 1), ('"_V395_QUADRATIC_CONTRACT": ', '"_V394_QUADRATIC_CONTRACT": ', 1), ('"_V395_NETWORK_CONTRACT": ', '"_V394_NETWORK_CONTRACT": ', 1),
    ('    "_V395_SPECS": ', '    "_V395_PSIBIT_CONTRACT": "C12: so\' o numero expected_ladder (o psibit_v395 exige a igualdade exata com a escada do rito)",\n    "_V395_SPECS": ', 1),
    ("N00/N01/N02: a chamada de psibit_v396 na fractalizacao do Um, a chamada dos registros por spec da v396 e o selo (psibit_v396, registros_v396)", "N00/N01/N02: a chamada de testemunha_estatica_v396 na fractalizacao do Um (logo depois do bloco psibit_v395), a chamada dos registros por spec da v396 e o selo (testemunha_estatica_v396, registros_v396)", 1),
])

# ------------------------------------------------------------------------------------------- simular_arvore_do_nos
entrada("simular_arvore_do_nos_v395.py", regras=[
    ("roda o indice, o psibit_v396 e os registros por spec\nv395 e v396 sobre esse kf. Molde: simular_arvore_do_nos.py (v395_exame).", "roda o indice, o psibit_v395, a testemunha_estatica_v396 e os registros por spec\nv394, v395 e v396 sobre esse kf. Molde: simular_arvore_do_nos_v395.py.", 1),
    ("um.psibit_v396(core)   # (na fractalizacao do Um, no main; aqui o kf ja' e' o da arvore simulada do Nos)", "um.psibit_v395(core); um.testemunha_estatica_v396(core)   # (na fractalizacao do Um, no main; aqui o kf ja' e' o da arvore simulada do Nos)", 1),
    ("um.tempo_frequencia_v395(core); um.regra_quadratica_v395(core); um.rede_fock_v395(core); um._v395_rodar_specs(core); um._v396_rodar_specs(core)", "um.tempo_frequencia_v394(core); um.regra_quadratica_v394(core); um.rede_fock_v394(core); um._v394_rodar_specs(core); um._v395_rodar_specs(core); um._v396_rodar_specs(core)", 1),
    ('for k in ("psibit_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "tempo_frequencia_v395", "regra_quadratica_v395", "rede_fock_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "criterio_binario_de_parada_v395"):',
     'for k in ("testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394"):', 1),
])

# ------------------------------------------------------------------------------------------- exame_pontos
entrada("exame_pontos_v395.py", regras=[
    ("declaration_sources_status_v395", "declaration_sources_status_v394", 3),
    ("DEPOIS o PONTO DE CHAMADA REAL do psibit_v396 (a instrucao do main que o chama, achada por", "DEPOIS o PONTO DE CHAMADA REAL do psibit_v395 e da testemunha_estatica_v396 (as instrucoes do main que os chamam, achadas por", 1),
    ('ipb = [i for i, s_ in enumerate(unp) if "psibit_v396(core)" in s_]\nassert len(ipb) == 1, ("a instrucao do main que chama psibit_v396 nao e\' unica", len(ipb))\nipb = ipb[0]\n',
     'ipb = [i for i, s_ in enumerate(unp) if "psibit_v395(core)" in s_]\nassert len(ipb) == 1, ("a instrucao do main que chama psibit_v395 nao e\' unica", len(ipb))\nipb = ipb[0]\n'
     'ipt = [i for i, s_ in enumerate(unp) if "testemunha_estatica_v396(core)" in s_]\nassert len(ipt) == 1 and ipt[0] == ipb + 1, ("a instrucao do main que chama testemunha_estatica_v396 nao e\' unica ou nao vem IMEDIATAMENTE depois da do psibit_v395", ipt, ipb)\nipt = ipt[0]\n', 1),
    ('R["ponto_psibit"] = {"indice_no_main": ipb, "linha": main.body[ipb].lineno, "antes_do_bloco_v393": ipb < i0, "logo_depois_do_principio_da_defasagem_fractal": bool(fd_antes), "instrucao_anterior": unp[ipb - 1][:160].replace("\\n", " | ")}\n',
     'R["ponto_psibit"] = {"indice_no_main": ipb, "linha": main.body[ipb].lineno, "antes_do_bloco_v393": ipb < i0, "logo_depois_do_principio_da_defasagem_fractal": bool(fd_antes), "instrucao_anterior": unp[ipb - 1][:160].replace("\\n", " | ")}\n'
     'R["ponto_testemunha"] = {"indice_no_main": ipt, "linha": main.body[ipt].lineno, "antes_do_bloco_v393": ipt < i0, "logo_depois_do_psibit_v395": "psibit_v395(core)" in unp[ipt - 1], "instrucao_anterior": unp[ipt - 1][:160].replace("\\n", " | ")}\n', 1),
    ('["tempo_frequencia_v395", "regra_quadratica_v395", "rede_fock_v395"] + list(um._V395_NOMES_REGISTROS):\n    core.pop(n_, None)',
     '["tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394"] + list(um._V394_NOMES_REGISTROS) + ["psibit_v395"] + list(um._V395_NOMES_REGISTROS):\n    core.pop(n_, None)', 1),
    ("# (4a) o PONTO DE CHAMADA REAL do psibit_v396 (a instrucao do main, como esta' no candidato)", "# (4a) os PONTOS DE CHAMADA REAIS do psibit_v395 e da testemunha_estatica_v396 (as duas instrucoes do main, em ordem, como estao no candidato)", 1),
    ('body=[main.body[ipb]], type_ignores=[])), "<main:psibit_v396>", "exec"), g); errp = None', 'body=[main.body[ipb], main.body[ipt]], type_ignores=[])), "<main:psibit_v395+testemunha_estatica_v396>", "exec"), g); errp = None', 1),
    ('pb = core.get("psibit_v396") or {}\nR["ponto_psibit"].update({"erro": errp, "stdout": stdout_psb.splitlines(), "avisos": [l for l in stdout_psb.splitlines() if "AVISO" in l], "verdict": pb.get("verdict"), "all_verified": pb.get("all_verified"),\n'
     '                          "mecanica": {"passed": (pb.get("mechanics") or {}).get("passed"), "n_checks": (pb.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (pb.get("unconditional") or {}).get("in_kernel"),\n'
     '                          "conditional_status": (pb.get("conditional_psion_face") or {}).get("status")})\n'
     'out["core.psibit_v396"] = {"all_verified": pb.get("all_verified"), "verdict": str(pb.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((pb.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}\n',
     'pb = core.get("psibit_v395") or {}; tb = core.get("testemunha_estatica_v396") or {}\n'
     'R["ponto_psibit"].update({"erro": errp, "stdout": stdout_psb.splitlines(), "avisos": [l for l in stdout_psb.splitlines() if "AVISO" in l], "verdict": pb.get("verdict"), "all_verified": pb.get("all_verified"),\n'
     '                          "mecanica": {"passed": (pb.get("mechanics") or {}).get("passed"), "n_checks": (pb.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (pb.get("unconditional") or {}).get("in_kernel"),\n'
     '                          "conditional_status": (pb.get("conditional_psion_face") or {}).get("status")})\n'
     'R["ponto_testemunha"].update({"erro": errp, "avisos": [l for l in stdout_psb.splitlines() if "AVISO" in l], "verdict": tb.get("verdict"), "all_verified": tb.get("all_verified"),\n'
     '                              "mecanica": {"passed": (tb.get("mechanics") or {}).get("passed"), "n_checks": (tb.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (tb.get("unconditional") or {}).get("in_kernel"),\n'
     '                              "fock_status": (tb.get("fock_face") or {}).get("status"), "fock_fora_da_pedra": (tb.get("fock_face") or {}).get("declared_outside_the_stone")})\n'
     'out["core.psibit_v395"] = {"all_verified": pb.get("all_verified"), "verdict": str(pb.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((pb.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}\n'
     'out["core.testemunha_estatica_v396"] = {"all_verified": tb.get("all_verified"), "verdict": str(tb.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((tb.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}\n', 1),
    ('                   "v395": [k for k in ["tempo_frequencia_v395", "regra_quadratica_v395", "rede_fock_v395"] + list(um._V395_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n',
     '                   "v394": [k for k in ["tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394"] + list(um._V394_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n'
     '                   "v395": [k for k in ["psibit_v395"] + list(um._V395_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n', 1),
    ('"psibit_v396": {x: (seal.get("psibit_v396") or {}).get(x) for x in ("verdict", "all_verified")}}', '"psibit_v395": {x: (seal.get("psibit_v395") or {}).get(x) for x in ("verdict", "all_verified")}, "testemunha_estatica_v396": {x: (seal.get("testemunha_estatica_v396") or {}).get(x) for x in ("verdict", "all_verified")}}', 1),
    ('if pp.get("erro") or pp.get("avisos") or pp.get("all_verified") is not True or not pp.get("antes_do_bloco_v393") or not pp.get("logo_depois_do_principio_da_defasagem_fractal"): falsos.append("ponto_psibit")\n',
     'if pp.get("erro") or pp.get("avisos") or pp.get("all_verified") is not True or not pp.get("antes_do_bloco_v393") or not pp.get("logo_depois_do_principio_da_defasagem_fractal"): falsos.append("ponto_psibit")\n'
     'pt = R["ponto_testemunha"]\n'
     'if pt.get("erro") or pt.get("avisos") or pt.get("all_verified") is not True or not pt.get("antes_do_bloco_v393") or not pt.get("logo_depois_do_psibit_v395") or pt.get("fock_status") != "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE" or pt.get("fock_fora_da_pedra") is not True: falsos.append("ponto_testemunha")\n', 1),
])

# ------------------------------------------------------------------------------------------- diff_e_pinos
entrada("diff_e_pinos_v395.py", regras=[
    ("os vereditos esperados do passo simples (REPINADA_B5__...)", "os vereditos esperados do passo simples (REPINADA_B6__...)", 1),
])

# ------------------------------------------------------------------------------------------- p00_precondicoes
entrada("p00_precondicoes_v395.py", regras=[
    ('and sim["psibit_v396"]["all_verified"] is True and sim["kf_all_verified"] is True,', 'and sim["testemunha_estatica_v396"]["all_verified"] is True and sim["psibit_v395"]["all_verified"] is True and sim["kf_all_verified"] is True,', 1),
    ("nenhum ponto de chamada real da falso (o do psibit_v396 vem logo depois do principio da defasagem fractal)", "nenhum ponto de chamada real da falso (o do psibit_v395 vem logo depois do principio da defasagem fractal e o da testemunha_estatica_v396 logo depois do psibit_v395)", 1),
    ('exm["ponto_psibit"]["logo_depois_do_principio_da_defasagem_fractal"] is True,', 'exm["ponto_psibit"]["logo_depois_do_principio_da_defasagem_fractal"] is True and exm["ponto_testemunha"]["logo_depois_do_psibit_v395"] is True,', 1),
    ('chk("as quatro cunhagens de 21/10: arquivo duravel == sha256 == fonte original", len([k for k in MI if k.startswith("cunhagens/")]) == 4', 'chk("as tres cunhagens de 22/10: arquivo duravel == sha256 == fonte original", len([k for k in MI if k.startswith("cunhagens/")]) == 3', 1),
    ('"o modulo novo (%d, lido da lista) NAO esta no kernel do Nos; as pedras da v395 estao" % len(nov)', '"o modulo novo (%d, lido da lista) NAO esta no kernel do Nos; as pedras da v394 e da v395 estao" % len(nov)', 1),
    ('for n in ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual")))', 'for n in ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit")))', 1),
    ('"runtime_psibit_v396.py"', '"runtime_testemunha_v396.py"', 1),
])

# ------------------------------------------------------------------------------------------- instalar / reverter / regras
entrada("instalar_v395.py", regras=[
    ("escrito em 21/10/2026, NAO executado na preparacao", "escrito em 22/10/2026, NAO executado na preparacao", 1),
    ("# v396: (a) as pedras da v395 (o criterio binario, a rede de Fock, o tempo) JA estao no kernel do Nos (a base instalada e' a v395 selada); (b) o modulo novo da v396 (Psibit) NAO esta la ainda.",
     "# v396: (a) as pedras da v394 (o criterio binario, a rede de Fock, o tempo) e da v395 (Psibit) JA estao no kernel do Nos (a base instalada e' a v395 selada); (b) o modulo novo da v396 (TestemunhaEstatica) NAO esta la ainda.", 1),
    ('_PEDRAS_V395 = ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual")\nassert all(os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", n_ + ".lean")) for n_ in _PEDRAS_V395) and os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "F1Fecho395", "NetworkProofAuditR8.lean")), "as pedras da v395 nao estao no kernel do Nos -- nao instalo"',
     '_PEDRAS_ANTERIORES = ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit")\nassert all(os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", n_ + ".lean")) for n_ in _PEDRAS_ANTERIORES) and os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "F1Fecho394", "NetworkProofAuditR8.lean")), "as pedras da v394 e da v395 nao estao no kernel do Nos -- nao instalo"', 1),
])
entrada("reverter_v395.py", regras=[("escrito em 21/10/2026, NAO executado na preparacao", "escrito em 22/10/2026, NAO executado na preparacao", 1)])
entrada("regras_v395.py", regras=[("ESCRITO em 21/10/2026", "ESCRITO em 22/10/2026", 1)])

# ------------------------------------------------------------------------------------------- teste do conferidor (caminho positivo)
entrada("teste_conferidor_positivo_v395.py")

# ------------------------------------------------------------------------------------------- derivar_instalar_rito (rito_v396.sh derivado do rito_v395.sh FINAL)
entrada("derivar_instalar_rito_v395.py", regras=[
    ('"""v395 -> v396, v393 -> v395 (o \'anterior\'), V395 -> V396, V393 -> V395, k395d -> k396c, k393 -> k395."""\n    t = t.replace("v395", "@@A@@").replace("v393", "v395").replace("@@A@@", "v396")\n    t = t.replace("V395", "@@B@@").replace("V393", "V395").replace("@@B@@", "V396")\n    t = t.replace("k395d", "k396c").replace("k393", "k395")',
     '"""v395 -> v396, v394 -> v395 (o \'anterior\'), V395 -> V396, V394 -> V395, k395c -> k396c, k394 -> k395."""\n    t = t.replace("v395", "@@A@@").replace("v394", "v395").replace("@@A@@", "v396")\n    t = t.replace("V395", "@@B@@").replace("V394", "V395").replace("@@B@@", "V396")\n    t = t.replace("k395c", "k396c").replace("k394", "k395")', 1),
    ('"kernel_modulos_novos_v396.json tem de trazer a LISTA com a pedra Psibit"', '"kernel_modulos_novos_v396.json tem de trazer a LISTA com a pedra TestemunhaEstatica"', 1),
    ("(a pedra Psibit ja' estava compilada em .lake/build; mudam a raiz TGLExt e o Audit)", "(a pedra TestemunhaEstatica pode ja' estar compilada em .lake/build numa versao anterior do texto, e o Lake a recompila se a fonte mudou; mudam a raiz TGLExt e o Audit)", 1),
    ('CABECALHO = ["# O RITO v396 (ato da gerencia c1, 21/10/2026): roda o um.py v396 instalado no Nos -- %d modulo novo de kernel (TGLExt/Psibit, a leitura psibit da orbita do Um pela matriz-S; o numero e\' lido de kernel_modulos_novos_v396.json) materializado a partir do corpo embutido, kernel e Audit" % N_NOVOS,\n'
     '             "# construidos pelo proprio um.py, os registros por spec e os tres registros novos do core v396 (psibit_v396, chamado NA FRACTALIZACAO DO UM; cunhagens_v396; kh_n1_cobertura_v396). O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (_QP_REUSE_V386",',
     'CABECALHO = ["# O RITO v396 (ato da gerencia c1, 22/10/2026): roda o um.py v396 instalado no Nos -- %d modulo novo de kernel (TGLExt/TestemunhaEstatica, a testemunha estatica: o psion habita a fronteira; nome provisorio; o numero e\' lido de kernel_modulos_novos_v396.json) materializado a partir do corpo embutido, kernel e Audit" % N_NOVOS,\n'
     '             "# construidos pelo proprio um.py, os registros por spec e os tres registros novos do core v396 (testemunha_estatica_v396, chamado NA FRACTALIZACAO DO UM junto do psibit_v395; cunhagens_v396; kh_n1_cobertura_v396). O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (_QP_REUSE_V386",', 1),
    ('assert L[0] == "#!/bin/sh" and L[1].startswith("# O RITO v395 (ato da gerencia c1, 19/10/2026)")', 'assert L[0] == "#!/bin/sh" and L[1].startswith("# O RITO v395 (ato da gerencia c1, 21/10/2026)")', 1),
    ('and "v393" not in RITO and "190" not in RITO.split("PK=")[0]', 'and "v394" not in RITO and "21/10/2026" not in RITO.split("PK=")[0]', 1),
    ('for tok in ("k395d", "k393", "work395", "v393"):\n        if tok in tx:', 'for tok in ("k395d", "k394", "work395", "v394"):\n        if tok in tx.replace("as pedras da v394", "").replace("pedras da v394 e da v395", ""):   # as pedras da v394 TEM de existir no kernel do Nos: referencia legitima ao passado', 1),
])
