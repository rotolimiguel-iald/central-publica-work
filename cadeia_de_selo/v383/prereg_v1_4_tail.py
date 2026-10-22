b = json.dumps(pre, ensure_ascii=False, indent=1).encode("utf-8")
if os.path.exists(SAIDA_JSON) or os.path.exists(SAIDA_MD):
    raise SystemExit("o pré-registro V1.4 já existe; não se reescreve: " + SAIDA_JSON)
tmp = SAIDA_JSON + ".tmp"; open(tmp, "wb").write(b); assert open(tmp, "rb").read() == b; os.replace(tmp, SAIDA_JSON)
hj = hashlib.sha256(b).hexdigest()
sn = lambda x: "sim" if x else "não"
L = ["# PRÉ-REGISTRO DOS DOIS LADOS — V1.4 — o estimando δ⟨K_∂⟩ (02/10/2026, noite)", "",
     ("**Identificador** `%s` · escrito em %s · JSON `%s` (sha256 `%s`) · base: `um.py` %s `%s` (custodiada) · SUPERSEDE o V1.3 (sha256 `%s`, mapa seq 282), o V1.2 (`%s`, seq 279), "
      "o V1.1 (`%s`, seq 276) e o V1 (`%s`, seq 275), antes de qualquer estimador ou dado NOVO, pela decisão do operador; os anteriores ficam como registro.") % (
         ID, pre["escrito_em"], os.path.basename(SAIDA_JSON), hj, selo.get("um_version"), um_sha[:16], ant_sha["v1_3"][:16], ant_sha["v1_2"][:16], ant_sha["v1_1"][:16], ant_sha["v1"][:16]), "",
     "**O operador (02/10, noite, verbatim):** «%s». E a decisão: «%s», sobre a opção da gerência: «%s»" % (VERB["nao_publicar_20261002"], VERB["decisao_20261002"], OPCAO_ESCOLHIDA), "",
     "**A v382** (`um.py` `%s`) foi selada SÓ no Nós e NÃO é custodiada: levava os nove pares do eco no livro, ao lado; a v383 a supera." % V382_SHA[:16], "",
     "**A chave do operador (verbatim):** «%s»" % VERB["chave_20261002"], "", "**A correção (verbatim):** «%s»; e a ordem: «%s»" % (VERB["otica_20261002"], VERB["prossiga_20261002"]), "",
     "**O estimando.** %s. A regra: β_TGL = α√e = %.12f (nunca literal); o custo no reflexo é β = |R|² = sin²θ_M; o pagamento na face é 1 − β = |T|² = cos²θ_M; |T|² + |R|² = 1. Onde incide: %s." % (pre["estimando"]["nome"], beta, pre["estimando"]["onde_incide"]), "",
     "**Os dois lados.** REFLEXO: %s. FACE: %s." % (LADOS["reflexo"], LADOS["face"]), "",
     "## As %d cobranças (UMA por lei de leitura; nenhuma move a regra; FALSIFIED só onde a lei do canal o admite — %d com canal futuro que o admite)" % (len(C), n_canal), "",
     "| id | lado | critério de lado | registro | como | desfecho lido | na regra | o que JÁ foi lido (core v381) | qualificador | cego (estimador / dado) | canal futuro com FALSIFIED | o que se pré-registra |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for c in C:
    L.append("| %s | %s | %s | %s | %s | `%s` | %s | %s | %s | %s / %s | %s | %s |" % (c["id"], c["lado"], c["criterio_de_lado"], c["registro"], c["como"], c["desfecho_lido"], "sim" if c["na_regra"] else "não (ao lado)",
                                                                                c["ja_lido"], c["qualificador"], sn(c["cego"]["estimador"]), sn(c["cego"]["dado"]), sn(c["canal_futuro_com_falsified"]), c["futuro"]))
L += ["", "Contagem do livro: %s · na regra (%d): %s · ao lado (%d): %s." % (
          ", ".join("%s %d" % kv for kv in contagem.items()), len(pre["na_regra"]), ", ".join("%s %d" % kv for kv in contagem_na_regra.items() if kv[1]), len(pre["ao_lado"]), ", ".join(pre["ao_lado"])), "",
      "## As %d rotas examinadas FORA do livro (o eco como cópia atrasada; NÃO são cobranças da teoria) — %d excluídas pelos dados, %d inconclusivas" % (
          rotas_cont["rotas"], rotas_cont["excluidas_pelos_dados"], rotas_cont["inconclusivas"]), "",
      pre["rotas_regra"] + ".", "",
      "| rota | antes (V1.3) | par (amplitude, lei de atraso) | estado | o que foi lido | qualificador | a amplitude e o seu estatuto | a lei de atraso e o seu estatuto |", "|---|---|---|---|---|---|---|---|"]
for r in ROTAS:
    L.append("| %s | %s | %s | `%s` | %s | %s | %s | %s |" % (r["id"], r["id_no_v1_3"], r["par"], r["estado"], r["ja_lido"], r["qualificador"], r["amplitude"]["estatuto"], r["lei_de_atraso"]["texto_e_estatuto"]))
L += ["", "**O motivo comum (lido das fontes):** o eco como cópia atrasada está fora da cadeia — «%s»; a definição do operador de 16/09 fica — «%s»; as três leis de atraso nomeiam a massa do remanescente, "
      "e a leitura R6 ratificada diz «%s» [a ligação é DERIVED de leitura, gerência]; a errata da lei KMS: «%s»." % (FORA_DA_CADEIA, DEF_16SET, R6_RATIFICADA, GWECO05), "",
      "## Pendentes", ""] + ["- %s" % x for x in pre["pendentes"]]
L += ["", "## Regras de leitura — as da Fase 6 e das emendas V4/V5 (lidas dos arquivos, na ordem; governam o rótulo citado das rotas) e os acréscimos da casa (ditos como tais)", ""]
for k, v in pre["regras_de_leitura"].items():
    if k == "desfechos":
        continue
    if isinstance(v, list):
        L.append("- **%s:**" % k); L += ["  - %s" % x for x in v]
    else:
        L.append("- **%s:** %s" % (k, v))
L += ["", "Fontes das regras (sha256): %s." % "; ".join("%s `%s`" % (k, v[:16]) for k, v in pre["fontes_das_regras"].items()), "",
      "## Cegueira", "", "%s. Declaração: %s. Cego quanto ao estimador: %s. Cego quanto ao dado: %s. %s." % (pre["cegueira"]["sentido"], pre["cegueira"]["declaracao"], ", ".join(pre["cegueira"]["cego_quanto_ao_estimador"]) or "nenhum",
                                                                                                         ", ".join(pre["cegueira"]["cego_quanto_ao_dado"]) or "nenhum", pre["cegueira"]["o_que_nao_foi_feito"]), "",
      "## Ordem", ""] + ["%d. %s" % (i + 1, s) for i, s in enumerate(pre["ordem"])]
L += ["", "Estatuto: %s. PROVADA ≠ CONFIRMADA; `NOT_FALSIFIED` nunca é `CONFIRMED`." % pre["estimando"]["estatuto"], ""]
bm = "\n".join(L).encode("utf-8")
tmp = SAIDA_MD + ".tmp"; open(tmp, "wb").write(bm); assert open(tmp, "rb").read() == bm; os.replace(tmp, SAIDA_MD)
hm = hashlib.sha256(bm).hexdigest()
print("pré-registro V1.4 gravado:", SAIDA_JSON, "sha256", hj); print("md:", SAIDA_MD, "sha256", hm)
print("contagem do livro:", contagem, "| na regra:", contagem_na_regra, "| rotas fora do livro:", rotas_cont, "| canal futuro com FALSIFIED:", n_canal)
r = subprocess.run([sys.executable, os.path.join(BU, "ferramentas", "publicar_relatorio.py"), "02/10 — Pré-registro dos dois lados V1.4 (11 cobranças; os nove pares do eco fora do livro, como rotas examinadas; supersede o V1.3 pela decisão do operador)", SAIDA_MD],
                   capture_output=True, text=True, encoding="utf-8")
print(r.stdout.strip()); assert r.returncode == 0, r.stderr
out = rotas.registrar([dict(tipo="ERRATA", corrige=282, rota_id="bancada.preregistro_dois_lados_delta_k", status="PROPOSTA", estatuto="REAL", olhou_dados=False,
                            titulo=("V1.4 SUPERSEDE o V1.3 (seq 282) ANTES de qualquer estimador ou dado novo, pela decisão do operador («%s»): os nove pares do eco como cópia atrasada NÃO são cobranças "
                                    "da teoria -- saem do livro e passam a rotas examinadas fora do livro, com os números e o motivo lidos das fontes; as onze cobranças não mudam de desfecho; base v381 custodiada") % VERB["decisao_20261002"],
                            resultado="V1.4 gravado (JSON sha256 %s; MD sha256 %s); livro %s; na regra %s; rotas fora do livro %s; canal futuro com FALSIFIED %d; publicado na aba Relatórios; o V1.3 (sha256 %s) fica como registro" % (
                                hj[:16], hm[:16], json.dumps(contagem, ensure_ascii=False), json.dumps(contagem_na_regra, ensure_ascii=False), json.dumps(rotas_cont, ensure_ascii=False), n_canal, ant_sha["v1_3"][:16]),
                            nao_refazer="não contar os pares do eco como cobranças da teoria; não publicar a v382",
                            proximo_passo="um.py v383 lê o V1.4 por hash; depois os pendentes (a lei transmitida nos cronômetros; o estimador da propagação R2) com o poder dito antes de abrir",
                            artefatos=[SAIDA_JSON, SAIDA_MD], refs=["kernel.regra_matriz.cadeia_unica"])],
                      "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
print("inscrito no mapa: seq", out["gravados"][0]["seq"], "cabeça", out["cabeca"][:16])
