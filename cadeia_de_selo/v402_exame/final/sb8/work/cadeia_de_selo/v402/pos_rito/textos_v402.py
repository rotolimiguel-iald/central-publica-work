# -*- coding: utf-8 -*-
# Os TEXTOS da v402 SELADA, ESCRITOS A MAO para o delta da v402 (a semente mecanica veio de textos_v401.py, subida pelo motor; o conteudo e' novo): os TRES modulos de kernel `PonteDaEscalaDual` (do Codex, ORDEM 025, com as erratas E1 a E4 ao lado),
# `QuedaSemGeometria` e `EsperancaCondicional` (os nomes sao PROVISORIOS; o operador nomeia), os TRES registros com funcao `ponte_da_escala_dual_v402`, `queda_sem_geometria_v402` e `esperanca_condicional_v402` (cada um LE do kernel do rito a composicao, a estrela, o contrato e o suporte
# da sua pedra e CALCULA um modelo honesto com beta = alfa x raiz de e em runtime), os registros por spec `cunhagens_v402` (as TRES falas do operador de 26/10 por sha256, as erratas E1 a E4 em nome proprio da gerencia c1, as decisoes D11 a D16 e a pergunta e a resposta de 26/10 sobre a direcao do Um posto)
# e `kh_n1_cobertura_v402`, e a secao «A ponte da escala dual, a queda sem geometria e a esperança condicional» do artigo.
# O QUADRO «O Teste da Única Palavra» (v397) PERMANECE no topo do artigo PT/EN e do .md canonico, INTOCADO. Cada numero, hash e veredito entra por chave de V (leitura_v402.ler), por ESPERADOS ou pelo core do Nos, ou e' LIDO de um arquivo aqui, nunca digitado;
# o que vai escrito a mao e' so' prosa, nome de termo (conferido em tempo de execucao no kernel do Nos, no um.py ou no pacote) e frase curta do operador (conferida palavra por palavra contra os bytes das falas).
# REGRA DA ORDEM DO OPERADOR (23/10/2026, sha16 9b182958a5a7a1bc: reportar o 4,44 no inicio do artigo, no README e em tudo mais; vale em TODO texto que o cite): o 4,44 (z_disc calibrado) NUNCA aparece sem o p calibrado e sem a linha dos 5σ no MESMO item (a discriminacao a 5σ,
# o degrau da creditacao, NAO foi alcancada; NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move; o teste nao foi cego). A frase do operador entra VERBATIM (nunca parafraseada entre aspas); o paragrafo do QUADRO sai das MESMAS funcoes do quadro (quadro_v397),
# sobre o core SELADO do Nos. O paragrafo NOVO da v402 NAO traz o 4,44. Estatutos marcados; erratas AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a traducao falhou).
# O PARAGRAFO DO TESTEMUNHO DE DOIS (v399) e o da FALSIDADE (v401) SEGUEM COMO ESTAO no README do espelho e no site: esta versao NAO os regenera nem os substitui; o handoff da v402 so' o diz e traz a ERRATA ao lado do da falsidade (a hipotese `H_tau` na forma literal e' REFUTADA no kernel).
# GUARDA: as cinco regras da P18 (guarda_p18_v402.py) rodam sobre cada texto renderizado em superficies_v402.py, fechar_v402.py e registrar_mapa_v402.py e sobre este arquivo na cadeia. A palavra recusada nunca aparece aqui: a recusa e' dita como «creditação».
import hashlib, json, os, re, sys
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V402"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v402 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(PK))          # ...\Central de Patentes\work
NOS = 'C:/IALD/Central de Patentes/work/cadeia_de_selo/v402_exame/final/sb8\\nos'
TOPICO_NOVO = "v402-selada-ponte-queda-esperanca.md"
# os marcadores entre os quais o handoff traz os PARAGRAFOS PRONTOS do README do espelho e do site: o QUADRO (v397, intocado) com os MESMOS marcadores da v397, e o paragrafo NOVO da falsidade
MARC_PAR_INI = "<!-- INICIO_PARAGRAFO_README_v397 -->"; MARC_PAR_FIM = "<!-- FIM_PARAGRAFO_README_v397 -->"
# o tema de cada uma das TRES inscricoes de 26/10 (resumo da gerencia, nunca citacao): a chave e' o trecho do nome do arquivo de origem (depois do sha16); o sha16, a data e o autor vem dos bytes e do nome, nunca daqui
_TEMAS = (
    ("esperanca_condicional_e_nome", "o pedido de se inteirar do que o Kimi e o ChatGPT avançaram, a dúvida dele se a tipagem já está no um.py e a equação esperança condicional = nome [INPUT]"),
    ("o_um_se_poe_e_cai", "o Um, quando se põe, realiza a operação input; a fase cai; a queda tem direção mas não é geométrica nem força; entrega = custas; o relaxamento; a parábola do labirinto; a pergunta de como explicar queda sem geometria [INPUT/ONTO]"),
    ("e_isso_faca_a_prova_prossiga", "a aprovação da rota: faça a prova e prossiga [INPUT]"),
)
# nomes de termo de kernel (Lean) citados nos textos: cada um tem de existir em algum .lean de TGLExt/ do Nos (lido na hora); os modulos citados como fonte tem de existir como arquivo
_NOMES_KERNEL = ("core_positive_realization_exists", "lift_mass_not_selected", "positive_weight_cannot_be_invariant_mass", "lift_rest_energy", "rest_energy_eq_mc2", "momentumScaling", "boost_is_existing_4D_block", "theta_energy",
                 "a_queda_sem_geometria", "the_fall_is_strictly_anti", "IsotropicPost", "covariance_is_load_bearing", "s8_h3_is_load_bearing", "no_post_before_the_impression", "the_floor_fixes_the_cut", "Smat_has_no_limit", "relaxation_to_the_attractor",
                 "esperanca_condicional_e_nome", "the_name_of_the_unit_is_the_diagonal_expectation", "nameOp", "diagExpect", "observing_adds_nothing", "iald_reads_the_expectation", "NameIndex", "ppIndex", "fixed_tau_zero", "Inertial",
                 "the_inertia_is_the_absolute_zero", "oneScaling", "metric_einstein_from_screen_clausius")
_MODULOS_KERNEL = ("PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional", "FalsidadeDaInercia", "BisognanoWichmann", "Fundacao", "TheCorrespondence", "IALDJones", "Palavra", "PPIndex", "CondExpect", "TheGreatAttractor")
# identificadores do um.py citados nos textos: cada um tem de existir no um.py do Nos (lido na hora)
_NOMES_UM = ("SEALED_CODATA_ALPHA", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "_V402_CONTRACTS", "_V402_VERBATINS2", "_V402_SPECS",
             "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "_V401_VERBATINS2", "_V401_SPECS", "_V401_FALSIDADE_CONTRACT", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399",
             "cunhagens_v399", "kh_n1_cobertura_v399", "selo_acom_sidecar_v399", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "hubble_ratio_opening_v388", "_v397_quadro_md", "_v397_atomos", "_V397_FRASE_444",
             "testemunha_estatica_v396", "psibit_v395", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V395_PSIBIT_CONTRACT",
             "_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT")
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
N_FALAS = len(_TEMAS)   # (o numero e' CONFERIDO em _d contra len(DL.VERBATIM_ORIGEM_V402) e ESPERADOS[cunhagens]; a prosa diz «tres» e o assert derruba a geracao se o numero mudar)
_CACHE = {}
# a DIRECAO (v399): nenhuma frase pode por a IALD como quem testifica DO operador (fora da fala em que ele a recusa); a mesma regex do conferidor (C12)
_RX_INV = re.compile(r"IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)")
ERRATA_TEOREMAS = "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"   # (a mesma frase de delta_v402.ERRATA_TEOREMAS_PT; o harness confere)


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
    """ESPERADOS_v402.json (gerado pelo ensaio a seco do candidato), lido uma vez."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v402.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _core():
    """O core do Nos (so' leitura), para os campos que so' existem depois do rito; ausente e' falha visivel."""
    if "core" not in _CACHE:
        _CACHE["core"] = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["core"]


def _base_core():
    """O core da v401 selada (a copia de bytes em base_v401): de onde saem os numeros da errata ao lado e a medida da proveniencia."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v401", "um_absoluto.json"), encoding="utf-8"))["core"]
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
    """As TRES inscricoes de 26/10 embutidas no um.py: o texto vem do arquivo em insumos/cunhagens e o sha256 e' conferido contra ESPERADOS (fail-closed). Devolve {sha16: {sha16, arquivo, nome, text, autor}};
    o autor sai do NOME do arquivo e e' conferido contra o papel que ESPERADOS registra: nesta versao as tres sao falas do operador (nenhuma e' da gerencia)."""
    if "falas" not in _CACHE:
        ec = _esp()["cunhagens"]; out = {}; pasta = os.path.join(PK, "insumos", "cunhagens")
        for k, meta in ec.items():
            s = k[len("v402_cun_"):]
            fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(s + "_")]
            assert len(fs) == 1, ("a inscricao %s nao tem arquivo unico em insumos/cunhagens" % s, fs)
            b = open(os.path.join(pasta, fs[0]), "rb").read()
            assert hashlib.sha256(b).hexdigest() == meta["sha256"] and len(b) == meta["bytes"] and meta["sha256"][:16] == s, "a inscricao %s nao confere com o sha256 de ESPERADOS" % s
            nome = fs[0][len(s) + 1:]
            autor = "gerencia" if nome.startswith("GERENCIA_") else "operador"
            assert autor == "operador" and not str(meta.get("papel", "")).startswith("leitura da gerencia"), ("a v402 nao tem inscricao da gerencia: as tres sao falas do operador", s)
            out[s] = {"sha16": s, "arquivo": fs[0], "nome": nome, "text": b.decode("utf-8"), "autor": autor}
        assert len(out) == len(_TEMAS) == N_FALAS, "as inscricoes de ESPERADOS nao sao as tres de 26/10"
        _CACHE["falas"] = out
    return _CACHE["falas"]


def _sha_por(sub):
    """O sha16 da unica inscricao cujo arquivo de origem contem `sub` (as inscricoes sao achadas assim, nunca digitadas)."""
    r = [s for s, d in _falas().items() if sub in d["nome"]]
    assert len(r) == 1, ("inscricao nao unica ou ausente", sub, r)
    return r[0]


def _cita(trecho):
    """Fail-closed: o trecho tem de estar numa das tres falas DO OPERADOR, palavra por palavra e na mesma ordem; devolve «trecho». Citacao fora dos bytes derruba a geracao.
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
    """A cobertura do Audit e a arvore formal da v401 selada (o core guardado em base_v401): de onde saem os numeros da errata ao lado dos pisos."""
    if "cov_base" not in _CACHE:
        kf = _base_core()["kernel_formalization"]
        cov = kf["axiom_coverage_v392"]
        _CACHE["cov_base"] = {"decl": cov["decl"], "thm": cov["thm"], "h8": len(kf["formal_files_sha256"]), "axr": len(kf["axiom_report"])}
    return _CACHE["cov_base"]


def _bancada():
    """A geracao do manifesto que a Bancada de producao pina (do recibo pre_selo pinado em PINOS_BN) e a versao que ela pina; o passo e' simples (sem salto e sem cadeia de selos)."""
    p = json.load(open(os.path.join(PK, "PINOS_BN_v402.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v401" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v401 -> v402 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1}


def _proveniencia(esp):
    """A proveniencia que o compilador emite atribui ao modulo da pedra N declaracoes; todas sao NOVAS no axiom_report (nenhuma reatribuida), e o FLAGS_v402.json do sandbox concorda (as contagens de
    publicas, privadas, nomeadas e auxiliares so' existem la')."""
    if "prov" not in _CACHE:
        kf = _core()["kernel_formalization"]; src = kf["declaration_sources_v394"]; pedras = set(esp["pedras_sha256"])
        b0 = _base_core()["kernel_formalization"]; axr0 = b0["axiom_report"]
        mine = sorted(n for n, p in src.items() if p in pedras)
        novas = [n for n in mine if n not in axr0]
        fj = json.load(open(os.path.join(PK, "kernel", "FLAGS_v402.json"), encoding="utf-8"))
        assert len(mine) == fj["decl_totais_modulos_novos"] and len(novas) == fj["decl_novas_dos_modulos"] == len(mine) and not fj["reatribuidas_as_pedras"], ("a proveniencia do rito != FLAGS_v402.json do sandbox", len(mine), len(novas), fj["reatribuidas_as_pedras"])
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
    """Os numeros da v402, todos LIDOS (V da leitura da rodada, ESPERADOS, core do Nos, base v401, FLAGS do sandbox, os registros): nenhum e' digitado aqui. Recusa se as contagens nao fecham."""
    _conferir_nomes()
    esp = _esp(); tv = V["veracidade"]; sa = V["selo"]; dc = V["declaracao"]; cg = V["cunhagens"]; sc = V["sidecar"]; core = _core()
    DL_ = _qd().DL; ks = _CHAVES
    mods = sorted(p["modulo"] for p in V["pedras"])
    assert mods == sorted(DL_.STONE_BY_KEY[k]["mod"] for k in ks) and V["n_pedras"] == len(mods) == esp["kernel"]["modulos_novos"] == 3, ("o delta da v402 sao tres modulos, PonteDaEscalaDual, QuedaSemGeometria e EsperancaCondicional", mods)
    nf = esp["n_bandeiras_novas"]; grp = esp["n_bandeiras_por_grupo"]
    assert set(grp) == set(ks) and sum(grp.values()) == nf == esp["politica_de_bandeiras"]["n_flags"] == len(esp["bandeiras_novas_chaves"]), "as bandeiras novas nao sao so' as dos tres modulos"
    ft = {}; sha = {}; unc = {}; est_t = {}; est_f = {}; nck = {}; n_sup = {}; n_contr = {}
    for k in ks:
        st = DL_.STONE_BY_KEY[k]; pe = V[k]
        ch = sorted(c for c in esp["bandeiras_novas_chaves"] if c.startswith(st["flag_prefix"]))
        assert len(ch) == grp[k], ("as bandeiras do grupo nao fecham", k, len(ch), grp[k])
        ft[k] = (ch[0], ch[-1])
        assert pe["flag"] == esp["bandeiras_das_pedras"][k] and pe["flag_true"] is True and pe["theorem"] == esp["teoremas_das_pedras"][k], ("a pedra no kernel do rito nao e' a de ESPERADOS", k)
        assert pe["ok"] is True and pe["mech_ok"] is True and pe["values_ok"] is True and pe["estrela_ok"] is True and pe["kernel_ok"] is True and pe["beta_ok"] is True and pe["contexto_ok"] is True and pe["n_checks"] == DL_.N_CHECKS[k], ("o registro com funcao nao e' o contrato de ESPERADOS", k)
        assert len(esp["contrato_das_pedras"][k]) == len(st["contract"]) and len(esp["suporte_das_pedras"][k]) == len(st["support"]), ("o contrato ou o suporte != delta_v402", k)
        sha[k] = esp["pedras"][st["rel"]]["sha16"]; unc[k] = esp["teoremas_das_pedras"][k]; est_t[k] = esp["estrelas_v402"][k]["teorema"]; est_f[k] = esp["estrelas_v402"][k]["bandeira"]
        nck[k] = pe["n_checks"]; n_sup[k] = len(esp["suporte_das_pedras"][k]); n_contr[k] = len(esp["contrato_das_pedras"][k])
    assert N_FALAS == len(DL_.VERBATIM_ORIGEM_V402) == len(esp["cunhagens"]) == 3, "o numero de inscricoes de 26/10 mudou: a prosa dos textos diz tres (ler N_FALAS, DL.VERBATIM_ORIGEM_V402 e ESPERADOS[cunhagens])"
    pre = DL_.VERBATIM_PREFIXOS_DA_ORDEM_V402
    assert _sha_por("esperanca_condicional_e_nome").startswith(pre[0]) and _sha_por("o_um_se_poe_e_cai").startswith(pre[1]) and _sha_por("e_isso_faca_a_prova").startswith(pre[2]), "as inscricoes nao sao as de DL.VERBATIM_PREFIXOS_DA_ORDEM_V402"
    assert V["fal401"]["ok"] is True and V["fal401"]["verdict"] == esp["veredito_da_falsidade_v401"], "o registro falsidade_da_inercia_v401 recriado nao e' o selado da v401"
    assert sa["ok"] is True and sa["n_checks"] == esp["selo_acom"]["n_checks"] and sa["checks_ok"] is True and sa["values_ok"] is True and sa["beta_ok"] is True, "o registro selo_pela_propria_tecnologia_v399 do core nao e' o contrato de ESPERADOS"
    assert dc["ok"] is True and dc["n_checks"] == esp["declaracao"]["n_checks"] and dc["checks_ok"] is True and dc["ancoras_ok"] is True and dc["direcao_ok"] is True, "o registro declaracao_do_operador_v399 do core nao e' o contrato de ESPERADOS"
    assert sc["ok"] is True and sc["n_objetos"] == len(esp["sidecar"]["objetos"]) and sc["recusas"] == 0, "o sidecar um_absoluto_selo_acom.json nao e' o de ESPERADOS"
    assert tv["ok"] is True and tv["n_checks"] == esp["veracidade"]["n_checks"] and tv["checks_ok"] is True and tv["numeros_ok"] is True and tv["fontes_ok"] is True, "o registro teste_de_veracidade_fase9_v397 do core nao e' o contrato de ESPERADOS (o quadro do topo le os numeros dele)"
    assert cg["ok"] is True and cg["verbatim_ok"] is True and cg["n"] == len(V["verbatins"]) == len(_falas()) == N_FALAS and cg["todas_do_operador"] is True and cg["erratas_ok"] is True and cg["n_erratas"] == 4 and cg["decisoes_ok"] is True and cg["direcao_ok"] is True, "cunhagens_v402 != as tres de 26/10, ou alguma nao e' fala do operador, ou faltam as erratas E1 a E4, as decisoes D11 a D16 ou a leitura da direcao"
    er = _g(core, "cunhagens_v402", "erratas") or []
    assert len(er) == 4 and all(str(e.get("assinatura", "")).startswith("gerencia c1, em nome proprio") for e in er) and "REFUTADA" in str(er[0].get("agora")), "as erratas E1 a E4 nao estao no registro cunhagens_v402 (E1 com REFUTADA, em nome proprio da gerencia c1)"
    assert {re.match(r"(?:OPERADOR|GERENCIA)_(\d{2})out_", f["nome"]).group(1) for f in _falas().values()} == {"26"}, "o nome de arquivo de alguma inscricao nao e' de 26/10 (a data dos textos e' 26/10)"
    qd = _qd(); a = _atomos()
    assert qd.Q._v397_linha_de_maquina(a, "pt") == esp["quadro"]["linha_de_maquina_pt"], "a linha de maquina do quadro (core) != a de ESPERADOS"
    assert esp["quadro"]["frase_do_operador"] == qd.DL.FRASE_DO_OPERADOR_4_44 == qd.Q._V397_FRASE_444, "a frase do operador do quadro != a verbatim"
    base = os.path.join(PK, "base_v401", "um.py")
    if "base_b" not in _CACHE:
        assert s16(base) == V["base16"], "base_v401/um.py nao e' a v401 selada"
        _CACHE["base_b"] = os.path.getsize(base)
    delta = V["umb"] - _CACHE["base_b"]
    kf = core.get("kernel_formalization") or {}; prov = kf.get("declaration_sources_status_v394") or {}
    assert prov.get("ok") is True and prov.get("compiler_names") == prov.get("audited_names") == V["axiom_report_n"], "a proveniencia emitida pelo compilador nao cobre o axiom_report do rito"
    assert V["n_ver_mudaram"] == 0, "algum veredito fora da troca dita mudou: nao ha texto a escrever"
    assert V["n18"] == 18 and all(i in V["patch_ids"] for i in ("N00_main_tres_registros", "N01_main_specs", "N02_selo")), "o gate nao tem as 18 bandeiras True, ou o candidato nao traz os patches que chamam os tres registros (N00), os registros por spec (N01) e o resumo no selo (N02)"
    assert esp["h8_entradas"] == esp["formal_files_n"] + len(esp["h8_residuais_do_nos"]), "a arvore formal do rito != embutidas + residuais do Nos"
    pb = core.get("psibit_v395") or {}; pbc = pb.get("conditional_psion_face") or {}
    assert pbc.get("flag_true") is True and kf.get(pbc.get("flag")) is True and pbc.get("inhabitant_exhibited") is False, "a face de Fock do psibit_v395 nao segue condicional e com a bandeira True"
    pv = _proveniencia(esp); ad = _adendo_texto(); o025 = _cod025()
    assert o025 and re.fullmatch(r"[0-9a-f]{16}", o025) and _g(core, "ponte_da_escala_dual_v402", "literal_h_tau", "status") == "REFUTED_IN_THE_KERNEL", "a ORDEM 025 ou a refutacao da forma literal de H_tau nao estao no registro da ponte"
    return {"n_f": nf, "n_g": {k: grp[k] for k in ks}, "ft": ft, "sha": sha, "unc": unc, "est_t": est_t, "est_f": est_f, "nck": nck, "n_sup": n_sup, "n_contr": n_contr, "n_aux": esp["politica_de_bandeiras"]["n_excluidas"],
            "depois": V["teor"].split("/")[0], "delta": delta, "pct": ("%.1f" % (100.0 * delta / _CACHE["base_b"])).replace(".", ","), "prov": prov["compiler_names"], "n_cun": len(V["verbatins"]), "n_op": N_FALAS,
            "h8": esp["h8_entradas"], "h8_emb": esp["formal_files_n"], "h8_res": ", ".join("`%s`" % x for x in esp["h8_residuais_do_nos"]), "n_res": len(esp["h8_residuais_do_nos"]), "cb": _cov_base(), "bank": _bancada(), "pv": pv,
            "n_checks_v": tv["n_checks"], "n_ck_sel": sa["n_checks"], "n_ck_dec": dc["n_checks"], "n_ck_cun": cg["n_checks"], "n_anc": len(esp["declaracao"]["ancoras"]), "f8": {k: v[:8] for k, v in esp["veracidade"]["fontes"].items()},
            "s_esp": _sha_por("esperanca_condicional_e_nome"), "s_queda": _sha_por("o_um_se_poe_e_cai"), "s_pros": _sha_por("e_isso_faca_a_prova"), "o025": o025, "s_adendo": ad["sha16"], "data_falas": "26/10/2026"}


def _mods(V):
    return ", ".join("`%s`" % p["modulo"].split(".")[-1] for p in sorted(V["pedras"], key=lambda p: p["modulo"]))


def _extras(V):
    # os registros novos ALEM DOS CINCO FIXOS (V["reg402"] tem so' os cinco), ditos pelo nome
    ex = [k for k in V["registros_novos"] if k not in V["reg402"]]
    return (", ".join("`%s`" % k for k in ex)) if ex else "nenhum além dos cinco fixos"


def _cab(V):
    return "v402 SELADA (COMPLETA)** `%s`" % V["s16"]


def _num(V, verdicts=True):
    """O paragrafo dos numeros da v402 (kernel, os tres registros com funcao, os dois registros por spec, os da v401 e da v399 recriados, o sidecar, a troca dita): usado na linhagem, no Atlas, no core, no topico novo, no verbete e no handoff."""
    d = _d(V); kh = V["kh"]; sc = V["sidecar"]; sa = V["selo"]
    vd = (lambda k: " (%s)" % V["reg402"][k]["verdict"]) if verdicts else (lambda k: "")
    pv = V["ponte"]["values"]; qv = V["queda"]["values"]; ev = V["esperanca"]["values"]; ft = d["ft"]; ng = d["n_g"]
    kern = _f("o kernel ganhou {n_pedras} módulos novos ({mods}; os nomes são PROVISÓRIOS, o operador nomeia), com {n_f} bandeiras novas True (ponte {n_p}, de `{p0}` a `{p1}`; queda {n_q}, de `{q0}` a `{q1}`; esperança {n_e}, de `{e0}` a `{e1}`), só de declaração nomeada ({aux} auxiliares geradas pelo compilador ficam sem bandeira), e escada {antes} → {depois} teoremas limpos "
              "({axr} declarações no `axiom_report`, {fora} fora do trio, {nl} nomes não lidos; a proveniência de cada declaração emitida pelo compilador cobre as mesmas {prov}); "
              "errata ao lado da v394, mantida (em nome próprio da gerência c1): " + ERRATA_TEOREMAS,
              n_pedras=V["n_pedras"], mods=_mods(V), n_f=d["n_f"], n_p=ng["ponte"], n_q=ng["queda"], n_e=ng["esperanca"], p0=ft["ponte"][0], p1=ft["ponte"][1], q0=ft["queda"][0], q1=ft["queda"][1], e0=ft["esperanca"][0], e1=ft["esperanca"][1],
              aux=d["n_aux"], antes=V["escada_antes"], depois=d["depois"], axr=V["axiom_report_n"], fora=kh["fora"], nl=kh["nao_lidas"], prov=d["prov"])
    pon = _f("o registro `ponte_da_escala_dual_v402`{vd}, lido na fractalização do Um logo depois da falsidade da inércia (v401): lê do kernel do próprio rito a composição (bandeira `{unc}`), a estrela `lift_mass_not_selected` (bandeira `{est}`), os {n_contr} itens do contrato e os {n_sup} termos antigos que ela cita, todos no trio, "
             "e CALCULA, com β = α(CODATA 2018) × √e = {beta} em runtime, o modelo longitudinal (E, p) com c = 1: m² = p⁺p⁻ é invariante sob p± ↦ e^(∓s)p±; a energia E muda com o observador (deslocamento mínimo {nes} nas energias nulas e {res} no repouso, em {grid} escalas de teste); "
             "a massa NÃO é selecionada pela lei (os μ² {ms} dão o mesmo p⁺); o repouso levanta a ({rl}) e o fora do repouso a ({orl}); só o vetor zero é fixo por todo boost ({fx}) ({nck} checagens, todas passaram); o texto de Bisognano–Wichmann está no kernel embutido deste rito",
             vd=vd("ponte_da_escala_dual_v402"), unc=d["unc"]["ponte"], est=d["est_f"]["ponte"], n_contr=d["n_contr"]["ponte"], n_sup=d["n_sup"]["ponte"], beta=_p(pv["beta"], 12), nes=_p(pv["min_null_energy_shift"], 6), res=_p(pv["min_rest_energy_shift"], 6), grid=pv["grid_scales"],
             ms=_lst(pv["lifts_same_pplus_masses"]), rl=_lst(pv["rest_lift"]), orl=_lst(pv["off_rest_lift"]), fx=_lst(pv["fixed_by_every_boost"]), nck=d["nck"]["ponte"])
    que = _f("o registro `queda_sem_geometria_v402`{vd}: lê a composição `a_queda_sem_geometria` (bandeira `{unc}`), a estrela `the_fall_is_strictly_anti` (bandeira `{est}`), os {n_contr} itens do contrato e os {n_sup} termos antigos, todos no trio, e CALCULA o modelo `oneScaling` (τ = id, θ_s = e^(−s)·): "
             "o peso depois da escala s é e^(−s) (vale {w1} em s = 1 e {w_1} em s = −1, em {grid} escalas), a queda em nats é s e a seta é o sinal de s; o custo t·β·g tem mínimo {mincost} (> 0), o fator de defasagem tem máximo {maxd} (< 1) e vale {deph} em t = 1, g = 1, e a perda por unidade vale {loss}; "
             "os testemunhos do abismo são {n_ab} e os do vazamento {n_lk}; o fluxo diagonal de gap zero {fx0}; o regime angular tem período {per} e só lê; o modelo finito tem grupo de ordem {ordem} ({nck} checagens, todas passaram); «o piso limita» está no kernel embutido deste rito",
             vd=vd("queda_sem_geometria_v402"), unc=d["unc"]["queda"], est=d["est_f"]["queda"], n_contr=d["n_contr"]["queda"], n_sup=d["n_sup"]["queda"], w1=_p(qv["post_weight_at_scale_one"], 6), w_1=_p(qv["post_weight_at_minus_one"], 6), grid=qv["grid_scales"], mincost=_p(qv["min_cost_t_beta_g"], 9),
             maxd=_p(qv["max_dephasing_factor"], 9), deph=_p(qv["dephasing_factor_at_t1_g1"], 9), loss=_p(qv["loss_per_unit"], 9), n_ab=len(qv["abyss_witnesses"]), n_lk=len(qv["leak_witnesses_g_half"]),
             fx0=("é fixo em todo t testado" if qv["diag_flow_gap_zero_is_fixed"] is True else "NÃO é fixo"), per=_p(qv["angular_period"], 6), ordem=qv["finite_model_group_order"], nck=d["nck"]["queda"])
    esq = _f("o registro `esperanca_condicional_v402`{vd}: lê a composição `esperanca_condicional_e_nome` (bandeira `{unc}`), a estrela `the_name_of_the_unit_is_the_diagonal_expectation` (bandeira `{est}`), os {n_contr} itens do contrato e os {n_sup} termos antigos, todos no trio, e CALCULA em M2(C) (matrizes 2×2 e o espaço GNS de dimensão {gns}): "
             "com sin²θ_M = β = {s2} (θ_M = {tm}), o Operador do Nome de ρ* é a esperança diagonal (constante {dpp} no PP, índice {idx2} em M2), preserva o Um (E(1) = 1), reler não acrescenta, é memória-subálgebra e bimodular, e a compressão pelo espelho é o Nome; "
             "o índice condicional 1/β vale {nidx} (CONDICIONAL a duas hipóteses do enunciado; nenhuma instância é construída) ({nck} checagens, todas passaram)",
             vd=vd("esperanca_condicional_v402"), unc=d["unc"]["esperanca"], est=d["est_f"]["esperanca"], n_contr=d["n_contr"]["esperanca"], n_sup=d["n_sup"]["esperanca"], gns=ev["gns_dimension"], s2=_p(ev["sin2_theta_M"], 12), tm=_p(ev["theta_M"], 9), dpp=_pn(ev["diagonal_expectation_pp_constant"], 3),
             idx2=ev["diagonal_expectation_index_M2"], nidx=_p(ev["name_index_one_over_beta"], 4), nck=d["nck"]["esperanca"])
    cun = _f("o registro `cunhagens_v402`{vd}: as {n} inscrições de 26/10 embutidas por sha256 e consumidas no rito, TODAS falas do operador (nenhuma é da gerência); as erratas E1 a E4 (em nome próprio da gerência c1: a forma literal de `H_tau` é REFUTADA no kernel); as decisões D11 a D16 da gerência; "
             "e a pergunta e a resposta de 26/10 sobre a direção do Um posto ({nck} checagens, todas passaram); as falas são [INPUT/ONTO] e valem como leitura dele, não como medida", vd=vd("cunhagens_v402"), n=d["n_cun"], nck=d["n_ck_cun"])
    khs = _f("o registro `kh_n1_cobertura_v402`{vd}: {decl} constantes, {thm} teoremas, {fora} fora do trio, {nl} nomes não lidos; a árvore formal do Nós depois do rito tem {h8} entradas ({emb} embutidas mais {nres} residual do Nós: {res}), "
             "e o pino h8 do registro é o hash dessa árvore, calculado por script sobre a árvore simulada do Nós na geração do candidato",
             vd=vd("kh_n1_cobertura_v402"), decl=kh["decl"], thm=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"], h8=d["h8"], emb=d["h8_emb"], nres=d["n_res"], res=d["h8_res"])
    rec = _f("os três registros da v401 (`falsidade_da_inercia_v401`, `cunhagens_v401` e `kh_n1_cobertura_v401`) e os quatro da v399 (`selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399`, `cunhagens_v399` e `kh_n1_cobertura_v399`) são recriados no mesmo ponto do main e seguem selados e iguais ao ensaio a seco (os da v401, também iguais à v401 selada); "
             "o selo pela própria tecnologia sela os {bytes} bytes do `um.py` v402 ao lado do SHA-256 (perfil `{perfil}`, {nctl} controles negativos recusados), e o sidecar `um_absoluto_selo_acom.json` (arquivo da custódia desde a v399, reescrito pelo rito; sha256 `{sc16}`, veredito `{sv}`, {nr} recusas) lista os {no} objetos finais",
             bytes=format(sa["bytes"], ","), perfil=sa["perfil"], nctl=sa["n_controles"], sc16=sc["sha16"], sv=sc["veredito"], nr=sc["recusas"], no=sc["n_objetos"])
    ex = _extras(V)
    resto = _f("{ex}; o registro `teste_de_veracidade_fase9_v397` segue selado e igual (o quadro do topo do artigo le os numeros dele); troca dita (só números): {troca}; nenhuma mudança NÃO numérica: {nm} vereditos fora da troca dita mudaram (exigido: 0); validade no kernel não é creditação",
               ex=("nenhum registro novo além dos cinco fixos" if ex.startswith("nenhum") else "registros novos além dos cinco fixos: " + ex), troca=", ".join("`%s`" % x for x in V["troca_dita"]), nm=V["n_ver_mudaram"])
    return "; ".join([kern, pon, que, esq, cun, khs, rec, resto])


def _cunhagens(V, forma="lista"):
    """As inscricoes de 26/10 embutidas por sha256: 'lista' (data, sha16, autor e tema, uma por linha; as tres sao falas do operador) ou 'curta' (uma frase com os sha16). Data, sha16 e autor vem dos bytes e do nome; o tema e' da gerencia (_TEMAS)."""
    fl = list(_falas().values()); assert len(fl) == len(V["verbatins"]) == N_FALAS
    if forma == "curta":
        return _f("{n} inscrições embutidas por sha256, todas falas do operador [INPUT/ONTO] — a equação esperança condicional = nome `{a}`, o Um que se põe e a fase que cai, a queda sem geometria `{b}` e a aprovação da rota `{c}`",
                  n=len(fl), a=_sha_por("esperanca_condicional_e_nome"), b=_sha_por("o_um_se_poe_e_cai"), c=_sha_por("e_isso_faca_a_prova"))
    linhas = []
    for d in fl:
        r = [tema for chave, tema in _TEMAS if chave in d["nome"]]
        assert len(r) == 1, ("a inscricao nao tem um tema unico em _TEMAS", d["sha16"], len(r))
        linhas.append("- %s `%s` (fala do operador) — %s" % (_data_fala(d, V), d["sha16"], r[0]))
    return "\n".join(linhas)


def _ordem(V):
    """A ordem do operador de 26/10: so' citacao conferida contra os bytes das falas DO OPERADOR."""
    d = _d(V)
    q_esp = _cita("esperança condicional=nome"); q_taip = _cita("ainda não sei se fizemos a tipagem no um.py")
    q_inp = _cita("o Um quando se põe realiza a operação \"input\""); q_cai = _cita("ao se inscrever, ele cai. a fase cai."); q_dir = _cita("então tem direção, mas não é gemétrica")
    q_ent = _cita("é a operação da entrega (entrega=custas), opera o relaxamaneto"); q_fim = _cita("a queda que eu quero traduzir não é força também"); q_chao = _cita("porque vc sabe que tem um chão, então relaxa"); q_pros = _cita("é isso, faça a prova, prossiga.")
    return _f("**A ordem:** [INPUT/ONTO] as {n_op} falas do operador (Luiz Antonio Rotoli Miguel) de {data} que entram nesta rodada, TODAS dele (nenhuma é da gerência), embutidas por sha256 no registro `cunhagens_v402` e listadas abaixo (as aspas aqui são TRECHOS, conferidos palavra por palavra contra os bytes de cada fala; "
              "o texto íntegro está em `work\\cadeia_de_selo\\v402\\insumos\\cunhagens`): sobre o nome, a dúvida {q_taip} e a equação {q_esp} (`{s_esp}`); sobre a queda, {q_inp}, {q_cai}, {q_dir}, {q_ent}, {q_fim}, e a parábola do labirinto que termina em {q_chao} (`{s_queda}`); "
              "e a aprovação da rota, {q_pros} (`{s_pros}`). A gerência c1 preparou o candidato e rodou o rito (pacote `work\\cadeia_de_selo\\v402`); as fontes pinadas dos registros ficam em `insumos`: as três pedras (`PonteDaEscalaDual.lean`, `QuedaSemGeometria.lean` e `EsperancaCondicional.lean`), "
              "a medida da cobertura (`KH_N1_v402.json`) e a cópia durável do adendo de 03-04/09 (`insumos\\adendo`); o resultado do Teste da Única Palavra, que o quadro do topo lê, mora na v397 (`insumos\\fase9`); "
              "quem constrói não aprova: a revisão independente do candidato, das pedras e dos derivados da cadeia é ato distinto e não é afirmada por este registro.",
              n_op=d["n_op"], data=d["data_falas"], q_taip=q_taip, q_esp=q_esp, q_inp=q_inp, q_cai=q_cai, q_dir=q_dir, q_ent=q_ent, q_fim=q_fim, q_chao=q_chao, q_pros=q_pros, s_esp=d["s_esp"], s_queda=d["s_queda"], s_pros=d["s_pros"])


def _sidecar(V):
    """O sidecar um_absoluto_selo_acom.json: arquivo da custodia desde a v399 (D5); o selo nao pode conter o selo ACOM de si mesmo; o rito da v402 o REESCREVE."""
    d = _d(V); sc = V["sidecar"]
    objs = "; ".join("`%s` (%s B, sha16 `%s`)" % (n, format(o["bytes"], ","), o["sha16"]) for n, o in sc["objetos"].items())
    return _f("**O sidecar `um_absoluto_selo_acom.json` [REAL; arquivo da custódia desde a v399, D5; reescrito por este rito]:** depois da ÚLTIMA escrita do selo, o `um.py` v402 escreve a segunda testemunha dos {no} objetos FINAIS com o SHA-256 ao lado ({objs}); sha256 do sidecar `{sc16}` ({sb} B), esquema `{esq}`, veredito `{sv}`, {nr} recusas. "
              "O selo não pode conter o selo ACOM de si mesmo (seria circular): o sidecar fica AO LADO e carrega o SHA-256 do selo final, e o selo traz só os resumos (veredito, bandeira e hashes), agora também os dos três registros com função da v402. "
              "A recusa do selo ACOM só REGISTRA (D4): o SHA-256 segue soberano e o rito não cai. A primitiva de integridade é o SHA-256 [KNOWN]; a segunda testemunha NÃO acrescenta força criptográfica independente, e a confidencialidade não é alegada nem medida. A custódia da v399, da v401 e da v402 é CONJUNTA.",
              objs=objs, no=sc["n_objetos"], sc16=sc["sha16"], sb=format(sc["bytes"], ","), esq=sc["esquema"], sv=sc["veredito"], nr=sc["recusas"])


def _pedra(V):
    """As TRES pedras: composicao incondicional por citacao, estrela, suporte; o que elas NAO entregam."""
    d = _d(V)
    return _f("**As três pedras [REAL]** (nomes PROVISÓRIOS; o operador nomeia): `PonteDaEscalaDual` (sha16 `{h1}`; {c1} itens de contrato; {s1} termos antigos citados; composição `{t1}`, estrela `{e1}`), `QuedaSemGeometria` (sha16 `{h2}`; {c2} itens; {s2} termos; composição `{t2}`, estrela `{e2}`) "
              "e `EsperancaCondicional` (sha16 `{h3}`; {c3} itens; {s3} termos; composição `{t3}`, estrela `{e3}`); {n_f} bandeiras ao todo, só no trio, sem axioma próprio. As composições são INCONDICIONAIS na ponte; na queda o enunciado leva a hipótese NOMEADA `IsotropicPost`, e na esperança o índice 1/β leva duas hipóteses do enunciado. "
              "A lei de escala de Takesaki é DADO ([KNOWN], campo de `DualScalingData`); β entra como variável real positiva, jamais literal; que a taxa observada seja α√e é a identificação de runtime, não do kernel. "
              "Os nomes são o que a gerência deu a módulos novos, não creditação de coisa alguma. As pedras NÃO provam a primeira lei de Newton, nem que E = mc² seja composta da escala (E3), nem a dimensão 3, nem a assinatura (1,3), nem o rank c = 4.",
              h1=d["sha"]["ponte"], c1=d["n_contr"]["ponte"], s1=d["n_sup"]["ponte"], t1=d["unc"]["ponte"].split(".")[-1], e1=d["est_t"]["ponte"].split(".")[-1], h2=d["sha"]["queda"], c2=d["n_contr"]["queda"], s2=d["n_sup"]["queda"], t2=d["unc"]["queda"].split(".")[-1],
              e2=d["est_t"]["queda"].split(".")[-1], h3=d["sha"]["esperanca"], c3=d["n_contr"]["esperanca"], s3=d["n_sup"]["esperanca"], t3=d["unc"]["esperanca"].split(".")[-1], e3=d["est_t"]["esperanca"].split(".")[-1], n_f=d["n_f"])


def _entrou(V):
    d = _d(V)
    return _f("**O que entrou** (pacote `work\\cadeia_de_selo\\v402` sobre a v401 `{base}`; {np} patches — {patches}; instalado em {inst}; o `um.py` cresce {delta} B, {pct}%): {num}.",
              base=V["base16"], np=V["n_patches"], patches=V["patches"], inst=V["instalado_em"], delta=format(d["delta"], ","), pct=d["pct"], num=_num(V))


def _regra_do_4_44(V):
    """A regra da ordem do operador (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item; o QUADRO do topo (v397) PERMANECE, intocado; onde o numero aparece e como se confere."""
    d = _d(V); a = _atomos(); q = _frase_444()
    return _f("**A regra do 4,44 (ordem do operador de 23/10/2026, `{s44}`) e o quadro do topo:** o quadro «O Teste da Única Palavra» (v397) PERMANECE, intocado, no topo do artigo (PT e EN) e do .md canônico, e o parágrafo dele segue no README do espelho e no site: o z_disc calibrado é reportado no início, "
              "e NUNCA sem o p calibrado e sem a linha dos 5σ no mesmo item: {z444}. A frase do operador entra VERBATIM, {q}, como leitura dele [INPUT/ONTO], não como critério da régua; a paráfrase da gerência nunca entra entre aspas. `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; o teste não foi cego. "
              "[REAL] o quadro do artigo, o do .md e o parágrafo pronto do README/site saem das MESMAS funções (`_v397_atomos` e `_v397_quadro_md`), sobre o registro `teste_de_veracidade_fase9_v397` selado no core do Nós, e a cadeia os confere de novo contra o resultado pinado "
              "(a linha de máquina do quadro, cada número, a frase verbatim e a regra da ordem item a item), com controles negativos que reprovam o 4,44 sem o p, sem a linha dos 5σ, com número adulterado ou com a frase parafraseada. "
              "O parágrafo NOVO da v402 não traz o 4,44, e a cadeia confere isso.",
              s44=_esp()["quadro"]["frase_sha16"], z444=_z444(), q=q)


def _kernel_prova(V):
    d = _d(V)
    return _f("**O que o kernel prova e o que é leitura:** [REAL] as composições das três pedras e as estrelas estão no kernel deste rito, dentro do trio, com proveniência no módulo de cada pedra, e citam termos que o kernel já tem, cada um no `axiom_report`, no trio, com a proveniência que o compilador emite: "
              "`{t1}` / `{e1}` (ponte), `{t2}` / `{e2}` (queda) e `{t3}` / `{e3}` (esperança); tudo lido a cada rito pelos registros `ponte_da_escala_dual_v402` ({n1} checagens do cálculo), `queda_sem_geometria_v402` ({n2}), `esperanca_condicional_v402` ({n3}) e `cunhagens_v402` ({nc} checagens) "
              "e coberto por `kh_n1_cobertura_v402`. [REAL] os registros NÃO são prova de kernel sobre a natureza: conferem os termos citados e o cálculo nos modelos e não movem o gate; a prova como validade não muda. "
              "[KNOWN] a lei de escala de Takesaki é campo da estrutura; Bisognano–Wichmann, a relatividade restrita, a esperança condicional, o índice de Jones e Pimsner–Popa são da literatura. [INPUT/ONTO] as falas do operador de 26/10 (o Um que se põe e a fase que cai; esperança condicional = nome) são leituras dele; "
              "[ONTO, só estas] a direção do Um posto como a seta da queda da fase, o 1 + 3 e o Nome como três faces de um objeto fixo são leituras, sem termo no kernel. [OPEN] `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β e o caso III₁. "
              "A forma literal de `H_tau` (τ é a massa de Newton) é REFUTADA no kernel (E1), e a ORDEM 025 ao Codex (sha16 `{o025}`) foi integrada com as erratas ao lado.",
              t1=d["unc"]["ponte"].split(".")[-1], e1=d["est_t"]["ponte"].split(".")[-1], t2=d["unc"]["queda"].split(".")[-1], e2=d["est_t"]["queda"].split(".")[-1], t3=d["unc"]["esperanca"].split(".")[-1], e3=d["est_t"]["esperanca"].split(".")[-1],
              n1=d["nck"]["ponte"], n2=d["nck"]["queda"], n3=d["nck"]["esperanca"], nc=d["n_ck_cun"], o025=d["o025"])


def _limites(V, curto=False):
    """Os estatutos fieis da v402: o que as pedras, os registros e as erratas dizem e NAO dizem."""
    d = _d(V)
    if curto:
        return _f("**Limites ditos:** [REAL] os registros com função LEEM o kernel do próprio rito e CONFEREM o cálculo nos modelos (longitudinal (E, p), `oneScaling`, M2(C)); não abrem dado, não são teste, não acrescentam rito; [KNOWN] a lei de escala de Takesaki é dado, e E = mc², Bisognano–Wichmann e a esperança condicional são da literatura; "
                  "as pedras NÃO provam a primeira lei de Newton, nem que E = mc² seja composta da escala; [INPUT/ONTO] as três falas de 26/10 são dele; [DERIVED] a realização da lei de escala como o boost longitudinal e a composição do Nome; [ONTO, só estas] a direção do Um posto como a seta da queda da fase, o 1 + 3 e o Nome como três faces de um objeto fixo; "
                  "[OPEN] `H_BW`, `H_cal`, H3, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β e a discriminação a 5σ; a forma literal de `H_tau` é REFUTADA no kernel (E1); a ORDEM 025 ao Codex (sha16 `{o025}`) entrou com erratas; o quadro do topo segue com a sua linha dos 5σ; validade no kernel não é creditação; o gate não se move.", o025=d["o025"])
    return _f("**Limites ditos (estatutos fiéis):** [REAL] ESCOPO: os três registros com função leem as composições e as estrelas das pedras no kernel do rito e conferem o cálculo nos modelos (β = α√e em runtime); CONFEREM, não provam (quem prova é o kernel), não abrem dado, não são teste, não acrescentam rito e não movem o gate. "
              "[REAL] As pedras COMPÕEM por citação termos que o kernel já tem e a matemática nova é só de cola; a lei de escala de Takesaki é DADO [KNOWN], campo da estrutura, como na Fundação. "
              "[REAL] As pedras NÃO provam a primeira lei de Newton, nem que E = mc² seja composta da escala (E3: `rest_energy_eq_mc2` é álgebra real com premissas explícitas e a composição é `lift_rest_energy`, do repouso, c = 1, condicionada a μ² e a τ = m), nem a dimensão 3, nem a assinatura (1,3), nem o rank c = 4. "
              "[REAL] «Inertial» na instância `momentumScaling` é o VETOR ZERO (E2), não movimento livre. [INPUT/ONTO] As falas de 26/10 (o Um que se põe e a fase que cai; entrega = custas; esperança condicional = nome) são do operador: o kernel não as prova. "
              "[DERIVED] A realização da lei de escala como a ação do boost longitudinal sobre (E, p), a queda estritamente decrescente do peso e a composição do Nome. [ONTO, só estas] A direção do Um posto como a seta da queda da fase, o 1 + 3, o labirinto como o regime angular e o Nome como três faces de um objeto fixo são leituras, sem termo no kernel. "
              "[DECLARADO] A pergunta e a resposta de 26/10 sobre a direção não têm arquivo verbatim no acervo desta cadeia. [LEGAL] O ponteiro CC art. 125 fica a conferir com advogado. "
              "[OPEN] `H_BW` (a rapidez é o tempo modular de Bisognano–Wichmann), `H_cal` (este p⁺ é a energia de UM corpo), H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost` no atlas curvo, a instância e o caso III₁ do índice 1/β, que `s` seja a fase de um corpo físico e a atestação física externa. "
              "A forma literal de `H_tau` (τ é a massa de Newton) é REFUTADA no kernel (E1) e a ORDEM 025 ao Codex (sha16 `{o025}`) entrou com as erratas E1 a E4 ao lado. "
              "O quadro «O Teste da Única Palavra» segue no topo, com a sua linha dos 5σ, e esta rodada não o altera. NÃO é teste novo: as pedras são a prova que o operador pediu, e a cadeia não acrescenta dado nem desfecho experimental. Validade no kernel não é creditação; o gate não se move.", o025=d["o025"])


def _legal(V):
    """A pendencia [LEGAL] herdada (D2): publicar o bloco embutido e as adaptacoes; a v402 nao a decide."""
    _d(V)
    return ("**Pendência [LEGAL] (herdada da v399, D2):** o bloco embutido do método do operador e as adaptações (centro 96, ids derivados dos hashes, `rint`, tabela de códigos, auditoria de separação) seguem sob a decisão do operador com a agente de PI; a v402 não muda o bloco (o runtime da seção é o da v401) e NÃO decide a pendência. "
            "Perguntas à agente de PI, não conclusões: o que o depósito já cobre do que o bloco mostra; publicar as adaptações inicia a contagem do prazo de graça para eventual depósito de melhoria; a divergência da tabela dos estados do ACOM Mirror com a fórmula de índice e o código executado, registrada na v395, segue pendente.")


def _erratas(V):
    """A errata de contagem da v402, AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (estrutura / escrito / falha): o registro kh_n1_cobertura_v401 e os oito contratos."""
    d = _d(V); kh = V["kh"]; cb = d["cb"]
    ids = V["patch_ids"]
    assert all(i in ids for i in ("C12__V401_FALSIDADE_CONTRACT", "C12__V398_SONICO_CONTRACT", "C12__V398_AFINACAO_CONTRACT", "C12__V396_TESTEMUNHA_CONTRACT", "C12__V395_PSIBIT_CONTRACT", "C12__V394_FORMAL_CONTRACT", "C12__V394_QUADRATIC_CONTRACT", "C12__V394_NETWORK_CONTRACT", "C13_kh_n1_v401_pisos")), "o CANDIDATO_v402.json nao traz os patches C12 e C13 que a errata descreve"
    return _f("**Errata ao lado (em nome próprio da gerência c1; o registro `kh_n1_cobertura_v401` e os contratos ficam como registro):** a v402 acrescenta três módulos: a cobertura do Audit cresce de {d0} constantes e {t0} teoremas para {d1} e {t1}, "
              "a árvore formal do Nós de {h0} para {h1} entradas e a escada de {e0} para {e1}. Por isso, na v402, (i) `kh_n1_cobertura_v401` passa a cobrar piso em h2, h3 e h6 (as igualdades de contagem) e tamanho mínimo da árvore em h8 (as igualdades exatas e o pino exato da "
              "árvore ficam em `kh_n1_cobertura_v402`); (ii) os oito contratos (`_V394_FORMAL_CONTRACT`, `_V394_QUADRATIC_CONTRACT`, `_V394_NETWORK_CONTRACT`, `_V395_PSIBIT_CONTRACT`, `_V396_TESTEMUNHA_CONTRACT`, `_V398_SONICO_CONTRACT`, `_V398_AFINACAO_CONTRACT` e `_V401_FALSIDADE_CONTRACT`) passam a ler `expected_ladder` = {e1}, a escada desta versão (o consumidor exige a igualdade "
              "exata com a escada do rito; só o número muda); o veredito dos registros anteriores NÃO muda [REAL, lido de `CANDIDATO_v402.json` (patches C12 e C13) e do ensaio a seco, que deu `TUDO PASSOU`: com a escada nova e o número velho a igualdade exata não fecharia]. "
              "Lacuna de fidelidade: a estrutura da v401 dizia que as contagens e o pino da árvore eram a cobertura exata e que o contrato esperava a escada vigente; o escrito deixou, dentro dos registros e dos contratos, números que só valem na versão que os escreveu; "
              "a falha: igualdades e literais presos a uma versão quebram quando o kernel cresce (a mesma lacuna que a v395, a v396, a v397, a v399 e a v401 acharam nos registros anteriores). A cobrança exata passa a ser de `kh_n1_cobertura_v402` ({dd} constantes, {dt} teoremas, {fora} fora do trio, {nl} nomes não lidos), contra a medida do sandbox da v402.",
              d0=cb["decl"], t0=cb["thm"], h0=cb["h8"], d1=kh["decl"], t1=kh["thm"], h1=d["h8"], e0=V["escada_antes"], e1=d["depois"], dd=kh["decl"], dt=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"])


def _depois(V):
    d = _d(V); bk = d["bank"]
    return ("**O que vem depois destas superfícies:** o elo B(n) da Bancada Um (passos 10, 10a, 10b e 10c da cadeia; B3 nos scripts) é pós-selo, um passo SIMPLES (a Bancada de produção pina a %s, geração B%d, e o Nós passa a v402: sem salto e sem cadeia de selos; "
            "a geração esperada é B%d e o veredito esperado do aplicar é REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, lido do código do esboço R3.5, não rodado) "
            "e pede a palavra do operador (parada e religamento do serviço exigem V402_AUTORIZACAO_OPERADOR); o recibo dele é citado no handoff (fechar), que traz PRONTOS os parágrafos do README do espelho e do site (o quadro do Teste da Única Palavra, intocado, e o NOVO da v402), "
            "a ERRATA ao lado do parágrafo da falsidade (v401), diz que o parágrafo do testemunho de dois (v399) e o da falsidade SEGUEM COMO ESTÃO e LISTA o sidecar `um_absoluto_selo_acom.json`. A pendência [LEGAL] (D2) segue do operador com a agente de PI; a atestação física externa e a discriminação a 5σ seguem [OPEN]; "
            "a revisão independente e a nomeação das três pedras e dos cinco registros são do operador e da gerência, não desta cadeia. NOT_FALSIFIED não é a palavra da creditação; o gate não se move." % (bk["de"], bk["geracao"], bk["proxima"], bk["proxima"]))


def _rodada(V):
    """O paragrafo da rodada (horarios, escada, selo, conferidor, sidecar, pilar, artefatos): tudo lido da leitura da rodada."""
    sc = V["sidecar"]
    return ("Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado (%d bandeiras True; o veredito do gate é o mesmo da v401); o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); "
            "o sidecar `um_absoluto_selo_acom.json` `%s` (%d objetos, %d recusas); o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.") % (
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["n18"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"], sc["sha16"], sc["n_objetos"], sc["recusas"], "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]),
        V["pilar"]["result16"], V["servidor"], V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()))


# v402: a linhagem (diario datado do Nos)
def linhagem(V):
    d = _d(V)
    return (("## %s — **%s — A PONTE DA ESCALA DUAL, A QUEDA SEM GEOMETRIA E A ESPERANÇA CONDICIONAL (v402): %d módulos novos, escada %s → %s\n<!-- linhagem_v402_selada -->\n\n"
             "%s\n\n%s\n\n"
             "**As inscrições de 26/10** (embutidas por sha256 no registro `cunhagens_v402`): [INPUT/ONTO] as três são falas do operador (Luiz Antonio Rotoli Miguel) e valem como leitura dele, não como medida; nenhuma é da gerência. "
             "O texto íntegro de cada uma está no arquivo (`work\\cadeia_de_selo\\v402\\insumos\\cunhagens`); abaixo, a data, o sha16, o autor e o tema (resumo da gerência, não citação):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s") % (
        V["data"], _cab(V), V["n_pedras"], V["escada_antes"], d["depois"], _ordem(V), _entrou(V), _cunhagens(V), _ponte(V) + "\n\n" + _queda(V) + "\n\n" + _esperanca(V), _erratas_e(V), _decisoes(V), _leitura_direcao(V), _pedra(V), _sidecar(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V), _rodada(V), _erratas(V)) + "\n\n" + _depois(V))


# v402: o adendo do desenho do fechamento
def desenho(V):
    d = _d(V); kh = V["kh"]
    return (("## ADENDO — %s · v402 SELADA (COMPLETA) `%s` — o caminho crítico NÃO mudou; entram a ponte da escala dual, a queda sem geometria e a esperança condicional (%d módulos)\n\n<!-- adendo_v402_selada -->\n"
             "- **O que a v402 diz:** %d módulos novos no kernel (%s; os nomes são provisórios, o operador nomeia), escada %s → %s, %s constantes no `axiom_report` (%s fora do trio). A ponte REALIZA a lei de escala de Takesaki ([KNOWN], dado) como o boost longitudinal sobre (E, p): m² = p⁺p⁻ é invariante, a energia é a leitura do observador, "
             "e a massa NÃO é selecionada pela lei (`lift_mass_not_selected`); a forma literal de `H_tau` (τ é a massa de Newton) é REFUTADA no kernel, e τ só pode ser p⁺ [REAL]. A queda: o peso cai estritamente (a seta é o sinal de s), o chão é o POSTO e nunca o 0, a entrega custa, o regime angular só lê; a isotropia é hipótese nomeada `IsotropicPost` [REAL; ONTO: o 1 + 3]. "
             "A esperança condicional É o Nome (`nameOp`): em M2(C), a esperança diagonal, com E(1) = 1; o índice 1/β é CONDICIONAL [REAL; ONTO: três faces de um objeto fixo]. %d inscrições de 26/10 por sha256 (as três são falas do operador). O quadro do topo do artigo (O Teste da Única Palavra, v397) segue intocado: %s. Gate intocado.\n"
             "- **O que a v402 NÃO é para o caminho crítico:** não é teste novo; as pedras não provam a primeira lei de Newton, nem E = mc² composta da escala, nem a dimensão 3; `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura (4,0) contra (1,3) e rank c = 4 seguem NOMEADAS [OPEN] (as dívidas do adendo de 03-04/09 sobre a assinatura e o rank c = 4 seguem abertas); "
             "as erratas E1 a E4 são da gerência, em nome próprio; não identifica β na natureza a 5σ.\n"
             "- **O que segue do operador:** a nomeação das pedras e dos registros; a pendência [LEGAL] (D2, com a agente de PI); o elo B(n) da Bancada Um (passo simples, sem salto; parada e religamento do serviço); a custódia conjunta (sessão do site, com os parágrafos do README/site, a errata ao lado do parágrafo da v401 e o sidecar que o handoff traz); commit/push.") % (
        V["data"], V["s16"], V["n_pedras"], V["n_pedras"], _mods(V), V["escada_antes"], d["depois"], kh["decl"], kh["fora"], d["n_cun"], _z444()))


# v402: o verbete do Atlas
def atlas(V):
    return (("### %s — v402 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v402_selada -->\n[REAL — rodada v402, selo `%s`] %s.\n\n[INPUT/ONTO] As falas do operador entram como o operador as disse e valem como leitura, não como medida; as três são dele: %s.\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\nEstatuto: validade no kernel ≠ creditação; o gate não se move.") % (
        V["data"], V["s16"], V["selo_ts"], _num(V), _cunhagens(V, "curta"), _ponte(V) + "\n\n" + _queda(V) + "\n\n" + _esperanca(V), _erratas_e(V), _decisoes(V), _leitura_direcao(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V)))


# v402: o bloco do TGL_CORE_MEMORY
def core_memory(V):
    return (("## %s — v402 SELADA `%s` (claude-c1; a ponte da escala dual, a queda sem geometria e a esperança condicional, integradas pela gerência)\n<!-- core_v402_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
             "[REAL] %s.\n\n%s\n\n%s\n\n%s\n\n%s\n\n[OPEN] A discriminação a 5σ (β_TGL na natureza), `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β, a atestação física externa (nenhuma `AttestedCollapse` é exibida), a tipagem (sinapse, token, nome), "
             "a face de Fock do psion (o certificado de Fock da luz sem habitante), o contrato conjunto da rede e a pendência [LEGAL] seguem abertos; o elo B(n) da Bancada Um depende da palavra do operador. Nada disto move o gate.") % (
        V["data"], V["s16"], _num(V), _ponte(V) + "\n\n" + _queda(V) + "\n\n" + _esperanca(V), _erratas_e(V), _regra_do_4_44(V), _limites(V, curto=True)))


# v402: o bloco do CLAUDE.md da Haja_Luz (as erratas ao lado, assinadas, vao DENTRO dele)
def haja_luz(V):
    d = _d(V)
    return (("## %s — v402 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v402_selada -->\n%d módulos novos no kernel (%s; nomes provisórios, o operador nomeia): a ponte da escala dual (módulo do Codex, ORDEM 025, com erratas) REALIZA a lei de escala de Takesaki ([KNOWN], dado) como o boost longitudinal sobre (E, p): m² = p⁺p⁻ é invariante, "
             "a energia é a leitura e a massa NÃO é selecionada pela lei [REAL]; a forma literal de `H_tau` (τ é a massa de Newton) é REFUTADA no kernel. A queda sem geometria: o peso cai estritamente (a seta é o sinal de s), o chão é o POSTO e nunca o 0, a entrega custa; `IsotropicPost` é hipótese nomeada [OPEN]. "
             "A esperança condicional É o Nome (`nameOp`; em M2(C) a esperança diagonal; o índice 1/β é condicional) [REAL; ONTO: três faces de um objeto fixo]. As %d inscrições de 26/10 por sha256 (as três são do operador); escada %s → %s. O quadro do topo (O Teste da Única Palavra) segue intocado.\n\n"
             "%s\n\n"
             "Memórias: `%s`, `missao-ultima-flag-um-py.md`, `estatuto-da-prova-07out.md`; handoff `handoff-v402-custodia.md`.") % (
        V["data"], V["s16"], V["teor"], V["n_pedras"], _mods(V), d["n_cun"], V["escada_antes"], d["depois"], _erratas_e(V), TOPICO_NOVO))


def marca_topico_missao(V):
    return "## %s — v402 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v402 SELADA `%s`" % V["s16"]


# v402: o topico da missao da ultima flag
def topico_missao(V):
    d = _d(V)
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): %d módulos novos no kernel (%s); `ponte_da_escala_dual_v402`, `queda_sem_geometria_v402` e `esperanca_condicional_v402` (cada um lê o kernel do rito e confere o cálculo no seu modelo), `cunhagens_v402` (%d inscrições por sha256, todas do operador, as erratas E1 a E4 e as decisões D11 a D16) e `kh_n1_cobertura_v402`; "
                                     "os três registros da v401 e os quatro da v399 recriados e selados; sidecar `um_absoluto_selo_acom.json` reescrito; troca dita nos vereditos que carregam a escada; conferidor (deve mudar %s; não pode mudar %s). Pacote e cadeia: `work\\cadeia_de_selo\\v402` (+ `pos_rito`).") % (V["teor"], V["n_pedras"], _mods(V), d["n_cun"], V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v402 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v402 SELADA (COMPLETA):**"


# v402: o topico do estado da Central
def topico_central(V):
    d = _d(V)
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v401 `%s`; escada %s → %s; gate intocado. %d módulos novos no kernel (%s; nomes provisórios): a ponte da escala dual (a massa NÃO é selecionada pela lei; a forma literal de `H_tau` é REFUTADA no kernel), a queda sem geometria (o peso cai, o chão é o posto) e a esperança condicional é o Nome; "
                               "o `um.py` confere o cálculo nos três modelos (registros `ponte_da_escala_dual_v402`, `queda_sem_geometria_v402` e `esperanca_condicional_v402`); as erratas E1 a E4 (da gerência, em nome próprio) e as decisões D11 a D16 estão no registro `cunhagens_v402`; as %d inscrições de 26/10 por sha256 (todas do operador); "
                               "o quadro do topo (O Teste da Única Palavra, v397) segue intocado. Falta o elo B(n) da Bancada Um (passo simples, sem salto) e a custódia conjunta (sessão do site, `handoff-v402-custodia.md`, que traz os parágrafos do README/site, a errata ao lado do parágrafo da v401 e lista o sidecar); "
                               "a nomeação das pedras e a pendência [LEGAL] (D2) são do operador; commit/push = operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], d["depois"], V["n_pedras"], _mods(V), d["n_cun"])


# v402: o topico do estatuto da prova
def topico_estatuto(V):
    d = _d(V)
    return ("<!-- v402_selada -->\n**%s — v402 `%s`:** o registro `estatuto_da_prova_v391` passou a ler a escada nova (%s → %s; veredito trocado, troca dita; as pedras e os registros da v401 ficam como registro). "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora e é o β_TGL na natureza a 5σ. Os três registros com função conferem o cálculo nos modelos e leem os termos do kernel ([REAL]); a lei de escala de Takesaki é dado ([KNOWN]); "
            "a forma literal de `H_tau` (τ é a massa de Newton) é REFUTADA no kernel e τ só pode ser p⁺; as falas do operador de 26/10 são [INPUT/ONTO]; a direção do Um posto como a seta da queda da fase, o 1 + 3 e o Nome como três faces de um objeto fixo são [ONTO]; `IsotropicPost`, `H_BW`, `H_cal`, H3 e a assinatura seguem [OPEN]. "
            "O quadro do topo segue intocado: %s. Nada disso é prova sobre a natureza.") % (V["data"], V["s16"], V["escada_antes"], d["depois"], _z444())


# v402: o gancho da missao no MEMORY.md
def marca_missao(V):
    return "**v402 SELADA %s `%s` %s COMPLETA (a ponte da escala dual, a queda sem geometria e a esperança condicional; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


# v402: a linha do handoff no MEMORY.md
def linha_handoff(V):
    return "- [HANDOFF v402 — ponte da escala dual, queda sem geometria, esperança condicional; custódia](handoff-v402-custodia.md) — **%s, para a sessão do site (traz o parágrafo novo, o do quadro e a errata do da v401; o do testemunho segue como está)** · `%s`" % (V["data"][:5], V["s16"])


def linha_topico_novo(V):
    return "- [v402 SELADA: a ponte da escala dual, a queda sem geometria e a esperança condicional (%s)](%s) — **%s** · `%s`" % (V["data"][:5], TOPICO_NOVO, V["teor"], V["s16"])


# v402: o topico novo da memoria (um arquivo por versao)
def topico_novo(V):
    d = _d(V)
    return (("---\nname: %s\ndescription: \"v402 SELADA (%s) `%s`: %d módulos novos no kernel (PonteDaEscalaDual do Codex com erratas, QuedaSemGeometria e EsperancaCondicional; nomes provisórios), os registros ponte_da_escala_dual_v402, queda_sem_geometria_v402 e esperanca_condicional_v402, %d inscrições de 26/10 por sha256, as erratas E1 a E4 (H_tau literal REFUTADA no kernel), escada %s → %s; B(n) e custódia pendentes\"\n"
             "metadata:\n  type: project\n---\n\n# v402 SELADA (%s)\n\n"
             "**O que é:** `um.py` **v402** `%s` (%s B) sobre a v401 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); o `um.py` cresce %s B (%s%%).\n\n"
             "**O que entrou:** %s.\n\n"
             "**As inscrições de 26/10** (embutidas por sha256; data, sha16, autor e tema — resumo da gerência, não citação; o texto íntegro está em `insumos\\cunhagens`):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"
             "**Pendências:** a nomeação das pedras e dos registros (operador), o elo B(n) da Bancada Um (palavra do operador; passo simples, sem salto; parada e religamento do serviço), a pendência [LEGAL] (D2), a custódia conjunta (sessão do site, com o sidecar), commit/push. Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v402`.\n\n"
             "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v402-custodia]]\n") % (
        TOPICO_NOVO[:-3], V["data"], V["s16"], V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
        format(d["delta"], ","), d["pct"], _num(V), _cunhagens(V), _ponte(V) + "\n\n" + _queda(V) + "\n\n" + _esperanca(V), _erratas_e(V), _decisoes(V), _leitura_direcao(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V) + "\n\n" + _erratas(V)))


# v402: o aviso a coordenadora (so' sob reivindicacao nomeada)
def aviso(V, reivindicacao):
    d = _d(V)
    return (("### %s — v402 SELADA `%s` [claude-c1]\n<!-- aviso_v402_selada -->\n\n[REAL] A v402 SELOU (%s; COMPLETA; gate intocado): a ponte da escala dual (a lei de escala realizada como o boost longitudinal; a massa não é selecionada; a forma literal de `H_tau` é REFUTADA no kernel), a queda sem geometria (o peso cai, o chão é o posto) "
             "e a esperança condicional é o Nome entram no selo corrente com as %d inscrições de 26/10 (por sha256; todas do operador), as erratas E1 a E4 e as decisões D11 a D16; a ponte do Codex (ORDEM 025) entrou COM erratas ao lado. Escrito sob a reivindicação %s. %d módulos novos no kernel (nomes provisórios); escada %s → %s; "
             "o elo B(n) da Bancada Um, a nomeação das pedras e a pendência [LEGAL] esperam o operador. Não altera pinos, dado, MCP nem gate.") % (V["data"], V["s16"], V["teor"], d["n_cun"], reivindicacao, V["n_pedras"], V["escada_antes"], d["depois"]))


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V402_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# ---------------------------------------------------------------- o PARAGRAFO PRONTO do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO; ordem do operador de 23/10: o 4,44 no inicio do artigo, no readme e tudo mais) e (2) o paragrafo NOVO da falsidade
def verificar_paragrafo_readme(par, res, tv):
    """Verifica o paragrafo do QUADRO (texto) contra o RESULTADO pinado (`res`, o JSON lido) e o registro `tv` selado no core: devolve a lista de falhas (vazia = passou). As verificacoes (as mesmas da v397, da v399 e da v401):
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
    from guarda_p18_v402 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    for st in ("[REAL", "[INPUT]", "[KNOWN]", "COMPOSIÇÃO da gerência"):   # os estatutos que o quadro escreve: REAL (os numeros), INPUT (a leitura binaria e a frase), COMPOSICAO da gerencia (as duas faces) e KNOWN (Jeffreys)
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    return fa


def paragrafo_readme():
    """(texto, relatorio): o paragrafo do QUADRO pronto para colar no README do espelho e no site (o MESMO da v397, da v399 e da v401), gerado por quadro_v397.paragrafo_pronto_readme sobre o core SELADO do Nos, verificado contra o resultado pinado
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
    """Falhas de ATRIBUICAO e de DIRECAO num texto renderizado (v402: nao ha inscricao da gerencia; as tres sao falas do operador): (a) nenhuma frase poe a IALD como quem testifica do operador (fora da fala em que ele recusa a ordem inversa);
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
        fa.append("diz que ha inscricao da gerencia (nesta versao as tres inscricoes sao falas do operador)")
    return fa


# v402: o handoff para a sessao do site (memory\handoff-v402-custodia.md + Nos\HANDOFF_v402_CUSTODIA.md); `k` traz os campos dos recibos do B(n) e os paragrafos do README (fechar_v402.py os le dos recibos e do core): nenhum numero digitado
def handoff(V, k):
    d = _d(V); sc = V["sidecar"]
    k = dict(k)
    if "readme_paragrafo_v402" not in k and "readme_paragrafo_falsidade" in k:
        k["readme_paragrafo_v402"] = k["readme_paragrafo_falsidade"]
    for chave in ("ap_nome", "ap_sha", "ap_ver", "ap_evento", "ap_bat", "par_sha", "rel_sha", "rel_man", "readme_paragrafo", "readme_paragrafo_v402"):
        assert chave in k, ("o handoff precisa do campo dos recibos do B(n) e dos paragrafos do README: " + chave)
    par = k["readme_paragrafo"].rstrip("\n"); par_f = k["readme_paragrafo_v402"].rstrip("\n"); err = errata_v401_bloco().rstrip("\n")
    assert par.startswith("### O Teste da Única Palavra (v397"), "o paragrafo do README (quadro) nao e' o do quadro"
    assert par_f.startswith("### A ponte da escala dual, a queda sem geometria e a esperança condicional (v402"), "o paragrafo da v402 nao e' o novo"
    k.update({"data": V["data"], "s16": V["s16"], "umb": format(V["umb"], ","), "base16": V["base16"], "teor": V["teor"], "rc": V["rc"], "conf16": V["conf16"], "conf_dm": V["conf_dm"], "conf_np": V["conf_np"],
              "pilar": "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), "selo_ts": V["selo_ts"], "num": _num(V), "kernel_prova": _kernel_prova(V), "limites": _limites(V, curto=True), "legal": _legal(V),
              "artigos": ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), "n_cun": d["n_cun"], "n_pedras": V["n_pedras"], "topico": TOPICO_NOVO[:-3], "regra": _regra_do_4_44(V), "erratas_e": _erratas_e(V), "decisoes": _decisoes(V), "direcao": _leitura_direcao(V),
              "sc_nome": "um_absoluto_selo_acom.json", "sc_sha": sc["sha256"], "sc_ver": sc["veredito"], "sc_bytes": format(sc["bytes"], ","), "sc_objs": "; ".join("`%s` sha256 `%s`" % (n, o["sha256"]) for n, o in sc["objetos"].items()),
              "par_bloco": MARC_PAR_INI + "\n" + par + "\n" + MARC_PAR_FIM, "par_v402_bloco": MARC_V402_INI + "\n" + par_f + "\n" + MARC_V402_FIM, "err_bloco": MARC_ERR_INI + "\n" + err + "\n" + MARC_ERR_FIM})
    doc = ("---\nname: handoff-v402-custodia\ndescription: \"HANDOFF v402 (%(data)s) para a sessão do site: a ponte da escala dual (módulo do Codex, com as erratas E1 a E4), a queda sem geometria e a esperança condicional (três módulos, cinco registros, três inscrições de 26/10 e as decisões da gerência); `%(s16)s`; B(n) da Bancada feito; TRAZ os parágrafos prontos do README/site (o quadro do Teste da Única Palavra, intocado, e o novo da v402) e a ERRATA ao lado do parágrafo da falsidade (v401); o parágrafo do testemunho de dois SEGUE COMO ESTÁ; LISTA o sidecar; custódia + pendências do operador\"\n"
           "metadata:\n  type: project\n---\n\n# HANDOFF v402 — CUSTÓDIA (%(data)s)\n\n"
           "**O que é:** `um.py` **v402** `%(s16)s` (%(umb)s B) sobre a v401 `%(base16)s`; %(teor)s; COMPLETA; rc %(rc)s; selftest PASSED; gate intocado; conferidor `%(conf16)s` (deve mudar %(conf_dm)s; não pode mudar %(conf_np)s); pilar %(pilar)s pela chave. "
           "Selo `%(selo_ts)s`.\n\n"
           "**PARÁGRAFOS PRONTOS para o README do espelho e para o site (colar como estão, cada um entre os seus marcadores; o primeiro é o quadro do Teste da Única Palavra, o MESMO da v397, intocado; o segundo é novo).** O do quadro é gerado pelas MESMAS funções do quadro do artigo "
           "(a função paragrafo_pronto_readme do módulo quadro_v397), sobre o core SELADO do Nós, com os mesmos números e estatutos, e verificado contra o resultado pinado ANTES de este handoff nascer (o fechar recusa se o z_disc aparecer sem o p calibrado e sem a linha dos 5σ no mesmo item, "
           "se a frase do operador não for a verbatim ou se algum número diferir do resultado). O novo (a ponte da escala dual, a queda sem geometria e a esperança condicional) é gerado dos registros selados `ponte_da_escala_dual_v402`, `queda_sem_geometria_v402`, `esperanca_condicional_v402` e `cunhagens_v402` e verificado contra o core e contra os números do ensaio a seco "
           "(sem o z_disc do quadro; as citações são trechos verbatim das falas do operador ou da docstring do kernel embutido; sem alegação de segurança criptográfica):\n\n%(par_bloco)s\n\n%(par_v402_bloco)s\n\n"
           "**ERRATA ao lado do parágrafo da falsidade (v401) no README e no site (colar logo abaixo dele, entre os marcadores; o parágrafo da v401 fica como registro):**\n\n%(err_bloco)s\n\n"
           "**O parágrafo do testemunho de dois (v399) e o da falsidade (v401) SEGUEM COMO ESTÃO.** O handoff da v401 (`handoff-v401-custodia.md`) trouxe o da falsidade, e o da v400 regenerou o do testemunho de dois; são os que estão no README do espelho e no site, e esta versão NÃO os regenera nem os substitui (o `um.py` mudou de bytes, mas os parágrafos são dos selos daquelas rodadas). "
           "Os registros que os geravam (`selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399`, `cunhagens_v399`, `falsidade_da_inercia_v401` e `cunhagens_v401`) seguem selados e iguais ao ensaio a seco neste rito (a leitura os confere); só a errata do bloco acima corrige uma frase do da falsidade.\n\n"
           "%(regra)s\n\n%(erratas_e)s\n\n%(decisoes)s\n\n%(direcao)s\n\n"
           "**O que entrou e o que mediu:** %(num)s.\n\n"
           "**O SIDECAR (arquivo da custódia desde a v399, D5; REESCRITO por este rito):** `%(sc_nome)s` (sha256 `%(sc_sha)s`, %(sc_bytes)s B; veredito `%(sc_ver)s`); objetos selados: %(sc_objs)s. O sidecar fica AO LADO do selo (o selo não pode conter o selo ACOM de si mesmo) e o fechar o copia para `work\\cadeia_de_selo\\v402_selo` e o lista no manifesto de incorporação; "
           "a custódia o leva ao cofre, à PORTA (PORTA.json, URL raw) e ao espelho, junto do selo, porque a segunda testemunha só se confere com ele. A custódia da v399, da v401 e da v402 é CONJUNTA. A recusa do selo ACOM só registra (D4); o SHA-256 segue soberano.\n\n"
           "%(kernel_prova)s\n\n%(limites)s\n\n%(legal)s\n\n"
           "**O elo B(n) da Bancada Um (feito antes deste handoff; passo simples, sem salto):** recibo da aplicação `%(ap_nome)s` (sha256 `%(ap_sha)s`; veredito `%(ap_ver)s`; evento %(ap_evento)s; bateria `%(ap_bat)s`); recibo da parada do serviço sha256 `%(par_sha)s`; "
           "recibo do religamento sha256 `%(rel_sha)s` (versão servida v402, manifesto `%(rel_man)s`).\n\n"
           "**Para a sessão do site (custódia):** o `um.py` v402, `rodada_v402_stdout.txt`, o selo, o sidecar, o core, o .md canônico (com o quadro no topo, intocado) e o manifesto, os artigos PT/EN (%(artigos)s; o quadro «O Teste da Única Palavra» abre os dois), as %(n_cun)s inscrições de 26/10 por sha256 "
           "(as três são falas do operador; lista na linhagem e no tópico `%(topico)s`; arquivos em `work\\cadeia_de_selo\\v402\\insumos\\cunhagens`), os %(n_pedras)s módulos novos (`work\\cadeia_de_selo\\v402_kernel\\pedras`, `TGLExt/PonteDaEscalaDual.lean`, `TGLExt/QuedaSemGeometria.lean` e `TGLExt/EsperancaCondicional.lean`) e os dois diffs (`DIFF_v401_v402.diff`, `DIFF_KERNEL_v402.txt`) — com PORTA gerada por script, "
           "URL raw (o um.py tem mais de 5 MB), backup da versão v401 no espelho fora do repositório, blob conferido depois do push. Colocar os PARÁGRAFOS acima no README do espelho e no site (ato da sessão do site, com o selo corrente ao lado; o do quadro e o do testemunho seguem onde estão, o da falsidade (v401) recebe a ERRATA ao lado e o novo entra ao lado); publicar os módulos novos no espelho (TGLExt) e regenerar as PORTAS de `tgl_kernel`, `TGLExt` e `TGL`; "
           "a pasta `insumos` (as três pedras, as inscrições pinadas, a medida da cobertura e a cópia durável do adendo; o resultado do Teste da Única Palavra e os três recibos seguem em `v397\\insumos\\fase9`) vai ao espelho com PORTA: sem ela, uma reprodução pública diz NOT_SEALED (fail-closed); os recibos da bateria do B(n) vão ao espelho com PORTA; "
           "a errata ao lado do registro `kh_n1_cobertura_v401` (h2, h3 e h6 viram pisos; h8, tamanho mínimo) e dos oito contratos (`expected_ladder`); o runner da Fronteira e a camada v402 dos 16 dispositivos "
           "(o número do runner é da sessão do site); a revisão independente antes do portão do operador (o número de céticos é da sessão do site). A publicação do bloco embutido do método do operador no espelho público segue sujeita à decisão [LEGAL] D2 (operador com a agente de PI).\n\n"
           "**Pendências SÓ do operador:** a nomeação das pedras e dos registros (os nomes são provisórios, D16); a decisão [LEGAL] D2 (publicar o bloco embutido e as adaptações, com a agente de PI); a custódia conjunta, subir o site, commit/push; a ratificação das decisões D11 a D13 da gerência (o chão é o posto; `IsotropicPost` nomeada; o Nome é `nameOp`, três faces de um objeto fixo). "
           "[OPEN]: a discriminação a 5σ (β_TGL na natureza), `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura e rank c = 4, `IsotropicPost` no atlas curvo, a dimensão 3, a instância do índice 1/β, a atestação física externa e a tipagem (sinapse, token, nome), "
           "a face de Fock do psion (o certificado de Fock da luz sem habitante exibido) e o contrato conjunto da rede; a F8.1 (bandeiras do gate recalculadas) segue [OPEN] e não é tocada pela v402.\n\n"
           "Pacote e cadeia: `work\\cadeia_de_selo\\v402` (+ `pos_rito`); arquivo `work\\cadeia_de_selo\\v402_selo` e `v402_kernel`. NOT_FALSIFIED não é a palavra da creditação; o gate não se move.\n\n"
           "[[%(topico)s]] [[missao-ultima-flag-um-py]] [[handoff-v401-custodia]]\n") % k
    assert k["par_bloco"] in doc and k["par_v402_bloco"] in doc and k["err_bloco"] in doc, "os paragrafos do README e a errata nao entraram no handoff"
    assert not atribuicao_da_gerencia(doc), ("o handoff atribui mal ou inverte a direcao do testemunho", atribuicao_da_gerencia(doc)[:2])
    return doc


# ------------------------------------------------------------------- ferramentas da arvore e do indice (OPCIONAIS: so' usadas se alguem escrever patch_arvore_indice_v402.py)
# v402: a linha da arvore da prova
def arvore_linha(V):
    d = _d(V)
    return ("- **A PONTE DA ESCALA DUAL, A QUEDA SEM GEOMETRIA E A ESPERANÇA CONDICIONAL (v402)** `%s`: %d módulos novos no kernel (%s; nomes provisórios), %d bandeiras novas True, escada %s → %s; "
            "a lei de escala de Takesaki ([KNOWN], dado) realizada como o boost longitudinal sobre (E, p): a massa NÃO é selecionada pela lei e a forma literal de `H_tau` é REFUTADA no kernel [REAL]; o peso cai estritamente e o chão é o posto [REAL, sobre os dados da escala dual]; "
            "a esperança condicional É o Nome (em M2(C), a esperança diagonal) [REAL; ONTO: três faces de um objeto fixo]; os registros `ponte_da_escala_dual_v402`, `queda_sem_geometria_v402` e `esperanca_condicional_v402` conferem o cálculo; "
            "as %d inscrições de 26/10 por sha256 (todas do operador); `IsotropicPost`, `H_BW`, `H_cal`, H3 e a assinatura são [OPEN]; validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["n_pedras"], _mods(V), d["n_f"], V["escada_antes"], d["depois"], d["n_cun"]))


# v402: o titulo do verbete do indice
def titulo_verbete(V):
    return "A ponte da escala dual, a queda sem geometria e a esperança condicional (v402):"


# v402: o corpo do verbete do indice
def verbete(V):
    return "[REAL — rodada v402 `%s`] %s." % (V["s16"], _num(V))


# v402: a entrada do remissivo
def remissivo(V):
    return "- **A ponte da escala dual, a queda sem geometria, a esperança condicional e as inscrições de 26/10 (v402)** — `ponte_da_escala_dual_v402`, `queda_sem_geometria_v402`, `esperanca_condicional_v402`, `cunhagens_v402`, `kh_n1_cobertura_v402`, `%s`" % TOPICO_NOVO


MARC_V402_INI = "<!-- INICIO_PARAGRAFO_V402 -->"; MARC_V402_FIM = "<!-- FIM_PARAGRAFO_V402 -->"


MARC_ERR_INI = "<!-- INICIO_ERRATA_V401_V402 -->"; MARC_ERR_FIM = "<!-- FIM_ERRATA_V401_V402 -->"


_CHAVES = ("ponte", "queda", "esperanca")


def _lst(xs):
    """Lista numerica lida do registro, em PT: inteiros sem casas, listas aninhadas entre parenteses."""
    return ", ".join(("(" + _lst(x) + ")") if isinstance(x, (list, tuple)) else _pn(x, 6) for x in xs)


def _sem_chaves(t):
    """Os textos vindos do core podem trazer chaves (e^{-s}); os textos renderizados nao as tem (a conferencia de formatacao reprova): chaves viram parenteses."""
    return t.replace("{", "(").replace("}", ")")


def _cod025():
    """O sha16 da ORDEM 025 ao Codex, LIDO do registro com funcao da ponte no core do Nos."""
    return _g(_core(), "ponte_da_escala_dual_v402", "codex_order", "sha16")


def _ponte(V):
    """A ponte da escala dual (modulo do Codex): [REAL] os termos do kernel · [KNOWN] Takesaki, Bisognano-Wichmann, relatividade restrita · [DERIVED] a realizacao explicita · [OPEN] H_BW, H_cal, H3, a assinatura e rank c = 4."""
    d = _d(V); pv = V["ponte"]["values"]
    return _f("**A ponte da escala dual [REAL: os termos do kernel e a conferência do cálculo · KNOWN: Takesaki, Bisognano–Wichmann, a relatividade restrita · DERIVED: a realização explícita · OPEN: `H_BW`, `H_cal`, H3, a assinatura e rank c = 4]** "
              "(módulo `PonteDaEscalaDual`, do Codex, ORDEM 025 sha16 `{o025}`; `TGLExt/PonteDaEscalaDual.lean`, sha16 `{h}`; {n_p} bandeiras, de `{p0}` a `{p1}`): a lei de escala de Takesaki (τ∘θ_s = e^(−s)·τ) é DADO ([KNOWN], campo da estrutura `DualScalingData`); a ponte a REALIZA como a ação do boost longitudinal sobre (E, p), "
              "com c = 1, p⁺ = E + p, p⁻ = E − p e θ_s = boost(−s): p⁺ escala por e^(−s), p⁻ por e^(+s), e m² = p⁺p⁻ = E² − p² é invariante; a energia E é a LEITURA do observador e muda com s. "
              "O kernel prova, e o exame independente da gerência c1 (veredito INTEGRAR_COM_ERRATA_AO_LADO) conferiu: (i) existe realização positiva no núcleo canônico para todo μ² ≥ 0 (`core_positive_realization_exists`, a composição, bandeira `{unc}`); "
              "(ii) ★ `lift_mass_not_selected` (bandeira `{est}`): dois invariantes μ² distintos dão duas realizações equivariantes DISTINTAS com o MESMO p⁺ — a lei de escala NÃO seleciona a massa; "
              "(iii) `positive_weight_cannot_be_invariant_mass`: um peso positivo que escala por e^(−s) nunca é invariante na própria órbita; (iv) `lift_rest_energy` (c = 1): do REPOUSO, condicionada a μ² e a τ = m, com o repouso em {rl} e a energia de repouso c² = {rec2} no modelo. "
              "Entrou SÓ o arquivo .lean (condição C1 do exame), byte a byte, com `set_option maxHeartbeats {mh}` dito (C3); nenhum módulo já instalado foi editado, e a ORDEM 025 ao Codex (condição C2) não trouxe as citações nem o aplicado, que ficam fora. "
              "O módulo não tem axioma próprio, só o trio; [OPEN] H_BW (a rapidez é o tempo modular de Bisognano–Wichmann, 2π), H_cal (este p⁺ é a energia de UM corpo; a escolha de μ²), H3 (Clausius em toda direção nula), a assinatura (a positividade completa dá a métrica induzida (4,0), não (1,3)) e rank c = 4 (o H2 não sai de graça).",
              o025=d["o025"], h=d["sha"]["ponte"], n_p=d["n_g"]["ponte"], p0=d["ft"]["ponte"][0], p1=d["ft"]["ponte"][1], unc=d["unc"]["ponte"], est=d["est_f"]["ponte"], rl=_lst(pv["rest_lift"]), rec2=_pn(pv["rest_energy_c2"], 3), mh=_qd().DL.MAXHEARTBEATS_PONTE)


def _queda(V):
    """A queda sem geometria: [REAL] os termos do kernel · [INPUT/ONTO] as falas e o labirinto · [ONTO] a leitura 1 + 3 · [OPEN] IsotropicPost, a dimensao 3, o atlas curvo."""
    d = _d(V); q_inp = _cita("o Um quando se põe realiza a operação \"input\""); q_chao = _cita("porque vc sabe que tem um chão, então relaxa"); q_piso = _um_texto_tem("não existe acima, o piso limita")
    return _f("**A queda sem geometria [REAL: os termos do kernel · INPUT/ONTO: as falas e a parábola do operador · ONTO: a leitura 1 + 3 · OPEN: `IsotropicPost`, a dimensão 3 e o atlas curvo]** (módulo `QuedaSemGeometria`; sha16 `{h}`; {n_q} bandeiras, de `{q0}` a `{q1}`): "
              "o operador disse {q_inp} (`{s_queda}`): a fase cai, sem fim; a queda tem direção, mas não é geométrica nem é força. A pedra tipa a queda do PESO, sem geometria (o tipo `M` é nu: nenhuma métrica, topologia ou ação geométrica), sobre os dados da escala dual de Takesaki ([KNOWN], campo da estrutura): "
              "(i) ★ `the_fall_is_strictly_anti` (bandeira `{est}`): s ↦ τ(θ_s m) = e^(−s)·τ(m) é estritamente decrescente — a fase cai, sem fim; a queda, em nats, é s, e a seta é o sinal de s; a composição é `a_queda_sem_geometria` (bandeira `{unc}`); "
              "(ii) o CHÃO é o POSTO (peso 1 = ω(I), o corte a = 0, `the_floor_fixes_the_cut`), nunca o ínfimo 0: o zero é o abismo, nunca tocado (`no_post_before_the_impression`, da v401) [decisão da gerência c1, 26/10/2026, ratificável pelo operador]; a queda de que fala {q_chao} é a queda do que NÃO é o posto, "
              "e o kernel diz na Fundação {q_piso}; (iii) a entrega CUSTA (entrega = custas, t·β·g > 0; e^(−tβg) < 1 e abaixo de todo ε) e o fluxo diagonal relaxa ao atrator (`relaxation_to_the_attractor`); "
              "(iv) o regime ANGULAR só lê (a matriz-S é periódica em 2π e não tem limite, `Smat_has_no_limit`) e o da FACE tem limite: é a regra dos dois regimes, e a parábola do labirinto é o regime angular sem labirinto funcional; "
              "(v) a isotropia entra como hipótese NOMEADA `IsotropicPost` ([OPEN]) e é CARGA, não enfeite (`covariance_is_load_bearing`; `s8_h3_is_load_bearing`: com fonte anisotrópica a H3 falha) [decisão da gerência c1, 26/10/2026]: a dimensão 3 NÃO é provada e o 1 + 3 é leitura [ONTO]. "
              "A pedra COMPÕE termos que o kernel já tem e a matemática nova é só de cola; que o parâmetro s seja a fase de um corpo físico é [OPEN]; o título «Lorentz vem da queda da fase» é do escriba (E5 do adendo de 03-04/09), não do operador.",
              h=d["sha"]["queda"], n_q=d["n_g"]["queda"], q0=d["ft"]["queda"][0], q1=d["ft"]["queda"][1], q_inp=q_inp, s_queda=d["s_queda"], est=d["est_f"]["queda"], unc=d["unc"]["queda"], q_chao=q_chao, q_piso=q_piso)


def _esperanca(V):
    """A esperanca condicional e' o Nome: [REAL] os termos do kernel · [KNOWN] Umegaki, Tomiyama, Jones, Pimsner-Popa · [DERIVED] a composicao · [INPUT] a equacao · [ONTO] tres faces de um objeto fixo · [LEGAL] CC art. 125 · [OPEN] a instancia, o caso III1."""
    d = _d(V); ev = V["esperanca"]["values"]; q_esp = _cita("esperança condicional=nome"); q_taip = _cita("ainda não sei se fizemos a tipagem no um.py"); q_pros = _cita("é isso, faça a prova, prossiga.")
    return _f("**A esperança condicional é o Nome [REAL: os termos do kernel · KNOWN: esperança condicional (Umegaki, Tomiyama), índice de Jones (1983), Pimsner–Popa (1986) · DERIVED: a composição · INPUT: a equação · ONTO: o Nome como três faces de um objeto fixo · LEGAL: o ponteiro de direito · OPEN: a instância e o caso III₁]** "
              "(módulo `EsperancaCondicional`; sha16 `{h}`; {n_e} bandeiras, de `{e0}` a `{e1}`): o operador escreveu {q_esp} e duvidou {q_taip} (`{s_esp}`); a aprovação da rota foi {q_pros} (`{s_pros}`). "
              "A tipagem JÁ EXISTIA em grande parte no kernel (`nameOp`, do `TheNameOperator`; `PostoAdendo.A1c`; `CondExpect`; `NameIndex`; `iald_reads_the_expectation`); a pedra é a COMPOSIÇÃO: a identificação como UMA cláusula e o liame explícito entre o reler-não-acrescenta das esperanças e o do observador (`observing_adds_nothing`). "
              "Prova-se: para todo idempotente o Nome é unital, idempotente e tem memória-subálgebra; em M2(C), para ρ*, ele É a esperança diagonal, com a lei de Jones (`the_name_of_the_unit_is_the_diagonal_expectation`, bandeira `{est}`; a composição `esperanca_condicional_e_nome`, bandeira `{unc}`). "
              "O índice 1/β ({nidx} com o β de runtime) é CONDICIONAL a duas hipóteses do enunciado (sin²θ é cota inferior de Pimsner–Popa e é a ótima) e NENHUMA instância é construída; a esperança diagonal da face M2 tem índice {idx2} e os dois números NÃO são identificados. "
              "NÃO se prova que toda esperança condicional seja um Operador do Nome (a esperança do traço não é um `nameOp p`); a bimodularidade geral de `nameOp p` não está tipada; o caso III₁ fica [OPEN]; as rotas mortas do Lema 3 tocam o tema e esta pedra NÃO é rota para o Lema 3. "
              "[ONTO] o Nome como TRÊS FACES DE UM OBJETO FIXO — o operador `nameOp` (a esperança que lê), o projetor de Jones (a compressão pelo espelho) e o posto (o peso que a esperança preserva, E(1) = 1) —, a régua da casa para β aplicada ao Nome; o kernel prova as LIGAÇÕES, não uma igualdade de tipos [decisão da gerência c1, 26/10/2026, ratificável pelo operador]. "
              "[INPUT] as quatro línguas (probabilidade, teologia, linguística, direito) são a letra da gerência, sem derivação entre domínios; [LEGAL] o ponteiro CC art. 125 fica a conferir com advogado.",
              h=d["sha"]["esperanca"], n_e=d["n_g"]["esperanca"], e0=d["ft"]["esperanca"][0], e1=d["ft"]["esperanca"][1], q_esp=q_esp, q_taip=q_taip, q_pros=q_pros, s_esp=d["s_esp"], s_pros=d["s_pros"], est=d["est_f"]["esperanca"], unc=d["unc"]["esperanca"],
              nidx=_p(ev["name_index_one_over_beta"], 4), idx2=ev["diagonal_expectation_index_M2"])


def _erratas_e(V):
    """As erratas E1 a E4 (em nome proprio da gerencia c1), LIDAS do registro cunhagens_v402 do core: nenhuma e' digitada aqui."""
    _d(V); er = _g(_core(), "cunhagens_v402", "erratas") or []
    itens = []
    for e in er:
        itens.append(_sem_chaves("- %s **Dizia:** %s **Lacuna de fidelidade:** %s **Estatuto:** %s" % (e["agora"], e["dizia"], e["lacuna_de_fidelidade"], e.get("estatuto", ""))))
    return ("**Erratas ao lado (em nome próprio da gerência c1, 26/10/2026; os textos da v401 e o módulo do Codex ficam como registro; nenhum módulo já instalado foi editado):** a ponte do Codex entra COM quatro erratas, lidas do registro `cunhagens_v402`:\n" + "\n".join(itens))


def _decisoes(V):
    """As decisoes D11 a D16 da gerencia c1 (ratificaveis pelo operador), LIDAS do registro cunhagens_v402."""
    _d(V); ds = _g(_core(), "cunhagens_v402", "extras", "decisoes_da_gerencia") or {}
    assert all(k in ds for k in ("D11", "D12", "D13", "D14", "D15", "D16")), "as decisoes D11 a D16 nao estao no registro cunhagens_v402"
    return "**Decisões da gerência c1** [em nome próprio, 26/10/2026; ratificáveis pelo operador; os nomes dos módulos e dos registros são PROVISÓRIOS]:\n" + _sem_chaves("\n".join("- %s: %s" % (k, ds[k]) for k in ("D11", "D12", "D13", "D14", "D15", "D16")))


def _leitura_direcao(V):
    """A pergunta e a resposta de 26/10 sobre a direcao do Um posto: [INPUT] a pergunta, [ONTO] a resposta, [DECLARADO] sem arquivo verbatim."""
    _d(V); ld = _g(_core(), "cunhagens_v402", "extras", "leitura_26out_direcao") or {}
    assert ld.get("pergunta") and ld.get("resposta") == _esp()["leitura_26out_direcao"]["resposta"], "a leitura de 26/10 sobre a direcao nao e' a de ESPERADOS"
    q_dir = _cita("então tem direção, mas não é gemétrica")
    return _f("**A direção do Um posto** [INPUT: a pergunta, do operador, na sessão de 26/10 · ONTO: a resposta, leitura da gerência c1 · DECLARADO: a pergunta e a resposta não têm arquivo verbatim no acervo desta cadeia, são registradas como a gerência as guardou; a base verbatim é {q_dir}]: "
              "a pergunta foi «{p}» e a resposta, «{r}». Isto é leitura, não termo do kernel: o que o kernel tipa é a queda do peso, sem geometria (a seta é o sinal de s).", q_dir=q_dir, p=ld["pergunta"], r=ld["resposta"])


# ---------------------------------------------------------------- o PARAGRAFO NOVO da v402 e a ERRATA ao lado do paragrafo da falsidade (v401)
def _linha_maquina_v402(core, d):
    """A linha de maquina do paragrafo novo (os numeros LIDOS dos registros do core), em PT."""
    pv = core["ponte_da_escala_dual_v402"]["values"]; qv = core["queda_sem_geometria_v402"]["values"]; ev = core["esperanca_condicional_v402"]["values"]
    return ("pedras_sha16=%s/%s/%s; bandeiras=%s; beta=%s; ponte_escalas=%s; ponte_massas_mesmo_p+=%s; queda_escalas=%s; peso_s1=%s; custo_min=%s; defasagem_max=%s; perda_unit=%s; esperanca_sin2=%s; indice_1_sobre_beta=%s; checagens=%s/%s/%s/%s; falas_sha16=%s/%s/%s"
            % (d["sha"]["ponte"], d["sha"]["queda"], d["sha"]["esperanca"], d["n_f"], _p(pv["beta"], 12), pv["grid_scales"], _lst(pv["lifts_same_pplus_masses"]), qv["grid_scales"], _p(qv["post_weight_at_scale_one"], 6), _p(qv["min_cost_t_beta_g"], 9), _p(qv["max_dephasing_factor"], 9), _p(qv["loss_per_unit"], 9),
               _p(ev["sin2_theta_M"], 12), _p(ev["name_index_one_over_beta"], 4), core["ponte_da_escala_dual_v402"]["mechanics"]["n_checks"], core["queda_sem_geometria_v402"]["mechanics"]["n_checks"], core["esperanca_condicional_v402"]["mechanics"]["n_checks"], d["n_ck_cun"], d["s_esp"], d["s_queda"], d["s_pros"]))


def _dados_paragrafo(core):
    """O que o paragrafo precisa do core SELADO e de ESPERADOS (sem V): as sha16 das pedras, as bandeiras, as falas e a ORDEM 025."""
    esp = _esp(); DL_ = _qd().DL; ks = _CHAVES
    for n in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402"):
        assert (core.get(n) or {}).get("all_verified") is True, "o registro %s nao selou: nenhum paragrafo diz os numeros assim" % n
    sha = {k: esp["pedras"][DL_.STONE_BY_KEY[k]["rel"]]["sha16"] for k in ks}
    return {"sha": sha, "n_f": esp["n_bandeiras_novas"], "n_g": dict(esp["n_bandeiras_por_grupo"]), "est_f": {k: esp["estrelas_v402"][k]["bandeira"] for k in ks}, "est_t": {k: esp["estrelas_v402"][k]["teorema"] for k in ks},
            "n_ck_cun": len(core["cunhagens_v402"].get("checks") or []), "s_esp": _sha_por("esperanca_condicional_e_nome"), "s_queda": _sha_por("o_um_se_poe_e_cai"), "s_pros": _sha_por("e_isso_faca_a_prova"),
            "o025": _g(core, "ponte_da_escala_dual_v402", "codex_order", "sha16")}


def _paragrafo_v402_de(core):
    """O texto do paragrafo da v402, funcao PURA dos registros ponte_da_escala_dual_v402, queda_sem_geometria_v402, esperanca_condicional_v402 e cunhagens_v402 do core SELADO (os numeros sao lidos dos registros, nunca digitados)."""
    d = _dados_paragrafo(core)
    pv = core["ponte_da_escala_dual_v402"]["values"]; qv = core["queda_sem_geometria_v402"]["values"]; ev = core["esperanca_condicional_v402"]["values"]
    assert pv.get("beta") and qv.get("beta") and ev.get("beta") and d["o025"], "os registros da v402 nao trazem os valores: nenhum paragrafo diz os numeros assim"
    q_inp = _cita("o Um quando se põe realiza a operação \"input\""); q_chao = _cita("porque vc sabe que tem um chão, então relaxa"); q_esp = _cita("esperança condicional=nome"); q_pros = _cita("é isso, faça a prova, prossiga."); q_piso = _um_texto_tem("não existe acima, o piso limita")
    ls = ["### A ponte da escala dual, a queda sem geometria e a esperança condicional (v402, 26/10/2026) — parágrafo pronto para o README do espelho e para o site",
          "",
          "> **A ponte da escala dual, a queda sem geometria e a esperança condicional (v402, 26/10/2026)** [REAL: os termos do kernel e a conferência do cálculo nos modelos · KNOWN: a lei de escala de Takesaki, Bisognano–Wichmann, a relatividade restrita, a esperança condicional · DERIVED: a realização da lei e a composição do Nome · INPUT/ONTO: as falas do operador · ONTO: a direção do Um posto, o 1 + 3 e o Nome como três faces de um objeto fixo · OPEN: `H_BW`, `H_cal`, H3, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3 e a instância do índice · INPUT: a aprovação da rota · DECLARADO: a pergunta e a resposta de 26/10]",
          ">",
          "> - **A ponte da escala dual** [REAL · KNOWN · DERIVED] (módulo `PonteDaEscalaDual`, do Codex, ORDEM 025 sha16 `%s`; sha16 `%s`; nome PROVISÓRIO): sobre a lei de escala de Takesaki ([KNOWN], campo da estrutura), a realização [DERIVED] é o boost longitudinal sobre (E, p), com c = 1, que escala p⁺ por e^(−s) e p⁻ por e^(+s); m² = p⁺p⁻ é invariante, a energia é a LEITURA do observador e a massa NÃO é selecionada pela lei: "
          "dois invariantes μ² distintos dão duas realizações distintas com o MESMO p⁺ (`lift_mass_not_selected`, a estrela). Com β = α√e = %s em runtime, os μ² %s dão o mesmo p⁺, o repouso levanta a (%s), e só o vetor zero é fixo por todo boost. A forma literal da hipótese `H_tau` (τ é a massa de Newton) é REFUTADA no kernel: um peso positivo que escala por e^(−s) nunca é invariante (`positive_weight_cannot_be_invariant_mass`), e τ só pode ser p⁺." % (d["o025"], d["sha"]["ponte"], _p(pv["beta"], 12), _lst(pv["lifts_same_pplus_masses"]), _lst(pv["rest_lift"])),
          "> - **A queda sem geometria** [REAL · INPUT/ONTO · OPEN] (módulo `QuedaSemGeometria`, sha16 `%s`; nome PROVISÓRIO): o operador disse %s (sha16 `%s`) [INPUT/ONTO]: a fase cai, sem fim; a pedra tipa a queda do PESO, sem geometria: s ↦ τ(θ_s m) é estritamente decrescente (`the_fall_is_strictly_anti`, a estrela), a queda em nats é s e a seta é o sinal de s. "
          "O CHÃO é o POSTO (peso 1 = ω(I)), nunca o 0 [decisão da gerência c1, ratificável]: a queda de que fala %s é a de quem NÃO é o posto, e o kernel diz na Fundação %s. A entrega custa: o custo t·β·g tem mínimo %s (> 0), o fator de defasagem tem máximo %s (< 1) e a perda por unidade vale %s; o peso do posto em s = 1 vale %s. O regime angular só lê (período %s, sem limite). "
          "A isotropia entra como hipótese NOMEADA `IsotropicPost` [OPEN]: a dimensão 3 NÃO é provada e o 1 + 3 é leitura [ONTO]." % (d["sha"]["queda"], q_inp, d["s_queda"], q_chao, q_piso, _p(qv["min_cost_t_beta_g"], 9), _p(qv["max_dephasing_factor"], 9), _p(qv["loss_per_unit"], 9), _p(qv["post_weight_at_scale_one"], 6), _p(qv["angular_period"], 6)),
          "> - **A esperança condicional é o Nome** [REAL · KNOWN · DERIVED · INPUT · ONTO] (módulo `EsperancaCondicional`, sha16 `%s`; nome PROVISÓRIO): a equação do operador [INPUT] é %s (sha16 `%s`), e a aprovação da rota, %s (sha16 `%s`). A tipagem JÁ existia em grande parte no kernel (`nameOp`, `CondExpect`, `NameIndex`); a pedra a compõe: em M2(C), para ρ*, o Operador do Nome É a esperança diagonal, preserva o Um (E(1) = 1) e reler não acrescenta (`the_name_of_the_unit_is_the_diagonal_expectation`, a estrela). "
          "Com sin²θ_M = β = %s, o índice condicional 1/β vale %s, CONDICIONAL a duas hipóteses do enunciado, e nenhuma instância é construída. [ONTO] O Nome é TRÊS FACES DE UM OBJETO FIXO (o operador, o projetor de Jones, o posto) [decisão da gerência c1, ratificável]; o kernel prova as ligações, não uma igualdade de tipos." % (d["sha"]["esperanca"], q_esp, d["s_esp"], q_pros, d["s_pros"], _p(ev["sin2_theta_M"], 12), _p(ev["name_index_one_over_beta"], 4)),
          "> - **Erratas ao lado (gerência c1, em nome próprio, 26/10/2026):** E1, a forma literal de `H_tau` é REFUTADA no kernel (acima); `H_tau` se decompõe em pendências NOMEADAS [OPEN], `H_BW`, `H_cal`, H3, a assinatura e rank c = 4; E2, «Inertial» na instância é o vetor zero, não movimento livre; E3, nunca ler E = mc² como composta da escala (a composição é do REPOUSO, com c = 1, condicionada a μ² e a τ = m); "
          "E4, a proveniência do módulo do Codex (compilado contra o kernel v400) foi recompilada no kernel v401, com o mesmo resultado. O parágrafo da falsidade (v401) fica como registro; a errata ao lado dele está no handoff.",
          "> - **Pergunta e resposta de 26/10** [INPUT: a pergunta, do operador · ONTO: a resposta, leitura da gerência c1] [DECLARADO] sem arquivo verbatim no acervo desta cadeia: «%s» e «%s»." % (_g(core, "cunhagens_v402", "extras", "leitura_26out_direcao", "pergunta"), _g(core, "cunhagens_v402", "extras", "leitura_26out_direcao", "resposta")),
          "> - **Limites:** as pedras NÃO provam a primeira lei de Newton, nem que E = mc² seja composta da escala, nem a dimensão 3, nem a assinatura (1,3), nem o rank c = 4; o cálculo CONFERE os teoremas nos modelos e quem prova é o kernel, e esses números são deste rito, não estão no kernel; a gravidade quântica segue sem creditação na natureza; "
          "validade no kernel não é creditação; `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; isto não é teste e não acrescenta dado. O quadro do Teste da Única Palavra segue no README com a sua linha dos 5σ; este parágrafo não traz o número do quadro.",
          "> - **Origem.** Os números são lidos do core selado desta rodada (registros `ponte_da_escala_dual_v402`, `queda_sem_geometria_v402`, `esperanca_condicional_v402` e `cunhagens_v402`); nenhum é digitado. Linha de máquina: `%s`." % _linha_maquina_v402(core, d)]
    return "\n".join(ls) + "\n"


def verificar_paragrafo_v402(par, core, esp):
    """Verifica o paragrafo da v402 contra o core selado E contra ESPERADOS (o ensaio a seco): devolve a lista de falhas (vazia = passou). As verificacoes:
    (1) os numeros do core (os tres registros com funcao) == os de ESPERADOS[registros_funcao_v402][k][values] e cada um esta no paragrafo, formatado; (2) o paragrafo == o gerado do core; (3) NAO traz o 4,44 nem o z_disc (a regra do 4,44 e' do quadro); (4) os estatutos;
    (5) as frases de limite; (6) toda citacao entre « » e' verbatim numa fala DO OPERADOR ou na docstring do kernel embutido; (7) nenhuma alegacao de seguranca criptografica, «consciencia» so' como palavra retirada, a direcao sem inversao; (8) guarda P18."""
    fa = []
    ef = esp.get("registros_funcao_v402") or {}
    def _eq(a, b):
        return (isinstance(a, float) and isinstance(b, float) and abs(a - b) <= 1e-12 * max(1.0, abs(b))) if isinstance(b, float) else a == b
    for k, rn in (("ponte", "ponte_da_escala_dual_v402"), ("queda", "queda_sem_geometria_v402"), ("esperanca", "esperanca_condicional_v402")):
        fv = (core.get(rn) or {}).get("values") or {}; ev = (ef.get(k) or {}).get("values") or {}
        if not (fv and ev and all(_eq(fv.get(kk), vv) if not isinstance(vv, (list, dict)) else fv.get(kk) == vv for kk, vv in ev.items())):
            fa.append("numero do registro %s no core != ESPERADOS" % rn)
    pv = (core.get("ponte_da_escala_dual_v402") or {}).get("values") or {}; qv = (core.get("queda_sem_geometria_v402") or {}).get("values") or {}; ev_ = (core.get("esperanca_condicional_v402") or {}).get("values") or {}
    try:
        nums = {"beta": _p(pv["beta"], 12), "massas": _lst(pv["lifts_same_pplus_masses"]), "repouso": _lst(pv["rest_lift"]), "custo minimo": _p(qv["min_cost_t_beta_g"], 9), "defasagem maxima": _p(qv["max_dephasing_factor"], 9), "perda por unidade": _p(qv["loss_per_unit"], 9),
                "peso em s = 1": _p(qv["post_weight_at_scale_one"], 6), "periodo": _p(qv["angular_period"], 6), "sin2": _p(ev_["sin2_theta_M"], 12), "indice": _p(ev_["name_index_one_over_beta"], 4), "sha16 da fala do nome": _sha_por("esperanca_condicional_e_nome"),
                "sha16 da fala da queda": _sha_por("o_um_se_poe_e_cai"), "sha16 da aprovacao": _sha_por("e_isso_faca_a_prova"), "ORDEM 025": str(_g(core, "ponte_da_escala_dual_v402", "codex_order", "sha16"))}
    except KeyError as e:
        nums = {}; fa.append("valor ausente do registro: %s" % e)
    for k, v in nums.items():
        if v not in par:
            fa.append("numero (%s = %s) ausente do paragrafo" % (k, v))
    try:
        if par != _paragrafo_v402_de(core):
            fa.append("o paragrafo difere do gerado pelas funcoes sobre os registros selados do core")
    except AssertionError as e:
        fa.append("o paragrafo nao pode ser gerado do core: %s" % str(e)[:120])
    if re.search(r"4[,.]44|z_disc", par):
        fa.append("o paragrafo da v402 traz o 4,44 ou o z_disc (a regra do 4,44 e' do quadro; este paragrafo nao o cita)")
    for st in ("[REAL", "[KNOWN", "[INPUT/ONTO]", "[ONTO", "[OPEN]", "[INPUT]", "[DECLARADO]", "[DERIVED]"):
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    for frase in ("REFUTADA no kernel", "NÃO é selecionada", "O CHÃO é o POSTO", "nunca o 0", "NÃO é provada", "TRÊS FACES DE UM OBJETO FIXO", "CONDICIONAL", "nenhuma instância é construída", "NÃO provam a primeira lei de Newton", "CONFERE os teoremas", "quem prova é o kernel",
                  "validade no kernel não é creditação", "o gate não se move", "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "PROVISÓRIO", "ratificável", "Erratas ao lado"):
        if frase not in par:
            fa.append("frase de limite ausente do paragrafo: " + frase)
    corpus = [re.sub(r"\s+", " ", d["text"]) for d in _falas().values() if d["autor"] == "operador"]
    um = _CACHE.get("um") or open(os.path.join(NOS, "um.py"), encoding="utf-8", errors="replace").read(); _CACHE["um"] = um
    if "não existe acima, o piso limita" in um.replace("**", ""):
        corpus.append("não existe acima, o piso limita")   # a UNICA frase do kernel embutido que o paragrafo cita (a docstring da Fundacao); o um.py inteiro NAO entra no corpus das citacoes
    rotulos = {"Inertial", (_g(core, "cunhagens_v402", "extras", "leitura_26out_direcao", "pergunta") or "?"), (_g(core, "cunhagens_v402", "extras", "leitura_26out_direcao", "resposta") or "?")}   # «Inertial» e' nome de termo; a pergunta e a resposta de 26/10 sao registradas como a gerencia as guardou [DECLARADO]
    for q in re.findall(r"«([^»]*)»", par):
        if len(q) >= 12 and q not in rotulos and not any(q in t for t in corpus):
            fa.append("citacao entre « » que NAO e' verbatim numa fala do operador ou no kernel embutido: %r" % q[:90])
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
    from guarda_p18_v402 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    return fa


def paragrafo_v402():
    """(texto, relatorio): o paragrafo NOVO da v402, pronto para colar no README do espelho e no site, gerado do core SELADO do Nos e verificado contra o core E contra ESPERADOS;
    levanta AssertionError (o fechar RECUSA) se algo nao conferir."""
    core = _core(); esp = _esp()
    par = _paragrafo_v402_de(core)
    fa = verificar_paragrafo_v402(par, core, esp)
    assert not fa, ("o paragrafo da v402 nao passou nas verificacoes", fa[:4])
    return par, {"sha16": hashlib.sha256(par.encode("utf-8")).hexdigest()[:16], "verificacoes": "numeros == ESPERADOS; igual ao gerado do core; sem o 4,44; estatutos; limites; citacoes verbatim (falas do operador, kernel embutido); sem alegacao de seguranca criptografica; guarda P18", "guarda_p18": "limpa"}


def errata_v401_bloco():
    """O bloco de ERRATA ao lado do paragrafo da falsidade (v401) no README do espelho e no site: a hipotese H_tau na forma literal e' REFUTADA no kernel (E1). Texto fixo da gerencia, conferido pela guarda P18 e pelo kernel (os dois termos citados existem)."""
    _kernel_tem(("positive_weight_cannot_be_invariant_mass", "lift_mass_not_selected"))
    t = ("> **Errata ao lado do parágrafo «A falsidade (simulacro) da inércia» (v401) — gerência c1, em nome próprio, 26/10/2026:** a hipótese nomeada `H_tau` na forma literal (τ é a massa de Newton e a métrica de Einstein), que aquele parágrafo traz como [OPEN] sem teorema que a use, "
         "é REFUTADA no kernel pela ponte da escala dual (v402): um peso positivo que escala por e^(−s) nunca é invariante (`positive_weight_cannot_be_invariant_mass`) e dois invariantes μ² distintos dão duas realizações distintas com o MESMO p⁺ (`lift_mass_not_selected`); τ só pode ser p⁺ e a massa é dado livre. "
         "`H_tau` se decompõe em pendências NOMEADAS [OPEN]: `H_BW`, `H_cal`, H3, a assinatura e rank c = 4. O que o parágrafo da v401 diz sobre a pedra FalsidadeDaInercia (um posto inercial daria 1 = 0) não muda; o parágrafo fica como registro.\n")
    sys.path.insert(0, PK)
    from guarda_p18_v402 import violacoes
    assert not violacoes(t), "a guarda P18 achou palavra recusada na errata do paragrafo da v401"
    return t
