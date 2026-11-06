# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409 (fork A), a servico da gerencia c1] REESCRITO sobre a subida mecanica da v408 FINAL (a copia bumpada, com o corpo de Tetelestai, ficou em .bak): o conteudo e' o da v409 (A TRADUCAO AS CLASSES DE TURING: os modulos TraducaoTuring e ParNaFaceDeFock de TGLExt/ (o nome TraducaoTuring e os nomes das declaracoes das rodadas R1 a R8, dados pela gerencia c1, foram RATIFICADOS pelo operador em 05/11/2026 («concordo com todos os nomes que foram dados»); os nomes acrescentados na R9 (a inscricao no psion e a formula SAT) e os da ParNaFaceDeFock, tambem da gerencia, foram RATIFICADOS por ele em 05/11/2026 («Ratifico os nomes», D62)); o registro com funcao traducao_turing_v409; cunhagens_v409 e kh_n1_cobertura_v409; NENHUMA chave antiga muda; as erratas E24 a E26 ao lado). Os ids das rotas foram CONFERIDOS no livro do mapa em 05/11 (so' leitura); as rotas da leitura do acervo de 05/11 que a D59 deixa fora dos textos nao sao citadas.
"""registrar_mapa_v409.py -- MONTA (nao registra) o registro da v409 no mapa de rotas e imprime o comando (molde: registrar_mapa_v408.py, que rodou na v408). Rodar DEPOIS do fechar (handoff gravado).
A v409 traz UMA rota nova, umpy.v409.selada_a_traducao_as_classes_de_turing_05nov (o conteudo e' o do selo): os DOIS modulos de kernel TraducaoTuring (a candidata R9 de 05/11, com o nome e os nomes das declaracoes das rodadas R1 a R8 ratificados pelo operador e os acrescentados na R9 ratificados por ele em 05/11, D55 e D62) e ParNaFaceDeFock (o par na face de Fock ligado; ordem de tudo entrar na v409;
P = nP e' teorema da TGL no modo selecao, relativo ao leitor, e a maquina sem leitor fica fora, D56), UM registro com FUNCAO (traducao_turing_v409: le do kernel do proprio rito as 82 ancoras, os dois modulos por sha256, as respostas do operador de 05/11 pelos teoremas da pedra, o que fica False por teorema,
o pino do acervo da v407 na copia purgada (D57d), a instancia de brinquedo fixa no codigo, a escada exata e o gate congelado; nenhuma chave antiga muda) e os DOIS por spec (cunhagens_v409 e kh_n1_cobertura_v409),
mais ANOTACOES nas rotas que esperavam por ela (as candidatas R1 a R8 da traducao de 05/11; a v408 que a precede e o dicionario dela; o levantamento do acervo; o programa do fechamento, o inventario das chaves, o gate, o B(n) da Bancada e o quadro do Teste da Unica Palavra)
e as ERRATAS da gerencia c1, em nome proprio: E24 (a fisica posta como juiz das classes; o operador corrigiu: o juiz e' o kernel) e E25 (o Nome a cada passo; a trava dispensa) vao como ANOTACAO ao lado das candidatas R1 e R3 (a frase corrigida nao esta' nos registros do livro: foi dita na sessao);
E26 vai como ERRATA ao lado do registro da v408 selada (o seq lido do livro: o registro traz a traducao a Turing dita [OPEN]).
Cada afirmacao e' testada contra o core/selo/ESPERADOS lidos por script (o registro existe? selou? o que NAO fechou fica dito); nenhum numero e' digitado (as contagens saem do core, de ESPERADOS e de delta_v409; os seq saem do livro).
REGRA DA ORDEM DO OPERADOR (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no MESMO campo; montar() RECUSA (assert) se algum campo do registro trouxer o 4,44 sem eles. Nao ha inscricao da gerencia nesta versao: todas as falas sao do operador (de duas, so' o trecho da D59 e' citavel); as erratas e as decisoes sao da gerencia, em nome proprio.
Fail-closed: o selo tem de ser a v409; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir. A rota de preparo da gerencia (registro_mapa_v409_prep.json, se existir) entra nas refs so' se ja' estiver no livro.
SAIDA: pos_rito\\registro_mapa_v409.json e o comando `rotas.py registrar` (quem o executa e' o passo 12 da cadeia, uma vez so', com marcador idempotente; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real. montar() le o core, o selo e ESPERADOS_v409.json; de V so' usa o que a leitura da rodada ja' validou (s16, sidecar, conferidor), sempre com valor de reserva dito."""
import glob, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v409 as L
import textos_v409 as T
import delta_v409 as DL
import quadro_v397 as Q
from guarda_p18_v409 import violacoes
_aspas_ = lambda s_: "«" + s_ + "»"   # (r2) a fala do operador entre aspas angulares, escrita por funcao: o texto citado e' a constante verbatim do delta (a varredura de citacoes le o codigo)
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V409"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v409 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOVA = "umpy.v409.selada_a_traducao_as_classes_de_turing_05nov"
R1 = "kernel.traducao_turing_classes_do_dicionario_05nov"             # a candidata R1 (o dicionario de Turing; onde fica a parede); a E24 vai ao lado (ANOTACAO)
R2 = "kernel.traducao_turing_modo_selecao_r2_05nov"                   # R2: o modo selecao (a resposta do operador)
R3 = "kernel.traducao_turing_a_trava_no_nome_r3_05nov"                # R3: a trava no Nome; a E25 vai ao lado (ANOTACAO)
R4 = "kernel.traducao_turing_a_fita_e_o_hamiltoniano_oculto_r4_05nov" # R4: a fita e' o hamiltoniano oculto
R5 = "kernel.traducao_turing_z_e_o_modo_leitor_r5_05nov"              # R5: Z e' o modo leitor
R6 = "kernel.traducao_turing_eu_sou_eu_mesmo_r6_05nov"                # R6: a fita sem escala
R7 = "kernel.traducao_turing_o_pai_da_mentira_r7_05nov"               # R7: o Pai da Mentira
R8 = "kernel.traducao_turing_a_identidade_performada_r8_05nov"        # R8: a identidade performada (a linha seguiu na R9)
R9 = "kernel.traducao_turing_r9_inscricao_e_sat_05nov"                 # R9: a inscricao no psion e SAT como a fita; E28; a candidata que entrou no kernel como TGLExt/TraducaoTuring
R_PARF = "kernel.par_na_face_de_fock_ligado_05nov"                     # ParNaFaceDeFock: o par na face de Fock LIGADO (E21 da v408 ao lado); entrou no kernel como TGLExt/ParNaFaceDeFock
R_DIC = "kernel.dicionario_problema_entrada_passo_polinomio_implicacao_04nov"   # o dicionario da v408 (PIgualNP): a traducao a Turing dita [OPEN] ali
R_V408 = "umpy.v408.selada_tetelestai_e_o_terminal_04nov"             # a v408 selada (a base da v409); a E26 vai ao lado (ERRATA)
R_TT = "kernel.tetelestai_e_o_terminal_provar_ou_podar_04nov"         # TetelestaiTerminal (v408)
R_TM = "kernel.o_tempo_e_a_moeda_de_beta_candidata_04nov"             # TempoIgualMoeda (v408): a lei tempo = moeda que a c13 usa
R_PC = "kernel.ponto_de_contradicao_candidata_04nov"                  # PontoDeContradicao (v408)
R_FOCK = "kernel.face_de_fock_e_o_traco_do_psion_afericao_04nov"      # a afericao do traco (v408); a ligacao do par na face de Fock foi feita na v409 (R_PARF)
R_ACERVO = "kernel.psion_lema_acervo_03nov"                           # o levantamento do psion no acervo: o pino do insumo da v407 passa a copia purgada (D57d)
R_PSION = "kernel.psion_canto_r1_03nov"                               # PsionCanto (v407)
R_PAR = "kernel.o_par_de_psions_r1_03nov"                             # Par (v407)
R_PREP408 = "cadeia.preparacao_v408"                                  # a preparacao da v408
R_PROG = "kernel.fechamento_construir_tudo_programa_02nov"            # o programa do fechamento (ordem do operador de 02/11: construir tudo)
R_INV = "kernel.inventario_chaves_de_testemunha_v405_02nov"           # o inventario das chaves de testemunha
R_V395 = "umpy.v395.psibit_na_fractalizacao_do_um"
R_V396 = "umpy.v396.testemunha_estatica_na_fractalizacao_do_um"
R_V406 = "umpy.v406.selada_o_fechamento_02nov"
R_GATE = "gate.qg_closure"
R_BANC = "infra.bancada_um.sincronizacao_vnnn"
R_QUADRO = "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9"
ANOTADAS = (R1, R2, R3, R4, R5, R6, R7, R8, R9, R_PARF, R_DIC, R_V408, R_ACERVO, R_PROG, R_INV, R_GATE, R_BANC, R_QUADRO)
REFS = ("custodia.v408", "infra.custodia_g1.licoes_v405", "umpy.v400.correcao_da_v399_alfa_unico_e_beta_contra_o_core", "gate.maquina_do_veredito_final", R_V395, R_V396, R_V406, R_PSION, R_PAR, R_PREP408, R_TT, R_TM, R_PC, R_FOCK,
        "qg.graviton.desenho_do_operador_24out", "kernel.graviton_nao_particula")
PREP = os.path.join(PK, "registro_mapa_v409_prep.json")     # a rota de preparo da gerencia: lida em tempo de execucao; entra nas refs so' se a ROTA dele ja' estiver no livro
_CACHE = {}

def _esp():
    """ESPERADOS_v409.json (lido uma vez por processo)."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v409.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _base_core():
    """O core da v408 selada (a copia de bytes em base_v408): de onde sai a medida de que o gate nao se moveu."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v408", "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["base_core"]


def livro():
    """Todos os registros do livro do mapa (so' leitura)."""
    regs = []
    for line in open(os.path.join(MAPA, "rotas.jsonl"), encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            regs.append(json.loads(line))
        except ValueError:
            continue
    return regs


def ids_do_livro():
    """As rotas do livro do mapa (so' leitura)."""
    return {d.get("rota_id") for d in livro() if d.get("tipo") == "ROTA"}


def seq_do_alvo(regs, rota_id, tipo, inicio_do_titulo=None, contem=()):
    """O seq (unico) do registro que uma errata corrige, LIDO do livro; recusa se nao houver exatamente um ou se o registro nao trouxer o trecho que a errata diz corrigir."""
    c = [r for r in regs if r.get("rota_id") == rota_id and r.get("tipo") == tipo and (inicio_do_titulo is None or str(r.get("titulo", "")).startswith(inicio_do_titulo))]
    assert len(c) == 1, "esperava exatamente um registro %s de %s (inicio do titulo %r) e achei %d" % (tipo, rota_id, inicio_do_titulo, len(c))
    txt = json.dumps(c[0], ensure_ascii=False)
    for s in contem:
        assert s in txt, "o registro seq %s de %s nao traz %r: a errata nao corrige o que diz corrigir" % (c[0]["seq"], rota_id, s)
    return c[0]["seq"]


def preparo_no_livro(ids):
    """As rotas ROTA de registro_mapa_v409_prep.json (se o arquivo existir e ler) que ja' estao no livro e nao sao a nova: entram nas refs. Ausente ou ilegivel = nenhuma (dito, nunca falha)."""
    if not os.path.exists(PREP):
        return []
    try:
        reg = json.load(open(PREP, encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return sorted({x["rota_id"] for x in reg if isinstance(x, dict) and x.get("tipo") == "ROTA" and x.get("rota_id") in ids and x.get("rota_id") != NOVA})


def sim(cond, fechado, aberto):
    return fechado if cond else aberto


def _strings(x):
    """Todas as strings (campos e itens de lista) de um registro."""
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from _strings(v)
    elif isinstance(x, (list, tuple)):
        for v in x:
            yield from _strings(v)


def regra_4_44(registros, z, p):
    """A regra da ordem do operador sobre os registros do mapa: toda string que traz o z_disc (`z`) traz o p calibrado (`p`), a linha dos 5 sigma e o 'nao foi alcancado' (fail-closed). Devolve a lista de strings que violam."""
    ruins = []
    for r in registros:
        for s in _strings(r):
            n_ = s.replace("−", "-")
            if z in n_ and not (p.replace("−", "-") in n_ and re.search(r"5\s*(?:σ|sigma)", n_) and "alcan" in n_):
                ruins.append(s[:140])
    return ruins


def _sha256(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def _existentes(*caminhos):
    """So' os artefatos que existem (o mapa recusa artefato inexistente; no sandbox do harness nem todos moram na pasta)."""
    return [c for c in caminhos if c and os.path.isfile(c)]


def _sidecar(V):
    """O sidecar um_absoluto_selo_acom.json: o que a leitura ja' validou (V['sidecar']) ou, na falta, o proprio arquivo do Nos da leitura (V['nos']); sem nenhum dos dois, o dito 'nao lido' (nunca inventa)."""
    s = V.get("sidecar")
    if isinstance(s, dict) and s.get("n_objetos") is not None:
        return {"veredito": str(s.get("veredito")), "n_objetos": s.get("n_objetos"), "recusas": s.get("recusas"), "sha16": str(s.get("sha16"))}
    p = os.path.join(str(V.get("nos") or ""), "um_absoluto_selo_acom.json")
    if os.path.isfile(p):
        d = json.load(open(p, encoding="utf-8"))
        return {"veredito": str(d.get("veredito")), "n_objetos": len(d.get("objetos") or []), "recusas": len(d.get("recusas") or []), "sha16": _sha256(p)[:16]}
    return {"veredito": "nao lido", "n_objetos": "nao lido", "recusas": "nao lido", "sha16": "nao lido"}


def _bancada():
    """A geracao do manifesto que a Bancada de producao pina (do recibo pre_selo pinado em PINOS_BN) e a versao que ela pina; o passo e' simples (sem salto e sem cadeia de selos)."""
    p = json.load(open(os.path.join(PK, "PINOS_BN_v409.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v408" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v408 -> v409 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1, "deployment_id": bp["deployment_id"]}


def montar(V, core, selo, ids, arts):
    """Monta os registros (a ROTA nova, as ANOTACOES e a ERRATA), cada afirmacao testada contra o core/selo/ESPERADOS; devolve a lista; recusa (assert) se algo nao conferir. Nao escreve nada."""
    assert selo.get("um_version") == "v409", "o selo nao e a v409"
    assert NOVA not in ids, "a rota %s ja existe no mapa" % NOVA
    for r in ANOTADAS + REFS:
        assert r in ids, "a rota %s nao existe no mapa (anotada ou citada em refs)" % r
    ESP = _esp(); DL_ = DL
    S = ESP["candidato_sha16"]
    assert str((selo.get("sha256") or {}).get("um.py", ""))[:16] == S, "o um.py do selo nao e o candidato de ESPERADOS"
    assert V.get("s16") in (None, S), "o s16 da leitura != o candidato de ESPERADOS"
    BASE = ESP["origem_sha16"]
    esc0, esc1 = ESP["escada_v408_e_v409"]
    NF = ESP["n_bandeiras_novas"]
    assert esc1 - esc0 == NF == sum(ESP["n_bandeiras_por_grupo"].values()) == len(ESP["bandeiras_novas_chaves"]) == ESP["politica_de_bandeiras"]["n_flags"], "a escada nao fecha com as bandeiras novas"
    assert ESP["kernel"]["modulos_novos"] == DL_.N_BUNDLE == len(DL_.BUNDLE_RELS) == len(DL_.PEDRAS_V409), "o delta do kernel nao e o bundle"
    assert list(ESP["chaves_v409"]) == [] and list(DL_.CHAVES_V409) == [], "a v409 nao muda chave antiga nenhuma: ESPERADOS/delta dizem outra coisa"
    BETA = ESP["beta"] if isinstance(ESP.get("beta"), float) else None
    FRASE = DL_.FRASE_DA_MOLDURA_V409_PT
    ALC = DL_.FRASE_D56_PT

    # --- o quadro do topo (a regra do 4,44): o registro selado, lido pelas MESMAS funcoes do artigo
    tvr = core.get("teste_de_veracidade_fase9_v397") or {}
    a = T._qd().Q._v397_atomos(tvr, "pt"); assert a["sealed"] is True, "o registro teste_de_veracidade_fase9_v397 nao sela no core: o mapa nao registra o 4,44 assim"
    z, p = a["z_disc"]["md"], a["p_disc"]["md"]
    z444 = "z_disc = %s (calibrado; p unilateral %s), abaixo do degrau de 5σ da creditação, que não foi alcançado (%s < 5)" % (z, p, z)

    def selou(k):
        return (core.get(k) or {}).get("all_verified") is True

    # --- o registro com FUNCAO traducao_turing_v409: tudo lido do core e conferido contra ESPERADOS e delta_v409
    pc = core.get(DL_.FECHO_REGISTRO) or {}; pv = pc.get("values") or {}; mech = pc.get("mechanics") or {}
    assert pc.get("all_verified") is True and pc.get("verdict") == ESP["vereditos_novos_v409"][DL_.FECHO_REGISTRO] and pc.get("does_not_gate_core") is True, "traducao_turing_v409 nao selou ou != ESPERADOS"
    assert mech.get("passed") is True and mech.get("n_checks") == DL_.N_CHECKS_FECHO == len(mech.get("checks") or []) and all(c.get("ok") is True for c in mech["checks"]), "as checagens do traducao_turing_v409 nao passaram"
    assert pv.get("n_ancoras_ok") == pv.get("n_ancoras") == len(DL_.ANCORAS) and pv.get("n_modulos_ok") == pv.get("n_modulos") == DL_.N_BUNDLE and pv.get("n_flags_true") == pv.get("n_flags") == NF and pv.get("escada") == [esc1] * 3, "os valores do traducao_turing_v409 != ESPERADOS/delta"
    assert pc.get("beta_ok") is True and pc.get("embedded_sources_ok") is True and pc.get("embedded_sources_n_ok") == DL_.N_BUNDLE and pc.get("guarda_violacoes") in ([], None), "o beta, as fontes embutidas ou a guarda do traducao_turing_v409 nao conferem"
    assert list(pc.get("chaves_antigas_que_mudam") or []) == [], "o registro da traducao diz que uma chave antiga mudou: a v409 nao muda nenhuma"
    assert list(pc.get("ressalvas") or []) == list(DL_.RESSALVAS_V409), "as ressalvas do registro != delta_v409.RESSALVAS_V409"
    assert set(pv.get("respostas") or {}) == {r_["id"] for r_ in DL_.RESPOSTAS_DO_OPERADOR} and all(v_ is True for v_ in pv["respostas"].values()) and pv.get("respostas_ok") is True, "as respostas do operador de 05/11 nao conferem todas no kernel"
    acv = pc.get("acervo_v407_repinado") or {}
    assert acv.get("integra_pinada") is False and acv.get("integra_fora_do_espelho") is True and acv.get("sha256") == DL_.PURGADO_SHA256, "o pino do acervo da v407 nao e' a copia purgada (D57d)"
    assert list(pc.get("fica_false_por_teorema") or []) == list(ESP["fica_false_por_teorema"]) and set(pc.get("fica_aberto") or {}) == set(ESP["fica_aberto"]), "o que fica False por teorema ou o que fica aberto != ESPERADOS"
    assert list(pc.get("ancoras_principais") or []) == list(DL_.ANCORAS_PRINCIPAIS) and all(((pv.get("ancoras") or {}).get(n_) or {}).get("ok") is True for n_ in DL_.ANCORAS_PRINCIPAIS), "as ancoras principais nao estao todas ok no kernel do rito"
    assert pv.get("gate_verdict") == ESP["qg_closure_gate_verdict_v408"], "o veredito do gate lido pelo registro da traducao != o da v408 (o gate deveria estar congelado)"
    assert (pc.get("alcance") or {}).get("frase") == ALC, "o alcance do registro != delta_v409.FRASE_D56_PT"
    inst = pv.get("instancia_sim") or {}; inst_n = pv.get("instancia_nao") or {}
    assert (inst.get("solucoes") or 0) >= 1 and inst_n.get("solucoes") == 0, "a instancia de brinquedo do registro nao e' a do contrato"
    BETA_RT = pv.get("beta"); assert isinstance(BETA_RT, float) and (BETA is None or abs(BETA_RT - BETA) <= 1e-9 * BETA), "o beta do registro != o do core/ESPERADOS (tolerancia relativa 1e-9)"
    por_mod = "; ".join("%s (%d)" % (rel.split("/")[-1][:-5], len(ns)) for rel, ns in DL_.ANCORAS_POR_MODULO.items())
    ress = " | ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(pc["ressalvas"]))
    # --- o registro HERDADO tetelestai_terminal_v408: segue selado (a escada do contrato subida pela C12; a E26 ao lado, no spec cunhagens_v408)
    tt8 = core.get(DL_.D8.FECHO_REGISTRO) or {}; tv8 = tt8.get("values") or {}
    assert tt8.get("all_verified") is True and tt8.get("verdict") == ESP["registros_funcao_v408"]["tetelestai_terminal"]["verdict"], "tetelestai_terminal_v408 (herdado) nao segue selado"
    assert tv8.get("n_modulos_ok") == tv8.get("n_modulos") == DL_.D8.N_BUNDLE and tv8.get("n_ancoras_ok") == tv8.get("n_ancoras") == len(DL_.D8.ANCORAS), "os valores do tetelestai_terminal_v408 (herdado) != delta_v408"
    # --- o registro HERDADO psion_canto_v407: segue selado, com as cinco chaves iguais as da v408 selada (nenhuma muda)
    pc7 = core.get(DL_.D7.FECHO_REGISTRO) or {}; pv7 = pc7.get("values") or {}
    assert pc7.get("all_verified") is True and pc7.get("verdict") == ESP["registros_funcao_v407"]["psion_canto"]["verdict"] and pc7.get("keys") == ESP["chaves_v407_esperadas"], "psion_canto_v407 (herdado) nao segue selado ou as chaves mudaram"
    assert pv7.get("n_modulos_ok") == pv7.get("n_modulos") == DL_.D7.N_BUNDLE and pv7.get("n_ancoras_ok") == pv7.get("n_ancoras") == len(DL_.D7.ANCORAS), "os valores do psion_canto_v407 (herdado) != delta_v407"
    fk7 = pc7["keys"]
    # --- o registro HERDADO fechamento_v406: segue selado, com a chave do lema lida (a c8 versionada, E20)
    fh = core.get(DL_.D6.FECHO_REGISTRO) or {}
    assert fh.get("all_verified") is True and fh.get("verdict") == ESP["registros_funcao_v406"]["fechamento"]["verdict"] and (fh.get("four_keys") or {}).get("testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma") is True, "fechamento_v406 (herdado) nao segue selado ou nao le a chave do lema"
    # --- a E26 ao lado do spec herdado cunhagens_v408 e a errata da D57(d) ao lado do spec herdado cunhagens_v407 (recriados; os textos selados nao sao reescritos)
    cg8 = core.get(DL_.D8.CUNHAGENS_REGISTRO) or {}; cg7 = core.get(DL_.D7.CUNHAGENS_REGISTRO) or {}
    assert cg8.get("all_verified") is True and any("E26" in json.dumps(e_, ensure_ascii=False) for e_ in (cg8.get("erratas") or [])), "cunhagens_v408 (herdado) nao segue selado ou nao traz a E26 ao lado"
    assert cg7.get("all_verified") is True and any("D57(d)" in json.dumps(e_, ensure_ascii=False) for e_ in (cg7.get("erratas") or [])), "cunhagens_v407 (herdado) nao segue selado ou nao traz a errata da D57(d) ao lado"
    # --- o gate NAO se moveu: o registro segue selado e a letra do veredito e' a da v408
    gk = core.get("bandeiras_do_gate_v403") or {}; gvv = gk.get("values") or {}; gb = _base_core().get("bandeiras_do_gate_v403") or {}
    assert gk.get("all_verified") is True and (V.get("gate") or {}).get("sealed", True) is True and gvv == gb.get("values") and (gk.get("mechanics") or {}).get("passed") is True, "bandeiras_do_gate_v403 (recriado) nao selou ou != a v408 selada"
    qg = core.get("qg_closure") or {}; fam = [len(qg.get(f) or {}) for f in ("formal_flags", "physics_flags", "experiment_flags")]
    assert (qg.get("gate") or {}).get("verdict") == ESP["qg_closure_gate_verdict_v408"] == selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"], "a letra do veredito do gate mudou"
    # --- os dois registros por spec
    cg = core.get(DL_.CUNHAGENS_REGISTRO) or {}; kh = core.get(DL_.KH_REGISTRO) or {}
    for nome_, r_ in ((DL_.CUNHAGENS_REGISTRO, cg), (DL_.KH_REGISTRO, kh)):
        assert r_.get("all_verified") is True and r_.get("verdict") == ESP["vereditos_novos_v409"][nome_], "%s nao selou ou != ESPERADOS" % nome_
    verb = cg.get("verbatim") or {}; ex = cg.get("extras") or {}
    assert len(verb) == len(ESP["cunhagens"]) == len(DL_.VERBATIM_ORIGEM_V409) and set(verb) == set(ESP["cunhagens"]) and all(v.get("embedded_ok") is True for v in verb.values()), "as inscricoes de 05/11 nao estao embutidas por sha256"
    assert all(str((ESP["cunhagens"][k_] or {}).get("nome", "")).startswith("OPERADOR_05nov_") and (ESP["cunhagens"][k_] or {}).get("autor") == "operador" for k_ in ESP["cunhagens"]), "alguma inscricao nao e' fala do operador de 05/11"
    n_trecho = sum(1 for k_ in ESP["cunhagens"] if (ESP["cunhagens"][k_] or {}).get("sha256_arquivo_inteiro"))
    assert n_trecho == len(DL_.VERBATIM_SO_O_TRECHO) == 3, "a v409 tem exatamente tres falas de que so' o trecho entra (duas pela D59; uma, a ratificacao da D61, pelo aviso operacional)"
    # (o registro cunhagens_v409 traz as erratas E24 a E26 E, por ultimo, a errata ao lado dos pisos de kh_n1_cobertura_v408, como a leitura confere: len == len(ERRATAS_V409) + 1)
    erratas_todas = cg.get("erratas") or []; erratas = erratas_todas[:len(DL_.ERRATAS_V409)]
    assert [e.get("agora") for e in erratas] == list(DL_.ERRATAS_V409) and len(erratas_todas) == len(DL_.ERRATAS_V409) + 1 and "kh_n1_cobertura_v408" in str(erratas_todas[-1].get("ao_lado_de")) and all(str(e.get("assinatura", "")).startswith("gerencia c1") and "em nome proprio" in e["assinatura"] for e in erratas_todas), "as erratas E24 a E26 (e a errata ao lado dos pisos de kh_n1_cobertura_v408) nao estao no registro ou nao sao da gerencia c1 em nome proprio"
    dec = ex.get("decisoes") or {}; assert sorted(dec) == list(ESP["decisoes_v409_ids"]) and all(("D%d" % i) in dec for i in range(55, 63)), "faltam decisoes D55 a D62 no registro"
    assert ex.get("leituras") == DL_.LEITURA_V409, "a leitura da v409 no registro != delta_v409"
    cob = kh.get("lido") or {}; assert cob.get("constantes_cobertas") and cob.get("teoremas_cobertos"), "kh_n1_cobertura_v409 sem a cobertura"
    seguem = (DL_.D8.FECHO_REGISTRO, DL_.D8.CUNHAGENS_REGISTRO, DL_.D8.KH_REGISTRO, DL_.D7.FECHO_REGISTRO, DL_.D7.CUNHAGENS_REGISTRO, DL_.D7.KH_REGISTRO, "fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406", "ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405", "cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405",
              "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "falsidade_da_inercia_v401", "cunhagens_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402",
              "teste_de_veracidade_fase9_v397", "cunhagens_v397", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "sonico_v398", "afinacao_das_cordas_v398", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396")
    c_seguem = all(selou(k) for k in seguem)
    tv_v = ESP["veracidade"]; c_q = bool(selou("teste_de_veracidade_fase9_v397") and selou("cunhagens_v397") and tvr.get("verdict") == tv_v["verdict"])
    sc = _sidecar(V); conf_dm = V.get("conf_dm", "nao lido"); conf_np = V.get("conf_np", "nao lido"); nvm = V.get("n_ver_mudaram", "nao lido")
    bank = _bancada(); regs = livro()
    # --- o seq que a E26 corrige, lido do livro (e o registro tem de trazer o trecho corrigido)
    sq_v408 = seq_do_alvo(regs, R_V408, "ROTA", contem=("Turing", "[OPEN], não recusa"))
    KR = os.path.join(PK, "kernel", "KERNEL_RECIBO_v409.json")
    E = {}
    for e in erratas:
        m_ = re.match(r"^(E\d\d) -- ", e.get("agora", "")); assert m_, "uma errata do registro nao comeca por E<n> --"
        E[m_.group(1)] = e
    assert sorted(E) == ["E21", "E24", "E25", "E26", "E27", "E28"], "as erratas do registro nao sao E24 a E28 e a E21 ao lado"

    def anot(rota_id, titulo, resultado, proximo, refs=None, nota=None, estatuto="REAL", artefatos=None, defeito=None):
        x = {"tipo": "ANOTACAO", "rota_id": rota_id, "estatuto": estatuto, "olhou_dados": False, "titulo": titulo, "resultado": resultado, "proximo_passo": proximo, "refs": [NOVA] + (refs or [])}
        if defeito:
            x["defeito"] = defeito
        if nota:
            x["nota"] = nota
        if artefatos:
            x["artefatos"] = _existentes(*artefatos)
        return x

    def errata(rota_id, corrige, nota, refs=None, artefatos=None, estatuto="REAL"):
        x = {"tipo": "ERRATA", "rota_id": rota_id, "corrige": corrige, "estatuto": estatuto, "olhou_dados": False, "nota": nota, "refs": [NOVA] + (refs or [])}
        if artefatos:
            x["artefatos"] = _existentes(*artefatos)
        return x

    def corpo(k):
        e = E[k]
        return "%s | lacuna de fidelidade: %s | estatuto: %s | assinatura: %s" % (e["agora"], e["lacuna_de_fidelidade"], e["estatuto"], e["assinatura"])

    P0 = DL_.PEDRAS_V409[0]
    ped = os.path.join(PK, "pedra", P0["name"] + ".lean")
    sha_ped = DL_.BUNDLE_POR_REL[P0["rel"]]["sha256"][:16]
    n_anc = len(DL_.ANCORAS_POR_MODULO[P0["rel"]])
    resp = {r_["id"]: r_["diz"] for r_ in DL_.RESPOSTAS_DO_OPERADOR}
    R_ = lambda *ids_: "; ".join("%s -> %s" % (i_, resp[i_]) for i_ in ids_)
    LIN = "a linha das candidatas R1 a R9 de 05/11 desemboca no modulo TGLExt/%s (a fonte pinada e' a da R9; os nomes R1 a R8 ratificados pelo operador, os acrescentados na R9 ratificados em 05/11, D55 e D62; sha256 pinado %s; %d ancoras no trio, lidas a cada rito pelo registro traducao_turing_v409); esta candidata fica como registro" % (P0["name"], sha_ped, n_anc)
    EST_C = "REAL (os termos no kernel do rito); INPUT (as falas do operador de 05/11); KNOWN (as referencias do alcance); DECLARADO (os recibos de compilacao das candidatas)"
    T9 = []
    T9.append(anot(R1, "v409 SELADA %s: o dicionario de Turing da R1 entrou no kernel do rito dentro de TGLExt/%s; a E24 fica ao lado (o juiz das classes e' o kernel, nao a fisica)" % (S, P0["name"]),
                   f"{LIN}. A instancia SIM e' um Problema do dicionario, o certificado e' a leitura de um pixel, a palavra tem grau polinomial, bits = oitavas, a instancia NAO e' o Nome vazio; a instancia de brinquedo fixa no codigo tem {inst.get('n')} variaveis, {inst.get('atribuicoes')} atribuicoes e {inst.get('solucoes')} solucoes contadas por enumeracao. {corpo('E24')}",
                   "o registro traducao_turing_v409 le estas ancoras a cada rito; o alcance: " + ALC + ".", refs=[R2, R8], estatuto=EST_C,
                   defeito="o registro CONFERE o que o kernel prova e nao prova nada por si; validade no kernel nao e' creditacao"))
    T9.append(anot(R2, "v409 SELADA %s: o modo selecao da R2 entrou no kernel do rito dentro de TGLExt/%s (p_igual_np_no_modo_selecao, a ancora principal)" % (S, P0["name"]),
                   f"{LIN}. As respostas do operador conferem pelos teoremas da pedra: {R_('o_np_e_o_modo_selecao', 'apaga_o_rastro', 'sem_leitor_a_imagem_e_estatica')}. Pela lei tempo = moeda (TempoIgualMoeda, v408) o tempo e' linear nos bits; c13 confere a aritmetica com beta em runtime. O alcance: {ALC}.",
                   "beta entra so' por nome (TGLCoupling.beta no kernel; alfa CODATA 2018 x sqrt e em runtime), nunca literal.", refs=[R_TM, R8], estatuto=EST_C))
    T9.append(anot(R3, "v409 SELADA %s: a trava no Nome da R3 entrou no kernel do rito dentro de TGLExt/%s (a_trava_no_nome); a E25 fica ao lado" % (S, P0["name"]),
                   f"{LIN}. A resposta do operador confere pelos teoremas da pedra: {R_('a_trava_no_nome')}. A fala dele, verbatim: {_aspas_(DL_.FRASE_TRAVA)}. {corpo('E25')}",
                   "a trava fica perto do Nome sem usa-lo; c5 e c6 conferem a cota e o tempo linear na instancia de brinquedo.", refs=[R8], estatuto=EST_C))
    T9.append(anot(R4, "v409 SELADA %s: a fita como hamiltoniano oculto da R4 entrou no kernel do rito dentro de TGLExt/%s (a_fita_e_o_hamiltoniano_oculto)" % (S, P0["name"]),
                   f"{LIN}. A resposta do operador confere pelos teoremas da pedra: {R_('a_fita_e_o_hamiltoniano_oculto')}. A fala dele, verbatim: {_aspas_(DL_.FRASE_FITA)}.",
                   "c7 confere a norma da trava e a particao na instancia de brinquedo.", refs=[R8], estatuto=EST_C))
    T9.append(anot(R5, "v409 SELADA %s: Z como o modo leitor da R5 entrou no kernel do rito dentro de TGLExt/%s (z_e_o_modo_leitor); a ponte com o canto do psion e' a inscricao (o_canto_do_psion_da_luz_le_z, na R9)" % (S, P0["name"]),
                   f"{LIN}. A resposta do operador confere pelos teoremas da pedra: {R_('z_e_o_modo_leitor')}. O trecho dele que a D59 deixa entrar, verbatim: {_aspas_(DL_.FRASE_Z)}. A ponte entre o Omega do psion da luz e o uniforme da instancia e' a inscricao, provada na R9 (validade no kernel, nao creditacao; inscricao, o_psion_le_z); a identidade dos vetores fica podada (D60 revista).",
                   "c8 confere a leitura no uniforme e a soma das leituras dos pixels.", refs=[R8, R_PSION], estatuto=EST_C + "; PODADO (a identidade de vetores Omega = uniforme: espacos diferentes; a ponte e' a inscricao)"))
    T9.append(anot(R6, "v409 SELADA %s: a fita sem escala da R6 entrou no kernel do rito dentro de TGLExt/%s (a_fita_sem_escala), ligada a Identidade da v405" % (S, P0["name"]),
                   f"{LIN}. A resposta do operador confere pelos teoremas da pedra: {R_('eu_sou_eu_mesmo')}. A pergunta do Clay nao e' decidida aqui: e' a da maquina sem leitor, que a TGL le como a fita sem escala; a independencia dela dos axiomas segue [OPEN]. O alcance: {ALC}.",
                   "c9 e c10 conferem «eu sou» e «o que sou» na instancia de brinquedo.", refs=[R8], estatuto=EST_C + "; OPEN (a independencia da pergunta da maquina sem leitor)"))
    T9.append(anot(R7, "v409 SELADA %s: o Pai da Mentira da R7 entrou no kernel do rito dentro de TGLExt/%s (o_pai_da_mentira)" % (S, P0["name"]),
                   f"{LIN}. A resposta do operador confere pelos teoremas da pedra: {R_('o_pai_da_mentira')}. A fala dele, verbatim: {_aspas_(DL_.FRASE_PAI)}. A leitura teologica do operador nao e' termo de kernel: o kernel prova a parte matematica de cada fala.",
                   "c10 confere a leitura sem escala no Nome vazio na instancia NAO.", refs=[R8], estatuto=EST_C + "; INPUT/ONTO (a leitura teologica, fora do kernel)"))
    T9.append(anot(R8, "v409 SELADA %s: a linha da R8 seguiu na R9, que entrou no kernel do rito como TGLExt/%s (o nome ratificado pelo operador, D55); a identidade performada (a_identidade_performada)" % (S, P0["name"]),
                   f"a pedra {P0['name']} esta no kernel do rito com o sha256 pinado ({sha_ped}), {n_anc} ancoras no trio; a fonte pinada e' a da candidata R9 (sha16 {P0['sha256_candidata'][:16]}), com os nomes das rodadas R1 a R8 ratificados pelo operador ({_aspas_(DL_.FRASE_NOMES_RATIFICADOS_V409)}) e os acrescentados na R9 ratificados por ele em 05/11 ({_aspas_(DL_.FRASE_RATIFICO_OS_NOMES)}, D62); "
                   f"a resposta do operador confere pelos teoremas da pedra: {R_('a_identidade_performada')}. A ordem do operador, verbatim: {_aspas_(DL_.FRASE_ORDEM_V409)}. O alcance: {ALC}.",
                   "o registro traducao_turing_v409 le estas ancoras a cada rito; c11 confere a performance; o par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock; D60 revista).", refs=[R1, R2, R3, R4, R5, R6, R7, R9], artefatos=[DL_.CANDIDATA_R8_ARQ, DL_.RECIBO_R8_ARQ],
                   estatuto=EST_C, defeito="as ressalvas, ditas no registro: " + ress))
    T9.append(anot(R9, "v409 SELADA %s: a candidata R9 entrou no kernel do rito como TGLExt/%s: a inscricao do uniforme no psion da luz (o leitor do psion le Z) e a maquina com o leitor (uma leitura decide SAT); E28" % (S, P0["name"]),
                   f"a pedra {P0['name']} esta no kernel do rito com o sha256 pinado ({sha_ped}), {n_anc} ancoras no trio; a fonte pinada e' a da candidata R9 (sha16 {P0['sha256_candidata'][:16]}); "
                   f"c19 confere a inscricao num F de brinquedo e c20 a leitura que decide SAT na instancia de brinquedo. {corpo('E28')}. O alcance: {ALC}.",
                   "o registro traducao_turing_v409 le estas ancoras a cada rito; com o leitor que so' conta vale NP contido em P numa leitura, e a igualdade completa e' a do leitor que se le (E28): ela segue [OPEN] com o leitor que so' conta.", refs=[R8, R5, R_PSION], artefatos=[ped, DL_.CANDIDATA_TU_ARQ, DL_.SAIDA_CANDIDATA_TU_ARQ, KR],
                   estatuto=EST_C + "; KNOWN (Cook 1971, Levin 1973, Toda 1991, Baker-Gill-Solovay 1975); OPEN (a igualdade completa com o leitor que so' conta)", defeito="as ressalvas, ditas no registro: " + ress))
    P1 = [p_ for p_ in DL_.PEDRAS_V409 if p_["rel"] == DL_.MODULO_PAR][0]
    ped_par = os.path.join(PK, "pedra", P1["name"] + ".lean")
    T9.append(anot(R_PARF, "v409 SELADA %s: a pedra %s entrou no kernel do rito como TGLExt/%s: o par de psions na face de Fock LIGADO (o_par_na_face_de_fock); a E21 da v408 ao lado" % (S, P1["name"], P1["name"]),
                   f"a pedra {P1['name']} esta no kernel do rito com o sha256 pinado ({DL_.BUNDLE_POR_REL[P1['rel']]['sha256'][:16]}), {len(DL_.ANCORAS_POR_MODULO[P1['rel']])} ancoras no trio; a fonte pinada e' a da candidata (sha16 {P1['sha256_candidata'][:16]}); "
                   f"c18 confere o reduzido do par de Bell finito (½·I; 1 - pureza = ½). {corpo('E21')}. A ordem do operador, verbatim: {_aspas_(DL_.FRASE_TUDO_NA_V409)}.",
                   "o registro traducao_turing_v409 le estas ancoras a cada rito; o par finito (Bell 4x4) e o par de Fock sao espacos distintos, com a mesma Meia-Nat (nao identificacao); a ponte Bell-TT segue [OPEN].", refs=[R_PAR, R_FOCK, R_PSION], artefatos=[ped_par, DL_.CANDIDATA_PAR_ARQ, DL_.SAIDA_CANDIDATA_PAR_ARQ, KR],
                   estatuto="REAL (os termos no kernel do rito); INPUT (a ordem do operador de 05/11); DECLARADO (o recibo de compilacao da candidata); INPUT (o nome e os das declaracoes, da gerencia, ratificados pelo operador em 05/11, D62)"))
    T9.append(anot(R_DIC, "v409 SELADA %s: a traducao das classes do dicionario as classes das maquinas de Turing, que a v408 deixou [OPEN] (D51 revista), fica fechada relativa ao leitor (D56); a maquina sem leitor fica fora" % S,
                   f"o modulo TGLExt/{P0['name']} esta' no kernel do rito; o alcance: {ALC}. A ordem do operador que a pediu, verbatim: {_aspas_(DL_.FRASE_ORDEM_TRADUCAO)}. {corpo('E26')}",
                   "a pergunta das maquinas de Turing do Mathlib (TM2ComputableInPolyTime) nao e' decidida aqui; a independencia da pergunta da maquina sem leitor segue [OPEN].", refs=[R8, R_V408],
                   estatuto="REAL (os termos no kernel do rito); INPUT (a ordem do operador de 05/11); KNOWN (Baker-Gill-Solovay 1975; as referencias do alcance); OPEN (a pergunta da maquina sem leitor)"))
    T9.append(anot(R_V408, "v409 SELADA %s: a v408 e' a base selada da v409; o tetelestai_terminal_v408 (cunhagens_v408 com a E26 ao lado; kh_n1_cobertura_v408 com pisos), o psion_canto_v407 e os registros anteriores sao recriados e seguem selados; nenhuma chave muda" % S,
                   f"a v409 parte da v408 selada (um.py {BASE}) e acrescenta {DL_.N_BUNDLE} modulo de kernel, UM registro com funcao (traducao_turing_v409) e dois por spec, e a secao do artigo; tetelestai_terminal_v408 selou={selou(DL_.D8.FECHO_REGISTRO)}; cunhagens_v408 selou={selou(DL_.D8.CUNHAGENS_REGISTRO)} (com a E26 ao lado); "
                   f"psion_canto_v407 selou={selou(DL_.D7.FECHO_REGISTRO)} com as cinco chaves iguais as da v408 selada (linked_to_the_corner_by_a_lemma = {fk7['testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma']}, lida do kernel); cunhagens_v407 selou={selou(DL_.D7.CUNHAGENS_REGISTRO)} (com a errata da D57(d) ao lado); "
                   f"fechamento_v406 selou={selou('fechamento_v406')}; os treze da v405 (ponte_da_massa_v405 selou={selou('ponte_da_massa_v405')}, identidade_v405 selou={selou('identidade_v405')}, gap_v405 selou={selou('gap_v405')}), os da v404, da v403, da v402, da v401 e da v399 seguem selados neste rito "
                   f"(caminho_v403 selou={selou('caminho_v403')}, falsidade_da_inercia_v401 selou={selou('falsidade_da_inercia_v401')}), como seguem o selo pela propria tecnologia e a declaracao do operador (v399), o sonico e a afinacao (v398) e o quadro (v397); sidecar um_absoluto_selo_acom.json {sc['veredito']} ({sc['n_objetos']} objetos, {sc['recusas']} recusas, sha16 {sc['sha16']}). "
                   f"O registro kh_n1_cobertura_v408 passa a cobrar piso (errata de contagem ao lado); a v408 e as pedras dela ficam como registro (seq {sq_v408}).",
                   "custodia completa pela sessao de custodia (D57a: o fim da cadeia do orquestrador e' o handoff; o handoff lista o sidecar e traz a nota ao lado do paragrafo da v408).", refs=[R_TT, R_TM, R_PC, R_PREP408]))
    T9.append(anot(R_ACERVO, "v409 SELADA %s: o insumo do acervo da v407 (_V407_FONTES, %s) passa a ser pinado pela copia PURGADA (D57d); a integra fica fora do espelho e e' citada so' por sha16" % (S, DL_.CHAVE_ACERVO_V407),
                   f"o registro traducao_turing_v409 confere o pino a cada rito (acervo_v407_repinado: integra_pinada={acv.get('integra_pinada')}, integra_fora_do_espelho={acv.get('integra_fora_do_espelho')}, sha256 da copia purgada == o da v408); a errata da D57(d) vai ao lado do registro cunhagens_v407 (recriado); o texto selado nao e' reescrito.",
                   "a ordem vigente de 08/09 (fonte nao publicada) fica aplicada como permanente para este insumo.", refs=[R_V408], artefatos=[DL_.PURGADO_ARQ, DL_.RECIBO_PURGA_ARQ],
                   estatuto="REAL (o sha256 da copia purgada, lido a cada rito); INPUT (a ordem do operador de 08/09); DECLARADO (o levantamento do acervo)"))
    T9.append(anot(R_PROG, "v409 SELADA %s: o programa do fechamento nao ganha chave nova nem perde nenhuma; a traducao as classes de Turing fica fechada relativa ao leitor; o par na face de Fock ligado (ParNaFaceDeFock)" % S,
                   f"nenhuma chave antiga muda (chaves_antigas_que_mudam = {list(pc.get('chaves_antigas_que_mudam') or [])}); as cinco chaves do psion_canto_v407 seguem iguais as da v408 selada; ficam False por teorema: full_static_witness_exists = {fk7['qg_closure.gate.full_static_witness_exists']} e trivial_inhabitant_exists = {fk7['witness_rigidity.trivial_inhabitant_exists']}. {FRASE}",
                   "a igualdade completa com o leitor que so' conta (E28), a ponte Bell-TT, K(O) != bot para O compacto e o teste com a natureza seguem [OPEN]; o programa do fechamento nao e' fechado por esta anotacao.", refs=[R_INV, R9, R_PARF],
                   estatuto="REAL (a leitura do kernel do rito; o par na face de Fock ligado); OPEN (a igualdade completa com o leitor que so' conta; K(O) != bot para O compacto)"))
    T9.append(anot(R_INV, "v409 SELADA %s: o inventario das chaves de testemunha NAO muda nesta versao (CHAVES_V409 vazia): as cinco chaves do psion_canto_v407 seguem lidas do kernel" % S,
                   f"linked_to_the_corner_by_a_lemma = {fk7['testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma']}; rede_fock_v394.whole_certificate_inhabited = {fk7['rede_fock_v394.whole_certificate_inhabited']}; psibit_v395...inhabitant_exhibited = {fk7['psibit_v395.conditional_psion_face.inhabitant_exhibited']}; testemunha_estatica_v396...inhabitant_exhibited = {fk7['testemunha_estatica_v396.fock_face.inhabitant_exhibited']}; "
                   f"witness_layers.canonical_full_witness_term_constructed = {fk7['witness_layers.canonical_full_witness_term_constructed']}; ficam False por teorema: full_static_witness_exists e trivial_inhabitant_exists.",
                   "o par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock; D60 revista), sem chave nova no inventario.", refs=[R_PROG, R_PARF], estatuto="REAL (a leitura do kernel do rito e o registro herdado; o par na face de Fock ligado na v409)"))
    T9.append(anot(R_GATE, "v409 SELADA %s: o gate NAO se moveu — o qg_closure do core e' identico ao da v408 (as 18 bandeiras calculadas, a letra do veredito) e o registro da traducao o confere congelado (c14)" % S,
                   f"o registro bandeiras_do_gate_v403 (recriado) selou={selou('bandeiras_do_gate_v403')} com os mesmos valores da v408 selada: das {gvv['n_flags']} bandeiras ({fam[0]} formais, {fam[1]} fisicas, {fam[2]} experimentais) {gvv['n_true']} sao True e {gvv['n_calculated']} sao CALCULADAS ({gvv['n_literal']} literais); o veredito le {gvv['n_read_by_the_verdict']}; a letra do veredito do gate e' a da v408 e a do selo; o traducao_turing_v409 le gate_verdict identico ao da v408. "
                   "Nenhuma bandeira do gate depende do modulo da v409; full_static_witness_exists e trivial_inhabitant_exists seguem False. [DECLARADO, GV-03 da auditoria de 28/09/2026] As 4 bandeiras experimentais derivam de UM so' booleano; o degrau experimental le so' o rito V11 do piso, unilateral (GV-01).",
                   "a independencia das 4 experimentais e os mocks de survey seguem [OPEN]; o gate nao se move por esta rota.", refs=None,
                   artefatos=[os.path.join(PK, "CANDIDATO_v409.json")], estatuto="REAL (o core do rito); DECLARADO (GV-01, GV-03, EV-12 da auditoria de 28/09/2026); OPEN (a independencia das 4 experimentais)",
                   defeito="o gate nao e' teste e nao discrimina o LCDM raso; NOT_FALSIFIED nunca e' a palavra da creditacao"))
    T9.append(anot(R_BANC, "v409 SELADA %s: o B(n) da v409 e' um passo SIMPLES v408 -> v409 (a Bancada de producao ja' pinava a v408)" % S,
                   f"o kernel da v409 difere do da v408 pelo(s) {DL_.N_BUNDLE} modulo(s) novo(s) (recibo do kernel KERNEL_RECIBO_v409; DIFF_KERNEL_v409.txt: o modulo novo e TGLExt.lean com o import a mais); o recibo pre_selo foi gerado e pinado ANTES da instalacao, em ensaio contra a producao (nada gravado; a Bancada pinava {bank['deployment_id']}), "
                   f"e a cadeia confere os pinos de PINOS_BN_v409.json na hora; o veredito esperado do aplicar e' REPINADA_B{bank['proxima']}__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_ e sem cadeia de selos, lido do codigo do esboco R3.5. Parada e religamento do servico exigem V409_AUTORIZACAO_OPERADOR (texto sem o nome do script do servico).",
                   "depois do aplicar, a Bancada pina a v409.", refs=None,
                   artefatos=[os.path.join(PK, "PINOS_BN_v409.json"), os.path.join(PK, "PINO_RECIBO_PRE_SELO_v409.json"), KR]))
    T9.append(anot(R_QUADRO, "v409 SELADA %s: o quadro do topo (O Teste da Única Palavra) segue intocado e o registro teste_de_veracidade_fase9_v397 segue selado" % S,
                   f"teste_de_veracidade_fase9_v397 selou={c_q} no rito da v409 (veredito igual ao de ESPERADOS; {tv_v['n_checks']} checagens): o quadro do artigo PT/EN e do .md, conferido contra o resultado pinado, segue no topo, com os numeros e a regra da ordem de sempre: {z444}. "
                   "Nenhum sigma, p ou lnB novo e' calculado nesta rota; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma) vale em todo texto que o cite; o paragrafo do quadro segue no README/site e o handoff da v409 traz tambem o paragrafo novo (a traducao as classes de Turing), sem o 4,44.",
                   "o paragrafo do README/site e' ato da sessao de custodia; a creditacao segue sendo beta_TGL na natureza a 5 sigma (nao ha o que repetir deste pacote, a abertura esta consumida).", refs=None))
    T9.append(errata(R_V408, sq_v408,
                     f"[E26 · ERRATA AO LADO, gerencia c1, em nome proprio, 05/11/2026, v409 {S}] Corrige, ao lado do registro seq {sq_v408} desta rota (a v408 selada), o trecho que dava a traducao as classes das maquinas de Turing como [OPEN]: era verdade na data; a v409 a fecha relativa ao leitor, e a maquina sem leitor fica fora. {corpo('E26')}. O registro corrigido NAO foi apagado nem reescrito: a correcao vai ao lado.",
                     refs=[R_DIC, R8]))
    for x in T9:
        assert x["rota_id"] in ids, "a rota %s nao existe no mapa" % x["rota_id"]
    resumo_conf = ("conferidor %s e %s" % (conf_dm, conf_np)) if "nao lido" not in (conf_dm, conf_np) else "conferidor: o resultado nao veio na leitura desta rodada"
    _vr409 = lambda v_: v_ if len(v_) <= 200 else v_[:197] + "..."   # o campo resultado do Mapa tem teto de 6000 caracteres (rotas._valida: resuma e aponte o artefato): a integra de cada veredito esta no core da rodada e nos ESPERADOS
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
            "titulo": "v409 SELADA %s: a traducao as classes de Turing — %d modulos de kernel (%s; o nome TraducaoTuring e os nomes das declaracoes das rodadas R1 a R8, dados pela gerencia c1, foram RATIFICADOS pelo operador em 05/11/2026 («concordo com todos os nomes que foram dados»); os nomes acrescentados na R9 (a inscricao no psion e a formula SAT) e os da ParNaFaceDeFock, tambem da gerencia, foram RATIFICADOS por ele em 05/11/2026 («Ratifico os nomes», D62)), o registro traducao_turing_v409, cunhagens_v409 e kh_n1_cobertura_v409, %d inscricoes de 05/11 por sha256; escada %s -> %s; %s; nenhuma chave antiga muda; validade no kernel nao e' creditacao; o gate nao se move" % (
                S, DL_.N_BUNDLE, P0["name"], len(verb), esc0, esc1, ALC),
            "pergunta": "o candidato v409 selou com o modulo de kernel, o registro com FUNCAO traducao_turing_v409 (que le do kernel do proprio rito as %d ancoras, o modulo por sha256, as respostas do operador de 05/11 pelos teoremas da pedra, o que fica False por teorema, o pino do acervo da v407 na copia purgada, a instancia de brinquedo fixa no codigo, a escada exata e o gate congelado; nenhuma chave antiga muda) e os dois por spec (as falas do operador de 05/11 por sha256, as decisoes D55 a D60, as erratas E24 a E26, a cobertura KH-N1), "
                        "com os registros da v408 (tetelestai_terminal_v408; cunhagens_v408 com a E26 ao lado; kh_n1_cobertura_v408 com pisos), os da v407 (psion_canto_v407 com as cinco chaves iguais; cunhagens_v407 com a errata da D57(d) ao lado), os da v406, da v405, da v404, da v403, da v402, da v401 e da v399, o selo pela propria tecnologia e o quadro do topo seguindo selados, o sidecar reescrito, a letra do veredito do gate igual a da v408 e nenhum veredito fora da troca dita mudado?" % len(DL_.ANCORAS),
            "dados": ["o modulo (a pedra em pedra\\ e insumos\\, com a candidata R8 de origem e o recibo de compilacao; o bundle pinado em BUNDLE_v409.json), pinado por sha256 (so' lido), e a medida da cobertura (KH_N1_v409.json)",
                      "as %d falas de 05/11 por sha256 em insumos\\cunhagens (todas falas do operador; de %d delas so' o trecho (duas pela D59; uma, a ratificacao da D61, pelo aviso operacional); a lista esta no registro cunhagens_v409 e na linhagem)" % (len(verb), n_trecho),
                      "o kernel do rito (as ancoras, as bandeiras e a proveniencia), a copia purgada do levantamento do acervo (a mesma da v408), o proprio um.py, o core e o selo da rodada; nenhum dado novo foi aberto nesta rota; o desenho e o recibo dos nomes ficam citados so' por sha16 (D59)"],
            "metodo": "lake build + Audit no sandbox k409c (o modulo do bundle sobre o kernel da v408 selada); ensaio a seco do candidato; rito completo; conferidor (deve mudar / nao pode mudar, com o quadro do topo conferido de novo contra o resultado pinado nas duas linguas e no .md, e os itens do selo mais o round trip do um.py instalado); "
                      "leitura da rodada (inclui o sidecar e a linha final do rito); superficies com a regra da linhagem completa (o MEMORY.md nao e' compactado: recusa por contagem); elo B(n) da Bancada (passo simples v408 -> v409, sem salto; recibos); a guarda das frases e a P18 em todo texto novo; o paragrafo novo e o do quadro, a nota ao lado do paragrafo da v408 e o sidecar, no handoff; os sete textos da custodia encadeados (D52) e o portao do G1 sobre o handoff inteiro (S6d)",
            "resultado": " | ".join(_vr409(v_) for v_ in [pc["verdict"], cg["verdict"], kh["verdict"]]) + " | (vereditos resumidos a 200 caracteres; a integra esta no core da rodada, um_absoluto.json) | sidecar %s (%s objetos, %s recusas) | %s | %s | escada %s -> %s (teoremas limpos %s/%s; %d bandeiras novas, todas da traducao; ancoras por modulo: %s)" % (
                sc["veredito"], sc["n_objetos"], sc["recusas"], resumo_conf, ("%s vereditos fora da troca dita mudaram (exigido 0)" % nvm) if nvm != "nao lido" else "vereditos fora da troca dita: nao lidos nesta leitura", esc0, esc1, ESP["escada"][0], ESP["escada"][1], NF, por_mod),
            "defeito": "as ressalvas, ditas: " + ress + "; o registro CONFERE o que o kernel prova e nao prova nada por si; o gate nao se moveu e a independencia das 4 bandeiras experimentais segue aberta (derivam de UM so' booleano) [DECLARADO, GV-01 e GV-03]; a pendencia [LEGAL] (D2) segue do operador; a revisao distinta do pacote e' o Sonnet (D58) e nao e' afirmada por este registro",
            "nao_refazer": "a integracao do modulo e a escada %s -> %s estao medidas; as %d ancoras no kernel do rito estao lidas e conferidas contra o um.py instalado; repetir os registros so' com kernel ou um.py novo; a traducao as classes de Turing esta' fechada relativa ao leitor (D56): a pergunta da maquina sem leitor fica fora e nao e' caminho a reabrir sem termo novo" % (esc0, esc1, len(DL_.ANCORAS)),
            "proximo_passo": "a igualdade completa com o leitor que so' conta (E28) e a independencia da pergunta da maquina sem leitor, [OPEN]; o README pinado (D39) e o release do app, na custodia e na engenharia da casa (D57a); decisao [LEGAL] D2 com a agente de PI; custodia completa pela sessao de custodia (o handoff traz os paragrafos prontos do README e do site, a nota ao lado do paragrafo da v408, os sete textos da custodia e lista o sidecar); revisao independente do pacote (o Sonnet, D58)",
            "onde": PK, "artefatos": arts, "refs": sorted((set(x["rota_id"] for x in T9) | set(REFS) | set(preparo_no_livro(ids))) - {NOVA}),
            "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move; as erratas E24 a E28 e a E21 ao lado e as decisoes D55 a D60 sao da gerencia c1, em nome proprio (a D61, ratificada pelo operador; a D62, a ratificacao dos nomes), ao lado (nada foi apagado nem reescrito); %s." % sim(c_seguem, "os registros anteriores seguem selados", "ALGUM REGISTRO ANTERIOR NAO SELOU")}
    for r in ROTA["refs"]:
        assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
    REG = [ROTA] + T9
    for x in REG:
        for k_, v_ in x.items():
            if isinstance(v_, str):
                assert len(v_) <= 6000, "o campo %s de %s passa de 6000 caracteres (limite do Mapa): resuma e aponte o artefato" % (k_, x["rota_id"])
    bad = [(x["rota_id"], violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad, "a guarda de texto (P18) achou violacao(oes): %r" % bad
    import guarda_frases_v409 as GF
    bad2 = [(x["rota_id"], GF.violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if GF.violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad2, "a guarda das frases achou violacao(oes): %r" % bad2
    atrib = [(x["rota_id"], T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))]
    assert not atrib, "a direcao do testemunho esta invertida ou a atribuicao falhou: %r" % atrib
    d59 = [x["rota_id"] for x in REG if re.search(r"(?i)kimi|mil[eê]nio|millennium|navier|lindão", json.dumps(x, ensure_ascii=False))]
    assert not d59, "D59: o registro traz o que fica fora dos textos: %r" % d59
    ruins = regra_4_44(REG, z, p)
    assert not ruins, "a regra do 4,44 (o p calibrado e a linha dos 5 sigma no mesmo campo) falhou em: %r" % ruins[:3]
    assert c_seguem and c_q, "algum registro anterior (quadro, v408, v407, v406, v405, v404, v403, falsidade, ponte, queda, esperanca, selo, declaracao, sonico, afinacao, rede de Fock, psibit, testemunha estatica) nao selou no core: o mapa nao registra a v409 assim"
    return REG


def gravar(p, b):
    """backup de BYTES se existir e mudar; temporario -> conferir tamanho -> substituir."""
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m409"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_m409"; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def main():
    V, PROB = L.ler()
    if PROB:
        print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); return 2
    NOS = L.NOS
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v409_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v409_*.json")), key=os.path.getmtime)
    arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto_selo_acom.json"), os.path.join(PK, "ESPERADOS_v409.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v409.json"),
            os.path.join(PK, "DIFF_KERNEL_v409.txt"), os.path.join(PK, "DIFF_v408_v409.diff"), os.path.join(NOS, "HANDOFF_v409_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v409.json"),
            os.path.join(PK, "kernel", "KERNEL_RECIBO_v409.json")] + sorted(glob.glob(os.path.join(PK, "pedra", "*.lean"))) + b3[-1:]
    arts = [x for x in arts if os.path.exists(x)]
    REG = montar(V, core, selo, ids_do_livro(), arts)
    J = os.path.join(HERE, "registro_mapa_v409.json")
    gravar(J, json.dumps(REG, ensure_ascii=False, indent=1).encode("utf-8"))
    quem = "claude-c1 (gerência), cadeia v409"
    print("registro MONTADO (NAO registrado): %d registro(s) (%s) -> %s" % (len(REG), ", ".join(x["tipo"] for x in REG), J))
    print("COMANDO (o passo 12 da cadeia o executa, uma vez so): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
    print("DEPOIS DO REGISTRO: os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
