# -*- coding: utf-8 -*-
"""conferir_citacoes_v407.py -- confere, por script, toda inscricao de 03/11/2026 que a v407 EMBUTE ou CITA (as TRES falas novas, em _V407_VERBATINS2; as 23 de 02/11 ja' estao embutidas no um.py v406 selado e entram aqui como corpus da base) (regua nº 1: nunca fabricar citacao; nunca atribuir ao operador o que e' da gerencia): (a) cada texto embutido em _V407_VERBATINS2 e' IGUAL, byte a byte, ao arquivo
duravel da cadeia (insumos\\cunhagens) e o sha256 bate; (b) a fonte original existe e tem o MESMO sha256; (c) cada fala de `leituras_do_operador` do registro cunhagens_v407 esta VERBATIM num dos textos embutidos DO OPERADOR; (d) as cunhagens listam exatamente
as inscricoes embutidas (todas falas do operador: nenhuma e' da gerencia); (e) TODA citacao « » do snippet PT esta VERBATIM nos textos do operador embutidos (e as tres falas que sustentam o lema, o par e o nome estao no snippet); o snippet EN traz traducao da gerencia, marcada como nao-citacao, e nenhuma fala entre aspas « »; (f) o QUADRO do 4,44 (v397) segue com a frase VERBATIM do operador e a PARAFRASE
da gerencia NAO aparece em nenhum artefato novo; (g) VARREDURA das aspas dos artefatos novos e (h) do CANDIDATO inteiro: toda citacao entre « » e `` '' tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (as pastas das falas e as copias duraveis da v407), no Atlas, no texto do kernel embutido na base,
no adendo de 03-04/09, nas fontes das nove pedras, no CLAUDE.md da casa ou ser rotulo da propria cadeia; (i) as docstrings das NOVE pedras (PsionCanto e Par, da gerencia c1; as sete de 02/11 de nome ratificado): toda citacao entre « » delas tem de existir verbatim nas falas do operador, no Atlas, no kernel embutido da base, no adendo e no CLAUDE.md da casa, com as nove FORA do corpus (errata R2 da v406; o que nao e' fala e' rotulo listado; o que nao e' verbatim nem rotulo e' apontado a gerencia, que e' quem corrige pedra; o agente nao corrige). Sai 0 se tudo bate. Escrito a mao para a v407 (molde: conferir_citacoes_v406.py, adaptado em 03/11/2026 ao bundle de nove modulos e as tres falas novas)."""
import ast, glob, hashlib, json, os, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v407 as DL  # noqa: E402
pins = open(os.path.join(HERE, "v407_pins.py"), encoding="utf-8").read(); tree = ast.parse(pins)   # o bloco v407 como esta no CANDIDATO (extraido por gerar_candidato_v407.py)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v407.json"), encoding="utf-8"))
ns = {}
alvo = {"_V407_VERBATINS2", "_V407_SPECS", "_V407_PSION_TEXT"}
for n in tree.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in alvo:
        ns[n.targets[0].id] = ast.literal_eval(n.value)
assert alvo <= set(ns), ("o bloco v407 (v407_pins.py) nao traz os nomes esperados", sorted(alvo - set(ns)))
V = ns["_V407_VERBATINS2"]; R = {"verbatins": {}, "leituras": {}, "snippets": {}}; ok = True
todos_op = ""
for k, v in V.items():
    b = open(v["arquivo"], "rb").read()
    igual = hashlib.sha256(b).hexdigest() == v["sha256"] and b.decode("utf-8") == v["text"]
    orig = v.get("fonte_original", ""); orig_ok = None
    if orig and os.path.exists(orig):
        orig_ok = hashlib.sha256(open(orig, "rb").read()).hexdigest() == v["sha256"]
    gerencia = os.path.basename(v["fonte_original"]).startswith("GERENCIA_")
    R["verbatins"][k] = {"embutida_igual_ao_arquivo": igual, "fonte_original_igual": orig_ok, "autor": "gerencia" if gerencia else "operador"}
    ok = ok and igual and (orig_ok is True) and not gerencia
    if not gerencia:
        todos_op += " " + re.sub(r"\s+", " ", v["text"])
R["n_inscricoes_embutidas"] = len(V); ok = ok and len(V) == len(DL.VERBATIM_ORIGEM_V407) == CM["verbatins_embutidos"]
R["as_inscricoes_embutidas_sao_as_de_DL_pelo_sha16_da_ordem"] = sorted(k_[len(DL.VERBATIM_CHAVE_PREFIXO_V407):] for k_ in V) == sorted(DL.VERBATIM_PREFIXOS_DA_ORDEM_V407.values()); ok = ok and R["as_inscricoes_embutidas_sao_as_de_DL_pelo_sha16_da_ordem"]
R["o_sha16_de_cada_inscricao_e_o_da_ordem"] = all(v_["sha256"][:16] == k_[len(DL.VERBATIM_CHAVE_PREFIXO_V407):] for k_, v_ in V.items()); ok = ok and R["o_sha16_de_cada_inscricao_e_o_da_ordem"]
R["nenhuma_e_da_gerencia_todas_sao_do_operador"] = all(os.path.basename(v["fonte_original"]).split("OPERADOR_")[0] in ("", os.path.basename(v["fonte_original"]).split("_")[0] + "_") and "OPERADOR_" in os.path.basename(v["fonte_original"]) for v in V.values()); ok = ok and R["nenhuma_e_da_gerencia_todas_sao_do_operador"]
cg = [s for s in ns["_V407_SPECS"] if s["nome"] == DL.CUNHAGENS_REGISTRO][0]
for it in list(cg["leituras_do_operador"]):   # (as leituras do fecho_text sao a leitura [ONTO] da gerencia, nao citacao: nao entram aqui)
    achou = re.sub(r"\s+", " ", it["trecho"]) in todos_op
    R["leituras"][DL.CUNHAGENS_REGISTRO + ": " + it["trecho"][:60]] = "VERBATIM (fala do operador)" if achou else "NAO ACHADA NAS FALAS DO OPERADOR"; ok = ok and achou
R["leituras_do_operador_n"] = len(cg["leituras_do_operador"]); ok = ok and len(cg["leituras_do_operador"]) > 0
R["as_frases_de_DL_estao_nas_leituras"] = {fr_[:50]: any(re.sub(r"\s+", " ", fr_) == re.sub(r"\s+", " ", it["trecho"]) or re.sub(r"\s+", " ", fr_) in re.sub(r"\s+", " ", it["trecho"]) for it in cg["leituras_do_operador"]) for _, fr_ in DL.FRASES_V407 if fr_ in (DL.FRASE_LEMA_PSION, DL.FRASE_NOME, DL.FRASE_PAR_LIGADO, DL.FRASE_PROJETOR, DL.FRASE_NOMES_RATIFICADOS, DL.FRASE_TESTE_C, DL.FRASE_BANHO, DL.FRASE_PAR)}; ok = ok and all(R["as_frases_de_DL_estao_nas_leituras"].values()) and len(R["as_frases_de_DL_estao_nas_leituras"]) == 8
R["cunhagens_listam_todas_as_inscricoes_embutidas"] = sorted(cg["verbatins"]) == sorted(V); ok = ok and R["cunhagens_listam_todas_as_inscricoes_embutidas"]
# as citacoes do operador nos snippets: o fragmento PRECISA estar no snippet e verbatim nos textos do operador (os fragmentos nao carregam aspas retas: o LaTeX as escreve de outro modo)
_base = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), encoding="utf-8").read()
_norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'")).strip()
_KERN = _norm(re.sub(r"\s--\s+", " ", _base.replace("**", "").replace("`", "").replace("\\n", " ")))   # (v407: sem crases, como o resto do corpus e como o trecho conferido; e com a quebra de linha dos comentarios Lean (o `\n` literal do kernel embutido + o prefixo `-- ` da linha seguinte) desfeita: uma citacao que atravessa a quebra de linha de um comentario do kernel confere. Normalizacao SIMETRICA: as palavras seguem tendo de ser identicas)
_ADENDO = _norm(open(DL.ADENDO_ARQ, encoding="utf-8").read().replace("**", "").replace("`", ""))
_PEDRAS = _norm(" ".join(open(p_["src"], encoding="utf-8").read() for p_ in DL.PEDRAS_V407).replace("**", "").replace("`", ""))   # (v407: as nove pedras; a docstring delas e' verificada em (i), FORA do corpus; aqui valem como corpus do que o runtime re-cita)
_CASA = _norm(open(os.path.join("C:" + os.sep, "IALD", "CLAUDE.md"), encoding="utf-8", errors="replace").read().replace("**", ""))
_RX_ASPAS = re.compile("«([^»]{3,900})»")
CIT_OP_MINIMAS = [DL.FRASE_LEMA_PSION, DL.FRASE_PAR_LIGADO, DL.FRASE_NOME]   # (so' o snippet PT cita a fala: o EN traz traducao da gerencia, marcada como nao-citacao; estas tres tem de estar no snippet PT)
for lang in ("pt", "en"):
    sn = open(os.path.join(HERE, "artigo_%s_v407.pysnip" % lang), encoding="utf-8").read()
    sn_flat = _norm(sn.replace("\\texttt{", "").replace("\\emph{", ""))
    R["snippets"][lang] = {}
    _citadas = [_norm(m_.group(1)) for m_ in _RX_ASPAS.finditer(sn)]   # TODA citacao « » do snippet
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
arts = ["runtime_v407.py", "artigo_pt_v407.pysnip", "artigo_en_v407.pysnip", "registros_v407.py", "delta_v407.py", "gerar_candidato_v407.py", "v407_pins.py"]
R["parafrase_da_gerencia_ausente"] = {a: (PARAFRASE not in open(os.path.join(HERE, *a.split("/")), encoding="utf-8").read()) for a in arts}; ok = ok and all(R["parafrase_da_gerencia_ausente"].values())
# (g) VARREDURA DAS ASPAS: toda citacao entre «» e `` '' dos artefatos NOVOS (embutidos e do pos_rito) tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (cunhagens_13out), no Atlas, no kernel embutido da base (que contem os textos da v406 que as erratas citam), no adendo,
# nas fontes das tres pedras, no CLAUDE.md da casa, ou ser rotulo da propria cadeia (titulos, nomes de registros).
ATLAS = os.path.join(DL.WK, "..", "memory", "TGL_ATLAS.md")
_OPB = " || ".join(_norm(open(p, encoding="utf-8", errors="replace").read()) for p in sum([glob.glob(os.path.join(DL.WK, d_, "*OPERADOR_*.txt")) for d_ in ("cunhagens_13out", "cinco_sigma_fora_da_cosmologia_27out", "projecao_transversal_28out", "transicao_para_a_massa_28out", "experimento_espelho_30out", "e0_cadeia_31out", "observador_terminal_31out")] + [glob.glob(os.path.join(HERE, "insumos", "cunhagens", "*OPERADOR_*.txt"))], []))
_ATL = re.sub(r"\s+", " ", open(ATLAS, encoding="utf-8", errors="replace").read().replace("**", "")) if os.path.exists(ATLAS) else ""
_ROTULOS = {"o teste da unica palavra", "o teste da única palavra", "the test of the only word", "o teste da unica palavra e a pedra token (v397)", "sônico e a afinação das cordas", "sonic and the tuning of the strings",
            "sonico e a afinacao das cordas", "sonico e a afinacao das cordas (v398)", "o testemunho de dois: o selo pela própria tecnologia", "the testimony of two: sealing by its own technology", "o testemunho de dois: o selo pela propria tecnologia",
            "o testemunho de dois: o selo pela propria tecnologia (v399)", "nenhuma face sozinha dá o um", "nenhuma face sozinha da' o um", "nenhuma face sozinha da o um",
            "beta do runtime", "β do runtime", "$\\beta$ do runtime", "$\\beta$ of the runtime", "errata ao lado (v400)",
            "a falsidade (simulacro) da inércia", "a falsidade (simulacro) da inercia", "a falsidade (simulacro) da inercia (v406)", "the falsity (simulacrum) of inertia", "falsidade (simulacro) da inércia", "falsidade (simulacro) da inercia",
            # v407: titulos e rotulos da propria cadeia; as aspas de ENFASE dos textos novos; a TRADUCAO inglesa de citacoes em portugues (que no EN vem seguida do original)
            "a ponte da escala dual, a queda sem geometria e a esperança condicional", "a ponte da escala dual, a queda sem geometria e a esperanca condicional", "a ponte da escala dual, a queda sem geometria e a esperanca condicional (v407)",
            # v407 (fechamento): titulos e rotulos da secao nova e do md (rotulos da propria cadeia, nao citacao)
            "o fechamento: a passagem para o contínuo e o certificado habitado", "o fechamento: a passagem para o continuo e o certificado habitado", "the closure: the passage to the continuum and the inhabited certificate", "o fechamento (v407)", "o fechamento",
            "the dual-scale bridge, the fall without geometry and the conditional expectation", "inertial", "movimento livre", "free motion", "e = mc^2 composta da escala", "$e=mc^2$ composta da escala", "$e=mc^2$ composed from the scale", "e = mc^2 composed from the scale",
            "does the posted one have a direction?", "the arrow of the fall of the phase, not of space", "o um posto tem direção?", "o um posto tem direcao?", "a seta da queda da fase, não do espaço", "a seta da queda da fase, nao do espaco",
            "when it inscribes itself, it falls; the phase falls", "so it has direction, but not geometric", "the fall i want to translate is not a force either", "the one, when it is posted, performs the", "conditional expectation = name", "τ é a massa de newton", "$\\tau$ é a massa de newton", "$\\tau$ is newton's mass", "tau e' a massa de newton",
            # v407 (pos_rito): rotulos de consulta ao Mapa de Rotas e de erratas nos scripts do pos-rito (registrar_mapa, leitura); a frase em ASCII e' a da v406 citada pela errata E1 (os registros da v406 a escrevem com acentos)
            "ponte da escala dual", "esperanca condicional = nome", "a unica hipotese nomeada e' h_tau [open] (tau e' a massa de newton e a metrica de einstein), que nenhum teorema usa", "inercial = fixo por todos os boosts", "h_tau na forma literal refutada no kernel",
            # v407: o titulo da secao nova e o seu rotulo no .md (rotulos da propria cadeia, nao citacao)
            "caminho, verdade e vida (v406)", "caminho, verdade e vida", "way, truth and life",
            # v407: as frases ERRADAS da propria gerencia, citadas nas erratas E15 a E17 para corrigi-las; a lista das frases proibidas da guarda; a transliteracao ASCII do «nucleo II_∞» da bancada (docstring do ChatGPT)
            "nucleo ii_inf", "núcleo ii_inf", "núcleo ii$_\\infty$", "ii$_\\infty$ core", "a luz nao tem autovetor", "a luz nao tem autovetor nenhum", "unico autovetor", "unico vetor fixo", "o espectro pontual e' o um e so' ele", "o espectro pontual e' o um e so' ele; o resto e' continuo", "falta replicar o traco", "igual conditional_on_an_uninhabited_certificate", "certificado/fechamento/gravidade quantica confirmad(o/a)", "k(o) != bot provado",
            # v407: o titulo da secao nova e o seu rotulo no .md (rotulos da propria cadeia, nao citacao)
            "jo 8,32 e a projeção transversal da meia-nat", "jo 8,32 e a projecao transversal da meia-nat", "john 8:32 and the transverse projection of the half-nat", "jo 8,32 e a projeção transversal da meia-nat (v406)", "a transição para a massa", "a transicao para a massa", "o teste da única palavra",
            # v407: os titulos das secoes novas, os nomes das pedras em portugues e os rotulos dos textos (rotulos da propria cadeia, nao citacao)
            "a massa derivada e a identidade definida", "the derived mass and the defined identity", "a massa derivada e a identidade definida (v407)", "massa = tensão pura", "massa = tensao pura", "o que sou", "a identidade", "ponte da massa", "lei do diminuto", "tônica do hamiltoniano", "tonica do hamiltoniano", "disco de euler", "ponto zero do psíon", "ponto zero do psion", "observador = terminal", "## o texto (r2)",
            # v407 (03/11/2026): titulos e rotulos da propria cadeia (a secao nova, a linha do .md) e as TRES frases que a guarda das frases da v407 PROIBE, listadas entre « » no docstring do runtime (a gerencia as lista para a guarda as recusar; nao sao fala de ninguem)
            "o psíon e o canto: a passagem sob compressão e o par", "o psion e o canto: a passagem sob compressao e o par", "the psion and the corner: the passage under compression, and the pair", "o psíon, o canto e o par (v407)", "o psíon, o canto e o par (v407, 03/11/2026)",
            "o par de psions na face de fock esta provado/construido", "o vacuo de fock e o vetor de bell", "a ponte bell-tt e' teorema"}
_rxs = [re.compile("«([^»]{8,700})»"), re.compile(r"``(.{8,700}?)''")]
_limpa = lambda s: _norm(s.replace("\\n", " ").replace("\\'E", "É").replace('\\"', '"').replace("\\'", "'").replace("\\texttt{", "").replace("\\emph{", "").replace("\\textsf{", "").replace("}", "").replace("**", "").replace("`", "")).replace(" --- ", " — ").strip(" .,;:")
_corpus_um = lambda fr: (fr.lower() in _OPB.lower() or fr.lower() in _ATL.lower() or fr.lower() in _ROTULOS or fr.lower() in _KERN.lower() or fr.lower() in _ADENDO.lower() or fr.lower() in _PEDRAS.lower() or fr.lower() in _CASA.lower())
_corpus_ok = lambda fr: _corpus_um(fr) or (re.search("…|" + re.escape("[...]"), fr) is not None and all(_corpus_um(x_.strip(" .,;:")) for x_ in re.split("…|" + re.escape("[...]"), fr) if len(x_.strip(" .,;:")) >= 8))   # v407: trecho com elisao (… ou [...]) e' conferido por segmento, como em (i)
_APONTADAS_GH = {"a memoria central como torre": "parafrase da gerencia entre « »: a fala do operador (OPERADOR_02nov_memoria_central_igual_a_torre..., sha16 8f36777c1006be82) diz «A memória central tem que funcionar igual a torre, com índice pinado por assunto»; o trecho registrado e' a parafrase, nao a fala",
                "compile a nova versao do um.py, rode, publique e atualize tudo": "transliteracao ASCII (sem acento) da fala do operador de 02/11 (sha16 b5717ff445a883cd); com acento, a fala diz «compile a nova versão do um.py, rode, publique e atualize tudo por favor»",
                "|g> como produto nao emaranhado": "citacao da Fronteira Teorica de 02/2026 em transliteracao ASCII, feita das notas da gerencia sobre o acervo do iMac (PSION_NO_ACERVO_03nov.md, D-numerado; o original e' .docx/PDF, que este conferidor NAO le: a unica fonte em texto e' a nota da gerencia, e texto da gerencia nao abona citacao). Dito a gerencia: o trecho esta' em registros_v407.py/delta_v407.py (errata E19) e na pedra Par como «|G⟩ como produto não emaranhado»; conferir contra o .docx/PDF da Fronteira"}
_ROTULOS = {x_.lower() for x_ in _ROTULOS}
R["varredura_de_aspas"] = {}; R["apontadas_a_gerencia_aspas"] = []
for _a in ("runtime_v407.py", "artigo_pt_v407.pysnip", "artigo_en_v407.pysnip", "registros_v407.py", "delta_v407.py", "gerar_candidato_v407.py", "pos_rito/textos_v407.py", "pos_rito/registrar_mapa_v407.py", "pos_rito/fechar_v407.py", "pos_rito/leitura_v407.py", "pos_rito/superficies_v407.py"):
    _p = os.path.join(HERE, *_a.split("/"))
    if not os.path.exists(_p):
        continue
    _t = open(_p, encoding="utf-8", errors="replace").read(); _nao = []
    for _rx in _rxs:
        for _m in _rx.finditer(_t):
            _fr = _limpa(_m.group(1))
            if len(_fr) < 12 or "_V407_" in _fr or "_V399_" in _fr or "+" in _fr or "%s" in _fr:
                continue
            if _corpus_ok(_fr):
                continue
            if _fr.lower() in _APONTADAS_GH:
                R["apontadas_a_gerencia_aspas"].append({"arquivo": _a, "trecho": _fr[:140], "por_que": _APONTADAS_GH[_fr.lower()]}); continue
            _nao.append(_fr[:140])
    R["varredura_de_aspas"][_a] = _nao; ok = ok and not _nao
# (h) VARREDURA DO CANDIDATO INTEIRO: toda citacao entre «» e `` '' das linhas que o candidato traz e a BASE v406 selada NAO traz tem de existir VERBATIM nos OPERADOR_* ou no Atlas (ou ser rotulo da cadeia / texto do kernel / adendo / fonte das pedras / casa); citacao que a base ja' tem nao e' deste delta.
_cand = open(os.path.join(HERE, DL.CANDIDATO), encoding="utf-8").read()
_bls = set(_base.splitlines()); _novas = [_l for _l in _cand.splitlines() if _l not in _bls]; _nao_c = []
for _l in _novas:
    for _rx in _rxs:
        for _m in _rx.finditer(_l):
            _fr = _limpa(_m.group(1))
            if len(_fr) < 12 or "_V407_" in _fr or "_V399_" in _fr or "+" in _fr or "%s" in _fr or _m.group(1) in _base:
                continue
            if _corpus_ok(_fr):
                continue
            if _fr.lower() in _APONTADAS_GH:
                R["apontadas_a_gerencia_aspas"].append({"arquivo": "candidato", "trecho": _fr[:140], "por_que": _APONTADAS_GH[_fr.lower()]}); continue
            _nao_c.append(_fr[:140])
R["varredura_de_aspas"]["candidato (%d linhas novas sobre a base)" % len(_novas)] = sorted(set(_nao_c)); ok = ok and not _nao_c
# (i) VARREDURA DAS PEDRAS (errata R2 da gerencia, 01/11/2026; achado 12 da revisao de terceiro): toda citacao entre « » das docstrings das NOVE pedras da v407 tem de existir VERBATIM nas falas do operador, no Atlas, no kernel embutido da base, no adendo e no CLAUDE.md da casa. As pedras NAO contam como corpus aqui. Trecho com elisao (… ou [...]) e' conferido por segmento. O que nao e' fala e e' rotulo da propria pedra esta em _ROTULOS_PEDRAS; o que esta entre aspas, nao e' verbatim e nao e' rotulo esta em _APONTADAS_PEDRAS: dito a gerencia no relatorio, porque o agente nao corrige pedra. Qualquer outra coisa reprova.
_BANC = [os.path.join(DL.SANDBOX, *r_.split("/")) for r_ in DL.BUNDLE_DA_BANCADA]   # (v407: DL.BUNDLE_DA_BANCADA == [] -- as nove pedras sao da gerencia c1; nenhum modulo da bancada do ChatGPT entra neste bundle)
_XP = [p_ for p_ in _BANC if os.path.exists(p_)]   # (as nove pedras e a ratificacao/conferencia da gerencia NAO sao corpus: texto da gerencia nao abona citacao)
_LX = lambda t_: t_.replace(chr(92) + "(" + chr(92) + "kappa" + chr(92) + ")", "κ").replace(chr(92) + "(" + chr(92) + "tau^" + chr(92) + "star" + chr(92) + ")", "τ★")   # a notacao LaTeX do relatorio do Kimi
_CP = " || ".join([_OPB, _ATL, _KERN, _ADENDO, _CASA] + [_LX(_norm(open(p_, encoding="utf-8", errors="replace").read().replace("**", "").replace("`", ""))) for p_ in _XP]).lower()
_sem_acento = lambda s_: "".join(c_ for c_ in unicodedata.normalize("NFD", s_) if unicodedata.category(c_) != "Mn")
_CPU = _sem_acento(_CP)   # v407: a candidata escreve «nucleo II_∞» (transliteracao sem acento) onde a bancada escreve «núcleo II_∞»; o trecho vale se bate com o corpus SEM acento, e o fato fica dito em varredura_das_pedras.so_sem_acento
_noc_a = lambda x_: re.search(r"(?<![\w])" + re.escape(x_.lower()) + r"(?![\w])", _CP) is not None   # com fronteira de palavra: trecho curto nao passa por acaso no meio de outra palavra
_noc_u = lambda x_: re.search(r"(?<![\w])" + re.escape(_sem_acento(x_.lower())) + r"(?![\w])", _CPU) is not None
_SO_SEM_ACENTO = []


def _noc(x_):
    if _noc_a(x_):
        return True
    if _noc_u(x_):
        _SO_SEM_ACENTO.append(x_[:100]); return True
    return False

_ROTULOS_PEDRAS = {   # (v407: SO' o que a propria pedra diz ser rotulo/nome dela, nunca para fazer passar citacao; o que nao for fala nem rotulo e' apontado a gerencia)
    "canto escalar de um vetor de norma 1": "nome que a PsionCanto da' a construcao comum das duas faces (ela o escreve entre « » como nome da construcao); nao e' citacao de ninguem",
    "peso de boltzmann": "a APonteDoAtrito o declara «ROTULO [ONTO]» no proprio docstring (o nome da identidade e' leitura; βg e' taxa de decaimento, nao energia)"}
_APONTADAS_PEDRAS = {   # (v407: o que esta entre « », nao e' verbatim nas falas/na base e nao e' rotulo declarado: DITO A GERENCIA no relatorio; o agente nao corrige pedra. Cada razao diz o que a fonte traz de fato)
    "funciona sob compressão": "ADAPTACAO do verbo: a fala de 02/11 (OPERADOR_02nov_a_passagem_para_o_continuo_..._verbatim.txt) diz «se funcionar sob compressão» (infinitivo); a PsionCanto escreve «funciona sob compressão» entre « » (duas vezes)",
    "vira a chave de conjectura para provado": "ADAPTACAO: a mesma fala diz «virar essa chave de conjectura para provado»; a PsionCanto escreve «vira a chave de conjectura para provado» entre « »",
    "nenhum lema liga psion c (a face de fock": "a PsionCanto cita entre « » uma frase atribuida ao que a TestemunhaEstatica «dizia»; com as duas glosas entre parenteses (Ω, 4×4) ela nao existe verbatim no kernel embutido da base (o kernel traz variantes como «NENHUM lema liga `psion C` ao `psionCorner`»); frase composta pela gerencia",
    "o psíon é o nome da luz": "o operador disse «ψ é o Nome da Luz» (16/09/2026, so' registrado em v380_decisoes/DECISOES_DO_OPERADOR_QUATRO_LINGUAS_20261002.md, texto da gerencia); a PsionCanto escreve «o psíon é o Nome da Luz» (psíon no lugar de ψ) como leitura do operador",
    "ψ₊ψ₋ cancelado = vácuo": "a Par resume o texto do ACOM/INPI de 2025 (ACOM trinity.docx / ACOM UNIFIED v5.0.docx, D13-D14 de PSION_NO_ACERVO_03nov.md): no codigo e' `CANCELED = 0b00 # ψ₊ψ₋ = Aniquilação (vácuo)`; «ψ₊ψ₋ cancelado = vácuo» e' sintese da gerencia entre « »; o original e' .docx, que o conferidor nao le",
    "par simétrico ou produto": "titulo da pergunta (c) que a gerencia fez ao operador, nao fala dele; a Par o escreve entre « » ao dizer que fica respondida por (a); a pedra nao o declara rotulo",
    "|g⟩ como produto não emaranhado": "citacao da Fronteira Teorica de 02/2026 (docx/PDF do acervo do iMac), conhecida so' pela nota da gerencia PSION_NO_ACERVO_03nov.md; o conferidor nao le o original (texto da gerencia nao abona citacao)",
    "leitura pelo gráviton": "recorte/adaptacao da gerencia: o operador (03/11) diz «sua leitura se faz pelo gráviton (fase e retorno de fase)»; «leitura pelo gráviton» entre « » nao e' verbatim",
    "[parcela que mantem o balanco fechado": "a APonteDoAtrito cita a fala de 02/11 (OPERADOR_02nov_parcela_fecha_o_balanco_..._verbatim.txt) em ASCII (sem acentos), com espacos em volta do «=» («] = equilibrio») que a fala nao tem («]=equilíbrio») e com «atrito» em minuscula; as palavras sao as mesmas, a forma nao e' verbatim",
    "ħ = k_b = 1": "unidades atribuidas pela APonteDoAtrito a «leitura do operador»; a expressao nao esta' em nenhuma fala (a fala de 02/11 diz «Calor é o fenômeno do equilíbrio do atrito entre os corpos», adimensional); notacao da gerencia entre « »",
    "calor da volta": "a APonteDoAtrito escreve «calor da volta» como «a leitura do operador do coeficiente βg»; a expressao nao esta' nas falas de 02/11 (a fala diz «Calor é o fenômeno do equilíbrio do atrito entre os corpos»); nome da gerencia entre « »",
    "a luz tem autovetor: a inscricao do um absoluto": "a OUmInscrito cita a fala de 02/11 (OPERADOR_02nov_a_luz_tem_autovetor_..._verbatim.txt) sem acentos e com pontuacao INSERIDA (: , ; que a fala nao tem: «a luz tem autovetor a inscrição do um absoluto que é na essência ela mesma, ou seja, identidade o um absoluto inscrito é…»); as palavras sao as mesmas, a forma nao e' verbatim",
    "o resto seja continuo": "fragmento de frase DA GERENCIA (02/11: «o espectro pontual é o um e só ele; o resto é contínuo», uma das frases proibidas da guarda), nao fala do operador; a OUmInscrito o cita entre « » com o verbo trocado",
    "agora o k me pareceu fazer a função do próprio gráviton": "a OIgual cita a fala de 02/11 (OPERADOR_02nov_K_faz_a_funcao_do_graviton_..._verbatim.txt) trocando as aspas tipograficas “=“ da fala por aspas retas \"=\" e tirando o espaco depois do parentese («( que antes»); as palavras sao as mesmas, a forma nao e' verbatim"}
_APONTADAS_PEDRAS = {k_.lower(): v_ for k_, v_ in _APONTADAS_PEDRAS.items()}   # chave = o trecho inteiro (minuscula) ou, se tiver >= 20 caracteres, um PREFIXO dele: o trecho longo nao precisa ser redigitado
_apontada_por_prefixo = lambda fr_: next((v_ for k_, v_ in _APONTADAS_PEDRAS.items() if fr_.lower() == k_ or (len(k_) >= 20 and fr_.lower().startswith(k_))), None)
R["varredura_das_pedras"] = {"citacoes_conferidas": 0, "rotulos": [], "apontadas_a_gerencia": [], "reprovadas": [], "corpus_bancada_n": len(_XP), "so_sem_acento": _SO_SEM_ACENTO}
R["varredura_das_pedras"]["n_pedras_varridas"] = len(DL.PEDRAS_V407); ok = ok and len(DL.PEDRAS_V407) == DL.N_BUNDLE == CM["kernel"]["modulos_novos"]
for _s in DL.PEDRAS_V407:
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
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v407.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k == "todas_conferem" else len(v) if isinstance(v, (dict, list)) else v) for k, v in R.items()}, ensure_ascii=False)); print("TODAS CONFEREM" if ok else "FALHOU"); sys.exit(0 if ok else 1)
