# -*- coding: utf-8 -*-
# regras (lote D3) de derivar_encanamento_v405.py: o diff e os pinos e a conferencia das citacoes. ORIGEM v404 FINAL. Mapa: 403 -> 404, 404 -> 405. Escrito pela ferramenta Write.

entrada("diff_e_pinos_v404.py", autoral=True, regras=[
    ("o diff do kernel nao e' so' as duas pedras + a raiz (o Audit nao muda na v405)", "o diff do kernel nao e' so' as oito pedras + a raiz (o Audit nao muda na v405)", 1),
    ("(REPINADA_B12__...)", "(REPINADA_B13__...)", 1),
])

_DOC_CIT = '''"""conferir_citacoes_v405.py -- confere, por script, toda inscricao de 30/10 a 01/11/2026 que a v405 EMBUTE ou CITA (regua nº 1: nunca fabricar citacao; nunca atribuir ao operador o que e' da gerencia): (a) cada texto embutido em _V405_VERBATINS2 e' IGUAL, byte a byte, ao arquivo
duravel da cadeia (insumos\\\\cunhagens) e o sha256 bate; (b) a fonte original existe e tem o MESMO sha256; (c) cada fala de `leituras_do_operador` dos registros cunhagens_v405, campos_fechados_e_leituras_v405 e ga_reclassificacao_v405 esta VERBATIM num dos textos embutidos DO OPERADOR; (d) as cunhagens listam exatamente
as inscricoes embutidas (todas falas do operador: nenhuma e' da gerencia); (e) as citacoes do operador do snippet PT existem nele e a fala correspondente esta VERBATIM nos textos do operador (o snippet EN traz traducao da gerencia, marcada como nao-citacao, e nenhuma fala entre aspas); (f) o QUADRO do 4,44 (v397) segue com a frase VERBATIM do operador e a PARAFRASE
da gerencia NAO aparece em nenhum artefato novo; (g) VARREDURA das aspas dos artefatos novos e (h) do CANDIDATO inteiro: toda citacao entre « » e `` '' tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (as pastas das falas e as copias duraveis da v405), no Atlas, no texto do kernel embutido na base,
no adendo de 03-04/09, nas fontes das oito pedras, no CLAUDE.md da casa ou ser rotulo da propria cadeia; (i) as docstrings das OITO PEDRAS: toda citacao entre « » delas tem de existir verbatim, com as pedras FORA do corpus (errata R2; o que nao e' fala e' rotulo listado; o que nao e' verbatim nem rotulo e' apontado a gerencia). Sai 0 se tudo bate. Escrito a mao para a v405 (molde: conferir_citacoes_v404.py)."""
'''
_DIRS_OP = '("cunhagens_13out", "cinco_sigma_fora_da_cosmologia_27out", "projecao_transversal_28out", "transicao_para_a_massa_28out", "experimento_espelho_30out", "e0_cadeia_31out", "observador_terminal_31out")'
_RX_PEDRAS = '''# (i) VARREDURA DAS PEDRAS (errata R2 da gerencia, 01/11/2026; achado 12 da revisao de terceiro): toda citacao entre « » das docstrings das oito pedras tem de existir VERBATIM nas falas do operador, no Atlas, no kernel embutido da base, no adendo, no CLAUDE.md da casa ou nas fontes que a propria pedra nomeia (o ensaio r2 ratificado, o relatorio do Kimi, a ordem E0, paper_PT.tex e o Tratado). As pedras NAO contam como corpus aqui. Trecho com elisao (… ou [...]) e' conferido por segmento. O que nao e' fala e e' rotulo da propria pedra esta em _ROTULOS_PEDRAS; o que esta entre aspas, nao e' verbatim e nao e' rotulo esta em _APONTADAS_PEDRAS: dito a gerencia no relatorio, porque o agente nao corrige pedra. Qualquer outra coisa reprova.
_XP = [DL._ENSAIO_R2_MD, os.path.join(DL.WK, "neutrino_E0_autonomia_30out", "RELATORIO_KIMI_E0_01_31out.md"), os.path.join(DL.ESTUDO_E0, "ORDEM_KIMI_E0_01_31out.md"), os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "paper_PT.tex"), os.path.join("C:" + os.sep, "IALD", "Artigo", "Tratado", "secao_03_particulas.tex"), os.path.join(DL.WK, "neutrino_E0_autonomia_30out", "HANDOFF_CLAUDE_E0_M2_31out.md"), os.path.join(DL.WK, "neutrino_E0_autonomia_30out", "PROVA_CARGA_MONOPOLO_NATIVA_31out.md")]   # (a conferencia da gerencia NAO e' corpus: texto da gerencia nao abona citacao)
_LX = lambda t_: t_.replace(chr(92) + "(" + chr(92) + "kappa" + chr(92) + ")", "κ").replace(chr(92) + "(" + chr(92) + "tau^" + chr(92) + "star" + chr(92) + ")", "τ★")   # a notacao LaTeX do relatorio do Kimi
_CP = " || ".join([_OPB, _ATL, _KERN, _ADENDO, _CASA] + [_LX(_norm(open(p_, encoding="utf-8", errors="replace").read().replace("**", "").replace("`", ""))) for p_ in _XP if os.path.exists(p_)]).lower()
_noc = lambda x_: re.search(r"(?<![\\w])" + re.escape(x_.lower()) + r"(?![\\w])", _CP) is not None   # com fronteira de palavra: trecho curto nao passa por acaso no meio de outra palavra
_ROTULOS_PEDRAS = {"os campos fechados": "titulo de secao da propria pedra", "o que resta de entrada é o acoplamento e o um posto": "frase da propria pedra, corrigida na nota ao lado", "proporcional / derivada": "rotulo do par de leituras", "acoplamento da onda = massa inscrita": "rotulo da gerencia para a hipotese do teorema", "o acorde": "titulo de secao da propria pedra", "o no-go se levanta": "frase errada da propria gerencia, citada na nota ao lado para corrigi-la", "a liberdade passa para a tônica, que segue livre": "frase errada da propria gerencia, citada na nota ao lado para corrigi-la", "a mesma estrutura": "frase da conferencia de 31/10 da gerencia, citada na nota ao lado para corrigi-la", "o gap": "titulo de secao da propria pedra",
                   "a massa é o que a volta paga e fecha, ou o que a volta deixa sem fechar? e, se é o que paga, de que lado se lê: no que atravessa ou no que fica?": "a pergunta formulada pela gerencia a pedido do operador (o pedido e\' a fala; a pergunta nao)"}
_APONTADAS_PEDRAS = {}   # (vazia: a errata R5 corrigiu na pedra o que estava apontado)
R["varredura_das_pedras"] = {"citacoes_conferidas": 0, "rotulos": [], "apontadas_a_gerencia": [], "reprovadas": []}
for _s in DL.STONES:
    _t = _norm(re.sub(r"\\n>\\s*", " ", open(_s["src"], encoding="utf-8").read()))
    for _m in re.finditer("«([^»]{8,900})»", _t):
        _fr = _norm(_m.group(1).replace("`", "").replace("**", "")).strip(" .,;:")
        _sg = [x_.strip(" .,;:") for x_ in re.split(r"…|\\[\\.\\.\\.\\]", _fr) if len(x_.strip(" .,;:")) >= 8]
        if all(_noc(x_) for x_ in _sg):
            R["varredura_das_pedras"]["citacoes_conferidas"] += 1
        elif _fr.lower() in _ROTULOS_PEDRAS:
            R["varredura_das_pedras"]["rotulos"].append({"pedra": _s["name"], "trecho": _fr[:120], "por_que": _ROTULOS_PEDRAS[_fr.lower()]})
        elif _fr.lower() in _APONTADAS_PEDRAS:
            R["varredura_das_pedras"]["apontadas_a_gerencia"].append({"pedra": _s["name"], "trecho": _fr[:120], "por_que": _APONTADAS_PEDRAS[_fr.lower()]})
        else:
            R["varredura_das_pedras"]["reprovadas"].append({"pedra": _s["name"], "trecho": _fr[:160]})
ok = ok and not R["varredura_das_pedras"]["reprovadas"] and R["varredura_das_pedras"]["citacoes_conferidas"] > 0
'''
entrada("conferir_citacoes_v404.py", autoral=True, regras=[
    ('R["todas_conferem"] = ok\n', _RX_PEDRAS + 'R["todas_conferem"] = ok\n', 1),
    entre('"""conferir_citacoes_v405.py', "import ast, glob, hashlib, json, os, re, sys", _DOC_CIT, "docstring do conferir_citacoes"),
    ('alvo = {"_V404_VERBATINS2", "_V404_SPECS", "_V404_CONTRACTS"}', 'alvo = {"_V405_VERBATINS2", "_V405_SPECS", "_V405_CONTRACTS"}', 1),
    ('V = ns["_V404_VERBATINS2"]; R = {', 'V = ns["_V405_VERBATINS2"]; R = {', 1),
    ("ok = ok and len(V) == len(DL.VERBATIM_ORIGEM_V405) == 9", "ok = ok and len(V) == len(DL.VERBATIM_ORIGEM_V405)", 1),
    ('startswith("OPERADOR_28out_") for v in V.values()', 'split("OPERADOR_")[0] in ("", os.path.basename(v["fonte_original"]).split("_")[0] + "_") and "OPERADOR_" in os.path.basename(v["fonte_original"]) for v in V.values()', 1),
    ('R["nenhuma_e_da_gerencia_as_nove_sao_do_operador"]', 'R["nenhuma_e_da_gerencia_todas_sao_do_operador"]', 2),
    ('cg = [s for s in ns["_V404_SPECS"] if s["nome"] == "cunhagens_v404"][0]\nfor it in cg["leituras_do_operador"]:\n', 'cg = [s for s in ns["_V405_SPECS"] if s["nome"] == "cunhagens_v405"][0]; cf = [s for s in ns["_V405_SPECS"] if s["nome"] == "campos_fechados_e_leituras_v405"][0]; ga = [s for s in ns["_V405_SPECS"] if s["nome"] == "ga_reclassificacao_v405"][0]\nfor it in list(cg["leituras_do_operador"]) + list(cf["leituras_do_operador"]) + list(ga["leituras_do_operador"]):\n', 1),
    ('R["leituras"]["cunhagens_v404: " + it["trecho"][:60]]', 'R["leituras"]["cunhagens_v405: " + it["trecho"][:60]]', 1),
    ('CIT_OP = [DL.FRASE_JO8, DL.FRASE_CONCORDO405]   # (os fragmentos nao carregam aspas retas: o LaTeX as escreve de outro modo; a fala de 27/10 traz o resto)', 'CIT_OP = [DL.FRASE_UM_DE_1EV, DL.FRASE_DERIVAR_ALFA, DL.FRASE_SINGULARIDADE, DL.FRASE_IDENTIDADE_NOME, DL.FRASE_ISSO_E_A_TGL]   # (so\' o snippet PT cita a fala: o EN traz traducao da gerencia, marcada como nao-citacao)', 1),
    ('    for frag in CIT_OP:\n', '    for frag in (CIT_OP if lang == "pt" else []):\n', 1),
    ('for d_ in ("cunhagens_13out", "cinco_sigma_fora_da_cosmologia_27out", "projecao_transversal_28out", "transicao_para_a_massa_28out")], []))', 'for d_ in ' + _DIRS_OP + '] + [glob.glob(os.path.join(HERE, "insumos", "cunhagens", "*OPERADOR_*.txt"))], []))', 1),
    ('"jo 8,32 e a projeção transversal da meia-nat (v405)", "a transição para a massa", "a transicao para a massa", "o teste da única palavra"}',
     '"jo 8,32 e a projeção transversal da meia-nat (v404)", "a transição para a massa", "a transicao para a massa", "o teste da única palavra",\n'
     '            # v405: os titulos das secoes novas, os nomes das pedras em portugues e os rotulos dos textos (rotulos da propria cadeia, nao citacao)\n'
     '            "a massa derivada e a identidade definida", "the derived mass and the defined identity", "a massa derivada e a identidade definida (v405)", "massa = tensão pura", "massa = tensao pura", "o que sou", "a identidade", "ponte da massa", "lei do diminuto", "tônica do hamiltoniano", "tonica do hamiltoniano", "disco de euler", "ponto zero do psíon", "ponto zero do psion", "observador = terminal", "## o texto (r2)"}', 1),
])
