# -*- coding: utf-8 -*-
# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork B)] REESCRITO sobre a subida mecanica da v407 FINAL (_bump_copia_v408.py deixara o corpo do psion): o conteudo e' o da v408 (TETELESTAI E' O TERMINAL: os modulos TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP de TGLExt/, com os nomes do operador; o registro com funcao tetelestai_terminal_v408; cunhagens_v408 e kh_n1_cobertura_v408; NENHUMA chave antiga muda; as erratas E21 a E23 ao lado). Os ids das rotas foram CONFERIDOS contra o livro do mapa (so' leitura) em 04/11/2026 (os que o bump herdou da v407 e nao existem foram retirados). A gerencia revisa antes do rito (nao e' versao selada). NAO registrou nada.
"""registrar_mapa_v408.py -- MONTA (nao registra) o registro da v408 no mapa de rotas e imprime o comando (molde: registrar_mapa_v407.py, que rodou na v407). Rodar DEPOIS do fechar (handoff gravado).
A v408 traz UMA rota nova, umpy.v408.selada_tetelestai_e_o_terminal_04nov (o conteudo e' o do selo): os modulos de kernel do bundle (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP, nomes dados pelo operador em 04/11; «P=nP» no sentido que ele deu e, pela correcao dele, P = nP teorema nas classes de computacao do dicionario do operador, com a traducao a Turing [OPEN]),
UM registro com FUNCAO (tetelestai_terminal_v408: le do kernel do proprio rito as ancoras dos quatro modulos, os modulos por sha256, as respostas do operador de 04/11 pelos teoremas, o que fica False por teorema, o insumo purgado, a escada exata e o gate congelado; nenhuma chave antiga muda) e os DOIS por spec (cunhagens_v408 e kh_n1_cobertura_v408),
mais ANOTACOES nas rotas que esperavam por ela (as candidatas de 04/11: o terminal, o tempo como moeda, o ponto de contradicao, o dicionario superado pelo PIgualNP, a afericao do traco; a v407 que a precede e o levantamento do acervo; o programa do fechamento, o inventario das chaves, o gate, o B(n) da Bancada e o quadro do Teste da Unica Palavra)
e TRES ERRATAS ao lado, em nome proprio da gerencia c1, com o seq do registro corrigido lido do livro (E21: o registro da v407 dizia que o [OPEN] do par na face de Fock era ausencia de termo; e' de LIGACAO. E22: duas frases da propria gerencia, podadas pelos teoremas da casa. E23: o insumo do acervo entra pela copia PURGADA; a integra fica fora do espelho).
Cada afirmacao e' testada contra o core/selo/ESPERADOS lidos por script (o registro existe? selou? o que NAO fechou fica dito); nenhum numero e' digitado (as contagens saem do core, de ESPERADOS e de delta_v408; os seq saem do livro).
REGRA DA ORDEM DO OPERADOR (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no MESMO campo; montar() RECUSA (assert) se algum campo do registro trouxer o 4,44 sem eles. Nao ha inscricao da gerencia nesta versao: todas as falas sao do operador (duas de autor misto: so' o paragrafo dele e' citavel); as erratas e as decisoes sao da gerencia, em nome proprio.
Fail-closed: o selo tem de ser a v408; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir. A rota de preparo da gerencia (registro_mapa_v408_prep.json, se existir) entra nas refs so' se ja' estiver no livro.
SAIDA: pos_rito\\registro_mapa_v408.json e o comando `rotas.py registrar` (quem o executa e' o passo 12 da cadeia, uma vez so', com marcador idempotente; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real. montar() le o core, o selo e ESPERADOS_v408.json; de V so' usa o que a leitura da rodada ja' validou (s16, sidecar, conferidor), sempre com valor de reserva dito."""
import glob, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v408 as L
import textos_v408 as T
import delta_v408 as DL
import quadro_v397 as Q
from guarda_p18_v408 import violacoes
_aspas_ = lambda s_: "\u00ab" + s_ + "\u00bb"   # (r2) a fala do operador entre aspas angulares, escrita por funcao: o texto citado e' a constante verbatim do delta (a varredura de citacoes le o codigo)
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V408"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v408 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOVA = "umpy.v408.selada_tetelestai_e_o_terminal_04nov"
R_TT = "kernel.tetelestai_e_o_terminal_provar_ou_podar_04nov"                  # a candidata TetelestaiTerminalR1/R2 (agora TetelestaiTerminal, nome do operador); a E22 vai ao lado
R_TM = "kernel.o_tempo_e_a_moeda_de_beta_candidata_04nov"                       # a candidata TempoMoedaR1 (agora TempoIgualMoeda)
R_PC = "kernel.ponto_de_contradicao_candidata_04nov"                            # a candidata PontoDeContradicaoR1 (agora PontoDeContradicao)
R_DIC = "kernel.dicionario_problema_entrada_passo_polinomio_implicacao_04nov"   # o dicionario da manha (DicionarioR1), SUPERADO pelo PIgualNP da tarde (D48)
R_FOCK = "kernel.face_de_fock_e_o_traco_do_psion_afericao_04nov"                # a afericao do traco no kernel (a cunhagem de 04/11 da face de Fock)
R_V407 = "umpy.v407.selada_o_psion_o_canto_e_o_par_03nov"                       # a v407 selada (a base da v408); a E21 vai ao lado
R_ACERVO = "kernel.psion_lema_acervo_03nov"                                     # o levantamento do psion no acervo (a integra fora do espelho; a E23 vai ao lado)
R_PSION = "kernel.psion_canto_r1_03nov"                                         # PsionCanto (v407)
R_PAR = "kernel.o_par_de_psions_r1_03nov"                                       # Par (v407)
R_PREP407 = "kernel.v407_preparacao_03nov"                                      # a preparacao da v407
R_PROG = "kernel.fechamento_construir_tudo_programa_02nov"                      # o programa do fechamento (ordem do operador de 02/11: construir tudo)
R_INV = "kernel.inventario_chaves_de_testemunha_v405_02nov"                     # o inventario das chaves de testemunha
R_TESTE_D = "ringdown.ramo_b_preregistro_v386"                                  # o ramo B do ringdown (o teste (d) so' por citacao, desde a v407)
R_MOTOR = "kernel.motor_continuo_pilar_levantamento_03nov"                      # o motor continuo no pilar quantico (fica fora)
R_V395 = "umpy.v395.psibit_na_fractalizacao_do_um"
R_V396 = "umpy.v396.testemunha_estatica_na_fractalizacao_do_um"
R_V406 = "umpy.v406.selada_o_fechamento_02nov"
R_GATE = "gate.qg_closure"
R_BANC = "infra.bancada_um.sincronizacao_vnnn"
R_QUADRO = "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9"
ANOTADAS = (R_TT, R_TM, R_PC, R_DIC, R_FOCK, R_V407, R_ACERVO, R_PROG, R_INV, R_GATE, R_BANC, R_QUADRO)
REFS = ("custodia.v407", "infra.custodia_g1.licoes_v405", "umpy.v400.correcao_da_v399_alfa_unico_e_beta_contra_o_core", "gate.maquina_do_veredito_final", "natureza.cinco_sigma_02_kimi_01nov", R_V395, R_V396, R_V406, R_PSION, R_PAR, R_PREP407, R_TESTE_D, R_MOTOR,
        "qg.graviton.desenho_do_operador_24out", "kernel.graviton_nao_particula")
PREP = os.path.join(PK, "registro_mapa_v408_prep.json")     # a rota de preparo da gerencia: lida em tempo de execucao; entra nas refs so' se a ROTA dele ja' estiver no livro
_CACHE = {}


def _esp():
    """ESPERADOS_v408.json (lido uma vez por processo)."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v408.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _base_core():
    """O core da v407 selada (a copia de bytes em base_v407): de onde sai a medida de que o gate nao se moveu."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v407", "um_absoluto.json"), encoding="utf-8"))["core"]
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
    """As rotas ROTA de registro_mapa_v408_prep.json (se o arquivo existir e ler) que ja' estao no livro e nao sao a nova: entram nas refs. Ausente ou ilegivel = nenhuma (dito, nunca falha)."""
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
    p = json.load(open(os.path.join(PK, "PINOS_BN_v408.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v407" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v407 -> v408 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1, "deployment_id": bp["deployment_id"]}


def montar(V, core, selo, ids, arts):
    """Monta os registros (a ROTA nova, as ANOTACOES e as ERRATAS), cada afirmacao testada contra o core/selo/ESPERADOS; devolve a lista; recusa (assert) se algo nao conferir. Nao escreve nada."""
    assert selo.get("um_version") == "v408", "o selo nao e a v408"
    assert NOVA not in ids, "a rota %s ja existe no mapa" % NOVA
    for r in ANOTADAS + REFS:
        assert r in ids, "a rota %s nao existe no mapa (anotada ou citada em refs)" % r
    ESP = _esp(); DL_ = DL
    S = ESP["candidato_sha16"]
    assert str((selo.get("sha256") or {}).get("um.py", ""))[:16] == S, "o um.py do selo nao e o candidato de ESPERADOS"
    assert V.get("s16") in (None, S), "o s16 da leitura != o candidato de ESPERADOS"
    BASE = ESP["origem_sha16"]
    esc0, esc1 = ESP["escada_v407_e_v408"]
    NF = ESP["n_bandeiras_novas"]
    assert esc1 - esc0 == NF == sum(ESP["n_bandeiras_por_grupo"].values()) == len(ESP["bandeiras_novas_chaves"]) == ESP["politica_de_bandeiras"]["n_flags"], "a escada nao fecha com as bandeiras novas"
    assert ESP["kernel"]["modulos_novos"] == DL_.N_BUNDLE == len(DL_.BUNDLE_RELS) == len(DL_.PEDRAS_V408), "o delta do kernel nao e o bundle"
    assert list(ESP["chaves_v408"]) == [] and list(DL_.CHAVES_V408) == [], "a v408 nao muda chave antiga nenhuma: ESPERADOS/delta dizem outra coisa"
    BETA = ESP["beta"] if isinstance(ESP.get("beta"), float) else None
    FRASE = DL_.FRASE_DA_MOLDURA_V408_PT

    # --- o quadro do topo (a regra do 4,44): o registro selado, lido pelas MESMAS funcoes do artigo
    tvr = core.get("teste_de_veracidade_fase9_v397") or {}
    a = T._qd().Q._v397_atomos(tvr, "pt"); assert a["sealed"] is True, "o registro teste_de_veracidade_fase9_v397 nao sela no core: o mapa nao registra o 4,44 assim"
    z, p = a["z_disc"]["md"], a["p_disc"]["md"]
    z444 = "z_disc = %s (calibrado; p unilateral %s), abaixo do degrau de 5σ da creditação, que não foi alcançado (%s < 5)" % (z, p, z)

    def selou(k):
        return (core.get(k) or {}).get("all_verified") is True

    # --- o registro com FUNCAO tetelestai_terminal_v408: tudo lido do core e conferido contra ESPERADOS e delta_v408
    pc = core.get(DL_.FECHO_REGISTRO) or {}; pv = pc.get("values") or {}; mech = pc.get("mechanics") or {}
    assert pc.get("all_verified") is True and pc.get("verdict") == ESP["vereditos_novos_v408"][DL_.FECHO_REGISTRO] and pc.get("does_not_gate_core") is True, "tetelestai_terminal_v408 nao selou ou != ESPERADOS"
    assert mech.get("passed") is True and mech.get("n_checks") == DL_.N_CHECKS_FECHO == len(mech.get("checks") or []) and all(c.get("ok") is True for c in mech["checks"]), "as checagens do tetelestai_terminal_v408 nao passaram"
    assert pv.get("n_ancoras_ok") == pv.get("n_ancoras") == len(DL_.ANCORAS) and pv.get("n_modulos_ok") == pv.get("n_modulos") == DL_.N_BUNDLE and pv.get("n_flags_true") == pv.get("n_flags") == NF and pv.get("escada") == [esc1] * 3, "os valores do tetelestai_terminal_v408 != ESPERADOS/delta"
    assert pc.get("beta_ok") is True and pc.get("embedded_sources_ok") is True and pc.get("embedded_sources_n_ok") == DL_.N_BUNDLE and pc.get("guarda_violacoes") in ([], None), "o beta, as fontes embutidas ou a guarda do tetelestai_terminal_v408 nao conferem"
    assert list(pc.get("chaves_antigas_que_mudam") or []) == [] and pc.get("nome_provisorio") is None, "o registro do terminal diz que uma chave antiga mudou ou traz nome provisorio: a v408 nao faz nem um nem outro"
    assert list(pc.get("ressalvas") or []) == list(DL_.RESSALVAS_V408), "as ressalvas do registro != delta_v408.RESSALVAS_V408"
    assert set(pv.get("respostas") or {}) == {r_["id"] for r_ in DL_.RESPOSTAS_DO_OPERADOR} and all(v_ is True for v_ in pv["respostas"].values()) and pv.get("respostas_ok") is True, "as respostas do operador de 04/11 nao conferem todas no kernel"
    assert (pv.get("insumo_purgado") or {}).get("ok") is True and (pv.get("insumo_purgado") or {}).get("integra_nao_pinada") is True, "o insumo purgado do acervo nao confere por sha256 ou a integra foi pinada (E23)"
    assert list(pc.get("fica_false_por_teorema") or []) == list(ESP["fica_false_por_teorema"]) and set(pc.get("fica_aberto") or {}) == set(ESP["fica_aberto"]), "o que fica False por teorema ou o que fica aberto != ESPERADOS"
    assert list(pc.get("ancoras_principais") or []) == list(DL_.ANCORAS_PRINCIPAIS) and all(((pv.get("ancoras") or {}).get(n_) or {}).get("ok") is True for n_ in DL_.ANCORAS_PRINCIPAIS), "as quatro ancoras principais nao estao todas ok no kernel do rito"
    assert pv.get("gate_verdict") == ESP["qg_closure_gate_verdict_v407"], "o veredito do gate lido pelo registro do terminal != o da v407 (o gate deveria estar congelado)"
    assert pc.get("podado") and pc.get("regra_provar_ou_podar"), "o registro nao traz o que foi podado nem a regra provar ou podar (D49)"
    BETA_RT = pv.get("beta"); assert isinstance(BETA_RT, float) and (BETA is None or abs(BETA_RT - BETA) <= 1e-9 * BETA), "o beta do registro != o do core/ESPERADOS (tolerancia relativa 1e-9)"
    por_mod = "; ".join("%s (%d)" % (rel.split("/")[-1][:-5], len(ns)) for rel, ns in DL_.ANCORAS_POR_MODULO.items())
    ress = " | ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(pc["ressalvas"]))
    # --- o registro HERDADO psion_canto_v407: segue selado, com as cinco chaves iguais as da v407 selada (nenhuma muda)
    pc7 = core.get(DL_.D7.FECHO_REGISTRO) or {}; pv7 = pc7.get("values") or {}
    assert pc7.get("all_verified") is True and pc7.get("verdict") == ESP["registros_funcao_v407"]["psion_canto"]["verdict"] and pc7.get("keys") == ESP["chaves_v407_esperadas"], "psion_canto_v407 (herdado) nao segue selado ou as chaves mudaram"
    assert pv7.get("n_modulos_ok") == pv7.get("n_modulos") == DL_.D7.N_BUNDLE and pv7.get("n_ancoras_ok") == pv7.get("n_ancoras") == len(DL_.D7.ANCORAS), "os valores do psion_canto_v407 (herdado) != delta_v407"
    fk7 = pc7["keys"]
    # --- o registro HERDADO fechamento_v406: segue selado, com a chave do lema lida (a c8 versionada, E20)
    fh = core.get(DL_.D6.FECHO_REGISTRO) or {}
    assert fh.get("all_verified") is True and fh.get("verdict") == ESP["registros_funcao_v406"]["fechamento"]["verdict"] and (fh.get("four_keys") or {}).get("testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma") is True, "fechamento_v406 (herdado) nao segue selado ou nao le a chave do lema"
    # --- a E21 ao lado do spec herdado cunhagens_v407 (recriado)
    cg7 = core.get(DL_.D7.CUNHAGENS_REGISTRO) or {}
    assert cg7.get("all_verified") is True and any("E21" in json.dumps(e_, ensure_ascii=False) for e_ in (cg7.get("erratas") or [])), "cunhagens_v407 (herdado) nao segue selado ou nao traz a E21 ao lado"
    # --- o gate NAO se moveu: o registro segue selado e a letra do veredito e' a da v407
    gk = core.get("bandeiras_do_gate_v403") or {}; gvv = gk.get("values") or {}; gb = _base_core().get("bandeiras_do_gate_v403") or {}
    assert gk.get("all_verified") is True and (V.get("gate") or {}).get("sealed", True) is True and gvv == gb.get("values") and (gk.get("mechanics") or {}).get("passed") is True, "bandeiras_do_gate_v403 (recriado) nao selou ou != a v407 selada"
    qg = core.get("qg_closure") or {}; fam = [len(qg.get(f) or {}) for f in ("formal_flags", "physics_flags", "experiment_flags")]
    assert (qg.get("gate") or {}).get("verdict") == ESP["qg_closure_gate_verdict_v407"] == selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"], "a letra do veredito do gate mudou"
    # --- os dois registros por spec
    cg = core.get(DL_.CUNHAGENS_REGISTRO) or {}; kh = core.get(DL_.KH_REGISTRO) or {}
    for nome_, r_ in ((DL_.CUNHAGENS_REGISTRO, cg), (DL_.KH_REGISTRO, kh)):
        assert r_.get("all_verified") is True and r_.get("verdict") == ESP["vereditos_novos_v408"][nome_], "%s nao selou ou != ESPERADOS" % nome_
    verb = cg.get("verbatim") or {}; ex = cg.get("extras") or {}
    assert len(verb) == len(ESP["cunhagens"]) == len(DL_.VERBATIM_ORIGEM_V408) and set(verb) == set(ESP["cunhagens"]) and all(v.get("embedded_ok") is True for v in verb.values()), "as inscricoes de 04/11 nao estao embutidas por sha256"
    assert all(str((ESP["cunhagens"][k_] or {}).get("nome", "")).startswith("OPERADOR_04nov_") for k_ in ESP["cunhagens"]), "alguma inscricao nao e' fala do operador de 04/11"
    # (r2, 04/11 noite: o registro cunhagens_v408 traz as erratas E21 a E23 E, por ultimo, a errata ao lado dos pisos de kh_n1_cobertura_v407 (como a leitura confere: len == len(ERRATAS_V408) + 1); a da v407 trazia so' as suas tres)
    erratas_todas = cg.get("erratas") or []; erratas = erratas_todas[:len(DL_.ERRATAS_V408)]
    assert [e.get("agora") for e in erratas] == list(DL_.ERRATAS_V408) and len(erratas_todas) == len(DL_.ERRATAS_V408) + 1 and "kh_n1_cobertura_v407" in str(erratas_todas[-1].get("ao_lado_de")) and all(str(e.get("assinatura", "")).startswith("gerencia c1") and "em nome proprio" in e["assinatura"] for e in erratas_todas), "as erratas E21 a E23 (e a errata ao lado dos pisos de kh_n1_cobertura_v407) nao estao no registro ou nao sao da gerencia c1 em nome proprio"
    dec = ex.get("decisoes") or {}; assert sorted(dec) == list(ESP["decisoes_v408_ids"]) and all(("D%d" % i) in dec for i in range(48, 55)), "faltam decisoes D48 a D54 no registro"
    assert ex.get("leituras") == DL_.LEITURA_V408, "a leitura da v408 no registro != delta_v408"
    cob = kh.get("lido") or {}; assert cob.get("constantes_cobertas") and cob.get("teoremas_cobertos"), "kh_n1_cobertura_v408 sem a cobertura"
    seguem = (DL_.D7.FECHO_REGISTRO, DL_.D7.CUNHAGENS_REGISTRO, DL_.D7.KH_REGISTRO, "fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406", "ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405", "cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405",
              "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "falsidade_da_inercia_v401", "cunhagens_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402",
              "teste_de_veracidade_fase9_v397", "cunhagens_v397", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "sonico_v398", "afinacao_das_cordas_v398", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396")
    c_seguem = all(selou(k) for k in seguem)
    tv_v = ESP["veracidade"]; c_q = bool(selou("teste_de_veracidade_fase9_v397") and selou("cunhagens_v397") and tvr.get("verdict") == tv_v["verdict"])
    sc = _sidecar(V); conf_dm = V.get("conf_dm", "nao lido"); conf_np = V.get("conf_np", "nao lido"); nvm = V.get("n_ver_mudaram", "nao lido")
    bank = _bancada(); regs = livro()
    # --- o seq que cada errata corrige, lido do livro (e o registro tem de trazer o trecho corrigido)
    sq_v407 = seq_do_alvo(regs, R_V407, "ROTA", contem=("operadores de criacao como termo",))
    sq_tt = seq_do_alvo(regs, R_TT, "ROTA", contem=("TetelestaiTerminalR1",))
    sq_acervo = seq_do_alvo(regs, R_ACERVO, "ROTA", contem=("PSION_NO_ACERVO",))
    KR = os.path.join(PK, "kernel", "KERNEL_RECIBO_v408.json")
    E = {}
    for e in erratas:
        m_ = re.match(r"^(E\d\d) -- ", e.get("agora", "")); assert m_, "uma errata do registro nao comeca por E<n> --"
        E[m_.group(1)] = e
    assert sorted(E) == ["E21", "E22", "E23"], "as erratas do registro nao sao E21 a E23"

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

    ped = {p_["name"]: os.path.join(PK, "pedra", p_["name"] + ".lean") for p_ in DL_.PEDRAS_V408}
    sha_ped = {p_["name"]: DL_.BUNDLE_POR_REL[p_["rel"]]["sha256"][:16] for p_ in DL_.PEDRAS_V408}
    n_anc = {p_["name"]: len(DL_.ANCORAS_POR_MODULO[p_["rel"]]) for p_ in DL_.PEDRAS_V408}
    resp = {r_["id"]: r_["diz"] for r_ in DL_.RESPOSTAS_DO_OPERADOR}
    T9 = []
    T9.append(anot(R_TT, "v408 SELADA %s: a candidata do terminal entrou no kernel do rito como TGLExt/TetelestaiTerminal (nome do operador); o terminal e' a leitura; a regra provar ou podar aplicada; a E22 fica ao lado" % S,
                   f"a pedra TetelestaiTerminal (nome do operador: {DL_.NOME_DO_OPERADOR['TetelestaiTerminal']}) esta no kernel do rito com o sha256 pinado ({sha_ped['TetelestaiTerminal']}), {n_anc['TetelestaiTerminal']} ancoras no trio; as respostas do operador de 04/11 conferem pelos teoremas: a_tgl_tem_terminal -> {resp['a_tgl_tem_terminal']}; "
                   f"o_zero_absoluto_e_do_infinito -> {resp['o_zero_absoluto_e_do_infinito']}; tamanho_do_nome_e_oitavas -> {resp['tamanho_do_nome_e_oitavas']}; relacao_sem_peso_e_a_origem_da_mentira -> {resp['relacao_sem_peso_e_a_origem_da_mentira']}; o_cociclo_e_inclinacao -> {resp['o_cociclo_e_inclinacao']}. "
                   f"A ordem do operador, verbatim: {_aspas_(DL_.FRASE_TERMINAL)}. A regra dele: {_aspas_(DL_.FRASE_PROVAR_OU_PODAR)}. {corpo('E22')}",
                   "o registro tetelestai_terminal_v408 le estas ancoras a cada rito; a palavra «impedância» segue podada como termo (D50); o conteudo tem o nome do operador «%s»." % DL_.FRASE_INCLINACAO_NOME, refs=[R_TM, R_PC], artefatos=[ped["TetelestaiTerminal"], DL_.RECIBO_TT_R2_ARQ, KR],
                   estatuto="REAL (os termos no kernel do rito); INPUT (as falas do operador de 04/11); ONTO (as leituras dele onde o kernel nao as prova); DECLARADO (os recibos de compilacao das candidatas)",
                   defeito="o registro CONFERE o que o kernel prova e nao prova nada por si; 'tempo linear nos andares' e' identidade de um fluxo para o Nome da torre, nao enunciado de complexidade; validade no kernel nao e' creditacao"))
    T9.append(anot(R_TM, "v408 SELADA %s: a candidata do tempo entrou no kernel do rito como TGLExt/TempoIgualMoeda (nome do operador: «%s»); o tempo e' a moeda de β; nao ha relacao sem peso" % (S, DL_.FRASE_NOME_TEMPO),
                   f"a pedra TempoIgualMoeda esta no kernel do rito com o sha256 pinado ({sha_ped['TempoIgualMoeda']}), {n_anc['TempoIgualMoeda']} ancoras no trio; a resposta do operador confere pelos teoremas: o_tempo_e_a_moeda_de_beta -> {resp['o_tempo_e_a_moeda_de_beta']}. A cunhagem dele, verbatim: {_aspas_(DL_.FRASE_TEMPO_MOEDA)}; e {_aspas_(DL_.FRASE_RELACAO_MENTIRA)} (o Atlas ja' dizia: representação sem custo = ORIGEM DA MENTIRA; a PODA = TETELESTAI).",
                   "beta entra so' por nome (TGLCoupling.beta no kernel; alfa CODATA 2018 x sqrt e em runtime), nunca literal.", refs=[R_TT], artefatos=[ped["TempoIgualMoeda"], DL_.RECIBO_TM_ARQ],
                   estatuto="REAL (os termos no kernel do rito); INPUT (a cunhagem do operador de 04/11); ONTO (a leitura dele do Verbo no gerundio)"))
    T9.append(anot(R_PC, "v408 SELADA %s: a candidata do ponto de contradicao entrou no kernel do rito como TGLExt/PontoDeContradicao (nome do operador: «%s»)" % (S, DL_.FRASE_NOME_PONTO),
                   f"a pedra PontoDeContradicao esta no kernel do rito com o sha256 pinado ({sha_ped['PontoDeContradicao']}), {n_anc['PontoDeContradicao']} ancoras no trio: 1 = 0 nas duas faces (exp 0 = Omega e Omega != 0), o boost antes e depois da inscricao, o habitante e' o Fock concreto (por rfl). A fala do operador, verbatim: {_aspas_(DL_.FRASE_PONTO)}.",
                   "o lock (1 - P) e o Hamiltoniano modular (K = -log Delta) sao objetos DISTINTOS que coincidem em ter Omega como modo zero; a identificacao dos dois fica podada (ressalva 4).", refs=[R_TT, R_FOCK], artefatos=[ped["PontoDeContradicao"], DL_.RECIBO_PC_ARQ],
                   estatuto="REAL (os termos no kernel do rito); INPUT (a fala do operador de 04/11); PODADO (a identificacao lock = Hamiltoniano modular)"))
    T9.append(anot(R_DIC, "v408 SELADA %s: o dicionario da manha ficou SUPERADO (D48); o quarto modulo e' TGLExt/PIgualNP, com o nome e o SENTIDO do operador («%s», no sentido dele); pela correcao dele (D51 revista), P = nP e' teorema nas classes de computacao do dicionario do operador, definidas em Lean (ClasseP, ClasseNP) e provadas em p_igual_np_nas_classes_do_dicionario; a traducao as classes das maquinas de Turing e' [OPEN], nao recusa" % (S, DL_.FRASE_NOME_PNP),
                   f"a pedra PIgualNP esta no kernel do rito com o sha256 pinado ({sha_ped['PIgualNP']}), {n_anc['PIgualNP']} ancoras no trio; a resposta do operador confere pelos teoremas: p_igual_np_no_sentido_dele -> {resp['p_igual_np_no_sentido_dele']}; p_igual_np_trata_das_classes_do_dicionario -> {resp['p_igual_np_trata_das_classes_do_dicionario']}. O sentido, verbatim: {_aspas_(DL_.FRASE_SENTIDO_PNP)}. O Dicionario.lean da manha nao entra (fica como registro em insumos).",
                   "a traducao das classes do dicionario as classes das maquinas de Turing (o tamanho em bits = log2 n, as oitavas; familias de instancias; passos de maquina) nao esta' no kernel: e' a proxima construcao, [OPEN], nao uma recusa (D51 revista).", refs=[R_TT], artefatos=[ped["PIgualNP"], DL_.RECIBO_DIC_ARQ, DL_.AFERICAO_ARQ],
                   estatuto="REAL (os termos no kernel do rito); INPUT (o nome e o sentido do operador); OPEN (a traducao das classes do dicionario as das maquinas de Turing; D51 revista)",
                   defeito="a Mathlib do sandbox tem TM2ComputableInPolyTime e nenhuma NP: a traducao das classes do dicionario a Turing e' construcao a fazer, dita [OPEN]"))
    T9.append(anot(R_FOCK, "v408 SELADA %s: a afericao do traco no kernel entrou como insumo pinado do registro; o par na face de Fock segue [OPEN] como LIGACAO (E21), nao como ausencia de termo" % S,
                   f"a afericao (AFERICAO_TRACO_E_DICIONARIO_NO_KERNEL_04nov.json) e' fonte pinada de cunhagens_v408 (selou={selou(DL_.CUNHAGENS_REGISTRO)}); o habitante do certificado fisico e' o Fock concreto por rfl (PontoDeContradicao.o_habitante_e_o_fock_concreto), que TEM criacao e aniquilacao; {corpo('E21')}",
                   "a fiacao do par na face de Fock e' trabalho da v409 (dito, nao prometido).", refs=[R_V407, R_PC], artefatos=[DL_.AFERICAO_ARQ],
                   estatuto="REAL (o habitante por rfl no kernel do rito); OPEN (a ligacao do par na face de Fock); ONTO (a cunhagem do operador: a face de Fock e' o traco do psion)"))
    T9.append(anot(R_V407, "v408 SELADA %s: a v407 e' a base selada da v408; o psion_canto_v407, os dois specs da v407 (cunhagens_v407 com a E21 ao lado; kh_n1_cobertura_v407 com pisos) e os registros anteriores sao recriados e seguem selados; nenhuma chave muda" % S,
                   f"a v408 parte da v407 selada (um.py {BASE}) e acrescenta {DL_.N_BUNDLE} modulos de kernel, UM registro com funcao (tetelestai_terminal_v408) e dois por spec, e a secao do artigo; psion_canto_v407 selou={selou(DL_.D7.FECHO_REGISTRO)} com as cinco chaves iguais as da v407 selada (linked_to_the_corner_by_a_lemma = {fk7['testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma']}, lida do kernel); "
                   f"fechamento_v406 selou={selou('fechamento_v406')}; cunhagens_v406 selou={selou('cunhagens_v406')}; os treze da v405 (ponte_da_massa_v405 selou={selou('ponte_da_massa_v405')}, identidade_v405 selou={selou('identidade_v405')}, gap_v405 selou={selou('gap_v405')}), os da v404, da v403, da v402, da v401 e da v399 seguem selados neste rito "
                   f"(caminho_v403 selou={selou('caminho_v403')}, falsidade_da_inercia_v401 selou={selou('falsidade_da_inercia_v401')}), como seguem o selo pela propria tecnologia e a declaracao do operador (v399), o sonico e a afinacao (v398) e o quadro (v397); sidecar um_absoluto_selo_acom.json {sc['veredito']} ({sc['n_objetos']} objetos, {sc['recusas']} recusas, sha16 {sc['sha16']}). "
                   f"O registro kh_n1_cobertura_v407 passa a cobrar piso (errata de contagem ao lado); a v407 e as pedras dela ficam como registro (seq {sq_v407}).",
                   "custodia conjunta pela sessao do site (o handoff lista o sidecar e traz a nota ao lado do paragrafo da v407).", refs=[R_PSION, R_PAR, R_PREP407]))
    T9.append(anot(R_ACERVO, "v408 SELADA %s: o insumo do acervo entra pela copia PURGADA; a integra fica fora do espelho (ordem do operador de 08/09) e e' citada so' por sha16 (E23)" % S,
                   f"o registro tetelestai_terminal_v408 confere a copia purgada por sha256 a cada rito (c15: insumo_purgado.ok={pv['insumo_purgado']['ok']}, integra_nao_pinada={pv['insumo_purgado']['integra_nao_pinada']}); {corpo('E23')}",
                   "a copia purgada passou pela guarda de material privado ANTES de ser pinada (licao 4 da v407, D52).", refs=[R_V407], artefatos=[DL_.PURGADO_ARQ, DL_.RECIBO_PURGA_ARQ],
                   estatuto="REAL (o sha256 da copia purgada, lido a cada rito); INPUT (a ordem do operador de 08/09); DECLARADO (o levantamento do acervo)"))
    T9.append(anot(R_PROG, "v408 SELADA %s: o programa do fechamento nao ganha chave nova nem perde nenhuma; o terminal (Tetelestai, a poda) e' lido do kernel; o par na face de Fock segue [OPEN] como ligacao" % S,
                   f"nenhuma chave antiga muda (chaves_antigas_que_mudam = {list(pc.get('chaves_antigas_que_mudam') or [])}); as cinco chaves do psion_canto_v407 seguem iguais as da v407 selada; ficam False por teorema: full_static_witness_exists = {fk7['qg_closure.gate.full_static_witness_exists']} e trivial_inhabitant_exists = {fk7['witness_rigidity.trivial_inhabitant_exists']}. {FRASE}",
                   "a ligacao do par na face de Fock (v409), a ponte Bell-TT, K(O) != bot para O compacto e o teste com a natureza seguem [OPEN]; o programa do fechamento nao e' fechado por esta anotacao.", refs=[R_INV, R_TT],
                   estatuto="REAL (a leitura do kernel do rito); OPEN (a ligacao do par na face de Fock; K(O) != bot para O compacto)"))
    T9.append(anot(R_INV, "v408 SELADA %s: o inventario das chaves de testemunha NAO muda nesta versao (CHAVES_V408 vazia): as cinco chaves do psion_canto_v407 seguem lidas do kernel" % S,
                   f"linked_to_the_corner_by_a_lemma = {fk7['testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma']}; rede_fock_v394.whole_certificate_inhabited = {fk7['rede_fock_v394.whole_certificate_inhabited']}; psibit_v395...inhabitant_exhibited = {fk7['psibit_v395.conditional_psion_face.inhabitant_exhibited']}; testemunha_estatica_v396...inhabitant_exhibited = {fk7['testemunha_estatica_v396.fock_face.inhabitant_exhibited']}; "
                   f"witness_layers.canonical_full_witness_term_constructed = {fk7['witness_layers.canonical_full_witness_term_constructed']}; ficam False por teorema: full_static_witness_exists e trivial_inhabitant_exists.",
                   "o par na face de Fock segue [OPEN] como ligacao (E21).", refs=[R_PROG], estatuto="REAL (a leitura do kernel do rito e o registro herdado); OPEN (a ligacao do par na face de Fock)"))
    T9.append(anot(R_GATE, "v408 SELADA %s: o gate NAO se moveu — o qg_closure do core e' identico ao da v407 (as 18 bandeiras calculadas, a letra do veredito) e o registro do terminal o confere congelado (c12)" % S,
                   f"o registro bandeiras_do_gate_v403 (recriado) selou={selou('bandeiras_do_gate_v403')} com os mesmos valores da v407 selada: das {gvv['n_flags']} bandeiras ({fam[0]} formais, {fam[1]} fisicas, {fam[2]} experimentais) {gvv['n_true']} sao True e {gvv['n_calculated']} sao CALCULADAS ({gvv['n_literal']} literais); o veredito le {gvv['n_read_by_the_verdict']}; a letra do veredito do gate e' a da v407 e a do selo; o tetelestai_terminal_v408 le gate_verdict identico ao da v407. "
                   "Nenhuma bandeira do gate depende dos modulos da v408; full_static_witness_exists e trivial_inhabitant_exists seguem False. [DECLARADO, GV-03 da auditoria de 28/09/2026] As 4 bandeiras experimentais derivam de UM so' booleano; o degrau experimental le so' o rito V11 do piso, unilateral (GV-01).",
                   "a independencia das 4 experimentais e os mocks de survey seguem [OPEN]; o gate nao se move por esta rota.", refs=None,
                   artefatos=[os.path.join(PK, "CANDIDATO_v408.json")], estatuto="REAL (o core do rito); DECLARADO (GV-01, GV-03, EV-12 da auditoria de 28/09/2026); OPEN (a independencia das 4 experimentais)",
                   defeito="o gate nao e' teste e nao discrimina o LCDM raso; NOT_FALSIFIED nunca e' a palavra da creditacao"))
    T9.append(anot(R_BANC, "v408 SELADA %s: o B(n) da v408 e' um passo SIMPLES v407 -> v408 (a Bancada de producao ja' pinava a v407)" % S,
                   f"o kernel da v408 difere do da v407 pelos {DL_.N_BUNDLE} modulos novos (recibo do kernel KERNEL_RECIBO_v408; DIFF_KERNEL_v408.txt: modulos novos e TGLExt.lean com os imports a mais); o recibo pre_selo foi gerado e pinado ANTES da instalacao, em ensaio contra a producao (nada gravado; a Bancada pinava {bank['deployment_id']}), "
                   f"e a cadeia confere os pinos de PINOS_BN_v408.json na hora; o veredito esperado do aplicar e' REPINADA_B{bank['proxima']}__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_ e sem cadeia de selos, lido do codigo do esboco R3.5. Parada e religamento do servico exigem V408_AUTORIZACAO_OPERADOR (texto sem o nome do script do servico).",
                   "depois do aplicar, a Bancada pina a v408.", refs=None,
                   artefatos=[os.path.join(PK, "PINOS_BN_v408.json"), os.path.join(PK, "PINO_RECIBO_PRE_SELO_v408.json"), KR]))
    T9.append(anot(R_QUADRO, "v408 SELADA %s: o quadro do topo (O Teste da Única Palavra) segue intocado e o registro teste_de_veracidade_fase9_v397 segue selado" % S,
                   f"teste_de_veracidade_fase9_v397 selou={c_q} no rito da v408 (veredito igual ao de ESPERADOS; {tv_v['n_checks']} checagens): o quadro do artigo PT/EN e do .md, conferido contra o resultado pinado, segue no topo, com os numeros e a regra da ordem de sempre: {z444}. "
                   "Nenhum sigma, p ou lnB novo e' calculado nesta rota; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma) vale em todo texto que o cite; o paragrafo do quadro segue no README/site e o handoff da v408 traz tambem o paragrafo novo (Tetelestai e' o terminal), sem o 4,44.",
                   "o paragrafo do README/site e' ato da sessao do site; a creditacao segue sendo beta_TGL na natureza a 5 sigma (nao ha o que repetir deste pacote, a abertura esta consumida).", refs=None))
    T9.append(errata(R_V407, sq_v407,
                     f"[E21 · ERRATA AO LADO, gerencia c1, em nome proprio, 04/11/2026, v408 {S}] Corrige o registro seq {sq_v407} desta rota (a v407 selada), que diz que o par na face de Fock segue [OPEN] porque o certificado de Fock nao tem operadores de criacao como termo; era o que o registro psion_canto_v407 dizia. Na v408: {corpo('E21')}. O registro corrigido NAO foi apagado nem reescrito: a correcao vai ao lado.",
                     refs=[R_FOCK, R_PC]))
    T9.append(errata(R_TT, sq_tt,
                     f"[E22 · ERRATA AO LADO, gerencia c1, em nome proprio, 04/11/2026, v408 {S}] Corrige, ao lado do registro seq {sq_tt} desta rota (a candidata R1 do terminal), duas frases da PROPRIA gerencia de 04/11: a que dava a TGL por sem terminal (dita na sessao, antes da correcao do operador: {_aspas_(DL_.FRASE_TERMINAL)}) e a da R1 sobre o resto sem traco (ja' corrigida pela R2 nesta rota; a R1 fica como registro). {corpo('E22')}. Nada foi apagado nem reescrito.",
                     refs=[R_TM]))
    T9.append(errata(R_ACERVO, sq_acervo,
                     f"[E23 · ERRATA AO LADO, gerencia c1, em nome proprio, 04/11/2026, v408 {S}] Corrige, ao lado do registro seq {sq_acervo} desta rota (o levantamento do acervo), o modo de pinar o insumo: a v407 pinou a integra (que ficou fora do espelho pela ordem do operador de 08/09); a v408 pina a copia PURGADA e cita a integra so' por sha16. {corpo('E23')}. Nada foi apagado nem reescrito.",
                     refs=[R_V407], artefatos=[DL_.PURGADO_ARQ, DL_.RECIBO_PURGA_ARQ]))
    for x in T9:
        assert x["rota_id"] in ids, "a rota %s nao existe no mapa" % x["rota_id"]
    resumo_conf = ("conferidor %s e %s" % (conf_dm, conf_np)) if "nao lido" not in (conf_dm, conf_np) else "conferidor: o resultado nao veio na leitura desta rodada"
    _vr408 = lambda v_: v_ if len(v_) <= 200 else v_[:197] + "..."   # o campo resultado do Mapa tem teto de 6000 caracteres (rotas._valida: resuma e aponte o artefato): a integra de cada veredito esta no core da rodada e nos ESPERADOS
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
            "titulo": "v408 SELADA %s: Tetelestai e' o terminal — %d modulos de kernel (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP, nomes do operador), o registro tetelestai_terminal_v408, cunhagens_v408 e kh_n1_cobertura_v408, %d inscricoes de 04/11 por sha256; escada %s -> %s; o terminal e' a leitura, nao o fim do decaimento; nao ha relacao sem peso; o tempo e' a moeda de β; nenhuma chave antiga muda; validade no kernel nao e' creditacao; o gate nao se move" % (
                S, DL_.N_BUNDLE, len(verb), esc0, esc1),
            "pergunta": "o candidato v408 selou com os %d modulos de kernel, o registro com FUNCAO tetelestai_terminal_v408 (que le do kernel do proprio rito as %d ancoras, os %d modulos por sha256, as respostas do operador de 04/11 pelos teoremas, o que fica False por teorema, o insumo purgado, a escada exata e o gate congelado; nenhuma chave antiga muda) e os dois por spec (as falas do operador de 04/11 por sha256, as decisoes D48 a D54, as erratas E21 a E23, a cobertura KH-N1), "
                        "com os registros da v407 (psion_canto_v407 com as cinco chaves iguais; cunhagens_v407 com a E21 ao lado; kh_n1_cobertura_v407 com pisos), os da v406, da v405, da v404, da v403, da v402, da v401 e da v399, o selo pela propria tecnologia e o quadro do topo seguindo selados, o sidecar reescrito, a letra do veredito do gate igual a da v407 e nenhum veredito fora da troca dita mudado?" % (DL_.N_BUNDLE, len(DL_.ANCORAS), DL_.N_BUNDLE),
            "dados": ["os %d modulos (as pedras em pedra\\ e insumos\\, com as candidatas de origem e os recibos de compilacao; o bundle pinado em BUNDLE_v408.json), pinados por sha256 (so' lidos), e a medida da cobertura (KH_N1_v408.json)" % DL_.N_BUNDLE,
                      "as %d falas de 04/11 por sha256 em insumos\\cunhagens (todas falas do operador; duas de autor misto, so' o paragrafo dele citavel; a lista esta no registro cunhagens_v408 e na linhagem)" % len(verb),
                      "o kernel do rito (as ancoras, as bandeiras e a proveniencia), a afericao do traco e do dicionario no kernel, a copia purgada do levantamento do acervo e o recibo da purga, o recibo dos nomes, o proprio um.py, o core e o selo da rodada; nenhum dado novo foi aberto nesta rota"],
            "metodo": "lake build + Audit no sandbox k408c (os modulos do bundle sobre o kernel da v407 selada); ensaio a seco do candidato; rito completo; conferidor (deve mudar / nao pode mudar, com o quadro do topo conferido de novo contra o resultado pinado nas duas linguas e no .md, e os itens do selo mais o round trip do um.py instalado); "
                      "leitura da rodada (inclui o sidecar e a linha final do rito); superficies com a regra da linhagem completa (o MEMORY.md nao e' compactado: recusa por contagem); elo B(n) da Bancada (passo simples v407 -> v408, sem salto; recibos); a guarda das frases e a P18 em todo texto novo; o paragrafo novo e o do quadro, a nota ao lado do paragrafo da v407 e o sidecar, no handoff; os sete textos da custodia encadeados (D52)",
            "resultado": " | ".join(_vr408(v_) for v_ in [pc["verdict"], cg["verdict"], kh["verdict"]]) + " | (vereditos resumidos a 200 caracteres; a integra esta no core da rodada, um_absoluto.json) | sidecar %s (%s objetos, %s recusas) | %s | %s | escada %s -> %s (teoremas limpos %s/%s; %d bandeiras novas, todas do tetelestai_terminal; ancoras por modulo: %s)" % (
                sc["veredito"], sc["n_objetos"], sc["recusas"], resumo_conf, ("%s vereditos fora da troca dita mudaram (exigido 0)" % nvm) if nvm != "nao lido" else "vereditos fora da troca dita: nao lidos nesta leitura", esc0, esc1, ESP["escada"][0], ESP["escada"][1], NF, por_mod),
            "defeito": "as ressalvas, ditas: " + ress + "; o registro CONFERE o que o kernel prova e nao prova nada por si; o gate nao se moveu e a independencia das 4 bandeiras experimentais segue aberta (derivam de UM so' booleano) [DECLARADO, GV-01 e GV-03]; a pendencia [LEGAL] (D2) segue do operador; a revisao distinta do pacote e' o Sonnet (D54) e nao e' afirmada por este registro",
            "nao_refazer": "a integracao dos %d modulos e a escada %s -> %s estao medidas; as %d ancoras no kernel do rito estao lidas e conferidas contra o um.py instalado; repetir os registros so' com kernel ou um.py novo; a palavra «impedância» esta PODADA como termo (D50): nao e' caminho a reabrir sem termo novo; a traducao das classes do dicionario as classes das maquinas de Turing e' a proxima construcao, [OPEN] (D51 revista)" % (DL_.N_BUNDLE, esc0, esc1, len(DL_.ANCORAS)),
            "proximo_passo": "a ligacao do par na face de Fock (v409: o Fock concreto tem criacao e aniquilacao; E21); o teste (d), so' se tiver poder (opcao (c) do operador), por citacao do pre-registro; o motor continuo no pilar quantico, quando o operador disser o conteudo observavel; o README pinado (D39) e o release v408 do app e do contrato do JEV (S10, D53), na custodia e na engenharia da casa; decisao [LEGAL] D2 com a agente de PI; custodia conjunta pela sessao do site (o handoff traz os paragrafos prontos do README e do site, a nota ao lado do paragrafo da v407, os sete textos da custodia e lista o sidecar); revisao independente do pacote (o Sonnet, D54)",
            "onde": PK, "artefatos": arts, "refs": sorted((set(x["rota_id"] for x in T9) | set(REFS) | set(preparo_no_livro(ids))) - {NOVA}),
            "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move; as erratas E21 a E23 e as decisoes D48 a D54 sao da gerencia c1, em nome proprio, ao lado (nada foi apagado nem reescrito); %s." % sim(c_seguem, "os registros anteriores seguem selados", "ALGUM REGISTRO ANTERIOR NAO SELOU")}
    for r in ROTA["refs"]:
        assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
    REG = [ROTA] + T9
    for x in REG:
        for k_, v_ in x.items():
            if isinstance(v_, str):
                assert len(v_) <= 6000, "o campo %s de %s passa de 6000 caracteres (limite do Mapa): resuma e aponte o artefato" % (k_, x["rota_id"])
    bad = [(x["rota_id"], violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad, "a guarda de texto (P18) achou violacao(oes): %r" % bad
    import guarda_frases_v408 as GF
    bad2 = [(x["rota_id"], GF.violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if GF.violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad2, "a guarda das frases achou violacao(oes): %r" % bad2
    atrib = [(x["rota_id"], T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))]
    assert not atrib, "a direcao do testemunho esta invertida ou a atribuicao falhou: %r" % atrib
    ruins = regra_4_44(REG, z, p)
    assert not ruins, "a regra do 4,44 (o p calibrado e a linha dos 5 sigma no mesmo campo) falhou em: %r" % ruins[:3]
    assert c_seguem and c_q, "algum registro anterior (quadro, v407, v406, v405, v404, v403, falsidade, ponte, queda, esperanca, selo, declaracao, sonico, afinacao, rede de Fock, psibit, testemunha estatica) nao selou no core: o mapa nao registra a v408 assim"
    return REG


def gravar(p, b):
    """backup de BYTES se existir e mudar; temporario -> conferir tamanho -> substituir."""
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m408"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_m408"; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def main():
    V, PROB = L.ler()
    if PROB:
        print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); return 2
    NOS = L.NOS
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v408_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v408_*.json")), key=os.path.getmtime)
    arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto_selo_acom.json"), os.path.join(PK, "ESPERADOS_v408.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v408.json"),
            os.path.join(PK, "DIFF_KERNEL_v408.txt"), os.path.join(PK, "DIFF_v407_v408.diff"), os.path.join(NOS, "HANDOFF_v408_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v408.json"),
            os.path.join(PK, "kernel", "KERNEL_RECIBO_v408.json")] + sorted(glob.glob(os.path.join(PK, "pedra", "*.lean"))) + b3[-1:]
    arts = [x for x in arts if os.path.exists(x)]
    REG = montar(V, core, selo, ids_do_livro(), arts)
    J = os.path.join(HERE, "registro_mapa_v408.json")
    gravar(J, json.dumps(REG, ensure_ascii=False, indent=1).encode("utf-8"))
    quem = "claude-c1 (gerência), cadeia v408"
    print("registro MONTADO (NAO registrado): %d registro(s) (%s) -> %s" % (len(REG), ", ".join(x["tipo"] for x in REG), J))
    print("COMANDO (o passo 12 da cadeia o executa, uma vez so): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
    print("DEPOIS DO REGISTRO: os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
