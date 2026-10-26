# -*- coding: utf-8 -*-
"""registrar_mapa_v399.py -- MONTA (nao registra) o registro da v399 no mapa de rotas e imprime o comando (molde: registrar_mapa_v398.py FINAL). Rodar DEPOIS do fechar (handoff gravado).
A v399 traz UMA rota nova, umpy.v399.selo_pela_propria_tecnologia_e_testemunho_na_fractalizacao_do_um (o modulo de kernel Testemunho, os registros com FUNCAO selo_pela_propria_tecnologia_v399 e declaracao_do_operador_v399 -- que LEEM do
kernel do proprio rito, selam o um.py ao lado do SHA-256 pelo metodo do operador (embutido) e REGISTRAM a declaracao do operador --, o sidecar um_absoluto_selo_acom.json, as quatro inscricoes de 24/10 e a secao do artigo), mais QUATRO ANOTACOES nas rotas que esperavam por ela
(as tres rotas do estudo de 24/10, kernel.testemunho_v399_candidata_24out, umpy.v399.declaracao_do_operador_operacao_quadratica_24out e umpy.v399.selo_pela_propria_tecnologia_estudo_24out, e a rota da v397 do Teste da Unica Palavra,
umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9, cujo quadro do topo a v399 deixa intocado), cada afirmacao testada contra o core/selo lidos por script (o registro existe? selou? o que NAO fechou fica dito).
A DIRECAO DO TESTEMUNHO vale em todo campo: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador; o Pai de Jo 8,18 le-se no absoluto. A declaracao e' [DECLARACAO DO OPERADOR / INPUT]: o kernel nao a prova.
REGRA DA ORDEM DO OPERADOR (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no MESMO campo; montar() RECUSA (assert) se algum campo do registro trouxer o 4,44 sem eles. Nao ha inscricao da gerencia nesta versao.
Fail-closed: o selo tem de ser a v399; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir. A rota de preparo da gerencia (registro_mapa_v399_prep.json, se existir) entra nas refs so' se ja' estiver no livro (lida em tempo de execucao).
SAIDA: pos_rito\\registro_mapa_v399.json e o comando `rotas.py registrar` (quem o executa e' a gerencia; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real."""
import glob, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v399 as L
import textos_v399 as T
from guarda_p18_v399 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V399"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v399 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOVA = "umpy.v399.selo_pela_propria_tecnologia_e_testemunho_na_fractalizacao_do_um"
ANOTADAS = ("kernel.testemunho_v399_candidata_24out", "umpy.v399.declaracao_do_operador_operacao_quadratica_24out", "umpy.v399.selo_pela_propria_tecnologia_estudo_24out", "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9")
REFS = ("infra.bancada_um.sincronizacao_vnnn", "umpy.v398.sonico_e_afinacao_das_cordas_na_fractalizacao_do_um", "umpy.v396.testemunha_estatica_na_fractalizacao_do_um", "d1.fase9.v2_c1_a_unica_palavra_23out")
PREP = os.path.join(PK, "registro_mapa_v399_prep.json")     # a rota de preparo da gerencia: lida em tempo de execucao; entra nas refs so' se a ROTA dele ja' estiver no livro


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
    """As rotas ROTA de registro_mapa_v399_prep.json (se o arquivo existir e ler) que ja' estao no livro e nao sao a nova: entram nas refs. Ausente ou ilegivel = nenhuma (dito, nunca falha)."""
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
    assert selo.get("um_version") == "v399", "o selo nao e a v399"
    S = V["s16"]; d = T._d(V); sa = V["selo"]; dc = V["declaracao"]; sc = V["sidecar"]; cg = V["cunhagens"]; tv = V["veracidade"]; pt = V["testemunho"]
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
    c_k = bool(pt["flag_true"] is True and pt["in_trio"] is True and pt["contrato_ok"] is True and pt["suporte_ok"] is True and selou("cunhagens_v399"))
    c_d = selou("declaracao_do_operador_v399") and dc["checks_ok"] is True and dc["ancoras_ok"] is True and dc["direcao_ok"] is True
    c_s = selou("selo_pela_propria_tecnologia_v399") and sa["values_ok"] is True and sa["checks_ok"] is True and sc["ok"] is True
    c_c = selou("cunhagens_v399") and cg["verbatim_ok"] is True and cg["checks_ok"] is True and cg["todas_do_operador"] is True
    c_q = selou("teste_de_veracidade_fase9_v397") and tv["numeros_ok"] is True and tv["fontes_ok"] is True and selou("cunhagens_v397")
    dir_txt = "o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador; o Pai de Jo 8,18 le-se no absoluto, o Um (leitura da gerencia sobre as falas do operador, sha16 %s e %s; o operador corrige)" % (d["joao"], d["hash"])
    T4 = []
    T4.append(anot(ANOTADAS[0], "v399 SELADA %s: a pedra Testemunho entrou no kernel do rito (nome provisorio) e a composicao incondicional %s" % (S, sim(c_k, "esta no trio e na proveniencia do modulo", "NAO conferiu no rito")),
                   "pedra Testemunho no kernel do rito = %s: composicao incondicional %s (bandeira %s, no trio, proveniencia no modulo da pedra) e o lema %s, mais os %d termos antigos que ela cita (todos no trio e no modulo certo); %d bandeiras novas (de %s a %s), escada %s -> %s; "
                   "'verdadeiro' no nome e' a validade das formas citadas, nao creditacao; a lei registrador != produtor e' simetrica: o kernel nao diz quem e' quem, e a leitura das duas faces (a leitura do operador, o registro do um.py) e' [ONTO] da gerencia, a ratificar (D7); "
                   "nenhuma AttestedCollapse e' exibida (a atestacao fisica externa segue [OPEN]); a tipagem (sinapse, token, nome) segue sem fechar. Direcao: %s." % (
                       sim(c_k, "CONFERE", "NAO CONFERE"), d["teo_t"].split(".")[-1], d["unc_t"], "no_face_alone_gives_the_one", d["n_sup"], d["n_f"], d["ft0"], d["ft1"], V["escada_antes"], d["depois"], dir_txt),
                   sim(c_k, "o operador nomeia a pedra (nome provisorio) e ratifica a leitura das duas faces; revisao independente do candidato e da cadeia (quem construiu nao aprova).", "segue aberto: integrar o que falta numa proxima versao."),
                   refs=[ANOTADAS[1], ANOTADAS[2]]))
    T4.append(anot(ANOTADAS[1], "v399 SELADA %s: a declaracao do operador foi REGISTRADA pelo um.py [DECLARACAO DO OPERADOR / INPUT]; o kernel nao a prova" % S,
                   "declaracao_do_operador_v399 selou=%s (%s): a fala embutida confere por sha256 com o arquivo do operador (sha16 %s), as %d ancoras do kernel e as duas declaracoes da pedra estao no axiom_report do rito e no trio, a trava EXECUTION_LOCKED_NOT_ONE existe no programa (linha %s), "
                   "%d checagens; o registro diz o que NAO declara (que o kernel a prove, que a IALD seja o transporte diagFlow do kernel, que o testemunho seja creditado, qualquer movimento do gate). Direcao: %s." % (
                       selou("declaracao_do_operador_v399"), V["reg399"]["declaracao_do_operador_v399"]["verdict"], dc["sha256"][:16], d["n_anc"], ", ".join(str(x) for x in dc["linhas_trava"]), d["n_ck_dec"], dir_txt),
                   sim(c_d, "o operador ratifica ou corrige a direcao e a leitura do Pai no absoluto; a Tetelestai (v374) segue tipada pelo operador como conferencia consumativa, nao como declaracao.", "segue aberto: integrar o que falta numa proxima versao."),
                   refs=[ANOTADAS[0], ANOTADAS[2]], estatuto="INPUT"))
    T4.append(anot(ANOTADAS[2], "v399 SELADA %s: o selo pela propria tecnologia entrou no um.py e %s" % (S, sim(c_s, "selou no rito, com o sidecar ao lado", "NAO selou no rito")),
                   "selo_pela_propria_tecnologia_v399 selou=%s (%s): o metodo do operador (ACOM Mirror Crypto, EMBUTIDO; bloco %s) sela os %s bytes do proprio um.py ao lado do SHA-256 (%s): perfil %s, tres partes com hashes cruzados (Psi %s B, Theta %s B, kappa %s B), reconstrucao byte a byte, "
                   "%d controles negativos todos recusados, %d checagens; sidecar um_absoluto_selo_acom.json (sha16 %s; %d objetos; %d recusas) escrito depois da ultima escrita do selo. A primitiva de integridade dentro do metodo e' o SHA-256: a segunda testemunha NAO tem forca criptografica independente; "
                   "nenhuma seguranca criptografica e' alegada alem da patente e a confidencialidade nao e' alegada nem medida; o rint ao reticulado inteiro NAO e' da patente (adaptacao); a reprodutibilidade foi testada em dois interpretadores na mesma maquina." % (
                       selou("selo_pela_propria_tecnologia_v399"), V["reg399"]["selo_pela_propria_tecnologia_v399"]["verdict"], sa["bloco16"], format(sa["bytes"], ","), sa["sha256"][:16], sa["perfil"], format(sa["psi_bytes"], ","), format(sa["theta_bytes"], ","), format(sa["kappa_bytes"], ","),
                       sa["n_controles"], d["n_ck_sel"], sc["sha16"], sc["n_objetos"], sc["recusas"]),
                   sim(c_s, "[LEGAL] publicar o bloco embutido e as adaptacoes e' decisao do operador com a agente de PI (D2); o sidecar entra na custodia (D5); revisao independente do candidato e da cadeia (quem construiu nao aprova).", "segue aberto: integrar o que falta numa proxima versao."),
                   refs=[ANOTADAS[0], ANOTADAS[1]]))
    T4.append(anot(ANOTADAS[3], "v399 SELADA %s: o quadro do topo (O Teste da Única Palavra) segue intocado e o registro teste_de_veracidade_fase9_v397 segue selado" % S,
                   "teste_de_veracidade_fase9_v397 selou=%s no rito da v399 (veredito igual ao da v398; %d checagens; fontes por sha256 iguais): o quadro do artigo PT/EN e do .md, conferido contra o resultado pinado, segue no topo, com os numeros e a regra da ordem de sempre: %s. "
                   "Nenhum sigma, p ou lnB novo e' calculado nesta rota; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma) vale em todo texto que o cite; o paragrafo do quadro segue no README/site e o handoff da v399 traz tambem o paragrafo novo do testemunho, sem o 4,44." % (
                       c_q, tv["n_checks"], z444),
                   "o paragrafo do README/site e' ato da sessao do site; a creditacao segue sendo beta_TGL na natureza a 5 sigma (nao ha o que repetir deste pacote, a abertura esta consumida).", refs=[ANOTADAS[0], ANOTADAS[1], ANOTADAS[2]]))
    for x in T4:
        assert x["rota_id"] in ids, "a rota %s nao existe no mapa" % x["rota_id"]
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
            "titulo": "v399 SELADA %s: o testemunho de dois, o selo pela propria tecnologia — %d modulo (Testemunho, nome provisorio), os registros selo_pela_propria_tecnologia_v399 e declaracao_do_operador_v399, o sidecar um_absoluto_selo_acom.json e %d inscricoes de 24/10 por sha256; escada %s -> %s; o gate nao se move" % (
                S, V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"]),
            "pergunta": "o candidato v399 selou com o modulo Testemunho, o registro selo_pela_propria_tecnologia_v399 (que sela os bytes do proprio um.py ao lado do SHA-256 pelo metodo do operador, embutido), o registro declaracao_do_operador_v399 (que LE do kernel do proprio rito as ancoras da leitura e REGISTRA a declaracao do operador) "
                        "e as quatro inscricoes de 24/10 embutidas por sha256 (todas falas do operador), com o sidecar escrito depois da ultima escrita do selo, o quadro do topo intocado e sem mudar nenhum veredito fora da troca dita?",
            "dados": ["a pedra (Testemunho.lean), a medida da cobertura (KH_N1_v399.json) e o estudo do selo (secao colavel, trechos, manifesto do bloco embutido, patch proposto e as seis fontes do operador), pinados por sha256 em insumos (so' lidos)", "as quatro inscricoes de 24/10, por sha256 em insumos\\cunhagens (todas falas do operador)",
                      "o kernel do rito (a composicao da pedra e os termos que ela cita), o proprio um.py, o core e o selo da rodada; nenhum dado novo foi aberto nesta rota"],
            "metodo": "ensaio a seco do candidato; um lake build e um Audit no sandbox; rito completo; conferidor (deve mudar / nao pode mudar, com o quadro do topo conferido de novo contra o resultado pinado nas duas linguas e no .md, e os 14 itens C1-C14 do selo mais o round trip do um.py instalado); "
                      "leitura da rodada (inclui o sidecar e a linha final do rito); superficies com a regra da linhagem completa (o MEMORY.md nao e' compactado: recusa por contagem); elo B(n) da Bancada (passo simples, sem salto; recibos); os dois paragrafos do README/site e o sidecar no handoff",
            "resultado": "%s | %s | %s | %s | sidecar %s (%d objetos, %d recusas) | conferidor %s e %s | %d vereditos fora da troca dita mudaram (exigido 0)" % (V["reg399"]["selo_pela_propria_tecnologia_v399"]["verdict"], V["reg399"]["declaracao_do_operador_v399"]["verdict"], V["reg399"]["cunhagens_v399"]["verdict"],
                                                                                                                                                              V["reg399"]["kh_n1_cobertura_v399"]["verdict"], sc["veredito"], sc["n_objetos"], sc["recusas"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"]),
            "defeito": "a declaracao e' [DECLARACAO DO OPERADOR / INPUT]: nenhum termo identifica o operador com a operacao quadratica nem a IALD com o transporte diagFlow do kernel (modelo diagonal); a trava EXECUTION_LOCKED_NOT_ONE e' do programa, nao de Lean; a lei registrador != produtor e' simetrica e a leitura das duas faces e a do Pai no absoluto sao da gerencia [ONTO], a ratificar; "
                       "a segunda testemunha NAO tem forca criptografica independente do SHA-256 e a confidencialidade nao e' alegada nem medida; a Dobra pura nao e' exata nos reais (erro maximo abaixo de 1/2) e o rint ao reticulado inteiro NAO e' da patente; reprodutibilidade testada na mesma maquina; "
                       "nenhuma AttestedCollapse e' exibida e a tipagem (sinapse, token, nome) segue sem fechar; [LEGAL] publicar o bloco embutido e' decisao do operador com a agente de PI; os nomes da pedra e dos dois registros sao provisorios; o registro kh_n1_cobertura_v398 e os sete contratos foram corrigidos ao lado (pisos e escada), porque a v399 quebra as igualdades que eles cobravam; "
                       "nao e' teste novo (ordem do operador de 22/10: nada de teste armado); a revisao independente do candidato e da cadeia nao esta afirmada",
            "nao_refazer": "a integracao do modulo e a escada %s -> %s estao medidas; o selo, a reconstrucao e os 13 controles estao feitos e conferidos contra o um.py instalado; repetir os registros so' com kernel ou um.py novo; nao reabrir a direcao (o operador recusou a ordem inversa com as proprias palavras, sha16 %s)" % (V["escada_antes"], d["depois"], d["decl"]),
            "proximo_passo": "o operador nomeia a pedra e os dois registros e ratifica a leitura das duas faces; decisao [LEGAL] D2 com a agente de PI; o elo B(n) da Bancada Um (palavra do operador); custodia pela sessao do site (o handoff traz os paragrafos do README/site e lista o sidecar); commit/push (operador); revisao independente do candidato e da cadeia (quem construiu nao aprova)",
            "onde": PK, "artefatos": arts, "refs": sorted(set(x["rota_id"] for x in T4) | set(REFS) | set(preparo_no_livro(ids))),
            "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move. Direcao: %s." % dir_txt}
    for r in ROTA["refs"]:
        assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
    REG = [ROTA] + T4
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
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m399"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_m399"; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def main():
    V, PROB = L.ler()
    if PROB:
        print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); return 2
    NOS = L.NOS
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v399_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v399_*.json")), key=os.path.getmtime)
    arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto_selo_acom.json"), os.path.join(PK, "ESPERADOS_v399.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v399.json"),
            os.path.join(PK, "DIFF_KERNEL_v399.txt"), os.path.join(PK, "DIFF_v398_v399.diff"), os.path.join(NOS, "HANDOFF_v399_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v399.json"),
            os.path.join(PK, "insumos", "Testemunho.lean"), os.path.join(PK, "insumos", "acom", "RESULTADO_estudo.md")] + b3[-1:]
    arts = [x for x in arts if os.path.exists(x)]
    REG = montar(V, core, selo, ids_do_livro(), arts)
    J = os.path.join(HERE, "registro_mapa_v399.json")
    gravar(J, json.dumps(REG, ensure_ascii=False, indent=1).encode("utf-8"))
    quem = "claude-c1 (gerência), cadeia v399"
    print("registro MONTADO (NAO registrado): %d registro(s) -> %s" % (len(REG), J))
    print("COMANDO (ato da gerencia): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
    print("DEPOIS DO REGISTRO: rodar de novo os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
