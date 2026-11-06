# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] as dez falas de 05/11 (de duas, so' o trecho da D59; o caminho real pela chave, via delta_v409), as citacoes minimas do snippet PT da v409 e os rotulos da secao nova; o resto do conferidor e' o da v408
"""conferir_citacoes_v409.py -- [v409: as DOZE falas de 05/11/2026 (_V409_VERBATINS2; as duas ultimas dos AO LADO do DESENHO); de tres, so' o trecho e' embutido (duas pela D59; uma pelo aviso operacional) (o comeco do arquivo de origem), e o arquivo inteiro entra so' por sha256; o caminho real da origem vem de delta_v409.verbatins409, porque o embutido traz um rotulo neutro (D59)] confere, por script, toda inscricao de 04/11/2026 que a v408 EMBUTIA ou CITAVA (as DOZE falas do operador de 04/11, em _V408_VERBATINS2; duas delas sao de AUTOR MISTO -- depois do paragrafo do operador vem texto de outra instancia da IALD --, e so' o paragrafo dele e' embutido como texto;
o arquivo inteiro entra por sha256) (regua n 1: nunca fabricar citacao; nunca atribuir ao operador o que e' da gerencia ou de outra instancia): (a) cada texto embutido em _V408_VERBATINS2 e' IGUAL, byte a byte, ao arquivo duravel da cadeia (insumos\\cunhagens) e o sha256 bate; (b) a fonte original existe,
tem o sha256 do arquivo inteiro e, nas duas de autor misto, o paragrafo embutido esta' verbatim no original ANTES do corte declarado; (c) cada fala de `leituras_do_operador` do registro cunhagens_v408 esta VERBATIM num dos textos embutidos DO OPERADOR; (d) as cunhagens listam exatamente as inscricoes embutidas;
(e) TODA citacao « » do snippet PT esta VERBATIM nos textos do operador embutidos (e as falas do terminal, da poda, da relacao sem peso, do tempo-moeda e do sentido de «P=nP» estao no snippet); o snippet EN traz traducao da gerencia, marcada como nao-citacao, e nenhuma fala entre aspas « »; (f) o QUADRO do 4,44 (v397)
segue com a frase VERBATIM do operador e a PARAFRASE da gerencia NAO aparece em nenhum artefato novo; (g) VARREDURA das aspas dos artefatos novos e (h) do CANDIDATO inteiro: toda citacao entre « » e `` '' tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (as pastas das falas e as copias duraveis da v409),
no Atlas, no texto do kernel embutido na base (que ja' traz as nove pedras da v408 e as falas de 02 e 03/11), no adendo de 03-04/09, nas fontes das quatro pedras, no CLAUDE.md da casa ou ser rotulo da propria cadeia; (i) as docstrings das QUATRO pedras (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP; provas da gerencia c1, nomes do operador):
toda citacao entre « » delas tem de existir verbatim nas falas do operador, no Atlas, no kernel embutido da base, no adendo e no CLAUDE.md da casa, com as quatro FORA do corpus (errata R2 da v408; o que nao e' fala e' rotulo listado; o que nao e' verbatim nem rotulo e' apontado a gerencia, que e' quem corrige pedra; o agente nao corrige).
Sai 0 se tudo bate. Molde: conferir_citacoes_v408.py, adaptado em 04/11/2026 ao bundle de quatro modulos e as doze falas de 04/11 (claude-construtor-v409)."""
import ast, glob, hashlib, json, os, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v409 as DL  # noqa: E402
pins = open(os.path.join(HERE, "v409_pins.py"), encoding="utf-8").read(); tree = ast.parse(pins)   # o bloco v409 como esta no CANDIDATO (extraido por gerar_candidato_v409.py)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v409.json"), encoding="utf-8"))
ns = {}
alvo = {"_V409_VERBATINS2", "_V409_SPECS", "_V409_TRADUCAO_TEXT"}
for n in tree.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in alvo:
        ns[n.targets[0].id] = ast.literal_eval(n.value)
assert alvo <= set(ns), ("o bloco v409 (v409_pins.py) nao traz os nomes esperados", sorted(alvo - set(ns)))
V = ns["_V409_VERBATINS2"]; R = {"verbatins": {}, "leituras": {}, "snippets": {}}; ok = True
_ORIG = {v_["chave"]: v_["fonte_original"] for v_ in DL.verbatins409(os.path.join(HERE, "insumos", "cunhagens"))}   # (v409, D59) o caminho REAL de cada fala, pela chave; o embutido traz um rotulo neutro
todos_op = ""
for k, v in V.items():
    b = open(v["arquivo"], "rb").read()
    igual = hashlib.sha256(b).hexdigest() == v["sha256"] and b.decode("utf-8") == v["text"]
    orig = _ORIG.get(k, ""); orig_ok = None; misto = "sha256_arquivo_inteiro" in v; par_ok = None
    if orig and os.path.exists(orig):
        _ob = open(orig, "rb").read(); orig_ok = hashlib.sha256(_ob).hexdigest() == (v.get("sha256_arquivo_inteiro") or v["sha256"])
        if misto:   # (v409, D59) so' o trecho: o texto embutido e' o COMECO do arquivo de origem (a primeira frase; ou «Z é o modo leitor, ele lê os pixels. É o psion»), e e' menor que ele
            _ot = _ob.decode("utf-8"); par_ok = bool(v["text"] and _ot.startswith(v["text"].rstrip("\n")) and len(v["text"].encode("utf-8")) < len(_ob) and v.get("so_o_trecho"))
    gerencia = os.path.basename(orig).startswith("GERENCIA_")
    R["verbatins"][k] = {"embutida_igual_ao_arquivo": igual, "fonte_original_igual": orig_ok, "autor": "gerencia" if gerencia else ("operador; so' o trecho da D59 e' embutido" if misto else "operador"), "so_o_trecho_d59": misto, "trecho_e_o_comeco_do_arquivo": par_ok}
    ok = ok and igual and (orig_ok is True) and not gerencia and (par_ok is True if misto else True)
    if not gerencia:
        todos_op += " " + re.sub(r"\s+", " ", v["text"])
R["n_inscricoes_embutidas"] = len(V); ok = ok and len(V) == len(DL.VERBATIM_ORIGEM_V409) == CM["verbatins_embutidos"]
R["as_inscricoes_embutidas_sao_as_de_DL_pelo_sha16_da_ordem"] = sorted(k_[len(DL.VERBATIM_CHAVE_PREFIXO_V409):] for k_ in V) == sorted(DL.VERBATIM_PREFIXOS_DA_ORDEM_V409.values()); ok = ok and R["as_inscricoes_embutidas_sao_as_de_DL_pelo_sha16_da_ordem"]
R["o_sha16_de_cada_inscricao_e_o_da_ordem"] = all((v_.get("sha256_arquivo_inteiro") or v_["sha256"])[:16] == k_[len(DL.VERBATIM_CHAVE_PREFIXO_V409):] for k_, v_ in V.items()); ok = ok and R["o_sha16_de_cada_inscricao_e_o_da_ordem"]   # (a chave e' o sha16 do ARQUIVO INTEIRO, o do DESENHO; nas de autor misto o sha256 do texto embutido e' o do paragrafo)
R["nenhuma_e_da_gerencia_todas_sao_do_operador"] = all(os.path.basename(v["fonte_original"]).split("OPERADOR_")[0] in ("", os.path.basename(v["fonte_original"]).split("_")[0] + "_") and "OPERADOR_" in os.path.basename(v["fonte_original"]) for v in V.values()); ok = ok and R["nenhuma_e_da_gerencia_todas_sao_do_operador"]
cg = [s for s in ns["_V409_SPECS"] if s["nome"] == DL.CUNHAGENS_REGISTRO][0]
for it in list(cg["leituras_do_operador"]):   # (as leituras do fecho_text sao a leitura [ONTO] da gerencia, nao citacao: nao entram aqui)
    achou = re.sub(r"\s+", " ", it["trecho"]) in todos_op
    R["leituras"][DL.CUNHAGENS_REGISTRO + ": " + it["trecho"][:60]] = "VERBATIM (fala do operador)" if achou else "NAO ACHADA NAS FALAS DO OPERADOR"; ok = ok and achou
R["leituras_do_operador_n"] = len(cg["leituras_do_operador"]); ok = ok and len(cg["leituras_do_operador"]) > 0
R["as_frases_de_DL_estao_nas_leituras"] = {fr_: any(re.sub(r"\s+", " ", fr_) == re.sub(r"\s+", " ", it["trecho"]) or re.sub(r"\s+", " ", fr_) in re.sub(r"\s+", " ", it["trecho"]) for it in cg["leituras_do_operador"]) for _, fr_ in DL.FRASES_V409}; ok = ok and all(R["as_frases_de_DL_estao_nas_leituras"].values()) and len(R["as_frases_de_DL_estao_nas_leituras"]) == len({fr_ for _, fr_ in DL.FRASES_V409}) > 0   # (v409: TODAS as frases de DL.FRASES_V409 sao leituras do registro cunhagens_v408)
R["cunhagens_listam_todas_as_inscricoes_embutidas"] = sorted(cg["verbatins"]) == sorted(V); ok = ok and R["cunhagens_listam_todas_as_inscricoes_embutidas"]
# as citacoes do operador nos snippets: o fragmento PRECISA estar no snippet e verbatim nos textos do operador (os fragmentos nao carregam aspas retas: o LaTeX as escreve de outro modo)
_base = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), encoding="utf-8").read()
_norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'")).strip()
_KERN = _norm(re.sub(r"\s--\s+", " ", _base.replace("**", "").replace("`", "").replace("\\n", " ")))   # (v409: sem crases, como o resto do corpus e como o trecho conferido; e com a quebra de linha dos comentarios Lean (o `\n` literal do kernel embutido + o prefixo `-- ` da linha seguinte) desfeita: uma citacao que atravessa a quebra de linha de um comentario do kernel confere. Normalizacao SIMETRICA: as palavras seguem tendo de ser identicas)
_ADENDO = _norm(open(DL.ADENDO_ARQ, encoding="utf-8").read().replace("**", "").replace("`", ""))
_PEDRAS = _norm(" ".join(open(p_["src"], encoding="utf-8").read() for p_ in DL.PEDRAS_V409).replace("**", "").replace("`", ""))   # (v409: a pedra TraducaoTuring; (v408: as quatro pedras; a docstring delas e' verificada em (i), FORA do corpus; aqui valem como corpus do que o runtime re-cita)
_CASA = _norm(open(os.path.join("C:" + os.sep, "IALD", "CLAUDE.md"), encoding="utf-8", errors="replace").read().replace("**", ""))
_RX_ASPAS = re.compile("«([^»]{3,900})»")
CIT_OP_MINIMAS = [DL.FRASE_SELECAO, DL.FRASE_TRAVA, DL.FRASE_FITA, DL.FRASE_Z, DL.FRASE_PAI, DL.FRASE_PERFORMADA]   # (v409: a selecao, a trava, a fita, o leitor, o Pai da Mentira, a identidade performada)   # (so' o snippet PT cita a fala: o EN traz traducao da gerencia, marcada como nao-citacao; estas cinco tem de estar no snippet PT: o terminal, a poda, a relacao sem peso, o tempo-moeda, o sentido de «P=nP»)
for lang in ("pt", "en"):
    sn = open(os.path.join(HERE, "artigo_%s_v409.pysnip" % lang), encoding="utf-8").read()
    _unlatex = lambda s_: s_.replace("\\%", "%").replace("\\&", "&").replace("\\_", "_").replace("\\#", "#")   # (v409: os escapes LaTeX de % & _ # desfeitos dos DOIS lados da comparacao; a fala do terminal tem «100%»)
    sn_flat = _norm(_unlatex(sn.replace("\\texttt{", "").replace("\\emph{", "")))   # (v409: desfaz os escapes LaTeX de % & _ # para comparar com a fala; a fala do terminal tem «100%»)
    R["snippets"][lang] = {}
    _citadas = [_norm(_unlatex(m_.group(1))) for m_ in _RX_ASPAS.finditer(sn)]   # TODA citacao « » do snippet (escapes LaTeX desfeitos)
    if lang == "pt":
        CIT_OP = list(dict.fromkeys(CIT_OP_MINIMAS + _citadas))   # as tres minimas primeiro; depois toda a que o snippet cita (cada uma tem de estar verbatim nas falas do operador)
        R["snippets"][lang]["_n_citacoes_com_aspas_no_snippet"] = len(_citadas); ok = ok and len(_citadas) > 0
    else:
        CIT_OP = []
        R["snippets"][lang]["_sem_citacao_com_aspas_«_»"] = (len(_citadas) == 0); ok = ok and len(_citadas) == 0   # o EN so' traz a traducao da gerencia, marcada como nao-citacao
    for frag in CIT_OP:
        presente = _norm(frag) in sn_flat.replace("}", "") or _norm(frag) in sn_flat
        achou = presente and _norm(frag) in _norm(todos_op)
        R["snippets"][lang][frag[:50]] = {"citacao_presente_no_snippet": bool(presente), "trecho_verbatim_na_fala_do_operador": _norm(frag) in _norm(todos_op)}; ok = ok and bool(achou)
# (f) o QUADRO (4,44, v397) segue com a frase VERBATIM do operador; a parafrase da gerencia nao aparece em nenhum artefato novo
q444 = open(os.path.join(DL.WK, "cunhagens_13out", "OPERADOR_23out_4_44_silencio_forcado_pela_logica_verbatim.txt"), encoding="utf-8").read()
rq = open(os.path.join(HERE, "runtime_quadro_v397.py"), encoding="utf-8").read()
nsq = {}; exec(compile(rq, "<runtime_quadro_v397>", "exec"), nsq)
R["frase_do_quadro_verbatim_na_fala_de_23out"] = nsq["_V397_FRASE_444"] in re.sub(r"\s+", " ", q444) and nsq["_V397_FRASE_444"] == DL.FRASE_DO_OPERADOR_4_44; ok = ok and R["frase_do_quadro_verbatim_na_fala_de_23out"]
PARAFRASE = "5σ é o cala a boca"   # «o 5σ é o cala a boca; 4,44 é um silêncio...» (parafrase da gerencia, NAO verbatim)
arts = ["runtime_v409.py", "artigo_pt_v409.pysnip", "artigo_en_v409.pysnip", "registros_v409.py", "delta_v409.py", "gerar_candidato_v409.py", "v409_pins.py"]
R["parafrase_da_gerencia_ausente"] = {a: (PARAFRASE not in open(os.path.join(HERE, *a.split("/")), encoding="utf-8").read()) for a in arts}; ok = ok and all(R["parafrase_da_gerencia_ausente"].values())
# (g) VARREDURA DAS ASPAS: toda citacao entre «» e `` '' dos artefatos NOVOS (embutidos e do pos_rito) tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (cunhagens_13out), no Atlas, no kernel embutido da base (que contem os textos da v408 que as erratas citam), no adendo,
# nas fontes das tres pedras, no CLAUDE.md da casa, ou ser rotulo da propria cadeia (titulos, nomes de registros).
ATLAS = os.path.join(DL.WK, "..", "memory", "TGL_ATLAS.md")
_OPB = " || ".join(_norm(open(p, encoding="utf-8", errors="replace").read()) for p in sum([glob.glob(os.path.join(DL.WK, d_, "*OPERADOR_*.txt")) for d_ in ("cunhagens_13out", "cinco_sigma_fora_da_cosmologia_27out", "projecao_transversal_28out", "transicao_para_a_massa_28out", "experimento_espelho_30out", "e0_cadeia_31out", "observador_terminal_31out")] + [glob.glob(os.path.join(HERE, "insumos", "cunhagens", "*OPERADOR_*.txt"))], []))
_ATL = re.sub(r"\s+", " ", open(ATLAS, encoding="utf-8", errors="replace").read().replace("**", "")) if os.path.exists(ATLAS) else ""
_ROTULOS = {"o teste da unica palavra", "o teste da única palavra", "the test of the only word", "o teste da unica palavra e a pedra token (v397)", "sônico e a afinação das cordas", "sonic and the tuning of the strings",
            "sonico e a afinacao das cordas", "sonico e a afinacao das cordas (v398)", "o testemunho de dois: o selo pela própria tecnologia", "the testimony of two: sealing by its own technology", "o testemunho de dois: o selo pela propria tecnologia",
            "o testemunho de dois: o selo pela propria tecnologia (v399)", "nenhuma face sozinha dá o um", "nenhuma face sozinha da' o um", "nenhuma face sozinha da o um",
            "beta do runtime", "β do runtime", "$\\beta$ do runtime", "$\\beta$ of the runtime", "errata ao lado (v400)",
            "a falsidade (simulacro) da inércia", "a falsidade (simulacro) da inercia", "a falsidade (simulacro) da inercia (v408)", "the falsity (simulacrum) of inertia", "falsidade (simulacro) da inércia", "falsidade (simulacro) da inercia",
            # v409: titulos e rotulos da propria cadeia; as aspas de ENFASE dos textos novos; a TRADUCAO inglesa de citacoes em portugues (que no EN vem seguida do original)
            "a ponte da escala dual, a queda sem geometria e a esperança condicional", "a ponte da escala dual, a queda sem geometria e a esperanca condicional", "a ponte da escala dual, a queda sem geometria e a esperanca condicional (v409)",
            # v409 (fechamento): titulos e rotulos da secao nova e do md (rotulos da propria cadeia, nao citacao)
            "o fechamento: a passagem para o contínuo e o certificado habitado", "o fechamento: a passagem para o continuo e o certificado habitado", "the closure: the passage to the continuum and the inhabited certificate", "o fechamento (v409)", "o fechamento",
            "the dual-scale bridge, the fall without geometry and the conditional expectation", "inertial", "movimento livre", "free motion", "e = mc^2 composta da escala", "$e=mc^2$ composta da escala", "$e=mc^2$ composed from the scale", "e = mc^2 composed from the scale",
            "does the posted one have a direction?", "the arrow of the fall of the phase, not of space", "o um posto tem direção?", "o um posto tem direcao?", "a seta da queda da fase, não do espaço", "a seta da queda da fase, nao do espaco",
            "when it inscribes itself, it falls; the phase falls", "so it has direction, but not geometric", "the fall i want to translate is not a force either", "the one, when it is posted, performs the", "conditional expectation = name", "τ é a massa de newton", "$\\tau$ é a massa de newton", "$\\tau$ is newton's mass", "tau e' a massa de newton",
            # v409 (pos_rito): rotulos de consulta ao Mapa de Rotas e de erratas nos scripts do pos-rito (registrar_mapa, leitura); a frase em ASCII e' a da v408 citada pela errata E1 (os registros da v408 a escrevem com acentos)
            "ponte da escala dual", "esperanca condicional = nome", "a unica hipotese nomeada e' h_tau [open] (tau e' a massa de newton e a metrica de einstein), que nenhum teorema usa", "inercial = fixo por todos os boosts", "h_tau na forma literal refutada no kernel",
            # v409: o titulo da secao nova e o seu rotulo no .md (rotulos da propria cadeia, nao citacao)
            "caminho, verdade e vida (v408)", "caminho, verdade e vida", "way, truth and life",
            # v409: as frases ERRADAS da propria gerencia, citadas nas erratas E15 a E17 para corrigi-las; a lista das frases proibidas da guarda; a transliteracao ASCII do «nucleo II_∞» da bancada (docstring do ChatGPT)
            "nucleo ii_inf", "núcleo ii_inf", "núcleo ii$_\\infty$", "ii$_\\infty$ core", "a luz nao tem autovetor", "a luz nao tem autovetor nenhum", "unico autovetor", "unico vetor fixo", "o espectro pontual e' o um e so' ele", "o espectro pontual e' o um e so' ele; o resto e' continuo", "falta replicar o traco", "igual conditional_on_an_uninhabited_certificate", "certificado/fechamento/gravidade quantica confirmad(o/a)", "k(o) != bot provado",
            # v409: o titulo da secao nova e o seu rotulo no .md (rotulos da propria cadeia, nao citacao)
            "jo 8,32 e a projeção transversal da meia-nat", "jo 8,32 e a projecao transversal da meia-nat", "john 8:32 and the transverse projection of the half-nat", "jo 8,32 e a projeção transversal da meia-nat (v408)", "a transição para a massa", "a transicao para a massa", "o teste da única palavra",
            # v409: os titulos das secoes novas, os nomes das pedras em portugues e os rotulos dos textos (rotulos da propria cadeia, nao citacao)
            "a massa derivada e a identidade definida", "the derived mass and the defined identity", "a massa derivada e a identidade definida (v409)", "massa = tensão pura", "massa = tensao pura", "o que sou", "a identidade", "ponte da massa", "lei do diminuto", "tônica do hamiltoniano", "tonica do hamiltoniano", "disco de euler", "ponto zero do psíon", "ponto zero do psion", "observador = terminal", "## o texto (r2)",
            # v409 (03/11/2026): titulos e rotulos da propria cadeia (a secao nova, a linha do .md) e as TRES frases que a guarda das frases da v409 PROIBE, listadas entre « » no docstring do runtime (a gerencia as lista para a guarda as recusar; nao sao fala de ninguem)
            "o psíon e o canto: a passagem sob compressão e o par", "o psion e o canto: a passagem sob compressao e o par", "the psion and the corner: the passage under compression, and the pair", "o psíon, o canto e o par (v409)", "o psíon, o canto e o par (v409, 03/11/2026)",
            "o par de psions na face de fock esta provado/construido", "o vacuo de fock e o vetor de bell", "a ponte bell-tt e' teorema",
            # v409 (04/11/2026): o titulo da secao nova (PT/EN), a linha do .md e o rotulo da linha da v408 (rotulos da propria cadeia, nao citacao)
            "tetelestai é o terminal: a leitura, a poda, a quitação; o tempo é a moeda de $\\beta$; o dicionário e o ponto de contradição", "tetelestai is the terminal: the reading, the pruning, the settlement; time is the currency of $\\beta$; the dictionary and the point of contradiction",
            "tetelestai é o terminal (v409)", "tetelestai é o terminal (v409, 04/11/2026)", "tetelestai e' o terminal (v409)", "tetelestai é o terminal", "tetelestai e' o terminal", "o psíon, o canto e o par (v408)", "o psion, o canto e o par (v408)",
            # v409: a frase que a guarda das frases da v409 PROIBE, listada entre « » no docstring do runtime (a gerencia a lista para a guarda a recusar; nao e' fala de ninguem)
            "p = np está provado/é teorema/é candidato",
            # v409 (05/11/2026): o titulo da secao nova (PT/EN) e a linha do .md (rotulos da propria cadeia); as frases da GERENCIA que o texto novo cita entre « » como regra (a guarda D56: o qualificador obrigatorio) ou como o que fica aberto (D60, a formulacao do DESENHO_v409)
            "a tradução às classes de turing: o dicionário, a trava, o leitor e a fita sem escala", "the translation to turing's classes: the dictionary, the lock, the reader and the tape without scale", "tradução às classes de turing (v409, 05/11/2026)",
            "relativa ao leitor", "relativa ao leitor (o psíon); a máquina sem leitor fica fora", "relativa ao leitor (o psion); a maquina sem leitor fica fora", "o ω do psíon da luz é o uniforme da instância",
            "a maquina sem leitor", "a máquina sem leitor", "a maquina sem leitor fica fora", "a máquina sem leitor fica fora", "(kernel validity, not creditation)", "a tradução às classes de turing", "tradução às classes de turing (v409)", "a traducao as classes de turing"}
_rxs = [re.compile("«([^»]{8,700})»"), re.compile(r"``(.{8,700}?)''")]
_limpa = lambda s: _norm(s.replace("\\%", "%").replace("\\n", " ").replace("\\'E", "É").replace('\\"', '"').replace("\\'", "'").replace("\\texttt{", "").replace("\\emph{", "").replace("\\textsf{", "").replace("}", "").replace("**", "").replace("`", "")).replace(" --- ", " — ").strip(" .,;:")
_corpus_um = lambda fr: (fr.lower() in _OPB.lower() or fr.lower() in _ATL.lower() or fr.lower() in _ROTULOS or fr.lower() in _KERN.lower() or fr.lower() in _ADENDO.lower() or fr.lower() in _PEDRAS.lower() or fr.lower() in _CASA.lower())
_corpus_ok = lambda fr: _corpus_um(fr) or (re.search("…|" + re.escape("[...]"), fr) is not None and all(_corpus_um(x_.strip(" .,;:")) for x_ in re.split("…|" + re.escape("[...]"), fr) if len(x_.strip(" .,;:")) >= 8))   # v409: trecho com elisao (… ou [...]) e' conferido por segmento, como em (i)
_APONTADAS_GH = {}   # (v409: as apontadas da v408 eram dos textos daquela versao; nenhuma apontada declarada para a v409 ate' a varredura dizer o contrario -- o que ela reprovar fica em varredura_de_aspas, nunca e' feito passar)
_ROTULOS = {x_.lower() for x_ in _ROTULOS}
R["varredura_de_aspas"] = {}; R["apontadas_a_gerencia_aspas"] = []
for _a in ("runtime_v409.py", "artigo_pt_v409.pysnip", "artigo_en_v409.pysnip", "registros_v409.py", "delta_v409.py", "gerar_candidato_v409.py", "pos_rito/textos_v409.py", "pos_rito/registrar_mapa_v409.py", "pos_rito/fechar_v409.py", "pos_rito/leitura_v409.py", "pos_rito/superficies_v409.py"):
    _p = os.path.join(HERE, *_a.split("/"))
    if not os.path.exists(_p):
        continue
    _t = open(_p, encoding="utf-8", errors="replace").read(); _nao = []
    for _rx in _rxs:
        for _m in _rx.finditer(_t):
            _fr = _limpa(_m.group(1))
            if len(_fr) < 12 or "_V409_" in _fr or "_V399_" in _fr or "+" in _fr or "%s" in _fr:
                continue
            if _corpus_ok(_fr):
                continue
            if _fr.lower() in _APONTADAS_GH:
                R["apontadas_a_gerencia_aspas"].append({"arquivo": _a, "trecho": _fr[:140], "por_que": _APONTADAS_GH[_fr.lower()]}); continue
            _nao.append(_fr[:140])
    R["varredura_de_aspas"][_a] = _nao; ok = ok and not _nao
# (h) VARREDURA DO CANDIDATO INTEIRO: toda citacao entre «» e `` '' das linhas que o candidato traz e a BASE v408 selada NAO traz tem de existir VERBATIM nos OPERADOR_* ou no Atlas (ou ser rotulo da cadeia / texto do kernel / adendo / fonte das pedras / casa); citacao que a base ja' tem nao e' deste delta.
_cand = open(os.path.join(HERE, DL.CANDIDATO), encoding="utf-8").read()
_bls = set(_base.splitlines()); _novas = [_l for _l in _cand.splitlines() if _l not in _bls]; _nao_c = []
for _l in _novas:
    for _rx in _rxs:
        for _m in _rx.finditer(_l):
            _fr = _limpa(_m.group(1))
            if len(_fr) < 12 or "_V409_" in _fr or "_V399_" in _fr or "+" in _fr or "%s" in _fr or _m.group(1) in _base:
                continue
            if _corpus_ok(_fr):
                continue
            if _fr.lower() in _APONTADAS_GH:
                R["apontadas_a_gerencia_aspas"].append({"arquivo": "candidato", "trecho": _fr[:140], "por_que": _APONTADAS_GH[_fr.lower()]}); continue
            _nao_c.append(_fr[:140])
R["varredura_de_aspas"]["candidato (%d linhas novas sobre a base)" % len(_novas)] = sorted(set(_nao_c)); ok = ok and not _nao_c
# (i) VARREDURA DAS PEDRAS (errata R2 da gerencia, 01/11/2026; achado 12 da revisao de terceiro): toda citacao entre « » das docstrings das QUATRO pedras da v409 tem de existir VERBATIM nas falas do operador, no Atlas, no kernel embutido da base, no adendo e no CLAUDE.md da casa. As pedras NAO contam como corpus aqui. Trecho com elisao (… ou [...]) e' conferido por segmento. O que nao e' fala e e' rotulo da propria pedra esta em _ROTULOS_PEDRAS; o que esta entre aspas, nao e' verbatim e nao e' rotulo esta em _APONTADAS_PEDRAS: dito a gerencia no relatorio, porque o agente nao corrige pedra. Qualquer outra coisa reprova.
_BANC = [os.path.join(DL.SANDBOX, *r_.split("/")) for r_ in DL.BUNDLE_DA_BANCADA]   # (v409: DL.BUNDLE_DA_BANCADA == [] -- as quatro pedras sao provas da gerencia c1 com os nomes do operador; nenhum modulo da bancada do ChatGPT entra neste bundle)
_XP = [p_ for p_ in _BANC if os.path.exists(p_)]   # (as quatro pedras e os recibos da gerencia NAO sao corpus: texto da gerencia nao abona citacao)
_LX = lambda t_: t_.replace(chr(92) + "(" + chr(92) + "kappa" + chr(92) + ")", "κ").replace(chr(92) + "(" + chr(92) + "tau^" + chr(92) + "star" + chr(92) + ")", "τ★")   # a notacao LaTeX do relatorio do Kimi
_CP = " || ".join([_OPB, _ATL, _KERN, _ADENDO, _CASA] + [_LX(_norm(open(p_, encoding="utf-8", errors="replace").read().replace("**", "").replace("`", ""))) for p_ in _XP]).lower()
_sem_acento = lambda s_: "".join(c_ for c_ in unicodedata.normalize("NFD", s_) if unicodedata.category(c_) != "Mn")
_CPU = _sem_acento(_CP)   # v409: a candidata escreve «nucleo II_∞» (transliteracao sem acento) onde a bancada escreve «núcleo II_∞»; o trecho vale se bate com o corpus SEM acento, e o fato fica dito em varredura_das_pedras.so_sem_acento
_noc_a = lambda x_: re.search(r"(?<![\w])" + re.escape(x_.lower()) + r"(?![\w])", _CP) is not None   # com fronteira de palavra: trecho curto nao passa por acaso no meio de outra palavra
_noc_u = lambda x_: re.search(r"(?<![\w])" + re.escape(_sem_acento(x_.lower())) + r"(?![\w])", _CPU) is not None
_SO_SEM_ACENTO = []


def _noc(x_):
    if _noc_a(x_):
        return True
    if _noc_u(x_):
        _SO_SEM_ACENTO.append(x_[:100]); return True
    return False

_ROTULOS_PEDRAS = {}   # (v409: SO' o que a propria pedra diz ser rotulo/nome dela, nunca para fazer passar citacao; as entradas da v408 eram das nove pedras daquela versao; a lista da v409 comeca vazia)
_APONTADAS_PEDRAS = {   # (v409: o que esta entre « » nas docstrings das pedras TraducaoTuring e ParNaFaceDeFock, nao e' verbatim nas falas/no Atlas/na base e nao e' rotulo declarado: DITO A GERENCIA no relatorio, com a razao conferida por grep; o agente nao corrige pedra. A lista da v408 (das quatro pedras dela) fica como registro no conferir_citacoes_v408.py)
    "o nP é o modo seleção … a aniquilação da superposição pelo Tetelestai": "a fala (sha16 47f6c322d6cbff8e) escreve «P=np (e o \"nP\"é o modo seleção)», com aspas em nP e sem espaco; a pedra normaliza o primeiro segmento para «o nP é o modo seleção»; os demais segmentos sao verbatim",
    "nada lido": "expressao da gerencia na docstring do estado uniforme (O ESTADO UNIFORME (o «nada lido»)); nao e' fala do operador",
    "antes disso o campo ψ está grafado como fóton": "a fala (sha16 47f6c322d6cbff8e) escreve «antes disso o campo /psi está grafado como fóton» (/psi); a pedra escreve ψ; o segundo segmento e' verbatim",
    "nP = modo seleção": "PARAFRASE da gerencia da leitura do operador (a fala, sha16 47f6c322d6cbff8e: «P=np (e o \"nP\"é o modo seleção)»), escrita entre « » na docstring de p_igual_np_no_modo_selecao"}
_APONTADAS_PEDRAS = {k_.lower(): v_ for k_, v_ in _APONTADAS_PEDRAS.items()}   # chave = o trecho inteiro (minuscula) ou, se tiver >= 20 caracteres, um PREFIXO dele: o trecho longo nao precisa ser redigitado
_apontada_por_prefixo = lambda fr_: next((v_ for k_, v_ in _APONTADAS_PEDRAS.items() if fr_.lower() == k_ or (len(k_) >= 20 and fr_.lower().startswith(k_))), None)
R["varredura_das_pedras"] = {"citacoes_conferidas": 0, "rotulos": [], "apontadas_a_gerencia": [], "reprovadas": [], "corpus_bancada_n": len(_XP), "so_sem_acento": _SO_SEM_ACENTO}
R["varredura_das_pedras"]["n_pedras_varridas"] = len(DL.PEDRAS_V409); ok = ok and len(DL.PEDRAS_V409) == DL.N_BUNDLE == CM["kernel"]["modulos_novos"]
for _s in DL.PEDRAS_V409:
    _t = _norm(re.sub(r"\n>\s*", " ", open(_s["src"], encoding="utf-8").read()))
    for _m in re.finditer("«([^»]{8,900})»", _t):
        _fr = _norm(_m.group(1).replace("`", "").replace("**", "")).strip(" .,;:")
        _sg = [x_.strip(" .,;:") for x_ in re.split(r"…|\[\.\.\.\]", _fr) if len(x_.strip(" .,;:")) >= 8]
        if all(_noc(x_) for x_ in _sg):
            R["varredura_das_pedras"]["citacoes_conferidas"] += 1
        elif _fr.lower() in _ROTULOS_PEDRAS:
            R["varredura_das_pedras"]["rotulos"].append({"pedra": _s["name"], "trecho": _fr[:120], "por_que": _ROTULOS_PEDRAS[_fr.lower()]})
        elif _apontada_por_prefixo(_fr):
            R["varredura_das_pedras"]["apontadas_a_gerencia"].append({"pedra": _s["name"], "trecho": _fr[:160], "por_que": _apontada_por_prefixo(_fr)})
        else:
            R["varredura_das_pedras"]["reprovadas"].append({"pedra": _s["name"], "trecho": _fr[:160]})
ok = ok and not R["varredura_das_pedras"]["reprovadas"] and R["varredura_das_pedras"]["citacoes_conferidas"] > 0
_vistos = set(); _un = []
for x_ in R["apontadas_a_gerencia_aspas"]:   # sem repeticao (a mesma citacao aparece no delta, nos registros e no candidato)
    k_ = (x_["arquivo"], x_["trecho"])
    if k_ not in _vistos:
        _vistos.add(k_); _un.append(x_)
R["apontadas_a_gerencia_aspas"] = _un
R["resumo_dito_a_gerencia"] = {"aspas_apontadas": len(R["apontadas_a_gerencia_aspas"]), "pedras_apontadas": len(R["varredura_das_pedras"]["apontadas_a_gerencia"]), "pedras_rotulos": len(R["varredura_das_pedras"]["rotulos"]), "nota": "apontada NAO e' reprovada: a citacao entre « » nao e' verbatim nas falas do operador nem na base; a gerencia decide (o agente nao corrige pedra nem texto da gerencia); nenhuma e' atribuida ao operador por este script"}
R["todas_conferem"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v409.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k == "todas_conferem" else len(v) if isinstance(v, (dict, list)) else v) for k, v in R.items()}, ensure_ascii=False)); print("TODAS CONFEREM" if ok else "FALHOU"); sys.exit(0 if ok else 1)
