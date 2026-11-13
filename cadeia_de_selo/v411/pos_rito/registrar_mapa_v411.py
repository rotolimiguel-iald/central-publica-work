# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-sonnet-posrito-M-v411] REESCRITO para a v411 (DESENHO_v411 secoes 2, 4 e 5.3): a rota nova e' o TESTE H0DN x BG1 ABERTO e RECALCULADO NO RITO (registro h0dn_bg1_v411), sem modulo de kernel novo; os textos saem do core selado e do selo (fatos em consts_mapa_x_v411.py); a montagem nao registra nada
"""registrar_mapa_v411.py -- MONTA (nao registra) o registro da v411 no mapa de rotas e imprime o comando (molde: registrar_mapa_v410.py, que rodou na v410). Rodar DEPOIS do fechar (handoff gravado).
A v411 NAO traz modulo de kernel novo (o kernel e' o da v410 byte a byte; escada e gate iguais) e traz UM registro com FUNCAO, h0dn_bg1_v411 (16 checagens): a cada rito ele decodifica os insumos EMBUTIDOS do teste da razao de Hubble local/fundo
(H0DN x BG1), confere cada um contra os pinos de producao, executa dos bytes embutidos o codigo PUBLICADO antes da abertura e compara o recalculo com o resultado da abertura de 12/11/2026 (numeros a 1e-9; ramo, desfecho e cabeca por igualdade de texto);
mais os dois por spec (cunhagens_v411 e kh_n1_cobertura_v411). Os quatro registros com funcao da v410 (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410) sao recriados e seguem selados (nao sao novos); o h0dn_bg1_v410 (o pre-registro) NAO e' reescrito: a emenda e a abertura vao AO LADO.
UMA rota nova, umpy.v411.selada_h0dn_aberto_12nov, mais ANOTACOES nas rotas que esperavam por ela (o H0DN x BG1 com as DUAS linhas e as sete ressalvas; a publicacao da custodia, cuja ordem dos atos o rito confere; a v410, base; o gate; o B(n) da Bancada, B20; o quadro de 23/10).
REGRAS QUE ESTE SCRIPT CUMPRE (nada digitado; tudo lido do core, do selo, do livro e de delta_v411):
 (1) a REGRA DA OBRIGACAO (DESENHO secao 4, F67): todo CAMPO que traga o Z do primario contra o nulo, a cabeca do teste ou «provado na natureza» ligado a este teste traz, no MESMO campo, sob o modelo de erros publicado, a linha das Cefeidas livres com o numero dela,
     validade (nao creditacao), retrodicao e nao cego (a moldura de delta_v411 preenchida com os numeros do core); a guarda de frases da v411 e a P18 rodam sobre o registro inteiro, e o Mapa recusa a palavra da creditacao em titulo/resultado/veredito (aqui: «conferiu»);
 (2) a REGRA DO 4,44 (ordem do operador de 23/10): este registro NAO cita o numero do quadro de 23/10; se algum campo o trouxer, montar() RECUSA; (3) a D59 (o nome do executor so' no contexto do H0DN) e a D65; (4) a regra do nome (D122, D123): nenhuma identificacao do operador como leitura dele;
 (5) P = nP sempre relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora; (6) olhou_dados True so' na rota e na anotacao do H0DN (o rito RELE o vetor da abertura unica, seq lido do livro): e' o mesmo vetor recalculado, nao uma nova tentativa, e a nota o diz.
Fail-closed: o selo tem de ser a v411; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir; todo registro da v410 selada que tinha all_verified True segue True; o gate e a escada sao os da v410.
SAIDA: pos_rito\\registro_mapa_v411.json e o comando `rotas.py registrar` (quem o executa e' o passo 12 da cadeia, uma vez so, com marcador idempotente; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real. montar() le o core, o selo e ESPERADOS_v411.json (chaves usadas: candidato_sha16, origem_sha16,
escada_v410_e_v411, vereditos_novos_v411, e, se existirem, n_bandeiras_novas, chaves_v411 e qg_closure_gate_verdict_v410); de V so' usa o que a leitura da rodada ja' validou (s16, sidecar, conf_dm, conf_np, n_ver_mudaram), sempre com valor de reserva dito."""
import glob, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import delta_v411 as DL
import consts_mapa_x_v411 as C
from guarda_p18_v411 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V411"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v411 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOVA = "umpy.v411.selada_h0dn_aberto_12nov"
R_H0DN = "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov"                     # a rota do H0DN x BG1 (a ORDEM ao Kimi, o pre-registro, a abertura de 12/11 -- seq lido do livro)
R_PUBL = "infra.github.publicacao_fora_da_cadeia_h0dn_12nov"                # a publicacao da custodia (pre-registro antes da abertura; resultado depois)
R_V410 = "umpy.v410.selada_iald2_06nov"                                    # a v410 selada: a base da v411
R_GATE = "gate.qg_closure"
R_BANC = "infra.bancada_um.sincronizacao_vnnn"
R_QUADRO = "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9"
R_H0DN_COV = "estatistica.h0dn_bg1.cov_injecoes_06nov"                      # o desenho do Codex astra-bell (06/11)
R_PREP411 = "cadeia.preparacao_v411"                                       # a preparacao da v411 (12/11)
R_CUST410 = "custodia.v410"                                                # a custodia da v410
R_G1P18 = "infra.custodia_g1.cabeca_h0dn_p18_12nov"                         # a cabeca do H0DN diante do portao da G1 e da P18
R_AESCALA = "kernel.a_escala_tres_faces_v410_09nov"                         # a pedra AEscala (E43: as seis aberturas da secao da Escala, ao lado)
ANOTADAS = (R_H0DN, R_PUBL, R_V410, R_GATE, R_BANC, R_QUADRO)
REFS = (R_H0DN_COV, R_PREP411, R_CUST410, R_G1P18, R_AESCALA)
_CACHE = {}


def _esp():
    """ESPERADOS_v411.json (lido uma vez por processo)."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v411.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _base_core():
    """O core da v410 selada (a copia de bytes em base_v410): de onde sai a medida de que o gate, a escada e os registros anteriores nao se moveram."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v410", "um_absoluto.json"), encoding="utf-8"))["core"]
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
    """O seq (unico) do registro a que o texto novo se refere, LIDO do livro; recusa se nao houver exatamente um ou se o registro nao trouxer o trecho que o texto diz que ele traz."""
    c = [r for r in regs if r.get("rota_id") == rota_id and r.get("tipo") == tipo and (inicio_do_titulo is None or str(r.get("titulo", "")).startswith(inicio_do_titulo))]
    assert len(c) == 1, "esperava exatamente um registro %s de %s (inicio do titulo %r) e achei %d" % (tipo, rota_id, inicio_do_titulo, len(c))
    txt = json.dumps(c[0], ensure_ascii=False)
    for s in contem:
        assert s in txt, "o registro seq %s de %s nao traz %r: o texto novo nao se refere ao que diz" % (c[0]["seq"], rota_id, s)
    return c[0]["seq"]


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
    p = json.load(open(os.path.join(PK, "PINOS_BN_v411.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v410" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v410 -> v411 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1, "deployment_id": bp["deployment_id"]}


_RX_D59 = re.compile(r"(?i)mil[eê]nio|millennium|navier|lindão")


def d59_viola(txt):
    """D59 (v410) com a UNICA excecao que a D72 abre: o Milenio, o Navier e o resto do que a D59 deixa fora seguem proibidos em qualquer texto; o nome do Kimi so' pode aparecer no contexto do H0DN (a ORDEM ao Kimi e a rota dela). Devolve True se violar."""
    t = str(txt)
    return bool(_RX_D59.search(t)) or bool(re.search(r"(?i)kimi", t) and not re.search(r"(?i)h0dn", t))


def selou(core, k):
    return (core.get(k) or {}).get("all_verified") is True


def h0dn_do_core(DL_, hd, ESP, base_core):
    """Confere o registro h0dn_bg1_v411 do core (FAIL-CLOSED: registro ausente, nao selado, chave congelada que falta, veredito de maquina que nao bate com os numeros, checagem que falha, n_checks != DL.N_CHECKS_FECHO, veredito diferente do de ESPERADOS,
    gate ou escada diferentes da v410, o h0dn_bg1_v410 (pre-registro) tocado => AssertionError visivel) e devolve os FATOS que o mapa cita, todos LIDOS (nada digitado)."""
    F = C.fatos_h0dn(hd)
    hv, hm = hd.get("values") or {}, hd.get("mechanics") or {}
    ev = (ESP.get("vereditos_novos_v411") or {}).get(DL_.FECHO_REGISTRO)
    assert ev and ev == hd.get("verdict"), "ESPERADOS_v411.json nao traz vereditos_novos_v411[%s] igual ao veredito do registro do core (o gerar_esperados_v411 deve emiti-lo)" % DL_.FECHO_REGISTRO
    assert hm.get("passed") is True and hm.get("n_checks") == DL_.N_CHECKS_FECHO == len(hm.get("checks") or []) and all(c_.get("ok") is True for c_ in hm["checks"]), "as %d checagens do h0dn_bg1_v411 nao passaram todas" % DL_.N_CHECKS_FECHO
    assert hd.get("beta_ok") is True, "h0dn_bg1_v411: beta_ok nao e' True (beta so' por nome, em runtime)"
    gb = ((base_core.get("qg_closure") or {}).get("gate") or {}).get("verdict")
    assert gb and hv.get("gate_verdict") == gb, "h0dn_bg1_v411: o gate lido != o da v410 selada (deveria estar congelado)"
    eb = (base_core.get("external_ladder") or {}).get("n_theorems_expected")
    assert eb and hv.get("escada") == eb, "h0dn_bg1_v411: a escada lida != a da v410 selada (a v411 nao tem modulo novo)"
    assert not (hv.get("p18_violacoes") or []) and not (hv.get("frases_violacoes") or []) and not (hv.get("tokens_no_texto") or []) and not (hv.get("sob_pasta_vedada") or []), "h0dn_bg1_v411: as guardas de texto ou a pasta vedada do Kimi acusaram algo"
    antigo = DL_.D10.H0DN_REGISTRO
    return dict(F, n_checks=hm["n_checks"], antigo=antigo, antigo_verdict_base=(base_core.get(antigo) or {}).get("verdict"))


def _lei_pt(F):
    L_ = F.get("lei")
    ks = ("H0_fundo", "previsao_de_K_para_o_local", "lido_primario", "lido_cefeidas_livres", "publicado_pela_colaboracao", "desvio_publicado")
    if not L_ or not all(isinstance(L_.get(k_), (int, float)) for k_ in ks):
        return ""
    k_ = ("K = %s; " % C.pt(F["K"], 4)) if F.get("K") is not None else ""
    return ("A lei K = E(z*)^(2β/3), com β = α·√e em runtime (nunca literal) e zero parâmetro livre: %sem km/s/Mpc o fundo dá %s, a previsão de K para o local é %s, o primário lê %s, as %s leem %s e a colaboração publica %s ± %s. " % (
        k_, C.pt(L_["H0_fundo"]), C.pt(L_["previsao_de_K_para_o_local"]), C.pt(L_["lido_primario"]), DL.OBRIG_CEFEIDAS_PT, C.pt(L_["lido_cefeidas_livres"]), C.pt(L_["publicado_pela_colaboracao"]), C.pt(L_["desvio_publicado"])))


def _atos_pt(F):
    a_ = F["atos"]
    return ("Os atos, lidos dos recibos embutidos (c3): push do pré-registro %s (commit %s), início da abertura %s, push do resultado %s (commit %s); a ordem é push do pré-registro < início da abertura < push do resultado, e o commit do pré-voo é o do pré-registro. " % (
        a_["push_do_pre_registro_utc"], a_["commit_do_pre_registro"][:12], a_["inicio_da_abertura_utc"], a_["push_do_resultado_utc"], a_["commit_do_resultado"][:12]))


def _agregados_pt(F):
    if not F.get("agregados"):
        return ""
    itens = []
    for x_ in F["agregados"]:
        if all(isinstance(x_.get(k_), (int, float)) for k_ in ("z_nulo_esperado", "z_nulo_observado")) and isinstance(x_.get("linha"), str):
            itens.append("%s: Z contra o nulo esperado %s, observado %s" % (x_["linha"], C.pt(x_["z_nulo_esperado"]), C.pt(x_["z_nulo_observado"])))
    return ("O esperado pelos agregados públicos, ao lado do observado (relato, não portão; retrodição sem ajuste): %s. " % "; ".join(itens)) if itens else ""


def h0dn_textos(DL_, F, ctx):
    """Os textos do H0DN para o mapa, MONTADOS dos fatos F (h0dn_do_core) e do contexto ctx (S, seq lidos do livro, sha16 lidos dos arquivos); so' os conectivos sao escritos aqui. Devolve {titulo, resultado, defeito, proximo, naorefazer, estatuto}.
    Todo campo que traz o numero do primario traz, no MESMO campo, a moldura inteira (F67) ou a cauda das obrigacoes."""
    M = C.moldura_pt(F); cauda = C.cauda_pt(F); S = ctx["S"]
    c6 = F.get("c6_max_dif")
    c6t = (" (a maior diferença do recálculo contra o resultado da abertura é %g, com tolerância %g)" % (max(abs(float(v_)) for v_ in c6.values()), DL_.TOL_RECALCULO)) if c6 else ""
    titulo = "v411 SELADA %s: o teste H0DN × BG1 aberto em 12/11/2026 foi recalculado no rito dos bytes embutidos e conferiu contra o resultado da abertura (registro h0dn_bg1_v411, %d checagens); %s" % (S, F["n_checks"], M)
    resultado = ("[REAL, lido do core do rito] o registro com FUNÇÃO h0dn_bg1_v411 (o único novo com função na v411) selou: %d checagens ok. O resultado da abertura (RESULTADO do seq %d deste livro; sha16 %s) foi RECALCULADO a cada rito dos bytes embutidos (o código publicado antes da abertura, compile + exec em módulos isolados; nada transcrito) e conferiu%s. "
                 "%s. Primário (modelo de erros publicado): Z contra o nulo %s, Z contra K %s, D de desenho %s, p unilateral %s, ramo %d, desfecho %s (a palavra do livro de cobranças: vai no campo outcome do registro, nunca na cabeça do teste). "
                 "Linha ao lado, no mesmo item (%s): Z contra o nulo %s, Z contra K %s, D %s, ramo %d. %s%s%s") % (
        F["n_checks"], ctx["sq_abertura"], ctx["res16"], c6t, C.cap(M), F["zn4_pt"], F["zk4_pt"], F["D4_pt"], F["p_pt"], F["ramo_p"], F["outcome"], DL_.OBRIG_CEFEIDAS_PT, F["cn4_pt"], F["ck4_pt"], F["Dc4_pt"], F["ramo_c"], _lei_pt(F), _atos_pt(F), _agregados_pt(F))
    defeito = ("[as sete ressalvas, lidas do registro: seção 8 do pré-registro embutido] %s. O que o teste não decide (seção 6): %s. A creditação é de quem observa de fora; o um.py não a dá. "
               "[OPEN] se o orçamento de erros publicado está certo; a independência entre a medida local e o fundo é hipótese nomeada; a covariância física conjunta segue aberta (o recibo HMS/13 da v410 é cobertura de fontes). "
               "[DECLARADO pelo Kimi] as três linhas de covariância S1, S2 e S4 entram só como texto do pré-registro, sem número observado; nada da pasta do Kimi é lido em rito. Em resumo: %s.") % (C.ressalvas_pt(F), "; ".join(F["nao_decide"]), cauda)
    proximo = ("a creditação é de quem observa de fora (o um.py não a dá); a custódia da v411 (README, site e X) é da sessão de custódia: o HANDOFF traz os blocos prontos (DESENHO_v411 5.3); dado mais sensível pode rever o que foi lido (a letra do veredito do gate diz MORE_SENSITIVE_DATA_COULD_REVISE); "
               "a pedra do observador e da escala e as doze candidatas de 11/11 ficam para a versão seguinte, à espera dos nomes do operador; o gate não se move. Em resumo: %s.") % cauda
    naorefazer = ("a abertura é uma só (12/11/2026, depois do commit público do pré-registro): não se roda de novo o executor, não se escolhe outro vetor, outro modelo, outro limiar nem outra marca, e o recálculo do rito é conferência da conta, não é nova tentativa; "
                  "o desenho e o texto final do pré-registro (sha16 %s) estão congelados e embutidos como bytes; as emendas posteriores à guarda ficam ditas nas ressalvas, não se escondem; o primário nunca sai sem a linha das Cefeidas livres no mesmo item") % ctx["prereg16"]
    estatuto = ("REAL (o recálculo no rito dos bytes embutidos e a conferência contra o resultado da abertura; as %d checagens; a ordem dos atos lida dos recibos; os números, lidos do core); INPUT (a cabeça do veredito, fixada pelo operador em 09/11, e a emenda de 11/11, as falas dele por sha256); "
                "DECLARADO (as três linhas de covariância do Kimi, só como texto do pré-registro); OPEN (se o orçamento de erros publicado está certo; a independência entre local e fundo; a covariância física conjunta)") % F["n_checks"]
    return {"titulo": titulo, "resultado": resultado, "defeito": defeito, "proximo": proximo, "naorefazer": naorefazer, "estatuto": estatuto}


def montar(V, core, selo, ids, arts):
    """Monta os registros (a ROTA nova e as ANOTACOES), cada afirmacao testada contra o core/selo/ESPERADOS; devolve a lista; recusa (assert) se algo nao conferir. Nao escreve nada."""
    assert selo.get("um_version") == "v411", "o selo nao e a v411"
    assert NOVA not in ids, "a rota %s ja existe no mapa" % NOVA
    for r in ANOTADAS + REFS:
        assert r in ids, "a rota %s nao existe no mapa (anotada ou citada em refs)" % r
    ESP = _esp(); DL_ = DL; bc = _base_core()
    S = ESP["candidato_sha16"]
    assert str((selo.get("sha256") or {}).get("um.py", ""))[:16] == S, "o um.py do selo nao e o candidato de ESPERADOS"
    assert V.get("s16") in (None, S), "o s16 da leitura != o candidato de ESPERADOS"
    BASE = ESP["origem_sha16"]
    assert BASE == DL_.BASE_SHA16_DA_ORDEM, "a base de ESPERADOS (%s) != a v410 selada da ordem (%s)" % (BASE, DL_.BASE_SHA16_DA_ORDEM)
    esc0, esc1 = ESP["escada_v410_e_v411"]
    el = core.get("external_ladder") or {}; eb = (bc.get("external_ladder") or {}).get("n_theorems_expected")
    assert esc0 == esc1 == eb == el.get("n_theorems_expected") == el.get("n_theorems_clean"), "a escada nao e' a da v410 (a v411 nao tem modulo novo): %r %r %r" % (ESP["escada_v410_e_v411"], eb, el)
    assert int(ESP.get("n_bandeiras_novas", 0) or 0) == 0 and list(ESP.get("chaves_v411") or []) == [], "a v411 nao tem bandeira nova nem chave antiga que mude: ESPERADOS diz outra coisa"
    # --- o gate NAO se moveu: o registro segue selado e a letra do veredito e' a da v410
    gk = core.get("bandeiras_do_gate_v403") or {}; gvv = gk.get("values") or {}; gb = bc.get("bandeiras_do_gate_v403") or {}
    assert gk.get("all_verified") is True and (V.get("gate") or {}).get("sealed", True) is True and gvv == gb.get("values") and (gk.get("mechanics") or {}).get("passed") is True, "bandeiras_do_gate_v403 (recriado) nao selou ou != a v410 selada"
    qg = core.get("qg_closure") or {}; fam = [len(qg.get(f) or {}) for f in ("formal_flags", "physics_flags", "experiment_flags")]
    gate_base = ((bc.get("qg_closure") or {}).get("gate") or {}).get("verdict")
    assert gate_base and (qg.get("gate") or {}).get("verdict") == gate_base == selo.get("qg_closure_verdict"), "a letra do veredito do gate mudou"
    if ESP.get("qg_closure_gate_verdict_v410") is not None:
        assert ESP["qg_closure_gate_verdict_v410"] == gate_base, "ESPERADOS traz um gate da v410 diferente do da v410 selada"
    # --- o registro com FUNCAO h0dn_bg1_v411: tudo lido do core e conferido contra ESPERADOS, o delta e a v410 selada
    F = h0dn_do_core(DL_, core.get(DL_.FECHO_REGISTRO), ESP, bc)
    # --- os registros da v410 selada: cada um que tinha all_verified True segue True (recriados pelo rito); os quatro com funcao da v410 dizem-se um a um
    sem_selo = sorted(k_ for k_, v_ in bc.items() if isinstance(v_, dict) and v_.get("all_verified") is True and (core.get(k_) or {}).get("all_verified") is not True)
    assert not sem_selo, "registros selados na v410 que nao selam na v411 (ou sumiram do core): %s (%d)" % (sem_selo[:5], len(sem_selo))
    n_selados_v410 = sum(1 for v_ in bc.values() if isinstance(v_, dict) and v_.get("all_verified") is True)
    n_seguem = sum(1 for k_, v_ in bc.items() if isinstance(v_, dict) and v_.get("all_verified") is True and selou(core, k_))
    for k_ in DL_.REGISTROS_FUNCAO_V410:
        assert (core.get(k_) or {}).get("all_verified") is True and (bc.get(k_) or {}).get("all_verified") is True, "o registro com funcao da v410 %s nao segue selado na v411" % k_
    n_iguais = sum(1 for k_ in DL_.REGISTROS_FUNCAO_V410 if (core.get(k_) or {}).get("verdict") == (bc.get(k_) or {}).get("verdict"))
    assert (core.get(DL_.D10.H0DN_REGISTRO) or {}).get("verdict") == F["antigo_verdict_base"], "o pre-registro h0dn_bg1_v410 foi reescrito: o veredito dele difere do da v410 selada (a emenda vai AO LADO, no registro novo)"
    # --- os dois registros por spec
    cg = core.get(DL_.CUNHAGENS_REGISTRO) or {}; kh = core.get(DL_.KH_REGISTRO) or {}
    for nome_, r_ in ((DL_.CUNHAGENS_REGISTRO, cg), (DL_.KH_REGISTRO, kh)):
        assert r_.get("all_verified") is True and r_.get("verdict") and r_.get("verdict") == (ESP.get("vereditos_novos_v411") or {}).get(nome_), "%s nao selou ou != ESPERADOS" % nome_
    verb = cg.get("verbatim") or {}; ex = cg.get("extras") or {}
    assert len(verb) == DL_.N_FALAS_V411 and all(v_.get("citado_por_sha256") is True and v_.get("texto_transcrito") is False and re.fullmatch(r"[0-9a-f]{64}", str(v_.get("sha256"))) for v_ in verb.values()), "as %d falas de 11 e 12/11 nao estao CITADAS por data e sha256 (D181) no cunhagens_v411" % DL_.N_FALAS_V411
    erratas = cg.get("erratas") or []
    assert [str(e_.get("agora")) for e_ in erratas[:len(DL_.ERRATAS_V411)]] == [e_["texto"] for e_ in DL_.ERRATAS_V411] and len(erratas) == len(DL_.ERRATAS_V411) + 1 and all(e_.get("assinatura") == DL_.ASSINA for e_ in erratas), "as erratas E41 a E44 (e a dos pisos de kh_n1_cobertura_v410) nao estao no cunhagens_v411, ou nao sao da gerencia c1 em nome proprio"
    assert sorted(ex.get("decisoes") or {}) == sorted(DL_.DECISOES_V411), "as decisoes do delta nao estao no cunhagens_v411"
    cob = kh.get("lido") or {}; assert cob.get("constantes_cobertas") and cob.get("teoremas_cobertos"), "kh_n1_cobertura_v411 sem a cobertura"
    sc = _sidecar(V); conf_dm = V.get("conf_dm", "nao lido"); conf_np = V.get("conf_np", "nao lido"); nvm = V.get("n_ver_mudaram", "nao lido")
    bank = _bancada(); regs = livro()
    # --- os seq que o texto novo cita, LIDOS do livro (e o registro tem de trazer o que o texto diz que ele traz)
    sq_ab = seq_do_alvo(regs, R_H0DN, "RESULTADO", inicio_do_titulo="H0DN x BG1 (12/11): ABERTURA", contem=("Cefeidas livres",))
    sq_pre = seq_do_alvo(regs, R_H0DN, "ANOTACAO", inicio_do_titulo="H0DN x BG1 (12/11): marca ratificada", contem=("literal dos vereditos",))
    sq_pub = seq_do_alvo(regs, R_PUBL, "RESULTADO", contem=("f24d954a3b90",))
    sq_prep = seq_do_alvo(regs, R_PREP411, "ROTA")
    res16 = DL_.INSUMO_POR_NOME["RESULTADO_DA_ABERTURA_V411.json"]["sha256"][:16]; pre16 = DL_.INSUMO_POR_NOME["EMENDA_E_PRE_REGISTRO_V411.md"]["sha256"][:16]; ram16 = DL_.INSUMO_POR_NOME["RAMOS_V411.json"]["sha256"][:16]
    vet16 = DL_.INSUMO_POR_NOME["vetor_y255.npz"]["sha256"][:16]
    ctx = {"S": S, "sq_abertura": sq_ab, "res16": res16, "prereg16": pre16}
    TH = h0dn_textos(DL_, F, ctx); M = C.moldura_pt(F); cauda = C.cauda_pt(F)
    KR = os.path.join(PK, "kernel", "KERNEL_RECIBO_v411.json")
    ins_arq = [i_["arquivo"] for i_ in DL_.INSUMOS_V411]
    ERR = ", ".join(e_["id"] for e_ in DL_.ERRATAS_V411); DEC = "%s a %s" % (min(DL_.DECISOES_V411), max(DL_.DECISOES_V411))

    def anot(rota_id, titulo, resultado, proximo, refs=None, nota=None, estatuto="REAL", artefatos=None, defeito=None, olhou=False):
        x = {"tipo": "ANOTACAO", "rota_id": rota_id, "estatuto": estatuto, "olhou_dados": olhou, "titulo": titulo, "resultado": resultado, "proximo_passo": proximo, "refs": [NOVA] + (refs or [])}
        if defeito:
            x["defeito"] = defeito
        if nota:
            x["nota"] = nota
        if artefatos:
            x["artefatos"] = _existentes(*artefatos)
        return x

    T11 = []
    T11.append(anot(R_H0DN, TH["titulo"], TH["resultado"], TH["proximo"], refs=[R_H0DN_COV, R_PUBL, R_PREP411, R_G1P18], estatuto=TH["estatuto"], defeito=TH["defeito"], olhou=True,
                    nota="olhou_dados True porque o rito RELÊ o vetor da abertura única (RESULTADO do seq %d, também olhou_dados True): é o mesmo vetor, recalculado dos bytes embutidos, não uma nova tentativa e não soma escolha alguma; %s" % (sq_ab, TH["naorefazer"]),
                    artefatos=[DL_.INSUMO_POR_NOME[n_]["arquivo"] for n_ in ("RESULTADO_DA_ABERTURA_V411.json", "EMENDA_E_PRE_REGISTRO_V411.md", "RAMOS_V411.json", "PINOS_DE_PRODUCAO.json", "PRE_VOO_DA_ABERTURA_V411.json", "RECIBO_DA_ABERTURA_V411.json", "ESPERADO_PELOS_AGREGADOS.json")] + [KR]))
    a_ = F["atos"]
    T11.append(anot(R_PUBL, "v411 SELADA %s: o rito conferiu a ordem dos atos da publicação, lida dos recibos embutidos: push do pré-registro, depois início da abertura, depois push do resultado" % S,
                    ("[REAL, lido do core do rito; o conteúdo dos recibos é DECLARADO pela custódia] o registro h0dn_bg1_v411 lê, dos dois recibos de publicação embutidos por sha256, que o push do pré-registro (%s, commit %s) precede o início da abertura (%s) e que o push do resultado (%s, commit %s) a segue; "
                     "o commit do pré-voo (%s) é o do recibo da custódia%s; a abertura teve código 0 e a saída do executor tem o sha256 do resultado embutido. Repositório: %s. Os seq deste livro: a publicação do pré-registro é a ROTA seq %d e a do resultado é o RESULTADO seq %d.") % (
                        a_["push_do_pre_registro_utc"], a_["commit_do_pre_registro"][:12], a_["inicio_da_abertura_utc"], a_["push_do_resultado_utc"], a_["commit_do_resultado"][:12], a_["commit_do_pre_voo"][:12],
                        (" e os %d arquivos pinados do pré-voo conferem" % F["n_pre_voo"]) if F.get("n_pre_voo") else "", a_["repositorio"], seq_do_alvo(regs, R_PUBL, "ROTA"), sq_pub),
                    "a custódia da v411 publica o que a gerência mandar; o que o teste não decide e as sete ressalvas seguem ditos no registro h0dn_bg1_v411 e no H0DN × BG1 da rota própria.", refs=[R_H0DN, R_CUST410],
                    estatuto="REAL (a ordem dos atos lida dos recibos embutidos, conferida a cada rito); DECLARADO (o conteúdo dos recibos, pela custódia)", artefatos=[DL_.INSUMO_POR_NOME[n_]["arquivo"] for n_ in ("RECIBO_PUBLICACAO_20261112_074508.json", "RECIBO_PUBLICACAO_RESULTADO_20261112_075315.json", "RECIBO_DA_ABERTURA_V411.json", "PRE_VOO_DA_ABERTURA_V411.json")]))
    T11.append(anot(R_V410, "v411 SELADA %s: a v410 é a base da v411; a v411 não traz módulo de kernel novo; os QUATRO registros com função da v410 (%s) são recriados e seguem selados, e o pré-registro h0dn_bg1_v410 não é reescrito: a emenda e a abertura vão AO LADO, no registro novo h0dn_bg1_v411" % (S, ", ".join(DL_.REGISTROS_FUNCAO_V410)),
                    ("a v411 parte da v410 selada (um.py %s) e acrescenta UM registro com função (h0dn_bg1_v411; selou=%s) e dois por spec (cunhagens_v411; kh_n1_cobertura_v411; selaram=%s e %s), sem módulo de kernel novo: o kernel é o da v410 (KERNEL_RECIBO_v411: nenhuma pedra, rc 0, escada %s = a da v410, nenhuma bandeira nova). "
                     "Dos %d registros da v410 selada com all_verified True, os %d seguem True no core da v411 (recriados pelo rito); dos quatro com função da v410, %d têm o veredito idêntico ao da v410. O registro h0dn_bg1_v410 (pré-registro, função congelada de seis ramos) segue como foi selado, com o texto da data dele (a v411 o supera ao lado, não o reescreve). "
                     "As erratas %s e as decisões %s são da gerência c1, em nome próprio, ao lado; o sidecar um_absoluto_selo_acom.json %s (%s objetos, %s recusas, sha16 %s). Nenhuma chave antiga muda.") % (
                        BASE, selou(core, DL_.FECHO_REGISTRO), selou(core, DL_.CUNHAGENS_REGISTRO), selou(core, DL_.KH_REGISTRO), esc1, n_selados_v410, n_seguem, n_iguais, ERR, DEC, sc["veredito"], sc["n_objetos"], sc["recusas"], sc["sha16"]),
                    "custódia completa pela sessão de custódia (o fim da cadeia do orquestrador é o HANDOFF; o handoff lista o sidecar e diz quais contratos novos são de registro, fora da escada).", refs=[R_CUST410, R_AESCALA, R_PREP411],
                    estatuto="REAL (a leitura do core do rito contra o core da v410 selada); INPUT (a ordem do operador de 12/11)"))
    T11.append(anot(R_GATE, "v411 SELADA %s: o gate NÃO se moveu — o qg_closure do core é idêntico ao da v410 (as 18 bandeiras calculadas, a letra do veredito) e o resultado do teste H0DN × BG1 não move bandeira alguma" % S,
                    (f"o registro bandeiras_do_gate_v403 (recriado) selou={selou(core, 'bandeiras_do_gate_v403')} com os mesmos valores da v410 selada: das {gvv['n_flags']} bandeiras ({fam[0]} formais, {fam[1]} físicas, {fam[2]} experimentais) {gvv['n_true']} são True e {gvv['n_calculated']} são CALCULADAS ({gvv['n_literal']} literais); o veredito lê {gvv['n_read_by_the_verdict']}; "
                     "a letra do veredito do gate é a da v410 e a do selo; o registro h0dn_bg1_v411 lê gate_verdict idêntico ao da v410 e does_not_gate_core = True: cosmologia não move o gate, e este teste também não. "
                     "A letra do próprio veredito diz que dado mais sensível pode rever o que foi lido (MORE_SENSITIVE_DATA_COULD_REVISE). [DECLARADO, GV-03 da auditoria de 28/09/2026] As 4 bandeiras experimentais derivam de UM só booleano; o degrau experimental lê só o rito V11 do piso, unilateral (GV-01)."),
                    "a independência das 4 experimentais e os mocks de survey seguem [OPEN]; o gate não se move por esta rota.", refs=None,
                    artefatos=[os.path.join(PK, "CANDIDATO_v411.json")], estatuto="REAL (o core do rito); DECLARADO (GV-01, GV-03, EV-12 da auditoria de 28/09/2026); OPEN (a independência das 4 experimentais)",
                    defeito="o gate não é teste e não discrimina o ΛCDM raso; NOT_FALSIFIED nunca é a palavra da creditação"))
    T11.append(anot(R_BANC, "v411 SELADA %s: o B(n) da v411 é um passo SIMPLES v410 -> v411 (a Bancada de produção já pinava a v410), rótulo B%d" % (S, bank["proxima"]),
                    (f"o kernel da v411 é o da v410, sem módulo novo (KERNEL_RECIBO_v411: nenhuma pedra, rc 0); o recibo pre_selo foi gerado e pinado ANTES da instalação, em ensaio contra a produção (nada gravado; a Bancada pinava {bank['deployment_id']}), "
                     f"e a cadeia confere os pinos de PINOS_BN_v411.json na hora; o veredito esperado do aplicar é REPINADA_B{bank['proxima']}__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_ e sem cadeia de selos, lido do código do esboço R3.5. Parada e religamento do serviço exigem V411_AUTORIZACAO_OPERADOR (texto sem o nome do script do serviço)."),
                    "depois do aplicar, a Bancada pina a v411.", refs=None, artefatos=[os.path.join(PK, "PINOS_BN_v411.json"), os.path.join(PK, "PINO_RECIBO_PRE_SELO_v411.json"), KR]))
    T11.append(anot(R_QUADRO, "v411 SELADA %s: o quadro «O Teste da Única Palavra» (23/10) segue como registro e o registro teste_de_veracidade_fase9_v397 segue selado; um quadro novo, o do H0DN × BG1, vai ACIMA dele" % S,
                    f"teste_de_veracidade_fase9_v397 selou={selou(core, 'teste_de_veracidade_fase9_v397')} e cunhagens_v397 selou={selou(core, 'cunhagens_v397')} neste rito (os dois seguem selados, como todo registro da v410 selada com all_verified True). O DESENHO_v411 (5.1) manda pôr o quadro novo ACIMA do de 23/10 e acrescentar a este uma linha que remete ao novo (ordem do operador de 12/11). "
                    "Este registro não cita o número do quadro de 23/10: a regra da ordem do operador (nunca o número sem o p calibrado e sem a linha dos 5 sigma no mesmo campo) vale em todo texto que o cite.",
                    "o quadro novo e a linha que remete a ele são do artigo, do .md e do handoff da v411; a creditação segue sendo de quem observa de fora.", refs=None))
    for x in T11:
        assert x["rota_id"] in ids, "a rota %s nao existe no mapa" % x["rota_id"]
    resumo_conf = ("conferidor %s e %s" % (conf_dm, conf_np)) if "nao lido" not in (conf_dm, conf_np) else "conferidor: o resultado nao veio na leitura desta rodada"
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": True,
            "titulo": "v411 SELADA %s: o teste H0DN × BG1 aberto em 12/11/2026, recalculado no rito dos bytes embutidos e conferido contra o resultado da abertura (registro h0dn_bg1_v411, %d checagens); %s; escada %s = a da v410, sem módulo de kernel novo" % (S, F["n_checks"], M, esc1),
            "pergunta": ("a v411 (sem módulo de kernel novo) sela a emenda e o resultado da abertura do teste pré-registrado da razão de Hubble local/fundo (H0DN × BG1), recalculando-o a cada rito dos bytes embutidos e conferindo-o contra o resultado da abertura, "
                         "com os quatro registros com função da v410 recriados e selados, os dois por spec (as %d falas de 11 e 12/11 citadas por data e sha256, não transcritas; as decisões %s; as erratas %s; a cobertura KH-N1), o gate e a escada iguais aos da v410 e nenhum veredito fora da troca dita mudado?") % (DL_.N_FALAS_V411, DEC, ERR),
            "dados": ["o um.py da v411 (candidato %s; selo, core e sidecar da rodada; ESPERADOS_v411.json), só leitura; a base é a v410 selada (um.py %s, cópia de bytes em base_v410)" % (S, BASE),
                      "os insumos do teste H0DN × BG1, embutidos no um.py em base64 e pinados por sha256 (%d arquivos; o estimador congelado e o fundo BG1 são de reuso da v410, sem duplicar): a rede, o estimador S0, o literal dos vereditos (sha16 %s), o pré-registro final (sha16 %s), o vetor (sha16 %s), os três módulos de código (estimador, veredito, abertura), os pinos de produção, o resultado da abertura (sha16 %s), o pré-voo, o recibo da abertura, o esperado pelos agregados e os dois recibos da publicação da custódia" % (len(DL_.INSUMOS_V411), ram16, pre16, vet16, res16),
                      "citados por sha256, não embutidos: %d arquivos (o executor da abertura, o diff do veredito da v410 para a v411, os pinos, os manifestos da publicação, o desenho ratificado e o achado da gerência sobre o suporte)" % len(DL_.CITADOS_V411),
                      "as %d ordens e ratificações do operador de 11 e 12/11, citadas por data e sha256 e não transcritas (todas dele; os textos da gerência a que ele respondeu entram só citados por sha256)" % DL_.N_FALAS_V411,
                      "o kernel do rito (o da v410, sem módulo novo), o core e o selo da rodada; nenhum dado novo foi aberto nesta rota: a abertura foi uma só, em 12/11/2026 (RESULTADO do seq %d), e o rito recalcula o mesmo vetor" % sq_ab],
            "metodo": ("lake build incremental (nenhum módulo compilado) + Audit no sandbox k411c (a escada e as declarações são as da v410); ensaio a seco do candidato; rito completo (o registro h0dn_bg1_v411: os três módulos pinados executados dos bytes embutidos, compile + exec em módulos isolados, o recálculo comparado ao resultado da abertura, "
                       "as %d checagens; os quatro registros com função da v410 recriados); conferidor (deve mudar / não pode mudar); leitura da rodada (inclui o sidecar e a linha final do rito); superfícies com a regra da linhagem completa; elo B(n) da Bancada (passo simples v410 -> v411, sem salto); "
                       "a guarda das frases e a P18 em todo texto novo (a moldura com os dois números no mesmo campo); o HANDOFF com os blocos prontos do README, do site e do X (sem S7 e sem S10 no orquestrador); a D59 e a D65 sobre o handoff inteiro (S6d)") % F["n_checks"],
            "resultado": ("%s | sidecar %s (%s objetos, %s recusas) | %s | %s | escada %s = a da v410; nenhuma bandeira nova; nenhum módulo novo; %d de %d registros da v410 selada seguem selados | o teste H0DN × BG1: %s. Primário: Z contra o nulo %s, Z contra K %s, ramo %d, desfecho %s; linha ao lado (%s): Z contra o nulo %s, Z contra K %s, ramo %d.") % (
                F["verdict"], sc["veredito"], sc["n_objetos"], sc["recusas"], resumo_conf, ("%s vereditos fora da troca dita mudaram (exigido 0)" % nvm) if nvm != "nao lido" else "vereditos fora da troca dita: nao lidos nesta leitura", esc1, n_seguem, n_selados_v410, M, F["zn4_pt"], F["zk4_pt"], F["ramo_p"], F["outcome"], DL_.OBRIG_CEFEIDAS_PT, F["cn4_pt"], F["ck4_pt"], F["ramo_c"]),
            "veredito": F["verdict"],
            "defeito": "as ressalvas, ditas: %s | o que o teste não decide: %s | o registro CONFERE o que o kernel e o código pinado dão e não prova nada por si; a creditação é de quem observa de fora; o gate não se moveu e a independência das 4 bandeiras experimentais segue aberta (derivam de UM só booleano) [DECLARADO, GV-01 e GV-03]; a pendência [LEGAL] (D2) segue do operador; a revisão distinta do pacote (D167) não é afirmada por este registro; %s" % (C.ressalvas_pt(F), "; ".join(F["nao_decide"]), cauda),
            "nao_refazer": "o kernel da v411 é o da v410 (build incremental e Audit medidos: não refazer sem mudança de fonte); %s; o alcance de P = nP não muda: %s" % (TH["naorefazer"], DL_.D10.FRASE_QUALIFICADOR_PT),
            "proximo_passo": "%s; o README pinado (D39) e o release do app, na custódia e na engenharia da casa; a decisão [LEGAL] D2 com a agente de PI; o HANDOFF da v411 traz os blocos do README já prontos (o painel do topo, a linha do topo, o bloco do H0DN × BG1, a linha da tabela do estado; o bloco P = nP com a faixa de versões atualizada)" % TH["proximo"].rstrip("."),
            "onde": PK, "artefatos": arts + [DL_.INSUMO_POR_NOME[n_]["arquivo"] for n_ in ("RESULTADO_DA_ABERTURA_V411.json", "EMENDA_E_PRE_REGISTRO_V411.md", "RAMOS_V411.json", "PINOS_DE_PRODUCAO.json")], "refs": sorted((set(x["rota_id"] for x in T11) | set(REFS)) - {NOVA}),
            "nota": ("validade no kernel não é creditação; NOT_FALSIFIED (o desfecho do livro de cobranças) não é a palavra da creditação; o gate não se move; as erratas %s e as decisões %s são da gerência c1, em nome próprio, ao lado (nada foi apagado nem reescrito); "
                     "olhou_dados True porque o rito RELÊ o vetor da abertura única (seq %d, também True): é o mesmo vetor recalculado, não uma nova tentativa; os seq do livro citados (abertura %d, marca ratificada %d, publicação %d, preparação %d) foram LIDOS do livro; %s; os registros anteriores %s.") % (
                ERR, DEC, sq_ab, sq_ab, sq_pre, sq_pub, sq_prep, "P = nP " + DL_.D10.FRASE_QUALIFICADOR_PT, sim(not sem_selo, "seguem selados", "ALGUM REGISTRO ANTERIOR NAO SELOU"))}
    for r in ROTA["refs"]:
        assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
    REG = [ROTA] + T11
    for x in REG:
        for k_, v_ in x.items():
            if isinstance(v_, str):
                assert len(v_) <= 6000, "o campo %s de %s passa de 6000 caracteres (limite do Mapa): resuma e aponte o artefato" % (k_, x["rota_id"])
    # --- as guardas de texto sobre o registro inteiro (cada uma com controle negativo no teste sem candidato)
    import guarda_frases_v411 as GF
    bad = [(x["rota_id"], GF.violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if GF.violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad, "a guarda das frases (inclui a P18 e a F67) achou violacao(oes): %r" % bad
    bad_p18 = [(x["rota_id"], violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad_p18, "a guarda de texto (P18) achou violacao(oes): %r" % bad_p18
    import textos_v411 as T   # (so' aqui: a direcao do testemunho e a atribuicao seguem conferidas em todo texto novo)
    atrib = [(x["rota_id"], T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))]
    assert not atrib, "a direcao do testemunho esta invertida ou a atribuicao falhou: %r" % atrib
    d59 = [x["rota_id"] for x in REG if d59_viola(json.dumps(x, ensure_ascii=False))]
    assert not d59, "D59: o registro traz o que fica fora dos textos (o Milenio, o Navier; o nome do Kimi so' no contexto do H0DN): %r" % d59
    d65 = [x["rota_id"] for x in REG if any(f_.lower() in json.dumps(x, ensure_ascii=False).lower() for f_ in DL_.FORA_D65)]
    assert not d65, "D65: o registro traz o que a fala do nome do algoritmo deixa fora: %r" % d65
    n444 = [s_[:120] for x in REG for s_ in _strings(x) if "4,44" in s_.replace("−", "-") or "4.44" in s_]
    assert not n444, "a regra da ordem do 4,44: este registro nao cita o numero do quadro de 23/10, e algum campo o trouxe: %r" % n444[:2]
    j_ = {x["rota_id"] + "#" + x["tipo"]: json.dumps(x, ensure_ascii=False) for x in REG}
    tok = [k_ for k_, t_ in j_.items() if any(tk_ in t_ for tk_ in DL_.TOKENS_PROIBIDOS_V411)]
    assert not tok, "o registro traz um token de veredito proibido (%s): %r" % (", ".join(DL_.TOKENS_PROIBIDOS_V411), tok)
    por_dentro = [(x["rota_id"], k_) for x in REG for k_, v_ in x.items() if isinstance(v_, str) and re.search(C.RX_GATILHO_F67, v_, re.I) and (DL_.OBRIG_MODELO_PT not in v_ or DL_.OBRIG_VALIDADE_PT not in v_ or DL_.OBRIG_RETRO_PT not in v_ or DL_.OBRIG_NAO_CEGO_PT not in v_ or not re.search(DL_.OBRIG_CEFEIDAS_PT + r"[^\n]{0,160}?\d+,\d+", v_))]
    assert not por_dentro, "a regra da obrigacao (F67): o campo traz o resultado sem as quatro obrigacoes no mesmo campo: %r" % por_dentro[:3]
    assert all(selou(core, k_) for k_ in (DL_.FECHO_REGISTRO, DL_.CUNHAGENS_REGISTRO, DL_.KH_REGISTRO) + tuple(DL_.REGISTROS_FUNCAO_V410)), "algum registro (novo ou da v410) nao selou no core: o mapa nao registra a v411 assim"
    return REG


def gravar(p, b):
    """backup de BYTES se existir e mudar; temporario -> conferir tamanho -> substituir."""
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m411"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_m411"; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def main():
    import leitura_v411 as L   # (so' aqui: o import do teste sem candidato nao depende da leitura)
    V, PROB = L.ler()
    if PROB:
        print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); return 2
    NOS = L.NOS
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v411_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v411_*.json")), key=os.path.getmtime)
    arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto_selo_acom.json"), os.path.join(PK, "ESPERADOS_v411.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v411.json"),
            os.path.join(PK, "DIFF_KERNEL_v411.txt"), os.path.join(PK, "DIFF_v410_v411.diff"), os.path.join(NOS, "HANDOFF_v411_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v411.json"),
            os.path.join(PK, "kernel", "KERNEL_RECIBO_v411.json")] + b3[-1:]
    arts = [x for x in arts if os.path.exists(x)]
    REG = montar(V, core, selo, ids_do_livro(), arts)
    J = os.path.join(HERE, "registro_mapa_v411.json")
    gravar(J, json.dumps(REG, ensure_ascii=False, indent=1).encode("utf-8"))
    quem = "claude-c1 (gerência), cadeia v411"
    print("registro MONTADO (NAO registrado): %d registro(s) (%s) -> %s" % (len(REG), ", ".join(x["tipo"] for x in REG), J))
    print("COMANDO (o passo 12 da cadeia o executa, uma vez so): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
    print("DEPOIS DO REGISTRO: os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
