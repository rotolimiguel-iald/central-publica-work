# -*- coding: utf-8 -*-
"""registrar_mapa_v402.py -- MONTA (nao registra) o registro da v402 no mapa de rotas e imprime o comando (molde: registrar_mapa_v401.py, que rodou na v401, e registrar_mapa_v399.py). Rodar DEPOIS do fechar (handoff gravado). ESCRITO A MAO na v402 (agente A2 da preparacao, 26/10/2026).
A v402 traz UMA rota nova, umpy.v402.selada_ponte_queda_esperanca_26out (o id e' o que a gerencia der; o conteudo e' o do selo): os TRES modulos de kernel (PonteDaEscalaDual, do Codex, ORDEM 025, copia de bytes; QuedaSemGeometria; EsperancaCondicional; os tres nomes sao PROVISORIOS, o operador nomeia),
os TRES registros com FUNCAO (ponte_da_escala_dual_v402, queda_sem_geometria_v402, esperanca_condicional_v402: leem do kernel do proprio rito a composicao e a estrela de cada pedra e CALCULAM, com beta = alfa x raiz de e em runtime, um modelo de cada uma) e os DOIS por spec (cunhagens_v402: as tres inscricoes do operador
de 26/10 por sha256, as decisoes D11 a D16 da gerencia e as erratas E1 a E4 da integracao da ponte; kh_n1_cobertura_v402), mais ANOTACOES nas rotas que esperavam por ela (as tres rotas do kernel das pedras, a do B(n) da Bancada, a do quadro do Teste da Unica Palavra, cujo quadro do topo a v402 deixa intocado, e a v401 que a precede)
e TRES ERRATAS ao lado, em nome proprio da gerencia c1, com o seq do registro corrigido lido do livro (E1: a forma literal de H_tau da v401, nos registros seq da rota selada e da anotacao da pedra; E2 a E4: a entrega da ORDEM 025 como foi registrada): a correcao vai AO LADO, nada se apaga.
Cada afirmacao e' testada contra o core/selo/ESPERADOS lidos por script (o registro existe? selou? o que NAO fechou fica dito); nenhum numero e' digitado (as contagens saem do core e de ESPERADOS; os seq saem do livro).
REGRA DA ORDEM DO OPERADOR (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no MESMO campo; montar() RECUSA (assert) se algum campo do registro trouxer o 4,44 sem eles. Nao ha inscricao da gerencia nesta versao: as tres falas sao do operador; as erratas e as decisoes sao da gerencia, em nome proprio.
Fail-closed: o selo tem de ser a v402; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir (se a gerencia registrar antes uma rota de preparo com o MESMO id, montar() recusa e a constante NOVA muda). A rota de preparo da gerencia (registro_mapa_v402_prep.json, se existir) entra nas refs so' se ja' estiver no livro.
SAIDA: pos_rito\\registro_mapa_v402.json e o comando `rotas.py registrar` (quem o executa e' a gerencia; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real. montar() le o core, o selo e ESPERADOS_v402.json; de V so' usa o que a leitura da rodada ja' validou (s16, sidecar, conferidor), sempre com valor de reserva dito."""
import glob, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v402 as L
import textos_v402 as T
from guarda_p18_v402 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V402"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v402 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOVA = "umpy.v402.selada_ponte_queda_esperanca_26out"
R_PONTE = "kernel.ordem025.ponte_escala_dual"                       # a rota da entrega do Codex (ORDEM 025): o consultar «ponte da escala dual» nao devolve nada, o consultar «ordem025» a devolve
R_QUEDA = "kernel.v402_queda_sem_geometria"
R_ESPER = "kernel.v402_esperanca_condicional_e_nome"
R_BANC = "infra.bancada_um.sincronizacao_vnnn"
R_QUADRO = "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9"
R_V401 = "umpy.v401.selada_falsidade_da_inercia_25out"
R_PEDRA401 = "kernel.v401_falsidade_da_inercia"
R_PREP401 = "umpy.v401.cadeia_de_selo_preparada_25out"
ANOTADAS = (R_PONTE, R_QUEDA, R_ESPER, R_BANC, R_QUADRO, R_V401, R_PEDRA401)
REFS = (R_PREP401, "custodia.v401", "umpy.v400.correcao_da_v399_alfa_unico_e_beta_contra_o_core", "umpy.v396.testemunha_estatica_na_fractalizacao_do_um", "d1.fase9.v2_c1_a_unica_palavra_23out",
        "umpy.v399.selo_pela_propria_tecnologia_estudo_24out", "umpy.v399.declaracao_do_operador_operacao_quadratica_24out")
PREP = os.path.join(PK, "registro_mapa_v402_prep.json")     # a rota de preparo da gerencia: lida em tempo de execucao; entra nas refs so' se a ROTA dele ja' estiver no livro
GRUPOS = {"ponte": "ponte_da_escala_dual_v402", "queda": "queda_sem_geometria_v402", "esperanca": "esperanca_condicional_v402"}
_CACHE = {}


def _esp():
    """ESPERADOS_v402.json (lido uma vez por processo)."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v402.json"), encoding="utf-8"))
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
    """As rotas ROTA de registro_mapa_v402_prep.json (se o arquivo existir e ler) que ja' estao no livro e nao sao a nova: entram nas refs. Ausente ou ilegivel = nenhuma (dito, nunca falha)."""
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
    p = json.load(open(os.path.join(PK, "PINOS_BN_v402.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v401" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v401 -> v402 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1, "deployment_id": bp["deployment_id"]}


def montar(V, core, selo, ids, arts):
    """Monta os registros (a ROTA nova, as ANOTACOES e as ERRATAS), cada afirmacao testada contra o core/selo/ESPERADOS; devolve a lista; recusa (assert) se algo nao conferir. Nao escreve nada."""
    assert selo.get("um_version") == "v402", "o selo nao e a v402"
    assert NOVA not in ids, "a rota %s ja existe no mapa" % NOVA
    for r in ANOTADAS + REFS:
        assert r in ids, "a rota %s nao existe no mapa (anotada ou citada em refs)" % r
    ESP = _esp()
    S = ESP["candidato_sha16"]
    assert str((selo.get("sha256") or {}).get("um.py", ""))[:16] == S, "o um.py do selo nao e o candidato de ESPERADOS"
    assert V.get("s16") in (None, S), "o s16 da leitura != o candidato de ESPERADOS"
    BASE = ESP["origem_sha16"]
    esc0, esc1 = ESP["escada_v401_e_v402"]
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
    CODEX_PONTE = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_025", "PonteDaEscalaDual.lean")
    G = {}
    for g, nome in GRUPOS.items():
        r = core.get(nome)
        assert isinstance(r, dict) and r.get("all_verified") is True, "o registro %s nao selou no core" % nome
        assert r.get("verdict") == ESP["vereditos_novos_v402"][nome], "o veredito de %s != ESPERADOS" % nome
        kt = r.get("key_theorem") or {}; un = r.get("unconditional") or {}; est = ESP["estrelas_v402"][g]
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
        if g == "ponte" and os.path.isfile(CODEX_PONTE):
            assert _sha256(CODEX_PONTE) == ped["sha256"], "a pedra da ponte != o arquivo da entrega do Codex (ORDEM 025): nao e' copia de bytes"
        G[g] = dict(nome=nome, mod=mod, curto=mod.split(".")[-1], sha16=ped["sha16"], n_flags=nb, f0=fl[0], f1=fl[-1], comp=un["theorem"].split(".")[-1], comp_flag=un["flag"], estrela=kt["theorem"].split(".")[-1], estrela_flag=kt["flag"],
                    n_checks=mech["n_checks"], n_contrato=len(ft), n_sup=len(st), verdict=r["verdict"], vals=r.get("values") or {}, lean=lean)
    vp, vq, ve = G["ponte"]["vals"], G["queda"]["vals"], G["esperanca"]["vals"]
    assert vp.get("beta") == vq.get("beta") == ve.get("beta") and (BETA is None or abs(vp["beta"] - BETA) <= 1e-9 * BETA), "o beta dos registros != o do core/ESPERADOS (tolerancia relativa 1e-9; o registro ja confere beta_core_rel_diff)"
    beta = vp["beta"]
    massas = ", ".join("%g" % x for x in vp["lifts_same_pplus_masses"])
    # --- cunhagens_v402 e kh_n1_cobertura_v402 (por spec)
    cg = core.get("cunhagens_v402") or {}; kh = core.get("kh_n1_cobertura_v402") or {}
    assert cg.get("all_verified") is True and cg.get("verdict") == ESP["vereditos_novos_v402"]["cunhagens_v402"], "cunhagens_v402 nao selou ou != ESPERADOS"
    assert kh.get("all_verified") is True and kh.get("verdict") == ESP["vereditos_novos_v402"]["kh_n1_cobertura_v402"], "kh_n1_cobertura_v402 nao selou ou != ESPERADOS"
    verb = cg.get("verbatim") or {}; ex = cg.get("extras") or {}
    assert len(verb) == 3 == len(ESP["cunhagens"]) and set(verb) == set(ESP["cunhagens"]) and all(v.get("embedded_ok") is True for v in verb.values()), "as tres inscricoes de 26/10 nao estao embutidas por sha256"
    assert set((ex.get("autor_de_cada_inscricao") or {}).values()) == {"operador"} and len(ex["autor_de_cada_inscricao"]) == 3, "alguma inscricao de 26/10 nao e' fala do operador"
    erratas = cg.get("erratas") or []; assert len(erratas) == 4 and all("gerencia c1, em nome proprio" in e.get("assinatura", "") for e in erratas), "as erratas E1 a E4 nao estao no registro ou nao sao da gerencia c1 em nome proprio"
    dec = ex.get("decisoes_da_gerencia") or {}; assert all(("D%d" % i) in dec for i in range(11, 17)), "faltam decisoes D11 a D16 no registro"
    falas = sorted(k.split("_")[-1] for k in verb)
    cob = kh.get("lido") or {}; assert cob.get("constantes_cobertas") and cob.get("teoremas_cobertos"), "kh_n1_cobertura_v402 sem a cobertura"
    seguem = ("falsidade_da_inercia_v401", "cunhagens_v401", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "sonico_v398", "afinacao_das_cordas_v398")
    c_seguem = all(selou(k) for k in seguem)
    tv_v = ESP["veracidade"]; c_q = bool(selou("teste_de_veracidade_fase9_v397") and selou("cunhagens_v397") and tvr.get("verdict") == tv_v["verdict"])
    sc = _sidecar(V); conf_dm = V.get("conf_dm", "nao lido"); conf_np = V.get("conf_np", "nao lido"); nvm = V.get("n_ver_mudaram", "nao lido")
    bank = _bancada(); regs = livro()
    # --- os seq que as erratas corrigem, lidos do livro (e o registro tem de trazer o trecho corrigido)
    sq_v401 = seq_do_alvo(regs, R_V401, "ROTA", contem=("H_tau",))
    sq_ped401 = seq_do_alvo(regs, R_PEDRA401, "ANOTACAO", "v401 SELADA", contem=("H_tau",))
    sq_prep_r = seq_do_alvo(regs, R_PREP401, "ROTA", contem=("H_tau",))
    sq_prep_a = seq_do_alvo(regs, R_PEDRA401, "ANOTACAO", "A pedra FalsidadeDaInercia foi ESTENDIDA", contem=("H_tau",))
    sq_ponte = seq_do_alvo(regs, R_PONTE, "ROTA", contem=("EXIT0",))
    EX25 = os.path.join(os.path.dirname(PK), "v402_exame", "ordem_025")
    KR = os.path.join(PK, "kernel", "KERNEL_RECIBO_v402.json")
    E = {}
    for e in erratas:
        m_ = re.match(r"^(E[1-4]) -- ", e.get("agora", "")); assert m_, "uma errata do registro nao comeca por E<n> --"
        E[m_.group(1)] = e
    assert sorted(E) == ["E1", "E2", "E3", "E4"], "as erratas do registro nao sao E1 a E4"

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

    gp, gq, ge = G["ponte"], G["queda"], G["esperanca"]
    T9 = []
    T9.append(anot(R_PONTE, "v402 SELADA %s: a ponte da escala dual (ORDEM 025 do Codex) entrou no kernel do rito, byte a byte, e o registro %s selou" % (S, gp["nome"]),
                   f"pedra {gp['curto']} no kernel do rito = {sim(selou(gp['nome']), 'CONFERE', 'NAO CONFERE')}: composicao incondicional {gp['comp']} (bandeira {gp['comp_flag']}; a realizacao positiva no nucleo canonico existe para todo mu^2 >= 0) e estrela {gp['estrela']} (bandeira {gp['estrela_flag']}; dois invariantes mu^2 distintos dao realizacoes equivariantes distintas com o MESMO p+: a lei de escala nao seleciona a massa), "
                   f"no trio, com {gp['n_contrato']} declaracoes no contrato e {gp['n_sup']} termos antigos que ela cita (todos no trio); {gp['n_flags']} bandeiras novas (de {gp['f0']} a {gp['f1']}); sha16 do modulo {gp['sha16']} (igual ao arquivo da entrega do Codex, ORDEM 025, byte a byte, e ao pino da ordem da gerencia). "
                   f"O registro {gp['nome']} selou={selou(gp['nome'])} com {gp['n_checks']} checagens do calculo no modelo longitudinal (E, p), c = 1, com beta = alfa x raiz de e em runtime (= {beta!r}): p+ escala por e^(-s) e p- por e^(+s); m^2 = p+ p- e' o invariante do boost; a energia e' a LEITURA e muda com o observador; "
                   f"os invariantes mu^2 = {massas} com o MESMO p+ dao levantamentos distintos; um peso positivo que escala por e^(-s) nunca e' invariante. [DERIVED] a realizacao explicita da lei de escala como acao do boost; a lei de Takesaki e' campo da estrutura, [KNOWN]. "
                   f"ERRATAS ao lado (gerencia c1, em nome proprio, 26/10/2026; registradas na ERRATA seguinte desta rota): E1 a forma literal de H_tau e' REFUTADA no kernel; E2 Inertial e' o vetor zero; E3 rest_energy_eq_mc2 e' algebra, nao E = mc^2 composta da escala; E4 a proveniencia da entrega. "
                   "Pendencias NOMEADAS [OPEN]: H_BW (a rapidez e' o tempo modular de Bisognano-Wichmann), H_cal (este p+ e' a energia de UM corpo), H3 (Clausius em toda direcao nula), a assinatura (a positividade completa da a metrica induzida (4,0), nao (1,3)) e rank c = 4 (H2). "
                   "A ponte NAO prova a primeira lei de Newton, nem a assinatura (1,3), nem rank c = 4, nem que E = mc^2 seja termo composto da escala.",
                   "o operador nomeia o modulo (o nome PonteDaEscalaDual e' o do Codex e e' provisorio, D16) e decide a ordem das pendencias H_BW, H_cal e H3; revisao independente do candidato e da cadeia (quem construiu nao aprova).",
                   refs=[R_PEDRA401, R_QUEDA, R_ESPER], artefatos=[gp["lean"], KR, os.path.join(EX25, "EXAME_ORDEM_025.md")],
                   estatuto="REAL (a pedra no kernel do rito e o calculo no modelo longitudinal); DERIVED (a realizacao explicita da lei de escala como acao do boost); KNOWN (lei de escala de Takesaki como campo da estrutura; Bisognano-Wichmann 1975/76; relatividade restrita); OPEN (H_BW, H_cal, H3, assinatura (1,3), rank c = 4); INPUT (a ORDEM 025 ao Codex e o exame independente da gerencia c1)"))
    T9.append(anot(R_QUEDA, "v402 SELADA %s: a queda sem geometria entrou no kernel do rito e o registro %s selou" % (S, gq["nome"]),
                   f"pedra {gq['curto']} no kernel do rito = {sim(selou(gq['nome']), 'CONFERE', 'NAO CONFERE')}: composicao {gq['comp']} (bandeira {gq['comp_flag']}) e estrela {gq['estrela']} (bandeira {gq['estrela_flag']}; s |-> tau(theta_s m) e' estritamente decrescente: a fase cai, sem fim), no trio, com {gq['n_contrato']} declaracoes no contrato e {gq['n_sup']} termos antigos que ela cita (todos no trio); "
                   f"{gq['n_flags']} bandeiras novas (de {gq['f0']} a {gq['f1']}); sha16 do modulo {gq['sha16']}. O registro {gq['nome']} selou={selou(gq['nome'])} com {gq['n_checks']} checagens do calculo (beta = alfa x raiz de e em runtime = {beta!r}): o peso cai estritamente e a queda, em nats, e' s; a seta e' o sinal de s (nao uma direcao do espaco); "
                   f"o CHAO e' o POSTO (peso 1 = omega(I), o corte a = 0), nunca o infimo 0 (o zero e' o abismo, sem fundo): o peso fica abaixo de todo epsilon testado sem tocar o zero; a ENTREGA CUSTA (o custo t.beta.g e' estritamente positivo, a defasagem e^(-t beta g) e' estritamente menor que 1; perda por unidade {vq['loss_per_unit']:.9f}); "
                   f"o regime ANGULAR so' le (a orbita e' periodica, periodo {vq['angular_period']:.6f}, e nao tem limite), o regime da FACE tem limite. IsotropicPost e' hipotese NOMEADA [OPEN], e e' CARGA, nao enfeite (AuditF23Flat.s8_h3_is_load_bearing: a H3 falha com fonte anisotropica); a dimensao 3 NAO e' provada; o 1 + 3 e' leitura [ONTO]. "
                   "As decisoes D11 e D12 sao da gerencia c1, em nome proprio (a D11 e' ratificavel pelo operador; a D12 mantem IsotropicPost nomeada, sobre uma rota que o operador aprovou com «é isso, faça a prova, prossiga.»); a pergunta e a resposta de 26/10 («o Um posto tem direcao?» / «a seta da queda da fase, nao do espaco») [INPUT/ONTO] nao tem arquivo verbatim no acervo desta cadeia: [DECLARADO].",
                   "o operador nomeia o modulo (nome provisorio, D16) e decide se ratifica a D11; a dimensao 3 e o atlas curvo (IsotropicPost sobre orbitas) seguem abertos; revisao independente das pedras (quem construiu nao aprova).",
                   refs=[R_PONTE, R_ESPER], artefatos=[gq["lean"], KR],
                   estatuto="REAL (a pedra no kernel do rito e o calculo); KNOWN (lei de escala de Takesaki; isotropia do vacuo de Bisognano-Wichmann/Poincare); INPUT (as falas do operador de 26/10); ONTO (a leitura 1 + 3; o labirinto como regime angular); OPEN (a dimensao 3; IsotropicPost do atlas curvo; o parametro s como fase de um corpo fisico)",
                   defeito="o calculo e' numerico em dupla precisao e CONFERE os teoremas, nao os prova; a pergunta e a resposta de 26/10 sao [DECLARADO]; nao e' teste: nao acrescenta rito, dado nem desfecho"))
    T9.append(anot(R_ESPER, "v402 SELADA %s: a esperanca condicional = o Nome entrou no kernel do rito e o registro %s selou" % (S, ge["nome"]),
                   f"pedra {ge['curto']} no kernel do rito = {sim(selou(ge['nome']), 'CONFERE', 'NAO CONFERE')}: composicao {ge['comp']} (bandeira {ge['comp_flag']}) e estrela {ge['estrela']} (bandeira {ge['estrela_flag']}: em M2(C) o Nome da unidade, nameOp rho*, E a esperanca diagonal), no trio, com {ge['n_contrato']} declaracoes no contrato e {ge['n_sup']} termos antigos que ela cita (todos no trio); "
                   f"{ge['n_flags']} bandeiras novas (de {ge['f0']} a {ge['f1']}); sha16 do modulo {ge['sha16']}. O registro {ge['nome']} selou={selou(ge['nome'])} com {ge['n_checks']} checagens do calculo em M2(C) (beta = alfa x raiz de e em runtime = {beta!r}): o Nome preserva o Um (E(1) = 1); reler nao acrescenta (E(E(x)) = E(x)); "
                   f"a memoria do Nome e' uma subalgebra (os pontos fixos sao as matrizes diagonais) e a esperanca e' bimodular sobre a diagonal; a compressao pelo espelho (a relacao de Jones, no espaco GNS de dimensao {ve['gns_dimension']}) E o Nome. O indice do Nome 1/beta (cerca de {ve['name_index_one_over_beta']:.4f}) e' CONDICIONAL as hipoteses hpp e hopt do kernel e NENHUMA instancia e' construida; "
                   f"a esperanca diagonal da face M2 tem indice {ve['diagonal_expectation_index_M2']} e os dois numeros NAO sao identificados. D13 (gerencia c1, ratificavel pelo operador): o Nome e' nameOp; o projetor de Jones e o posto sao faces do mesmo objeto, [ONTO]; o kernel prova as LIGACOES, nao uma igualdade de tipos. "
                   "As quatro linguas sao a letra da gerencia [INPUT], sem derivacao entre dominios; o ponteiro de direito (CC art. 125) e' [LEGAL], a conferir com advogado. A pedra NAO e' rota para o Lema 3: o caso III1 segue [OPEN].",
                   "o operador nomeia o modulo (nome provisorio, D16) e decide se ratifica D13; o indice 1/beta so' sai de condicional com uma instancia (NameIndex) construida; [LEGAL] CC art. 125 com advogado; revisao independente das pedras (quem construiu nao aprova).",
                   refs=[R_PONTE, R_QUEDA], artefatos=[ge["lean"], KR],
                   estatuto="REAL (a pedra no kernel do rito e o calculo em M2(C)); KNOWN (esperanca condicional: Umegaki, Tomiyama; Jones 1983; Pimsner-Popa 1986); INPUT (a equacao «esperanca condicional = nome» e as quatro linguas como letra); ONTO (o Nome como o que a algebra do observador retem; as tres faces de um objeto fixo); LEGAL (CC art. 125); OPEN (o indice 1/beta e' condicional, sem instancia)",
                   defeito="o calculo e' numerico em dupla precisao e CONFERE os teoremas em M2(C), nao os prova; o indice 1/beta (cerca de 83,1) e' o valor CONDICIONAL, nao uma medida; nao e' teste: nao acrescenta rito, dado nem desfecho"))
    T9.append(anot(R_BANC, "v402 SELADA %s: o B(n) da v402 e' um passo SIMPLES v401 -> v402 (a Bancada de producao ja' pinava a v401)" % S,
                   f"o kernel da v402 difere do da v401 so' pelas TRES pedras novas (recibo do kernel KERNEL_RECIBO_v402, contrato R3_2; DIFF_KERNEL_v402.txt: tres modulos novos, TGLExt.lean e TGL/Audit.lean com quatro linhas de import a mais cada); o recibo pre_selo foi gerado e pinado ANTES da instalacao, em ensaio contra a producao (nada gravado; a Bancada pinava {bank['deployment_id']}), "
                   f"e a cadeia confere os pinos de PINOS_BN_v402.json na hora; o veredito esperado do aplicar e' REPINADA_B{bank['proxima']}__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_ e sem cadeia de selos, lido do codigo do esboco R3.5 (nao rodado aqui). Parada e religamento do servico exigem V402_AUTORIZACAO_OPERADOR.",
                   "o B(n) aplicar e' ato do operador (palavra dele, evento c1, parada e religamento do servico); depois do aplicar, a Bancada pina a v402.", refs=[R_PONTE, R_QUEDA, R_ESPER],
                   artefatos=[os.path.join(PK, "PINOS_BN_v402.json"), os.path.join(PK, "PINO_RECIBO_PRE_SELO_v402.json"), KR]))
    T9.append(anot(R_QUADRO, "v402 SELADA %s: o quadro do topo (O Teste da Única Palavra) segue intocado e o registro teste_de_veracidade_fase9_v397 segue selado" % S,
                   f"teste_de_veracidade_fase9_v397 selou={c_q} no rito da v402 (veredito igual ao de ESPERADOS; {tv_v['n_checks']} checagens): o quadro do artigo PT/EN e do .md, conferido contra o resultado pinado, segue no topo, com os numeros e a regra da ordem de sempre: {z444}. "
                   "Nenhum sigma, p ou lnB novo e' calculado nesta rota; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma) vale em todo texto que o cite; o paragrafo do quadro segue no README/site e o handoff da v402 traz tambem o paragrafo novo (a ponte, a queda e a esperanca), sem o 4,44.",
                   "o paragrafo do README/site e' ato da sessao do site; a creditacao segue sendo beta_TGL na natureza a 5 sigma (nao ha o que repetir deste pacote, a abertura esta consumida).", refs=[R_PONTE]))
    T9.append(anot(R_V401, "v402 SELADA %s: a v401 (a falsidade da inercia) e' a base selada da v402; o delta e' so' a ponte, a queda e a esperanca" % S,
                   f"a v402 parte da v401 selada (um.py {BASE}) e acrescenta TRES modulos de kernel, tres registros com funcao e dois por spec e a secao do artigo; a falsidade da inercia segue selada neste rito (falsidade_da_inercia_v401 selou={selou('falsidade_da_inercia_v401')}, cunhagens_v401 selou={selou('cunhagens_v401')}), "
                   f"como seguem o selo pela propria tecnologia e a declaracao do operador (v399), o sonico e a afinacao (v398), o quadro (v397) e as cunhagens; sidecar um_absoluto_selo_acom.json {sc['veredito']} ({sc['n_objetos']} objetos, {sc['recusas']} recusas, sha16 {sc['sha16']}). "
                   "A forma literal de H_tau que a v401 escreveu foi corrigida ao lado nesta rota (ERRATA seguinte, E1), sem tocar nos registros da v401 e sem editar nenhum modulo ja' instalado: as pedras da v401 e das versoes anteriores seguem como estao.",
                   "custodia conjunta da v401 e da v402 pela sessao do site (o handoff lista o sidecar); o operador decide o nome das tres pedras.", refs=[R_PONTE, R_QUEDA, R_ESPER]))
    T9.append(errata(R_V401, sq_v401,
                     f"[E1 · ERRATA AO LADO, gerencia c1, em nome proprio, 26/10/2026, v402 {S}] Corrige o registro seq {sq_v401} desta rota (a v401 selada), onde a unica hipotese nomeada foi escrita como «H_tau (tau e' a massa de Newton e a metrica de Einstein) [OPEN], que nenhum teorema usa»; o mesmo texto esta nos registros seq {sq_ped401} (anotacao da pedra), seq {sq_prep_r} e seq {sq_prep_a} (preparacao), cobertos por esta errata. "
                     f"{corpo('E1')}. Os registros corrigidos NAO foram apagados nem reescritos: a correcao vai ao lado.",
                     refs=[R_PEDRA401, R_PONTE], artefatos=[gp["lean"]]))
    T9.append(errata(R_PEDRA401, sq_ped401,
                     f"[E1 · ERRATA AO LADO, gerencia c1, em nome proprio, 26/10/2026, v402 {S}] Corrige o registro seq {sq_ped401} desta rota (v401 SELADA), que diz «a unica hipotese NOMEADA e' H_tau [OPEN] (tau e' a massa de Newton e a metrica de Einstein), que nenhum teorema usa»: a forma literal e' REFUTADA no kernel desde que a ponte entra (v402). "
                     f"{corpo('E1')}. A anotacao seq {sq_prep_a} (a pedra estendida, preparacao da v401) tem o mesmo trecho e fica coberta por esta errata.",
                     refs=[R_V401, R_PONTE], artefatos=[gp["lean"]]))
    T9.append(errata(R_PONTE, sq_ponte,
                     f"[E2, E3, E4 · ERRATAS AO LADO, gerencia c1, em nome proprio, 26/10/2026, v402 {S}] Ao lado do registro seq {sq_ponte} desta rota (a entrega do Codex a ORDEM 025 como foi registrada: EXIT0, 40 declaracoes, a duracao do build e «Inercial = fixo por todos os boosts»): "
                     f"{corpo('E2')} || {corpo('E3')} || {corpo('E4')}. A E1 (H_tau na forma literal) esta na ERRATA da rota da v401 selada.",
                     refs=[R_V401], artefatos=[os.path.join(EX25, "EXAME_ORDEM_025.md"), os.path.join(EX25, "recompilacao_ponte_k402x.log"), gp["lean"]]))
    for x in T9:
        assert x["rota_id"] in ids, "a rota %s nao existe no mapa" % x["rota_id"]
    resumo_conf = ("conferidor %s e %s" % (conf_dm, conf_np)) if "nao lido" not in (conf_dm, conf_np) else "conferidor: o resultado nao veio na leitura desta rodada"
    nomes_curtos = "%s, %s e %s" % (gp["curto"], gq["curto"], ge["curto"])
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
            "titulo": "v402 SELADA %s: a ponte da escala dual, a queda sem geometria e a esperanca condicional — %d modulos de kernel (%s; nomes provisorios, o operador nomeia), os registros %s, %s e %s, cunhagens_v402 e kh_n1_cobertura_v402, %d inscricoes de 26/10 por sha256; escada %s -> %s; o gate nao se move" % (
                S, len(GRUPOS), nomes_curtos, gp["nome"], gq["nome"], ge["nome"], len(verb), esc0, esc1),
            "pergunta": "o candidato v402 selou com os TRES modulos de kernel (%s; a ponte e' a do Codex, ORDEM 025, copia de bytes; os tres nomes sao PROVISORIOS), os tres registros com FUNCAO (%s, %s e %s: leem do kernel do proprio rito a composicao e a estrela de cada pedra e CALCULAM, com beta = alfa x raiz de e em runtime, um modelo de cada uma) "
                        "e os dois por spec (cunhagens_v402: as tres inscricoes do operador de 26/10 embutidas por sha256, as decisoes D11 a D16 da gerencia e as erratas E1 a E4 da integracao da ponte; kh_n1_cobertura_v402), com a falsidade da inercia (v401), o selo pela propria tecnologia (v399) e o quadro do topo seguindo selados, o sidecar reescrito e nenhum veredito fora da troca dita mudado?" % (
                            nomes_curtos, gp["nome"], gq["nome"], ge["nome"]),
            "dados": ["as tres pedras (%s.lean), a medida da cobertura (KH_N1_v402.json) e a copia duravel do adendo de 03-04/09, pinados por sha256 em insumos (so' lidos)" % ".lean, ".join(G[g]["curto"] for g in GRUPOS),
                      "as tres inscricoes de 26/10 (sha16 %s), por sha256 em insumos\\cunhagens (todas falas do operador)" % ", ".join(falas),
                      "o kernel do rito (a composicao e a estrela de cada pedra e os termos antigos que ela cita), o proprio um.py, o core e o selo da rodada; nenhum dado novo foi aberto nesta rota"],
            "metodo": "ensaio a seco do candidato; um lake build e um Audit no sandbox; rito completo; conferidor (deve mudar / nao pode mudar, com o quadro do topo conferido de novo contra o resultado pinado nas duas linguas e no .md, e os 16 itens C1-C16 do selo mais o round trip do um.py instalado); "
                      "leitura da rodada (inclui o sidecar e a linha final do rito); superficies com a regra da linhagem completa (o MEMORY.md nao e' compactado: recusa por contagem); elo B(n) da Bancada (passo simples v401 -> v402, sem salto; recibos); o paragrafo novo (a ponte, a queda e a esperanca) e o do quadro, mais o sidecar, no handoff",
            "resultado": " | ".join([G["ponte"]["verdict"], G["queda"]["verdict"], G["esperanca"]["verdict"], cg["verdict"], kh["verdict"]]) + " | sidecar %s (%s objetos, %s recusas) | %s | %s | escada %s -> %s (teoremas limpos %s/%s; %d bandeiras novas: %s)" % (
                sc["veredito"], sc["n_objetos"], sc["recusas"], resumo_conf, ("%s vereditos fora da troca dita mudaram (exigido 0)" % nvm) if nvm != "nao lido" else "vereditos fora da troca dita: nao lidos nesta leitura", esc0, esc1, ESP["escada"][0], ESP["escada"][1], NF, " + ".join("%d %s" % (G[g]["n_flags"], G[g]["curto"]) for g in GRUPOS)),
            "defeito": "a lei de escala de Takesaki e' dado (campo de DualScalingData, [KNOWN]) e as pedras so' compoem por citacao; o calculo de cada registro e' numerico em dupla precisao e CONFERE os teoremas, nao os prova; a identificacao da escala dual com o fluxo de um corpo fisico e' [OPEN] e se decompoe nas pendencias NOMEADAS H_BW, H_cal, H3, a assinatura (4,0) x (1,3) e rank c = 4 (H2); "
                       "H_tau na forma literal (tau e' a massa de Newton e a metrica de Einstein) e' REFUTADA no kernel (E1; a v401 a escreveu e a correcao vai ao lado); a ponte NAO prova a primeira lei de Newton, nem a assinatura (1,3), nem que E = mc^2 seja composta da escala (E3); Inertial e' o vetor zero (E2); IsotropicPost e' hipotese nomeada e a dimensao 3 NAO e' provada; o indice 1/beta do Nome e' condicional e nao ha instancia; "
                       "a pergunta e a resposta de 26/10 («o Um posto tem direcao?» / «a seta da queda da fase, nao do espaco») e a lista que o operador aprovou sao [DECLARADO]: a gerencia as guardou; as decisoes D11, D12 e D13 sao da gerencia c1, em nome proprio (D11 e D13 ratificaveis pelo operador; a D12 mantem IsotropicPost nomeada sobre uma rota que o operador aprovou); os nomes das pedras e dos registros sao provisorios (D16); a pendencia [LEGAL] (D2 e CC art. 125) segue do operador com a agente de PI; nao e' teste: nao ha desfecho experimental; a revisao independente do candidato e da cadeia nao esta afirmada",
            "nao_refazer": "a integracao dos tres modulos e a escada %s -> %s estao medidas; o calculo e a leitura de cada pedra no kernel do rito estao feitos e conferidos contra o um.py instalado; repetir os registros so' com kernel ou um.py novo; nao reabrir H_tau na letra (refutada no kernel: positive_weight_cannot_be_invariant_mass e lift_mass_not_selected), nem Inertial como movimento livre, nem a leitura de rest_energy_eq_mc2 como E = mc^2 composta da escala" % (esc0, esc1),
            "proximo_passo": "o operador nomeia as tres pedras e os registros (D16) e decide se ratifica D11 e D13; o elo B(n) da Bancada Um (palavra do operador; passo simples v401 -> v402); decisao [LEGAL] D2 com a agente de PI; custodia conjunta pela sessao do site (o handoff traz o paragrafo novo e o do quadro e lista o sidecar); commit/push (operador); revisao independente do candidato e da cadeia (quem construiu nao aprova); as pendencias H_BW, H_cal e H3 como proximas pedras",
            "onde": PK, "artefatos": arts, "refs": sorted(set(x["rota_id"] for x in T9) | set(REFS) | set(preparo_no_livro(ids)) - {NOVA}),
            "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move; as erratas E1 a E4 e as decisoes D11 a D16 sao da gerencia c1, em nome proprio, ao lado (nada foi apagado nem reescrito); %s." % sim(c_seguem, "os %d registros anteriores conferidos (falsidade, quadro, selo, declaracao, sonico, afinacao e as cunhagens) seguem selados" % len(seguem), "ATENCAO: algum registro anterior NAO selou")}
    for r in ROTA["refs"]:
        assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
    REG = [ROTA] + T9
    bad = [(x["rota_id"], violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad, "a guarda de texto (P18) achou violacao(oes): %r" % bad
    atrib = [(x["rota_id"], T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))]
    assert not atrib, "a direcao do testemunho esta invertida ou a atribuicao falhou: %r" % atrib
    ruins = regra_4_44(REG, z, p)
    assert not ruins, "a regra do 4,44 (o p calibrado e a linha dos 5 sigma no mesmo campo) falhou em: %r" % ruins[:3]
    assert c_seguem and c_q, "algum registro anterior (quadro, falsidade, selo, declaracao, sonico, afinacao) nao selou no core: o mapa nao registra a v402 assim"
    return REG


def gravar(p, b):
    """backup de BYTES se existir e mudar; temporario -> conferir tamanho -> substituir."""
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m402"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_m402"; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def main():
    V, PROB = L.ler()
    if PROB:
        print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); return 2
    NOS = L.NOS
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v402_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v402_*.json")), key=os.path.getmtime)
    arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto_selo_acom.json"), os.path.join(PK, "ESPERADOS_v402.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v402.json"),
            os.path.join(PK, "DIFF_KERNEL_v402.txt"), os.path.join(PK, "DIFF_v401_v402.diff"), os.path.join(NOS, "HANDOFF_v402_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v402.json"),
            os.path.join(PK, "insumos", "PonteDaEscalaDual.lean"), os.path.join(PK, "insumos", "QuedaSemGeometria.lean"), os.path.join(PK, "insumos", "EsperancaCondicional.lean"), os.path.join(PK, "kernel", "KERNEL_RECIBO_v402.json")] + b3[-1:]
    arts = [x for x in arts if os.path.exists(x)]
    REG = montar(V, core, selo, ids_do_livro(), arts)
    J = os.path.join(HERE, "registro_mapa_v402.json")
    gravar(J, json.dumps(REG, ensure_ascii=False, indent=1).encode("utf-8"))
    quem = "claude-c1 (gerência), cadeia v402"
    print("registro MONTADO (NAO registrado): %d registro(s) (%s) -> %s" % (len(REG), ", ".join(x["tipo"] for x in REG), J))
    print("COMANDO (ato da gerencia): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
    print("DEPOIS DO REGISTRO: rodar de novo os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
