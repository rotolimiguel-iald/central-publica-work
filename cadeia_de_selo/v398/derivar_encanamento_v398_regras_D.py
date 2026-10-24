# -*- coding: utf-8 -*-
# regras (lote D) de derivar_encanamento_v398.py: as PRE-CONDICOES (p00_precondicoes_v398.py) e o derivador do LANCADOR DO RITO (derivar_instalar_rito_v398.py). Mesmo metodo do lote B: a ancora `old` e' o trecho EXATO da v397 (lido do arquivo
# por `_seg`, sem digitar) passado por `bump()`; o `new` e' a v398. Contagem exata em cada regra; nada e' executado. (`_seg` e' definido no lote B, que o derivador executa antes.)

# ------------------------------------------------------------------------------------------- p00_precondicoes
_P = "p00_precondicoes_v397.py"
_ASTS = ('for f in ("delta_v398.py", "preparar_kernel_v398.py", "pos_build_kernel_v398.py", "registros_v398.py", "runtime_pedras_v398.py", "runtime_quadro_v397.py", "quadro_v397.py", "copiar_base_v398.py", "copiar_pedras_v398.py", "copiar_insumos_v398.py", "diff_e_pinos_v398.py", "gerar_esperados_v398.py",\n'
         '          "derivar_instalar_rito_v398.py", "simular_arvore_do_nos_v398.py", "exame_pontos_v398.py", "instalar_v398.py", "reverter_v398.py", "refazer_arvore_v398_pos_selo.py", "conferir_rito_v398.py", "gerar_candidato_v398.py", "ensaio_a_seco_v398.py", "comparar_v397_v398.py", "conferir_citacoes_v398.py",\n'
         '          "teste_conferidor_positivo_v398.py", "regras_v398.py", "guarda_p18_v398.py", "derivar_encanamento_v398.py", "derivar_encanamento_v398_regras.py", "derivar_encanamento_v398_regras_B.py", "derivar_encanamento_v398_regras_D.py", "gerar_estado_v398.py", "gerar_registro_mapa_prep_v398.py"):\n')
entrada(_P, regras=[
    (bump(_seg(_P, 'chk("o modulo novo (%d, lido da lista)', "\n")),
     'chk("os modulos novos (%d, lidos da lista) NAO estao no kernel do Nos; as pedras da v394 a v397 estao" % len(nov), nov == list(DL.STONE_RELS) and not any(os.path.exists(os.path.join(NK, *p.split("/"))) for p in nov) and all(os.path.exists(os.path.join(NK, "TGLExt", n + ".lean")) for n in ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica", "Token")))\n', 1),
    (bump(_seg(_P, 'F9 = DL.f9_fontes(', '[f["sha256"][:16] for f in F9])\n')),
     'F9 = [(c_, os.path.join(DL.F9_DIR_DURAVEL, n_)) for c_, n_ in (("f9v2_resultado", DL.F9_RESULTADO_NOME), ("f9v2_congelamento", "RECIBO_DE_CONGELAMENTO.json"), ("f9v2_abertura", "RECIBO_DE_ABERTURA.json"), ("f9v2_consumida", "ABERTURA_CONSUMIDA.json"))]\n'
     'chk("o Teste da Unica Palavra (v397, o QUADRO do topo): o resultado e os tres recibos (copias duraveis em v397/insumos/fase9) == os sha256 que a v397 pinou (ESPERADOS_v397); o resultado == o sha256 da ordem da v397; as SEIS inscricoes de 23/10 desta versao tem os prefixos de sha256 que a ordem da gerencia deu (a sexta e do texto da gerencia)",\n'
     '    all(sha(rd(p_)) == esp4["veracidade"]["fontes"][c_] for c_, p_ in F9) and sha(rd(F9[0][1])) == DL.F9_RESULTADO_SHA256_DA_ORDEM and len(DL.verbatins(os.path.join(HERE, "insumos", "cunhagens"))) == 6, [sha(rd(p_))[:16] for _, p_ in F9])\n', 1),
    (bump(_seg(_P, 'chk("simular_arvore_do_nos DESTE candidato:', "\n")),
     'chk("simular_arvore_do_nos DESTE candidato: o sonico_v398, a afinacao_das_cordas_v398 e os registros por spec v398 selam na arvore simulada do Nos (os anteriores tambem) e o hash formal tem %d entradas" % ESP["h8_entradas"], sim["candidato_sha16"] == CM["sha16"] and sim["formal_files_n_no_rito_real"] == ESP["h8_entradas"] '
     'and all(sim[k_]["all_verified"] is True for k_ in ("sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "testemunha_estatica_v396", "kh_n1_cobertura_v396", "psibit_v395")) and sim["kf_all_verified"] is True, sim["formal_files_n_no_rito_real"])\n', 1),
    (bump(_seg(_P, 'chk("exame_pontos_v397 DESTE candidato:', "\n")),
     'chk("exame_pontos_v398 DESTE candidato: nenhum ponto de chamada real da falso (o do psibit_v395 vem logo depois do principio da defasagem fractal, o da testemunha_estatica_v396 logo depois do psibit_v395, o do sonico_v398 logo depois da testemunha, o da afinacao_das_cordas_v398 logo depois do sonico e o do teste_de_veracidade_fase9_v397 logo depois do bloco do V1)", '
     'exm["sha256"] == CM["sha256"] and exm.get("algum_falso") == [] and exm["ponto_psibit"]["logo_depois_do_principio_da_defasagem_fractal"] is True and exm["ponto_testemunha"]["logo_depois_do_psibit_v395"] is True '
     'and exm["ponto_sonico"]["all_verified"] is True and exm["ponto_sonico"]["logo_depois_da_testemunha_v396"] is True and exm["ponto_sonico"]["beta_ok"] is True and exm["ponto_afinacao"]["all_verified"] is True and exm["ponto_afinacao"]["logo_depois_do_sonico_v398"] is True '
     'and exm["ponto_veracidade"]["all_verified"] is True and exm["ponto_veracidade"]["depois_do_psibit_e_da_testemunha"] is True and exm["ponto_veracidade"]["antes_do_bloco_v393"] is True and all(exm["ponto_veracidade"]["numeros_lidos_iguais_ao_resultado_pinado"].values()), exm.get("algum_falso"))\n', 1),
    (bump(_seg(_P, 'chk("a pedra: a fonte autoral', "\n")),
     'chk("as pedras: a fonte aprovada (work) == a copia v398/pedra == a copia duravel pinada (insumos) == a EMBUTIDA no candidato == a do sandbox == o pino dos ESPERADOS == o sha16 que a ordem da gerencia deu", '
     'all(sha(rd(s_["origem"])) == sha(rd(s_["src"])) == sha(rd(os.path.join(HERE, "insumos", s_["insumo"]))) == sha(E1[s_["rel"]].encode("utf-8")) == sha(rd(os.path.join(KS, *s_["rel"].split("/")))) == ESP["pedras_sha256"][s_["rel"]] and sha(rd(s_["src"]))[:16] == s_["sha16_da_ordem"] for s_ in DL.STONES), [s_["sha16_da_ordem"] for s_ in DL.STONES])\n'
     'ML_ = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "MEMORY.md")\n'
     'ML_N = len(open(ML_, encoding="utf-8", errors="replace").read().splitlines()) if os.path.exists(ML_) else -1\n'
     'chk("o MEMORY.md real tem folga para o handoff novo e o gancho da missao (linhas hoje + 2 <= 195; a superficie NAO compacta: se nao couber, PARE e diga)", 0 < ML_N and ML_N + 2 <= 195, [ML_N, 195])\n', 1),
    (bump(_seg(_P, 'for f in ("delta_v397.py"', 'quadro_v397.py"):\n')), _ASTS, 1),
    (bump('for f in ("rito_v397.sh", "refazer_sandbox_v397.sh", "refazer_sandbox_v397_pos_selo.sh", "construir_kernel_v397.sh", os.path.join("pos_rito", "chain_pos_rito_v397.sh")):'),
     'for f in ("rito_v398.sh", "refazer_sandbox_v398.sh", "refazer_sandbox_v398_pos_selo.sh", "construir_kernel_v398.sh", "refazer_candidato_v398.sh", os.path.join("pos_rito", "chain_pos_rito_v398.sh")):', 1),
])

# ------------------------------------------------------------------------------------------- derivar_instalar_rito (rito_v398.sh derivado do rito_v397.sh FINAL)
_R = "derivar_instalar_rito_v397.py"
_CAB398 = ('CABECALHO = ["# O RITO v398 (ato da gerencia c1, 23/10/2026): roda o um.py v398 instalado no Nos -- %d modulos novos de kernel (TGLExt/Sonico, o nome «sonico» e\' do operador; TGLExt/AfinacaoDasCordas, pedra e nome ratificados por ele; o numero e\' lido de kernel_modulos_novos_v398.json) materializados a partir do corpo embutido, kernel e Audit" % N_NOVOS,\n'
           '             "# construidos pelo proprio um.py, os registros com FUNCAO sonico_v398 e afinacao_das_cordas_v398 (chamados NA FRACTALIZACAO DO UM, logo depois da testemunha estatica) e os registros por spec novos do core v398 (cunhagens_v398, com as seis inscricoes de 23/10; kh_n1_cobertura_v398). O QUADRO do Teste da Unica Palavra (v397) segue no topo. O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (_QP_REUSE_V386",\n'
           '             "# segue no um.py; TGL_RITE_CHECKPOINT DESLIGADO). Molde: rito_v397.sh herdado com as afericoes dele, trocados os nomes, o pacote (a propria pasta da cadeia v398) e a",\n'
           '             "# guarda do marcador anterior: echo 1 | python um.py no Nos, stdout canonico em rodada_v398_stdout.txt, trailer RITO_RC=<rc>, horarios no pacote. RODADA COMPLETA."]\n')
entrada(_R, regras=[
    (bump('assert isinstance(_NJ.get("novos"), list) and _NJ["novos"] == [DL.STONE_REL], "kernel_modulos_novos_v397.json tem de trazer a LISTA com a pedra Token"'),
     'assert isinstance(_NJ.get("novos"), list) and _NJ["novos"] == list(DL.STONE_RELS), "kernel_modulos_novos_v398.json tem de trazer a LISTA com as DUAS pedras (Sonico e AfinacaoDasCordas)"', 1),
    (bump('t = t.replace("v396", "@@A@@").replace("v395", "v396").replace("@@A@@", "v397")'), 't = t.replace("v397", "@@A@@").replace("v396", "v397").replace("@@A@@", "v398")', 1),
    (bump('t = t.replace("V396", "@@B@@").replace("V395", "V396").replace("@@B@@", "V397")'), 't = t.replace("V397", "@@B@@").replace("V396", "V397").replace("@@B@@", "V398")', 1),
    (bump('t = t.replace("k396c", "k397c").replace("k395", "k396")'), 't = t.replace("k397c", "k398c").replace("k396", "k397")', 1),
    (bump('"""v396 -> v397, v395 -> v396 (o \'anterior\'), V396 -> V397, V395 -> V396, k396c -> k397c, k395 -> k396."""'), '"""v397 -> v398, v396 -> v397 (o \'anterior\'), V397 -> V398, V396 -> V397, k397c -> k398c, k396 -> k397."""', 1),
    (bump(_seg(_R, "CABECALHO = [", 'RODADA COMPLETA."]\n')), _CAB398, 1),
    (bump('"sobe": "v396 -> v397, v395 -> v396 (anterior), V396 -> V397, V395 -> V396, k396c -> k397c, k395 -> k396; o cabecalho descritivo de 4 linhas e a linha TEMPO ESPERADO sao ESCRITOS para a v397"'),
     '"sobe": "v397 -> v398, v396 -> v397 (anterior), V397 -> V398, V396 -> V397, k397c -> k398c, k396 -> k397; o cabecalho descritivo de 4 linhas e a linha TEMPO ESPERADO sao ESCRITOS para a v398"', 1),
    (bump('L[1].startswith("# O RITO v396 (ato da gerencia c1, 22/10/2026)")'), 'L[1].startswith("# O RITO v397 (ato da gerencia c1, 23/10/2026)")', 1),
    (bump('and "v395" not in RITO and "22/10/2026" not in RITO.split("PK=")[0]'), 'and "v396" not in RITO', 1),
    (bump("(a v396 ja' esta compilada em .lake/build e a pedra Token foi compilada sozinha antes; mudam a raiz TGLExt e o Audit)"), "(a v397 e as duas pedras novas ja' estao compiladas em .lake/build, cada pedra isolada; mudam a raiz TGLExt e o Audit)", 1),
    (bump("no Nos o primeiro build compila a pedra a frio, dezenas de segundos a mais"), "no Nos o primeiro build compila as pedras a frio, dezenas de segundos a mais", 1),
    (bump('for tok in ("k396d", "k395", "work396", "v395"):'), 'for tok in ("k397d", "k396", "work397", "v396"):', 1),
    (bump('"""derivar_instalar_rito_v397.py -- DERIVA MECANICAMENTE, do rito_v396.sh FINAL (o que rodou em 22/10), o lancador do rito da v397: rito_v397.sh (a subida de versao e\' v396 -> v397 e v395 -> v396, o \'anterior\' da guarda do marcador;'),
     '"""derivar_instalar_rito_v398.py -- DERIVA MECANICAMENTE, do rito_v397.sh FINAL (o que rodou em 23/10), o lancador do rito da v398: rito_v398.sh (a subida de versao e\' v397 -> v398 e v396 -> v397, o \'anterior\' da guarda do marcador;', 1),
])
