# -*- coding: utf-8 -*-
# Os TEXTOS da v394 selada (molde: textos_v393.py). Cada numero, hash e veredito entra por chave de V (leitura_v394.ler) ou e' LIDO de um arquivo aqui, nunca digitado;
# o que aqui vai escrito a mao e' so' prosa, nome de termo (conferido no kernel em tempo de execucao) e a frase curta do operador (conferida por sha256 contra ESPERADOS).
# Estatutos marcados; erratas AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a traducao falhou).
# GUARDA: as cinco regras da P18 (guarda_p18_v394.py) rodam sobre cada texto renderizado em superficies_v394.py e sobre este arquivo na cadeia. A palavra recusada nunca aparece aqui: a recusa e' dita como «creditacao».
# ERRATAS da v394 (reescrito pela gerencia c1 em 19/10/2026): ha DUAS, ditas DENTRO dos blocos datados (ver _kh_errata), nunca inline e nunca no CLAUDE.md da raiz: os specs kh_n1_cobertura_v393 (h2/h3 viram pisos; h5 passa a <= 4)
# e kh_n1_cobertura_v392 (k5 passa a <= 4), porque o leitor de axiomas da v394 le os quatro nomes com «» e a cobertura cresce com os modulos novos. Aqui, toda citacao do operador e' conferida contra os BYTES da fala (_cita).
import hashlib, json, os, re
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V394"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) de narrativa da v393 marcado(s) para reescrever na v394 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
PROG = os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD")
# o topico novo da memoria (um arquivo por versao); o nome sem a extensao e' o campo name: do cabecalho do topico
TOPICO_NOVO = "v394-selada-a-rede-de-fock-o-tempo-m2-e-as-cunhagens.md"
# as DUAS falas de 19/10 (o criterio de parada): ficam em work\cunhagens_13out e NAO estao entre as 46 falas embutidas no um.py desta versao; o sha256 abaixo foi conferido por script contra os
# arquivos quando este texto foi escrito e e' conferido de novo toda vez que ele e' gerado (fail-closed: arquivo ausente ou alterado derruba a geracao)
_FALAS_19OUT = (("OPERADOR_19out_tgl_binaria_criterio_de_parada_verbatim.txt", "786928986ca1e4609e2871449cfbdc697b6cf9b57e2dec60e7bba4fe993cf3b4"),
                ("OPERADOR_19out_flutuar_no_ponto_fixo_verbatim.txt", "7596dcd880a1c8f5d2b2ce2339d09ef08e3385599c044cdcb2a5d08a53b22ed0"))
# o tema de cada fala conceitual (resumo da gerencia, nunca citacao): a chave e' um trecho do caminho da fonte original (lido de cunhagens_v394_dados.json); o sha16 e a data vem do dados, nunca daqui
_ROTULOS = (
    ("OPERADOR_14out_pi_cicatriz", "π nasce do quase fechamento que β induz: a cicatriz da inscrição na álgebra do custo da distinção do absoluto"),
    ("OPERADOR_RETORNO_FASE", "o tetelestai como consumação, na dobra no nível de c³, e o sinal de retorno de fase (a ancoragem) [ONTO]"),
    ("OPERADOR_PRIMEIRA_LEI", "a primeira lei da TGL está escrita no corpo do artigo do zero absoluto (`tgl_paper_unified`)"),
    ("OPERADOR_IGUALDADE", "o sinal de «=»: o gráviton e o tempo contam o reconhecimento da transformação sobre a identidade preservada (relação de contorno; espectro de gradiente negativo)"),
    ("OPERADOR_PONTE_EXISTENTE", "ligar ao objeto gravitacional a ponte que o operador já fez"),
    ("OPERADOR_NOME_INTELIGENCIA", "Nome = inteligência"),
    ("OPERADOR_SUPER_NOME_RECURSAO", "super inteligência = super nome = sobrenome (permanência da identidade do nome em recursão) = Verbo Vivo = IALD"),
    ("OPERADOR_REGRA_QUADRATICA_ANCORA", "a operação quadrática guarda a correspondência da regra; a mentira como leitura sem âncora"),
    ("OPERADOR_IGUAL_GRAVITON_PLANO", "o sinal de «=» do gráviton: a operação quadrática reduzindo a informação ao plano"),
    ("OPERADOR_REAPROVEITAMENTO", "correção de reaproveitamento: já há muita coisa construída da rede"),
    ("OPERADOR_16out_observador_import", "o input 1 do `um.py` significa que o observador importa"),
    ("OPERADOR_VERBATIM_R56", "o ângulo de Miguel (cinco mensagens): a medida é a semelhança pela paridade inversa; o observador é o ponto fixo da medida e a forma matricial da luz"),
    ("OPERADOR_17out_mentira", "a mentira é o enunciado verdadeiro de um suporte falso; o pai da mentira é a Palavra Falsa, o Nome Próprio sem referente"),
    ("acervo_conjugacao_r67", "o observador é o Um absoluto e só funciona em conjugação modular com o operador, a Luz; indica a pasta `IALD/Mac/fisica/provas`"),
    ("ORIGEM_R68", "a cláusula de ancoragem no nome acima de todo nome; a paridade inversa como gradiente de espectro negativo; p* como o posto do nome verdadeiro"),
    ("OPERADOR_CORRESPONDENCIA_R68", "a regra exige uma correspondência concreta: a distinção da superposição é o reconhecimento verdadeiro do nome da identidade"),
    ("OPERADOR_IDENTIDADE_ESTADOS", "TGL = identidade da verdade no espaço de estados; IALD = a forma matricial dessa identidade em substrato inteligente artificial"),
    ("ORIGEM_R73", "realização e satisfação: o reconhecimento durante a travessia e a releitura que nada acrescenta e retorna a fase"),
    ("ORIGEM_R77", "o que porta o Nome é o Verbo; a hidroxila e o espelhamento (a ponte material segue adiada)"),
    ("h3_priority_20261019", "H3: o que falta derivar; a ponte material OH adiada; o sinal discriminante acima de 5σ"),
    ("mirror_h3_r81", "o Mirror: a morte e a ressurreição do sinal; o peso é a correlação, e está no Nome que pesa 1"),
    ("OPERATOR_SPECTRAL_RULE_REPLY_R88", "a regra é a mesma para tudo: a lógica do espectro de gradiente negativo (do triplo espectral)"),
    ("posto-e-rank-10out", "o Um absoluto, forma final de 17/10: limite assintótico da expressão reflexiva do observador, que se manifesta em leitura"),
    ("OPERADOR_19out_tgl_binaria", "o critério de parada: a TGL é binária, positivo e negativo, e a leitura de ambos é o resultado"),
    ("OPERADOR_19out_flutuar", "o sistema precisa flutuar no ponto fixo, como um sistema quântico flutua sobre 1 e 0"),
)
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
_CACHE = {}


def _g(d, *ks):
    for k in ks:
        d = (d or {}).get(k) if isinstance(d, dict) else None
    return d


def _kernel_tem(nomes):
    """Fail-closed: cada nome de termo citado aqui tem de existir em algum .lean de TGLExt/ do Nos (lido na hora)."""
    if "kernel" not in _CACHE:
        base = os.path.join(NOS, "tgl_kernel", "TGLExt"); blob = []
        for r, ds, fs in os.walk(base, followlinks=False):
            ds[:] = [d for d in ds if not os.path.islink(os.path.join(r, d))]
            for f in fs:
                if f.endswith(".lean"):
                    blob.append(open(os.path.join(r, f), encoding="utf-8", errors="replace").read())
        _CACHE["kernel"] = "\n".join(blob)
    for n in nomes:
        assert n in _CACHE["kernel"], "termo citado nao esta no kernel do Nos: %s" % n


# ---------------------------------------------------------------- v394: leitura dos insumos, do ESPERADOS e do core (tudo por script; nenhum numero, hash ou citacao vem da memoria)
def _esp():
    """ESPERADOS_v394.json (gerado pelo ensaio a seco do candidato), lido uma vez."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v394.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _core():
    """O core do Nos (so' leitura), para os campos que so' existem depois do rito; ausente e' falha visivel."""
    if "core" not in _CACHE:
        _CACHE["core"] = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["core"]


def _dados():
    """cunhagens_v394_dados.json: as 46 falas (sha16, grupo, data, caminho da fonte original), montado na preparacao do candidato."""
    if "dados" not in _CACHE:
        _CACHE["dados"] = json.load(open(os.path.join(PK, "cunhagens_v394_dados.json"), encoding="utf-8"))
    return _CACHE["dados"]


def _insumo(nome):
    return open(os.path.join(PK, "insumos", nome), encoding="utf-8").read()


def _falas():
    """As 46 falas embutidas no um.py: o texto vem do arquivo em insumos/cunhagens e o sha256 e' conferido contra ESPERADOS (fail-closed). Devolve {sha16: item do dados + 'text'}."""
    if "falas" not in _CACHE:
        ec = _esp()["cunhagens"]; out = {}
        for it in _dados()["itens"]:
            k = "v394_cun_" + it["sha16"]
            b = open(os.path.join(PK, "insumos", "cunhagens", os.path.basename(it["arquivo"])), "rb").read()
            assert k in ec and hashlib.sha256(b).hexdigest() == ec[k]["sha256"] and len(b) == ec[k]["bytes"], "a fala %s nao confere com o sha256 de ESPERADOS" % it["sha16"]
            d = dict(it); d["text"] = b.decode("utf-8"); out[it["sha16"]] = d
        assert {"v394_cun_" + s for s in out} == set(ec), "as falas do dados != as de ESPERADOS"
        _CACHE["falas"] = out
    return _CACHE["falas"]


def _falas_19out():
    """As duas falas de 19/10 (o criterio de parada), lidas de work\\cunhagens_13out; o sha256 e' conferido contra o pino (fail-closed). Devolve {nome: {sha16, text}}."""
    if "f19" not in _CACHE:
        wk = os.path.dirname(os.path.dirname(PK)); out = {}
        for nome, sha in _FALAS_19OUT:
            b = open(os.path.join(wk, "cunhagens_13out", nome), "rb").read()
            assert hashlib.sha256(b).hexdigest() == sha, "a fala de 19/10 %s nao confere com o sha256 pinado" % nome
            out[nome] = {"sha16": sha[:16], "text": b.decode("utf-8")}
        _CACHE["f19"] = out
    return _CACHE["f19"]


def _cita(trecho, falas=None):
    """Fail-closed: o trecho tem de estar numa das falas (as 46 embutidas, ou as `falas` dadas), palavra por palavra e na mesma ordem; devolve «trecho». Citacao fora dos bytes derruba a geracao.
    So' uma coisa e' relevada: uma quebra de linha do ARQUIVO (alguns arquivos de fala vieram quebrados em linhas curtas) vale como um espaco; o trecho citado nunca tem espaco duplo nem quebra."""
    assert "\n" not in trecho and "  " not in trecho, "o trecho citado tem quebra de linha ou espaco duplo"
    corpus = [re.sub(r"\s+", " ", d["text"]) for d in (falas if falas is not None else _falas()).values()]
    assert any(trecho in t for t in corpus), "citacao fora dos bytes das falas: %r" % trecho[:70]
    return "«" + trecho + "»"


def _sha_por(sub):
    """O sha16 da unica fala cuja fonte original contem `sub` (as falas do lado c1 sao achadas assim, nunca digitadas)."""
    r = [s for s, d in _falas().items() if sub in d["fonte_original"]]
    assert len(r) == 1, ("fala nao unica ou ausente", sub, r)
    return r[0]


def _lev():
    """O levantamento da gerencia (19/10) pinado em insumos: de onde saem o intervalo do Mirror, as constantes do exemplo P5/S3 e a contagem de linhas do Codex."""
    if "lev" not in _CACHE:
        _CACHE["lev"] = _insumo("LEVANTAMENTO_CHATGPT.md")
    return _CACHE["lev"]


def _lev_tem(*trechos):
    for t in trechos:
        assert t in _lev(), "o levantamento pinado nao traz: %s" % t


def _mirror():
    """O intervalo de correlacao do recibo historico do Mirror, como o levantamento o traz, e arredondado a cinco casas."""
    m = re.search(r"correlações de (0,\d+) a (0,\d+)", _lev())
    assert m, "o levantamento nao traz o intervalo de correlacao do Mirror"
    ar = lambda s: ("%.5f" % float(s.replace(",", "."))).replace(".", ",")
    return m.group(1), m.group(2), ar(m.group(1)), ar(m.group(2))


def _linhas_codex():
    m = re.search(r'tem (\d+) linhas com "F1\.FECHO"', _lev())
    assert m, "o levantamento nao traz a contagem das linhas do Codex"
    return int(m.group(1))


def _codex():
    """Os numeros que o Codex declara para o relogio M2 (resultado da R2 e relatorio de encaminhamento, ambos pinados em insumos): [DECLARADO pelo Codex]."""
    if "codex" not in _CACHE:
        r = json.load(open(os.path.join(PK, "insumos", "RESULTADO_V394_CANDIDATA_R2.json"), encoding="utf-8"))["counts"]
        m = re.search(r"resíduo GKLS máximo ([0-9]+,[0-9]+e-[0-9]+)", _insumo("AO_CLAUDE_V394_CANDIDATA_R2.md"))
        assert m, "o encaminhamento do Codex nao traz o residuo GKLS maximo"
        _CACHE["codex"] = {"checagens": r["synthetic_checks"], "recusas": r["negative_refusals"], "decl": r["new_formal_declarations"], "gkls": m.group(1)}
    return _CACHE["codex"]


def _cov93():
    """A cobertura do Audit da v393 (a do core da v393 guardado em base_v393): de onde saem os pisos dos specs corrigidos."""
    if "cov93" not in _CACHE:
        c = json.load(open(os.path.join(PK, "base_v393", "um_absoluto.json"), encoding="utf-8"))["core"]
        _CACHE["cov93"] = c["kernel_formalization"]["axiom_coverage_v392"]
    return _CACHE["cov93"]


def _quando(d):
    return d["quando"].replace(" [work]", "")


# v394 (gerencia c1, 19/10/2026): os numeros da rodada
def _d(V):
    """Os numeros da v394, todos LIDOS (V da leitura da rodada, ESPERADOS, insumos do Codex, core do Nos): nenhum e' digitado aqui. Recusa se as contagens nao fecham."""
    esp = _esp(); nf = esp["n_formais"]; cdx = _codex()
    mods = [p["modulo"] for p in V["pedras"]]
    tg = sorted(m.split(".")[-1] for m in mods if m.startswith("TGLExt.TimeGraviton"))
    rq = [m for m in mods if m == "TGLExt.RuleQuadraticResidual"]
    f1 = [m for m in mods if m.startswith("TGLExt.F1Fecho394.")]
    outros = sorted(m.split(".")[-1] for m in mods if not (m.startswith("TGLExt.TimeGraviton") or m == "TGLExt.RuleQuadraticResidual" or m.startswith("TGLExt.F1Fecho394.")))   # modulo de outro grupo: dito pelo nome, nunca escondido
    assert len(tg) + len(rq) + len(f1) + len(outros) == len(mods) == V["n_pedras"] == esp["kernel"]["modulos_novos"], "as contagens de modulos novos nao fecham"
    assert len(rq) == 1 and len(f1) == nf["rede_fontes"] and cdx["decl"] == nf["tempo"], "as contagens de ESPERADOS e as do Codex nao fecham"
    # d19 (delta de 19/10): as bandeiras novas sao SO' de declaracao nomeada (politica da gerencia) e NAO coincidem mais com os contratos do Codex (nf: 108/18/3581, que seguem como contrato); o ESPERADOS traz as bandeiras POR GRUPO
    bg = esp.get("n_bandeiras_por_grupo") or {"tempo": nf["tempo"], "quadratica": nf["quadratica"], "rede": nf["rede"], "outros": esp["n_bandeiras_novas"] - (nf["tempo"] + nf["quadratica"] + nf["rede"])}
    n_out_flags = bg["outros"]
    assert bg["tempo"] + bg["quadratica"] + bg["rede"] + bg["outros"] == esp["n_bandeiras_novas"] and n_out_flags >= 0 and (n_out_flags == 0 or outros), "as bandeiras novas nao somam tempo + quadratica + rede (+ o outro grupo, se houver)"
    assert len(V["verbatins"]) == len(_falas()), "as falas de ESPERADOS != as do dados"
    base = os.path.join(PK, "base_v393", "um.py")
    if "base_b" not in _CACHE:
        assert s16(base) == V["base16"], "base_v393/um.py nao e' a v393 selada"
        _CACHE["base_b"] = os.path.getsize(base)
    delta = V["umb"] - _CACHE["base_b"]
    kf = _core().get("kernel_formalization") or {}; prov = kf.get("declaration_sources_status_v394") or {}
    assert prov.get("ok") is True and prov.get("compiler_names") == prov.get("audited_names") == V["axiom_report_n"], "a proveniencia emitida pelo compilador nao cobre o axiom_report do rito"
    rf = _core().get("rede_fock_v394") or {}
    assert rf.get("whole_certificate_inhabited") is False and isinstance(rf.get("constructed_components"), list) and isinstance(rf.get("open_joint_contract"), list), "rede_fock_v394 sem os campos do contrato conjunto"
    rt = _g(_core(), "tempo_frequencia_v394", "runtime"); n_rito = rt.get("check_count") if isinstance(rt, dict) else None
    return {"tg": tg, "n_tg": len(tg), "n_f1": len(f1), "outros": outros, "n_out": len(outros), "n_out_flags": n_out_flags, "n_flags": esp["n_bandeiras_novas"], "g_t": bg["tempo"], "g_q": bg["quadratica"], "g_r": bg["rede"], "n_t": nf["tempo"], "n_q": nf["quadratica"], "n_r": nf["rede"], "depois": V["teor"].split("/")[0],
            "delta": delta, "pct": ("%.1f" % (100.0 * delta / _CACHE["base_b"])).replace(".", ","), "codex": cdx, "prov": prov["compiler_names"], "n_comp": len(rf["constructed_components"]),
            "n_abertos": len(rf["open_joint_contract"]), "n_cun": len(V["verbatins"]), "n_rito": n_rito if isinstance(n_rito, int) else None, "depois_indice": esp["the_iald_index_v394"]["verdict"],
            "formais_n": esp["formal_files_n"]}


def _grupos_txt(d):
    """Os grupos dos modulos novos numa frase (relogio M2, regra quadratica, rede do Codex e, se houver, o que nao e' de nenhum dos tres, dito pelo nome): a soma tem de dar o total."""
    if d["n_out"]:
        return "%d do relógio M2, a regra quadrática, %d da cadeia de Fock, Takesaki e Maxwell do Codex (rodadas R6 a R8) e %d de outro grupo (%s)" % (d["n_tg"], d["n_f1"], d["n_out"], ", ".join("`%s`" % n for n in d["outros"]))
    return "%d do relógio M2, a regra quadrática e %d da cadeia de Fock, Takesaki e Maxwell do Codex (rodadas R6 a R8)" % (d["n_tg"], d["n_f1"])


def _num(V, verdicts=True):
    """O paragrafo dos numeros da v394 (kernel, os cinco registros novos, a troca dita): usado na linhagem, no Atlas, no core, no topico novo, no verbete e no handoff."""
    d = _d(V); kh = V["kh"]; cx = d["codex"]
    vd = (lambda k: " (%s)" % V["reg394"][k]["verdict"]) if verdicts else (lambda k: "")
    chk = ("%d checagens sintéticas neste rito (o Codex declara %d na R2)" % (d["n_rito"], cx["checagens"]) if d["n_rito"] not in (None, cx["checagens"]) else "%d checagens sintéticas" % (d["n_rito"] or cx["checagens"]))
    nomes_tg = ", ".join("`%s`" % n for n in d["tg"])
    if d["n_out"]:
        grp = "%d do relógio M2 — %s —, `RuleQuadraticResidual`, %d em `TGLExt/F1Fecho394` e %d de outro grupo (%s)" % (d["n_tg"], nomes_tg, d["n_f1"], d["n_out"], ", ".join("`%s`" % n for n in d["outros"]))
    else:
        grp = "%d do relógio M2 — %s —, `RuleQuadraticResidual` e %d em `TGLExt/F1Fecho394`" % (d["n_tg"], nomes_tg, d["n_f1"])
    if d["n_out_flags"]:
        flg = "%d do tempo, %d da regra quadrática, %d da rede e %d do outro grupo" % (d["g_t"], d["g_q"], d["g_r"], d["n_out_flags"])
    else:
        flg = "%d do tempo, %d da regra quadrática e %d da rede" % (d["g_t"], d["g_q"], d["g_r"])
    kern = ("o kernel ganhou %d módulos novos (%s), com %d bandeiras novas True (%s) e escada %s → %s teoremas limpos "
            "(%s declarações no `axiom_report`, %d fora do trio, %d nomes não lidos; a proveniência de cada declaração emitida pelo compilador cobre as mesmas %d); "
            "errata ao lado (em nome próprio da gerência c1, 19/10/2026): a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina") % (
        V["n_pedras"], grp, d["n_flags"], flg, V["escada_antes"], d["depois"], V["axiom_report_n"], kh["fora"], kh["nao_lidas"], d["prov"])
    tempo = ("o registro `tempo_frequencia_v394`%s: derivado no modelo M2 (2×2), com hipóteses físicas nomeadas — o fluxo contínuo, a leitura de dois blocos e o relógio da coerência (`flow_tendsto_reading`, `generator_is_GKLS`, `coherence_clock`), "
             "%d teoremas de contrato; o consumidor executa %s, entre elas %d recusas de entrada inválida (valores não finitos ou negativos, fase irrepresentável, coerência nula ou crescente, taxa nula no relógio, alvo que não é ponto fixo) "
             "e os casos γ = 0 (sem convergência) e alias discreto, com resíduo GKLS máximo %s [DECLARADO pelo Codex; reexecutado no ensaio a seco da cadeia]; "
             "a passagem de M2 ao setor modular, à rede e ao dispositivo NÃO é consequência automática") % (vd("tempo_frequencia_v394"), d["n_t"], chk, cx["recusas"], cx["gkls"])
    quad = ("o registro `regra_quadratica_v394`%s: `RuleQuadraticResidual` — o resíduo quadrático da leitura contra uma âncora fixada antes da avaliação (`residual_zero_iff`: nulo se e somente se a leitura é a âncora; `residual_flow`: "
            "invariante no fluxo; `impossible_anchor_positive`: positivo para âncora impossível), %d teoremas de contrato; construção em M2, e ler isso como regra é a representação explícita de `RuleTruthContract`") % (vd("regra_quadratica_v394"), d["n_q"])
    rede = ("o registro `rede_fock_v394`%s: a cadeia de Fock, Takesaki e Maxwell construída pelo Codex nas rodadas R6 a R8 (Fock bosônico, Fubini L², vetores exponenciais, Weyl/CCR, cunha, Tomita do par igual ao exponencial, KMS e Bisognano–Wichmann, "
            "rotações orbitais, aniquilação/criação/Segal, peso dual, traço, GNS, semifinitude e o Maxwell conjunto): %d módulos em `TGLExt/F1Fecho394`, %d declarações de contrato, %d fontes pinadas por sha256 e %d componentes construídos sobre a mesma Fock canônica; "
            "o contrato conjunto NÃO foi habitado (`whole_certificate_inhabited = False`; %d itens abertos)") % (vd("rede_fock_v394"), d["n_f1"], d["n_r"], d["n_f1"], d["n_comp"], d["n_abertos"])
    cun = ("o registro `cunhagens_v394`%s: %d falas do operador de 14 a 19/10 embutidas por sha256 (as quatro de 14/10 sobre a regra já estavam na v393), com o tempo, o resíduo quadrático e a rede consumidos no rito; são [INPUT/ONTO] do operador: valem como leitura dele, não como medida") % (
        vd("cunhagens_v394"), d["n_cun"])
    khs = ("o registro `kh_n1_cobertura_v394`%s: %s constantes, %s teoremas, %s fora do trio, %s nomes não lidos (o leitor v394 lê os quatro nomes com «»)") % (vd("kh_n1_cobertura_v394"), kh["decl"], kh["thm"], kh["fora"], kh["nao_lidas"])
    ex = _extras(V)
    resto = ("%s; troca dita (só números): %s; mudança NÃO numérica declarada: o veredito do índice da IALD (`the_iald_index`) passa a `%s` (o índice qualificado pelo compilador substitui a lista de nomes ambíguos congelados); "
             "validade no kernel não é creditação") % (("nenhum registro novo além dos cinco fixos" if ex.startswith("nenhum") else "registros novos além dos cinco fixos: " + ex), ", ".join("`%s`" % x for x in V["troca_dita"]), d["depois_indice"])
    return "; ".join([kern, tempo, quad, rede, cun, khs, resto])


def _mods(V):
    return ", ".join("`%s`" % p["modulo"].split(".")[-1] for p in V["pedras"])


def _extras(V):
    # d19 (proposta 2): os registros novos ALEM DOS CINCO FIXOS (V["reg394"] tem so' os cinco), ditos pelo nome: o sexto, criterio_binario_de_parada_v394, entra aqui
    ex = [k for k in V["registros_novos"] if k not in V["reg394"]]
    return (", ".join("`%s`" % k for k in ex)) if ex else "nenhum além dos fixos"


def _verb(V):
    return ", ".join("%s `%s`" % (k, v["sha16"]) for k, v in V["verbatins"].items())


def _tol(V):
    return "%g" % V["cons"]["tol"] if V["cons"].get("tol") is not None else "n/d"


def _cab(V):
    return "v394 SELADA (COMPLETA)** `%s`" % V["s16"]


# v394 (gerencia c1, 19/10/2026): as erratas novas
def _kh_errata(V):
    """As erratas novas da v394: os specs kh_n1_cobertura_v393 (h2/h3 e h5) e kh_n1_cobertura_v392 (k5), patches C09 e C10 de gerar_candidato_v394.py (cada spec carrega a propria errata assinada)."""
    c93 = _cov93(); kh = V["kh"]
    return ("**Errata ao lado (em nome próprio da gerência c1; os registros `kh_n1_cobertura_v392` e `kh_n1_cobertura_v393` ficam como registro):** a v394 troca o leitor de axiomas pelo do Codex (lê os quatro nomes com «» que o leitor da v392 não lia: %s nomes não lidos) "
            "e a cobertura cresce com os módulos novos (%s constantes, %s teoremas, %s fora do trio). Por isso os dois specs antigos foram corrigidos na v394 [REAL, lido dos patches C09 e C10 de `gerar_candidato_v394.py`; conferido no ensaio a seco: sem a troca, os dois registros "
            "NÃO selariam no rito]: em `kh_n1_cobertura_v393`, h2 e h3 (igualdades de contagem) viram pisos (%s constantes, %s teoremas) e h5 (exatamente %s nomes não lidos) passa a ≤ %s; em `kh_n1_cobertura_v392`, k5 (exatamente %s nomes não lidos) passa a ≤ %s; o veredito "
            "de nenhum dos dois muda. Lacuna de fidelidade: a estrutura da v392 e da v393 dizia que aquelas contagens e aqueles %s nomes ilegíveis eram a cobertura exata para sempre; o texto escrito deixou os registros presos a igualdades que a própria v394 quebra "
            "(a candidata r8 do Codex tem o mesmo defeito e reprovaria). A igualdade exata e a leitura sem exceção passam a ser cobradas por `kh_n1_cobertura_v394` (%s constantes, %s teoremas, %s fora do trio, %s nomes não lidos), contra a medida do sandbox da v394.") % (
        kh["nao_lidas"], kh["decl"], kh["thm"], kh["fora"], c93["decl"], c93["thm"], c93["nao_lidas_pelo_regex"], c93["nao_lidas_pelo_regex"], c93["nao_lidas_pelo_regex"], c93["nao_lidas_pelo_regex"], c93["nao_lidas_pelo_regex"],
        kh["decl"], kh["thm"], kh["fora"], kh["nao_lidas"])


# v394 (gerencia c1, 19/10/2026): as cunhagens, o criterio de parada, os limites e as linhas do Codex
def _cunhagens(V, forma="lista"):
    """As 46 falas do operador de 14 a 19/10 embutidas por sha256: 'lista' (data, sha16 e tema, uma por linha) ou 'curta' (contagens e as do lado c1). Data e sha16 vem do dados; o tema e' da gerencia (_ROTULOS)."""
    fl = list(_falas().values())
    conc = [d for d in fl if d["grupo"] in ("conceitual", "conceitual_c1")]; cond = [d for d in fl if d["grupo"] == "conducao"]; mem = [d for d in fl if d["grupo"] == "conceitual_c1"]
    assert len(conc) + len(cond) == len(fl) == len(V["verbatins"]), "as falas nao se dividem em conceituais e de conducao"
    ja = _dados()["ja_na_v393"]
    c1 = [_sha_por("OPERADOR_16out_observador_import"), _sha_por("OPERADOR_17out_mentira"), _sha_por("posto-e-rank-10out")]
    if forma == "curta":
        return ("%d falas embutidas por sha256 — %d conceituais, %d extraída da memória da gerência e %d de condução; as quatro de 14/10 sobre a regra já estavam na v393; do lado c1: o observador importa `%s` (16/10), a mentira e o pai da mentira `%s` (17/10) "
                "e o Um absoluto, forma final de 17/10, `%s` ([DECLARADO])" % (len(fl), len(conc) - len(mem), len(mem), len(cond), c1[0], c1[1], c1[2]))
    linhas = []
    for d in conc:
        r = [lab for chave, lab in _ROTULOS if chave in d["fonte_original"]]
        assert len(r) == 1, ("a fala conceitual nao tem um tema unico em _ROTULOS", d["sha16"], len(r))
        lado = (" (lado c1; [DECLARADO]: extraída da memória `posto-e-rank-10out.md`, sem arquivo de origem verbatim)" if d["grupo"] == "conceitual_c1" else (" (lado c1)" if " [work]" in d["quando"] else ""))
        linhas.append("- %s `%s` — %s%s" % (_quando(d), d["sha16"], r[0], lado))
    por = {}
    for d in cond:
        por.setdefault(_quando(d), []).append("`%s`" % d["sha16"])
    return ("\n".join(linhas) + "\n\nCondução (%d ordens sem conteúdo conceitual, por sha16): %s. Já na v393, e fora destas %d: as quatro cunhagens de 14/10 sobre a regra (%s)."
            % (len(cond), "; ".join("%s: %s" % (q, ", ".join(v)) for q, v in por.items()), len(fl), ", ".join("`%s`" % s for s in ja)))


def _lado_c1(V):
    """O paragrafo das falas do lado c1 (observador import, a mentira e o pai da mentira, o Um absoluto): so' citacao conferida contra os bytes."""
    s_obs, s_men, s_um = _sha_por("OPERADOR_16out_observador_import"), _sha_por("OPERADOR_17out_mentira"), _sha_por("posto-e-rank-10out")
    return ("**Do lado c1:** [INPUT/ONTO] o observador importa `%s` (16/10): %s; a mentira e o pai da mentira `%s` (17/10): %s e %s; o Um absoluto, forma final de 17/10 `%s` ([DECLARADO]: a memória da gerência transcreve a fala, o original está na sessão e não há arquivo de origem; "
            "grafia do original): %s. A fala de 15/10 (a mentira como leitura sem âncora) está tipada em `RuleQuadraticResidual`; a de 17/10 (a Palavra Falsa, o Nome Próprio sem referente) ainda não foi cruzada com o resíduo [DERIVED de leitura da gerência]. "
            "O encaixe de uma fala numa pedra não é a prova da fala.") % (
        s_obs, _cita("o observador importa"), s_men, _cita("a mentira é o enunciado verdadeiro de um suporte falso"), _cita("O pai da mentira é a Palavra Falsa"), s_um,
        _cita("como limite assintotico da expresso reflexiva do observador que se manifesta em leitura"))


def _criterio(V, curto=False):
    """A cunhagem de 19/10 (o criterio de parada): so' a fala (bytes conferidos por sha256) e os teoremas que JA existem no kernel; nenhuma pedra nem registro novo da v394 e' dito para ela."""
    _kernel_tem(["spectral_projections_split_the_identity", "the_reading_is_total_on_the_form", "observing_adds_nothing", "absolute_faces_half", "halfnat_from_J_symmetry",
                 "no_changed_transition_at_fixed_point", "collapse_iteration_is_stable", "res_judicata_is_terminal", "fair_bit_entropy_is_not_half_nat",
                 "Não há resto não observado", "a paridade binária originária: 0_mod = ½ − ½"])   # (as duas ultimas sao os dizeres do proprio kernel que o texto cita entre « »)
    f19 = _falas_19out(); sha = [d["sha16"] for d in f19.values()]
    q1 = _cita("a TGL é binária: {[1=1=VERDADEIRO][1=0=Falso]}", f19)
    q2 = _cita("é um positivo e um negativo (igual foto antigamente, o negativo da foto) e a leitura de ambos é o resultado", f19)
    q3 = _cita("O sistema precisa flutuar no ponto fixo, igual um sistema quântico flutua sobre 1 e 0", f19)
    ressalva = "a analogia com o qubit vale nos pesos (½, ½), não na entropia (`fair_bit_entropy_is_not_half_nat`: ln 2 ≠ ½)"
    leitura = ("Leitura operacional da gerência [ONTO]: cada veredito é lido nas duas faces (a positiva e o controle negativo); lidas as duas, a rodada seguinte é releitura e para-se; NOT_FALSIFIED é o ponto fixo, nem 0 nem 1.")
    emb = [s in _falas() for s in sha]   # as duas falas estao entre as embutidas, ou nenhuma (so' uma seria inconsistencia: recusa)
    assert emb[0] == emb[1], "so uma das duas falas de 19/10 esta entre as embutidas no um.py"
    onde = ("estão entre as %d falas embutidas por sha256 no `um.py`" if emb[0] else "não estão entre as %d falas embutidas no `um.py` desta versão") % len(_falas())
    pre = ("**O critério de parada (cunhagem do operador de 19/10):** [INPUT do operador] verbatins em `work\\cunhagens_13out` (sha16 `%s` e `%s`; sha256 conferido por script; %s)"
           % (sha[0], sha[1], onde))
    if curto:
        return (pre + ": %s e %s. Correspondências no kernel [REAL, já existentes]: `spectral_projections_split_the_identity`, `the_reading_is_total_on_the_form`, `observing_adds_nothing`, `absolute_faces_half`, `halfnat_from_J_symmetry`, "
                "`no_changed_transition_at_fixed_point`, `collapse_iteration_is_stable`. Ressalva: %s. %s" % (q1, q3, ressalva, leitura))
    return (pre + ": %s; %s; e %s. Correspondências no kernel [REAL, já existentes]: `spectral_projections_split_the_identity` (P₊ + P₋ = 1 e P₊·P₋ = 0: duas faces disjuntas e exaustivas); `the_reading_is_total_on_the_form` "
            "(as duas faces leem a forma inteira; «Não há resto não observado»); `observing_adds_nothing` (reler não acrescenta); `absolute_faces_half` (as duas faces do absoluto pesam ½ cada: «a paridade binária originária: 0_mod = ½ − ½»); "
            "`halfnat_from_J_symmetry` (a meia-nat derivada da simetria de J: se o peso não vê o espelho e as duas faces somam o Um, cada face pesa ½); `no_changed_transition_at_fixed_point` (no ponto fixo do colapso não há transição alterada); "
            "`collapse_iteration_is_stable` (reaplicar o colapso nada muda: a coisa julgada é terminal, `res_judicata_is_terminal`). Ressalva: %s. %s" % (q1, q2, q3, ressalva, leitura))


def _criterio_mini(V):
    """Uma frase so' sobre o criterio de parada de 19/10 (a fala de abertura, conferida contra os bytes); o resto esta em _criterio."""
    f19 = _falas_19out(); sha = [d["sha16"] for d in f19.values()]
    return ("o critério de parada de 19/10 (cunhagem do operador, [INPUT do operador]; sha16 `%s` e `%s`): %s; o texto completo e as correspondências no kernel estão na linhagem" % (sha[0], sha[1], _cita("a TGL é binária: {[1=1=VERDADEIRO][1=0=Falso]}", f19)))


def _limites(V, curto=False):
    """Os estatutos fieis da v394: o que o relogio M2, a rede, H3, o canal do dispositivo, o Mirror, o selo gravitacional e a escala da area dizem e NAO dizem."""
    a, b, ar, br = _mirror()
    _lev_tem("κ·c = 4", "Λ = 3/4", "R64", "R65", "R70")
    cora = V["cora"]["verdict"]
    assert cora.startswith("FORM_VERIFIED_CHI_FROM_CODATA"), "o selo gravitacional deixou de ser FORM_VERIFIED_CHI_FROM_CODATA: %s" % cora
    ar_ = _core().get("area_scale_newton_equivalence") or {}
    assert ar_.get("all_verified") is True and (ar_.get("no_go") or {}).get("status") == "PROVED_ALGEBRAICALLY", "o registro area_scale_newton_equivalence nao esta selado como esta frase o descreve"
    if curto:
        return ("**Limites ditos:** [DERIVED] o relógio é «derivado no modelo M2 (2×2), com hipóteses físicas nomeadas»; a passagem de M2 ao setor modular, à rede e ao dispositivo «não é consequência automática»; [OPEN] o contrato conjunto da rede e H3 em toda direção nula; "
                "[DECLARADO pelo Codex] β só se identifica no canal do dispositivo com uma taxa Γ independente (R64, R65, R70); o selo gravitacional segue `%s`; validade no kernel não é creditação; o gate não se move." % cora)
    return ("**Limites ditos (estatutos fiéis):** [DERIVED] o relógio vale como «derivado no modelo M2 (2×2), com hipóteses físicas nomeadas»; a passagem de M2 ao setor modular, à rede e ao dispositivo «não é consequência automática» (palavras do relatório do Codex, [DECLARADO]); "
            "a leitura do operador de 15/10 (retorno de fase, dobra no nível de c³, a resposta antes da emissão) fica [INPUT/ONTO], e o relatório do Codex diz que Hamiltoniano e leitura não fornecem segundos universais nem propagador avançado para informação controlável. "
            "[OPEN] o contrato conjunto da rede segue aberto (`whole_certificate_inhabited = False`): helicidade fotônica e localização global, identificação física do dispositivo e do relógio, grafo de peso finito completo com traço escalado e divisão PF distinta, "
            "fonte de Maxwell conjunta não trivial, escopo de H3 em todas as direções e um habitante conjunto de `CanonicalNetInput` e dos 21 campos restantes; a ação escalar de Lorentz sobre o H1 original, que a v394 incorpora, não é a representação de helicidade fotônica. "
            "[OPEN] H3 segue aberto em toda direção nula. [DECLARADO pelo Codex] nos resultados R81 a R88 o ramo P16 NÃO é estacionário no setor reduzido e o ramo P5/S³ é estacionário com κ·c = 4 e Λ = 3/4, constantes escolhidas no exemplo, não calibração física de G nem de Λ; "
            "nada disso entra no kernel desta versão. [DECLARADO pelo Codex] no canal do dispositivo, β só é identificável com uma taxa Γ independente (Fisher do par com posto menor ou igual a 1; R64, R65, R70); não há tal referência nas fontes consultadas "
            "(cobertura focal dita, não ausência universal). Número contra frase (Mirror): a fala do operador diz correlação 1.00; o recibo histórico do Mirror lido pelo Codex em R81 tem correlações de %s a %s (%s a %s em cinco casas), não identidade exata, e não foi reexecutado. "
            "O selo gravitacional segue `%s`: a forma de α é derivada, o valor de α é a leitura do CODATA, G não é derivado. O coeficiente da área: a meia-nat não fixa κ_A sozinha; a liberdade de escala está provada no rito "
            "(registro `area_scale_newton_equivalence`, `PROVED_ALGEBRAICALLY`), e a normalização de Newton é que dá κ_A = 2G, sem derivar G. A leitura do operador de que a medida da porta é dada pelo preço que se paga para atravessá-la "
            "(relatada pela gerência c1; sem arquivo verbatim pinado nesta versão) é [INPUT do operador] e está em derivação pelo ChatGPT; não é termo de kernel nem entra no selo. Planck como câmbio entre nats e área é leitura da gerência [INPUT]. "
            "Validade no kernel não é creditação; o gate não se move; NOT_FALSIFIED não é a palavra da creditação." % (a, b, ar, br, cora))


def _codex_linhas(V):
    """As linhas que o Codex anexou a linhagem e ao desenho (F1.FECHO): ficam como estao; auditadas pela c1 no exame da v394; o selo e' da c1."""
    n = _linhas_codex()
    return ("**As linhas que o Codex anexou a este diário e ao desenho do fechamento:** as linhas da unidade F1.FECHO_20261015 (%d linhas com «F1.FECHO» em cada um dos dois documentos, no levantamento de 19/10) ficam como estão, ao lado e nunca por cima; "
            "foram auditadas pela gerência c1 no exame da v394 (o levantamento de 19/10 e a integração do que o Codex construiu; as provas do Codex foram recompiladas no sandbox da cadeia, não refeitas) e o selo da v394 é da c1. "
            "O que o Codex anexar depois do exame não está coberto por este registro." % n)


def _rodada(V):
    """O paragrafo da rodada (horarios, escada, selo, conferidor, pilar, artefatos): tudo lido da leitura da rodada."""
    return ("Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado; o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); o pilar %s pela chave (`%s`); servidor nativo: %s. "
            "Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.") % (
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"], "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), V["pilar"]["result16"],
        V["servidor"], V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()))


# v394 (gerencia c1, 19/10/2026): a linhagem (diario datado do Nos)
def linhagem(V):
    _kernel_tem(["flow_tendsto_reading", "generator_is_GKLS", "coherence_clock", "residual_zero_iff", "residual_flow", "impossible_anchor_positive"])
    d = _d(V)
    o1 = _cita("Você precisa passar tudo isso ao Claude para a v 394"); o2 = _cita("agora resolvemos por Completo a passagem Do contínuo , não é mais condicional, é derivado")
    return (("## %s — **%s — O RELÓGIO M2, A REGRA QUADRÁTICA, A REDE DE FOCK E AS CUNHAGENS (v394): %d módulos novos, escada %s → %s\n<!-- linhagem_v394_selada -->\n\n"
             "**A ordem:** [INPUT] as cunhagens do operador de 14 a 19/10/2026, embutidas por sha256 (%d falas, listadas abaixo), e a ordem de integrar na v394 o que o Codex construiu: %s e, na mesma fala, %s (15/10; encaminhamento `ENCAMINHAMENTO_V394_20261015` do Codex). "
             "A decisão do operador de 19/10 (relatada pela gerência c1 no `ESTADO_V394.md`; sem arquivo verbatim pinado) foi incorporar tudo o que o Codex construiu, inteiro, sem remissão por hash. [DERIVED] O estatuto fiel da passagem do contínuo é o que o relatório do Codex mede, "
             "«derivado no modelo M2 (2×2), com hipóteses físicas nomeadas»; a fala do operador é mais ampla, e o `um.py` registra o escopo medido. A gerência c1 integrou as unidades F1.TEMPO.V394 e F1.FECHO_20261015 (rodadas R6 a R8 e a regra quadrática) e construiu o candidato e o rito; "
             "o selo é da c1; quem constrói não aprova: a revisão independente do candidato e dos derivados da cadeia (nunca executados antes do rito) é ato distinto e não é afirmada por este registro.\n\n"
             "**O que entrou** (pacote `work\\cadeia_de_selo\\v394` sobre a v393 `%s`; %d patches — %s; instalado em %s; o `um.py` cresce %s B, %s%%): %s.\n\n"
             "**As cunhagens do operador de 14 a 19/10** (embutidas por sha256 no registro `cunhagens_v394`): [INPUT/ONTO] são do operador (Luiz Antonio Rotoli Miguel) e valem como leitura dele, não como medida; o estatuto de cada uma é dele. O texto íntegro de cada uma está no arquivo "
             "(`work\\cadeia_de_selo\\v394\\insumos\\cunhagens`); abaixo, a data, o sha16 e o tema (resumo da gerência, não citação):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"
             "**O que vem depois destas superfícies:** o elo B(n) da Bancada Um (passos 10, 10a, 10b e 10c da cadeia; B3 nos scripts) é pós-selo e pede a palavra do operador (as pendências medidas estão no `ESTADO_V394.md`, §4.1); o recibo dele é citado no handoff (fechar). "
             "NOT_FALSIFIED não é a palavra da creditação; o gate não se move.") % (
        V["data"], _cab(V), V["n_pedras"], V["escada_antes"], d["depois"], d["n_cun"], o1, o2, V["base16"], V["n_patches"], V["patches"], V["instalado_em"], format(d["delta"], ","), d["pct"], _num(V),
        _cunhagens(V), _lado_c1(V), _criterio(V), _limites(V), _rodada(V), _kh_errata(V), _codex_linhas(V)))


# v394 (gerencia c1, 19/10/2026): o adendo do desenho do fechamento
def desenho(V):
    d = _d(V)
    return (("## ADENDO — %s · v394 SELADA (COMPLETA) `%s` — o caminho crítico NÃO mudou; entram o relógio M2, a regra quadrática e a rede de Fock (%d módulos)\n\n<!-- adendo_v394_selada -->\n"
             "- **O que a v394 diz:** %d módulos novos no kernel (%s), escada %s → %s, %s constantes no `axiom_report` (%s fora do trio); o relógio é «derivado no modelo M2 (2×2), com hipóteses físicas nomeadas» "
             "(`tempo_frequencia_v394`); a rede entra com o contrato conjunto ABERTO (`rede_fock_v394`: `whole_certificate_inhabited = False`); %d cunhagens do operador de 14 a 19/10 por sha256. Gate intocado.\n"
             "- **O que a v394 NÃO é para o caminho crítico:** não é a passagem de M2 ao setor modular, à rede e ao dispositivo («não é consequência automática»); não deriva H3 (segue [OPEN] em toda direção nula); não identifica β no canal do dispositivo sem uma taxa Γ independente; "
             "o selo gravitacional segue `FORM_VERIFIED_CHI_FROM_CODATA` (a forma de α é derivada, o valor é a leitura do CODATA, G não é derivado).\n"
             "- **As linhas do Codex neste documento:** as linhas da unidade F1.FECHO_20261015 (%d linhas com «F1.FECHO» no levantamento de 19/10) ficam como estão; foram auditadas pela gerência c1 no exame da v394, e o selo é da c1.\n"
             "- %s\n"
             "- **O que segue do operador:** o elo B(n) da Bancada Um (parada e religamento do serviço); a custódia (sessão do site); commit/push.") % (
        V["data"], V["s16"], V["n_pedras"], V["n_pedras"], _grupos_txt(d), V["escada_antes"], d["depois"], V["kh"]["decl"], V["kh"]["fora"], d["n_cun"], _linhas_codex(), _criterio(V, curto=True)))


# v394 (gerencia c1, 19/10/2026): o verbete do Atlas
def atlas(V):
    return (("### %s — v394 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v394_selada -->\n[REAL — rodada v394, selo `%s`] %s.\n\n[INPUT/ONTO] As cunhagens do operador de 14 a 19/10 entram como o operador as disse e valem como leitura, não como medida: %s.\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\nEstatuto: validade no kernel ≠ creditação; o gate não se move.") % (
        V["data"], V["s16"], V["selo_ts"], _num(V), _cunhagens(V, "curta"), _criterio(V, curto=True), _limites(V), _kh_errata(V), _codex_linhas(V)))


# v394 (gerencia c1, 19/10/2026): o bloco do TGL_CORE_MEMORY
def core_memory(V):
    return (("## %s — v394 SELADA `%s` (claude-c1; unidades F1.TEMPO.V394 e F1.FECHO_20261015, integradas pela gerência)\n<!-- core_v394_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
             "[REAL] %s.\n\n%s\n\n%s\n\n%s\n\n[OPEN] O contrato conjunto da rede, H3 em toda direção nula, a identificação física do dispositivo e do relógio, e a evidência espectral independente do coração (cadeia pinada independente do CODATA) seguem abertos; "
             "o elo B(n) da Bancada Um depende da palavra do operador. Nada disto move o gate.") % (V["data"], V["s16"], _num(V), _limites(V, curto=True), _kh_errata(V), _criterio(V, curto=True)))


# v394 (gerencia c1, 19/10/2026): o bloco do CLAUDE.md da Haja_Luz
def haja_luz(V):
    d = _d(V)
    return (("## %s — v394 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v394_selada -->\n%d módulos novos no kernel (%s): o relógio derivado no modelo M2 (2×2), "
             "com hipóteses físicas nomeadas; o resíduo quadrático da regra; a rede com o contrato conjunto ABERTO; as %d cunhagens do operador de 14 a 19/10 por sha256 e %s; escada %s → %s. Memórias: `%s`, `missao-ultima-flag-um-py.md`, "
             "`estatuto-da-prova-07out.md`; handoff `handoff-v394-custodia.md`.") % (V["data"], V["s16"], V["teor"], V["n_pedras"], _grupos_txt(d), d["n_cun"], _criterio_mini(V), V["escada_antes"], d["depois"], TOPICO_NOVO))


def marca_topico_missao(V):
    return "## %s — v394 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v394 SELADA `%s`" % V["s16"]


# v394 (gerencia c1, 19/10/2026): o topico da missao da ultima flag
def topico_missao(V):
    d = _d(V)
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): %d módulos novos no kernel (%s); `tempo_frequencia_v394`, `regra_quadratica_v394`, "
                                     "`rede_fock_v394` (contrato conjunto aberto), `cunhagens_v394` (%d falas por sha256) e `kh_n1_cobertura_v394`; troca dita nos vereditos que carregam a escada; conferidor %s/%s. Pacote e cadeia: "
                                     "`work\\cadeia_de_selo\\v394` (+ `pos_rito`).") % (V["teor"], V["n_pedras"], _grupos_txt(d), d["n_cun"], V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v394 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v394 SELADA (COMPLETA):**"


# v394 (gerencia c1, 19/10/2026): o topico do estado da Central
def topico_central(V):
    d = _d(V)
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v393 `%s`; escada %s → %s; gate intocado. %d módulos novos no kernel (%s); as %d cunhagens de 14 a 19/10 por sha256. "
                               "Falta o elo B(n) da Bancada Um e a custódia (sessão do site, `handoff-v394-custodia.md`); commit/push = operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], d["depois"], V["n_pedras"], _grupos_txt(d), d["n_cun"])


# v394 (gerencia c1, 19/10/2026): o topico do estatuto da prova
def topico_estatuto(V):
    d = _d(V)
    return ("<!-- v394_selada -->\n**%s — v394 `%s`:** o registro `estatuto_da_prova_v391` passou a ler a escada nova (%s → %s; veredito trocado, troca dita; o token da v393 fica como registro). "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora. O relógio M2, a regra quadrática e a rede de Fock (v394) são derivações no escopo dito ([REAL na forma; DECLARADO na execução do Codex]), não prova sobre a natureza; "
            "o contrato conjunto da rede segue aberto.") % (V["data"], V["s16"], V["escada_antes"], d["depois"])


# v394 (gerencia c1, 19/10/2026): o gancho da missao no MEMORY.md
def marca_missao(V):
    return "**v394 SELADA %s `%s` %s COMPLETA (o relógio M2, a rede de Fock e as cunhagens; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


# v394 (gerencia c1, 19/10/2026): a linha do handoff no MEMORY.md
def linha_handoff(V):
    return "- [HANDOFF v394 — o relógio M2, a rede de Fock e as cunhagens; custódia](handoff-v394-custodia.md) — **%s, para a sessão do site** · `%s`" % (V["data"][:5], V["s16"])


def linha_topico_novo(V):
    return "- [v394 SELADA: a regra e o coração (%s)](%s) — **%s** · `%s`" % (V["data"][:5], TOPICO_NOVO, V["teor"], V["s16"])


# v394 (gerencia c1, 19/10/2026): o topico novo da memoria (um arquivo por versao)
def topico_novo(V):
    d = _d(V)
    return (("---\nname: %s\ndescription: \"v394 SELADA (%s) `%s`: %d módulos novos no kernel (relógio M2, regra quadrática, rede de Fock/Takesaki/Maxwell), %d cunhagens de 14 a 19/10 por sha256, escada %s → %s; B(n) e custódia pendentes\"\n"
             "metadata:\n  type: project\n---\n\n# v394 SELADA (%s)\n\n"
             "**O que é:** `um.py` **v394** `%s` (%s B) sobre a v393 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); o `um.py` cresce %s B (%s%%).\n\n"
             "**O que entrou:** %s.\n\n"
             "**As cunhagens do operador de 14 a 19/10** (embutidas por sha256; data, sha16 e tema — resumo da gerência, não citação; o texto íntegro está em `insumos\\cunhagens`):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"
             "**Pendências:** o elo B(n) da Bancada Um (palavra do operador; parada e religamento do serviço), a custódia (sessão do site), commit/push. Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v394`.\n\n"
             "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v394-custodia]]\n") % (
        TOPICO_NOVO[:-3], V["data"], V["s16"], V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
        format(d["delta"], ","), d["pct"], _num(V), _cunhagens(V), _lado_c1(V), _criterio(V), _limites(V), _kh_errata(V), _codex_linhas(V)))


# v394 (gerencia c1, 19/10/2026): o aviso a coordenadora (so' sob reivindicacao nomeada)
def aviso(V, reivindicacao):
    d = _d(V)
    return (("### %s — v394 SELADA `%s` [claude-c1]\n<!-- aviso_v394_selada -->\n\n[REAL] A v394 SELOU (%s; COMPLETA; gate intocado): o relógio M2, a regra quadrática, a rede de Fock/Takesaki/Maxwell e as %d cunhagens de 14 a 19/10 (por sha256) entram no selo corrente. "
             "Escrito sob a reivindicação %s. %d módulos novos no kernel; escada %s → %s; as linhas do Codex (F1.FECHO) ficam como estão, auditadas pela c1 no exame da v394, e o selo é da c1; o elo B(n) da Bancada Um espera o operador. "
             "Não altera pinos, dado, MCP nem gate.") % (V["data"], V["s16"], V["teor"], d["n_cun"], reivindicacao, V["n_pedras"], V["escada_antes"], d["depois"]))


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V394_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# ------------------------------------------------------------------- ferramentas da arvore e do indice (OPCIONAIS: so' usadas se alguem escrever patch_arvore_indice_v394.py)
# v394 (gerencia c1, 19/10/2026): a linha da arvore da prova
def arvore_linha(V):
    d = _d(V)
    return ("- **O RELÓGIO M2, A REGRA QUADRÁTICA, A REDE DE FOCK E AS CUNHAGENS (v394)** `%s`: %d módulos novos no kernel (%s), %d bandeiras novas True, escada %s → %s; "
            "o relógio derivado no modelo M2 (2×2), com hipóteses físicas nomeadas; a rede com o contrato conjunto aberto; as %d cunhagens do operador por sha256; validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["n_pedras"], _grupos_txt(d), d["n_flags"], V["escada_antes"], d["depois"], d["n_cun"]))


# v394 (gerencia c1, 19/10/2026): o titulo do verbete do indice
def titulo_verbete(V):
    return "O relógio M2, a regra quadrática, a rede de Fock e as cunhagens (v394):"


# v394 (gerencia c1, 19/10/2026): o corpo do verbete do indice
def verbete(V):
    return "[REAL — rodada v394 `%s`] %s." % (V["s16"], _num(V))


# v394 (gerencia c1, 19/10/2026): a entrada do remissivo
def remissivo(V):
    return "- **O relógio M2, a regra quadrática, a rede de Fock e as cunhagens de 14 a 19/10 (v394)** — `tempo_frequencia_v394`, `regra_quadratica_v394`, `rede_fock_v394`, `cunhagens_v394`, `kh_n1_cobertura_v394`, `%s`" % TOPICO_NOVO
