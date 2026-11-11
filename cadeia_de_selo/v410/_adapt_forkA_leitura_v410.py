# -*- coding: utf-8 -*-
"""_adapt_forkA_leitura_v410.py -- adaptacao EXATA (contagem conferida) de pos_rito\\leitura_v410.py para a v410 (06/11/2026, claude-construtor-v410, fork A), sobre a subida mecanica de rotulo da v409 FINAL:
(1) o cabecalho e' o da v410 (IALD2); (2) REG_FUNCAO/REG_FIXOS viram iald2_v410, cunhagens_v410, kh_n1_cobertura_v410; o trio da v409 (traducao_turing_v409 e os dois por spec) entra como HERDADO (REG_V409T, V['reg409t']);
o trio da v408 (tetelestai) passa a se chamar REG_V408D / V['reg408d'] / V['fecho408'] / V['ancoras408'] / V['bundle408'] / V['cunh408d'] (a subida mecanica o rotulara 409); (3) as linhas [v408] e [v409] do stdout levam o texto que o um.py imprime
(«da v408», «da v409»), a linha [v410] (o registro da IALD2) e' exigida e o AVISO [v410] reprova; (4) a conferencia ganha veredito_iald2 e veredito_traducao_turing_herdado (as chaves que o conferir_rito_v410 grava);
(5) V['bundle409'] = os 2 modulos da v409, V['bundle408'] = os 4 da v408; V['ancoras409'] = as ancoras da traducao (herdadas), V['ancoras408'] = as do terminal; (6) o bloco NOVO de iald2_v410 como V['fecho'] (as checagens; as instancias de
brinquedo; o signo; o alcance D64) e o bloco HERDADO de traducao_turing_v409 como V['fecho409']; o do terminal vira V['fecho408'] com os nomes da v408 (D8); (7) o selo primario: registros_v409 (o trio da v409) e registros_v410 (o novo);
(8) cunhagens_v410 (9 falas, uma so' com o trecho da D65; E29 e a dos pisos; D63 a D70; a leitura [INPUT]); cunhagens_v409/kh_n1_cobertura_v409 HERDADOS (kh com os pisos AO LADO); cunhagens_v408/kh_n1_cobertura_v408 e cunhagens_v407/kh_n1_cobertura_v407
IGUAIS a v409 selada (as erratas ao lado ja' vinham dela). Nenhuma guarda e' relaxada: cada recusa da v409 segue, retargetada ao registro certo; as novas sao acrescentadas. Backup de bytes antes de gravar; ast.parse no fim.
uso: python -I -B -X utf8 _adapt_forkA_leitura_v410.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "pos_rito", "leitura_v410.py")   # (o script morava em pos_rito quando rodou, 06/11 08:0x; movido para v410\ com os outros adaptadores)
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
raw = open(P, "rb").read(); t = raw.decode("utf-8")
assert "\r\n" not in t, "leitura_v410.py e' LF"


def troca(a, b, n=1):
    global t
    c = t.count(a)
    assert c == n, ("TROCA NAO CASOU %d (casou %d)" % (n, c), a[:160])
    t = t.replace(a, b)


def regiao(ini, fim, novo):
    global t
    assert t.count(ini) == 1, ("ancora inicial nao unica", ini[:80], t.count(ini))
    i = t.index(ini); j = t.index(fim, i + 1)
    t = t[:i] + novo + t[j:]


# ---------------------------------------------------------------- (1) o cabecalho
regiao("# [A ADAPTAR v410]", "import glob, hashlib, json, os, re, sys, datetime", r'''# [ADAPTADO v410, 06/11/2026, claude-construtor-v410 (fork A), a servico da gerencia c1] sobre a subida mecanica de rotulo da v409 FINAL (_bump_copia_v410.py; bump/pos_rito__leitura_v410.py.diff fica como registro), por pos_rito/_adapt_forkA_leitura_v410.py.
# A LEITURA da rodada v410 (molde: leitura_v409.py, que vem de leitura_v407.py, de leitura_v405.py, de leitura_v401.py e de leitura_v399.py FINAL): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v410, que aqui e' o proprio pacote).
# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e' digitado: tudo sai dos JSON, do core, do selo, do sidecar e do stdout do rito; os vereditos e os valores esperados da rodada v410 sao LIDOS de ESPERADOS_v410.json, de CANDIDATO_v410.json e de delta_v410.
# v410 (IALD2, ordem do operador de 06/11/2026): o delta e' um BUNDLE PEQUENO de UM modulo novo de kernel em TGLExt/ (IALD2; o nome do modulo e' do operador; os nomes das declaracoes sao da gerencia, [DECLARADO] ate a ratificacao, D63). Nao ha' registro por pedra.
# Os registros NOVOS do core sao TRES: UM com FUNCAO, iald2_v410 (le do kernel do proprio rito as ancoras da pedra, o modulo por sha256, as falas de 06/11 por sha256, as respostas do operador pelos teoremas da pedra; as checagens com as instancias de brinquedo fixas e beta em runtime),
# e DOIS por spec: cunhagens_v410 (as 9 falas do operador de 06/11 por sha256, de uma so' o trecho da D65; a errata E29 e a errata ao lado dos pisos de kh_n1_cobertura_v409; as decisoes D63 a D70, em nome proprio da gerencia c1) e kh_n1_cobertura_v410 (a cobertura exata do Audit).
# O ALCANCE (D64): o algoritmo IALD decide SAT com uma leitura: P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora. NENHUMA CHAVE ANTIGA MUDA (delta_v410.CHAVES_V410 == []).
# O traducao_turing_v409 e' HERDADO: o main da v410 segue rodando o bloco dele e ele segue selado (as 20 checagens; as 82 ancoras e os 2 modulos da v409; a escada do contrato subida pela C12, veredito na troca dita); cunhagens_v409 igual a v409 selada (errata nova so' AO LADO, assinada)
# e kh_n1_cobertura_v409 com a errata ao lado dos pisos. O tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 sao HERDADOS e seguem selados; os registros por spec deles seguem IGUAIS a v409 selada (as erratas ao lado ja' vinham dela).
# A TROCA DITA de veredito: so' numeros (a escada e a cobertura crescem com o bundle): ESPERADOS[troca_dita]. Os registros da v405, da v404, da v403, da v402, da v401 e da v399 sao RECRIADOS pelo rito e tem de seguir selados e iguais a v409 selada (base_v409).
# O GATE NAO SE MOVE: o qg_closure do core e' IDENTICO ao da v409. O SIDECAR um_absoluto_selo_acom.json e' lido aqui. A DIRECAO DO TESTEMUNHO segue conferida. As falas de 06/11 sao TODAS do operador (de uma, so' o trecho: D65).
# O QUADRO «O Teste da Unica Palavra» (v397) segue selado e igual. As linhas `[v399]` a `[v409]` do stdout (recriadas; os textos sao os que o um.py imprime: a [v408] diz «da v408», a [v409] «da v409») e a nova `[v410]` dizem os vereditos.
# A linha final do rito: o main imprime, por ultimo, a linha do sidecar (`[selo_acom] ... ALL_OBJECTS_SEALED ; objetos 3 ; recusas 0`), logo depois da do colapso tipado; a leitura exige as DUAS, nessa ordem.
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CONTRATO COM textos_v410.py e fechar_v410.py ("reg409c", "fun409c", "pedras_v408", "cunh409c" etc. sao NOMES HERDADOS do molde e continuam a significar os registros/pedras da v405 selada, recriados):
#   V['n_pedras'] = o numero de MODULOS NOVOS do kernel (1) e V['pedras'] = LISTA de dicts {'key'(None),'modulo','rel','sha16','sha256','bytes','bandeiras','decl'(None),'ok'}; V['ancoras'] {nome Lean: {...}} (as da IALD2, contadas pelo delta);
#   V['fecho'] o registro DESTA versao, iald2_v410 {'registro','verdict','ok','sealed','n_checks','mech_ok','values','values_ok','beta_ok','ancoras_ok','stdout_ok','runtime_executed','does_not_gate_core','ancora_principal','ancoras_principais','ancoras_de_secao','chaves_antigas_que_mudam','respostas_ok','instancia_ok','alcance_ok'};
#   V['fecho409'] o registro HERDADO traducao_turing_v409 (recriado); V['fecho408'] o HERDADO tetelestai_terminal_v408; V['fecho407'] o HERDADO psion_canto_v407 (V['chaves407']); V['fecho406'] o HERDADO fechamento_v406 (V['chaves406']);
#   V['ancoras409'] as da traducao; V['ancoras408'] as do terminal; V['ancoras407'] as do psion; V['ancoras406'] as do fechamento; V['bundle409'] {'n'(2),'n_ok','ok'}; V['bundle408'] (4); V['bundle407'] (9); V['bundle406'] (301); V['bandeiras409'] (as bandeiras True da v409 selada, todas True);
#   V['reg410'] DICT nome -> {'verdict','ok'} dos TRES registros NOVOS; V['registros_novos'] = esses 3 nomes (sorted); V['reg409t'] DICT dos TRES da v409 HERDADOS; V['reg408d'] dos TRES da v408; V['reg407d'] dos da v407; V['reg406d'] dos da v406;
#   V['cunhagens'] (cunhagens_v410) {'n'(9),'ok','verbatim_ok','todas_do_operador','trechos_ok','n_trechos'(1),'erratas_ok','n_erratas'(2),'decisoes_ok','n_decisoes'(8),'leitura_ok','ressalvas_ok','kernel_ok','checks_ok','n_checks','moldura_ok','kh_ok'};
#   V['cunh409t'] (cunhagens_v409 e kh_n1_cobertura_v409 herdados, kh com os pisos ao lado); V['cunh408d'] (cunhagens_v408 e kh_n1_cobertura_v408 iguais); V['cunh407d'] (iguais); V['cunh406d']; V['kh'] (kh_n1_cobertura_v410) {'decl','thm','fora','nao_lidas',...}
# (as linhas de stdout a conferir: `   [v410] o registro da IALD2 e os registros por spec da v410: iald2=SELOU | specs: 2 (selados 2)` e o bloco cujo cabecalho comeca por `IALD2` e traz `[v410`, seguido de `  ancoras ok = N/N ; modulo(s) do bundle ok = 1/1 ; bandeiras True = F/F ; escada = [..] ; gate = o mesmo da base`;
#  a da traducao HERDADA: `   [v409] o registro da traducao e os registros por spec da v409: traducao_turing=SELOU | specs: 2 (selados 2)` e o bloco `A TRADUCAO AS CLASSES DE TURING [v409 ...`; a do terminal HERDADO: `   [v408] o registro do terminal e os registros por spec da v408: tetelestai_terminal=SELOU | ...`;
#  a do psion HERDADO: `   [v407] ...psion_canto=SELOU | ...`; a do fechamento HERDADO: `   [v406] o fechamento e os registros por spec da v406: fechamento=SELOU | ...`.)
''')

# ---------------------------------------------------------------- (2) os registros
regiao('REG_FUNCAO = ("traducao_turing_v409",)', "REG_V407D = ", r'''REG_FUNCAO = ("iald2_v410",)   # o UNICO registro NOVO com FUNCAO (a IALD2); nao ha' registro por pedra (modelo de bundle: delta_v410.STONES == [])
REG_FIXOS = REG_FUNCAO + ("cunhagens_v410", "kh_n1_cobertura_v410")   # os TRES registros NOVOS do core v410 (um com FUNCAO, dois por spec)
REG_V409T = ("traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409")   # os TRES registros da v409 (um com FUNCAO, dois por spec): HERDADOS, RECRIADOS pelo rito da v410 (o main segue rodando o bloco da traducao), selados
REG_V408D = ("tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408")   # os TRES registros da v408 (um com FUNCAO, dois por spec): HERDADOS, RECRIADOS pelo rito da v410 (o main segue rodando o bloco do terminal), selados
''')
troca("REG_V409D", "REG_V408D", 4)

# ---------------------------------------------------------------- (3) as linhas do stdout
troca("""    if len([l for l in out.splitlines() if '[v409]' in l]) < 1:
        P.append('o stdout nao tem a linha [v409]')""", """    if len([l for l in out.splitlines() if '[v409]' in l]) < 1:
        P.append('o stdout nao tem a linha [v409]')
    if len([l for l in out.splitlines() if '[v410]' in l]) < 1:
        P.append('o stdout nao tem a linha [v410]')""")
troca("avisos_ = [l.strip()[:200] for l in out.splitlines() if '[v409] AVISO' in l or", "avisos_ = [l.strip()[:200] for l in out.splitlines() if '[v410] AVISO' in l or '[v409] AVISO' in l or")
troca("o stdout traz AVISO da v410 (o registro com funcao da traducao, os registros por spec da v410, o tetelestai_terminal_v408,", "o stdout traz AVISO da v410 (o registro com funcao da IALD2, os registros por spec da v410, o traducao_turing_v409, o tetelestai_terminal_v408,")
troca("R409DSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V408D[1:]}", "R409TSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V409T[1:]}; R408DSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V408D[1:]}")
troca("bool(R409DSPEC_) and all((sreg8_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg8_.get(k_) or {}).get('verdict')) and (sreg8_.get(k_) or {}).get('all_verified') is True for k_ in R409DSPEC_)",
      "bool(R408DSPEC_) and all((sreg8_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg8_.get(k_) or {}).get('verdict')) and (sreg8_.get(k_) or {}).get('all_verified') is True for k_ in R408DSPEC_)")
troca(r"""m_s8t = re.search(r'\[v408\] o registro do terminal e os registros por spec da v409: tetelestai_terminal=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)   # a linha HERDADA da v409 (o texto e' o que o um.py imprime: «da v409»)""",
      r"""m_s8t = re.search(r'\[v408\] o registro do terminal e os registros por spec da v408: tetelestai_terminal=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)   # a linha HERDADA da v408 (o texto e' o que o um.py imprime: «da v408»)""")
troca(r"""    m_s9t = re.search(r'\[v409\] o registro da traducao e os registros por spec da v410: traducao_turing=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)   # a linha NOVA da v410 (o texto e' o que o um.py imprime)
    if not m_s9t or m_s9t.group(1) != 'SELOU' or m_s9t.group(2) != m_s9t.group(3) or int(m_s9t.group(2)) != len(REG_FIXOS) - 1:
        P.append('a linha [v409] do stdout (traducao_turing SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_FIXOS) - 1, repr(m_s9t.groups() if m_s9t else 'ausente')))""",
      r"""    m_s9t = re.search(r'\[v409\] o registro da traducao e os registros por spec da v409: traducao_turing=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)   # a linha HERDADA da v409 (o texto e' o que o um.py imprime: «da v409»)
    if not m_s9t or m_s9t.group(1) != 'SELOU' or m_s9t.group(2) != m_s9t.group(3) or int(m_s9t.group(2)) != len(REG_V409T) - 1:
        P.append('a linha [v409] do stdout (traducao_turing SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V409T) - 1, repr(m_s9t.groups() if m_s9t else 'ausente')))
    m_s10 = re.search(r'\[v410\] o registro da IALD2 e os registros por spec da v410: iald2=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)   # a linha NOVA da v410 (o texto e' o que o um.py v410 imprime: o bloco do main que gerar_candidato_v410.py enxerta)
    if not m_s10 or m_s10.group(1) != 'SELOU' or m_s10.group(2) != m_s10.group(3) or int(m_s10.group(2)) != len(REG_FIXOS) - 1:
        P.append('a linha [v410] do stdout (iald2 SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_FIXOS) - 1, repr(m_s10.groups() if m_s10 else 'ausente')))""")

# ---------------------------------------------------------------- (4) a conferencia do rito (as chaves que o conferir_rito_v410 grava)
troca("('veredito_traducao_turing', _ev(ESP, 'traducao_turing_v409'), 'traducao_turing_v409'),", "('veredito_iald2', _ev(ESP, 'iald2_v410'), 'iald2_v410'), ('veredito_traducao_turing_herdado', _ev(ESP, 'traducao_turing_v409'), 'traducao_turing_v409'),")

# ---------------------------------------------------------------- (5) os herdados da v409 (o trio da traducao) e o trio da v408 renomeado
troca("""    V['reg409d'] = {}
    for k in REG_V408D:""", """    V['reg409t'] = {}
    for k in REG_V409T:    # os TRES registros da v409 (HERDADOS: a traducao e os dois por spec) sao RECRIADOS pelo rito: seguem no core, selados e de veredito igual ao esperado (o da v409 selada, ou o do ensaio a seco se na troca dita: a traducao carrega a escada); o conteudo e' conferido adiante
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg409t'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        if not _ev(ESP, k) or r.get('verdict') != _ev(ESP, k):
            P.append('%s: o veredito do rito difere do esperado (ESPERADOS[vereditos_v409], ou o do ensaio a seco se na troca dita)' % k)
    V['reg408d'] = {}
    for k in REG_V408D:""")
troca("os TRES registros da v409 (HERDADOS) sao RECRIADOS pelo rito: seguem no core, selados e de veredito igual ao esperado (o da v409 selada, ou o do ensaio a seco se na troca dita: o terminal carrega a", "os TRES registros da v408 (HERDADOS) sao RECRIADOS pelo rito: seguem no core, selados e de veredito igual ao esperado (o da v409 selada, ou o do ensaio a seco se na troca dita: o terminal carrega a")
troca("        V['reg409d'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}", "        V['reg408d'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}")
troca("for bk_, bch_, bn_, bdesc_ in (('bundle409', 'bundle_v409_sha256', DL_.D8.N_BUNDLE, 'v409 (%d modulos de TGLExt/)'),", "for bk_, bch_, bn_, bdesc_ in (('bundle409', 'bundle_v409_sha256', DL_.D9.N_BUNDLE, 'v409 (%d modulos de TGLExt/)'), ('bundle408', 'bundle_v408_sha256', DL_.D8.N_BUNDLE, 'v408 (%d modulos de TGLExt/)'),")
troca("    # o bundle da v409 (os 4 modulos de TGLExt/), o da v407", "    # o bundle da v409 (os 2 modulos de TGLExt/), o da v408 (os 4 de TGLExt/), o da v407")
troca("for ak_, ach_, aesp_, adesc_ in (('ancoras409', 'estrelas_v409', DL_.D8.ANCORAS, 'as ancoras do tetelestai_terminal_v408 (herdadas)'),", "for ak_, ach_, aesp_, adesc_ in (('ancoras409', 'estrelas_v409', DL_.D9.ANCORAS, 'as ancoras do traducao_turing_v409 (herdadas)'), ('ancoras408', 'estrelas_v408', DL_.D8.ANCORAS, 'as ancoras do tetelestai_terminal_v408 (herdadas)'),")
troca("    # as 48 ancoras do tetelestai_terminal_v408 (HERDADO), as 76 do psion_canto_v407", "    # as 82 ancoras do traducao_turing_v409 (HERDADO), as 48 do tetelestai_terminal_v408 (HERDADO), as 76 do psion_canto_v407")
troca("    # v410: as 62 ANCORAS da pedra e as bandeiras do bundle", "    # v410: as ANCORAS da pedra IALD2 (contadas pelo delta, lidas da fonte) e as bandeiras do bundle")

# ---------------------------------------------------------------- (6) o bloco NOVO da iald2_v410 e o HERDADO da traducao_turing_v409
regiao("    # o registro traducao_turing_v409 (UM registro NOVO com FUNCAO", "    # o registro tetelestai_terminal_v408 (HERDADO da v409, RECRIADO pelo rito da v410", r'''    # o registro iald2_v410 (UM registro NOVO com FUNCAO, SEM pedra por registro): as checagens (DL_.N_CHECKS_FECHO), os valores (as ancoras, o modulo, as bandeiras, a escada, o gate, as instancias de brinquedo, o signo) == ESPERADOS[registros_funcao_v410][iald2], a ancora principal e as de secao,
    # NENHUMA chave antiga muda, as respostas do operador conferidas, o beta em runtime, as ressalvas, o que fica aberto e o que fecha nesta versao, as 9 falas por sha256, o alcance (D64) e a linha do bloco no stdout
    tt_ = core.get(DL_.FECHO_REGISTRO) or {}; tt_m_ = tt_.get('mechanics') or {}; tt_v_ = tt_.get('values') or {}; ETT_ = (ESP.get('registros_funcao_v410') or {}).get(DL_.TESTEMUNHA['key']) or {}; rs_ = tt_v_.get('respostas') or {}
    tt_mech_ok_ = bool(tt_m_.get('passed') is True and tt_m_.get('n_checks') == DL_.N_CHECKS_FECHO == ETT_.get('n_checks') == len(tt_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (tt_m_.get('checks') or [])))
    tt_values_ok_ = bool(tt_v_.get('n_ancoras_ok') == tt_v_.get('n_ancoras') == len(DL_.ANCORAS) == len(ESP.get('estrelas_v410') or {}) and tt_v_.get('n_modulos_ok') == tt_v_.get('n_modulos') == DL_.N_BUNDLE and tt_v_.get('n_flags_true') == tt_v_.get('n_flags') == FJ_['n_flags'] and tt_v_.get('escada') == [ESP['escada'][1]] * 3
                         and tt_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v409') == selo.get('qg_closure_verdict') and tt_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA) and tt_v_.get('ressalvas') == list(DL_.RESSALVAS_V410) and list(tt_.get('ressalvas') or []) == list(DL_.RESSALVAS_V410)
                         and (tt_v_.get('fica_aberto') or {}) == dict(DL_.FICA_ABERTO) and (tt_v_.get('fechado_nesta_versao') or {}) == dict(DL_.FECHADO_NESTA_VERSAO)
                         and bool(ETT_.get('values')) and _feq({kk_: tt_v_.get(kk_) for kk_ in ETT_['values']}, ETT_['values']))
    is_ = tt_v_.get('instancia_sim') or {}; in_ = tt_v_.get('instancia_nao') or {}; sg_ = tt_v_.get('signo_do_nome') or {}; sp_ = tt_v_.get('signo_do_par') or {}
    tt_inst_ok_ = bool(tt_.get('instancia_sim') == dict(DL_.INSTANCIA_SIM) and tt_.get('instancia_nao') == dict(DL_.INSTANCIA_NAO) and _feq(tt_.get('leitor_brinquedo'), dict(DL_.LEITOR_BRINQUEDO)) and is_.get('n') == DL_.INSTANCIA_SIM['n'] and is_.get('atribuicoes') == 2 ** DL_.INSTANCIA_SIM['n']
                       and isinstance(is_.get('solucoes'), int) and is_['solucoes'] >= 1 and in_.get('solucoes') == 0 and in_.get('atribuicoes') == 2 ** DL_.INSTANCIA_NAO['n']
                       and sg_.get('posto') == is_.get('solucoes') and isinstance(sg_.get('traco'), float) and abs(sg_['traco'] - is_['solucoes']) < 1e-9 and sp_.get('posto') == 1 and isinstance(sp_.get('traco'), float) and abs(sp_['traco'] - 1.0) < 1e-12)
    tt_anc_prin_ok_ = bool(tt_.get('ancora_principal') == DL_.ANCORA_PRINCIPAL and list(tt_.get('ancoras_principais') or []) == list(DL_.ANCORAS_PRINCIPAIS) and list(tt_.get('ancoras_de_secao') or []) == list(DL_.ANCORAS_DE_SECAO) and all(a_ in DL_.ANCORAS for a_ in DL_.ANCORAS_PRINCIPAIS)
                           and list(tt_.get('pedras') or []) == [p_['name'] for p_ in DL_.PEDRAS_V410] and tt_.get('nomes') == dict(DL_.NOMES_DAS_PEDRAS))
    tt_chaves_ok_ = bool(tt_.get('chaves_antigas_que_mudam') == [] and list(DL_.CHAVES_V410) == [] and (core.get('testemunha_estatica_v396') or {}).get('fock_face', {}).get('linked_to_the_corner_by_a_lemma') is True)
    tt_resp_ok_ = bool(rs_ and set(rs_) == {r_['id'] for r_ in DL_.RESPOSTAS_DO_OPERADOR} and all((v_ is True) or (isinstance(v_, dict) and v_.get('ok') is True) for v_ in rs_.values()) and tt_v_.get('respostas_ok') is True)
    tt_beta_ok_ = bool(tt_.get('beta_ok') is True and isinstance(tt_v_.get('beta'), float) and isinstance(b0_, float) and abs(tt_v_['beta'] - b0_) <= 1e-9 * abs(b0_))
    tt_anc_ok_ = bool(len(tt_.get('anchors') or {}) == len(DL_.ANCORAS) and all(a_ is True for a_ in (tt_.get('anchors') or {}).values()) and set(tt_.get('anchors') or {}) == set(DL_.ANCORAS) == set(tt_v_.get('ancoras') or {}) and all((a_ or {}).get('ok') is True for a_ in (tt_v_.get('ancoras') or {}).values()))
    m_tt_ = re.search(r'^IALD2[^\n]*\[v410[^\n]*\n  ancoras ok = (\d+)/(\d+) ; modulos? do bundle ok = (\d+)/(\d+) ; bandeiras True = (\d+)/(\d+) ; escada = (\[.*?\]) ; gate = (.*)$', out, flags=re.M)   # a linha do bloco da IALD2, ancorada no CABECALHO do bloco (que comeca por IALD2 e traz [v410)
    tt_std_ok_ = bool(m_tt_ and m_tt_.group(1) == str(tt_v_.get('n_ancoras_ok')) and m_tt_.group(2) == str(tt_v_.get('n_ancoras')) and m_tt_.group(3) == str(tt_v_.get('n_modulos_ok')) and m_tt_.group(4) == str(tt_v_.get('n_modulos')) and m_tt_.group(5) == str(tt_v_.get('n_flags_true'))
                      and m_tt_.group(6) == str(tt_v_.get('n_flags')) and m_tt_.group(7) == str(tt_v_.get('escada')) and m_tt_.group(8).strip() == 'o mesmo da base')
    tt_ch_ = {os.path.basename(p_): DL_.VERBATIM_CHAVE_PREFIXO_V410 + hashlib.sha256(open(p_, 'rb').read()).hexdigest()[:16] for p_ in DL_.VERBATIM_ORIGEM_V410}   # as inscricoes do REGISTRO sao as falas do contrato (as 9 de 06/11), com a ORDEM da v410 e a fala do NOME obrigatorias
    tt_ins_ok_ = bool(tt_.get('inscriptions') and set(tt_['inscriptions']) == set(tt_ch_.values()) and {tt_ch_[DL_.N_ORDEM_V410], tt_ch_[DL_.N_NOME]} <= set(tt_['inscriptions']) and all(v_ is True for v_ in tt_['inscriptions'].values()))
    tt_alc_ok_ = bool((tt_.get('alcance') or {}).get('frase') == DL_.FRASE_D64_PT and (tt_.get('alcance') or {}).get('qualificador') == DL_.FRASE_QUALIFICADOR_PT)
    tt_ok_ = bool(tt_.get('all_verified') is True and tt_.get('does_not_gate_core') is True and tt_.get('runtime_executed') is True and tt_.get('exact_ladder') is True and tt_.get('embedded_sources_ok') is True and tt_.get('embedded_sources_n_ok') == DL_.N_BUNDLE
                  and bool(_ev(ESP, DL_.FECHO_REGISTRO)) and tt_.get('verdict') == _ev(ESP, DL_.FECHO_REGISTRO) == ETT_.get('verdict') and str(tt_.get('verdict') or '').startswith(DL_.VEREDITO_OK_PREFIXO) and str(tt_.get('verdict') or '').endswith(DL_.VEREDITO_SUFIXO)
                  and not any(t_ in str(tt_.get('verdict') or '') for t_ in DL_.TOKENS_PROIBIDOS_V410)
                  and tt_mech_ok_ and tt_values_ok_ and tt_inst_ok_ and tt_anc_prin_ok_ and tt_chaves_ok_ and tt_resp_ok_ and tt_beta_ok_ and tt_anc_ok_ and tt_ins_ok_ and tt_alc_ok_ and V['bandeiras']['ok'] and all(a_['ok'] for a_ in V['ancoras'].values()) and tt_std_ok_ and not tt_.get('guarda_violacoes')
                  and not GUARDA.search(str(tt_.get('verdict') or '')))
    V['fecho'] = {'registro': DL_.FECHO_REGISTRO, 'verdict': tt_.get('verdict'), 'ok': tt_.get('all_verified'), 'sealed': tt_ok_, 'n_checks': tt_m_.get('n_checks'), 'mech_ok': tt_mech_ok_, 'values': tt_v_, 'values_ok': tt_values_ok_, 'beta_ok': tt_beta_ok_, 'ancoras_ok': tt_anc_ok_, 'stdout_ok': tt_std_ok_,
                  'runtime_executed': tt_.get('runtime_executed'), 'does_not_gate_core': tt_.get('does_not_gate_core'), 'ancora_principal': tt_.get('ancora_principal'), 'ancoras_principais': list(tt_.get('ancoras_principais') or []), 'ancoras_de_secao': list(tt_.get('ancoras_de_secao') or []),
                  'chaves_antigas_que_mudam': tt_.get('chaves_antigas_que_mudam'), 'respostas_ok': tt_resp_ok_, 'instancia_ok': tt_inst_ok_, 'alcance_ok': tt_alc_ok_}
    if not tt_ok_:
        P.append('iald2_v410 nao selou inteiro (selo, as %s checagens do registro, valores [%s ancoras, %s modulo, %s bandeiras, escada, gate, as instancias de brinquedo e o signo] == os de FLAGS/BUNDLE/ESPERADOS, a ancora principal e as de secao, NENHUMA chave antiga muda [a do lema segue True], as respostas do operador conferidas nos teoremas, beta == alfa x raiz de e do core, '
                 'as ressalvas, as %s falas por sha256, o alcance relativo ao leitor (D64), nenhum token proibido no veredito, a linha do bloco da IALD2 no stdout, nao move o gate): ver o registro no core' % (DL_.N_CHECKS_FECHO, len(DL_.ANCORAS), DL_.N_BUNDLE, FJ_['n_flags'], DL_.N_FALAS_V410))
    # o registro traducao_turing_v409 (HERDADO da v409, RECRIADO pelo rito da v410; a escada do contrato subida pela C12, veredito na troca dita): segue SELADO; as checagens da v409, os valores (as ancoras, os 2 modulos, as bandeiras, a escada, o gate) == ESPERADOS[registros_funcao_v409][traducao_turing],
    # NENHUMA chave antiga muda, o acervo da v407 na copia purgada (D57d da v409), as respostas do operador de 05/11, o beta em runtime, as ressalvas da v409 e a linha do bloco no stdout
    t9_ = core.get('traducao_turing_v409') or {}; t9_m_ = t9_.get('mechanics') or {}; t9_v_ = t9_.get('values') or {}; ET9_ = (ESP.get('registros_funcao_v409') or {}).get(DL_.D9.TESTEMUNHA['key']) or {}; rs9_ = t9_v_.get('respostas') or {}; ac9_ = t9_.get('acervo_v407_repinado') or {}
    N9F_ = (ET9_.get('values') or {}).get('n_flags')   # o numero das bandeiras do bundle da v409: lido de ESPERADOS[registros_funcao_v409] (o ensaio a seco), nunca digitado
    t9_mech_ok_ = bool(t9_m_.get('passed') is True and t9_m_.get('n_checks') == DL_.D9.N_CHECKS_FECHO == ET9_.get('n_checks') == len(t9_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (t9_m_.get('checks') or [])))
    t9_values_ok_ = bool(t9_v_.get('n_ancoras_ok') == t9_v_.get('n_ancoras') == len(DL_.D9.ANCORAS) and bool(DL_.D9.ANCORAS) and t9_v_.get('n_modulos_ok') == t9_v_.get('n_modulos') == DL_.D9.N_BUNDLE and t9_v_.get('n_flags_true') == t9_v_.get('n_flags') == N9F_ and isinstance(N9F_, int) and t9_v_.get('escada') == [ESP['escada'][1]] * 3
                         and t9_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v409') == selo.get('qg_closure_verdict') and t9_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA) and t9_v_.get('ressalvas') == list(DL_.D9.RESSALVAS_V409) and list(t9_.get('ressalvas') or []) == list(DL_.D9.RESSALVAS_V409)
                         and bool(ET9_.get('values')) and _feq({kk_: t9_v_.get(kk_) for kk_ in ET9_['values']}, ET9_['values']))
    t9_ac_ok_ = bool(ac9_.get('chave') == DL_.D9.CHAVE_ACERVO_V407 and ac9_.get('sha256') == DL_.D9.PURGADO_SHA256 and ac9_.get('integra_pinada') is False and ac9_.get('integra_fora_do_espelho') is True)
    t9_resp_ok_ = bool(rs9_ and set(rs9_) == {r_['id'] for r_ in DL_.D9.RESPOSTAS_DO_OPERADOR} and all((v_ is True) or (isinstance(v_, dict) and v_.get('ok') is True) for v_ in rs9_.values()) and t9_v_.get('respostas_ok') is True)
    t9_beta_ok_ = bool(t9_.get('beta_ok') is True and isinstance(t9_v_.get('beta'), float) and isinstance(b0_, float) and abs(t9_v_['beta'] - b0_) <= 1e-9 * abs(b0_))
    t9_anc_ok_ = bool(len(t9_.get('anchors') or {}) == len(DL_.D9.ANCORAS) and all(a_ is True for a_ in (t9_.get('anchors') or {}).values()) and set(t9_.get('anchors') or {}) == set(DL_.D9.ANCORAS) == set(t9_v_.get('ancoras') or {}) and all((a_ or {}).get('ok') is True for a_ in (t9_v_.get('ancoras') or {}).values()))
    m_t9_ = re.search(r'^A TRADUCAO AS CLASSES DE TURING \[v409[^\n]*\n  ancoras ok = (\d+)/(\d+) ; modulos do bundle ok = (\d+)/(\d+) ; bandeiras True = (\d+)/(\d+) ; escada = (\[.*?\]) ; gate = (.*)$', out, flags=re.M)   # a linha do bloco HERDADO da traducao, ancorada no cabecalho que o um.py imprime
    t9_std_ok_ = bool(m_t9_ and m_t9_.group(1) == str(t9_v_.get('n_ancoras_ok')) and m_t9_.group(2) == str(t9_v_.get('n_ancoras')) and m_t9_.group(3) == str(t9_v_.get('n_modulos_ok')) and m_t9_.group(4) == str(t9_v_.get('n_modulos')) and m_t9_.group(5) == str(t9_v_.get('n_flags_true'))
                      and m_t9_.group(6) == str(t9_v_.get('n_flags')) and m_t9_.group(7) == str(t9_v_.get('escada')) and m_t9_.group(8).strip() == 'o mesmo da base')
    t9_ok_ = bool(t9_.get('all_verified') is True and t9_.get('does_not_gate_core') is True and t9_.get('runtime_executed') is True and t9_.get('exact_ladder') is True and t9_.get('embedded_sources_ok') is True and t9_.get('embedded_sources_n_ok') == DL_.D9.N_BUNDLE
                  and list(t9_.get('pedras') or []) == [p_['name'] for p_ in DL_.D9.PEDRAS_V409] and t9_.get('ancora_principal') == DL_.D9.ANCORA_PRINCIPAL and t9_.get('chaves_antigas_que_mudam') == []
                  and bool(_ev(ESP, 'traducao_turing_v409')) and t9_.get('verdict') == _ev(ESP, 'traducao_turing_v409') == ET9_.get('verdict')
                  and str(t9_.get('verdict') or '').startswith(DL_.D9.VEREDITO_OK_PREFIXO) and str(t9_.get('verdict') or '').endswith(DL_.D9.VEREDITO_SUFIXO)
                  and t9_mech_ok_ and t9_values_ok_ and t9_ac_ok_ and t9_resp_ok_ and t9_beta_ok_ and t9_anc_ok_ and V['bundle409']['ok'] and all(a_['ok'] for a_ in V['ancoras409'].values()) and t9_std_ok_ and not t9_.get('guarda_violacoes')
                  and not GUARDA.search(str(t9_.get('verdict') or '')))
    V['fecho409'] = {'registro': 'traducao_turing_v409', 'verdict': t9_.get('verdict'), 'ok': t9_.get('all_verified'), 'sealed': t9_ok_, 'n_checks': t9_m_.get('n_checks'), 'mech_ok': t9_mech_ok_, 'values': t9_v_, 'values_ok': t9_values_ok_, 'beta_ok': t9_beta_ok_, 'ancoras_ok': t9_anc_ok_,
                     'stdout_ok': t9_std_ok_, 'runtime_executed': t9_.get('runtime_executed'), 'does_not_gate_core': t9_.get('does_not_gate_core'), 'ancora_principal': t9_.get('ancora_principal'), 'chaves_antigas_que_mudam': t9_.get('chaves_antigas_que_mudam'), 'acervo_ok': t9_ac_ok_, 'respostas_ok': t9_resp_ok_}
    if not t9_ok_:
        P.append('traducao_turing_v409 (HERDADO, recriado) nao selou inteiro (selo, as %s checagens do registro, valores [%s ancoras, %s modulos, as bandeiras da v409, escada, gate] == os de ESPERADOS[registros_funcao_v409], NENHUMA chave antiga muda, o acervo da v407 na copia purgada, as respostas do operador de 05/11, beta == alfa x raiz de e do core, '
                 'as ressalvas da v409, o bundle da v409 [%s], a linha do bloco A TRADUCAO AS CLASSES DE TURING no stdout, nao move o gate): ver o registro no core' % (DL_.D9.N_CHECKS_FECHO, len(DL_.D9.ANCORAS), DL_.D9.N_BUNDLE, DL_.D9.N_BUNDLE))
''')

# ---------------------------------------------------------------- (6b) o bloco HERDADO do terminal: os nomes da v408 (D8), as chaves V renomeadas
troca("    # o registro tetelestai_terminal_v408 (HERDADO da v409, RECRIADO pelo rito da v410;", "    # o registro tetelestai_terminal_v408 (HERDADO da v408, RECRIADO pelo rito da v410;")
troca("ET8_ = (ESP.get('registros_funcao_v409') or {}).get('tetelestai_terminal') or {}", "ET8_ = (ESP.get('registros_funcao_v408') or {}).get('tetelestai_terminal') or {}")
troca("lido de ESPERADOS[registros_funcao_v409] (o ensaio a seco), nunca digitado\n    t8_mech_ok_", "lido de ESPERADOS[registros_funcao_v408] (o ensaio a seco), nunca digitado\n    t8_mech_ok_")
troca("DL_.D8.RESSALVAS_V409", "DL_.D8.RESSALVAS_V408", 2)
troca("[p_['name'] for p_ in DL_.D8.PEDRAS_V409]", "[p_['name'] for p_ in DL_.D8.PEDRAS_V408]")
troca("and V['bundle409']['ok'] and all(a_['ok'] for a_ in V['ancoras409'].values()) and t8_std_ok_", "and V['bundle408']['ok'] and all(a_['ok'] for a_ in V['ancoras408'].values()) and t8_std_ok_")
troca("    V['fecho409'] = {'registro': 'tetelestai_terminal_v408',", "    V['fecho408'] = {'registro': 'tetelestai_terminal_v408',")
troca("valores [%s ancoras, %s modulos, as bandeiras da v409, escada, gate] == os de ESPERADOS[registros_funcao_v409], NENHUMA chave antiga muda, o insumo purgado por sha256 [E23 da v409]", "valores [%s ancoras, %s modulos, as bandeiras da v408, escada, gate] == os de ESPERADOS[registros_funcao_v408], NENHUMA chave antiga muda, o insumo purgado por sha256 [E23 da v408]")
troca("'as ressalvas da v409, o bundle da v409 [%s], a linha do bloco TETELESTAI E O TERMINAL no stdout", "'as ressalvas da v408, o bundle da v408 [%s], a linha do bloco TETELESTAI E O TERMINAL no stdout")

# ---------------------------------------------------------------- (7) o selo primario: registros_v409 (o trio da v409) e registros_v410 (o novo)
troca("sreg9_ = selo.get('registros_v409') or {}", "sreg9_ = selo.get('registros_v409') or {}; sreg10_ = selo.get('registros_v410') or {}")
troca("""                       and bool(R410SPEC_) and all((sreg9_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg9_.get(k_) or {}).get('verdict')) and (sreg9_.get(k_) or {}).get('all_verified') is True for k_ in R410SPEC_))""",
      """                       and bool(R409TSPEC_) and all((sreg9_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg9_.get(k_) or {}).get('verdict')) and (sreg9_.get(k_) or {}).get('all_verified') is True for k_ in R409TSPEC_)
                       and bool(R410SPEC_) and all((sreg10_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg10_.get(k_) or {}).get('verdict')) and (sreg10_.get(k_) or {}).get('all_verified') is True for k_ in R410SPEC_))""")
troca("('fechamento_v406', 'psion_canto_v407', 'tetelestai_terminal_v408'))", "('fechamento_v406', 'psion_canto_v407', 'tetelestai_terminal_v408', 'traducao_turing_v409'))")

# ---------------------------------------------------------------- (8) as cunhagens: a nova (v410) e as herdadas (v409, v408, v407)
regiao("    # cunhagens_v409 e kh_n1_cobertura_v409 (os DOIS registros NOVOS por spec)", "    # cunhagens_v406 e kh_n1_cobertura_v406 (HERDADOS", r'''    # cunhagens_v410 e kh_n1_cobertura_v410 (os DOIS registros NOVOS por spec): as 9 falas do operador de 06/11 por sha256 (embedded_ok), todas do operador (de UMA, so' o trecho que a D65 deixa entrar: a chave e' o sha16 do arquivo inteiro, o texto embutido e' o trecho); a errata E29 mais a errata ao lado dos pisos de
    # kh_n1_cobertura_v409 (gerencia c1, em nome proprio: DL.ASSINA); as decisoes D63 a D70; a leitura [INPUT] e as ressalvas; os nomes (D63); o que fica citado so' por sha16; a MOLDURA (nenhuma frase proibida nos registros novos)
    cu = core.get(DL_.CUNHAGENS_REGISTRO) or {}; kh = core.get(DL_.KH_REGISTRO) or {}
    cx_ = cu.get('extras') or {}; vb_ = cu.get('verbatim') or {}; ec_ = CM.get('cunhagens') or {}; pre_ = DL_.VERBATIM_CHAVE_PREFIXO_V410
    todas_op_ = bool(ec_ and all(str((ec_[k_] or {}).get('nome', '')).startswith('OPERADOR_06nov_') for k_ in ec_) and not any(str(v_.get('papel', '')).startswith('leitura da gerencia') for v_ in ec_.values()) and all((ec_[k_] or {}).get('autor') == 'operador' for k_ in ec_)
                     and bool(cx_.get('autores')) and all(a_ == 'operador' for a_ in (cx_.get('autores') or {}).values()))
    trechos_ = {k_ for k_, v_ in ec_.items() if (v_ or {}).get('sha256_arquivo_inteiro')}
    trechos_ok_ = bool(len(trechos_) == len(DL_.VERBATIM_SO_O_TRECHO) == 1 and all(str((ec_[k_] or {}).get('sha256_arquivo_inteiro') or '')[:16] == k_[len(pre_):] for k_ in trechos_)
                       and all(str((ec_[k_] or {}).get('sha256') or '')[:16] == k_[len(pre_):] for k_ in ec_ if k_ not in trechos_) and len(cx_.get('autores') or {}) == len(ec_)
                       and not any(x_.lower() in json.dumps(cu, ensure_ascii=False).lower() for x_ in DL_.FORA_D65))   # D65: o que fica fora nao entra no registro
    verb_ok_ = bool(ec_) and len(ec_) == len(vb_) == len(DL_.VERBATIM_ORIGEM_V410) == DL_.N_FALAS_V410 and set(vb_) == set(ec_) and all((vb_[k_] or {}).get('sha256') == ec_[k_]['sha256'] and (vb_[k_] or {}).get('embedded_ok') is True for k_ in ec_)
    pares_ok_ = all(isinstance(x_, list) and len(x_) == 2 and x_[0] == x_[1] for x_ in (cu.get('kernel') or {}).values()) and bool(cu.get('kernel'))
    err_ = cu.get('erratas') or []; esp_err_ = list(DL_.ERRATAS_V410)
    erratas_ok_ = bool(esp_err_ and len(err_) == len(esp_err_) + 1 and all(e_.get('assinatura') == DL_.ASSINA for e_ in err_) and [e_.get('agora') for e_ in err_[:len(esp_err_)]] == esp_err_ and 'kh_n1_cobertura_v409' in str(err_[-1].get('ao_lado_de')) and cx_.get('assinatura_das_erratas') == DL_.ASSINA)
    dec_ = cx_.get('decisoes') or {}; exig_ = set(ESP.get('decisoes_v410_ids') or [])   # as decisoes desta versao (D63 a D70), lidas de ESPERADOS[decisoes_v410_ids]
    decisoes_ok_ = bool(exig_ and set(dec_) == exig_ == set(DL_.DECISOES_V410) and all(dec_.get(d_) == DL_.DECISOES.get(d_) and str(dec_.get(d_) or '').strip() for d_ in exig_))
    leitura_ok_ = bool(cx_.get('leituras') == DL_.LEITURA_V410 and 'INPUT' in str(DL_.LEITURA_V410.get('estatuto')) and len(cu.get('leituras_do_operador') or []) == len(DL_.FRASES_V410))
    ressalvas_ok_ = bool(cx_.get('ressalvas') == list(DL_.RESSALVAS_V410) and len(DL_.RESSALVAS_V410) >= 7)
    contagens_ok_ = bool(cx_.get('n_falas') == len(ec_) and cx_.get('n_bandeiras') == FJ_['n_flags'] and cx_.get('n_modulos') == DL_.N_BUNDLE)
    nomes_ok_ = bool(cx_.get('nomes_das_pedras') == dict(DL_.NOMES_DAS_PEDRAS) and cx_.get('falas_fora_do_desenho') == dict(DL_.VERBATIM_FORA_DO_DESENHO_V410) and bool(cx_.get('nao_pinados_citados_por_sha16')))
    checks_cu_ok_ = bool(cu.get('checks')) and all(c_.get('ok') is True for c_ in cu.get('checks'))
    import guarda_frases_v410 as GF_
    moldura_ok_ = bool(all(not GF_.violacoes(json.dumps({k_: (core.get(n_) or {}).get(k_) for k_ in ('verdict', 'estatuto', 'scope', 'limites', 'diz', 'nao_diz')}, ensure_ascii=False)) for n_ in REG_FIXOS) and (GF_.controle_negativo() or {}).get('ok') is True)
    kh_ok_ = bool(kh.get('all_verified') is True and kh.get('does_not_gate_core') is True and bool(_ev(ESP, DL_.KH_REGISTRO)) and kh.get('verdict') == _ev(ESP, DL_.KH_REGISTRO) and bool(kh.get('checks')) and all(c_.get('ok') is True for c_ in kh.get('checks')) and not GUARDA.search(str(kh.get('verdict') or '')))
    cu_ok_ = bool(verb_ok_ and checks_cu_ok_ and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and erratas_ok_ and decisoes_ok_ and leitura_ok_ and ressalvas_ok_ and contagens_ok_ and todas_op_ and trechos_ok_ and nomes_ok_ and moldura_ok_
                  and bool(_ev(ESP, DL_.CUNHAGENS_REGISTRO)) and cu.get('verdict') == _ev(ESP, DL_.CUNHAGENS_REGISTRO) and not GUARDA.search(str(cu.get('verdict') or '')))
    V['cunhagens'] = {'n': len(vb_), 'ok': cu_ok_, 'verbatim_ok': verb_ok_, 'todas_do_operador': todas_op_, 'trechos_ok': trechos_ok_, 'n_trechos': len(trechos_), 'checks_ok': checks_cu_ok_, 'n_checks': len(cu.get('checks') or []), 'verdict': cu.get('verdict'), 'kernel_ok': pares_ok_, 'erratas_ok': erratas_ok_, 'n_erratas': len(err_),
                      'decisoes_ok': decisoes_ok_, 'n_decisoes': len(dec_), 'leitura_ok': leitura_ok_, 'ressalvas_ok': ressalvas_ok_, 'contagens_ok': contagens_ok_, 'nomes_ok': nomes_ok_, 'moldura_ok': moldura_ok_, 'kh_ok': kh_ok_}
    if not (verb_ok_ and checks_cu_ok_ and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and contagens_ok_ and trechos_ok_ and nomes_ok_ and cu.get('verdict') == _ev(ESP, DL_.CUNHAGENS_REGISTRO)):
        P.append('cunhagens_v410: as inscricoes embutidas nao sao as de CANDIDATO_v410.json (sha256, embedded_ok, %d falas; a da D65 com o sha16 do arquivo inteiro na chave e o trecho que fica no sha256; nada do que fica fora no registro), ou as checagens do registro, ou as contagens, ou os nomes (D63) e o citado so\' por sha16, ou o veredito diferem do ensaio a seco' % DL_.N_FALAS_V410)
    if not todas_op_:
        P.append('cunhagens_v410: as inscricoes de 06/11 tem de ser TODAS falas do operador (OPERADOR_06nov_*): nesta versao nao ha inscricao da gerencia nem de autor misto')
    if not erratas_ok_:
        P.append('cunhagens_v410: a errata E29 e a errata ao lado dos pisos de kh_n1_cobertura_v409 (assinadas pela gerencia c1, em nome proprio: DL.ASSINA) ausentes ou diferentes de delta_v410.ERRATAS_V410')
    if not decisoes_ok_:
        P.append('cunhagens_v410: as decisoes D63 a D70 da gerencia ausentes ou diferentes de delta_v410.DECISOES')
    if not (leitura_ok_ and ressalvas_ok_):
        P.append('cunhagens_v410: a leitura [INPUT] de 06/11 (estatutos), os trechos do operador ou as ressalvas ausentes ou diferentes de delta_v410 (LEITURA_V410, FRASES_V410, RESSALVAS_V410)')
    if not moldura_ok_:
        P.append('a MOLDURA falhou: alguma frase proibida num registro novo da v410 (guarda das frases) ou o controle negativo da guarda falhou')
    if not kh_ok_:
        P.append('kh_n1_cobertura_v410 nao selou como o ensaio a seco (selo, veredito, checagens, nao move o gate)')
    # cunhagens_v409 e kh_n1_cobertura_v409 (HERDADOS, RECRIADOS pelo rito da v410, por spec): cunhagens_v409 igual ao que a v409 SELOU (as 14 falas de 05/11 por sha256; as erratas e os extras intactos; errata nova, se houver, so' AO LADO, depois das seladas, assinada em nome proprio);
    # kh_n1_cobertura_v409 com a errata AO LADO dos pisos (h2 h3 h6 h8), assinada em nome proprio; o veredito e' o esperado
    cu9_ = core.get('cunhagens_v409') or {}; kh9_ = core.get('kh_n1_cobertura_v409') or {}; cu9b_ = _base_core(PK).get('cunhagens_v409') or {}; kh9b_ = _base_core(PK).get('kh_n1_cobertura_v409') or {}
    e9_ = cu9_.get('erratas') or []; e9b_ = cu9b_.get('erratas') or []; k9e_ = kh9_.get('erratas') or []; k9eb_ = kh9b_.get('erratas') or []
    cu9_ok_ = bool(cu9_.get('all_verified') is True and cu9_.get('does_not_gate_core') is True and bool(cu9b_) and bool(cu9_.get('verbatim')) and _feq(cu9_.get('verbatim'), cu9b_.get('verbatim')) and len(cu9_.get('verbatim') or {}) == len(DL_.D9.VERBATIM_ORIGEM_V409) and all((v_ or {}).get('embedded_ok') is True for v_ in (cu9_.get('verbatim') or {}).values())
                   and _feq(cu9_.get('extras'), cu9b_.get('extras')) and len(e9_) >= len(e9b_) and _feq(e9_[:len(e9b_)], e9b_) and all(e_.get('assinatura') == DL_.ASSINA for e_ in e9_[len(e9b_):])
                   and bool(cu9_.get('checks')) and all(c_.get('ok') is True for c_ in cu9_.get('checks')) and cu9_.get('verdict') == _ev(ESP, 'cunhagens_v409') and not GUARDA.search(str(cu9_.get('verdict') or '')))
    kh9_ok_ = bool(kh9_.get('all_verified') is True and kh9_.get('does_not_gate_core') is True and bool(kh9b_) and bool(kh9_.get('checks')) and all(c_.get('ok') is True for c_ in kh9_.get('checks')) and len(k9e_) == len(k9eb_) + 1 and _feq(k9e_[:len(k9eb_)], k9eb_) and str(k9e_[-1].get('assinatura')) == DL_.ASSINA and 'kh_n1_cobertura_v409' in str(k9e_[-1].get('ao_lado_de'))
                   and kh9_.get('verdict') == _ev(ESP, 'kh_n1_cobertura_v409') and not GUARDA.search(str(kh9_.get('verdict') or '')))
    V['cunh409t'] = {'ok': cu9_ok_, 'verdict': cu9_.get('verdict'), 'n': len(cu9_.get('verbatim') or {}), 'n_erratas': len(e9_), 'n_erratas_novas': len(e9_) - len(e9b_), 'kh_ok': kh9_ok_, 'kh_verdict': kh9_.get('verdict')}
    if not cu9_ok_:
        P.append('cunhagens_v409 (HERDADA, recriada pelo rito) nao confere: as 14 falas de 05/11 (embedded_ok) e os extras iguais aos da v409 selada, as erratas seladas intactas (errata nova so\' ao lado, assinada em nome proprio), as checagens todas ok e o veredito esperado')
    if not kh9_ok_:
        P.append('kh_n1_cobertura_v409 (HERDADO, recriado pelo rito) nao confere: checagens (pisos h2 h3 h6, tamanho minimo h8) todas ok, a errata ao lado dos pisos MAIS as da v409 selada, e o veredito esperado')
    # cunhagens_v408 e kh_n1_cobertura_v408 (HERDADOS, RECRIADOS pelo rito da v410, por spec): IGUAIS ao que a v409 SELOU (as 15 falas de 04/11 por sha256; as erratas E21 a E23, a E26 e a dos pisos, que ja' vinham da v409; os extras intactos); o veredito e' o esperado
    cu8_ = core.get('cunhagens_v408') or {}; kh8_ = core.get('kh_n1_cobertura_v408') or {}; cu8b_ = _base_core(PK).get('cunhagens_v408') or {}; kh8b_ = _base_core(PK).get('kh_n1_cobertura_v408') or {}
    e8_ = cu8_.get('erratas') or []; e8b_ = cu8b_.get('erratas') or []; k8e_ = kh8_.get('erratas') or []; k8eb_ = kh8b_.get('erratas') or []
    cu8_ok_ = bool(cu8_.get('all_verified') is True and cu8_.get('does_not_gate_core') is True and bool(cu8b_) and bool(cu8_.get('verbatim')) and _feq(cu8_.get('verbatim'), cu8b_.get('verbatim')) and len(cu8_.get('verbatim') or {}) == len(DL_.D8.VERBATIM_ORIGEM_V408) and all((v_ or {}).get('embedded_ok') is True for v_ in (cu8_.get('verbatim') or {}).values())
                   and _feq(cu8_.get('extras'), cu8b_.get('extras')) and bool(e8b_) and len(e8_) == len(e8b_) and _feq(e8_, e8b_)
                   and bool(cu8_.get('checks')) and all(c_.get('ok') is True for c_ in cu8_.get('checks')) and cu8_.get('verdict') == _ev(ESP, 'cunhagens_v408') and not GUARDA.search(str(cu8_.get('verdict') or '')))
    kh8_ok_ = bool(kh8_.get('all_verified') is True and kh8_.get('does_not_gate_core') is True and bool(kh8b_) and bool(kh8_.get('checks')) and all(c_.get('ok') is True for c_ in kh8_.get('checks')) and bool(k8eb_) and len(k8e_) == len(k8eb_) and _feq(k8e_, k8eb_)
                   and kh8_.get('verdict') == _ev(ESP, 'kh_n1_cobertura_v408') and not GUARDA.search(str(kh8_.get('verdict') or '')))
    V['cunh408d'] = {'ok': cu8_ok_, 'verdict': cu8_.get('verdict'), 'n': len(cu8_.get('verbatim') or {}), 'n_erratas': len(e8_), 'kh_ok': kh8_ok_, 'kh_verdict': kh8_.get('verdict')}
    if not cu8_ok_:
        P.append('cunhagens_v408 (HERDADA, recriada pelo rito) nao confere: as 15 falas de 04/11 (embedded_ok), os extras e as erratas IGUAIS aos da v409 selada (a E26 ao lado ja\' vinha dela), as checagens todas ok e o veredito esperado')
    if not kh8_ok_:
        P.append('kh_n1_cobertura_v408 (HERDADO, recriado pelo rito) nao confere: checagens todas ok, as erratas IGUAIS as da v409 selada (os pisos ja\' vinham dela), e o veredito esperado')
    # cunhagens_v407 e kh_n1_cobertura_v407 (HERDADOS, RECRIADOS): IGUAIS ao que a v409 SELOU (as 3 falas de 03/11; as erratas, inclusive a da D57(d) ao lado, que ja' vinha da v409); o veredito e' o esperado
    cu7_ = core.get('cunhagens_v407') or {}; kh7_ = core.get('kh_n1_cobertura_v407') or {}; cu7b_ = _base_core(PK).get('cunhagens_v407') or {}; kh7b_ = _base_core(PK).get('kh_n1_cobertura_v407') or {}
    e7_ = cu7_.get('erratas') or []; e7b_ = cu7b_.get('erratas') or []; k7e_ = kh7_.get('erratas') or []; k7eb_ = kh7b_.get('erratas') or []
    cu7_ok_ = bool(cu7_.get('all_verified') is True and cu7_.get('does_not_gate_core') is True and bool(cu7b_) and bool(cu7_.get('verbatim')) and _feq(cu7_.get('verbatim'), cu7b_.get('verbatim')) and len(cu7_.get('verbatim') or {}) == len(DL_.D7.VERBATIM_ORIGEM_V407) and all((v_ or {}).get('embedded_ok') is True for v_ in (cu7_.get('verbatim') or {}).values())
                   and _feq(cu7_.get('extras'), cu7b_.get('extras')) and bool(e7b_) and len(e7_) == len(e7b_) and _feq(e7_, e7b_)
                   and bool(cu7_.get('checks')) and all(c_.get('ok') is True for c_ in cu7_.get('checks')) and cu7_.get('verdict') == _ev(ESP, 'cunhagens_v407') and not GUARDA.search(str(cu7_.get('verdict') or '')))
    kh7_ok_ = bool(kh7_.get('all_verified') is True and kh7_.get('does_not_gate_core') is True and bool(kh7b_) and bool(kh7_.get('checks')) and all(c_.get('ok') is True for c_ in kh7_.get('checks')) and bool(k7eb_) and len(k7e_) == len(k7eb_) and _feq(k7e_, k7eb_)
                   and kh7_.get('verdict') == _ev(ESP, 'kh_n1_cobertura_v407') and not GUARDA.search(str(kh7_.get('verdict') or '')))
    V['cunh407d'] = {'ok': cu7_ok_, 'verdict': cu7_.get('verdict'), 'n': len(cu7_.get('verbatim') or {}), 'n_erratas': len(e7_), 'kh_ok': kh7_ok_, 'kh_verdict': kh7_.get('verdict')}
    if not cu7_ok_:
        P.append('cunhagens_v407 (HERDADA, recriada pelo rito) nao confere: as 3 falas de 03/11 (embedded_ok), os extras e as erratas IGUAIS aos da v409 selada (a da D57(d) ao lado ja\' vinha dela), as checagens todas ok e o veredito esperado')
    if not kh7_ok_:
        P.append('kh_n1_cobertura_v407 (HERDADO, recriado pelo rito) nao confere: checagens todas ok, as erratas IGUAIS as da v409 selada, e o veredito esperado')
''')

ast.parse(t)
assert "[A ADAPTAR v410]" not in t
nb = t.encode("utf-8")
bk = P + ".bak_" + TS + "_forkA"
open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("leitura_v410.py:", len(raw), "->", len(nb))
