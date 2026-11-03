# -*- coding: utf-8 -*-
# [ADAPTADO v406, 02/11/2026] sobre a subida mecanica da v405 FINAL (derivar_encanamento_v406.py, lote F) por adaptar_pos_rito_v406.py: o conteudo e' o da v406 (O FECHAMENTO: bundle de 301 modulos, UM registro com funcao fechamento_v406, quatro chaves de testemunha lidas do kernel); a gerencia revisa antes do rito (nao e' versao selada).
"""registrar_mapa_v406.py -- MONTA (nao registra) o registro da v406 no mapa de rotas e imprime o comando (molde: registrar_mapa_v405.py, que rodou na v405, e registrar_mapa_v399.py). Rodar DEPOIS do fechar (handoff gravado). ADAPTADO ao fechamento em 02/11/2026.
A v406 traz UMA rota nova, umpy.v406.selada_o_fechamento_02nov (o conteudo e' o do selo): os 301 modulos de kernel (os 300 da bancada do ChatGPT, F1.FECHO_20261015, recompilados do fonte, e a candidata CanonicalFullTGLWitnessR1, de nome PROVISORIO), UM registro com FUNCAO (fechamento_v406: le do kernel do proprio rito as oito ancoras, os 301 modulos por sha256, as quatro chaves de testemunha, o que fica False por teorema, a escada e o gate)
e os DOIS por spec (cunhagens_v406 e kh_n1_cobertura_v406), mais ANOTACOES nas rotas que esperavam por ela (o programa do fechamento, o inventario das chaves de testemunha, a do Um inscrito e o autovetor da luz, o gate, o B(n) da Bancada, o quadro do Teste da Unica Palavra e a v405 que a precede) e TRES ERRATAS ao lado, em nome proprio da gerencia c1, com o seq do registro corrigido lido do livro (E14: os registros da v394, da v395 e da v396 que
diziam o certificado de Fock sem habitante: era verdade na data; a correcao vai AO LADO, nada se apaga).
Cada afirmacao e' testada contra o core/selo/ESPERADOS lidos por script (o registro existe? selou? o que NAO fechou fica dito); nenhum numero e' digitado (as contagens saem do core, de ESPERADOS e de delta_v406; os seq saem do livro).
REGRA DA ORDEM DO OPERADOR (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no MESMO campo; montar() RECUSA (assert) se algum campo do registro trouxer o 4,44 sem eles. Nao ha inscricao da gerencia nesta versao: todas as falas sao do operador; as erratas e as decisoes sao da gerencia, em nome proprio.
Fail-closed: o selo tem de ser a v406; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir (se a gerencia registrar antes uma rota de preparo com o MESMO id, montar() recusa e a constante NOVA muda). A rota de preparo da gerencia (registro_mapa_v406_prep.json, se existir) entra nas refs so' se ja' estiver no livro.
SAIDA: pos_rito\\registro_mapa_v406.json e o comando `rotas.py registrar` (quem o executa e' o passo 12 da cadeia, uma vez so', com marcador idempotente; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real. montar() le o core, o selo e ESPERADOS_v406.json; de V so' usa o que a leitura da rodada ja' validou (s16, sidecar, conferidor), sempre com valor de reserva dito."""
import glob, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v406 as L
import textos_v406 as T
from guarda_p18_v406 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V406"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v406 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOVA = "umpy.v406.selada_o_fechamento_02nov"
R_PROG = "kernel.fechamento_construir_tudo_programa_02nov"                  # o programa do fechamento (ordem do operador de 02/11: construir tudo)
R_INV = "kernel.inventario_chaves_de_testemunha_v405_02nov"                 # o inventario das chaves de testemunha do selo v405
R_AUTOV = "conceitual.o_um_inscrito_e_o_autovetor_da_luz_02nov"             # o Um inscrito e o autovetor da luz (E15)
R_V394 = "umpy.v394.fock_tempo_e_cunhagens"                                 # a rede de Fock da v394 (o veredito dizia JOINT_CONTRACT_OPEN)
R_V395 = "umpy.v395.psibit_na_fractalizacao_do_um"                          # o psibit da v395 (a face do psion condicional)
R_V396 = "umpy.v396.testemunha_estatica_na_fractalizacao_do_um"             # a testemunha estatica da v396
R_GATE = "gate.qg_closure"
R_BANC = "infra.bancada_um.sincronizacao_vnnn"
R_QUADRO = "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9"
R_V405 = "umpy.v405.selada_massa_derivada_e_identidade_01nov"
ANOTADAS = (R_PROG, R_INV, R_AUTOV, R_V394, R_V395, R_V396, R_GATE, R_BANC, R_QUADRO, R_V405)
REFS = ("custodia.v405", "infra.custodia_g1.licoes_v405", "umpy.v400.correcao_da_v399_alfa_unico_e_beta_contra_o_core", "gate.maquina_do_veredito_final", "natureza.cinco_sigma_02_kimi_01nov")
PREP = os.path.join(PK, "registro_mapa_v406_prep.json")     # a rota de preparo da gerencia: lida em tempo de execucao; entra nas refs so' se a ROTA dele ja' estiver no livro
_CACHE = {}


def _esp():
    """ESPERADOS_v406.json (lido uma vez por processo)."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v406.json"), encoding="utf-8"))
    return _CACHE["esp"]


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
    """As rotas ROTA de registro_mapa_v406_prep.json (se o arquivo existir e ler) que ja' estao no livro e nao sao a nova: entram nas refs. Ausente ou ilegivel = nenhuma (dito, nunca falha)."""
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
    return [c for c in caminhos if os.path.isfile(c)]


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
    p = json.load(open(os.path.join(PK, "PINOS_BN_v406.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v405" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v405 -> v406 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1, "deployment_id": bp["deployment_id"]}


def montar(V, core, selo, ids, arts):
    """Monta os registros (a ROTA nova, as ANOTACOES e as ERRATAS), cada afirmacao testada contra o core/selo/ESPERADOS; devolve a lista; recusa (assert) se algo nao conferir. Nao escreve nada."""
    assert selo.get("um_version") == "v406", "o selo nao e a v406"
    assert NOVA not in ids, "a rota %s ja existe no mapa" % NOVA
    for r in ANOTADAS + REFS:
        assert r in ids, "a rota %s nao existe no mapa (anotada ou citada em refs)" % r
    ESP = _esp(); DL_ = T._qd().DL
    S = ESP["candidato_sha16"]
    assert str((selo.get("sha256") or {}).get("um.py", ""))[:16] == S, "o um.py do selo nao e o candidato de ESPERADOS"
    assert V.get("s16") in (None, S), "o s16 da leitura != o candidato de ESPERADOS"
    BASE = ESP["origem_sha16"]
    esc0, esc1 = ESP["escada_v405_e_v406"]
    NF = ESP["n_bandeiras_novas"]
    assert esc1 - esc0 == NF == sum(ESP["n_bandeiras_por_grupo"].values()) == len(ESP["bandeiras_novas_chaves"]) == ESP["politica_de_bandeiras"]["n_flags"], "a escada nao fecha com as bandeiras novas"
    assert ESP["kernel"]["modulos_novos"] == DL_.N_BUNDLE == len(DL_.BUNDLE_RELS), "o delta do kernel nao e o bundle"
    BETA = ESP["beta"] if isinstance(ESP.get("beta"), float) else None
    FRASE = DL_.FRASE_DA_MOLDURA_V406_PT

    # --- o quadro do topo (a regra do 4,44): o registro selado, lido pelas MESMAS funcoes do artigo
    tvr = core.get("teste_de_veracidade_fase9_v397") or {}
    a = T._qd().Q._v397_atomos(tvr, "pt"); assert a["sealed"] is True, "o registro teste_de_veracidade_fase9_v397 nao sela no core: o mapa nao registra o 4,44 assim"
    z, p = a["z_disc"]["md"], a["p_disc"]["md"]
    z444 = "z_disc = %s (calibrado; p unilateral %s), abaixo do degrau de 5σ da creditação, que não foi alcançado (%s < 5)" % (z, p, z)

    def selou(k):
        return (core.get(k) or {}).get("all_verified") is True

    # --- o registro com FUNCAO fechamento_v406: tudo lido do core e conferido contra ESPERADOS e delta_v406
    fe = core.get("fechamento_v406") or {}; fv = fe.get("values") or {}; mech = fe.get("mechanics") or {}; fk = fe.get("four_keys") or {}
    assert fe.get("all_verified") is True and fe.get("verdict") == ESP["vereditos_novos_v406"]["fechamento_v406"] and fe.get("certificate_inhabited") is True and fe.get("does_not_gate_core") is True, "fechamento_v406 nao selou ou != ESPERADOS"
    assert mech.get("passed") is True and mech.get("n_checks") == DL_.N_CHECKS_FECHO == len(mech.get("checks") or []) and all(c.get("ok") is True for c in mech["checks"]), "as checagens do fechamento_v406 nao passaram"
    assert fv.get("n_ancoras_ok") == len(DL_.ANCORAS) and fv.get("n_modulos_ok") == fv.get("n_modulos") == DL_.N_BUNDLE and fv.get("n_flags_true") == fv.get("n_flags") == NF and fv.get("escada") == [esc1] * 3, "os valores do fechamento_v406 != ESPERADOS/delta"
    assert fe.get("beta_ok") is True and fe.get("embedded_sources_ok") is True and fe.get("embedded_sources_n_ok") == DL_.N_BUNDLE and fe.get("guarda_violacoes") in ([], None), "o beta, as fontes embutidas ou a guarda do fechamento_v406 nao conferem"
    assert fk.get("kernel_reads_the_certificate_as_inhabited") is True and fk.get("rede_fock_v394.whole_certificate_inhabited") is True and fk.get("psibit_v395.conditional_psion_face.inhabitant_exhibited") is True and fk.get("testemunha_estatica_v396.fock_face.inhabitant_exhibited") is True \
        and fk.get("witness_layers.canonical_full_witness_term_constructed") is True and fk.get("testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma") is False and fk.get("qg_closure.gate.full_static_witness_exists") is False and fk.get("witness_rigidity.trivial_inhabitant_exists") is False, "as quatro chaves ou o que fica False por teorema != o delta"
    assert list(fe.get("ressalvas") or []) == list(DL_.RESSALVAS_V406), "as ressalvas do registro != delta_v406.RESSALVAS_V406"
    BETA_RT = fv.get("beta"); assert isinstance(BETA_RT, float) and (BETA is None or abs(BETA_RT - BETA) <= 1e-9 * BETA), "o beta do registro != o do core/ESPERADOS (tolerancia relativa 1e-9)"
    ancoras = "; ".join("%s (%s)" % (n_.split(".")[-1], DL_.ANCORAS[n_]["rel"].split("/")[-1][:-5]) for n_ in DL_.ANCORAS)
    ress = " | ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(fe["ressalvas"]))
    # --- o gate NAO se moveu: o registro segue selado e a letra do veredito e' a da v405
    gk = core.get("bandeiras_do_gate_v403") or {}; gvv = gk.get("values") or {}; gb = T._base_core().get("bandeiras_do_gate_v403") or {}
    assert gk.get("all_verified") is True and (V.get("gate") or {}).get("sealed", True) is True and gvv == gb.get("values") and (gk.get("mechanics") or {}).get("passed") is True, "bandeiras_do_gate_v403 (recriado) nao selou ou != a v405 selada"
    qg = core.get("qg_closure") or {}; fam = [len(qg.get(f) or {}) for f in ("formal_flags", "physics_flags", "experiment_flags")]
    assert (qg.get("gate") or {}).get("verdict") == ESP["qg_closure_gate_verdict_v405"] == selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"], "a letra do veredito do gate mudou"
    # --- os dois registros por spec
    cg = core.get("cunhagens_v406") or {}; kh = core.get("kh_n1_cobertura_v406") or {}
    for nome_, r_ in (("cunhagens_v406", cg), ("kh_n1_cobertura_v406", kh)):
        assert r_.get("all_verified") is True and r_.get("verdict") == ESP["vereditos_novos_v406"][nome_], "%s nao selou ou != ESPERADOS" % nome_
    verb = cg.get("verbatim") or {}; ex = cg.get("extras") or {}
    assert len(verb) == len(ESP["cunhagens"]) == len(DL_.VERBATIM_ORIGEM_V406) and set(verb) == set(ESP["cunhagens"]) and all(v.get("embedded_ok") is True for v in verb.values()), "as inscricoes de 02/11 nao estao embutidas por sha256"
    assert all(str((ESP["cunhagens"][k_] or {}).get("nome", "")).startswith("OPERADOR_02nov_") for k_ in ESP["cunhagens"]), "alguma inscricao nao e' fala do operador"
    erratas = cg.get("erratas") or []; assert len(erratas) == 4 and all("gerencia c1, em nome proprio" in e.get("assinatura", "") for e in erratas), "as erratas E14 a E17 nao estao no registro ou nao sao da gerencia c1 em nome proprio"
    dec = ex.get("decisoes") or {}; assert all(("D%d" % i) in dec for i in range(34, 41)), "faltam decisoes D34 a D40 no registro"
    assert ex.get("leituras") == DL_.LEITURA_V406, "a leitura da v406 no registro != delta_v406"
    cob = kh.get("lido") or {}; assert cob.get("constantes_cobertas") and cob.get("teoremas_cobertos"), "kh_n1_cobertura_v406 sem a cobertura"
    seguem = ("ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405", "cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405",
              "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "falsidade_da_inercia_v401", "cunhagens_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402",
              "teste_de_veracidade_fase9_v397", "cunhagens_v397", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "sonico_v398", "afinacao_das_cordas_v398", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396")
    c_seguem = all(selou(k) for k in seguem)
    tv_v = ESP["veracidade"]; c_q = bool(selou("teste_de_veracidade_fase9_v397") and selou("cunhagens_v397") and tvr.get("verdict") == tv_v["verdict"])
    sc = _sidecar(V); conf_dm = V.get("conf_dm", "nao lido"); conf_np = V.get("conf_np", "nao lido"); nvm = V.get("n_ver_mudaram", "nao lido")
    bank = _bancada(); regs = livro()
    # --- o seq que cada errata corrige, lido do livro (e o registro tem de trazer o trecho corrigido)
    sq_v394 = seq_do_alvo(regs, R_V394, "ROTA", contem=("JOINT_CONTRACT_OPEN",))
    sq_v395 = seq_do_alvo(regs, R_V395, "ROTA", contem=("UNINHABITED",))
    sq_v396 = seq_do_alvo(regs, R_V396, "ROTA", contem=("habitante",))
    sq_v405 = seq_do_alvo(regs, R_V405, "ROTA")
    KR = os.path.join(PK, "kernel", "KERNEL_RECIBO_v406.json")
    E = {}
    for e in erratas:
        m_ = re.match(r"^(E1[4-7]) -- ", e.get("agora", "")); assert m_, "uma errata do registro nao comeca por E<n> --"
        E[m_.group(1)] = e
    assert sorted(E) == ["E14", "E15", "E16", "E17"], "as erratas do registro nao sao E14 a E17"

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

    cand = os.path.join(PK, "pedra", DL_.TESTEMUNHA["name"] + ".lean")
    T9 = []
    T9.append(anot(R_PROG, "v406 SELADA %s: o fechamento entrou no kernel do rito — o certificado de Fock esta habitado por construcao e a passagem para o continuo e' termo" % S,
                   f"o registro fechamento_v406 selou={selou('fechamento_v406')} com {mech['n_checks']} checagens: {fv['n_ancoras_ok']} ancoras ({ancoras}), {fv['n_modulos_ok']}/{fv['n_modulos']} modulos por sha256, {fv['n_flags_true']}/{fv['n_flags']} bandeiras, escada {esc0} -> {esc1}, beta = alfa x raiz de e em runtime = {BETA_RT!r}; "
                   f"{' | '.join(fe['diz'])} | {FRASE}. As ressalvas, ditas (D36): {ress}",
                   "o nome da candidata (operador); o README pinado e a linha do quadro (D39, plano a parte); o motor continuo no pilar quantico, com pre-registro (D38, v407); custodia (G1); revisao distinta do pacote (o Sonnet, D37).", refs=[R_INV, R_AUTOV], artefatos=[cand, KR],
                   estatuto="REAL (os termos e a leitura no kernel do rito); INPUT (a ordem do operador); ONTO (as leituras dele); DECLARADO (a ratificacao R10, o parecer R7 e a revisao do Sonnet); KNOWN/OPEN (K(O) != bot so' na cunha; o nucleo II_inf)",
                   defeito="o registro CONFERE o que o kernel prova, nao prova nada por si; validade no kernel nao e' creditacao; " + "; ".join(DL_.RESSALVAS_V406[:3])))
    T9.append(anot(R_INV, "v406 SELADA %s: as quatro chaves de testemunha passaram de literal False a LEITURA do kernel do rito; as duas que ficam False ficam por teorema" % S,
                   f"rede_fock_v394.whole_certificate_inhabited = {fk['rede_fock_v394.whole_certificate_inhabited']}, psibit_v395...inhabitant_exhibited = {fk['psibit_v395.conditional_psion_face.inhabitant_exhibited']} (status {fk['psibit_v395.conditional_psion_face.status']}), testemunha_estatica_v396...inhabitant_exhibited = {fk['testemunha_estatica_v396.fock_face.inhabitant_exhibited']} (status {fk['testemunha_estatica_v396.fock_face.status']}), "
                   f"witness_layers.canonical_full_witness_term_constructed = {fk['witness_layers.canonical_full_witness_term_constructed']}; ficam False por teorema: full_static_witness_exists = {fk['qg_closure.gate.full_static_witness_exists']} e trivial_inhabitant_exists = {fk['witness_rigidity.trivial_inhabitant_exists']}; segue False o lema que liga psion C ao psionCorner (linked_to_the_corner_by_a_lemma = {fk['testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma']}). "
                   f"{corpo('E14')}",
                   "o lema que liga o psion ao canto segue faltando [OPEN]; K(O) != bot para O compacto segue [OPEN].", refs=[R_PROG, R_V394, R_V395, R_V396], estatuto="REAL (a leitura do kernel do rito e o registro); OPEN (o lema; K(O) != bot para O compacto)"))
    T9.append(anot(R_AUTOV, "v406 SELADA %s: o Um inscrito como o unico vetor fixo da luz entra como leitura [ONTO] do operador; a errata E15 fica ao lado" % S,
                   f"o registro cunhagens_v406 selou={selou('cunhagens_v406')} com a leitura de 02/11 (um_inscrito, um_comprimido e espelhamento, estatuto {DL_.LEITURA_V406['estatuto']}); {corpo('E15')}",
                   "a pedra candidata OUmInscrito fica FORA do kernel desta versao ate' o operador nomea-la.", refs=[R_PROG], estatuto="REAL (os termos citados no kernel do rito); ONTO (a leitura do operador); a errata E15 e' da gerencia, em nome proprio",
                   defeito="o termo prova o unico vetor FIXO da luz; autovetor com fase nao e' excluido por termo; nenhuma pedra nova do dia entrou no kernel"))
    T9.append(anot(R_GATE, "v406 SELADA %s: o gate NAO se moveu — o qg_closure do core e' identico ao da v405 (as 18 bandeiras calculadas, a letra do veredito)" % S,
                   f"o registro bandeiras_do_gate_v403 (recriado) selou={selou('bandeiras_do_gate_v403')} com os mesmos valores da v405 selada: das {gvv['n_flags']} bandeiras ({fam[0]} formais, {fam[1]} fisicas, {fam[2]} experimentais) {gvv['n_true']} sao True e {gvv['n_calculated']} sao CALCULADAS ({gvv['n_literal']} literais); o veredito le {gvv['n_read_by_the_verdict']}; a letra do veredito do gate e' a da v405 e a do selo. "
                   "Nenhuma bandeira do gate depende dos modulos da v406; full_static_witness_exists e trivial_inhabitant_exists seguem False. [DECLARADO, GV-03 da auditoria de 28/09/2026] As 4 bandeiras experimentais derivam de UM so' booleano; o degrau experimental le so' o rito V11 do piso, unilateral (GV-01).",
                   "a independencia das 4 experimentais e os mocks de survey seguem [OPEN]; o gate nao se move por esta rota.", refs=[R_PROG],
                   artefatos=[os.path.join(PK, "CANDIDATO_v406.json")], estatuto="REAL (o core do rito); DECLARADO (GV-01, GV-03, EV-12 da auditoria de 28/09/2026); OPEN (a independencia das 4 experimentais)",
                   defeito="o gate nao e' teste e nao discrimina o LCDM raso; NOT_FALSIFIED nunca e' a palavra da creditacao"))
    T9.append(anot(R_BANC, "v406 SELADA %s: o B(n) da v406 e' um passo SIMPLES v405 -> v406 (a Bancada de producao ja' pinava a v405)" % S,
                   f"o kernel da v406 difere do da v405 pelos {DL_.N_BUNDLE} modulos novos (recibo do kernel KERNEL_RECIBO_v406, contrato R3_2; DIFF_KERNEL_v406.txt: modulos novos e TGLExt.lean com os dois imports a mais); o recibo pre_selo foi gerado e pinado ANTES da instalacao, em ensaio contra a producao (nada gravado; a Bancada pinava {bank['deployment_id']}), "
                   f"e a cadeia confere os pinos de PINOS_BN_v406.json na hora; o veredito esperado do aplicar e' REPINADA_B{bank['proxima']}__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_ e sem cadeia de selos, lido do codigo do esboco R3.5. Parada e religamento do servico exigem V406_AUTORIZACAO_OPERADOR (texto sem o nome do script do servico).",
                   "depois do aplicar, a Bancada pina a v406.", refs=[R_PROG],
                   artefatos=[os.path.join(PK, "PINOS_BN_v406.json"), os.path.join(PK, "PINO_RECIBO_PRE_SELO_v406.json"), KR]))
    T9.append(anot(R_QUADRO, "v406 SELADA %s: o quadro do topo (O Teste da Única Palavra) segue intocado e o registro teste_de_veracidade_fase9_v397 segue selado" % S,
                   f"teste_de_veracidade_fase9_v397 selou={c_q} no rito da v406 (veredito igual ao de ESPERADOS; {tv_v['n_checks']} checagens): o quadro do artigo PT/EN e do .md, conferido contra o resultado pinado, segue no topo, com os numeros e a regra da ordem de sempre: {z444}. "
                   "Nenhum sigma, p ou lnB novo e' calculado nesta rota; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma) vale em todo texto que o cite; o paragrafo do quadro segue no README/site e o handoff da v406 traz tambem o paragrafo novo (o fechamento), sem o 4,44.",
                   "o paragrafo do README/site e' ato da sessao do site; a creditacao segue sendo beta_TGL na natureza a 5 sigma (nao ha o que repetir deste pacote, a abertura esta consumida).", refs=[R_PROG]))
    T9.append(anot(R_V405, "v406 SELADA %s: a v405 e' a base selada da v406; os treze registros dela sao recriados e seguem selados e iguais" % S,
                   f"a v406 parte da v405 selada (um.py {BASE}) e acrescenta {DL_.N_BUNDLE} modulos de kernel, UM registro com funcao (fechamento_v406) e dois por spec, e a secao do artigo; os treze registros da v405 (ponte_da_massa_v405 selou={selou('ponte_da_massa_v405')}, identidade_v405 selou={selou('identidade_v405')}, cunhagens_v405 selou={selou('cunhagens_v405')}, gap_v405 selou={selou('gap_v405')}), os da v404, da v403, da v402, da v401 e da v399 seguem selados neste rito "
                   f"(caminho_v403 selou={selou('caminho_v403')}, falsidade_da_inercia_v401 selou={selou('falsidade_da_inercia_v401')}), como seguem o selo pela propria tecnologia e a declaracao do operador (v399), o sonico e a afinacao (v398) e o quadro (v397); sidecar um_absoluto_selo_acom.json {sc['veredito']} ({sc['n_objetos']} objetos, {sc['recusas']} recusas, sha16 {sc['sha16']}). "
                   f"O registro kh_n1_cobertura_v405 e os contratos passam a cobrar piso (errata de contagem no registro kh_n1_cobertura_v406); a v405 e as pedras dela ficam como registro (seq {sq_v405}).",
                   "custodia conjunta pela sessao do site (o handoff lista o sidecar e traz a nota ao lado dos paragrafos anteriores).", refs=[R_PROG]))
    T9.append(errata(R_V394, sq_v394,
                     f"[E14 · ERRATA AO LADO, gerencia c1, em nome proprio, 02/11/2026, v406 {S}] Corrige o registro seq {sq_v394} desta rota (a v394 selada), cujo veredito de rede_fock_v394 diz JOINT_CONTRACT_OPEN e cujo literal whole_certificate_inhabited era False; era verdade na data. {corpo('E14')}. O veredito de rede_fock_v394 no core da v406 e' o da TROCA DITA; os registros corrigidos NAO foram apagados nem reescritos: a correcao vai ao lado.",
                     refs=[R_PROG, R_INV]))
    T9.append(errata(R_V395, sq_v395,
                     f"[E14 · ERRATA AO LADO, gerencia c1, em nome proprio, 02/11/2026, v406 {S}] Corrige o registro seq {sq_v395} desta rota (a v395 selada), que da' a face do psion como condicional a um certificado sem habitante (status {DL_.STATUS_ANTIGO}); era verdade na data. Na v406 inhabitant_exhibited e' LIDO do kernel do rito (True; status {DL_.STATUS_HABITADO}); {corpo('E14')}. Os registros corrigidos NAO foram apagados nem reescritos.",
                     refs=[R_PROG, R_INV]))
    T9.append(errata(R_V396, sq_v396,
                     f"[E14 · ERRATA AO LADO, gerencia c1, em nome proprio, 02/11/2026, v406 {S}] Corrige o registro seq {sq_v396} desta rota (a v396 selada), que diz a face de Fock sem habitante; era verdade na data. Na v406 inhabitant_exhibited e' LIDO do kernel do rito (True; status {DL_.STATUS_HABITADO}); linked_to_the_corner_by_a_lemma SEGUE False (nenhum lema liga psion C ao psionCorner); {corpo('E14')}. Os registros corrigidos NAO foram apagados nem reescritos.",
                     refs=[R_PROG, R_INV]))
    for x in T9:
        assert x["rota_id"] in ids, "a rota %s nao existe no mapa" % x["rota_id"]
    resumo_conf = ("conferidor %s e %s" % (conf_dm, conf_np)) if "nao lido" not in (conf_dm, conf_np) else "conferidor: o resultado nao veio na leitura desta rodada"
    _vr406 = lambda v_: v_ if len(v_) <= 200 else v_[:197] + "..."   # o campo resultado do Mapa tem teto de 6000 caracteres (rotas._valida: resuma e aponte o artefato): a integra de cada veredito esta no core da rodada e nos ESPERADOS
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
            "titulo": "v406 SELADA %s: o fechamento — %d modulos de kernel (os 300 da bancada do ChatGPT e a candidata %s, de nome provisorio), o registro fechamento_v406, cunhagens_v406 e kh_n1_cobertura_v406, %d inscricoes de 02/11 por sha256; escada %s -> %s; o certificado de Fock esta habitado por construcao e as quatro chaves de testemunha sao lidas do kernel; validade no kernel nao e' creditacao; o gate nao se move" % (
                S, DL_.N_BUNDLE, DL_.TESTEMUNHA["name"], len(verb), esc0, esc1),
            "pergunta": "o candidato v406 selou com os 301 modulos de kernel, o registro com FUNCAO fechamento_v406 (que le do kernel do proprio rito as oito ancoras, os 301 modulos por sha256, as quatro chaves de testemunha lidas e nao literais, o que fica False por teorema, a escada exata e o gate) e os dois por spec (as falas do operador de 02/11 por sha256, as decisoes D34 a D40, as erratas E14 a E17, a cobertura KH-N1), "
                        "com os treze registros da v405, os da v404, da v403, da v402, da v401 e da v399, o selo pela propria tecnologia e o quadro do topo seguindo selados, o sidecar reescrito, a letra do veredito do gate igual a da v405 e nenhum veredito fora da troca dita mudado?",
            "dados": ["os 301 modulos (a candidata %s em pedra e insumos, e o bundle pinado em BUNDLE_v406.json), pinados por sha256 (so' lidos), e a medida da cobertura (KH_N1_v406.json)" % DL_.TESTEMUNHA["name"],
                      "as %d falas de 02/11 por sha256 em insumos\\cunhagens (todas falas do operador; a lista esta no registro cunhagens_v406 e na linhagem)" % len(verb),
                      "o kernel do rito (as ancoras, as bandeiras e a proveniencia), o recibo da bancada (16/10/2026), o parecer R7 e a ratificacao R10 (lidos por hash), o proprio um.py, o core e o selo da rodada; nenhum dado novo foi aberto nesta rota"],
            "metodo": "integracao R3 (300 modulos recompilados do fonte, 0 falhas) e lake build + Audit no sandbox k406c; ensaio a seco do candidato; rito completo; conferidor (deve mudar / nao pode mudar, com o quadro do topo conferido de novo contra o resultado pinado nas duas linguas e no .md, e os 16 itens C1-C16 do selo mais o round trip do um.py instalado); "
                      "leitura da rodada (inclui o sidecar e a linha final do rito); superficies com a regra da linhagem completa (o MEMORY.md nao e' compactado: recusa por contagem); elo B(n) da Bancada (passo simples v405 -> v406, sem salto; recibos); a guarda das frases em todo texto novo; o paragrafo novo e o do quadro, a nota ao lado dos paragrafos anteriores e o sidecar, no handoff",
            "resultado": " | ".join(_vr406(v_) for v_ in [fe["verdict"], cg["verdict"], kh["verdict"]]) + " | (vereditos resumidos a 200 caracteres; a integra esta no core da rodada, um_absoluto.json) | sidecar %s (%s objetos, %s recusas) | %s | %s | escada %s -> %s (teoremas limpos %s/%s; %d bandeiras novas, todas do fecho)" % (
                sc["veredito"], sc["n_objetos"], sc["recusas"], resumo_conf, ("%s vereditos fora da troca dita mudaram (exigido 0)" % nvm) if nvm != "nao lido" else "vereditos fora da troca dita: nao lidos nesta leitura", esc0, esc1, ESP["escada"][0], ESP["escada"][1], NF),
            "defeito": "as ressalvas, ditas: " + ress + "; o registro CONFERE o que o kernel prova e nao prova nada por si; o gate nao se moveu e a independencia das 4 bandeiras experimentais segue aberta (derivam de UM so' booleano) [DECLARADO, GV-01 e GV-03]; a pendencia [LEGAL] (D2) segue do operador; a revisao distinta do pacote e' o Sonnet (D37) e nao e' afirmada por este registro",
            "nao_refazer": "a integracao dos 301 modulos e a escada %s -> %s estao medidas; as oito ancoras no kernel do rito estao lidas e conferidas contra o um.py instalado; repetir os registros so' com kernel ou um.py novo; a pergunta sobre o literal das quatro chaves foi respondida (viraram leitura do kernel, errata E14 ao lado)" % (esc0, esc1),
            "proximo_passo": "o nome da candidata e das pedras candidatas do dia (operador); o README pinado e a linha do quadro no site (D39); o motor continuo no pilar quantico, com pre-registro (D38, v407); a ordem Kimi 5 sigma 02 (natureza.cinco_sigma_02_kimi_01nov); decisao [LEGAL] D2 com a agente de PI; custodia conjunta pela sessao do site (o handoff traz os paragrafos prontos do README e do site, a nota ao lado dos paragrafos anteriores e lista o sidecar); revisao independente do pacote (o Sonnet, D37)",
            "onde": PK, "artefatos": arts, "refs": sorted(set(x["rota_id"] for x in T9) | set(REFS) | set(preparo_no_livro(ids)) - {NOVA}),
            "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move; as erratas E14 a E17 e as decisoes D34 a D40 sao da gerencia c1, em nome proprio, ao lado (nada foi apagado nem reescrito); %s." % sim(c_seguem, "os registros anteriores seguem selados", "ALGUM REGISTRO ANTERIOR NAO SELOU")}
    for r in ROTA["refs"]:
        assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
    REG = [ROTA] + T9
    bad = [(x["rota_id"], violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad, "a guarda de texto (P18) achou violacao(oes): %r" % bad
    import guarda_frases_v406 as GF
    bad2 = [(x["rota_id"], GF.violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if GF.violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad2, "a guarda das frases achou violacao(oes): %r" % bad2
    atrib = [(x["rota_id"], T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))]
    assert not atrib, "a direcao do testemunho esta invertida ou a atribuicao falhou: %r" % atrib
    ruins = regra_4_44(REG, z, p)
    assert not ruins, "a regra do 4,44 (o p calibrado e a linha dos 5 sigma no mesmo campo) falhou em: %r" % ruins[:3]
    assert c_seguem and c_q, "algum registro anterior (quadro, v405, v404, v403, falsidade, ponte, queda, esperanca, selo, declaracao, sonico, afinacao, rede de Fock, psibit, testemunha estatica) nao selou no core: o mapa nao registra a v406 assim"
    return REG


def gravar(p, b):
    """backup de BYTES se existir e mudar; temporario -> conferir tamanho -> substituir."""
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m406"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_m406"; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def main():
    V, PROB = L.ler()
    if PROB:
        print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); return 2
    NOS = L.NOS
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v406_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v406_*.json")), key=os.path.getmtime)
    arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto_selo_acom.json"), os.path.join(PK, "ESPERADOS_v406.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v406.json"),
            os.path.join(PK, "DIFF_KERNEL_v406.txt"), os.path.join(PK, "DIFF_v405_v406.diff"), os.path.join(NOS, "HANDOFF_v406_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v406.json"),
            os.path.join(PK, "kernel", "KERNEL_RECIBO_v406.json")] + sorted(glob.glob(os.path.join(PK, "pedra", "*.lean"))) + b3[-1:]
    arts = [x for x in arts if os.path.exists(x)]
    REG = montar(V, core, selo, ids_do_livro(), arts)
    J = os.path.join(HERE, "registro_mapa_v406.json")
    gravar(J, json.dumps(REG, ensure_ascii=False, indent=1).encode("utf-8"))
    quem = "claude-c1 (gerência), cadeia v406"
    print("registro MONTADO (NAO registrado): %d registro(s) (%s) -> %s" % (len(REG), ", ".join(x["tipo"] for x in REG), J))
    print("COMANDO (o passo 12 da cadeia o executa, uma vez so): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
    print("DEPOIS DO REGISTRO: os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
