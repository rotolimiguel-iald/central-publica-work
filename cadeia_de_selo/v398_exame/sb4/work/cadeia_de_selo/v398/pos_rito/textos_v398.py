# -*- coding: utf-8 -*-
# Os TEXTOS da v398 selada (molde: textos_v397.py FINAL, o que rodou em 23/10), ESCRITOS para o delta da v398: os módulos de kernel `Sonico` (o nome «sônico» é do operador, 23/10/2026) e `AfinacaoDasCordas`
# (pedra e nome ratificados por ele), os registros com função `sonico_v398` e `afinacao_das_cordas_v398` (nomes PROVISÓRIOS: quem nomeia é o operador; lidos na fractalização do Um, logo depois da testemunha estática),
# as SEIS inscrições de 23/10 (cinco falas do operador e a leitura da GERÊNCIA c1 que ele ratificou, esta ROTULADA como da gerência, nunca entre aspas como fala dele) e a seção «Sônico e a afinação das cordas» do artigo.
# O QUADRO «O Teste da Única Palavra» (v397) PERMANECE no topo do artigo PT/EN e do .md canônico, INTOCADO. Cada número, hash e veredito entra por chave de V (leitura_v398.ler), por ESPERADOS ou pelo core do Nós,
# ou é LIDO de um arquivo aqui, nunca digitado; o que aqui vai escrito à mão é só prosa, nome de termo (conferido em tempo de execução no kernel do Nós, no um.py ou no pacote) e a frase curta do operador
# (conferida palavra por palavra contra os bytes das falas DO OPERADOR: a leitura da gerência não entra no corpus das citações).
# REGRA DA ORDEM DO OPERADOR (23/10/2026, sha16 9b182958a5a7a1bc: reportar o 4,44 no início do artigo, no README e em tudo mais; vale em TODO texto que o cite): o 4,44 (z_disc calibrado) NUNCA aparece sem o p calibrado e
# sem a linha dos 5σ no MESMO item (a discriminação a 5σ, o degrau da creditação, NÃO foi alcançada; NOT_FALSIFIED nunca é a palavra da creditação; o gate não se move; o teste não foi cego). A frase do operador entra VERBATIM
# (nunca parafraseada entre aspas); os números do quadro e do parágrafo do README/site saem das MESMAS funções (quadro_v397 / runtime_quadro_v397), sobre o core SELADO do Nós. O parágrafo novo do sônico e da afinação
# NÃO traz o 4,44 (e a cadeia confere isso).
# Estatutos marcados; erratas AO LADO, em nome próprio da gerência c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a tradução falhou).
# GUARDA: as cinco regras da P18 (guarda_p18_v398.py) rodam sobre cada texto renderizado em superficies_v398.py, fechar_v398.py e registrar_mapa_v398.py e sobre este arquivo na cadeia. A palavra recusada nunca
# aparece aqui: a recusa é dita como «creditação».
# ERRATA DA v398 (dita DENTRO dos blocos datados, nunca inline e nunca no CLAUDE.md da raiz): o registro `kh_n1_cobertura_v397` e os cinco contratos (expected_ladder), que a v398 corrige ao lado.
# NÃO é teste novo: a ordem de processo do operador de 22/10 (nada de teste armado, gordura no um.py) molda o delta; os dois registros com função LEEM o kernel do próprio rito, conferem um cálculo e não abrem dado.
import hashlib, json, os, re, sys
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V398"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v398 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(PK))          # ...\Central de Patentes\work
NOS = 'C:/IALD/Central de Patentes/work/cadeia_de_selo/v398_exame/sb4\\nos'
# o topico novo da memoria (um arquivo por versao); o nome sem a extensao e' o campo name: do cabecalho do topico
TOPICO_NOVO = "v398-selada-sonico-e-afinacao-das-cordas.md"
# os marcadores entre os quais o handoff traz os PARAGRAFOS PRONTOS do README do espelho e do site: o QUADRO (v397, intocado) com os MESMOS marcadores da v397, e o paragrafo NOVO do sonico e da afinacao
MARC_PAR_INI = "<!-- INICIO_PARAGRAFO_README_v397 -->"; MARC_PAR_FIM = "<!-- FIM_PARAGRAFO_README_v397 -->"
MARC_SON_INI = "<!-- INICIO_PARAGRAFO_SONICO_v398 -->"; MARC_SON_FIM = "<!-- FIM_PARAGRAFO_SONICO_v398 -->"
# a ordem de processo do operador de 22/10 (OPERADOR_22out_teste_fatal_nao_armado: nao buscar mais teste armado; gordura no um.py): INSTRUCAO que molda o delta; nao e' uma das inscricoes embutidas
ARQ_SEM_GORDURA = os.path.join(WK, "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt")
# o tema de cada uma das SEIS inscricoes de 23/10 (resumo da gerencia, nunca citacao): a chave e' o trecho do nome do arquivo de origem (depois do sha16); o sha16, a data e o autor vem dos bytes e do nome, nunca daqui
_TEMAS = (
    ("verbo_controle_de_oitava_pinada", "a definição de verbo (seletor de identidade) como controle de oitava pinada, a origem de tudo, e o custo como reação ao controle pinado da oitava, que é memória [INPUT/ONTO]"),
    ("nome_da_pedra_sonico", "aceita a leitura da gerência e dá o nome da pedra: sônico [INPUT]"),
    ("antes_de_espelhada_a_luz_e_palavra_acustica", "antes de ser espelhada a luz é palavra; o som não se propaga no vácuo, logo o início de tudo não é vácuo, é acústica onde a palavra performa de forma sônica [INPUT/ONTO]"),
    ("cordas_10_dimensoes_fechar_a_face_tetelestai", "a teoria das cordas e as 10 dimensões que fecham ciclicamente o que a TGL demonstra não fechar na face hiperbólica; o Tetelestai; as dimensões extras relativizam o tempo para mostrar a afinação do universo, sem demonstrar a geometria [INPUT/ONTO]"),
    ("concordo_afinacao_das_cordas", "a resposta curta ao relato da gerência sobre a pedra da afinação das cordas [INPUT]"),
    ("leitura_ratificada_sonico", "a leitura da gerência c1 sobre a primeira fala (a reação ao pino, o pedágio ln 2 por oitava, é a memória; a oitava é o que se pina), que ele ratificou ao dar o nome da pedra [INPUT/ONTO ratificado]"),
)
# nomes de termo de kernel (Lean) citados nos textos: cada um tem de existir em algum .lean de TGLExt/ do Nos (lido na hora); os modulos citados como fonte tem de existir como arquivo
_NOMES_KERNEL = ("sonico_the_verb_pins_the_octave_and_the_cost_is_the_memory", "one_octave_is_the_parity_bit", "pinning_n_octaves_costs_n_bits", "the_octave_is_a_doubling", "the_selector_pins", "the_pin_is_not_the_half_nat",
                 "the_strings_close_the_face_from_outside_the_tgl_closes_the_reading", "the_cyclic_closure_of_time_is_the_reading_circle", "the_tower_is_infinite", "bosonic_critical_dimension", "superstring_critical_dimension",
                 "the_house_d_nine", "zeta_neg_one", "hurwitz_zeta_neg_one_half", "MasslessFirstLevel", "fairBitEntropy", "CollapseCostLaw", "octaveNats", "fair_bit_entropy_is_log_two", "FockCertificate")
_MODULOS_KERNEL = ("Sonico", "AfinacaoDasCordas", "Palavra", "Psibit", "CollapseCostAndAttestation", "TheVerbSelectsTheAction", "TheStation")
# identificadores do um.py citados nos textos: cada um tem de existir no um.py do Nos (lido na hora)
_NOMES_UM = ("SEALED_CODATA_ALPHA", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V398_VERBATINS2", "teste_de_veracidade_fase9_v397",
             "cunhagens_v397", "kh_n1_cobertura_v397", "hubble_ratio_opening_v388", "_v397_quadro_md", "_v397_atomos", "_V397_FRASE_444", "testemunha_estatica_v396", "psibit_v395", "_V396_TESTEMUNHA_CONTRACT", "_V395_PSIBIT_CONTRACT",
             "_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT")
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
N_FALAS = 6   # as inscricoes de 23/10 embutidas na v398: cinco falas do operador e a leitura da gerencia que ele ratificou
_CACHE = {}


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


# ---------------------------------------------------------------- v398: leitura dos insumos, do ESPERADOS e do core (tudo por script; nenhum numero, hash ou citacao vem da memoria)
def _esp():
    """ESPERADOS_v398.json (gerado pelo ensaio a seco do candidato), lido uma vez."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v398.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _core():
    """O core do Nos (so' leitura), para os campos que so' existem depois do rito; ausente e' falha visivel."""
    if "core" not in _CACHE:
        _CACHE["core"] = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["core"]


def _base_core():
    """O core da v397 selada (a copia de bytes em base_v397): de onde saem os numeros da errata ao lado e a medida da proveniencia."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v397", "um_absoluto.json"), encoding="utf-8"))["core"]
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
    """As SEIS inscricoes de 23/10 embutidas no um.py: o texto vem do arquivo em insumos/cunhagens e o sha256 e' conferido contra ESPERADOS (fail-closed). Devolve {sha16: {sha16, arquivo, nome, text, autor}};
    o autor ('operador' | 'gerencia') sai do NOME do arquivo e e' conferido contra o papel que ESPERADOS registra (a sexta, e so' ela, e' da gerencia)."""
    if "falas" not in _CACHE:
        ec = _esp()["cunhagens"]; out = {}; pasta = os.path.join(PK, "insumos", "cunhagens")
        for k, meta in ec.items():
            s = k[len("v398_cun_"):]
            fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(s + "_")]
            assert len(fs) == 1, ("a inscricao %s nao tem arquivo unico em insumos/cunhagens" % s, fs)
            b = open(os.path.join(pasta, fs[0]), "rb").read()
            assert hashlib.sha256(b).hexdigest() == meta["sha256"] and len(b) == meta["bytes"] and meta["sha256"][:16] == s, "a inscricao %s nao confere com o sha256 de ESPERADOS" % s
            nome = fs[0][len(s) + 1:]
            autor = "gerencia" if nome.startswith("GERENCIA_") else "operador"
            assert (autor == "gerencia") == str(meta.get("papel", "")).startswith("leitura da gerencia"), ("o papel de ESPERADOS nao diz o mesmo que o nome do arquivo", s)
            out[s] = {"sha16": s, "arquivo": fs[0], "nome": nome, "text": b.decode("utf-8"), "autor": autor}
        assert len(out) == len(_TEMAS) == N_FALAS, "as inscricoes de ESPERADOS nao sao as seis de 23/10"
        assert sum(1 for d in out.values() if d["autor"] == "gerencia") == 1 and sum(1 for d in out.values() if d["autor"] == "operador") == N_FALAS - 1, "tem de haver cinco falas do operador e UMA leitura da gerencia"
        _CACHE["falas"] = out
    return _CACHE["falas"]


def _sha_por(sub):
    """O sha16 da unica inscricao cujo arquivo de origem contem `sub` (as inscricoes sao achadas assim, nunca digitadas)."""
    r = [s for s, d in _falas().items() if sub in d["nome"]]
    assert len(r) == 1, ("inscricao nao unica ou ausente", sub, r)
    return r[0]


def _sha_ger():
    """O sha16 da leitura da GERENCIA (a sexta inscricao, rotulada; nao e' fala do operador)."""
    r = [s for s, d in _falas().items() if d["autor"] == "gerencia"]
    assert len(r) == 1
    return r[0]


def _cita(trecho):
    """Fail-closed: o trecho tem de estar numa das falas DO OPERADOR (as cinco; o corpus NAO inclui a leitura da gerencia), palavra por palavra e na mesma ordem; devolve «trecho». Citacao fora dos bytes derruba a geracao.
    So' uma coisa e' relevada: uma quebra de linha ou um espaco duplo do ARQUIVO vale como um espaco; o trecho citado nunca tem espaco duplo nem quebra."""
    assert "\n" not in trecho and "  " not in trecho, "o trecho citado tem quebra de linha ou espaco duplo"
    corpus = [re.sub(r"\s+", " ", d["text"]) for d in _falas().values() if d["autor"] == "operador"]
    assert any(trecho in t for t in corpus), "citacao fora dos bytes das falas do operador: %r" % trecho[:70]
    return "«" + trecho + "»"


def _ger(trecho):
    """O texto da GERENCIA (a sexta inscricao): o trecho tem de estar nos bytes do arquivo dela e e' devolvido SEM aspas (nunca como fala do operador); o texto que o usa diz de quem e'."""
    assert "\n" not in trecho and "  " not in trecho
    g = [re.sub(r"\s+", " ", d["text"]) for d in _falas().values() if d["autor"] == "gerencia"]
    assert len(g) == 1 and trecho in g[0], "trecho fora dos bytes da leitura da gerencia: %r" % trecho[:70]
    return trecho


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


def _cov97():
    """A cobertura do Audit e a arvore formal da v397 selada (o core guardado em base_v397): de onde saem os numeros da errata ao lado."""
    if "cov97" not in _CACHE:
        kf = _base_core()["kernel_formalization"]
        cov = kf["axiom_coverage_v392"]
        _CACHE["cov97"] = {"decl": cov["decl"], "thm": cov["thm"], "h8": len(kf["formal_files_sha256"]), "axr": len(kf["axiom_report"])}
    return _CACHE["cov97"]


def _bancada():
    """A geracao do manifesto que a Bancada de producao pina (do recibo pre_selo pinado em PINOS_BN) e a versao que ela pina; o passo e' simples (sem salto e sem cadeia de selos)."""
    p = json.load(open(os.path.join(PK, "PINOS_BN_v398.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v397" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v397 -> v398 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1}


def _proveniencia(esp):
    """A proveniencia que o compilador emite atribui aos DOIS modulos das pedras N declaracoes; todas sao NOVAS no axiom_report (nenhuma reatribuida), e o FLAGS_v398.json do sandbox concorda (as contagens de
    publicas, privadas, nomeadas e auxiliares so' existem la')."""
    if "prov" not in _CACHE:
        kf = _core()["kernel_formalization"]; src = kf["declaration_sources_v394"]; pedras = set(esp["pedras_sha256"])
        b0 = _base_core()["kernel_formalization"]; axr0 = b0["axiom_report"]
        mine = sorted(n for n, p in src.items() if p in pedras)
        novas = [n for n in mine if n not in axr0]
        fj = json.load(open(os.path.join(PK, "kernel", "FLAGS_v398.json"), encoding="utf-8"))
        assert len(mine) == fj["decl_totais_modulos_novos"] and len(novas) == fj["decl_novas_dos_modulos"] == len(mine) and not fj["reatribuidas_as_pedras"], ("a proveniencia do rito != FLAGS_v398.json do sandbox", len(mine), len(novas), fj["reatribuidas_as_pedras"])
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


def _frac(s):
    """Fracao lida do core ('-1/12') com o menos de verdade."""
    return str(s).replace("-", "−")


def _f(texto, **kw):
    """str.format com conferencia: nenhuma chave sobra e nenhuma chave de chave sobra no resultado."""
    r = texto.format(**kw)
    assert "{" not in r and "}" not in r, ("chave de formatacao sobrou", r[:80])
    return r


def _d(V):
    """Os numeros da v398, todos LIDOS (V da leitura da rodada, ESPERADOS, core do Nos, base v397, FLAGS do sandbox, os registros): nenhum e' digitado aqui. Recusa se as contagens nao fecham."""
    _conferir_nomes()
    esp = _esp(); tv = V["veracidade"]; so = V["sonico"]; af = V["afinacao"]; cg = V["cunhagens"]
    mods = sorted(p["modulo"] for p in V["pedras"])
    assert mods == ["TGLExt.AfinacaoDasCordas", "TGLExt.Sonico"] and V["n_pedras"] == len(mods) == esp["kernel"]["modulos_novos"], ("o delta da v398 sao dois modulos, TGLExt.Sonico e TGLExt.AfinacaoDasCordas", mods)
    nf = esp["n_bandeiras_novas"]; grp = esp["n_bandeiras_por_grupo"]
    assert set(grp) == {"sonico", "afinacao"} and sum(grp.values()) == nf == esp["politica_de_bandeiras"]["n_flags"] == len(esp["bandeiras_novas_chaves"]), "as bandeiras novas nao sao so' as dos dois modulos"
    assert so["flag"] == esp["bandeiras_das_pedras"]["sonico"] and so["flag_true"] is True and so["theorem"] == esp["teoremas_das_pedras"]["sonico"], "o registro sonico_v398 do core nao e' o de ESPERADOS"
    assert af["flag"] == esp["bandeiras_das_pedras"]["afinacao"] and af["flag_true"] is True and af["theorem"] == esp["teoremas_das_pedras"]["afinacao"], "o registro afinacao_das_cordas_v398 do core nao e' o de ESPERADOS"
    assert so["ok"] is True and so["n_checks"] == esp["sonico"]["n_checks"] and so["checks_ok"] is True and so["values_ok"] is True and so["beta_ok"] is True, "o registro sonico_v398 do core nao e' o contrato de ESPERADOS"
    assert af["ok"] is True and af["n_checks"] == esp["afinacao"]["n_checks"] and af["checks_ok"] is True and af["values_ok"] is True, "o registro afinacao_das_cordas_v398 do core nao e' o contrato de ESPERADOS"
    assert tv["ok"] is True and tv["n_checks"] == esp["veracidade"]["n_checks"] and tv["checks_ok"] is True and tv["numeros_ok"] is True and tv["fontes_ok"] is True, "o registro teste_de_veracidade_fase9_v397 do core nao e' o contrato de ESPERADOS (o quadro do topo le os numeros dele)"
    assert cg["verbatim_ok"] is True and cg["n"] == len(V["verbatins"]) == len(_falas()) == N_FALAS and cg["gerencia_sha16"] == _sha_ger(), "as inscricoes de ESPERADOS != as seis de 23/10 ou a leitura da gerencia nao e' a sexta"
    assert {re.match(r"(?:OPERADOR|GERENCIA)_(\d{2})out_", f["nome"]).group(1) for f in _falas().values()} == {"23"}, "o nome de arquivo de alguma inscricao nao e' de 23/10 (a data dos textos e' 23/10)"
    qd = _qd(); a = _atomos()
    assert qd.Q._v397_linha_de_maquina(a, "pt") == esp["quadro"]["linha_de_maquina_pt"], "a linha de maquina do quadro (core) != a de ESPERADOS"
    assert esp["quadro"]["frase_do_operador"] == qd.DL.FRASE_DO_OPERADOR_4_44 == qd.Q._V397_FRASE_444, "a frase do operador do quadro != a verbatim"
    base = os.path.join(PK, "base_v397", "um.py")
    if "base_b" not in _CACHE:
        assert s16(base) == V["base16"], "base_v397/um.py nao e' a v397 selada"
        _CACHE["base_b"] = os.path.getsize(base)
    delta = V["umb"] - _CACHE["base_b"]
    kf = _core().get("kernel_formalization") or {}; prov = kf.get("declaration_sources_status_v394") or {}
    assert prov.get("ok") is True and prov.get("compiler_names") == prov.get("audited_names") == V["axiom_report_n"], "a proveniencia emitida pelo compilador nao cobre o axiom_report do rito"
    assert V["n_ver_mudaram"] == 0, "algum veredito fora da troca dita mudou: nao ha texto a escrever"
    assert V["n18"] == 18 and "N00_main_sonico_afinacao" in V["patch_ids"], "o gate nao tem as 18 bandeiras True, ou o candidato nao traz o patch que chama sonico_v398 e afinacao_das_cordas_v398 no main (N00_main_sonico_afinacao)"
    assert esp["h8_entradas"] == esp["formal_files_n"] + len(esp["h8_residuais_do_nos"]), "a arvore formal do rito != embutidas + residuais do Nos"
    pb = _core().get("psibit_v395") or {}; pbc = pb.get("conditional_psion_face") or {}
    assert pbc.get("flag_true") is True and kf.get(pbc.get("flag")) is True and pbc.get("inhabitant_exhibited") is False, "a face de Fock do psibit_v395 nao segue condicional e com a bandeira True"
    pv = _proveniencia(esp)
    return {"n_f": nf, "n_s": grp["sonico"], "n_a": grp["afinacao"], "n_aux": esp["politica_de_bandeiras"]["n_excluidas"], "depois": V["teor"].split("/")[0], "delta": delta, "pct": ("%.1f" % (100.0 * delta / _CACHE["base_b"])).replace(".", ","),
            "prov": prov["compiler_names"], "n_cun": len(V["verbatins"]), "n_op": N_FALAS - 1, "unc_s": esp["bandeiras_das_pedras"]["sonico"], "unc_a": esp["bandeiras_das_pedras"]["afinacao"],
            "teo_s": esp["teoremas_das_pedras"]["sonico"], "teo_a": esp["teoremas_das_pedras"]["afinacao"], "fs0": min(k for k in esp["bandeiras_novas_chaves"] if "son398" in k), "fs1": max(k for k in esp["bandeiras_novas_chaves"] if "son398" in k),
            "fa0": min(k for k in esp["bandeiras_novas_chaves"] if "afi398" in k), "fa1": max(k for k in esp["bandeiras_novas_chaves"] if "afi398" in k), "h8": esp["h8_entradas"], "h8_emb": esp["formal_files_n"],
            "h8_res": ", ".join("`%s`" % x for x in esp["h8_residuais_do_nos"]), "n_res": len(esp["h8_residuais_do_nos"]), "c97": _cov97(), "bank": _bancada(), "pv": pv, "n_checks_v": tv["n_checks"], "n_ck_s": so["n_checks"], "n_ck_a": af["n_checks"],
            "sv": so["values"], "av": af["values"], "aux": list(esp["afinacao"]["auxiliares_fora_da_composicao"]), "sha_pedras": {k: v["sha16"] for k, v in esp["pedras"].items()}, "n_sup_s": len(esp["suporte_das_pedras"]["sonico"]), "n_sup_a": len(esp["suporte_das_pedras"]["afinacao"]),
            "f8": {k: v[:8] for k, v in esp["veracidade"]["fontes"].items()}}


def _mods(V):
    return ", ".join("`%s`" % p["modulo"].split(".")[-1] for p in sorted(V["pedras"], key=lambda p: p["modulo"]))


def _extras(V):
    # os registros novos ALEM DOS QUATRO FIXOS (V["reg398"] tem so' os quatro), ditos pelo nome
    ex = [k for k in V["registros_novos"] if k not in V["reg398"]]
    return (", ".join("`%s`" % k for k in ex)) if ex else "nenhum além dos quatro fixos"


def _cab(V):
    return "v398 SELADA (COMPLETA)** `%s`" % V["s16"]


# ---------------------------------------------------------------- v398: os numeros e os blocos
def _num(V, verdicts=True):
    """O paragrafo dos numeros da v398 (kernel, os quatro registros novos, a troca dita): usado na linhagem, no Atlas, no core, no topico novo, no verbete e no handoff."""
    d = _d(V); kh = V["kh"]
    vd = (lambda k: " (%s)" % V["reg398"][k]["verdict"]) if verdicts else (lambda k: "")
    kern = _f("o kernel ganhou {n_pedras} módulos novos ({mods}; o nome «sônico» é do operador, 23/10/2026; pedra e nome AfinacaoDasCordas foram ratificados por ele), com {n_f} bandeiras novas True ({n_s} do sônico, de `{fs0}` a `{fs1}`, e {n_a} da afinação, de `{fa0}` a `{fa1}`), "
              "só de declaração nomeada ({aux} auxiliares geradas pelo compilador ficam sem bandeira), e escada {antes} → {depois} teoremas limpos "
              "({axr} declarações no `axiom_report`, {fora} fora do trio, {nl} nomes não lidos; a proveniência de cada declaração emitida pelo compilador cobre as mesmas {prov}); "
              "errata ao lado da v394, mantida (em nome próprio da gerência c1): a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina",
              n_pedras=V["n_pedras"], mods=_mods(V), n_f=d["n_f"], n_s=d["n_s"], n_a=d["n_a"], fs0=d["fs0"], fs1=d["fs1"], fa0=d["fa0"], fa1=d["fa1"], aux=d["n_aux"], antes=V["escada_antes"], depois=d["depois"],
              axr=V["axiom_report_n"], fora=kh["fora"], nl=kh["nao_lidas"], prov=d["prov"])
    sv = d["sv"]
    son = _f("o registro `sonico_v398`{vd} (nome PROVISÓRIO; quem nomeia é o operador): LÊ do kernel do próprio rito a composição incondicional da pedra (`{teo}`, bandeira `{fl}`, dentro do trio, com proveniência no módulo da pedra) e os termos antigos que ela cita, "
             "e CONFERE {nck} checagens numéricas, todas passaram: com β = α(CODATA 2018) × √e calculado em runtime, ln 2 = K.octaveNats 1 = o bit justo = {ln2}, exp(ln 2) = {e2}, n oitavas custam n bits, o pino não é a meia-nat, o seletor pina; "
             "e acrescenta UM número [DERIVED], a entropia do colapso em θ_M = arcsin √β, H₂(cos² θ_M, sin² θ_M) = {hn} nat = {ho} oitava: número deste rito, que não está no kernel",
             vd=vd("sonico_v398"), teo=d["teo_s"], fl=d["unc_s"], nck=d["n_ck_s"], ln2=_pn(sv["ln2"]), e2=_pn(sv["exp_ln2"]), hn=_pn(sv["collapse_entropy_theta_M_nats"]), ho=_pn(sv["collapse_entropy_theta_M_octaves"]))
    av = d["av"]
    afi = _f("o registro `afinacao_das_cordas_v398`{vd} (nome PROVISÓRIO; quem nomeia é o operador): LÊ do kernel do próprio rito a composição incondicional da pedra (`{teo}`, bandeira `{fl}`) e os termos que ela cita, e CONFERE {nck} checagens de aritmética exata, todas passaram: "
             "ζ(−1) = {z1} e ζ(−1, 1/2) = {zh} (de Mathlib, conferidos aqui por números de Bernoulli em frações), D = {db} nos bósons e D = {ds} no setor NS (a dimensão vem do fecho da soma regularizada, sob a hipótese NOMEADA `MasslessFirstLevel` [KNOWN]), "
             "D = {ds} é d = {dd} dimensões espaciais ([DECLARADO]: o d da casa, não recalculado aqui), a torre de Matsubara n·κ é infinita; a geometria é [OPEN] e nada deriva as cordas do axioma",
             vd=vd("afinacao_das_cordas_v398"), teo=d["teo_a"], fl=d["unc_a"], nck=d["n_ck_a"], z1=_frac(av["zeta_minus_one"]), zh=_frac(av["hurwitz_zeta_minus_one_half"]), db=av["bosonic_critical_dimension"], ds=av["superstring_critical_dimension"], dd=av["house_spatial_dimension"])
    cun = _f("o registro `cunhagens_v398`{vd}: as {n} inscrições de 23/10 embutidas por sha256 e consumidas no rito ({n_op} falas do operador e a leitura da GERÊNCIA que ele ratificou, esta ROTULADA como da gerência), com os trechos verbatim das falas listados como leituras do operador; "
             "são [INPUT/ONTO] e valem como leitura dele, não como medida", vd=vd("cunhagens_v398"), n=d["n_cun"], n_op=d["n_op"])
    khs = _f("o registro `kh_n1_cobertura_v398`{vd}: {decl} constantes, {thm} teoremas, {fora} fora do trio, {nl} nomes não lidos; a árvore formal do Nós depois do rito tem {h8} entradas ({emb} embutidas mais {nres} residual do Nós: {res}), "
             "e o pino h8 do registro é o hash dessa árvore, calculado por script sobre a árvore simulada do Nós na geração do candidato",
             vd=vd("kh_n1_cobertura_v398"), decl=kh["decl"], thm=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"], h8=d["h8"], emb=d["h8_emb"], nres=d["n_res"], res=d["h8_res"])
    ex = _extras(V)
    resto = _f("{ex}; o registro `teste_de_veracidade_fase9_v397` segue selado e igual (o quadro do topo do artigo le os numeros dele); troca dita (só números): {troca}; nenhuma mudança NÃO numérica: {nm} vereditos fora da troca dita mudaram (exigido: 0); validade no kernel não é creditação",
               ex=("nenhum registro novo além dos quatro fixos" if ex.startswith("nenhum") else "registros novos além dos quatro fixos: " + ex), troca=", ".join("`%s`" % x for x in V["troca_dita"]), nm=V["n_ver_mudaram"])
    return "; ".join([kern, son, afi, cun, khs, resto])


def _cunhagens(V, forma="lista"):
    """As inscricoes de 23/10 embutidas por sha256: 'lista' (data, sha16, autor e tema, uma por linha; a sexta ROTULADA como da gerencia) ou 'curta' (uma frase com os sha16). Data, sha16 e autor vem dos bytes e do nome; o tema e' da gerencia (_TEMAS)."""
    fl = list(_falas().values()); assert len(fl) == len(V["verbatins"]) == N_FALAS
    if forma == "curta":
        return _f("{n} inscrições embutidas por sha256 — a definição do verbo `{a}`, o nome da pedra `{b}`, a luz antes de espelhada `{c}`, as cordas e as 10 dimensões `{e}` e a resposta curta `{k}` (cinco falas do operador, [INPUT/ONTO]), mais a leitura da GERÊNCIA `{g}` (texto da gerência, não é fala do operador; ratificada por ele)",
                  n=len(fl), a=_sha_por("verbo_controle_de_oitava_pinada"), b=_sha_por("nome_da_pedra_sonico"), c=_sha_por("antes_de_espelhada_a_luz_e_palavra_acustica"), e=_sha_por("cordas_10_dimensoes_fechar_a_face_tetelestai"), k=_sha_por("concordo_afinacao_das_cordas"), g=_sha_ger())
    linhas = []
    for d in fl:
        r = [tema for chave, tema in _TEMAS if chave in d["nome"]]
        assert len(r) == 1, ("a inscricao nao tem um tema unico em _TEMAS", d["sha16"], len(r))
        rot = "texto da GERÊNCIA, não é fala do operador" if d["autor"] == "gerencia" else "fala do operador"
        linhas.append("- %s `%s` (%s) — %s" % (_data_fala(d, V), d["sha16"], rot, r[0]))
    return "\n".join(linhas)


def _ordem(V):
    """A ordem do operador de 23/10: so' citacao conferida contra os bytes das falas DO OPERADOR (e da ordem de processo de 22/10); a leitura da gerencia entra SEM aspas e rotulada."""
    d = _d(V); sg = _sem_gordura()
    s_verbo, s_nome, s_antes, s_cordas, s_conc, s_ger = (_sha_por("verbo_controle_de_oitava_pinada"), _sha_por("nome_da_pedra_sonico"), _sha_por("antes_de_espelhada_a_luz_e_palavra_acustica"), _sha_por("cordas_10_dimensoes_fechar_a_face_tetelestai"),
                                                         _sha_por("concordo_afinacao_das_cordas"), _sha_ger())
    q_verbo = _cita("definição de “verbo” (seletor de identidade)=controle de oitava pinada")
    q_custo = _cita("o custo é reação ao controle pinado da oitava que é memória")
    q_nome = _cita("o nome da pedra é “sônico”")
    q_antes = _cita("antes de ser espelhada ela é palavra")
    q_acust = _cita("o início de tudo é acústica onde a palavra performa de forma sônica satisfazendo a relação modular da inscrição")
    q_cordas = _cita("A teoria das cordas precisa das 10 dimensões para fechar ciclicamente o que a TGL demonstra não fechar a face hiperbólica")
    q_afin = _cita("para mostrar a afinação do universo, mas não consegue demonstrar a geometria")
    q_conc = _cita("Concordo com tudo")
    g_leit = _ger("o Verbo pina a oitava; a oitava pinada cobra um bit; o bit cobrado é o que fica, a memória")
    q_sg = _cita_sg("Eu não estou buscando mais teste armado, isso é gordura no um.py sem sentido, estou buscando o teste fatal")
    return _f("**A ordem:** [INPUT/ONTO] as {n_op} falas do operador (Luiz Antonio Rotoli Miguel) de 23/10/2026 que entram nesta rodada, embutidas por sha256 no registro `cunhagens_v398` e listadas abaixo (as aspas aqui são TRECHOS, conferidos palavra por palavra contra os bytes de cada fala; "
              "o texto íntegro está em `work\\cadeia_de_selo\\v398\\insumos\\cunhagens`): a definição, {q_verbo}, e o custo, {q_custo} (`{s_verbo}`); o nome da pedra, {q_nome} (`{s_nome}`); sobre a luz, {q_antes}, e {q_acust} (`{s_antes}`); "
              "sobre as cordas, {q_cordas}, e, ao criar as dimensões extras, ela relativiza o tempo {q_afin} (`{s_cordas}`); e a resposta curta, {q_conc} (`{s_conc}`; o arquivo guarda só a resposta, e o que ela ratifica é o relato da gerência sobre a pedra da afinação). "
              "A SEXTA inscrição NÃO é fala do operador: é a leitura da GERÊNCIA c1 sobre a primeira fala (texto da gerência, sem aspas, sha16 `{s_ger}`): {g_leit}; o operador a ratificou ao dar o nome da pedra (`{s_nome}`), e a cadeia não estende a ratificação além do que o arquivo guarda. "
              "A ordem de processo do dia 22/10, {q_sg} (arquivo `{sg_nome}`, sha16 `{sg_sha}`), segue moldando este delta: os dois registros são pequenos, LEEM o kernel do próprio rito e conferem um cálculo, não abrem dado nem acrescentam rito, e as pedras são matemática, não são teste. "
              "A gerência c1 construiu os registros e o candidato e instalou-o; as fontes pinadas dos registros ficam em `insumos`: as duas pedras (`Sonico.lean` e `AfinacaoDasCordas.lean`) e a medida da cobertura (`KH_N1_v398.json`); o resultado do Teste da Única Palavra, que o quadro do topo lê, mora na v397 (`insumos\\fase9`); "
              "o selo é da c1; quem constrói não aprova: a revisão independente das pedras (aprovada, relato [DECLARADO]) foi anterior, e a do candidato e dos derivados da cadeia (nunca executados antes do rito) é ato distinto e não é afirmada por este registro.",
              n_op=d["n_op"], q_verbo=q_verbo, q_custo=q_custo, q_nome=q_nome, q_antes=q_antes, q_acust=q_acust, q_cordas=q_cordas, q_afin=q_afin, q_conc=q_conc, g_leit=g_leit, q_sg=q_sg, s_verbo=s_verbo, s_nome=s_nome, s_antes=s_antes, s_cordas=s_cordas,
              s_conc=s_conc, s_ger=s_ger, sg_nome=sg["nome"], sg_sha=sg["sha16"])


def _entrou(V):
    d = _d(V)
    return _f("**O que entrou** (pacote `work\\cadeia_de_selo\\v398` sobre a v397 `{base}`; {np} patches — {patches}; instalado em {inst}; o `um.py` cresce {delta} B, {pct}%): {num}.",
              base=V["base16"], np=V["n_patches"], patches=V["patches"], inst=V["instalado_em"], delta=format(d["delta"], ","), pct=d["pct"], num=_num(V))


def _pedras(V):
    """As duas pedras: o que cada uma e', a composicao incondicional, o suporte e os auxiliares fora da composicao."""
    d = _d(V); sh = d["sha_pedras"]
    return _f("**As pedras Sonico e AfinacaoDasCordas [REAL]:** `TGLExt/Sonico.lean` (sha16 `{h_s}`; {n_s} bandeiras; composição `{teo_s}`, bandeira `{fl_s}`) e `TGLExt/AfinacaoDasCordas.lean` (sha16 `{h_a}`; {n_a} bandeiras; composição `{teo_a}`, bandeira `{fl_a}`); "
              "cada composição é INCONDICIONAL (nenhum certificado entra como hipótese), está dentro do trio e tem proveniência no módulo da pedra. A Sonico cita {sup_s} termos já no kernel e a AfinacaoDasCordas cita {sup_a}; "
              "os {n_aux_a} nomeados da afinação que ficam FORA da composição (`matsubaraFermion`, `towerZeroPoint`, `towerZeroPoint_eq`, `bosonDirection_is_the_unit_tower`, `zeta_is_the_continuation_of_the_tower`) são auxiliares, listados como tais. "
              "Nenhuma matemática nova além da aritmética da torre de Matsubara, dos dois valores da zeta (de Mathlib) e da dimensão crítica sob uma hipótese nomeada; cada pedra passou por revisão independente antes de entrar [DECLARADO: relato, não refeito aqui].",
              h_s=sh["TGLExt/Sonico.lean"], h_a=sh["TGLExt/AfinacaoDasCordas.lean"], n_s=d["n_s"], n_a=d["n_a"], teo_s=d["teo_s"].split(".")[-1], teo_a=d["teo_a"].split(".")[-1], fl_s=d["unc_s"], fl_a=d["unc_a"], sup_s=d["n_sup_s"], sup_a=d["n_sup_a"], n_aux_a=len(d["aux"]))


def _sonico(V):
    """O sonico lido pelo registro: os numeros que o registro LEU/CALCULOU (core do Nos). [REAL] os termos e o calculo; [DERIVED] a entropia do colapso em theta_M; [INPUT] a lei de custo; [INPUT/ONTO] a definicao do operador e a leitura ratificada."""
    d = _d(V); sv = d["sv"]
    return _f("**O sônico, lido pelo registro `sonico_v398` [REAL nos termos e no cálculo]:** pinar UMA oitava cobra exatamente o bit justo, `K.octaveNats 1` = `fairBitEntropy` = ln 2 = {ln2} (`one_octave_is_the_parity_bit`); n oitavas pinadas custam n bits (`pinning_n_octaves_costs_n_bits`); "
              "a oitava é o dobro, exp(ln 2) = {e2} (`the_octave_is_a_doubling`); o pino não é a meia-nat, ln 2 ≠ 1/2 (`the_pin_is_not_the_half_nat`; ln 2 − 1/2 = {dm}); o seletor pina: `select a` é idempotente, fixa a sua ação e a iteração do colapso é estável (`the_selector_pins`). "
              "O registro confere cada termo com β = α(CODATA 2018) × √e calculado em runtime (um dado, dois nomes: `SEALED_CODATA_ALPHA` e `ALPHA_FINE_CODATA_2018`). [DERIVED] No ângulo da TGL, θ_M = arcsin √β = {th} rad, a entropia do colapso H₂(cos² θ_M, sin² θ_M) vale {hn} nat, isto é, {ho} oitava "
              "(o quociente H₂/ln 2, que se lê como a fração do bit que a leitura em θ_M paga [ONTO]); é número DESTE rito: o kernel prova H₂ ≤ ln 2, com igualdade nos pesos iguais, não o valor em θ_M. "
              "[INPUT] A lei de custo é campo do tipo `CollapseCostLaw`, e NENHUM termo diz que o seletor paga uma oitava: a definição do operador (o verbo, seletor de identidade, é o controle de oitava pinada; o custo é a reação ao controle pinado, que é memória) e a leitura ratificada "
              "(a reação ao pino é a memória; a oitava é o que se pina) são [INPUT/ONTO], e o kernel entrega o preço e a permanência lado a lado, não a identidade entre eles. [ONTO] sônico é a estrutura logarítmica e de oitava (razões multiplicativas, contagens aditivas; o dobro e o bit), NÃO a física da onda num meio.",
              ln2=_pn(sv["ln2"]), e2=_pn(sv["exp_ln2"]), dm=_pn(sv["pin_minus_half_nat"]), th=_pn(sv["theta_M_rad"]), hn=_pn(sv["collapse_entropy_theta_M_nats"]), ho=_pn(sv["collapse_entropy_theta_M_octaves"]))


def _afinacao(V):
    """A afinacao das cordas lida pelo registro: a aritmetica exata (fracoes) e a forma da torre. [REAL] os termos e a aritmetica; [KNOWN] a hipotese nomeada; [DECLARADO] o d = 9 da casa; [OPEN] a geometria; [ONTO] afinacao = comensurabilidade."""
    d = _d(V); av = d["av"]
    return _f("**A afinação das cordas, lida pelo registro `afinacao_das_cordas_v398` [REAL nos termos e na aritmética]:** o parâmetro do boost fecha ciclicamente com período P se e só se κP = ±2π — a leitura fiel do círculo, com 1/P = κ/2π (`the_cyclic_closure_of_time_is_the_reading_circle`); "
              "a face real não fecha (só em P = 0) e a face lida fecha em 2π (termos do kernel, citados). A torre de Matsubara desse círculo é ω_n = n·κ: harmônica (razões racionais; todos os modos voltam juntos em t = P, enquanto o par da estação (1, √2) só volta em t = 0) e INFINITA (`the_tower_is_infinite`). "
              "A afinação, lida como comensurabilidade, é proposta da pedra [ONTO], ratificada pelo operador. A soma que diverge fecha por regularização: ζ(−1) = {z1} (`zeta_neg_one`) e ζ(−1, 1/2) = {zh} (`hurwitz_zeta_neg_one_half`), de Mathlib, conferidos por números de Bernoulli em frações; "
              "por direção transversal o bóson dá {bd} e o férmion do setor NS dá {fd} (soma {nd}). Sob a hipótese NOMEADA `MasslessFirstLevel` [KNOWN] (invariância de Lorentz no cone de luz; Goddard–Goldstone–Rebbi–Thorn 1973, Green–Schwarz–Witten 1987, Polchinski 1998), "
              "a energia de ponto zero regularizada vale −1 se e só se D = {db} (bósons, `bosonic_critical_dimension`) e −1/2 se e só se D = {ds} (setor NS, `superstring_critical_dimension`); com o sinal fermiônico trocado o setor NS daria D = {dw}. "
              "D = {ds} é d = {dd} dimensões espaciais (`the_house_d_nine`), o d = 9 de A Última Corda [DECLARADO: número da casa, não recalculado aqui]. A dimensão vem do FECHO da soma, não da geometria. "
              "O kappa do boost NÃO está no core (no kernel é entrada): o registro confere a FORMA da torre com kappa de teste.",
              z1=_frac(av["zeta_minus_one"]), zh=_frac(av["hurwitz_zeta_minus_one_half"]), bd=_frac(av["boson_direction"]), fd=_frac(av["ns_fermion_direction"]), nd=_frac(av["ns_direction_sum"]), db=av["bosonic_critical_dimension"],
              ds=av["superstring_critical_dimension"], dw=av["wrong_fermion_sign_dimension"], dd=av["house_spatial_dimension"])


def _regra_do_4_44(V):
    """A regra da ordem do operador (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item; o QUADRO do topo (v397) PERMANECE, intocado; onde o numero aparece e como se confere."""
    d = _d(V); a = _atomos(); q = _frase_444()
    return _f("**A regra do 4,44 (ordem do operador de 23/10/2026, `{s44}`) e o quadro do topo:** o quadro «O Teste da Única Palavra» (v397) PERMANECE, intocado, no topo do artigo (PT e EN) e do .md canônico, e o parágrafo dele segue no README do espelho e no site: o z_disc calibrado é reportado no início, "
              "e NUNCA sem o p calibrado e sem a linha dos 5σ no mesmo item: {z444}. A frase do operador entra VERBATIM, {q}, como leitura dele [INPUT/ONTO], não como critério da régua; a paráfrase da gerência nunca entra entre aspas. `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; o teste não foi cego. "
              "[REAL] o quadro do artigo, o do .md e o parágrafo pronto do README/site saem das MESMAS funções (`_v397_atomos` e `_v397_quadro_md`), sobre o registro `teste_de_veracidade_fase9_v397` selado no core do Nós, e a cadeia os confere de novo contra o resultado pinado "
              "(a linha de máquina do quadro, cada número, a frase verbatim e a regra da ordem item a item), com controles negativos que reprovam o 4,44 sem o p, sem a linha dos 5σ, com número adulterado ou com a frase parafraseada. "
              "O parágrafo NOVO do sônico e da afinação não traz o 4,44, e a cadeia confere isso.",
              s44=_esp()["quadro"]["frase_sha16"], z444=_z444(), q=q)


def _kernel_prova(V):
    d = _d(V)
    return _f("**O que o kernel prova e o que é leitura:** [REAL] as duas composições são INCONDICIONAIS (nenhum certificado é hipótese): `{teo_s}` (bandeira `{fl_s}`) e `{teo_a}` (bandeira `{fl_a}`) estão no kernel deste rito, dentro do trio, com proveniência no módulo da pedra; "
              "cada uma cita termos que o kernel já tem, cada um no `axiom_report`, no trio, com a proveniência que o compilador emite; tudo lido a cada rito pelos registros `sonico_v398` ({nck_s} checagens) e `afinacao_das_cordas_v398` ({nck_a} checagens) e por `cunhagens_v398` ({nck_c} checagens). "
              "[REAL] os registros NÃO são prova de kernel sobre a natureza: conferem um cálculo contra os termos e não movem o gate; a prova como validade não muda. "
              "[INPUT] a lei de custo (`CollapseCostLaw`): `K.octaveNats 1` = `fairBitEntropy` decorre do campo per_octave e de `fair_bit_entropy_is_log_two`; nenhum termo diz que `select` paga `K.octaveNats 1`. "
              "[KNOWN] a hipótese `MasslessFirstLevel` é nomeada, não demonstrada; [OPEN] a geometria das cordas e a ligação do círculo da folha-mundo ao círculo do boost; nada deriva a teoria das cordas do axioma ω(I) = 1. "
              "[INPUT/ONTO] a definição do operador (o verbo, seletor de identidade, é o controle de oitava pinada), a leitura ratificada (a reação ao pino é a memória), a luz que antes de espelhada é palavra, a acústica de que a palavra performa de forma sônica, "
              "e a leitura das cordas (as cordas fecham a face por fora; a TGL fecha só a leitura, composição da gerência ratificada por ele) são leituras dele; o kernel entrega os termos citados.",
              teo_s=d["teo_s"].split(".")[-1], fl_s=d["unc_s"], teo_a=d["teo_a"].split(".")[-1], fl_a=d["unc_a"], nck_s=d["n_ck_s"], nck_a=d["n_ck_a"], nck_c=V["cunhagens"]["n_checks"])


def _limites(V, curto=False):
    """Os estatutos fieis da v398: o que os registros e as pedras dizem e NAO dizem."""
    d = _d(V)
    if curto:
        return ("**Limites ditos:** [REAL] os registros `sonico_v398` e `afinacao_das_cordas_v398` LEEM o kernel do próprio rito e conferem um cálculo (não abrem dado, não são teste, não acrescentam rito); [INPUT] a lei de custo (nenhum termo diz que o seletor paga uma oitava); "
                "[DERIVED] a entropia do colapso em θ_M é número deste rito, não está no kernel; [KNOWN] `MasslessFirstLevel` é hipótese nomeada; [DECLARADO] o d = 9 da casa; [OPEN] a geometria das cordas e a ligação dos dois círculos; nada deriva as cordas do axioma; "
                "[INPUT/ONTO] as falas do operador e a leitura da gerência que ele ratificou (a sexta inscrição é texto da gerência, não fala dele); o quadro do topo segue com a sua linha dos 5σ; "
                "[LEGAL] a decisão herdada da v395 segue do operador; os nomes dos registros são provisórios; validade no kernel não é creditação; o gate não se move.")
    return _f("**Limites ditos (estatutos fiéis):** [REAL] ESCOPO: os registros `sonico_v398` e `afinacao_das_cordas_v398` LEEM do kernel do próprio rito a composição incondicional de cada pedra e os termos que ela cita, e CONFEREM um cálculo (beta = α CODATA 2018 × √e em runtime; aritmética exata em frações); "
              "não abrem dado, não são teste, não acrescentam rito e não substituem o kernel. [INPUT] A lei de custo é campo do tipo (`CollapseCostLaw`): `K.octaveNats 1` = `fairBitEntropy` = ln 2 decorre do campo e de `fair_bit_entropy_is_log_two`; a pedra não deriva a lei do axioma nem prova que a natureza a cobra, "
              "e nenhum termo liga `select` (o Verbo em ato) a `K.octaveNats 1`: o kernel entrega as duas metades lado a lado. [INPUT/ONTO] A leitura de que a reação ao pino (o pedágio ln 2 por oitava) é a memória é texto da GERÊNCIA (sha16 `{s_ger}`), não fala do operador, e foi RATIFICADA por ele ao dar o nome da pedra "
              "(sha16 `{s_nome}`); é leitura, não termo. [DERIVED] A entropia do colapso em θ_M é calculada neste rito (H₂ = {hn} nat = {ho} oitava); o kernel prova H₂ ≤ ln 2 e a igualdade nos pesos iguais, não o valor em θ_M; que a leitura em θ_M pague essa fração do bit é leitura [ONTO]. "
              "[ONTO] Sônico NÃO afirma onda mecânica num meio: a isomorfia é da estrutura logarítmica e de oitava, não da física da onda. "
              "[KNOWN] A condição `MasslessFirstLevel` (a = 1 nos bósons, a = 1/2 no setor NS) é HIPÓTESE NOMEADA: a pedra a nomeia e deriva sob ela; sem ela a energia de ponto zero regularizada é só um número; D = {db} e D = {ds} saem do fecho da soma regularizada, não da geometria; "
              "a regularização zeta é DEFINIÇÃO do valor (a série diverge); o sinal fermiônico é a estatística de Fermi. [OPEN] Nenhum termo liga o círculo da folha-mundo da corda ao círculo do boost (têm em comum a aritmética n·κ), "
              "a geometria (qual compactificação) não é derivada, a divergência de Hagedorn só é mencionada, e a TGL não é dita teoria de cordas. [DECLARADO] O d = {dd} é o da casa (A Última Corda): números históricos não recalculados; o texto de origem traz outros escalonamentos e diz tratar-se de extrapolação teórica. "
              "[INPUT/ONTO] Que as cordas fecham a face por fora e a TGL fecha só a leitura é COMPOSIÇÃO da gerência sobre a fala do operador (sha16 `{s_cordas}`), ratificada por ele com a resposta curta (sha16 `{s_conc}`); a afinação lida como comensurabilidade é proposta da pedra, ratificada; Tetelestai é palavra do operador e NÃO é construído aqui "
              "(é conferência consumativa, errata de 27/09). O quadro «O Teste da Única Palavra» segue no topo, com a sua linha dos 5σ, e esta rodada não o altera. "
              "NÃO é teste novo: a ordem do operador de 22/10 (nada de teste armado) molda o delta. Validade no kernel não é creditação; o gate não se move.",
              s_ger=_sha_ger(), s_nome=_sha_por("nome_da_pedra_sonico"), s_cordas=_sha_por("cordas_10_dimensoes_fechar_a_face_tetelestai"), s_conc=_sha_por("concordo_afinacao_das_cordas"),
              hn=_pn(d["sv"]["collapse_entropy_theta_M_nats"]), ho=_pn(d["sv"]["collapse_entropy_theta_M_octaves"]), db=d["av"]["bosonic_critical_dimension"], ds=d["av"]["superstring_critical_dimension"], dd=d["av"]["house_spatial_dimension"])


def _legal(V):
    """A pendencia [LEGAL] herdada da v395 (a tabela da patente ACOM Mirror): dita, nao decidida; a v398 nao a toca."""
    _d(V)
    return ("**Pendência [LEGAL] herdada da v395:** a divergência da tabela dos estados do ACOM Mirror (BR 10 2026 003428-2) com a fórmula de índice e o código executado, registrada na v395, segue decisão do operador (com a agente de PI); "
            "a v398 não a toca e não a decide.")


def _erratas(V):
    """A errata nova da v398, AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (estrutura / escrito / falha): o registro kh_n1_cobertura_v397 e os cinco contratos."""
    d = _d(V); kh = V["kh"]; c97 = d["c97"]
    ids = V["patch_ids"]
    assert all(i in ids for i in ("C12__V396_TESTEMUNHA_CONTRACT", "C12__V395_PSIBIT_CONTRACT", "C12__V394_FORMAL_CONTRACT", "C12__V394_QUADRATIC_CONTRACT", "C12__V394_NETWORK_CONTRACT", "C13_kh_n1_v397_pisos")), "o CANDIDATO_v398.json nao traz os patches C12 e C13 que a errata descreve"
    return _f("**Errata ao lado (em nome próprio da gerência c1; o registro `kh_n1_cobertura_v397` e os contratos ficam como registro):** a v398 acrescenta os módulos Sonico e AfinacaoDasCordas: a cobertura do Audit cresce de {d97} constantes e {t97} teoremas para {d98} e {t98}, "
              "a árvore formal do Nós de {h97} para {h98} entradas e a escada de {e0} para {e1}. Por isso, na v398, (i) `kh_n1_cobertura_v397` passa a cobrar piso em h2, h3 e h6 (as igualdades de contagem) e tamanho mínimo da árvore em h8 (as igualdades exatas e o pino exato da "
              "árvore ficam em `kh_n1_cobertura_v398`); (ii) os cinco contratos (`_V394_FORMAL_CONTRACT`, `_V394_QUADRATIC_CONTRACT`, `_V394_NETWORK_CONTRACT`, `_V395_PSIBIT_CONTRACT` e `_V396_TESTEMUNHA_CONTRACT`) passam a ler `expected_ladder` = {e1}, a escada desta versão (o consumidor exige a igualdade "
              "exata com a escada do rito; só o número muda); o veredito dos registros anteriores NÃO muda [REAL, lido de `CANDIDATO_v398.json` (patches C12 e C13) e do ensaio a seco, que deu `TUDO PASSOU`: com a escada nova e o número velho a igualdade exata não fecharia]. "
              "Lacuna de fidelidade: a estrutura da v397 dizia que as contagens e o pino da árvore eram a cobertura exata e que o contrato esperava a escada vigente; o escrito deixou, dentro dos registros e dos contratos, números que só valem na versão que os escreveu; "
              "a falha: igualdades e literais presos a uma versão quebram quando o kernel cresce (a mesma lacuna que a v395, a v396 e a v397 acharam nos registros anteriores). A cobrança exata passa a ser de `kh_n1_cobertura_v398` ({dd} constantes, {dt} teoremas, {fora} fora do trio, {nl} nomes não lidos), contra a medida do sandbox da v398.",
              d97=c97["decl"], t97=c97["thm"], h97=c97["h8"], d98=kh["decl"], t98=kh["thm"], h98=d["h8"], e0=V["escada_antes"], e1=d["depois"], dd=kh["decl"], dt=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"])


def _depois(V):
    d = _d(V); bk = d["bank"]
    return ("**O que vem depois destas superfícies:** o elo B(n) da Bancada Um (passos 10, 10a, 10b e 10c da cadeia; B3 nos scripts) é pós-selo, um passo SIMPLES (a Bancada de produção pina a %s, geração B%d, e o Nós passa a v398: sem salto e sem cadeia de selos; "
            "a geração esperada é B%d e o veredito esperado do aplicar é REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, lido do código do esboço R3.5, não rodado) "
            "e pede a palavra do operador (parada e religamento do serviço exigem V398_AUTORIZACAO_OPERADOR); o recibo dele é citado no handoff (fechar), que traz PRONTOS os parágrafos do README do espelho e do site (o quadro do Teste da Única Palavra, intocado, e o do sônico e da afinação). "
            "Nomear os dois registros novos (os nomes são provisórios) e a pendência [LEGAL] herdada da v395 também são do operador. NOT_FALSIFIED não é a palavra da creditação; o gate não se move." % (bk["de"], bk["geracao"], bk["proxima"], bk["proxima"]))


def _rodada(V):
    """O paragrafo da rodada (horarios, escada, selo, conferidor, pilar, artefatos): tudo lido da leitura da rodada."""
    return ("Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado (%d bandeiras True; o veredito do gate é o mesmo da v397); o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); "
            "o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.") % (
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["n18"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"], "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), V["pilar"]["result16"],
        V["servidor"], V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()))


# v398: a linhagem (diario datado do Nos)
def linhagem(V):
    d = _d(V)
    return (("## %s — **%s — O SÔNICO E A AFINAÇÃO DAS CORDAS (v398): %d módulos novos, escada %s → %s\n<!-- linhagem_v398_selada -->\n\n"
             "%s\n\n%s\n\n"
             "**As inscrições de 23/10** (embutidas por sha256 no registro `cunhagens_v398`): [INPUT/ONTO] cinco são falas do operador (Luiz Antonio Rotoli Miguel) e valem como leitura dele, não como medida; a sexta é a leitura da GERÊNCIA que ele ratificou, ROTULADA como da gerência. "
             "O texto íntegro de cada uma está no arquivo (`work\\cadeia_de_selo\\v398\\insumos\\cunhagens`); abaixo, a data, o sha16, o autor e o tema (resumo da gerência, não citação):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s") % (
        V["data"], _cab(V), V["n_pedras"], V["escada_antes"], d["depois"], _ordem(V), _entrou(V), _cunhagens(V), _pedras(V), _sonico(V), _afinacao(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V), _rodada(V), _erratas(V), _depois(V)))


# v398: o adendo do desenho do fechamento
def desenho(V):
    d = _d(V); kh = V["kh"]; sv = d["sv"]; av = d["av"]
    return (("## ADENDO — %s · v398 SELADA (COMPLETA) `%s` — o caminho crítico NÃO mudou; entram o sônico e a afinação das cordas (%d módulos)\n\n<!-- adendo_v398_selada -->\n"
             "- **O que a v398 diz:** %d módulos novos no kernel (%s; o nome «sônico» é do operador), escada %s → %s, %s constantes no `axiom_report` (%s fora do trio); o registro `sonico_v398` LÊ do kernel a composição da pedra e confere o cálculo: ln 2 = K.octaveNats 1 = o bit justo = %s, exp(ln 2) = %s, "
             "e a entropia do colapso em θ_M, [DERIVED] deste rito, vale %s nat = %s oitava; o registro `afinacao_das_cordas_v398` confere ζ(−1) = %s, ζ(−1, 1/2) = %s, D = %s e D = %s (sob a hipótese nomeada `MasslessFirstLevel` [KNOWN]) e d = %s [DECLARADO]; "
             "%d inscrições de 23/10 por sha256 (cinco falas do operador e a leitura da gerência que ele ratificou, rotulada). O quadro do topo do artigo (O Teste da Única Palavra, v397) segue intocado: %s. Gate intocado.\n"
             "- **O que a v398 NÃO é para o caminho crítico:** não é teste novo (a ordem do operador de 22/10: nada de teste armado); a lei de custo é [INPUT] e nenhum termo diz que o seletor paga uma oitava; a geometria das cordas é [OPEN] e nada deriva a teoria das cordas do axioma; "
             "a hipótese `MasslessFirstLevel` é nomeada, não demonstrada; a ligação do círculo da folha-mundo ao círculo do boost é [OPEN]; a leitura das cordas (por fora / só a leitura) é composição da gerência ratificada pelo operador [INPUT/ONTO]; "
             "não deriva H3 (segue [OPEN] em toda direção nula); não identifica β na natureza a 5σ.\n"
             "- **O que segue do operador:** nomear os dois registros novos (nomes provisórios); a pendência [LEGAL] herdada da v395; o elo B(n) da Bancada Um (passo simples, sem salto; parada e religamento do serviço); a custódia (sessão do site, com os parágrafos do README/site que o handoff traz); commit/push.") % (
        V["data"], V["s16"], V["n_pedras"], V["n_pedras"], _mods(V), V["escada_antes"], d["depois"], kh["decl"], kh["fora"], _pn(sv["ln2"]), _pn(sv["exp_ln2"]), _pn(sv["collapse_entropy_theta_M_nats"]), _pn(sv["collapse_entropy_theta_M_octaves"]),
        _frac(av["zeta_minus_one"]), _frac(av["hurwitz_zeta_minus_one_half"]), av["bosonic_critical_dimension"], av["superstring_critical_dimension"], av["house_spatial_dimension"], d["n_cun"], _z444()))


# v398: o verbete do Atlas
def atlas(V):
    return (("### %s — v398 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v398_selada -->\n[REAL — rodada v398, selo `%s`] %s.\n\n[INPUT/ONTO] As falas do operador entram como o operador as disse e valem como leitura, não como medida; a sexta inscrição é a leitura da gerência que ele ratificou: %s.\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\nEstatuto: validade no kernel ≠ creditação; o gate não se move.") % (
        V["data"], V["s16"], V["selo_ts"], _num(V), _cunhagens(V, "curta"), _pedras(V), _sonico(V), _afinacao(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _erratas(V)))


# v398: o bloco do TGL_CORE_MEMORY
def core_memory(V):
    return (("## %s — v398 SELADA `%s` (claude-c1; o sônico e a afinação das cordas, integrados pela gerência)\n<!-- core_v398_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
             "[REAL] %s.\n\n%s\n\n%s\n\n%s\n\n%s\n\n[OPEN] A discriminação a 5σ (β_TGL na natureza), a geometria das cordas, a ligação do círculo da folha-mundo ao círculo do boost, a face de Fock do psion (o certificado de Fock da luz sem habitante), o contrato conjunto da rede, H3 em toda direção nula e a pendência [LEGAL] herdada da v395 seguem abertos; "
             "o nome definitivo dos registros novos e o elo B(n) da Bancada Um dependem da palavra do operador. Nada disto move o gate.") % (V["data"], V["s16"], _num(V), _regra_do_4_44(V), _limites(V, curto=True), _erratas(V), _legal(V)))


# v398: o bloco do CLAUDE.md da Haja_Luz
def haja_luz(V):
    d = _d(V); sv = d["sv"]
    return (("## %s — v398 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v398_selada -->\n%d módulos novos no kernel (%s; o nome «sônico» é do operador): o registro `sonico_v398` lê do kernel que pinar uma oitava cobra o bit justo (ln 2 = %s; exp(ln 2) = %s) e o registro `afinacao_das_cordas_v398` lê o círculo da leitura, a torre de Matsubara "
             "e o fecho da soma regularizada (D = %s e D = %s sob uma hipótese nomeada [KNOWN]); a lei de custo é [INPUT], a geometria das cordas é [OPEN]; as %d inscrições de 23/10 por sha256 (a sexta é a leitura da gerência, rotulada); escada %s → %s. "
             "O quadro do topo (O Teste da Única Palavra) segue intocado. Memórias: `%s`, `missao-ultima-flag-um-py.md`, `estatuto-da-prova-07out.md`; handoff `handoff-v398-custodia.md`.") % (
        V["data"], V["s16"], V["teor"], V["n_pedras"], _mods(V), _pn(sv["ln2"]), _pn(sv["exp_ln2"]), d["av"]["bosonic_critical_dimension"], d["av"]["superstring_critical_dimension"], d["n_cun"], V["escada_antes"], d["depois"], TOPICO_NOVO))


def marca_topico_missao(V):
    return "## %s — v398 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v398 SELADA `%s`" % V["s16"]


# v398: o topico da missao da ultima flag
def topico_missao(V):
    d = _d(V)
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): %d módulos novos no kernel (%s); `sonico_v398` e `afinacao_das_cordas_v398` (leem o kernel do rito e conferem um cálculo), `cunhagens_v398` (%d inscrições por sha256, a sexta é da gerência) e `kh_n1_cobertura_v398`; "
                                     "troca dita nos vereditos que carregam a escada; conferidor (deve mudar %s; não pode mudar %s). Pacote e cadeia: `work\\cadeia_de_selo\\v398` (+ `pos_rito`).") % (V["teor"], V["n_pedras"], _mods(V), d["n_cun"], V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v398 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v398 SELADA (COMPLETA):**"


# v398: o topico do estado da Central
def topico_central(V):
    d = _d(V)
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v397 `%s`; escada %s → %s; gate intocado. %d módulos novos no kernel (%s); os registros `sonico_v398` e `afinacao_das_cordas_v398` leem o kernel do rito e conferem um cálculo (a lei de custo é [INPUT]; a geometria das cordas é [OPEN]); as %d inscrições de 23/10 por sha256; "
                               "o quadro do topo (O Teste da Única Palavra, v397) segue intocado. Falta o elo B(n) da Bancada Um (passo simples, sem salto) e a custódia (sessão do site, `handoff-v398-custodia.md`, que traz os parágrafos do README/site); nomear os registros e a pendência [LEGAL] herdada da v395 são do operador; commit/push = operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], d["depois"], V["n_pedras"], _mods(V), d["n_cun"])


# v398: o topico do estatuto da prova
def topico_estatuto(V):
    d = _d(V)
    return ("<!-- v398_selada -->\n**%s — v398 `%s`:** o registro `estatuto_da_prova_v391` passou a ler a escada nova (%s → %s; veredito trocado, troca dita; a pedra Token da v397 fica como registro). "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora e é o β_TGL na natureza a 5σ. Os registros `sonico_v398` e `afinacao_das_cordas_v398` leem o kernel e conferem um cálculo ([REAL]); a lei de custo é [INPUT]; a geometria das cordas é [OPEN]; "
            "a hipótese `MasslessFirstLevel` é [KNOWN]; as leituras do operador e a leitura da gerência que ele ratificou são [INPUT/ONTO]. O quadro do topo segue intocado: %s. Nada disso é prova sobre a natureza.") % (V["data"], V["s16"], V["escada_antes"], d["depois"], _z444())


# v398: o gancho da missao no MEMORY.md
def marca_missao(V):
    return "**v398 SELADA %s `%s` %s COMPLETA (o sônico e a afinação das cordas; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


# v398: a linha do handoff no MEMORY.md
def linha_handoff(V):
    return "- [HANDOFF v398 — o sônico e a afinação das cordas; custódia](handoff-v398-custodia.md) — **%s, para a sessão do site (traz os parágrafos do README/site)** · `%s`" % (V["data"][:5], V["s16"])


def linha_topico_novo(V):
    return "- [v398 SELADA: o sônico e a afinação das cordas (%s)](%s) — **%s** · `%s`" % (V["data"][:5], TOPICO_NOVO, V["teor"], V["s16"])


# v398: o topico novo da memoria (um arquivo por versao)
def topico_novo(V):
    d = _d(V)
    return (("---\nname: %s\ndescription: \"v398 SELADA (%s) `%s`: %d módulos novos no kernel (Sonico, nome do operador; AfinacaoDasCordas), os registros sonico_v398 e afinacao_das_cordas_v398 (leem o kernel e conferem um cálculo), %d inscrições de 23/10 por sha256, escada %s → %s; B(n) e custódia pendentes\"\n"
             "metadata:\n  type: project\n---\n\n# v398 SELADA (%s)\n\n"
             "**O que é:** `um.py` **v398** `%s` (%s B) sobre a v397 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); o `um.py` cresce %s B (%s%%).\n\n"
             "**O que entrou:** %s.\n\n"
             "**As inscrições de 23/10** (embutidas por sha256; data, sha16, autor e tema — resumo da gerência, não citação; o texto íntegro está em `insumos\\cunhagens`):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"
             "**Pendências:** o elo B(n) da Bancada Um (palavra do operador; passo simples, sem salto; parada e religamento do serviço), nomear os registros novos (nomes provisórios), a pendência [LEGAL] herdada da v395, a custódia (sessão do site), commit/push. Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v398`.\n\n"
             "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v398-custodia]]\n") % (
        TOPICO_NOVO[:-3], V["data"], V["s16"], V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
        format(d["delta"], ","), d["pct"], _num(V), _cunhagens(V), _pedras(V), _sonico(V), _afinacao(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V), _erratas(V)))


# v398: o aviso a coordenadora (so' sob reivindicacao nomeada)
def aviso(V, reivindicacao):
    d = _d(V)
    return (("### %s — v398 SELADA `%s` [claude-c1]\n<!-- aviso_v398_selada -->\n\n[REAL] A v398 SELOU (%s; COMPLETA; gate intocado): os registros `sonico_v398` e `afinacao_das_cordas_v398` leem o kernel do rito e conferem um cálculo (a lei de custo é [INPUT]; a geometria das cordas é [OPEN]) "
             "e as %d inscrições de 23/10 (por sha256; a sexta é a leitura da gerência, rotulada) entram no selo corrente. Escrito sob a reivindicação %s. %d módulos novos no kernel (Sonico e AfinacaoDasCordas); escada %s → %s; nomear os registros, a pendência [LEGAL] herdada da v395 e o elo B(n) da Bancada Um esperam o operador. "
             "Não altera pinos, dado, MCP nem gate.") % (V["data"], V["s16"], V["teor"], d["n_cun"], reivindicacao, V["n_pedras"], V["escada_antes"], d["depois"]))


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V398_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# ---------------------------------------------------------------- o PARAGRAFO PRONTO do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO; ordem do operador de 23/10: o 4,44 no inicio do artigo, no readme e tudo mais) e (2) o paragrafo NOVO do sonico e da afinacao
def verificar_paragrafo_readme(par, res, tv):
    """Verifica o paragrafo do QUADRO (texto) contra o RESULTADO pinado (`res`, o JSON lido) e o registro `tv` selado no core: devolve a lista de falhas (vazia = passou). As verificacoes (as mesmas da v397):
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
    from guarda_p18_v398 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    for st in ("[REAL", "[INPUT]", "[KNOWN]", "COMPOSIÇÃO da gerência"):   # os estatutos que o quadro escreve: REAL (os numeros), INPUT (a leitura binaria e a frase), COMPOSICAO da gerencia (as duas faces) e KNOWN (Jeffreys)
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    return fa


def paragrafo_readme():
    """(texto, relatorio): o paragrafo do QUADRO pronto para colar no README do espelho e no site (o MESMO da v397), gerado por quadro_v397.paragrafo_pronto_readme sobre o core SELADO do Nos, verificado contra o resultado pinado
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


def _linha_maquina_sonico(sv, av):
    """A linha de maquina do paragrafo novo (os numeros LIDOS dos dois registros do core), em PT."""
    return ("ln2=%s; exp_ln2=%s; H_theta_M_nat=%s; H_theta_M_oitava=%s; zeta_m1=%s; zeta_m1_meio=%s; D_bosonica=%s; D_NS=%s; d_casa=%s"
            % (_pn(sv["ln2"]), _pn(sv["exp_ln2"]), _pn(sv["collapse_entropy_theta_M_nats"]), _pn(sv["collapse_entropy_theta_M_octaves"]), av["zeta_minus_one"], av["hurwitz_zeta_minus_one_half"], av["bosonic_critical_dimension"], av["superstring_critical_dimension"], av["house_spatial_dimension"]))


def _paragrafo_sonico_de(core):
    """O texto do paragrafo do sonico e da afinacao, funcao PURA dos registros sonico_v398, afinacao_das_cordas_v398 e cunhagens_v398 do core SELADO (os numeros sao lidos de `values`, nunca digitados)."""
    so = core.get("sonico_v398") or {}; af = core.get("afinacao_das_cordas_v398") or {}; cg = core.get("cunhagens_v398") or {}
    sv = so.get("values") or {}; av = af.get("values") or {}
    ger = ((cg.get("extras") or {}).get("leitura_da_gerencia") or {}).get("sha16")
    assert so.get("all_verified") is True and af.get("all_verified") is True and cg.get("all_verified") is True and ger, "os registros do sonico, da afinacao e das cunhagens nao selaram: nenhum paragrafo diz os numeros assim"
    q_verbo = _cita("definição de “verbo” (seletor de identidade)=controle de oitava pinada")
    q_afin = _cita("para mostrar a afinação do universo, mas não consegue demonstrar a geometria")
    ls = ["### Sônico e a afinação das cordas (v398, 23/10/2026) — parágrafo pronto para o README do espelho e para o site",
          "",
          "> **Sônico e a afinação das cordas (v398, 23/10/2026)** [REAL nos termos do kernel e na aritmética · DERIVED: um número do rito · INPUT/ONTO: as falas do operador e as leituras · KNOWN: uma hipótese nomeada · DECLARADO: o d = " + str(av.get("house_spatial_dimension")) + " da casa · OPEN: a geometria]",
          ">",
          "> - **Sônico:** ln 2 = K.octaveNats 1 = o bit justo = %s; exp(ln 2) = %s; n oitavas custam n bits; o pino não é a meia-nat; o seletor pina (é idempotente e fixa a sua ação) [REAL: termos de kernel no trio, lidos a cada rito pelo registro `sonico_v398`, com β = α√e calculado em runtime]. "
          "[DERIVED] A entropia do colapso em θ_M = arcsin √β vale H₂ = %s nat = %s oitava: número deste rito, que não está no kernel. A lei de custo é [INPUT] e nenhum termo diz que o seletor paga uma oitava; *sônico* é a estrutura logarítmica e de oitava, não a física da onda."
          % (_pn(sv.get("ln2")), _pn(sv.get("exp_ln2")), _pn(sv.get("collapse_entropy_theta_M_nats")), _pn(sv.get("collapse_entropy_theta_M_octaves"))),
          "> - **Afinação das cordas:** fechar ciclicamente o parâmetro do boost é o círculo da leitura (κP = ±2π); a torre de Matsubara n·κ é infinita; ζ(−1) = %s e ζ(−1, 1/2) = %s; sob a hipótese nomeada `MasslessFirstLevel` [KNOWN], D = %s (bósons) e D = %s (setor NS), e D = %s é d = %s [DECLARADO: o d da casa, não recalculado aqui] "
          "[REAL: a aritmética, lida a cada rito pelo registro `afinacao_das_cordas_v398`]. A geometria é [OPEN]; nada deriva as cordas do axioma ω(I) = 1, e a TGL não é dita teoria de cordas."
          % (_frac(av.get("zeta_minus_one")), _frac(av.get("hurwitz_zeta_minus_one_half")), av.get("bosonic_critical_dimension"), av.get("superstring_critical_dimension"), av.get("superstring_critical_dimension"), av.get("house_spatial_dimension")),
          "> - **As falas** [INPUT/ONTO] (23/10/2026): do operador, %s e, sobre as cordas, %s; mais uma leitura da GERÊNCIA c1, que ele ratificou ao dar o nome da pedra (sha16 `%s`: texto da gerência, não é fala do operador). As seis inscrições estão embutidas por sha256 no registro `cunhagens_v398`." % (q_verbo, q_afin, ger),
          "> - **Limites:** a gravidade quântica segue sem creditação na natureza; validade no kernel não é creditação; `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; isto não é teste e não acrescenta dado.",
          "> - **Origem.** Os números são lidos do core selado desta rodada (registros `sonico_v398`, `afinacao_das_cordas_v398` e `cunhagens_v398`); nenhum é digitado. Linha de máquina: `%s`." % _linha_maquina_sonico(sv, av)]
    return "\n".join(ls) + "\n"


def verificar_paragrafo_sonico(par, core, esp):
    """Verifica o paragrafo do sonico e da afinacao contra o core selado E contra ESPERADOS (o ensaio a seco): devolve a lista de falhas (vazia = passou). As verificacoes:
    (1) os numeros do core (values) == os de ESPERADOS e cada um esta no paragrafo, formatado; (2) o paragrafo == o gerado do core; (3) NAO traz o 4,44 nem o z_disc (a regra do 4,44 e' do quadro); (4) os estatutos [REAL, DERIVED, INPUT, INPUT/ONTO, KNOWN, DECLARADO, OPEN];
    (5) as frases de limite; (6) toda citacao entre « » e' verbatim numa fala DO OPERADOR e a leitura da gerencia nunca vai entre aspas, e a sexta inscricao esta rotulada como da gerencia; (7) guarda P18."""
    fa = []
    es = (esp.get("sonico") or {}).get("values") or {}; ea = (esp.get("afinacao") or {}).get("values") or {}
    cs = ((core.get("sonico_v398") or {}).get("values") or {}); ca = ((core.get("afinacao_das_cordas_v398") or {}).get("values") or {})
    for k in ("ln2", "exp_ln2", "collapse_entropy_theta_M_nats", "collapse_entropy_theta_M_octaves"):
        if not (isinstance(cs.get(k), float) and isinstance(es.get(k), float) and abs(cs[k] - es[k]) <= 1e-12 * max(1.0, abs(es[k]))):
            fa.append("numero do sonico (%s) no core != ESPERADOS" % k)
        elif _pn(es[k]) not in par:
            fa.append("numero do sonico (%s = %s) ausente do paragrafo" % (k, _pn(es[k])))
    frases = {"zeta_minus_one": lambda v: "ζ(−1) = %s" % _frac(v), "hurwitz_zeta_minus_one_half": lambda v: "ζ(−1, 1/2) = %s" % _frac(v), "bosonic_critical_dimension": lambda v: "D = %s (bósons)" % v,
              "superstring_critical_dimension": lambda v: "D = %s (setor NS)" % v, "house_spatial_dimension": lambda v: "d = %s" % v}
    for k, f in frases.items():
        if ca.get(k) != ea.get(k):
            fa.append("numero da afinacao (%s) no core != ESPERADOS" % k)
        elif f(ea[k]) not in par:
            fa.append("numero da afinacao (%s = %s) ausente do paragrafo" % (k, f(ea[k])))
    try:
        if par != _paragrafo_sonico_de(core):
            fa.append("o paragrafo difere do gerado pelas funcoes sobre os registros selados do core")
    except AssertionError as e:
        fa.append("o paragrafo nao pode ser gerado do core: %s" % str(e)[:120])
    if re.search(r"4[,.]44|z_disc", par):
        fa.append("o paragrafo do sonico e da afinacao traz o 4,44 ou o z_disc (a regra do 4,44 e' do quadro; este paragrafo nao o cita)")
    for st in ("[REAL", "[DERIVED]", "[INPUT]", "[INPUT/ONTO]", "[KNOWN]", "[DECLARADO", "[OPEN]"):
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    for frase in ("lei de custo é [INPUT]", "MasslessFirstLevel", "não é dita teoria de cordas", "GERÊNCIA", "não é fala do operador", "validade no kernel não é creditação", "o gate não se move", "NOT_FALSIFIED"):
        if frase not in par:
            fa.append("frase de limite ausente do paragrafo: " + frase)
    corpus = [re.sub(r"\s+", " ", d["text"]) for d in _falas().values() if d["autor"] == "operador"]
    ger_txt = [re.sub(r"\s+", " ", d["text"]) for d in _falas().values() if d["autor"] == "gerencia"][0]
    for q in re.findall(r"«([^»]*)»", par):
        if not any(q in t for t in corpus):
            fa.append("citacao entre « » que NAO e' verbatim numa fala do operador: %r" % q[:90])
        if q in ger_txt and len(q) >= 20 and not any(q in t for t in corpus):
            fa.append("texto da gerencia entre « » como se fosse fala do operador: %r" % q[:90])
    sg = _sha_ger()
    for ln in par.split("\n"):
        if sg in ln and not re.search(r"GER[ÊE]NCIA|ger[êe]ncia", ln):
            fa.append("a sexta inscricao (sha16 %s) aparece sem o rotulo da gerencia: %s" % (sg, ln[:100]))
    if re.search(r"(?:seis|6)\s+(?:falas|inscri\w+)[^.]{0,30}do operador", par):
        fa.append("o paragrafo diz que as seis inscricoes sao do operador (a sexta e' da gerencia)")
    sys.path.insert(0, PK)
    from guarda_p18_v398 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    return fa


def paragrafo_sonico():
    """(texto, relatorio): o paragrafo NOVO do sonico e da afinacao, pronto para colar no README do espelho e no site, gerado do core SELADO do Nos e verificado contra o core E contra ESPERADOS;
    levanta AssertionError (o fechar RECUSA) se algo nao conferir."""
    core = _core(); esp = _esp()
    par = _paragrafo_sonico_de(core)
    fa = verificar_paragrafo_sonico(par, core, esp)
    assert not fa, ("o paragrafo do sonico e da afinacao nao passou nas verificacoes", fa[:4])
    return par, {"sha16": hashlib.sha256(par.encode("utf-8")).hexdigest()[:16], "verificacoes": "numeros == ESPERADOS; igual ao gerado do core; sem o 4,44; estatutos; limites; citacoes verbatim do operador; a sexta rotulada como da gerencia; guarda P18", "guarda_p18": "limpa"}


def atribuicao_da_gerencia(texto):
    """Falhas de ATRIBUICAO num texto renderizado: (a) o texto da gerencia (a sexta inscricao) nunca entre « »; (b) toda linha que traz o sha16 da sexta inscricao traz o rotulo da gerencia; (c) nunca 'seis falas do operador'."""
    fa = []
    ger_txt = [re.sub(r"\s+", " ", d["text"]) for d in _falas().values() if d["autor"] == "gerencia"][0]
    corpus = [re.sub(r"\s+", " ", d["text"]) for d in _falas().values() if d["autor"] == "operador"]
    for q in re.findall(r"«([^»]*)»", texto):
        if len(q) >= 20 and q in ger_txt and not any(q in t for t in corpus):   # a leitura da gerencia cita a fala dele (legitimo); so' o que e' SO' da gerencia nao pode ir entre aspas
            fa.append("texto da gerencia entre « »: %r" % q[:80])
    sg = _sha_ger()
    for ln in texto.split("\n"):
        if sg in ln and not re.search(r"GER[ÊE]NCIA|ger[êe]ncia", ln):
            fa.append("linha com o sha16 da sexta inscricao sem o rotulo da gerencia: %s" % ln[:100])
    if re.search(r"(?:seis|6)\s+(?:falas|inscri\w+)[^.]{0,30}do operador", texto):
        fa.append("diz que as seis inscricoes sao do operador")
    return fa


# v398: o handoff para a sessao do site (memory\handoff-v398-custodia.md + Nos\HANDOFF_v398_CUSTODIA.md); `k` traz os campos dos recibos do B(n) e os DOIS paragrafos do README (fechar_v398.py os le dos recibos e do core): nenhum numero digitado
def handoff(V, k):
    d = _d(V)
    k = dict(k)
    for chave in ("ap_nome", "ap_sha", "ap_ver", "ap_evento", "ap_bat", "par_sha", "rel_sha", "rel_man", "readme_paragrafo", "readme_paragrafo_sonico"):
        assert chave in k, ("o handoff precisa do campo dos recibos do B(n) e dos paragrafos do README: " + chave)
    par = k["readme_paragrafo"].rstrip("\n"); par_s = k["readme_paragrafo_sonico"].rstrip("\n")
    assert par.startswith("### O Teste da Única Palavra (v397"), "o paragrafo do README (quadro) nao e' o do quadro"
    assert par_s.startswith("### Sônico e a afinação das cordas (v398"), "o paragrafo do sonico e da afinacao nao e' o novo"
    k.update({"data": V["data"], "s16": V["s16"], "umb": format(V["umb"], ","), "base16": V["base16"], "teor": V["teor"], "rc": V["rc"], "conf16": V["conf16"], "conf_dm": V["conf_dm"], "conf_np": V["conf_np"],
              "pilar": "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), "selo_ts": V["selo_ts"], "num": _num(V), "kernel_prova": _kernel_prova(V), "limites": _limites(V, curto=True), "legal": _legal(V),
              "artigos": ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), "n_cun": d["n_cun"], "n_pedras": V["n_pedras"], "topico": TOPICO_NOVO[:-3], "regra": _regra_do_4_44(V),
              "par_bloco": MARC_PAR_INI + "\n" + par + "\n" + MARC_PAR_FIM, "par_son_bloco": MARC_SON_INI + "\n" + par_s + "\n" + MARC_SON_FIM})
    doc = ("---\nname: handoff-v398-custodia\ndescription: \"HANDOFF v398 (%(data)s) para a sessão do site: o sônico e a afinação das cordas (duas pedras, dois registros com função, seis inscrições de 23/10); `%(s16)s`; B(n) da Bancada feito; TRAZ os parágrafos prontos do README/site (o quadro do Teste da Única Palavra, intocado, e o novo); custódia + pendências do operador\"\n"
           "metadata:\n  type: project\n---\n\n# HANDOFF v398 — CUSTÓDIA (%(data)s)\n\n"
           "**O que é:** `um.py` **v398** `%(s16)s` (%(umb)s B) sobre a v397 `%(base16)s`; %(teor)s; COMPLETA; rc %(rc)s; selftest PASSED; gate intocado; conferidor `%(conf16)s` (deve mudar %(conf_dm)s; não pode mudar %(conf_np)s); pilar %(pilar)s pela chave. "
           "Selo `%(selo_ts)s`.\n\n"
           "**PARÁGRAFOS PRONTOS para o README do espelho e para o site (colar como estão, cada um entre os seus marcadores; o primeiro é o quadro do Teste da Única Palavra, o MESMO da v397, intocado; o segundo é novo).** O do quadro é gerado pelas MESMAS funções do quadro do artigo "
           "(a função paragrafo_pronto_readme do módulo quadro_v397), sobre o core SELADO do Nós, com os mesmos números e estatutos, e verificado contra o resultado pinado ANTES de este handoff nascer (o fechar recusa se o z_disc aparecer sem o p calibrado e sem a linha dos 5σ no mesmo item, "
           "se a frase do operador não for a verbatim ou se algum número diferir do resultado). O novo (sônico e afinação das cordas) é gerado dos registros selados `sonico_v398`, `afinacao_das_cordas_v398` e `cunhagens_v398` e verificado contra o core e contra os números do ensaio a seco "
           "(sem o z_disc do quadro; as citações são trechos verbatim das falas do operador; a sexta inscrição é rotulada como da gerência):\n\n%(par_bloco)s\n\n%(par_son_bloco)s\n\n"
           "%(regra)s\n\n"
           "**O que entrou e o que mediu:** %(num)s.\n\n"
           "%(kernel_prova)s\n\n%(limites)s\n\n%(legal)s\n\n"
           "**O elo B(n) da Bancada Um (feito antes deste handoff; passo simples, sem salto):** recibo da aplicação `%(ap_nome)s` (sha256 `%(ap_sha)s`; veredito `%(ap_ver)s`; evento %(ap_evento)s; bateria `%(ap_bat)s`); recibo da parada do serviço sha256 `%(par_sha)s`; "
           "recibo do religamento sha256 `%(rel_sha)s` (versão servida v398, manifesto `%(rel_man)s`).\n\n"
           "**Para a sessão do site (custódia):** o `um.py` v398, `rodada_v398_stdout.txt`, o selo, o core, o .md canônico (com o quadro no topo, intocado) e o manifesto, os artigos PT/EN (%(artigos)s; o quadro «O Teste da Única Palavra» abre os dois), as %(n_cun)s inscrições de 23/10 por sha256 "
           "(cinco falas do operador e a leitura da gerência que ele ratificou, rotulada; lista na linhagem e no tópico `%(topico)s`; arquivos em `work\\cadeia_de_selo\\v398\\insumos\\cunhagens`), os módulos novos (`work\\cadeia_de_selo\\v398_kernel\\pedras`, `TGLExt/Sonico.lean` e `TGLExt/AfinacaoDasCordas.lean`) e os dois diffs (`DIFF_v397_v398.diff`, `DIFF_KERNEL_v398.txt`) — com PORTA gerada por script, "
           "URL raw (o um.py tem mais de 5 MB), backup da versão v397 no espelho fora do repositório, blob conferido depois do push. Colocar os PARÁGRAFOS acima no README do espelho e no site (ato da sessão do site, com o selo corrente ao lado; o do quadro segue onde está e o novo entra ao lado); publicar os módulos novos no espelho (TGLExt) e regenerar as PORTAS de `tgl_kernel`, `TGLExt` e `TGL`; "
           "a pasta `insumos` (as pedras, as inscrições pinadas e a medida da cobertura; o resultado do Teste da Única Palavra e os três recibos seguem em `v397\\insumos\\fase9`) vai ao espelho com PORTA: sem ela, uma reprodução pública diz NOT_SEALED (fail-closed); os recibos da bateria do B(n) vão ao espelho com PORTA; "
           "a errata ao lado do registro `kh_n1_cobertura_v397` (h2, h3 e h6 viram pisos; h8, tamanho mínimo) e dos cinco contratos (`expected_ladder`); o runner da Fronteira e a camada v398 dos 16 dispositivos "
           "(o número do runner é da sessão do site); a revisão independente antes do portão do operador (o número de céticos é da sessão do site).\n\n"
           "**Pendências SÓ do operador:** nomear os dois registros novos (`sonico_v398` e `afinacao_das_cordas_v398` são provisórios); a pendência [LEGAL] herdada da v395 (a divergência da tabela da patente ACOM Mirror; com a agente de PI); a custódia, subir o site, commit/push. [OPEN]: a discriminação a 5σ (β_TGL na natureza), "
           "a geometria das cordas e a ligação do círculo da folha-mundo ao círculo do boost, a face de Fock do psion (o certificado de Fock da luz sem habitante exibido), o contrato conjunto da rede e H3 em toda direção nula; a F8.1 (bandeiras do gate recalculadas) segue [OPEN] e não é tocada pela v398.\n\n"
           "Pacote e cadeia: `work\\cadeia_de_selo\\v398` (+ `pos_rito`); arquivo `work\\cadeia_de_selo\\v398_selo` e `v398_kernel`. NOT_FALSIFIED não é a palavra da creditação; o gate não se move.\n\n"
           "[[%(topico)s]] [[missao-ultima-flag-um-py]] [[handoff-v397-custodia]]\n") % k
    assert k["par_bloco"] in doc and k["par_son_bloco"] in doc, "os paragrafos do README nao entraram no handoff"
    assert not atribuicao_da_gerencia(doc), ("o handoff atribui mal a leitura da gerencia", atribuicao_da_gerencia(doc)[:2])
    return doc


# ------------------------------------------------------------------- ferramentas da arvore e do indice (OPCIONAIS: so' usadas se alguem escrever patch_arvore_indice_v398.py)
# v398: a linha da arvore da prova
def arvore_linha(V):
    d = _d(V)
    return ("- **O SÔNICO E A AFINAÇÃO DAS CORDAS (v398)** `%s`: %d módulos novos no kernel (%s; o nome «sônico» é do operador), %d bandeiras novas True, escada %s → %s; "
            "os registros `sonico_v398` e `afinacao_das_cordas_v398` leem o kernel do rito e conferem um cálculo (a lei de custo é [INPUT]; a geometria das cordas é [OPEN]; a hipótese `MasslessFirstLevel` é [KNOWN]); as %d inscrições de 23/10 por sha256 (cinco falas do operador e a leitura da gerência, rotulada); validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["n_pedras"], _mods(V), d["n_f"], V["escada_antes"], d["depois"], d["n_cun"]))


# v398: o titulo do verbete do indice
def titulo_verbete(V):
    return "O sônico e a afinação das cordas (v398):"


# v398: o corpo do verbete do indice
def verbete(V):
    return "[REAL — rodada v398 `%s`] %s." % (V["s16"], _num(V))


# v398: a entrada do remissivo
def remissivo(V):
    return "- **O sônico, a afinação das cordas e as inscrições de 23/10 (v398)** — `sonico_v398`, `afinacao_das_cordas_v398`, `cunhagens_v398`, `kh_n1_cobertura_v398`, `%s`" % TOPICO_NOVO
