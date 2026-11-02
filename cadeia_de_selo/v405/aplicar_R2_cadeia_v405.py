# -*- coding: utf-8 -*-
"""aplicar_R2_cadeia_v405.py -- a parte de CADEIA da errata R2 da gerencia c1: as guardas novas (guarda_frases varre as oito pedras; conferir_citacoes confere as docstrings das pedras), o recibo R2 nos insumos, o p00, o ensaio, o conferidor e o pos-rito. Cada substituicao exige a contagem exata (fail-closed). Tudo ou nada; backup de BYTES; temporario -> conferir -> os.replace. Roda uma vez so'."""
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")
NOVOS = {}


def carrega(arq):
    if arq not in NOVOS:
        NOVOS[arq] = open(os.path.join(HERE, arq), "rb").read().decode("utf-8")
    return NOVOS[arq]


def sub(arq, old, new, n=1):
    s = carrega(arq); c = s.count(old)
    assert c == n, (arq, c, n, old[:100])
    NOVOS[arq] = s.replace(old, new)


# ===================================================================================================== guarda_frases_v405.py
G = "guarda_frases_v405.py"
sub(G, "Identificador Lean rebatizado (minusculas com sublinhado) e' citacao da errata E13, nao frase. As pedras (.lean) e as falas embutidas NAO passam por esta guarda: as pedras trazem a correcao AO LADO nas docstrings.",
    "Identificador Lean rebatizado (minusculas com sublinhado) e' citacao da errata E13, nao frase. AO LADO (errata R2 da gerencia, 01/11/2026): a guarda passa a varrer tambem as OITO PEDRAS (pedras(), o achado 6 da revisao de terceiro), com as falas do operador como excecao: o trecho entre « » conferido verbatim contra as falas embutidas sai antes da varredura; o resto da pedra e' texto da gerencia e passa pelas mesmas regras. Frase de pedra reprovada e' apontada a gerencia: quem corrige e' ela; o gerador do candidato para.")
sub(G, "import json, os, sys\n", "import json, os, re, sys\n")
sub(G, '''def controle_negativo():
    r = {"proibidas": {}, "limpas": {}, "fala_do_operador": {}}
''', '''_norm = lambda s_: re.sub(r"\\s+", " ", str(s_).replace(chr(8217), "'")).strip()


def _falas_do_operador():
    """o corpus das excecoes das pedras: as falas embutidas (os arquivos de VERBATIM_ORIGEM_V405), em minusculas e com o espaco normalizado."""
    return " || ".join(_norm(open(p_, encoding="utf-8", errors="replace").read()) for p_ in DL.VERBATIM_ORIGEM_V405).lower()


def sem_falas(txt, falas):
    """retira de uma pedra os trechos entre « » que sao fala verbatim do operador (trecho com elisao e' conferido por segmento); devolve (texto_sem_as_falas, n_retiradas). As quebras de linha das docstrings ('> ') sao juntadas antes."""
    n_ = [0]

    def fora(m_):
        fr_ = _norm(m_.group(1).replace("`", "").replace("**", "")).strip(" .,;:")
        segs_ = [x_.strip(" .,;:") for x_ in re.split(r"…|\\[\\.\\.\\.\\]", fr_) if len(x_.strip(" .,;:")) >= 4]
        if segs_ and all(x_.lower() in falas for x_ in segs_):
            n_[0] += 1
            return " "
        return m_.group(0)
    return re.sub("«([^»]{4,900})»", fora, _norm(re.sub(r"\\n>\\s*", " ", str(txt)))), n_[0]


def pedras():
    """a varredura das OITO pedras (errata R2): {modulo: {violacoes, falas_retiradas}}."""
    falas = _falas_do_operador(); out = {}
    for s_ in DL.STONES:
        t_, n_ = sem_falas(open(s_["src"], encoding="utf-8").read(), falas)
        out[s_["name"]] = {"violacoes": [list(v_) for v_ in RT._v405_guarda_frases(t_)], "falas_retiradas": n_}
    return out


def controle_negativo():
    r = {"proibidas": {}, "limpas": {}, "fala_do_operador": {}}
''')
sub(G, '''    r["ok"] = bool(all(r["proibidas"].values()) and not any(r["limpas"].values()) and not r["fala_do_operador"]["com_a_excecao"] and r["fala_do_operador"]["sem_a_excecao"])
    return r
''', '''    falas_ = _falas_do_operador()                 # o controle da varredura das pedras: a frase da gerencia reprova; a fala do operador entre « » passa; a mesma fala SEM aspas reprova; uma parafrase entre « » reprova
    r["pedras_controle"] = {"frase_da_gerencia_reprovada": bool(RT._v405_guarda_frases(sem_falas("a transicao ficou com tudo derivado aqui", falas_)[0])),
                            "fala_entre_aspas_passa": not RT._v405_guarda_frases(sem_falas("«" + DL.FRASE_NOMES + "»", falas_)[0]),
                            "fala_quebrada_em_docstring_passa": not RT._v405_guarda_frases(sem_falas("> «" + DL.FRASE_NOMES[:40] + "\\n>  " + DL.FRASE_NOMES[40:] + "»", falas_)[0]),
                            "parafrase_entre_aspas_reprovada": bool(RT._v405_guarda_frases(sem_falas("«agora ficou tudo derivado»", falas_)[0]))}
    r["ok"] = bool(all(r["proibidas"].values()) and not any(r["limpas"].values()) and not r["fala_do_operador"]["com_a_excecao"] and r["fala_do_operador"]["sem_a_excecao"] and all(r["pedras_controle"].values()))
    return r
''')
sub(G, '''    c = controle_negativo()
    json.dump(c, open(os.path.join(HERE, "GUARDA_FRASES_v405.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
''', '''    c = controle_negativo()
    c["pedras"] = pedras(); c["pedras_limpas"] = not any(v_["violacoes"] for v_ in c["pedras"].values())
    if not c["pedras_limpas"]:
        print("FRASE DE PEDRA REPROVADA (apontar a gerencia, nao corrigir):", {k_: v_["violacoes"][:3] for k_, v_ in c["pedras"].items() if v_["violacoes"]})
    json.dump(c, open(os.path.join(HERE, "GUARDA_FRASES_v405.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
''')
sub(G, '''    rc = 0 if c["ok"] else 1
''', '''    print("pedras:", "LIMPAS" if c["pedras_limpas"] else "REPROVADAS", "| falas retiradas:", sum(v_["falas_retiradas"] for v_ in c["pedras"].values()))
    rc = 0 if (c["ok"] and c["pedras_limpas"]) else 1
''')

# ===================================================================================================== gerar_candidato_v405.py (a guarda das pedras entra no gerador e no CANDIDATO.json)
Y = "gerar_candidato_v405.py"
sub(Y, '''G0_ = GF.controle_negativo(); assert G0_["ok"], "o controle negativo da guarda das frases falhou"\n''',
    '''G0_ = GF.controle_negativo(); assert G0_["ok"], "o controle negativo da guarda das frases falhou"\nGP_ = GF.pedras(); assert not any(v_["violacoes"] for v_ in GP_.values()), ("FRASE PROIBIDA numa pedra: apontar a gerencia, nao corrigir", {k_: v_["violacoes"][:2] for k_, v_ in GP_.items() if v_["violacoes"]})\n''')
sub(Y, '''"violacoes_no_texto_novo": len(V_GF)},''', '''"violacoes_no_texto_novo": len(V_GF), "pedras_varridas": len(GP_), "violacoes_nas_pedras": sum(len(v_["violacoes"]) for v_ in GP_.values())},''')

# ===================================================================================================== copiar_insumos_v405.py
sub("copiar_insumos_v405.py", '''(os.path.basename(RG.RECIBO_ERRATA_ARQ), RG.RECIBO_ERRATA_ARQ), (os.path.basename(DL.GA_RECLASS_ARQ),''', '''(os.path.basename(RG.RECIBO_ERRATA_ARQ), RG.RECIBO_ERRATA_ARQ), (os.path.basename(RG.RECIBO_ERRATA_R2_ARQ), RG.RECIBO_ERRATA_R2_ARQ), (os.path.basename(DL.GA_RECLASS_ARQ),''')

# ===================================================================================================== lote D3: conferir_citacoes confere as docstrings das pedras
D3 = "derivar_encanamento_v405_regrasD3_diff_citacoes.py"
sub(D3, '''entrada("conferir_citacoes_v404.py", autoral=True, regras=[\n''', '''_RX_PEDRAS = \'\'\'# (i) VARREDURA DAS PEDRAS (errata R2 da gerencia, 01/11/2026; achado 12 da revisao de terceiro): toda citacao entre « » das docstrings das oito pedras tem de existir VERBATIM nas falas do operador, no Atlas, no kernel embutido da base, no adendo, no CLAUDE.md da casa ou nas fontes que a propria pedra nomeia (o ensaio r2 ratificado, o relatorio do Kimi, a ordem E0, paper_PT.tex e o Tratado). As pedras NAO contam como corpus aqui. Trecho com elisao (… ou [...]) e' conferido por segmento. O que nao e' fala e e' rotulo da propria pedra esta em _ROTULOS_PEDRAS; o que esta entre aspas, nao e' verbatim e nao e' rotulo esta em _APONTADAS_PEDRAS: dito a gerencia no relatorio, porque o agente nao corrige pedra. Qualquer outra coisa reprova.
_XP = [DL._ENSAIO_R2_MD, os.path.join(DL.WK, "neutrino_E0_autonomia_30out", "RELATORIO_KIMI_E0_01_31out.md"), os.path.join(DL.ESTUDO_E0, "ORDEM_KIMI_E0_01_31out.md"), os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "paper_PT.tex"), os.path.join("C:" + os.sep, "IALD", "Artigo", "Tratado", "secao_03_particulas.tex"), os.path.join(HERE, "insumos", "CONFERENCIA_E0_KIMI_E_CADEIA_31out.md")]
_CP = " || ".join([_OPB, _ATL, _KERN, _ADENDO, _CASA] + [_norm(open(p_, encoding="utf-8", errors="replace").read().replace("**", "").replace("`", "")) for p_ in _XP if os.path.exists(p_)]).lower()
_ROTULOS_PEDRAS = {"os campos fechados": "titulo de secao da propria pedra", "o que resta de entrada é o acoplamento e o um posto": "frase da propria pedra, corrigida na nota ao lado", "proporcional / derivada": "rotulo do par de leituras", "acoplamento da onda = massa inscrita": "rotulo da gerencia para a hipotese do teorema",
                   "a massa é o que a volta paga e fecha, ou o que a volta deixa sem fechar? e, se é o que paga, de que lado se lê: no que atravessa ou no que fica?": "a pergunta formulada pela gerencia a pedido do operador (o pedido e\\' a fala; a pergunta nao)"}
_APONTADAS_PEDRAS = {"r é o pagamento": "PontoZeroDoPsion: nome de lei entre aspas; a fala e\\' «A curvatura não é curvatura, é o pagamento»", "observador = gravidade viva: opera, permanece, é o terminal": "ObservadorTerminal: composicao de titulo e linha da tabela do Atlas (cunhagem 78_), nao texto corrido"}
R["varredura_das_pedras"] = {"citacoes_conferidas": 0, "rotulos": [], "apontadas_a_gerencia": [], "reprovadas": []}
for _s in DL.STONES:
    _t = _norm(re.sub(r"\\\\n>\\\\s*", " ", open(_s["src"], encoding="utf-8").read()))
    for _m in re.finditer("«([^»]{8,900})»", _t):
        _fr = _norm(_m.group(1).replace("`", "").replace("**", "")).strip(" .,;:")
        _sg = [x_.strip(" .,;:") for x_ in re.split(r"…|\\\\[\\\\.\\\\.\\\\.\\\\]", _fr) if len(x_.strip(" .,;:")) >= 8]
        if all(x_.lower() in _CP for x_ in _sg):
            R["varredura_das_pedras"]["citacoes_conferidas"] += 1
        elif _fr.lower() in _ROTULOS_PEDRAS:
            R["varredura_das_pedras"]["rotulos"].append({"pedra": _s["name"], "trecho": _fr[:120], "por_que": _ROTULOS_PEDRAS[_fr.lower()]})
        elif _fr.lower() in _APONTADAS_PEDRAS:
            R["varredura_das_pedras"]["apontadas_a_gerencia"].append({"pedra": _s["name"], "trecho": _fr[:120], "por_que": _APONTADAS_PEDRAS[_fr.lower()]})
        else:
            R["varredura_das_pedras"]["reprovadas"].append({"pedra": _s["name"], "trecho": _fr[:160]})
ok = ok and not R["varredura_das_pedras"]["reprovadas"] and R["varredura_das_pedras"]["citacoes_conferidas"] > 0
\'\'\'
entrada("conferir_citacoes_v404.py", autoral=True, regras=[
    ('R["todas_conferem"] = ok\\n', _RX_PEDRAS + 'R["todas_conferem"] = ok\\n', 1),
''')
sub(D3, '''no adendo de 03-04/09, nas fontes das oito pedras, no CLAUDE.md da casa ou ser rotulo da propria cadeia. Sai 0 se tudo bate.''', '''no adendo de 03-04/09, nas fontes das oito pedras, no CLAUDE.md da casa ou ser rotulo da propria cadeia; (i) as docstrings das OITO PEDRAS: toda citacao entre « » delas tem de existir verbatim, com as pedras FORA do corpus (errata R2; o que nao e' fala e' rotulo listado; o que nao e' verbatim nem rotulo e' apontado a gerencia). Sai 0 se tudo bate.''')

# ===================================================================================================== lote C2: o ensaio a seco
C2 = "derivar_encanamento_v405_regrasC2_ensaio.py"
sub(C2, '''and [l_["n"] for l_ in (_xf5.get("o_que_entra") or {}).get("quatro_leituras", [])] == [1, 2, 3, 4] and all(l_["definicao_lean"] in _sp5c["kernel_decls"] and l_["entra_como"] == "DEFINICAO, nao teorema" for l_ in (_xf5.get("o_que_entra") or {}).get("quatro_leituras", []))''',
    '''and [l_["n"] for l_ in (_xf5.get("o_que_entra") or {}).get("leituras_da_cadeia_da_massa", [])] == [l_["n"] for l_ in DL.LEITURAS_DEFINICOES] and (_xf5.get("o_que_entra") or {}).get("lista_de_leituras_fechada") is False and all(l_["definicao_lean"] in _sp5c["kernel_decls"] and l_["entra_como"].endswith(", nao teorema") for l_ in (_xf5.get("o_que_entra") or {}).get("leituras_da_cadeia_da_massa", []))''')
sub(C2, '''len(_xf5.get("teoremas_rebatizados_antes_do_selo") or {}) == 3 and DL.ERRATA_E13''', '''len(_xf5.get("teoremas_rebatizados_antes_do_selo") or {}) == 4 and DL.ERRATA_E13''')

# ===================================================================================================== lote D1: o conferidor
D1 = "derivar_encanamento_v405_regrasD1_conferidor.py"
sub(D1, "as decisoes D27 a D33, os campos fechados, os dois postos e as quatro leituras estao no registro;", "as decisoes D27 a D33, os campos fechados, os dois postos e as leituras da cadeia da massa estao no registro;")
sub(D1, '''[l_["n"] for l_ in ((CF5.get("extras") or {}).get("o_que_entra") or {}).get("quatro_leituras", [])] == [1, 2, 3, 4] and''', '''[l_["n"] for l_ in ((CF5.get("extras") or {}).get("o_que_entra") or {}).get("leituras_da_cadeia_da_massa", [])] == [l_["n"] for l_ in DL.LEITURAS_DEFINICOES] and''')

# ===================================================================================================== lote E1: o p00
E1 = "derivar_encanamento_v405_regrasE1_p00.py"
s_ = carrega(E1); i_ = s_.index('_rec_err = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_01nov.json"))'); j_ = s_.index("'''\nentrada(\"p00_precondicoes_v404.py\"")
NOVOS[E1] = s_[:i_] + '''_rec_err = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_01nov.json"))
_rec_r2 = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_R2_01nov.json"))
chk("[v405] as pedras sao as da ERRATA R2 da gerencia: o sha256 de cada arquivo == o sha256_depois do recibo vigente (oito arquivos), e o sha256_antes do R2 fecha a cadeia de custodia com o sha256_depois do R1 (sete arquivos; os recibos antigos ficam como registro); duas mudancas de codigo no R2", all(sha(rd(os.path.join(HERE, "pedra", k_ + ".lean"))) == v_["sha256_depois"] for k_, v_ in _rec_r2["pedras"].items()) and len(_rec_r2["pedras"]) == 8 and all(_rec_r2["pedras"][a_["modulo"]]["sha256_antes"] == a_["sha256_depois"] for a_ in _rec_err["arquivos"]) and len(_rec_err["arquivos"]) == 7 and len(_rec_err["teoremas_renomeados"]) == 3 and len(_rec_r2["codigo_mudado"]) == 2, len(_rec_r2["pedras"]))
chk("[v405, a lista de exclusao] nenhuma fala de VERBATIM_EXCLUIDAS_V405 esta no candidato: o sha16 nao aparece nas cunhagens do CANDIDATO_v405.json nem na copia duravel insumos\\\\cunhagens", not any(k_ in json.dumps(CM["cunhagens"]) for k_ in DL.VERBATIM_EXCLUIDAS_V405) and not any(os.path.basename(p_)[:16] in DL.VERBATIM_EXCLUIDAS_V405 for p_ in glob.glob(os.path.join(HERE, "insumos", "cunhagens", "*"))), sorted(DL.VERBATIM_EXCLUIDAS_V405))
chk("[v405, a errata R2] a guarda das frases varreu as oito pedras (zero frase proibida fora das falas) e a conferencia de citacoes conferiu as docstrings delas (zero reprovada; as apontadas a gerencia ficam ditas no JSON)", CM["guarda_frases"]["pedras_varridas"] == 8 and CM["guarda_frases"]["violacoes_nas_pedras"] == 0 and not lj(os.path.join(HERE, "conferir_citacoes_v405.json"))["varredura_das_pedras"]["reprovadas"], lj(os.path.join(HERE, "conferir_citacoes_v405.json"))["varredura_das_pedras"]["citacoes_conferidas"])
''' + s_[j_:]

# ===================================================================================================== pos-rito: a leitura e os controles
A = os.path.join("pos_rito", "adaptar_pos_rito_v405.py")
sub(A, "o que entra (os dois postos e as quatro leituras, cada uma com a definicao Lean);", "o que entra (os dois postos e as leituras da cadeia da massa, lista que nao e' fechada, cada uma com o nome Lean);")
sub(A, """leit_ok_ = bool([l_.get('n') for l_ in ent_.get('quatro_leituras') or []] == [1, 2, 3, 4] and all(l_.get('entra_como') == 'DEFINICAO, nao teorema' and src_.get(l_.get('definicao_lean')) == l_.get('modulo') for l_ in ent_.get('quatro_leituras') or []))""",
    """leit_ok_ = bool([l_.get('n') for l_ in ent_.get('leituras_da_cadeia_da_massa') or []] == [l_['n'] for l_ in DL.LEITURAS_DEFINICOES] and ent_.get('lista_de_leituras_fechada') is False and all(str(l_.get('entra_como')).endswith(', nao teorema') and src_.get(l_.get('definicao_lean')) == l_.get('modulo') for l_ in ent_.get('leituras_da_cadeia_da_massa') or []))""")
sub(A, """'n_leituras': len(ent_.get('quatro_leituras') or []),""", """'n_leituras': len(ent_.get('leituras_da_cadeia_da_massa') or []),""")
sub(A, "cada campo fechado com os termos no trio, as quatro leituras e os dois postos com a definicao Lean no modulo certo)", "cada campo fechado com os termos no trio, as leituras da cadeia da massa e os dois postos com o nome Lean no modulo certo)")
A2 = os.path.join("pos_rito", "adaptar_regras2_v405.py")
sub(A2, "as quatro leituras do operador entram como DEFINICAO [INPUT/ONTO], nao sao teoremas;", "as leituras da cadeia da massa entram como DEFINICAO ou identificacao [INPUT/ONTO], nao sao teoremas, e a lista nao e' fechada;")
A3 = os.path.join("pos_rito", "adaptar_regras3_v405.py")
sub(A3, '''variante("campos: uma das quatro leituras dita teorema", f_core=lambda c: c["campos_fechados_e_leituras_v405"]["extras"]["o_que_entra"]["quatro_leituras"][0].update(entra_como="teorema"), espera="campos_fechados_e_leituras_v405 nao selou inteiro"),''',
    '''variante("campos: uma das leituras da cadeia da massa dita teorema", f_core=lambda c: c["campos_fechados_e_leituras_v405"]["extras"]["o_que_entra"]["leituras_da_cadeia_da_massa"][0].update(entra_como="teorema"), espera="campos_fechados_e_leituras_v405 nao selou inteiro"),''')
sub(A3, "campos_fechados_e_leituras_v405 (o que fechou, os dois postos, as quatro leituras que entram como definicao)", "campos_fechados_e_leituras_v405 (o que fechou, os dois postos, as leituras da cadeia da massa, que entram como definicao ou identificacao)")

# ===================================================================================================== o relatorio
Z = "gerar_relatorio_v405.py"
sub(Z, '''"o titulo da secao ficou «A massa derivada e a identidade definida», como a ordem pediu, qualificado pela moldura: «derivada» e' literal (a massa como derivada da projecao transversal, uma definicao)",''',
    '''"o titulo da secao fica «A massa derivada e a identidade definida», porque vem da fala dele; a moldura diz que a derivacao e' da forma, dadas as entradas, e que a leitura fisica segue leitura (decisao da gerencia, errata R2)",''')
sub(Z, '''"as docstrings das pedras mantem o cabecalho antigo com a nota AO LADO (a guarda das frases nao varre as pedras nem as falas)",''',
    '''"a guarda das frases passou a varrer as oito pedras, com as falas como excecao, e a conferencia de citacoes passou a conferir as docstrings delas (conferir_citacoes_v405.json, varredura_das_pedras); as frases apontadas a gerencia estao la: o agente nao corrige pedra",
    "checks tautologicos da revisao: enxuguei so' o du_ do g1 (comparava forma(57) com forma(57)); p6 e d6 ficam como estao, descritos como conferencia de identidade",
    "os nomes de declaracao com derivad- (transicaoDerivada, leiDerivada, emprestimoDerivado, angulo_derivado_do_absoluto) ficam: a decisao e' da gerencia; as docstrings avisam",''')
sub(Z, "Sha256 lidos do recibo de errata das pedras (`insumos\\\\RECIBO_ERRATA_PEDRAS_01nov.json`): nenhuma prova mudou; docstrings e três nomes de teorema mudaram porque o nome afirmava mais do que o teorema prova.",
    "Sha256 lidos do recibo vigente das pedras (`insumos\\\\RECIBO_ERRATA_PEDRAS_R2_01nov.json`, cadeia de custódia com o recibo da primeira errata): nenhuma prova existente mudou; quatro nomes de teorema mudaram porque o nome afirmava mais do que o teorema prova; o disco ganhou `the_flow_is_the_canonical_law` e o fecho do observador ganhou a leitura binária.")

for arq, novo in NOVOS.items():
    compile(novo, arq, "exec") if arq.endswith(".py") else None
for arq, novo in NOVOS.items():
    p = os.path.join(HERE, arq); b = open(p, "rb").read()
    bak = p + ".bak_" + TS + "_R2"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
    t = p + ".tmp_R2"; open(t, "wb").write(novo.encode("utf-8")); assert os.path.getsize(t) == len(novo.encode("utf-8")) and os.path.getsize(t) > 1000
    os.replace(t, p)
    print(arq, len(b), "->", len(novo.encode("utf-8")))
print("ok, backups .bak_%s_R2" % TS)
