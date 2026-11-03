# -*- coding: utf-8 -*-
# Os TEXTOS da v406 SELADA: O FECHAMENTO (ordem do operador, 02/11/2026, sha16 f3998f01262aad6b: «precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento»). MONTADOS, sem prosa nova de conteudo, do que o core SELADO do rito traz:
# o registro com funcao fechamento_v406 (o diz, o nao_diz, os limites, as ressalvas, as oito ancoras, as quatro chaves de testemunha lidas do kernel, os valores), cunhagens_v406 (as erratas E14 a E17, as decisoes D34 a D40, as leituras de 02/11 e as 23 falas do operador por sha256) e kh_n1_cobertura_v406,
# mais os vereditos, os numeros do kernel (301 modulos novos, 1794 bandeiras, a escada) e as falas; so' os conectivos e os titulos sao escritos aqui. A semente (textos_v405.py com os rotulos subidos) fornece a infraestrutura: leitura dos insumos, citacao verbatim, o quadro do Teste da Unica Palavra, a rodada, o sidecar.
# A MOLDURA em toda peca: o certificado de Fock esta habitado por construcao no kernel do rito (physicalFockCertificate, bancada do ChatGPT 16/10, recompilado do fonte em 02/11); validade no kernel nao e creditacao; o gate nao se move. As RESSALVAS, ditas: K(O) != bot so' na cunha; o «nucleo II_inf» [KNOWN/DECLARADO]; o traco ENNReal ciclico, nao linear; R7 Codex x Codex e a revisao distinta do Sonnet sem compilacao propria;
# R4/R5 fora; duas chaves False por teorema; o lema que falta; o nome CanonicalFullTGLWitnessR1 e' PROVISORIO (os nomes das pedras sao do operador e ele ainda nao a nomeou). Toda superficie passa pela guarda das frases (guarda_frases_v406.py) e pela P18 (guarda_p18_v406.py), com a excecao so' da fala do operador.
# O QUADRO «O Teste da Única Palavra» (v397) PERMANECE no topo do artigo PT/EN e do .md canonico, INTOCADO. Cada numero, hash e veredito entra por chave de V (leitura_v406.ler), por ESPERADOS, pelo core do Nos ou e' LIDO de um arquivo aqui, nunca digitado; o que vai escrito a mao e' so' conectivo, titulo, nome de termo (conferido em tempo de execucao no kernel do Nos, no um.py ou no pacote) e frase curta do operador (conferida palavra por palavra contra os bytes das falas).
# REGRA DA ORDEM DO OPERADOR (23/10/2026, sha16 9b182958a5a7a1bc: reportar o 4,44 no inicio do artigo, no README e em tudo mais; vale em TODO texto que o cite): o 4,44 (z_disc calibrado) NUNCA aparece sem o p calibrado e sem a linha dos 5σ no MESMO item; o paragrafo do QUADRO sai das MESMAS funcoes do quadro (quadro_v397), sobre o core SELADO do Nos. O paragrafo NOVO da v406 NAO traz o 4,44 (a regra: delta_v406.REGRA_DO_4_44).
# Os paragrafos do TESTEMUNHO DE DOIS (v399), da FALSIDADE (v401), da PONTE, DA QUEDA E DA ESPERANCA (v402), de CAMINHO, VERDADE E VIDA (v403), de JO 8,32 (v404) e da MASSA DERIVADA E DA IDENTIDADE DEFINIDA (v405) SEGUEM COMO ESTAO no README do espelho e no site: esta versao NAO os regenera nem os substitui; o handoff da v406 so' o diz e traz a NOTA ao lado deles (E14: as quatro chaves de testemunha eram literal e passaram a leitura do kernel).
# GUARDA: as cinco regras da P18 (guarda_p18_v406.py) rodam sobre cada texto renderizado em superficies_v406.py, fechar_v406.py e registrar_mapa_v406.py e sobre este arquivo na cadeia. A palavra recusada nunca aparece aqui: a recusa e' dita como «creditação».
import hashlib, json, os, re, sys
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V406"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v406 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(PK))          # ...\Central de Patentes\work
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
TOPICO_NOVO = "v406-selada-o-fechamento.md"
# os marcadores entre os quais o handoff traz os PARAGRAFOS PRONTOS do README do espelho e do site: o QUADRO (v397, intocado) com os MESMOS marcadores da v397, e o paragrafo NOVO da falsidade
MARC_PAR_INI = "<!-- INICIO_PARAGRAFO_README_v397 -->"; MARC_PAR_FIM = "<!-- FIM_PARAGRAFO_README_v397 -->"
_NOMES_KERNEL = ("modularCoreInput", "physicalModularCoreInput", "physicalFockCertificate", "physical_trace", "physicalCanonicalNet", "physical_canonical_net_nonzero", "canonicalFullTGLWitness", "canonical_full_witness_inhabited",
                 "cyclicTraceCandidate", "ShiftRelated", "dual_calibration", "normalized_split_exists", "compactPhysicalNet", "FullTGLWitness", "lightNet", "lightRealization")
_MODULOS_KERNEL = ("CanonicalFockModularCoreInputR1", "PhysicalCanonicalNetCompleteR1", "CanonicalFullTGLWitnessR1", "CanonicalFockCyclicTraceCompletionR3", "CanonicalFockFiniteProjectionR3", "CanonicalFockNormalizedSplitR5")
_NOMES_UM = ("SEALED_CODATA_ALPHA", "fechamento_v406", "_v406_certificado_habitado", "cunhagens_v406", "kh_n1_cobertura_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396",
             "prove_qg_closure_gate", "evaluate_quantum_gravity_closure", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386", "angle_status", "GA_WINDOW_STATUS", "prove_ga_mass_audit", "prove_joint_coincidence_result_v3",
             "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "selo_acom_sidecar_v399", "teste_de_veracidade_fase9_v397", "hubble_ratio_opening_v388", "_v397_quadro_md", "_v397_atomos", "_V397_FRASE_444")
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
_CACHE = {}
# a DIRECAO (v399): nenhuma frase pode por a IALD como quem testifica DO operador (fora da fala em que ele a recusa); a mesma regex do conferidor (C12)
_RX_INV = re.compile(r"IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)")
ERRATA_TEOREMAS = "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"   # (a mesma frase de delta_v406.ERRATA_TEOREMAS_PT; o harness confere)


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
    """Cada modulo citado existe como arquivo .lean em TGLExt/ ou em TGLExt/F1Fecho394/ (os 301 modulos do fecho) do Nos."""
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
    """ESPERADOS_v406.json (gerado pelo ensaio a seco do candidato), lido uma vez."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v406.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _core():
    """O core do Nos (so' leitura), para os campos que so' existem depois do rito; ausente e' falha visivel."""
    if "core" not in _CACHE:
        _CACHE["core"] = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["core"]


def _base_core():
    """O core da v405 selada (a copia de bytes em base_v405): de onde saem os numeros da errata ao lado e a medida da proveniencia."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v405", "um_absoluto.json"), encoding="utf-8"))["core"]
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
    """As inscricoes de 30/10 a 01/11 embutidas no um.py: o texto vem do arquivo em insumos/cunhagens e o sha256 e' conferido contra ESPERADOS (fail-closed). Devolve {sha16: {sha16, arquivo, nome, text, autor}};
    o autor sai do NOME do arquivo e e' conferido contra o papel que ESPERADOS registra: nesta versao todas sao falas do operador (nenhuma e' da gerencia)."""
    if "falas" not in _CACHE:
        ec = _esp()["cunhagens"]; out = {}; pasta = os.path.join(PK, "insumos", "cunhagens")
        for k, meta in ec.items():
            s = k[len("v406_cun_"):]
            fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(s + "_")]
            assert len(fs) == 1, ("a inscricao %s nao tem arquivo unico em insumos/cunhagens" % s, fs)
            b = open(os.path.join(pasta, fs[0]), "rb").read()
            assert hashlib.sha256(b).hexdigest() == meta["sha256"] and len(b) == meta["bytes"] and meta["sha256"][:16] == s, "a inscricao %s nao confere com o sha256 de ESPERADOS" % s
            nome = fs[0][len(s) + 1:]
            autor = "gerencia" if nome.startswith("GERENCIA_") else "operador"
            assert autor == "operador" and not str(meta.get("papel", "")).startswith("leitura da gerencia"), ("a v406 nao tem inscricao da gerencia: todas sao falas do operador", s)
            out[s] = {"sha16": s, "arquivo": fs[0], "nome": nome, "text": b.decode("utf-8"), "autor": autor}
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
    """A cobertura do Audit e a arvore formal da v405 selada (o core guardado em base_v405): de onde saem os numeros da errata ao lado dos pisos."""
    if "cov_base" not in _CACHE:
        kf = _base_core()["kernel_formalization"]
        cov = kf["axiom_coverage_v392"]
        _CACHE["cov_base"] = {"decl": cov["decl"], "thm": cov["thm"], "h8": len(kf["formal_files_sha256"]), "axr": len(kf["axiom_report"])}
    return _CACHE["cov_base"]


def _bancada():
    """A geracao do manifesto que a Bancada de producao pina (do recibo pre_selo pinado em PINOS_BN) e a versao que ela pina; o passo e' simples (sem salto e sem cadeia de selos)."""
    p = json.load(open(os.path.join(PK, "PINOS_BN_v406.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v405" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v405 -> v406 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1}


def _proveniencia(esp):
    """A proveniencia que o compilador emite atribui ao modulo da pedra N declaracoes; todas sao NOVAS no axiom_report (nenhuma reatribuida), e o FLAGS_v406.json do sandbox concorda (as contagens de
    publicas, privadas, nomeadas e auxiliares so' existem la')."""
    if "prov" not in _CACHE:
        kf = _core()["kernel_formalization"]; src = kf["declaration_sources_v394"]; pedras = set(esp["bundle_sha256"])
        b0 = _base_core()["kernel_formalization"]; axr0 = b0["axiom_report"]
        mine = sorted(n for n, p in src.items() if p in pedras)
        novas = [n for n in mine if n not in axr0]
        fj = json.load(open(os.path.join(PK, "kernel", "FLAGS_v406.json"), encoding="utf-8"))
        assert len(mine) == fj["decl_totais_modulos_novos"] and len(novas) == fj["decl_novas_dos_modulos"] == len(mine) and not fj["reatribuidas_as_pedras"], ("a proveniencia do rito != FLAGS_v406.json do sandbox", len(mine), len(novas), fj["reatribuidas_as_pedras"])
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
    """Os numeros da v406, todos LIDOS (V da leitura da rodada, ESPERADOS, core do Nos, base v405, FLAGS do sandbox, os registros): nenhum e' digitado aqui. Recusa se as contagens nao fecham."""
    _conferir_nomes()
    esp = _esp(); tv = V["veracidade"]; sa = V["selo"]; dc = V["declaracao"]; cg = V["cunhagens"]; sc = V["sidecar"]; core = _core(); gt = V["gate"]; gv = gt["values"]; fb = V["f2b"]; fe = V["fecho"]
    DL_ = _qd().DL
    mods = sorted(p["modulo"] for p in V["pedras"])
    assert mods == sorted(DL_.BUNDLE_MODS) and V["n_pedras"] == len(mods) == esp["kernel"]["modulos_novos"] == DL_.N_BUNDLE and all(p_["ok"] is True for p_ in V["pedras"]), ("o delta da v406 e' o bundle dos modulos novos, cada um com o sha256 pinado", len(mods))
    nf = esp["n_bandeiras_novas"]; grp = esp["n_bandeiras_por_grupo"]
    assert grp == {DL_.GRUPO_BUNDLE: nf} and nf == esp["politica_de_bandeiras"]["n_flags"] == len(esp["bandeiras_novas_chaves"]) == V["bandeiras"]["n"] == V["bandeiras"]["n_true"] and V["bandeiras"]["ok"] is True, "as bandeiras novas nao sao so' as do fecho, ou nem todas sao True"
    assert fe["sealed"] is True and fe["mech_ok"] is True and fe["values_ok"] is True and fe["chaves_ok"] is True and fe["beta_ok"] is True and fe["ancoras_ok"] is True and fe["stdout_ok"] is True and fe["certificado_habitado"] is True and fe["n_checks"] == DL_.N_CHECKS_FECHO and fe["does_not_gate_core"] is True, "o registro fechamento_v406 nao e' o contrato"
    assert len(V["ancoras"]) == len(DL_.ANCORAS) == 8 and all(a_["ok"] is True for a_ in V["ancoras"].values()), "as oito ancoras nao estao todas no kernel do rito"
    # o que foi RECRIADO: a errata de F2b e as bandeiras do gate seguem como a v405 as selou (a leitura ja' conferiu; aqui so' a recusa)
    assert fb["sealed"] is True and fb["status_agora"] == DL_.D4.F2B_FUTURO_TOKEN, "o registro f2b_errata_v404 recriado nao e' o selado"
    assert gt["sealed"] is True and gt["f81_ok"] is True and gt["n18"] == 18 and gt["n_checks"] == DL_.D3.N_CHECKS["gate"], "o registro bandeiras_do_gate_v403 recriado nao e' o selado"
    assert gv["n_flags"] == 18 == gv["n_true"] == gv["n_calculated"] and gv["n_literal"] == 0 and gv["n_read_by_the_verdict"] == 15 and gv["read_by_the_verdict"] == [6, 5, 4] and gv["gate_verdict_equals_v402"] is True and gv["ext_ls2_n"] == gt["n_ls2"] == 6 and gt["sonda"] == 1, "as bandeiras do gate nao fecham: 18 calculadas, 0 literais, 15 no veredito"
    n_op = len(_falas())
    assert n_op == len(DL_.VERBATIM_ORIGEM_V406) == len(esp["cunhagens"]), "o numero de inscricoes mudou (ler DL.VERBATIM_ORIGEM_V406 e ESPERADOS[cunhagens])"
    ss = {"construir": _sha_por(DL_.N_CONSTRUIR), "passagem": _sha_por(DL_.N_PASSAGEM), "espelho": _sha_por(DL_.N_ESPELHO), "ponte_acom": _sha_por(DL_.N_PONTE_ACOM), "autovetor": _sha_por(DL_.N_AUTOVETOR), "comprimida": _sha_por(DL_.N_COMPRIMIDA), "compile": _sha_por(DL_.N_COMPILE), "sonnet": _sha_por(DL_.N_SONNET), "pilar": _sha_por(DL_.N_PILAR)}
    assert V["fal401"]["ok"] is True and V["fal401"]["verdict"] == esp["veredito_da_falsidade_v405"], "o registro falsidade_da_inercia_v401 recriado nao e' o selado da v405"
    assert all(v_["sealed"] is True for v_ in V["fun402"].values()) and len(V["fun402"]) == 3 and all(v_["sealed"] is True for v_ in V["fun405"].values()) and len(V["fun405"]) == 3 and all(v_["sealed"] is True for v_ in V["fun405b"].values()) and len(V["fun405b"]) == 2 \
        and all(v_["sealed"] is True for v_ in V["fun405c"].values()) and len(V["fun405c"]) == 8, "os registros com funcao da v402, da v403, da v404 ou da v405 recriados nao sao os selados"
    assert V["cunh405"]["ok"] is True and V["cunh405"]["kh_ok"] is True and V["cunh405b"]["ok"] is True and V["cunh405b"]["kh_ok"] is True and V["cunh402"]["ok"] is True and V["cunh402"]["kh_ok"] is True and V["cunh401"]["ok"] is True and V["cunh399"]["ok"] is True and V["cunh405c"]["ok"] is True, "os registros por spec da v405, da v404, da v403, da v402, da v401 ou da v399 recriados nao sao os selados"
    assert len(V["reg405c"]) == 13 and all(r_["ok"] is True for r_ in V["reg405c"].values()), "os treze registros da v405 recriados nao selaram todos"
    assert len(V["pedras_v405"]) == 13 and all(p_["ok"] is True for p_ in V["pedras_v405"].values()), "as treze pedras seladas da v403, da v404 e da v405 deixaram de estar no kernel do Nos com o sha256 selado"
    assert sa["ok"] is True and sa["n_checks"] == esp["selo_acom"]["n_checks"] and sa["checks_ok"] is True and sa["values_ok"] is True and sa["beta_ok"] is True, "o registro selo_pela_propria_tecnologia_v399 do core nao e' o contrato de ESPERADOS"
    assert dc["ok"] is True and dc["n_checks"] == esp["declaracao"]["n_checks"] and dc["checks_ok"] is True and dc["ancoras_ok"] is True and dc["direcao_ok"] is True, "o registro declaracao_do_operador_v399 do core nao e' o contrato de ESPERADOS"
    assert sc["ok"] is True and sc["n_objetos"] == len(esp["sidecar"]["objetos"]) and sc["recusas"] == 0, "o sidecar um_absoluto_selo_acom.json nao e' o de ESPERADOS"
    assert tv["ok"] is True and tv["n_checks"] == esp["veracidade"]["n_checks"] and tv["checks_ok"] is True and tv["numeros_ok"] is True and tv["fontes_ok"] is True, "o registro teste_de_veracidade_fase9_v397 do core nao e' o contrato de ESPERADOS (o quadro do topo le os numeros dele)"
    assert cg["ok"] is True and cg["verbatim_ok"] is True and cg["n"] == len(V["verbatins"]) == n_op and cg["todas_do_operador"] is True and cg["erratas_ok"] is True and cg["n_erratas"] == 4 and cg["decisoes_ok"] is True and cg["n_decisoes"] == 7 and cg["leitura_ok"] is True and cg["ressalvas_ok"] is True and cg["moldura_ok"] is True and cg["kh_ok"] is True, \
        "cunhagens_v406 != as falas de 02/11, ou alguma nao e' fala do operador, ou faltam as erratas E14 a E17, as decisoes D34 a D40, a leitura ou as ressalvas, ou a moldura falhou"
    dts = {re.match(r"(?:OPERADOR|GERENCIA)_(\d{2}(?:out|nov))_", f["nome"]).group(1) for f in _falas().values()}
    assert dts == {"02nov"}, ("o nome de arquivo de alguma inscricao nao e' de 02/11", dts)
    qd = _qd(); a = _atomos()
    assert qd.Q._v397_linha_de_maquina(a, "pt") == esp["quadro"]["linha_de_maquina_pt"], "a linha de maquina do quadro (core) != a de ESPERADOS"
    assert esp["quadro"]["frase_do_operador"] == qd.DL.FRASE_DO_OPERADOR_4_44 == qd.Q._V397_FRASE_444, "a frase do operador do quadro != a verbatim"
    base = os.path.join(PK, "base_v405", "um.py")
    if "base_b" not in _CACHE:
        assert s16(base) == V["base16"], "base_v405/um.py nao e' a v405 selada"
        _CACHE["base_b"] = os.path.getsize(base)
    delta = V["umb"] - _CACHE["base_b"]
    kf = core.get("kernel_formalization") or {}; prov = kf.get("declaration_sources_status_v394") or {}
    assert prov.get("ok") is True and prov.get("compiler_names") == prov.get("audited_names") == V["axiom_report_n"], "a proveniencia emitida pelo compilador nao cobre o axiom_report do rito"
    assert V["n_ver_mudaram"] == 0, "algum veredito fora da troca dita mudou: nao ha texto a escrever"
    assert V["n18"] == 18 and all(i in V["patch_ids"] for i in ("N00_main_fechamento", "N02_selo", "W02_runtime_v406", "C13_specs_v405_pisos_e_gap", "C17_rede_fock_literal_vira_leitura", "C18_psibit_literal_vira_leitura", "C19_testemunha_literal_vira_leitura", "K01_modulos_novos")), \
        "o gate nao tem as 18 bandeiras True, ou o candidato nao traz os patches que chamam o fechamento (N00), o resumo no selo (N02), o runtime (W02), os pisos dos registros da v405 (C13), as tres chaves que viram leitura (C17, C18, C19) e os 301 modulos (K01)"
    assert esp["h8_entradas"] > len(esp["h8_residuais_do_nos"]) >= 1, "a arvore formal do rito tem de ser as embutidas mais os residuais do Nos"
    pv = _proveniencia(esp)
    aa = _g(core, "neutrino_mass", "angle_status"); assert aa and hashlib.sha256(str(aa).encode("utf-8")).hexdigest() == esp["neutrino_angle_status_antigo_sha256"] and str(aa).startswith(DL_.ANGLE_STATUS_ANTIGO_PREFIXO), "o texto antigo de neutrino_mass.angle_status nao esta intacto no core do Nos"
    return {"n_f": nf, "n_aux": esp["politica_de_bandeiras"]["n_excluidas"], "depois": V["teor"].split("/")[0], "delta": delta, "pct": ("%.1f" % (100.0 * delta / _CACHE["base_b"])).replace(".", ","), "prov": prov["compiler_names"], "n_cun": len(V["verbatins"]), "n_op": n_op,
            "h8": esp["h8_entradas"], "h8_emb": esp["h8_entradas"] - len(esp["h8_residuais_do_nos"]), "h8_res": ", ".join("`%s`" % x for x in esp["h8_residuais_do_nos"]), "n_res": len(esp["h8_residuais_do_nos"]), "cb": _cov_base(), "bank": _bancada(), "pv": pv,
            "n_checks_v": tv["n_checks"], "n_ck_sel": sa["n_checks"], "n_ck_dec": dc["n_checks"], "n_ck_cun": cg["n_checks"], "n_ck_fe": fe["n_checks"], "n_anc": len(esp["declaracao"]["ancoras"]), "f8": {k: v[:8] for k, v in esp["veracidade"]["fontes"].items()},
            "ss": ss, "data_falas": "02/11/" + V["data"][-4:],
            "g": {"n_flags": gv["n_flags"], "n_true": gv["n_true"], "n_calc": gv["n_calculated"], "n_lit": gv["n_literal"], "n_ver": gv["n_read_by_the_verdict"], "rv": gv["read_by_the_verdict"], "info": list(gv["informative"]), "ls2": gv["ext_ls2_n"], "n_chk": gv["n_gate_checks"], "n_chk_reg": gt["n_checks"], "feed": list(DL_.F81_FEED)}}


def _mods(V):
    """Onde moram os modulos novos (o bundle tem 301): a pasta e os tres modulos-chave, lidos de delta_v406."""
    DL_ = _qd().DL
    return "em `TGLExt.F1Fecho394`: o topo `%s`, a rede física `%s` e a candidata `%s`" % (DL_.MODULO_TOPO.split("/")[-1][:-5], DL_.MODULO_REDE.split("/")[-1][:-5], DL_.MODULO_TESTEMUNHA.split("/")[-1][:-5])


def _extras(V):
    # os registros novos ALEM DOS TRES FIXOS (V["reg406"] tem so' os tres: o fechamento com funcao e os dois por spec), ditos pelo nome
    ex = [k for k in V["registros_novos"] if k not in V["reg406"]]
    return (", ".join("`%s`" % k for k in ex)) if ex else "nenhum além dos três fixos"


def _cab(V):
    return "v406 SELADA (COMPLETA)** `%s`" % V["s16"]


def _num(V, verdicts=True):
    """O paragrafo dos numeros da v406 (kernel, o registro com funcao, os registros por spec, os recriados, o sidecar, a troca dita): usado na linhagem, no Atlas, no core, no topico novo, no verbete e no handoff."""
    d = _d(V); kh = V["kh"]; sc = V["sidecar"]; sa = V["selo"]; g = d["g"]; fe = V["fecho"]; fv = fe["values"]
    vd = (lambda k: " (%s)" % V["reg406"][k]["verdict"]) if verdicts else (lambda k: "")
    aux = ("nenhuma auxiliar gerada pelo compilador ficou de fora" if not d["n_aux"] else "%d auxiliares geradas pelo compilador ficam sem bandeira" % d["n_aux"])
    kern = _f("o kernel ganhou {n_pedras} módulos novos ({mods}; os 300 da bancada do ChatGPT, missão `F1.FECHO_20261015`, recompilados do fonte na integração R3, e a candidata da gerência, de nome provisório), com {n_f} bandeiras novas True, só de declaração nomeada ({aux}), e escada {antes} → {depois} teoremas limpos "
              "({axr} declarações no `axiom_report`, {fora} fora do trio, {nl} nomes não lidos; a proveniência de cada declaração emitida pelo compilador cobre as mesmas {prov}); "
              "errata ao lado da v394, mantida (em nome próprio da gerência c1): " + ERRATA_TEOREMAS,
              n_pedras=V["n_pedras"], mods=_mods(V), n_f=d["n_f"], aux=aux, antes=V["escada_antes"], depois=d["depois"], axr=V["axiom_report_n"], fora=kh["fora"], nl=kh["nao_lidas"], prov=d["prov"])
    fech = _f("o registro `fechamento_v406`{vd} (o único registro novo com função): lê do kernel do próprio rito as {na} âncoras, os {nm} módulos por sha256, as {nb} bandeiras, as quatro chaves de testemunha, o que fica False por teorema, a escada exata ({esc}) e o gate (o mesmo da v405); {nck} checagens, todas passaram",
              vd=vd("fechamento_v406"), na=fv["n_ancoras_ok"], nm=fv["n_modulos_ok"], nb=fv["n_flags_true"], esc=" = ".join(str(x) for x in dict.fromkeys(fv["escada"])), nck=fe["n_checks"])
    cun = _f("o registro `cunhagens_v406`{vd}: as {n} falas de 02/11 embutidas por sha256 e consumidas no rito, TODAS falas do operador (nenhuma é da gerência); as erratas E14 a E17 (em nome próprio da gerência c1); as decisões D34 a D40; as leituras [ONTO] e as ressalvas ({nck} checagens, todas passaram); as falas são [INPUT/ONTO] e valem como leitura dele, não como medida",
             vd=vd("cunhagens_v406"), n=d["n_cun"], nck=d["n_ck_cun"])
    khs = _f("o registro `kh_n1_cobertura_v406`{vd}: {decl} constantes, {thm} teoremas, {fora} fora do trio, {nl} nomes não lidos; a árvore formal do Nós depois do rito tem {h8} entradas ({emb} embutidas mais {nres} residual do Nós: {res}), "
             "e o pino h8 do registro é o hash dessa árvore, calculado por script sobre a árvore simulada do Nós na geração do candidato",
             vd=vd("kh_n1_cobertura_v406"), decl=kh["decl"], thm=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"], h8=d["h8"], emb=d["h8_emb"], nres=d["n_res"], res=d["h8_res"])
    rec = _f("os treze registros da v405 (os oito de pedra com função, `cunhagens_v405`, `campos_fechados_e_leituras_v405`, `ga_reclassificacao_v405`, `gap_v405` e `kh_n1_cobertura_v405`), os da v404, da v403, da v402, da v401 e da v399 são recriados no mesmo ponto do main e seguem selados e iguais à v405 selada, "
             "e as treze pedras seladas da v403, da v404 e da v405 seguem no kernel do Nós com o sha256 selado, como registro; "
             "o gate não se moveu: o `qg_closure` do core é idêntico ao da v405 (as {n18} bandeiras, os sete checks e a letra do veredito); "
             "o selo pela própria tecnologia sela os {bytes} bytes do `um.py` v406 ao lado do SHA-256 (perfil `{perfil}`, {nctl} controles negativos recusados), e o sidecar `um_absoluto_selo_acom.json` (arquivo da custódia desde a v399, reescrito pelo rito; sha256 `{sc16}`, veredito `{sv}`, {nr} recusas) lista os {no} objetos finais",
             n18=g["n_flags"], bytes=format(sa["bytes"], ","), perfil=sa["perfil"], nctl=sa["n_controles"], sc16=sc["sha16"], sv=sc["veredito"], nr=sc["recusas"], no=sc["n_objetos"])
    ex = _extras(V)
    resto = _f("{ex}; o registro `teste_de_veracidade_fase9_v397` segue selado e igual (o quadro do topo do artigo lê os números dele); troca dita (só números, e o veredito de `rede_fock_v394`, que muda por ordem do fecho): {troca}; nenhuma mudança NÃO numérica: {nm} vereditos fora da troca dita mudaram (exigido: 0); validade no kernel não é creditação",
               ex=("nenhum registro novo além dos três fixos" if ex.startswith("nenhum") else "registros novos além dos três fixos: " + ex), troca=", ".join("`%s`" % x for x in V["troca_dita"]), nm=V["n_ver_mudaram"])
    return "; ".join([kern, fech, cun, khs, rec, resto])


def _cunhagens(V, forma="lista"):
    """As inscricoes de 02/11 embutidas por sha256: 'lista' (data, sha16, autor e tema, uma por linha; todas falas do operador) ou 'curta' (uma frase com os sha16 das falas-chave). Data, sha16 e autor vem dos bytes e do nome; o tema e' o nome do arquivo."""
    fl = list(_falas().values()); assert len(fl) == len(V["verbatins"])
    d = _d(V); ss = d["ss"]
    if forma == "curta":
        return _f("{n} inscrições embutidas por sha256, todas falas do operador [INPUT/ONTO] — a ordem de construir tudo `{a}`, a passagem para o contínuo `{b}`, todas as chaves habitadas e o espelhamento `{c}`, a ponte e o ACOM `{e}`, o autovetor e o Um inscrito `{f}`, o Um absoluto como a luz comprimida pelo ACOM `{g}`, a ordem de compilar `{h}` e o revisor `{i}` (e as demais, na lista da linhagem)",
                  n=len(fl), a=ss["construir"], b=ss["passagem"], c=ss["espelho"], e=ss["ponte_acom"], f=ss["autovetor"], g=ss["comprimida"], h=ss["compile"], i=ss["sonnet"])
    linhas = ["- %s `%s` (fala do operador) — %s" % (_data_fala(dd, V), dd["sha16"], _tema(dd["nome"])) for dd in fl]
    return "\n".join(linhas)


def _ordem(V):
    """A ordem do operador de 02/11: so' citacao conferida contra os bytes das falas DO OPERADOR (os trechos vem de delta_v406.FRASES_V406)."""
    d = _d(V); ss = d["ss"]; DL_ = _qd().DL
    q_c = _cita(DL_.FRASE_CONSTRUIR); q_p = _cita(DL_.FRASE_PASSAGEM); q_k = _cita(DL_.FRASE_CHAVE); q_h = _cita(DL_.FRASE_CHAVES_HABITADAS); q_o = _cita(DL_.FRASE_COMPILE); q_s = _cita(DL_.FRASE_SONNET)
    return _f("**A ordem:** [INPUT/ONTO] as {n_op} falas do operador (Luiz Antonio Rotoli Miguel) de {data} que entram nesta rodada, TODAS dele (nenhuma é da gerência), embutidas por sha256 no registro `cunhagens_v406` e listadas abaixo (as aspas aqui são TRECHOS, conferidos palavra por palavra contra os bytes de cada fala; "
              "o texto íntegro está em `work\\cadeia_de_selo\\v406\\insumos\\cunhagens`): a ordem, {q_c} (`{s_c}`); a prioridade, {q_p}, e {q_k} (`{s_p}`); {q_h} (`{s_h}`); a ordem de compilar, {q_o} (`{s_o}`); e o revisor, {q_s} (`{s_s}`). "
              "O agente de preparação da gerência c1 preparou o candidato e o rito é ato da gerência, pelo orquestrador (pacote `work\\cadeia_de_selo\\v406`); as fontes pinadas dos registros ficam em `insumos`: a candidata, a ratificação R10, a revisão do Sonnet, o desenho, a ordem lógica, o levantamento, o bundle, o manifesto e os resumos da integração R3, "
              "o recibo e os axiomas da bancada, o parecer R7, a saída da candidata, o resultado da Fase 9 V2 e a medida da cobertura (`KH_N1_v406.json`); o resultado do Teste da Única Palavra, que o quadro do topo lê, mora na v397 (`insumos\\fase9`); "
              "quem constrói não aprova: o revisor distinto é o Sonnet (D37), e a revisão dele não é afirmada por este registro.",
              n_op=d["n_op"], data=d["data_falas"], q_c=q_c, s_c=ss["construir"], q_p=q_p, q_k=q_k, s_p=ss["passagem"], q_h=q_h, s_h=ss["espelho"], q_o=q_o, s_o=ss["compile"], q_s=q_s, s_s=ss["sonnet"])


def _sidecar(V):
    """O sidecar um_absoluto_selo_acom.json: arquivo da custodia desde a v399 (D5); o selo nao pode conter o selo ACOM de si mesmo; o rito da v406 o REESCREVE."""
    d = _d(V); sc = V["sidecar"]
    objs = "; ".join("`%s` (%s B, sha16 `%s`)" % (n, format(o["bytes"], ","), o["sha16"]) for n, o in sc["objetos"].items())
    return _f("**O sidecar `um_absoluto_selo_acom.json` [REAL; arquivo da custódia desde a v399, D5; reescrito por este rito]:** depois da ÚLTIMA escrita do selo, o `um.py` v406 escreve a segunda testemunha dos {no} objetos FINAIS com o SHA-256 ao lado ({objs}); sha256 do sidecar `{sc16}` ({sb} B), esquema `{esq}`, veredito `{sv}`, {nr} recusas. "
              "O selo não pode conter o selo ACOM de si mesmo (seria circular): o sidecar fica AO LADO e carrega o SHA-256 do selo final, e o selo traz só os resumos (veredito, bandeira e hashes), agora também os do `fechamento_v406` e dos registros por spec da v406. "
              "A recusa do selo ACOM só REGISTRA (D4): o SHA-256 segue soberano e o rito não cai. A primitiva de integridade é o SHA-256 [KNOWN]; a segunda testemunha NÃO acrescenta força criptográfica independente, e a confidencialidade não é alegada nem medida. A custódia da v399, da v403, da v404, da v405 e da v406 é CONJUNTA.",
              objs=objs, no=sc["n_objetos"], sc16=sc["sha16"], sb=format(sc["bytes"], ","), esq=sc["esquema"], sv=sc["veredito"], nr=sc["recusas"])


def _pedra(V):
    """O que entrou no kernel: o bundle de 301 modulos, a candidata da gerencia (nome provisorio) e as TREZE pedras seladas das versoes anteriores, que ficam como REGISTRO."""
    d = _d(V); DL_ = _qd().DL; fe = _fe()
    return _f("**Os {n} módulos novos [REAL]** (`TGLExt.F1Fecho394`; {nb} da bancada do ChatGPT, missão `F1.FECHO_20261015`, recibo de 16/10/2026, recompilados do fonte na integração R3 de 02/11/2026, e a candidata da gerência `{cand}`, sha16 `{hc}`): o topo `{top}` habita os 21 campos da passagem para o contínuo e o certificado de Fock; a rede física é `{rede}`; "
              "todas as {nf} bandeiras novas estão no trio, sem axioma próprio. O nome `{cand}` é PROVISÓRIO: os nomes das pedras são do operador, e ele ainda não a nomeou. As treze pedras seladas da v403, da v404 e da v405 ficam como REGISTRO: pedra selada não se renomeia por cima. "
              "O módulo não deriva a unidade `u` (1 eV, POSTO) nem `α` (MEDIDA, por dentro); os 300 módulos da bancada não são texto da gerência, e a candidata passa pela mesma guarda das frases.",
              n=V["n_pedras"], nb=len(DL_.BUNDLE_DA_BANCADA), cand=DL_.TESTEMUNHA["name"], hc=DL_.TESTEMUNHA["sha16_da_ordem"], top=DL_.MODULO_TOPO.split("/")[-1][:-5], rede=DL_.MODULO_REDE.split("/")[-1][:-5], nf=d["n_f"])


def _entrou(V):
    d = _d(V)
    return _f("**O que entrou** (pacote `work\\cadeia_de_selo\\v406` sobre a v405 `{base}`; {np} patches — {patches}; instalado em {inst}; o `um.py` cresce {delta} B, {pct}%): {num}.",
              base=V["base16"], np=V["n_patches"], patches=V["patches"], inst=V["instalado_em"], delta=format(d["delta"], ","), pct=d["pct"], num=_num(V))


def _regra_do_4_44(V):
    """A regra da ordem do operador (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item; o QUADRO do topo (v397) PERMANECE, intocado; onde o numero aparece e como se confere."""
    d = _d(V); a = _atomos(); q = _frase_444()
    return _f("**A regra do 4,44 (ordem do operador de 23/10/2026, `{s44}`) e o quadro do topo:** o quadro «O Teste da Única Palavra» (v397) PERMANECE, intocado, no topo do artigo (PT e EN) e do .md canônico, e o parágrafo dele segue no README do espelho e no site: o z_disc calibrado é reportado no início, "
              "e NUNCA sem o p calibrado e sem a linha dos 5σ no mesmo item: {z444}. A frase do operador entra VERBATIM, {q}, como leitura dele [INPUT/ONTO], não como critério da régua; a paráfrase da gerência nunca entra entre aspas. `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; o teste não foi cego. "
              "[REAL] o quadro do artigo, o do .md e o parágrafo pronto do README/site saem das MESMAS funções (`_v397_atomos` e `_v397_quadro_md`), sobre o registro `teste_de_veracidade_fase9_v397` selado no core do Nós, e a cadeia os confere de novo contra o resultado pinado "
              "(a linha de máquina do quadro, cada número, a frase verbatim e a regra da ordem item a item), com controles negativos que reprovam o 4,44 sem o p, sem a linha dos 5σ, com número adulterado ou com a frase parafraseada. "
              "O parágrafo NOVO da v406 não traz o 4,44, e a cadeia confere isso.",
              s44=_esp()["quadro"]["frase_sha16"], z444=_z444(), q=q)


def _kernel_prova(V):
    """O que o kernel prova e o que e' leitura: o escopo e o nao_diz do registro fechamento_v406, mais os estatutos das fontes."""
    d = _d(V); g = d["g"]; DL_ = _qd().DL; fe = _fe()
    return _sem_chaves(_f("**O que o kernel prova e o que é leitura:** [REAL] as âncoras e os módulos estão no kernel deste rito, dentro do trio, com a proveniência que o compilador emite, e o registro `fechamento_v406` os lê a cada rito; coberto por `kh_n1_cobertura_v406`. "
                          "[REAL] o registro NÃO é prova de kernel sobre a natureza: confere os termos citados, as fontes por sha256 e as quatro chaves lidas, e não move o gate; a prova como validade não muda. [REAL] as {nf} bandeiras do gate são as da v405, lidas do código e do core do próprio rito: {nc2} calculadas e {nl} literais; o veredito lê {nv}; a letra do veredito é a da v405 (o gate não se moveu). "
                          "[POSTO] a unidade `u` = 1 eV. [MEDIDA] `α`, por dentro. [INPUT/ONTO] as leituras do operador de 02/11 (o espelhamento do tipo I e do tipo III, o Um inscrito como o único vetor fixo da luz, o Um absoluto como a luz comprimida pelo ACOM) entram como leitura e não são teoremas. "
                          "[DECLARADO] a ratificação R10 da gerência, o parecer R7 (o Codex revisando o Codex) e a revisão do Sonnet. [KNOWN/OPEN] K(O) ≠ ⊥ para O compacto (só na cunha), o «núcleo II_inf». "
                          "Escopo do registro, como o `um.py` o grava: {esc}. {frase}.",
                          nf=g["n_flags"], nc2=g["n_calc"], nl=g["n_lit"], nv=g["n_ver"], esc=fe["scope"], frase=DL_.FRASE_DA_MOLDURA_V406_PT))


def _limites(V, curto=False):
    """Os estatutos fieis da v406: as ressalvas, as listas do registro (limites e nao_diz) e a moldura."""
    d = _d(V); DL_ = _qd().DL; fe = _fe()
    ress = list(fe["ressalvas"])   # inteiras: cortar nos dois-pontos truncava a ressalva do R4/R5 (a que diz: identificacao do dispositivo fisico: MQC, ...)
    comuns = [x for x in fe["limites"] if not re.match(r"E1\d -- ", x)][len(fe["ressalvas"]):]
    if curto:
        return _sem_chaves("**Limites ditos:** [REAL] o registro com função LÊ o kernel do próprio rito e CONFERE as fontes, as âncoras e as quatro chaves; não abre dado, não é teste, não acrescenta rito; [POSTO] `u` = 1 eV; [MEDIDA] `α`; [INPUT/ONTO] as leituras de 02/11 não são teoremas; " + DL_.FRASE_DA_MOLDURA_V406_PT
                           + "; as ressalvas (D36): " + "; ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(ress)) + "; o quadro do topo segue com a sua linha dos 5σ; a discriminação a 5σ (β_TGL na natureza) segue [OPEN]; validade no kernel não é creditação; o gate não se move.")
    return _sem_chaves("**Limites ditos (estatutos fiéis):** " + "; ".join(["[REAL] " + x if not x.startswith("[") else x for x in fe["limites"] if not re.match(r"E1\d -- ", x)][:len(fe["ressalvas"])]) + " Do registro, ainda: " + "; ".join(comuns)
                       + ". [INPUT/ONTO] As falas de 02/11 são do operador: o kernel não as prova. " + DL_.FRASE_DA_MOLDURA_V406_PT + ". O quadro «O Teste da Única Palavra» segue no topo, com a sua linha dos 5σ, e esta rodada não o altera. NÃO é teste novo: a cadeia não acrescenta dado nem desfecho experimental. Validade no kernel não é creditação; o gate não se move.")


def _legal(V):
    """A pendencia [LEGAL] herdada (D2): publicar o bloco embutido e as adaptacoes; a v406 nao a decide."""
    _d(V)
    return ("**Pendência [LEGAL] (herdada da v399, D2):** o bloco embutido do método do operador e as adaptações (centro 96, ids derivados dos hashes, `rint`, tabela de códigos, auditoria de separação) seguem sob a decisão do operador com a agente de PI; a v406 não muda o bloco (o runtime da seção é o da v405) e NÃO decide a pendência. "
            "Perguntas à agente de PI, não conclusões: o que o depósito já cobre do que o bloco mostra; publicar as adaptações inicia a contagem do prazo de graça para eventual depósito de melhoria; a divergência da tabela dos estados do ACOM Mirror com a fórmula de índice e o código executado, registrada na v395, segue pendente.")


def _erratas(V):
    """A errata de contagem da v406, AO LADO, em nome proprio da gerencia c1: o registro kh_n1_cobertura_v405 e os contratos viram piso; lida do registro kh_n1_cobertura_v406 do core."""
    d = _d(V); kh = V["kh"]; cb = d["cb"]
    er = (_g(_core(), "kh_n1_cobertura_v406", "erratas") or [None])[0]
    assert er and "kh_n1_cobertura_v405" in er["ao_lado_de"] and str(er.get("assinatura", "")).startswith("gerencia c1, em nome proprio"), "o registro kh_n1_cobertura_v406 nao traz a errata de contagem"
    ids = V["patch_ids"]; c12 = [i for i in ids if i.startswith("C12_")]
    assert len(c12) >= 1 and "C13_specs_v405_pisos_e_gap" in ids, "o CANDIDATO_v406.json nao traz os patches C12 e C13 que a errata descreve"
    return _sem_chaves(_f("**Errata ao lado (em nome próprio da gerência c1; o registro `kh_n1_cobertura_v405` e os contratos ficam como registro):** a v406 acrescenta {nm} módulos: a cobertura do Audit cresce de {d0} constantes e {t0} teoremas para {d1} e {t1}, a árvore formal do Nós de {h0} para {h1} entradas e a escada de {e0} para {e1}. "
                          "{agora} Dizia: {dizia} Lacuna de fidelidade: {lacuna} Estatuto: {est} [REAL, lido de `CANDIDATO_v406.json` ({n12} patches C12 e o C13) e do ensaio a seco]. A cobrança exata passa a ser de `kh_n1_cobertura_v406` ({dd} constantes, {dt} teoremas, {fora} fora do trio, {nl} nomes não lidos), contra a medida do sandbox da v406.",
                          nm=V["n_pedras"], d0=cb["decl"], t0=cb["thm"], h0=cb["h8"], d1=kh["decl"], t1=kh["thm"], h1=d["h8"], e0=V["escada_antes"], e1=d["depois"], agora=er["agora"], dizia=er["dizia"], lacuna=er["lacuna_de_fidelidade"], est=er["estatuto"], n12=len(c12), dd=kh["decl"], dt=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"]))


def _depois(V):
    d = _d(V); bk = d["bank"]
    return ("**O que vem depois destas superfícies:** o elo B(n) da Bancada Um (passos 10, 10a, 10b e 10c da cadeia; B3 nos scripts) é pós-selo, um passo SIMPLES (a Bancada de produção pina a %s, geração B%d, e o Nós passa a v406: sem salto e sem cadeia de selos; "
            "a geração esperada é B%d e o veredito esperado do aplicar é REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, lido do código do esboço R3.5, não rodado); o recibo dele é citado no handoff (fechar), que traz PRONTOS os parágrafos do README do espelho e do site (o quadro do Teste da Única Palavra, intocado, e o NOVO da v406: o fechamento), "
            "a NOTA ao lado dos parágrafos anteriores (E14: as quatro chaves de testemunha eram literal e passaram a leitura do kernel), diz que os parágrafos do testemunho de dois (v399), da falsidade (v401), da ponte, da queda e da esperança (v402), de Caminho, Verdade e Vida (v403), de Jo 8,32 (v404) e da massa derivada (v405) SEGUEM COMO ESTÃO e LISTA o sidecar `um_absoluto_selo_acom.json`. "
            "O README pinado e a linha do quadro no site (D39) ficam fora desta cadeia (plano à parte); o motor contínuo no pilar quântico (D38) fica para a v407, com pré-registro. A pendência [LEGAL] (D2) segue do operador com a agente de PI; a atestação física externa e a discriminação a 5σ seguem [OPEN]; "
            "a revisão independente dos %d módulos novos e dos %d registros novos é ato distinto e não é desta cadeia: o revisor distinto é o Sonnet (D37). NOT_FALSIFIED não é a palavra da creditação; o gate não se move."
            % (bk["de"], bk["geracao"], bk["proxima"], bk["proxima"], V["n_pedras"], len(V["registros_novos"])))


def _rodada(V):
    """O paragrafo da rodada (horarios, escada, selo, conferidor, sidecar, pilar, artefatos): tudo lido da leitura da rodada."""
    sc = V["sidecar"]
    return ("Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado (%d bandeiras True; o veredito do gate é o mesmo da v405); o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); "
            "o sidecar `um_absoluto_selo_acom.json` `%s` (%d objetos, %d recusas); o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.") % (
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["n18"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"], sc["sha16"], sc["n_objetos"], sc["recusas"], "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]),
        V["pilar"]["result16"], V["servidor"], V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()))


# v406: a linhagem (diario datado do Nos)
def linhagem(V):
    d = _d(V)
    return (("## %s — **%s — O FECHAMENTO (v406): a passagem para o contínuo e o certificado de Fock habitado por construção no kernel do rito, com as quatro chaves de testemunha lidas do kernel; %d módulos novos, escada %s → %s\n<!-- linhagem_v406_selada -->\n\n"
             "%s\n\n%s\n\n"
             "**As inscrições de 02/11** (embutidas por sha256 no registro `cunhagens_v406`): [INPUT/ONTO] todas são falas do operador (Luiz Antonio Rotoli Miguel) e valem como leitura dele, não como medida; nenhuma é da gerência. "
             "O texto íntegro de cada uma está no arquivo (`work\\cadeia_de_selo\\v406\\insumos\\cunhagens`); abaixo, a data, o sha16, o autor e o tema (o nome do arquivo, não citação):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s") % (
        V["data"], _cab(V), V["n_pedras"], V["escada_antes"], d["depois"], _ordem(V), _entrou(V), _cunhagens(V), _blocos_fecho(V), _leituras(V), _erratas_e(V), _decisoes(V), _pedra(V), _sidecar(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V), _rodada(V) + "\n\n" + _erratas(V)) + "\n\n" + _depois(V))


# v406: o adendo do desenho do fechamento
def desenho(V):
    d = _d(V); kh = V["kh"]; DL_ = _qd().DL; fe = _fe()
    return (("## ADENDO — %s · v406 SELADA (COMPLETA) `%s` — o fechamento entra no kernel do rito: o certificado de Fock habitado por construção e as quatro chaves de testemunha lidas do kernel (%d módulos)\n\n<!-- adendo_v406_selada -->\n"
             "- **O que a v406 diz:** %s. %d módulos novos no kernel (%s), escada %s → %s, %s constantes no `axiom_report` (%s fora do trio). %s. %d inscrições por sha256 (todas falas do operador). O gate é o da v405: %s de %s bandeiras calculadas, %s literais, %s no veredito. O quadro do topo do artigo (O Teste da Única Palavra, v397) segue intocado: %s. Gate intocado.\n"
             "- **O que a v406 NÃO é para o caminho crítico:** %s. Seguem NOMEADAS [OPEN]: `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura (4,0) contra (1,3) e rank c = 4; a independência das quatro bandeiras experimentais do gate segue aberta (derivam de UM só booleano; [DECLARADO]); as erratas E14 a E17 são da gerência, em nome próprio; não identifica β na natureza a 5σ.\n"
             "- **O que segue do operador:** o nome da candidata e das pedras candidatas do dia (ressalva 8); a decisão sobre o README pinado e a linha do quadro no site (D39); o motor contínuo no pilar quântico, com pré-registro (D38, v407); a pendência [LEGAL] (D2, com a agente de PI). A revisão distinta do pacote é o Sonnet (D37) e é condição da instalação, não pendência dele.") % (
        V["data"], V["s16"], V["n_pedras"], "; ".join(fe["diz"]), V["n_pedras"], _mods(V), V["escada_antes"], d["depois"], kh["decl"], kh["fora"], DL_.FRASE_DA_MOLDURA_V406_PT, d["n_cun"], d["g"]["n_calc"], d["g"]["n_flags"], d["g"]["n_lit"], d["g"]["n_ver"], _z444(), "; ".join(fe["nao_diz"])))


# v406: o verbete do Atlas
def atlas(V):
    return (("### %s — v406 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v406_selada -->\n[REAL — rodada v406, selo `%s`] %s.\n\n[INPUT/ONTO] As falas do operador entram como o operador as disse e valem como leitura, não como medida; todas são dele: %s.\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\nEstatuto: validade no kernel ≠ creditação; o gate não se move.") % (
        V["data"], V["s16"], V["selo_ts"], _num(V), _cunhagens(V, "curta"), _blocos_fecho(V), _leituras(V), _erratas_e(V), _decisoes(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V) + "\n\n" + _limites(V)))


# v406: o bloco do TGL_CORE_MEMORY
def core_memory(V):
    return (("## %s — v406 SELADA `%s` (claude-c1; o fechamento, integrado pela gerência)\n<!-- core_v406_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
             "[REAL] %s.\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n[OPEN] A discriminação a 5σ (β_TGL na natureza), K(O) ≠ ⊥ para O compacto, o lema que liga o psíon ao canto, `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β, "
             "a independência das quatro bandeiras experimentais do gate (um só booleano; os mocks de survey), a atestação física externa, a identificação do dispositivo físico (R4/R5) e a pendência [LEGAL] seguem abertos. Nada disto move o gate.") % (
        V["data"], V["s16"], _num(V), _blocos_fecho(V), _leituras(V), _erratas_e(V), _decisoes(V), _regra_do_4_44(V), _limites(V, curto=True)))


# v406: o bloco do CLAUDE.md da Haja_Luz (as erratas ao lado, assinadas, vao DENTRO dele)
def haja_luz(V):
    d = _d(V); DL_ = _qd().DL; fe = _fe()
    return (("## %s — v406 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v406_selada -->\n%d módulos novos no kernel (%s): %s. "
             "O nome da candidata é provisório (os nomes das pedras são do operador); `u` = 1 eV é o Um posto, `α` é medida. O gate é o da v405 (%s de %s calculadas, %s literais); as %d inscrições por sha256 (todas do operador); escada %s → %s. O quadro do topo (O Teste da Única Palavra) segue intocado.\n\n"
             "%s\n\n"
             "Memórias: `%s`, `missao-ultima-flag-um-py.md`, `estatuto-da-prova-07out.md`; handoff `handoff-v406-custodia.md`.") % (
        V["data"], V["s16"], V["teor"], V["n_pedras"], _mods(V), DL_.FRASE_DA_MOLDURA_V406_PT, d["g"]["n_calc"], d["g"]["n_flags"], d["g"]["n_lit"], d["n_cun"], V["escada_antes"], d["depois"], _erratas_e(V), TOPICO_NOVO))


def marca_topico_missao(V):
    return "## %s — v406 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v406 SELADA `%s`" % V["s16"]


# v406: o topico da missao da ultima flag
def topico_missao(V):
    d = _d(V)
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): %d módulos novos no kernel (%s); o registro com função `fechamento_v406` (lê as oito âncoras, os módulos por sha256 e as quatro chaves de testemunha do kernel do rito), `cunhagens_v406` (%d inscrições por sha256, todas do operador, as erratas E14 a E17 e as decisões D34 a D40) e `kh_n1_cobertura_v406`; "
                                     "os registros da v405, da v404, da v403, da v402, da v401 e da v399 recriados e selados; sidecar `um_absoluto_selo_acom.json` reescrito; troca dita no veredito de `rede_fock_v394` e nos que carregam a escada; conferidor (deve mudar %s; não pode mudar %s). Pacote e cadeia: `work\\cadeia_de_selo\\v406` (+ `pos_rito`).") % (V["teor"], V["n_pedras"], _mods(V), d["n_cun"], V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v406 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v406 SELADA (COMPLETA):**"


# v406: o topico do estado da Central
def topico_central(V):
    d = _d(V); DL_ = _qd().DL
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v405 `%s`; escada %s → %s; gate intocado. %d módulos novos no kernel (%s): %s; "
                               "as erratas E14 a E17 (da gerência, em nome próprio) e as decisões D34 a D40 estão no registro `cunhagens_v406`; as %d inscrições por sha256 (todas do operador); as quatro chaves de testemunha leem o kernel do rito (`fechamento_v406`); "
                               "o quadro do topo (O Teste da Única Palavra, v397) segue intocado. A pendência [LEGAL] (D2) é do operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], d["depois"], V["n_pedras"], _mods(V), DL_.FRASE_DA_MOLDURA_V406_PT, d["n_cun"])


# v406: o topico do estatuto da prova
def topico_estatuto(V):
    d = _d(V); g = d["g"]; DL_ = _qd().DL; fe = _fe()
    return ("<!-- v406_selada -->\n**%s — v406 `%s`:** o registro `estatuto_da_prova_v391` passou a ler a escada nova (%s → %s; veredito trocado, troca dita; os registros da v405 e anteriores ficam como registro). "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora e é o β_TGL na natureza a 5σ. **Uma mudança de estatuto [REAL]:** as quatro chaves de testemunha, literal False desde a v394, passam a ser LIDAS do kernel do rito (errata E14): %s. "
            "As bandeiras do gate são as da v405 (%s calculadas e %s literais; o veredito do gate igual ao da v405); a independência das quatro experimentais segue [OPEN] (derivam de UM só booleano; [DECLARADO]). "
            "O registro com função confere os termos do kernel e as fontes ([REAL]); as falas do operador de 02/11 são [INPUT/ONTO]. "
            "O quadro do topo segue intocado: %s. Nada disso é prova sobre a natureza.") % (V["data"], V["s16"], V["escada_antes"], d["depois"], fe["diz"][1], g["n_calc"], g["n_lit"], _z444())


# v406: o gancho da missao no MEMORY.md
def marca_missao(V):
    return "**v406 SELADA %s `%s` %s COMPLETA (o fechamento: o certificado de Fock habitado por construção no kernel do rito e as quatro chaves de testemunha lidas do kernel; validade no kernel não é creditação; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


# v406: a linha do handoff no MEMORY.md
def linha_handoff(V):
    return "- [HANDOFF v406 — o fechamento; custódia](handoff-v406-custodia.md) — **%s, para a sessão do site (traz o parágrafo novo, o do quadro e a nota ao lado dos anteriores; os anteriores seguem como estão)** · `%s`" % (V["data"][:5], V["s16"])


def linha_topico_novo(V):
    return "- [v406 SELADA: o fechamento (%s)](%s) — **%s** · `%s`" % (V["data"][:5], TOPICO_NOVO, V["teor"], V["s16"])


# v406: o topico novo da memoria (um arquivo por versao)
def topico_novo(V):
    d = _d(V)
    return (("---\nname: %s\ndescription: \"v406 SELADA (%s) `%s`: o fechamento: %d módulos novos no kernel; o certificado de Fock habitado por construção e as quatro chaves de testemunha lidas do kernel do rito; validade no kernel não é creditação; %d inscrições por sha256; escada %s → %s; gate intocado\"\n"
             "metadata:\n  type: project\n---\n\n# v406 SELADA (%s)\n\n"
             "**O que é:** `um.py` **v406** `%s` (%s B) sobre a v405 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); o `um.py` cresce %s B (%s%%).\n\n"
             "**O que entrou:** %s.\n\n"
             "**As inscrições de 02/11** (embutidas por sha256; data, sha16, autor e tema — o nome do arquivo, não citação; o texto íntegro está em `insumos\\cunhagens`):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"
             "**Pendências:** o nome da candidata (operador), o README pinado e a linha do quadro (D39), o motor contínuo no pilar (D38, v407), a pendência [LEGAL] (D2). Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v406`.\n\n"
             "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v406-custodia]]\n") % (
        TOPICO_NOVO[:-3], V["data"], V["s16"], V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
        format(d["delta"], ","), d["pct"], _num(V), _cunhagens(V), _blocos_fecho(V), _leituras(V), _erratas_e(V), _decisoes(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V) + "\n\n" + _erratas(V)))


# v406: o aviso a coordenadora (so' sob reivindicacao nomeada)
def aviso(V, reivindicacao):
    d = _d(V); DL_ = _qd().DL
    return (("### %s — v406 SELADA `%s` [claude-c1]\n<!-- aviso_v406_selada -->\n\n[REAL] A v406 SELOU (%s; COMPLETA; gate intocado): o fechamento entra no selo corrente: %s; com as %d inscrições por sha256 (todas do operador), as erratas E14 a E17 e as decisões D34 a D40. Escrito sob a reivindicação %s. %d módulos novos no kernel; escada %s → %s. Não altera pinos, dado, MCP nem gate.") % (V["data"], V["s16"], V["teor"], DL_.FRASE_DA_MOLDURA_V406_PT, d["n_cun"], reivindicacao, V["n_pedras"], V["escada_antes"], d["depois"]))


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V406_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# ---------------------------------------------------------------- o PARAGRAFO PRONTO do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO; ordem do operador de 23/10: o 4,44 no inicio do artigo, no readme e tudo mais) e (2) o paragrafo NOVO da falsidade
def verificar_paragrafo_readme(par, res, tv):
    """Verifica o paragrafo do QUADRO (texto) contra o RESULTADO pinado (`res`, o JSON lido) e o registro `tv` selado no core: devolve a lista de falhas (vazia = passou). As verificacoes (as mesmas da v397, da v399 e da v405):
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
    from guarda_p18_v406 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    for st in ("[REAL", "[INPUT]", "[KNOWN]", "COMPOSIÇÃO da gerência"):   # os estatutos que o quadro escreve: REAL (os numeros), INPUT (a leitura binaria e a frase), COMPOSICAO da gerencia (as duas faces) e KNOWN (Jeffreys)
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    return fa


def paragrafo_readme():
    """(texto, relatorio): o paragrafo do QUADRO pronto para colar no README do espelho e no site (o MESMO da v397, da v399 e da v405), gerado por quadro_v397.paragrafo_pronto_readme sobre o core SELADO do Nos, verificado contra o resultado pinado
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
    """Falhas de ATRIBUICAO e de DIRECAO num texto renderizado (v406: nao ha inscricao da gerencia; todas sao falas do operador): (a) nenhuma frase poe a IALD como quem testifica do operador (fora da fala em que ele recusa a ordem inversa);
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


# v406: o handoff para a sessao do site (memory\handoff-v406-custodia.md + Nos\HANDOFF_v406_CUSTODIA.md); `k` traz os campos dos recibos do B(n) e os paragrafos do README (fechar_v406.py os le dos recibos e do core): nenhum numero digitado
def handoff(V, k):
    d = _d(V); sc = V["sidecar"]
    k = dict(k)
    for chave in ("ap_nome", "ap_sha", "ap_ver", "ap_evento", "ap_bat", "par_sha", "rel_sha", "rel_man", "readme_paragrafo", "readme_paragrafo_v406"):
        assert chave in k, ("o handoff precisa do campo dos recibos do B(n) e dos paragrafos do README: " + chave)
    par = k["readme_paragrafo"].rstrip("\n"); par_f = k["readme_paragrafo_v406"].rstrip("\n"); err = errata_v405_bloco().rstrip("\n")
    assert par.startswith("### O Teste da Única Palavra (v397"), "o paragrafo do README (quadro) nao e' o do quadro"
    assert par_f.startswith("### O fechamento: a passagem para o contínuo e o certificado habitado (v406"), "o paragrafo da v406 nao e' o novo"
    k.update({"data": V["data"], "s16": V["s16"], "umb": format(V["umb"], ","), "base16": V["base16"], "teor": V["teor"], "rc": V["rc"], "conf16": V["conf16"], "conf_dm": V["conf_dm"], "conf_np": V["conf_np"],
              "pilar": "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), "selo_ts": V["selo_ts"], "num": _num(V), "kernel_prova": _kernel_prova(V), "limites": _limites(V, curto=True), "legal": _legal(V),
              "artigos": ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), "n_cun": d["n_cun"], "n_pedras": V["n_pedras"], "topico": TOPICO_NOVO[:-3], "regra": _regra_do_4_44(V), "erratas_e": _erratas_e(V), "decisoes": _decisoes(V), "leituras": _leituras(V), "moldura": _blocos_fecho(V),
              "sc_nome": "um_absoluto_selo_acom.json", "sc_sha": sc["sha256"], "sc_ver": sc["veredito"], "sc_bytes": format(sc["bytes"], ","), "sc_objs": "; ".join("`%s` sha256 `%s`" % (n, o["sha256"]) for n, o in sc["objetos"].items()),
              "par_bloco": MARC_PAR_INI + "\n" + par + "\n" + MARC_PAR_FIM, "par_v406_bloco": MARC_V406_INI + "\n" + par_f + "\n" + MARC_V406_FIM, "err_bloco": MARC_ERR_INI + "\n" + err + "\n" + MARC_ERR_FIM})
    doc = ("---\nname: handoff-v406-custodia\ndescription: \"HANDOFF v406 (%(data)s) para a sessão do site: o fechamento: o certificado de Fock habitado por construção no kernel do rito e as quatro chaves de testemunha lidas do kernel; validade no kernel não é creditação; `%(s16)s`; B(n) da Bancada feito; TRAZ os parágrafos prontos do README/site, a nota ao lado dos anteriores e lista o sidecar\"\n"
           "metadata:\n  type: project\n---\n\n# HANDOFF v406 — CUSTÓDIA (%(data)s)\n\n"
           "**O que é:** `um.py` **v406** `%(s16)s` (%(umb)s B) sobre a v405 `%(base16)s`; %(teor)s; COMPLETA; rc %(rc)s; selftest PASSED; gate intocado; conferidor `%(conf16)s` (deve mudar %(conf_dm)s; não pode mudar %(conf_np)s); pilar %(pilar)s pela chave. "
           "Selo `%(selo_ts)s`.\n\n"
           "**PARÁGRAFOS PRONTOS para o README do espelho e para o site (colar como estão, cada um entre os seus marcadores; o primeiro é o quadro do Teste da Única Palavra, o MESMO da v397, intocado; o segundo é novo).** O do quadro é gerado pelas MESMAS funções do quadro do artigo "
           "(a função paragrafo_pronto_readme do módulo quadro_v397), sobre o core SELADO do Nós, com os mesmos números e estatutos, e verificado contra o resultado pinado ANTES de este handoff nascer (o fechar recusa se o z_disc aparecer sem o p calibrado e sem a linha dos 5σ no mesmo item, "
           "se a frase do operador não for a verbatim ou se algum número diferir do resultado). O novo é gerado do registro selado `fechamento_v406` e verificado contra o core e contra os números do ensaio a seco "
           "(sem o z_disc do quadro; as citações são trechos verbatim das falas do operador; sem alegação de segurança criptográfica; com a guarda das frases):\n\n%(par_bloco)s\n\n%(par_v406_bloco)s\n\n"
           "**NOTA ao lado dos parágrafos anteriores no README e no site (colar logo abaixo do parágrafo da v405, entre os marcadores; os parágrafos anteriores ficam como registro):**\n\n%(err_bloco)s\n\n"
           "**Os parágrafos do testemunho de dois (v399), da falsidade (v401), da ponte, da queda e da esperança (v402), de Caminho, Verdade e Vida (v403), de Jo 8,32 (v404) e da massa derivada e da identidade definida (v405) SEGUEM COMO ESTÃO.** São os que estão no README do espelho e no site, e esta versão NÃO os regenera nem os substitui (o `um.py` mudou de bytes, mas os parágrafos são dos selos daquelas rodadas). Os registros que os geravam seguem selados e iguais ao selado neste rito (a leitura os confere); só a nota do bloco acima acrescenta o que mudou no estatuto das quatro chaves de testemunha.\n\n"
           "%(moldura)s\n\n%(leituras)s\n\n%(regra)s\n\n%(erratas_e)s\n\n%(decisoes)s\n\n"
           "**O que entrou e o que mediu:** %(num)s.\n\n"
           "**O SIDECAR (arquivo da custódia desde a v399, D5; REESCRITO por este rito):** `%(sc_nome)s` (sha256 `%(sc_sha)s`, %(sc_bytes)s B; veredito `%(sc_ver)s`); objetos selados: %(sc_objs)s. O sidecar fica AO LADO do selo (o selo não pode conter o selo ACOM de si mesmo) e o fechar o copia para `work\\cadeia_de_selo\\v406_selo` e o lista no manifesto de incorporação; "
           "a custódia o leva ao cofre, à PORTA (PORTA.json, URL raw) e ao espelho, junto do selo, porque a segunda testemunha só se confere com ele. A custódia da v399, da v403, da v404, da v405 e da v406 é CONJUNTA. A recusa do selo ACOM só registra (D4); o SHA-256 segue soberano.\n\n"
           "%(kernel_prova)s\n\n%(limites)s\n\n%(legal)s\n\n"
           "**O elo B(n) da Bancada Um (feito antes deste handoff; passo simples, sem salto):** recibo da aplicação `%(ap_nome)s` (sha256 `%(ap_sha)s`; veredito `%(ap_ver)s`; evento %(ap_evento)s; bateria `%(ap_bat)s`); recibo da parada do serviço sha256 `%(par_sha)s`; "
           "recibo do religamento sha256 `%(rel_sha)s` (versão servida v406, manifesto `%(rel_man)s`).\n\n"
           "**Para a sessão do site (custódia):** o `um.py` v406, `rodada_v406_stdout.txt`, o selo, o sidecar, o core, o .md canônico (com o quadro no topo, intocado) e o manifesto, os artigos PT/EN (%(artigos)s; o quadro «O Teste da Única Palavra» abre os dois), as %(n_cun)s inscrições por sha256 "
           "(todas falas do operador; lista na linhagem e no tópico `%(topico)s`; arquivos em `work\\cadeia_de_selo\\v406\\insumos\\cunhagens`), os %(n_pedras)s módulos novos (`TGLExt.F1Fecho394`) e os dois diffs (`DIFF_v405_v406.diff`, `DIFF_KERNEL_v406.txt`) — com PORTA gerada por script, "
           "URL raw (o um.py tem mais de 5 MB), backup da versão v405 no espelho fora do repositório, blob conferido depois do push. Colocar os PARÁGRAFOS acima no README do espelho e no site (ato da sessão do site, com o selo corrente ao lado; o do quadro e os anteriores seguem onde estão, e o novo entra ao lado, com a NOTA); "
           "publicar os módulos novos no espelho (TGLExt/F1Fecho394) e regenerar as PORTAS de `tgl_kernel`, `TGLExt` e `TGL`; a pasta `insumos` vai ao espelho com PORTA: sem ela, uma reprodução pública diz NOT_SEALED (fail-closed); os recibos da bateria do B(n) vão ao espelho com PORTA; o runner da Fronteira e a camada v406 dos 16 dispositivos; a revisão independente (o Sonnet, D37) antes do portão do operador. "
           "A publicação do bloco embutido do método do operador no espelho público segue sujeita à decisão [LEGAL] D2 (operador com a agente de PI). O README pinado e a linha do quadro no site (D39) são plano à parte, a executar na custódia ou depois, por decisão dele; a regra do z_disc calibrado (nunca sozinho) vale em qualquer superfície.\n\n"
           "**Pendências SÓ do operador:** o nome da candidata e das pedras candidatas do dia; a decisão [LEGAL] D2; o README pinado (D39); a ratificação das decisões D34 a D40 da gerência que ele ainda não leu. [OPEN]: a discriminação a 5σ (β_TGL na natureza), K(O) ≠ ⊥ para O compacto, o lema que liga o psíon ao canto, o magnetismo na cadeia da tensão, qual é o disco, quais são as cinco notas, `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura e rank c = 4, "
           "`IsotropicPost` no atlas curvo, a dimensão 3, a instância do índice 1/β, a atestação física externa, a identificação do dispositivo físico (R4/R5) e a independência das quatro bandeiras experimentais do gate (um só booleano; os mocks de survey).\n\n"
           "Pacote e cadeia: `work\\cadeia_de_selo\\v406` (+ `pos_rito`); arquivo `work\\cadeia_de_selo\\v406_selo` e `v406_kernel`. NOT_FALSIFIED não é a palavra da creditação; o gate não se move.\n\n"
           "[[%(topico)s]] [[missao-ultima-flag-um-py]] [[handoff-v405-custodia]]\n") % k
    assert k["par_bloco"] in doc and k["par_v406_bloco"] in doc and k["err_bloco"] in doc, "os paragrafos do README e a nota nao entraram no handoff"
    assert not atribuicao_da_gerencia(doc), ("o handoff atribui mal ou inverte a direcao do testemunho", atribuicao_da_gerencia(doc)[:2])
    return doc


# v406: a linha da arvore da prova
def arvore_linha(V):
    d = _d(V); DL_ = _qd().DL
    return ("- **O FECHAMENTO (v406)** `%s`: %d módulos novos no kernel, %d bandeiras novas True, escada %s → %s; o certificado de Fock está habitado por construção e as quatro chaves de testemunha são lidas do kernel do rito: %s [REAL os termos e a leitura; INPUT/ONTO a ordem e as leituras do operador; KNOWN/DECLARADO o núcleo II_inf, o parecer R7 e a ratificação]; "
            "o registro `fechamento_v406` confere os termos; as %d inscrições por sha256 (todas do operador); validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["n_pedras"], d["n_f"], V["escada_antes"], d["depois"], DL_.FRASE_DA_MOLDURA_V406_PT, d["n_cun"]))


# v406: o titulo do verbete do indice
def titulo_verbete(V):
    return "O fechamento (v406): a passagem para o contínuo e o certificado de Fock habitado por construção no kernel do rito; as quatro chaves de testemunha lidas do kernel:"


# v406: o corpo do verbete do indice
def verbete(V):
    return "[REAL — rodada v406 `%s`] %s." % (V["s16"], _num(V))


# v406: a entrada do remissivo
def remissivo(V):
    return "- **O fechamento, as quatro chaves de testemunha lidas do kernel e as inscrições de 02/11 (v406)** — o registro `fechamento_v406`, `cunhagens_v406`, `kh_n1_cobertura_v406`, `%s`" % TOPICO_NOVO


MARC_V406_INI = "<!-- INICIO_PARAGRAFO_O_FECHAMENTO_v406 -->"; MARC_V406_FIM = "<!-- FIM_PARAGRAFO_O_FECHAMENTO_v406 -->"


MARC_ERR_INI = "<!-- INICIO_ERRATA_V405_V406 -->"; MARC_ERR_FIM = "<!-- FIM_ERRATA_V405_V406 -->"


def _lst(xs):
    """Lista numerica lida do registro, em PT: inteiros sem casas, listas aninhadas entre parenteses."""
    return ", ".join(("(" + _lst(x) + ")") if isinstance(x, (list, tuple)) else _pn(x, 6) for x in xs)


def _sem_chaves(t):
    """Os textos vindos do core podem trazer chaves (e^{-s}); os textos renderizados nao as tem (a conferencia de formatacao reprova): chaves viram parenteses."""
    return t.replace("{", "(").replace("}", ")")


def _erratas_e(V):
    """As erratas E14 a E17 (em nome proprio da gerencia c1), LIDAS do registro cunhagens_v406 do core: nenhuma e' digitada aqui."""
    _d(V); er = _g(_core(), "cunhagens_v406", "erratas") or []
    assert len(er) == 4, "o registro cunhagens_v406 nao traz as quatro erratas"
    itens = []
    for e in er:
        itens.append(_sem_chaves("- %s **Dizia:** %s **Lacuna de fidelidade:** %s **Estatuto:** %s" % (e["agora"], e["dizia"], e["lacuna_de_fidelidade"], e.get("estatuto", ""))))
    return ("**Erratas ao lado (em nome próprio da gerência c1, 02/11/2026; os literais das versões anteriores, os specs marcados «até a v405», o texto antigo de `neutrino_mass.angle_status` e as pedras seladas ficam como registro; nenhum módulo já instalado foi editado):** a v406 entra COM quatro erratas, lidas do registro `cunhagens_v406`:\n" + "\n".join(itens))


def _decisoes(V):
    """As decisoes D34 a D40 da gerencia c1, LIDAS do registro cunhagens_v406."""
    _d(V); ds = _g(_core(), "cunhagens_v406", "extras", "decisoes") or {}
    ks = ("D34", "D35", "D36", "D37", "D38", "D39", "D40")
    assert all(k in ds for k in ks), "as decisoes D34 a D40 nao estao no registro cunhagens_v406"
    return "**Decisões** [da gerência c1, em nome próprio, ratificáveis pelo operador; as que trazem fala dele dizem o sha16]:\n" + _sem_chaves("\n".join("- %s: %s%s" % (k, ds[k], (" [regra do 4,44: " + _z444() + "]") if "4,44" in ds[k] else "") for k in ks))


# ---------------------------------------------------------------- o PARAGRAFO NOVO da v406 e a NOTA ao lado dos paragrafos anteriores
def _linha_maquina_v406(core, d):
    """A linha de maquina do paragrafo novo (os numeros LIDOS do registro do core), em PT."""
    fv = core["fechamento_v406"]["values"]
    return ("modulos=%s; bandeiras=%s; ancoras=%s; escada=%s; checagens=%s; certificado_habitado=%s; falas_sha16=%s/%s"
            % (d["n_mod"], d["n_f"], fv["n_ancoras_ok"], "/".join(str(x) for x in dict.fromkeys(fv["escada"])), core["fechamento_v406"]["mechanics"]["n_checks"], fv["certificado_habitado_lido_do_kernel"], d["s_construir"], d["s_passagem"]))


def _dados_paragrafo(core):
    """O que o paragrafo precisa do core SELADO e de ESPERADOS (sem V): as contagens e as falas."""
    esp = _esp(); DL_ = _qd().DL
    for n in ("fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406"):
        assert (core.get(n) or {}).get("all_verified") is True, "o registro %s nao selou: nenhum paragrafo diz os numeros assim" % n
    fe = core["fechamento_v406"]; fv = fe["values"]
    assert fv["n_modulos_ok"] == fv["n_modulos"] == DL_.N_BUNDLE and fv["n_flags_true"] == fv["n_flags"] == esp["n_bandeiras_novas"] and fv["n_ancoras_ok"] == len(DL_.ANCORAS), "os valores do registro fechamento_v406 nao sao os do ensaio a seco"
    return {"n_mod": DL_.N_BUNDLE, "n_f": esp["n_bandeiras_novas"], "escada": (esp["escada_v405_e_v406"][0], esp["escada"][1]), "s_construir": _sha_por(DL_.N_CONSTRUIR), "s_passagem": _sha_por(DL_.N_PASSAGEM), "s_compile": _sha_por(DL_.N_COMPILE), "n_checks": fe["mechanics"]["n_checks"]}


def _paragrafo_v406_de(core):
    """O texto do paragrafo da v406, funcao PURA dos registros selados do core (os numeros sao lidos dos registros, nunca digitados; as frases de limite saem do proprio registro)."""
    d = _dados_paragrafo(core); DL_ = _qd().DL; fe = core["fechamento_v406"]
    q_c = _cita(DL_.FRASE_CONSTRUIR); q_p = _cita(DL_.FRASE_PASSAGEM); q_k = _cita(DL_.FRASE_CHAVE)
    ress = "; ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(fe["ressalvas"]))   # inteiras (R2 da revisao de terceiro: o corte nos dois-pontos deixava as ressalvas sem a segunda metade)
    ls = ["### O fechamento: a passagem para o contínuo e o certificado habitado (v406, 02/11/2026) — parágrafo pronto para o README do espelho e para o site",
          "",
          "> **O fechamento: a passagem para o contínuo e o certificado habitado (v406, 02/11/2026)** [REAL: os termos do kernel do rito e as quatro chaves lidas do kernel · INPUT: a ordem do operador · ONTO: as leituras dele · KNOWN/DECLARADO: o núcleo II_inf, o parecer R7, a ratificação da gerência · OPEN: K(O) ≠ ⊥ para O compacto, o lema que liga o psíon ao canto, o teste com a natureza]",
          ">",
          "> - **O que entrou** [REAL]: %s módulos novos no kernel (`TGLExt.F1Fecho394`: os 300 da bancada do ChatGPT, recompilados do fonte, e a candidata `%s`; o nome é provisório, porque os nomes das pedras são do operador e ele ainda não a nomeou), com %s bandeiras, todas no trio; escada %s → %s (sha16 das falas `%s`, `%s`)." % (d["n_mod"], DL_.TESTEMUNHA["name"], d["n_f"], d["escada"][0], d["escada"][1], d["s_construir"], d["s_passagem"]),
          "> - **O certificado de Fock está habitado por construção** [REAL · INPUT]: %s." % _sem_chaves(fe["diz"][1]),
          "> - **As quatro chaves** [REAL]: %s." % _sem_chaves(fe["diz"][2]),
          "> - **O que não muda** [REAL]: %s." % _sem_chaves(fe["diz"][3]),
          "> - **A ordem do operador** [INPUT]: %s; a prioridade, %s, e %s." % (q_c, q_p, q_k),
          "> - **As ressalvas, ditas** [OPEN · KNOWN/DECLARADO · REAL]: %s." % _sem_chaves(ress),
          "> - **O que o registro NÃO diz** [REAL]: %s." % _sem_chaves("; ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(fe["nao_diz"]))),
          "> - **Limites:** %s; o registro CONFERE os termos, as fontes por sha256 e as quatro chaves lidas, e quem prova é o kernel; `NOT_FALSIFIED` nunca é a palavra da creditação; isto não é teste e não acrescenta dado; este parágrafo não traz o número do quadro (o quadro do Teste da Única Palavra segue no README com a sua linha dos 5σ)." % DL_.FRASE_DA_MOLDURA_V406_PT,
          "> - **Origem.** Os números são lidos do core selado desta rodada; nenhum é digitado. Linha de máquina: `%s`." % _linha_maquina_v406(core, d)]
    return "\n".join(ls) + "\n"


def verificar_paragrafo_v406(par, core, esp):
    """Verifica o paragrafo da v406 contra o core selado E contra ESPERADOS (o ensaio a seco): devolve a lista de falhas (vazia = passou). As verificacoes:
    (1) os numeros do core (o registro fechamento_v406) == os de ESPERADOS/delta e cada um esta no paragrafo, formatado; (2) o paragrafo == o gerado do core; (3) NAO traz o 4,44 nem o z_disc (a regra do 4,44 e' do quadro); (4) os estatutos;
    (5) as frases de limite e as ressalvas; (6) toda citacao entre « » e' verbatim numa fala DO OPERADOR ou rotulo; (7) nenhuma alegacao de seguranca criptografica, «consciencia» so' como palavra retirada, a direcao sem inversao; (8) a guarda P18 e a guarda das frases."""
    fa = []
    DL_ = _qd().DL
    fe = core.get("fechamento_v406") or {}; fv = fe.get("values") or {}
    try:
        nums = {"modulos": str(DL_.N_BUNDLE), "bandeiras": str(esp["n_bandeiras_novas"]), "escada antes": str(esp["escada_v405_e_v406"][0]), "escada depois": str(esp["escada"][1]), "sha16 da ordem": _sha_por(DL_.N_CONSTRUIR), "sha16 da prioridade": _sha_por(DL_.N_PASSAGEM), "candidata": DL_.TESTEMUNHA["name"]}
        if not (fv and fv.get("n_modulos_ok") == DL_.N_BUNDLE and fv.get("n_flags_true") == esp["n_bandeiras_novas"] and fv.get("n_ancoras_ok") == len(DL_.ANCORAS) and fe.get("certificate_inhabited") is True):
            fa.append("os valores do registro fechamento_v406 no core != ESPERADOS/delta")
    except KeyError as e:
        nums = {}; fa.append("valor ausente: %s" % e)
    for k, v in nums.items():
        if v not in par:
            fa.append("numero (%s = %s) ausente do paragrafo" % (k, v))
    try:
        if par != _paragrafo_v406_de(core):
            fa.append("o paragrafo difere do gerado pelas funcoes sobre os registros selados do core")
    except AssertionError as e:
        fa.append("o paragrafo nao pode ser gerado do core: %s" % str(e)[:120])
    if re.search(r"4[,.]44|z_disc", par):
        fa.append("o paragrafo da v406 traz o 4,44 ou o z_disc (a regra do 4,44 e' do quadro; este paragrafo nao o cita)")
    for st in ("[REAL", "INPUT", "ONTO", "OPEN", "DECLARADO", "KNOWN"):
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    for frase in (DL_.FRASE_DA_MOLDURA_V406_PT, "validade no kernel nao e creditacao", "o gate nao se move", "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "K(O)", "R7", "II_inf", "é provisório", "ENNReal", "quem prova é o kernel", "isto não é teste", "lema"):
        if frase not in par:
            fa.append("frase de limite ausente do paragrafo: " + frase)
    for r_ in DL_.RESSALVAS_V406:
        c_ = _sem_chaves(r_)   # a ressalva inteira (R2 da revisao de terceiro)
        if c_ not in par:
            fa.append("ressalva ausente do paragrafo: " + c_[:60])
    corpus = [re.sub(r"\s+", " ", dd["text"]) for dd in _falas().values() if dd["autor"] == "operador"]
    for q in re.findall(r"«([^»]*)»", par):
        if len(q) >= 13 and not any(q in t for t in corpus) and q not in " ".join(DL_.RESSALVAS_V406) and q not in " ".join(fe.get("diz") or []) and q not in " ".join(fe.get("nao_diz") or []):
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
    from guarda_p18_v406 import violacoes
    import guarda_frases_v406 as GF
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    v2 = GF.violacoes(par)
    if v2:
        fa.append("a guarda das frases achou %r" % (v2[:2],))
    return fa


def paragrafo_v406():
    """(texto, relatorio): o paragrafo NOVO da v406, pronto para colar no README do espelho e no site, gerado do core SELADO do Nos e verificado contra o core E contra ESPERADOS;
    levanta AssertionError (o fechar RECUSA) se algo nao conferir."""
    core = _core(); esp = _esp()
    par = _paragrafo_v406_de(core)
    fa = verificar_paragrafo_v406(par, core, esp)
    assert not fa, ("o paragrafo da v406 nao passou nas verificacoes", fa[:4])
    return par, {"sha16": hashlib.sha256(par.encode("utf-8")).hexdigest()[:16], "verificacoes": "numeros == ESPERADOS/delta; igual ao gerado do core; sem o 4,44; estatutos; limites e ressalvas; citacoes verbatim (falas do operador ou texto do registro); sem alegacao de seguranca criptografica; guarda P18; guarda das frases", "guarda_p18": "limpa"}


def errata_v405_bloco():
    """O bloco de NOTA ao lado dos paragrafos anteriores (v394 a v405) no README do espelho e no site: as quatro chaves de testemunha eram literal False e passaram a leitura do kernel (E14). Texto lido do registro cunhagens_v406; a guarda P18 confere."""
    _kernel_tem(("physicalFockCertificate",))
    er = (_g(_core(), "cunhagens_v406", "erratas") or [None])[0]
    assert er and er["agora"] == _qd().DL.ERRATA_E14 and str(er.get("assinatura", "")).startswith("gerencia c1, em nome proprio"), "a errata E14 do registro cunhagens_v406 nao e' a do delta"
    t = ("> **Nota ao lado dos parágrafos anteriores (v394 a v405) — gerência c1, em nome próprio, 02/11/2026:** onde um parágrafo ou texto publicado antes diz que o certificado de Fock, a face do psíon ou o contrato conjunto da rede não tinham habitante, isso era verdade na data e fica como registro. " + _sem_chaves(er["agora"])
         + " Os módulos selados das versões anteriores NÃO foram editados nem renomeados, e os registros delas seguem selados; o que o parágrafo da v405 e os anteriores dizem sobre as pedras, o cálculo e os limites não muda.\n")
    sys.path.insert(0, PK)
    from guarda_p18_v406 import violacoes
    import guarda_frases_v406 as GF
    assert not violacoes(t) and not GF.violacoes(t), "a guarda P18 ou a das frases achou palavra recusada na nota ao lado dos paragrafos anteriores"
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


def _fam_gate():
    """As contagens por familia do gate (formais, fisicas, experimentais), LIDAS do qg_closure do core do Nos."""
    qg = _core().get("qg_closure") or {}
    return [len(qg.get(f) or {}) for f in ("formal_flags", "physics_flags", "experiment_flags")]


def _sha_verdade():
    """O sha16 da pedra Verdade (v392) no kernel do Nos (o homonimo que a «Verdade» sozinha repetiria), LIDO do arquivo."""
    return s16(os.path.join(NOS, "tgl_kernel", "TGLExt", "Verdade.lean"))


# os temas das falas de 30/10 a 01/11 sao os proprios nomes dos arquivos (resumo dado no nome, nunca citacao); o sha16, a data e o autor vem dos bytes e do nome, nunca daqui. So' o nome que carrega uma frase que a guarda recusa e' reescrito.
_TEMA_ESPECIAL = {"nomes_das_sete_pedras_e_tudo_derivado": "os nomes das sete pedras e o pedido de que não restassem hipóteses nomeadas"}


def _tema(nome):
    """O tema de uma fala: o nome do arquivo sem o autor, a data e o sufixo (o resumo que a gerencia deu ao gravar; nunca citacao)."""
    t = re.sub(r"_verbatim\.txt$", "", re.sub(r"^(?:OPERADOR|GERENCIA)_\d{2}(?:out|nov)_", "", nome))
    return _TEMA_ESPECIAL.get(t, t.replace("_", " "))


def _moldura(V):
    """A MOLDURA da v406, LIDA do registro fechamento_v406 do core: a frase da moldura (delta) e o estatuto que o registro grava."""
    d = _d(V); fe = _fe(); DL_ = _qd().DL
    assert "creditacao" in DL_.FRASE_DA_MOLDURA_V406_PT, "a frase da moldura nao e' a do delta"
    return _sem_chaves(_f("**A moldura [REAL · INPUT · ONTO · KNOWN/DECLARADO · OPEN; registro `fechamento_v406`, {nck} checagens]:** {frase}. Estatuto do registro, como o `um.py` o grava: {est}.", nck=d["n_ck_fe"], frase=DL_.FRASE_DA_MOLDURA_V406_PT, est=fe["estatuto"]))


def _fe():
    """O registro fechamento_v406 do core SELADO do Nos (so' leitura); recusa se nao selou."""
    fe = _core().get("fechamento_v406") or {}
    assert fe.get("all_verified") is True and fe.get("certificate_inhabited") is True and fe.get("does_not_gate_core") is True, "o registro fechamento_v406 nao selou no core do Nos: nenhum texto diz o fecho assim"
    return fe


def _escopo(V):
    """O que entra: o escopo do registro fechamento_v406, como o um.py o grava."""
    _d(V); fe = _fe()
    return _sem_chaves("**O que entra (escopo do registro `fechamento_v406`)** [REAL]: " + fe["scope"])


def _ancoras(V):
    """As oito ancoras do fecho: nome Lean curto, modulo e papel (delta_v406.ANCORAS), conferidas no kernel do rito pela leitura."""
    d = _d(V); DL_ = _qd().DL; fe = _fe()
    assert set(fe["anchors"]) == set(DL_.ANCORAS) and all(a_ is True for a_ in fe["anchors"].values()) and all((a_ or {}).get("ok") is True for a_ in (fe["values"].get("ancoras") or {}).values()), "as ancoras do registro != delta_v406.ANCORAS"
    itens = "; ".join("`%s` (módulo `%s`: %s)" % (n.split(".")[-1], DL_.ANCORAS[n]["rel"].split("/")[-1][:-5], DL_.ANCORAS[n]["papel"]) for n in DL_.ANCORAS)
    return _sem_chaves(_f("**As oito âncoras** [REAL; lidas do `axiom_report` do rito, só no trio, com a proveniência que o compilador emite no módulo esperado e a bandeira True]: {itens}.", itens=itens))


def _chaves(V):
    """As quatro chaves de testemunha (delta_v406.CHAVES_V406) e o que o rito leu delas (V['chaves'])."""
    d = _d(V); DL_ = _qd().DL; fk = V["chaves"]
    assert fk["kernel_reads_the_certificate_as_inhabited"] is True and fk["rede_fock_v394.whole_certificate_inhabited"] is True and fk["psibit_v395.conditional_psion_face.status"] == DL_.STATUS_HABITADO == fk["testemunha_estatica_v396.fock_face.status"], "as quatro chaves nao estao lidas do kernel como o delta diz"
    itens = "; ".join("`%s` (era: %s; agora: %s; desde a %s)" % (c_["chave"], c_["era"], c_["agora"], c_["desde"]) for c_ in DL_.CHAVES_V406)
    ff = "; ".join("`%s` (lido: %s)" % (n_, {"full_static_witness_exists": fk["qg_closure.gate.full_static_witness_exists"], "trivial_inhabitant_exists": fk["witness_rigidity.trivial_inhabitant_exists"]}[n_]) for n_ in DL_.FICAM_FALSE_POR_TEOREMA)
    return _sem_chaves(_f("**As quatro chaves de testemunha** [REAL; errata E14 ao lado; registro `fechamento_v406`]: deixaram de ser literal False e são LIDAS do kernel do próprio rito: {itens}. Lido neste rito: o kernel lê o certificado como habitado = {h}; a face do psíon e a da testemunha estática leem o status `{st}`. "
                          "Ficam False por teorema: {ff}. Segue False, porque nenhum lema liga o psíon ao canto: `{lk}` (lido: {lkv}).",
                          itens=itens, h=fk["kernel_reads_the_certificate_as_inhabited"], st=DL_.STATUS_HABITADO, ff=ff, lk=DL_.FICA_FALSE_SEM_LEMA.split(".")[-1], lkv=fk["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"]))


def _diznao(V):
    """O que o registro diz e o que NAO diz: as listas diz e nao_diz do registro fechamento_v406."""
    _d(V); fe = _fe()
    return _sem_chaves("**O que o registro diz** [REAL]: " + "; ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(fe["diz"])) + ". **O que o registro NÃO diz:** " + "; ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(fe["nao_diz"])) + ".")


def _ressalvas(V):
    """As ressalvas (D36), ditas uma a uma: delta_v406.RESSALVAS_V406 == fechamento_v406.ressalvas."""
    _d(V); fe = _fe(); DL_ = _qd().DL
    assert list(fe["ressalvas"]) == list(DL_.RESSALVAS_V406) and len(fe["ressalvas"]) >= 8, "as ressalvas do registro != delta_v406.RESSALVAS_V406"   # (a revisao de terceiro R1 acrescentou duas: 10 em 02/11 22h)
    return _sem_chaves("**As ressalvas, ditas (D36)** [OPEN · KNOWN/DECLARADO · REAL, uma a uma]: " + "; ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(fe["ressalvas"])) + ".")


def _leituras(V):
    """As leituras [ONTO] do operador de 02/11, LIDAS do registro cunhagens_v406 (extras.leituras) e conferidas contra delta_v406."""
    d = _d(V); x = _g(_core(), "cunhagens_v406", "extras", "leituras") or {}; DL_ = _qd().DL
    assert x and x == DL_.LEITURA_V406 and "ONTO" in str(x.get("estatuto")), "a leitura da v406 nao e' a de delta_v406"
    outras = ", ".join("`%s`" % k_ for k_ in x if k_ not in ("espelhamento", "um_inscrito", "um_comprimido", "estatuto"))
    return _sem_chaves("**As leituras do operador de 02/11** %s: (espelhamento) %s; (um_inscrito) %s; (um_comprimido) %s. As demais leituras e ordens (%s) ficam no registro `cunhagens_v406`, cada uma com o estatuto que a fala dele autoriza; nenhuma é termo de kernel." % (x["estatuto"], x["espelhamento"], x["um_inscrito"], x["um_comprimido"], outras))


def _blocos_fecho(V):
    return "\n\n".join([_moldura(V), _escopo(V), _ancoras(V), _chaves(V), _diznao(V), _ressalvas(V)])
