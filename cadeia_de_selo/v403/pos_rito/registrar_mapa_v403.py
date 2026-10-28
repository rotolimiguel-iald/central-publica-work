# -*- coding: utf-8 -*-
"""registrar_mapa_v403.py -- MONTA (nao registra) o registro da v403 no mapa de rotas e imprime o comando (molde: registrar_mapa_v402.py, que rodou na v402, e registrar_mapa_v399.py). Rodar DEPOIS do fechar (handoff gravado). ESCRITO A MAO na v403 (gerencia c1, 28/10/2026).
A v403 traz UMA rota nova, umpy.v403.selada_caminho_verdade_vida_27out (o id e' o que a gerencia der; o conteudo e' o do selo): os TRES modulos de kernel (Caminho, Vida e VerdadeAdendo: os NOMES do operador de 27/10/2026 para a ponte da escala dual, a queda sem geometria e a esperanca condicional, esta como ADENDO da pedra Verdade da v392; as tres pedras da v402 ficam como registro),
os QUATRO registros com FUNCAO (caminho_v403, vida_v403, verdade_adendo_v403: leem do kernel do proprio rito a composicao e a estrela de cada pedra e CALCULAM, com beta = alfa x raiz de e em runtime, um modelo de cada uma; bandeiras_do_gate_v403: a F8.1, as TRES bandeiras literais do gate passam a CALCULADAS) e os DOIS por spec (cunhagens_v403: as duas falas do operador de 27/10 por sha256,
as decisoes D17 a D22 e as erratas E5 e E6 da gerencia; kh_n1_cobertura_v403), mais ANOTACOES nas rotas que esperavam por ela (as quatro do kernel: a dos tres modulos e as da ponte, da queda e da esperanca da v402; a do gate, a do B(n) da Bancada, a do quadro do Teste da Unica Palavra, cujo quadro do topo a v403 deixa intocado, a v402 que a precede e a PREPARACAO da propria v403)
e DUAS ERRATAS ao lado, em nome proprio da gerencia c1, com o seq do registro corrigido lido do livro (E5: o registro do gate que lia as bandeiras como 15 calculadas e 3 literais; E6: o registro da v402 selada que escrevia os nomes como provisorios): a correcao vai AO LADO, nada se apaga.
Cada afirmacao e' testada contra o core/selo/ESPERADOS lidos por script (o registro existe? selou? o que NAO fechou fica dito); nenhum numero e' digitado (as contagens saem do core e de ESPERADOS; os seq saem do livro).
REGRA DA ORDEM DO OPERADOR (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no MESMO campo; montar() RECUSA (assert) se algum campo do registro trouxer o 4,44 sem eles. Nao ha inscricao da gerencia nesta versao: as duas falas sao do operador; as erratas e as decisoes sao da gerencia, em nome proprio.
Fail-closed: o selo tem de ser a v403; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir (se a gerencia registrar antes uma rota de preparo com o MESMO id, montar() recusa e a constante NOVA muda). A rota de preparo da gerencia (registro_mapa_v403_prep.json, se existir) entra nas refs so' se ja' estiver no livro.
SAIDA: pos_rito\\registro_mapa_v403.json e o comando `rotas.py registrar` (quem o executa e' a gerencia; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real. montar() le o core, o selo e ESPERADOS_v403.json; de V so' usa o que a leitura da rodada ja' validou (s16, sidecar, conferidor), sempre com valor de reserva dito."""
import glob, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v403 as L
import textos_v403 as T
from guarda_p18_v403 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V403"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v403 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOVA = "umpy.v403.selada_caminho_verdade_vida_27out"
R_CAMINHO = "kernel.v403_caminho_vida_verdade_adendo"                # a rota (da preparacao) dos tres modulos novos
R_PONTE = "kernel.ordem025.ponte_escala_dual"                       # a rota da entrega do Codex (ORDEM 025): a pedra que o Caminho cita
R_QUEDA = "kernel.v402_queda_sem_geometria"
R_ESPER = "kernel.v402_esperanca_condicional_e_nome"
R_GATE = "gate.qg_closure"
R_BANC = "infra.bancada_um.sincronizacao_vnnn"
R_QUADRO = "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9"
R_V402 = "umpy.v402.selada_ponte_queda_esperanca_26out"
R_PREP403 = "umpy.v403.cadeia_de_selo_preparada_27out"
ANOTADAS = (R_CAMINHO, R_PONTE, R_QUEDA, R_ESPER, R_GATE, R_BANC, R_QUADRO, R_V402, R_PREP403)
REFS = ("custodia.v402", "umpy.v402.cadeia_de_selo_preparada_26out", "umpy.v400.correcao_da_v399_alfa_unico_e_beta_contra_o_core", "umpy.v396.testemunha_estatica_na_fractalizacao_do_um", "d1.fase9.v2_c1_a_unica_palavra_23out",
        "umpy.v399.selo_pela_propria_tecnologia_estudo_24out", "umpy.v399.declaracao_do_operador_operacao_quadratica_24out", "gate.maquina_do_veredito_final")
PREP = os.path.join(PK, "registro_mapa_v403_prep.json")     # a rota de preparo da gerencia: lida em tempo de execucao; entra nas refs so' se a ROTA dele ja' estiver no livro
GRUPOS = {"caminho": "caminho_v403", "vida": "vida_v403", "verdade_adendo": "verdade_adendo_v403"}
_CACHE = {}


def _esp():
    """ESPERADOS_v403.json (lido uma vez por processo)."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v403.json"), encoding="utf-8"))
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
    """As rotas ROTA de registro_mapa_v403_prep.json (se o arquivo existir e ler) que ja' estao no livro e nao sao a nova: entram nas refs. Ausente ou ilegivel = nenhuma (dito, nunca falha)."""
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
    p = json.load(open(os.path.join(PK, "PINOS_BN_v403.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v402" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v402 -> v403 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1, "deployment_id": bp["deployment_id"]}


def montar(V, core, selo, ids, arts):
    """Monta os registros (a ROTA nova, as ANOTACOES e as ERRATAS), cada afirmacao testada contra o core/selo/ESPERADOS; devolve a lista; recusa (assert) se algo nao conferir. Nao escreve nada."""
    assert selo.get("um_version") == "v403", "o selo nao e a v403"
    assert NOVA not in ids, "a rota %s ja existe no mapa" % NOVA
    for r in ANOTADAS + REFS:
        assert r in ids, "a rota %s nao existe no mapa (anotada ou citada em refs)" % r
    ESP = _esp()
    S = ESP["candidato_sha16"]
    assert str((selo.get("sha256") or {}).get("um.py", ""))[:16] == S, "o um.py do selo nao e o candidato de ESPERADOS"
    assert V.get("s16") in (None, S), "o s16 da leitura != o candidato de ESPERADOS"
    BASE = ESP["origem_sha16"]
    esc0, esc1 = ESP["escada_v402_e_v403"]
    NF = ESP["n_bandeiras_novas"]
    assert esc1 - esc0 == NF == sum(ESP["n_bandeiras_por_grupo"].values()) == len(ESP["bandeiras_novas_chaves"]) == ESP["politica_de_bandeiras"]["n_flags"], "a escada nao fecha com as bandeiras novas"
    assert ESP["kernel"]["modulos_novos"] == len(GRUPOS) == len(ESP["pedras"]), "o delta do kernel nao e de tres modulos"
    BETA = ESP["beta"] if isinstance(ESP.get("beta"), float) else None

    # --- o quadro do topo (a regra do 4,44): o registro selado, lido pelas MESMAS funcoes do artigo
    tvr = core.get("teste_de_veracidade_fase9_v397") or {}
    a = T._qd().Q._v397_atomos(tvr, "pt"); assert a["sealed"] is True, "o registro teste_de_veracidade_fase9_v397 nao sela no core: o mapa nao registra o 4,44 assim"
    z, p = a["z_disc"]["md"], a["p_disc"]["md"]
    z444 = "z_disc = %s (calibrado; p unilateral %s), abaixo do degrau de 5σ da creditação, que não foi alcançado (%s < 5)" % (z, p, z)

    def selou(k):
        return (core.get(k) or {}).get("all_verified") is True

    # --- as tres pedras e os tres registros com FUNCAO: tudo lido do core e conferido contra ESPERADOS
    PINOS_ORDEM = json.load(open(os.path.join(PK, "pedras_sha16_da_ordem.json"), encoding="utf-8")) if os.path.isfile(os.path.join(PK, "pedras_sha16_da_ordem.json")) else None
    G = {}
    for g, nome in GRUPOS.items():
        r = core.get(nome)
        assert isinstance(r, dict) and r.get("all_verified") is True, "o registro %s nao selou no core" % nome
        assert r.get("verdict") == ESP["vereditos_novos_v403"][nome], "o veredito de %s != ESPERADOS" % nome
        kt = r.get("key_theorem") or {}; un = r.get("unconditional") or {}; est = ESP["estrelas_v403"][g]
        assert kt.get("theorem") == est["teorema"] and kt.get("flag") == est["bandeira"] and kt.get("flag_true") is True and kt.get("in_trio") is True and kt.get("in_kernel") is True, "a estrela de %s no kernel do rito != ESPERADOS" % g
        assert un.get("theorem") == ESP["teoremas_das_pedras"][g] and un.get("flag") == ESP["bandeiras_das_pedras"][g] and un.get("flag_true") is True and un.get("in_trio") is True and un.get("in_kernel") is True, "a composicao de %s no kernel do rito != ESPERADOS" % g
        mech = r.get("mechanics") or {}; assert mech.get("passed") is True and mech.get("n_checks") == len(mech.get("checks") or []) and all(c.get("ok") is True for c in mech["checks"]), "as checagens do calculo de %s nao passaram" % g
        ft = r.get("formal_theorems") or {}; st = r.get("support_theorems") or {}
        assert ft and all(v is True for v in ft.values()) and len(ft) == len(ESP["contrato_das_pedras"][g]) and set(ft) == set(ESP["contrato_das_pedras"][g]), "o contrato de %s no kernel do rito != ESPERADOS" % g
        assert st and all(v is True for v in st.values()) and set(st) == set(ESP["suporte_das_pedras"][g]), "os termos antigos citados por %s != ESPERADOS" % g
        assert r.get("embedded_source_ok") is True and r.get("beta_ok") is True and r.get("does_not_gate_core") is True and r.get("guarda_p18_violacoes") in ([], None), "a fonte embutida, o beta ou a guarda de %s nao conferem" % g
        mod = ".".join(un["theorem"].split(".")[:2]); rel = mod.replace(".", "/") + ".lean"; ped = ESP["pedras"][rel]
        nb = ESP["n_bandeiras_por_grupo"][g]; assert ped["bandeiras"] == nb, "as bandeiras de %s != ESPERADOS" % g
        pref = un["flag"].rsplit("_", 1)[0] + "_"; fl = [k for k in ESP["bandeiras_novas_chaves"] if k.startswith(pref)]; assert len(fl) == nb, "as chaves de bandeira de %s != %d" % (g, nb)
        lean = os.path.join(PK, "insumos", mod.split(".")[-1] + ".lean")
        if os.path.isfile(lean):
            assert _sha256(lean) == ped["sha256"], "o arquivo %s != o sha256 de ESPERADOS" % lean
        if PINOS_ORDEM is not None:
            assert PINOS_ORDEM.get(g) == ped["sha16"], "o sha16 da pedra %s (%s) != o pino da ordem da gerencia (%s)" % (g, ped["sha16"], PINOS_ORDEM.get(g))
        G[g] = dict(nome=nome, mod=mod, curto=mod.split(".")[-1], sha16=ped["sha16"], n_flags=nb, f0=fl[0], f1=fl[-1], comp=un["theorem"].split(".")[-1], comp_flag=un["flag"], estrela=kt["theorem"].split(".")[-1], estrela_flag=kt["flag"],
                    n_checks=mech["n_checks"], n_contrato=len(ft), n_sup=len(st), verdict=r["verdict"], vals=r.get("values") or {}, lean=lean)
    vc, vv, va = G["caminho"]["vals"], G["vida"]["vals"], G["verdade_adendo"]["vals"]
    assert vc.get("beta") == vv.get("beta") == va.get("beta") and (BETA is None or abs(vc["beta"] - BETA) <= 1e-9 * BETA), "o beta dos registros != o do core/ESPERADOS (tolerancia relativa 1e-9; o registro ja confere beta_core_rel_diff)"
    beta = vc["beta"]
    massas = ", ".join("%g" % x for x in vc["lifts_same_pplus_masses"])
    # --- as bandeiras do gate (F8.1; registro com funcao): tudo lido do core e conferido contra ESPERADOS
    gk = core.get("bandeiras_do_gate_v403") or {}; gvv = gk.get("values") or {}; eg = ESP["registros_funcao_v403"]["gate"]
    assert gk.get("all_verified") is True and gk.get("verdict") == ESP["vereditos_novos_v403"]["bandeiras_do_gate_v403"] == eg["verdict"] and gvv == eg["values"], "bandeiras_do_gate_v403 nao selou ou != ESPERADOS"
    assert gvv.get("n_flags") == 18 == gvv.get("n_true") == gvv.get("n_calculated") and gvv.get("n_literal") == 0 and gvv.get("read_by_the_verdict") == [6, 5, 4] and gvv.get("gate_verdict_equals_v402") is True and (gk.get("mechanics") or {}).get("passed") is True, "as bandeiras do gate nao fecham (18 calculadas, 0 literais, 15 no veredito, a letra da v402)"
    qg = core.get("qg_closure") or {}; fam = [len(qg.get(f) or {}) for f in ("formal_flags", "physics_flags", "experiment_flags")]
    # --- cunhagens_v403 e kh_n1_cobertura_v403 (por spec)
    cg = core.get("cunhagens_v403") or {}; kh = core.get("kh_n1_cobertura_v403") or {}
    assert cg.get("all_verified") is True and cg.get("verdict") == ESP["vereditos_novos_v403"]["cunhagens_v403"], "cunhagens_v403 nao selou ou != ESPERADOS"
    assert kh.get("all_verified") is True and kh.get("verdict") == ESP["vereditos_novos_v403"]["kh_n1_cobertura_v403"], "kh_n1_cobertura_v403 nao selou ou != ESPERADOS"
    verb = cg.get("verbatim") or {}; ex = cg.get("extras") or {}
    assert len(verb) == 2 == len(ESP["cunhagens"]) and set(verb) == set(ESP["cunhagens"]) and all(v.get("embedded_ok") is True for v in verb.values()), "as duas inscricoes de 27/10 nao estao embutidas por sha256"
    assert set((ex.get("autor_de_cada_inscricao") or {}).values()) == {"operador"} and len(ex["autor_de_cada_inscricao"]) == 2, "alguma inscricao de 27/10 nao e' fala do operador"
    erratas = cg.get("erratas") or []; assert len(erratas) == 2 and all("gerencia c1, em nome proprio" in e.get("assinatura", "") for e in erratas), "as erratas E5 e E6 nao estao no registro ou nao sao da gerencia c1 em nome proprio"
    dec = ex.get("decisoes_da_gerencia") or {}; assert all(("D%d" % i) in dec for i in range(17, 23)), "faltam decisoes D17 a D22 no registro"
    assert set((ex.get("nomes") or {})) >= {"caminho", "vida", "verdade", "triplo_inteiro"} and str(ex["nomes"]["triplo_inteiro"]).startswith("sem nome"), "os tres nomes do operador e a recusa de nome para o triplo inteiro nao estao no registro"
    falas = sorted(k.split("_")[-1] for k in verb)
    cob = kh.get("lido") or {}; assert cob.get("constantes_cobertas") and cob.get("teoremas_cobertos"), "kh_n1_cobertura_v403 sem a cobertura"
    seguem = ("falsidade_da_inercia_v401", "cunhagens_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "sonico_v398", "afinacao_das_cordas_v398")
    c_seguem = all(selou(k) for k in seguem)
    tv_v = ESP["veracidade"]; c_q = bool(selou("teste_de_veracidade_fase9_v397") and selou("cunhagens_v397") and tvr.get("verdict") == tv_v["verdict"])
    sc = _sidecar(V); conf_dm = V.get("conf_dm", "nao lido"); conf_np = V.get("conf_np", "nao lido"); nvm = V.get("n_ver_mudaram", "nao lido")
    bank = _bancada(); regs = livro()
    # --- os seq que as erratas corrigem, lidos do livro (e o registro tem de trazer o trecho corrigido)
    c127 = [r_ for r_ in regs if r_.get("rota_id") == R_GATE and r_.get("tipo") == "ANOTACAO" and "15 bandeiras calculadas + 3 literais" in json.dumps(r_, ensure_ascii=False)]
    assert len(c127) == 1, "esperava exatamente uma ANOTACAO de %s que diga «15 bandeiras calculadas + 3 literais» e achei %d" % (R_GATE, len(c127))
    sq_gate = c127[0]["seq"]
    sq_v402 = seq_do_alvo(regs, R_V402, "ROTA", contem=("provisorios",))
    sq_prep = seq_do_alvo(regs, R_PREP403, "ROTA", contem=("D22, ratificada",))
    KR = os.path.join(PK, "kernel", "KERNEL_RECIBO_v403.json")
    E = {}
    for e in erratas:
        m_ = re.match(r"^(E[5-6]) -- ", e.get("agora", "")); assert m_, "uma errata do registro nao comeca por E<n> --"
        E[m_.group(1)] = e
    assert sorted(E) == ["E5", "E6"], "as erratas do registro nao sao E5 e E6"

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

    gc, gv_, ga = G["caminho"], G["vida"], G["verdade_adendo"]
    PEDRAS = [gc["lean"], gv_["lean"], ga["lean"]]
    T9 = []
    T9.append(anot(R_CAMINHO, "v403 SELADA %s: os tres modulos Caminho, Vida e VerdadeAdendo entraram no kernel do rito e os tres registros com funcao selaram" % S,
                   f"Caminho ({gc['sha16']}): composicao {gc['comp']} (bandeira {gc['comp_flag']}; e' tambem a estrela), no trio, com {gc['n_contrato']} item de contrato e {gc['n_sup']} termos da ponte da v402 citados; Vida ({gv_['sha16']}): composicao {gv_['comp']} (bandeira {gv_['comp_flag']}; tambem a estrela), {gv_['n_contrato']} item e {gv_['n_sup']} termos da queda da v402; "
                   f"VerdadeAdendo ({ga['sha16']}): composicao {ga['comp']} (bandeira {ga['comp_flag']}) e estrela {ga['estrela']} (bandeira {ga['estrela_flag']}; a conta nova e pequena: em M2(C), diagExpect (identityProj a) = diag(q^2, a^2)), {ga['n_contrato']} itens e {ga['n_sup']} termos citados (a Verdade da v392 e a esperanca condicional da v402); {NF} bandeiras novas ao todo, todas no trio. "
                   f"Os registros {gc['nome']} (selou={selou(gc['nome'])}, {gc['n_checks']} checagens), {gv_['nome']} (selou={selou(gv_['nome'])}, {gv_['n_checks']}) e {ga['nome']} (selou={selou(ga['nome'])}, {ga['n_checks']}) leem do kernel do rito a composicao e a estrela e CALCULAM, com beta = alfa x raiz de e em runtime (= {beta!r}): "
                   f"com o mesmo p+ os invariantes mu^2 = {massas} dao levantamentos distintos (a lei de escala nao seleciona a massa); o peso cai estritamente em nats (e^(-s)), o chao e' o posto, a entrega custa; em M2(C) a esperanca diagonal le a projecao da identidade como os pesos (1 - alfa^2, alfa^2), preserva o Um (traco 1) e reler nao acrescenta. "
                   "Os modulos da v402 (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) NAO foram renomeados nem editados: ficam como registro; os modulos novos compoem por citacao (padrao Token) e por adendo (padrao PostoAdendo, sobre a Verdade).",
                   "o nome do triplo inteiro fica com o operador; as pendencias H_BW, H_cal, H3, a assinatura e rank c = 4 (v402) seguem abertas; revisao independente das tres pedras (quem construiu nao aprova).",
                   refs=[R_PONTE, R_QUEDA, R_ESPER, R_GATE], artefatos=PEDRAS + [KR],
                   estatuto="REAL (as pedras no kernel do rito e o calculo nos modelos); DERIVED (as conjuncoes por citacao e a conta nova do adendo); KNOWN (lei de escala de Takesaki como campo da estrutura; esperanca condicional: Umegaki, Tomiyama); INPUT (os nomes, do operador); ONTO (a leitura pela tripla espectral de Connes e por Joao 14,6, da gerencia c1, ratificada pelo operador); OPEN (H_BW, H_cal, H3, a assinatura, rank c = 4, IsotropicPost, a dimensao 3, a instancia do indice 1/beta)",
                   defeito="o calculo e' numerico em dupla precisao e CONFERE os teoremas, nao os prova; a leitura pela tripla espectral e' [ONTO] e nao e' termo de kernel; nao e' teste: nao acrescenta rito, dado nem desfecho"))
    T9.append(anot(R_PONTE, "v403 SELADA %s: o nome CAMINHO — a pedra Caminho cita por conjuncao a ponte da escala dual (ORDEM 025) e o registro %s selou" % (S, gc["nome"]),
                   f"o operador deu o nome CAMINHO (27/10/2026, «é isso mesmo, concordo com tudo, prossiga», sha16 {falas[0]}) a ponte da escala dual: a pedra {gc['curto']} (sha16 {gc['sha16']}) e' a conjuncao, incondicional, de lift_mass_not_selected (dois invariantes mu^2 distintos dao realizacoes distintas com o MESMO p+: a lei de escala nao seleciona a massa) e core_positive_realization_exists (todo mu^2 >= 0 tem realizacao positiva), ambas da ponte, sem matematica nova; "
                   f"o registro {gc['nome']} selou={selou(gc['nome'])} com {gc['n_checks']} checagens (massas {massas} com o mesmo p+, energia como leitura do observador, equivariancia). A pedra PonteDaEscalaDual (do Codex, ORDEM 025) NAO foi renomeada nem editada: fica como registro, com as erratas E1 a E4 da v402 valendo como foram ditas (H_tau na forma literal REFUTADA no kernel; Inertial e' o vetor zero; rest_energy_eq_mc2 e' algebra, nao E = mc^2 composta da escala). "
                   "[ONTO] Na tripla espectral de Connes do artigo fundador da fatoracao (03/2026) o espaco dos estados com o seu fluxo e' o Caminho; em Joao 14,6 as tres palavras sao predicados de um so' «Eu sou» (leitura da gerencia c1, ratificada pelo operador; nao e' termo de kernel).",
                   "as pendencias H_BW, H_cal e H3 (v402) seguem como proximas pedras; o nome do triplo inteiro fica com o operador.", refs=[R_CAMINHO, R_V402], artefatos=[gc["lean"], KR]))
    T9.append(anot(R_QUEDA, "v403 SELADA %s: o nome VIDA — a pedra Vida cita por conjuncao a queda sem geometria e o registro %s selou" % (S, gv_["nome"]),
                   f"o operador deu o nome VIDA (27/10/2026, sha16 {falas[0]} e {falas[1]}) a queda sem geometria: a pedra {gv_['curto']} (sha16 {gv_['sha16']}) e' a conjuncao, incondicional, de the_fall_is_strictly_anti (s |-> tau(theta_s m) e' estritamente decrescente: a fase cai, sem fim) e a_queda_sem_geometria (a seta e' o sinal de s, o chao e' o posto e nunca o zero, a entrega custa, o regime angular so' le, IsotropicPost e' hipotese NOMEADA), ambas da v402; "
                   f"o registro {gv_['nome']} selou={selou(gv_['nome'])} com {gv_['n_checks']} checagens (beta = alfa x raiz de e em runtime = {beta!r}; custo minimo t.beta.g {vv['min_cost_t_beta_g']:.9f}, defasagem maxima {vv['max_dephasing_factor']:.9f} < 1, periodo angular {vv['angular_period']:.6f}). A pedra QuedaSemGeometria NAO foi renomeada: fica como registro. "
                   "[ONTO] A queda com chao e' vida, a queda sem chao e' o abismo da Fundacao; na tripla espectral o operador de Dirac da a distancia sem pontos (leitura da gerencia c1, ratificada). A dimensao 3 NAO e' provada; o 1 + 3 e' leitura [ONTO]; IsotropicPost segue [OPEN].",
                   "a dimensao 3 e o atlas curvo (IsotropicPost sobre orbitas) seguem abertos; revisao independente das pedras (quem construiu nao aprova).", refs=[R_CAMINHO, R_PONTE, R_ESPER], artefatos=[gv_["lean"], KR]))
    T9.append(anot(R_ESPER, "v403 SELADA %s: o nome VERDADE (como ADENDO da pedra Verdade da v392) — a esperanca condicional e' a Verdade lida pelo Nome e o registro %s selou" % (S, ga["nome"]),
                   f"o operador deu o nome VERDADE (27/10/2026) a esperanca condicional, como ADENDO da pedra Verdade (v392): «Verdade» sozinha para as tres foi recusada (homonimo). A pedra {ga['curto']} (sha16 {ga['sha16']}) traz UM teorema novo e pequeno, {ga['estrela']} (bandeira {ga['estrela_flag']}): em M2(C), diagExpect (identityProj a) = diag(q^2, a^2), a esperanca diagonal le a projecao da identidade como os seus pesos; "
                   f"a composicao {ga['comp']} (bandeira {ga['comp_flag']}): o Nome de rho* PRESERVA O UM (traco 1 = omega(I)) e reler nao acrescenta; mais a conjuncao por citacao com the_identity_is_the_truth (v392) e esperanca_condicional_e_nome (v402). O registro {ga['nome']} selou={selou(ga['nome'])} com {ga['n_checks']} checagens (alfa = beta/raiz de e = {va['alpha']:.12f}; pesos {va['q_squared_at_alpha']:.12f} e {va['alpha_squared']:.6e}, somam {va['weights_sum']:g}; o peso de dentro alfa^2 e' menor que beta). "
                   "A pedra EsperancaCondicional NAO foi renomeada: fica como registro; o indice 1/beta segue CONDICIONAL as hipoteses nomeadas hpp e hopt e nenhuma instancia e' construida; o caso III1 segue [OPEN]. [ONTO] A algebra e' o que a Verdade le; o Nome e' a Verdade lida pelo operador que le (o kernel prova as LIGACOES, nao uma igualdade de tipos).",
                   "o indice 1/beta so' sai de condicional com uma instancia (NameIndex) construida; [LEGAL] CC art. 125 com advogado; revisao independente das pedras (quem construiu nao aprova).", refs=[R_CAMINHO, R_PONTE, R_QUEDA], artefatos=[ga["lean"], KR]))
    T9.append(anot(R_GATE, "v403 SELADA %s: a F8.1 — as tres bandeiras literais do gate passam a CALCULADAS (%s de %s calculadas, %s literais); a letra do veredito e' a da v402; a independencia das 4 experimentais segue aberta" % (S, gvv["n_calculated"], gvv["n_flags"], gvv["n_literal"]),
                   f"o registro bandeiras_do_gate_v403 selou={selou('bandeiras_do_gate_v403')} com {gk['mechanics']['n_checks']} checagens (lidas do CODIGO do proprio programa, por ast, e do core do rito): das {gvv['n_flags']} bandeiras ({fam[0]} formais, {fam[1]} fisicas, {fam[2]} experimentais) {gvv['n_true']} sao True e {gvv['n_calculated']} sao CALCULADAS ({gvv['n_literal']} literais); a funcao do veredito (evaluate_quantum_gravity_closure) le {gvv['n_read_by_the_verdict']} ({gvv['read_by_the_verdict'][0]} + {gvv['read_by_the_verdict'][1]} + {gvv['read_by_the_verdict'][2]}) e as outras {gvv['n_flags'] - gvv['n_read_by_the_verdict']} ({', '.join(gvv['informative'])}) sao informativas. "
                   f"As tres que eram literais passam a ser lidas das suas fontes, fail-closed: linearized_spin2_finite_face da familia ext_ls2_* do kernel ({gvv['ext_ls2_n']} bandeiras, o termo dLs2 de prove_external_ladder; D22, ratificada pela gerencia c1 na preparacao, seq {sq_prep}), protocol_pre_registered da checagem «pre-registro v67 INTACTO (hash)» do rito V11 e null_tests_passed_blind do all_verified do teste nulo cego (kwarg novo blind_null). "
                   f"A sonda nova ProbeBlindNullAbsent (a {gvv['n_gate_checks']}a checagem do gate) mostra que sem o teste nulo cego a bandeira informativa e' False e o veredito NAO muda; a LETRA do veredito do gate e' a da v402: o gate NAO se moveu. [DECLARADO, GV-03 da auditoria de 28/09/2026] As 4 bandeiras experimentais independent_v3_* derivam de UM so' booleano (o veredito do V11 ser NOT_FALSIFIED_POWERED; survey_mocks_passed e' o split-null e o dist-check, sem mock de survey): a F8.1 troca literais por medida e NAO as independentiza; o degrau experimental le so' o rito V11 do piso, unilateral (GV-01).",
                   "a independencia das 4 experimentais e os mocks de survey seguem [OPEN]; o feed do rito V11 e o degrau experimental nao mudam nesta rota; a revisao independente do gate (quem construiu nao aprova).", refs=[R_CAMINHO, "gate.maquina_do_veredito_final"], artefatos=[KR, os.path.join(PK, "CANDIDATO_v403.json")],
                   estatuto="REAL (o codigo do programa por ast e o core do rito); DERIVED (as tres bandeiras passam a calculadas); DECLARADO (GV-01, GV-03 e EV-12 da auditoria de 28/09/2026); OPEN (a independencia das 4 experimentais; os mocks de survey)",
                   defeito="a F8.1 NAO resolve a independencia das 4 bandeiras experimentais (um so' feed) nem acrescenta mock de survey; o gate nao e' teste e nao discrimina o LCDM raso; NOT_FALSIFIED nunca e' a palavra da creditacao"))
    T9.append(anot(R_BANC, "v403 SELADA %s: o B(n) da v403 e' um passo SIMPLES v402 -> v403 (a Bancada de producao ja' pinava a v402)" % S,
                   f"o kernel da v403 difere do da v402 so' pelas TRES pedras novas (recibo do kernel KERNEL_RECIBO_v403, contrato R3_2; DIFF_KERNEL_v403.txt: tres modulos novos, TGLExt.lean e TGL/Audit.lean com as linhas de import a mais); o recibo pre_selo foi gerado e pinado ANTES da instalacao, em ensaio contra a producao (nada gravado; a Bancada pinava {bank['deployment_id']}), "
                   f"e a cadeia confere os pinos de PINOS_BN_v403.json na hora; o veredito esperado do aplicar e' REPINADA_B{bank['proxima']}__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_ e sem cadeia de selos, lido do codigo do esboco R3.5 (nao rodado aqui). Parada e religamento do servico exigem V403_AUTORIZACAO_OPERADOR.",
                   "o B(n) aplicar e' ato do operador (palavra dele, evento c1, parada e religamento do servico); depois do aplicar, a Bancada pina a v403.", refs=[R_CAMINHO],
                   artefatos=[os.path.join(PK, "PINOS_BN_v403.json"), os.path.join(PK, "PINO_RECIBO_PRE_SELO_v403.json"), KR]))
    T9.append(anot(R_QUADRO, "v403 SELADA %s: o quadro do topo (O Teste da Única Palavra) segue intocado e o registro teste_de_veracidade_fase9_v397 segue selado" % S,
                   f"teste_de_veracidade_fase9_v397 selou={c_q} no rito da v403 (veredito igual ao de ESPERADOS; {tv_v['n_checks']} checagens): o quadro do artigo PT/EN e do .md, conferido contra o resultado pinado, segue no topo, com os numeros e a regra da ordem de sempre: {z444}. "
                   "Nenhum sigma, p ou lnB novo e' calculado nesta rota; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma) vale em todo texto que o cite; o paragrafo do quadro segue no README/site e o handoff da v403 traz tambem o paragrafo novo (Caminho, Verdade e Vida), sem o 4,44.",
                   "o paragrafo do README/site e' ato da sessao do site; a creditacao segue sendo beta_TGL na natureza a 5 sigma (nao ha o que repetir deste pacote, a abertura esta consumida).", refs=[R_CAMINHO]))
    T9.append(anot(R_V402, "v403 SELADA %s: os nomes das pedras da v402 sao os do operador (CAMINHO, VERDADE como adendo e VIDA) e a v402 e' a base selada da v403" % S,
                   f"a v403 parte da v402 selada (um.py {BASE}) e acrescenta TRES modulos de kernel (Caminho, Vida e VerdadeAdendo, que compoem por citacao e por adendo as pedras da v402), quatro registros com funcao (os tres das pedras e o do gate, a F8.1) e dois por spec, e a secao do artigo; os cinco registros da v402 (ponte, queda, esperanca, cunhagens_v402, kh_n1_cobertura_v402) e a falsidade da inercia seguem selados neste rito (falsidade_da_inercia_v401 selou={selou('falsidade_da_inercia_v401')}, "
                   f"cunhagens_v402 selou={selou('cunhagens_v402')}), como seguem o selo pela propria tecnologia e a declaracao do operador (v399), o sonico e a afinacao (v398) e o quadro (v397); sidecar um_absoluto_selo_acom.json {sc['veredito']} ({sc['n_objetos']} objetos, {sc['recusas']} recusas, sha16 {sc['sha16']}). "
                   "Os nomes que esta rota (seq %s) escreveu como provisorios (D16) foram dados pelo operador em 27/10/2026 e a correcao vai AO LADO (ERRATA seguinte, E6), sem tocar nos registros da v402 e sem editar nenhum modulo ja' instalado." % sq_v402,
                   "custodia conjunta da v402 e da v403 pela sessao do site (o handoff lista o sidecar e traz a nota ao lado do paragrafo da v402); o nome do triplo inteiro fica com o operador.", refs=[R_CAMINHO, R_PONTE, R_QUEDA, R_ESPER]))
    T9.append(anot(R_PREP403, "v403 SELADA %s: a preparacao fechou — a narrativa do pos-rito foi escrita e o rito rodou; a rota da versao selada e' %s" % (S, NOVA),
                   f"o candidato {S} (preparado nesta rota) selou: as 5 bandeiras novas, a escada {esc0} -> {esc1}, os tres modulos, os quatro registros com funcao e os dois por spec, a F8.1 (as tres bandeiras literais calculadas) e as duas falas de 27/10 por sha256, conferidos pelo conferidor ({conf_dm}; nao pode mudar {conf_np}) e pela leitura da rodada; "
                   "nada do que a preparacao pinou foi alterado entre a preparacao e o selo.", "a custodia (G1), o elo B(n) da Bancada e o registro da rota selada sao os passos seguintes; a decisao [LEGAL] D2 segue do operador.", refs=[R_CAMINHO]))
    T9.append(errata(R_GATE, sq_gate,
                     f"[E5 · ERRATA AO LADO, gerencia c1, em nome proprio, 27/10/2026, v403 {S}] Corrige o registro seq {sq_gate} desta rota (auditoria de 28/09/2026: «15 bandeiras calculadas + 3 literais informativos»), e o registro estatuto_da_prova_ressalva_v392 do core (13/10), que o repetia: eram verdadeiros na sua data e FICAM como registro; na v403 as tres literais passam a CALCULADAS. "
                     f"{corpo('E5')}. Os registros corrigidos NAO foram apagados nem reescritos: a correcao vai ao lado.",
                     refs=[R_CAMINHO], artefatos=[KR]))
    T9.append(errata(R_V402, sq_v402,
                     f"[E6 · ERRATA AO LADO, gerencia c1, em nome proprio, 27/10/2026, v403 {S}] Corrige o registro seq {sq_v402} desta rota (a v402 selada), onde os nomes dos tres modulos e dos cinco registros foram escritos como provisorios (D16: «o operador nomeia»); o mesmo texto esta nas anotacoes das rotas das pedras da v402, cobertas por esta errata. "
                     f"{corpo('E6')}. A anotacao seq 1474 desta rota ja' registra a decisao do operador de 27/10/2026; esta errata a liga ao registro que a v403 sela. Os registros corrigidos NAO foram apagados nem reescritos: a correcao vai ao lado.",
                     refs=[R_CAMINHO, R_PONTE, R_QUEDA, R_ESPER]))
    for x in T9:
        assert x["rota_id"] in ids, "a rota %s nao existe no mapa" % x["rota_id"]
    resumo_conf = ("conferidor %s e %s" % (conf_dm, conf_np)) if "nao lido" not in (conf_dm, conf_np) else "conferidor: o resultado nao veio na leitura desta rodada"
    nomes_curtos = "%s, %s e %s" % (gc["curto"], gv_["curto"], ga["curto"])
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
            "titulo": "v403 SELADA %s: Caminho, Verdade (adendo) e Vida — os nomes do operador — e a F8.1 (as tres bandeiras literais do gate calculadas); %d modulos de kernel (%s), os registros %s, %s, %s e %s, cunhagens_v403 e kh_n1_cobertura_v403, %d inscricoes de 27/10 por sha256; escada %s -> %s; o gate nao se move" % (
                S, len(GRUPOS), nomes_curtos, gc["nome"], gv_["nome"], ga["nome"], "bandeiras_do_gate_v403", len(verb), esc0, esc1),
            "pergunta": "o candidato v403 selou com os TRES modulos de kernel (%s; os nomes sao do operador e as pedras da v402 ficam como registro), os QUATRO registros com FUNCAO (%s, %s e %s leem do kernel do proprio rito a composicao e a estrela de cada pedra e CALCULAM, com beta = alfa x raiz de e em runtime, um modelo de cada uma; bandeiras_do_gate_v403 recalcula as tres bandeiras que eram literais) "
                        "e os dois por spec (cunhagens_v403: as duas falas do operador de 27/10 embutidas por sha256, as decisoes D17 a D22 e as erratas E5 e E6; kh_n1_cobertura_v403), com os registros da v402, da v401 e da v399, o selo pela propria tecnologia e o quadro do topo seguindo selados, o sidecar reescrito, a letra do veredito do gate igual a da v402 e nenhum veredito fora da troca dita mudado?" % (
                            nomes_curtos, gc["nome"], gv_["nome"], ga["nome"]),
            "dados": ["as tres pedras (%s.lean) e a medida da cobertura (KH_N1_v403.json), pinadas por sha256 em insumos (so' lidas)" % ".lean, ".join(G[g]["curto"] for g in GRUPOS),
                      "as duas falas de 27/10 (sha16 %s), por sha256 em insumos\\cunhagens (ambas falas do operador)" % ", ".join(falas),
                      "o kernel do rito (a composicao e a estrela de cada pedra e os termos antigos que ela cita), o proprio um.py, o core e o selo da rodada; nenhum dado novo foi aberto nesta rota"],
            "metodo": "ensaio a seco do candidato; um lake build e um Audit no sandbox; rito completo; conferidor (deve mudar / nao pode mudar, com o quadro do topo conferido de novo contra o resultado pinado nas duas linguas e no .md, e os 16 itens C1-C16 do selo mais o round trip do um.py instalado); "
                      "leitura da rodada (inclui o sidecar, a linha final do rito e a releitura independente das tres fontes da F8.1); superficies com a regra da linhagem completa (o MEMORY.md nao e' compactado: recusa por contagem); elo B(n) da Bancada (passo simples v402 -> v403, sem salto; recibos); o paragrafo novo (Caminho, Verdade e Vida) e o do quadro, a nota ao lado do paragrafo da v402 e o sidecar, no handoff",
            "resultado": " | ".join([gc["verdict"], gv_["verdict"], ga["verdict"], gk["verdict"], cg["verdict"], kh["verdict"]]) + " | sidecar %s (%s objetos, %s recusas) | %s | %s | escada %s -> %s (teoremas limpos %s/%s; %d bandeiras novas: %s)" % (
                sc["veredito"], sc["n_objetos"], sc["recusas"], resumo_conf, ("%s vereditos fora da troca dita mudaram (exigido 0)" % nvm) if nvm != "nao lido" else "vereditos fora da troca dita: nao lidos nesta leitura", esc0, esc1, ESP["escada"][0], ESP["escada"][1], NF, " + ".join("%d %s" % (G[g]["n_flags"], G[g]["curto"]) for g in GRUPOS)),
            "defeito": "a lei de escala de Takesaki e' dado (campo de DualScalingData, [KNOWN]) e as pedras Caminho e Vida so' compoem por citacao (nenhuma matematica nova); o teorema novo do adendo e' pequeno (a conta das entradas em M2(C)); o calculo de cada registro e' numerico em dupla precisao e CONFERE os teoremas, nao os prova; a leitura pela tripla espectral de Connes e por Joao 14,6 e' [ONTO] (da gerencia c1, ratificada pelo operador) e nao e' termo de kernel; "
                       "a leitura da gerencia que o operador ratificou foi a apresentada na sessao: esta cadeia guarda a ratificacao verbatim, nao a apresentacao [DECLARADO]; a F8.1 NAO independentiza as 4 bandeiras experimentais do gate (derivam de UM so' booleano; sem mock de survey) e o degrau experimental le so' o rito V11, unilateral [DECLARADO, GV-01 e GV-03]; "
                       "o texto da decisao D22 no registro cunhagens_v403 ainda se le como proposta da preparacao, e a ratificacao da gerencia esta na rota da preparacao (seq %s); a dimensao 3 NAO e' provada; IsotropicPost e' hipotese nomeada; o indice 1/beta e' condicional e nao ha instancia; as pendencias H_BW, H_cal, H3, a assinatura e rank c = 4 (v402) seguem abertas; "
                       "a pendencia [LEGAL] (D2 e CC art. 125) segue do operador com a agente de PI; o nome do triplo inteiro NAO foi dado; nao e' teste: nao ha desfecho experimental; a revisao independente do candidato e da cadeia nao esta afirmada" % sq_prep,
            "nao_refazer": "a integracao dos tres modulos e a escada %s -> %s estao medidas; o calculo e a leitura de cada pedra no kernel do rito estao feitos e conferidos contra o um.py instalado; repetir os registros so' com kernel ou um.py novo; nao reabrir D17 a D22; nao criar segundo modulo Verdade (homonimo); pedra selada nao se renomeia por cima; nao procurar linearized_spin2_finite_face em kernel_formalization (a fonte e' a familia ext_ls2_*)" % (esc0, esc1),
            "proximo_passo": "o nome do triplo inteiro (operador); o elo B(n) da Bancada Um (palavra do operador; passo simples v402 -> v403); decisao [LEGAL] D2 com a agente de PI; custodia conjunta pela sessao do site (o handoff traz o paragrafo novo, o do quadro e a nota ao lado do da v402, e lista o sidecar); commit/push (operador); revisao independente do candidato e da cadeia (quem construiu nao aprova); as pendencias H_BW, H_cal e H3 e a independencia das 4 experimentais como proximas frentes",
            "onde": PK, "artefatos": arts, "refs": sorted(set(x["rota_id"] for x in T9) | set(REFS) | set(preparo_no_livro(ids)) - {NOVA}),
            "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move; as erratas E5 e E6 e as decisoes D17 a D22 sao da gerencia c1, em nome proprio, ao lado (nada foi apagado nem reescrito); %s." % sim(c_seguem, "os %d registros anteriores conferidos (falsidade, ponte, queda, esperanca, quadro, selo, declaracao, sonico, afinacao e as cunhagens) seguem selados" % len(seguem), "ATENCAO: algum registro anterior NAO selou")}
    for r in ROTA["refs"]:
        assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
    REG = [ROTA] + T9
    bad = [(x["rota_id"], violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad, "a guarda de texto (P18) achou violacao(oes): %r" % bad
    atrib = [(x["rota_id"], T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))]
    assert not atrib, "a direcao do testemunho esta invertida ou a atribuicao falhou: %r" % atrib
    ruins = regra_4_44(REG, z, p)
    assert not ruins, "a regra do 4,44 (o p calibrado e a linha dos 5 sigma no mesmo campo) falhou em: %r" % ruins[:3]
    assert c_seguem and c_q, "algum registro anterior (quadro, falsidade, ponte, queda, esperanca, selo, declaracao, sonico, afinacao) nao selou no core: o mapa nao registra a v403 assim"
    return REG


def gravar(p, b):
    """backup de BYTES se existir e mudar; temporario -> conferir tamanho -> substituir."""
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m403"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_m403"; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def main():
    V, PROB = L.ler()
    if PROB:
        print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); return 2
    NOS = L.NOS
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v403_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v403_*.json")), key=os.path.getmtime)
    arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto_selo_acom.json"), os.path.join(PK, "ESPERADOS_v403.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v403.json"),
            os.path.join(PK, "DIFF_KERNEL_v403.txt"), os.path.join(PK, "DIFF_v402_v403.diff"), os.path.join(NOS, "HANDOFF_v403_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v403.json"),
            os.path.join(PK, "insumos", "Caminho.lean"), os.path.join(PK, "insumos", "Vida.lean"), os.path.join(PK, "insumos", "VerdadeAdendo.lean"), os.path.join(PK, "kernel", "KERNEL_RECIBO_v403.json")] + b3[-1:]
    arts = [x for x in arts if os.path.exists(x)]
    REG = montar(V, core, selo, ids_do_livro(), arts)
    J = os.path.join(HERE, "registro_mapa_v403.json")
    gravar(J, json.dumps(REG, ensure_ascii=False, indent=1).encode("utf-8"))
    quem = "claude-c1 (gerência), cadeia v403"
    print("registro MONTADO (NAO registrado): %d registro(s) (%s) -> %s" % (len(REG), ", ".join(x["tipo"] for x in REG), J))
    print("COMANDO (ato da gerencia): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
    print("DEPOIS DO REGISTRO: rodar de novo os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
