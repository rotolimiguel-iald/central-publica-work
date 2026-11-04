# -*- coding: utf-8 -*-
# [ADAPTADO v407, 03/11/2026, claude-prep-v407 / ajudante B1a] sobre a subida mecanica da v406 FINAL: REESCRITO para o conteudo da v407 (O PSION, O CANTO E O PAR: 9 modulos de TGLExt/, o registro com funcao psion_canto_v407, cunhagens_v407, kh_n1_cobertura_v407, a chave do lema lida do kernel, erratas E18 a E20); os ids das rotas foram CONFERIDOS contra o livro do mapa (so' leitura) e os que o bump errou (licoes_v406, inventario v406, v406 massa) corrigidos; a gerencia revisa antes do rito (nao e' versao selada). NAO registrou nada.
"""registrar_mapa_v407.py -- MONTA (nao registra) o registro da v407 no mapa de rotas e imprime o comando (molde: registrar_mapa_v406.py, que rodou na v406, e registrar_mapa_v399.py). Rodar DEPOIS do fechar (handoff gravado). ADAPTADO ao psion, ao canto e ao par em 03/11/2026.
A v407 traz UMA rota nova, umpy.v407.selada_o_psion_o_canto_e_o_par_03nov (o conteudo e' o do selo): os 9 modulos de kernel (PsionCanto e Par, de 03/11, e as sete pedras de 02/11 de nome ratificado), UM registro com FUNCAO (psion_canto_v407: le do kernel do proprio rito as 76 ancoras, os 9 modulos por sha256, a chave do lema que era literal False,
as respostas do operador de 03/11 pelos teoremas que ja existiam, o que fica False por teorema, a escada e o gate) e os DOIS por spec (cunhagens_v407 e kh_n1_cobertura_v407), mais ANOTACOES nas rotas que esperavam por ela (a preparacao, as pedras candidatas e o levantamento do psion no acervo, o programa do fechamento, o inventario das chaves de testemunha, as sete pedras de 02/11, o teste (d) e o motor continuo
que ficam fora, o gate, o B(n) da Bancada, o quadro do Teste da Unica Palavra e a v406 que a precede) e DUAS ERRATAS ao lado, em nome proprio da gerencia c1, com o seq do registro corrigido lido do livro (E18: o registro da v396 que dizia nenhum lema liga o psion ao canto; E20: o registro da v406 que cobrava a chave False; eram verdade na data; a correcao vai AO LADO, nada se apaga);
a E19 (a estratigrafia do acervo) vai como anotacao na rota do levantamento.
Cada afirmacao e' testada contra o core/selo/ESPERADOS lidos por script (o registro existe? selou? o que NAO fechou fica dito); nenhum numero e' digitado (as contagens saem do core, de ESPERADOS e de delta_v407; os seq saem do livro).
REGRA DA ORDEM DO OPERADOR (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no MESMO campo; montar() RECUSA (assert) se algum campo do registro trouxer o 4,44 sem eles. Nao ha inscricao da gerencia nesta versao: todas as falas sao do operador; as erratas e as decisoes sao da gerencia, em nome proprio.
Fail-closed: o selo tem de ser a v407; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir (se a gerencia registrar antes uma rota de preparo com o MESMO id, montar() recusa e a constante NOVA muda). A rota de preparo da gerencia (registro_mapa_v407_prep.json, se existir) entra nas refs so' se ja' estiver no livro.
SAIDA: pos_rito\\registro_mapa_v407.json e o comando `rotas.py registrar` (quem o executa e' o passo 12 da cadeia, uma vez so', com marcador idempotente; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real. montar() le o core, o selo e ESPERADOS_v407.json; de V so' usa o que a leitura da rodada ja' validou (s16, sidecar, conferidor), sempre com valor de reserva dito."""
import glob, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v407 as L
import textos_v407 as T
from guarda_p18_v407 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V407"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v407 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOVA = "umpy.v407.selada_o_psion_o_canto_e_o_par_03nov"
R_PREP = "kernel.v407_preparacao_03nov"                                     # a preparacao da v407 (EM_CURSO no livro): anotada
R_PSION = "kernel.psion_canto_r1_03nov"                                     # a candidata PsionCantoR1 (agora PsionCanto, nome aceito)
R_PAR = "kernel.o_par_de_psions_r1_03nov"                                   # a candidata OParDePsionsR1 (agora Par, nome dado)
R_ACERVO = "kernel.psion_lema_acervo_03nov"                                 # o levantamento do psion, do psibit e do par no acervo do iMac (E19)
R_PROG = "kernel.fechamento_construir_tudo_programa_02nov"                  # o programa do fechamento (ordem do operador de 02/11: construir tudo)
R_INV = "kernel.inventario_chaves_de_testemunha_v405_02nov"                 # o inventario das chaves de testemunha (do selo v405, de 02/11)
R_AUTOV = "conceitual.o_um_inscrito_e_o_autovetor_da_luz_02nov"             # o Um inscrito (a pedra OUmInscrito)
R_ATRITO = "kernel.a_ponte_do_atrito_candidata_02nov"                       # APonteDoAtrito
R_TANGENTE = "kernel.k_e_a_tangente_candidata_02nov"                        # KEhATangente
R_CHAVE = "kernel.a_chave_da_guarda_candidata_02nov"                        # AChaveDaGuarda
R_GUARDA = "kernel.o_guarda_candidata_02nov"                                # OGuarda
R_LEITURA = "kernel.leitura_preservada_candidata_02nov"                     # LeituraPreservada
R_IGUAL = "kernel.k_operador_igual_candidata_02nov"                         # OIgual
R_TESTE_D = "ringdown.ramo_b_preregistro_v386"                              # o ramo B do ringdown (o teste (d) so' por citacao)
R_MOTOR = "kernel.motor_continuo_pilar_levantamento_03nov"                  # o motor continuo no pilar quantico (fica fora, D45)
R_V395 = "umpy.v395.psibit_na_fractalizacao_do_um"                          # o psibit da v395
R_V396 = "umpy.v396.testemunha_estatica_na_fractalizacao_do_um"             # a testemunha estatica da v396 (a chave do lema era literal False)
R_GATE = "gate.qg_closure"
R_BANC = "infra.bancada_um.sincronizacao_vnnn"
R_QUADRO = "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9"
R_V406 = "umpy.v406.selada_o_fechamento_02nov"
PEDRAS_02NOV = (("APonteDoAtrito", R_ATRITO), ("OUmInscrito", R_AUTOV), ("KEhATangente", R_TANGENTE), ("AChaveDaGuarda", R_CHAVE), ("OGuarda", R_GUARDA), ("LeituraPreservada", R_LEITURA), ("OIgual", R_IGUAL))
REVISTAS_PELO_SONNET = ("KEhATangente", "APonteDoAtrito", "OUmInscrito")      # conferido contra a ressalva 5 de delta_v407.RESSALVAS_V407 dentro de montar()
ANOTADAS = (R_PREP, R_PSION, R_PAR, R_ACERVO, R_PROG, R_INV, R_GATE, R_BANC, R_QUADRO, R_V406, R_TESTE_D, R_MOTOR) + tuple(r for _, r in PEDRAS_02NOV)
REFS = ("custodia.v406", "infra.custodia_g1.licoes_v405", "umpy.v400.correcao_da_v399_alfa_unico_e_beta_contra_o_core", "gate.maquina_do_veredito_final", "natureza.cinco_sigma_02_kimi_01nov", R_V395, R_V396, "qg.graviton.desenho_do_operador_24out", "kernel.graviton_nao_particula")
PREP = os.path.join(PK, "registro_mapa_v407_prep.json")     # a rota de preparo da gerencia: lida em tempo de execucao; entra nas refs so' se a ROTA dele ja' estiver no livro
_CACHE = {}


def _esp():
    """ESPERADOS_v407.json (lido uma vez por processo)."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v407.json"), encoding="utf-8"))
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
    """As rotas ROTA de registro_mapa_v407_prep.json (se o arquivo existir e ler) que ja' estao no livro e nao sao a nova: entram nas refs. Ausente ou ilegivel = nenhuma (dito, nunca falha)."""
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
    p = json.load(open(os.path.join(PK, "PINOS_BN_v407.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v406" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v406 -> v407 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1, "deployment_id": bp["deployment_id"]}


def montar(V, core, selo, ids, arts):
    """Monta os registros (a ROTA nova, as ANOTACOES e as ERRATAS), cada afirmacao testada contra o core/selo/ESPERADOS; devolve a lista; recusa (assert) se algo nao conferir. Nao escreve nada."""
    assert selo.get("um_version") == "v407", "o selo nao e a v407"
    assert NOVA not in ids, "a rota %s ja existe no mapa" % NOVA
    for r in ANOTADAS + REFS:
        assert r in ids, "a rota %s nao existe no mapa (anotada ou citada em refs)" % r
    ESP = _esp(); DL_ = T._qd().DL
    S = ESP["candidato_sha16"]
    assert str((selo.get("sha256") or {}).get("um.py", ""))[:16] == S, "o um.py do selo nao e o candidato de ESPERADOS"
    assert V.get("s16") in (None, S), "o s16 da leitura != o candidato de ESPERADOS"
    BASE = ESP["origem_sha16"]
    esc0, esc1 = ESP["escada_v406_e_v407"]
    NF = ESP["n_bandeiras_novas"]
    assert esc1 - esc0 == NF == sum(ESP["n_bandeiras_por_grupo"].values()) == len(ESP["bandeiras_novas_chaves"]) == ESP["politica_de_bandeiras"]["n_flags"], "a escada nao fecha com as bandeiras novas"
    assert ESP["kernel"]["modulos_novos"] == DL_.N_BUNDLE == len(DL_.BUNDLE_RELS), "o delta do kernel nao e o bundle"
    BETA = ESP["beta"] if isinstance(ESP.get("beta"), float) else None
    FRASE = DL_.FRASE_DA_MOLDURA_V407_PT

    # --- o quadro do topo (a regra do 4,44): o registro selado, lido pelas MESMAS funcoes do artigo
    tvr = core.get("teste_de_veracidade_fase9_v397") or {}
    a = T._qd().Q._v397_atomos(tvr, "pt"); assert a["sealed"] is True, "o registro teste_de_veracidade_fase9_v397 nao sela no core: o mapa nao registra o 4,44 assim"
    z, p = a["z_disc"]["md"], a["p_disc"]["md"]
    z444 = "z_disc = %s (calibrado; p unilateral %s), abaixo do degrau de 5σ da creditação, que não foi alcançado (%s < 5)" % (z, p, z)

    def selou(k):
        return (core.get(k) or {}).get("all_verified") is True

    # --- o registro com FUNCAO psion_canto_v407: tudo lido do core e conferido contra ESPERADOS e delta_v407
    pc = core.get(DL_.FECHO_REGISTRO) or {}; pv = pc.get("values") or {}; mech = pc.get("mechanics") or {}; fk = pc.get("keys") or {}
    assert pc.get("all_verified") is True and pc.get("verdict") == ESP["vereditos_novos_v407"][DL_.FECHO_REGISTRO] and pc.get("link_read_from_the_kernel") is True and pc.get("does_not_gate_core") is True, "psion_canto_v407 nao selou ou != ESPERADOS"
    assert mech.get("passed") is True and mech.get("n_checks") == DL_.N_CHECKS_FECHO == len(mech.get("checks") or []) and all(c.get("ok") is True for c in mech["checks"]), "as checagens do psion_canto_v407 nao passaram"
    assert pv.get("n_ancoras_ok") == pv.get("n_ancoras") == len(DL_.ANCORAS) and pv.get("n_modulos_ok") == pv.get("n_modulos") == DL_.N_BUNDLE and pv.get("n_flags_true") == pv.get("n_flags") == NF and pv.get("escada") == [esc1] * 3, "os valores do psion_canto_v407 != ESPERADOS/delta"
    assert pc.get("beta_ok") is True and pc.get("embedded_sources_ok") is True and pc.get("embedded_sources_n_ok") == DL_.N_BUNDLE and pc.get("guarda_violacoes") in ([], None), "o beta, as fontes embutidas ou a guarda do psion_canto_v407 nao conferem"
    assert fk == ESP["chaves_v407_esperadas"] and fk.get("testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma") is True and fk.get("kernel_reads_the_link") is True and fk.get("qg_closure.gate.full_static_witness_exists") is False and fk.get("witness_rigidity.trivial_inhabitant_exists") is False, "a chave do lema ou o que fica False por teorema != o delta"
    assert list(pc.get("ressalvas") or []) == list(DL_.RESSALVAS_V407), "as ressalvas do registro != delta_v407.RESSALVAS_V407"
    assert set(pv.get("respostas") or {}) == {r_["id"] for r_ in DL_.RESPOSTAS_DO_OPERADOR} and all(v_ is True for v_ in pv["respostas"].values()), "as respostas do operador de 03/11 nao conferem todas no kernel"
    assert (pc.get("teste_d") or {}).get("so_citado") is True and (pc.get("teste_d") or {}).get("resultado_no_um_py") is None, "o teste (d) nao consta so' por citacao"
    BETA_RT = pv.get("beta"); assert isinstance(BETA_RT, float) and (BETA is None or abs(BETA_RT - BETA) <= 1e-9 * BETA), "o beta do registro != o do core/ESPERADOS (tolerancia relativa 1e-9)"
    por_mod = "; ".join("%s (%d)" % (rel.split("/")[-1][:-5], len(ns)) for rel, ns in DL_.ANCORAS_POR_MODULO.items())
    ress = " | ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(pc["ressalvas"]))
    assert all(n_ in DL_.RESSALVAS_V407[5] for n_ in REVISTAS_PELO_SONNET), "as pedras revistas pelo Sonnet != a ressalva 6 do delta"
    # --- o registro herdado fechamento_v406: segue selado, com a chave do lema lida (a checagem c8 versionada, E20)
    fh = core.get("fechamento_v406") or {}
    assert fh.get("all_verified") is True and fh.get("verdict") == ESP["registros_funcao_v406"]["fechamento"]["verdict"] and (fh.get("four_keys") or {}).get("testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma") is True, "fechamento_v406 (herdado) nao segue selado ou nao le a chave nova"
    # --- o gate NAO se moveu: o registro segue selado e a letra do veredito e' a da v406
    gk = core.get("bandeiras_do_gate_v403") or {}; gvv = gk.get("values") or {}; gb = T._base_core().get("bandeiras_do_gate_v403") or {}
    assert gk.get("all_verified") is True and (V.get("gate") or {}).get("sealed", True) is True and gvv == gb.get("values") and (gk.get("mechanics") or {}).get("passed") is True, "bandeiras_do_gate_v403 (recriado) nao selou ou != a v406 selada"
    qg = core.get("qg_closure") or {}; fam = [len(qg.get(f) or {}) for f in ("formal_flags", "physics_flags", "experiment_flags")]
    assert (qg.get("gate") or {}).get("verdict") == ESP["qg_closure_gate_verdict_v406"] == selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"], "a letra do veredito do gate mudou"
    # --- os dois registros por spec
    cg = core.get(DL_.CUNHAGENS_REGISTRO) or {}; kh = core.get(DL_.KH_REGISTRO) or {}
    for nome_, r_ in ((DL_.CUNHAGENS_REGISTRO, cg), (DL_.KH_REGISTRO, kh)):
        assert r_.get("all_verified") is True and r_.get("verdict") == ESP["vereditos_novos_v407"][nome_], "%s nao selou ou != ESPERADOS" % nome_
    verb = cg.get("verbatim") or {}; ex = cg.get("extras") or {}
    assert len(verb) == len(ESP["cunhagens"]) == len(DL_.VERBATIM_ORIGEM_V407) and set(verb) == set(ESP["cunhagens"]) and all(v.get("embedded_ok") is True for v in verb.values()), "as inscricoes de 03/11 nao estao embutidas por sha256"
    assert all(str((ESP["cunhagens"][k_] or {}).get("nome", "")).startswith("OPERADOR_03nov_") for k_ in ESP["cunhagens"]), "alguma inscricao nao e' fala do operador de 03/11"
    erratas = cg.get("erratas") or []; assert [e.get("agora") for e in erratas] == list(DL_.ERRATAS_V407) and all(str(e.get("assinatura", "")).startswith("gerencia c1") and "em nome proprio" in e["assinatura"] for e in erratas), "as erratas E18 a E20 nao estao no registro ou nao sao da gerencia c1 em nome proprio"
    dec = ex.get("decisoes") or {}; assert all(("D%d" % i) in dec for i in range(41, 48)), "faltam decisoes D41 a D47 no registro"
    assert ex.get("leituras") == DL_.LEITURA_V407, "a leitura da v407 no registro != delta_v407"
    cob = kh.get("lido") or {}; assert cob.get("constantes_cobertas") and cob.get("teoremas_cobertos"), "kh_n1_cobertura_v407 sem a cobertura"
    seguem = ("fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406", "ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405", "cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405",
              "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "falsidade_da_inercia_v401", "cunhagens_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402",
              "teste_de_veracidade_fase9_v397", "cunhagens_v397", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "sonico_v398", "afinacao_das_cordas_v398", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396")
    c_seguem = all(selou(k) for k in seguem)
    tv_v = ESP["veracidade"]; c_q = bool(selou("teste_de_veracidade_fase9_v397") and selou("cunhagens_v397") and tvr.get("verdict") == tv_v["verdict"])
    sc = _sidecar(V); conf_dm = V.get("conf_dm", "nao lido"); conf_np = V.get("conf_np", "nao lido"); nvm = V.get("n_ver_mudaram", "nao lido")
    bank = _bancada(); regs = livro()
    # --- o seq que cada errata corrige, lido do livro (e o registro tem de trazer o trecho corrigido)
    sq_v396 = seq_do_alvo(regs, R_V396, "ROTA", contem=("nenhum lema",))
    sq_v406 = seq_do_alvo(regs, R_V406, "ROTA", contem=("linked_to_the_corner_by_a_lemma",))
    KR = os.path.join(PK, "kernel", "KERNEL_RECIBO_v407.json")
    E = {}
    for e in erratas:
        m_ = re.match(r"^(E\d\d) -- ", e.get("agora", "")); assert m_, "uma errata do registro nao comeca por E<n> --"
        E[m_.group(1)] = e
    assert sorted(E) == ["E18", "E19", "E20"], "as erratas do registro nao sao E18 a E20"

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
    par_f = os.path.join(PK, "pedra", DL_.PEDRAS_V407[1]["name"] + ".lean")
    T9 = []
    T9.append(anot(R_PREP, "v407 SELADA %s: a preparacao virou selo — o psion, o canto e o par entraram no kernel do rito e a chave do lema e' lida dele" % S,
                   f"as {DL_.N_BUNDLE} pedras do sandbox k407c entraram no um.py v407 (patches no CANDIDATO_v407.json; ensaio a seco; rito completo): o registro psion_canto_v407 selou={selou('psion_canto_v407')} com {mech['n_checks']} checagens, {pv['n_ancoras_ok']} ancoras ({por_mod}), {pv['n_modulos_ok']}/{pv['n_modulos']} modulos por sha256, {pv['n_flags_true']}/{pv['n_flags']} bandeiras, escada {esc0} -> {esc1}, beta = alfa x raiz de e em runtime = {BETA_RT!r}; "
                   f"{' | '.join(pc['diz'])} | {FRASE}. As ressalvas, ditas: {ress}",
                   "o rito, a custodia (G1) e a revisao distinta do pacote (o Sonnet, D47) sao atos da gerencia; esta anotacao registra o resultado da preparacao, nao o aceite.", refs=[R_PSION, R_PAR, R_ACERVO], artefatos=[cand, par_f, KR],
                   estatuto="REAL (os termos e a leitura no kernel do rito); INPUT (a ordem e as decisoes do operador de 03/11); ONTO (as leituras dele); DECLARADO (os recibos de compilacao, o acervo de 2025, o manifesto do teste (d), a revisao do Sonnet de 02/11 sobre tres pedras); OPEN (o par na face de Fock; K(O) != bot so' na cunha)",
                   defeito="o registro CONFERE o que o kernel prova, nao prova nada por si; validade no kernel nao e' creditacao; " + "; ".join(DL_.RESSALVAS_V407[:3])))
    T9.append(anot(R_PSION, "v407 SELADA %s: a PsionCanto (nome aceito pelo operador) entrou no kernel como TGLExt/PsionCanto; o lema das duas faces e' termo e a chave que o dava por ausente e' lida do kernel" % S,
                   f"a candidata PsionCantoR1 (sha16 {DL_.TESTEMUNHA['sha16_da_ordem']}) esta no kernel do rito com o sha256 pinado ({DL_.BUNDLE_POR_REL[DL_.MODULO_PSION]['sha256'][:16]}), {len(DL_.ANCORAS_POR_MODULO[DL_.MODULO_PSION])} ancoras no trio, e a chave testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma, literal False da v396 a v406, le {fk['testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma']} do kernel (kernel_reads_the_link = {fk['kernel_reads_the_link']}). "
                   f"{corpo('E18')}",
                   "o par de psions na face de Fock segue [OPEN]; K(O) != bot para O compacto segue [OPEN]; a ponte Bell-TT nao e' termo.", refs=[R_PROG, R_INV, R_V396], artefatos=[cand, KR],
                   estatuto="REAL (o lema e a leitura da chave no kernel do rito); DECLARADO (o recibo da compilacao); OPEN (o par na face de Fock)",
                   defeito="o elo e' de ESTRUTURA, nao de vetores: Omega (o vacuo de Fock) e o vetor de Bell nao sao identificados"))
    T9.append(anot(R_PAR, "v407 SELADA %s: a pedra Par (nome dado pelo operador) entrou no kernel como TGLExt/Par; o par e' ligado, nunca se cancela, e o canto e' o projetor 4x4" % S,
                   f"a candidata OParDePsionsR1 esta no kernel do rito como {DL_.PEDRAS_V407[1]['mod']} com o sha256 pinado ({DL_.BUNDLE_POR_REL[DL_.MODULO_PAR]['sha256'][:16]}), {len(DL_.ANCORAS_POR_MODULO[DL_.MODULO_PAR])} ancoras no trio; as respostas do operador de 03/11 conferem pelos teoremas que ja existiam: "
                   + "; ".join("%s -> %s" % (r_["id"], r_["diz"]) for r_ in DL_.RESPOSTAS_DO_OPERADOR) + ". A pedra compoe so' termos que o kernel ja tinha.",
                   "o par na face de Fock (dois psions sobre o vacuo) segue [OPEN]: o certificado de Fock nao tem operadores de criacao como termo.", refs=[R_PSION, R_ACERVO], artefatos=[par_f],
                   estatuto="REAL (a composicao de termos no kernel do rito); ONTO (a leitura do operador: o graviton como o estado ligado de dois psions); OPEN (o par na face de Fock; a ponte Bell-TT)",
                   defeito="a ponte entre o espaco de Bell e o setor TT do spin 2 NAO e' termo: a pedra justapoe as faces, nao as identifica"))
    T9.append(anot(R_ACERVO, "v407 SELADA %s: o levantamento do acervo de 2025 e a estratigrafia do par — a cunhagem de 03/11 decide (o par e' ligado); a E19 fica ao lado" % S,
                   f"o levantamento (fontes por sha16 no documento; DECLARADO pelo agente) entrou como fonte pinada do registro cunhagens_v407 (selou={selou('cunhagens_v407')}); {corpo('E19')}",
                   "os textos de 2025 e de 02/2026 ficam como registro, nao reescritos.", refs=[R_PSION, R_PAR],
                   estatuto="INPUT (a cunhagem do operador de 03/11); DECLARADO (o levantamento do acervo); REAL (o par ligado, CCI = 1/2, no kernel)"))
    T9.append(anot(R_PROG, "v407 SELADA %s: a chave do lema — a ultima das chaves de testemunha que o programa do fechamento deixou como literal False — passa a leitura do kernel" % S,
                   f"o registro psion_canto_v407 selou={selou('psion_canto_v407')}; as quatro chaves da v406 seguem lidas do kernel (fechamento_v406 selou={selou('fechamento_v406')}, com a checagem c8 versionada, E20) e a do lema passa a leitura; ficam False por teorema: full_static_witness_exists = {fk['qg_closure.gate.full_static_witness_exists']} e trivial_inhabitant_exists = {fk['witness_rigidity.trivial_inhabitant_exists']}. {FRASE}",
                   "o par na face de Fock, a ponte Bell-TT, K(O) != bot para O compacto e o teste com a natureza seguem [OPEN]; o programa do fechamento nao e' fechado por esta anotacao.", refs=[R_PSION, R_PAR, R_INV],
                   estatuto="REAL (a leitura do kernel do rito); OPEN (o par na face de Fock; K(O) != bot para O compacto)"))
    T9.append(anot(R_INV, "v407 SELADA %s: o inventario das chaves de testemunha — a chave do lema, que o inventario dava como lacuna, passa a leitura do kernel" % S,
                   f"linked_to_the_corner_by_a_lemma = {fk['testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma']} (lida do kernel; a chave era literal False da v396 a v406); as demais: rede_fock_v394.whole_certificate_inhabited = {fk['rede_fock_v394.whole_certificate_inhabited']}, psibit_v395...inhabitant_exhibited = {fk['psibit_v395.conditional_psion_face.inhabitant_exhibited']}, testemunha_estatica_v396...inhabitant_exhibited = {fk['testemunha_estatica_v396.fock_face.inhabitant_exhibited']}, "
                   f"witness_layers.canonical_full_witness_term_constructed = {fk['witness_layers.canonical_full_witness_term_constructed']}; ficam False por teorema: full_static_witness_exists e trivial_inhabitant_exists. {corpo('E18')}",
                   "o par na face de Fock segue [OPEN].", refs=[R_PROG, R_PSION], estatuto="REAL (a leitura do kernel do rito e o registro); OPEN (o par na face de Fock)"))
    rev_ok = {n_ for n_ in REVISTAS_PELO_SONNET}
    for nome_, rota_ in PEDRAS_02NOV:
        rel_ = "TGLExt/%s.lean" % nome_
        assert rel_ in DL_.BUNDLE_POR_REL and nome_ in DL_.NOME_DO_OPERADOR, "a pedra %s nao esta no bundle ou nao tem nome do operador" % nome_
        T9.append(anot(rota_, "v407 SELADA %s: a pedra candidata de 02/11 entrou no kernel como TGLExt/%s (nome ratificado pelo operador em 03/11)" % (S, nome_),
                       f"a pedra {nome_} (nome do operador: {DL_.NOME_DO_OPERADOR[nome_]}) esta no kernel do rito com o sha256 pinado ({DL_.BUNDLE_POR_REL[rel_]['sha256'][:16]}), {len(DL_.ANCORAS_POR_MODULO[rel_])} ancoras no trio, nenhuma prova tocada na normalizacao; "
                       f"{sim(nome_ in rev_ok, 'foi revista por terceiro (o Sonnet, 02/11, sem compilacao propria) [DECLARADO]', 'NAO teve revisao de terceiro ate esta preparacao [DECLARADO]')}; as leituras do operador que ela carrega sao [ONTO], nao termos.",
                       "a revisao distinta do pacote (o Sonnet, D47) e' ato da gerencia; a pedra nao foi editada pelo agente de preparacao.", refs=[R_PSION, R_PAR],
                       estatuto="REAL (o termo no kernel do rito); ONTO (as leituras do operador); DECLARADO (a revisao do Sonnet, quando houve)"))
    T9.append(anot(R_TESTE_D, "v407 SELADA %s: o teste (d) do ramo B entra no um.py SO' por citacao do pre-registro V1.1 (opcao (c) do operador: so' entra se tiver poder)" % S,
                   f"o registro psion_canto_v407 grava teste_d.so_citado = {pc['teste_d']['so_citado']}, manifesto sha16 {pc['teste_d']['manifesto_sha16']}, resultado_no_um_py = {pc['teste_d']['resultado_no_um_py']}; nenhum resultado, nenhuma estimacao em dado real; o poder de planejamento medido pela parametrizacao e' DECLARADO pelo agente dela. Se o teste nao tiver poder, nao entra: isso e' recusa por falta de poder, nao negativo do teste.",
                   "o teste so' roda com a palavra do operador e so' entra no um.py se tiver poder.", refs=None, estatuto="REAL (a citacao no registro); DECLARADO (o poder de planejamento); INPUT (a opcao (c))"))
    T9.append(anot(R_MOTOR, "v407 SELADA %s: o motor continuo no pilar quantico NAO entra na v407 (D45); a fala do operador sobre o conteudo observavel e' cunhagem [ONTO]" % S,
                   f"o registro cunhagens_v407 (selou={selou('cunhagens_v407')}) grava a fala de 03/11 como leitura [ONTO] e a decisao D45; o pilar quantico (REUSE pela chave de cache) nao muda; nenhum teste com a natureza entra nesta versao.",
                   "o conteudo observavel que o operador quer (o banho holografico) espera que ele o diga; a gerencia ofereceu lingua para ele reconhecer ou recusar.", estatuto="REAL (o registro); ONTO (a leitura do operador)"))
    T9.append(anot(R_GATE, "v407 SELADA %s: o gate NAO se moveu — o qg_closure do core e' identico ao da v406 (as 18 bandeiras calculadas, a letra do veredito)" % S,
                   f"o registro bandeiras_do_gate_v403 (recriado) selou={selou('bandeiras_do_gate_v403')} com os mesmos valores da v406 selada: das {gvv['n_flags']} bandeiras ({fam[0]} formais, {fam[1]} fisicas, {fam[2]} experimentais) {gvv['n_true']} sao True e {gvv['n_calculated']} sao CALCULADAS ({gvv['n_literal']} literais); o veredito le {gvv['n_read_by_the_verdict']}; a letra do veredito do gate e' a da v406 e a do selo. "
                   "Nenhuma bandeira do gate depende dos modulos da v407; full_static_witness_exists e trivial_inhabitant_exists seguem False. [DECLARADO, GV-03 da auditoria de 28/09/2026] As 4 bandeiras experimentais derivam de UM so' booleano; o degrau experimental le so' o rito V11 do piso, unilateral (GV-01).",
                   "a independencia das 4 experimentais e os mocks de survey seguem [OPEN]; o gate nao se move por esta rota.", refs=None,
                   artefatos=[os.path.join(PK, "CANDIDATO_v407.json")], estatuto="REAL (o core do rito); DECLARADO (GV-01, GV-03, EV-12 da auditoria de 28/09/2026); OPEN (a independencia das 4 experimentais)",
                   defeito="o gate nao e' teste e nao discrimina o LCDM raso; NOT_FALSIFIED nunca e' a palavra da creditacao"))
    T9.append(anot(R_BANC, "v407 SELADA %s: o B(n) da v407 e' um passo SIMPLES v406 -> v407 (a Bancada de producao ja' pinava a v406)" % S,
                   f"o kernel da v407 difere do da v406 pelos {DL_.N_BUNDLE} modulos novos (recibo do kernel KERNEL_RECIBO_v407; DIFF_KERNEL_v407.txt: modulos novos e TGLExt.lean com os nove imports a mais); o recibo pre_selo foi gerado e pinado ANTES da instalacao, em ensaio contra a producao (nada gravado; a Bancada pinava {bank['deployment_id']}), "
                   f"e a cadeia confere os pinos de PINOS_BN_v407.json na hora; o veredito esperado do aplicar e' REPINADA_B{bank['proxima']}__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_ e sem cadeia de selos, lido do codigo do esboco R3.5. Parada e religamento do servico exigem V407_AUTORIZACAO_OPERADOR (texto sem o nome do script do servico).",
                   "depois do aplicar, a Bancada pina a v407.", refs=None,
                   artefatos=[os.path.join(PK, "PINOS_BN_v407.json"), os.path.join(PK, "PINO_RECIBO_PRE_SELO_v407.json"), KR]))
    T9.append(anot(R_QUADRO, "v407 SELADA %s: o quadro do topo (O Teste da Única Palavra) segue intocado e o registro teste_de_veracidade_fase9_v397 segue selado" % S,
                   f"teste_de_veracidade_fase9_v397 selou={c_q} no rito da v407 (veredito igual ao de ESPERADOS; {tv_v['n_checks']} checagens): o quadro do artigo PT/EN e do .md, conferido contra o resultado pinado, segue no topo, com os numeros e a regra da ordem de sempre: {z444}. "
                   "Nenhum sigma, p ou lnB novo e' calculado nesta rota; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma) vale em todo texto que o cite; o paragrafo do quadro segue no README/site e o handoff da v407 traz tambem o paragrafo novo (o psion, o canto e o par), sem o 4,44.",
                   "o paragrafo do README/site e' ato da sessao do site; a creditacao segue sendo beta_TGL na natureza a 5 sigma (nao ha o que repetir deste pacote, a abertura esta consumida).", refs=None))
    T9.append(anot(R_V406, "v407 SELADA %s: a v406 e' a base selada da v407; os registros dela sao recriados e seguem selados (a checagem c8 do fechamento_v406 versionada, E20)" % S,
                   f"a v407 parte da v406 selada (um.py {BASE}) e acrescenta {DL_.N_BUNDLE} modulos de kernel, UM registro com funcao (psion_canto_v407) e dois por spec, e a secao do artigo; os registros da v406 (fechamento_v406 selou={selou('fechamento_v406')}, cunhagens_v406 selou={selou('cunhagens_v406')}, kh_n1_cobertura_v406 selou={selou('kh_n1_cobertura_v406')}), os treze da v405 (ponte_da_massa_v405 selou={selou('ponte_da_massa_v405')}, identidade_v405 selou={selou('identidade_v405')}, gap_v405 selou={selou('gap_v405')}), os da v404, da v403, da v402, da v401 e da v399 seguem selados neste rito "
                   f"(caminho_v403 selou={selou('caminho_v403')}, falsidade_da_inercia_v401 selou={selou('falsidade_da_inercia_v401')}), como seguem o selo pela propria tecnologia e a declaracao do operador (v399), o sonico e a afinacao (v398) e o quadro (v397); sidecar um_absoluto_selo_acom.json {sc['veredito']} ({sc['n_objetos']} objetos, {sc['recusas']} recusas, sha16 {sc['sha16']}). "
                   f"O registro kh_n1_cobertura_v406 passa a cobrar piso (errata de contagem no registro kh_n1_cobertura_v407); a v406 e as pedras dela ficam como registro (seq {sq_v406}).",
                   "custodia conjunta pela sessao do site (o handoff lista o sidecar e traz a nota ao lado dos paragrafos anteriores).", refs=None))
    T9.append(errata(R_V396, sq_v396,
                     f"[E18 · ERRATA AO LADO, gerencia c1, em nome proprio, 03/11/2026, v407 {S}] Corrige o registro seq {sq_v396} desta rota (a v396 selada), que diz que nenhum lema liga psion C ao psionCorner e cuja chave linked_to_the_corner_by_a_lemma era o literal False; era verdade na data. Na v407 a chave e' LIDA do kernel do rito ({fk['testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma']}): {corpo('E18')}. Os registros corrigidos NAO foram apagados nem reescritos: a correcao vai ao lado.",
                     refs=[R_PSION, R_INV]))
    T9.append(errata(R_V406, sq_v406,
                     f"[E20 · ERRATA AO LADO, gerencia c1, em nome proprio, 03/11/2026, v407 {S}] Corrige o registro seq {sq_v406} desta rota (a v406 selada), que da' a chave linked_to_the_corner_by_a_lemma como False (nenhum lema liga o psion ao canto); era verdade na data. Na v407 a chave le {fk['testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma']} do kernel e a checagem c8 do fechamento_v406 e' versionada: {corpo('E20')}. Os registros corrigidos NAO foram apagados nem reescritos.",
                     refs=[R_PSION, R_INV]))
    for x in T9:
        assert x["rota_id"] in ids, "a rota %s nao existe no mapa" % x["rota_id"]
    resumo_conf = ("conferidor %s e %s" % (conf_dm, conf_np)) if "nao lido" not in (conf_dm, conf_np) else "conferidor: o resultado nao veio na leitura desta rodada"
    _vr407 = lambda v_: v_ if len(v_) <= 200 else v_[:197] + "..."   # o campo resultado do Mapa tem teto de 6000 caracteres (rotas._valida: resuma e aponte o artefato): a integra de cada veredito esta no core da rodada e nos ESPERADOS
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
            "titulo": "v407 SELADA %s: o psion, o canto e o par — %d modulos de kernel (PsionCanto, Par e as sete pedras de 02/11 de nome ratificado), o registro psion_canto_v407, cunhagens_v407 e kh_n1_cobertura_v407, %d inscricoes de 03/11 por sha256; escada %s -> %s; o lema das duas faces esta no kernel e a chave do lema e' lida dele (elo de estrutura, nao de vetores); o par na face de Fock segue em aberto; validade no kernel nao e' creditacao; o gate nao se move" % (
                S, DL_.N_BUNDLE, len(verb), esc0, esc1),
            "pergunta": "o candidato v407 selou com os 9 modulos de kernel, o registro com FUNCAO psion_canto_v407 (que le do kernel do proprio rito as 76 ancoras, os 9 modulos por sha256, a chave do lema lida e nao literal, as quatro respostas do operador de 03/11 pelos teoremas que ja existiam, o que fica False por teorema, a escada exata e o gate) e os dois por spec (as falas do operador de 03/11 por sha256, as decisoes D41 a D47, as erratas E18 a E20, a cobertura KH-N1), "
                        "com os registros da v406 (o fechamento_v406 herdado, com a checagem c8 versionada), os da v405, da v404, da v403, da v402, da v401 e da v399, o selo pela propria tecnologia e o quadro do topo seguindo selados, o sidecar reescrito, a letra do veredito do gate igual a da v406 e nenhum veredito fora da troca dita mudado?",
            "dados": ["os 9 modulos (PsionCanto e Par em pedra e insumos, as sete pedras de 02/11, e o bundle pinado em BUNDLE_v407.json), pinados por sha256 (so' lidos), e a medida da cobertura (KH_N1_v407.json)",
                      "as %d falas de 03/11 por sha256 em insumos\\cunhagens (todas falas do operador; a lista esta no registro cunhagens_v407 e na linhagem)" % len(verb),
                      "o kernel do rito (as ancoras, as bandeiras e a proveniencia), os recibos de compilacao das duas pedras de 03/11, o levantamento do acervo, o manifesto do pre-registro do teste (d) (so' citado), o proprio um.py, o core e o selo da rodada; nenhum dado novo foi aberto nesta rota"],
            "metodo": "lake build + Audit no sandbox k407c (9 modulos sobre o kernel da v406 selada); ensaio a seco do candidato; rito completo; conferidor (deve mudar / nao pode mudar, com o quadro do topo conferido de novo contra o resultado pinado nas duas linguas e no .md, e os itens do selo mais o round trip do um.py instalado); "
                      "leitura da rodada (inclui o sidecar e a linha final do rito); superficies com a regra da linhagem completa (o MEMORY.md nao e' compactado: recusa por contagem); elo B(n) da Bancada (passo simples v406 -> v407, sem salto; recibos); a guarda das frases em todo texto novo; o paragrafo novo e o do quadro, a nota ao lado dos paragrafos anteriores e o sidecar, no handoff",
            "resultado": " | ".join(_vr407(v_) for v_ in [pc["verdict"], cg["verdict"], kh["verdict"]]) + " | (vereditos resumidos a 200 caracteres; a integra esta no core da rodada, um_absoluto.json) | sidecar %s (%s objetos, %s recusas) | %s | %s | escada %s -> %s (teoremas limpos %s/%s; %d bandeiras novas, todas do psion_canto)" % (
                sc["veredito"], sc["n_objetos"], sc["recusas"], resumo_conf, ("%s vereditos fora da troca dita mudaram (exigido 0)" % nvm) if nvm != "nao lido" else "vereditos fora da troca dita: nao lidos nesta leitura", esc0, esc1, ESP["escada"][0], ESP["escada"][1], NF),
            "defeito": "as ressalvas, ditas: " + ress + "; o registro CONFERE o que o kernel prova e nao prova nada por si; o gate nao se moveu e a independencia das 4 bandeiras experimentais segue aberta (derivam de UM so' booleano) [DECLARADO, GV-01 e GV-03]; a pendencia [LEGAL] (D2) segue do operador; a revisao distinta do pacote e' o Sonnet (D47) e nao e' afirmada por este registro",
            "nao_refazer": "a integracao dos 9 modulos e a escada %s -> %s estao medidas; as 76 ancoras no kernel do rito estao lidas e conferidas contra o um.py instalado; repetir os registros so' com kernel ou um.py novo; a pergunta sobre o literal da chave do lema foi respondida (virou leitura do kernel, errata E18 ao lado)" % (esc0, esc1),
            "proximo_passo": "o teste (d), so' se tiver poder (opcao (c) do operador), por citacao do pre-registro; o motor continuo no pilar quantico (D45), quando o operador disser o conteudo observavel; o README pinado (D39) e o app e o contrato do JEV (D46), na custodia e na engenharia da casa; a ordem Kimi 5 sigma 02 (natureza.cinco_sigma_02_kimi_01nov); decisao [LEGAL] D2 com a agente de PI; custodia conjunta pela sessao do site (o handoff traz os paragrafos prontos do README e do site, a nota ao lado dos paragrafos anteriores e lista o sidecar); revisao independente do pacote (o Sonnet, D47)",
            "onde": PK, "artefatos": arts, "refs": sorted((set(x["rota_id"] for x in T9) | set(REFS) | set(preparo_no_livro(ids))) - {NOVA}),
            "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move; as erratas E18 a E20 e as decisoes D41 a D47 sao da gerencia c1, em nome proprio, ao lado (nada foi apagado nem reescrito); %s." % sim(c_seguem, "os registros anteriores seguem selados", "ALGUM REGISTRO ANTERIOR NAO SELOU")}
    for r in ROTA["refs"]:
        assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
    REG = [ROTA] + T9
    for x in REG:
        for k_, v_ in x.items():
            if isinstance(v_, str):
                assert len(v_) <= 6000, "o campo %s de %s passa de 6000 caracteres (limite do Mapa): resuma e aponte o artefato" % (k_, x["rota_id"])
    bad = [(x["rota_id"], violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad, "a guarda de texto (P18) achou violacao(oes): %r" % bad
    import guarda_frases_v407 as GF
    bad2 = [(x["rota_id"], GF.violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if GF.violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad2, "a guarda das frases achou violacao(oes): %r" % bad2
    atrib = [(x["rota_id"], T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))]
    assert not atrib, "a direcao do testemunho esta invertida ou a atribuicao falhou: %r" % atrib
    ruins = regra_4_44(REG, z, p)
    assert not ruins, "a regra do 4,44 (o p calibrado e a linha dos 5 sigma no mesmo campo) falhou em: %r" % ruins[:3]
    assert c_seguem and c_q, "algum registro anterior (quadro, v406, v405, v404, v403, falsidade, ponte, queda, esperanca, selo, declaracao, sonico, afinacao, rede de Fock, psibit, testemunha estatica) nao selou no core: o mapa nao registra a v407 assim"
    return REG


def gravar(p, b):
    """backup de BYTES se existir e mudar; temporario -> conferir tamanho -> substituir."""
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m407"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_m407"; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def main():
    V, PROB = L.ler()
    if PROB:
        print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); return 2
    NOS = L.NOS
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v407_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v407_*.json")), key=os.path.getmtime)
    arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto_selo_acom.json"), os.path.join(PK, "ESPERADOS_v407.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v407.json"),
            os.path.join(PK, "DIFF_KERNEL_v407.txt"), os.path.join(PK, "DIFF_v406_v407.diff"), os.path.join(NOS, "HANDOFF_v407_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v407.json"),
            os.path.join(PK, "kernel", "KERNEL_RECIBO_v407.json")] + sorted(glob.glob(os.path.join(PK, "pedra", "*.lean"))) + b3[-1:]
    arts = [x for x in arts if os.path.exists(x)]
    REG = montar(V, core, selo, ids_do_livro(), arts)
    J = os.path.join(HERE, "registro_mapa_v407.json")
    gravar(J, json.dumps(REG, ensure_ascii=False, indent=1).encode("utf-8"))
    quem = "claude-c1 (gerência), cadeia v407"
    print("registro MONTADO (NAO registrado): %d registro(s) (%s) -> %s" % (len(REG), ", ".join(x["tipo"] for x in REG), J))
    print("COMANDO (o passo 12 da cadeia o executa, uma vez so): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
    print("DEPOIS DO REGISTRO: os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
