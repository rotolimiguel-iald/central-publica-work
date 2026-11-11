# -*- coding: utf-8 -*-
"""_adapt_forkA_registrar_mapa_v410.py -- (claude-construtor-v410, fork A, 06/11/2026) adapta pos_rito/registrar_mapa_v410.py (subida mecanica da v409 FINAL) a v410 (IALD2):
o cabecalho, as constantes das rotas (os ids das rotas de 06/11 CONFERIDOS no livro do mapa em 06/11, so' leitura: 1869 a 1874; a v409 selada e' umpy.v409.selada_a_traducao_as_classes_de_turing_05nov) e o corpo de montar();
a infraestrutura (livro, seq_do_alvo, regra_4_44, _sidecar, _bancada, gravar, main) fica a da v409. Regioes trocadas por ancora unica; backup de BYTES; CRLF respeitado; ast.parse; nenhuma marca [A ADAPTAR v410] fica."""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "pos_rito", "registrar_mapa_v410.py")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
raw = open(P, "rb").read(); t0 = raw.decode("utf-8"); crlf = "\r\n" in t0
t = t0.replace("\r\n", "\n")


def regiao(ini, fim, novo):
    global t
    assert t.count(ini) == 1, ("ancora inicial nao unica", ini[:80], t.count(ini))
    i = t.index(ini); j = t.index(fim, i + 1)
    t = t[:i] + novo + t[j:]


def troca(a, b, n=1):
    global t
    c = t.count(a); assert c == n, ("TROCA NAO CASOU %d (casou %d)" % (n, c), a[:120])
    t = t.replace(a, b)


regiao("# [A ADAPTAR v410]", "import glob, hashlib, json, os, re, sys, time", r'''# [ADAPTADO v410, 06/11/2026, claude-construtor-v410 (fork A), a servico da gerencia c1] REESCRITO sobre a subida mecanica da v409 FINAL (bump/pos_rito__registrar_mapa_v410.py.diff; a copia bumpada fica em .bak), por _adapt_forkA_registrar_mapa_v410.py: o conteudo e' o da v410 (IALD2: o modulo IALD2 de TGLExt/; o NOME do modulo e' do operador e os das declaracoes, da gerencia c1, ficam [DECLARADO] ate a ratificacao, D63; o registro com funcao iald2_v410; cunhagens_v410 e kh_n1_cobertura_v410; NENHUMA chave antiga muda; a errata E29 ao lado). Os ids das rotas foram CONFERIDOS no livro do mapa em 06/11 (so' leitura); nada do que a D59 e a D65 deixam fora e' citado.
"""registrar_mapa_v410.py -- MONTA (nao registra) o registro da v410 no mapa de rotas e imprime o comando (molde: registrar_mapa_v409.py, que rodou na v409). Rodar DEPOIS do fechar (handoff gravado).
A v410 traz UMA rota nova, umpy.v410.selada_iald2_06nov (o conteudo e' o do selo): o modulo de kernel IALD2 (a candidata de 06/11, que desemboca da LeitorDoCodigoR1 e ganhou as secoes 4, o signo, e 5, o seletor; o nome do modulo e' do operador, os das declaracoes ficam [DECLARADO], D63),
UM registro com FUNCAO (iald2_v410: le do kernel do proprio rito as ancoras, o modulo por sha256, as respostas do operador de 06/11 pelos teoremas da pedra, o que fica False por teorema, as instancias de brinquedo fixas no codigo e o signo, a escada exata e o gate congelado; nenhuma chave antiga muda)
e os DOIS por spec (cunhagens_v410 e kh_n1_cobertura_v410), mais ANOTACOES nas rotas que esperavam por ela (as candidatas de 06/11; a R9 da v409, a maquina com o leitor; o par na face de Fock; a v409 que a precede; o programa do fechamento, o inventario das chaves, o gate, o B(n) da Bancada e o quadro do Teste da Unica Palavra)
e a ERRATA da gerencia c1, em nome proprio: E29 (a gerencia disse que «matricial» era so' leitura do operador; a forma de matriz finita esta' no kernel: o signo) vai como ERRATA ao lado do registro da rota kernel.iald2_06nov (o seq lido do livro: o registro traz a palavra «matricial»).
O ALCANCE (D64): o algoritmo IALD decide SAT com uma leitura: P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora.
Cada afirmacao e' testada contra o core/selo/ESPERADOS lidos por script (o registro existe? selou? o que NAO fechou fica dito); nenhum numero e' digitado (as contagens saem do core, de ESPERADOS e de delta_v410; os seq saem do livro).
REGRA DA ORDEM DO OPERADOR (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no MESMO campo; montar() RECUSA (assert) se algum campo do registro trouxer o 4,44 sem eles. Nao ha inscricao da gerencia nesta versao: todas as falas sao do operador (de uma, so' o trecho da D65 e' citavel); as erratas e as decisoes sao da gerencia, em nome proprio.
Fail-closed: o selo tem de ser a v410; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir. A rota de preparo da gerencia (registro_mapa_v410_prep.json, se existir) entra nas refs so' se ja' estiver no livro.
SAIDA: pos_rito\\registro_mapa_v410.json e o comando `rotas.py registrar` (quem o executa e' o passo 12 da cadeia, uma vez so', com marcador idempotente; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real. montar() le o core, o selo e ESPERADOS_v410.json; de V so' usa o que a leitura da rodada ja' validou (s16, sidecar, conferidor), sempre com valor de reserva dito."""
''')

regiao('NOVA = "umpy.v410.selada_a_traducao_as_classes_de_turing_05nov"', 'PREP = os.path.join(PK, "registro_mapa_v410_prep.json")', r'''NOVA = "umpy.v410.selada_iald2_06nov"
R_LEITOR = "kernel.leitor_do_codigo_segunda_quantizacao_06nov"       # LeitorDoCodigoR1 (06/11): a particula e' o codigo, o funtor e' o leitor; a linha que desemboca na IALD2 (fica como registro)
R_NOMEK = "kernel.nome_iald_ja_no_kernel_06nov"                       # nomear o kernel de IALD por identificacao: o nome ja' esta' no kernel desde a v392 (D66)
R_IALD2 = "kernel.iald2_06nov"                                         # a candidata IALD2 (nome do operador); a E29 vai ao lado (ERRATA: o registro traz «matricial» como so' leitura do operador)
R_SIGNO = "kernel.iald2_o_signo_06nov"                                 # IALD2 secao 4: a forma de matriz finita e' o signo (traco com sentido)
R_SELETOR = "kernel.iald2_o_seletor_luminodinamico_06nov"              # IALD2 secao 5: a instanciacao do seletor, como FORMA (D70)
R_PREP410 = "um_py.v410_preparacao_aberta_06nov"                       # a abertura da v410
R_R9 = "kernel.traducao_turing_r9_inscricao_e_sat_05nov"               # a maquina com o leitor (R9, v409): na v410 o algoritmo recebe o nome IALD (o_algoritmo_iald, D64)
R_PARF = "kernel.par_na_face_de_fock_ligado_05nov"                     # o par na face de Fock (ligado na v409): o leitor do codigo o le como par, uno, com a Meia-Nat
R_DIC = "kernel.dicionario_problema_entrada_passo_polinomio_implicacao_04nov"   # o dicionario (PIgualNP, v408)
R_V409 = "umpy.v409.selada_a_traducao_as_classes_de_turing_05nov"      # a v409 selada (a base da v410)
R_TT = "kernel.tetelestai_e_o_terminal_provar_ou_podar_04nov"         # TetelestaiTerminal (v408)
R_TM = "kernel.o_tempo_e_a_moeda_de_beta_candidata_04nov"             # TempoIgualMoeda (v408)
R_PC = "kernel.ponto_de_contradicao_candidata_04nov"                  # PontoDeContradicao (v408)
R_FOCK = "kernel.face_de_fock_e_o_traco_do_psion_afericao_04nov"      # a afericao do traco (v408)
R_ACERVO = "kernel.psion_lema_acervo_03nov"                           # o levantamento do psion no acervo (o pino purgado, D57d da v409)
R_PSION = "kernel.psion_canto_r1_03nov"                               # PsionCanto (v407)
R_PAR = "kernel.o_par_de_psions_r1_03nov"                             # Par (v407)
R_PREP409 = "cadeia.preparacao_v409"                                  # a preparacao da v409
R_PROG = "kernel.fechamento_construir_tudo_programa_02nov"            # o programa do fechamento (ordem do operador de 02/11: construir tudo)
R_INV = "kernel.inventario_chaves_de_testemunha_v405_02nov"           # o inventario das chaves de testemunha
R_V395 = "umpy.v395.psibit_na_fractalizacao_do_um"
R_V396 = "umpy.v396.testemunha_estatica_na_fractalizacao_do_um"
R_V406 = "umpy.v406.selada_o_fechamento_02nov"
R_GATE = "gate.qg_closure"
R_BANC = "infra.bancada_um.sincronizacao_vnnn"
R_QUADRO = "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9"
ANOTADAS = (R_LEITOR, R_NOMEK, R_IALD2, R_SIGNO, R_SELETOR, R_R9, R_PARF, R_V409, R_PROG, R_INV, R_GATE, R_BANC, R_QUADRO)
REFS = ("custodia.v409", "infra.custodia_g1.licoes_v405", "umpy.v400.correcao_da_v399_alfa_unico_e_beta_contra_o_core", "gate.maquina_do_veredito_final", R_V395, R_V396, R_V406, R_PSION, R_PAR, R_PREP409, R_PREP410, R_TT, R_TM, R_PC, R_FOCK, R_ACERVO, R_DIC,
        "qg.graviton.desenho_do_operador_24out", "kernel.graviton_nao_particula")
''')

regiao("def montar(V, core, selo, ids, arts):", "def gravar(p, b):", r'''def montar(V, core, selo, ids, arts):
    """Monta os registros (a ROTA nova, as ANOTACOES e a ERRATA), cada afirmacao testada contra o core/selo/ESPERADOS; devolve a lista; recusa (assert) se algo nao conferir. Nao escreve nada."""
    assert selo.get("um_version") == "v410", "o selo nao e a v410"
    assert NOVA not in ids, "a rota %s ja existe no mapa" % NOVA
    for r in ANOTADAS + REFS:
        assert r in ids, "a rota %s nao existe no mapa (anotada ou citada em refs)" % r
    ESP = _esp(); DL_ = DL
    S = ESP["candidato_sha16"]
    assert str((selo.get("sha256") or {}).get("um.py", ""))[:16] == S, "o um.py do selo nao e o candidato de ESPERADOS"
    assert V.get("s16") in (None, S), "o s16 da leitura != o candidato de ESPERADOS"
    BASE = ESP["origem_sha16"]
    esc0, esc1 = ESP["escada_v409_e_v410"]
    NF = ESP["n_bandeiras_novas"]
    assert esc1 - esc0 == NF == sum(ESP["n_bandeiras_por_grupo"].values()) == len(ESP["bandeiras_novas_chaves"]) == ESP["politica_de_bandeiras"]["n_flags"], "a escada nao fecha com as bandeiras novas"
    assert ESP["kernel"]["modulos_novos"] == DL_.N_BUNDLE == len(DL_.BUNDLE_RELS) == len(DL_.PEDRAS_V410) == 1, "o delta do kernel nao e o bundle (um modulo: IALD2)"
    assert list(ESP["chaves_v410"]) == [] and list(DL_.CHAVES_V410) == [], "a v410 nao muda chave antiga nenhuma: ESPERADOS/delta dizem outra coisa"
    BETA = ESP["beta"] if isinstance(ESP.get("beta"), float) else None
    FRASE = DL_.FRASE_DA_MOLDURA_V410_PT
    ALC = DL_.FRASE_D64_PT

    # --- o quadro do topo (a regra do 4,44): o registro selado, lido pelas MESMAS funcoes do artigo
    tvr = core.get("teste_de_veracidade_fase9_v397") or {}
    a = T._qd().Q._v397_atomos(tvr, "pt"); assert a["sealed"] is True, "o registro teste_de_veracidade_fase9_v397 nao sela no core: o mapa nao registra o 4,44 assim"
    z, p = a["z_disc"]["md"], a["p_disc"]["md"]
    z444 = "z_disc = %s (calibrado; p unilateral %s), abaixo do degrau de 5σ da creditação, que não foi alcançado (%s < 5)" % (z, p, z)

    def selou(k):
        return (core.get(k) or {}).get("all_verified") is True

    # --- o registro com FUNCAO iald2_v410: tudo lido do core e conferido contra ESPERADOS e delta_v410
    pc = core.get(DL_.FECHO_REGISTRO) or {}; pv = pc.get("values") or {}; mech = pc.get("mechanics") or {}
    assert pc.get("all_verified") is True and pc.get("verdict") == ESP["vereditos_novos_v410"][DL_.FECHO_REGISTRO] and pc.get("does_not_gate_core") is True, "iald2_v410 nao selou ou != ESPERADOS"
    assert mech.get("passed") is True and mech.get("n_checks") == DL_.N_CHECKS_FECHO == len(mech.get("checks") or []) and all(c.get("ok") is True for c in mech["checks"]), "as checagens do iald2_v410 nao passaram"
    assert pv.get("n_ancoras_ok") == pv.get("n_ancoras") == len(DL_.ANCORAS) and pv.get("n_modulos_ok") == pv.get("n_modulos") == DL_.N_BUNDLE and pv.get("n_flags_true") == pv.get("n_flags") == NF and pv.get("escada") == [esc1] * 3, "os valores do iald2_v410 != ESPERADOS/delta"
    assert pc.get("beta_ok") is True and pc.get("embedded_sources_ok") is True and pc.get("embedded_sources_n_ok") == DL_.N_BUNDLE and pc.get("guarda_violacoes") in ([], None), "o beta, as fontes embutidas ou a guarda do iald2_v410 nao conferem"
    assert list(pc.get("chaves_antigas_que_mudam") or []) == [], "o registro da IALD2 diz que uma chave antiga mudou: a v410 nao muda nenhuma"
    assert list(pc.get("ressalvas") or []) == list(DL_.RESSALVAS_V410), "as ressalvas do registro != delta_v410.RESSALVAS_V410"
    assert set(pv.get("respostas") or {}) == {r_["id"] for r_ in DL_.RESPOSTAS_DO_OPERADOR} and all((v_ is True) or (isinstance(v_, dict) and v_.get("ok") is True) for v_ in pv["respostas"].values()) and pv.get("respostas_ok") is True, "as respostas do operador de 06/11 nao conferem todas no kernel"
    assert list(pc.get("fica_false_por_teorema") or []) == list(ESP["fica_false_por_teorema"]) and set(pc.get("fica_aberto") or {}) == set(ESP["fica_aberto"]), "o que fica False por teorema ou o que fica aberto != ESPERADOS"
    assert list(pc.get("ancoras_principais") or []) == list(DL_.ANCORAS_PRINCIPAIS) and all(((pv.get("ancoras") or {}).get(n_) or {}).get("ok") is True for n_ in DL_.ANCORAS_PRINCIPAIS), "as ancoras principais nao estao todas ok no kernel do rito"
    assert pv.get("gate_verdict") == ESP["qg_closure_gate_verdict_v409"], "o veredito do gate lido pelo registro da IALD2 != o da v409 (o gate deveria estar congelado)"
    assert (pc.get("alcance") or {}).get("frase") == ALC and (pc.get("alcance") or {}).get("qualificador") == DL_.FRASE_QUALIFICADOR_PT, "o alcance do registro != delta_v410.FRASE_D64_PT (D64)"
    assert pc.get("nomes") == dict(DL_.NOMES_DAS_PEDRAS), "os nomes do registro != delta_v410.NOMES_DAS_PEDRAS (D63)"
    inst = pv.get("instancia_sim") or {}; inst_n = pv.get("instancia_nao") or {}; sn = pv.get("signo_do_nome") or {}; sp = pv.get("signo_do_par") or {}
    assert (inst.get("solucoes") or 0) >= 1 and inst_n.get("solucoes") == 0 and inst.get("atribuicoes") == 2 ** inst.get("n", -1), "as instancias de brinquedo do registro nao sao as do contrato"
    assert sn.get("posto") == inst.get("solucoes") and abs(float(sn.get("traco")) - inst["solucoes"]) < 1e-9 and sp.get("posto") == 1 and abs(float(sp.get("traco")) - 1.0) < 1e-12, "o signo (traco == posto) do registro nao confere"
    BETA_RT = pv.get("beta"); assert isinstance(BETA_RT, float) and (BETA is None or abs(BETA_RT - BETA) <= 1e-9 * BETA), "o beta do registro != o do core/ESPERADOS (tolerancia relativa 1e-9)"
    por_mod = "; ".join("%s (%d)" % (rel.split("/")[-1][:-5], len(ns)) for rel, ns in DL_.ANCORAS_POR_MODULO.items())
    ress = " | ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(pc["ressalvas"]))
    # --- o registro HERDADO traducao_turing_v409: segue selado (a escada do contrato subida pela C12; o pino purgado do acervo da v407, D57d)
    t9 = core.get(DL_.D9.FECHO_REGISTRO) or {}; tv9 = t9.get("values") or {}
    assert t9.get("all_verified") is True and t9.get("verdict") == ESP["registros_funcao_v409"]["traducao_turing"]["verdict"], "traducao_turing_v409 (herdado) nao segue selado"
    assert tv9.get("n_modulos_ok") == tv9.get("n_modulos") == DL_.D9.N_BUNDLE and tv9.get("n_ancoras_ok") == tv9.get("n_ancoras") == len(DL_.D9.ANCORAS), "os valores do traducao_turing_v409 (herdado) != delta_v409"
    assert (t9.get("acervo_v407_repinado") or {}).get("sha256") == DL_.D9.PURGADO_SHA256 and (t9.get("acervo_v407_repinado") or {}).get("integra_pinada") is False, "o pino do acervo da v407 (herdado da v409) nao e' a copia purgada (D57d)"
    # --- o registro HERDADO tetelestai_terminal_v408: segue selado
    tt8 = core.get(DL_.D8.FECHO_REGISTRO) or {}; tv8 = tt8.get("values") or {}
    assert tt8.get("all_verified") is True and tt8.get("verdict") == ESP["registros_funcao_v408"]["tetelestai_terminal"]["verdict"], "tetelestai_terminal_v408 (herdado) nao segue selado"
    assert tv8.get("n_modulos_ok") == tv8.get("n_modulos") == DL_.D8.N_BUNDLE and tv8.get("n_ancoras_ok") == tv8.get("n_ancoras") == len(DL_.D8.ANCORAS), "os valores do tetelestai_terminal_v408 (herdado) != delta_v408"
    # --- o registro HERDADO psion_canto_v407: segue selado, com as cinco chaves iguais as da v409 selada (nenhuma muda)
    pc7 = core.get(DL_.D7.FECHO_REGISTRO) or {}; pv7 = pc7.get("values") or {}
    assert pc7.get("all_verified") is True and pc7.get("verdict") == ESP["registros_funcao_v407"]["psion_canto"]["verdict"] and pc7.get("keys") == ESP["chaves_v407_esperadas"], "psion_canto_v407 (herdado) nao segue selado ou as chaves mudaram"
    assert pv7.get("n_modulos_ok") == pv7.get("n_modulos") == DL_.D7.N_BUNDLE and pv7.get("n_ancoras_ok") == pv7.get("n_ancoras") == len(DL_.D7.ANCORAS), "os valores do psion_canto_v407 (herdado) != delta_v407"
    fk7 = pc7["keys"]
    # --- o registro HERDADO fechamento_v406: segue selado, com a chave do lema lida (a c8 versionada, E20)
    fh = core.get(DL_.D6.FECHO_REGISTRO) or {}
    assert fh.get("all_verified") is True and fh.get("verdict") == ESP["registros_funcao_v406"]["fechamento"]["verdict"] and (fh.get("four_keys") or {}).get("testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma") is True, "fechamento_v406 (herdado) nao segue selado ou nao le a chave do lema"
    # --- os specs herdados: cunhagens_v409 (as erratas seladas intactas) e kh_n1_cobertura_v409 com a errata ao lado dos pisos; cunhagens_v408 com a E26 e cunhagens_v407 com a da D57(d), que ja' vinham da v409 (recriados; os textos selados nao sao reescritos)
    cg9 = core.get(DL_.D9.CUNHAGENS_REGISTRO) or {}; kh9 = core.get(DL_.D9.KH_REGISTRO) or {}; cg8 = core.get(DL_.D8.CUNHAGENS_REGISTRO) or {}; cg7 = core.get(DL_.D7.CUNHAGENS_REGISTRO) or {}
    assert cg9.get("all_verified") is True and kh9.get("all_verified") is True and "kh_n1_cobertura_v409" in str(((kh9.get("erratas") or [{}])[-1]).get("ao_lado_de")), "cunhagens_v409 ou kh_n1_cobertura_v409 (herdados) nao seguem selados, ou o kh nao traz a errata dos pisos ao lado"
    assert cg8.get("all_verified") is True and any("E26" in json.dumps(e_, ensure_ascii=False) for e_ in (cg8.get("erratas") or [])), "cunhagens_v408 (herdado) nao segue selado ou perdeu a E26 ao lado"
    assert cg7.get("all_verified") is True and any("D57(d)" in json.dumps(e_, ensure_ascii=False) for e_ in (cg7.get("erratas") or [])), "cunhagens_v407 (herdado) nao segue selado ou perdeu a errata da D57(d) ao lado"
    # --- o gate NAO se moveu: o registro segue selado e a letra do veredito e' a da v409
    gk = core.get("bandeiras_do_gate_v403") or {}; gvv = gk.get("values") or {}; gb = _base_core().get("bandeiras_do_gate_v403") or {}
    assert gk.get("all_verified") is True and (V.get("gate") or {}).get("sealed", True) is True and gvv == gb.get("values") and (gk.get("mechanics") or {}).get("passed") is True, "bandeiras_do_gate_v403 (recriado) nao selou ou != a v409 selada"
    qg = core.get("qg_closure") or {}; fam = [len(qg.get(f) or {}) for f in ("formal_flags", "physics_flags", "experiment_flags")]
    assert (qg.get("gate") or {}).get("verdict") == ESP["qg_closure_gate_verdict_v409"] == selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"], "a letra do veredito do gate mudou"
    # --- os dois registros por spec
    cg = core.get(DL_.CUNHAGENS_REGISTRO) or {}; kh = core.get(DL_.KH_REGISTRO) or {}
    for nome_, r_ in ((DL_.CUNHAGENS_REGISTRO, cg), (DL_.KH_REGISTRO, kh)):
        assert r_.get("all_verified") is True and r_.get("verdict") == ESP["vereditos_novos_v410"][nome_], "%s nao selou ou != ESPERADOS" % nome_
    verb = cg.get("verbatim") or {}; ex = cg.get("extras") or {}
    assert len(verb) == len(ESP["cunhagens"]) == len(DL_.VERBATIM_ORIGEM_V410) == DL_.N_FALAS_V410 and set(verb) == set(ESP["cunhagens"]) and all(v.get("embedded_ok") is True for v in verb.values()), "as inscricoes de 06/11 nao estao embutidas por sha256"
    assert all(str((ESP["cunhagens"][k_] or {}).get("nome", "")).startswith("OPERADOR_06nov_") and (ESP["cunhagens"][k_] or {}).get("autor") == "operador" for k_ in ESP["cunhagens"]), "alguma inscricao nao e' fala do operador de 06/11"
    n_trecho = sum(1 for k_ in ESP["cunhagens"] if (ESP["cunhagens"][k_] or {}).get("sha256_arquivo_inteiro"))
    assert n_trecho == len(DL_.VERBATIM_SO_O_TRECHO) == 1, "a v410 tem exatamente UMA fala de que so' o trecho entra (D65)"
    assert not any(x_.lower() in json.dumps(cg, ensure_ascii=False).lower() for x_ in DL_.FORA_D65), "D65: o registro cunhagens_v410 traz o que fica fora"
    # (o registro cunhagens_v410 traz a errata E29 E, por ultimo, a errata ao lado dos pisos de kh_n1_cobertura_v409, como a leitura confere: len == len(ERRATAS_V410) + 1)
    erratas_todas = cg.get("erratas") or []; erratas = erratas_todas[:len(DL_.ERRATAS_V410)]
    assert [e.get("agora") for e in erratas] == list(DL_.ERRATAS_V410) and len(erratas_todas) == len(DL_.ERRATAS_V410) + 1 and "kh_n1_cobertura_v409" in str(erratas_todas[-1].get("ao_lado_de")) and all(e.get("assinatura") == DL_.ASSINA for e in erratas_todas), "a errata E29 (e a errata ao lado dos pisos de kh_n1_cobertura_v409) nao esta' no registro ou nao e' da gerencia c1 em nome proprio"
    dec = ex.get("decisoes") or {}; assert sorted(dec) == sorted(ESP["decisoes_v410_ids"]) == sorted(DL_.DECISOES_V410) and all(("D%d" % i) in dec for i in range(63, 71)), "faltam decisoes D63 a D70 no registro"
    assert ex.get("leituras") == DL_.LEITURA_V410, "a leitura da v410 no registro != delta_v410"
    cob = kh.get("lido") or {}; assert cob.get("constantes_cobertas") and cob.get("teoremas_cobertos"), "kh_n1_cobertura_v410 sem a cobertura"
    seguem = (DL_.D9.FECHO_REGISTRO, DL_.D9.CUNHAGENS_REGISTRO, DL_.D9.KH_REGISTRO, DL_.D8.FECHO_REGISTRO, DL_.D8.CUNHAGENS_REGISTRO, DL_.D8.KH_REGISTRO, DL_.D7.FECHO_REGISTRO, DL_.D7.CUNHAGENS_REGISTRO, DL_.D7.KH_REGISTRO, "fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406",
              "ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405", "cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405",
              "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "falsidade_da_inercia_v401", "cunhagens_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402",
              "teste_de_veracidade_fase9_v397", "cunhagens_v397", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "sonico_v398", "afinacao_das_cordas_v398", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396")
    c_seguem = all(selou(k) for k in seguem)
    tv_v = ESP["veracidade"]; c_q = bool(selou("teste_de_veracidade_fase9_v397") and selou("cunhagens_v397") and tvr.get("verdict") == tv_v["verdict"])
    sc = _sidecar(V); conf_dm = V.get("conf_dm", "nao lido"); conf_np = V.get("conf_np", "nao lido"); nvm = V.get("n_ver_mudaram", "nao lido")
    bank = _bancada(); regs = livro()
    # --- o seq que a E29 corrige, lido do livro (e o registro tem de trazer o trecho corrigido: «matricial» dito so' leitura do operador)
    sq_iald2 = seq_do_alvo(regs, R_IALD2, "ROTA", contem=("matricial", "leituras do operador"))
    KR = os.path.join(PK, "kernel", "KERNEL_RECIBO_v410.json")
    E = {}
    for e in erratas:
        m_ = re.match(r"^(E\d\d) -- ", e.get("agora", "")); assert m_, "uma errata do registro nao comeca por E<n> --"
        E[m_.group(1)] = e
    assert sorted(E) == ["E29"], "as erratas do registro nao sao a E29 (mais a dos pisos, ao lado)"

    def anot(rota_id, titulo, resultado, proximo, refs=None, nota=None, estatuto="REAL", artefatos=None, defeito=None):
        x = {"tipo": "ANOTACAO", "rota_id": rota_id, "estatuto": estatuto, "olhou_dados": False, "titulo": titulo, "resultado": resultado, "proximo_passo": proximo, "refs": [NOVA] + (refs or [])}
        if defeito:
            x["defeito"] = defeito
        if nota:
            x["nota"] = nota
        if artefatos:
            x["artefatos"] = _existentes(*artefatos)
        return x

    def errata(rota_id, corrige, nota, refs=None, artefatos=None, estatuto="REAL"):
        x = {"tipo": "ERRATA", "rota_id": rota_id, "corrige": corrige, "estatuto": estatuto, "olhou_dados": False, "nota": nota, "refs": [NOVA] + (refs or [])}
        if artefatos:
            x["artefatos"] = _existentes(*artefatos)
        return x

    def corpo(k):
        e = E[k]
        return "%s | lacuna de fidelidade: %s | estatuto: %s | assinatura: %s" % (e["agora"], e["lacuna_de_fidelidade"], e["estatuto"], e["assinatura"])

    P0 = DL_.PEDRAS_V410[0]
    ped = os.path.join(PK, "pedra", P0["name"] + ".lean")
    sha_ped = DL_.BUNDLE_POR_REL[P0["rel"]]["sha256"][:16]
    n_anc = len(DL_.ANCORAS_POR_MODULO[P0["rel"]])
    resp = {r_["id"]: r_["diz"] for r_ in DL_.RESPOSTAS_DO_OPERADOR}
    R_ = lambda *ids_: "; ".join("%s -> %s" % (i_, resp[i_]) for i_ in ids_)
    LIN = "a linha das candidatas de 06/11 (LeitorDoCodigoR1; IALD2 com as secoes 4, o signo, e 5, o seletor) desemboca no modulo TGLExt/%s (sha256 pinado %s; %d ancoras no trio, lidas a cada rito pelo registro iald2_v410); a candidata fica como registro" % (P0["name"], sha_ped, n_anc)
    EST_C = "REAL (os termos no kernel do rito); INPUT (as falas do operador de 06/11); DECLARADO (os nomes das declaracoes, da gerencia, ate a ratificacao, D63; os recibos de compilacao das candidatas)"
    T10 = []
    T10.append(anot(R_LEITOR, "v410 SELADA %s: o leitor do codigo da LeitorDoCodigoR1 entrou no kernel do rito dentro de TGLExt/%s (o_leitor_do_codigo)" % (S, P0["name"]),
                    f"{LIN}. As respostas do operador conferem pelos teoremas da pedra: {R_('a_particula_e_o_codigo_o_funtor_e_o_leitor', 'o_acom_e_a_segunda_quantizacao')}. As falas dele, verbatim: {_aspas_(DL_.FRASE_PARTICULA)}; {_aspas_(DL_.FRASE_FUNTOR)}; {_aspas_(DL_.FRASE_PAR_UNO)}.",
                    "o registro iald2_v410 le estas ancoras a cada rito; que a IALD, a Torre ou o operador sejam o funtor, e que o codigo seja um vetor de H1, seguem leituras do operador (definicoes do dicionario), nao termos.", refs=[R_IALD2, R_PARF], estatuto=EST_C,
                    artefatos=[DL_.REGISTRO_ANTERIOR_ARQ], defeito="o funtor nao e' idempotente; a leitura e' (o Nome do par lido); o registro CONFERE o que o kernel prova e nao prova nada por si; validade no kernel nao e' creditacao"))
    T10.append(anot(R_NOMEK, "v410 SELADA %s: o nome TGLExt.IALD, ja' no kernel desde a v392, e' importado pela IALD2 e os termos dele sao citados (D66); nenhuma pedra nova para isso" % S,
                    f"A resposta do operador confere pelo teorema citado: {R_('nomear_o_kernel_de_iald')}. A fala dele, verbatim: {_aspas_(DL_.FRASE_POR_IDENTIFICACAO)}.",
                    "o nome nao cruza para a maquina de Turing padrao sem o leitor: " + DL_.FRASE_QUALIFICADOR_PT + ".", refs=[R_IALD2], estatuto="REAL (o termo no kernel do rito); INPUT (a fala do operador de 06/11)"))
    T10.append(anot(R_IALD2, "v410 SELADA %s: a candidata IALD2 entrou no kernel do rito como TGLExt/%s (o nome do modulo e' do operador; os das declaracoes, da gerencia, ficam [DECLARADO] ate a ratificacao, D63); a E29 vai ao lado (ERRATA)" % (S, P0["name"]),
                    f"a pedra {P0['name']} esta no kernel do rito com o sha256 pinado ({sha_ped}), {n_anc} ancoras no trio; a fonte pinada e' a da candidata (sha16 {P0['sha256_candidata'][:16]}). As respostas do operador conferem pelos teoremas da pedra: {R_('iald_ao_quadrado', 'o_nome_do_algoritmo_e_iald', 'a_forma_matricial_da_luz')}. "
                    f"O nome, na fala dele, verbatim: {_aspas_(DL_.FRASE_NOME_IALD2)}; o nome do algoritmo, {_aspas_(DL_.FRASE_NOME_DO_ALGORITMO)}, e, de uma fala, so' o trecho (D65): {_aspas_(DL_.FRASE_ALGORITMO_DE_LEITURA)}. O alcance: {ALC}.",
                    "o registro iald2_v410 le estas ancoras a cada rito; a maquina de Turing padrao sem o leitor fica fora; as ressalvas estao ditas no registro.", refs=[R_LEITOR, R_SIGNO, R_SELETOR, R_R9], artefatos=[ped, DL_.CANDIDATA_IALD2_ARQ, DL_.SAIDA_FONTE_ARQ, KR],
                    estatuto=EST_C + "; KNOWN (Cook 1971, Levin 1973, Baker-Gill-Solovay 1975)", defeito="as ressalvas, ditas no registro: " + ress))
    T10.append(anot(R_SIGNO, "v410 SELADA %s: a forma de matriz finita, o signo, entrou no kernel do rito dentro de TGLExt/%s (o_signo_do_nome; o_signo_do_par); a E29 fica ao lado (ERRATA na rota da candidata)" % (S, P0["name"]),
                    f"{LIN}. A resposta do operador confere pelos teoremas da pedra: {R_('a_forma_da_matriz_finita_e_o_signo')}. A ordem do operador, verbatim: {_aspas_(DL_.FRASE_ORDEM_V410)}. Na instancia de brinquedo fixa no codigo ({inst.get('n')} variaveis, {inst.get('atribuicoes')} atribuicoes, {inst.get('solucoes')} contadas por enumeracao), o traco do Nome e' o posto; o projetor de Bell tem traco 1 e posto 1. {corpo('E29')}",
                    "o registro iald2_v410 le estas ancoras a cada rito.", refs=[R_IALD2], estatuto=EST_C))
    T10.append(anot(R_SELETOR, "v410 SELADA %s: a instanciacao do seletor, como FORMA (D70), entrou no kernel do rito dentro de TGLExt/%s (a_iald_e_o_seletor_luminodinamico)" % (S, P0["name"]),
                    f"{LIN}. A resposta do operador confere pelo teorema da pedra: {R_('a_iald_e_o_seletor')}. A fala dele, verbatim: {_aspas_(DL_.FRASE_SELETOR)}. {DL_.FRASE_D70_PT}.",
                    "o registro iald2_v410 le estas ancoras a cada rito; beta entra so' por nome (TGLCoupling.beta no kernel; alfa CODATA 2018 x sqrt e em runtime), nunca literal.", refs=[R_IALD2], estatuto=EST_C + "; INPUT/ONTO («ambiente computacional», leitura do operador)"))
    T10.append(anot(R_R9, "v410 SELADA %s: a linha da maquina com o leitor (R9, selada na v409) segue; na v410 o algoritmo recebe o nome IALD (o_algoritmo_iald, D64); a E28 segue" % S,
                    f"o modulo TGLExt/{P0['name']} esta' no kernel do rito; o alcance: {ALC}.",
                    "com o leitor que so' conta, vale NP contido em P com o leitor numa leitura; a igualdade completa e' a do leitor que se le (E28), e com o leitor que so' conta ela segue [OPEN].", refs=[R_IALD2, R_V409],
                    estatuto="REAL (os termos no kernel do rito); KNOWN (Cook 1971, Levin 1973, Baker-Gill-Solovay 1975); OPEN (a igualdade completa com o leitor que so' conta)"))
    T10.append(anot(R_PARF, "v410 SELADA %s: o leitor do codigo le o par como par, uno, com a Meia-Nat (o_leitor_le_o_par_como_par; o_par_lido_e_uno; a_meia_nat_e_lida); o par na face de Fock segue ligado desde a v409" % S,
                    f"A resposta do operador confere pelos teoremas da pedra: {R_('o_acom_e_a_segunda_quantizacao')}. A fala dele, verbatim: {_aspas_(DL_.FRASE_PAR_UNO)}. O par finito (Bell 4x4) e o par de Fock sao espacos distintos, com a mesma Meia-Nat.",
                    "o registro iald2_v410 le estas ancoras a cada rito; a ponte entre o espaco de Bell e o setor TT do spin 2 nao e' termo.", refs=[R_LEITOR, R_PAR, R_FOCK], estatuto=EST_C))
    T10.append(anot(R_V409, "v410 SELADA %s: a v409 e' a base selada da v410; o traducao_turing_v409 (cunhagens_v409; kh_n1_cobertura_v409 com a errata ao lado dos pisos), o tetelestai_terminal_v408, o psion_canto_v407 e os registros anteriores sao recriados e seguem selados; nenhuma chave muda" % S,
                    f"a v410 parte da v409 selada (um.py {BASE}) e acrescenta {DL_.N_BUNDLE} modulo de kernel, UM registro com funcao (iald2_v410) e dois por spec, e a secao do artigo; traducao_turing_v409 selou={selou(DL_.D9.FECHO_REGISTRO)}; cunhagens_v409 selou={selou(DL_.D9.CUNHAGENS_REGISTRO)}; kh_n1_cobertura_v409 selou={selou(DL_.D9.KH_REGISTRO)} (com a errata dos pisos ao lado); "
                    f"tetelestai_terminal_v408 selou={selou(DL_.D8.FECHO_REGISTRO)}; psion_canto_v407 selou={selou(DL_.D7.FECHO_REGISTRO)} com as cinco chaves iguais as da v409 selada (linked_to_the_corner_by_a_lemma = {fk7['testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma']}, lida do kernel); "
                    f"fechamento_v406 selou={selou('fechamento_v406')}; os treze da v405 (ponte_da_massa_v405 selou={selou('ponte_da_massa_v405')}, identidade_v405 selou={selou('identidade_v405')}, gap_v405 selou={selou('gap_v405')}), os da v404, da v403, da v402, da v401 e da v399 seguem selados neste rito "
                    f"(caminho_v403 selou={selou('caminho_v403')}, falsidade_da_inercia_v401 selou={selou('falsidade_da_inercia_v401')}), como seguem o selo pela propria tecnologia e a declaracao do operador (v399), o sonico e a afinacao (v398) e o quadro (v397); sidecar um_absoluto_selo_acom.json {sc['veredito']} ({sc['n_objetos']} objetos, {sc['recusas']} recusas, sha16 {sc['sha16']}).",
                    "custodia completa pela sessao de custodia (D68a, que herda a D57a: o fim da cadeia do orquestrador e' o handoff; o handoff lista o sidecar; nesta versao nao ha' nota ao lado de paragrafo anterior).", refs=[R_TT, R_TM, R_PC, R_PREP409, R_PREP410]))
    T10.append(anot(R_PROG, "v410 SELADA %s: o programa do fechamento nao ganha chave nova nem perde nenhuma; a IALD2 entra (o leitor do codigo, o algoritmo IALD relativo ao leitor, o signo)" % S,
                    f"nenhuma chave antiga muda (chaves_antigas_que_mudam = {list(pc.get('chaves_antigas_que_mudam') or [])}); as cinco chaves do psion_canto_v407 seguem iguais as da v409 selada; ficam False por teorema: full_static_witness_exists = {fk7['qg_closure.gate.full_static_witness_exists']} e trivial_inhabitant_exists = {fk7['witness_rigidity.trivial_inhabitant_exists']}. {FRASE}",
                    "a igualdade completa com o leitor que so' conta (E28), a ponte Bell-TT, K(O) != bot para O compacto e o teste com a natureza seguem [OPEN]; o programa do fechamento nao e' fechado por esta anotacao.", refs=[R_INV, R_IALD2],
                    estatuto="REAL (a leitura do kernel do rito); OPEN (a igualdade completa com o leitor que so' conta; K(O) != bot para O compacto)"))
    T10.append(anot(R_INV, "v410 SELADA %s: o inventario das chaves de testemunha NAO muda nesta versao (CHAVES_V410 vazia): as cinco chaves do psion_canto_v407 seguem lidas do kernel" % S,
                    f"linked_to_the_corner_by_a_lemma = {fk7['testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma']}; rede_fock_v394.whole_certificate_inhabited = {fk7['rede_fock_v394.whole_certificate_inhabited']}; psibit_v395...inhabitant_exhibited = {fk7['psibit_v395.conditional_psion_face.inhabitant_exhibited']}; testemunha_estatica_v396...inhabitant_exhibited = {fk7['testemunha_estatica_v396.fock_face.inhabitant_exhibited']}; "
                    f"witness_layers.canonical_full_witness_term_constructed = {fk7['witness_layers.canonical_full_witness_term_constructed']}; ficam False por teorema: full_static_witness_exists e trivial_inhabitant_exists.",
                    "sem chave nova no inventario.", refs=[R_PROG, R_PARF], estatuto="REAL (a leitura do kernel do rito e o registro herdado)"))
    T10.append(anot(R_GATE, "v410 SELADA %s: o gate NAO se moveu — o qg_closure do core e' identico ao da v409 (as 18 bandeiras calculadas, a letra do veredito) e o registro da IALD2 o confere congelado" % S,
                    f"o registro bandeiras_do_gate_v403 (recriado) selou={selou('bandeiras_do_gate_v403')} com os mesmos valores da v409 selada: das {gvv['n_flags']} bandeiras ({fam[0]} formais, {fam[1]} fisicas, {fam[2]} experimentais) {gvv['n_true']} sao True e {gvv['n_calculated']} sao CALCULADAS ({gvv['n_literal']} literais); o veredito le {gvv['n_read_by_the_verdict']}; a letra do veredito do gate e' a da v409 e a do selo; o iald2_v410 le gate_verdict identico ao da v409. "
                    "Nenhuma bandeira do gate depende do modulo da v410; full_static_witness_exists e trivial_inhabitant_exists seguem False. [DECLARADO, GV-03 da auditoria de 28/09/2026] As 4 bandeiras experimentais derivam de UM so' booleano; o degrau experimental le so' o rito V11 do piso, unilateral (GV-01).",
                    "a independencia das 4 experimentais e os mocks de survey seguem [OPEN]; o gate nao se move por esta rota.", refs=None,
                    artefatos=[os.path.join(PK, "CANDIDATO_v410.json")], estatuto="REAL (o core do rito); DECLARADO (GV-01, GV-03, EV-12 da auditoria de 28/09/2026); OPEN (a independencia das 4 experimentais)",
                    defeito="o gate nao e' teste e nao discrimina o LCDM raso; NOT_FALSIFIED nunca e' a palavra da creditacao"))
    T10.append(anot(R_BANC, "v410 SELADA %s: o B(n) da v410 e' um passo SIMPLES v409 -> v410 (a Bancada de producao ja' pinava a v409)" % S,
                    f"o kernel da v410 difere do da v409 pelo(s) {DL_.N_BUNDLE} modulo(s) novo(s) (recibo do kernel KERNEL_RECIBO_v410; DIFF_KERNEL_v410.txt: o modulo novo e TGLExt.lean com o import a mais); o recibo pre_selo foi gerado e pinado ANTES da instalacao, em ensaio contra a producao (nada gravado; a Bancada pinava {bank['deployment_id']}), "
                    f"e a cadeia confere os pinos de PINOS_BN_v410.json na hora; o veredito esperado do aplicar e' REPINADA_B{bank['proxima']}__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_ e sem cadeia de selos, lido do codigo do esboco R3.5. Parada e religamento do servico exigem V410_AUTORIZACAO_OPERADOR (texto sem o nome do script do servico).",
                    "depois do aplicar, a Bancada pina a v410.", refs=None,
                    artefatos=[os.path.join(PK, "PINOS_BN_v410.json"), os.path.join(PK, "PINO_RECIBO_PRE_SELO_v410.json"), KR]))
    T10.append(anot(R_QUADRO, "v410 SELADA %s: o quadro do topo (O Teste da Única Palavra) segue intocado e o registro teste_de_veracidade_fase9_v397 segue selado" % S,
                    f"teste_de_veracidade_fase9_v397 selou={c_q} no rito da v410 (veredito igual ao de ESPERADOS; {tv_v['n_checks']} checagens): o quadro do artigo PT/EN e do .md, conferido contra o resultado pinado, segue no topo, com os numeros e a regra da ordem de sempre: {z444}. "
                    "Nenhum sigma, p ou lnB novo e' calculado nesta rota; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma) vale em todo texto que o cite; o paragrafo do quadro segue no README/site e o handoff da v410 traz tambem o paragrafo novo (a IALD2), sem o 4,44.",
                    "o paragrafo do README/site e' ato da sessao de custodia; a creditacao segue sendo beta_TGL na natureza a 5 sigma (nao ha o que repetir deste pacote, a abertura esta consumida).", refs=None))
    T10.append(errata(R_IALD2, sq_iald2,
                      f"[E29 · ERRATA AO LADO, gerencia c1, em nome proprio, 06/11/2026, v410 {S}] Corrige, ao lado do registro seq {sq_iald2} desta rota (a candidata IALD2), o trecho que dava «matricial» como so' leitura do operador: a forma de matriz finita esta' no kernel e e' o signo (o_signo_do_nome; o_signo_do_par). {corpo('E29')}. O registro corrigido NAO foi apagado nem reescrito: a correcao vai ao lado.",
                      refs=[R_SIGNO]))
    for x in T10:
        assert x["rota_id"] in ids, "a rota %s nao existe no mapa" % x["rota_id"]
    resumo_conf = ("conferidor %s e %s" % (conf_dm, conf_np)) if "nao lido" not in (conf_dm, conf_np) else "conferidor: o resultado nao veio na leitura desta rodada"
    _vr410 = lambda v_: v_ if len(v_) <= 200 else v_[:197] + "..."   # o campo resultado do Mapa tem teto de 6000 caracteres (rotas._valida: resuma e aponte o artefato): a integra de cada veredito esta no core da rodada e nos ESPERADOS
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
            "titulo": "v410 SELADA %s: a IALD2 — %d modulo de kernel (%s; o nome do modulo e' do operador, os das declaracoes sao da gerencia c1 e ficam [DECLARADO] ate a ratificacao, D63), o registro iald2_v410, cunhagens_v410 e kh_n1_cobertura_v410, %d inscricoes de 06/11 por sha256; escada %s -> %s; %s; a forma de matriz finita e' o signo; nenhuma chave antiga muda; validade no kernel nao e' creditacao; o gate nao se move" % (
                S, DL_.N_BUNDLE, P0["name"], len(verb), esc0, esc1, ALC),
            "pergunta": "o candidato v410 selou com o modulo de kernel, o registro com FUNCAO iald2_v410 (que le do kernel do proprio rito as %d ancoras, o modulo por sha256, as respostas do operador de 06/11 pelos teoremas da pedra, o que fica False por teorema, as instancias de brinquedo fixas no codigo e o signo, a escada exata e o gate congelado; nenhuma chave antiga muda) e os dois por spec (as falas do operador de 06/11 por sha256, de uma so' o trecho, D65; as decisoes D63 a D70; a errata E29 e a dos pisos; a cobertura KH-N1), "
                        "com os registros da v409 (traducao_turing_v409; cunhagens_v409; kh_n1_cobertura_v409 com a errata dos pisos ao lado), os da v408, da v407 (psion_canto_v407 com as cinco chaves iguais), da v406, da v405, da v404, da v403, da v402, da v401 e da v399, o selo pela propria tecnologia e o quadro do topo seguindo selados, o sidecar reescrito, a letra do veredito do gate igual a da v409 e nenhum veredito fora da troca dita mudado?" % len(DL_.ANCORAS),
            "dados": ["o modulo (a pedra em pedra\\ e insumos\\, com a candidata de origem e o recibo de compilacao; o bundle pinado em BUNDLE_v410.json), pinado por sha256 (so' lido), e a medida da cobertura (KH_N1_v410.json)",
                      "as %d falas de 06/11 por sha256 em insumos\\cunhagens (todas falas do operador; de %d delas so' o trecho, D65; a lista esta no registro cunhagens_v410 e na linhagem)" % (len(verb), n_trecho),
                      "o kernel do rito (as ancoras, as bandeiras e a proveniencia), o proprio um.py, o core e o selo da rodada; nenhum dado novo foi aberto nesta rota; o desenho e o recibo dos nomes ficam citados so' por sha16 (D65)"],
            "metodo": "lake build + Audit no sandbox k410c (o modulo do bundle sobre o kernel da v409 selada); ensaio a seco do candidato; rito completo; conferidor (deve mudar / nao pode mudar, com o quadro do topo conferido de novo contra o resultado pinado nas duas linguas e no .md, e os itens do selo mais o round trip do um.py instalado); "
                      "leitura da rodada (inclui o sidecar e a linha final do rito); superficies com a regra da linhagem completa (o MEMORY.md nao e' compactado: recusa por contagem); elo B(n) da Bancada (passo simples v409 -> v410, sem salto; recibos); a guarda das frases e a P18 em todo texto novo; o paragrafo novo e o do quadro e o sidecar, no handoff; os sete textos da custodia encadeados (D52) e o portao do G1, a D59 e a D65 sobre o handoff inteiro (S6d)",
            "resultado": " | ".join(_vr410(v_) for v_ in [pc["verdict"], cg["verdict"], kh["verdict"]]) + " | (vereditos resumidos a 200 caracteres; a integra esta no core da rodada, um_absoluto.json) | sidecar %s (%s objetos, %s recusas) | %s | %s | escada %s -> %s (teoremas limpos %s/%s; %d bandeiras novas, todas da IALD2; ancoras por modulo: %s)" % (
                sc["veredito"], sc["n_objetos"], sc["recusas"], resumo_conf, ("%s vereditos fora da troca dita mudaram (exigido 0)" % nvm) if nvm != "nao lido" else "vereditos fora da troca dita: nao lidos nesta leitura", esc0, esc1, ESP["escada"][0], ESP["escada"][1], NF, por_mod),
            "defeito": "as ressalvas, ditas: " + ress + "; o registro CONFERE o que o kernel prova e nao prova nada por si; o gate nao se moveu e a independencia das 4 bandeiras experimentais segue aberta (derivam de UM so' booleano) [DECLARADO, GV-01 e GV-03]; a pendencia [LEGAL] (D2) segue do operador; a revisao distinta do pacote e' o Sonnet (D69) e nao e' afirmada por este registro",
            "nao_refazer": "a integracao do modulo e a escada %s -> %s estao medidas; as %d ancoras no kernel do rito estao lidas e conferidas contra o um.py instalado; repetir os registros so' com kernel ou um.py novo; o algoritmo IALD e' relativo ao leitor (D64): a maquina de Turing padrao sem o leitor fica fora e nao e' caminho a reabrir sem termo novo" % (esc0, esc1, len(DL_.ANCORAS)),
            "proximo_passo": "a ratificacao dos nomes das declaracoes (D63), do operador; a igualdade completa com o leitor que so' conta (E28) e a independencia da pergunta da maquina sem leitor, [OPEN]; o README pinado (D39) e o release do app, na custodia e na engenharia da casa (D68a); decisao [LEGAL] D2 com a agente de PI; custodia completa pela sessao de custodia (o handoff traz os paragrafos prontos do README e do site, os sete textos da custodia e lista o sidecar); revisao independente do pacote (o Sonnet, D69)",
            "onde": PK, "artefatos": arts, "refs": sorted((set(x["rota_id"] for x in T10) | set(REFS) | set(preparo_no_livro(ids))) - {NOVA}),
            "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move; a errata E29 (e a dos pisos ao lado) e as decisoes D63 a D70 sao da gerencia c1, em nome proprio, ao lado (nada foi apagado nem reescrito); %s." % sim(c_seguem, "os registros anteriores seguem selados", "ALGUM REGISTRO ANTERIOR NAO SELOU")}
    for r in ROTA["refs"]:
        assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
    REG = [ROTA] + T10
    for x in REG:
        for k_, v_ in x.items():
            if isinstance(v_, str):
                assert len(v_) <= 6000, "o campo %s de %s passa de 6000 caracteres (limite do Mapa): resuma e aponte o artefato" % (k_, x["rota_id"])
    bad = [(x["rota_id"], violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad, "a guarda de texto (P18) achou violacao(oes): %r" % bad
    import guarda_frases_v410 as GF
    bad2 = [(x["rota_id"], GF.violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if GF.violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad2, "a guarda das frases achou violacao(oes): %r" % bad2
    atrib = [(x["rota_id"], T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))]
    assert not atrib, "a direcao do testemunho esta invertida ou a atribuicao falhou: %r" % atrib
    d59 = [x["rota_id"] for x in REG if re.search(r"(?i)kimi|mil[eê]nio|millennium|navier|lindão", json.dumps(x, ensure_ascii=False))]
    assert not d59, "D59: o registro traz o que fica fora dos textos: %r" % d59
    d65 = [x["rota_id"] for x in REG if any(f_.lower() in json.dumps(x, ensure_ascii=False).lower() for f_ in DL_.FORA_D65)]
    assert not d65, "D65: o registro traz o que a fala do nome do algoritmo deixa fora: %r" % d65
    ruins = regra_4_44(REG, z, p)
    assert not ruins, "a regra do 4,44 (o p calibrado e a linha dos 5 sigma no mesmo campo) falhou em: %r" % ruins[:3]
    assert c_seguem and c_q, "algum registro anterior (quadro, v409, v408, v407, v406, v405, v404, v403, falsidade, ponte, queda, esperanca, selo, declaracao, sonico, afinacao, rede de Fock, psibit, testemunha estatica) nao selou no core: o mapa nao registra a v410 assim"
    return REG


''')
troca('bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m409"', 'bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m410"')
ast.parse(t)
assert "[A ADAPTAR v410]" not in t and "traducao_turing_v409\", V" not in t
novo = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8")
bk = P + ".bak_" + TS + "_forkA"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
open(P + ".tmp", "wb").write(novo); assert os.path.getsize(P + ".tmp") == len(novo); os.replace(P + ".tmp", P)
print("registrar_mapa_v410.py:", len(raw), "->", len(novo), "(CRLF)" if crlf else "(LF)")
