# -*- coding: utf-8 -*-
# Os TEXTOS da v404 SELADA, ESCRITOS A MAO para o delta da v404 (a semente mecanica veio de textos_v403.py, subida pelo motor; o conteudo e' novo): os DOIS modulos de kernel `ProjecaoTransversalDaMeiaNat` (nome PROVISORIO da gerencia c1, 28/10/2026, aceito pelo operador: a Meia-Nat e' o angulo de 45 graus) e
# `Jo8v32` (o nome do triplo inteiro Caminho . Verdade . Vida, dado pelo operador em 28/10/2026), os TRES registros com funcao `projecao_transversal_v404`, `jo8v32_v404` e `f2b_errata_v404` (os dois primeiros LEEM do kernel do rito a composicao, a estrela, o contrato e o suporte da sua pedra e CALCULAM
# um modelo honesto com beta = alfa x raiz de e em runtime; o terceiro, SEM pedra, le o V1 do ramo B por hash e confere a errata de F2b AO LADO), os registros por spec `cunhagens_v404` (as NOVE falas do operador de 28/10 por sha256, as erratas E7 a E9 em nome proprio da gerencia c1, as decisoes D23 a D26 e a leitura
# da massa) e `kh_n1_cobertura_v404`, e a secao «Jo 8,32 e a projecao transversal da Meia-Nat» do artigo. Os SEIS registros da v403 (caminho, vida, verdade_adendo, bandeiras_do_gate, cunhagens, kh_n1_cobertura) e as pedras seladas da v403 ficam como REGISTRO: sao RECRIADOS pelo rito e conferidos iguais a v403 selada.
# O QUADRO «O Teste da Única Palavra» (v397) PERMANECE no topo do artigo PT/EN e do .md canonico, INTOCADO. Cada numero, hash e veredito entra por chave de V (leitura_v404.ler), por ESPERADOS ou pelo core do Nos, ou e' LIDO de um arquivo aqui, nunca digitado;
# o que vai escrito a mao e' so' prosa, nome de termo (conferido em tempo de execucao no kernel do Nos, no um.py ou no pacote) e frase curta do operador (conferida palavra por palavra contra os bytes das falas).
# REGRA DA ORDEM DO OPERADOR (23/10/2026, sha16 9b182958a5a7a1bc: reportar o 4,44 no inicio do artigo, no README e em tudo mais; vale em TODO texto que o cite): o 4,44 (z_disc calibrado) NUNCA aparece sem o p calibrado e sem a linha dos 5σ no MESMO item (a discriminacao a 5σ,
# o degrau da creditacao, NAO foi alcancada; NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move; o teste nao foi cego). A frase do operador entra VERBATIM (nunca parafraseada entre aspas); o paragrafo do QUADRO sai das MESMAS funcoes do quadro (quadro_v397),
# sobre o core SELADO do Nos. O paragrafo NOVO da v404 NAO traz o 4,44. Estatutos marcados; erratas AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a traducao falhou).
# O PARAGRAFO DO TESTEMUNHO DE DOIS (v399), o da FALSIDADE (v401), o da PONTE, DA QUEDA E DA ESPERANCA (v402) e o de CAMINHO, VERDADE E VIDA (v403) SEGUEM COMO ESTAO no README do espelho e no site: esta versao NAO os regenera nem os substitui; o handoff da v404 so' o diz e traz a NOTA ao lado do da v403 (o nome do triplo inteiro, que ele registra como nao dado, foi dado).
# GUARDA: as cinco regras da P18 (guarda_p18_v404.py) rodam sobre cada texto renderizado em superficies_v404.py, fechar_v404.py e registrar_mapa_v404.py e sobre este arquivo na cadeia. A palavra recusada nunca aparece aqui: a recusa e' dita como «creditação».
import hashlib, json, os, re, sys
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V404"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v404 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(PK))          # ...\Central de Patentes\work
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
TOPICO_NOVO = "v404-selada-jo8v32-projecao-transversal.md"
# os marcadores entre os quais o handoff traz os PARAGRAFOS PRONTOS do README do espelho e do site: o QUADRO (v397, intocado) com os MESMOS marcadores da v397, e o paragrafo NOVO da falsidade
MARC_PAR_INI = "<!-- INICIO_PARAGRAFO_README_v397 -->"; MARC_PAR_FIM = "<!-- FIM_PARAGRAFO_README_v397 -->"
# o tema de cada uma das NOVE falas de 28/10 (resumo da gerencia, nunca citacao): a chave e' o trecho do nome do arquivo de origem (depois do sha16); o sha16, a data e o autor vem dos bytes e do nome, nunca daqui
_TEMAS = (
    ("cunhagem_um_absoluto_radical_entropico", "a constante da luz como raiz da energia sobre a matéria e o um absoluto como o estado de energia fundamental cuja inscrição no radical entrópico quebra a simetria e inaugura o defasamento [INPUT/ONTO]"),
    ("materia_sombra_de_beta", "a pergunta se a matéria é a sombra de β [INPUT]"),
    ("resposta_quatro_bocas_ramo_b", "a resposta às quatro bocas do ramo B do ringdown: o pedágio de Planck lido na propagação, um retorno em 83 raios como a matéria, o 1 absoluto igual ao zero modular como relação (a identidade preservada) [INPUT/ONTO]"),
    ("transicao_para_a_massa", "o aceite do levantamento de onde uma fração igual a β poderia ser contada, e a transição para a massa [INPUT]"),
    ("materia_projecao_transversal_derivada", "a cunhagem: a matéria não é proporcional ao raio de β, é a projeção do eixo transversal e a derivada; por isso o ângulo agudo do neutrino faz sentido [INPUT/ONTO]"),
    ("ordem_prova_do_neutrino", "a ordem de fazer a prova do neutrino para o sen 45° deixar de ser postulado [INPUT]"),
    ("ratificacao_calibrar_nao_e_validar", "calibrar não significa validar: a rota se ajusta ao número, o núcleo sintático permanece íntegro; a ratificação da leitura que faltava [INPUT]"),
    ("nome_do_triplo_Jo8_32", "o nome do triplo inteiro (Caminho, Verdade, Vida): Jo8:32 [INPUT]"),
    ("ratificacao_concordo_com_tudo", "a ratificação da pedra do sen 45°, da leitura, do plano da v404 e da leitura sobre Jo 8,32 [INPUT]"),
)
# nomes de termo de kernel (Lean) citados nos textos: cada um tem de existir em algum .lean de TGLExt/ do Nos (lido na hora); os modulos citados como fonte tem de existir como arquivo
_NOMES_KERNEL = ("neutrino_mass_form_eq", "transverse_amplitude_of_self_conjugate", "half_from_self_conjugate", "half_amplitude_sq", "half_amplitude_eq_halfRoot", "forty_five_unique", "theta_miguel_ne_pi_div_four", "transverse_weight_hasDerivAt_half",
                 "sin_sq_thetaMiguel", "halfnat_from_J_symmetry", "observer_inverse_projection_halfnat", "a_verdade_vos_libertara", "caminho_e_a_ponte_da_escala_dual", "verdade_e_a_esperanca_condicional", "vida_e_a_queda_sem_geometria",
                 "lift_mass_not_selected", "the_fall_is_strictly_anti", "esperanca_condicional_e_nome", "the_name_reads_the_inscription_as_weights", "IsotropicPost", "metric_einstein_from_screen_clausius", "observing_adds_nothing")
_MODULOS_KERNEL = ("ProjecaoTransversalDaMeiaNat", "Jo8v32", "Caminho", "Vida", "VerdadeAdendo", "Verdade", "Posto", "PostoAdendo", "ConjugateAct", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional", "FalsidadeDaInercia", "Fundacao", "Token", "TheNameOperator", "CondExpect", "BisognanoWichmann")
# identificadores do um.py citados nos textos: cada um tem de existir no um.py do Nos (lido na hora)
_NOMES_UM = ("SEALED_CODATA_ALPHA", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404", "_V404_CONTRACTS", "_V404_VERBATINS2", "_V404_SPECS",
             "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "_V403_CONTRACTS", "_V403_VERBATINS2", "_V403_SPECS",
             "prove_qg_closure_gate", "evaluate_quantum_gravity_closure", "ProbeBlindNullAbsent", "blind_null", "void_stacking_blind", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386", "angle_status",
             "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "_V402_CONTRACTS", "_V402_VERBATINS2", "_V402_SPECS",
             "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "_V401_VERBATINS2", "_V401_SPECS", "_V401_FALSIDADE_CONTRACT", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399",
             "cunhagens_v399", "kh_n1_cobertura_v399", "selo_acom_sidecar_v399", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "hubble_ratio_opening_v388", "_v397_quadro_md", "_v397_atomos", "_V397_FRASE_444",
             "testemunha_estatica_v396", "psibit_v395", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V395_PSIBIT_CONTRACT",
             "_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT")
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
N_FALAS = len(_TEMAS)   # (o numero e' CONFERIDO em _d contra len(DL.VERBATIM_ORIGEM_V404) e ESPERADOS[cunhagens]; a prosa diz «nove» e o assert derruba a geracao se o numero mudar)
_CACHE = {}
# a DIRECAO (v399): nenhuma frase pode por a IALD como quem testifica DO operador (fora da fala em que ele a recusa); a mesma regex do conferidor (C12)
_RX_INV = re.compile(r"IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)")
ERRATA_TEOREMAS = "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"   # (a mesma frase de delta_v404.ERRATA_TEOREMAS_PT; o harness confere)


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
    """ESPERADOS_v404.json (gerado pelo ensaio a seco do candidato), lido uma vez."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v404.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _core():
    """O core do Nos (so' leitura), para os campos que so' existem depois do rito; ausente e' falha visivel."""
    if "core" not in _CACHE:
        _CACHE["core"] = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["core"]


def _base_core():
    """O core da v403 selada (a copia de bytes em base_v403): de onde saem os numeros da errata ao lado e a medida da proveniencia."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v403", "um_absoluto.json"), encoding="utf-8"))["core"]
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
    """As NOVE inscricoes de 28/10 embutidas no um.py: o texto vem do arquivo em insumos/cunhagens e o sha256 e' conferido contra ESPERADOS (fail-closed). Devolve {sha16: {sha16, arquivo, nome, text, autor}};
    o autor sai do NOME do arquivo e e' conferido contra o papel que ESPERADOS registra: nesta versao as nove sao falas do operador (nenhuma e' da gerencia)."""
    if "falas" not in _CACHE:
        ec = _esp()["cunhagens"]; out = {}; pasta = os.path.join(PK, "insumos", "cunhagens")
        for k, meta in ec.items():
            s = k[len("v404_cun_"):]
            fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(s + "_")]
            assert len(fs) == 1, ("a inscricao %s nao tem arquivo unico em insumos/cunhagens" % s, fs)
            b = open(os.path.join(pasta, fs[0]), "rb").read()
            assert hashlib.sha256(b).hexdigest() == meta["sha256"] and len(b) == meta["bytes"] and meta["sha256"][:16] == s, "a inscricao %s nao confere com o sha256 de ESPERADOS" % s
            nome = fs[0][len(s) + 1:]
            autor = "gerencia" if nome.startswith("GERENCIA_") else "operador"
            assert autor == "operador" and not str(meta.get("papel", "")).startswith("leitura da gerencia"), ("a v404 nao tem inscricao da gerencia: as nove sao falas do operador", s)
            out[s] = {"sha16": s, "arquivo": fs[0], "nome": nome, "text": b.decode("utf-8"), "autor": autor}
        assert len(out) == len(_TEMAS) == N_FALAS, "as inscricoes de ESPERADOS nao sao as nove de 28/10"
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
    """A cobertura do Audit e a arvore formal da v403 selada (o core guardado em base_v403): de onde saem os numeros da errata ao lado dos pisos."""
    if "cov_base" not in _CACHE:
        kf = _base_core()["kernel_formalization"]
        cov = kf["axiom_coverage_v392"]
        _CACHE["cov_base"] = {"decl": cov["decl"], "thm": cov["thm"], "h8": len(kf["formal_files_sha256"]), "axr": len(kf["axiom_report"])}
    return _CACHE["cov_base"]


def _bancada():
    """A geracao do manifesto que a Bancada de producao pina (do recibo pre_selo pinado em PINOS_BN) e a versao que ela pina; o passo e' simples (sem salto e sem cadeia de selos)."""
    p = json.load(open(os.path.join(PK, "PINOS_BN_v404.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v403" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v403 -> v404 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1}


def _proveniencia(esp):
    """A proveniencia que o compilador emite atribui ao modulo da pedra N declaracoes; todas sao NOVAS no axiom_report (nenhuma reatribuida), e o FLAGS_v404.json do sandbox concorda (as contagens de
    publicas, privadas, nomeadas e auxiliares so' existem la')."""
    if "prov" not in _CACHE:
        kf = _core()["kernel_formalization"]; src = kf["declaration_sources_v394"]; pedras = set(esp["pedras_sha256"])
        b0 = _base_core()["kernel_formalization"]; axr0 = b0["axiom_report"]
        mine = sorted(n for n, p in src.items() if p in pedras)
        novas = [n for n in mine if n not in axr0]
        fj = json.load(open(os.path.join(PK, "kernel", "FLAGS_v404.json"), encoding="utf-8"))
        assert len(mine) == fj["decl_totais_modulos_novos"] and len(novas) == fj["decl_novas_dos_modulos"] == len(mine) and not fj["reatribuidas_as_pedras"], ("a proveniencia do rito != FLAGS_v404.json do sandbox", len(mine), len(novas), fj["reatribuidas_as_pedras"])
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
    """Os numeros da v404, todos LIDOS (V da leitura da rodada, ESPERADOS, core do Nos, base v403, FLAGS do sandbox, os registros): nenhum e' digitado aqui. Recusa se as contagens nao fecham."""
    _conferir_nomes()
    esp = _esp(); tv = V["veracidade"]; sa = V["selo"]; dc = V["declaracao"]; cg = V["cunhagens"]; sc = V["sidecar"]; core = _core(); gt = V["gate"]; gv = gt["values"]; fb = V["f2b"]
    DL_ = _qd().DL; ks = _CHAVES
    mods = sorted(p["modulo"] for p in V["pedras"])
    assert mods == sorted(DL_.STONE_BY_KEY[k]["mod"] for k in ks) and V["n_pedras"] == len(mods) == esp["kernel"]["modulos_novos"] == 2, ("o delta da v404 sao dois modulos, ProjecaoTransversalDaMeiaNat e Jo8v32", mods)
    nf = esp["n_bandeiras_novas"]; grp = esp["n_bandeiras_por_grupo"]
    assert set(grp) == set(ks) and sum(grp.values()) == nf == esp["politica_de_bandeiras"]["n_flags"] == len(esp["bandeiras_novas_chaves"]), "as bandeiras novas nao sao so' as dos dois modulos"
    ft = {}; sha = {}; unc = {}; est_t = {}; est_f = {}; nck = {}; n_sup = {}; n_contr = {}
    for k in ks:
        st = DL_.STONE_BY_KEY[k]; pe = V[k]
        ch = sorted(c for c in esp["bandeiras_novas_chaves"] if c.startswith(st["flag_prefix"]))
        assert len(ch) == grp[k], ("as bandeiras do grupo nao fecham", k, len(ch), grp[k])
        ft[k] = (ch[0], ch[-1])
        assert pe["flag"] == esp["bandeiras_das_pedras"][k] and pe["flag_true"] is True and pe["theorem"] == esp["teoremas_das_pedras"][k], ("a pedra no kernel do rito nao e' a de ESPERADOS", k)
        assert pe["ok"] is True and pe["mech_ok"] is True and pe["values_ok"] is True and pe["estrela_ok"] is True and pe["kernel_ok"] is True and pe["beta_ok"] is True and pe["contexto_ok"] is True and pe["n_checks"] == DL_.N_CHECKS[k], ("o registro com funcao nao e' o contrato de ESPERADOS", k)
        assert len(esp["contrato_das_pedras"][k]) == len(st["contract"]) and len(esp["suporte_das_pedras"][k]) == len(st["support"]), ("o contrato ou o suporte != delta_v404", k)
        sha[k] = esp["pedras"][st["rel"]]["sha16"]; unc[k] = esp["teoremas_das_pedras"][k]; est_t[k] = esp["estrelas_v404"][k]["teorema"]; est_f[k] = esp["estrelas_v404"][k]["bandeira"]
        nck[k] = pe["n_checks"]; n_sup[k] = len(esp["suporte_das_pedras"][k]); n_contr[k] = len(esp["contrato_das_pedras"][k])
    # a errata de F2b (registro com funcao, SEM pedra): selou inteira, o canal retirado antes do dado AO LADO, o V1 e o livro como antes
    rf = esp["registros_funcao_v404"]["f2b"]
    assert fb["sealed"] is True and fb["mech_ok"] is True and fb["values_ok"] is True and fb["ao_lado_ok"] is True and fb["neutrino_intacto"] is True and fb["n_checks"] == DL_.N_CHECKS["f2b"] == rf["n_checks"] and fb["verdict"] == rf["verdict"], "o registro f2b_errata_v404 nao e' o contrato de ESPERADOS (a errata de F2b AO LADO)"
    assert fb["status_antes"] == "AWAITING" and fb["status_agora"] == DL_.F2B_FUTURO_TOKEN and fb["token_v1"] == DL_.F2B_V1_TOKEN_ANTIGO and fb["values"]["previsao_fora_do_intervalo_de_A"] is True, "o canal F2b nao foi de AWAITING a retirado antes do dado, ou o V1 nao segue AWAITING_DATA, ou a previsao do par nao esta fora do intervalo de A"
    # o registro das BANDEIRAS DO GATE (F8.1 da v403) RECRIADO: selado, as 18 calculadas, 0 literais, 15 no veredito (6 + 5 + 4), a letra do veredito a da v403 (o gate nao se move)
    rg = esp["registros_funcao_v403"]["gate"]
    assert gt["sealed"] is True and gt["f81_ok"] is True and gt["mech_ok"] is True and gt["values_ok"] is True and gt["n18"] == 18 and gt["n_checks"] == DL_.D3.N_CHECKS["gate"] == rg["n_checks"] and gt["verdict"] == rg["verdict"], "o registro bandeiras_do_gate_v403 recriado nao e' o da v403 selada"
    assert gv["n_flags"] == 18 == gv["n_true"] == gv["n_calculated"] and gv["n_literal"] == 0 and gv["n_read_by_the_verdict"] == 15 and gv["read_by_the_verdict"] == [6, 5, 4] and gv["gate_verdict_equals_v402"] is True and gv["ext_ls2_n"] == gt["n_ls2"] == 6 and gt["sonda"] == 1, "as bandeiras do gate nao fecham: 18 calculadas, 0 literais, 15 no veredito, a familia ext_ls2_*, a sonda e a letra da v403"
    assert N_FALAS == len(DL_.VERBATIM_ORIGEM_V404) == len(esp["cunhagens"]) == 9, "o numero de inscricoes de 28/10 mudou: a prosa dos textos diz nove (ler N_FALAS, DL.VERBATIM_ORIGEM_V404 e ESPERADOS[cunhagens])"
    pre = list(DL_.VERBATIM_PREFIXOS_DA_ORDEM_V404)
    ss = {"umabs": _sha_por("cunhagem_um_absoluto_radical_entropico"), "sombra": _sha_por("materia_sombra_de_beta"), "bocas": _sha_por("resposta_quatro_bocas_ramo_b"), "trans": _sha_por("transicao_para_a_massa"), "massa": _sha_por("materia_projecao_transversal_derivada"),
          "ordem": _sha_por("ordem_prova_do_neutrino"), "calibrar": _sha_por("ratificacao_calibrar_nao_e_validar"), "jo8": _sha_por("nome_do_triplo_Jo8_32"), "ok": _sha_por("ratificacao_concordo_com_tudo")}
    assert sorted(s_[:8] for s_ in ss.values()) == sorted(p_[:8] for p_ in pre) and len(set(ss.values())) == 9, "as inscricoes nao sao as de DL.VERBATIM_PREFIXOS_DA_ORDEM_V404"
    assert V["fal401"]["ok"] is True and V["fal401"]["verdict"] == esp["veredito_da_falsidade_v403"], "o registro falsidade_da_inercia_v401 recriado nao e' o selado da v403"
    assert all(v_["sealed"] is True for v_ in V["fun402"].values()) and len(V["fun402"]) == 3 and all(v_["sealed"] is True for v_ in V["fun403"].values()) and len(V["fun403"]) == 3, "os registros com funcao da v402 ou da v403 recriados nao sao os selados"
    assert V["cunh403"]["ok"] is True and V["cunh403"]["kh_ok"] is True and V["cunh402"]["ok"] is True and V["cunh402"]["kh_ok"] is True and V["cunh401"]["ok"] is True and V["cunh399"]["ok"] is True, "os registros por spec da v403, da v402, da v401 ou da v399 recriados nao sao os selados"
    assert len(V["pedras_v403"]) == 3 and all(p_["ok"] is True for p_ in V["pedras_v403"].values()), "as tres pedras seladas da v403 deixaram de estar no kernel do Nos com o sha256 da v403"
    assert sa["ok"] is True and sa["n_checks"] == esp["selo_acom"]["n_checks"] and sa["checks_ok"] is True and sa["values_ok"] is True and sa["beta_ok"] is True, "o registro selo_pela_propria_tecnologia_v399 do core nao e' o contrato de ESPERADOS"
    assert dc["ok"] is True and dc["n_checks"] == esp["declaracao"]["n_checks"] and dc["checks_ok"] is True and dc["ancoras_ok"] is True and dc["direcao_ok"] is True, "o registro declaracao_do_operador_v399 do core nao e' o contrato de ESPERADOS"
    assert sc["ok"] is True and sc["n_objetos"] == len(esp["sidecar"]["objetos"]) and sc["recusas"] == 0, "o sidecar um_absoluto_selo_acom.json nao e' o de ESPERADOS"
    assert tv["ok"] is True and tv["n_checks"] == esp["veracidade"]["n_checks"] and tv["checks_ok"] is True and tv["numeros_ok"] is True and tv["fontes_ok"] is True, "o registro teste_de_veracidade_fase9_v397 do core nao e' o contrato de ESPERADOS (o quadro do topo le os numeros dele)"
    assert cg["ok"] is True and cg["verbatim_ok"] is True and cg["n"] == len(V["verbatins"]) == len(_falas()) == N_FALAS and cg["todas_do_operador"] is True and cg["erratas_ok"] is True and cg["n_erratas"] == 3 and cg["decisoes_ok"] is True and cg["nomes_ok"] is True and cg["massa_ok"] is True and cg["reg403_ok"] is True, \
        "cunhagens_v404 != as nove de 28/10, ou alguma nao e' fala do operador, ou faltam as erratas E7 a E9, as decisoes D23 a D26, os nomes das pedras, a leitura da massa ou as pedras da v403 como registro"
    er = _g(core, "cunhagens_v404", "erratas") or []
    assert len(er) == 3 and all(str(e.get("assinatura", "")).startswith("gerencia c1, em nome proprio") for e in er) and "neutrino_mass.angle_status" in str(er[0].get("ao_lado_de")) and "F2b" in str(er[1].get("ao_lado_de")) and "cunhagens_v403" in str(er[2].get("ao_lado_de")), "as erratas E7, E8 e E9 nao estao no registro cunhagens_v404 (em nome proprio da gerencia c1, E7 ao lado de neutrino_mass.angle_status, E8 ao lado da cobranca F2b, E9 ao lado de cunhagens_v403)"
    dts = {re.match(r"(?:OPERADOR|GERENCIA)_(\d{2})out_", f["nome"]).group(1) for f in _falas().values()}
    assert dts == {"28"}, "o nome de arquivo de alguma inscricao nao e' de 28/10 (a data dos textos e' 28/10)"
    qd = _qd(); a = _atomos()
    assert qd.Q._v397_linha_de_maquina(a, "pt") == esp["quadro"]["linha_de_maquina_pt"], "a linha de maquina do quadro (core) != a de ESPERADOS"
    assert esp["quadro"]["frase_do_operador"] == qd.DL.FRASE_DO_OPERADOR_4_44 == qd.Q._V397_FRASE_444, "a frase do operador do quadro != a verbatim"
    base = os.path.join(PK, "base_v403", "um.py")
    if "base_b" not in _CACHE:
        assert s16(base) == V["base16"], "base_v403/um.py nao e' a v403 selada"
        _CACHE["base_b"] = os.path.getsize(base)
    delta = V["umb"] - _CACHE["base_b"]
    kf = core.get("kernel_formalization") or {}; prov = kf.get("declaration_sources_status_v394") or {}
    assert prov.get("ok") is True and prov.get("compiler_names") == prov.get("audited_names") == V["axiom_report_n"], "a proveniencia emitida pelo compilador nao cobre o axiom_report do rito"
    assert V["n_ver_mudaram"] == 0, "algum veredito fora da troca dita mudou: nao ha texto a escrever"
    assert V["n18"] == 18 and all(i in V["patch_ids"] for i in ("N00_main_projecao_jo8v32", "N00b_main_errata_f2b", "N01_main_specs", "N02_selo", "W02_runtime_v404", "C13_kh_n1_v403_pisos")), \
        "o gate nao tem as 18 bandeiras True, ou o candidato nao traz os patches que chamam os tres registros (N00), os registros por spec (N01), o resumo no selo (N02), o runtime (W02) e os pisos do registro da v403 (C13)"
    assert esp["h8_entradas"] == esp["formal_files_n"] + len(esp["h8_residuais_do_nos"]), "a arvore formal do rito != embutidas + residuais do Nos"
    pb = core.get("psibit_v395") or {}; pbc = pb.get("conditional_psion_face") or {}
    assert pbc.get("flag_true") is True and kf.get(pbc.get("flag")) is True and pbc.get("inhabitant_exhibited") is False, "a face de Fock do psibit_v395 nao segue condicional e com a bandeira True"
    pv = _proveniencia(esp)
    s403 = {"caminho": esp["pedras_v403_sha256"]["TGLExt/Caminho.lean"][:16], "vida": esp["pedras_v403_sha256"]["TGLExt/Vida.lean"][:16], "verdade_adendo": esp["pedras_v403_sha256"]["TGLExt/VerdadeAdendo.lean"][:16]}
    assert [_g(core, "cunhagens_v404", "extras", "pedras_da_v403_como_registro", k_) for k_ in ("caminho", "vida", "verdade_adendo")] == [s403["caminho"], s403["vida"], s403["verdade_adendo"]], "as pedras da v403 como registro (cunhagens_v404) != os sha16 de ESPERADOS[pedras_v403_sha256]"
    aa = _g(core, "neutrino_mass", "angle_status"); assert aa and hashlib.sha256(str(aa).encode("utf-8")).hexdigest() == esp["neutrino_angle_status_antigo_sha256"] and str(aa).startswith(DL_.ANGLE_STATUS_ANTIGO_PREFIXO), "o texto antigo de neutrino_mass.angle_status nao esta intacto no core do Nos"
    return {"n_f": nf, "n_g": {k: grp[k] for k in ks}, "ft": ft, "sha": sha, "unc": unc, "est_t": est_t, "est_f": est_f, "nck": nck, "n_sup": n_sup, "n_contr": n_contr, "n_aux": esp["politica_de_bandeiras"]["n_excluidas"],
            "depois": V["teor"].split("/")[0], "delta": delta, "pct": ("%.1f" % (100.0 * delta / _CACHE["base_b"])).replace(".", ","), "prov": prov["compiler_names"], "n_cun": len(V["verbatins"]), "n_op": N_FALAS,
            "h8": esp["h8_entradas"], "h8_emb": esp["formal_files_n"], "h8_res": ", ".join("`%s`" % x for x in esp["h8_residuais_do_nos"]), "n_res": len(esp["h8_residuais_do_nos"]), "cb": _cov_base(), "bank": _bancada(), "pv": pv,
            "n_checks_v": tv["n_checks"], "n_ck_sel": sa["n_checks"], "n_ck_dec": dc["n_checks"], "n_ck_cun": cg["n_checks"], "n_anc": len(esp["declaracao"]["ancoras"]), "f8": {k: v[:8] for k, v in esp["veracidade"]["fontes"].items()},
            "ss": ss, "data_falas": "28/10/" + V["data"][-4:], "s403": s403, "f2b": fb["values"], "f2b_agora": fb["status_agora"], "f2b_antes": fb["status_antes"],
            "g": {"n_flags": gv["n_flags"], "n_true": gv["n_true"], "n_calc": gv["n_calculated"], "n_lit": gv["n_literal"], "n_ver": gv["n_read_by_the_verdict"], "rv": gv["read_by_the_verdict"], "info": list(gv["informative"]), "ls2": gv["ext_ls2_n"], "n_chk": gv["n_gate_checks"], "n_chk_reg": gt["n_checks"], "feed": list(DL_.F81_FEED)}}


def _mods(V):
    return ", ".join("`%s`" % p["modulo"].split(".")[-1] for p in sorted(V["pedras"], key=lambda p: p["modulo"]))


def _extras(V):
    # os registros novos ALEM DOS CINCO FIXOS (V["reg404"] tem so' os cinco: os tres com funcao, cunhagens_v404 e kh_n1_cobertura_v404), ditos pelo nome
    ex = [k for k in V["registros_novos"] if k not in V["reg404"]]
    return (", ".join("`%s`" % k for k in ex)) if ex else "nenhum além dos cinco fixos"


def _cab(V):
    return "v404 SELADA (COMPLETA)** `%s`" % V["s16"]


def _num(V, verdicts=True):
    """O paragrafo dos numeros da v404 (kernel, os tres registros com funcao, os dois registros por spec, os da v403, da v402, da v401 e da v399 recriados, o sidecar, a troca dita): usado na linhagem, no Atlas, no core, no topico novo, no verbete e no handoff."""
    d = _d(V); kh = V["kh"]; sc = V["sidecar"]; sa = V["selo"]; g = d["g"]
    vd = (lambda k: " (%s)" % V["reg404"][k]["verdict"]) if verdicts else (lambda k: "")
    pv_ = V["projecao"]["values"]; jv = V["jo8v32"]["values"]; fv = d["f2b"]; ft = d["ft"]; ng = d["n_g"]
    aux = ("nenhuma auxiliar gerada pelo compilador ficou de fora" if not d["n_aux"] else "%d auxiliares geradas pelo compilador ficam sem bandeira" % d["n_aux"])
    kern = _f("o kernel ganhou {n_pedras} módulos novos ({mods}; o nome do primeiro é provisório da gerência c1, aceito pelo operador; o do segundo é do operador, 28/10/2026), com {n_f} bandeiras novas True (projeção {n_p}, {p0}; Jo8v32 {n_j}, {j0}), só de declaração nomeada ({aux}), e escada {antes} → {depois} teoremas limpos "
              "({axr} declarações no `axiom_report`, {fora} fora do trio, {nl} nomes não lidos; a proveniência de cada declaração emitida pelo compilador cobre as mesmas {prov}); "
              "errata ao lado da v394, mantida (em nome próprio da gerência c1): " + ERRATA_TEOREMAS,
              n_pedras=V["n_pedras"], mods=_mods(V), n_f=d["n_f"], n_p=ng["projecao"], p0=_faixa(ft["projecao"], ng["projecao"]), n_j=ng["jo8v32"], j0=_faixa(ft["jo8v32"], ng["jo8v32"]),
              aux=aux, antes=V["escada_antes"], depois=d["depois"], axr=V["axiom_report_n"], fora=kh["fora"], nl=kh["nao_lidas"], prov=d["prov"])
    pro = _f("o registro `projecao_transversal_v404`{vd}, lido na fractalização do Um logo depois das bandeiras do gate (v403): lê do kernel do próprio rito a composição `{unc}` ({n_contr} do contrato, {n_sup} termos que ela cita, todos no trio; a estrela `{est}`, bandeira `{estf}`) "
             "e CALCULA, com β = α(CODATA 2018) × √e = {beta} em runtime: sen(π/4) = {s}, sen²(π/4) = {s2} (a Meia-Nat é o ângulo de 45°), θ_M = {tm} e θ_M − π/4 = {dtm} (o ângulo agudo do neutrino não é θ_M), a derivada de sen²θ em π/4 vale {der}, "
             "e a massa m = β · sen(π/4) · E₀ = {m} meV, com E₀ = {e0} eV DECLARADO, idêntica ao canal `neutrino_mass` do core a 1e-12 ({nck} checagens, todas passaram); o texto antigo de `neutrino_mass.angle_status` fica no registro (a errata é ao lado)",
             vd=vd("projecao_transversal_v404"), unc=d["unc"]["projecao"].split(".")[-1], n_contr=_pl(d["n_contr"]["projecao"], "item", "itens"), n_sup=d["n_sup"]["projecao"], est=d["est_t"]["projecao"].split(".")[-1], estf=d["est_f"]["projecao"],
             beta=_p(pv_["beta"], 12), s=_p(pv_["sin_pi_over_4"], 12), s2=_p(pv_["sin_sq_pi_over_4"], 12), tm=_p(pv_["theta_M"], 9), dtm=_p(pv_["theta_M_minus_pi_over_4"], 9), der=_p(pv_["derivative_of_sin_sq_at_pi_over_4"], 9),
             m=_p(pv_["m_nu_meV_runtime"], 9), e0=_pn(pv_["e0_eV_declared"], 3), nck=d["nck"]["projecao"])
    jo = _f("o registro `jo8v32_v404`{vd}: lê a conjunção `{unc}` (bandeira `{unf}`; também a estrela), {n_contr} do contrato e os {n_sup} termos da v403 que ela cita, todos no trio, e RELÊ os três registros da v403 (as checagens {cks}, todas passaram) com β = {beta} em runtime: "
            "o p⁺ encolhe pelo fator {pf} em s = β, a perda de peso por unidade vale {loss} e α² vale {a2} ({nck} checagens, todas passaram); as hipóteses nomeadas dos componentes seguem nomeadas (`IsotropicPost` na Vida; `hpp` e `hopt` na Verdade)",
            vd=vd("jo8v32_v404"), unc=d["unc"]["jo8v32"].split(".")[-1], unf=g_flag(V, "jo8v32"), n_contr=_pl(d["n_contr"]["jo8v32"], "item", "itens"), n_sup=d["n_sup"]["jo8v32"], cks="/".join(str(x) for x in jv["v403_mechanics_checks"]), beta=_p(jv["beta"], 12),
            pf=_p(jv["p_plus_factor_at_beta"], 9), loss=_p(jv["post_weight_loss_per_unit"], 9), a2=_pe(jv["alpha_squared"], 6), nck=d["nck"]["jo8v32"])
    f2 = _f("o registro `f2b_errata_v404`{vd}, sem pedra: o V1 do ramo B (v386) lido por hash e como antes (veredito `{v1}`, conjunto D cego de {nd} eventos, {nc} cobranças do livro v383 intactas), a calibração A (NOT_BLIND) com a deformação comum {a} [{a0}; {a1}] contra a previsão do par {par}, fora do intervalo de A e de sinal oposto "
            "({dist} abaixo do limite inferior); o canal F2b passa de `{antes}` a `{agora}`, AO LADO, sem reescrever o V1 nem o registro da v386; nenhum desfecho sai de A, D não é aberto, β, a lei do defasamento e R2 ficam ({nck} checagens, todas passaram)",
            vd=vd("f2b_errata_v404"), v1=V["f2b"]["token_v1"], nd=fv["conjunto_D_n"], nc=fv["n_cobrancas_v383"], a=_p(fv["calibracao_A_central"], 3), a0=_p(fv["calibracao_A_inferior"], 3), a1=_p(fv["calibracao_A_superior"], 3), par=_p(fv["previsao_do_par"], 6),
            dist=_p(fv["distancia_da_previsao_ao_limite_inferior_de_A"], 6), antes=d["f2b_antes"], agora=d["f2b_agora"], nck=V["f2b"]["n_checks"])
    cun = _f("o registro `cunhagens_v404`{vd}: as {n} falas de 28/10 embutidas por sha256 e consumidas no rito, TODAS falas do operador (nenhuma é da gerência); as erratas E7, E8 e E9 (em nome próprio da gerência c1: o texto antigo do ângulo do neutrino fica e a errata é ao lado; o canal F2b é retirado antes do dado; o nome do triplo inteiro foi dado); "
             "as decisões D23 a D26 da gerência; a leitura da massa de 28/10 [ONTO]; as três pedras da v403 como registro ({nck} checagens, todas passaram); as falas são [INPUT/ONTO] e valem como leitura dele, não como medida",
             vd=vd("cunhagens_v404"), n=d["n_cun"], nck=d["n_ck_cun"])
    khs = _f("o registro `kh_n1_cobertura_v404`{vd}: {decl} constantes, {thm} teoremas, {fora} fora do trio, {nl} nomes não lidos; a árvore formal do Nós depois do rito tem {h8} entradas ({emb} embutidas mais {nres} residual do Nós: {res}), "
             "e o pino h8 do registro é o hash dessa árvore, calculado por script sobre a árvore simulada do Nós na geração do candidato",
             vd=vd("kh_n1_cobertura_v404"), decl=kh["decl"], thm=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"], h8=d["h8"], emb=d["h8_emb"], nres=d["n_res"], res=d["h8_res"])
    rec = _f("os registros da v403 (`caminho_v403`, `vida_v403`, `verdade_adendo_v403`, `bandeiras_do_gate_v403`, `cunhagens_v403` e `kh_n1_cobertura_v403`), da v402 (`ponte_da_escala_dual_v402`, `queda_sem_geometria_v402`, `esperanca_condicional_v402`, `cunhagens_v402` e `kh_n1_cobertura_v402`), "
             "da v401 (`falsidade_da_inercia_v401`, `cunhagens_v401` e `kh_n1_cobertura_v401`) e da v399 (`selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399`, `cunhagens_v399` e `kh_n1_cobertura_v399`) "
             "são recriados no mesmo ponto do main e seguem selados e iguais ao ensaio a seco (os da v403, da v402 e da v401, também iguais à v403 selada), e as três pedras seladas da v403 (Caminho, Vida e VerdadeAdendo) seguem no kernel do Nós com o sha256 da v403, como registro; "
             "o gate não se moveu: o `qg_closure` do core é idêntico ao da v403 (as {n18} bandeiras, os sete checks e a letra do veredito); "
             "o selo pela própria tecnologia sela os {bytes} bytes do `um.py` v404 ao lado do SHA-256 (perfil `{perfil}`, {nctl} controles negativos recusados), e o sidecar `um_absoluto_selo_acom.json` (arquivo da custódia desde a v399, reescrito pelo rito; sha256 `{sc16}`, veredito `{sv}`, {nr} recusas) lista os {no} objetos finais",
             n18=g["n_flags"], bytes=format(sa["bytes"], ","), perfil=sa["perfil"], nctl=sa["n_controles"], sc16=sc["sha16"], sv=sc["veredito"], nr=sc["recusas"], no=sc["n_objetos"])
    ex = _extras(V)
    resto = _f("{ex}; o registro `teste_de_veracidade_fase9_v397` segue selado e igual (o quadro do topo do artigo le os numeros dele); troca dita (só números): {troca}; nenhuma mudança NÃO numérica: {nm} vereditos fora da troca dita mudaram (exigido: 0); validade no kernel não é creditação",
               ex=("nenhum registro novo além dos cinco fixos" if ex.startswith("nenhum") else "registros novos além dos cinco fixos: " + ex), troca=", ".join("`%s`" % x for x in V["troca_dita"]), nm=V["n_ver_mudaram"])
    return "; ".join([kern, pro, jo, f2, cun, khs, rec, resto])


def _cunhagens(V, forma="lista"):
    """As inscricoes de 28/10 embutidas por sha256: 'lista' (data, sha16, autor e tema, uma por linha; as nove sao falas do operador) ou 'curta' (uma frase com os sha16). Data, sha16 e autor vem dos bytes e do nome; o tema e' da gerencia (_TEMAS)."""
    fl = list(_falas().values()); assert len(fl) == len(V["verbatins"]) == N_FALAS
    d = _d(V); ss = d["ss"]
    if forma == "curta":
        return _f("{n} inscrições embutidas por sha256, todas falas do operador [INPUT/ONTO] — a matéria como projeção do eixo transversal `{a}`, a ordem de provar o neutrino `{b}`, o pedágio de Planck lido na propagação `{c}`, calibrar não significa validar `{e}`, o nome Jo8:32 `{f}` e a ratificação `{g}` (e as outras três: `{h}`, `{i}`, `{j}`)",
                  n=len(fl), a=ss["massa"], b=ss["ordem"], c=ss["bocas"], e=ss["calibrar"], f=ss["jo8"], g=ss["ok"], h=ss["sombra"], i=ss["trans"], j=ss["umabs"])
    linhas = []
    for dd in fl:
        r = [tema for chave, tema in _TEMAS if chave in dd["nome"]]
        assert len(r) == 1, ("a inscricao nao tem um tema unico em _TEMAS", dd["sha16"], len(r))
        linhas.append("- %s `%s` (fala do operador) — %s" % (_data_fala(dd, V), dd["sha16"], r[0]))
    return "\n".join(linhas)


def _ordem(V):
    """A ordem do operador de 28/10: so' citacao conferida contra os bytes das falas DO OPERADOR."""
    d = _d(V); ss = d["ss"]
    q_sombra = _cita("A matéria é a sombra de betatgl, então?"); q_materia = _cita("a matéria é a projeção do eixo transversal"); q_derivada = _cita("então a matéria não é proporcional, ela seria a derivada"); q_ordem = _cita("veja se consegue fazer a prova do neutrino para derivarmos e não ser mais postulado")
    q_ped = _cita("pedágio de planck lido na propagação"); q_cal = _cita("calibrar Não significa validar"); q_jo8 = _cita("só consegui sintetizar assim: Jo8:32"); q_ok = _cita("Perfeito, concordo com tudo")
    return _f("**A ordem:** [INPUT/ONTO] as {n_op} falas do operador (Luiz Antonio Rotoli Miguel) de {data} que entram nesta rodada, TODAS dele (nenhuma é da gerência), embutidas por sha256 no registro `cunhagens_v404` e listadas abaixo (as aspas aqui são TRECHOS, conferidos palavra por palavra contra os bytes de cada fala; "
              "o texto íntegro está em `work\\cadeia_de_selo\\v404\\insumos\\cunhagens`): a pergunta {q_sombra} (`{s_sombra}`); a cunhagem {q_materia} e {q_derivada} (`{s_massa}`); a ordem {q_ordem} (`{s_ordem}`); sobre o ramo B do ringdown, {q_ped} (`{s_bocas}`) e {q_cal} (`{s_cal}`); "
              "o nome do triplo inteiro, {q_jo8} (`{s_jo8}`); e a ratificação, {q_ok} (`{s_ok}`) [DECLARADO: o plano, a leitura sobre Jo 8,32 e a leitura da gerência foram os apresentados na sessão; esta cadeia guarda a ratificação verbatim, não a apresentação]. "
              "A gerência c1 preparou o candidato e rodou o rito (pacote `work\\cadeia_de_selo\\v404`); as fontes pinadas dos registros ficam em `insumos`: as duas pedras (`ProjecaoTransversalDaMeiaNat.lean` e `Jo8v32.lean`), o levantamento da transição para a massa e a medida da cobertura (`KH_N1_v404.json`); "
              "o resultado do Teste da Única Palavra, que o quadro do topo lê, mora na v397 (`insumos\\fase9`); quem constrói não aprova: a revisão independente do candidato, das pedras e dos derivados da cadeia é ato distinto e não é afirmada por este registro.",
              n_op=d["n_op"], data=d["data_falas"], q_sombra=q_sombra, q_materia=q_materia, q_derivada=q_derivada, q_ordem=q_ordem, q_ped=q_ped, q_cal=q_cal, q_jo8=q_jo8, q_ok=q_ok, s_sombra=ss["sombra"], s_massa=ss["massa"], s_ordem=ss["ordem"], s_bocas=ss["bocas"], s_cal=ss["calibrar"], s_jo8=ss["jo8"], s_ok=ss["ok"])


def _sidecar(V):
    """O sidecar um_absoluto_selo_acom.json: arquivo da custodia desde a v399 (D5); o selo nao pode conter o selo ACOM de si mesmo; o rito da v404 o REESCREVE."""
    d = _d(V); sc = V["sidecar"]
    objs = "; ".join("`%s` (%s B, sha16 `%s`)" % (n, format(o["bytes"], ","), o["sha16"]) for n, o in sc["objetos"].items())
    return _f("**O sidecar `um_absoluto_selo_acom.json` [REAL; arquivo da custódia desde a v399, D5; reescrito por este rito]:** depois da ÚLTIMA escrita do selo, o `um.py` v404 escreve a segunda testemunha dos {no} objetos FINAIS com o SHA-256 ao lado ({objs}); sha256 do sidecar `{sc16}` ({sb} B), esquema `{esq}`, veredito `{sv}`, {nr} recusas. "
              "O selo não pode conter o selo ACOM de si mesmo (seria circular): o sidecar fica AO LADO e carrega o SHA-256 do selo final, e o selo traz só os resumos (veredito, bandeira e hashes), agora também os dos três registros com função da v404. "
              "A recusa do selo ACOM só REGISTRA (D4): o SHA-256 segue soberano e o rito não cai. A primitiva de integridade é o SHA-256 [KNOWN]; a segunda testemunha NÃO acrescenta força criptográfica independente, e a confidencialidade não é alegada nem medida. A custódia da v399, da v403 e da v404 é CONJUNTA.",
              objs=objs, no=sc["n_objetos"], sc16=sc["sha16"], sb=format(sc["bytes"], ","), esq=sc["esquema"], sv=sc["veredito"], nr=sc["recusas"])


def _pedra(V):
    """As DUAS pedras: a projecao transversal (teoremas novos e pequenos sobre termos que o kernel ja tem) e a conjuncao Jo8v32 (por citacao); o que elas NAO entregam; as tres da v403 como registro."""
    d = _d(V); s4 = d["s403"]
    return _f("**As duas pedras [REAL]** (o nome da primeira é provisório da gerência c1, aceito pelo operador; o da segunda é do operador, 28/10/2026): `ProjecaoTransversalDaMeiaNat` (sha16 `{h1}`; {c1} do contrato; {s1} termos citados, entre eles `observer_inverse_projection_halfnat`, `halfnat_from_J_symmetry` e `sin_sq_thetaMiguel`; composição `{t1}`, estrela `{e1}`; {n1} bandeiras) "
              "e `Jo8v32` (sha16 `{h2}`; {c2}; {s2} termos citados; composição `{t2}`, que é também a estrela; {n2} bandeira), só no trio, sem axioma próprio. A primeira traz teoremas novos e pequenos, só álgebra sobre termos que o kernel já tem: da fronteira autoconjugada `x = 1 − x` sai `x = ½`, a amplitude transversal de um peso ½ é `√½ = sen(π/4)` (`transverse_amplitude_of_self_conjugate`), "
              "em `[0, π/2]` só `π/4` tem `sen² = ½` (`forty_five_unique`), a forma do neutrino `β · sen 45° · E₀` é `sen²θ_M · sen(π/4) · E₀` (`neutrino_mass_form_eq`), `θ_M ≠ π/4` sempre que `β ≠ ½` (`theta_miguel_ne_pi_div_four`) e a derivada de `sen²θ` em `π/4` vale 1 (`transverse_weight_hasDerivAt_half`). "
              "A segunda é uma conjunção INCONDICIONAL, por citação, das três estrelas da v403 (padrão `Token`, v397): nenhuma matemática nova, nenhum número; as hipóteses nomeadas dos componentes (`IsotropicPost`; `hpp` e `hopt`) seguem nomeadas, a conjunção as carrega e não as descarrega. "
              "As três pedras seladas da v403 (`Caminho` `{o1}`, `Vida` `{o2}` e `VerdadeAdendo` `{o3}`) ficam como REGISTRO: pedra selada não se renomeia por cima. "
              "As pedras NÃO derivam E₀ (a escala de 1 eV do neutrino segue DECLARADA) nem β (β = α√e é a regra, do axioma; entra como variável real positiva, jamais literal) e NÃO afirmam que a massa do neutrino É a projeção transversal do estado inscrito: essa identificação é [ONTO] (leitura do operador, ratificada) e nenhum termo de kernel a diz.",
              h1=d["sha"]["projecao"], c1=_pl(d["n_contr"]["projecao"], "item", "itens"), s1=d["n_sup"]["projecao"], t1=d["unc"]["projecao"].split(".")[-1], e1=d["est_t"]["projecao"].split(".")[-1], n1=d["n_g"]["projecao"],
              h2=d["sha"]["jo8v32"], c2=_pl(d["n_contr"]["jo8v32"], "item", "itens"), s2=d["n_sup"]["jo8v32"], t2=d["unc"]["jo8v32"].split(".")[-1], n2=d["n_g"]["jo8v32"], o1=s4["caminho"], o2=s4["vida"], o3=s4["verdade_adendo"])


def _entrou(V):
    d = _d(V)
    return _f("**O que entrou** (pacote `work\\cadeia_de_selo\\v404` sobre a v403 `{base}`; {np} patches — {patches}; instalado em {inst}; o `um.py` cresce {delta} B, {pct}%): {num}.",
              base=V["base16"], np=V["n_patches"], patches=V["patches"], inst=V["instalado_em"], delta=format(d["delta"], ","), pct=d["pct"], num=_num(V))


def _regra_do_4_44(V):
    """A regra da ordem do operador (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item; o QUADRO do topo (v397) PERMANECE, intocado; onde o numero aparece e como se confere."""
    d = _d(V); a = _atomos(); q = _frase_444()
    return _f("**A regra do 4,44 (ordem do operador de 23/10/2026, `{s44}`) e o quadro do topo:** o quadro «O Teste da Única Palavra» (v397) PERMANECE, intocado, no topo do artigo (PT e EN) e do .md canônico, e o parágrafo dele segue no README do espelho e no site: o z_disc calibrado é reportado no início, "
              "e NUNCA sem o p calibrado e sem a linha dos 5σ no mesmo item: {z444}. A frase do operador entra VERBATIM, {q}, como leitura dele [INPUT/ONTO], não como critério da régua; a paráfrase da gerência nunca entra entre aspas. `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; o teste não foi cego. "
              "[REAL] o quadro do artigo, o do .md e o parágrafo pronto do README/site saem das MESMAS funções (`_v397_atomos` e `_v397_quadro_md`), sobre o registro `teste_de_veracidade_fase9_v397` selado no core do Nós, e a cadeia os confere de novo contra o resultado pinado "
              "(a linha de máquina do quadro, cada número, a frase verbatim e a regra da ordem item a item), com controles negativos que reprovam o 4,44 sem o p, sem a linha dos 5σ, com número adulterado ou com a frase parafraseada. "
              "O parágrafo NOVO da v404 não traz o 4,44, e a cadeia confere isso.",
              s44=_esp()["quadro"]["frase_sha16"], z444=_z444(), q=q)


def _kernel_prova(V):
    d = _d(V); g = d["g"]
    return _f("**O que o kernel prova e o que é leitura:** [REAL] as composições das duas pedras e as estrelas estão no kernel deste rito, dentro do trio, com proveniência no módulo de cada pedra, e citam termos que o kernel já tem, cada um no `axiom_report`, no trio, com a proveniência que o compilador emite: "
              "`{t1}` (a forma do neutrino; estrela `{e1}`) e `{t2}` (a conjunção das três estrelas da v403; também a estrela); tudo lido a cada rito pelos registros `projecao_transversal_v404` ({n1} checagens do cálculo), `jo8v32_v404` ({n2}), `f2b_errata_v404` ({n3}) e `cunhagens_v404` ({nc} checagens) "
              "e coberto por `kh_n1_cobertura_v404`. [REAL] os registros NÃO são prova de kernel sobre a natureza: conferem os termos citados e o cálculo nos modelos e não movem o gate; a prova como validade não muda. "
              "[REAL] as {nf} bandeiras do gate são as da v403, lidas do código e do core do próprio rito: {nc2} calculadas e {nl} literais; o veredito lê {nv}; a letra do veredito é a da v403 (o gate não se moveu). "
              "[KNOWN] a fronteira autoconjugada, o Teorema S-∂ e o seno de π/4 são da literatura e do axioma; a lei de escala de Takesaki segue dado. [INPUT] as falas do operador de 28/10 são leituras dele; "
              "[ONTO, só estas] a identificação de que a massa é a projeção transversal do estado inscrito, a leitura do pedágio de Planck na propagação (o 1 absoluto igual ao zero modular como relação) e a leitura por Jo 8,31-32 são do operador e da gerência c1, ratificadas, sem termo no kernel. "
              "[OPEN] `E₀` (1 eV declarado; 1,02 eV zeraria a tensão do m², conta da gerência c1 [DERIVED]), a lei de propagação que carregaria o pedágio, `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β e o caso III₁; a independência das quatro bandeiras experimentais do gate e os mocks de survey. "
              "A retirada do canal F2b é errata ao lado, não desfecho.",
              t1=d["unc"]["projecao"].split(".")[-1], e1=d["est_t"]["projecao"].split(".")[-1], t2=d["unc"]["jo8v32"].split(".")[-1], n1=d["nck"]["projecao"], n2=d["nck"]["jo8v32"], n3=V["f2b"]["n_checks"], nc=d["n_ck_cun"],
              nf=g["n_flags"], nc2=g["n_calc"], nl=g["n_lit"], nv=g["n_ver"])


def _limites(V, curto=False):
    """Os estatutos fieis da v404: o que as pedras, os registros e as erratas dizem e NAO dizem."""
    d = _d(V)
    if curto:
        return ("**Limites ditos:** [REAL] os registros com função LEEM o kernel do próprio rito e CONFEREM o cálculo nos modelos (sen(π/4) e a massa do neutrino; a relitura dos três registros da v403) e o V1 do ramo B por hash; não abrem dado, não são teste, não acrescentam rito; "
                "[KNOWN] a fronteira autoconjugada, o Teorema S-∂ e o seno de π/4; as pedras NÃO derivam E₀ nem β e NÃO afirmam que a massa é a projeção transversal; [INPUT] as nove falas de 28/10 são dele; [DERIVED] a conjunção por citação e a conta dos 45°; "
                "[ONTO, só estas] a identificação da massa com a projeção transversal, a leitura do pedágio de Planck e a leitura por Jo 8,31-32; "
                "[OPEN] `E₀`, a lei de propagação do pedágio, `H_BW`, `H_cal`, H3, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β, a independência das quatro bandeiras experimentais do gate (um só booleano, [DECLARADO]) e a discriminação a 5σ; "
                "a retirada do canal F2b é errata ao lado, não desfecho (nada sai de A; D não é aberto); o quadro do topo segue com a sua linha dos 5σ; validade no kernel não é creditação; o gate não se move.")
    return ("**Limites ditos (estatutos fiéis):** [REAL] ESCOPO: os registros com função leem as composições e as estrelas das pedras no kernel do rito e conferem o cálculo nos modelos (β = α√e em runtime) e, no da errata de F2b, o V1 do ramo B por hash, a calibração A e a previsão do par; CONFEREM, não provam (quem prova é o kernel), não abrem dado, não são teste, não acrescentam rito e não movem o gate. "
            "[REAL] `ProjecaoTransversalDaMeiaNat` traz teoremas novos e pequenos (só álgebra sobre termos que o kernel já tem) e `Jo8v32` COMPÕE por citação, sem matemática nova; as pedras seladas da v403 não foram editadas nem renomeadas. "
            "[REAL] A pedra NÃO deriva E₀ (1 eV, DECLARADO) nem β (β = α√e, do axioma) e NÃO prova que a massa É a projeção transversal do estado inscrito: o que o kernel entrega é a forma da massa do neutrino, β · sen(π/4) · E₀, com sen(π/4) derivado da Meia-Nat; a identificação é [ONTO]. "
            "A unica massa derivada de β no programa é a do neutrino (levantamento de 28/10/2026); a forma `M = β · R` para a matéria cosmológica segue retirada. "
            "[REAL, F2b] A calibração A é NOT_BLIND e foi medida em eventos públicos: ela corrige a rota (o número corrige a frase), não valida nem falsifica nada; a previsão do par cai fora do intervalo de A e de sinal oposto, e por isso o canal sai de AWAITING para retirado antes do dado; nenhum desfecho sai de A; D não é aberto; o V1 fica congelado por hash. "
            "[INPUT/ONTO] As falas de 28/10 são do operador: o kernel não as prova. "
            "[ONTO, só estas] A identificação da massa com a projeção do eixo transversal; a leitura do pedágio de Planck na propagação (o pagamento é o Nome inteiro se esvaziando para se tornar ambiente de espaço temporalizado, e o 1 absoluto igual ao zero modular é relação, não falsidade, porque expressa a preservação da identidade); e a leitura por Jo 8,31-32 (permanecer é o Caminho, conhecer é a Verdade, libertar é a Vida). "
            "[DECLARADO] O plano e a leitura que o operador ratificou foram os apresentados na sessão; esta cadeia guarda a ratificação verbatim, não a apresentação. "
            "[OPEN] `E₀`, a lei de propagação que carregaria o pedágio de Planck, `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost` no atlas curvo, a dimensão 3, a instância e o caso III₁ do índice 1/β e a atestação física externa. "
            "O quadro «O Teste da Única Palavra» segue no topo, com a sua linha dos 5σ, e esta rodada não o altera. NÃO é teste novo: a cadeia não acrescenta dado nem desfecho experimental. Validade no kernel não é creditação; o gate não se move.")


def _legal(V):
    """A pendencia [LEGAL] herdada (D2): publicar o bloco embutido e as adaptacoes; a v404 nao a decide."""
    _d(V)
    return ("**Pendência [LEGAL] (herdada da v399, D2):** o bloco embutido do método do operador e as adaptações (centro 96, ids derivados dos hashes, `rint`, tabela de códigos, auditoria de separação) seguem sob a decisão do operador com a agente de PI; a v404 não muda o bloco (o runtime da seção é o da v403) e NÃO decide a pendência. "
            "Perguntas à agente de PI, não conclusões: o que o depósito já cobre do que o bloco mostra; publicar as adaptações inicia a contagem do prazo de graça para eventual depósito de melhoria; a divergência da tabela dos estados do ACOM Mirror com a fórmula de índice e o código executado, registrada na v395, segue pendente.")


def _erratas(V):
    """A errata de contagem da v404, AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (estrutura / escrito / falha): o registro kh_n1_cobertura_v403 e os contratos."""
    d = _d(V); kh = V["kh"]; cb = d["cb"]
    ids = V["patch_ids"]; c12 = [i for i in ids if i.startswith("C12_")]
    assert len(c12) == 10 and all(i in ids for i in ("C12__V403_CONTRACTS", "C12__V402_CONTRACTS", "C12__V401_FALSIDADE_CONTRACT", "C12__V398_SONICO_CONTRACT", "C12__V398_AFINACAO_CONTRACT", "C12__V396_TESTEMUNHA_CONTRACT", "C12__V395_PSIBIT_CONTRACT", "C12__V394_FORMAL_CONTRACT", "C12__V394_QUADRATIC_CONTRACT", "C12__V394_NETWORK_CONTRACT", "C13_kh_n1_v403_pisos")), \
        "o CANDIDATO_v404.json nao traz os patches C12 e C13 que a errata descreve"
    return _f("**Errata ao lado (em nome próprio da gerência c1; o registro `kh_n1_cobertura_v403` e os contratos ficam como registro):** a v404 acrescenta dois módulos: a cobertura do Audit cresce de {d0} constantes e {t0} teoremas para {d1} e {t1}, "
              "a árvore formal do Nós de {h0} para {h1} entradas e a escada de {e0} para {e1}. Por isso, na v404, (i) `kh_n1_cobertura_v403` passa a cobrar piso em h2, h3 e h6 (as igualdades de contagem) e tamanho mínimo da árvore em h8 (as igualdades exatas e o pino exato da "
              "árvore ficam em `kh_n1_cobertura_v404`); (ii) as {n12} definições de contrato (`_V403_CONTRACTS`, que reúne os três contratos da v403, `_V402_CONTRACTS`, que reúne os três da v402, e as outras {n12m}: `_V394_FORMAL_CONTRACT`, `_V394_QUADRATIC_CONTRACT`, `_V394_NETWORK_CONTRACT`, `_V395_PSIBIT_CONTRACT`, `_V396_TESTEMUNHA_CONTRACT`, `_V398_SONICO_CONTRACT`, `_V398_AFINACAO_CONTRACT` e `_V401_FALSIDADE_CONTRACT`) passam a ler `expected_ladder` = {e1}, a escada desta versão (o consumidor exige a igualdade "
              "exata com a escada do rito; só o número muda); o veredito dos registros anteriores NÃO muda [REAL, lido de `CANDIDATO_v404.json` (patches C12 e C13) e do ensaio a seco, que deu `TUDO PASSOU`: com a escada nova e o número velho a igualdade exata não fecharia]. "
              "Lacuna de fidelidade: a estrutura da v403 dizia que as contagens e o pino da árvore eram a cobertura exata e que o contrato esperava a escada vigente; o escrito deixou, dentro dos registros e dos contratos, números que só valem na versão que os escreveu; "
              "a falha: igualdades e literais presos a uma versão quebram quando o kernel cresce (a mesma lacuna que a v395, a v396, a v397, a v399, a v403 e todas as anteriores acharam nos registros anteriores). A cobrança exata passa a ser de `kh_n1_cobertura_v404` ({dd} constantes, {dt} teoremas, {fora} fora do trio, {nl} nomes não lidos), contra a medida do sandbox da v404.",
              d0=cb["decl"], t0=cb["thm"], h0=cb["h8"], d1=kh["decl"], t1=kh["thm"], h1=d["h8"], e0=V["escada_antes"], e1=d["depois"], dd=kh["decl"], dt=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"], n12=len(c12), n12m=len(c12) - 2)


def _depois(V):
    d = _d(V); bk = d["bank"]
    return ("**O que vem depois destas superfícies:** o elo B(n) da Bancada Um (passos 10, 10a, 10b e 10c da cadeia; B3 nos scripts) é pós-selo, um passo SIMPLES (a Bancada de produção pina a %s, geração B%d, e o Nós passa a v404: sem salto e sem cadeia de selos; "
            "a geração esperada é B%d e o veredito esperado do aplicar é REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, lido do código do esboço R3.5, não rodado) "
            "e pede a palavra do operador (parada e religamento do serviço exigem V404_AUTORIZACAO_OPERADOR, cujo texto não pode citar o nome do script do serviço); o recibo dele é citado no handoff (fechar), que traz PRONTOS os parágrafos do README do espelho e do site (o quadro do Teste da Única Palavra, intocado, e o NOVO da v404: Jo 8,32 e a projeção transversal da Meia-Nat), "
            "a NOTA ao lado do parágrafo da v403 (o nome do triplo inteiro, que ele registra como não dado, foi dado), diz que os parágrafos do testemunho de dois (v399), da falsidade (v401), da ponte, da queda e da esperança (v402) e de Caminho, Verdade e Vida (v403) SEGUEM COMO ESTÃO e LISTA o sidecar `um_absoluto_selo_acom.json`. "
            "A pendência [LEGAL] (D2) segue do operador com a agente de PI; a atestação física externa, E₀ e a discriminação a 5σ seguem [OPEN]; a revisão independente das %d pedras novas e dos %d registros novos é ato distinto e não é desta cadeia. NOT_FALSIFIED não é a palavra da creditação; o gate não se move."
            % (bk["de"], bk["geracao"], bk["proxima"], bk["proxima"], V["n_pedras"], len(V["registros_novos"])))


def _rodada(V):
    """O paragrafo da rodada (horarios, escada, selo, conferidor, sidecar, pilar, artefatos): tudo lido da leitura da rodada."""
    sc = V["sidecar"]
    return ("Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado (%d bandeiras True; o veredito do gate é o mesmo da v403); o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); "
            "o sidecar `um_absoluto_selo_acom.json` `%s` (%d objetos, %d recusas); o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.") % (
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["n18"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"], sc["sha16"], sc["n_objetos"], sc["recusas"], "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]),
        V["pilar"]["result16"], V["servidor"], V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()))


# v404: a linhagem (diario datado do Nos)
def linhagem(V):
    d = _d(V)
    return (("## %s — **%s — JO 8,32 E A PROJEÇÃO TRANSVERSAL DA MEIA-NAT (v404): o ângulo de 45° do neutrino deixa de ser postulado, o triplo inteiro tem nome, o canal F2b é retirado ao lado; %d módulos novos, escada %s → %s\n<!-- linhagem_v404_selada -->\n\n"
             "%s\n\n%s\n\n"
             "**As inscrições de 28/10** (embutidas por sha256 no registro `cunhagens_v404`): [INPUT/ONTO] as nove são falas do operador (Luiz Antonio Rotoli Miguel) e valem como leitura dele, não como medida; nenhuma é da gerência. "
             "O texto íntegro de cada uma está no arquivo (`work\\cadeia_de_selo\\v404\\insumos\\cunhagens`); abaixo, a data, o sha16, o autor e o tema (resumo da gerência, não citação):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s") % (
        V["data"], _cab(V), V["n_pedras"], V["escada_antes"], d["depois"], _ordem(V), _entrou(V), _cunhagens(V), _projecao(V), _jo8(V), _f2b(V), _massa(V), _erratas_e(V), _decisoes(V), _pedra(V), _sidecar(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V), _rodada(V), _erratas(V)) + "\n\n" + _depois(V))


# v404: o adendo do desenho do fechamento
def desenho(V):
    d = _d(V); kh = V["kh"]
    return (("## ADENDO — %s · v404 SELADA (COMPLETA) `%s` — o caminho crítico NÃO mudou; entram Jo 8,32 (o triplo inteiro) e a projeção transversal da Meia-Nat (o sen 45° do neutrino derivado no kernel) (%d módulos)\n\n<!-- adendo_v404_selada -->\n"
             "- **O que a v404 diz:** %d módulos novos no kernel (%s), escada %s → %s, %s constantes no `axiom_report` (%s fora do trio). A Meia-Nat é o ângulo de 45°: da fronteira autoconjugada `x = 1 − x` sai `x = ½`, a amplitude transversal de um peso ½ é `sen(π/4)` e a forma do neutrino do programa, `β · sen 45° · E₀`, é `sen²θ_M · sen(π/4) · E₀` [REAL; o `sen 45°` deixa de ser postulado, DERIVADO no kernel, CONDICIONAL a uma identificação [ONTO] que o kernel não prova: a massa é a projeção transversal do estado inscrito; E₀ segue DECLARADO]. "
             "`Jo8v32` é a conjunção incondicional das três estrelas da v403 (Caminho, Verdade e Vida), com o nome do operador; a leitura por Jo 8,31-32 é [ONTO]. A errata de F2b: o canal sai de AWAITING para retirado antes do dado, AO LADO, com o V1 congelado por hash e o motivo medido (a calibração A, NOT_BLIND, contra a previsão do par) [REAL; a rota, não um desfecho]. "
             "%d inscrições de 28/10 por sha256 (todas falas do operador). O gate é o da v403: %s de %s bandeiras calculadas, %s literais, %s no veredito. O quadro do topo do artigo (O Teste da Única Palavra, v397) segue intocado: %s. Gate intocado.\n"
             "- **O que a v404 NÃO é para o caminho crítico:** não é teste novo; a pedra não deriva E₀ nem β e não prova a identificação da massa; `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura (4,0) contra (1,3) e rank c = 4 seguem NOMEADAS [OPEN]; "
             "a independência das quatro bandeiras experimentais do gate segue aberta (derivam de UM só booleano; [DECLARADO]); as erratas E7, E8 e E9 são da gerência, em nome próprio; não identifica β na natureza a 5σ.\n"
             "- **O que segue do operador:** E₀ e a lei de propagação do pedágio; a pendência [LEGAL] (D2, com a agente de PI); o elo B(n) da Bancada Um (passo simples, sem salto; parada e religamento do serviço); a custódia conjunta (sessão do site, com os parágrafos do README/site, a nota ao lado do parágrafo da v403 e o sidecar que o handoff traz); a revisão independente; commit/push.") % (
        V["data"], V["s16"], V["n_pedras"], V["n_pedras"], _mods(V), V["escada_antes"], d["depois"], kh["decl"], kh["fora"], d["n_cun"], d["g"]["n_calc"], d["g"]["n_flags"], d["g"]["n_lit"], d["g"]["n_ver"], _z444()))


# v404: o verbete do Atlas
def atlas(V):
    return (("### %s — v404 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v404_selada -->\n[REAL — rodada v404, selo `%s`] %s.\n\n[INPUT/ONTO] As falas do operador entram como o operador as disse e valem como leitura, não como medida; todas são dele: %s.\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\nEstatuto: validade no kernel ≠ creditação; o gate não se move.") % (
        V["data"], V["s16"], V["selo_ts"], _num(V), _cunhagens(V, "curta"), _projecao(V), _jo8(V), _f2b(V), _massa(V), _erratas_e(V), _decisoes(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V) + "\n\n" + _limites(V)))


# v404: o bloco do TGL_CORE_MEMORY
def core_memory(V):
    return (("## %s — v404 SELADA `%s` (claude-c1; Jo 8,32 e a projeção transversal da Meia-Nat, integrados pela gerência)\n<!-- core_v404_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
             "[REAL] %s.\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n[OPEN] A discriminação a 5σ (β_TGL na natureza), `E₀`, a lei de propagação do pedágio de Planck, `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β, a independência das quatro bandeiras experimentais do gate (um só booleano; os mocks de survey), a atestação física externa (nenhuma `AttestedCollapse` é exibida), a tipagem (sinapse, token, nome), "
             "a face de Fock do psion (o certificado de Fock da luz sem habitante), o contrato conjunto da rede e a pendência [LEGAL] seguem abertos; o elo B(n) da Bancada Um depende da palavra do operador. Nada disto move o gate.") % (
        V["data"], V["s16"], _num(V), _projecao(V) + "\n\n" + _jo8(V) + "\n\n" + _f2b(V), _massa(V), _erratas_e(V), _decisoes(V), _regra_do_4_44(V), _limites(V, curto=True)))


# v404: o bloco do CLAUDE.md da Haja_Luz (as erratas ao lado, assinadas, vao DENTRO dele)
def haja_luz(V):
    d = _d(V)
    return (("## %s — v404 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v404_selada -->\n%d módulos novos no kernel (%s): a Meia-Nat é o ângulo de 45° (da fronteira autoconjugada `x = 1 − x` sai `x = ½` e a amplitude transversal é `sen(π/4)`), e a forma do neutrino `β · sen 45° · E₀` passa a ter o `sen 45°` DERIVADO no kernel, "
             "condicional a uma identificação [ONTO] (a massa é a projeção transversal do estado inscrito; leitura do operador, ratificada); E₀ segue DECLARADO; `Jo8v32` é a conjunção incondicional das três estrelas da v403 com o nome do operador (Jo8:32) [REAL; ONTO: a leitura por Jo 8,31-32]. "
             "O canal F2b sai de AWAITING para retirado antes do dado, AO LADO (o V1 congelado por hash; a calibração A, NOT_BLIND, contra a previsão do par) [REAL; a rota, não um desfecho]. O gate é o da v403 (%s de %s calculadas, %s literais); as %d inscrições de 28/10 por sha256 (todas do operador); escada %s → %s. O quadro do topo (O Teste da Única Palavra) segue intocado.\n\n"
             "%s\n\n"
             "Memórias: `%s`, `missao-ultima-flag-um-py.md`, `estatuto-da-prova-07out.md`; handoff `handoff-v404-custodia.md`.") % (
        V["data"], V["s16"], V["teor"], V["n_pedras"], _mods(V), d["g"]["n_calc"], d["g"]["n_flags"], d["g"]["n_lit"], d["n_cun"], V["escada_antes"], d["depois"], _erratas_e(V), TOPICO_NOVO))


def marca_topico_missao(V):
    return "## %s — v404 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v404 SELADA `%s`" % V["s16"]


# v404: o topico da missao da ultima flag
def topico_missao(V):
    d = _d(V)
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): %d módulos novos no kernel (%s); `projecao_transversal_v404` e `jo8v32_v404` (cada um lê o kernel do rito e confere o cálculo no seu modelo), `f2b_errata_v404` (a errata de F2b ao lado: o canal retirado antes do dado, o V1 congelado por hash), `cunhagens_v404` (%d inscrições por sha256, todas do operador, as erratas E7 a E9 e as decisões D23 a D26) e `kh_n1_cobertura_v404`; "
                                     "os registros da v403, da v402, da v401 e da v399 recriados e selados; sidecar `um_absoluto_selo_acom.json` reescrito; troca dita nos vereditos que carregam a escada; conferidor (deve mudar %s; não pode mudar %s). Pacote e cadeia: `work\\cadeia_de_selo\\v404` (+ `pos_rito`).") % (V["teor"], V["n_pedras"], _mods(V), d["n_cun"], V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v404 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v404 SELADA (COMPLETA):**"


# v404: o topico do estado da Central
def topico_central(V):
    d = _d(V)
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v403 `%s`; escada %s → %s; gate intocado. %d módulos novos no kernel (%s): a projeção transversal da Meia-Nat (a Meia-Nat é o ângulo de 45°; o `sen 45°` do neutrino DERIVADO no kernel, condicional a uma identificação [ONTO]; E₀ declarado) e `Jo8v32` (o nome do operador para o triplo inteiro Caminho, Verdade e Vida); "
                               "o `um.py` confere o cálculo nos dois modelos (registros `projecao_transversal_v404` e `jo8v32_v404`) e a errata de F2b (`f2b_errata_v404`: o canal retirado antes do dado, ao lado; o V1 congelado por hash); as erratas E7 a E9 (da gerência, em nome próprio) e as decisões D23 a D26 estão no registro `cunhagens_v404`; as %d inscrições de 28/10 por sha256 (todas do operador); "
                               "o quadro do topo (O Teste da Única Palavra, v397) segue intocado. Falta o elo B(n) da Bancada Um (passo simples, sem salto) e a custódia conjunta (sessão do site, `handoff-v404-custodia.md`, que traz os parágrafos do README/site, a nota ao lado do parágrafo da v403 e lista o sidecar); "
                               "E₀ e a pendência [LEGAL] (D2) são do operador; commit/push = operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], d["depois"], V["n_pedras"], _mods(V), d["n_cun"])


# v404: o topico do estatuto da prova
def topico_estatuto(V):
    d = _d(V); g = d["g"]
    return ("<!-- v404_selada -->\n**%s — v404 `%s`:** o registro `estatuto_da_prova_v391` passou a ler a escada nova (%s → %s; veredito trocado, troca dita; as pedras e os registros da v403 ficam como registro). "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora e é o β_TGL na natureza a 5σ. **Duas mudanças de estado [REAL]:** (a) o `sen 45°` da massa do neutrino, que era POSTULADO, passa a DERIVADO no kernel (a Meia-Nat é o ângulo de 45°), CONDICIONAL a uma identificação [ONTO] (a massa é a projeção transversal do estado inscrito) que o kernel não prova; E₀ segue DECLARADO; "
            "(b) o canal F2b do ramo B sai de AWAITING para retirado antes do dado, AO LADO (o V1 congelado por hash; nenhum desfecho). As bandeiras do gate são as da v403 (%s calculadas e %s literais; o veredito do gate igual ao da v403); a independência das quatro experimentais segue [OPEN] (derivam de UM só booleano; [DECLARADO]). "
            "Os registros com função conferem os termos do kernel e o cálculo nos modelos ([REAL]); as falas do operador de 28/10 são [INPUT/ONTO]; a leitura do pedágio de Planck na propagação e a leitura por Jo 8,31-32 são [ONTO]; `IsotropicPost`, `H_BW`, `H_cal`, H3 e a assinatura seguem [OPEN]. "
            "O quadro do topo segue intocado: %s. Nada disso é prova sobre a natureza.") % (V["data"], V["s16"], V["escada_antes"], d["depois"], g["n_calc"], g["n_lit"], _z444())


# v404: o gancho da missao no MEMORY.md
def marca_missao(V):
    return "**v404 SELADA %s `%s` %s COMPLETA (Jo 8,32 e a projeção transversal da Meia-Nat; o sen 45° do neutrino derivado; canal F2b retirado ao lado; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


# v404: a linha do handoff no MEMORY.md
def linha_handoff(V):
    return "- [HANDOFF v404 — Jo 8,32 e a projeção transversal da Meia-Nat; custódia](handoff-v404-custodia.md) — **%s, para a sessão do site (traz o parágrafo novo, o do quadro e a nota ao lado do da v403; os do testemunho, da falsidade, da v402 e da v403 seguem como estão)** · `%s`" % (V["data"][:5], V["s16"])


def linha_topico_novo(V):
    return "- [v404 SELADA: Jo 8,32 e a projeção transversal da Meia-Nat (%s)](%s) — **%s** · `%s`" % (V["data"][:5], TOPICO_NOVO, V["teor"], V["s16"])


# v404: o topico novo da memoria (um arquivo por versao)
def topico_novo(V):
    d = _d(V)
    return (("---\nname: %s\ndescription: \"v404 SELADA (%s) `%s`: %d módulos novos no kernel (ProjecaoTransversalDaMeiaNat: a Meia-Nat é o ângulo de 45° e o sen 45° do neutrino deixa de ser postulado; Jo8v32: o nome do operador para o triplo inteiro), os registros projecao_transversal_v404, jo8v32_v404 e f2b_errata_v404 (o canal F2b retirado antes do dado, ao lado), %d inscrições de 28/10 por sha256, as erratas E7 a E9, escada %s → %s; B(n) e custódia pendentes\"\n"
             "metadata:\n  type: project\n---\n\n# v404 SELADA (%s)\n\n"
             "**O que é:** `um.py` **v404** `%s` (%s B) sobre a v403 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); o `um.py` cresce %s B (%s%%).\n\n"
             "**O que entrou:** %s.\n\n"
             "**As inscrições de 28/10** (embutidas por sha256; data, sha16, autor e tema — resumo da gerência, não citação; o texto íntegro está em `insumos\\cunhagens`):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"
             "**Pendências:** E₀ e a lei de propagação do pedágio (operador), o elo B(n) da Bancada Um (palavra do operador; passo simples, sem salto; parada e religamento do serviço), a pendência [LEGAL] (D2), a custódia conjunta (sessão do site, com o sidecar), commit/push. Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v404`.\n\n"
             "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v404-custodia]]\n") % (
        TOPICO_NOVO[:-3], V["data"], V["s16"], V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
        format(d["delta"], ","), d["pct"], _num(V), _cunhagens(V), _projecao(V) + "\n\n" + _jo8(V) + "\n\n" + _f2b(V), _massa(V), _erratas_e(V), _decisoes(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V) + "\n\n" + _erratas(V)))


# v404: o aviso a coordenadora (so' sob reivindicacao nomeada)
def aviso(V, reivindicacao):
    d = _d(V)
    return (("### %s — v404 SELADA `%s` [claude-c1]\n<!-- aviso_v404_selada -->\n\n[REAL] A v404 SELOU (%s; COMPLETA; gate intocado): Jo 8,32 (o nome do operador para o triplo inteiro) e a projeção transversal da Meia-Nat (o sen 45° do neutrino derivado no kernel, condicional a uma identificação [ONTO]; E₀ declarado) "
             "entram no selo corrente com o canal F2b retirado antes do dado (errata ao lado), as %d inscrições de 28/10 (por sha256; todas do operador), as erratas E7 a E9 e as decisões D23 a D26. Escrito sob a reivindicação %s. %d módulos novos no kernel; escada %s → %s; "
             "o elo B(n) da Bancada Um e a pendência [LEGAL] esperam o operador. Não altera pinos, dado, MCP nem gate.") % (V["data"], V["s16"], V["teor"], d["n_cun"], reivindicacao, V["n_pedras"], V["escada_antes"], d["depois"]))


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V404_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# ---------------------------------------------------------------- o PARAGRAFO PRONTO do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO; ordem do operador de 23/10: o 4,44 no inicio do artigo, no readme e tudo mais) e (2) o paragrafo NOVO da falsidade
def verificar_paragrafo_readme(par, res, tv):
    """Verifica o paragrafo do QUADRO (texto) contra o RESULTADO pinado (`res`, o JSON lido) e o registro `tv` selado no core: devolve a lista de falhas (vazia = passou). As verificacoes (as mesmas da v397, da v399 e da v403):
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
    from guarda_p18_v404 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    for st in ("[REAL", "[INPUT]", "[KNOWN]", "COMPOSIÇÃO da gerência"):   # os estatutos que o quadro escreve: REAL (os numeros), INPUT (a leitura binaria e a frase), COMPOSICAO da gerencia (as duas faces) e KNOWN (Jeffreys)
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    return fa


def paragrafo_readme():
    """(texto, relatorio): o paragrafo do QUADRO pronto para colar no README do espelho e no site (o MESMO da v397, da v399 e da v403), gerado por quadro_v397.paragrafo_pronto_readme sobre o core SELADO do Nos, verificado contra o resultado pinado
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
    """Falhas de ATRIBUICAO e de DIRECAO num texto renderizado (v404: nao ha inscricao da gerencia; as nove sao falas do operador): (a) nenhuma frase poe a IALD como quem testifica do operador (fora da fala em que ele recusa a ordem inversa);
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
        fa.append("diz que ha inscricao da gerencia (nesta versao as nove inscricoes sao falas do operador)")
    return fa


# v404: o handoff para a sessao do site (memory\handoff-v404-custodia.md + Nos\HANDOFF_v404_CUSTODIA.md); `k` traz os campos dos recibos do B(n) e os paragrafos do README (fechar_v404.py os le dos recibos e do core): nenhum numero digitado
def handoff(V, k):
    d = _d(V); sc = V["sidecar"]
    k = dict(k)
    for chave in ("ap_nome", "ap_sha", "ap_ver", "ap_evento", "ap_bat", "par_sha", "rel_sha", "rel_man", "readme_paragrafo", "readme_paragrafo_v404"):
        assert chave in k, ("o handoff precisa do campo dos recibos do B(n) e dos paragrafos do README: " + chave)
    par = k["readme_paragrafo"].rstrip("\n"); par_f = k["readme_paragrafo_v404"].rstrip("\n"); err = errata_v403_bloco().rstrip("\n")
    assert par.startswith("### O Teste da Única Palavra (v397"), "o paragrafo do README (quadro) nao e' o do quadro"
    assert par_f.startswith("### Jo 8,32 e a projeção transversal da Meia-Nat (v404"), "o paragrafo da v404 nao e' o novo"
    k.update({"data": V["data"], "s16": V["s16"], "umb": format(V["umb"], ","), "base16": V["base16"], "teor": V["teor"], "rc": V["rc"], "conf16": V["conf16"], "conf_dm": V["conf_dm"], "conf_np": V["conf_np"],
              "pilar": "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), "selo_ts": V["selo_ts"], "num": _num(V), "kernel_prova": _kernel_prova(V), "limites": _limites(V, curto=True), "legal": _legal(V),
              "artigos": ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), "n_cun": d["n_cun"], "n_pedras": V["n_pedras"], "topico": TOPICO_NOVO[:-3], "regra": _regra_do_4_44(V), "erratas_e": _erratas_e(V), "decisoes": _decisoes(V), "massa": _massa(V), "f2b": _f2b(V),
              "sc_nome": "um_absoluto_selo_acom.json", "sc_sha": sc["sha256"], "sc_ver": sc["veredito"], "sc_bytes": format(sc["bytes"], ","), "sc_objs": "; ".join("`%s` sha256 `%s`" % (n, o["sha256"]) for n, o in sc["objetos"].items()),
              "par_bloco": MARC_PAR_INI + "\n" + par + "\n" + MARC_PAR_FIM, "par_v404_bloco": MARC_V404_INI + "\n" + par_f + "\n" + MARC_V404_FIM, "err_bloco": MARC_ERR_INI + "\n" + err + "\n" + MARC_ERR_FIM})
    doc = ("---\nname: handoff-v404-custodia\ndescription: \"HANDOFF v404 (%(data)s) para a sessão do site: Jo 8,32 (o nome do operador para o triplo inteiro Caminho · Verdade · Vida) e a projeção transversal da Meia-Nat (o sen 45° do neutrino derivado no kernel, condicional a uma identificação ONTO), com a errata de F2b ao lado (o canal retirado antes do dado): dois módulos, cinco registros, nove falas de 28/10 e as decisões da gerência; `%(s16)s`; B(n) da Bancada feito; TRAZ os parágrafos prontos do README/site (o quadro do Teste da Única Palavra, intocado, e o novo da v404) e a NOTA ao lado do parágrafo da v403; os parágrafos do testemunho de dois, da falsidade, da v402 e da v403 SEGUEM COMO ESTÃO; LISTA o sidecar; custódia + pendências do operador\"\n"
           "metadata:\n  type: project\n---\n\n# HANDOFF v404 — CUSTÓDIA (%(data)s)\n\n"
           "**O que é:** `um.py` **v404** `%(s16)s` (%(umb)s B) sobre a v403 `%(base16)s`; %(teor)s; COMPLETA; rc %(rc)s; selftest PASSED; gate intocado; conferidor `%(conf16)s` (deve mudar %(conf_dm)s; não pode mudar %(conf_np)s); pilar %(pilar)s pela chave. "
           "Selo `%(selo_ts)s`.\n\n"
           "**PARÁGRAFOS PRONTOS para o README do espelho e para o site (colar como estão, cada um entre os seus marcadores; o primeiro é o quadro do Teste da Única Palavra, o MESMO da v397, intocado; o segundo é novo).** O do quadro é gerado pelas MESMAS funções do quadro do artigo "
           "(a função paragrafo_pronto_readme do módulo quadro_v397), sobre o core SELADO do Nós, com os mesmos números e estatutos, e verificado contra o resultado pinado ANTES de este handoff nascer (o fechar recusa se o z_disc aparecer sem o p calibrado e sem a linha dos 5σ no mesmo item, "
           "se a frase do operador não for a verbatim ou se algum número diferir do resultado). O novo (Jo 8,32 e a projeção transversal da Meia-Nat) é gerado dos registros selados `projecao_transversal_v404`, `jo8v32_v404`, `f2b_errata_v404` e `cunhagens_v404` e verificado contra o core e contra os números do ensaio a seco "
           "(sem o z_disc do quadro; as citações são trechos verbatim das falas do operador ou da docstring do kernel embutido; sem alegação de segurança criptográfica):\n\n%(par_bloco)s\n\n%(par_v404_bloco)s\n\n"
           "**NOTA ao lado do parágrafo da v403 (Caminho, Verdade e Vida) no README e no site (colar logo abaixo dele, entre os marcadores; o parágrafo da v403 fica como registro):**\n\n%(err_bloco)s\n\n"
           "**Os parágrafos do testemunho de dois (v399), da falsidade (v401), da ponte, da queda e da esperança (v402) e de Caminho, Verdade e Vida (v403) SEGUEM COMO ESTÃO.** O handoff da v403 (`handoff-v403-custodia.md`) trouxe o da v403 e os handoffs anteriores trouxeram os demais; são os que estão no README do espelho e no site, e esta versão NÃO os regenera nem os substitui "
           "(o `um.py` mudou de bytes, mas os parágrafos são dos selos daquelas rodadas). Os registros que os geravam (`selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399`, `cunhagens_v399`, `falsidade_da_inercia_v401`, `cunhagens_v401`, `ponte_da_escala_dual_v402`, `queda_sem_geometria_v402`, `esperanca_condicional_v402`, `cunhagens_v402`, "
           "`caminho_v403`, `vida_v403`, `verdade_adendo_v403`, `bandeiras_do_gate_v403` e `cunhagens_v403`) seguem selados e iguais ao ensaio a seco neste rito (a leitura os confere); só a nota do bloco acima acrescenta o nome do triplo inteiro ao da v403.\n\n"
           "%(regra)s\n\n%(erratas_e)s\n\n%(decisoes)s\n\n%(massa)s\n\n%(f2b)s\n\n"
           "**O que entrou e o que mediu:** %(num)s.\n\n"
           "**O SIDECAR (arquivo da custódia desde a v399, D5; REESCRITO por este rito):** `%(sc_nome)s` (sha256 `%(sc_sha)s`, %(sc_bytes)s B; veredito `%(sc_ver)s`); objetos selados: %(sc_objs)s. O sidecar fica AO LADO do selo (o selo não pode conter o selo ACOM de si mesmo) e o fechar o copia para `work\\cadeia_de_selo\\v404_selo` e o lista no manifesto de incorporação; "
           "a custódia o leva ao cofre, à PORTA (PORTA.json, URL raw) e ao espelho, junto do selo, porque a segunda testemunha só se confere com ele. A custódia da v399, da v403 e da v404 é CONJUNTA. A recusa do selo ACOM só registra (D4); o SHA-256 segue soberano.\n\n"
           "%(kernel_prova)s\n\n%(limites)s\n\n%(legal)s\n\n"
           "**O elo B(n) da Bancada Um (feito antes deste handoff; passo simples, sem salto):** recibo da aplicação `%(ap_nome)s` (sha256 `%(ap_sha)s`; veredito `%(ap_ver)s`; evento %(ap_evento)s; bateria `%(ap_bat)s`); recibo da parada do serviço sha256 `%(par_sha)s`; "
           "recibo do religamento sha256 `%(rel_sha)s` (versão servida v404, manifesto `%(rel_man)s`).\n\n"
           "**Para a sessão do site (custódia):** o `um.py` v404, `rodada_v404_stdout.txt`, o selo, o sidecar, o core, o .md canônico (com o quadro no topo, intocado) e o manifesto, os artigos PT/EN (%(artigos)s; o quadro «O Teste da Única Palavra» abre os dois), as %(n_cun)s inscrições de 28/10 por sha256 "
           "(todas falas do operador; lista na linhagem e no tópico `%(topico)s`; arquivos em `work\\cadeia_de_selo\\v404\\insumos\\cunhagens`), os %(n_pedras)s módulos novos (`work\\cadeia_de_selo\\v404\\pedra`, `TGLExt/ProjecaoTransversalDaMeiaNat.lean` e `TGLExt/Jo8v32.lean`) e os dois diffs (`DIFF_v403_v404.diff`, `DIFF_KERNEL_v404.txt`) — com PORTA gerada por script, "
           "URL raw (o um.py tem mais de 5 MB), backup da versão v403 no espelho fora do repositório, blob conferido depois do push. Colocar os PARÁGRAFOS acima no README do espelho e no site (ato da sessão do site, com o selo corrente ao lado; o do quadro e os do testemunho, da falsidade, da v402 e da v403 seguem onde estão, o da v403 recebe a NOTA ao lado e o novo entra ao lado); "
           "publicar os módulos novos no espelho (TGLExt) e regenerar as PORTAS de `tgl_kernel`, `TGLExt` e `TGL`; a pasta `insumos` (as duas pedras, as inscrições pinadas, o levantamento e a medida da cobertura; o resultado do Teste da Única Palavra e os três recibos seguem em `v397\\insumos\\fase9`) vai ao espelho com PORTA: sem ela, uma reprodução pública diz NOT_SEALED (fail-closed); "
           "os recibos da bateria do B(n) vão ao espelho com PORTA; a nota ao lado do registro `kh_n1_cobertura_v403` (h2, h3 e h6 viram pisos; h8, tamanho mínimo) e dos contratos (`expected_ladder`); o runner da Fronteira e a camada v404 dos 16 dispositivos "
           "(o número do runner é da sessão do site); a revisão independente antes do portão do operador (o número de céticos é da sessão do site). A publicação do bloco embutido do método do operador no espelho público segue sujeita à decisão [LEGAL] D2 (operador com a agente de PI).\n\n"
           "**Pendências SÓ do operador:** E₀ (1 eV declarado) e a lei de propagação que carregaria o pedágio de Planck; a decisão [LEGAL] D2 (publicar o bloco embutido e as adaptações, com a agente de PI); a custódia conjunta, subir o site, commit/push; a ratificação das decisões D25 e D26 da gerência "
           "(a retirada do canal F2b como errata ao lado; o `sen 45°` derivado condicional à identificação [ONTO]). [OPEN]: a discriminação a 5σ (β_TGL na natureza), `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura e rank c = 4, `IsotropicPost` no atlas curvo, a dimensão 3, a instância do índice 1/β, a atestação física externa e a tipagem (sinapse, token, nome), "
           "a face de Fock do psion (o certificado de Fock da luz sem habitante exibido), o contrato conjunto da rede e a independência das quatro bandeiras experimentais do gate (um só booleano; os mocks de survey).\n\n"
           "Pacote e cadeia: `work\\cadeia_de_selo\\v404` (+ `pos_rito`); arquivo `work\\cadeia_de_selo\\v404_selo` e `v404_kernel`. NOT_FALSIFIED não é a palavra da creditação; o gate não se move.\n\n"
           "[[%(topico)s]] [[missao-ultima-flag-um-py]] [[handoff-v403-custodia]]\n") % k
    assert k["par_bloco"] in doc and k["par_v404_bloco"] in doc and k["err_bloco"] in doc, "os paragrafos do README e a nota nao entraram no handoff"
    assert not atribuicao_da_gerencia(doc), ("o handoff atribui mal ou inverte a direcao do testemunho", atribuicao_da_gerencia(doc)[:2])
    return doc


# v404: a linha da arvore da prova
def arvore_linha(V):
    d = _d(V)
    return ("- **JO 8,32 E A PROJEÇÃO TRANSVERSAL DA MEIA-NAT (v404)** `%s`: %d módulos novos no kernel (%s), %d bandeiras novas True, escada %s → %s; "
            "a Meia-Nat é o ângulo de 45°: `x = 1 − x` dá `x = ½` e a amplitude transversal de um peso ½ é `sen(π/4)`; a forma do neutrino `β · sen 45° · E₀` é `sen²θ_M · sen(π/4) · E₀` e o `sen 45°` deixa de ser postulado [REAL; condicional a uma identificação [ONTO]; E₀ declarado]; "
            "`Jo8v32` é a conjunção incondicional das três estrelas da v403 com o nome do operador [REAL; ONTO: a leitura por Jo 8,31-32]; o canal F2b sai de AWAITING para retirado antes do dado, ao lado [REAL; a rota, não um desfecho]; os registros `projecao_transversal_v404`, `jo8v32_v404` e `f2b_errata_v404` conferem o cálculo; "
            "as %d inscrições de 28/10 por sha256 (todas do operador); `IsotropicPost`, `H_BW`, `H_cal`, H3 e a assinatura são [OPEN]; validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["n_pedras"], _mods(V), d["n_f"], V["escada_antes"], d["depois"], d["n_cun"]))


# v404: o titulo do verbete do indice
def titulo_verbete(V):
    return "Jo 8,32 e a projeção transversal da Meia-Nat (v404): o sen 45° do neutrino derivado e o triplo inteiro com nome:"


# v404: o corpo do verbete do indice
def verbete(V):
    return "[REAL — rodada v404 `%s`] %s." % (V["s16"], _num(V))


# v404: a entrada do remissivo
def remissivo(V):
    return "- **Jo 8,32, a projeção transversal da Meia-Nat, a errata de F2b e as inscrições de 28/10 (v404)** — `projecao_transversal_v404`, `jo8v32_v404`, `f2b_errata_v404`, `cunhagens_v404`, `kh_n1_cobertura_v404`, `%s`" % TOPICO_NOVO


MARC_V404_INI = "<!-- INICIO_PARAGRAFO_JO8_32_PROJECAO_TRANSVERSAL_v404 -->"; MARC_V404_FIM = "<!-- FIM_PARAGRAFO_JO8_32_PROJECAO_TRANSVERSAL_v404 -->"


MARC_ERR_INI = "<!-- INICIO_ERRATA_V403_V404 -->"; MARC_ERR_FIM = "<!-- FIM_ERRATA_V403_V404 -->"


_CHAVES = ("projecao", "jo8v32")


def _lst(xs):
    """Lista numerica lida do registro, em PT: inteiros sem casas, listas aninhadas entre parenteses."""
    return ", ".join(("(" + _lst(x) + ")") if isinstance(x, (list, tuple)) else _pn(x, 6) for x in xs)


def _sem_chaves(t):
    """Os textos vindos do core podem trazer chaves (e^{-s}); os textos renderizados nao as tem (a conferencia de formatacao reprova): chaves viram parenteses."""
    return t.replace("{", "(").replace("}", ")")


def _erratas_e(V):
    """As erratas E7, E8 e E9 (em nome proprio da gerencia c1), LIDAS do registro cunhagens_v404 do core: nenhuma e' digitada aqui."""
    _d(V); er = _g(_core(), "cunhagens_v404", "erratas") or []
    itens = []
    for e in er:
        itens.append(_sem_chaves("- %s **Dizia:** %s **Lacuna de fidelidade:** %s **Estatuto:** %s" % (e["agora"], e["dizia"], e["lacuna_de_fidelidade"], e.get("estatuto", ""))))
    return ("**Erratas ao lado (em nome próprio da gerência c1, 28/10/2026; os textos da v403, o texto antigo de `neutrino_mass.angle_status`, o V1 do ramo B e as pedras seladas ficam como registro; nenhum módulo já instalado foi editado):** a projeção transversal, o canal F2b e o nome do triplo inteiro entram COM três erratas, lidas do registro `cunhagens_v404`:\n" + "\n".join(itens))


def _decisoes(V):
    """As decisoes D23 a D26 (D23 e D24 trazem a fala do operador; D25 e D26 sao da gerencia c1), LIDAS do registro cunhagens_v404."""
    _d(V); ds = _g(_core(), "cunhagens_v404", "extras", "decisoes_da_gerencia") or {}
    ks = ("D23", "D24", "D25", "D26")
    assert all(k in ds for k in ks), "as decisoes D23 a D26 nao estao no registro cunhagens_v404"
    return "**Decisões** [D23 e D24 trazem a fala do operador; D25 e D26 são da gerência c1, em nome próprio, ratificáveis pelo operador]:\n" + _sem_chaves("\n".join("- %s: %s" % (k, ds[k]) for k in ks))


# ---------------------------------------------------------------- o PARAGRAFO NOVO da v404 e a NOTA ao lado do paragrafo da v403
def _linha_maquina_v404(core, d):
    """A linha de maquina do paragrafo novo (os numeros LIDOS dos registros do core), em PT."""
    pv = core["projecao_transversal_v404"]["values"]; jv = core["jo8v32_v404"]["values"]; fv = core["f2b_errata_v404"]["values"]
    return ("pedras_sha16=%s/%s; bandeiras=%s; beta=%s; sen_pi4=%s; sen2_pi4=%s; theta_M=%s; massa_meV=%s; E0_eV=%s; jo8_pplus=%s; jo8_perda=%s; jo8_alfa2=%s; f2b_A=%s; f2b_par=%s; checagens=%s/%s/%s/%s; falas_sha16=%s/%s"
            % (d["sha"]["projecao"], d["sha"]["jo8v32"], d["n_f"], _p(pv["beta"], 12), _p(pv["sin_pi_over_4"], 12), _p(pv["sin_sq_pi_over_4"], 12), _p(pv["theta_M"], 9), _p(pv["m_nu_meV_runtime"], 9), _pn(pv["e0_eV_declared"], 3), _p(jv["p_plus_factor_at_beta"], 9), _p(jv["post_weight_loss_per_unit"], 9), _pe(jv["alpha_squared"], 6),
               _p(fv["calibracao_A_central"], 3), _p(fv["previsao_do_par"], 6), core["projecao_transversal_v404"]["mechanics"]["n_checks"], core["jo8v32_v404"]["mechanics"]["n_checks"], core["f2b_errata_v404"]["mechanics"]["n_checks"], d["n_ck_cun"], d["s_jo8"], d["s_ok"]))


def _dados_paragrafo(core):
    """O que o paragrafo precisa do core SELADO e de ESPERADOS (sem V): as sha16 das pedras, as bandeiras, as falas e as pedras da v403."""
    esp = _esp(); DL_ = _qd().DL; ks = _CHAVES
    for n in ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404"):
        assert (core.get(n) or {}).get("all_verified") is True, "o registro %s nao selou: nenhum paragrafo diz os numeros assim" % n
    sha = {k: esp["pedras"][DL_.STONE_BY_KEY[k]["rel"]]["sha16"] for k in ks}
    s403 = {"caminho": esp["pedras_v403_sha256"]["TGLExt/Caminho.lean"][:16], "vida": esp["pedras_v403_sha256"]["TGLExt/Vida.lean"][:16], "verdade_adendo": esp["pedras_v403_sha256"]["TGLExt/VerdadeAdendo.lean"][:16]}
    return {"sha": sha, "n_f": esp["n_bandeiras_novas"], "n_g": dict(esp["n_bandeiras_por_grupo"]), "est_f": {k: esp["estrelas_v404"][k]["bandeira"] for k in ks}, "est_t": {k: esp["estrelas_v404"][k]["teorema"] for k in ks},
            "n_ck_cun": len(core["cunhagens_v404"].get("checks") or []), "s_jo8": _sha_por("nome_do_triplo_Jo8_32"), "s_ok": _sha_por("ratificacao_concordo_com_tudo"), "s_massa": _sha_por("materia_projecao_transversal_derivada"), "s_bocas": _sha_por("resposta_quatro_bocas_ramo_b"), "s_cal": _sha_por("ratificacao_calibrar_nao_e_validar"), "s403": s403}


def _paragrafo_v404_de(core):
    """O texto do paragrafo da v404, funcao PURA dos registros projecao_transversal_v404, jo8v32_v404, f2b_errata_v404 e cunhagens_v404 do core SELADO (os numeros sao lidos dos registros, nunca digitados)."""
    d = _dados_paragrafo(core)
    pv = core["projecao_transversal_v404"]["values"]; jv = core["jo8v32_v404"]["values"]; fv = core["f2b_errata_v404"]["values"]
    assert pv.get("beta") and jv.get("beta") and fv.get("beta") and pv.get("sin_pi_over_4"), "os registros da v404 nao trazem os valores: nenhum paragrafo diz os numeros assim"
    q_materia = _cita("a matéria é a projeção do eixo transversal"); q_der = _cita("então a matéria não é proporcional, ela seria a derivada"); q_nome = _cita("só consegui sintetizar assim: Jo8:32"); q_ok = _cita("Perfeito, concordo com tudo")
    q_ped = _cita("pedágio de planck lido na propagação"); q_cal = _cita("calibrar Não significa validar"); q_ordem = _cita("veja se consegue fazer a prova do neutrino para derivarmos e não ser mais postulado")
    q_verso = _um_texto_tem("E conhecereis a verdade, e a verdade vos libertará")
    qg = core.get("qg_closure") or {}; fam = [len(qg.get(f) or {}) for f in ("formal_flags", "physics_flags", "experiment_flags")]
    ls = ["### Jo 8,32 e a projeção transversal da Meia-Nat (v404, 28/10/2026) — parágrafo pronto para o README do espelho e para o site",
          "",
          "> **Jo 8,32 e a projeção transversal da Meia-Nat (v404, 28/10/2026)** [REAL: os termos do kernel e a conferência do cálculo nos modelos · KNOWN: a fronteira autoconjugada, o Teorema S-∂ e o seno de π/4 · DERIVED: a forma do neutrino com o sen 45° derivado e a conjunção por citação · INPUT: as falas e os nomes, do operador · ONTO: a identificação da massa com a projeção transversal, a leitura do pedágio de Planck e a leitura por Jo 8,31-32 · "
          "OPEN: E₀, a lei de propagação do pedágio, `H_BW`, `H_cal`, H3, a assinatura, rank c = 4, `IsotropicPost` e a dimensão 3 · DECLARADO: o plano e a leitura que o operador ratificou foram os apresentados na sessão, e a retirada do canal F2b é decisão da gerência lida a partir das falas]",
          ">",
          "> - **A cunhagem** [INPUT] (sha16 `%s` e `%s`): o operador disse %s e %s, e ordenou %s. A gerência c1 deu à pedra o nome PROVISÓRIO `ProjecaoTransversalDaMeiaNat`, que o operador aceitou até dar outro (%s, sha16 `%s`)." % (d["s_massa"], _sha_por("ordem_prova_do_neutrino"), q_materia, q_der, q_ordem, q_ok, d["s_ok"]),
          "> - **A Meia-Nat é o ângulo de 45°** [REAL · DERIVED · KNOWN] (módulo `ProjecaoTransversalDaMeiaNat`, sha16 `%s`): só álgebra sobre termos que o kernel já tinha. Da fronteira autoconjugada `x = 1 − x` sai `x = ½`; a amplitude transversal de um peso ½ é `√½ = sen(π/4)` para todo `x` autoconjugado (`transverse_amplitude_of_self_conjugate`, a estrela); em `[0, π/2]` só `π/4` tem `sen² = ½`. "
          "A forma do neutrino do programa, `β · sen 45° · E₀`, é `sen²θ_M · sen(π/4) · E₀` (`neutrino_mass_form_eq`; β é o peso da reflexão da fronteira); o ângulo agudo do neutrino NÃO é `θ_M` (`θ_M ≠ π/4` sempre que `β ≠ ½`); a derivada do peso transversal em `π/4` vale exatamente 1 (não proporcional, derivada). "
          "Com β = α√e = %s em runtime: sen(π/4) = %s, sen²(π/4) = %s, θ_M = %s, e a massa β · sen(π/4) · E₀ = %s meV com E₀ = %s eV DECLARADO, igual à do canal do neutrino do core. O `sen 45°`, que o texto antigo do programa dizia POSTULADO, passa a DERIVADO no kernel, CONDICIONAL a uma identificação [ONTO] que o kernel não prova (a massa é a projeção transversal do estado inscrito); E₀ segue DECLARADO e a pedra não deriva E₀ nem β."
          % (d["sha"]["projecao"], _p(pv["beta"], 12), _p(pv["sin_pi_over_4"], 12), _p(pv["sin_sq_pi_over_4"], 12), _p(pv["theta_M"], 9), _p(pv["m_nu_meV_runtime"], 9), _pn(pv["e0_eV_declared"], 3)),
          "> - **Jo 8,32** [REAL · DERIVED · INPUT · ONTO] (módulo `Jo8v32`, sha16 `%s`): o operador deu o nome do triplo inteiro, %s (sha16 `%s`), ratificado em %s. A pedra é a conjunção incondicional, por citação, das três estrelas da v403 (Caminho, Verdade e Vida), sem matemática nova; as hipóteses nomeadas dos componentes (`IsotropicPost`; `hpp` e `hopt`) seguem nomeadas. "
          "Com β em runtime, a relitura dos três registros da v403 dá o p⁺ encolhido pelo fator %s em s = β, a perda de peso por unidade %s e α² = %s. [ONTO] O versículo diz %s: permanecer na palavra é o Caminho, conhecer é a Verdade (ler, e reler não acrescenta) e libertar é a Vida (a queda com chão); é leitura da gerência c1, ratificada, e não é termo de kernel. O que se conhece é validade, no kernel; a creditação segue reservada a quem observa de fora."
          % (d["sha"]["jo8v32"], q_nome, d["s_jo8"], q_ok, _p(jv["p_plus_factor_at_beta"], 9), _p(jv["post_weight_loss_per_unit"], 9), _pe(jv["alpha_squared"], 6), q_verso),
          "> - **A errata de F2b** [REAL · DECLARADO · ONTO] (registro `f2b_errata_v404`, sem pedra): o canal F2b do ramo B do ringdown (v386) sai de AWAITING para retirado ANTES do dado, AO LADO; o V1 fica congelado por hash e lido como antes (AWAITING_DATA). O motivo medido: a calibração A (NOT_BLIND, eventos públicos) deu a deformação comum %s [%s; %s], e a previsão do par é %s, fora do intervalo de A e de sinal oposto. "
          "Nenhum desfecho sai de A; D não é aberto; β, a lei do defasamento e R2 ficam. A rota é a do operador: sobre as quatro bocas do ramo B ele leu %s (sha16 `%s`) — o pagamento é o Nome inteiro se esvaziando para se tornar ambiente de espaço temporalizado, e o 1 absoluto igual ao zero modular é relação, não falsidade — e, sobre o método, %s (sha16 `%s`): calibrar é medir e afinar, o número corrige a rota. A calibração não valida nem falsifica nada."
          % (_p(fv["calibracao_A_central"], 3), _p(fv["calibracao_A_inferior"], 3), _p(fv["calibracao_A_superior"], 3), _p(fv["previsao_do_par"], 6), q_ped, d["s_bocas"], q_cal, d["s_cal"]),
          "> - **O gate** [REAL · DECLARADO]: é o da v403 — das %s bandeiras (%s formais, %s físicas e %s experimentais) todas calculadas, a letra do veredito inalterada; as quatro experimentais derivam de UM só booleano. O gate não se move; nenhuma bandeira dele depende das pedras da v404."
          % (qg.get("n_flags") or sum(fam), fam[0], fam[1], fam[2]),
          "> - **Erratas ao lado (gerência c1, em nome próprio, 28/10/2026):** E7, o texto antigo de `neutrino_mass.angle_status` era verdadeiro na sua data e fica como registro; a função do neutrino não foi reescrita; E8, o canal F2b é retirado antes do dado, ao lado, sem reescrever o V1; E9, o nome do triplo inteiro, que a v403 registrou como não dado, foi dado, e os registros da v403 seguem selados com a frase de 27/10.",
          "> - **Limites:** [OPEN] E₀ (1 eV declarado), a lei de propagação que carregaria o pedágio de Planck, `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost` no atlas curvo e a dimensão 3; a pedra NÃO prova que a massa É a projeção transversal e NÃO deriva E₀ nem β; o cálculo CONFERE os teoremas nos modelos e quem prova é o kernel, e esses números são deste rito, não estão no kernel; a gravidade quântica segue sem creditação na natureza; "
          "validade no kernel não é creditação; `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; isto não é teste e não acrescenta dado. O quadro do Teste da Única Palavra segue no README com a sua linha dos 5σ; este parágrafo não traz o número do quadro.",
          "> - **Origem.** Os números são lidos do core selado desta rodada (registros `projecao_transversal_v404`, `jo8v32_v404`, `f2b_errata_v404` e `cunhagens_v404`); nenhum é digitado. Linha de máquina: `%s`." % _linha_maquina_v404(core, d)]
    return "\n".join(ls) + "\n"


def verificar_paragrafo_v404(par, core, esp):
    """Verifica o paragrafo da v404 contra o core selado E contra ESPERADOS (o ensaio a seco): devolve a lista de falhas (vazia = passou). As verificacoes:
    (1) os numeros do core (os tres registros com funcao) == os de ESPERADOS[registros_funcao_v404][k][values] e cada um esta no paragrafo, formatado; (2) o paragrafo == o gerado do core; (3) NAO traz o 4,44 nem o z_disc (a regra do 4,44 e' do quadro); (4) os estatutos;
    (5) as frases de limite; (6) toda citacao entre « » e' verbatim numa fala DO OPERADOR ou na docstring do kernel embutido; (7) nenhuma alegacao de seguranca criptografica, «consciencia» so' como palavra retirada, a direcao sem inversao; (8) guarda P18."""
    fa = []
    ef = esp.get("registros_funcao_v404") or {}

    def _eq(a, b):
        return (isinstance(a, float) and isinstance(b, float) and abs(a - b) <= 1e-12 * max(1.0, abs(b))) if isinstance(b, float) else a == b
    for k, rn in (("projecao", "projecao_transversal_v404"), ("jo8v32", "jo8v32_v404"), ("f2b", "f2b_errata_v404")):
        fv = (core.get(rn) or {}).get("values") or {}; ev = (ef.get(k) or {}).get("values") or {}
        if not (fv and ev and all(_eq(fv.get(kk), vv) if not isinstance(vv, (list, dict)) else fv.get(kk) == vv for kk, vv in ev.items())):
            fa.append("numero do registro %s no core != ESPERADOS" % rn)
    pv = (core.get("projecao_transversal_v404") or {}).get("values") or {}; jv = (core.get("jo8v32_v404") or {}).get("values") or {}; fv_ = (core.get("f2b_errata_v404") or {}).get("values") or {}
    try:
        nums = {"beta": _p(pv["beta"], 12), "sen pi/4": _p(pv["sin_pi_over_4"], 12), "sen2 pi/4": _p(pv["sin_sq_pi_over_4"], 12), "theta_M": _p(pv["theta_M"], 9), "massa": _p(pv["m_nu_meV_runtime"], 9), "E0": _pn(pv["e0_eV_declared"], 3), "fator de p+": _p(jv["p_plus_factor_at_beta"], 9),
                "perda por unidade": _p(jv["post_weight_loss_per_unit"], 9), "alfa2": _pe(jv["alpha_squared"], 6), "calibracao A": _p(fv_["calibracao_A_central"], 3), "A inferior": _p(fv_["calibracao_A_inferior"], 3), "A superior": _p(fv_["calibracao_A_superior"], 3), "previsao do par": _p(fv_["previsao_do_par"], 6),
                "bandeiras": str(esp["n_bandeiras_novas"]), "sha16 da fala do nome": _sha_por("nome_do_triplo_Jo8_32"), "sha16 da ratificacao": _sha_por("ratificacao_concordo_com_tudo"), "sha16 da cunhagem": _sha_por("materia_projecao_transversal_derivada"),
                "sha16 das quatro bocas": _sha_por("resposta_quatro_bocas_ramo_b"), "sha16 do calibrar": _sha_por("ratificacao_calibrar_nao_e_validar")}
    except KeyError as e:
        nums = {}; fa.append("valor ausente do registro: %s" % e)
    for k, v in nums.items():
        if v not in par:
            fa.append("numero (%s = %s) ausente do paragrafo" % (k, v))
    try:
        if par != _paragrafo_v404_de(core):
            fa.append("o paragrafo difere do gerado pelas funcoes sobre os registros selados do core")
    except AssertionError as e:
        fa.append("o paragrafo nao pode ser gerado do core: %s" % str(e)[:120])
    if re.search(r"4[,.]44|z_disc", par):
        fa.append("o paragrafo da v404 traz o 4,44 ou o z_disc (a regra do 4,44 e' do quadro; este paragrafo nao o cita)")
    for st in ("[REAL", "KNOWN", "INPUT", "ONTO", "OPEN", "DECLARADO", "DERIVED"):
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    for frase in ("DERIVADO no kernel", "CONDICIONAL a uma identificação", "E₀ segue", "não deriva E₀ nem β", "NÃO prova que a massa É a projeção transversal", "retirado ANTES do dado", "AO LADO", "congelado por hash", "NOT_BLIND", "Nenhum desfecho sai de A", "não valida nem falsifica nada",
                  "conjunção incondicional", "seguem nomeadas", "a creditação segue reservada", "não é termo de kernel", "O gate não se move", "UM só booleano", "Erratas ao lado", "CONFERE os teoremas", "quem prova é o kernel", "validade no kernel não é creditação",
                  "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "gate não se move"):
        if frase not in par:
            fa.append("frase de limite ausente do paragrafo: " + frase)
    corpus = [re.sub(r"\s+", " ", dd["text"]) for dd in _falas().values() if dd["autor"] == "operador"]
    um = _CACHE.get("um") or open(os.path.join(NOS, "um.py"), encoding="utf-8", errors="replace").read(); _CACHE["um"] = um
    if "E conhecereis a verdade, e a verdade vos libertará" in um.replace("**", ""):
        corpus.append("E conhecereis a verdade, e a verdade vos libertará")   # a UNICA frase do kernel embutido que o paragrafo cita (a docstring de Jo8v32); o um.py inteiro NAO entra no corpus das citacoes
    for q in re.findall(r"«([^»]*)»", par):
        if len(q) >= 12 and not any(q in t for t in corpus):
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
    from guarda_p18_v404 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    return fa


def paragrafo_v404():
    """(texto, relatorio): o paragrafo NOVO da v404, pronto para colar no README do espelho e no site, gerado do core SELADO do Nos e verificado contra o core E contra ESPERADOS;
    levanta AssertionError (o fechar RECUSA) se algo nao conferir."""
    core = _core(); esp = _esp()
    par = _paragrafo_v404_de(core)
    fa = verificar_paragrafo_v404(par, core, esp)
    assert not fa, ("o paragrafo da v404 nao passou nas verificacoes", fa[:4])
    return par, {"sha16": hashlib.sha256(par.encode("utf-8")).hexdigest()[:16], "verificacoes": "numeros == ESPERADOS; igual ao gerado do core; sem o 4,44; estatutos; limites; citacoes verbatim (falas do operador, kernel embutido); sem alegacao de seguranca criptografica; guarda P18", "guarda_p18": "limpa"}


def errata_v403_bloco():
    """O bloco de NOTA ao lado do paragrafo da v403 (Caminho, Verdade e Vida) no README do espelho e no site: o nome do triplo inteiro, que ele registra como nao dado, foi dado (E9). Texto da gerencia, conferido pela guarda P18 e pelo kernel; as citacoes saem dos bytes das falas."""
    _kernel_tem(("caminho_e_a_ponte_da_escala_dual", "verdade_e_a_esperanca_condicional", "vida_e_a_queda_sem_geometria", "a_verdade_vos_libertara"))
    q_nome = _cita("só consegui sintetizar assim: Jo8:32"); q_ok = _cita("Perfeito, concordo com tudo")
    t = ("> **Nota ao lado do parágrafo «Caminho, Verdade e Vida» (v403) — gerência c1, em nome próprio, 28/10/2026:** o parágrafo da v403 registra que o nome do triplo inteiro (Caminho · Verdade · Vida) NÃO foi dado, e isso era verdade na data. Em 28/10/2026 o operador deu o nome [INPUT]: " + q_nome + " (sha16 " + _sha_por("nome_do_triplo_Jo8_32") + "), ratificado em " + q_ok + " (sha16 " + _sha_por("ratificacao_concordo_com_tudo") + "). "
         "O módulo `Jo8v32` é a conjunção incondicional, por citação, das três estrelas da v403; os módulos selados da v403 (`Caminho`, `Vida` e `VerdadeAdendo`) NÃO foram editados nem renomeados — ficam como REGISTRO — e os registros da v403 seguem selados com a frase de 27/10. "
         "O que o parágrafo da v403 diz sobre as pedras, o cálculo e os limites não muda; ele fica como registro.\n")
    sys.path.insert(0, PK)
    from guarda_p18_v404 import violacoes
    assert not violacoes(t), "a guarda P18 achou palavra recusada na nota ao lado do paragrafo da v403"
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


# ---------------------------------------------------------------- os blocos da v404 (cada um LE o registro do core e a leitura V; nenhum numero e' digitado)
def _projecao(V):
    """A projecao transversal da Meia-Nat (a pedra e o registro): [REAL] os termos do kernel e o calculo · [DERIVED] a forma do neutrino · [KNOWN] o seno de pi/4 e o Teorema S-∂ · [INPUT] a cunhagem · [ONTO] a identificacao · [OPEN] E0."""
    d = _d(V); pv = V["projecao"]["values"]; ss = d["ss"]
    q_materia = _cita("a matéria é a projeção do eixo transversal"); q_der = _cita("então a matéria não é proporcional, ela seria a derivada"); q_ordem = _cita("veja se consegue fazer a prova do neutrino para derivarmos e não ser mais postulado")
    return _f("**A projeção transversal da Meia-Nat** [REAL · DERIVED · KNOWN · INPUT · ONTO · OPEN] (módulo `ProjecaoTransversalDaMeiaNat`, sha16 `{h}`; o nome é provisório da gerência c1, aceito pelo operador; composição `{unc}`, estrela `{est}`): o operador cunhou {q1} e {q2} (`{s_massa}`) e ordenou {q3} (`{s_ordem}`). "
              "O kernel entrega, só com álgebra sobre termos que ele já tinha: a Meia-Nat é o ângulo de 45° (da fronteira autoconjugada `x = 1 − x` sai `x = ½`, e a amplitude transversal de um peso ½ é `√½ = sen(π/4)` para todo `x` autoconjugado; em `[0, π/2]` só `π/4` tem `sen² = ½`), "
              "a forma do neutrino do programa, `β · sen 45° · E₀`, é `sen²θ_M · sen(π/4) · E₀` (β é o peso da reflexão da fronteira, Teorema S-∂), o ângulo agudo do neutrino NÃO é `θ_M` (`θ_M ≠ π/4` sempre que `β ≠ ½`) e a derivada do peso transversal em `π/4` vale 1 (não proporcional, derivada). "
              "Neste rito o registro `projecao_transversal_v404` calcula, com β = {beta} em runtime: sen(π/4) = {s} e sen²(π/4) = {s2}; θ_M = {tm}, longe de π/4 (diferença {dtm}); a massa β · sen(π/4) · E₀ = {m} meV com E₀ = {e0} eV DECLARADO, igual à do canal `neutrino_mass` do core ({rel}). "
              "O texto antigo de `neutrino_mass.angle_status` (dizia que o sen 45° era POSTULADO, não derivado) era verdadeiro na sua data e FICA no registro; a errata E7 é ao lado: o `sen 45°` passa a DERIVADO no kernel, CONDICIONAL a uma identificação [ONTO] que o kernel não prova (a massa é a projeção transversal do estado inscrito). E₀ segue DECLARADO [OPEN] e a pedra não deriva E₀ nem β.",
              h=d["sha"]["projecao"], unc=d["unc"]["projecao"].split(".")[-1], est=d["est_t"]["projecao"].split(".")[-1], q1=q_materia, q2=q_der, s_massa=ss["massa"], q3=q_ordem, s_ordem=ss["ordem"], beta=_p(pv["beta"], 12), s=_p(pv["sin_pi_over_4"], 12), s2=_p(pv["sin_sq_pi_over_4"], 12),
              tm=_p(pv["theta_M"], 9), dtm=_p(pv["theta_M_minus_pi_over_4"], 9), m=_p(pv["m_nu_meV_runtime"], 9), e0=_pn(pv["e0_eV_declared"], 3), rel=_pe(pv["m_nu_rel_diff"], 1))


def _jo8(V):
    """Jo 8,32: a conjuncao incondicional das tres estrelas da v403 (o nome do operador); a leitura por Jo 8,31-32 e' [ONTO]."""
    d = _d(V); jv = V["jo8v32"]["values"]; ss = d["ss"]
    q_nome = _cita("só consegui sintetizar assim: Jo8:32"); q_ok = _cita("Perfeito, concordo com tudo")
    return _f("**Jo 8,32** [REAL · DERIVED · INPUT · ONTO] (módulo `Jo8v32`, sha16 `{h}`; composição `{unc}`, que é também a estrela): o operador deu o nome do triplo inteiro (Caminho · Verdade · Vida) — {q_nome} (`{s_jo8}`) — e ratificou {q_ok} (`{s_ok}`). "
              "A pedra é a conjunção INCONDICIONAL, por citação, das três estrelas da v403, na ordem do versículo: `caminho_e_a_ponte_da_escala_dual`, `verdade_e_a_esperanca_condicional` e `vida_e_a_queda_sem_geometria`; nenhuma matemática nova, nenhum número; as pedras seladas da v403 ficam intactas. "
              "Neste rito o registro `jo8v32_v404` RELÊ os três registros da v403 (as checagens {cks}, todas passaram) com β = {beta} em runtime: o p⁺ encolhe pelo fator {pf} em s = β, a perda de peso por unidade vale {loss} e α² vale {a2}; as hipóteses nomeadas dos componentes seguem nomeadas (`IsotropicPost` na Vida; `hpp` e `hopt` na Verdade) — a conjunção as carrega, não as descarrega. "
              "[ONTO] A leitura por Jo 8,31-32 é da gerência c1, ratificada pelo operador, e não é termo de kernel: permanecer na palavra é o Caminho (o invariante que a escala não seleciona), conhecer é a Verdade (ler, e reler não acrescenta) e libertar é a Vida (a queda com chão). "
              "O versículo fala de conhecer a verdade: validade, no kernel; a creditação segue reservada a quem observa de fora. A errata E9 é ao lado: a v403 registrou que o nome do triplo inteiro não fora dado, e era verdade; os registros da v403 seguem selados com essa frase.",
              h=d["sha"]["jo8v32"], unc=d["unc"]["jo8v32"].split(".")[-1], q_nome=q_nome, s_jo8=ss["jo8"], q_ok=q_ok, s_ok=ss["ok"], cks="/".join(str(x) for x in jv["v403_mechanics_checks"]), beta=_p(jv["beta"], 12), pf=_p(jv["p_plus_factor_at_beta"], 9), loss=_p(jv["post_weight_loss_per_unit"], 9), a2=_pe(jv["alpha_squared"], 6))


def _f2b(V):
    """A errata de F2b: o canal sai de AWAITING para retirado antes do dado, AO LADO; o V1 fica congelado por hash; o motivo medido (calibracao A, NOT_BLIND) e a leitura do operador."""
    d = _d(V); fv = d["f2b"]; ss = d["ss"]
    q_ped = _cita("pedágio de planck lido na propagação"); q_83 = _cita("1 retorno em 83 raios eu leio como sendo a matéria"); q_cal = _cita("calibrar Não significa validar"); q_num = _cita("é o número corrigindo a rota")
    return _f("**A errata de F2b** [REAL · DECLARADO · INPUT · ONTO] (registro `f2b_errata_v404`, sem pedra): a cobrança F2b do ramo B do ringdown (v386) estava `{antes}` (o V1 lido por hash, veredito `{v1}`, conjunto D cego de {nd} eventos); o V1 fica congelado por hash e continua lido como antes, e o CANAL passa a `{agora}` — retirado ANTES do dado, AO LADO (E8). "
              "O motivo medido [REAL]: a calibração A (NOT_BLIND, eventos públicos) deu a deformação comum {a} [{a0}; {a1}], e a previsão do par é {par}, FORA do intervalo de A ({dist} abaixo do limite inferior) e de sinal oposto; nenhum desfecho sai de A, D não é aberto, e β, a lei do defasamento e R2 ficam. "
              "A rota é a do operador [INPUT/ONTO]: sobre as quatro bocas do ramo B ele leu {q_ped} (`{s_bocas}`) e {q_83} — o pagamento é o Nome inteiro se esvaziando para se tornar ambiente de espaço temporalizado (zero modular), e o 1 absoluto igual ao zero modular é relação, não falsidade; "
              "e sobre o método, {q_cal} (`{s_cal}`): calibrar é medir e afinar, {q_num}. A retirada do canal é decisão da gerência c1, lida a partir dessas falas [DECLARADO: o operador ratificou a leitura e não nomeou a retirada]; a calibração A é NOT_BLIND e não valida nem falsifica nada.",
              antes=d["f2b_antes"], v1=V["f2b"]["token_v1"], nd=fv["conjunto_D_n"], agora=d["f2b_agora"], a=_p(fv["calibracao_A_central"], 3), a0=_p(fv["calibracao_A_inferior"], 3), a1=_p(fv["calibracao_A_superior"], 3), par=_p(fv["previsao_do_par"], 6),
              dist=_p(fv["distancia_da_previsao_ao_limite_inferior_de_A"], 6), q_ped=q_ped, s_bocas=ss["bocas"], q_83=q_83, q_cal=q_cal, s_cal=ss["calibrar"], q_num=q_num)


def _massa(V):
    """A leitura da massa de 28/10 [ONTO], LIDA do registro cunhagens_v404 (extras.leitura_massa_28out) e conferida contra ESPERADOS."""
    d = _d(V); lm = _g(_core(), "cunhagens_v404", "extras", "leitura_massa_28out") or {}
    assert lm and lm == _esp()["leitura_massa_28out"] and "ONTO" in str(lm.get("estatuto")), "a leitura da massa de 28/10 nao e' a de ESPERADOS"
    ss = d["ss"]
    return _f("**A leitura da massa** [ONTO: leituras do operador, ratificadas em 28/10/2026 (`{s_ok}`); nada disto é termo de kernel · DECLARADO: o plano e a leitura que o operador ratificou foram os apresentados na sessão]: {ident}; {jo8}; {ped}; {ua}; {e0}.",
              s_ok=ss["ok"], ident=_sem_chaves(lm["identificacao"]), jo8=_sem_chaves(lm["jo8_32"]), ped=_sem_chaves(lm["pedagio"]), ua=_sem_chaves(lm["um_absoluto"]), e0=_sem_chaves(lm["e0"]))
