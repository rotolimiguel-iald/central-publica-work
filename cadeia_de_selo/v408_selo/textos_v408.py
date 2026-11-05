# -*- coding: utf-8 -*-
# Os TEXTOS da v408 SELADA: TETELESTAI E' O TERMINAL (ordem do operador, 04/11/2026: «liste as pedras que eu preciso nominar e em seguida produza a v408 …»; os nomes das quatro pedras; a regra provar ou podar; a correcao sobre as classes do dicionario, D51 revista). MONTADOS, sem prosa nova de conteudo, do que o core SELADO do rito traz:
# o registro com funcao tetelestai_terminal_v408 (o diz, o nao_diz, os limites, as ressalvas, as ancoras das quatro pedras, as respostas do operador conferidas no kernel, o insumo purgado, os valores), cunhagens_v408 (as 15 falas de 04/11 por sha256, duas de autor misto; as erratas E21 a E23 e a dos pisos; as decisoes D48 a D54, D51 revista; as leituras)
# e kh_n1_cobertura_v408, mais os vereditos, os numeros do kernel (os 4 modulos novos, as bandeiras, a escada) e as falas; so' os conectivos e os titulos sao escritos aqui. A semente fornece a infraestrutura: leitura dos insumos, citacao verbatim, o quadro do Teste da Unica Palavra, a rodada, o sidecar.
# A MOLDURA em toda peca: o terminal e' a leitura, nao o fim do decaimento; nao ha' relacao sem peso; o tempo e' a moeda de beta; validade no kernel nao e' creditacao; o gate nao se move. As RESSALVAS, ditas: o par na face de Fock segue [OPEN] como LIGACAO (E21); P = nP e' teorema nas classes de computacao do dicionario do operador e a traducao as classes das maquinas de Turing e' [OPEN];
# o lock e o Hamiltoniano modular sao objetos distintos; a palavra impedancia fica podada como termo; o insumo do acervo entra pela copia purgada (E23); nenhum teste com a natureza. Toda superficie passa pela guarda das frases (guarda_frases_v408.py) e pela P18 (guarda_p18_v408.py), com a excecao so' da fala do operador.
# O QUADRO «O Teste da Única Palavra» (v397) PERMANECE no topo do artigo PT/EN e do .md canonico, INTOCADO. Cada numero, hash e veredito entra por chave de V (leitura_v408.ler), por ESPERADOS, pelo core do Nos ou e' LIDO de um arquivo aqui, nunca digitado; o que vai escrito a mao e' so' conectivo, titulo, nome de termo (conferido em tempo de execucao no kernel do Nos, no um.py ou no pacote) e frase curta do operador (conferida palavra por palavra contra os bytes das falas).
import hashlib, json, os, re, sys
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V408"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v408 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(PK))          # ...\Central de Patentes\work
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
TOPICO_NOVO = "v408-selada-tetelestai-e-o-terminal.md"
# os marcadores entre os quais o handoff traz os PARAGRAFOS PRONTOS do README do espelho e do site: o QUADRO (v397, intocado) com os MESMOS marcadores da v397, e o paragrafo NOVO da falsidade
MARC_PAR_INI = "<!-- INICIO_PARAGRAFO_README_v397 -->"; MARC_PAR_FIM = "<!-- FIM_PARAGRAFO_README_v397 -->"
_NOMES_KERNEL = ("tetelestai", "o_terminal_e_a_leitura_nao_o_fim_do_decaimento", "basta", "a_poda", "a_quitacao", "o_zero_absoluto_e_do_infinito", "card_chainIdx", "o_tamanho_e_o_custo", "a_inclinacao_modular", "relacao_sem_peso_e_a_origem_da_mentira", "o_um_sozinho_nao_se_mede",
                 "o_tempo_e_a_moeda", "o_pagamento_e_preco_vezes_tempo", "o_ponto_de_contradicao", "o_zero_modular_inscrito_e_o_um", "o_um_nao_e_o_zero_absoluto", "o_habitante_e_o_fock_concreto", "p_igual_np", "p_igual_a_n_vezes_p", "as_classes_do_dicionario",
                 "annihilating_word_exists", "exact_witness_of_annihilating_word", "memory_one_iff_identity", "the_reading_absorbs_the_dephasing", "two_clocks_are_needed", "physicalFockCertificate", "FockCertificate", "BosonicFock")
_MODULOS_KERNEL = ("TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao", "PIgualNP", "PsionCanto", "Par")
_NOMES_UM = ("SEALED_CODATA_ALPHA", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "_V408_TERMINAL_CONTRACT", "_v408_guarda_frases", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "_v407_elo_lido", "_V407_PSION_CONTRACT",
             "fechamento_v406", "_v406_certificado_habitado", "cunhagens_v406", "kh_n1_cobertura_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396",
             "prove_qg_closure_gate", "evaluate_quantum_gravity_closure", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386", "angle_status", "GA_WINDOW_STATUS", "prove_ga_mass_audit", "prove_joint_coincidence_result_v3",
             "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "selo_acom_sidecar_v399", "teste_de_veracidade_fase9_v397", "hubble_ratio_opening_v388", "_v397_quadro_md", "_v397_atomos", "_V397_FRASE_444")
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
_CACHE = {}
# a DIRECAO (v399): nenhuma frase pode por a IALD como quem testifica DO operador (fora da fala em que ele a recusa); a mesma regex do conferidor (C12)
_RX_INV = re.compile(r"IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)")
ERRATA_TEOREMAS = "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"   # (a mesma frase de delta_v408.ERRATA_TEOREMAS_PT; o harness confere)


def _g(d, *ks):
    for k in ks:
        d = (d or {}).get(k) if isinstance(d, dict) else None
    return d


def _kernel_tem(nomes):
    """Fail-closed: cada nome de termo citado aqui tem de existir em algum .lean de TGLExt/ do Nos (lido na hora)."""
    if "kernel" not in _CACHE:
        base = os.path.join(NOS, "tgl_kernel", "TGLExt"); blob = []
        for r, ds, fs in os.walk(base, followlinks=False):
            ds[:] = [d for d in ds if not os.path.islink(os.path.join(r, d))]
            for f in fs:
                if f.endswith(".lean"):
                    blob.append(open(os.path.join(r, f), encoding="utf-8", errors="replace").read())
        _CACHE["kernel"] = "\n".join(blob)
    for n in nomes:
        assert n in _CACHE["kernel"], "termo citado nao esta no kernel do Nos: %s" % n


def _modulos_tem(nomes):
    """Cada modulo citado existe como arquivo .lean em TGLExt/ (os 4 da v408 e os 9 da v407) ou em TGLExt/F1Fecho394/ (os 301 da v406) do Nos."""
    for n in nomes:
        assert any(os.path.isfile(os.path.join(NOS, "tgl_kernel", "TGLExt", *p, n + ".lean")) for p in ((), ("F1Fecho394",))), "modulo citado nao esta no kernel do Nos: %s" % n


def _um_tem(nomes):
    """Cada identificador do um.py citado aqui existe no um.py do Nos (lido na hora)."""
    if "um" not in _CACHE:
        _CACHE["um"] = open(os.path.join(NOS, "um.py"), encoding="utf-8", errors="replace").read()
    for n in nomes:
        assert n in _CACHE["um"], "identificador citado nao esta no um.py do Nos: %s" % n


def _conferir_nomes():
    if "nomes_ok" not in _CACHE:
        _kernel_tem(_NOMES_KERNEL); _modulos_tem(_MODULOS_KERNEL); _um_tem(_NOMES_UM)
        _CACHE["nomes_ok"] = True


# ---------------------------------------------------------------- leitura dos insumos, do ESPERADOS e do core (tudo por script; nenhum numero, hash ou citacao vem da memoria)
def _esp():
    """ESPERADOS_v408.json (gerado pelo ensaio a seco do candidato), lido uma vez."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v408.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _core():
    """O core do Nos (so' leitura), para os campos que so' existem depois do rito; ausente e' falha visivel."""
    if "core" not in _CACHE:
        _CACHE["core"] = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["core"]


def _base_core():
    """O core da v407 selada (a copia de bytes em base_v407): de onde saem os numeros da errata ao lado e a medida da proveniencia."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v407", "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["base_core"]


def _qd():
    """O modulo quadro_v397 (da pasta do pacote, copia intocada): as MESMAS funcoes que o artigo, o .md e o paragrafo do README/site usam para o quadro do Teste da Unica Palavra."""
    if "qd" not in _CACHE:
        if PK not in sys.path:
            sys.path.insert(0, PK)
        import quadro_v397 as QD
        _CACHE["qd"] = QD
    return _CACHE["qd"]


def _res_path(esp):
    """O resultado pinado do Teste da Unica Palavra: a copia em PK/insumos/fase9 (so' existe no SANDBOX do harness) ou, no real, a copia duravel da v397 (ESPERADOS[veracidade][resultado][duravel]); o sha256 e' conferido contra ESPERADOS."""
    nome = os.path.basename(esp["veracidade"]["resultado"]["duravel"])
    loc = os.path.join(PK, "insumos", "fase9", nome)
    return loc if os.path.exists(loc) else esp["veracidade"]["resultado"]["duravel"]


def _atomos():
    """Os atomos numericos do quadro (PT) sobre o registro SELADO no core do Nos: o menos de verdade e a virgula decimal ja vem dentro; recusa se o registro nao selou."""
    a = _qd().Q._v397_atomos(_core().get("teste_de_veracidade_fase9_v397") or {}, "pt")
    assert a["sealed"] is True, "o registro teste_de_veracidade_fase9_v397 nao sela no core do Nos (algum numero ausente ou all_verified falso): nenhum texto diz o 4,44 assim"
    return a


def _z444():
    """A clausula-padrao do 4,44, USADA toda vez que o numero entra num texto: o z_disc, o p calibrado e a linha dos 5 sigma na mesma frase (regra da ordem do operador)."""
    a = _atomos()
    return "z_disc = %s (calibrado; p unilateral %s), abaixo do degrau de 5σ da creditação, que não foi alcançado (%s < 5)" % (a["z_disc"]["md"], a["p_disc"]["md"], a["z_disc"]["md"])


def _falas():
    """As inscricoes de 04/11 embutidas no um.py: o texto vem do arquivo em insumos/cunhagens e o sha256 e' conferido contra ESPERADOS (fail-closed). Devolve {sha16: {sha16, arquivo, nome, text, autor, misto, autor_do_arquivo}}.
    Nas duas de AUTOR MISTO (operador + outra instancia da IALD [DECLARADO]) a chave e' o sha16 do ARQUIVO INTEIRO e o texto embutido (e o unico citavel) e' o PARAGRAFO DO OPERADOR (o arquivo .paragrafo_do_operador.txt,
    conferido contra ESPERADOS[cunhagens][..][sha256]; o arquivo inteiro contra sha256_arquivo_inteiro): por isso `autor` e' 'operador' (o texto citavel e' so' dele) e `autor_do_arquivo` diz o autor do arquivo. Nenhuma e' da gerencia."""
    if "falas" not in _CACHE:
        ec = _esp()["cunhagens"]; out = {}; pasta = os.path.join(PK, "insumos", "cunhagens"); suf = ".paragrafo_do_operador.txt"
        for k, meta in ec.items():
            s = k[len("v408_cun_"):]
            misto = bool(meta.get("sha256_arquivo_inteiro"))
            fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(s + "_") and (f.endswith(suf) if misto else not f.endswith(suf))]
            assert len(fs) == 1, ("a inscricao %s nao tem arquivo unico em insumos/cunhagens" % s, fs)
            b = open(os.path.join(pasta, fs[0]), "rb").read()
            assert hashlib.sha256(b).hexdigest() == meta["sha256"] and len(b) == meta["bytes"], "a inscricao %s nao confere com o sha256 de ESPERADOS" % s
            if misto:
                bi = open(os.path.join(pasta, fs[0][:-len(suf)]), "rb").read()
                assert hashlib.sha256(bi).hexdigest() == meta["sha256_arquivo_inteiro"] and meta["sha256_arquivo_inteiro"][:16] == s, "o arquivo inteiro da inscricao de autor misto %s nao confere com ESPERADOS" % s
                nome = fs[0][len(s) + 1:-len(suf)]
            else:
                assert meta["sha256"][:16] == s, "a chave da inscricao %s nao e' o sha16 do arquivo" % s
                nome = fs[0][len(s) + 1:]
            assert nome.startswith("OPERADOR_04nov_") and not str(meta.get("papel", "")).startswith("leitura da gerencia"), ("a v408 nao tem inscricao da gerencia: todas sao falas do operador (duas de autor misto)", s)
            out[s] = {"sha16": s, "arquivo": fs[0], "nome": nome, "text": b.decode("utf-8"), "autor": "operador", "misto": misto, "autor_do_arquivo": meta.get("autor") or "operador"}
        assert sum(1 for d in out.values() if d["misto"]) == 2, "a v408 tem exatamente duas inscricoes de autor misto"
        _CACHE["falas"] = out
    return _CACHE["falas"]


def _sha_por(sub):
    """O sha16 da unica inscricao cujo arquivo de origem contem `sub` (as inscricoes sao achadas assim, nunca digitadas)."""
    r = [s for s, d in _falas().items() if sub in d["nome"]]
    assert len(r) == 1, ("inscricao nao unica ou ausente", sub, r)
    return r[0]


def _cita(trecho):
    """Fail-closed: o trecho tem de estar numa das falas DO OPERADOR, palavra por palavra e na mesma ordem; devolve «trecho». Citacao fora dos bytes derruba a geracao.
    So' uma coisa e' relevada: uma quebra de linha ou um espaco duplo do ARQUIVO vale como um espaco; o trecho citado nunca tem espaco duplo nem quebra."""
    assert "\n" not in trecho and "  " not in trecho, "o trecho citado tem quebra de linha ou espaco duplo"
    corpus = [re.sub(r"\s+", " ", d["text"]) for d in _falas().values() if d["autor"] == "operador"]
    assert any(trecho in t for t in corpus), "citacao fora dos bytes das falas do operador: %r" % trecho[:70]
    return "«" + trecho + "»"


def _um_texto_tem(frase):
    """A frase do KERNEL embutido no um.py do Nos (a docstring do 0_abs, sem a marca de negrito): fail-closed."""
    if "um" not in _CACHE:
        _CACHE["um"] = open(os.path.join(NOS, "um.py"), encoding="utf-8", errors="replace").read()
    assert frase in _CACHE["um"].replace("**", ""), "a frase do kernel nao esta no um.py do Nos: %r" % frase[:70]
    return "«" + frase + "»"


def _frase_444():
    """A frase do operador do quadro (v397), VERBATIM, conferida contra os bytes do arquivo da v397 (pelo sha16 que ESPERADOS[quadro] registra): devolve «frase»."""
    if "f444" not in _CACHE:
        esp = _esp(); frase = esp["quadro"]["frase_do_operador"]; h = esp["quadro"]["frase_sha16"]
        pasta = os.path.join(WK, "cadeia_de_selo", "v397", "insumos", "cunhagens")
        fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(h + "_")]
        assert len(fs) == 1, ("o arquivo da fala do 4,44 nao e' unico em v397\\insumos\\cunhagens", fs)
        b = open(os.path.join(pasta, fs[0]), "rb").read()
        assert hashlib.sha256(b).hexdigest()[:16] == h and frase in re.sub(r"\s+", " ", b.decode("utf-8")), "a frase do 4,44 nao esta nos bytes da fala pinada"
        assert frase == _qd().DL.FRASE_DO_OPERADOR_4_44 == _qd().Q._V397_FRASE_444, "a frase do quadro != a verbatim"
        _CACHE["f444"] = frase
    return "«" + _CACHE["f444"] + "»"


def _data_fala(d, V):
    m = re.match(r"(?:OPERADOR|GERENCIA)_(\d{2})(out|nov)_", d["nome"])
    assert m, ("o nome do arquivo da inscricao nao traz a data", d["nome"])
    return "%s/%s/%s" % (m.group(1), "10" if m.group(2) == "out" else "11", V["data"][-4:])


def _cov_base():
    """A cobertura do Audit e a arvore formal da v407 selada (o core guardado em base_v407): de onde saem os numeros da errata ao lado dos pisos."""
    if "cov_base" not in _CACHE:
        kf = _base_core()["kernel_formalization"]
        cov = kf["axiom_coverage_v392"]
        _CACHE["cov_base"] = {"decl": cov["decl"], "thm": cov["thm"], "h8": len(kf["formal_files_sha256"]), "axr": len(kf["axiom_report"])}
    return _CACHE["cov_base"]


def _bancada():
    """A geracao do manifesto que a Bancada de producao pina (do recibo pre_selo pinado em PINOS_BN) e a versao que ela pina; o passo e' simples (sem salto e sem cadeia de selos)."""
    p = json.load(open(os.path.join(PK, "PINOS_BN_v408.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v407" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v407 -> v408 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1}


def _proveniencia(esp):
    """A proveniencia que o compilador emite atribui ao modulo da pedra N declaracoes; todas sao NOVAS no axiom_report (nenhuma reatribuida), e o FLAGS_v408.json do sandbox concorda (as contagens de
    publicas, privadas, nomeadas e auxiliares so' existem la')."""
    if "prov" not in _CACHE:
        kf = _core()["kernel_formalization"]; src = kf["declaration_sources_v394"]; pedras = set(esp["bundle_sha256"])
        b0 = _base_core()["kernel_formalization"]; axr0 = b0["axiom_report"]
        mine = sorted(n for n, p in src.items() if p in pedras)
        novas = [n for n in mine if n not in axr0]
        fj = json.load(open(os.path.join(PK, "kernel", "FLAGS_v408.json"), encoding="utf-8"))
        assert len(mine) == fj["decl_totais_modulos_novos"] and len(novas) == fj["decl_novas_dos_modulos"] == len(mine) and not fj["reatribuidas_as_pedras"], ("a proveniencia do rito != FLAGS_v408.json do sandbox", len(mine), len(novas), fj["reatribuidas_as_pedras"])
        assert fj["publicas_no_modulo"] + fj["privadas_no_modulo"] == len(mine) and fj["n_flags"] + fj["excluidas_auxiliares"]["n"] == fj["publicas_no_modulo"], "as contagens de publicas, privadas, nomeadas e auxiliares nao fecham"
        assert len(kf["axiom_report"]) - len(axr0) == len(novas), "o axiom_report nao cresceu exatamente pelas declaracoes novas"
        _CACHE["prov"] = {"mod": len(mine), "novas": len(novas), "pub": fj["publicas_no_modulo"], "priv": fj["privadas_no_modulo"], "axr0": len(axr0), "axr1": len(kf["axiom_report"])}
    return _CACHE["prov"]


# ---------------------------------------------------------------- formatacao de numeros (virgula decimal; nenhum numero e' digitado: todos chegam por V)
def _p(x, nd=None):
    x = float(x)
    return (repr(x) if nd is None else "%.*f" % (nd, x)).replace(".", ",")


def _pn(x, nd=6):
    """Numero lido do core, em PT: inteiro sem casas (2.0 -> 2); senao `nd` casas com virgula."""
    x = float(x)
    return str(int(x)) if x.is_integer() else _p(x, nd)


def _f(texto, **kw):
    """str.format com conferencia: nenhuma chave sobra e nenhuma chave de chave sobra no resultado."""
    r = texto.format(**kw)
    assert "{" not in r and "}" not in r, ("chave de formatacao sobrou", r[:80])
    return r


def _d(V):
    """Os numeros da v408, todos LIDOS (V da leitura da rodada, ESPERADOS, core do Nos, base v407, os registros): nenhum e' digitado aqui. Recusa se as contagens nao fecham."""
    _conferir_nomes()
    esp = _esp(); tv = V["veracidade"]; sa = V["selo"]; dc = V["declaracao"]; sc = V["sidecar"]; core = _core(); gt = V["gate"]; gv = gt["values"]; fb = V["f2b"]
    DL_ = _dl(); pc = _pc(); cg = _cg(); khr = _khr(); fh = _fe_herdado(); ph = _ps_herdado(); pv = pc["values"]
    mods = sorted(DL_.BUNDLE_MODS)
    assert V["n_pedras"] == len(mods) == esp["kernel"]["modulos_novos"] == DL_.N_BUNDLE == pv["n_modulos"], ("o delta da v408 e' o bundle dos 4 modulos novos, cada um com o sha256 pinado", len(mods))
    for rel in DL_.BUNDLE_RELS:
        p = os.path.join(NOS, "tgl_kernel", *rel.split("/"))
        assert os.path.isfile(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() == esp["bundle_sha256"][rel] == DL_.BUNDLE_POR_REL[rel]["sha256"], "o modulo %s no Nos != o sha256 pinado" % rel
    nf = esp["n_bandeiras_novas"]; grp = esp["n_bandeiras_por_grupo"]
    assert grp == {DL_.GRUPO_BUNDLE: nf} and nf == esp["politica_de_bandeiras"]["n_flags"] == len(esp["bandeiras_novas_chaves"]) == pv["n_flags_true"], "as bandeiras novas nao sao so' as do terminal, ou nem todas sao True"
    if V.get("bandeiras") is not None:
        assert V["bandeiras"]["n"] == V["bandeiras"]["n_true"] == nf and V["bandeiras"]["ok"] is True, "a leitura da rodada nao confirma as bandeiras novas True"
    assert fb["sealed"] is True and fb["status_agora"] == DL_.D4.F2B_FUTURO_TOKEN, "o registro f2b_errata_v404 recriado nao e' o selado"
    assert gt["sealed"] is True and gt["f81_ok"] is True and gt["n18"] == 18 and gt["n_checks"] == DL_.D3.N_CHECKS["gate"], "o registro bandeiras_do_gate_v403 recriado nao e' o selado"
    assert gv["n_flags"] == 18 == gv["n_true"] == gv["n_calculated"] and gv["n_literal"] == 0 and gv["n_read_by_the_verdict"] == 15 and gv["read_by_the_verdict"] == [6, 5, 4] and gv["gate_verdict_equals_v402"] is True and gv["ext_ls2_n"] == gt["n_ls2"] == 6 and gt["sonda"] == 1, "as bandeiras do gate nao fecham: 18 calculadas, 0 literais, 15 no veredito"
    fl = _falas(); n_op = len(fl); chaves_ = {"v408_cun_" + s_ for s_ in fl}
    assert n_op == len(DL_.VERBATIM_ORIGEM_V408) == len(esp["cunhagens"]) == len(cg["verbatim"]) and set(pc["inscriptions"]) <= chaves_ and all(v_ is True for v_ in pc["inscriptions"].values()), "o numero de inscricoes mudou (ler DL.VERBATIM_ORIGEM_V408 e ESPERADOS[cunhagens])"
    n_misto = sum(1 for d_ in fl.values() if d_["misto"])
    ss = {"ordem": _sha_por(DL_.N_ORDEM_V408), "nomes": _sha_por(DL_.N_NOMES), "sentido": _sha_por(DL_.N_SENTIDO_PNP), "classes": _sha_por(DL_.N_CLASSES_PNP), "claro": _sha_por(DL_.N_CLARO_V408), "ratificado": _sha_por(DL_.N_RATIFICADO), "regra": _sha_por(DL_.N_TETELESTAI)}
    assert all(ss[k_] == DL_.VERBATIM_PREFIXOS_DA_ORDEM_V408[n_] for k_, n_ in (("ordem", DL_.N_ORDEM_V408), ("nomes", DL_.N_NOMES), ("sentido", DL_.N_SENTIDO_PNP), ("classes", DL_.N_CLASSES_PNP), ("claro", DL_.N_CLARO_V408), ("ratificado", DL_.N_RATIFICADO), ("regra", DL_.N_TETELESTAI))), "os sha16 das falas != os que a ordem da gerencia deu"
    rec = _recriados(); n_rec = {ver: len(ns) for ver, ns in rec.items()}; n13, n9, n301 = _pedras_anteriores()
    assert n13 == len(esp["pedras_v405_sha256"]) and n9 == DL_.D7.N_BUNDLE and n301 == DL_.D6.N_BUNDLE, ("as pedras seladas anteriores nao sao as de ESPERADOS e os bundles da v407 e da v406", n13, n9, n301)
    assert sa["ok"] is True and sa["n_checks"] == esp["selo_acom"]["n_checks"] and sa["checks_ok"] is True and sa["values_ok"] is True and sa["beta_ok"] is True, "o registro selo_pela_propria_tecnologia_v399 do core nao e' o contrato de ESPERADOS"
    assert dc["ok"] is True and dc["n_checks"] == esp["declaracao"]["n_checks"] and dc["checks_ok"] is True and dc["ancoras_ok"] is True and dc["direcao_ok"] is True, "o registro declaracao_do_operador_v399 do core nao e' o contrato de ESPERADOS"
    assert sc["ok"] is True and sc["n_objetos"] == len(esp["sidecar"]["objetos"]) and sc["recusas"] == 0, "o sidecar um_absoluto_selo_acom.json nao e' o de ESPERADOS"
    assert tv["ok"] is True and tv["n_checks"] == esp["veracidade"]["n_checks"] and tv["checks_ok"] is True and tv["numeros_ok"] is True and tv["fontes_ok"] is True, "o registro teste_de_veracidade_fase9_v397 do core nao e' o contrato de ESPERADOS (o quadro do topo le os numeros dele)"
    dts = {re.match(r"(?:OPERADOR|GERENCIA)_(\d{2}(?:out|nov))_", f["nome"]).group(1) for f in fl.values()}
    assert dts == {"04nov"}, ("o nome de arquivo de alguma inscricao nao e' de 04/11", dts)
    qd = _qd(); a = _atomos()
    assert qd.Q._v397_linha_de_maquina(a, "pt") == esp["quadro"]["linha_de_maquina_pt"], "a linha de maquina do quadro (core) != a de ESPERADOS"
    assert esp["quadro"]["frase_do_operador"] == qd.DL.FRASE_DO_OPERADOR_4_44 == qd.Q._V397_FRASE_444, "a frase do operador do quadro != a verbatim"
    base = os.path.join(PK, "base_v407", "um.py")
    if "base_b" not in _CACHE:
        assert s16(base) == V["base16"], "base_v407/um.py nao e' a v407 selada"
        _CACHE["base_b"] = os.path.getsize(base)
    delta = V["umb"] - _CACHE["base_b"]
    kf = core.get("kernel_formalization") or {}; prov = kf.get("declaration_sources_status_v394") or {}
    assert prov.get("ok") is True and prov.get("compiler_names") == prov.get("audited_names") == V["axiom_report_n"], "a proveniencia emitida pelo compilador nao cobre o axiom_report do rito"
    assert V["n_ver_mudaram"] == 0, "algum veredito fora da troca dita mudou: nao ha texto a escrever"
    assert V["n18"] == 18 and all(i in V["patch_ids"] for i in _ESCADA_PATCHES), "o gate nao tem as 18 bandeiras True, ou o candidato nao traz os patches que chamam o terminal (N00), o resumo no selo (N02), o runtime (W02), os pisos dos registros da v407 com a E21 (C13) e os 4 modulos (K01)"
    assert esp["h8_entradas"] > len(esp["h8_residuais_do_nos"]) >= 1, "a arvore formal do rito tem de ser as embutidas mais os residuais do Nos"
    assert khr["lido"]["constantes_cobertas"] == V["kh"]["decl"] and khr["lido"]["teoremas_cobertos"] == V["kh"]["thm"], "a cobertura do registro kh_n1_cobertura_v408 != a leitura da rodada"
    pv_ = _proveniencia(esp)
    aa = _g(core, "neutrino_mass", "angle_status"); assert aa and hashlib.sha256(str(aa).encode("utf-8")).hexdigest() == esp["neutrino_angle_status_antigo_sha256"] and str(aa).startswith(DL_.ANGLE_STATUS_ANTIGO_PREFIXO), "o texto antigo de neutrino_mass.angle_status nao esta intacto no core do Nos"
    return {"n_f": nf, "n_aux": esp["politica_de_bandeiras"]["n_excluidas"], "depois": V["teor"].split("/")[0], "delta": delta, "pct": ("%.1f" % (100.0 * delta / _CACHE["base_b"])).replace(".", ","), "prov": prov["compiler_names"], "n_cun": len(V["verbatins"]), "n_op": n_op, "n_misto": n_misto,
            "h8": esp["h8_entradas"], "h8_emb": esp["h8_entradas"] - len(esp["h8_residuais_do_nos"]), "h8_res": ", ".join("`%s`" % x for x in esp["h8_residuais_do_nos"]), "n_res": len(esp["h8_residuais_do_nos"]), "cb": _cov_base(), "bank": _bancada(), "pv": pv_,
            "n_checks_v": tv["n_checks"], "n_ck_sel": sa["n_checks"], "n_ck_dec": dc["n_checks"], "n_ck_cun": len(cg["checks"]), "n_ck_pc": pc["mechanics"]["n_checks"], "n_ck_ps": ph["mechanics"]["n_checks"], "n_ck_fe": fh["mechanics"]["n_checks"], "n_anc": len(DL_.ANCORAS),
            "n_resp": len(pv["respostas"]), "n_insc": len(pc["inscriptions"]), "f8": {k: v[:8] for k, v in esp["veracidade"]["fontes"].items()},
            "ss": ss, "n_rec": n_rec, "n13": n13, "n9": n9, "n301": n301, "data_falas": "04/11/" + V["data"][-4:],
            "g": {"n_flags": gv["n_flags"], "n_true": gv["n_true"], "n_calc": gv["n_calculated"], "n_lit": gv["n_literal"], "n_ver": gv["n_read_by_the_verdict"], "rv": gv["read_by_the_verdict"], "info": list(gv["informative"]), "ls2": gv["ext_ls2_n"], "n_chk": gv["n_gate_checks"], "n_chk_reg": gt["n_checks"], "feed": list(DL_.F81_FEED)}}


def _mods(V):
    """Onde moram os modulos novos (os 4 estao em TGLExt/), com os nomes que o operador deu em 04/11 (lidos de delta_v408)."""
    ns = [p_["name"] for p_ in _dl().PEDRAS_V408]
    return "em `TGLExt`: %s, os quatro com o nome que o operador deu em 04/11" % ", ".join("`%s`" % n_ for n_ in ns)


def _extras(V):
    # os registros novos ALEM DOS TRES FIXOS (V["registros_novos"] tem os tres: o tetelestai_terminal com funcao e os dois por spec), ditos pelo nome
    DL_ = _dl(); fixos = [DL_.FECHO_REGISTRO, DL_.CUNHAGENS_REGISTRO, DL_.KH_REGISTRO]
    ex = [k for k in V["registros_novos"] if k not in fixos]
    return (", ".join("`%s`" % k for k in ex)) if ex else "nenhum além dos três fixos"


def _cab(V):
    return "v408 SELADA (COMPLETA)** `%s`" % V["s16"]


def _num(V, verdicts=True):
    """O paragrafo dos numeros da v408 (kernel, o registro com funcao, os registros por spec, os recriados, o sidecar, a troca dita): usado na linhagem, no Atlas, no core, no topico novo, no verbete e no handoff."""
    d = _d(V); kh = V["kh"]; sc = V["sidecar"]; sa = V["selo"]; g = d["g"]; pc = _pc(); pv = pc["values"]; esp = _esp(); DL_ = _dl()
    vd = (lambda k: " (%s)" % esp["vereditos_novos_v408"][k]) if verdicts else (lambda k: "")
    aux = ("nenhuma auxiliar gerada pelo compilador ficou de fora" if not d["n_aux"] else "%d auxiliares geradas pelo compilador ficam sem bandeira" % d["n_aux"])
    kern = _f("o kernel ganhou {n_pedras} módulos novos ({mods}; os {n_pedras} são da gerência c1, compilados no sandbox da v408), com {n_f} bandeiras novas True, só de declaração nomeada ({aux}), e escada {antes} → {depois} teoremas limpos "
              "({axr} declarações no `axiom_report`, {fora} fora do trio, {nl} nomes não lidos; a proveniência de cada declaração emitida pelo compilador cobre as mesmas {prov}); "
              "errata ao lado da v394, mantida (em nome próprio da gerência c1): " + ERRATA_TEOREMAS,
              n_pedras=V["n_pedras"], mods=_mods(V), n_f=d["n_f"], aux=aux, antes=V["escada_antes"], depois=d["depois"], axr=V["axiom_report_n"], fora=kh["fora"], nl=kh["nao_lidas"], prov=d["prov"])
    fech = _f("o registro `tetelestai_terminal_v408`{vd} (o único registro novo com função): lê do kernel do próprio rito as {na} âncoras, os {nm} módulos por sha256, as {nb} bandeiras, as {nr} respostas do operador de 04/11 pelos teoremas que já existiam e pelas declarações novas, as {ni} falas do contrato por sha256, o insumo do acervo pela cópia purgada, "
              "o que fica False por teorema, a escada exata ({esc}) e o gate (o mesmo da v407); nenhuma chave antiga muda; {nck} checagens, todas passaram",
              vd=vd(DL_.FECHO_REGISTRO), na=pv["n_ancoras_ok"], nm=pv["n_modulos_ok"], nb=pv["n_flags_true"], nr=d["n_resp"], ni=d["n_insc"], esc=" = ".join(str(x) for x in dict.fromkeys(pv["escada"])), nck=d["n_ck_pc"])
    cun = _f("o registro `cunhagens_v408`{vd}: as {n} falas de 04/11 embutidas por sha256 e consumidas no rito ({nop} falas do operador e {nm} de autor misto, operador e outra instância da IALD [DECLARADO], das quais só o parágrafo do operador é embutido e citável; nenhuma é da gerência); "
             "as erratas E21 a E23 e a dos pisos (em nome próprio da gerência c1); as decisões D48 a D54 (a D51 revista pela correção do operador: {d51}); as leituras pela regra provar ou podar e as ressalvas ({nck} checagens, todas passaram)",
             vd=vd(DL_.CUNHAGENS_REGISTRO), n=d["n_cun"], nop=d["n_op"] - d["n_misto"], nm=d["n_misto"], d51=_d51(), nck=d["n_ck_cun"])
    khs = _f("o registro `kh_n1_cobertura_v408`{vd}: {decl} constantes, {thm} teoremas, {fora} fora do trio, {nl} nomes não lidos; a árvore formal do Nós depois do rito tem {h8} entradas ({emb} embutidas mais {nres} residual do Nós: {res}), "
             "e o pino h8 do registro é o hash dessa árvore, calculado por script sobre a árvore simulada do Nós na geração do candidato",
             vd=vd(DL_.KH_REGISTRO), decl=kh["decl"], thm=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"], h8=d["h8"], emb=d["h8_emb"], nres=d["n_res"], res=d["h8_res"])
    nr = d["n_rec"]; muda = ", ".join("`%s`" % x for x in esp["selo_chaves_que_mudam"]) or "nenhum"
    rec = _f("os registros da v407 (`psion_canto_v407`, `cunhagens_v407`, `kh_n1_cobertura_v407`: {n7} no total), os da v406 (`fechamento_v406`, `cunhagens_v406`, `kh_n1_cobertura_v406`: {n6}), os {n5} da v405, os {n4} da v404, os {n3} da v403, os da v402, da v401 e da v399 são recriados no mesmo ponto do main e seguem selados; os que mudam de conteúdo no selo são os ditos: {muda}; "
             "nenhum veredito deles muda de prefixo, e a errata E21 vai AO LADO do `psion_canto_v407` (o texto selado não é reescrito); "
             "as {n13} pedras seladas da v403, da v404 e da v405, os {n9} módulos da v407 e os {n301} módulos da v406 seguem no kernel do Nós com o sha256 selado, como registro; "
             "o gate não se moveu: o `qg_closure` do core é idêntico ao da v407 (as {n18} bandeiras, os sete checks e a letra do veredito); "
             "o selo pela própria tecnologia sela os {bytes} bytes do `um.py` v408 ao lado do SHA-256 (perfil `{perfil}`, {nctl} controles negativos recusados), e o sidecar `um_absoluto_selo_acom.json` (arquivo da custódia desde a v399, reescrito pelo rito; sha256 `{sc16}`, veredito `{sv}`, {nr} recusas) lista os {no} objetos finais",
             n7=nr["407"], n6=nr["406"], n5=nr["405"], n4=nr["404"], n3=nr["403"], muda=muda, n13=d["n13"], n9=d["n9"], n301=d["n301"], n18=g["n_flags"], bytes=format(sa["bytes"], ","), perfil=sa["perfil"], nctl=sa["n_controles"], sc16=sc["sha16"], sv=sc["veredito"], nr=sc["recusas"], no=sc["n_objetos"])
    ex = _extras(V)
    resto = _f("{ex}; o registro `teste_de_veracidade_fase9_v397` segue selado e igual (o quadro do topo do artigo lê os números dele); troca dita (só números: os vereditos que carregam a escada, as declarações ou a contagem de arquivos do kernel): {troca}; nenhuma mudança NÃO numérica: {nm} vereditos fora da troca dita mudaram (exigido: 0); validade no kernel não é creditação",
               ex=("nenhum registro novo além dos três fixos" if ex.startswith("nenhum") else "registros novos além dos três fixos: " + ex), troca=", ".join("`%s`" % x for x in V["troca_dita"]), nm=V["n_ver_mudaram"])
    return "; ".join([kern, fech, cun, khs, rec, resto])


def _cunhagens(V, forma="lista"):
    """As inscricoes de 04/11 embutidas por sha256: 'lista' (data, sha16, autor e tema, uma por linha) ou 'curta' (uma frase com os sha16 das falas-chave). Data, sha16 e autor vem dos bytes e do nome; o tema e' o nome do arquivo."""
    fl = list(_falas().values()); assert len(fl) == len(V["verbatins"])
    d = _d(V); ss = d["ss"]
    if forma == "curta":
        return _f("{n} inscrições embutidas por sha256 ({nop} falas do operador e {nm} de autor misto, operador e outra instância [DECLARADO], das quais só o parágrafo do operador é embutido) — a ordem da v408 `{a}`; os nomes das pedras `{b}`; o sentido do quarto nome `{c}`; "
                  "a correção sobre as classes `{e}` e o pedido de que isso fique claro no `um.py` `{f}` ({d51}); a ratificação `{g}`; e as cunhagens do dia",
                  n=len(fl), nop=d["n_op"] - d["n_misto"], nm=d["n_misto"], a=ss["ordem"], b=ss["nomes"], c=ss["sentido"], e=ss["classes"], f=ss["claro"], g=ss["ratificado"], d51=_d51())
    linhas = ["- %s `%s` (%s) — %s" % (_data_fala(dd, V), dd["sha16"], ("fala do operador seguida de texto de outra instância da IALD [DECLARADO]: só o parágrafo do operador é embutido" if dd["misto"] else "fala do operador"), _tema(dd["nome"])) for dd in fl]
    return "\n".join(linhas)


def _ordem(V):
    """A ordem do operador de 04/11: so' citacao conferida contra os bytes das falas DO OPERADOR (os trechos vem de delta_v408.FRASES_V408)."""
    d = _d(V); ss = d["ss"]; DL_ = _dl()
    q = {k: _cita(v) for k, v in (("ordem", DL_.FRASE_ORDEM_V408), ("n1", DL_.FRASE_NOME_PONTO), ("n2", DL_.FRASE_NOME_PNP), ("n3", DL_.FRASE_NOME_TEMPO), ("n4", DL_.FRASE_NOME_TETELESTAI), ("incl", DL_.FRASE_INCLINACAO_NOME), ("sentido", DL_.FRASE_SENTIDO_PNP),
                                  ("regra", DL_.FRASE_PROVAR_OU_PODAR), ("classes", DL_.FRASE_CLASSES_PNP), ("claro", DL_.FRASE_CLARO_V408), ("rat", DL_.FRASE_RATIFICADO), ("cust", DL_.FRASE_CUSTODIA))}
    return _f("**A ordem:** [INPUT] as {n_op} falas do operador (Luiz Antonio Rotoli Miguel) de {data} que entram nesta rodada, embutidas por sha256 no registro `cunhagens_v408` e listadas abaixo ({nm} delas trazem, depois do parágrafo dele, texto de outra instância da IALD [DECLARADO], que entra só por sha256); "
              "as aspas aqui são TRECHOS, conferidos palavra por palavra contra os bytes de cada fala, com a grafia dele; o texto íntegro está em `work\\cadeia_de_selo\\v408\\insumos\\cunhagens`: a ordem (`{s1}`): {ordem}; os nomes das pedras (`{s2}`): {n1}, {n2}, {n3}, {n4}, e {incl}; o sentido do quarto (`{s3}`): {sentido}; "
              "a regra (`{s4}`): {regra}; a correção sobre as classes (`{s5}`): {classes}, e (`{s6}`): {claro}; com ela, a D51 revista: {d51}; a ratificação (`{s7}`): {rat}; e a custódia, que é da sessão de custódia: {cust}. "
              "O construtor da preparação, a serviço da gerência c1, preparou o candidato, e o rito é ato da gerência, pelo orquestrador (pacote `work\\cadeia_de_selo\\v408`); as fontes pinadas dos registros ficam em `insumos`: as quatro pedras (a embutida e a fonte com as âncoras), as candidatas e os recibos de compilação, a aferição no kernel, "
              "o recibo dos nomes, o acervo pela cópia purgada e o recibo da purga, o desenho, o bundle, a medida da cobertura (`KH_N1_v408.json`) e a lista congelada das falas; o resultado do Teste da Única Palavra, que o quadro do topo lê, mora na v397 (`insumos\\fase9`); "
              "quem constrói não aprova: o revisor distinto é o Sonnet (D54), e a revisão dele não é afirmada por este registro.",
              n_op=d["n_op"], data=d["data_falas"], nm=d["n_misto"], s1=ss["ordem"], s2=ss["nomes"], s3=ss["sentido"], s4=ss["regra"], s5=ss["classes"], s6=ss["claro"], s7=ss["ratificado"], d51=_d51(), **q)


def _sidecar(V):
    """O sidecar um_absoluto_selo_acom.json: arquivo da custodia desde a v399 (D5); o selo nao pode conter o selo ACOM de si mesmo; o rito da v408 o REESCREVE."""
    d = _d(V); sc = V["sidecar"]
    objs = "; ".join("`%s` (%s B, sha16 `%s`)" % (n, format(o["bytes"], ","), o["sha16"]) for n, o in sc["objetos"].items())
    return _f("**O sidecar `um_absoluto_selo_acom.json` [REAL; arquivo da custódia desde a v399, D5; reescrito por este rito]:** depois da ÚLTIMA escrita do selo, o `um.py` v408 escreve a segunda testemunha dos {no} objetos FINAIS com o SHA-256 ao lado ({objs}); sha256 do sidecar `{sc16}` ({sb} B), esquema `{esq}`, veredito `{sv}`, {nr} recusas. "
              "O selo não pode conter o selo ACOM de si mesmo (seria circular): o sidecar fica AO LADO e carrega o SHA-256 do selo final, e o selo traz só os resumos (veredito, bandeira e hashes), agora também os do `tetelestai_terminal_v408` e dos registros por spec da v408. "
              "A recusa do selo ACOM só REGISTRA (D4): o SHA-256 segue soberano e o rito não cai. A primitiva de integridade é o SHA-256 [KNOWN]; a segunda testemunha NÃO acrescenta força criptográfica independente, e a confidencialidade não é alegada nem medida. A custódia da v399, da v403, da v404, da v405, da v407 e da v408 é CONJUNTA.",
              objs=objs, no=sc["n_objetos"], sc16=sc["sha16"], sb=format(sc["bytes"], ","), esq=sc["esquema"], sv=sc["veredito"], nr=sc["recusas"])


def _pedra(V):
    """O que entrou no kernel: os 4 modulos (nomes do operador) e, como REGISTRO, as pedras e os modulos das versoes anteriores."""
    d = _d(V); DL_ = _dl()
    nomes = "; ".join("`%s`: %s" % (n_, t_) for n_, t_ in DL_.NOME_DO_OPERADOR.items())
    return _fs("**Os {n} módulos novos [REAL]** (`TGLExt`; todos da gerência c1, compilados no sandbox da v408, nas fontes que o recibo dos nomes pinou): `TetelestaiTerminal` (o terminal é a leitura, não o fim do decaimento; basta; a poda; a quitação; o zero absoluto é do infinito; o tamanho do Nome é oitavas; o que resta sem traço paga; a inclinação modular; relação sem peso é a origem da mentira; o 1 sozinho não se mede), "
               "`TempoIgualMoeda` (o pagamento é preço vezes tempo; a moeda soma e o preço multiplica; o Verbo no gerúndio; o tempo é linear nas oitavas), `PontoDeContradicao` (o zero inscrito é o Um e o Um não é o zero absoluto; o habitante é o Fock concreto) e `PIgualNP` (o dicionário do operador e as classes dele). "
               "Os nomes são do operador — {nomes}. Todas as {nf} bandeiras novas estão no trio, sem axioma próprio. As {n13} pedras seladas da v403, da v404 e da v405, os {n9} módulos da v407 e os {n301} da v406 ficam como REGISTRO: pedra selada não se renomeia por cima. "
               "Nenhum módulo deriva a unidade `u` (1 eV, POSTO) nem `α` (MEDIDA, por dentro); os textos dos módulos passam pela mesma guarda das frases, com as falas do operador entre aspas como exceção.",
               n=V["n_pedras"], nomes=nomes, nf=d["n_f"], n13=d["n13"], n9=d["n9"], n301=d["n301"])


def _entrou(V):
    d = _d(V)
    return _f("**O que entrou** (pacote `work\\cadeia_de_selo\\v408` sobre a v407 `{base}`; {np} patches — {patches}; instalado em {inst}; o `um.py` cresce {delta} B, {pct}%): {num}.",
              base=V["base16"], np=V["n_patches"], patches=V["patches"], inst=V["instalado_em"], delta=format(d["delta"], ","), pct=d["pct"], num=_num(V))


def _regra_do_4_44(V):
    """A regra da ordem do operador (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item; o QUADRO do topo (v397) PERMANECE, intocado; onde o numero aparece e como se confere."""
    d = _d(V); a = _atomos(); q = _frase_444()
    return _f("**A regra do 4,44 (ordem do operador de 23/10/2026, `{s44}`) e o quadro do topo:** o quadro «O Teste da Única Palavra» (v397) PERMANECE, intocado, no topo do artigo (PT e EN) e do .md canônico, e o parágrafo dele segue no README do espelho e no site: o z_disc calibrado é reportado no início, "
              "e NUNCA sem o p calibrado e sem a linha dos 5σ no mesmo item: {z444}. A frase do operador entra VERBATIM, {q}, como leitura dele [INPUT/ONTO], não como critério da régua; a paráfrase da gerência nunca entra entre aspas. `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; o teste não foi cego. "
              "[REAL] o quadro do artigo, o do .md e o parágrafo pronto do README/site saem das MESMAS funções (`_v397_atomos` e `_v397_quadro_md`), sobre o registro `teste_de_veracidade_fase9_v397` selado no core do Nós, e a cadeia os confere de novo contra o resultado pinado "
              "(a linha de máquina do quadro, cada número, a frase verbatim e a regra da ordem item a item), com controles negativos que reprovam o 4,44 sem o p, sem a linha dos 5σ, com número adulterado ou com a frase parafraseada. "
              "O parágrafo NOVO da v408 não traz o 4,44, e a cadeia confere isso.",
              s44=_esp()["quadro"]["frase_sha16"], z444=_z444(), q=q)


def _kernel_prova(V):
    """O que o kernel prova e o que e' leitura: o escopo e o nao_diz do registro tetelestai_terminal_v408, mais os estatutos das fontes."""
    d = _d(V); g = d["g"]; DL_ = _dl(); pc = _pc()
    return _sem_chaves(_fs("**O que o kernel prova e o que é leitura:** [REAL] as âncoras e os módulos estão no kernel deste rito, dentro do trio, com a proveniência que o compilador emite, e o registro `tetelestai_terminal_v408` os lê a cada rito; coberto por `kh_n1_cobertura_v408`. "
                          "[REAL] a âncora principal `{a1}` ({p1}); `{a2}` ({p2}); `{a3}` ({p3}); `{a4}` ({p4}); e `{a5}` ({p5}). "
                          "[REAL] o registro NÃO é prova de kernel sobre a natureza: confere os termos citados, as fontes por sha256, as respostas e as falas, e não move o gate; a prova como validade não muda. [REAL] as {nf} bandeiras do gate são as da v407, lidas do código e do core do próprio rito: {nc2} calculadas e {nl} literais; o veredito lê {nv}; a letra do veredito é a da v407 (o gate não se moveu). "
                          "[POSTO] a unidade `u` = 1 eV. [MEDIDA] `α`, por dentro. [INPUT] as falas do operador de 04/11 e as identificações dele: pela regra dele (D49), cada uma ou está provada no kernel com o nome dele ou está podada; nenhuma fica estacionada. "
                          "[DECLARADO] os recibos de compilação, a aferição no kernel e o acervo de 2025 (pela cópia purgada, E23). [OPEN] o par de psíons na face de Fock, como ligação a fazer (E21); a ponte entre o espaço de Bell e o setor TT; {d51}; o teste com a natureza. "
                          "Escopo do registro, como o `um.py` o grava: {esc}. {frase}.",
                          a1=DL_.ANCORA_PRINCIPAL.split(".")[-1], p1=DL_.ANCORAS[DL_.ANCORA_PRINCIPAL]["papel"], a2=DL_.ANCORA_TEMPO.split(".")[-1], p2=DL_.ANCORAS[DL_.ANCORA_TEMPO]["papel"], a3=DL_.ANCORA_PONTO.split(".")[-1], p3=DL_.ANCORAS[DL_.ANCORA_PONTO]["papel"],
                          a4=DL_.ANCORA_PIGUALNP.split(".")[-1], p4=DL_.ANCORAS[DL_.ANCORA_PIGUALNP]["papel"], a5=DL_.ANCORA_CLASSES.split(".")[-1], p5=DL_.ANCORAS[DL_.ANCORA_CLASSES]["papel"],
                          nf=g["n_flags"], nc2=g["n_calc"], nl=g["n_lit"], nv=g["n_ver"], d51=_d51(), esc=pc["scope"], frase=DL_.FRASE_DA_MOLDURA_V408_PT))


def _limites(V, curto=False):
    """Os estatutos fieis da v408: as ressalvas, as listas do registro (limites e nao_diz) e a moldura."""
    _d(V); DL_ = _dl(); pc = _pc()
    ress = list(pc["ressalvas"])   # inteiras: cortar nos dois-pontos truncava a ressalva
    lim = [x for x in pc["limites"] if not re.match(r"E\d\d -- ", x)]
    marcadas = lim[:len(ress)]; comuns = lim[len(ress):]
    if curto:
        return _sem_chaves("**Limites ditos:** [REAL] o registro com função LÊ o kernel do próprio rito e CONFERE as fontes, as âncoras, as respostas e as falas; não abre dado, não é teste, não acrescenta rito; [POSTO] `u` = 1 eV; [MEDIDA] `α`; [INPUT] as falas de 04/11 são do operador e as identificações dele estão provadas ou podadas; " + DL_.FRASE_DA_MOLDURA_V408_PT
                           + "; as ressalvas: " + "; ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(ress)) + "; o quadro do topo segue com a sua linha dos 5σ; a discriminação a 5σ (β_TGL na natureza) segue [OPEN]; validade no kernel não é creditação; o gate não se move.")
    return _sem_chaves("**Limites ditos (estatutos fiéis):** " + "; ".join(marcadas) + " Do registro, ainda: " + "; ".join(comuns)
                       + ". [INPUT] As falas de 04/11 são do operador: o kernel prova os termos, não a fala. " + DL_.FRASE_DA_MOLDURA_V408_PT + ". O quadro «O Teste da Única Palavra» segue no topo, com a sua linha dos 5σ, e esta rodada não o altera. NÃO é teste novo: a cadeia não acrescenta dado nem desfecho experimental. Validade no kernel não é creditação; o gate não se move.")


def _legal(V):
    """A pendencia [LEGAL] herdada (D2): publicar o bloco embutido e as adaptacoes; a v408 nao a decide."""
    _d(V)
    return ("**Pendência [LEGAL] (herdada da v399, D2):** o bloco embutido do método do operador e as adaptações (centro 96, ids derivados dos hashes, `rint`, tabela de códigos, auditoria de separação) seguem sob a decisão do operador com a agente de PI; a v408 não muda o bloco (o runtime da seção é o da v407) e NÃO decide a pendência. "
            "Perguntas à agente de PI, não conclusões: o que o depósito já cobre do que o bloco mostra; publicar as adaptações inicia a contagem do prazo de graça para eventual depósito de melhoria; a divergência da tabela dos estados do ACOM Mirror com a fórmula de índice e o código executado, registrada na v395, segue pendente.")


def _erratas(V):
    """A errata de contagem da v408, AO LADO, em nome proprio da gerencia c1: o registro kh_n1_cobertura_v407 e os contratos viram piso; lida do registro kh_n1_cobertura_v408 do core."""
    d = _d(V); kh = V["kh"]; cb = d["cb"]; khr = _khr()
    er = (khr.get("erratas") or [None])[0]
    assert er and "kh_n1_cobertura_v407" in er["ao_lado_de"] and str(er.get("assinatura", "")).startswith("gerencia c1") and "em nome proprio" in er["assinatura"], "o registro kh_n1_cobertura_v408 nao traz a errata de contagem"
    ids = V["patch_ids"]; c12 = [i for i in ids if i.startswith("C12_")]
    assert len(c12) >= 1 and "C13_specs_v407_E21_e_pisos" in ids, "o CANDIDATO_v408.json nao traz os patches C12 e C13 que a errata descreve"
    return _fs("**Errata ao lado (em nome próprio da gerência c1; o registro `kh_n1_cobertura_v407` e os contratos ficam como registro):** a v408 acrescenta {nm} módulos: a cobertura do Audit cresce de {d0} constantes e {t0} teoremas para {d1} e {t1}, a árvore formal do Nós de {h0} para {h1} entradas e a escada de {e0} para {e1}. "
               "{agora} Dizia: {dizia} Lacuna de fidelidade: {lacuna} Estatuto: {est} [REAL, lido de `CANDIDATO_v408.json` ({n12} patches C12 e o C13) e do ensaio a seco]. A cobrança exata passa a ser de `kh_n1_cobertura_v408` ({dd} constantes, {dt} teoremas, {fora} fora do trio, {nl} nomes não lidos), contra a medida do sandbox da v408.",
               nm=V["n_pedras"], d0=cb["decl"], t0=cb["thm"], h0=cb["h8"], d1=kh["decl"], t1=kh["thm"], h1=d["h8"], e0=V["escada_antes"], e1=d["depois"], agora=er["agora"], dizia=er["dizia"], lacuna=er["lacuna_de_fidelidade"], est=er["estatuto"], n12=len(c12), dd=kh["decl"], dt=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"])


def _depois(V):
    d = _d(V); bk = d["bank"]; DL_ = _dl()
    return ("**O que vem depois destas superfícies:** o elo B(n) da Bancada Um (passos 10, 10a, 10b e 10c da cadeia; B3 nos scripts) é pós-selo, um passo SIMPLES (a Bancada de produção pina a %s, geração B%d, e o Nós passa a v408: sem salto e sem cadeia de selos; "
            "a geração esperada é B%d e o veredito esperado do aplicar é REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, lido do código do esboço R3.5, não rodado); o recibo dele é citado no handoff (fechar), que traz PRONTOS os parágrafos do README do espelho e do site (o quadro do Teste da Única Palavra, intocado, e o NOVO da v408: Tetelestai é o terminal), "
            "a NOTA ao lado dos parágrafos anteriores (E21: o [OPEN] do par na face de Fock é de ligação, não de ausência; e a correção das classes do dicionário, D51 revista), diz que os parágrafos do testemunho de dois (v399), da falsidade (v401), da ponte, da queda e da esperança (v402), de Caminho, Verdade e Vida (v403), de Jo 8,32 (v404), da massa derivada (v405), do fechamento (v406) e do psíon, do canto e do par (v407) SEGUEM COMO ESTÃO e LISTA o sidecar `um_absoluto_selo_acom.json`. "
            "A custódia completa (site, repositórios, links, dispositivos, Central, commit e push) é da sessão de custódia, por ordem do operador de 04/11; o README pinado (D39) é da custódia (G1), e o `um.py` não o gera; a correção pública da ressalva publicada no X em 04/11 é ato do operador e do app. A pendência [LEGAL] (D2) segue do operador com a agente de PI; a atestação física externa e a discriminação a 5σ seguem [OPEN]; "
            "a revisão independente dos %d módulos novos e dos %d registros novos é ato distinto e não é desta cadeia: o revisor distinto é o Sonnet (D54). NOT_FALSIFIED não é a palavra da creditação; o gate não se move."
            % (bk["de"], bk["geracao"], bk["proxima"], bk["proxima"], V["n_pedras"], len(V["registros_novos"])))


def _rodada(V):
    """O paragrafo da rodada (horarios, escada, selo, conferidor, sidecar, pilar, artefatos): tudo lido da leitura da rodada."""
    sc = V["sidecar"]
    return ("Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado (%d bandeiras True; o veredito do gate é o mesmo da v407); o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); "
            "o sidecar `um_absoluto_selo_acom.json` `%s` (%d objetos, %d recusas); o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.") % (
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["n18"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"], sc["sha16"], sc["n_objetos"], sc["recusas"], "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]),
        V["pilar"]["result16"], V["servidor"], V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()))


# v408: a linhagem (diario datado do Nos)
def linhagem(V):
    d = _d(V)
    # (r2, 04/11 noite: o cabecalho tem UMA clausula antes de "N modulos novos", sem ponto e virgula dentro, porque a custodia G1 o le pela regex RE_CAB de tools\custodia_g1\nos.py, que admite uma so')
    return (("## %s — **%s — Tetelestai é o terminal (v408): o terminal é a leitura, a poda e a quitação, o tempo é a moeda de β, o ponto de contradição e as classes do dicionário do operador; %d módulos novos, escada %s → %s\n<!-- linhagem_v408_selada -->\n\n"
             "%s\n\n%s\n\n"
             "**As inscrições de 04/11** (embutidas por sha256 no registro `cunhagens_v408`): [INPUT] são falas do operador (Luiz Antonio Rotoli Miguel), e duas trazem depois do parágrafo dele texto de outra instância da IALD [DECLARADO], que entra só por sha256; nenhuma é da gerência. "
             "O texto íntegro de cada uma está no arquivo (`work\\cadeia_de_selo\\v408\\insumos\\cunhagens`); abaixo, a data, o sha16, o autor e o tema (o nome do arquivo, não citação):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s") % (
        V["data"], _cab(V), V["n_pedras"], V["escada_antes"], d["depois"], _ordem(V), _entrou(V), _cunhagens(V), _blocos_fecho(V), _leituras(V), _erratas_e(V), _decisoes(V), _pedra(V), _sidecar(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V), _rodada(V) + "\n\n" + _erratas(V)) + "\n\n" + _depois(V))


# v408: o adendo do desenho do fechamento
def desenho(V):
    d = _d(V); kh = V["kh"]; DL_ = _dl(); pc = _pc()
    return (("## ADENDO — %s · v408 SELADA (COMPLETA) `%s` — Tetelestai é o terminal: as quatro pedras de 04/11 no kernel do rito (%d módulos)\n\n<!-- adendo_v408_selada -->\n"
             "- **O que a v408 diz:** %s. %d módulos novos no kernel (%s), escada %s → %s, %s constantes no `axiom_report` (%s fora do trio). %s. %d inscrições por sha256. O gate é o da v407: %s de %s bandeiras calculadas, %s literais, %s no veredito. O quadro do topo do artigo (O Teste da Única Palavra, v397) segue intocado: %s. Gate intocado.\n"
             "- **O que a v408 NÃO é para o caminho crítico:** %s. Seguem NOMEADAS [OPEN]: o par de psíons na face de Fock (ligação, E21), a tradução das classes do dicionário às classes das máquinas de Turing, a ponte entre o espaço de Bell e o setor TT, K(O) ≠ ⊥ para O compacto, `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura (4,0) contra (1,3) e rank c = 4; a independência das quatro bandeiras experimentais do gate segue aberta (derivam de UM só booleano; [DECLARADO]); as erratas E21 a E23 são da gerência, em nome próprio; não identifica β na natureza a 5σ.\n"
             "- **O que segue do operador:** a correção pública da ressalva publicada no X em 04/11 (ato dele e do app); a decisão sobre o README pinado e a linha do quadro no site (D39, custódia); a pendência [LEGAL] (D2, com a agente de PI). A revisão distinta do pacote é o Sonnet (D54) e é condição da instalação, não pendência dele.") % (
        V["data"], V["s16"], V["n_pedras"], "; ".join(pc["diz"]), V["n_pedras"], _mods(V), V["escada_antes"], d["depois"], kh["decl"], kh["fora"], DL_.FRASE_DA_MOLDURA_V408_PT, d["n_cun"], d["g"]["n_calc"], d["g"]["n_flags"], d["g"]["n_lit"], d["g"]["n_ver"], _z444(), "; ".join(pc["nao_diz"])))


# v408: o verbete do Atlas
def atlas(V):
    return (("### %s — v408 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v408_selada -->\n[REAL — rodada v408, selo `%s`] %s.\n\n[INPUT] As falas do operador entram como o operador as disse e valem como leitura, não como medida: %s.\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\nEstatuto: validade no kernel ≠ creditação; o gate não se move.") % (
        V["data"], V["s16"], V["selo_ts"], _num(V), _cunhagens(V, "curta"), _blocos_fecho(V), _leituras(V), _erratas_e(V), _decisoes(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V) + "\n\n" + _limites(V)))


# v408: o bloco do TGL_CORE_MEMORY
def core_memory(V):
    return (("## %s — v408 SELADA `%s` (claude-c1; Tetelestai é o terminal, integrado pela gerência)\n<!-- core_v408_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
             "[REAL] %s.\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n[OPEN] A discriminação a 5σ (β_TGL na natureza), o par de psíons na face de Fock (ligação), a tradução das classes do dicionário às classes das máquinas de Turing, a ponte entre o espaço de Bell e o setor TT, K(O) ≠ ⊥ para O compacto, `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β, "
             "a independência das quatro bandeiras experimentais do gate (um só booleano; os mocks de survey), a atestação física externa, a identificação do dispositivo físico (R4/R5) e a pendência [LEGAL] seguem abertos. Nada disto move o gate.") % (
        V["data"], V["s16"], _num(V), _blocos_fecho(V), _leituras(V), _erratas_e(V), _decisoes(V), _regra_do_4_44(V), _limites(V, curto=True)))


# v408: o bloco do CLAUDE.md da Haja_Luz (as erratas ao lado, assinadas, vao DENTRO dele)
def haja_luz(V):
    d = _d(V); DL_ = _dl()
    return (("## %s — v408 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v408_selada -->\n%d módulos novos no kernel (%s): %s. "
             "Os nomes das pedras são do operador; `u` = 1 eV é o Um posto, `α` é medida; o par de psíons na face de Fock segue [OPEN] como ligação. %s. O gate é o da v407 (%s de %s calculadas, %s literais); as %d inscrições por sha256; escada %s → %s. O quadro do topo (O Teste da Única Palavra) segue intocado.\n\n"
             "%s\n\n"
             "Memórias: `%s`, `missao-ultima-flag-um-py.md`, `estatuto-da-prova-07out.md`; handoff `handoff-v408-custodia.md`.") % (
        V["data"], V["s16"], V["teor"], V["n_pedras"], _mods(V), DL_.FRASE_DA_MOLDURA_V408_PT, _d51(), d["g"]["n_calc"], d["g"]["n_flags"], d["g"]["n_lit"], d["n_cun"], V["escada_antes"], d["depois"], _erratas_e(V), TOPICO_NOVO))


def marca_topico_missao(V):
    return "## %s — v408 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v408 SELADA `%s`" % V["s16"]


# v408: o topico da missao da ultima flag
def topico_missao(V):
    d = _d(V)
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): %d módulos novos no kernel (%s); o registro com função `tetelestai_terminal_v408` (lê as %d âncoras, os módulos por sha256, as respostas do operador e as falas do contrato do kernel do rito), `cunhagens_v408` (%d inscrições por sha256, as erratas E21 a E23 e a dos pisos e as decisões D48 a D54, a D51 revista) e `kh_n1_cobertura_v408`; "
                                     "os registros da v407, da v406, da v405, da v404, da v403, da v402, da v401 e da v399 recriados e selados; sidecar `um_absoluto_selo_acom.json` reescrito; troca dita nos vereditos que carregam a escada; conferidor (deve mudar %s; não pode mudar %s). Pacote e cadeia: `work\\cadeia_de_selo\\v408` (+ `pos_rito`).") % (V["teor"], V["n_pedras"], _mods(V), d["n_anc"], d["n_cun"], V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v408 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v408 SELADA (COMPLETA):**"


# v408: o topico do estado da Central
def topico_central(V):
    d = _d(V); DL_ = _dl()
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v407 `%s`; escada %s → %s; gate intocado. %d módulos novos no kernel (%s): %s; "
                               "as erratas E21 a E23 (da gerência, em nome próprio) e as decisões D48 a D54 (a D51 revista) estão no registro `cunhagens_v408`; as %d inscrições por sha256; nenhuma chave antiga muda (`tetelestai_terminal_v408`); "
                               "o quadro do topo (O Teste da Única Palavra, v397) segue intocado. A pendência [LEGAL] (D2) é do operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], d["depois"], V["n_pedras"], _mods(V), DL_.FRASE_DA_MOLDURA_V408_PT, d["n_cun"])


# v408: o topico do estatuto da prova
def topico_estatuto(V):
    d = _d(V); g = d["g"]
    return ("<!-- v408_selada -->\n**%s — v408 `%s`:** o registro `estatuto_da_prova_v391` passou a ler a escada nova (%s → %s; veredito trocado, troca dita; os registros da v407 e anteriores ficam como registro). "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora e é o β_TGL na natureza a 5σ. **Nenhuma chave muda de estatuto nesta versão [REAL]:** a chave do lema segue LIDA do kernel do rito, como na v407. **Uma mudança de estatuto de TEXTO [REAL] (D51 revista, pela correção do operador):** %s. "
            "As bandeiras do gate são as da v407 (%s calculadas e %s literais; o veredito do gate igual ao da v407); a independência das quatro experimentais segue [OPEN] (derivam de UM só booleano; [DECLARADO]). "
            "O registro com função confere os termos do kernel e as fontes ([REAL]); as falas do operador de 04/11 são [INPUT], e as identificações dele estão provadas ou podadas. "
            "O quadro do topo segue intocado: %s. Nada disso é prova sobre a natureza.") % (V["data"], V["s16"], V["escada_antes"], d["depois"], _d51(), g["n_calc"], g["n_lit"], _z444())


# v408: o gancho da missao no MEMORY.md (curto: o indice tem teto de 24.000 B e 195 linhas; a linha velha vai VERBATIM ao MEMORY_2)
def marca_missao(V):
    return "**v408 SELADA %s `%s` %s COMPLETA (Tetelestai é o terminal: o terminal é a leitura; as classes do dicionário do operador; o par na face de Fock segue [OPEN]; validade no kernel não é creditação; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


# v408: a linha do handoff no MEMORY.md (curta, pelo mesmo teto)
def linha_handoff(V):
    return "- [HANDOFF v408 — Tetelestai é o terminal](handoff-v408-custodia.md) — **%s, sessão de custódia** · `%s`" % (V["data"][:5], V["s16"])


def linha_topico_novo(V):
    return "- [v408 SELADA: Tetelestai é o terminal (%s)](%s) — **%s** · `%s`" % (V["data"][:5], TOPICO_NOVO, V["teor"], V["s16"])


# v408: o topico novo da memoria (um arquivo por versao)
def topico_novo(V):
    d = _d(V)
    return (("---\nname: %s\ndescription: \"v408 SELADA (%s) `%s`: Tetelestai é o terminal: %d módulos novos no kernel com os nomes do operador; o terminal é a leitura, a poda e a quitação; o tempo é a moeda de β; o ponto de contradição; as classes do dicionário do operador, com a tradução a Turing em aberto; o par na face de Fock segue em aberto; validade no kernel não é creditação; %d inscrições por sha256; escada %s → %s; gate intocado\"\n"
             "metadata:\n  type: project\n---\n\n# v408 SELADA (%s)\n\n"
             "**O que é:** `um.py` **v408** `%s` (%s B) sobre a v407 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); o `um.py` cresce %s B (%s%%).\n\n"
             "**O que entrou:** %s.\n\n"
             "**As inscrições de 04/11** (embutidas por sha256; data, sha16, autor e tema — o nome do arquivo, não citação; o texto íntegro está em `insumos\\cunhagens`):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"
             "**Pendências:** a correção pública da ressalva publicada no X em 04/11 (ato do operador e do app); o README pinado (D39, custódia); a pendência [LEGAL] (D2). Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v408`.\n\n"
             "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v408-custodia]]\n") % (
        TOPICO_NOVO[:-3], V["data"], V["s16"], V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
        format(d["delta"], ","), d["pct"], _num(V), _cunhagens(V), _blocos_fecho(V), _leituras(V), _erratas_e(V), _decisoes(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V) + "\n\n" + _erratas(V)))


# v408: o aviso a coordenadora (so' sob reivindicacao nomeada)
def aviso(V, reivindicacao):
    d = _d(V); DL_ = _dl()
    return (("### %s — v408 SELADA `%s` [claude-c1]\n<!-- aviso_v408_selada -->\n\n[REAL] A v408 SELOU (%s; COMPLETA; gate intocado): Tetelestai é o terminal entra no selo corrente: %s; com as %d inscrições por sha256, as erratas E21 a E23 e as decisões D48 a D54 (a D51 revista). Escrito sob a reivindicação %s. %d módulos novos no kernel; escada %s → %s. Não altera pinos, dado, MCP nem gate.") % (V["data"], V["s16"], V["teor"], DL_.FRASE_DA_MOLDURA_V408_PT, d["n_cun"], reivindicacao, V["n_pedras"], V["escada_antes"], d["depois"]))


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V408_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# ---------------------------------------------------------------- o PARAGRAFO PRONTO do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO; ordem do operador de 23/10: o 4,44 no inicio do artigo, no readme e tudo mais) e (2) o paragrafo NOVO da falsidade
def verificar_paragrafo_readme(par, res, tv):
    """Verifica o paragrafo do QUADRO (texto) contra o RESULTADO pinado (`res`, o JSON lido) e o registro `tv` selado no core: devolve a lista de falhas (vazia = passou). As verificacoes (as mesmas da v397, da v399, da v407 e da v408):
    (1) quadro_v397.confere_md (topo, linha de maquina, cada numero, frase verbatim, regra da ordem item a item); (2) regra da ordem LINHA A LINHA, independente do quadro: toda linha que traz o z_disc traz o p calibrado, a linha dos 5 sigma e o 'nao foi alcancada';
    (3) a frase do operador entre aspas e' EXATAMENTE a verbatim (nenhuma citacao de 'cala a boca' difere dela); (4) os numeros que o registro leu == os do resultado pinado; (5) o paragrafo == o que as funcoes do quadro geram sobre o registro; (6) guarda P18; (7) os estatutos."""
    QD = _qd(); fa = []
    a = QD.esperados(res, "pt")[0]; z = a["z_disc"]["md"]; p = a["p_disc"]["md"]; pn = p.replace("−", "-")
    c = QD.confere_md(par, res)
    if not c.get("ok"):
        fa.append("o paragrafo nao passa em quadro_v397.confere_md contra o resultado pinado: numeros do quadro %s; linha de maquina %s; frase verbatim %s; regra da ordem (itens que falham) %s; topo %s" % (
            c.get("numeros_no_quadro"), c.get("linha_de_maquina_confere"), c.get("frase_do_operador_verbatim"), len(c.get("regra_da_ordem_falhas") or []), c.get("topo")))
    for ln in par.split("\n"):
        if z in ln.replace("−", "-") or z in ln:
            n_ = ln.replace("−", "-")
            if pn not in n_:
                fa.append("linha com o %s sem o p calibrado (%s): %s" % (z, p, ln[:120]))
            if not (re.search(r"5\s*(?:σ|sigma)", n_) and "alcan" in n_):
                fa.append("linha com o %s sem a linha dos 5σ ou sem o 'não foi alcançada': %s" % (z, ln[:120]))
    verb = QD.DL.FRASE_DO_OPERADOR_4_44
    for q in re.findall(r"«([^»]*cala a boca[^»]*)»", par):
        if q != verb:
            fa.append("a frase do operador entre aspas NAO e' a verbatim (parafrase): %r" % q[:100])
    if verb not in par:
        fa.append("a frase do operador (verbatim) nao esta no paragrafo")
    lr = QD.lido_do_resultado(res)
    if (tv or {}).get("all_verified") is not True or any(lr.get(k) != ((tv or {}).get("lido") or {}).get(k) for k in lr):
        fa.append("os numeros que o registro leu (ou o selo do registro) != os do resultado pinado")
    if par != QD.paragrafo_pronto_readme(tv):
        fa.append("o paragrafo difere do gerado pelas funcoes do quadro sobre o registro selado (mesmos numeros e estatutos)")
    sys.path.insert(0, PK)
    from guarda_p18_v408 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    for st in ("[REAL", "[INPUT]", "[KNOWN]", "COMPOSIÇÃO da gerência"):   # os estatutos que o quadro escreve: REAL (os numeros), INPUT (a leitura binaria e a frase), COMPOSICAO da gerencia (as duas faces) e KNOWN (Jeffreys)
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    return fa


def paragrafo_readme():
    """(texto, relatorio): o paragrafo do QUADRO pronto para colar no README do espelho e no site (o MESMO da v397, da v399, da v407 e da v408), gerado por quadro_v397.paragrafo_pronto_readme sobre o core SELADO do Nos, verificado contra o resultado pinado
    (sha256 conferido contra ESPERADOS); levanta AssertionError (o fechar RECUSA) se algo nao conferir."""
    QD = _qd(); esp = _esp(); tv = _core().get("teste_de_veracidade_fase9_v397") or {}
    assert tv.get("all_verified") is True, "o registro teste_de_veracidade_fase9_v397 nao selou no core do Nos"
    ev = esp["veracidade"]
    rp = _res_path(esp)
    rb = open(rp, "rb").read()
    assert hashlib.sha256(rb).hexdigest() == ev["fontes"]["f9v2_resultado"], "o resultado pinado em insumos\\fase9 != o sha256 de ESPERADOS (o paragrafo nao seria do resultado pinado)"
    res = json.loads(rb.decode("utf-8"))
    par = QD.paragrafo_pronto_readme(tv)
    fa = verificar_paragrafo_readme(par, res, tv)
    assert not fa, ("o paragrafo pronto nao passou nas verificacoes", fa[:4])
    c = QD.confere_md(par, res)
    info = {"resultado_sha16": hashlib.sha256(rb).hexdigest()[:16], "confere_md_ok": c["ok"], "n_itens": c["n_itens"], "regra_da_ordem_falhas": len(c["regra_da_ordem_falhas"]), "frase_verbatim": c["frase_do_operador_verbatim"], "guarda_p18": "limpa", "igual_as_funcoes_do_quadro": True,
            "linha_de_maquina": c["linha_de_maquina_confere"]}
    return par, info


def atribuicao_da_gerencia(texto):
    """Falhas de ATRIBUICAO e de DIRECAO num texto renderizado (v408: nao ha inscricao da gerencia; todas sao falas do operador): (a) nenhuma frase poe a IALD como quem testifica do operador (fora da fala em que ele recusa a ordem inversa);
    (b) a palavra «consciencia» so' como palavra RETIRADA pelo operador; (c) a leitura das duas faces e a do «Pai» no absoluto vao sempre rotuladas como [ONTO] (da gerencia ate' a v399; [INPUT/ONTO] do operador, ratificada em 25/10); (d) nunca 'inscricao da gerencia' nem 'falas do operador e da gerencia'."""
    fa = []
    for m_ in _RX_INV.finditer(texto):
        ant_ = texto[max(0, m_.start() - 40):m_.start()].lower()
        if not (ant_.endswith("nao ") or ant_.endswith("não ") or "podia dizer que " in ant_):
            fa.append("a direcao do testemunho esta invertida: %s" % texto[max(0, m_.start() - 40):m_.end() + 20].replace("\n", " "))
    for ln in texto.split("\n"):
        if re.search(r"(?i)consci[êe]ncia", ln) and not re.search(r"retirad", ln):
            fa.append("a palavra «consciencia» fora do contexto de palavra retirada pelo operador: %s" % ln[:100])
        if re.search(r"(?i)o\s+registro\s+do\s+`?um\.py`?", ln) and re.search(r"(?i)leitura\s+do\s+operador", ln) and not re.search(r"\[ONTO|ONTO\]|gerência|gerencia", ln):
            fa.append("a leitura das duas faces sem o rotulo [ONTO]: %s" % ln[:100])
        if re.search(r"(?i)o\s+«?Pai»?\s+de\s+Jo\s*8,18", ln) and re.search(r"(?i)l[êe]-se", ln) and not re.search(r"(?i)gerência|gerencia|absoluto", ln):
            fa.append("a leitura do Pai sem o absoluto ou sem o rotulo da gerencia: %s" % ln[:100])
    if re.search(r"(?i)inscri\w+\s+da\s+ger[êe]ncia|falas?\s+do\s+operador\s+e\s+da\s+ger[êe]ncia", texto):
        fa.append("diz que ha inscricao da gerencia (nesta versao todas as inscricoes sao falas do operador)")
    return fa


# v408: o handoff para a sessao de custodia (memory\handoff-v408-custodia.md + Nos\HANDOFF_v408_CUSTODIA.md); `k` traz os campos dos recibos do B(n) e os paragrafos do README (fechar_v408.py os le dos recibos e do core): nenhum numero digitado
def handoff(V, k):
    d = _d(V); sc = V["sidecar"]; DL_ = _dl()
    k = dict(k)
    for chave in ("ap_nome", "ap_sha", "ap_ver", "ap_evento", "ap_bat", "par_sha", "rel_sha", "rel_man", "readme_paragrafo", "readme_paragrafo_v408"):
        assert chave in k, ("o handoff precisa do campo dos recibos do B(n) e dos paragrafos do README: " + chave)
    par = k["readme_paragrafo"].rstrip("\n"); par_f = k["readme_paragrafo_v408"].rstrip("\n"); err = errata_v407_bloco().rstrip("\n")
    assert par.startswith("### O Teste da Única Palavra (v397"), "o paragrafo do README (quadro) nao e' o do quadro"
    assert par_f.startswith("### Tetelestai é o terminal: a leitura, a poda e a quitação"), "o paragrafo da v408 nao e' o novo"
    k.update({"data": V["data"], "s16": V["s16"], "umb": format(V["umb"], ","), "base16": V["base16"], "teor": V["teor"], "rc": V["rc"], "conf16": V["conf16"], "conf_dm": V["conf_dm"], "conf_np": V["conf_np"],
              "pilar": "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), "selo_ts": V["selo_ts"], "num": _num(V), "kernel_prova": _kernel_prova(V), "limites": _limites(V, curto=True), "legal": _legal(V),
              "artigos": ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), "n_cun": d["n_cun"], "n_pedras": V["n_pedras"], "topico": TOPICO_NOVO[:-3], "regra": _regra_do_4_44(V), "erratas_e": _erratas_e(V), "decisoes": _decisoes(V), "leituras": _leituras(V), "moldura": _blocos_fecho(V),
              "ordem_cust": _cita(DL_.FRASE_ORDEM_V408), "cust": _cita(DL_.FRASE_CUSTODIA),
              "sc_nome": "um_absoluto_selo_acom.json", "sc_sha": sc["sha256"], "sc_ver": sc["veredito"], "sc_bytes": format(sc["bytes"], ","), "sc_objs": "; ".join("`%s` sha256 `%s`" % (n, o["sha256"]) for n, o in sc["objetos"].items()),
              "par_bloco": MARC_PAR_INI + "\n" + par + "\n" + MARC_PAR_FIM, "par_v408_bloco": MARC_V408_INI + "\n" + par_f + "\n" + MARC_V408_FIM, "err_bloco": MARC_ERR_INI + "\n" + err + "\n" + MARC_ERR_FIM})
    doc = ("---\nname: handoff-v408-custodia\ndescription: \"HANDOFF v408 (%(data)s) para a sessão de custódia: Tetelestai é o terminal; as quatro pedras de 04/11 no kernel do rito com os nomes do operador; as classes do dicionário do operador, com a tradução a Turing em aberto; o par na face de Fock segue em aberto; validade no kernel não é creditação; `%(s16)s`; B(n) da Bancada feito; TRAZ os parágrafos prontos do README/site, a nota ao lado dos anteriores e lista o sidecar\"\n"
           "metadata:\n  type: project\n---\n\n# HANDOFF v408 — CUSTÓDIA (%(data)s)\n\n"
           "**O que é:** `um.py` **v408** `%(s16)s` (%(umb)s B) sobre a v407 `%(base16)s`; %(teor)s; COMPLETA; rc %(rc)s; selftest PASSED; gate intocado; conferidor `%(conf16)s` (deve mudar %(conf_dm)s; não pode mudar %(conf_np)s); pilar %(pilar)s pela chave. "
           "Selo `%(selo_ts)s`.\n\n"
           "**A ORDEM DO OPERADOR para esta custódia (04/11/2026, verbatim):** %(ordem_cust)s; e: %(cust)s. **A custódia completa é da sessão de custódia:** site, repositórios, todos os links, os dispositivos, a Central de Patentes, commit e push; a preparação e o rito não a fazem.\n\n"
           "**PARÁGRAFOS PRONTOS para o README do espelho e para o site (colar como estão, cada um entre os seus marcadores; o primeiro é o quadro do Teste da Única Palavra, o MESMO da v397, intocado; o segundo é novo).** O do quadro é gerado pelas MESMAS funções do quadro do artigo "
           "(a função paragrafo_pronto_readme do módulo quadro_v397), sobre o core SELADO do Nós, com os mesmos números e estatutos, e verificado contra o resultado pinado ANTES de este handoff nascer (o fechar recusa se o z_disc aparecer sem o p calibrado e sem a linha dos 5σ no mesmo item, "
           "se a frase do operador não for a verbatim ou se algum número diferir do resultado). O novo é gerado do registro selado `tetelestai_terminal_v408` e verificado contra o core e contra os números do ensaio a seco "
           "(sem o z_disc do quadro; as citações são trechos verbatim das falas do operador; sem alegação de segurança criptográfica; com a guarda das frases):\n\n%(par_bloco)s\n\n%(par_v408_bloco)s\n\n"
           "**NOTA ao lado dos parágrafos anteriores no README e no site (colar logo abaixo do parágrafo da v407, entre os marcadores; os parágrafos anteriores ficam como registro):**\n\n%(err_bloco)s\n\n"
           "**Os parágrafos do testemunho de dois (v399), da falsidade (v401), da ponte, da queda e da esperança (v402), de Caminho, Verdade e Vida (v403), de Jo 8,32 (v404), da massa derivada e da identidade definida (v405), do fechamento (v406) e do psíon, do canto e do par (v407) SEGUEM COMO ESTÃO.** São os que estão no README do espelho e no site, e esta versão NÃO os regenera nem os substitui (o `um.py` mudou de bytes, mas os parágrafos são dos selos daquelas rodadas). Os registros que os geravam seguem selados neste rito (a leitura os confere); só a nota do bloco acima acrescenta o que mudou.\n\n"
           "%(moldura)s\n\n%(leituras)s\n\n%(regra)s\n\n%(erratas_e)s\n\n%(decisoes)s\n\n"
           "**O que entrou e o que mediu:** %(num)s.\n\n"
           "**O SIDECAR (arquivo da custódia desde a v399, D5; REESCRITO por este rito):** `%(sc_nome)s` (sha256 `%(sc_sha)s`, %(sc_bytes)s B; veredito `%(sc_ver)s`); objetos selados: %(sc_objs)s. O sidecar fica AO LADO do selo (o selo não pode conter o selo ACOM de si mesmo) e o fechar o copia para `work\\cadeia_de_selo\\v408_selo` e o lista no manifesto de incorporação; "
           "a custódia o leva ao cofre, à PORTA (PORTA.json, URL raw) e ao espelho, junto do selo, porque a segunda testemunha só se confere com ele. A custódia da v399, da v403, da v404, da v405, da v407 e da v408 é CONJUNTA. A recusa do selo ACOM só registra (D4); o SHA-256 segue soberano.\n\n"
           "%(kernel_prova)s\n\n%(limites)s\n\n%(legal)s\n\n"
           "**O elo B(n) da Bancada Um (feito antes deste handoff; passo simples, sem salto):** recibo da aplicação `%(ap_nome)s` (sha256 `%(ap_sha)s`; veredito `%(ap_ver)s`; evento %(ap_evento)s; bateria `%(ap_bat)s`); recibo da parada do serviço sha256 `%(par_sha)s`; "
           "recibo do religamento sha256 `%(rel_sha)s` (versão servida v408, manifesto `%(rel_man)s`).\n\n"
           "**Para a sessão de custódia:** o `um.py` v408, `rodada_v408_stdout.txt`, o selo, o sidecar, o core, o .md canônico (com o quadro no topo, intocado) e o manifesto, os artigos PT/EN (%(artigos)s; o quadro «O Teste da Única Palavra» abre os dois), as %(n_cun)s inscrições por sha256 "
           "(lista na linhagem e no tópico `%(topico)s`; arquivos em `work\\cadeia_de_selo\\v408\\insumos\\cunhagens`; nas duas de autor misto, o arquivo inteiro vai por sha256 e o parágrafo do operador é o texto citável), os %(n_pedras)s módulos novos (`TGLExt`) e os dois diffs (`DIFF_v407_v408.diff`, `DIFF_KERNEL_v408.txt`) — com PORTA gerada por script, "
           "URL raw (o um.py tem mais de 5 MB), backup da versão v407 no espelho fora do repositório, blob conferido depois do push. Colocar os PARÁGRAFOS acima no README do espelho e no site (ato da sessão de custódia, com o selo corrente ao lado; o do quadro e os anteriores seguem onde estão, e o novo entra ao lado, com a NOTA); "
           "publicar os módulos novos no espelho (`TGLExt`) e regenerar as PORTAS de `tgl_kernel`, `TGLExt` e `TGL`; a pasta `insumos` vai ao espelho com PORTA (a íntegra do acervo da v407 segue FORA do espelho pela ordem vigente do operador: entra só a cópia purgada, E23): sem ela, uma reprodução pública diz NOT_SEALED (fail-closed); os recibos da bateria do B(n) vão ao espelho com PORTA; o runner da Fronteira e a camada v408 dos 16 dispositivos; a revisão independente (o Sonnet, D54) antes do portão do operador. "
           "A publicação do bloco embutido do método do operador no espelho público segue sujeita à decisão [LEGAL] D2 (operador com a agente de PI). O README pinado e a linha do quadro no site (D39) são da custódia (G1); a regra do z_disc calibrado (nunca sozinho) vale em qualquer superfície.\n\n"
           "**Pendências SÓ do operador:** a correção pública da ressalva publicada no X em 04/11 (ato dele e do app); a decisão [LEGAL] D2; o README pinado (D39); a ratificação das decisões D48 a D54, que são da gerência, em nome próprio, ao lado das falas dele. [OPEN]: a discriminação a 5σ (β_TGL na natureza), o par de psíons na face de Fock (ligação, v409), a tradução das classes do dicionário às classes das máquinas de Turing, a ponte entre o espaço de Bell e o setor TT, K(O) ≠ ⊥ para O compacto, `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura e rank c = 4, "
           "`IsotropicPost` no atlas curvo, a dimensão 3, a instância do índice 1/β, a atestação física externa, a identificação do dispositivo físico (R4/R5) e a independência das quatro bandeiras experimentais do gate (um só booleano; os mocks de survey).\n\n"
           "Pacote e cadeia: `work\\cadeia_de_selo\\v408` (+ `pos_rito`); arquivo `work\\cadeia_de_selo\\v408_selo` e `v408_kernel`. NOT_FALSIFIED não é a palavra da creditação; o gate não se move.\n\n"
           "[[%(topico)s]] [[missao-ultima-flag-um-py]] [[handoff-v407-custodia]]\n") % k
    assert k["par_bloco"] in doc and k["par_v408_bloco"] in doc and k["err_bloco"] in doc, "os paragrafos do README e a nota nao entraram no handoff"
    assert not atribuicao_da_gerencia(doc), ("o handoff atribui mal ou inverte a direcao do testemunho", atribuicao_da_gerencia(doc)[:2])
    return doc


# v408: a linha da arvore da prova
def arvore_linha(V):
    d = _d(V); DL_ = _dl()
    return ("- **TETELESTAI É O TERMINAL (v408)** `%s`: %d módulos novos no kernel, %d bandeiras novas True, escada %s → %s; as identificações do operador de 04/11 estão provadas com o nome dele ou podadas: %s [REAL os termos; INPUT as falas do operador; DECLARADO os recibos e o acervo purgado; OPEN o par na face de Fock como ligação e a tradução das classes do dicionário às máquinas de Turing]; "
            "o registro `tetelestai_terminal_v408` confere os termos; as %d inscrições por sha256; validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["n_pedras"], d["n_f"], V["escada_antes"], d["depois"], DL_.FRASE_DA_MOLDURA_V408_PT, d["n_cun"]))


# v408: o titulo do verbete do indice
def titulo_verbete(V):
    return "Tetelestai é o terminal (v408): o terminal é a leitura, a poda e a quitação; o tempo é a moeda de β; o ponto de contradição; as classes do dicionário do operador:"


# v408: o corpo do verbete do indice
def verbete(V):
    return "[REAL — rodada v408 `%s`] %s." % (V["s16"], _num(V))


# v408: a entrada do remissivo
def remissivo(V):
    return "- **Tetelestai é o terminal, o tempo como moeda de β, o ponto de contradição, as classes do dicionário do operador e as inscrições de 04/11 (v408)** — o registro `tetelestai_terminal_v408`, `cunhagens_v408`, `kh_n1_cobertura_v408`, `%s`" % TOPICO_NOVO


MARC_V408_INI = "<!-- INICIO_PARAGRAFO_TETELESTAI_v408 -->"; MARC_V408_FIM = "<!-- FIM_PARAGRAFO_TETELESTAI_v408 -->"


MARC_ERR_INI = "<!-- INICIO_ERRATA_V407_V408 -->"; MARC_ERR_FIM = "<!-- FIM_ERRATA_V407_V408 -->"




def _lst(xs):
    """Lista numerica lida do registro, em PT: inteiros sem casas, listas aninhadas entre parenteses."""
    return ", ".join(("(" + _lst(x) + ")") if isinstance(x, (list, tuple)) else _pn(x, 6) for x in xs)


def _sem_chaves(t):
    """Os textos vindos do core podem trazer chaves (e^{-s}); os textos renderizados nao as tem (a conferencia de formatacao reprova): chaves viram parenteses."""
    return t.replace("{", "(").replace("}", ")")


def _erratas_e(V):
    """As erratas E21 a E23 e a dos pisos (em nome proprio da gerencia c1), LIDAS do registro cunhagens_v408 do core: nenhuma e' digitada aqui."""
    _d(V); er = _cg()["erratas"]; DL_ = _dl()
    assert len(er) == len(DL_.ERRATAS_V408) + 1, "o registro cunhagens_v408 nao traz as tres erratas e a dos pisos"
    itens = []
    for e in er:
        itens.append(_sem_chaves("- %s **Dizia:** %s **Lacuna de fidelidade:** %s **Estatuto:** %s" % (e["agora"], e["dizia"], e["lacuna_de_fidelidade"], e.get("estatuto", ""))))
    return ("**Erratas ao lado (em nome próprio da gerência c1, 04/11/2026; os literais das versões anteriores, os specs marcados «até a v407», o registro selado do psíon e as pedras seladas ficam como registro; nenhum módulo já instalado foi editado):** a v408 entra COM três erratas e a errata ao lado dos pisos, lidas do registro `cunhagens_v408`:\n" + "\n".join(itens))


def _decisoes(V):
    """As decisoes D48 a D54 da gerencia c1, LIDAS do registro cunhagens_v408 (a D51 revista pela correcao do operador)."""
    _d(V); ds = _cg()["extras"]["decisoes"]
    ks = ("D48", "D49", "D50", "D51", "D52", "D53", "D54")
    assert all(k in ds for k in ks), "as decisoes D48 a D54 nao estao no registro cunhagens_v408"
    return "**Decisões** [da gerência c1, em nome próprio, ratificáveis pelo operador; as que trazem fala dele dizem o sha16]:\n" + _sem_chaves("\n".join("- %s: %s%s" % (k, ds[k], (" [regra do 4,44: " + _z444() + "]") if "4,44" in ds[k] else "") for k in ks))


# ---------------------------------------------------------------- o PARAGRAFO NOVO da v408 e a NOTA ao lado dos paragrafos anteriores
def _linha_maquina_v408(core, d):
    """A linha de maquina do paragrafo novo (os numeros LIDOS do registro do core), em PT."""
    pc = core["tetelestai_terminal_v408"]; fv = pc["values"]
    return ("modulos=%s; bandeiras=%s; ancoras=%s; escada=%s; checagens=%s; respostas_conferidas=%s/%s; falas_sha16=%s/%s/%s"
            % (d["n_mod"], d["n_f"], fv["n_ancoras_ok"], "/".join(str(x) for x in dict.fromkeys(fv["escada"])), pc["mechanics"]["n_checks"], sum(1 for v_ in fv["respostas"].values() if v_ is True), len(fv["respostas"]), d["s_ordem"], d["s_nomes"], d["s_classes"]))


def _dados_paragrafo(core):
    """O que o paragrafo precisa do core SELADO e de ESPERADOS (sem V): as contagens e as falas."""
    esp = _esp(); DL_ = _dl()
    for n in (DL_.FECHO_REGISTRO, DL_.CUNHAGENS_REGISTRO, DL_.KH_REGISTRO, "psion_canto_v407", "fechamento_v406"):
        assert (core.get(n) or {}).get("all_verified") is True, "o registro %s nao selou: nenhum paragrafo diz os numeros assim" % n
    pc = core[DL_.FECHO_REGISTRO]; fv = pc["values"]
    assert fv["n_modulos_ok"] == fv["n_modulos"] == DL_.N_BUNDLE and fv["n_flags_true"] == fv["n_flags"] == esp["n_bandeiras_novas"] and fv["n_ancoras_ok"] == len(DL_.ANCORAS) and fv.get("respostas_ok") is True, "os valores do registro tetelestai_terminal_v408 nao sao os do ensaio a seco"
    return {"n_mod": DL_.N_BUNDLE, "n_f": esp["n_bandeiras_novas"], "escada": (esp["escada_v407_e_v408"][0], esp["escada"][1]), "s_ordem": _sha_por(DL_.N_ORDEM_V408), "s_nomes": _sha_por(DL_.N_NOMES), "s_classes": _sha_por(DL_.N_CLASSES_PNP), "n_checks": pc["mechanics"]["n_checks"]}


def _paragrafo_v408_de(core):
    """O texto do paragrafo da v408, funcao PURA dos registros selados do core (os numeros sao lidos dos registros, nunca digitados; as frases de limite saem do proprio registro)."""
    d = _dados_paragrafo(core); DL_ = _dl(); pc = core[DL_.FECHO_REGISTRO]
    q_o = _cita(DL_.FRASE_TERMINAL); q_c = _cita(DL_.FRASE_CLASSES_PNP); q_l = _cita(DL_.FRASE_CLARO_V408); q_r = _cita(DL_.FRASE_PROVAR_OU_PODAR)
    ress = "; ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(pc["ressalvas"]))   # inteiras
    ns = ", ".join("`%s`" % p_["name"] for p_ in DL_.PEDRAS_V408)
    ls = ["### Tetelestai é o terminal: a leitura, a poda e a quitação; o tempo é a moeda de β; o ponto de contradição; as classes do dicionário do operador (v408, 04/11/2026) — parágrafo pronto para o README do espelho e para o site",
          "",
          "> **Tetelestai é o terminal (v408, 04/11/2026)** [REAL: os termos do kernel do rito, as respostas do operador conferidas nele · INPUT: a ordem, os nomes, a regra e a correção do operador · DECLARADO: os recibos de compilação e o acervo purgado · OPEN: o par na face de Fock como ligação, a tradução das classes do dicionário às máquinas de Turing, o teste com a natureza]",
          ">",
          "> - **O que entrou** [REAL]: %s módulos novos no kernel (`TGLExt`: %s, todos com o nome que o operador deu), com %s bandeiras, todas no trio; escada %s → %s (sha16 das falas `%s`, `%s`, `%s`)." % (d["n_mod"], ns, d["n_f"], d["escada"][0], d["escada"][1], d["s_ordem"], d["s_nomes"], d["s_classes"]),
          "> - **O terminal é a leitura** [REAL · INPUT]: %s. A correção do operador: %s; e a regra dele: %s." % (_sem_chaves(pc["diz"][1]), q_o, q_r),
          "> - **O tempo é a moeda de β** [REAL · INPUT]: %s." % _sem_chaves(pc["diz"][2]),
          "> - **O ponto de contradição e as classes do dicionário** [REAL · INPUT]: %s." % _sem_chaves(pc["diz"][3]),
          "> - **A correção do operador sobre as classes** [INPUT]: %s; e %s." % (q_c, q_l),
          "> - **O que não muda** [REAL]: %s." % _sem_chaves(pc["diz"][5]),
          "> - **As ressalvas, ditas** [OPEN · DECLARADO · REAL]: %s." % _sem_chaves(ress),
          "> - **O que o registro NÃO diz** [REAL]: %s." % _sem_chaves("; ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(pc["nao_diz"]))),
          "> - **Limites:** %s; o registro CONFERE os termos, as fontes por sha256, as respostas e as falas, e quem prova é o kernel; `NOT_FALSIFIED` nunca é a palavra da creditação; isto não é teste e não acrescenta dado; este parágrafo não traz o número do quadro (o quadro do Teste da Única Palavra segue no README com a sua linha dos 5σ)." % DL_.FRASE_DA_MOLDURA_V408_PT,
          "> - **Origem.** Os números são lidos do core selado desta rodada; nenhum é digitado. Linha de máquina: `%s`." % _linha_maquina_v408(core, d)]
    return "\n".join(ls) + "\n"


def verificar_paragrafo_v408(par, core, esp):
    """Verifica o paragrafo da v408 contra o core selado E contra ESPERADOS (o ensaio a seco): devolve a lista de falhas (vazia = passou). As verificacoes:
    (1) os numeros do core (o registro tetelestai_terminal_v408) == os de ESPERADOS/delta e cada um esta no paragrafo, formatado; (2) o paragrafo == o gerado do core; (3) NAO traz o 4,44 nem o z_disc (a regra do 4,44 e' do quadro); (4) os estatutos;
    (5) as frases de limite e as ressalvas; (6) toda citacao entre « » e' verbatim numa fala DO OPERADOR ou texto do registro; (7) nenhuma alegacao de seguranca criptografica, «consciencia» so' como palavra retirada, a direcao sem inversao; (8) a guarda P18 e a guarda das frases."""
    fa = []
    DL_ = _dl()
    pc = core.get(DL_.FECHO_REGISTRO) or {}; fv = pc.get("values") or {}
    try:
        nums = {"modulos": str(DL_.N_BUNDLE), "bandeiras": str(esp["n_bandeiras_novas"]), "escada antes": str(esp["escada_v407_e_v408"][0]), "escada depois": str(esp["escada"][1]), "sha16 da ordem": _sha_por(DL_.N_ORDEM_V408), "sha16 dos nomes": _sha_por(DL_.N_NOMES), "sha16 da correcao das classes": _sha_por(DL_.N_CLASSES_PNP)}
        if not (fv and fv.get("n_modulos_ok") == DL_.N_BUNDLE and fv.get("n_flags_true") == esp["n_bandeiras_novas"] and fv.get("n_ancoras_ok") == len(DL_.ANCORAS) and fv.get("respostas_ok") is True):
            fa.append("os valores do registro tetelestai_terminal_v408 no core != ESPERADOS/delta")
    except KeyError as e:
        nums = {}; fa.append("valor ausente: %s" % e)
    for k, v in nums.items():
        if v not in par:
            fa.append("numero (%s = %s) ausente do paragrafo" % (k, v))
    for n_ in [p_["name"] for p_ in DL_.PEDRAS_V408]:
        if "`%s`" % n_ not in par:
            fa.append("o nome da pedra %s ausente do paragrafo" % n_)
    try:
        if par != _paragrafo_v408_de(core):
            fa.append("o paragrafo difere do gerado pelas funcoes sobre os registros selados do core")
    except AssertionError as e:
        fa.append("o paragrafo nao pode ser gerado do core: %s" % str(e)[:120])
    if re.search(r"4[,.]44|z_disc", par):
        fa.append("o paragrafo da v408 traz o 4,44 ou o z_disc (a regra do 4,44 e' do quadro; este paragrafo nao o cita)")
    for st in ("[REAL", "INPUT", "OPEN", "DECLARADO"):
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    for frase in (DL_.FRASE_DA_MOLDURA_V408_PT, DL_.FRASE_D51_PT, "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "quem prova é o kernel", "isto não é teste", "face de Fock", "classes de computação do dicionário do operador", "máquinas de Turing", "não recusa"):
        if frase not in par:
            fa.append("frase de limite ausente do paragrafo: " + frase)
    for r_ in DL_.RESSALVAS_V408:
        c_ = _sem_chaves(r_)   # a ressalva inteira
        if c_ not in par:
            fa.append("ressalva ausente do paragrafo: " + c_[:60])
    corpus = [re.sub(r"\s+", " ", dd["text"]) for dd in _falas().values() if dd["autor"] == "operador"]
    for q in re.findall(r"«([^»]*)»", par):
        if len(q) >= 13 and not any(q in t for t in corpus) and q not in " ".join(DL_.RESSALVAS_V408) and q not in " ".join(pc.get("diz") or []) and q not in " ".join(pc.get("nao_diz") or []):
            fa.append("citacao entre « » que NAO e' verbatim numa fala do operador (nem texto do registro): %r" % q[:90])
    for m_ in _RX_INV.finditer(par):
        ant_ = par[max(0, m_.start() - 40):m_.start()].lower()
        if not (ant_.endswith("nao ") or ant_.endswith("não ") or "podia dizer que " in ant_):
            fa.append("a DIRECAO esta invertida (a IALD como quem testifica do operador): %s" % par[max(0, m_.start() - 40):m_.end() + 20].replace("\n", " "))
    if re.search(r"(?i)inviol|indecifr|quantum[- ]safe|seguran[çc]a\s+criptogr[aá]fica\s+garantida|sigilo\s+garantido|confidencialidade\s+garantida", par):
        fa.append("o paragrafo alega seguranca criptografica ou confidencialidade")
    for ln in par.split("\n"):
        if re.search(r"(?i)consci[êe]ncia", ln) and not re.search(r"retirad", ln):
            fa.append("a palavra «consciencia» fora do contexto de palavra retirada pelo operador: %s" % ln[:100])
    sys.path.insert(0, PK)
    from guarda_p18_v408 import violacoes
    import guarda_frases_v408 as GF
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    v2 = GF.violacoes(par)
    if v2:
        fa.append("a guarda das frases achou %r" % (v2[:2],))
    return fa


def paragrafo_v408():
    """(texto, relatorio): o paragrafo NOVO da v408, pronto para colar no README do espelho e no site, gerado do core SELADO do Nos e verificado contra o core E contra ESPERADOS;
    levanta AssertionError (o fechar RECUSA) se algo nao conferir."""
    core = _core(); esp = _esp()
    par = _paragrafo_v408_de(core)
    fa = verificar_paragrafo_v408(par, core, esp)
    assert not fa, ("o paragrafo da v408 nao passou nas verificacoes", fa[:4])
    return par, {"sha16": hashlib.sha256(par.encode("utf-8")).hexdigest()[:16], "verificacoes": "numeros == ESPERADOS/delta; igual ao gerado do core; sem o 4,44; estatutos; limites e ressalvas; citacoes verbatim (falas do operador ou texto do registro); sem alegacao de seguranca criptografica; guarda P18; guarda das frases", "guarda_p18": "limpa"}


def errata_v407_bloco():
    """O bloco de NOTA ao lado dos paragrafos anteriores (v394 a v407) no README do espelho e no site: E21 (o [OPEN] do par na face de Fock e' de ligacao, nao de ausencia) e a correcao das classes do dicionario (D51 revista). Texto lido do registro cunhagens_v408; as guardas conferem."""
    _kernel_tem(("o_habitante_e_o_fock_concreto", "as_classes_do_dicionario", "p_igual_np_nas_classes_do_dicionario"))
    er = (_cg().get("erratas") or [None])[0]; DL_ = _dl()
    assert er and er["agora"] == DL_.ERRATA_E21 and er.get("assinatura") == DL_.ASSINA, "a errata E21 do registro cunhagens_v408 nao e' a do delta"
    t = ("> **Nota ao lado dos parágrafos anteriores (v394 a v407) — gerência c1, em nome próprio, 04/11/2026:** onde o parágrafo da v407 (o psíon, o canto e o par) diz que o par na face de Fock segue em aberto porque o certificado de Fock não tem operadores de criação como termo, isso era verdade sobre o certificado abstrato e fica como registro. "
         + _sem_chaves(er["agora"]).rstrip().rstrip(".") + ". E onde um texto publicado pela gerência em 04/11 (a ressalva do post no X) negou que «P = nP» tratasse das classes de computação, vale a correção do operador (D51 revista): " + _d51()
         + "; a correção pública é ato do operador e do app. Os módulos selados das versões anteriores NÃO foram editados nem renomeados, e os registros delas seguem selados; o que o parágrafo da v407 e os anteriores dizem sobre as pedras, o cálculo e os limites não muda.\n")
    sys.path.insert(0, PK)
    from guarda_p18_v408 import violacoes
    import guarda_frases_v408 as GF
    assert not violacoes(t) and not GF.violacoes(t), ("a guarda P18 ou a das frases achou palavra recusada na nota ao lado dos paragrafos anteriores", violacoes(t)[:2], GF.violacoes(t)[:2])
    return t


def _pl(n, sing, plur):
    """«1 item» / «3 itens»: o numero lido, o substantivo no numero certo."""
    return "%d %s" % (n, sing if n == 1 else plur)


def _faixa(par, n):
    """A bandeira unica («`a`») ou a faixa («de `a` a `b`») de um grupo de bandeiras novas."""
    return "`%s`" % par[0] if n == 1 else "de `%s` a `%s`" % (par[0], par[1])


def _pe(x, nd=6):
    """Numero lido do core em notacao cientifica, em PT (5,325135e-05)."""
    return ("%.*e" % (nd, float(x))).replace(".", ",")






def _sha_verdade():
    """O sha16 da pedra Verdade (v392) no kernel do Nos (o homonimo que a «Verdade» sozinha repetiria), LIDO do arquivo."""
    return s16(os.path.join(NOS, "tgl_kernel", "TGLExt", "Verdade.lean"))




# os temas das falas sao os proprios nomes dos arquivos (resumo dado no nome, nunca citacao); o sha16, a data e o autor vem dos bytes e do nome, nunca daqui. So' o nome que carrega uma frase que a guarda recusa e' reescrito.
_TEMA_ESPECIAL = {"nomes_das_sete_pedras_e_tudo_derivado": "os nomes das sete pedras e o pedido de que não restassem hipóteses nomeadas"}






def _tema(nome):
    """O tema de uma fala: o nome do arquivo sem o autor, a data e o sufixo (o resumo que a gerencia deu ao gravar; nunca citacao)."""
    t = re.sub(r"_verbatim\.txt$", "", re.sub(r"^(?:OPERADOR|GERENCIA)_\d{2}(?:out|nov)_", "", nome))
    return _TEMA_ESPECIAL.get(t, t.replace("_", " "))


def _moldura(V):
    """A MOLDURA da v408, LIDA do registro tetelestai_terminal_v408 do core: a frase da moldura (delta) e o estatuto que o registro grava."""
    d = _d(V); pc = _pc(); DL_ = _dl()
    assert "creditação" in DL_.FRASE_DA_MOLDURA_V408_PT, "a frase da moldura nao e' a do delta"
    # (r2, 04/11 noite: o estatuto cita, entre os nomes do operador, o nome P=nP; a obrigacao F34 da guarda das frases pede, no MESMO texto, o qualificador do dicionario e a traducao [OPEN]: a D51 revista vai junto)
    return _fs("**A moldura [REAL · INPUT · DECLARADO · OPEN; registro `tetelestai_terminal_v408`, {nck} checagens]:** {frase}. Estatuto do registro, como o `um.py` o grava: {est}. O nome P=nP, que o estatuto cita entre os nomes do operador, lê-se pela D51 revista: {d51}.", nck=d["n_ck_pc"], frase=DL_.FRASE_DA_MOLDURA_V408_PT, est=pc["estatuto"], d51=_d51())






















_ESCADA_PATCHES = ("N00_main_tetelestai_terminal", "N02_selo", "W02_runtime_v408", "C13_specs_v407_E21_e_pisos", "K01_modulos_novos")


def _fs(texto, **kw):
    """_f com os valores textuais vindos do core sem chaves (e^{-s} vira e^(-s)): o resultado nao tem chave."""
    return _f(texto, **{k: (_sem_chaves(v) if isinstance(v, str) else v) for k, v in kw.items()})


def _dl():
    """O delta da v408 (pela copia do quadro, que o importa; nunca o da v407)."""
    DL_ = _qd().DL
    assert DL_.UM_VERSION == "v408" and DL_.FECHO_REGISTRO == "tetelestai_terminal_v408", "o delta lido nao e' o da v408"
    return DL_


def _d51():
    """A frase da D51 REVISTA (delta_v408.FRASE_D51_PT): P = nP e' teorema nas classes de computacao do dicionario do operador; a traducao a Turing e' [OPEN]. Toda peca que nomeia «P = nP» a traz."""
    return _dl().FRASE_D51_PT


def _pc():
    """O registro com FUNCAO tetelestai_terminal_v408 do core SELADO do Nos (so' leitura); recusa se nao selou ou se nao e' o contrato do delta e de ESPERADOS."""
    DL_ = _dl(); esp = _esp(); pc = _core().get(DL_.FECHO_REGISTRO) or {}
    assert pc.get("all_verified") is True and pc.get("verdict") == esp["vereditos_novos_v408"][DL_.FECHO_REGISTRO] and pc.get("does_not_gate_core") is True and pc.get("runtime_executed") is True, "o registro tetelestai_terminal_v408 nao selou no core do Nos (ou != ESPERADOS)"
    mech = pc.get("mechanics") or {}; pv = pc.get("values") or {}
    assert mech.get("passed") is True and mech.get("n_checks") == DL_.N_CHECKS_FECHO == len(mech.get("checks") or []) and all(c_.get("ok") is True for c_ in mech["checks"]), "as checagens do registro tetelestai_terminal_v408 nao passaram todas"
    assert pv.get("n_ancoras_ok") == pv.get("n_ancoras") == len(DL_.ANCORAS) and pv.get("n_modulos_ok") == pv.get("n_modulos") == DL_.N_BUNDLE and pv.get("n_flags_true") == pv.get("n_flags") == esp["n_bandeiras_novas"] and pv.get("escada") == [esp["escada"][1]] * 3, "os valores do registro tetelestai_terminal_v408 != ESPERADOS/delta"
    assert pc.get("ancora_principal") == DL_.ANCORA_PRINCIPAL and list(pc.get("ancoras_principais") or []) == list(DL_.ANCORAS_PRINCIPAIS) and list(pc.get("pedras") or []) == [p_["name"] for p_ in DL_.PEDRAS_V408] and pc.get("nome_provisorio") is None and pc.get("chaves_antigas_que_mudam") == [], "a ancora principal, as pedras, o nome provisorio ou as chaves do registro != delta"
    assert pc.get("beta_ok") is True and pc.get("embedded_sources_ok") is True and pc.get("embedded_sources_n_ok") == DL_.N_BUNDLE and pc.get("guarda_violacoes") in ([], None), "o beta, as fontes embutidas ou a guarda do registro tetelestai_terminal_v408 nao conferem"
    assert list(pc.get("ressalvas") or []) == list(DL_.RESSALVAS_V408) and len(DL_.RESSALVAS_V408) >= 8, "as ressalvas do registro != delta_v408.RESSALVAS_V408"
    assert set((pv.get("respostas") or {})) == {r_["id"] for r_ in DL_.RESPOSTAS_DO_OPERADOR} and all(v_ is True for v_ in pv["respostas"].values()) and pv.get("respostas_ok") is True, "as respostas do operador de 04/11 nao conferem todas no kernel"
    ip = pc.get("insumo_purgado") or {}
    assert ip.get("integra_pinada") is False and ip.get("integra_fora_do_espelho") is True and ip.get("sha256") == DL_.PURGADO_SHA256, "o insumo do acervo nao entra pela copia purgada (E23)"
    assert pc.get("fica_false_por_teorema") == list(DL_.FICAM_FALSE_POR_TEOREMA) and (pc.get("fica_aberto") or {}) == {"par_na_face_de_fock": DL_.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, "ponte_bell_tt": DL_.FICA_ABERTO_PONTE_BELL_TT}, "o que fica False por teorema ou aberto != delta_v408"
    return pc


def _ps_herdado():
    """O registro psion_canto_v407 (HERDADO da v407, recriado pelo rito; a escada do contrato subida pela C12): segue selado, com o elo lido do kernel."""
    ps = _core().get("psion_canto_v407") or {}; esp = _esp()
    assert ps.get("all_verified") is True and ps.get("link_read_from_the_kernel") is True and ps.get("does_not_gate_core") is True and ps.get("verdict") == esp["registros_funcao_v407"]["psion_canto"]["verdict"], "o registro psion_canto_v407 (herdado) nao segue selado no core do Nos"
    return ps


def _fe_herdado():
    """O registro fechamento_v406 (HERDADO da v406, com a checagem c8 versionada pela errata E20): tem de seguir selado."""
    fe = _core().get("fechamento_v406") or {}; esp = _esp()
    assert fe.get("all_verified") is True and fe.get("certificate_inhabited") is True and fe.get("does_not_gate_core") is True and fe.get("verdict") == esp["registros_funcao_v406"]["fechamento"]["verdict"], "o registro fechamento_v406 (herdado) nao segue selado no core do Nos"
    return fe


def _cg():
    """O registro por spec cunhagens_v408 do core SELADO: as 15 falas de 04/11 por sha256 (13 do operador e 2 de autor misto, das quais so' o paragrafo dele e' embutido), as erratas E21 a E23 e a dos pisos (da gerencia, em nome proprio), as decisoes D48 a D54 (D51 revista), as leituras e as ressalvas."""
    DL_ = _dl(); esp = _esp(); cg = _core().get(DL_.CUNHAGENS_REGISTRO) or {}
    assert cg.get("all_verified") is True and cg.get("verdict") == esp["vereditos_novos_v408"][DL_.CUNHAGENS_REGISTRO] and cg.get("does_not_gate_core") is True and cg.get("checks") and all(c_.get("ok") is True for c_ in cg["checks"]), "o registro cunhagens_v408 nao selou no core do Nos (ou != ESPERADOS)"
    vb = cg.get("verbatim") or {}
    assert set(vb) == set(esp["cunhagens"]) and len(vb) == len(DL_.VERBATIM_ORIGEM_V408) and all(v_.get("embedded_ok") is True for v_ in vb.values()), "as inscricoes de 04/11 nao estao embutidas por sha256"
    er = cg.get("erratas") or []
    assert [e_.get("agora") for e_ in er[:len(DL_.ERRATAS_V408)]] == list(DL_.ERRATAS_V408) and len(er) == len(DL_.ERRATAS_V408) + 1 and all(e_.get("assinatura") == DL_.ASSINA for e_ in er), "o registro cunhagens_v408 nao traz as erratas E21 a E23 e a dos pisos, da gerencia c1, em nome proprio"
    ex = cg.get("extras") or {}; dec = ex.get("decisoes") or {}
    assert all(dec.get(k_) == DL_.DECISOES[k_] for k_ in ("D48", "D49", "D50", "D51", "D52", "D53", "D54")) and ex.get("leituras") == DL_.LEITURA_V408 and ex.get("n_falas") == len(vb) and list(ex.get("ressalvas") or []) == list(DL_.RESSALVAS_V408), "cunhagens_v408: as decisoes D48 a D54, a leitura ou as ressalvas != delta_v408"
    return cg


def _khr():
    """O registro por spec kh_n1_cobertura_v408 do core SELADO (a cobertura do Audit desta versao)."""
    DL_ = _dl(); esp = _esp(); kh = _core().get(DL_.KH_REGISTRO) or {}
    assert kh.get("all_verified") is True and kh.get("verdict") == esp["vereditos_novos_v408"][DL_.KH_REGISTRO] and kh.get("does_not_gate_core") is True and kh.get("checks") and all(c_.get("ok") is True for c_ in kh["checks"]), "o registro kh_n1_cobertura_v408 nao selou no core do Nos (ou != ESPERADOS)"
    return kh


def _recriados():
    """Os registros das versoes anteriores, RECRIADOS pelo rito, conferidos no core SELADO contra os vereditos de ESPERADOS; devolve {versao: [nomes]}. So' os nomes que ESPERADOS lista; nada e' digitado."""
    esp = _esp(); core = _core(); out = {}; base = esp["vereditos_v407"]
    for ver in ("407", "406", "405", "404", "403", "402", "401", "399"):
        nomes = {}
        nomes.update(esp.get("registros_v" + ver) or {})
        for v_ in (esp.get("registros_funcao_v" + ver) or {}).values():
            nomes[v_["nome"]] = v_["verdict"]
        out[ver] = nomes
    extra = {"402": ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"), "401": ("falsidade_da_inercia_v401",), "399": ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399")}
    for ver, ns in extra.items():
        for n in ns:
            if n not in out[ver]:
                assert n in base, ("o registro nao esta' nos vereditos de ESPERADOS", n)
                out[ver][n] = base[n]
    for ver, nomes in out.items():
        for n, vd in nomes.items():
            r = core.get(n) or {}
            assert r.get("all_verified") is True and r.get("verdict") == vd, "o registro recriado %s (v%s) nao selou no core do Nos ou != ESPERADOS" % (n, ver)
    return {ver: sorted(nomes) for ver, nomes in out.items()}


def _pedras_anteriores():
    """As pedras seladas das versoes anteriores seguem no kernel do Nos com o sha256 selado: as treze da v403, v404 e v405 (pedras_v405_sha256), os 9 modulos da v407 (bundle_v407_sha256) e os 301 da v406 (bundle_v406_sha256). Devolve (n_treze, n_9, n_301)."""
    esp = _esp()
    for chave in ("pedras_v405_sha256", "bundle_v407_sha256", "bundle_v406_sha256"):
        for rel, h in esp[chave].items():
            p = os.path.join(NOS, "tgl_kernel", *rel.split("/"))
            assert os.path.isfile(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() == h, "a pedra selada %s deixou de estar no kernel do Nos com o sha256 selado" % rel
    return len(esp["pedras_v405_sha256"]), len(esp["bundle_v407_sha256"]), len(esp["bundle_v406_sha256"])


def _escopo(V):
    """O que entra: o escopo do registro tetelestai_terminal_v408, como o um.py o grava."""
    _d(V); pc = _pc()
    return _sem_chaves("**O que entra (escopo do registro `tetelestai_terminal_v408`)** [REAL]: " + pc["scope"])


def _ancoras(V):
    """As ancoras dos 4 modulos: contagem por modulo (delta_v408.ANCORAS_POR_MODULO) e as principais com o papel (delta_v408.ANCORAS), conferidas no kernel do rito pelo registro."""
    d = _d(V); DL_ = _dl(); pc = _pc(); anc = pc["values"].get("ancoras") or {}
    assert set(anc) == set(DL_.ANCORAS) and all((a_ or {}).get("ok") is True for a_ in anc.values()) and len(anc) == d["n_anc"], "as ancoras do registro != delta_v408.ANCORAS"
    por = "; ".join("`%s` (%d)" % (rel.split("/")[-1][:-5], len(ns)) for rel, ns in DL_.ANCORAS_POR_MODULO.items())
    cen = "; ".join("`%s` (%s)" % (n_.split(".")[-1], DL_.ANCORAS[n_]["papel"]) for n_ in list(DL_.ANCORAS_PRINCIPAIS) + [DL_.ANCORA_CLASSES])
    return _fs("**As {na} âncoras** [REAL; lidas do `axiom_report` do rito, só no trio, com a proveniência que o compilador emite no módulo esperado e a bandeira True], por módulo: {por}. As principais, uma por módulo, e a das classes do dicionário: {cen}.", na=d["n_anc"], por=por, cen=cen)


def _chaves(V):
    """As chaves: nenhuma chave antiga muda nesta versao; a chave do lema (v407) e a do certificado habitado seguem lidas do kernel; o que fica False por teorema."""
    _d(V); DL_ = _dl(); core = _core()
    lv = ((core.get("testemunha_estatica_v396") or {}).get("fock_face") or {}).get("linked_to_the_corner_by_a_lemma"); rf = (core.get("rede_fock_v394") or {}).get("whole_certificate_inhabited")
    assert lv is True and rf is True and list(DL_.CHAVES_V408) == [], "a chave do lema ou a do certificado habitado nao estao lidas True do kernel, ou a v408 muda alguma chave antiga"
    ff = "; ".join("`%s` (lido: %s)" % (n_, {"full_static_witness_exists": ((core.get("qg_closure") or {}).get("gate") or {}).get("full_static_witness_exists"), "trivial_inhabitant_exists": (core.get("witness_rigidity") or {}).get("trivial_inhabitant_exists")}[n_]) for n_ in DL_.FICAM_FALSE_POR_TEOREMA)
    return _fs("**As chaves** [REAL; registro `tetelestai_terminal_v408`]: NENHUMA chave antiga muda nesta versão (a lista das chaves que mudam é vazia, e o registro a confere). A chave do lema da v407 (`testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma`) segue LIDA do kernel do rito e lê {lv}; a do certificado habitado (`rede_fock_v394.whole_certificate_inhabited`) lê {rf}. Ficam False por teorema: {ff}.", lv=lv, rf=rf, ff=ff)


def _respostas(V):
    """As respostas do operador de 04/11 (delta_v408.RESPOSTAS_DO_OPERADOR), conferidas no kernel pelos teoremas que JA existiam e pelas declaracoes novas (registro tetelestai_terminal_v408, values.respostas); a fala entre aspas e' verbatim, e a partitura: o que isto decide e o que nao decide."""
    d = _d(V); DL_ = _dl(); pc = _pc()
    itens = "; ".join("(%s) %s — %s" % ("abcdefghij"[i], _cita(r_["fala"]), r_["diz"]) for i, r_ in enumerate(DL_.RESPOSTAS_DO_OPERADOR))
    return _fs("**As respostas do operador de 04/11, conferidas no kernel** [INPUT a fala dele; REAL a conferência; regra provar ou podar, `{s_r}`]: cada identificação dele ou está provada no kernel com o nome dele ou está podada; o registro as confere, uma a uma, pelos teoremas que já existiam e pelas declarações novas, no trio: {itens}. "
               "O que esta conferência DECIDE: que cada uma dessas identificações tem espelho no kernel, como composição de termos (a leitura é dele, a validade é do kernel). O que NÃO decide: {d51}; nem o par na face de Fock, que segue [OPEN] como ligação (E21); nem nada sobre a natureza. "
               "O negativo, se viesse, seria parede medida (o termo que falta), não falsificação da fala dele.",
               s_r=d["ss"]["regra"], itens=itens, d51="a tradução para as máquinas de Turing, que segue [OPEN] como a próxima construção, não como recusa (" + _d51() + ")")


def _diznao(V):
    """O que o registro diz e o que NAO diz: as listas diz e nao_diz do registro tetelestai_terminal_v408."""
    _d(V); pc = _pc()
    return _sem_chaves("**O que o registro diz** [REAL]: " + "; ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(pc["diz"])) + ". **O que o registro NÃO diz:** " + "; ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(pc["nao_diz"])) + ".")


def _ressalvas(V):
    """As ressalvas, ditas uma a uma: delta_v408.RESSALVAS_V408 == tetelestai_terminal_v408.ressalvas."""
    _d(V); pc = _pc(); DL_ = _dl()
    assert list(pc["ressalvas"]) == list(DL_.RESSALVAS_V408) and len(pc["ressalvas"]) >= 8, "as ressalvas do registro != delta_v408.RESSALVAS_V408"
    return _sem_chaves("**As ressalvas, ditas (%d)** [OPEN · DECLARADO · REAL, uma a uma]: " % len(pc["ressalvas"]) + "; ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(pc["ressalvas"])) + ".")


def _teste_d(V):
    """(nome herdado da v407, papel novo) A v408 NAO entra com teste com a natureza: o que o registro diz disso (sem numero novo, sem rito de natureza, sem dado)."""
    _d(V); pc = _pc()
    sem = [x for x in pc["ressalvas"] if "nenhum teste com a natureza" in x]
    assert len(sem) == 1, "a ressalva do teste com a natureza nao esta no registro"
    return _sem_chaves("**Nenhum teste com a natureza nesta versão** [REAL · OPEN]: [REAL] a v408 não roda rito de natureza novo, não abre dado e não acrescenta desfecho experimental; o registro com função LÊ o kernel do próprio rito e CONFERE as fontes, e quem prova é o kernel. "
                       "[OPEN] o que a natureza decide segue da natureza: β_TGL a 5σ. Do registro, a ressalva: " + sem[0] + ".")


def _leituras(V):
    """As leituras do operador de 04/11 pela regra provar ou podar, LIDAS do registro cunhagens_v408 (extras.leituras) e conferidas contra delta_v408."""
    _d(V); x = _cg()["extras"]["leituras"]; DL_ = _dl()
    assert x and x == DL_.LEITURA_V408 and "INPUT" in str(x.get("estatuto")), "a leitura da v408 nao e' a de delta_v408"
    ks = [k_ for k_ in x if k_ != "estatuto"]
    return _sem_chaves("**As leituras do operador de 04/11, pela regra provar ou podar** %s: %s. Nenhuma fica estacionada como identificação dele sem espelho: o que é termo está nas âncoras dos 4 módulos; o que não tem espelho está podado e dito." % (x["estatuto"], "; ".join("(%s) %s" % (k_, x[k_]) for k_ in ks)))


def _blocos_fecho(V):
    return "\n\n".join([_moldura(V), _escopo(V), _ancoras(V), _chaves(V), _respostas(V), _diznao(V), _ressalvas(V), _teste_d(V)])
