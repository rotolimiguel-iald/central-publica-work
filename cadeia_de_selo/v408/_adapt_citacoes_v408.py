# -*- coding: utf-8 -*-
"""_adapt_citacoes_v408.py -- adapta conferir_citacoes_v408.py (subida mecanica de rotulo da v407) a v408 (04/11/2026, claude-construtor-v408, a servico da gerencia c1):
o bloco v408 do candidato (_V408_VERBATINS2, _V408_SPECS, _V408_TERMINAL_TEXT); as 12 falas de 04/11 (duas de AUTOR MISTO: o texto embutido e' so' o paragrafo do operador, o arquivo inteiro entra por sha256 -- a conferencia (b) le o
sha256 do arquivo inteiro e confere que o paragrafo esta' verbatim no original ANTES do corte); a chave de cada inscricao e' o sha16 do arquivo inteiro; TODAS as frases de DL.FRASES_V408 tem de estar nas leituras do registro cunhagens_v408;
as citacoes minimas do snippet PT sao as falas do terminal, da poda, da relacao sem peso, do tempo-moeda e do sentido de «P=nP»; os rotulos da propria cadeia v408 (titulo da secao PT/EN, a linha do .md) entram em _ROTULOS; as listas
de apontadas e de rotulos das PEDRAS comecam VAZIAS (as da v407 eram das nove pedras daquela versao): o que a varredura das quatro pedras de 04/11 reprovar e' dito a gerencia, nunca feito passar.
Trocas de contagem EXATA; backup de bytes; a marca sai. Escrito pela ferramenta Write."""
import ast, datetime, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "conferir_citacoes_v408.py")
raw = open(P, "rb").read(); open(P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_adapt", "wb").write(raw)
t = raw.decode("utf-8"); assert "\r\n" not in t


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n); t = t.replace(old, new)


MARCA_RX = re.compile(r"(?m)^# \[A ADAPTAR v408\][^\n]*\n"); assert len(MARCA_RX.findall(t)) == 1; t = MARCA_RX.sub("", t, count=1)
# ---- o docstring inteiro
_i0 = t.index('"""conferir_citacoes_v408.py -- '); _i1 = t.index('adaptado em 03/11/2026 ao bundle de nove modulos e as tres falas novas)."""') + len('adaptado em 03/11/2026 ao bundle de nove modulos e as tres falas novas)."""')
DOC = ('"""conferir_citacoes_v408.py -- confere, por script, toda inscricao de 04/11/2026 que a v408 EMBUTE ou CITA (as DOZE falas do operador de 04/11, em _V408_VERBATINS2; duas delas sao de AUTOR MISTO -- depois do paragrafo do operador vem texto de outra instancia da IALD --, e so\' o paragrafo dele e\' embutido como texto;\n'
       'o arquivo inteiro entra por sha256) (regua n 1: nunca fabricar citacao; nunca atribuir ao operador o que e\' da gerencia ou de outra instancia): (a) cada texto embutido em _V408_VERBATINS2 e\' IGUAL, byte a byte, ao arquivo duravel da cadeia (insumos\\\\cunhagens) e o sha256 bate; (b) a fonte original existe,\n'
       'tem o sha256 do arquivo inteiro e, nas duas de autor misto, o paragrafo embutido esta\' verbatim no original ANTES do corte declarado; (c) cada fala de `leituras_do_operador` do registro cunhagens_v408 esta VERBATIM num dos textos embutidos DO OPERADOR; (d) as cunhagens listam exatamente as inscricoes embutidas;\n'
       '(e) TODA citacao « » do snippet PT esta VERBATIM nos textos do operador embutidos (e as falas do terminal, da poda, da relacao sem peso, do tempo-moeda e do sentido de «P=nP» estao no snippet); o snippet EN traz traducao da gerencia, marcada como nao-citacao, e nenhuma fala entre aspas « »; (f) o QUADRO do 4,44 (v397)\n'
       'segue com a frase VERBATIM do operador e a PARAFRASE da gerencia NAO aparece em nenhum artefato novo; (g) VARREDURA das aspas dos artefatos novos e (h) do CANDIDATO inteiro: toda citacao entre « » e `` \'\' tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (as pastas das falas e as copias duraveis da v408),\n'
       'no Atlas, no texto do kernel embutido na base (que ja\' traz as nove pedras da v407 e as falas de 02 e 03/11), no adendo de 03-04/09, nas fontes das quatro pedras, no CLAUDE.md da casa ou ser rotulo da propria cadeia; (i) as docstrings das QUATRO pedras (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP; provas da gerencia c1, nomes do operador):\n'
       'toda citacao entre « » delas tem de existir verbatim nas falas do operador, no Atlas, no kernel embutido da base, no adendo e no CLAUDE.md da casa, com as quatro FORA do corpus (errata R2 da v407; o que nao e\' fala e\' rotulo listado; o que nao e\' verbatim nem rotulo e\' apontado a gerencia, que e\' quem corrige pedra; o agente nao corrige).\n'
       'Sai 0 se tudo bate. Molde: conferir_citacoes_v407.py, adaptado em 04/11/2026 ao bundle de quatro modulos e as doze falas de 04/11 (claude-construtor-v408)."""')
t = t[:_i0] + DOC + t[_i1:]
sub('alvo = {"_V407_VERBATINS2", "_V407_SPECS", "_V407_PSION_TEXT"}', 'alvo = {"_V408_VERBATINS2", "_V408_SPECS", "_V408_TERMINAL_TEXT"}')
sub('V = ns["_V407_VERBATINS2"]; R = {"verbatins": {}, "leituras": {}, "snippets": {}}; ok = True', 'V = ns["_V408_VERBATINS2"]; R = {"verbatins": {}, "leituras": {}, "snippets": {}}; ok = True')
# (b): o sha256 da fonte original e' o do ARQUIVO INTEIRO (nas duas de autor misto difere do sha256 do paragrafo embutido); o paragrafo tem de estar verbatim no original, antes do corte
sub('    orig = v.get("fonte_original", ""); orig_ok = None\n    if orig and os.path.exists(orig):\n        orig_ok = hashlib.sha256(open(orig, "rb").read()).hexdigest() == v["sha256"]\n',
    '    orig = v.get("fonte_original", ""); orig_ok = None; misto = "sha256_arquivo_inteiro" in v; par_ok = None\n    if orig and os.path.exists(orig):\n        _ob = open(orig, "rb").read(); orig_ok = hashlib.sha256(_ob).hexdigest() == (v.get("sha256_arquivo_inteiro") or v["sha256"])\n'
    '        if misto:   # autor misto: o texto embutido e\' SO\' o paragrafo do operador, verbatim no original e ANTES do corte declarado (depois do corte fala outra instancia)\n'
    '            _ot = _ob.decode("utf-8"); par_ok = bool(v["text"] and v["text"] in _ot and v.get("corte") and v["corte"] in _ot and _ot.find(v["text"]) < _ot.find(v["corte"]))\n')
sub('    R["verbatins"][k] = {"embutida_igual_ao_arquivo": igual, "fonte_original_igual": orig_ok, "autor": "gerencia" if gerencia else "operador"}\n    ok = ok and igual and (orig_ok is True) and not gerencia\n',
    '    R["verbatins"][k] = {"embutida_igual_ao_arquivo": igual, "fonte_original_igual": orig_ok, "autor": "gerencia" if gerencia else ("operador + outra instancia [DECLARADO]: so\' o paragrafo do operador e\' embutido" if misto else "operador"), "autor_misto": misto, "paragrafo_do_operador_verbatim_antes_do_corte": par_ok}\n'
    '    ok = ok and igual and (orig_ok is True) and not gerencia and (par_ok is True if misto else True)\n')
sub('R["o_sha16_de_cada_inscricao_e_o_da_ordem"] = all(v_["sha256"][:16] == k_[len(DL.VERBATIM_CHAVE_PREFIXO_V408):] for k_, v_ in V.items()); ok = ok and R["o_sha16_de_cada_inscricao_e_o_da_ordem"]',
    'R["o_sha16_de_cada_inscricao_e_o_da_ordem"] = all((v_.get("sha256_arquivo_inteiro") or v_["sha256"])[:16] == k_[len(DL.VERBATIM_CHAVE_PREFIXO_V408):] for k_, v_ in V.items()); ok = ok and R["o_sha16_de_cada_inscricao_e_o_da_ordem"]   # (a chave e\' o sha16 do ARQUIVO INTEIRO, o do DESENHO; nas de autor misto o sha256 do texto embutido e\' o do paragrafo)')
sub('cg = [s for s in ns["_V407_SPECS"] if s["nome"] == DL.CUNHAGENS_REGISTRO][0]', 'cg = [s for s in ns["_V408_SPECS"] if s["nome"] == DL.CUNHAGENS_REGISTRO][0]')
sub('R["as_frases_de_DL_estao_nas_leituras"] = {fr_[:50]: any(re.sub(r"\\s+", " ", fr_) == re.sub(r"\\s+", " ", it["trecho"]) or re.sub(r"\\s+", " ", fr_) in re.sub(r"\\s+", " ", it["trecho"]) for it in cg["leituras_do_operador"]) for _, fr_ in DL.FRASES_V408 if fr_ in (DL.FRASE_LEMA_PSION, DL.FRASE_NOME, DL.FRASE_PAR_LIGADO, DL.FRASE_PROJETOR, DL.FRASE_NOMES_RATIFICADOS, DL.FRASE_TESTE_C, DL.FRASE_BANHO, DL.FRASE_PAR)}; ok = ok and all(R["as_frases_de_DL_estao_nas_leituras"].values()) and len(R["as_frases_de_DL_estao_nas_leituras"]) == 8',
    'R["as_frases_de_DL_estao_nas_leituras"] = {fr_: any(re.sub(r"\\s+", " ", fr_) == re.sub(r"\\s+", " ", it["trecho"]) or re.sub(r"\\s+", " ", fr_) in re.sub(r"\\s+", " ", it["trecho"]) for it in cg["leituras_do_operador"]) for _, fr_ in DL.FRASES_V408}; ok = ok and all(R["as_frases_de_DL_estao_nas_leituras"].values()) and len(R["as_frases_de_DL_estao_nas_leituras"]) == len({fr_ for _, fr_ in DL.FRASES_V408}) > 0   # (v408: TODAS as frases de DL.FRASES_V408 sao leituras do registro cunhagens_v408)')
sub('_PEDRAS = _norm(" ".join(open(p_["src"], encoding="utf-8").read() for p_ in DL.PEDRAS_V408).replace("**", "").replace("`", ""))   # (v408: as nove pedras; a docstring delas e\' verificada em (i), FORA do corpus; aqui valem como corpus do que o runtime re-cita)',
    '_PEDRAS = _norm(" ".join(open(p_["src"], encoding="utf-8").read() for p_ in DL.PEDRAS_V408).replace("**", "").replace("`", ""))   # (v408: as quatro pedras; a docstring delas e\' verificada em (i), FORA do corpus; aqui valem como corpus do que o runtime re-cita)')
sub('CIT_OP_MINIMAS = [DL.FRASE_LEMA_PSION, DL.FRASE_PAR_LIGADO, DL.FRASE_NOME]   # (so\' o snippet PT cita a fala: o EN traz traducao da gerencia, marcada como nao-citacao; estas tres tem de estar no snippet PT)',
    'CIT_OP_MINIMAS = [DL.FRASE_TERMINAL, DL.FRASE_PROVAR_OU_PODAR, DL.FRASE_RELACAO_MENTIRA, DL.FRASE_TEMPO_MOEDA, DL.FRASE_SENTIDO_PNP]   # (so\' o snippet PT cita a fala: o EN traz traducao da gerencia, marcada como nao-citacao; estas cinco tem de estar no snippet PT: o terminal, a poda, a relacao sem peso, o tempo-moeda, o sentido de «P=nP»)')
# o LaTeX escapa % & _ # no snippet (a fala tem o caractere puro): normalizacao SIMETRICA so' para comparar (a palavra segue tendo de ser identica)
sub('    sn_flat = _norm(sn.replace("\\\\texttt{", "").replace("\\\\emph{", ""))', '    sn_flat = _norm(sn.replace("\\\\texttt{", "").replace("\\\\emph{", "").replace("\\\\%", "%").replace("\\\\&", "&").replace("\\\\_", "_").replace("\\\\#", "#"))   # (v408: desfaz os escapes LaTeX de % & _ # para comparar com a fala; a fala do terminal tem «100%»)')
# os rotulos da propria cadeia v408
sub('            "o par de psions na face de fock esta provado/construido", "o vacuo de fock e o vetor de bell", "a ponte bell-tt e\' teorema"}',
    '            "o par de psions na face de fock esta provado/construido", "o vacuo de fock e o vetor de bell", "a ponte bell-tt e\' teorema",\n'
    '            # v408 (04/11/2026): o titulo da secao nova (PT/EN), a linha do .md e o rotulo da linha da v407 (rotulos da propria cadeia, nao citacao)\n'
    '            "tetelestai é o terminal: a leitura, a poda, a quitação; o tempo é a moeda de $\\\\beta$; o dicionário e o ponto de contradição", "tetelestai is the terminal: the reading, the pruning, the settlement; time is the currency of $\\\\beta$; the dictionary and the point of contradiction",\n'
    '            "tetelestai é o terminal (v408)", "tetelestai é o terminal (v408, 04/11/2026)", "tetelestai e\' o terminal (v408)", "tetelestai é o terminal", "tetelestai e\' o terminal", "o psíon, o canto e o par (v407)", "o psion, o canto e o par (v407)"}')
# as apontadas da v407 eram daquela versao: a lista da v408 comeca vazia (o que a varredura achar e' dito, nunca feito passar)
_j0 = t.index('_APONTADAS_GH = {'); _j1 = t.index('_ROTULOS = {x_.lower() for x_ in _ROTULOS}')
t = t[:_j0] + '_APONTADAS_GH = {}   # (v408: as apontadas da v407 eram dos textos daquela versao; nenhuma apontada declarada para a v408 ate\' a varredura dizer o contrario -- o que ela reprovar fica em varredura_de_aspas, nunca e\' feito passar)\n' + t[_j1:]
sub('# (i) VARREDURA DAS PEDRAS (errata R2 da gerencia, 01/11/2026; achado 12 da revisao de terceiro): toda citacao entre « » das docstrings das NOVE pedras da v408', '# (i) VARREDURA DAS PEDRAS (errata R2 da gerencia, 01/11/2026; achado 12 da revisao de terceiro): toda citacao entre « » das docstrings das QUATRO pedras da v408')
sub('_BANC = [os.path.join(DL.SANDBOX, *r_.split("/")) for r_ in DL.BUNDLE_DA_BANCADA]   # (v408: DL.BUNDLE_DA_BANCADA == [] -- as nove pedras sao da gerencia c1; nenhum modulo da bancada do ChatGPT entra neste bundle)',
    '_BANC = [os.path.join(DL.SANDBOX, *r_.split("/")) for r_ in DL.BUNDLE_DA_BANCADA]   # (v408: DL.BUNDLE_DA_BANCADA == [] -- as quatro pedras sao provas da gerencia c1 com os nomes do operador; nenhum modulo da bancada do ChatGPT entra neste bundle)')
sub('_XP = [p_ for p_ in _BANC if os.path.exists(p_)]   # (as nove pedras e a ratificacao/conferencia da gerencia NAO sao corpus: texto da gerencia nao abona citacao)', '_XP = [p_ for p_ in _BANC if os.path.exists(p_)]   # (as quatro pedras e os recibos da gerencia NAO sao corpus: texto da gerencia nao abona citacao)')
_k0 = t.index('_ROTULOS_PEDRAS = {'); _k1 = t.index('_APONTADAS_PEDRAS = {k_.lower(): v_ for k_, v_ in _APONTADAS_PEDRAS.items()}')
t = t[:_k0] + ('_ROTULOS_PEDRAS = {}   # (v408: SO\' o que a propria pedra diz ser rotulo/nome dela, nunca para fazer passar citacao; as entradas da v407 eram das nove pedras daquela versao; a lista da v408 comeca vazia)\n'
                '_APONTADAS_PEDRAS = {}   # (v408: o que esta entre « », nao e\' verbatim nas falas/na base e nao e\' rotulo declarado: DITO A GERENCIA no relatorio; o agente nao corrige pedra. Comeca vazia: o que a varredura reprovar e\' reprovado, ate\' a gerencia decidir)\n') + t[_k1:]
assert not any(l_.startswith("# [A ADAPTAR v408]") for l_ in t.split("\n"))
ast.parse(t); open(P, "wb").write(t.encode("utf-8")); print("ok conferir_citacoes", len(raw), "->", len(t.encode("utf-8")))
