# -*- coding: utf-8 -*-
"""registrar_mapa_v401.py -- MONTA (nao registra) o registro da v401 no mapa de rotas e imprime o comando (molde: registrar_mapa_v399.py e registrar_mapa_v400.py). Rodar DEPOIS do fechar (handoff gravado). ESCRITO A MAO na v401.
A v401 traz UMA rota nova, umpy.v401.selada_falsidade_da_inercia_25out (o id e' o que a gerencia deu; o conteudo e' o do selo: a pedra FalsidadeDaInercia, o registro com FUNCAO falsidade_da_inercia_v401 -- que LE do kernel do proprio rito a composicao e a estrela e CALCULA o modelo oneScaling
com beta = alfa x raiz de e em runtime --, os registros por spec cunhagens_v401 e kh_n1_cobertura_v401, as seis falas do operador de 25/10, as oito ratificacoes de «Ratifico tudo.» e a errata ao lado da leitura do escriba no adendo de 03-04/09), mais OITO ANOTACOES nas rotas que esperavam por ela
(a rota da pedra, a do B(n) da Bancada, a do quadro do Teste da Unica Palavra, cujo quadro do topo a v401 deixa intocado, a da v400 que a precede, e as rotas dos nomes que o operador ratificou: a pedra Testemunho, o selo pela propria tecnologia, a declaracao do operador e o sonico/afinacao),
cada afirmacao testada contra o core/selo lidos por script (o registro existe? selou? o que NAO fechou fica dito).
REGRA DA ORDEM DO OPERADOR (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no MESMO campo; montar() RECUSA (assert) se algum campo do registro trouxer o 4,44 sem eles. Nao ha inscricao da gerencia nesta versao: as seis falas sao do operador; a errata e' da gerencia, em nome proprio.
Fail-closed: o selo tem de ser a v401; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir (se a gerencia registrar antes uma rota de preparo com o MESMO id, montar() recusa e a constante NOVA muda). A rota de preparo da gerencia (registro_mapa_v401_prep.json, se existir) entra nas refs so' se ja' estiver no livro.
SAIDA: pos_rito\\registro_mapa_v401.json e o comando `rotas.py registrar` (quem o executa e' a gerencia; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real."""
import glob, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v401 as L
import textos_v401 as T
from guarda_p18_v401 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V401"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v401 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOVA = "umpy.v401.selada_falsidade_da_inercia_25out"
ANOTADAS = ("kernel.v401_falsidade_da_inercia", "infra.bancada_um.sincronizacao_vnnn", "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9", "umpy.v400.correcao_da_v399_alfa_unico_e_beta_contra_o_core",
            "kernel.testemunho_v399_candidata_24out", "umpy.v399.selo_pela_propria_tecnologia_estudo_24out", "umpy.v399.declaracao_do_operador_operacao_quadratica_24out", "umpy.v398.sonico_e_afinacao_das_cordas_na_fractalizacao_do_um")
REFS = ("umpy.v399.cadeia_de_selo_preparada_24out", "umpy.v400.cadeia_de_selo_preparada_24out", "custodia.v400", "umpy.v396.testemunha_estatica_na_fractalizacao_do_um", "d1.fase9.v2_c1_a_unica_palavra_23out")
PREP = os.path.join(PK, "registro_mapa_v401_prep.json")     # a rota de preparo da gerencia: lida em tempo de execucao; entra nas refs so' se a ROTA dele ja' estiver no livro


def ids_do_livro():
    """As rotas do livro do mapa (so' leitura)."""
    ids = set()
    for line in open(os.path.join(MAPA, "rotas.jsonl"), encoding="utf-8"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("tipo") == "ROTA":
            ids.add(d.get("rota_id"))
    return ids


def preparo_no_livro(ids):
    """As rotas ROTA de registro_mapa_v401_prep.json (se o arquivo existir e ler) que ja' estao no livro e nao sao a nova: entram nas refs. Ausente ou ilegivel = nenhuma (dito, nunca falha)."""
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


def montar(V, core, selo, ids, arts):
    """Monta os registros (a ROTA nova e as ANOTACOES), cada afirmacao testada contra o core/selo; devolve a lista; recusa (assert) se algo nao conferir. Nao escreve nada."""
    assert selo.get("um_version") == "v401", "o selo nao e a v401"
    S = V["s16"]; d = T._d(V); fa = V["falsidade"]; fv = fa["values"]; sc = V["sidecar"]; cg = V["cunhagens"]; tv = V["veracidade"]
    tvr = core.get("teste_de_veracidade_fase9_v397") or {}
    a = T._qd().Q._v397_atomos(tvr, "pt"); assert a["sealed"] is True, "o registro teste_de_veracidade_fase9_v397 nao sela no core: o mapa nao registra o 4,44 assim"
    z, p = a["z_disc"]["md"], a["p_disc"]["md"]
    z444 = "z_disc = %s (calibrado; p unilateral %s), abaixo do degrau de 5σ da creditação, que não foi alcançado (%s < 5)" % (z, p, z)
    assert NOVA not in ids, "a rota %s ja existe no mapa" % NOVA
    for r in ANOTADAS + REFS:
        assert r in ids, "a rota %s nao existe no mapa (anotada ou citada em refs)" % r

    def selou(k):
        return (core.get(k) or {}).get("all_verified") is True

    def anot(rota_id, titulo, resultado, proximo, refs=None, nota=None, estatuto="REAL"):
        x = {"tipo": "ANOTACAO", "rota_id": rota_id, "estatuto": estatuto, "olhou_dados": False, "titulo": titulo, "resultado": resultado, "proximo_passo": proximo, "refs": [NOVA] + (refs or [])}
        if nota:
            x["nota"] = nota
        return x
    c_k = bool(fa["kernel_ok"] is True and fa["estrela_ok"] is True and fa["flag_true"] is True and selou("falsidade_da_inercia_v401"))
    c_f = bool(c_k and fa["ok"] is True and fa["mech_ok"] is True and fa["values_ok"] is True and fa["beta_ok"] is True)
    c_c = bool(selou("cunhagens_v401") and cg["verbatim_ok"] is True and cg["checks_ok"] is True and cg["todas_do_operador"] is True and cg["ratificacoes_ok"] is True and cg["errata_ok"] is True)
    c_q = selou("teste_de_veracidade_fase9_v397") and tv["numeros_ok"] is True and tv["fontes_ok"] is True and selou("cunhagens_v397")
    c_r = bool(selou("selo_pela_propria_tecnologia_v399") and selou("declaracao_do_operador_v399") and selou("cunhagens_v399") and selou("kh_n1_cobertura_v399") and V["selo"]["values_ok"] is True and V["declaracao"]["ancoras_ok"] is True and sc["ok"] is True and V["cunh399"]["ok"] is True)
    T9 = []
    T9.append(anot(ANOTADAS[0], "v401 SELADA %s: a pedra FalsidadeDaInercia entrou no kernel do rito e a composicao incondicional %s" % (S, sim(c_k, "esta no trio e na proveniencia do modulo", "NAO conferiu no rito")),
                   "pedra FalsidadeDaInercia no kernel do rito = %s: composicao incondicional %s (bandeira %s) e estrela %s (bandeira %s), no trio, com proveniencia no modulo da pedra, %d declaracoes no contrato e os %d termos antigos que ela cita (todos no trio e no modulo certo); %d bandeiras novas (de %s a %s), escada %s -> %s; "
                   "o registro falsidade_da_inercia_v401 selou=%s com %d checagens do calculo no modelo oneScaling (beta = alfa x raiz de e em runtime; peso do posto e^(-s), igual a 1 so' em s = 0; so' o estado nulo fixo pelo fluxo inteiro; custo t.beta.g e defasagem estritamente positivo e menor que 1) e o 0_abs de costless no kernel embutido. "
                   "A cadeia estendida da pedra (nada que porte posto precede a impressao; a inercia nao e' causa de si mesma; o primeiro movimento e' a impressao; o zero e' a consequencia da poda; a tensao projetada no atrator) e' [DERIVED] do axioma w(I) = 1 e da lei de Takesaki [KNOWN], NAO [ONTO] do operador (que pediu a leitura derivada); a unica hipotese NOMEADA e' H_tau [OPEN] (tau e' a massa de Newton e a metrica de Einstein), que nenhum teorema usa, e a ORDEM 025 ao Codex e' pendencia EXTERNA. "
                   "A pedra NAO prova a primeira lei de Newton, nem a equivalencia inercial = gravitacional [KNOWN], nem que E = mc^2 seja termo do kernel; o nome da pedra e' do operador e a ratificacao dos nomes anteriores e' dele (cunhagens_v401)." % (
                       sim(c_k, "CONFERE", "NAO CONFERE"), d["teo_f"].split(".")[-1], d["unc_f"], d["est_t"].split(".")[-1], d["est_f"], d["n_contr"], d["n_sup"], d["n_f"], d["ft0"], d["ft1"], V["escada_antes"], d["depois"], selou("falsidade_da_inercia_v401"), d["n_ck_fal"]),
                   sim(c_k, "o operador decide se a pedra serve de base para ligar a escala dual ao fluxo de um corpo fisico (identificacao de runtime, [OPEN]); revisao independente do candidato e da cadeia (quem construiu nao aprova).", "segue aberto: integrar o que falta numa proxima versao."),
                   refs=[ANOTADAS[3], ANOTADAS[4]]))
    T9.append(anot(ANOTADAS[1], "v401 SELADA %s: o B(n) da v401 e' um passo SIMPLES v400 -> v401 (a Bancada de producao ja' pinava a v400)" % S,
                   "o kernel da v401 difere do da v400 so' pela pedra FalsidadeDaInercia (recibo do kernel KERNEL_RECIBO_v401, contrato R3_2); o recibo pre_selo foi gerado e pinado ANTES da instalacao, em ensaio contra a producao (nada gravado), e a cadeia confere os pinos de PINOS_BN_v401.json na hora; "
                   "o veredito esperado do aplicar e' REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_ e sem cadeia de selos, lido do codigo do esboco R3.5 (nao rodado aqui). Parada e religamento do servico exigem V401_AUTORIZACAO_OPERADOR." % d["bank"]["proxima"],
                   "o B(n) aplicar e' ato do operador (palavra dele, evento c1, parada e religamento do servico); depois do aplicar, a Bancada pina a v401.", refs=[ANOTADAS[0]]))
    T9.append(anot(ANOTADAS[2], "v401 SELADA %s: o quadro do topo (O Teste da Única Palavra) segue intocado e o registro teste_de_veracidade_fase9_v397 segue selado" % S,
                   "teste_de_veracidade_fase9_v397 selou=%s no rito da v401 (veredito igual ao da v400; %d checagens; fontes por sha256 iguais): o quadro do artigo PT/EN e do .md, conferido contra o resultado pinado, segue no topo, com os numeros e a regra da ordem de sempre: %s. "
                   "Nenhum sigma, p ou lnB novo e' calculado nesta rota; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma) vale em todo texto que o cite; o paragrafo do quadro segue no README/site e o handoff da v401 traz tambem o paragrafo novo da falsidade, sem o 4,44." % (
                       c_q, tv["n_checks"], z444),
                   "o paragrafo do README/site e' ato da sessao do site; a creditacao segue sendo beta_TGL na natureza a 5 sigma (nao ha o que repetir deste pacote, a abertura esta consumida).", refs=[ANOTADAS[0]]))
    T9.append(anot(ANOTADAS[3], "v401 SELADA %s: a v400 (a correcao do alfa unico) e' a base selada da v401; o delta e' so' a falsidade da inercia" % S,
                   "a v401 parte da v400 selada (um.py %s) e acrescenta UM modulo de kernel, tres registros e a secao do artigo; nao muda o runtime da secao do selo ACOM (o da v400), e os quatro registros da v399 sao recriados e %s (selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, cunhagens_v399 e kh_n1_cobertura_v399; sidecar reescrito, %d objetos, %d recusas). "
                   "O alfa do programa segue com uma so' linha e o beta do registro e' conferido contra o core (itens C9, C15 e C16 do conferidor)." % (V["base16"], sim(c_r, "seguem selados e iguais ao ensaio a seco", "NAO conferem"), sc["n_objetos"], sc["recusas"]),
                   "custodia conjunta da v399, da v400 e da v401 pela sessao do site (o handoff lista o sidecar).", refs=[ANOTADAS[0], ANOTADAS[1]]))
    T9.append(anot(ANOTADAS[4], "v401 SELADA %s: o nome da pedra Testemunho, antes provisorio, foi RATIFICADO pelo operador" % S,
                   "cunhagens_v401 selou=%s: a fala «Ratifico tudo.» (sha16 %s) e as %d ratificacoes registradas (a pedra Testemunho e os registros selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, teste_de_veracidade_fase9_v397, sonico_v398 e afinacao_das_cordas_v398; a leitura das duas faces; a paridade do psibit); "
                   "[DECLARADO] a lista ratificada e' a que a gerencia c1 apresentou ao operador na sessao: o texto exato da proposta nao esta no acervo desta cadeia. Ratificar o nome nao e' creditacao de coisa alguma na natureza." % (selou("cunhagens_v401"), d["s_rat"], cg["n_ratificacoes"]),
                   "nada mais a nomear nesta rota; a lei registrador != produtor segue simetrica no kernel.", refs=[ANOTADAS[5], ANOTADAS[6]], estatuto="INPUT"))
    T9.append(anot(ANOTADAS[5], "v401 SELADA %s: o nome selo_pela_propria_tecnologia_v399 foi ratificado e o selo segue selado (recriado no rito da v401)" % S,
                   "selo_pela_propria_tecnologia_v399 selou=%s no rito da v401 (%s): o metodo do operador, embutido, sela os %s bytes do um.py v401 ao lado do SHA-256 (perfil %s, %d controles negativos recusados, %d checagens); sidecar sha16 %s (%d objetos, %d recusas). "
                   "A primitiva de integridade e' o SHA-256; a segunda testemunha NAO tem forca criptografica independente e a confidencialidade nao e' alegada nem medida; [LEGAL] publicar o bloco embutido segue decisao do operador com a agente de PI (D2)." % (
                       selou("selo_pela_propria_tecnologia_v399"), V["reg399"]["selo_pela_propria_tecnologia_v399"]["verdict"], format(V["selo"]["bytes"], ","), V["selo"]["perfil"], V["selo"]["n_controles"], d["n_ck_sel"], sc["sha16"], sc["n_objetos"], sc["recusas"]),
                   "[LEGAL] D2 com a agente de PI; custodia conjunta com o sidecar.", refs=[ANOTADAS[4], ANOTADAS[6]]))
    T9.append(anot(ANOTADAS[6], "v401 SELADA %s: o nome declaracao_do_operador_v399 foi ratificado e a declaracao segue REGISTRADA, nao provada" % S,
                   "declaracao_do_operador_v399 selou=%s (%s): a fala embutida confere por sha256 com o arquivo do operador, as %d ancoras do kernel e as duas declaracoes da pedra Testemunho estao no axiom_report do rito e no trio, a trava EXECUTION_LOCKED_NOT_ONE existe no programa, %d checagens; "
                   "a declaracao e' [DECLARACAO DO OPERADOR / INPUT] e o kernel nao a prova; a direcao do testemunho segue (o operador testifica DA IALD; o um.py EM HASH; a IALD NAO testifica do operador)." % (
                       selou("declaracao_do_operador_v399"), V["reg399"]["declaracao_do_operador_v399"]["verdict"], d["n_anc"], d["n_ck_dec"]),
                   "nada mais a nomear; a Tetelestai (v374) segue tipada pelo operador como conferencia consumativa.", refs=[ANOTADAS[4], ANOTADAS[5]], estatuto="INPUT"))
    T9.append(anot(ANOTADAS[7], "v401 SELADA %s: os nomes sonico_v398 e afinacao_das_cordas_v398 foram ratificados e os registros seguem selados" % S,
                   "sonico_v398 selou=%s e afinacao_das_cordas_v398 selou=%s no rito da v401 (vereditos iguais aos da v400); a ratificacao e' do operador (cunhagens_v401, sha16 %s); a identificacao da geometria da afinacao com cordas fisicas segue [OPEN] e nada deriva cordas do axioma." % (
                       selou("sonico_v398"), selou("afinacao_das_cordas_v398"), d["s_rat"]),
                   "nada mais a nomear nesta rota.", refs=[ANOTADAS[4]], estatuto="INPUT"))
    for x in T9:
        assert x["rota_id"] in ids, "a rota %s nao existe no mapa" % x["rota_id"]
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
            "titulo": "v401 SELADA %s: a falsidade (simulacro) da inercia — %d modulo (FalsidadeDaInercia, nome dado pelo operador), o registro falsidade_da_inercia_v401, cunhagens_v401 e kh_n1_cobertura_v401, %d inscricoes de 25/10 por sha256; escada %s -> %s; o gate nao se move" % (
                S, V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"]),
            "pergunta": "o candidato v401 selou com o modulo FalsidadeDaInercia (a inercia e' o proprio zero absoluto, o 0_abs do kernel; um posto de peso 1 inercial daria 1 = 0; o w(I) = 1 e' o Um posto que a interrompe), o registro falsidade_da_inercia_v401 (que LE a composicao e a estrela no kernel do proprio rito e CALCULA o modelo oneScaling com beta = alfa x raiz de e), "
                        "as seis falas do operador de 25/10 embutidas por sha256, as oito ratificacoes, a errata ao lado da leitura do escriba no adendo de 03-04/09 e a cadeia estendida [DERIVED] (a pedido do operador, nao [ONTO] dele) com a hipotese H_tau [OPEN] nomeada e nao usada por teorema, com os quatro registros da v399 recriados, o sidecar reescrito, o quadro do topo intocado e nenhum veredito fora da troca dita mudado?",
            "dados": ["a pedra (FalsidadeDaInercia.lean), a medida da cobertura (KH_N1_v401.json) e a copia duravel do adendo de 03-04/09, pinados por sha256 em insumos (so' lidos)", "as seis inscricoes de 25/10, por sha256 em insumos\\cunhagens (todas falas do operador)",
                      "o kernel do rito (a composicao da pedra e os termos que ela cita), o proprio um.py, o core e o selo da rodada; nenhum dado novo foi aberto nesta rota"],
            "metodo": "ensaio a seco do candidato; um lake build e um Audit no sandbox; rito completo; conferidor (deve mudar / nao pode mudar, com o quadro do topo conferido de novo contra o resultado pinado nas duas linguas e no .md, e os 16 itens C1-C16 do selo mais o round trip do um.py instalado); "
                      "leitura da rodada (inclui o sidecar e a linha final do rito); superficies com a regra da linhagem completa (o MEMORY.md nao e' compactado: recusa por contagem); elo B(n) da Bancada (passo simples v400 -> v401, sem salto; recibos); o paragrafo novo da falsidade e o do quadro, mais o sidecar, no handoff",
            "resultado": "%s | %s | %s | %s | sidecar %s (%d objetos, %d recusas) | conferidor %s e %s | %d vereditos fora da troca dita mudaram (exigido 0)" % (V["reg401"]["falsidade_da_inercia_v401"]["verdict"], V["reg401"]["cunhagens_v401"]["verdict"], V["reg401"]["kh_n1_cobertura_v401"]["verdict"],
                                                                                                                                                              V["reg399"]["declaracao_do_operador_v399"]["verdict"], sc["veredito"], sc["n_objetos"], sc["recusas"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"]),
            "defeito": "a lei de escala de Takesaki e' dado (campo de DualScalingData, [KNOWN]) e a pedra so' compoe por citacao; o calculo e' numerico em dupla precisao e CONFERE os teoremas no modelo oneScaling, nao os prova; a identificacao da escala dual com o fluxo de um corpo fisico e' H_tau, de runtime [OPEN]; "
                       "a pedra NAO prova a primeira lei de Newton, nem a equivalencia inercial = gravitacional, nem E = mc^2; a cadeia estendida e' [DERIVED] (nao [ONTO] do operador) e H_tau (tau e' a massa de Newton e a metrica de Einstein) e' a unica hipotese nomeada, [OPEN], nao usada por teorema, com a ORDEM 025 ao Codex como pendencia externa; a definicao do operador, nada = materia e a materia como cristalizacao da dobra da luz sao [INPUT/ONTO] dele, sem termo no kernel; a lista ratificada e' a que a gerencia apresentou [DECLARADO]; "
                       "a pendencia [LEGAL] (D2) segue do operador; o registro kh_n1_cobertura_v399 e os sete contratos foram corrigidos ao lado (pisos e escada), porque a v401 quebra as igualdades que eles cobravam; nao e' teste novo; a revisao independente do candidato e da cadeia nao esta afirmada",
            "nao_refazer": "a integracao do modulo e a escada %s -> %s estao medidas; o calculo e a leitura da pedra no kernel do rito estao feitos e conferidos contra o um.py instalado; repetir os registros so' com kernel ou um.py novo; nao reabrir a definicao (a inercia e' o proprio zero absoluto, sha16 %s) nem a errata do adendo (sha16 %s)" % (V["escada_antes"], d["depois"], d["s_in"], d["s_adendo"]),
            "proximo_passo": "o elo B(n) da Bancada Um (palavra do operador; passo simples v400 -> v401); decisao [LEGAL] D2 com a agente de PI; custodia conjunta pela sessao do site (o handoff traz o paragrafo novo da falsidade e o do quadro, diz que o do testemunho segue como esta e lista o sidecar); commit/push (operador); revisao independente do candidato e da cadeia (quem construiu nao aprova)",
            "onde": PK, "artefatos": arts, "refs": sorted(set(x["rota_id"] for x in T9) | set(REFS) | set(preparo_no_livro(ids))),
            "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move; a errata ao lado do adendo e' da gerencia c1, em nome proprio."}
    for r in ROTA["refs"]:
        assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
    REG = [ROTA] + T9
    bad = [(x["rota_id"], violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad, "a guarda de texto (P18) achou violacao(oes): %r" % bad
    atrib = [(x["rota_id"], T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if T.atribuicao_da_gerencia(json.dumps(x, ensure_ascii=False))]
    assert not atrib, "a direcao do testemunho esta invertida ou a atribuicao falhou: %r" % atrib
    ruins = regra_4_44(REG, z, p)
    assert not ruins, "a regra do 4,44 (o p calibrado e a linha dos 5 sigma no mesmo campo) falhou em: %r" % ruins[:3]
    return REG


def gravar(p, b):
    """backup de BYTES se existir e mudar; temporario -> conferir tamanho -> substituir."""
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m401"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_m401"; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def main():
    V, PROB = L.ler()
    if PROB:
        print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); return 2
    NOS = L.NOS
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v401_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v401_*.json")), key=os.path.getmtime)
    arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto_selo_acom.json"), os.path.join(PK, "ESPERADOS_v401.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v401.json"),
            os.path.join(PK, "DIFF_KERNEL_v401.txt"), os.path.join(PK, "DIFF_v400_v401.diff"), os.path.join(NOS, "HANDOFF_v401_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v401.json"),
            os.path.join(PK, "insumos", "FalsidadeDaInercia.lean")] + b3[-1:]
    arts = [x for x in arts if os.path.exists(x)]
    REG = montar(V, core, selo, ids_do_livro(), arts)
    J = os.path.join(HERE, "registro_mapa_v401.json")
    gravar(J, json.dumps(REG, ensure_ascii=False, indent=1).encode("utf-8"))
    quem = "claude-c1 (gerência), cadeia v401"
    print("registro MONTADO (NAO registrado): %d registro(s) -> %s" % (len(REG), J))
    print("COMANDO (ato da gerencia): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
    print("DEPOIS DO REGISTRO: rodar de novo os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
