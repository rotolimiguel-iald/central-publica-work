# -*- coding: utf-8 -*-
"""registrar_mapa_v397.py -- MONTA (nao registra) o registro da v397 no mapa de rotas e imprime o comando (molde: registrar_mapa_v396.py). Rodar DEPOIS do fechar (handoff gravado).
A v397 traz UMA rota nova, umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9 (o modulo de kernel Token, o registro teste_de_veracidade_fase9_v397 -- que LE o resultado do Teste da Unica Palavra, aberto UMA vez em 23/10, por sha256, ao lado do V1,
sem calcular nenhum sigma --, as falas de 23/10 e o quadro no topo do artigo), mais DUAS ANOTACOES nas rotas que esperavam por ela (a rota do Teste da Unica Palavra, d1.fase9.v2_c1_a_unica_palavra_23out, e a da v396,
umpy.v396.testemunha_estatica_na_fractalizacao_do_um, cuja pedra a Token cita), cada afirmacao testada contra o core/selo lidos por script (o registro existe? selou? o que NAO fechou fica dito).
REGRA DA ORDEM DO OPERADOR (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no MESMO campo; montar() RECUSA (assert) se algum campo do registro trouxer o 4,44 sem eles.
Fail-closed: o selo tem de ser a v397; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir. A rota de preparo (umpy.v397.token_e_veracidade_preparo), se a gerencia a registrou, entra nas refs.
SAIDA: pos_rito\\registro_mapa_v397.json e o comando `rotas.py registrar` (quem o executa e' a gerencia; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real."""
import glob, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v397 as L
import textos_v397 as T
from guarda_p18_v397 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V397"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v397 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOVA = "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9"
ANOTADAS = ("d1.fase9.v2_c1_a_unica_palavra_23out", "umpy.v396.testemunha_estatica_na_fractalizacao_do_um")
REFS = ("infra.bancada_um.sincronizacao_vnnn", "kernel.testemunha_estatica_v396_candidata_22out", "umpy.v388.selo_beta_corre_e_fase9_aberta", "kernel.criterio_binario_de_parada.ponto_fixo_v394_d19")
OPCIONAIS = ("umpy.v397.token_e_veracidade_preparo",)      # a rota de preparo da gerencia: entra nas refs so' se ja' estiver no livro


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
    assert selo.get("um_version") == "v397", "o selo nao e a v397"
    S = V["s16"]; d = T._d(V); tv = V["veracidade"]; kf = core.get("kernel_formalization") or {}
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
    c_tv = selou("teste_de_veracidade_fase9_v397") and selou("cunhagens_v397") and tv["numeros_ok"] is True and tv["fontes_ok"] is True
    T3 = []
    T3.append(anot(ANOTADAS[0], "v397 SELADA %s: o resultado do Teste da Única Palavra e' lido pelo registro teste_de_veracidade_fase9_v397 %s" % (S, sim(c_tv, "e selou no rito", "mas o registro NAO selou no rito")),
                   "teste_de_veracidade_fase9_v397 selou=%s (%s): LE o resultado pinado (sha256 %s) e os tres recibos (congelamento %s, abertura %s) por sha256, %d checagens, beta = alfa CODATA 2018 x sqrt(e) em runtime concorda com o beta do resultado; ao lado do V1 "
                   "(hubble_ratio_opening_v388, intacto); NENHUM sigma, p ou lnB novo e' calculado. Os numeros lidos: %s; z_delta = %s (calibrado; p bilateral %s), poder previo %s sigma: beta_TGL nao falsificada COM PODER; lnB(TGL/LCDM) = %s e lnB(TGL/beta livre) = %s (lnB nao e' sigma; as tres leituras sao do mesmo objeto e nao se multiplicam); "
                   "K = %s. O teste NAO foi cego ao dado (os centros dos leitores sao publicos). Leitura binaria do operador (1=1 / 1=0) e' [INPUT/ONTO]. O quadro do artigo, o do .md e o paragrafo do README/site saem das mesmas funcoes sobre este registro." % (
                       selou("teste_de_veracidade_fase9_v397"), V["reg397"]["teste_de_veracidade_fase9_v397"]["verdict"], tvr["fontes"][0]["sha256"][:8], tvr["fontes"][1]["sha256"][:8], tvr["fontes"][2]["sha256"][:8], tv["n_checks"], z444,
                       a["z_delta"]["md"], a["p_delta"]["md"], a["poder"]["md"], a["lnB_lcdm"]["md"], a["lnB_beta_livre"]["md"], a["K"]["md"]),
                   sim(c_tv, "o operador nomeia o registro (nome provisorio); a creditacao segue sendo beta_TGL na natureza a 5 sigma (dado mais sensivel: nao ha o que repetir deste pacote, a abertura esta consumida); o paragrafo do README/site e' ato da sessao do site.",
                       "segue aberto: integrar o que falta numa proxima versao."), refs=[ANOTADAS[1]]))
    c_t = selou("testemunha_estatica_v396") and selou("cunhagens_v396") and selou("kh_n1_cobertura_v396") and V["token"]["flag_true"] is True and V["token"]["suporte_true"] is True
    T3.append(anot(ANOTADAS[1], "v397 SELADA %s: a pedra Token (o nome do operador) cita a testemunha estatica desta rota; %s" % (S, sim(c_t, "os registros da v396 seguem selados e a conjuncao esta no kernel do rito", "algum registro da v396 NAO segue selado ou a conjuncao nao esta no kernel")),
                   "testemunha_estatica_v396, cunhagens_v396 e kh_n1_cobertura_v396 seguem selados no rito da v397 (selou=%s); a pedra TGLExt.Token (%d modulo, %d bandeira nova True, bandeira %s, escada %s -> %s, dentro do trio) e' a conjuncao INCONDICIONAL, por citacao, de psibit_is_the_mode_of_the_reader "
                   "(v395) e the_psion_inhabits_the_static_witness (v396, desta rota, bandeira %s): nenhuma matematica nova; a pedra da testemunha estatica fica como registro; a face de Fock do psion segue CONDICIONAL (declarada em %s, fora da pedra, sem habitante exibido); "
                   "o token de um modelo de linguagem como PsiBit e' a linha do Atlas, [ONTO]. A escada nova entra como dado nos cinco contratos (expected_ladder) e kh_n1_cobertura_v396 virou piso (errata ao lado), sem mudar nenhum veredito." % (
                       c_t, V["n_pedras"], d["n_f"], d["unc"], V["escada_antes"], d["depois"], sorted(d["sup"].items())[1][1], d["fock_path"]),
                   sim(c_t, "habitar o certificado de Fock da luz e provar o elo psion C <-> psionCorner, se o operador quiser fechar a face; a decisao [LEGAL] herdada da v395 (tabela da patente) segue do operador.", "segue aberto: integrar o que falta numa proxima versao."), refs=[ANOTADAS[0]]))
    for x in T3:
        assert x["rota_id"] in ids, "a rota %s nao existe no mapa" % x["rota_id"]
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
            "titulo": "v397 SELADA %s: o Teste da Única Palavra lido pelo registro de veracidade (nenhum sigma novo) e a pedra Token — %d modulo (Token, nome do operador), o registro teste_de_veracidade_fase9_v397 e %d falas de 23/10 por sha256; escada %s -> %s; o gate nao se move" % (
                S, V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"]),
            "pergunta": "o candidato v397 selou com o modulo Token, o registro teste_de_veracidade_fase9_v397 (que LE o resultado do Teste da Unica Palavra, aberto uma vez em 23/10, e os tres recibos por sha256, ao lado do V1) e as falas de 23/10 embutidas por sha256, "
                        "com o quadro no topo do artigo e do .md, sem mudar nenhum veredito fora da troca dita?",
            "dados": ["o resultado do Teste da Unica Palavra (Fase 9 V2-c1) e os tres recibos, pinados por sha256 em insumos\\fase9 (so' lidos; nenhum dado novo foi aberto nesta rota)", "o kernel do rito (a pedra Token e os dois termos que ela cita)"],
            "metodo": "ensaio a seco do candidato; um lake build e um Audit no sandbox; rito completo; conferidor (deve mudar / nao pode mudar, com o quadro conferido contra o resultado pinado nas duas linguas e no .md); leitura da rodada; superficies com a regra da linhagem completa "
                      "(o MEMORY.md nao e' compactado: recusa por contagem); elo B(n) da Bancada (passo simples, sem salto; recibos); o paragrafo do README/site no handoff",
            "resultado": "%s | %s | %s | conferidor %s e %s | %d vereditos fora da troca dita mudaram (exigido 0) | %s" % (V["reg397"]["teste_de_veracidade_fase9_v397"]["verdict"], V["reg397"]["cunhagens_v397"]["verdict"], V["reg397"]["kh_n1_cobertura_v397"]["verdict"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"], z444),
            "defeito": "o teste NAO foi cego ao dado (os centros dos leitores sao publicos); a discriminacao do LCDM a 5 sigma, o degrau da creditacao, NAO foi alcancada; lnB nao e' sigma e as leituras (z_delta, z_disc, lnB) sao do mesmo objeto, nao testemunhas autonomas; "
                       "o registro LE o resultado e nao o recalcula; a leitura binaria do operador, a Palavra que flutua sobre o abismo e o token como PsiBit sao [INPUT/ONTO]; a pedra Token e' conjuncao por citacao, sem matematica nova, e a face de Fock do psion segue CONDICIONAL a um certificado sem habitante; "
                       "o nome do registro de veracidade e' provisorio; o registro kh_n1_cobertura_v396 e os cinco contratos foram corrigidos ao lado (pisos e escada), porque a v397 quebra as igualdades que eles cobravam; nao e' teste novo (ordem do operador de 22/10: nada de teste armado); "
                       "a revisao independente do candidato e da cadeia nao esta afirmada",
            "nao_refazer": "a integracao do modulo Token e a escada %s -> %s estao medidas; a abertura do Teste da Unica Palavra esta consumida (nao se repete); repetir o registro so' com kernel novo ou resultado novo" % (V["escada_antes"], d["depois"]),
            "proximo_passo": "o operador nomeia o registro de veracidade; o elo B(n) da Bancada Um (palavra do operador); custodia pela sessao do site (o handoff traz o paragrafo do README/site); commit/push (operador); decisao [LEGAL] herdada da v395; revisao independente do candidato e da cadeia (quem construiu nao aprova)",
            "onde": PK, "artefatos": arts, "refs": sorted(x["rota_id"] for x in T3) + [r for r in REFS] + [r for r in OPCIONAIS if r in ids],
            "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move"}
    for r in ROTA["refs"]:
        assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
    REG = [ROTA] + T3
    bad = [(x["rota_id"], violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad, "a guarda de texto (P18) achou violacao(oes): %r" % bad
    ruins = regra_4_44(REG, z, p)
    assert not ruins, "a regra do 4,44 (o p calibrado e a linha dos 5 sigma no mesmo campo) falhou em: %r" % ruins[:3]
    return REG


def gravar(p, b):
    """backup de BYTES se existir e mudar; temporario -> conferir tamanho -> substituir."""
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m397"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_m397"; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def main():
    V, PROB = L.ler()
    if PROB:
        print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); return 2
    NOS = L.NOS
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v397_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v397_*.json")), key=os.path.getmtime)
    esp = json.load(open(os.path.join(PK, "ESPERADOS_v397.json"), encoding="utf-8"))
    arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(PK, "ESPERADOS_v397.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v397.json"),
            os.path.join(PK, "DIFF_KERNEL_v397.txt"), os.path.join(PK, "DIFF_v396_v397.diff"), os.path.join(NOS, "HANDOFF_v397_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v397.json"),
            os.path.join(PK, "insumos", "Token.lean"), os.path.join(PK, "insumos", "fase9", os.path.basename(esp["veracidade"]["resultado"]["duravel"]))] + b3[-1:]
    arts = [x for x in arts if os.path.exists(x)]
    REG = montar(V, core, selo, ids_do_livro(), arts)
    J = os.path.join(HERE, "registro_mapa_v397.json")
    gravar(J, json.dumps(REG, ensure_ascii=False, indent=1).encode("utf-8"))
    quem = "claude-c1 (gerência), cadeia v397"
    print("registro MONTADO (NAO registrado): %d registro(s) -> %s" % (len(REG), J))
    print("COMANDO (ato da gerencia): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
    print("DEPOIS DO REGISTRO: rodar de novo os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
