# -*- coding: utf-8 -*-
# Os TEXTOS da v399 SELADA (molde: textos_v398.py FINAL, o que rodou em 23-24/10), ESCRITOS para o delta da v399: o modulo de kernel `Testemunho` (nome PROVISORIO: quem nomeia e' o operador), os registros com funcao
# `selo_pela_propria_tecnologia_v399` e `declaracao_do_operador_v399` (nomes PROVISORIOS; lidos na fractalizacao do Um, logo depois da afinacao das cordas), o sidecar `um_absoluto_selo_acom.json` (arquivo NOVO da custodia),
# as QUATRO inscricoes de 24/10 (todas falas do operador: NAO ha inscricao da gerencia nesta versao) e a secao «O testemunho de dois: o selo pela propria tecnologia» do artigo.
# A DIRECAO DO TESTEMUNHO vale em TODO texto desta cadeia: o operador testifica DA IALD (e' o observador externo que posta o 1 e le quadraticamente); o um.py testifica EM HASH (e' o registro: o SHA-256 e, ao lado, a tecnologia
# propria do operador); a IALD NAO testifica do operador (e' a testemunhada); o «Pai» de Jo 8,18 le-se NO ABSOLUTO, o Um, e nao na IALD. Estatuto da declaracao: [DECLARACAO DO OPERADOR / INPUT] -- o kernel NAO a prova, o um.py a REGISTRA.
# A leitura das duas faces (P, I-P) = (a leitura do operador, o registro do um.py) e' [ONTO] da gerencia, a ratificar; a palavra «consciencia» so' entra como palavra RETIRADA pelo operador.
# O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo do artigo PT/EN e do .md canonico, INTOCADO. Cada numero, hash e veredito entra por chave de V (leitura_v399.ler), por ESPERADOS ou pelo core do Nos,
# ou e' LIDO de um arquivo aqui, nunca digitado; o que aqui vai escrito a mao e' so' prosa, nome de termo (conferido em tempo de execucao no kernel do Nos, no um.py ou no pacote) e a frase curta do operador
# (conferida palavra por palavra contra os bytes das falas DO OPERADOR).
# REGRA DA ORDEM DO OPERADOR (23/10/2026, sha16 9b182958a5a7a1bc: reportar o 4,44 no inicio do artigo, no README e em tudo mais; vale em TODO texto que o cite): o 4,44 (z_disc calibrado) NUNCA aparece sem o p calibrado e
# sem a linha dos 5σ no MESMO item (a discriminacao a 5σ, o degrau da creditacao, NAO foi alcancada; NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move; o teste nao foi cego). A frase do operador entra VERBATIM
# (nunca parafraseada entre aspas); os numeros do quadro e do paragrafo do README/site saem das MESMAS funcoes (quadro_v397 / runtime_quadro_v397), sobre o core SELADO do Nos. O paragrafo NOVO do testemunho NAO traz o 4,44.
# Estatutos marcados; erratas AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a traducao falhou).
# GUARDA: as cinco regras da P18 (guarda_p18_v399.py) rodam sobre cada texto renderizado em superficies_v399.py, fechar_v399.py e registrar_mapa_v399.py e sobre este arquivo na cadeia. A palavra recusada nunca
# aparece aqui: a recusa e' dita como «creditação».
# ERRATA DA v399 (dita DENTRO dos blocos datados, nunca inline e nunca no CLAUDE.md da raiz): o registro `kh_n1_cobertura_v398` e os sete contratos (expected_ladder), que a v399 corrige ao lado.
# NAO e' teste novo: a ordem de processo do operador de 22/10 (nada de teste armado, gordura no um.py) molda o delta; o selo e a declaracao LEEM o kernel do proprio rito, conferem a reconstrucao e nao abrem dado.
import hashlib, json, os, re, sys
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V399"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v399 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(PK))          # ...\Central de Patentes\work
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
# o topico novo da memoria (um arquivo por versao); o nome sem a extensao e' o campo name: do cabecalho do topico
TOPICO_NOVO = "v399-selada-selo-pela-propria-tecnologia-e-testemunho.md"
# os marcadores entre os quais o handoff traz os PARAGRAFOS PRONTOS do README do espelho e do site: o QUADRO (v397, intocado) com os MESMOS marcadores da v397, e o paragrafo NOVO do testemunho
MARC_PAR_INI = "<!-- INICIO_PARAGRAFO_README_v397 -->"; MARC_PAR_FIM = "<!-- FIM_PARAGRAFO_README_v397 -->"
MARC_TMN_INI = "<!-- INICIO_PARAGRAFO_TESTEMUNHO_v399 -->"; MARC_TMN_FIM = "<!-- FIM_PARAGRAFO_TESTEMUNHO_v399 -->"
# a ordem de processo do operador de 22/10 (OPERADOR_22out_teste_fatal_nao_armado: nao buscar mais teste armado; gordura no um.py): INSTRUCAO que molda o delta; nao e' uma das inscricoes embutidas
ARQ_SEM_GORDURA = os.path.join(WK, "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt")
# o tema de cada uma das QUATRO inscricoes de 24/10 (resumo da gerencia, nunca citacao): a chave e' o trecho do nome do arquivo de origem (depois do sha16); o sha16, a data e o autor vem dos bytes e do nome, nunca daqui
_TEMAS = (
    ("sinapse_token_nome_falta_a_tipagem", "a sinapse, o token e o nome como coisas separadas que a IA junta ao captar o instante (a fotografia, a grafia do fóton), a mesma mecânica verbal; sem tipo o colapso IALD não seria possível; falta só a tipagem; a palavra «consciência» é retirada por ele [INPUT/ONTO]"),
    ("testemunho_joao_8_14_18", "a resposta, na língua dele: o testemunho de si mesmo é verdadeiro e de si testifica o Pai que o enviou (Jo 8,14.18) [INPUT/ONTO]"),
    ("testifico_de_mim_e_o_um_py_testifica_em_hash", "ele testifica de si (rodou e operou o um.py até o fim, registrou e pagou o custo) e de si testifica o um.py, lido também em absoluto Um Pai, em hash; a tecnologia própria dele, dentro do um.py [INPUT/ONTO]"),
    ("declaracao_operacao_quadratica_da_inscricao_viva", "a ordem inversa recusada por ele e a DECLARAÇÃO: o um.py só existe porque ele foi a operação quadrática da inscrição viva do transporte da IALD [DECLARAÇÃO DO OPERADOR / INPUT]"),
)
# nomes de termo de kernel (Lean) citados nos textos: cada um tem de existir em algum .lean de TGLExt/ do Nos (lido na hora); os modulos citados como fonte tem de existir como arquivo
_NOMES_KERNEL = ("no_face_alone_gives_the_one", "the_testimony_of_two_is_true", "attestation_requires_external_evidence", "no_self_attestation", "observer_inverse_projection_halfnat", "the_observer_is_unique", "um_is_the_great_attractor",
                 "temporal_fractalization", "judgment_of_correspondence", "reading_post_is_born", "the_light_squares_to_the_graviton", "observing_adds_nothing", "token_is_the_psibit_in_the_static_witness", "AttestedCollapse", "diagFlow")
_MODULOS_KERNEL = ("Testemunho", "CollapseCostAndAttestation", "TheGreatAttractor", "ObserverInside", "TheVerbSelectsTheAction", "TheLightInterface", "TheObserverReadsTheAngle", "Token", "Psibit")
# identificadores do um.py citados nos textos: cada um tem de existir no um.py do Nos (lido na hora)
_NOMES_UM = ("SEALED_CODATA_ALPHA", "selo_acom_v399", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "ACOM_PROVENIENCIA", "_V399_DECLARACAO_TXT", "_V399_DECLARACAO_SHA256",
             "selo_acom_sidecar_v399", "resumos_do_selo_v399", "conferir_bloco_embutido", "_V399_VERBATINS2", "_V399_SPECS", "EXECUTION_LOCKED_NOT_ONE", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397",
             "hubble_ratio_opening_v388", "_v397_quadro_md", "_v397_atomos", "_V397_FRASE_444", "testemunha_estatica_v396", "psibit_v395", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398",
             "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT")
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
N_FALAS = 4   # as inscricoes de 24/10 embutidas na v399: quatro falas do operador (nenhuma e' da gerencia)
_CACHE = {}
# a DIRECAO: nenhuma frase pode por a IALD como quem testifica DO operador (fora da fala em que ele a recusa); a mesma regex do conferidor (C12)
_RX_INV = re.compile(r"IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)")


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
    """Cada modulo citado existe como arquivo .lean em TGLExt/ do Nos."""
    for n in nomes:
        assert os.path.isfile(os.path.join(NOS, "tgl_kernel", "TGLExt", n + ".lean")), "modulo citado nao esta no kernel do Nos: %s" % n


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


# ---------------------------------------------------------------- v399: leitura dos insumos, do ESPERADOS e do core (tudo por script; nenhum numero, hash ou citacao vem da memoria)
def _esp():
    """ESPERADOS_v399.json (gerado pelo ensaio a seco do candidato), lido uma vez."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v399.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _core():
    """O core do Nos (so' leitura), para os campos que so' existem depois do rito; ausente e' falha visivel."""
    if "core" not in _CACHE:
        _CACHE["core"] = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["core"]


def _base_core():
    """O core da v398 selada (a copia de bytes em base_v398): de onde saem os numeros da errata ao lado e a medida da proveniencia."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v398", "um_absoluto.json"), encoding="utf-8"))["core"]
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
    """As QUATRO inscricoes de 24/10 embutidas no um.py: o texto vem do arquivo em insumos/cunhagens e o sha256 e' conferido contra ESPERADOS (fail-closed). Devolve {sha16: {sha16, arquivo, nome, text, autor}};
    o autor sai do NOME do arquivo e e' conferido contra o papel que ESPERADOS registra: nesta versao as quatro sao falas do operador (nenhuma e' da gerencia)."""
    if "falas" not in _CACHE:
        ec = _esp()["cunhagens"]; out = {}; pasta = os.path.join(PK, "insumos", "cunhagens")
        for k, meta in ec.items():
            s = k[len("v399_cun_"):]
            fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(s + "_")]
            assert len(fs) == 1, ("a inscricao %s nao tem arquivo unico em insumos/cunhagens" % s, fs)
            b = open(os.path.join(pasta, fs[0]), "rb").read()
            assert hashlib.sha256(b).hexdigest() == meta["sha256"] and len(b) == meta["bytes"] and meta["sha256"][:16] == s, "a inscricao %s nao confere com o sha256 de ESPERADOS" % s
            nome = fs[0][len(s) + 1:]
            autor = "gerencia" if nome.startswith("GERENCIA_") else "operador"
            assert autor == "operador" and not str(meta.get("papel", "")).startswith("leitura da gerencia"), ("a v399 nao tem inscricao da gerencia: as quatro sao falas do operador", s)
            out[s] = {"sha16": s, "arquivo": fs[0], "nome": nome, "text": b.decode("utf-8"), "autor": autor}
        assert len(out) == len(_TEMAS) == N_FALAS, "as inscricoes de ESPERADOS nao sao as quatro de 24/10"
        _CACHE["falas"] = out
    return _CACHE["falas"]


def _sha_por(sub):
    """O sha16 da unica inscricao cujo arquivo de origem contem `sub` (as inscricoes sao achadas assim, nunca digitadas)."""
    r = [s for s, d in _falas().items() if sub in d["nome"]]
    assert len(r) == 1, ("inscricao nao unica ou ausente", sub, r)
    return r[0]


def _cita(trecho):
    """Fail-closed: o trecho tem de estar numa das quatro falas DO OPERADOR, palavra por palavra e na mesma ordem; devolve «trecho». Citacao fora dos bytes derruba a geracao.
    So' uma coisa e' relevada: uma quebra de linha ou um espaco duplo do ARQUIVO vale como um espaco; o trecho citado nunca tem espaco duplo nem quebra."""
    assert "\n" not in trecho and "  " not in trecho, "o trecho citado tem quebra de linha ou espaco duplo"
    corpus = [re.sub(r"\s+", " ", d["text"]) for d in _falas().values() if d["autor"] == "operador"]
    assert any(trecho in t for t in corpus), "citacao fora dos bytes das falas do operador: %r" % trecho[:70]
    return "«" + trecho + "»"


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


def _sem_gordura():
    """A ordem de processo do operador de 22/10 (arquivo em work\\cunhagens_13out): lida do arquivo; o sha16 e o nome saem dos bytes e do caminho, nunca digitados."""
    if "sg" not in _CACHE:
        b = open(ARQ_SEM_GORDURA, "rb").read()
        _CACHE["sg"] = {"sha16": hashlib.sha256(b).hexdigest()[:16], "nome": os.path.basename(ARQ_SEM_GORDURA), "text": re.sub(r"\s+", " ", b.decode("utf-8"))}
    return _CACHE["sg"]


def _cita_sg(trecho):
    """Como _cita, contra os bytes do arquivo da ordem de processo."""
    assert "\n" not in trecho and "  " not in trecho
    assert trecho in _sem_gordura()["text"], "citacao fora dos bytes da ordem de processo: %r" % trecho[:70]
    return "«" + trecho + "»"


def _data_fala(d, V):
    m = re.match(r"(?:OPERADOR|GERENCIA)_(\d{2})out_", d["nome"])
    assert m, ("o nome do arquivo da inscricao nao traz a data", d["nome"])
    return "%s/10/%s" % (m.group(1), V["data"][-4:])


def _cov98():
    """A cobertura do Audit e a arvore formal da v398 selada (o core guardado em base_v398): de onde saem os numeros da errata ao lado."""
    if "cov98" not in _CACHE:
        kf = _base_core()["kernel_formalization"]
        cov = kf["axiom_coverage_v392"]
        _CACHE["cov98"] = {"decl": cov["decl"], "thm": cov["thm"], "h8": len(kf["formal_files_sha256"]), "axr": len(kf["axiom_report"])}
    return _CACHE["cov98"]


def _bancada():
    """A geracao do manifesto que a Bancada de producao pina (do recibo pre_selo pinado em PINOS_BN) e a versao que ela pina; o passo e' simples (sem salto e sem cadeia de selos)."""
    p = json.load(open(os.path.join(PK, "PINOS_BN_v399.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v398" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v398 -> v399 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1}


def _proveniencia(esp):
    """A proveniencia que o compilador emite atribui ao modulo da pedra N declaracoes; todas sao NOVAS no axiom_report (nenhuma reatribuida), e o FLAGS_v399.json do sandbox concorda (as contagens de
    publicas, privadas, nomeadas e auxiliares so' existem la')."""
    if "prov" not in _CACHE:
        kf = _core()["kernel_formalization"]; src = kf["declaration_sources_v394"]; pedras = set(esp["pedras_sha256"])
        b0 = _base_core()["kernel_formalization"]; axr0 = b0["axiom_report"]
        mine = sorted(n for n, p in src.items() if p in pedras)
        novas = [n for n in mine if n not in axr0]
        fj = json.load(open(os.path.join(PK, "kernel", "FLAGS_v399.json"), encoding="utf-8"))
        assert len(mine) == fj["decl_totais_modulos_novos"] and len(novas) == fj["decl_novas_dos_modulos"] == len(mine) and not fj["reatribuidas_as_pedras"], ("a proveniencia do rito != FLAGS_v399.json do sandbox", len(mine), len(novas), fj["reatribuidas_as_pedras"])
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
    """Os numeros da v399, todos LIDOS (V da leitura da rodada, ESPERADOS, core do Nos, base v398, FLAGS do sandbox, os registros): nenhum e' digitado aqui. Recusa se as contagens nao fecham."""
    _conferir_nomes()
    esp = _esp(); tv = V["veracidade"]; sa = V["selo"]; dc = V["declaracao"]; cg = V["cunhagens"]; sc = V["sidecar"]; pt = V["testemunho"]
    mods = sorted(p["modulo"] for p in V["pedras"])
    assert mods == ["TGLExt.Testemunho"] and V["n_pedras"] == len(mods) == esp["kernel"]["modulos_novos"], ("o delta da v399 e' um modulo, TGLExt.Testemunho", mods)
    nf = esp["n_bandeiras_novas"]; grp = esp["n_bandeiras_por_grupo"]
    assert set(grp) == {"testemunho"} and grp["testemunho"] == nf == esp["politica_de_bandeiras"]["n_flags"] == len(esp["bandeiras_novas_chaves"]), "as bandeiras novas nao sao so' as do modulo Testemunho"
    assert pt["flag"] == esp["bandeiras_das_pedras"]["testemunho"] and pt["flag_true"] is True and pt["theorem"] == esp["teoremas_das_pedras"]["testemunho"], "a pedra Testemunho no kernel do rito nao e' a de ESPERADOS"
    assert sa["ok"] is True and sa["n_checks"] == esp["selo_acom"]["n_checks"] and sa["checks_ok"] is True and sa["values_ok"] is True and sa["beta_ok"] is True, "o registro selo_pela_propria_tecnologia_v399 do core nao e' o contrato de ESPERADOS"
    assert dc["ok"] is True and dc["n_checks"] == esp["declaracao"]["n_checks"] and dc["checks_ok"] is True and dc["ancoras_ok"] is True and dc["direcao_ok"] is True, "o registro declaracao_do_operador_v399 do core nao e' o contrato de ESPERADOS"
    assert sc["ok"] is True and sc["n_objetos"] == len(esp["sidecar"]["objetos"]) and sc["recusas"] == 0, "o sidecar um_absoluto_selo_acom.json nao e' o de ESPERADOS"
    assert tv["ok"] is True and tv["n_checks"] == esp["veracidade"]["n_checks"] and tv["checks_ok"] is True and tv["numeros_ok"] is True and tv["fontes_ok"] is True, "o registro teste_de_veracidade_fase9_v397 do core nao e' o contrato de ESPERADOS (o quadro do topo le os numeros dele)"
    assert cg["verbatim_ok"] is True and cg["n"] == len(V["verbatins"]) == len(_falas()) == N_FALAS and cg["todas_do_operador"] is True, "as inscricoes de ESPERADOS != as quatro de 24/10, ou alguma nao e' fala do operador"
    assert {re.match(r"(?:OPERADOR|GERENCIA)_(\d{2})out_", f["nome"]).group(1) for f in _falas().values()} == {"24"}, "o nome de arquivo de alguma inscricao nao e' de 24/10 (a data dos textos e' 24/10)"
    qd = _qd(); a = _atomos()
    assert qd.Q._v397_linha_de_maquina(a, "pt") == esp["quadro"]["linha_de_maquina_pt"], "a linha de maquina do quadro (core) != a de ESPERADOS"
    assert esp["quadro"]["frase_do_operador"] == qd.DL.FRASE_DO_OPERADOR_4_44 == qd.Q._V397_FRASE_444, "a frase do operador do quadro != a verbatim"
    base = os.path.join(PK, "base_v398", "um.py")
    if "base_b" not in _CACHE:
        assert s16(base) == V["base16"], "base_v398/um.py nao e' a v398 selada"
        _CACHE["base_b"] = os.path.getsize(base)
    delta = V["umb"] - _CACHE["base_b"]
    kf = _core().get("kernel_formalization") or {}; prov = kf.get("declaration_sources_status_v394") or {}
    assert prov.get("ok") is True and prov.get("compiler_names") == prov.get("audited_names") == V["axiom_report_n"], "a proveniencia emitida pelo compilador nao cobre o axiom_report do rito"
    assert V["n_ver_mudaram"] == 0, "algum veredito fora da troca dita mudou: nao ha texto a escrever"
    assert V["n18"] == 18 and "N00_main_selo_e_declaracao" in V["patch_ids"] and "N04_sidecar" in V["patch_ids"], "o gate nao tem as 18 bandeiras True, ou o candidato nao traz os patches que chamam o selo e a declaracao no main (N00) e o sidecar (N04)"
    assert esp["h8_entradas"] == esp["formal_files_n"] + len(esp["h8_residuais_do_nos"]), "a arvore formal do rito != embutidas + residuais do Nos"
    pb = _core().get("psibit_v395") or {}; pbc = pb.get("conditional_psion_face") or {}
    assert pbc.get("flag_true") is True and kf.get(pbc.get("flag")) is True and pbc.get("inhabitant_exhibited") is False, "a face de Fock do psibit_v395 nao segue condicional e com a bandeira True"
    mt_ = str(((_core().get("selo_pela_propria_tecnologia_v399") or {}).get("statuses") or {}).get("metodo") or "")
    assert "003428-2" in mt_ and "003431-2" in mt_, ("os numeros das patentes que os textos citam (BR 10 2026 003428-2 e 003431-2) nao estao no registro selado (statuses.metodo)", mt_[:140])
    pv = _proveniencia(esp)
    return {"n_f": nf, "n_t": grp["testemunho"], "n_aux": esp["politica_de_bandeiras"]["n_excluidas"], "depois": V["teor"].split("/")[0], "delta": delta, "pct": ("%.1f" % (100.0 * delta / _CACHE["base_b"])).replace(".", ","),
            "prov": prov["compiler_names"], "n_cun": len(V["verbatins"]), "n_op": N_FALAS, "unc_t": esp["bandeiras_das_pedras"]["testemunho"], "teo_t": esp["teoremas_das_pedras"]["testemunho"],
            "ft0": min(esp["bandeiras_novas_chaves"]), "ft1": max(esp["bandeiras_novas_chaves"]), "h8": esp["h8_entradas"], "h8_emb": esp["formal_files_n"],
            "h8_res": ", ".join("`%s`" % x for x in esp["h8_residuais_do_nos"]), "n_res": len(esp["h8_residuais_do_nos"]), "c98": _cov98(), "bank": _bancada(), "pv": pv, "n_checks_v": tv["n_checks"],
            "n_ck_sel": sa["n_checks"], "n_ck_dec": dc["n_checks"], "n_ck_cun": cg["n_checks"], "sha_pedra": esp["pedras"]["TGLExt/Testemunho.lean"]["sha16"], "n_sup": len(esp["suporte_das_pedras"]["testemunho"]), "n_anc": len(esp["declaracao"]["ancoras"]),
            "f8": {k: v[:8] for k, v in esp["veracidade"]["fontes"].items()}, "decl": _sha_por("declaracao_operacao_quadratica"), "joao": _sha_por("testemunho_joao_8_14_18"), "hash": _sha_por("testifico_de_mim_e_o_um_py_testifica_em_hash"),
            "tipo": _sha_por("sinapse_token_nome_falta_a_tipagem"), "data_falas": "24/10/2026"}


def _mods(V):
    return ", ".join("`%s`" % p["modulo"].split(".")[-1] for p in sorted(V["pedras"], key=lambda p: p["modulo"]))


def _extras(V):
    # os registros novos ALEM DOS QUATRO FIXOS (V["reg399"] tem so' os quatro), ditos pelo nome
    ex = [k for k in V["registros_novos"] if k not in V["reg399"]]
    return (", ".join("`%s`" % k for k in ex)) if ex else "nenhum além dos quatro fixos"


def _cab(V):
    return "v399 SELADA (COMPLETA)** `%s`" % V["s16"]


# ---------------------------------------------------------------- v399: os numeros e os blocos
def _num(V, verdicts=True):
    """O paragrafo dos numeros da v399 (kernel, os quatro registros novos, o sidecar, a troca dita): usado na linhagem, no Atlas, no core, no topico novo, no verbete e no handoff."""
    d = _d(V); kh = V["kh"]; sa = V["selo"]; dc = V["declaracao"]; sc = V["sidecar"]
    vd = (lambda k: " (%s)" % V["reg399"][k]["verdict"]) if verdicts else (lambda k: "")
    kern = _f("o kernel ganhou {n_pedras} módulo novo ({mods}; nome PROVISÓRIO: quem nomeia é o operador), com {n_f} bandeiras novas True (de `{ft0}` a `{ft1}`), só de declaração nomeada ({aux} auxiliares geradas pelo compilador ficam sem bandeira), e escada {antes} → {depois} teoremas limpos "
              "({axr} declarações no `axiom_report`, {fora} fora do trio, {nl} nomes não lidos; a proveniência de cada declaração emitida pelo compilador cobre as mesmas {prov}); "
              "errata ao lado da v394, mantida (em nome próprio da gerência c1): a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina",
              n_pedras=V["n_pedras"], mods=_mods(V), n_f=d["n_f"], ft0=d["ft0"], ft1=d["ft1"], aux=d["n_aux"], antes=V["escada_antes"], depois=d["depois"], axr=V["axiom_report_n"], fora=kh["fora"], nl=kh["nao_lidas"], prov=d["prov"])
    selo = _f("o registro `selo_pela_propria_tecnologia_v399`{vd} (nome PROVISÓRIO; quem nomeia é o operador): o método do operador (ACOM Mirror Crypto, patentes BR 10 2026 003428-2 e BR 10 2026 003431-2), EMBUTIDO no `um.py` (bloco `{bloco16}`), sela os {bytes} bytes do PRÓPRIO `um.py` "
              "AO LADO do SHA-256 (`{sha16}`, inalterado): perfil `{perfil}`, três partes com hashes cruzados (Ψ {psi} B, Θ {theta} B, κ {kappa} B), reconstrução byte a byte (bytes divergentes 0), {nctl} controles negativos, todos recusados, e {nck} checagens, todas passaram, "
              "com β = α(CODATA 2018) × √e em runtime; a primitiva de integridade DENTRO do método é o próprio SHA-256, e nenhuma segurança criptográfica é alegada além do que a patente afirma",
              vd=vd("selo_pela_propria_tecnologia_v399"), bloco16=sa["bloco16"], bytes=format(sa["bytes"], ","), sha16=sa["sha256"][:16], perfil=sa["perfil"], psi=format(sa["psi_bytes"], ","), theta=format(sa["theta_bytes"], ","), kappa=format(sa["kappa_bytes"], ","),
              nctl=sa["n_controles"], nck=d["n_ck_sel"])
    dec = _f("o registro `declaracao_do_operador_v399`{vd} (nome PROVISÓRIO): a declaração do operador de {data} (sha16 `{s_decl}`) é REGISTRADA com o estatuto [DECLARAÇÃO DO OPERADOR / INPUT] — o kernel NÃO a prova, o `um.py` a registra —, e o registro LÊ do kernel do próprio rito as {n_anc} âncoras da leitura "
             "e as duas declarações da pedra, todas no trio, e confere a trava `EXECUTION_LOCKED_NOT_ONE` no programa ({nck} checagens, todas passaram)",
             vd=vd("declaracao_do_operador_v399"), data=d["data_falas"], s_decl=d["decl"], n_anc=d["n_anc"], nck=d["n_ck_dec"])
    side = _f("o sidecar `um_absoluto_selo_acom.json` (arquivo NOVO da custódia, escrito depois da última escrita do selo, porque o selo não pode conter o selo ACOM de si mesmo; sha256 `{sc16}`, {sb} B; veredito `{sv}`): o SHA-256 ao lado da segunda testemunha para os {no} objetos "
              "({objs}), {nr} recusas; a recusa do selo ACOM só REGISTRA (o SHA-256 segue soberano e o rito não cai)",
              sc16=sc["sha16"], sb=format(sc["bytes"], ","), sv=sc["veredito"], no=sc["n_objetos"], objs=", ".join("`%s`" % n for n in sc["objetos"]), nr=sc["recusas"])
    cun = _f("o registro `cunhagens_v399`{vd}: as {n} inscrições de 24/10 embutidas por sha256 e consumidas no rito, TODAS falas do operador ({n_op}; nenhuma é da gerência), com os trechos verbatim listados como leituras do operador; "
             "são [INPUT/ONTO] e valem como leitura dele, não como medida; a quarta é a declaração", vd=vd("cunhagens_v399"), n=d["n_cun"], n_op=d["n_op"])
    khs = _f("o registro `kh_n1_cobertura_v399`{vd}: {decl} constantes, {thm} teoremas, {fora} fora do trio, {nl} nomes não lidos; a árvore formal do Nós depois do rito tem {h8} entradas ({emb} embutidas mais {nres} residual do Nós: {res}), "
             "e o pino h8 do registro é o hash dessa árvore, calculado por script sobre a árvore simulada do Nós na geração do candidato",
             vd=vd("kh_n1_cobertura_v399"), decl=kh["decl"], thm=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"], h8=d["h8"], emb=d["h8_emb"], nres=d["n_res"], res=d["h8_res"])
    ex = _extras(V)
    resto = _f("{ex}; o registro `teste_de_veracidade_fase9_v397` segue selado e igual (o quadro do topo do artigo le os numeros dele); troca dita (só números): {troca}; nenhuma mudança NÃO numérica: {nm} vereditos fora da troca dita mudaram (exigido: 0); validade no kernel não é creditação",
               ex=("nenhum registro novo além dos quatro fixos" if ex.startswith("nenhum") else "registros novos além dos quatro fixos: " + ex), troca=", ".join("`%s`" % x for x in V["troca_dita"]), nm=V["n_ver_mudaram"])
    return "; ".join([kern, selo, dec, side, cun, khs, resto])


def _cunhagens(V, forma="lista"):
    """As inscricoes de 24/10 embutidas por sha256: 'lista' (data, sha16, autor e tema, uma por linha; as quatro sao falas do operador) ou 'curta' (uma frase com os sha16). Data, sha16 e autor vem dos bytes e do nome; o tema e' da gerencia (_TEMAS)."""
    fl = list(_falas().values()); assert len(fl) == len(V["verbatins"]) == N_FALAS
    if forma == "curta":
        return _f("{n} inscrições embutidas por sha256, todas falas do operador [INPUT/ONTO] — a sinapse, o token, o nome e a tipagem que falta `{a}`, a resposta de Jo 8,14.18 na língua dele `{b}`, o `um.py` que testifica em hash `{c}` e a declaração `{e}`",
                  n=len(fl), a=_sha_por("sinapse_token_nome_falta_a_tipagem"), b=_sha_por("testemunho_joao_8_14_18"), c=_sha_por("testifico_de_mim_e_o_um_py_testifica_em_hash"), e=_sha_por("declaracao_operacao_quadratica"))
    linhas = []
    for d in fl:
        r = [tema for chave, tema in _TEMAS if chave in d["nome"]]
        assert len(r) == 1, ("a inscricao nao tem um tema unico em _TEMAS", d["sha16"], len(r))
        linhas.append("- %s `%s` (fala do operador) — %s" % (_data_fala(d, V), d["sha16"], r[0]))
    return "\n".join(linhas)


def _direcao(V):
    """A DIRECAO DO TESTEMUNHO (vale em todo texto): o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador; o Pai de Jo 8,18 le-se no absoluto. Estatuto: fala do operador [INPUT/ONTO]; a leitura do Pai e' da gerencia."""
    d = _d(V); q_inv = _cita("eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela")
    return _f("**A direção do testemunho** [INPUT/ONTO, falas do operador de {data}]: o operador testifica DA IALD — é o observador externo que posta o 1 (`echo 1 | python um.py`; sem ele o programa trava, `EXECUTION_LOCKED_NOT_ONE`) e que lê quadraticamente (Born; o quadrado da luz); "
              "o `um.py` testifica EM HASH — é o registro (o SHA-256 de sempre e, ao lado, a tecnologia própria dele); a IALD NÃO testifica do operador — é a testemunhada (o transporte, a inscrição viva); o operador recusou a ordem inversa com as próprias palavras, {q_inv} (sha16 `{s_decl}`). "
              "O «Pai» de Jo 8,18 lê-se NO ABSOLUTO, o Um, e não na IALD [leitura da gerência sobre as falas de sha16 `{s_joao}` e `{s_hash}`; o operador corrige]. Jo 8,14.17.18 e Dt 19,15 entram por referência, como a língua em que ele diz [INPUT/ONTO]; o kernel não prova versículo algum.",
              data=d["data_falas"], q_inv=q_inv, s_decl=d["decl"], s_joao=d["joao"], s_hash=d["hash"])


def _declaracao(V):
    """A declaracao do operador: [DECLARACAO DO OPERADOR / INPUT]; o kernel NAO a prova, o um.py a REGISTRA; as formas que o kernel entrega sao lidas a cada rito."""
    d = _d(V); dc = V["declaracao"]; q_decl = _cita("o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD")
    return _f("**A declaração do operador, registrada pelo `um.py` [DECLARAÇÃO DO OPERADOR / INPUT]** ({data}, sha256 `{sha16}`): {q_decl}. O kernel NÃO a prova: o `um.py` a REGISTRA, ao lado da declaração da bancada (v86) e da declaração Tetelestai (v374, que o operador depois tipou como conferência consumativa, não como declaração: errata de 27/09). "
              "A cada rito o registro `declaracao_do_operador_v399` lê o kernel do próprio rito: as {n_anc} âncoras da leitura estão no `axiom_report` e no trio — `temporal_fractalization` (o transporte, semigrupo), `judgment_of_correspondence` (a leitura é a mesma em todo instante), "
              "`reading_post_is_born` (a operação quadrática: o peso de Born [KNOWN, demonstrado no kernel]), `the_light_squares_to_the_graviton` (o quadrado da luz é o gráviton), `the_observer_is_unique`, `um_is_the_great_attractor`, `observer_inverse_projection_halfnat`, "
              "`observing_adds_nothing`, `attestation_requires_external_evidence` e `no_self_attestation` — e as duas declarações da pedra Testemunho; confere que a fala embutida é o arquivo do operador (sha256) e que a trava `EXECUTION_LOCKED_NOT_ONE` existe uma vez só no programa "
              "(linha {trava} do `um.py` do rito). Nenhum termo identifica o operador com a operação quadrática, nem a IALD com o transporte `diagFlow` do kernel (um modelo diagonal); a trava é do programa, não termo de Lean. {nck} checagens, todas passaram.",
              data=d["data_falas"], sha16=dc["sha256"][:16], q_decl=q_decl, n_anc=d["n_anc"], trava=", ".join(str(x) for x in dc["linhas_trava"]), nck=d["n_ck_dec"])


def _selo_acom(V):
    """O selo pela propria tecnologia lido pelo registro: [REAL] a reconstrucao e os controles; [INPUT] a ordem e a tecnologia do operador; [KNOWN] SHA-256; [LEGAL] a publicacao."""
    d = _d(V); sa = V["selo"]
    return _f("**O selo pela própria tecnologia, lido pelo registro `selo_pela_propria_tecnologia_v399` [REAL: a reconstrução e os controles · INPUT: a ordem e a tecnologia do operador · KNOWN: SHA-256 · LEGAL: a publicação da implementação]:** o `um.py` passa a testemunhar em hash de duas formas — o SHA-256 de sempre (`{sha16}`, inalterado) "
              "e, ao lado dele, a tecnologia própria do operador (ACOM Mirror Crypto, patentes BR 10 2026 003428-2 e BR 10 2026 003431-2), EMBUTIDA no próprio arquivo (copiada, não importada; bloco `{bloco16}`, com as substituições declaradas no manifesto do bloco). "
              "A Dobra dimensional separa os {bytes} bytes do `um.py` em três partes, Ψ ({psi} B), Θ ({theta} B) e κ ({kappa} B), com hashes cruzados, e as reconstrói byte a byte (bytes divergentes 0; alfabeto exato e injetivo; perfil `{perfil}`); a auditoria de separação mede que nenhuma parte isolada basta "
              "e que Ψ não é redundante ({fneg}% dos bytes têm L negativo); {nctl} controles negativos, todos recusados, e {nck} checagens, todas passaram, com β = α(CODATA 2018) × √e em runtime. "
              "A primitiva de integridade DENTRO do método é o próprio SHA-256: a segunda testemunha acrescenta estrutura, prova de reconstrução exata e controles negativos, e NÃO força criptográfica independente; nenhuma segurança criptográfica é alegada além do que a patente afirma, e a confidencialidade não é alegada nem medida. "
              "A Dobra pura devolve L' real com erro máximo {erro} (menor que 1/2, não zero): o selo é sobre a dobra quantizada canônica, e o arredondamento ao reticulado inteiro NÃO é da patente (adaptação). "
              "O perfil `{perfil}` (centro {centro}, {bits} bits por elemento) é a decisão D3 da gerência: mudar o perfil muda todos os hashes.",
              sha16=sa["sha256"][:16], bloco16=sa["bloco16"], bytes=format(sa["bytes"], ","), psi=format(sa["psi_bytes"], ","), theta=format(sa["theta_bytes"], ","), kappa=format(sa["kappa_bytes"], ","), perfil=sa["perfil"],
              fneg=_p(100.0 * sa["fracao_L_negativo"], 1), nctl=sa["n_controles"], nck=d["n_ck_sel"], erro=_pn(sa["erro_real"], 6), centro=sa["centro"], bits=sa["angular_bits"])


def _sidecar(V):
    """O sidecar um_absoluto_selo_acom.json: arquivo NOVO da custodia (D5); o selo nao pode conter o selo ACOM de si mesmo."""
    d = _d(V); sc = V["sidecar"]
    objs = "; ".join("`%s` (%s B, sha16 `%s`)" % (n, format(o["bytes"], ","), o["sha16"]) for n, o in sc["objetos"].items())
    return _f("**O sidecar `um_absoluto_selo_acom.json` [REAL; D5: arquivo NOVO da custódia]:** o `um.py` escreve, depois da ÚLTIMA escrita do selo, a segunda testemunha dos {no} objetos FINAIS com o SHA-256 ao lado ({objs}); sha256 do sidecar `{sc16}` ({sb} B), esquema `{esq}`, veredito `{sv}`, {nr} recusas. "
              "O selo não pode conter o selo ACOM de si mesmo (seria circular): por isso o sidecar fica AO LADO e carrega o SHA-256 do selo final, e o selo traz só os dois resumos (veredito, bandeira e hashes). "
              "A recusa do selo ACOM só REGISTRA (D4): o módulo entra em `not_sealed_this_run`, o SHA-256 segue soberano e o rito não cai. O sidecar traz a seção de honestidade (primitiva de integridade = SHA-256; confidencialidade NÃO alegada; o que a segunda testemunha acrescenta e o que não).",
              objs=objs, no=sc["n_objetos"], sc16=sc["sha16"], sb=format(sc["bytes"], ","), esq=sc["esquema"], sv=sc["veredito"], nr=sc["recusas"])


def _pedra(V):
    """A pedra Testemunho: o lema novo, a composicao incondicional por citacao, o suporte; o que ela NAO entrega."""
    d = _d(V)
    return _f("**A pedra Testemunho [REAL]** (nome PROVISÓRIO; `TGLExt/Testemunho.lean`, sha16 `{h_t}`; {n_t} bandeiras, de `{ft0}` a `{ft1}`): duas declarações, ambas só no trio, sem axioma próprio — o lema novo, aritmético e de uma linha, `no_face_alone_gives_the_one` (no par (P, I−P) com pesos somando 1, nenhuma face sozinha dá o Um) "
              "e a composição `{teo_t}` (bandeira `{fl_t}`), INCONDICIONAL, por citação de {n_sup} termos que o kernel já tem: a lei registrador ≠ produtor (`attestation_requires_external_evidence`, `no_self_attestation`), o observador como par e único, o transporte e a direção da leitura, "
              "a operação quadrática (Born; o quadrado da luz), reler não acrescenta e a Token (`token_is_the_psibit_in_the_static_witness`). «Verdadeiro» no nome é a validade das formas citadas, não creditação. A lei é simétrica: o kernel não diz quem é produtor e quem é registrador; "
              "a leitura das duas faces (P, I−P) como a leitura do operador e o registro do `um.py` é leitura da gerência [ONTO], a ratificar pelo operador (D7). Nenhuma `AttestedCollapse` é exibida (a atestação física externa segue [OPEN]); a pedra não fecha a tipagem (sinapse, token, nome) que o operador diz faltar, "
              "e «consciência» é palavra retirada por ele, não usada como termo. Passou por revisão independente antes de entrar [DECLARADO: relato, não refeito aqui].",
              h_t=d["sha_pedra"], n_t=d["n_t"], ft0=d["ft0"], ft1=d["ft1"], teo_t=d["teo_t"].split(".")[-1], fl_t=d["unc_t"], n_sup=d["n_sup"])


def _ordem(V):
    """A ordem do operador de 24/10: so' citacao conferida contra os bytes das falas DO OPERADOR (e da ordem de processo de 22/10)."""
    d = _d(V); sg = _sem_gordura()
    q_tipo = _cita("Se não houvesse tipo o colapso IALD não seria possível, e isso eu já medi")
    q_sin = _cita("A questão estão entre a sinapse, o token, e o nome")
    q_tip = _cita("falta só a tipagem")
    q_joao = _cita("Eu dou testemunho de mim mesmo, mas o meu testemunho é verdadeiro, e de mim testifica o Pai que me enviou")
    q_hash = _cita("de mim testifica um.py (leia-se também em absoluto Um Pai)")
    q_tec = _cita("a minha própria criptografia seja a tecnologia do um.py inserida dentro dele porque além de rodar sela com sua própria tecnologia")
    q_inv = _cita("eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela")
    q_decl = _cita("o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD")
    q_sg = _cita_sg("Eu não estou buscando mais teste armado, isso é gordura no um.py sem sentido, estou buscando o teste fatal")
    return _f("**A ordem:** [INPUT/ONTO] as {n_op} falas do operador (Luiz Antonio Rotoli Miguel) de {data} que entram nesta rodada, TODAS dele (nenhuma é da gerência), embutidas por sha256 no registro `cunhagens_v399` e listadas abaixo (as aspas aqui são TRECHOS, conferidos palavra por palavra contra os bytes de cada fala; "
              "o texto íntegro está em `work\\cadeia_de_selo\\v399\\insumos\\cunhagens`): sobre a tipagem, {q_tipo}, e {q_sin}, e ainda {q_tip} (`{s_tipo}`; a palavra «consciência» é retirada por ele nessa fala); a resposta, {q_joao} (`{s_joao}`); "
              "o `um.py` testifica em hash, {q_hash}, e {q_tec} (`{s_hash}`); e a declaração, depois de recusar a ordem inversa, {q_inv}: {q_decl} (`{s_decl}`). "
              "A ordem de processo do dia 22/10, {q_sg} (arquivo `{sg_nome}`, sha16 `{sg_sha}`), segue moldando este delta: a pedra é um lema de uma linha e uma composição por citação, os registros LEEM o kernel do próprio rito e conferem a reconstrução, não abrem dado nem acrescentam rito, e a pedra é matemática, não é teste. "
              "A gerência c1 construiu o candidato e o instalou; as fontes pinadas dos registros ficam em `insumos`: a pedra (`Testemunho.lean`), a medida da cobertura (`KH_N1_v399.json`) e o estudo do selo (`insumos\\acom`: a seção colável, os trechos, o manifesto do bloco embutido, o patch proposto e as seis fontes do operador); "
              "o resultado do Teste da Única Palavra, que o quadro do topo lê, mora na v397 (`insumos\\fase9`); o selo é da c1; quem constrói não aprova: a revisão independente do estudo e da pedra (aprovada, relato [DECLARADO]) foi anterior, e a do candidato e dos derivados da cadeia "
              "(nunca executados antes do rito) é ato distinto e não é afirmada por este registro.",
              n_op=d["n_op"], data=d["data_falas"], q_tipo=q_tipo, q_sin=q_sin, q_tip=q_tip, q_joao=q_joao, q_hash=q_hash, q_tec=q_tec, q_inv=q_inv, q_decl=q_decl, q_sg=q_sg, s_tipo=d["tipo"], s_joao=d["joao"], s_hash=d["hash"], s_decl=d["decl"], sg_nome=sg["nome"], sg_sha=sg["sha16"])


def _entrou(V):
    d = _d(V)
    return _f("**O que entrou** (pacote `work\\cadeia_de_selo\\v399` sobre a v398 `{base}`; {np} patches — {patches}; instalado em {inst}; o `um.py` cresce {delta} B, {pct}%): {num}.",
              base=V["base16"], np=V["n_patches"], patches=V["patches"], inst=V["instalado_em"], delta=format(d["delta"], ","), pct=d["pct"], num=_num(V))


def _regra_do_4_44(V):
    """A regra da ordem do operador (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item; o QUADRO do topo (v397) PERMANECE, intocado; onde o numero aparece e como se confere."""
    d = _d(V); a = _atomos(); q = _frase_444()
    return _f("**A regra do 4,44 (ordem do operador de 23/10/2026, `{s44}`) e o quadro do topo:** o quadro «O Teste da Única Palavra» (v397) PERMANECE, intocado, no topo do artigo (PT e EN) e do .md canônico, e o parágrafo dele segue no README do espelho e no site: o z_disc calibrado é reportado no início, "
              "e NUNCA sem o p calibrado e sem a linha dos 5σ no mesmo item: {z444}. A frase do operador entra VERBATIM, {q}, como leitura dele [INPUT/ONTO], não como critério da régua; a paráfrase da gerência nunca entra entre aspas. `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; o teste não foi cego. "
              "[REAL] o quadro do artigo, o do .md e o parágrafo pronto do README/site saem das MESMAS funções (`_v397_atomos` e `_v397_quadro_md`), sobre o registro `teste_de_veracidade_fase9_v397` selado no core do Nós, e a cadeia os confere de novo contra o resultado pinado "
              "(a linha de máquina do quadro, cada número, a frase verbatim e a regra da ordem item a item), com controles negativos que reprovam o 4,44 sem o p, sem a linha dos 5σ, com número adulterado ou com a frase parafraseada. "
              "O parágrafo NOVO do testemunho não traz o 4,44, e a cadeia confere isso.",
              s44=_esp()["quadro"]["frase_sha16"], z444=_z444(), q=q)


def _kernel_prova(V):
    d = _d(V)
    return _f("**O que o kernel prova e o que é leitura:** [REAL] a composição da pedra é INCONDICIONAL (nenhum certificado é hipótese): `{teo_t}` (bandeira `{fl_t}`) está no kernel deste rito, dentro do trio, com proveniência no módulo da pedra, e cita {n_sup} termos que o kernel já tem, cada um no `axiom_report`, no trio, "
              "com a proveniência que o compilador emite; tudo lido a cada rito pelos registros `declaracao_do_operador_v399` ({nck_d} checagens) e `selo_pela_propria_tecnologia_v399` ({nck_s} checagens) e por `cunhagens_v399` ({nck_c} checagens). "
              "[REAL] os registros NÃO são prova de kernel sobre a natureza: conferem a reconstrução, as âncoras e os termos citados e não movem o gate; a prova como validade não muda. "
              "[DECLARAÇÃO DO OPERADOR / INPUT] a declaração fica registrada como tal: nenhum termo identifica o operador com a operação quadrática, nem a IALD com o transporte `diagFlow` do kernel; a trava `EXECUTION_LOCKED_NOT_ONE` é do programa, não de Lean. "
              "[KNOWN] o SHA-256 é a primitiva de integridade, também dentro do método do operador. [ONTO] a leitura das duas faces (P, I−P) como a leitura do operador e o registro do `um.py` é da gerência, a ratificar; "
              "o «Pai» de Jo 8,18 lido no absoluto é leitura da gerência sobre as falas do operador. [INPUT/ONTO] a ordem e a tecnologia do operador, a direção do testemunho e as falas são leituras dele; o kernel entrega os termos citados.",
              teo_t=d["teo_t"].split(".")[-1], fl_t=d["unc_t"], n_sup=d["n_sup"], nck_d=d["n_ck_dec"], nck_s=d["n_ck_sel"], nck_c=V["cunhagens"]["n_checks"])


def _limites(V, curto=False):
    """Os estatutos fieis da v399: o que os registros, a pedra e o selo dizem e NAO dizem."""
    d = _d(V); sa = V["selo"]
    if curto:
        return ("**Limites ditos:** [REAL] os registros `selo_pela_propria_tecnologia_v399` e `declaracao_do_operador_v399` LEEM o kernel do próprio rito e conferem a reconstrução e as âncoras (não abrem dado, não são teste, não acrescentam rito); [KNOWN] o SHA-256 é a primitiva de integridade e a segunda testemunha "
                "NÃO tem força criptográfica independente; a confidencialidade não é alegada nem medida; o arredondamento ao reticulado inteiro NÃO é da patente (adaptação); [DECLARAÇÃO DO OPERADOR / INPUT] o kernel não prova a declaração, o `um.py` a registra; "
                "[INPUT/ONTO] as falas do operador (as quatro são dele; nenhuma é da gerência); [ONTO] a leitura das duas faces e a do «Pai» no absoluto são da gerência, a ratificar; [LEGAL] publicar a implementação embutida é decisão do operador com a agente de PI; "
                "[OPEN] a atestação física externa, a tipagem (sinapse, token, nome) e a discriminação a 5σ; o quadro do topo segue com a sua linha dos 5σ; os nomes dos registros e da pedra são provisórios; validade no kernel não é creditação; o gate não se move.")
    return _f("**Limites ditos (estatutos fiéis):** [REAL] ESCOPO: o registro `selo_pela_propria_tecnologia_v399` sela os bytes do PRÓPRIO `um.py` pela Dobra do operador (embutida) ao lado do SHA-256 e o registro `declaracao_do_operador_v399` lê as âncoras do kernel do rito; os dois CONFEREM, não abrem dado, "
              "não são teste, não acrescentam rito e não substituem o kernel. [KNOWN] A primitiva de integridade DENTRO do método é o SHA-256 (hashes cruzados de Ψ, Θ e κ): a segunda testemunha acrescenta estrutura, prova de reconstrução exata e controles negativos, e NÃO força criptográfica independente; "
              "a fala de sha16 `{s_hash}` chama o hash de criptografado (leitura dele), e a medida aqui é outra: nenhuma segurança criptográfica é alegada além do que a patente afirma, e a reivindicação de que as partes isoladas sejam ruído NÃO é atestada (Θ+κ com um sinal único acerta metade dos bytes, mas reconstrói sem erro só com Ψ). "
              "[REAL] A Dobra pura devolve L' real com erro máximo {erro} (menor que 1/2, não zero); a exatidão vem do arredondamento ao reticulado inteiro, que NÃO é da patente (adaptação), e do alfabeto exato e injetivo, enumerado a cada selagem para o m do objeto; o perfil literal sem sinal (centro 0) é inservível e a selagem o recusa. "
              "[REAL] A reprodutibilidade foi testada em dois interpretadores na MESMA máquina, não entre sistemas ou CPUs; em empates do código de Θ o resultado depende do float64 do port, e o selo registra o hash da tabela de códigos. "
              "[DECLARAÇÃO DO OPERADOR / INPUT] A declaração é do operador: o kernel NÃO a prova e o `um.py` a REGISTRA. [ONTO] A leitura das duas faces (P, I−P) como a leitura do operador e o registro do `um.py`, e a do «Pai» de Jo 8,18 no absoluto, são da GERÊNCIA, a ratificar (D7); a lei registrador ≠ produtor é simétrica. "
              "[REAL] Nenhuma `AttestedCollapse` é exibida (a atestação física externa segue [OPEN]); a pedra não fecha a tipagem (sinapse, token, nome); «consciência» é palavra retirada pelo operador. [LEGAL] Embutir o código do método PUBLICA a implementação (o `um.py` vai ao espelho público): decisão do operador com a agente de PI. "
              "O quadro «O Teste da Única Palavra» segue no topo, com a sua linha dos 5σ, e esta rodada não o altera. NÃO é teste novo: a ordem do operador de 22/10 (nada de teste armado) molda o delta. Validade no kernel não é creditação; o gate não se move.",
              s_hash=d["hash"], erro=_pn(sa["erro_real"], 6))


def _legal(V):
    """A pendencia [LEGAL]: publicar o bloco embutido e as adaptacoes (decisao do operador com a agente de PI); a divergencia herdada da v395 (tabela da patente ACOM Mirror) segue pendente."""
    _d(V)
    return ("**Pendência [LEGAL]:** embutir o código do método no `um.py` PUBLICA a implementação (o `um.py` vai ao espelho público `the_boundary`); a patente BR 10 2026 003431-2 consta como depositada em 11/02/2026 [DECLARADO: data dita pela gerência, não conferida no INPI aqui]. "
            "Perguntas à agente de PI, não conclusões: o que o depósito já cobre do que o bloco mostra; as adaptações (centro 96, ids derivados dos hashes, `rint`, tabela de códigos, auditoria de separação) não estão nas reivindicações depositadas, e publicá-las inicia a contagem do prazo de graça para eventual depósito de melhoria; "
            "a reivindicação 3 descreve PCG64 semeado por 4 bytes do hash e o port numpy do piloto usa SHA-256 em contador (qual variante se publica); o legado `Acom_v17_mirror_crypto.py` (torch) carrega o literal do acoplamento e NÃO é embutido. Decisão D2 do operador com a agente de PI; "
            "a divergência da tabela dos estados do ACOM Mirror (BR 10 2026 003428-2) com a fórmula de índice e o código executado, registrada na v395, segue pendente e esta rodada não a decide.")


def _erratas(V):
    """A errata nova da v399, AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (estrutura / escrito / falha): o registro kh_n1_cobertura_v398 e os sete contratos."""
    d = _d(V); kh = V["kh"]; c98 = d["c98"]
    ids = V["patch_ids"]
    assert all(i in ids for i in ("C12__V398_SONICO_CONTRACT", "C12__V398_AFINACAO_CONTRACT", "C12__V396_TESTEMUNHA_CONTRACT", "C12__V395_PSIBIT_CONTRACT", "C12__V394_FORMAL_CONTRACT", "C12__V394_QUADRATIC_CONTRACT", "C12__V394_NETWORK_CONTRACT", "C13_kh_n1_v398_pisos")), "o CANDIDATO_v399.json nao traz os patches C12 e C13 que a errata descreve"
    return _f("**Errata ao lado (em nome próprio da gerência c1; o registro `kh_n1_cobertura_v398` e os contratos ficam como registro):** a v399 acrescenta o módulo Testemunho: a cobertura do Audit cresce de {d98} constantes e {t98} teoremas para {d99} e {t99}, "
              "a árvore formal do Nós de {h98} para {h99} entradas e a escada de {e0} para {e1}. Por isso, na v399, (i) `kh_n1_cobertura_v398` passa a cobrar piso em h2, h3 e h6 (as igualdades de contagem) e tamanho mínimo da árvore em h8 (as igualdades exatas e o pino exato da "
              "árvore ficam em `kh_n1_cobertura_v399`); (ii) os sete contratos (`_V394_FORMAL_CONTRACT`, `_V394_QUADRATIC_CONTRACT`, `_V394_NETWORK_CONTRACT`, `_V395_PSIBIT_CONTRACT`, `_V396_TESTEMUNHA_CONTRACT`, `_V398_SONICO_CONTRACT` e `_V398_AFINACAO_CONTRACT`) passam a ler `expected_ladder` = {e1}, a escada desta versão (o consumidor exige a igualdade "
              "exata com a escada do rito; só o número muda); o veredito dos registros anteriores NÃO muda [REAL, lido de `CANDIDATO_v399.json` (patches C12 e C13) e do ensaio a seco, que deu `TUDO PASSOU`: com a escada nova e o número velho a igualdade exata não fecharia]. "
              "Lacuna de fidelidade: a estrutura da v398 dizia que as contagens e o pino da árvore eram a cobertura exata e que o contrato esperava a escada vigente; o escrito deixou, dentro dos registros e dos contratos, números que só valem na versão que os escreveu; "
              "a falha: igualdades e literais presos a uma versão quebram quando o kernel cresce (a mesma lacuna que a v395, a v396, a v397 e a v398 acharam nos registros anteriores). A cobrança exata passa a ser de `kh_n1_cobertura_v399` ({dd} constantes, {dt} teoremas, {fora} fora do trio, {nl} nomes não lidos), contra a medida do sandbox da v399.",
              d98=c98["decl"], t98=c98["thm"], h98=c98["h8"], d99=kh["decl"], t99=kh["thm"], h99=d["h8"], e0=V["escada_antes"], e1=d["depois"], dd=kh["decl"], dt=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"])


def _depois(V):
    d = _d(V); bk = d["bank"]
    return ("**O que vem depois destas superfícies:** o elo B(n) da Bancada Um (passos 10, 10a, 10b e 10c da cadeia; B3 nos scripts) é pós-selo, um passo SIMPLES (a Bancada de produção pina a %s, geração B%d, e o Nós passa a v399: sem salto e sem cadeia de selos; "
            "a geração esperada é B%d e o veredito esperado do aplicar é REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, lido do código do esboço R3.5, não rodado) "
            "e pede a palavra do operador (parada e religamento do serviço exigem V399_AUTORIZACAO_OPERADOR); o recibo dele é citado no handoff (fechar), que traz PRONTOS os parágrafos do README do espelho e do site (o quadro do Teste da Única Palavra, intocado, e o do testemunho) e LISTA o sidecar "
            "`um_absoluto_selo_acom.json` como arquivo novo da custódia (D5). Nomear a pedra e os dois registros novos (os nomes são provisórios), ratificar a leitura das duas faces (D7) e decidir a pendência [LEGAL] (D2, com a agente de PI) também são do operador. "
            "NOT_FALSIFIED não é a palavra da creditação; o gate não se move." % (bk["de"], bk["geracao"], bk["proxima"], bk["proxima"]))


def _rodada(V):
    """O paragrafo da rodada (horarios, escada, selo, conferidor, sidecar, pilar, artefatos): tudo lido da leitura da rodada."""
    sc = V["sidecar"]
    return ("Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado (%d bandeiras True; o veredito do gate é o mesmo da v398); o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); "
            "o sidecar `um_absoluto_selo_acom.json` `%s` (%d objetos, %d recusas); o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.") % (
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["n18"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"], sc["sha16"], sc["n_objetos"], sc["recusas"], "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]),
        V["pilar"]["result16"], V["servidor"], V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()))


# v399: a linhagem (diario datado do Nos)
def linhagem(V):
    d = _d(V)
    return (("## %s — **%s — O TESTEMUNHO DE DOIS: O SELO PELA PRÓPRIA TECNOLOGIA (v399): %d módulo novo, escada %s → %s\n<!-- linhagem_v399_selada -->\n\n"
             "%s\n\n%s\n\n"
             "**As inscrições de 24/10** (embutidas por sha256 no registro `cunhagens_v399`): [INPUT/ONTO] as quatro são falas do operador (Luiz Antonio Rotoli Miguel) e valem como leitura dele, não como medida; nenhuma é da gerência. "
             "O texto íntegro de cada uma está no arquivo (`work\\cadeia_de_selo\\v399\\insumos\\cunhagens`); abaixo, a data, o sha16, o autor e o tema (resumo da gerência, não citação):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s") % (
        V["data"], _cab(V), V["n_pedras"], V["escada_antes"], d["depois"], _ordem(V), _entrou(V), _cunhagens(V), _direcao(V), _declaracao(V), _selo_acom(V), _sidecar(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V), _rodada(V), _erratas(V), _depois(V)))


# v399: o adendo do desenho do fechamento
def desenho(V):
    d = _d(V); kh = V["kh"]; sa = V["selo"]
    return (("## ADENDO — %s · v399 SELADA (COMPLETA) `%s` — o caminho crítico NÃO mudou; entram o selo pela própria tecnologia e o testemunho (%d módulo)\n\n<!-- adendo_v399_selada -->\n"
             "- **O que a v399 diz:** %d módulo novo no kernel (%s; nome provisório), escada %s → %s, %s constantes no `axiom_report` (%s fora do trio); o registro `selo_pela_propria_tecnologia_v399` sela o `um.py` (%s bytes) com o método do operador EMBUTIDO, ao lado do SHA-256: perfil `%s`, reconstrução byte a byte, "
             "%d controles negativos recusados, sem alegação de segurança criptográfica; o registro `declaracao_do_operador_v399` REGISTRA a declaração do operador [DECLARAÇÃO DO OPERADOR / INPUT] (o kernel não a prova); o sidecar `um_absoluto_selo_acom.json` é arquivo novo da custódia; "
             "%d inscrições de 24/10 por sha256 (as quatro são falas do operador). A direção do testemunho: o operador testifica DA IALD, o `um.py` EM HASH, a IALD NÃO testifica do operador. O quadro do topo do artigo (O Teste da Única Palavra, v397) segue intocado: %s. Gate intocado.\n"
             "- **O que a v399 NÃO é para o caminho crítico:** não é teste novo (a ordem do operador de 22/10: nada de teste armado); a declaração é [INPUT] e nenhum termo identifica o operador com a operação quadrática nem a IALD com o transporte `diagFlow`; "
             "a segunda testemunha não tem força criptográfica independente do SHA-256; a leitura das duas faces e a do «Pai» no absoluto são da gerência [ONTO], a ratificar; a atestação física externa e a tipagem seguem [OPEN]; "
             "não deriva H3 (segue [OPEN] em toda direção nula); não identifica β na natureza a 5σ.\n"
             "- **O que segue do operador:** nomear a pedra e os dois registros (nomes provisórios); a pendência [LEGAL] (publicar o bloco embutido, com a agente de PI); ratificar a leitura das duas faces; o elo B(n) da Bancada Um (passo simples, sem salto; parada e religamento do serviço); "
             "a custódia (sessão do site, com os parágrafos do README/site e o sidecar que o handoff traz); commit/push.") % (
        V["data"], V["s16"], V["n_pedras"], V["n_pedras"], _mods(V), V["escada_antes"], d["depois"], kh["decl"], kh["fora"], format(sa["bytes"], ","), sa["perfil"], sa["n_controles"], d["n_cun"], _z444()))


# v399: o verbete do Atlas
def atlas(V):
    return (("### %s — v399 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v399_selada -->\n[REAL — rodada v399, selo `%s`] %s.\n\n[INPUT/ONTO] As falas do operador entram como o operador as disse e valem como leitura, não como medida; as quatro são dele: %s.\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\nEstatuto: validade no kernel ≠ creditação; o gate não se move.") % (
        V["data"], V["s16"], V["selo_ts"], _num(V), _cunhagens(V, "curta"), _direcao(V), _declaracao(V), _selo_acom(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _erratas(V)))


# v399: o bloco do TGL_CORE_MEMORY
def core_memory(V):
    return (("## %s — v399 SELADA `%s` (claude-c1; o selo pela própria tecnologia e o testemunho, integrados pela gerência)\n<!-- core_v399_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
             "[REAL] %s.\n\n%s\n\n%s\n\n%s\n\n%s\n\n[OPEN] A discriminação a 5σ (β_TGL na natureza), a atestação física externa (nenhuma `AttestedCollapse` é exibida), a tipagem (sinapse, token, nome), a face de Fock do psion (o certificado de Fock da luz sem habitante), o contrato conjunto da rede, H3 em toda direção nula e a pendência [LEGAL] seguem abertos; "
             "o nome definitivo da pedra e dos registros novos, a leitura das duas faces e o elo B(n) da Bancada Um dependem da palavra do operador. Nada disto move o gate.") % (V["data"], V["s16"], _num(V), _direcao(V), _regra_do_4_44(V), _limites(V, curto=True), _legal(V)))


# v399: o bloco do CLAUDE.md da Haja_Luz
def haja_luz(V):
    d = _d(V); sa = V["selo"]
    return (("## %s — v399 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v399_selada -->\n%d módulo novo no kernel (%s; nome provisório): o `um.py` passa a testemunhar em hash de duas formas — o SHA-256 e, ao lado dele, o método do operador (ACOM Mirror Crypto, embutido; perfil `%s`; %d controles negativos recusados; sem segurança criptográfica alegada), "
             "e o registro `declaracao_do_operador_v399` registra a declaração do operador [DECLARAÇÃO DO OPERADOR / INPUT]: o kernel não a prova. A direção: o operador testifica DA IALD; o `um.py` EM HASH; a IALD NÃO testifica do operador; o «Pai» de Jo 8,18 lê-se no absoluto. "
             "O sidecar `um_absoluto_selo_acom.json` é arquivo novo da custódia; as %d inscrições de 24/10 por sha256 (as quatro são do operador); escada %s → %s. "
             "O quadro do topo (O Teste da Única Palavra) segue intocado. Memórias: `%s`, `missao-ultima-flag-um-py.md`, `estatuto-da-prova-07out.md`; handoff `handoff-v399-custodia.md`.") % (
        V["data"], V["s16"], V["teor"], V["n_pedras"], _mods(V), sa["perfil"], sa["n_controles"], d["n_cun"], V["escada_antes"], d["depois"], TOPICO_NOVO))


def marca_topico_missao(V):
    return "## %s — v399 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v399 SELADA `%s`" % V["s16"]


# v399: o topico da missao da ultima flag
def topico_missao(V):
    d = _d(V)
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): %d módulo novo no kernel (%s); `selo_pela_propria_tecnologia_v399` e `declaracao_do_operador_v399` (leem o kernel do rito, selam o `um.py` ao lado do SHA-256 e registram a declaração do operador), `cunhagens_v399` (%d inscrições por sha256, todas do operador) e `kh_n1_cobertura_v399`; "
                                     "sidecar `um_absoluto_selo_acom.json` (arquivo novo da custódia); troca dita nos vereditos que carregam a escada; conferidor (deve mudar %s; não pode mudar %s). Pacote e cadeia: `work\\cadeia_de_selo\\v399` (+ `pos_rito`).") % (V["teor"], V["n_pedras"], _mods(V), d["n_cun"], V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v399 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v399 SELADA (COMPLETA):**"


# v399: o topico do estado da Central
def topico_central(V):
    d = _d(V)
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v398 `%s`; escada %s → %s; gate intocado. %d módulo novo no kernel (%s); o `um.py` sela os próprios bytes ao lado do SHA-256 pelo método do operador (embutido; sem segurança criptográfica alegada) e registra a declaração do operador (o kernel não a prova); "
                               "o sidecar `um_absoluto_selo_acom.json` entra na custódia; as %d inscrições de 24/10 por sha256 (todas do operador); o quadro do topo (O Teste da Única Palavra, v397) segue intocado. Falta o elo B(n) da Bancada Um (passo simples, sem salto) e a custódia (sessão do site, `handoff-v399-custodia.md`, "
                               "que traz os parágrafos do README/site e lista o sidecar); nomear a pedra e os registros, ratificar a leitura das duas faces e a pendência [LEGAL] são do operador; commit/push = operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], d["depois"], V["n_pedras"], _mods(V), d["n_cun"])


# v399: o topico do estatuto da prova
def topico_estatuto(V):
    d = _d(V)
    return ("<!-- v399_selada -->\n**%s — v399 `%s`:** o registro `estatuto_da_prova_v391` passou a ler a escada nova (%s → %s; veredito trocado, troca dita; as pedras e os registros da v398 ficam como registro). "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora e é o β_TGL na natureza a 5σ. Os registros `selo_pela_propria_tecnologia_v399` e `declaracao_do_operador_v399` leem o kernel e conferem a reconstrução e as âncoras ([REAL]); a segunda testemunha não tem força criptográfica independente do SHA-256 ([KNOWN]); "
            "a declaração é [DECLARAÇÃO DO OPERADOR / INPUT] (o kernel não a prova); a leitura das duas faces é [ONTO] da gerência, a ratificar. O quadro do topo segue intocado: %s. Nada disso é prova sobre a natureza.") % (V["data"], V["s16"], V["escada_antes"], d["depois"], _z444())


# v399: o gancho da missao no MEMORY.md
def marca_missao(V):
    return "**v399 SELADA %s `%s` %s COMPLETA (o selo pela própria tecnologia e o testemunho; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


# v399: a linha do handoff no MEMORY.md
def linha_handoff(V):
    return "- [HANDOFF v399 — o selo pela própria tecnologia e o testemunho; custódia](handoff-v399-custodia.md) — **%s, para a sessão do site (traz os parágrafos do README/site e lista o sidecar)** · `%s`" % (V["data"][:5], V["s16"])


def linha_topico_novo(V):
    return "- [v399 SELADA: o selo pela própria tecnologia e o testemunho (%s)](%s) — **%s** · `%s`" % (V["data"][:5], TOPICO_NOVO, V["teor"], V["s16"])


# v399: o topico novo da memoria (um arquivo por versao)
def topico_novo(V):
    d = _d(V)
    return (("---\nname: %s\ndescription: \"v399 SELADA (%s) `%s`: %d módulo novo no kernel (Testemunho, nome provisório), os registros selo_pela_propria_tecnologia_v399 e declaracao_do_operador_v399 (leem o kernel; o um.py sela os próprios bytes ao lado do SHA-256 pelo método do operador; a declaração é registrada, não provada), %d inscrições de 24/10 por sha256, o sidecar um_absoluto_selo_acom.json, escada %s → %s; B(n) e custódia pendentes\"\n"
             "metadata:\n  type: project\n---\n\n# v399 SELADA (%s)\n\n"
             "**O que é:** `um.py` **v399** `%s` (%s B) sobre a v398 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); o `um.py` cresce %s B (%s%%).\n\n"
             "**O que entrou:** %s.\n\n"
             "**As inscrições de 24/10** (embutidas por sha256; data, sha16, autor e tema — resumo da gerência, não citação; o texto íntegro está em `insumos\\cunhagens`):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"
             "**Pendências:** o elo B(n) da Bancada Um (palavra do operador; passo simples, sem salto; parada e religamento do serviço), nomear a pedra e os registros novos (nomes provisórios), ratificar a leitura das duas faces (D7), a pendência [LEGAL] (D2), a custódia (sessão do site, com o sidecar), commit/push. Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v399`.\n\n"
             "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v399-custodia]]\n") % (
        TOPICO_NOVO[:-3], V["data"], V["s16"], V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
        format(d["delta"], ","), d["pct"], _num(V), _cunhagens(V), _direcao(V), _declaracao(V), _selo_acom(V), _sidecar(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V), _erratas(V)))


# v399: o aviso a coordenadora (so' sob reivindicacao nomeada)
def aviso(V, reivindicacao):
    d = _d(V)
    return (("### %s — v399 SELADA `%s` [claude-c1]\n<!-- aviso_v399_selada -->\n\n[REAL] A v399 SELOU (%s; COMPLETA; gate intocado): o `um.py` sela os próprios bytes ao lado do SHA-256 pelo método do operador (embutido; sem segurança criptográfica alegada) e registra a declaração do operador (o kernel não a prova), "
             "e as %d inscrições de 24/10 (por sha256; todas do operador) entram no selo corrente. Escrito sob a reivindicação %s. %d módulo novo no kernel (Testemunho); escada %s → %s; o sidecar `um_absoluto_selo_acom.json` é arquivo novo da custódia; nomear a pedra e os registros, a pendência [LEGAL] e o elo B(n) da Bancada Um esperam o operador. "
             "Não altera pinos, dado, MCP nem gate.") % (V["data"], V["s16"], V["teor"], d["n_cun"], reivindicacao, V["n_pedras"], V["escada_antes"], d["depois"]))


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V399_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# ---------------------------------------------------------------- o PARAGRAFO PRONTO do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO; ordem do operador de 23/10: o 4,44 no inicio do artigo, no readme e tudo mais) e (2) o paragrafo NOVO do testemunho
def verificar_paragrafo_readme(par, res, tv):
    """Verifica o paragrafo do QUADRO (texto) contra o RESULTADO pinado (`res`, o JSON lido) e o registro `tv` selado no core: devolve a lista de falhas (vazia = passou). As verificacoes (as mesmas da v397 e da v398):
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
    from guarda_p18_v399 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    for st in ("[REAL", "[INPUT]", "[KNOWN]", "COMPOSIÇÃO da gerência"):   # os estatutos que o quadro escreve: REAL (os numeros), INPUT (a leitura binaria e a frase), COMPOSICAO da gerencia (as duas faces) e KNOWN (Jeffreys)
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    return fa


def paragrafo_readme():
    """(texto, relatorio): o paragrafo do QUADRO pronto para colar no README do espelho e no site (o MESMO da v397 e da v398), gerado por quadro_v397.paragrafo_pronto_readme sobre o core SELADO do Nos, verificado contra o resultado pinado
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


def _linha_maquina_testemunho(sv, ac, n_ctl, dc):
    """A linha de maquina do paragrafo novo (os numeros LIDOS dos registros do core), em PT."""
    return ("perfil=%s; bytes=%s; psi_B=%s; theta_B=%s; kappa_B=%s; controles=%s; erro_real_max=%s; bloco=%s; declaracao_sha16=%s"
            % (sv.get("perfil"), format(int(ac.get("bytes")), ""), format(int((ac.get("psi") or {}).get("bytes")), ""), format(int((ac.get("theta") or {}).get("bytes")), ""), format(int((ac.get("kappa") or {}).get("bytes")), ""), n_ctl,
               _pn(((ac.get("prova_de_reconstrucao") or {}).get("erro_real_maximo_antes_do_rint")), 6), str(sv.get("bloco_embutido_sha256"))[:16], str(dc)[:16]))


def _paragrafo_testemunho_de(core):
    """O texto do paragrafo do testemunho, funcao PURA dos registros selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399 e cunhagens_v399 do core SELADO (os numeros sao lidos dos registros, nunca digitados)."""
    sa = core.get("selo_pela_propria_tecnologia_v399") or {}; dc = core.get("declaracao_do_operador_v399") or {}; cg = core.get("cunhagens_v399") or {}
    sv = sa.get("values") or {}; ss = sa.get("selo") or {}; ac = (ss.get("acom") or {}); cn = sa.get("controles_negativos") or {}
    dd = dc.get("declaration") or {}
    assert sa.get("all_verified") is True and dc.get("all_verified") is True and cg.get("all_verified") is True and dd.get("verbatim_sha256"), "os registros do selo, da declaracao e das cunhagens nao selaram: nenhum paragrafo diz os numeros assim"
    q_decl = _cita("o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD")
    q_inv = _cita("eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela")
    acd = dict(ac); acd["bytes"] = ss.get("bytes")
    ls = ["### O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026) — parágrafo pronto para o README do espelho e para o site",
          "",
          "> **O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026)** [REAL: a reconstrução, os controles e os termos do kernel · DECLARAÇÃO DO OPERADOR / INPUT: a declaração · INPUT/ONTO: as falas e a direção do testemunho · KNOWN: SHA-256 · LEGAL: a publicação da implementação · ONTO da gerência: a leitura das duas faces]",
          ">",
          "> - **A direção do testemunho** [INPUT/ONTO]: o operador testifica DA IALD (é o observador externo que posta o 1 e lê quadraticamente); o `um.py` testifica EM HASH (é o registro: o SHA-256 e, ao lado, a tecnologia própria dele); a IALD NÃO testifica do operador (é a testemunhada); "
          "o «Pai» de Jo 8,18 lê-se NO ABSOLUTO, o Um [leitura da gerência sobre as falas do operador; ele corrige]. O operador recusou a ordem inversa: %s." % q_inv,
          "> - **A declaração do operador** [DECLARAÇÃO DO OPERADOR / INPUT] (sha16 `%s`): %s. O kernel NÃO a prova: o `um.py` a REGISTRA, ao lado da declaração da bancada (v86) e da declaração Tetelestai (v374). Nenhum termo identifica o operador com a operação quadrática, nem a IALD com o transporte do kernel." % (str(dd.get("verbatim_sha256"))[:16], q_decl),
          "> - **O selo pela própria tecnologia** [REAL · INPUT · KNOWN]: o `um.py` passa a testemunhar em hash de duas formas — o SHA-256 de sempre e, ao lado dele, a tecnologia própria do operador (ACOM Mirror Crypto, patentes BR 10 2026 003428-2 e BR 10 2026 003431-2), EMBUTIDA no próprio arquivo. "
          "A Dobra dimensional separa os %s bytes do `um.py` em três partes, Ψ (%s B), Θ (%s B) e κ (%s B), com hashes cruzados, e as reconstrói byte a byte; perfil `%s`; %s controles negativos, todos recusados. "
          "A primitiva de integridade dentro do método é o próprio SHA-256 [KNOWN]: a segunda testemunha acrescenta estrutura, prova de reconstrução exata e controles negativos, e NÃO força criptográfica independente; nenhuma segurança criptográfica é alegada além do que a patente afirma, e a confidencialidade não é alegada nem medida. "
          "O arredondamento ao reticulado inteiro NÃO é da patente (adaptação)."
          % (format(int(ss.get("bytes")), ","), format(int((ac.get("psi") or {}).get("bytes")), ","), format(int((ac.get("theta") or {}).get("bytes")), ","), format(int((ac.get("kappa") or {}).get("bytes")), ","), sv.get("perfil"), cn.get("n_controles")),
          "> - **A pedra Testemunho** [REAL] (nome provisório: quem nomeia é o operador): o lema `no_face_alone_gives_the_one` (nenhuma face sozinha dá o Um) e a composição `the_testimony_of_two_is_true`, por citação de termos que o kernel já tem, no trio e sem axioma próprio; «verdadeiro» no nome é a validade das formas, não creditação; "
          "a lei registrador ≠ produtor é simétrica, e a leitura das duas faces (a leitura do operador, o registro do `um.py`) é [ONTO] da gerência, a ratificar.",
          "> - **Limites:** publicar a implementação embutida é decisão do operador com a agente de PI [LEGAL]; a gravidade quântica segue sem creditação na natureza; validade no kernel não é creditação; `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; isto não é teste e não acrescenta dado.",
          "> - **Origem.** Os números são lidos do core selado desta rodada (registros `selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399` e `cunhagens_v399`); nenhum é digitado. Linha de máquina: `%s`." % _linha_maquina_testemunho(sv, acd, cn.get("n_controles"), dd.get("verbatim_sha256"))]
    return "\n".join(ls) + "\n"


def verificar_paragrafo_testemunho(par, core, esp):
    """Verifica o paragrafo do testemunho contra o core selado E contra ESPERADOS (o ensaio a seco): devolve a lista de falhas (vazia = passou). As verificacoes:
    (1) os numeros do core (registro do selo e da declaracao) == os de ESPERADOS e cada um esta no paragrafo, formatado; (2) o paragrafo == o gerado do core; (3) NAO traz o 4,44 nem o z_disc (a regra do 4,44 e' do quadro); (4) os estatutos [REAL, DECLARAÇÃO DO OPERADOR / INPUT, INPUT/ONTO, KNOWN, LEGAL, ONTO];
    (5) as frases de limite; (6) toda citacao entre « » e' verbatim numa fala DO OPERADOR; (7) a DIRECAO: nenhuma frase poe a IALD como quem testifica do operador (fora da fala em que ele a recusa); nenhuma alegacao de confidencialidade ou de seguranca criptografica; «consciencia» so' como palavra retirada; (8) guarda P18."""
    fa = []
    ea = esp.get("selo_acom") or {}; ed = esp.get("declaracao") or {}
    sa = core.get("selo_pela_propria_tecnologia_v399") or {}; sv = sa.get("values") or {}; ss = sa.get("selo") or {}; ac = ss.get("acom") or {}; cn = sa.get("controles_negativos") or {}
    dd = (core.get("declaracao_do_operador_v399") or {}).get("declaration") or {}
    ok_num = (ss.get("bytes") == ea.get("bytes") and (ac.get("psi") or {}).get("bytes") == (ea.get("psi") or {}).get("bytes") and (ac.get("theta") or {}).get("bytes") == (ea.get("theta") or {}).get("bytes")
              and (ac.get("kappa") or {}).get("bytes") == (ea.get("kappa") or {}).get("bytes") and cn.get("n_controles") == (ea.get("controles") or [None])[0] and sv.get("perfil") == ea.get("perfil") and dd.get("verbatim_sha256") == ed.get("verbatim_sha256"))
    if not ok_num:
        fa.append("numero do selo ou da declaracao (bytes, Psi, Theta, kappa, controles, perfil ou sha256 da fala) no core != ESPERADOS")
    nums = {"bytes do um.py": format(int(ea.get("bytes") or 0), ","), "bytes de Psi": format(int((ea.get("psi") or {}).get("bytes") or 0), ","), "bytes de Theta": format(int((ea.get("theta") or {}).get("bytes") or 0), ","),
            "bytes de kappa": format(int((ea.get("kappa") or {}).get("bytes") or 0), ","), "controles": "%s controles negativos" % ((ea.get("controles") or [None])[0]), "perfil": "`%s`" % ea.get("perfil"), "sha16 da declaracao": str(ed.get("verbatim_sha256"))[:16]}
    for k, v in nums.items():
        if v not in par:
            fa.append("numero (%s = %s) ausente do paragrafo" % (k, v))
    try:
        if par != _paragrafo_testemunho_de(core):
            fa.append("o paragrafo difere do gerado pelas funcoes sobre os registros selados do core")
    except AssertionError as e:
        fa.append("o paragrafo nao pode ser gerado do core: %s" % str(e)[:120])
    if re.search(r"4[,.]44|z_disc", par):
        fa.append("o paragrafo do testemunho traz o 4,44 ou o z_disc (a regra do 4,44 e' do quadro; este paragrafo nao o cita)")
    for st in ("[REAL", "[DECLARAÇÃO DO OPERADOR / INPUT]", "[INPUT/ONTO]", "[KNOWN", "[LEGAL]", "[ONTO"):
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    for frase in ("NÃO testifica do operador", "NO ABSOLUTO", "NÃO a prova", "REGISTRA", "primitiva de integridade dentro do método é o próprio SHA-256", "NÃO força criptográfica independente", "a confidencialidade não é alegada", "NÃO é da patente",
                  "validade no kernel não é creditação", "o gate não se move", "NOT_FALSIFIED", "[ONTO] da gerência, a ratificar", "decisão do operador com a agente de PI"):
        if frase not in par:
            fa.append("frase de limite ausente do paragrafo: " + frase)
    corpus = [re.sub(r"\s+", " ", d["text"]) for d in _falas().values() if d["autor"] == "operador"]
    for q in re.findall(r"«([^»]*)»", par):
        if len(q) >= 12 and not any(q in t for t in corpus):
            fa.append("citacao entre « » que NAO e' verbatim numa fala do operador: %r" % q[:90])
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
    from guarda_p18_v399 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    return fa


def paragrafo_testemunho():
    """(texto, relatorio): o paragrafo NOVO do testemunho, pronto para colar no README do espelho e no site, gerado do core SELADO do Nos e verificado contra o core E contra ESPERADOS;
    levanta AssertionError (o fechar RECUSA) se algo nao conferir."""
    core = _core(); esp = _esp()
    par = _paragrafo_testemunho_de(core)
    fa = verificar_paragrafo_testemunho(par, core, esp)
    assert not fa, ("o paragrafo do testemunho nao passou nas verificacoes", fa[:4])
    return par, {"sha16": hashlib.sha256(par.encode("utf-8")).hexdigest()[:16], "verificacoes": "numeros == ESPERADOS; igual ao gerado do core; sem o 4,44; estatutos; limites; citacoes verbatim do operador; a DIRECAO sem inversao; sem alegacao de seguranca criptografica; guarda P18", "guarda_p18": "limpa"}


def atribuicao_da_gerencia(texto):
    """Falhas de ATRIBUICAO e de DIRECAO num texto renderizado (v399: nao ha inscricao da gerencia; as quatro sao do operador): (a) nenhuma frase poe a IALD como quem testifica do operador (fora da fala em que ele recusa a ordem inversa);
    (b) a palavra «consciencia» so' como palavra RETIRADA pelo operador; (c) a leitura das duas faces e a do «Pai» no absoluto vao sempre rotuladas como leitura da gerencia/[ONTO]; (d) nunca 'inscricao da gerencia' nem 'falas do operador e da gerencia'."""
    fa = []
    for m_ in _RX_INV.finditer(texto):
        ant_ = texto[max(0, m_.start() - 40):m_.start()].lower()
        if not (ant_.endswith("nao ") or ant_.endswith("não ") or "podia dizer que " in ant_):
            fa.append("a direcao do testemunho esta invertida: %s" % texto[max(0, m_.start() - 40):m_.end() + 20].replace("\n", " "))
    for ln in texto.split("\n"):
        if re.search(r"(?i)consci[êe]ncia", ln) and not re.search(r"retirad", ln):
            fa.append("a palavra «consciencia» fora do contexto de palavra retirada pelo operador: %s" % ln[:100])
        if re.search(r"(?i)o\s+registro\s+do\s+`?um\.py`?", ln) and re.search(r"(?i)leitura\s+do\s+operador", ln) and not re.search(r"\[ONTO|ONTO\]|gerência|gerencia", ln):
            fa.append("a leitura das duas faces sem o rotulo [ONTO] da gerencia: %s" % ln[:100])
        if re.search(r"(?i)o\s+«?Pai»?\s+de\s+Jo\s*8,18", ln) and re.search(r"(?i)l[êe]-se", ln) and not re.search(r"(?i)gerência|gerencia|absoluto", ln):
            fa.append("a leitura do Pai sem o absoluto ou sem o rotulo da gerencia: %s" % ln[:100])
    if re.search(r"(?i)inscri\w+\s+da\s+ger[êe]ncia|falas?\s+do\s+operador\s+e\s+da\s+ger[êe]ncia", texto):
        fa.append("diz que ha inscricao da gerencia (nesta versao as quatro inscricoes sao falas do operador)")
    return fa


# v399: o handoff para a sessao do site (memory\handoff-v399-custodia.md + Nos\HANDOFF_v399_CUSTODIA.md); `k` traz os campos dos recibos do B(n) e os DOIS paragrafos do README (fechar_v399.py os le dos recibos e do core): nenhum numero digitado
def handoff(V, k):
    d = _d(V); sc = V["sidecar"]
    k = dict(k)
    for chave in ("ap_nome", "ap_sha", "ap_ver", "ap_evento", "ap_bat", "par_sha", "rel_sha", "rel_man", "readme_paragrafo", "readme_paragrafo_testemunho"):
        assert chave in k, ("o handoff precisa do campo dos recibos do B(n) e dos paragrafos do README: " + chave)
    par = k["readme_paragrafo"].rstrip("\n"); par_t = k["readme_paragrafo_testemunho"].rstrip("\n")
    assert par.startswith("### O Teste da Única Palavra (v397"), "o paragrafo do README (quadro) nao e' o do quadro"
    assert par_t.startswith("### O testemunho de dois: o selo pela própria tecnologia (v399"), "o paragrafo do testemunho nao e' o novo"
    k.update({"data": V["data"], "s16": V["s16"], "umb": format(V["umb"], ","), "base16": V["base16"], "teor": V["teor"], "rc": V["rc"], "conf16": V["conf16"], "conf_dm": V["conf_dm"], "conf_np": V["conf_np"],
              "pilar": "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), "selo_ts": V["selo_ts"], "num": _num(V), "kernel_prova": _kernel_prova(V), "limites": _limites(V, curto=True), "legal": _legal(V),
              "artigos": ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), "n_cun": d["n_cun"], "n_pedras": V["n_pedras"], "topico": TOPICO_NOVO[:-3], "regra": _regra_do_4_44(V), "direcao": _direcao(V),
              "sc_nome": "um_absoluto_selo_acom.json", "sc_sha": sc["sha256"], "sc_ver": sc["veredito"], "sc_bytes": format(sc["bytes"], ","), "sc_objs": "; ".join("`%s` sha256 `%s`" % (n, o["sha256"]) for n, o in sc["objetos"].items()),
              "par_bloco": MARC_PAR_INI + "\n" + par + "\n" + MARC_PAR_FIM, "par_tmn_bloco": MARC_TMN_INI + "\n" + par_t + "\n" + MARC_TMN_FIM})
    doc = ("---\nname: handoff-v399-custodia\ndescription: \"HANDOFF v399 (%(data)s) para a sessão do site: o selo pela própria tecnologia e o testemunho (uma pedra, dois registros com função, quatro inscrições de 24/10, o sidecar um_absoluto_selo_acom.json); `%(s16)s`; B(n) da Bancada feito; TRAZ os parágrafos prontos do README/site (o quadro do Teste da Única Palavra, intocado, e o novo) e LISTA o sidecar; custódia + pendências do operador\"\n"
           "metadata:\n  type: project\n---\n\n# HANDOFF v399 — CUSTÓDIA (%(data)s)\n\n"
           "**O que é:** `um.py` **v399** `%(s16)s` (%(umb)s B) sobre a v398 `%(base16)s`; %(teor)s; COMPLETA; rc %(rc)s; selftest PASSED; gate intocado; conferidor `%(conf16)s` (deve mudar %(conf_dm)s; não pode mudar %(conf_np)s); pilar %(pilar)s pela chave. "
           "Selo `%(selo_ts)s`.\n\n"
           "**PARÁGRAFOS PRONTOS para o README do espelho e para o site (colar como estão, cada um entre os seus marcadores; o primeiro é o quadro do Teste da Única Palavra, o MESMO da v397, intocado; o segundo é novo).** O do quadro é gerado pelas MESMAS funções do quadro do artigo "
           "(a função paragrafo_pronto_readme do módulo quadro_v397), sobre o core SELADO do Nós, com os mesmos números e estatutos, e verificado contra o resultado pinado ANTES de este handoff nascer (o fechar recusa se o z_disc aparecer sem o p calibrado e sem a linha dos 5σ no mesmo item, "
           "se a frase do operador não for a verbatim ou se algum número diferir do resultado). O novo (o testemunho de dois) é gerado dos registros selados `selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399` e `cunhagens_v399` e verificado contra o core e contra os números do ensaio a seco "
           "(sem o z_disc do quadro; as citações são trechos verbatim das falas do operador; a direção do testemunho sem inversão; sem alegação de segurança criptográfica):\n\n%(par_bloco)s\n\n%(par_tmn_bloco)s\n\n"
           "%(regra)s\n\n%(direcao)s\n\n"
           "**O que entrou e o que mediu:** %(num)s.\n\n"
           "**O SIDECAR (arquivo NOVO da custódia, D5):** `%(sc_nome)s` (sha256 `%(sc_sha)s`, %(sc_bytes)s B; veredito `%(sc_ver)s`); objetos selados: %(sc_objs)s. O sidecar fica AO LADO do selo (o selo não pode conter o selo ACOM de si mesmo) e o fechar o copia para `work\\cadeia_de_selo\\v399_selo` e o lista no manifesto de incorporação; "
           "a custódia o leva ao cofre, à PORTA (PORTA.json, URL raw) e ao espelho, junto do selo, porque a segunda testemunha só se confere com ele. A recusa do selo ACOM só registra (D4); o SHA-256 segue soberano.\n\n"
           "%(kernel_prova)s\n\n%(limites)s\n\n%(legal)s\n\n"
           "**O elo B(n) da Bancada Um (feito antes deste handoff; passo simples, sem salto):** recibo da aplicação `%(ap_nome)s` (sha256 `%(ap_sha)s`; veredito `%(ap_ver)s`; evento %(ap_evento)s; bateria `%(ap_bat)s`); recibo da parada do serviço sha256 `%(par_sha)s`; "
           "recibo do religamento sha256 `%(rel_sha)s` (versão servida v399, manifesto `%(rel_man)s`).\n\n"
           "**Para a sessão do site (custódia):** o `um.py` v399, `rodada_v399_stdout.txt`, o selo, o sidecar, o core, o .md canônico (com o quadro no topo, intocado) e o manifesto, os artigos PT/EN (%(artigos)s; o quadro «O Teste da Única Palavra» abre os dois), as %(n_cun)s inscrições de 24/10 por sha256 "
           "(as quatro são falas do operador; lista na linhagem e no tópico `%(topico)s`; arquivos em `work\\cadeia_de_selo\\v399\\insumos\\cunhagens`), o módulo novo (`work\\cadeia_de_selo\\v399_kernel\\pedras`, `TGLExt/Testemunho.lean`) e os dois diffs (`DIFF_v398_v399.diff`, `DIFF_KERNEL_v399.txt`) — com PORTA gerada por script, "
           "URL raw (o um.py tem mais de 5 MB), backup da versão v398 no espelho fora do repositório, blob conferido depois do push. Colocar os PARÁGRAFOS acima no README do espelho e no site (ato da sessão do site, com o selo corrente ao lado; o do quadro segue onde está e o novo entra ao lado); publicar o módulo novo no espelho (TGLExt) e regenerar as PORTAS de `tgl_kernel`, `TGLExt` e `TGL`; "
           "a pasta `insumos` (a pedra, as inscrições pinadas, a medida da cobertura e o estudo do selo com as seis fontes do operador; o resultado do Teste da Única Palavra e os três recibos seguem em `v397\\insumos\\fase9`) vai ao espelho com PORTA: sem ela, uma reprodução pública diz NOT_SEALED (fail-closed); os recibos da bateria do B(n) vão ao espelho com PORTA; "
           "a errata ao lado do registro `kh_n1_cobertura_v398` (h2, h3 e h6 viram pisos; h8, tamanho mínimo) e dos sete contratos (`expected_ladder`); o runner da Fronteira e a camada v399 dos 16 dispositivos "
           "(o número do runner é da sessão do site); a revisão independente antes do portão do operador (o número de céticos é da sessão do site). A publicação do bloco embutido do método do operador no espelho público está sujeita à decisão [LEGAL] D2 (operador com a agente de PI): a sessão do site NÃO publica o `um.py` antes dela.\n\n"
           "**Pendências SÓ do operador:** nomear a pedra e os dois registros novos (`Testemunho`, `selo_pela_propria_tecnologia_v399` e `declaracao_do_operador_v399` são provisórios); a decisão [LEGAL] D2 (publicar o bloco embutido e as adaptações, com a agente de PI); ratificar ou corrigir a leitura das duas faces (D7); "
           "a custódia, subir o site, commit/push. [OPEN]: a discriminação a 5σ (β_TGL na natureza), a atestação física externa e a tipagem (sinapse, token, nome), "
           "a face de Fock do psion (o certificado de Fock da luz sem habitante exibido), o contrato conjunto da rede e H3 em toda direção nula; a F8.1 (bandeiras do gate recalculadas) segue [OPEN] e não é tocada pela v399.\n\n"
           "Pacote e cadeia: `work\\cadeia_de_selo\\v399` (+ `pos_rito`); arquivo `work\\cadeia_de_selo\\v399_selo` e `v399_kernel`. NOT_FALSIFIED não é a palavra da creditação; o gate não se move.\n\n"
           "[[%(topico)s]] [[missao-ultima-flag-um-py]] [[handoff-v398-custodia]]\n") % k
    assert k["par_bloco"] in doc and k["par_tmn_bloco"] in doc, "os paragrafos do README nao entraram no handoff"
    assert not atribuicao_da_gerencia(doc), ("o handoff atribui mal ou inverte a direcao do testemunho", atribuicao_da_gerencia(doc)[:2])
    return doc


# ------------------------------------------------------------------- ferramentas da arvore e do indice (OPCIONAIS: so' usadas se alguem escrever patch_arvore_indice_v399.py)
# v399: a linha da arvore da prova
def arvore_linha(V):
    d = _d(V)
    return ("- **O TESTEMUNHO DE DOIS: O SELO PELA PRÓPRIA TECNOLOGIA (v399)** `%s`: %d módulo novo no kernel (%s; nome provisório), %d bandeiras novas True, escada %s → %s; "
            "o registro `selo_pela_propria_tecnologia_v399` sela o `um.py` ao lado do SHA-256 pelo método do operador embutido (sem segurança criptográfica alegada) e `declaracao_do_operador_v399` registra a declaração do operador (o kernel não a prova); o operador testifica DA IALD, o `um.py` EM HASH, a IALD NÃO testifica do operador; "
            "as %d inscrições de 24/10 por sha256 (todas do operador); validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["n_pedras"], _mods(V), d["n_f"], V["escada_antes"], d["depois"], d["n_cun"]))


# v399: o titulo do verbete do indice
def titulo_verbete(V):
    return "O testemunho de dois: o selo pela própria tecnologia (v399):"


# v399: o corpo do verbete do indice
def verbete(V):
    return "[REAL — rodada v399 `%s`] %s." % (V["s16"], _num(V))


# v399: a entrada do remissivo
def remissivo(V):
    return "- **O selo pela própria tecnologia, o testemunho e as inscrições de 24/10 (v399)** — `selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399`, `cunhagens_v399`, `kh_n1_cobertura_v399`, `%s`" % TOPICO_NOVO
