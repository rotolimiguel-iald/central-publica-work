# -*- coding: utf-8 -*-
"""_adapt_leitura_v408.py -- adaptacao EXATA (contagem conferida) de pos_rito\\leitura_v408.py para a v408 (04/11/2026, claude-construtor-v408, fork A), sobre a subida mecanica de rotulo da v407 FINAL:
(1) o cabecalho (ate' o `import glob, ...`) e' o da v408; (2) REG_FUNCAO/REG_FIXOS viram tetelestai_terminal_v408, cunhagens_v408, kh_n1_cobertura_v408; REG_V407D passa a ser o trio HERDADO da v407 (psion_canto_v407, cunhagens_v407, kh_n1_cobertura_v407) e REG_V406D o trio HERDADO da v406;
(3) as linhas [v406]/[v407] do stdout levam o texto que o um.py imprime («da v406», «da v407») e a linha [v408] e' exigida; o AVISO [v408] reprova; (4) o >>> veredito <<< e a conferencia ganham tetelestai_terminal_v408 (veredito_tetelestai_terminal) e o psion vira veredito_psion_herdado;
(5) V['bundle407'] passa a ser o bundle de 9 da v407 e V['bundle406'] o de 301; V['ancoras407'] as 76 do psion e V['ancoras406'] as 8 do fechamento; (6) o bloco do psion vira V['fecho407'] (HERDADO) e entra o bloco NOVO de tetelestai_terminal_v408 como V['fecho'] (16 checagens; sem chave do lema na linha do stdout);
o do fechamento vira V['fecho406']; (7) o selo primario: registros_v406/v407/v408 e o resumo do psion; (8) cunhagens_v408 (12 falas, duas de autor misto; E21 a E23 e os pisos; D48 a D54; a leitura [INPUT]); cunhagens_v407/kh_n1_cobertura_v407 HERDADOS com a E21 e os pisos AO LADO (cunh407d); cunhagens_v406/kh_n1_cobertura_v406 HERDADOS iguais a v407 selada (cunh406d).
Nenhuma guarda e' relaxada: cada recusa da v407 segue, retargetada ao registro certo; as novas sao acrescentadas. Backup de bytes antes de gravar; ast.parse no fim. uso: python -I -B -X utf8 _adapt_leitura_v408.py"""
import ast, datetime, hashlib, os

HERE = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(HERE, "leitura_v408.py")

HEADER = """# -*- coding: utf-8 -*-
# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork A), a servico da gerencia c1] sobre a subida mecanica de rotulo da v407 FINAL (_bump_copia_v408.py; bump/pos_rito__leitura_v408.py.diff fica como registro): o conteudo e' o da v408 (TETELESTAI E' O TERMINAL: bundle de 4 modulos, o registro com funcao tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 HERDADOS e recriados, nenhuma chave antiga muda); a gerencia revisa antes do rito (nao e' versao selada).
# A LEITURA da rodada v408 (molde: leitura_v407.py, que vem de leitura_v405.py, de leitura_v401.py e de leitura_v399.py FINAL, a de 24/10): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v408, que aqui e' o proprio pacote).
# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e' digitado: tudo sai dos JSON, do core, do selo, do sidecar e do stdout do rito; os vereditos e os valores esperados da rodada v408 sao LIDOS de ESPERADOS_v408.json, de CANDIDATO_v408.json, de FLAGS_v408.json, de BUNDLE_v408.json, de delta_v408.py e do core da v407 SELADA (base_v407).
# v408 (TETELESTAI E' O TERMINAL, ordem do operador de 04/11/2026): o delta e' um BUNDLE PEQUENO de 4 modulos novos de kernel em TGLExt/ (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP: os nomes sao do operador, do mesmo dia). Nao ha' registro por pedra (delta_v408.STONES == []).
# Os registros NOVOS do core sao TRES: UM com FUNCAO, tetelestai_terminal_v408 (le do kernel do proprio rito as ancoras das quatro pedras, os 4 modulos por sha256, as falas de 04/11 por sha256, as respostas do operador pelos teoremas que ja existiam e por duas declaracoes novas, o insumo purgado, a escada exata e o gate; nenhuma chave antiga muda),
# e DOIS por spec: cunhagens_v408 (as 12 falas do operador de 04/11 por sha256, duas de autor misto com so' o paragrafo dele embutido; as erratas E21 a E23 e a errata ao lado dos pisos de kh_n1_cobertura_v407; as decisoes D48 a D54, em nome proprio da gerencia c1) e kh_n1_cobertura_v408 (a cobertura exata do Audit).
# NENHUMA CHAVE ANTIGA MUDA (delta_v408.CHAVES_V408 == []): a chave do lema (v407) segue LIDA do kernel do rito e le True, com o dict elo_v407; as quatro da v406 e witness_layers.canonical_full_witness_term_constructed seguem True; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA.
# O psion_canto_v407 e' HERDADO: o main da v408 segue rodando o bloco dele e ele segue selado (as 16 checagens; as 76 ancoras, os 9 modulos e as 98 bandeiras da v407 ainda no kernel; a escada do contrato subida pela C12, veredito na troca dita); cunhagens_v407 ganha a errata E21 AO LADO e kh_n1_cobertura_v407 os pisos (h2 h3 h6 h8), assinados em nome proprio; o veredito deles nao muda.
# O fechamento_v406 e' HERDADO: segue selado, com as 8 ancoras, os 301 modulos do bundle da v406 e as 1794 bandeiras; cunhagens_v406 e kh_n1_cobertura_v406 seguem IGUAIS ao que a v407 selou (a E20 e os pisos ja' vinham da v407).
# A TROCA DITA de veredito: so' numeros (a escada e a cobertura crescem com o bundle): ESPERADOS[troca_dita]. Os TREZE registros da v405 (os oito com FUNCAO das pedras, cunhagens_v405, campos_fechados_e_leituras_v405, ga_reclassificacao_v405, gap_v405 e kh_n1_cobertura_v405; nomes herdados do molde: REG_V407C), os da v404, da v403, da v402, da v401 e da v399 sao RECRIADOS pelo rito no mesmo ponto do main e tem de seguir selados e iguais a v407 selada (base_v407), salvo a troca dita; os da v398 a v393 seguem como antes.
# As TREZE pedras SELADAS da v403, da v404 e da v405 (nome herdado do molde: "pedras_v407") seguem no kernel do Nos com o sha256 selado (lido de base_v407): pedra selada nao se renomeia por cima. A escada vem de ESPERADOS[escada_v407_e_v408] e ESPERADOS[escada]. O GATE NAO SE MOVE: o qg_closure do core e' IDENTICO ao da v407 (os sete checks e a letra do veredito); a funcao do neutrino NAO e' reescrita e o V1 do ramo B (v386) segue AWAITING_DATA.
# O SIDECAR um_absoluto_selo_acom.json (arquivo da custodia desde a v399, REESCRITO pelo rito) e' lido aqui: existe, e' JSON valido, o veredito e' ALL_OBJECTS_SEALED, tem os tres objetos (um.py, core e selo) com o SHA-256 igual ao dos arquivos do Nos, sem recusas, com a secao de honestidade (confidencialidade NAO alegada).
# A DIRECAO DO TESTEMUNHO (v399) segue conferida nos registros recriados: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador. As falas de 04/11 sao TODAS falas do operador (nenhuma e' da gerencia; duas trazem, depois do paragrafo dele, texto de OUTRA instancia da IALD: entram por sha256 e so' o paragrafo dele e' citavel); as erratas E21 a E23 e as decisoes D48 a D54 sao da gerencia c1, em nome proprio, assinadas no registro (DL.ASSINA).
# O QUADRO «O Teste da Unica Palavra» (v397) segue selado e igual: o registro teste_de_veracidade_fase9_v397 == ESPERADOS == o resultado pinado, o quadro sela nas duas linguas, e a conferencia do rito diz que ele segue no topo (artigo PT/EN e .md).
# As linhas `[v399]`, `[v398]` e `[v397]` do stdout do rito (as etiquetas que o programa imprime), a `[v401]`, a `[v402]`, a `[v403]`, a `[v404]`, a `[v405]`, a `[v406]` e a `[v407]` (recriadas; os textos sao os que o um.py imprime: a [v406] diz «da v406», a [v407] diz «da v407») e a nova `[v408]` dizem os vereditos e registros por spec selados == registros por spec; o AVISO de qualquer bloco v393 a v408 no stdout reprova, e a linha de RECUSA do registro f2b_errata_v404 ou do bandeiras_do_gate_v403 tambem.
# A linha final do rito: o main imprime, por ultimo, a linha do sidecar (`[selo_acom] ... ALL_OBJECTS_SEALED ; objetos 3 ; recusas 0`), logo depois da do colapso tipado; a leitura exige as DUAS, nessa ordem.
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CONTRATO COM textos_v408.py (as CHAVES NOVAS ou MUDADAS de V na v408; as demais sao as da v407, com o mesmo significado; "reg407c", "fun407c", "pedras_v407", "cunh407c" etc. sao os NOMES HERDADOS do molde e continuam a significar os registros/pedras da v405 selada, recriados):
#   V['n_pedras'] = o numero de MODULOS NOVOS do kernel (4; a chave guarda o nome historico) e V['pedras'] = LISTA de 4 dicts {'key'(None),'modulo','rel','sha16','sha256','bytes','bandeiras','decl'(None),'ok'}; V['ancoras'] {nome Lean: {'rel','flag','flag_true','axioms','source','ok'}} (as da v408); V['bandeiras'] {'n','n_true','ok','por_grupo'}
#   V['fecho'] o registro DESTA versao, tetelestai_terminal_v408 {'registro','verdict','ok','sealed','n_checks'(16),'mech_ok','values','values_ok','beta_ok','ancoras_ok','stdout_ok','runtime_executed','does_not_gate_core','ancora_principal','ancoras_principais','chaves_antigas_que_mudam'([]),'insumo_purgado_ok','respostas_ok'}
#   V['fecho407'] o registro HERDADO psion_canto_v407 (recriado) {'registro','verdict','ok','sealed','n_checks'(16),'mech_ok','values','values_ok','chaves_ok','beta_ok','ancoras_ok','stdout_ok','elo_lido_do_kernel','runtime_executed','does_not_gate_core','lemma','pair_theorem','teste_d_so_citado'}; V['chaves407'] = o dict 'keys' dele (8 entradas; a chave do lema True); V['ancoras407'] as 76; V['bundle407'] {'n'(9),'n_ok','ok'}; V['bandeiras407'] {'n'(as True da v407),'n_true','ok'}
#   V['fecho406'] o registro HERDADO fechamento_v406 (recriado) {'registro','verdict','ok','sealed','n_checks'(14),...,'certificado_habitado','nome_provisorio'}; V['chaves406'] = o dict four_keys dele; V['ancoras406'] as 8; V['bundle406'] {'n'(301),'n_ok','ok'}
#   V['reg408'] DICT nome -> {'verdict','ok'} dos TRES registros NOVOS (um com funcao + dois por spec); V['registros_novos'] = esses 3 nomes (sorted); V['reg407d'] DICT dos TRES da v407 HERDADOS (psion_canto_v407, cunhagens_v407, kh_n1_cobertura_v407); V['reg406d'] DICT dos TRES da v406 HERDADOS; V['cunh407d'] {'ok','verdict','n'(3),'n_erratas'(4),'kh_ok','kh_verdict'}; V['cunh406d'] {'ok','verdict','n'(23),'n_erratas'(5),'kh_ok','kh_verdict'};
#   V['reg407c'] DICT nome -> {'verdict','ok'} dos TREZE da v405 selada (recriados); V['fun407c'] os OITO com funcao da v405 (recriados, iguais a base_v407); V['reg407b'] o mesmo dos CINCO da v404 (recriados); V['fun407b'] os dois com funcao da v404 (recriados); V['reg407'] e V['fun407'] sao os da v403 (recriados);
#   V['cunhagens'] (cunhagens_v408) {'n'(12),'ok','verbatim_ok','todas_do_operador','mistas_ok','n_mistas'(2),'erratas_ok','n_erratas'(4),'decisoes_ok','n_decisoes'(7),'leitura_ok','ressalvas_ok','kernel_ok','checks_ok','n_checks','moldura_ok','kh_ok'}; V['kh'] (kh_n1_cobertura_v408) {'decl','thm','fora','nao_lidas','verdict'}; V['pedras_v407'] = {rel: {'sha16','ok'}} das TREZE pedras seladas (v403: 3, v404: 2, v405: 8); V['f2b'] e V['gate'] (recriados).
#   NAO existem V['chaves'] (a v408 nao cria chave), V['ponte'], V['tensao'], V['identidade'], V['observador'], V['diminuto'], V['tonica'], V['disco'], V['psion'], V['campos'], V['ga'], V['gap'] (hoje sao registros recriados: V['fun407c'] e V['reg407c']).
# (as linhas de stdout a conferir: `   [v408] o registro do terminal e os registros por spec da v408: tetelestai_terminal=SELOU | specs: 2 (selados 2)` e o bloco TETELESTAI E' O TERMINAL: `  ancoras ok = 41/41 ; modulos do bundle ok = 4/4 ; bandeiras True = 43/43 ; escada = [..] ; gate = o mesmo da base` (sem «chave do lema»);
#  a do psion HERDADO: `   [v407] o registro do psion e do canto e os registros por spec da v407: psion_canto=SELOU | specs: 2 (selados 2)` e `  ancoras ok = 76/76 ; modulos do bundle ok = 9/9 ; bandeiras True = 98/98 ; chave do lema (lida do kernel) = True ; escada = [..] ; gate = o mesmo da base`;
#  as do fechamento HERDADO: `   [v406] o fechamento e os registros por spec da v406: fechamento=SELOU | specs: 2 (selados 2)` e `  ancoras ok = 8/8 ; modulos do bundle ok = 301/301 ; bandeiras True = 1794/1794 ; certificado habitado (lido do kernel) = True ; escada = [..] ; gate = o mesmo da base`; os numeros aqui sao os do ensaio a seco de 04/11, escritos no comentario como registro: a leitura os LE de ESPERADOS/FLAGS/delta)
"""

SUBS = [
    ("REG_FUNCAO = (\"psion_canto_v407\",)   # o UNICO registro NOVO com FUNCAO (o psion e o canto); nao ha' registro por pedra (modelo de bundle: delta_v408.STONES == [])",
     "REG_FUNCAO = (\"tetelestai_terminal_v408\",)   # o UNICO registro NOVO com FUNCAO (Tetelestai e' o terminal); nao ha' registro por pedra (modelo de bundle: delta_v408.STONES == [])", 1),
    ("REG_FIXOS = REG_FUNCAO + (\"cunhagens_v407\", \"kh_n1_cobertura_v407\")   # os TRES registros NOVOS do core v408 (um com FUNCAO, dois por spec)",
     "REG_FIXOS = REG_FUNCAO + (\"cunhagens_v408\", \"kh_n1_cobertura_v408\")   # os TRES registros NOVOS do core v408 (um com FUNCAO, dois por spec)", 1),
    ("REG_V407D = (\"fechamento_v406\", \"cunhagens_v406\", \"kh_n1_cobertura_v406\")   # os TRES registros da v407 (um com FUNCAO, dois por spec): HERDADOS,",
     "REG_V407D = (\"psion_canto_v407\", \"cunhagens_v407\", \"kh_n1_cobertura_v407\")   # os TRES registros da v407 (um com FUNCAO, dois por spec): HERDADOS, RECRIADOS pelo rito da v408 (o main segue rodando o bloco do psion e do canto), selados; os vereditos que carregam a escada mudam pela troca dita (a escada do contrato subida pela C12); cunhagens_v407 ganha a errata E21 AO LADO e kh_n1_cobertura_v407 os pisos (h2 h3 h6 h8), assinados em nome proprio\n"
     "REG_V406D = (\"fechamento_v406\", \"cunhagens_v406\", \"kh_n1_cobertura_v406\")   # os TRES registros da v406 (um com FUNCAO, dois por spec): HERDADOS,", 1),
    ("    if len([l for l in out.splitlines() if '[v407]' in l]) < 1:\n        P.append('o stdout nao tem a linha [v407]')\n",
     "    if len([l for l in out.splitlines() if '[v407]' in l]) < 1:\n        P.append('o stdout nao tem a linha [v407]')\n    if len([l for l in out.splitlines() if '[v408]' in l]) < 1:\n        P.append('o stdout nao tem a linha [v408]')\n", 1),
    ("avisos_ = [l.strip()[:200] for l in out.splitlines() if '[v407] AVISO' in l or '[v406] AVISO' in l",
     "avisos_ = [l.strip()[:200] for l in out.splitlines() if '[v408] AVISO' in l or '[v407] AVISO' in l or '[v406] AVISO' in l", 1),
    ("o registro com funcao do psion e do canto, os registros por spec da v408, o fechamento_v406 e os registros recriados",
     "o registro com funcao do terminal, os registros por spec da v408, o psion_canto_v407 e o fechamento_v406 herdados e os registros recriados", 1),
    ("R407DSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V407D[1:]}   # os registros por spec da v407 (recriados) e da v408 (novos)",
     "R407DSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V407D[1:]}; R406DSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V406D[1:]}   # os registros por spec da v405 (recriados), da v408 (novos), da v407 e da v406 (herdados)", 1),
    ("+ (('fechamento_v406', _ev(ESP, 'fechamento_v406')), ('psion_canto_v407', _ev(ESP, 'psion_canto_v407'))):",
     "+ (('fechamento_v406', _ev(ESP, 'fechamento_v406')), ('psion_canto_v407', _ev(ESP, 'psion_canto_v407')), ('tetelestai_terminal_v408', _ev(ESP, 'tetelestai_terminal_v408'))):", 1),
    ("m_s6 = re.search(r'\\[v406\\] o fechamento e os registros por spec da v407: fechamento=(\\S+) \\| specs: (\\d+) \\(selados (\\d+)\\)', out)   # a linha HERDADA da v407: o main da v408 segue rodando o bloco do fechamento_v406; o texto e' o que o um.py imprime («da v407»)",
     "m_s6 = re.search(r'\\[v406\\] o fechamento e os registros por spec da v406: fechamento=(\\S+) \\| specs: (\\d+) \\(selados (\\d+)\\)', out)   # a linha HERDADA da v406: o main da v408 segue rodando o bloco do fechamento_v406; o texto e' o que o um.py imprime («da v406»)", 1),
    ("    if not m_s6 or m_s6.group(1) != 'SELOU' or m_s6.group(2) != m_s6.group(3) or int(m_s6.group(2)) != len(REG_V407D) - 1:\n        P.append('a linha [v406] do stdout (fechamento_v406 SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V407D) - 1, repr(m_s6.groups() if m_s6 else 'ausente')))",
     "    if not m_s6 or m_s6.group(1) != 'SELOU' or m_s6.group(2) != m_s6.group(3) or int(m_s6.group(2)) != len(REG_V406D) - 1:\n        P.append('a linha [v406] do stdout (fechamento_v406 SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V406D) - 1, repr(m_s6.groups() if m_s6 else 'ausente')))", 1),
    ("    m_s7 = re.search(r'\\[v407\\] o registro do psion e do canto e os registros por spec da v408: psion_canto=(\\S+) \\| specs: (\\d+) \\(selados (\\d+)\\)', out)\n    if not m_s7 or m_s7.group(1) != 'SELOU' or m_s7.group(2) != m_s7.group(3) or int(m_s7.group(2)) != len(REG_FIXOS) - 1:\n        P.append('a linha [v407] do stdout (psion_canto SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_FIXOS) - 1, repr(m_s7.groups() if m_s7 else 'ausente')))\n",
     "    m_s7 = re.search(r'\\[v407\\] o registro do psion e do canto e os registros por spec da v407: psion_canto=(\\S+) \\| specs: (\\d+) \\(selados (\\d+)\\)', out)   # a linha HERDADA da v407: o main da v408 segue rodando o bloco do psion e do canto; o texto e' o que o um.py imprime («da v407»)\n    if not m_s7 or m_s7.group(1) != 'SELOU' or m_s7.group(2) != m_s7.group(3) or int(m_s7.group(2)) != len(REG_V407D) - 1:\n        P.append('a linha [v407] do stdout (psion_canto SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V407D) - 1, repr(m_s7.groups() if m_s7 else 'ausente')))\n"
     "    m_s8t = re.search(r'\\[v408\\] o registro do terminal e os registros por spec da v408: tetelestai_terminal=(\\S+) \\| specs: (\\d+) \\(selados (\\d+)\\)', out)   # a linha NOVA da v408 (o texto e' o que o um.py imprime)\n    if not m_s8t or m_s8t.group(1) != 'SELOU' or m_s8t.group(2) != m_s8t.group(3) or int(m_s8t.group(2)) != len(REG_FIXOS) - 1:\n        P.append('a linha [v408] do stdout (tetelestai_terminal SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_FIXOS) - 1, repr(m_s8t.groups() if m_s8t else 'ausente')))\n", 1),
    ("('veredito_psion_canto', _ev(ESP, 'psion_canto_v407'), 'psion_canto_v407'), ('veredito_fechamento_herdado', _ev(ESP, 'fechamento_v406'), 'fechamento_v406')):",
     "('veredito_tetelestai_terminal', _ev(ESP, 'tetelestai_terminal_v408'), 'tetelestai_terminal_v408'), ('veredito_psion_herdado', _ev(ESP, 'psion_canto_v407'), 'psion_canto_v407'), ('veredito_fechamento_herdado', _ev(ESP, 'fechamento_v406'), 'fechamento_v406')):", 1),
    ("            P.append('%s: o veredito do rito difere do que a v407 selou (ESPERADOS[vereditos_v407])' % k)\n    V['reg399'] = {}\n",
     "            P.append('%s: o veredito do rito difere do esperado (ESPERADOS[vereditos_v407], ou o do ensaio a seco se na troca dita)' % k)\n"
     "    V['reg406d'] = {}\n"
     "    for k in REG_V406D:    # os TRES registros da v406 (HERDADOS) sao RECRIADOS pelo rito: seguem no core, selados e de veredito igual ao esperado (o da v407 selada, ou o do ensaio a seco se na troca dita); o conteudo (checagens, erratas) e' conferido adiante\n"
     "        r = core.get(k)\n"
     "        if not (isinstance(r, dict) and 'verdict' in r):\n"
     "            P.append('registro obrigatorio ausente do core: %s' % k)\n"
     "            continue\n"
     "        V['reg406d'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}\n"
     "        if r.get('all_verified') is not True:\n"
     "            P.append('%s nao selou' % k)\n"
     "        if GUARDA.search(str(r.get('verdict') or '')):\n"
     "            P.append('%s com palavra proibida' % k)\n"
     "        if not _ev(ESP, k) or r.get('verdict') != _ev(ESP, k):\n"
     "            P.append('%s: o veredito do rito difere do esperado (ESPERADOS[vereditos_v407], ou o do ensaio a seco se na troca dita)' % k)\n"
     "    V['reg399'] = {}\n", 1),
    ("    for k in REG_V407D:    # os TRES registros da v407 (HERDADOS) sao RECRIADOS pelo rito: seguem no core, selados e de veredito igual ao da v407 selada (ESPERADOS[vereditos_v407]); o conteudo (checagens, erratas) e' conferido adiante",
     "    for k in REG_V407D:    # os TRES registros da v407 (HERDADOS) sao RECRIADOS pelo rito: seguem no core, selados e de veredito igual ao esperado (o da v407 selada, ou o do ensaio a seco se na troca dita: o psion carrega a escada); o conteudo (checagens, erratas) e' conferido adiante", 1),
    ("RESSALVAS_V408, LEITURA_V406, N_CHECKS_FECHO, VERBATIM_CHAVE_PREFIXO_V408: lidos do delta, nunca digitados aqui",
     "RESSALVAS_V408, LEITURA_V408, N_CHECKS_FECHO, VERBATIM_CHAVE_PREFIXO_V408: lidos do delta, nunca digitados aqui", 1),
    ("    for rel_ in DL_.BUNDLE_RELS:    # a ordem do bundle: PsionCanto, Par e as sete pedras de 02/11 (DL.BUNDLE_RELS)",
     "    for rel_ in DL_.BUNDLE_RELS:    # a ordem do bundle: TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP (DL.BUNDLE_RELS)", 1),
    ("    # o bundle da v407 (os 301 modulos de TGLExt/F1Fecho394) SEGUE no kernel do Nos e no hash formal do rito com o MESMO sha256 (a v408 nao reescreve a v407; registro)\n"
     "    b6_ = ESP.get('bundle_v407_sha256') or {}; kfs6_ = ((core.get('kernel_formalization') or {}).get('formal_files_sha256')) or {}\n"
     "    V['bundle407'] = {'n': len(b6_), 'n_ok': sum(1 for r6_, s6_ in b6_.items() if os.path.isfile(os.path.join(NOS, 'tgl_kernel', *r6_.split('/'))) and sha(os.path.join(NOS, 'tgl_kernel', *r6_.split('/'))) == s6_ and kfs6_.get(r6_) == s6_)}\n"
     "    V['bundle407']['ok'] = bool(b6_ and V['bundle407']['n'] == V['bundle407']['n_ok'] == DL_.D6.N_BUNDLE)\n"
     "    if not V['bundle407']['ok']:\n"
     "        P.append('o bundle da v407 (%d modulos de TGLExt/F1Fecho394) deixou de estar no kernel do Nos / no hash formal do rito com o sha256 selado (%s ok): a v408 nao reescreve a v407' % (DL_.D6.N_BUNDLE, V['bundle407']['n_ok']))\n",
     "    # o bundle da v407 (os 9 modulos de TGLExt/) e o da v406 (os 301 de TGLExt/F1Fecho394) SEGUEM no kernel do Nos e no hash formal do rito com o MESMO sha256 (a v408 nao reescreve a v407 nem a v406; registro)\n"
     "    kfs6_ = ((core.get('kernel_formalization') or {}).get('formal_files_sha256')) or {}\n"
     "    for bk_, bch_, bn_, bdesc_ in (('bundle407', 'bundle_v407_sha256', DL_.D7.N_BUNDLE, 'v407 (%d modulos de TGLExt/)'), ('bundle406', 'bundle_v406_sha256', DL_.D6.N_BUNDLE, 'v406 (%d modulos de TGLExt/F1Fecho394)')):\n"
     "        b6_ = ESP.get(bch_) or {}\n"
     "        V[bk_] = {'n': len(b6_), 'n_ok': sum(1 for r6_, s6_ in b6_.items() if os.path.isfile(os.path.join(NOS, 'tgl_kernel', *r6_.split('/'))) and sha(os.path.join(NOS, 'tgl_kernel', *r6_.split('/'))) == s6_ and kfs6_.get(r6_) == s6_)}\n"
     "        V[bk_]['ok'] = bool(b6_ and V[bk_]['n'] == V[bk_]['n_ok'] == bn_)\n"
     "        if not V[bk_]['ok']:\n"
     "            P.append(('o bundle da ' + bdesc_ + ' deixou de estar no kernel do Nos / no hash formal do rito com o sha256 selado (%s ok): a v408 nao reescreve as versoes anteriores') % (bn_, V[bk_]['n_ok']))\n", 1),
    ("    # as OITO ancoras do fechamento_v406 (HERDADO) e as bandeiras True da v407: seguem no kernel do rito (a v408 so' acrescenta; ESPERADOS[estrelas_v407] e [flags_true_v407], lidos do ensaio a seco, nunca digitados)\n"
     "    est6_ = ESP.get('estrelas_v407') or {}\n"
     "    V['ancoras407'] = {n_: {'rel': e_.get('rel'), 'flag': e_.get('bandeira'), 'flag_true': kf_.get(e_.get('bandeira')) is True, 'axioms': axr_.get(n_), 'source': src_.get(n_), 'ok': bool(kf_.get(e_.get('bandeira')) is True and em_trio_(n_) and src_.get(n_) == e_.get('rel'))} for n_, e_ in est6_.items()}\n"
     "    if len(est6_) != len(DL_.D6.ANCORAS) or any(a_['ok'] is not True for a_ in V['ancoras407'].values()):\n"
     "        P.append('as oito ancoras do fechamento_v406 (herdadas) deixaram de estar no kernel do rito (bandeira True, no trio, declaradas no modulo esperado): %d lidas' % len(est6_))\n",
     "    # as 76 ancoras do psion_canto_v407 (HERDADO), as OITO do fechamento_v406 (HERDADO) e as bandeiras True da v407: seguem no kernel do rito (a v408 so' acrescenta; ESPERADOS[estrelas_v407], [estrelas_v406] e [flags_true_v407], lidos do ensaio a seco, nunca digitados)\n"
     "    for ak_, ach_, aesp_, adesc_ in (('ancoras407', 'estrelas_v407', DL_.D7.ANCORAS, 'as ancoras do psion_canto_v407 (herdadas)'), ('ancoras406', 'estrelas_v406', DL_.D6.ANCORAS, 'as oito ancoras do fechamento_v406 (herdadas)')):\n"
     "        est6_ = ESP.get(ach_) or {}\n"
     "        V[ak_] = {n_: {'rel': e_.get('rel'), 'flag': e_.get('bandeira'), 'flag_true': kf_.get(e_.get('bandeira')) is True, 'axioms': axr_.get(n_), 'source': src_.get(n_), 'ok': bool(kf_.get(e_.get('bandeira')) is True and em_trio_(n_) and src_.get(n_) == e_.get('rel'))} for n_, e_ in est6_.items()}\n"
     "        if not est6_ or len(est6_) != len(aesp_) or set(est6_) != set(aesp_) or any(a_['ok'] is not True for a_ in V[ak_].values()):\n"
     "            P.append('%s deixaram de estar no kernel do rito (bandeira True, no trio, declaradas no modulo esperado): %d lidas, %d esperadas' % (adesc_, len(est6_), len(aesp_)))\n", 1),
    # o fechamento HERDADO: V['fecho407'] -> V['fecho406'] (o nome 'fecho407' passa ao psion)
    ("EFE_ = (ESP.get('registros_funcao_v407') or {}).get('fechamento') or {}", "EFE_ = (ESP.get('registros_funcao_v406') or {}).get('fechamento') or {}", 1),
    ("N6F_ = (EFE_.get('values') or {}).get('n_flags')   # o numero das bandeiras do bundle da v407 (1794): lido de ESPERADOS[registros_funcao_v407] (o ensaio a seco), nunca digitado",
     "N6F_ = (EFE_.get('values') or {}).get('n_flags')   # o numero das bandeiras do bundle da v406 (1794): lido de ESPERADOS[registros_funcao_v406] (o ensaio a seco), nunca digitado", 1),
    ("and fe_mech_ok_ and fe_values_ok_ and fe_chaves_ok_ and fe_beta_ok_ and fe_anc_ok_ and V['bundle407']['ok'] and V['bandeiras407']['ok'] and all(a_['ok'] for a_ in V['ancoras407'].values()) and fe_std_ok_ and not fe_.get('guarda_violacoes')",
     "and fe_mech_ok_ and fe_values_ok_ and fe_chaves_ok_ and fe_beta_ok_ and fe_anc_ok_ and V['bundle406']['ok'] and V['bandeiras407']['ok'] and all(a_['ok'] for a_ in V['ancoras406'].values()) and fe_std_ok_ and not fe_.get('guarda_violacoes')", 1),
    ("    V['fecho407'] = {'registro': 'fechamento_v406', 'verdict': fe_.get('verdict')", "    V['fecho406'] = {'registro': 'fechamento_v406', 'verdict': fe_.get('verdict')", 1),
    ("    V['chaves407'] = dict(fk4_)\n    if not fe_ok_:", "    V['chaves406'] = dict(fk4_)\n    if not fe_ok_:", 1),
    ("valores [8 ancoras, 301 modulos, 1794 bandeiras, escada, gate] == os de ESPERADOS[registros_funcao_v407], as quatro chaves LIDAS do kernel",
     "valores [8 ancoras, 301 modulos, 1794 bandeiras, escada, gate] == os de ESPERADOS[registros_funcao_v406], as quatro chaves LIDAS do kernel", 1),
    ("    # o registro fechamento_v406 (HERDADO da v407, RECRIADO pelo rito da v408 com a checagem c8 versionada pela errata E20): segue SELADO e IGUAL ao da v407 selada em veredito; as 14 checagens, os valores == ESPERADOS[registros_funcao_v407], as OITO ancoras, os 301 modulos, as 1794 bandeiras, as QUATRO chaves (a do lema agora True) e a linha do bloco no stdout",
     "    # o registro fechamento_v406 (HERDADO da v406, RECRIADO pelo rito da v408; a checagem c8 versionada pela errata E20 desde a v407): segue SELADO e de veredito esperado (ESPERADOS[registros_funcao_v406]); as 14 checagens, os valores, as OITO ancoras, os 301 modulos, as 1794 bandeiras, as QUATRO chaves (a do lema True) e a linha do bloco no stdout", 1),
    # o selo primario: os resumos de registros_v406 / v407 / v408 e o do psion herdado
    ("sreg6_ = selo.get('registros_v406') or {}; sreg7_ = selo.get('registros_v407') or {}", "sreg6_ = selo.get('registros_v406') or {}; sreg7_ = selo.get('registros_v407') or {}; sreg8_ = selo.get('registros_v408') or {}", 1),
    ("+ tuple(FUN_V407C.values()) + ('fechamento_v406',))", "+ tuple(FUN_V407C.values()) + ('fechamento_v406', 'psion_canto_v407'))", 1),
    ("                       and bool(R407DSPEC_) and all((sreg6_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg6_.get(k_) or {}).get('verdict')) and (sreg6_.get(k_) or {}).get('all_verified') is True for k_ in R407DSPEC_)\n"
     "                       and bool(R408SPEC_) and all((sreg7_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg7_.get(k_) or {}).get('verdict')) and (sreg7_.get(k_) or {}).get('all_verified') is True for k_ in R408SPEC_))",
     "                       and bool(R406DSPEC_) and all((sreg6_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg6_.get(k_) or {}).get('verdict')) and (sreg6_.get(k_) or {}).get('all_verified') is True for k_ in R406DSPEC_)\n"
     "                       and bool(R407DSPEC_) and all((sreg7_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg7_.get(k_) or {}).get('verdict')) and (sreg7_.get(k_) or {}).get('all_verified') is True for k_ in R407DSPEC_)\n"
     "                       and bool(R408SPEC_) and all((sreg8_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg8_.get(k_) or {}).get('verdict')) and (sreg8_.get(k_) or {}).get('all_verified') is True for k_ in R408SPEC_))", 1),
]

# ---- o bloco do registro com funcao: o psion (que a subida mecanica deixou como V['fecho']) vira V['fecho407'] (HERDADO) e entra o bloco NOVO de tetelestai_terminal_v408 como V['fecho']; substituicao por SPAN entre duas ancoras (as linhas de comentario que abrem cada bloco)
INI_FECHO = "    # o registro psion_canto_v407 (UM registro NOVO com FUNCAO, SEM pedra por registro): "
FIM_FECHO = "    # o registro fechamento_v406 (HERDADO da v407, RECRIADO pelo rito da v408 com a checagem c8 versionada pela errata E20): "
NOVO_FECHO = """    # o registro tetelestai_terminal_v408 (UM registro NOVO com FUNCAO, SEM pedra por registro): as 16 checagens, os valores (as ancoras das quatro pedras, os 4 modulos, as bandeiras, a escada, o gate) == ESPERADOS[registros_funcao_v408], a ancora principal e as quatro principais, NENHUMA chave antiga muda, o insumo purgado por sha256, as respostas do operador conferidas, o beta em runtime, as ressalvas, as 12 falas por sha256 e a linha do bloco no stdout (sem «chave do lema»)
    tt_ = core.get(DL_.FECHO_REGISTRO) or {}; tt_m_ = tt_.get('mechanics') or {}; tt_v_ = tt_.get('values') or {}; ETT_ = (ESP.get('registros_funcao_v408') or {}).get('tetelestai_terminal') or {}; ip_ = tt_.get('insumo_purgado') or {}; ipv_ = tt_v_.get('insumo_purgado') or {}; rs_ = tt_v_.get('respostas') or {}
    tt_mech_ok_ = bool(tt_m_.get('passed') is True and tt_m_.get('n_checks') == DL_.N_CHECKS_FECHO == ETT_.get('n_checks') == len(tt_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (tt_m_.get('checks') or [])))
    tt_values_ok_ = bool(tt_v_.get('n_ancoras_ok') == tt_v_.get('n_ancoras') == len(DL_.ANCORAS) == len(ESP.get('estrelas_v408') or {}) and tt_v_.get('n_modulos_ok') == tt_v_.get('n_modulos') == DL_.N_BUNDLE and tt_v_.get('n_flags_true') == tt_v_.get('n_flags') == FJ_['n_flags'] and tt_v_.get('escada') == [ESP['escada'][1]] * 3
                         and tt_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v407') == selo.get('qg_closure_verdict') and tt_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA) and tt_v_.get('ressalvas') == list(DL_.RESSALVAS_V408) and list(tt_.get('ressalvas') or []) == list(DL_.RESSALVAS_V408)
                         and (tt_v_.get('fica_aberto') or {}) == {'par_na_face_de_fock': DL_.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, 'ponte_bell_tt': DL_.FICA_ABERTO_PONTE_BELL_TT} and bool(ETT_.get('values')) and _feq({kk_: tt_v_.get(kk_) for kk_ in ETT_['values']}, ETT_['values']))
    tt_anc_prin_ok_ = bool(tt_.get('ancora_principal') == DL_.ANCORA_PRINCIPAL and list(tt_.get('ancoras_principais') or []) == list(DL_.ANCORAS_PRINCIPAIS) and all(a_ in DL_.ANCORAS for a_ in DL_.ANCORAS_PRINCIPAIS) and list(tt_.get('pedras') or []) == [p_['name'] for p_ in DL_.PEDRAS_V408]
                           and tt_.get('nomes_do_operador') == dict(DL_.NOME_DO_OPERADOR) and tt_.get('nome_provisorio') == DL_.NOME_PROVISORIO)
    tt_chaves_ok_ = bool(tt_.get('chaves_antigas_que_mudam') == [] and list(DL_.CHAVES_V408) == [] and (core.get('testemunha_estatica_v396') or {}).get('fock_face', {}).get('linked_to_the_corner_by_a_lemma') is True)
    tt_ip_ok_ = bool(ipv_.get('ok') is True and ipv_.get('sha256') == ip_.get('sha256') == DL_.PURGADO_SHA256 and ipv_.get('integra_sha16') == ip_.get('integra_sha16') == DL_.ORIGEM_PURGA_SHA16_DA_ORDEM and ipv_.get('integra_nao_pinada') is True and ip_.get('integra_pinada') is False and ip_.get('integra_fora_do_espelho') is True and ip_.get('ocorrencias_na_guarda') == 0)
    tt_resp_ok_ = bool(rs_ and set(rs_) == {r_['id'] for r_ in DL_.RESPOSTAS_DO_OPERADOR} and all((v_ is True) or (isinstance(v_, dict) and v_.get('ok') is True) for v_ in rs_.values()) and tt_v_.get('respostas_ok') is True)
    tt_beta_ok_ = bool(tt_.get('beta_ok') is True and isinstance(tt_v_.get('beta'), float) and isinstance(b0_, float) and abs(tt_v_['beta'] - b0_) <= 1e-9 * abs(b0_))
    tt_anc_ok_ = bool(len(tt_.get('anchors') or {}) == len(DL_.ANCORAS) and all(a_ is True for a_ in (tt_.get('anchors') or {}).values()) and set(tt_.get('anchors') or {}) == set(DL_.ANCORAS) == set(tt_v_.get('ancoras') or {}) and all((a_ or {}).get('ok') is True for a_ in (tt_v_.get('ancoras') or {}).values()))
    m_tt_ = re.search(r'ancoras ok = (\\d+)/(\\d+) ; modulos do bundle ok = (\\d+)/(\\d+) ; bandeiras True = (\\d+)/(\\d+) ; escada = (\\[.*?\\]) ; gate = (.*)$', out, flags=re.M)   # a linha do bloco TETELESTAI E' O TERMINAL: sem «chave do lema» e sem «certificado habitado» (as dos blocos herdados tem esses campos entre as bandeiras e a escada, e nao casam aqui)
    tt_std_ok_ = bool(m_tt_ and m_tt_.group(1) == str(tt_v_.get('n_ancoras_ok')) and m_tt_.group(2) == str(tt_v_.get('n_ancoras')) and m_tt_.group(3) == str(tt_v_.get('n_modulos_ok')) and m_tt_.group(4) == str(tt_v_.get('n_modulos')) and m_tt_.group(5) == str(tt_v_.get('n_flags_true'))
                      and m_tt_.group(6) == str(tt_v_.get('n_flags')) and m_tt_.group(7) == str(tt_v_.get('escada')) and m_tt_.group(8).strip() == 'o mesmo da base')
    tt_ch_ = {os.path.basename(p_): DL_.VERBATIM_CHAVE_PREFIXO_V408 + hashlib.sha256(open(p_, 'rb').read()).hexdigest()[:16] for p_ in DL_.VERBATIM_ORIGEM_V408}   # (r2, 04/11 noite) as inscricoes do REGISTRO sao as falas do CONTRATO: um subconjunto das falas embutidas (todas estao em cunhagens_v408), com a ordem, os nomes e a correcao das classes (D51 revista) obrigatorias
    tt_ins_ok_ = bool(tt_.get('inscriptions') and set(tt_['inscriptions']) <= set(tt_ch_.values()) and {tt_ch_[DL_.N_ORDEM_V408], tt_ch_[DL_.N_NOMES], tt_ch_[DL_.N_CLASSES_PNP]} <= set(tt_['inscriptions']) and all(v_ is True for v_ in tt_['inscriptions'].values()))
    tt_ok_ = bool(tt_.get('all_verified') is True and tt_.get('does_not_gate_core') is True and tt_.get('runtime_executed') is True and tt_.get('exact_ladder') is True and tt_.get('embedded_sources_ok') is True and tt_.get('embedded_sources_n_ok') == DL_.N_BUNDLE
                  and bool(_ev(ESP, DL_.FECHO_REGISTRO)) and tt_.get('verdict') == _ev(ESP, DL_.FECHO_REGISTRO) == ETT_.get('verdict') and str(tt_.get('verdict') or '').startswith(DL_.VEREDITO_OK_PREFIXO) and str(tt_.get('verdict') or '').endswith(DL_.VEREDITO_SUFIXO)
                  and tt_mech_ok_ and tt_values_ok_ and tt_anc_prin_ok_ and tt_chaves_ok_ and tt_ip_ok_ and tt_resp_ok_ and tt_beta_ok_ and tt_anc_ok_ and tt_ins_ok_ and V['bandeiras']['ok'] and all(a_['ok'] for a_ in V['ancoras'].values()) and tt_std_ok_ and not tt_.get('guarda_violacoes')
                  and bool(tt_.get('podado')) and tt_.get('regra_provar_ou_podar') == DL_.REGRA_PROVAR_OU_PODAR and not GUARDA.search(str(tt_.get('verdict') or '')))
    V['fecho'] = {'registro': DL_.FECHO_REGISTRO, 'verdict': tt_.get('verdict'), 'ok': tt_.get('all_verified'), 'sealed': tt_ok_, 'n_checks': tt_m_.get('n_checks'), 'mech_ok': tt_mech_ok_, 'values': tt_v_, 'values_ok': tt_values_ok_, 'beta_ok': tt_beta_ok_, 'ancoras_ok': tt_anc_ok_, 'stdout_ok': tt_std_ok_,
                  'runtime_executed': tt_.get('runtime_executed'), 'does_not_gate_core': tt_.get('does_not_gate_core'), 'ancora_principal': tt_.get('ancora_principal'), 'ancoras_principais': list(tt_.get('ancoras_principais') or []), 'chaves_antigas_que_mudam': tt_.get('chaves_antigas_que_mudam'), 'insumo_purgado_ok': tt_ip_ok_, 'respostas_ok': tt_resp_ok_}
    if not tt_ok_:
        P.append('tetelestai_terminal_v408 nao selou inteiro (selo, as %s checagens do registro, valores [%s ancoras, %s modulos, %s bandeiras, escada, gate] == os de FLAGS/BUNDLE/ESPERADOS, a ancora principal e as quatro principais, NENHUMA chave antiga muda [a do lema segue True], o insumo purgado por sha256 [E23], as respostas do operador conferidas nos teoremas, beta == alfa x raiz de e do core, '
                 'as ressalvas, as %s falas por sha256, o podado e a regra provar ou podar, a linha do bloco TETELESTAI E O TERMINAL no stdout, nao move o gate): ver o registro no core' % (DL_.N_CHECKS_FECHO, len(DL_.ANCORAS), DL_.N_BUNDLE, FJ_['n_flags'], DL_.N_FALAS_V408))
    # o registro psion_canto_v407 (HERDADO da v407, RECRIADO pelo rito da v408; a escada do contrato subida pela C12, veredito na troca dita): segue SELADO; as 16 checagens, os valores (as 76 ancoras, os 9 modulos, as 98 bandeiras, a escada, o gate) == ESPERADOS[registros_funcao_v407], a CHAVE DO LEMA lida do kernel, as cinco chaves iguais as da v407 selada, o que fica False por teorema, o beta em runtime, as ressalvas da v407, o teste (d) so' citado e a linha do bloco no stdout
    pc_ = core.get('psion_canto_v407') or {}; pc_m_ = pc_.get('mechanics') or {}; pc_v_ = pc_.get('values') or {}; pc_k_ = pc_.get('keys') or {}; EPC_ = (ESP.get('registros_funcao_v407') or {}).get('psion_canto') or {}; td_ = pc_.get('teste_d') or {}
    N7F_ = (EPC_.get('values') or {}).get('n_flags')   # o numero das bandeiras do bundle da v407 (98): lido de ESPERADOS[registros_funcao_v407] (o ensaio a seco), nunca digitado
    pc_mech_ok_ = bool(pc_m_.get('passed') is True and pc_m_.get('n_checks') == DL_.D7.N_CHECKS_FECHO == EPC_.get('n_checks') == len(pc_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (pc_m_.get('checks') or [])))
    pc_values_ok_ = bool(pc_v_.get('n_ancoras_ok') == pc_v_.get('n_ancoras') == len(DL_.D7.ANCORAS) and bool(DL_.D7.ANCORAS) and pc_v_.get('n_modulos_ok') == pc_v_.get('n_modulos') == DL_.D7.N_BUNDLE and pc_v_.get('n_flags_true') == pc_v_.get('n_flags') == N7F_ and isinstance(N7F_, int) and pc_v_.get('escada') == [ESP['escada'][1]] * 3
                         and pc_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v407') == selo.get('qg_closure_verdict') and pc_v_.get('elo_lido_do_kernel') is True and pc_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA) and pc_v_.get('ressalvas') == list(DL_.D7.RESSALVAS_V407) and list(pc_.get('ressalvas') or []) == list(DL_.D7.RESSALVAS_V407)
                         and bool(EPC_.get('values')) and _feq({kk_: pc_v_.get(kk_) for kk_ in EPC_['values']}, EPC_['values']))
    pc_chaves_ok_ = bool(pc_k_.get('kernel_reads_the_link') is True and pc_k_.get('testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma') is True and bool(ESP.get('chaves_v407_esperadas')) and _feq(pc_k_, ESP.get('chaves_v407_esperadas')) and _feq(pc_k_, (EPC_.get('values') or {}).get('chaves'))
                         and pc_k_.get('witness_rigidity.trivial_inhabitant_exists') is False and pc_k_.get('qg_closure.gate.full_static_witness_exists') is False and pc_k_.get('witness_layers.canonical_full_witness_term_constructed') is True)
    pc_beta_ok_ = bool(pc_.get('beta_ok') is True and isinstance(pc_v_.get('beta'), float) and isinstance(b0_, float) and abs(pc_v_['beta'] - b0_) <= 1e-9 * abs(b0_))
    pc_anc_ok_ = bool(len(pc_.get('anchors') or {}) == len(DL_.D7.ANCORAS) and all(a_ is True for a_ in (pc_.get('anchors') or {}).values()) and set(pc_.get('anchors') or {}) == set(DL_.D7.ANCORAS) == set(pc_v_.get('ancoras') or {}) and all((a_ or {}).get('ok') is True for a_ in (pc_v_.get('ancoras') or {}).values()))
    m_pc_ = re.search(r'ancoras ok = (\\d+)/(\\d+) ; modulos do bundle ok = (\\d+)/(\\d+) ; bandeiras True = (\\d+)/(\\d+) ; chave do lema \\(lida do kernel\\) = (\\S+) ; escada = (\\[.*?\\]) ; gate = (.*)$', out, flags=re.M)
    pc_std_ok_ = bool(m_pc_ and m_pc_.group(1) == str(pc_v_.get('n_ancoras_ok')) and m_pc_.group(2) == str(pc_v_.get('n_ancoras')) and m_pc_.group(3) == str(pc_v_.get('n_modulos_ok')) and m_pc_.group(4) == str(pc_v_.get('n_modulos')) and m_pc_.group(5) == str(pc_v_.get('n_flags_true'))
                      and m_pc_.group(6) == str(pc_v_.get('n_flags')) and m_pc_.group(7) == 'True' and m_pc_.group(8) == str(pc_v_.get('escada')) and m_pc_.group(9).strip() == 'o mesmo da base')
    pc_ins_ok_ = bool(len(pc_.get('inscriptions') or {}) == len(DL_.D7.VERBATIM_ORIGEM_V407) and all(v_ is True for v_ in (pc_.get('inscriptions') or {}).values()))
    pc_ok_ = bool(pc_.get('all_verified') is True and pc_.get('does_not_gate_core') is True and pc_.get('runtime_executed') is True and pc_.get('link_read_from_the_kernel') is True and pc_.get('lemma') == DL_.D7.ANCORA_LEMA and pc_.get('pair_theorem') == DL_.D7.ANCORA_PAR and pc_.get('exact_ladder') is True
                  and pc_.get('embedded_sources_ok') is True and pc_.get('embedded_sources_n_ok') == DL_.D7.N_BUNDLE and list(pc_.get('pedras') or []) == [p_['name'] for p_ in DL_.D7.PEDRAS_V407] and bool(_ev(ESP, 'psion_canto_v407')) and pc_.get('verdict') == _ev(ESP, 'psion_canto_v407') == EPC_.get('verdict')
                  and str(pc_.get('verdict') or '').startswith('TGL_PSION_CANTO_V407__THE_LEMMA_THAT_LINKS_THE_TWO_FACES_OF_THE_PSION_IS_A_KERNEL_TERM__') and str(pc_.get('verdict') or '').endswith('__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED')
                  and pc_mech_ok_ and pc_values_ok_ and pc_chaves_ok_ and pc_beta_ok_ and pc_anc_ok_ and pc_ins_ok_ and V['bundle407']['ok'] and all(a_['ok'] for a_ in V['ancoras407'].values()) and pc_std_ok_ and not pc_.get('guarda_violacoes')
                  and td_.get('so_citado') is True and td_.get('resultado_no_um_py') is None and not GUARDA.search(str(pc_.get('verdict') or '')))
    V['fecho407'] = {'registro': 'psion_canto_v407', 'verdict': pc_.get('verdict'), 'ok': pc_.get('all_verified'), 'sealed': pc_ok_, 'n_checks': pc_m_.get('n_checks'), 'mech_ok': pc_mech_ok_, 'values': pc_v_, 'values_ok': pc_values_ok_, 'chaves_ok': pc_chaves_ok_, 'beta_ok': pc_beta_ok_, 'ancoras_ok': pc_anc_ok_,
                     'stdout_ok': pc_std_ok_, 'elo_lido_do_kernel': pc_.get('link_read_from_the_kernel'), 'runtime_executed': pc_.get('runtime_executed'), 'does_not_gate_core': pc_.get('does_not_gate_core'), 'lemma': pc_.get('lemma'), 'pair_theorem': pc_.get('pair_theorem'), 'teste_d_so_citado': td_.get('so_citado')}
    V['chaves407'] = dict(pc_k_)
    if not pc_ok_:
        P.append('psion_canto_v407 (HERDADO, recriado) nao selou inteiro (selo, as %s checagens do registro, valores [%s ancoras, %s modulos, as bandeiras da v407, escada, gate] == os de ESPERADOS[registros_funcao_v407], a CHAVE DO LEMA LIDA do kernel [True; as quatro da v406 True; as duas que ficam False por teorema, False], beta == alfa x raiz de e do core, '
                 'as ressalvas da v407, as %s falas de 03/11 por sha256, o teste (d) so\\' citado, o bundle da v407 [%s], a linha do bloco O PSION, O CANTO E O PAR no stdout, nao move o gate): ver o registro no core' % (DL_.D7.N_CHECKS_FECHO, len(DL_.D7.ANCORAS), DL_.D7.N_BUNDLE, len(DL_.D7.VERBATIM_ORIGEM_V407), DL_.D7.N_BUNDLE))
"""

# ---- o bloco das cunhagens: cunhagens_v408 (NOVO) + cunhagens_v407 / kh_n1_cobertura_v407 HERDADOS (E21 e pisos AO LADO) + cunhagens_v406 / kh_n1_cobertura_v406 HERDADOS (iguais a v407 selada); substituicao por SPAN entre as ancoras
INI_CUN = "    # cunhagens_v407 e kh_n1_cobertura_v407 (os DOIS registros NOVOS por spec): "
FIM_CUN = "    # os registros por spec da v407 (cunhagens_v404 e kh_n1_cobertura_v404, RECRIADOS): iguais aos selados"
NOVO_CUN = """    # cunhagens_v408 e kh_n1_cobertura_v408 (os DOIS registros NOVOS por spec): as 12 falas do operador de 04/11 por sha256 (embedded_ok), todas do operador (duas de AUTOR MISTO: a chave e' o sha16 do arquivo inteiro, o texto embutido e' so' o paragrafo dele); as erratas E21 a E23 mais a errata ao lado dos pisos de kh_n1_cobertura_v407 (gerencia c1, em nome proprio: DL.ASSINA); as decisoes D48 a D54; a leitura [INPUT] e as ressalvas; os nomes das pedras; o podado; a MOLDURA (nenhuma frase proibida nos tres registros novos)
    cu = core.get(DL_.CUNHAGENS_REGISTRO) or {}; kh = core.get(DL_.KH_REGISTRO) or {}
    cx_ = cu.get('extras') or {}; vb_ = cu.get('verbatim') or {}; ec_ = CM.get('cunhagens') or {}; pre_ = DL_.VERBATIM_CHAVE_PREFIXO_V408
    todas_op_ = bool(ec_ and all(str((ec_[k_] or {}).get('nome', '')).startswith('OPERADOR_04nov_') for k_ in ec_) and not any(str(v_.get('papel', '')).startswith('leitura da gerencia') for v_ in ec_.values()) and all((ec_[k_] or {}).get('autor') in ('operador', DL_.AUTOR_MISTO) for k_ in ec_))
    mistas_ = {k_ for k_, v_ in ec_.items() if (v_ or {}).get('autor') == DL_.AUTOR_MISTO}
    mistas_ok_ = bool(len(mistas_) == len(DL_.VERBATIM_CORTE) == len(DL_.VERBATIM_AUTOR_POR_NOME) and all(str((ec_[k_] or {}).get('sha256_arquivo_inteiro') or '')[:16] == k_[len(pre_):] and (ec_[k_] or {}).get('nome') in DL_.VERBATIM_CORTE for k_ in mistas_)
                      and all(str((ec_[k_] or {}).get('sha256') or '')[:16] == k_[len(pre_):] and not (ec_[k_] or {}).get('sha256_arquivo_inteiro') for k_ in ec_ if k_ not in mistas_)
                      and sum(1 for a_ in (cx_.get('autores') or {}).values() if a_ == DL_.AUTOR_MISTO) == len(mistas_) and len(cx_.get('autores') or {}) == len(ec_))
    verb_ok_ = bool(ec_) and len(ec_) == len(vb_) == len(DL_.VERBATIM_ORIGEM_V408) == DL_.N_FALAS_V408 and set(vb_) == set(ec_) and all((vb_[k_] or {}).get('sha256') == ec_[k_]['sha256'] and (vb_[k_] or {}).get('embedded_ok') is True for k_ in ec_)
    pares_ok_ = all(isinstance(x_, list) and len(x_) == 2 and x_[0] == x_[1] for x_ in (cu.get('kernel') or {}).values()) and bool(cu.get('kernel'))
    err_ = cu.get('erratas') or []; esp_err_ = list(DL_.ERRATAS_V408)
    erratas_ok_ = bool(esp_err_ and len(err_) == len(esp_err_) + 1 and all(e_.get('assinatura') == DL_.ASSINA for e_ in err_) and [e_.get('agora') for e_ in err_[:len(esp_err_)]] == esp_err_ and 'kh_n1_cobertura_v407' in str(err_[-1].get('ao_lado_de')) and cx_.get('assinatura_das_erratas') == DL_.ASSINA)
    dec_ = cx_.get('decisoes') or {}; exig_ = set(ESP.get('decisoes_v408_ids') or [])   # as decisoes desta versao (D48 a D54), lidas de ESPERADOS[decisoes_v408_ids]
    decisoes_ok_ = bool(exig_ and set(dec_) == exig_ and all(dec_.get(d_) == DL_.DECISOES.get(d_) and str(dec_.get(d_) or '').strip() for d_ in exig_))
    leitura_ok_ = bool(cx_.get('leituras') == DL_.LEITURA_V408 and 'INPUT' in str(DL_.LEITURA_V408.get('estatuto')) and 'PODADO' in str(DL_.LEITURA_V408.get('estatuto')) and len(cu.get('leituras_do_operador') or []) == len(DL_.FRASES_V408))
    ressalvas_ok_ = bool(cx_.get('ressalvas') == list(DL_.RESSALVAS_V408) and len(DL_.RESSALVAS_V408) >= 8)
    contagens_ok_ = bool(cx_.get('n_falas') == len(ec_) and cx_.get('n_bandeiras') == FJ_['n_flags'] and cx_.get('n_modulos') == DL_.N_BUNDLE)
    nomes_ok_ = bool(cx_.get('nomes_das_pedras') == dict(DL_.NOME_DO_OPERADOR) and cx_.get('falas_fora_do_desenho') == dict(DL_.VERBATIM_FORA_DO_DESENHO_V408) and bool(cx_.get('podado')))
    checks_cu_ok_ = bool(cu.get('checks')) and all(c_.get('ok') is True for c_ in cu.get('checks'))
    import guarda_frases_v408 as GF_
    moldura_ok_ = bool(all(not GF_.violacoes(json.dumps({k_: (core.get(n_) or {}).get(k_) for k_ in ('verdict', 'estatuto', 'scope', 'limites', 'diz', 'nao_diz')}, ensure_ascii=False)) for n_ in REG_FIXOS) and (GF_.controle_negativo() or {}).get('ok') is True)
    kh_ok_ = bool(kh.get('all_verified') is True and kh.get('does_not_gate_core') is True and bool(_ev(ESP, DL_.KH_REGISTRO)) and kh.get('verdict') == _ev(ESP, DL_.KH_REGISTRO) and bool(kh.get('checks')) and all(c_.get('ok') is True for c_ in kh.get('checks')) and not GUARDA.search(str(kh.get('verdict') or '')))
    cu_ok_ = bool(verb_ok_ and checks_cu_ok_ and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and erratas_ok_ and decisoes_ok_ and leitura_ok_ and ressalvas_ok_ and contagens_ok_ and todas_op_ and mistas_ok_ and nomes_ok_ and moldura_ok_
                  and bool(_ev(ESP, DL_.CUNHAGENS_REGISTRO)) and cu.get('verdict') == _ev(ESP, DL_.CUNHAGENS_REGISTRO) and not GUARDA.search(str(cu.get('verdict') or '')))
    V['cunhagens'] = {'n': len(vb_), 'ok': cu_ok_, 'verbatim_ok': verb_ok_, 'todas_do_operador': todas_op_, 'mistas_ok': mistas_ok_, 'n_mistas': len(mistas_), 'checks_ok': checks_cu_ok_, 'n_checks': len(cu.get('checks') or []), 'verdict': cu.get('verdict'), 'kernel_ok': pares_ok_, 'erratas_ok': erratas_ok_, 'n_erratas': len(err_),
                      'decisoes_ok': decisoes_ok_, 'n_decisoes': len(dec_), 'leitura_ok': leitura_ok_, 'ressalvas_ok': ressalvas_ok_, 'contagens_ok': contagens_ok_, 'nomes_ok': nomes_ok_, 'moldura_ok': moldura_ok_, 'kh_ok': kh_ok_}
    if not (verb_ok_ and checks_cu_ok_ and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and contagens_ok_ and mistas_ok_ and nomes_ok_ and cu.get('verdict') == _ev(ESP, DL_.CUNHAGENS_REGISTRO)):
        P.append('cunhagens_v408: as inscricoes embutidas nao sao as de CANDIDATO_v408.json (sha256, embedded_ok, %d falas; as duas de autor misto com o sha16 do arquivo inteiro na chave e o paragrafo dele no sha256), ou as checagens do registro, ou as contagens, ou os nomes das pedras, o podado e as falas fora do desenho, ou o veredito diferem do ensaio a seco' % DL_.N_FALAS_V408)
    if not todas_op_:
        P.append('cunhagens_v408: as inscricoes de 04/11 tem de ser TODAS falas do operador (OPERADOR_04nov_*; duas de autor misto, declaradas): nesta versao nao ha inscricao da gerencia')
    if not erratas_ok_:
        P.append('cunhagens_v408: as erratas E21 a E23 e a errata ao lado dos pisos de kh_n1_cobertura_v407 (assinadas pela gerencia c1, em nome proprio: DL.ASSINA) ausentes ou diferentes de delta_v408.ERRATAS_V408')
    if not decisoes_ok_:
        P.append('cunhagens_v408: as decisoes D48 a D54 da gerencia ausentes ou diferentes de delta_v408.DECISOES')
    if not (leitura_ok_ and ressalvas_ok_):
        P.append('cunhagens_v408: a leitura [INPUT] de 04/11 (estatutos), os trechos do operador ou as ressalvas ausentes ou diferentes de delta_v408 (LEITURA_V408, FRASES_V408, RESSALVAS_V408)')
    if not moldura_ok_:
        P.append('a MOLDURA falhou: alguma frase proibida num registro novo da v408 (guarda das frases) ou o controle negativo da guarda falhou')
    if not kh_ok_:
        P.append('kh_n1_cobertura_v408 nao selou como o ensaio a seco (selo, veredito, checagens, nao move o gate)')
    # cunhagens_v407 e kh_n1_cobertura_v407 (HERDADOS, RECRIADOS pelo rito da v408, por spec): iguais ao que a v407 SELOU (as 3 falas de 03/11 por sha256, todas do operador; as erratas E18 a E20 e os extras intactos) MAIS uma errata AO LADO (E21 / os pisos h2 h3 h6 h8), assinada em nome proprio; o veredito e' o esperado
    cu7_ = core.get('cunhagens_v407') or {}; kh7_ = core.get('kh_n1_cobertura_v407') or {}; cu7b_ = _base_core(PK).get('cunhagens_v407') or {}; kh7b_ = _base_core(PK).get('kh_n1_cobertura_v407') or {}
    e7_ = cu7_.get('erratas') or []; e7b_ = cu7b_.get('erratas') or []; k7e_ = kh7_.get('erratas') or []; k7eb_ = kh7b_.get('erratas') or []
    cu7_ok_ = bool(cu7_.get('all_verified') is True and cu7_.get('does_not_gate_core') is True and bool(cu7b_) and bool(cu7_.get('verbatim')) and _feq(cu7_.get('verbatim'), cu7b_.get('verbatim')) and len(cu7_.get('verbatim') or {}) == len(DL_.D7.VERBATIM_ORIGEM_V407) and all((v_ or {}).get('embedded_ok') is True for v_ in (cu7_.get('verbatim') or {}).values())
                   and _feq(cu7_.get('extras'), cu7b_.get('extras')) and len(e7_) == len(e7b_) + 1 and _feq(e7_[:len(e7b_)], e7b_) and e7_[-1].get('agora') == DL_.ERRATA_E21 and e7_[-1].get('assinatura') == DL_.ASSINA
                   and bool(cu7_.get('checks')) and all(c_.get('ok') is True for c_ in cu7_.get('checks')) and cu7_.get('verdict') == _ev(ESP, 'cunhagens_v407') and not GUARDA.search(str(cu7_.get('verdict') or '')))
    kh7_ok_ = bool(kh7_.get('all_verified') is True and kh7_.get('does_not_gate_core') is True and bool(kh7b_) and bool(kh7_.get('checks')) and all(c_.get('ok') is True for c_ in kh7_.get('checks')) and len(k7e_) == len(k7eb_) + 1 and _feq(k7e_[:len(k7eb_)], k7eb_) and str(k7e_[-1].get('assinatura')) == DL_.ASSINA and 'kh_n1_cobertura_v407' in str(k7e_[-1].get('ao_lado_de'))
                   and kh7_.get('verdict') == _ev(ESP, 'kh_n1_cobertura_v407') and not GUARDA.search(str(kh7_.get('verdict') or '')))
    V['cunh407d'] = {'ok': cu7_ok_, 'verdict': cu7_.get('verdict'), 'n': len(cu7_.get('verbatim') or {}), 'n_erratas': len(e7_), 'kh_ok': kh7_ok_, 'kh_verdict': kh7_.get('verdict')}
    if not cu7_ok_:
        P.append('cunhagens_v407 (HERDADA, recriada pelo rito) nao confere: as 3 falas de 03/11 (embedded_ok) e os extras iguais aos da v407 selada, as erratas E18 a E20 intactas MAIS a errata E21 ao lado (assinada em nome proprio), as checagens todas ok e o veredito esperado')
    if not kh7_ok_:
        P.append('kh_n1_cobertura_v407 (HERDADO, recriado pelo rito) nao confere: checagens (pisos h2 h3 h6, tamanho minimo h8) todas ok, a errata ao lado dos pisos MAIS as da v407 selada, e o veredito esperado')
    # cunhagens_v406 e kh_n1_cobertura_v406 (HERDADOS, RECRIADOS pelo rito da v408, por spec): IGUAIS ao que a v407 SELOU (as 23 falas de 02/11 por sha256, todas do operador; as erratas E14 a E17 e a E20 ao lado, que ja' vinham da v407; os pisos); o veredito NAO muda
    cu6_ = core.get('cunhagens_v406') or {}; kh6_ = core.get('kh_n1_cobertura_v406') or {}; cu6b_ = _base_core(PK).get('cunhagens_v406') or {}; kh6b_ = _base_core(PK).get('kh_n1_cobertura_v406') or {}
    e6_ = cu6_.get('erratas') or []; e6b_ = cu6b_.get('erratas') or []; k6e_ = kh6_.get('erratas') or []; k6eb_ = kh6b_.get('erratas') or []
    cu6_ok_ = bool(cu6_.get('all_verified') is True and cu6_.get('does_not_gate_core') is True and bool(cu6b_) and bool(cu6_.get('verbatim')) and _feq(cu6_.get('verbatim'), cu6b_.get('verbatim')) and len(cu6_.get('verbatim') or {}) == len(DL_.VERBATIM_ORIGEM_V406) and all((v_ or {}).get('embedded_ok') is True for v_ in (cu6_.get('verbatim') or {}).values())
                   and _feq(cu6_.get('extras'), cu6b_.get('extras')) and bool(e6b_) and len(e6_) == len(e6b_) and _feq(e6_, e6b_) and e6_[-1].get('agora') == DL_.ERRATA_E20 and str(e6_[-1].get('assinatura', '')).startswith('gerencia c1') and 'em nome proprio' in str(e6_[-1].get('assinatura', ''))
                   and bool(cu6_.get('checks')) and all(c_.get('ok') is True for c_ in cu6_.get('checks')) and cu6_.get('verdict') == _ev(ESP, 'cunhagens_v406') and not GUARDA.search(str(cu6_.get('verdict') or '')))
    kh6_ok_ = bool(kh6_.get('all_verified') is True and kh6_.get('does_not_gate_core') is True and bool(kh6b_) and bool(kh6_.get('checks')) and all(c_.get('ok') is True for c_ in kh6_.get('checks')) and bool(k6eb_) and len(k6e_) == len(k6eb_) and _feq(k6e_, k6eb_) and str(k6e_[-1].get('assinatura', '')).startswith('gerencia c1')
                   and kh6_.get('verdict') == _ev(ESP, 'kh_n1_cobertura_v406') and not GUARDA.search(str(kh6_.get('verdict') or '')))
    V['cunh406d'] = {'ok': cu6_ok_, 'verdict': cu6_.get('verdict'), 'n': len(cu6_.get('verbatim') or {}), 'n_erratas': len(e6_), 'kh_ok': kh6_ok_, 'kh_verdict': kh6_.get('verdict')}
    if not cu6_ok_:
        P.append('cunhagens_v406 (HERDADA, recriada pelo rito) nao confere: as 23 falas de 02/11 (embedded_ok), os extras e as erratas (E14 a E17 e a E20 ao lado, assinada em nome proprio) IGUAIS aos da v407 selada, as checagens (u7 versionada) todas ok e o veredito esperado')
    if not kh6_ok_:
        P.append('kh_n1_cobertura_v406 (HERDADO, recriado pelo rito) nao confere: checagens (pisos h2 h3 h6, tamanho minimo h8) todas ok, as erratas IGUAIS as da v407 selada (a dos pisos ao lado, assinada), e o veredito esperado')
"""


def _span(t, ini, fim, novo, rotulo):
    assert t.count(ini) == 1 and t.count(fim) == 1, ("ancora do span nao e' unica", rotulo, t.count(ini), t.count(fim))
    a = t.index(ini); b = t.index(fim)
    assert a < b, ("ancoras do span fora de ordem", rotulo)
    return t[:a] + novo + t[b:]


def main():
    b = open(ALVO, "rb").read(); t = b.decode("utf-8")
    assert "\r\n" not in t, "leitura_v408.py deixou de ser LF: adaptador escrito para o molde LF"
    # (1) o cabecalho: tudo antes do import
    k = t.index("import glob, hashlib, json, os, re, sys, datetime\n")
    assert t[:k].startswith("# -*- coding: utf-8 -*-\n# [A ADAPTAR v408]"), "o cabecalho nao e' o da subida mecanica"
    t = HEADER + t[k:]
    # (2) os spans (feitos ANTES das substituicoes exatas que tocam o bloco do fechamento, que fica fora dos spans)
    t = _span(t, INI_FECHO, FIM_FECHO, NOVO_FECHO, "fecho")
    t = _span(t, INI_CUN, FIM_CUN, NOVO_CUN, "cunhagens")
    # (3) as substituicoes exatas
    for velho, novo, vezes in SUBS:
        c = t.count(velho)
        assert c == vezes, ("substituicao nao casou (contagem)", vezes, c, velho[:100])
        t = t.replace(velho, novo)
    for proibido in ("[A ADAPTAR v408]", "03/11/2026] sobre a subida", "da v408: psion_canto=", "registros_funcao_v408') or {}).get('psion_canto')", "chaves_v408_esperadas", "cunhagens_v407: as inscricoes embutidas nao sao as de CANDIDATO_v408.json", "V['fecho407'] = {'registro': 'fechamento_v406'"):
        assert proibido not in t, ("sobrou texto da subida mecanica", proibido)
    ast.parse(t)
    bak = ALVO + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_adapt"
    open(bak, "wb").write(b)
    tmp = ALVO + ".tmp"; open(tmp, "wb").write(t.encode("utf-8"))
    assert os.path.getsize(tmp) > len(b) - 2000, "a leitura adaptada encolheu demais"
    os.replace(tmp, ALVO)
    print("ok leitura_v408.py %d -> %d B; sha16 %s; backup %s" % (len(b), os.path.getsize(ALVO), hashlib.sha256(open(ALVO, "rb").read()).hexdigest()[:16], os.path.basename(bak)))


if __name__ == "__main__":
    main()
