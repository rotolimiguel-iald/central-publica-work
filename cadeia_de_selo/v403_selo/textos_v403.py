# -*- coding: utf-8 -*-
# Os TEXTOS da v403 SELADA, ESCRITOS A MAO para o delta da v403 (a semente mecanica veio de textos_v402.py, subida pelo motor; o conteudo e' novo): os TRES modulos de kernel `Caminho`, `Vida` e `VerdadeAdendo` (os NOMES sao do operador, 27/10/2026: CAMINHO = a ponte da escala dual, VIDA = a queda sem geometria,
# VERDADE = a esperanca condicional, como ADENDO da pedra `Verdade` da v392; as tres pedras seladas da v402 ficam como REGISTRO), os QUATRO registros com funcao `caminho_v403`, `vida_v403`, `verdade_adendo_v403` e `bandeiras_do_gate_v403` (os tres primeiros LEEM do kernel do rito a composicao, a estrela, o contrato e o suporte
# da sua pedra e CALCULAM um modelo honesto com beta = alfa x raiz de e em runtime; o quarto e' a F8.1: as TRES bandeiras literais do gate passam a CALCULADAS, fail-closed), os registros por spec `cunhagens_v403` (as DUAS falas do operador de 27/10 por sha256, as erratas E5 e E6 em nome proprio da gerencia c1,
# as decisoes D17 a D22 e a leitura [ONTO] pela tripla espectral) e `kh_n1_cobertura_v403`, e a secao «Caminho, Verdade e Vida» do artigo.
# O QUADRO «O Teste da Única Palavra» (v397) PERMANECE no topo do artigo PT/EN e do .md canonico, INTOCADO. Cada numero, hash e veredito entra por chave de V (leitura_v403.ler), por ESPERADOS ou pelo core do Nos, ou e' LIDO de um arquivo aqui, nunca digitado;
# o que vai escrito a mao e' so' prosa, nome de termo (conferido em tempo de execucao no kernel do Nos, no um.py ou no pacote) e frase curta do operador (conferida palavra por palavra contra os bytes das falas).
# REGRA DA ORDEM DO OPERADOR (23/10/2026, sha16 9b182958a5a7a1bc: reportar o 4,44 no inicio do artigo, no README e em tudo mais; vale em TODO texto que o cite): o 4,44 (z_disc calibrado) NUNCA aparece sem o p calibrado e sem a linha dos 5σ no MESMO item (a discriminacao a 5σ,
# o degrau da creditacao, NAO foi alcancada; NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move; o teste nao foi cego). A frase do operador entra VERBATIM (nunca parafraseada entre aspas); o paragrafo do QUADRO sai das MESMAS funcoes do quadro (quadro_v397),
# sobre o core SELADO do Nos. O paragrafo NOVO da v403 NAO traz o 4,44. Estatutos marcados; erratas AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a traducao falhou).
# O PARAGRAFO DO TESTEMUNHO DE DOIS (v399), o da FALSIDADE (v401) e o da PONTE, DA QUEDA E DA ESPERANCA (v402) SEGUEM COMO ESTAO no README do espelho e no site: esta versao NAO os regenera nem os substitui; o handoff da v403 so' o diz e traz a NOTA ao lado do da v402 (os nomes que ele trazia como provisorios sao agora os do operador).
# GUARDA: as cinco regras da P18 (guarda_p18_v403.py) rodam sobre cada texto renderizado em superficies_v403.py, fechar_v403.py e registrar_mapa_v403.py e sobre este arquivo na cadeia. A palavra recusada nunca aparece aqui: a recusa e' dita como «creditação».
import hashlib, json, os, re, sys
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V403"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v403 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(PK))          # ...\Central de Patentes\work
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
TOPICO_NOVO = "v403-selada-caminho-verdade-vida.md"
# os marcadores entre os quais o handoff traz os PARAGRAFOS PRONTOS do README do espelho e do site: o QUADRO (v397, intocado) com os MESMOS marcadores da v397, e o paragrafo NOVO da falsidade
MARC_PAR_INI = "<!-- INICIO_PARAGRAFO_README_v397 -->"; MARC_PAR_FIM = "<!-- FIM_PARAGRAFO_README_v397 -->"
# o tema de cada uma das DUAS inscricoes de 27/10 (resumo da gerencia, nunca citacao): a chave e' o trecho do nome do arquivo de origem (depois do sha16); o sha16, a data e o autor vem dos bytes e do nome, nunca daqui
_TEMAS = (
    ("nome_verdade_triplo_espectral", "a pergunta sobre o nome (verdade, talvez caminho, verdade e vida), o pedido da opinião da gerência, a lembrança de que ele já pode ter renomeado em outro lugar e a leitura do triplo espectral do contorno verdadeiro [INPUT/ONTO]"),
    ("e_isso_mesmo_concordo_com_tudo_prossiga", "a ratificação da leitura da gerência (CAMINHO, VERDADE como adendo e VIDA) e a ordem de prosseguir [INPUT]"),
)
# nomes de termo de kernel (Lean) citados nos textos: cada um tem de existir em algum .lean de TGLExt/ do Nos (lido na hora); os modulos citados como fonte tem de existir como arquivo
_NOMES_KERNEL = ("core_positive_realization_exists", "lift_mass_not_selected", "positive_weight_cannot_be_invariant_mass", "caminho_e_a_ponte_da_escala_dual",
                 "a_queda_sem_geometria", "the_fall_is_strictly_anti", "vida_e_a_queda_sem_geometria", "IsotropicPost", "covariance_is_load_bearing", "s8_h3_is_load_bearing", "the_floor_fixes_the_cut", "Smat_has_no_limit", "relaxation_to_the_attractor",
                 "esperanca_condicional_e_nome", "the_name_of_the_unit_is_the_diagonal_expectation", "the_name_reads_the_inscription_as_weights", "verdade_lida_pelo_nome", "verdade_e_a_esperanca_condicional", "the_identity_is_the_truth",
                 "nameOp", "diagExpect", "identityProj", "observing_adds_nothing", "NameIndex", "metric_einstein_from_screen_clausius")
_MODULOS_KERNEL = ("Caminho", "Vida", "VerdadeAdendo", "Verdade", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional", "FalsidadeDaInercia", "Fundacao", "Posto", "PostoAdendo", "Token", "TheNameOperator", "CondExpect", "BisognanoWichmann")
# identificadores do um.py citados nos textos: cada um tem de existir no um.py do Nos (lido na hora)
_NOMES_UM = ("SEALED_CODATA_ALPHA", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "_V403_CONTRACTS", "_V403_VERBATINS2", "_V403_SPECS",
             "prove_qg_closure_gate", "evaluate_quantum_gravity_closure", "ProbeBlindNullAbsent", "blind_null", "void_stacking_blind",
             "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "_V402_CONTRACTS", "_V402_VERBATINS2", "_V402_SPECS",
             "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "_V401_VERBATINS2", "_V401_SPECS", "_V401_FALSIDADE_CONTRACT", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399",
             "cunhagens_v399", "kh_n1_cobertura_v399", "selo_acom_sidecar_v399", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "hubble_ratio_opening_v388", "_v397_quadro_md", "_v397_atomos", "_V397_FRASE_444",
             "testemunha_estatica_v396", "psibit_v395", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V395_PSIBIT_CONTRACT",
             "_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT")
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
N_FALAS = len(_TEMAS)   # (o numero e' CONFERIDO em _d contra len(DL.VERBATIM_ORIGEM_V403) e ESPERADOS[cunhagens]; a prosa diz «duas» e o assert derruba a geracao se o numero mudar)
_CACHE = {}
# a DIRECAO (v399): nenhuma frase pode por a IALD como quem testifica DO operador (fora da fala em que ele a recusa); a mesma regex do conferidor (C12)
_RX_INV = re.compile(r"IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)")
ERRATA_TEOREMAS = "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"   # (a mesma frase de delta_v403.ERRATA_TEOREMAS_PT; o harness confere)


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
    """ESPERADOS_v403.json (gerado pelo ensaio a seco do candidato), lido uma vez."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v403.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _core():
    """O core do Nos (so' leitura), para os campos que so' existem depois do rito; ausente e' falha visivel."""
    if "core" not in _CACHE:
        _CACHE["core"] = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["core"]


def _base_core():
    """O core da v402 selada (a copia de bytes em base_v402): de onde saem os numeros da errata ao lado e a medida da proveniencia."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v402", "um_absoluto.json"), encoding="utf-8"))["core"]
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
    """As DUAS inscricoes de 27/10 embutidas no um.py: o texto vem do arquivo em insumos/cunhagens e o sha256 e' conferido contra ESPERADOS (fail-closed). Devolve {sha16: {sha16, arquivo, nome, text, autor}};
    o autor sai do NOME do arquivo e e' conferido contra o papel que ESPERADOS registra: nesta versao as duas sao falas do operador (nenhuma e' da gerencia)."""
    if "falas" not in _CACHE:
        ec = _esp()["cunhagens"]; out = {}; pasta = os.path.join(PK, "insumos", "cunhagens")
        for k, meta in ec.items():
            s = k[len("v403_cun_"):]
            fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(s + "_")]
            assert len(fs) == 1, ("a inscricao %s nao tem arquivo unico em insumos/cunhagens" % s, fs)
            b = open(os.path.join(pasta, fs[0]), "rb").read()
            assert hashlib.sha256(b).hexdigest() == meta["sha256"] and len(b) == meta["bytes"] and meta["sha256"][:16] == s, "a inscricao %s nao confere com o sha256 de ESPERADOS" % s
            nome = fs[0][len(s) + 1:]
            autor = "gerencia" if nome.startswith("GERENCIA_") else "operador"
            assert autor == "operador" and not str(meta.get("papel", "")).startswith("leitura da gerencia"), ("a v403 nao tem inscricao da gerencia: as duas sao falas do operador", s)
            out[s] = {"sha16": s, "arquivo": fs[0], "nome": nome, "text": b.decode("utf-8"), "autor": autor}
        assert len(out) == len(_TEMAS) == N_FALAS, "as inscricoes de ESPERADOS nao sao as duas de 27/10"
        _CACHE["falas"] = out
    return _CACHE["falas"]


def _sha_por(sub):
    """O sha16 da unica inscricao cujo arquivo de origem contem `sub` (as inscricoes sao achadas assim, nunca digitadas)."""
    r = [s for s, d in _falas().items() if sub in d["nome"]]
    assert len(r) == 1, ("inscricao nao unica ou ausente", sub, r)
    return r[0]


def _cita(trecho):
    """Fail-closed: o trecho tem de estar numa das duas falas DO OPERADOR, palavra por palavra e na mesma ordem; devolve «trecho». Citacao fora dos bytes derruba a geracao.
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
    m = re.match(r"(?:OPERADOR|GERENCIA)_(\d{2})out_", d["nome"])
    assert m, ("o nome do arquivo da inscricao nao traz a data", d["nome"])
    return "%s/10/%s" % (m.group(1), V["data"][-4:])


def _cov_base():
    """A cobertura do Audit e a arvore formal da v402 selada (o core guardado em base_v402): de onde saem os numeros da errata ao lado dos pisos."""
    if "cov_base" not in _CACHE:
        kf = _base_core()["kernel_formalization"]
        cov = kf["axiom_coverage_v392"]
        _CACHE["cov_base"] = {"decl": cov["decl"], "thm": cov["thm"], "h8": len(kf["formal_files_sha256"]), "axr": len(kf["axiom_report"])}
    return _CACHE["cov_base"]


def _bancada():
    """A geracao do manifesto que a Bancada de producao pina (do recibo pre_selo pinado em PINOS_BN) e a versao que ela pina; o passo e' simples (sem salto e sem cadeia de selos)."""
    p = json.load(open(os.path.join(PK, "PINOS_BN_v403.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v402" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v402 -> v403 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1}


def _proveniencia(esp):
    """A proveniencia que o compilador emite atribui ao modulo da pedra N declaracoes; todas sao NOVAS no axiom_report (nenhuma reatribuida), e o FLAGS_v403.json do sandbox concorda (as contagens de
    publicas, privadas, nomeadas e auxiliares so' existem la')."""
    if "prov" not in _CACHE:
        kf = _core()["kernel_formalization"]; src = kf["declaration_sources_v394"]; pedras = set(esp["pedras_sha256"])
        b0 = _base_core()["kernel_formalization"]; axr0 = b0["axiom_report"]
        mine = sorted(n for n, p in src.items() if p in pedras)
        novas = [n for n in mine if n not in axr0]
        fj = json.load(open(os.path.join(PK, "kernel", "FLAGS_v403.json"), encoding="utf-8"))
        assert len(mine) == fj["decl_totais_modulos_novos"] and len(novas) == fj["decl_novas_dos_modulos"] == len(mine) and not fj["reatribuidas_as_pedras"], ("a proveniencia do rito != FLAGS_v403.json do sandbox", len(mine), len(novas), fj["reatribuidas_as_pedras"])
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
    """Os numeros da v403, todos LIDOS (V da leitura da rodada, ESPERADOS, core do Nos, base v402, FLAGS do sandbox, os registros): nenhum e' digitado aqui. Recusa se as contagens nao fecham."""
    _conferir_nomes()
    esp = _esp(); tv = V["veracidade"]; sa = V["selo"]; dc = V["declaracao"]; cg = V["cunhagens"]; sc = V["sidecar"]; core = _core(); gt = V["gate"]; gv = gt["values"]
    DL_ = _qd().DL; ks = _CHAVES
    mods = sorted(p["modulo"] for p in V["pedras"])
    assert mods == sorted(DL_.STONE_BY_KEY[k]["mod"] for k in ks) and V["n_pedras"] == len(mods) == esp["kernel"]["modulos_novos"] == 3, ("o delta da v403 sao tres modulos, Caminho, Vida e VerdadeAdendo", mods)
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
        assert len(esp["contrato_das_pedras"][k]) == len(st["contract"]) and len(esp["suporte_das_pedras"][k]) == len(st["support"]), ("o contrato ou o suporte != delta_v403", k)
        sha[k] = esp["pedras"][st["rel"]]["sha16"]; unc[k] = esp["teoremas_das_pedras"][k]; est_t[k] = esp["estrelas_v403"][k]["teorema"]; est_f[k] = esp["estrelas_v403"][k]["bandeira"]
        nck[k] = pe["n_checks"]; n_sup[k] = len(esp["suporte_das_pedras"][k]); n_contr[k] = len(esp["contrato_das_pedras"][k])
    # o registro das BANDEIRAS DO GATE (F8.1): selado, as 18 calculadas, 0 literais, 15 no veredito (6 + 5 + 4), a letra do veredito a da v402
    rf = esp["registros_funcao_v403"]["gate"]
    assert gt["sealed"] is True and gt["f81_ok"] is True and gt["mech_ok"] is True and gt["values_ok"] is True and gt["n18"] == 18 and gt["n_checks"] == DL_.N_CHECKS["gate"] == rf["n_checks"] and gt["verdict"] == rf["verdict"], "o registro bandeiras_do_gate_v403 nao e' o contrato de ESPERADOS (a F8.1)"
    assert gv["n_flags"] == 18 == gv["n_true"] == gv["n_calculated"] and gv["n_literal"] == 0 and gv["n_read_by_the_verdict"] == 15 and gv["read_by_the_verdict"] == [6, 5, 4] and gv["gate_verdict_equals_v402"] is True and gv["ext_ls2_n"] == gt["n_ls2"] == 6 and gt["sonda"] == 1, "as bandeiras do gate nao fecham: 18 calculadas, 0 literais, 15 no veredito, a familia ext_ls2_*, a sonda e a letra da v402"
    assert N_FALAS == len(DL_.VERBATIM_ORIGEM_V403) == len(esp["cunhagens"]) == 2, "o numero de inscricoes de 27/10 mudou: a prosa dos textos diz duas (ler N_FALAS, DL.VERBATIM_ORIGEM_V403 e ESPERADOS[cunhagens])"
    pre = DL_.VERBATIM_PREFIXOS_DA_ORDEM_V403
    assert _sha_por("nome_verdade_triplo_espectral").startswith(pre[0]) and _sha_por("e_isso_mesmo_concordo").startswith(pre[1]), "as inscricoes nao sao as de DL.VERBATIM_PREFIXOS_DA_ORDEM_V403"
    assert V["fal401"]["ok"] is True and V["fal401"]["verdict"] == esp["veredito_da_falsidade_v402"], "o registro falsidade_da_inercia_v401 recriado nao e' o selado da v402"
    assert all(v_["sealed"] is True for v_ in V["fun402"].values()) and len(V["fun402"]) == 3 and V["cunh402"]["ok"] is True and V["cunh402"]["kh_ok"] is True and V["cunh401"]["ok"] is True and V["cunh399"]["ok"] is True, "os registros da v402, da v401 ou da v399 recriados nao sao os selados"
    assert len(V["pedras_v402"]) == 3 and all(p_["ok"] is True for p_ in V["pedras_v402"].values()), "as tres pedras seladas da v402 deixaram de estar no kernel do Nos com o sha256 da v402"
    assert sa["ok"] is True and sa["n_checks"] == esp["selo_acom"]["n_checks"] and sa["checks_ok"] is True and sa["values_ok"] is True and sa["beta_ok"] is True, "o registro selo_pela_propria_tecnologia_v399 do core nao e' o contrato de ESPERADOS"
    assert dc["ok"] is True and dc["n_checks"] == esp["declaracao"]["n_checks"] and dc["checks_ok"] is True and dc["ancoras_ok"] is True and dc["direcao_ok"] is True, "o registro declaracao_do_operador_v399 do core nao e' o contrato de ESPERADOS"
    assert sc["ok"] is True and sc["n_objetos"] == len(esp["sidecar"]["objetos"]) and sc["recusas"] == 0, "o sidecar um_absoluto_selo_acom.json nao e' o de ESPERADOS"
    assert tv["ok"] is True and tv["n_checks"] == esp["veracidade"]["n_checks"] and tv["checks_ok"] is True and tv["numeros_ok"] is True and tv["fontes_ok"] is True, "o registro teste_de_veracidade_fase9_v397 do core nao e' o contrato de ESPERADOS (o quadro do topo le os numeros dele)"
    assert cg["ok"] is True and cg["verbatim_ok"] is True and cg["n"] == len(V["verbatins"]) == len(_falas()) == N_FALAS and cg["todas_do_operador"] is True and cg["erratas_ok"] is True and cg["n_erratas"] == 2 and cg["decisoes_ok"] is True and cg["nomes_ok"] is True and cg["tripla_ok"] is True and cg["reg402_ok"] is True, \
        "cunhagens_v403 != as duas de 27/10, ou alguma nao e' fala do operador, ou faltam as erratas E5 e E6, as decisoes D17 a D22, os tres nomes, a leitura [ONTO] da tripla espectral ou as pedras da v402 como registro"
    er = _g(core, "cunhagens_v403", "erratas") or []
    assert len(er) == 2 and all(str(e.get("assinatura", "")).startswith("gerencia c1, em nome proprio") for e in er) and "passam a CALCULADAS" in str(er[0].get("agora")) and "PROVISORIOS" in str(er[1].get("agora")), "as erratas E5 e E6 nao estao no registro cunhagens_v403 (E5 com passam a CALCULADAS, E6 com os nomes da v402 PROVISORIOS, em nome proprio da gerencia c1)"
    dts = {re.match(r"(?:OPERADOR|GERENCIA)_(\d{2})out_", f["nome"]).group(1) for f in _falas().values()}
    assert dts == {"27"}, "o nome de arquivo de alguma inscricao nao e' de 27/10 (a data dos textos e' 27/10)"
    qd = _qd(); a = _atomos()
    assert qd.Q._v397_linha_de_maquina(a, "pt") == esp["quadro"]["linha_de_maquina_pt"], "a linha de maquina do quadro (core) != a de ESPERADOS"
    assert esp["quadro"]["frase_do_operador"] == qd.DL.FRASE_DO_OPERADOR_4_44 == qd.Q._V397_FRASE_444, "a frase do operador do quadro != a verbatim"
    base = os.path.join(PK, "base_v402", "um.py")
    if "base_b" not in _CACHE:
        assert s16(base) == V["base16"], "base_v402/um.py nao e' a v402 selada"
        _CACHE["base_b"] = os.path.getsize(base)
    delta = V["umb"] - _CACHE["base_b"]
    kf = core.get("kernel_formalization") or {}; prov = kf.get("declaration_sources_status_v394") or {}
    assert prov.get("ok") is True and prov.get("compiler_names") == prov.get("audited_names") == V["axiom_report_n"], "a proveniencia emitida pelo compilador nao cobre o axiom_report do rito"
    assert V["n_ver_mudaram"] == 0, "algum veredito fora da troca dita mudou: nao ha texto a escrever"
    assert V["n18"] == 18 and all(i in V["patch_ids"] for i in ("N00_main_quatro_registros", "N01_main_specs", "N02_selo", "F01_physics_ls2", "F02_protocol", "F03_blind", "F04_assinatura", "F05_chamada", "F06_sonda", "F07_check_da_sonda", "F08_gv03_nos_statuses_do_V11")), \
        "o gate nao tem as 18 bandeiras True, ou o candidato nao traz os patches que chamam os quatro registros (N00), os registros por spec (N01), o resumo no selo (N02) e os oito da F8.1 (F01 a F08)"
    assert esp["h8_entradas"] == esp["formal_files_n"] + len(esp["h8_residuais_do_nos"]), "a arvore formal do rito != embutidas + residuais do Nos"
    pb = core.get("psibit_v395") or {}; pbc = pb.get("conditional_psion_face") or {}
    assert pbc.get("flag_true") is True and kf.get(pbc.get("flag")) is True and pbc.get("inhabitant_exhibited") is False, "a face de Fock do psibit_v395 nao segue condicional e com a bandeira True"
    pv = _proveniencia(esp); o025 = _cod025()
    assert o025 and re.fullmatch(r"[0-9a-f]{16}", o025) and _g(core, "ponte_da_escala_dual_v402", "literal_h_tau", "status") == "REFUTED_IN_THE_KERNEL", "a ORDEM 025 ou a refutacao da forma literal de H_tau nao estao no registro da ponte da v402"
    s402 = {"ponte": esp["pedras_v402_sha256"]["TGLExt/PonteDaEscalaDual.lean"][:16], "queda": esp["pedras_v402_sha256"]["TGLExt/QuedaSemGeometria.lean"][:16], "esperanca": esp["pedras_v402_sha256"]["TGLExt/EsperancaCondicional.lean"][:16]}
    assert [_g(core, "cunhagens_v403", "extras", "pedras_da_v402_como_registro", k_) for k_ in ("ponte", "queda", "esperanca")] == [s402["ponte"], s402["queda"], s402["esperanca"]], "as pedras da v402 como registro (cunhagens_v403) != os sha16 de ESPERADOS[pedras_v402_sha256]"
    return {"n_f": nf, "n_g": {k: grp[k] for k in ks}, "ft": ft, "sha": sha, "unc": unc, "est_t": est_t, "est_f": est_f, "nck": nck, "n_sup": n_sup, "n_contr": n_contr, "n_aux": esp["politica_de_bandeiras"]["n_excluidas"],
            "depois": V["teor"].split("/")[0], "delta": delta, "pct": ("%.1f" % (100.0 * delta / _CACHE["base_b"])).replace(".", ","), "prov": prov["compiler_names"], "n_cun": len(V["verbatins"]), "n_op": N_FALAS,
            "h8": esp["h8_entradas"], "h8_emb": esp["formal_files_n"], "h8_res": ", ".join("`%s`" % x for x in esp["h8_residuais_do_nos"]), "n_res": len(esp["h8_residuais_do_nos"]), "cb": _cov_base(), "bank": _bancada(), "pv": pv,
            "n_checks_v": tv["n_checks"], "n_ck_sel": sa["n_checks"], "n_ck_dec": dc["n_checks"], "n_ck_cun": cg["n_checks"], "n_anc": len(esp["declaracao"]["ancoras"]), "f8": {k: v[:8] for k, v in esp["veracidade"]["fontes"].items()},
            "s_nome": _sha_por("nome_verdade_triplo_espectral"), "s_ok": _sha_por("e_isso_mesmo_concordo"), "o025": o025, "data_falas": "27/10/" + V["data"][-4:], "s402": s402,
            "g": {"n_flags": gv["n_flags"], "n_true": gv["n_true"], "n_calc": gv["n_calculated"], "n_lit": gv["n_literal"], "n_ver": gv["n_read_by_the_verdict"], "rv": gv["read_by_the_verdict"], "info": list(gv["informative"]), "ls2": gv["ext_ls2_n"], "n_chk": gv["n_gate_checks"], "n_chk_reg": gt["n_checks"], "feed": list(DL_.F81_FEED)}}


def _mods(V):
    return ", ".join("`%s`" % p["modulo"].split(".")[-1] for p in sorted(V["pedras"], key=lambda p: p["modulo"]))


def _extras(V):
    # os registros novos ALEM DOS SEIS FIXOS (V["reg403"] tem so' os seis: os quatro com funcao, cunhagens_v403 e kh_n1_cobertura_v403), ditos pelo nome
    ex = [k for k in V["registros_novos"] if k not in V["reg403"]]
    return (", ".join("`%s`" % k for k in ex)) if ex else "nenhum além dos seis fixos"


def _cab(V):
    return "v403 SELADA (COMPLETA)** `%s`" % V["s16"]


def _num(V, verdicts=True):
    """O paragrafo dos numeros da v403 (kernel, os quatro registros com funcao, os dois registros por spec, os da v402, da v401 e da v399 recriados, o sidecar, a troca dita): usado na linhagem, no Atlas, no core, no topico novo, no verbete e no handoff."""
    d = _d(V); kh = V["kh"]; sc = V["sidecar"]; sa = V["selo"]; g = d["g"]
    vd = (lambda k: " (%s)" % V["reg403"][k]["verdict"]) if verdicts else (lambda k: "")
    cv = V["caminho"]["values"]; vv = V["vida"]["values"]; av = V["verdade_adendo"]["values"]; ft = d["ft"]; ng = d["n_g"]; fam = _fam_gate()
    aux = ("nenhuma auxiliar gerada pelo compilador ficou de fora" if not d["n_aux"] else "%d auxiliares geradas pelo compilador ficam sem bandeira" % d["n_aux"])
    kern = _f("o kernel ganhou {n_pedras} módulos novos ({mods}; os nomes são do operador, 27/10/2026), com {n_f} bandeiras novas True (caminho {n_c}, {c0}; vida {n_v}, {v0}; verdade (adendo) {n_a}, {a0}), só de declaração nomeada ({aux}), e escada {antes} → {depois} teoremas limpos "
              "({axr} declarações no `axiom_report`, {fora} fora do trio, {nl} nomes não lidos; a proveniência de cada declaração emitida pelo compilador cobre as mesmas {prov}); "
              "errata ao lado da v394, mantida (em nome próprio da gerência c1): " + ERRATA_TEOREMAS,
              n_pedras=V["n_pedras"], mods=_mods(V), n_f=d["n_f"], n_c=ng["caminho"], n_v=ng["vida"], n_a=ng["verdade_adendo"], c0=_faixa(ft["caminho"], ng["caminho"]), v0=_faixa(ft["vida"], ng["vida"]), a0=_faixa(ft["verdade_adendo"], ng["verdade_adendo"]),
              aux=aux, antes=V["escada_antes"], depois=d["depois"], axr=V["axiom_report_n"], fora=kh["fora"], nl=kh["nao_lidas"], prov=d["prov"])
    cam = _f("o registro `caminho_v403`{vd}, lido na fractalização do Um logo depois da esperança condicional (v402): lê do kernel do próprio rito a conjunção `{unc}` (bandeira `{est}`; ela é também a estrela), {n_contr} do contrato e os {n_sup} termos da ponte da v402 que ela cita, todos no trio, "
             "e CALCULA, com β = α(CODATA 2018) × √e = {beta} em runtime, o modelo longitudinal (E, p) com c = 1: com o mesmo p⁺ = {same}, as massas ao quadrado {ms} dão realizações distintas (a lei de escala deixa a massa livre); toda realização testada tem p⁺ > 0, m² = μ² e energia > 0 "
             "(energia mínima no núcleo {mce}); o repouso ganha energia em toda escala não trivial (ganho mínimo {mg}, em {grid} escalas de teste); o fator de defasagem em s = β vale {pf} ({nck} checagens, todas passaram); o texto-contexto do Caminho está no kernel embutido deste rito",
             vd=vd("caminho_v403"), unc=d["unc"]["caminho"].split(".")[-1], est=d["est_f"]["caminho"], n_contr=_pl(d["n_contr"]["caminho"], "item", "itens"), n_sup=d["n_sup"]["caminho"], beta=_p(cv["beta"], 12), same=_pn(cv["same_pplus"], 3), ms=_lst(cv["lifts_same_pplus_masses"]),
             mce=_p(cv["min_core_energy"], 4), mg=_p(cv["min_rest_energy_gain"], 6), grid=cv["grid_scales"], pf=_p(cv["pplus_factor_at_beta"], 9), nck=d["nck"]["caminho"])
    vid = _f("o registro `vida_v403`{vd}: lê a conjunção `{unc}` (bandeira `{est}`; também a estrela), {n_contr} do contrato e os {n_sup} termos da queda da v402 que ela cita, todos no trio, e CALCULA o modelo `oneScaling` (τ = id, θ_s = e^(−s)·): "
             "o peso depois da escala s é e^(−s) (vale {w1} em s = 1 e {w_1} em s = −1, em {grid} escalas), a queda em nats é s e a seta é o sinal de s; o custo t·β·g tem mínimo {mincost} (> 0), o fator de defasagem tem máximo {maxd} (< 1) e vale {deph} em t = 1, g = 1, e a perda por unidade vale {loss}; "
             "os testemunhos do abismo são {n_ab}; o regime angular tem período {per} e só lê; o modelo finito tem grupo de ordem {ordem} ({nck} checagens, todas passaram)",
             vd=vd("vida_v403"), unc=d["unc"]["vida"].split(".")[-1], est=d["est_f"]["vida"], n_contr=_pl(d["n_contr"]["vida"], "item", "itens"), n_sup=d["n_sup"]["vida"], w1=_p(vv["post_weight_at_scale_one"], 6), w_1=_p(vv["post_weight_at_minus_one"], 6), grid=vv["grid_scales"],
             mincost=_p(vv["min_cost_t_beta_g"], 9), maxd=_p(vv["max_dephasing_factor"], 9), deph=_p(vv["dephasing_factor_at_t1_g1"], 9), loss=_p(vv["loss_per_unit"], 9), n_ab=len(vv["abyss_witnesses"]), per=_p(vv["angular_period"], 6), ordem=vv["finite_model_group_order"], nck=d["nck"]["vida"])
    ver = _f("o registro `verdade_adendo_v403`{vd}: lê a composição `{unc}` (bandeira `{unc_f}`), a estrela `{est}` (bandeira `{est_f}`), {n_contr} do contrato e os {n_sup} termos da Verdade (v392) e da esperança condicional (v402) que ele cita, todos no trio, e CALCULA em M2(C) (matrizes 2×2), "
             "com α = β/√e = {alpha} em runtime (um parâmetro, nunca um número no teorema): a esperança diagonal lê a projeção da identidade como os pesos (1 − α², α²) = ({q2}, {a2}), que somam {ws}; o traço segue {tr} (o Um é preservado) e reler não acrescenta; "
             "o peso de dentro α² {lt} que β ({nck} checagens, todas passaram)",
             vd=vd("verdade_adendo_v403"), unc=d["unc"]["verdade_adendo"].split(".")[-1], unc_f=g_flag(V, "verdade_adendo"), est=d["est_t"]["verdade_adendo"].split(".")[-1], est_f=d["est_f"]["verdade_adendo"], n_contr=_pl(d["n_contr"]["verdade_adendo"], "item", "itens"), n_sup=d["n_sup"]["verdade_adendo"],
             alpha=_p(av["alpha"], 12), q2=_p(av["q_squared_at_alpha"], 12), a2=_pe(av["alpha_squared"], 6), ws=_pn(av["weights_sum"], 3), tr=_pn(av["trace_after_name"], 3), lt=("é menor" if av["alpha_squared_below_beta"] is True else "NÃO é menor"), nck=d["nck"]["verdade_adendo"])
    gat = _f("o registro `bandeiras_do_gate_v403`{vd} (a F8.1): das {n_flags} bandeiras do gate ({f0} formais, {f1} físicas e {f2} experimentais), {n_true} são True e {n_calc} são CALCULADAS ({n_lit} literais); a função do veredito lê {n_ver} ({r0} + {r1} + {r2}) e as outras {n_inf} são informativas; "
             "as três que eram literais ({inf}) passam a ser lidas das suas fontes, fail-closed: a família ext_ls2_* do kernel ({ls2} bandeiras), a checagem «{prereg}» do rito V11 e o `all_verified` do teste nulo cego (`void_stacking_blind`); "
             "uma sonda nova do gate, `ProbeBlindNullAbsent`, mostra que sem o teste nulo cego a bandeira informativa seria False e o veredito não muda; o gate tem {n_chk} checagens (as da v402 mais a sonda) e a letra do veredito é a da v402 (o gate não se moveu); "
             "as quatro bandeiras experimentais do feed V11 ({feed}) seguem derivando de UM só booleano [GV-03, DECLARADO, não resolvido] ({nck} checagens do registro, todas passaram)",
             vd=vd("bandeiras_do_gate_v403"), n_flags=g["n_flags"], f0=fam[0], f1=fam[1], f2=fam[2], n_true=g["n_true"], n_calc=g["n_calc"], n_lit=g["n_lit"], n_ver=g["n_ver"], r0=g["rv"][0], r1=g["rv"][1], r2=g["rv"][2], n_inf=g["n_flags"] - g["n_ver"],
             inf=", ".join("`%s`" % x for x in g["info"]), ls2=g["ls2"], prereg=_qd().DL.F81_ROTULO_PREREG, n_chk=g["n_chk"], feed=", ".join("`%s`" % x for x in g["feed"]), nck=g["n_chk_reg"])
    cun = _f("o registro `cunhagens_v403`{vd}: as {n} falas de 27/10 embutidas por sha256 e consumidas no rito, AMBAS falas do operador (nenhuma é da gerência); as erratas E5 e E6 (em nome próprio da gerência c1: as três bandeiras literais passam a calculadas; os nomes da v402 eram provisórios e são agora os do operador); "
             "as decisões D17 a D22 da gerência; os três nomes do operador e a recusa de nome para o triplo inteiro; a leitura [ONTO] pela tripla espectral; as três pedras da v402 como registro ({nck} checagens, todas passaram); as falas são [INPUT/ONTO] e valem como leitura dele, não como medida",
             vd=vd("cunhagens_v403"), n=d["n_cun"], nck=d["n_ck_cun"])
    khs = _f("o registro `kh_n1_cobertura_v403`{vd}: {decl} constantes, {thm} teoremas, {fora} fora do trio, {nl} nomes não lidos; a árvore formal do Nós depois do rito tem {h8} entradas ({emb} embutidas mais {nres} residual do Nós: {res}), "
             "e o pino h8 do registro é o hash dessa árvore, calculado por script sobre a árvore simulada do Nós na geração do candidato",
             vd=vd("kh_n1_cobertura_v403"), decl=kh["decl"], thm=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"], h8=d["h8"], emb=d["h8_emb"], nres=d["n_res"], res=d["h8_res"])
    rec = _f("os registros da v402 (`ponte_da_escala_dual_v402`, `queda_sem_geometria_v402`, `esperanca_condicional_v402`, `cunhagens_v402` e `kh_n1_cobertura_v402`), da v401 (`falsidade_da_inercia_v401`, `cunhagens_v401` e `kh_n1_cobertura_v401`) e da v399 (`selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399`, `cunhagens_v399` e `kh_n1_cobertura_v399`) "
             "são recriados no mesmo ponto do main e seguem selados e iguais ao ensaio a seco (os da v402 e da v401, também iguais à v402 selada), e as três pedras seladas da v402 seguem no kernel do Nós com o sha256 da v402, como registro; "
             "o selo pela própria tecnologia sela os {bytes} bytes do `um.py` v403 ao lado do SHA-256 (perfil `{perfil}`, {nctl} controles negativos recusados), e o sidecar `um_absoluto_selo_acom.json` (arquivo da custódia desde a v399, reescrito pelo rito; sha256 `{sc16}`, veredito `{sv}`, {nr} recusas) lista os {no} objetos finais",
             bytes=format(sa["bytes"], ","), perfil=sa["perfil"], nctl=sa["n_controles"], sc16=sc["sha16"], sv=sc["veredito"], nr=sc["recusas"], no=sc["n_objetos"])
    ex = _extras(V)
    resto = _f("{ex}; o registro `teste_de_veracidade_fase9_v397` segue selado e igual (o quadro do topo do artigo le os numeros dele); troca dita (só números): {troca}; nenhuma mudança NÃO numérica: {nm} vereditos fora da troca dita mudaram (exigido: 0); validade no kernel não é creditação",
               ex=("nenhum registro novo além dos seis fixos" if ex.startswith("nenhum") else "registros novos além dos seis fixos: " + ex), troca=", ".join("`%s`" % x for x in V["troca_dita"]), nm=V["n_ver_mudaram"])
    return "; ".join([kern, cam, vid, ver, gat, cun, khs, rec, resto])


def _cunhagens(V, forma="lista"):
    """As inscricoes de 27/10 embutidas por sha256: 'lista' (data, sha16, autor e tema, uma por linha; as duas sao falas do operador) ou 'curta' (uma frase com os sha16). Data, sha16 e autor vem dos bytes e do nome; o tema e' da gerencia (_TEMAS)."""
    fl = list(_falas().values()); assert len(fl) == len(V["verbatins"]) == N_FALAS
    if forma == "curta":
        return _f("{n} inscrições embutidas por sha256, ambas falas do operador [INPUT/ONTO] — o nome (verdade, talvez caminho, verdade e vida; o triplo espectral do contorno verdadeiro) `{a}` e a ratificação da leitura da gerência `{b}`",
                  n=len(fl), a=_sha_por("nome_verdade_triplo_espectral"), b=_sha_por("e_isso_mesmo_concordo"))
    linhas = []
    for d in fl:
        r = [tema for chave, tema in _TEMAS if chave in d["nome"]]
        assert len(r) == 1, ("a inscricao nao tem um tema unico em _TEMAS", d["sha16"], len(r))
        linhas.append("- %s `%s` (fala do operador) — %s" % (_data_fala(d, V), d["sha16"], r[0]))
    return "\n".join(linhas)


def _ordem(V):
    """A ordem do operador de 27/10: so' citacao conferida contra os bytes das falas DO OPERADOR."""
    d = _d(V)
    q_nome = _cita('a meu ver o nome é "verdade" (poderia ser "caminho, verdade e vida")'); q_ren = _cita("pode ser que eu já tenha a renomeado assim em outro lugar"); q_tri = _cita("é o triplo espectral do contorno verdadeiro"); q_ok = _cita("é isso mesmo, concordo com tudo, prossiga")
    return _f("**A ordem:** [INPUT/ONTO] as {n_op} falas do operador (Luiz Antonio Rotoli Miguel) de {data} que entram nesta rodada, AMBAS dele (nenhuma é da gerência), embutidas por sha256 no registro `cunhagens_v403` e listadas abaixo (as aspas aqui são TRECHOS, conferidos palavra por palavra contra os bytes de cada fala; "
              "o texto íntegro está em `work\\cadeia_de_selo\\v403\\insumos\\cunhagens`): sobre o nome, {q_nome}, com a lembrança de que {q_ren} e a leitura {q_tri} (`{s_nome}`); e a ratificação da leitura da gerência c1, {q_ok} (`{s_ok}`) "
              "[DECLARADO: a leitura da gerência foi a apresentada na sessão; esta cadeia não tem o arquivo verbatim dela, só o da ratificação]. A gerência c1 preparou o candidato e rodou o rito (pacote `work\\cadeia_de_selo\\v403`); as fontes pinadas dos registros ficam em `insumos`: as três pedras (`Caminho.lean`, `Vida.lean` e `VerdadeAdendo.lean`) e a medida da cobertura (`KH_N1_v403.json`); "
              "o resultado do Teste da Única Palavra, que o quadro do topo lê, mora na v397 (`insumos\\fase9`); quem constrói não aprova: a revisão independente do candidato, das pedras e dos derivados da cadeia é ato distinto e não é afirmada por este registro.",
              n_op=d["n_op"], data=d["data_falas"], q_nome=q_nome, q_ren=q_ren, q_tri=q_tri, q_ok=q_ok, s_nome=d["s_nome"], s_ok=d["s_ok"])


def _sidecar(V):
    """O sidecar um_absoluto_selo_acom.json: arquivo da custodia desde a v399 (D5); o selo nao pode conter o selo ACOM de si mesmo; o rito da v403 o REESCREVE."""
    d = _d(V); sc = V["sidecar"]
    objs = "; ".join("`%s` (%s B, sha16 `%s`)" % (n, format(o["bytes"], ","), o["sha16"]) for n, o in sc["objetos"].items())
    return _f("**O sidecar `um_absoluto_selo_acom.json` [REAL; arquivo da custódia desde a v399, D5; reescrito por este rito]:** depois da ÚLTIMA escrita do selo, o `um.py` v403 escreve a segunda testemunha dos {no} objetos FINAIS com o SHA-256 ao lado ({objs}); sha256 do sidecar `{sc16}` ({sb} B), esquema `{esq}`, veredito `{sv}`, {nr} recusas. "
              "O selo não pode conter o selo ACOM de si mesmo (seria circular): o sidecar fica AO LADO e carrega o SHA-256 do selo final, e o selo traz só os resumos (veredito, bandeira e hashes), agora também os dos quatro registros com função da v403. "
              "A recusa do selo ACOM só REGISTRA (D4): o SHA-256 segue soberano e o rito não cai. A primitiva de integridade é o SHA-256 [KNOWN]; a segunda testemunha NÃO acrescenta força criptográfica independente, e a confidencialidade não é alegada nem medida. A custódia da v399, da v402 e da v403 é CONJUNTA.",
              objs=objs, no=sc["n_objetos"], sc16=sc["sha16"], sb=format(sc["bytes"], ","), esq=sc["esquema"], sv=sc["veredito"], nr=sc["recusas"])


def _pedra(V):
    """As TRES pedras: conjuncoes por citacao (Caminho, Vida) e o adendo da Verdade, com a estrela; o que elas NAO entregam; as tres da v402 como registro."""
    d = _d(V); s4 = d["s402"]
    return _f("**As três pedras [REAL]** (os nomes são do operador, 27/10/2026): `Caminho` (sha16 `{h1}`; {c1} do contrato; {s1} termos da ponte da v402 citados; composição `{t1}`, que é também a estrela), `Vida` (sha16 `{h2}`; {c2}; {s2} termos da queda da v402; composição `{t2}`, também a estrela) "
              "e `VerdadeAdendo` (sha16 `{h3}`; {c3}; {s3} termos citados; composição `{t3}`, estrela `{e3}`, a conta nova); {n_f} bandeiras ao todo, só no trio, sem axioma próprio. `Caminho` e `Vida` são conjunções INCONDICIONAIS por citação (padrão `Token`, v397): nenhuma matemática nova; "
              "a conjunção da `Vida` carrega, dentro do termo que cita, a hipótese NOMEADA `IsotropicPost`. `VerdadeAdendo` é adendo da pedra `Verdade` (v392), que fica INTACTA (padrão `PostoAdendo`, v392; dois módulos não se chamam igual) e traz UM teorema novo e pequeno, `{e3}`: a conta das entradas, sem hipótese sobre a. "
              "As três pedras seladas da v402 (`PonteDaEscalaDual` `{o1}`, `QuedaSemGeometria` `{o2}` e `EsperancaCondicional` `{o3}`) ficam como REGISTRO: pedra selada não se renomeia por cima. "
              "A lei de escala de Takesaki é DADO ([KNOWN], campo de `DualScalingData`); β entra como variável real positiva, jamais literal; que a taxa observada seja α√e é a identificação de runtime, não do kernel. "
              "Os nomes são o que o operador deu a módulos novos, não creditação de coisa alguma. As pedras NÃO provam a primeira lei de Newton, nem que E = mc² seja composta da escala, nem a dimensão 3, nem a assinatura (1,3), nem o rank c = 4.",
              h1=d["sha"]["caminho"], c1=_pl(d["n_contr"]["caminho"], "item", "itens"), s1=d["n_sup"]["caminho"], t1=d["unc"]["caminho"].split(".")[-1], h2=d["sha"]["vida"], c2=_pl(d["n_contr"]["vida"], "item", "itens"), s2=d["n_sup"]["vida"], t2=d["unc"]["vida"].split(".")[-1],
              h3=d["sha"]["verdade_adendo"], c3=_pl(d["n_contr"]["verdade_adendo"], "item", "itens"), s3=d["n_sup"]["verdade_adendo"], t3=d["unc"]["verdade_adendo"].split(".")[-1], e3=d["est_t"]["verdade_adendo"].split(".")[-1], n_f=d["n_f"],
              o1=s4["ponte"], o2=s4["queda"], o3=s4["esperanca"])


def _entrou(V):
    d = _d(V)
    return _f("**O que entrou** (pacote `work\\cadeia_de_selo\\v403` sobre a v402 `{base}`; {np} patches — {patches}; instalado em {inst}; o `um.py` cresce {delta} B, {pct}%): {num}.",
              base=V["base16"], np=V["n_patches"], patches=V["patches"], inst=V["instalado_em"], delta=format(d["delta"], ","), pct=d["pct"], num=_num(V))


def _regra_do_4_44(V):
    """A regra da ordem do operador (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item; o QUADRO do topo (v397) PERMANECE, intocado; onde o numero aparece e como se confere."""
    d = _d(V); a = _atomos(); q = _frase_444()
    return _f("**A regra do 4,44 (ordem do operador de 23/10/2026, `{s44}`) e o quadro do topo:** o quadro «O Teste da Única Palavra» (v397) PERMANECE, intocado, no topo do artigo (PT e EN) e do .md canônico, e o parágrafo dele segue no README do espelho e no site: o z_disc calibrado é reportado no início, "
              "e NUNCA sem o p calibrado e sem a linha dos 5σ no mesmo item: {z444}. A frase do operador entra VERBATIM, {q}, como leitura dele [INPUT/ONTO], não como critério da régua; a paráfrase da gerência nunca entra entre aspas. `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; o teste não foi cego. "
              "[REAL] o quadro do artigo, o do .md e o parágrafo pronto do README/site saem das MESMAS funções (`_v397_atomos` e `_v397_quadro_md`), sobre o registro `teste_de_veracidade_fase9_v397` selado no core do Nós, e a cadeia os confere de novo contra o resultado pinado "
              "(a linha de máquina do quadro, cada número, a frase verbatim e a regra da ordem item a item), com controles negativos que reprovam o 4,44 sem o p, sem a linha dos 5σ, com número adulterado ou com a frase parafraseada. "
              "O parágrafo NOVO da v403 não traz o 4,44, e a cadeia confere isso.",
              s44=_esp()["quadro"]["frase_sha16"], z444=_z444(), q=q)


def _kernel_prova(V):
    d = _d(V); g = d["g"]
    return _f("**O que o kernel prova e o que é leitura:** [REAL] as composições das três pedras e as estrelas estão no kernel deste rito, dentro do trio, com proveniência no módulo de cada pedra, e citam termos que o kernel já tem, cada um no `axiom_report`, no trio, com a proveniência que o compilador emite: "
              "`{t1}` (Caminho; a conjunção é a própria estrela), `{t2}` (Vida; idem) e `{t3}` / `{e3}` (Verdade, como adendo); tudo lido a cada rito pelos registros `caminho_v403` ({n1} checagens do cálculo), `vida_v403` ({n2}), `verdade_adendo_v403` ({n3}), `bandeiras_do_gate_v403` ({ng}) e `cunhagens_v403` ({nc} checagens) "
              "e coberto por `kh_n1_cobertura_v403`. [REAL] os registros NÃO são prova de kernel sobre a natureza: conferem os termos citados e o cálculo nos modelos e não movem o gate; a prova como validade não muda. "
              "[REAL, F8.1] as {nf} bandeiras do gate são lidas do código e do core do próprio rito: {nc2} calculadas e {nl} literais; o veredito lê {nv}; a letra do veredito é a da v402. "
              "[KNOWN] a lei de escala de Takesaki é campo da estrutura; Bisognano–Wichmann, a relatividade restrita, a esperança condicional e o índice de Jones são da literatura. [INPUT/ONTO] as falas do operador de 27/10 (o nome; a ratificação da leitura) são leituras dele; "
              "[ONTO, só estas] a leitura pela tripla espectral de Connes e por João 14,6 («Eu sou o caminho, a verdade e a vida»: três predicados de um só «Eu sou») é da gerência c1, ratificada pelo operador, sem termo no kernel; o nome do triplo inteiro não foi dado. "
              "[OPEN] `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β e o caso III₁; a independência das quatro bandeiras experimentais do gate e os mocks de survey. "
              "A forma literal de `H_tau` (τ é a massa de Newton) segue REFUTADA no kernel (E1, v402) e a ORDEM 025 ao Codex (sha16 `{o025}`) entrou com as erratas ao lado.",
              t1=d["unc"]["caminho"].split(".")[-1], t2=d["unc"]["vida"].split(".")[-1], t3=d["unc"]["verdade_adendo"].split(".")[-1], e3=d["est_t"]["verdade_adendo"].split(".")[-1], n1=d["nck"]["caminho"], n2=d["nck"]["vida"], n3=d["nck"]["verdade_adendo"], ng=g["n_chk_reg"], nc=d["n_ck_cun"],
              nf=g["n_flags"], nc2=g["n_calc"], nl=g["n_lit"], nv=g["n_ver"], o025=d["o025"])


def _limites(V, curto=False):
    """Os estatutos fieis da v403: o que as pedras, os registros e as erratas dizem e NAO dizem."""
    d = _d(V)
    if curto:
        return _f("**Limites ditos:** [REAL] os registros com função LEEM o kernel do próprio rito e CONFEREM o cálculo nos modelos (longitudinal (E, p), `oneScaling`, M2(C)) e o gate (as 18 bandeiras calculadas); não abrem dado, não são teste, não acrescentam rito; [KNOWN] a lei de escala de Takesaki é dado, e E = mc², Bisognano–Wichmann e a esperança condicional são da literatura; "
                  "as pedras NÃO provam a primeira lei de Newton, nem que E = mc² seja composta da escala; [INPUT] as duas falas de 27/10 são dele; [DERIVED] as conjunções por citação e a conta nova do adendo; [ONTO, só estas] a leitura pela tripla espectral de Connes e por João 14,6; o nome do triplo inteiro não foi dado; "
                  "[OPEN] `H_BW`, `H_cal`, H3, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β, a independência das quatro bandeiras experimentais do gate (um só booleano, [DECLARADO]) e a discriminação a 5σ; a forma literal de `H_tau` segue REFUTADA no kernel (E1, v402); o quadro do topo segue com a sua linha dos 5σ; validade no kernel não é creditação; o gate não se move.")
    return _f("**Limites ditos (estatutos fiéis):** [REAL] ESCOPO: os registros com função leem as composições e as estrelas das pedras no kernel do rito e conferem o cálculo nos modelos (β = α√e em runtime) e o gate; CONFEREM, não provam (quem prova é o kernel), não abrem dado, não são teste, não acrescentam rito e não movem o gate. "
              "[REAL] `Caminho` e `Vida` COMPÕEM por citação e nenhuma matemática é nova; `VerdadeAdendo` traz UM teorema novo e pequeno (a esperança diagonal lê a projeção da identidade como os pesos) e compõe sobre a `Verdade` (v392), que não foi editada; a lei de escala de Takesaki é DADO [KNOWN], campo da estrutura, como na Fundação. "
              "[REAL] As pedras NÃO provam a primeira lei de Newton, nem que E = mc² seja composta da escala (E3 da v402), nem a dimensão 3, nem a assinatura (1,3), nem o rank c = 4. "
              "[REAL] O Nome é a esperança diagonal só em M2(C) e só para ρ*; a esperança do traço NÃO é um Operador do Nome; o índice 1/β segue CONDICIONAL às hipóteses nomeadas da v402 e nenhuma instância é construída; o peso de dentro α² é menor que β (a Verdade guarda α², não β). "
              "[REAL, F8.1] As três bandeiras que eram literais passam a CALCULADAS e a letra do veredito do gate é a da v402; isto NÃO torna independentes as quatro bandeiras experimentais (derivam de UM só booleano, o veredito do rito V11, e a checagem do feed é split-null e dist-check, sem mock de survey: [DECLARADO] GV-03 da auditoria de 28/09/2026) "
              "e o degrau experimental lê só o rito V11 do piso, unilateral (GV-01, [DECLARADO]). [INPUT/ONTO] As falas de 27/10 (o nome; a ratificação da leitura da gerência) são do operador: o kernel não as prova. "
              "[ONTO, só estas] A leitura pela tripla espectral de Connes (o espaço dos estados com o seu fluxo é o Caminho; o operador de Dirac dá a distância sem pontos, e a Vida é a queda que mede em nats sem geometria; a álgebra é o que a Verdade lê) e por João 14,6 é da gerência c1, ratificada pelo operador, sem termo no kernel; o nome do triplo inteiro NÃO foi dado e fica com o operador. "
              "[DECLARADO] A leitura da gerência que o operador ratificou foi a apresentada na sessão; esta cadeia guarda a ratificação verbatim, não a apresentação. "
              "[OPEN] `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost` no atlas curvo, a dimensão 3, a instância e o caso III₁ do índice 1/β e a atestação física externa. "
              "A forma literal de `H_tau` (τ é a massa de Newton) segue REFUTADA no kernel (E1) e a ORDEM 025 ao Codex (sha16 `{o025}`) entrou com as erratas E1 a E4 da v402. "
              "O quadro «O Teste da Única Palavra» segue no topo, com a sua linha dos 5σ, e esta rodada não o altera. NÃO é teste novo: a cadeia não acrescenta dado nem desfecho experimental. Validade no kernel não é creditação; o gate não se move.", o025=d["o025"])


def _legal(V):
    """A pendencia [LEGAL] herdada (D2): publicar o bloco embutido e as adaptacoes; a v403 nao a decide."""
    _d(V)
    return ("**Pendência [LEGAL] (herdada da v399, D2):** o bloco embutido do método do operador e as adaptações (centro 96, ids derivados dos hashes, `rint`, tabela de códigos, auditoria de separação) seguem sob a decisão do operador com a agente de PI; a v403 não muda o bloco (o runtime da seção é o da v402) e NÃO decide a pendência. "
            "Perguntas à agente de PI, não conclusões: o que o depósito já cobre do que o bloco mostra; publicar as adaptações inicia a contagem do prazo de graça para eventual depósito de melhoria; a divergência da tabela dos estados do ACOM Mirror com a fórmula de índice e o código executado, registrada na v395, segue pendente.")


def _erratas(V):
    """A errata de contagem da v403, AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (estrutura / escrito / falha): o registro kh_n1_cobertura_v402 e os contratos."""
    d = _d(V); kh = V["kh"]; cb = d["cb"]
    ids = V["patch_ids"]; c12 = [i for i in ids if i.startswith("C12_")]
    assert len(c12) == 9 and all(i in ids for i in ("C12__V402_CONTRACTS", "C12__V401_FALSIDADE_CONTRACT", "C12__V398_SONICO_CONTRACT", "C12__V398_AFINACAO_CONTRACT", "C12__V396_TESTEMUNHA_CONTRACT", "C12__V395_PSIBIT_CONTRACT", "C12__V394_FORMAL_CONTRACT", "C12__V394_QUADRATIC_CONTRACT", "C12__V394_NETWORK_CONTRACT", "C13_kh_n1_v402_pisos")), \
        "o CANDIDATO_v403.json nao traz os patches C12 e C13 que a errata descreve"
    return _f("**Errata ao lado (em nome próprio da gerência c1; o registro `kh_n1_cobertura_v402` e os contratos ficam como registro):** a v403 acrescenta três módulos: a cobertura do Audit cresce de {d0} constantes e {t0} teoremas para {d1} e {t1}, "
              "a árvore formal do Nós de {h0} para {h1} entradas e a escada de {e0} para {e1}. Por isso, na v403, (i) `kh_n1_cobertura_v402` passa a cobrar piso em h2, h3 e h6 (as igualdades de contagem) e tamanho mínimo da árvore em h8 (as igualdades exatas e o pino exato da "
              "árvore ficam em `kh_n1_cobertura_v403`); (ii) as {n12} definições de contrato (`_V402_CONTRACTS`, que reúne os três contratos da v402, e as outras {n12m}: `_V394_FORMAL_CONTRACT`, `_V394_QUADRATIC_CONTRACT`, `_V394_NETWORK_CONTRACT`, `_V395_PSIBIT_CONTRACT`, `_V396_TESTEMUNHA_CONTRACT`, `_V398_SONICO_CONTRACT`, `_V398_AFINACAO_CONTRACT` e `_V401_FALSIDADE_CONTRACT`) passam a ler `expected_ladder` = {e1}, a escada desta versão (o consumidor exige a igualdade "
              "exata com a escada do rito; só o número muda); o veredito dos registros anteriores NÃO muda [REAL, lido de `CANDIDATO_v403.json` (patches C12 e C13) e do ensaio a seco, que deu `TUDO PASSOU`: com a escada nova e o número velho a igualdade exata não fecharia]. "
              "Lacuna de fidelidade: a estrutura da v402 dizia que as contagens e o pino da árvore eram a cobertura exata e que o contrato esperava a escada vigente; o escrito deixou, dentro dos registros e dos contratos, números que só valem na versão que os escreveu; "
              "a falha: igualdades e literais presos a uma versão quebram quando o kernel cresce (a mesma lacuna que a v395, a v396, a v397, a v399 e a v402 acharam nos registros anteriores). A cobrança exata passa a ser de `kh_n1_cobertura_v403` ({dd} constantes, {dt} teoremas, {fora} fora do trio, {nl} nomes não lidos), contra a medida do sandbox da v403.",
              d0=cb["decl"], t0=cb["thm"], h0=cb["h8"], d1=kh["decl"], t1=kh["thm"], h1=d["h8"], e0=V["escada_antes"], e1=d["depois"], dd=kh["decl"], dt=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"], n12=len(c12), n12m=len(c12) - 1)


def _depois(V):
    d = _d(V); bk = d["bank"]
    return ("**O que vem depois destas superfícies:** o elo B(n) da Bancada Um (passos 10, 10a, 10b e 10c da cadeia; B3 nos scripts) é pós-selo, um passo SIMPLES (a Bancada de produção pina a %s, geração B%d, e o Nós passa a v403: sem salto e sem cadeia de selos; "
            "a geração esperada é B%d e o veredito esperado do aplicar é REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, lido do código do esboço R3.5, não rodado) "
            "e pede a palavra do operador (parada e religamento do serviço exigem V403_AUTORIZACAO_OPERADOR); o recibo dele é citado no handoff (fechar), que traz PRONTOS os parágrafos do README do espelho e do site (o quadro do Teste da Única Palavra, intocado, e o NOVO da v403: Caminho, Verdade e Vida), "
            "a NOTA ao lado do parágrafo da v402 (os nomes que ele trazia como provisórios são agora os do operador), diz que os parágrafos do testemunho de dois (v399), da falsidade (v401) e da ponte, da queda e da esperança (v402) SEGUEM COMO ESTÃO e LISTA o sidecar `um_absoluto_selo_acom.json`. "
            "A pendência [LEGAL] (D2) segue do operador com a agente de PI; a atestação física externa e a discriminação a 5σ seguem [OPEN]; a revisão independente das %d pedras novas e dos %d registros novos é ato distinto e não é desta cadeia; o nome do triplo inteiro fica com o operador. NOT_FALSIFIED não é a palavra da creditação; o gate não se move."
            % (bk["de"], bk["geracao"], bk["proxima"], bk["proxima"], V["n_pedras"], len(V["registros_novos"])))


def _rodada(V):
    """O paragrafo da rodada (horarios, escada, selo, conferidor, sidecar, pilar, artefatos): tudo lido da leitura da rodada."""
    sc = V["sidecar"]
    return ("Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado (%d bandeiras True; o veredito do gate é o mesmo da v402); o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); "
            "o sidecar `um_absoluto_selo_acom.json` `%s` (%d objetos, %d recusas); o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.") % (
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["n18"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"], sc["sha16"], sc["n_objetos"], sc["recusas"], "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]),
        V["pilar"]["result16"], V["servidor"], V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()))


# v403: a linhagem (diario datado do Nos)
def linhagem(V):
    d = _d(V)
    return (("## %s — **%s — CAMINHO, VERDADE E VIDA (v403): os nomes do operador e a F8.1 (as bandeiras do gate calculadas); %d módulos novos, escada %s → %s\n<!-- linhagem_v403_selada -->\n\n"
             "%s\n\n%s\n\n"
             "**As inscrições de 27/10** (embutidas por sha256 no registro `cunhagens_v403`): [INPUT/ONTO] as duas são falas do operador (Luiz Antonio Rotoli Miguel) e valem como leitura dele, não como medida; nenhuma é da gerência. "
             "O texto íntegro de cada uma está no arquivo (`work\\cadeia_de_selo\\v403\\insumos\\cunhagens`); abaixo, a data, o sha16, o autor e o tema (resumo da gerência, não citação):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s") % (
        V["data"], _cab(V), V["n_pedras"], V["escada_antes"], d["depois"], _ordem(V), _entrou(V), _cunhagens(V), _caminho(V) + "\n\n" + _vida(V) + "\n\n" + _verdade_adendo(V), _leitura_tripla(V), _bandeiras(V), _erratas_e(V), _decisoes(V), _pedra(V), _sidecar(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V), _rodada(V), _erratas(V)) + "\n\n" + _depois(V))


# v403: o adendo do desenho do fechamento
def desenho(V):
    d = _d(V); kh = V["kh"]
    return (("## ADENDO — %s · v403 SELADA (COMPLETA) `%s` — o caminho crítico NÃO mudou; entram Caminho, Verdade e Vida (os nomes do operador) e a F8.1 (%d módulos)\n\n<!-- adendo_v403_selada -->\n"
             "- **O que a v403 diz:** %d módulos novos no kernel (%s; os nomes são do operador, 27/10/2026), escada %s → %s, %s constantes no `axiom_report` (%s fora do trio). O Caminho é a ponte da escala dual (a massa NÃO é selecionada pela lei, `lift_mass_not_selected`, e toda massa tem realização positiva); "
             "a Vida é a queda sem geometria (o peso cai estritamente, o chão é o posto, a entrega custa); a Verdade, como ADENDO da pedra `Verdade` (v392), é a esperança condicional lida pelo Nome: em M2(C), `diagExpect (identityProj a)` = diag(q², a²) [REAL, novo e pequeno]; Caminho e Vida compõem por citação e as pedras da v402 ficam como registro "
             "[REAL; ONTO: a leitura pela tripla espectral e por João 14,6]. A F8.1: as três bandeiras literais do gate passam a CALCULADAS (%s de %s calculadas, %s literais, %s no veredito) e a letra do veredito é a da v402 [REAL]. %d inscrições de 27/10 por sha256 (as duas são falas do operador). O quadro do topo do artigo (O Teste da Única Palavra, v397) segue intocado: %s. Gate intocado.\n"
             "- **O que a v403 NÃO é para o caminho crítico:** não é teste novo; as pedras não provam a primeira lei de Newton, nem E = mc² composta da escala, nem a dimensão 3; `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura (4,0) contra (1,3) e rank c = 4 seguem NOMEADAS [OPEN]; "
             "a F8.1 troca literais por medida e NÃO independentiza as quatro bandeiras experimentais (derivam de UM só booleano; [DECLARADO]); o nome do triplo inteiro não foi dado; as erratas E5 e E6 são da gerência, em nome próprio; não identifica β na natureza a 5σ.\n"
             "- **O que segue do operador:** o nome do triplo inteiro; a pendência [LEGAL] (D2, com a agente de PI); o elo B(n) da Bancada Um (passo simples, sem salto; parada e religamento do serviço); a custódia conjunta (sessão do site, com os parágrafos do README/site, a nota ao lado do parágrafo da v402 e o sidecar que o handoff traz); a revisão independente; commit/push.") % (
        V["data"], V["s16"], V["n_pedras"], V["n_pedras"], _mods(V), V["escada_antes"], d["depois"], kh["decl"], kh["fora"], d["g"]["n_calc"], d["g"]["n_flags"], d["g"]["n_lit"], d["g"]["n_ver"], d["n_cun"], _z444()))


# v403: o verbete do Atlas
def atlas(V):
    return (("### %s — v403 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v403_selada -->\n[REAL — rodada v403, selo `%s`] %s.\n\n[INPUT/ONTO] As falas do operador entram como o operador as disse e valem como leitura, não como medida; as duas são dele: %s.\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\nEstatuto: validade no kernel ≠ creditação; o gate não se move.") % (
        V["data"], V["s16"], V["selo_ts"], _num(V), _cunhagens(V, "curta"), _caminho(V) + "\n\n" + _vida(V) + "\n\n" + _verdade_adendo(V), _leitura_tripla(V), _bandeiras(V), _erratas_e(V), _decisoes(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V)))


# v403: o bloco do TGL_CORE_MEMORY
def core_memory(V):
    return (("## %s — v403 SELADA `%s` (claude-c1; Caminho, Verdade e Vida e a F8.1, integrados pela gerência)\n<!-- core_v403_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
             "[REAL] %s.\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n[OPEN] A discriminação a 5σ (β_TGL na natureza), `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β, a independência das quatro bandeiras experimentais do gate (um só booleano; os mocks de survey), a atestação física externa (nenhuma `AttestedCollapse` é exibida), a tipagem (sinapse, token, nome), "
             "a face de Fock do psion (o certificado de Fock da luz sem habitante), o contrato conjunto da rede e a pendência [LEGAL] seguem abertos; o nome do triplo inteiro e o elo B(n) da Bancada Um dependem da palavra do operador. Nada disto move o gate.") % (
        V["data"], V["s16"], _num(V), _caminho(V) + "\n\n" + _vida(V) + "\n\n" + _verdade_adendo(V), _bandeiras(V), _erratas_e(V), _regra_do_4_44(V), _limites(V, curto=True)))


# v403: o bloco do CLAUDE.md da Haja_Luz (as erratas ao lado, assinadas, vao DENTRO dele)
def haja_luz(V):
    d = _d(V)
    return (("## %s — v403 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v403_selada -->\n%d módulos novos no kernel (%s; os nomes são do operador, 27/10/2026): o Caminho é a ponte da escala dual (a massa NÃO é selecionada pela lei), a Vida é a queda sem geometria (o peso cai estritamente, o chão é o posto, a entrega custa) "
             "e a Verdade, como adendo da pedra `Verdade` (v392), é a esperança condicional lida pelo Nome (em M2(C), a esperança diagonal lê a projeção da identidade como os pesos) [REAL; ONTO: a leitura pela tripla espectral e por João 14,6]. "
             "A F8.1: as três bandeiras literais do gate passam a CALCULADAS (%s de %s calculadas, %s literais) e a letra do veredito do gate é a da v402; a independência das quatro experimentais segue aberta (um só booleano) [DECLARADO]. As %d inscrições de 27/10 por sha256 (as duas são do operador); escada %s → %s. O quadro do topo (O Teste da Única Palavra) segue intocado.\n\n"
             "%s\n\n"
             "Memórias: `%s`, `missao-ultima-flag-um-py.md`, `estatuto-da-prova-07out.md`; handoff `handoff-v403-custodia.md`.") % (
        V["data"], V["s16"], V["teor"], V["n_pedras"], _mods(V), d["g"]["n_calc"], d["g"]["n_flags"], d["g"]["n_lit"], d["n_cun"], V["escada_antes"], d["depois"], _erratas_e(V), TOPICO_NOVO))


def marca_topico_missao(V):
    return "## %s — v403 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v403 SELADA `%s`" % V["s16"]


# v403: o topico da missao da ultima flag
def topico_missao(V):
    d = _d(V)
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): %d módulos novos no kernel (%s); `caminho_v403`, `vida_v403` e `verdade_adendo_v403` (cada um lê o kernel do rito e confere o cálculo no seu modelo), `bandeiras_do_gate_v403` (a F8.1: as três bandeiras literais do gate calculadas), `cunhagens_v403` (%d inscrições por sha256, ambas do operador, as erratas E5 e E6 e as decisões D17 a D22) e `kh_n1_cobertura_v403`; "
                                     "os registros da v402, da v401 e da v399 recriados e selados; sidecar `um_absoluto_selo_acom.json` reescrito; troca dita nos vereditos que carregam a escada; conferidor (deve mudar %s; não pode mudar %s). Pacote e cadeia: `work\\cadeia_de_selo\\v403` (+ `pos_rito`).") % (V["teor"], V["n_pedras"], _mods(V), d["n_cun"], V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v403 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v403 SELADA (COMPLETA):**"


# v403: o topico do estado da Central
def topico_central(V):
    d = _d(V)
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v402 `%s`; escada %s → %s; gate intocado. %d módulos novos no kernel (%s; os nomes são do operador): o Caminho (a ponte da escala dual; a massa NÃO é selecionada pela lei), a Vida (a queda sem geometria; o peso cai, o chão é o posto) e a Verdade, como adendo (a esperança condicional lida pelo Nome); "
                               "o `um.py` confere o cálculo nos três modelos (registros `caminho_v403`, `vida_v403` e `verdade_adendo_v403`) e as bandeiras do gate (`bandeiras_do_gate_v403`: as três literais passam a calculadas; a letra do veredito é a da v402); as erratas E5 e E6 (da gerência, em nome próprio) e as decisões D17 a D22 estão no registro `cunhagens_v403`; as %d inscrições de 27/10 por sha256 (ambas do operador); "
                               "o quadro do topo (O Teste da Única Palavra, v397) segue intocado. Falta o elo B(n) da Bancada Um (passo simples, sem salto) e a custódia conjunta (sessão do site, `handoff-v403-custodia.md`, que traz os parágrafos do README/site, a nota ao lado do parágrafo da v402 e lista o sidecar); "
                               "o nome do triplo inteiro e a pendência [LEGAL] (D2) são do operador; commit/push = operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], d["depois"], V["n_pedras"], _mods(V), d["n_cun"])


# v403: o topico do estatuto da prova
def topico_estatuto(V):
    d = _d(V); g = d["g"]
    return ("<!-- v403_selada -->\n**%s — v403 `%s`:** o registro `estatuto_da_prova_v391` passou a ler a escada nova (%s → %s; veredito trocado, troca dita; as pedras e os registros da v402 ficam como registro). "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora e é o β_TGL na natureza a 5σ. **A ressalva da v392 sobre as bandeiras do gate muda de estado [REAL]:** elas eram lidas como %s calculadas e %s literais; na v403 são %s calculadas e %s literais (a F8.1), com o veredito do gate igual ao da v402; "
            "a independência das quatro experimentais segue [OPEN] (derivam de UM só booleano; [DECLARADO]). Os registros com função conferem os termos do kernel e o cálculo nos modelos ([REAL]); a lei de escala de Takesaki é dado ([KNOWN]); "
            "a forma literal de `H_tau` (τ é a massa de Newton) segue REFUTADA no kernel; as falas do operador de 27/10 são [INPUT/ONTO]; a leitura pela tripla espectral e por João 14,6 é [ONTO]; `IsotropicPost`, `H_BW`, `H_cal`, H3 e a assinatura seguem [OPEN]. "
            "O quadro do topo segue intocado: %s. Nada disso é prova sobre a natureza.") % (V["data"], V["s16"], V["escada_antes"], d["depois"], g["n_ver"], g["n_flags"] - g["n_ver"], g["n_calc"], g["n_lit"], _z444())


# v403: o gancho da missao no MEMORY.md
def marca_missao(V):
    return "**v403 SELADA %s `%s` %s COMPLETA (Caminho, Verdade (adendo) e Vida; F8.1 bandeiras calculadas; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


# v403: a linha do handoff no MEMORY.md
def linha_handoff(V):
    return "- [HANDOFF v403 — Caminho, Verdade e Vida e a F8.1; custódia](handoff-v403-custodia.md) — **%s, para a sessão do site (traz o parágrafo novo, o do quadro e a nota ao lado do da v402; os do testemunho, da falsidade e da v402 seguem como estão)** · `%s`" % (V["data"][:5], V["s16"])


def linha_topico_novo(V):
    return "- [v403 SELADA: Caminho, Verdade e Vida e a F8.1 (%s)](%s) — **%s** · `%s`" % (V["data"][:5], TOPICO_NOVO, V["teor"], V["s16"])


# v403: o topico novo da memoria (um arquivo por versao)
def topico_novo(V):
    d = _d(V)
    return (("---\nname: %s\ndescription: \"v403 SELADA (%s) `%s`: %d módulos novos no kernel (Caminho, Vida e VerdadeAdendo: os nomes do operador para a ponte da escala dual, a queda sem geometria e a esperança condicional), os registros caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403 (a F8.1: as três bandeiras literais do gate calculadas), %d inscrições de 27/10 por sha256, as erratas E5 e E6, escada %s → %s; B(n) e custódia pendentes\"\n"
             "metadata:\n  type: project\n---\n\n# v403 SELADA (%s)\n\n"
             "**O que é:** `um.py` **v403** `%s` (%s B) sobre a v402 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); o `um.py` cresce %s B (%s%%).\n\n"
             "**O que entrou:** %s.\n\n"
             "**As inscrições de 27/10** (embutidas por sha256; data, sha16, autor e tema — resumo da gerência, não citação; o texto íntegro está em `insumos\\cunhagens`):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"
             "**Pendências:** o nome do triplo inteiro (operador), o elo B(n) da Bancada Um (palavra do operador; passo simples, sem salto; parada e religamento do serviço), a pendência [LEGAL] (D2), a custódia conjunta (sessão do site, com o sidecar), commit/push. Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v403`.\n\n"
             "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v403-custodia]]\n") % (
        TOPICO_NOVO[:-3], V["data"], V["s16"], V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
        format(d["delta"], ","), d["pct"], _num(V), _cunhagens(V), _caminho(V) + "\n\n" + _vida(V) + "\n\n" + _verdade_adendo(V), _leitura_tripla(V), _bandeiras(V), _erratas_e(V), _decisoes(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V) + "\n\n" + _erratas(V)))


# v403: o aviso a coordenadora (so' sob reivindicacao nomeada)
def aviso(V, reivindicacao):
    d = _d(V)
    return (("### %s — v403 SELADA `%s` [claude-c1]\n<!-- aviso_v403_selada -->\n\n[REAL] A v403 SELOU (%s; COMPLETA; gate intocado): Caminho, Verdade (adendo) e Vida, os nomes do operador, e a F8.1 (as três bandeiras literais do gate calculadas; a letra do veredito é a da v402) "
             "entram no selo corrente com as %d inscrições de 27/10 (por sha256; ambas do operador), as erratas E5 e E6 e as decisões D17 a D22. Escrito sob a reivindicação %s. %d módulos novos no kernel; escada %s → %s; "
             "o elo B(n) da Bancada Um, o nome do triplo inteiro e a pendência [LEGAL] esperam o operador. Não altera pinos, dado, MCP nem gate.") % (V["data"], V["s16"], V["teor"], d["n_cun"], reivindicacao, V["n_pedras"], V["escada_antes"], d["depois"]))


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V403_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# ---------------------------------------------------------------- o PARAGRAFO PRONTO do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO; ordem do operador de 23/10: o 4,44 no inicio do artigo, no readme e tudo mais) e (2) o paragrafo NOVO da falsidade
def verificar_paragrafo_readme(par, res, tv):
    """Verifica o paragrafo do QUADRO (texto) contra o RESULTADO pinado (`res`, o JSON lido) e o registro `tv` selado no core: devolve a lista de falhas (vazia = passou). As verificacoes (as mesmas da v397, da v399 e da v402):
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
    from guarda_p18_v403 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    for st in ("[REAL", "[INPUT]", "[KNOWN]", "COMPOSIÇÃO da gerência"):   # os estatutos que o quadro escreve: REAL (os numeros), INPUT (a leitura binaria e a frase), COMPOSICAO da gerencia (as duas faces) e KNOWN (Jeffreys)
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    return fa


def paragrafo_readme():
    """(texto, relatorio): o paragrafo do QUADRO pronto para colar no README do espelho e no site (o MESMO da v397, da v399 e da v402), gerado por quadro_v397.paragrafo_pronto_readme sobre o core SELADO do Nos, verificado contra o resultado pinado
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
    """Falhas de ATRIBUICAO e de DIRECAO num texto renderizado (v403: nao ha inscricao da gerencia; as duas sao falas do operador): (a) nenhuma frase poe a IALD como quem testifica do operador (fora da fala em que ele recusa a ordem inversa);
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
        fa.append("diz que ha inscricao da gerencia (nesta versao as duas inscricoes sao falas do operador)")
    return fa


# v403: o handoff para a sessao do site (memory\handoff-v403-custodia.md + Nos\HANDOFF_v403_CUSTODIA.md); `k` traz os campos dos recibos do B(n) e os paragrafos do README (fechar_v403.py os le dos recibos e do core): nenhum numero digitado
def handoff(V, k):
    d = _d(V); sc = V["sidecar"]
    k = dict(k)
    for chave in ("ap_nome", "ap_sha", "ap_ver", "ap_evento", "ap_bat", "par_sha", "rel_sha", "rel_man", "readme_paragrafo", "readme_paragrafo_v403"):
        assert chave in k, ("o handoff precisa do campo dos recibos do B(n) e dos paragrafos do README: " + chave)
    par = k["readme_paragrafo"].rstrip("\n"); par_f = k["readme_paragrafo_v403"].rstrip("\n"); err = errata_v402_bloco().rstrip("\n")
    assert par.startswith("### O Teste da Única Palavra (v397"), "o paragrafo do README (quadro) nao e' o do quadro"
    assert par_f.startswith("### Caminho, Verdade e Vida (v403"), "o paragrafo da v403 nao e' o novo"
    k.update({"data": V["data"], "s16": V["s16"], "umb": format(V["umb"], ","), "base16": V["base16"], "teor": V["teor"], "rc": V["rc"], "conf16": V["conf16"], "conf_dm": V["conf_dm"], "conf_np": V["conf_np"],
              "pilar": "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), "selo_ts": V["selo_ts"], "num": _num(V), "kernel_prova": _kernel_prova(V), "limites": _limites(V, curto=True), "legal": _legal(V),
              "artigos": ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), "n_cun": d["n_cun"], "n_pedras": V["n_pedras"], "topico": TOPICO_NOVO[:-3], "regra": _regra_do_4_44(V), "erratas_e": _erratas_e(V), "decisoes": _decisoes(V), "tripla": _leitura_tripla(V), "bandeiras": _bandeiras(V),
              "sc_nome": "um_absoluto_selo_acom.json", "sc_sha": sc["sha256"], "sc_ver": sc["veredito"], "sc_bytes": format(sc["bytes"], ","), "sc_objs": "; ".join("`%s` sha256 `%s`" % (n, o["sha256"]) for n, o in sc["objetos"].items()),
              "par_bloco": MARC_PAR_INI + "\n" + par + "\n" + MARC_PAR_FIM, "par_v403_bloco": MARC_V403_INI + "\n" + par_f + "\n" + MARC_V403_FIM, "err_bloco": MARC_ERR_INI + "\n" + err + "\n" + MARC_ERR_FIM})
    doc = ("---\nname: handoff-v403-custodia\ndescription: \"HANDOFF v403 (%(data)s) para a sessão do site: Caminho, Verdade e Vida (os nomes do operador para a ponte da escala dual, a esperança condicional como adendo da pedra Verdade e a queda sem geometria) e a F8.1 (as três bandeiras literais do gate calculadas): três módulos, seis registros, duas falas de 27/10 e as decisões da gerência; `%(s16)s`; B(n) da Bancada feito; TRAZ os parágrafos prontos do README/site (o quadro do Teste da Única Palavra, intocado, e o novo da v403) e a NOTA ao lado do parágrafo da v402; os parágrafos do testemunho de dois, da falsidade e da v402 SEGUEM COMO ESTÃO; LISTA o sidecar; custódia + pendências do operador\"\n"
           "metadata:\n  type: project\n---\n\n# HANDOFF v403 — CUSTÓDIA (%(data)s)\n\n"
           "**O que é:** `um.py` **v403** `%(s16)s` (%(umb)s B) sobre a v402 `%(base16)s`; %(teor)s; COMPLETA; rc %(rc)s; selftest PASSED; gate intocado; conferidor `%(conf16)s` (deve mudar %(conf_dm)s; não pode mudar %(conf_np)s); pilar %(pilar)s pela chave. "
           "Selo `%(selo_ts)s`.\n\n"
           "**PARÁGRAFOS PRONTOS para o README do espelho e para o site (colar como estão, cada um entre os seus marcadores; o primeiro é o quadro do Teste da Única Palavra, o MESMO da v397, intocado; o segundo é novo).** O do quadro é gerado pelas MESMAS funções do quadro do artigo "
           "(a função paragrafo_pronto_readme do módulo quadro_v397), sobre o core SELADO do Nós, com os mesmos números e estatutos, e verificado contra o resultado pinado ANTES de este handoff nascer (o fechar recusa se o z_disc aparecer sem o p calibrado e sem a linha dos 5σ no mesmo item, "
           "se a frase do operador não for a verbatim ou se algum número diferir do resultado). O novo (Caminho, Verdade e Vida) é gerado dos registros selados `caminho_v403`, `vida_v403`, `verdade_adendo_v403`, `bandeiras_do_gate_v403` e `cunhagens_v403` e verificado contra o core e contra os números do ensaio a seco "
           "(sem o z_disc do quadro; as citações são trechos verbatim das falas do operador ou da docstring do kernel embutido; sem alegação de segurança criptográfica):\n\n%(par_bloco)s\n\n%(par_v403_bloco)s\n\n"
           "**NOTA ao lado do parágrafo da v402 (a ponte da escala dual, a queda sem geometria e a esperança condicional) no README e no site (colar logo abaixo dele, entre os marcadores; o parágrafo da v402 fica como registro):**\n\n%(err_bloco)s\n\n"
           "**Os parágrafos do testemunho de dois (v399), da falsidade (v401) e da v402 SEGUEM COMO ESTÃO.** O handoff da v402 (`handoff-v402-custodia.md`) trouxe o da v402 e a errata ao lado do da falsidade, e o da v400 regenerou o do testemunho de dois; são os que estão no README do espelho e no site, e esta versão NÃO os regenera nem os substitui "
           "(o `um.py` mudou de bytes, mas os parágrafos são dos selos daquelas rodadas). Os registros que os geravam (`selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399`, `cunhagens_v399`, `falsidade_da_inercia_v401`, `cunhagens_v401`, `ponte_da_escala_dual_v402`, `queda_sem_geometria_v402`, `esperanca_condicional_v402` e `cunhagens_v402`) "
           "seguem selados e iguais ao ensaio a seco neste rito (a leitura os confere); só a nota do bloco acima acrescenta os nomes do operador ao da v402.\n\n"
           "%(regra)s\n\n%(erratas_e)s\n\n%(decisoes)s\n\n%(tripla)s\n\n%(bandeiras)s\n\n"
           "**O que entrou e o que mediu:** %(num)s.\n\n"
           "**O SIDECAR (arquivo da custódia desde a v399, D5; REESCRITO por este rito):** `%(sc_nome)s` (sha256 `%(sc_sha)s`, %(sc_bytes)s B; veredito `%(sc_ver)s`); objetos selados: %(sc_objs)s. O sidecar fica AO LADO do selo (o selo não pode conter o selo ACOM de si mesmo) e o fechar o copia para `work\\cadeia_de_selo\\v403_selo` e o lista no manifesto de incorporação; "
           "a custódia o leva ao cofre, à PORTA (PORTA.json, URL raw) e ao espelho, junto do selo, porque a segunda testemunha só se confere com ele. A custódia da v399, da v402 e da v403 é CONJUNTA. A recusa do selo ACOM só registra (D4); o SHA-256 segue soberano.\n\n"
           "%(kernel_prova)s\n\n%(limites)s\n\n%(legal)s\n\n"
           "**O elo B(n) da Bancada Um (feito antes deste handoff; passo simples, sem salto):** recibo da aplicação `%(ap_nome)s` (sha256 `%(ap_sha)s`; veredito `%(ap_ver)s`; evento %(ap_evento)s; bateria `%(ap_bat)s`); recibo da parada do serviço sha256 `%(par_sha)s`; "
           "recibo do religamento sha256 `%(rel_sha)s` (versão servida v403, manifesto `%(rel_man)s`).\n\n"
           "**Para a sessão do site (custódia):** o `um.py` v403, `rodada_v403_stdout.txt`, o selo, o sidecar, o core, o .md canônico (com o quadro no topo, intocado) e o manifesto, os artigos PT/EN (%(artigos)s; o quadro «O Teste da Única Palavra» abre os dois), as %(n_cun)s inscrições de 27/10 por sha256 "
           "(as duas são falas do operador; lista na linhagem e no tópico `%(topico)s`; arquivos em `work\\cadeia_de_selo\\v403\\insumos\\cunhagens`), os %(n_pedras)s módulos novos (`work\\cadeia_de_selo\\v403_kernel\\pedras`, `TGLExt/Caminho.lean`, `TGLExt/Vida.lean` e `TGLExt/VerdadeAdendo.lean`) e os dois diffs (`DIFF_v402_v403.diff`, `DIFF_KERNEL_v403.txt`) — com PORTA gerada por script, "
           "URL raw (o um.py tem mais de 5 MB), backup da versão v402 no espelho fora do repositório, blob conferido depois do push. Colocar os PARÁGRAFOS acima no README do espelho e no site (ato da sessão do site, com o selo corrente ao lado; o do quadro e os do testemunho, da falsidade e da v402 seguem onde estão, o da v402 recebe a NOTA ao lado e o novo entra ao lado); "
           "publicar os módulos novos no espelho (TGLExt) e regenerar as PORTAS de `tgl_kernel`, `TGLExt` e `TGL`; a pasta `insumos` (as três pedras, as inscrições pinadas e a medida da cobertura; o resultado do Teste da Única Palavra e os três recibos seguem em `v397\\insumos\\fase9`) vai ao espelho com PORTA: sem ela, uma reprodução pública diz NOT_SEALED (fail-closed); "
           "os recibos da bateria do B(n) vão ao espelho com PORTA; a nota ao lado do registro `kh_n1_cobertura_v402` (h2, h3 e h6 viram pisos; h8, tamanho mínimo) e dos contratos (`expected_ladder`); o runner da Fronteira e a camada v403 dos 16 dispositivos "
           "(o número do runner é da sessão do site); a revisão independente antes do portão do operador (o número de céticos é da sessão do site). A publicação do bloco embutido do método do operador no espelho público segue sujeita à decisão [LEGAL] D2 (operador com a agente de PI).\n\n"
           "**Pendências SÓ do operador:** o nome do triplo inteiro (a leitura [ONTO] da tripla espectral e de João 14,6 deixou três predicados de um só «Eu sou»; a casa já cunhou EU SOU = 1 = 1); a decisão [LEGAL] D2 (publicar o bloco embutido e as adaptações, com a agente de PI); a custódia conjunta, subir o site, commit/push; a ratificação das decisões D18 a D22 da gerência "
           "(a recusa de «Verdade» sozinha; pedra selada não se renomeia por cima; a F8.1; a fonte da bandeira linearized_spin2_finite_face). [OPEN]: a discriminação a 5σ (β_TGL na natureza), `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura e rank c = 4, `IsotropicPost` no atlas curvo, a dimensão 3, a instância do índice 1/β, a atestação física externa e a tipagem (sinapse, token, nome), "
           "a face de Fock do psion (o certificado de Fock da luz sem habitante exibido), o contrato conjunto da rede e a independência das quatro bandeiras experimentais do gate (um só booleano; os mocks de survey).\n\n"
           "Pacote e cadeia: `work\\cadeia_de_selo\\v403` (+ `pos_rito`); arquivo `work\\cadeia_de_selo\\v403_selo` e `v403_kernel`. NOT_FALSIFIED não é a palavra da creditação; o gate não se move.\n\n"
           "[[%(topico)s]] [[missao-ultima-flag-um-py]] [[handoff-v402-custodia]]\n") % k
    assert k["par_bloco"] in doc and k["par_v403_bloco"] in doc and k["err_bloco"] in doc, "os paragrafos do README e a nota nao entraram no handoff"
    assert not atribuicao_da_gerencia(doc), ("o handoff atribui mal ou inverte a direcao do testemunho", atribuicao_da_gerencia(doc)[:2])
    return doc


# ------------------------------------------------------------------- ferramentas da arvore e do indice (OPCIONAIS: so' usadas se alguem escrever patch_arvore_indice_v403.py)
# v403: a linha da arvore da prova
def arvore_linha(V):
    d = _d(V)
    return ("- **CAMINHO, VERDADE E VIDA (v403)** `%s`: %d módulos novos no kernel (%s; os nomes são do operador), %d bandeiras novas True, escada %s → %s; "
            "o Caminho é a ponte da escala dual e a massa NÃO é selecionada pela lei (`lift_mass_not_selected`) [REAL]; a Vida é a queda sem geometria: o peso cai estritamente e o chão é o posto [REAL, sobre os dados da escala dual]; "
            "a Verdade, como adendo da pedra `Verdade` (v392), é a esperança condicional lida pelo Nome (em M2(C), a esperança diagonal lê a projeção da identidade como os pesos) [REAL; ONTO: a tripla espectral]; os registros `caminho_v403`, `vida_v403` e `verdade_adendo_v403` conferem o cálculo; "
            "a F8.1: as três bandeiras literais do gate passam a calculadas (`bandeiras_do_gate_v403`) e a letra do veredito é a da v402 [REAL]; as %d inscrições de 27/10 por sha256 (ambas do operador); `IsotropicPost`, `H_BW`, `H_cal`, H3 e a assinatura são [OPEN]; validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["n_pedras"], _mods(V), d["n_f"], V["escada_antes"], d["depois"], d["n_cun"]))


# v403: o titulo do verbete do indice
def titulo_verbete(V):
    return "Caminho, Verdade e Vida (v403): os nomes do operador e a F8.1:"


# v403: o corpo do verbete do indice
def verbete(V):
    return "[REAL — rodada v403 `%s`] %s." % (V["s16"], _num(V))


# v403: a entrada do remissivo
def remissivo(V):
    return "- **Caminho, Verdade e Vida, as bandeiras do gate calculadas (F8.1) e as inscrições de 27/10 (v403)** — `caminho_v403`, `vida_v403`, `verdade_adendo_v403`, `bandeiras_do_gate_v403`, `cunhagens_v403`, `kh_n1_cobertura_v403`, `%s`" % TOPICO_NOVO


MARC_V403_INI = "<!-- INICIO_PARAGRAFO_CAMINHO_VERDADE_VIDA_v403 -->"; MARC_V403_FIM = "<!-- FIM_PARAGRAFO_CAMINHO_VERDADE_VIDA_v403 -->"


MARC_ERR_INI = "<!-- INICIO_ERRATA_V402_V403 -->"; MARC_ERR_FIM = "<!-- FIM_ERRATA_V402_V403 -->"


_CHAVES = ("caminho", "vida", "verdade_adendo")


def _lst(xs):
    """Lista numerica lida do registro, em PT: inteiros sem casas, listas aninhadas entre parenteses."""
    return ", ".join(("(" + _lst(x) + ")") if isinstance(x, (list, tuple)) else _pn(x, 6) for x in xs)


def _sem_chaves(t):
    """Os textos vindos do core podem trazer chaves (e^{-s}); os textos renderizados nao as tem (a conferencia de formatacao reprova): chaves viram parenteses."""
    return t.replace("{", "(").replace("}", ")")


def _cod025():
    """O sha16 da ORDEM 025 ao Codex (a ponte da escala dual da v402, hoje o Caminho), LIDO do registro com funcao da ponte da v402, recriado no core do Nos."""
    return _g(_core(), "ponte_da_escala_dual_v402", "codex_order", "sha16")


def _erratas_e(V):
    """As erratas E5 e E6 (em nome proprio da gerencia c1), LIDAS do registro cunhagens_v403 do core: nenhuma e' digitada aqui."""
    _d(V); er = _g(_core(), "cunhagens_v403", "erratas") or []
    itens = []
    for e in er:
        itens.append(_sem_chaves("- %s **Dizia:** %s **Lacuna de fidelidade:** %s **Estatuto:** %s" % (e["agora"], e["dizia"], e["lacuna_de_fidelidade"], e.get("estatuto", ""))))
    return ("**Erratas ao lado (em nome próprio da gerência c1, 27/10/2026; os textos da v402, o registro `f81_nao_fechada_v392` e as pedras seladas ficam como registro; nenhum módulo já instalado foi editado):** a F8.1 e os nomes entram COM duas erratas, lidas do registro `cunhagens_v403`:\n" + "\n".join(itens))


def _decisoes(V):
    """As decisoes D17 a D22 (D17 e' do operador, ratificando a leitura da gerencia; D18 a D22 sao da gerencia c1), LIDAS do registro cunhagens_v403."""
    _d(V); ds = _g(_core(), "cunhagens_v403", "extras", "decisoes_da_gerencia") or {}
    ks = ("D17", "D18", "D19", "D20", "D21", "D22")
    assert all(k in ds for k in ks), "as decisoes D17 a D22 nao estao no registro cunhagens_v403"
    nota22 = ("\n- Nota da gerência c1 (28/10/2026): a D22 já traz a ratificação da gerência c1 de 27/10/2026 (ls2_keys da base conferidas: as seis bandeiras ext_ls2_*), registrada também na rota da preparação, no mapa de rotas.")
    return "**Decisões** [D17 é do operador, 27/10/2026, ratificando a leitura da gerência c1; D18 a D22 são da gerência c1, em nome próprio, ratificáveis pelo operador]:\n" + _sem_chaves("\n".join("- %s: %s" % (k, ds[k]) for k in ks)) + nota22


# ---------------------------------------------------------------- o PARAGRAFO NOVO da v403 e a NOTA ao lado do paragrafo da v402
def _linha_maquina_v403(core, d):
    """A linha de maquina do paragrafo novo (os numeros LIDOS dos registros do core), em PT."""
    cv = core["caminho_v403"]["values"]; vv = core["vida_v403"]["values"]; av = core["verdade_adendo_v403"]["values"]; gv = core["bandeiras_do_gate_v403"]["values"]
    return ("pedras_sha16=%s/%s/%s; bandeiras=%s; beta=%s; caminho_massas_mesmo_p+=%s; caminho_p+_em_beta=%s; vida_peso_s1=%s; vida_custo_min=%s; vida_defasagem_max=%s; vida_perda_unit=%s; verdade_alfa=%s; verdade_alfa2=%s; verdade_pesos_somam=%s; gate=%s/%s/%s/%s; checagens=%s/%s/%s/%s/%s; falas_sha16=%s/%s"
            % (d["sha"]["caminho"], d["sha"]["vida"], d["sha"]["verdade_adendo"], d["n_f"], _p(cv["beta"], 12), _lst(cv["lifts_same_pplus_masses"]), _p(cv["pplus_factor_at_beta"], 9), _p(vv["post_weight_at_scale_one"], 6), _p(vv["min_cost_t_beta_g"], 9), _p(vv["max_dephasing_factor"], 9), _p(vv["loss_per_unit"], 9),
               _p(av["alpha"], 12), _pe(av["alpha_squared"], 6), _pn(av["weights_sum"], 3), gv["n_true"], gv["n_calculated"], gv["n_literal"], gv["n_read_by_the_verdict"],
               core["caminho_v403"]["mechanics"]["n_checks"], core["vida_v403"]["mechanics"]["n_checks"], core["verdade_adendo_v403"]["mechanics"]["n_checks"], core["bandeiras_do_gate_v403"]["mechanics"]["n_checks"], d["n_ck_cun"], d["s_nome"], d["s_ok"]))


def _dados_paragrafo(core):
    """O que o paragrafo precisa do core SELADO e de ESPERADOS (sem V): as sha16 das pedras, as bandeiras, as falas e a ORDEM 025."""
    esp = _esp(); DL_ = _qd().DL; ks = _CHAVES
    for n in ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403"):
        assert (core.get(n) or {}).get("all_verified") is True, "o registro %s nao selou: nenhum paragrafo diz os numeros assim" % n
    sha = {k: esp["pedras"][DL_.STONE_BY_KEY[k]["rel"]]["sha16"] for k in ks}
    s402 = {"ponte": esp["pedras_v402_sha256"]["TGLExt/PonteDaEscalaDual.lean"][:16], "queda": esp["pedras_v402_sha256"]["TGLExt/QuedaSemGeometria.lean"][:16], "esperanca": esp["pedras_v402_sha256"]["TGLExt/EsperancaCondicional.lean"][:16]}
    return {"sha": sha, "n_f": esp["n_bandeiras_novas"], "n_g": dict(esp["n_bandeiras_por_grupo"]), "est_f": {k: esp["estrelas_v403"][k]["bandeira"] for k in ks}, "est_t": {k: esp["estrelas_v403"][k]["teorema"] for k in ks},
            "n_ck_cun": len(core["cunhagens_v403"].get("checks") or []), "s_nome": _sha_por("nome_verdade_triplo_espectral"), "s_ok": _sha_por("e_isso_mesmo_concordo"), "o025": _g(core, "ponte_da_escala_dual_v402", "codex_order", "sha16"), "s402": s402, "vsha": _sha_verdade()}


def _paragrafo_v403_de(core):
    """O texto do paragrafo da v403, funcao PURA dos registros caminho_v403, vida_v403, verdade_adendo_v403, bandeiras_do_gate_v403 e cunhagens_v403 do core SELADO (os numeros sao lidos dos registros, nunca digitados)."""
    d = _dados_paragrafo(core)
    cv = core["caminho_v403"]["values"]; vv = core["vida_v403"]["values"]; av = core["verdade_adendo_v403"]["values"]; gv = core["bandeiras_do_gate_v403"]["values"]
    assert cv.get("beta") and vv.get("beta") and av.get("beta") and gv.get("n_flags") and d["o025"], "os registros da v403 nao trazem os valores: nenhum paragrafo diz os numeros assim"
    q_nome = _cita('a meu ver o nome é "verdade" (poderia ser "caminho, verdade e vida")'); q_ok = _cita("é isso mesmo, concordo com tudo, prossiga"); q_piso = _um_texto_tem("não existe acima, o piso limita")
    qg = core.get("qg_closure") or {}; fam = [len(qg.get(f) or {}) for f in ("formal_flags", "physics_flags", "experiment_flags")]; DL_ = _qd().DL
    ev = _g(core, "esperanca_condicional_v402", "values") or {}
    ls = ["### Caminho, Verdade e Vida (v403, 27/10/2026) — parágrafo pronto para o README do espelho e para o site",
          "",
          "> **Caminho, Verdade e Vida (v403, 27/10/2026)** [REAL: os termos do kernel e a conferência do cálculo nos modelos · KNOWN: a lei de escala de Takesaki, Bisognano–Wichmann, a esperança condicional · DERIVED: as conjunções por citação e a conta nova do adendo · INPUT: os nomes, do operador · ONTO: a leitura pela tripla espectral e por João 14,6 · "
          "OPEN: `H_BW`, `H_cal`, H3, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3 e a instância do índice · DECLARADO: a leitura da gerência que o operador ratificou foi a apresentada na sessão, e as quatro bandeiras experimentais do gate derivam de um só booleano]",
          ">",
          "> - **Os nomes** [INPUT] (sha16 `%s` e `%s`): o operador disse %s e, sobre a leitura da gerência, %s. CAMINHO é a ponte da escala dual, VIDA é a queda sem geometria e VERDADE é a esperança condicional, como ADENDO da pedra `Verdade` (v392, sha16 `%s`). «Verdade» sozinha para as três foi recusada (homônimo do módulo `Verdade`); "
          "as três pedras seladas da v402 (`PonteDaEscalaDual` `%s`, `QuedaSemGeometria` `%s` e `EsperancaCondicional` `%s`) ficam como REGISTRO e os módulos novos as compõem por citação e por adendo; o nome do triplo inteiro não foi dado." % (d["s_nome"], d["s_ok"], q_nome, q_ok, d["vsha"], d["s402"]["ponte"], d["s402"]["queda"], d["s402"]["esperanca"]),
          "> - **O Caminho** [REAL · KNOWN · DERIVED] (módulo `Caminho`, sha16 `%s`; ponte do Codex, ORDEM 025 sha16 `%s`): a conjunção, incondicional, de dois termos que o kernel já tinha, sem matemática nova: a lei de escala de Takesaki ([KNOWN], campo da estrutura) realizada como o boost longitudinal sobre (E, p), com c = 1, deixa a massa livre — dois invariantes μ² distintos dão duas realizações distintas com o MESMO p⁺ (`lift_mass_not_selected`, a estrela) — "
          "e todo μ² ≥ 0 tem realização positiva (`core_positive_realization_exists`). Com β = α√e = %s em runtime, as massas ao quadrado %s dão o mesmo p⁺, o repouso ganha energia em toda escala não trivial (ganho mínimo %s) e o p⁺ encolhe pelo fator %s em s = β. Assim a massa NÃO é selecionada pela lei: m² = p⁺p⁻ é o invariante e a energia é a leitura do observador."
          % (d["sha"]["caminho"], d["o025"], _p(cv["beta"], 12), _lst(cv["lifts_same_pplus_masses"]), _p(cv["min_rest_energy_gain"], 6), _p(cv["pplus_factor_at_beta"], 9)),
          "> - **A Vida** [REAL · ONTO · OPEN] (módulo `Vida`, sha16 `%s`): a conjunção, incondicional, de `the_fall_is_strictly_anti` (s ↦ τ(θ_s m) é estritamente decrescente: a fase cai, sem fim; a estrela) e `a_queda_sem_geometria` (a seta é o sinal de s, a entrega custa, o regime angular só lê, a isotropia é a hipótese NOMEADA `IsotropicPost`). "
          "O CHÃO é o POSTO (peso 1 = ω(I)), nunca o 0 [decisão D11 da v402, mantida]: o kernel diz na Fundação %s. Neste rito, o peso em s = 1 vale %s; o custo mínimo t·β·g vale %s (> 0), o fator de defasagem tem máximo %s (< 1) e a perda por unidade vale %s; o regime angular tem período %s e só lê. "
          "A queda é do PESO, em nats, sem geometria. A dimensão 3 NÃO é provada no kernel (a validade é só a dos termos do trio) e o 1 + 3 é leitura [ONTO]." % (d["sha"]["vida"], q_piso, _p(vv["post_weight_at_scale_one"], 6), _p(vv["min_cost_t_beta_g"], 9), _p(vv["max_dephasing_factor"], 9), _p(vv["loss_per_unit"], 9), _p(vv["angular_period"], 6)),
          "> - **A Verdade, como ADENDO** [REAL · KNOWN · DERIVED · ONTO] (módulo `VerdadeAdendo`, sha16 `%s`): a esperança condicional da v402 é a Verdade lida pelo Nome (`nameOp`); a pedra `Verdade` fica INTACTA. Um teorema novo e pequeno (`the_name_reads_the_inscription_as_weights`, a estrela): em M2(C), a esperança diagonal lê a projeção da identidade como os seus pesos, "
          "`diagExpect (identityProj a)` = diag(q², a²); a composição `verdade_lida_pelo_nome` diz que o Nome de ρ* PRESERVA O UM (traço 1) e que reler não acrescenta. Com α = %s (CODATA 2018, a entrada do programa; β = α√e em runtime; um parâmetro, nunca um número no teorema), os pesos (1 − α², α²) = (%s, %s) somam %s, e o peso de dentro α² é menor que β: a Verdade guarda α², não β. "
          "O índice 1/β (%s) é CONDICIONAL a duas hipóteses nomeadas da v402 e nenhuma instância é construída. [ONTO] O Nome é a Verdade lida pelo operador que lê; o kernel prova as ligações, não uma igualdade de tipos." % (d["sha"]["verdade_adendo"], _p(av["alpha"], 12), _p(av["q_squared_at_alpha"], 12), _pe(av["alpha_squared"], 6), _pn(av["weights_sum"], 3), _p(ev["name_index_one_over_beta"], 4)),
          "> - **As bandeiras do gate (F8.1)** [REAL · DERIVED · DECLARADO] (registro `bandeiras_do_gate_v403`): das %s bandeiras do gate (%s formais, %s físicas e %s experimentais), %s são True e %s são CALCULADAS (%s literais); a função do veredito lê %s (%s + %s + %s) e as outras %s são informativas. "
          "As três que eram literais (`linearized_spin2_finite_face`, `protocol_pre_registered`, `null_tests_passed_blind`) passam a ser lidas das suas fontes, fail-closed: a família ext_ls2_* do kernel (%s bandeiras), a checagem «%s» do rito V11 e o `all_verified` do teste nulo cego. A letra do veredito do gate é a da v402: o gate não se move. "
          "[DECLARADO] As quatro bandeiras experimentais derivam de UM só booleano (o veredito do V11); a F8.1 troca literais por medida, não independentiza o feed, e o degrau experimental lê só o rito V11 do piso, unilateral."
          % (gv["n_flags"], fam[0], fam[1], fam[2], gv["n_true"], gv["n_calculated"], gv["n_literal"], gv["n_read_by_the_verdict"], gv["read_by_the_verdict"][0], gv["read_by_the_verdict"][1], gv["read_by_the_verdict"][2], gv["n_flags"] - gv["n_read_by_the_verdict"], gv["ext_ls2_n"], DL_.F81_ROTULO_PREREG),
          "> - **A leitura pela tripla espectral** [ONTO · DECLARADO]: na tripla espectral de Connes do artigo fundador da fatoração (03/2026), o espaço dos estados com o seu fluxo é o Caminho, o operador de Dirac dá a distância sem pontos (a Vida é a queda que mede em nats sem geometria) e a álgebra é o que a Verdade lê; em João 14,6 as três palavras são predicados de um só «Eu sou». "
          "É leitura da gerência c1, ratificada pelo operador; não é termo de kernel.",
          "> - **Erratas ao lado (gerência c1, em nome próprio, 27/10/2026):** E5, a errata de 13/10/2026 (v392) e o registro `f81_nao_fechada_v392` eram verdadeiros na sua data e ficam como registro; na v403 as três literais passam a calculadas, a independência das quatro experimentais não é resolvida e a letra do veredito é a da v402; "
          "E6, os nomes dos três módulos e dos cinco registros da v402 eram provisórios (D16 da v402); o operador os nomeou e os módulos selados não foram renomeados.",
          "> - **Limites:** [OPEN] `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost` no atlas curvo, a dimensão 3, a instância e o caso III₁ do índice 1/β e a atestação física externa; as pedras NÃO provam a primeira lei de Newton, nem que E = mc² seja composta da escala, nem a dimensão 3, nem a assinatura (1,3), nem o rank c = 4; o cálculo CONFERE os teoremas nos modelos e quem prova é o kernel, e esses números são deste rito, não estão no kernel; a gravidade quântica segue sem creditação na natureza; "
          "validade no kernel não é creditação; `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; isto não é teste e não acrescenta dado. O quadro do Teste da Única Palavra segue no README com a sua linha dos 5σ; este parágrafo não traz o número do quadro.",
          "> - **Origem.** Os números são lidos do core selado desta rodada (registros `caminho_v403`, `vida_v403`, `verdade_adendo_v403`, `bandeiras_do_gate_v403` e `cunhagens_v403`); nenhum é digitado. Linha de máquina: `%s`." % _linha_maquina_v403(core, d)]
    return "\n".join(ls) + "\n"


def verificar_paragrafo_v403(par, core, esp):
    """Verifica o paragrafo da v403 contra o core selado E contra ESPERADOS (o ensaio a seco): devolve a lista de falhas (vazia = passou). As verificacoes:
    (1) os numeros do core (os quatro registros com funcao) == os de ESPERADOS[registros_funcao_v403][k][values] e cada um esta no paragrafo, formatado; (2) o paragrafo == o gerado do core; (3) NAO traz o 4,44 nem o z_disc (a regra do 4,44 e' do quadro); (4) os estatutos;
    (5) as frases de limite; (6) toda citacao entre « » e' verbatim numa fala DO OPERADOR ou na docstring do kernel embutido; (7) nenhuma alegacao de seguranca criptografica, «consciencia» so' como palavra retirada, a direcao sem inversao; (8) guarda P18."""
    fa = []
    ef = esp.get("registros_funcao_v403") or {}
    def _eq(a, b):
        return (isinstance(a, float) and isinstance(b, float) and abs(a - b) <= 1e-12 * max(1.0, abs(b))) if isinstance(b, float) else a == b
    for k, rn in (("caminho", "caminho_v403"), ("vida", "vida_v403"), ("verdade_adendo", "verdade_adendo_v403"), ("gate", "bandeiras_do_gate_v403")):
        fv = (core.get(rn) or {}).get("values") or {}; ev = (ef.get(k) or {}).get("values") or {}
        if not (fv and ev and all(_eq(fv.get(kk), vv) if not isinstance(vv, (list, dict)) else fv.get(kk) == vv for kk, vv in ev.items())):
            fa.append("numero do registro %s no core != ESPERADOS" % rn)
    cv = (core.get("caminho_v403") or {}).get("values") or {}; vv_ = (core.get("vida_v403") or {}).get("values") or {}; av_ = (core.get("verdade_adendo_v403") or {}).get("values") or {}; gv_ = (core.get("bandeiras_do_gate_v403") or {}).get("values") or {}
    try:
        nums = {"beta": _p(cv["beta"], 12), "massas": _lst(cv["lifts_same_pplus_masses"]), "ganho do repouso": _p(cv["min_rest_energy_gain"], 6), "fator de p+": _p(cv["pplus_factor_at_beta"], 9), "peso em s = 1": _p(vv_["post_weight_at_scale_one"], 6), "custo minimo": _p(vv_["min_cost_t_beta_g"], 9),
                "defasagem maxima": _p(vv_["max_dephasing_factor"], 9), "perda por unidade": _p(vv_["loss_per_unit"], 9), "periodo": _p(vv_["angular_period"], 6), "alfa": _p(av_["alpha"], 12), "q2": _p(av_["q_squared_at_alpha"], 12), "alfa2": _pe(av_["alpha_squared"], 6),
                "indice": _p((_g(core, "esperanca_condicional_v402", "values") or {})["name_index_one_over_beta"], 4), "bandeiras": str(gv_["n_flags"]), "sha16 da fala do nome": _sha_por("nome_verdade_triplo_espectral"), "sha16 da ratificacao": _sha_por("e_isso_mesmo_concordo"), "ORDEM 025": str(_g(core, "ponte_da_escala_dual_v402", "codex_order", "sha16"))}
    except KeyError as e:
        nums = {}; fa.append("valor ausente do registro: %s" % e)
    for k, v in nums.items():
        if v not in par:
            fa.append("numero (%s = %s) ausente do paragrafo" % (k, v))
    try:
        if par != _paragrafo_v403_de(core):
            fa.append("o paragrafo difere do gerado pelas funcoes sobre os registros selados do core")
    except AssertionError as e:
        fa.append("o paragrafo nao pode ser gerado do core: %s" % str(e)[:120])
    if re.search(r"4[,.]44|z_disc", par):
        fa.append("o paragrafo da v403 traz o 4,44 ou o z_disc (a regra do 4,44 e' do quadro; este paragrafo nao o cita)")
    for st in ("[REAL", "[KNOWN]", "[INPUT]", "[ONTO", "[OPEN]", "[DECLARADO]", "DERIVED"):
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    for frase in ("a massa NÃO é selecionada pela lei", "O CHÃO é o POSTO", "nunca o 0", "NÃO é provada", "ADENDO", "PRESERVA O UM", "CONDICIONAL", "nenhuma instância é construída", "CALCULADAS", "UM só booleano", "o nome do triplo inteiro não foi dado", "ficam como REGISTRO",
                  "NÃO provam a primeira lei de Newton", "CONFERE os teoremas", "quem prova é o kernel", "validade no kernel não é creditação", "o gate não se move", "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "Erratas ao lado", "letra do veredito do gate é a da v402"):
        if frase not in par:
            fa.append("frase de limite ausente do paragrafo: " + frase)
    corpus = [re.sub(r"\s+", " ", d["text"]) for d in _falas().values() if d["autor"] == "operador"]
    um = _CACHE.get("um") or open(os.path.join(NOS, "um.py"), encoding="utf-8", errors="replace").read(); _CACHE["um"] = um
    if "não existe acima, o piso limita" in um.replace("**", ""):
        corpus.append("não existe acima, o piso limita")   # a UNICA frase do kernel embutido que o paragrafo cita (a docstring da Fundacao); o um.py inteiro NAO entra no corpus das citacoes
    rotulos = {"Inertial", _qd().DL.F81_ROTULO_PREREG}   # o rotulo da checagem do rito V11 e' nome de checagem (DL.F81_ROTULO_PREREG), nao fala
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
    from guarda_p18_v403 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    return fa


def paragrafo_v403():
    """(texto, relatorio): o paragrafo NOVO da v403, pronto para colar no README do espelho e no site, gerado do core SELADO do Nos e verificado contra o core E contra ESPERADOS;
    levanta AssertionError (o fechar RECUSA) se algo nao conferir."""
    core = _core(); esp = _esp()
    par = _paragrafo_v403_de(core)
    fa = verificar_paragrafo_v403(par, core, esp)
    assert not fa, ("o paragrafo da v403 nao passou nas verificacoes", fa[:4])
    return par, {"sha16": hashlib.sha256(par.encode("utf-8")).hexdigest()[:16], "verificacoes": "numeros == ESPERADOS; igual ao gerado do core; sem o 4,44; estatutos; limites; citacoes verbatim (falas do operador, kernel embutido); sem alegacao de seguranca criptografica; guarda P18", "guarda_p18": "limpa"}


def errata_v402_bloco():
    """O bloco de NOTA ao lado do paragrafo da v402 (a ponte, a queda e a esperanca) no README do espelho e no site: os nomes que ele trazia como provisorios sao agora os do operador (E6). Texto da gerencia, conferido pela guarda P18 e pelo kernel; as citacoes saem dos bytes das falas."""
    _kernel_tem(("lift_mass_not_selected", "the_fall_is_strictly_anti", "esperanca_condicional_e_nome", "caminho_e_a_ponte_da_escala_dual"))
    q_ok = _cita("é isso mesmo, concordo com tudo, prossiga")
    t = ("> **Nota ao lado do parágrafo «A ponte da escala dual, a queda sem geometria e a esperança condicional» (v402) — gerência c1, em nome próprio, 27/10/2026:** os nomes dos três módulos e dos cinco registros que aquele parágrafo traz como PROVISÓRIOS foram dados pelo operador em 27/10/2026 [INPUT]: "
         "CAMINHO é a ponte da escala dual, VIDA é a queda sem geometria e VERDADE é a esperança condicional, como ADENDO da pedra `Verdade` (v392), ratificados em " + q_ok + " (sha16 " + _sha_por("e_isso_mesmo_concordo") + "). "
         "Os módulos selados da v402 (`PonteDaEscalaDual`, `QuedaSemGeometria` e `EsperancaCondicional`) NÃO foram renomeados — ficam como REGISTRO (pedra selada não se renomeia por cima); os módulos novos `Caminho`, `Vida` e `VerdadeAdendo` os compõem por citação e por adendo, e os registros da v402 seguem selados com os nomes da v402. "
         "«Verdade» sozinha para as três foi recusada (homônimo do módulo `Verdade`) e o nome do triplo inteiro não foi dado. O que o parágrafo da v402 diz sobre as pedras, o cálculo e os limites não muda; ele fica como registro.\n")
    sys.path.insert(0, PK)
    from guarda_p18_v403 import violacoes
    assert not violacoes(t), "a guarda P18 achou palavra recusada na nota ao lado do paragrafo da v402"
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


def g_flag(V, k):
    """A bandeira da COMPOSICAO de uma pedra (o teorema incondicional), lida de ESPERADOS."""
    return _esp()["bandeiras_das_pedras"][k]


def _sha_verdade():
    """O sha16 da pedra Verdade (v392) no kernel do Nos (o homonimo que a «Verdade» sozinha repetiria), LIDO do arquivo."""
    return s16(os.path.join(NOS, "tgl_kernel", "TGLExt", "Verdade.lean"))


def _caminho(V):
    """O Caminho (a ponte da escala dual, nome do operador): [REAL] os termos do kernel · [KNOWN] Takesaki, Bisognano-Wichmann, relatividade restrita · [DERIVED] a conjuncao · [INPUT] o nome · [ONTO] a leitura pela tripla espectral e por Joao 14,6 · [OPEN] H_BW, H_cal, H3, a assinatura e rank c = 4."""
    d = _d(V); cv = V["caminho"]["values"]
    q_nome = _cita('a meu ver o nome é "verdade" (poderia ser "caminho, verdade e vida")'); q_ok = _cita("é isso mesmo, concordo com tudo, prossiga")
    return _f("**O Caminho [REAL: os termos do kernel e a conferência do cálculo · KNOWN: Takesaki, Bisognano–Wichmann, a relatividade restrita · DERIVED: a conjunção · INPUT: o nome · ONTO: a leitura pela tripla espectral e por João 14,6 · OPEN: `H_BW`, `H_cal`, H3, a assinatura e rank c = 4]** "
              "(módulo `Caminho`; `TGLExt/Caminho.lean`, sha16 `{h}`; {n_c} bandeira, {c0}; o nome é do operador: {q_nome} e {q_ok}, `{s_nome}` e `{s_ok}`): o Caminho é a ponte da escala dual da v402 (`PonteDaEscalaDual`, sha16 `{o1}`, do Codex, ORDEM 025 sha16 `{o025}`, que fica como REGISTRO com as suas erratas E1 a E4). "
              "A pedra não repete matemática: CITA. Ela é a conjunção, incondicional, de dois termos que o kernel já tinha desde a v402: "
              "(i) ★ `lift_mass_not_selected`: com τ(a) ≠ 0, dois invariantes μ² distintos dão duas realizações equivariantes DISTINTAS com o MESMO p⁺ — a lei de escala de Takesaki ([KNOWN], dado) determina a componente nula e deixa a massa livre; "
              "(ii) `core_positive_realization_exists`: para todo perfil e todo μ² ≥ 0 há uma realização positiva do núcleo, com p⁺ > 0, m² = μ² e energia > 0 (composição `{unc}`, bandeira `{est}`). "
              "O cálculo (β = α√e = {beta} em runtime) CONFERE no modelo longitudinal (E, p), c = 1: m² = p⁺p⁻ é o invariante sob p± ↦ e^(∓s)p±, a energia é a LEITURA do observador (o repouso ganha energia em toda escala não trivial, ganho mínimo {mg}) e a massa NÃO é selecionada pela lei "
              "(as massas ao quadrado {ms} dão o mesmo p⁺ = {same}); o levantamento é equivariante nas {grid} escalas de teste; esses números são deste rito, não estão no kernel. "
              "[ONTO] Na tripla espectral de Connes do artigo fundador da fatoração (03/2026), o espaço dos estados com o seu fluxo é o Caminho: a lei pela qual a leitura viaja sem escolher o corpo; e em João 14,6 as três palavras são predicados de um só «Eu sou». "
              "É leitura da gerência c1, ratificada pelo operador; não é termo de kernel, nem igualdade de tipos, nem prova de que a ponte seja o fluxo modular. "
              "[OPEN] `H_BW` (a rapidez é o tempo modular de Bisognano–Wichmann), `H_cal`, H3 em toda direção nula, a assinatura (a positividade completa dá a métrica induzida (4,0), não (1,3)) e rank c = 4 seguem NOMEADAS (v402); nada do Caminho as paga. "
              "A forma literal de `H_tau` (τ é a massa de Newton) segue REFUTADA no kernel (E1).",
              h=d["sha"]["caminho"], n_c=d["n_g"]["caminho"], c0=_faixa(d["ft"]["caminho"], d["n_g"]["caminho"]), q_nome=q_nome, q_ok=q_ok, s_nome=d["s_nome"], s_ok=d["s_ok"], o1=d["s402"]["ponte"], o025=d["o025"], unc=d["unc"]["caminho"].split(".")[-1], est=d["est_f"]["caminho"],
              beta=_p(cv["beta"], 12), mg=_p(cv["min_rest_energy_gain"], 6), ms=_lst(cv["lifts_same_pplus_masses"]), same=_pn(cv["same_pplus"], 3), grid=cv["grid_scales"])


def _vida(V):
    """A Vida (a queda sem geometria, nome do operador): [REAL] os termos do kernel · [INPUT] o nome · [ONTO] a leitura pela tripla espectral e a leitura 1 + 3 · [OPEN] IsotropicPost, a dimensao 3, o atlas curvo."""
    d = _d(V); vv = V["vida"]["values"]
    q_nome = _cita('a meu ver o nome é "verdade" (poderia ser "caminho, verdade e vida")'); q_ok = _cita("é isso mesmo, concordo com tudo, prossiga"); q_piso = _um_texto_tem("não existe acima, o piso limita")
    return _f("**A Vida [REAL: os termos do kernel e a conferência do cálculo · INPUT: o nome · ONTO: a leitura pela tripla espectral e a leitura 1 + 3 · OPEN: `IsotropicPost`, a dimensão 3 e o atlas curvo]** "
              "(módulo `Vida`; `TGLExt/Vida.lean`, sha16 `{h}`; {n_v} bandeira, {v0}; o nome é do operador: {q_nome} e {q_ok}): a Vida é a queda sem geometria da v402 (`QuedaSemGeometria`, sha16 `{o2}`, que fica como REGISTRO). A pedra CITA: é a conjunção, incondicional, de dois termos que o kernel já tinha: "
              "(i) ★ `the_fall_is_strictly_anti`: com 0 < τ m, s ↦ τ(θ_s m) é estritamente decrescente — a fase cai, sem fim; (ii) `a_queda_sem_geometria`: sob o posto, a queda estrita e linear em nats, a seta pelo sinal de s, nunca o zero, a entrega que custa, o relaxamento ao ponto final, "
              "o regime angular que só lê (período 2π, sem limite: `Smat_has_no_limit`) e a hipótese NOMEADA `IsotropicPost` (composição `{unc}`, bandeira `{est}`). "
              "O CHÃO é o POSTO (peso 1 = ω(I), o corte a = 0: `the_floor_fixes_the_cut`), nunca o ínfimo 0: o zero é o `abismo` da Fundação [decisão D11 da v402, mantida]; o kernel diz na Fundação {q_piso}. "
              "O cálculo CONFERE (β = α√e = {beta} em runtime): o peso depois da escala s é e^(−s) (vale {w1} em s = 1 e {w_1} em s = −1, em {grid} escalas), a queda em nats é s e a seta é o sinal de s; a entrega custa (o custo t·β·g tem mínimo {mincost} > 0, o fator de defasagem tem máximo {maxd} < 1 e vale {deph} em t = 1, g = 1; a perda por unidade vale {loss}); "
              "o peso cai abaixo de todo ε testado sem tocar o zero ({n_ab} testemunhos do abismo); o regime angular tem período {per} e só lê; e a isotropia é carga de um modelo finito (grupo de ordem {ordem}). "
              "[ONTO] A queda com chão é vida; a queda sem chão é o abismo da Fundação (v390). Na tripla espectral de Connes, o operador de Dirac dá a distância sem pontos: a Vida é a queda que mede em nats sem geometria. É leitura da gerência c1, ratificada pelo operador; não é termo de kernel. "
              "[OPEN] `IsotropicPost` é hipótese NOMEADA e carga (`covariance_is_load_bearing`; `s8_h3_is_load_bearing`: com fonte anisotrópica a H3 falha): a dimensão 3 NÃO é provada no kernel (a validade é só a dos termos do trio) e o 1 + 3 é leitura [ONTO]; que o parâmetro s seja a fase de um corpo físico, a H3 em toda tela e direção e o atlas curvo seguem abertos. "
              "A queda é do PESO, em nats, e não é força nem queda no espaço.",
              h=d["sha"]["vida"], n_v=d["n_g"]["vida"], v0=_faixa(d["ft"]["vida"], d["n_g"]["vida"]), q_nome=q_nome, q_ok=q_ok, o2=d["s402"]["queda"], unc=d["unc"]["vida"].split(".")[-1], est=d["est_f"]["vida"], q_piso=q_piso, beta=_p(vv["beta"], 12),
              w1=_p(vv["post_weight_at_scale_one"], 6), w_1=_p(vv["post_weight_at_minus_one"], 6), grid=vv["grid_scales"], mincost=_p(vv["min_cost_t_beta_g"], 9), maxd=_p(vv["max_dephasing_factor"], 9), deph=_p(vv["dephasing_factor_at_t1_g1"], 9), loss=_p(vv["loss_per_unit"], 9),
              n_ab=len(vv["abyss_witnesses"]), per=_p(vv["angular_period"], 6), ordem=vv["finite_model_group_order"])


def _verdade_adendo(V):
    """A Verdade, como adendo (a esperanca condicional, nome do operador): [REAL] os termos do kernel e a conta nova · [KNOWN] esperanca condicional · [DERIVED] a composicao · [INPUT] o nome · [ONTO] o Nome como a Verdade lida pelo operador que le · [OPEN] a instancia e o caso III1."""
    d = _d(V); av = V["verdade_adendo"]["values"]; ev = _g(_core(), "esperanca_condicional_v402", "values") or {}
    q_nome = _cita('a meu ver o nome é "verdade" (poderia ser "caminho, verdade e vida")'); q_ren = _cita("pode ser que eu já tenha a renomeado assim em outro lugar"); q_tri = _cita("é o triplo espectral do contorno verdadeiro"); q_ok = _cita("é isso mesmo, concordo com tudo, prossiga")
    return _f("**A Verdade, como adendo [REAL: os termos do kernel e a conta nova · KNOWN: esperança condicional (Umegaki, Tomiyama) · DERIVED: a composição · INPUT: o nome · ONTO: o Nome como a Verdade lida pelo operador que lê · OPEN: a instância do índice e o caso III₁]** "
              "(módulo `VerdadeAdendo`; `TGLExt/VerdadeAdendo.lean`, sha16 `{h}`; {n_a} bandeiras, {a0}; o nome é do operador: {q_nome}, {q_tri}; ratificado em {q_ok}): o operador suspeitou que {q_ren}. Sim: a pedra `Verdade` (v392, «a identidade tem nome»; sha16 `{vsha}`) já existe — a estrutura `Verdade a` guarda a inscrição quadrática 1 = q² + α², "
              "a projeção `identityProj a` (traço 1, idempotente, posto 1) e a relação com reler (`rereading_the_post`). A esperança condicional da v402 (`EsperancaCondicional`, sha16 `{o3}`, que fica como REGISTRO) é essa mesma projeção do posto levada do projetor de posto 1 à esperança condicional sobre a subálgebra da memória: "
              "não é uma Verdade segunda, é a Verdade LIDA PELO NOME (`nameOp`). Por isso a pedra é um ADENDO (padrão `PostoAdendo`): `Verdade` fica INTACTA, dois módulos não se chamam igual, e «Verdade» sozinha para as três foi recusada pela gerência e o operador concordou. "
              "O adendo entrega: (i) ★ `{est}` [REAL, novo e pequeno]: em M2(C), `diagExpect (identityProj a) = diagonal ![q², a²]` — a esperança diagonal lê a projeção da identidade como os seus PESOS, sem hipótese sobre a (bandeira `{est_f}`); "
              "(ii) `{unc}` (bandeira `{unc_f}`): para a ∈ [0, 1] há a Verdade de a, o Nome de ρ* lê a projeção como diag(q², a²), PRESERVA O UM (traço 1 = ω(I)) e reler não acrescenta; "
              "(iii) `verdade_e_a_esperanca_condicional`: a conjunção por citação de `the_identity_is_the_truth` (v392) e `esperanca_condicional_e_nome` (v402). "
              "O cálculo (α = β/√e = {alpha} em runtime, um parâmetro e nunca um número no teorema) CONFERE em M2(C) nos {tp} pontos de teste: o Nome de ρ* lê a projeção como diag(q², a²) = a esperança diagonal, o traço segue {tr} e reler não acrescenta; em a = α os pesos (1 − α², α²) = ({q2}, {a2}) somam {ws}, "
              "o peso de dentro α² é menor que β (a Verdade guarda α², não β) e o posto 1 da projeção não persiste na esperança (det P = 0, det diag(q², α²) > 0); esses números são deste rito, não estão no kernel. "
              "[ONTO] A álgebra é o que a Verdade lê: o Nome é a Verdade lida pelo operador que lê (a leitura pela tripla espectral); o kernel prova as LIGAÇÕES, não uma igualdade de tipos. É leitura da gerência c1, ratificada pelo operador. "
              "[OPEN] O índice 1/β ({nidx} com o β de runtime) segue CONDICIONAL às duas hipóteses nomeadas da v402 (`hpp`, `hopt`) e nenhuma instância é construída; o caso III₁ fica [OPEN]. NÃO se prova que toda esperança condicional seja um Operador do Nome (a esperança do traço não é um `nameOp p`), "
              "nem que o Nome em dimensão geral seja `diagExpect` (só em M2(C) e só para ρ*).",
              h=d["sha"]["verdade_adendo"], n_a=d["n_g"]["verdade_adendo"], a0=_faixa(d["ft"]["verdade_adendo"], d["n_g"]["verdade_adendo"]), q_nome=q_nome, q_tri=q_tri, q_ok=q_ok, q_ren=q_ren, vsha=_sha_verdade(), o3=d["s402"]["esperanca"], est=d["est_t"]["verdade_adendo"].split(".")[-1], est_f=d["est_f"]["verdade_adendo"],
              unc=d["unc"]["verdade_adendo"].split(".")[-1], unc_f=g_flag(V, "verdade_adendo"), alpha=_p(av["alpha"], 12), tp=av["test_points"], tr=_pn(av["trace_after_name"], 3), q2=_p(av["q_squared_at_alpha"], 12), a2=_pe(av["alpha_squared"], 6), ws=_pn(av["weights_sum"], 3),
              nidx=_p(ev["name_index_one_over_beta"], 4))


def _bandeiras(V):
    """As bandeiras do gate (F8.1): [REAL] o codigo do proprio programa (ast) e o core do rito · [DERIVED] as tres literais passam a calculadas · [DECLARADO] GV-01, GV-03 e EV-12 da auditoria de 28/09/2026 · [OPEN] a independencia das 4 experimentais e os mocks de survey."""
    d = _d(V); g = d["g"]; fam = _fam_gate(); n_old = len(_esp()["qg_closure_v402_checks"])
    return _f("**As bandeiras do gate (F8.1) [REAL: o código do próprio programa (ast) e o core do rito, lidos a cada rito · DERIVED: as três bandeiras que eram literais passam a calculadas · DECLARADO: GV-01, GV-03 e EV-12 da auditoria de 28/09/2026 · OPEN: a independência das quatro experimentais e os mocks de survey]** "
              "(registro `bandeiras_do_gate_v403`; {nck} checagens, todas passaram): o gate do fechamento carrega {n_flags} bandeiras ({f0} formais, {f1} físicas e {f2} experimentais); a função do veredito (`evaluate_quantum_gravity_closure`) lê {n_ver} ({r0} + {r1} + {r2}) e as outras {n_inf} ({inf}) são informativas, fora do veredito. "
              "A errata de 13/10/2026 (v392) e o registro `f81_nao_fechada_v392` diziam: as {n_ver} calculadas e as {n_inf} restantes literais. Na v403 as três passam a CALCULADAS, fail-closed, das fontes que o programa já tinha: "
              "(i) `linearized_spin2_finite_face` lê a família ext_ls2_* do kernel ({ls2} bandeiras, o termo dLs2 de `prove_external_ladder`: hélice dupla, setor TT sem fantasma, duas polarizações, face finita), lida de `kernel_formalization` [decisão D22]; "
              "(ii) `protocol_pre_registered` lê a checagem «{prereg}» do rito V11 do piso dos vazios (uma checagem, True); "
              "(iii) `null_tests_passed_blind` lê o `all_verified` do teste nulo cego (`void_stacking_blind`), passado ao gate pelo novo argumento `blind_null`. "
              "O registro é fail-closed: se qualquer bandeira calculada vier False ou uma checagem falhar, ele RECUSA (all_verified False e veredito de recusa) e o conferidor para o rito. "
              "A sonda nova `ProbeBlindNullAbsent` (a {nsonda}ª checagem do gate: as {n_old} da v402 mais ela) mostra em runtime que sem o teste nulo cego a bandeira informativa fica False e o veredito do gate NÃO muda: a literal nunca entrou no veredito. "
              "Neste rito: {n_true} de {n_flags} bandeiras verdadeiras, {n_calc} calculadas, {n_lit} literais; a letra do veredito do gate é a da v402: o gate não se moveu [REAL]. "
              "[DECLARADO, não resolvido] As quatro bandeiras experimentais do feed V11 ({feed}) derivam de UM só booleano (o veredito do V11 ser NOT_FALSIFIED_POWERED: o veredito emitido implica as outras três; survey_mocks_passed é o split-null e o dist-check, sem mock de survey) [GV-03]; "
              "a F8.1 troca literais por medida, não independentiza o feed. O degrau experimental lê só o rito V11 do piso, unilateral, e o espaço de vereditos dele não tem FALSIFIED: o ΛCDM raso também o respeita [GV-01, DECLARADO pela auditoria]. "
              "NOT_FALSIFIED nunca é a palavra da creditação; isto não é teste: não acrescenta rito, dado nem desfecho.",
              nck=g["n_chk_reg"], n_flags=g["n_flags"], f0=fam[0], f1=fam[1], f2=fam[2], n_ver=g["n_ver"], r0=g["rv"][0], r1=g["rv"][1], r2=g["rv"][2], n_inf=g["n_flags"] - g["n_ver"], inf=", ".join("`%s`" % x for x in g["info"]), ls2=g["ls2"], prereg=_qd().DL.F81_ROTULO_PREREG,
              nsonda=g["n_chk"], n_old=n_old, n_true=g["n_true"], n_calc=g["n_calc"], n_lit=g["n_lit"], feed=", ".join("`%s`" % x for x in g["feed"]))


def _leitura_tripla(V):
    """A leitura [ONTO] pela tripla espectral de Connes e por Joao 14,6 (da gerencia c1, ratificada pelo operador), LIDA do registro cunhagens_v403."""
    d = _d(V); lt = _g(_core(), "cunhagens_v403", "extras", "leitura_tripla_27out") or {}
    assert lt and lt == _esp()["leitura_tripla_27out"] and "ONTO" in str(lt.get("estatuto")), "a leitura da tripla espectral nao e' a de ESPERADOS"
    return _f("**A leitura pela tripla espectral** [ONTO: leitura da gerência c1, ratificada pelo operador em 27/10/2026 (`{s_ok}`); não é termo de kernel · DECLARADO: a leitura que o operador ratificou foi a apresentada na sessão]: o Caminho — {c}; a Vida — {v}; a Verdade — {ve}; e {j}; {tri}.",
              s_ok=d["s_ok"], c=_sem_chaves(lt["caminho"]), v=_sem_chaves(lt["vida"]), ve=_sem_chaves(lt["verdade"]), j=_sem_chaves(lt["joao_14_6"]), tri=_sem_chaves(lt["triplo_inteiro"]))
