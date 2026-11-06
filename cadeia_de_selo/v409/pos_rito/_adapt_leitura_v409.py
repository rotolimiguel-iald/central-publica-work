# -*- coding: utf-8 -*-
"""_adapt_leitura_v409.py -- adaptacao EXATA (contagem conferida) de pos_rito\\leitura_v409.py para a v409 (05/11/2026, claude-construtor-v409, fork A), sobre a subida mecanica de rotulo da v408 FINAL:
(1) o cabecalho e' o da v409 (A TRADUCAO AS CLASSES DE TURING); (2) REG_FUNCAO/REG_FIXOS viram traducao_turing_v409, cunhagens_v409, kh_n1_cobertura_v409; REG_V408D passa a ser o trio HERDADO da v408 (tetelestai_terminal_v408, cunhagens_v408, kh_n1_cobertura_v408)
e REG_V407D (novo nome) o trio HERDADO da v407 (psion_canto_v407, cunhagens_v407, kh_n1_cobertura_v407), que a subida mecanica rotulara 408; (3) as linhas [v407]/[v408] do stdout levam o texto que o um.py imprime («da v407», «da v408») e a linha [v409] e' exigida; o AVISO [v409] reprova;
(4) o >>> veredito <<< e a conferencia ganham traducao_turing_v409 (veredito_traducao_turing) e o terminal vira herdado; (5) V['bundle408'] passa a ser o bundle de 4 da v408 e V['bundle407'] (novo) o de 9 da v407; V['ancoras408'] as 48 do terminal e V['ancoras407'] (novo) as 76 do psion;
(6) o bloco do terminal vira V['fecho408'] (HERDADO) e entra o bloco NOVO de traducao_turing_v409 como V['fecho'] (17 checagens; a instancia de brinquedo; o acervo da v407 repinado, D57d); o do psion vira V['fecho407'] (HERDADO); (7) o selo primario: registros_v406/v407/v408/v409 e os resumos;
(8) cunhagens_v409 (10 falas, duas so' com o trecho da D59; E24 a E26 e a dos pisos; D55 a D60; a leitura [INPUT]); cunhagens_v408/kh_n1_cobertura_v408 HERDADOS com a E26 e os pisos AO LADO (cunh408d); cunhagens_v407 com a errata da D57(d) ao lado e kh_n1_cobertura_v407 igual a v408 selada (cunh407d);
cunhagens_v406/kh_n1_cobertura_v406 HERDADOS iguais a v408 selada (cunh406d). Nenhuma guarda e' relaxada: cada recusa da v408 segue, retargetada ao registro certo; as novas sao acrescentadas. Backup de bytes antes de gravar (via _adapt_util_v409.Arq); ast.parse no fim.
uso: python -I -B -X utf8 _adapt_leitura_v409.py"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from _adapt_util_v409 import Arq  # noqa: E402

a = Arq(os.path.join(HERE, "leitura_v409.py"))


def regiao(ini, fim, novo):
    """troca o trecho que comeca em `ini` (unico) e vai ate o comeco de `fim` (o primeiro depois de `ini`) por `novo`."""
    t = a.t
    assert t.count(ini) == 1, ("ancora inicial nao unica", ini[:80], t.count(ini))
    i = t.index(ini)
    j = t.index(fim, i + len(ini))
    a.t = t[:i] + novo + t[j:]


# ---------------------------------------------------------------- (1) o cabecalho
HEADER = """# A LEITURA da rodada v409 (molde: leitura_v408.py, que vem de leitura_v407.py, de leitura_v405.py, de leitura_v401.py e de leitura_v399.py FINAL): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v409, que aqui e' o proprio pacote).
# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e' digitado: tudo sai dos JSON, do core, do selo, do sidecar e do stdout do rito; os vereditos e os valores esperados da rodada v409 sao LIDOS de ESPERADOS_v409.json, de CANDIDATO_v409.json, de FLAGS_v409.json, de BUNDLE_v409.json, de delta_v409.py e do core da v408 SELADA (base_v408).
# v409 (A TRADUCAO AS CLASSES DE TURING, ordem do operador de 05/11/2026): o delta e' um BUNDLE PEQUENO de UM modulo novo de kernel em TGLExt/ (TraducaoTuring; o nome e os nomes das 62 declaracoes dados pela gerencia e RATIFICADOS pelo operador). Nao ha' registro por pedra (delta_v409.STONES == []).
# Os registros NOVOS do core sao TRES: UM com FUNCAO, traducao_turing_v409 (le do kernel do proprio rito as 62 ancoras, o modulo por sha256, as falas de 05/11 por sha256, as respostas do operador pelos teoremas da pedra; as 17 checagens com a instancia de brinquedo FIXA e beta em runtime; a escada exata e o gate),
# e DOIS por spec: cunhagens_v409 (as 10 falas do operador de 05/11 por sha256, de duas so' o trecho que a D59 deixa entrar; as erratas E24 a E26 e a errata ao lado dos pisos de kh_n1_cobertura_v408; as decisoes D55 a D60, em nome proprio da gerencia c1) e kh_n1_cobertura_v409 (a cobertura exata do Audit).
# O ALCANCE: P = nP e' teorema da TGL no modo selecao, RELATIVO AO LEITOR (o psion); a maquina sem leitor fica fora (a fita sem escala). NENHUMA CHAVE ANTIGA MUDA (delta_v409.CHAVES_V409 == []): a chave do lema (v407) segue LIDA do kernel do rito e le True; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA.
# O tetelestai_terminal_v408 e' HERDADO: o main da v409 segue rodando o bloco dele e ele segue selado (as 16 checagens; as 48 ancoras, os 4 modulos e as 71 bandeiras da v408 no kernel; a escada do contrato subida pela C12, veredito na troca dita); cunhagens_v408 ganha a errata E26 AO LADO e kh_n1_cobertura_v408 os pisos (h2 h3 h6 h8).
# O psion_canto_v407 e' HERDADO: segue selado (as 76 ancoras, os 9 modulos); cunhagens_v407 ganha AO LADO a errata da D57(d) (o pino do insumo do acervo da v407 passa a ser a copia purgada); kh_n1_cobertura_v407 segue igual a v408 selada. O fechamento_v406 e' HERDADO, igual a v408 selada.
# A TROCA DITA de veredito: so' numeros (a escada e a cobertura crescem com o bundle): ESPERADOS[troca_dita]. Os registros da v405, da v404, da v403, da v402, da v401 e da v399 sao RECRIADOS pelo rito e tem de seguir selados e iguais a v408 selada (base_v408), salvo a troca dita.
# O GATE NAO SE MOVE: o qg_closure do core e' IDENTICO ao da v408. O SIDECAR um_absoluto_selo_acom.json e' lido aqui (veredito ALL_OBJECTS_SEALED; os tres objetos; sem recusas; honestidade). A DIRECAO DO TESTEMUNHO segue conferida. As falas de 05/11 sao TODAS falas do operador.
# O QUADRO «O Teste da Unica Palavra» (v397) segue selado e igual. As linhas `[v399]` a `[v408]` do stdout (recriadas; os textos sao os que o um.py imprime: a [v406] diz «da v406», a [v407] «da v407», a [v408] «da v408») e a nova `[v409]` dizem os vereditos e os registros por spec selados; o AVISO de qualquer bloco reprova.
# A linha final do rito: o main imprime, por ultimo, a linha do sidecar (`[selo_acom] ... ALL_OBJECTS_SEALED ; objetos 3 ; recusas 0`), logo depois da do colapso tipado; a leitura exige as DUAS, nessa ordem.
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CONTRATO COM textos_v409.py (as CHAVES NOVAS ou MUDADAS de V na v409; "reg408c", "fun408c", "pedras_v408", "cunh408c" etc. sao NOMES HERDADOS do molde e continuam a significar os registros/pedras da v405 selada, recriados):
#   V['n_pedras'] = o numero de MODULOS NOVOS do kernel (1) e V['pedras'] = LISTA de dicts {'key'(None),'modulo','rel','sha16','sha256','bytes','bandeiras','decl'(None),'ok'}; V['ancoras'] {nome Lean: {...}} (as 62 da v409);
#   V['fecho'] o registro DESTA versao, traducao_turing_v409 {'registro','verdict','ok','sealed','n_checks'(17),'mech_ok','values','values_ok','beta_ok','ancoras_ok','stdout_ok','runtime_executed','does_not_gate_core','ancora_principal','ancoras_principais','ancoras_de_secao','chaves_antigas_que_mudam'([]),'acervo_ok','respostas_ok','instancia_ok'};
#   V['fecho408'] o registro HERDADO tetelestai_terminal_v408 (recriado) {'registro','verdict','ok','sealed','n_checks'(16),'mech_ok','values','values_ok','beta_ok','ancoras_ok','stdout_ok','runtime_executed','does_not_gate_core','ancora_principal','chaves_antigas_que_mudam'};
#   V['fecho407'] o registro HERDADO psion_canto_v407 (recriado) {...,'chaves_ok','elo_lido_do_kernel','lemma','pair_theorem','teste_d_so_citado'}; V['chaves407'] = as chaves dele; V['fecho406'] o fechamento_v406 HERDADO; V['chaves406'];
#   V['ancoras408'] as 48 do terminal; V['ancoras407'] as 76 do psion; V['ancoras406'] as 8 do fechamento; V['bundle408'] {'n'(4),'n_ok','ok'}; V['bundle407'] (9); V['bundle406'] (301); V['bandeiras408'] (as bandeiras True da v408 selada, todas True);
#   V['reg409'] DICT nome -> {'verdict','ok'} dos TRES registros NOVOS; V['registros_novos'] = esses 3 nomes (sorted); V['reg408d'] DICT dos TRES da v408 HERDADOS; V['reg407d'] DICT dos TRES da v407 HERDADOS; V['reg406d'] DICT dos TRES da v406 HERDADOS;
#   V['cunhagens'] (cunhagens_v409) {'n'(10),'ok','verbatim_ok','todas_do_operador','trechos_ok','n_trechos'(2),'erratas_ok','n_erratas'(4),'decisoes_ok','n_decisoes'(6),'leitura_ok','ressalvas_ok','kernel_ok','checks_ok','n_checks','moldura_ok','kh_ok'};
#   V['cunh408d'] (cunhagens_v408 e kh_n1_cobertura_v408 herdados, com a E26 e os pisos ao lado); V['cunh407d'] (cunhagens_v407 com a errata da D57(d); kh_n1_cobertura_v407 igual); V['cunh406d']; V['kh'] (kh_n1_cobertura_v409) {'decl','thm','fora','nao_lidas','verdict'}.
# (as linhas de stdout a conferir: `   [v409] o registro da traducao e os registros por spec da v409: traducao_turing=SELOU | specs: 2 (selados 2)` e o bloco A TRADUCAO AS CLASSES DE TURING: `  ancoras ok = 62/62 ; modulo do bundle ok = 1/1 ; bandeiras True = N/N ; escada = [..] ; gate = o mesmo da base`;
#  a do terminal HERDADO: `   [v408] o registro do terminal e os registros por spec da v408: tetelestai_terminal=SELOU | specs: 2 (selados 2)` e `  ancoras ok = 48/48 ; modulos do bundle ok = 4/4 ; bandeiras True = 71/71 ; escada = [..] ; gate = o mesmo da base`;
#  a do psion HERDADO: `   [v407] o registro do psion e do canto e os registros por spec da v407: psion_canto=SELOU | specs: 2 (selados 2)` e `  ancoras ok = 76/76 ; modulos do bundle ok = 9/9 ; bandeiras True = 98/98 ; chave do lema (lida do kernel) = True ; escada = [..] ; gate = o mesmo da base`;
#  as do fechamento HERDADO: `   [v406] o fechamento e os registros por spec da v406: fechamento=SELOU | specs: 2 (selados 2)` e `  ancoras ok = 8/8 ; modulos do bundle ok = 301/301 ; bandeiras True = 1794/1794 ; certificado habitado (lido do kernel) = True ; escada = [..] ; gate = o mesmo da base`;
"""
regiao("# [A ADAPTAR " + "v409]", "import glob, hashlib", "# [ADAPTADO v409, 05/11/2026, claude-construtor-v409 (fork A), a servico da gerencia c1] sobre a subida mecanica de rotulo da v408 FINAL (_bump_copia_v409.py; bump/pos_rito__leitura_v409.py.diff fica como registro), por _adapt_leitura_v409.py: o conteudo e' o da v409 (A TRADUCAO AS CLASSES DE TURING: bundle de 1 modulo, o registro com funcao traducao_turing_v409, o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 HERDADOS e recriados, nenhuma chave antiga muda); a gerencia revisa antes do rito (nao e' versao selada).\n" + HEADER)

# ---------------------------------------------------------------- (2) os registros
a.troca('REG_FUNCAO = ("tetelestai_terminal_v408",)   # o UNICO registro NOVO com FUNCAO (Tetelestai e\' o terminal); nao ha\' registro por pedra (modelo de bundle: delta_v409.STONES == [])',
        'REG_FUNCAO = ("traducao_turing_v409",)   # o UNICO registro NOVO com FUNCAO (a traducao as classes de Turing); nao ha\' registro por pedra (modelo de bundle: delta_v409.STONES == [])')
a.troca('REG_FIXOS = REG_FUNCAO + ("cunhagens_v408", "kh_n1_cobertura_v408")   # os TRES registros NOVOS do core v409 (um com FUNCAO, dois por spec)',
        'REG_FIXOS = REG_FUNCAO + ("cunhagens_v409", "kh_n1_cobertura_v409")   # os TRES registros NOVOS do core v409 (um com FUNCAO, dois por spec)')
a.troca_re(r'^REG_V408D = \("psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407"\)[^\n]*$',
           'REG_V408D = ("tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408")   # os TRES registros da v408 (um com FUNCAO, dois por spec): HERDADOS, RECRIADOS pelo rito da v409 (o main segue rodando o bloco do terminal), selados; o terminal carrega a escada (troca dita, C12); cunhagens_v408 ganha a errata E26 AO LADO e kh_n1_cobertura_v408 os pisos (h2 h3 h6 h8), assinados em nome proprio\n'
           'REG_V407D = ("psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407")   # os TRES registros da v407 (um com FUNCAO, dois por spec): HERDADOS, RECRIADOS pelo rito da v409, selados; o psion carrega a escada (troca dita); cunhagens_v407 ganha AO LADO a errata da D57(d) (o pino do acervo da v407 na copia purgada); kh_n1_cobertura_v407 segue igual a v408 selada')

# ---------------------------------------------------------------- (3) o stdout
a.troca("    if len([l for l in out.splitlines() if '[v408]' in l]) < 1:\n        P.append('o stdout nao tem a linha [v408]')\n",
        "    if len([l for l in out.splitlines() if '[v408]' in l]) < 1:\n        P.append('o stdout nao tem a linha [v408]')\n    if len([l for l in out.splitlines() if '[v409]' in l]) < 1:\n        P.append('o stdout nao tem a linha [v409]')\n")
a.troca("if '[v408] AVISO' in l or '[v407] AVISO' in l", "if '[v409] AVISO' in l or '[v408] AVISO' in l or '[v407] AVISO' in l")
a.troca("P.append('o stdout traz AVISO da v409 (o registro com funcao do terminal, os registros por spec da v409, o psion_canto_v407 e o fechamento_v406 herdados",
        "P.append('o stdout traz AVISO da v409 (o registro com funcao da traducao, os registros por spec da v409, o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados")
a.troca("R408DSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V408D[1:]}; R406DSPEC_", "R408DSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V408D[1:]}; R407DSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V407D[1:]}; R406DSPEC_")
a.troca("# os registros por spec da v405 (recriados), da v409 (novos), da v408 e da v406 (herdados)", "# os registros por spec da v405 (recriados), da v409 (novos), da v408, da v407 e da v406 (herdados)")
a.troca("(('fechamento_v406', _ev(ESP, 'fechamento_v406')), ('psion_canto_v407', _ev(ESP, 'psion_canto_v407')), ('tetelestai_terminal_v408', _ev(ESP, 'tetelestai_terminal_v408'))):",
        "(('fechamento_v406', _ev(ESP, 'fechamento_v406')), ('psion_canto_v407', _ev(ESP, 'psion_canto_v407')), ('tetelestai_terminal_v408', _ev(ESP, 'tetelestai_terminal_v408')), ('traducao_turing_v409', _ev(ESP, 'traducao_turing_v409'))):")
a.troca("m_s7 = re.search(r'\\[v407\\] o registro do psion e do canto e os registros por spec da v408: psion_canto=(\\S+) \\| specs: (\\d+) \\(selados (\\d+)\\)', out)   # a linha HERDADA da v408: o main da v409 segue rodando o bloco do psion e do canto; o texto e' o que o um.py imprime («da v408»)\n"
        "    if not m_s7 or m_s7.group(1) != 'SELOU' or m_s7.group(2) != m_s7.group(3) or int(m_s7.group(2)) != len(REG_V408D) - 1:\n"
        "        P.append('a linha [v407] do stdout (psion_canto SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V408D) - 1, repr(m_s7.groups() if m_s7 else 'ausente')))\n"
        "    m_s8t = re.search(r'\\[v408\\] o registro do terminal e os registros por spec da v409: tetelestai_terminal=(\\S+) \\| specs: (\\d+) \\(selados (\\d+)\\)', out)   # a linha NOVA da v409 (o texto e' o que o um.py imprime)\n"
        "    if not m_s8t or m_s8t.group(1) != 'SELOU' or m_s8t.group(2) != m_s8t.group(3) or int(m_s8t.group(2)) != len(REG_FIXOS) - 1:\n"
        "        P.append('a linha [v408] do stdout (tetelestai_terminal SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_FIXOS) - 1, repr(m_s8t.groups() if m_s8t else 'ausente')))\n",
        "m_s7 = re.search(r'\\[v407\\] o registro do psion e do canto e os registros por spec da v407: psion_canto=(\\S+) \\| specs: (\\d+) \\(selados (\\d+)\\)', out)   # a linha HERDADA da v407: o main da v409 segue rodando o bloco do psion e do canto; o texto e' o que o um.py imprime («da v407»)\n"
        "    if not m_s7 or m_s7.group(1) != 'SELOU' or m_s7.group(2) != m_s7.group(3) or int(m_s7.group(2)) != len(REG_V407D) - 1:\n"
        "        P.append('a linha [v407] do stdout (psion_canto SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V407D) - 1, repr(m_s7.groups() if m_s7 else 'ausente')))\n"
        "    m_s8t = re.search(r'\\[v408\\] o registro do terminal e os registros por spec da v408: tetelestai_terminal=(\\S+) \\| specs: (\\d+) \\(selados (\\d+)\\)', out)   # a linha HERDADA da v408 (o texto e' o que o um.py imprime: «da v408»)\n"
        "    if not m_s8t or m_s8t.group(1) != 'SELOU' or m_s8t.group(2) != m_s8t.group(3) or int(m_s8t.group(2)) != len(REG_V408D) - 1:\n"
        "        P.append('a linha [v408] do stdout (tetelestai_terminal SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V408D) - 1, repr(m_s8t.groups() if m_s8t else 'ausente')))\n"
        "    m_s9t = re.search(r'\\[v409\\] o registro da traducao e os registros por spec da v409: traducao_turing=(\\S+) \\| specs: (\\d+) \\(selados (\\d+)\\)', out)   # a linha NOVA da v409 (o texto e' o que o um.py imprime)\n"
        "    if not m_s9t or m_s9t.group(1) != 'SELOU' or m_s9t.group(2) != m_s9t.group(3) or int(m_s9t.group(2)) != len(REG_FIXOS) - 1:\n"
        "        P.append('a linha [v409] do stdout (traducao_turing SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_FIXOS) - 1, repr(m_s9t.groups() if m_s9t else 'ausente')))\n")
# a conferencia do rito
a.troca("('veredito_tetelestai_terminal', _ev(ESP, 'tetelestai_terminal_v408'), 'tetelestai_terminal_v408'), ('veredito_psion_herdado'",
        "('veredito_traducao_turing', _ev(ESP, 'traducao_turing_v409'), 'traducao_turing_v409'), ('veredito_tetelestai_terminal', _ev(ESP, 'tetelestai_terminal_v408'), 'tetelestai_terminal_v408'), ('veredito_psion_herdado'")

# ---------------------------------------------------------------- (4) os registros herdados: v408 (terminal) e v407 (psion)
VELHO_408D = """    V['reg408d'] = {}
    for k in REG_V408D:    # os TRES registros da v408 (HERDADOS) sao RECRIADOS pelo rito: seguem no core, selados e de veredito igual ao esperado (o da v408 selada, ou o do ensaio a seco se na troca dita: o psion carrega a escada); o conteudo (checagens, erratas) e' conferido adiante
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg408d'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        if not _ev(ESP, k) or r.get('verdict') != _ev(ESP, k):
            P.append('%s: o veredito do rito difere do esperado (ESPERADOS[vereditos_v408], ou o do ensaio a seco se na troca dita)' % k)
"""
NOVO_408D = VELHO_408D.replace("(o da v408 selada, ou o do ensaio a seco se na troca dita: o psion carrega a escada)", "(o da v408 selada, ou o do ensaio a seco se na troca dita: o terminal carrega a escada)") + VELHO_408D.replace("reg408d", "reg407d").replace("REG_V408D", "REG_V407D").replace("os TRES registros da v408 (HERDADOS)", "os TRES registros da v407 (HERDADOS)")
a.troca(VELHO_408D, NOVO_408D)

# ---------------------------------------------------------------- (5) os bundles e as ancoras herdadas
a.troca("    # v409: os 9 modulos novos de kernel (o BUNDLE PEQUENO)", "    # v409: o modulo novo de kernel (o BUNDLE PEQUENO, de UM modulo)")
a.troca("    for rel_ in DL_.BUNDLE_RELS:    # a ordem do bundle: TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP (DL.BUNDLE_RELS)", "    for rel_ in DL_.BUNDLE_RELS:    # o bundle: TraducaoTuring (DL.BUNDLE_RELS)")
a.troca("    # o bundle da v408 (os 9 modulos de TGLExt/) e o da v406 (os 301 de TGLExt/F1Fecho394) SEGUEM no kernel do Nos e no hash formal do rito com o MESMO sha256 (a v409 nao reescreve a v408 nem a v406; registro)",
        "    # o bundle da v408 (os 4 modulos de TGLExt/), o da v407 (os 9 de TGLExt/) e o da v406 (os 301 de TGLExt/F1Fecho394) SEGUEM no kernel do Nos e no hash formal do rito com o MESMO sha256 (a v409 nao reescreve as versoes anteriores; registro)")
a.troca("for bk_, bch_, bn_, bdesc_ in (('bundle408', 'bundle_v408_sha256', DL_.D7.N_BUNDLE, 'v408 (%d modulos de TGLExt/)'), ('bundle406', 'bundle_v406_sha256', DL_.D6.N_BUNDLE, 'v406 (%d modulos de TGLExt/F1Fecho394)')):",
        "for bk_, bch_, bn_, bdesc_ in (('bundle408', 'bundle_v408_sha256', DL_.D8.N_BUNDLE, 'v408 (%d modulos de TGLExt/)'), ('bundle407', 'bundle_v407_sha256', DL_.D7.N_BUNDLE, 'v407 (%d modulos de TGLExt/)'), ('bundle406', 'bundle_v406_sha256', DL_.D6.N_BUNDLE, 'v406 (%d modulos de TGLExt/F1Fecho394)')):")
a.troca("    # v409: as 76 ANCORAS das nove pedras e as 98 bandeiras do bundle no kernel do rito", "    # v409: as 62 ANCORAS da pedra e as bandeiras do bundle no kernel do rito")
a.troca("    # as 76 ancoras do psion_canto_v407 (HERDADO), as OITO do fechamento_v406 (HERDADO) e as bandeiras True da v408: seguem no kernel do rito (a v409 so' acrescenta; ESPERADOS[estrelas_v408], [estrelas_v406] e [flags_true_v408], lidos do ensaio a seco, nunca digitados)\n"
        "    for ak_, ach_, aesp_, adesc_ in (('ancoras408', 'estrelas_v408', DL_.D7.ANCORAS, 'as ancoras do psion_canto_v407 (herdadas)'), ('ancoras406', 'estrelas_v406', DL_.D6.ANCORAS, 'as oito ancoras do fechamento_v406 (herdadas)')):",
        "    # as 48 ancoras do tetelestai_terminal_v408 (HERDADO), as 76 do psion_canto_v407 (HERDADO), as OITO do fechamento_v406 (HERDADO) e as bandeiras True da v408 selada: seguem no kernel do rito (a v409 so' acrescenta; ESPERADOS[estrelas_v408], [estrelas_v407], [estrelas_v406] e [flags_true_v408], lidos do ensaio a seco, nunca digitados)\n"
        "    for ak_, ach_, aesp_, adesc_ in (('ancoras408', 'estrelas_v408', DL_.D8.ANCORAS, 'as ancoras do tetelestai_terminal_v408 (herdadas)'), ('ancoras407', 'estrelas_v407', DL_.D7.ANCORAS, 'as ancoras do psion_canto_v407 (herdadas)'), ('ancoras406', 'estrelas_v406', DL_.D6.ANCORAS, 'as oito ancoras do fechamento_v406 (herdadas)')):")

# ---------------------------------------------------------------- (6) os blocos dos registros com funcao: a traducao (NOVO), o terminal (HERDADO), o psion (HERDADO)
TRADUCAO = r"""    # o registro traducao_turing_v409 (UM registro NOVO com FUNCAO, SEM pedra por registro): as 17 checagens, os valores (as 62 ancoras, o modulo, as bandeiras, a escada, o gate, a instancia de brinquedo) == ESPERADOS[registros_funcao_v409], a ancora principal e as de secao, NENHUMA chave antiga muda, o acervo da v407 repinado na copia purgada (D57d), as respostas do operador conferidas, o beta em runtime, as ressalvas, as 10 falas por sha256 e a linha do bloco no stdout
    tt_ = core.get(DL_.FECHO_REGISTRO) or {}; tt_m_ = tt_.get('mechanics') or {}; tt_v_ = tt_.get('values') or {}; ETT_ = (ESP.get('registros_funcao_v409') or {}).get('traducao_turing') or {}; ac_ = tt_.get('acervo_v407_repinado') or {}; rs_ = tt_v_.get('respostas') or {}
    tt_mech_ok_ = bool(tt_m_.get('passed') is True and tt_m_.get('n_checks') == DL_.N_CHECKS_FECHO == ETT_.get('n_checks') == len(tt_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (tt_m_.get('checks') or [])))
    tt_values_ok_ = bool(tt_v_.get('n_ancoras_ok') == tt_v_.get('n_ancoras') == len(DL_.ANCORAS) == len(ESP.get('estrelas_v409') or {}) and tt_v_.get('n_modulos_ok') == tt_v_.get('n_modulos') == DL_.N_BUNDLE and tt_v_.get('n_flags_true') == tt_v_.get('n_flags') == FJ_['n_flags'] and tt_v_.get('escada') == [ESP['escada'][1]] * 3
                         and tt_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v408') == selo.get('qg_closure_verdict') and tt_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA) and tt_v_.get('ressalvas') == list(DL_.RESSALVAS_V409) and list(tt_.get('ressalvas') or []) == list(DL_.RESSALVAS_V409)
                         and (tt_v_.get('fica_aberto') or {}) == {'par_na_face_de_fock': DL_.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, 'omega_do_psion_e_o_uniforme': DL_.FICA_ABERTO_OMEGA_UNIFORME, 'maquina_sem_leitor': DL_.FICA_ABERTO_MAQUINA_SEM_LEITOR, 'ponte_bell_tt': DL_.FICA_ABERTO_PONTE_BELL_TT}
                         and bool(ETT_.get('values')) and _feq({kk_: tt_v_.get(kk_) for kk_ in ETT_['values']}, ETT_['values']))
    is_ = tt_v_.get('instancia_sim') or {}; in_ = tt_v_.get('instancia_nao') or {}
    tt_inst_ok_ = bool(tt_.get('instancia_sim') == dict(DL_.INSTANCIA_SIM) and tt_.get('instancia_nao') == dict(DL_.INSTANCIA_NAO) and is_.get('n') == DL_.INSTANCIA_SIM['n'] and is_.get('atribuicoes') == 2 ** DL_.INSTANCIA_SIM['n'] and isinstance(is_.get('solucoes'), int) and is_['solucoes'] >= 1
                       and in_.get('solucoes') == 0 and in_.get('atribuicoes') == 2 ** DL_.INSTANCIA_NAO['n'])
    tt_anc_prin_ok_ = bool(tt_.get('ancora_principal') == DL_.ANCORA_PRINCIPAL and list(tt_.get('ancoras_principais') or []) == list(DL_.ANCORAS_PRINCIPAIS) and list(tt_.get('ancoras_de_secao') or []) == list(DL_.ANCORAS_DE_SECAO) and all(a_ in DL_.ANCORAS for a_ in DL_.ANCORAS_PRINCIPAIS)
                           and list(tt_.get('pedras') or []) == [p_['name'] for p_ in DL_.PEDRAS_V409] and tt_.get('nomes_ratificados') == dict(DL_.NOMES_RATIFICADOS))
    tt_chaves_ok_ = bool(tt_.get('chaves_antigas_que_mudam') == [] and list(DL_.CHAVES_V409) == [] and (core.get('testemunha_estatica_v396') or {}).get('fock_face', {}).get('linked_to_the_corner_by_a_lemma') is True)
    f407_ = ((core.get('cunhagens_v407') or {}).get('fontes') or [])
    f407_ac_ = [f_ for f_ in f407_ if isinstance(f_, dict) and f_.get('chave') == DL_.CHAVE_ACERVO_V407]
    tt_ac_ok_ = bool(ac_.get('chave') == DL_.CHAVE_ACERVO_V407 and ac_.get('sha256') == DL_.PURGADO_SHA256 and ac_.get('integra_sha16') == DL_.ORIGEM_PURGA_SHA16_DA_ORDEM and ac_.get('integra_pinada') is False and ac_.get('integra_fora_do_espelho') is True
                     and len(f407_ac_) == 1 and f407_ac_[0].get('sha256') == DL_.PURGADO_SHA256 and f407_ac_[0].get('ok') is True and not str(f407_ac_[0].get('sha256') or '').startswith(DL_.ORIGEM_PURGA_SHA16_DA_ORDEM))
    tt_resp_ok_ = bool(rs_ and set(rs_) == {r_['id'] for r_ in DL_.RESPOSTAS_DO_OPERADOR} and all((v_ is True) or (isinstance(v_, dict) and v_.get('ok') is True) for v_ in rs_.values()) and tt_v_.get('respostas_ok') is True)
    tt_beta_ok_ = bool(tt_.get('beta_ok') is True and isinstance(tt_v_.get('beta'), float) and isinstance(b0_, float) and abs(tt_v_['beta'] - b0_) <= 1e-9 * abs(b0_))
    tt_anc_ok_ = bool(len(tt_.get('anchors') or {}) == len(DL_.ANCORAS) and all(a_ is True for a_ in (tt_.get('anchors') or {}).values()) and set(tt_.get('anchors') or {}) == set(DL_.ANCORAS) == set(tt_v_.get('ancoras') or {}) and all((a_ or {}).get('ok') is True for a_ in (tt_v_.get('ancoras') or {}).values()))
    m_tt_ = re.search(r'ancoras ok = (\d+)/(\d+) ; modulo do bundle ok = (\d+)/(\d+) ; bandeiras True = (\d+)/(\d+) ; escada = (\[.*?\]) ; gate = (.*)$', out, flags=re.M)   # a linha do bloco A TRADUCAO AS CLASSES DE TURING («modulo», no singular; as dos blocos herdados dizem «modulos»)
    tt_std_ok_ = bool(m_tt_ and m_tt_.group(1) == str(tt_v_.get('n_ancoras_ok')) and m_tt_.group(2) == str(tt_v_.get('n_ancoras')) and m_tt_.group(3) == str(tt_v_.get('n_modulos_ok')) and m_tt_.group(4) == str(tt_v_.get('n_modulos')) and m_tt_.group(5) == str(tt_v_.get('n_flags_true'))
                      and m_tt_.group(6) == str(tt_v_.get('n_flags')) and m_tt_.group(7) == str(tt_v_.get('escada')) and m_tt_.group(8).strip() == 'o mesmo da base')
    tt_ch_ = {os.path.basename(p_): DL_.VERBATIM_CHAVE_PREFIXO_V409 + hashlib.sha256(open(p_, 'rb').read()).hexdigest()[:16] for p_ in DL_.VERBATIM_ORIGEM_V409}   # as inscricoes do REGISTRO sao as falas do contrato (todas as 10 de 05/11), com a ordem da traducao e a da v409 obrigatorias
    tt_ins_ok_ = bool(tt_.get('inscriptions') and set(tt_['inscriptions']) == set(tt_ch_.values()) and {tt_ch_[DL_.N_ORDEM_V409], tt_ch_[DL_.N_ORDEM_TRADUCAO]} <= set(tt_['inscriptions']) and all(v_ is True for v_ in tt_['inscriptions'].values()))
    tt_alc_ok_ = bool((tt_.get('alcance') or {}).get('frase') == DL_.FRASE_D56_PT and (tt_.get('alcance') or {}).get('qualificador') == DL_.FRASE_QUALIFICADOR_PT)
    tt_ok_ = bool(tt_.get('all_verified') is True and tt_.get('does_not_gate_core') is True and tt_.get('runtime_executed') is True and tt_.get('exact_ladder') is True and tt_.get('embedded_sources_ok') is True and tt_.get('embedded_sources_n_ok') == DL_.N_BUNDLE
                  and bool(_ev(ESP, DL_.FECHO_REGISTRO)) and tt_.get('verdict') == _ev(ESP, DL_.FECHO_REGISTRO) == ETT_.get('verdict') and str(tt_.get('verdict') or '').startswith(DL_.VEREDITO_OK_PREFIXO) and str(tt_.get('verdict') or '').endswith(DL_.VEREDITO_SUFIXO)
                  and not any(t_ in str(tt_.get('verdict') or '') for t_ in DL_.TOKENS_PROIBIDOS_V409)
                  and tt_mech_ok_ and tt_values_ok_ and tt_inst_ok_ and tt_anc_prin_ok_ and tt_chaves_ok_ and tt_ac_ok_ and tt_resp_ok_ and tt_beta_ok_ and tt_anc_ok_ and tt_ins_ok_ and tt_alc_ok_ and V['bandeiras']['ok'] and all(a_['ok'] for a_ in V['ancoras'].values()) and tt_std_ok_ and not tt_.get('guarda_violacoes')
                  and not GUARDA.search(str(tt_.get('verdict') or '')))
    V['fecho'] = {'registro': DL_.FECHO_REGISTRO, 'verdict': tt_.get('verdict'), 'ok': tt_.get('all_verified'), 'sealed': tt_ok_, 'n_checks': tt_m_.get('n_checks'), 'mech_ok': tt_mech_ok_, 'values': tt_v_, 'values_ok': tt_values_ok_, 'beta_ok': tt_beta_ok_, 'ancoras_ok': tt_anc_ok_, 'stdout_ok': tt_std_ok_,
                  'runtime_executed': tt_.get('runtime_executed'), 'does_not_gate_core': tt_.get('does_not_gate_core'), 'ancora_principal': tt_.get('ancora_principal'), 'ancoras_principais': list(tt_.get('ancoras_principais') or []), 'ancoras_de_secao': list(tt_.get('ancoras_de_secao') or []),
                  'chaves_antigas_que_mudam': tt_.get('chaves_antigas_que_mudam'), 'acervo_ok': tt_ac_ok_, 'respostas_ok': tt_resp_ok_, 'instancia_ok': tt_inst_ok_, 'alcance_ok': tt_alc_ok_}
    if not tt_ok_:
        P.append('traducao_turing_v409 nao selou inteiro (selo, as %s checagens do registro, valores [%s ancoras, %s modulo, %s bandeiras, escada, gate, a instancia de brinquedo] == os de FLAGS/BUNDLE/ESPERADOS, a ancora principal e as de secao, NENHUMA chave antiga muda [a do lema segue True], o acervo da v407 repinado na copia purgada [D57d], as respostas do operador conferidas nos teoremas, beta == alfa x raiz de e do core, '
                 'as ressalvas, as %s falas por sha256, o alcance relativo ao leitor, nenhum token proibido no veredito, a linha do bloco A TRADUCAO AS CLASSES DE TURING no stdout, nao move o gate): ver o registro no core' % (DL_.N_CHECKS_FECHO, len(DL_.ANCORAS), DL_.N_BUNDLE, FJ_['n_flags'], DL_.N_FALAS_V409))
    # o registro tetelestai_terminal_v408 (HERDADO da v408, RECRIADO pelo rito da v409; a escada do contrato subida pela C12, veredito na troca dita): segue SELADO; as 16 checagens, os valores (as 48 ancoras, os 4 modulos, as 71 bandeiras, a escada, o gate) == ESPERADOS[registros_funcao_v408], NENHUMA chave antiga muda, o insumo purgado (E23 da v408), as respostas do operador de 04/11, o beta em runtime, as ressalvas da v408 e a linha do bloco no stdout
    t8_ = core.get('tetelestai_terminal_v408') or {}; t8_m_ = t8_.get('mechanics') or {}; t8_v_ = t8_.get('values') or {}; ET8_ = (ESP.get('registros_funcao_v408') or {}).get('tetelestai_terminal') or {}; ip8_ = t8_.get('insumo_purgado') or {}; ip8v_ = t8_v_.get('insumo_purgado') or {}; rs8_ = t8_v_.get('respostas') or {}
    N8F_ = (ET8_.get('values') or {}).get('n_flags')   # o numero das bandeiras do bundle da v408 (71): lido de ESPERADOS[registros_funcao_v408] (o ensaio a seco), nunca digitado
    t8_mech_ok_ = bool(t8_m_.get('passed') is True and t8_m_.get('n_checks') == DL_.D8.N_CHECKS_FECHO == ET8_.get('n_checks') == len(t8_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (t8_m_.get('checks') or [])))
    t8_values_ok_ = bool(t8_v_.get('n_ancoras_ok') == t8_v_.get('n_ancoras') == len(DL_.D8.ANCORAS) and bool(DL_.D8.ANCORAS) and t8_v_.get('n_modulos_ok') == t8_v_.get('n_modulos') == DL_.D8.N_BUNDLE and t8_v_.get('n_flags_true') == t8_v_.get('n_flags') == N8F_ and isinstance(N8F_, int) and t8_v_.get('escada') == [ESP['escada'][1]] * 3
                         and t8_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v408') == selo.get('qg_closure_verdict') and t8_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA) and t8_v_.get('ressalvas') == list(DL_.D8.RESSALVAS_V408) and list(t8_.get('ressalvas') or []) == list(DL_.D8.RESSALVAS_V408)
                         and bool(ET8_.get('values')) and _feq({kk_: t8_v_.get(kk_) for kk_ in ET8_['values']}, ET8_['values']))
    t8_ip_ok_ = bool(ip8v_.get('ok') is True and ip8v_.get('sha256') == ip8_.get('sha256') == DL_.D8.PURGADO_SHA256 and ip8v_.get('integra_nao_pinada') is True and ip8_.get('integra_pinada') is False and ip8_.get('integra_fora_do_espelho') is True)
    t8_resp_ok_ = bool(rs8_ and set(rs8_) == {r_['id'] for r_ in DL_.D8.RESPOSTAS_DO_OPERADOR} and all(v_ is True for v_ in rs8_.values()) and t8_v_.get('respostas_ok') is True)
    t8_beta_ok_ = bool(t8_.get('beta_ok') is True and isinstance(t8_v_.get('beta'), float) and isinstance(b0_, float) and abs(t8_v_['beta'] - b0_) <= 1e-9 * abs(b0_))
    t8_anc_ok_ = bool(len(t8_.get('anchors') or {}) == len(DL_.D8.ANCORAS) and all(a_ is True for a_ in (t8_.get('anchors') or {}).values()) and set(t8_.get('anchors') or {}) == set(DL_.D8.ANCORAS) == set(t8_v_.get('ancoras') or {}) and all((a_ or {}).get('ok') is True for a_ in (t8_v_.get('ancoras') or {}).values()))
    m_t8_ = re.search(r'ancoras ok = (\d+)/(\d+) ; modulos do bundle ok = (\d+)/(\d+) ; bandeiras True = (\d+)/(\d+) ; escada = (\[.*?\]) ; gate = (.*)$', out, flags=re.M)   # a linha do bloco TETELESTAI E' O TERMINAL (herdado): sem «chave do lema» e sem «certificado habitado»; «modulos» no plural (a da v409 diz «modulo»)
    t8_std_ok_ = bool(m_t8_ and m_t8_.group(1) == str(t8_v_.get('n_ancoras_ok')) and m_t8_.group(2) == str(t8_v_.get('n_ancoras')) and m_t8_.group(3) == str(t8_v_.get('n_modulos_ok')) and m_t8_.group(4) == str(t8_v_.get('n_modulos')) and m_t8_.group(5) == str(t8_v_.get('n_flags_true'))
                      and m_t8_.group(6) == str(t8_v_.get('n_flags')) and m_t8_.group(7) == str(t8_v_.get('escada')) and m_t8_.group(8).strip() == 'o mesmo da base')
    t8_ok_ = bool(t8_.get('all_verified') is True and t8_.get('does_not_gate_core') is True and t8_.get('runtime_executed') is True and t8_.get('exact_ladder') is True and t8_.get('embedded_sources_ok') is True and t8_.get('embedded_sources_n_ok') == DL_.D8.N_BUNDLE
                  and list(t8_.get('pedras') or []) == [p_['name'] for p_ in DL_.D8.PEDRAS_V408] and t8_.get('ancora_principal') == DL_.D8.ANCORA_PRINCIPAL and t8_.get('chaves_antigas_que_mudam') == []
                  and bool(_ev(ESP, 'tetelestai_terminal_v408')) and t8_.get('verdict') == _ev(ESP, 'tetelestai_terminal_v408') == ET8_.get('verdict')
                  and str(t8_.get('verdict') or '').startswith(DL_.D8.VEREDITO_OK_PREFIXO) and str(t8_.get('verdict') or '').endswith(DL_.D8.VEREDITO_SUFIXO)
                  and t8_mech_ok_ and t8_values_ok_ and t8_ip_ok_ and t8_resp_ok_ and t8_beta_ok_ and t8_anc_ok_ and V['bundle408']['ok'] and all(a_['ok'] for a_ in V['ancoras408'].values()) and t8_std_ok_ and not t8_.get('guarda_violacoes')
                  and not GUARDA.search(str(t8_.get('verdict') or '')))
    V['fecho408'] = {'registro': 'tetelestai_terminal_v408', 'verdict': t8_.get('verdict'), 'ok': t8_.get('all_verified'), 'sealed': t8_ok_, 'n_checks': t8_m_.get('n_checks'), 'mech_ok': t8_mech_ok_, 'values': t8_v_, 'values_ok': t8_values_ok_, 'beta_ok': t8_beta_ok_, 'ancoras_ok': t8_anc_ok_,
                     'stdout_ok': t8_std_ok_, 'runtime_executed': t8_.get('runtime_executed'), 'does_not_gate_core': t8_.get('does_not_gate_core'), 'ancora_principal': t8_.get('ancora_principal'), 'chaves_antigas_que_mudam': t8_.get('chaves_antigas_que_mudam'), 'insumo_purgado_ok': t8_ip_ok_, 'respostas_ok': t8_resp_ok_}
    if not t8_ok_:
        P.append('tetelestai_terminal_v408 (HERDADO, recriado) nao selou inteiro (selo, as %s checagens do registro, valores [%s ancoras, %s modulos, as bandeiras da v408, escada, gate] == os de ESPERADOS[registros_funcao_v408], NENHUMA chave antiga muda, o insumo purgado por sha256 [E23 da v408], as respostas do operador de 04/11, beta == alfa x raiz de e do core, '
                 'as ressalvas da v408, o bundle da v408 [%s], a linha do bloco TETELESTAI E O TERMINAL no stdout, nao move o gate): ver o registro no core' % (DL_.D8.N_CHECKS_FECHO, len(DL_.D8.ANCORAS), DL_.D8.N_BUNDLE, DL_.D8.N_BUNDLE))
"""
regiao("    # o registro tetelestai_terminal_v408 (UM registro NOVO com FUNCAO, SEM pedra por registro)", "    # o registro psion_canto_v407 (HERDADO da v408, RECRIADO pelo rito da v409;", TRADUCAO)
# o bloco do psion: herdado da v407 (a subida mecanica o rotulara 408)
a.troca("    # o registro psion_canto_v407 (HERDADO da v408, RECRIADO pelo rito da v409; a escada do contrato subida pela C12, veredito na troca dita): segue SELADO; as 16 checagens, os valores (as 76 ancoras, os 9 modulos, as 98 bandeiras, a escada, o gate) == ESPERADOS[registros_funcao_v408],",
        "    # o registro psion_canto_v407 (HERDADO da v407, RECRIADO pelo rito da v409; a escada do contrato subida pela C12, veredito na troca dita): segue SELADO; as 16 checagens, os valores (as 76 ancoras, os 9 modulos, as 98 bandeiras, a escada, o gate) == ESPERADOS[registros_funcao_v407],")
a.troca("EPC_ = (ESP.get('registros_funcao_v408') or {}).get('psion_canto') or {}", "EPC_ = (ESP.get('registros_funcao_v407') or {}).get('psion_canto') or {}")
a.troca("    N7F_ = (EPC_.get('values') or {}).get('n_flags')   # o numero das bandeiras do bundle da v408 (98): lido de ESPERADOS[registros_funcao_v408]", "    N7F_ = (EPC_.get('values') or {}).get('n_flags')   # o numero das bandeiras do bundle da v407 (98): lido de ESPERADOS[registros_funcao_v407]")
a.troca("pc_v_.get('ressalvas') == list(DL_.D7.RESSALVAS_V408) and list(pc_.get('ressalvas') or []) == list(DL_.D7.RESSALVAS_V408)", "pc_v_.get('ressalvas') == list(DL_.D7.RESSALVAS_V407) and list(pc_.get('ressalvas') or []) == list(DL_.D7.RESSALVAS_V407)")
a.troca("bool(ESP.get('chaves_v408_esperadas')) and _feq(pc_k_, ESP.get('chaves_v408_esperadas'))", "bool(ESP.get('chaves_v407_esperadas')) and _feq(pc_k_, ESP.get('chaves_v407_esperadas'))")
a.troca("pc_ins_ok_ = bool(len(pc_.get('inscriptions') or {}) == len(DL_.D7.VERBATIM_ORIGEM_V408)", "pc_ins_ok_ = bool(len(pc_.get('inscriptions') or {}) == len(DL_.D7.VERBATIM_ORIGEM_V407)")
a.troca("list(pc_.get('pedras') or []) == [p_['name'] for p_ in DL_.D7.PEDRAS_V408]", "list(pc_.get('pedras') or []) == [p_['name'] for p_ in DL_.D7.PEDRAS_V407]")
a.troca("and pc_mech_ok_ and pc_values_ok_ and pc_chaves_ok_ and pc_beta_ok_ and pc_anc_ok_ and pc_ins_ok_ and V['bundle408']['ok'] and all(a_['ok'] for a_ in V['ancoras408'].values()) and pc_std_ok_",
        "and pc_mech_ok_ and pc_values_ok_ and pc_chaves_ok_ and pc_beta_ok_ and pc_anc_ok_ and pc_ins_ok_ and V['bundle407']['ok'] and all(a_['ok'] for a_ in V['ancoras407'].values()) and pc_std_ok_")
a.troca("    V['fecho408'] = {'registro': 'psion_canto_v407',", "    V['fecho407'] = {'registro': 'psion_canto_v407',")
a.troca("    V['chaves408'] = dict(pc_k_)", "    V['chaves407'] = dict(pc_k_)")
a.troca("P.append('psion_canto_v407 (HERDADO, recriado) nao selou inteiro (selo, as %s checagens do registro, valores [%s ancoras, %s modulos, as bandeiras da v408, escada, gate] == os de ESPERADOS[registros_funcao_v408],",
        "P.append('psion_canto_v407 (HERDADO, recriado) nao selou inteiro (selo, as %s checagens do registro, valores [%s ancoras, %s modulos, as bandeiras da v407, escada, gate] == os de ESPERADOS[registros_funcao_v407],")
a.troca("'as ressalvas da v408, as %s falas de 03/11 por sha256, o teste (d) so\\' citado, o bundle da v408 [%s], a linha do bloco O PSION, O CANTO E O PAR no stdout, nao move o gate): ver o registro no core' % (DL_.D7.N_CHECKS_FECHO, len(DL_.D7.ANCORAS), DL_.D7.N_BUNDLE, len(DL_.D7.VERBATIM_ORIGEM_V408), DL_.D7.N_BUNDLE))",
        "'as ressalvas da v407, as %s falas de 03/11 por sha256, o teste (d) so\\' citado, o bundle da v407 [%s], a linha do bloco O PSION, O CANTO E O PAR no stdout, nao move o gate): ver o registro no core' % (DL_.D7.N_CHECKS_FECHO, len(DL_.D7.ANCORAS), DL_.D7.N_BUNDLE, len(DL_.D7.VERBATIM_ORIGEM_V407), DL_.D7.N_BUNDLE))")

# ---------------------------------------------------------------- (7) o selo primario: os resumos (registros_v409 novo; a lista dos registros com funcao inclui o terminal herdado)
a.troca("sreg7_ = selo.get('registros_v407') or {}; sreg8_ = selo.get('registros_v408') or {}", "sreg7_ = selo.get('registros_v407') or {}; sreg8_ = selo.get('registros_v408') or {}; sreg9_ = selo.get('registros_v409') or {}")
a.troca("+ tuple(FUN_V408C.values()) + ('fechamento_v406', 'psion_canto_v407'))", "+ tuple(FUN_V408C.values()) + ('fechamento_v406', 'psion_canto_v407', 'tetelestai_terminal_v408'))")
a.troca("                       and bool(R408DSPEC_) and all((sreg7_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg7_.get(k_) or {}).get('verdict')) and (sreg7_.get(k_) or {}).get('all_verified') is True for k_ in R408DSPEC_)\n"
        "                       and bool(R409SPEC_) and all((sreg8_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg8_.get(k_) or {}).get('verdict')) and (sreg8_.get(k_) or {}).get('all_verified') is True for k_ in R409SPEC_))",
        "                       and bool(R407DSPEC_) and all((sreg7_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg7_.get(k_) or {}).get('verdict')) and (sreg7_.get(k_) or {}).get('all_verified') is True for k_ in R407DSPEC_)\n"
        "                       and bool(R408DSPEC_) and all((sreg8_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg8_.get(k_) or {}).get('verdict')) and (sreg8_.get(k_) or {}).get('all_verified') is True for k_ in R408DSPEC_)\n"
        "                       and bool(R409SPEC_) and all((sreg9_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg9_.get(k_) or {}).get('verdict')) and (sreg9_.get(k_) or {}).get('all_verified') is True for k_ in R409SPEC_))")

# ---------------------------------------------------------------- (8) cunhagens_v409 (NOVO) e os herdados
CUNH = r"""    # cunhagens_v409 e kh_n1_cobertura_v409 (os DOIS registros NOVOS por spec): as 10 falas do operador de 05/11 por sha256 (embedded_ok), todas do operador (de DUAS, so' o trecho que a D59 deixa entrar: a chave e' o sha16 do arquivo inteiro, o texto embutido e' o trecho); as erratas E24 a E26 mais a errata ao lado dos pisos de kh_n1_cobertura_v408 (gerencia c1, em nome proprio: DL.ASSINA); as decisoes D55 a D60; a leitura [INPUT] e as ressalvas; os nomes ratificados; o que fica citado so' por sha16; a MOLDURA (nenhuma frase proibida nos tres registros novos)
    cu = core.get(DL_.CUNHAGENS_REGISTRO) or {}; kh = core.get(DL_.KH_REGISTRO) or {}
    cx_ = cu.get('extras') or {}; vb_ = cu.get('verbatim') or {}; ec_ = CM.get('cunhagens') or {}; pre_ = DL_.VERBATIM_CHAVE_PREFIXO_V409
    todas_op_ = bool(ec_ and all(str((ec_[k_] or {}).get('nome', '')).startswith('OPERADOR_05nov_') for k_ in ec_) and not any(str(v_.get('papel', '')).startswith('leitura da gerencia') for v_ in ec_.values()) and all((ec_[k_] or {}).get('autor') == 'operador' for k_ in ec_)
                     and bool(cx_.get('autores')) and all(a_ == 'operador' for a_ in (cx_.get('autores') or {}).values()))
    trechos_ = {k_ for k_, v_ in ec_.items() if (v_ or {}).get('sha256_arquivo_inteiro')}
    trechos_ok_ = bool(len(trechos_) == len(DL_.VERBATIM_SO_O_TRECHO) == 2 and all(str((ec_[k_] or {}).get('sha256_arquivo_inteiro') or '')[:16] == k_[len(pre_):] for k_ in trechos_)
                       and all(str((ec_[k_] or {}).get('sha256') or '')[:16] == k_[len(pre_):] for k_ in ec_ if k_ not in trechos_) and len(cx_.get('autores') or {}) == len(ec_)
                       and not any(x_ in json.dumps(cu, ensure_ascii=False).lower() for x_ in ('kimi', 'milenio', 'milênio', 'navier', 'lindão')))   # D59: o que fica fora nao entra no registro
    verb_ok_ = bool(ec_) and len(ec_) == len(vb_) == len(DL_.VERBATIM_ORIGEM_V409) == DL_.N_FALAS_V409 and set(vb_) == set(ec_) and all((vb_[k_] or {}).get('sha256') == ec_[k_]['sha256'] and (vb_[k_] or {}).get('embedded_ok') is True for k_ in ec_)
    pares_ok_ = all(isinstance(x_, list) and len(x_) == 2 and x_[0] == x_[1] for x_ in (cu.get('kernel') or {}).values()) and bool(cu.get('kernel'))
    err_ = cu.get('erratas') or []; esp_err_ = list(DL_.ERRATAS_V409)
    erratas_ok_ = bool(esp_err_ and len(err_) == len(esp_err_) + 1 and all(e_.get('assinatura') == DL_.ASSINA for e_ in err_) and [e_.get('agora') for e_ in err_[:len(esp_err_)]] == esp_err_ and 'kh_n1_cobertura_v408' in str(err_[-1].get('ao_lado_de')) and cx_.get('assinatura_das_erratas') == DL_.ASSINA)
    dec_ = cx_.get('decisoes') or {}; exig_ = set(ESP.get('decisoes_v409_ids') or [])   # as decisoes desta versao (D55 a D60), lidas de ESPERADOS[decisoes_v409_ids]
    decisoes_ok_ = bool(exig_ and set(dec_) == exig_ == set(DL_.DECISOES_V409) and all(dec_.get(d_) == DL_.DECISOES.get(d_) and str(dec_.get(d_) or '').strip() for d_ in exig_))
    leitura_ok_ = bool(cx_.get('leituras') == DL_.LEITURA_V409 and 'INPUT' in str(DL_.LEITURA_V409.get('estatuto')) and len(cu.get('leituras_do_operador') or []) == len(DL_.FRASES_V409))
    ressalvas_ok_ = bool(cx_.get('ressalvas') == list(DL_.RESSALVAS_V409) and len(DL_.RESSALVAS_V409) >= 8)
    contagens_ok_ = bool(cx_.get('n_falas') == len(ec_) and cx_.get('n_bandeiras') == FJ_['n_flags'] and cx_.get('n_modulos') == DL_.N_BUNDLE)
    nomes_ok_ = bool(cx_.get('nomes_das_pedras') == dict(DL_.NOMES_RATIFICADOS) and cx_.get('falas_fora_do_desenho') == dict(DL_.VERBATIM_FORA_DO_DESENHO_V409) and bool(cx_.get('nao_pinados_citados_por_sha16')))
    checks_cu_ok_ = bool(cu.get('checks')) and all(c_.get('ok') is True for c_ in cu.get('checks'))
    import guarda_frases_v409 as GF_
    moldura_ok_ = bool(all(not GF_.violacoes(json.dumps({k_: (core.get(n_) or {}).get(k_) for k_ in ('verdict', 'estatuto', 'scope', 'limites', 'diz', 'nao_diz')}, ensure_ascii=False)) for n_ in REG_FIXOS) and (GF_.controle_negativo() or {}).get('ok') is True)
    kh_ok_ = bool(kh.get('all_verified') is True and kh.get('does_not_gate_core') is True and bool(_ev(ESP, DL_.KH_REGISTRO)) and kh.get('verdict') == _ev(ESP, DL_.KH_REGISTRO) and bool(kh.get('checks')) and all(c_.get('ok') is True for c_ in kh.get('checks')) and not GUARDA.search(str(kh.get('verdict') or '')))
    cu_ok_ = bool(verb_ok_ and checks_cu_ok_ and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and erratas_ok_ and decisoes_ok_ and leitura_ok_ and ressalvas_ok_ and contagens_ok_ and todas_op_ and trechos_ok_ and nomes_ok_ and moldura_ok_
                  and bool(_ev(ESP, DL_.CUNHAGENS_REGISTRO)) and cu.get('verdict') == _ev(ESP, DL_.CUNHAGENS_REGISTRO) and not GUARDA.search(str(cu.get('verdict') or '')))
    V['cunhagens'] = {'n': len(vb_), 'ok': cu_ok_, 'verbatim_ok': verb_ok_, 'todas_do_operador': todas_op_, 'trechos_ok': trechos_ok_, 'n_trechos': len(trechos_), 'checks_ok': checks_cu_ok_, 'n_checks': len(cu.get('checks') or []), 'verdict': cu.get('verdict'), 'kernel_ok': pares_ok_, 'erratas_ok': erratas_ok_, 'n_erratas': len(err_),
                      'decisoes_ok': decisoes_ok_, 'n_decisoes': len(dec_), 'leitura_ok': leitura_ok_, 'ressalvas_ok': ressalvas_ok_, 'contagens_ok': contagens_ok_, 'nomes_ok': nomes_ok_, 'moldura_ok': moldura_ok_, 'kh_ok': kh_ok_}
    if not (verb_ok_ and checks_cu_ok_ and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and contagens_ok_ and trechos_ok_ and nomes_ok_ and cu.get('verdict') == _ev(ESP, DL_.CUNHAGENS_REGISTRO)):
        P.append('cunhagens_v409: as inscricoes embutidas nao sao as de CANDIDATO_v409.json (sha256, embedded_ok, %d falas; as duas da D59 com o sha16 do arquivo inteiro na chave e o trecho que fica no sha256; nada do que fica fora no registro), ou as checagens do registro, ou as contagens, ou os nomes ratificados e o citado so\' por sha16, ou o veredito diferem do ensaio a seco' % DL_.N_FALAS_V409)
    if not todas_op_:
        P.append('cunhagens_v409: as inscricoes de 05/11 tem de ser TODAS falas do operador (OPERADOR_05nov_*): nesta versao nao ha inscricao da gerencia nem de autor misto')
    if not erratas_ok_:
        P.append('cunhagens_v409: as erratas E24 a E26 e a errata ao lado dos pisos de kh_n1_cobertura_v408 (assinadas pela gerencia c1, em nome proprio: DL.ASSINA) ausentes ou diferentes de delta_v409.ERRATAS_V409')
    if not decisoes_ok_:
        P.append('cunhagens_v409: as decisoes D55 a D60 da gerencia ausentes ou diferentes de delta_v409.DECISOES')
    if not (leitura_ok_ and ressalvas_ok_):
        P.append('cunhagens_v409: a leitura [INPUT] de 05/11 (estatutos), os trechos do operador ou as ressalvas ausentes ou diferentes de delta_v409 (LEITURA_V409, FRASES_V409, RESSALVAS_V409)')
    if not moldura_ok_:
        P.append('a MOLDURA falhou: alguma frase proibida num registro novo da v409 (guarda das frases) ou o controle negativo da guarda falhou')
    if not kh_ok_:
        P.append('kh_n1_cobertura_v409 nao selou como o ensaio a seco (selo, veredito, checagens, nao move o gate)')
    # cunhagens_v408 e kh_n1_cobertura_v408 (HERDADOS, RECRIADOS pelo rito da v409, por spec): iguais ao que a v408 SELOU (as 15 falas de 04/11 por sha256; as erratas E21 a E23 e a dos pisos; os extras intactos) MAIS uma errata AO LADO (E26 / os pisos h2 h3 h6 h8), assinada em nome proprio; o veredito e' o esperado
    cu8_ = core.get('cunhagens_v408') or {}; kh8_ = core.get('kh_n1_cobertura_v408') or {}; cu8b_ = _base_core(PK).get('cunhagens_v408') or {}; kh8b_ = _base_core(PK).get('kh_n1_cobertura_v408') or {}
    e8_ = cu8_.get('erratas') or []; e8b_ = cu8b_.get('erratas') or []; k8e_ = kh8_.get('erratas') or []; k8eb_ = kh8b_.get('erratas') or []
    cu8_ok_ = bool(cu8_.get('all_verified') is True and cu8_.get('does_not_gate_core') is True and bool(cu8b_) and bool(cu8_.get('verbatim')) and _feq(cu8_.get('verbatim'), cu8b_.get('verbatim')) and len(cu8_.get('verbatim') or {}) == len(DL_.D8.VERBATIM_ORIGEM_V408) and all((v_ or {}).get('embedded_ok') is True for v_ in (cu8_.get('verbatim') or {}).values())
                   and _feq(cu8_.get('extras'), cu8b_.get('extras')) and len(e8_) == len(e8b_) + 1 and _feq(e8_[:len(e8b_)], e8b_) and e8_[-1].get('agora') == DL_.ERRATA_E26 and e8_[-1].get('assinatura') == DL_.ASSINA
                   and bool(cu8_.get('checks')) and all(c_.get('ok') is True for c_ in cu8_.get('checks')) and cu8_.get('verdict') == _ev(ESP, 'cunhagens_v408') and not GUARDA.search(str(cu8_.get('verdict') or '')))
    kh8_ok_ = bool(kh8_.get('all_verified') is True and kh8_.get('does_not_gate_core') is True and bool(kh8b_) and bool(kh8_.get('checks')) and all(c_.get('ok') is True for c_ in kh8_.get('checks')) and len(k8e_) == len(k8eb_) + 1 and _feq(k8e_[:len(k8eb_)], k8eb_) and str(k8e_[-1].get('assinatura')) == DL_.ASSINA and 'kh_n1_cobertura_v408' in str(k8e_[-1].get('ao_lado_de'))
                   and kh8_.get('verdict') == _ev(ESP, 'kh_n1_cobertura_v408') and not GUARDA.search(str(kh8_.get('verdict') or '')))
    V['cunh408d'] = {'ok': cu8_ok_, 'verdict': cu8_.get('verdict'), 'n': len(cu8_.get('verbatim') or {}), 'n_erratas': len(e8_), 'kh_ok': kh8_ok_, 'kh_verdict': kh8_.get('verdict')}
    if not cu8_ok_:
        P.append('cunhagens_v408 (HERDADA, recriada pelo rito) nao confere: as 15 falas de 04/11 (embedded_ok) e os extras iguais aos da v408 selada, as erratas E21 a E23 e a dos pisos intactas MAIS a errata E26 ao lado (assinada em nome proprio), as checagens todas ok e o veredito esperado')
    if not kh8_ok_:
        P.append('kh_n1_cobertura_v408 (HERDADO, recriado pelo rito) nao confere: checagens (pisos h2 h3 h6, tamanho minimo h8) todas ok, a errata ao lado dos pisos MAIS as da v408 selada, e o veredito esperado')
    # cunhagens_v407 (HERDADA, RECRIADA): igual ao que a v408 SELOU (as 3 falas de 03/11; as erratas E18 a E20 e a E21 ao lado, que ja' vinham da v408) MAIS a errata AO LADO da D57(d) (o pino do acervo da v407 na copia purgada), assinada em nome proprio; kh_n1_cobertura_v407 IGUAL ao que a v408 selou; o veredito e' o esperado
    cu7_ = core.get('cunhagens_v407') or {}; kh7_ = core.get('kh_n1_cobertura_v407') or {}; cu7b_ = _base_core(PK).get('cunhagens_v407') or {}; kh7b_ = _base_core(PK).get('kh_n1_cobertura_v407') or {}
    e7_ = cu7_.get('erratas') or []; e7b_ = cu7b_.get('erratas') or []; k7e_ = kh7_.get('erratas') or []; k7eb_ = kh7b_.get('erratas') or []
    cu7_ok_ = bool(cu7_.get('all_verified') is True and cu7_.get('does_not_gate_core') is True and bool(cu7b_) and bool(cu7_.get('verbatim')) and _feq(cu7_.get('verbatim'), cu7b_.get('verbatim')) and len(cu7_.get('verbatim') or {}) == len(DL_.D7.VERBATIM_ORIGEM_V407) and all((v_ or {}).get('embedded_ok') is True for v_ in (cu7_.get('verbatim') or {}).values())
                   and _feq(cu7_.get('extras'), cu7b_.get('extras')) and len(e7_) == len(e7b_) + 1 and _feq(e7_[:len(e7b_)], e7b_) and str(e7_[-1].get('agora') or '').startswith('v409, D57(d)') and e7_[-1].get('assinatura') == DL_.ASSINA
                   and bool(cu7_.get('checks')) and all(c_.get('ok') is True for c_ in cu7_.get('checks')) and cu7_.get('verdict') == _ev(ESP, 'cunhagens_v407') and not GUARDA.search(str(cu7_.get('verdict') or '')))
    kh7_ok_ = bool(kh7_.get('all_verified') is True and kh7_.get('does_not_gate_core') is True and bool(kh7b_) and bool(kh7_.get('checks')) and all(c_.get('ok') is True for c_ in kh7_.get('checks')) and bool(k7eb_) and len(k7e_) == len(k7eb_) and _feq(k7e_, k7eb_)
                   and kh7_.get('verdict') == _ev(ESP, 'kh_n1_cobertura_v407') and not GUARDA.search(str(kh7_.get('verdict') or '')))
    V['cunh407d'] = {'ok': cu7_ok_, 'verdict': cu7_.get('verdict'), 'n': len(cu7_.get('verbatim') or {}), 'n_erratas': len(e7_), 'kh_ok': kh7_ok_, 'kh_verdict': kh7_.get('verdict')}
    if not cu7_ok_:
        P.append('cunhagens_v407 (HERDADA, recriada pelo rito) nao confere: as 3 falas de 03/11 (embedded_ok) e os extras iguais aos da v408 selada, as erratas intactas MAIS a errata da D57(d) ao lado (o pino do acervo da v407 na copia purgada, assinada em nome proprio), as checagens todas ok e o veredito esperado')
    if not kh7_ok_:
        P.append('kh_n1_cobertura_v407 (HERDADO, recriado pelo rito) nao confere: checagens todas ok, as erratas IGUAIS as da v408 selada, e o veredito esperado')
"""
regiao("    # cunhagens_v408 e kh_n1_cobertura_v408 (os DOIS registros NOVOS por spec):", "    # cunhagens_v406 e kh_n1_cobertura_v406 (HERDADOS, RECRIADOS pelo rito da v409, por spec):", CUNH)
a.grava()
