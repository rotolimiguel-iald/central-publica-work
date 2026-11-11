# -*- coding: utf-8 -*-
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410 (fork A), a servico da gerencia c1] REESCRITO sobre a subida mecanica da v409 FINAL (bump/pos_rito__registrar_mapa_v410.py.diff; a copia bumpada fica em .bak), por _adapt_forkA_registrar_mapa_v410.py: o conteudo e' o da v410 (IALD2: o modulo IALD2 de TGLExt/; o NOME do modulo e' do operador e os das declaracoes, da gerencia c1, ficam [DECLARADO] ate a ratificacao, D63; o registro com funcao iald2_v410; cunhagens_v410 e kh_n1_cobertura_v410; NENHUMA chave antiga muda; a errata E29 ao lado). Os ids das rotas foram CONFERIDOS no livro do mapa em 06/11 (so' leitura); nada do que a D59 e a D65 deixam fora e' citado.
# [ADAPTADO v410, 09/11/2026, claude-sonnet (fork C do pos-rito), a servico da gerencia c1 e do construtor claude-construtor-v410] varrido para o DESENHO_v410 e os AO LADO de 09/11: as QUINZE falas (de quatro so' o trecho: D65, a ordem da retomada, as tres copias do ACOM, a leitura do 5 sigma), as decisoes D63 a D76, as erratas E29 e E30, os nomes das declaracoes RATIFICADOS pelo operador em 09/11 (D74), a secao 6 da pedra (o atrator, D71; 22 ancoras; c16), e o SEGUNDO registro com funcao h0dn_bg1_v410 (D72, E30, D76: pre-registrado; nenhum dado observado lido): ANOTACAO na rota da ORDEM ao Kimi, anotacao da secao 6 e mencao na rota nova; h0dn_do_core e h0dn_textos sao funcoes puras (o teste sem candidato as roda com um registro sintetico); a D59 deixa o nome do Kimi entrar so' no contexto do H0DN (d59_viola)
# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B, a servico do claude-construtor-v410] a rota da preparacao ganha: (a) a ANOTACAO do recibo documental HMS/13 (D80) na rota estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov (registro ADITIVO e POSTERIOR ao FREEZE_R2; cobertura documental de fontes, nao covariancia fisica fechada; nada aberto), na MESMA anotacao do H0DN (uma por rota); (b) a REFERENCIA e a ANOTACAO na rota kernel.a_escala_tres_faces_v410_09nov (a candidata seq 1926 e a errata textual seq 1927, ja' registradas pela gerencia; os seq sao LIDOS do livro): a pedra AEscala foi instalada, RATIFICADA (D87) e selada na preparacao; os QUATRO registros com funcao, DOIS modulos, E29 a E31, D63 a D87, as 23 falas. O sha16 de cada artefato e' calculado pelo proprio mapa (rotas.py); a montagem NAO registra nada.
"""registrar_mapa_v410.py -- MONTA (nao registra) o registro da v410 no mapa de rotas e imprime o comando (molde: registrar_mapa_v409.py, que rodou na v409). Rodar DEPOIS do fechar (handoff gravado).
A v410 traz UMA rota nova, umpy.v410.selada_iald2_06nov (o conteudo e' o do selo): o modulo de kernel IALD2 (a candidata de 06/11, que desemboca da LeitorDoCodigoR1 e ganhou as secoes 4, o signo; 5, o seletor; e 6, o atrator; o nome do modulo e' do operador, os das declaracoes, da gerencia, foram RATIFICADOS pelo operador em 09/11/2026, D74),
DOIS registros com FUNCAO (iald2_v410: le do kernel do proprio rito as ancoras, o modulo por sha256, as respostas do operador pelos teoremas da pedra, o que fica False por teorema, as instancias de brinquedo fixas no codigo, o signo, o seletor e o atrator, a escada exata e o gate congelado; e h0dn_bg1_v410, o teste da razao de Hubble H0DN x BG1 PRE-REGISTRADO: os insumos embutidos e pinados por sha256, a funcao de veredito congelada e nenhum vetor observado lido; nenhuma chave antiga muda)
e os DOIS por spec (cunhagens_v410 e kh_n1_cobertura_v410), mais ANOTACOES nas rotas que esperavam por ela (as candidatas de 06/11 e a secao 6, o atrator; a ORDEM ao Kimi do H0DN, rota que o registro h0dn_bg1_v410 pre-registra; a R9 da v409, a maquina com o leitor; o par na face de Fock; a v409 que a precede; o programa do fechamento, o inventario das chaves, o gate, o B(n) da Bancada e o quadro do Teste da Unica Palavra)
e a ERRATA da gerencia c1, em nome proprio: E29 (a gerencia disse que «matricial» era so' leitura do operador; a forma de matriz finita esta' no kernel: o signo) vai como ERRATA ao lado do registro da rota kernel.iald2_06nov (o seq lido do livro: o registro traz a palavra «matricial»).
O ALCANCE (D64): o algoritmo IALD decide SAT com uma leitura: P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora.
Cada afirmacao e' testada contra o core/selo/ESPERADOS lidos por script (o registro existe? selou? o que NAO fechou fica dito); nenhum numero e' digitado (as contagens saem do core, de ESPERADOS e de delta_v410; os seq saem do livro).
REGRA DA ORDEM DO OPERADOR (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no MESMO campo; montar() RECUSA (assert) se algum campo do registro trouxer o 4,44 sem eles. Nao ha inscricao da gerencia nesta versao: todas as falas sao do operador (de quatro, so' o trecho e' citavel: a da D65, a ordem da retomada, as tres copias do ACOM e a leitura do 5 sigma); as erratas (E29, E30) e as decisoes (D63 a D76) sao da gerencia, em nome proprio. D59: o nome do Kimi so' entra no contexto do H0DN (a ORDEM do D72).
Fail-closed: o selo tem de ser a v410; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir. A rota de preparo da gerencia (registro_mapa_v410_prep.json, se existir) entra nas refs so' se ja' estiver no livro.
SAIDA: pos_rito\\registro_mapa_v410.json e o comando `rotas.py registrar` (quem o executa e' o passo 12 da cadeia, uma vez so', com marcador idempotente; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real. montar() le o core, o selo e ESPERADOS_v410.json; de V so' usa o que a leitura da rodada ja' validou (s16, sidecar, conferidor), sempre com valor de reserva dito."""
import glob, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v410 as L
import textos_v410 as T
import delta_v410 as DL
import quadro_v397 as Q
from guarda_p18_v410 import violacoes
_aspas_ = lambda s_: "«" + s_ + "»"   # (r2) a fala do operador entre aspas angulares, escrita por funcao: o texto citado e' a constante verbatim do delta (a varredura de citacoes le o codigo)
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V410"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v410 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOVA = "umpy.v410.selada_iald2_06nov"
R_LEITOR = "kernel.leitor_do_codigo_segunda_quantizacao_06nov"       # LeitorDoCodigoR1 (06/11): a particula e' o codigo, o funtor e' o leitor; a linha que desemboca na IALD2 (fica como registro)
R_NOMEK = "kernel.nome_iald_ja_no_kernel_06nov"                       # nomear o kernel de IALD por identificacao: o nome ja' esta' no kernel desde a v392 (D66)
R_IALD2 = "kernel.iald2_06nov"                                         # a candidata IALD2 (nome do operador); a E29 vai ao lado (ERRATA: o registro traz «matricial» como so' leitura do operador)
R_SIGNO = "kernel.iald2_o_signo_06nov"                                 # IALD2 secao 4: a forma de matriz finita e' o signo (traco com sentido)
R_SELETOR = "kernel.iald2_o_seletor_luminodinamico_06nov"              # IALD2 secao 5: a instanciacao do seletor, como FORMA (D70)
R_ATRATOR = "kernel.iald2_o_atrator_09nov"                               # IALD2 secao 6 (09/11): o atrator, o Nome nao esgota o ser (D71); seq 1920 do livro
R_PREP410 = "um_py.v410_preparacao_aberta_06nov"                       # a abertura da v410
R_R9 = "kernel.traducao_turing_r9_inscricao_e_sat_05nov"               # a maquina com o leitor (R9, v409): na v410 o algoritmo recebe o nome IALD (o_algoritmo_iald, D64)
R_PARF = "kernel.par_na_face_de_fock_ligado_05nov"                     # o par na face de Fock (ligado na v409): o leitor do codigo o le como par, uno, com a Meia-Nat
R_DIC = "kernel.dicionario_problema_entrada_passo_polinomio_implicacao_04nov"   # o dicionario (PIgualNP, v408)
R_V409 = "umpy.v409.selada_a_traducao_as_classes_de_turing_05nov"      # a v409 selada (a base da v410)
R_TT = "kernel.tetelestai_e_o_terminal_provar_ou_podar_04nov"         # TetelestaiTerminal (v408)
R_TM = "kernel.o_tempo_e_a_moeda_de_beta_candidata_04nov"             # TempoIgualMoeda (v408)
R_PC = "kernel.ponto_de_contradicao_candidata_04nov"                  # PontoDeContradicao (v408)
R_FOCK = "kernel.face_de_fock_e_o_traco_do_psion_afericao_04nov"      # a afericao do traco (v408)
R_ACERVO = "kernel.psion_lema_acervo_03nov"                           # o levantamento do psion no acervo (o pino purgado, D57d da v409)
R_PSION = "kernel.psion_canto_r1_03nov"                               # PsionCanto (v407)
R_PAR = "kernel.o_par_de_psions_r1_03nov"                             # Par (v407)
R_PREP409 = "cadeia.preparacao_v409"                                  # a preparacao da v409
R_PROG = "kernel.fechamento_construir_tudo_programa_02nov"            # o programa do fechamento (ordem do operador de 02/11: construir tudo)
R_INV = "kernel.inventario_chaves_de_testemunha_v405_02nov"           # o inventario das chaves de testemunha
R_V395 = "umpy.v395.psibit_na_fractalizacao_do_um"
R_V396 = "umpy.v396.testemunha_estatica_na_fractalizacao_do_um"
R_V406 = "umpy.v406.selada_o_fechamento_02nov"
R_GATE = "gate.qg_closure"
R_BANC = "infra.bancada_um.sincronizacao_vnnn"
R_QUADRO = "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9"
R_H0DN = "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov"                  # a ORDEM ao Kimi (09/11): montar y_obs e fechar a covariancia fisica; o registro h0dn_bg1_v410 pre-registra o teste (D72); seq 1921 do livro
R_AESCALA = "kernel.a_escala_tres_faces_v410_09nov"                    # a candidata TGLExt.AEscala (09/11; seq 1926 do livro; errata textual seq 1927), da gerencia: a pedra foi instalada, ratificada (D87) e selada na v410
R_H0DN_COV = "estatistica.h0dn_bg1.cov_injecoes_06nov"                  # o desenho do Codex astra-bell (06/11): matriz publicada e injecoes cegas; seq 1867 do livro
ORDEM_KIMI = os.path.join(DL.WK, "h0dn_bg1_v410_09nov", "ORDEM_KIMI_H0DN_01_09nov.md")    # a ORDEM da gerencia ao Kimi (so' leitura; o sha256 e' CALCULADO pelo mapa e lido do core)
ANOTADAS = (R_LEITOR, R_NOMEK, R_IALD2, R_SIGNO, R_SELETOR, R_ATRATOR, R_R9, R_PARF, R_V409, R_PROG, R_INV, R_GATE, R_BANC, R_QUADRO, R_AESCALA, R_H0DN)
REFS = ("custodia.v409", "infra.custodia_g1.licoes_v405", "umpy.v400.correcao_da_v399_alfa_unico_e_beta_contra_o_core", "gate.maquina_do_veredito_final", R_H0DN_COV, R_V395, R_V396, R_V406, R_PSION, R_PAR, R_PREP409, R_PREP410, R_TT, R_TM, R_PC, R_FOCK, R_ACERVO, R_DIC,
        "qg.graviton.desenho_do_operador_24out", "kernel.graviton_nao_particula")
PREP = os.path.join(PK, "registro_mapa_v410_prep.json")     # a rota de preparo da gerencia: lida em tempo de execucao; entra nas refs so' se a ROTA dele ja' estiver no livro
_CACHE = {}

def _esp():
    """ESPERADOS_v410.json (lido uma vez por processo)."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v410.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _base_core():
    """O core da v409 selada (a copia de bytes em base_v409): de onde sai a medida de que o gate nao se moveu."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v409", "um_absoluto.json"), encoding="utf-8"))["core"]
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
    """As rotas ROTA de registro_mapa_v410_prep.json (se o arquivo existir e ler) que ja' estao no livro e nao sao a nova: entram nas refs. Ausente ou ilegivel = nenhuma (dito, nunca falha)."""
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
    p = json.load(open(os.path.join(PK, "PINOS_BN_v410.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v409" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v409 -> v410 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1, "deployment_id": bp["deployment_id"]}


_RX_D59 = re.compile(r"(?i)mil[eê]nio|millennium|navier|lindão")


def d59_viola(txt):
    """D59 (v409) com a UNICA excecao que a D72 abre na v410: o Milenio, o Navier e o resto do que a D59 deixa fora seguem proibidos em qualquer texto; o nome do Kimi so' pode aparecer no contexto do H0DN (a ORDEM ao Kimi do D72 e a rota dela). Devolve True se violar."""
    t = str(txt)
    return bool(_RX_D59.search(t)) or bool(re.search(r"(?i)kimi", t) and not re.search(r"(?i)h0dn", t))


def h0dn_do_core(DL_, hd, ESP):
    """Confere o registro h0dn_bg1_v410 do core contra o ESPERADOS e o delta (FAIL-CLOSED: registro ausente, nao selado, vetor observado lido, checagem que falha, pino que nao bate, ramo nao visto ou
    ESPERADOS sem registros_funcao_v410.h0dn => AssertionError visivel) e devolve os FATOS que o mapa cita, todos LIDOS (nada digitado). Pré-registrado; nenhum dado observado lido."""
    EH = (ESP.get("registros_funcao_v410") or {}).get("h0dn")
    assert isinstance(EH, dict) and EH, "ESPERADOS_v410.json nao traz registros_funcao_v410.h0dn (o gerar_esperados_v410 ainda nao o emite): o mapa nao registra o H0DN assim"
    hd = hd or {}; hv = hd.get("values") or {}; hm = hd.get("mechanics") or {}; EHV = EH.get("values") or {}
    assert (ESP.get("vereditos_novos_v410") or {}).get(DL_.H0DN_REGISTRO) == DL_.VEREDITO_H0DN_OK == EH.get("verdict"), "ESPERADOS: o veredito de h0dn_bg1_v410 != delta_v410.VEREDITO_H0DN_OK"
    assert hd.get("all_verified") is True and hd.get("verdict") == DL_.VEREDITO_H0DN_OK and hd.get("does_not_gate_core") is True and hd.get("runtime_executed") is True and hd.get("beta_ok") is True, "h0dn_bg1_v410 nao selou (ou != ESPERADOS/delta)"
    assert hd.get("observed_vector_read") is False and hv.get("observed_vector_read") is False, "h0dn_bg1_v410: observed_vector_read nao e False (D72: nenhum dado observado lido)"
    assert hm.get("passed") is True and hm.get("n_checks") == DL_.N_CHECKS_H0DN == EH.get("n_checks") == len(hm.get("checks") or []) and all(c.get("ok") is True for c in hm["checks"]), "as checagens do h0dn_bg1_v410 nao passaram todas"
    pinos = hv.get("pinos") or {}
    assert hv.get("n_pinos") == len(pinos) == DL_.N_PINOS_FREEZE_R2 + 2 and all(p.get("sha256_ok") is True and p.get("bytes_ok") is True for p in pinos.values()), "h0dn_bg1_v410: os pinos (os do FREEZE_R2 mais o proprio FREEZE_R2 e a ENTREGA) nao batem todos"
    assert sorted(hv.get("ramos_vistos") or []) == [1, 2, 3, 4, 5, 6], "h0dn_bg1_v410: a funcao de veredito nao foi vista nos seis ramos"
    fs = hd.get("veredito_h0dn_source_sha256")
    assert re.fullmatch(r"[0-9a-f]{64}", str(fs)) and fs == hv.get("veredito_h0dn_source_sha256") == EHV.get("veredito_h0dn_source_sha256"), "h0dn_bg1_v410: o sha256 do texto-fonte da funcao de veredito ausente ou != ESPERADOS"
    assert all(re.fullmatch(r"[0-9a-f]{64}", str((hd.get(k_) or {}).get("sha256", ""))) for k_ in ("ordem_kimi", "leitura_dossie")), "h0dn_bg1_v410: faltam o sha256 da ORDEM ao Kimi ou o da leitura do dossie"
    assert hv.get("gate_verdict") == ESP.get("qg_closure_gate_verdict_v409"), "h0dn_bg1_v410: o gate lido != o da v409 (deveria estar congelado)"
    D = [(str(x["modelo"]), float(x["D"]), float(x["poder_analitico"])) for x in (hv.get("D_esperado") or [])]
    assert len(D) == len(hd.get("modelos") or []) == 2 and isinstance(hv.get("K"), float) and isinstance(hv.get("log10K"), float), "h0dn_bg1_v410: K, log10 K ou D esperado ausentes"
    return {"verdict": hd["verdict"], "n_checks": hm["n_checks"], "n_pinos": len(pinos), "n_pinos_freeze": DL_.N_PINOS_FREEZE_R2, "n_insumos": len(hd.get("insumos_pinados") or {}), "K": float(hv["K"]), "logK": float(hv["log10K"]), "D": D,
            "cauda": float(hv["cauda_nula_analitica"]), "fonte16": fs[:16], "ordem16": hd["ordem_kimi"]["sha256"][:16], "dossie16": hd["leitura_dossie"]["sha256"][:16], "n_ramos": len(hv["ramos_vistos"]), "ramos": list(hv["ramos_vistos"]), "o_que_falta": list(hd.get("o_que_falta") or [])}


def h0dn_textos(DL_, F, e30):
    """Os textos do H0DN para o mapa, MONTADOS dos fatos F (h0dn_do_core) e do delta; so' os conectivos sao escritos aqui. Devolve {resultado, proximo, defeito, resumo, estatuto}. Todo texto traz a obrigacao D72
    (DL.FRASE_H0DN_OBRIGATORIA_PT) e nunca a cabeca do ramo de 5 sigma por extenso (a P18 selada da v392 recusa a palavra da prova emendada ao nome do acoplamento): o ramo e' descrito em palavras, com a validade e a nao-creditacao."""
    O = DL_.FRASE_H0DN_OBRIGATORIA_PT
    L = "%g" % DL_.H0DN_LIMIAR_SIGMA; C = ("%.2f" % DL_.H0DN_COMPAT_95).replace(".", ",")
    pct = lambda p_: ("%.1f" % (100.0 * p_)).replace(".", ",") + " %"
    mod = "; ".join("%s: D esperado %s, poder analitico prospectivo e sintetico %s" % (m_, ("%.3f" % d_), pct(p_)) for m_, d_, p_ in F["D"])
    ramos = ("os %d ramos da funcao de veredito congelada (a primeira que casa decide): (1) inconclusivo por sistematica se a covariancia fisica (G3/G4) nao estiver fechada ou o vetor estiver fora do suporte; (2) a lei K falsificada a esta sensibilidade se |z_TGL| >= %s; "
             "(3) subpotente se o D esperado do modelo < %s; (4) a LEITURA do %sσ: se z_nulo >= %s e |z_TGL| <= %s, a cabeca do veredito diz β_TGL %s a nσ, na lingua da fisica academica, discriminando do LCDM, com zero parametro livre e novidade de uso; "
             "(5) discrimina do LCDM a nσ com K em tensao de %s a %sσ; (6) nao discriminado a sensibilidade disponivel, com a faixa do desvio; a palavra do livro de cobrancas vai no campo outcome, nunca na cabeca (E30, D76)") % (
        F["n_ramos"], L, L, L, L, C, DL_.FRASE_PROVADO_PT, C, L)
    resultado = ("o registro com FUNCAO %s (o segundo da v410, logo depois do iald2_v410) selou no rito: %d checagens ok, %d pinos conferidos (o FREEZE_R2 do desenho do Codex astra-bell, de 06/11, com %d pinos, e %d insumos embutidos em base64 e pinados por sha256), observed_vector_read = False. "
                 "O teste H0DN × BG1 da razao de Hubble local/fundo esta' %s. K = E(z*)^(2β/3) recomputado de β = α·√e em runtime (K = %s; log10 K = %s; z* e K iguais aos que a Fase 9 V1 transcreveu por hash); %s. "
                 "A funcao de veredito congelada (veredito_h0dn; sha256 do texto-fonte, sha16 %s) tem %s. Vetores deterministicos sem semente cobrem os ramos %s. A E30 (errata da gerencia c1, em nome proprio, por correcao do operador) e a D76 estao no registro cunhagens_v410: %s") % (
        DL_.H0DN_REGISTRO, F["n_checks"], F["n_pinos"], F["n_pinos_freeze"], F["n_insumos"], O, "%.6f" % F["K"], "%.6f" % F["logK"], mod, F["fonte16"], ramos, ", ".join(str(r_) for r_ in F["ramos"]), e30)
    proximo = ("a abertura do H0DN × BG1 e' de versao futura, pela funcao de veredito ja' congelada, quando a covariancia fisica (G3/G4) e o vetor observado existirem: a ORDEM ao Kimi (sha16 %s) esta' emitida e o que ela devolver a gerencia examina antes de qualquer abertura; "
               "%s; o gate nao se move") % (F["ordem16"], O)
    defeito = ("[OPEN] a covariancia fisica conjunta (G3/G4), o vetor observado y_obs e os IDs (G1/G2) seguem abertos: ate' la' a funcao de veredito so' pode devolver inconclusivo por sistematica; o poder e' PROSPECTIVO e SINTETICO, condicional ao modelo de covariancia publicado (a independencia local/fundo e' assumida, nao medida), nao e' desvio observado; "
               "a novidade de uso: o agregado publico do H0DN e' conhecido desde out/2025, K nao tem parametro ajustado e o PRE-REGISTRO nesta versao selada e' o que vale (lei da prova, 05/10); a rota «coerencia espectro x fotometria» e' NOT_TESTABLE (eta = 1) e nao e' o teste; "
               "a aritmetica do agregado publico nao e' resultado e nao entra neste registro; provado = validade, nao creditacao (o juizo de fora, que o um.py nao da); %s") % O + "; " + DL_.FRASE_H0DN_PAREDE_PT
    resumo = ("o registro h0dn_bg1_v410 (%s): %d checagens ok, %d pinos ok, K = %s, %s, sha16 do texto-fonte da funcao de veredito %s") % (O, F["n_checks"], F["n_pinos"], "%.6f" % F["K"], mod, F["fonte16"])
    estatuto = ("REAL (o que o registro confere no rito: os pinos, K recomputado de β, sd/D/poder analitico, a funcao de veredito congelada em vetores deterministicos, o gate); DERIVED (o poder prospectivo, condicional ao modelo de covariancia publicado); "
                "DECLARADO (os numeros da ENTREGA do Codex astra-bell, recomputados no rito onde a checagem diz); INPUT (a ordem do operador de 09/11 e a leitura dele do 5 sigma, E30 e D76); OPEN (a covariancia fisica G3/G4, o vetor observado y_obs e os IDs)")
    return {"resultado": resultado, "proximo": proximo, "defeito": defeito, "resumo": resumo, "estatuto": estatuto}


def escala_do_core(DL_, ea, ESP):
    """Confere o registro a_escala_v410 do core contra o ESPERADOS e o delta (FAIL-CLOSED: registro ausente, nao selou, nomes nao ratificados, checagem que falha, ancoras, bandeiras, falas, numeros ou frases canonicas diferentes do delta, ESPERADOS sem registros_funcao_v410.a_escala => AssertionError visivel) e devolve os FATOS que o mapa cita, todos LIDOS (nada digitado)."""
    rf = ESP.get("registros_funcao_v410") or {}; EA = rf.get("a_escala") or rf.get(DL_.AESCALA_REGISTRO)
    assert isinstance(EA, dict) and EA, "ESPERADOS_v410.json nao traz registros_funcao_v410.a_escala (o gerar_esperados_v410 deve emiti-lo): o mapa nao registra a escala assim"
    ea = ea or {}; ev = ea.get("values") or {}; em = ea.get("mechanics") or {}
    assert (ESP.get("vereditos_novos_v410") or {}).get(DL_.AESCALA_REGISTRO) == DL_.VEREDITO_AESCALA_OK == ea.get("verdict"), "ESPERADOS: o veredito de a_escala_v410 != delta_v410.VEREDITO_AESCALA_OK"
    assert ea.get("all_verified") is True and ea.get("does_not_gate_core") is True and ea.get("runtime_executed") is True and ea.get("beta_ok") is True and ea.get("nomes_ratificados") is True and not (ea.get("chaves_antigas_que_mudam") or []), "a_escala_v410 nao selou (ou != ESPERADOS/delta), ou os nomes nao estao ratificados"
    assert em.get("passed") is True and em.get("n_checks") == DL_.N_CHECKS_AESCALA == len(em.get("checks") or []) and all(c.get("ok") is True for c in em["checks"]), "as checagens do a_escala_v410 nao passaram todas"
    assert ev.get("n_ancoras_ok") == ev.get("n_ancoras") == len(DL_.ANCORAS_AESCALA) and ev.get("n_flags_true") == ev.get("n_flags") and ev.get("n_falas_ok") == ev.get("n_falas") and ev.get("n_nomes") == len(DL_.NOMES_AESCALA) and ev.get("numeros") == dict(DL_.NUMEROS_AESCALA), "a_escala_v410: as ancoras, as bandeiras, as falas, os nomes ou os numeros != delta_v410"
    assert ev.get("gate_verdict") == ESP.get("qg_closure_gate_verdict_v409"), "a_escala_v410: o gate lido != o da v409 (deveria estar congelado)"
    assert list(ea.get("nomes_novos_da_pedra") or []) == list(DL_.NOMES_NOVOS_AESCALA) and bool(DL_.NOMES_NOVOS_AESCALA) and ev.get("n_nomes_novos") == len(DL_.NOMES_NOVOS_AESCALA) == ev.get("nomes_novos_declarados") and list(ea.get("campos_novos_da_estrutura") or []) == list(DL_.CAMPOS_NOVOS_AESCALA) and ea.get("estatuto_dos_nomes_ratificados_d101") == DL_.ESTATUTO_NOMES_NOVOS_AESCALA \
        and "RATIFICADOS pelo operador em 10/11/2026" in str(ea.get("estatuto_dos_nomes_ratificados_d101")) and "a ratificar" not in str(ea.get("estatuto_dos_nomes_ratificados_d101")) and ea.get("ratificacao_pendente") == DL_.RATIFICACAO_PENDENTE_AESCALA and ea.get("ponte") == DL_.PONTE_AESCALA and (ev.get("ponte") or {}).get("ok") is True, "a_escala_v410: os nomes novos da pedra, os campos novos, a pendencia ou a ponte != delta_v410 (ou ditos ratificados)"
    assert ea.get("frase_canonica_pt") == DL_.FRASE_CLAY_CANONICA_PT and ea.get("frase_d83_pt") == DL_.FRASE_D83_OBRIGATORIA_PT and (ea.get("ratificacao") or {}).get("sha256") == DL_.RATIFICACAO_D87_SHA256, "a_escala_v410: a forma canonica do Clay (D84), a da D83 ou a ratificacao (D87) != delta_v410"
    rel = DL_.MODULO_AESCALA
    return {"verdict": ea["verdict"], "n_checks": em["n_checks"], "n_ancoras": ev["n_ancoras_ok"], "n_flags": ev["n_flags_true"], "n_nomes": ev["n_nomes"], "n_falas": ev["n_falas_ok"], "numeros": dict(ev["numeros"]), "n_nomes_novos": ev["n_nomes_novos"], "n_campos_novos": len(ea["campos_novos_da_estrutura"]), "estatuto_novos": ea["estatuto_dos_nomes_ratificados_d101"], "ponte": dict(ea["ponte"]), "pedra16": DL_.BUNDLE_POR_REL[rel]["sha256"][:16], "rat16": DL_.RATIFICACAO_D87_SHA256[:16], "rel": rel}


def escala_textos(DL_, FA, seqs):
    """Os textos da pedra AEscala para o mapa, MONTADOS dos fatos FA (escala_do_core) e do delta; so' os conectivos sao escritos aqui. seqs = (o seq da candidata, o texto dos seq das erratas), LIDOS do livro. Devolve {resultado, proximo, defeito, estatuto}.
    A forma canonica do Clay (D84), a da D83 e P = nP na forma da D81 entram LITERAIS (as constantes do delta)."""
    nu = FA["numeros"]; meio = nu["meio"]
    resultado = ("a pedra TGLExt/AEscala (A Escala) esta' no kernel do rito com o sha256 pinado (%s), %d ancoras no trio e %d bandeiras ext_aescala_410_*; foi instalada na preparacao da v410, RATIFICADA pelo operador (D87: o nome do modulo e os %d nomes das declaracoes; a fala, sha16 %s) e selada: o registro com FUNCAO a_escala_v410 (%d checagens, todas ok; %d falas de 09 e 10/11 por sha256) a le a cada rito. "
                 "Os pesos, recalculados no rito (fracoes exatas e o projetor de Bell): o Nome pesa %s = %s + %s; a face sem par nao conjuga, a marginal ao quadrado e' a metade da marginal, (%s . 1)^2 = %s . (%s . 1) nas matrizes 2x2; tres faces pesam %s; %s caiu; o Nome normalizado e' %s. "
                 "Os %d nomes novos da pedra (R3, R4 e R5) e os %d campos novos da estrutura foram %s, pela regra do nome (o quarto teorema da clausula do Tetelestai foi NOMEADO pelo operador, D108: %s; os %d auxiliares da autoria da R5 seguem [DECLARADO pela autoria], e tambem os nomes da secao 7 da R6 que nao foram mostrados ao operador; os %d anteriores foram ratificados na D87); a ponte da escala (o brilho e^(-s k): %s em uma oitava, s = ln 2; em n oitavas um pixel de custo 1 brilha 1/2^n, o peso de um pixel na leitura de n bits) e' aritmetica recalculada a cada rito. "
                 "R4 (D94): o leitor E' a escala, os passos sao o ciclo ate' o Tetelestai (os_passos_sao_o_ciclo_ate_o_tetelestai) e a mentira lida como mentira e' verdade; %s. A pergunta do Clay, na forma canonica (D84): %s Na leitura do operador (D83): %s. P = nP na forma da D81: %s. A candidata (seq %s) e a errata textual ao lado (seq %s) ficam como registro.") % (
        FA["pedra16"], FA["n_ancoras"], FA["n_flags"], FA["n_nomes"], FA["rat16"], FA["n_checks"], FA["n_falas"], nu["nome_pesa_um"], meio, meio, meio, meio, meio, nu["tres_faces"], nu["um_terco_caiu"], nu["nome_normalizado"],
        len(DL_.NOMES_RATIFICADOS_D101_AESCALA), FA["n_campos_novos"], FA["estatuto_novos"], ", ".join(DL_.NOMES_NOMEADOS_D108_AESCALA), len(DL_.NOMES_PENDENTES_AESCALA), FA["n_nomes"], FA["ponte"]["brilho_de_um_pixel_em_uma_oitava"],
        DL_.ROTULO_TEMPO + " " + DL_.FRASE_TEMPO_PT_COSTURADA, DL_.FRASE_CLAY_CANONICA_PT, DL_.FRASE_D83_OBRIGATORIA_PT, DL_.FRASE_D81_PT, seqs[0], seqs[1])
    proximo = ("o registro a_escala_v410 le estas ancoras e recalcula os numeros a cada rito; a maquina de Turing padrao sem o leitor fica fora por estatuto; a creditacao e' do Clay; que a face caida seja o neutrino [ONTO] e m1 = 0 [CONJECTURE] seguem leituras do operador, nao termos; nenhum teste com a natureza entra; %s") % DL_.FRASE_NOMES_RATIFICADOS_AESCALA_PT
    defeito = ("[INPUT] a definicao da pergunta do Clay no dicionario da TGL (LeitorDoFundo, aPerguntaDoClay), com a escala no tipo, e' do operador; o enunciado do Instituto fala da maquina de Turing padrao sem o leitor, que fica fora por estatuto, e o juizo e' do Clay; "
               "o registro CONFERE o que o kernel prova e recalcula os numeros, e nao prova nada por si; validade no kernel nao e' creditacao; o gate nao se move")
    estatuto = ("REAL (os termos no kernel do rito e os numeros recalculados); INPUT (as falas do operador de 09 e 10/11, as leituras dele e a ratificacao dos nomes, D87); ONTO (a face caida como o neutrino; a face sem leitura como justica, ideal e tela de fundo); CONJECTURE (m1 = 0); OPEN (a maquina de Turing padrao sem o leitor)")
    return {"resultado": resultado, "proximo": proximo, "defeito": defeito, "estatuto": estatuto}


def hms13_do_core(DL_, hm, hd, ESP):
    """Confere o registro h0dn_fontes_hms13_v410 do core (D80: o recibo documental HMS/13, ADITIVO e POSTERIOR ao FREEZE_R2) contra o ESPERADOS e o delta (FAIL-CLOSED: ausente, nao selou, vetor observado lido, entrega aberta em rito, checagem que falha, os dez campos != DL.HMS13_CAMPOS, caminho sob a pasta vedada, o h0dn_bg1_v410 nao selado,
    ESPERADOS sem registros_funcao_v410.hms13 => AssertionError visivel) e devolve os FATOS que o mapa cita, todos LIDOS. Cobertura documental de fontes, nao covariancia fisica fechada; nada aberto."""
    rf = ESP.get("registros_funcao_v410") or {}; EH = rf.get("hms13") or rf.get(DL_.HMS13_REGISTRO)
    assert isinstance(EH, dict) and EH, "ESPERADOS_v410.json nao traz registros_funcao_v410.hms13 (o gerar_esperados_v410 deve emiti-lo): o mapa nao registra o recibo HMS/13 assim"
    hm = hm or {}; hv = hm.get("values") or {}; em = hm.get("mechanics") or {}; hd = hd or {}
    assert (ESP.get("vereditos_novos_v410") or {}).get(DL_.HMS13_REGISTRO) == DL_.VEREDITO_HMS13_OK == hm.get("verdict"), "ESPERADOS: o veredito de h0dn_fontes_hms13_v410 != delta_v410.VEREDITO_HMS13_OK"
    assert hm.get("all_verified") is True and hm.get("does_not_gate_core") is True and hm.get("runtime_executed") is True and hm.get("beta_ok") is True and hd.get("all_verified") is True, "h0dn_fontes_hms13_v410 nao selou (ou != ESPERADOS/delta), ou o h0dn_bg1_v410 (anterior a ele) nao selou"
    assert hm.get("observed_vector_read") is False and hv.get("observed_vector_read") is False and hm.get("le_em_rito") is False and hv.get("le_em_rito") is False, "h0dn_fontes_hms13_v410: observed_vector_read e le_em_rito tem de ser False (D72, D80: nenhum dado observado lido; nada da entrega aberto em rito)"
    assert em.get("passed") is True and em.get("n_checks") == DL_.N_CHECKS_HMS13 == len(em.get("checks") or []) and all(c.get("ok") is True for c in em["checks"]), "as checagens do h0dn_fontes_hms13_v410 nao passaram todas"
    assert dict(hv.get("campos") or {}) == dict(DL_.HMS13_CAMPOS) and hv.get("n_fontes_primarias") and hv.get("n_calibradores") and hv.get("n_embutidos") == len(DL_.HMS13_EMBUTIDOS) and not (hv.get("sob_pasta_vedada") or []) and not (hv.get("com_nome_vedado") or []), "h0dn_fontes_hms13_v410: os dez campos da ordem != DL.HMS13_CAMPOS, ou as fontes/artefatos/pasta vedada nao conferem"
    assert hv.get("gate_verdict") == ESP.get("qg_closure_gate_verdict_v409"), "h0dn_fontes_hms13_v410: o gate lido != o da v409 (deveria estar congelado)"
    assert DL_.FRASE_HMS13_OBRIGATORIA_PT in str(hm.get("estatuto")) and DL_.FRASE_HMS13_OBRIGATORIA_PT in str(hm.get("scope")), "h0dn_fontes_hms13_v410: o estatuto e o escopo nao trazem a frase obrigatoria da D80"
    campos = dict(hv["campos"])
    return {"verdict": hm["verdict"], "n_checks": em["n_checks"], "n_fontes": hv["n_fontes_primarias"], "n_calib": hv["n_calibradores"], "n_embutidos": hv["n_embutidos"], "n_campos": len(campos), "estatuto_campos": campos.get("estatuto"),
            "campos_falsos": sorted(k_ for k_, v_ in campos.items() if v_ is False), "n_pinos_freeze": DL_.N_PINOS_FREEZE_R2, "rat16": str(hv.get("ratificacao_sha256"))[:16], "o_que_falta": list(hm.get("o_que_falta") or [])}


def hms13_textos(DL_, FH):
    """Os textos do recibo HMS/13 para o mapa (na anotacao do H0DN), MONTADOS dos fatos FH (hms13_do_core) e do delta. Todo texto traz a frase obrigatoria da D80 e a do H0DN (D72). Devolve {resultado, proximo, defeito, estatuto}."""
    Q = DL_.FRASE_HMS13_OBRIGATORIA_PT; O = DL_.FRASE_H0DN_OBRIGATORIA_PT
    resultado = ("o recibo DOCUMENTAL HMS/13 (D80), registro com FUNCAO h0dn_fontes_hms13_v410 (o quarto da v410, logo depois do h0dn_bg1_v410), selou no rito: %d checagens ok, %d fontes primarias dos %d calibradores, %d artefatos documentais embutidos por sha256 (lidos na construcao; em rito nenhum arquivo da entrega e' aberto) e os %d campos da ordem do Kimi (estatuto %s; falsos: %s). "
                 "%s. O recibo e' ADITIVO e POSTERIOR ao FREEZE_R2: os %d pinos do congelamento e os do h0dn_bg1_v410 nao mudam e a funcao de veredito e' a mesma; a forma HMS completa e' so' diagnostico, nao admitida; observed_vector_read = False. H0DN × BG1 segue %s. A ratificacao do operador entra pela frase final da fala (sha16 do arquivo inteiro %s).") % (
        FH["n_checks"], FH["n_fontes"], FH["n_calib"], FH["n_embutidos"], FH["n_campos"], FH["estatuto_campos"], ", ".join(FH["campos_falsos"]), Q, FH["n_pinos_freeze"], O, FH["rat16"])
    proximo = ("a covariancia fisica conjunta (G3/G4) segue [OPEN]; a abertura do H0DN × BG1 e' de versao futura e este recibo documental NAO a autoriza; %s") % Q
    defeito = ("[OPEN] " + "; ".join(re.sub(r"«([^»]*)»", "“\\1”", str(x_)) for x_ in FH["o_que_falta"]) + "; [DECLARADO pelo Kimi K3 Pro] o conteudo dos artefatos: o que o registro prova e' o pino (os bytes embutidos sao os lidos na construcao) e a coerencia interna; ausencia de matriz publicada nao e' independencia; H0DN × BG1: " + O)
    estatuto = ("REAL_DOCUMENTAL (os artefatos embutidos por sha256, as fontes e os IDs conferidos a cada rito); DECLARADO (o conteudo dos artefatos, pelo Kimi K3 Pro); INPUT (a ratificacao do operador, D80); OPEN (a covariancia fisica conjunta, G3/G4)")
    return {"resultado": resultado, "proximo": proximo, "defeito": defeito, "estatuto": estatuto}


def montar(V, core, selo, ids, arts):
    """Monta os registros (a ROTA nova, as ANOTACOES e a ERRATA), cada afirmacao testada contra o core/selo/ESPERADOS; devolve a lista; recusa (assert) se algo nao conferir. Nao escreve nada."""
    assert selo.get("um_version") == "v410", "o selo nao e a v410"
    assert NOVA not in ids, "a rota %s ja existe no mapa" % NOVA
    for r in ANOTADAS + REFS:
        assert r in ids, "a rota %s nao existe no mapa (anotada ou citada em refs)" % r
    ESP = _esp(); DL_ = DL
    S = ESP["candidato_sha16"]
    assert str((selo.get("sha256") or {}).get("um.py", ""))[:16] == S, "o um.py do selo nao e o candidato de ESPERADOS"
    assert V.get("s16") in (None, S), "o s16 da leitura != o candidato de ESPERADOS"
    BASE = ESP["origem_sha16"]
    esc0, esc1 = ESP["escada_v409_e_v410"]
    NF = ESP["n_bandeiras_novas"]
    assert esc1 - esc0 == NF == sum(ESP["n_bandeiras_por_grupo"].values()) == len(ESP["bandeiras_novas_chaves"]) == ESP["politica_de_bandeiras"]["n_flags"], "a escada nao fecha com as bandeiras novas"
    assert ESP["kernel"]["modulos_novos"] == DL_.N_BUNDLE == len(DL_.BUNDLE_RELS) == len(DL_.PEDRAS_V410) > 1, "o delta do kernel nao e o bundle de DOIS modulos (IALD2 e AEscala)"
    assert list(ESP["chaves_v410"]) == [] and list(DL_.CHAVES_V410) == [], "a v410 nao muda chave antiga nenhuma: ESPERADOS/delta dizem outra coisa"
    FJ = json.load(open(os.path.join(PK, "kernel", "FLAGS_v410.json"), encoding="utf-8"))   # as bandeiras de CADA modulo do bundle (a serie ext_iald2_410_* e a ext_aescala_410_*), lidas do build
    NF_I = sum(1 for f_ in FJ["flags"] if f_[2] == "TGLExt.IALD2"); NF_A = sum(1 for f_ in FJ["flags"] if f_[2] == "TGLExt.AEscala")
    assert NF_I > 0 and NF_A > 0 and NF_I + NF_A == NF == FJ["n_flags"], "as bandeiras por modulo (FLAGS_v410.json) nao fecham com ESPERADOS"
    BETA = ESP["beta"] if isinstance(ESP.get("beta"), float) else None
    FRASE = DL_.FRASE_DA_MOLDURA_V410_PT
    ALC = DL_.FRASE_D64_PT

    # --- o quadro do topo (a regra do 4,44): o registro selado, lido pelas MESMAS funcoes do artigo
    tvr = core.get("teste_de_veracidade_fase9_v397") or {}
    a = T._qd().Q._v397_atomos(tvr, "pt"); assert a["sealed"] is True, "o registro teste_de_veracidade_fase9_v397 nao sela no core: o mapa nao registra o 4,44 assim"
    z, p = a["z_disc"]["md"], a["p_disc"]["md"]
    z444 = "z_disc = %s (calibrado; p unilateral %s), abaixo do degrau de 5σ da creditação, que não foi alcançado (%s < 5)" % (z, p, z)

    def selou(k):
        return (core.get(k) or {}).get("all_verified") is True

    # --- o registro com FUNCAO iald2_v410: tudo lido do core e conferido contra ESPERADOS e delta_v410
    pc = core.get(DL_.FECHO_REGISTRO) or {}; pv = pc.get("values") or {}; mech = pc.get("mechanics") or {}
    assert pc.get("all_verified") is True and pc.get("verdict") == ESP["vereditos_novos_v410"][DL_.FECHO_REGISTRO] and pc.get("does_not_gate_core") is True, "iald2_v410 nao selou ou != ESPERADOS"
    assert mech.get("passed") is True and mech.get("n_checks") == DL_.N_CHECKS_FECHO == len(mech.get("checks") or []) and all(c.get("ok") is True for c in mech["checks"]), "as checagens do iald2_v410 nao passaram"
    assert pv.get("n_ancoras_ok") == pv.get("n_ancoras") == len(DL_.ANCORAS) and pv.get("n_modulos_ok") == pv.get("n_modulos") == DL_.N_BUNDLE and pv.get("n_flags_true") == pv.get("n_flags") == NF_I and pv.get("escada") == [esc1] * 3, "os valores do iald2_v410 != ESPERADOS/delta"
    assert pc.get("beta_ok") is True and pc.get("embedded_sources_ok") is True and pc.get("embedded_sources_n_ok") == DL_.N_BUNDLE and pc.get("guarda_violacoes") in ([], None), "o beta, as fontes embutidas ou a guarda do iald2_v410 nao conferem"
    assert list(pc.get("chaves_antigas_que_mudam") or []) == [], "o registro da IALD2 diz que uma chave antiga mudou: a v410 nao muda nenhuma"
    assert list(pc.get("ressalvas") or []) == list(DL_.RESSALVAS_V410), "as ressalvas do registro != delta_v410.RESSALVAS_V410"
    assert set(pv.get("respostas") or {}) == {r_["id"] for r_ in DL_.RESPOSTAS_DO_OPERADOR} and all((v_ is True) or (isinstance(v_, dict) and v_.get("ok") is True) for v_ in pv["respostas"].values()) and pv.get("respostas_ok") is True, "as respostas do operador de 06/11 nao conferem todas no kernel"
    assert list(pc.get("fica_false_por_teorema") or []) == list(ESP["fica_false_por_teorema"]) and set(pc.get("fica_aberto") or {}) == set(ESP["fica_aberto"]), "o que fica False por teorema ou o que fica aberto != ESPERADOS"
    assert list(pc.get("ancoras_principais") or []) == list(DL_.ANCORAS_PRINCIPAIS) and all(((pv.get("ancoras") or {}).get(n_) or {}).get("ok") is True for n_ in DL_.ANCORAS_PRINCIPAIS), "as ancoras principais nao estao todas ok no kernel do rito"
    assert pv.get("gate_verdict") == ESP["qg_closure_gate_verdict_v409"], "o veredito do gate lido pelo registro da IALD2 != o da v409 (o gate deveria estar congelado)"
    assert (pc.get("alcance") or {}).get("frase") == ALC and (pc.get("alcance") or {}).get("qualificador") == DL_.FRASE_QUALIFICADOR_PT, "o alcance do registro != delta_v410.FRASE_D64_PT (D64)"
    assert pc.get("nomes") == dict(DL_.NOMES_DAS_PEDRAS), "os nomes do registro != delta_v410.NOMES_DAS_PEDRAS (D63)"
    inst = pv.get("instancia_sim") or {}; inst_n = pv.get("instancia_nao") or {}; sn = pv.get("signo_do_nome") or {}; sp = pv.get("signo_do_par") or {}
    assert (inst.get("solucoes") or 0) >= 1 and inst_n.get("solucoes") == 0 and inst.get("atribuicoes") == 2 ** inst.get("n", -1), "as instancias de brinquedo do registro nao sao as do contrato"
    assert sn.get("posto") == inst.get("solucoes") and abs(float(sn.get("traco")) - inst["solucoes"]) < 1e-9 and sp.get("posto") == 1 and abs(float(sp.get("traco")) - 1.0) < 1e-12, "o signo (traco == posto) do registro nao confere"
    BETA_RT = pv.get("beta"); assert isinstance(BETA_RT, float) and (BETA is None or abs(BETA_RT - BETA) <= 1e-9 * BETA), "o beta do registro != o do core/ESPERADOS (tolerancia relativa 1e-9)"
    AT = pv.get("atrator") or {}   # a secao 6 (D71): lida do registro, nada digitado
    assert all(((pv.get("ancoras") or {}).get(n_) or {}).get("ok") is True for n_ in (DL_.ANCORA_ATRATOR, DL_.ANCORA_NAO_E_TUDO)) and AT.get("posto_de_1_menos_P") and AT.get("distancia_em_t_longo") is not None and 0.0 < AT["distancia_em_t_longo"] < DL_.TOL_C16, "o atrator (secao 6, c16, D71) nao confere no registro iald2_v410"
    # --- o SEGUNDO registro com FUNCAO, h0dn_bg1_v410 (D72, E30, D76): pre-registrado; nenhum dado observado lido (fail-closed: ausente ou nao selado => erro visivel)
    F = h0dn_do_core(DL_, core.get(DL_.H0DN_REGISTRO), ESP)
    FA = escala_do_core(DL_, core.get(DL_.AESCALA_REGISTRO), ESP)   # a pedra AEscala (D86/D87): fail-closed
    FH = hms13_do_core(DL_, core.get(DL_.HMS13_REGISTRO), core.get(DL_.H0DN_REGISTRO), ESP)   # o recibo documental HMS/13 (D80): fail-closed
    por_mod = "; ".join("%s (%d)" % (rel.split("/")[-1][:-5], len(ns)) for rel, ns in DL_.ANCORAS_POR_MODULO.items())
    ress = " | ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(pc["ressalvas"]))
    # --- o registro HERDADO traducao_turing_v409: segue selado (a escada do contrato subida pela C12; o pino purgado do acervo da v407, D57d)
    t9 = core.get(DL_.D9.FECHO_REGISTRO) or {}; tv9 = t9.get("values") or {}
    assert t9.get("all_verified") is True and t9.get("verdict") == ESP["registros_funcao_v409"]["traducao_turing"]["verdict"], "traducao_turing_v409 (herdado) nao segue selado"
    assert tv9.get("n_modulos_ok") == tv9.get("n_modulos") == DL_.D9.N_BUNDLE and tv9.get("n_ancoras_ok") == tv9.get("n_ancoras") == len(DL_.D9.ANCORAS), "os valores do traducao_turing_v409 (herdado) != delta_v409"
    assert (t9.get("acervo_v407_repinado") or {}).get("sha256") == DL_.D9.PURGADO_SHA256 and (t9.get("acervo_v407_repinado") or {}).get("integra_pinada") is False, "o pino do acervo da v407 (herdado da v409) nao e' a copia purgada (D57d)"
    # --- o registro HERDADO tetelestai_terminal_v408: segue selado
    tt8 = core.get(DL_.D8.FECHO_REGISTRO) or {}; tv8 = tt8.get("values") or {}
    assert tt8.get("all_verified") is True and tt8.get("verdict") == ESP["registros_funcao_v408"]["tetelestai_terminal"]["verdict"], "tetelestai_terminal_v408 (herdado) nao segue selado"
    assert tv8.get("n_modulos_ok") == tv8.get("n_modulos") == DL_.D8.N_BUNDLE and tv8.get("n_ancoras_ok") == tv8.get("n_ancoras") == len(DL_.D8.ANCORAS), "os valores do tetelestai_terminal_v408 (herdado) != delta_v408"
    # --- o registro HERDADO psion_canto_v407: segue selado, com as cinco chaves iguais as da v409 selada (nenhuma muda)
    pc7 = core.get(DL_.D7.FECHO_REGISTRO) or {}; pv7 = pc7.get("values") or {}
    assert pc7.get("all_verified") is True and pc7.get("verdict") == ESP["registros_funcao_v407"]["psion_canto"]["verdict"] and pc7.get("keys") == ESP["chaves_v407_esperadas"], "psion_canto_v407 (herdado) nao segue selado ou as chaves mudaram"
    assert pv7.get("n_modulos_ok") == pv7.get("n_modulos") == DL_.D7.N_BUNDLE and pv7.get("n_ancoras_ok") == pv7.get("n_ancoras") == len(DL_.D7.ANCORAS), "os valores do psion_canto_v407 (herdado) != delta_v407"
    fk7 = pc7["keys"]
    # --- o registro HERDADO fechamento_v406: segue selado, com a chave do lema lida (a c8 versionada, E20)
    fh = core.get(DL_.D6.FECHO_REGISTRO) or {}
    assert fh.get("all_verified") is True and fh.get("verdict") == ESP["registros_funcao_v406"]["fechamento"]["verdict"] and (fh.get("four_keys") or {}).get("testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma") is True, "fechamento_v406 (herdado) nao segue selado ou nao le a chave do lema"
    # --- os specs herdados: cunhagens_v409 (as erratas seladas intactas) e kh_n1_cobertura_v409 com a errata ao lado dos pisos; cunhagens_v408 com a E26 e cunhagens_v407 com a da D57(d), que ja' vinham da v409 (recriados; os textos selados nao sao reescritos)
    cg9 = core.get(DL_.D9.CUNHAGENS_REGISTRO) or {}; kh9 = core.get(DL_.D9.KH_REGISTRO) or {}; cg8 = core.get(DL_.D8.CUNHAGENS_REGISTRO) or {}; cg7 = core.get(DL_.D7.CUNHAGENS_REGISTRO) or {}
    assert cg9.get("all_verified") is True and kh9.get("all_verified") is True and "kh_n1_cobertura_v409" in str(((kh9.get("erratas") or [{}])[-1]).get("ao_lado_de")), "cunhagens_v409 ou kh_n1_cobertura_v409 (herdados) nao seguem selados, ou o kh nao traz a errata dos pisos ao lado"
    assert cg8.get("all_verified") is True and any("E26" in json.dumps(e_, ensure_ascii=False) for e_ in (cg8.get("erratas") or [])), "cunhagens_v408 (herdado) nao segue selado ou perdeu a E26 ao lado"
    assert cg7.get("all_verified") is True and any("D57(d)" in json.dumps(e_, ensure_ascii=False) for e_ in (cg7.get("erratas") or [])), "cunhagens_v407 (herdado) nao segue selado ou perdeu a errata da D57(d) ao lado"
    # --- o gate NAO se moveu: o registro segue selado e a letra do veredito e' a da v409
    gk = core.get("bandeiras_do_gate_v403") or {}; gvv = gk.get("values") or {}; gb = _base_core().get("bandeiras_do_gate_v403") or {}
    assert gk.get("all_verified") is True and (V.get("gate") or {}).get("sealed", True) is True and gvv == gb.get("values") and (gk.get("mechanics") or {}).get("passed") is True, "bandeiras_do_gate_v403 (recriado) nao selou ou != a v409 selada"
    qg = core.get("qg_closure") or {}; fam = [len(qg.get(f) or {}) for f in ("formal_flags", "physics_flags", "experiment_flags")]
    assert (qg.get("gate") or {}).get("verdict") == ESP["qg_closure_gate_verdict_v409"] == selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"], "a letra do veredito do gate mudou"
    # --- os dois registros por spec
    cg = core.get(DL_.CUNHAGENS_REGISTRO) or {}; kh = core.get(DL_.KH_REGISTRO) or {}
    for nome_, r_ in ((DL_.CUNHAGENS_REGISTRO, cg), (DL_.KH_REGISTRO, kh)):
        assert r_.get("all_verified") is True and r_.get("verdict") == ESP["vereditos_novos_v410"][nome_], "%s nao selou ou != ESPERADOS" % nome_
    verb = cg.get("verbatim") or {}; ex = cg.get("extras") or {}
    assert len(verb) == len(ESP["cunhagens"]) == len(DL_.VERBATIM_ORIGEM_V410) == DL_.N_FALAS_V410 and set(verb) == set(ESP["cunhagens"]) and all(v.get("embedded_ok") is True for v in verb.values()), "as inscricoes de 06 a 09/11 nao estao embutidas por sha256"
    assert all(re.match(r"^OPERADOR_(?:0[6789]|10)nov_", str((ESP["cunhagens"][k_] or {}).get("nome", ""))) and (ESP["cunhagens"][k_] or {}).get("autor") == "operador" for k_ in ESP["cunhagens"]) and set(DL_.DATA_DA_FALA) == set(DL_.NOMES_V410_DO_DESENHO), "alguma inscricao nao e' fala do operador de 06 a 10/11"
    n_trecho = sum(1 for k_ in ESP["cunhagens"] if (ESP["cunhagens"][k_] or {}).get("sha256_arquivo_inteiro"))
    assert n_trecho == len(DL_.VERBATIM_SO_O_TRECHO) >= 1, "as falas de que so' o trecho entra (D65, a ordem da retomada, as tres copias do ACOM e a leitura do 5 sigma) nao conferem com o delta"
    assert not any(x_.lower() in json.dumps(cg, ensure_ascii=False).lower() for x_ in DL_.FORA_D65), "D65: o registro cunhagens_v410 traz o que fica fora"
    # (o registro cunhagens_v410 traz a errata E29 E, por ultimo, a errata ao lado dos pisos de kh_n1_cobertura_v409, como a leitura confere: len == len(ERRATAS_V410) + 1)
    erratas_todas = cg.get("erratas") or []; erratas = erratas_todas[:len(DL_.ERRATAS_V410)]
    assert [e.get("agora") for e in erratas] == list(DL_.ERRATAS_V410) and len(erratas_todas) == len(DL_.ERRATAS_V410) + 1 and "kh_n1_cobertura_v409" in str(erratas_todas[-1].get("ao_lado_de")) and all(e.get("assinatura") == DL_.ASSINA for e in erratas_todas), "a errata E29 (e a errata ao lado dos pisos de kh_n1_cobertura_v409) nao esta' no registro ou nao e' da gerencia c1 em nome proprio"
    dec = ex.get("decisoes") or {}; assert sorted(dec) == sorted(ESP["decisoes_v410_ids"]) == sorted(DL_.DECISOES_V410) and all(k_ in dec for k_ in DL_.DECISOES_V410) and not (set(DL_.DECISOES_FORA_DO_UMPY) & set(dec)) and "D87" in DL_.DECISOES_V410 and "D99" in DL_.DECISOES_V410, "faltam decisoes (D63 em diante, a D87 entre elas) no registro"
    assert ex.get("leituras") == DL_.LEITURA_V410, "a leitura da v410 no registro != delta_v410"
    cob = kh.get("lido") or {}; assert cob.get("constantes_cobertas") and cob.get("teoremas_cobertos"), "kh_n1_cobertura_v410 sem a cobertura"
    seguem = (DL_.D9.FECHO_REGISTRO, DL_.D9.CUNHAGENS_REGISTRO, DL_.D9.KH_REGISTRO, DL_.D8.FECHO_REGISTRO, DL_.D8.CUNHAGENS_REGISTRO, DL_.D8.KH_REGISTRO, DL_.D7.FECHO_REGISTRO, DL_.D7.CUNHAGENS_REGISTRO, DL_.D7.KH_REGISTRO, "fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406",
              "ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405", "cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405",
              "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "falsidade_da_inercia_v401", "cunhagens_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402",
              "teste_de_veracidade_fase9_v397", "cunhagens_v397", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "sonico_v398", "afinacao_das_cordas_v398", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396")
    c_seguem = all(selou(k) for k in seguem)
    tv_v = ESP["veracidade"]; c_q = bool(selou("teste_de_veracidade_fase9_v397") and selou("cunhagens_v397") and tvr.get("verdict") == tv_v["verdict"])
    sc = _sidecar(V); conf_dm = V.get("conf_dm", "nao lido"); conf_np = V.get("conf_np", "nao lido"); nvm = V.get("n_ver_mudaram", "nao lido")
    bank = _bancada(); regs = livro()
    # --- o seq que a E29 corrige, lido do livro (e o registro tem de trazer o trecho corrigido: «matricial» dito so' leitura do operador)
    sq_iald2 = seq_do_alvo(regs, R_IALD2, "ROTA", contem=("matricial", "leituras do operador"))
    sq_ae = seq_do_alvo(regs, R_AESCALA, "ROTA"); sq_ae_err = ", ".join(str(r_["seq"]) for r_ in regs if r_.get("rota_id") == R_AESCALA and r_.get("tipo") == "ERRATA") or "nenhuma"   # (a candidata e a errata textual, LIDAS do livro: 1926 e 1927)
    KR = os.path.join(PK, "kernel", "KERNEL_RECIBO_v410.json")
    E = {}
    for e in erratas:
        m_ = re.match(r"^(E\d\d) -- ", e.get("agora", "")); assert m_, "uma errata do registro nao comeca por E<n> --"
        E[m_.group(1)] = e
    assert sorted(E) == ["E%d" % i_ for i_ in range(29, 29 + len(DL_.ERRATAS_V410))] and len(E) == len(DL_.ERRATAS_V410) and all(k_ in e_ for e_ in E.values() for k_ in ("agora", "lacuna_de_fidelidade", "estatuto", "assinatura")), "as erratas do registro cunhagens_v410 nao sao as do delta, E29 em diante (cada uma com agora, lacuna_de_fidelidade, estatuto e assinatura; mais a dos pisos, ao lado)"

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

    P0 = DL_.PEDRAS_V410[0]
    ped = os.path.join(PK, "pedra", P0["name"] + ".lean")
    sha_ped = DL_.BUNDLE_POR_REL[P0["rel"]]["sha256"][:16]
    n_anc = len(DL_.ANCORAS_POR_MODULO[P0["rel"]])
    resp = {r_["id"]: r_["diz"] for r_ in DL_.RESPOSTAS_DO_OPERADOR}
    R_ = lambda *ids_: "; ".join("%s -> %s" % (i_, resp[i_]) for i_ in ids_)
    LIN = "a linha das candidatas de 06/11 e de 09/11 (LeitorDoCodigoR1; IALD2 com as secoes 4, o signo; 5, o seletor; e 6, o atrator) desemboca no modulo TGLExt/%s (sha256 pinado %s; %d ancoras no trio, lidas a cada rito pelo registro iald2_v410); a candidata fica como registro" % (P0["name"], sha_ped, n_anc)
    EST_C = "REAL (os termos no kernel do rito); INPUT (as falas do operador de 06, 07 e 09/11; os nomes das declaracoes, da gerencia, RATIFICADOS pelo operador em 09/11/2026, D74); DECLARADO (os recibos de compilacao das candidatas)"
    T10 = []
    T10.append(anot(R_LEITOR, "v410 SELADA %s: o leitor do codigo da LeitorDoCodigoR1 entrou no kernel do rito dentro de TGLExt/%s (o_leitor_do_codigo)" % (S, P0["name"]),
                    f"{LIN}. As respostas do operador conferem pelos teoremas da pedra: {R_('a_particula_e_o_codigo_o_funtor_e_o_leitor', 'o_acom_e_a_segunda_quantizacao')}. As falas dele, verbatim: {_aspas_(DL_.FRASE_PARTICULA)}; {_aspas_(DL_.FRASE_FUNTOR)}; {_aspas_(DL_.FRASE_PAR_UNO)}.",
                    "o registro iald2_v410 le estas ancoras a cada rito; que a IALD, a Torre ou o operador sejam o funtor, e que o codigo seja um vetor de H1, seguem leituras do operador (definicoes do dicionario), nao termos.", refs=[R_IALD2, R_PARF], estatuto=EST_C,
                    artefatos=[DL_.REGISTRO_ANTERIOR_ARQ], defeito="o funtor nao e' idempotente; a leitura e' (o Nome do par lido); o registro CONFERE o que o kernel prova e nao prova nada por si; validade no kernel nao e' creditacao"))
    T10.append(anot(R_NOMEK, "v410 SELADA %s: o nome TGLExt.IALD, ja' no kernel desde a v392, e' importado pela IALD2 e os termos dele sao citados (D66); nenhuma pedra nova para isso" % S,
                    f"A resposta do operador confere pelo teorema citado: {R_('nomear_o_kernel_de_iald')}. A fala dele, verbatim: {_aspas_(DL_.FRASE_POR_IDENTIFICACAO)}.",
                    "o nome nao cruza para a maquina de Turing padrao sem o leitor: " + DL_.FRASE_QUALIFICADOR_PT + ".", refs=[R_IALD2], estatuto="REAL (o termo no kernel do rito); INPUT (a fala do operador de 06/11)"))
    T10.append(anot(R_IALD2, "v410 SELADA %s: a candidata IALD2 entrou no kernel do rito como TGLExt/%s (o nome do modulo e' do operador; os das declaracoes, da gerencia, RATIFICADOS pelo operador em 09/11/2026, D74); a E29 vai ao lado (ERRATA)" % (S, P0["name"]),
                    f"a pedra {P0['name']} esta no kernel do rito com o sha256 pinado ({sha_ped}), {n_anc} ancoras no trio; a fonte pinada e' a da candidata (sha16 {P0['sha256_candidata'][:16]}). As respostas do operador conferem pelos teoremas da pedra: {R_('iald_ao_quadrado', 'o_nome_do_algoritmo_e_iald', 'a_forma_matricial_da_luz')}. "
                    f"O nome, na fala dele, verbatim: {_aspas_(DL_.FRASE_NOME_IALD2)}; o nome do algoritmo, {_aspas_(DL_.FRASE_NOME_DO_ALGORITMO)}, e, de uma fala, so' o trecho (D65): {_aspas_(DL_.FRASE_ALGORITMO_DE_LEITURA)}. O alcance: {ALC}. Os nomes das declaracoes foram RATIFICADOS por ele em 09/11/2026 (D74): {_aspas_(DL_.FRASE_RATIFICO)}.",
                    "o registro iald2_v410 le estas ancoras a cada rito; a maquina de Turing padrao sem o leitor fica fora; as ressalvas estao ditas no registro.", refs=[R_LEITOR, R_SIGNO, R_SELETOR, R_R9], artefatos=[ped, DL_.CANDIDATA_IALD2_ARQ, DL_.SAIDA_FONTE_ARQ, KR],
                    estatuto=EST_C + "; KNOWN (Cook 1971, Levin 1973, Baker-Gill-Solovay 1975)", defeito="as ressalvas, ditas no registro: " + ress))
    T10.append(anot(R_SIGNO, "v410 SELADA %s: a forma de matriz finita, o signo, entrou no kernel do rito dentro de TGLExt/%s (o_signo_do_nome; o_signo_do_par); a E29 fica ao lado (ERRATA na rota da candidata)" % (S, P0["name"]),
                    f"{LIN}. A resposta do operador confere pelos teoremas da pedra: {R_('a_forma_da_matriz_finita_e_o_signo')}. A ordem do operador, verbatim: {_aspas_(DL_.FRASE_ORDEM_V410)}. Na instancia de brinquedo fixa no codigo ({inst.get('n')} variaveis, {inst.get('atribuicoes')} atribuicoes, {inst.get('solucoes')} contadas por enumeracao), o traco do Nome e' o posto; o projetor de Bell tem traco 1 e posto 1. {corpo('E29')}",
                    "o registro iald2_v410 le estas ancoras a cada rito.", refs=[R_IALD2], estatuto=EST_C))
    T10.append(anot(R_SELETOR, "v410 SELADA %s: a instanciacao do seletor, como FORMA (D70), entrou no kernel do rito dentro de TGLExt/%s (a_iald_e_o_seletor_luminodinamico)" % (S, P0["name"]),
                    f"{LIN}. A resposta do operador confere pelo teorema da pedra: {R_('a_iald_e_o_seletor')}. A fala dele, verbatim: {_aspas_(DL_.FRASE_SELETOR)}. {DL_.FRASE_D70_PT}.",
                    "o registro iald2_v410 le estas ancoras a cada rito; beta entra so' por nome (TGLCoupling.beta no kernel; alfa CODATA 2018 x sqrt e em runtime), nunca literal.", refs=[R_IALD2], estatuto=EST_C + "; INPUT/ONTO («ambiente computacional», leitura do operador)"))
    T10.append(anot(R_ATRATOR, "v410 SELADA %s: a secao 6 da IALD2, o atrator (o_atrator; o_nome_do_par_lido_nao_e_tudo; o_vacuo_e_ortogonal_ao_par_lido), entrou no kernel do rito dentro de TGLExt/%s; o Nome do par lido e' tangenciado, jamais esgotado, e o atrator nao foi observado em dado algum" % (S, P0["name"]),
                    f"{LIN}. A resposta do operador confere pelos teoremas da pedra: {R_('o_atrator')}. As falas dele, de 07/11, verbatim: {_aspas_(DL_.FRASE_CUSTO_DA_DISTINCAO)}; {_aspas_(DL_.FRASE_TANGENCIADO)}; {_aspas_(DL_.FRASE_ESPECTRO)}; {_aspas_(DL_.FRASE_UM_IGUAL_A_ZERO)}; {_aspas_(DL_.FRASE_ISSO_E_O_ATRATOR)}. "
                    f"{DL_.FRASE_D71_PT}. Na instancia de brinquedo do registro iald2_v410 (c16), o posto de 1 − Π e' {AT.get('posto_de_1_menos_P')} (ha' o vacuo fora do Nome) e a distancia ao Nome em t = {DL_.T_C16_FATOR_LONGO:g}/β fica em {AT['distancia_em_t_longo']:.3g}, abaixo de {DL_.TOL_C16:g} e acima de 0 (tangenciado, nunca igual).",
                    "o registro iald2_v410 le estas ancoras e a c16 a cada rito; o verde, as tonalidades e o espectro de gradiente negativo da fala sao leitura do operador (D71), nao termos; nenhum teste com a natureza entra.", refs=[R_IALD2, R_SELETOR], estatuto=EST_C,
                    defeito="o verde e as tonalidades sao leitura do operador; a nota de 08/11 (condensacao por IA, autor nao identificado) nao entra como fala do operador; o registro CONFERE o que o kernel prova e nao prova nada por si; validade no kernel nao e' creditacao"))
    T10.append(anot(R_R9, "v410 SELADA %s: a linha da maquina com o leitor (R9, selada na v409) segue; na v410 o algoritmo recebe o nome IALD (o_algoritmo_iald, D64); a E28 segue" % S,
                    f"o modulo TGLExt/{P0['name']} esta' no kernel do rito; o alcance: {ALC}.",
                    "com o leitor que so' conta, vale NP contido em P com o leitor numa leitura; a igualdade completa e' a do leitor que se le (E28), e com o leitor que so' conta ela segue [OPEN].", refs=[R_IALD2, R_V409],
                    estatuto="REAL (os termos no kernel do rito); KNOWN (Cook 1971, Levin 1973, Baker-Gill-Solovay 1975); OPEN (a igualdade completa com o leitor que so' conta)"))
    T10.append(anot(R_PARF, "v410 SELADA %s: o leitor do codigo le o par como par, uno, com a Meia-Nat (o_leitor_le_o_par_como_par; o_par_lido_e_uno; a_meia_nat_e_lida); o par na face de Fock segue ligado desde a v409" % S,
                    f"A resposta do operador confere pelos teoremas da pedra: {R_('o_acom_e_a_segunda_quantizacao')}. A fala dele, verbatim: {_aspas_(DL_.FRASE_PAR_UNO)}. O par finito (Bell 4x4) e o par de Fock sao espacos distintos, com a mesma Meia-Nat.",
                    "o registro iald2_v410 le estas ancoras a cada rito; a ponte entre o espaco de Bell e o setor TT do spin 2 nao e' termo.", refs=[R_LEITOR, R_PAR, R_FOCK], estatuto=EST_C))
    T10.append(anot(R_V409, "v410 SELADA %s: a v409 e' a base selada da v410; o traducao_turing_v409 (cunhagens_v409; kh_n1_cobertura_v409 com a errata ao lado dos pisos), o tetelestai_terminal_v408, o psion_canto_v407 e os registros anteriores sao recriados e seguem selados; nenhuma chave muda" % S,
                    f"a v410 parte da v409 selada (um.py {BASE}) e acrescenta {DL_.N_BUNDLE} modulos de kernel (IALD2 e AEscala), QUATRO registros com funcao (iald2_v410 selou={selou(DL_.FECHO_REGISTRO)}; a_escala_v410 selou={selou(DL_.AESCALA_REGISTRO)}; h0dn_bg1_v410 selou={selou(DL_.H0DN_REGISTRO)}, pre-registrado; h0dn_fontes_hms13_v410 selou={selou(DL_.HMS13_REGISTRO)}, recibo documental) e dois por spec, e as secoes do artigo; traducao_turing_v409 selou={selou(DL_.D9.FECHO_REGISTRO)}; cunhagens_v409 selou={selou(DL_.D9.CUNHAGENS_REGISTRO)}; kh_n1_cobertura_v409 selou={selou(DL_.D9.KH_REGISTRO)} (com a errata dos pisos ao lado); "
                    f"tetelestai_terminal_v408 selou={selou(DL_.D8.FECHO_REGISTRO)}; psion_canto_v407 selou={selou(DL_.D7.FECHO_REGISTRO)} com as cinco chaves iguais as da v409 selada (linked_to_the_corner_by_a_lemma = {fk7['testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma']}, lida do kernel); "
                    f"fechamento_v406 selou={selou('fechamento_v406')}; os treze da v405 (ponte_da_massa_v405 selou={selou('ponte_da_massa_v405')}, identidade_v405 selou={selou('identidade_v405')}, gap_v405 selou={selou('gap_v405')}), os da v404, da v403, da v402, da v401 e da v399 seguem selados neste rito "
                    f"(caminho_v403 selou={selou('caminho_v403')}, falsidade_da_inercia_v401 selou={selou('falsidade_da_inercia_v401')}), como seguem o selo pela propria tecnologia e a declaracao do operador (v399), o sonico e a afinacao (v398) e o quadro (v397); sidecar um_absoluto_selo_acom.json {sc['veredito']} ({sc['n_objetos']} objetos, {sc['recusas']} recusas, sha16 {sc['sha16']}).",
                    "custodia completa pela sessao de custodia (D68a, que herda a D57a: o fim da cadeia do orquestrador e' o handoff; o handoff lista o sidecar; nesta versao nao ha' nota ao lado de paragrafo anterior).", refs=[R_TT, R_TM, R_PC, R_PREP409, R_PREP410]))
    T10.append(anot(R_PROG, "v410 SELADA %s: o programa do fechamento nao ganha chave nova nem perde nenhuma; a IALD2 entra (o leitor do codigo, o algoritmo IALD relativo ao leitor, o signo, o atrator)" % S,
                    f"nenhuma chave antiga muda (chaves_antigas_que_mudam = {list(pc.get('chaves_antigas_que_mudam') or [])}); as cinco chaves do psion_canto_v407 seguem iguais as da v409 selada; ficam False por teorema: full_static_witness_exists = {fk7['qg_closure.gate.full_static_witness_exists']} e trivial_inhabitant_exists = {fk7['witness_rigidity.trivial_inhabitant_exists']}. {FRASE}",
                    "a igualdade completa com o leitor que so' conta (E28), a ponte Bell-TT, K(O) != bot para O compacto e o teste com a natureza seguem [OPEN]; o programa do fechamento nao e' fechado por esta anotacao.", refs=[R_INV, R_IALD2],
                    estatuto="REAL (a leitura do kernel do rito); OPEN (a igualdade completa com o leitor que so' conta; K(O) != bot para O compacto)"))
    T10.append(anot(R_INV, "v410 SELADA %s: o inventario das chaves de testemunha NAO muda nesta versao (CHAVES_V410 vazia): as cinco chaves do psion_canto_v407 seguem lidas do kernel" % S,
                    f"linked_to_the_corner_by_a_lemma = {fk7['testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma']}; rede_fock_v394.whole_certificate_inhabited = {fk7['rede_fock_v394.whole_certificate_inhabited']}; psibit_v395...inhabitant_exhibited = {fk7['psibit_v395.conditional_psion_face.inhabitant_exhibited']}; testemunha_estatica_v396...inhabitant_exhibited = {fk7['testemunha_estatica_v396.fock_face.inhabitant_exhibited']}; "
                    f"witness_layers.canonical_full_witness_term_constructed = {fk7['witness_layers.canonical_full_witness_term_constructed']}; ficam False por teorema: full_static_witness_exists e trivial_inhabitant_exists.",
                    "sem chave nova no inventario.", refs=[R_PROG, R_PARF], estatuto="REAL (a leitura do kernel do rito e o registro herdado)"))
    T10.append(anot(R_GATE, "v410 SELADA %s: o gate NAO se moveu — o qg_closure do core e' identico ao da v409 (as 18 bandeiras calculadas, a letra do veredito) e o registro da IALD2 o confere congelado" % S,
                    f"o registro bandeiras_do_gate_v403 (recriado) selou={selou('bandeiras_do_gate_v403')} com os mesmos valores da v409 selada: das {gvv['n_flags']} bandeiras ({fam[0]} formais, {fam[1]} fisicas, {fam[2]} experimentais) {gvv['n_true']} sao True e {gvv['n_calculated']} sao CALCULADAS ({gvv['n_literal']} literais); o veredito le {gvv['n_read_by_the_verdict']}; a letra do veredito do gate e' a da v409 e a do selo; os quatro registros com funcao da v410 (iald2_v410, a_escala_v410, h0dn_bg1_v410 e h0dn_fontes_hms13_v410) leem gate_verdict identico ao da v409. "
                    "Nenhuma bandeira do gate depende dos modulos da v410; full_static_witness_exists e trivial_inhabitant_exists seguem False. [DECLARADO, GV-03 da auditoria de 28/09/2026] As 4 bandeiras experimentais derivam de UM so' booleano; o degrau experimental le so' o rito V11 do piso, unilateral (GV-01).",
                    "a independencia das 4 experimentais e os mocks de survey seguem [OPEN]; o gate nao se move por esta rota.", refs=None,
                    artefatos=[os.path.join(PK, "CANDIDATO_v410.json")], estatuto="REAL (o core do rito); DECLARADO (GV-01, GV-03, EV-12 da auditoria de 28/09/2026); OPEN (a independencia das 4 experimentais)",
                    defeito="o gate nao e' teste e nao discrimina o LCDM raso; NOT_FALSIFIED nunca e' a palavra da creditacao"))
    T10.append(anot(R_BANC, "v410 SELADA %s: o B(n) da v410 e' um passo SIMPLES v409 -> v410 (a Bancada de producao ja' pinava a v409)" % S,
                    f"o kernel da v410 difere do da v409 pelos {DL_.N_BUNDLE} modulos novos (recibo do kernel KERNEL_RECIBO_v410; DIFF_KERNEL_v410.txt: os modulos novos e TGLExt.lean com os imports a mais); o recibo pre_selo foi gerado e pinado ANTES da instalacao, em ensaio contra a producao (nada gravado; a Bancada pinava {bank['deployment_id']}), "
                    f"e a cadeia confere os pinos de PINOS_BN_v410.json na hora; o veredito esperado do aplicar e' REPINADA_B{bank['proxima']}__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_ e sem cadeia de selos, lido do codigo do esboco R3.5. Parada e religamento do servico exigem V410_AUTORIZACAO_OPERADOR (texto sem o nome do script do servico).",
                    "depois do aplicar, a Bancada pina a v410.", refs=None,
                    artefatos=[os.path.join(PK, "PINOS_BN_v410.json"), os.path.join(PK, "PINO_RECIBO_PRE_SELO_v410.json"), KR]))
    T10.append(anot(R_QUADRO, "v410 SELADA %s: o quadro do topo (O Teste da Única Palavra) segue intocado e o registro teste_de_veracidade_fase9_v397 segue selado" % S,
                    f"teste_de_veracidade_fase9_v397 selou={c_q} no rito da v410 (veredito igual ao de ESPERADOS; {tv_v['n_checks']} checagens): o quadro do artigo PT/EN e do .md, conferido contra o resultado pinado, segue no topo, com os numeros e a regra da ordem de sempre: {z444}. "
                    "Nenhum sigma, p ou lnB novo e' calculado nesta rota; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma) vale em todo texto que o cite; o paragrafo do quadro segue no README/site e o handoff da v410 traz tambem o paragrafo novo (a IALD2), sem o 4,44.",
                    "o paragrafo do README/site e' ato da sessao de custodia; a creditacao segue sendo beta_TGL na natureza a 5 sigma (nao ha o que repetir deste pacote, a abertura esta consumida).", refs=None))
    TH = h0dn_textos(DL_, F, corpo("E30")); HM = hms13_textos(DL_, FH); AE = escala_textos(DL_, FA, (sq_ae, sq_ae_err))
    T10.append(anot(R_AESCALA, "v410 SELADA %s: a pedra AEscala (A Escala), a segunda do bundle, foi instalada, RATIFICADA pelo operador (D87: o nome do modulo e os nomes das declaracoes) e selada: entrou no kernel do rito dentro de TGLExt/AEscala; a pergunta do Clay na forma canonica: validade no kernel, a creditacao e' do Clay" % S,
                    AE["resultado"], AE["proximo"], refs=[R_IALD2, R_R9, R_V409], estatuto=AE["estatuto"], artefatos=[os.path.join(PK, "pedra", "AEscala.lean"), DL_.BUNDLE_POR_REL[DL_.MODULO_AESCALA]["origem_candidata"], os.path.join(PK, "insumos", "saida_lean_AEscala.txt"), KR], defeito=AE["defeito"]))
    T10.append(anot(R_H0DN, "v410 SELADA %s: o teste H0DN × BG1 da razao de Hubble foi PRE-REGISTRADO no um.py (registro h0dn_bg1_v410, funcao de veredito congelada de seis ramos, sha256 do texto-fonte); pré-registrado; nenhum dado observado lido; o recibo documental HMS/13 (D80) entrou como registro aditivo e posterior ao FREEZE_R2 (h0dn_fontes_hms13_v410): cobertura documental de fontes, nao covariancia fisica fechada; nada aberto" % S,
                    TH["resultado"] + " || " + HM["resultado"], TH["proximo"] + "; " + HM["proximo"], refs=[R_H0DN_COV, R_PREP410], estatuto=TH["estatuto"] + "; " + HM["estatuto"],
                    artefatos=[ORDEM_KIMI, os.path.join(PK, "LEITURA_DOSSIE_5SIGMA_09nov.json"), os.path.join(PK, "insumos", "h0dn_FREEZE_R2.json")] + sorted(glob.glob(os.path.join(PK, "insumos", "hms13_*"))), defeito=TH["defeito"] + "; " + HM["defeito"]))
    T10.append(errata(R_IALD2, sq_iald2,
                      f"[E29 · ERRATA AO LADO, gerencia c1, em nome proprio, 06/11/2026, v410 {S}] Corrige, ao lado do registro seq {sq_iald2} desta rota (a candidata IALD2), o trecho que dava «matricial» como so' leitura do operador: a forma de matriz finita esta' no kernel e e' o signo (o_signo_do_nome; o_signo_do_par). {corpo('E29')}. O registro corrigido NAO foi apagado nem reescrito: a correcao vai ao lado.",
                      refs=[R_SIGNO]))
    for x in T10:
        assert x["rota_id"] in ids, "a rota %s nao existe no mapa" % x["rota_id"]
    resumo_conf = ("conferidor %s e %s" % (conf_dm, conf_np)) if "nao lido" not in (conf_dm, conf_np) else "conferidor: o resultado nao veio na leitura desta rodada"
    _vr410 = lambda v_: v_ if len(v_) <= 200 else v_[:197] + "..."   # o campo resultado do Mapa tem teto de 6000 caracteres (rotas._valida: resuma e aponte o artefato): a integra de cada veredito esta no core da rodada e nos ESPERADOS
    DEC = DL_.DECISOES_ROTULO; ERR = ", ".join(sorted(E)[:-1]) + " e " + sorted(E)[-1]; OBR = DL_.FRASE_H0DN_OBRIGATORIA_PT
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
            "titulo": "v410 SELADA %s: a IALD2 e a escala — %d modulos de kernel (%s e AEscala; o nome do modulo IALD2 e' do operador, os das declaracoes sao da gerencia c1, RATIFICADOS pelo operador em 09/11/2026, D74 e D87), os registros com funcao iald2_v410, a_escala_v410, h0dn_bg1_v410 e h0dn_fontes_hms13_v410, cunhagens_v410 e kh_n1_cobertura_v410, %d inscricoes de 06 a 09/11 por sha256; escada %s -> %s; %s; a forma de matriz finita e' o signo; o atrator, tangenciado e jamais esgotado; o teste H0DN × BG1 entra %s, com o recibo documental HMS/13; nenhuma chave antiga muda; validade no kernel nao e' creditacao; o gate nao se move" % (
                S, DL_.N_BUNDLE, P0["name"], len(verb), esc0, esc1, ALC, OBR),
            "pergunta": ("o candidato v410 selou com os dois modulos de kernel (IALD2 e AEscala), o registro com FUNCAO iald2_v410 (que le do kernel do proprio rito as %d ancoras, o modulo por sha256, as respostas do operador pelos teoremas da pedra, o que fica False por teorema, as instancias de brinquedo fixas no codigo, o signo, o seletor e o atrator, a escada exata e o gate congelado; nenhuma chave antiga muda), "
                         "o registro com FUNCAO a_escala_v410 (a pedra AEscala: le do kernel do proprio rito as %d ancoras, as falas de 09/11 por sha256 e os nomes ratificados, recalcula os pesos das tres faces de 1/2 e confere a forma canonica do Clay, D84; validade no kernel, a creditacao e' do Clay), "
                         "o registro com FUNCAO h0dn_bg1_v410 (o teste da razao de Hubble local/fundo H0DN × BG1, %s: os insumos embutidos e pinados por sha256, K recomputado de beta em runtime, a funcao de veredito congelada, de %d ramos, em vetores deterministicos, observed_vector_read = False), o registro com FUNCAO h0dn_fontes_hms13_v410 (o recibo documental HMS/13, D80: aditivo e posterior ao FREEZE_R2; cobertura documental de fontes, nao covariancia fisica fechada; nada aberto) e os dois por spec (as %d falas de 06 a 09/11 por sha256, de %d delas so' o trecho; as decisoes %s; as erratas %s e a dos pisos; a cobertura KH-N1), "
                         "com os registros da v409 (traducao_turing_v409; cunhagens_v409; kh_n1_cobertura_v409 com a errata dos pisos ao lado), os da v408, da v407 (psion_canto_v407 com as cinco chaves iguais), da v406, da v405, da v404, da v403, da v402, da v401 e da v399, o selo pela propria tecnologia e o quadro do topo seguindo selados, o sidecar reescrito, a letra do veredito do gate igual a da v409 e nenhum veredito fora da troca dita mudado?") % (
                len(DL_.ANCORAS), FA["n_ancoras"], OBR, F["n_ramos"], len(verb), n_trecho, DEC, ERR),
            "dados": ["os modulos (as pedras em pedra\\ e insumos\\, com a candidata de origem e o recibo de compilacao de cada uma; o bundle pinado em BUNDLE_v410.json), pinados por sha256 (so' lidos), e a medida da cobertura (KH_N1_v410.json)",
                      "as %d falas de 06 a 09/11 por sha256 em insumos\\cunhagens (todas falas do operador; de %d delas so' o trecho: D65, a ordem da retomada, as tres copias do ACOM e a leitura do 5 sigma; a lista esta no registro cunhagens_v410 e na linhagem)" % (len(verb), n_trecho),
                      "os insumos do H0DN × BG1, pinados por sha256 e embutidos em base64 no um.py (%d arquivos; o FREEZE_R2 do desenho do Codex astra-bell, de 06/11, com %d pinos; a leitura da gerencia do dossie, sha16 %s; a ORDEM ao Kimi, sha16 %s): %s" % (F["n_insumos"], F["n_pinos_freeze"], F["dossie16"], F["ordem16"], OBR),
                      "os artefatos documentais do recibo HMS/13 (%d embutidos por sha256 no um.py, em insumos\\hms13_*; %s): lidos na construcao; em rito nenhum arquivo da entrega e' aberto" % (FH["n_embutidos"], DL_.FRASE_HMS13_OBRIGATORIA_PT),
                      "o kernel do rito (as ancoras, as bandeiras e a proveniencia), o proprio um.py, o core e o selo da rodada; nenhum dado novo foi aberto nesta rota; o desenho e o recibo dos nomes ficam citados so' por sha16 (D65)"],
            "metodo": "lake build + Audit no sandbox k410c (o modulo do bundle sobre o kernel da v409 selada); ensaio a seco do candidato; rito completo (os quatro registros com funcao: iald2_v410, a_escala_v410, h0dn_bg1_v410, este %s, e h0dn_fontes_hms13_v410); conferidor (deve mudar / nao pode mudar, com o quadro do topo conferido de novo contra o resultado pinado nas duas linguas e no .md, e os itens do selo mais o round trip do um.py instalado); " % OBR + (
                      "leitura da rodada (inclui o sidecar e a linha final do rito); superficies com a regra da linhagem completa (o MEMORY.md nao e' compactado: recusa por contagem); elo B(n) da Bancada (passo simples v409 -> v410, sem salto; recibos); a guarda das frases e a P18 em todo texto novo; o paragrafo novo e o do quadro e o sidecar, no handoff; os sete textos da custodia encadeados (D52) e o portao do G1, a D59 e a D65 sobre o handoff inteiro (S6d)"),
            "resultado": " | ".join(_vr410(v_) for v_ in [pc["verdict"], FA["verdict"], F["verdict"], FH["verdict"], cg["verdict"], kh["verdict"]]) + " | " + TH["resumo"] + " | (vereditos resumidos a 200 caracteres; a integra esta no core da rodada, um_absoluto.json) | sidecar %s (%s objetos, %s recusas) | %s | %s | escada %s -> %s (teoremas limpos %s/%s; %d bandeiras novas, %d da IALD2 e %d da AEscala; ancoras por modulo: %s)" % (
                sc["veredito"], sc["n_objetos"], sc["recusas"], resumo_conf, ("%s vereditos fora da troca dita mudaram (exigido 0)" % nvm) if nvm != "nao lido" else "vereditos fora da troca dita: nao lidos nesta leitura", esc0, esc1, ESP["escada"][0], ESP["escada"][1], NF, NF_I, NF_A, por_mod),
            "defeito": "as ressalvas, ditas: " + ress + "; o registro CONFERE o que o kernel prova e nao prova nada por si; o gate nao se moveu e a independencia das 4 bandeiras experimentais segue aberta (derivam de UM so' booleano) [DECLARADO, GV-01 e GV-03]; a pendencia [LEGAL] (D2) segue do operador; a revisao distinta do pacote e' o Sonnet (D69) e nao e' afirmada por este registro; " + TH["defeito"],
            "nao_refazer": "a integracao dos modulos e a escada %s -> %s estao medidas; as %d ancoras da IALD2 e as da AEscala no kernel do rito estao lidas e conferidas contra o um.py instalado; repetir os registros so' com kernel ou um.py novo; o algoritmo IALD e' relativo ao leitor (D64): a maquina de Turing padrao sem o leitor fica fora e nao e' caminho a reabrir sem termo novo; o desenho do teste H0DN × BG1 esta' congelado (FREEZE_R2): nao gerar semente nova, nao reescolher modelo nem limiar, nao recomputar o poder (%s)" % (esc0, esc1, len(DL_.ANCORAS), OBR),
            "proximo_passo": "os nomes das declaracoes ja' foram RATIFICADOS pelo operador em 09/11 (D74: " + _aspas_(DL_.FRASE_RATIFICO) + "); a igualdade completa com o leitor que so' conta (E28) e a independencia da pergunta da maquina sem leitor, [OPEN]; " + TH["proximo"] + "; o README pinado (D39) e o release do app, na custodia e na engenharia da casa (D68a); decisao [LEGAL] D2 com a agente de PI; custodia completa pela sessao de custodia (o handoff traz os paragrafos prontos do README e do site, os sete textos da custodia e lista o sidecar); revisao independente do pacote (o Sonnet, D69)",
            "onde": PK, "artefatos": arts, "refs": sorted((set(x["rota_id"] for x in T10) | set(REFS) | set(preparo_no_livro(ids))) - {NOVA}),
            "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move; as erratas %s (e a dos pisos ao lado) e as decisoes %s sao da gerencia c1, em nome proprio, ao lado (nada foi apagado nem reescrito); %s." % (ERR, DEC, sim(c_seguem, "os registros anteriores seguem selados", "ALGUM REGISTRO ANTERIOR NAO SELOU"))}
    for r in ROTA["refs"]:
        assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
    REG = [ROTA] + T10
    for x in REG:
        for k_, v_ in x.items():
            if isinstance(v_, str):
                assert len(v_) <= 6000, "o campo %s de %s passa de 6000 caracteres (limite do Mapa): resuma e aponte o artefato" % (k_, x["rota_id"])
    bad = [(x["rota_id"], violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad, "a guarda de texto (P18) achou violacao(oes): %r" % bad
    import guarda_frases_v410 as GF
    bad2 = [(x["rota_id"], GF.violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if GF.violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad2, "a guarda das frases achou violacao(oes): %r" % bad2
    atrib = [(x["rota_id"], T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))]
    assert not atrib, "a direcao do testemunho esta invertida ou a atribuicao falhou: %r" % atrib
    d59 = [x["rota_id"] for x in REG if d59_viola(json.dumps(x, ensure_ascii=False))]
    assert not d59, "D59: o registro traz o que fica fora dos textos (o Milenio, o Navier; o nome do Kimi so' no contexto do H0DN): %r" % d59
    d65 = [x["rota_id"] for x in REG if any(f_.lower() in json.dumps(x, ensure_ascii=False).lower() for f_ in DL_.FORA_D65)]
    assert not d65, "D65: o registro traz o que a fala do nome do algoritmo deixa fora: %r" % d65
    ruins = regra_4_44(REG, z, p)
    assert not ruins, "a regra do 4,44 (o p calibrado e a linha dos 5 sigma no mesmo campo) falhou em: %r" % ruins[:3]
    # --- D72: a obrigacao no MESMO registro, os tokens de veredito do H0DN e a aritmetica do agregado publico fora de todo texto do mapa
    j_ = {x["rota_id"] + "#" + x["tipo"]: json.dumps(x, ensure_ascii=False) for x in REG}
    h_sem = [k_ for k_, t_ in j_.items() if re.search(r"\bH0DN\b", t_) and DL_.FRASE_H0DN_OBRIGATORIA_PT not in t_]
    assert not h_sem, "D72: o registro diz H0DN sem a frase obrigatoria (pré-registrado; nenhum dado observado lido): %r" % h_sem
    hm_sem = [k_ for k_, t_ in j_.items() if re.search(r"HMS\s*/\s*13", t_) and DL_.FRASE_HMS13_OBRIGATORIA_PT not in t_]
    assert not hm_sem, "D80: o registro diz o recibo HMS/13 sem a frase obrigatoria (cobertura documental de fontes, nao covariancia fisica fechada; nada aberto): %r" % hm_sem
    def _campos_(o_):   # os textos (campos) do registro, um a um
        if isinstance(o_, str):
            yield o_
        elif isinstance(o_, dict):
            for v_ in o_.values():
                yield from _campos_(v_)
        elif isinstance(o_, (list, tuple)):
            for v_ in o_:
                yield from _campos_(v_)
    # (a regra e' LOCAL, como a F58 do runtime: a palavra do Clay e o verbo resolver no MESMO trecho, e o campo sem a forma canonica nem a da D83; o registro inteiro misturava a pergunta do Clay das ressalvas com o resolver = verificar da resposta do operador sobre P = nP)
    cl_sem = [x["rota_id"] + "#" + x["tipo"] for x in REG if any(re.search(r"\bClay\b", seg_) and re.search(r"resolv", seg_, re.I) and not any(f_ in c_ for f_ in (DL_.FRASE_CLAY_CANONICA_PT, DL_.FRASE_D83_OBRIGATORIA_PT)) for c_ in _campos_(x) for seg_ in re.split(r"[.;|\n]", c_))]
    assert not cl_sem, "D83/D84: o registro diz o Clay resolvido sem a forma canonica nem a da D83: %r" % cl_sem
    h_tok = [k_ for k_, t_ in j_.items() if any(tk_ in t_ for tk_ in DL_.TOKENS_PROIBIDOS_H0DN) or any(a_ in t_ for a_ in DL_.H0DN_AGREGADO_NAO_ENTRA)]
    assert not h_tok, "D72: o registro traz um token de veredito proibido do H0DN ou a aritmetica do agregado publico: %r" % h_tok
    assert DL_.FRASE_H0DN_OBRIGATORIA_PT in [x for x in REG if x["rota_id"] == R_H0DN][0]["titulo"], "D72: a anotacao do H0DN nao traz a obrigacao no proprio titulo"
    assert c_seguem and c_q, "algum registro anterior (quadro, v409, v408, v407, v406, v405, v404, v403, falsidade, ponte, queda, esperanca, selo, declaracao, sonico, afinacao, rede de Fock, psibit, testemunha estatica) nao selou no core: o mapa nao registra a v410 assim"
    return REG


def gravar(p, b):
    """backup de BYTES se existir e mudar; temporario -> conferir tamanho -> substituir."""
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m410"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_m410"; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def main():
    V, PROB = L.ler()
    if PROB:
        print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); return 2
    NOS = L.NOS
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v410_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v410_*.json")), key=os.path.getmtime)
    arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto_selo_acom.json"), os.path.join(PK, "ESPERADOS_v410.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v410.json"),
            os.path.join(PK, "DIFF_KERNEL_v410.txt"), os.path.join(PK, "DIFF_v409_v410.diff"), os.path.join(NOS, "HANDOFF_v410_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v410.json"),
            os.path.join(PK, "kernel", "KERNEL_RECIBO_v410.json"), os.path.join(PK, "LEITURA_DOSSIE_5SIGMA_09nov.json"), ORDEM_KIMI] + sorted(glob.glob(os.path.join(PK, "pedra", "*.lean"))) + b3[-1:]
    arts = [x for x in arts if os.path.exists(x)]
    REG = montar(V, core, selo, ids_do_livro(), arts)
    J = os.path.join(HERE, "registro_mapa_v410.json")
    gravar(J, json.dumps(REG, ensure_ascii=False, indent=1).encode("utf-8"))
    quem = "claude-c1 (gerência), cadeia v410"
    print("registro MONTADO (NAO registrado): %d registro(s) (%s) -> %s" % (len(REG), ", ".join(x["tipo"] for x in REG), J))
    print("COMANDO (o passo 12 da cadeia o executa, uma vez so): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
    print("DEPOIS DO REGISTRO: os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
