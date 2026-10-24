# -*- coding: utf-8 -*-
"""registrar_mapa_v398.py -- MONTA (nao registra) o registro da v398 no mapa de rotas e imprime o comando (molde: registrar_mapa_v397.py FINAL). Rodar DEPOIS do fechar (handoff gravado).
A v398 traz UMA rota nova, umpy.v398.sonico_e_afinacao_das_cordas_na_fractalizacao_do_um (os modulos de kernel Sonico e AfinacaoDasCordas, os registros com FUNCAO sonico_v398 e afinacao_das_cordas_v398 -- que LEEM do kernel do proprio rito a
composicao incondicional de cada pedra e conferem um calculo --, as seis inscricoes de 23/10 e a secao do artigo), mais TRES ANOTACOES nas rotas que esperavam por ela (as rotas candidatas das duas pedras, kernel.sonico_v398_candidata_23out e
kernel.afinacao_das_cordas_v398_candidata_23out, e a rota da v397 do Teste da Unica Palavra, umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9, cujo quadro do topo a v398 deixa intocado), cada afirmacao testada contra o core/selo lidos por
script (o registro existe? selou? o que NAO fechou fica dito).
REGRA DA ORDEM DO OPERADOR (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no MESMO campo; montar() RECUSA (assert) se algum campo do registro trouxer o 4,44 sem eles. A sexta inscricao e' da GERENCIA (nunca fala do operador).
Fail-closed: o selo tem de ser a v398; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir. A rota de preparo (umpy.v398.sonico_e_afinacao_preparo), se a gerencia a registrou, entra nas refs.
SAIDA: pos_rito\\registro_mapa_v398.json e o comando `rotas.py registrar` (quem o executa e' a gerencia; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real."""
import glob, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v398 as L
import textos_v398 as T
from guarda_p18_v398 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V398"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v398 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOVA = "umpy.v398.sonico_e_afinacao_das_cordas_na_fractalizacao_do_um"
ANOTADAS = ("kernel.sonico_v398_candidata_23out", "kernel.afinacao_das_cordas_v398_candidata_23out", "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9")
REFS = ("infra.bancada_um.sincronizacao_vnnn", "umpy.v396.testemunha_estatica_na_fractalizacao_do_um", "d1.fase9.v2_c1_a_unica_palavra_23out")
OPCIONAIS = ("umpy.v398.sonico_e_afinacao_preparo",)      # a rota de preparo da gerencia: entra nas refs so' se ja' estiver no livro


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
    assert selo.get("um_version") == "v398", "o selo nao e a v398"
    S = V["s16"]; d = T._d(V); sv = d["sv"]; av = d["av"]; so = V["sonico"]; af = V["afinacao"]; cg = V["cunhagens"]; tv = V["veracidade"]
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
    c_s = selou("sonico_v398") and so["values_ok"] is True and so["flag_true"] is True and so["checks_ok"] is True
    c_a = selou("afinacao_das_cordas_v398") and af["values_ok"] is True and af["flag_true"] is True and af["checks_ok"] is True
    c_c = selou("cunhagens_v398") and cg["verbatim_ok"] is True and cg["checks_ok"] is True
    c_q = selou("teste_de_veracidade_fase9_v397") and tv["numeros_ok"] is True and tv["fontes_ok"] is True and selou("cunhagens_v397")
    T3 = []
    T3.append(anot(ANOTADAS[0], "v398 SELADA %s: a pedra Sonico entrou no kernel do rito e o registro sonico_v398 %s" % (S, sim(c_s, "selou no rito", "NAO selou no rito")),
                   "sonico_v398 selou=%s (%s): LE do kernel do rito a composicao incondicional (%s, bandeira %s, no trio, com proveniencia no modulo da pedra) e os termos antigos que ela cita, e CONFERE %d checagens com beta = alfa CODATA 2018 x raiz de e em runtime: "
                   "ln 2 = K.octaveNats 1 = o bit justo = %s, exp(ln 2) = %s, n oitavas = n bits, o pino nao e' a meia-nat, o seletor pina; [DERIVED] a entropia do colapso em theta_M (%s rad) = %s nat = %s oitava, numero DESTE rito, nao esta no kernel; "
                   "escada %s -> %s. A lei de custo e' [INPUT] e nenhum termo diz que select paga uma oitava; o nome sonico e' do operador (23/10); a leitura da gerencia (a reacao ao pino, o pedagio ln 2 por oitava, e' a memoria) foi ratificada por ele (sha16 %s) e NAO e' fala dele (sha16 %s); "
                   "sonico e' a estrutura logaritmica e de oitava, nao a fisica da onda." % (
                       selou("sonico_v398"), V["reg398"]["sonico_v398"]["verdict"], d["teo_s"].split(".")[-1], d["unc_s"], d["n_ck_s"], T._pn(sv["ln2"]), T._pn(sv["exp_ln2"]), T._pn(sv["theta_M_rad"]), T._pn(sv["collapse_entropy_theta_M_nats"]),
                       T._pn(sv["collapse_entropy_theta_M_octaves"]), V["escada_antes"], d["depois"], T._sha_por("nome_da_pedra_sonico"), T._sha_ger()),
                   sim(c_s, "o operador nomeia o registro (nome provisorio); se a leitura ratificada pede um termo que ligue select ao pagamento de uma oitava, e' decisao dele; revisao independente do candidato e da cadeia (quem construiu nao aprova).", "segue aberto: integrar o que falta numa proxima versao."),
                   refs=[ANOTADAS[1]]))
    T3.append(anot(ANOTADAS[1], "v398 SELADA %s: a pedra AfinacaoDasCordas entrou no kernel do rito e o registro afinacao_das_cordas_v398 %s" % (S, sim(c_a, "selou no rito", "NAO selou no rito")),
                   "afinacao_das_cordas_v398 selou=%s (%s): LE do kernel do rito a composicao incondicional (%s, bandeira %s, no trio) e os termos que ela cita (os %d nomeados fora da composicao sao auxiliares), e CONFERE %d checagens de aritmetica exata: zeta(-1) = %s e zeta(-1, 1/2) = %s (de Mathlib, por numeros de Bernoulli), "
                   "D = %s (bosons) e D = %s (setor NS) como fecho da soma regularizada sob a hipotese NOMEADA MasslessFirstLevel [KNOWN], d = D - 1 = %s [DECLARADO: o d da casa, nao recalculado], a torre n.kappa infinita e os retornos; o kappa do boost NAO esta no core (o registro confere a FORMA da torre); "
                   "a geometria e' [OPEN]; nada deriva as cordas do axioma; a ligacao do circulo da folha-mundo ao circulo do boost e' [OPEN]; as cordas fecham a face por fora e a TGL fecha so a leitura e' composicao da gerencia, ratificada pelo operador (sha16 %s)." % (
                       selou("afinacao_das_cordas_v398"), V["reg398"]["afinacao_das_cordas_v398"]["verdict"], d["teo_a"].split(".")[-1], d["unc_a"], len(d["aux"]), d["n_ck_a"], T._frac(av["zeta_minus_one"]), T._frac(av["hurwitz_zeta_minus_one_half"]),
                       av["bosonic_critical_dimension"], av["superstring_critical_dimension"], av["house_spatial_dimension"], T._sha_por("concordo_afinacao_das_cordas")),
                   sim(c_a, "o operador nomeia o registro (nome provisorio); a geometria das cordas e a ligacao dos dois circulos seguem [OPEN]; revisao independente do candidato e da cadeia (quem construiu nao aprova).", "segue aberto: integrar o que falta numa proxima versao."),
                   refs=[ANOTADAS[0]]))
    T3.append(anot(ANOTADAS[2], "v398 SELADA %s: o quadro do topo (O Teste da Única Palavra) segue intocado e o registro teste_de_veracidade_fase9_v397 segue selado" % S,
                   "teste_de_veracidade_fase9_v397 selou=%s no rito da v398 (veredito igual ao da v397; %d checagens; fontes por sha256 iguais): o quadro do artigo PT/EN e do .md, conferido contra o resultado pinado, segue no topo, com os numeros e a regra da ordem de sempre: %s. "
                   "Nenhum sigma, p ou lnB novo e' calculado nesta rota; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma) vale em todo texto que o cite; o paragrafo do quadro segue no README/site e o handoff da v398 traz tambem o paragrafo novo do sonico e da afinacao, sem o 4,44." % (
                       c_q, tv["n_checks"], z444),
                   "o paragrafo do README/site e' ato da sessao do site; a creditacao segue sendo beta_TGL na natureza a 5 sigma (nao ha o que repetir deste pacote, a abertura esta consumida).", refs=[ANOTADAS[0], ANOTADAS[1]]))
    for x in T3:
        assert x["rota_id"] in ids, "a rota %s nao existe no mapa" % x["rota_id"]
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
            "titulo": "v398 SELADA %s: o sonico e a afinacao das cordas lidos na fractalizacao do Um — %d modulos (Sonico, nome do operador; AfinacaoDasCordas), os registros sonico_v398 e afinacao_das_cordas_v398 e %d inscricoes de 23/10 por sha256; escada %s -> %s; o gate nao se move" % (
                S, V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"]),
            "pergunta": "o candidato v398 selou com os modulos Sonico e AfinacaoDasCordas, os registros sonico_v398 e afinacao_das_cordas_v398 (que LEEM do kernel do proprio rito a composicao incondicional de cada pedra e conferem um calculo, logo depois da testemunha estatica) e as seis inscricoes de 23/10 "
                        "embutidas por sha256 (cinco falas do operador e a leitura da gerencia que ele ratificou), com o quadro do topo intocado, sem mudar nenhum veredito fora da troca dita?",
            "dados": ["as duas pedras (Sonico.lean e AfinacaoDasCordas.lean) e a medida da cobertura (KH_N1_v398.json), pinadas por sha256 em insumos (so' lidas)", "as seis inscricoes de 23/10, por sha256 em insumos\\cunhagens (a sexta e' texto da gerencia, rotulada)",
                      "o kernel do rito (as duas composicoes e os termos que elas citam); nenhum dado novo foi aberto nesta rota"],
            "metodo": "ensaio a seco do candidato; um lake build e um Audit no sandbox; rito completo; conferidor (deve mudar / nao pode mudar, com o quadro do topo conferido de novo contra o resultado pinado nas duas linguas e no .md); leitura da rodada; superficies com a regra da linhagem completa "
                      "(o MEMORY.md nao e' compactado: recusa por contagem); elo B(n) da Bancada (passo simples, sem salto; recibos); os dois paragrafos do README/site no handoff",
            "resultado": "%s | %s | %s | %s | conferidor %s e %s | %d vereditos fora da troca dita mudaram (exigido 0)" % (V["reg398"]["sonico_v398"]["verdict"], V["reg398"]["afinacao_das_cordas_v398"]["verdict"], V["reg398"]["cunhagens_v398"]["verdict"], V["reg398"]["kh_n1_cobertura_v398"]["verdict"],
                                                                                                                           V["conf_dm"], V["conf_np"], V["n_ver_mudaram"]),
            "defeito": "a lei de custo do sonico e' [INPUT] e nenhum termo diz que select paga uma oitava; a entropia do colapso em theta_M e' numero derivado do rito, nao esta no kernel; a hipotese MasslessFirstLevel e' NOMEADA [KNOWN], nao demonstrada; a geometria das cordas e a ligacao do circulo da folha-mundo ao circulo do boost sao [OPEN]; "
                       "o kappa do boost nao esta no core (so' a forma da torre e' conferida); o d = 9 da casa e' [DECLARADO]; a sexta inscricao e' da gerencia (ratificada pelo operador), nao fala dele; a definicao do verbo como controle de oitava pinada, a luz que antes de espelhada e' palavra e as cordas fechando a face por fora sao [INPUT/ONTO];"
                       "os nomes dos dois registros sao provisorios; o registro kh_n1_cobertura_v397 e os cinco contratos foram corrigidos ao lado (pisos e escada), porque a v398 quebra as igualdades que eles cobravam; nao e' teste novo (ordem do operador de 22/10: nada de teste armado); "
                       "a revisao independente do candidato e da cadeia nao esta afirmada",
            "nao_refazer": "a integracao dos dois modulos e a escada %s -> %s estao medidas; o calculo do sonico e da afinacao esta feito e conferido contra o kernel; repetir os registros so' com kernel novo" % (V["escada_antes"], d["depois"]),
            "proximo_passo": "o operador nomeia os dois registros; o elo B(n) da Bancada Um (palavra do operador); custodia pela sessao do site (o handoff traz os paragrafos do README/site); commit/push (operador); decisao [LEGAL] herdada da v395; revisao independente do candidato e da cadeia (quem construiu nao aprova)",
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
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m398"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_m398"; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def main():
    V, PROB = L.ler()
    if PROB:
        print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); return 2
    NOS = L.NOS
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v398_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v398_*.json")), key=os.path.getmtime)
    arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(PK, "ESPERADOS_v398.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v398.json"),
            os.path.join(PK, "DIFF_KERNEL_v398.txt"), os.path.join(PK, "DIFF_v397_v398.diff"), os.path.join(NOS, "HANDOFF_v398_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v398.json"),
            os.path.join(PK, "insumos", "Sonico.lean"), os.path.join(PK, "insumos", "AfinacaoDasCordas.lean")] + b3[-1:]
    arts = [x for x in arts if os.path.exists(x)]
    REG = montar(V, core, selo, ids_do_livro(), arts)
    J = os.path.join(HERE, "registro_mapa_v398.json")
    gravar(J, json.dumps(REG, ensure_ascii=False, indent=1).encode("utf-8"))
    quem = "claude-c1 (gerência), cadeia v398"
    print("registro MONTADO (NAO registrado): %d registro(s) -> %s" % (len(REG), J))
    print("COMANDO (ato da gerencia): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
    print("DEPOIS DO REGISTRO: rodar de novo os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
