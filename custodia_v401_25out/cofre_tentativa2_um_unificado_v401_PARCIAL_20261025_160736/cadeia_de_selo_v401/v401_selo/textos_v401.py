# -*- coding: utf-8 -*-
# Os TEXTOS da v401 SELADA, ESCRITOS A MAO para o delta da v401 (a semente mecanica veio de textos_v399.py, subida pelo motor; o conteudo e' novo): o modulo de kernel `FalsidadeDaInercia` (o nome «falsidade (simulacro) da inercia» e' do operador),
# o registro com funcao `falsidade_da_inercia_v401` (a inercia e' o proprio zero absoluto, o 0_abs do kernel, 1 = 0; um posto de peso 1 inercial daria 1 = 0; w(I) = 1 e' o Um POSTO que a interrompe, 1 = 1; calcula no modelo oneScaling com beta = alfa x raiz de e em runtime),
# os registros por spec `cunhagens_v401` (as SEIS falas do operador de 25/10, as oito ratificacoes de «Ratifico tudo.» e a errata ao lado da leitura do escriba no adendo de 03-04/09) e `kh_n1_cobertura_v401`, e a secao «A falsidade (simulacro) da inércia» do artigo.
# O QUADRO «O Teste da Única Palavra» (v397) PERMANECE no topo do artigo PT/EN e do .md canonico, INTOCADO. Cada numero, hash e veredito entra por chave de V (leitura_v401.ler), por ESPERADOS ou pelo core do Nos, ou e' LIDO de um arquivo aqui, nunca digitado;
# o que vai escrito a mao e' so' prosa, nome de termo (conferido em tempo de execucao no kernel do Nos, no um.py ou no pacote) e frase curta do operador (conferida palavra por palavra contra os bytes das falas).
# REGRA DA ORDEM DO OPERADOR (23/10/2026, sha16 9b182958a5a7a1bc: reportar o 4,44 no inicio do artigo, no README e em tudo mais; vale em TODO texto que o cite): o 4,44 (z_disc calibrado) NUNCA aparece sem o p calibrado e sem a linha dos 5σ no MESMO item (a discriminacao a 5σ,
# o degrau da creditacao, NAO foi alcancada; NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move; o teste nao foi cego). A frase do operador entra VERBATIM (nunca parafraseada entre aspas); o paragrafo do QUADRO sai das MESMAS funcoes do quadro (quadro_v397),
# sobre o core SELADO do Nos. O paragrafo NOVO da falsidade NAO traz o 4,44. Estatutos marcados; erratas AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a traducao falhou).
# O PARAGRAFO DO TESTEMUNHO DE DOIS (v399, regenerado no handoff da v400) SEGUE COMO ESTA no README do espelho e no site: esta versao NAO o regenera nem o substitui; o handoff da v401 so' o diz (e a leitura confere que os registros que o geravam seguem selados e iguais).
# GUARDA: as cinco regras da P18 (guarda_p18_v401.py) rodam sobre cada texto renderizado em superficies_v401.py, fechar_v401.py e registrar_mapa_v401.py e sobre este arquivo na cadeia. A palavra recusada nunca aparece aqui: a recusa e' dita como «creditação».
import hashlib, json, os, re, sys
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V401"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v401 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(PK))          # ...\Central de Patentes\work
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
# o topico novo da memoria (um arquivo por versao); o nome sem a extensao e' o campo name: do cabecalho do topico
TOPICO_NOVO = "v401-selada-falsidade-da-inercia.md"
# os marcadores entre os quais o handoff traz os PARAGRAFOS PRONTOS do README do espelho e do site: o QUADRO (v397, intocado) com os MESMOS marcadores da v397, e o paragrafo NOVO da falsidade
MARC_PAR_INI = "<!-- INICIO_PARAGRAFO_README_v397 -->"; MARC_PAR_FIM = "<!-- FIM_PARAGRAFO_README_v397 -->"
MARC_FAL_INI = "<!-- INICIO_PARAGRAFO_FALSIDADE_v401 -->"; MARC_FAL_FIM = "<!-- FIM_PARAGRAFO_FALSIDADE_v401 -->"
# o tema de cada uma das SEIS inscricoes de 25/10 (resumo da gerencia, nunca citacao): a chave e' o trecho do nome do arquivo de origem (depois do sha16); o sha16, a data e o autor vem dos bytes e do nome, nunca daqui
_TEMAS = (
    ("ratifico_tudo_e_emc2_geometria_projetada", "a ratificação («Ratifico tudo.») dos nomes antes provisórios e das leituras que a gerência lhe apresentou, e a pergunta dele sobre E = mc² como a geometria que a cinemática da gravidade projeta [INPUT]"),
    ("nada_e_materia_link_com_a_entropia", "nada = matéria como o link com a entropia, dito por ele como já explicado no artigo [INPUT/ONTO]"),
    ("materia_cristalizacao_da_dobra_da_luz", "a matéria como a cristalização da dobra da luz no vácuo, relativa ao observador [INPUT/ONTO]"),
    ("inercia_e_o_proprio_zero_absoluto", "a inércia de Newton e a definição dele: a inércia é o próprio zero absoluto [INPUT/ONTO; DEFINIÇÃO DO OPERADOR]"),
    ("nome_da_pedra_falsidade_simulacro_da_inercia", "o nome da pedra, «falsidade (simulacro) da inércia», e a ordem de fazer a prova [INPUT]"),
    ("derivacao_inercia_gravitacao_impressao", "o recorte declarado da fala de 25/10: o pedido de que a leitura seja DERIVADA e não [ONTO] dele, e o enunciado: a gravitação universal e a inércia não existem antes da impressão do Um posto; a inércia não é causa de si mesma; o zero é a consequência da poda [INPUT; pedido de derivação]"),
)
# nomes de termo de kernel (Lean) citados nos textos: cada um tem de existir em algum .lean de TGLExt/ do Nos (lido na hora); os modulos citados como fonte tem de existir como arquivo
_NOMES_KERNEL = ("the_inertia_is_the_absolute_zero", "the_inertia_of_a_post_is_false", "a_post_is_not_inertial", "the_post_exists_and_moves", "the_simulacrum", "the_inscription_interrupts_the_inertia", "falsidade_da_inercia", "fixed_tau_zero",
                 "nothing_above_bears_a_post", "the_floor_fixes_the_cut", "oneScaling", "beta_forbids_full_static_witness", "leakage_strictly_loses", "FullStaticWitness", "costless", "metric_einstein_from_screen_clausius",
                 "no_post_before_the_impression", "inertia_is_not_its_own_cause", "the_first_motion_is_the_impression", "diagFlow_coordinate_is_the_scaling", "leak_below_every_epsilon", "the_zero_is_the_consequence_of_the_pruning", "the_tension_is_projected_onto_the_attractor", "falsidade_da_inercia_derivada",
                 "the_fall_never_lands", "abismo", "um_is_the_great_attractor", "the_observer_is_unique", "diagFlow", "permanent", "observerProj")
_MODULOS_KERNEL = ("FalsidadeDaInercia", "TheCorrespondence", "Fundacao", "NoFullWitness", "GeneralMetricClausius", "Testemunho", "TheGreatAttractor", "BoundaryException", "ObserverInside")
# identificadores do um.py citados nos textos: cada um tem de existir no um.py do Nos (lido na hora)
_NOMES_UM = ("SEALED_CODATA_ALPHA", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "_V401_VERBATINS2", "_V401_SPECS", "_V401_FALSIDADE_CONTRACT", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399",
             "cunhagens_v399", "kh_n1_cobertura_v399", "selo_acom_sidecar_v399", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "hubble_ratio_opening_v388", "_v397_quadro_md", "_v397_atomos", "_V397_FRASE_444",
             "testemunha_estatica_v396", "psibit_v395", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V395_PSIBIT_CONTRACT",
             "_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT")
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
N_FALAS = len(_TEMAS)   # (o numero e' CONFERIDO em _d contra len(DL.VERBATIM_ORIGEM_V401) e ESPERADOS[cunhagens]; a prosa diz «seis» e o assert abaixo derruba a geracao se o numero mudar) as inscricoes de 25/10 embutidas na v401: seis falas do operador (nenhuma e' da gerencia)
_CACHE = {}
# a DIRECAO (v399): nenhuma frase pode por a IALD como quem testifica DO operador (fora da fala em que ele a recusa); a mesma regex do conferidor (C12)
_RX_INV = re.compile(r"IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)")
ERRATA_TEOREMAS = "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"   # (a mesma frase de delta_v401.ERRATA_TEOREMAS_PT; o harness confere)


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


# ---------------------------------------------------------------- leitura dos insumos, do ESPERADOS e do core (tudo por script; nenhum numero, hash ou citacao vem da memoria)
def _esp():
    """ESPERADOS_v401.json (gerado pelo ensaio a seco do candidato), lido uma vez."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v401.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _core():
    """O core do Nos (so' leitura), para os campos que so' existem depois do rito; ausente e' falha visivel."""
    if "core" not in _CACHE:
        _CACHE["core"] = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["core"]


def _base_core():
    """O core da v400 selada (a copia de bytes em base_v400): de onde saem os numeros da errata ao lado e a medida da proveniencia."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v400", "um_absoluto.json"), encoding="utf-8"))["core"]
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
    """As SEIS inscricoes de 25/10 embutidas no um.py: o texto vem do arquivo em insumos/cunhagens e o sha256 e' conferido contra ESPERADOS (fail-closed). Devolve {sha16: {sha16, arquivo, nome, text, autor}};
    o autor sai do NOME do arquivo e e' conferido contra o papel que ESPERADOS registra: nesta versao as seis sao falas do operador (nenhuma e' da gerencia)."""
    if "falas" not in _CACHE:
        ec = _esp()["cunhagens"]; out = {}; pasta = os.path.join(PK, "insumos", "cunhagens")
        for k, meta in ec.items():
            s = k[len("v401_cun_"):]
            fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(s + "_")]
            assert len(fs) == 1, ("a inscricao %s nao tem arquivo unico em insumos/cunhagens" % s, fs)
            b = open(os.path.join(pasta, fs[0]), "rb").read()
            assert hashlib.sha256(b).hexdigest() == meta["sha256"] and len(b) == meta["bytes"] and meta["sha256"][:16] == s, "a inscricao %s nao confere com o sha256 de ESPERADOS" % s
            nome = fs[0][len(s) + 1:]
            autor = "gerencia" if nome.startswith("GERENCIA_") else "operador"
            assert autor == "operador" and not str(meta.get("papel", "")).startswith("leitura da gerencia"), ("a v401 nao tem inscricao da gerencia: as seis sao falas do operador", s)
            out[s] = {"sha16": s, "arquivo": fs[0], "nome": nome, "text": b.decode("utf-8"), "autor": autor}
        assert len(out) == len(_TEMAS) == N_FALAS, "as inscricoes de ESPERADOS nao sao as seis de 25/10"
        _CACHE["falas"] = out
    return _CACHE["falas"]


def _sha_por(sub):
    """O sha16 da unica inscricao cujo arquivo de origem contem `sub` (as inscricoes sao achadas assim, nunca digitadas)."""
    r = [s for s, d in _falas().items() if sub in d["nome"]]
    assert len(r) == 1, ("inscricao nao unica ou ausente", sub, r)
    return r[0]


def _cita(trecho):
    """Fail-closed: o trecho tem de estar numa das seis falas DO OPERADOR, palavra por palavra e na mesma ordem; devolve «trecho». Citacao fora dos bytes derruba a geracao.
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


def _adendo_texto():
    """O texto do adendo de 03-04/09 (a copia duravel em insumos\\adendo, pinada por sha256 no registro cunhagens_v401): sem negrito e sem crase, como as conferencias leem."""
    if "adendo" not in _CACHE:
        pasta = os.path.join(PK, "insumos", "adendo"); fs = sorted(f for f in os.listdir(pasta) if f.endswith(".md")); assert len(fs) == 1, fs
        b = open(os.path.join(pasta, fs[0]), "rb").read()
        _CACHE["adendo"] = {"sha16": hashlib.sha256(b).hexdigest()[:16], "nome": fs[0], "text": re.sub(r"\s+", " ", b.decode("utf-8").replace("**", "").replace("`", ""))}
    return _CACHE["adendo"]


def _cita_adendo(trecho):
    """Como _cita, contra os bytes do adendo (a leitura do escriba que a errata cita; NAO e' fala do operador, exceto o item 7, que o adendo registra como dele)."""
    assert "\n" not in trecho and "  " not in trecho
    assert trecho in _adendo_texto()["text"], "citacao fora dos bytes do adendo: %r" % trecho[:70]
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


def _data_fala(d, V):
    m = re.match(r"(?:OPERADOR|GERENCIA)_(\d{2})out_", d["nome"])
    assert m, ("o nome do arquivo da inscricao nao traz a data", d["nome"])
    return "%s/10/%s" % (m.group(1), V["data"][-4:])


def _cov_base():
    """A cobertura do Audit e a arvore formal da v400 selada (o core guardado em base_v400): de onde saem os numeros da errata ao lado dos pisos."""
    if "cov_base" not in _CACHE:
        kf = _base_core()["kernel_formalization"]
        cov = kf["axiom_coverage_v392"]
        _CACHE["cov_base"] = {"decl": cov["decl"], "thm": cov["thm"], "h8": len(kf["formal_files_sha256"]), "axr": len(kf["axiom_report"])}
    return _CACHE["cov_base"]


def _bancada():
    """A geracao do manifesto que a Bancada de producao pina (do recibo pre_selo pinado em PINOS_BN) e a versao que ela pina; o passo e' simples (sem salto e sem cadeia de selos)."""
    p = json.load(open(os.path.join(PK, "PINOS_BN_v401.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v400" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v400 -> v401 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1}


def _proveniencia(esp):
    """A proveniencia que o compilador emite atribui ao modulo da pedra N declaracoes; todas sao NOVAS no axiom_report (nenhuma reatribuida), e o FLAGS_v401.json do sandbox concorda (as contagens de
    publicas, privadas, nomeadas e auxiliares so' existem la')."""
    if "prov" not in _CACHE:
        kf = _core()["kernel_formalization"]; src = kf["declaration_sources_v394"]; pedras = set(esp["pedras_sha256"])
        b0 = _base_core()["kernel_formalization"]; axr0 = b0["axiom_report"]
        mine = sorted(n for n, p in src.items() if p in pedras)
        novas = [n for n in mine if n not in axr0]
        fj = json.load(open(os.path.join(PK, "kernel", "FLAGS_v401.json"), encoding="utf-8"))
        assert len(mine) == fj["decl_totais_modulos_novos"] and len(novas) == fj["decl_novas_dos_modulos"] == len(mine) and not fj["reatribuidas_as_pedras"], ("a proveniencia do rito != FLAGS_v401.json do sandbox", len(mine), len(novas), fj["reatribuidas_as_pedras"])
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
    """Os numeros da v401, todos LIDOS (V da leitura da rodada, ESPERADOS, core do Nos, base v400, FLAGS do sandbox, os registros): nenhum e' digitado aqui. Recusa se as contagens nao fecham."""
    _conferir_nomes()
    esp = _esp(); tv = V["veracidade"]; sa = V["selo"]; dc = V["declaracao"]; cg = V["cunhagens"]; sc = V["sidecar"]; fa = V["falsidade"]
    mods = sorted(p["modulo"] for p in V["pedras"])
    assert mods == ["TGLExt.FalsidadeDaInercia"] and V["n_pedras"] == len(mods) == esp["kernel"]["modulos_novos"], ("o delta da v401 e' um modulo, TGLExt.FalsidadeDaInercia", mods)
    nf = esp["n_bandeiras_novas"]; grp = esp["n_bandeiras_por_grupo"]
    assert set(grp) == {"falsidade"} and grp["falsidade"] == nf == esp["politica_de_bandeiras"]["n_flags"] == len(esp["bandeiras_novas_chaves"]), "as bandeiras novas nao sao so' as do modulo FalsidadeDaInercia"
    assert fa["flag"] == esp["bandeiras_das_pedras"]["falsidade"] and fa["flag_true"] is True and fa["theorem"] == esp["teoremas_das_pedras"]["falsidade"], "a pedra FalsidadeDaInercia no kernel do rito nao e' a de ESPERADOS"
    DL_ = _qd().DL
    assert N_FALAS == len(DL_.VERBATIM_ORIGEM_V401) == len(esp["cunhagens"]) == 6, "o numero de inscricoes de 25/10 mudou: a prosa dos textos diz seis (ler N_FALAS, DL.VERBATIM_ORIGEM_V401 e ESPERADOS[cunhagens])"
    assert fa["n_checks"] == DL_.N_CHECKS_FALSIDADE and len(esp["contrato_das_pedras"]["falsidade"]) == len(DL_.STONES[0]["contract"]) and esp["n_bandeiras_novas"] == len(DL_.STONES[0]["contract"]), "as checagens do calculo ou as declaracoes do contrato != delta_v401 (N_CHECKS_FALSIDADE, STONES[0].contract)"
    assert _sha_por("derivacao_inercia_gravitacao_impressao").startswith(DL_.VERBATIM_PREFIXOS_DA_ORDEM_V401[-1]), "o recorte declarado da fala de 25/10 nao e' o ultimo prefixo de DL.VERBATIM_PREFIXOS_DA_ORDEM_V401"
    assert fa["chain_ok"] is True and cg["cadeia_ok"] is True, "a cadeia derivada (chain_status, H_tau nomeada e nao usada por teorema) nao confere nos registros"
    assert fa["ok"] is True and fa["mech_ok"] is True and fa["values_ok"] is True and fa["estrela_ok"] is True and fa["kernel_ok"] is True and fa["beta_ok"] is True, "o registro falsidade_da_inercia_v401 do core nao e' o contrato de ESPERADOS"
    assert sa["ok"] is True and sa["n_checks"] == esp["selo_acom"]["n_checks"] and sa["checks_ok"] is True and sa["values_ok"] is True and sa["beta_ok"] is True, "o registro selo_pela_propria_tecnologia_v399 do core nao e' o contrato de ESPERADOS"
    assert dc["ok"] is True and dc["n_checks"] == esp["declaracao"]["n_checks"] and dc["checks_ok"] is True and dc["ancoras_ok"] is True and dc["direcao_ok"] is True, "o registro declaracao_do_operador_v399 do core nao e' o contrato de ESPERADOS"
    assert sc["ok"] is True and sc["n_objetos"] == len(esp["sidecar"]["objetos"]) and sc["recusas"] == 0, "o sidecar um_absoluto_selo_acom.json nao e' o de ESPERADOS"
    assert tv["ok"] is True and tv["n_checks"] == esp["veracidade"]["n_checks"] and tv["checks_ok"] is True and tv["numeros_ok"] is True and tv["fontes_ok"] is True, "o registro teste_de_veracidade_fase9_v397 do core nao e' o contrato de ESPERADOS (o quadro do topo le os numeros dele)"
    assert cg["verbatim_ok"] is True and cg["n"] == len(V["verbatins"]) == len(_falas()) == N_FALAS and cg["todas_do_operador"] is True and cg["ratificacoes_ok"] is True and cg["errata_ok"] is True, "as inscricoes de ESPERADOS != as seis de 25/10, ou alguma nao e' fala do operador, ou faltam as ratificacoes/a errata"
    assert {re.match(r"(?:OPERADOR|GERENCIA)_(\d{2})out_", f["nome"]).group(1) for f in _falas().values()} == {"25"}, "o nome de arquivo de alguma inscricao nao e' de 25/10 (a data dos textos e' 25/10)"
    qd = _qd(); a = _atomos()
    assert qd.Q._v397_linha_de_maquina(a, "pt") == esp["quadro"]["linha_de_maquina_pt"], "a linha de maquina do quadro (core) != a de ESPERADOS"
    assert esp["quadro"]["frase_do_operador"] == qd.DL.FRASE_DO_OPERADOR_4_44 == qd.Q._V397_FRASE_444, "a frase do operador do quadro != a verbatim"
    base = os.path.join(PK, "base_v400", "um.py")
    if "base_b" not in _CACHE:
        assert s16(base) == V["base16"], "base_v400/um.py nao e' a v400 selada"
        _CACHE["base_b"] = os.path.getsize(base)
    delta = V["umb"] - _CACHE["base_b"]
    kf = _core().get("kernel_formalization") or {}; prov = kf.get("declaration_sources_status_v394") or {}
    assert prov.get("ok") is True and prov.get("compiler_names") == prov.get("audited_names") == V["axiom_report_n"], "a proveniencia emitida pelo compilador nao cobre o axiom_report do rito"
    assert V["n_ver_mudaram"] == 0, "algum veredito fora da troca dita mudou: nao ha texto a escrever"
    assert V["n18"] == 18 and all(i in V["patch_ids"] for i in ("N00_main_falsidade", "N01_main_specs", "N02_selo")), "o gate nao tem as 18 bandeiras True, ou o candidato nao traz os patches que chamam a falsidade (N00), os registros por spec (N01) e o resumo no selo (N02)"
    assert esp["h8_entradas"] == esp["formal_files_n"] + len(esp["h8_residuais_do_nos"]), "a arvore formal do rito != embutidas + residuais do Nos"
    pb = _core().get("psibit_v395") or {}; pbc = pb.get("conditional_psion_face") or {}
    assert pbc.get("flag_true") is True and kf.get(pbc.get("flag")) is True and pbc.get("inhabitant_exhibited") is False, "a face de Fock do psibit_v395 nao segue condicional e com a bandeira True"
    pv = _proveniencia(esp); ad = _adendo_texto()
    hy = _g(_core(), "cunhagens_v401", "extras", "hipotese_nomeada") or {}; m025 = re.search(r"sha16 ([0-9a-f]{16})", str(hy.get("pendencia_externa")))
    assert hy.get("nome") == "H_tau" and hy.get("estatuto") == "[OPEN]" and hy.get("usada_por_teorema") is False and m025, "a hipotese nomeada H_tau ([OPEN], nao usada por teorema, com a ORDEM 025 como pendencia externa) nao esta no registro cunhagens_v401"
    assert ad["sha16"] == _g(_core(), "cunhagens_v401", "extras", "adendo", "sha16"), "o adendo pinado em insumos != o que o registro cunhagens_v401 pina"
    return {"n_f": nf, "n_aux": esp["politica_de_bandeiras"]["n_excluidas"], "depois": V["teor"].split("/")[0], "delta": delta, "pct": ("%.1f" % (100.0 * delta / _CACHE["base_b"])).replace(".", ","),
            "prov": prov["compiler_names"], "n_cun": len(V["verbatins"]), "n_op": N_FALAS, "unc_f": esp["bandeiras_das_pedras"]["falsidade"], "teo_f": esp["teoremas_das_pedras"]["falsidade"], "est_f": esp["falsidade"]["estrela"]["bandeira"],
            "est_t": esp["falsidade"]["estrela"]["teorema"], "ft0": min(esp["bandeiras_novas_chaves"]), "ft1": max(esp["bandeiras_novas_chaves"]), "h8": esp["h8_entradas"], "h8_emb": esp["formal_files_n"],
            "h8_res": ", ".join("`%s`" % x for x in esp["h8_residuais_do_nos"]), "n_res": len(esp["h8_residuais_do_nos"]), "cb": _cov_base(), "bank": _bancada(), "pv": pv, "n_checks_v": tv["n_checks"],
            "n_ck_sel": sa["n_checks"], "n_ck_dec": dc["n_checks"], "n_ck_cun": cg["n_checks"], "n_ck_fal": fa["n_checks"], "sha_pedra": esp["pedras"]["TGLExt/FalsidadeDaInercia.lean"]["sha16"], "n_sup": len(esp["suporte_das_pedras"]["falsidade"]),
            "n_contr": len(esp["contrato_das_pedras"]["falsidade"]), "n_anc": len(esp["declaracao"]["ancoras"]), "f8": {k: v[:8] for k, v in esp["veracidade"]["fontes"].items()}, "s_rat": _sha_por("ratifico_tudo"), "s_nada": _sha_por("nada_e_materia"),
            "s_mat": _sha_por("materia_cristalizacao"), "s_imp": _sha_por("derivacao_inercia_gravitacao_impressao"), "o025": m025.group(1), "s_in": _sha_por("inercia_e_o_proprio_zero_absoluto"), "s_nome": _sha_por("nome_da_pedra"), "s_adendo": ad["sha16"], "data_falas": "25/10/2026", "n_rat": cg["n_ratificacoes"]}


def _mods(V):
    return ", ".join("`%s`" % p["modulo"].split(".")[-1] for p in sorted(V["pedras"], key=lambda p: p["modulo"]))


def _extras(V):
    # os registros novos ALEM DOS TRES FIXOS (V["reg401"] tem so' os tres), ditos pelo nome
    ex = [k for k in V["registros_novos"] if k not in V["reg401"]]
    return (", ".join("`%s`" % k for k in ex)) if ex else "nenhum além dos três fixos"


def _cab(V):
    return "v401 SELADA (COMPLETA)** `%s`" % V["s16"]


# ---------------------------------------------------------------- os numeros e os blocos
def _num(V, verdicts=True):
    """O paragrafo dos numeros da v401 (kernel, o registro com funcao, os dois registros por spec, os quatro da v399 recriados, o sidecar, a troca dita): usado na linhagem, no Atlas, no core, no topico novo, no verbete e no handoff."""
    d = _d(V); kh = V["kh"]; fa = V["falsidade"]; sc = V["sidecar"]; sa = V["selo"]
    vd = (lambda k: " (%s)" % V["reg401"][k]["verdict"]) if verdicts else (lambda k: "")
    kern = _f("o kernel ganhou {n_pedras} módulo novo ({mods}; o nome «falsidade (simulacro) da inércia» é do operador), com {n_f} bandeiras novas True (de `{ft0}` a `{ft1}`), só de declaração nomeada ({aux} auxiliares geradas pelo compilador ficam sem bandeira), e escada {antes} → {depois} teoremas limpos "
              "({axr} declarações no `axiom_report`, {fora} fora do trio, {nl} nomes não lidos; a proveniência de cada declaração emitida pelo compilador cobre as mesmas {prov}); "
              "errata ao lado da v394, mantida (em nome próprio da gerência c1): " + ERRATA_TEOREMAS,
              n_pedras=V["n_pedras"], mods=_mods(V), n_f=d["n_f"], ft0=d["ft0"], ft1=d["ft1"], aux=d["n_aux"], antes=V["escada_antes"], depois=d["depois"], axr=V["axiom_report_n"], fora=kh["fora"], nl=kh["nao_lidas"], prov=d["prov"])
    fal = _f("o registro `falsidade_da_inercia_v401`{vd}, lido na fractalização do Um logo depois da declaração do operador: lê do kernel do próprio rito a composição derivada da pedra (bandeira `{unc}`) e a estrela (bandeira `{est}`), as {n_contr} declarações do contrato e os {n_sup} termos antigos que ela cita, todos no trio, "
             "e CALCULA, com β = α(CODATA 2018) × √e em runtime, o modelo `oneScaling`: o peso do posto depois da escala s é e^(−s), igual a 1 só em s = 0; só o estado nulo é fixo pelo fluxo inteiro; o custo t·β·g é estritamente positivo e o fator de defasagem, estritamente menor que 1 "
             "e a cadeia derivada [DERIVED] (nada que porte posto precede a impressão; a inércia não é causa de si mesma; o zero é a consequência da poda; a tensão projetada no atrator; `chain_status`) com a única hipótese nomeada `H_tau` [OPEN], que nenhum teorema usa ({nck} checagens, todas passaram); o 0_abs de `costless` está no kernel embutido deste rito", vd=vd("falsidade_da_inercia_v401"), unc=d["unc_f"], est=d["est_f"], n_contr=d["n_contr"], n_sup=d["n_sup"], nck=d["n_ck_fal"])
    cun = _f("o registro `cunhagens_v401`{vd}: as {n} inscrições de 25/10 embutidas por sha256 e consumidas no rito, TODAS falas do operador (nenhuma é da gerência), as {nr} ratificações de «Ratifico tudo.» e a errata ao lado da leitura do escriba no adendo de 03-04/09 ({nck} checagens, todas passaram); "
             "são [INPUT/ONTO] e valem como leitura dele, não como medida; o registro traz também a `cadeia_derivada` [DERIVED] (o recorte declarado da fala de 25/10 pede a leitura derivada) e a `hipotese_nomeada` `H_tau` [OPEN]", vd=vd("cunhagens_v401"), n=d["n_cun"], nr=d["n_rat"], nck=d["n_ck_cun"])
    khs = _f("o registro `kh_n1_cobertura_v401`{vd}: {decl} constantes, {thm} teoremas, {fora} fora do trio, {nl} nomes não lidos; a árvore formal do Nós depois do rito tem {h8} entradas ({emb} embutidas mais {nres} residual do Nós: {res}), "
             "e o pino h8 do registro é o hash dessa árvore, calculado por script sobre a árvore simulada do Nós na geração do candidato",
             vd=vd("kh_n1_cobertura_v401"), decl=kh["decl"], thm=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"], h8=d["h8"], emb=d["h8_emb"], nres=d["n_res"], res=d["h8_res"])
    v399 = _f("os quatro registros da v399 (`selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399`, `cunhagens_v399` e `kh_n1_cobertura_v399`) são recriados no mesmo ponto do main e seguem selados e iguais ao ensaio a seco; o selo pela própria tecnologia sela os {bytes} bytes do `um.py` v401 ao lado do SHA-256 "
              "(perfil `{perfil}`, {nctl} controles negativos recusados), e o sidecar `um_absoluto_selo_acom.json` (arquivo da custódia desde a v399, reescrito pelo rito; sha256 `{sc16}`, veredito `{sv}`, {nr} recusas) lista os {no} objetos finais",
              bytes=format(sa["bytes"], ","), perfil=sa["perfil"], nctl=sa["n_controles"], sc16=sc["sha16"], sv=sc["veredito"], nr=sc["recusas"], no=sc["n_objetos"])
    ex = _extras(V)
    resto = _f("{ex}; o registro `teste_de_veracidade_fase9_v397` segue selado e igual (o quadro do topo do artigo le os numeros dele); troca dita (só números): {troca}; nenhuma mudança NÃO numérica: {nm} vereditos fora da troca dita mudaram (exigido: 0); validade no kernel não é creditação",
               ex=("nenhum registro novo além dos três fixos" if ex.startswith("nenhum") else "registros novos além dos três fixos: " + ex), troca=", ".join("`%s`" % x for x in V["troca_dita"]), nm=V["n_ver_mudaram"])
    return "; ".join([kern, fal, cun, khs, v399, resto])


def _cunhagens(V, forma="lista"):
    """As inscricoes de 25/10 embutidas por sha256: 'lista' (data, sha16, autor e tema, uma por linha; as seis sao falas do operador) ou 'curta' (uma frase com os sha16). Data, sha16 e autor vem dos bytes e do nome; o tema e' da gerencia (_TEMAS)."""
    fl = list(_falas().values()); assert len(fl) == len(V["verbatins"]) == N_FALAS
    if forma == "curta":
        return _f("{n} inscrições embutidas por sha256, todas falas do operador [INPUT/ONTO] — a ratificação e a pergunta sobre E = mc² `{a}`, nada = matéria e a entropia `{b}`, a matéria como cristalização da dobra da luz `{c}`, a inércia como o próprio zero absoluto `{e}` e o nome da pedra `{g}`",
                  n=len(fl), a=_sha_por("ratifico_tudo"), b=_sha_por("nada_e_materia"), c=_sha_por("materia_cristalizacao"), e=_sha_por("inercia_e_o_proprio_zero_absoluto"), g=_sha_por("nome_da_pedra"))
    linhas = []
    for d in fl:
        r = [tema for chave, tema in _TEMAS if chave in d["nome"]]
        assert len(r) == 1, ("a inscricao nao tem um tema unico em _TEMAS", d["sha16"], len(r))
        linhas.append("- %s `%s` (fala do operador) — %s" % (_data_fala(d, V), d["sha16"], r[0]))
    return "\n".join(linhas)


def _ordem(V):
    """A ordem do operador de 25/10: so' citacao conferida contra os bytes das falas DO OPERADOR."""
    d = _d(V)
    q_cheg = _cita("agora chegamos à inércia de Newton"); q_def = _cita("a minha definição é o próprio zero absoluto")
    q_mat = _cita("a matéria é a cristalização da dobra luz no vácuo relativa ao observador"); q_nada = _cita("nada=materia e esse é o link com a entropia")
    q_nome = _cita("a pedra chama-se \u201cfalsidade (simulacro) da inércia\u201d, faça a prova"); q_rat = _cita("Ratifico tudo."); q_emc2 = _cita("Então E=m.c2 é a geometria que a cinemática da gravidade=luz2.entropia projeta?")
    q_der = _cita("eu não queria que a leitura fosse ONTO minha, quero que seja derivado"); q_imp = _cita("a gravitação universal e a inércia não existem antes da posição impressa do Um absoluto")
    q_mov = _cita("o primeiro movimento é a impressão do posto absoluto ocupado por 1"); q_poda = _cita("o zero absoluto não é o início de tudo, não. ele é a consequencia da poda")
    return _f("**A ordem:** [INPUT/ONTO] as {n_op} falas do operador (Luiz Antonio Rotoli Miguel) de {data} que entram nesta rodada, TODAS dele (nenhuma é da gerência), embutidas por sha256 no registro `cunhagens_v401` e listadas abaixo (as aspas aqui são TRECHOS, conferidos palavra por palavra contra os bytes de cada fala; "
              "o texto íntegro está em `work\\cadeia_de_selo\\v401\\insumos\\cunhagens`): sobre a inércia, {q_cheg}, e a definição dele, {q_def} (`{s_in}`); sobre a matéria e o nada, {q_mat} (`{s_mat}`) e {q_nada} (`{s_nada}`); "
              "o nome da pedra e a ordem, {q_nome} (`{s_nome}`); a ratificação, {q_rat}, na mesma fala da pergunta {q_emc2} (`{s_rat}`); e o recorte declarado da fala de 25/10 (`{s_imp}`), que PEDE a leitura derivada: {q_der}, e enuncia {q_imp}, {q_mov}, e {q_poda}. "
              "A gerência c1 preparou o candidato e rodou o rito (pacote `work\\cadeia_de_selo\\v401`); as fontes pinadas dos registros ficam em `insumos`: a pedra (`FalsidadeDaInercia.lean`), a medida da cobertura (`KH_N1_v401.json`) e a cópia durável do adendo de 03-04/09 (`insumos\\adendo`); "
              "o resultado do Teste da Única Palavra, que o quadro do topo lê, mora na v397 (`insumos\\fase9`); quem constrói não aprova: a revisão independente do candidato, da pedra e dos derivados da cadeia é ato distinto e não é afirmada por este registro.",
              n_op=d["n_op"], data=d["data_falas"], q_cheg=q_cheg, q_def=q_def, q_mat=q_mat, q_nada=q_nada, q_nome=q_nome, q_rat=q_rat, q_emc2=q_emc2, s_in=d["s_in"], s_mat=d["s_mat"], s_nada=d["s_nada"], s_nome=d["s_nome"], s_rat=d["s_rat"], s_imp=d["s_imp"], q_der=q_der, q_imp=q_imp, q_mov=q_mov, q_poda=q_poda)


def _definicao(V):
    """A definicao do operador e o que a pedra tipa: [INPUT/ONTO] a definicao; [REAL] os termos do kernel; [KNOWN] a lei de escala de Takesaki; [OPEN] o fluxo de um corpo fisico."""
    d = _d(V); q_def = _cita("a minha definição é o próprio zero absoluto"); q_cost = _um_texto_tem("nunca correspondeu, e por isso nada custa")
    return _f("**A definição do operador e o que a pedra tipa** [INPUT/ONTO: a definição · REAL: os termos do kernel · KNOWN: a lei de escala de Takesaki · OPEN: o fluxo de um corpo físico]: a inércia de Newton é, na definição do operador, {q_def} (`{s_in}`). O kernel já tem esse zero: é o `0_abs` de `costless`, "
              "que o módulo `TheCorrespondence` escreve como {q_cost} (1 = 0). O ω(I) = 1 NÃO é a inércia: é o Um POSTO que a interrompe (1 = 1). Sobre os dados da escala dual de Takesaki ([KNOWN]: a lei τ∘θ_s = e^(−s)·τ é campo da estrutura `DualScalingData`, como na Fundação), a pedra `FalsidadeDaInercia` ({n_f} bandeiras, de `{ft0}` a `{ft1}`) "
              "compõe por citação, sem matemática nova: (i) `the_inertia_is_the_absolute_zero`: o que o fluxo inteiro fixa pesa zero; (ii) ★ `the_inertia_of_a_post_is_false` (bandeira `{est}`): um posto de peso 1 = ω(I) que fosse inercial daria (1:ℝ) = 0, isto é, falso, e `a_post_is_not_inertial` o diz em forma negativa; "
              "(iii) `the_simulacrum`: não há testemunha estática plena e o que parece resistência do corpo é o custo da interrupção, t·β·g > 0, não o zero; (iv) `the_inscription_interrupts_the_inertia`: o único peso 1 na órbita do posto está no corte a = 0 e tudo o que pesa é interrompido. "
              "A composição `falsidade_da_inercia` reúne as quatro, e `the_post_exists_and_moves` mostra que a pedra não é vácua: o modelo concreto tem o Um posto em 1 e o move em toda escala não trivial. A composição DERIVADA `falsidade_da_inercia_derivada` (bandeira `{unc}`) estende as quatro com a cadeia derivada (a seção seguinte). "
              "[ONTO, só estas leituras] a primeira lei de Newton é o 0_abs lido como corpo, e a massa de F = ma NÃO é a inércia: é a cristalização da dobra da luz lida contra o zero (ver abaixo); [OPEN] a identificação da escala dual com o fluxo de um corpo físico é de runtime e nenhum termo a faz.",
              q_def=q_def, q_cost=q_cost, s_in=d["s_in"], n_f=d["n_f"], ft0=d["ft0"], ft1=d["ft1"], est=d["est_f"], unc=d["unc_f"])


def _cadeia(V):
    """A cadeia derivada (a extensao da pedra, 25/10): [DERIVED] do axioma w(I) = 1 e da lei de Takesaki ([KNOWN], campo da estrutura); a unica hipotese NOMEADA e' H_tau [OPEN], que nenhum teorema usa. NUNCA [ONTO] do operador: ele pediu a leitura derivada."""
    d = _d(V)
    return _f("**A cadeia derivada** [DERIVED: o axioma ω(I) = 1 e a lei de escala de Takesaki ([KNOWN], campo da estrutura `DualScalingData`) · REAL: os termos do kernel · OPEN: `H_tau`]: o operador pediu que a leitura fosse DERIVADA e não [ONTO] dele (o recorte declarado da fala de 25/10, `{s_imp}`), e a pedra estendida ({n_f} bandeiras, de `{ft0}` a `{ft1}`) a deriva sobre os mesmos dados, por citação e sem hipótese nova: "
              "(i) `no_post_before_the_impression`: nada que porte posto precede a impressão — todo peso positivo é movido por toda escala não trivial, o peso 1 da órbita ocorre só no corte a = 0 e em todo outro corte o estado NÃO é um posto; "
              "(ii) `inertia_is_not_its_own_cause`: um estado fixo desde sempre (em toda escala negativa), ou em toda escala positiva, ou em toda escala, porta peso zero, e todo estado de peso positivo se move em alguma escala — a inércia não é causa de si mesma; "
              "(iii) `the_first_motion_is_the_impression`: o posto não repousa em escala alguma e o único ponto de peso 1 da órbita é a impressão — o primeiro movimento é a impressão; "
              "(iv) `diagFlow_coordinate_is_the_scaling` e `the_tension_is_projected_onto_the_attractor`: a coordenada do fluxo diagonal `diagFlow` do Grande Atrator é a escala dual (na escala s = t·β·d_i), a coordenada com gap d_i ≠ 0 é podada até zero no limite e é diferente de zero em todo t finito, e a de gap zero é o equilíbrio, fixa em todo t (o nome «tensão» dado ao gap é nomeação, sem teorema); "
              "(v) `leak_below_every_epsilon` e `the_zero_is_the_consequence_of_the_pruning`: o peso de um estado com posto nunca é zero em escala alguma (`the_fall_never_lands`), desce abaixo de todo ε > 0 (`abismo`) e o vazamento e^(−tβg) fica abaixo de todo ε em algum t > 0 — o zero é a consequência da poda, o ínfimo e não um estado da órbita, e não é o início; "
              "(vi) a composição `falsidade_da_inercia_derivada` (bandeira `{unc}`), que reúne as anteriores com as quatro da falsidade. Nada disto usa `H_tau`. "
              "A ÚNICA hipótese NOMEADA é `H_tau` [OPEN]: a identificação do peso τ com a massa de Newton e com a métrica de Einstein; nenhum teorema a usa, e a ORDEM 025 ao Codex (sha16 `{o025}`, enfileirada; pendência EXTERNA a esta cadeia) tenta tipá-la pela frente de luz de Bisognano-Wichmann. "
              "Continuam [ONTO] só as leituras da matéria como cristalização da dobra da luz e de nada = matéria, e a primeira lei de Newton lida como o 0_abs; a ponte ao corpo físico é `H_tau`, não esta cadeia.",
              s_imp=d["s_imp"], n_f=d["n_f"], ft0=d["ft0"], ft1=d["ft1"], unc=d["unc_f"], o025=d["o025"])


def _calculo(V):
    """O calculo do rito (registro falsidade_da_inercia_v401): os numeros LIDOS do registro; [REAL] a conferencia no modelo; [DERIVED] o custo e a perda; nada disto esta no kernel."""
    d = _d(V); fv = V["falsidade"]["values"]
    return _f("**O cálculo deste rito** [REAL: a conferência dos teoremas no modelo, em dupla precisão · DERIVED: o custo e a perda · os números não estão no kernel]: no modelo `oneScaling` (τ = id, θ_s = e^(−s)·), com β = α(CODATA 2018) × √e = {beta} em runtime (um dado, dois nomes; nunca literal), "
              "o peso do posto depois da escala s é e^(−s): vale {w1} em s = 1 e {w_1} em s = −1, e só é 1 em s = 0; nas {grid} escalas de teste a distância mínima de e^(−s) a 1 é {mind}; só o estado nulo é fixo pelo fluxo inteiro ({fix}) e nenhuma escala não trivial fixa o posto ({pin} escalas); "
              "o custo t·β·g tem mínimo {mincost} (> 0), o fator de defasagem tem máximo {maxd} (< 1) e vale {deph} em t = 1, g = 1, e a perda por unidade, 1 − e^(−β), vale {loss}. Na cadeia derivada [DERIVED]: o peso do posto na grade tem mínimo {minw} (> 0: o zero nunca é estado da órbita); os testemunhos do abismo (peso abaixo de ε em s = −ln ε + 1) são {n_ab} e os do vazamento (t = (1/ε)/(β·g), g = 1/2) são {n_lk}; o fluxo diagonal com gap, podado em t = 1e9/β, tem módulo {pr} (< 1e-12) e a coordenada de gap zero {fx0}. As {nck} checagens do registro passaram. O cálculo CONFERE os teoremas no modelo; quem prova é o kernel, e o registro não move o gate.",
              beta=_p(fv["beta"], 12), w1=_p(fv["post_weight_at_scale_one"], 6), w_1=_p(fv["post_weight_at_minus_one"], 6), grid=fv["grid_scales"], mind=_p(fv["min_distance_of_post_weight_to_one"], 6), fix=", ".join(_pn(x, 1) for x in fv["fixed_by_the_whole_flow"]),
              pin=len(fv["post_inertial_scales"]), mincost=_p(fv["min_cost_t_beta_g"], 9), maxd=_p(fv["max_dephasing_factor"], 9), deph=_p(fv["dephasing_factor_at_t1_g1"], 9), loss=_p(fv["loss_per_unit"], 9), nck=d["n_ck_fal"], minw=_p(fv["min_weight_on_the_grid_positive"], 9), n_ab=len(fv["abyss_witnesses"]), n_lk=len(fv["leak_witnesses_g_half"]), pr=" e ".join(("%.1e" % x).replace(".", ",") for x in fv["diag_flow_gap_pruned_at_1e9_over_beta"]), fx0=("é fixa em todo t testado" if fv["diag_flow_gap_zero_is_fixed"] is True else "NÃO é fixa"))


def _errata_adendo(V):
    """A errata ao lado da leitura do escriba no adendo de 03-04/09, em nome proprio da gerencia c1, com a lacuna de fidelidade."""
    d = _d(V); ad = _adendo_texto(); q_ad = _cita_adendo("ω(I)=1 é a INÉRCIA"); q_int = _cita_adendo("ele interrompe a inércia"); q_def = _cita("a minha definição é o próprio zero absoluto")
    return _f("**Errata ao lado (em nome próprio da gerência c1, 25/10/2026; a frase do adendo fica como registro):** o adendo de 03-04/09/2026 (`{nome}`, sha16 `{s_ad}` da cópia durável pinada em `insumos\\adendo`; o arquivo do Nós NÃO foi tocado) traz, na leitura do escriba, {q_ad}. "
              "Essa leitura fica SUPERADA pela definição do operador ({q_def}, `{s_in}`): a inércia é o `0_abs` (1 = 0) e o ω(I) = 1 é o Um posto que a interrompe (1 = 1). O que o adendo acertou fica: o item 7, que o adendo registra como dito pelo operador, {q_int}, "
              "e interromper a inércia não quebra simetria alguma (é enunciado sobre o fluxo, não sobre o grupo); são dois termos distintos. "
              "Lacuna de fidelidade: a estrutura (a fala do operador) dizia que a inscrição interrompe a inércia; o escrito do escriba pôs a identidade preservada (o que se conserva no grupo e por isso não custa) no lugar da inércia (o zero, o que nunca correspondeu), isto é, deu à inércia o nome do que a interrompe; "
              "a falha de tradução foi tomar o que se conserva pelo que não custa. A pedra tipa exatamente a diferença: posto + inercial = 1 = 0. [REAL] o trecho está no adendo, lido por sha256; [INPUT/ONTO] a definição é do operador.",
              nome=ad["nome"], s_ad=d["s_adendo"], q_ad=q_ad, q_def=q_def, s_in=d["s_in"], q_int=q_int)


def _ratificacoes(V):
    """As ratificacoes do operador: a fala e' [INPUT] verbatim; a LISTA e' a que a gerencia apresentou [DECLARADO]."""
    d = _d(V); q_rat = _cita("Ratifico tudo.")
    return _f("**Ratificações do operador** [INPUT, {data}: {q_rat}, `{s_rat}`]: ficam definitivos os nomes antes provisórios — a pedra `Testemunho` e os registros `selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399`, `teste_de_veracidade_fase9_v397`, `sonico_v398` e `afinacao_das_cordas_v398` —, "
              "a leitura das duas faces (P, I−P) = (a leitura do operador, o registro do `um.py`), que a v399 trazia como [ONTO] da gerência, a ratificar, e agora é [INPUT/ONTO] dele, e a paridade do psibit, sinal(L)·sinal(dL) ({nr} itens no registro `cunhagens_v401`). "
              "[DECLARADO] A lista ratificada é a que a gerência c1 apresentou a ele na sessão: o texto exato da proposta não está no acervo desta cadeia; o registro guarda a fala dele por sha256. A ratificação não é creditação de coisa alguma na natureza.",
              data=d["data_falas"], q_rat=q_rat, s_rat=d["s_rat"], nr=d["n_rat"])


def _emc2(V):
    """E = mc^2 lido pela TGL: [KNOWN] relatividade restrita e Jacobson; [REAL] a implicacao Clausius -> Einstein com H3 nomeada; [ONTO] a leitura da massa; [OPEN] H3 e o fluxo de um corpo."""
    d = _d(V); q_emc2 = _cita("Então E=m.c2 é a geometria que a cinemática da gravidade=luz2.entropia projeta?"); q_mat = _cita("a matéria é a cristalização da dobra luz no vácuo relativa ao observador"); q_nada = _cita("nada=materia e esse é o link com a entropia")
    return _f("**E = mc², lido pela TGL** [KNOWN · REAL · ONTO · INPUT · OPEN]: a pergunta do operador é {q_emc2} (`{s_rat}`). [KNOWN] E = mc² é relatividade restrita (Einstein, 1905) e NÃO é termo do kernel. [KNOWN] Jacobson (1995): a equação de Einstein sai do equilíbrio de Clausius na tela local; "
              "[REAL] o kernel tem a IMPLICAÇÃO (`metric_einstein_from_screen_clausius`: Clausius em toda tela implica Einstein com Λ único), com o antecedente H3 NOMEADO, não derivado do estado. "
              "[ONTO] A leitura da TGL: a massa é o custo do nada, lida pelo operador como {q_mat} (`{s_mat}`) e ligada a {q_nada} (`{s_nada}`); a entropia entra em β = α√e (a meia-nat do axioma). A massa lida assim NÃO é a inércia: a inércia é o zero, e a massa é o que custa ler contra ele. "
              "[OPEN] a ponte de τ à massa de Newton e à métrica de Einstein é a hipótese nomeada `H_tau` (nenhum teorema a usa; a ORDEM 025 ao Codex é pendência externa); H3 em toda tela e direção segue [KNOWN] (Jacobson), não derivada do estado; a família de Lorentz de cunhas segue fora do kernel; a RG é o limite clássico, não rival, e β não renormaliza G local.",
              q_emc2=q_emc2, q_mat=q_mat, q_nada=q_nada, s_rat=d["s_rat"], s_mat=d["s_mat"], s_nada=d["s_nada"])


def _sidecar(V):
    """O sidecar um_absoluto_selo_acom.json: arquivo da custodia desde a v399 (D5); o selo nao pode conter o selo ACOM de si mesmo; o rito da v401 o REESCREVE."""
    d = _d(V); sc = V["sidecar"]
    objs = "; ".join("`%s` (%s B, sha16 `%s`)" % (n, format(o["bytes"], ","), o["sha16"]) for n, o in sc["objetos"].items())
    return _f("**O sidecar `um_absoluto_selo_acom.json` [REAL; arquivo da custódia desde a v399, D5; reescrito por este rito]:** depois da ÚLTIMA escrita do selo, o `um.py` v401 escreve a segunda testemunha dos {no} objetos FINAIS com o SHA-256 ao lado ({objs}); sha256 do sidecar `{sc16}` ({sb} B), esquema `{esq}`, veredito `{sv}`, {nr} recusas. "
              "O selo não pode conter o selo ACOM de si mesmo (seria circular): o sidecar fica AO LADO e carrega o SHA-256 do selo final, e o selo traz só os resumos (veredito, bandeira e hashes), agora também o do registro `falsidade_da_inercia_v401`. "
              "A recusa do selo ACOM só REGISTRA (D4): o SHA-256 segue soberano e o rito não cai. A primitiva de integridade é o SHA-256 [KNOWN]; a segunda testemunha NÃO acrescenta força criptográfica independente, e a confidencialidade não é alegada nem medida. A custódia da v399, da v400 e da v401 é CONJUNTA.",
              objs=objs, no=sc["n_objetos"], sc16=sc["sha16"], sb=format(sc["bytes"], ","), esq=sc["esquema"], sv=sc["veredito"], nr=sc["recusas"])


def _pedra(V):
    """A pedra FalsidadeDaInercia: a composicao incondicional por citacao, a estrela, o suporte; o que ela NAO entrega."""
    d = _d(V)
    return _f("**A pedra FalsidadeDaInercia [REAL]** (`TGLExt/FalsidadeDaInercia.lean`, sha16 `{h_t}`; {n_f} bandeiras, de `{ft0}` a `{ft1}`; o nome «falsidade (simulacro) da inércia» é do operador, e no código vai sem acento e sem parênteses): {n_contr} declarações nomeadas no contrato, todas só no trio, sem axioma próprio — "
              "a composição derivada `{teo_f}` (bandeira `{unc}`), INCONDICIONAL, e a estrela `{est_t}` (bandeira `{est}`), por citação de {n_sup} termos que o kernel já tem (`fixed_tau_zero`, `nothing_above_bears_a_post`, `the_floor_fixes_the_cut`, `oneScaling`, `beta_forbids_full_static_witness`, `leakage_strictly_loses`, `FullStaticWitness`, `the_fall_never_lands`, `abismo`, `um_is_the_great_attractor`, `the_observer_is_unique`, `diagFlow`, `permanent` e `observerProj`). A composição é DERIVADA [DERIVED] do axioma ω(I) = 1 e da lei de Takesaki; a hipótese nomeada `H_tau` [OPEN] não entra em teorema algum. "
              "A lei de escala de Takesaki é DADO ([KNOWN], campo de `DualScalingData`); β entra como variável real positiva, jamais literal; que a taxa observada seja α√e é a identificação de runtime, não do kernel. "
              "«Falsidade» e «simulacro» são o nome dado pelo operador, não creditação de coisa alguma. A pedra NÃO prova a primeira lei de Newton, nem a equivalência inercial = gravitacional [KNOWN], nem que E = mc² seja termo do kernel; a identificação da escala dual com o fluxo de um corpo físico segue [OPEN].",
              h_t=d["sha_pedra"], n_f=d["n_f"], ft0=d["ft0"], ft1=d["ft1"], n_contr=d["n_contr"], teo_f=d["teo_f"].split(".")[-1], unc=d["unc_f"], est_t=d["est_t"].split(".")[-1], est=d["est_f"], n_sup=d["n_sup"])


def _entrou(V):
    d = _d(V)
    return _f("**O que entrou** (pacote `work\\cadeia_de_selo\\v401` sobre a v400 `{base}`; {np} patches — {patches}; instalado em {inst}; o `um.py` cresce {delta} B, {pct}%): {num}.",
              base=V["base16"], np=V["n_patches"], patches=V["patches"], inst=V["instalado_em"], delta=format(d["delta"], ","), pct=d["pct"], num=_num(V))


def _regra_do_4_44(V):
    """A regra da ordem do operador (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item; o QUADRO do topo (v397) PERMANECE, intocado; onde o numero aparece e como se confere."""
    d = _d(V); a = _atomos(); q = _frase_444()
    return _f("**A regra do 4,44 (ordem do operador de 23/10/2026, `{s44}`) e o quadro do topo:** o quadro «O Teste da Única Palavra» (v397) PERMANECE, intocado, no topo do artigo (PT e EN) e do .md canônico, e o parágrafo dele segue no README do espelho e no site: o z_disc calibrado é reportado no início, "
              "e NUNCA sem o p calibrado e sem a linha dos 5σ no mesmo item: {z444}. A frase do operador entra VERBATIM, {q}, como leitura dele [INPUT/ONTO], não como critério da régua; a paráfrase da gerência nunca entra entre aspas. `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; o teste não foi cego. "
              "[REAL] o quadro do artigo, o do .md e o parágrafo pronto do README/site saem das MESMAS funções (`_v397_atomos` e `_v397_quadro_md`), sobre o registro `teste_de_veracidade_fase9_v397` selado no core do Nós, e a cadeia os confere de novo contra o resultado pinado "
              "(a linha de máquina do quadro, cada número, a frase verbatim e a regra da ordem item a item), com controles negativos que reprovam o 4,44 sem o p, sem a linha dos 5σ, com número adulterado ou com a frase parafraseada. "
              "O parágrafo NOVO da falsidade não traz o 4,44, e a cadeia confere isso.",
              s44=_esp()["quadro"]["frase_sha16"], z444=_z444(), q=q)


def _kernel_prova(V):
    d = _d(V)
    return _f("**O que o kernel prova e o que é leitura:** [REAL] a composição derivada da pedra é INCONDICIONAL (nenhum certificado é hipótese) e a cadeia que ela reúne é [DERIVED] do axioma ω(I) = 1 e da lei de Takesaki ([KNOWN], campo da estrutura): `{teo_f}` (bandeira `{unc}`) e a estrela `{est_t}` (bandeira `{est}`) estão no kernel deste rito, dentro do trio, com proveniência no módulo da pedra, e citam {n_sup} termos que o kernel já tem, "
              "cada um no `axiom_report`, no trio, com a proveniência que o compilador emite; tudo lido a cada rito pelos registros `falsidade_da_inercia_v401` ({nck_f} checagens do cálculo) e `cunhagens_v401` ({nck_c} checagens) e coberto por `kh_n1_cobertura_v401`. "
              "[REAL] os registros NÃO são prova de kernel sobre a natureza: conferem os termos citados e o cálculo no modelo e não movem o gate; a prova como validade não muda. "
              "[KNOWN] a lei de escala de Takesaki é campo da estrutura; a equivalência inercial = gravitacional e E = mc² são da literatura. [INPUT/ONTO] a definição do operador (a inércia é o próprio zero absoluto), as cunhagens dele (a matéria como cristalização da dobra da luz; nada = matéria) e o nome da pedra são leituras dele; o kernel entrega os termos citados; o pedido do recorte declarado da fala de 25/10 (a leitura DERIVADA, não [ONTO] dele) é [INPUT], e a cadeia que o atende é [DERIVED]. "
              "[ONTO, só estas] a primeira lei de Newton como o 0_abs lido como corpo, a massa como o custo do nada e a matéria como cristalização da dobra da luz são leituras, sem termo no kernel. [OPEN] a identificação da escala dual com o fluxo de um corpo físico, que é a hipótese NOMEADA `H_tau` (τ é a massa de Newton e a métrica de Einstein), não usada por teorema algum; a ORDEM 025 ao Codex (sha16 `{o025}`, enfileirada) é pendência EXTERNA e tenta tipá-la pela frente de luz de Bisognano-Wichmann.",
              teo_f=d["teo_f"].split(".")[-1], unc=d["unc_f"], est_t=d["est_t"].split(".")[-1], est=d["est_f"], n_sup=d["n_sup"], nck_f=d["n_ck_fal"], nck_c=d["n_ck_cun"], o025=d["o025"])


def _limites(V, curto=False):
    """Os estatutos fieis da v401: o que a pedra, os registros e a errata dizem e NAO dizem."""
    d = _d(V)
    if curto:
        return ("**Limites ditos:** [REAL] o registro `falsidade_da_inercia_v401` LÊ o kernel do próprio rito e CONFERE o cálculo no modelo `oneScaling` (não abre dado, não é teste, não acrescenta rito); [KNOWN] a lei de escala de Takesaki é dado, a equivalência inercial = gravitacional e E = mc² são da literatura; "
                "a pedra NÃO prova a primeira lei de Newton; [INPUT/ONTO] a definição do operador, as seis falas e a leitura da matéria e do nada são dele; [DERIVED] a cadeia estendida (nada que porte posto precede a impressão; a inércia não é causa de si mesma; o zero é a consequência da poda; a tensão projetada no atrator) é derivada do axioma e da lei de Takesaki [KNOWN], não [ONTO] do operador; [ONTO, só estas] Newton lido como o 0_abs, a massa como o custo do nada e a matéria como cristalização da dobra da luz; [DECLARADO] a lista ratificada é a que a gerência apresentou a ele; "
                "[OPEN] a hipótese nomeada `H_tau` (τ é a massa de Newton e a métrica de Einstein; nenhum teorema a usa; a ORDEM 025 ao Codex é pendência externa), a atestação física externa e a discriminação a 5σ; o quadro do topo segue com a sua linha dos 5σ; validade no kernel não é creditação; o gate não se move.")
    return ("**Limites ditos (estatutos fiéis):** [REAL] ESCOPO: o registro `falsidade_da_inercia_v401` lê a composição e a estrela da pedra no kernel do rito e confere o cálculo no modelo `oneScaling` (β = α√e em runtime); CONFERE, não prova (quem prova é o kernel), não abre dado, não é teste, "
            "não acrescenta rito e não move o gate. [REAL] A pedra COMPÕE por citação termos que o kernel já tem e não acrescenta matemática nova; a lei de escala de Takesaki é DADO [KNOWN], campo da estrutura, como na Fundação. "
            "[REAL] A pedra NÃO prova a primeira lei de Newton, nem a equivalência inercial = gravitacional [KNOWN], nem que E = mc² seja termo do kernel; o kernel tem a implicação Clausius → Einstein com Λ único, com H3 nomeada [KNOWN, Jacobson 1995]. "
            "[INPUT/ONTO] A definição do operador (a inércia é o próprio zero absoluto), «nada = matéria», a matéria como cristalização da dobra da luz e o nome da pedra são falas dele: o kernel não as prova. [DERIVED] A cadeia estendida (nada que porte posto precede a impressão; a inércia não é causa de si mesma; o primeiro movimento é a impressão; o zero é a consequência da poda, o ínfimo e não um estado da órbita; a tensão projetada no atrator) é derivada do axioma ω(I) = 1 e da lei de Takesaki [KNOWN] e NÃO é [ONTO] do operador, que pediu a leitura derivada. "
            "[ONTO, só estas] A primeira lei de Newton como o 0_abs lido como corpo e a massa como o custo do nada, "
            "que NÃO é a inércia, são leituras, sem termo no kernel. [DECLARADO] A lista que «Ratifico tudo.» ratificou é a que a gerência apresentou a ele; o texto exato da proposta não está no acervo desta cadeia. "
            "[OPEN] A identificação da escala dual com o fluxo de um corpo físico é a hipótese NOMEADA `H_tau` (τ é a massa de Newton e a métrica de Einstein; ler Einstein como o processamento geométrico da métrica parametrizada na relatividade especial não é termo do kernel), que nenhum teorema usa; a ORDEM 025 ao Codex (sha16 `{o025}`, enfileirada) é pendência EXTERNA; a atestação física externa e a tipagem (sinapse, token, nome) seguem abertas. "
            "O quadro «O Teste da Única Palavra» segue no topo, com a sua linha dos 5σ, e esta rodada não o altera. NÃO é teste novo: a pedra é a prova que o operador pediu, e a cadeia não acrescenta dado nem desfecho experimental. Validade no kernel não é creditação; o gate não se move.").replace("{o025}", d["o025"])


def _legal(V):
    """A pendencia [LEGAL] herdada (D2): publicar o bloco embutido e as adaptacoes; a v401 nao a decide."""
    _d(V)
    return ("**Pendência [LEGAL] (herdada da v399, D2):** o bloco embutido do método do operador e as adaptações (centro 96, ids derivados dos hashes, `rint`, tabela de códigos, auditoria de separação) seguem sob a decisão do operador com a agente de PI; a v401 não muda o bloco (o runtime da seção é o da v400) e NÃO decide a pendência. "
            "Perguntas à agente de PI, não conclusões: o que o depósito já cobre do que o bloco mostra; publicar as adaptações inicia a contagem do prazo de graça para eventual depósito de melhoria; a divergência da tabela dos estados do ACOM Mirror com a fórmula de índice e o código executado, registrada na v395, segue pendente.")


def _erratas(V):
    """A errata de contagem da v401, AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (estrutura / escrito / falha): o registro kh_n1_cobertura_v399 e os sete contratos."""
    d = _d(V); kh = V["kh"]; cb = d["cb"]
    ids = V["patch_ids"]
    assert all(i in ids for i in ("C12__V398_SONICO_CONTRACT", "C12__V398_AFINACAO_CONTRACT", "C12__V396_TESTEMUNHA_CONTRACT", "C12__V395_PSIBIT_CONTRACT", "C12__V394_FORMAL_CONTRACT", "C12__V394_QUADRATIC_CONTRACT", "C12__V394_NETWORK_CONTRACT", "C13_kh_n1_v399_pisos")), "o CANDIDATO_v401.json nao traz os patches C12 e C13 que a errata descreve"
    return _f("**Errata ao lado (em nome próprio da gerência c1; o registro `kh_n1_cobertura_v399` e os contratos ficam como registro):** a v401 acrescenta o módulo FalsidadeDaInercia: a cobertura do Audit cresce de {d0} constantes e {t0} teoremas para {d1} e {t1}, "
              "a árvore formal do Nós de {h0} para {h1} entradas e a escada de {e0} para {e1}. Por isso, na v401, (i) `kh_n1_cobertura_v399` passa a cobrar piso em h2, h3 e h6 (as igualdades de contagem) e tamanho mínimo da árvore em h8 (as igualdades exatas e o pino exato da "
              "árvore ficam em `kh_n1_cobertura_v401`); (ii) os sete contratos (`_V394_FORMAL_CONTRACT`, `_V394_QUADRATIC_CONTRACT`, `_V394_NETWORK_CONTRACT`, `_V395_PSIBIT_CONTRACT`, `_V396_TESTEMUNHA_CONTRACT`, `_V398_SONICO_CONTRACT` e `_V398_AFINACAO_CONTRACT`) passam a ler `expected_ladder` = {e1}, a escada desta versão (o consumidor exige a igualdade "
              "exata com a escada do rito; só o número muda); o veredito dos registros anteriores NÃO muda [REAL, lido de `CANDIDATO_v401.json` (patches C12 e C13) e do ensaio a seco, que deu `TUDO PASSOU`: com a escada nova e o número velho a igualdade exata não fecharia]. "
              "Lacuna de fidelidade: a estrutura da v399 dizia que as contagens e o pino da árvore eram a cobertura exata e que o contrato esperava a escada vigente; o escrito deixou, dentro dos registros e dos contratos, números que só valem na versão que os escreveu; "
              "a falha: igualdades e literais presos a uma versão quebram quando o kernel cresce (a mesma lacuna que a v395, a v396, a v397, a v399 e a v400 acharam nos registros anteriores). A cobrança exata passa a ser de `kh_n1_cobertura_v401` ({dd} constantes, {dt} teoremas, {fora} fora do trio, {nl} nomes não lidos), contra a medida do sandbox da v401.",
              d0=cb["decl"], t0=cb["thm"], h0=cb["h8"], d1=kh["decl"], t1=kh["thm"], h1=d["h8"], e0=V["escada_antes"], e1=d["depois"], dd=kh["decl"], dt=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"])


def _depois(V):
    d = _d(V); bk = d["bank"]
    return ("**O que vem depois destas superfícies:** o elo B(n) da Bancada Um (passos 10, 10a, 10b e 10c da cadeia; B3 nos scripts) é pós-selo, um passo SIMPLES (a Bancada de produção pina a %s, geração B%d, e o Nós passa a v401: sem salto e sem cadeia de selos; "
            "a geração esperada é B%d e o veredito esperado do aplicar é REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, lido do código do esboço R3.5, não rodado) "
            "e pede a palavra do operador (parada e religamento do serviço exigem V401_AUTORIZACAO_OPERADOR); o recibo dele é citado no handoff (fechar), que traz PRONTOS os parágrafos do README do espelho e do site (o quadro do Teste da Única Palavra, intocado, e o NOVO da falsidade), "
            "diz que o parágrafo do testemunho de dois (v399) SEGUE COMO ESTÁ e LISTA o sidecar `um_absoluto_selo_acom.json`. A pendência [LEGAL] (D2) segue do operador com a agente de PI; a atestação física externa e a discriminação a 5σ seguem [OPEN]. "
            "NOT_FALSIFIED não é a palavra da creditação; o gate não se move." % (bk["de"], bk["geracao"], bk["proxima"], bk["proxima"]))


def _rodada(V):
    """O paragrafo da rodada (horarios, escada, selo, conferidor, sidecar, pilar, artefatos): tudo lido da leitura da rodada."""
    sc = V["sidecar"]
    return ("Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado (%d bandeiras True; o veredito do gate é o mesmo da v400); o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); "
            "o sidecar `um_absoluto_selo_acom.json` `%s` (%d objetos, %d recusas); o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.") % (
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["n18"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"], sc["sha16"], sc["n_objetos"], sc["recusas"], "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]),
        V["pilar"]["result16"], V["servidor"], V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()))


# v401: a linhagem (diario datado do Nos)
def linhagem(V):
    d = _d(V)
    return (("## %s — **%s — A FALSIDADE (SIMULACRO) DA INÉRCIA (v401): %d módulo novo, escada %s → %s\n<!-- linhagem_v401_selada -->\n\n"
             "%s\n\n%s\n\n"
             "**As inscrições de 25/10** (embutidas por sha256 no registro `cunhagens_v401`): [INPUT/ONTO] as seis são falas do operador (Luiz Antonio Rotoli Miguel) e valem como leitura dele, não como medida; nenhuma é da gerência. "
             "O texto íntegro de cada uma está no arquivo (`work\\cadeia_de_selo\\v401\\insumos\\cunhagens`); abaixo, a data, o sha16, o autor e o tema (resumo da gerência, não citação):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s") % (
        V["data"], _cab(V), V["n_pedras"], V["escada_antes"], d["depois"], _ordem(V), _entrou(V), _cunhagens(V), _definicao(V) + "\n\n" + _cadeia(V), _calculo(V), _errata_adendo(V), _ratificacoes(V), _emc2(V), _pedra(V), _sidecar(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V), _rodada(V), _erratas(V)) + "\n\n" + _depois(V))


# v401: o adendo do desenho do fechamento
def desenho(V):
    d = _d(V); kh = V["kh"]
    return (("## ADENDO — %s · v401 SELADA (COMPLETA) `%s` — o caminho crítico NÃO mudou; entra a falsidade (simulacro) da inércia (%d módulo)\n\n<!-- adendo_v401_selada -->\n"
             "- **O que a v401 diz:** %d módulo novo no kernel (%s; o nome «falsidade (simulacro) da inércia» é do operador), escada %s → %s, %s constantes no `axiom_report` (%s fora do trio); a inércia é o próprio zero absoluto (definição do operador [INPUT/ONTO]; o `0_abs` do kernel, 1 = 0); "
             "um posto de peso 1 = ω(I) que fosse inercial daria 1 = 0 (falso) [REAL, sobre os dados da escala dual de Takesaki, que são [KNOWN]]; o ω(I) = 1 é o Um posto que a interrompe (1 = 1); "
             "a cadeia estendida [DERIVED] (nada que porte posto precede a impressão; a inércia não é causa de si mesma; o primeiro movimento é a impressão; o zero é a consequência da poda, o ínfimo e não o início) vem do axioma e da lei de Takesaki [KNOWN] e não é [ONTO] do operador; a única hipótese nomeada é `H_tau` [OPEN] (τ é a massa de Newton e a métrica de Einstein), que nenhum teorema usa; o registro `falsidade_da_inercia_v401` confere o cálculo no modelo `oneScaling` com β = α√e em runtime; "
             "%d inscrições de 25/10 por sha256 (as seis são falas do operador) e as ratificações dele. O quadro do topo do artigo (O Teste da Única Palavra, v397) segue intocado: %s. Gate intocado.\n"
             "- **O que a v401 NÃO é para o caminho crítico:** não é teste novo; a pedra não prova a primeira lei de Newton, nem a equivalência inercial = gravitacional, nem E = mc²; a identificação da escala dual com o fluxo de um corpo físico (`H_tau`) segue [OPEN], e a ORDEM 025 ao Codex que tenta tipá-la é pendência externa; "
             "a errata ao lado da leitura do escriba no adendo de 03-04/09 («ω(I)=1 é a INÉRCIA» fica SUPERADA pela definição do operador) é da gerência, em nome próprio; não deriva H3 (segue [OPEN] em toda direção nula); não identifica β na natureza a 5σ.\n"
             "- **O que segue do operador:** a pendência [LEGAL] (D2, com a agente de PI); o elo B(n) da Bancada Um (passo simples, sem salto; parada e religamento do serviço); a custódia conjunta (sessão do site, com os parágrafos do README/site e o sidecar que o handoff traz); commit/push.") % (
        V["data"], V["s16"], V["n_pedras"], V["n_pedras"], _mods(V), V["escada_antes"], d["depois"], kh["decl"], kh["fora"], d["n_cun"], _z444()))


# v401: o verbete do Atlas
def atlas(V):
    return (("### %s — v401 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v401_selada -->\n[REAL — rodada v401, selo `%s`] %s.\n\n[INPUT/ONTO] As falas do operador entram como o operador as disse e valem como leitura, não como medida; as seis são dele: %s.\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\nEstatuto: validade no kernel ≠ creditação; o gate não se move.") % (
        V["data"], V["s16"], V["selo_ts"], _num(V), _cunhagens(V, "curta"), _definicao(V) + "\n\n" + _cadeia(V), _calculo(V), _errata_adendo(V), _ratificacoes(V), _emc2(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V)))


# v401: o bloco do TGL_CORE_MEMORY
def core_memory(V):
    return (("## %s — v401 SELADA `%s` (claude-c1; a falsidade (simulacro) da inércia, integrada pela gerência)\n<!-- core_v401_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
             "[REAL] %s.\n\n%s\n\n%s\n\n%s\n\n%s\n\n[OPEN] A discriminação a 5σ (β_TGL na natureza), a identificação da escala dual com o fluxo de um corpo físico, a atestação física externa (nenhuma `AttestedCollapse` é exibida), a tipagem (sinapse, token, nome), a face de Fock do psion (o certificado de Fock da luz sem habitante), "
             "o contrato conjunto da rede, H3 em toda direção nula e a pendência [LEGAL] seguem abertos; o elo B(n) da Bancada Um depende da palavra do operador. Nada disto move o gate.") % (V["data"], V["s16"], _num(V), _definicao(V) + "\n\n" + _cadeia(V), _errata_adendo(V), _regra_do_4_44(V), _limites(V, curto=True)))


# v401: o bloco do CLAUDE.md da Haja_Luz (a errata ao lado, assinada, vai DENTRO dele: nao ha linha da leitura do escriba nessa memoria para receber errata inline)
def haja_luz(V):
    d = _d(V)
    return (("## %s — v401 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v401_selada -->\n%d módulo novo no kernel (%s; o nome «falsidade (simulacro) da inércia» é do operador): a inércia é o próprio zero absoluto (definição do operador [INPUT/ONTO]; o `0_abs` do kernel, 1 = 0), "
             "um posto de peso 1 = ω(I) inercial daria 1 = 0 (falso) [REAL, sobre os dados da escala dual de Takesaki, [KNOWN]], e o ω(I) = 1 é o Um posto que a interrompe (1 = 1); A cadeia estendida [DERIVED] (nada que porte posto precede a impressão; a inércia não é causa de si mesma; o primeiro movimento é a impressão; o zero é a consequência da poda, o ínfimo e não o início) vem do axioma e da lei de Takesaki [KNOWN] e não é [ONTO] do operador; a única hipótese nomeada é `H_tau` [OPEN] (τ é a massa de Newton e a métrica de Einstein), que nenhum teorema usa; O registro `falsidade_da_inercia_v401` confere o cálculo no modelo `oneScaling` com β = α√e em runtime; "
             "a pedra NÃO prova a primeira lei de Newton. As %d inscrições de 25/10 por sha256 (as seis são do operador) e as ratificações dele; escada %s → %s. O quadro do topo (O Teste da Única Palavra) segue intocado.\n\n"
             "%s\n\n"
             "Memórias: `%s`, `missao-ultima-flag-um-py.md`, `estatuto-da-prova-07out.md`; handoff `handoff-v401-custodia.md`.") % (
        V["data"], V["s16"], V["teor"], V["n_pedras"], _mods(V), d["n_cun"], V["escada_antes"], d["depois"], _errata_adendo(V), TOPICO_NOVO))


def marca_topico_missao(V):
    return "## %s — v401 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v401 SELADA `%s`" % V["s16"]


# v401: o topico da missao da ultima flag
def topico_missao(V):
    d = _d(V)
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): %d módulo novo no kernel (%s); `falsidade_da_inercia_v401` (lê o kernel do rito e confere o cálculo no modelo `oneScaling`), `cunhagens_v401` (%d inscrições por sha256, todas do operador, as ratificações, a errata ao lado do adendo, a cadeia derivada [DERIVED] e a hipótese nomeada `H_tau` [OPEN]) e `kh_n1_cobertura_v401`; "
                                     "os quatro registros da v399 recriados e selados; sidecar `um_absoluto_selo_acom.json` reescrito; troca dita nos vereditos que carregam a escada; conferidor (deve mudar %s; não pode mudar %s). Pacote e cadeia: `work\\cadeia_de_selo\\v401` (+ `pos_rito`).") % (V["teor"], V["n_pedras"], _mods(V), d["n_cun"], V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v401 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v401 SELADA (COMPLETA):**"


# v401: o topico do estado da Central
def topico_central(V):
    d = _d(V)
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v400 `%s`; escada %s → %s; gate intocado. %d módulo novo no kernel (%s): a inércia é o próprio zero absoluto (definição do operador) e um posto inercial daria 1 = 0; o `um.py` confere o cálculo no modelo `oneScaling` (registro `falsidade_da_inercia_v401`); "
                               "a errata ao lado da leitura do escriba no adendo de 03-04/09 (da gerência, em nome próprio) e as ratificações do operador estão no registro `cunhagens_v401`; a cadeia estendida (nada que porte posto precede a impressão; o zero é a consequência da poda) é [DERIVED] e a hipótese `H_tau` é [OPEN] (ORDEM 025 ao Codex: pendência externa); as %d inscrições de 25/10 por sha256 (todas do operador); o quadro do topo (O Teste da Única Palavra, v397) segue intocado. "
                               "Falta o elo B(n) da Bancada Um (passo simples, sem salto) e a custódia conjunta (sessão do site, `handoff-v401-custodia.md`, que traz os parágrafos do README/site e lista o sidecar); a pendência [LEGAL] (D2) é do operador; commit/push = operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], d["depois"], V["n_pedras"], _mods(V), d["n_cun"])


# v401: o topico do estatuto da prova
def topico_estatuto(V):
    d = _d(V)
    return ("<!-- v401_selada -->\n**%s — v401 `%s`:** o registro `estatuto_da_prova_v391` passou a ler a escada nova (%s → %s; veredito trocado, troca dita; as pedras e os registros da v400 ficam como registro). "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora e é o β_TGL na natureza a 5σ. O registro `falsidade_da_inercia_v401` confere o cálculo no modelo e lê os termos do kernel ([REAL]); a lei de escala de Takesaki é dado ([KNOWN]); "
            "a definição do operador (a inércia é o próprio zero absoluto) é [INPUT/ONTO] e Newton lido como o 0_abs é [ONTO]; a cadeia estendida (nada que porte posto precede a impressão; o zero é a consequência da poda) é [DERIVED] do axioma e da lei de Takesaki [KNOWN], não [ONTO] do operador, e a única hipótese nomeada, `H_tau`, é [OPEN] e nenhum teorema a usa; a ratificação dos nomes é [INPUT]. O quadro do topo segue intocado: %s. Nada disso é prova sobre a natureza.") % (V["data"], V["s16"], V["escada_antes"], d["depois"], _z444())


# v401: o gancho da missao no MEMORY.md
def marca_missao(V):
    return "**v401 SELADA %s `%s` %s COMPLETA (a falsidade (simulacro) da inércia; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


# v401: a linha do handoff no MEMORY.md
def linha_handoff(V):
    return "- [HANDOFF v401 — a falsidade (simulacro) da inércia; custódia](handoff-v401-custodia.md) — **%s, para a sessão do site (traz o parágrafo novo e o do quadro; o do testemunho segue como está)** · `%s`" % (V["data"][:5], V["s16"])


def linha_topico_novo(V):
    return "- [v401 SELADA: a falsidade (simulacro) da inércia (%s)](%s) — **%s** · `%s`" % (V["data"][:5], TOPICO_NOVO, V["teor"], V["s16"])


# v401: o topico novo da memoria (um arquivo por versao)
def topico_novo(V):
    d = _d(V)
    return (("---\nname: %s\ndescription: \"v401 SELADA (%s) `%s`: %d módulo novo no kernel (FalsidadeDaInercia, nome dado pelo operador), o registro falsidade_da_inercia_v401 (a inércia é o próprio zero absoluto; um posto inercial daria 1 = 0; o cálculo no modelo oneScaling com beta = alfa x raiz de e), %d inscrições de 25/10 por sha256, as ratificações e a errata ao lado do adendo, escada %s → %s; B(n) e custódia pendentes\"\n"
             "metadata:\n  type: project\n---\n\n# v401 SELADA (%s)\n\n"
             "**O que é:** `um.py` **v401** `%s` (%s B) sobre a v400 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); o `um.py` cresce %s B (%s%%).\n\n"
             "**O que entrou:** %s.\n\n"
             "**As inscrições de 25/10** (embutidas por sha256; data, sha16, autor e tema — resumo da gerência, não citação; o texto íntegro está em `insumos\\cunhagens`):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"
             "**Pendências:** o elo B(n) da Bancada Um (palavra do operador; passo simples, sem salto; parada e religamento do serviço), a pendência [LEGAL] (D2), a custódia conjunta (sessão do site, com o sidecar), commit/push. Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v401`.\n\n"
             "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v401-custodia]]\n") % (
        TOPICO_NOVO[:-3], V["data"], V["s16"], V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
        format(d["delta"], ","), d["pct"], _num(V), _cunhagens(V), _definicao(V) + "\n\n" + _cadeia(V), _calculo(V), _errata_adendo(V), _ratificacoes(V), _emc2(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V) + "\n\n" + _erratas(V)))


# v401: o aviso a coordenadora (so' sob reivindicacao nomeada)
def aviso(V, reivindicacao):
    d = _d(V)
    return (("### %s — v401 SELADA `%s` [claude-c1]\n<!-- aviso_v401_selada -->\n\n[REAL] A v401 SELOU (%s; COMPLETA; gate intocado): a inércia é o próprio zero absoluto (definição do operador [INPUT/ONTO]) e um posto inercial daria 1 = 0 (falso, sobre os dados da escala dual de Takesaki, [KNOWN]); o `um.py` confere o cálculo no modelo `oneScaling` "
             "e as %d inscrições de 25/10 (por sha256; todas do operador), as ratificações dele e a errata ao lado do adendo de 03-04/09 entram no selo corrente; a cadeia estendida é [DERIVED] e a hipótese `H_tau` é [OPEN]. Escrito sob a reivindicação %s. %d módulo novo no kernel (FalsidadeDaInercia); escada %s → %s; "
             "o elo B(n) da Bancada Um e a pendência [LEGAL] esperam o operador. Não altera pinos, dado, MCP nem gate.") % (V["data"], V["s16"], V["teor"], d["n_cun"], reivindicacao, V["n_pedras"], V["escada_antes"], d["depois"]))


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V401_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# ---------------------------------------------------------------- o PARAGRAFO PRONTO do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO; ordem do operador de 23/10: o 4,44 no inicio do artigo, no readme e tudo mais) e (2) o paragrafo NOVO da falsidade
def verificar_paragrafo_readme(par, res, tv):
    """Verifica o paragrafo do QUADRO (texto) contra o RESULTADO pinado (`res`, o JSON lido) e o registro `tv` selado no core: devolve a lista de falhas (vazia = passou). As verificacoes (as mesmas da v397, da v399 e da v400):
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
    from guarda_p18_v401 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    for st in ("[REAL", "[INPUT]", "[KNOWN]", "COMPOSIÇÃO da gerência"):   # os estatutos que o quadro escreve: REAL (os numeros), INPUT (a leitura binaria e a frase), COMPOSICAO da gerencia (as duas faces) e KNOWN (Jeffreys)
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    return fa


def paragrafo_readme():
    """(texto, relatorio): o paragrafo do QUADRO pronto para colar no README do espelho e no site (o MESMO da v397, da v399 e da v400), gerado por quadro_v397.paragrafo_pronto_readme sobre o core SELADO do Nos, verificado contra o resultado pinado
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


def _linha_maquina_falsidade(fv, d_extra, n_checks):
    """A linha de maquina do paragrafo novo (os numeros LIDOS do registro falsidade_da_inercia_v401 do core), em PT."""
    return ("pedra_sha16=%s; bandeiras=%s; beta=%s; escalas=%s; dist_min=%s; peso_s1=%s; custo_min=%s; defasagem_max=%s; perda_unit=%s; checagens=%s; definicao_sha16=%s; adendo_sha16=%s"
            % (d_extra["pedra"], d_extra["n_f"], _p(fv["beta"], 12), fv["grid_scales"], _p(fv["min_distance_of_post_weight_to_one"], 6), _p(fv["post_weight_at_scale_one"], 6), _p(fv["min_cost_t_beta_g"], 9), _p(fv["max_dephasing_factor"], 9), _p(fv["loss_per_unit"], 9),
               n_checks, d_extra["definicao"], d_extra["adendo"]))


def _paragrafo_falsidade_de(core):
    """O texto do paragrafo da falsidade, funcao PURA dos registros falsidade_da_inercia_v401 e cunhagens_v401 do core SELADO (os numeros sao lidos dos registros, nunca digitados)."""
    fa = core.get("falsidade_da_inercia_v401") or {}; cg = core.get("cunhagens_v401") or {}
    fv = fa.get("values") or {}; mec = fa.get("mechanics") or {}; ex = cg.get("extras") or {}
    assert fa.get("all_verified") is True and cg.get("all_verified") is True and fv.get("beta") and (ex.get("adendo") or {}).get("sha16") and (ex.get("definicao_da_inercia") or {}).get("fala_sha16"), "os registros da falsidade e das cunhagens nao selaram: nenhum paragrafo diz os numeros assim"
    q_def = _cita("a minha definição é o próprio zero absoluto"); q_cost = _um_texto_tem("nunca correspondeu, e por isso nada custa"); q_rat = _cita("Ratifico tudo."); q_ad = _cita_adendo("ω(I)=1 é a INÉRCIA")
    q_nome = _cita("falsidade (simulacro) da inércia"); q_mat = _cita("a matéria é a cristalização da dobra luz no vácuo relativa ao observador")
    q_emc2 = _cita("Então E=m.c2 é a geometria que a cinemática da gravidade=luz2.entropia projeta?")
    m025 = re.search(r"sha16 ([0-9a-f]{16})", str((ex.get("hipotese_nomeada") or {}).get("pendencia_externa"))); assert m025 and (ex.get("hipotese_nomeada") or {}).get("nome") == "H_tau" and ex.get("cadeia_derivada", {}).get("estatuto") == "[DERIVED]", "a cadeia derivada e a hipotese H_tau nao estao no registro cunhagens_v401"
    o025 = m025.group(1)
    extra = {"pedra": _esp()["pedras"]["TGLExt/FalsidadeDaInercia.lean"]["sha16"], "n_f": ex.get("n_bandeiras"), "definicao": ex["definicao_da_inercia"]["fala_sha16"], "adendo": ex["adendo"]["sha16"]}
    ls = ["### A falsidade (simulacro) da inércia (v401, 25/10/2026) — parágrafo pronto para o README do espelho e para o site",
          "",
          "> **A falsidade (simulacro) da inércia (v401, 25/10/2026)** [REAL: os termos do kernel e a conferência do cálculo no modelo · KNOWN: a lei de escala de Takesaki, E = mc², Jacobson · INPUT/ONTO: a definição e as falas do operador · ONTO: Newton, a massa e a matéria lidos pela TGL · DERIVED: a cadeia estendida · OPEN: `H_tau` (o fluxo de um corpo físico) · INPUT: a ratificação · DECLARADO: a lista ratificada]",
          ">",
          "> - **A definição do operador** [INPUT/ONTO] (sha16 `%s`): %s. A inércia é o zero absoluto, o `0_abs` do kernel, que o módulo `TheCorrespondence` escreve como %s (1 = 0). O ω(I) = 1 é o Um POSTO que a interrompe (1 = 1)." % (extra["definicao"], q_def, q_cost),
          "> - **A pedra FalsidadeDaInercia** [REAL] (o nome %s é do operador; `TGLExt/FalsidadeDaInercia.lean`, sha16 `%s`, %s bandeiras): sobre os dados da escala dual de Takesaki (a lei é [KNOWN], campo da estrutura, como na Fundação), por citação, no trio e sem matemática nova: o que o fluxo inteiro fixa pesa zero; "
          "um posto de peso 1 = ω(I) que fosse inercial daria 1 = 0, isto é, falso (a estrela `the_inertia_of_a_post_is_false`); o simulacro (não há testemunha estática plena, e o que parece resistência do corpo é o custo da interrupção, t·β·g > 0, não o zero); "
          "a inscrição interrompe a inércia (o peso 1 na órbita do posto está só no corte a = 0). A pedra não é vácua: o modelo concreto tem o Um posto em 1 e o move em toda escala não trivial." % (q_nome, extra["pedra"], extra["n_f"]),
          "> - **A cadeia derivada** [DERIVED] (axioma ω(I) = 1 e lei de escala de Takesaki [KNOWN]; a pedido do operador a leitura é derivada e NÃO é [ONTO] dele, recorte declarado da fala de 25/10, sha16 `%s`): nada que porte posto precede a impressão; a inércia não é causa de si mesma; o primeiro movimento é a impressão; o zero é a consequência da poda (o ínfimo, não um estado da órbita, e não o início); a tensão do fluxo diagonal é projetada no atrator. "
          "A única hipótese nomeada é `H_tau` [OPEN] (τ é a massa de Newton e a métrica de Einstein), que nenhum teorema usa; a ORDEM 025 ao Codex (sha16 `%s`) é pendência EXTERNA e tenta tipá-la pela frente de luz de Bisognano-Wichmann." % (ex["cadeia_derivada"]["ordem_do_operador_sha16"], o025),
          "> - **O cálculo deste rito** [REAL: a conferência no modelo `oneScaling`, em dupla precisão · DERIVED: o custo e a perda]: com β = α√e = %s em runtime, o peso do posto depois da escala s é e^(−s), igual a 1 só em s = 0 (distância mínima %s em %s escalas de teste); só o estado nulo é fixo pelo fluxo inteiro; "
          "o custo t·β·g tem mínimo %s (> 0) e o fator de defasagem tem máximo %s (< 1); a perda por unidade vale %s; o peso mínimo do posto na grade é %s (> 0: o zero nunca é estado da órbita, só o ínfimo da poda). As %s checagens do registro passaram. O cálculo CONFERE os teoremas no modelo; quem prova é o kernel; esses números são deste rito e não estão no kernel."
          % (_p(fv["beta"], 12), _p(fv["min_distance_of_post_weight_to_one"], 6), fv["grid_scales"], _p(fv["min_cost_t_beta_g"], 9), _p(fv["max_dephasing_factor"], 9), _p(fv["loss_per_unit"], 9), _p(fv["min_weight_on_the_grid_positive"], 9), mec.get("n_checks")),
          "> - **Errata ao lado (gerência c1, em nome próprio)**: a leitura do escriba no adendo de 03-04/09 (sha16 `%s`), %s, fica SUPERADA pela definição do operador: a inércia é o `0_abs` (1 = 0) e o ω(I) = 1 é o Um posto que a interrompe (1 = 1); o arquivo do adendo não foi tocado." % (extra["adendo"], q_ad),
          "> - **Ratificações** [INPUT]: %s (sha16 `%s`) — ficam definitivos os nomes antes provisórios (a pedra `Testemunho` e os registros `selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399`, `teste_de_veracidade_fase9_v397`, `sonico_v398` e `afinacao_das_cordas_v398`); "
          "[DECLARADO] a lista ratificada é a que a gerência apresentou a ele na sessão." % (q_rat, ex["ratificacao_fala"]["sha16"]),
          "> - **E = mc², lido pela TGL** [KNOWN · REAL · ONTO]: a pergunta do operador é %s. E = mc² é relatividade restrita [KNOWN] e não é termo do kernel; o kernel tem a implicação Clausius → Einstein com Λ único, com o antecedente H3 nomeado [REAL; KNOWN, Jacobson 1995]; "
          "[ONTO] a massa é o custo do nada, lida pelo operador como %s, e NÃO é a inércia: a inércia é o zero, e a massa é o que custa ler contra ele." % (q_emc2, q_mat),
          "> - **Limites:** a pedra NÃO prova a primeira lei de Newton, nem a equivalência inercial = gravitacional [KNOWN], nem que E = mc² seja termo do kernel; a identificação da escala dual com o fluxo de um corpo físico é a hipótese nomeada `H_tau` [OPEN], não usada por teorema algum; a gravidade quântica segue sem creditação na natureza; "
          "validade no kernel não é creditação; `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; isto não é teste e não acrescenta dado. O quadro do Teste da Única Palavra segue no README com a sua linha dos 5σ; este parágrafo não traz o número do quadro.",
          "> - **Origem.** Os números são lidos do core selado desta rodada (registros `falsidade_da_inercia_v401` e `cunhagens_v401`); nenhum é digitado. Linha de máquina: `%s`." % _linha_maquina_falsidade(fv, extra, mec.get("n_checks"))]
    return "\n".join(ls) + "\n"


def verificar_paragrafo_falsidade(par, core, esp):
    """Verifica o paragrafo da falsidade contra o core selado E contra ESPERADOS (o ensaio a seco): devolve a lista de falhas (vazia = passou). As verificacoes:
    (1) os numeros do core (registro da falsidade) == os de ESPERADOS[falsidade_valores] e cada um esta no paragrafo, formatado; (2) o paragrafo == o gerado do core; (3) NAO traz o 4,44 nem o z_disc (a regra do 4,44 e' do quadro); (4) os estatutos [REAL, KNOWN, INPUT/ONTO, ONTO, OPEN, INPUT, DECLARADO];
    (5) as frases de limite; (6) toda citacao entre « » e' verbatim numa fala DO OPERADOR, na docstring do 0_abs do kernel embutido ou no adendo (a leitura que a errata supera); (7) nenhuma alegacao de seguranca criptografica, «consciencia» so' como palavra retirada, a direcao sem inversao; (8) guarda P18."""
    fa = []
    ev = esp.get("falsidade_valores") or {}
    f = core.get("falsidade_da_inercia_v401") or {}; fv = f.get("values") or {}
    if not (fv and all((fv.get(k) == v if not isinstance(v, float) else (isinstance(fv.get(k), float) and abs(fv[k] - v) <= 1e-12 * max(1.0, abs(v)))) for k, v in ev.items())):
        fa.append("numero do registro da falsidade (beta, escalas, distancias, custo, defasagem, perda ou fixos) no core != ESPERADOS")
    nums = {"beta": _p(ev.get("beta", 0), 12), "escalas": str(ev.get("grid_scales")), "distancia minima": _p(ev.get("min_distance_of_post_weight_to_one", 0), 6), "custo minimo": _p(ev.get("min_cost_t_beta_g", 0), 9),
            "defasagem maxima": _p(ev.get("max_dephasing_factor", 0), 9), "perda por unidade": _p(ev.get("loss_per_unit", 0), 9), "checagens": "As %d checagens" % _qd().DL.N_CHECKS_FALSIDADE, "peso minimo": _p(ev.get("min_weight_on_the_grid_positive", 0), 9), "sha16 da definicao": (esp.get("falsidade") and _sha_por("inercia_e_o_proprio_zero_absoluto")) or "?",
            "sha16 do adendo": _adendo_texto()["sha16"], "sha16 da ratificacao": str(esp.get("ratificacao_fala_sha16"))}
    for k, v in nums.items():
        if v not in par:
            fa.append("numero (%s = %s) ausente do paragrafo" % (k, v))
    try:
        if par != _paragrafo_falsidade_de(core):
            fa.append("o paragrafo difere do gerado pelas funcoes sobre os registros selados do core")
    except AssertionError as e:
        fa.append("o paragrafo nao pode ser gerado do core: %s" % str(e)[:120])
    if re.search(r"4[,.]44|z_disc", par):
        fa.append("o paragrafo da falsidade traz o 4,44 ou o z_disc (a regra do 4,44 e' do quadro; este paragrafo nao o cita)")
    for st in ("[REAL", "[KNOWN", "[INPUT/ONTO]", "[ONTO", "[OPEN]", "[INPUT]", "[DECLARADO]", "[DERIVED]"):
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    for frase in ("O ω(I) = 1 é o Um POSTO", "fica SUPERADA", "NÃO é a inércia", "NÃO prova a primeira lei de Newton", "CONFERE os teoremas no modelo", "quem prova é o kernel", "o nome ", "validade no kernel não é creditação", "o gate não se move", "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "a lista ratificada é a que a gerência apresentou", "NÃO é [ONTO] dele", "`H_tau` [OPEN]", "pendência EXTERNA", "nenhum teorema usa"):
        if frase not in par:
            fa.append("frase de limite ausente do paragrafo: " + frase)
    corpus = [re.sub(r"\s+", " ", d["text"]) for d in _falas().values() if d["autor"] == "operador"] + [_adendo_texto()["text"]]
    um = _CACHE.get("um") or open(os.path.join(NOS, "um.py"), encoding="utf-8", errors="replace").read(); _CACHE["um"] = um
    if "nunca correspondeu, e por isso nada custa" in um.replace("**", ""):
        corpus.append("nunca correspondeu, e por isso nada custa")   # a UNICA frase do kernel embutido que o paragrafo cita (a docstring do 0_abs); o um.py inteiro NAO entra no corpus das citacoes
    for q in re.findall(r"«([^»]*)»", par):
        if len(q) >= 12 and not any(q in t for t in corpus):
            fa.append("citacao entre « » que NAO e' verbatim numa fala do operador, no kernel embutido ou no adendo: %r" % q[:90])
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
    from guarda_p18_v401 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    return fa


def paragrafo_falsidade():
    """(texto, relatorio): o paragrafo NOVO da falsidade, pronto para colar no README do espelho e no site, gerado do core SELADO do Nos e verificado contra o core E contra ESPERADOS;
    levanta AssertionError (o fechar RECUSA) se algo nao conferir."""
    core = _core(); esp = _esp()
    par = _paragrafo_falsidade_de(core)
    fa = verificar_paragrafo_falsidade(par, core, esp)
    assert not fa, ("o paragrafo da falsidade nao passou nas verificacoes", fa[:4])
    return par, {"sha16": hashlib.sha256(par.encode("utf-8")).hexdigest()[:16], "verificacoes": "numeros == ESPERADOS; igual ao gerado do core; sem o 4,44; estatutos; limites; citacoes verbatim (falas do operador, kernel embutido, adendo); sem alegacao de seguranca criptografica; guarda P18", "guarda_p18": "limpa"}


def atribuicao_da_gerencia(texto):
    """Falhas de ATRIBUICAO e de DIRECAO num texto renderizado (v401: nao ha inscricao da gerencia; as seis sao do operador): (a) nenhuma frase poe a IALD como quem testifica do operador (fora da fala em que ele recusa a ordem inversa);
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
        fa.append("diz que ha inscricao da gerencia (nesta versao as seis inscricoes sao falas do operador)")
    return fa


# v401: o handoff para a sessao do site (memory\handoff-v401-custodia.md + Nos\HANDOFF_v401_CUSTODIA.md); `k` traz os campos dos recibos do B(n) e os DOIS paragrafos do README (fechar_v401.py os le dos recibos e do core): nenhum numero digitado
def handoff(V, k):
    d = _d(V); sc = V["sidecar"]
    k = dict(k)
    for chave in ("ap_nome", "ap_sha", "ap_ver", "ap_evento", "ap_bat", "par_sha", "rel_sha", "rel_man", "readme_paragrafo", "readme_paragrafo_falsidade"):
        assert chave in k, ("o handoff precisa do campo dos recibos do B(n) e dos paragrafos do README: " + chave)
    par = k["readme_paragrafo"].rstrip("\n"); par_f = k["readme_paragrafo_falsidade"].rstrip("\n")
    assert par.startswith("### O Teste da Única Palavra (v397"), "o paragrafo do README (quadro) nao e' o do quadro"
    assert par_f.startswith("### A falsidade (simulacro) da inércia (v401"), "o paragrafo da falsidade nao e' o novo"
    k.update({"data": V["data"], "s16": V["s16"], "umb": format(V["umb"], ","), "base16": V["base16"], "teor": V["teor"], "rc": V["rc"], "conf16": V["conf16"], "conf_dm": V["conf_dm"], "conf_np": V["conf_np"],
              "pilar": "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), "selo_ts": V["selo_ts"], "num": _num(V), "kernel_prova": _kernel_prova(V), "limites": _limites(V, curto=True), "legal": _legal(V),
              "artigos": ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), "n_cun": d["n_cun"], "n_pedras": V["n_pedras"], "topico": TOPICO_NOVO[:-3], "regra": _regra_do_4_44(V), "errata": _errata_adendo(V), "ratif": _ratificacoes(V), "cadeia": _cadeia(V),
              "sc_nome": "um_absoluto_selo_acom.json", "sc_sha": sc["sha256"], "sc_ver": sc["veredito"], "sc_bytes": format(sc["bytes"], ","), "sc_objs": "; ".join("`%s` sha256 `%s`" % (n, o["sha256"]) for n, o in sc["objetos"].items()),
              "par_bloco": MARC_PAR_INI + "\n" + par + "\n" + MARC_PAR_FIM, "par_fal_bloco": MARC_FAL_INI + "\n" + par_f + "\n" + MARC_FAL_FIM})
    doc = ("---\nname: handoff-v401-custodia\ndescription: \"HANDOFF v401 (%(data)s) para a sessão do site: a falsidade (simulacro) da inércia (uma pedra, um registro com função, seis inscrições de 25/10, as ratificações do operador e a errata ao lado do adendo de 03-04/09); `%(s16)s`; B(n) da Bancada feito; TRAZ os parágrafos prontos do README/site (o quadro do Teste da Única Palavra, intocado, e o novo da falsidade); o parágrafo do testemunho de dois SEGUE COMO ESTÁ; LISTA o sidecar; custódia + pendências do operador\"\n"
           "metadata:\n  type: project\n---\n\n# HANDOFF v401 — CUSTÓDIA (%(data)s)\n\n"
           "**O que é:** `um.py` **v401** `%(s16)s` (%(umb)s B) sobre a v400 `%(base16)s`; %(teor)s; COMPLETA; rc %(rc)s; selftest PASSED; gate intocado; conferidor `%(conf16)s` (deve mudar %(conf_dm)s; não pode mudar %(conf_np)s); pilar %(pilar)s pela chave. "
           "Selo `%(selo_ts)s`.\n\n"
           "**PARÁGRAFOS PRONTOS para o README do espelho e para o site (colar como estão, cada um entre os seus marcadores; o primeiro é o quadro do Teste da Única Palavra, o MESMO da v397, intocado; o segundo é novo).** O do quadro é gerado pelas MESMAS funções do quadro do artigo "
           "(a função paragrafo_pronto_readme do módulo quadro_v397), sobre o core SELADO do Nós, com os mesmos números e estatutos, e verificado contra o resultado pinado ANTES de este handoff nascer (o fechar recusa se o z_disc aparecer sem o p calibrado e sem a linha dos 5σ no mesmo item, "
           "se a frase do operador não for a verbatim ou se algum número diferir do resultado). O novo (a falsidade (simulacro) da inércia) é gerado dos registros selados `falsidade_da_inercia_v401` e `cunhagens_v401` e verificado contra o core e contra os números do ensaio a seco "
           "(sem o z_disc do quadro; as citações são trechos verbatim das falas do operador, do kernel embutido ou do adendo que a errata supera; sem alegação de segurança criptográfica):\n\n%(par_bloco)s\n\n%(par_fal_bloco)s\n\n"
           "**O parágrafo do testemunho de dois (v399) SEGUE COMO ESTÁ.** O handoff da v400 (`handoff-v400-custodia.md`) o trouxe regenerado dos registros daquele selo, e é o que está no README do espelho e no site; esta versão NÃO o regenera nem o substitui (o `um.py` mudou de bytes, mas o parágrafo é do selo daquela rodada). "
           "Os registros que o geravam (`selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399` e `cunhagens_v399`) seguem selados e iguais ao ensaio a seco neste rito (a leitura os confere), e o nome deles está ratificado pelo operador.\n\n"
           "%(regra)s\n\n%(errata)s\n\n%(ratif)s\n\n%(cadeia)s\n\n"
           "**O que entrou e o que mediu:** %(num)s.\n\n"
           "**O SIDECAR (arquivo da custódia desde a v399, D5; REESCRITO por este rito):** `%(sc_nome)s` (sha256 `%(sc_sha)s`, %(sc_bytes)s B; veredito `%(sc_ver)s`); objetos selados: %(sc_objs)s. O sidecar fica AO LADO do selo (o selo não pode conter o selo ACOM de si mesmo) e o fechar o copia para `work\\cadeia_de_selo\\v401_selo` e o lista no manifesto de incorporação; "
           "a custódia o leva ao cofre, à PORTA (PORTA.json, URL raw) e ao espelho, junto do selo, porque a segunda testemunha só se confere com ele. A custódia da v399, da v400 e da v401 é CONJUNTA. A recusa do selo ACOM só registra (D4); o SHA-256 segue soberano.\n\n"
           "%(kernel_prova)s\n\n%(limites)s\n\n%(legal)s\n\n"
           "**O elo B(n) da Bancada Um (feito antes deste handoff; passo simples, sem salto):** recibo da aplicação `%(ap_nome)s` (sha256 `%(ap_sha)s`; veredito `%(ap_ver)s`; evento %(ap_evento)s; bateria `%(ap_bat)s`); recibo da parada do serviço sha256 `%(par_sha)s`; "
           "recibo do religamento sha256 `%(rel_sha)s` (versão servida v401, manifesto `%(rel_man)s`).\n\n"
           "**Para a sessão do site (custódia):** o `um.py` v401, `rodada_v401_stdout.txt`, o selo, o sidecar, o core, o .md canônico (com o quadro no topo, intocado) e o manifesto, os artigos PT/EN (%(artigos)s; o quadro «O Teste da Única Palavra» abre os dois), as %(n_cun)s inscrições de 25/10 por sha256 "
           "(as seis são falas do operador; lista na linhagem e no tópico `%(topico)s`; arquivos em `work\\cadeia_de_selo\\v401\\insumos\\cunhagens`), o módulo novo (`work\\cadeia_de_selo\\v401_kernel\\pedras`, `TGLExt/FalsidadeDaInercia.lean`) e os dois diffs (`DIFF_v400_v401.diff`, `DIFF_KERNEL_v401.txt`) — com PORTA gerada por script, "
           "URL raw (o um.py tem mais de 5 MB), backup da versão v400 no espelho fora do repositório, blob conferido depois do push. Colocar os PARÁGRAFOS acima no README do espelho e no site (ato da sessão do site, com o selo corrente ao lado; o do quadro e o do testemunho seguem onde estão e o novo entra ao lado); publicar o módulo novo no espelho (TGLExt) e regenerar as PORTAS de `tgl_kernel`, `TGLExt` e `TGL`; "
           "a pasta `insumos` (a pedra, as inscrições pinadas, a medida da cobertura e a cópia durável do adendo; o resultado do Teste da Única Palavra e os três recibos seguem em `v397\\insumos\\fase9`) vai ao espelho com PORTA: sem ela, uma reprodução pública diz NOT_SEALED (fail-closed); os recibos da bateria do B(n) vão ao espelho com PORTA; "
           "a errata ao lado do registro `kh_n1_cobertura_v399` (h2, h3 e h6 viram pisos; h8, tamanho mínimo) e dos sete contratos (`expected_ladder`); o runner da Fronteira e a camada v401 dos 16 dispositivos "
           "(o número do runner é da sessão do site); a revisão independente antes do portão do operador (o número de céticos é da sessão do site). A publicação do bloco embutido do método do operador no espelho público segue sujeita à decisão [LEGAL] D2 (operador com a agente de PI).\n\n"
           "**Pendências SÓ do operador:** a decisão [LEGAL] D2 (publicar o bloco embutido e as adaptações, com a agente de PI); a custódia conjunta, subir o site, commit/push. Os nomes antes provisórios e a leitura das duas faces estão RATIFICADOS (25/10), e a errata ao lado do adendo é da gerência, em nome próprio. "
           "[OPEN]: a discriminação a 5σ (β_TGL na natureza), a hipótese nomeada `H_tau` (τ é a massa de Newton e a métrica de Einstein; a ORDEM 025 ao Codex é pendência externa), a atestação física externa e a tipagem (sinapse, token, nome), "
           "a face de Fock do psion (o certificado de Fock da luz sem habitante exibido), o contrato conjunto da rede e H3 em toda direção nula; a F8.1 (bandeiras do gate recalculadas) segue [OPEN] e não é tocada pela v401.\n\n"
           "Pacote e cadeia: `work\\cadeia_de_selo\\v401` (+ `pos_rito`); arquivo `work\\cadeia_de_selo\\v401_selo` e `v401_kernel`. NOT_FALSIFIED não é a palavra da creditação; o gate não se move.\n\n"
           "[[%(topico)s]] [[missao-ultima-flag-um-py]] [[handoff-v400-custodia]]\n") % k
    assert k["par_bloco"] in doc and k["par_fal_bloco"] in doc, "os paragrafos do README nao entraram no handoff"
    assert not atribuicao_da_gerencia(doc), ("o handoff atribui mal ou inverte a direcao do testemunho", atribuicao_da_gerencia(doc)[:2])
    return doc


# ------------------------------------------------------------------- ferramentas da arvore e do indice (OPCIONAIS: so' usadas se alguem escrever patch_arvore_indice_v401.py)
# v401: a linha da arvore da prova
def arvore_linha(V):
    d = _d(V)
    return ("- **A FALSIDADE (SIMULACRO) DA INÉRCIA (v401)** `%s`: %d módulo novo no kernel (%s; nome dado pelo operador), %d bandeiras novas True, escada %s → %s; "
            "a inércia é o próprio zero absoluto (definição do operador [INPUT/ONTO]; o `0_abs` do kernel, 1 = 0) e um posto de peso 1 = ω(I) inercial daria 1 = 0 [REAL, sobre os dados da escala dual de Takesaki, [KNOWN]]; o registro `falsidade_da_inercia_v401` confere o cálculo no modelo `oneScaling`; "
            "as %d inscrições de 25/10 por sha256 (todas do operador); a cadeia estendida (nada que porte posto precede a impressão; o zero é a consequência da poda) é [DERIVED], e `H_tau` é [OPEN]; a pedra não prova a primeira lei de Newton; validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["n_pedras"], _mods(V), d["n_f"], V["escada_antes"], d["depois"], d["n_cun"]))


# v401: o titulo do verbete do indice
def titulo_verbete(V):
    return "A falsidade (simulacro) da inércia (v401):"


# v401: o corpo do verbete do indice
def verbete(V):
    return "[REAL — rodada v401 `%s`] %s." % (V["s16"], _num(V))


# v401: a entrada do remissivo
def remissivo(V):
    return "- **A falsidade (simulacro) da inércia, a definição do operador e as inscrições de 25/10 (v401)** — `falsidade_da_inercia_v401`, `cunhagens_v401`, `kh_n1_cobertura_v401`, `%s`" % TOPICO_NOVO
