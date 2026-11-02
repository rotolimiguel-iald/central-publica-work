# -*- coding: utf-8 -*-
# Os TEXTOS da v405 SELADA, ESCRITOS A MAO para o delta da v405 (a semente mecanica veio de textos_v404.py, subida pelo motor; o conteudo e' novo): as OITO pedras com os nomes do operador (Ponte da Massa; Massa = tensao pura; Identidade; Observador = terminal; Lei do diminuto; Tonica do Hamiltoniano; Disco de Euler; Ponto Zero do Psion),
# os OITO registros com funcao (cada um LE do kernel do rito a composicao, a estrela, o contrato e o suporte da sua pedra e CALCULA um modelo honesto com beta = alfa x raiz de e em runtime), os registros por spec cunhagens_v405 (as falas do operador de 30/10 a 01/11 por sha256, as erratas E10 a E13 em nome proprio da gerencia c1, as decisoes D27 a D33), campos_fechados_e_leituras_v405,
# ga_reclassificacao_v405 (a classe nova do teste do Grande Atrator, ao lado), gap_v405 (o gap espectral do lock e o valor esperado dele no angulo de Miguel, ao lado) e kh_n1_cobertura_v405, e as secoes «A massa derivada e a identidade definida» e «A identidade» do artigo. Os registros da v404 e das versoes anteriores ficam como REGISTRO: sao RECRIADOS pelo rito e conferidos iguais a v404 selada.
# A MOLDURA (errata da gerencia c1, 01/11/2026): os campos das estruturas fecharam; as leituras do operador passaram do campo para a definicao; a leitura fisica nao virou teorema; dadas as entradas, a FORMA e' teorema. Toda superficie passa pela guarda das frases (guarda_frases_v405.py), com a excecao so' da fala do operador.
# O QUADRO «O Teste da Única Palavra» (v397) PERMANECE no topo do artigo PT/EN e do .md canonico, INTOCADO. Cada numero, hash e veredito entra por chave de V (leitura_v405.ler), por ESPERADOS ou pelo core do Nos, ou e' LIDO de um arquivo aqui, nunca digitado;
# o que vai escrito a mao e' so' prosa, nome de termo (conferido em tempo de execucao no kernel do Nos, no um.py ou no pacote) e frase curta do operador (conferida palavra por palavra contra os bytes das falas).
# REGRA DA ORDEM DO OPERADOR (23/10/2026, sha16 9b182958a5a7a1bc: reportar o 4,44 no inicio do artigo, no README e em tudo mais; vale em TODO texto que o cite): o 4,44 (z_disc calibrado) NUNCA aparece sem o p calibrado e sem a linha dos 5σ no MESMO item (a discriminacao a 5σ,
# o degrau da creditacao, NAO foi alcancada; NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move; o teste nao foi cego). A frase do operador entra VERBATIM (nunca parafraseada entre aspas); o paragrafo do QUADRO sai das MESMAS funcoes do quadro (quadro_v397),
# sobre o core SELADO do Nos. O paragrafo NOVO da v405 NAO traz o 4,44. Estatutos marcados; erratas AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a traducao falhou).
# Os paragrafos do TESTEMUNHO DE DOIS (v399), da FALSIDADE (v401), da PONTE, DA QUEDA E DA ESPERANCA (v402), de CAMINHO, VERDADE E VIDA (v403) e de JO 8,32 (v404) SEGUEM COMO ESTAO no README do espelho e no site: esta versao NAO os regenera nem os substitui; o handoff da v405 so' o diz e traz a NOTA ao lado do da v404 (E0 passou de declarado a posto; os nomes foram dados).
# GUARDA: as cinco regras da P18 (guarda_p18_v405.py) rodam sobre cada texto renderizado em superficies_v405.py, fechar_v405.py e registrar_mapa_v405.py e sobre este arquivo na cadeia. A palavra recusada nunca aparece aqui: a recusa e' dita como «creditação».
import hashlib, json, os, re, sys
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V405"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v405 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(PK))          # ...\Central de Patentes\work
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
TOPICO_NOVO = "v405-selada-massa-derivada-e-identidade.md"
# os marcadores entre os quais o handoff traz os PARAGRAFOS PRONTOS do README do espelho e do site: o QUADRO (v397, intocado) com os MESMOS marcadores da v397, e o paragrafo NOVO da falsidade
MARC_PAR_INI = "<!-- INICIO_PARAGRAFO_README_v397 -->"; MARC_PAR_FIM = "<!-- FIM_PARAGRAFO_README_v397 -->"
# nomes de termo de kernel (Lean) citados nos textos: cada um tem de existir em algum .lean de TGLExt/ do Nos (lido na hora); os modulos citados como fonte tem de existir como arquivo
_NOMES_KERNEL = ("massa_derivada_eq_form", "a_transicao_existe_para_todo_acoplamento", "peso_da_face_absoluta", "transicaoDerivada", "massaDerivada", "massa_e_tensao_pura", "emprestimoDerivado", "one_turn_gives_faithful_period", "leiDerivada", "tonica_eq", "the_tonic_lands_on_the_posted_unit", "the_tonic_at_the_posted_one",
                 "no_function_of_the_inscription_fixes_E0", "the_mass_is_the_zero_point", "pagamentoComoCurvatura", "stops_in_finite_time", "frequency_squared_unbounded_at_the_stop", "the_observers_posto_is_the_terminal", "the_fusion_is_not_pressupposed", "a_lei_inteira", "a_identidade_fecha", "absolute_faces_half", "forty_five_unique", "alpha_is_measured_from_within",
                 "gammaB_is_the_canonical_law_at_the_systems_frequency", "monopole_time_is_the_horizon_light_time", "umPosto", "the_flow_is_the_canonical_law", "the_fixed_points_read_one_and_zero", "the_omega_pole_reads_one", "foton_sem_massa", "the_charge_never_completes", "meioTom", "omegaSq", "lerE0", "mesmas_razoes_iff_transposicao", "transpor_preserva_toda_razao", "E0_relativo_pinado", "lerE0_transpor", "the_diminished_law_closes", "the_ratio_survives_the_rescaling", "meioTom_e_o_pedagio_local", "meioTom_e_a_face", "modular", "modular_sustenta", "modular_mantem_a_escala", "modular_nao_e_transposicao", "lerE0_e_a_tonica_modulada", "um_tom_vira_terca_menor", "the_gap_closes", "o_lock_tem_gap_um", "lock_no_angulo", "lock_no_angulo_de_miguel", "tempoDoRetido", "o_relogio_do_retido", "retidoNoAngulo", "lockDe", "o_gap_com_unidade", "o_retido_e_o_valor_esperado_do_lock", "HminMic_e_o_lock", "HminMic", "FockCertificate", "alphaKappa", "o_psion_e_a_projecao_do_modo", "a_tonica_e_o_retido_sobre_alpha", "a_massa_e_a_projecao_do_retido", "o_psion_e_raiz_de_dois_retidos", "zero_mode_weight_is_one", "alpha_transport")
_MODULOS_KERNEL = ("PonteDaMassa", "MassaTensaoPura", "Identidade", "ObservadorTerminal", "LeiDoDiminuto", "TonicaDoHamiltoniano", "DiscoDeEuler", "PontoZeroDoPsion", "ProjecaoTransversalDaMeiaNat", "Jo8v32", "Caminho", "Vida", "VerdadeAdendo", "Verdade", "Posto", "ContinuousModularZero")
# identificadores do um.py citados nos textos: cada um tem de existir no um.py do Nos (lido na hora)
_NOMES_UM = ("SEALED_CODATA_ALPHA", "ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405", "cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405",
             "_V405_CONTRACTS", "_V405_VERBATINS2", "_V405_SPECS", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404", "_V404_CONTRACTS", "_V404_SPECS", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403",
             "prove_qg_closure_gate", "evaluate_quantum_gravity_closure", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386", "angle_status", "GA_WINDOW_STATUS", "prove_ga_mass_audit", "prove_joint_coincidence_result_v3", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "selo_acom_sidecar_v399",
             "teste_de_veracidade_fase9_v397", "hubble_ratio_opening_v388", "_v397_quadro_md", "_v397_atomos", "_V397_FRASE_444", "testemunha_estatica_v396", "psibit_v395")
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
_CACHE = {}
# a DIRECAO (v399): nenhuma frase pode por a IALD como quem testifica DO operador (fora da fala em que ele a recusa); a mesma regex do conferidor (C12)
_RX_INV = re.compile(r"IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)")
ERRATA_TEOREMAS = "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"   # (a mesma frase de delta_v405.ERRATA_TEOREMAS_PT; o harness confere)


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
    """ESPERADOS_v405.json (gerado pelo ensaio a seco do candidato), lido uma vez."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v405.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _core():
    """O core do Nos (so' leitura), para os campos que so' existem depois do rito; ausente e' falha visivel."""
    if "core" not in _CACHE:
        _CACHE["core"] = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["core"]


def _base_core():
    """O core da v404 selada (a copia de bytes em base_v404): de onde saem os numeros da errata ao lado e a medida da proveniencia."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v404", "um_absoluto.json"), encoding="utf-8"))["core"]
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
            s = k[len("v405_cun_"):]
            fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(s + "_")]
            assert len(fs) == 1, ("a inscricao %s nao tem arquivo unico em insumos/cunhagens" % s, fs)
            b = open(os.path.join(pasta, fs[0]), "rb").read()
            assert hashlib.sha256(b).hexdigest() == meta["sha256"] and len(b) == meta["bytes"] and meta["sha256"][:16] == s, "a inscricao %s nao confere com o sha256 de ESPERADOS" % s
            nome = fs[0][len(s) + 1:]
            autor = "gerencia" if nome.startswith("GERENCIA_") else "operador"
            assert autor == "operador" and not str(meta.get("papel", "")).startswith("leitura da gerencia"), ("a v405 nao tem inscricao da gerencia: todas sao falas do operador", s)
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
    """A cobertura do Audit e a arvore formal da v404 selada (o core guardado em base_v404): de onde saem os numeros da errata ao lado dos pisos."""
    if "cov_base" not in _CACHE:
        kf = _base_core()["kernel_formalization"]
        cov = kf["axiom_coverage_v392"]
        _CACHE["cov_base"] = {"decl": cov["decl"], "thm": cov["thm"], "h8": len(kf["formal_files_sha256"]), "axr": len(kf["axiom_report"])}
    return _CACHE["cov_base"]


def _bancada():
    """A geracao do manifesto que a Bancada de producao pina (do recibo pre_selo pinado em PINOS_BN) e a versao que ela pina; o passo e' simples (sem salto e sem cadeia de selos)."""
    p = json.load(open(os.path.join(PK, "PINOS_BN_v405.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v404" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v404 -> v405 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1}


def _proveniencia(esp):
    """A proveniencia que o compilador emite atribui ao modulo da pedra N declaracoes; todas sao NOVAS no axiom_report (nenhuma reatribuida), e o FLAGS_v405.json do sandbox concorda (as contagens de
    publicas, privadas, nomeadas e auxiliares so' existem la')."""
    if "prov" not in _CACHE:
        kf = _core()["kernel_formalization"]; src = kf["declaration_sources_v394"]; pedras = set(esp["pedras_sha256"])
        b0 = _base_core()["kernel_formalization"]; axr0 = b0["axiom_report"]
        mine = sorted(n for n, p in src.items() if p in pedras)
        novas = [n for n in mine if n not in axr0]
        fj = json.load(open(os.path.join(PK, "kernel", "FLAGS_v405.json"), encoding="utf-8"))
        assert len(mine) == fj["decl_totais_modulos_novos"] and len(novas) == fj["decl_novas_dos_modulos"] == len(mine) and not fj["reatribuidas_as_pedras"], ("a proveniencia do rito != FLAGS_v405.json do sandbox", len(mine), len(novas), fj["reatribuidas_as_pedras"])
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
    """Os numeros da v405, todos LIDOS (V da leitura da rodada, ESPERADOS, core do Nos, base v404, FLAGS do sandbox, os registros): nenhum e' digitado aqui. Recusa se as contagens nao fecham."""
    _conferir_nomes()
    esp = _esp(); tv = V["veracidade"]; sa = V["selo"]; dc = V["declaracao"]; cg = V["cunhagens"]; sc = V["sidecar"]; core = _core(); gt = V["gate"]; gv = gt["values"]; fb = V["f2b"]
    DL_ = _qd().DL; ks = _CHAVES
    mods = sorted(p["modulo"] for p in V["pedras"])
    assert mods == sorted(DL_.STONE_BY_KEY[k]["mod"] for k in ks) and V["n_pedras"] == len(mods) == esp["kernel"]["modulos_novos"] == 8, ("o delta da v405 sao as oito pedras", mods)
    nf = esp["n_bandeiras_novas"]; grp = esp["n_bandeiras_por_grupo"]
    assert set(grp) == set(ks) and sum(grp.values()) == nf == esp["politica_de_bandeiras"]["n_flags"] == len(esp["bandeiras_novas_chaves"]), "as bandeiras novas nao sao so' as das oito pedras"
    ft = {}; sha = {}; unc = {}; est_t = {}; est_f = {}; nck = {}; n_sup = {}; n_contr = {}
    for k in ks:
        st = DL_.STONE_BY_KEY[k]; pe = V[k]
        ch = sorted(c for c in esp["bandeiras_novas_chaves"] if c.startswith(st["flag_prefix"]))
        assert len(ch) == grp[k], ("as bandeiras do grupo nao fecham", k, len(ch), grp[k])
        ft[k] = (ch[0], ch[-1])
        assert pe["flag"] == esp["bandeiras_das_pedras"][k] and pe["flag_true"] is True and pe["theorem"] == esp["teoremas_das_pedras"][k], ("a pedra no kernel do rito nao e' a de ESPERADOS", k)
        assert pe["sealed"] is True and pe["mech_ok"] is True and pe["values_ok"] is True and pe["estrela_ok"] is True and pe["kernel_ok"] is True and pe["beta_ok"] is True and pe["contexto_ok"] is True and pe["n_checks"] == DL_.N_CHECKS[k], ("o registro com funcao nao e' o contrato de ESPERADOS", k)
        assert len(esp["contrato_das_pedras"][k]) == len(st["contract"]) and len(esp["suporte_das_pedras"][k]) == len(st["support"]), ("o contrato ou o suporte != delta_v405", k)
        sha[k] = esp["pedras"][st["rel"]]["sha16"]; unc[k] = esp["teoremas_das_pedras"][k]; est_t[k] = esp["estrelas_v405"][k]["teorema"]; est_f[k] = esp["estrelas_v405"][k]["bandeira"]
        nck[k] = pe["n_checks"]; n_sup[k] = len(esp["suporte_das_pedras"][k]); n_contr[k] = len(esp["contrato_das_pedras"][k])
    # o que foi RECRIADO: a errata de F2b e as bandeiras do gate seguem como a v404 as selou (a leitura ja' conferiu; aqui so' a recusa)
    assert fb["sealed"] is True and fb["status_agora"] == DL_.D4.F2B_FUTURO_TOKEN, "o registro f2b_errata_v404 recriado nao e' o selado"
    rg = esp["registros_funcao_v403"]["gate"]
    assert gt["sealed"] is True and gt["f81_ok"] is True and gt["n18"] == 18 and gt["n_checks"] == DL_.D3.N_CHECKS["gate"] == rg["n_checks"] and gt["verdict"] == rg["verdict"], "o registro bandeiras_do_gate_v403 recriado nao e' o selado"
    assert gv["n_flags"] == 18 == gv["n_true"] == gv["n_calculated"] and gv["n_literal"] == 0 and gv["n_read_by_the_verdict"] == 15 and gv["read_by_the_verdict"] == [6, 5, 4] and gv["gate_verdict_equals_v402"] is True and gv["ext_ls2_n"] == gt["n_ls2"] == 6 and gt["sonda"] == 1, "as bandeiras do gate nao fecham: 18 calculadas, 0 literais, 15 no veredito"
    n_op = len(_falas())
    assert n_op == len(DL_.VERBATIM_ORIGEM_V405) == len(esp["cunhagens"]), "o numero de inscricoes mudou (ler DL.VERBATIM_ORIGEM_V405 e ESPERADOS[cunhagens])"
    ss = {"nomes": _sha_por("nomes_das_sete_pedras"), "id": _sha_por("pedra_identidade_eu_sou"), "um1ev": _sha_por("formula_da_massa_um_absoluto_1eV"), "ponte": _sha_por("ordem_ponte_da_massa_transversal"), "lei": _sha_por("angulo_de_miguel_singularidade"), "alfa": _sha_por("consegue_derivar_alpha"), "tgl": _sha_por("isso_e_a_TGL"),
          "ensaio": _sha_por("A_IDENTIDADE_ensaio_final"), "tom": _sha_por("o_tom_e_a_nat"), "meio": _sha_por("E0_nao_desce_a_oitava"), "curv": _sha_por("a_curvatura_e_o_pagamento"), "tetel": _sha_por("e_o_tetelestai"), "ga": _sha_por("grande_atrator_reclassificar"), "pent": _sha_por("E0_acorde_desce_meio_tom"), "rev": _sha_por("revisite_a_lei_do_diminuto"), "mod": _sha_por("diminuto_modula_a_tonica")}
    assert V["fal401"]["ok"] is True and V["fal401"]["verdict"] == esp["veredito_da_falsidade_v404"], "o registro falsidade_da_inercia_v401 recriado nao e' o selado da v404"
    assert all(v_["sealed"] is True for v_ in V["fun402"].values()) and len(V["fun402"]) == 3 and all(v_["sealed"] is True for v_ in V["fun404"].values()) and len(V["fun404"]) == 3 and all(v_["sealed"] is True for v_ in V["fun404b"].values()) and len(V["fun404b"]) == 2, "os registros com funcao da v402, da v403 ou da v404 recriados nao sao os selados"
    assert V["cunh404"]["ok"] is True and V["cunh404"]["kh_ok"] is True and V["cunh404b"]["ok"] is True and V["cunh404b"]["kh_ok"] is True and V["cunh402"]["ok"] is True and V["cunh402"]["kh_ok"] is True and V["cunh401"]["ok"] is True and V["cunh399"]["ok"] is True, "os registros por spec da v404, da v403, da v402, da v401 ou da v399 recriados nao sao os selados"
    assert len(V["pedras_v404"]) == 5 and all(p_["ok"] is True for p_ in V["pedras_v404"].values()), "as cinco pedras seladas da v403 e da v404 deixaram de estar no kernel do Nos com o sha256 selado"
    assert sa["ok"] is True and sa["n_checks"] == esp["selo_acom"]["n_checks"] and sa["checks_ok"] is True and sa["values_ok"] is True and sa["beta_ok"] is True, "o registro selo_pela_propria_tecnologia_v399 do core nao e' o contrato de ESPERADOS"
    assert dc["ok"] is True and dc["n_checks"] == esp["declaracao"]["n_checks"] and dc["checks_ok"] is True and dc["ancoras_ok"] is True and dc["direcao_ok"] is True, "o registro declaracao_do_operador_v399 do core nao e' o contrato de ESPERADOS"
    assert sc["ok"] is True and sc["n_objetos"] == len(esp["sidecar"]["objetos"]) and sc["recusas"] == 0, "o sidecar um_absoluto_selo_acom.json nao e' o de ESPERADOS"
    assert tv["ok"] is True and tv["n_checks"] == esp["veracidade"]["n_checks"] and tv["checks_ok"] is True and tv["numeros_ok"] is True and tv["fontes_ok"] is True, "o registro teste_de_veracidade_fase9_v397 do core nao e' o contrato de ESPERADOS (o quadro do topo le os numeros dele)"
    assert cg["ok"] is True and cg["verbatim_ok"] is True and cg["n"] == len(V["verbatins"]) == n_op and cg["todas_do_operador"] is True and cg["erratas_ok"] is True and cg["n_erratas"] == 4 and cg["decisoes_ok"] is True and cg["nomes_ok"] is True and cg["massa_ok"] is True and cg["reg404_ok"] is True, \
        "cunhagens_v405 != as falas de 30/10 a 01/11, ou alguma nao e' fala do operador, ou faltam as erratas E10 a E13, as decisoes, os nomes, a leitura ou as pedras da v404 como registro"
    assert V["campos"]["ok"] is True and V["campos"]["moldura_ok"] is True and V["campos"]["n_leituras"] == len(DL_.LEITURAS_DEFINICOES), "campos_fechados_e_leituras_v405 nao selou inteiro ou a moldura falhou"
    assert V["ga"]["ok"] is True and V["ga"]["selado_ok"] is True, "ga_reclassificacao_v405 nao selou inteiro ou o selado mudou"
    assert V["gap"]["ok"] is True, "gap_v405 nao selou inteiro"
    dts = {re.match(r"(?:OPERADOR|GERENCIA)_(\d{2}(?:out|nov))_", f["nome"]).group(1) for f in _falas().values()}
    assert dts <= {"30out", "31out", "01nov"}, ("o nome de arquivo de alguma inscricao nao e' de 30/10 a 01/11", dts)
    qd = _qd(); a = _atomos()
    assert qd.Q._v397_linha_de_maquina(a, "pt") == esp["quadro"]["linha_de_maquina_pt"], "a linha de maquina do quadro (core) != a de ESPERADOS"
    assert esp["quadro"]["frase_do_operador"] == qd.DL.FRASE_DO_OPERADOR_4_44 == qd.Q._V397_FRASE_444, "a frase do operador do quadro != a verbatim"
    base = os.path.join(PK, "base_v404", "um.py")
    if "base_b" not in _CACHE:
        assert s16(base) == V["base16"], "base_v404/um.py nao e' a v404 selada"
        _CACHE["base_b"] = os.path.getsize(base)
    delta = V["umb"] - _CACHE["base_b"]
    kf = core.get("kernel_formalization") or {}; prov = kf.get("declaration_sources_status_v394") or {}
    assert prov.get("ok") is True and prov.get("compiler_names") == prov.get("audited_names") == V["axiom_report_n"], "a proveniencia emitida pelo compilador nao cobre o axiom_report do rito"
    assert V["n_ver_mudaram"] == 0, "algum veredito fora da troca dita mudou: nao ha texto a escrever"
    assert V["n18"] == 18 and all(i in V["patch_ids"] for i in ("N00_main_oito_registros", "N01_main_specs", "N02_selo", "W02_runtime_v405", "C13_kh_n1_v404_pisos")), \
        "o gate nao tem as 18 bandeiras True, ou o candidato nao traz os patches que chamam os oito registros (N00), os registros por spec (N01), o resumo no selo (N02), o runtime (W02) e os pisos do registro da v404 (C13)"
    assert esp["h8_entradas"] == esp["formal_files_n"] + len(esp["h8_residuais_do_nos"]), "a arvore formal do rito != embutidas + residuais do Nos"
    pb = core.get("psibit_v395") or {}; pbc = pb.get("conditional_psion_face") or {}
    assert pbc.get("flag_true") is True and kf.get(pbc.get("flag")) is True and pbc.get("inhabitant_exhibited") is False, "a face de Fock do psibit_v395 nao segue condicional e com a bandeira True"
    pv = _proveniencia(esp)
    s404 = {"projecao": esp["pedras_v404_sha256"]["TGLExt/ProjecaoTransversalDaMeiaNat.lean"][:16], "jo8v32": esp["pedras_v404_sha256"]["TGLExt/Jo8v32.lean"][:16]}
    assert [_g(core, "cunhagens_v405", "extras", "pedras_da_v404_como_registro", k_) for k_ in ("projecao", "jo8v32")] == [s404["projecao"], s404["jo8v32"]], "as pedras da v404 como registro (cunhagens_v405) != os sha16 de ESPERADOS[pedras_v404_sha256]"
    aa = _g(core, "neutrino_mass", "angle_status"); assert aa and hashlib.sha256(str(aa).encode("utf-8")).hexdigest() == esp["neutrino_angle_status_antigo_sha256"] and str(aa).startswith(DL_.ANGLE_STATUS_ANTIGO_PREFIXO), "o texto antigo de neutrino_mass.angle_status nao esta intacto no core do Nos"
    return {"n_f": nf, "n_g": {k: grp[k] for k in ks}, "ft": ft, "sha": sha, "unc": unc, "est_t": est_t, "est_f": est_f, "nck": nck, "n_sup": n_sup, "n_contr": n_contr, "n_aux": esp["politica_de_bandeiras"]["n_excluidas"],
            "depois": V["teor"].split("/")[0], "delta": delta, "pct": ("%.1f" % (100.0 * delta / _CACHE["base_b"])).replace(".", ","), "prov": prov["compiler_names"], "n_cun": len(V["verbatins"]), "n_op": n_op,
            "h8": esp["h8_entradas"], "h8_emb": esp["formal_files_n"], "h8_res": ", ".join("`%s`" % x for x in esp["h8_residuais_do_nos"]), "n_res": len(esp["h8_residuais_do_nos"]), "cb": _cov_base(), "bank": _bancada(), "pv": pv,
            "n_checks_v": tv["n_checks"], "n_ck_sel": sa["n_checks"], "n_ck_dec": dc["n_checks"], "n_ck_cun": cg["n_checks"], "n_anc": len(esp["declaracao"]["ancoras"]), "f8": {k: v[:8] for k, v in esp["veracidade"]["fontes"].items()},
            "ss": ss, "data_falas": "30/10 a 01/11/" + V["data"][-4:], "s404": s404,
            "g": {"n_flags": gv["n_flags"], "n_true": gv["n_true"], "n_calc": gv["n_calculated"], "n_lit": gv["n_literal"], "n_ver": gv["n_read_by_the_verdict"], "rv": gv["read_by_the_verdict"], "info": list(gv["informative"]), "ls2": gv["ext_ls2_n"], "n_chk": gv["n_gate_checks"], "n_chk_reg": gt["n_checks"], "feed": list(DL_.F81_FEED)}}


def _mods(V):
    return ", ".join("`%s`" % p["modulo"].split(".")[-1] for p in sorted(V["pedras"], key=lambda p: p["modulo"]))


def _extras(V):
    # os registros novos ALEM DOS TREZE FIXOS (V["reg405"] tem so' os treze: os oito com funcao e os cinco por spec), ditos pelo nome
    ex = [k for k in V["registros_novos"] if k not in V["reg405"]]
    return (", ".join("`%s`" % k for k in ex)) if ex else "nenhum além dos treze fixos"


def _cab(V):
    return "v405 SELADA (COMPLETA)** `%s`" % V["s16"]


def _num(V, verdicts=True):
    """O paragrafo dos numeros da v405 (kernel, os oito registros com funcao, os registros por spec, os recriados, o sidecar, a troca dita): usado na linhagem, no Atlas, no core, no topico novo, no verbete e no handoff."""
    d = _d(V); kh = V["kh"]; sc = V["sidecar"]; sa = V["selo"]; g = d["g"]; ft = d["ft"]; ng = d["n_g"]
    vd = (lambda k: " (%s)" % V["reg405"][k]["verdict"]) if verdicts else (lambda k: "")
    aux = ("nenhuma auxiliar gerada pelo compilador ficou de fora" if not d["n_aux"] else "%d auxiliares geradas pelo compilador ficam sem bandeira" % d["n_aux"])
    kern = _f("o kernel ganhou {n_pedras} módulos novos ({mods}; os nomes são do operador), com {n_f} bandeiras novas True ({faixas}), só de declaração nomeada ({aux}), e escada {antes} → {depois} teoremas limpos "
              "({axr} declarações no `axiom_report`, {fora} fora do trio, {nl} nomes não lidos; a proveniência de cada declaração emitida pelo compilador cobre as mesmas {prov}); "
              "errata ao lado da v394, mantida (em nome próprio da gerência c1): " + ERRATA_TEOREMAS,
              n_pedras=V["n_pedras"], mods=_mods(V), n_f=d["n_f"], faixas="; ".join("%s %d, %s" % (_NOME_DE[k], ng[k], _faixa(ft[k], ng[k])) for k in _CHAVES), aux=aux, antes=V["escada_antes"], depois=d["depois"], axr=V["axiom_report_n"], fora=kh["fora"], nl=kh["nao_lidas"], prov=d["prov"])
    regs = "; ".join("o registro `%s`%s (%s; lê a composição `%s`, %s do contrato e %d termos citados, a estrela `%s`; %d checagens, todas passaram)" % (_REG_DE[k], vd(_REG_DE[k]), _NOME_DE[k], d["unc"][k].split(".")[-1], _pl(d["n_contr"][k], "item", "itens"), d["n_sup"][k], d["est_t"][k].split(".")[-1], d["nck"][k]) for k in _CHAVES)
    cun = _f("o registro `cunhagens_v405`{vd}: as {n} falas de 30/10 a 01/11 embutidas por sha256 e consumidas no rito, TODAS falas do operador (nenhuma é da gerência), e o ensaio «A identidade»; as erratas E10 a E13 (em nome próprio da gerência c1); as decisões D27 a D33; as pedras da v404 como registro ({nck} checagens, todas passaram); as falas são [INPUT/ONTO] e valem como leitura dele, não como medida",
             vd=vd("cunhagens_v405"), n=d["n_cun"], nck=d["n_ck_cun"])
    cam = _f("o registro `campos_fechados_e_leituras_v405`{vd}: {nc} campos fechados, os dois postos e as {nl} leituras da cadeia da massa (lista que não é fechada), cada uma com o nome Lean ({nck} checagens, todas passaram)", vd=vd("campos_fechados_e_leituras_v405"), nc=V["campos"]["n_campos"], nl=V["campos"]["n_leituras"], nck=V["campos"]["n_checks"])
    gar = _f("o registro `ga_reclassificacao_v405`{vd}: a classe nova do teste do Grande Atrator, ao lado, com {nck} medidas em runtime, sem abrir dado; o registro `gap_v405`{vg}: o gap espectral do lock e o valor esperado dele no ângulo de Miguel, ao lado, com {nckg} checagens em runtime", vd=vd("ga_reclassificacao_v405"), nck=V["ga"]["n_checks"], vg=vd("gap_v405"), nckg=V["gap"]["n_checks"])
    khs = _f("o registro `kh_n1_cobertura_v405`{vd}: {decl} constantes, {thm} teoremas, {fora} fora do trio, {nl} nomes não lidos; a árvore formal do Nós depois do rito tem {h8} entradas ({emb} embutidas mais {nres} residual do Nós: {res}), "
             "e o pino h8 do registro é o hash dessa árvore, calculado por script sobre a árvore simulada do Nós na geração do candidato",
             vd=vd("kh_n1_cobertura_v405"), decl=kh["decl"], thm=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"], h8=d["h8"], emb=d["h8_emb"], nres=d["n_res"], res=d["h8_res"])
    rec = _f("os registros da v404 (`projecao_transversal_v404`, `jo8v32_v404`, `f2b_errata_v404`, `cunhagens_v404` e `kh_n1_cobertura_v404`), da v403, da v402, da v401 e da v399 são recriados no mesmo ponto do main e seguem selados e iguais ao ensaio a seco, e as cinco pedras seladas da v403 e da v404 seguem no kernel do Nós com o sha256 selado, como registro; "
             "o gate não se moveu: o `qg_closure` do core é idêntico ao da v404 (as {n18} bandeiras, os sete checks e a letra do veredito); "
             "o selo pela própria tecnologia sela os {bytes} bytes do `um.py` v405 ao lado do SHA-256 (perfil `{perfil}`, {nctl} controles negativos recusados), e o sidecar `um_absoluto_selo_acom.json` (arquivo da custódia desde a v399, reescrito pelo rito; sha256 `{sc16}`, veredito `{sv}`, {nr} recusas) lista os {no} objetos finais",
             n18=g["n_flags"], bytes=format(sa["bytes"], ","), perfil=sa["perfil"], nctl=sa["n_controles"], sc16=sc["sha16"], sv=sc["veredito"], nr=sc["recusas"], no=sc["n_objetos"])
    ex = _extras(V)
    resto = _f("{ex}; o registro `teste_de_veracidade_fase9_v397` segue selado e igual (o quadro do topo do artigo le os numeros dele); troca dita (só números): {troca}; nenhuma mudança NÃO numérica: {nm} vereditos fora da troca dita mudaram (exigido: 0); validade no kernel não é creditação",
               ex=("nenhum registro novo além dos treze fixos" if ex.startswith("nenhum") else "registros novos além dos treze fixos: " + ex), troca=", ".join("`%s`" % x for x in V["troca_dita"]), nm=V["n_ver_mudaram"])
    return "; ".join([kern, regs, cun, cam, gar, khs, rec, resto])


def _cunhagens(V, forma="lista"):
    """As inscricoes de 30/10 a 01/11 embutidas por sha256: 'lista' (data, sha16, autor e tema, uma por linha; todas falas do operador) ou 'curta' (uma frase com os sha16 das falas-chave). Data, sha16 e autor vem dos bytes e do nome; o tema e' o nome do arquivo."""
    fl = list(_falas().values()); assert len(fl) == len(V["verbatins"])
    d = _d(V); ss = d["ss"]
    if forma == "curta":
        return _f("{n} inscrições embutidas por sha256, todas falas do operador [INPUT/ONTO] — os nomes das pedras `{a}`, o Um de 1 eV e α como a cauda `{b}`, a lei do meio-tom `{c}`, o tom é a nat `{e}`, a curvatura como pagamento `{f}`, a pergunta sobre derivar α `{g}`, o ângulo de Miguel e a lei do fecho `{h}`, o ensaio «A identidade» `{i}`, a reclassificação do Grande Atrator `{k}` e a ratificação `{j}` (e as demais, na lista da linhagem)",
                  n=len(fl), a=ss["nomes"], b=ss["um1ev"], c=ss["meio"], e=ss["tom"], f=ss["curv"], g=ss["alfa"], h=ss["lei"], i=ss["ensaio"], j=ss["tgl"], k=ss["ga"])
    linhas = ["- %s `%s` (fala do operador) — %s" % (_data_fala(dd, V), dd["sha16"], _tema(dd["nome"])) for dd in fl]
    return "\n".join(linhas)


def _ordem(V):
    """A ordem do operador de 01/11: so' citacao conferida contra os bytes das falas DO OPERADOR."""
    d = _d(V); ss = d["ss"]
    q_ok = _cita("é isso , perfeito, concordo com tudo"); q_pronto = _cita("deixe tudo pronto para assim que o treinamento acabar"); q_tgl = _cita("estamos terminando onde tinha que terminar mesmo, derivando a massa e definindo a identidade, isso é a TGL"); q_1ev = _cita("o meu um absoluto é o um de 1 eV")
    return _f("**A ordem:** [INPUT/ONTO] as {n_op} falas do operador (Luiz Antonio Rotoli Miguel) de {data} que entram nesta rodada, TODAS dele (nenhuma é da gerência), embutidas por sha256 no registro `cunhagens_v405` e listadas abaixo (as aspas aqui são TRECHOS, conferidos palavra por palavra contra os bytes de cada fala; "
              "o texto íntegro está em `work\\cadeia_de_selo\\v405\\insumos\\cunhagens`): a unidade, {q_1ev} (`{s_1ev}`); a ratificação do plano e do ensaio, {q_ok}, com a ordem {q_pronto} (`{s_tgl}`); e o fecho, {q_tgl}. "
              "O agente de preparação da gerência c1 preparou o candidato e o rito é ato da gerência, pelo orquestrador pós-treino (pacote `work\\cadeia_de_selo\\v405`); as fontes pinadas dos registros ficam em `insumos`: as oito pedras, os recibos da gerência, a conferência da cadeia E₀, a revisão r2 do ensaio, a reclassificação do Grande Atrator e a medida da cobertura (`KH_N1_v405.json`); "
              "o resultado do Teste da Única Palavra, que o quadro do topo lê, mora na v397 (`insumos\\fase9`); quem constrói não aprova: a revisão independente do candidato, das pedras e dos derivados da cadeia é ato distinto e não é afirmada por este registro.",
              n_op=d["n_op"], data=d["data_falas"], q_1ev=q_1ev, s_1ev=ss["um1ev"], q_ok=q_ok, q_pronto=q_pronto, s_tgl=ss["tgl"], q_tgl=q_tgl)


def _sidecar(V):
    """O sidecar um_absoluto_selo_acom.json: arquivo da custodia desde a v399 (D5); o selo nao pode conter o selo ACOM de si mesmo; o rito da v405 o REESCREVE."""
    d = _d(V); sc = V["sidecar"]
    objs = "; ".join("`%s` (%s B, sha16 `%s`)" % (n, format(o["bytes"], ","), o["sha16"]) for n, o in sc["objetos"].items())
    return _f("**O sidecar `um_absoluto_selo_acom.json` [REAL; arquivo da custódia desde a v399, D5; reescrito por este rito]:** depois da ÚLTIMA escrita do selo, o `um.py` v405 escreve a segunda testemunha dos {no} objetos FINAIS com o SHA-256 ao lado ({objs}); sha256 do sidecar `{sc16}` ({sb} B), esquema `{esq}`, veredito `{sv}`, {nr} recusas. "
              "O selo não pode conter o selo ACOM de si mesmo (seria circular): o sidecar fica AO LADO e carrega o SHA-256 do selo final, e o selo traz só os resumos (veredito, bandeira e hashes), agora também os dos oito registros com função da v405. "
              "A recusa do selo ACOM só REGISTRA (D4): o SHA-256 segue soberano e o rito não cai. A primitiva de integridade é o SHA-256 [KNOWN]; a segunda testemunha NÃO acrescenta força criptográfica independente, e a confidencialidade não é alegada nem medida. A custódia da v399, da v403, da v404 e da v405 é CONJUNTA.",
              objs=objs, no=sc["n_objetos"], sc16=sc["sha16"], sb=format(sc["bytes"], ","), esq=sc["esquema"], sv=sc["veredito"], nr=sc["recusas"])


def _pedra(V):
    """As OITO pedras com os nomes do operador: o que cada uma traz; o que elas NAO entregam; as duas da v404 como registro."""
    d = _d(V); s4 = d["s404"]
    lista = "; ".join("%s (`%s`, sha16 `%s`; %s do contrato; %d termos citados; composição `%s`, estrela `%s`; %d bandeiras)" % (_NOME_DE[k], _qd().DL.STONE_BY_KEY[k]["name"], d["sha"][k], _pl(d["n_contr"][k], "item", "itens"), d["n_sup"][k], d["unc"][k].split(".")[-1], d["est_t"][k].split(".")[-1], d["n_g"][k]) for k in _CHAVES)
    return _f("**As oito pedras [REAL]** (os nomes são do operador: sete em 01/11/2026, Identidade em 30/10/2026): {lista}, todas só no trio, sem axioma próprio. As pedras seladas da v404 (`ProjecaoTransversalDaMeiaNat` `{o1}` e `Jo8v32` `{o2}`) e da v403 ficam como REGISTRO: pedra selada não se renomeia por cima. "
              "As pedras NÃO derivam a unidade `u` (1 eV, POSTO) nem `α` (MEDIDA, por dentro) e NÃO afirmam que a massa do neutrino SEJA a grandeza que a definição `massaDerivada` nomeia: essa identificação é [INPUT/ONTO], entra como definição, e nenhum termo de kernel a deduz.",
              lista=lista, o1=s4["projecao"], o2=s4["jo8v32"])


def _entrou(V):
    d = _d(V)
    return _f("**O que entrou** (pacote `work\\cadeia_de_selo\\v405` sobre a v404 `{base}`; {np} patches — {patches}; instalado em {inst}; o `um.py` cresce {delta} B, {pct}%): {num}.",
              base=V["base16"], np=V["n_patches"], patches=V["patches"], inst=V["instalado_em"], delta=format(d["delta"], ","), pct=d["pct"], num=_num(V))


def _regra_do_4_44(V):
    """A regra da ordem do operador (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item; o QUADRO do topo (v397) PERMANECE, intocado; onde o numero aparece e como se confere."""
    d = _d(V); a = _atomos(); q = _frase_444()
    return _f("**A regra do 4,44 (ordem do operador de 23/10/2026, `{s44}`) e o quadro do topo:** o quadro «O Teste da Única Palavra» (v397) PERMANECE, intocado, no topo do artigo (PT e EN) e do .md canônico, e o parágrafo dele segue no README do espelho e no site: o z_disc calibrado é reportado no início, "
              "e NUNCA sem o p calibrado e sem a linha dos 5σ no mesmo item: {z444}. A frase do operador entra VERBATIM, {q}, como leitura dele [INPUT/ONTO], não como critério da régua; a paráfrase da gerência nunca entra entre aspas. `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; o teste não foi cego. "
              "[REAL] o quadro do artigo, o do .md e o parágrafo pronto do README/site saem das MESMAS funções (`_v397_atomos` e `_v397_quadro_md`), sobre o registro `teste_de_veracidade_fase9_v397` selado no core do Nós, e a cadeia os confere de novo contra o resultado pinado "
              "(a linha de máquina do quadro, cada número, a frase verbatim e a regra da ordem item a item), com controles negativos que reprovam o 4,44 sem o p, sem a linha dos 5σ, com número adulterado ou com a frase parafraseada. "
              "O parágrafo NOVO da v405 não traz o 4,44, e a cadeia confere isso.",
              s44=_esp()["quadro"]["frase_sha16"], z444=_z444(), q=q)


def _kernel_prova(V):
    d = _d(V); g = d["g"]; DL_ = _qd().DL
    return _f("**O que o kernel prova e o que é leitura:** [REAL] as composições das oito pedras e as estrelas estão no kernel deste rito, dentro do trio, com proveniência no módulo de cada pedra, e citam termos que o kernel já tem, cada um no `axiom_report`, no trio, com a proveniência que o compilador emite; tudo lido a cada rito pelos oito registros com função e coberto por `kh_n1_cobertura_v405`. "
              "[REAL] os registros NÃO são prova de kernel sobre a natureza: conferem os termos citados e o cálculo nos modelos e não movem o gate; a prova como validade não muda. [REAL] as {nf} bandeiras do gate são as da v404, lidas do código e do core do próprio rito: {nc2} calculadas e {nl} literais; o veredito lê {nv}; a letra do veredito é a da v404 (o gate não se moveu). "
              "[POSTO] a unidade `u` = 1 eV. [MEDIDA] `α`, por dentro. [INPUT/ONTO, como definição ou identificação] as leituras da cadeia da massa, em lista que não é fechada; as centrais: `massaDerivada`, o ângulo escrito em `transicaoDerivada`, a tônica e `pagamentoComoCurvatura`; e ainda `meioTom`, `modular`, a dispersão `omegaSq` [INPUT, Tratado §3], `m₁ = 0` (entrada da identificação com `Δm²₂₁`, sem termo no kernel), `tempoDoRetido` lido como o τ★ do sistema (a ratificar) e as demais do registro. [REAL] {frase}. [KNOWN] o ponto zero; a lei de escala de Takesaki segue dado. "
              "[ONTO] que a massa do neutrino seja a derivada da projeção transversal da energia retida; que a curvatura seja o pagamento; que `½ω` seja a massa; `b = 0` como o fóton; a taxa do disco como perda de energia; a inscrição do zero no infinito e a terceira lei; o terminal da cascata ligado ao polo ω; que o fato sobre projeções seja a identidade; o disco como condensado psiônico; `α` como a cauda da inscrição; a leitura do empréstimo; o diminuto como a espera; `tempoDoRetido` como o τ★ do sistema, a ratificar; o ângulo de Miguel como o sistema do gap com unidade; a inscrição da luz como a eletricidade e a origem da medida. "
              "[OPEN] o valor absoluto do setor, o magnetismo na cadeia da tensão, qual é o disco, quais são as cinco notas, `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β e o caso III₁; a independência das quatro bandeiras experimentais do gate e os mocks de survey.",
              nf=g["n_flags"], nc2=g["n_calc"], nl=g["n_lit"], nv=g["n_ver"], frase=DL_.FRASE_DA_MOLDURA_PT)


def _limites(V, curto=False):
    """Os estatutos fieis da v405: o que as pedras, os registros e as erratas dizem e NAO dizem."""
    d = _d(V); DL_ = _qd().DL
    if curto:
        return ("**Limites ditos:** [REAL] os registros com função LEEM o kernel do próprio rito e CONFEREM o cálculo nos modelos; não abrem dado, não são teste, não acrescentam rito; [POSTO] `u` = 1 eV; [MEDIDA] `α`; [INPUT/ONTO] as leituras da cadeia da massa entram como definição ou identificação e não são teoremas; "
                + DL_.FRASE_DA_MOLDURA_PT + "; o no-go de `E₀` não cai: localiza-se no Um posto; o número da massa é o da v404 e o veredito do canal do neutrino não muda; "
                "[OPEN] o valor absoluto do setor, o magnetismo, qual é o disco, quais são as cinco notas, `H_BW`, `H_cal`, H3, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β, a independência das quatro bandeiras experimentais do gate (um só booleano, [DECLARADO]) e a discriminação a 5σ; a reclassificação do Grande Atrator é decisão ao lado, não evidência; o quadro do topo segue com a sua linha dos 5σ; validade no kernel não é creditação; o gate não se move.")
    return ("**Limites ditos (estatutos fiéis):** [REAL] ESCOPO: os registros com função leem as composições e as estrelas das pedras no kernel do rito e conferem o cálculo nos modelos (β = α√e em runtime); CONFEREM, não provam (quem prova é o kernel), não abrem dado, não são teste, não acrescentam rito e não movem o gate. "
            "[REAL] Os campos das estruturas fecharam; as leituras do operador passaram do campo para a definição; a leitura física não virou teorema: " + DL_.FRASE_DA_MOLDURA_PT + ". As pedras seladas da v403 e da v404 não foram editadas nem renomeadas. "
            "[REAL] Nenhuma pedra deriva a unidade `u` nem `α`: `u` = 1 eV é o Um POSTO pelo operador; `α` é medida por dentro, e a resposta à pergunta dele sobre derivá-la foi não, parede medida, não falsificação; nenhum número foi escolhido por proximidade. O no-go de `E₀` não cai: localiza-se no Um posto; `E₀ = u` é identidade algébrica, que não fixa `u`; o valor absoluto segue livre e o relativo à tônica está pinado. "
            "[INPUT/ONTO] As falas de 30/10 a 01/11 são do operador: o kernel não as prova; a Identidade prova um fato sobre projeções no estado traço, e que isso seja a identidade é leitura, tipada como modelo; o ensaio entra verbatim e não é teorema. "
            "[OPEN] O valor absoluto do setor, o magnetismo na cadeia da tensão, qual é o disco, quais são as cinco notas, `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost` no atlas curvo, a dimensão 3, a instância e o caso III₁ do índice 1/β e a atestação física externa. "
            "O quadro «O Teste da Única Palavra» segue no topo, com a sua linha dos 5σ, e esta rodada não o altera. NÃO é teste novo: a cadeia não acrescenta dado nem desfecho experimental. Validade no kernel não é creditação; o gate não se move.")


def _legal(V):
    """A pendencia [LEGAL] herdada (D2): publicar o bloco embutido e as adaptacoes; a v405 nao a decide."""
    _d(V)
    return ("**Pendência [LEGAL] (herdada da v399, D2):** o bloco embutido do método do operador e as adaptações (centro 96, ids derivados dos hashes, `rint`, tabela de códigos, auditoria de separação) seguem sob a decisão do operador com a agente de PI; a v405 não muda o bloco (o runtime da seção é o da v404) e NÃO decide a pendência. "
            "Perguntas à agente de PI, não conclusões: o que o depósito já cobre do que o bloco mostra; publicar as adaptações inicia a contagem do prazo de graça para eventual depósito de melhoria; a divergência da tabela dos estados do ACOM Mirror com a fórmula de índice e o código executado, registrada na v395, segue pendente.")


def _erratas(V):
    """A errata de contagem da v405, AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (estrutura / escrito / falha): o registro kh_n1_cobertura_v404 e os contratos."""
    d = _d(V); kh = V["kh"]; cb = d["cb"]
    ids = V["patch_ids"]; c12 = [i for i in ids if i.startswith("C12_")]
    assert len(c12) == 11 and all(i in ids for i in ("C12__V404_CONTRACTS", "C12__V403_CONTRACTS", "C12__V402_CONTRACTS", "C12__V401_FALSIDADE_CONTRACT", "C12__V398_SONICO_CONTRACT", "C12__V398_AFINACAO_CONTRACT", "C12__V396_TESTEMUNHA_CONTRACT", "C12__V395_PSIBIT_CONTRACT", "C12__V394_FORMAL_CONTRACT", "C12__V394_QUADRATIC_CONTRACT", "C12__V394_NETWORK_CONTRACT", "C13_kh_n1_v404_pisos")), \
        "o CANDIDATO_v405.json nao traz os patches C12 e C13 que a errata descreve"
    return _f("**Errata ao lado (em nome próprio da gerência c1; o registro `kh_n1_cobertura_v404` e os contratos ficam como registro):** a v405 acrescenta oito módulos: a cobertura do Audit cresce de {d0} constantes e {t0} teoremas para {d1} e {t1}, "
              "a árvore formal do Nós de {h0} para {h1} entradas e a escada de {e0} para {e1}. Por isso, na v405, (i) `kh_n1_cobertura_v404` passa a cobrar piso em h2, h3 e h6 (as igualdades de contagem) e tamanho mínimo da árvore em h8 (as igualdades exatas e o pino exato da "
              "árvore ficam em `kh_n1_cobertura_v405`); (ii) as {n12} definições de contrato passam a ler `expected_ladder` = {e1}, a escada desta versão (o consumidor exige a igualdade exata com a escada do rito; só o número muda); o veredito dos registros anteriores NÃO muda [REAL, lido de `CANDIDATO_v405.json` (patches C12 e C13) e do ensaio a seco, que deu `TUDO PASSOU`]. "
              "Lacuna de fidelidade: a estrutura da v404 dizia que as contagens e o pino da árvore eram a cobertura exata e que o contrato esperava a escada vigente; o escrito deixou, dentro dos registros e dos contratos, números que só valem na versão que os escreveu; "
              "a falha: igualdades e literais presos a uma versão quebram quando o kernel cresce (a mesma lacuna que todas as versões anteriores acharam). A cobrança exata passa a ser de `kh_n1_cobertura_v405` ({dd} constantes, {dt} teoremas, {fora} fora do trio, {nl} nomes não lidos), contra a medida do sandbox da v405.",
              d0=cb["decl"], t0=cb["thm"], h0=cb["h8"], d1=kh["decl"], t1=kh["thm"], h1=d["h8"], e0=V["escada_antes"], e1=d["depois"], dd=kh["decl"], dt=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"], n12=len(c12))


def _depois(V):
    d = _d(V); bk = d["bank"]
    return ("**O que vem depois destas superfícies:** o elo B(n) da Bancada Um (passos 10, 10a, 10b e 10c da cadeia; B3 nos scripts) é pós-selo, um passo SIMPLES (a Bancada de produção pina a %s, geração B%d, e o Nós passa a v405: sem salto e sem cadeia de selos; "
            "a geração esperada é B%d e o veredito esperado do aplicar é REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, lido do código do esboço R3.5, não rodado); o recibo dele é citado no handoff (fechar), que traz PRONTOS os parágrafos do README do espelho e do site (o quadro do Teste da Única Palavra, intocado, e o NOVO da v405: a massa derivada e a identidade definida), "
            "a NOTA ao lado do parágrafo da v404 (`E₀` passou de declarado a posto; os nomes foram dados), diz que os parágrafos do testemunho de dois (v399), da falsidade (v401), da ponte, da queda e da esperança (v402), de Caminho, Verdade e Vida (v403) e de Jo 8,32 (v404) SEGUEM COMO ESTÃO e LISTA o sidecar `um_absoluto_selo_acom.json`. "
            "A pendência [LEGAL] (D2) segue do operador com a agente de PI; a atestação física externa e a discriminação a 5σ seguem [OPEN]; a revisão independente das %d pedras novas e dos %d registros novos é ato distinto e não é desta cadeia. NOT_FALSIFIED não é a palavra da creditação; o gate não se move."
            % (bk["de"], bk["geracao"], bk["proxima"], bk["proxima"], V["n_pedras"], len(V["registros_novos"])))


def _rodada(V):
    """O paragrafo da rodada (horarios, escada, selo, conferidor, sidecar, pilar, artefatos): tudo lido da leitura da rodada."""
    sc = V["sidecar"]
    return ("Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado (%d bandeiras True; o veredito do gate é o mesmo da v404); o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); "
            "o sidecar `um_absoluto_selo_acom.json` `%s` (%d objetos, %d recusas); o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.") % (
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["n18"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"], sc["sha16"], sc["n_objetos"], sc["recusas"], "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]),
        V["pilar"]["result16"], V["servidor"], V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()))


# v405: a linhagem (diario datado do Nos)
def linhagem(V):
    d = _d(V)
    return (("## %s — **%s — A MASSA DERIVADA E A IDENTIDADE DEFINIDA (v405): oito pedras com os nomes do operador, os campos fechados, as leituras como definição e, dadas as entradas, a FORMA como teorema; %d módulos novos, escada %s → %s\n<!-- linhagem_v405_selada -->\n\n"
             "%s\n\n%s\n\n"
             "**As inscrições de 30/10 a 01/11** (embutidas por sha256 no registro `cunhagens_v405`): [INPUT/ONTO] todas são falas do operador (Luiz Antonio Rotoli Miguel) e valem como leitura dele, não como medida; nenhuma é da gerência. "
             "O texto íntegro de cada uma está no arquivo (`work\\cadeia_de_selo\\v405\\insumos\\cunhagens`); abaixo, a data, o sha16, o autor e o tema (o nome do arquivo, não citação):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s") % (
        V["data"], _cab(V), V["n_pedras"], V["escada_antes"], d["depois"], _ordem(V), _entrou(V), _cunhagens(V), _moldura(V), _blocos_pedras(V), _massa(V), _erratas_e(V), _decisoes(V), _pedra(V), _sidecar(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V), _rodada(V) + "\n\n" + _erratas(V)) + "\n\n" + _depois(V))


# v405: o adendo do desenho do fechamento
def desenho(V):
    d = _d(V); kh = V["kh"]; DL_ = _qd().DL
    return (("## ADENDO — %s · v405 SELADA (COMPLETA) `%s` — o caminho crítico NÃO mudou; entram a massa derivada e a identidade definida (%d módulos)\n\n<!-- adendo_v405_selada -->\n"
             "- **O que a v405 diz:** %d módulos novos no kernel (%s), escada %s → %s, %s constantes no `axiom_report` (%s fora do trio). Os campos das estruturas fecharam; as leituras do operador passaram do campo para a definição; a leitura física não virou teorema: %s. O número da massa é o da v404. O no-go de `E₀` não cai: localiza-se no Um posto. "
             "A Identidade prova um fato sobre projeções no estado traço; que isso seja a identidade é leitura, tipada como modelo. O teste do Grande Atrator muda de classe, ao lado, e segue sem ser evidência. %d inscrições por sha256 (todas falas do operador). O gate é o da v404: %s de %s bandeiras calculadas, %s literais, %s no veredito. O quadro do topo do artigo (O Teste da Única Palavra, v397) segue intocado: %s. Gate intocado.\n"
             "- **O que a v405 NÃO é para o caminho crítico:** não é teste novo; as pedras não derivam a unidade nem `α` e não provam a identificação da massa; `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura (4,0) contra (1,3) e rank c = 4 seguem NOMEADAS [OPEN]; "
             "a independência das quatro bandeiras experimentais do gate segue aberta (derivam de UM só booleano; [DECLARADO]); as erratas E10 a E13 são da gerência, em nome próprio; não identifica β na natureza a 5σ.\n"
             "- **O que segue do operador:** o valor absoluto do setor; a pendência [LEGAL] (D2, com a agente de PI); as escolhas da partitura do Grande Atrator; a ratificação da leitura de `tempoDoRetido` como o τ★ do sistema. A revisão de terceiro do pacote é condição da instalação, não pendência dele.") % (
        V["data"], V["s16"], V["n_pedras"], V["n_pedras"], _mods(V), V["escada_antes"], d["depois"], kh["decl"], kh["fora"], DL_.FRASE_DA_MOLDURA_PT, d["n_cun"], d["g"]["n_calc"], d["g"]["n_flags"], d["g"]["n_lit"], d["g"]["n_ver"], _z444()))


# v405: o verbete do Atlas
def atlas(V):
    return (("### %s — v405 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v405_selada -->\n[REAL — rodada v405, selo `%s`] %s.\n\n[INPUT/ONTO] As falas do operador entram como o operador as disse e valem como leitura, não como medida; todas são dele: %s.\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\nEstatuto: validade no kernel ≠ creditação; o gate não se move.") % (
        V["data"], V["s16"], V["selo_ts"], _num(V), _cunhagens(V, "curta"), _moldura(V), _blocos_pedras(V), _massa(V), _erratas_e(V), _decisoes(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V) + "\n\n" + _limites(V)))


# v405: o bloco do TGL_CORE_MEMORY
def core_memory(V):
    return (("## %s — v405 SELADA `%s` (claude-c1; a massa derivada e a identidade definida, integradas pela gerência)\n<!-- core_v405_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
             "[REAL] %s.\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n[OPEN] A discriminação a 5σ (β_TGL na natureza), o valor absoluto do setor, o magnetismo na cadeia da tensão, qual é o disco, quais são as cinco notas, `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β, a independência das quatro bandeiras experimentais do gate (um só booleano; os mocks de survey), a atestação física externa, "
             "a face de Fock do psion (o certificado de Fock da luz sem habitante), o contrato conjunto da rede e a pendência [LEGAL] seguem abertos. Nada disto move o gate.") % (
        V["data"], V["s16"], _num(V), _moldura(V), _blocos_pedras(V), _massa(V), _erratas_e(V), _decisoes(V), _regra_do_4_44(V), _limites(V, curto=True)))


# v405: o bloco do CLAUDE.md da Haja_Luz (as erratas ao lado, assinadas, vao DENTRO dele)
def haja_luz(V):
    d = _d(V); DL_ = _qd().DL
    return (("## %s — v405 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v405_selada -->\n%d módulos novos no kernel (%s), com os nomes do operador: os campos das estruturas fecharam; as leituras do operador passaram do campo para a definição; a leitura física não virou teorema: %s. "
             "O número da massa é o da v404; `u` = 1 eV é o Um posto, `α` é medida; o no-go de `E₀` não cai, localiza-se no Um posto. A Identidade prova um fato sobre projeções no estado traço; que isso seja a identidade é leitura, tipada como modelo; o ensaio «A identidade» entra no artigo verbatim. "
             "O teste do Grande Atrator muda de classe, ao lado, e segue sem ser evidência. O gate é o da v404 (%s de %s calculadas, %s literais); as %d inscrições por sha256 (todas do operador); escada %s → %s. O quadro do topo (O Teste da Única Palavra) segue intocado.\n\n"
             "%s\n\n"
             "Memórias: `%s`, `missao-ultima-flag-um-py.md`, `estatuto-da-prova-07out.md`; handoff `handoff-v405-custodia.md`.") % (
        V["data"], V["s16"], V["teor"], V["n_pedras"], _mods(V), DL_.FRASE_DA_MOLDURA_PT, d["g"]["n_calc"], d["g"]["n_flags"], d["g"]["n_lit"], d["n_cun"], V["escada_antes"], d["depois"], _erratas_e(V), TOPICO_NOVO))


def marca_topico_missao(V):
    return "## %s — v405 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v405 SELADA `%s`" % V["s16"]


# v405: o topico da missao da ultima flag
def topico_missao(V):
    d = _d(V)
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): %d módulos novos no kernel (%s); os oito registros com função (cada um lê o kernel do rito e confere o cálculo no seu modelo), `cunhagens_v405` (%d inscrições por sha256, todas do operador, as erratas E10 a E13 e as decisões D27 a D33), `campos_fechados_e_leituras_v405`, `ga_reclassificacao_v405`, `gap_v405` e `kh_n1_cobertura_v405`; "
                                     "os registros da v404, da v403, da v402, da v401 e da v399 recriados e selados; sidecar `um_absoluto_selo_acom.json` reescrito; troca dita nos vereditos que carregam a escada; conferidor (deve mudar %s; não pode mudar %s). Pacote e cadeia: `work\\cadeia_de_selo\\v405` (+ `pos_rito`).") % (V["teor"], V["n_pedras"], _mods(V), d["n_cun"], V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v405 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v405 SELADA (COMPLETA):**"


# v405: o topico do estado da Central
def topico_central(V):
    d = _d(V); DL_ = _qd().DL
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v404 `%s`; escada %s → %s; gate intocado. %d módulos novos no kernel (%s), com os nomes do operador: %s; o número da massa é o da v404; "
                               "o `um.py` confere o cálculo nos oito modelos; as erratas E10 a E13 (da gerência, em nome próprio) e as decisões D27 a D33 estão no registro `cunhagens_v405`; as %d inscrições por sha256 (todas do operador); a classe nova do teste do Grande Atrator vai ao lado (`ga_reclassificacao_v405`); "
                               "o quadro do topo (O Teste da Única Palavra, v397) segue intocado. A pendência [LEGAL] (D2) é do operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], d["depois"], V["n_pedras"], _mods(V), DL_.FRASE_DA_MOLDURA_PT, d["n_cun"])


# v405: o topico do estatuto da prova
def topico_estatuto(V):
    d = _d(V); g = d["g"]; DL_ = _qd().DL
    return ("<!-- v405_selada -->\n**%s — v405 `%s`:** o registro `estatuto_da_prova_v391` passou a ler a escada nova (%s → %s; veredito trocado, troca dita; as pedras e os registros da v404 ficam como registro). "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora e é o β_TGL na natureza a 5σ. **Uma mudança de estatuto [REAL]:** os campos da transição à massa fecharam e as leituras do operador passaram do campo para a definição: %s; `E₀ = u` = 1 eV passou de declarado a POSTO. A leitura física não virou teorema. "
            "As bandeiras do gate são as da v404 (%s calculadas e %s literais; o veredito do gate igual ao da v404); a independência das quatro experimentais segue [OPEN] (derivam de UM só booleano; [DECLARADO]). "
            "Os registros com função conferem os termos do kernel e o cálculo nos modelos ([REAL]); as falas do operador de 30/10 a 01/11 são [INPUT/ONTO]. "
            "O quadro do topo segue intocado: %s. Nada disso é prova sobre a natureza.") % (V["data"], V["s16"], V["escada_antes"], d["depois"], DL_.FRASE_DA_MOLDURA_PT, g["n_calc"], g["n_lit"], _z444())


# v405: o gancho da missao no MEMORY.md
def marca_missao(V):
    return "**v405 SELADA %s `%s` %s COMPLETA (a massa derivada e a identidade definida: oito pedras com os nomes do operador; dadas as entradas, a FORMA é teorema; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


# v405: a linha do handoff no MEMORY.md
def linha_handoff(V):
    return "- [HANDOFF v405 — a massa derivada e a identidade definida; custódia](handoff-v405-custodia.md) — **%s, para a sessão do site (traz o parágrafo novo, o do quadro e a nota ao lado do da v404; os anteriores seguem como estão)** · `%s`" % (V["data"][:5], V["s16"])


def linha_topico_novo(V):
    return "- [v405 SELADA: a massa derivada e a identidade definida (%s)](%s) — **%s** · `%s`" % (V["data"][:5], TOPICO_NOVO, V["teor"], V["s16"])


# v405: o topico novo da memoria (um arquivo por versao)
def topico_novo(V):
    d = _d(V)
    return (("---\nname: %s\ndescription: \"v405 SELADA (%s) `%s`: %d módulos novos no kernel com os nomes do operador; os campos das estruturas fecharam, as leituras dele passaram à definição; dadas as entradas, a FORMA é teorema; o número da massa é o da v404; %d inscrições por sha256; escada %s → %s; gate intocado\"\n"
             "metadata:\n  type: project\n---\n\n# v405 SELADA (%s)\n\n"
             "**O que é:** `um.py` **v405** `%s` (%s B) sobre a v404 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); o `um.py` cresce %s B (%s%%).\n\n"
             "**O que entrou:** %s.\n\n"
             "**As inscrições de 30/10 a 01/11** (embutidas por sha256; data, sha16, autor e tema — o nome do arquivo, não citação; o texto íntegro está em `insumos\\cunhagens`):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"
             "**Pendências:** o valor absoluto do setor e as escolhas da partitura do Grande Atrator (operador), a pendência [LEGAL] (D2). Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405`.\n\n"
             "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v405-custodia]]\n") % (
        TOPICO_NOVO[:-3], V["data"], V["s16"], V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
        format(d["delta"], ","), d["pct"], _num(V), _cunhagens(V), _moldura(V), _blocos_pedras(V), _massa(V), _erratas_e(V), _decisoes(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V) + "\n\n" + _erratas(V)))


# v405: o aviso a coordenadora (so' sob reivindicacao nomeada)
def aviso(V, reivindicacao):
    d = _d(V); DL_ = _qd().DL
    return (("### %s — v405 SELADA `%s` [claude-c1]\n<!-- aviso_v405_selada -->\n\n[REAL] A v405 SELOU (%s; COMPLETA; gate intocado): a massa derivada e a identidade definida entram no selo corrente com as oito pedras com os nomes do operador: %s; com as %d inscrições por sha256 (todas do operador), as erratas E10 a E13 e as decisões D27 a D33. Escrito sob a reivindicação %s. %d módulos novos no kernel; escada %s → %s. Não altera pinos, dado, MCP nem gate.") % (V["data"], V["s16"], V["teor"], DL_.FRASE_DA_MOLDURA_PT, d["n_cun"], reivindicacao, V["n_pedras"], V["escada_antes"], d["depois"]))


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V405_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# ---------------------------------------------------------------- o PARAGRAFO PRONTO do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO; ordem do operador de 23/10: o 4,44 no inicio do artigo, no readme e tudo mais) e (2) o paragrafo NOVO da falsidade
def verificar_paragrafo_readme(par, res, tv):
    """Verifica o paragrafo do QUADRO (texto) contra o RESULTADO pinado (`res`, o JSON lido) e o registro `tv` selado no core: devolve a lista de falhas (vazia = passou). As verificacoes (as mesmas da v397, da v399 e da v404):
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
    from guarda_p18_v405 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    for st in ("[REAL", "[INPUT]", "[KNOWN]", "COMPOSIÇÃO da gerência"):   # os estatutos que o quadro escreve: REAL (os numeros), INPUT (a leitura binaria e a frase), COMPOSICAO da gerencia (as duas faces) e KNOWN (Jeffreys)
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    return fa


def paragrafo_readme():
    """(texto, relatorio): o paragrafo do QUADRO pronto para colar no README do espelho e no site (o MESMO da v397, da v399 e da v404), gerado por quadro_v397.paragrafo_pronto_readme sobre o core SELADO do Nos, verificado contra o resultado pinado
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
    """Falhas de ATRIBUICAO e de DIRECAO num texto renderizado (v405: nao ha inscricao da gerencia; todas sao falas do operador): (a) nenhuma frase poe a IALD como quem testifica do operador (fora da fala em que ele recusa a ordem inversa);
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


# v405: o handoff para a sessao do site (memory\handoff-v405-custodia.md + Nos\HANDOFF_v405_CUSTODIA.md); `k` traz os campos dos recibos do B(n) e os paragrafos do README (fechar_v405.py os le dos recibos e do core): nenhum numero digitado
def handoff(V, k):
    d = _d(V); sc = V["sidecar"]
    k = dict(k)
    for chave in ("ap_nome", "ap_sha", "ap_ver", "ap_evento", "ap_bat", "par_sha", "rel_sha", "rel_man", "readme_paragrafo", "readme_paragrafo_v405"):
        assert chave in k, ("o handoff precisa do campo dos recibos do B(n) e dos paragrafos do README: " + chave)
    par = k["readme_paragrafo"].rstrip("\n"); par_f = k["readme_paragrafo_v405"].rstrip("\n"); err = errata_v404_bloco().rstrip("\n")
    assert par.startswith("### O Teste da Única Palavra (v397"), "o paragrafo do README (quadro) nao e' o do quadro"
    assert par_f.startswith("### A massa derivada e a identidade definida (v405"), "o paragrafo da v405 nao e' o novo"
    k.update({"data": V["data"], "s16": V["s16"], "umb": format(V["umb"], ","), "base16": V["base16"], "teor": V["teor"], "rc": V["rc"], "conf16": V["conf16"], "conf_dm": V["conf_dm"], "conf_np": V["conf_np"],
              "pilar": "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), "selo_ts": V["selo_ts"], "num": _num(V), "kernel_prova": _kernel_prova(V), "limites": _limites(V, curto=True), "legal": _legal(V),
              "artigos": ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), "n_cun": d["n_cun"], "n_pedras": V["n_pedras"], "topico": TOPICO_NOVO[:-3], "regra": _regra_do_4_44(V), "erratas_e": _erratas_e(V), "decisoes": _decisoes(V), "massa": _massa(V), "moldura": _moldura(V), "ga": _ga(V),
              "sc_nome": "um_absoluto_selo_acom.json", "sc_sha": sc["sha256"], "sc_ver": sc["veredito"], "sc_bytes": format(sc["bytes"], ","), "sc_objs": "; ".join("`%s` sha256 `%s`" % (n, o["sha256"]) for n, o in sc["objetos"].items()),
              "par_bloco": MARC_PAR_INI + "\n" + par + "\n" + MARC_PAR_FIM, "par_v405_bloco": MARC_V405_INI + "\n" + par_f + "\n" + MARC_V405_FIM, "err_bloco": MARC_ERR_INI + "\n" + err + "\n" + MARC_ERR_FIM})
    doc = ("---\nname: handoff-v405-custodia\ndescription: \"HANDOFF v405 (%(data)s) para a sessão do site: a massa derivada e a identidade definida: oito pedras com os nomes do operador; os campos fecharam, as leituras passaram à definição; dadas as entradas, a FORMA é teorema; o número da massa é o da v404; `%(s16)s`; B(n) da Bancada feito; TRAZ os parágrafos prontos do README/site, a nota ao lado do da v404 e lista o sidecar\"\n"
           "metadata:\n  type: project\n---\n\n# HANDOFF v405 — CUSTÓDIA (%(data)s)\n\n"
           "**O que é:** `um.py` **v405** `%(s16)s` (%(umb)s B) sobre a v404 `%(base16)s`; %(teor)s; COMPLETA; rc %(rc)s; selftest PASSED; gate intocado; conferidor `%(conf16)s` (deve mudar %(conf_dm)s; não pode mudar %(conf_np)s); pilar %(pilar)s pela chave. "
           "Selo `%(selo_ts)s`.\n\n"
           "**PARÁGRAFOS PRONTOS para o README do espelho e para o site (colar como estão, cada um entre os seus marcadores; o primeiro é o quadro do Teste da Única Palavra, o MESMO da v397, intocado; o segundo é novo).** O do quadro é gerado pelas MESMAS funções do quadro do artigo "
           "(a função paragrafo_pronto_readme do módulo quadro_v397), sobre o core SELADO do Nós, com os mesmos números e estatutos, e verificado contra o resultado pinado ANTES de este handoff nascer (o fechar recusa se o z_disc aparecer sem o p calibrado e sem a linha dos 5σ no mesmo item, "
           "se a frase do operador não for a verbatim ou se algum número diferir do resultado). O novo é gerado dos registros selados da v405 e verificado contra o core e contra os números do ensaio a seco "
           "(sem o z_disc do quadro; as citações são trechos verbatim das falas do operador; sem alegação de segurança criptográfica; com a guarda das frases):\n\n%(par_bloco)s\n\n%(par_v405_bloco)s\n\n"
           "**NOTA ao lado do parágrafo da v404 (Jo 8,32 e a projeção transversal da Meia-Nat) no README e no site (colar logo abaixo dele, entre os marcadores; o parágrafo da v404 fica como registro):**\n\n%(err_bloco)s\n\n"
           "**Os parágrafos do testemunho de dois (v399), da falsidade (v401), da ponte, da queda e da esperança (v402), de Caminho, Verdade e Vida (v403) e de Jo 8,32 (v404) SEGUEM COMO ESTÃO.** São os que estão no README do espelho e no site, e esta versão NÃO os regenera nem os substitui (o `um.py` mudou de bytes, mas os parágrafos são dos selos daquelas rodadas). Os registros que os geravam seguem selados e iguais ao ensaio a seco neste rito (a leitura os confere); só a nota do bloco acima acrescenta o que mudou no estatuto de `E₀`.\n\n"
           "%(moldura)s\n\n%(ga)s\n\n%(regra)s\n\n%(erratas_e)s\n\n%(decisoes)s\n\n%(massa)s\n\n"
           "**O que entrou e o que mediu:** %(num)s.\n\n"
           "**O SIDECAR (arquivo da custódia desde a v399, D5; REESCRITO por este rito):** `%(sc_nome)s` (sha256 `%(sc_sha)s`, %(sc_bytes)s B; veredito `%(sc_ver)s`); objetos selados: %(sc_objs)s. O sidecar fica AO LADO do selo (o selo não pode conter o selo ACOM de si mesmo) e o fechar o copia para `work\\cadeia_de_selo\\v405_selo` e o lista no manifesto de incorporação; "
           "a custódia o leva ao cofre, à PORTA (PORTA.json, URL raw) e ao espelho, junto do selo, porque a segunda testemunha só se confere com ele. A custódia da v399, da v403, da v404 e da v405 é CONJUNTA. A recusa do selo ACOM só registra (D4); o SHA-256 segue soberano.\n\n"
           "%(kernel_prova)s\n\n%(limites)s\n\n%(legal)s\n\n"
           "**O elo B(n) da Bancada Um (feito antes deste handoff; passo simples, sem salto):** recibo da aplicação `%(ap_nome)s` (sha256 `%(ap_sha)s`; veredito `%(ap_ver)s`; evento %(ap_evento)s; bateria `%(ap_bat)s`); recibo da parada do serviço sha256 `%(par_sha)s`; "
           "recibo do religamento sha256 `%(rel_sha)s` (versão servida v405, manifesto `%(rel_man)s`).\n\n"
           "**Para a sessão do site (custódia):** o `um.py` v405, `rodada_v405_stdout.txt`, o selo, o sidecar, o core, o .md canônico (com o quadro no topo, intocado) e o manifesto, os artigos PT/EN (%(artigos)s; o quadro «O Teste da Única Palavra» abre os dois), as %(n_cun)s inscrições por sha256 "
           "(todas falas do operador; lista na linhagem e no tópico `%(topico)s`; arquivos em `work\\cadeia_de_selo\\v405\\insumos\\cunhagens`), os %(n_pedras)s módulos novos (`work\\cadeia_de_selo\\v405\\pedra`) e os dois diffs (`DIFF_v404_v405.diff`, `DIFF_KERNEL_v405.txt`) — com PORTA gerada por script, "
           "URL raw (o um.py tem mais de 5 MB), backup da versão v404 no espelho fora do repositório, blob conferido depois do push. Colocar os PARÁGRAFOS acima no README do espelho e no site (ato da sessão do site, com o selo corrente ao lado; o do quadro e os anteriores seguem onde estão, o da v404 recebe a NOTA ao lado e o novo entra ao lado); "
           "publicar os módulos novos no espelho (TGLExt) e regenerar as PORTAS de `tgl_kernel`, `TGLExt` e `TGL`; a pasta `insumos` vai ao espelho com PORTA: sem ela, uma reprodução pública diz NOT_SEALED (fail-closed); os recibos da bateria do B(n) vão ao espelho com PORTA; o runner da Fronteira e a camada v405 dos 16 dispositivos; a revisão independente antes do portão do operador. "
           "A publicação do bloco embutido do método do operador no espelho público segue sujeita à decisão [LEGAL] D2 (operador com a agente de PI).\n\n"
           "**Pendências SÓ do operador:** o valor absoluto do setor; as escolhas da partitura do Grande Atrator; a decisão [LEGAL] D2; a ratificação da leitura de `tempoDoRetido` como o τ★ do sistema; a ratificação das decisões D27 a D33 da gerência que ele ainda não leu. [OPEN]: a discriminação a 5σ (β_TGL na natureza), o magnetismo na cadeia da tensão, qual é o disco, quais são as cinco notas, `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura e rank c = 4, `IsotropicPost` no atlas curvo, a dimensão 3, a instância do índice 1/β, a atestação física externa, "
           "a face de Fock do psion (o certificado de Fock da luz sem habitante exibido), o contrato conjunto da rede e a independência das quatro bandeiras experimentais do gate (um só booleano; os mocks de survey).\n\n"
           "Pacote e cadeia: `work\\cadeia_de_selo\\v405` (+ `pos_rito`); arquivo `work\\cadeia_de_selo\\v405_selo` e `v405_kernel`. NOT_FALSIFIED não é a palavra da creditação; o gate não se move.\n\n"
           "[[%(topico)s]] [[missao-ultima-flag-um-py]] [[handoff-v404-custodia]]\n") % k
    assert k["par_bloco"] in doc and k["par_v405_bloco"] in doc and k["err_bloco"] in doc, "os paragrafos do README e a nota nao entraram no handoff"
    assert not atribuicao_da_gerencia(doc), ("o handoff atribui mal ou inverte a direcao do testemunho", atribuicao_da_gerencia(doc)[:2])
    return doc


# v405: a linha da arvore da prova
def arvore_linha(V):
    d = _d(V); DL_ = _qd().DL
    return ("- **A MASSA DERIVADA E A IDENTIDADE DEFINIDA (v405)** `%s`: %d módulos novos no kernel (%s), %d bandeiras novas True, escada %s → %s; os campos das estruturas fecharam e as leituras do operador passaram à definição: %s [REAL a forma; POSTO `u`; MEDIDA `α`; INPUT/ONTO as leituras]; "
            "a Identidade prova um fato sobre projeções no estado traço, e que isso seja a identidade é leitura tipada como modelo; os oito registros conferem o cálculo; as %d inscrições por sha256 (todas do operador); validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["n_pedras"], _mods(V), d["n_f"], V["escada_antes"], d["depois"], DL_.FRASE_DA_MOLDURA_PT, d["n_cun"]))


# v405: o titulo do verbete do indice
def titulo_verbete(V):
    return "A massa derivada e a identidade definida (v405): oito pedras com os nomes do operador, os campos fechados e as leituras como definição:"


# v405: o corpo do verbete do indice
def verbete(V):
    return "[REAL — rodada v405 `%s`] %s." % (V["s16"], _num(V))


# v405: a entrada do remissivo
def remissivo(V):
    return "- **A massa derivada, a identidade definida, os campos fechados e as leituras, e as inscrições de 30/10 a 01/11 (v405)** — os oito registros de pedra, `cunhagens_v405`, `campos_fechados_e_leituras_v405`, `ga_reclassificacao_v405`, `gap_v405`, `kh_n1_cobertura_v405`, `%s`" % TOPICO_NOVO


MARC_V405_INI = "<!-- INICIO_PARAGRAFO_MASSA_DERIVADA_E_IDENTIDADE_v405 -->"; MARC_V405_FIM = "<!-- FIM_PARAGRAFO_MASSA_DERIVADA_E_IDENTIDADE_v405 -->"


MARC_ERR_INI = "<!-- INICIO_ERRATA_V404_V405 -->"; MARC_ERR_FIM = "<!-- FIM_ERRATA_V404_V405 -->"


_CHAVES = ("ponte", "tensao", "identidade", "observador", "diminuto", "tonica", "disco", "psion")


def _lst(xs):
    """Lista numerica lida do registro, em PT: inteiros sem casas, listas aninhadas entre parenteses."""
    return ", ".join(("(" + _lst(x) + ")") if isinstance(x, (list, tuple)) else _pn(x, 6) for x in xs)


def _sem_chaves(t):
    """Os textos vindos do core podem trazer chaves (e^{-s}); os textos renderizados nao as tem (a conferencia de formatacao reprova): chaves viram parenteses."""
    return t.replace("{", "(").replace("}", ")")


def _erratas_e(V):
    """As erratas E10 a E13 (em nome proprio da gerencia c1), LIDAS do registro cunhagens_v405 do core: nenhuma e' digitada aqui."""
    _d(V); er = _g(_core(), "cunhagens_v405", "erratas") or []
    itens = []
    for e in er:
        itens.append(_sem_chaves("- %s **Dizia:** %s **Lacuna de fidelidade:** %s **Estatuto:** %s" % (e["agora"], e["dizia"], e["lacuna_de_fidelidade"], e.get("estatuto", ""))))
    return ("**Erratas ao lado (em nome próprio da gerência c1, 01/11/2026; o texto antigo de `neutrino_mass.angle_status`, a errata E7, os adendos do handoff, o recibo da nomeação e as pedras seladas ficam como registro; nenhum módulo já instalado foi editado):** a v405 entra COM quatro erratas, lidas do registro `cunhagens_v405`:\n" + "\n".join(itens))


def _decisoes(V):
    """As decisoes D27 a D33 da gerencia c1, LIDAS do registro cunhagens_v405."""
    _d(V); ds = _g(_core(), "cunhagens_v405", "extras", "decisoes_da_gerencia") or {}
    ks = ("D27", "D28", "D29", "D30", "D31", "D32", "D33")
    assert all(k in ds for k in ks), "as decisoes D27 a D33 nao estao no registro cunhagens_v405"
    return "**Decisões** [da gerência c1, em nome próprio, ratificáveis pelo operador; as que trazem fala dele dizem o sha16]:\n" + _sem_chaves("\n".join("- %s: %s" % (k, ds[k]) for k in ks))


# ---------------------------------------------------------------- o PARAGRAFO NOVO da v405 e a NOTA ao lado do paragrafo da v404
def _linha_maquina_v405(core, d):
    """A linha de maquina do paragrafo novo (os numeros LIDOS dos registros do core), em PT."""
    pv = core["ponte_da_massa_v405"]["values"]; dv = core["lei_do_diminuto_v405"]["values"]; zv = core["ponto_zero_do_psion_v405"]["values"]; gv = core["ga_reclassificacao_v405"]["values"]
    return ("pedras_sha16=%s; bandeiras=%s; beta=%s; massa_meV=%s; proporcional_meV=%s; meio_tom=%s; tonica_eV=%s; E0_eV=%s; hbar_omega_meV=%s; ga_piso=%s; checagens=%s; falas_sha16=%s/%s"
            % ("/".join(d["sha"][k] for k in _CHAVES), d["n_f"], _p(pv["beta"], 12), _p(pv["m_derivada_meV"], 9), _p(pv["m_proporcional_meV"], 9), _p(dv["meio_tom"], 9), _p(dv["tonica_eV"], 9), _p(dv["E0_eV"], 9), _p(zv["hbar_omega_meV"], 9), _p(gv["piso_de_definicao"], 6),
               "/".join(str(core[_REG_DE[k]]["mechanics"]["n_checks"]) for k in _CHAVES), d["s_nomes"], d["s_tgl"]))


def _dados_paragrafo(core):
    """O que o paragrafo precisa do core SELADO e de ESPERADOS (sem V): as sha16 das pedras, as bandeiras e as falas."""
    esp = _esp(); DL_ = _qd().DL; ks = _CHAVES
    for n in list(_REG_DE.values()) + ["cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405"]:
        assert (core.get(n) or {}).get("all_verified") is True, "o registro %s nao selou: nenhum paragrafo diz os numeros assim" % n
    sha = {k: esp["pedras"][DL_.STONE_BY_KEY[k]["rel"]]["sha16"] for k in ks}
    return {"sha": sha, "n_f": esp["n_bandeiras_novas"], "n_g": dict(esp["n_bandeiras_por_grupo"]), "n_ck_cun": len(core["cunhagens_v405"].get("checks") or []), "s_nomes": _sha_por("nomes_das_sete_pedras"), "s_tgl": _sha_por("isso_e_a_TGL"), "s_1ev": _sha_por("formula_da_massa_um_absoluto_1eV"), "s_lei": _sha_por("angulo_de_miguel_singularidade"), "s_ens": _sha_por("A_IDENTIDADE_ensaio_final"), "s_ga": _sha_por("grande_atrator_reclassificar")}


def _paragrafo_v405_de(core):
    """O texto do paragrafo da v405, funcao PURA dos registros selados do core (os numeros sao lidos dos registros, nunca digitados)."""
    d = _dados_paragrafo(core); DL_ = _qd().DL
    pv = core["ponte_da_massa_v405"]["values"]; dv = core["lei_do_diminuto_v405"]["values"]; zv = core["ponto_zero_do_psion_v405"]["values"]; ev = core["disco_de_euler_v405"]["values"]; gv = core["ga_reclassificacao_v405"]["values"]
    assert pv.get("beta") and dv.get("E0_eV") and zv.get("hbar_omega_meV"), "os registros da v405 nao trazem os valores: nenhum paragrafo diz os numeros assim"
    q_1ev = _cita("o meu um absoluto é o um de 1 eV"); q_ok = _cita("é isso , perfeito, concordo com tudo"); q_tgl = _cita("estamos terminando onde tinha que terminar mesmo, derivando a massa e definindo a identidade, isso é a TGL"); q_sing = _cita("não tem teorema para o ângulo de Miguel é a definição de singularidade, a meu ver")
    x = core["campos_fechados_e_leituras_v405"]["extras"]; ent = x["o_que_entra"]
    assert [DL_.nome_lean(l_) for l_ in ent["leituras_da_cadeia_da_massa"]][:4] == ["massaDerivada", "transicaoDerivada", "tonica", "pagamentoComoCurvatura"], "as leituras centrais do registro nao sao as que este paragrafo nomeia"
    lei = ("(1) a massa é a energia retida vezes a derivada da projeção transversal (`massaDerivada`); (2) o estado inscrito é lido em θ = π/4: o ângulo é escrito em `transicaoDerivada`, e o kernel confere `sen²(π/4) = ½`, coincidência de valor com o peso da face absoluta, não ponte; "
           "(3) a tônica `(β/α) · u` (`tonica`): `β/α = √e` é a definição de `TGLCoupling.alpha`; (4) `R = β · u²` (`pagamentoComoCurvatura`): o pagamento lido como curvatura, a escolha dimensional de uma unidade só")
    qg = core.get("qg_closure") or {}; fam = [len(qg.get(f) or {}) for f in ("formal_flags", "physics_flags", "experiment_flags")]
    ls = ["### A massa derivada e a identidade definida (v405, 01/11/2026) — parágrafo pronto para o README do espelho e para o site",
          "",
          "> **A massa derivada e a identidade definida (v405, 01/11/2026)** [REAL: os termos do kernel, a forma dadas as entradas e a conferência do cálculo nos modelos · POSTO: a unidade `u` = 1 eV · MEDIDA: `α`, por dentro · INPUT/ONTO: as leituras do operador, que entram como definição · INPUT: a dispersão do psíon, Tratado §3 · KNOWN: o ponto zero · DECLARADO: a reclassificação do Grande Atrator é decisão da gerência por ordem do operador · OPEN: o valor absoluto do setor, o magnetismo, qual é o disco, quais são as cinco notas, `H_BW`, `H_cal`, H3, a assinatura, rank c = 4, `IsotropicPost` e a dimensão 3]",
          ">",
          "> - **As oito pedras** [REAL · INPUT]: oito módulos novos no kernel, com os nomes do operador (sha16 `%s`): Ponte da Massa, Massa = tensão pura, Identidade, Observador = terminal, Lei do diminuto, Tônica do Hamiltoniano, Disco de Euler e Ponto Zero do Psíon, com %s bandeiras, todas no trio." % (d["s_nomes"], d["n_f"]),
          "> - **A moldura** [REAL · POSTO · MEDIDA · INPUT/ONTO]: os campos das estruturas fecharam; as leituras do operador passaram do campo para a definição; a leitura física não virou teorema. Entram o Um posto, %s (sha16 `%s`), a `α` medida por dentro (à pergunta de derivá-la a resposta foi não, parede medida; a leitura dele: %s, sha16 `%s`) e as leituras da cadeia da massa, que não são teoremas, numa lista que não é fechada; as centrais: %s; entram ainda, entre outras, `meioTom`, `modular`, a dispersão `omegaSq` [INPUT, Tratado §3] e `m₁ = 0`, esta como entrada da identificação com `Δm²₂₁`. Em uma frase: %s." % (q_1ev, d["s_1ev"], q_sing, d["s_lei"], lei, DL_.FRASE_DA_MOLDURA_PT),
          "> - **A forma** [REAL]: dadas essas entradas, `m₂ = β · sen 45° · u` é teorema; com β = α√e = %s em runtime, `m` = %s meV, o número da v404; a leitura proporcional daria %s meV. O meio-tom `e^(−½)` = %s desfaz o `√e`; a tônica `√e · u` = %s eV é definição, e `E₀ = u` = %s eV é identidade algébrica, que não fixa `u`: o no-go não cai, localiza-se no Um posto. O diminuto é modulação, não transposição: só a tônica desce o meio-tom, as demais notas ficam sustentadas, e `transpor` é só a liberdade do no-go. A escala é o que fica parado; o valor absoluto segue livre; o valor relativo à tônica está pinado; sobra um único grau de liberdade global, a transposição do acorde inteiro; quais são as cinco notas é [OPEN]. Sob a leitura `R = β · u²`, `½ħω` é a mesma forma, com `ħω` = %s meV: a coincidência é a aritmética `½ · √2 = sen 45°`."
          % (_p(pv["beta"], 12), _p(pv["m_derivada_meV"], 9), _p(pv["m_proporcional_meV"], 9), _p(dv["meio_tom"], 9), _p(dv["tonica_eV"], 9), _p(dv["E0_eV"], 9), _p(zv["hbar_omega_meV"], 9)),
          "> - **O gap, ao lado** [REAL · ONTO · OPEN]: o lock mínimo tem gap espectral 1; na unidade posta, `u`, o `E₀` da Lei do Diminuto, e a tônica fica meio-tom acima dele. No ângulo de Miguel o valor esperado do lock é β, e na unidade posta `Δ = β · u`, a energia retida: `Δ` não é gap, é 1/β vezes menor. A fala do operador diz gap com unidade; que o ângulo de Miguel seja esse sistema é leitura dele [ONTO]; ler `tempoDoRetido` como o τ★ do sistema é leitura [ONTO], a ratificar por ele; `κ` segue testemunha; `Δ` carrega `u`, e nada fixa `u`.",
          "> - **O disco e o observador** [REAL · ONTO · OPEN]: no Disco de Euler a energia linear e `Ω² = K/E` são definições; dadas elas, a `E` definida resolve o fluxo, zera em tempo finito e `Ω²` não tem cota antes disso; a taxa de dephasing lida como perda de energia e a inscrição do zero no infinito são leituras do operador; `K`, `τ` e `E₀` são dados do disco; o `K` que a nota posta exigiria é registrado, %s J/s², não escolhido. O posto do observador é o terminal, num modelo finito cujos níveis são rótulos; a fusão é o colapso, e o colapso é um Um posto do kernel." % _pe(ev["K_si_para_u_posto_J_s2"], 3),
          "> - **A identidade** [REAL · ONTO · DECLARAÇÃO DO OPERADOR]: a pedra prova um fato sobre projeções no estado traço; que isso seja a identidade é leitura, tipada como modelo. O ensaio «A identidade» é do operador e entra no artigo verbatim (r2, ratificada em %s; original sha16 `%s`); não é teorema." % (q_ok, d["s_ens"]),
          "> - **O Grande Atrator, ao lado** [DECLARADO · REAL]: a classe do teste muda de `A3_APOSENTADO` para `A13_FORMA_CONDICIONAL_SEM_INCERTEZA` (sha16 `%s`): a forma fica condicional; a janela mantém o veto; não é evidência; não discrimina da RG. Só a definição do raio move a previsão em %s. A linha da tabela, a constante e o gate ficam idênticos." % (d["s_ga"], _p(gv["piso_de_definicao"] * 100.0, 1) + "%"),
          "> - **O gate** [REAL · DECLARADO]: é o da v404 — das %s bandeiras (%s formais, %s físicas e %s experimentais) todas calculadas, a letra do veredito inalterada; as quatro experimentais derivam de UM só booleano. O gate não se move; nenhuma bandeira dele depende das pedras da v405." % (qg.get("n_flags") or sum(fam), fam[0], fam[1], fam[2]),
          "> - **Erratas ao lado (gerência c1, em nome próprio, 01/11/2026):** E10, o texto antigo de `neutrino_mass.angle_status` e a E7 ficam; o `sen 45°` tem duas leituras que coincidem na forma, e mais uma leitura do mesmo `sen 45°`, por aritmética; E11, os nomes provisórios e o `E₀` declarado eram verdadeiros na data; E12, com a energia total, o invariante do disco real é `K = 6Mg²` (`4Mg²` era a conta só com a energia potencial); E13, a gerência escreveu que a cadeia da massa ficava sem hipótese, e isso afirmava demais: foi erro da gerência, e quatro teoremas foram rebatizados antes do selo; a revisita da Lei do Diminuto, ordenada pelo operador, tipou o acorde e corrigiu a frase sobre o no-go; a resposta dele corrigiu a primeira correção: o diminuto é modulação, não transposição.",
          "> - **Limites:** [OPEN] o valor absoluto do setor, o magnetismo na cadeia da tensão, qual é o disco, quais são as cinco notas, `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura, rank c = 4, `IsotropicPost` no atlas curvo e a dimensão 3; as pedras NÃO derivam a unidade nem `α`; o cálculo CONFERE os teoremas nos modelos e quem prova é o kernel, e esses números são deste rito, não estão no kernel; a gravidade quântica segue sem creditação na natureza; "
          "validade no kernel não é creditação; `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; isto não é teste e não acrescenta dado. O quadro do Teste da Única Palavra segue no README com a sua linha dos 5σ; este parágrafo não traz o número do quadro.",
          "> - **O fecho** [INPUT]: %s." % q_tgl,
          "> - **Origem.** Os números são lidos do core selado desta rodada; nenhum é digitado. Linha de máquina: `%s`." % _linha_maquina_v405(core, d)]
    return "\n".join(ls) + "\n"


def verificar_paragrafo_v405(par, core, esp):
    """Verifica o paragrafo da v405 contra o core selado E contra ESPERADOS (o ensaio a seco): devolve a lista de falhas (vazia = passou). As verificacoes:
    (1) os numeros do core (os oito registros com funcao) == os de ESPERADOS[registros_funcao_v405][k][values] e cada um esta no paragrafo, formatado; (2) o paragrafo == o gerado do core; (3) NAO traz o 4,44 nem o z_disc (a regra do 4,44 e' do quadro); (4) os estatutos;
    (5) as frases de limite; (6) toda citacao entre « » e' verbatim numa fala DO OPERADOR ou rotulo; (7) nenhuma alegacao de seguranca criptografica, «consciencia» so' como palavra retirada, a direcao sem inversao; (8) a guarda P18 e a guarda das frases."""
    fa = []
    ef = esp.get("registros_funcao_v405") or {}

    def _eq(a, b):
        return (isinstance(a, float) and isinstance(b, float) and abs(a - b) <= 1e-12 * max(1.0, abs(b))) if isinstance(b, float) else a == b
    for k in _CHAVES:
        rn = _REG_DE[k]; fv = (core.get(rn) or {}).get("values") or {}; ev = (ef.get(k) or {}).get("values") or {}
        if not (fv and ev and all(_eq(fv.get(kk), vv) if not isinstance(vv, (list, dict)) else fv.get(kk) == vv for kk, vv in ev.items())):
            fa.append("numero do registro %s no core != ESPERADOS" % rn)
    pv = (core.get("ponte_da_massa_v405") or {}).get("values") or {}; dv = (core.get("lei_do_diminuto_v405") or {}).get("values") or {}; zv = (core.get("ponto_zero_do_psion_v405") or {}).get("values") or {}; ev_ = (core.get("disco_de_euler_v405") or {}).get("values") or {}; gv = (core.get("ga_reclassificacao_v405") or {}).get("values") or {}
    try:
        nums = {"beta": _p(pv["beta"], 12), "massa": _p(pv["m_derivada_meV"], 9), "proporcional": _p(pv["m_proporcional_meV"], 9), "meio-tom": _p(dv["meio_tom"], 9), "tonica": _p(dv["tonica_eV"], 9), "E0": _p(dv["E0_eV"], 9), "hbar omega": _p(zv["hbar_omega_meV"], 9), "K do disco": _pe(ev_["K_si_para_u_posto_J_s2"], 3), "piso do GA": _p(gv["piso_de_definicao"] * 100.0, 1),
                "bandeiras": str(esp["n_bandeiras_novas"]), "sha16 dos nomes": _sha_por("nomes_das_sete_pedras"), "sha16 do Um de 1 eV": _sha_por("formula_da_massa_um_absoluto_1eV"), "sha16 da singularidade": _sha_por("angulo_de_miguel_singularidade"), "sha16 do ensaio": _sha_por("A_IDENTIDADE_ensaio_final"), "sha16 do GA": _sha_por("grande_atrator_reclassificar")}
    except KeyError as e:
        nums = {}; fa.append("valor ausente do registro: %s" % e)
    for k, v in nums.items():
        if v not in par:
            fa.append("numero (%s = %s) ausente do paragrafo" % (k, v))
    try:
        if par != _paragrafo_v405_de(core):
            fa.append("o paragrafo difere do gerado pelas funcoes sobre os registros selados do core")
    except AssertionError as e:
        fa.append("o paragrafo nao pode ser gerado do core: %s" % str(e)[:120])
    if re.search(r"4[,.]44|z_disc", par):
        fa.append("o paragrafo da v405 traz o 4,44 ou o z_disc (a regra do 4,44 e' do quadro; este paragrafo nao o cita)")
    for st in ("[REAL", "POSTO", "MEDIDA", "INPUT", "ONTO", "OPEN", "DECLARADO", "KNOWN"):
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    for frase in ("dadas essas entradas, a FORMA é teorema", "a leitura física não virou teorema", "o no-go não cai", "não fixa `u`", "tipada como modelo", "não é teorema", "não é evidência", "não discrimina da RG", "O gate não se move", "UM só booleano", "Erratas ao lado", "CONFERE os teoremas", "quem prova é o kernel", "validade no kernel não é creditação",
                  "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "gate não se move", "o número da v404"):
        if frase not in par:
            fa.append("frase de limite ausente do paragrafo: " + frase)
    corpus = [re.sub(r"\s+", " ", dd["text"]) for dd in _falas().values() if dd["autor"] == "operador"]
    for q in re.findall(r"«([^»]*)»", par):
        if len(q) >= 13 and not any(q in t for t in corpus):
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
    from guarda_p18_v405 import violacoes
    import guarda_frases_v405 as GF
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    v2 = GF.violacoes(par)
    if v2:
        fa.append("a guarda das frases achou %r" % (v2[:2],))
    return fa


def paragrafo_v405():
    """(texto, relatorio): o paragrafo NOVO da v405, pronto para colar no README do espelho e no site, gerado do core SELADO do Nos e verificado contra o core E contra ESPERADOS;
    levanta AssertionError (o fechar RECUSA) se algo nao conferir."""
    core = _core(); esp = _esp()
    par = _paragrafo_v405_de(core)
    fa = verificar_paragrafo_v405(par, core, esp)
    assert not fa, ("o paragrafo da v405 nao passou nas verificacoes", fa[:4])
    return par, {"sha16": hashlib.sha256(par.encode("utf-8")).hexdigest()[:16], "verificacoes": "numeros == ESPERADOS; igual ao gerado do core; sem o 4,44; estatutos; limites; citacoes verbatim (falas do operador); sem alegacao de seguranca criptografica; guarda P18; guarda das frases", "guarda_p18": "limpa"}


def errata_v404_bloco():
    """O bloco de NOTA ao lado do paragrafo da v404 (Jo 8,32 e a projecao transversal da Meia-Nat) no README do espelho e no site: E0 passou de declarado a posto, e os nomes provisorios foram dados. Texto da gerencia, conferido pela guarda P18 e pelo kernel; as citacoes saem dos bytes das falas."""
    _kernel_tem(("umPosto", "massa_derivada_eq_form"))
    q_1ev = _cita("o meu um absoluto é o um de 1 eV")
    t = ("> **Nota ao lado do parágrafo «Jo 8,32 e a projeção transversal da Meia-Nat» (v404) — gerência c1, em nome próprio, 01/11/2026:** o parágrafo da v404 diz que `E₀` segue declarado e que o nome `ProjecaoTransversalDaMeiaNat` é provisório, e isso era verdade na data. Em 31/10/2026 o operador pôs a unidade [INPUT]: " + q_1ev + " (sha16 " + _sha_por("formula_da_massa_um_absoluto_1eV") + "): `u` = 1 eV é POSTO, não declarado nem derivado. "
         "Os módulos selados da v404 (`ProjecaoTransversalDaMeiaNat` e `Jo8v32`) NÃO foram editados nem renomeados — ficam como REGISTRO — e os registros da v404 seguem selados. "
         "O que o parágrafo da v404 diz sobre as pedras, o cálculo e os limites não muda; ele fica como registro.\n")
    sys.path.insert(0, PK)
    from guarda_p18_v405 import violacoes
    assert not violacoes(t), "a guarda P18 achou palavra recusada na nota ao lado do paragrafo da v404"
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


def _massa(V):
    """A leitura da v405, LIDA do registro cunhagens_v405 (extras.leitura_v405) e conferida contra ESPERADOS."""
    d = _d(V); lm = _g(_core(), "cunhagens_v405", "extras", "leitura_v405") or {}
    assert lm and lm == _esp()["leitura_v405"] and "ONTO" in str(lm.get("estatuto")), "a leitura da v405 nao e' a de ESPERADOS"
    return _sem_chaves("**As leituras** %s: %s." % (lm["estatuto"], "; ".join(str(lm[k_]) for k_ in ("massa", "unidade", "alfa", "identidade", "observador", "curvatura", "disco", "tom"))))


# os temas das falas de 30/10 a 01/11 sao os proprios nomes dos arquivos (resumo dado no nome, nunca citacao); o sha16, a data e o autor vem dos bytes e do nome, nunca daqui. So' o nome que carrega uma frase que a guarda recusa e' reescrito.
_TEMA_ESPECIAL = {"nomes_das_sete_pedras_e_tudo_derivado": "os nomes das sete pedras e o pedido de que não restassem hipóteses nomeadas"}


_REG_DE = {"ponte": "ponte_da_massa_v405", "tensao": "massa_tensao_pura_v405", "identidade": "identidade_v405", "observador": "observador_terminal_v405", "diminuto": "lei_do_diminuto_v405", "tonica": "tonica_do_hamiltoniano_v405", "disco": "disco_de_euler_v405", "psion": "ponto_zero_do_psion_v405"}


_NOME_DE = {"ponte": "Ponte da Massa", "tensao": "Massa = tensão pura", "identidade": "Identidade", "observador": "Observador = terminal", "diminuto": "Lei do diminuto", "tonica": "Tônica do Hamiltoniano", "disco": "Disco de Euler", "psion": "Ponto Zero do Psíon"}


def _tema(nome):
    """O tema de uma fala: o nome do arquivo sem o autor, a data e o sufixo (o resumo que a gerencia deu ao gravar; nunca citacao)."""
    t = re.sub(r"_verbatim\.txt$", "", re.sub(r"^(?:OPERADOR|GERENCIA)_\d{2}(?:out|nov)_", "", nome))
    return _TEMA_ESPECIAL.get(t, t.replace("_", " "))


def _moldura(V):
    """A MOLDURA da v405, LIDA do registro campos_fechados_e_leituras_v405 do core: o que fechou (campos) e o que entra (os dois postos e as leituras da cadeia da massa, lista que nao e' fechada, cada uma com o nome Lean)."""
    d = _d(V); x = _g(_core(), "campos_fechados_e_leituras_v405", "extras") or {}; DL_ = _qd().DL
    ent = x["o_que_entra"]; cf = x["o_que_fechou_campos"]
    assert x.get("a_frase_da_moldura") == DL_.FRASE_DA_MOLDURA_PT and len(ent["leituras_da_cadeia_da_massa"]) == len(DL_.LEITURAS_DEFINICOES) and ent.get("lista_de_leituras_fechada") is False and len(ent["dois_postos"]) == 2, "a moldura do registro nao e' a do delta"
    fech = _sem_chaves("; ".join("%s: %s (`%s`)" % (k_, v_["fechou_com"], "`, `".join(t_.split(".")[-1] for t_ in v_["termos"])) for k_, v_ in cf.items()))
    pos = _sem_chaves("; ".join("[%s] %s (`%s`)" % (p_["estatuto"], p_["o_que"], p_["definicao_lean"].split(".")[-1]) for p_ in ent["dois_postos"]))
    lei = _sem_chaves("; ".join("(%d) %s (`%s`)" % (l_["n"], l_["leitura"], DL_.nome_lean(l_)) for l_ in ent["leituras_da_cadeia_da_massa"]))
    dados = _sem_chaves("; ".join(ent["dados_do_sistema_que_le"]))
    forma = _sem_chaves("; ".join("%s%s" % (f_["o_que"], (" (`%s`)" % f_["termo"].split(".")[-1]) if f_.get("termo") else "") for f_ in x["a_forma_real"]))
    return _sem_chaves(_f("**A moldura: o que fechou e o que entra [REAL + POSTO + MEDIDA + INPUT/ONTO; registro `campos_fechados_e_leituras_v405`, {nck} checagens]:** os CAMPOS das estruturas fecharam; as LEITURAS do operador passaram do campo para a DEFINIÇÃO; a leitura física não virou teorema. O que fechou: {fech}. O que entra: {pos}; e as leituras da cadeia da massa, que entram como definição ou identificação e não são teoremas, numa lista que não é fechada: {lei}. Entram ainda: {dados}. "
                          "[REAL] A forma, dadas essas entradas: {forma}. Em uma frase: {frase}.",
                          nck=V["campos"]["n_checks"], fech=fech, pos=pos, lei=lei, dados=dados, forma=forma, frase=DL_.FRASE_DA_MOLDURA_PT))


def _ponte(V):
    d = _d(V); v = V["ponte"]["values"]
    return _f("**A Ponte da Massa** [REAL · INPUT/ONTO] (`PonteDaMassa`, sha16 `{h}`; composição `{u}`, estrela `{e}`; {n} checagens): a projeção transversal `sen θ` tem derivada `cos θ` e, no ponto autoconjugado, a projeção é a sua derivada, e só ali em `[0, π/2]`; o retido é `β · E₀` e nada se perde; sob a definição `massaDerivada`, a massa é a forma do neutrino `β · sen 45° · E₀`; a leitura proporcional difere da derivada por √2. "
              "Neste rito, com β = α(CODATA 2018) × √e = {beta} em runtime: massa {m} meV, leitura proporcional {mp} meV, `m_nu` do programa {mc} meV: o número é o da v404. Que a massa do neutrino SEJA esta grandeza é leitura do operador: a pedra prova que a definição implica a forma, não que a natureza a adota; quem a testa é o rito do neutrino, bilateral, que não muda.",
              h=d["sha"]["ponte"], u=d["unc"]["ponte"].split(".")[-1], e=d["est_t"]["ponte"].split(".")[-1], n=d["nck"]["ponte"], beta=_p(v["beta"], 12), m=_p(v["m_derivada_meV"], 9), mp=_p(v["m_proporcional_meV"], 9), mc=_p(v["m_nu_meV_core"], 9))


def _tensao(V):
    d = _d(V); v = V["tensao"]["values"]
    return _f("**Massa = tensão pura** [REAL · ONTO] (`MassaTensaoPura`, sha16 `{h}`; {n} checagens): a forma genérica `b · (√2/2) · E₀` anula com `b = 0`, e então toda a energia atravessa (`foton_sem_massa`, álgebra da forma); ler `b = 0` como o fóton é leitura [ONTO]: `TGLCoupling` exclui `b = 0` e nenhum termo do kernel tem fóton; sob a leitura `massaDerivada`, a massa é o produto do acoplamento e se reparte como resíduo, incidente menos transmitido, lido na projeção transversal; o período fiel do empréstimo é teorema, `P = 2π/κ` (`one_turn_gives_faithful_period`), e a parcela não quita numa volta (para qualquer tempo finito, `the_charge_never_completes`); sob a leitura `massaDerivada`, o principal é a energia retida projetada no transversal (`massa_e_tensao_pura`). "
              "Neste rito: retida {r} eV, transmitida {t} eV. A leitura do empréstimo foi ratificada pelo operador em 30/10/2026 e não é termo de kernel. [OPEN] Da cadeia tensão, atrito, temperatura e magnetismo, os três primeiros têm termo no kernel; o magnetismo não tem.",
              h=d["sha"]["tensao"], n=d["nck"]["tensao"], r=_p(v["retida_eV"], 12), t=_p(v["transmitida_eV"], 12))


def _lei(V):
    d = _d(V); v = V["diminuto"]["values"]; t = V["tonica"]["values"]; ss = d["ss"]
    return _f("**A lei do diminuto e a tônica do Hamiltoniano** [REAL · INPUT/ONTO · OPEN] (`LeiDoDiminuto`, sha16 `{h1}`; `TonicaDoHamiltoniano`, sha16 `{h2}`; {n1} e {n2} checagens): o diminuto é MODULAÇÃO, não transposição ({q_mod}, `{s_mod}`): só a tônica desce o meio-tom pinado `e^(−½)` (`modular`; `meioTom`, definição: o tom é a nat), as demais notas ficam sustentadas (`modular_sustenta`), elas e as razões entre elas ficam (`modular_mantem_a_escala`: a escala é o que fica parado, e a razão à tônica muda), e nenhum fator leva o acorde ao acorde modulado (`modular_nao_e_transposicao`): o meio-tom quebra a simetria do acorde, porque separa a tônica das notas sustentadas, mas não quebra a liberdade global. [INPUT] O tom fica, na fala dele: o kernel não tem termo para o tom. `E₀` é o valor da tônica modulada (`lerE0_e_a_tonica_modulada`), e `E₀/tônica = e^(−½)` em todo acorde (`E0_relativo_pinado`, a definição dita como razão); {q_ter} é, no kernel, a aritmética `1 nat + ½ nat` (`um_tom_vira_terca_menor`: `e^(3/2)`); {q_esp} é leitura [ONTO], com a forma `the_charge_never_completes`. "
              "O meio-tom desfaz exatamente o `√e`, e `β = α · e^(½)`; a tônica `(β/α) · u = √e · u` é DEFINIÇÃO, não traz informação além do `u` posto; o diminuto pousa em `E₀ = u` por identidade algébrica, que não fixa `u`; dadas as entradas, a forma `m = U · α · e^(½) · √2/2` é teorema. `Acorde`, `transpor`, `razao` e o teorema da razão vêm do `AcordeE0.lean` do Kimi (sha16 `{s_k}`); `transpor` é só a liberdade do no-go. "
              "O no-go NÃO cai: nenhuma função da inscrição fixa `E₀` (`no_function_of_the_inscription_fixes_E0`), e ele se localiza no Um posto; a reescala preserva `m/E₀` (`the_ratio_survives_the_rescaling`). A distinção é do operador, {q_livre} (`{s_pent}`): o valor ABSOLUTO segue livre; o valor RELATIVO à tônica está pinado; sobra um único grau de liberdade global, a transposição do acorde inteiro. Quais são as cinco notas é [OPEN]: a pêntada do teorema mestre são cinco componentes, não cinco autovalores. "
              "`meioTom_e_o_pedagio_local` e `meioTom_e_a_face` são igualdades de VALOR; `CollapseCostLaw` é [INPUT] no kernel; a calibração `⟨K_∂⟩_total = 1 nat` de 24/06/2026 (relatório sha16 `{s_h}`) é normalização definicional, não é termo do kernel nem medida, e fixa intervalos em nat, não a unidade em eV: `U_E_NOT_DERIVED` fica como está. "
              "Neste rito: meio-tom {mt}, tônica {tn} eV, `E₀` = {e0} eV, massa pela fórmula {m} meV, razão m/E₀ = {rz}. A lei é do operador ({q_meio}, `{s_meio}`; {q_tom}, `{s_tom}`); `α` como a magnitude (cauda) da inscrição é leitura dele; a resposta à pergunta dele sobre derivar `α` foi não, parede medida, não falsificação.",
              h1=d["sha"]["diminuto"], h2=d["sha"]["tonica"], n1=d["nck"]["diminuto"], n2=d["nck"]["tonica"], mt=_p(v["meio_tom"], 9), tn=_p(v["tonica_eV"], 9), e0=_p(v["E0_eV"], 9), m=_p(v["massa_formula_meV"], 9), rz=_p(t["razao_m_sobre_E0"], 12), q_meio=_cita("ele desce meio tom pinado, essa é a lei"), s_meio=ss["meio"], q_tom=_cita("pra mim o TOm é a NAT"), s_tom=ss["tom"], q_livre=_cita("E0 não é absolutamente livre"), s_pent=ss["pent"], s_k=v["acorde_kimi_sha16"], s_h=v["half_nat_sha16"], q_mod=_cita("vc apenas modula a tônica"), s_mod=ss["mod"], q_ter=_cita("o sistema está operando em terças"), q_esp=_cita("no harmônico o diminuto é a espera"))


def _gap(V):
    d = _d(V); v = V["gap"]["values"]; ss = d["ss"]
    return _f("**O gap, ao lado** [REAL · ONTO · OPEN] (registro `gap_v405`, {n} checagens; fala do operador, `{s}`: {q}; que o ângulo de Miguel seja esse sistema é leitura dele [ONTO]): em qualquer espaço de Hilbert, o lock mínimo `1 − P` sobre um vetor `Ω` (`lockDe`) tem gap espectral 1 (`o_lock_tem_gap_um`); na unidade posta o gap vale `u` (`o_gap_com_unidade`), o `E₀` da Lei do Diminuto, e a tônica fica meio-tom acima dele. Num estado a um ângulo θ de `Ω` o lock tem valor esperado `sen²θ` (`lock_no_angulo`); no ângulo de Miguel, β (`lock_no_angulo_de_miguel`); na unidade posta esse valor esperado é `Δ = β · u`, a energia retida (`retidoNoAngulo`, `o_retido_e_o_valor_esperado_do_lock`). `Δ` não é gap: é 1/β vezes menor (o gap é {gd} vezes `Δ`). [REAL, condicional] O `HminMic` do kernel é instância desses lemas (`HminMic_e_o_lock`), condicional a um `FockCertificate`, que o kernel não habita. A tônica é `Δ/α` (`a_tonica_e_o_retido_sobre_alpha`); a massa é a projeção transversal de `Δ` (`a_massa_e_a_projecao_do_retido`); o psíon é `√2 · Δ` (`o_psion_e_raiz_de_dois_retidos`); o fecho é `the_gap_closes`. Neste rito: `Δ` = {dl} eV, `τ` = {tau} s, `Γ_B` = {gam} eV, `Q = √2/β` = {q_v}. "
              "[ONTO, a ratificar pelo operador] ler `tempoDoRetido` como o τ★ do sistema: é tempo próprio, não `t_P`, e não mexe no ramo canônico. `κ` segue testemunha: `κ = F(α, β, θ_M)` é proibido como objetivo de busca, e `κ` só aparece como hipótese em `o_relogio_do_retido`. `U_E_NOT_DERIVED` fica: `Δ` carrega `u`, e nada fixa `u`. Medida negativa: sob esta leitura, `E_fluxo = c⁵τ/(4πG)` vale {ef} eV, não é `E₀`, e a ponte `E_fluxo = E₀` do Kimi não vale aqui. O invariante `K` do disco não depende da inclinação, logo o ângulo não fixa `K` [OPEN]; quais são as cinco notas segue [OPEN], e só se sabe, por fala dele, que o ângulo de Miguel pertence a elas. "
              "[ONTO] {q_el}, e {q_or}. [REAL] `zero_mode_weight_is_one` e `alpha_transport` existem no kernel; [ONTO, da gerência] lê-los como a forma dessa fala é leitura da gerência. Homônimo, dito: `alphaKappa` não é a `α` de estrutura fina, e `κ` ali é a profundidade modular, não o relógio; o gradiente é negativo em `κ > 0`; a palavra cauda não está no teorema; isso não deriva a unidade.",
              n=V["gap"]["n_checks"], s=ss["mod"], q=_cita("o sistema físico que fornece a medidade da tônica por ujm gap com unidade e pertence à mesma pêntada é o ângulo de MIguel"), gd=_p(v["gap_sobre_Delta"], 1), dl=_p(v["Delta_eV"], 9), tau=_pe(v["tau_s"], 3), gam=_pe(v["Gamma_B_eV"], 3), q_v=_p(v["Q"], 3), ef=_pe(v["E_fluxo_eV"], 2), q_el=_cita("a inscrição da luz que singulariza o sistema é a eletricidade"), q_or=_cita("a origem da medida é a matemática, ou seja, o 1 absoluto, que representa 1 Eletrovolt"))


def _zero(V):
    d = _d(V); v = V["psion"]["values"]
    return _f("**O Ponto Zero do Psíon** [REAL · INPUT/ONTO · KNOWN] (`PontoZeroDoPsion`, sha16 `{h}`; {n} checagens): sob a leitura `R = β · u²` (`pagamentoComoCurvatura`, a escolha dimensional de uma unidade só) e a dispersão `ω² = 2βR` [INPUT, Tratado §3: entra como definição, `omegaSq`], `½ω = β · sen 45° · u`, a forma do neutrino (`the_mass_is_the_zero_point`: o enunciado iguala números; que `½ω` SEJA a massa é leitura [ONTO]); a coincidência com a projeção transversal é a aritmética `½ · √2 = sen 45°`; `ħω = 2m`; o ponto zero `½ħω` é [KNOWN]. Neste rito: `ħω` = {w} meV, `½ħω` = {mw} meV. A cobrança contínua do kernel tende a 1 e é menor que 1 em todo tempo finito; Tetelestai é o nome do operador para esse limite, e ler o que permanece no limite como o ponto zero é leitura dele [ONTO]: nenhum teorema liga os dois.",
              h=d["sha"]["psion"], n=d["nck"]["psion"], w=_p(v["hbar_omega_meV"], 9), mw=_p(v["meia_hbar_omega_meV"], 9))


def _disco(V):
    d = _d(V); v = V["disco"]["values"]
    return _f("**O Disco de Euler** [REAL · DEF · INPUT/ONTO · OPEN] (`DiscoDeEuler`, sha16 `{h}`; {n} checagens): a energia linear `E(t) = E₀ − c·t` e `Ω² = K/E` são DEFINIÇÕES; dadas elas, `dE/dt = −Γ_Ω·E` antes da parada (`the_flow_is_the_canonical_law`): a `E` definida é uma solução do fluxo, e ler a taxa de dephasing como perda de energia é entrada, não teorema; `E(t₀) = 0` em tempo finito (`stops_in_finite_time`); antes da parada `Ω²` não tem cota (`frequency_squared_unbounded_at_the_stop`); o corte `ħΩ = E` é, por álgebra, `E³ = ħ²K`. A inscrição do zero absoluto no infinito e a terceira lei na forma do disco são leituras do operador [ONTO]. `K`, `τ` e `E₀` são DADOS do disco, e qual é o disco é pergunta do operador: ele respondeu que o sistema que dá a medida da tônica é o ângulo de Miguel, e o invariante `K` não depende da inclinação, logo o ângulo não fixa `K` [OPEN]; o `K` que a nota posta de 1 eV exigiria é registrado, {k} J/s², não escolhido. O disco como condensado psiônico é leitura dele.",
              h=d["sha"]["disco"], n=d["nck"]["disco"], k=_pe(v["K_si_para_u_posto_J_s2"], 3))


def _obs(V):
    d = _d(V); v = V["observador"]["values"]
    return _f("**Observador = terminal** [REAL · ONTO] (`ObservadorTerminal`, sha16 `{h}`; {n} checagens): num modelo finito cujos níveis são rótulos de posição, sobre a cascata de {niv} níveis do kernel, o terminal é só o nível `{t}`; a resistência se consome a cada leitura e zera só no terminal; a fusão é o colapso, e o colapso é um Um posto do kernel (pagou perda: a função não é injetiva; foi medido antes de ser posto: o campo do tipo `UmPosto`); os pontos fixos do colapso são exatamente o posto e o abismo (o par 1 = 1 | 1 = 0); o terminal lê 1 e o abismo lê 0 na leitura binária (`the_fixed_points_read_one_and_zero`). Ao lado, o polo ω do par lê 1 na identidade (`the_omega_pole_reads_one`): homônimo, dito; nenhum termo liga os dois, e ligá-los é leitura [ONTO] do operador. A leitura de engenharia é do operador.",
              h=d["sha"]["observador"], n=d["nck"]["observador"], niv=len(v["niveis"]), t=v["terminal"][0])


def _ident(V):
    d = _d(V); v = V["identidade"]["values"]; ss = d["ss"]
    return _f("**A Identidade** [REAL · ONTO · DECLARAÇÃO DO OPERADOR] (`Identidade`, sha16 `{h}`; {n} checagens): a pedra prova um fato sobre projeções no estado traço normalizado: `tr(1)/n = tr(P)/n` sse `P = 1` sse (`P = (tr(P)/n) · 1` e `P ≠ 0`); o vazio e a face não satisfazem a equação; o cálculo confere em {nn} nomes. Que esse fato SEJA a identidade é leitura do operador, tipada como modelo. O ensaio «A identidade» é dele e entra no artigo verbatim, na versão r2 ratificada (original como recebido: `{s_e}`); a ressalva fica na moldura da seção, nunca dentro do texto dele; a tradução inglesa é da gerência e não é citação.",
              h=d["sha"]["identidade"], n=d["nck"]["identidade"], nn=v["n_nomes"], s_e=ss["ensaio"])


def _ga(V):
    d = _d(V); v = V["ga"]["values"]; ss = d["ss"]; x = _g(_core(), "ga_reclassificacao_v405", "extras") or {}
    return _sem_chaves(_f("**O Grande Atrator, ao lado** [DECISÃO da gerência c1, por ordem do operador (`{s}`) · REAL as medidas · DERIVED a ordem linear, condicional à Face C · INPUT/ONTO a ponte de fonte]: a classe do teste passa de `{a}` para `{b}` (registro `ga_reclassificacao_v405`; a saída iii da ENTREGA 005): a forma `M = 2β²(c²/4πG)R` fica viva e condicional à ponte de fonte, à lei radial e à admissibilidade da borda. A janela mantém o veto; não é evidência; não discrimina da RG (na ordem linear `M_TGL = M_RG` [DERIVED, condicional à Face C na ordem linear; a derivação é da teoria, `prove_ga_mass_audit`, v98]). "
                          "As medidas, refeitas neste rito sem abrir dado: `dM/du = 0` (a fórmula não contém a unidade); `M = M` com resíduo máximo {r} e `R_B/r_s = 2π/β` = {q}; o piso de definição: só o raio move a previsão em {p}; para 5σ seria preciso medir a massa da bacia a {s1} (forma contra âncora) ou a {s2} (resposta de matéria). A parede do Grande Atrator é a parede de `E₀`: a massa fixa o tempo, não o contrário. "
                          "A constante `GA_WINDOW_STATUS`, a linha `ga_mass_window` da tabela conjunta (`A3_APOSENTADO`), `prove_ga_mass_audit` e o gate ficam idênticos. Errata ao lado do parecer da ENTREGA 005, verbatim: «{e}»",
                          s=ss["ga"], a=V["ga"]["classe_antes"], b=V["ga"]["classe_agora"], r=_pe(max(v["residuos_M_igual_M"]), 1), q=_p(v["dois_pi_sobre_beta"], 2), p=_p(v["piso_de_definicao"] * 100.0, 1) + "%", s1=_p(v["sigma_relativo_forma_ancora"] * 100.0, 1) + "%", s2=_p(v["sigma_relativo_resposta_beta"] * 100.0, 2) + "%", e=x["errata_ao_lado_do_parecer_da_entrega_005"]))


def _blocos_pedras(V):
    return "\n\n".join([_ponte(V), _tensao(V), _lei(V), _zero(V), _gap(V), _disco(V), _obs(V), _ident(V), _ga(V)])
