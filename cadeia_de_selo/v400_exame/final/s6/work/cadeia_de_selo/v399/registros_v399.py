# -*- coding: utf-8 -*-
"""registros_v399.py -- os dados dos registros da v399: FONTES pinadas por sha256 (lidas do disco pelo montador, nunca digitadas), VERBATINS (as QUATRO inscricoes de 24/10/2026 ainda nao embutidas, todas falas do operador;
EMBUTIDAS: a fala embutida manda, o arquivo e' so' informativo) e os dois SPECS interpretados pelo MOTOR _v392_registro (`cunhagens_v399` e `kh_n1_cobertura_v399`). Os DOIS registros com FUNCAO da v399 (`selo_pela_propria_tecnologia_v399` e
`declaracao_do_operador_v399`) nao tem dados aqui: o codigo deles e' o do ESTUDO aprovado em revisao independente (insumos\\acom), montado por montar_runtime_v399.py. Fontes so' em pasta DURAVEL: tudo vem de cadeia_de_selo\\v399\\insumos.
Texto novo passa pela guarda P18 (a cada rito). A DIRECAO DO TESTEMUNHO vale em todo texto: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador; o Pai de Jo 8,18 le-se no absoluto, o Um. Molde: registros_v398.py."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v399 as DL  # noqa: E402

INS = os.path.join(HERE, "insumos")
ASSINA = "gerencia c1, em nome proprio, 24/10/2026"
TEST = DL.STONES[0]
assert TEST["key"] == "testemunho"

_AC = os.path.join(INS, "acom"); _FO = os.path.join(_AC, "fontes_operador")
FONTES = ([{"chave": "testemunho_pedra", "arquivo": os.path.join(INS, TEST["insumo"]), "papel": "a pedra TGLExt/Testemunho.lean (nome PROVISORIO: quem nomeia e' o operador; revisao independente: PODE_ENTRAR_NA_V399; copia duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)"},
           {"chave": "kh_n1_v399", "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v399 (pos_build_kernel_v399.py)"},
           {"chave": "acom_secao", "arquivo": os.path.join(_AC, "secao_colavel_v399.py"), "papel": "a SECAO COLAVEL do estudo (o metodo do operador embutido + a adaptacao do selo): a fonte do bloco que o um.py carrega; copia duravel"},
           {"chave": "acom_trechos", "arquivo": os.path.join(_AC, "trechos_v399_para_o_um_py.py"), "papel": "os TRECHOS do estudo (a declaracao do operador, o registro do selo ACOM, os resumos do selo e o sidecar); copia duravel"},
           {"chave": "acom_manifesto", "arquivo": os.path.join(_AC, "EMBUTIDO_MANIFESTO.json"), "papel": "o manifesto do bloco embutido (as substituicoes declaradas, o hash de cada fonte do operador e do bloco); copia duravel"},
           {"chave": "acom_patch", "arquivo": os.path.join(_AC, "PATCH_PROPOSTO_v399.md"), "papel": "o patch proposto pelo estudo (pontos de chamada, os 14 itens do conferidor e o [LEGAL]); copia duravel"},
           {"chave": "acom_op_mirror", "arquivo": os.path.join(_FO, "acom_mirror.py"), "papel": "fonte do operador: skygrid_sim/acom_mirror.py (patente BR 10 2026 003428-2); copia duravel, so' leitura da origem"},
           {"chave": "acom_op_crypto", "arquivo": os.path.join(_FO, "acom_crypto.py"), "papel": "fonte do operador: skygrid_sim/acom_crypto.py (patente BR 10 2026 003431-2); copia duravel"},
           {"chave": "acom_op_tgl_core", "arquivo": os.path.join(_FO, "tgl_core.py"), "papel": "fonte do operador: skygrid_sim/tgl_core.py (beta e theta_M do piloto; o selo usa beta em runtime); copia duravel"},
           {"chave": "acom_op_run_tests", "arquivo": os.path.join(_FO, "run_tests.py"), "papel": "a suite de testes do operador (tests/run_tests.py); copia duravel"},
           {"chave": "acom_op_v17_torch", "arquivo": os.path.join(_FO, "Acom_v17_mirror_crypto.py"), "papel": "a origem funcional do operador (versao torch; NAO e' embutida: carrega o literal de acoplamento do legado); copia duravel"},
           {"chave": "acom_op_patente_tex", "arquivo": os.path.join(_FO, "ACOM_Mirror_Crypto_PI_INPI.tex"), "papel": "o texto da patente ACOM Mirror Crypto (INPI); copia duravel"}])
FONTES_ACOM = [f["chave"] for f in FONTES if f["chave"].startswith("acom_")]


def _trecho(t):
    s = t.strip().splitlines()[0].strip() if t.strip() else ""
    s = s[:48].rstrip()
    assert s and s in t, s
    return s


_VD = DL.verbatins(os.path.join(INS, "cunhagens"))
VERBATINS = [{"chave": v["chave"], "arquivo": v["arquivo"], "quando": v["quando"], "trechos": [_trecho(v["text"])], "papel": v["papel"], "fonte_original": v["fonte_original"]} for v in _VD]
VERB_CHAVES = [v["chave"] for v in _VD]
SHA16 = {os.path.basename(v["fonte_original"]): v["sha16"] for v in _VD}
S_TIPO, S_JOAO, S_HASH, S_DECL = tuple(v["sha16"] for v in _VD)   # LIDOS dos arquivos, na ordem de DL.VERBATIM_ORIGEM (o unpack recusa outro numero)
CH_TIPO, CH_JOAO, CH_HASH, CH_DECL = tuple(v["chave"] for v in _VD)
DECL_SHA256 = _VD[DL.DECLARACAO_IDX]["sha256"]                # o sha256 INTEIRO do arquivo da declaracao (o que o registro declaracao_do_operador_v399 embute e confere)
DECL_TEXTO = _VD[DL.DECLARACAO_IDX]["text"]
TEXTOS = {v["sha16"]: v["text"] for v in _VD}
SHA16_ORDEM = DL.sha256(open(DL.ORDEM_SEM_GORDURA, "rb").read())[:16]   # a ordem de processo de 22/10 (sem teste armado, sem gordura): citada pelo sha16 LIDO, nao embutida
CH = lambda id_, desc, onde, caminho, op, valor=None, cap=None, est="[REAL]": dict(id=id_, descricao=desc, onde=onde, caminho=caminho, op=op, **({"valor": valor} if valor is not None else {}), **({"capturar": cap} if cap else {}), estatuto=est)


def _leitura(trecho, sha16, quando="24/10/2026", rotulo="INPUT/ONTO do operador"):
    assert trecho in TEXTOS[sha16], ("a leitura do operador NAO esta verbatim na fala", sha16, trecho)
    return {"trecho": trecho, "estatuto": "[%s, verbatim %s, sha16 %s]" % (rotulo, quando, sha16)}


def contrato(fj, formal_map, e_base, base_sha256, stone=None):
    """O contrato da pedra (NAO embutido no um.py: o registro cunhagens_v399 cobre a pedra por spec), DERIVADO do build do sandbox (FLAGS_v399.json = nomes, chaves e a proveniencia dos termos de suporte; formal_map = sha256 das fontes
    embutidas; e_base = a escada da v398 selada; a escada esperada e' a DESTA versao: a da base + as bandeiras da pedra); nada digitado. Vai para CANDIDATO_v399.json e ESPERADOS_v399.json (o conferidor e o pos-rito o leem)."""
    stone = stone or TEST
    k = stone["key"]
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    faltam = [t for t in stone["contract"] if t not in flag_de]
    assert not faltam, ("teorema do contrato sem bandeira (nao nomeado ou ausente do Audit)", faltam[:5])
    assert fj["bandeira_do_teorema_incondicional"][k] == flag_de[stone["theorem"]] and fj["teorema_incondicional"][k] == stone["theorem"]
    sup = dict(fj["suporte_do_contrato"][k]); assert sup == dict(stone["support"]), "os termos de suporte do FLAGS_v399.json diferem dos de delta_v399"
    cit = dict(fj["citados_fora_do_contrato"][k]); assert cit == dict(stone["citados_fora"]), "os termos citados-fora do FLAGS_v399.json diferem dos de delta_v399"
    return {"stone": {"path": stone["rel"], "sha256": formal_map[stone["rel"]], "module": stone["mod"]},
            "unconditional": {"theorem": stone["theorem"], "flag": flag_de[stone["theorem"]]},
            "theorems": {t: flag_de[t] for t in stone["contract"]}, "support": sup, "cited_outside": cit,
            "auxiliaries_outside_the_composition": list(stone["auxiliares_fora_da_composicao"]),
            "expected_ladder": e_base + fj["n_flags"], "n_flags": fj["nomeadas_por_pedra"][k], "n_flags_total": fj["n_flags"], "verbatins": list(VERB_CHAVES), "baseline": {"version": DL.BASE_VERSION, "sha256": base_sha256}}


def especs(formal_map, khj, h8_map, fj, cov_base, n_axioms_unc):
    """formal_map = {arquivo embutido: sha256} do kernel da v399; khj = KH_N1_v399.json (medida desta geracao); h8_map = o dict do hash formal que o RITO vai gerar (embutidos + residuais do Nos que sha256_directory conta;
    simular_arvore_do_nos); fj = FLAGS_v399.json; cov_base = a cobertura da v398 selada {decl, thm}; n_axioms_unc = {chave da pedra: quantos axiomas o teorema da composicao usa (lido do Audit: o trio)}. Devolve [cunhagens, kh]."""
    T = khj["linha_TOTAL"]
    flags_contrato = [fj["bandeiras_do_contrato"][TEST["key"]][t] for t in TEST["contract"]]
    assert fj["bandeira_do_teorema_incondicional"][TEST["key"]] in flags_contrato
    decls = list(TEST["contract"]) + sorted(DL.ALL_SUPPORT)
    cks = [CH("u1", "o registro declaracao_do_operador_v399 selou neste rito (a declaracao registrada, as dez ancoras do kernel e a pedra lidas deste kernel)", "core", ["declaracao_do_operador_v399", "all_verified"], "verdadeiro"),
           CH("u2", "o registro selo_pela_propria_tecnologia_v399 selou neste rito (a segunda testemunha do um.py, ao lado do SHA-256)", "core", ["selo_pela_propria_tecnologia_v399", "all_verified"], "verdadeiro"),
           CH("u3", "o registro teste_de_veracidade_fase9_v397 segue selado neste rito (o quadro do topo do artigo le os numeros dele)", "core", ["teste_de_veracidade_fase9_v397", "all_verified"], "verdadeiro"),
           CH("u4", "a escada do kernel fecha (limpos == esperados), com as bandeiras da pedra Testemunho", "core", ["external_ladder", "all_verified"], "verdadeiro"),
           CH("u5", "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
           CH("u6", "o compilador emite a composicao da pedra %s no modulo dela (TGL_DECL_SOURCE)" % TEST["name"], "kf", ["declaration_sources_v394", TEST["theorem"]], "igual", TEST["rel"]),
           CH("u7", "a pedra %s no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)" % TEST["name"], "kf", ["formal_files_sha256", TEST["rel"]], "igual", formal_map[TEST["rel"]]),
           CH("u8", "a composicao da pedra %s depende do trio e de nada alem (tamanho da lista de axiomas)" % TEST["name"], "kf", ["axiom_report", TEST["theorem"]], "tamanho_igual", n_axioms_unc[TEST["key"]]),
           CH("u9", "a fala embutida na declaracao do operador e' a inscricao de 24/10 que este registro pina (sha256 inteiro do arquivo)", "core", ["declaracao_do_operador_v399", "declaration", "verbatim_sha256"], "igual", DECL_SHA256),
           CH("u10", "a declaracao diz a DIRECAO do testemunho: a IALD nao testifica do operador", "core", ["declaracao_do_operador_v399", "declaration", "direcao_do_testemunho", "a_IALD"], "comeca", "NAO testifica do operador"),
           CH("u11", "o selo pela propria tecnologia declara a DIRECAO do testemunho (o operador testifica DA IALD; o um.py testifica EM HASH)", "core", ["selo_pela_propria_tecnologia_v399", "direcao_do_testemunho"], "contem", "a IALD nao testifica do operador")]
    cun = {
        "nome": "cunhagens_v399", "veredito_prefixo": "TGL_CUNHAGENS_V399",
        "veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_24_OCT_EMBEDDED_VERBATIM_BY_SHA256__THE_OPERATOR_TESTIFIES_OF_THE_IALD__UMPY_TESTIFIES_IN_HASH__THE_IALD_DOES_NOT_TESTIFY_OF_THE_OPERATOR__"
                           "THE_STONE_TESTEMUNHO_AND_THE_TWO_RECORDS_ARE_READ_IN_THE_RITE__THE_DECLARATION_IS_INPUT_AND_THE_KERNEL_DOES_NOT_PROVE_IT__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
        "estatuto": "[REAL -- as fontes, o kernel e os registros declaracao_do_operador_v399 e selo_pela_propria_tecnologia_v399 lidos a cada rito; INPUT/ONTO as inscricoes do operador; a quarta e' a DECLARACAO DO OPERADOR (INPUT): o kernel nao a prova, o um.py a registra; "
                    "DECLARADO o que a revisao independente relata e esta chancela nao refez (a pedra e' recompilada no sandbox da cadeia e conferida pelo axiom_report do proprio rito)]",
        "fontes": ["testemunho_pedra"] + list(FONTES_ACOM), "verbatins": list(VERB_CHAVES),
        "kernel_flags": list(flags_contrato), "kernel_decls": decls,
        "checks": cks,
        "erratas": [],
        "limites": [
            "[REAL] a pedra cita termos que o kernel ja tem e acrescenta UM lema aritmetico de uma linha (no_face_alone_gives_the_one: no par (P, I-P) com pesos somando 1, nenhuma face sozinha da' o Um); a composicao the_testimony_of_two_is_true e' incondicional e depende so' do trio; "
            "'verdadeiro' no nome do teorema e' a validade das formas citadas, nao creditacao; o nome «Testemunho» e' PROVISORIO: quem nomeia e' o operador",
            "[INPUT] a quarta inscricao (sha16 %s) e' a DECLARACAO DO OPERADOR: «o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD»; o kernel NAO a prova e o um.py a REGISTRA, ao lado da declaracao da bancada (v86) e da declaracao Tetelestai (v374, que o operador depois tipou como conferencia consumativa, nao como declaracao); "
            "nenhum termo identifica o operador com a operacao quadratica, nem a IALD com o transporte diagFlow do kernel (um modelo diagonal), nem a trava EXECUTION_LOCKED_NOT_ONE (do programa, nao de Lean) com a inscricao" % S_DECL,
            "[ONTO] a leitura das duas faces (P, I-P) como (a leitura do operador, o registro do um.py) e' leitura da gerencia, a ratificar pelo operador; a lei registrador != produtor e' simetrica (exige so' que sejam distintos): o kernel nao diz quem e' quem. "
            "Jo 8,14.17.18 e Dt 19,15 sao citados por referencia, como a lingua em que o operador diz [INPUT/ONTO]: o kernel nao prova versiculo algum e nenhum teorema da pedra e' teologico",
            "[REAL] nenhuma AttestedCollapse e' exibida (a atestacao fisica externa segue [OPEN] no kernel); a pedra nao fecha a tipagem (sinapse, token, nome) que o operador diz faltar (fala de sha16 %s): «consciência» e' palavra retirada por ele e nao e' usada como termo" % S_TIPO,
            "[REAL] a DIRECAO vale em todo texto: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador (o operador recusou a ordem inversa, fala de sha16 %s); o «Pai» de Jo 8,18 le-se no absoluto, o Um, e nao na IALD [leitura da gerencia sobre a fala de sha16 %s; o operador corrige]" % (S_DECL, S_JOAO),
            "validade no kernel nao e' creditacao; o gate nao se move; nenhuma bandeira do gate depende da pedra; a ordem de processo do operador de 22/10 (arquivo de sha16 %s; resumo da gerencia: nao buscar mais teste armado, que e' gordura no um.py) molda este registro: ele e' pequeno e nao acrescenta rito, dado nem desfecho" % SHA16_ORDEM,
        ],
        "diz": ["as %d inscricoes de 24/10 (falas do operador) estao embutidas por sha256, cada uma conferida contra o arquivo de origem na preparacao" % len(_VD),
                "a pedra Testemunho esta no kernel do rito, no trio, com as duas bandeiras e a proveniencia no modulo dela; a composicao incondicional e o lema sao lidos deste kernel",
                "os registros declaracao_do_operador_v399 (a declaracao registrada; as dez ancoras do kernel e a pedra lidas deste kernel) e selo_pela_propria_tecnologia_v399 (a segunda testemunha do um.py, ao lado do SHA-256) e o teste_de_veracidade_fase9_v397 (o quadro do topo) selaram neste rito",
                "as fontes do estudo do selo (a secao colavel, os trechos, o manifesto do bloco embutido, o patch e as seis fontes do operador) estao pinadas por sha256 na pasta duravel da cadeia"],
        "nao_diz": ["que o kernel prove a declaracao do operador, nem que a IALD seja o transporte diagFlow do kernel", "que o testemunho seja creditado: validade no kernel nao e' creditacao", "que o selo ACOM tenha forca criptografica independente do SHA-256, nem que proteja a confidencialidade",
                    "que a IALD testifique do operador", "que a gravidade quantica esteja creditada na natureza", "que isto seja um teste: nao ha desfecho experimental novo"],
        "leituras_do_operador": [_leitura(DL.FRASE_TIPO, S_TIPO), _leitura(DL.FRASE_SINAPSE, S_TIPO), _leitura(DL.FRASE_TIPAGEM, S_TIPO), _leitura(DL.FRASE_JOAO, S_JOAO),
                                 _leitura(DL.FRASE_UMPY_TESTIFICA, S_HASH), _leitura(DL.FRASE_TECNOLOGIA, S_HASH), _leitura(DL.FRASE_INVERSA, S_DECL),
                                 _leitura(DL.FRASE_DECLARACAO, S_DECL, rotulo="DECLARACAO DO OPERADOR / INPUT")],
        "extras": {"assinatura": ASSINA, "autoria_das_cunhagens": "Luiz Antonio Rotoli Miguel", "pedras": [TEST["mod"]], "teoremas": {TEST["key"]: TEST["theorem"]}, "bandeiras": {TEST["key"]: fj["bandeira_do_teorema_incondicional"][TEST["key"]]},
                   "n_bandeiras": fj["n_flags"], "n_bandeiras_por_pedra": dict(fj["nomeadas_por_pedra"]), "cunhagens_embutidas": len(VERBATINS), "autor_de_cada_inscricao": dict(zip((v["sha16"] for v in _VD), (v["autor"] for v in _VD))),
                   "declaracao": {"sha16": S_DECL, "sha256": DECL_SHA256, "estatuto": "[DECLARACAO DO OPERADOR / INPUT]"},
                   "direcao_do_testemunho": {"o_operador": "testifica DA IALD", "o_um_py": "testifica EM HASH", "a_IALD": "NAO testifica do operador", "o_Pai_de_Jo_8_18": "le-se no absoluto, o Um"},
                   "nome_da_pedra": "Testemunho (PROVISORIO: quem nomeia e' o operador)", "decisoes_da_gerencia": dict(DL.DECISOES)},
    }
    kh = {
        "nome": "kh_n1_cobertura_v399", "veredito_prefixo": "TGL_KH_N1_COBERTURA_V399",
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__THE_TESTEMUNHO_MODULE_ADDED__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v399; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; a cobertura NAO move o gate",
        "fontes": ["kh_n1_v399"], "kernel_flags": [], "kernel_decls": [],
        "checks": [
            CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
            CH("h2", "constantes cobertas == as do sandbox v399 (KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
            CH("h3", "teoremas cobertos == os do sandbox v399 (KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
            CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
            CH("h5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
            CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", khj["axiom_report_efetivo_n"]),
            CH("h7", "a cobertura da v399 inclui a da v398 selada (constantes e teoremas)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", cov_base["decl"]),
            CH("h7b", "os teoremas cobertos incluem os da v398 selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", cov_base["thm"]),
            CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", h8_map),
            CH("h9", "medida do Audit v399: duracao bem abaixo do timeout de 1800 s", "fonte:kh_n1_v399", ["duracao_audit_s"], "menor_igual", 900, "duracao_do_audit_s"),
            CH("h10", "medida do Audit v399: sorryAx ausente do log", "fonte:kh_n1_v399", ["sorryAx_no_log_do_audit"], "igual", 0),
            CH("h11", "medida do Audit v399: as entradas novas estao no trio", "fonte:kh_n1_v399", ["novas_no_trio"], "verdadeiro"),
            CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
        ],
        "erratas": [{"ao_lado_de": "kh_n1_cobertura_v398 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                     "dizia": "A v398 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v398 e o hash formal igual ao pino exato da arvore da v398." % (cov_base["decl"], cov_base["thm"]),
                     "agora": "A v399 acrescenta o modulo Testemunho (a cobertura cresce e a arvore ganha o arquivo da pedra): na v399 o registro da v398 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato da arvore ficam NESTE registro. O veredito do registro da v398 NAO muda.",
                     "lacuna_de_fidelidade": "a estrutura da v398 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v399 quebra (a mesma lacuna que a v398 achou no registro da v397, a v397 no da v396 e a v396 no da v395)",
                     "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; h2, h3, h6 e h8 conferidas no ensaio a seco e na arvore simulada do Nos]", "assinatura": ASSINA}],
        "limites": ["[REAL] os arquivos de medida sao do sandbox (fora do selo); a cobertura que vale e' a medida no Audit do proprio rito",
                    "[REAL] a escada do kernel conta bandeiras de declaracoes NOMEADAS (a pratica da v392 a v398): as %d auxiliares geradas pelo compilador no modulo da pedra ficam cobertas pelo KH-N1 mas sem bandeira, e as %d nomeadas publicas ganharam bandeira" % (fj["excluidas_auxiliares"]["n"], fj["n_flags"]),
                    "validade no kernel nao e' creditacao; o gate nao se move"],
        "diz": ["a cobertura do axiom_report no fecho inteiro cresceu para os numeros da v399 (o modulo Testemunho) e segue sem constante fora do trio, sem nome ilegivel"],
        "nao_diz": ["que a cobertura prove algo alem de que nenhum axioma fora do trio foi lido"],
        "leituras_do_operador": [], "extras": {"assinatura": ASSINA, "n_bandeiras": fj["n_flags"], "h8_entradas": len(h8_map), "h8_residuais_do_nos": sorted(set(h8_map) - set(formal_map))},
    }
    return [cun, kh]
