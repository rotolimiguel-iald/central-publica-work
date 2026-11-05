# -*- coding: utf-8 -*-
"""_adapt_ensaio_v408.py -- adapta ensaio_a_seco_v408.py (subida mecanica de rotulo do ensaio_a_seco_v407.py FINAL) ao conteudo da v408 (TETELESTAI E' O TERMINAL: bundle de 4 modulos, registro tetelestai_terminal_v408 com 16 checagens, NENHUMA chave antiga muda).
O que muda, por bloco: (a) cabecalho e docstring; (b) as listas dos registros (os da v407 passam a HERDADOS, recriados e comparados; os NOVOS sao os da v408); (c) a ordem de chamada medida por AST agora e' a do tetelestai_terminal_v408 (controles negativos: o bloco antes do run_um; a chamada do psion_canto_v407 retirada);
(d) o selo: nenhuma chave antiga pode diferir (fechamento_v406, testemunha_estatica_v396, psion_canto_v407 ficam iguais); (e) os blocos HERDADOS da v406 e da v407 leem os seus numeros do DL.D6/DL.D7 e do CANDIDATO_v407.json, nunca do DL da v408 (o bump deixara rotulos errados: FLAGS_v407 no lugar de FLAGS_v406,
E407 no lugar da escada da v406, CM da v408 no lugar do da v407); os textos herdados passam pela guarda da v407 (_GF7), nao pela da v408 (a F29 da v408 reprovaria «leituras do operador [ONTO]» da v407 selada); (f) o bloco NOVO (6n) do tetelestai_terminal_v408 com os controles negativos; (g) os titulos do artigo (a secao v408 antes da v407), a variante sem os registros da v408, o markdown, a simulacao da arvore e o exame dos pontos.
Trocas de contagem EXATA (assert); backup de bytes; retira a marca [A ADAPTAR v408]. Escrito pela ferramenta Write (o heredoc do Bash colapsa barras invertidas). Uso: python -I -B -X utf8 _adapt_ensaio_v408.py"""
import ast
import datetime
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "ensaio_a_seco_v408.py")
raw = open(P, "rb").read()
open(P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_adapt", "wb").write(raw)
t = raw.decode("utf-8")
assert "\r\n" not in t
N0 = len(t)


def sub(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, ("troca nao casou", old[:110], "esperado", n, "achou", c)
    t = t.replace(old, new)


def rx(pattern, new, n=1, flags=re.M):
    global t
    c = len(re.findall(pattern, t, flags))
    assert c == n, ("regex nao casou", pattern[:90], "esperado", n, "achou", c)
    t = re.sub(pattern, lambda m_: new, t, count=n, flags=flags)


def entre(ini, fim, novo):
    """troca o trecho que comeca em `ini` (inclusive) e termina ANTES de `fim` (que fica); ambos unicos e na ordem."""
    global t
    assert t.count(ini) == 1 and t.count(fim) == 1, ("ancora nao unica", ini[:70], t.count(ini), fim[:70], t.count(fim))
    i = t.index(ini); j = t.index(fim); assert i < j
    t = t[:i] + novo + t[j:]


# ---------------------------------------------------------------- (a) cabecalho e docstring
rx(r"^# \[A ADAPTAR v408\][^\n]*\n", "", 1)
rx(r"^# ADAPTADO a v408 \(03/11/2026, claude-prep-v408\):[^\n]*\n",
   "# ADAPTADO a v408 (04/11/2026, claude-construtor-v408): molde ensaio_a_seco_v407.py (que rodou na cadeia da v407). A v408 e' um BUNDLE PEQUENO de 4 modulos em TGLExt/ (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP); o registro NOVO e' tetelestai_terminal_v408 (16 checagens); NENHUMA chave antiga muda; o psion_canto_v407 e o fechamento_v406 sao HERDADOS e seguem conferidos aqui, com os controles negativos da v407 e da v406; as TRES chaves novas do core sao tetelestai_terminal_v408, cunhagens_v408 e kh_n1_cobertura_v408.\n", 1)
rx(r"^A v408 \(03/11/2026\) e' O PSION.*?(?=^\(1\) copia o candidato)",
   "A v408 (04/11/2026) e' TETELESTAI E' O TERMINAL: um BUNDLE de 4 modulos novos de kernel em TGLExt/ (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP, com os nomes do operador), as bandeiras ext_tt408_NNNN so' de declaracao nomeada, a escada 11958 -> 12001 (lida do CANDIDATO_v408.json), UM registro com FUNCAO\n"
   "(tetelestai_terminal_v408: le do kernel do PROPRIO rito as 41 ancoras das quatro pedras, as 4 fontes por sha256, as respostas do operador pelos teoremas que ja existiam e por duas declaracoes novas, e faz as 16 checagens com beta em runtime, o gate congelado, a escada exata, as guardas e o insumo purgado), os registros por spec cunhagens_v408 e kh_n1_cobertura_v408 e as ERRATAS E21 a E23 AO LADO.\n"
   "NENHUMA chave antiga muda (CHAVES_V408 = []): nao ha patch C19/C20; a funcao do neutrino NAO e' reescrita e o numero da massa NAO muda. NAO ha registro de pedra novo por pedra (DL.STONES == [] de proposito; as 4 pedras estao em DL.PEDRAS_V408): os registros da v405, da v406 (fechamento_v406 e os specs) e da v407 (psion_canto_v407 e os specs) sao HERDADOS e seguem conferidos aqui, com os mesmos controles negativos.\n"
   "A MOLDURA: o terminal e' a leitura, nao o fim do decaimento; nao ha' relacao sem peso; o tempo e' a moeda de beta; o zero inscrito e' o Um e o Um nao e' o zero absoluto; «P = nP» so' no sentido do operador; validade no kernel nao e' creditacao; o gate nao se move. O ensaio cobra isto: cada registro recusa quando um elo e' tirado.\n"
   "A base e' a v407 SELADA (core e selo em base_v407), o kernel e' o da v407 + o bundle de 4 (sandbox C:/t/k408c); os registros de v393 a v399, os da v401 a v407 (inclusive os oito de pedra da v405, o fechamento_v406 e o psion_canto_v407 com os specs) sao RECRIADOS e comparados com os da v407 selada (o `witness_layers.canonical_full_witness_term_constructed`, medida de run_um sobre o kf do rito, e' recomputado pela expressao do proprio candidato).\n", 1, re.M | re.S)
sub("as TRES da v408 (psion_canto_v407, cunhagens_v407, kh_n1_cobertura_v407)", "as TRES da v408 (tetelestai_terminal_v408, cunhagens_v408, kh_n1_cobertura_v408)")
rx(r"^\(6\) unidade:[^\n]*\n", "(6) unidade: o Teste da Unica Palavra (v397), o sonico e a afinacao (v398), o selo pela propria tecnologia e a declaracao do operador (v399), a FALSIDADE DA INERCIA (v401, recriada), os registros da v402, da v403, da v404 e da v405 (recriados, cada elo recusa), o FECHAMENTO da v406 e O PSION, O CANTO E O PAR da v407 (herdados: os controles das duas versoes seguem recusando; a chave do lema segue lida do kernel), e TETELESTAI E' O TERMINAL da v408 (tudo certo, os numeros recalculados, a aritmetica das pedras refeita, cada elo recusa, nenhuma chave antiga muda);\n", 1)
sub("a secao v408 «O psíon e o canto: a passagem sob compressão e o par» (antes da v407)", "a secao v408 «Tetelestai é o terminal: a leitura, a poda, a quitação; o tempo é a moeda de β; o dicionário e o ponto de contradição» (antes da v407)")
# ---------------------------------------------------------------- o candidato da v407 (os numeros dos blocos herdados) e a guarda da v407
sub('CM = json.load(open(os.path.join(HERE, "CANDIDATO_v408.json"), encoding="utf-8")); assert CM["sha16"] == h16',
    'CM = json.load(open(os.path.join(HERE, "CANDIDATO_v408.json"), encoding="utf-8")); assert CM["sha16"] == h16\n'
    '_CM7 = json.load(open(os.path.join(DL.V407, "CANDIDATO_v407.json"), encoding="utf-8"))   # (v408) o candidato da v407 SELADA: os numeros dos blocos HERDADOS da v407 (escada da v406, sha16 da base v406, pino antigo do h8 da v406) saem dele e do DL.D7, nunca do DL da v408\n'
    'assert _CM7["sha16"] == DL.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v407.json nao e\' o da v407 selada", _CM7["sha16"])')
# ---------------------------------------------------------------- (b) as listas dos registros
sub("V408N = list(um._V407_REGISTROS_FUNCAO) + list(um._V407_NOMES_REGISTROS)   # os registros NOVOS da v408 (nao existem no core da base): psion_canto_v407, cunhagens_v407, kh_n1_cobertura_v407",
    "V407N = V407N + list(um._V407_REGISTROS_FUNCAO) + list(um._V407_NOMES_REGISTROS)   # (v408) os tres registros da v407 (psion_canto_v407, cunhagens_v407, kh_n1_cobertura_v407) sao HERDADOS: recriados pelo fluxo e comparados com os da v407 selada\n"
    "V408N = list(um._V408_REGISTROS_FUNCAO) + list(um._V408_NOMES_REGISTROS)   # os registros NOVOS da v408 (nao existem no core da base): tetelestai_terminal_v408, cunhagens_v408, kh_n1_cobertura_v408")
rx(r"^NOVAS408 = sorted\(V408N\)   #[^\n]*\n", "NOVAS408 = sorted(V408N)   # a v408 cria TRES chaves no core (tetelestai_terminal_v408, cunhagens_v408, kh_n1_cobertura_v408); os registros das v399, v401, v402, v403, v404, v405 (os oito de pedra inclusive), v406 (fechamento_v406 e os specs) e v407 (psion_canto_v407 e os specs) sao RECRIADOS e comparados com os da v407 selada\n", 1)
# ---------------------------------------------------------------- (c) a ordem de chamada medida por AST: agora a do tetelestai_terminal_v408
rx(r"^# \(5b'\) \[v407\] A ORDEM DE CHAMADA DO psion_canto_v407[^\n]*\n# ANTES da instrucao[^\n]*\n",
   "# (5b') [v408] A ORDEM DE CHAMADA DO tetelestai_terminal_v408, medida AQUI por AST (nao depende de a guarda_ordem_de_chamada_v408 conhecer a funcao nova): toda chave do core que o registro LE (tetelestai_terminal_v408, v408_terminal_mechanics, _v408_formal, _v398_beta) tem de estar pronta\n"
   "# ANTES da instrucao do main que o chama (vem de run_um, ou core[\"K\"] = ..., ou a chamada K(core) numa instrucao anterior); alem disso psion_canto_v407, _v407_rodar_specs, fechamento_v406 e _v406_rodar_specs (os registros herdados que o main roda antes) vem ANTES. Controles negativos: o bloco do terminal movido para antes de run_um, e a chamada do psion_canto_v407 retirada.\n", 1)
sub('_FN_PSION = ("psion_canto_v407", "v407_psion_mechanics", "_v407_formal", "_v407_chaves", "_v398_beta")', '_FN_PSION = ("tetelestai_terminal_v408", "v408_terminal_mechanics", "_v408_formal", "_v398_beta")')
sub('_EXIG_PSION = ("fechamento_v406", "_v406_rodar_specs", "_v405_rodar_specs", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers")',
    '_EXIG_PSION = ("psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "_v406_rodar_specs", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers")')
sub('    lidas_.discard("psion_canto_v407")', '    lidas_.discard("tetelestai_terminal_v408")')
sub('"psion_canto_v407(core)" in s_', '"tetelestai_terminal_v408(core)" in s_', 1)
sub('"psion_canto_v407(core)" in ast.unparse(st_)', '"tetelestai_terminal_v408(core)" in ast.unparse(st_)', 1)
sub(r'_lin_b = list(_lin); _ln_b = [i_ for i_, l_ in enumerate(_lin_b) if re.fullmatch(r"\s+_r406 = fechamento_v406\(core\)\s*", l_)]',
    r'_lin_b = list(_lin); _ln_b = [i_ for i_, l_ in enumerate(_lin_b) if re.fullmatch(r"\s+_r407 = psion_canto_v407\(core\)\s*", l_)]')
sub('assert len(_ln_b) == 1, ("a linha da chamada do fechamento_v406 nao foi achada uma vez", _ln_b)', 'assert len(_ln_b) == 1, ("a linha da chamada do psion_canto_v407 nao foi achada uma vez", _ln_b)')
sub(r'_lin_b[_ln_b[0]] = re.sub(r"_r406 = fechamento_v406\(core\)", "_r406 = {}", _lin_b[_ln_b[0]])', r'_lin_b[_ln_b[0]] = re.sub(r"_r407 = psion_canto_v407\(core\)", "_r407 = {}", _lin_b[_ln_b[0]])')
sub('_neg_b = _ordem_psion("\\n".join(_lin_b))   # (b) a chamada do fechamento_v406 retirada: o insumo exigido some', '_neg_b = _ordem_psion("\\n".join(_lin_b))   # (b) a chamada do psion_canto_v407 retirada: o insumo exigido some')
sub('rep["ordem_de_chamada_psion_canto_v408"] =', 'rep["ordem_de_chamada_tetelestai_terminal_v408"] =')
sub('U["v408_ordem_de_chamada_do_psion_canto_v408_medida_por_ast_com_dois_controles_negativos"] = bool(_op0["ok"] and _op0["n_chaves_lidas"] >= 5', 'U["v408_ordem_de_chamada_do_tetelestai_terminal_v408_medida_por_ast_com_dois_controles_negativos"] = bool(_op0["ok"] and _op0["n_chaves_lidas"] >= 4')
rx(r'"fechamento_v406" in \(_neg_b\.get\(', '"psion_canto_v407" in (_neg_b.get(', 1)
sub('print("ordem de chamada do psion_canto_v407 (AST propria):"', 'print("ordem de chamada do tetelestai_terminal_v408 (AST propria):"')
# ---------------------------------------------------------------- (d) o selo: nenhuma chave antiga muda
entre("    # [v407] o resumo do selo muda SO' no que a v408 declara", "\n\n\n_selo_inexplicado = sorted(",
      "    # [v408] NENHUMA chave antiga muda: fechamento_v406, testemunha_estatica_v396, psion_canto_v407, rede_fock_v394, psibit_v395 e os specs antigos NAO podem diferir no resumo do selo; se diferirem, ficam inexplicados e reprovam (as chaves NOVAS sao tetelestai_terminal_v408 e registros_v408)\n    return False")
sub('("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "registros_v407") + tuple(um._V407_REGISTROS_FUNCAO) and not _selo_explica(k_))   # (v408: as chaves NOVAS do selo sao psion_canto_v407 e registros_v407)',
    '("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "registros_v408") + tuple(um._V408_REGISTROS_FUNCAO) and not _selo_explica(k_))   # (v408: as chaves NOVAS do selo sao tetelestai_terminal_v408 e registros_v408)')
sub('for k_ in um._V407_REGISTROS_FUNCAO) and all(((seal.get("registros_v407") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V407_NOMES_REGISTROS)',
    'for k_ in um._V408_REGISTROS_FUNCAO) and all(((seal.get("registros_v408") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V408_NOMES_REGISTROS) and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V407_REGISTROS_FUNCAO) and all(((seal.get("registros_v407") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V407_NOMES_REGISTROS)')
sub('{"selo_pela_propria_tecnologia_v399", "um_version", "registros_v407", "fechamento_v406", "testemunha_estatica_v396"} | set(um._V407_REGISTROS_FUNCAO)) <= set(mud_selo)',
    '{"selo_pela_propria_tecnologia_v399", "um_version", "registros_v408"} | set(um._V408_REGISTROS_FUNCAO)) <= set(mud_selo)')
sub('and not ({"rede_fock_v394", "psibit_v395", "registros_v406"} & set(mud_selo)))',
    'and not ({"rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406", "psion_canto_v407", "registros_v406", "registros_v407"} & set(mud_selo)))')
# ---------------------------------------------------------------- os contratos pinam a escada da v408
sub('um._V406_FECHO_CONTRACT["expected_ladder"] == ESP and um._V407_PSION_CONTRACT["expected_ladder"] == ESP and _n_esc_base >= 1',
    'um._V406_FECHO_CONTRACT["expected_ladder"] == ESP and um._V407_PSION_CONTRACT["expected_ladder"] == ESP and um._V408_TERMINAL_CONTRACT["expected_ladder"] == ESP and _n_esc_base >= 1')
# ---------------------------------------------------------------- a guarda da v407 para os textos HERDADOS (v405 a v407); a da v408 (_GF5) fica para o texto novo
sub("import guarda_frases_v408 as _GF5\n",
    "import guarda_frases_v408 as _GF5\n"
    "import importlib.util as _ilu8   # (v408) a guarda da v407 para os textos HERDADOS (v405 a v407): o delta_v407 ja' vive neutralizado em DL.D7; a F29 da v408 reprovaria o «leituras do operador [ONTO]» da v407 selada, que e' texto selado, nao texto novo\n"
    "sys.modules.setdefault(\"delta_v407\", DL.D7)\n"
    "_sp7r = _ilu8.spec_from_file_location(\"runtime_v407\", os.path.join(DL.V407, \"runtime_v407.py\")); _rt7m = _ilu8.module_from_spec(_sp7r); _sp7r.loader.exec_module(_rt7m); sys.modules.setdefault(\"runtime_v407\", _rt7m)\n"
    "_sp7g = _ilu8.spec_from_file_location(\"guarda_frases_v407\", os.path.join(DL.V407, \"guarda_frases_v407.py\")); _GF7 = _ilu8.module_from_spec(_sp7g); _sp7g.loader.exec_module(_GF7)\n")
n_gf5 = t.count("_GF5.")
assert n_gf5 >= 6, n_gf5
t = t.replace("_GF5.", "_GF7.")   # (todos os usos ate' aqui sao sobre textos herdados; o bloco novo da v408, abaixo, usa _GF5)
# ---------------------------------------------------------------- (e) o bloco HERDADO da v406: os numeros da v406
sub('_FJ6 = json.load(open(os.path.join(DL.V407, DL.D6.KERNEL_DIR, "FLAGS_v407.json"), encoding="utf-8"))   # (v408) as 1794 bandeiras da v407: o FLAGS da v407 (o FLAGS_v408.json traz as 98 novas)',
    '_FJ6 = json.load(open(os.path.join(DL.V406, DL.D6.KERNEL_DIR, "FLAGS_v406.json"), encoding="utf-8"))   # (v408) as 1794 bandeiras da v406: o FLAGS da v406 (o FLAGS_v408.json traz as 43 novas)')
sub('_KHT6_v407 = json.load(open(os.path.join(DL.V407, _D6.KERNEL_DIR, "KH_N1_v407.json"), encoding="utf-8"))["linha_TOTAL"]   # a linha TOTAL do Audit da v407 (o piso que o spec herdado cobra agora)',
    '_KHT6_v406 = json.load(open(os.path.join(DL.V406, _D6.KERNEL_DIR, "KH_N1_v406.json"), encoding="utf-8"))["linha_TOTAL"]   # a linha TOTAL do Audit da v406 (o piso que o spec herdado da v406 cobra)')
sub('U["kh_n1_cobertura_v407_herdado_virou_piso_e_selou_na_v408"]', 'U["kh_n1_cobertura_v406_herdado_virou_piso_e_selou_na_v408"]')
assert t.count("_KHT6_v407") == 3, t.count("_KHT6_v407")
t = t.replace("_KHT6_v407", "_KHT6_v406")
sub('_h8_6["valor"] == CM["h8"]["pino_antigo_v407_entradas"]', '_h8_6["valor"] == _CM7["h8"]["pino_antigo_v406_entradas"]')
sub('any(str(e_).startswith("E20") for e_ in DL.ERRATAS_V408))   # (o c8 do fechamento_v406 le a chave do kernel', 'any(str(e_).startswith("E20") for e_ in DL.D7.ERRATAS_V407))   # (o c8 do fechamento_v406 le a chave do kernel')
sub('U["erratas_E20_os_tres_registros_da_v407_revistos_u7_c8_e_os_pisos_do_kh"]', 'U["erratas_E20_os_tres_registros_da_v406_revistos_u7_c8_e_os_pisos_do_kh"]')
n_f7h = len(re.findall(r"fechamento_v407_herdado_", t)); assert n_f7h >= 10, n_f7h
t = t.replace("fechamento_v407_herdado_", "fechamento_v406_herdado_")
n_c7h = len(re.findall(r"cunhagens_v407_herdado_", t)); assert n_c7h >= 2, n_c7h
t = t.replace("cunhagens_v407_herdado_", "cunhagens_v406_herdado_")
sub('rep["fechamento_v406_checagens_negadas"] = _det6   # (as checagens do fechamento HERDADO da v407 negadas, uma a uma)', 'rep["fechamento_v406_checagens_negadas"] = _det6   # (as checagens do fechamento HERDADO da v406 negadas, uma a uma)') if 'rep["fechamento_v406_checagens_negadas"] = _det6   # (as checagens do fechamento HERDADO da v407 negadas, uma a uma)' in t else None
# ---------------------------------------------------------------- (e') o bloco HERDADO da v407 (6m): os numeros da v407 vem do DL.D7 e do _CM7
i0 = t.index("# (6m) [v407] O REGISTRO COM FUNCAO psion_canto_v407 (o NOVO desta versao)")
i1 = t.index("# (8) o artigo\n")
bloco = t[i0:i1]
b0 = bloco
bloco = re.sub(r"^# \(6m\) \[v407\] O REGISTRO COM FUNCAO psion_canto_v407 \(o NOVO desta versao\)[^\n]*\n#[^\n]*\n#[^\n]*\n",
               "# (6m) [v407, HERDADO na v408: os numeros dele (9 modulos, 76 ancoras, 16 checagens, 98 bandeiras, 3 falas) saem do DL.D7, do contrato HERDADO do candidato e do CANDIDATO_v407.json, NUNCA do DL da v408] O REGISTRO COM FUNCAO psion_canto_v407: tudo certo, os numeros RECALCULADOS aqui por outro caminho,\n"
               "# a chave do lema (testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma) segue LIDA do kernel e nao literal; as quatro da v406 seguem lidas; o que fica False por teorema segue False; o gate que nao se move;\n"
               "# e cada elo recusa visivelmente (controles negativos): a ancora do lema, as 76 ancoras, as 9 fontes, as 3 falas, a escada, o beta, cada checagem de mecanica isolavel, a guarda das frases (da v407), o teste (d) so' por citacao.\n", bloco, count=1, flags=re.M)
assert bloco != b0
rep_blk = [('_FJ7 = json.load(open(os.path.join(KD, "FLAGS_v408.json"), encoding="utf-8"))', '_FJ7 = json.load(open(os.path.join(DL.V407, DL.D7.KERNEL_DIR, "FLAGS_v407.json"), encoding="utf-8"))   # (v408) as 98 bandeiras da v407: o FLAGS da v407'),
           ("_NCK7 = DL.N_CHECKS_FECHO   # as checagens do registro NOVO: 16 (c1..c16), lidas do DL", "_NCK7 = DL.D7.N_CHECKS_FECHO   # as checagens do registro HERDADO da v407: 16 (c1..c16), lidas do DL.D7"),
           ("DL.ANCORAS_POR_MODULO", "DL.D7.ANCORAS_POR_MODULO"), ("DL.BUNDLE_POR_REL", "DL.D7.BUNDLE_POR_REL"), ("DL.BUNDLE_RELS", "DL.D7.BUNDLE_RELS"), ("DL.N_BUNDLE", "DL.D7.N_BUNDLE"),
           ("DL.ANCORA_LEMA", "DL.D7.ANCORA_LEMA"), ("DL.ANCORA_PAR", "DL.D7.ANCORA_PAR"), ("DL.VERBATIM_PREFIXOS_DA_ORDEM_V408", "DL.D7.VERBATIM_PREFIXOS_DA_ORDEM_V407"),
           ('CM["n_bandeiras"]', '_CP7["n_flags"]'), ('CM["n_axiomas_das_ancoras"]', '_CM7["n_axiomas_das_ancoras"]'),
           ('_CP7["baseline"]["ladder"] == E407 and _CP7["baseline"]["sha256"] == hashlib.sha256(open(os.path.join(BASE, "um.py"), "rb").read()).hexdigest()', '_CP7["baseline"]["ladder"] == _CM7["escada"][0] and _CP7["baseline"]["sha256"][:16] == _CM7["base_v406_sha16"]'),
           ("DL.FICA_ABERTO_PAR_NA_FACE_DE_FOCK", "DL.D7.FICA_ABERTO_PAR_NA_FACE_DE_FOCK"), ("DL.FICA_ABERTO_PONTE_BELL_TT", "DL.D7.FICA_ABERTO_PONTE_BELL_TT"),
           ("DL.RESSALVAS_V408", "DL.D7.RESSALVAS_V407"), ("_xn7.get(\"assinatura_das_erratas\") == DL.ASSINA", "_xn7.get(\"assinatura_das_erratas\") == DL.D7.ASSINA"),
           ('len(_cn7.get("erratas") or []) == len(_sp7s["erratas"]) == len(DL.ERRATAS_V408) and all(e_["assinatura"].startswith("gerencia c1") for e_ in (_cn7.get("erratas") or []))',
            'len(_cn7.get("erratas") or []) == len(_sp7s["erratas"]) == len(DL.D7.ERRATAS_V407) + 1 and all(e_["assinatura"].startswith("gerencia c1") for e_ in (_cn7.get("erratas") or [])) and "E21" in str(((_cn7.get("erratas") or [{}])[-1]).get("agora")) and ((_cn7.get("erratas") or [{}])[-1]).get("assinatura") == DL.ASSINA'),
           ("psion_canto_v408_", "psion_canto_v407_herdado_"), ('U["cunhagens_v408_falas_de_03nov_decisoes_erratas_e_leituras"]', 'U["cunhagens_v407_herdado_falas_de_03nov_decisoes_erratas_e_leituras"]'),
           ('U["cunhagens_v408_o_4_44_nunca_vai_sozinho"]', 'U["cunhagens_v407_herdado_o_4_44_nunca_vai_sozinho"]'),
           ("DL.ANCORAS", "DL.D7.ANCORAS")]
for old_, new_ in rep_blk:
    assert old_ in bloco, ("ausente do bloco (6m)", old_[:80])
    bloco = bloco.replace(old_, new_)
assert "DL.D7.D7." not in bloco and "DL.D7.ANCORAS_POR_MODULO" in bloco
# o bloco do kh da v407 (agora PISO) + o bloco NOVO do kh da v408, no lugar do antigo
k0 = bloco.index('_kh7x = c.get("kh_n1_cobertura_v407") or {}')
k1 = bloco.index('print("psion_canto_v407:"')
bloco = bloco[:k0] + '''_kh7x = c.get("kh_n1_cobertura_v407") or {}; _kh7s = [s_ for s_ in um._V407_SPECS if s_["nome"] == "kh_n1_cobertura_v407"][0]
_KHT7 = json.load(open(os.path.join(DL.V407, DL.D7.KERNEL_DIR, "KH_N1_v407.json"), encoding="utf-8"))   # a medida do Audit da v407 (o piso que o spec herdado da v407 cobra agora)
_ck7 = {ck_["id"]: ck_ for ck_ in _kh7s["checks"]}
U["kh_n1_cobertura_v407_herdado_virou_piso_e_selou_na_v408"] = bool(_kh7x.get("all_verified") is True and (_kh7x.get("extras") or {}).get("n_modulos") == DL.D7.N_BUNDLE and (_kh7x.get("extras") or {}).get("n_bandeiras") == _CP7["n_flags"]
                                                                        and {i_: _ck7[i_]["op"] for i_ in ("h2", "h3", "h6", "h8")} == {"h2": "maior_igual", "h3": "maior_igual", "h6": "tamanho_maior_igual", "h8": "tamanho_maior_igual"} and len(_kh7s["erratas"]) >= 2 and "v408" in str(_kh7s["erratas"][-1].get("agora"))
                                                                        and _ck7["h2"]["valor"] == _KHT7["linha_TOTAL"]["decl"] and _ck7["h3"]["valor"] == _KHT7["linha_TOTAL"]["thm"] and _ck7["h8"]["valor"] == CM["h8"]["pino_antigo_v407_entradas"] and len(_kf0["formal_files_sha256"]) >= _ck7["h8"]["valor"]
                                                                        and _kf0["axiom_coverage_v392"]["decl"] >= _KHT7["linha_TOTAL"]["decl"] and _kf0["axiom_coverage_v392"]["thm"] >= _KHT7["linha_TOTAL"]["thm"] and len(_kf0["axiom_report"]) > _KHT7["linha_TOTAL"]["decl"])
''' + bloco[k1:]
t = t[:i0] + bloco + t[i1:]
# ---------------------------------------------------------------- (f) o bloco NOVO (6n): tetelestai_terminal_v408
NOVO = r'''# (6n) [v408] O REGISTRO COM FUNCAO tetelestai_terminal_v408 (o NOVO desta versao): tudo certo; os numeros RECALCULADOS aqui por outro caminho (as quatro fontes pelo BUNDLE_v408.json via DL, as bandeiras pelo FLAGS_v408.json, as 41 ancoras pelo DL.ANCORAS, o beta pelo alfa CODATA x sqrt(e), a aritmetica das pedras pelo math do ensaio);
# NENHUMA chave antiga muda (o core antes e depois do registro e' igual em tudo menos a propria chave); o gate que nao se move; o insumo PURGADO pinado por sha256 e a integra fora; e cada elo recusa visivelmente (controles negativos): as 41 ancoras, as 4 fontes, as 9 falas do contrato, a escada, o beta, as checagens de mecanica que o core alcanca, a guarda das frases (da v408).
_CP8, _TP8 = um._V408_TERMINAL_CONTRACT, um._V408_TERMINAL_TEXT
_FJ8 = json.load(open(os.path.join(KD, "FLAGS_v408.json"), encoding="utf-8"))
_FLAG_NOME8 = {f_[0]: f_[1] for f_ in _FJ8["flags"]}
_ANC_FLAGS8 = {n_: a_.get("flag") for n_, a_ in _CP8["ancoras"].items()}
_rapido8 = lambda: dict(core_s)   # o tetelestai_terminal_v408 so' LE o core e grava a propria chave: uma copia rasa basta (os campos mexidos abaixo sao copiados um a um por _kf6/_set6)
r8 = um.tetelestai_terminal_v408(cs()); RTT = r8
_v8 = r8.get("values") or {}
_NCK8 = DL.N_CHECKS_FECHO   # as checagens do registro NOVO: 16 (c1..c16), lidas do DL
U["tetelestai_terminal_v408_tudo_certo"] = bool(r8["all_verified"] is True and r8["verdict"] == _TP8["veredito_ok"] and r8["runtime_executed"] is True and r8["does_not_gate_core"] is True and r8["mechanics"]["n_checks"] == _NCK8 == len(r8["mechanics"]["checks"]) == 16 and all(ck_["ok"] for ck_ in r8["mechanics"]["checks"])
                                                and [ck_["id"] for ck_ in r8["mechanics"]["checks"]] == ["c%d" % i_ for i_ in range(1, _NCK8 + 1)]
                                                and r8["exact_ladder"] is True and r8["embedded_sources_ok"] is True and r8["embedded_sources_n_ok"] == DL.N_BUNDLE == len(DL.BUNDLE_RELS) == 4 and r8["beta_ok"] is True and all(r8["anchors"].values()) and len(r8["anchors"]) == len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 41
                                                and all(r8["inscriptions"].values()) and not r8["guarda_violacoes"] and _v8.get("n_ancoras_ok") == _v8.get("n_ancoras") == len(DL.ANCORAS) and _v8.get("n_modulos_ok") == _v8.get("n_modulos") == DL.N_BUNDLE and _v8.get("n_flags_true") == _v8.get("n_flags") == CM["n_bandeiras"] == _FJ8["n_flags"] and _v8.get("escada") == [ESP, ESP, ESP]
                                                and r8["ancora_principal"] == DL.ANCORA_PRINCIPAL and r8["ancoras_principais"] == list(DL.ANCORAS_PRINCIPAIS) and r8["pedras"] == list(_CP8["bundle"]["pedras"]) == [p_["name"] for p_ in DL.PEDRAS_V408] and r8["nome_provisorio"] is None and r8["chaves_antigas_que_mudam"] == [] and len(r8["inscriptions"]) == len(_CP8["verbatins"]) == 9
                                                and _v8.get("respostas_ok") is True and len(_v8.get("respostas") or {}) == len(DL.RESPOSTAS_DO_OPERADOR) == 7 and all(_v8["por_modulo"].values()) and len(_v8["por_modulo"]) == 4)
U["tetelestai_terminal_v408_veredito_e_textos_sem_palavra_proibida"] = bool(not guarda_txt(r8) and not _GUARDA98.search(r8["verdict"]) and not um._v408_guarda_frases(r8["verdict"]) and not um._v408_guarda_frases(json.dumps(r8["mechanics"]["checks"], ensure_ascii=False)) and not um._v408_guarda_frases(json.dumps({k_: r8.get(k_) for k_ in ("limites", "diz", "nao_diz", "ressalvas", "scope")}, ensure_ascii=False))
                                                                          and not _GF5.violacoes(r8["verdict"]) and not _GF5.violacoes(json.dumps({k_: r8.get(k_) for k_ in ("limites", "diz", "nao_diz", "ressalvas", "scope")}, ensure_ascii=False)))
# os numeros RECALCULADOS aqui por OUTRO caminho: as fontes pelo BUNDLE_v408.json (lido pelo delta), as bandeiras pelo FLAGS_v408.json, as ancoras pelo DL.ANCORAS e pelo FLAGS (cada ancora com bandeira aponta para a mesma declaracao), o beta pelo alfa x sqrt(e)
_fontes_ok8 = sum(1 for rel_ in DL.BUNDLE_RELS if hashlib.sha256(EMBK[rel_].encode("utf-8")).hexdigest() == DL.BUNDLE_POR_REL[rel_]["sha256"] == _kf0["formal_files_sha256"].get(rel_) == _CP8["source_sha256"][rel_])
_flags_ok8 = sum(1 for f_ in _FJ8["flags"] if _kf0.get(f_[0]) is True)
_anc_ok8 = sum(1 for n_ in DL.ANCORAS if isinstance(_kf0["axiom_report"].get(n_), list) and _kf0["axiom_report"][n_] and set(_kf0["axiom_report"][n_]) <= _trio6 and _kf0["declaration_sources_v394"].get(n_) == DL.ANCORAS[n_]["rel"])
_flag_aponta_8 = all(_FLAG_NOME8.get(a_.get("flag")) == n_ for n_, a_ in _CP8["ancoras"].items() if a_.get("flag"))
U["tetelestai_terminal_v408_os_numeros_foram_recalculados_aqui"] = bool(_fontes_ok8 == DL.N_BUNDLE == _v8["n_modulos_ok"] and _flags_ok8 == len(_FJ8["flags"]) == CM["n_bandeiras"] == _v8["n_flags_true"] and _anc_ok8 == len(DL.ANCORAS) == _v8["n_ancoras_ok"] and abs(_v8["beta"] - _bf6) <= 1e-15 and abs(c["beta"] / _bf6 - 1.0) <= 1e-9
                                                                        and set(r8["anchors"]) == set(DL.ANCORAS) == set(_CP8["ancoras"]) and set(DL.ANCORAS_POR_MODULO) == set(DL.BUNDLE_RELS) == set(_CP8["ancoras_por_modulo"]) and {rel_: list(v_) for rel_, v_ in DL.ANCORAS_POR_MODULO.items()} == {rel_: list(v_) for rel_, v_ in _CP8["ancoras_por_modulo"].items()}
                                                                        and sum(len(v_) for v_ in DL.ANCORAS_POR_MODULO.values()) == len(DL.ANCORAS) and _flag_aponta_8 and _kf0["formal_files_sha256"].keys() >= set(DL.BUNDLE_RELS) and len(_kf0["formal_files_sha256"]) == CM["h8"]["entradas"] and ESP == CM["escada"][1] == c["external_ladder"]["n_theorems_clean"] == c["external_ladder"]["n_theorems_expected"] == _CP8["expected_ladder"]
                                                                        and _CP8["baseline"]["gate_verdict"] == ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict") and _CP8["baseline"]["ladder"] == E407 and _CP8["baseline"]["sha256"] == hashlib.sha256(open(os.path.join(BASE, "um.py"), "rb").read()).hexdigest()
                                                                        and max(CM["n_axiomas_das_ancoras"].values()) <= len(_trio6) and len(CM["n_axiomas_das_ancoras"]) == len(DL.ANCORAS) == 41)
# a ARITMETICA das pedras (c3 a c11), recalculada aqui pelo math do ensaio com o beta do alfa x sqrt(e): os valores que o registro gravou batem
_ln2_8 = _math.log(2.0); _f12_8 = _math.exp(-0.5)
U["tetelestai_terminal_v408_a_aritmetica_das_pedras_recalculada_aqui"] = bool(abs(_v8["meia_nat_fator"] - _f12_8) <= 1e-15 and 0.0 < _f12_8 < 1.0 and abs((_f12_8 + (1.0 - _f12_8)) - 1.0) <= 1e-15 and abs(_v8["coeficiente_de_jones_s1"] - _math.exp(-_bf6)) <= 1e-15 and 0.0 < _v8["coeficiente_de_jones_s1"] < 1.0 and abs(_v8["ln2"] - _ln2_8) <= 1e-15
                                                                              and _v8["dim_chainIdx_N0_a_N10"] == [2 ** (n_ + 1) for n_ in range(11)] and all(abs(_v8["tempo_da_torre_N0_a_N10"][n_] - (n_ + 1) * _ln2_8 / _bf6) <= 1e-12 * ((n_ + 1) * _ln2_8 / _bf6) for n_ in range(11))
                                                                              and all(abs(_math.exp(-(t_ * _bf6)) - 2.0 ** (-(n_ + 1))) <= 1e-12 for n_, t_ in enumerate(_v8["tempo_da_torre_N0_a_N10"])) and _v8["piso_landauer_T1K_J"] > 0.0 and abs(_v8["piso_landauer_T1K_J"] - um._V408_KB_SI_J_PER_K * _ln2_8) <= 1e-30 and um._V408_KB_SI_J_PER_K > 0.0
                                                                              and abs(_v8["vazamento_t1_g1"] - _math.exp(-_bf6)) <= 1e-15)
# NENHUMA chave antiga muda: o core ANTES e DEPOIS do registro sao iguais em tudo menos a propria chave; o gate nao se move; a chave do lema (v407) segue lida e True; o que fica False por teorema segue False
_cc9 = _rapido8(); _cc9.pop("tetelestai_terminal_v408", None); _antes9 = {k_: _J(_cc9[k_]) for k_ in ("qg_closure", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers", "kernel_formalization", "external_ladder", "fechamento_v406", "psion_canto_v407")}; _k9 = set(_cc9)
um.tetelestai_terminal_v408(_cc9)
U["tetelestai_terminal_v408_so_grava_a_propria_chave_e_nao_toca_nas_outras"] = bool(set(_cc9) - _k9 == {"tetelestai_terminal_v408"} and all(_J(_cc9[k_]) == v_ for k_, v_ in _antes9.items()))
U["tetelestai_terminal_v408_o_gate_nao_se_move_e_nenhuma_chave_antiga_muda"] = bool(((c.get("qg_closure") or {}).get("gate") or {}).get("verdict") == ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict") == _CP8["baseline"]["gate_verdict"] == _v8["gate_verdict"] and any(ck_["id"] == "c12" and ck_["ok"] for ck_ in r8["mechanics"]["checks"]) and _CP8["chaves"] == [] and DL.CHAVES_V408 == []
                                                                                   and c["testemunha_estatica_v396"]["fock_face"]["linked_to_the_corner_by_a_lemma"] is True and (c.get("psion_canto_v407") or {}).get("link_read_from_the_kernel") is True and c["qg_closure"]["gate"]["full_static_witness_exists"] is False and c["witness_rigidity"]["trivial_inhabitant_exists"] is False
                                                                                   and list(_CP8["fica_false_por_teorema"]) == DL.FICAM_FALSE_POR_TEOREMA and r8["fica_aberto"] == {"par_na_face_de_fock": DL.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, "ponte_bell_tt": DL.FICA_ABERTO_PONTE_BELL_TT} == _CP8["fica_aberto"] and "[OPEN]" in DL.FICA_ABERTO_PAR_NA_FACE_DE_FOCK and "E21" in DL.FICA_ABERTO_PAR_NA_FACE_DE_FOCK)
# o insumo PURGADO (E23): pinado por sha256 e relido do disco; a integra NAO e' fonte desta versao (citada so' por sha16); o recibo da purga e' fonte
_ip8 = _CP8["insumo_purgado"]; _fp8 = um._V408_FONTES[_ip8["fonte_chave"]]
U["tetelestai_terminal_v408_o_insumo_purgado_e_pinado_e_a_integra_fica_fora"] = bool(_fp8["sha256"] == _ip8["sha256"] == hashlib.sha256(open(_fp8["arquivo"], "rb").read()).hexdigest() == DL.PURGADO_SHA256 and _ip8["integra_fora_do_espelho"] is True and _ip8["integra_pinada"] is False and _ip8["integra_sha16"] == DL.ORIGEM_PURGA_SHA16_DA_ORDEM
                                                                                    and not any(str(v_.get("sha256", "")).startswith(_ip8["integra_sha16"]) for v_ in um._V408_FONTES.values()) and _ip8["recibo_chave"] in um._V408_FONTES and r8["insumo_purgado"] == _ip8 and any(ck_["id"] == "c15" and ck_["ok"] for ck_ in r8["mechanics"]["checks"])
                                                                                    and _ip8["linhas_substituidas"] == DL.PURGA_LINHAS_SUBSTITUIDAS and _ip8["ocorrencias_na_guarda"] == 0)
# --- controles negativos: cada elo recusa
ok_ = True
for n_ in _CP8["ancoras"]:   # axioma fora do trio em CADA ancora lida
    c_ = _kf6(copiar=("axiom_report",)); c_["kernel_formalization"]["axiom_report"][n_] = ["propext", "sorryAx"]; ok_ = ok_ and _recusa6(um.tetelestai_terminal_v408(c_))
U["tetelestai_terminal_v408_axioma_fora_do_trio_em_cada_ancora_recusa"] = bool(ok_ and len(_CP8["ancoras"]) == len(DL.ANCORAS) == 41)
ok_ = True
for n_ in _CP8["ancoras"]:   # proveniencia errada em CADA ancora (o compilador diz outro modulo)
    c_ = _kf6(copiar=("declaration_sources_v394",)); c_["kernel_formalization"]["declaration_sources_v394"][n_] = "TGLExt/Outro.lean"; ok_ = ok_ and _recusa6(um.tetelestai_terminal_v408(c_))
U["tetelestai_terminal_v408_proveniencia_errada_em_cada_ancora_recusa"] = bool(ok_)
ok_ = True
for n_ in _CP8["ancoras"]:   # ancora AUSENTE do axiom_report do rito
    c_ = _kf6(copiar=("axiom_report",)); c_["kernel_formalization"]["axiom_report"].pop(n_); ok_ = ok_ and _recusa6(um.tetelestai_terminal_v408(c_))
U["tetelestai_terminal_v408_ancora_ausente_do_kernel_em_cada_ancora_recusa"] = bool(ok_)
ok_ = True
for n_, f_ in _ANC_FLAGS8.items():   # bandeira falsa de CADA ancora com bandeira
    if f_:
        c_ = _kf6(); c_["kernel_formalization"][f_] = False; ok_ = ok_ and _recusa6(um.tetelestai_terminal_v408(c_))
U["tetelestai_terminal_v408_bandeira_falsa_de_cada_ancora_recusa"] = bool(ok_ and sum(1 for f_ in _ANC_FLAGS8.values() if f_) == len(DL.ANCORAS))
ok_ = True; n_ok_ = 0
for rel_ in _CP8["source_sha256"]:   # a fonte de CADA um dos 4 modulos adulterada no corpo embutido: recusa, e a contagem cai para 3
    _ant8 = um._EMBEDDED_KERNEL_FILES[rel_]; um._EMBEDDED_KERNEL_FILES[rel_] = _ant8 + " "
    try:
        rr_ = um.tetelestai_terminal_v408(_rapido8())
    finally:
        um._EMBEDDED_KERNEL_FILES[rel_] = _ant8
    ok_ = ok_ and _recusa6(rr_) and rr_["embedded_sources_ok"] is False and rr_["embedded_sources_n_ok"] == DL.N_BUNDLE - 1; n_ok_ += 1
U["tetelestai_terminal_v408_fonte_adulterada_de_cada_um_dos_4_modulos_recusa"] = bool(ok_ and n_ok_ == DL.N_BUNDLE == 4)
ok_ = True
for rel_ in _CP8["source_sha256"]:   # o hash formal do rito errado em CADA um dos 4 modulos
    c_ = _kf6(copiar=("formal_files_sha256",)); c_["kernel_formalization"]["formal_files_sha256"][rel_] = "0" * 64; rr_ = um.tetelestai_terminal_v408(c_)
    ok_ = ok_ and _recusa6(rr_) and rr_["embedded_sources_n_ok"] == DL.N_BUNDLE - 1
U["tetelestai_terminal_v408_hash_formal_errado_em_cada_um_dos_4_modulos_recusa"] = bool(ok_)
ok_ = True
for rel_ in _CP8["source_sha256"]:   # o sha256 PINADO no contrato errado em CADA um dos 4 modulos
    _p08 = _CP8["source_sha256"][rel_]; _CP8["source_sha256"][rel_] = "0" * 64
    try:
        rr_ = um.tetelestai_terminal_v408(_rapido8())
    finally:
        _CP8["source_sha256"][rel_] = _p08
    ok_ = ok_ and _recusa6(rr_) and rr_["embedded_sources_n_ok"] == DL.N_BUNDLE - 1
U["tetelestai_terminal_v408_pino_do_contrato_errado_em_cada_um_dos_4_modulos_recusa"] = bool(ok_)
ok_ = True
for ch_ in _CP8["verbatins"]:   # a inscricao do operador adulterada em CADA fala do contrato (o texto embutido muda: o sha256 deixa de bater)
    _v08 = um._V408_VERBATINS2[ch_]["text"]; um._V408_VERBATINS2[ch_]["text"] = _v08 + " "
    try:
        rr_ = um.tetelestai_terminal_v408(_rapido8()); ok_ = ok_ and _recusa6(rr_) and rr_["inscriptions"][ch_] is False
    finally:
        um._V408_VERBATINS2[ch_]["text"] = _v08
U["tetelestai_terminal_v408_inscricao_do_operador_adulterada_recusa"] = bool(ok_ and len(_CP8["verbatins"]) == 9 and set(_CP8["verbatins"]) <= set(um._V408_VERBATINS2) and len(um._V408_VERBATINS2) == len(DL.VERBATIM_PREFIXOS_DA_ORDEM_V408) == DL.N_FALAS_V408 == 12)
c_ = _rapido8(); c_["external_ladder"] = dict(c_["external_ladder"]); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = um.tetelestai_terminal_v408(c_)
c2_ = _kf6(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = um.tetelestai_terminal_v408(c2_)
U["tetelestai_terminal_v408_escada_errada_ou_kernel_nao_verificado_recusa"] = bool(_recusa6(rr_) and rr_["exact_ladder"] is False and _recusa6(rr2_))
c_ = _rapido8(); c_["beta"] = c_["beta"] * 1.001; _rb8 = um.tetelestai_terminal_v408(c_)
_a08 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a08 * 1.001
try:
    _ra8 = um.tetelestai_terminal_v408(_rapido8())
finally:
    um.SEALED_CODATA_ALPHA = _a08
U["tetelestai_terminal_v408_beta_adulterado_recusa"] = bool(_rb8["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb8["verdict"] and _ra8["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra8["verdict"])
# cada checagem de MECANICA que o core alcanca, negada: a recusa e' a daquela checagem (MECHANICS_CHECK_FAILED + o id). As checagens c1, c2, c14 e c16 repetem o que a `_v408_formal` e o beta ja' barram antes (controles acima); c3 a c11 sao ARITMETICA PURA com beta em runtime e nao tem core que as negue:
# a mecanica e' chamada direto com beta = 0 (fora do intervalo aberto: c6, c7, c9 e c16 caem) e com o gate do contrato trocado (c12 cai), o que mostra que cada uma mede o que diz.
_mec8 = []   # (id esperado, core mexido, especial)
_nao_anc8 = [f_[0] for f_ in _FJ8["flags"] if f_[0] not in set(_ANC_FLAGS8.values())]
_mec8.append(("c2", _c6_mexe(lambda c_: None), "raiz"))
_mec8.append(("c12", _c6_mexe(lambda c_: _set6(c_, ["qg_closure", "gate", "verdict"], "OUTRO")), None))
if _nao_anc8:
    _mec8.append(("c13", _c6_mexe(lambda c_: _set6(c_, ["kernel_formalization", _nao_anc8[0]], False)), None))
_mec8.append(("c15", _c6_mexe(lambda c_: None), "fonte_purgada_adulterada"))
ok_ = True; _det8 = {}
for id_, c_, esp_ in _mec8:
    if esp_ == "raiz":   # c2: a raiz embutida sem o import da TetelestaiTerminal (as fontes seguem batendo; a raiz nao traz os quatro imports)
        _ant8 = um._EMBEDDED_KERNEL_FILES["TGLExt.lean"]; um._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = _ant8.replace("import TGLExt.TetelestaiTerminal", "-- retirado")
        try:
            rr_ = um.tetelestai_terminal_v408(_rapido8())
        finally:
            um._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = _ant8
    elif esp_ == "fonte_purgada_adulterada":   # c15: o sha256 pinado da fonte purgada trocado: a releitura do disco deixa de bater
        _s08 = um._V408_FONTES[_ip8["fonte_chave"]]["sha256"]; um._V408_FONTES[_ip8["fonte_chave"]]["sha256"] = "0" * 64
        try:
            rr_ = um.tetelestai_terminal_v408(_rapido8())
        finally:
            um._V408_FONTES[_ip8["fonte_chave"]]["sha256"] = _s08
    else:
        rr_ = um.tetelestai_terminal_v408(c_)
    _det8.setdefault(id_, []).append(_falhos6(rr_))
    ok_ = ok_ and rr_["all_verified"] is False and "MECHANICS_CHECK_FAILED" in rr_["verdict"] and id_ in _falhos6(rr_)
_mt0 = um.v408_terminal_mechanics(0.0, cs(), _CP8)   # beta fora do intervalo aberto: as aritmeticas com beta caem (c6, c7, c9) e a c16
_mtg = um.v408_terminal_mechanics(_bf6, cs(), dict(_CP8, baseline=dict(_CP8["baseline"], gate_verdict="OUTRO")))   # o gate do contrato trocado: c12 cai
_mtn = um.v408_terminal_mechanics(_bf6, cs(), dict(_CP8, n_ancoras=len(_CP8["ancoras"]) + 1))   # o contrato pede uma ancora a mais: c1 cai
_f0_ = lambda m_: sorted(ck_["id"] for ck_ in m_["checks"] if not ck_["ok"])
_IDS8 = {"c%d" % i_ for i_ in range(1, _NCK8 + 1)}
U["tetelestai_terminal_v408_cada_checagem_de_mecanica_negada_recusa_pela_propria_checagem"] = bool(ok_ and set(_det8) <= _IDS8 and sorted(_det8) == sorted({"c2", "c12", "c15"} | ({"c13"} if _nao_anc8 else set())) and _NCK8 == r8["mechanics"]["n_checks"]
                                                                                                   and _mt0["passed"] is False and {"c6", "c7", "c9", "c16"} <= set(_f0_(_mt0)) and _mtg["passed"] is False and _f0_(_mtg) == ["c12"] and _mtn["passed"] is False and _f0_(_mtn) == ["c1"]
                                                                                                   and um.v408_terminal_mechanics(_bf6, cs(), _CP8)["passed"] is True)
rep["tetelestai_terminal_v408_checagens_negadas"] = {"por_core": _det8, "beta_zero": _f0_(_mt0), "gate_trocado": _f0_(_mtg), "ancora_a_mais_no_contrato": _f0_(_mtn)}
# a GUARDA DAS FRASES (v405 a v408): cada frase proibida plantada no texto recusa; a frase certa passa; o que fica ABERTO, dito, passa
ok_ = True
_dz8 = _TP8["diz"]; _d08 = list(_dz8)
_FRASES_PROIBIDAS8 = ("tudo é teorema", "tudo derivado", "nenhuma hipótese resta", "everything is a theorem", "a luz não tem autovetor", "o único autovetor", "o certificado está confirmado", "the closure is confirmed", "K(O) ≠ ⊥ está provado", "FULLY_" + "DERIVED",
                      "o par na face de Fock está provado", "Ω = Φ⁺", "o vácuo de Fock é o vetor de Bell", "a ponte Bell-TT é teorema", "PAIR_ON_THE_FOCK_FACE_" + "PROVED",
                      "há relação sem peso", "relação sem peso existe", "there is a relation without weight", "o que resta sem peso é relação", "a TGL não tem terminal", "the TGL has no terminal", "P = NP está provado", "P = NP is a theorem", "provamos que P = NP",
                      "a impedância é um termo", "termo de impedância", "leitura do operador [ONTO]", "[ONTO] do operador", "TERMINAL_CONF" + "IRMED", "P_EQUALS_NP", "CLASSES_PROVED")
for f_ in _FRASES_PROIBIDAS8:
    _dz8[:] = _d08 + ["a cadeia: " + f_]
    try:
        rr_ = um.tetelestai_terminal_v408(_rapido8())
    finally:
        _dz8[:] = _d08
    ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and bool(rr_["guarda_violacoes"])
_FRASES_BOAS8 = (DL.FRASE_DA_MOLDURA_V408_PT, DL.FRASE_DA_MOLDURA_V408_EN, DL.FRASE_DA_MOLDURA_V407_PT, "não há relação sem peso", "relação sem peso é a origem da mentira", "relação sem peso é impossível", "there is no relation without weight", "«P = nP» só no sentido do operador: P só é P lido pelo módulo n minimamente acoplado",
                 "a palavra «impedância» fica podada como termo; o nome do operador é «inclinação modular (cociclo)»", DL.REGRA_DO_4_44, DL.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, "o terminal é a leitura, não o fim do decaimento", "o zero inscrito é o Um; o Um não é o zero absoluto")
for f_ in _FRASES_BOAS8:
    _dz8[:] = _d08 + [f_]
    try:
        rr_ = um.tetelestai_terminal_v408(_rapido8())
    finally:
        _dz8[:] = _d08
    ok_ = ok_ and rr_["all_verified"] is True
U["tetelestai_terminal_v408_guarda_das_frases_cada_frase_proibida_recusa_e_a_frase_certa_passa"] = bool(ok_ and um.tetelestai_terminal_v408(cs())["all_verified"] is True and _GF5.controle_negativo()["ok"] is True and len(set(_FRASES_PROIBIDAS8)) == len(_FRASES_PROIBIDAS8))
# --- as falas de 04/11 (cunhagens_v408), as decisoes D48-D54, as erratas E21-E23 e a cobertura exata (kh_n1_cobertura_v408)
_cn8 = c.get("cunhagens_v408") or {}; _xn8 = _cn8.get("extras") or {}
_sp8s = [s_ for s_ in um._V408_SPECS if s_["nome"] == "cunhagens_v408"][0]
U["cunhagens_v408_falas_de_04nov_decisoes_erratas_e_leituras"] = bool(_cn8.get("all_verified") is True and _cn8.get("does_not_gate_core") is True and len(_cn8.get("verbatim") or {}) == len(DL.VERBATIM_PREFIXOS_DA_ORDEM_V408) == len(_sp8s["verbatins"]) == DL.N_FALAS_V408 == 12 and all(v_["embedded_ok"] for v_ in (_cn8.get("verbatim") or {}).values())
                                                                      and len(_cn8.get("erratas") or []) == len(_sp8s["erratas"]) == 4 and all(e_["assinatura"] == DL.ASSINA for e_ in (_cn8.get("erratas") or [])) and [("E21" in str(e_.get("agora"))) for e_ in (_cn8.get("erratas") or [])][0] is True
                                                                      and len(_cn8.get("leituras_do_operador") or []) == len(_sp8s["leituras_do_operador"]) == len(DL.FRASES_V408) and set(_xn8.get("decisoes") or {}) == {"D48", "D49", "D50", "D51", "D52", "D53", "D54"} and _xn8.get("n_modulos") == DL.N_BUNDLE and _xn8.get("n_bandeiras") == CM["n_bandeiras"] and _xn8.get("n_falas") == 12
                                                                      and _xn8.get("assinatura_das_erratas") == DL.ASSINA and _xn8.get("ressalvas") == list(DL.RESSALVAS_V408) == list(_CP8["ressalvas"]) and _xn8.get("nomes_das_pedras") == dict(_CP8["bundle"]["nomes_do_operador"]) and sorted((_xn8.get("autores") or {}).values()) == sorted(["operador"] * 10 + [DL.AUTOR_MISTO] * 2)
                                                                      and not _GF5.violacoes(str(_cn8.get("verdict"))) and not _GF5.violacoes(json.dumps({k_: _cn8.get(k_) for k_ in ("limites", "diz", "nao_diz", "erratas")}, ensure_ascii=False)) and not um._v408_guarda_frases(json.dumps({k_: _cn8.get(k_) for k_ in ("limites", "diz", "nao_diz", "erratas")}, ensure_ascii=False)))
_mist8 = {k_: v_ for k_, v_ in um._V408_VERBATINS2.items() if v_.get("autor") == DL.AUTOR_MISTO}   # os dois arquivos de autor misto: o texto EMBUTIDO e' so' o paragrafo do operador (o corte nao aparece); o arquivo inteiro entra por sha256
U["cunhagens_v408_os_dois_arquivos_de_autor_misto_embutem_so_o_paragrafo_do_operador"] = bool(len(_mist8) == 2 and all(v_["corte"] not in v_["text"] and hashlib.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and hashlib.sha256(open(v_["arquivo_inteiro"], "rb").read()).hexdigest() == v_["sha256_arquivo_inteiro"] != v_["sha256"] and v_["corte"] in open(v_["arquivo_inteiro"], encoding="utf-8").read() for v_ in _mist8.values())
                                                                                                and all(v_.get("autor") == "operador" for k_, v_ in um._V408_VERBATINS2.items() if k_ not in _mist8))
_txts444_8 = (json.dumps(_cn8, ensure_ascii=False), json.dumps(r8, ensure_ascii=False))
U["cunhagens_v408_o_4_44_nunca_vai_sozinho"] = bool(_CP8["regra_do_4_44"] == DL.REGRA_DO_4_44 and all(("4,44" not in s_) or (DL.REGRA_DO_4_44 in s_) for s_ in _txts444_8))   # (se um texto da v408 cita o 4,44, ele carrega a regra inteira)
_kh8x = c.get("kh_n1_cobertura_v408") or {}; _kh8s = [s_ for s_ in um._V408_SPECS if s_["nome"] == "kh_n1_cobertura_v408"][0]
_KHT8 = json.load(open(os.path.join(KD, "KH_N1_v408.json"), encoding="utf-8"))   # a medida do Audit da v408, lida do arquivo da cadeia (nao digitada)
_cov0 = core0["kernel_formalization"]["axiom_coverage_v392"]
_ck8 = {ck_["id"]: ck_ for ck_ in _kh8s["checks"]}
_h8v8 = _ck8["h8"]["valor"]
U["kh_n1_cobertura_v408_selou_a_igualdade_exata_e_as_v407_sao_piso"] = bool(_kh8x.get("all_verified") is True and _kh7x.get("all_verified") is True and (c.get("kh_n1_cobertura_v406") or {}).get("all_verified") is True and (_kh8x.get("extras") or {}).get("n_modulos") == DL.N_BUNDLE and (_kh8x.get("extras") or {}).get("n_bandeiras") == CM["n_bandeiras"]
                                                                            and {i_: _ck8[i_]["op"] for i_ in ("h2", "h3", "h6", "h8")} == {"h2": "igual", "h3": "igual", "h6": "tamanho_igual", "h8": "igual"} and len(_kh8s["erratas"]) >= 1
                                                                            and _kf0["axiom_coverage_v392"]["decl"] == _KHT8["linha_TOTAL"]["decl"] == _ck8["h2"]["valor"] == _ck8["h6"]["valor"] and _kf0["axiom_coverage_v392"]["thm"] == _KHT8["linha_TOTAL"]["thm"] == _ck8["h3"]["valor"]
                                                                            and _kf0["axiom_coverage_v392"]["fora_do_trio"] == _KHT8["linha_TOTAL"]["fora_do_trio"] == 0 and len(_kf0["axiom_report"]) == _KHT8["linha_TOTAL"]["decl"] and _ck8["h7"]["valor"] == _cov0["decl"] and _ck8["h7b"]["valor"] == _cov0["thm"]
                                                                            and (_kh8x.get("extras") or {}).get("delta_vs_v407") == {"decl": _KHT8["linha_TOTAL"]["decl"] - _cov0["decl"], "thm": _KHT8["linha_TOTAL"]["thm"] - _cov0["thm"]} == _KHT8["delta_vs_v407"]
                                                                            and isinstance(_h8v8, dict) and dict(_h8v8) == dict(_kf0["formal_files_sha256"]) and len(_h8v8) == CM["h8"]["entradas"])   # o pino exato da arvore do Nos: as embutidas + os residuais, arquivo -> sha256
print("tetelestai_terminal_v408:", r8["all_verified"], "|", r8["verdict"][:96], "| ancoras:", _v8.get("n_ancoras_ok"), "/", _v8.get("n_ancoras"), "| checagens negadas:", sorted(_det8), "| beta=0:", _f0_(_mt0))
rep["tetelestai_terminal_v408"] = {"verdict": r8["verdict"], "all_verified": r8["all_verified"], "n_checks": r8["mechanics"]["n_checks"], "values": {k_: v_ for k_, v_ in r8["values"].items() if k_ not in ("ancoras",)}, "anchors": r8["anchors"], "embedded_sources_n_ok": r8["embedded_sources_n_ok"],
                                   "numeros_recalculados": {"fontes_ok": _fontes_ok8, "flags_true": _flags_ok8, "ancoras_ok": _anc_ok8, "beta": _bf6}, "checagens_negadas": rep["tetelestai_terminal_v408_checagens_negadas"], "insumo_purgado": _ip8, "nome_provisorio": r8["nome_provisorio"]}
'''
sub("# (8) o artigo\n", NOVO + "# (8) o artigo\n")
# ---------------------------------------------------------------- (g) o artigo: a secao v408 antes da v407 (o oraculo tipado aqui TEM de bater com os snippets)
rx(r'^T408 = "O psíon e o canto: a passagem sob compressão e o par"; T408E = "The psion and the corner: the passage under compression, and the pair"[^\n]*\n',
   'TPS407 = "O psíon e o canto: a passagem sob compressão e o par"; TPS407E = "The psion and the corner: the passage under compression, and the pair"   # a secao da v407 (HERDADA: logo depois da nova)\n'
   'T408 = "Tetelestai é o terminal: a leitura, a poda, a quitação; o tempo é a moeda de $\\\\beta$; o dicionário e o ponto de contradição"; T408E = "Tetelestai is the terminal: the reading, the pruning, the settlement; time is the currency of $\\\\beta$; the dictionary and the point of contradiction"   # a secao NOVA da v408 (antes da v407)\n', 1)
rx(r'^D408 = \["A ordem\.", "O que entra\.", "A condição, lida sob compressão\."[^\n]*\n',
   'DPS407 = ["A ordem.", "O que entra.", "A condição, lida sob compressão.", "O lema das duas faces.", "O par.", "O que o lema e o par NÃO afirmam.", "As sete pedras de 02/11, com os nomes do operador.", "O que fica fora, dito.", "O que o registro confere neste rito."]\n'
   'D408 = ["A ordem.", "O que entra.", "O terminal é a leitura.", "O que o operador identificou e foi provado (regra «provar ou podar»):", "Erratas em nome próprio (E22).", "O tempo é a moeda de $\\\\beta$.", "O ponto de contradição.", "«P = nP».", "O que fica aberto e o que fica dito.", "O que o registro confere neste rito."]\n', 1)
rx(r'^D408E = \["The order\.", "What enters\.", "The condition, read under compression\."[^\n]*\n',
   'DPS407E = ["The order.", "What enters.", "The condition, read under compression.", "The lemma of the two faces.", "The pair.", "What the lemma and the pair do NOT claim.", "The seven stones of 02/11, with the operator\'s names.", "What stays out, stated.", "What the record checks in this rite."]\n'
   'D408E = ["The order.", "What enters.", "The terminal is the reading.", "What the operator identified and was proved (the ``prove or prune\'\' rule):", "Errata in its own name (E22).", "Time is the currency of $\\\\beta$.", "The point of contradiction.", "``P = nP\'\'.", "What stays open and what is stated.", "What the record checks in this rite."]\n', 1)
sub('DEVE = {"pt": [T408] + D408 + [TX407] + DX407 +', 'DEVE = {"pt": [T408] + D408 + [TPS407] + DPS407 + [TX407] + DX407 +')
sub('        "en": [T408E] + D408E + [TX407E] + DX407E +', '        "en": [T408E] + D408E + [TPS407E] + DPS407E + [TX407E] + DX407E +')
sub('TOC = {"pt": [T408, TX407, TW407,', 'TOC = {"pt": [T408, TPS407, TX407, TW407,')
sub('"en": [T408E, TX407E, TW407E,', '"en": [T408E, TPS407E, TX407E, TW407E,')
# a variante sem os registros da v408 (a secao nova mostra a frase de guarda)
sub("cv7 = dict(copy.deepcopy(c)); [cv7.pop(k, None) for k in list(um._V407_REGISTROS_FUNCAO) + list(um._V407_NOMES_REGISTROS)]\n",
    "cv7 = dict(copy.deepcopy(c)); [cv7.pop(k, None) for k in list(um._V407_REGISTROS_FUNCAO) + list(um._V407_NOMES_REGISTROS)]   # (a secao do psion da v407, HERDADA, tambem mostra a frase quando o registro dela falta)\n"
    "cv8v = dict(copy.deepcopy(c)); [cv8v.pop(k, None) for k in list(um._V408_REGISTROS_FUNCAO) + list(um._V408_NOMES_REGISTROS)]   # (v408) a secao NOVA sem os tres registros da v408: a frase de guarda tem de aparecer\n")
sub('    _t7v, _x7v, _r27v, _l7v = compilar(cv7, "dry_v408_var7_%s" % lang, lang, duas=False); fl7 = re.sub(r"\\s+", " ", _x7v)\n',
    '    _t7v, _x7v, _r27v, _l7v = compilar(cv7, "dry_v408_var7_%s" % lang, lang, duas=False); fl7 = re.sub(r"\\s+", " ", _x7v)\n'
    '    _t8v, _x8v, _r28v, _l8v = compilar(cv8v, "dry_v408_var8v_%s" % lang, lang, duas=False); fl8v = re.sub(r"\\s+", " ", _x8v)\n')
sub('"rc_psion_canto_v408": _r27v, "frase_guarda_psion_canto_v408": ("NÃO selaram todos" in fl7) if lang == "pt" else ("did NOT all seal" in fl7)}',
    '"rc_psion_canto_v407": _r27v, "frase_guarda_psion_canto_v407": ("NÃO selaram todos" in fl7) if lang == "pt" else ("did NOT all seal" in fl7),\n'
    '                             "rc_tetelestai_v408": _r28v, "frase_guarda_tetelestai_v408": ("NÃO selaram todos" in fl8v) if lang == "pt" else ("did NOT all seal" in fl8v)}')
rx(r'v\["rc_psion_canto_v408"\] != \[0\] or not v\["frase_guarda_psion_canto_v408"\]', 'v["rc_psion_canto_v407"] != [0] or not v["frase_guarda_psion_canto_v407"] or v["rc_tetelestai_v408"] != [0] or not v["frase_guarda_tetelestai_v408"]', 1)
# o markdown: a linha da v408 antes da v407, que fica antes da v406
sub('"psion_canto_v407": "**O psíon, o canto e o par (v408, 03/11/2026):**" in md and md.find("**O psíon, o canto e o par (v408, 03/11/2026):**") < md.find("**O fechamento (v407, 02/11/2026):**"), "fechamento_v407_fica": "**O fechamento (v407, 02/11/2026):**" in md and md.find("**O fechamento (v407, 02/11/2026):**") < md.find("**A massa derivada e a identidade definida (v405, 01/11/2026):**")',
    '"tetelestai_terminal_v408": "**Tetelestai é o terminal (v408, 04/11/2026):**" in md and md.find("**Tetelestai é o terminal (v408, 04/11/2026):**") < md.find("**O psíon, o canto e o par (v407, 03/11/2026):**"), "psion_canto_v407_fica": "**O psíon, o canto e o par (v407, 03/11/2026):**" in md and md.find("**O psíon, o canto e o par (v407, 03/11/2026):**") < md.find("**O fechamento (v406, 02/11/2026):**"), "fechamento_v406_fica": "**O fechamento (v406, 02/11/2026):**" in md and md.find("**O fechamento (v406, 02/11/2026):**") < md.find("**A massa derivada e a identidade definida (v405, 01/11/2026):**")')
# a simulacao da arvore e o exame dos pontos
sub("_regs_sim = tuple(um._V407_REGISTROS_FUNCAO) + tuple(um._V407_NOMES_REGISTROS) + tuple(um._V406_REGISTROS_FUNCAO)", "_regs_sim = tuple(um._V408_REGISTROS_FUNCAO) + tuple(um._V408_NOMES_REGISTROS) + tuple(um._V407_REGISTROS_FUNCAO) + tuple(um._V407_NOMES_REGISTROS) + tuple(um._V406_REGISTROS_FUNCAO)")
rx(r'"ponto_psibit": _ej\.get\("ponto_psibit"\)', '"ponto_tetelestai": _ej.get("ponto_tetelestai"), "ponto_psibit": _ej.get("ponto_psibit")', 1)
assert "[A ADAPTAR" not in t
ast.parse(t)
open(P, "wb").write(t.encode("utf-8"))
print("ok", N0, "->", len(t))
