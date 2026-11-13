# -*- coding: utf-8 -*-
"""_fix_topo_ratificado_v411.py -- (claude-construtor-v411, retomada, 12/11/2026) o que a gerencia mandou com TOPO_RATIFICADO_v411.json (D172, D173): (1) o preenchimento do topo DIRIGIDO pela tabela `marcadores` do arquivo
(doze; cada um com a chave do core e o formato; marcador sem fonte resolvida ou que sobre = PARAR) e o fail-closed do acrescimo (“nenhuma foi falsificada” so' com falsificadas == 0 e a soma das categorias = as cobrancas;
o H0DN fica fora do livro); (2) o item da FALA DO AUTOR no quadro novo do topo (tex e md), o trecho verbatim conferido por bytes; (3) a F65 aceita os nomes fixos da convencao dos 5 sigma (critério/escala de descoberta;
discovery criterion/scale/threshold) e segue recusando “descoberta” dita do numero ou do rito, com controle negativo dos dois lados; (4) o spec cunhagens_v411 com as 11 falas e D159 a D173; (5) o gerador: a tabela,
o topo ratificado (fonte unica), a fala do autor no bloco de runtime, 11 falas. Backup de BYTES antes de cada; ancoras unicas; ast.parse depois. uso: python -B -X utf8 _fix_topo_ratificado_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca(arq_, pares_):
    p_ = os.path.join(HERE, arq_); b_ = open(p_, "rb").read(); t_ = b_.decode("utf-8"); assert "\r" not in t_, arq_
    for a_, n_ in pares_:
        assert t_.count(a_) == 1, (arq_, a_[:110], t_.count(a_))
        t_ = t_.replace(a_, n_)
    ast.parse(t_)
    bak_ = p_ + ".bak_" + TS + "_topo"; open(bak_, "wb").write(b_); assert open(bak_, "rb").read() == b_
    nb_ = t_.encode("utf-8"); open(p_ + ".tmp", "wb").write(nb_); assert os.path.getsize(p_ + ".tmp") == len(nb_); os.replace(p_ + ".tmp", p_)
    print("ok", arq_, len(b_), "->", len(nb_))


# ---------------- (1) e (2) o quadro: o topo dirigido pela tabela; a fala do autor
TOPO_NOVO = '''def _v411_topo_texto(core_, lang_, tex_=True):
    """O texto RATIFICADO do topo (TOPO_RATIFICADO_v411.json, a fonte unica; D172, D173), com os marcadores preenchidos na EMISSAO a partir da chave do core que a tabela `marcadores` do arquivo da' (doze: o H0DN, o livro de
    cobrancas e a Fase 9 V2). Marcador sem fonte resolvida, numero nao finito ou marcador que sobre no texto = PARAR (ValueError). O acrescimo e' fail-closed: a frase de que nenhuma cobranca foi falsificada so' sai se as
    falsificadas forem zero no core do rito e a soma das categorias mais as falsificadas for o numero de cobrancas; o H0DN nao entra no livro. Se o registro nao selou, devolve a frase de que nao selou."""
    import math as _m
    r_ = core_.get("h0dn_bg1_v411") or {}
    if r_.get("all_verified") is not True:
        return (r"\\textbf{O registro do teste H0DN $\\times$ BG1 (v411) NÃO selou nesta rodada: o resultado não é dito aqui.} " if lang_ == "pt" else r"\\textbf{The H0DN $\\times$ BG1 test record (v411) did NOT seal this round: the result is not stated here.} ") if tex_ else ""
    t_ = str(_V411_TOPO[lang_])
    tab_ = _V411_TOPO.get("marcadores") or {}
    if not tab_:
        raise ValueError("a tabela de marcadores do topo ratificado nao esta' embutida: PARAR")
    lv_ = _V411_TOPO.get("livro") or {}
    pr2_ = core_
    for k_ in lv_.get("caminho") or ["?"]:
        pr2_ = pr2_.get(k_) if isinstance(pr2_, dict) else None
    if any(f_ in t_ for f_ in lv_.get("frases_" + lang_) or []):   # (fail-closed do acrescimo: D173)
        led_ = (pr2_ or {}).get("ledger") if isinstance(pr2_, dict) else None
        if not isinstance(led_, dict) or not isinstance((pr2_ or {}).get("n_cobrancas"), int) or (pr2_ or {}).get("falsificadas") != 0 or led_.get("FALSIFIED", 0) != 0 \\
                or sum(int(led_.get(c_) or 0) for c_ in lv_["categorias"]) + int(led_.get("FALSIFIED") or 0) != int(pr2_["n_cobrancas"]):
            raise ValueError("o livro de cobrancas do rito nao sustenta a frase de que nenhuma foi falsificada (falsificadas != 0 ou a soma das categorias != as cobrancas): PARAR")
    for mk_pt_, d_ in tab_.items():
        mk_ = mk_pt_ if lang_ == "pt" else d_["en"]
        if mk_ not in t_:
            continue
        x_ = core_
        for k_ in d_["caminho"]:
            x_ = x_.get(k_) if isinstance(x_, dict) else None
        if isinstance(x_, bool) or not isinstance(x_, (int, float)) or x_ != x_ or x_ in (float("inf"), float("-inf")):
            raise ValueError("marcador do topo sem fonte resolvida no core (%s <- %s): PARAR" % (mk_, ".".join(d_["caminho"])))
        if d_["inteiro_de"]:
            rep_ = str(int(_m.floor(float(x_))))
        elif d_["inteiro"]:
            if float(x_) != int(x_):
                raise ValueError("marcador inteiro com valor nao inteiro (%s): PARAR" % mk_)
            rep_ = str(int(x_))
        else:
            rep_ = "%.*f" % (int(d_["casas"]), float(x_))
            if d_["com_sinal"] and float(x_) > 0:
                rep_ = "+" + rep_
            rep_ = (rep_.replace(".", ",") if lang_ == "pt" else rep_).replace("-", "−")
        t_ = t_.replace(mk_, rep_)
    if "⟨" in t_ or "⟩" in t_:
        raise ValueError("marcador do topo nao preenchido (sobrou no texto): PARAR")
    return (_v411_tex_misto(t_) + " ") if tex_ else t_
'''
FALA_TEX = '''def _v411_fala_do_autor_tex(lang_):
    """(D172) o item da FALA DO AUTOR no quadro novo do topo, no molde do item da fala do quadro da Fase 9 V2: o trecho VERBATIM (conferido por bytes na construcao), com a data e o sha16, seguido do que ele e'."""
    f_ = _V411_FALA_DO_AUTOR
    if not f_:
        return None
    if lang_ == "pt":
        return (r"\\item \\textbf{A fala do autor} \\textsf{[INPUT]} (" + f_["data_pt"] + r", sha16 \\texttt{" + f_["sha16"] + r"}), verbatim: «" + _v411_tex_unicode(f_["trecho"])
                + r"» --- testemunho do autor; a frase de máquina é a cabeça do veredito, com as ressalvas.")
    return (r"\\item \\textbf{The author's words} \\textsf{[INPUT]} (" + f_["data_en"] + r", sha16 \\texttt{" + f_["sha16"] + r"}), verbatim, in Portuguese: «" + _v411_tex_unicode(f_["trecho"])
            + r"» --- the author's testimony; the machine sentence is the head of the verdict, with the reservations.")


def _v411_fala_do_autor_md():
    f_ = _V411_FALA_DO_AUTOR
    if not f_:
        return None
    return "> - **A fala do autor** [INPUT] (%s, sha16 `%s`), verbatim: «%s» — testemunho do autor; a frase de máquina é a cabeça do veredito, com as ressalvas." % (f_["data_pt"], f_["sha16"], f_["trecho"])


'''
p = os.path.join(HERE, "quadro_v411.py"); t = open(p, encoding="utf-8").read()
i0 = t.index("def _v411_topo_texto(core_, lang_, tex_=True):"); i1 = t.index("def _v411_efeitos_tex(core_, lang_")
VELHO_TOPO = t[i0:i1].rstrip("\n") + "\n"
troca("quadro_v411.py", [
    (VELHO_TOPO, TOPO_NOVO),
    ('def _v411_remissao_tex(lang_):', FALA_TEX + 'def _v411_remissao_tex(lang_):'),
    ('                r"\\item \\textbf{O que o teste não decide:} " + nd_ + r".",\n',
     '                r"\\item \\textbf{O que o teste não decide:} " + nd_ + r".",\n               ] + [x_ for x_ in [_v411_fala_do_autor_tex("pt")] if x_] + [\n'),
    ('            r"\\item \\textbf{What the test does not decide:} " + nd_ + r".",\n',
     '            r"\\item \\textbf{What the test does not decide:} " + nd_ + r".",\n           ] + [x_ for x_ in [_v411_fala_do_autor_tex("en")] if x_] + [\n'),
    ('          "> - **O que o teste não decide:** " + "; ".join(a_["nao_decide"]) + ".",\n',
     '          "> - **O que o teste não decide:** " + "; ".join(a_["nao_decide"]) + ".",\n         ] + [x_ for x_ in [_v411_fala_do_autor_md()] if x_] + [\n'),
])

# ---------------- (3) a F65 (runtime) e o controle negativo dos dois lados (a guarda da cadeia e o teste offline)
troca("runtime_h0dn_v411.py", [
    ('        for m_ in _re.finditer(r"\\bdescobert[ao]s?\\b|\\bdescobr(?:e|iu|imos|iram)\\b|\\bdiscover(?:y|ies|ed|s)?\\b", seg_, _re.I):   # F65\n'
     '            if not _re.search(_NEG_, seg_[max(0, m_.start() - 30):m_.start()], _re.I):\n',
     '        _conv65_ = [(c_.start(), c_.end()) for c_ in _re.finditer(r"\\bcrit[ée]rio\\s+de\\s+descoberta\\b|\\bescala\\s+de\\s+descoberta\\b|\\bdiscovery\\s+(?:criterion|scale|threshold)\\b", seg_, _re.I)]   # (D172/D173: o NOME da convencao dos 5 sigma passa)\n'
     '        for m_ in _re.finditer(r"\\bdescobert[ao]s?\\b|\\bdescobr(?:e|iu|imos|iram)\\b|\\bdiscover(?:y|ies|ed|s)?\\b", seg_, _re.I):   # F65\n'
     '            if any(a__ <= m_.start() and m_.end() <= b__ for a__, b__ in _conv65_):\n                continue\n'
     '            if not _re.search(_NEG_, seg_[max(0, m_.start() - 30):m_.start()], _re.I):\n'),
])
troca("guarda_frases_v411.py", [
    ('    ("F65", "a descoberta do H0DN a 6 sigma"), ("F65", "the discovery of the Hubble ratio"),\n',
     '    ("F65", "a descoberta do H0DN a 6 sigma"), ("F65", "the discovery of the Hubble ratio"),\n'
     '    ("F65", "o rito fez a descoberta do número"), ("F65", "a descoberta de 6,11 sigma no critério de 5 sigma"), ("F65", "the rite made a discovery at 6 sigma"),   # (D172/D173: a descoberta dita do numero ou do rito segue recusada)\n'),
    ('    "β entra só por nome (ALPHA_FINE_CODATA_2018 × √e em runtime)",\n]',
     '    "β entra só por nome (ALPHA_FINE_CODATA_2018 × √e em runtime)",\n'
     '    "o que passa do degrau de 5σ, o critério de descoberta da física acadêmica", "na escala de descoberta da física acadêmica", "the one that passes the 5σ step, the discovery criterion of academic physics",\n'
     '    "the discovery scale of academic physics", "the 5σ discovery threshold",   # (D172/D173: o NOME fixo da convencao dos 5 sigma passa)\n]'),
])
troca("_teste_h0dn_offline_v411.py", [
    ('      "descoberta": "a descoberta do H0DN", ', '      "descoberta": "a descoberta do H0DN", "descoberta do rito": "o rito fez a descoberta do numero", '),
    ('             "negada": "nao e\' evidencia independente", "nao descobre": "o rito confere a conta, nao descobre um numero novo"}',
     '             "negada": "nao e\' evidencia independente", "nao descobre": "o rito confere a conta, nao descobre um numero novo", "o criterio": "o que passa do degrau de 5σ, o critério de descoberta da física acadêmica",\n'
     '             "the threshold": "the 5σ discovery threshold, the discovery criterion of academic physics"}'),
])

# ---------------- (4) o spec cunhagens_v411: as 11 falas e D159 a D173
troca("registros_v411.py", [
    ('    dec_tok = "D159_D162_D167_D168_D169_D170"\n', '    dec_tok = DL.DECISOES_TOKEN_V411   # (D159 a D173, lidas do DESENHO e do AO LADO de 12/11)\n'),
    ('a marca da emenda, D168; a ordem de abrir e a ordem da v411, D169; o testemunho e a ordem do topo, D170);',
     'a marca da emenda, D168; a ordem de abrir e a ordem da v411, D169; o testemunho e a ordem do topo, D170; a ratificacao da formula do topo e a leitura com o acervo, D172; a ratificacao da redacao do acrescimo, D173);'),
    ('"textos_da_gerencia_citados": [{"nome": g_["nome"], "sha256": g_["sha256"]} for g_ in DL.TEXTOS_DA_GERENCIA_CITADOS], "assinatura_das_erratas": ASSINA,',
     '"textos_da_gerencia_citados": [{"nome": g_["nome"], "sha256": g_["sha256"]} for g_ in DL.TEXTOS_DA_GERENCIA_CITADOS], "assinatura_das_erratas": ASSINA,\n'
     '                   "topo_ratificado": {"arquivo": os.path.basename(DL.TOPO_RATIFICADO_ARQ), "sha256": DL.TOPO_SHA256, "n_marcadores": len(DL.MARCADORES_V411 or {})} if DL.TOPO_SHA256 else None,'),
])

# ---------------- (5) o gerador: a tabela dirigindo as assercoes do topo, o topo ratificado embutido com a tabela e o livro, a fala do autor, 11 falas
troca("gerar_candidato_v411.py", [
    ('_MK = {"pt": ["⟨Z contra K⟩", "⟨Z contra o nulo⟩", "⟨n⟩", "⟨Z das Cefeidas livres⟩"], "en": ["⟨Z against K⟩", "⟨Z against the null⟩", "⟨n⟩", "⟨Z of the free Cepheids⟩"]}\n'
     'for _lg in ("pt", "en"):\n'
     '    assert all(TOPO[_lg].count(mk_) == 1 for mk_ in _MK[_lg]) and len(re.findall("⟨[^⟩]*⟩", TOPO[_lg])) == 4, ("o texto do topo nao traz exatamente os quatro marcadores de numero (um de cada)", _lg)\n',
     '# (D172/D173) os marcadores do topo sao DIRIGIDOS pela tabela `marcadores` do TOPO_RATIFICADO_v411.json (doze; a fonte de maquina de cada um em DL.MARCADORES_V411); no pre-voo e no ensaio do topo PROPOSTO, os quatro\n'
     '# de antes (a proposta do DESENHO 5.1 b so\' traz esses). Todo marcador do texto tem de estar na tabela; marcador fora dela = PARAR.\n'
     '_TAB_MK = (DL.MARCADORES_V411 if TOPO["ratificado"] else {k_: v_ for k_, v_ in DL.MARCADORES_V411.items() if k_ in re.findall("⟨[^⟩]*⟩", TOPO["pt"])}) if DL.MARCADORES_V411 else None\n'
     'assert _TAB_MK, "a tabela de marcadores do topo nao foi lida: PARAR"\n'
     '_MK = {"pt": list(_TAB_MK), "en": [v_["en"] for v_ in _TAB_MK.values()]}\n'
     'for _lg in ("pt", "en"):\n'
     '    _no_texto = re.findall("⟨[^⟩]*⟩", TOPO[_lg])\n'
     '    assert _no_texto and set(_no_texto) <= set(_MK[_lg]) and set(_MK[_lg]) <= set(_no_texto), ("marcador do topo fora da tabela, ou da tabela fora do texto: PARAR", _lg, sorted(set(_no_texto) ^ set(_MK[_lg])))\n'),
    ('_V411_TOPO = " + pprint.pformat({"pt": TOPO["pt"], "en": TOPO["en"], "ratificado": TOPO["ratificado"], "sha256_do_arquivo": TOPO["sha256"]}, width=160, sort_dicts=False)',
     '_V411_TOPO = " + pprint.pformat({"pt": TOPO["pt"], "en": TOPO["en"], "ratificado": TOPO["ratificado"], "sha256_do_arquivo": TOPO["sha256"], "marcadores": _TAB_MK, "livro": _LIVRO}, width=160, sort_dicts=False)'),
    ('"_V411_TITULO_QUADRO_PT = " + repr(DL.TITULO_QUADRO_TOPO_PT)', '"_V411_FALA_DO_AUTOR = " + repr(DL.FALA_DO_AUTOR_V411 if TOPO["ratificado"] else None) + "   # (D172) o trecho verbatim da fala do autor para o quadro (conferido por bytes; None no ensaio do topo proposto)\\n" + "_V411_TITULO_QUADRO_PT = " + repr(DL.TITULO_QUADRO_TOPO_PT)'),
    ('assert len(verb) == DL.N_FALAS_V411 == 9\n', 'assert len(verb) == DL.N_FALAS_V411 == 11\n'),
    ('_nsq = {"_V411_TOPO": {"pt": TOPO["pt"], "en": TOPO["en"]}, "_V411_ESTATUTO_AO_LADO_PT": DL.FRASE_ESTATUTO_DA_PROVA_AO_LADO_PT}',
     '_nsq = {"_V411_TOPO": {"pt": TOPO["pt"], "en": TOPO["en"], "marcadores": _TAB_MK, "livro": _LIVRO}, "_V411_ESTATUTO_AO_LADO_PT": DL.FRASE_ESTATUTO_DA_PROVA_AO_LADO_PT, "_V411_FALA_DO_AUTOR": DL.FALA_DO_AUTOR_V411 if TOPO["ratificado"] else None}'),
    ('_corq = {"h0dn_bg1_v411": _rq}\n',
     '_corq = {"h0dn_bg1_v411": _rq, "estatuto_da_prova_v391": core0.get("estatuto_da_prova_v391"), "teste_de_veracidade_fase9_v397": core0.get("teste_de_veracidade_fase9_v397")}   # (o topo le o livro e a Fase 9 V2 do core; o H0DN, do registro do ensaio offline)\n'),
    ('"_v411_tex_misto", "_v411_topo_texto",', '"_v411_tex_misto", "_v411_topo_texto", "_v411_fala_do_autor_tex", "_v411_fala_do_autor_md", "_V411_FALA_DO_AUTOR",'),
])
# o livro (fail-closed do acrescimo) e o arquivo da tabela da PROPOSTA (so' para o pre-voo/ensaio do topo proposto): inseridos no gerador logo depois de lida a tabela
troca("gerar_candidato_v411.py", [
    ('assert _TAB_MK, "a tabela de marcadores do topo nao foi lida: PARAR"\n',
     'assert _TAB_MK, "a tabela de marcadores do topo nao foi lida: PARAR"\n'
     '_LIVRO = {"caminho": ["estatuto_da_prova_v391", "prova_2_ritos"], "categorias": ["NOT_FALSIFIED", "INCONCLUSIVE", "AWAITING", "EXCLUDED_IN_READING"], "frases_pt": ["nenhuma foi falsificada", "nenhuma falsificada"],\n'
     '          "frases_en": ["none was falsified", "none falsified"], "regra": "a frase de que nenhuma cobranca foi falsificada so\' sai com falsificadas == 0 e a soma das categorias + as falsificadas == n_cobrancas (D173; regra do TOPO_RATIFICADO_v411.json); o H0DN nao entra no livro"}\n'
     'if TOPO["ratificado"]:\n'
     '    assert all(any(c_ in r_ for r_ in DL.REGRAS_DO_TOPO_V411) for c_ in ("falsificadas == 0", "soma das quatro categorias", "NÃO entra na contagem do livro", "F65")), "as regras do topo ratificado nao sao as que o gerador cumpre: PARAR"\n'
     '    _cats = [re.search(r"ledger\\.([A-Z_]+)$", ".".join(v_["caminho"])) for v_ in _TAB_MK.values()]\n'
     '    assert sorted(m_.group(1) for m_ in _cats if m_) == sorted(_LIVRO["categorias"]), "as quatro categorias do livro na tabela nao sao as do fail-closed: PARAR"\n'
     '    _p2r = core0["estatuto_da_prova_v391"]["prova_2_ritos"]; _led = _p2r["ledger"]\n'
     '    assert _p2r["falsificadas"] == 0 == _led.get("FALSIFIED", 0) and sum(_led[c_] for c_ in _LIVRO["categorias"]) + _led.get("FALSIFIED", 0) == _p2r["n_cobrancas"], "o livro da base nao sustenta a frase do acrescimo: PARAR"\n'
     '    _V397N = ast.literal_eval(top("_V397_CHAVES_NUM").value)\n'
     '    assert all(v_["caminho"][-1] in _V397N for v_ in _TAB_MK.values() if v_["caminho"][0] == "teste_de_veracidade_fase9_v397"), "a Fase 9 V2 da tabela nao e\' lida pelas chaves do quadro da v397: PARAR"\n'),
])
print("FEITO")
