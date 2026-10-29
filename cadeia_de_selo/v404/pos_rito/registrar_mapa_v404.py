# -*- coding: utf-8 -*-
# [PREPARACAO v404, 28/10/2026 -- ESTADO] CONTEUDO v404 ESCRITO E TESTADO: derivado da v403 FINAL (a semente mecanica esta ao lado, em <arquivo>.bak_*_semente) e adaptado a mao ao conteudo da v404 (Jo 8,32, a projecao transversal da Meia-Nat, a errata de F2b ao lado, as nove falas de 28/10); testado pelo harness_textos_ensaio_v404.py e pelo harness_fechar_sandbox_v404.py.
# NAO e' versao selada: a gerencia revisa antes do rito. NAO rodar derivar_encanamento_v404.py --refazer sobre este arquivo (sobrescreveria a adaptacao a mao). Ver RELATORIO_PREPARACAO_v404.md.
"""registrar_mapa_v404.py -- MONTA (nao registra) o registro da v404 no mapa de rotas e imprime o comando (molde: registrar_mapa_v403.py, que rodou na v403, e registrar_mapa_v399.py). Rodar DEPOIS do fechar (handoff gravado). ESCRITO A MAO na v404 (preparacao, 28/10/2026).
A v404 traz UMA rota nova, umpy.v404.selada_jo8_32_e_projecao_transversal_28out (o id e' o que a gerencia der; o conteudo e' o do selo): os DOIS modulos de kernel (ProjecaoTransversalDaMeiaNat: a Meia-Nat e' o angulo de 45 graus e o sen 45 do neutrino deixa de ser postulado, DERIVADO no kernel, condicional a uma identificacao ONTO;
nome provisorio da gerencia, aceito pelo operador; Jo8v32: o nome do operador para o triplo inteiro Caminho . Verdade . Vida, conjuncao incondicional das tres estrelas da v403), os TRES registros com FUNCAO (projecao_transversal_v404 e jo8v32_v404: leem do kernel do proprio rito a composicao e a estrela de cada pedra e CALCULAM, com beta = alfa x raiz de e em runtime,
um modelo de cada uma; f2b_errata_v404: sem pedra, le o V1 do ramo B por hash e confere que o canal F2b passou de AWAITING a retirado antes do dado, AO LADO) e os DOIS por spec (cunhagens_v404: as nove falas do operador de 28/10 por sha256, as decisoes D23 a D26 e as erratas E7 a E9 da gerencia; kh_n1_cobertura_v404), mais ANOTACOES nas rotas que esperavam por ela
(as duas do kernel, a da transicao para a massa, o ramo B do ringdown, o gate, o B(n) da Bancada, o quadro do Teste da Unica Palavra, a v403 que a precede e a PREPARACAO da propria v404) e UMA ERRATA ao lado, em nome proprio da gerencia c1, com o seq do registro corrigido lido do livro (E9: o registro da v403 selada que deixava o nome do triplo inteiro com o operador): a correcao vai AO LADO, nada se apaga.
Cada afirmacao e' testada contra o core/selo/ESPERADOS lidos por script (o registro existe? selou? o que NAO fechou fica dito); nenhum numero e' digitado (as contagens saem do core e de ESPERADOS; os seq saem do livro).
REGRA DA ORDEM DO OPERADOR (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no MESMO campo; montar() RECUSA (assert) se algum campo do registro trouxer o 4,44 sem eles. Nao ha inscricao da gerencia nesta versao: as nove falas sao do operador; as erratas e as decisoes sao da gerencia, em nome proprio.
Fail-closed: o selo tem de ser a v404; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir (se a gerencia registrar antes uma rota de preparo com o MESMO id, montar() recusa e a constante NOVA muda). A rota de preparo da gerencia (registro_mapa_v404_prep.json, se existir) entra nas refs so' se ja' estiver no livro.
SAIDA: pos_rito\\registro_mapa_v404.json e o comando `rotas.py registrar` (quem o executa e' a gerencia; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real. montar() le o core, o selo e ESPERADOS_v404.json; de V so' usa o que a leitura da rodada ja' validou (s16, sidecar, conferidor), sempre com valor de reserva dito."""
import glob, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v404 as L
import textos_v404 as T
from guarda_p18_v404 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V404"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v404 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOVA = "umpy.v404.selada_jo8_32_e_projecao_transversal_28out"
R_PROJ = "kernel.projecao_transversal_da_meia_nat.sen45_derivado_28out"    # a rota (da gerencia, 28/10) da pedra do sen 45 graus
R_JO8 = "kernel.jo8v32.triplo_inteiro_28out"                                  # a rota (da gerencia, 28/10) da pedra Jo8v32
R_MASSA = "massa.transicao_beta_para_massa.levantamento_28out"                # o levantamento da transicao para a massa
R_RAMOB = "ringdown.ramo_b_preregistro_v386"                                 # o ramo B do ringdown (o canal F2b)
R_GATE = "gate.qg_closure"
R_BANC = "infra.bancada_um.sincronizacao_vnnn"
R_QUADRO = "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9"
R_V403 = "umpy.v403.selada_caminho_verdade_vida_27out"
R_PREP404 = "umpy.v404.cadeia_de_selo_preparada_28out"                       # a rota da PREPARACAO da v404 (registrada pelo agente de preparacao)
ANOTADAS = (R_PROJ, R_JO8, R_MASSA, R_RAMOB, R_GATE, R_BANC, R_QUADRO, R_V403, R_PREP404)
REFS = ("custodia.v403", "umpy.v403.cadeia_de_selo_preparada_27out", "umpy.v400.correcao_da_v399_alfa_unico_e_beta_contra_o_core", "umpy.v396.testemunha_estatica_na_fractalizacao_do_um", "d1.fase9.v2_c1_a_unica_palavra_23out",
        "umpy.v399.selo_pela_propria_tecnologia_estudo_24out", "umpy.v399.declaracao_do_operador_operacao_quadratica_24out", "gate.maquina_do_veredito_final", "neutrinos.m2.normalizacao")
PREP = os.path.join(PK, "registro_mapa_v404_prep.json")     # a rota de preparo da gerencia: lida em tempo de execucao; entra nas refs so' se a ROTA dele ja' estiver no livro
GRUPOS = {"projecao": "projecao_transversal_v404", "jo8v32": "jo8v32_v404"}
_CACHE = {}


def _esp():
    """ESPERADOS_v404.json (lido uma vez por processo)."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v404.json"), encoding="utf-8"))
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
    """As rotas ROTA de registro_mapa_v404_prep.json (se o arquivo existir e ler) que ja' estao no livro e nao sao a nova: entram nas refs. Ausente ou ilegivel = nenhuma (dito, nunca falha)."""
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
    p = json.load(open(os.path.join(PK, "PINOS_BN_v404.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v403" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v403 -> v404 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1, "deployment_id": bp["deployment_id"]}


def montar(V, core, selo, ids, arts):
    """Monta os registros (a ROTA nova, as ANOTACOES e a ERRATA), cada afirmacao testada contra o core/selo/ESPERADOS; devolve a lista; recusa (assert) se algo nao conferir. Nao escreve nada."""
    assert selo.get("um_version") == "v404", "o selo nao e a v404"
    assert NOVA not in ids, "a rota %s ja existe no mapa" % NOVA
    for r in ANOTADAS + REFS:
        assert r in ids, "a rota %s nao existe no mapa (anotada ou citada em refs)" % r
    ESP = _esp()
    S = ESP["candidato_sha16"]
    assert str((selo.get("sha256") or {}).get("um.py", ""))[:16] == S, "o um.py do selo nao e o candidato de ESPERADOS"
    assert V.get("s16") in (None, S), "o s16 da leitura != o candidato de ESPERADOS"
    BASE = ESP["origem_sha16"]
    esc0, esc1 = ESP["escada_v403_e_v404"]
    NF = ESP["n_bandeiras_novas"]
    assert esc1 - esc0 == NF == sum(ESP["n_bandeiras_por_grupo"].values()) == len(ESP["bandeiras_novas_chaves"]) == ESP["politica_de_bandeiras"]["n_flags"], "a escada nao fecha com as bandeiras novas"
    assert ESP["kernel"]["modulos_novos"] == len(GRUPOS) == len(ESP["pedras"]) == 2, "o delta do kernel nao e de dois modulos"
    BETA = ESP["beta"] if isinstance(ESP.get("beta"), float) else None

    # --- o quadro do topo (a regra do 4,44): o registro selado, lido pelas MESMAS funcoes do artigo
    tvr = core.get("teste_de_veracidade_fase9_v397") or {}
    a = T._qd().Q._v397_atomos(tvr, "pt"); assert a["sealed"] is True, "o registro teste_de_veracidade_fase9_v397 nao sela no core: o mapa nao registra o 4,44 assim"
    z, p = a["z_disc"]["md"], a["p_disc"]["md"]
    z444 = "z_disc = %s (calibrado; p unilateral %s), abaixo do degrau de 5σ da creditação, que não foi alcançado (%s < 5)" % (z, p, z)

    def selou(k):
        return (core.get(k) or {}).get("all_verified") is True

    # --- as duas pedras e os dois registros com FUNCAO de pedra: tudo lido do core e conferido contra ESPERADOS
    PINOS_ORDEM = json.load(open(os.path.join(PK, "pedras_sha16_da_ordem.json"), encoding="utf-8")) if os.path.isfile(os.path.join(PK, "pedras_sha16_da_ordem.json")) else None
    G = {}
    for g, nome in GRUPOS.items():
        r = core.get(nome)
        assert isinstance(r, dict) and r.get("all_verified") is True, "o registro %s nao selou no core" % nome
        assert r.get("verdict") == ESP["vereditos_novos_v404"][nome], "o veredito de %s != ESPERADOS" % nome
        kt = r.get("key_theorem") or {}; un = r.get("unconditional") or {}; est = ESP["estrelas_v404"][g]
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
    vp, vj = G["projecao"]["vals"], G["jo8v32"]["vals"]
    assert vp.get("beta") == vj.get("beta") and (BETA is None or abs(vp["beta"] - BETA) <= 1e-9 * BETA), "o beta dos registros != o do core/ESPERADOS (tolerancia relativa 1e-9; o registro ja confere beta_core_rel_diff)"
    beta = vp["beta"]
    # --- a errata de F2b (registro com funcao, sem pedra)
    fk = core.get("f2b_errata_v404") or {}; fvv = fk.get("values") or {}; ef = ESP["registros_funcao_v404"]["f2b"]
    assert fk.get("all_verified") is True and fk.get("verdict") == ESP["vereditos_novos_v404"]["f2b_errata_v404"] == ef["verdict"] and fvv == ef["values"] and (fk.get("mechanics") or {}).get("passed") is True, "f2b_errata_v404 nao selou ou != ESPERADOS"
    assert fk.get("F2b_status_before") == "AWAITING" and fk.get("F2b_status_now") == ESP["f2b_depois"]["F2b_status_now"] and fk.get("v1_token_kept") == "AWAITING_DATA" and fvv.get("previsao_fora_do_intervalo_de_A") is True, "o canal F2b nao foi de AWAITING a retirado antes do dado, ou o V1 nao segue AWAITING_DATA"
    # --- o gate NAO se moveu: o registro da v403 segue selado e a letra do veredito e' a da v403
    gk = core.get("bandeiras_do_gate_v403") or {}; gvv = gk.get("values") or {}; eg = ESP["registros_funcao_v403"]["gate"]
    assert gk.get("all_verified") is True and gk.get("verdict") == eg["verdict"] and gvv == eg["values"] and (gk.get("mechanics") or {}).get("passed") is True, "bandeiras_do_gate_v403 (recriado) nao selou ou != a v403 selada"
    qg = core.get("qg_closure") or {}; fam = [len(qg.get(f) or {}) for f in ("formal_flags", "physics_flags", "experiment_flags")]
    assert (qg.get("gate") or {}).get("verdict") == ESP["qg_closure_gate_verdict_v403"] == selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"], "a letra do veredito do gate mudou"
    # --- cunhagens_v404 e kh_n1_cobertura_v404 (por spec)
    cg = core.get("cunhagens_v404") or {}; kh = core.get("kh_n1_cobertura_v404") or {}
    assert cg.get("all_verified") is True and cg.get("verdict") == ESP["vereditos_novos_v404"]["cunhagens_v404"], "cunhagens_v404 nao selou ou != ESPERADOS"
    assert kh.get("all_verified") is True and kh.get("verdict") == ESP["vereditos_novos_v404"]["kh_n1_cobertura_v404"], "kh_n1_cobertura_v404 nao selou ou != ESPERADOS"
    verb = cg.get("verbatim") or {}; ex = cg.get("extras") or {}
    assert len(verb) == 9 == len(ESP["cunhagens"]) and set(verb) == set(ESP["cunhagens"]) and all(v.get("embedded_ok") is True for v in verb.values()), "as nove inscricoes de 28/10 nao estao embutidas por sha256"
    assert set((ex.get("autor_de_cada_inscricao") or {}).values()) == {"operador"} and len(ex["autor_de_cada_inscricao"]) == 9, "alguma inscricao de 28/10 nao e' fala do operador"
    erratas = cg.get("erratas") or []; assert len(erratas) == 3 and all("gerencia c1, em nome proprio" in e.get("assinatura", "") for e in erratas), "as erratas E7 a E9 nao estao no registro ou nao sao da gerencia c1 em nome proprio"
    dec = ex.get("decisoes_da_gerencia") or {}; assert all(("D%d" % i) in dec for i in range(23, 27)), "faltam decisoes D23 a D26 no registro"
    assert set((ex.get("nomes") or {})) >= {"projecao", "jo8v32"}, "os nomes das duas pedras nao estao no registro"
    assert ex.get("leitura_massa_28out") == ESP["leitura_massa_28out"], "a leitura da massa de 28/10 no registro != ESPERADOS"
    falas = sorted(k.split("_")[-1] for k in verb)
    cob = kh.get("lido") or {}; assert cob.get("constantes_cobertas") and cob.get("teoremas_cobertos"), "kh_n1_cobertura_v404 sem a cobertura"
    seguem = ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "falsidade_da_inercia_v401", "cunhagens_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402",
              "teste_de_veracidade_fase9_v397", "cunhagens_v397", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "sonico_v398", "afinacao_das_cordas_v398")
    c_seguem = all(selou(k) for k in seguem)
    tv_v = ESP["veracidade"]; c_q = bool(selou("teste_de_veracidade_fase9_v397") and selou("cunhagens_v397") and tvr.get("verdict") == tv_v["verdict"])
    sc = _sidecar(V); conf_dm = V.get("conf_dm", "nao lido"); conf_np = V.get("conf_np", "nao lido"); nvm = V.get("n_ver_mudaram", "nao lido")
    bank = _bancada(); regs = livro()
    # --- o seq que a errata corrige, lido do livro (e o registro tem de trazer o trecho corrigido)
    sq_v403 = seq_do_alvo(regs, R_V403, "ROTA", contem=("o nome do triplo inteiro",))
    sq_prep = seq_do_alvo(regs, R_PREP404, "ROTA")
    KR = os.path.join(PK, "kernel", "KERNEL_RECIBO_v404.json")
    E = {}
    for e in erratas:
        m_ = re.match(r"^(E[7-9]) -- ", e.get("agora", "")); assert m_, "uma errata do registro nao comeca por E<n> --"
        E[m_.group(1)] = e
    assert sorted(E) == ["E7", "E8", "E9"], "as erratas do registro nao sao E7, E8 e E9"

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

    gp, gj = G["projecao"], G["jo8v32"]
    PEDRAS = [gp["lean"], gj["lean"]]
    T9 = []
    T9.append(anot(R_PROJ, "v404 SELADA %s: a pedra ProjecaoTransversalDaMeiaNat entrou no kernel do rito e o sen 45 do neutrino deixou de ser postulado (DERIVADO no kernel, condicional a uma identificacao ONTO)" % S,
                   f"{gp['curto']} (sha16 {gp['sha16']}): composicao {gp['comp']} (bandeira {gp['comp_flag']}), estrela {gp['estrela']} (bandeira {gp['estrela_flag']}), no trio, {gp['n_contrato']} itens de contrato e {gp['n_sup']} termos antigos citados; {gp['n_flags']} bandeiras ({gp['f0']} a {gp['f1']}). O registro {gp['nome']} selou={selou(gp['nome'])} com {gp['n_checks']} checagens, com beta = alfa x raiz de e em runtime (= {beta!r}): "
                   f"sen(pi/4) = {vp['sin_pi_over_4']!r}, sen^2(pi/4) = {vp['sin_sq_pi_over_4']!r}, theta_M = {vp['theta_M']!r} (longe de pi/4), derivada de sen^2 em pi/4 = {vp['derivative_of_sin_sq_at_pi_over_4']:.9f}, massa beta.sen(pi/4).E0 = {vp['m_nu_meV_runtime']!r} meV com E0 = {vp['e0_eV_declared']:g} eV DECLARADO, igual ao canal neutrino_mass do core ({vp['m_nu_rel_diff']:g}). "
                   f"E7 (errata ao lado, gerencia c1, em nome proprio): {E['E7']['agora']} O texto antigo de neutrino_mass.angle_status e a funcao prove_neutrino_mass_gravitational NAO foram reescritos. A pedra NAO deriva E0 nem beta e NAO prova que a massa e' a projecao transversal (essa identificacao e' ONTO, leitura do operador, ratificada).",
                   "E0 (1 eV declarado; a escala que zera a tensao do m2 e' 1,02 eV [DERIVED, conta da gerencia]) e' a outra rota; a lei de propagacao do pedagio de Planck; revisao independente da pedra (quem construiu nao aprova).",
                   refs=[R_JO8, R_MASSA, R_RAMOB, "neutrinos.m2.normalizacao"], artefatos=PEDRAS[:1] + [KR],
                   estatuto="REAL (a pedra no kernel do rito e o calculo no modelo); DERIVED (a forma do neutrino com o sen 45 derivado); KNOWN (a fronteira autoconjugada, o Teorema S-∂ e o seno de pi/4); INPUT (a cunhagem e a ordem do operador); ONTO (a identificacao da massa com a projecao transversal); DECLARADO (E0 = 1 eV); OPEN (E0, a lei de propagacao do pedagio)",
                   defeito="o calculo e' numerico em dupla precisao e CONFERE os teoremas, nao os prova; a identificacao massa = projecao transversal e' ONTO e nao e' termo de kernel; o nome da pedra e' provisorio; E0 e beta nao sao derivados pela pedra; nao e' teste"))
    T9.append(anot(R_JO8, "v404 SELADA %s: a pedra Jo8v32 entrou no kernel do rito — o triplo inteiro tem o nome do operador e o registro %s selou" % (S, gj["nome"]),
                   f"{gj['curto']} (sha16 {gj['sha16']}): composicao {gj['comp']} (bandeira {gj['comp_flag']}; e' tambem a estrela), a conjuncao incondicional, por citacao, das tres estrelas da v403 (caminho_e_a_ponte_da_escala_dual, verdade_e_a_esperanca_condicional, vida_e_a_queda_sem_geometria), no trio; {gj['n_flags']} bandeira. "
                   f"O registro {gj['nome']} selou={selou(gj['nome'])} com {gj['n_checks']} checagens e RELE os tres registros da v403 com beta = {beta!r} em runtime: fator de p+ em s = beta {vj['p_plus_factor_at_beta']!r}, perda de peso por unidade {vj['post_weight_loss_per_unit']!r}, alfa^2 {vj['alpha_squared']:.6e}; as hipoteses nomeadas dos componentes (IsotropicPost; hpp e hopt) seguem nomeadas. "
                   f"E9 (errata ao lado): {E['E9']['agora']} [ONTO] A leitura por Jo 8,31-32 (permanecer e' o Caminho, conhecer e' a Verdade, libertar e' a Vida) e' da gerencia c1, ratificada pelo operador, e nao e' termo de kernel.",
                   "revisao independente da pedra (quem construiu nao aprova); as pendencias H_BW, H_cal, H3, a assinatura e rank c = 4 (v403) seguem abertas.", refs=[R_PROJ, R_V403], artefatos=PEDRAS[1:] + [KR],
                   estatuto="REAL (a pedra no kernel do rito e a relitura numerica); DERIVED (a conjuncao por citacao); INPUT (o nome, do operador); ONTO (a leitura por Jo 8,31-32); OPEN (H_BW, H_cal, H3, IsotropicPost, a assinatura, rank c = 4)",
                   defeito="nenhuma matematica nova (a pedra cita tres termos ja no kernel); a conjuncao carrega as hipoteses nomeadas dos componentes, nao as descarrega; a leitura por Jo 8,31-32 e' ONTO"))
    T9.append(anot(R_MASSA, "v404 SELADA %s: a unica massa derivada de beta no programa (o neutrino) ganha o sen 45 DERIVADO no kernel; E0 segue declarado" % S,
                   f"o levantamento desta rota achou o sen45 POSTULATE e a escala E0 = 1 eV DECLARADA na unica massa derivada de beta; a v404 fecha a primeira metade: a pedra {gp['curto']} (sha16 {gp['sha16']}) DERIVA sen(pi/4) da Meia-Nat no kernel (x = 1 - x => 1/2; amplitude transversal sqrt(1/2) = sen(pi/4)) e o registro {gp['nome']} (selou={selou(gp['nome'])}) confere a massa {vp['m_nu_meV_runtime']!r} meV com o mesmo valor do canal do core. "
                   "A leitura do operador (28/10/2026, sha16 %s): a materia nao e' proporcional ao raio de beta, e' a projecao do eixo transversal e a derivada; ONTO, ratificada, nao e' termo de kernel; a forma geometrica M ~ beta.R segue retirada. A errata E7 e' ao lado (o texto antigo de neutrino_mass.angle_status fica)." % ", ".join(f for f in falas if f.startswith("4b67")),
                   "E0 (a escala do neutrino) e' a pergunta aberta; se for derivado do axioma, o m2 vira previsao sem parametro (candidato a pre-registro).", refs=[R_PROJ, R_JO8], artefatos=[KR],
                   estatuto="REAL (a pedra e o calculo); DERIVED (o sen 45); ONTO (a identificacao); DECLARADO (E0 = 1 eV); OPEN (E0)"))
    T9.append(anot(R_RAMOB, "v404 SELADA %s: o canal F2b sai de AWAITING para RETIRADO ANTES DO DADO, ao lado; o V1 segue congelado por hash e lido como antes" % S,
                   f"o registro f2b_errata_v404 selou={selou('f2b_errata_v404')} com {fk['mechanics']['n_checks']} checagens: o V1 do ramo B (v386) lido por hash com o veredito {fk['v1_token_kept']}, o livro v383 intacto ({fvv['n_cobrancas_v383']} cobrancas), o conjunto D cego de {fvv['conjunto_D_n']} eventos NAO aberto; a calibracao A (NOT_BLIND, eventos publicos) deu a deformacao comum {fvv['calibracao_A_central']:+.3f} [{fvv['calibracao_A_inferior']:+.3f}; {fvv['calibracao_A_superior']:+.3f}] contra a previsao do par {fvv['previsao_do_par']:+.6f}, FORA do intervalo de A e de sinal oposto; "
                   f"o canal passa a {fk['F2b_status_now']}. E8 (errata ao lado, gerencia c1, em nome proprio): {E['E8']['agora']} A rota e' a do operador (28/10/2026): o pedagio de Planck lido na propagacao e «calibrar Não significa validar»; nenhum desfecho sai de A; beta, a lei do defasamento e R2 ficam. A retirada e' decisao da gerencia lida a partir das falas [DECLARADO: o operador ratificou a leitura e nao nomeou a retirada].",
                   "o ramo B (par fonte) deixa de ser a leitura; o ramo A/R2 (pedagio na propagacao) e' a rota viva; nada a abrir em D.", refs=[R_PROJ, R_MASSA],
                   estatuto="REAL (o V1 e a calibracao A lidos por hash a cada rito); INPUT (a leitura do operador); DECLARADO (a retirada do canal); OPEN (a lei de propagacao do pedagio)",
                   defeito="a calibracao A e' NOT_BLIND: corrige a rota (o numero corrige a frase), nao valida nem falsifica; a retirada do canal e' errata ao lado, nao desfecho"))
    T9.append(anot(R_GATE, "v404 SELADA %s: o gate NAO se moveu — o qg_closure do core e' identico ao da v403 (as 18 bandeiras calculadas, a letra do veredito)" % S,
                   f"o registro bandeiras_do_gate_v403 (recriado) selou={selou('bandeiras_do_gate_v403')} com os mesmos valores da v403 selada: das {gvv['n_flags']} bandeiras ({fam[0]} formais, {fam[1]} fisicas, {fam[2]} experimentais) {gvv['n_true']} sao True e {gvv['n_calculated']} sao CALCULADAS ({gvv['n_literal']} literais); o veredito le {gvv['n_read_by_the_verdict']}; a letra do veredito do gate e' a da v403 e a do selo. "
                   "Nenhuma bandeira do gate depende das pedras da v404. [DECLARADO, GV-03 da auditoria de 28/09/2026] As 4 bandeiras experimentais derivam de UM so' booleano; o degrau experimental le so' o rito V11 do piso, unilateral (GV-01).",
                   "a independencia das 4 experimentais e os mocks de survey seguem [OPEN]; o gate nao se move por esta rota.", refs=[R_PROJ],
                   artefatos=[os.path.join(PK, "CANDIDATO_v404.json")], estatuto="REAL (o core do rito); DECLARADO (GV-01, GV-03, EV-12 da auditoria de 28/09/2026); OPEN (a independencia das 4 experimentais)",
                   defeito="o gate nao e' teste e nao discrimina o LCDM raso; NOT_FALSIFIED nunca e' a palavra da creditacao"))
    T9.append(anot(R_BANC, "v404 SELADA %s: o B(n) da v404 e' um passo SIMPLES v403 -> v404 (a Bancada de producao ja' pinava a v403)" % S,
                   f"o kernel da v404 difere do da v403 so' pelas DUAS pedras novas (recibo do kernel KERNEL_RECIBO_v404, contrato R3_2; DIFF_KERNEL_v404.txt: dois modulos novos, TGLExt.lean com as duas linhas de import a mais); o recibo pre_selo foi gerado e pinado ANTES da instalacao, em ensaio contra a producao (nada gravado; a Bancada pinava {bank['deployment_id']}), "
                   f"e a cadeia confere os pinos de PINOS_BN_v404.json na hora; o veredito esperado do aplicar e' REPINADA_B{bank['proxima']}__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_ e sem cadeia de selos, lido do codigo do esboco R3.5 (nao rodado aqui). Parada e religamento do servico exigem V404_AUTORIZACAO_OPERADOR (texto sem o nome do script do servico).",
                   "o B(n) aplicar e' ato do operador (palavra dele, evento c1, parada e religamento do servico); depois do aplicar, a Bancada pina a v404.", refs=[R_PROJ],
                   artefatos=[os.path.join(PK, "PINOS_BN_v404.json"), os.path.join(PK, "PINO_RECIBO_PRE_SELO_v404.json"), KR]))
    T9.append(anot(R_QUADRO, "v404 SELADA %s: o quadro do topo (O Teste da Única Palavra) segue intocado e o registro teste_de_veracidade_fase9_v397 segue selado" % S,
                   f"teste_de_veracidade_fase9_v397 selou={c_q} no rito da v404 (veredito igual ao de ESPERADOS; {tv_v['n_checks']} checagens): o quadro do artigo PT/EN e do .md, conferido contra o resultado pinado, segue no topo, com os numeros e a regra da ordem de sempre: {z444}. "
                   "Nenhum sigma, p ou lnB novo e' calculado nesta rota; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma) vale em todo texto que o cite; o paragrafo do quadro segue no README/site e o handoff da v404 traz tambem o paragrafo novo (Jo 8,32 e a projecao transversal da Meia-Nat), sem o 4,44.",
                   "o paragrafo do README/site e' ato da sessao do site; a creditacao segue sendo beta_TGL na natureza a 5 sigma (nao ha o que repetir deste pacote, a abertura esta consumida).", refs=[R_PROJ]))
    T9.append(anot(R_V403, "v404 SELADA %s: a v403 e' a base selada da v404; o nome do triplo inteiro foi dado (Jo8:32)" % S,
                   f"a v404 parte da v403 selada (um.py {BASE}) e acrescenta DOIS modulos de kernel (ProjecaoTransversalDaMeiaNat e Jo8v32), tres registros com funcao (projecao_transversal_v404, jo8v32_v404, f2b_errata_v404) e dois por spec, e a secao do artigo; os seis registros da v403 (caminho, vida, verdade_adendo, bandeiras_do_gate, cunhagens, kh_n1_cobertura) e os da v402, da v401 e da v399 seguem selados neste rito "
                   f"(caminho_v403 selou={selou('caminho_v403')}, cunhagens_v403 selou={selou('cunhagens_v403')}, falsidade_da_inercia_v401 selou={selou('falsidade_da_inercia_v401')}), como seguem o selo pela propria tecnologia e a declaracao do operador (v399), o sonico e a afinacao (v398) e o quadro (v397); sidecar um_absoluto_selo_acom.json {sc['veredito']} ({sc['n_objetos']} objetos, {sc['recusas']} recusas, sha16 {sc['sha16']}). "
                   "O nome do triplo inteiro, que esta rota (seq %s) deixou com o operador, foi dado em 28/10/2026 (Jo8:32) e a correcao vai AO LADO (ERRATA seguinte, E9), sem tocar nos registros da v403 e sem editar nenhum modulo ja' instalado." % sq_v403,
                   "custodia conjunta da v403 e da v404 pela sessao do site (o handoff lista o sidecar e traz a nota ao lado do paragrafo da v403).", refs=[R_PROJ, R_JO8]))
    T9.append(anot(R_PREP404, "v404 SELADA %s: a preparacao fechou — o rito rodou; a rota da versao selada e' %s" % (S, NOVA),
                   f"o candidato {S} (preparado nesta rota) selou: as {NF} bandeiras novas, a escada {esc0} -> {esc1}, os dois modulos, os tres registros com funcao e os dois por spec, a errata de F2b ao lado e as nove falas de 28/10 por sha256, conferidos pelo conferidor ({conf_dm}; nao pode mudar {conf_np}) e pela leitura da rodada; "
                   "nada do que a preparacao pinou foi alterado entre a preparacao e o selo.", "a custodia (G1), o elo B(n) da Bancada e o registro da rota selada sao os passos seguintes.", refs=[R_PROJ, R_JO8]))
    T9.append(errata(R_V403, sq_v403,
                     f"[E9 · ERRATA AO LADO, gerencia c1, em nome proprio, 28/10/2026, v404 {S}] Corrige o registro seq {sq_v403} desta rota (a v403 selada), que deixa o nome do triplo inteiro com o operador; o mesmo texto esta nos registros da v403 do core (cunhagens_v403, decisao D20), cobertos por esta errata. "
                     f"{corpo('E9')}. Os registros corrigidos NAO foram apagados nem reescritos: a correcao vai ao lado.",
                     refs=[R_JO8, R_PROJ]))
    for x in T9:
        assert x["rota_id"] in ids, "a rota %s nao existe no mapa" % x["rota_id"]
    resumo_conf = ("conferidor %s e %s" % (conf_dm, conf_np)) if "nao lido" not in (conf_dm, conf_np) else "conferidor: o resultado nao veio na leitura desta rodada"
    nomes_curtos = "%s e %s" % (gp["curto"], gj["curto"])
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
            "titulo": "v404 SELADA %s: Jo 8,32 e a projecao transversal da Meia-Nat — o sen 45 do neutrino DERIVADO no kernel (condicional a uma identificacao ONTO), o triplo inteiro com o nome do operador, o canal F2b retirado antes do dado (ao lado); %d modulos de kernel (%s), os registros %s, %s e %s, cunhagens_v404 e kh_n1_cobertura_v404, %d inscricoes de 28/10 por sha256; escada %s -> %s; o gate nao se move" % (
                S, len(GRUPOS), nomes_curtos, gp["nome"], gj["nome"], "f2b_errata_v404", len(verb), esc0, esc1),
            "pergunta": "o candidato v404 selou com os DOIS modulos de kernel (%s; a Meia-Nat e' o angulo de 45 graus e o triplo inteiro tem o nome do operador; as pedras da v403 ficam como registro), os TRES registros com FUNCAO (%s e %s leem do kernel do proprio rito a composicao e a estrela de cada pedra e CALCULAM, com beta = alfa x raiz de e em runtime, um modelo de cada uma; f2b_errata_v404 le o V1 do ramo B por hash e confere o canal retirado antes do dado, AO LADO) "
                        "e os dois por spec (cunhagens_v404: as nove falas do operador de 28/10 embutidas por sha256, as decisoes D23 a D26 e as erratas E7 a E9; kh_n1_cobertura_v404), com os registros da v403, da v402, da v401 e da v399, o selo pela propria tecnologia e o quadro do topo seguindo selados, o sidecar reescrito, a letra do veredito do gate igual a da v403 e nenhum veredito fora da troca dita mudado?" % (
                            nomes_curtos, gp["nome"], gj["nome"]),
            "dados": ["as duas pedras (%s.lean) e a medida da cobertura (KH_N1_v404.json), pinadas por sha256 em insumos (so' lidas)" % ".lean, ".join(G[g]["curto"] for g in GRUPOS),
                      "as nove falas de 28/10 (sha16 %s), por sha256 em insumos\\cunhagens (todas falas do operador)" % ", ".join(falas),
                      "o kernel do rito (a composicao e a estrela de cada pedra e os termos antigos que ela cita), o V1 do ramo B e a calibracao A (lidos por hash), o proprio um.py, o core e o selo da rodada; nenhum dado novo foi aberto nesta rota"],
            "metodo": "ensaio a seco do candidato; um lake build e um Audit no sandbox; rito completo; conferidor (deve mudar / nao pode mudar, com o quadro do topo conferido de novo contra o resultado pinado nas duas linguas e no .md, e os 16 itens C1-C16 do selo mais o round trip do um.py instalado); "
                      "leitura da rodada (inclui o sidecar e a linha final do rito); superficies com a regra da linhagem completa (o MEMORY.md nao e' compactado: recusa por contagem); elo B(n) da Bancada (passo simples v403 -> v404, sem salto; recibos); o paragrafo novo (Jo 8,32 e a projecao transversal da Meia-Nat) e o do quadro, a nota ao lado do paragrafo da v403 e o sidecar, no handoff",
            "resultado": " | ".join([gp["verdict"], gj["verdict"], fk["verdict"], cg["verdict"], kh["verdict"]]) + " | sidecar %s (%s objetos, %s recusas) | %s | %s | escada %s -> %s (teoremas limpos %s/%s; %d bandeiras novas: %s)" % (
                sc["veredito"], sc["n_objetos"], sc["recusas"], resumo_conf, ("%s vereditos fora da troca dita mudaram (exigido 0)" % nvm) if nvm != "nao lido" else "vereditos fora da troca dita: nao lidos nesta leitura", esc0, esc1, ESP["escada"][0], ESP["escada"][1], NF, " + ".join("%d %s" % (G[g]["n_flags"], G[g]["curto"]) for g in GRUPOS)),
            "defeito": "a pedra ProjecaoTransversalDaMeiaNat deriva o sen 45 mas NAO deriva E0 (1 eV, DECLARADO) nem beta, e a identificacao da massa com a projecao transversal e' ONTO (leitura do operador, ratificada) e nao e' termo de kernel; o nome da pedra e' provisorio; a pedra Jo8v32 so' compoe por citacao (nenhuma matematica nova) e a leitura por Jo 8,31-32 e' ONTO; o calculo de cada registro e' numerico em dupla precisao e CONFERE os teoremas, nao os prova; "
                       "a retirada do canal F2b e' decisao da gerencia lida a partir das falas do operador [DECLARADO: o operador ratificou a leitura e nao nomeou a retirada], e a calibracao A e' NOT_BLIND (corrige a rota, nao valida nem falsifica); o plano e a leitura que o operador ratificou foram os apresentados na sessao: esta cadeia guarda a ratificacao verbatim, nao a apresentacao [DECLARADO]; "
                       "o gate nao se moveu e a independencia das 4 bandeiras experimentais segue aberta (derivam de UM so' booleano) [DECLARADO, GV-01 e GV-03]; as pendencias H_BW, H_cal, H3, a assinatura e rank c = 4 (v403) seguem abertas; a pendencia [LEGAL] (D2 e CC art. 125) segue do operador com a agente de PI; nao e' teste: nao ha desfecho experimental; a revisao independente do candidato e da cadeia nao esta afirmada (preparacao: seq %s)" % sq_prep,
            "nao_refazer": "a integracao dos dois modulos e a escada %s -> %s estao medidas; o calculo e a leitura de cada pedra no kernel do rito estao feitos e conferidos contra o um.py instalado; repetir os registros so' com kernel ou um.py novo; nao reabrir D23 a D26; pedra selada nao se renomeia por cima; nao reabrir o canal F2b (retirado antes do dado; o V1 fica congelado por hash)" % (esc0, esc1),
            "proximo_passo": "E0 e a lei de propagacao do pedagio de Planck (operador); o elo B(n) da Bancada Um (palavra do operador; passo simples v403 -> v404); decisao [LEGAL] D2 com a agente de PI; custodia conjunta pela sessao do site (o handoff traz o paragrafo novo, o do quadro e a nota ao lado do da v403, e lista o sidecar); commit/push (operador); revisao independente do candidato e da cadeia (quem construiu nao aprova); as pendencias H_BW, H_cal e H3 e a independencia das 4 experimentais como proximas frentes",
            "onde": PK, "artefatos": arts, "refs": sorted(set(x["rota_id"] for x in T9) | set(REFS) | set(preparo_no_livro(ids)) - {NOVA}),
            "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move; as erratas E7 a E9 e as decisoes D23 a D26 sao da gerencia c1, em nome proprio, ao lado (nada foi apagado nem reescrito); %s." % sim(c_seguem, "os %d registros anteriores conferidos (v403, v402, v401, quadro, selo, declaracao, sonico, afinacao e as cunhagens) seguem selados" % len(seguem), "ATENCAO: algum registro anterior NAO selou")}
    for r in ROTA["refs"]:
        assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
    REG = [ROTA] + T9
    bad = [(x["rota_id"], violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad, "a guarda de texto (P18) achou violacao(oes): %r" % bad
    atrib = [(x["rota_id"], T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))]
    assert not atrib, "a direcao do testemunho esta invertida ou a atribuicao falhou: %r" % atrib
    ruins = regra_4_44(REG, z, p)
    assert not ruins, "a regra do 4,44 (o p calibrado e a linha dos 5 sigma no mesmo campo) falhou em: %r" % ruins[:3]
    assert c_seguem and c_q, "algum registro anterior (quadro, v403, falsidade, ponte, queda, esperanca, selo, declaracao, sonico, afinacao) nao selou no core: o mapa nao registra a v404 assim"
    return REG


def gravar(p, b):
    """backup de BYTES se existir e mudar; temporario -> conferir tamanho -> substituir."""
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m404"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_m404"; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def main():
    V, PROB = L.ler()
    if PROB:
        print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); return 2
    NOS = L.NOS
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v404_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v404_*.json")), key=os.path.getmtime)
    arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto_selo_acom.json"), os.path.join(PK, "ESPERADOS_v404.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v404.json"),
            os.path.join(PK, "DIFF_KERNEL_v404.txt"), os.path.join(PK, "DIFF_v403_v404.diff"), os.path.join(NOS, "HANDOFF_v404_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v404.json"),
            os.path.join(PK, "insumos", "ProjecaoTransversalDaMeiaNat.lean"), os.path.join(PK, "insumos", "Jo8v32.lean"), os.path.join(PK, "kernel", "KERNEL_RECIBO_v404.json")] + b3[-1:]
    arts = [x for x in arts if os.path.exists(x)]
    REG = montar(V, core, selo, ids_do_livro(), arts)
    J = os.path.join(HERE, "registro_mapa_v404.json")
    gravar(J, json.dumps(REG, ensure_ascii=False, indent=1).encode("utf-8"))
    quem = "claude-c1 (gerência), cadeia v404"
    print("registro MONTADO (NAO registrado): %d registro(s) (%s) -> %s" % (len(REG), ", ".join(x["tipo"] for x in REG), J))
    print("COMANDO (ato da gerencia): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
    print("DEPOIS DO REGISTRO: rodar de novo os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
