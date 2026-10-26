# -*- coding: utf-8 -*-
# regras (lote E) de derivar_encanamento_v400.py: o CONFERIDOR do rito e o teste do caminho positivo. Escrito pela ferramenta Write.
# O que a v400 muda no conferidor: a base e' a v399 (os nomes da v399 JA estao no core: nenhuma chave nova); NENHUM modulo novo (a pedra Testemunho e' nova so' para a Bancada); a secao do selo ACOM nao define alfa (le SEALED_CODATA_ALPHA);
# o beta do registro e' confrontado com o do core; e dois itens NOVOS, da licao da v399: C15 (as guardas ESTATICAS da Bancada, a funcao ler_nos do esboco pinado, sobre o um.py INSTALADO) e C16 (o mesmo com o Nos REAL inteiro).

_C15 = '''    # C15 [v400, LICAO NOVA]: as guardas ESTATICAS da Bancada (a FUNCAO ler_nos do esboco R3.5 pinado) sobre o um.py INSTALADO: UMA so' linha de alfa e UMA so' de UM_VERSION na coluna 0, nenhuma indentada, e o beta do core == o de runtime (o defeito que recusou a v399)
    _esb = AC.esboco_da_bancada(os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"), "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf")
    import pathlib as _pl
    _sd = os.path.join("C:" + os.sep, "t", "vb17", "conf_%s" % umsha); shutil.rmtree(_sd, ignore_errors=True); os.makedirs(_sd)
    open(os.path.join(_sd, "um.py"), "wb").write(UM_BYTES); json.dump({"um_version": "v400", "sha256": {"um.py": UM_FULL}}, open(os.path.join(_sd, "um_absoluto_selo.json"), "w", encoding="utf-8")); json.dump({"core": {"beta": core.get("beta")}}, open(os.path.join(_sd, "um_absoluto.json"), "w", encoding="utf-8"))
    try:
        _ni = _esb.ler_nos(_pl.Path(_sd), "v400")
        ACOM["C15"] = (bool(_ni["alpha"]["n_linhas_nao_indentadas"] == 1 and _ni["alpha"]["n_reatribuicoes_indentadas"] == 0 and _ni["um_version_linhas"] == {"nao_indentadas": 1, "indentadas": 0}), {"alfa": _ni["alpha"], "beta_rel_diff": _ni["core"]["beta_rel_diff"]})
    except _esb.Recusa as _e:
        ACOM["C15"] = (False, str(_e)[:160])
    finally:
        shutil.rmtree(_sd, ignore_errors=True)
    # C16 [v400]: com o Nos REAL, a funcao ler_nos do esboco aceita o Nos INTEIRO (o selo pina o um.py, o core e o manifesto do kernel; alfa unico; beta do core == runtime): o que o B(n) fara. Na emulacao (V400_NOS) o Nos falso nao tem os pinos reais.
    if os.environ.get("V400_NOS"):
        ACOM["C16"] = (True, "emulacao (V400_NOS): o Nos falso nao tem os pinos reais do core e do manifesto; a leitura inteira so' vale no Nos real")
    else:
        try:
            _nr = _esb.ler_nos(_pl.Path(NOS), "v400")
            ACOM["C16"] = (bool(_nr["um_py"]["sha256"] == UM_FULL and _nr["kernel"] is not None and _nr["alpha"]["n_linhas_nao_indentadas"] == 1), {"kernel_manifesto": (_nr["kernel"] or {}).get("sha256"), "alfa_linha": _nr["alpha"]["linha"], "beta_rel_diff": _nr["core"]["beta_rel_diff"]})
        except _esb.Recusa as _e:
            ACOM["C16"] = (False, str(_e)[:160])
'''

entrada("conferir_rito_v399.py", autoral=True, regras=[
    # a base v399 JA tem os registros da v399: nao-pode-mudar
    ('"cunhagens_regra_v393", "kh_n1_cobertura_v393"]\n', '"cunhagens_regra_v393", "kh_n1_cobertura_v393", "cunhagens_v399", "kh_n1_cobertura_v399", "declaracao_do_operador_v399"]\n', 1),
    ('REL_ = {s["key"]: s["rel"] for s in DL.STONES}', 'REL_ = {s["key"]: s["rel"] for s in DL.STONES_DESDE_B8}   # a pedra Testemunho: nova para a Bancada (v398), nao para a v400', 1),
    # C3: a secao nao define alfa
    ('_permitido = {"hashlib", "math", "time", "np", "ALPHA_FINE_CODATA_2018", "json", "os"}', '_permitido = {"hashlib", "math", "time", "np", "json", "os"}', 1),
    ('ACOM["C3"] = (bool(not _dup and um_c.ALPHA_FINE_CODATA_2018 == um_c.SEALED_CODATA_ALPHA), _dup[:5])',
     'ACOM["C3"] = (bool(not _dup and not hasattr(um_c, "ALPHA_FINE_CODATA_2018") and "ALPHA_FINE_CODATA_2018" not in _rtn and hasattr(um_c, "SEALED_CODATA_ALPHA")), _dup[:5])', 1),
    ("(so' os imports do mesmo modulo e ALPHA_FINE_CODATA_2018, de mesmo valor)", "(so' os imports do mesmo modulo; a secao NAO define ALPHA_FINE_CODATA_2018: le o SEALED_CODATA_ALPHA do programa)", 2),
    # C9: o beta do registro e' confrontado com o do core
    ('um_c.ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)', 'um_c.SEALED_CODATA_ALPHA * math.sqrt(math.e)', 1),
    ('and not AC.literais_de_beta(_RT)), core.get("beta"))',
     'and (SA.get("values") or {}).get("beta_core") == core.get("beta") and (SA.get("values") or {}).get("rel_beta_vs_core") is not None and (SA.get("values") or {}).get("rel_beta_vs_core") < 1e-9 and not AC.literais_de_beta(_RT)), core.get("beta"))', 1),
    ('"C9 beta de runtime (alfa CODATA x raiz de e), nenhum literal de beta no codigo do runtime da v400"', '"C9 beta de runtime (alfa CODATA do programa x raiz de e) == o beta do core do rito a 1e-9 (a checagem do registro deixou de ser tautologica), nenhum literal de beta no codigo do runtime da v400"', 1),
    # C13: o esquema do sidecar nasceu na v399
    ('SC.get("esquema") == "um_absoluto_selo_acom/v1 (v400)"', 'SC.get("esquema") == "um_absoluto_selo_acom/v1 (v399)"', 1),
    ('o sidecar sem recusas, esquema v400, tres objetos', 'o sidecar sem recusas, esquema v399, tres objetos', 1),
    # C15 e C16 (novos)
    ('acom_ok = bool(um_c is not None and all(ACOM.get(k_, (False,))[0] for k_ in ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "round_trip_do_um_py_instalado_independente"))',
     _C15 + 'acom_ok = bool(um_c is not None and all(ACOM.get(k_, (False,))[0] for k_ in ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "C15", "C16", "round_trip_do_um_py_instalado_independente"))', 1),
    ('ACOM.get("C14", (False,))[0],\n',
     'ACOM.get("C14", (False,))[0],\n'
     '    "C15 [v400, licao da v399] as guardas ESTATICAS da Bancada (a funcao ler_nos do esboco R3.5 pinado) sobre o um.py INSTALADO: UMA so\' linha de alfa e UMA so\' de UM_VERSION na coluna 0, nenhuma indentada, beta do core == runtime (o defeito que recusou a v399)": ACOM.get("C15", (False,))[0],\n'
     '    "C16 [v400] com o Nos REAL, a funcao ler_nos do esboco aceita o Nos inteiro (o selo pina o um.py, o core e o manifesto do kernel; alfa unico; beta do core == runtime): o que o B(n) fara": ACOM.get("C16", (False,))[0],\n', 1),
    # o sumario: nenhuma secao nova (a errata e' um paragrafo da secao da v399); o titulo da introducao diz v384 a v400
    ('"o sumario lista as secoes v400, v399, v397 e v396 e o titulo v384 a v39x"', '"o sumario lista as secoes v399, v398, v397 e v396 (a errata da v400 e\' um paragrafo da secao da v399) e o titulo v384 a v400"', 1),
    # kernel: a v400 nao acrescenta modulo
    ('"a escada subiu: %s" % E:', '"a escada e\' a da v399 (a v400 nao acrescenta bandeira): %s" % E:', 1),
    ('"o modulo novo (Testemunho) no kernel do Nos com o sha do candidato (%d modulo)" % len(ESP["pedras_sha256"]): pedras_ok and len(ESP["pedras_sha256"]) == ESP["kernel"]["modulos_novos"] == 1,',
     '"a v400 nao acrescenta modulo ao kernel (%d modulos novos) e a pedra Testemunho (nova para a Bancada) segue no kernel do Nos com o sha pinado" % len(ESP["pedras_sha256"]): pedras_ok and len(ESP["pedras_sha256"]) == ESP["kernel"]["modulos_novos"] == 0 and all(_sha_k(rel) == d_["sha256"] for rel, d_ in ESP["pedras_desde_a_bancada"].items()),', 1),
    # o .md: a linha da errata
    ("carimbo v400 e as linhas «O testemunho de dois (v400)», «Sonico e a afinacao das cordas (v399)»", "carimbo v400 e as linhas «Errata ao lado (v400)», «O testemunho de dois (v399)», «Sonico e a afinacao das cordas (v398)»", 1),
    ('ESP["md_testemunho"] in fc and ESP["md_sonico"] in fc', 'ESP["md_errata"] in fc and ESP["md_testemunho"] in fc and ESP["md_sonico"] in fc', 1),
    # nenhuma chave nova no core
    ('"nenhuma chave nova _v399 fora da lista (so\' selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399 e os registros por spec)": sorted(k for k in core if k not in ESP["vereditos_v399"] and isinstance(core[k], dict) and str(k).endswith("_v399")) == sorted(["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + RN),',
     '"nenhuma chave nova _v399/_v400 no core (a v400 nao cria chave: os registros da v399 sao recriados e iguais, menos o selo ACOM que muda de proposito)": sorted(k for k in core if k not in ESP["vereditos_v399"] and isinstance(core[k], dict) and (str(k).endswith("_v399") or str(k).endswith("_v400"))) == [],', 1),
])

entrada("teste_conferidor_positivo_v399.py", autoral=True)
